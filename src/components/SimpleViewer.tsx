import React from 'react';
import { SimpleViewerProps } from '@/types';

const SimpleViewer: React.FC<SimpleViewerProps> = ({
  rooms,
  buildingDimensions,
  className = '',
}) => {
  return (
    <div className={`relative w-full h-96 bg-gray-50 rounded-lg overflow-hidden ${className}`}>
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <h3 className="text-lg font-semibold mb-2">3D Viewer</h3>
          <p className="text-gray-600">
            {rooms.length} rooms | {buildingDimensions.total_width}x{buildingDimensions.total_length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default SimpleViewer;
