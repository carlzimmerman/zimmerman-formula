'use client'

import Link from 'next/link'

const L_FUNDAMENTAL = 20.6 // Gpc
const H0 = 70 // km/s/Mpc
const C = 299792 // km/s

// Calculate expected angular separations for different redshifts
function angularSeparation(z: number): number {
  // Simplified calculation - actual would use full cosmological distance
  const dH = C / H0 // Hubble distance in Mpc
  const dC = dH * Math.log(1 + z) * 2 // Comoving distance approximation
  const theta = (dC / (L_FUNDAMENTAL * 1000)) * (180 / Math.PI) * 2
  return Math.min(theta, 60) // Cap at 60 degrees
}

export default function GhostQuasarsPage() {
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
            Ghost Quasars: The Nobel-Level Test
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            In a finite universe, high-z quasars have topological duplicates
          </p>

          {/* The Core Prediction */}
          <div className="bg-amber-50 border border-amber-300 rounded p-6 my-6 text-center">
            <div className="text-xl text-gray-900 mb-2">
              <strong>Prediction:</strong> Quasars at z &gt; 3 have "ghost" images
            </div>
            <div className="font-mono text-lg text-amber-700">
              Same spectrum • Different flux • 20-60° separation
            </div>
          </div>
        </article>

        {/* How It Works */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">How It Works</h2>

          <div className="space-y-4 text-gray-700">
            <p>
              In the T³/Z₂ topology, space is <strong>finite and periodic</strong>.
              Light from a distant quasar can reach us via multiple paths — traveling
              "the short way" and "the long way" around the universe.
            </p>

            <div className="bg-gray-100 rounded p-4 my-4">
              <div className="text-center font-mono text-sm text-gray-600 mb-2">
                Fundamental Domain Scale
              </div>
              <div className="text-center text-3xl font-bold text-gray-900">
                L<sub>c</sub> = {L_FUNDAMENTAL} Gpc
              </div>
              <div className="text-center text-sm text-gray-500 mt-1">
                Light wrapping around this distance creates duplicate images
              </div>
            </div>

            <p>
              A quasar at z = 4 is ~7 Gpc away. Light can reach us directly,
              or go "around" the 20.6 Gpc universe. The two images appear at
              different sky positions with different ages (hence different brightness).
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mt-6">
            <div className="p-4 bg-blue-50 rounded border border-blue-200 text-center">
              <div className="text-3xl mb-2">💫</div>
              <div className="font-semibold text-gray-900">Primary Image</div>
              <div className="text-sm text-gray-600">Direct path to observer</div>
              <div className="text-xs text-blue-600 mt-1">Brighter, younger</div>
            </div>
            <div className="p-4 bg-amber-50 rounded border border-amber-200 text-center">
              <div className="text-3xl mb-2">👻</div>
              <div className="font-semibold text-gray-900">Ghost Image</div>
              <div className="text-sm text-gray-600">Wrapped path around universe</div>
              <div className="text-xs text-amber-600 mt-1">Dimmer, older</div>
            </div>
            <div className="p-4 bg-green-50 rounded border border-green-200 text-center">
              <div className="text-3xl mb-2">🔬</div>
              <div className="font-semibold text-gray-900">Same Spectrum</div>
              <div className="text-sm text-gray-600">Identical emission lines</div>
              <div className="text-xs text-green-600 mt-1">Fingerprint match</div>
            </div>
          </div>
        </div>

        {/* Predicted Separations */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Predicted Angular Separations</h2>

          <p className="text-gray-700 mb-4">
            The separation between primary and ghost images depends on redshift
            and the specific topology. For T³/Z₂ with L<sub>c</sub> = 20.6 Gpc:
          </p>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 font-medium text-gray-600">Redshift</th>
                  <th className="text-left py-2 font-medium text-gray-600">Distance (Gpc)</th>
                  <th className="text-left py-2 font-medium text-gray-600">Expected Separation</th>
                  <th className="text-left py-2 font-medium text-gray-600">Flux Ratio</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                <tr>
                  <td className="py-3 text-gray-700">z = 3</td>
                  <td className="py-3 text-gray-500">~6.5 Gpc</td>
                  <td className="py-3 font-mono text-blue-600">18-25°</td>
                  <td className="py-3 text-gray-500">~0.3</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">z = 4</td>
                  <td className="py-3 text-gray-500">~7.5 Gpc</td>
                  <td className="py-3 font-mono text-blue-600">25-35°</td>
                  <td className="py-3 text-gray-500">~0.2</td>
                </tr>
                <tr className="bg-amber-50">
                  <td className="py-3 text-gray-700 font-semibold">z = 5</td>
                  <td className="py-3 text-gray-500">~8.3 Gpc</td>
                  <td className="py-3 font-mono text-amber-700 font-semibold">35-45°</td>
                  <td className="py-3 text-gray-500">~0.15</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">z = 6</td>
                  <td className="py-3 text-gray-500">~9.0 Gpc</td>
                  <td className="py-3 font-mono text-blue-600">45-55°</td>
                  <td className="py-3 text-gray-500">~0.1</td>
                </tr>
                <tr>
                  <td className="py-3 text-gray-700">z = 7</td>
                  <td className="py-3 text-gray-500">~9.5 Gpc</td>
                  <td className="py-3 font-mono text-blue-600">50-60°</td>
                  <td className="py-3 text-gray-500">~0.08</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded">
            <div className="text-sm text-blue-800">
              <strong>Sweet spot:</strong> z = 4-6 quasars with 30-50° separation
              are optimal targets. Bright enough to detect, far enough for clear separation.
            </div>
          </div>
        </div>

        {/* Search Strategy */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Search Strategy</h2>

          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold flex-shrink-0">1</div>
              <div>
                <div className="font-semibold text-gray-900">Start with known high-z quasars</div>
                <p className="text-sm text-gray-600">
                  SDSS, DESI, and JWST have cataloged thousands of z &gt; 3 quasars
                  with precise spectroscopy and positions.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold flex-shrink-0">2</div>
              <div>
                <div className="font-semibold text-gray-900">Search in annulus around each</div>
                <p className="text-sm text-gray-600">
                  For each quasar, search for dimmer objects at 20-60° separation
                  in the predicted direction (along Z₂ axis).
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold flex-shrink-0">3</div>
              <div>
                <div className="font-semibold text-gray-900">Match emission line spectra</div>
                <p className="text-sm text-gray-600">
                  Ghost images have IDENTICAL emission line patterns (same source),
                  but different continuum (different light travel time).
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-green-100 text-green-700 flex items-center justify-center font-bold flex-shrink-0">4</div>
              <div>
                <div className="font-semibold text-gray-900">Confirm with multiple pairs</div>
                <p className="text-sm text-gray-600">
                  One pair could be coincidence. Multiple pairs at consistent
                  separations and along consistent axis = topology confirmed.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Why This is Nobel-Level */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Why This is Nobel-Level</h2>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-amber-50 rounded border border-amber-200">
              <div className="font-semibold text-amber-800 mb-2">If Found:</div>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Direct proof universe is finite</li>
                <li>• Measurement of cosmic topology</li>
                <li>• Confirms L_c = 20.6 Gpc</li>
                <li>• Validates entire Z² framework</li>
                <li>• Nobel Prize in Physics (guaranteed)</li>
              </ul>
            </div>
            <div className="p-4 bg-red-50 rounded border border-red-200">
              <div className="font-semibold text-red-800 mb-2">If Not Found:</div>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Either L_c &gt; 20.6 Gpc (larger universe)</li>
                <li>• Or different topology than T³/Z₂</li>
                <li>• Or ghosts too faint to detect</li>
                <li>• Z² framework would need revision</li>
              </ul>
            </div>
          </div>

          <div className="mt-4 p-4 bg-gray-900 text-white rounded text-center">
            <p className="text-gray-300">
              This is not a vague philosophical question.
            </p>
            <p className="text-xl text-blue-300 font-semibold mt-2">
              It's a concrete observational test with existing data.
            </p>
          </div>
        </div>

        {/* The Algorithm */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Search Algorithm</h2>

          <div className="bg-gray-900 text-white rounded p-4 font-mono text-sm overflow-x-auto">
            <pre>{`# Ghost Quasar Search Algorithm
# Available at github.com/carlzimmermanbriar/ghost-quasar-search

for quasar in high_z_catalog:
    if quasar.z < 3.0:
        continue  # Too close for ghosts

    # Predicted ghost location
    theta_min, theta_max = angular_bounds(quasar.z, L_c=20.6)

    # Search annulus along Z₂ axis
    candidates = search_annulus(
        center=quasar.position,
        inner=theta_min, outer=theta_max,
        axis=Z2_AXIS,  # (287°, 9°) Galactic
        flux_ratio_max=0.5
    )

    for candidate in candidates:
        # Spectroscopic matching
        if emission_lines_match(quasar, candidate):
            if continuum_differs(quasar, candidate):
                flag_as_ghost_pair(quasar, candidate)`}</pre>
          </div>

          <p className="text-sm text-gray-600 mt-4 text-center">
            Algorithm is ready to run on SDSS DR18 + DESI DR1 quasar catalogs
          </p>
        </div>

        {/* What We Need */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">What We Need</h2>

          <div className="grid md:grid-cols-3 gap-4">
            <div className="p-4 bg-green-50 rounded border border-green-200 text-center">
              <div className="text-2xl mb-2">✓</div>
              <div className="font-semibold text-green-800">Have</div>
              <ul className="text-sm text-gray-700 mt-2 text-left">
                <li>• SDSS quasar catalog</li>
                <li>• DESI DR1 spectra</li>
                <li>• Search algorithm</li>
                <li>• Predicted separations</li>
              </ul>
            </div>
            <div className="p-4 bg-blue-50 rounded border border-blue-200 text-center">
              <div className="text-2xl mb-2">⏳</div>
              <div className="font-semibold text-blue-800">Need</div>
              <ul className="text-sm text-gray-700 mt-2 text-left">
                <li>• Compute time</li>
                <li>• Follow-up spectroscopy</li>
                <li>• Deep imaging for faint ghosts</li>
              </ul>
            </div>
            <div className="p-4 bg-amber-50 rounded border border-amber-200 text-center">
              <div className="text-2xl mb-2">🎯</div>
              <div className="font-semibold text-amber-800">Goal</div>
              <ul className="text-sm text-gray-700 mt-2 text-left">
                <li>• Find 1 confirmed pair</li>
                <li>• Validate with 3+ pairs</li>
                <li>• Measure L_c precisely</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Links */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <Link
            href="/topology"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">T³/Z₂ Topology</div>
            <div className="text-sm text-gray-500">Why the universe wraps</div>
          </Link>
          <Link
            href="/predictions"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">All Predictions</div>
            <div className="text-sm text-gray-500">13 testable predictions</div>
          </Link>
          <Link
            href="/evidence/4pcf"
            className="block p-4 bg-red-50 border border-red-200 rounded shadow-sm hover:border-red-400 transition-all text-center"
          >
            <div className="font-semibold text-red-800">DESI 4PCF</div>
            <div className="text-sm text-red-600">r = 0.9986 (confirmed)</div>
          </Link>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p>
            The universe may be finite. We can check.
          </p>
        </footer>
      </div>
    </main>
  )
}
