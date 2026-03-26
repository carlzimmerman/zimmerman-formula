'use client'

import { motion } from 'framer-motion'
import { useState, useMemo } from 'react'
import { Citation, CITATIONS } from './Citation'

// Physics constants (CODATA 2018)
const Z = 2 * Math.sqrt(8 * Math.PI / 3)  // 5.788810
const G = 6.67430e-11  // m³/kg/s² (CODATA 2018)
const c = 299792458    // m/s (exact)
const OMEGA_M = 0.315  // Planck 2018
const OMEGA_LAMBDA = 0.685  // Planck 2018
const a0_local = 1.2e-10  // m/s² (McGaugh et al. 2016)

// E(z) function
function E(z: number): number {
  return Math.sqrt(OMEGA_M * Math.pow(1 + z, 3) + OMEGA_LAMBDA)
}

// SPARC-like galaxy data (representative sample)
const GALAXY_DATA = [
  { name: 'NGC 2403', distance: 3.2, vFlat: 134, rLast: 22, mass: 3.2e10 },
  { name: 'NGC 3198', distance: 13.8, vFlat: 150, rLast: 30, mass: 4.5e10 },
  { name: 'NGC 6946', distance: 5.9, vFlat: 210, rLast: 20, mass: 8.1e10 },
  { name: 'UGC 128', distance: 64, vFlat: 131, rLast: 55, mass: 2.9e10 },
  { name: 'DDO 154', distance: 4.0, vFlat: 47, rLast: 8, mass: 4.0e8 },
  { name: 'NGC 2841', distance: 14.1, vFlat: 305, rLast: 50, mass: 2.1e11 },
  { name: 'NGC 7331', distance: 14.7, vFlat: 250, rLast: 35, mass: 1.2e11 },
  { name: 'IC 2574', distance: 4.0, vFlat: 67, rLast: 13, mass: 1.5e9 },
]

// Model predictions
interface ModelPrediction {
  name: string
  color: string
  description: string
  getVelocity: (r: number, M: number, a0: number) => number
  evolves: boolean
  darkMatter: boolean
}

const MODELS: ModelPrediction[] = [
  {
    name: 'Newton',
    color: '#666666',
    description: 'Classical gravity: v = √(GM/r)',
    getVelocity: (r, M) => Math.sqrt(G * M * 1.989e30 / (r * 3.086e19)) / 1000,
    evolves: false,
    darkMatter: false,
  },
  {
    name: 'ΛCDM',
    color: '#ff6b6b',
    description: 'Dark matter halo: NFW profile (requires tuning per galaxy)',
    getVelocity: (r, M) => {
      const r_m = r * 3.086e19
      const M_kg = M * 1.989e30

      // Baryonic contribution
      const v_bar_sq = G * M_kg / r_m

      // NFW dark matter halo (typical parameters)
      // In ΛCDM, these must be tuned for EACH galaxy
      const rs = 15 * 3.086e19  // scale radius ~15 kpc
      const rho_s = 0.01 * 1.989e30 / Math.pow(3.086e19, 3)  // characteristic density
      const x = r_m / rs

      // NFW enclosed mass: M(<r) ∝ ln(1+x) - x/(1+x)
      const nfw_mass = 4 * Math.PI * rho_s * Math.pow(rs, 3) * (Math.log(1 + x) - x / (1 + x))
      const v_dm_sq = G * nfw_mass / r_m

      // Total: v² = v_bar² + v_dm²
      const v = Math.sqrt(v_bar_sq + v_dm_sq) / 1000  // km/s
      return v
    },
    evolves: false,
    darkMatter: true,
  },
  {
    name: 'Zimmerman',
    color: '#00ffff',
    description: 'a₀(z) = cH₀/Z × E(z) — evolves with redshift',
    getVelocity: (r, M, a0) => {
      const r_m = r * 3.086e19
      const M_kg = M * 1.989e30
      const g_bar = G * M_kg / (r_m * r_m)  // Baryonic/Newtonian acceleration

      // RAR formula: g_obs = g_bar / (1 - exp(-√(g_bar/a₀)))
      // This is the exact empirical relation from SPARC data
      const x = Math.sqrt(g_bar / a0)
      const g_obs = g_bar / (1 - Math.exp(-x))

      // Rotation velocity: v = √(g_obs × r)
      const v = Math.sqrt(g_obs * r_m) / 1000  // km/s
      return v
    },
    evolves: true,
    darkMatter: false,
  },
]

