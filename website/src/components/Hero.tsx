'use client'

import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

export default function Hero() {
  const [zValue, setZValue] = useState(0)
  const targetZ = 5.788810

  useEffect(() => {
    const duration = 2000
    const steps = 60
    const increment = targetZ / steps
    let current = 0

    const timer = setInterval(() => {
      current += increment
      if (current >= targetZ) {
        setZValue(targetZ)
        clearInterval(timer)
      } else {
        setZValue(current)
      }
    }, duration / steps)

    return () => clearInterval(timer)
  }, [])

  return (
    <section className="min-h-screen flex flex-col items-center justify-center px-4 relative">
      {/* Glowing orb background */}
      <motion.div
        className="absolute w-96 h-96 rounded-full bg-quantum-purple/20 blur-3xl"
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />

      {/* Main content */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="text-center z-10"
      >
        <motion.h1
          className="text-5xl md:text-7xl font-bold mb-6"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <span className="text-white">The </span>
          <span className="text-quantum-purple glow-text">Zimmerman</span>
          <span className="text-white"> Framework</span>
        </motion.h1>

        <motion.p
          className="text-xl md:text-2xl text-gray-400 mb-12"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          One constant. All of physics.
        </motion.p>

        {/* The Z formula with animation */}
        <motion.div
          className="gradient-border p-8 md:p-12 inline-block"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8, duration: 0.5 }}
        >
          <div className="text-2xl md:text-4xl mb-4 text-gray-300">
            Z = 2√(8π/3)
          </div>
          <motion.div
            className="text-4xl md:text-6xl font-bold text-dimension-gold glow-text"
            key={zValue}
          >
            = {zValue.toFixed(6)}
          </motion.div>
        </motion.div>

        {/* Key stats */}
        <motion.div
          className="flex flex-wrap justify-center gap-8 mt-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2 }}
        >
          <Stat value="20+" label="Formulas" />
          <Stat value="<1%" label="Error" />
          <Stat value="0" label="Free Parameters" />
        </motion.div>

        {/* Launch Simulation Button */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
          className="mt-12"
        >
          <a
            href="/simulate"
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-600 to-cyan-600 rounded-lg text-white font-semibold hover:from-purple-500 hover:to-cyan-500 transition-all transform hover:scale-105"
          >
            <span>🌀</span>
            Launch Universe Simulation
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </a>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <svg
            className="w-6 h-6 text-gray-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            />
          </svg>
        </motion.div>
      </motion.div>
    </section>
  )
}

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div className="text-center">
      <div className="text-3xl md:text-4xl font-bold text-energy-cyan">{value}</div>
      <div className="text-gray-500 text-sm">{label}</div>
    </div>
  )
}
