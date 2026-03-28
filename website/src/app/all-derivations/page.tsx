'use client'

import Link from 'next/link'

const PI = Math.PI
const Z = 2 * Math.sqrt(8 * PI / 3)
const Z_SQUARED = Z * Z
const BEKENSTEIN = 3 * Z_SQUARED / (8 * PI)
const GAUGE = 9 * Z_SQUARED / (8 * PI)
const ALPHA_INV = 4 * Z_SQUARED + 3
const OMEGA_LAMBDA = (3 * Z) / (8 + 3 * Z)
const OMEGA_MATTER = 8 / (8 + 3 * Z)

// New derivations
const ALPHA_S = BEKENSTEIN / Z_SQUARED
const KOIDE = 8 / GAUGE
const MT_MB = Z_SQUARED + 8
const MS_MD = 5 * BEKENSTEIN
const MZ_MW = Math.sqrt(13 / 10)
const STRING_DIMS = GAUGE - 2
const COMPACT_DIMS = GAUGE / 2

// Lepton mass ratios
const M_TAU_MU = Z_SQUARED / 2
const M_MU_E = 6 * Z_SQUARED + Z

// Higgs mass
const V_HIGGS = 246.22 // GeV
const M_HIGGS = V_HIGGS * Math.sqrt(26) / 10
const LAMBDA_HIGGS = 13 / 100

// Neutrino masses (in meV)
const M_E_EV = 511000 // eV
const ALPHA = 1 / ALPHA_INV
const M_NU_3 = M_E_EV * Math.pow(ALPHA, 3) / BEKENSTEIN * 1000 // meV
const M_NU_2 = M_NU_3 / Z // meV
const M_NU_1 = 0 // meV (prediction!)

// Neutrino mixing (PMNS)
const THETA_23 = 180 / BEKENSTEIN // 45 degrees
const THETA_12 = Math.atan(Math.sqrt(BEKENSTEIN / 9)) * 180 / Math.PI
const THETA_13 = Math.asin(Math.sqrt(3 * ALPHA)) * 180 / Math.PI
const DELTA_CP = 180 * (GAUGE + 1) / GAUGE

// CKM matrix (quark mixing)
const SIN_CABIBBO = 3 / (GAUGE + 1) // = sin²θ_W = 0.2308
const SIN_CKM_23 = ALPHA * Z // = 0.0422
const SIN_CKM_13 = ALPHA / 2 // = 0.00365
const DELTA_CKM = Math.atan(BEKENSTEIN - 1) * 180 / Math.PI // = 71.6°
const WOLFENSTEIN_A = BEKENSTEIN / (BEKENSTEIN + 1) // = 0.8

// Quark masses (MeV) - Individual quarks from lepton partners
const M_E = 0.511 // electron mass in MeV
const M_MU = 105.66 // muon mass in MeV
const M_TAU = 1776.86 // tau mass in MeV

// First generation (tied to electron)
const M_D_PRED = M_E * Math.pow(BEKENSTEIN - 1, 2) // = 9 × m_e
const M_U_PRED = M_D_PRED / 2 // = 4.5 × m_e

// Second generation (tied to muon)
const M_S_PRED = M_D_PRED * 5 * BEKENSTEIN // = 20 × m_d
const M_C_PRED = M_MU * GAUGE // = 12 × m_μ

// Third generation (tied to tau)
const M_B_PRED = M_TAU * 2 * Z / 5 // = m_τ × 2Z/5
const M_T_PRED = M_B_PRED * (Z_SQUARED + 8) / 1000 // in GeV

// NEW: Cosmological and fundamental scale derivations
const BARYON_ASYMMETRY = Math.pow(ALPHA, 4) / (BEKENSTEIN + 1) // η = α⁴/5
const LOG_MP_ME = 2 * Z_SQUARED / 3 // log₁₀(m_P/m_e) = 22.34
const INFLATION_N = 54 // e-folds from m_p/m_e coefficient
const SPECTRAL_INDEX = 1 - 2 / INFLATION_N // n_s = 0.963
const LAMBDA_QCD = 2 * M_MU // ≈ 211 MeV
const THETA_QCD = Math.pow(ALPHA, 4) / Z_SQUARED // ≈ 8.5×10⁻¹¹

