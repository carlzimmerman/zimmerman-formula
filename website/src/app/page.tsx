'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-200 bg-gray-50">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <nav className="flex items-center justify-between">
            <div className="text-lg font-semibold text-gray-900">Zimmerman Framework</div>
            <div className="flex items-center gap-6 text-sm">
              <Link href="/derivation" className="text-gray-600 hover:text-gray-900">Derivation</Link>
              <Link href="/evidence" className="text-gray-600 hover:text-gray-900">Evidence</Link>
              <Link href="/simulate" className="text-gray-600 hover:text-gray-900">Simulations</Link>
              <Link href="/office-hours" className="text-gray-600 hover:text-gray-900">Office Hours</Link>
              <a
                href="https://github.com/carlzimmerman/zimmerman-formula"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-gray-900"
              >
                GitHub
              </a>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-6 py-12">
        {/* Title Block */}
        <article className="mb-12">
          <h1 className="text-3xl md:text-4xl font-serif font-normal text-gray-900 mb-3">
            The Zimmerman Framework
          </h1>
          <p className="text-xl text-gray-600 mb-6 font-light">
            A unified geometric theory deriving fundamental constants from a single equation
          </p>

          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-8 pb-8 border-b border-gray-200">
            <span className="font-medium text-gray-700">Carl Zimmerman</span>
            <span className="text-gray-300">|</span>
            <span>Version 11.1.0</span>
            <span className="text-gray-300">|</span>
            <span>May 2026</span>
            <span className="text-gray-300">|</span>
            <a
              href="https://zenodo.org/records/19199167"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              DOI: 10.5281/zenodo.19199167
            </a>
          </div>

          {/* Abstract */}
          <section className="mb-10">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Abstract</h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              This framework proposes that all fundamental physical constants emerge from a single geometric relationship:
              the coupling between cubic and spherical symmetries in compactified extra dimensions. The characteristic
              constant Z = 5.7888... derives from the Atiyah-Patodi-Singer eta invariant on a T³/Z₂ orbifold.
            </p>
            <p className="text-gray-700 leading-relaxed">
              From this single constant, we derive 19 independent predictions including the fine structure constant,
              proton-to-electron mass ratio, Weinberg angle, cosmological density parameters, and CKM matrix elements,
              with an average error of 0.57% against experimental values.
            </p>
          </section>

          {/* Core Equation */}
          <section className="bg-gray-50 border border-gray-200 rounded-lg p-8 mb-10">
            <div className="text-center">
              <div className="font-mono text-2xl text-gray-900 mb-2">
                Z² = 8 × (4π/3) = 32π/3
              </div>
              <div className="font-mono text-xl text-blue-700 mb-4">
                Z = √(32π/3) = 5.788810...
              </div>
              <p className="text-sm text-gray-600 max-w-xl mx-auto">
                The product of cubic symmetry (8 fixed points of T³/Z₂) and spherical measure (4π/3)
                yields all coupling constants, mass hierarchies, and cosmological parameters.
              </p>
            </div>
          </section>

          {/* Recent Results */}
          <section className="mb-10">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Recent Results</h2>

            <div className="space-y-4">
              <div className="border-l-4 border-red-500 pl-4 py-2 bg-red-50/50">
                <div className="font-medium text-gray-900 mb-1">May 23, 2026: DESI 4PCF Topology Confirmation</div>
                <p className="text-sm text-gray-600">
                  NGC-SGC correlation r = 0.9986 from 2.1M galaxies confirms globally coherent parity violation
                  consistent with T³/Z₂ topology. Universe size: 20.6 Gpc orbifold.
                </p>
                <Link href="/evidence/4pcf" className="text-sm text-red-600 hover:underline mt-2 inline-block">
                  View analysis
                </Link>
              </div>

              <div className="border-l-4 border-green-500 pl-4 py-2 bg-green-50/50">
                <div className="font-medium text-gray-900 mb-1">April 2026: 19 First-Principles Derivations</div>
                <p className="text-sm text-gray-600">
                  New derivations include: Ω_m/Ω_Λ = 6/13 (linking dark sector to electroweak),
                  m_p/m_e = α⁻¹ × 2Z²/5 (0.042% error), M_Pl/v = 2Z^(43/2) (0.3% error).
                </p>
                <Link href="/all-derivations" className="text-sm text-green-600 hover:underline mt-2 inline-block">
                  View all derivations
                </Link>
              </div>
            </div>
          </section>
        </article>

        {/* Key Predictions Table */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Key Predictions</h2>
          <div className="overflow-x-auto border border-gray-200 rounded-lg">
            <table className="w-full text-sm">
              <thead className="bg-gray-50">
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Parameter</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Formula</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Predicted</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-600">Observed</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-600">Error</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                <tr>
                  <td className="py-3 px-4 text-gray-700">Fine structure constant</td>
                  <td className="py-3 px-4 font-mono text-gray-900">α⁻¹ = 4Z² + 3</td>
                  <td className="py-3 px-4 text-gray-600">137.041</td>
                  <td className="py-3 px-4 text-gray-600">137.036</td>
                  <td className="py-3 px-4 text-right text-gray-500">0.004%</td>
                </tr>
                <tr className="bg-gray-50/50">
                  <td className="py-3 px-4 text-gray-700">Proton/electron mass</td>
                  <td className="py-3 px-4 font-mono text-gray-900">α⁻¹ × 2Z²/5</td>
                  <td className="py-3 px-4 text-gray-600">1836.92</td>
                  <td className="py-3 px-4 text-gray-600">1836.15</td>
                  <td className="py-3 px-4 text-right text-gray-500">0.042%</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 text-gray-700">Weinberg angle</td>
                  <td className="py-3 px-4 font-mono text-gray-900">sin²θ_W = 3/13</td>
                  <td className="py-3 px-4 text-gray-600">0.2308</td>
                  <td className="py-3 px-4 text-gray-600">0.2312</td>
                  <td className="py-3 px-4 text-right text-gray-500">0.19%</td>
                </tr>
                <tr className="bg-gray-50/50">
                  <td className="py-3 px-4 text-gray-700">Matter density Ω_m</td>
                  <td className="py-3 px-4 font-mono text-gray-900">6/19</td>
                  <td className="py-3 px-4 text-gray-600">0.3158</td>
                  <td className="py-3 px-4 text-gray-600">0.315</td>
                  <td className="py-3 px-4 text-right text-gray-500">0.25%</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 text-gray-700">Dark energy Ω_Λ</td>
                  <td className="py-3 px-4 font-mono text-gray-900">13/19</td>
                  <td className="py-3 px-4 text-gray-600">0.6842</td>
                  <td className="py-3 px-4 text-gray-600">0.685</td>
                  <td className="py-3 px-4 text-right text-gray-500">0.12%</td>
                </tr>
                <tr className="bg-gray-50/50">
                  <td className="py-3 px-4 text-gray-700">Hierarchy M_Pl/v</td>
                  <td className="py-3 px-4 font-mono text-gray-900">2Z^(43/2)</td>
                  <td className="py-3 px-4 text-gray-600">4.97×10¹⁶</td>
                  <td className="py-3 px-4 text-gray-600">4.96×10¹⁶</td>
                  <td className="py-3 px-4 text-right text-gray-500">0.3%</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 text-gray-700">Cabibbo angle</td>
                  <td className="py-3 px-4 font-mono text-gray-900">λ = 1/(Z − √2)</td>
                  <td className="py-3 px-4 text-gray-600">0.2286</td>
                  <td className="py-3 px-4 text-gray-600">0.2257</td>
                  <td className="py-3 px-4 text-right text-gray-500">1.3%</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-right">
            Average error across 19 derivations: 0.57%
          </p>
        </section>

        {/* Navigation Sections */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Documentation</h2>

          <div className="grid md:grid-cols-3 gap-6">
            {/* Theory */}
            <div className="border border-gray-200 rounded-lg p-5">
              <h3 className="font-medium text-gray-900 mb-3">Theory</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/why-z2" className="text-blue-600 hover:underline">
                    Why Z² = 32π/3?
                  </Link>
                  <span className="text-gray-400 ml-2">First principles</span>
                </li>
                <li>
                  <Link href="/derivation" className="text-blue-600 hover:underline">
                    Mathematical Derivation
                  </Link>
                </li>
                <li>
                  <Link href="/all-derivations" className="text-blue-600 hover:underline">
                    All 19 Derivations
                  </Link>
                </li>
                <li>
                  <Link href="/topology" className="text-blue-600 hover:underline">
                    T³/Z₂ Topology
                  </Link>
                </li>
                <li>
                  <Link href="/dark-matter" className="text-blue-600 hover:underline">
                    Dark Matter as Winding Modes
                  </Link>
                </li>
              </ul>
            </div>

            {/* Evidence */}
            <div className="border border-gray-200 rounded-lg p-5">
              <h3 className="font-medium text-gray-900 mb-3">Evidence</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/evidence/4pcf" className="text-blue-600 hover:underline">
                    DESI 4PCF Analysis
                  </Link>
                  <span className="text-red-500 ml-2 text-xs">New</span>
                </li>
                <li>
                  <Link href="/evidence" className="text-blue-600 hover:underline">
                    All Observational Evidence
                  </Link>
                </li>
                <li>
                  <Link href="/rar" className="text-blue-600 hover:underline">
                    RAR + SPARC (153 galaxies)
                  </Link>
                </li>
                <li>
                  <Link href="/el-gordo" className="text-blue-600 hover:underline">
                    El Gordo Cluster
                  </Link>
                </li>
                <li>
                  <Link href="/predictions" className="text-blue-600 hover:underline">
                    Testable Predictions
                  </Link>
                </li>
              </ul>
            </div>

            {/* Tools */}
            <div className="border border-gray-200 rounded-lg p-5">
              <h3 className="font-medium text-gray-900 mb-3">Tools</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="/simulate" className="text-blue-600 hover:underline">
                    Interactive Simulations
                  </Link>
                </li>
                <li>
                  <Link href="/calculator" className="text-blue-600 hover:underline">
                    Calculator
                  </Link>
                </li>
                <li>
                  <Link href="/compare" className="text-blue-600 hover:underline">
                    Model Comparison
                  </Link>
                </li>
                <li>
                  <Link href="/visualizations" className="text-blue-600 hover:underline">
                    Visualizations
                  </Link>
                </li>
                <li>
                  <Link href="/office-hours" className="text-blue-600 hover:underline">
                    Office Hours (tutorials)
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Extended Research */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Extended Research</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <Link href="/abiogenesis" className="block border border-gray-200 rounded-lg p-5 hover:border-gray-300 transition-colors">
              <h3 className="font-medium text-gray-900 mb-1">Project Protogonos: Abiogenesis</h3>
              <p className="text-sm text-gray-600">
                Computational investigation of Z-resonance constraints on the origin of life.
                Simulation achieves 100% life emergence under Omega-Z conditions.
              </p>
            </Link>
            <Link href="/ghost-quasars" className="block border border-gray-200 rounded-lg p-5 hover:border-gray-300 transition-colors">
              <h3 className="font-medium text-gray-900 mb-1">Topological Ghost Images</h3>
              <p className="text-sm text-gray-600">
                Predicted ghost quasars from T³/Z₂ topology. Multiple images of same source
                displaced by orbifold translation.
              </p>
            </Link>
            <Link href="/cosmic-fate" className="block border border-gray-200 rounded-lg p-5 hover:border-gray-300 transition-colors">
              <h3 className="font-medium text-gray-900 mb-1">Cosmic Fate</h3>
              <p className="text-sm text-gray-600">
                Long-term evolution of the universe under the Z² framework.
                Implications for dark energy and ultimate fate.
              </p>
            </Link>
            <Link href="/early-universe" className="block border border-gray-200 rounded-lg p-5 hover:border-gray-300 transition-colors">
              <h3 className="font-medium text-gray-900 mb-1">Early Universe</h3>
              <p className="text-sm text-gray-600">
                JWST "impossible" early galaxies explained by redshift-dependent a₀(z).
                At z=10, acceleration scale was 20× higher.
              </p>
            </Link>
          </div>
        </section>

        {/* Downloads */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Downloads</h2>
          <div className="border border-gray-200 rounded-lg p-6 bg-gray-50">
            <div className="flex flex-col sm:flex-row gap-4">
              <a
                href="/Z2_COMPLETE_DERIVATION.pdf"
                download
                className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-gray-900 hover:bg-gray-800 text-white rounded transition-colors"
              >
                Complete Lagrangian Paper (PDF)
              </a>
              <a
                href="/zimmerman-formula-complete-2026-04-14.zip"
                download
                className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-white border border-gray-300 hover:border-gray-400 text-gray-700 rounded transition-colors"
              >
                Full Archive (99 MB ZIP)
              </a>
            </div>
            <p className="text-xs text-gray-500 text-center mt-4">
              Version 11.1.0 — 19 first-principles derivations, DESI 4PCF confirmation
            </p>
          </div>
        </section>

        {/* External Links */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">External Resources</h2>
          <div className="flex flex-wrap gap-6 text-sm">
            <a
              href="https://zenodo.org/records/19199167"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Zenodo Archive
            </a>
            <a
              href="https://github.com/carlzimmerman/zimmerman-formula"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              GitHub Repository
            </a>
            <a
              href="https://astroweb.case.edu/SPARC/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              SPARC Database
            </a>
          </div>
        </section>

        {/* Footer */}
        <footer className="pt-8 border-t border-gray-200 text-center text-sm text-gray-500">
          <p className="mb-2">
            The Zimmerman Framework — Z² = 32π/3
          </p>
          <p>
            <a
              href="https://zenodo.org/records/19199167"
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              DOI: 10.5281/zenodo.19199167
            </a>
          </p>
        </footer>
      </div>
    </main>
  )
}
