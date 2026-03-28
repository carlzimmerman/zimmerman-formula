'use client'

import Link from 'next/link'

const PI = Math.PI
const Z = 2 * Math.sqrt(8 * PI / 3)
const OMEGA_LAMBDA = (3 * Z) / (8 + 3 * Z)
const OMEGA_MATTER = 8 / (8 + 3 * Z)
const LAMBDA_MATTER_RATIO = OMEGA_LAMBDA / OMEGA_MATTER

// Key epochs
const z_equality = Math.pow(LAMBDA_MATTER_RATIO, 1/3) - 1
const z_transition = Math.pow(2 * LAMBDA_MATTER_RATIO, 1/3) - 1
const H_infinity_ratio = Math.sqrt(OMEGA_LAMBDA)
const a0_infinity_ratio = H_infinity_ratio

// De Sitter timescale
const tau_H0 = 14.0 // Gyr
const tau_infinity = tau_H0 / H_infinity_ratio

export default function CosmicFatePage() {
  return (
    <main className="min-h-screen bg-[#fafafa]">
      <div className="max-w-4xl mx-auto px-4 py-6 md:py-8">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 -mx-4 -mt-6 md:-mt-8 px-4 py-4 mb-6">
          <Link href="/" className="text-sm text-blue-600 hover:underline">
            ← Back to Overview
          </Link>
        </header>

        {/* Title Block */}
        <article className="bg-white border border-gray-200 rounded shadow-sm p-5 md:p-8 mb-6">
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2 leading-tight">
            When Does the Universe Stop Expanding?
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            Deriving cosmic fate from Z² = CUBE × SPHERE
          </p>

          {/* The Answer */}
          <div className="bg-blue-900 text-white rounded p-6 my-6 text-center">
            <div className="text-3xl font-bold mb-2">
              Never
            </div>
            <div className="text-blue-200">
              The Zimmerman framework proves eternal expansion from first principles
            </div>
          </div>
        </article>

        {/* The Proof */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Proof</h2>

          <div className="space-y-4">
            <div className="bg-gray-50 border border-gray-200 rounded p-4">
              <div className="text-sm text-gray-600 mb-2">From Z², the cosmological densities:</div>
              <div className="font-mono text-center">
                <div>Ω_Λ = 3Z/(8+3Z) = {OMEGA_LAMBDA.toFixed(4)}</div>
                <div>Ω_m = 8/(8+3Z) = {OMEGA_MATTER.toFixed(4)}</div>
              </div>
            </div>

            <div className="bg-gray-50 border border-gray-200 rounded p-4">
              <div className="text-sm text-gray-600 mb-2">The Friedmann equation:</div>
              <div className="font-mono text-center">
                H² = H₀² × [Ω_m × a⁻³ + Ω_Λ]
              </div>
            </div>

            <div className="bg-red-50 border border-red-200 rounded p-4">
              <div className="text-sm text-gray-600 mb-2">For expansion to stop (H = 0):</div>
              <div className="font-mono text-center mb-2">
                Ω_m × a⁻³ + Ω_Λ = 0
              </div>
              <div className="text-sm text-center text-red-700">
                But both terms are <strong>positive</strong> → Impossible!
              </div>
            </div>

            <div className="bg-green-50 border border-green-200 rounded p-4 text-center">
              <div className="text-green-700 font-semibold">
                H &gt; 0 always. The universe expands forever.
              </div>
            </div>
          </div>
        </div>

        {/* The Cosmic Timeline */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Cosmic Timeline</h2>
          <p className="text-sm text-gray-600 mb-4">All epochs derived from Z²</p>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 font-medium text-gray-600">Epoch</th>
                  <th className="text-center py-2 font-medium text-gray-600">Redshift</th>
                  <th className="text-center py-2 font-medium text-gray-600">When</th>
                  <th className="text-left py-2 font-medium text-gray-600">What Happens</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                <tr>
                  <td className="py-3 text-gray-700">Big Bang</td>
                  <td className="py-3 text-center font-mono text-gray-500">z = ∞</td>
                  <td className="py-3 text-center text-gray-500">t = 0</td>
                  <td className="py-3 text-gray-500">Beginning</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Matter-Λ Equality</td>
                  <td className="py-3 text-center font-mono text-blue-600">z = {z_equality.toFixed(2)}</td>
                  <td className="py-3 text-center text-gray-500">~3.5 Gyr ago</td>
                  <td className="py-3 text-gray-500">Dark energy takes over</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Decel → Accel</td>
                  <td className="py-3 text-center font-mono text-blue-600">z = {z_transition.toFixed(2)}</td>
                  <td className="py-3 text-center text-gray-500">~6 Gyr ago</td>
                  <td className="py-3 text-gray-500">Expansion accelerates</td>
                </tr>
                <tr className="bg-amber-50">
                  <td className="py-3 text-amber-800 font-semibold">TODAY</td>
                  <td className="py-3 text-center font-mono text-amber-600">z = 0</td>
                  <td className="py-3 text-center text-amber-600">13.8 Gyr</td>
                  <td className="py-3 text-amber-600">We are here</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Practical de Sitter</td>
                  <td className="py-3 text-center font-mono text-gray-500">z &lt; 0</td>
                  <td className="py-3 text-center text-gray-500">~4 Gyr from now</td>
                  <td className="py-3 text-gray-500">Effectively equilibrium</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Far Future</td>
                  <td className="py-3 text-center font-mono text-gray-500">z → -1</td>
                  <td className="py-3 text-center text-gray-500">t → ∞</td>
                  <td className="py-3 text-gray-500">Pure de Sitter</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* The Asymptotic State */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Asymptotic State</h2>

          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center">
              <div className="text-sm text-gray-600 mb-1">Hubble Parameter</div>
              <div className="font-mono text-lg text-blue-700">
                H → {H_infinity_ratio.toFixed(2)} × H₀
              </div>
              <div className="text-xs text-gray-500 mt-1">Floors at 83% of current</div>
            </div>
            <div className="bg-amber-50 border border-amber-200 rounded p-4 text-center">
              <div className="text-sm text-gray-600 mb-1">MOND Scale</div>
              <div className="font-mono text-lg text-amber-700">
                a₀ → {a0_infinity_ratio.toFixed(2)} × a₀(0)
              </div>
              <div className="text-xs text-gray-500 mt-1">Also has a floor</div>
            </div>
          </div>

          <div className="bg-gray-900 text-white rounded p-6 text-center">
            <div className="text-gray-400 text-sm mb-2">De Sitter e-folding time</div>
            <div className="text-3xl font-mono font-bold text-white mb-2">
              τ = {tau_infinity.toFixed(0)} Gyr
            </div>
            <div className="text-gray-400 text-sm">
              The scale factor doubles every {tau_infinity.toFixed(0)} billion years, forever
            </div>
          </div>
        </div>

        {/* The Geometric Insight */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Geometric Insight</h2>

          <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-4">
            <div className="font-mono text-center text-lg mb-2">
              Ω_Λ/Ω_m = 3Z/8 = (3/4) × √(8π/3)
            </div>
            <div className="text-center text-sm text-gray-600">
              = (spatial dims / spacetime dims) × √(8π/3)
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div className="border border-gray-200 rounded p-4">
              <div className="text-center mb-2">
                <span className="text-2xl">🔲</span>
              </div>
              <div className="text-center font-semibold text-gray-900">CUBE = 8</div>
              <div className="text-center text-sm text-gray-600">
                Matter: discrete, finite, localized
              </div>
            </div>
            <div className="border border-gray-200 rounded p-4">
              <div className="text-center mb-2">
                <span className="text-2xl">🔵</span>
              </div>
              <div className="text-center font-semibold text-gray-900">3Z = SPHERE-related</div>
              <div className="text-center text-sm text-gray-600">
                Vacuum: continuous, infinite, pervasive
              </div>
            </div>
          </div>

          <div className="bg-gray-50 border border-gray-200 rounded p-4">
            <div className="text-center text-gray-700">
              <strong>The universe's fate is the triumph of SPHERE over CUBE</strong>
            </div>
            <div className="text-center text-sm text-gray-600 mt-2">
              Early times: CUBE dominates (matter era)<br/>
              Late times: SPHERE dominates (Λ era)<br/>
              The transition is encoded in Z²
            </div>
          </div>
        </div>

        {/* Why Eternal? */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Why Eternal Expansion?</h2>

          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-sm font-bold flex-shrink-0">1</div>
              <div className="text-gray-700">
                <strong>Ω_Λ = 3Z/(8+3Z) &gt; 0</strong> for any positive Z
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-sm font-bold flex-shrink-0">2</div>
              <div className="text-gray-700">
                <strong>Z = 2√(8π/3) &gt; 0</strong> by mathematical necessity
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-green-100 text-green-700 flex items-center justify-center text-sm font-bold flex-shrink-0">∴</div>
              <div className="text-gray-700">
                <strong>Eternal expansion is encoded in the positivity of Z²</strong>
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-gray-900 text-white rounded text-center">
            <div className="text-gray-400 text-sm mb-2">The "End"</div>
            <div className="text-white">
              Not a stop, but an asymptotic approach to de Sitter equilibrium:
            </div>
            <div className="text-blue-300 mt-2 font-mono">
              Isolated MOND islands in an exponentially expanding sea
            </div>
          </div>
        </div>

        {/* Key Numbers */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Key Numbers from Z²</h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div className="bg-gray-50 rounded p-3 border border-gray-200">
              <div className="font-mono text-lg text-blue-700">{OMEGA_LAMBDA.toFixed(3)}</div>
              <div className="text-xs text-gray-500">Ω_Λ</div>
            </div>
            <div className="bg-gray-50 rounded p-3 border border-gray-200">
              <div className="font-mono text-lg text-blue-700">{OMEGA_MATTER.toFixed(3)}</div>
              <div className="text-xs text-gray-500">Ω_m</div>
            </div>
            <div className="bg-gray-50 rounded p-3 border border-gray-200">
              <div className="font-mono text-lg text-blue-700">{z_equality.toFixed(2)}</div>
              <div className="text-xs text-gray-500">z (matter=Λ)</div>
            </div>
            <div className="bg-gray-50 rounded p-3 border border-gray-200">
              <div className="font-mono text-lg text-blue-700">{z_transition.toFixed(2)}</div>
              <div className="text-xs text-gray-500">z (accel starts)</div>
            </div>
          </div>
        </div>

        {/* Links */}
        <div className="grid md:grid-cols-2 gap-4 mb-6">
          <Link
            href="/why-z2"
            className="block p-5 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 hover:shadow transition-all"
          >
            <div className="font-semibold text-gray-900 mb-1">Why Z² = 32π/3? →</div>
            <div className="text-sm text-gray-500">
              First principles derivation
            </div>
          </Link>

          <Link
            href="/early-universe"
            className="block p-5 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 hover:shadow transition-all"
          >
            <div className="font-semibold text-gray-900 mb-1">Early Universe →</div>
            <div className="text-sm text-gray-500">
              JWST predictions and cosmic dawn
            </div>
          </Link>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p>
            The universe expands forever — this is encoded in Z² = CUBE × SPHERE
          </p>
        </footer>
      </div>
    </main>
  )
}
