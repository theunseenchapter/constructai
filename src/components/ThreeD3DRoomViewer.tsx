'use client';

import React from 'react';

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
  const handleRoomClick = (roomId: string) => {
    if (onRoomSelect) {
      onRoomSelect(roomId);
    }
  };

  return (
    <div className={`relative w-full h-96 bg-gradient-to-br from-blue-50 to-gray-100 rounded-lg overflow-hidden border ${className}`}>
      <div className="absolute inset-0 bg-gradient-to-t from-gray-200/20 to-transparent"></div>
      
      {/* Room Layout Visualization */}
      <div className="flex items-center justify-center h-full relative">
        <div className="grid grid-cols-2 gap-4 p-8">
          {rooms.slice(0, 4).map((room) => (
            <div
              key={room.id}
              className="bg-white/80 backdrop-blur-sm rounded-lg p-4 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:scale-105"
              onClick={() => handleRoomClick(room.id)}
            >
              <div className="text-center">
                <div className="text-2xl mb-2">
                  {room.type === 'bedroom' ? '🛏️' : 
                   room.type === 'kitchen' ? '�' : 
                   room.type === 'bathroom' ? '🚿' : 
                   room.type === 'living room' ? '🛋️' : '�🏠'}
                </div>
                <h4 className="font-semibold text-sm text-gray-800">{room.name}</h4>
                <p className="text-xs text-gray-600">{room.area}m²</p>
                <div className="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-blue-500 transition-all duration-500"
                    style={{ width: `${Math.min(100, (room.area / 50) * 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Building Info */}
      <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-3 shadow-lg">
        <div className="text-xs text-gray-600 space-y-1">
          <div className="font-semibold">Building Overview</div>
          <div>📐 {rooms.length} rooms</div>
          <div>📏 {rooms.reduce((total, room) => total + room.area, 0)}m² total</div>
          <div>🏢 {buildingDimensions.total_width}m × {buildingDimensions.total_length}m</div>
        </div>
      </div>

      {/* Controls overlay */}
      <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-2 shadow-lg">
        <div className="text-xs text-gray-600 space-y-1">
          <div>🖱️ Click rooms to select</div>
          <div>🔍 Interactive room layout</div>
          <div>� {rooms.length} rooms configured</div>
        </div>
      </div>

      {/* 3D Effect Indicator */}
      <div className="absolute top-4 right-4 bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-semibold">
        3D Layout View
      </div>
    </div>
  );
};

export default ThreeD3DRoomViewer;