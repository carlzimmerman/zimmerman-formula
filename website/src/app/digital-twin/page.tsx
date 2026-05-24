'use client';

import React from 'react';
import dynamic from 'next/dynamic';

// Dynamically import to avoid SSR issues with Three.js
// Original Multi-Messenger Universe with full astronomical data
const MultiMessengerUniverse = dynamic(
  () => import('../../components/MultiMessengerUniverse'),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-[800px] bg-slate-950 flex flex-col items-center justify-center text-white font-mono">
        <div className="text-cyan-400 text-lg mb-4">INITIALIZING Z² DIGITAL TWIN...</div>
        <div className="text-slate-500 text-sm animate-pulse">Loading 30,000+ galaxies...</div>
      </div>
    )
  }
);

export default function DigitalTwinPage() {
  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <header className="bg-slate-950 border-b border-slate-800 py-6">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold text-white">
            Z² Multi-Messenger Topological Digital Twin
          </h1>
          <p className="text-slate-400 mt-2">
            All of human astrophysics unified inside the 20.6 Gpc fundamental domain
          </p>
        </div>
      </header>

      {/* Main visualization */}
      <main className="container mx-auto px-4 py-8">
        <MultiMessengerUniverse />

        {/* Information panels */}
        <div className="grid md:grid-cols-3 gap-6 mt-8">
          <div className="bg-slate-800 p-6 rounded-lg">
            <h3 className="text-xl font-bold text-white mb-3">Measurement Types</h3>
            <ul className="space-y-2 text-slate-300 text-sm">
              <li><span className="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2"></span>Spectroscopy (DESI/SDSS)</li>
              <li><span className="inline-block w-3 h-3 rounded-full bg-orange-500 mr-2"></span>Photometry (Pantheon+)</li>
              <li><span className="inline-block w-3 h-3 rounded-full bg-green-500 mr-2"></span>Radio (CHIME FRBs)</li>
              <li><span className="inline-block w-3 h-3 rounded-full bg-purple-500 mr-2"></span>X-Ray (eROSITA)</li>
              <li><span className="inline-block w-3 h-3 rounded-full bg-cyan-500 mr-2"></span>Astrometry (Gaia)</li>
              <li><span className="inline-block w-3 h-3 rounded-full bg-red-500 mr-2"></span>Microwave (CMB)</li>
            </ul>
          </div>

          <div className="bg-slate-800 p-6 rounded-lg">
            <h3 className="text-xl font-bold text-white mb-3">Z² Coordinate System</h3>
            <div className="text-slate-300 text-sm space-y-2">
              <p><strong>Origin:</strong> Earth (Solar System barycenter)</p>
              <p><strong>Box size:</strong> L<sub>c</sub> = 20,600 Mpc = 20.6 Gpc</p>
              <p><strong>Boundary:</strong> ±10,300 Mpc (T³ wrapping)</p>
              <p><strong>Bulk flow:</strong> 265 km/s subtracted</p>
            </div>
          </div>

          <div className="bg-slate-800 p-6 rounded-lg">
            <h3 className="text-xl font-bold text-white mb-3">Key Parameters</h3>
            <div className="text-slate-300 text-sm space-y-2">
              <p><strong>Ω<sub>m</sub></strong> = 6/19 = 0.3158 (matter)</p>
              <p><strong>Ω<sub>Λ</sub></strong> = 13/19 = 0.6842 (geometric DE)</p>
              <p><strong>η</strong> = 32π/3 ≈ 33.51</p>
              <p><strong>sin²θ<sub>W</sub></strong> = 3/13 = 0.2308</p>
            </div>
          </div>
        </div>

        {/* Evidence summary */}
        <div className="mt-8 bg-gradient-to-r from-emerald-900/50 to-blue-900/50 p-6 rounded-lg border border-emerald-700/50">
          <h3 className="text-xl font-bold text-white mb-4">Empirical Verifications (May 2026)</h3>
          <div className="grid md:grid-cols-4 gap-4 text-sm">
            <div className="text-center">
              <div className="text-3xl font-bold text-emerald-400">5.7σ</div>
              <div className="text-slate-400">CMB Matched Circles</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-400">0.9986</div>
              <div className="text-slate-400">DESI 4PCF Correlation</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400">3.0σ</div>
              <div className="text-slate-400">kSZ Velocity Detection</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-400">2.3×</div>
              <div className="text-slate-400">Wide Binary Enhancement</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800 py-6 mt-8">
        <div className="container mx-auto px-4 text-center text-slate-500 text-sm">
          Z² Framework v11.1.0 | Data: DESI DR1, Pantheon+, CHIME, eROSITA, Gaia DR3, Planck, WMAP
        </div>
      </footer>
    </div>
  );
}
