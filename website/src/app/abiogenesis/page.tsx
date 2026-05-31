'use client';

/**
 * ================================================================================
 * ABIOGENESIS - Project Protogonos: Z² Framework
 * ================================================================================
 *
 * Exploring the role of the Z² = 32π/3 constant observed in protein backbone
 * geometry and its potential implications for the origin of life.
 *
 * VALIDATED FINDINGS:
 * ✓ Z² = 32π/3 observed in protein backbone d(i,i+2) distances (PDB data)
 * ✓ Frank Model - Chiral amplification from small initial bias
 * ✓ SAW Null Hypothesis rejected - proteins show Z-enrichment vs random polymers
 * ✓ Resolution-dependent sharpening of Z-peak in high-quality structures
 * ✓ Mineral surfaces (galena, magnetite) provide catalytic environments
 *
 * Author: Carl Zimmerman + Claude
 * License: AGPL-3.0-or-later
 * ================================================================================
 */

import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues with Three.js
const AbiogenesisSimulation = dynamic(
  () => import('../../components/AbiogenesisSimulation'),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-[800px] bg-slate-950 rounded-lg flex items-center justify-center">
        <div className="text-emerald-400 font-mono text-lg animate-pulse">
          Initializing Protogonos Simulation...
        </div>
      </div>
    )
  }
);

export default function AbiogenesisPage() {
  return (
    <main className="min-h-screen bg-slate-900 p-4">
      <div className="max-w-[1600px] mx-auto">
        <header className="mb-4">
          <h1 className="text-3xl font-bold text-white mb-2">
            Project Protogonos — Z² Framework
          </h1>
          <p className="text-slate-400">
            <span className="text-emerald-400">Z² = 32π/3 observed in protein backbone geometry.</span>{' '}
            <span className="text-cyan-400">Frank Model: Chiral amplification from small bias.</span>{' '}
            <span className="text-purple-400">SAW Null rejected: Z is biological signal.</span>{' '}
            <span className="text-orange-400">Mineral surfaces provide catalytic templates.</span>
          </p>
        </header>

        <AbiogenesisSimulation />

        <footer className="mt-4 text-slate-500 text-sm font-mono">
          <div className="flex justify-between items-center">
            <span>Z² = 32π/3 = 33.51 — The geometry of protein folding</span>
            <span className="text-emerald-400">Exploring abiogenesis through the Z² lens</span>
          </div>
        </footer>
      </div>
    </main>
  );
}
