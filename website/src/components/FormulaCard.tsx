'use client'

import { motion } from 'framer-motion'
import { useEffect, useRef } from 'react'

interface FormulaCardProps {
  title: string
  formula: string
  predicted: string
  measured: string
  error: number
  delay?: number
}

export default function FormulaCard({
  title,
  formula,
  predicted,
  measured,
  error,
  delay = 0
}: FormulaCardProps) {
  const cardRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Render KaTeX
    if (cardRef.current && typeof window !== 'undefined') {
      const formulaEl = cardRef.current.querySelector('.formula')
      if (formulaEl && (window as any).katex) {
        (window as any).katex.render(formula, formulaEl, {
          throwOnError: false,
          displayMode: true
        })
      }
    }
  }, [formula])

  // Determine error color
  const getErrorColor = (err: number) => {
    if (err < 0.01) return 'text-green-400'
    if (err < 0.1) return 'text-green-500'
    if (err < 0.5) return 'text-yellow-400'
    return 'text-orange-400'
  }

  return (
    <motion.div
      ref={cardRef}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      viewport={{ once: true }}
      whileHover={{ scale: 1.02, y: -5 }}
      className="gradient-border p-6 bg-cosmic-dark/80 backdrop-blur"
    >
      <h3 className="text-lg font-semibold text-quantum-purple mb-4">{title}</h3>

      {/* Formula display */}
      <div className="formula text-xl text-white mb-6 min-h-[60px] flex items-center justify-center">
        {/* KaTeX will render here */}
      </div>

      {/* Values comparison */}
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-400">Predicted:</span>
          <span className="text-dimension-gold font-mono">{predicted}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Measured:</span>
          <span className="text-energy-cyan font-mono">{measured}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Error:</span>
          <span className={`font-mono font-bold ${getErrorColor(error)}`}>
            {error}%
          </span>
        </div>
      </div>

      {/* Accuracy bar */}
      <div className="mt-4 h-2 bg-gray-700 rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-gradient-to-r from-quantum-purple to-energy-cyan"
          initial={{ width: 0 }}
          whileInView={{ width: `${Math.max(100 - error * 20, 50)}%` }}
          transition={{ duration: 1, delay: delay + 0.3 }}
          viewport={{ once: true }}
        />
      </div>
    </motion.div>
  )
}
