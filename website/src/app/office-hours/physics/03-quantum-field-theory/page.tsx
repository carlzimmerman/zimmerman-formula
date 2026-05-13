'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Feynman Diagram Builder
function FeynmanDiagramViz() {
  const [process, setProcess] = useState<'electronPhoton' | 'electronElectron' | 'pairAnnihilation'>('electronPhoton')

  const diagrams = {
    electronPhoton: {
      title: 'Electron-Photon Vertex',
      description: 'Basic QED interaction: e- emits or absorbs a photon',
      amplitude: '-i * e * gamma^mu',
    },
    electronElectron: {
      title: 'Electron-Electron Scattering (Moller)',
      description: 'Two electrons exchange a virtual photon',
      amplitude: '|M|^2 ~ e^4 / q^4',
    },
    pairAnnihilation: {
      title: 'Pair Annihilation',
      description: 'Electron-positron annihilate into two photons',
      amplitude: 'e+ + e- -> gamma + gamma',
    },
  }

  const current = diagrams[process]

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-2">
        {(Object.keys(diagrams) as Array<keyof typeof diagrams>).map((key) => (
          <button
            key={key}
            onClick={() => setProcess(key)}
            className={`px-3 py-1 text-sm rounded transition-colors ${
              process === key
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
            }`}
          >
            {diagrams[key].title.split(' ')[0]}
          </button>
        ))}
      </div>

      <svg viewBox="0 0 200 120" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {process === 'electronPhoton' && (
          <g>
            {/* Incoming electron */}
            <line x1="30" y1="90" x2="100" y2="60" stroke="#3B82F6" strokeWidth="2" />
            <polygon points="70,72 68,78 75,75" fill="#3B82F6" />

            {/* Outgoing electron */}
            <line x1="100" y1="60" x2="170" y2="90" stroke="#3B82F6" strokeWidth="2" />
            <polygon points="140,78 143,72 135,75" fill="#3B82F6" />

            {/* Photon (wavy line) */}
            <path d="M 100 60 Q 105 50, 110 55 Q 115 60, 120 55 Q 125 50, 130 55 Q 135 60, 140 55 Q 145 50, 150 55 Q 155 60, 160 55 L 170 30"
                  fill="none" stroke="#FBBF24" strokeWidth="2" />

            {/* Vertex */}
            <circle cx="100" cy="60" r="4" fill="#EF4444" />

            {/* Labels */}
            <text x="20" y="95" fontSize="10" fill="#3B82F6">e-</text>
            <text x="175" y="95" fontSize="10" fill="#3B82F6">e-</text>
            <text x="175" y="30" fontSize="10" fill="#FBBF24">gamma</text>
            <text x="100" y="75" fontSize="8" fill="#EF4444">vertex</text>
          </g>
        )}

        {process === 'electronElectron' && (
          <g>
            {/* Electron 1 */}
            <line x1="30" y1="30" x2="80" y2="60" stroke="#3B82F6" strokeWidth="2" />
            <line x1="80" y1="60" x2="170" y2="30" stroke="#3B82F6" strokeWidth="2" />

            {/* Electron 2 */}
            <line x1="30" y1="90" x2="80" y2="60" stroke="#3B82F6" strokeWidth="2" />
            <line x1="80" y1="60" x2="170" y2="90" stroke="#3B82F6" strokeWidth="2" />

            {/* Virtual photon */}
            <path d="M 80 60 Q 90 55, 95 60 Q 100 65, 105 60 Q 110 55, 115 60 L 120 60"
                  fill="none" stroke="#FBBF24" strokeWidth="2" strokeDasharray="3,2" />

            {/* Vertices */}
            <circle cx="80" cy="60" r="3" fill="#EF4444" />
            <circle cx="120" cy="60" r="3" fill="#EF4444" />

            {/* Labels */}
            <text x="20" y="28" fontSize="10" fill="#3B82F6">e-</text>
            <text x="20" y="95" fontSize="10" fill="#3B82F6">e-</text>
            <text x="175" y="28" fontSize="10" fill="#3B82F6">e-</text>
            <text x="175" y="95" fontSize="10" fill="#3B82F6">e-</text>
            <text x="90" y="50" fontSize="8" fill="#FBBF24">gamma*</text>
          </g>
        )}

        {process === 'pairAnnihilation' && (
          <g>
            {/* Incoming electron */}
            <line x1="30" y1="30" x2="100" y2="60" stroke="#3B82F6" strokeWidth="2" />

            {/* Incoming positron */}
            <line x1="30" y1="90" x2="100" y2="60" stroke="#EF4444" strokeWidth="2" />

            {/* Outgoing photons */}
            <path d="M 100 60 Q 110 50, 115 55 Q 120 60, 125 55 Q 130 50, 135 55 Q 140 60, 145 55 L 170 30"
                  fill="none" stroke="#FBBF24" strokeWidth="2" />
            <path d="M 100 60 Q 110 70, 115 65 Q 120 60, 125 65 Q 130 70, 135 65 Q 140 60, 145 65 L 170 90"
                  fill="none" stroke="#FBBF24" strokeWidth="2" />

            {/* Vertex */}
            <circle cx="100" cy="60" r="4" fill="#8B5CF6" />

            {/* Labels */}
            <text x="20" y="28" fontSize="10" fill="#3B82F6">e-</text>
            <text x="20" y="95" fontSize="10" fill="#EF4444">e+</text>
            <text x="175" y="28" fontSize="10" fill="#FBBF24">gamma</text>
            <text x="175" y="95" fontSize="10" fill="#FBBF24">gamma</text>
          </g>
        )}
      </svg>

      <div className="bg-gray-50 p-3 rounded">
        <div className="font-medium text-gray-900">{current.title}</div>
        <div className="text-sm text-gray-600 mt-1">{current.description}</div>
        <div className="font-mono text-sm text-purple-700 mt-2">Amplitude: {current.amplitude}</div>
      </div>

      <div className="grid grid-cols-3 gap-2 text-xs text-center">
        <div className="bg-blue-50 p-2 rounded">
          <div className="text-blue-700 font-medium">Solid line</div>
          <div className="text-gray-600">Fermion (e-, e+)</div>
        </div>
        <div className="bg-yellow-50 p-2 rounded">
          <div className="text-yellow-700 font-medium">Wavy line</div>
          <div className="text-gray-600">Photon</div>
        </div>
        <div className="bg-red-50 p-2 rounded">
          <div className="text-red-700 font-medium">Dot</div>
          <div className="text-gray-600">Vertex (-ie*gamma)</div>
        </div>
      </div>
    </div>
  )
}

