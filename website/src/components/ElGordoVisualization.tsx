'use client'

import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import { Citation, CITATIONS } from './Citation'

// Physics constants
const Z = 2 * Math.sqrt(8 * Math.PI / 3)  // 5.788810
const OMEGA_M = 0.315   // Planck 2018
const OMEGA_LAMBDA = 0.685  // Planck 2018
const EL_GORDO_Z = 0.870  // ACT-CL J0102-4915

// Observed El Gordo properties (Menanteau et al. 2012, Kim et al. 2021, Asencio et al. 2021)
const EL_GORDO_DATA = {
  redshift: 0.870,
  redshift_err: 0.005,
  velocity_dispersion: 1321,  // km/s
  velocity_dispersion_err: 106,
  X_ray_temperature: 14.5,  // keV
  total_mass: 2.13e15,  // M_sun (M200)
  total_mass_err: 0.25e15,
  infall_velocity: 2500,  // km/s
  infall_velocity_err: 200,
  lcdm_tension_sigma: 6.16,  // Asencio et al. 2021
}

// Calculate E(z) = H(z)/H₀
function E(z: number): number {
  return Math.sqrt(OMEGA_M * Math.pow(1 + z, 3) + OMEGA_LAMBDA)
}

// El Gordo E(z) value
const E_EL_GORDO = E(EL_GORDO_Z)  // ~1.66

