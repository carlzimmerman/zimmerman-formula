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
            Deriving the MOND acceleration scale from cosmological critical density
          </p>

          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-6">
            <span className="font-medium text-gray-700">Carl Zimmerman</span>
            <span>·</span>
            <span>March 2025</span>
            <span>·</span>
            <a
              href="https://zenodo.org/records/19199167"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              DOI: 10.5281/zenodo.19199167
            </a>
          </div>

          {/* Core Formula */}
          <div className="bg-blue-50 border border-blue-200 rounded p-6 my-6 text-center">
            <div className="font-mono text-xl text-gray-900 mb-2">
              Z = 2√(8π/3) = 5.788810
            </div>
            <div className="font-mono text-lg text-blue-700">
              a₀ = cH₀/Z ≈ 1.2×10⁻¹⁰ m/s²
            </div>
            <div className="text-sm text-gray-600 mt-3">
              Derived from a₀ = c√(Gρ<sub>c</sub>)/2 using ρ<sub>c</sub> = 3H₀²/(8πG)
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
          <p className="text-gray-700 leading-relaxed">
            This framework predicts that a₀ evolves with redshift: <strong>a₀(z) = a₀(0) × E(z)</strong>.
            At z=10, a₀ was 20× higher — explaining JWST "impossible" early galaxies and the El Gordo
            cluster timing problem without dark matter.
          </p>
        </article>

        {/* Quick Links */}
        <div className="grid md:grid-cols-2 gap-4 mb-6">
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
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Testable Predictions</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 font-medium text-gray-600">Prediction</th>
                  <th className="text-left py-2 font-medium text-gray-600">Value</th>
                  <th className="text-left py-2 font-medium text-gray-600">Test</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                <tr>
                  <td className="py-3 text-gray-700">H₀ from a₀</td>
                  <td className="py-3 font-mono text-gray-900">71.5 km/s/Mpc</td>
                  <td className="py-3 text-gray-500">Between Planck & SH0ES</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">BTFR offset at z=2</td>
                  <td className="py-3 font-mono text-gray-900">−0.47 dex</td>
                  <td className="py-3 text-gray-500">KMOS3D, ALMA</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">a₀ at z=10</td>
                  <td className="py-3 font-mono text-gray-900">20× local</td>
                  <td className="py-3 text-gray-500">JWST kinematics</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Simulations Grid */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Simulations</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
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
          </div>
        </div>

        {/* External Links */}
        <div className="flex flex-wrap justify-center gap-4 text-sm mb-8">
          <a
            href="https://zenodo.org/records/19199167"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            Full Paper (Zenodo) ↗
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
            Zimmerman Framework —
            <a
              href="https://zenodo.org/records/19199167"
              className="text-blue-600 hover:underline ml-1"
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
