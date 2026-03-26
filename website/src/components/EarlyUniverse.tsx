'use client'

import { motion } from 'framer-motion'
import { useState, useEffect, useMemo } from 'react'

// Physics constants
const Z = 2 * Math.sqrt(8 * Math.PI / 3)
const OMEGA_M = 0.315
const OMEGA_LAMBDA = 0.685
const a0_LOCAL = 1.2e-10

// E(z) function
function E(z: number): number {
  return Math.sqrt(OMEGA_M * Math.pow(1 + z, 3) + OMEGA_LAMBDA)
}

// Cosmic time from redshift (approximate, in Gyr)
function cosmicTime(z: number): number {
  // Approximation for flat ΛCDM
  if (z === 0) return 13.8
  const a = 1 / (1 + z)
  return 13.8 * Math.pow(a, 1.5)
}

// Key cosmic epochs
const EPOCHS = [
  { z: 1100, name: 'CMB Release', time: 0.00038, description: 'Universe becomes transparent', color: '#ff4444' },
  { z: 30, name: 'Dark Ages End', time: 0.1, description: 'First stars ignite', color: '#ff8844' },
  { z: 20, name: 'Cosmic Dawn', time: 0.18, description: 'First galaxies form', color: '#ffaa44' },
  { z: 10, name: 'Reionization', time: 0.48, description: 'UV light ionizes IGM', color: '#ffdd44' },
  { z: 6, name: 'Galaxy Assembly', time: 0.95, description: 'Rapid structure growth', color: '#88ff44' },
  { z: 2, name: 'Peak Star Formation', time: 3.3, description: 'Cosmic noon', color: '#44ff88' },
  { z: 0.87, name: 'El Gordo', time: 6.5, description: 'Massive cluster collision', color: '#44ffdd' },
  { z: 0, name: 'Today', time: 13.8, description: 'Present epoch', color: '#44ddff' },
]

// Structure formation rate enhancement
function structureEnhancement(z: number): number {
  // In Zimmerman framework, higher a₀ means faster structure formation
  // Enhancement scales roughly as E(z)^2 for gravitational dynamics
  return Math.pow(E(z), 2)
}

