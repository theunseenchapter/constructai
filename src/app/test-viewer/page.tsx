'use client';

import React from 'react';
import ThreeJSViewer from '../../components/ThreeJSViewer';

export default function TestThreeJSViewer() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Test ThreeJSViewer Component</h1>
      <div className="border rounded-lg overflow-hidden">
        <ThreeJSViewer
          objUrl="/renders/professional_3d.obj"
          mtlUrl="/renders/professional_3d.mtl"
          width={800}
          height={600}
          onModelLoad={() => console.log('✅ Test: 3D model loaded successfully')}
          onModelError={(error: Error) => console.error('❌ Test: 3D viewer error:', error)}
        />
      </div>
    </div>
  );
}
