'use client'

import { useState } from 'react'
import { Citation, CITATIONS } from './Citation'

// Precise mathematical constants
const PI = Math.PI
const Z = 2 * Math.sqrt(8 * PI / 3)
const Z_SQUARED = Z * Z
const DENOMINATOR = 8 + 3 * Z

// Derived values with high precision
const OMEGA_LAMBDA = (3 * Z) / DENOMINATOR
const OMEGA_MATTER = 8 / DENOMINATOR
const ALPHA_INV = 4 * Z_SQUARED + 3
const ALPHA = 1 / ALPHA_INV

// Physical constants
const c = 299792458  // m/s (exact)
const H0_SI = 2.268e-18  // s⁻¹ (70.0 km/s/Mpc)
const a0_LOCAL = (c * H0_SI) / Z

// Measured values
const PLANCK_OMEGA_LAMBDA = 0.6847
const PLANCK_OMEGA_MATTER = 0.3153
const MEASURED_ALPHA_INV = 137.035999084
const MOND_A0 = 1.2e-10

// E(z) function for redshift evolution
function E(z: number): number {
  return Math.sqrt(OMEGA_MATTER * Math.pow(1 + z, 3) + OMEGA_LAMBDA)
}

interface StepProps {
  number: number
  title: string
  children: React.ReactNode
  delay?: number
}

function Step({ number, title, children, delay = 0 }: StepProps) {
  return (
    <div className="mb-8 p-6 bg-white border border-gray-200 rounded shadow-sm">
      <div className="flex items-center gap-4 mb-4">
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center font-bold text-gray-900 text-sm">
          {number}
        </div>
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      </div>
      <div className="ml-12">{children}</div>
    </div>
  )
}

function MathBlock({ children, highlight = false }: { children: React.ReactNode, highlight?: boolean }) {
  return (
    <div className={`font-mono text-base p-4 rounded my-4 ${
      highlight ? 'bg-blue-50 border border-blue-200' : 'bg-gray-50 border border-gray-200'
    }`}>
      {children}
    </div>
  )
}

function Comparison({ label, predicted, measured, unit = '' }: {
  label: string
  predicted: number | string
  measured: number | string
  unit?: string
}) {
  const pred = typeof predicted === 'number' ? predicted : parseFloat(predicted)
  const meas = typeof measured === 'number' ? measured : parseFloat(measured)
  const error = Math.abs((pred - meas) / meas * 100)

  return (
    <div className="grid grid-cols-3 gap-4 p-3 bg-gray-50 border border-gray-200 rounded text-sm">
      <div className="text-gray-600">{label}</div>
      <div className="text-center">
        <span className="text-gray-900 font-medium">{typeof predicted === 'number' ? predicted.toPrecision(6) : predicted}</span>
        <span className="text-gray-500 ml-1">{unit}</span>
      </div>
      <div className="text-center">
        <span className="text-blue-600">{typeof measured === 'number' ? measured.toPrecision(6) : measured}</span>
        <span className="text-gray-500 ml-1">{unit}</span>
        <span className={`ml-2 text-xs ${error < 0.1 ? 'text-green-600' : 'text-amber-600'}`}>
          ({error.toFixed(3)}%)
        </span>
      </div>
    </div>
  )
}

