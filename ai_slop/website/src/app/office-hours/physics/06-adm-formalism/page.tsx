'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// 3+1 Decomposition Visualization
function ThreePlusOneViz() {
  const [time, setTime] = useState(0)
  const [showFoliation, setShowFoliation] = useState(true)

  // Generate multiple spatial slices
  const slices = Array.from({ length: 7 }, (_, i) => ({
    t: i * 0.5 - 1.5,
    offset: Math.sin(i * 0.3) * 5,
    scale: 1 + Math.sin(i * 0.2) * 0.1
  }))

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Time coordinate: t = {time.toFixed(2)}
        </label>
        <input
          type="range"
          min="-1.5"
          max="1.5"
          step="0.1"
          value={time}
          onChange={(e) => setTime(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gradient-to-b from-gray-900 to-gray-800 rounded-lg">
        {/* Time axis */}
        <line x1="30" y1="180" x2="30" y2="20" stroke="#9CA3AF" strokeWidth="2" />
        <polygon points="30,15 25,25 35,25" fill="#9CA3AF" />
        <text x="40" y="25" fontSize="12" fill="#9CA3AF">t (time)</text>

        {/* Spatial slices */}
        {showFoliation && slices.map((slice, i) => {
          const y = 100 - slice.t * 50
          const isCurrentSlice = Math.abs(slice.t - time) < 0.3
          return (
            <g key={i} opacity={isCurrentSlice ? 1 : 0.3}>
              <ellipse
                cx={160}
                cy={y}
                rx={100 * slice.scale}
                ry={20}
                fill="none"
                stroke={isCurrentSlice ? '#4ADE80' : '#6B7280'}
                strokeWidth={isCurrentSlice ? 2 : 1}
              />
              {isCurrentSlice && (
                <text x="270" y={y + 4} fontSize="10" fill="#4ADE80">
                  Sigma_t
                </text>
              )}
            </g>
          )
        })}

        {/* Normal vector */}
        {showFoliation && (
          <g>
            <line
              x1={160}
              y1={100 - time * 50 + 20}
              x2={160}
              y2={100 - time * 50 - 25}
              stroke="#F59E0B"
              strokeWidth="2"
            />
            <polygon
              points={`160,${100 - time * 50 - 30} 155,${100 - time * 50 - 20} 165,${100 - time * 50 - 20}`}
              fill="#F59E0B"
            />
            <text x="170" y={100 - time * 50 - 20} fontSize="10" fill="#F59E0B">n^mu</text>
          </g>
        )}

        {/* Labels */}
        <text x="150" y="190" fontSize="10" textAnchor="middle" fill="#9CA3AF">
          Spacetime foliated into spatial slices
        </text>
      </svg>

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={showFoliation}
          onChange={(e) => setShowFoliation(e.target.checked)}
          className="rounded"
        />
        <label className="text-sm text-gray-600">Show foliation</label>
      </div>

      <div className="bg-green-50 p-3 rounded border border-green-200 text-sm">
        <strong>3+1 decomposition:</strong> Spacetime is sliced into a family of 3D spatial
        hypersurfaces Sigma_t, each labeled by time t. The normal vector n^mu points in the time direction.
      </div>
    </div>
  )
}

// ADM Variables Visualization
function ADMVariablesViz() {
  const [lapse, setLapse] = useState(1)
  const [shiftX, setShiftX] = useState(0)
  const [shiftY, setShiftY] = useState(0)

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Lapse N = {lapse.toFixed(2)}
          </label>
          <input
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            value={lapse}
            onChange={(e) => setLapse(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Shift N^x = {shiftX.toFixed(2)}
          </label>
          <input
            type="range"
            min="-1"
            max="1"
            step="0.1"
            value={shiftX}
            onChange={(e) => setShiftX(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Shift N^y = {shiftY.toFixed(2)}
          </label>
          <input
            type="range"
            min="-1"
            max="1"
            step="0.1"
            value={shiftY}
            onChange={(e) => setShiftY(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-white border border-gray-200 rounded">
        {/* Two spatial slices */}
        <ellipse cx="150" cy="140" rx="100" ry="25" fill="#E5E7EB" stroke="#9CA3AF" strokeWidth="1" />
        <ellipse cx="150" cy={60} rx="100" ry="25" fill="#DBEAFE" stroke="#3B82F6" strokeWidth="2" />

        {/* Time labels */}
        <text x="260" y="145" fontSize="10" fill="#6B7280">t</text>
        <text x="260" y="65" fontSize="10" fill="#3B82F6">t + dt</text>

        {/* A point on lower slice */}
        <circle cx="150" cy="140" r="5" fill="#10B981" />
        <text x="155" y="155" fontSize="10" fill="#10B981">P</text>

        {/* Normal evolution (lapse) */}
        <line
          x1="150"
          y1="140"
          x2="150"
          y2={140 - 60 * lapse}
          stroke="#F59E0B"
          strokeWidth="2"
          strokeDasharray="4,2"
        />
        <text x="155" y={140 - 30 * lapse} fontSize="10" fill="#F59E0B">N*dt</text>

        {/* Shift vector */}
        <line
          x1="150"
          y1="60"
          x2={150 + shiftX * 40}
          y2={60 + shiftY * 15}
          stroke="#8B5CF6"
          strokeWidth="2"
        />
        {(shiftX !== 0 || shiftY !== 0) && (
          <>
            <polygon
              points={`${150 + shiftX * 40},${60 + shiftY * 15} ${145 + shiftX * 35},${55 + shiftY * 12} ${145 + shiftX * 35},${65 + shiftY * 12}`}
              fill="#8B5CF6"
            />
            <text x={155 + shiftX * 40} y={55 + shiftY * 15} fontSize="10" fill="#8B5CF6">N^i</text>
          </>
        )}

        {/* Final position */}
        <circle cx={150 + shiftX * 40} cy={60 + shiftY * 15} r="5" fill="#3B82F6" />
      </svg>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="bg-amber-50 p-3 rounded border border-amber-200">
          <strong className="text-amber-700">Lapse N:</strong>
          <div className="text-gray-600">How fast proper time advances between slices. N = 1 means coordinate time equals proper time.</div>
        </div>
        <div className="bg-purple-50 p-3 rounded border border-purple-200">
          <strong className="text-purple-700">Shift N^i:</strong>
          <div className="text-gray-600">How spatial coordinates slide between slices. Non-zero shift means coordinates move in space.</div>
        </div>
      </div>
    </div>
  )
}

// Extrinsic Curvature Visualization
function ExtrinsicCurvatureViz() {
  const [embedding, setEmbedding] = useState(0.5)

  // Generate surface points
  const generateSurface = () => {
    const points = []
    for (let i = -10; i <= 10; i++) {
      const x = i * 10
      const y = embedding * Math.sin(i * 0.3) * 20
      points.push({ x: 150 + x, y: 100 - y })
    }
    return points
  }

  const surfacePoints = generateSurface()
  const pathD = `M ${surfacePoints.map(p => `${p.x},${p.y}`).join(' L ')}`

  // Compute approximate K at center
  const K_approx = embedding * 0.3

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Surface embedding: {embedding.toFixed(2)}
        </label>
        <input
          type="range"
          min="0"
          max="1.5"
          step="0.1"
          value={embedding}
          onChange={(e) => setEmbedding(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto bg-gray-900 rounded-lg">
        {/* Surface */}
        <path d={pathD} fill="none" stroke="#4ADE80" strokeWidth="3" />

        {/* Normal vectors at several points */}
        {[-5, 0, 5].map((i) => {
          const x = 150 + i * 20
          const y = 100 - embedding * Math.sin(i * 0.3) * 20
          const angle = -embedding * Math.cos(i * 0.3) * 0.3
          const nx = -Math.sin(angle) * 30
          const ny = -Math.cos(angle) * 30
          return (
            <g key={i}>
              <line
                x1={x}
                y1={y}
                x2={x + nx}
                y2={y + ny}
                stroke="#F59E0B"
                strokeWidth="2"
              />
              <circle cx={x + nx} cy={y + ny} r="3" fill="#F59E0B" />
            </g>
          )
        })}

        {/* Labels */}
        <text x="150" y="180" textAnchor="middle" fontSize="10" fill="#9CA3AF">
          Normal vectors change direction = extrinsic curvature
        </text>
      </svg>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-50 p-3 rounded text-center">
          <div className="text-sm text-gray-500">Surface curvature</div>
          <div className="text-xl font-bold text-gray-800">
            K ~ {K_approx.toFixed(2)}
          </div>
        </div>
        <div className="bg-green-50 p-3 rounded border border-green-200 text-center">
          <div className="text-sm text-gray-500">Flat embedding (K=0)</div>
          <div className="text-xl font-bold text-green-600">
            {embedding < 0.1 ? 'Yes' : 'No'}
          </div>
        </div>
      </div>

      <div className="bg-blue-50 p-3 rounded border border-blue-200 text-sm">
        <strong>Extrinsic curvature K_ij:</strong> Measures how the spatial slice bends within
        the higher-dimensional spacetime. Unlike intrinsic curvature (within the slice),
        this captures the embedding.
      </div>
    </div>
  )
}

export default function ADMFormalismPage() {
  return (
    <DocumentLayout
      title="ADM Formalism"
      description="The 3+1 decomposition of spacetime for canonical gravity"
      phase="physics"
      currentIndex={6}
      prevLink={{ href: '/office-hours/physics/05-general-relativity', title: 'General Relativity' }}
      nextLink={{ href: '/office-hours/physics/07-cosmology', title: 'Cosmology' }}
    >
      <Section title="1. The 3+1 Decomposition">
        <p className="text-gray-700 mb-4">
          The <strong>ADM formalism</strong> (Arnowitt-Deser-Misner) reformulates general relativity
          by splitting 4D spacetime into 3D space evolving in time. This is essential for
          canonical quantization and numerical relativity.
        </p>

        <InteractiveBox title="Spacetime Foliation">
          <ThreePlusOneViz />
        </InteractiveBox>

        <KeyPoint>
          The 3+1 decomposition rewrites the 4D metric as a 3D spatial metric plus
          lapse and shift functions that describe how time flows and coordinates move.
        </KeyPoint>
      </Section>

      <Section title="2. ADM Variables">
        <p className="text-gray-700 mb-4">
          The 4D metric g_uv is decomposed into:
        </p>

        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2">Variable</th>
                <th className="border border-gray-200 p-2">Symbol</th>
                <th className="border border-gray-200 p-2">Meaning</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2">Spatial metric</td>
                <td className="border border-gray-200 p-2 font-mono">gamma_ij</td>
                <td className="border border-gray-200 p-2">3D geometry of each slice</td>
              </tr>
              <tr className="bg-amber-50">
                <td className="border border-gray-200 p-2">Lapse</td>
                <td className="border border-gray-200 p-2 font-mono">N</td>
                <td className="border border-gray-200 p-2">Proper time between slices</td>
              </tr>
              <tr className="bg-purple-50">
                <td className="border border-gray-200 p-2">Shift</td>
                <td className="border border-gray-200 p-2 font-mono">N^i</td>
                <td className="border border-gray-200 p-2">Coordinate drift between slices</td>
              </tr>
            </tbody>
          </table>
        </div>

        <InteractiveBox title="Lapse and Shift">
          <ADMVariablesViz />
        </InteractiveBox>

        <SubSection title="The ADM Metric">
          <Formula label="4D line element">
            ds^2 = -N^2 dt^2 + gamma_ij (dx^i + N^i dt)(dx^j + N^j dt)
          </Formula>

          <p className="text-gray-700 mt-4">
            This decomposes the 10 components of g_uv into:
          </p>
          <ul className="list-disc list-inside text-gray-700 space-y-1 ml-4">
            <li>6 components in gamma_ij (symmetric 3x3 matrix)</li>
            <li>1 component in N (lapse function)</li>
            <li>3 components in N^i (shift vector)</li>
          </ul>
        </SubSection>
      </Section>

      <Section title="3. Extrinsic Curvature">
        <p className="text-gray-700 mb-4">
          The <strong>extrinsic curvature</strong> K_ij measures how each spatial slice
          is embedded in 4D spacetime - how much it curves in the time direction.
        </p>

        <InteractiveBox title="Extrinsic Curvature">
          <ExtrinsicCurvatureViz />
        </InteractiveBox>

        <Formula label="Definition">
          K_ij = -(1/2N)(d_t gamma_ij - D_i N_j - D_j N_i)
        </Formula>

        <div className="grid grid-cols-2 gap-3 my-4">
          <div className="bg-blue-50 p-3 rounded border border-blue-200">
            <strong>Intrinsic curvature (R):</strong>
            <div className="text-sm text-gray-600">Curvature within the 3D slice</div>
          </div>
          <div className="bg-green-50 p-3 rounded border border-green-200">
            <strong>Extrinsic curvature (K):</strong>
            <div className="text-sm text-gray-600">How the slice bends in 4D spacetime</div>
          </div>
        </div>

        <KeyPoint>
          The pair (gamma_ij, K_ij) forms the <strong>canonical variables</strong> for gravity,
          analogous to position and momentum in mechanics. This is the starting point for
          quantum gravity!
        </KeyPoint>
      </Section>

      <Section title="4. Constraints">
        <p className="text-gray-700 mb-4">
          Not all (gamma_ij, K_ij) configurations are valid initial data for Einstein's equations.
          They must satisfy <strong>constraint equations</strong>:
        </p>

        <SubSection title="Hamiltonian Constraint">
          <Formula>
            H = R + K^2 - K_ij K^ij = 16 pi G rho
          </Formula>
          <p className="text-gray-700 mt-2">
            Relates the spatial curvature and extrinsic curvature to energy density.
            This constraint generates time evolution.
          </p>
        </SubSection>

        <SubSection title="Momentum Constraints">
          <Formula>
            H_i = D_j(K^j_i - delta^j_i K) = 8 pi G j_i
          </Formula>
          <p className="text-gray-700 mt-2">
            Relates the gradient of extrinsic curvature to momentum density.
            These generate spatial diffeomorphisms.
          </p>
        </SubSection>

        <div className="bg-amber-50 p-4 rounded border border-amber-200 my-4">
          <h4 className="font-semibold text-amber-800 mb-2">Physical Meaning</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>- <strong>H = 0:</strong> Energy is conserved (no creation from nothing)</li>
            <li>- <strong>H_i = 0:</strong> Momentum is conserved (gauge invariance)</li>
            <li>- <strong>4 constraints</strong> reduce 12 variables to 8 physical degrees of freedom</li>
            <li>- <strong>2 polarizations</strong> of gravitational waves (4 more gauge freedoms)</li>
          </ul>
        </div>
      </Section>

      <Section title="5. Evolution Equations">
        <p className="text-gray-700 mb-4">
          Given valid initial data, the ADM formalism provides evolution equations:
        </p>

        <Formula label="Evolution of spatial metric">
          d_t gamma_ij = -2N K_ij + D_i N_j + D_j N_i
        </Formula>

        <Formula label="Evolution of extrinsic curvature">
          d_t K_ij = -D_i D_j N + N(R_ij + K K_ij - 2 K_ik K^k_j) + ...
        </Formula>

        <div className="bg-blue-50 p-3 rounded border border-blue-200 text-sm my-4">
          <strong>Numerical relativity:</strong> These equations are solved on supercomputers
          to simulate black hole mergers and neutron star collisions. LIGO detections
          are compared to these simulations!
        </div>
      </Section>

      <Section title="6. Connection to Z2 Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="(gamma_ij, K_ij)"
            description="Canonical variables for gravity enable quantization and cosmological calculations"
          />
          <Z2Connection
            formula="H = R + K^2 - K_ij K^ij"
            description="The Hamiltonian constraint must be solved on the T^3/Z_2 compactification"
          />
          <Z2Connection
            formula="3+1 split"
            description="Separates compact spatial dimensions (T^3/Z_2) from cosmic time evolution"
          />
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why ADM Matters for Z2</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>- <strong>Canonical quantization:</strong> Path to quantum gravity</li>
            <li>- <strong>Constraint algebra:</strong> Tests consistency of compactification</li>
            <li>- <strong>Moduli dynamics:</strong> Extra dimension sizes as dynamical variables</li>
            <li>- <strong>Cosmology:</strong> FLRW metric in ADM form gives Friedmann equations</li>
          </ul>
        </div>
      </Section>

      <Section title="7. BSSN Formulation">
        <p className="text-gray-700 mb-4">
          For numerical stability, the ADM equations are often recast in the <strong>BSSN</strong>
          (Baumgarte-Shapiro-Shibata-Nakamura) form:
        </p>

        <div className="grid grid-cols-2 gap-3 my-4 text-sm">
          <div className="bg-gray-50 p-3 rounded">
            <strong>ADM:</strong>
            <div className="text-gray-600">Original formulation, elegant but numerically unstable</div>
          </div>
          <div className="bg-green-50 p-3 rounded border border-green-200">
            <strong>BSSN:</strong>
            <div className="text-gray-600">Conformal decomposition, stable for simulations</div>
          </div>
        </div>

        <Formula label="Conformal decomposition">
          gamma_ij = e^(4 phi) * gamma_tilde_ij (det gamma_tilde = 1)
        </Formula>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Write the Minkowski metric ds^2 = -dt^2 + dx^2 + dy^2 + dz^2 in ADM form. What are N and N^i?</li>
          <li>For the Schwarzschild solution in Schwarzschild coordinates, find the lapse N(r).</li>
          <li>Show that a flat spatial slice (K_ij = 0) in flat spacetime satisfies both constraints.</li>
          <li>How many independent components does K_ij have? (Hint: it is symmetric)</li>
          <li>Why are the constraints called "initial value" constraints?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
