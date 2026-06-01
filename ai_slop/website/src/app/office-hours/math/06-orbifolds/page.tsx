'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Z2 Action Visualization
function Z2ActionViz() {
  const [showAction, setShowAction] = useState(false)
  const [point, setPoint] = useState({ x: 0.6, y: 0.4 })

  const reflectedPoint = { x: 1 - point.x, y: 1 - point.y }

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 200 200" className="w-full max-w-xs mx-auto bg-white border border-gray-200 rounded">
        {/* Torus fundamental domain */}
        <rect x="20" y="20" width="160" height="160" fill="#F3F4F6" stroke="#9CA3AF" strokeWidth="2" />

        {/* Grid */}
        {[0.25, 0.5, 0.75].map((f) => (
          <g key={f}>
            <line x1={20 + f * 160} y1="20" x2={20 + f * 160} y2="180" stroke="#E5E7EB" strokeWidth="1" />
            <line x1="20" y1={20 + f * 160} x2="180" y2={20 + f * 160} stroke="#E5E7EB" strokeWidth="1" />
          </g>
        ))}

        {/* Fixed points (corners and center) */}
        {[
          { x: 0, y: 0 }, { x: 0.5, y: 0 }, { x: 1, y: 0 },
          { x: 0, y: 0.5 }, { x: 0.5, y: 0.5 }, { x: 1, y: 0.5 },
          { x: 0, y: 1 }, { x: 0.5, y: 1 }, { x: 1, y: 1 },
        ].map((p, i) => (
          <g key={i}>
            <circle
              cx={20 + p.x * 160}
              cy={20 + p.y * 160}
              r="8"
              fill="#EF4444"
              stroke="#DC2626"
              strokeWidth="2"
            />
            {(p.x === 0 || p.x === 1) && (p.y === 0 || p.y === 1) && (
              <text
                x={20 + p.x * 160 + (p.x === 0 ? -15 : 15)}
                y={20 + p.y * 160 + (p.y === 0 ? -8 : 15)}
                fontSize="10"
                fill="#DC2626"
                textAnchor="middle"
              >
                fixed
              </text>
            )}
          </g>
        ))}

        {/* Original point */}
        <circle
          cx={20 + point.x * 160}
          cy={20 + point.y * 160}
          r="10"
          fill="#3B82F6"
          stroke="#2563EB"
          strokeWidth="2"
          className="cursor-move"
        />
        <text x={20 + point.x * 160} y={20 + point.y * 160 - 15} fontSize="12" fill="#3B82F6" textAnchor="middle">P</text>

        {/* Reflected point */}
        {showAction && (
          <>
            <line
              x1={20 + point.x * 160}
              y1={20 + point.y * 160}
              x2={20 + reflectedPoint.x * 160}
              y2={20 + reflectedPoint.y * 160}
              stroke="#8B5CF6"
              strokeWidth="2"
              strokeDasharray="5,5"
            />
            <circle
              cx={20 + reflectedPoint.x * 160}
              cy={20 + reflectedPoint.y * 160}
              r="10"
              fill="#8B5CF6"
              stroke="#7C3AED"
              strokeWidth="2"
            />
            <text x={20 + reflectedPoint.x * 160} y={20 + reflectedPoint.y * 160 - 15} fontSize="12" fill="#8B5CF6" textAnchor="middle">σ(P)</text>
          </>
        )}

        {/* Labels */}
        <text x="100" y="15" textAnchor="middle" fontSize="10" fill="#6B7280">0</text>
        <text x="100" y="195" textAnchor="middle" fontSize="10" fill="#6B7280">2π</text>
        <text x="10" y="105" textAnchor="middle" fontSize="10" fill="#6B7280" transform="rotate(-90, 10, 105)">2π</text>
      </svg>

      <div className="flex justify-center gap-4">
        <button
          onClick={() => setShowAction(!showAction)}
          className={`px-4 py-2 rounded-lg transition-colors ${
            showAction
              ? 'bg-purple-600 text-white'
              : 'bg-gray-200 hover:bg-gray-300 text-gray-700'
          }`}
        >
          {showAction ? 'Hide Z₂ action' : 'Show Z₂ action: P → σ(P)'}
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">P.x = {point.x.toFixed(2)}</label>
          <input
            type="range"
            min="0.05"
            max="0.95"
            step="0.01"
            value={point.x}
            onChange={(e) => setPoint({ ...point, x: Number(e.target.value) })}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">P.y = {point.y.toFixed(2)}</label>
          <input
            type="range"
            min="0.05"
            max="0.95"
            step="0.01"
            value={point.y}
            onChange={(e) => setPoint({ ...point, y: Number(e.target.value) })}
            className="w-full"
          />
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Z₂ action:</strong> σ: (x, y) → (2π - x, 2π - y)
        <br />
        <span className="text-red-600">Red points</span> are fixed: σ(P) = P. These create orbifold singularities!
      </div>
    </div>
  )
}

