'use client'

import { motion } from 'framer-motion'

const formulas = [
  { category: 'Cosmology', count: 2, avgError: 0.015, color: '#22d3d1' },
  { category: 'Fine Structure', count: 1, avgError: 0.004, color: '#fbbf24' },
  { category: 'Lepton Masses', count: 2, avgError: 0.12, color: '#8b5cf6' },
  { category: 'Proton Mass', count: 1, avgError: 0.008, color: '#f59e0b' },
  { category: 'CKM Matrix', count: 4, avgError: 0.34, color: '#3b82f6' },
  { category: 'PMNS Matrix', count: 4, avgError: 0.49, color: '#10b981' },
  { category: 'Boson Masses', count: 2, avgError: 0.43, color: '#ec4899' },
  { category: 'Strong Coupling', count: 1, avgError: 0.23, color: '#ef4444' },
  { category: 'CP Phases', count: 2, avgError: 0.28, color: '#6366f1' },
]

export default function AccuracyTable() {
  const totalFormulas = formulas.reduce((sum, f) => sum + f.count, 0)
  const weightedError = formulas.reduce((sum, f) => sum + f.avgError * f.count, 0) / totalFormulas

  return (
    <section className="py-20 px-4 md:px-8">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-quantum-purple">
            Accuracy Summary
          </h2>
          <p className="text-center text-gray-400 mb-12">
            {totalFormulas} formulas. Average error: {weightedError.toFixed(2)}%
          </p>
        </motion.div>

        {/* Animated bars */}
        <div className="space-y-4">
          {formulas.map((formula, index) => (
            <motion.div
              key={formula.category}
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="gradient-border p-4 bg-cosmic-dark/80"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: formula.color }}
                  />
                  <span className="text-white font-medium">{formula.category}</span>
                  <span className="text-gray-500 text-sm">({formula.count})</span>
                </div>
                <span
                  className="font-mono font-bold"
                  style={{ color: formula.avgError < 0.1 ? '#22c55e' : formula.avgError < 0.5 ? '#fbbf24' : '#f97316' }}
                >
                  {formula.avgError}%
                </span>
              </div>

              {/* Accuracy bar */}
              <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                <motion.div
                  className="h-full rounded-full"
                  style={{ backgroundColor: formula.color }}
                  initial={{ width: 0 }}
                  whileInView={{ width: `${Math.max(100 - formula.avgError * 50, 20)}%` }}
                  transition={{ duration: 1, delay: index * 0.1 + 0.3 }}
                  viewport={{ once: true }}
                />
              </div>
            </motion.div>
          ))}
        </div>

        {/* Total summary */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 1 }}
          viewport={{ once: true }}
          className="mt-12 text-center"
        >
          <div className="inline-block gradient-border p-8 bg-cosmic-dark/80">
            <div className="text-5xl font-bold text-dimension-gold mb-2">
              {totalFormulas}+
            </div>
            <div className="text-xl text-gray-300 mb-4">
              Formulas with Sub-Percent Accuracy
            </div>
            <div className="text-gray-500">
              All from a single constant: Z = 2√(8π/3)
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
