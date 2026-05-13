'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// String Modes Visualization
function StringModesViz() {
  const [mode, setMode] = useState(1)
  const [time, setTime] = useState(0)

  // Generate string shape for given mode
  const generateString = () => {
    const points = []
    for (let i = 0; i <= 100; i++) {
      const sigma = (i / 100) * Math.PI * 2 // Parameter along string
      const x = 50 + i * 2
      // Standing wave: sin(n*sigma) * cos(omega*t)
      const y = 100 - Math.sin(mode * sigma) * Math.cos(time * 0.1) * 30
      points.push({ x, y })
    }
    return points
  }

  const stringPoints = generateString()

  // Auto-advance time
  useState(() => {
    const interval = setInterval(() => {
      setTime(t => (t + 1) % 628)
    }, 50)
    return () => clearInterval(interval)
  })

  const particles = [
    { mode: 1, name: 'Graviton', spin: 2, mass: 0 },
    { mode: 2, name: 'Photon-like', spin: 1, mass: 0 },
    { mode: 3, name: 'Massive', spin: 0, mass: 'M_s' },
    { mode: 4, name: 'Heavy', spin: 1, mass: '2M_s' },
  ]

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Vibration mode n = {mode}
        </label>
        <input
          type="range"
          min="1"
          max="5"
          step="1"
          value={mode}
          onChange={(e) => setMode(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gray-900 rounded-lg">
        {/* String */}
        <path
          d={stringPoints.map((p, i) => (i === 0 ? `M ${p.x},${p.y}` : `L ${p.x},${p.y}`)).join(' ')}
          fill="none"
          stroke="#4ADE80"
          strokeWidth="3"
        />

        {/* Endpoints (for open string) */}
        <circle cx={stringPoints[0].x} cy={stringPoints[0].y} r="6" fill="#F59E0B" />
        <circle cx={stringPoints[100].x} cy={stringPoints[100].y} r="6" fill="#F59E0B" />

        {/* Mode label */}
        <text x="150" y="30" textAnchor="middle" fontSize="14" fill="#9CA3AF">
          n = {mode} mode
        </text>
        <text x="150" y="180" textAnchor="middle" fontSize="10" fill="#9CA3AF">
          Energy ~ n * M_string
        </text>
      </svg>

      <div className="grid grid-cols-4 gap-2">
        {particles.map((p, i) => (
          <div
            key={i}
            className={`p-2 rounded text-center text-xs ${
              mode === p.mode ? 'bg-green-100 border-2 border-green-400' : 'bg-gray-50'
            }`}
          >
            <div className="font-medium">{p.name}</div>
            <div className="text-gray-500">spin {p.spin}</div>
            <div className="text-gray-500">m = {p.mass}</div>
          </div>
        ))}
      </div>

      <div className="bg-blue-50 p-3 rounded border border-blue-200 text-sm">
        <strong>Key insight:</strong> Different vibration modes of the same string appear as
        different particles! The graviton is the lowest mode of a closed string.
      </div>
    </div>
  )
}

// D-Brane Visualization
function DBraneViz() {
  const [dimension, setDimension] = useState(3)
  const [showStrings, setShowStrings] = useState(true)

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          D{dimension}-brane (extends in {dimension} spatial dimensions)
        </label>
        <input
          type="range"
          min="0"
          max="9"
          step="1"
          value={dimension}
          onChange={(e) => setDimension(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gray-900 rounded-lg">
        {/* D-brane as a surface */}
        {dimension >= 2 ? (
          <g>
            {/* 2D surface representation */}
            <path
              d="M 50 150 L 150 50 L 250 80 L 180 170 Z"
              fill="#3B82F6"
              fillOpacity="0.3"
              stroke="#3B82F6"
              strokeWidth="2"
            />
            <text x="150" y="120" textAnchor="middle" fontSize="12" fill="#60A5FA">
              D{dimension}-brane
            </text>
          </g>
        ) : dimension === 1 ? (
          <g>
            {/* 1D line */}
            <line x1="50" y1="150" x2="250" y2="50" stroke="#3B82F6" strokeWidth="4" />
            <text x="150" y="120" textAnchor="middle" fontSize="12" fill="#60A5FA">
              D1-brane (string)
            </text>
          </g>
        ) : (
          <g>
            {/* 0D point */}
            <circle cx="150" cy="100" r="10" fill="#3B82F6" />
            <text x="150" y="130" textAnchor="middle" fontSize="12" fill="#60A5FA">
              D0-brane (particle)
            </text>
          </g>
        )}

        {/* Open strings attached to brane */}
        {showStrings && dimension >= 1 && (
          <g>
            <path
              d="M 100 120 Q 110 80, 130 90 Q 150 100, 140 110"
              fill="none"
              stroke="#4ADE80"
              strokeWidth="2"
            />
            <circle cx="100" cy="120" r="4" fill="#F59E0B" />
            <circle cx="140" cy="110" r="4" fill="#F59E0B" />
            <text x="120" y="70" fontSize="8" fill="#4ADE80">open string</text>

            <path
              d="M 180 90 Q 200 60, 220 80 Q 240 100, 220 120"
              fill="none"
              stroke="#4ADE80"
              strokeWidth="2"
            />
            <circle cx="180" cy="90" r="4" fill="#F59E0B" />
            <circle cx="220" cy="120" r="4" fill="#F59E0B" />
          </g>
        )}

        {/* Bulk closed string */}
        {showStrings && (
          <g>
            <ellipse cx="80" cy="50" rx="15" ry="10" fill="none" stroke="#8B5CF6" strokeWidth="2" />
            <text x="80" y="30" fontSize="8" fill="#8B5CF6" textAnchor="middle">closed string</text>
            <text x="80" y="75" fontSize="8" fill="#8B5CF6" textAnchor="middle">(in bulk)</text>
          </g>
        )}
      </svg>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={showStrings}
          onChange={(e) => setShowStrings(e.target.checked)}
          className="rounded"
        />
        <label className="text-sm text-gray-600">Show strings</label>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <strong>D-branes:</strong> Objects where open strings can end.
          "D" stands for Dirichlet boundary conditions.
        </div>
        <div className="bg-green-50 p-3 rounded border border-green-200">
          <strong>Gauge fields:</strong> Open strings on D-branes give rise
          to gauge fields (like photons).
        </div>
      </div>
    </div>
  )
}

// Compactification Visualization
function CompactificationViz() {
  const [showCompact, setShowCompact] = useState(true)
  const [compactRadius, setCompactRadius] = useState(0.5)

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Compactification radius R = {compactRadius.toFixed(2)} (Planck units)
        </label>
        <input
          type="range"
          min="0.1"
          max="2"
          step="0.1"
          value={compactRadius}
          onChange={(e) => setCompactRadius(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Extended dimensions */}
        <line x1="20" y1="100" x2="180" y2="100" stroke="#6B7280" strokeWidth="2" />
        <line x1="100" y1="180" x2="100" y2="20" stroke="#6B7280" strokeWidth="2" />
        <text x="170" y="115" fontSize="10" fill="#6B7280">x</text>
        <text x="110" y="30" fontSize="10" fill="#6B7280">y</text>

        {/* Compact dimension(s) */}
        {showCompact && (
          <g>
            {/* Circle representing compact dimension at each point */}
            {[{ x: 60, y: 60 }, { x: 140, y: 60 }, { x: 60, y: 140 }, { x: 140, y: 140 }].map((pos, i) => (
              <circle
                key={i}
                cx={pos.x}
                cy={pos.y}
                r={compactRadius * 20}
                fill="none"
                stroke="#8B5CF6"
                strokeWidth="2"
                opacity="0.6"
              />
            ))}

            {/* Main compact circle */}
            <circle
              cx={220}
              cy={100}
              r={compactRadius * 30}
              fill="#8B5CF6"
              fillOpacity="0.2"
              stroke="#8B5CF6"
              strokeWidth="2"
            />
            <text x="220" y={100 + compactRadius * 30 + 15} fontSize="10" fill="#8B5CF6" textAnchor="middle">
              Compact S^1
            </text>
          </g>
        )}

        {/* Labels */}
        <text x="100" y="195" fontSize="10" fill="#6B7280" textAnchor="middle">
          Extended spacetime
        </text>
      </svg>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={showCompact}
          onChange={(e) => setShowCompact(e.target.checked)}
          className="rounded"
        />
        <label className="text-sm text-gray-600">Show compact dimensions</label>
      </div>

      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <div className="bg-gray-50 p-2 rounded">
          <div className="font-medium">10D</div>
          <div className="text-xs text-gray-500">Full string theory</div>
        </div>
        <div className="bg-purple-50 p-2 rounded border border-purple-200">
          <div className="font-medium">= 4D + 6D</div>
          <div className="text-xs text-purple-600">Spacetime + compact</div>
        </div>
        <div className="bg-green-50 p-2 rounded border border-green-200">
          <div className="font-medium">T^3/Z_2</div>
          <div className="text-xs text-green-600">Z2 compactification</div>
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Why compactify?</strong> String theory requires 10D, but we observe 4D.
        The extra 6 dimensions must be compact (curled up) at small scales.
      </div>
    </div>
  )
}

export default function StringTheoryPage() {
  return (
    <DocumentLayout
      title="String Theory"
      description="Strings, D-branes, and the path to the Z2 framework"
      phase="physics"
      currentIndex={8}
      prevLink={{ href: '/office-hours/physics/07-cosmology', title: 'Cosmology' }}
      nextLink={{ href: '/office-hours/physics/09-holography', title: 'Holography' }}
    >
      <Section title="1. Why Strings?">
        <p className="text-gray-700 mb-4">
          String theory replaces point particles with 1-dimensional extended objects: <strong>strings</strong>.
          This simple change resolves the infinities of quantum gravity and unifies all forces.
        </p>

        <div className="grid grid-cols-2 gap-4 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <strong>Point particles:</strong>
            <div className="text-sm text-gray-600">
              Interactions at a single point lead to infinite energies (UV divergences)
            </div>
          </div>
          <div className="bg-green-50 p-3 rounded border border-green-200">
            <strong>Strings:</strong>
            <div className="text-sm text-gray-600">
              Interactions spread over string worldsheet, naturally regularizing infinities
            </div>
          </div>
        </div>

        <KeyPoint>
          String theory is the only known consistent theory of quantum gravity.
          It automatically includes gravity (the graviton is a string vibration mode)!
        </KeyPoint>
      </Section>

      <Section title="2. String Vibrations as Particles">
        <p className="text-gray-700 mb-4">
          Different vibration modes of the string correspond to different particles.
          The particle spectrum emerges from the string spectrum!
        </p>

        <InteractiveBox title="String Vibration Modes">
          <StringModesViz />
        </InteractiveBox>

        <SubSection title="Particle Spectrum">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">String Type</th>
                  <th className="border border-gray-200 p-2">Mode</th>
                  <th className="border border-gray-200 p-2">Particle</th>
                </tr>
              </thead>
              <tbody>
                <tr className="bg-purple-50">
                  <td className="border border-gray-200 p-2">Closed string</td>
                  <td className="border border-gray-200 p-2">Lowest</td>
                  <td className="border border-gray-200 p-2 font-bold">Graviton (spin 2)</td>
                </tr>
                <tr className="bg-blue-50">
                  <td className="border border-gray-200 p-2">Open string</td>
                  <td className="border border-gray-200 p-2">Lowest</td>
                  <td className="border border-gray-200 p-2 font-bold">Gauge boson (spin 1)</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Any string</td>
                  <td className="border border-gray-200 p-2">Higher modes</td>
                  <td className="border border-gray-200 p-2">Massive particles</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>

        <Formula label="String mass formula">
          M^2 = (n - 1) / alpha' (open string, bosonic)
        </Formula>
      </Section>

      <Section title="3. D-Branes">
        <p className="text-gray-700 mb-4">
          <strong>D-branes</strong> are extended objects where open strings can end.
          They are essential for understanding gauge theories in string theory.
        </p>

        <InteractiveBox title="D-Branes and Open Strings">
          <DBraneViz />
        </InteractiveBox>

        <SubSection title="D-Brane Properties">
          <div className="space-y-2 text-gray-700">
            <p>- <strong>Dp-brane:</strong> Extends in p spatial dimensions</p>
            <p>- <strong>Gauge fields:</strong> Open strings on N D-branes give U(N) gauge theory</p>
            <p>- <strong>Tension:</strong> T_p ~ 1/(g_s * l_s^(p+1)) - branes are heavy at weak coupling</p>
            <p>- <strong>Charge:</strong> D-branes carry RR charge, sources for form fields</p>
          </div>
        </SubSection>

        <Z2Connection
          formula="N D-branes -> U(N) gauge group"
          description="Stacks of D-branes give non-abelian gauge symmetries"
        />
      </Section>

      <Section title="4. Compactification">
        <p className="text-gray-700 mb-4">
          String theory naturally lives in 10 dimensions (26 for bosonic strings).
          We need to <strong>compactify</strong> extra dimensions to match our 4D world.
        </p>

        <InteractiveBox title="Extra Dimensions">
          <CompactificationViz />
        </InteractiveBox>

        <SubSection title="Compactification Choices">
          <div className="grid grid-cols-2 gap-3 my-4 text-sm">
            <div className="bg-gray-50 p-3 rounded">
              <strong>Calabi-Yau:</strong>
              <div className="text-gray-600">Complex 3-fold, preserves N=1 SUSY</div>
            </div>
            <div className="bg-purple-50 p-3 rounded border border-purple-200">
              <strong>T^6/Z_2 (or T^3/Z_2):</strong>
              <div className="text-purple-600">Orbifold, simpler but singular</div>
            </div>
            <div className="bg-blue-50 p-3 rounded">
              <strong>G2 manifold:</strong>
              <div className="text-blue-600">For M-theory compactification</div>
            </div>
            <div className="bg-green-50 p-3 rounded border border-green-200">
              <strong>Flux compactification:</strong>
              <div className="text-green-600">Stabilizes moduli with fluxes</div>
            </div>
          </div>
        </SubSection>

        <KeyPoint>
          The Z2 framework uses <strong>T^3/Z_2</strong> compactification with D-branes.
          The orbifold fixed points give rise to chiral matter and the 13/19 cosmological constant!
        </KeyPoint>
      </Section>

      <Section title="5. Types of String Theory">
        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2">Theory</th>
                <th className="border border-gray-200 p-2">Strings</th>
                <th className="border border-gray-200 p-2">SUSY</th>
                <th className="border border-gray-200 p-2">Gauge Group</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2">Type I</td>
                <td className="border border-gray-200 p-2">Open + Closed</td>
                <td className="border border-gray-200 p-2">N=1</td>
                <td className="border border-gray-200 p-2">SO(32)</td>
              </tr>
              <tr className="bg-blue-50">
                <td className="border border-gray-200 p-2">Type IIA</td>
                <td className="border border-gray-200 p-2">Closed</td>
                <td className="border border-gray-200 p-2">N=2 (non-chiral)</td>
                <td className="border border-gray-200 p-2">U(1) (from D-branes)</td>
              </tr>
              <tr className="bg-purple-50">
                <td className="border border-gray-200 p-2 font-bold">Type IIB</td>
                <td className="border border-gray-200 p-2">Closed</td>
                <td className="border border-gray-200 p-2">N=2 (chiral)</td>
                <td className="border border-gray-200 p-2">From D-branes</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Heterotic E8</td>
                <td className="border border-gray-200 p-2">Closed</td>
                <td className="border border-gray-200 p-2">N=1</td>
                <td className="border border-gray-200 p-2">E8 x E8</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Heterotic SO</td>
                <td className="border border-gray-200 p-2">Closed</td>
                <td className="border border-gray-200 p-2">N=1</td>
                <td className="border border-gray-200 p-2">SO(32)</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="bg-purple-50 p-4 rounded border border-purple-200 my-4">
          <strong>Z2 uses Type IIB:</strong> D3-branes in Type IIB string theory on T^3/Z_2
          give the Z2 framework. AdS/CFT connects this to holography!
        </div>
      </Section>

      <Section title="6. Connection to Z2 Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="Type IIB on T^3/Z_2"
            description="The specific string compactification used in the Z2 framework"
          />
          <Z2Connection
            formula="D3-branes at fixed points"
            description="D-branes at the 8 orbifold singularities give gauge fields and matter"
          />
          <Z2Connection
            formula="Open strings -> SM particles"
            description="Standard Model particles arise from open string modes on D-branes"
          />
        </div>

        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why String Theory Matters for Z2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>- <strong>Consistency:</strong> Only known UV-complete quantum gravity</li>
            <li>- <strong>D-branes:</strong> Provide gauge fields and matter</li>
            <li>- <strong>Compactification:</strong> T^3/Z_2 gives specific predictions</li>
            <li>- <strong>Holography:</strong> Connects to AdS/CFT (next chapter)</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Why does string theory require 10 dimensions? (Hint: conformal anomaly cancellation)</li>
          <li>How many spatial dimensions does a D3-brane extend in?</li>
          <li>What gauge group arises from N coincident D-branes?</li>
          <li>The graviton has spin 2. What string mode gives a spin-2 particle?</li>
          <li>Why is the orbifold T^3/Z_2 simpler than a generic Calabi-Yau?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
