'use client'

import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-[#fafafa]">
      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-6 md:py-8">
        {/* Title Block */}
        <article className="bg-white border border-gray-200 rounded shadow-sm p-5 md:p-8 mb-6">
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2 leading-tight">
            The Zimmerman Framework
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            A unified geometric theory: Z² = CUBE × SPHERE generates all of physics
          </p>

          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-6">
            <span className="font-medium text-gray-700">Carl Zimmerman</span>
            <span>·</span>
            <span>April 2026 (v5.4.0)</span>
            <span>·</span>
            <a
              href="https://zenodo.org/records/19474535"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              DOI: 10.5281/zenodo.19474535
            </a>
          </div>

          {/* April 16 Breakthrough Banner */}
          <div className="bg-green-50 border border-green-200 rounded p-4 mb-6">
            <div className="font-semibold text-green-800 mb-2">🎯 April 16, 2026: 16+ First-Principles Derivations</div>
            <div className="text-sm text-green-700 space-y-1">
              <div>• <strong>Hierarchy:</strong> M_Pl/v = 2Z^(43/2) — 0.3% error</div>
              <div>• <strong>Cosmology:</strong> Ω_m = 6/19, Ω_Λ = 13/19 — Weinberg angle connection!</div>
              <div>• <strong>Proton mass:</strong> m_p/m_e = α⁻¹ × 2Z²/5 — 0.042% error</div>
              <div>• <strong>Cabibbo:</strong> λ = 1/(Z - √2) — 1.3% error</div>
            </div>
          </div>

          {/* Core Formula */}
          <div className="bg-blue-50 border border-blue-200 rounded p-6 my-6 text-center">
            <div className="font-mono text-xl text-gray-900 mb-2">
              Z² = 8 × (4π/3) = CUBE × SPHERE
            </div>
            <div className="font-mono text-lg text-blue-700 mb-2">
              Z = 2√(8π/3) = 5.788810...
            </div>
            <div className="text-sm text-gray-600 mt-3">
              From this single equation: all coupling constants, mass ratios, spacetime dimensions, and the genetic code
            </div>
          </div>

          {/* Big Visualizations Button */}
          <Link
            href="/simulate"
            className="block w-full py-4 px-6 bg-blue-600 hover:bg-blue-700 text-white text-center text-lg font-medium rounded transition-colors mb-6"
          >
            Explore Interactive Visualizations →
          </Link>

          {/* Key insight */}
          <p className="text-gray-700 leading-relaxed mb-4">
            This framework derives <strong>a₀ = cH₀/Z</strong> from first principles, predicting it evolves with redshift: <strong>a₀(z) = a₀(0) × E(z)</strong>.
            At z=10, a₀ was 20× higher — explaining JWST "impossible" early galaxies without dark matter.
          </p>
        </article>

        {/* Z² Geometric Closure */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Z² Derives Everything</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="text-center p-3 bg-gray-50 rounded">
              <div className="font-mono text-lg text-blue-700">α⁻¹ = 4Z²+3</div>
              <div className="text-gray-600">= 137.036</div>
              <div className="text-xs text-gray-400 mt-1">Fine structure</div>
            </div>
            <div className="text-center p-3 bg-green-50 rounded border border-green-200">
              <div className="font-mono text-lg text-green-700">Ω_m/Ω_Λ</div>
              <div className="text-gray-600">= 6/13 = 2sin²θ_W</div>
              <div className="text-xs text-green-600 mt-1">NEW: Weinberg↔Cosmo!</div>
            </div>
            <div className="text-center p-3 bg-green-50 rounded border border-green-200">
              <div className="font-mono text-lg text-green-700">m_p/m_e</div>
              <div className="text-gray-600">= α⁻¹ × 2Z²/5</div>
              <div className="text-xs text-green-600 mt-1">NEW: 0.042% error!</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded">
              <div className="font-mono text-lg text-blue-700">sin²θ_W</div>
              <div className="text-gray-600">= 3/13</div>
              <div className="text-xs text-gray-400 mt-1">= 0.231</div>
            </div>
          </div>
          <div className="mt-4 text-sm text-gray-600 text-center">
            Plus: 3 generations, M_Pl/v = 2Z^(43/2), λ_Cabibbo = 1/(Z−√2), δ_CKM = arccos(1/3)...
          </div>
        </div>

        {/* Quick Links */}
        <div className="grid md:grid-cols-2 gap-4 mb-6">
          <Link
            href="/why-z2"
            className="block p-5 bg-blue-50 border border-blue-200 rounded shadow-sm hover:border-blue-400 hover:shadow transition-all"
          >
            <div className="font-semibold text-blue-800 mb-1">Why Z² = 32π/3?</div>
            <div className="text-sm text-blue-600">
              First principles derivation from BEKENSTEIN = 4
            </div>
          </Link>

          <Link
            href="/derivation"
            className="block p-5 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 hover:shadow transition-all"
          >
            <div className="font-semibold text-gray-900 mb-1">Mathematical Derivation</div>
            <div className="text-sm text-gray-500">
              Step-by-step from critical density to a₀(z)
            </div>
          </Link>

          <Link
            href="/evidence"
            className="block p-5 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 hover:shadow transition-all"
          >
            <div className="font-semibold text-gray-900 mb-1">Observational Evidence</div>
            <div className="text-sm text-gray-500">
              JWST, DESI, Gaia wide binaries, El Gordo
            </div>
          </Link>

          <Link
            href="/rar"
            className="block p-5 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 hover:shadow transition-all"
          >
            <div className="font-semibold text-gray-900 mb-1">RAR + SPARC Data</div>
            <div className="text-sm text-gray-500">
              153 galaxies, 2,693 data points
            </div>
          </Link>

          <Link
            href="/calculator"
            className="block p-5 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 hover:shadow transition-all"
          >
            <div className="font-semibold text-gray-900 mb-1">Calculator</div>
            <div className="text-sm text-gray-500">
              Compute a₀(z), BTFR, galaxy dynamics
            </div>
          </Link>
        </div>

        {/* Testable Predictions */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Key Predictions (16+ First-Principles)</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 font-medium text-gray-600">Prediction</th>
                  <th className="text-left py-2 font-medium text-gray-600">Z² Formula</th>
                  <th className="text-left py-2 font-medium text-gray-600">Result</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                <tr>
                  <td className="py-3 text-gray-700">Fine structure constant</td>
                  <td className="py-3 font-mono text-gray-900">α⁻¹ = 4Z² + 3</td>
                  <td className="py-3 text-gray-500">137.036 (0.004% error)</td>
                </tr>
                <tr className="bg-green-50">
                  <td className="py-3 text-gray-700 font-medium">Proton/electron mass</td>
                  <td className="py-3 font-mono text-gray-900">α⁻¹ × 2Z²/5</td>
                  <td className="py-3 text-green-700 font-medium">1836.92 (0.042% error) ⭐</td>
                </tr>
                <tr className="bg-green-50">
                  <td className="py-3 text-gray-700 font-medium">Hierarchy M_Pl/v</td>
                  <td className="py-3 font-mono text-gray-900">2Z^(43/2)</td>
                  <td className="py-3 text-green-700 font-medium">4.97×10¹⁶ (0.3% error) ⭐</td>
                </tr>
                <tr className="bg-green-50">
                  <td className="py-3 text-gray-700 font-medium">Matter density Ω_m</td>
                  <td className="py-3 font-mono text-gray-900">6/19</td>
                  <td className="py-3 text-green-700 font-medium">0.3158 (0.25% error) ⭐</td>
                </tr>
                <tr className="bg-green-50">
                  <td className="py-3 text-gray-700 font-medium">Dark energy Ω_Λ</td>
                  <td className="py-3 font-mono text-gray-900">13/19</td>
                  <td className="py-3 text-green-700 font-medium">0.6842 (0.12% error) ⭐</td>
                </tr>
                <tr className="bg-green-50">
                  <td className="py-3 text-gray-700 font-medium">Cabibbo angle λ</td>
                  <td className="py-3 font-mono text-gray-900">1/(Z − √2)</td>
                  <td className="py-3 text-green-700 font-medium">0.2286 (1.3% error) ⭐</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Weinberg angle</td>
                  <td className="py-3 font-mono text-gray-900">sin²θ = 3/13</td>
                  <td className="py-3 text-gray-500">0.231 (0.19% error)</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">CKM CP phase δ</td>
                  <td className="py-3 font-mono text-gray-900">arccos(1/3)</td>
                  <td className="py-3 text-gray-500">70.5° (3.7% error)</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="mt-3 text-xs text-gray-500 text-center">
            ⭐ = April 2026 breakthrough | Key: Ω_m/Ω_Λ = 6/13 = 2×sin²θ_W (Weinberg angle in cosmology!)
          </div>
        </div>

        {/* Simulations Grid */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Explore</h2>
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
            <Link href="/simulate" className="p-4 bg-gray-50 rounded border border-gray-200 hover:border-blue-300 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">🌀</div>
              <div className="text-sm font-medium text-gray-700">Galaxy Rotation</div>
            </Link>
            <Link href="/rar" className="p-4 bg-gray-50 rounded border border-gray-200 hover:border-blue-300 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">📈</div>
              <div className="text-sm font-medium text-gray-700">RAR</div>
            </Link>
            <Link href="/el-gordo" className="p-4 bg-gray-50 rounded border border-gray-200 hover:border-blue-300 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">💥</div>
              <div className="text-sm font-medium text-gray-700">El Gordo</div>
            </Link>
            <Link href="/early-universe" className="p-4 bg-gray-50 rounded border border-gray-200 hover:border-blue-300 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">🌌</div>
              <div className="text-sm font-medium text-gray-700">Early Universe</div>
            </Link>
            <Link href="/lattice" className="p-4 bg-blue-50 rounded border border-blue-200 hover:border-blue-400 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">🔲</div>
              <div className="text-sm font-medium text-blue-700">Cube Lattice</div>
            </Link>
            <Link href="/why-z2" className="p-4 bg-amber-50 rounded border border-amber-200 hover:border-amber-400 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">?</div>
              <div className="text-sm font-medium text-amber-700">Why Z²?</div>
            </Link>
            <Link href="/cosmic-fate" className="p-4 bg-gray-900 rounded border border-gray-700 hover:border-gray-500 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">∞</div>
              <div className="text-sm font-medium text-gray-100">Cosmic Fate</div>
            </Link>
            <Link href="/all-derivations" className="p-4 bg-green-50 rounded border border-green-200 hover:border-green-400 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">*</div>
              <div className="text-sm font-medium text-green-700">All Derivations</div>
            </Link>
            <Link href="/predictions" className="p-4 bg-red-50 rounded border border-red-200 hover:border-red-400 text-center transition-colors min-h-[72px] flex flex-col justify-center">
              <div className="text-2xl mb-1">!</div>
              <div className="text-sm font-medium text-red-700">2026 Predictions</div>
            </Link>
          </div>
        </div>

        {/* Download Section */}
        <div className="bg-gray-900 text-white rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold mb-2 text-center">Download</h2>
          <p className="text-gray-400 text-sm text-center mb-4">
            Complete derivation paper and full archive
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <a
              href="/Z2_COMPLETE_DERIVATION.pdf"
              download
              className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded font-medium transition-colors"
            >
              <span>Complete Lagrangian Paper</span>
              <span className="text-green-200 text-sm">(PDF)</span>
            </a>
            <a
              href="/zimmerman-formula-complete-2026-04-14.zip"
              download
              className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition-colors"
            >
              <span>Full Archive</span>
              <span className="text-blue-200 text-sm">(99 MB ZIP)</span>
            </a>
          </div>
          <p className="text-gray-500 text-xs text-center mt-4">
            v5.4.0: 16+ first-principles derivations including hierarchy, cosmology, proton mass, and CKM
          </p>
        </div>

        {/* External Links */}
        <div className="flex flex-wrap justify-center gap-4 text-sm mb-8">
          <a
            href="https://zenodo.org/records/19474535"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            Full Paper (Zenodo) ↗
          </a>
          <a
            href="https://github.com/carlzimmerman/zimmerman-formula"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            GitHub Repository ↗
          </a>
          <a
            href="https://astroweb.case.edu/SPARC/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            SPARC Database ↗
          </a>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p>
            Zimmerman Framework: Z² = CUBE × SPHERE —
            <a
              href="https://zenodo.org/records/19474535"
              className="text-blue-600 hover:underline ml-1"
              target="_blank"
              rel="noopener noreferrer"
            >
              DOI: 10.5281/zenodo.19474535
            </a>
          </p>
        </footer>
      </div>
    </main>
  )
}
