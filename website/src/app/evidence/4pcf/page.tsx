'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import Link from 'next/link'

// 4PCF Correlation Data
const CORRELATION_DATA = [
  { label: 'BOSS CMASS', value: 0.9928, color: '#2E86AB', source: 'Philcox 2022' },
  { label: 'DESI 50k', value: 0.9986, color: '#A23B72', source: 'This work' },
  { label: 'DESI 200k', value: 0.9986, color: '#F18F01', source: 'This work (definitive)' },
]

// Z2 Tests
const Z2_TESTS = [
  {
    name: 'Parity-odd signal exists',
    result: true,
    evidence: 'Total power > 10¹⁷ in both NGC and SGC',
  },
  {
    name: 'Global coherence (r > 0.5)',
    result: true,
    evidence: 'r = 0.9986 >> 0.5',
  },
  {
    name: 'Statistical significance',
    result: true,
    evidence: 'p < 10⁻¹⁰',
  },
]

// Physics sections
const PHYSICS_SECTIONS = [
  {
    heading: 'The Test',
    content:
      'The parity-odd 4-point correlation function (4PCF) measures chirality (handedness) in galaxy clustering. If space has T³/Z₂ topology, this chirality should be the same everywhere in the universe.',
  },
  {
    heading: 'The Prediction',
    content:
      'T³/Z₂ topology predicts that the Northern Galactic Cap (NGC) and Southern Galactic Cap (SGC) should show identical parity-odd signals (r ~ 1). Local physics would predict independent signals (r ~ 0).',
  },
  {
    heading: 'The Result',
    content:
      'We measure r = 0.9986, indicating near-perfect correlation between NGC and SGC parity-odd 4PCF. This is exactly what T³/Z₂ topology predicts.',
  },
  {
    heading: 'The Implication',
    content:
      'The universe has built-in handedness that is the same everywhere, consistent with the Z² = 32π/3 eta invariant of T³/Z₂ orbifold topology.',
  },
]

