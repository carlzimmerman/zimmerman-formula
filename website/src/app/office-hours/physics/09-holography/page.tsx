'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// AdS/CFT Visualization
function AdSCFTViz() {
  const [radialPosition, setRadialPosition] = useState(0.5)
  const [showBulk, setShowBulk] = useState(true)

  // Energy scale corresponding to radial position
  const energyScale = Math.pow(10, 3 * (1 - radialPosition)) // Higher r = lower E

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gray-900 rounded-lg">
        {/* AdS bulk (represented as interior) */}
        {showBulk && (
          <g>
            {/* Concentric circles representing radial slices */}
            {[0.2, 0.4, 0.6, 0.8, 1].map((r, i) => (
              <circle
                key={i}
                cx="150"
                cy="100"
                r={r * 80}
                fill="none"
                stroke="#4ADE80"
                strokeWidth="0.5"
                opacity={0.3 + r * 0.5}
              />
            ))}

            {/* Radial lines */}
            {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => {
              const rad = (angle * Math.PI) / 180
              return (
                <line
                  key={i}
                  x1="150"
                  y1="100"
                  x2={150 + 80 * Math.cos(rad)}
                  y2={100 + 80 * Math.sin(rad)}
                  stroke="#4ADE80"
                  strokeWidth="0.5"
                  opacity="0.3"
                />
              )
            })}
          </g>
        )}

        {/* Boundary (CFT lives here) */}
        <circle
          cx="150"
          cy="100"
          r="80"
          fill="none"
          stroke="#8B5CF6"
          strokeWidth="3"
        />
        <text x="250" y="100" fontSize="10" fill="#8B5CF6">CFT (boundary)</text>

        {/* Current radial position */}
        <circle
          cx="150"
          cy="100"
          r={radialPosition * 80}
          fill="none"
          stroke="#F59E0B"
          strokeWidth="2"
          strokeDasharray="4,2"
        />

        {/* Point at current position */}
        <circle
          cx={150 + radialPosition * 80}
          cy={100}
          r="6"
          fill="#F59E0B"
        />

        {/* Labels */}
        <text x="150" y="195" textAnchor="middle" fontSize="10" fill="#9CA3AF">
          AdS bulk (gravity)
        </text>
        <text x="150" y="100" textAnchor="middle" fontSize="10" fill="#4ADE80">
          r = {radialPosition.toFixed(2)}
        </text>
      </svg>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Radial position: r = {radialPosition.toFixed(2)}
        </label>
        <input
          type="range"
          min="0.05"
          max="0.95"
          step="0.05"
          value={radialPosition}
          onChange={(e) => setRadialPosition(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={showBulk}
          onChange={(e) => setShowBulk(e.target.checked)}
          className="rounded"
        />
        <label className="text-sm text-gray-600">Show bulk geometry</label>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-purple-50 p-3 rounded border border-purple-200 text-center">
          <div className="text-sm text-gray-500">Boundary (r = 1)</div>
          <div className="font-bold text-purple-600">UV (high energy)</div>
          <div className="text-xs text-gray-500">CFT lives here</div>
        </div>
        <div className="bg-green-50 p-3 rounded border border-green-200 text-center">
          <div className="text-sm text-gray-500">Interior (r = 0)</div>
          <div className="font-bold text-green-600">IR (low energy)</div>
          <div className="text-xs text-gray-500">Deep bulk = IR physics</div>
        </div>
      </div>

      <div className="bg-blue-50 p-3 rounded border border-blue-200 text-sm">
        <strong>Current position (r = {radialPosition.toFixed(2)}):</strong>
        <br />
        Corresponds to energy scale E ~ {energyScale.toFixed(0)} GeV
      </div>
    </div>
  )
}

