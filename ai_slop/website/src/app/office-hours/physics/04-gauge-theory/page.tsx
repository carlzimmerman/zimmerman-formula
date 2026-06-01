'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Gauge Transformation Visualization
function GaugeTransformViz() {
  const [phase, setPhase] = useState(0)
  const [showGaugeField, setShowGaugeField] = useState(true)

  const phaseRad = (phase * Math.PI) / 180

  // Points on a loop representing local phase
  const numPoints = 8
  const points = Array.from({ length: numPoints }, (_, i) => {
    const angle = (i / numPoints) * 2 * Math.PI
    const localPhase = phaseRad * Math.sin(angle) // position-dependent phase
    return {
      x: 100 + 60 * Math.cos(angle),
      y: 60 + 40 * Math.sin(angle),
      phase: localPhase,
    }
  })

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Local phase rotation: theta(x) = {phase} degrees * sin(x)
          </label>
          <input
            type="range"
            min="0"
            max="180"
            value={phase}
            onChange={(e) => setPhase(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="gaugeField"
            checked={showGaugeField}
            onChange={(e) => setShowGaugeField(e.target.checked)}
            className="rounded mr-2"
          />
          <label htmlFor="gaugeField" className="text-sm text-gray-700">
            Show gauge field A_mu (compensating)
          </label>
        </div>
      </div>

      <svg viewBox="0 0 200 120" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Background grid */}
        <defs>
          <pattern id="gaugeGrid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#E5E7EB" strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect x="0" y="0" width="200" height="120" fill="url(#gaugeGrid)" />

        {/* Draw phase arrows at each point */}
        {points.map((p, i) => (
          <g key={i} transform={`translate(${p.x}, ${p.y})`}>
            {/* Local phase arrow */}
            <line
              x1="0"
              y1="0"
              x2={15 * Math.cos(p.phase)}
              y2={-15 * Math.sin(p.phase)}
              stroke="#3B82F6"
              strokeWidth="2"
            />
            <circle
              cx={15 * Math.cos(p.phase)}
              cy={-15 * Math.sin(p.phase)}
              r="3"
              fill="#3B82F6"
            />

            {/* Gauge field compensation */}
            {showGaugeField && phase > 0 && (
              <line
                x1="0"
                y1="0"
                x2={-10 * Math.cos(p.phase)}
                y2={10 * Math.sin(p.phase)}
                stroke="#EF4444"
                strokeWidth="1.5"
                strokeDasharray="3,2"
              />
            )}
          </g>
        ))}

        {/* Connection path */}
        <path
          d={`M ${points[0].x} ${points[0].y} ${points.map(p => `L ${p.x} ${p.y}`).join(' ')} Z`}
          fill="none"
          stroke="#9CA3AF"
          strokeWidth="1"
          strokeDasharray="4,2"
        />

        {/* Labels */}
        <text x="100" y="15" fontSize="10" textAnchor="middle" fill="#6B7280">Local gauge transformation</text>
        <text x="100" y="115" fontSize="8" textAnchor="middle" fill="#3B82F6">ψ → e^(iθ(x)) · ψ</text>
      </svg>

      <div className="grid grid-cols-2 gap-3 text-center text-sm">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="text-blue-700 font-medium">Global Symmetry</div>
          <div className="text-gray-600">Same phase everywhere: ψ → e^(iθ) · ψ</div>
        </div>
        <div className="bg-purple-50 p-3 rounded border border-purple-200">
          <div className="text-purple-700 font-medium">Local (Gauge) Symmetry</div>
          <div className="text-gray-600">Phase varies: ψ → e^(iθ(x)) · ψ</div>
        </div>
      </div>

      <KeyPoint>
        <strong>Gauge invariance requires the gauge field!</strong>
        To maintain local symmetry, we must introduce a compensating field A_mu (the photon field in QED).
        The gauge field transforms as: A_μ → A_μ + ∂_μθ.
      </KeyPoint>
    </div>
  )
}

