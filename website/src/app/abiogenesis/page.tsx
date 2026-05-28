'use client';

/**
 * ================================================================================
 * ABIOGENESIS - Project Protogonos Interactive Simulation
 * ================================================================================
 *
 * Interactive visualization of the 5 phases of abiogenesis as modeled by the
 * Z² Kaluza-Klein framework:
 *
 * Phase 1: Prebiotic Synthesis - Amino acid formation from simple molecules
 * Phase 2: Chirality Breaking - L-amino acid selection via Z² geometry
 * Phase 3: Polymerization - Peptide bond formation with geometric selection
 * Phase 4: Autocatalytic Closure - Self-replicating chemical networks
 * Phase 5: Compartmentalization - Proto-cell membrane formation
 *
 * Central Thesis: Life is a geometric phase transition, not a historical accident.
 * The Z² = 32π/3 compactification metric makes abiogenesis inevitable.
 *
 * Author: Carl Zimmerman + Claude
 * Framework: Z² Unified Action v11.1.0
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
            Project Protogonos — The Geometric Origin of Life
          </h1>
          <p className="text-slate-400">
            Interactive simulation demonstrating that abiogenesis is a deterministic
            geometric phase transition driven by the Z² = 32π/3 Kaluza-Klein compactification.
          </p>
        </header>

        <AbiogenesisSimulation />

        <footer className="mt-4 text-slate-500 text-sm font-mono">
          <div className="flex justify-between items-center">
            <span>Z² Framework — Project Protogonos v1.0</span>
            <span>Computational research only. Not experimentally validated.</span>
          </div>
        </footer>
      </div>
    </main>
  );
}