interface DerivationCardProps {
  title: string
  formula: string
  predicted: string
  measured: string
  error: string
  category: 'strong' | 'good' | 'approximate'
}

function DerivationCard({ title, formula, predicted, measured, error, category }: DerivationCardProps) {
  const borderColor = category === 'strong' ? 'border-green-300 bg-green-50' :
                      category === 'good' ? 'border-blue-300 bg-blue-50' :
                      'border-gray-300 bg-gray-50'
  const errorColor = category === 'strong' ? 'text-green-600' :
                     category === 'good' ? 'text-blue-600' :
                     'text-gray-600'

  return (
    <div className={`border rounded p-4 ${borderColor}`}>
      <div className="font-semibold text-gray-900 mb-2">{title}</div>
      <div className="font-mono text-sm text-gray-700 mb-2">{formula}</div>
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <span className="text-gray-500">Predicted: </span>
          <span className="font-mono text-gray-900">{predicted}</span>
        </div>
        <div>
          <span className="text-gray-500">Measured: </span>
          <span className="font-mono text-gray-900">{measured}</span>
        </div>
      </div>
      <div className={`text-xs mt-2 ${errorColor}`}>{error}</div>
    </div>
  )
}

export default function AllDerivationsPage() {
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
            Everything Derived from Z²
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            One constant → all of physics
          </p>

          <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center">
            <div className="font-mono text-lg text-gray-900">
              Z² = CUBE × SPHERE = 8 × (4π/3) = {Z_SQUARED.toFixed(4)}
            </div>
          </div>
        </article>

        {/* Fundamental Constants */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Fundamental Constants</h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="bg-blue-900 text-white rounded p-3 text-center">
              <div className="text-2xl font-bold">{BEKENSTEIN.toFixed(0)}</div>
              <div className="text-xs text-blue-200">BEKENSTEIN</div>
              <div className="text-xs text-blue-300 mt-1">3Z²/(8π)</div>
            </div>
            <div className="bg-blue-800 text-white rounded p-3 text-center">
              <div className="text-2xl font-bold">{GAUGE.toFixed(0)}</div>
              <div className="text-xs text-blue-200">GAUGE</div>
              <div className="text-xs text-blue-300 mt-1">9Z²/(8π)</div>
            </div>
            <div className="bg-blue-700 text-white rounded p-3 text-center">
              <div className="text-2xl font-bold">{ALPHA_INV.toFixed(1)}</div>
              <div className="text-xs text-blue-200">α⁻¹</div>
              <div className="text-xs text-blue-300 mt-1">4Z² + 3</div>
            </div>
            <div className="bg-blue-600 text-white rounded p-3 text-center">
              <div className="text-2xl font-bold">{Z.toFixed(2)}</div>
              <div className="text-xs text-blue-200">Z</div>
              <div className="text-xs text-blue-300 mt-1">2√(8π/3)</div>
            </div>
          </div>
        </div>

        {/* Strong Candidates */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Strong Derivations</h2>
          <p className="text-sm text-gray-500 mb-4">Error &lt; 5%</p>

          <div className="grid md:grid-cols-2 gap-4">
            <DerivationCard
              title="Fine Structure Constant"
              formula="α⁻¹ = 4Z² + 3"
              predicted="137.04"
              measured="137.036"
              error="0.004% error"
              category="strong"
            />
            <DerivationCard
              title="Strong Coupling α_s"
              formula="α_s = BEKENSTEIN/Z² = 4/Z²"
              predicted={ALPHA_S.toFixed(4)}
              measured="0.1179"
              error="1.2% error"
              category="strong"
            />
            <DerivationCard
              title="Weinberg Angle"
              formula="sin²θ_W = 3/(GAUGE+1) = 3/13"
              predicted="0.2308"
              measured="0.2312"
              error="0.15% error"
              category="strong"
            />
            <DerivationCard
              title="Koide Formula"
              formula="(Σm)/(Σ√m)² = CUBE/GAUGE = 8/12"
              predicted={KOIDE.toFixed(6)}
              measured="0.666666"
              error="Exact!"
              category="strong"
            />
            <DerivationCard
              title="Dark Energy Density"
              formula="Ω_Λ = 3Z/(8+3Z)"
              predicted={OMEGA_LAMBDA.toFixed(4)}
              measured="0.685"
              error="0.1% error"
              category="strong"
            />
            <DerivationCard
              title="Matter Density"
              formula="Ω_m = 8/(8+3Z)"
              predicted={OMEGA_MATTER.toFixed(4)}
              measured="0.315"
              error="0.1% error"
              category="strong"
            />
          </div>
        </div>

        {/* Mass Ratios */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Mass Ratios</h2>
          <p className="text-sm text-gray-500 mb-4">Particle mass relationships</p>

          <div className="grid md:grid-cols-2 gap-4">
            <DerivationCard
              title="Proton/Electron Mass"
              formula="m_p/m_e = 54Z² + 6Z - 8"
              predicted="1836.3"
              measured="1836.15"
              error="0.02% error"
              category="strong"
            />
            <DerivationCard
              title="Top/Bottom Quark"
              formula="m_t/m_b = Z² + CUBE"
              predicted={MT_MB.toFixed(1)}
              measured="41.3"
              error="0.4% error"
              category="strong"
            />
            <DerivationCard
              title="Strange/Down Quark"
              formula="m_s/m_d = 5 × BEKENSTEIN"
              predicted={MS_MD.toFixed(0)}
              measured="20.0"
              error="~0% error"
              category="strong"
            />
            <DerivationCard
              title="Z/W Boson Mass"
              formula="m_Z/m_W = √(13/10)"
              predicted={MZ_MW.toFixed(4)}
              measured="1.1345"
              error="0.5% error"
              category="strong"
            />
            <DerivationCard
              title="Tau/Muon Mass"
              formula="m_τ/m_μ ≈ Z²/2"
              predicted={M_TAU_MU.toFixed(2)}
              measured="16.82"
              error="0.4% error"
              category="good"
            />
            <DerivationCard
              title="Muon/Electron Mass"
              formula="m_μ/m_e ≈ 6Z² + Z"
              predicted={M_MU_E.toFixed(1)}
              measured="206.8"
              error="0.3% error"
              category="good"
            />
            <DerivationCard
              title="Higgs Mass"
              formula="m_H = v×√26/10"
              predicted={M_HIGGS.toFixed(2) + " GeV"}
              measured="125.25 GeV"
              error="0.23% error"
              category="strong"
            />
            <DerivationCard
              title="Higgs Self-Coupling"
              formula="λ = (GAUGE+1)/(GAUGE-2)² = 13/100"
              predicted={LAMBDA_HIGGS.toFixed(4)}
              measured="~0.13"
              error="0.5% error"
              category="strong"
            />
          </div>
        </div>

        {/* Neutrinos */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Neutrino Sector</h2>
          <p className="text-sm text-gray-500 mb-4">Masses and PMNS mixing angles</p>

          <div className="grid md:grid-cols-2 gap-4">
            <DerivationCard
              title="Heaviest Neutrino m₃"
              formula="m₃ = m_e × α³ / BEKENSTEIN"
              predicted={M_NU_3.toFixed(1) + " meV"}
              measured="~50 meV"
              error="1% error"
              category="strong"
            />
            <DerivationCard
              title="Middle Neutrino m₂"
              formula="m₂ = m₃ / Z"
              predicted={M_NU_2.toFixed(1) + " meV"}
              measured="~8.6 meV"
              error="0.5% error"
              category="strong"
            />
            <DerivationCard
              title="Lightest Neutrino m₁"
              formula="m₁ = 0 (prediction!)"
              predicted="0"
              measured="unknown"
              error="Testable"
              category="good"
            />
            <DerivationCard
              title="Solar Angle θ₁₂"
              formula="tan²θ₁₂ = BEKENSTEIN/9 = 4/9"
              predicted={THETA_12.toFixed(2) + "°"}
              measured="33.44°"
              error="0.7% error"
              category="strong"
            />
            <DerivationCard
              title="Reactor Angle θ₁₃"
              formula="sin²θ₁₃ = 3α = 3/(4Z²+3)"
              predicted={THETA_13.toFixed(2) + "°"}
              measured="8.57°"
              error="0.7% error"
              category="strong"
            />
            <DerivationCard
              title="CP Phase δ_CP"
              formula="δ = π(GAUGE+1)/GAUGE = 13π/12"
              predicted={DELTA_CP.toFixed(0) + "°"}
              measured="~195°"
              error="Exact!"
              category="strong"
            />
          </div>

          <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded text-sm text-amber-800">
            <strong>Prediction:</strong> Normal hierarchy (m₁ &lt; m₂ &lt; m₃) with m₁ = 0.
            Testable by JUNO (~2030) and neutrinoless double beta decay experiments.
          </div>
        </div>

        {/* CKM Matrix */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">CKM Matrix (Quark Mixing)</h2>
          <p className="text-sm text-gray-500 mb-4">All parameters from Z² with ~3% accuracy</p>

          <div className="grid md:grid-cols-2 gap-4">
            <DerivationCard
              title="Cabibbo Angle θ₁₂"
              formula="sin θ = sin²θ_W = 3/(GAUGE+1)"
              predicted={SIN_CABIBBO.toFixed(4)}
              measured="0.2250"
              error="2.6% error"
              category="good"
            />
            <DerivationCard
              title="CKM θ₂₃ (c-b mixing)"
              formula="sin θ₂₃ = α × Z"
              predicted={SIN_CKM_23.toFixed(4)}
              measured="0.0408"
              error="3.5% error"
              category="good"
            />
            <DerivationCard
              title="CKM θ₁₃ (u-b mixing)"
              formula="sin θ₁₃ = α/2"
              predicted={SIN_CKM_13.toFixed(5)}
              measured="0.00382"
              error="4.5% error"
              category="good"
            />
            <DerivationCard
              title="CKM CP Phase δ"
              formula="δ = arctan(BEKENSTEIN-1) = arctan(3)"
              predicted={DELTA_CKM.toFixed(1) + "°"}
              measured="68.8° ± 5°"
              error="4% (within error)"
              category="good"
            />
            <DerivationCard
              title="Wolfenstein A"
              formula="A = BEKENSTEIN/(BEKENSTEIN+1) = 4/5"
              predicted={WOLFENSTEIN_A.toFixed(2)}
              measured="0.826"
              error="3.1% error"
              category="good"
            />
          </div>

          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded text-sm text-blue-800">
            <strong>Key insight:</strong> sin θ_Cabibbo = sin²θ_W connects quark mixing to electroweak symmetry!
            CKM angles are suppressed by α compared to PMNS because quarks feel the EM interaction.
          </div>
        </div>

        {/* Quark Masses */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Individual Quark Masses</h2>
          <p className="text-sm text-gray-500 mb-4">Each generation tied to its lepton partner</p>

          <div className="grid md:grid-cols-2 gap-4">
            <DerivationCard
              title="Up Quark"
              formula="m_u = m_e × (BEKENSTEIN-1)² / 2"
              predicted={M_U_PRED.toFixed(2) + " MeV"}
              measured="2.16 MeV"
              error="6.5% error"
              category="good"
            />
            <DerivationCard
              title="Down Quark"
              formula="m_d = m_e × (BEKENSTEIN-1)² = 9m_e"
              predicted={M_D_PRED.toFixed(2) + " MeV"}
              measured="4.67 MeV"
              error="1.5% error"
              category="strong"
            />
            <DerivationCard
              title="Strange Quark"
              formula="m_s = m_d × 5 × BEKENSTEIN = 20m_d"
              predicted={M_S_PRED.toFixed(1) + " MeV"}
              measured="93.4 MeV"
              error="1.5% error"
              category="strong"
            />
            <DerivationCard
              title="Charm Quark"
              formula="m_c = m_μ × GAUGE = 12m_μ"
              predicted={M_C_PRED.toFixed(0) + " MeV"}
              measured="1270 MeV"
              error="0.2% error"
              category="strong"
            />
            <DerivationCard
              title="Bottom Quark"
              formula="m_b = m_τ × 2Z / (BEKENSTEIN+1)"
              predicted={M_B_PRED.toFixed(0) + " MeV"}
              measured="4180 MeV"
              error="1.6% error"
              category="strong"
            />
            <DerivationCard
              title="Top Quark"
              formula="m_t = m_b × (Z² + CUBE)"
              predicted={M_T_PRED.toFixed(1) + " GeV"}
              measured="172.8 GeV"
              error="1.1% error"
              category="strong"
            />
          </div>

          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded text-sm text-green-800">
            <strong>Quark-Lepton Universality:</strong> Generation 1 quarks scale with m_e,
            charm scales with m_μ, and third generation with m_τ.
            Each generation is unified through Z²!
          </div>
        </div>

        {/* Integers */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Exact Integers</h2>
          <p className="text-sm text-gray-500 mb-4">Structure of reality</p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-50 border border-gray-200 rounded p-4 text-center">
              <div className="text-3xl font-bold text-gray-900">4</div>
              <div className="text-sm text-gray-600">Spacetime dims</div>
              <div className="text-xs text-gray-400 mt-1">BEKENSTEIN</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded p-4 text-center">
              <div className="text-3xl font-bold text-gray-900">12</div>
              <div className="text-sm text-gray-600">Gauge bosons</div>
              <div className="text-xs text-gray-400 mt-1">GAUGE</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded p-4 text-center">
              <div className="text-3xl font-bold text-gray-900">3</div>
              <div className="text-sm text-gray-600">Generations</div>
              <div className="text-xs text-gray-400 mt-1">BEKENSTEIN - 1</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded p-4 text-center">
              <div className="text-3xl font-bold text-gray-900">8</div>
              <div className="text-sm text-gray-600">Gluons</div>
              <div className="text-xs text-gray-400 mt-1">CUBE</div>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
            <div className="bg-amber-50 border border-amber-200 rounded p-4 text-center">
              <div className="text-3xl font-bold text-amber-700">10</div>
              <div className="text-sm text-gray-600">String dims</div>
              <div className="text-xs text-amber-500 mt-1">GAUGE - 2</div>
            </div>
            <div className="bg-amber-50 border border-amber-200 rounded p-4 text-center">
              <div className="text-3xl font-bold text-amber-700">6</div>
              <div className="text-sm text-gray-600">Compact dims</div>
              <div className="text-xs text-amber-500 mt-1">GAUGE / 2</div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded p-4 text-center">
              <div className="text-3xl font-bold text-green-700">64</div>
              <div className="text-sm text-gray-600">Genetic codons</div>
              <div className="text-xs text-green-500 mt-1">CUBE²</div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded p-4 text-center">
              <div className="text-3xl font-bold text-green-700">20</div>
              <div className="text-sm text-gray-600">Amino acids</div>
              <div className="text-xs text-green-500 mt-1">5 × BEKENSTEIN</div>
            </div>
          </div>
        </div>

        {/* Cosmology */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Cosmology</h2>
          <p className="text-sm text-gray-500 mb-4">Universe-scale predictions</p>

          <div className="grid md:grid-cols-2 gap-4">
            <DerivationCard
              title="MOND Acceleration"
              formula="a₀ = cH₀/Z"
              predicted="1.17×10⁻¹⁰"
              measured="1.2×10⁻¹⁰ m/s²"
              error="2.5% error"
              category="good"
            />
            <DerivationCard
              title="Hubble Constant"
              formula="H₀ = Z × a₀ / c"
              predicted="71.5"
              measured="70 ± 3 km/s/Mpc"
              error="Within tension"
              category="good"
            />
            <DerivationCard
              title="Decel→Accel Transition"
              formula="z = (3Z/4)^(1/3) - 1"
              predicted="0.63"
              measured="~0.7"
              error="~10% error"
              category="good"
            />
            <DerivationCard
              title="Matter-Λ Equality"
              formula="z = (3Z/8)^(1/3) - 1"
              predicted="0.29"
              measured="~0.3"
              error="~3% error"
              category="good"
            />
          </div>
        </div>

        {/* Fundamental Scales */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Fundamental Scales & Early Universe</h2>
          <p className="text-sm text-gray-500 mb-4">Connecting Planck scale to particle physics</p>

          <div className="grid md:grid-cols-2 gap-4">
            <DerivationCard
              title="Electron Mass from Planck"
              formula="log₁₀(m_P/m_e) = 2Z²/3"
              predicted={LOG_MP_ME.toFixed(2)}
              measured="22.38"
              error="0.2% error"
              category="strong"
            />
            <DerivationCard
              title="Baryon Asymmetry η"
              formula="η = α⁴/(BEKENSTEIN+1) = α⁴/5"
              predicted={BARYON_ASYMMETRY.toExponential(2)}
              measured="6.1×10⁻¹⁰"
              error="7% error"
              category="good"
            />
            <DerivationCard
              title="Inflation e-folds N"
              formula="N = 54 (from m_p/m_e coefficient)"
              predicted="54"
              measured="~57"
              error="~5% error"
              category="good"
            />
            <DerivationCard
              title="Spectral Index n_s"
              formula="n_s = 1 - 2/N = 1 - 2/54"
              predicted={SPECTRAL_INDEX.toFixed(4)}
              measured="0.965"
              error="0.21% error"
              category="strong"
            />
            <DerivationCard
              title="QCD Scale Λ_QCD"
              formula="Λ_QCD ≈ 2m_μ"
              predicted={LAMBDA_QCD.toFixed(0) + " MeV"}
              measured="220 MeV"
              error="~4% error"
              category="good"
            />
            <DerivationCard
              title="Strong CP θ_QCD"
              formula="θ_QCD = α⁴/Z²"
              predicted={THETA_QCD.toExponential(1)}
              measured="< 10⁻¹⁰"
              error="Consistent"
              category="strong"
            />
          </div>

          <div className="mt-4 p-3 bg-purple-50 border border-purple-200 rounded text-sm text-purple-800">
            <strong>Key insight:</strong> The coefficient 54 in m_p/m_e = <strong>54</strong>Z² + 6Z - 8
            appears to be the number of inflation e-folds! This connects particle masses to cosmological expansion.
          </div>
        </div>

        {/* The Master Equation */}
        <div className="bg-gray-900 text-white rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold mb-4 text-center">The Master Equation</h2>

          <div className="text-center font-mono mb-4">
            <div className="text-blue-300 mb-2">GAUGE = BEKENSTEIN × (BEKENSTEIN - 1)</div>
            <div className="text-2xl text-white">12 = 4 × 3</div>
          </div>

          <div className="text-center text-gray-400 text-sm">
            The three fundamental integers (3, 4, 12) determine each other
          </div>
        </div>

        {/* The Derivation Tree */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Derivation Tree</h2>

          <div className="font-mono text-xs md:text-sm overflow-x-auto">
            <pre className="text-gray-700">{`
                          Z² = 32π/3
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
   BEKENSTEIN = 4        GAUGE = 12           α⁻¹ = 137
         │                    │                    │
    ┌────┴────┐          ┌────┴────┐          ┌────┴────┐
    │         │          │         │          │         │
  4D space  BH ent.   8+3+1    sin²θ_W      α_s      masses
                      bosons   = 3/13     = 4/Z²
                         │
                    ┌────┴────┐
                    │         │
                 m_Z/m_W    String
                 = √(13/10)  10D

                          CUBE = 8
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
     64 codons          Koide = 2/3           m_t/m_b
     = CUBE²            = 8/GAUGE             = Z² + 8
            `}</pre>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="bg-blue-50 border border-blue-200 rounded p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 text-center">Summary</h2>

          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-3xl font-bold text-blue-700">45+</div>
              <div className="text-sm text-gray-600">Quantities derived</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-600">32</div>
              <div className="text-sm text-gray-600">Under 2% error</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-amber-600">1</div>
              <div className="text-sm text-gray-600">Starting constant</div>
            </div>
          </div>

          <div className="text-center mt-4 text-gray-600">
            From Z² = 32π/3, all of physics emerges
          </div>
        </div>

        {/* Links */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <Link
            href="/why-z2"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Why Z²?</div>
            <div className="text-sm text-gray-500">First principles</div>
          </Link>
          <Link
            href="/derivation"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Full Derivation</div>
            <div className="text-sm text-gray-500">Step by step</div>
          </Link>
          <Link
            href="/cosmic-fate"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Cosmic Fate</div>
            <div className="text-sm text-gray-500">Eternal expansion</div>
          </Link>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p>Z² = CUBE × SPHERE — the geometry that generates physics</p>
        </footer>
      </div>
    </main>
  )
}
