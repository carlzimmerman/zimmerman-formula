'use client'

import { useState, useRef, useEffect, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const Z = 2 * Math.sqrt(8 * Math.PI / 3)  // 5.788810

// Define all the nodes in our connection web
interface Node {
  id: string
  label: string
  formula?: string
  value?: string
  category: 'foundation' | 'exact' | 'derived' | 'physics' | 'cosmology' | 'particle'
  description: string
  x: number
  y: number
}

interface Connection {
  from: string
  to: string
  label?: string
  type: 'derives' | 'equals' | 'contains' | 'predicts'
}

const nodes: Node[] = [
  // Foundation - center
  {
    id: 'Z',
    label: 'Z',
    formula: '2√(8π/3)',
    value: '5.7888',
    category: 'foundation',
    description: 'The master constant derived from Friedmann geometry',
    x: 50,
    y: 45
  },

  // Geometric components - top
  {
    id: 'friedmann',
    label: 'Friedmann',
    formula: 'H² = 8πGρ/3',
    category: 'foundation',
    description: 'General Relativity cosmology equation',
    x: 25,
    y: 8
  },
  {
    id: 'bekenstein',
    label: 'Bekenstein',
    formula: 'S = A/4l_P²',
    category: 'foundation',
    description: 'Holographic entropy bound (factor of 2)',
    x: 75,
    y: 8
  },
  {
    id: '8pi',
    label: '8π',
    formula: 'Einstein tensor',
    category: 'foundation',
    description: 'From G_μν = 8πG T_μν',
    x: 35,
    y: 25
  },
  {
    id: '3dim',
    label: '3',
    formula: 'Spatial dim',
    category: 'foundation',
    description: 'Three spatial dimensions',
    x: 65,
    y: 25
  },
  {
    id: '11mtheory',
    label: '11',
    formula: '3 + 8',
    category: 'foundation',
    description: 'M-theory dimensions = space + cube',
    x: 50,
    y: 15
  },

  // Exact identities - middle ring
  {
    id: 'Z2',
    label: 'Z²',
    formula: '8 × (4π/3)',
    value: '33.51',
    category: 'exact',
    description: 'Cube vertices × Sphere volume',
    x: 30,
    y: 55
  },
  {
    id: 'Z4',
    label: 'Z⁴×9/π²',
    formula: '= 1024 = 2¹⁰',
    value: '10 bits',
    category: 'exact',
    description: 'Information content - exactly 10 bits',
    x: 70,
    y: 55
  },
  {
    id: 'cube',
    label: '8',
    formula: 'Cube vertices',
    category: 'exact',
    description: '2³ = corners of unit cube',
    x: 15,
    y: 45
  },
  {
    id: 'sphere',
    label: '4π/3',
    formula: 'Sphere vol',
    category: 'exact',
    description: 'Volume of unit sphere',
    x: 85,
    y: 45
  },
  {
    id: '2pi',
    label: '2π',
    formula: '3Z²/16',
    value: 'exact',
    category: 'exact',
    description: 'Circle circumference - from Z',
    x: 50,
    y: 60
  },

  // Derived physics - left side
  {
    id: 'alpha',
    label: 'α⁻¹',
    formula: '4Z² + 3',
    value: '137.04',
    category: 'derived',
    description: 'Fine structure constant (0.004% error)',
    x: 8,
    y: 65
  },
  {
    id: 'alphaself',
    label: 'α⁻¹+α',
    formula: '= 4Z² + 3',
    value: '137.034',
    category: 'derived',
    description: 'Self-referential (0.0015% error!)',
    x: 8,
    y: 78
  },
  {
    id: 'gauge12',
    label: '12',
    formula: '9Z²/(8π)',
    value: 'exact',
    category: 'derived',
    description: 'dim(SU(3)×SU(2)×U(1)) - SM gauge group',
    x: 92,
    y: 58
  },
  {
    id: 'bek4',
    label: '4',
    formula: '3Z²/(8π)',
    value: 'exact',
    category: 'derived',
    description: 'Bekenstein entropy factor S = A/4l_P²',
    x: 92,
    y: 70
  },
  {
    id: 'alpha_gut',
    label: 'α_GUT⁻¹',
    formula: '4Z + 1',
    value: '≈ 24',
    category: 'derived',
    description: 'GUT coupling = dim(SU(5))',
    x: 8,
    y: 55
  },
  {
    id: 'alpha_s',
    label: 'α_s',
    formula: 'Ω_Λ/Z',
    value: '0.118',
    category: 'derived',
    description: 'Strong coupling (QCD)',
    x: 20,
    y: 70
  },

  // Cosmology - bottom left
  {
    id: 'omega',
    label: 'Ω_Λ',
    formula: '3Z/(8+3Z)',
    value: '0.685',
    category: 'cosmology',
    description: 'Dark energy fraction (0.06% error)',
    x: 25,
    y: 88
  },
  {
    id: 'omega_m',
    label: 'Ω_m',
    formula: '8/(8+3Z)',
    value: '0.315',
    category: 'cosmology',
    description: 'Matter fraction (exact complement)',
    x: 38,
    y: 95
  },
  {
    id: 'a0',
    label: 'a₀',
    formula: 'cH₀/Z',
    value: '1.2×10⁻¹⁰',
    category: 'cosmology',
    description: 'MOND acceleration scale',
    x: 50,
    y: 88
  },
  {
    id: 'a0z',
    label: 'a₀(z)',
    formula: 'a₀×E(z)',
    value: 'evolution',
    category: 'cosmology',
    description: 'Evolves with cosmic time',
    x: 62,
    y: 95
  },
  {
    id: 'cc122',
    label: '122',
    formula: '4Z² - 12',
    value: 'log(ρ_Pl/ρ_Λ)',
    category: 'cosmology',
    description: 'Cosmological constant problem!',
    x: 12,
    y: 88
  },
  {
    id: 'H0',
    label: 'H₀',
    formula: 'Z×a₀/c',
    value: '71.5',
    category: 'cosmology',
    description: 'Hubble constant prediction',
    x: 75,
    y: 88
  },

  // Inflation
  {
    id: 'ns',
    label: 'n_s',
    formula: '1 - 1/(5Z)',
    value: '0.965',
    category: 'cosmology',
    description: 'Scalar spectral index',
    x: 88,
    y: 88
  },
  {
    id: 'efolds',
    label: 'N',
    formula: '10Z',
    value: '≈ 58',
    category: 'cosmology',
    description: 'Number of e-folds',
    x: 88,
    y: 95
  },

  // Particle physics - right side
  {
    id: 'tau_mu',
    label: 'm_τ/m_μ',
    formula: 'Z + 11',
    value: '16.79',
    category: 'particle',
    description: 'Tau/muon mass ratio (11 = 3+8)',
    x: 5,
    y: 35
  },
  {
    id: 'mu_e',
    label: 'm_μ/m_e',
    formula: '6Z² + Z',
    value: '206.8',
    category: 'particle',
    description: 'Muon/electron mass ratio',
    x: 5,
    y: 25
  },
  {
    id: 'mu_p',
    label: 'μ_p',
    formula: 'Z - 3',
    value: '2.789',
    category: 'particle',
    description: 'Proton magnetic moment',
    x: 18,
    y: 35
  },
  {
    id: 'mu_n_p',
    label: 'μ_n/μ_p',
    formula: '-Ω_Λ',
    value: '-0.685',
    category: 'particle',
    description: 'Nucleon moment ratio (0.003%!)',
    x: 32,
    y: 35
  },
  {
    id: 'theta13',
    label: 'sin²θ₁₃',
    formula: '1/(Z²+11)',
    value: '0.0225',
    category: 'particle',
    description: 'Neutrino mixing angle (0.01%)',
    x: 95,
    y: 35
  },
  {
    id: 'nu_ratio',
    label: 'Δm²₃₁/Δm²₂₁',
    formula: 'Z² - 1',
    value: '32.5',
    category: 'particle',
    description: 'Neutrino mass hierarchy',
    x: 95,
    y: 25
  },
  {
    id: 'proton_e',
    label: 'm_p/m_e',
    formula: '54Z²+6Z-8',
    value: '1836.3',
    category: 'particle',
    description: 'Proton/electron mass ratio',
    x: 82,
    y: 35
  },
  {
    id: 'b_c',
    label: 'm_b/m_c',
    formula: 'Z - 2.5',
    value: '3.29',
    category: 'particle',
    description: 'Bottom/charm quark ratio',
    x: 68,
    y: 35
  },
  {
    id: 'weinberg',
    label: 'sin²θ_W',
    formula: '6/(5Z-3)',
    value: '0.231',
    category: 'particle',
    description: 'Weak mixing angle',
    x: 55,
    y: 35
  },
]

const connections: Connection[] = [
  // Foundation to Z
  { from: 'friedmann', to: 'Z', type: 'derives', label: '√(8π/3)' },
  { from: 'bekenstein', to: 'Z', type: 'derives', label: '× 2' },
  { from: '8pi', to: 'Z', type: 'contains' },
  { from: '3dim', to: 'Z', type: 'contains' },
  { from: '3dim', to: '11mtheory', type: 'contains' },
  { from: 'cube', to: '11mtheory', type: 'contains' },

  // Z to exact identities
  { from: 'Z', to: 'Z2', type: 'derives' },
  { from: 'Z', to: 'Z4', type: 'derives' },
  { from: 'cube', to: 'Z2', type: 'equals', label: '×' },
  { from: 'sphere', to: 'Z2', type: 'equals' },
  { from: 'Z2', to: '2pi', type: 'equals' },

  // Exact to derived - couplings
  { from: 'Z2', to: 'alpha', type: 'predicts', label: '4Z²+3' },
  { from: 'alpha', to: 'alphaself', type: 'derives' },
  { from: 'Z2', to: 'gauge12', type: 'equals', label: '9Z²/8π' },
  { from: 'Z2', to: 'bek4', type: 'equals', label: '3Z²/8π' },
  { from: 'Z', to: 'alpha_gut', type: 'predicts', label: '4Z+1' },
  { from: 'omega', to: 'alpha_s', type: 'derives' },
  { from: 'Z', to: 'alpha_s', type: 'predicts' },

  // Z to cosmology
  { from: 'Z', to: 'omega', type: 'predicts' },
  { from: 'Z', to: 'omega_m', type: 'predicts' },
  { from: 'Z', to: 'a0', type: 'predicts' },
  { from: 'a0', to: 'a0z', type: 'derives' },
  { from: 'omega', to: 'a0z', type: 'contains' },
  { from: 'a0', to: 'H0', type: 'derives' },
  { from: 'Z', to: 'H0', type: 'predicts' },
  { from: 'alpha', to: 'cc122', type: 'derives', label: 'α⁻¹-15' },
  { from: 'Z2', to: 'cc122', type: 'predicts' },

  // Inflation
  { from: 'Z', to: 'ns', type: 'predicts' },
  { from: 'Z', to: 'efolds', type: 'predicts', label: '10Z' },

  // Z to particle physics - leptons
  { from: 'Z', to: 'tau_mu', type: 'predicts', label: '+11' },
  { from: '11mtheory', to: 'tau_mu', type: 'contains' },
  { from: 'Z2', to: 'mu_e', type: 'predicts', label: '6Z²+Z' },
  { from: 'Z', to: 'mu_p', type: 'predicts', label: '-3' },
  { from: '3dim', to: 'mu_p', type: 'contains' },
  { from: 'omega', to: 'mu_n_p', type: 'equals', label: '-Ω_Λ' },

  // Neutrinos
  { from: 'Z2', to: 'theta13', type: 'predicts' },
  { from: '11mtheory', to: 'theta13', type: 'contains', label: '+11' },
  { from: 'Z2', to: 'nu_ratio', type: 'predicts', label: '-1' },

  // Quarks
  { from: 'Z2', to: 'proton_e', type: 'predicts' },
  { from: 'Z', to: 'b_c', type: 'predicts', label: '-2.5' },
  { from: 'Z', to: 'weinberg', type: 'predicts' },

  // Cross connections
  { from: '3dim', to: 'alpha', type: 'contains', label: '+3' },
  { from: 'cube', to: 'tau_mu', type: 'contains', label: '+8' },
  { from: '3dim', to: 'tau_mu', type: 'contains', label: '+3' },
  { from: 'omega', to: 'a0', type: 'contains' },
  { from: 'bek4', to: 'bekenstein', type: 'equals' },
  { from: 'gauge12', to: 'alpha_gut', type: 'contains' },
]

const categoryColors: Record<string, { bg: string, border: string, text: string }> = {
  foundation: { bg: 'bg-purple-900/50', border: 'border-purple-500', text: 'text-purple-300' },
  exact: { bg: 'bg-cyan-900/50', border: 'border-cyan-500', text: 'text-cyan-300' },
  derived: { bg: 'bg-green-900/50', border: 'border-green-500', text: 'text-green-300' },
  physics: { bg: 'bg-blue-900/50', border: 'border-blue-500', text: 'text-blue-300' },
  cosmology: { bg: 'bg-orange-900/50', border: 'border-orange-500', text: 'text-orange-300' },
  particle: { bg: 'bg-pink-900/50', border: 'border-pink-500', text: 'text-pink-300' },
}

const connectionTypeColors: Record<string, string> = {
  derives: '#a855f7',
  equals: '#22d3ee',
  contains: '#6b7280',
  predicts: '#22c55e',
}

function NodeComponent({
  node,
  isSelected,
  onClick
}: {
  node: Node
  isSelected: boolean
  onClick: () => void
}) {
  const colors = categoryColors[node.category]

  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ delay: Math.random() * 0.5 }}
      className={`absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer
        ${colors.bg} ${colors.border} border-2 rounded-lg px-2 py-1
        ${isSelected ? 'ring-2 ring-white ring-offset-2 ring-offset-black z-20' : 'z-10'}
        hover:scale-110 transition-transform`}
      style={{
        left: `${node.x}%`,
        top: `${node.y}%`,
        minWidth: node.id === 'Z' ? '80px' : '60px'
      }}
      onClick={onClick}
    >
      <div className={`text-center ${colors.text} font-bold text-sm`}>
        {node.label}
      </div>
      {node.value && (
        <div className="text-center text-xs text-gray-400">
          {node.value}
        </div>
      )}
    </motion.div>
  )
}

