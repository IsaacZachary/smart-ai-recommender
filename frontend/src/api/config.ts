import axios from 'axios';

// API Configuration
const API_BASE_URL = process.env.NODE_ENV === 'development' 
  ? 'http://localhost:8000/api/v1'
  : 'https://your-backend-domain.com/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    // You can add any request preprocessing here
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle specific error cases
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // Handle unauthorized
          break;
        case 403:
          // Handle forbidden
          break;
        case 429:
          // Handle rate limiting
          break;
        default:
          // Handle other errors
          break;
      }
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const endpoints = {
  recommend: '/recommend',
  clarify: '/clarify',
  tip: {
    initiate: '/tip/initiate',
    callback: '/tip/callback',
  },
};

// API types
export interface RecommendationRequest {
  query: string;
  context?: Record<string, any>;
  language?: string;
}

export interface RecommendationResponse {
  clarification?: string;
  products: Product[];
  session_id: string;
  query_type: 'comparative' | 'feature_based' | 'subjective';
}

export interface Product {
  name: string;
  description: string;
  specs: ProductSpec[];
  image_url: string;
  price: Price;
  vendor_url: string;
  confidence_score: number;
}

export interface ProductSpec {
  key: string;
  value: string;
}

export interface Price {
  value: number;
  currency: string;
}

export interface TipRequest {
  phone_number: string;
  amount: number;
}

export interface TipResponse {
  transaction_id: string;
  status: string;
  message: string;
}

// API functions
export const apiService = {
  // Get product recommendations
  getRecommendations: async (data: RecommendationRequest) => {
    const response = await api.post<RecommendationResponse>(endpoints.recommend, data);
    return response.data;
  },

  // Handle clarification
  clarifyRecommendation: async (data: RecommendationRequest, sessionId: string) => {
    const response = await api.post<RecommendationResponse>(
      endpoints.clarify,
      data,
      { params: { session_id: sessionId } }
    );
    return response.data;
  },

  // Initiate M-Pesa tip
  initiateTip: async (data: TipRequest) => {
    const response = await api.post<TipResponse>(endpoints.tip.initiate, data);
    return response.data;
  },
};

export default apiService; 