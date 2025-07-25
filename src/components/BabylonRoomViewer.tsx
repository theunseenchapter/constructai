'use client';

import React, { useRef, useEffect, useState } from 'react';
import { Engine, Scene, ArcRotateCamera, Vector3, HemisphericLight, DirectionalLight, MeshBuilder, Color3, PBRMaterial, EnvironmentHelper, ShadowGenerator, PointLight, Mesh } from '@babylonjs/core';

// Interface definitions to match Enhanced3DBOQ requirements
interface RoomData {
  id: string;
  name: string;
  type: string;
  area: number;
  width: number;
  height: number;
  length: number;
  position: { x: number; y: number; z: number };
  materials?: Array<{
    type: string;
    area: number;
    cost: number;
    finish: string;
  }>;
  fixtures?: Array<{
    type: string;
    quantity: number;
    cost: number;
    position: { x: number; y: number; z: number };
  }>;
}

interface BuildingDimensions {
  total_width: number;
  total_length: number;
  height: number;
}

interface ThreeD3DRoomViewerProps {
  rooms: RoomData[];
  buildingDimensions: BuildingDimensions;
  onRoomSelect?: (roomId: string) => void;
  className?: string;
}

const ThreeD3DRoomViewer: React.FC<ThreeD3DRoomViewerProps> = ({
  rooms,
  buildingDimensions,
  onRoomSelect,
  className = '',
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const engineRef = useRef<Engine | null>(null);
  const sceneRef = useRef<Scene | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Create realistic PBR materials
  const createRealisticMaterials = (scene: Scene) => {
    const materials = {
      // Wall materials
      drywall: new PBRMaterial('drywall', scene),
      brick: new PBRMaterial('brick', scene),
      concrete: new PBRMaterial('concrete', scene),
      
      // Floor materials
      hardwood: new PBRMaterial('hardwood', scene),
      tile: new PBRMaterial('tile', scene),
      carpet: new PBRMaterial('carpet', scene),
      
      // Ceiling materials
      ceiling: new PBRMaterial('ceiling', scene),
      
      // Furniture materials
      wood: new PBRMaterial('wood', scene),
      metal: new PBRMaterial('metal', scene),
      glass: new PBRMaterial('glass', scene),
      fabric: new PBRMaterial('fabric', scene),
    };

    // Configure drywall
    materials.drywall.albedoColor = Color3.FromHexString('#f5f5f5');
    materials.drywall.roughness = 0.8;
    materials.drywall.metallic = 0.0;

    // Configure brick
    materials.brick.albedoColor = Color3.FromHexString('#8b4513');
    materials.brick.roughness = 0.9;
    materials.brick.metallic = 0.0;

    // Configure concrete
    materials.concrete.albedoColor = Color3.FromHexString('#888888');
    materials.concrete.roughness = 0.7;
    materials.concrete.metallic = 0.0;

    // Configure hardwood
    materials.hardwood.albedoColor = Color3.FromHexString('#8B4513');
    materials.hardwood.roughness = 0.2;
    materials.hardwood.metallic = 0.0;

    // Configure tile
    materials.tile.albedoColor = Color3.FromHexString('#ffffff');
    materials.tile.roughness = 0.1;
    materials.tile.metallic = 0.0;

    // Configure carpet
    materials.carpet.albedoColor = Color3.FromHexString('#8fbc8f');
    materials.carpet.roughness = 0.9;
    materials.carpet.metallic = 0.0;

    // Configure ceiling
    materials.ceiling.albedoColor = Color3.FromHexString('#ffffff');
    materials.ceiling.roughness = 0.6;
    materials.ceiling.metallic = 0.0;

    // Configure wood
    materials.wood.albedoColor = Color3.FromHexString('#8B4513');
    materials.wood.roughness = 0.3;
    materials.wood.metallic = 0.0;

    // Configure metal
    materials.metal.albedoColor = Color3.FromHexString('#888888');
    materials.metal.roughness = 0.2;
    materials.metal.metallic = 0.8;

    // Configure glass
    materials.glass.albedoColor = Color3.FromHexString('#ffffff');
    materials.glass.roughness = 0.0;
    materials.glass.metallic = 0.0;
    materials.glass.alpha = 0.3;

    // Configure fabric
    materials.fabric.albedoColor = Color3.FromHexString('#4169e1');
    materials.fabric.roughness = 0.8;
    materials.fabric.metallic = 0.0;

    return materials;
  };

  // Generate furniture based on room type
  const generateFurniture = (room: RoomData, scene: Scene, materials: Record<string, PBRMaterial>) => {
    const furniture: Mesh[] = [];

    switch (room.type.toLowerCase()) {
      case 'bedroom':
        // Bed
        const bedFrame = MeshBuilder.CreateBox('bedFrame', { width: 2, height: 0.5, depth: 1.5 }, scene);
        bedFrame.material = materials.wood;
        bedFrame.position = new Vector3(room.position.x, room.position.y + 0.25, room.position.z - 1);
        furniture.push(bedFrame);

        const mattress = MeshBuilder.CreateBox('mattress', { width: 1.9, height: 0.3, depth: 1.4 }, scene);
        mattress.material = materials.fabric;
        mattress.position = new Vector3(room.position.x, room.position.y + 0.65, room.position.z - 1);
        furniture.push(mattress);

        // Nightstand
        const nightstand = MeshBuilder.CreateBox('nightstand', { width: 0.5, height: 0.6, depth: 0.4 }, scene);
        nightstand.material = materials.wood;
        nightstand.position = new Vector3(room.position.x + 1.5, room.position.y + 0.3, room.position.z - 1);
        furniture.push(nightstand);
        break;

      case 'kitchen':
        // Kitchen island
        const island = MeshBuilder.CreateBox('island', { width: 2, height: 0.9, depth: 1 }, scene);
        island.material = materials.wood;
        island.position = new Vector3(room.position.x, room.position.y + 0.45, room.position.z);
        furniture.push(island);

        // Cabinets
        const cabinet = MeshBuilder.CreateBox('cabinet', { width: 3, height: 2, depth: 0.6 }, scene);
        cabinet.material = materials.wood;
        cabinet.position = new Vector3(room.position.x + 1, room.position.y + 1, room.position.z + 2);
        furniture.push(cabinet);
        break;

      case 'living room':
        // Sofa base
        const sofaBase = MeshBuilder.CreateBox('sofaBase', { width: 2.5, height: 0.8, depth: 1 }, scene);
        sofaBase.material = materials.fabric;
        sofaBase.position = new Vector3(room.position.x, room.position.y + 0.4, room.position.z);
        furniture.push(sofaBase);

        // Sofa back
        const sofaBack = MeshBuilder.CreateBox('sofaBack', { width: 2.5, height: 0.8, depth: 0.2 }, scene);
        sofaBack.material = materials.fabric;
        sofaBack.position = new Vector3(room.position.x, room.position.y + 0.8, room.position.z - 0.4);
        furniture.push(sofaBack);

        // Coffee table
        const coffeeTable = MeshBuilder.CreateBox('coffeeTable', { width: 1.2, height: 0.4, depth: 0.8 }, scene);
        coffeeTable.material = materials.wood;
        coffeeTable.position = new Vector3(room.position.x, room.position.y + 0.2, room.position.z + 1.5);
        furniture.push(coffeeTable);
        break;

      case 'bathroom':
        // Toilet base
        const toiletBase = MeshBuilder.CreateBox('toiletBase', { width: 0.4, height: 0.4, depth: 0.7 }, scene);
        toiletBase.material = materials.tile;
        toiletBase.position = new Vector3(room.position.x + 1, room.position.y + 0.2, room.position.z + 1);
        furniture.push(toiletBase);

        // Toilet tank
        const toiletTank = MeshBuilder.CreateBox('toiletTank', { width: 0.4, height: 0.5, depth: 0.2 }, scene);
        toiletTank.material = materials.tile;
        toiletTank.position = new Vector3(room.position.x + 1, room.position.y + 0.5, room.position.z + 0.75);
        furniture.push(toiletTank);

        // Sink
        const sink = MeshBuilder.CreateBox('sink', { width: 0.6, height: 0.8, depth: 0.4 }, scene);
        sink.material = materials.tile;
        sink.position = new Vector3(room.position.x - 1, room.position.y + 0.4, room.position.z + 1);
        furniture.push(sink);
        break;
    }

    return furniture;
  };

  // Create realistic lighting setup
  const setupLighting = (scene: Scene) => {
    // Ambient light
    const ambientLight = new HemisphericLight('ambientLight', new Vector3(0, 1, 0), scene);
    ambientLight.intensity = 0.3;

    // Main directional light (sun)
    const directionalLight = new DirectionalLight('directionalLight', new Vector3(-1, -1, -1), scene);
    directionalLight.intensity = 0.8;
    directionalLight.position = new Vector3(10, 15, 10);

    // Shadow generator
    const shadowGenerator = new ShadowGenerator(2048, directionalLight);
    shadowGenerator.useExponentialShadowMap = true;

    // Additional point lights for interior lighting
    const pointLight1 = new PointLight('pointLight1', new Vector3(0, 8, 0), scene);
    pointLight1.intensity = 0.5;
    pointLight1.range = 10;

    const pointLight2 = new PointLight('pointLight2', new Vector3(-5, 6, 5), scene);
    pointLight2.intensity = 0.3;
    pointLight2.range = 8;

    return { shadowGenerator, directionalLight, pointLight1, pointLight2 };
  };

  // Create room geometry
  const createRoomGeometry = (room: RoomData, scene: Scene, materials: Record<string, PBRMaterial>, shadowGenerator: ShadowGenerator) => {
    const roomMeshes: Mesh[] = [];
    
    // Floor
    const floor = MeshBuilder.CreateGround('floor', { width: room.width, height: room.length }, scene);
    floor.material = materials.hardwood;
    floor.position = new Vector3(room.position.x, room.position.y, room.position.z);
    floor.receiveShadows = true;
    roomMeshes.push(floor);

    // Ceiling
    const ceiling = MeshBuilder.CreateGround('ceiling', { width: room.width, height: room.length }, scene);
    ceiling.material = materials.ceiling;
    ceiling.position = new Vector3(room.position.x, room.position.y + room.height, room.position.z);
    ceiling.rotation.x = Math.PI;
    ceiling.receiveShadows = true;
    roomMeshes.push(ceiling);

    // Walls
    const wallThickness = 0.1;
    
    // Front wall
    const frontWall = MeshBuilder.CreateBox('frontWall', { width: room.width, height: room.height, depth: wallThickness }, scene);
    frontWall.material = materials.drywall;
    frontWall.position = new Vector3(room.position.x, room.position.y + room.height / 2, room.position.z + room.length / 2);
    frontWall.receiveShadows = true;
    shadowGenerator.addShadowCaster(frontWall);
    roomMeshes.push(frontWall);

    // Back wall
    const backWall = MeshBuilder.CreateBox('backWall', { width: room.width, height: room.height, depth: wallThickness }, scene);
    backWall.material = materials.drywall;
    backWall.position = new Vector3(room.position.x, room.position.y + room.height / 2, room.position.z - room.length / 2);
    backWall.receiveShadows = true;
    shadowGenerator.addShadowCaster(backWall);
    roomMeshes.push(backWall);

    // Left wall
    const leftWall = MeshBuilder.CreateBox('leftWall', { width: wallThickness, height: room.height, depth: room.length }, scene);
    leftWall.material = materials.drywall;
    leftWall.position = new Vector3(room.position.x - room.width / 2, room.position.y + room.height / 2, room.position.z);
    leftWall.receiveShadows = true;
    shadowGenerator.addShadowCaster(leftWall);
    roomMeshes.push(leftWall);

    // Right wall
    const rightWall = MeshBuilder.CreateBox('rightWall', { width: wallThickness, height: room.height, depth: room.length }, scene);
    rightWall.material = materials.drywall;
    rightWall.position = new Vector3(room.position.x + room.width / 2, room.position.y + room.height / 2, room.position.z);
    rightWall.receiveShadows = true;
    shadowGenerator.addShadowCaster(rightWall);
    roomMeshes.push(rightWall);

    return roomMeshes;
  };

  // Initialize Babylon.js scene
  useEffect(() => {
    if (!canvasRef.current) return;

    try {
      // Create engine
      const engine = new Engine(canvasRef.current, true, { 
        preserveDrawingBuffer: true, 
        stencil: true,
        antialias: true,
        adaptToDeviceRatio: true
      });
      engineRef.current = engine;

      // Create scene
      const scene = new Scene(engine);
      scene.clearColor = Color3.FromHexString('#87ceeb').toColor4(); // Sky blue background
      sceneRef.current = scene;

      // Create camera
      const camera = new ArcRotateCamera('camera', -Math.PI / 2, Math.PI / 3, 20, Vector3.Zero(), scene);
      camera.setTarget(Vector3.Zero());
      camera.attachControl(canvasRef.current, true);
      camera.wheelPrecision = 50;
      camera.minZ = 0.1;
      camera.maxZ = 100;

      // Setup lighting
      const { shadowGenerator } = setupLighting(scene);

      // Create materials
      const materials = createRealisticMaterials(scene);

      // Generate rooms and furniture
      rooms.forEach((room) => {
        createRoomGeometry(room, scene, materials, shadowGenerator);
        const furniture = generateFurniture(room, scene, materials);
        
        // Add furniture to shadow generator
        furniture.forEach(item => {
          shadowGenerator.addShadowCaster(item);
        });
      });

      // Environment for realistic lighting
      new EnvironmentHelper({
        skyboxSize: 100,
        groundColor: new Color3(0.5, 0.5, 0.5),
        skyboxColor: new Color3(0.53, 0.81, 0.92),
        enableGroundShadow: true,
        groundShadowLevel: 0.4
      }, scene);

      // Start render loop
      engine.runRenderLoop(() => {
        scene.render();
      });

      // Handle window resize
      const handleResize = () => {
        engine.resize();
      };
      window.addEventListener('resize', handleResize);

      setIsLoading(false);

      // Cleanup
      return () => {
        window.removeEventListener('resize', handleResize);
        engine.dispose();
      };
    } catch (err) {
      console.error('Error initializing Babylon.js scene:', err);
      setError('Failed to initialize 3D viewer');
      setIsLoading(false);
    }
  }, [rooms, buildingDimensions]);

  // Handle room selection
  const handleRoomClick = () => {
    if (!onRoomSelect) return;
    
    const roomId = rooms[0]?.id || '';
    onRoomSelect(roomId);
  };

  if (error) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-100 rounded-lg">
        <div className="text-center">
          <div className="text-red-500 mb-2">⚠️</div>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`relative w-full h-96 bg-gray-50 rounded-lg overflow-hidden ${className}`}>
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 z-10">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
            <p className="text-gray-600">Loading 3D visualization...</p>
          </div>
        </div>
      )}
      
      <canvas 
        ref={canvasRef} 
        className="w-full h-full cursor-grab active:cursor-grabbing"
        onClick={handleRoomClick}
      />
      
      {/* Controls overlay */}
      <div className="absolute top-4 left-4 bg-white bg-opacity-90 rounded-lg p-2 shadow-lg">
        <div className="text-xs text-gray-600 space-y-1">
          <div>🖱️ Click and drag to rotate</div>
          <div>🔍 Scroll to zoom</div>
          <div>📐 {rooms.length} rooms</div>
          <div>📏 {rooms.reduce((total, room) => total + room.area, 0)}m² total</div>
        </div>
      </div>

      {/* Babylon.js indicator */}
      <div className="absolute top-4 right-4 bg-purple-500 text-white px-3 py-1 rounded-full text-xs font-semibold">
        Babylon.js 3D
      </div>
    </div>
  );
};

export default ThreeD3DRoomViewer;