// Holographic RG Flow Visualization
function RGFlowViz() {
  const [flowParameter, setFlowParameter] = useState(0.5)

  // Coupling constants along the flow
  const g_UV = 0.1
  const g_IR = 0.8
  const g_current = g_UV + (g_IR - g_UV) * flowParameter

  // Beta function visualization
  const generateBetaFunction = () => {
    const points = []
    for (let i = 0; i <= 100; i++) {
      const g = i / 100
      // Simple beta function with UV and IR fixed points
      const beta = g * (1 - g) * (g - 0.5) * 4
      points.push({ x: 30 + g * 240, y: 100 - beta * 80 })
    }
    return points
  }

  const betaPoints = generateBetaFunction()

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Axes */}
        <line x1="30" y1="100" x2="280" y2="100" stroke="#9CA3AF" strokeWidth="1" />
        <line x1="30" y1="180" x2="30" y2="20" stroke="#9CA3AF" strokeWidth="1" />
        <text x="155" y="195" textAnchor="middle" fontSize="10" fill="#6B7280">Coupling g</text>
        <text x="20" y="60" textAnchor="middle" fontSize="10" fill="#6B7280" transform="rotate(-90 20,60)">Beta(g)</text>

        {/* Beta function curve */}
        <path
          d={betaPoints.map((p, i) => (i === 0 ? `M ${p.x},${p.y}` : `L ${p.x},${p.y}`)).join(' ')}
          fill="none"
          stroke="#3B82F6"
          strokeWidth="2"
        />

        {/* Fixed points */}
        <circle cx="30" cy="100" r="6" fill="#10B981" stroke="#059669" strokeWidth="2" />
        <text x="30" y="120" textAnchor="middle" fontSize="8" fill="#10B981">UV (g=0)</text>

        <circle cx="270" cy="100" r="6" fill="#EF4444" stroke="#DC2626" strokeWidth="2" />
        <text x="270" y="120" textAnchor="middle" fontSize="8" fill="#EF4444">IR (g=1)</text>

        <circle cx="150" cy="100" r="5" fill="#8B5CF6" stroke="#7C3AED" strokeWidth="2" />
        <text x="150" y="85" textAnchor="middle" fontSize="8" fill="#8B5CF6">saddle</text>

        {/* Flow arrows */}
        {[0.2, 0.4, 0.7, 0.9].map((g, i) => {
          const beta = g * (1 - g) * (g - 0.5) * 4
          const x = 30 + g * 240
          const direction = beta > 0 ? 1 : -1
          return (
            <g key={i}>
              <line
                x1={x}
                y1="100"
                x2={x + direction * 15}
                y2="100"
                stroke="#F59E0B"
                strokeWidth="2"
              />
              <polygon
                points={`${x + direction * 20},100 ${x + direction * 12},95 ${x + direction * 12},105`}
                fill="#F59E0B"
              />
            </g>
          )
        })}

        {/* Current position on flow */}
        <circle
          cx={30 + g_current * 240}
          cy="100"
          r="8"
          fill="#F59E0B"
          stroke="#D97706"
          strokeWidth="2"
        />
      </svg>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          RG flow parameter (UV to IR): {flowParameter.toFixed(2)}
        </label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={flowParameter}
          onChange={(e) => setFlowParameter(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="grid grid-cols-3 gap-3 text-center text-sm">
        <div className="bg-green-50 p-2 rounded border border-green-200">
          <div className="font-medium text-green-700">UV Fixed Point</div>
          <div className="text-xs text-gray-500">g = 0, free theory</div>
        </div>
        <div className="bg-amber-50 p-2 rounded border border-amber-200">
          <div className="font-medium text-amber-700">Current: g = {g_current.toFixed(2)}</div>
          <div className="text-xs text-gray-500">Flowing...</div>
        </div>
        <div className="bg-red-50 p-2 rounded border border-red-200">
          <div className="font-medium text-red-700">IR Fixed Point</div>
          <div className="text-xs text-gray-500">g = 1, strongly coupled</div>
        </div>
      </div>
    </div>
  )
}

// IR Fixed Point Visualization
function IRFixedPointViz() {
  const [showFlow, setShowFlow] = useState(true)

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gray-900 rounded-lg">
        {/* AdS bulk with flow lines */}
        <circle cx="150" cy="100" r="80" fill="none" stroke="#8B5CF6" strokeWidth="2" />

        {/* IR fixed point at center */}
        <circle cx="150" cy="100" r="15" fill="#EF4444" stroke="#DC2626" strokeWidth="2" />
        <text x="150" y="104" textAnchor="middle" fontSize="10" fill="white" fontWeight="bold">IR</text>

        {/* Flow lines from boundary to center */}
        {showFlow && [0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => {
          const rad = (angle * Math.PI) / 180
          const startX = 150 + 80 * Math.cos(rad)
          const startY = 100 + 80 * Math.sin(rad)
          const endX = 150 + 20 * Math.cos(rad)
          const endY = 100 + 20 * Math.sin(rad)

          // Spiral path
          const midX = 150 + 50 * Math.cos(rad + 0.3)
          const midY = 100 + 50 * Math.sin(rad + 0.3)

          return (
            <g key={i}>
              <path
                d={`M ${startX},${startY} Q ${midX},${midY} ${endX},${endY}`}
                fill="none"
                stroke="#4ADE80"
                strokeWidth="1.5"
                opacity="0.7"
              />
              {/* Arrowhead */}
              <circle cx={endX} cy={endY} r="3" fill="#4ADE80" />
            </g>
          )
        })}

        {/* UV label on boundary */}
        <text x="150" y="25" textAnchor="middle" fontSize="10" fill="#8B5CF6">UV (boundary)</text>

        {/* Legend */}
        <text x="150" y="190" textAnchor="middle" fontSize="9" fill="#9CA3AF">
          RG flow: UV (boundary) to IR (center)
        </text>
      </svg>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={showFlow}
          onChange={(e) => setShowFlow(e.target.checked)}
          className="rounded"
        />
        <label className="text-sm text-gray-600">Show RG flow lines</label>
      </div>

      <div className="bg-purple-50 p-4 rounded border border-purple-200">
        <h4 className="font-semibold text-purple-800 mb-2">Holographic RG Flow</h4>
        <ul className="text-sm text-gray-700 space-y-1">
          <li>- <strong>Boundary:</strong> UV CFT (high energy, short distances)</li>
          <li>- <strong>Moving inward:</strong> Integrating out high-energy modes</li>
          <li>- <strong>Center:</strong> IR fixed point (low energy physics)</li>
          <li>- <strong>Z2 connection:</strong> The IR fixed point determines low-energy observables!</li>
        </ul>
      </div>
    </div>
  )
}