export default function Derivation() {
  const [showPrecision, setShowPrecision] = useState(false)

  return (
    <div className="w-full min-h-screen bg-[#fafafa] p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 -mx-8 -mt-8 px-8 py-4 mb-8">
          <a href="/" className="text-sm text-blue-600 hover:underline">← Back to Overview</a>
        </header>

        <article className="bg-white border border-gray-200 rounded shadow-sm p-8 mb-8">
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2">
            Mathematical Derivation
          </h1>
          <p className="text-gray-600 mb-4">
            Deriving the MOND acceleration scale from cosmological critical density
          </p>
          <div className="flex items-center gap-4 text-sm text-gray-500 border-t border-gray-200 pt-4">
            <span>Carl Zimmerman</span>
            <span>·</span>
            <a href="https://doi.org/10.5281/zenodo.19199167" className="text-blue-600 hover:underline">
              DOI: 10.5281/zenodo.19199167
            </a>
            <span>·</span>
            <button
              onClick={() => setShowPrecision(!showPrecision)}
              className={`px-3 py-1 rounded text-xs transition-colors ${
                showPrecision
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {showPrecision ? 'High Precision' : 'Show Precision'}
            </button>
          </div>
        </article>

        {/* Step 1: The Geometric Origin */}
        <Step number={1} title="The Geometric Origin" delay={0.1}>
          <p className="text-gray-700 mb-4">
            The Zimmerman constant emerges from the ratio of gravitational geometry (8π from Einstein's field equations)
            to spatial dimensionality (3), with a quantum factor of 2.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">Z</span> = 2 × √(8π / 3)
            </div>
          </MathBlock>
          <div className="grid md:grid-cols-3 gap-4 mt-4 text-sm">
            <div className="p-3 bg-blue-50 border border-blue-100 rounded-lg">
              <div className="text-blue-600 font-bold">8π</div>
              <div className="text-gray-600">Einstein's Gμν = 8πG Tμν</div>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-700 font-bold">3</div>
              <div className="text-gray-600">Spatial dimensions</div>
            </div>
            <div className="p-3 bg-amber-50 border border-amber-100 rounded-lg">
              <div className="text-amber-600 font-bold">2</div>
              <div className="text-gray-600">Quantum amplitude factor</div>
            </div>
          </div>
          <MathBlock>
            <div className="space-y-2 text-sm">
              <div>8π/3 = {(8 * PI / 3).toFixed(showPrecision ? 10 : 6)}</div>
              <div>√(8π/3) = {Math.sqrt(8 * PI / 3).toFixed(showPrecision ? 10 : 6)}</div>
              <div className="text-blue-700 font-bold">Z = {Z.toFixed(showPrecision ? 10 : 6)}</div>
            </div>
          </MathBlock>
        </Step>

        {/* Step 2: The Universal Denominator */}
        <Step number={2} title="The Universal Denominator" delay={0.2}>
          <p className="text-gray-700 mb-4">
            A key structural element appears: the sum of 8 and 3Z. This denominator
            appears in multiple derived quantities.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">D</span> = 8 + 3Z = 8 + 3({Z.toFixed(4)}) = {DENOMINATOR.toFixed(showPrecision ? 10 : 6)}
            </div>
          </MathBlock>
          <p className="text-gray-600 text-sm mt-4">
            This structure suggests a partition: 8 parts matter-like, 3Z parts vacuum-like.
          </p>
        </Step>

        {/* Step 3: Dark Energy Density */}
        <Step number={3} title="Dark Energy Density" delay={0.3}>
          <p className="text-gray-700 mb-4">
            The cosmological constant fraction is the ratio of the vacuum contribution (3Z)
            to the total (8 + 3Z).
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">Ω_Λ</span> = 3Z / (8 + 3Z) = {(3 * Z).toFixed(4)} / {DENOMINATOR.toFixed(4)}
            </div>
          </MathBlock>
          <MathBlock>
            <div className="text-blue-700 text-center text-xl">
              Ω_Λ = {OMEGA_LAMBDA.toFixed(showPrecision ? 10 : 6)}
            </div>
          </MathBlock>
          <div className="mt-4">
            <Comparison
              label="Dark Energy"
              predicted={OMEGA_LAMBDA}
              measured={PLANCK_OMEGA_LAMBDA}
            />
          </div>
        </Step>

        {/* Step 4: Matter Density */}
        <Step number={4} title="Matter Density" delay={0.4}>
          <p className="text-gray-700 mb-4">
            The matter fraction is the remaining portion: 8 out of (8 + 3Z).
            Note that Ω_Λ + Ω_m = 1 by construction — a flat universe.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">Ω_m</span> = 8 / (8 + 3Z) = 8 / {DENOMINATOR.toFixed(4)}
            </div>
          </MathBlock>
          <MathBlock>
            <div className="text-blue-700 text-center text-xl">
              Ω_m = {OMEGA_MATTER.toFixed(showPrecision ? 10 : 6)}
            </div>
          </MathBlock>
          <div className="mt-4">
            <Comparison
              label="Matter"
              predicted={OMEGA_MATTER}
              measured={PLANCK_OMEGA_MATTER}
            />
          </div>
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-sm">
            <span className="text-green-600">Check:</span> Ω_Λ + Ω_m = {(OMEGA_LAMBDA + OMEGA_MATTER).toFixed(10)} ≈ 1.000 ✓
          </div>
        </Step>

        {/* Step 5: Fine Structure Constant */}
        <Step number={5} title="Fine Structure Constant" delay={0.5}>
          <p className="text-gray-700 mb-4">
            The electromagnetic coupling constant emerges from Z² with the same structural element (3).
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">α</span> = 1 / (4Z² + 3)
            </div>
          </MathBlock>
          <MathBlock>
            <div className="space-y-2 text-sm">
              <div>Z² = {Z_SQUARED.toFixed(showPrecision ? 10 : 6)}</div>
              <div>4Z² = {(4 * Z_SQUARED).toFixed(showPrecision ? 10 : 6)}</div>
              <div>4Z² + 3 = {ALPHA_INV.toFixed(showPrecision ? 10 : 6)}</div>
              <div className="text-blue-700 font-bold">1/α = {ALPHA_INV.toFixed(showPrecision ? 10 : 6)}</div>
            </div>
          </MathBlock>
          <div className="mt-4">
            <Comparison
              label="1/α"
              predicted={ALPHA_INV}
              measured={MEASURED_ALPHA_INV}
            />
          </div>
        </Step>

        {/* Step 6: MOND Acceleration */}
        <Step number={6} title="Zimmerman Acceleration Scale" delay={0.6}>
          <p className="text-gray-700 mb-4">
            The characteristic acceleration scale that governs galaxy dynamics is derived from
            fundamental constants divided by Z.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">a₀</span> = c × H₀ / Z
            </div>
          </MathBlock>
          <MathBlock>
            <div className="space-y-2 text-sm">
              <div>c = {c.toExponential(6)} m/s (exact)</div>
              <div>H₀ = {H0_SI.toExponential(4)} s⁻¹ (70 km/s/Mpc)</div>
              <div>c × H₀ = {(c * H0_SI).toExponential(4)} m/s²</div>
              <div className="text-blue-700 font-bold">a₀ = {a0_LOCAL.toExponential(showPrecision ? 6 : 4)} m/s²</div>
            </div>
          </MathBlock>
          <div className="mt-4">
            <Comparison
              label="a₀"
              predicted={`${(a0_LOCAL * 1e10).toFixed(2)}×10⁻¹⁰`}
              measured={`${(MOND_A0 * 1e10).toFixed(1)}×10⁻¹⁰`}
              unit="m/s²"
            />
          </div>
        </Step>

        {/* The Testable Prediction */}
        <div className="mt-12 p-8 bg-blue-50 rounded border border-blue-200">
          <h2 className="text-2xl font-bold text-blue-700 mb-4 text-center">
            The Testable Prediction
          </h2>
          <p className="text-gray-300 mb-6 text-center">
            Unlike constant-a₀ MOND, the Zimmerman framework predicts that a₀ <strong>evolves with redshift</strong>:
          </p>
          <MathBlock highlight>
            <div className="text-center text-xl">
              a₀(z) = a₀(0) × E(z)
              <div className="text-sm text-gray-600 mt-2">
                where E(z) = √(Ω_m(1+z)³ + Ω_Λ)
              </div>
            </div>
          </MathBlock>

          <div className="mt-6 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-600 border-b border-gray-200">
                  <th className="py-2 text-left">Redshift</th>
                  <th className="py-2 text-center">Lookback</th>
                  <th className="py-2 text-center">E(z)</th>
                  <th className="py-2 text-center">a₀(z) / a₀(0)</th>
                </tr>
              </thead>
              <tbody className="text-gray-300">
                {[0, 0.5, 0.87, 1, 2, 5, 10].map((z) => (
                  <tr key={z} className="border-b border-gray-800">
                    <td className="py-2">z = {z}</td>
                    <td className="py-2 text-center text-gray-600">
                      {z === 0 ? 'Now' : z === 0.87 ? 'El Gordo' : `${(13.8 * (1 - 1/Math.pow(1+z, 1.5))).toFixed(1)} Gyr`}
                    </td>
                    <td className="py-2 text-center text-blue-700">{E(z).toFixed(3)}</td>
                    <td className="py-2 text-center text-amber-600">{E(z).toFixed(2)}×</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <p className="text-gray-600 text-sm mt-6 text-center">
            This prediction is <strong className="text-green-600">falsifiable</strong> by JWST observations of high-redshift galaxy kinematics.
          </p>
        </div>

        {/* Step 7: The Radial Acceleration Relation (RAR) */}
        <Step number={7} title="The Radial Acceleration Relation" delay={0.7}>
          <p className="text-gray-700 mb-4">
            The RAR connects observed gravitational acceleration to baryonic acceleration.
            This interpolation function emerges naturally from the Zimmerman framework.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">g_obs</span> = g_bar / (1 - e^(-√(g_bar/a₀)))
            </div>
          </MathBlock>
          <p className="text-gray-600 text-sm mt-4 mb-4">
            In the Zimmerman framework, a₀ sets the transition scale between Newtonian and
            modified dynamics. The key insight is that a₀ evolves with cosmic time:
          </p>
          <MathBlock>
            <div className="space-y-2 text-sm">
              <div><span className="text-gray-600">Newtonian limit (g_bar ≫ a₀):</span> g_obs ≈ g_bar</div>
              <div><span className="text-gray-600">Deep MOND limit (g_bar ≪ a₀):</span> g_obs ≈ √(g_bar × a₀)</div>
              <div className="text-blue-700 font-bold mt-2">Transition at: g = a₀ = cH₀/Z = 1.2 × 10⁻¹⁰ m/s²</div>
            </div>
          </MathBlock>
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-sm">
            <span className="text-green-600">Confirmed:</span> 2,693 data points from 153 SPARC galaxies
            follow this relation with scatter &lt; 0.13 dex (McGaugh et al. 2016)
          </div>
        </Step>

        {/* Step 8: Baryonic Tully-Fisher Relation */}
        <Step number={8} title="Baryonic Tully-Fisher Relation" delay={0.8}>
          <p className="text-gray-700 mb-4">
            In the deep MOND regime, the RAR implies a precise relationship between
            baryonic mass and rotation velocity — the BTFR with slope exactly 4.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">M_bar</span> = V⁴ / (G × a₀)
            </div>
          </MathBlock>
          <MathBlock>
            <div className="space-y-2 text-sm">
              <div><span className="text-gray-600">Taking log:</span> log(M_bar) = 4 × log(V) - log(G × a₀)</div>
              <div><span className="text-gray-600">Slope:</span> <span className="text-blue-700">d log M / d log V = 4</span> (exact)</div>
              <div className="mt-2 text-gray-600">At redshift z, the relation shifts:</div>
              <div className="text-amber-600 font-bold">Δlog M_bar(z) = -log₁₀(E(z))</div>
            </div>
          </MathBlock>
          <div className="mt-4 p-3 bg-blue-50 border border-blue-100 rounded-lg text-sm">
            <span className="text-blue-600">Zimmerman Prediction:</span> At z = 2, the BTFR offset should be
            <span className="text-amber-600 font-mono"> Δlog M = -{Math.log10(E(2)).toFixed(2)} dex</span>
            — testable with KMOS3D and JWST data.
          </div>
        </Step>

        {/* Step 9: Hubble Tension Resolution */}
        <Step number={9} title="Hubble Tension Resolution" delay={0.9}>
          <p className="text-gray-700 mb-4">
            The Zimmerman framework provides an independent route to H₀ through the
            MOND acceleration scale, landing between CMB and local measurements.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">H₀</span> = Z × a₀ / c = (Z × 1.2 × 10⁻¹⁰) / c
            </div>
          </MathBlock>
          <MathBlock>
            <div className="space-y-2 text-sm">
              <div>Z = {Z.toFixed(6)}</div>
              <div>a₀ = 1.2 × 10⁻¹⁰ m/s² (McGaugh+ 2016)</div>
              <div>c = 299,792,458 m/s</div>
              <div className="mt-2 border-t border-gray-200 pt-2">
                <span className="text-blue-700 font-bold">H₀ = {((Z * 1.2e-10 / c) * 3.086e19).toFixed(1)} km/s/Mpc</span>
              </div>
            </div>
          </MathBlock>
          <div className="mt-4 grid grid-cols-3 gap-2 text-sm">
            <div className="p-2 bg-blue-50 border border-blue-200 rounded text-center">
              <div className="text-blue-600 font-bold">67.4</div>
              <div className="text-gray-500 text-xs">Planck CMB</div>
            </div>
            <div className="p-2 bg-blue-100 rounded text-center border border-blue-300">
              <div className="text-blue-700 font-bold">71.5</div>
              <div className="text-gray-600 text-xs">Zimmerman</div>
            </div>
            <div className="p-2 bg-red-50 border border-red-200 rounded text-center">
              <div className="text-red-600 font-bold">73.0</div>
              <div className="text-gray-500 text-xs">SH0ES local</div>
            </div>
          </div>
          <p className="text-gray-600 text-sm mt-4">
            The Zimmerman H₀ falls naturally between early- and late-universe measurements,
            suggesting the "tension" reflects evolving physics rather than systematic errors.
          </p>
        </Step>

        {/* Step 10: Structure Formation Enhancement */}
        <Step number={10} title="Structure Formation at High Redshift" delay={1.0}>
          <p className="text-gray-700 mb-4">
            At high redshift, the enhanced a₀ produces stronger effective gravity,
            allowing structure to form faster than in standard ΛCDM.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">g_eff(z)</span> = g_bar × [1 + (a₀(z)/g_bar)^n]^(1/n)
            </div>
          </MathBlock>
          <MathBlock>
            <div className="space-y-2 text-sm">
              <div><span className="text-gray-600">At z = 0.87 (El Gordo):</span> a₀ = 1.66 × a₀(0)</div>
              <div><span className="text-gray-600">At z = 10 (JWST early galaxies):</span> a₀ = 20 × a₀(0)</div>
              <div className="mt-2 text-amber-600">This resolves:</div>
              <div className="text-gray-300">• El Gordo 6σ tension</div>
              <div className="text-gray-300">• JWST "impossible" early massive galaxies</div>
              <div className="text-gray-300">• S8 structure growth tension</div>
            </div>
          </MathBlock>
        </Step>

        {/* Summary Box */}
        <div className="mt-12 p-6 bg-white rounded border border-gray-200">
          <h3 className="text-lg font-bold text-blue-600 mb-4 text-center">Summary of Predictions</h3>
          <div className="space-y-2">
            <Comparison label="Ω_Λ (Dark Energy)" predicted={OMEGA_LAMBDA} measured={PLANCK_OMEGA_LAMBDA} />
            <Comparison label="Ω_m (Matter)" predicted={OMEGA_MATTER} measured={PLANCK_OMEGA_MATTER} />
            <Comparison label="1/α (Fine Structure)" predicted={ALPHA_INV} measured={MEASURED_ALPHA_INV} />
          </div>
          <div className="mt-6 text-center text-sm text-gray-600">
            All derived from a single constant: <span className="text-blue-700 font-mono">Z = 2√(8π/3) = {Z.toFixed(6)}</span>
          </div>
        </div>

        {/* Step 11: Galaxy Size Evolution */}
        <Step number={11} title="Galaxy Size Evolution" delay={1.1}>
          <p className="text-gray-700 mb-4">
            The <strong>MOND radius</strong> — where dynamics transition from Newtonian to modified —
            depends on a₀. As a₀ evolves, so does the characteristic size of galaxies.
          </p>
          <MathBlock highlight>
            <div className="text-center">
              <span className="text-blue-600">r_M</span> = √(GM / a₀) — MOND transition radius
            </div>
          </MathBlock>
          <MathBlock>
            <div className="space-y-2 text-sm">
              <div><span className="text-gray-600">At the MOND radius:</span> g_bar = GM/r² = a₀</div>
              <div><span className="text-gray-600">Solving for r:</span> r_M = √(GM/a₀)</div>
              <div className="mt-2 text-amber-600">At redshift z:</div>
              <div className="text-blue-700 font-bold">r_M(z) = r_M(0) / √E(z)</div>
            </div>
          </MathBlock>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-600 border-b border-gray-200">
                  <th className="py-2 text-left">Redshift</th>
                  <th className="py-2 text-center">E(z)</th>
                  <th className="py-2 text-center">r_M(z) / r_M(0)</th>
                  <th className="py-2 text-center">Size Reduction</th>
                </tr>
              </thead>
              <tbody className="text-gray-300">
                {[0, 1, 2, 3, 5, 10].map((z) => {
                  const Ez = E(z)
                  const ratio = 1 / Math.sqrt(Ez)
                  const reduction = (1 - ratio) * 100
                  return (
                    <tr key={z} className="border-b border-gray-800">
                      <td className="py-2">z = {z}</td>
                      <td className="py-2 text-center text-blue-700">{Ez.toFixed(2)}</td>
                      <td className="py-2 text-center text-amber-600">{ratio.toFixed(2)}×</td>
                      <td className="py-2 text-center text-blue-600">{reduction > 0 ? `-${reduction.toFixed(0)}%` : '—'}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg text-sm">
            <span className="text-green-600">JWST Confirmation:</span> High-z galaxies are observed to be
            significantly more compact than local galaxies at the same mass. The Zimmerman framework
            <strong className="text-blue-700"> predicts this naturally</strong> — as a₀ increases, the MOND
            radius shrinks, making galaxies appear smaller.
          </div>
          <div className="mt-4 p-3 bg-blue-50 border border-blue-100 rounded-lg text-sm">
            <span className="text-blue-600">Additional Predictions:</span>
            <ul className="mt-2 space-y-1 text-gray-300">
              <li>• The mass-size relation should steepen at high z</li>
              <li>• Disk scale heights should be smaller at high z</li>
              <li>• The "half-light radius" evolution traces E(z)^(-1/2)</li>
              <li>• Bulge-to-disk ratios may differ due to modified dynamics</li>
            </ul>
          </div>
        </Step>

        {/* Key Equations Reference */}
        <div className="mt-12 p-6 bg-gray-50 rounded border border-gray-200">
          <h3 className="text-lg font-bold text-gray-900 mb-4 text-center">Key Equations at a Glance</h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm font-mono">
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-600 mb-1">Zimmerman Constant</div>
              <div className="text-gray-900">Z = 2√(8π/3) = 5.788810</div>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-600 mb-1">Dark Energy</div>
              <div className="text-gray-900">Ω_Λ = 3Z/(8+3Z) = 0.6856</div>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-600 mb-1">Matter Density</div>
              <div className="text-gray-900">Ω_m = 8/(8+3Z) = 0.3144</div>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-600 mb-1">Fine Structure</div>
              <div className="text-gray-900">α = 1/(4Z²+3) = 1/137.04</div>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-600 mb-1">Acceleration Scale</div>
              <div className="text-gray-900">a₀ = cH₀/Z = 1.2×10⁻¹⁰ m/s²</div>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-600 mb-1">Redshift Evolution</div>
              <div className="text-gray-900">a₀(z) = a₀(0) × E(z)</div>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-600 mb-1">RAR Interpolation</div>
              <div className="text-gray-900">g_obs = g_bar/(1-e^(-√(g_bar/a₀)))</div>
            </div>
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
              <div className="text-blue-600 mb-1">BTFR</div>
              <div className="text-gray-900">M_bar = V⁴/(G × a₀)</div>
            </div>
          </div>
        </div>

        {/* Academic Citations */}
        <Citation
          citations={[
            CITATIONS.RAR,
            CITATIONS.SPARC,
            CITATIONS.PLANCK_2018,
            CITATIONS.CODATA_2018,
            {
              authors: 'Milgrom, M.',
              year: 1983,
              title: 'A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis',
              journal: 'The Astrophysical Journal',
              volume: '270',
              pages: '365',
              doi: '10.1086/161130',
              description: 'Original MOND proposal'
            },
          ]}
        />

        {/* Back link */}
        <div className="mt-12 text-center py-8 border-t border-gray-200">
          <a
            href="/"
            className="text-blue-600 hover:underline"
          >
            ← Back to Overview
          </a>
        </div>
      </div>
    </div>
  )
}
