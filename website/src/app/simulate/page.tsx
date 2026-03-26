'use client'

import dynamic from 'next/dynamic'
import { useState } from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'

// Dynamic import to avoid SSR issues with Three.js
const GalaxySimulation = dynamic(
  () => import('@/components/GalaxySimulation'),
  { ssr: false, loading: () => <LoadingScreen /> }
)

function LoadingScreen() {
  return (
    <div className="w-full h-screen bg-black flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-purple-400">Loading Universe...</p>
      </div>
    </div>
  )
}

const simulations = [
  { id: 'galaxy', name: 'Galaxy Rotation', icon: '🌀', available: true },
  { id: 'btfr', name: 'Tully-Fisher', icon: '📊', available: false },
  { id: 'elgordo', name: 'El Gordo Cluster', icon: '💥', available: false },
  { id: 'universe', name: '4D Universe', icon: '🌌', available: false },
  { id: 'rar', name: 'RAR Evolution', icon: '📈', available: false },
]

export default function SimulatePage() {
  const [activeSimulation, setActiveSimulation] = useState('galaxy')

  return (
    <div className="flex h-screen bg-black">
      {/* Sidebar */}
      <motion.div
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className="w-64 bg-gray-900/80 backdrop-blur border-r border-purple-500/20 flex flex-col"
      >
        {/* Logo */}
        <Link href="/" className="p-4 border-b border-purple-500/20">
          <h1 className="text-lg font-bold text-white">
            <span className="text-purple-400">Z</span>immerman
          </h1>
          <p className="text-xs text-gray-500">Framework Visualizer</p>
        </Link>

        {/* Simulations List */}
        <div className="flex-1 p-4">
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Simulations
          </h2>
          <div className="space-y-2">
            {simulations.map((sim) => (
              <button
                key={sim.id}
                onClick={() => sim.available && setActiveSimulation(sim.id)}
                disabled={!sim.available}
                className={`w-full text-left px-3 py-2 rounded-lg flex items-center gap-3 transition-colors ${
                  activeSimulation === sim.id
                    ? 'bg-purple-600/30 text-white border border-purple-500/50'
                    : sim.available
                    ? 'text-gray-400 hover:bg-gray-800 hover:text-white'
                    : 'text-gray-600 cursor-not-allowed'
                }`}
              >
                <span className="text-xl">{sim.icon}</span>
                <div>
                  <div className="text-sm font-medium">{sim.name}</div>
                  {!sim.available && (
                    <div className="text-xs text-gray-600">Coming soon</div>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-purple-500/20">
          <div className="text-xs text-gray-500 mb-2">
            Z = 2√(8π/3) = 5.788810
          </div>
          <Link
            href="/"
            className="text-xs text-purple-400 hover:text-purple-300"
          >
            ← Back to Overview
          </Link>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 relative">
        {activeSimulation === 'galaxy' && <GalaxySimulation />}
      </div>
    </div>
  )
}
