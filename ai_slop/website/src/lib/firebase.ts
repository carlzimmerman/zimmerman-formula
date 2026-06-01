/**
 * Firebase Client Configuration
 *
 * NOTE: Firebase client config values are designed to be public.
 * Security is enforced via:
 * 1. Domain restrictions on API keys (Google Cloud Console)
 * 2. Firebase Security Rules (for Firestore/Database)
 * 3. App Check (optional additional layer)
 *
 * Environment variables are used for flexibility, not secrecy.
 */

import { initializeApp, getApps, FirebaseApp } from 'firebase/app';
import { getAnalytics, isSupported, Analytics } from 'firebase/analytics';
import { getDatabase, Database } from 'firebase/database';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
};

// Initialize Firebase only if config is present
let app: FirebaseApp | undefined;
let analytics: Analytics | undefined;
let database: Database | undefined;

export function getFirebaseApp(): FirebaseApp | undefined {
  if (typeof window === 'undefined') return undefined;

  if (!firebaseConfig.apiKey || !firebaseConfig.projectId) {
    // Config not set - analytics disabled (development without .env.local)
    return undefined;
  }

  if (!app && getApps().length === 0) {
    app = initializeApp(firebaseConfig);
  } else if (!app) {
    app = getApps()[0];
  }

  return app;
}

export async function getFirebaseAnalytics(): Promise<Analytics | undefined> {
  if (typeof window === 'undefined') return undefined;

  const firebaseApp = getFirebaseApp();
  if (!firebaseApp) return undefined;

  if (!analytics) {
    const supported = await isSupported();
    if (supported) {
      analytics = getAnalytics(firebaseApp);
    }
  }

  return analytics;
}

export function getFirebaseDatabase(): Database | undefined {
  if (typeof window === 'undefined') return undefined;

  const firebaseApp = getFirebaseApp();
  if (!firebaseApp) return undefined;

  if (!database) {
    database = getDatabase(firebaseApp);
  }

  return database;
}