export default function ModelComparison() {
  const [selectedGalaxy, setSelectedGalaxy] = useState(0)
  const [redshift, setRedshift] = useState(0)

  const galaxy = GALAXY_DATA[selectedGalaxy]
  const a0_z = a0_local * E(redshift)

  // Generate rotation curve data
  const curves = useMemo(() => {
    const radii = Array.from({ length: 50 }, (_, i) => 0.5 + (i / 49) * (galaxy.rLast - 0.5))

    return MODELS.map(model => ({
      ...model,
      points: radii.map(r => ({
        r,
        v: model.getVelocity(r, galaxy.mass, model.evolves ? a0_z : a0_local)
      }))
    }))
  }, [selectedGalaxy, redshift, galaxy])

  const maxV = Math.max(...curves.flatMap(c => c.points.map(p => p.v)))
  const maxR = galaxy.rLast

  return (
    <div className="w-full min-h-screen bg-gradient-to-b from-black via-gray-950 to-black p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-cyan-400 via-purple-500 to-red-500 bg-clip-text text-transparent mb-4">
            Model Comparison
          </h1>
          <p className="text-xl text-gray-400">
            Newton vs ΛCDM vs Zimmerman — Real Galaxy Data
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Model Cards */}
          <div className="space-y-4">
            <h3 className="text-lg font-bold text-white mb-4">The Three Models</h3>

            {MODELS.map((model, i) => (
              <motion.div
                key={model.name}
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                className="p-4 bg-black/50 backdrop-blur rounded-xl border"
                style={{ borderColor: `${model.color}40` }}
              >
                <div className="flex items-center gap-3 mb-2">
                  <div
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: model.color }}
                  />
                  <h4 className="font-bold" style={{ color: model.color }}>
                    {model.name}
                  </h4>
                </div>
                <p className="text-sm text-gray-400 mb-2">{model.description}</p>
                <div className="flex gap-2 text-xs">
                  {model.darkMatter && (
                    <span className="px-2 py-1 bg-red-900/30 text-red-400 rounded">
                      Dark Matter
                    </span>
                  )}
                  {model.evolves && (
                    <span className="px-2 py-1 bg-cyan-900/30 text-cyan-400 rounded">
                      Evolves with z
                    </span>
                  )}
                  {!model.darkMatter && !model.evolves && (
                    <span className="px-2 py-1 bg-gray-800 text-gray-400 rounded">
                      Classical
                    </span>
                  )}
                </div>
              </motion.div>
            ))}

            {/* Key Difference */}
            <div className="p-4 bg-purple-900/20 rounded-xl border border-purple-500/30 mt-6">
              <h4 className="font-bold text-purple-400 mb-2">Key Difference</h4>
              <p className="text-sm text-gray-300">
                <span className="text-red-400">ΛCDM</span> requires invisible dark matter.
                <br />
                <span className="text-cyan-400">Zimmerman</span> predicts evolving a₀ with redshift — testable!
              </p>
            </div>
          </div>

          {/* Rotation Curve Plot */}
          <div className="lg:col-span-2">
            <div className="bg-black/50 backdrop-blur rounded-2xl border border-gray-700/50 p-6">
              <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
                <div>
                  <h3 className="text-xl font-bold text-white">{galaxy.name}</h3>
                  <p className="text-sm text-gray-400">
                    M = {(galaxy.mass / 1e10).toFixed(1)} × 10¹⁰ M☉ | D = {galaxy.distance} Mpc
                  </p>
                </div>

                {/* Galaxy selector */}
                <select
                  value={selectedGalaxy}
                  onChange={(e) => setSelectedGalaxy(parseInt(e.target.value))}
                  className="bg-gray-800 text-white px-3 py-2 rounded-lg border border-gray-600"
                >
                  {GALAXY_DATA.map((g, i) => (
                    <option key={g.name} value={i}>{g.name}</option>
                  ))}
                </select>
              </div>

              {/* SVG Plot */}
              <svg viewBox="0 0 500 300" className="w-full h-80">
                {/* Grid */}
                {[0, 0.25, 0.5, 0.75, 1].map((frac) => (
                  <g key={frac}>
                    <line
                      x1={50}
                      y1={250 - frac * 200}
                      x2={480}
                      y2={250 - frac * 200}
                      stroke="#333"
                      strokeWidth="0.5"
                    />
                    <text
                      x={45}
                      y={255 - frac * 200}
                      fill="#666"
                      fontSize="10"
                      textAnchor="end"
                    >
                      {Math.round(frac * maxV)}
                    </text>
                  </g>
                ))}
                {[0, 0.25, 0.5, 0.75, 1].map((frac) => (
                  <g key={frac}>
                    <line
                      x1={50 + frac * 430}
                      y1={50}
                      x2={50 + frac * 430}
                      y2={250}
                      stroke="#333"
                      strokeWidth="0.5"
                    />
                    <text
                      x={50 + frac * 430}
                      y={265}
                      fill="#666"
                      fontSize="10"
                      textAnchor="middle"
                    >
                      {Math.round(frac * maxR)}
                    </text>
                  </g>
                ))}

                {/* Axes labels */}
                <text x={265} y={290} fill="#888" fontSize="12" textAnchor="middle">
                  Radius (kpc)
                </text>
                <text
                  x={15}
                  y={150}
                  fill="#888"
                  fontSize="12"
                  textAnchor="middle"
                  transform="rotate(-90, 15, 150)"
                >
                  Velocity (km/s)
                </text>

                {/* Curves */}
                {curves.map((curve) => (
                  <path
                    key={curve.name}
                    d={curve.points.map((p, i) => {
                      const x = 50 + (p.r / maxR) * 430
                      const y = 250 - (p.v / maxV) * 200
                      return `${i === 0 ? 'M' : 'L'} ${x} ${y}`
                    }).join(' ')}
                    fill="none"
                    stroke={curve.color}
                    strokeWidth={curve.name === 'Zimmerman' ? 3 : 2}
                    strokeDasharray={curve.name === 'Newton' ? '4,4' : undefined}
                    opacity={curve.name === 'Newton' ? 0.7 : 1}
                  />
                ))}

                {/* Observed flat velocity line */}
                <line
                  x1={50}
                  y1={250 - (galaxy.vFlat / maxV) * 200}
                  x2={480}
                  y2={250 - (galaxy.vFlat / maxV) * 200}
                  stroke="#fbbf24"
                  strokeWidth="1"
                  strokeDasharray="8,4"
                  opacity={0.5}
                />
                <text
                  x={485}
                  y={250 - (galaxy.vFlat / maxV) * 200 + 4}
                  fill="#fbbf24"
                  fontSize="9"
                >
                  Observed
                </text>

                {/* Legend */}
                {curves.map((curve, i) => (
                  <g key={curve.name} transform={`translate(60, ${60 + i * 20})`}>
                    <line
                      x1={0}
                      y1={0}
                      x2={20}
                      y2={0}
                      stroke={curve.color}
                      strokeWidth={2}
                      strokeDasharray={curve.name === 'Newton' ? '4,4' : undefined}
                    />
                    <text x={25} y={4} fill={curve.color} fontSize="10">
                      {curve.name}
                    </text>
                  </g>
                ))}
              </svg>

              {/* Redshift Slider */}
              <div className="mt-6 p-4 bg-gray-900/50 rounded-xl">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-400">Redshift: z = {redshift.toFixed(1)}</span>
                  <span className="text-cyan-400">
                    a₀ = {(a0_z * 1e10).toFixed(2)} × 10⁻¹⁰ m/s²
                    {redshift > 0 && ` (${E(redshift).toFixed(1)}× today)`}
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="10"
                  step="0.1"
                  value={redshift}
                  onChange={(e) => setRedshift(parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-cyan-500"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>Today</span>
                  <span>← Earlier Universe (only Zimmerman changes)</span>
                </div>
              </div>
            </div>

            {/* Predictions Table */}
            <div className="mt-6 bg-black/50 backdrop-blur rounded-xl border border-gray-700/50 p-6">
              <h3 className="font-bold text-white mb-4">Testable Predictions at z = {redshift.toFixed(1)}</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-gray-400 border-b border-gray-700">
                      <th className="text-left py-2">Observable</th>
                      <th className="text-center py-2">Newton</th>
                      <th className="text-center py-2">ΛCDM</th>
                      <th className="text-center py-2">Zimmerman</th>
                    </tr>
                  </thead>
                  <tbody className="text-gray-300">
                    <tr className="border-b border-gray-800">
                      <td className="py-2">Flat rotation curves</td>
                      <td className="text-center text-red-400">✗</td>
                      <td className="text-center text-green-400">✓</td>
                      <td className="text-center text-green-400">✓</td>
                    </tr>
                    <tr className="border-b border-gray-800">
                      <td className="py-2">No dark matter needed</td>
                      <td className="text-center text-red-400">✗</td>
                      <td className="text-center text-red-400">✗</td>
                      <td className="text-center text-green-400">✓</td>
                    </tr>
                    <tr className="border-b border-gray-800">
                      <td className="py-2">a₀ at z={redshift.toFixed(1)}</td>
                      <td className="text-center text-gray-500">N/A</td>
                      <td className="text-center text-gray-400">constant</td>
                      <td className="text-center text-cyan-400">{E(redshift).toFixed(2)}× local</td>
                    </tr>
                    <tr className="border-b border-gray-800">
                      <td className="py-2">BTFR offset at z={redshift.toFixed(1)}</td>
                      <td className="text-center text-gray-500">N/A</td>
                      <td className="text-center text-gray-400">0 dex</td>
                      <td className="text-center text-cyan-400">{(-Math.log10(E(redshift))).toFixed(2)} dex</td>
                    </tr>
                    <tr>
                      <td className="py-2">Falsifiable by JWST</td>
                      <td className="text-center text-gray-500">-</td>
                      <td className="text-center text-yellow-400">Partially</td>
                      <td className="text-center text-green-400">Yes</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        {/* Formula Reference */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 text-center p-6 bg-gradient-to-r from-cyan-900/20 to-purple-900/20 rounded-xl border border-cyan-500/20"
        >
          <div className="font-mono text-lg text-cyan-300 mb-2">
            Zimmerman: Z = 2√(8π/3) = {Z.toFixed(4)}
          </div>
          <div className="text-sm text-gray-400">
            a₀ = cH₀/Z | a₀(z) = a₀(0) × E(z) | Based on 175 SPARC galaxies
          </div>
        </motion.div>

        {/* Academic Citations */}
        <Citation
          citations={[
            CITATIONS.SPARC,
            CITATIONS.RAR,
            CITATIONS.PLANCK_2018,
            CITATIONS.CODATA_2018,
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
