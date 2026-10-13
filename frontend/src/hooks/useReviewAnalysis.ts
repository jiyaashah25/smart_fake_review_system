import { useState, useEffect, useCallback } from 'react';
import { PredictionResultData, HistoryItem } from '../types/review';
import { api } from '../services/api';

const HISTORY_STORAGE_KEY = 'reviewguard_session_history';

export const useReviewAnalysis = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<PredictionResultData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>(() => {
    try {
      const stored = sessionStorage.getItem(HISTORY_STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    try {
      sessionStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(history));
    } catch (e) {
      console.warn('Session storage limit reached:', e);
    }
  }, [history]);

  const analyzeReview = useCallback(async (reviewText: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.predictReview(reviewText);
      setResult(data);

      // Append to session history (capped at 15 items)
      const newItem: HistoryItem = {
        id: `hist_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
        text: reviewText,
        result: data,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setHistory(prev => [newItem, ...prev.slice(0, 14)]);
      return data;
    } catch (err: any) {
      const message = err.message || 'An unexpected error occurred during analysis.';
      setError(message);
      setResult(null);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const clearHistory = useCallback(() => {
    setHistory([]);
    try {
      sessionStorage.removeItem(HISTORY_STORAGE_KEY);
    } catch {}
  }, []);

  const selectHistoryItem = useCallback((item: HistoryItem) => {
    setResult(item.result);
    setError(null);
  }, []);

  return {
    loading,
    result,
    error,
    history,
    analyzeReview,
    clearHistory,
    selectHistoryItem,
    setResult,
    setError,
  };
};
