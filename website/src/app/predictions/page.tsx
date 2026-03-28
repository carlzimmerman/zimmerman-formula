'use client'

import Link from 'next/link'

const PI = Math.PI
const Z = 2 * Math.sqrt(8 * PI / 3)
const Z_SQUARED = Z * Z
const BEKENSTEIN = 3 * Z_SQUARED / (8 * PI)
const GAUGE = 9 * Z_SQUARED / (8 * PI)
const ALPHA_INV = 4 * Z_SQUARED + 3
const ALPHA = 1 / ALPHA_INV
const OMEGA_LAMBDA = (3 * Z) / (8 + 3 * Z)
const OMEGA_MATTER = 8 / (8 + 3 * Z)

// Neutrino masses
const M_E_EV = 511000
const M_NU_3 = M_E_EV * Math.pow(ALPHA, 3) / BEKENSTEIN * 1000
const M_NU_2 = M_NU_3 / Z
const SUM_M_NU = M_NU_2 + M_NU_3

// Higgs
const LAMBDA_HIGGS = (GAUGE + 1) / Math.pow(GAUGE - 2, 2)

// CP phase
const DELTA_CP = 180 * (GAUGE + 1) / GAUGE

// E(z) function
function E(z: number): number {
  return Math.sqrt(OMEGA_MATTER * Math.pow(1 + z, 3) + OMEGA_LAMBDA)
}

interface PredictionCardProps {
  number: number
  title: string
  experiment: string
  timeline: string
  prediction: string
  formula: string
  falsification: string
  status: 'upcoming' | 'in_progress' | 'matches'
}

