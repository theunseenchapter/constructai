'use client';

import React from 'react';
import ThreeD3DRoomViewer from './ThreeD3DRoomViewer';

const Test3DViewer = () => {
  const testRooms = [
    {
      id: 'room1',
      name: 'Living Room',
      type: 'living room',
      area: 25,
      width: 5,
      height: 3,
      length: 5,
      position: { x: 0, y: 0, z: 0 }
    }
  ];

  const testDimensions = {
    total_width: 10,
    total_length: 10,
    height: 3
  };

  return (
    <div>
      <h2>Test 3D Viewer</h2>
      <ThreeD3DRoomViewer
        rooms={testRooms}
        buildingDimensions={testDimensions}
      />
    </div>
  );
};

export default Test3DViewer;
