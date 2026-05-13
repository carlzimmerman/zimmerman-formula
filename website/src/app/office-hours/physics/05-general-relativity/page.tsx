'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Curved Spacetime Visualization
function CurvedSpacetimeViz() {
  const [mass, setMass] = useState(3)

  // Generate grid points with curvature based on mass
  const gridSize = 11
  const points: { x: number; y: number; z: number }[][] = []

  for (let i = 0; i < gridSize; i++) {
    const row: { x: number; y: number; z: number }[] = []
    for (let j = 0; j < gridSize; j++) {
      const x = (i - gridSize / 2) * 20
      const y = (j - gridSize / 2) * 20
      const r = Math.sqrt(x * x + y * y)
      const z = -mass * 15 / (r + 20) // Depression from mass
      row.push({ x, y, z })
    }
    points.push(row)
  }

  // Project 3D to 2D with simple isometric view
  const project = (x: number, y: number, z: number) => ({
    px: 150 + x * 0.8 + y * 0.4,
    py: 100 - z * 1.5 + y * 0.3
  })

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Mass: {mass} solar masses
        </label>
        <input
          type="range"
          min="0"
          max="10"
          step="0.5"
          value={mass}
          onChange={(e) => setMass(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gradient-to-b from-gray-900 to-gray-800 rounded-lg">
        {/* Grid lines in Y direction */}
        {points.map((row, i) => {
          const pathData = row.map((p, j) => {
            const { px, py } = project(p.x, p.y, p.z)
            return j === 0 ? `M ${px} ${py}` : `L ${px} ${py}`
          }).join(' ')
          return <path key={`y-${i}`} d={pathData} fill="none" stroke="#4ADE80" strokeWidth="0.5" opacity="0.6" />
        })}

        {/* Grid lines in X direction */}
        {Array.from({ length: gridSize }, (_, j) => {
          const pathData = points.map((row, i) => {
            const p = row[j]
            const { px, py } = project(p.x, p.y, p.z)
            return i === 0 ? `M ${px} ${py}` : `L ${px} ${py}`
          }).join(' ')
          return <path key={`x-${j}`} d={pathData} fill="none" stroke="#4ADE80" strokeWidth="0.5" opacity="0.6" />
        })}

        {/* Central mass */}
        {mass > 0 && (
          <circle
            cx={150}
            cy={100 + mass * 2}
            r={4 + mass}
            fill="#FBBF24"
            className="drop-shadow-lg"
          />
        )}

        {/* Label */}
        <text x="150" y="185" fontSize="10" textAnchor="middle" fill="#9CA3AF">
          Spacetime curvature from mass
        </text>
      </svg>

      <div className="bg-green-50 p-3 rounded border border-green-200 text-sm">
        <strong>Einstein's insight:</strong> Mass tells spacetime how to curve.
        Objects follow the straightest possible paths (geodesics) in curved spacetime.
      </div>
    </div>
  )
}

// Geodesic Visualization
function GeodesicViz() {
  const [angle, setAngle] = useState(45)
  const [time, setTime] = useState(0)
  const [isRunning, setIsRunning] = useState(false)

  // Light ray path (affected by curvature near center)
  const generatePath = () => {
    const points = []
    const angleRad = (angle * Math.PI) / 180

    for (let t = 0; t <= time; t += 0.5) {
      // Simple model: straight line with bending near center
      let x = -100 + t * 3 * Math.cos(angleRad)
      let y = -50 + t * 3 * Math.sin(angleRad)

      // Add curvature effect near center
      const r = Math.sqrt(x * x + y * y)
      if (r < 80 && r > 10) {
        const bendFactor = 0.3 * (80 - r) / 80
        const theta = Math.atan2(y, x)
        y += bendFactor * 30 * Math.cos(theta)
      }

      points.push({ x: 150 + x, y: 100 + y })
    }
    return points
  }

  const pathPoints = generatePath()

  // Animation effect
  useState(() => {
    if (isRunning && time < 100) {
      const interval = setInterval(() => {
        setTime(t => Math.min(t + 1, 100))
      }, 50)
      return () => clearInterval(interval)
    }
  })

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Initial angle: {angle}deg
          </label>
          <input
            type="range"
            min="20"
            max="70"
            value={angle}
            onChange={(e) => { setAngle(Number(e.target.value)); setTime(0) }}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Time: {time.toFixed(0)}
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={time}
            onChange={(e) => setTime(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gray-900 rounded-lg">
        {/* Concentric circles representing curvature */}
        {[20, 40, 60, 80].map(r => (
          <circle key={r} cx="150" cy="100" r={r} fill="none" stroke="#374151" strokeWidth="0.5" />
        ))}

        {/* Central mass */}
        <circle cx="150" cy="100" r="15" fill="#FBBF24" className="drop-shadow-lg" />
        <text x="150" y="104" fontSize="8" textAnchor="middle" fill="#78350F">M</text>

        {/* Light ray path */}
        {pathPoints.length > 1 && (
          <path
            d={pathPoints.map((p, i) => (i === 0 ? `M ${p.x} ${p.y}` : `L ${p.x} ${p.y}`)).join(' ')}
            fill="none"
            stroke="#3B82F6"
            strokeWidth="2"
          />
        )}

        {/* Current position */}
        {pathPoints.length > 0 && (
          <circle
            cx={pathPoints[pathPoints.length - 1]?.x || 0}
            cy={pathPoints[pathPoints.length - 1]?.y || 0}
            r="4"
            fill="#60A5FA"
          />
        )}

        {/* Labels */}
        <text x="150" y="190" fontSize="10" textAnchor="middle" fill="#9CA3AF">
          Light bends near massive objects
        </text>
      </svg>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <strong>Geodesic:</strong> The shortest path through curved spacetime.
          Light always follows null geodesics (ds2 = 0).
        </div>
        <div className="bg-amber-50 p-3 rounded border border-amber-200">
          <strong>Gravitational lensing:</strong> Light from distant stars bends around the Sun,
          confirmed in the 1919 eclipse.
        </div>
      </div>
    </div>
  )
}

// GPS Time Dilation Example
function GPSTimeDilationViz() {
  const [altitude, setAltitude] = useState(20200) // GPS satellite altitude in km
  const [showEffect, setShowEffect] = useState(true)

  // Calculate time dilation effects
  const c = 299792.458 // km/s
  const G = 6.674e-11 // gravitational constant
  const M_earth = 5.972e24 // kg
  const R_earth = 6371 // km

  // Simplified calculations (order of magnitude)
  // Gravitational time dilation: clocks run faster at altitude
  const gravitationalEffect = (altitude / R_earth) * 45.7 // microseconds per day (faster)

  // Special relativistic time dilation: moving clocks run slower
  const orbitalVelocity = Math.sqrt((G * M_earth) / ((R_earth + altitude) * 1000)) / 1000 // km/s
  const velocityEffect = -7.2 * (orbitalVelocity / 3.87) // microseconds per day (slower)

  const netEffect = gravitationalEffect + velocityEffect

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Satellite altitude: {altitude.toLocaleString()} km
        </label>
        <input
          type="range"
          min="200"
          max="35786"
          step="100"
          value={altitude}
          onChange={(e) => setAltitude(Number(e.target.value))}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-500">
          <span>Low Earth Orbit</span>
          <span>GPS (~20,200 km)</span>
          <span>Geostationary</span>
        </div>
      </div>

      <div className="flex items-center justify-center">
        <svg viewBox="0 0 300 200" className="w-full max-w-md">
          {/* Earth */}
          <circle cx="150" cy="180" r="60" fill="#3B82F6" />
          <ellipse cx="150" cy="180" rx="60" ry="20" fill="#2563EB" opacity="0.5" />

          {/* Orbit */}
          <ellipse
            cx="150"
            cy="180"
            rx={60 + altitude / 200}
            ry={20 + altitude / 600}
            fill="none"
            stroke="#9CA3AF"
            strokeWidth="1"
            strokeDasharray="4 2"
          />

          {/* Satellite */}
          <g transform={`translate(${150 + 60 + altitude / 200}, ${180 - 20 - altitude / 600})`}>
            <rect x="-8" y="-4" width="16" height="8" fill="#F59E0B" />
            <rect x="-20" y="-2" width="10" height="4" fill="#6366F1" />
            <rect x="10" y="-2" width="10" height="4" fill="#6366F1" />
          </g>

          {/* Ground station */}
          <rect x="145" y="170" width="10" height="10" fill="#10B981" />

          {/* Time comparison */}
          <text x="50" y="30" fontSize="10" fill="#374151">Satellite Clock</text>
          <text x="50" y="45" fontSize="12" fontFamily="monospace" fill={gravitationalEffect > 0 ? '#059669' : '#DC2626'}>
            {showEffect ? `+${gravitationalEffect.toFixed(1)} us/day (gravity)` : '00:00:00.000000'}
          </text>
          <text x="50" y="60" fontSize="12" fontFamily="monospace" fill={velocityEffect > 0 ? '#059669' : '#DC2626'}>
            {showEffect ? `${velocityEffect.toFixed(1)} us/day (velocity)` : '00:00:00.000000'}
          </text>

          <text x="200" y="30" fontSize="10" fill="#374151">Net Effect</text>
          <text x="200" y="50" fontSize="14" fontFamily="monospace" fontWeight="bold" fill="#7C3AED">
            +{netEffect.toFixed(1)} us/day
          </text>
        </svg>
      </div>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={showEffect}
          onChange={(e) => setShowEffect(e.target.checked)}
          className="rounded"
        />
        <label className="text-sm text-gray-600">Show relativistic corrections</label>
      </div>

      <div className="grid grid-cols-1 gap-3 text-sm">
        <div className="bg-purple-50 p-3 rounded border border-purple-200">
          <strong>Without corrections:</strong> GPS would accumulate ~10 km/day of error!
          <br />
          General relativity is not just theory - it is essential technology.
        </div>
      </div>
    </div>
  )
}

export default function GeneralRelativityPage() {
  return (
    <DocumentLayout
      title="General Relativity"
      description="Curved spacetime, Einstein's equations, and gravity as geometry"
      phase="physics"
      currentIndex={5}
      prevLink={{ href: '/office-hours/physics/04-gauge-theory', title: 'Gauge Theory' }}
      nextLink={{ href: '/office-hours/physics/06-adm-formalism', title: 'ADM Formalism' }}
    >
      <Section title="1. The Equivalence Principle">
        <p className="text-gray-700 mb-4">
          Einstein's key insight: <strong>gravity is indistinguishable from acceleration</strong>.
          In a falling elevator, you feel weightless. In an accelerating rocket, you feel weight.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
          <div className="bg-blue-50 p-3 rounded border border-blue-200">
            <strong>Weak Equivalence Principle:</strong>
            <div className="text-sm text-gray-600 mt-1">
              All objects fall at the same rate, regardless of mass or composition.
            </div>
          </div>
          <div className="bg-green-50 p-3 rounded border border-green-200">
            <strong>Strong Equivalence Principle:</strong>
            <div className="text-sm text-gray-600 mt-1">
              Physics in a freely falling frame is locally the same as in flat spacetime.
            </div>
          </div>
        </div>

        <KeyPoint>
          The equivalence principle implies that <strong>gravity curves spacetime</strong>.
          Free-falling objects follow straight lines (geodesics) in curved spacetime.
        </KeyPoint>
      </Section>

      <Section title="2. Curved Spacetime">
        <p className="text-gray-700 mb-4">
          Mass and energy curve the fabric of spacetime. Objects then follow the natural paths
          (geodesics) through this curved geometry.
        </p>

        <InteractiveBox title="Spacetime Curvature from Mass">
          <CurvedSpacetimeViz />
        </InteractiveBox>

        <SubSection title="The Metric Tensor">
          <p className="text-gray-700 mb-4">
            Spacetime geometry is encoded in the <strong>metric tensor</strong> g_uv,
            which defines distances and angles:
          </p>

          <Formula label="Spacetime interval">
            ds2 = g_uv dx^u dx^v
          </Formula>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
            <div className="bg-gray-50 p-3 rounded">
              <strong>Flat spacetime (Minkowski):</strong>
              <div className="font-mono text-sm mt-1">ds2 = -c2dt2 + dx2 + dy2 + dz2</div>
            </div>
            <div className="bg-purple-50 p-3 rounded border border-purple-200">
              <strong>Schwarzschild (black hole):</strong>
              <div className="font-mono text-sm mt-1">ds2 = -(1-r_s/r)c2dt2 + dr2/(1-r_s/r) + ...</div>
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="3. Geodesics">
        <p className="text-gray-700 mb-4">
          A <strong>geodesic</strong> is the straightest possible path through curved spacetime.
          Massive objects follow timelike geodesics; light follows null geodesics.
        </p>

        <InteractiveBox title="Light Bending Around Mass">
          <GeodesicViz />
        </InteractiveBox>

        <Formula label="Geodesic equation">
          d2x^u/dt2 + G^u_ab (dx^a/dt)(dx^b/dt) = 0
        </Formula>

        <p className="text-gray-700 my-4">
          The <strong>Christoffel symbols</strong> G^u_ab encode how coordinates curve,
          derived from the metric: G^u_ab = (1/2)g^um(g_ma,b + g_mb,a - g_ab,m)
        </p>
      </Section>

      <Section title="4. Einstein Field Equations">
        <p className="text-gray-700 mb-4">
          Einstein's equations relate spacetime curvature to matter and energy content:
        </p>

        <Formula label="Einstein field equations">
          G_uv + Lambda g_uv = (8 pi G / c4) T_uv
        </Formula>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 my-4">
          <div className="bg-blue-50 p-3 rounded border border-blue-200">
            <strong>G_uv</strong>
            <div className="text-sm text-gray-600">Einstein tensor (curvature)</div>
          </div>
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <strong>Lambda</strong>
            <div className="text-sm text-gray-600">Cosmological constant</div>
          </div>
          <div className="bg-green-50 p-3 rounded border border-green-200">
            <strong>T_uv</strong>
            <div className="text-sm text-gray-600">Stress-energy tensor (matter)</div>
          </div>
        </div>

        <SubSection title="The Einstein Tensor">
          <Formula>
            G_uv = R_uv - (1/2)R g_uv
          </Formula>
          <p className="text-gray-700 mt-2">
            Where R_uv is the Ricci tensor (contraction of Riemann curvature) and R is the Ricci scalar.
          </p>
        </SubSection>
      </Section>

      <Section title="5. Real-World Application: GPS">
        <p className="text-gray-700 mb-4">
          General relativity is not just abstract theory - GPS satellites must account for
          relativistic time dilation to maintain accuracy.
        </p>

        <InteractiveBox title="GPS Time Dilation">
          <GPSTimeDilationViz />
        </InteractiveBox>

        <KeyPoint>
          GPS satellites experience two competing effects:
          <br />
          1. <strong>Gravitational time dilation:</strong> Clocks run faster at higher altitude (+45 us/day)
          <br />
          2. <strong>Velocity time dilation:</strong> Moving clocks run slower (-7 us/day)
          <br />
          Net effect: satellite clocks gain ~38 microseconds per day.
        </KeyPoint>
      </Section>

      <Section title="6. Key Solutions">
        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2">Solution</th>
                <th className="border border-gray-200 p-2">Describes</th>
                <th className="border border-gray-200 p-2">Key Feature</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2 font-mono">Schwarzschild</td>
                <td className="border border-gray-200 p-2">Non-rotating black hole</td>
                <td className="border border-gray-200 p-2">Event horizon at r_s = 2GM/c2</td>
              </tr>
              <tr className="bg-blue-50">
                <td className="border border-gray-200 p-2 font-mono">Kerr</td>
                <td className="border border-gray-200 p-2">Rotating black hole</td>
                <td className="border border-gray-200 p-2">Frame dragging, ergosphere</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2 font-mono">FLRW</td>
                <td className="border border-gray-200 p-2">Expanding universe</td>
                <td className="border border-gray-200 p-2">Scale factor a(t), Hubble flow</td>
              </tr>
              <tr className="bg-green-50">
                <td className="border border-gray-200 p-2 font-mono">de Sitter</td>
                <td className="border border-gray-200 p-2">Pure dark energy</td>
                <td className="border border-gray-200 p-2">Exponential expansion</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="7. Connection to Z2 Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="G_uv + Lambda g_uv = 8piG T_uv"
            description="Einstein equations must be satisfied by any physical spacetime, including the Z2 compactification"
          />
          <Z2Connection
            formula="Lambda = 13/19 * rho_crit"
            description="The cosmological constant fraction emerges from moduli stabilization on T3/Z2"
          />
          <Z2Connection
            formula="AdS_5 x S5 / Z2"
            description="The near-horizon geometry of D3-branes includes a Z2 orbifold"
          />
        </div>

        <div className="bg-gradient-to-r from-green-50 to-purple-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why General Relativity Matters for Z2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>* <strong>Compactification</strong> requires solving Einstein equations on compact spaces</li>
            <li>* <strong>Moduli stabilization</strong> fixes the size of extra dimensions</li>
            <li>* <strong>ADM formalism</strong> separates time from space for canonical quantization</li>
            <li>* <strong>Cosmological constant</strong> arises from vacuum energy of compactified dimensions</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Calculate the Schwarzschild radius for the Sun (M = 2 x 10^30 kg). Is the Sun a black hole?</li>
          <li>At what altitude does gravitational time dilation equal velocity time dilation?</li>
          <li>Show that the Einstein tensor is divergence-free: nabla_u G^uv = 0.</li>
          <li>Derive the Newtonian limit: show g_00 approx -(1 + 2Phi/c2) where Phi is gravitational potential.</li>
          <li>Why does the cosmological constant have units of (length)^-2?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
