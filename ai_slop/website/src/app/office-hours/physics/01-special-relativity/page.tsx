'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Time Dilation Calculator
function TimeDilationViz() {
  const [velocity, setVelocity] = useState(0.5) // as fraction of c

  const gamma = 1 / Math.sqrt(1 - velocity ** 2)
  const properTime = 1 // 1 second in rest frame
  const dilatedTime = gamma * properTime

  // Visualization of moving clock
  const clockAngle = (Date.now() / 1000) % 1 * 360 // actual animation would need useEffect

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Velocity: v = {(velocity * 100).toFixed(0)}% of c = {(velocity * 299792).toFixed(0)} km/s
        </label>
        <input
          type="range"
          min="0"
          max="0.99"
          step="0.01"
          value={velocity}
          onChange={(e) => setVelocity(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Stationary observer's clock */}
        <div className="text-center">
          <div className="text-sm text-gray-600 mb-2">Your clock (at rest)</div>
          <svg viewBox="-50 -50 100 100" className="w-32 h-32 mx-auto">
            <circle cx="0" cy="0" r="45" fill="white" stroke="#3B82F6" strokeWidth="3" />
            <line x1="0" y1="0" x2="0" y2="-35" stroke="#1F2937" strokeWidth="3" strokeLinecap="round" />
            <circle cx="0" cy="0" r="4" fill="#1F2937" />
          </svg>
          <div className="font-mono text-lg mt-2">1.00 second</div>
        </div>

        {/* Moving observer's clock */}
        <div className="text-center">
          <div className="text-sm text-gray-600 mb-2">Moving clock (v = {(velocity * 100).toFixed(0)}% c)</div>
          <svg viewBox="-50 -50 100 100" className="w-32 h-32 mx-auto">
            <ellipse cx="0" cy="0" rx={45 * Math.sqrt(1 - velocity ** 2)} ry="45" fill="white" stroke="#EF4444" strokeWidth="3" />
            <line x1="0" y1="0" x2="0" y2="-35" stroke="#1F2937" strokeWidth="3" strokeLinecap="round" />
            <circle cx="0" cy="0" r="4" fill="#1F2937" />
          </svg>
          <div className="font-mono text-lg mt-2">{(1/gamma).toFixed(3)} seconds</div>
          <div className="text-xs text-gray-500">(appears to run slower)</div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="text-blue-600 text-xs">Lorentz Factor</div>
          <div className="font-mono text-xl text-blue-700">gamma = {gamma.toFixed(3)}</div>
        </div>
        <div className="bg-purple-50 p-3 rounded border border-purple-200">
          <div className="text-purple-600 text-xs">Time Dilation</div>
          <div className="font-mono text-purple-700">Delta t = gamma * Delta tau</div>
        </div>
        <div className="bg-green-50 p-3 rounded border border-green-200">
          <div className="text-green-600 text-xs">Proper Time</div>
          <div className="font-mono text-green-700">tau = t/gamma</div>
        </div>
      </div>

      {velocity > 0.9 && (
        <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
          <strong>Near light speed!</strong> At v = 99% c, gamma ~ 7, meaning 1 year of travel = 7 years on Earth.
          This is how muons created in the atmosphere reach the ground!
        </div>
      )}
    </div>
  )
}

// Length Contraction Visualization
function LengthContractionViz() {
  const [velocity, setVelocity] = useState(0.6)

  const gamma = 1 / Math.sqrt(1 - velocity ** 2)
  const properLength = 100 // meters
  const contractedLength = properLength / gamma

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Velocity: v = {(velocity * 100).toFixed(0)}% of c
        </label>
        <input
          type="range"
          min="0"
          max="0.99"
          step="0.01"
          value={velocity}
          onChange={(e) => setVelocity(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="0 0 300 120" className="w-full max-w-lg mx-auto bg-white border border-gray-200 rounded">
        {/* Rest frame object */}
        <text x="150" y="20" fontSize="12" textAnchor="middle" fill="#6B7280">Object at rest (proper length = 100m)</text>
        <rect x="50" y="30" width="200" height="30" fill="#3B82F6" rx="3" />
        <text x="150" y="50" fontSize="14" textAnchor="middle" fill="white" fontWeight="bold">L0 = 100m</text>

        {/* Moving frame object */}
        <text x="150" y="85" fontSize="12" textAnchor="middle" fill="#6B7280">Same object moving at v = {(velocity * 100).toFixed(0)}% c</text>
        <rect x={150 - contractedLength} y="95" width={contractedLength * 2} height="30" fill="#EF4444" rx="3" />
        <text x="150" y="115" fontSize="12" textAnchor="middle" fill="white" fontWeight="bold">
          L = {contractedLength.toFixed(1)}m
        </text>

        {/* Motion arrow */}
        <path d="M 260 110 L 280 110 L 275 105 M 280 110 L 275 115" stroke="#EF4444" strokeWidth="2" fill="none" />
        <text x="270" y="100" fontSize="10" fill="#EF4444">v</text>
      </svg>

      <div className="grid grid-cols-2 gap-3 text-center">
        <div className="bg-blue-50 p-3 rounded">
          <div className="text-sm text-gray-600">Length Contraction Formula</div>
          <div className="font-mono mt-1">L = L0 / gamma = L0 * sqrt(1 - v^2/c^2)</div>
        </div>
        <div className="bg-purple-50 p-3 rounded">
          <div className="text-sm text-gray-600">Contraction Factor</div>
          <div className="font-mono mt-1">L/L0 = {(1/gamma).toFixed(3)} = {((1/gamma) * 100).toFixed(1)}%</div>
        </div>
      </div>

      <KeyPoint>
        <strong>Only the direction of motion contracts!</strong> Lengths perpendicular to motion are unchanged.
        This is why we get ellipses, not smaller spheres.
      </KeyPoint>
    </div>
  )
}

// Light Cone Visualization
function LightConeViz() {
  const [eventX, setEventX] = useState(0)
  const [eventT, setEventT] = useState(0)

  // Determine causal relationship
  const interval = eventT ** 2 - eventX ** 2
  let causalType = ''
  let causalColor = ''
  if (Math.abs(interval) < 0.1) {
    causalType = 'Lightlike (null)'
    causalColor = 'text-yellow-600'
  } else if (interval > 0) {
    causalType = 'Timelike (causal)'
    causalColor = 'text-green-600'
  } else {
    causalType = 'Spacelike (no causal connection)'
    causalColor = 'text-red-600'
  }

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Space coordinate x = {eventX}
          </label>
          <input
            type="range"
            min="-3"
            max="3"
            step="0.5"
            value={eventX}
            onChange={(e) => setEventX(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Time coordinate t = {eventT}
          </label>
          <input
            type="range"
            min="-3"
            max="3"
            step="0.5"
            value={eventT}
            onChange={(e) => setEventT(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <svg viewBox="-4 -4 8 8" className="w-full max-w-sm mx-auto bg-gray-900 border border-gray-700 rounded">
        {/* Future light cone */}
        <polygon points="0,0 -3.5,-3.5 0,-3.5 3.5,-3.5" fill="rgba(34, 197, 94, 0.2)" />
        {/* Past light cone */}
        <polygon points="0,0 -3.5,3.5 0,3.5 3.5,3.5" fill="rgba(34, 197, 94, 0.2)" />

        {/* Spacelike regions */}
        <polygon points="0,0 -3.5,-3.5 -3.5,0 -3.5,3.5" fill="rgba(239, 68, 68, 0.1)" />
        <polygon points="0,0 3.5,-3.5 3.5,0 3.5,3.5" fill="rgba(239, 68, 68, 0.1)" />

        {/* Light cone edges */}
        <line x1="-3.5" y1="-3.5" x2="3.5" y2="3.5" stroke="#FBBF24" strokeWidth="0.08" />
        <line x1="3.5" y1="-3.5" x2="-3.5" y2="3.5" stroke="#FBBF24" strokeWidth="0.08" />

        {/* Axes */}
        <line x1="-3.5" y1="0" x2="3.5" y2="0" stroke="#6B7280" strokeWidth="0.05" />
        <line x1="0" y1="-3.5" x2="0" y2="3.5" stroke="#6B7280" strokeWidth="0.05" />

        {/* Labels */}
        <text x="3.2" y="0.4" fontSize="0.4" fill="#9CA3AF">x</text>
        <text x="0.2" y="-3.2" fontSize="0.4" fill="#9CA3AF">t</text>
        <text x="0.3" y="-2" fontSize="0.3" fill="#22C55E">Future</text>
        <text x="0.3" y="2.3" fontSize="0.3" fill="#22C55E">Past</text>
        <text x="2" y="0.3" fontSize="0.25" fill="#EF4444">Elsewhere</text>

        {/* Event point */}
        <circle cx={eventX} cy={-eventT} r="0.2" fill="#8B5CF6" stroke="white" strokeWidth="0.05" />

        {/* Origin */}
        <circle cx="0" cy="0" r="0.12" fill="white" />
      </svg>

      <div className="grid grid-cols-2 gap-3 text-center text-sm">
        <div className="bg-gray-800 text-white p-3 rounded">
          <div className="text-gray-400 text-xs">Spacetime Interval</div>
          <div className="font-mono">s^2 = t^2 - x^2 = {interval.toFixed(2)}</div>
        </div>
        <div className={`bg-gray-100 p-3 rounded ${causalColor}`}>
          <div className="text-gray-600 text-xs">Causal Relationship</div>
          <div className="font-medium">{causalType}</div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 text-xs">
        <div className="bg-green-50 p-2 rounded border border-green-200 text-center">
          <div className="text-green-700 font-medium">Timelike</div>
          <div className="text-green-600">s^2 &gt; 0: Events can be causally connected</div>
        </div>
        <div className="bg-yellow-50 p-2 rounded border border-yellow-200 text-center">
          <div className="text-yellow-700 font-medium">Lightlike</div>
          <div className="text-yellow-600">s^2 = 0: Connected by light ray</div>
        </div>
        <div className="bg-red-50 p-2 rounded border border-red-200 text-center">
          <div className="text-red-700 font-medium">Spacelike</div>
          <div className="text-red-600">s^2 &lt; 0: No causal connection possible</div>
        </div>
      </div>
    </div>
  )
}

export default function SpecialRelativityPage() {
  return (
    <DocumentLayout
      title="Special Relativity"
      description="Spacetime, Lorentz transformations, and the geometry of causality"
      phase="physics"
      currentIndex={11}
      prevLink={{ href: '/office-hours/physics/00-classical-mechanics', title: 'Classical Mechanics' }}
      nextLink={{ href: '/office-hours/physics/02-quantum-mechanics', title: 'Quantum Mechanics' }}
    >
      <Section title="1. Einstein's Postulates">
        <p className="text-gray-700 mb-4">
          Special relativity rests on two simple postulates that revolutionized our understanding of space and time:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div className="font-semibold text-blue-800 mb-2">1. Principle of Relativity</div>
            <p className="text-sm text-gray-700">
              The laws of physics are the same in all inertial reference frames.
              No experiment can detect "absolute motion."
            </p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
            <div className="font-semibold text-purple-800 mb-2">2. Constancy of Light Speed</div>
            <p className="text-sm text-gray-700">
              The speed of light c is the same for all observers, regardless of the motion of the source.
            </p>
          </div>
        </div>

        <KeyPoint>
          These two postulates seem contradictory with Newtonian physics. The resolution requires
          abandoning absolute time and absolute simultaneity!
        </KeyPoint>
      </Section>

      <Section title="2. Time Dilation">
        <p className="text-gray-700 mb-4">
          Moving clocks run slow! A clock moving at velocity v relative to you ticks slower by a factor gamma:
        </p>

        <Formula label="Lorentz Factor">
          gamma = 1 / sqrt(1 - v^2/c^2)
        </Formula>

        <InteractiveBox title="Time Dilation Calculator">
          <TimeDilationViz />
        </InteractiveBox>

        <SubSection title="The Twin Paradox">
          <p className="text-gray-700">
            If you travel to a star 10 light-years away at 0.99c, only about 1.4 years pass for you,
            but about 10 years pass on Earth! This is not symmetric: the traveling twin accelerates
            and decelerates, breaking the symmetry.
          </p>
        </SubSection>
      </Section>

      <Section title="3. Length Contraction">
        <p className="text-gray-700 mb-4">
          Objects contract along the direction of motion. A meter stick moving past you appears shorter:
        </p>

        <Formula>
          L = L0 / gamma = L0 * sqrt(1 - v^2/c^2)
        </Formula>

        <InteractiveBox title="Length Contraction">
          <LengthContractionViz />
        </InteractiveBox>
      </Section>

      <Section title="4. Spacetime and the Light Cone">
        <p className="text-gray-700 mb-4">
          Space and time are unified into <strong>spacetime</strong>. The light cone divides spacetime
          into causally connected and disconnected regions.
        </p>

        <InteractiveBox title="Light Cone and Causality">
          <LightConeViz />
        </InteractiveBox>

        <SubSection title="The Invariant Interval">
          <p className="text-gray-700 mb-4">
            While space and time separately depend on the observer, the <strong>spacetime interval</strong> is invariant:
          </p>
          <Formula label="Minkowski Metric">
            ds^2 = c^2 dt^2 - dx^2 - dy^2 - dz^2
          </Formula>
          <p className="text-gray-700 mt-4">
            This is the signature of <strong>Minkowski spacetime</strong> with metric signature (+,-,-,-).
          </p>
        </SubSection>
      </Section>

      <Section title="5. Lorentz Transformations">
        <p className="text-gray-700 mb-4">
          The transformations that preserve the spacetime interval are the <strong>Lorentz transformations</strong>:
        </p>

        <Formula label="Lorentz Boost in x-direction">
          t' = gamma(t - vx/c^2), x' = gamma(x - vt)
        </Formula>

        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2">Transformation</th>
                <th className="border border-gray-200 p-2">Matrix Form</th>
                <th className="border border-gray-200 p-2">Preserves</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2">Rotation (3D)</td>
                <td className="border border-gray-200 p-2 font-mono">SO(3)</td>
                <td className="border border-gray-200 p-2">Spatial distance</td>
              </tr>
              <tr className="bg-blue-50">
                <td className="border border-gray-200 p-2">Boost</td>
                <td className="border border-gray-200 p-2 font-mono">Hyperbolic rotation</td>
                <td className="border border-gray-200 p-2">Spacetime interval</td>
              </tr>
              <tr className="bg-purple-50">
                <td className="border border-gray-200 p-2">Full Lorentz</td>
                <td className="border border-gray-200 p-2 font-mono">SO(3,1)</td>
                <td className="border border-gray-200 p-2">Minkowski metric</td>
              </tr>
            </tbody>
          </table>
        </div>

        <Z2Connection
          formula="SO(3,1)"
          description="The Lorentz group has 4 disconnected components, related by P (parity) and T (time reversal)"
        />
      </Section>

      <Section title="6. Energy-Momentum Relation">
        <p className="text-gray-700 mb-4">
          The famous equation E = mc^2 is actually a special case of a more general relation:
        </p>

        <Formula label="Energy-Momentum Relation">
          E^2 = (pc)^2 + (mc^2)^2
        </Formula>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <div className="font-medium mb-1">Rest mass (p = 0)</div>
            <div className="font-mono text-sm">E = mc^2</div>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <div className="font-medium mb-1">Photon (m = 0)</div>
            <div className="font-mono text-sm">E = pc</div>
          </div>
        </div>

        <KeyPoint>
          Energy and momentum form a 4-vector (E/c, p). The "length" of this 4-vector is the rest mass:
          m^2 c^2 = E^2/c^2 - p^2
        </KeyPoint>
      </Section>

      <Section title="7. Connection to Z^2 Framework">
        <p className="text-gray-700 mb-4">
          Special relativity is the foundation of relativistic quantum field theory:
        </p>

        <div className="space-y-3">
          <Z2Connection
            formula="ds^2 = g_mu,nu dx^mu dx^nu"
            description="The Minkowski metric is the flat limit of curved spacetime in general relativity"
          />
          <Z2Connection
            formula="SO(3,1) -> Spin(3,1)"
            description="Spinors require the double cover of the Lorentz group"
          />
          <Z2Connection
            formula="CPT Theorem"
            description="All Lorentz-invariant QFTs are invariant under combined C, P, T"
          />
        </div>

        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Special Relativity Matters for Z^2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>* <strong>Causality:</strong> The light cone structure determines what can influence what</li>
            <li>* <strong>Lorentz invariance:</strong> All fundamental physics must respect this symmetry</li>
            <li>* <strong>Spinors:</strong> Fermions transform under the double cover Spin(3,1)</li>
            <li>* <strong>E = mc^2:</strong> Mass and energy are interchangeable in particle physics</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Calculate gamma for v = 0.6c and verify gamma = 1.25.</li>
          <li>A muon (lifetime 2.2 microseconds) travels at 0.99c. How far does it travel in the lab frame?</li>
          <li>Show that if s^2 &gt; 0, there exists a frame where the two events occur at the same place.</li>
          <li>Derive the velocity addition formula: u' = (u - v)/(1 - uv/c^2).</li>
          <li>Verify that the Lorentz transformation preserves ds^2.</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