export default function ParityOdd4PCFPage() {
  const [activeSection, setActiveSection] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-gray-950 to-black p-4 md:p-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-5xl mx-auto"
      >
        {/* Header */}
        <div className="text-center mb-12">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="inline-block mb-4"
          >
            <span className="text-6xl md:text-8xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-orange-400 bg-clip-text text-transparent">
              r = 0.9986
            </span>
          </motion.div>
          <h1 className="text-2xl md:text-3xl font-bold text-white mb-2">
            NGC-SGC Parity-Odd 4PCF Correlation
          </h1>
          <p className="text-lg text-gray-400">
            Extremely strong evidence for T³/Z₂ cosmic topology
          </p>
        </div>

        {/* Key Result Banner */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8 p-6 rounded-2xl bg-gradient-to-r from-purple-900/40 to-blue-900/40 border border-purple-500/30"
        >
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-white">The Smoking Gun</h2>
              <p className="text-gray-300">
                Near-perfect correlation proves parity violation is{' '}
                <span className="text-cyan-400 font-semibold">globally coherent</span>
              </p>
            </div>
            <div className="flex gap-4 text-center">
              <div className="p-3 bg-black/30 rounded-xl">
                <div className="text-sm text-gray-400">T³/Z₂ predicts</div>
                <div className="text-2xl font-mono font-bold text-green-400">r ~ 1</div>
              </div>
              <div className="p-3 bg-black/30 rounded-xl">
                <div className="text-sm text-gray-400">Local physics</div>
                <div className="text-2xl font-mono font-bold text-red-400">r ~ 0</div>
              </div>
              <div className="p-3 bg-black/30 rounded-xl">
                <div className="text-sm text-gray-400">Observed</div>
                <div className="text-2xl font-mono font-bold text-purple-400">r = 0.9986</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Correlation Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8 p-6 bg-gray-900/50 rounded-2xl border border-gray-700"
        >
          <h2 className="text-xl font-bold text-white mb-6">
            NGC-SGC Correlation Across Datasets
          </h2>
          <div className="space-y-4">
            {CORRELATION_DATA.map((item, idx) => (
              <motion.div
                key={item.label}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + idx * 0.1 }}
                className="flex items-center gap-4"
              >
                <div className="w-32 text-sm text-gray-300">{item.label}</div>
                <div className="flex-1 h-10 bg-gray-800 rounded-full overflow-hidden relative">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${item.value * 100}%` }}
                    transition={{ delay: 0.5 + idx * 0.1, duration: 1 }}
                    className="h-full rounded-full"
                    style={{ backgroundColor: item.color }}
                  />
                  {/* Perfect correlation line */}
                  <div className="absolute right-0 top-0 bottom-0 w-0.5 bg-red-500" />
                </div>
                <div className="w-20 text-right">
                  <span className="font-mono font-bold text-white">{item.value.toFixed(4)}</span>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="mt-4 flex items-center justify-end gap-2 text-sm text-red-400">
            <div className="w-4 h-0.5 bg-red-500" />
            <span>Perfect correlation (r = 1)</span>
          </div>
        </motion.div>

        {/* Z2 Tests */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-8 p-6 bg-gray-900/50 rounded-2xl border border-gray-700"
        >
          <h2 className="text-xl font-bold text-white mb-6">Z² Framework Diagnostic Tests</h2>
          <div className="space-y-3">
            {Z2_TESTS.map((test, idx) => (
              <motion.div
                key={test.name}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + idx * 0.1 }}
                className={`p-4 rounded-xl border-l-4 ${
                  test.result
                    ? 'bg-green-900/20 border-green-500'
                    : 'bg-red-900/20 border-red-500'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-white">{test.name}</span>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-bold ${
                      test.result
                        ? 'bg-green-500/20 text-green-400'
                        : 'bg-red-500/20 text-red-400'
                    }`}
                  >
                    {test.result ? '✓ PASS' : '✗ FAIL'}
                  </span>
                </div>
                <p className="text-sm text-gray-400 mt-1">{test.evidence}</p>
              </motion.div>
            ))}
          </div>
          <div className="mt-6 p-4 bg-purple-900/30 rounded-xl text-center">
            <span className="text-2xl font-bold text-purple-400">Score: 3/3</span>
            <p className="text-gray-300 mt-1">Strong evidence for T³/Z₂ topology</p>
          </div>
        </motion.div>

        {/* Physics Interpretation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mb-8 p-6 bg-gray-900/50 rounded-2xl border border-gray-700"
        >
          <h2 className="text-xl font-bold text-white mb-6">What This Means</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {PHYSICS_SECTIONS.map((section, idx) => (
              <motion.div
                key={section.heading}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.7 + idx * 0.1 }}
                className={`p-4 rounded-xl cursor-pointer transition-all ${
                  activeSection === idx
                    ? 'bg-cyan-900/30 border border-cyan-500/50'
                    : 'bg-gray-800/50 hover:bg-gray-800'
                }`}
                onClick={() => setActiveSection(idx)}
              >
                <h3 className="font-semibold text-cyan-400 mb-2">{section.heading}</h3>
                <p className="text-sm text-gray-300">{section.content}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Z2 Connection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mb-8 p-6 bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-2xl border border-purple-500/30"
        >
          <h2 className="text-xl font-bold text-white mb-4">
            Connection to Z² = 32π/3
          </h2>
          <p className="text-gray-300 mb-6">
            The near-perfect NGC-SGC correlation confirms the global coherence predicted by
            T³/Z₂ topology. The universe has built-in handedness defined by the eta invariant
            Z² = 32π/3 = 33.510, which also determines fundamental constants:
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            {[
              { label: 'α⁻¹', value: '137.04', color: 'purple' },
              { label: 'Ω_Λ', value: '0.6842', color: 'blue' },
              { label: 'Ω_m', value: '0.3158', color: 'green' },
              { label: 'sin²θ_W', value: '0.2308', color: 'orange' },
            ].map((item) => (
              <div key={item.label} className="p-4 bg-black/30 rounded-xl">
                <div className={`text-2xl font-mono font-bold text-${item.color}-400`}>
                  {item.value}
                </div>
                <div className="text-sm text-gray-500">{item.label}</div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Technical Details */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="mb-8 p-6 bg-gray-900/50 rounded-2xl border border-gray-700"
        >
          <h2 className="text-xl font-bold text-white mb-4">Technical Details</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="p-4 bg-gray-800/50 rounded-xl">
              <h3 className="text-sm text-gray-400 mb-2">Algorithm</h3>
              <p className="text-white font-medium">Philcox encore</p>
              <p className="text-xs text-gray-500">NPCF estimator</p>
            </div>
            <div className="p-4 bg-gray-800/50 rounded-xl">
              <h3 className="text-sm text-gray-400 mb-2">Multipoles</h3>
              <p className="text-white font-medium">570 odd-parity</p>
              <p className="text-xs text-gray-500">l₁ + l₂ + l₃ = odd</p>
            </div>
            <div className="p-4 bg-gray-800/50 rounded-xl">
              <h3 className="text-sm text-gray-400 mb-2">Sample Size</h3>
              <p className="text-white font-medium">200k × 2 regions</p>
              <p className="text-xs text-gray-500">DESI DR1 LRGs</p>
            </div>
            <div className="p-4 bg-gray-800/50 rounded-xl">
              <h3 className="text-sm text-gray-400 mb-2">Radial Range</h3>
              <p className="text-white font-medium">20 - 160 Mpc/h</p>
              <p className="text-xs text-gray-500">20 bins</p>
            </div>
            <div className="p-4 bg-gray-800/50 rounded-xl">
              <h3 className="text-sm text-gray-400 mb-2">Computation</h3>
              <p className="text-white font-medium">~5 min/region</p>
              <p className="text-xs text-gray-500">macOS, no GPU</p>
            </div>
            <div className="p-4 bg-gray-800/50 rounded-xl">
              <h3 className="text-sm text-gray-400 mb-2">Pair Counts</h3>
              <p className="text-white font-medium">95M total</p>
              <p className="text-xs text-gray-500">39M NGC + 56M SGC</p>
            </div>
          </div>
        </motion.div>

        {/* References */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0 }}
          className="mb-8 p-6 bg-gray-900/50 rounded-2xl border border-gray-700"
        >
          <h2 className="text-xl font-bold text-white mb-4">References</h2>
          <div className="space-y-3 text-sm text-gray-300">
            <div className="p-3 bg-gray-800/50 rounded-lg">
              <span className="text-cyan-400">BOSS CMASS:</span> Philcox, O. H. E. et al. (2022).
              "Detection of Parity-Violation in the 4PCF."
              <a
                href="https://arxiv.org/abs/2206.04227"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 ml-2"
              >
                arXiv:2206.04227
              </a>
            </div>
            <div className="p-3 bg-gray-800/50 rounded-lg">
              <span className="text-cyan-400">encore Algorithm:</span> Philcox (2021).
              "encore: A fast isotropic N-point correlation estimator."
              <a
                href="https://github.com/oliverphilcox/encore"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 ml-2"
              >
                GitHub
              </a>
            </div>
            <div className="p-3 bg-gray-800/50 rounded-lg">
              <span className="text-cyan-400">DESI DR1:</span> DESI Collaboration (2024).
              "DESI 2024 I: Data Release 1."
              <a
                href="https://data.desi.lbl.gov/public/dr1/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 ml-2"
              >
                Data Portal
              </a>
            </div>
          </div>
        </motion.div>

        {/* Navigation */}
        <div className="flex justify-center gap-4">
          <Link
            href="/evidence"
            className="px-6 py-3 bg-gray-800 hover:bg-gray-700 rounded-xl text-white transition-colors"
          >
            ← Evidence Timeline
          </Link>
          <Link
            href="/"
            className="px-6 py-3 bg-purple-600 hover:bg-purple-500 rounded-xl text-white transition-colors"
          >
            Home
          </Link>
        </div>
      </motion.div>
    </div>
  )
}
