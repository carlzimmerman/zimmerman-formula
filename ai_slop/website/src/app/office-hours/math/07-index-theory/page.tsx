'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Index Calculation Visualization
function IndexViz() {
  const [nPlus, setNPlus] = useState(5)
  const [nMinus, setNMinus] = useState(2)

  const index = nPlus - nMinus

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            n₊ (+ chirality zero modes) = {nPlus}
          </label>
          <input
            type="range"
            min="0"
            max="10"
            value={nPlus}
            onChange={(e) => setNPlus(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            n₋ (- chirality zero modes) = {nMinus}
          </label>
          <input
            type="range"
            min="0"
            max="10"
            value={nMinus}
            onChange={(e) => setNMinus(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <div className="flex items-center justify-center gap-4">
        {/* Positive modes */}
        <div className="text-center">
          <div className="text-sm text-blue-600 mb-2">Left-handed</div>
          <div className="flex flex-wrap justify-center gap-1 max-w-32">
            {Array.from({ length: nPlus }).map((_, i) => (
              <div key={i} className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs">
                +
              </div>
            ))}
          </div>
        </div>

        <div className="text-4xl text-gray-400">−</div>

        {/* Negative modes */}
        <div className="text-center">
          <div className="text-sm text-red-600 mb-2">Right-handed</div>
          <div className="flex flex-wrap justify-center gap-1 max-w-32">
            {Array.from({ length: nMinus }).map((_, i) => (
              <div key={i} className="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center text-white text-xs">
                −
              </div>
            ))}
          </div>
        </div>

        <div className="text-4xl text-gray-400">=</div>

        {/* Index */}
        <div className="text-center">
          <div className="text-sm text-purple-600 mb-2">Index</div>
          <div className={`text-5xl font-bold ${index > 0 ? 'text-blue-600' : index < 0 ? 'text-red-600' : 'text-gray-400'}`}>
            {index}
          </div>
        </div>
      </div>

      <div className="bg-purple-50 p-4 rounded-lg text-center">
        <div className="font-mono text-lg">
          ind(D) = n₊ - n₋ = {nPlus} - {nMinus} = {index}
        </div>
        <div className="text-sm text-gray-600 mt-2">
          The index counts the <em>net</em> number of chiral zero modes
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Key insight:</strong> The index is a topological invariant — it doesn't change
        under continuous deformations of the operator D!
      </div>
    </div>
  )
}

// APS Theorem Visualization
function APSViz() {
  const [showBoundary, setShowBoundary] = useState(true)

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Manifold with boundary */}
        <ellipse cx="150" cy="100" rx="100" ry="70" fill="#EFF6FF" stroke="#3B82F6" strokeWidth="2" />

        {/* Interior region */}
        <text x="150" y="90" textAnchor="middle" fontSize="14" fill="#1E40AF" fontWeight="bold">
          M (manifold)
        </text>
        <text x="150" y="110" textAnchor="middle" fontSize="12" fill="#3B82F6">
          Dirac operator D
        </text>

        {/* Boundary */}
        {showBoundary && (
          <g>
            <ellipse cx="150" cy="100" rx="100" ry="70" fill="none" stroke="#EF4444" strokeWidth="4" />
            <text x="260" y="100" fontSize="12" fill="#EF4444" fontWeight="bold">∂M</text>

            {/* Eta invariant label */}
            <path d="M 250 85 Q 270 70 280 80" fill="none" stroke="#EF4444" strokeWidth="1" />
            <text x="285" y="85" fontSize="10" fill="#EF4444">η(∂M)</text>
          </g>
        )}

        {/* Formula box */}
        <rect x="50" y="150" width="200" height="40" fill="white" stroke="#9CA3AF" rx="5" />
        <text x="150" y="175" textAnchor="middle" fontSize="12" fill="#374151" fontFamily="monospace">
          ind(D) = ∫_M â - η(∂M)/2
        </text>
      </svg>

      <button
        onClick={() => setShowBoundary(!showBoundary)}
        className={`mx-auto block px-4 py-2 rounded-lg transition-colors ${
          showBoundary ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700'
        }`}
      >
        {showBoundary ? 'Hide boundary terms' : 'Show boundary ∂M'}
      </button>

      <div className="grid grid-cols-3 gap-3 text-center text-sm">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="font-mono font-bold text-blue-700">ind(D)</div>
          <div className="text-xs text-gray-600">Analytical index</div>
        </div>
        <div className="bg-green-50 p-3 rounded border border-green-200">
          <div className="font-mono font-bold text-green-700">∫_M â</div>
          <div className="text-xs text-gray-600">A-hat genus (curvature)</div>
        </div>
        <div className="bg-red-50 p-3 rounded border border-red-200">
          <div className="font-mono font-bold text-red-700">η(∂M)</div>
          <div className="text-xs text-gray-600">Eta invariant (boundary)</div>
        </div>
      </div>
    </div>
  )
}

// Eta Invariant Visualization
function EtaInvariantViz() {
  const [eigenvalues, setEigenvalues] = useState([
    { value: -2.5, included: true },
    { value: -1.2, included: true },
    { value: -0.3, included: true },
    { value: 0.5, included: true },
    { value: 1.8, included: true },
    { value: 3.1, included: true },
  ])

  const toggleEigenvalue = (index: number) => {
    const newEigenvalues = [...eigenvalues]
    newEigenvalues[index].included = !newEigenvalues[index].included
    setEigenvalues(newEigenvalues)
  }

  const eta = eigenvalues
    .filter(e => e.included && e.value !== 0)
    .reduce((sum, e) => sum + Math.sign(e.value), 0)

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 300 150" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Number line */}
        <line x1="20" y1="75" x2="280" y2="75" stroke="#9CA3AF" strokeWidth="2" />

        {/* Zero marker */}
        <line x1="150" y1="65" x2="150" y2="85" stroke="#000" strokeWidth="2" />
        <text x="150" y="100" textAnchor="middle" fontSize="12">0</text>

        {/* Eigenvalue markers */}
        {eigenvalues.map((ev, i) => {
          const x = 150 + ev.value * 35
          return (
            <g key={i}>
              <circle
                cx={x}
                cy="75"
                r="10"
                fill={ev.included ? (ev.value < 0 ? '#EF4444' : '#3B82F6') : '#E5E7EB'}
                stroke={ev.included ? (ev.value < 0 ? '#DC2626' : '#2563EB') : '#9CA3AF'}
                strokeWidth="2"
                className="cursor-pointer"
                onClick={() => toggleEigenvalue(i)}
              />
              <text
                x={x}
                y="55"
                textAnchor="middle"
                fontSize="10"
                fill={ev.value < 0 ? '#EF4444' : '#3B82F6'}
              >
                {ev.value > 0 ? '+1' : '-1'}
              </text>
              <text
                x={x}
                y="120"
                textAnchor="middle"
                fontSize="9"
                fill="#6B7280"
              >
                λ={ev.value}
              </text>
            </g>
          )
        })}

        {/* Labels */}
        <text x="20" y="100" fontSize="10" fill="#6B7280">−</text>
        <text x="275" y="100" fontSize="10" fill="#6B7280">+</text>
      </svg>

      <div className="text-center text-sm text-gray-600">
        Click eigenvalues to include/exclude them
      </div>

      <div className="bg-purple-50 p-4 rounded-lg text-center">
        <div className="text-lg">
          η = Σ sign(λ) = {eta}
        </div>
        <div className="text-sm text-gray-600 mt-1">
          (Sum of signs of non-zero eigenvalues)
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Eta invariant:</strong> η = Σ_{'{λ≠0}'} sign(λ)|λ|^{'{-s}'}|_{'{s=0}'} (regularized sum)
        <br />
        Measures the asymmetry of the spectrum around zero.
      </div>
    </div>
  )
}

