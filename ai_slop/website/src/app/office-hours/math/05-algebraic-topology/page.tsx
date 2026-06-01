'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Homology Cycle Visualization
function HomologyCycleViz() {
  const [surface, setSurface] = useState<'sphere' | 'torus' | 'torus3'>('torus')

  const surfaces = {
    sphere: { b0: 1, b1: 0, b2: 1, euler: 2, name: 'Sphere S²' },
    torus: { b0: 1, b1: 2, b2: 1, euler: 0, name: 'Torus T²' },
    torus3: { b0: 1, b1: 3, b2: 3, euler: 0, name: '3-Torus T³' },
  }

  const current = surfaces[surface]

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-4">
        {(Object.keys(surfaces) as Array<keyof typeof surfaces>).map((key) => (
          <button
            key={key}
            onClick={() => setSurface(key)}
            className={`px-4 py-2 rounded-lg border-2 transition-all ${
              surface === key
                ? 'border-purple-500 bg-purple-50 text-purple-700'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            {surfaces[key].name}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-4 gap-3 text-center">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="text-xs text-blue-600">b₀ (connected components)</div>
          <div className="text-3xl font-bold text-blue-700">{current.b0}</div>
        </div>
        <div className="bg-green-50 p-3 rounded border border-green-200">
          <div className="text-xs text-green-600">b₁ (1-cycles / holes)</div>
          <div className="text-3xl font-bold text-green-700">{current.b1}</div>
        </div>
        <div className="bg-orange-50 p-3 rounded border border-orange-200">
          <div className="text-xs text-orange-600">b₂ (2-cycles / voids)</div>
          <div className="text-3xl font-bold text-orange-700">{current.b2}</div>
        </div>
        <div className="bg-purple-50 p-3 rounded border border-purple-200">
          <div className="text-xs text-purple-600">Euler χ</div>
          <div className="text-3xl font-bold text-purple-700">{current.euler}</div>
        </div>
      </div>

      {surface === 'torus' && (
        <svg viewBox="0 0 300 150" className="w-full max-w-md mx-auto">
          {/* Torus outline */}
          <ellipse cx="150" cy="75" rx="100" ry="50" fill="none" stroke="#9CA3AF" strokeWidth="2" />
          <ellipse cx="150" cy="75" rx="35" ry="18" fill="#fafafa" stroke="#9CA3AF" strokeWidth="2" />

          {/* Alpha cycle */}
          <ellipse cx="150" cy="75" rx="70" ry="35" fill="none" stroke="#3B82F6" strokeWidth="3" strokeDasharray="8,4" />
          <text x="230" y="80" fontSize="14" fill="#3B82F6" fontWeight="bold">α</text>

          {/* Beta cycle */}
          <path d="M 150 25 Q 200 75 150 125 Q 100 75 150 25" fill="none" stroke="#EF4444" strokeWidth="3" strokeDasharray="8,4" />
          <text x="160" y="30" fontSize="14" fill="#EF4444" fontWeight="bold">β</text>
        </svg>
      )}

      {surface === 'torus3' && (
        <div className="bg-purple-50 p-4 rounded-lg text-center">
          <div className="text-lg font-medium text-purple-800">T³ = S¹ × S¹ × S¹</div>
          <div className="text-sm text-purple-600 mt-2">
            Three independent 1-cycles: α, β, γ — one for each S¹ factor
          </div>
          <div className="font-mono mt-2 p-2 bg-white rounded">
            b₁(T³) = 3 → <strong>Three particle generations!</strong>
          </div>
        </div>
      )}

      {surface === 'sphere' && (
        <div className="bg-blue-50 p-4 rounded-lg text-center">
          <div className="text-lg font-medium text-blue-800">S² has no holes</div>
          <div className="text-sm text-blue-600 mt-2">
            Every loop can be shrunk to a point: b₁ = 0
          </div>
        </div>
      )}

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Key formula:</strong> χ = b₀ - b₁ + b₂ - b₃ + ... (alternating sum of Betti numbers)
      </div>
    </div>
  )
}

// Cohomology Visualization
function CohomologyViz() {
  const [formDegree, setFormDegree] = useState(1)

  const forms = [
    { degree: 0, name: 'Functions', example: 'f(x, y)', dual: 'points' },
    { degree: 1, name: '1-forms', example: 'f dx + g dy', dual: 'curves' },
    { degree: 2, name: '2-forms', example: 'h dx∧dy', dual: 'surfaces' },
    { degree: 3, name: '3-forms', example: 'ρ dx∧dy∧dz', dual: 'volumes' },
  ]

  const current = forms[formDegree]

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Form degree: p = {formDegree}
        </label>
        <input
          type="range"
          min="0"
          max="3"
          value={formDegree}
          onChange={(e) => setFormDegree(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-blue-50 p-4 rounded border border-blue-200">
          <div className="text-sm text-blue-600 font-medium">p-form (cohomology)</div>
          <div className="text-xl font-bold text-blue-800 mt-1">{current.name}</div>
          <div className="font-mono text-sm mt-2 bg-white p-2 rounded">{current.example}</div>
        </div>
        <div className="bg-green-50 p-4 rounded border border-green-200">
          <div className="text-sm text-green-600 font-medium">Dual p-chain (homology)</div>
          <div className="text-xl font-bold text-green-800 mt-1">{current.dual}</div>
          <div className="text-sm mt-2">Integrate p-forms over {current.dual}</div>
        </div>
      </div>

      <div className="bg-gray-50 p-4 rounded">
        <div className="text-center font-mono text-lg">
          <span className="text-blue-600">Hᵖ(M)</span>
          <span className="mx-2">≅</span>
          <span className="text-green-600">Hₚ(M)</span>
          <span className="text-gray-400 text-sm ml-2">(Poincaré duality)</span>
        </div>
      </div>

      <div className="bg-purple-50 p-3 rounded border border-purple-200 text-sm">
        <strong>Exterior derivative:</strong> d raises degree by 1
        <div className="font-mono mt-1">
          df = (∂f/∂x)dx + (∂f/∂y)dy + (∂f/∂z)dz
        </div>
        <div className="mt-1">Closed forms: dω = 0. Exact forms: ω = dα.</div>
      </div>
    </div>
  )
}

// De Rham Theorem Visualization
function DeRhamViz() {
  const [showIntegration, setShowIntegration] = useState(false)

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 300 180" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Torus */}
        <ellipse cx="150" cy="90" rx="90" ry="45" fill="none" stroke="#9CA3AF" strokeWidth="2" />
        <ellipse cx="150" cy="90" rx="30" ry="15" fill="#fafafa" stroke="#9CA3AF" strokeWidth="2" />

        {/* Alpha cycle */}
        <ellipse
          cx="150"
          cy="90"
          rx="60"
          ry="30"
          fill="none"
          stroke="#3B82F6"
          strokeWidth="3"
        />

        {/* 1-form arrows */}
        {showIntegration && (
          <g>
            {[0, 45, 90, 135, 180, 225, 270, 315].map((angle, i) => {
              const rad = (angle * Math.PI) / 180
              const x = 150 + 60 * Math.cos(rad)
              const y = 90 + 30 * Math.sin(rad)
              const tx = -Math.sin(rad) * 12
              const ty = Math.cos(rad) * 6
              return (
                <g key={i}>
                  <line
                    x1={x}
                    y1={y}
                    x2={x + tx}
                    y2={y + ty}
                    stroke="#EF4444"
                    strokeWidth="2"
                    markerEnd="url(#arrowRed)"
                  />
                </g>
              )
            })}
          </g>
        )}

        <defs>
          <marker id="arrowRed" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
            <polygon points="0 0, 6 3, 0 6" fill="#EF4444" />
          </marker>
        </defs>

        {/* Labels */}
        <text x="220" y="90" fontSize="12" fill="#3B82F6" fontWeight="bold">γ (cycle)</text>
        {showIntegration && (
          <text x="150" y="170" textAnchor="middle" fontSize="11" fill="#EF4444">ω (1-form)</text>
        )}
      </svg>

      <button
        onClick={() => setShowIntegration(!showIntegration)}
        className="mx-auto block px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
      >
        {showIntegration ? 'Hide 1-form' : 'Show integration ∮γ ω'}
      </button>

      <div className="bg-gradient-to-r from-blue-50 to-red-50 p-4 rounded-lg">
        <div className="text-center">
          <div className="text-lg font-medium">De Rham Theorem</div>
          <div className="font-mono text-xl mt-2">
            <span className="text-blue-600">H*_dR(M)</span>
            <span className="mx-2">≅</span>
            <span className="text-green-600">H*(M; ℝ)</span>
          </div>
          <div className="text-sm text-gray-600 mt-2">
            Differential forms ↔ Topology (via integration over cycles)
          </div>
        </div>
      </div>

      <div className="text-sm text-gray-600">
        <strong>Pairing:</strong> The integral ∮_γ ω pairs a 1-form ω with a 1-cycle γ.
        If ω is closed (dω = 0) and γ is a cycle (∂γ = 0), the result depends only on cohomology/homology classes!
      </div>
    </div>
  )
}

export default function AlgebraicTopologyPage() {
  return (
    <DocumentLayout
      title="Algebraic Topology"
      description="Homology, cohomology, and counting holes with algebra"
      phase="math"
      currentIndex={5}
      prevLink={{ href: '/office-hours/math/04-differential-geometry', title: 'Differential Geometry' }}
      nextLink={{ href: '/office-hours/math/06-orbifolds', title: 'Orbifolds' }}
    >
      <Section title="1. What is Algebraic Topology?">
        <p className="text-gray-700 mb-4">
          Algebraic topology converts topological problems into algebraic ones.
          Instead of asking "what shape is this?", we ask "what algebraic invariants does it have?"
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <strong>Topology:</strong>
            <div className="text-sm text-gray-600">Are these two spaces the same shape?</div>
          </div>
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <strong>Algebraic Topology:</strong>
            <div className="text-sm text-purple-600">Compare their homology groups!</div>
          </div>
        </div>

        <KeyPoint>
          <strong>Key idea:</strong> If two spaces have different algebraic invariants (like Betti numbers),
          they cannot be topologically equivalent!
        </KeyPoint>
      </Section>

      <Section title="2. Homology: Counting Holes">
        <p className="text-gray-700 mb-4">
          <strong>Homology</strong> counts the "holes" in a space systematically.
          The n-th Betti number bₙ counts n-dimensional holes.
        </p>

        <InteractiveBox title="Betti Numbers">
          <HomologyCycleViz />
        </InteractiveBox>

        <SubSection title="What Betti Numbers Count">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">Betti #</th>
                  <th className="border border-gray-200 p-2">Counts</th>
                  <th className="border border-gray-200 p-2">Example</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2 font-mono">b₀</td>
                  <td className="border border-gray-200 p-2">Connected components</td>
                  <td className="border border-gray-200 p-2">Two separate circles: b₀ = 2</td>
                </tr>
                <tr className="bg-green-50">
                  <td className="border border-gray-200 p-2 font-mono">b₁</td>
                  <td className="border border-gray-200 p-2">1D holes (loops that can't shrink)</td>
                  <td className="border border-gray-200 p-2">Torus: b₁ = 2</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2 font-mono">b₂</td>
                  <td className="border border-gray-200 p-2">2D holes (voids, cavities)</td>
                  <td className="border border-gray-200 p-2">Sphere: b₂ = 1</td>
                </tr>
                <tr className="bg-purple-50">
                  <td className="border border-gray-200 p-2 font-mono">b₁(T³)</td>
                  <td className="border border-gray-200 p-2 font-bold">= 3</td>
                  <td className="border border-gray-200 p-2">Three generations!</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>

        <Z2Connection
          formula="b₁(T³) = 3"
          description="The first Betti number of T³ gives three particle generations"
        />
      </Section>

      <Section title="3. Cohomology: Dual Perspective">
        <p className="text-gray-700 mb-4">
          <strong>Cohomology</strong> is the dual of homology — instead of counting cycles,
          we study differential forms. Cohomology classes are closed forms modulo exact forms.
        </p>

        <InteractiveBox title="Forms and Their Duals">
          <CohomologyViz />
        </InteractiveBox>

        <Formula label="Cohomology group">
          Hᵖ(M) = {'{closed p-forms}'} / {'{exact p-forms}'} = ker(d) / im(d)
        </Formula>

        <SubSection title="The Exterior Derivative">
          <div className="space-y-2 text-gray-700">
            <p>• <strong>d²= 0:</strong> Applying d twice always gives zero</p>
            <p>• <strong>Closed:</strong> dω = 0 (ω has no "boundary")</p>
            <p>• <strong>Exact:</strong> ω = dα (ω is a "boundary")</p>
            <p>• <strong>Cohomology:</strong> Closed forms that aren't exact</p>
          </div>
        </SubSection>
      </Section>

      <Section title="4. De Rham Theorem">
        <p className="text-gray-700 mb-4">
          The <strong>de Rham theorem</strong> is a profound connection: differential forms
          (analysis) encode the same information as homology (topology)!
        </p>

        <InteractiveBox title="Integration Pairs Forms with Cycles">
          <DeRhamViz />
        </InteractiveBox>

        <Formula label="De Rham Theorem">
          H*_dR(M) ≅ H*(M; ℝ)
        </Formula>

        <KeyPoint>
          <strong>Integration connects analysis and topology:</strong> The integral ∮_γ ω
          of a closed form over a cycle gives a topological invariant.
        </KeyPoint>
      </Section>

      <Section title="5. Homology of the 3-Torus">
        <p className="text-gray-700 mb-4">
          The 3-torus T³ = S¹ × S¹ × S¹ has rich homological structure:
        </p>

        <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <div className="grid grid-cols-4 gap-3 text-center">
            <div>
              <div className="text-xs text-gray-500">H₀(T³)</div>
              <div className="text-2xl font-bold">ℤ</div>
              <div className="text-xs text-gray-500">b₀ = 1</div>
            </div>
            <div className="bg-white p-2 rounded">
              <div className="text-xs text-purple-600 font-medium">H₁(T³)</div>
              <div className="text-2xl font-bold text-purple-700">ℤ³</div>
              <div className="text-xs text-purple-600">b₁ = 3</div>
            </div>
            <div>
              <div className="text-xs text-gray-500">H₂(T³)</div>
              <div className="text-2xl font-bold">ℤ³</div>
              <div className="text-xs text-gray-500">b₂ = 3</div>
            </div>
            <div>
              <div className="text-xs text-gray-500">H₃(T³)</div>
              <div className="text-2xl font-bold">ℤ</div>
              <div className="text-xs text-gray-500">b₃ = 1</div>
            </div>
          </div>
        </div>

        <SubSection title="The Three 1-Cycles">
          <p className="text-gray-700 mb-4">
            The three independent 1-cycles on T³ correspond to going around each of the three S¹ factors:
          </p>
          <div className="grid grid-cols-3 gap-3 text-center text-sm">
            <div className="bg-blue-50 p-3 rounded">
              <div className="font-mono font-bold text-blue-700">γ₁</div>
              <div className="text-xs text-gray-600">Around first S¹</div>
            </div>
            <div className="bg-green-50 p-3 rounded">
              <div className="font-mono font-bold text-green-700">γ₂</div>
              <div className="text-xs text-gray-600">Around second S¹</div>
            </div>
            <div className="bg-orange-50 p-3 rounded">
              <div className="font-mono font-bold text-orange-700">γ₃</div>
              <div className="text-xs text-gray-600">Around third S¹</div>
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="6. Connection to Z² Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="b₁(T³) = 3"
            description="Three 1-cycles on T³ give three generations of quarks and leptons"
          />
          <Z2Connection
            formula="H₁(T³/Z₂)"
            description="Orbifold projection modifies homology, selecting chiral spectrum"
          />
          <Z2Connection
            formula="∮ A"
            description="Wilson lines (integrals of gauge fields over cycles) give masses"
          />
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Algebraic Topology Matters</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Betti numbers:</strong> b₁(T³) = 3 explains three generations</li>
            <li>• <strong>Cohomology:</strong> Differential forms describe gauge fields</li>
            <li>• <strong>De Rham theory:</strong> Connects field equations to topology</li>
            <li>• <strong>Intersection numbers:</strong> Count D-brane intersections</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Calculate the Betti numbers of a Klein bottle. (Hint: b₁ = 1)</li>
          <li>Show that χ = b₀ - b₁ + b₂ gives χ = 0 for the torus T².</li>
          <li>Why is b₁(T³) = 3 while b₁(T²) = 2? (Hint: product rule)</li>
          <li>If df = 0 on a simply connected space, show f is constant.</li>
          <li>The sphere S² has b₁ = 0. What does this mean for loops on S²?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
