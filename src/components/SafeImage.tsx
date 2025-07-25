import React from 'react';
import IMAGE_CONFIG from '@/config/images';

interface SafeImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  onClick?: () => void;
  onError?: (e: React.SyntheticEvent<HTMLImageElement, Event>) => void;
}

const SafeImage: React.FC<SafeImageProps> = ({
  src,
  alt,
  width,
  height,
  className = '',
  onClick,
  onError
}) => {
  // Always ensure leading slash for relative paths
  let safeUrl = src;
  if (safeUrl && !safeUrl.startsWith('/') && !safeUrl.startsWith('http')) {
    safeUrl = '/' + safeUrl;
  }
  const normalizedUrl = IMAGE_CONFIG.normalizeUrl(safeUrl);
  if (!normalizedUrl) {
    console.warn(`SafeImage: Invalid or unsafe URL provided: ${src}`);
    return (
      <div 
        className={`bg-gray-200 flex items-center justify-center ${className}`}
        style={{ width, height }}
      >
        <span className="text-gray-500 text-sm">Invalid Image</span>
      </div>
    );
  }


  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={normalizedUrl}
      alt={alt}
      width={width}
      height={height}
      className={className}
      onClick={onClick}
      onError={(e) => {
        console.error(`SafeImage: Failed to load image: ${normalizedUrl}`);
        if (onError) {
          onError(e);
        } else {
          // Default error handling - hide the image
          e.currentTarget.style.display = 'none';
        }
      }}
      loading={IMAGE_CONFIG.LAZY_LOADING ? "lazy" : undefined}
    />
  );
};

export default SafeImage;
