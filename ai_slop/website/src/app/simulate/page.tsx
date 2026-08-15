'use client'

import dynamic from 'next/dynamic'
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'

// Dynamic imports to avoid SSR issues with heavy components
const GalaxySimulation = dynamic(
  () => import('@/components/GalaxySimulation'),
  { ssr: false, loading: () => <LoadingScreen label="Galaxy" /> }
)

const BTFRSimulation = dynamic(
  () => import('@/components/BTFRSimulation'),
  { ssr: false, loading: () => <LoadingScreen label="BTFR" /> }
)

const ElGordoVisualization = dynamic(
  () => import('@/components/ElGordoVisualization'),
  { ssr: false, loading: () => <LoadingScreen label="El Gordo" /> }
)

const EarlyUniverse = dynamic(
  () => import('@/components/EarlyUniverse'),
  { ssr: false, loading: () => <LoadingScreen label="Universe" /> }
)

const RARVisualization = dynamic(
  () => import('@/components/RARVisualization'),
  { ssr: false, loading: () => <LoadingScreen label="RAR" /> }
)

const A0RedshiftDiscriminator = dynamic(
  () => import('@/components/A0RedshiftDiscriminator'),
  { ssr: false, loading: () => <LoadingScreen label="a₀(z)" /> }
)

const GeometricVisualization = dynamic(
  () => import('@/components/GeometricVisualization'),
  { ssr: false, loading: () => <LoadingScreen label="Geometry" /> }
)

const ZConnectionWeb = dynamic(
  () => import('@/components/ZConnectionWeb'),
  { ssr: false, loading: () => <LoadingScreen label="Connections" /> }
)

const HurricaneSimulation = dynamic(
  () => import('@/components/HurricaneSimulation'),
  { ssr: false, loading: () => <LoadingScreen label="Hurricane" /> }
)

const ZSquaredAnalysis = dynamic(
  () => import('@/components/ZSquaredAnalysis'),
  { ssr: false, loading: () => <LoadingScreen label="Z² Analysis" /> }
)

const IntensityForecastViz = dynamic(
  () => import('@/components/IntensityForecastViz'),
  { ssr: false, loading: () => <LoadingScreen label="Intensity Forecast" /> }
)

const FundamentalDomainVisualization = dynamic(
  () => import('@/components/FundamentalDomainVisualization'),
  { ssr: false, loading: () => <LoadingScreen label="DESI 4PCF" /> }
)

function LoadingScreen({ label }: { label: string }) {
  return (
    <div className="w-full h-full min-h-screen bg-black flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-purple-400">Loading {label}...</p>
      </div>
    </div>
  )
}

const simulations = [
  {
    id: 'galaxy',
    name: 'Galaxy Rotation',
    icon: '🌀',
    available: true,
    description: '10 SPARC galaxies with 3 physics models',
    color: 'cyan'
  },
  {
    id: 'btfr',
    name: 'Tully-Fisher',
    icon: '📊',
    available: true,
    description: 'BTFR evolution with KMOS3D z~2 data',
    color: 'orange'
  },
  {
    id: 'elgordo',
    name: 'El Gordo Cluster',
    icon: '💥',
    available: true,
    description: '6σ tension at z=0.87 resolved',
    color: 'red'
  },
  {
    id: 'universe',
    name: 'Cosmic Timeline',
    icon: '🌌',
    available: true,
    description: 'a₀ evolution through cosmic history',
    color: 'purple'
  },
  {
    id: 'rar',
    name: 'RAR + SPARC',
    icon: '',
    available: true,
    description: '2,693 data points from 153 galaxies',
    color: 'blue'
  },
  {
    id: 'a0z',
    name: 'a₀(z) Discriminator',
    icon: '',
    available: true,
    description: 'Flat-below-z₀ derived law vs the disfavoured rising branch',
    color: 'cyan'
  },
  {
    id: 'geometry',
    name: 'Z Geometry',
    icon: '🔷',
    available: true,
    description: 'Cube × Sphere = Z² structure',
    color: 'indigo'
  },
  {
    id: 'connections',
    name: 'Full Structure',
    icon: '🕸️',
    available: true,
    description: 'Complete Z connection web',
    color: 'violet'
  },
  {
    id: 'hurricane',
    name: 'Hurricane Forecast',
    icon: '🌀',
    available: true,
    description: 'Track prediction with V* scaling',
    color: 'teal'
  },
  {
    id: 'z2analysis',
    name: 'Z² Framework',
    icon: '📐',
    available: true,
    description: 'RI prediction & golden ratio analysis',
    color: 'amber'
  },
  {
    id: 'intensity',
    name: 'Intensity Forecast',
    icon: '📈',
    available: true,
    description: 'Full intensity evolution comparison',
    color: 'rose'
  },
  {
    id: 'desi4pcf',
    name: 'DESI 4PCF',
    icon: '🌐',
    available: true,
    description: '2.1M galaxies show r=0.9986 NGC-SGC',
    color: 'blue'
  },
]

