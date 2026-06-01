'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Cosmic Pie Chart Visualization - The Z2 prediction
function CosmicPieChartViz() {
  const [showZ2, setShowZ2] = useState(true)

  // Z2 prediction: Omega_Lambda = 13/19, Omega_M = 6/19
  const z2Lambda = 13 / 19 // ~0.6842
  const z2Matter = 6 / 19 // ~0.3158

  // Observed values (Planck 2018)
  const obsLambda = 0.685
  const obsMatter = 0.315

  const values = showZ2
    ? { lambda: z2Lambda, matter: z2Matter, label: 'Z2 Prediction' }
    : { lambda: obsLambda, matter: obsMatter, label: 'Observed (Planck)' }

  // Pie chart calculations
  const lambdaAngle = values.lambda * 360
  const matterAngle = values.matter * 360

  const polarToCart = (angle: number, r: number) => ({
    x: 100 + r * Math.sin((angle * Math.PI) / 180),
    y: 100 - r * Math.cos((angle * Math.PI) / 180)
  })

  const lambdaPath = () => {
    const start = polarToCart(0, 80)
    const end = polarToCart(lambdaAngle, 80)
    const largeArc = lambdaAngle > 180 ? 1 : 0
    return `M 100,100 L ${start.x},${start.y} A 80,80 0 ${largeArc},1 ${end.x},${end.y} Z`
  }

  const matterPath = () => {
    const start = polarToCart(lambdaAngle, 80)
    const end = polarToCart(360, 80)
    const largeArc = matterAngle > 180 ? 1 : 0
    return `M 100,100 L ${start.x},${start.y} A 80,80 0 ${largeArc},1 ${end.x},${end.y} Z`
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-4">
        <button
          onClick={() => setShowZ2(true)}
          className={`px-4 py-2 rounded-lg transition-colors ${
            showZ2 ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-700'
          }`}
        >
          Z2 Prediction
        </button>
        <button
          onClick={() => setShowZ2(false)}
          className={`px-4 py-2 rounded-lg transition-colors ${
            !showZ2 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
          }`}
        >
          Observed (Planck)
        </button>
      </div>

      <div className="flex items-center justify-center">
        <svg viewBox="0 0 200 200" className="w-64 h-64">
          {/* Dark energy slice */}
          <path d={lambdaPath()} fill="#8B5CF6" stroke="white" strokeWidth="2" />

          {/* Matter slice */}
          <path d={matterPath()} fill="#3B82F6" stroke="white" strokeWidth="2" />

          {/* Center label */}
          <text x="100" y="95" textAnchor="middle" fontSize="10" fill="#374151" fontWeight="bold">
            {values.label}
          </text>
          <text x="100" y="110" textAnchor="middle" fontSize="8" fill="#6B7280">
            Universe composition
          </text>
        </svg>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-purple-50 p-4 rounded border border-purple-200 text-center">
          <div className="text-sm text-gray-500">Dark Energy</div>
          <div className="text-3xl font-bold text-purple-600">
            {showZ2 ? '13/19' : (values.lambda * 100).toFixed(1) + '%'}
          </div>
          <div className="text-sm text-purple-500">
            = {(values.lambda * 100).toFixed(2)}%
          </div>
        </div>
        <div className="bg-blue-50 p-4 rounded border border-blue-200 text-center">
          <div className="text-sm text-gray-500">Matter</div>
          <div className="text-3xl font-bold text-blue-600">
            {showZ2 ? '6/19' : (values.matter * 100).toFixed(1) + '%'}
          </div>
          <div className="text-sm text-blue-500">
            = {(values.matter * 100).toFixed(2)}%
          </div>
        </div>
      </div>

      <div className="bg-green-50 p-3 rounded border border-green-200 text-sm text-center">
        <strong>Agreement:</strong> Z2 predicts 68.42%, observed is 68.5% - a match to 0.1%!
      </div>
    </div>
  )
}