export default function ZConnectionWeb() {
  const [selectedNode, setSelectedNode] = useState<string | null>('Z')
  const [showAllConnections, setShowAllConnections] = useState(true)
  const [highlightCategory, setHighlightCategory] = useState<string | null>(null)
  const svgRef = useRef<SVGSVGElement>(null)

  const selectedNodeData = nodes.find(n => n.id === selectedNode)

  // Filter connections based on selection
  const visibleConnections = useMemo(() => {
    if (showAllConnections) return connections
    if (!selectedNode) return []
    return connections.filter(c => c.from === selectedNode || c.to === selectedNode)
  }, [selectedNode, showAllConnections])

  // Filter nodes based on category highlight
  const nodeOpacity = (node: Node) => {
    if (!highlightCategory) return 1
    return node.category === highlightCategory ? 1 : 0.3
  }

  return (
    <div className="relative w-full h-screen bg-gradient-to-b from-gray-900 to-black overflow-hidden">
      {/* SVG for connections */}
      <svg
        ref={svgRef}
        className="absolute inset-0 w-full h-full pointer-events-none"
        style={{ zIndex: 5 }}
      >
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" fill="#666" />
          </marker>
        </defs>

        {visibleConnections.map((conn, i) => {
          const fromNode = nodes.find(n => n.id === conn.from)
          const toNode = nodes.find(n => n.id === conn.to)
          if (!fromNode || !toNode) return null

          const x1 = fromNode.x
          const y1 = fromNode.y
          const x2 = toNode.x
          const y2 = toNode.y

          // Calculate midpoint for label
          const mx = (x1 + x2) / 2
          const my = (y1 + y2) / 2

          const isHighlighted = selectedNode === conn.from || selectedNode === conn.to

          return (
            <g key={i}>
              <line
                x1={`${x1}%`}
                y1={`${y1}%`}
                x2={`${x2}%`}
                y2={`${y2}%`}
                stroke={connectionTypeColors[conn.type]}
                strokeWidth={isHighlighted ? 2 : 1}
                strokeOpacity={isHighlighted ? 0.8 : 0.3}
                strokeDasharray={conn.type === 'contains' ? '4,4' : undefined}
              />
              {conn.label && isHighlighted && (
                <text
                  x={`${mx}%`}
                  y={`${my}%`}
                  fill="#fff"
                  fontSize="10"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  className="bg-black"
                >
                  <tspan className="bg-black">{conn.label}</tspan>
                </text>
              )}
            </g>
          )
        })}
      </svg>

      {/* Nodes */}
      <div className="absolute inset-0" style={{ zIndex: 10 }}>
        {nodes.map(node => (
          <div
            key={node.id}
            style={{ opacity: nodeOpacity(node) }}
          >
            <NodeComponent
              node={node}
              isSelected={selectedNode === node.id}
              onClick={() => setSelectedNode(node.id === selectedNode ? null : node.id)}
            />
          </div>
        ))}
      </div>

      {/* Control Panel */}
      <div className="absolute top-4 left-4 bg-black/90 backdrop-blur p-4 rounded-lg border border-purple-500/30 max-w-xs z-30">
        <h2 className="text-lg font-bold text-white mb-1">Z Connection Web</h2>
        <p className="text-xs text-gray-400 mb-3">
          Complete geometric structure showing all relationships
        </p>

        {/* Category Legend */}
        <div className="space-y-1 mb-4">
          <div className="text-xs text-gray-500 mb-1">Categories (click to highlight):</div>
          {Object.entries(categoryColors).map(([cat, colors]) => (
            <button
              key={cat}
              onClick={() => setHighlightCategory(highlightCategory === cat ? null : cat)}
              className={`flex items-center gap-2 text-xs w-full px-2 py-1 rounded
                ${highlightCategory === cat ? 'bg-white/10' : 'hover:bg-white/5'}`}
            >
              <span className={`w-3 h-3 rounded ${colors.bg} ${colors.border} border`}></span>
              <span className={colors.text}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</span>
            </button>
          ))}
        </div>

        {/* Connection types */}
        <div className="text-xs text-gray-500 mb-2">Connection types:</div>
        <div className="grid grid-cols-2 gap-1 text-xs mb-4">
          <span className="flex items-center gap-1">
            <span className="w-4 h-0.5 bg-purple-500"></span> Derives
          </span>
          <span className="flex items-center gap-1">
            <span className="w-4 h-0.5 bg-cyan-500"></span> Equals
          </span>
          <span className="flex items-center gap-1">
            <span className="w-4 h-0.5 bg-gray-500" style={{backgroundImage: 'repeating-linear-gradient(90deg, #6b7280 0, #6b7280 4px, transparent 4px, transparent 8px)'}}></span> Contains
          </span>
          <span className="flex items-center gap-1">
            <span className="w-4 h-0.5 bg-green-500"></span> Predicts
          </span>
        </div>

        {/* Toggle */}
        <label className="flex items-center gap-2 text-sm cursor-pointer">
          <input
            type="checkbox"
            checked={showAllConnections}
            onChange={(e) => setShowAllConnections(e.target.checked)}
            className="rounded border-gray-600"
          />
          <span className="text-gray-300">Show all connections</span>
        </label>
      </div>

      {/* Selected Node Details */}
      <AnimatePresence>
        {selectedNodeData && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="absolute top-4 right-4 bg-black/90 backdrop-blur p-4 rounded-lg border border-purple-500/30 max-w-sm z-30"
          >
            <div className={`text-lg font-bold ${categoryColors[selectedNodeData.category].text} mb-1`}>
              {selectedNodeData.label}
            </div>
            {selectedNodeData.formula && (
              <div className="text-white font-mono text-sm mb-2">
                {selectedNodeData.formula}
              </div>
            )}
            {selectedNodeData.value && (
              <div className="text-cyan-400 font-mono text-sm mb-2">
                = {selectedNodeData.value}
              </div>
            )}
            <div className="text-gray-400 text-sm">
              {selectedNodeData.description}
            </div>

            {/* Show connections from this node */}
            <div className="mt-3 pt-3 border-t border-gray-700">
              <div className="text-xs text-gray-500 mb-1">Connected to:</div>
              <div className="flex flex-wrap gap-1">
                {connections
                  .filter(c => c.from === selectedNodeData.id || c.to === selectedNodeData.id)
                  .map((c, i) => {
                    const otherId = c.from === selectedNodeData.id ? c.to : c.from
                    const otherNode = nodes.find(n => n.id === otherId)
                    if (!otherNode) return null
                    return (
                      <button
                        key={i}
                        onClick={() => setSelectedNode(otherId)}
                        className={`text-xs px-2 py-1 rounded ${categoryColors[otherNode.category].bg} ${categoryColors[otherNode.category].text}`}
                      >
                        {otherNode.label}
                      </button>
                    )
                  })}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Bottom info */}
      <div className="absolute bottom-4 left-4 right-4 flex justify-center z-30">
        <div className="bg-black/80 backdrop-blur px-4 py-2 rounded-lg border border-gray-700 text-xs text-gray-400 max-w-2xl text-center">
          <span className="text-purple-400 font-bold">Z = 2√(8π/3)</span> connects Friedmann cosmology,
          Bekenstein entropy, the fine structure constant, Standard Model structure, and particle masses
          through pure geometry. Click nodes to explore relationships.
        </div>
      </div>
    </div>
  )
}
