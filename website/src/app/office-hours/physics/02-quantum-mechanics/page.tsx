'use client'

import { useState, useEffect } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Wave Function Probability Visualization
function WaveFunctionViz() {
  const [n, setN] = useState(1) // quantum number
  const [showProbability, setShowProbability] = useState(true)

  // Particle in a box: psi_n(x) = sqrt(2/L) * sin(n*pi*x/L)
  const L = 1 // box length
  const points = 100
  const waveData = Array.from({ length: points + 1 }, (_, i) => {
    const x = (i / points) * L
    const psi = Math.sqrt(2 / L) * Math.sin(n * Math.PI * x / L)
    const prob = psi * psi
    return { x, psi, prob }
  })

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Quantum number n = {n}
          </label>
          <input
            type="range"
            min="1"
            max="5"
            value={n}
            onChange={(e) => setN(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            id="showProb"
            checked={showProbability}
            onChange={(e) => setShowProbability(e.target.checked)}
            className="rounded"
          />
          <label htmlFor="showProb" className="text-sm text-gray-700">
            Show probability density |psi|^2
          </label>
        </div>
      </div>

      <svg viewBox="-0.1 -2.5 1.2 5" className="w-full max-w-lg mx-auto bg-white border border-gray-200 rounded">
        {/* Box walls */}
        <rect x="0" y="-2.2" width="0.02" height="4.4" fill="#374151" />
        <rect x="0.98" y="-2.2" width="0.02" height="4.4" fill="#374151" />

        {/* Axes */}
        <line x1="0" y1="0" x2="1" y2="0" stroke="#9CA3AF" strokeWidth="0.01" />

        {/* Wave function */}
        <path
          d={`M ${waveData[0].x} ${-waveData[0].psi} ${waveData.map(d => `L ${d.x} ${-d.psi}`).join(' ')}`}
          fill="none"
          stroke="#3B82F6"
          strokeWidth="0.03"
        />

        {/* Probability density */}
        {showProbability && (
          <path
            d={`M 0 0 ${waveData.map(d => `L ${d.x} ${-d.prob}`).join(' ')} L 1 0 Z`}
            fill="rgba(239, 68, 68, 0.3)"
            stroke="#EF4444"
            strokeWidth="0.02"
          />
        )}

        {/* Labels */}
        <text x="0.5" y="2.3" fontSize="0.1" textAnchor="middle" fill="#6B7280">x</text>
        <text x="-0.05" y="-1.8" fontSize="0.08" fill="#3B82F6">psi</text>
        {showProbability && <text x="-0.05" y="-1.5" fontSize="0.08" fill="#EF4444">|psi|^2</text>}
      </svg>

      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <div className="bg-blue-50 p-2 rounded">
          <div className="text-gray-500 text-xs">Energy Level</div>
          <div className="font-mono">E_n = n^2 h^2 / (8mL^2)</div>
        </div>
        <div className="bg-purple-50 p-2 rounded">
          <div className="text-gray-500 text-xs">Nodes</div>
          <div className="font-mono">{n - 1} nodes</div>
        </div>
        <div className="bg-green-50 p-2 rounded">
          <div className="text-gray-500 text-xs">Wavelength</div>
          <div className="font-mono">lambda = 2L/{n}</div>
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded text-sm">
        <strong>Born Rule:</strong> The probability of finding the particle at position x is |psi(x)|^2.
        Notice higher n states have more nodes where P(x) = 0.
      </div>
    </div>
  )
}

// Spin State Visualization (Bloch Sphere)
function SpinStateViz() {
  const [theta, setTheta] = useState(0)
  const [phi, setPhi] = useState(0)

  const thetaRad = (theta * Math.PI) / 180
  const phiRad = (phi * Math.PI) / 180

  // Probabilities
  const probUp = Math.cos(thetaRad / 2) ** 2
  const probDown = Math.sin(thetaRad / 2) ** 2

  // Bloch sphere coordinates
  const x = Math.sin(thetaRad) * Math.cos(phiRad)
  const y = Math.sin(thetaRad) * Math.sin(phiRad)
  const z = Math.cos(thetaRad)

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            theta = {theta} degrees (polar angle)
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
            phi = {phi} degrees (azimuthal)
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
          <ellipse cx="0" cy="0" rx="1" ry="0.3" fill="none" stroke="#E5E7EB" strokeWidth="0.01" />

          {/* Axes */}
          <line x1="0" y1="-1.2" x2="0" y2="1.2" stroke="#9CA3AF" strokeWidth="0.015" />
          <line x1="-1.2" y1="0" x2="1.2" y2="0" stroke="#9CA3AF" strokeWidth="0.015" />

          {/* State vector (projected to xz plane for visualization) */}
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
          <text x="0" y="-1.25" fontSize="0.15" textAnchor="middle" fill="#3B82F6">|up&gt;</text>
          <text x="0" y="1.35" fontSize="0.15" textAnchor="middle" fill="#EF4444">|down&gt;</text>
        </svg>

        <div className="space-y-3">
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <div className="text-xs text-purple-600 mb-1">Qubit State</div>
            <div className="font-mono text-sm">
              |psi&gt; = cos(theta/2)|up&gt; + e^(i*phi)sin(theta/2)|down&gt;
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div className="bg-blue-50 p-2 rounded text-center">
              <div className="text-xs text-gray-500">P(|up&gt;)</div>
              <div className="font-mono text-lg text-blue-700">{(probUp * 100).toFixed(1)}%</div>
            </div>
            <div className="bg-red-50 p-2 rounded text-center">
              <div className="text-xs text-gray-500">P(|down&gt;)</div>
              <div className="font-mono text-lg text-red-700">{(probDown * 100).toFixed(1)}%</div>
            </div>
          </div>

          <div className="text-xs text-gray-600">
            <div>Expectation values:</div>
            <div className="font-mono">
              &lt;sigma_z&gt; = {z.toFixed(2)}, &lt;sigma_x&gt; = {x.toFixed(2)}
            </div>
          </div>
        </div>
      </div>

      <KeyPoint>
        <strong>Spin-1/2:</strong> A rotation of 360 degrees gives |psi&gt; = -|psi&gt;.
        Only a 720 degree rotation returns to the original state! This is the signature of a spinor.
      </KeyPoint>
    </div>
  )
}