// 8 Fixed Points Visualization
function FixedPointsViz() {
  const [selected, setSelected] = useState<number | null>(null)

  // Fixed points on T³/Z₂: (0 or π) in each of 3 coordinates → 2³ = 8 points
  const fixedPoints = [
    { coords: [0, 0, 0], label: '(0,0,0)' },
    { coords: [Math.PI, 0, 0], label: '(π,0,0)' },
    { coords: [0, Math.PI, 0], label: '(0,π,0)' },
    { coords: [0, 0, Math.PI], label: '(0,0,π)' },
    { coords: [Math.PI, Math.PI, 0], label: '(π,π,0)' },
    { coords: [Math.PI, 0, Math.PI], label: '(π,0,π)' },
    { coords: [0, Math.PI, Math.PI], label: '(0,π,π)' },
    { coords: [Math.PI, Math.PI, Math.PI], label: '(π,π,π)' },
  ]

  // Project 3D to 2D isometric view
  const project = (coords: number[]) => {
    const scale = 30
    const x = coords[0] - coords[2] * 0.5
    const y = coords[1] - coords[0] * 0.3 - coords[2] * 0.3
    return { x: 100 + x * scale / Math.PI, y: 100 - y * scale / Math.PI }
  }

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 200 200" className="w-full max-w-xs mx-auto bg-white border border-gray-200 rounded">
        {/* Draw edges of the cube */}
        {[
          [[0,0,0], [Math.PI,0,0]],
          [[0,0,0], [0,Math.PI,0]],
          [[0,0,0], [0,0,Math.PI]],
          [[Math.PI,Math.PI,0], [Math.PI,0,0]],
          [[Math.PI,Math.PI,0], [0,Math.PI,0]],
          [[Math.PI,Math.PI,0], [Math.PI,Math.PI,Math.PI]],
          [[Math.PI,0,Math.PI], [Math.PI,0,0]],
          [[Math.PI,0,Math.PI], [0,0,Math.PI]],
          [[Math.PI,0,Math.PI], [Math.PI,Math.PI,Math.PI]],
          [[0,Math.PI,Math.PI], [0,Math.PI,0]],
          [[0,Math.PI,Math.PI], [0,0,Math.PI]],
          [[0,Math.PI,Math.PI], [Math.PI,Math.PI,Math.PI]],
        ].map(([start, end], i) => {
          const p1 = project(start)
          const p2 = project(end)
          return (
            <line
              key={i}
              x1={p1.x}
              y1={p1.y}
              x2={p2.x}
              y2={p2.y}
              stroke="#D1D5DB"
              strokeWidth="1"
            />
          )
        })}

        {/* Fixed points */}
        {fixedPoints.map((fp, i) => {
          const p = project(fp.coords)
          return (
            <g key={i}>
              <circle
                cx={p.x}
                cy={p.y}
                r={selected === i ? 12 : 8}
                fill={selected === i ? '#8B5CF6' : '#EF4444'}
                stroke={selected === i ? '#7C3AED' : '#DC2626'}
                strokeWidth="2"
                className="cursor-pointer transition-all"
                onClick={() => setSelected(selected === i ? null : i)}
              />
              <text
                x={p.x}
                y={p.y + 4}
                fontSize="10"
                fill="white"
                textAnchor="middle"
                fontWeight="bold"
              >
                {i + 1}
              </text>
            </g>
          )
        })}

        {/* Axes labels */}
        <text x="160" y="140" fontSize="12" fill="#6B7280">x</text>
        <text x="70" y="40" fontSize="12" fill="#6B7280">y</text>
        <text x="50" y="160" fontSize="12" fill="#6B7280">z</text>
      </svg>

      <div className="text-center">
        <div className="text-4xl font-bold text-purple-600">8 Fixed Points</div>
        <div className="text-sm text-gray-600">= 2³ (two choices per dimension)</div>
      </div>

      {selected !== null && (
        <div className="bg-purple-50 p-3 rounded border border-purple-200 text-center">
          <div className="font-mono font-bold">{fixedPoints[selected].label}</div>
          <div className="text-sm text-gray-600 mt-1">
            Each fixed point contributes a twisted sector to the string spectrum
          </div>
        </div>
      )}

      <div className="bg-green-50 p-3 rounded border border-green-200 text-sm">
        <strong>Why 8?</strong> The Z₂ action sends x → -x (mod 2π). Fixed points satisfy x = -x,
        so x = 0 or π. With 3 coordinates, that's 2³ = 8 fixed points.
      </div>
    </div>
  )
}

