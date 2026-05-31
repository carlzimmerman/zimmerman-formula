'use client';

/**
 * ================================================================================
 * ABIOGENESIS - Project Protogonos: Z² FRAMEWORK (SPECULATIVE)
 * ================================================================================
 *
 * ⚠️ HONESTY NOTICE (May 2026):
 * After critical self-review, several claims have been RETRACTED or REVISED.
 * See EARTH_ABIOGENESIS_HONESTY_ASSESSMENT.md for full analysis.
 *
 * WHAT IS VALID (Real Science):
 * ✓ Z² = 32π/3 observed in protein backbone data (real PDB observation)
 * ✓ Frank Model - Chiral amplification (established chemistry)
 * ✓ SAW Null Hypothesis rejection (proteins ≠ random polymers)
 * ✓ General pathway stages (scientific consensus)
 *
 * WHAT IS PROBLEMATIC:
 * ⚠️ "25 Million × Enhancement" - Made-up number, no derivation
 * ⚠️ Mars magnetic fields - WRONG UNITS (0.015 Gauss, not 1500)
 * ⚠️ Ω_Z = 1.0 "inevitable" - CIRCULAR REASONING (tuned parameters)
 * ⚠️ Probability estimates - Speculation, not measurements
 *
 * REVISED ESTIMATES:
 * - Mars Ω_Z: 0.4-0.7 (was 0.95) - magnetic field argument invalid
 * - Venus life probability: 5-10% (was 20%)
 * - "We are Martians": 0.1-2% (was 5%)
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
        {/* Honesty Banner */}
        <div className="bg-yellow-900/50 border border-yellow-500 rounded-lg p-3 mb-4">
          <div className="flex items-center gap-2">
            <span className="text-yellow-400 text-xl">⚠️</span>
            <span className="text-yellow-400 font-bold">HONESTY NOTICE:</span>
            <span className="text-yellow-200 text-sm">
              After critical self-review, several claims have been revised. See honesty assessments for details.
            </span>
          </div>
        </div>

        <header className="mb-4">
          <h1 className="text-3xl font-bold text-white mb-2">
            Project Protogonos — Z² Framework <span className="text-yellow-400">(Speculative)</span>
          </h1>
          <p className="text-slate-400">
            <span className="text-emerald-400">✓ Frank Model: Chiral amplification (valid science).</span>{' '}
            <span className="text-yellow-400">⚠️ Z-Catalysis: Enhancement factor unverified.</span>{' '}
            <span className="text-emerald-400">✓ SAW Null: REJECTED — Z is biological signal.</span>{' '}
            <span className="text-emerald-400">✓ Pathological Lock: Valid mechanism.</span>{' '}
            <span className="text-red-400">❌ Mars B-field: WRONG UNITS (revised).</span>
          </p>
        </header>

        <AbiogenesisSimulation />

        <footer className="mt-4 text-slate-500 text-sm font-mono">
          <div className="flex justify-between items-center">
            <span>Z² = 32π/3 — Observed in protein backbone data (✓ real)</span>
            <span className="text-yellow-400">Status: SPECULATIVE — Some claims retracted after self-review</span>
          </div>
        </footer>
      </div>
    </main>
  );
}