export default function HolographyPage() {
  return (
    <DocumentLayout
      title="Holography and AdS/CFT"
      description="The holographic principle, AdS/CFT correspondence, and holographic RG"
      phase="physics"
      currentIndex={9}
      prevLink={{ href: '/office-hours/physics/08-string-theory', title: 'String Theory' }}
      nextLink={{ href: '/office-hours', title: 'Office Hours Home' }}
    >
      <Section title="1. The Holographic Principle">
        <p className="text-gray-700 mb-4">
          The <strong>holographic principle</strong> states that all information in a volume of space
          can be encoded on its boundary. A theory of gravity in (d+1) dimensions is equivalent
          to a non-gravitational theory in d dimensions!
        </p>

        <div className="grid grid-cols-2 gap-4 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <strong>Bulk (interior):</strong>
            <div className="text-sm text-gray-600">
              Gravity, strings, extra dimensions
            </div>
          </div>
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <strong>Boundary:</strong>
            <div className="text-sm text-purple-600">
              Quantum field theory, no gravity
            </div>
          </div>
        </div>

        <KeyPoint>
          Holography suggests that spacetime itself may be emergent!
          Gravity in the bulk = strongly coupled QFT on the boundary.
        </KeyPoint>
      </Section>

      <Section title="2. AdS/CFT Correspondence">
        <p className="text-gray-700 mb-4">
          The <strong>AdS/CFT correspondence</strong> (Maldacena, 1997) is the most concrete
          realization of holography. It relates:
        </p>

        <Formula label="AdS/CFT">
          Type IIB on AdS_5 x S^5 = N=4 SYM in 4D
        </Formula>

        <InteractiveBox title="AdS/CFT Geometry">
          <AdSCFTViz />
        </InteractiveBox>

        <SubSection title="The Dictionary">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">Bulk (Gravity)</th>
                  <th className="border border-gray-200 p-2">Boundary (CFT)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2">Radial coordinate r</td>
                  <td className="border border-gray-200 p-2">Energy scale E</td>
                </tr>
                <tr className="bg-blue-50">
                  <td className="border border-gray-200 p-2">Bulk field phi(r, x)</td>
                  <td className="border border-gray-200 p-2">Operator O(x)</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Field mass m</td>
                  <td className="border border-gray-200 p-2">Operator dimension Delta</td>
                </tr>
                <tr className="bg-purple-50">
                  <td className="border border-gray-200 p-2">Graviton</td>
                  <td className="border border-gray-200 p-2">Stress tensor T_uv</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Black hole</td>
                  <td className="border border-gray-200 p-2">Thermal state (temperature)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>
      </Section>

      <Section title="3. Holographic Renormalization Group">
        <p className="text-gray-700 mb-4">
          The radial direction in AdS corresponds to the <strong>RG scale</strong> in the CFT.
          Moving into the bulk = flowing to lower energies (IR).
        </p>

        <InteractiveBox title="RG Flow and Beta Functions">
          <RGFlowViz />
        </InteractiveBox>

        <SubSection title="UV to IR Flow">
          <div className="space-y-2 text-gray-700">
            <p>- <strong>UV (boundary):</strong> High energy, conformal fixed point</p>
            <p>- <strong>RG flow:</strong> Coupling constants evolve with scale</p>
            <p>- <strong>IR (deep bulk):</strong> Low energy, possibly new fixed point</p>
          </div>
        </SubSection>

        <Formula label="Holographic c-theorem">
          c_UV &gt;= c_IR (degrees of freedom decrease under RG)
        </Formula>
      </Section>

      <Section title="4. The IR Fixed Point">
        <p className="text-gray-700 mb-4">
          In the Z2 framework, the deep IR physics determines the cosmological constant
          and matter content. The <strong>IR fixed point</strong> is crucial!
        </p>

        <InteractiveBox title="Flow to IR Fixed Point">
          <IRFixedPointViz />
        </InteractiveBox>

        <KeyPoint>
          The Z2 framework uses holography to connect:
          <br />
          - UV physics: String theory on T^3/Z_2
          <br />
          - IR physics: 4D effective theory with Lambda = 13/19
        </KeyPoint>
      </Section>

      <Section title="5. Applications">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
          <div className="bg-gray-50 p-4 rounded">
            <h4 className="font-semibold text-gray-800 mb-2">Quark-Gluon Plasma</h4>
            <p className="text-sm text-gray-600">
              AdS/CFT predicts viscosity eta/s = 1/(4 pi), confirmed by RHIC experiments!
            </p>
          </div>
          <div className="bg-blue-50 p-4 rounded border border-blue-200">
            <h4 className="font-semibold text-blue-800 mb-2">Condensed Matter</h4>
            <p className="text-sm text-gray-600">
              Holographic superconductors and strange metals modeled via AdS/CFT.
            </p>
          </div>
          <div className="bg-purple-50 p-4 rounded border border-purple-200">
            <h4 className="font-semibold text-purple-800 mb-2">Quantum Information</h4>
            <p className="text-sm text-gray-600">
              Entanglement entropy = area of minimal surface (Ryu-Takayanagi).
            </p>
          </div>
          <div className="bg-green-50 p-4 rounded border border-green-200">
            <h4 className="font-semibold text-green-800 mb-2">Black Hole Information</h4>
            <p className="text-sm text-gray-600">
              Holography resolves the information paradox: info preserved on boundary.
            </p>
          </div>
        </div>
      </Section>

      <Section title="6. Connection to Z2 Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="AdS_5 x S^5 / Z_2"
            description="The near-horizon geometry of D3-branes includes the Z_2 orbifold"
          />
          <Z2Connection
            formula="Holographic RG"
            description="UV string theory flows to IR effective theory with predictable Lambda"
          />
          <Z2Connection
            formula="IR fixed point -> Lambda = 13/19"
            description="The deep IR physics determines the cosmological constant"
          />
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-green-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Holography Matters for Z2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>- <strong>UV/IR connection:</strong> High-energy string physics determines low-energy cosmos</li>
            <li>- <strong>Non-perturbative:</strong> Strong coupling accessible via gravity dual</li>
            <li>- <strong>Counting DOF:</strong> Holographic c-function counts degrees of freedom</li>
            <li>- <strong>Emergent spacetime:</strong> 4D spacetime may emerge from boundary theory</li>
          </ul>
        </div>
      </Section>

      <Section title="7. The Full Picture">
        <div className="bg-gray-900 text-white p-6 rounded-lg my-4">
          <h4 className="font-semibold text-xl mb-4 text-center">Z2 Framework: UV to IR</h4>
          <div className="flex items-center justify-between text-sm">
            <div className="text-center">
              <div className="text-purple-400 font-bold">UV</div>
              <div>Type IIB String</div>
              <div>10D gravity</div>
            </div>
            <div className="text-gray-500">---&gt;</div>
            <div className="text-center">
              <div className="text-blue-400 font-bold">Compactify</div>
              <div>T^3/Z_2 orbifold</div>
              <div>D3-branes</div>
            </div>
            <div className="text-gray-500">---&gt;</div>
            <div className="text-center">
              <div className="text-green-400 font-bold">Holography</div>
              <div>AdS/CFT</div>
              <div>RG flow</div>
            </div>
            <div className="text-gray-500">---&gt;</div>
            <div className="text-center">
              <div className="text-amber-400 font-bold">IR</div>
              <div>4D physics</div>
              <div>Lambda = 13/19</div>
            </div>
          </div>
        </div>

        <KeyPoint>
          The Z2 framework connects string theory in the UV to cosmology in the IR
          via holography. The result: a parameter-free prediction for dark energy!
        </KeyPoint>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Explain in your own words why the boundary of AdS corresponds to UV physics.</li>
          <li>The AdS_5 metric is ds^2 = (L^2/z^2)(dz^2 + dx^2). Where is the boundary? The interior?</li>
          <li>What is the CFT dual of a black hole in AdS?</li>
          <li>Why does the c-theorem say c_UV &gt;= c_IR? What happens to degrees of freedom?</li>
          <li>How does holography help understand strong coupling in QFT?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
