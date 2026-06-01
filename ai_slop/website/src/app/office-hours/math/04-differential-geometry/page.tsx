'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Metric Tensor Visualization
function MetricViz() {
  const [g11, setG11] = useState(1)
  const [g22, setG22] = useState(1)
  const [g12, setG12] = useState(0)

  // Generate grid points
  const gridSize = 5
  const points: { x: number; y: number; tx: number; ty: number }[] = []

  for (let i = -gridSize; i <= gridSize; i++) {
    for (let j = -gridSize; j <= gridSize; j++) {
      const x = i * 0.4
      const y = j * 0.4
      // Apply metric transformation
      const tx = Math.sqrt(g11) * x + g12 * y / 2
      const ty = Math.sqrt(g22) * y + g12 * x / 2
      points.push({ x, y, tx, ty })
    }
  }

  const det = g11 * g22 - g12 * g12

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">g₁₁ = {g11.toFixed(1)}</label>
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={g11}
            onChange={(e) => setG11(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">g₂₂ = {g22.toFixed(1)}</label>
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={g22}
            onChange={(e) => setG22(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">g₁₂ = {g12.toFixed(1)}</label>
          <input
            type="range"
            min="-0.5"
            max="0.5"
            step="0.1"
            value={g12}
            onChange={(e) => setG12(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <div className="flex items-center justify-center gap-8">
        <div>
          <div className="text-sm text-gray-500 text-center mb-1">Flat Space</div>
          <svg viewBox="-3 -3 6 6" className="w-40 h-40 bg-white border border-gray-200 rounded">
            {/* Grid lines */}
            {[-2, -1, 0, 1, 2].map((i) => (
              <g key={i}>
                <line x1={i} y1="-2.5" x2={i} y2="2.5" stroke="#E5E7EB" strokeWidth="0.05" />
                <line x1="-2.5" y1={i} x2="2.5" y2={i} stroke="#E5E7EB" strokeWidth="0.05" />
              </g>
            ))}
            {/* Points */}
            {points.slice(0, 50).map((p, i) => (
              <circle key={i} cx={p.x} cy={-p.y} r="0.08" fill="#3B82F6" opacity="0.6" />
            ))}
          </svg>
        </div>

        <div className="text-2xl text-gray-400">→</div>

        <div>
          <div className="text-sm text-gray-500 text-center mb-1">With Metric gᵢⱼ</div>
          <svg viewBox="-3 -3 6 6" className="w-40 h-40 bg-white border border-gray-200 rounded">
            {/* Transformed points */}
            {points.slice(0, 50).map((p, i) => (
              <circle key={i} cx={p.tx} cy={-p.ty} r="0.08" fill="#8B5CF6" opacity="0.6" />
            ))}
          </svg>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 text-center">
        <div className="bg-gray-50 p-3 rounded">
          <div className="text-sm text-gray-500">Metric Tensor</div>
          <div className="font-mono text-sm grid grid-cols-2 gap-1 w-24 mx-auto mt-1">
            <div className="bg-white p-1 rounded border">{g11.toFixed(1)}</div>
            <div className="bg-white p-1 rounded border">{g12.toFixed(1)}</div>
            <div className="bg-white p-1 rounded border">{g12.toFixed(1)}</div>
            <div className="bg-white p-1 rounded border">{g22.toFixed(1)}</div>
          </div>
        </div>
        <div className={`p-3 rounded ${det > 0 ? 'bg-green-50' : 'bg-red-50'}`}>
          <div className="text-sm text-gray-500">Determinant</div>
          <div className={`text-xl font-bold ${det > 0 ? 'text-green-600' : 'text-red-600'}`}>
            det(g) = {det.toFixed(2)}
          </div>
          <div className="text-xs text-gray-500">
            {det > 0 ? 'Valid metric' : 'Invalid (need det > 0)'}
          </div>
        </div>
      </div>
    </div>
  )
}

// Curvature Visualization
function CurvatureViz() {
  const [curvature, setCurvature] = useState(0)

  const curveType = curvature > 0 ? 'positive' : curvature < 0 ? 'negative' : 'zero'

  // Generate surface points
  const generateSurface = () => {
    const points = []
    for (let i = -10; i <= 10; i++) {
      const x = i * 10
      const y = curvature * (i * i) * 0.5
      points.push({ x: 50 + x, y: 80 - y })
    }
    return points
  }

  const surfacePoints = generateSurface()
  const pathD = `M ${surfacePoints.map(p => `${p.x},${p.y}`).join(' L ')}`

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Curvature K = {curvature.toFixed(1)}
        </label>
        <input
          type="range"
          min="-2"
          max="2"
          step="0.1"
          value={curvature}
          onChange={(e) => setCurvature(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="0 0 200 120" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Surface */}
        <path
          d={pathD}
          fill="none"
          stroke={curvature > 0 ? '#3B82F6' : curvature < 0 ? '#EF4444' : '#10B981'}
          strokeWidth="3"
        />

        {/* Parallel transport visualization */}
        {curvature !== 0 && (
          <>
            <path
              d="M 50 80 L 50 60"
              stroke="#8B5CF6"
              strokeWidth="2"
              markerEnd="url(#arrowhead)"
            />
            <path
              d={`M 150 ${80 - curvature * 50} L ${150 + curvature * 10} ${60 - curvature * 50}`}
              stroke="#8B5CF6"
              strokeWidth="2"
              markerEnd="url(#arrowhead)"
            />
          </>
        )}

        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#8B5CF6" />
          </marker>
        </defs>

        {/* Labels */}
        <text x="100" y="110" textAnchor="middle" fontSize="12" fill="#6B7280">
          {curveType === 'positive' ? 'Sphere-like (K > 0)' :
           curveType === 'negative' ? 'Saddle-like (K < 0)' : 'Flat (K = 0)'}
        </text>
      </svg>

      <div className="grid grid-cols-3 gap-3 text-center text-sm">
        <div className={`p-3 rounded border ${curvature > 0 ? 'bg-blue-100 border-blue-300' : 'bg-gray-50 border-gray-200'}`}>
          <div className="font-medium">K {'>'} 0</div>
          <div className="text-xs text-gray-600">Sphere, closed geodesics</div>
        </div>
        <div className={`p-3 rounded border ${curvature === 0 ? 'bg-green-100 border-green-300' : 'bg-gray-50 border-gray-200'}`}>
          <div className="font-medium">K = 0</div>
          <div className="text-xs text-gray-600">Flat, parallel lines stay parallel</div>
        </div>
        <div className={`p-3 rounded border ${curvature < 0 ? 'bg-red-100 border-red-300' : 'bg-gray-50 border-gray-200'}`}>
          <div className="font-medium">K {'<'} 0</div>
          <div className="text-xs text-gray-600">Saddle, geodesics diverge</div>
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Parallel transport:</strong> Moving a vector along a curved surface rotates it.
        The rotation angle after a closed loop measures the curvature!
      </div>
    </div>
  )
}

// Fiber Bundle Visualization
function FiberBundleViz() {
  const [basePoint, setBasePoint] = useState(0.5)
  const [fiberAngle, setFiberAngle] = useState(45)

  const baseX = basePoint * 200
  const fiberRad = (fiberAngle * Math.PI) / 180

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Base point x = {basePoint.toFixed(2)}
          </label>
          <input
            type="range"
            min="0.1"
            max="0.9"
            step="0.01"
            value={basePoint}
            onChange={(e) => setBasePoint(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Fiber value (angle) = {fiberAngle}°
          </label>
          <input
            type="range"
            min="0"
            max="360"
            value={fiberAngle}
            onChange={(e) => setFiberAngle(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <svg viewBox="0 0 250 180" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Base manifold (line) */}
        <line x1="20" y1="140" x2="230" y2="140" stroke="#6B7280" strokeWidth="3" />
        <text x="125" y="165" textAnchor="middle" fontSize="12" fill="#6B7280">Base Manifold M</text>

        {/* Fibers at different points */}
        {[0.2, 0.4, 0.6, 0.8].map((p, i) => (
          <g key={i} opacity={Math.abs(p - basePoint) < 0.1 ? 1 : 0.3}>
            <line
              x1={20 + p * 200}
              y1="140"
              x2={20 + p * 200}
              y2="30"
              stroke="#D1D5DB"
              strokeWidth="1"
              strokeDasharray="4,4"
            />
            <circle cx={20 + p * 200} cy="85" r="20" fill="none" stroke="#D1D5DB" strokeWidth="1" />
          </g>
        ))}

        {/* Active fiber */}
        <line
          x1={20 + baseX}
          y1="140"
          x2={20 + baseX}
          y2="30"
          stroke="#3B82F6"
          strokeWidth="2"
        />
        <circle
          cx={20 + baseX}
          cy="85"
          r="20"
          fill="none"
          stroke="#8B5CF6"
          strokeWidth="2"
        />

        {/* Point on fiber */}
        <circle
          cx={20 + baseX + 20 * Math.cos(fiberRad)}
          cy={85 - 20 * Math.sin(fiberRad)}
          r="5"
          fill="#8B5CF6"
        />

        {/* Base point */}
        <circle cx={20 + baseX} cy="140" r="6" fill="#3B82F6" />

        {/* Labels */}
        <text x={20 + baseX + 30} y="85" fontSize="10" fill="#8B5CF6">Fiber F (circle)</text>
        <text x={20 + baseX - 5} y="155" fontSize="10" fill="#3B82F6">x</text>
      </svg>

      <div className="grid grid-cols-3 gap-3 text-center text-sm">
        <div className="bg-gray-50 p-3 rounded">
          <div className="font-medium text-gray-700">Base M</div>
          <div className="text-xs text-gray-500">Where you are</div>
        </div>
        <div className="bg-purple-50 p-3 rounded">
          <div className="font-medium text-purple-700">Fiber F</div>
          <div className="text-xs text-purple-600">Internal degrees of freedom</div>
        </div>
        <div className="bg-blue-50 p-3 rounded">
          <div className="font-medium text-blue-700">Total E</div>
          <div className="text-xs text-blue-600">E = M × F locally</div>
        </div>
      </div>

      <div className="bg-green-50 p-3 rounded border border-green-200 text-sm">
        <strong>Gauge fields live on fiber bundles:</strong> The photon field is a connection
        on a U(1) bundle — the fiber is a circle representing the phase of the electron field.
      </div>
    </div>
  )
}

export default function DifferentialGeometryPage() {
  return (
    <DocumentLayout
      title="Differential Geometry"
      description="Metrics, curvature, geodesics, and the geometry of spacetime and gauge fields"
      phase="math"
      currentIndex={4}
      prevLink={{ href: '/office-hours/math/03-topology', title: 'Topology' }}
      nextLink={{ href: '/office-hours/math/05-algebraic-topology', title: 'Algebraic Topology' }}
    >
      <Section title="1. What is Differential Geometry?">
        <p className="text-gray-700 mb-4">
          Differential geometry studies curved spaces using calculus. It provides the mathematical
          language for Einstein's general relativity and modern gauge theories.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
          <div className="bg-gray-50 p-3 rounded">
            <strong>Topology:</strong>
            <div className="text-sm text-gray-600">What is the shape? (donut vs. sphere)</div>
          </div>
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <strong>Differential Geometry:</strong>
            <div className="text-sm text-purple-600">How curved is it? What are distances?</div>
          </div>
        </div>

        <KeyPoint>
          <strong>The metric tensor gᵢⱼ tells you how to measure distances on a curved surface.</strong>
          In general relativity, gravity IS the curvature of spacetime!
        </KeyPoint>
      </Section>

      <Section title="2. The Metric Tensor">
        <p className="text-gray-700 mb-4">
          The <strong>metric tensor</strong> gᵢⱼ defines the inner product between tangent vectors,
          allowing us to measure lengths and angles:
        </p>

        <Formula label="Line element">
          ds² = gᵢⱼ dxⁱ dxʲ
        </Formula>

        <InteractiveBox title="Metric Tensor Effects">
          <MetricViz />
        </InteractiveBox>

        <SubSection title="Examples of Metrics">
          <div className="space-y-2 text-sm">
            <div className="bg-gray-50 p-2 rounded font-mono">
              <strong>Flat space:</strong> ds² = dx² + dy² + dz²
            </div>
            <div className="bg-gray-50 p-2 rounded font-mono">
              <strong>Sphere S²:</strong> ds² = R²(dθ² + sin²θ dφ²)
            </div>
            <div className="bg-purple-50 p-2 rounded font-mono border border-purple-200">
              <strong>Torus T²:</strong> ds² = R₁²dθ² + R₂²dφ²
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="3. Curvature">
        <p className="text-gray-700 mb-4">
          <strong>Curvature</strong> measures how a space deviates from being flat.
          The Riemann curvature tensor Rᵢⱼₖₗ captures all curvature information.
        </p>

        <InteractiveBox title="Gaussian Curvature">
          <CurvatureViz />
        </InteractiveBox>

        <SubSection title="Types of Curvature">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">Curvature</th>
                  <th className="border border-gray-200 p-2">Symbol</th>
                  <th className="border border-gray-200 p-2">Measures</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2">Riemann</td>
                  <td className="border border-gray-200 p-2 font-mono">Rᵢⱼₖₗ</td>
                  <td className="border border-gray-200 p-2">Full curvature information</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Ricci</td>
                  <td className="border border-gray-200 p-2 font-mono">Rᵢⱼ = Rᵏᵢₖⱼ</td>
                  <td className="border border-gray-200 p-2">Volume distortion</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Scalar</td>
                  <td className="border border-gray-200 p-2 font-mono">R = gⁱʲRᵢⱼ</td>
                  <td className="border border-gray-200 p-2">Average curvature</td>
                </tr>
                <tr className="bg-purple-50">
                  <td className="border border-gray-200 p-2">Gaussian</td>
                  <td className="border border-gray-200 p-2 font-mono">K</td>
                  <td className="border border-gray-200 p-2">Intrinsic 2D curvature</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>

        <Z2Connection
          formula="∫_M R √g d⁴x"
          description="The Einstein-Hilbert action - gravity is geometry!"
        />
      </Section>

      <Section title="4. Geodesics">
        <p className="text-gray-700 mb-4">
          <strong>Geodesics</strong> are the straightest possible paths on a curved surface.
          They minimize (or extremize) the distance between two points.
        </p>

        <Formula label="Geodesic equation">
          d²xᵘ/dτ² + Γᵘᵥρ (dxᵛ/dτ)(dxᵖ/dτ) = 0
        </Formula>

        <div className="grid grid-cols-3 gap-3 my-4 text-center text-sm">
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-lg mb-1">___</div>
            <div className="font-medium">Flat Space</div>
            <div className="text-xs text-gray-500">Geodesic = straight line</div>
          </div>
          <div className="bg-blue-50 p-3 rounded">
            <div className="text-lg mb-1">⌒</div>
            <div className="font-medium">Sphere</div>
            <div className="text-xs text-blue-600">Geodesic = great circle</div>
          </div>
          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <div className="text-lg mb-1">~</div>
            <div className="font-medium">Torus</div>
            <div className="text-xs text-purple-600">Geodesic can wrap around!</div>
          </div>
        </div>

        <KeyPoint>
          In general relativity, <strong>free particles follow geodesics</strong>.
          Gravity isn't a force — it's the curvature of spacetime guiding particles along geodesics!
        </KeyPoint>
      </Section>

      <Section title="5. Fiber Bundles">
        <p className="text-gray-700 mb-4">
          A <strong>fiber bundle</strong> attaches extra structure (the "fiber") to each point
          of a base space. Gauge fields are connections on fiber bundles!
        </p>

        <InteractiveBox title="Fiber Bundle Structure">
          <FiberBundleViz />
        </InteractiveBox>

        <SubSection title="Bundle Components">
          <div className="space-y-2 text-gray-700">
            <p>• <strong>Base M:</strong> The physical spacetime (or internal manifold)</p>
            <p>• <strong>Fiber F:</strong> Extra degrees of freedom at each point (e.g., U(1) phase)</p>
            <p>• <strong>Total space E:</strong> M × F locally (but may twist globally!)</p>
            <p>• <strong>Connection A:</strong> Tells how to parallel transport in the fiber</p>
          </div>
        </SubSection>

        <Formula label="Connection (gauge field)">
          A = Aᵢ dxⁱ (local 1-form)
        </Formula>

        <Z2Connection
          formula="F = dA + A ∧ A"
          description="Field strength = curvature of the connection"
        />
      </Section>

      <Section title="6. Connection to Z² Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="T³"
            description="The 3-torus has a flat metric: ds² = dx² + dy² + dz² with x ~ x + 2π"
          />
          <Z2Connection
            formula="T³/Z₂"
            description="Orbifold has curvature singularities at 8 fixed points"
          />
          <Z2Connection
            formula="A = Aᵢ dxⁱ"
            description="D-brane gauge fields are connections on bundles over T³/Z₂"
          />
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Differential Geometry Matters</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Metrics on T³:</strong> Define the geometry of extra dimensions</li>
            <li>• <strong>Curvature:</strong> Orbifold singularities contribute to index theorems</li>
            <li>• <strong>Connections:</strong> Gauge fields live on fiber bundles</li>
            <li>• <strong>Geodesics:</strong> Wrapped branes follow geodesics on T³</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Calculate the line element ds² for the 2-sphere of radius R in spherical coordinates.</li>
          <li>What is the Gaussian curvature K of a sphere of radius R? (Answer: K = 1/R²)</li>
          <li>Show that great circles on a sphere are geodesics.</li>
          <li>A cylinder has K = 0 (it's intrinsically flat!). Why is this surprising?</li>
          <li>For a U(1) bundle over a circle, the fiber is also a circle. What is the total space?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