function PredictionCard({ number, title, experiment, timeline, prediction, formula, falsification, status }: PredictionCardProps) {
  const statusColors = {
    upcoming: 'bg-blue-50 border-blue-200',
    in_progress: 'bg-amber-50 border-amber-200',
    matches: 'bg-green-50 border-green-200'
  }
  const statusLabels = {
    upcoming: 'Upcoming',
    in_progress: 'Data Coming',
    matches: 'Already Matches!'
  }
  const statusBadgeColors = {
    upcoming: 'bg-blue-100 text-blue-700',
    in_progress: 'bg-amber-100 text-amber-700',
    matches: 'bg-green-100 text-green-700'
  }

  return (
    <div className={`border rounded-lg p-5 ${statusColors[status]}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-2xl font-bold text-gray-400">#{number}</span>
          <div>
            <h3 className="font-semibold text-gray-900">{title}</h3>
            <p className="text-sm text-gray-500">{experiment} · {timeline}</p>
          </div>
        </div>
        <span className={`text-xs px-2 py-1 rounded-full ${statusBadgeColors[status]}`}>
          {statusLabels[status]}
        </span>
      </div>

      <div className="space-y-2 text-sm">
        <div>
          <span className="text-gray-500">Prediction: </span>
          <span className="font-medium text-gray-900">{prediction}</span>
        </div>
        <div>
          <span className="text-gray-500">Formula: </span>
          <span className="font-mono text-blue-700">{formula}</span>
        </div>
        <div>
          <span className="text-gray-500">Falsified if: </span>
          <span className="text-red-600">{falsification}</span>
        </div>
      </div>
    </div>
  )
}

export default function PredictionsPage() {
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
            10 Testable Predictions for 2026-2027
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            Specific, quantitative, falsifiable predictions from Z²
          </p>

          <div className="bg-amber-50 border border-amber-200 rounded p-4">
            <p className="text-sm text-amber-800">
              <strong>Scientific standard:</strong> Each prediction below includes a specific numerical value and a falsification threshold.
              If ANY prediction is definitively falsified, the framework requires revision or rejection.
            </p>
          </div>
        </article>

        {/* Summary Table */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6 overflow-x-auto">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Reference</h2>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-2 font-medium text-gray-600">#</th>
                <th className="text-left py-2 font-medium text-gray-600">Test</th>
                <th className="text-left py-2 font-medium text-gray-600">Prediction</th>
                <th className="text-left py-2 font-medium text-gray-600">Falsification</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              <tr>
                <td className="py-2 text-gray-400">1</td>
                <td className="py-2">JWST BTFR z=2</td>
                <td className="py-2 font-mono text-blue-700">-0.47 dex offset</td>
                <td className="py-2 text-red-600">&gt; -0.3 dex</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">2</td>
                <td className="py-2">DESI S8</td>
                <td className="py-2 font-mono text-blue-700">z-dependent</td>
                <td className="py-2 text-red-600">No evolution</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">3</td>
                <td className="py-2">Euclid lensing</td>
                <td className="py-2 font-mono text-blue-700">M_lens = M_bar</td>
                <td className="py-2 text-red-600">Requires DM</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">4</td>
                <td className="py-2">JUNO neutrinos</td>
                <td className="py-2 font-mono text-blue-700">Normal, m₁=0</td>
                <td className="py-2 text-red-600">Inverted</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">5</td>
                <td className="py-2">NOvA/T2K δ_CP</td>
                <td className="py-2 font-mono text-blue-700">195°</td>
                <td className="py-2 text-red-600">&lt;180° or &gt;210°</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">6</td>
                <td className="py-2">Gaia binaries</td>
                <td className="py-2 font-mono text-blue-700">MOND at &gt;7kAU</td>
                <td className="py-2 text-red-600">Newtonian</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">7</td>
                <td className="py-2">LHC Higgs λ</td>
                <td className="py-2 font-mono text-blue-700">0.13</td>
                <td className="py-2 text-red-600">&lt;0.11 or &gt;0.15</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">8</td>
                <td className="py-2">CMB Σmν</td>
                <td className="py-2 font-mono text-blue-700">58 meV</td>
                <td className="py-2 text-red-600">&lt;50 or &gt;70 meV</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">9</td>
                <td className="py-2">LSST H₀</td>
                <td className="py-2 font-mono text-blue-700">71.5 km/s/Mpc</td>
                <td className="py-2 text-red-600">&lt;69 or &gt;74</td>
              </tr>
              <tr>
                <td className="py-2 text-gray-400">10</td>
                <td className="py-2">SZ clusters</td>
                <td className="py-2 font-mono text-blue-700">2× enhanced z&gt;0.8</td>
                <td className="py-2 text-red-600">Matches ΛCDM</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Detailed Predictions */}
        <div className="space-y-4 mb-6">
          <h2 className="text-lg font-semibold text-gray-900">Detailed Predictions</h2>

          <PredictionCard
            number={1}
            title="JWST Baryonic Tully-Fisher Evolution"
            experiment="JWST NIRSpec Cycles 3-4"
            timeline="2026-2027"
            prediction={`BTFR offset at z=2: -${Math.log10(E(2)).toFixed(2)} dex`}
            formula="Δlog M_bar = -log₁₀(E(z))"
            falsification="Offset > -0.3 dex at z=2"
            status="upcoming"
          />

          <PredictionCard
            number={2}
            title="DESI Structure Growth (S8)"
            experiment="DESI Year 3 + BAO"
            timeline="Late 2026"
            prediction="S8 tension shows redshift dependence"
            formula="ΔS8 ∝ log(E(z))"
            falsification="S8 tension resolves with no z-evolution"
            status="in_progress"
          />

          <PredictionCard
            number={3}
            title="Euclid Weak Lensing Mass"
            experiment="Euclid DR1"
            timeline="2026"
            prediction="Lensing mass = baryonic mass (no dark matter)"
            formula="M_lens / M_bar = 1.0"
            falsification="Clear NFW profiles require dark matter halos"
            status="upcoming"
          />

          <PredictionCard
            number={4}
            title="JUNO Neutrino Mass Hierarchy"
            experiment="JUNO reactor oscillations"
            timeline="2026-2027"
            prediction={`Normal hierarchy, m₁=0, Σmν=${SUM_M_NU.toFixed(1)} meV`}
            formula="m₃ = m_e×α³/BEKENSTEIN, m₂ = m₃/Z, m₁ = 0"
            falsification="Inverted hierarchy or Σmν > 70 meV"
            status="upcoming"
          />

          <PredictionCard
            number={5}
            title="NOvA + T2K CP Violation Phase"
            experiment="NOvA, T2K neutrino beams"
            timeline="Ongoing"
            prediction={`δ_CP = ${DELTA_CP.toFixed(0)}° = 13π/12`}
            formula="δ_CP = π(GAUGE+1)/GAUGE"
            falsification="δ_CP < 180° or > 210° at 3σ"
            status="matches"
          />

          <PredictionCard
            number={6}
            title="Gaia DR4 Wide Binary Dynamics"
            experiment="Gaia DR4 proper motions"
            timeline="2026"
            prediction="MOND effects at separations > 7000 AU"
            formula="v/v_Newt = 1.3 at 15,000 AU"
            falsification="Newtonian v ∝ s^(-1/2) at all separations"
            status="in_progress"
          />

          <PredictionCard
            number={7}
            title="LHC Run 3 Higgs Self-Coupling"
            experiment="ATLAS + CMS di-Higgs"
            timeline="2026-2027"
            prediction={`λ = ${LAMBDA_HIGGS.toFixed(2)} = 13/100 (SM value)`}
            formula="λ = (GAUGE+1)/(GAUGE-2)²"
            falsification="λ < 0.11 or λ > 0.15"
            status="upcoming"
          />

          <PredictionCard
            number={8}
            title="CMB + BAO Neutrino Mass Sum"
            experiment="SPT-3G + Planck + BAO"
            timeline="2026"
            prediction={`Σmν = ${SUM_M_NU.toFixed(1)} meV (minimum for NH)`}
            formula="Σmν = m₃(1 + 1/Z)"
            falsification="Σmν > 70 meV or < 50 meV"
            status="upcoming"
          />

          <PredictionCard
            number={9}
            title="Rubin/LSST Strong Lensing H₀"
            experiment="LSST time delay cosmography"
            timeline="2026-2027"
            prediction="H₀ = 71.5 km/s/Mpc (between Planck and SH0ES)"
            formula="H₀ = Z × a₀ / c"
            falsification="H₀ < 69 or > 74 km/s/Mpc"
            status="upcoming"
          />

          <PredictionCard
            number={10}
            title="SZ Cluster Abundances"
            experiment="SPT-3G + ACT surveys"
            timeline="2027"
            prediction={`High-z clusters enhanced by factor ~${E(0.8).toFixed(1)}`}
            formula="Enhancement = E(z) at formation epoch"
            falsification="Cluster counts match ΛCDM exactly"
            status="upcoming"
          />
        </div>

        {/* Key Formulas */}
        <div className="bg-gray-900 text-white rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4 text-center">Underlying Formulas</h2>

          <div className="grid md:grid-cols-2 gap-4 font-mono text-sm">
            <div className="bg-gray-800 rounded p-3">
              <div className="text-blue-300 mb-1">Cosmology:</div>
              <div>E(z) = √(Ω_m(1+z)³ + Ω_Λ)</div>
              <div>a₀(z) = a₀(0) × E(z)</div>
              <div>H₀ = Z × a₀ / c</div>
            </div>
            <div className="bg-gray-800 rounded p-3">
              <div className="text-blue-300 mb-1">Neutrinos:</div>
              <div>m₃ = m_e × α³ / BEKENSTEIN</div>
              <div>m₂ = m₃ / Z</div>
              <div>δ_CP = 13π/12</div>
            </div>
            <div className="bg-gray-800 rounded p-3">
              <div className="text-blue-300 mb-1">Higgs:</div>
              <div>λ = (GAUGE+1)/(GAUGE-2)²</div>
              <div>m_H = v × √(2λ)</div>
            </div>
            <div className="bg-gray-800 rounded p-3">
              <div className="text-blue-300 mb-1">MOND:</div>
              <div>s_crit = √(GM/a₀)</div>
              <div>v_MOND = (GMa₀)^(1/4)</div>
            </div>
          </div>
        </div>

        {/* Timeline */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Expected Timeline</h2>

          <div className="space-y-3">
            <div className="flex items-center gap-4">
              <div className="w-20 text-sm font-medium text-gray-500">2026 Q1</div>
              <div className="flex-1 bg-blue-100 rounded p-2 text-sm">Euclid DR1, DESI Year 3 preliminary</div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-20 text-sm font-medium text-gray-500">2026 Q2</div>
              <div className="flex-1 bg-blue-100 rounded p-2 text-sm">Gaia DR4, NOvA/T2K updates</div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-20 text-sm font-medium text-gray-500">2026 Q3</div>
              <div className="flex-1 bg-blue-100 rounded p-2 text-sm">JUNO first hierarchy results, CMB constraints</div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-20 text-sm font-medium text-gray-500">2026 Q4</div>
              <div className="flex-1 bg-blue-100 rounded p-2 text-sm">LSST Year 1, JWST Cycle 4 data</div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-20 text-sm font-medium text-gray-500">2027</div>
              <div className="flex-1 bg-amber-100 rounded p-2 text-sm">LHC Run 3 full analysis, SPT-3G clusters, comprehensive tests</div>
            </div>
          </div>
        </div>

        {/* What happens if... */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Outcomes</h2>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-green-50 border border-green-200 rounded p-4">
              <h3 className="font-semibold text-green-800 mb-2">If Predictions Confirmed</h3>
              <ul className="text-sm text-green-700 space-y-1">
                <li>• Z² = 32π/3 is fundamental to physics</li>
                <li>• MOND explains galaxy dynamics</li>
                <li>• Dark matter paradigm needs revision</li>
                <li>• Neutrino physics connected to geometry</li>
              </ul>
            </div>
            <div className="bg-red-50 border border-red-200 rounded p-4">
              <h3 className="font-semibold text-red-800 mb-2">If Predictions Falsified</h3>
              <ul className="text-sm text-red-700 space-y-1">
                <li>• Framework requires revision</li>
                <li>• Specific failures indicate where</li>
                <li>• Numerology without physical basis</li>
                <li>• Back to standard ΛCDM + dark matter</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Links */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <Link
            href="/all-derivations"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">All Derivations</div>
            <div className="text-sm text-gray-500">30+ quantities from Z²</div>
          </Link>
          <Link
            href="/evidence"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Current Evidence</div>
            <div className="text-sm text-gray-500">JWST, DESI, Gaia</div>
          </Link>
          <Link
            href="/why-z2"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Why Z²?</div>
            <div className="text-sm text-gray-500">First principles</div>
          </Link>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p>Predictions generated March 2026 · Updates will be posted as data arrives</p>
        </footer>
      </div>
    </main>
  )
}
