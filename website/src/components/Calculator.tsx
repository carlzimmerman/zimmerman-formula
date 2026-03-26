'use client'

import { motion } from 'framer-motion'
import { useState, useMemo } from 'react'
import { Citation, CITATIONS } from './Citation'

// Precise constants (CODATA 2018)
const PI = Math.PI
const Z = 2 * Math.sqrt(8 * PI / 3)  // 5.788810...
const c = 299792458  // m/s (exact, SI definition)
const G = 6.67430e-11  // m³/kg/s² (CODATA 2018, ±0.00015)
const M_sun = 1.98892e30  // kg (IAU 2015)
const kpc_to_m = 3.08567758e19  // m (IAU 2015)
const Mpc_to_m = 3.08567758e22  // m (IAU 2015)

// Cosmological parameters derived from Z (compare with Planck 2018)
const OMEGA_M = 8 / (8 + 3 * Z)  // 0.31537 (Planck: 0.315 ± 0.007)
const OMEGA_LAMBDA = 3 * Z / (8 + 3 * Z)  // 0.68463 (Planck: 0.685 ± 0.007)

// Default H₀ (can be varied)
const H0_default = 70  // km/s/Mpc

function E(z: number): number {
  return Math.sqrt(OMEGA_M * Math.pow(1 + z, 3) + OMEGA_LAMBDA)
}

function a0(H0_kmsMpc: number): number {
  const H0_SI = H0_kmsMpc * 1000 / Mpc_to_m  // Convert to s⁻¹
  return c * H0_SI / Z
}

function cosmicTime(z: number, H0: number): number {
  // Approximate lookback time in Gyr
  const H0_SI = H0 * 1000 / Mpc_to_m
  const tH = 1 / H0_SI / (365.25 * 24 * 3600 * 1e9)  // Hubble time in Gyr
  if (z === 0) return 0
  // Integration approximation
  let t = 0
  const dz = 0.01
  for (let zp = 0; zp < z; zp += dz) {
    t += dz / ((1 + zp) * E(zp))
  }
  return t * tH
}

interface CalculatorMode {
  id: string
  name: string
  description: string
  color: string
}

const MODES: CalculatorMode[] = [
  { id: 'redshift', name: 'Redshift → a₀', description: 'Calculate acceleration scale at any redshift', color: 'cyan' },
  { id: 'galaxy', name: 'Galaxy Dynamics', description: 'Predict rotation velocity from mass', color: 'purple' },
  { id: 'hubble', name: 'Hubble from a₀', description: 'Derive H₀ from acceleration measurement', color: 'green' },
  { id: 'btfr', name: 'BTFR Offset', description: 'Baryonic Tully-Fisher shift at redshift', color: 'orange' },
]