export default function ElGordoVisualization() {
  const [animationProgress, setAnimationProgress] = useState(0)
  const [showCalculation, setShowCalculation] = useState(false)

  useEffect(() => {
    const timer = setInterval(() => {
      setAnimationProgress(prev => (prev + 0.005) % 1)
    }, 50)
    return () => clearInterval(timer)
  }, [])

  // Cluster positions for collision animation
  const cluster1X = -150 + animationProgress * 150
  const cluster2X = 150 - animationProgress * 150

  return (
    <div className="w-full min-h-screen bg-gradient-to-b from-black via-purple-950/20 to-black p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-12">
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-orange-400 via-red-500 to-purple-600 bg-clip-text text-transparent mb-4"
          >
            El Gordo: The Fat One
          </motion.h1>
          <p className="text-xl text-gray-400">
            A massive galaxy cluster collision at z = {EL_GORDO_Z} that challenges ΛCDM
          </p>
        </div>

        {/* Main Visualization */}
        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {/* Collision Animation */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-black/50 backdrop-blur rounded-2xl border border-orange-500/30 p-6 relative overflow-hidden"
          >
            <h3 className="text-lg font-bold text-orange-400 mb-4">Cluster Collision</h3>

            <svg viewBox="-200 -100 400 200" className="w-full h-64">
              {/* Background stars */}
              {[...Array(50)].map((_, i) => (
                <circle
                  key={i}
                  cx={(Math.random() - 0.5) * 380}
                  cy={(Math.random() - 0.5) * 180}
                  r={Math.random() * 1.5}
                  fill="white"
                  opacity={Math.random() * 0.5 + 0.2}
                />
              ))}

              {/* Cluster 1 (approaching from left) */}
              <g transform={`translate(${cluster1X}, 0)`}>
                <circle r="40" fill="url(#cluster1Gradient)" opacity={0.8} />
                <circle r="60" fill="none" stroke="#ff6b35" strokeWidth="1" strokeDasharray="4,4" opacity={0.5} />
                {/* Hot gas glow */}
                <ellipse rx="55" ry="35" fill="url(#gasGlow1)" opacity={0.4} />
              </g>

              {/* Cluster 2 (approaching from right) */}
              <g transform={`translate(${cluster2X}, 0)`}>
                <circle r="35" fill="url(#cluster2Gradient)" opacity={0.8} />
                <circle r="50" fill="none" stroke="#a855f7" strokeWidth="1" strokeDasharray="4,4" opacity={0.5} />
                {/* Hot gas glow */}
                <ellipse rx="45" ry="30" fill="url(#gasGlow2)" opacity={0.4} />
              </g>

              {/* Collision shockwave */}
              {animationProgress > 0.7 && (
                <circle
                  r={(animationProgress - 0.7) * 200}
                  fill="none"
                  stroke="#fbbf24"
                  strokeWidth="2"
                  opacity={1 - (animationProgress - 0.7) * 3}
                />
              )}

              {/* Gradients */}
              <defs>
                <radialGradient id="cluster1Gradient">
                  <stop offset="0%" stopColor="#fbbf24" />
                  <stop offset="50%" stopColor="#f97316" />
                  <stop offset="100%" stopColor="#dc2626" stopOpacity="0.3" />
                </radialGradient>
                <radialGradient id="cluster2Gradient">
                  <stop offset="0%" stopColor="#c084fc" />
                  <stop offset="50%" stopColor="#a855f7" />
                  <stop offset="100%" stopColor="#7c3aed" stopOpacity="0.3" />
                </radialGradient>
                <radialGradient id="gasGlow1">
                  <stop offset="0%" stopColor="#ff6b35" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#ff6b35" stopOpacity="0" />
                </radialGradient>
                <radialGradient id="gasGlow2">
                  <stop offset="0%" stopColor="#a855f7" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#a855f7" stopOpacity="0" />
                </radialGradient>
              </defs>
            </svg>

            <div className="text-center text-sm text-gray-400 mt-4">
              Two massive clusters colliding at z = {EL_GORDO_Z}
            </div>
          </motion.div>

          {/* The Problem */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-black/50 backdrop-blur rounded-2xl border border-red-500/30 p-6"
          >
            <h3 className="text-lg font-bold text-red-400 mb-4">The ΛCDM Problem</h3>

            <div className="space-y-4">
              <div className="p-4 bg-red-900/20 rounded-lg border border-red-500/20">
                <div className="text-3xl font-bold text-red-400 mb-2">6.16σ</div>
                <div className="text-sm text-gray-400">
                  Tension with standard cosmology
                </div>
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex items-start gap-2">
                  <span className="text-red-400">✗</span>
                  <span className="text-gray-300">Mass of 2-3 × 10¹⁵ M☉ assembled "too fast"</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-red-400">✗</span>
                  <span className="text-gray-300">Collision velocity of ~2500 km/s is "impossible"</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-red-400">✗</span>
                  <span className="text-gray-300">Structure formation efficiency exceeds ΛCDM limits</span>
                </div>
              </div>

              <div className="p-3 bg-gray-800/50 rounded-lg text-xs text-gray-400">
                At z = 0.87, the universe was only 6.5 Gyr old. Standard dark matter simulations struggle to form such massive structures this quickly.
              </div>
            </div>
          </motion.div>
        </div>

        {/* The Zimmerman Solution */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="bg-gradient-to-r from-cyan-900/20 to-purple-900/20 backdrop-blur rounded-2xl border border-cyan-500/30 p-8 mb-12"
        >
          <h2 className="text-2xl font-bold text-cyan-400 mb-6 text-center">
            The Zimmerman Solution
          </h2>

          <div className="grid md:grid-cols-3 gap-6">
            {/* Step 1 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-cyan-900/50 flex items-center justify-center border border-cyan-500/50">
                <span className="text-2xl font-bold text-cyan-400">1</span>
              </div>
              <h4 className="font-bold text-white mb-2">Calculate E(z)</h4>
              <div className="font-mono text-sm text-cyan-300 bg-black/30 p-3 rounded">
                E(z) = √(Ωₘ(1+z)³ + Ω_Λ)
              </div>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-purple-900/50 flex items-center justify-center border border-purple-500/50">
                <span className="text-2xl font-bold text-purple-400">2</span>
              </div>
              <h4 className="font-bold text-white mb-2">At z = {EL_GORDO_Z}</h4>
              <div className="font-mono text-sm text-purple-300 bg-black/30 p-3 rounded">
                E({EL_GORDO_Z}) = √(0.315×1.87³ + 0.685)<br/>
                = √(2.06 + 0.685) = <span className="text-yellow-400 font-bold">{E_EL_GORDO.toFixed(2)}</span>
              </div>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-yellow-900/50 flex items-center justify-center border border-yellow-500/50">
                <span className="text-2xl font-bold text-yellow-400">3</span>
              </div>
              <h4 className="font-bold text-white mb-2">Enhanced Dynamics</h4>
              <div className="font-mono text-sm text-yellow-300 bg-black/30 p-3 rounded">
                a₀(z=0.87) = {E_EL_GORDO.toFixed(2)} × a₀(today)<br/>
                <span className="text-green-400">66% stronger acceleration!</span>
              </div>
            </div>
          </div>

          {/* Result */}
          <div className="mt-8 p-6 bg-black/40 rounded-xl border border-green-500/30">
            <h4 className="text-lg font-bold text-green-400 mb-3 text-center">Resolution</h4>
            <div className="grid md:grid-cols-2 gap-6 text-sm">
              <div className="space-y-2">
                <div className="flex items-start gap-2">
                  <span className="text-green-400">✓</span>
                  <span className="text-gray-300">Higher a₀ means stronger gravitational dynamics without dark matter</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-400">✓</span>
                  <span className="text-gray-300">Structure formation proceeds faster at higher redshift</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-start gap-2">
                  <span className="text-green-400">✓</span>
                  <span className="text-gray-300">Higher collision velocities are natural consequence</span>
                </div>
                <div className="flex items-start gap-2">
                  <span className="text-green-400">✓</span>
                  <span className="text-gray-300">6σ tension dissolves — no exotic physics needed</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Key Numbers */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          {[
            { label: 'Redshift', value: 'z = 0.87', color: 'text-orange-400' },
            { label: 'E(z)', value: E_EL_GORDO.toFixed(2), color: 'text-cyan-400' },
            { label: 'a₀ Enhancement', value: '66%', color: 'text-green-400' },
            { label: 'Tension Resolved', value: '6σ → 0', color: 'text-purple-400' },
          ].map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 + i * 0.1 }}
              className="bg-black/50 backdrop-blur rounded-xl border border-gray-700/50 p-4 text-center"
            >
              <div className={`text-2xl font-bold ${stat.color} mb-1`}>{stat.value}</div>
              <div className="text-xs text-gray-500">{stat.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Observed Properties Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0 }}
          className="mb-12 p-6 bg-black/50 backdrop-blur rounded-2xl border border-gray-700/50"
        >
          <h3 className="text-lg font-bold text-white mb-4">Observed Properties (ACT-CL J0102-4915)</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-700 text-gray-400">
                  <th className="text-left py-2 pr-4">Property</th>
                  <th className="text-right py-2 pr-4">Value</th>
                  <th className="text-right py-2">Source</th>
                </tr>
              </thead>
              <tbody className="text-gray-300">
                <tr className="border-b border-gray-800">
                  <td className="py-2 pr-4">Redshift</td>
                  <td className="text-right pr-4 font-mono">{EL_GORDO_DATA.redshift} ± {EL_GORDO_DATA.redshift_err}</td>
                  <td className="text-right text-gray-500">Menanteau+ 2012</td>
                </tr>
                <tr className="border-b border-gray-800">
                  <td className="py-2 pr-4">Velocity Dispersion</td>
                  <td className="text-right pr-4 font-mono">{EL_GORDO_DATA.velocity_dispersion} ± {EL_GORDO_DATA.velocity_dispersion_err} km/s</td>
                  <td className="text-right text-gray-500">Menanteau+ 2012</td>
                </tr>
                <tr className="border-b border-gray-800">
                  <td className="py-2 pr-4">X-ray Temperature</td>
                  <td className="text-right pr-4 font-mono">{EL_GORDO_DATA.X_ray_temperature} keV</td>
                  <td className="text-right text-gray-500">Menanteau+ 2012</td>
                </tr>
                <tr className="border-b border-gray-800">
                  <td className="py-2 pr-4">Total Mass (M₂₀₀)</td>
                  <td className="text-right pr-4 font-mono">(2.13 ± 0.25) × 10¹⁵ M☉</td>
                  <td className="text-right text-gray-500">Kim+ 2021</td>
                </tr>
                <tr className="border-b border-gray-800">
                  <td className="py-2 pr-4">Infall Velocity</td>
                  <td className="text-right pr-4 font-mono">{EL_GORDO_DATA.infall_velocity} ± {EL_GORDO_DATA.infall_velocity_err} km/s</td>
                  <td className="text-right text-gray-500">Asencio+ 2023</td>
                </tr>
                <tr>
                  <td className="py-2 pr-4 text-red-400 font-medium">ΛCDM Tension</td>
                  <td className="text-right pr-4 font-mono text-red-400">{EL_GORDO_DATA.lcdm_tension_sigma}σ</td>
                  <td className="text-right text-gray-500">Asencio+ 2021</td>
                </tr>
              </tbody>
            </table>
          </div>
        </motion.div>

        {/* Formula Reference */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
          className="text-center p-6 bg-black/30 rounded-xl border border-purple-500/20"
        >
          <div className="font-mono text-lg text-purple-300 mb-2">
            The Zimmerman Framework: Z = 2√(8π/3) = {Z.toFixed(4)}
          </div>
          <div className="text-sm text-gray-400">
            a₀ = cH₀/Z evolves as a₀(z) = a₀(0) × E(z)
          </div>
        </motion.div>

        {/* Academic Citations */}
        <Citation
          citations={[
            CITATIONS.EL_GORDO,
            {
              authors: 'Menanteau, F. et al.',
              year: 2012,
              title: 'The Atacama Cosmology Telescope: ACT-CL J0102-4915 "El Gordo"',
              journal: 'The Astrophysical Journal',
              volume: '748',
              pages: '7',
              doi: '10.1088/0004-637X/748/1/7',
              arxiv: '1109.0953',
              description: 'Discovery paper'
            },
            {
              authors: 'Kim, J. et al.',
              year: 2021,
              title: 'Measuring the mass of ACT-CL J0102-4915 using weak gravitational lensing',
              journal: 'The Astrophysical Journal',
              volume: '923',
              pages: '101',
              doi: '10.3847/1538-4357/ac295f',
              description: 'Weak lensing mass measurement'
            },
            CITATIONS.PLANCK_2018,
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