// Double Slit Visualization
function DoubleSlitViz() {
  const [slitSeparation, setSlitSeparation] = useState(2)
  const [wavelength, setWavelength] = useState(1)
  const [showInterference, setShowInterference] = useState(true)

  const screenWidth = 200
  const points = 100

  // Interference pattern: I = 4 * I0 * cos^2(pi * d * x / (lambda * L))
  const pattern = Array.from({ length: points + 1 }, (_, i) => {
    const x = (i / points - 0.5) * 10 // -5 to 5
    const phase = (Math.PI * slitSeparation * x) / (wavelength * 10)
    const intensity = showInterference ? Math.cos(phase) ** 2 : 0.5
    return { x: i / points * screenWidth, intensity }
  })

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Slit separation: d = {slitSeparation}
          </label>
          <input
            type="range"
            min="1"
            max="5"
            step="0.5"
            value={slitSeparation}
            onChange={(e) => setSlitSeparation(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Wavelength: lambda = {wavelength}
          </label>
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.25"
            value={wavelength}
            onChange={(e) => setWavelength(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="interference"
            checked={showInterference}
            onChange={(e) => setShowInterference(e.target.checked)}
            className="rounded mr-2"
          />
          <label htmlFor="interference" className="text-sm text-gray-700">
            Quantum interference
          </label>
        </div>
      </div>

      <svg viewBox="0 0 250 100" className="w-full max-w-xl mx-auto bg-gray-900 rounded">
        {/* Source */}
        <circle cx="20" cy="50" r="5" fill="#FBBF24" />
        <text x="20" y="70" fontSize="8" textAnchor="middle" fill="#9CA3AF">Source</text>

        {/* Barrier with slits */}
        <rect x="80" y="0" width="5" height="40" fill="#6B7280" />
        <rect x="80" y="60" width="5" height="40" fill="#6B7280" />
        <rect x="80" y="45" width="5" height="10" fill="#6B7280" />

        {/* Waves from source to slits */}
        {[1, 2, 3].map(i => (
          <circle key={i} cx="20" cy="50" r={i * 20} fill="none" stroke="rgba(251, 191, 36, 0.3)" strokeWidth="1" />
        ))}

        {/* Screen */}
        <rect x="200" y="5" width="5" height="90" fill="#374151" />

        {/* Interference pattern */}
        <g transform="translate(205, 5)">
          {pattern.map((p, i) => (
            <rect
              key={i}
              x="0"
              y={(i / points) * 90}
              width={p.intensity * 30}
              height={90 / points + 1}
              fill={showInterference ? `rgba(59, 130, 246, ${p.intensity})` : 'rgba(59, 130, 246, 0.5)'}
            />
          ))}
        </g>

        {/* Labels */}
        <text x="82" y="95" fontSize="8" textAnchor="middle" fill="#9CA3AF">Slits</text>
        <text x="220" y="95" fontSize="8" textAnchor="middle" fill="#9CA3AF">Screen</text>
      </svg>

      <div className="grid grid-cols-2 gap-3 text-center text-sm">
        <div className="bg-blue-50 p-3 rounded">
          <div className="text-gray-600 mb-1">Interference Condition</div>
          <div className="font-mono">Maxima: d*sin(theta) = n*lambda</div>
        </div>
        <div className="bg-purple-50 p-3 rounded">
          <div className="text-gray-600 mb-1">Wave-Particle Duality</div>
          <div className="text-sm">Each particle interferes with itself!</div>
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded text-sm">
        <strong>The mystery:</strong> Even when particles are sent one at a time, the interference pattern
        builds up! The particle goes through "both slits" as a wave, but is detected at one spot as a particle.
      </div>
    </div>
  )
}

export default function QuantumMechanicsPage() {
  return (
    <DocumentLayout
      title="Quantum Mechanics"
      description="Wave functions, operators, and the foundations of quantum physics"
      phase="physics"
      currentIndex={12}
      prevLink={{ href: '/office-hours/physics/01-special-relativity', title: 'Special Relativity' }}
      nextLink={{ href: '/office-hours/physics/03-quantum-field-theory', title: 'Quantum Field Theory' }}
    >
      <Section title="1. The Wave Function">
        <p className="text-gray-700 mb-4">
          In quantum mechanics, the state of a particle is described by a <strong>wave function</strong> psi(x, t).
          The wave function is complex-valued and contains all information about the system.
        </p>

        <Formula label="Schrodinger Equation">
          i * h-bar * (partial psi / partial t) = H * psi
        </Formula>

        <KeyPoint>
          <strong>The Born Rule:</strong> The probability of finding a particle at position x is |psi(x)|^2.
          The wave function must be normalized: integral of |psi|^2 dx = 1.
        </KeyPoint>

        <InteractiveBox title="Particle in a Box">
          <WaveFunctionViz />
        </InteractiveBox>
      </Section>

      <Section title="2. Operators and Observables">
        <p className="text-gray-700 mb-4">
          Physical quantities are represented by <strong>Hermitian operators</strong>.
          The eigenvalues are the possible measurement outcomes.
        </p>

        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2 text-left">Observable</th>
                <th className="border border-gray-200 p-2 text-left">Operator</th>
                <th className="border border-gray-200 p-2 text-left">Eigenvalue Equation</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2">Position</td>
                <td className="border border-gray-200 p-2 font-mono">x-hat = x</td>
                <td className="border border-gray-200 p-2 font-mono">x|x&gt; = x|x&gt;</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Momentum</td>
                <td className="border border-gray-200 p-2 font-mono">p-hat = -i*h-bar * d/dx</td>
                <td className="border border-gray-200 p-2 font-mono">p|p&gt; = p|p&gt;</td>
              </tr>
              <tr className="bg-blue-50">
                <td className="border border-gray-200 p-2">Energy</td>
                <td className="border border-gray-200 p-2 font-mono">H = p^2/(2m) + V</td>
                <td className="border border-gray-200 p-2 font-mono">H|E&gt; = E|E&gt;</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Angular momentum</td>
                <td className="border border-gray-200 p-2 font-mono">L = r x p</td>
                <td className="border border-gray-200 p-2 font-mono">L_z|l,m&gt; = m*h-bar|l,m&gt;</td>
              </tr>
            </tbody>
          </table>
        </div>

        <SubSection title="The Uncertainty Principle">
          <Formula label="Heisenberg Uncertainty">
            Delta x * Delta p &gt;= h-bar / 2
          </Formula>
          <p className="text-gray-700 mt-4">
            This is not a measurement limitation but a fundamental property of nature!
            It arises from [x, p] = i * h-bar.
          </p>
        </SubSection>
      </Section>

      <Section title="3. Spin and the Pauli Matrices">
        <p className="text-gray-700 mb-4">
          <strong>Spin</strong> is intrinsic angular momentum with no classical analog.
          Electrons have spin-1/2, meaning they can be in states |up&gt; or |down&gt;.
        </p>

        <InteractiveBox title="Spin-1/2 on the Bloch Sphere">
          <SpinStateViz />
        </InteractiveBox>

        <SubSection title="The Pauli Matrices">
          <div className="grid grid-cols-3 gap-3 my-4 text-center">
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-sm text-gray-600 mb-1">sigma_x</div>
              <div className="font-mono text-sm">
                [0 1]<br />[1 0]
              </div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-sm text-gray-600 mb-1">sigma_y</div>
              <div className="font-mono text-sm">
                [0 -i]<br />[i  0]
              </div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <div className="text-sm text-gray-600 mb-1">sigma_z</div>
              <div className="font-mono text-sm">
                [1  0]<br />[0 -1]
              </div>
            </div>
          </div>
          <p className="text-gray-700">
            These satisfy sigma_i * sigma_j = delta_ij * I + i * epsilon_ijk * sigma_k
          </p>
        </SubSection>
      </Section>

      <Section title="4. Wave-Particle Duality">
        <p className="text-gray-700 mb-4">
          The <strong>double-slit experiment</strong> reveals the fundamental mystery of quantum mechanics:
          matter exhibits both wave and particle properties.
        </p>

        <InteractiveBox title="Double-Slit Interference">
          <DoubleSlitViz />
        </InteractiveBox>

        <SubSection title="De Broglie Wavelength">
          <Formula>
            lambda = h / p
          </Formula>
          <p className="text-gray-700 mt-4">
            Every particle has an associated wavelength! For an electron at 100 eV, lambda ~ 0.1 nm.
          </p>
        </SubSection>
      </Section>

      <Section title="5. The Path Integral Formulation">
        <p className="text-gray-700 mb-4">
          Feynman showed that quantum mechanics can be formulated as a sum over all possible paths:
        </p>

        <Formula label="Path Integral">
          &lt;x_f|x_i&gt; = integral of exp(i*S[path]/h-bar) D[path]
        </Formula>

        <KeyPoint>
          Every path contributes with a phase e^(iS/h-bar). The classical path dominates because
          nearby paths have similar phases that add constructively.
        </KeyPoint>

        <Z2Connection
          formula="Z = integral exp(-S_E) D[fields]"
          description="This extends to quantum field theory as the partition function"
        />
      </Section>

      <Section title="6. Connection to Z^2 Framework">
        <p className="text-gray-700 mb-4">
          Quantum mechanics provides the foundation for understanding the Z^2 framework:
        </p>

        <div className="space-y-3">
          <Z2Connection
            formula="|psi|^2 = probability"
            description="The Born rule connects complex amplitudes to observable probabilities"
          />
          <Z2Connection
            formula="[x, p] = i*h-bar"
            description="Commutation relations define the quantum algebra"
          />
          <Z2Connection
            formula="SU(2) for spin"
            description="Spin-1/2 transforms under SU(2), the double cover of SO(3)"
          />
        </div>

        <div className="bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Quantum Mechanics Matters for Z^2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>* <strong>Complex amplitudes:</strong> The fundamental description uses complex numbers</li>
            <li>* <strong>Spin:</strong> Fermions require spinor representations of the Lorentz group</li>
            <li>* <strong>Path integrals:</strong> The language of quantum field theory</li>
            <li>* <strong>Symmetries:</strong> Quantum numbers are eigenvalues of symmetry generators</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>For the particle in a box, show that the energy levels are E_n = n^2 * pi^2 * h-bar^2 / (2mL^2).</li>
          <li>Verify that the Pauli matrices satisfy [sigma_x, sigma_y] = 2i*sigma_z.</li>
          <li>Calculate the de Broglie wavelength of an electron with kinetic energy 100 eV.</li>
          <li>Show that sigma_x^2 = sigma_y^2 = sigma_z^2 = I (the identity matrix).</li>
          <li>For a spin-1/2 particle in state |+x&gt;, calculate the probability of measuring spin up in the z-direction.</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