// Twisted Sector Visualization
function TwistedSectorViz() {
  const [showTwisted, setShowTwisted] = useState(true)

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-4">
        <button
          onClick={() => setShowTwisted(false)}
          className={`px-4 py-2 rounded-lg transition-colors ${
            !showTwisted ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
          }`}
        >
          Untwisted Sector
        </button>
        <button
          onClick={() => setShowTwisted(true)}
          className={`px-4 py-2 rounded-lg transition-colors ${
            showTwisted ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-700'
          }`}
        >
          Twisted Sector
        </button>
      </div>

      <svg viewBox="0 0 300 150" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {!showTwisted ? (
          // Untwisted: closed string freely moving
          <g>
            <ellipse cx="150" cy="75" rx="60" ry="30" fill="none" stroke="#3B82F6" strokeWidth="3" />
            <path
              d="M 50 75 C 80 60, 100 90, 150 75 C 200 60, 220 90, 250 75"
              fill="none"
              stroke="#9CA3AF"
              strokeWidth="1"
              strokeDasharray="4,4"
            />
            <text x="150" y="120" textAnchor="middle" fontSize="12" fill="#3B82F6">
              Closed string can move freely
            </text>
          </g>
        ) : (
          // Twisted: string stuck at fixed point
          <g>
            {/* Fixed point */}
            <circle cx="150" cy="75" r="15" fill="#EF4444" stroke="#DC2626" strokeWidth="3" />

            {/* String attached to fixed point */}
            <ellipse cx="150" cy="75" rx="40" ry="25" fill="none" stroke="#8B5CF6" strokeWidth="3" />

            {/* Arrows showing string endpoints tied to fixed point */}
            <line x1="150" y1="75" x2="190" y2="75" stroke="#8B5CF6" strokeWidth="2" />
            <line x1="150" y1="75" x2="110" y2="75" stroke="#8B5CF6" strokeWidth="2" />

            <text x="150" y="120" textAnchor="middle" fontSize="12" fill="#8B5CF6">
              String stuck at fixed point
            </text>
            <text x="150" y="135" textAnchor="middle" fontSize="10" fill="#EF4444">
              (Boundary conditions: σ(X) = X)
            </text>
          </g>
        )}
      </svg>

      <div className="grid grid-cols-2 gap-4">
        <div className={`p-4 rounded border ${!showTwisted ? 'bg-blue-50 border-blue-300' : 'bg-gray-50 border-gray-200'}`}>
          <div className="font-medium text-blue-800">Untwisted Sector</div>
          <ul className="text-sm text-gray-600 mt-2 space-y-1">
            <li>• String moves freely on orbifold</li>
            <li>• States must be Z₂-invariant</li>
            <li>• Gives gauge bosons</li>
          </ul>
        </div>
        <div className={`p-4 rounded border ${showTwisted ? 'bg-purple-50 border-purple-300' : 'bg-gray-50 border-gray-200'}`}>
          <div className="font-medium text-purple-800">Twisted Sector</div>
          <ul className="text-sm text-gray-600 mt-2 space-y-1">
            <li>• String stuck at fixed point</li>
            <li>• One sector per fixed point (8 total)</li>
            <li>• Gives chiral fermions!</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default function OrbifoldsPage() {
  return (
    <DocumentLayout
      title="Orbifolds"
      description="T³/Z₂, fixed points, and the origin of chirality"
      phase="math"
      currentIndex={6}
      prevLink={{ href: '/office-hours/math/05-algebraic-topology', title: 'Algebraic Topology' }}
      nextLink={{ href: '/office-hours/math/07-index-theory', title: 'Index Theory' }}
    >
      <Section title="1. What is an Orbifold?">
        <p className="text-gray-700 mb-4">
          An <strong>orbifold</strong> is a space obtained by quotienting a manifold by a group action.
          Unlike a smooth manifold, orbifolds can have <em>singularities</em> at fixed points.
        </p>

        <Formula label="Definition">
          Orbifold = M / G (manifold M quotiented by group G)
        </Formula>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <strong>Manifold:</strong>
            <div className="text-sm text-gray-600">Smooth everywhere (like a sphere)</div>
          </div>
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <strong>Orbifold:</strong>
            <div className="text-sm text-purple-600">Singularities at fixed points (like a cone tip)</div>
          </div>
        </div>

        <KeyPoint>
          The Z² framework uses the orbifold <strong>T³/Z₂</strong> — the 3-torus with opposite
          points identified. This creates 8 fixed points and introduces <em>chirality</em>!
        </KeyPoint>
      </Section>

      <Section title="2. The Z₂ Action on the Torus">
        <p className="text-gray-700 mb-4">
          The Z₂ group has one non-trivial element σ that acts by reflection through the origin:
        </p>

        <Formula>
          σ: (x, y, z) → (-x, -y, -z) [mod 2π]
        </Formula>

        <InteractiveBox title="Z₂ Action on T² (2D slice of T³)">
          <Z2ActionViz />
        </InteractiveBox>

        <SubSection title="Properties of the Z₂ Action">
          <div className="space-y-2 text-gray-700">
            <p>• <strong>Involution:</strong> σ² = identity (applying twice returns to original)</p>
            <p>• <strong>Free action:</strong> σ has no fixed points (NOT true here!)</p>
            <p>• <strong>Fixed points:</strong> Points where σ(P) = P (orbifold singularities)</p>
          </div>
        </SubSection>
      </Section>

      <Section title="3. The 8 Fixed Points">
        <p className="text-gray-700 mb-4">
          Points fixed by the Z₂ action satisfy (x, y, z) = (-x, -y, -z) mod 2π.
          This means each coordinate is either 0 or π.
        </p>

        <InteractiveBox title="Fixed Points on T³/Z₂">
          <FixedPointsViz />
        </InteractiveBox>

        <Formula label="Fixed point count">
          2 × 2 × 2 = 8 fixed points
        </Formula>

        <Z2Connection
          formula="8 fixed points"
          description="Each fixed point creates a singularity where twisted sector strings can live"
        />
      </Section>

      <Section title="4. Twisted Sectors">
        <p className="text-gray-700 mb-4">
          In string theory on orbifolds, there are two types of string states:
        </p>

        <InteractiveBox title="Untwisted vs Twisted Sectors">
          <TwistedSectorViz />
        </InteractiveBox>

        <SubSection title="Physical Significance">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">Sector</th>
                  <th className="border border-gray-200 p-2">Boundary Condition</th>
                  <th className="border border-gray-200 p-2">Physics</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2">Untwisted</td>
                  <td className="border border-gray-200 p-2 font-mono">X(σ+2π) = X(σ)</td>
                  <td className="border border-gray-200 p-2">Gauge bosons, gravity</td>
                </tr>
                <tr className="bg-purple-50">
                  <td className="border border-gray-200 p-2">Twisted</td>
                  <td className="border border-gray-200 p-2 font-mono">X(σ+2π) = σ(X(σ))</td>
                  <td className="border border-gray-200 p-2 font-bold">Chiral fermions!</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>

        <KeyPoint>
          <strong>Chirality from orbifolds:</strong> The twisted sector states are localized
          at fixed points and naturally produce chiral (left-handed or right-handed) particles.
          This is why the weak force only affects left-handed particles!
        </KeyPoint>
      </Section>

      <Section title="5. Orbifold Geometry">
        <p className="text-gray-700 mb-4">
          Near each fixed point, the orbifold looks like ℝ³/Z₂ — a cone with a singular tip.
        </p>

        <div className="grid grid-cols-3 gap-3 text-center">
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-2xl mb-1">○</div>
            <div className="font-medium">Away from fixed points</div>
            <div className="text-xs text-gray-500">Locally looks like T³</div>
          </div>
          <div className="bg-red-50 p-3 rounded border border-red-200">
            <div className="text-2xl mb-1">△</div>
            <div className="font-medium">At fixed points</div>
            <div className="text-xs text-red-600">Conical singularity</div>
          </div>
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <div className="text-2xl mb-1">◆</div>
            <div className="font-medium">Blowing up</div>
            <div className="text-xs text-purple-600">Replace singularity with CP¹</div>
          </div>
        </div>

        <SubSection title="Resolution of Singularities">
          <p className="text-gray-700 mb-4">
            The conical singularities can be "resolved" by replacing each fixed point with
            a small 2-sphere (blowup). This is important for understanding the geometry!
          </p>
        </SubSection>
      </Section>

      <Section title="6. Connection to Z² Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="T³/Z₂"
            description="The fundamental compactification space of the Z² framework"
          />
          <Z2Connection
            formula="8 fixed points"
            description="Create 8 twisted sectors, contributing to the particle spectrum"
          />
          <Z2Connection
            formula="Chirality"
            description="Z₂ projection removes half the states, leaving only left-handed weak interactions"
          />
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Orbifolds Matter</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>T³/Z₂:</strong> Provides the compact extra dimensions</li>
            <li>• <strong>8 fixed points:</strong> Give twisted sector contributions</li>
            <li>• <strong>Chirality:</strong> Z₂ action creates matter-antimatter asymmetry</li>
            <li>• <strong>D-branes:</strong> Wrap cycles of T³/Z₂, giving gauge groups</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Verify that σ(x) = -x (mod 2π) satisfies σ² = identity.</li>
          <li>List all 8 fixed points of the Z₂ action on T³. Show they are (kπ, lπ, mπ) for k,l,m ∈ {'{0,1}'}.</li>
          <li>Why does T²/Z₂ have 4 fixed points while T³/Z₂ has 8?</li>
          <li>The orbifold ℝ²/Z₂ is a cone. What is the deficit angle?</li>
          <li>Explain why the Z₂ projection removes half the states from the spectrum.</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