// Cosmic Expansion Timeline
function ExpansionTimelineViz() {
  const [era, setEra] = useState(2)

  const eras = [
    { name: 'Radiation', color: '#EF4444', time: '0 - 50,000 years', desc: 'Universe dominated by photons, neutrinos' },
    { name: 'Matter', color: '#3B82F6', time: '50,000 - 9.8 billion years', desc: 'Dark matter and baryons dominate' },
    { name: 'Dark Energy', color: '#8B5CF6', time: '9.8 billion - now', desc: 'Accelerating expansion takes over' },
  ]

  // Scale factor evolution
  const generateScaleFactor = () => {
    const points = []
    for (let i = 0; i <= 100; i++) {
      const t = i / 100 // normalized time
      let a
      if (t < 0.1) {
        // Radiation era: a ~ t^(1/2)
        a = Math.sqrt(t / 0.1) * 0.2
      } else if (t < 0.7) {
        // Matter era: a ~ t^(2/3)
        a = 0.2 + Math.pow((t - 0.1) / 0.6, 2/3) * 0.5
      } else {
        // Dark energy era: exponential
        a = 0.7 + (Math.exp((t - 0.7) * 2) - 1) * 0.15
      }
      points.push({ x: 30 + t * 240, y: 170 - a * 150 })
    }
    return points
  }

  const scaleFactorPoints = generateScaleFactor()

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-2 flex-wrap">
        {eras.map((e, i) => (
          <button
            key={i}
            onClick={() => setEra(i)}
            className={`px-3 py-1 rounded-full text-sm transition-colors ${
              era === i ? 'text-white' : 'bg-gray-200 text-gray-700'
            }`}
            style={{ backgroundColor: era === i ? e.color : undefined }}
          >
            {e.name}
          </button>
        ))}
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gray-900 rounded-lg">
        {/* Axes */}
        <line x1="30" y1="170" x2="280" y2="170" stroke="#6B7280" strokeWidth="1" />
        <line x1="30" y1="170" x2="30" y2="20" stroke="#6B7280" strokeWidth="1" />
        <text x="155" y="190" textAnchor="middle" fontSize="10" fill="#9CA3AF">Time (billions of years)</text>
        <text x="15" y="100" textAnchor="middle" fontSize="10" fill="#9CA3AF" transform="rotate(-90 15,100)">Scale factor a(t)</text>

        {/* Era backgrounds */}
        <rect x="30" y="20" width="24" height="150" fill="#EF4444" opacity={era === 0 ? 0.3 : 0.1} />
        <rect x="54" y="20" width="144" height="150" fill="#3B82F6" opacity={era === 1 ? 0.3 : 0.1} />
        <rect x="198" y="20" width="72" height="150" fill="#8B5CF6" opacity={era === 2 ? 0.3 : 0.1} />

        {/* Scale factor curve */}
        <path
          d={scaleFactorPoints.map((p, i) => (i === 0 ? `M ${p.x},${p.y}` : `L ${p.x},${p.y}`)).join(' ')}
          fill="none"
          stroke="#4ADE80"
          strokeWidth="2"
        />

        {/* Era labels */}
        <text x="42" y="35" fontSize="8" fill="#EF4444">Rad</text>
        <text x="126" y="35" fontSize="8" fill="#3B82F6">Matter</text>
        <text x="234" y="35" fontSize="8" fill="#8B5CF6">DE</text>

        {/* Now marker */}
        <line x1="270" y1="170" x2="270" y2="25" stroke="#F59E0B" strokeWidth="1" strokeDasharray="4,2" />
        <text x="270" y="18" textAnchor="middle" fontSize="8" fill="#F59E0B">Now</text>
      </svg>

      <div className="bg-gray-50 p-4 rounded border border-gray-200">
        <div className="font-medium" style={{ color: eras[era].color }}>{eras[era].name} Era</div>
        <div className="text-sm text-gray-600">{eras[era].time}</div>
        <div className="text-sm text-gray-700 mt-1">{eras[era].desc}</div>
      </div>
    </div>
  )
}