export default function EarlyUniverse() {
  const [currentEpoch, setCurrentEpoch] = useState(7) // Start at today
  const [animating, setAnimating] = useState(false)
  const [showParticles, setShowParticles] = useState(true)

  const epoch = EPOCHS[currentEpoch]
  const a0_ratio = E(epoch.z)

  // Generate particles representing matter distribution
  const particles = useMemo(() => {
    const count = 200
    const arr = []
    for (let i = 0; i < count; i++) {
      // More clustered at low z, more uniform at high z
      const clusterFactor = 1 / (1 + epoch.z / 10)
      const x = Math.random() * 100
      const y = Math.random() * 100

      // Add clustering based on epoch
      const clustered = Math.random() < clusterFactor
      const cx = clustered ? (Math.random() * 0.3 + 0.35) * 100 : x
      const cy = clustered ? (Math.random() * 0.3 + 0.35) * 100 : y

      arr.push({
        x: clustered ? cx + (Math.random() - 0.5) * 20 : x,
        y: clustered ? cy + (Math.random() - 0.5) * 20 : y,
        size: 2 + Math.random() * 3,
        brightness: 0.3 + Math.random() * 0.7,
      })
    }
    return arr
  }, [currentEpoch])

  // Auto-play through epochs
  const playTimeline = () => {
    setAnimating(true)
    let epoch = 0
    const interval = setInterval(() => {
      setCurrentEpoch(epoch)
      epoch++
      if (epoch >= EPOCHS.length) {
        clearInterval(interval)
        setAnimating(false)
      }
    }, 1500)
  }

  return (
    <div className="w-full min-h-screen bg-black p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-red-500 via-yellow-400 to-cyan-400 bg-clip-text text-transparent mb-4">
            Early Universe Simulation
          </h1>
          <p className="text-xl text-gray-400">
            Structure formation with evolving Zimmerman acceleration
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Visualization */}
          <div className="bg-gray-950 rounded-2xl border border-gray-800 overflow-hidden">
            {/* Universe view */}
            <div className="relative h-96 bg-gradient-to-b from-gray-950 to-black">
              {/* Background glow based on epoch */}
              <div
                className="absolute inset-0 opacity-20"
                style={{
                  background: `radial-gradient(circle at center, ${epoch.color}40 0%, transparent 70%)`,
                }}
              />

              {/* Particles */}
              {showParticles && (
                <svg viewBox="0 0 100 100" className="absolute inset-0 w-full h-full">
                  {particles.map((p, i) => (
                    <motion.circle
                      key={i}
                      initial={{ opacity: 0 }}
                      animate={{
                        cx: p.x,
                        cy: p.y,
                        opacity: p.brightness,
                      }}
                      transition={{ duration: 0.5 }}
                      r={p.size * (1 + a0_ratio / 20)}
                      fill={epoch.color}
                    />
                  ))}
                </svg>
              )}

              {/* Epoch label */}
              <div className="absolute top-4 left-4 right-4">
                <motion.div
                  key={currentEpoch}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-center"
                >
                  <div className="text-2xl font-bold" style={{ color: epoch.color }}>
                    {epoch.name}
                  </div>
                  <div className="text-sm text-gray-400">{epoch.description}</div>
                </motion.div>
              </div>

              {/* Stats overlay */}
              <div className="absolute bottom-4 left-4 right-4 grid grid-cols-3 gap-2 text-center text-xs">
                <div className="bg-black/60 rounded p-2">
                  <div className="text-gray-400">Redshift</div>
                  <div className="text-white font-mono">z = {epoch.z}</div>
                </div>
                <div className="bg-black/60 rounded p-2">
                  <div className="text-gray-400">Cosmic Age</div>
                  <div className="text-white font-mono">{epoch.time < 1 ? `${(epoch.time * 1000).toFixed(0)} Myr` : `${epoch.time.toFixed(1)} Gyr`}</div>
                </div>
                <div className="bg-black/60 rounded p-2">
                  <div className="text-gray-400">a₀ / a₀(today)</div>
                  <div className="text-cyan-400 font-mono font-bold">{a0_ratio.toFixed(1)}×</div>
                </div>
              </div>
            </div>

            {/* Timeline scrubber */}
            <div className="p-4 bg-gray-900/50">
              <div className="flex items-center gap-4 mb-2">
                <button
                  onClick={playTimeline}
                  disabled={animating}
                  className={`px-4 py-2 rounded text-sm ${
                    animating
                      ? 'bg-gray-700 text-gray-500'
                      : 'bg-cyan-600 text-white hover:bg-cyan-500'
                  }`}
                >
                  {animating ? 'Playing...' : 'Play Timeline'}
                </button>
                <div className="text-xs text-gray-500">
                  Click epochs or drag slider
                </div>
              </div>

              {/* Epoch buttons */}
              <div className="flex flex-wrap gap-1 mb-4">
                {EPOCHS.map((e, i) => (
                  <button
                    key={e.name}
                    onClick={() => setCurrentEpoch(i)}
                    className={`px-2 py-1 text-xs rounded transition-all ${
                      i === currentEpoch
                        ? 'ring-2 ring-white'
                        : 'opacity-60 hover:opacity-100'
                    }`}
                    style={{ backgroundColor: `${e.color}40`, color: e.color }}
                  >
                    {e.name}
                  </button>
                ))}
              </div>

              {/* Slider */}
              <input
                type="range"
                min={0}
                max={EPOCHS.length - 1}
                value={currentEpoch}
                onChange={(e) => setCurrentEpoch(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Big Bang</span>
                <span>Today</span>
              </div>
            </div>
          </div>

          {/* Physics explanation */}
          <div className="space-y-6">
            {/* Current epoch details */}
            <motion.div
              key={currentEpoch}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="p-6 bg-gray-900/50 rounded-xl border"
              style={{ borderColor: `${epoch.color}40` }}
            >
              <h3 className="text-lg font-bold mb-4" style={{ color: epoch.color }}>
                {epoch.name} (z = {epoch.z})
              </h3>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="p-3 bg-black/30 rounded">
                    <div className="text-gray-400">E(z)</div>
                    <div className="text-xl font-mono text-white">{E(epoch.z).toFixed(3)}</div>
                  </div>
                  <div className="p-3 bg-black/30 rounded">
                    <div className="text-gray-400">a₀(z)</div>
                    <div className="text-xl font-mono text-cyan-400">
                      {(a0_LOCAL * E(epoch.z) * 1e10).toFixed(2)} × 10⁻¹⁰
                    </div>
                  </div>
                </div>

                <div className="p-3 bg-cyan-900/20 rounded border border-cyan-500/20">
                  <div className="text-sm text-cyan-300 mb-1">Zimmerman Prediction:</div>
                  <div className="text-gray-300 text-sm">
                    {epoch.z > 5 ? (
                      <>
                        At z = {epoch.z}, gravitational dynamics were <strong className="text-cyan-400">{a0_ratio.toFixed(0)}× stronger</strong>.
                        This explains why JWST sees "impossible" early galaxies — they formed faster than ΛCDM predicts.
                      </>
                    ) : epoch.z > 0 ? (
                      <>
                        Structure formation proceeded {structureEnhancement(epoch.z).toFixed(1)}× faster than today due to enhanced a₀.
                        This resolves timing tensions in cluster formation.
                      </>
                    ) : (
                      <>
                        Local value of a₀ = 1.2 × 10⁻¹⁰ m/s². All high-z predictions reference this baseline.
                      </>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>

            {/* JWST comparison */}
            <div className="p-6 bg-purple-900/20 rounded-xl border border-purple-500/30">
              <h3 className="text-lg font-bold text-purple-400 mb-4">
                JWST "Impossible" Galaxies Explained
              </h3>

              <div className="space-y-3 text-sm">
                <div className="flex items-start gap-3">
                  <span className="text-red-400 text-lg">❌</span>
                  <div>
                    <div className="text-white font-medium">ΛCDM Problem:</div>
                    <div className="text-gray-400">
                      JWST finds massive galaxies at z &gt; 10 requiring &gt;80% star formation efficiency
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-green-400 text-lg">✓</span>
                  <div>
                    <div className="text-white font-medium">Zimmerman Solution:</div>
                    <div className="text-gray-400">
                      At z = 10, a₀ was {E(10).toFixed(0)}× stronger → dynamics enhanced → normal efficiency works
                    </div>
                  </div>
                </div>
              </div>

              {/* Efficiency comparison */}
              <div className="mt-4 grid grid-cols-2 gap-3">
                <div className="p-3 bg-red-900/20 rounded text-center">
                  <div className="text-xs text-gray-400">ΛCDM requires</div>
                  <div className="text-xl font-bold text-red-400">&gt;80%</div>
                  <div className="text-xs text-gray-500">star formation efficiency</div>
                </div>
                <div className="p-3 bg-green-900/20 rounded text-center">
                  <div className="text-xs text-gray-400">Zimmerman allows</div>
                  <div className="text-xl font-bold text-green-400">~10%</div>
                  <div className="text-xs text-gray-500">normal efficiency</div>
                </div>
              </div>
            </div>

            {/* Key insight */}
            <div className="p-4 bg-gradient-to-r from-cyan-900/30 to-purple-900/30 rounded-xl border border-cyan-500/20 text-center">
              <div className="font-mono text-cyan-300 mb-2">
                a₀(z) = a₀(0) × √(Ω_m(1+z)³ + Ω_Λ)
              </div>
              <div className="text-sm text-gray-400">
                The Zimmerman framework predicts evolving dynamics — testable by JWST
              </div>
            </div>
          </div>
        </div>

        {/* E(z) Evolution Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-8 p-6 bg-gray-900/50 rounded-xl border border-gray-700/50"
        >
          <h3 className="text-lg font-bold text-white mb-4 text-center">
            Acceleration Scale Evolution Through Cosmic History
          </h3>

          <svg viewBox="0 0 800 200" className="w-full h-48">
            {/* Grid */}
            <defs>
              <linearGradient id="evolutionGradient" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#ff4444" />
                <stop offset="30%" stopColor="#ffaa44" />
                <stop offset="60%" stopColor="#44ff88" />
                <stop offset="100%" stopColor="#44ddff" />
              </linearGradient>
            </defs>

            {/* Axes */}
            <line x1="60" y1="170" x2="760" y2="170" stroke="#444" strokeWidth="1" />
            <line x1="60" y1="20" x2="60" y2="170" stroke="#444" strokeWidth="1" />

            {/* Y-axis labels */}
            {[1, 5, 10, 15, 20].map((val, i) => (
              <g key={val}>
                <line x1="55" y1={170 - val * 7.5} x2="60" y2={170 - val * 7.5} stroke="#444" />
                <text x="50" y={174 - val * 7.5} fill="#666" fontSize="10" textAnchor="end">
                  {val}×
                </text>
              </g>
            ))}
            <text x="30" y="100" fill="#888" fontSize="10" textAnchor="middle" transform="rotate(-90, 30, 100)">
              a₀(z) / a₀(today)
            </text>

            {/* X-axis labels (cosmic time) */}
            <text x="410" y="195" fill="#888" fontSize="10" textAnchor="middle">
              Cosmic Time (Gyr)
            </text>

            {/* Evolution curve */}
            <path
              d={`M 60 ${170 - E(1100) * 7.5} ` +
                Array.from({ length: 100 }, (_, i) => {
                  const z = 1100 * Math.pow(0.95, i)
                  const t = cosmicTime(z)
                  const x = 60 + (t / 13.8) * 700
                  const y = Math.max(20, 170 - E(z) * 7.5)
                  return `L ${x} ${y}`
                }).join(' ')}
              fill="none"
              stroke="url(#evolutionGradient)"
              strokeWidth="3"
            />

            {/* Epoch markers */}
            {EPOCHS.map((e, i) => {
              const x = 60 + (e.time / 13.8) * 700
              const y = Math.max(20, 170 - E(e.z) * 7.5)
              return (
                <g key={e.name}>
                  <circle
                    cx={x}
                    cy={y}
                    r={currentEpoch === i ? 8 : 5}
                    fill={e.color}
                    stroke={currentEpoch === i ? 'white' : 'none'}
                    strokeWidth="2"
                    style={{ cursor: 'pointer' }}
                    onClick={() => setCurrentEpoch(i)}
                  />
                  {e.z > 0 && e.z < 100 && (
                    <text x={x} y={y - 12} fill={e.color} fontSize="8" textAnchor="middle">
                      z={e.z}
                    </text>
                  )}
                </g>
              )
            })}
          </svg>
        </motion.div>

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