// Standard Model Structure Visualization
function StandardModelViz() {
  const [selectedForce, setSelectedForce] = useState<'em' | 'weak' | 'strong' | null>(null)

  const forces = {
    em: {
      name: 'Electromagnetic',
      group: 'U(1)',
      boson: 'Photon (gamma)',
      charge: 'Electric charge Q',
      color: '#FBBF24',
      strength: '1/137',
    },
    weak: {
      name: 'Weak',
      group: 'SU(2)',
      boson: 'W+, W-, Z',
      charge: 'Weak isospin T',
      color: '#3B82F6',
      strength: '~10^-5 (at low E)',
    },
    strong: {
      name: 'Strong',
      group: 'SU(3)',
      boson: '8 Gluons',
      charge: 'Color (r, g, b)',
      color: '#EF4444',
      strength: '~1',
    },
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-2">
        {(Object.keys(forces) as Array<keyof typeof forces>).map((key) => (
          <button
            key={key}
            onClick={() => setSelectedForce(selectedForce === key ? null : key)}
            className={`px-4 py-2 text-sm rounded-lg transition-colors ${
              selectedForce === key
                ? 'text-white'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
            }`}
            style={{ backgroundColor: selectedForce === key ? forces[key].color : undefined }}
          >
            {forces[key].name}
          </button>
        ))}
      </div>

      <svg viewBox="0 0 300 150" className="w-full max-w-xl mx-auto bg-gray-900 rounded-lg">
        {/* Standard Model structure */}

        {/* U(1) - Electromagnetic */}
        <g opacity={selectedForce === null || selectedForce === 'em' ? 1 : 0.3}>
          <circle cx="75" cy="75" r="35" fill="none" stroke="#FBBF24" strokeWidth="3" />
          <text x="75" y="75" fontSize="14" textAnchor="middle" fill="#FBBF24" dominantBaseline="middle">U(1)</text>
          <text x="75" y="120" fontSize="10" textAnchor="middle" fill="#9CA3AF">EM</text>
        </g>

        {/* SU(2) - Weak */}
        <g opacity={selectedForce === null || selectedForce === 'weak' ? 1 : 0.3}>
          <circle cx="150" cy="75" r="45" fill="none" stroke="#3B82F6" strokeWidth="3" />
          <text x="150" y="75" fontSize="14" textAnchor="middle" fill="#3B82F6" dominantBaseline="middle">SU(2)</text>
          <text x="150" y="130" fontSize="10" textAnchor="middle" fill="#9CA3AF">Weak</text>
        </g>

        {/* SU(3) - Strong */}
        <g opacity={selectedForce === null || selectedForce === 'strong' ? 1 : 0.3}>
          <circle cx="225" cy="75" r="55" fill="none" stroke="#EF4444" strokeWidth="3" />
          <text x="225" y="75" fontSize="14" textAnchor="middle" fill="#EF4444" dominantBaseline="middle">SU(3)</text>
          <text x="225" y="140" fontSize="10" textAnchor="middle" fill="#9CA3AF">Strong</text>
        </g>

        {/* Multiplication signs */}
        <text x="112" y="75" fontSize="18" textAnchor="middle" fill="#6B7280" dominantBaseline="middle">x</text>
        <text x="187" y="75" fontSize="18" textAnchor="middle" fill="#6B7280" dominantBaseline="middle">x</text>

        {/* Title */}
        <text x="150" y="20" fontSize="12" textAnchor="middle" fill="#D1D5DB">Standard Model Gauge Group</text>
      </svg>

      {selectedForce && (
        <div className="bg-gray-50 p-4 rounded-lg border" style={{ borderColor: forces[selectedForce].color }}>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div className="text-gray-500">Gauge Group</div>
              <div className="font-mono font-medium">{forces[selectedForce].group}</div>
            </div>
            <div>
              <div className="text-gray-500">Gauge Bosons</div>
              <div className="font-medium">{forces[selectedForce].boson}</div>
            </div>
            <div>
              <div className="text-gray-500">Conserved Charge</div>
              <div className="font-medium">{forces[selectedForce].charge}</div>
            </div>
            <div>
              <div className="text-gray-500">Coupling Strength</div>
              <div className="font-mono">{forces[selectedForce].strength}</div>
            </div>
          </div>
        </div>
      )}

      <Formula label="Standard Model Gauge Group">
        G_SM = SU(3)_C x SU(2)_L x U(1)_Y
      </Formula>

      <div className="grid grid-cols-3 gap-2 text-xs">
        <div className="bg-red-50 p-2 rounded text-center">
          <div className="text-red-700 font-medium">SU(3)_C</div>
          <div className="text-gray-600">8 gluons, 3 colors</div>
          <div className="text-gray-600">Dim: 8</div>
        </div>
        <div className="bg-blue-50 p-2 rounded text-center">
          <div className="text-blue-700 font-medium">SU(2)_L</div>
          <div className="text-gray-600">W+, W-, (Z, gamma)</div>
          <div className="text-gray-600">Dim: 3</div>
        </div>
        <div className="bg-yellow-50 p-2 rounded text-center">
          <div className="text-yellow-700 font-medium">U(1)_Y</div>
          <div className="text-gray-600">Hypercharge</div>
          <div className="text-gray-600">Dim: 1</div>
        </div>
      </div>
    </div>
  )
}

