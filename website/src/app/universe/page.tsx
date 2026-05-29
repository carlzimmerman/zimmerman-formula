'use client';

/**
 * ================================================================================
 * THE Z² UNIVERSE - Full Digital Twin Experience
 * ================================================================================
 *
 * Unified T³/Z₂ cosmic visualization with:
 * - Multi-scale zoom from planets to 20.6 Gpc cosmic horizon
 * - Player Mode spacecraft navigation
 * - CMB Proof visualization (topology circles)
 * - Gravitational wave simulations
 * - Cinematic tours
 *
 * Author: Carl Zimmerman + Claude
 * Framework: Z² Unified Action v11.1.0
 * ================================================================================
 */

import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues with Three.js
const MultiMessengerUniverse = dynamic(
  () => import('../../components/MultiMessengerUniverse'),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-[800px] bg-slate-950 rounded-lg flex items-center justify-center">
        <div className="text-cyan-400 font-mono text-lg animate-pulse">
          Loading Z² Digital Twin...
        </div>
      </div>
    )
  }
);

export default function UniversePage() {
  return (
    <main className="min-h-screen bg-slate-900 p-4">
      <div className="max-w-[1600px] mx-auto">
        <header className="mb-4">
          <h1 className="text-3xl font-bold text-white mb-2">
            Z² Digital Twin
          </h1>
          <p className="text-slate-400">
            Explore the T³/Z₂ universe from Earth to the 20.6 Gpc cosmic horizon.
            Start your spacecraft or view CMB topology evidence.
          </p>
        </header>

        <MultiMessengerUniverse />

        <footer className="mt-4 text-slate-600 text-xs font-mono">
          <div className="flex justify-between items-center">
            <span>Z² Framework v11.1.0</span>
            <span className="text-slate-500">Scroll: zoom | Drag: rotate | ESC: exit modes</span>
          </div>
        </footer>
      </div>
    </main>
  );
}
