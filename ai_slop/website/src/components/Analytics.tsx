'use client';

import { useEffect } from 'react';
import { getFirebaseAnalytics } from '@/lib/firebase';
import { logEvent } from 'firebase/analytics';

/**
 * Firebase Analytics Component
 *
 * Initializes analytics on mount and logs page views.
 * Gracefully handles missing configuration (no errors in dev without .env.local).
 */
export function Analytics() {
  useEffect(() => {
    const initAnalytics = async () => {
      try {
        const analytics = await getFirebaseAnalytics();
        if (analytics) {
          // Log initial page view
          logEvent(analytics, 'page_view', {
            page_title: document.title,
            page_location: window.location.href,
            page_path: window.location.pathname,
          });
        }
      } catch (error) {
        // Silently fail - analytics is non-critical
        console.debug('Analytics initialization skipped:', error);
      }
    };

    initAnalytics();
  }, []);

  // This component renders nothing - it's just for side effects
  return null;
}

export default Analytics;
