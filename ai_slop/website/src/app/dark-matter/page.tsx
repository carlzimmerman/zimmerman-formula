'use client'

import Link from 'next/link'

const OMEGA_MATTER = 6 / 19
const OMEGA_LAMBDA = 13 / 19
const SIN2_WEINBERG = 3 / 13

export default function DarkMatterPage() {
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
            Dark Matter is Topological
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            40 years of null searches explained: there are no particles to find
          </p>

          {/* The Core Result */}
          <div className="bg-blue-50 border border-blue-200 rounded p-6 my-6 text-center">
            <div className="font-mono text-xl text-gray-900 mb-2">
              Ω<sub>m</sub> = 6/19 = 0.3158
            </div>
            <div className="text-sm text-gray-600 mt-3">
              Derived from T³ winding modes — no particles, no WIMPs, no axions
            </div>
          </div>
        </article>

        {/* The 40-Year Null Result */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The 40-Year Mystery</h2>

          <div className="space-y-4 text-gray-700">
            <p>
              Since the 1980s, physicists have searched for dark matter particles.
              Every experiment has found <strong>nothing</strong>:
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-4 mt-4">
            <div className="p-4 bg-red-50 rounded border border-red-200">
              <div className="font-semibold text-red-800 mb-2">WIMPs (Weakly Interacting)</div>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• LUX-ZEPLIN: null</li>
                <li>• PandaX-4T: null</li>
                <li>• XENONnT: null</li>
                <li>• CDMS: null</li>
              </ul>
              <div className="text-xs text-red-600 mt-2">Cross-section limits: &lt;10⁻⁴⁷ cm²</div>
            </div>
            <div className="p-4 bg-red-50 rounded border border-red-200">
              <div className="font-semibold text-red-800 mb-2">Axions (Ultralight)</div>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• ADMX: null</li>
                <li>• HAYSTAC: null</li>
                <li>• ABRACADABRA: null</li>
                <li>• CASPEr: null</li>
              </ul>
              <div className="text-xs text-red-600 mt-2">Coupling limits: &lt;10⁻¹⁵ GeV⁻¹</div>
            </div>
          </div>

          <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded">
            <p className="text-amber-800 text-center">
              <strong>Standard explanation:</strong> "The particles exist but are even harder to detect"
            </p>
            <p className="text-amber-700 text-center text-sm mt-1">
              Z² explanation: <strong>There are no particles. The effect is topological.</strong>
            </p>
          </div>
        </div>

        {/* The Topological Origin */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Topological Origin</h2>

          <p className="text-gray-700 mb-4">
            In the T³/Z₂ topology, space wraps around periodically. A scalar field φ
            can wind around these cycles. These <strong>winding modes</strong> carry
            energy but have no localized particle interpretation.
          </p>

          <div className="bg-gray-900 text-white rounded p-6 font-mono text-center mb-4">
            <div className="text-blue-300 text-sm mb-2">T³ has b₁ = 3 independent 1-cycles:</div>
            <div className="grid grid-cols-3 gap-4 my-4">
              <div className="p-3 bg-gray-800 rounded">
                <div className="text-2xl">↔️</div>
                <div className="text-xs text-gray-400">x-cycle</div>
              </div>
              <div className="p-3 bg-gray-800 rounded">
                <div className="text-2xl">↕️</div>
                <div className="text-xs text-gray-400">y-cycle</div>
              </div>
              <div className="p-3 bg-gray-800 rounded">
                <div className="text-2xl">⬆️</div>
                <div className="text-xs text-gray-400">z-cycle</div>
              </div>
            </div>
            <div className="text-gray-300">
              Each cycle supports 2 winding modes (complex field)
            </div>
            <div className="text-xl text-green-400 mt-2">
              3 cycles × 2 modes = <strong>6</strong> topological degrees of freedom
            </div>
          </div>

          <div className="bg-green-50 border border-green-200 rounded p-4">
            <div className="font-semibold text-green-800 mb-2">The Derivation:</div>
            <div className="space-y-2 text-sm text-gray-700">
              <div>1. T³/Z₂ has 19 total degrees of freedom (6 winding + 13 vacuum)</div>
              <div>2. Energy distributes according to equipartition</div>
              <div>3. Winding modes (matter): <strong>Ω_m = 6/19 = 0.3158</strong></div>
              <div>4. Vacuum modes (dark energy): <strong>Ω_Λ = 13/19 = 0.6842</strong></div>
            </div>
          </div>
        </div>

        {/* The Cosmic Weinberg Relation */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Cosmic Weinberg Relation</h2>

          <p className="text-gray-700 mb-4">
            The ratio of matter to dark energy has a remarkable connection to
            the electroweak Weinberg angle:
          </p>

          <div className="bg-red-50 border border-red-300 rounded p-6 text-center mb-4">
            <div className="font-mono text-2xl text-gray-900 mb-2">
              Ω<sub>m</sub>/Ω<sub>Λ</sub> = 6/13 = 2 × sin²θ<sub>W</sub>
            </div>
            <div className="text-sm text-red-700 mt-2">
              The dark sector ratio equals twice the Weinberg angle!
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-blue-50 rounded border border-blue-200 text-center">
              <div className="text-sm text-gray-600 mb-1">Matter/Dark Energy Ratio</div>
              <div className="font-mono text-xl text-blue-700">6/13 = 0.4615</div>
            </div>
            <div className="p-4 bg-amber-50 rounded border border-amber-200 text-center">
              <div className="text-sm text-gray-600 mb-1">2 × sin²θ_W</div>
              <div className="font-mono text-xl text-amber-700">2 × 3/13 = 0.4615</div>
            </div>
          </div>

          <p className="text-gray-600 text-sm mt-4 text-center">
            This is not a coincidence — both arise from the same T³/Z₂ topology
          </p>
        </div>

        {/* Why No Particles? */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Why No Particles?</h2>

          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold flex-shrink-0">1</div>
              <div>
                <div className="font-semibold text-gray-900">Winding modes are non-local</div>
                <p className="text-sm text-gray-600">
                  A field winding around the universe isn't localized anywhere.
                  It cannot be detected by local particle detectors.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-green-100 text-green-700 flex items-center justify-center font-bold flex-shrink-0">2</div>
              <div>
                <div className="font-semibold text-gray-900">Gravitational effects are global</div>
                <p className="text-sm text-gray-600">
                  The winding modes affect spacetime curvature uniformly,
                  mimicking a uniform matter distribution — "dark matter."
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center font-bold flex-shrink-0">3</div>
              <div>
                <div className="font-semibold text-gray-900">No coupling to Standard Model</div>
                <p className="text-sm text-gray-600">
                  Topological modes don't interact with electromagnetic or weak forces.
                  Only gravity "sees" them — exactly as observed.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-red-100 text-red-700 flex items-center justify-center font-bold flex-shrink-0">4</div>
              <div>
                <div className="font-semibold text-gray-900">Explains 40 years of nulls</div>
                <p className="text-sm text-gray-600">
                  No WIMP cross-section, no axion coupling, no annihilation signal —
                  because there's nothing to detect. The 6/19 is already there.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Comparison Table */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Particle vs. Topological Dark Matter</h2>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 font-medium text-gray-600">Property</th>
                  <th className="text-left py-2 font-medium text-gray-600">Particle DM</th>
                  <th className="text-left py-2 font-medium text-gray-600">Topological DM</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                <tr>
                  <td className="py-3 text-gray-700">Nature</td>
                  <td className="py-3 text-gray-500">New particles (WIMPs, axions)</td>
                  <td className="py-3 text-green-600 font-medium">T³ winding modes</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Direct detection</td>
                  <td className="py-3 text-red-500">Should work (but doesn't)</td>
                  <td className="py-3 text-green-600 font-medium">Impossible (non-local)</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Density</td>
                  <td className="py-3 text-gray-500">Free parameter</td>
                  <td className="py-3 text-green-600 font-medium">Ω_m = 6/19 (derived)</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Collider production</td>
                  <td className="py-3 text-red-500">Should work (but doesn't)</td>
                  <td className="py-3 text-green-600 font-medium">Impossible (topological)</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Annihilation signal</td>
                  <td className="py-3 text-red-500">Expected (not seen)</td>
                  <td className="py-3 text-green-600 font-medium">None (no particles)</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">Galaxy rotation</td>
                  <td className="py-3 text-gray-500">Requires halo tuning</td>
                  <td className="py-3 text-green-600 font-medium">MOND from a₀ = cH₀/Z</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Observational Predictions */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Predictions</h2>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-green-50 rounded border border-green-200">
              <div className="font-semibold text-green-800 mb-2">✓ Already Confirmed</div>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• No WIMP detection (all experiments)</li>
                <li>• No axion detection (all experiments)</li>
                <li>• No LHC dark matter production</li>
                <li>• Ω_m ≈ 0.315 (Planck)</li>
              </ul>
            </div>
            <div className="p-4 bg-blue-50 rounded border border-blue-200">
              <div className="font-semibold text-blue-800 mb-2">Still To Test</div>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Ghost quasar duplicates</li>
                <li>• CMB matched circles</li>
                <li>• 4PCF chirality axis direction</li>
                <li>• kSZ velocity at vertices</li>
              </ul>
            </div>
          </div>
        </div>

        {/* The Bottom Line */}
        <div className="bg-gray-900 text-white rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4 text-center">The Bottom Line</h2>

          <div className="space-y-3 text-center">
            <p className="text-gray-300">
              Dark matter search experiments are not failing.
            </p>
            <p className="text-gray-300">
              They are succeeding at proving there are no particles.
            </p>
            <p className="text-xl text-blue-300 font-semibold mt-4">
              Ω_m = 6/19 is topological, not particulate.
            </p>
          </div>
        </div>

        {/* Links */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <Link
            href="/topology"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">T³/Z₂ Topology</div>
            <div className="text-sm text-gray-500">The underlying structure</div>
          </Link>
          <Link
            href="/cosmic-fate"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Cosmic Fate</div>
            <div className="text-sm text-gray-500">Ω_Λ = 13/19 derivation</div>
          </Link>
          <Link
            href="/evidence"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Evidence Timeline</div>
            <div className="text-sm text-gray-500">40 years of null results</div>
          </Link>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p>
            Sometimes the null result IS the discovery
          </p>
        </footer>
      </div>
    </main>
  )
}
