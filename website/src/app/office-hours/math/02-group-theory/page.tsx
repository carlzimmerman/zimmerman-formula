'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Z2 Group Interactive
function Z2GroupViz() {
  const [state, setState] = useState<'e' | 'g'>('e')
  const [history, setHistory] = useState<string[]>(['e'])

  const applyG = () => {
    const newState = state === 'e' ? 'g' : 'e'
    setState(newState)
    setHistory([...history, 'g'])
  }

  const applyE = () => {
    setHistory([...history, 'e'])
  }

  const reset = () => {
    setState('e')
    setHistory(['e'])
  }

  return (
    <div className="space-y-4">
      {/* Visual representation */}
      <div className="flex items-center justify-center gap-8">
        <div
          className={`w-24 h-24 rounded-xl flex items-center justify-center text-4xl font-bold transition-all duration-300 ${
            state === 'e'
              ? 'bg-blue-100 border-2 border-blue-400 text-blue-700'
              : 'bg-orange-100 border-2 border-orange-400 text-orange-700 scale-x-[-1]'
          }`}
        >
          {state === 'e' ? '😊' : '🙃'}
        </div>
        <div className="text-center">
          <div className="text-sm text-gray-500">Current state</div>
          <div className="text-2xl font-bold font-mono">{state}</div>
        </div>
      </div>

      {/* Buttons */}
      <div className="flex justify-center gap-3">
        <button
          onClick={applyE}
          className="px-4 py-2 bg-blue-100 hover:bg-blue-200 text-blue-700 rounded-lg font-medium transition-colors"
        >
          Apply e (identity)
        </button>
        <button
          onClick={applyG}
          className="px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-lg font-medium transition-colors"
        >
          Apply g (flip)
        </button>
        <button
          onClick={reset}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors"
        >
          Reset
        </button>
      </div>

      {/* History */}
      <div className="text-center text-sm">
        <span className="text-gray-500">Operations: </span>
        <span className="font-mono">
          {history.slice(-8).join(' · ')}
          {history.length > 8 && '...'}
        </span>
        <span className="text-gray-500"> = </span>
        <span className="font-bold">{state}</span>
      </div>

      {/* Cayley table */}
      <div className="flex justify-center">
        <table className="text-sm border-collapse">
          <thead>
            <tr>
              <th className="border border-gray-300 p-2 bg-gray-100">·</th>
              <th className="border border-gray-300 p-2 bg-blue-100">e</th>
              <th className="border border-gray-300 p-2 bg-orange-100">g</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border border-gray-300 p-2 bg-blue-100 font-medium">e</td>
              <td className="border border-gray-300 p-2">e</td>
              <td className="border border-gray-300 p-2">g</td>
            </tr>
            <tr>
              <td className="border border-gray-300 p-2 bg-orange-100 font-medium">g</td>
              <td className="border border-gray-300 p-2">g</td>
              <td className="border border-gray-300 p-2 bg-green-100 font-medium">e ← g² = e!</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}

// Cyclic Group Clock
function CyclicGroupViz() {
  const [n, setN] = useState(12)
  const [current, setCurrent] = useState(0)
  const [addValue, setAddValue] = useState(1)

  const add = () => {
    setCurrent((current + addValue) % n)
  }

  const angles = Array.from({ length: n }, (_, i) => (i * 2 * Math.PI) / n - Math.PI / 2)

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-center gap-4">
        <label className="text-sm">
          Group Z<sub>{n}</sub>:
          <select
            value={n}
            onChange={(e) => {
              setN(Number(e.target.value))
              setCurrent(0)
            }}
            className="ml-2 border rounded p-1"
          >
            {[3, 4, 5, 6, 7, 8, 12].map((val) => (
              <option key={val} value={val}>
                n = {val}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          Add:
          <input
            type="number"
            value={addValue}
            onChange={(e) => setAddValue(Number(e.target.value))}
            className="ml-2 w-16 border rounded p-1 text-center"
            min="1"
            max={n - 1}
          />
        </label>
      </div>

      <div className="flex items-center justify-center gap-8">
        <svg viewBox="-1.5 -1.5 3 3" className="w-48 h-48">
          {/* Circle */}
          <circle cx="0" cy="0" r="1" fill="none" stroke="#E5E7EB" strokeWidth="0.05" />

          {/* Elements */}
          {angles.map((angle, i) => {
            const x = Math.cos(angle)
            const y = Math.sin(angle)
            const isActive = i === current
            return (
              <g key={i}>
                <circle
                  cx={x}
                  cy={y}
                  r={isActive ? 0.18 : 0.12}
                  fill={isActive ? '#8B5CF6' : '#E5E7EB'}
                  stroke={isActive ? '#7C3AED' : '#9CA3AF'}
                  strokeWidth="0.03"
                  className="cursor-pointer transition-all"
                  onClick={() => setCurrent(i)}
                />
                <text
                  x={x * 1.3}
                  y={y * 1.3 + 0.05}
                  fontSize="0.2"
                  textAnchor="middle"
                  fill={isActive ? '#7C3AED' : '#6B7280'}
                  fontWeight={isActive ? 'bold' : 'normal'}
                >
                  {i}
                </text>
              </g>
            )
          })}

          {/* Center */}
          <text x="0" y="0.08" fontSize="0.25" textAnchor="middle" fill="#1F2937" fontWeight="bold">
            Z<tspan fontSize="0.15" dy="0.08">{n}</tspan>
          </text>
        </svg>

        <div className="space-y-3">
          <button
            onClick={add}
            className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors"
          >
            +{addValue} (mod {n})
          </button>

          <div className="text-center">
            <div className="text-sm text-gray-500">Current element</div>
            <div className="text-3xl font-bold text-purple-600">{current}</div>
          </div>

          <div className="text-xs text-gray-500 text-center">
            {current} + {addValue} = {current + addValue} ≡ {(current + addValue) % n} (mod {n})
          </div>
        </div>
      </div>

      <div className="bg-blue-50 p-3 rounded text-sm text-center">
        <strong>Clock arithmetic:</strong> After 12 o'clock comes... 1! That's Z₁₂ in action.
      </div>
    </div>
  )
}

// SU(2) Rotation Visualization
function SU2Viz() {
  const [theta, setTheta] = useState(0)
  const [phi, setPhi] = useState(0)

  const thetaRad = (theta * Math.PI) / 180
  const phiRad = (phi * Math.PI) / 180

  // Point on Bloch sphere
  const x = Math.sin(thetaRad) * Math.cos(phiRad)
  const y = Math.sin(thetaRad) * Math.sin(phiRad)
  const z = Math.cos(thetaRad)

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            θ = {theta}° (latitude from north pole)
          </label>
          <input
            type="range"
            min="0"
            max="180"
            value={theta}
            onChange={(e) => setTheta(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            φ = {phi}° (longitude)
          </label>
          <input
            type="range"
            min="0"
            max="360"
            value={phi}
            onChange={(e) => setPhi(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <div className="flex items-center justify-center gap-8">
        <svg viewBox="-1.5 -1.5 3 3" className="w-48 h-48 bg-white border border-gray-200 rounded">
          {/* Sphere outline */}
          <circle cx="0" cy="0" r="1" fill="none" stroke="#D1D5DB" strokeWidth="0.02" />
          <ellipse cx="0" cy="0" rx="1" ry="0.3" fill="none" stroke="#E5E7EB" strokeWidth="0.02" />

          {/* Axes */}
          <line x1="0" y1="-1.2" x2="0" y2="1.2" stroke="#9CA3AF" strokeWidth="0.02" />
          <line x1="-1.2" y1="0" x2="1.2" y2="0" stroke="#9CA3AF" strokeWidth="0.02" />

          {/* State vector projected to 2D (simplified) */}
          <line
            x1="0"
            y1="0"
            x2={x * 0.9}
            y2={-z * 0.9}
            stroke="#8B5CF6"
            strokeWidth="0.06"
          />
          <circle cx={x * 0.9} cy={-z * 0.9} r="0.1" fill="#8B5CF6" />

          {/* Labels */}
          <text x="0" y="-1.3" fontSize="0.15" textAnchor="middle" fill="#3B82F6">|0⟩ (↑)</text>
          <text x="0" y="1.35" fontSize="0.15" textAnchor="middle" fill="#EF4444">|1⟩ (↓)</text>
        </svg>

        <div className="space-y-2 text-sm">
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <div className="text-xs text-purple-600 mb-1">Qubit state</div>
            <div className="font-mono">
              |ψ⟩ = cos(θ/2)|0⟩ + e<sup>iφ</sup>sin(θ/2)|1⟩
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2 text-center">
            <div className="bg-gray-50 p-2 rounded">
              <div className="text-xs text-gray-500">P(|0⟩)</div>
              <div className="font-mono">{(Math.cos(thetaRad / 2) ** 2 * 100).toFixed(0)}%</div>
            </div>
            <div className="bg-gray-50 p-2 rounded">
              <div className="text-xs text-gray-500">P(|1⟩)</div>
              <div className="font-mono">{(Math.sin(thetaRad / 2) ** 2 * 100).toFixed(0)}%</div>
            </div>
            <div className="bg-gray-50 p-2 rounded">
              <div className="text-xs text-gray-500">Phase</div>
              <div className="font-mono">{phi}°</div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>SU(2) acts on qubits:</strong> The group SU(2) rotates points on this sphere.
        <br />
        Note: θ = 180° only gives a sign flip, showing SU(2) → SO(3) is 2:1!
      </div>
    </div>
  )
}

export default function GroupTheoryPage() {
  return (
    <DocumentLayout
      title="Group Theory"
      description="Symmetry groups, Lie groups, and the structure of gauge theories"
      phase="math"
      currentIndex={2}
      prevLink={{ href: '/office-hours/math/01-linear-algebra', title: 'Linear Algebra' }}
      nextLink={{ href: '/office-hours/math/03-topology', title: 'Topology' }}
    >
      <Section title="1. What is a Group?">
        <p className="text-gray-700 mb-4">
          A <strong>group</strong> is a set G with an operation · that satisfies four axioms:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <strong>1. Closure:</strong>
            <div className="text-sm text-gray-600">If a, b ∈ G, then a · b ∈ G</div>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <strong>2. Associativity:</strong>
            <div className="text-sm text-gray-600">(a · b) · c = a · (b · c)</div>
          </div>
          <div className="bg-blue-50 p-3 rounded border border-blue-200">
            <strong>3. Identity:</strong>
            <div className="text-sm text-gray-600">∃e: e · a = a · e = a</div>
          </div>
          <div className="bg-green-50 p-3 rounded border border-green-200">
            <strong>4. Inverses:</strong>
            <div className="text-sm text-gray-600">∀a ∃a⁻¹: a · a⁻¹ = e</div>
          </div>
        </div>

        <KeyPoint>
          <strong>Groups encode symmetry.</strong> The set of all rotations of a square forms a group.
          The set of all permutations of objects forms a group. The gauge symmetries of physics form groups!
        </KeyPoint>
      </Section>

      <Section title="2. The Z₂ Group — The Simplest Non-Trivial Group">
        <p className="text-gray-700 mb-4">
          Z₂ = {'{e, g}'} has just two elements, with g² = e (applying g twice gives identity).
        </p>

        <InteractiveBox title="Z₂ Group Operations">
          <Z2GroupViz />
        </InteractiveBox>

        <SubSection title="Real-World Z₂ Examples">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-lg mb-1">💡</div>
              <strong>Light Switch</strong>
              <div className="text-sm text-gray-600">ON ↔ OFF, two flips = original</div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-lg mb-1">🪞</div>
              <strong>Mirror</strong>
              <div className="text-sm text-gray-600">Reflection², returns to original</div>
            </div>
            <div className="bg-purple-50 p-3 rounded border border-purple-200">
              <div className="text-lg mb-1">✋</div>
              <strong>Chirality</strong>
              <div className="text-sm text-purple-600">Left ↔ Right hand (can't rotate!)</div>
            </div>
          </div>
        </SubSection>

        <Z2Connection
          formula="T³/Z₂"
          description="The Z₂ projection on T³ creates chirality — why weak force only affects left-handed particles!"
        />
      </Section>

      <Section title="3. Cyclic Groups Zₙ">
        <p className="text-gray-700 mb-4">
          The cyclic group Zₙ is like clock arithmetic: numbers 0 to n-1, where n wraps back to 0.
        </p>

        <InteractiveBox title="Cyclic Groups (Clock Arithmetic)">
          <CyclicGroupViz />
        </InteractiveBox>

        <KeyPoint>
          <strong>Z₂ is the cyclic group Z₂</strong> — it has order 2, meaning you cycle back after 2 operations.
          The subscript tells you the number of elements.
        </KeyPoint>
      </Section>

      <Section title="4. Lie Groups">
        <p className="text-gray-700 mb-4">
          <strong>Lie groups</strong> are continuous groups — groups with infinitely many elements
          that vary smoothly. The Standard Model uses these extensively!
        </p>

        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2">Group</th>
                <th className="border border-gray-200 p-2">Name</th>
                <th className="border border-gray-200 p-2">Dim</th>
                <th className="border border-gray-200 p-2">Physics Role</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2 font-mono">U(1)</td>
                <td className="border border-gray-200 p-2">Unitary 1×1</td>
                <td className="border border-gray-200 p-2">1</td>
                <td className="border border-gray-200 p-2">Electromagnetism</td>
              </tr>
              <tr className="bg-blue-50">
                <td className="border border-gray-200 p-2 font-mono">SU(2)</td>
                <td className="border border-gray-200 p-2">Special Unitary 2×2</td>
                <td className="border border-gray-200 p-2">3</td>
                <td className="border border-gray-200 p-2">Weak force</td>
              </tr>
              <tr className="bg-green-50">
                <td className="border border-gray-200 p-2 font-mono">SU(3)</td>
                <td className="border border-gray-200 p-2">Special Unitary 3×3</td>
                <td className="border border-gray-200 p-2">8</td>
                <td className="border border-gray-200 p-2">Strong force (QCD)</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2 font-mono">SO(3)</td>
                <td className="border border-gray-200 p-2">Special Orthogonal</td>
                <td className="border border-gray-200 p-2">3</td>
                <td className="border border-gray-200 p-2">3D rotations</td>
              </tr>
            </tbody>
          </table>
        </div>

        <Formula label="The Standard Model Gauge Group">
          G_SM = SU(3) × SU(2) × U(1)
        </Formula>
      </Section>

      <Section title="5. SU(2) and Qubits">
        <p className="text-gray-700 mb-4">
          SU(2) is the group of 2×2 unitary matrices with determinant 1. It acts on 2-component
          spinors and describes rotations in quantum mechanics.
        </p>

        <InteractiveBox title="SU(2) Acting on the Bloch Sphere">
          <SU2Viz />
        </InteractiveBox>

        <SubSection title="Key Properties of SU(2)">
          <div className="space-y-2 text-gray-700">
            <p>• <strong>3 generators:</strong> The Pauli matrices σₓ, σᵧ, σᵤ</p>
            <p>• <strong>Commutation:</strong> [σᵢ, σⱼ] = 2iεᵢⱼₖσₖ</p>
            <p>• <strong>Covers SO(3):</strong> SU(2) → SO(3) is 2:1 (360° rotation = -1)</p>
          </div>
        </SubSection>
      </Section>

      <Section title="6. Group Generators and Lie Algebras">
        <p className="text-gray-700 mb-4">
          Every Lie group has an associated <strong>Lie algebra</strong> — the space of infinitesimal generators.
        </p>

        <Formula label="Lie bracket (commutator)">
          [T_a, T_b] = if_abc T_c
        </Formula>

        <p className="text-gray-700 my-4">
          The <strong>structure constants</strong> f_abc encode the group's structure.
        </p>

        <Z2Connection
          formula="rank(G_SM) = 2 + 1 + 1 = 4"
          description="This '4' appears in α⁻¹ = 4Z² + 3"
        />
      </Section>

      <Section title="7. Connection to Z² Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="T³/Z₂"
            description="Z₂ orbifold creates fixed points and chirality"
          />
          <Z2Connection
            formula="SU(3)×SU(2)×U(1)"
            description="Standard Model gauge group emerges from compactification"
          />
          <Z2Connection
            formula="sin²θ_W = 3/13"
            description="From intersection numbers of D-branes on the orbifold"
          />
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Group Theory Matters</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Symmetries</strong> determine conservation laws (Noether's theorem)</li>
            <li>• <strong>Gauge groups</strong> determine the forces of nature</li>
            <li>• <strong>Z₂</strong> creates chirality through orbifold projection</li>
            <li>• <strong>Rank</strong> of gauge group appears in fine structure constant</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Verify that Z₂ satisfies all four group axioms.</li>
          <li>In Z₁₂ (clock arithmetic), compute: 7 + 8 = ?</li>
          <li>How many elements does SU(2) have? (Hint: it's infinite!)</li>
          <li>The Pauli matrices satisfy σᵢσⱼ = δᵢⱼI + iεᵢⱼₖσₖ. Verify [σₓ, σᵧ] = 2iσᵤ.</li>
          <li>Why is rank(SU(n)) = n - 1? (Hint: traceless diagonal matrices)</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
