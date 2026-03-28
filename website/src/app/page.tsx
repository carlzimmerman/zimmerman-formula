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
            <span>March 2026</span>
            <span>·</span>
            <a
              href="https://zenodo.org/records/19244651"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              DOI: 10.5281/zenodo.19244651
            </a>
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
            <div className="text-center p-3 bg-gray-50 rounded">
              <div className="font-mono text-lg text-blue-700">GAUGE = 12</div>
              <div className="text-gray-600">= 9Z²/(8π)</div>
              <div className="text-xs text-gray-400 mt-1">8+3+1 bosons</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded">
              <div className="font-mono text-lg text-blue-700">Bekenstein = 4</div>
              <div className="text-gray-600">= 3Z²/(8π)</div>
              <div className="text-xs text-gray-400 mt-1">DNA bases, BH entropy</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded">
              <div className="font-mono text-lg text-blue-700">sin²θ_W</div>
              <div className="text-gray-600">= 3/13 = 3/(GAUGE+1)</div>
              <div className="text-xs text-gray-400 mt-1">= 0.231</div>
            </div>
          </div>
          <div className="mt-4 text-sm text-gray-600 text-center">
            Plus: 3 generations, 20 amino acids, m_p/m_e = 1836, 10D strings, holographic principle...
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
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Key Predictions</h2>
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
                <tr>
                  <td className="py-3 text-gray-700">Proton/electron mass</td>
                  <td className="py-3 font-mono text-gray-900">54Z² + 6Z − 8</td>
                  <td className="py-3 text-gray-500">1836.3 (0.02% error)</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Weinberg angle</td>
                  <td className="py-3 font-mono text-gray-900">sin²θ = 3/(GAUGE+1)</td>
                  <td className="py-3 text-gray-500">0.231 (0.15% error)</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Hubble constant</td>
                  <td className="py-3 font-mono text-gray-900">H₀ = Z × a₀ / c</td>
                  <td className="py-3 text-gray-500">71.5 km/s/Mpc</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">BTFR at z=2</td>
                  <td className="py-3 font-mono text-gray-900">−log₁₀(E(z))</td>
                  <td className="py-3 text-gray-500">−0.47 dex offset</td>
                </tr>
              </tbody>
            </table>
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
          </div>
        </div>

        {/* External Links */}
        <div className="flex flex-wrap justify-center gap-4 text-sm mb-8">
          <a
            href="https://zenodo.org/records/19244651"
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
              href="https://zenodo.org/records/19244651"
              className="text-blue-600 hover:underline ml-1"
              target="_blank"
              rel="noopener noreferrer"
            >
              DOI: 10.5281/zenodo.19244651
            </a>
          </p>
        </footer>
      </div>
    </main>
  )
}