export default function IndexTheoryPage() {
  return (
    <DocumentLayout
      title="Index Theory"
      description="The Atiyah-Singer index theorem, eta invariants, and counting zero modes"
      phase="math"
      currentIndex={7}
      prevLink={{ href: '/office-hours/math/06-orbifolds', title: 'Orbifolds' }}
      nextLink={{ href: '/office-hours/math/08-intersection-theory', title: 'Intersection Theory' }}
    >
      <Section title="1. What is Index Theory?">
        <p className="text-gray-700 mb-4">
          Index theory connects <strong>analysis</strong> (solutions of differential equations) to
          <strong> topology</strong> (global shape of spaces). The central result is that the
          number of solutions is determined by topological invariants!
        </p>

        <Formula label="The Index">
          ind(D) = dim(ker D) - dim(ker D†)
        </Formula>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
          <div className="bg-blue-50 p-3 rounded border border-blue-200">
            <strong>ker D:</strong>
            <div className="text-sm text-blue-700">Solutions to Dψ = 0 (zero modes)</div>
          </div>
          <div className="bg-red-50 p-3 rounded border border-red-200">
            <strong>ker D†:</strong>
            <div className="text-sm text-red-700">Solutions to D†ψ = 0 (adjoint zero modes)</div>
          </div>
        </div>

        <KeyPoint>
          <strong>The index is topological!</strong> It doesn't change under continuous deformations
          of the operator D. This is why we can compute it from topology alone.
        </KeyPoint>
      </Section>

      <Section title="2. The Dirac Index">
        <p className="text-gray-700 mb-4">
          For the <strong>Dirac operator</strong> on spinors, the index counts the difference
          between left-handed and right-handed zero modes:
        </p>

        <InteractiveBox title="Index = Left - Right">
          <IndexViz />
        </InteractiveBox>

        <Formula label="Dirac index on manifold M">
          ind(D) = n₊ - n₋ = ∫_M Â(R) ch(F)
        </Formula>

        <SubSection title="Physical Interpretation">
          <div className="space-y-2 text-gray-700">
            <p>• <strong>n₊:</strong> Number of left-handed fermion zero modes</p>
            <p>• <strong>n₋:</strong> Number of right-handed fermion zero modes</p>
            <p>• <strong>ind(D):</strong> Net chirality — the "excess" of one handedness</p>
          </div>
        </SubSection>

        <Z2Connection
          formula="n₊ - n₋ = 3"
          description="The index on T³/Z₂ gives 3 generations of chiral fermions"
        />
      </Section>

      <Section title="3. The Atiyah-Singer Index Theorem">
        <p className="text-gray-700 mb-4">
          The <strong>Atiyah-Singer theorem</strong> (1963) says that the analytical index
          equals a topological integral:
        </p>

        <Formula label="Atiyah-Singer Theorem">
          ind(D) = ∫_M Â(M) ∧ ch(E)
        </Formula>

        <SubSection title="Ingredients">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">Term</th>
                  <th className="border border-gray-200 p-2">Name</th>
                  <th className="border border-gray-200 p-2">Meaning</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2 font-mono">Â(M)</td>
                  <td className="border border-gray-200 p-2">A-hat genus</td>
                  <td className="border border-gray-200 p-2">Built from Riemann curvature</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2 font-mono">ch(E)</td>
                  <td className="border border-gray-200 p-2">Chern character</td>
                  <td className="border border-gray-200 p-2">Built from gauge field strength</td>
                </tr>
                <tr className="bg-purple-50">
                  <td className="border border-gray-200 p-2 font-mono">∫_M</td>
                  <td className="border border-gray-200 p-2">Integration</td>
                  <td className="border border-gray-200 p-2">Over the manifold M</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>

        <KeyPoint>
          <strong>Analysis = Topology:</strong> The number of solutions to a differential
          equation (left side) equals a topological integral (right side)!
        </KeyPoint>
      </Section>

      <Section title="4. The APS Theorem (with Boundary)">
        <p className="text-gray-700 mb-4">
          When the manifold M has a boundary ∂M, there's an additional correction term:
          the <strong>eta invariant</strong>.
        </p>

        <InteractiveBox title="Atiyah-Patodi-Singer Theorem">
          <APSViz />
        </InteractiveBox>

        <Formula label="APS Theorem">
          ind(D) = ∫_M Â(R) - η(∂M)/2
        </Formula>

        <SubSection title="The Eta Invariant">
          <p className="text-gray-700 mb-4">
            The eta invariant η measures the spectral asymmetry of the Dirac operator
            on the boundary:
          </p>
        </SubSection>

        <InteractiveBox title="Eta Invariant: Spectral Asymmetry">
          <EtaInvariantViz />
        </InteractiveBox>
      </Section>

      <Section title="5. Index Theory for Orbifolds">
        <p className="text-gray-700 mb-4">
          On orbifolds like T³/Z₂, the index theorem gets contributions from fixed points:
        </p>

        <Formula label="Orbifold Index">
          ind(D) = ∫_{'{T³/Z₂}'} Â + Σ_{'{fixed}'} η_p / 2
        </Formula>

        <div className="grid grid-cols-2 gap-4 my-4">
          <div className="bg-blue-50 p-3 rounded border border-blue-200">
            <div className="font-medium text-blue-800">Bulk contribution</div>
            <div className="text-sm text-gray-600">∫ Â over the smooth part</div>
          </div>
          <div className="bg-red-50 p-3 rounded border border-red-200">
            <div className="font-medium text-red-800">Fixed point contributions</div>
            <div className="text-sm text-gray-600">Eta invariants at the 8 singularities</div>
          </div>
        </div>

        <Z2Connection
          formula="η contributions"
          description="Each of the 8 fixed points on T³/Z₂ contributes to the index"
        />
      </Section>

      <Section title="6. Connection to Z² Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="ind(D) = 3"
            description="Index theorem on T³/Z₂ gives exactly 3 generations of fermions"
          />
          <Z2Connection
            formula="η invariant"
            description="Boundary corrections important for D-brane physics"
          />
          <Z2Connection
            formula="Â genus"
            description="Gravitational contribution to anomalies"
          />
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Index Theory Matters</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Generation counting:</strong> Index = number of fermion generations</li>
            <li>• <strong>Anomaly cancellation:</strong> Related to consistency of the theory</li>
            <li>• <strong>Topological protection:</strong> Index is stable under perturbations</li>
            <li>• <strong>D-brane charges:</strong> Counted by K-theory and indices</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>If a Dirac operator has 5 left-handed and 2 right-handed zero modes, what is the index?</li>
          <li>The Â genus of a 4-torus T⁴ is 0. What does this tell us about the Dirac index?</li>
          <li>Why is the index an integer? (Hint: dimensions of vector spaces)</li>
          <li>For the sphere S², show that χ(S²) = 2 using V - E + F for a triangulation.</li>
          <li>The eta invariant is regularized. Why is the naive sum Σ sign(λ) problematic?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
