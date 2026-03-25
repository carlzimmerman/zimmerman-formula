'use client'

import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import Hero from '@/components/Hero'
import FormulaCard from '@/components/FormulaCard'
import DimensionalHierarchy from '@/components/DimensionalHierarchy'
import AccuracyTable from '@/components/AccuracyTable'
import Footer from '@/components/Footer'

export default function Home() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <main className="relative min-h-screen overflow-x-hidden">
      {/* Animated background particles */}
      <div className="particles">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 10}s`,
              animationDuration: `${10 + Math.random() * 10}s`,
            }}
          />
        ))}
      </div>

      {/* Content */}
      <div className="relative z-10">
        <Hero />

        {/* Main formulas section */}
        <section className="py-20 px-4 md:px-8">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="max-w-6xl mx-auto"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-quantum-purple">
              The Core Formulas
            </h2>
            <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
              Every fundamental constant derives from Z = 2√(8π/3).
              No free parameters. Sub-percent accuracy.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <FormulaCard
                title="Fine Structure Constant"
                formula="\\alpha = \\frac{1}{4Z^2 + 3}"
                predicted="1/137.04"
                measured="1/137.036"
                error={0.004}
                delay={0}
              />
              <FormulaCard
                title="Dark Energy"
                formula="\\Omega_\\Lambda = \\frac{3Z}{8 + 3Z}"
                predicted="0.6846"
                measured="0.6847"
                error={0.01}
                delay={0.1}
              />
              <FormulaCard
                title="Matter Density"
                formula="\\Omega_m = \\frac{8}{8 + 3Z}"
                predicted="0.3154"
                measured="0.3153"
                error={0.02}
                delay={0.2}
              />
              <FormulaCard
                title="Strong Coupling"
                formula="\\alpha_s = \\frac{3}{8 + 3Z}"
                predicted="0.1183"
                measured="0.1180"
                error={0.23}
                delay={0.3}
              />
              <FormulaCard
                title="Muon/Electron Mass"
                formula="\\frac{m_\\mu}{m_e} = 64\\pi + Z"
                predicted="206.85"
                measured="206.77"
                error={0.04}
                delay={0.4}
              />
              <FormulaCard
                title="Proton/Electron Mass"
                formula="\\frac{m_p}{m_e} = 9\\frac{m_\\mu}{m_e} - (8+3Z)"
                predicted="1836.29"
                measured="1836.15"
                error={0.008}
                delay={0.5}
              />
            </div>
          </motion.div>
        </section>

        {/* Dimensional Hierarchy */}
        <DimensionalHierarchy />

        {/* Accuracy Table */}
        <AccuracyTable />

        {/* Footer */}
        <Footer />
      </div>
    </main>
  )
}
