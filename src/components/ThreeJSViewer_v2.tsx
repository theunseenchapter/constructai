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
    
    // Assume it's a relative path from current directory
    return `${window.location.origin}/${url}`;
  };

  // Initialize Three.js scene
  useEffect(() => {
    if (!mountRef.current) return;

    console.log('🎬 ThreeJSViewer: Initializing Three.js scene');

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);
    sceneRef.current = scene;

    // Camera
    const camera = new THREE.PerspectiveCamera(
      75,
      width / height,
      0.1,
      1000
    );
    camera.position.set(5, 5, 5);
    cameraRef.current = camera;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    rendererRef.current = renderer;

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 1;
    controls.maxDistance = 50;
    controlsRef.current = controls;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    // Mount renderer
    mountRef.current.appendChild(renderer.domElement);

    console.log('✅ ThreeJSViewer: Three.js scene initialized');

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // Cleanup
    return () => {
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [width, height]);

  // Load model when URLs change
  useEffect(() => {
    if (!objUrl || !sceneRef.current) {
      console.log('🚫 ThreeJSViewer: No objUrl provided or scene not ready');
      return;
    }

    const normalizedObjUrl = normalizeUrl(objUrl);
    const normalizedMtlUrl = normalizeUrl(mtlUrl);

    if (!normalizedObjUrl || normalizedObjUrl === window.location.origin + '/undefined') {
      console.log('🚫 ThreeJSViewer: Invalid OBJ URL');
      return;
    }

    console.log('🔄 ThreeJSViewer: Loading model:', { 
      objUrl: normalizedObjUrl, 
      mtlUrl: normalizedMtlUrl 
    });

    setIsLoading(true);
    setError(null);

    // Clear existing models
    const scene = sceneRef.current;
    const modelsToRemove = scene.children.filter(child => child.userData.isModel);
    modelsToRemove.forEach(model => scene.remove(model));

    const loadModel = async () => {
      try {
        let materials: THREE.Material[] = [];

        // Load MTL file first if provided
        if (normalizedMtlUrl) {
          console.log('📦 ThreeJSViewer: Loading MTL file:', normalizedMtlUrl);
          const mtlLoader = new MTLLoader();
          
          try {
            const materialCreator = await new Promise<any>((resolve, reject) => {
              mtlLoader.load(
                normalizedMtlUrl,
                resolve,
                (progress) => console.log('📊 ThreeJSViewer: MTL loading progress:', progress),
                reject
              );
            });
            
            materialCreator.preload();
            materials = Object.values(materialCreator.materials) as THREE.Material[];
            console.log('✅ ThreeJSViewer: MTL loaded successfully, materials:', materials.length);
          } catch (mtlError) {
            console.warn('⚠️ ThreeJSViewer: MTL loading failed:', mtlError);
          }
        }

        // Load OBJ file
        console.log('📦 ThreeJSViewer: Loading OBJ file:', normalizedObjUrl);
        const objLoader = new OBJLoader();

        const object = await new Promise<THREE.Group>((resolve, reject) => {
          objLoader.load(
            normalizedObjUrl,
            resolve,
            (progress) => console.log('📊 ThreeJSViewer: OBJ loading progress:', progress),
            reject
          );
        });

        console.log('✅ ThreeJSViewer: OBJ loaded successfully');

        // Mark as model for cleanup
        object.userData.isModel = true;

        // Calculate model statistics
        let vertices = 0;
        let faces = 0;
        
        object.traverse((child) => {
          if (child instanceof THREE.Mesh && child.geometry) {
            if (child.geometry.attributes.position) {
              vertices += child.geometry.attributes.position.count;
            }
            if (child.geometry.index) {
              faces += child.geometry.index.count / 3;
            }
          }
        });

        const stats = {
          vertices,
          faces,
          materials: materials.length
        };

        console.log('📊 ThreeJSViewer: Model statistics:', stats);

        // Apply materials if available
        if (materials.length > 0) {
          console.log('🎨 ThreeJSViewer: Applying materials to model');
          object.traverse((child) => {
            if (child instanceof THREE.Mesh) {
              const materialName = child.material?.name || child.name;
              const matchingMaterial = materials.find(mat => mat.name === materialName);
              if (matchingMaterial) {
                child.material = matchingMaterial;
              }
            }
          });
        }

        // Calculate bounding box for auto-centering and scaling
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        console.log('📏 ThreeJSViewer: Model bounds:', { center, size });

        // Center the model
        object.position.sub(center);

        // Scale model to fit in view (max dimension should be ~3 units)
        const maxDimension = Math.max(size.x, size.y, size.z);
        if (maxDimension > 0) {
          const scale = 3 / maxDimension;
          object.scale.setScalar(scale);
          console.log('📏 ThreeJSViewer: Applied scale:', scale);
        }

        // Add to scene
        scene.add(object);

        // Position camera to view the model
        if (cameraRef.current && controlsRef.current) {
          const camera = cameraRef.current;
          const controls = controlsRef.current;
          
          // Set camera position
          camera.position.set(5, 5, 5);
          camera.lookAt(0, 0, 0);
          
          // Update controls target
          controls.target.set(0, 0, 0);
          controls.update();
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
      <div 
        ref={mountRef} 
        style={{ width, height }}
        className="border rounded overflow-hidden"
      />
      
      {isLoading && (
        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center text-white">
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
            <span>Loading 3D model...</span>
          </div>
        </div>
      )}

      {error && (
        <div className="absolute inset-0 bg-red-500 bg-opacity-90 flex items-center justify-center text-white p-4">
          <div className="text-center">
            <div className="text-lg font-semibold mb-2">Error loading model</div>
            <div className="text-sm">{error}</div>
          </div>
        </div>
      )}

      {!isLoading && !error && objUrl && (
        <div className="absolute bottom-2 left-2 bg-black bg-opacity-70 text-white px-2 py-1 rounded text-xs">
          3D Model Viewer
        </div>
      )}
    </div>
  );
}

export default ThreeJSViewer;