// Friedmann Equation Visualization
function FriedmannViz() {
  const [omegaM, setOmegaM] = useState(0.316)
  const [omegaLambda, setOmegaLambda] = useState(0.684)

  const omegaK = 1 - omegaM - omegaLambda

  const geometry = omegaK > 0.01 ? 'Open' : omegaK < -0.01 ? 'Closed' : 'Flat'
  const geometryColor = omegaK > 0.01 ? '#EF4444' : omegaK < -0.01 ? '#3B82F6' : '#10B981'

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Omega_M = {omegaM.toFixed(3)}
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={omegaM}
            onChange={(e) => setOmegaM(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Omega_Lambda = {omegaLambda.toFixed(3)}
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={omegaLambda}
            onChange={(e) => setOmegaLambda(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 text-center">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="text-sm text-gray-500">Matter</div>
          <div className="text-xl font-bold text-blue-600">{(omegaM * 100).toFixed(1)}%</div>
        </div>
        <div className="bg-purple-50 p-3 rounded border border-purple-200">
          <div className="text-sm text-gray-500">Dark Energy</div>
          <div className="text-xl font-bold text-purple-600">{(omegaLambda * 100).toFixed(1)}%</div>
        </div>
        <div className="p-3 rounded border" style={{ backgroundColor: geometryColor + '20', borderColor: geometryColor }}>
          <div className="text-sm text-gray-500">Curvature</div>
          <div className="text-xl font-bold" style={{ color: geometryColor }}>{geometry}</div>
          <div className="text-xs text-gray-500">Omega_k = {omegaK.toFixed(3)}</div>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={() => { setOmegaM(6/19); setOmegaLambda(13/19); }}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          Set to Z2 values (6/19, 13/19)
        </button>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Flatness puzzle:</strong> Why is Omega_k so close to 0? The Z2 framework
        naturally produces a flat universe with exactly Omega_M + Omega_Lambda = 1.
      </div>
    </div>
  )
}

export default function CosmologyPage() {
  return (
    <DocumentLayout
      title="Cosmology"
      description="The expanding universe and the Z2 prediction for dark energy"
      phase="physics"
      currentIndex={7}
      prevLink={{ href: '/office-hours/physics/06-adm-formalism', title: 'ADM Formalism' }}
      nextLink={{ href: '/office-hours/physics/08-string-theory', title: 'String Theory' }}
    >
      <Section title="1. The Expanding Universe">
        <p className="text-gray-700 mb-4">
          The universe is expanding. Galaxies are moving apart, and spacetime itself is stretching.
          This expansion is described by the <strong>scale factor</strong> a(t).
        </p>

        <Formula label="Hubble's Law">
          v = H_0 * d
        </Formula>

        <div className="grid grid-cols-2 gap-4 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <strong>H_0:</strong> Hubble constant
            <div className="text-sm text-gray-600">~70 km/s/Mpc</div>
          </div>
          <div className="bg-blue-50 p-3 rounded border border-blue-200">
            <strong>Scale factor a(t):</strong>
            <div className="text-sm text-gray-600">Measures the "size" of the universe</div>
          </div>
        </div>

        <InteractiveBox title="Cosmic Expansion Timeline">
          <ExpansionTimelineViz />
        </InteractiveBox>
      </Section>

      <Section title="2. The Friedmann Equations">
        <p className="text-gray-700 mb-4">
          Einstein's equations applied to a homogeneous, isotropic universe give the
          <strong> Friedmann equations</strong> governing cosmic expansion:
        </p>

        <Formula label="First Friedmann equation">
          H^2 = (8 pi G / 3) * rho - k/a^2 + Lambda/3
        </Formula>

        <Formula label="Second Friedmann equation">
          a_ddot/a = -(4 pi G / 3)(rho + 3p) + Lambda/3
        </Formula>

        <SubSection title="Density Parameters">
          <p className="text-gray-700 mb-4">
            We define dimensionless density parameters relative to the critical density:
          </p>

          <Formula>
            Omega_M = rho_M / rho_crit, Omega_Lambda = Lambda / (3H^2), Omega_k = -k/(aH)^2
          </Formula>

          <div className="bg-green-50 p-3 rounded border border-green-200 text-sm my-4">
            <strong>Constraint:</strong> Omega_M + Omega_Lambda + Omega_k = 1 (exactly!)
          </div>
        </SubSection>

        <InteractiveBox title="Cosmic Density Parameters">
          <FriedmannViz />
        </InteractiveBox>
      </Section>

      <Section title="3. The Z2 Prediction">
        <p className="text-gray-700 mb-4">
          The Z2 framework makes a precise prediction for the cosmic composition:
        </p>

        <InteractiveBox title="Cosmic Composition: Z2 vs Observation">
          <CosmicPieChartViz />
        </InteractiveBox>

        <KeyPoint>
          <strong>The Z2 framework predicts Omega_Lambda = 13/19 and Omega_M = 6/19.</strong>
          <br />
          These exact fractions emerge from counting degrees of freedom in the T^3/Z_2 compactification!
        </KeyPoint>

        <SubSection title="Why 13/19 and 6/19?">
          <div className="space-y-3 text-gray-700">
            <p>The numbers 13 and 19 arise from the topology of the T^3/Z_2 orbifold:</p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li><strong>19</strong> = Total degrees of freedom from D-branes</li>
              <li><strong>13</strong> = Degrees of freedom contributing to vacuum energy</li>
              <li><strong>6</strong> = Degrees of freedom giving matter</li>
            </ul>
          </div>

          <div className="bg-purple-50 p-4 rounded border border-purple-200 mt-4">
            <div className="font-mono text-center text-lg">
              13 + 6 = 19 (total DOF)
            </div>
            <div className="text-center text-sm text-gray-600 mt-2">
              Hence Omega_Lambda + Omega_M = 13/19 + 6/19 = 1 (flat universe)
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="4. Cosmic History">
        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2">Era</th>
                <th className="border border-gray-200 p-2">Dominant Component</th>
                <th className="border border-gray-200 p-2">Scale Factor</th>
                <th className="border border-gray-200 p-2">a(t) Behavior</th>
              </tr>
            </thead>
            <tbody>
              <tr className="bg-red-50">
                <td className="border border-gray-200 p-2">Radiation</td>
                <td className="border border-gray-200 p-2">Photons, neutrinos</td>
                <td className="border border-gray-200 p-2">rho ~ a^-4</td>
                <td className="border border-gray-200 p-2 font-mono">a ~ t^(1/2)</td>
              </tr>
              <tr className="bg-blue-50">
                <td className="border border-gray-200 p-2">Matter</td>
                <td className="border border-gray-200 p-2">Dark matter, baryons</td>
                <td className="border border-gray-200 p-2">rho ~ a^-3</td>
                <td className="border border-gray-200 p-2 font-mono">a ~ t^(2/3)</td>
              </tr>
              <tr className="bg-purple-50">
                <td className="border border-gray-200 p-2">Dark Energy</td>
                <td className="border border-gray-200 p-2">Cosmological constant</td>
                <td className="border border-gray-200 p-2">rho = const</td>
                <td className="border border-gray-200 p-2 font-mono">a ~ e^(Ht)</td>
              </tr>
            </tbody>
          </table>
        </div>

        <KeyPoint>
          We entered the dark energy era about 4-5 billion years ago. The universe will
          expand exponentially forever (de Sitter space).
        </KeyPoint>
      </Section>

      <Section title="5. Observational Evidence">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
          <div className="bg-gray-50 p-4 rounded">
            <h4 className="font-semibold text-gray-800 mb-2">Type Ia Supernovae</h4>
            <p className="text-sm text-gray-600">
              Standard candles showing distant supernovae are fainter than expected,
              revealing accelerating expansion (1998 discovery, Nobel Prize 2011).
            </p>
          </div>
          <div className="bg-blue-50 p-4 rounded border border-blue-200">
            <h4 className="font-semibold text-blue-800 mb-2">CMB Measurements</h4>
            <p className="text-sm text-gray-600">
              Planck satellite measures Omega_Lambda = 0.685 +/- 0.007,
              remarkably close to the Z2 prediction of 13/19 = 0.6842.
            </p>
          </div>
          <div className="bg-green-50 p-4 rounded border border-green-200">
            <h4 className="font-semibold text-green-800 mb-2">BAO (Baryon Acoustic Oscillations)</h4>
            <p className="text-sm text-gray-600">
              Sound waves frozen in the early universe provide a standard ruler,
              confirming dark energy domination.
            </p>
          </div>
          <div className="bg-amber-50 p-4 rounded border border-amber-200">
            <h4 className="font-semibold text-amber-800 mb-2">Large Scale Structure</h4>
            <p className="text-sm text-gray-600">
              Galaxy clustering patterns consistent with Lambda-CDM model
              with Omega_Lambda ~ 0.7.
            </p>
          </div>
        </div>
      </Section>

      <Section title="6. Connection to Z2 Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="Omega_Lambda = 13/19 = 0.6842..."
            description="Dark energy fraction predicted from D-brane vacuum energy on T^3/Z_2"
          />
          <Z2Connection
            formula="Omega_M = 6/19 = 0.3158..."
            description="Matter fraction from D-brane matter content"
          />
          <Z2Connection
            formula="Omega_k = 0"
            description="Flat universe emerges naturally from the framework"
          />
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Cosmology Validates Z2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>- <strong>13/19:</strong> Matches observed dark energy to 0.1%</li>
            <li>- <strong>Flatness:</strong> No fine-tuning needed</li>
            <li>- <strong>Coincidence problem:</strong> Why now? Z2 provides a structural answer</li>
            <li>- <strong>Predictive:</strong> Not a fit, but a calculation from first principles</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Calculate 13/19 and 6/19 as decimals. Compare to Planck 2018 values.</li>
          <li>If H_0 = 70 km/s/Mpc, what is the Hubble time t_H = 1/H_0 in years?</li>
          <li>Show that Omega_M + Omega_Lambda = 1 implies a flat universe (k = 0).</li>
          <li>When did the dark energy era begin? (Hint: when did rho_Lambda = rho_M?)</li>
          <li>Why does rho_matter ~ a^-3 but rho_radiation ~ a^-4?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
