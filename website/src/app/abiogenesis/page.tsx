'use client';

/**
 * ================================================================================
 * ABIOGENESIS - Project Protogonos: Computational Investigation Results
 * ================================================================================
 *
 * COMPUTATIONAL FRAMEWORKS TESTED (May 2026):
 *
 * 1. RAF THEORY (Kauffman/Steel):
 *    - Phase transition at p_c ≈ 0.035 → autocatalytic sets emerge
 *    - Z² does NOT appear in this framework
 *
 * 2. ASSEMBLY THEORY (Walker/Cronin):
 *    - Molecular complexity measured by Assembly Index
 *    - Z² does NOT appear in this framework
 *
 * 3. DIFFERENTIAL GEOMETRY OF CRNs:
 *    - Riemannian manifold structure on concentration space
 *    - Curvature constrains reaction pathways
 *    - Z² does NOT appear in this framework
 *
 * INTRIGUING OBSERVATION:
 * - Z/12 = 0.482 vs Protein Factor = 0.491 (1.8% difference)
 * - 12 = kissing number in 3D
 * - Simple cubic packing gives 0.483 ≈ Z/12
 * - Status: INCONCLUSIVE but worth further investigation
 *
 * NOVEL CONTRIBUTIONS:
 * - The Galena Test: Proposed experiment to distinguish geometry vs chemistry
 * - Computational analysis showing Z² absent from abiogenesis frameworks
 *
 * HONEST CONCLUSION: Z² does not emerge from computational abiogenesis models.
 * The Z/12 ≈ protein factor observation is intriguing but not definitive.
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
            Project Protogonos — Computational Investigation
          </h1>
          <p className="text-slate-400">
            Rigorous computational analysis using RAF Theory, Assembly Theory, and Differential Geometry of reaction networks.
            <span className="text-green-400"> Z² does NOT appear in these established frameworks.</span>{' '}
            <span className="text-yellow-400">One intriguing observation: Z/12 ≈ protein factor (0.482 vs 0.491, 1.8% off).</span>{' '}
            <span className="text-cyan-400">Simple cubic packing gives 0.483 ≈ Z/12.</span>
            <span className="text-slate-500 font-semibold"> Status: INCONCLUSIVE but honest.</span>
          </p>
        </header>

        <AbiogenesisSimulation />

        <footer className="mt-4 text-slate-500 text-sm font-mono">
          <div className="flex justify-between items-center">
            <span>Z² Framework — Honest Science</span>
            <span>Statistical verdict: Coincidences are expected by chance.</span>
          </div>
        </footer>
      </div>
    </main>
  );
}
