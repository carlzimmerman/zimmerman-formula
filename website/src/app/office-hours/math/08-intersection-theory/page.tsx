'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Intersection Number Visualization
function IntersectionNumberViz() {
  const [curve1Angle, setCurve1Angle] = useState(30)
  const [curve2Angle, setCurve2Angle] = useState(-30)

  const rad1 = (curve1Angle * Math.PI) / 180
  const rad2 = (curve2Angle * Math.PI) / 180

  // Calculate intersection point (simplified for visualization)
  const intersectionX = 150
  const intersectionY = 100

  // Calculate orientation at intersection
  const cross = Math.cos(rad1) * Math.sin(rad2) - Math.sin(rad1) * Math.cos(rad2)
  const orientation = cross > 0 ? '+1' : cross < 0 ? '-1' : '0'

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Curve A angle = {curve1Angle}°
          </label>
          <input
            type="range"
            min="-80"
            max="80"
            value={curve1Angle}
            onChange={(e) => setCurve1Angle(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Curve B angle = {curve2Angle}°
          </label>
          <input
            type="range"
            min="-80"
            max="80"
            value={curve2Angle}
            onChange={(e) => setCurve2Angle(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Grid */}
        {[50, 100, 150, 200, 250].map((x) => (
          <line key={`v${x}`} x1={x} y1="20" x2={x} y2="180" stroke="#F3F4F6" strokeWidth="1" />
        ))}
        {[50, 100, 150].map((y) => (
          <line key={`h${y}`} x1="20" y1={y} x2="280" y2={y} stroke="#F3F4F6" strokeWidth="1" />
        ))}

        {/* Curve A */}
        <line
          x1={intersectionX - 100 * Math.cos(rad1)}
          y1={intersectionY + 100 * Math.sin(rad1)}
          x2={intersectionX + 100 * Math.cos(rad1)}
          y2={intersectionY - 100 * Math.sin(rad1)}
          stroke="#3B82F6"
          strokeWidth="3"
        />
        <text
          x={intersectionX + 110 * Math.cos(rad1)}
          y={intersectionY - 110 * Math.sin(rad1)}
          fontSize="14"
          fill="#3B82F6"
          fontWeight="bold"
        >
          A
        </text>

        {/* Curve B */}
        <line
          x1={intersectionX - 100 * Math.cos(rad2)}
          y1={intersectionY + 100 * Math.sin(rad2)}
          x2={intersectionX + 100 * Math.cos(rad2)}
          y2={intersectionY - 100 * Math.sin(rad2)}
          stroke="#EF4444"
          strokeWidth="3"
        />
        <text
          x={intersectionX + 110 * Math.cos(rad2)}
          y={intersectionY - 110 * Math.sin(rad2)}
          fontSize="14"
          fill="#EF4444"
          fontWeight="bold"
        >
          B
        </text>

        {/* Intersection point */}
        <circle
          cx={intersectionX}
          cy={intersectionY}
          r="8"
          fill={cross > 0 ? '#10B981' : cross < 0 ? '#F59E0B' : '#9CA3AF'}
          stroke="#1F2937"
          strokeWidth="2"
        />

        {/* Orientation arrows */}
        <defs>
          <marker id="arrowBlue" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#3B82F6" />
          </marker>
          <marker id="arrowRed" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#EF4444" />
          </marker>
        </defs>
      </svg>

      <div className="grid grid-cols-3 gap-3 text-center">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="text-sm text-blue-600">Curve A</div>
          <div className="font-mono">{curve1Angle}°</div>
        </div>
        <div className={`p-3 rounded border-2 ${
          cross > 0 ? 'bg-green-100 border-green-400' :
          cross < 0 ? 'bg-amber-100 border-amber-400' :
          'bg-gray-100 border-gray-300'
        }`}>
          <div className="text-sm text-gray-600">Intersection #</div>
          <div className="text-2xl font-bold">{orientation}</div>
        </div>
        <div className="bg-red-50 p-3 rounded border border-red-200">
          <div className="text-sm text-red-600">Curve B</div>
          <div className="font-mono">{curve2Angle}°</div>
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Signed intersection:</strong> The sign depends on the relative orientation of the curves.
        Reversing the direction of either curve flips the sign!
      </div>
    </div>
  )
}

// D-brane Intersection Visualization
function DBraneIntersectionViz() {
  const [braneAWrapping, setBraneAWrapping] = useState({ x: 1, y: 0 })
  const [braneBWrapping, setBraneBWrapping] = useState({ x: 0, y: 1 })

  // Intersection number = |det([Ax, Ay; Bx, By])|
  const intersectionNumber = Math.abs(
    braneAWrapping.x * braneBWrapping.y - braneAWrapping.y * braneBWrapping.x
  )

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="text-sm font-medium text-blue-700 mb-2">D-brane A wrapping numbers</div>
          <div className="flex gap-4">
            <label className="flex items-center gap-2">
              <span className="text-sm">n_x:</span>
              <input
                type="number"
                value={braneAWrapping.x}
                onChange={(e) => setBraneAWrapping({ ...braneAWrapping, x: Number(e.target.value) })}
                className="w-16 p-1 border rounded text-center"
                min="-3"
                max="3"
              />
            </label>
            <label className="flex items-center gap-2">
              <span className="text-sm">n_y:</span>
              <input
                type="number"
                value={braneAWrapping.y}
                onChange={(e) => setBraneAWrapping({ ...braneAWrapping, y: Number(e.target.value) })}
                className="w-16 p-1 border rounded text-center"
                min="-3"
                max="3"
              />
            </label>
          </div>
        </div>
        <div className="bg-red-50 p-3 rounded border border-red-200">
          <div className="text-sm font-medium text-red-700 mb-2">D-brane B wrapping numbers</div>
          <div className="flex gap-4">
            <label className="flex items-center gap-2">
              <span className="text-sm">m_x:</span>
              <input
                type="number"
                value={braneBWrapping.x}
                onChange={(e) => setBraneBWrapping({ ...braneBWrapping, x: Number(e.target.value) })}
                className="w-16 p-1 border rounded text-center"
                min="-3"
                max="3"
              />
            </label>
            <label className="flex items-center gap-2">
              <span className="text-sm">m_y:</span>
              <input
                type="number"
                value={braneBWrapping.y}
                onChange={(e) => setBraneBWrapping({ ...braneBWrapping, y: Number(e.target.value) })}
                className="w-16 p-1 border rounded text-center"
                min="-3"
                max="3"
              />
            </label>
          </div>
        </div>
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Torus fundamental domain */}
        <rect x="50" y="30" width="200" height="140" fill="#F9FAFB" stroke="#9CA3AF" strokeWidth="2" />

        {/* Grid */}
        {[100, 150, 200].map((x) => (
          <line key={`v${x}`} x1={x} y1="30" x2={x} y2="170" stroke="#E5E7EB" strokeWidth="1" />
        ))}
        {[65, 100, 135].map((y) => (
          <line key={`h${y}`} x1="50" y1={y} x2="250" y2={y} stroke="#E5E7EB" strokeWidth="1" />
        ))}

        {/* D-brane A (wrapping (nx, ny) times) */}
        {braneAWrapping.x !== 0 || braneAWrapping.y !== 0 ? (
          <line
            x1="50"
            y1={100 - braneAWrapping.y * 35}
            x2="250"
            y2={100 + braneAWrapping.y * 35}
            stroke="#3B82F6"
            strokeWidth="3"
            strokeDasharray={braneAWrapping.x === 0 ? "8,4" : "none"}
          />
        ) : null}

        {/* D-brane B (wrapping (mx, my) times) */}
        {braneBWrapping.x !== 0 || braneBWrapping.y !== 0 ? (
          <line
            x1={150 - braneBWrapping.x * 50}
            y1="30"
            x2={150 + braneBWrapping.x * 50}
            y2="170"
            stroke="#EF4444"
            strokeWidth="3"
            strokeDasharray={braneBWrapping.y === 0 ? "8,4" : "none"}
          />
        ) : null}

        {/* Intersection points */}
        {intersectionNumber > 0 && (
          <g>
            {Array.from({ length: Math.min(intersectionNumber, 6) }).map((_, i) => (
              <circle
                key={i}
                cx={150 + (i - Math.floor(Math.min(intersectionNumber, 6) / 2)) * 30}
                cy={100}
                r="6"
                fill="#8B5CF6"
                stroke="#7C3AED"
                strokeWidth="2"
              />
            ))}
          </g>
        )}

        {/* Labels */}
        <text x="255" y="105" fontSize="12" fill="#3B82F6" fontWeight="bold">A</text>
        <text x="155" y="25" fontSize="12" fill="#EF4444" fontWeight="bold">B</text>
      </svg>

      <div className="bg-purple-50 p-4 rounded-lg border border-purple-200 text-center">
        <div className="text-sm text-purple-600">Intersection number</div>
        <div className="text-4xl font-bold text-purple-700">
          I<sub>AB</sub> = |n<sub>x</sub>m<sub>y</sub> - n<sub>y</sub>m<sub>x</sub>| = {intersectionNumber}
        </div>
        <div className="text-sm text-gray-600 mt-2">
          = |({braneAWrapping.x})({braneBWrapping.y}) - ({braneAWrapping.y})({braneBWrapping.x})|
        </div>
      </div>

      <div className="bg-green-50 p-3 rounded border border-green-200 text-sm">
        <strong>Physical meaning:</strong> Each intersection point gives rise to a chiral fermion!
        Set wrapping numbers to get I<sub>AB</sub> = 3 for three generations.
      </div>
    </div>
  )
}