export default function SimulatePage() {
  const [activeSimulation, setActiveSimulation] = useState('galaxy')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const activeSim = simulations.find(s => s.id === activeSimulation)

  return (
    <div className="flex flex-col md:flex-row h-screen bg-black">
      {/* Mobile Header */}
      <div className="md:hidden flex items-center justify-between p-4 bg-gray-900/80 border-b border-purple-500/20">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-lg font-bold text-white">
            <span className="text-purple-400">Z</span>immerman
          </span>
        </Link>
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 text-white rounded-lg bg-gray-800 hover:bg-gray-700"
          aria-label="Toggle menu"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {sidebarOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile Simulation Selector (Dropdown) */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="md:hidden bg-gray-900/95 border-b border-purple-500/20 overflow-hidden"
          >
            <div className="p-4 grid grid-cols-2 gap-2">
              {simulations.map((sim) => (
                <button
                  key={sim.id}
                  onClick={() => {
                    sim.available && setActiveSimulation(sim.id)
                    setSidebarOpen(false)
                  }}
                  disabled={!sim.available}
                  className={`text-left px-3 py-3 rounded-lg flex items-center gap-2 transition-all ${
                    activeSimulation === sim.id
                      ? 'bg-purple-600/20 text-white border border-purple-500/50'
                      : sim.available
                      ? 'text-gray-400 bg-gray-800 hover:text-white'
                      : 'text-gray-600 cursor-not-allowed'
                  }`}
                >
                  <span className="text-xl">{sim.icon}</span>
                  <span className="text-sm font-medium truncate">{sim.name}</span>
                </button>
              ))}
            </div>
            <div className="px-4 pb-4">
              <Link
                href="/"
                className="text-xs text-purple-400 hover:text-purple-300 flex items-center gap-1"
              >
                ← Back to Overview
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Desktop Sidebar */}
      <motion.div
        initial={{ x: -100, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className="hidden md:flex w-72 bg-gray-900/80 backdrop-blur border-r border-purple-500/20 flex-col"
      >
        {/* Logo */}
        <Link href="/" className="p-4 border-b border-purple-500/20">
          <h1 className="text-lg font-bold text-white">
            <span className="text-purple-400">Z</span>immerman
          </h1>
          <p className="text-xs text-gray-500">Interactive Simulations</p>
        </Link>

        {/* Simulations List */}
        <div className="flex-1 p-4 overflow-y-auto">
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Simulations
          </h2>
          <div className="space-y-2">
            {simulations.map((sim) => (
              <button
                key={sim.id}
                onClick={() => sim.available && setActiveSimulation(sim.id)}
                disabled={!sim.available}
                className={`w-full text-left px-3 py-3 rounded-lg flex items-start gap-3 transition-all ${
                  activeSimulation === sim.id
                    ? `bg-${sim.color}-600/20 text-white border border-${sim.color}-500/50`
                    : sim.available
                    ? 'text-gray-400 hover:bg-gray-800 hover:text-white'
                    : 'text-gray-600 cursor-not-allowed'
                }`}
                style={{
                  backgroundColor: activeSimulation === sim.id ? `var(--${sim.color}-900, rgba(0,100,100,0.2))` : undefined,
                  borderColor: activeSimulation === sim.id ? `var(--${sim.color}-500, #06b6d4)` : undefined,
                }}
              >
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium">{sim.name}</div>
                  <div className="text-xs text-gray-500 truncate">{sim.description}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Info Panel */}
        <div className="p-4 border-t border-purple-500/20 bg-black/30">
          <div className="text-xs text-gray-400 mb-2">
            <span className="text-purple-400 font-bold">a₀</span> = c²√(Λ/32π) = 9.36 × 10⁻¹¹ m/s²
          </div>
          <div className="text-xs text-gray-500 mb-3">
            The Galaxy Rotation, Tully–Fisher, RAR and a₀(z) panels use real observational data and the
            framework&rsquo;s own footing. Other panels are legacy and not part of the audited result.
          </div>
          <Link
            href="/"
            className="text-xs text-purple-400 hover:text-purple-300 flex items-center gap-1"
          >
            ← Back to Overview
          </Link>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="flex-1 relative overflow-auto">
        {activeSimulation === 'galaxy' && <GalaxySimulation />}
        {activeSimulation === 'btfr' && <BTFRSimulation />}
        {activeSimulation === 'elgordo' && <ElGordoVisualization />}
        {activeSimulation === 'universe' && <EarlyUniverse />}
        {activeSimulation === 'rar' && <RARVisualization />}
        {activeSimulation === 'a0z' && (
          <div className="min-h-screen bg-black p-6">
            <div className="mx-auto max-w-4xl">
              <A0RedshiftDiscriminator />
            </div>
          </div>
        )}
        {activeSimulation === 'geometry' && <GeometricVisualization />}
        {activeSimulation === 'connections' && <ZConnectionWeb />}
        {activeSimulation === 'hurricane' && <HurricaneSimulation />}
        {activeSimulation === 'z2analysis' && <ZSquaredAnalysis />}
        {activeSimulation === 'intensity' && <IntensityForecastViz />}
        {activeSimulation === 'desi4pcf' && (
          <div className="w-full h-full min-h-screen bg-[#0a0a0a] p-8 overflow-auto">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-2xl font-bold text-white mb-2">DESI DR1 Parity-Odd 4PCF</h2>
              <p className="text-gray-400 mb-6">
                20,000 galaxies from 2.1M DESI LRGs mapped into T³/Z₂ fundamental domain.
                NGC-SGC correlation r = 0.9986 confirms global topological chirality.
              </p>
              <FundamentalDomainVisualization />
              <div className="mt-6 p-4 bg-gray-900/50 rounded border border-gray-800">
                <h3 className="text-sm font-bold text-gray-400 uppercase mb-2">Key Result</h3>
                <p className="text-gray-300 text-sm">
                  The correlation between Northern and Southern Galactic Caps would indicate
                  parity violation that is <em>globally coherent</em> — qualitatively
                  consistent with a chiral T³/Z₂ spatial topology, in which the orbifold&apos;s
                  Z₂ inversion fixes a single handedness for the whole space.
                </p>
                <p className="text-gray-500 text-xs mt-2">
                  Note: the chirality arises from the orbifold Z₂ projection, not from an
                  eta-invariant. The Dirac eta invariant of T³/Z₂ is 0 (see reviews/), so the
                  earlier identification η = Z² = 32π/3 was incorrect; Z² = 32π/3 = 8×(4π/3)
                  is the compactification scale (an input), and its relation to a cosmic-scale
                  parity signal is not established.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
