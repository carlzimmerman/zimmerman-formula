'use client'

import { useState, ReactNode } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface CollapsiblePanelProps {
  title: string
  children: ReactNode
  defaultOpen?: boolean
  className?: string
  headerClassName?: string
  titleColor?: string
  borderColor?: string
}

export default function CollapsiblePanel({
  title,
  children,
  defaultOpen = true,
  className = "",
  headerClassName = "",
  titleColor = "text-purple-400",
  borderColor = "border-purple-500/30"
}: CollapsiblePanelProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen)

  return (
    <div className={`bg-black/90 backdrop-blur rounded-lg border ${borderColor} overflow-hidden ${className}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full flex items-center justify-between p-3 hover:bg-white/5 transition-colors ${headerClassName}`}
      >
        <span className={`text-sm font-bold ${titleColor}`}>{title}</span>
        <svg
          className={`w-4 h-4 ${titleColor} transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className="px-4 pb-4">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
