'use client'

import { motion } from 'framer-motion'

interface FormulaCardProps {
  title: string
  formula: string
  predicted: string
  measured: string
  error: number
  delay?: number
}

// Simple formula display without KaTeX (for reliability)
function FormulaDisplay({ formula }: { formula: string }) {
  // Convert LaTeX-like notation to readable Unicode text
  // Order matters: replace Greek letters first, then subscripts
  const readable = formula
    // Greek letters (must be done before removing backslashes)
    .replace(/\\alpha_s/g, 'αₛ')
    .replace(/\\alpha/g, 'α')
    .replace(/\\Omega_\\Lambda/g, 'Ω_Λ')
    .replace(/\\Omega/g, 'Ω')
    .replace(/\\Lambda/g, 'Λ')
    .replace(/\\mu/g, 'μ')
    .replace(/\\pi/g, 'π')
    .replace(/\\sqrt/g, '√')
    // Fractions
    .replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, '($1) / ($2)')
    // Superscripts
    .replace(/\^2/g, '²')
    .replace(/\^3/g, '³')
    .replace(/\^4/g, '⁴')
    // Subscripts (convert _X to subscript Unicode)
    .replace(/_\\Lambda/g, '_Λ')
    .replace(/_s/g, 'ₛ')
    .replace(/_m/g, 'ₘ')
    .replace(/_e/g, 'ₑ')
    .replace(/_p/g, 'ₚ')
    .replace(/_0/g, '₀')
    // Clean up remaining LaTeX artifacts
    .replace(/\\_/g, '_')
    .replace(/\{/g, '')
    .replace(/\}/g, '')
    .replace(/\\/g, '')  // Remove any remaining backslashes

  return (
    <div className="text-xl text-white font-mono text-center">
      {readable}
    </div>
  )
}

export default function FormulaCard({
  title,
  formula,
  predicted,
  measured,
  error,
  delay = 0
}: FormulaCardProps) {

  // Determine error color
  const getErrorColor = (err: number) => {
    if (err < 0.01) return 'text-green-400'
    if (err < 0.1) return 'text-green-500'
    if (err < 0.5) return 'text-yellow-400'
    return 'text-orange-400'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      viewport={{ once: true }}
      whileHover={{ scale: 1.02, y: -5 }}
      className="p-6 bg-gray-900/80 backdrop-blur rounded-xl border border-purple-500/30 hover:border-purple-500/60 transition-colors"
    >
      <h3 className="text-lg font-semibold text-purple-400 mb-4">{title}</h3>

      {/* Formula display */}
      <div className="mb-6 min-h-[60px] flex items-center justify-center bg-black/30 rounded-lg p-4">
        <FormulaDisplay formula={formula} />
      </div>

      {/* Values comparison */}
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-400">Predicted:</span>
          <span className="text-yellow-400 font-mono">{predicted}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Measured:</span>
          <span className="text-cyan-400 font-mono">{measured}</span>
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
          className="h-full bg-gradient-to-r from-purple-500 to-cyan-500"
          initial={{ width: 0 }}
          whileInView={{ width: `${Math.max(100 - error * 20, 50)}%` }}
          transition={{ duration: 1, delay: delay + 0.3 }}
          viewport={{ once: true }}
        />
      </div>
    </motion.div>
  )
}
