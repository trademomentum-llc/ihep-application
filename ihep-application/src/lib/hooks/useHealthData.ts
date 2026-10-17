// lib/hooks/useHealthData.ts
'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';

interface WellnessMetrics {
  heartRate: number;
  bloodPressureSystolic: number;
  bloodPressureDiastolic: number;
  oxygenSaturation: number;
  temperature: number;
  viralLoad?: number;
  cd4Count?: number;
  lastUpdated: string;
}

export function useHealthData() {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState<WellnessMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initial load: state already starts as loading/no-error.
  const fetchMetrics = async () => {
    if (!user) return;
    
    try {
      const response = await fetch('/api/health/metrics', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        },
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch health metrics');
      }
      
      const data = await response.json();
      setMetrics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // User-triggered reload: show the spinner and clear stale errors first.
  const refreshMetrics = async () => {
    if (!user) return;
    setLoading(true);
    setError(null);
    await fetchMetrics();
  };

  useEffect(() => {
    if (!user) return;
    // Start the fetch from a microtask so no setState runs synchronously in
    // the effect body (react-hooks/set-state-in-effect).
    let cancelled = false;
    queueMicrotask(() => {
      if (!cancelled) void fetchMetrics();
    });
    return () => {
      cancelled = true;
    };
  }, [user]);

  return { metrics, loading, error, refreshMetrics };
}