// Three Generations Visualization
function ThreeGenerationsViz() {
  const [showDetails, setShowDetails] = useState<number | null>(null)

  const generations = [
    { name: 'First Generation', particles: ['u, d quarks', 'e electron', 'ν_e neutrino'], color: 'blue' },
    { name: 'Second Generation', particles: ['c, s quarks', 'μ muon', 'ν_μ neutrino'], color: 'green' },
    { name: 'Third Generation', particles: ['t, b quarks', 'τ tau', 'ν_τ neutrino'], color: 'orange' },
  ]

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 300 180" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* T³/Z₂ representation */}
        <rect x="30" y="30" width="240" height="120" fill="#F3E8FF" stroke="#8B5CF6" strokeWidth="2" rx="10" />
        <text x="150" y="25" textAnchor="middle" fontSize="12" fill="#7C3AED" fontWeight="bold">
          T³/Z₂ Orbifold
        </text>

        {/* Three D-brane stacks */}
        {[0, 1, 2].map((i) => {
          const x = 80 + i * 70
          const colors = ['#3B82F6', '#10B981', '#F59E0B']
          return (
            <g key={i}>
              {/* D-brane stack */}
              <rect
                x={x - 25}
                y={60}
                width="50"
                height="60"
                fill={colors[i]}
                fillOpacity="0.2"
                stroke={colors[i]}
                strokeWidth="2"
                rx="5"
                className="cursor-pointer"
                onClick={() => setShowDetails(showDetails === i ? null : i)}
              />
              {/* Intersection points */}
              <circle cx={x} cy={90} r="8" fill={colors[i]} stroke="#1F2937" strokeWidth="2" />
              <text x={x} y={93} textAnchor="middle" fontSize="10" fill="white" fontWeight="bold">
                {i + 1}
              </text>
              {/* Label */}
              <text x={x} y={140} textAnchor="middle" fontSize="10" fill={colors[i]} fontWeight="bold">
                Gen {i + 1}
              </text>
            </g>
          )
        })}

        {/* Formula */}
        <text x="150" y="165" textAnchor="middle" fontSize="11" fill="#374151" fontFamily="monospace">
          I_ab = 3 intersections = 3 generations
        </text>
      </svg>

      {showDetails !== null && (
        <div className={`p-4 rounded-lg border-2 ${
          showDetails === 0 ? 'bg-blue-50 border-blue-300' :
          showDetails === 1 ? 'bg-green-50 border-green-300' :
          'bg-amber-50 border-amber-300'
        }`}>
          <div className="font-bold mb-2">{generations[showDetails].name}</div>
          <div className="grid grid-cols-3 gap-2 text-sm">
            {generations[showDetails].particles.map((p, i) => (
              <div key={i} className="bg-white p-2 rounded text-center">{p}</div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-3 gap-3 text-center">
        {generations.map((gen, i) => (
          <button
            key={i}
            onClick={() => setShowDetails(showDetails === i ? null : i)}
            className={`p-3 rounded-lg border-2 transition-all ${
              showDetails === i
                ? i === 0 ? 'border-blue-500 bg-blue-100' :
                  i === 1 ? 'border-green-500 bg-green-100' :
                  'border-amber-500 bg-amber-100'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="font-medium text-sm">{gen.name}</div>
          </button>
        ))}
      </div>

      <div className="bg-purple-50 p-3 rounded border border-purple-200 text-sm text-center">
        <strong>The mystery of three generations is solved!</strong>
        <br />
        D-branes wrapping T³/Z₂ intersect exactly 3 times → 3 copies of each fermion type.
      </div>
    </div>
  )
}

export default function IntersectionTheoryPage() {
  return (
    <DocumentLayout
      title="Intersection Theory"
      description="D-brane intersections, homology classes, and the origin of three generations"
      phase="math"
      currentIndex={8}
      prevLink={{ href: '/office-hours/math/07-index-theory', title: 'Index Theory' }}
      nextLink={{ href: '/office-hours/physics/00-overview', title: 'Physics Overview' }}
    >
      <Section title="1. What is Intersection Theory?">
        <p className="text-gray-700 mb-4">
          <strong>Intersection theory</strong> counts how many times geometric objects (curves, surfaces, etc.)
          cross each other. In physics, this determines how many chiral fermions appear at D-brane intersections!
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <strong>Topology:</strong>
            <div className="text-sm text-gray-600">Counts holes (Betti numbers)</div>
          </div>
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <strong>Intersection Theory:</strong>
            <div className="text-sm text-purple-600">Counts crossings (intersection numbers)</div>
          </div>
        </div>

        <KeyPoint>
          <strong>The central result:</strong> The intersection number I<sub>ab</sub> = 3 on T³/Z₂
          explains why there are exactly three generations of quarks and leptons!
        </KeyPoint>
      </Section>

      <Section title="2. Intersection Numbers">
        <p className="text-gray-700 mb-4">
          When two curves cross on a surface, each intersection point contributes +1 or -1
          depending on the relative orientation:
        </p>

        <InteractiveBox title="Signed Intersection of Curves">
          <IntersectionNumberViz />
        </InteractiveBox>

        <Formula label="Intersection number">
          A · B = Σ_p ε_p (sum over intersection points, with signs)
        </Formula>

        <SubSection title="Properties">
          <div className="space-y-2 text-gray-700">
            <p>• <strong>Symmetric:</strong> A · B = B · A (for even-dimensional intersections)</p>
            <p>• <strong>Antisymmetric:</strong> A · B = -B · A (for odd-dimensional)</p>
            <p>• <strong>Topological:</strong> Only depends on homology classes, not representatives</p>
            <p>• <strong>Additive:</strong> (A + A') · B = A · B + A' · B</p>
          </div>
        </SubSection>
      </Section>

      <Section title="3. Homology and Intersections">
        <p className="text-gray-700 mb-4">
          Intersection numbers are defined between <strong>homology classes</strong>, not just geometric objects.
          This makes them topological invariants!
        </p>

        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <div className="font-medium text-blue-800 mb-2">Intersection Pairing</div>
          <div className="font-mono text-center">
            H_p(M) × H_q(M) → ℤ
          </div>
          <div className="text-sm text-gray-600 mt-2 text-center">
            where p + q = dim(M)
          </div>
        </div>

        <SubSection title="On the Torus T²">
          <p className="text-gray-700 mb-4">
            The torus has two basic 1-cycles: α (around the hole) and β (around the tube).
            Their intersection number is:
          </p>
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="bg-gray-50 p-3 rounded">
              <div className="font-mono">α · α = 0</div>
              <div className="text-xs text-gray-500">Self-intersection</div>
            </div>
            <div className="bg-purple-50 p-3 rounded border border-purple-200">
              <div className="font-mono font-bold">α · β = 1</div>
              <div className="text-xs text-purple-600">Cross once!</div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <div className="font-mono">β · β = 0</div>
              <div className="text-xs text-gray-500">Self-intersection</div>
            </div>
          </div>
        </SubSection>

        <Z2Connection
          formula="H₁(T²) = ℤ ⊕ ℤ"
          description="Two generators α and β with intersection matrix ((0,1),(−1,0))"
        />
      </Section>

      <Section title="4. D-Brane Intersections">
        <p className="text-gray-700 mb-4">
          In string theory, <strong>D-branes</strong> are extended objects that wrap cycles of the
          compactification space. When two D-branes intersect, massless chiral fermions appear!
        </p>

        <InteractiveBox title="D-Brane Wrapping and Intersections">
          <DBraneIntersectionViz />
        </InteractiveBox>

        <Formula label="Chiral fermion count">
          # of fermions = |I_ab| = |[Σ_a] · [Σ_b]|
        </Formula>

        <SubSection title="Wrapping Numbers">
          <p className="text-gray-700 mb-4">
            A D-brane wrapping a cycle is characterized by its <strong>wrapping numbers</strong> —
            how many times it goes around each direction:
          </p>
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">D-brane</th>
                  <th className="border border-gray-200 p-2">Cycle Class</th>
                  <th className="border border-gray-200 p-2">Wrapping</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2">Brane A</td>
                  <td className="border border-gray-200 p-2 font-mono">[Σ_a] = n_x[α] + n_y[β]</td>
                  <td className="border border-gray-200 p-2">(n_x, n_y) times</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Brane B</td>
                  <td className="border border-gray-200 p-2 font-mono">[Σ_b] = m_x[α] + m_y[β]</td>
                  <td className="border border-gray-200 p-2">(m_x, m_y) times</td>
                </tr>
                <tr className="bg-purple-50">
                  <td className="border border-gray-200 p-2 font-bold">Intersection</td>
                  <td className="border border-gray-200 p-2 font-mono">I_ab = n_x m_y - n_y m_x</td>
                  <td className="border border-gray-200 p-2">Determinant!</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>
      </Section>

      <Section title="5. Three Generations from I_ab = 3">
        <p className="text-gray-700 mb-4">
          The Z² framework predicts exactly three particle generations because D-branes on T³/Z₂
          can be arranged to have intersection number I<sub>ab</sub> = 3.
        </p>

        <InteractiveBox title="Three Generations from D-Brane Intersections">
          <ThreeGenerationsViz />
        </InteractiveBox>

        <Formula label="The key result">
          I_ab = 3 → 3 generations of quarks and leptons
        </Formula>

        <SubSection title="Why Exactly 3?">
          <div className="space-y-2 text-gray-700">
            <p>• <strong>Topological:</strong> The intersection number is fixed by the homology classes</p>
            <p>• <strong>Stable:</strong> Cannot change by continuous deformation</p>
            <p>• <strong>Integer:</strong> Must be a whole number (no fractional generations!)</p>
            <p>• <strong>Geometric:</strong> Related to b₁(T³) = 3</p>
          </div>
        </SubSection>

        <Z2Connection
          formula="I_ab = 3"
          description="Three D-brane intersections on T³/Z₂ give three copies of each fermion"
        />
      </Section>

      <Section title="6. Intersection Theory on T³/Z₂">
        <p className="text-gray-700 mb-4">
          On the orbifold T³/Z₂, intersection theory becomes richer due to the fixed points:
        </p>

        <div className="grid grid-cols-2 gap-4 my-4">
          <div className="bg-blue-50 p-3 rounded border border-blue-200">
            <div className="font-medium text-blue-800">Bulk Intersections</div>
            <ul className="text-sm text-gray-600 mt-2 space-y-1">
              <li>• On the smooth part of T³/Z₂</li>
              <li>• Standard intersection pairing</li>
              <li>• Gives chiral fermions</li>
            </ul>
          </div>
          <div className="bg-red-50 p-3 rounded border border-red-200">
            <div className="font-medium text-red-800">Fixed Point Contributions</div>
            <ul className="text-sm text-gray-600 mt-2 space-y-1">
              <li>• At the 8 orbifold singularities</li>
              <li>• Additional twisted sector states</li>
              <li>• Modify the count by factors of 1/2</li>
            </ul>
          </div>
        </div>

        <Formula label="Full intersection formula">
          I_ab = [Σ_a] · [Σ_b] + Σ_{'{fixed}'} correction terms
        </Formula>

        <KeyPoint>
          The orbifold structure of T³/Z₂ is essential: it provides both the chirality (from Z₂)
          and the specific intersection number that gives three generations.
        </KeyPoint>
      </Section>

      <Section title="7. Connection to Z² Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="I_ab = 3"
            description="D-brane intersections on T³/Z₂ give exactly 3 generations"
          />
          <Z2Connection
            formula="b₁(T³) = 3"
            description="Three 1-cycles on T³ allow wrappings that give I_ab = 3"
          />
          <Z2Connection
            formula="Gauge groups from branes"
            description="SU(3)×SU(2)×U(1) arises from stacks of intersecting D-branes"
          />
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Intersection Theory Matters</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Generation counting:</strong> I_ab = 3 explains three families</li>
            <li>• <strong>Chirality:</strong> Intersecting branes naturally produce chiral fermions</li>
            <li>• <strong>Gauge groups:</strong> Stacks of branes give SU(N) gauge symmetries</li>
            <li>• <strong>Yukawa couplings:</strong> Come from triple intersections of branes</li>
          </ul>
        </div>
      </Section>

      <Section title="8. Summary: From Geometry to Particles">
        <div className="bg-gradient-to-r from-blue-50 via-purple-50 to-green-50 p-4 rounded-lg">
          <div className="text-center space-y-4">
            <div className="grid grid-cols-5 gap-2 items-center text-sm">
              <div className="bg-white p-2 rounded shadow">T³/Z₂</div>
              <div className="text-2xl">→</div>
              <div className="bg-white p-2 rounded shadow">D-branes wrap cycles</div>
              <div className="text-2xl">→</div>
              <div className="bg-white p-2 rounded shadow">I_ab = 3</div>
            </div>
            <div className="text-2xl">↓</div>
            <div className="bg-purple-100 p-3 rounded-lg text-purple-800 font-bold">
              3 Generations of Quarks and Leptons
            </div>
          </div>
        </div>

        <p className="text-gray-700 mt-4">
          This is the geometric origin of the three-generation structure of the Standard Model!
          The number 3 is not arbitrary — it comes from the topology of the extra-dimensional space.
        </p>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>On T², if brane A wraps (2, 1) and brane B wraps (1, 1), calculate I_AB.</li>
          <li>Show that α · β = 1 on the torus by drawing the two cycles and counting intersections with signs.</li>
          <li>Why is the intersection number unchanged if we move the curves continuously (without cutting)?</li>
          <li>If we want I_ab = 3 on T², find wrapping numbers (n_x, n_y) and (m_x, m_y) that work.</li>
          <li>On T³ = S¹ × S¹ × S¹, how many independent 2-cycles are there? (Hint: b₂(T³) = 3)</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
