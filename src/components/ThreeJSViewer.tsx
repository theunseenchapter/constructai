'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

interface ThreeJSViewerProps {
  objUrl?: string;
  mtlUrl?: string;
  width?: number;
  height?: number;
  onModelLoad?: () => void;
  onModelError?: (error: Error) => void;
}

function ThreeJSViewer(props: ThreeJSViewerProps) {
  const {
    objUrl,
    mtlUrl,
    width = 800,
    height = 600,
    onModelLoad,
    onModelError
  } = props;
  const mountRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [modelStats, setModelStats] = useState<{
    vertices: number;
    faces: number;
    materials: number;
  } | null>(null);

  // Normalize URL - ensure it's a full URL
  const normalizeUrl = (url: string | undefined): string | undefined => {
    if (!url) return undefined;
    
    // If it's already a full URL, return as is
    if (url.startsWith('http://') || url.startsWith('https://')) {
      return url;
    }
    
    // If it's a relative path, prepend the current origin
    if (url.startsWith('/')) {
      return `${window.location.origin}${url}`;
    }
    
    return url;
  };

  // Initialize Three.js scene
  useEffect(() => {
    if (!mountRef.current) return;

    console.log('🎬 ThreeJSViewer: Initializing Three.js scene');

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    sceneRef.current = scene;

    // Camera setup
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.set(10, 10, 10);
    camera.lookAt(0, 0, 0);
    cameraRef.current = camera;

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    rendererRef.current = renderer;

    // Controls setup
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controlsRef.current = controls;

    // Lighting setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    // Add to DOM
    const mountElement = mountRef.current;
    mountElement.appendChild(renderer.domElement);

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    console.log('✅ ThreeJSViewer: Three.js scene initialized');

    // Cleanup
    return () => {
      if (mountElement && renderer.domElement && mountElement.contains(renderer.domElement)) {
        mountElement.removeChild(renderer.domElement);
      }
      renderer.dispose();
      controls.dispose();
    };
  }, [width, height]);

  // Load 3D model
  useEffect(() => {
    if (!objUrl || !sceneRef.current) {
      console.log('🚫 ThreeJSViewer: No objUrl provided or scene not ready');
      return;
    }

    const normalizedObjUrl = normalizeUrl(objUrl);
    const normalizedMtlUrl = normalizeUrl(mtlUrl);
    
    if (!normalizedObjUrl) {
      console.log('🚫 ThreeJSViewer: Invalid OBJ URL');
      return;
    }

    console.log('🔄 ThreeJSViewer: Loading model:', { 
      objUrl: normalizedObjUrl, 
      mtlUrl: normalizedMtlUrl 
    });
    
    setIsLoading(true);
    setError(null);
    setModelStats(null);

    // Clear previous model
    const scene = sceneRef.current;
    const objectsToRemove = scene.children.filter(child => 
      child.userData.isModel || child.type === 'Group'
    );
    objectsToRemove.forEach(obj => scene.remove(obj));

    const loadModel = async () => {
      try {
        let materials: THREE.Material[] = [];
        
        // Load materials if MTL file is provided
        if (normalizedMtlUrl) {
          console.log('📦 ThreeJSViewer: Loading MTL file:', normalizedMtlUrl);
          const mtlLoader = new MTLLoader();
          
          try {
            const mtlData = await new Promise<{ materials: Record<string, THREE.Material>; preload: () => void }>((resolve, reject) => {
              mtlLoader.load(
                normalizedMtlUrl,
                resolve,
                (progress) => {
                  console.log('📊 ThreeJSViewer: MTL loading progress:', progress);
                },
                reject
              );
            });
            
            mtlData.preload();
            materials = Object.values(mtlData.materials);
            console.log('✅ ThreeJSViewer: MTL loaded successfully, materials:', materials.length);
          } catch (mtlError) {
            console.warn('⚠️ ThreeJSViewer: MTL loading failed:', mtlError);
            // Continue without materials
          }
        }

        // Load OBJ file
        console.log('📦 ThreeJSViewer: Loading OBJ file:', normalizedObjUrl);
        const objLoader = new OBJLoader();
        
        const object = await new Promise<THREE.Group>((resolve, reject) => {
          objLoader.load(
            normalizedObjUrl,
            resolve,
            (progress) => {
              console.log('📊 ThreeJSViewer: OBJ loading progress:', progress);
            },
            reject
          );
        });

        console.log('✅ ThreeJSViewer: OBJ loaded successfully');
        
        // Calculate model statistics
        let vertexCount = 0;
        let faceCount = 0;
        let materialCount = 0;
        
        object.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            const geometry = child.geometry;
            if (geometry.attributes.position) {
              vertexCount += geometry.attributes.position.count;
            }
            if (geometry.index) {
              faceCount += geometry.index.count / 3;
            }
            if (child.material) {
              materialCount++;
            }
          }
        });

        const stats = {
          vertices: vertexCount,
          faces: Math.floor(faceCount),
          materials: materialCount
        };
        
        console.log('📊 ThreeJSViewer: Model statistics:', stats);
        setModelStats(stats);

        // Apply materials if loaded
        if (materials.length > 0) {
          console.log('🎨 ThreeJSViewer: Applying materials to model');
          let materialIndex = 0;
          object.traverse((child) => {
            if (child instanceof THREE.Mesh && materialIndex < materials.length) {
              child.material = materials[materialIndex % materials.length];
              materialIndex++;
            }
          });
        }

        // Position and scale the model
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        
        console.log('📏 ThreeJSViewer: Model bounds:', { center, size });
        
        // Center the model
        object.position.sub(center);
        
        // Scale to fit in view
        const maxSize = Math.max(size.x, size.y, size.z);
        if (maxSize > 0) {
          const scale = 8 / maxSize;
          object.scale.setScalar(scale);
          console.log('📏 ThreeJSViewer: Applied scale:', scale);
        }

        // Mark as model for cleanup
        object.userData.isModel = true;
        
        // Add to scene
        scene.add(object);
        
        // Update camera position based on model size
        if (cameraRef.current) {
          const scaledSize = maxSize * (8 / maxSize);
          cameraRef.current.position.set(
            scaledSize * 1.5,
            scaledSize * 1.5,
            scaledSize * 1.5
          );
          cameraRef.current.lookAt(0, 0, 0);
        }

        console.log('✅ ThreeJSViewer: Model added to scene successfully');
        setIsLoading(false);
        onModelLoad?.();
        
      } catch (error) {
        console.error('❌ ThreeJSViewer: Model loading error:', error);
        setError(error instanceof Error ? error.message : 'Failed to load model');
        setIsLoading(false);
        onModelError?.(error instanceof Error ? error : new Error('Failed to load model'));
      }
    };

    loadModel();
  }, [objUrl, mtlUrl, onModelLoad, onModelError]);

  return (
    <div className="relative">
      <div ref={mountRef} className="border border-gray-300 rounded-lg overflow-hidden" />
      
      {/* Loading overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center rounded-lg">
          <div className="text-white text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-2"></div>
            <p>Loading 3D Model...</p>
          </div>
        </div>
      )}
      
      {/* Error display */}
      {error && (
        <div className="absolute inset-0 bg-red-500 bg-opacity-90 flex items-center justify-center rounded-lg">
          <div className="text-white text-center p-4">
            <p className="font-semibold mb-2">Error Loading Model</p>
            <p className="text-sm">{error}</p>
          </div>
        </div>
      )}
      
      {/* Model stats */}
      {modelStats && (
        <div className="absolute top-2 left-2 bg-black bg-opacity-70 text-white text-xs p-2 rounded">
          <div>Vertices: {modelStats.vertices.toLocaleString()}</div>
          <div>Faces: {modelStats.faces.toLocaleString()}</div>
          <div>Materials: {modelStats.materials}</div>
        </div>
      )}
      
      {/* Debug info */}
      {process.env.NODE_ENV === 'development' && (
        <div className="absolute bottom-2 left-2 bg-blue-500 bg-opacity-70 text-white text-xs p-2 rounded max-w-xs overflow-hidden">
          <div>OBJ: {objUrl ? `${objUrl.substring(0, 50)}...` : 'Not set'}</div>
          <div>MTL: {mtlUrl ? `${mtlUrl.substring(0, 50)}...` : 'Not set'}</div>
          <div>Loading: {isLoading ? 'Yes' : 'No'}</div>
          <div>Error: {error ? error.substring(0, 30) : 'None'}</div>
        </div>
      )}
      
      {/* No model message */}
      {!objUrl && !isLoading && !error && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-gray-500">
            <p className="text-sm">No 3D model URL provided</p>
            <p className="text-xs mt-1">Generate a model to view it here</p>
          </div>
        </div>
      )}
    </div>
  );
};

ThreeJSViewer.displayName = 'ThreeJSViewer';

export default ThreeJSViewer;