// Propagator Visualization
function PropagatorViz() {
  const [particleType, setParticleType] = useState<'scalar' | 'fermion' | 'photon'>('scalar')
  const [momentum, setMomentum] = useState(2)
  const [mass, setMass] = useState(1)

  const p2 = momentum ** 2
  const m2 = mass ** 2

  const propagators = {
    scalar: {
      formula: 'i / (p^2 - m^2 + i*epsilon)',
      value: 1 / (p2 - m2 + 0.001),
      description: 'Klein-Gordon propagator for spin-0 particles (Higgs)',
    },
    fermion: {
      formula: 'i * (p-slash + m) / (p^2 - m^2 + i*epsilon)',
      value: (momentum + mass) / (p2 - m2 + 0.001),
      description: 'Dirac propagator for spin-1/2 particles (electrons, quarks)',
    },
    photon: {
      formula: '-i * g_mu,nu / (p^2 + i*epsilon)',
      value: 1 / (p2 + 0.001),
      description: 'Photon propagator in Feynman gauge (massless)',
    },
  }

  const current = propagators[particleType]

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-2">
        {(Object.keys(propagators) as Array<keyof typeof propagators>).map((key) => (
          <button
            key={key}
            onClick={() => setParticleType(key)}
            className={`px-4 py-2 text-sm rounded transition-colors ${
              particleType === key
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
            }`}
          >
            {key.charAt(0).toUpperCase() + key.slice(1)}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Momentum |p| = {momentum}
          </label>
          <input
            type="range"
            min="0.1"
            max="5"
            step="0.1"
            value={momentum}
            onChange={(e) => setMomentum(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Mass m = {mass} {particleType === 'photon' && '(fixed at 0)'}
          </label>
          <input
            type="range"
            min="0"
            max="3"
            step="0.1"
            value={particleType === 'photon' ? 0 : mass}
            onChange={(e) => setMass(Number(e.target.value))}
            className="w-full"
            disabled={particleType === 'photon'}
          />
        </div>
      </div>

      <svg viewBox="0 0 200 100" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Propagator line */}
        {particleType === 'scalar' && (
          <line x1="30" y1="50" x2="170" y2="50" stroke="#8B5CF6" strokeWidth="3" strokeDasharray="8,4" />
        )}
        {particleType === 'fermion' && (
          <g>
            <line x1="30" y1="50" x2="170" y2="50" stroke="#3B82F6" strokeWidth="3" />
            <polygon points="100,50 90,45 90,55" fill="#3B82F6" />
          </g>
        )}
        {particleType === 'photon' && (
          <path d="M 30 50 Q 45 35, 60 50 Q 75 65, 90 50 Q 105 35, 120 50 Q 135 65, 150 50 Q 165 35, 170 50"
                fill="none" stroke="#FBBF24" strokeWidth="3" />
        )}

        {/* Momentum label */}
        <text x="100" y="30" fontSize="12" textAnchor="middle" fill="#6B7280">p</text>
        <line x1="60" y1="35" x2="140" y2="35" stroke="#6B7280" strokeWidth="1" markerEnd="url(#arrow)" />

        {/* Endpoints */}
        <circle cx="30" cy="50" r="5" fill="#374151" />
        <circle cx="170" cy="50" r="5" fill="#374151" />
      </svg>

      <div className="bg-purple-50 p-4 rounded border border-purple-200">
        <div className="font-mono text-center text-lg text-purple-800">{current.formula}</div>
        <div className="text-sm text-gray-600 text-center mt-2">{current.description}</div>
      </div>

      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-500">p^2</div>
          <div className="font-mono">{p2.toFixed(2)}</div>
        </div>
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-500">m^2</div>
          <div className="font-mono">{(particleType === 'photon' ? 0 : m2).toFixed(2)}</div>
        </div>
        <div className={`p-2 rounded ${Math.abs(p2 - m2) < 0.5 ? 'bg-red-50' : 'bg-green-50'}`}>
          <div className="text-gray-500">On-shell?</div>
          <div className="font-mono">{Math.abs(p2 - (particleType === 'photon' ? 0 : m2)) < 0.5 ? 'Yes (pole!)' : 'No (virtual)'}</div>
        </div>
      </div>

      {Math.abs(p2 - (particleType === 'photon' ? 0 : m2)) < 0.5 && (
        <div className="bg-amber-50 p-3 rounded text-sm border border-amber-200">
          <strong>Near the pole!</strong> When p^2 = m^2, the particle is "on-shell" (real).
          The propagator diverges, but this is regulated by the i*epsilon prescription.
        </div>
      )}
    </div>
  )
}

// Vacuum Fluctuations Visualization
function VacuumFluctuationsViz() {
  const [showPairs, setShowPairs] = useState(true)
  const [energyScale, setEnergyScale] = useState(1)

  // Generate random "virtual pairs"
  const pairs = Array.from({ length: Math.floor(energyScale * 5) }, (_, i) => ({
    x: 30 + Math.random() * 140,
    y: 20 + Math.random() * 60,
    size: Math.random() * 8 + 4,
    lifetime: Math.random(),
  }))

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Energy scale: {energyScale.toFixed(1)} (higher = more fluctuations)
          </label>
          <input
            type="range"
            min="0.5"
            max="3"
            step="0.1"
            value={energyScale}
            onChange={(e) => setEnergyScale(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="showPairs"
            checked={showPairs}
            onChange={(e) => setShowPairs(e.target.checked)}
            className="rounded mr-2"
          />
          <label htmlFor="showPairs" className="text-sm text-gray-700">
            Show virtual pairs
          </label>
        </div>
      </div>

      <svg viewBox="0 0 200 100" className="w-full max-w-md mx-auto bg-gray-900 border border-gray-700 rounded">
        {/* Background "energy" */}
        <defs>
          <radialGradient id="vacuumGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="rgba(139, 92, 246, 0.3)" />
            <stop offset="100%" stopColor="rgba(0, 0, 0, 0)" />
          </radialGradient>
        </defs>
        <rect x="0" y="0" width="200" height="100" fill="url(#vacuumGlow)" />

        {/* Virtual pairs */}
        {showPairs && pairs.map((pair, i) => (
          <g key={i} opacity={pair.lifetime}>
            {/* Electron */}
            <circle cx={pair.x - pair.size/2} cy={pair.y} r={pair.size/3} fill="#3B82F6" />
            {/* Positron */}
            <circle cx={pair.x + pair.size/2} cy={pair.y} r={pair.size/3} fill="#EF4444" />
            {/* Connection */}
            <line x1={pair.x - pair.size/2} y1={pair.y} x2={pair.x + pair.size/2} y2={pair.y}
                  stroke="rgba(255,255,255,0.3)" strokeWidth="1" strokeDasharray="2,1" />
          </g>
        ))}

        {/* Labels */}
        <text x="100" y="95" fontSize="8" textAnchor="middle" fill="#9CA3AF">
          Virtual particle-antiparticle pairs
        </text>
      </svg>

      <div className="grid grid-cols-2 gap-3 text-center text-sm">
        <div className="bg-blue-50 p-3 rounded">
          <div className="text-gray-600 mb-1">Uncertainty Principle</div>
          <div className="font-mono text-sm">Delta E * Delta t &gt;= h-bar/2</div>
        </div>
        <div className="bg-purple-50 p-3 rounded">
          <div className="text-gray-600 mb-1">Zero-Point Energy</div>
          <div className="font-mono text-sm">E_0 = (1/2) h-bar * omega</div>
        </div>
      </div>

      <KeyPoint>
        <strong>The vacuum is not empty!</strong> Virtual particles constantly appear and disappear.
        This is observable through the Casimir effect and the Lamb shift.
      </KeyPoint>
    </div>
  )
}

export default function QuantumFieldTheoryPage() {
  return (
    <DocumentLayout
      title="Quantum Field Theory"
      description="Fields, particles, and the quantum vacuum"
      phase="physics"
      currentIndex={13}
      prevLink={{ href: '/office-hours/physics/02-quantum-mechanics', title: 'Quantum Mechanics' }}
      nextLink={{ href: '/office-hours/physics/04-gauge-theory', title: 'Gauge Theory' }}
    >
      <Section title="1. From Particles to Fields">
        <p className="text-gray-700 mb-4">
          Quantum Field Theory (QFT) unifies quantum mechanics with special relativity.
          Instead of particles, the fundamental objects are <strong>quantum fields</strong> that permeate all of spacetime.
        </p>

        <KeyPoint>
          <strong>Particles are excitations of fields!</strong> An electron is a quantum of the electron field,
          just as a photon is a quantum of the electromagnetic field.
        </KeyPoint>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
          <div className="bg-gray-50 p-4 rounded">
            <div className="font-medium text-gray-800 mb-2">Quantum Mechanics</div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>* Fixed number of particles</li>
              <li>* Particles are fundamental</li>
              <li>* Non-relativistic</li>
            </ul>
          </div>
          <div className="bg-blue-50 p-4 rounded border border-blue-200">
            <div className="font-medium text-blue-800 mb-2">Quantum Field Theory</div>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>* Particle creation/annihilation</li>
              <li>* Fields are fundamental</li>
              <li>* Fully relativistic</li>
            </ul>
          </div>
        </div>
      </Section>

      <Section title="2. The Lagrangian Density">
        <p className="text-gray-700 mb-4">
          QFT is formulated using the Lagrangian density L. The action is:
        </p>

        <Formula label="Action in Field Theory">
          S = integral of L d^4x
        </Formula>

        <SubSection title="Example: Free Scalar Field">
          <Formula label="Klein-Gordon Lagrangian">
            L = (1/2)(partial_mu phi)(partial^mu phi) - (1/2)m^2 phi^2
          </Formula>
          <p className="text-gray-700 mt-4">
            This describes a spin-0 particle of mass m (like the Higgs boson before symmetry breaking).
          </p>
        </SubSection>

        <SubSection title="Example: Dirac Field">
          <Formula label="Dirac Lagrangian">
            L = psi-bar (i*gamma^mu partial_mu - m) psi
          </Formula>
          <p className="text-gray-700 mt-4">
            This describes spin-1/2 fermions (electrons, quarks).
          </p>
        </SubSection>
      </Section>

      <Section title="3. Feynman Diagrams">
        <p className="text-gray-700 mb-4">
          <strong>Feynman diagrams</strong> are pictorial representations of terms in perturbation theory.
          Each diagram corresponds to a mathematical expression for the scattering amplitude.
        </p>

        <InteractiveBox title="Feynman Diagram Examples">
          <FeynmanDiagramViz />
        </InteractiveBox>

        <SubSection title="Feynman Rules">
          <div className="space-y-2 text-gray-700">
            <p>* <strong>External lines:</strong> Incoming/outgoing particles</p>
            <p>* <strong>Internal lines:</strong> Virtual particles (propagators)</p>
            <p>* <strong>Vertices:</strong> Interaction points (coupling constants)</p>
            <p>* <strong>Loops:</strong> Integrate over all internal momenta</p>
          </div>
        </SubSection>
      </Section>

      <Section title="4. Propagators">
        <p className="text-gray-700 mb-4">
          The <strong>propagator</strong> describes how a particle moves from one point to another.
          In momentum space, it encodes the particle's mass and spin.
        </p>

        <InteractiveBox title="Propagators for Different Particles">
          <PropagatorViz />
        </InteractiveBox>

        <KeyPoint>
          The propagator has a <strong>pole</strong> at p^2 = m^2. This is where the particle is "on-shell"
          (physical). Virtual particles can be off-shell (p^2 != m^2).
        </KeyPoint>
      </Section>

      <Section title="5. The Quantum Vacuum">
        <p className="text-gray-700 mb-4">
          In QFT, the vacuum is not empty. The uncertainty principle allows virtual particles
          to briefly exist, creating <strong>vacuum fluctuations</strong>.
        </p>

        <InteractiveBox title="Vacuum Fluctuations">
          <VacuumFluctuationsViz />
        </InteractiveBox>

        <SubSection title="Observable Effects">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
            <div className="bg-gray-50 p-3 rounded">
              <div className="font-medium">Casimir Effect</div>
              <div className="text-sm text-gray-600">Two metal plates attract due to vacuum fluctuations</div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <div className="font-medium">Lamb Shift</div>
              <div className="text-sm text-gray-600">Energy level shift in hydrogen from vacuum polarization</div>
            </div>
          </div>
        </SubSection>

        <Z2Connection
          formula="&lt;0|phi^2|0&gt; != 0"
          description="The vacuum expectation value of field fluctuations is non-zero"
        />
      </Section>

      <Section title="6. Renormalization">
        <p className="text-gray-700 mb-4">
          Loop diagrams give infinite results! <strong>Renormalization</strong> is the procedure
          of absorbing these infinities into redefined (physical) parameters.
        </p>

        <Formula label="Running Coupling">
          alpha(mu) = alpha(mu_0) + beta * ln(mu/mu_0) + ...
        </Formula>

        <KeyPoint>
          Physical predictions are <strong>finite</strong> and <strong>testable</strong>.
          The fine structure constant alpha ~ 1/137 "runs" with energy scale.
        </KeyPoint>

        <Z2Connection
          formula="alpha^(-1) = 4Z^2 + 3"
          description="The Z^2 framework predicts alpha at a specific scale from geometry"
        />
      </Section>

      <Section title="7. Connection to Z^2 Framework">
        <p className="text-gray-700 mb-4">
          Quantum field theory provides the language for understanding the Standard Model:
        </p>

        <div className="space-y-3">
          <Z2Connection
            formula="Z = integral exp(-S[phi]) D[phi]"
            description="The partition function sums over all field configurations"
          />
          <Z2Connection
            formula="Feynman diagrams"
            description="Perturbation theory organizes calculations by number of vertices"
          />
          <Z2Connection
            formula="Renormalization group"
            description="Physical quantities depend on the energy scale of observation"
          />
        </div>

        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why QFT Matters for Z^2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>* <strong>Field content:</strong> The Standard Model is a specific QFT with particular fields</li>
            <li>* <strong>Interactions:</strong> Determined by gauge symmetry (next document!)</li>
            <li>* <strong>Coupling constants:</strong> The values alpha, alpha_s, etc. require explanation</li>
            <li>* <strong>Vacuum energy:</strong> Connected to the cosmological constant problem</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Derive the Klein-Gordon equation from the scalar field Lagrangian using the Euler-Lagrange equations.</li>
          <li>Count the number of vertices in a 2-to-2 electron scattering diagram at tree level.</li>
          <li>Why does the photon propagator have no mass term (m^2 = 0)?</li>
          <li>The electron self-energy diagram is divergent. What physical quantity does it renormalize?</li>
          <li>At what energy scale does the electromagnetic coupling become strong (alpha ~ 1)?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