// Yang-Mills Field Strength Visualization
function YangMillsViz() {
  const [nonAbelian, setNonAbelian] = useState(true)
  const [coupling, setCoupling] = useState(1)

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="flex items-center">
          <input
            type="checkbox"
            id="nonAbelian"
            checked={nonAbelian}
            onChange={(e) => setNonAbelian(e.target.checked)}
            className="rounded mr-2"
          />
          <label htmlFor="nonAbelian" className="text-sm text-gray-700">
            Non-Abelian (self-interaction)
          </label>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Coupling g = {coupling.toFixed(1)}
          </label>
          <input
            type="range"
            min="0.1"
            max="2"
            step="0.1"
            value={coupling}
            onChange={(e) => setCoupling(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <svg viewBox="0 0 200 120" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {nonAbelian ? (
          // Non-Abelian: gluon self-interaction
          <g>
            {/* Three-gluon vertex */}
            <line x1="100" y1="30" x2="100" y2="60" stroke="#EF4444" strokeWidth="3" />
            <line x1="100" y1="60" x2="70" y2="90" stroke="#3B82F6" strokeWidth="3" />
            <line x1="100" y1="60" x2="130" y2="90" stroke="#10B981" strokeWidth="3" />
            <circle cx="100" cy="60" r="6" fill="#8B5CF6" />

            {/* Four-gluon vertex */}
            <line x1="160" y1="30" x2="180" y2="60" stroke="#EF4444" strokeWidth="2" />
            <line x1="200" y1="30" x2="180" y2="60" stroke="#3B82F6" strokeWidth="2" />
            <line x1="160" y1="90" x2="180" y2="60" stroke="#10B981" strokeWidth="2" />
            <line x1="200" y1="90" x2="180" y2="60" stroke="#FBBF24" strokeWidth="2" />
            <circle cx="180" cy="60" r="5" fill="#8B5CF6" />

            <text x="100" y="110" fontSize="9" textAnchor="middle" fill="#6B7280">3-gluon</text>
            <text x="180" y="110" fontSize="9" textAnchor="middle" fill="#6B7280">4-gluon</text>
            <text x="100" y="15" fontSize="10" textAnchor="middle" fill="#8B5CF6">Non-Abelian: Gluons interact!</text>
          </g>
        ) : (
          // Abelian: photons don't self-interact
          <g>
            <path d="M 30 60 Q 50 45, 70 60 Q 90 75, 110 60 Q 130 45, 150 60 Q 170 75, 190 60"
                  fill="none" stroke="#FBBF24" strokeWidth="3" />
            <path d="M 30 60 Q 50 75, 70 60 Q 90 45, 110 60 Q 130 75, 150 60"
                  fill="none" stroke="#FBBF24" strokeWidth="3" opacity="0.5" transform="translate(0, 20)" />

            {/* X mark where they would interact */}
            <g transform="translate(110, 70)">
              <line x1="-8" y1="-8" x2="8" y2="8" stroke="#EF4444" strokeWidth="2" />
              <line x1="8" y1="-8" x2="-8" y2="8" stroke="#EF4444" strokeWidth="2" />
            </g>

            <text x="100" y="110" fontSize="10" textAnchor="middle" fill="#6B7280">Photons pass through each other</text>
            <text x="100" y="15" fontSize="10" textAnchor="middle" fill="#FBBF24">Abelian: No self-interaction</text>
          </g>
        )}
      </svg>

      <div className="grid grid-cols-2 gap-3">
        <div className="bg-yellow-50 p-3 rounded border border-yellow-200">
          <div className="font-medium text-yellow-800">Abelian (U(1))</div>
          <div className="font-mono text-sm mt-1">F_mu,nu = partial_mu A_nu - partial_nu A_mu</div>
          <div className="text-xs text-gray-600 mt-1">Photons don't carry charge</div>
        </div>
        <div className="bg-purple-50 p-3 rounded border border-purple-200">
          <div className="font-medium text-purple-800">Non-Abelian (SU(N))</div>
          <div className="font-mono text-sm mt-1">F = dA + g*A^A</div>
          <div className="text-xs text-gray-600 mt-1">Gluons carry color charge!</div>
        </div>
      </div>

      <KeyPoint>
        <strong>Asymptotic freedom:</strong> In non-Abelian theories like QCD, the coupling gets
        <em> weaker</em> at high energies. This is why quarks are "free" inside protons but confined at large distances.
      </KeyPoint>
    </div>
  )
}

export default function GaugeTheoryPage() {
  return (
    <DocumentLayout
      title="Gauge Theory"
      description="Local symmetry, gauge bosons, and the structure of the Standard Model"
      phase="physics"
      currentIndex={14}
      prevLink={{ href: '/office-hours/physics/03-quantum-field-theory', title: 'Quantum Field Theory' }}
      nextLink={{ href: '/office-hours/physics/05-general-relativity', title: 'General Relativity' }}
    >
      <Section title="1. From Global to Local Symmetry">
        <p className="text-gray-700 mb-4">
          A <strong>global symmetry</strong> is a transformation that is the same everywhere.
          A <strong>local (gauge) symmetry</strong> can vary from point to point.
        </p>

        <InteractiveBox title="Local Gauge Transformation">
          <GaugeTransformViz />
        </InteractiveBox>

        <SubSection title="The Gauge Principle">
          <p className="text-gray-700 mb-4">
            To maintain invariance under local transformations, we must introduce a
            <strong> gauge field</strong> that compensates for the varying phase:
          </p>
          <Formula label="Covariant Derivative">
            D_mu = partial_mu + i*g*A_mu
          </Formula>
          <p className="text-gray-700 mt-4">
            The gauge field A_mu transforms to cancel the derivative of the phase:
          </p>
          <Formula>
            A_μ → A_μ - (1/g) ∂_μθ
          </Formula>
        </SubSection>
      </Section>

      <Section title="2. The Standard Model Gauge Group">
        <p className="text-gray-700 mb-4">
          The Standard Model is a gauge theory based on the product of three groups:
        </p>

        <InteractiveBox title="Standard Model Structure">
          <StandardModelViz />
        </InteractiveBox>

        <SubSection title="Gauge Bosons">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2 text-left">Force</th>
                  <th className="border border-gray-200 p-2 text-left">Group</th>
                  <th className="border border-gray-200 p-2 text-left">Bosons</th>
                  <th className="border border-gray-200 p-2 text-left">Mass</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2">Strong</td>
                  <td className="border border-gray-200 p-2 font-mono">SU(3)</td>
                  <td className="border border-gray-200 p-2">8 gluons</td>
                  <td className="border border-gray-200 p-2">0</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Weak</td>
                  <td className="border border-gray-200 p-2 font-mono">SU(2)</td>
                  <td className="border border-gray-200 p-2">W+, W-, Z</td>
                  <td className="border border-gray-200 p-2">80-91 GeV</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">EM</td>
                  <td className="border border-gray-200 p-2 font-mono">U(1)</td>
                  <td className="border border-gray-200 p-2">Photon</td>
                  <td className="border border-gray-200 p-2">0</td>
                </tr>
              </tbody>
            </table>
          </div>

          <KeyPoint>
            <strong>Gauge bosons mediate forces!</strong> The photon mediates electromagnetism,
            W/Z bosons mediate the weak force, and gluons mediate the strong force.
          </KeyPoint>
        </SubSection>
      </Section>

      <Section title="3. Yang-Mills Theory">
        <p className="text-gray-700 mb-4">
          <strong>Yang-Mills theory</strong> extends electromagnetism to non-Abelian gauge groups.
          The key difference: the gauge bosons themselves carry charge!
        </p>

        <InteractiveBox title="Abelian vs Non-Abelian">
          <YangMillsViz />
        </InteractiveBox>

        <SubSection title="The Field Strength Tensor">
          <Formula label="Yang-Mills Field Strength">
            F^a_mu,nu = partial_mu A^a_nu - partial_nu A^a_mu + g * f^abc * A^b_mu * A^c_nu
          </Formula>
          <p className="text-gray-700 mt-4">
            The last term is the non-Abelian contribution. The structure constants f^abc
            encode the commutation relations of the Lie algebra: [T^a, T^b] = i*f^abc*T^c.
          </p>
        </SubSection>

        <Z2Connection
          formula="[T^a, T^b] = i*f^abc*T^c"
          description="The structure constants determine the gluon self-interactions"
        />
      </Section>

      <Section title="4. The Weinberg Angle">
        <p className="text-gray-700 mb-4">
          The electromagnetic and weak forces are unified above the electroweak scale.
          The <strong>Weinberg angle</strong> theta_W parametrizes this mixing:
        </p>

        <Formula label="Weinberg Angle Definition">
          sin^2(theta_W) = 1 - (M_W / M_Z)^2 ~ 0.231
        </Formula>

        <div className="grid grid-cols-2 gap-4 my-4">
          <div className="bg-blue-50 p-4 rounded">
            <div className="font-medium text-blue-800">Before symmetry breaking</div>
            <div className="text-sm text-gray-600 mt-2">
              SU(2)_L x U(1)_Y with W^1, W^2, W^3, B bosons
            </div>
          </div>
          <div className="bg-green-50 p-4 rounded">
            <div className="font-medium text-green-800">After symmetry breaking</div>
            <div className="text-sm text-gray-600 mt-2">
              U(1)_EM with gamma, Z, W+, W- bosons
            </div>
          </div>
        </div>

        <Z2Connection
          formula="sin^2(theta_W) = 3/13"
          description="The Z^2 framework predicts this exact value from orbifold geometry"
        />
      </Section>

      <Section title="5. Spontaneous Symmetry Breaking">
        <p className="text-gray-700 mb-4">
          Gauge bosons should be massless! But W and Z have mass. The <strong>Higgs mechanism</strong>
          gives mass to gauge bosons through spontaneous symmetry breaking.
        </p>

        <Formula label="Higgs Potential">
          V(phi) = -mu^2 |phi|^2 + lambda |phi|^4
        </Formula>

        <div className="bg-purple-50 p-4 rounded my-4">
          <div className="font-medium text-purple-800 mb-2">The Mexican Hat Potential</div>
          <p className="text-sm text-gray-700">
            The Higgs field has a "Mexican hat" potential. The minimum is not at phi = 0,
            so the field acquires a vacuum expectation value (VEV): v ~ 246 GeV.
          </p>
        </div>

        <KeyPoint>
          The Higgs VEV breaks SU(2)_L × U(1)_Y → U(1)_EM.
          The "eaten" Goldstone bosons become the longitudinal modes of the massive W and Z.
        </KeyPoint>
      </Section>

      <Section title="6. Connection to Z^2 Framework">
        <p className="text-gray-700 mb-4">
          The Z^2 framework provides a geometric origin for the Standard Model gauge structure:
        </p>

        <div className="space-y-3">
          <Z2Connection
            formula="G_SM = SU(3) x SU(2) x U(1)"
            description="Emerges from D-branes on the T^6/Z_2 orbifold"
          />
          <Z2Connection
            formula="sin^2(theta_W) = 3/13"
            description="Predicted exactly by brane intersection angles"
          />
          <Z2Connection
            formula="alpha^(-1) = 4Z^2 + 3"
            description="Fine structure constant from geometry"
          />
          <Z2Connection
            formula="T^3/Z_2 chirality"
            description="Z_2 orbifold projection creates chiral fermions"
          />
        </div>

        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Gauge Theory Matters for Z^2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>* <strong>Gauge group:</strong> The specific structure SU(3) x SU(2) x U(1) requires explanation</li>
            <li>* <strong>Coupling constants:</strong> Why alpha ~ 1/137? Why do couplings run?</li>
            <li>* <strong>Weinberg angle:</strong> The Z^2 framework predicts sin^2(theta_W) = 3/13</li>
            <li>* <strong>Chirality:</strong> Why does the weak force only affect left-handed particles?</li>
          </ul>
        </div>
      </Section>

      <Section title="7. Summary: The Gauge Theory Paradigm">
        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2 text-left">Principle</th>
                <th className="border border-gray-200 p-2 text-left">Consequence</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2">Local gauge invariance</td>
                <td className="border border-gray-200 p-2">Requires gauge bosons</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Non-Abelian gauge group</td>
                <td className="border border-gray-200 p-2">Gauge bosons self-interact</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Spontaneous symmetry breaking</td>
                <td className="border border-gray-200 p-2">Massive gauge bosons (W, Z)</td>
              </tr>
              <tr className="bg-purple-50">
                <td className="border border-gray-200 p-2">Z^2 orbifold geometry</td>
                <td className="border border-gray-200 p-2">Standard Model group + couplings</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Show that the covariant derivative D_mu psi transforms covariantly under a gauge transformation.</li>
          <li>Count the number of gauge bosons in SU(3) x SU(2) x U(1). (Hint: 8 + 3 + 1 = 12)</li>
          <li>Why do gluons carry color charge but photons don't carry electric charge?</li>
          <li>Calculate M_W from M_Z = 91 GeV and sin^2(theta_W) = 0.231.</li>
          <li>The Higgs mechanism "eats" 3 Goldstone bosons. Where do they go?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
