import {
  PredictionResultData,
  AnalyticsData
} from '../types/review';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

class ApiError extends Error {
  statusCode?: number;
  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMsg = `Server error (${response.status})`;
    try {
      const errorJson = await response.json();
      errorMsg = errorJson.message || errorJson.detail || errorMsg;
    } catch {
      // Fallback to status text
      errorMsg = response.statusText || errorMsg;
    }
    throw new ApiError(errorMsg, response.status);
  }
  return response.json();
}

export const api = {
  getBaseUrl(): string {
    return API_BASE_URL;
  },

  async checkHealth(): Promise<{ status: string; model_loaded: boolean; model_name?: string }> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
      });
      return handleResponse(response);
    } catch (err: any) {
      throw new ApiError(
        err.message?.includes('Failed to fetch')
          ? 'Cannot reach ReviewGuard backend. Ensure the server is running on http://127.0.0.1:8000'
          : err.message
      );
    }
  },

  async predictReview(reviewText: string): Promise<PredictionResultData> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ review_text: reviewText }),
      });
      return handleResponse<PredictionResultData>(response);
    } catch (err: any) {
      if (err instanceof ApiError) throw err;
      throw new ApiError(
        err.message?.includes('Failed to fetch')
          ? 'Network error: Backend server is unreachable at ' + API_BASE_URL
          : err.message
      );
    }
  },


  async getAnalytics(): Promise<AnalyticsData> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/analytics`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
      });
      return handleResponse<AnalyticsData>(response);
    } catch (err: any) {
      if (err instanceof ApiError) throw err;
      throw new ApiError(
        err.message?.includes('Failed to fetch')
          ? 'Unable to connect to backend for analytics telemetry.'
          : err.message
      );
    }
  },
};
