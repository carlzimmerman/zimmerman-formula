'use client'

import { motion } from 'framer-motion'

const dimensions = [
  { d: 26, name: 'Bosonic String', color: '#f59e0b', physics: 'Flavor, CKM matrix' },
  { d: 11, name: 'M-Theory', color: '#8b5cf6', physics: 'Mass hierarchy' },
  { d: 8, name: 'E8 Gauge', color: '#3b82f6', physics: 'Matter density, gluons' },
  { d: 7, name: 'Compact', color: '#10b981', physics: 'W/Z ratio' },
  { d: 3, name: 'Spatial', color: '#22d3d1', physics: 'Dark energy, QCD colors' },
]

export default function DimensionalHierarchy() {
  return (
    <section className="py-20 px-4 md:px-8 bg-cosmic-blue/30">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-quantum-purple">
            The Dimensional Hierarchy
          </h2>
          <p className="text-center text-gray-400 mb-12 max-w-2xl mx-auto">
            Physics emerges from dimensions: 26 → 11 → 8 → 7 → 3.
            Each level controls different aspects of reality.
          </p>
        </motion.div>

        {/* Vertical hierarchy visualization */}
        <div className="relative">
          {/* Connecting line */}
          <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-dimension-gold via-quantum-purple to-energy-cyan" />

          {dimensions.map((dim, index) => (
            <motion.div
              key={dim.d}
              initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              viewport={{ once: true }}
              className={`relative flex items-center mb-8 ${
                index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'
              }`}
            >
              {/* Content box */}
              <div className={`w-5/12 ${index % 2 === 0 ? 'text-right pr-8' : 'text-left pl-8'}`}>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="inline-block gradient-border p-4 bg-cosmic-dark/80"
                >
                  <div className="text-sm text-gray-400">{dim.name}</div>
                  <div
                    className="text-2xl font-bold"
                    style={{ color: dim.color }}
                  >
                    {dim.d}D
                  </div>
                  <div className="text-xs text-gray-500 mt-1">{dim.physics}</div>
                </motion.div>
              </div>

              {/* Center node */}
              <div className="w-2/12 flex justify-center">
                <motion.div
                  className="w-6 h-6 rounded-full border-2 z-10"
                  style={{ borderColor: dim.color, backgroundColor: `${dim.color}33` }}
                  whileHover={{ scale: 1.5 }}
                  animate={{
                    boxShadow: [
                      `0 0 5px ${dim.color}`,
                      `0 0 20px ${dim.color}`,
                      `0 0 5px ${dim.color}`,
                    ],
                  }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
              </div>

              {/* Spacer */}
              <div className="w-5/12" />
            </motion.div>
          ))}
        </div>

        {/* Key equation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <div className="inline-block gradient-border p-6 bg-cosmic-dark/80">
            <div className="text-gray-400 mb-2">The unifying insight:</div>
            <div className="text-xl md:text-2xl text-white">
              (3 × 8 × 11) / 26 ≈ <span className="text-dimension-gold">10</span>
            </div>
            <div className="text-sm text-gray-500 mt-2">
              Superstring dimension emerges from the hierarchy!
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
