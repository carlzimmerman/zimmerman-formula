/**
 * =============================================================================
 * FIREBASE CONFIGURATION - Z² Universe Multiplayer
 * =============================================================================
 *
 * Firebase Realtime Database for multiplayer vessel synchronization.
 * Players can see each other flying through the T³/Z₂ cosmos!
 *
 * SETUP REQUIRED:
 * 1. Go to Firebase Console: https://console.firebase.google.com
 * 2. Select project: abeautifullygeometricuniverse
 * 3. Enable Realtime Database (Build → Realtime Database → Create Database)
 * 4. Set rules to allow read/write (for development):
 *    {
 *      "rules": {
 *        ".read": true,
 *        ".write": true
 *      }
 *    }
 * 5. Copy your config from Project Settings → General → Your apps → Web app
 *
 * =============================================================================
 */

import { initializeApp, getApps, FirebaseApp } from 'firebase/app';
import { getDatabase, Database } from 'firebase/database';

// Firebase configuration - Public keys (security is in database rules)
const firebaseConfig = {
  apiKey: "AIzaSyAI4qRD2NUybVRUgUT5Ryv9kqNhaeJtXIc",
  authDomain: "abeautifullygeometricuniverse.firebaseapp.com",
  databaseURL: "https://abeautifullygeometricuniverse-default-rtdb.firebaseio.com",
  projectId: "abeautifullygeometricuniverse",
  storageBucket: "abeautifullygeometricuniverse.firebasestorage.app",
  messagingSenderId: "232552319342",
  appId: "1:232552319342:web:a0aca6437295d31bed597f",
  measurementId: "G-MD6553PLSY"
};

// Initialize Firebase (singleton pattern for Next.js)
let app: FirebaseApp;
let database: Database;

export function getFirebaseApp(): FirebaseApp {
  if (!app && typeof window !== 'undefined') {
    if (getApps().length === 0) {
      app = initializeApp(firebaseConfig);
    } else {
      app = getApps()[0];
    }
  }
  return app;
}

export function getFirebaseDatabase(): Database | null {
  if (typeof window === 'undefined') return null;

  if (!database) {
    const firebaseApp = getFirebaseApp();
    if (firebaseApp) {
      database = getDatabase(firebaseApp);
    }
  }
  return database;
}

// Export for convenience
export { firebaseConfig };
