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

        {/* Interactive Demonstrations */}
        <section className="py-20 px-4 md:px-8 bg-gradient-to-b from-transparent via-purple-950/10 to-transparent">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-quantum-purple">
              Interactive Demonstrations
            </h2>
            <p className="text-center text-gray-400 mb-12">
              Explore the Zimmerman framework with real physics simulations
            </p>

            <div className="grid md:grid-cols-3 gap-6">
              <a
                href="/derivation"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-green-500/30 hover:border-green-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">📐</div>
                <h3 className="text-xl font-bold text-green-400 mb-2 group-hover:text-green-300">
                  Full Derivation
                </h3>
                <p className="text-gray-400 text-sm">
                  Step-by-step math from Z = 2√(8π/3) to all predictions.
                </p>
              </a>

              <a
                href="/compare"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-purple-500/30 hover:border-purple-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">📊</div>
                <h3 className="text-xl font-bold text-purple-400 mb-2 group-hover:text-purple-300">
                  Model Comparison
                </h3>
                <p className="text-gray-400 text-sm">
                  Newton vs ΛCDM vs Zimmerman with SPARC data.
                </p>
              </a>

              <a
                href="/early-universe"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-red-500/30 hover:border-red-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">🌌</div>
                <h3 className="text-xl font-bold text-red-400 mb-2 group-hover:text-red-300">
                  Early Universe
                </h3>
                <p className="text-gray-400 text-sm">
                  Structure formation with evolving a₀ through cosmic history.
                </p>
              </a>

              <a
                href="/simulate"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-cyan-500/30 hover:border-cyan-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">🌀</div>
                <h3 className="text-xl font-bold text-cyan-400 mb-2 group-hover:text-cyan-300">
                  Galaxy Rotation
                </h3>
                <p className="text-gray-400 text-sm">
                  Galaxy dynamics as a₀ evolves through cosmic time.
                </p>
              </a>

              <a
                href="/el-gordo"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-orange-500/30 hover:border-orange-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">💥</div>
                <h3 className="text-xl font-bold text-orange-400 mb-2 group-hover:text-orange-300">
                  El Gordo Cluster
                </h3>
                <p className="text-gray-400 text-sm">
                  Resolves the 6σ tension at z = 0.87.
                </p>
              </a>

              <a
                href="https://doi.org/10.5281/zenodo.19199167"
                target="_blank"
                rel="noopener noreferrer"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-yellow-500/30 hover:border-yellow-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">📄</div>
                <h3 className="text-xl font-bold text-yellow-400 mb-2 group-hover:text-yellow-300">
                  Full Paper
                </h3>
                <p className="text-gray-400 text-sm">
                  Complete documentation with all 60+ formulas (DOI).
                </p>
              </a>
            </div>

            {/* Tools & Data section */}
            <h3 className="text-2xl font-bold text-center mt-12 mb-6 text-gray-300">
              Tools & Observational Data
            </h3>
            <div className="grid md:grid-cols-3 gap-6">
              <a
                href="/rar"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-blue-500/30 hover:border-blue-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">📈</div>
                <h3 className="text-xl font-bold text-blue-400 mb-2 group-hover:text-blue-300">
                  RAR + SPARC Data
                </h3>
                <p className="text-gray-400 text-sm">
                  2,693 data points from 153 galaxies showing the Radial Acceleration Relation.
                </p>
              </a>

              <a
                href="/calculator"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-teal-500/30 hover:border-teal-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">🧮</div>
                <h3 className="text-xl font-bold text-teal-400 mb-2 group-hover:text-teal-300">
                  Calculator
                </h3>
                <p className="text-gray-400 text-sm">
                  Interactive tool for a₀(z), galaxy dynamics, and BTFR predictions.
                </p>
              </a>

              <a
                href="/evidence"
                className="group p-6 bg-black/50 backdrop-blur rounded-xl border border-pink-500/30 hover:border-pink-500/60 transition-all hover:scale-[1.02]"
              >
                <div className="text-4xl mb-4">📜</div>
                <h3 className="text-xl font-bold text-pink-400 mb-2 group-hover:text-pink-300">
                  Evidence Timeline
                </h3>
                <p className="text-gray-400 text-sm">
                  JWST, DESI, wide binaries, El Gordo — all the supporting observations.
                </p>
              </a>
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