export default function Calculator() {
  const [mode, setMode] = useState('redshift')
  const [H0, setH0] = useState(H0_default)

  // Mode-specific inputs
  const [redshift, setRedshift] = useState(0)
  const [galaxyMass, setGalaxyMass] = useState(1e11)  // Solar masses
  const [radius, setRadius] = useState(10)  // kpc
  const [measuredA0, setMeasuredA0] = useState(1.2e-10)

  // Calculations
  const results = useMemo(() => {
    const a0_local = a0(H0)
    const a0_z = a0_local * E(redshift)

    switch (mode) {
      case 'redshift': {
        return {
          a0_local,
          E_z: E(redshift),
          a0_z,
          lookback: cosmicTime(redshift, H0),
          btfr_offset: -Math.log10(E(redshift)),
        }
      }

      case 'galaxy': {
        const M_kg = galaxyMass * M_sun
        const r_m = radius * kpc_to_m

        // Newtonian velocity
        const v_newton = Math.sqrt(G * M_kg / r_m)

        // Zimmerman/MOND velocity (deep MOND regime)
        const g_N = G * M_kg / (r_m * r_m)
        const v_zimmerman = Math.pow(G * M_kg * a0_z, 0.25) * Math.sqrt(r_m / Math.sqrt(r_m * r_m))
        // More accurate: interpolating function
        const mu = g_N / (g_N + a0_z)
        const v_mond = Math.sqrt(g_N * r_m / mu)

        return {
          v_newton: v_newton / 1000,  // km/s
          v_zimmerman: v_mond / 1000,
          g_newton: g_N,
          g_mond: g_N / mu,
          ratio: v_mond / v_newton,
        }
      }

      case 'hubble': {
        // H₀ = Z × a₀ / c
        const H0_derived_SI = Z * measuredA0 / c
        const H0_derived = H0_derived_SI * Mpc_to_m / 1000  // km/s/Mpc

        return {
          H0_derived,
          planck_tension: Math.abs(H0_derived - 67.4),
          shoes_tension: Math.abs(H0_derived - 73.0),
        }
      }

      case 'btfr': {
        const offset = -Math.log10(E(redshift))
        return {
          E_z: E(redshift),
          offset_dex: offset,
          mass_factor: Math.pow(10, offset),
        }
      }

      default:
        return {}
    }
  }, [mode, H0, redshift, galaxyMass, radius, measuredA0])

  return (
    <div className="w-full min-h-screen bg-gradient-to-b from-black via-gray-950 to-black p-4 md:p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent mb-4">
            Zimmerman Calculator
          </h1>
          <p className="text-xl text-gray-400">
            Interactive predictions from Z = 2√(8π/3)
          </p>
        </div>

        {/* Mode selector */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
          {MODES.map((m) => (
            <button
              key={m.id}
              onClick={() => setMode(m.id)}
              className={`p-4 rounded-xl border transition-all text-left ${
                mode === m.id
                  ? `bg-${m.color}-900/30 border-${m.color}-500/60`
                  : 'bg-gray-900/30 border-gray-700 hover:border-gray-500'
              }`}
              style={{
                backgroundColor: mode === m.id ? `var(--${m.color}-900, #1a1a2e)` : undefined,
                borderColor: mode === m.id ? `var(--${m.color}-500, #00bcd4)` : undefined,
              }}
            >
              <div className={`font-bold text-sm ${mode === m.id ? `text-${m.color}-400` : 'text-white'}`}
                   style={{ color: mode === m.id ? `var(--${m.color}-400, #00ffff)` : undefined }}>
                {m.name}
              </div>
              <div className="text-xs text-gray-500 mt-1">{m.description}</div>
            </button>
          ))}
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Inputs */}
          <div className="p-6 bg-gray-900/50 rounded-2xl border border-gray-700">
            <h2 className="text-lg font-bold text-white mb-6">Inputs</h2>

            {/* Global H₀ input */}
            <div className="mb-6 p-4 bg-black/30 rounded-xl">
              <label className="block text-sm text-gray-400 mb-2">
                H₀ (km/s/Mpc)
              </label>
              <input
                type="number"
                value={H0}
                onChange={(e) => setH0(parseFloat(e.target.value) || 70)}
                className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-600"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-2">
                <button onClick={() => setH0(67.4)} className="hover:text-cyan-400">Planck: 67.4</button>
                <button onClick={() => setH0(70)} className="hover:text-cyan-400">Default: 70</button>
                <button onClick={() => setH0(73)} className="hover:text-cyan-400">SH0ES: 73</button>
              </div>
            </div>

            {/* Mode-specific inputs */}
            {mode === 'redshift' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Redshift (z)
                  </label>
                  <input
                    type="number"
                    value={redshift}
                    onChange={(e) => setRedshift(parseFloat(e.target.value) || 0)}
                    min={0}
                    max={1100}
                    step={0.1}
                    className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-600"
                  />
                  <input
                    type="range"
                    value={redshift}
                    onChange={(e) => setRedshift(parseFloat(e.target.value))}
                    min={0}
                    max={20}
                    step={0.1}
                    className="w-full mt-2 accent-cyan-500"
                  />
                </div>
                <div className="grid grid-cols-4 gap-2">
                  {[0, 0.87, 2, 10].map(z => (
                    <button
                      key={z}
                      onClick={() => setRedshift(z)}
                      className="px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded text-sm text-gray-300"
                    >
                      z={z}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {mode === 'galaxy' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Baryonic Mass (M☉)
                  </label>
                  <input
                    type="number"
                    value={galaxyMass}
                    onChange={(e) => setGalaxyMass(parseFloat(e.target.value) || 1e10)}
                    className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-600"
                  />
                  <div className="text-xs text-gray-500 mt-1">
                    {galaxyMass.toExponential(2)} solar masses
                  </div>
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Radius (kpc)
                  </label>
                  <input
                    type="number"
                    value={radius}
                    onChange={(e) => setRadius(parseFloat(e.target.value) || 1)}
                    min={0.1}
                    max={100}
                    step={0.1}
                    className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-600"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Redshift (for a₀ evolution)
                  </label>
                  <input
                    type="number"
                    value={redshift}
                    onChange={(e) => setRedshift(parseFloat(e.target.value) || 0)}
                    min={0}
                    max={20}
                    step={0.1}
                    className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-600"
                  />
                </div>
              </div>
            )}

            {mode === 'hubble' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Measured a₀ (m/s²)
                  </label>
                  <input
                    type="number"
                    value={measuredA0}
                    onChange={(e) => setMeasuredA0(parseFloat(e.target.value) || 1.2e-10)}
                    step="1e-11"
                    className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-600"
                  />
                  <div className="text-xs text-gray-500 mt-1">
                    Empirical value: ~1.2 × 10⁻¹⁰ m/s²
                  </div>
                </div>
              </div>
            )}

            {mode === 'btfr' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">
                    Redshift (z)
                  </label>
                  <input
                    type="number"
                    value={redshift}
                    onChange={(e) => setRedshift(parseFloat(e.target.value) || 0)}
                    min={0}
                    max={20}
                    step={0.1}
                    className="w-full bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-600"
                  />
                  <input
                    type="range"
                    value={redshift}
                    onChange={(e) => setRedshift(parseFloat(e.target.value))}
                    min={0}
                    max={10}
                    step={0.1}
                    className="w-full mt-2 accent-orange-500"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Results */}
          <div className="p-6 bg-gradient-to-br from-gray-900/50 to-gray-900/30 rounded-2xl border border-cyan-500/30">
            <h2 className="text-lg font-bold text-cyan-400 mb-6">Results</h2>

            {mode === 'redshift' && results.a0_local && (
              <div className="space-y-4">
                <ResultRow label="a₀ (local)" value={`${(results.a0_local * 1e10).toFixed(4)} × 10⁻¹⁰ m/s²`} />
                <ResultRow label="E(z)" value={results.E_z.toFixed(4)} highlight />
                <ResultRow label={`a₀ at z=${redshift}`} value={`${(results.a0_z * 1e10).toFixed(4)} × 10⁻¹⁰ m/s²`} highlight />
                <ResultRow label="Lookback time" value={`${results.lookback.toFixed(2)} Gyr`} />
                <ResultRow label="BTFR offset" value={`${results.btfr_offset.toFixed(3)} dex`} />
              </div>
            )}

            {mode === 'galaxy' && results.v_newton && (
              <div className="space-y-4">
                <ResultRow label="v (Newton)" value={`${results.v_newton.toFixed(1)} km/s`} />
                <ResultRow label="v (Zimmerman)" value={`${results.v_zimmerman.toFixed(1)} km/s`} highlight />
                <ResultRow label="Boost factor" value={`${results.ratio.toFixed(2)}×`} highlight />
                <ResultRow label="g_N" value={`${results.g_newton.toExponential(2)} m/s²`} />
                <ResultRow label="g_obs (predicted)" value={`${results.g_mond.toExponential(2)} m/s²`} />
              </div>
            )}

            {mode === 'hubble' && results.H0_derived && (
              <div className="space-y-4">
                <ResultRow label="H₀ (derived)" value={`${results.H0_derived.toFixed(2)} km/s/Mpc`} highlight />
                <ResultRow label="vs Planck (67.4)" value={`${results.planck_tension.toFixed(2)} km/s/Mpc`} />
                <ResultRow label="vs SH0ES (73.0)" value={`${results.shoes_tension.toFixed(2)} km/s/Mpc`} />
                <div className="mt-4 p-3 bg-green-900/20 rounded-lg text-sm text-green-300">
                  Zimmerman predicts H₀ ≈ 71.5 from a₀ — between Planck and SH0ES!
                </div>
              </div>
            )}

            {mode === 'btfr' && results.E_z !== undefined && results.offset_dex !== undefined && results.mass_factor !== undefined && (
              <div className="space-y-4">
                <ResultRow label="E(z)" value={results.E_z.toFixed(4)} />
                <ResultRow label="Log offset" value={`${results.offset_dex.toFixed(3)} dex`} highlight />
                <ResultRow label="Mass factor" value={`${results.mass_factor.toFixed(3)}×`} highlight />
                <div className="mt-4 p-3 bg-orange-900/20 rounded-lg text-sm text-orange-300">
                  At z={redshift.toFixed(1)}, galaxies appear {(1/results.mass_factor).toFixed(2)}× less massive at fixed v
                </div>
              </div>
            )}

            {/* Formula reference */}
            <div className="mt-6 p-4 bg-black/40 rounded-xl text-center">
              <div className="font-mono text-sm text-purple-300">
                Z = 2√(8π/3) = {Z.toFixed(6)}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                a₀ = cH₀/Z | E(z) = √(Ωm(1+z)³ + ΩΛ)
              </div>
            </div>
          </div>
        </div>

        {/* Academic Citations */}
        <Citation
          compact
          citations={[
            CITATIONS.PLANCK_2018,
            CITATIONS.SHOES_2022,
            CITATIONS.CODATA_2018,
            CITATIONS.RAR,
          ]}
        />

        {/* Back link */}
        <div className="mt-8 text-center">
          <a href="/" className="text-purple-400 hover:text-purple-300 transition-colors">
            ← Back to Home
          </a>
        </div>
      </motion.div>
    </div>
  )
}

function ResultRow({ label, value, highlight = false }: { label: string, value: string, highlight?: boolean }) {
  return (
    <div className={`flex justify-between items-center p-3 rounded-lg ${highlight ? 'bg-cyan-900/20' : 'bg-black/20'}`}>
      <span className="text-gray-400">{label}</span>
      <span className={`font-mono ${highlight ? 'text-cyan-400 font-bold' : 'text-white'}`}>{value}</span>
    </div>
  )
}
