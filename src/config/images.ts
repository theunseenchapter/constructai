// Image handling configuration for ConstructAI

export const IMAGE_CONFIG = {
  // Supported image formats
  SUPPORTED_FORMATS: ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'],
  
  // Default dimensions for various use cases
  DIMENSIONS: {
    RENDER_PREVIEW: { width: 400, height: 300 },
    RENDER_FULL: { width: 800, height: 600 },
    THUMBNAIL: { width: 100, height: 75 },
    LARGE_VIEW: { width: 1200, height: 900 }
  },
  
  // URL validation patterns
  PATTERNS: {
    RELATIVE_PATH: /^\/[a-zA-Z0-9\/_.-]+\.(jpg|jpeg|png|gif|webp|svg)$/i,
    ABSOLUTE_URL: /^https?:\/\/.+\.(jpg|jpeg|png|gif|webp|svg)$/i
  },
  
  // Error handling
  FALLBACK_IMAGE: '/images/placeholder.png',
  ERROR_PLACEHOLDER: '/images/error.png',
  
  // Performance settings
  LAZY_LOADING: true,
  QUALITY: 85,
  
  // Validate image URL
  validateUrl: (url: string): boolean => {
    if (!url || typeof url !== 'string') return false;
    
    const trimmedUrl = url.trim();
    if (trimmedUrl === '') return false;
    
    // Check against patterns
    return IMAGE_CONFIG.PATTERNS.RELATIVE_PATH.test(trimmedUrl) || 
           IMAGE_CONFIG.PATTERNS.ABSOLUTE_URL.test(trimmedUrl);
  },
  
  // Normalize URL for consistent handling
  normalizeUrl: (url: string): string | null => {
    if (!url || typeof url !== 'string') return null;
    
    const trimmedUrl = url.trim();
    if (trimmedUrl === '') return null;
    
    // Handle absolute URLs
    if (trimmedUrl.startsWith('http://') || trimmedUrl.startsWith('https://')) {
      return IMAGE_CONFIG.validateUrl(trimmedUrl) ? trimmedUrl : null;
    }
    
    // Handle relative URLs
    const normalizedUrl = trimmedUrl.startsWith('/') ? trimmedUrl : `/${trimmedUrl}`;
    return IMAGE_CONFIG.validateUrl(normalizedUrl) ? normalizedUrl : null;
  }
};

export default IMAGE_CONFIG;
