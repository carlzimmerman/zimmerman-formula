'use client';

/**
 * ================================================================================
 * ABIOGENESIS - Project Protogonos Interactive Simulation
 * ================================================================================
 *
 * Interactive visualization exploring Z² geometric hypotheses for abiogenesis.
 *
 * VALIDATED MATCHES (from crystallography/PDB):
 * - FeS₂ pyrite lattice: 5.417 Å vs Z = 5.789 Å (6.8% error) ✓
 * - α-helix backbone angles: within 1σ of PDB statistics ✓
 * - α-helix pitch: 5.4 Å vs Z = 5.79 Å (7% error) ✓
 *
 * HYPOTHESES (require experimental validation):
 * - Z² geometry creates chirality bias
 * - Geometric selection of stable peptides
 * - Z-scale membrane spacing (original claim incorrect: actual headgroup 8-9 Å)
 *
 * Central Question: Could geometric constraints have guided prebiotic chemistry?
 * This is a hypothesis to be tested, not an established fact.
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
            Project Protogonos — Exploring Geometric Constraints on Life
          </h1>
          <p className="text-slate-400">
            Interactive exploration of how Z² = 32π/3 geometry might have constrained prebiotic chemistry.
            Some matches are <span className="text-green-400">validated</span> (FeS₂ lattice, α-helix angles);
            others remain <span className="text-orange-400">hypotheses</span> requiring experimental testing.
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
