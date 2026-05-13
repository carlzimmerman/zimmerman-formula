'use client'

import { useState, useEffect } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Pendulum Oscillator Visualization
function PendulumViz() {
  const [angle, setAngle] = useState(30)
  const [time, setTime] = useState(0)
  const [isRunning, setIsRunning] = useState(false)
  const [length, setLength] = useState(1)

  const omega = Math.sqrt(9.8 / length) // angular frequency
  const period = 2 * Math.PI / omega

  useEffect(() => {
    if (!isRunning) return
    const interval = setInterval(() => {
      setTime(t => t + 0.05)
    }, 50)
    return () => clearInterval(interval)
  }, [isRunning])

  const angleRad = (angle * Math.PI / 180) * Math.cos(omega * time)
  const pendulumX = Math.sin(angleRad) * length * 100
  const pendulumY = Math.cos(angleRad) * length * 100

  const energy = 0.5 * length * (angle * Math.PI / 180) ** 2 * 9.8 // simplified
  const KE = energy * Math.sin(omega * time) ** 2
  const PE = energy * Math.cos(omega * time) ** 2

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Initial angle: {angle} degrees
          </label>
          <input
            type="range"
            min="5"
            max="60"
            value={angle}
            onChange={(e) => setAngle(Number(e.target.value))}
            className="w-full"
            disabled={isRunning}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Length: {length.toFixed(1)} m
          </label>
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={length}
            onChange={(e) => setLength(Number(e.target.value))}
            className="w-full"
            disabled={isRunning}
          />
        </div>
      </div>

      <div className="flex justify-center gap-3">
        <button
          onClick={() => setIsRunning(!isRunning)}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            isRunning
              ? 'bg-red-500 hover:bg-red-600 text-white'
              : 'bg-green-500 hover:bg-green-600 text-white'
          }`}
        >
          {isRunning ? 'Stop' : 'Start'}
        </button>
        <button
          onClick={() => { setTime(0); setIsRunning(false) }}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
        >
          Reset
        </button>
      </div>

      <svg viewBox="-150 -20 300 200" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Pivot */}
        <circle cx="0" cy="0" r="5" fill="#374151" />

        {/* String */}
        <line x1="0" y1="0" x2={pendulumX} y2={pendulumY} stroke="#6B7280" strokeWidth="2" />

        {/* Bob */}
        <circle cx={pendulumX} cy={pendulumY} r="15" fill="#3B82F6" />

        {/* Equilibrium line */}
        <line x1="0" y1="0" x2="0" y2={length * 100} stroke="#E5E7EB" strokeWidth="1" strokeDasharray="5,5" />

        {/* Angle arc */}
        <path
          d={`M 0 30 A 30 30 0 0 ${pendulumX > 0 ? 1 : 0} ${Math.sin(angleRad) * 30} ${Math.cos(angleRad) * 30}`}
          fill="none"
          stroke="#10B981"
          strokeWidth="2"
        />
      </svg>

      <div className="grid grid-cols-4 gap-2 text-center text-sm">
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-500">Time</div>
          <div className="font-mono">{time.toFixed(2)}s</div>
        </div>
        <div className="bg-blue-50 p-2 rounded">
          <div className="text-gray-500">Period</div>
          <div className="font-mono">{period.toFixed(2)}s</div>
        </div>
        <div className="bg-red-50 p-2 rounded">
          <div className="text-gray-500">KE</div>
          <div className="font-mono">{(KE * 100).toFixed(0)}%</div>
        </div>
        <div className="bg-green-50 p-2 rounded">
          <div className="text-gray-500">PE</div>
          <div className="font-mono">{(PE * 100).toFixed(0)}%</div>
        </div>
      </div>

      <div className="bg-blue-50 p-3 rounded text-sm text-center">
        <strong>Period:</strong> T = 2pi * sqrt(L/g) - independent of mass and amplitude (for small angles)
      </div>
    </div>
  )
}

// Lagrangian Visualization
function LagrangianViz() {
  const [position, setPosition] = useState(0)
  const [velocity, setVelocity] = useState(2)
  const [mass, setMass] = useState(1)
  const [springK, setSpringK] = useState(1)

  const KE = 0.5 * mass * velocity ** 2
  const PE = 0.5 * springK * position ** 2
  const L = KE - PE
  const E = KE + PE

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Position x = {position}</label>
          <input
            type="range"
            min="-3"
            max="3"
            step="0.5"
            value={position}
            onChange={(e) => setPosition(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Velocity v = {velocity}</label>
          <input
            type="range"
            min="0"
            max="5"
            step="0.5"
            value={velocity}
            onChange={(e) => setVelocity(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Mass m = {mass}</label>
          <input
            type="range"
            min="0.5"
            max="3"
            step="0.5"
            value={mass}
            onChange={(e) => setMass(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Spring k = {springK}</label>
          <input
            type="range"
            min="0.5"
            max="3"
            step="0.5"
            value={springK}
            onChange={(e) => setSpringK(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <svg viewBox="-4 -0.5 8 5" className="w-full max-w-lg mx-auto bg-white border border-gray-200 rounded">
        {/* Horizontal axis */}
        <line x1="-3.5" y1="4" x2="3.5" y2="4" stroke="#9CA3AF" strokeWidth="0.03" />

        {/* Wall */}
        <rect x="-3.7" y="2.5" width="0.2" height="2" fill="#374151" />

        {/* Spring (zigzag) */}
        <path
          d={`M -3.5 3.5 ${Array.from({length: 10}, (_, i) =>
            `L ${-3.5 + (3.5 + position) * (i + 0.5) / 10} ${3.5 + (i % 2 === 0 ? 0.3 : -0.3)}`
          ).join(' ')} L ${position} 3.5`}
          fill="none"
          stroke="#6B7280"
          strokeWidth="0.05"
        />

        {/* Mass */}
        <rect x={position - 0.3} y="3.2" width="0.6" height="0.6" fill="#3B82F6" rx="0.05" />

        {/* Velocity arrow */}
        {velocity > 0 && (
          <g>
            <line x1={position + 0.4} y1="3.5" x2={position + 0.4 + velocity * 0.3} y2="3.5" stroke="#EF4444" strokeWidth="0.08" />
            <polygon points={`${position + 0.4 + velocity * 0.3},3.5 ${position + 0.2 + velocity * 0.3},3.4 ${position + 0.2 + velocity * 0.3},3.6`} fill="#EF4444" />
          </g>
        )}

        {/* Energy bar chart */}
        <rect x="-3" y={2 - KE * 0.3} width="0.8" height={KE * 0.3} fill="#EF4444" />
        <rect x="-1.6" y={2 - PE * 0.3} width="0.8" height={PE * 0.3} fill="#10B981" />
        <rect x="-0.2" y={2 - L * 0.3} width="0.8" height={Math.abs(L) * 0.3} fill={L >= 0 ? "#8B5CF6" : "#F97316"} />
        <rect x="1.2" y={2 - E * 0.3} width="0.8" height={E * 0.3} fill="#3B82F6" />

        {/* Labels */}
        <text x="-2.6" y="2.3" fontSize="0.25" fill="#6B7280" textAnchor="middle">KE</text>
        <text x="-1.2" y="2.3" fontSize="0.25" fill="#6B7280" textAnchor="middle">PE</text>
        <text x="0.2" y="2.3" fontSize="0.25" fill="#6B7280" textAnchor="middle">L</text>
        <text x="1.6" y="2.3" fontSize="0.25" fill="#6B7280" textAnchor="middle">E</text>
      </svg>

      <div className="grid grid-cols-4 gap-2 text-center text-sm">
        <div className="bg-red-50 p-2 rounded border border-red-200">
          <div className="text-red-600 text-xs">KE = (1/2)mv^2</div>
          <div className="font-mono text-red-700">{KE.toFixed(2)}</div>
        </div>
        <div className="bg-green-50 p-2 rounded border border-green-200">
          <div className="text-green-600 text-xs">PE = (1/2)kx^2</div>
          <div className="font-mono text-green-700">{PE.toFixed(2)}</div>
        </div>
        <div className="bg-purple-50 p-2 rounded border border-purple-200">
          <div className="text-purple-600 text-xs">L = KE - PE</div>
          <div className="font-mono text-purple-700">{L.toFixed(2)}</div>
        </div>
        <div className="bg-blue-50 p-2 rounded border border-blue-200">
          <div className="text-blue-600 text-xs">E = KE + PE</div>
          <div className="font-mono text-blue-700">{E.toFixed(2)}</div>
        </div>
      </div>
    </div>
  )
}

// Phase Space Visualization
function PhaseSpaceViz() {
  const [energy, setEnergy] = useState(2)
  const [currentPoint, setCurrentPoint] = useState({ x: 1, p: 1 })

  // For harmonic oscillator: E = (1/2)p^2 + (1/2)x^2
  // Trajectory is an ellipse: x^2 + p^2 = 2E
  const radius = Math.sqrt(2 * energy)

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Total Energy E = {energy.toFixed(1)}
        </label>
        <input
          type="range"
          min="0.5"
          max="4"
          step="0.5"
          value={energy}
          onChange={(e) => setEnergy(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="-4 -4 8 8" className="w-full max-w-sm mx-auto bg-white border border-gray-200 rounded">
        {/* Grid */}
        <defs>
          <pattern id="phaseGrid" width="1" height="1" patternUnits="userSpaceOnUse">
            <path d="M 1 0 L 0 0 0 1" fill="none" stroke="#E5E7EB" strokeWidth="0.02" />
          </pattern>
        </defs>
        <rect x="-4" y="-4" width="8" height="8" fill="url(#phaseGrid)" />

        {/* Axes */}
        <line x1="-3.5" y1="0" x2="3.5" y2="0" stroke="#9CA3AF" strokeWidth="0.05" />
        <line x1="0" y1="-3.5" x2="0" y2="3.5" stroke="#9CA3AF" strokeWidth="0.05" />

        {/* Labels */}
        <text x="3.3" y="0.4" fontSize="0.4" fill="#6B7280">x</text>
        <text x="0.2" y="-3.2" fontSize="0.4" fill="#6B7280">p</text>

        {/* Phase space trajectory (ellipse for harmonic oscillator) */}
        <circle cx="0" cy="0" r={radius} fill="none" stroke="#3B82F6" strokeWidth="0.08" />

        {/* Direction arrows */}
        <path d={`M ${radius * 0.7} ${-radius * 0.7} l 0.2 -0.1`} stroke="#3B82F6" strokeWidth="0.08" fill="none" markerEnd="url(#arrow)" />

        {/* Current point */}
        <circle
          cx={currentPoint.x}
          cy={-currentPoint.p}
          r="0.2"
          fill="#EF4444"
          className="cursor-pointer"
        />

        {/* Flow direction indicator */}
        <text x={radius * 0.8} y={-radius * 0.1} fontSize="0.3" fill="#3B82F6">clockwise</text>
      </svg>

      <div className="grid grid-cols-2 gap-3 text-center text-sm">
        <div className="bg-blue-50 p-3 rounded">
          <div className="text-gray-600 mb-1">Phase Space Trajectory</div>
          <div className="font-mono text-sm">x^2 + p^2 = 2E = {(2 * energy).toFixed(1)}</div>
        </div>
        <div className="bg-purple-50 p-3 rounded">
          <div className="text-gray-600 mb-1">Liouville's Theorem</div>
          <div className="text-sm">Phase space volume is conserved!</div>
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded text-sm">
        <strong>Key insight:</strong> In phase space (x, p), each point represents a complete state.
        The trajectory never crosses itself (determinism) and the area is conserved.
      </div>
    </div>
  )
}

export default function ClassicalMechanicsPage() {
  return (
    <DocumentLayout
      title="Classical Mechanics"
      description="Lagrangian and Hamiltonian formulations, the foundation for all physics"
      phase="physics"
      currentIndex={10}
      prevLink={{ href: '/office-hours/math/07-index-theory', title: 'Index Theory' }}
      nextLink={{ href: '/office-hours/physics/01-special-relativity', title: 'Special Relativity' }}
    >
      <Section title="1. From Newton to Lagrange">
        <p className="text-gray-700 mb-4">
          Newton gave us <strong>F = ma</strong>, but there's a more powerful formulation.
          The <strong>Lagrangian approach</strong> starts from a single function and derives all equations of motion.
        </p>

        <Formula label="The Lagrangian">
          L = T - V = (Kinetic Energy) - (Potential Energy)
        </Formula>

        <KeyPoint>
          <strong>The Principle of Least Action:</strong> Nature chooses the path that minimizes (or extremizes) the action S = integral of L dt.
          This single principle generates all of classical mechanics!
        </KeyPoint>

        <SubSection title="Euler-Lagrange Equations">
          <p className="text-gray-700 mb-4">
            From the principle of least action, we derive:
          </p>
          <Formula label="Euler-Lagrange Equation">
            d/dt (partial L / partial q-dot) - partial L / partial q = 0
          </Formula>
          <p className="text-gray-700 mt-4">
            This single equation replaces all of Newton's laws for any coordinate system!
          </p>
        </SubSection>
      </Section>

      <Section title="2. The Simple Harmonic Oscillator">
        <p className="text-gray-700 mb-4">
          The pendulum (for small angles) and the spring-mass system are both examples of
          <strong> simple harmonic motion</strong> - the most fundamental oscillating system in physics.
        </p>

        <InteractiveBox title="Pendulum Oscillator">
          <PendulumViz />
        </InteractiveBox>

        <SubSection title="Why Oscillators Matter">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
            <div className="bg-gray-50 p-3 rounded">
              <strong>Near any minimum</strong>
              <div className="text-sm text-gray-600">Every stable equilibrium looks like a harmonic oscillator locally</div>
            </div>
            <div className="bg-blue-50 p-3 rounded border border-blue-200">
              <strong>Quantum field theory</strong>
              <div className="text-sm text-gray-600">Free fields are infinite collections of oscillators!</div>
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="3. The Lagrangian">
        <p className="text-gray-700 mb-4">
          The Lagrangian L = T - V encodes all the dynamics. For a harmonic oscillator:
        </p>

        <Formula>
          L = (1/2)m*v^2 - (1/2)k*x^2
        </Formula>

        <InteractiveBox title="Lagrangian for Harmonic Oscillator">
          <LagrangianViz />
        </InteractiveBox>

        <KeyPoint>
          Notice that the <strong>Lagrangian is NOT the total energy</strong>. It's the difference T - V.
          The total energy E = T + V is conserved, but L oscillates between positive and negative values.
        </KeyPoint>
      </Section>

      <Section title="4. The Hamiltonian and Phase Space">
        <p className="text-gray-700 mb-4">
          The <strong>Hamiltonian</strong> approach uses position q and momentum p as coordinates:
        </p>

        <Formula label="Legendre Transform">
          H(q, p) = p * q-dot - L(q, q-dot)
        </Formula>

        <p className="text-gray-700 my-4">
          For many systems, H equals the total energy. The equations of motion become symmetric:
        </p>

        <Formula label="Hamilton's Equations">
          dq/dt = partial H / partial p,  dp/dt = - partial H / partial q
        </Formula>

        <InteractiveBox title="Phase Space Trajectories">
          <PhaseSpaceViz />
        </InteractiveBox>

        <SubSection title="Poisson Brackets">
          <p className="text-gray-700 mb-4">
            Time evolution is generated by the Hamiltonian via Poisson brackets:
          </p>
          <Formula>
            df/dt = {'{f, H}'} = (partial f / partial q)(partial H / partial p) - (partial f / partial p)(partial H / partial q)
          </Formula>
          <p className="text-gray-700 mt-4">
            This structure directly maps to quantum mechanics: {'{,}'} becomes [,]/ih-bar!
          </p>
        </SubSection>
      </Section>

      <Section title="5. Symmetry and Conservation">
        <p className="text-gray-700 mb-4">
          <strong>Noether's Theorem</strong>: Every continuous symmetry corresponds to a conserved quantity.
        </p>

        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2 text-left">Symmetry</th>
                <th className="border border-gray-200 p-2 text-left">Conserved Quantity</th>
                <th className="border border-gray-200 p-2 text-left">Generator</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2">Time translation</td>
                <td className="border border-gray-200 p-2">Energy</td>
                <td className="border border-gray-200 p-2 font-mono">H</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Space translation</td>
                <td className="border border-gray-200 p-2">Momentum</td>
                <td className="border border-gray-200 p-2 font-mono">p</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Rotation</td>
                <td className="border border-gray-200 p-2">Angular momentum</td>
                <td className="border border-gray-200 p-2 font-mono">L</td>
              </tr>
              <tr className="bg-purple-50">
                <td className="border border-gray-200 p-2">Gauge symmetry</td>
                <td className="border border-gray-200 p-2">Charge</td>
                <td className="border border-gray-200 p-2 font-mono">Q</td>
              </tr>
            </tbody>
          </table>
        </div>

        <Z2Connection
          formula="Symmetry <-> Conservation"
          description="This deep connection underlies all of physics, including gauge theories"
        />
      </Section>

      <Section title="6. Connection to Z^2 Framework">
        <p className="text-gray-700 mb-4">
          Classical mechanics provides the foundation for understanding the Z^2 framework:
        </p>

        <div className="space-y-3">
          <Z2Connection
            formula="S = integral L dt"
            description="The action principle extends to field theory and strings"
          />
          <Z2Connection
            formula="{q, p} = 1"
            description="Poisson brackets become commutators [q, p] = ih-bar in quantum mechanics"
          />
          <Z2Connection
            formula="Phase space volume"
            description="Liouville's theorem connects to unitarity in quantum mechanics"
          />
        </div>

        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Classical Mechanics Matters for Z^2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>* <strong>Lagrangian formulation:</strong> Extends to quantum field theory via path integrals</li>
            <li>* <strong>Hamiltonian structure:</strong> Essential for canonical quantization</li>
            <li>* <strong>Symmetries:</strong> Gauge symmetries determine the Standard Model</li>
            <li>* <strong>Phase space:</strong> Becomes Hilbert space in quantum mechanics</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Derive the equation of motion for a simple pendulum using the Euler-Lagrange equation.</li>
          <li>Show that for a free particle, the Hamiltonian equals the kinetic energy.</li>
          <li>Verify that {'{q, p}'} = 1 using the definition of Poisson brackets.</li>
          <li>For V(x) = (1/2)kx^2, find the phase space trajectory and show it's an ellipse.</li>
          <li>Use Noether's theorem to show that if L doesn't depend on x, momentum is conserved.</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
