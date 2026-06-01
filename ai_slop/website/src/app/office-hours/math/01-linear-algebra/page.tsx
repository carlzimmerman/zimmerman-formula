'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Matrix Multiplication Visualizer
function MatrixMultiplyViz() {
  const [a, setA] = useState([[1, 2], [3, 4]])
  const [b, setB] = useState([[5, 6], [7, 8]])

  const result = [
    [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
    [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
  ]

  const [highlight, setHighlight] = useState<[number, number] | null>(null)

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-center gap-2 text-sm">
        {/* Matrix A */}
        <div className="bg-blue-50 p-2 rounded border border-blue-200">
          <div className="text-xs text-blue-600 text-center mb-1">A</div>
          <div className="grid grid-cols-2 gap-1">
            {a.flat().map((val, i) => (
              <div
                key={i}
                className={`w-8 h-8 flex items-center justify-center font-mono text-sm border rounded ${
                  highlight && Math.floor(i / 2) === highlight[0]
                    ? 'bg-blue-200 border-blue-400'
                    : 'bg-white border-gray-200'
                }`}
              >
                {val}
              </div>
            ))}
          </div>
        </div>

        <span className="text-xl text-gray-400">×</span>

        {/* Matrix B */}
        <div className="bg-green-50 p-2 rounded border border-green-200">
          <div className="text-xs text-green-600 text-center mb-1">B</div>
          <div className="grid grid-cols-2 gap-1">
            {b.flat().map((val, i) => (
              <div
                key={i}
                className={`w-8 h-8 flex items-center justify-center font-mono text-sm border rounded ${
                  highlight && i % 2 === highlight[1]
                    ? 'bg-green-200 border-green-400'
                    : 'bg-white border-gray-200'
                }`}
              >
                {val}
              </div>
            ))}
          </div>
        </div>

        <span className="text-xl text-gray-400">=</span>

        {/* Result */}
        <div className="bg-purple-50 p-2 rounded border border-purple-200">
          <div className="text-xs text-purple-600 text-center mb-1">A×B</div>
          <div className="grid grid-cols-2 gap-1">
            {result.flat().map((val, i) => (
              <div
                key={i}
                className={`w-10 h-8 flex items-center justify-center font-mono text-sm border rounded cursor-pointer transition-colors ${
                  highlight && Math.floor(i / 2) === highlight[0] && i % 2 === highlight[1]
                    ? 'bg-purple-300 border-purple-500'
                    : 'bg-white border-gray-200 hover:bg-purple-100'
                }`}
                onMouseEnter={() => setHighlight([Math.floor(i / 2), i % 2])}
                onMouseLeave={() => setHighlight(null)}
              >
                {val}
              </div>
            ))}
          </div>
        </div>
      </div>

      {highlight && (
        <div className="text-center text-sm bg-gray-50 p-2 rounded">
          <span className="text-blue-600">Row {highlight[0] + 1}</span>
          <span className="text-gray-400"> · </span>
          <span className="text-green-600">Col {highlight[1] + 1}</span>
          <span className="text-gray-400"> = </span>
          <span className="font-mono">
            {a[highlight[0]][0]}×{b[0][highlight[1]]} + {a[highlight[0]][1]}×{b[1][highlight[1]]}
          </span>
          <span className="text-gray-400"> = </span>
          <span className="text-purple-600 font-bold">{result[highlight[0]][highlight[1]]}</span>
        </div>
      )}

      <p className="text-xs text-gray-500 text-center">
        Hover over result elements to see how they're computed
      </p>
    </div>
  )
}

// Eigenvalue Visualization
function EigenvalueViz() {
  const [angle, setAngle] = useState(30)

  const theta = angle * Math.PI / 180
  const matrix = [
    [Math.cos(theta), -Math.sin(theta)],
    [Math.sin(theta), Math.cos(theta)],
  ]

  // For rotation matrix, eigenvalues are e^(±iθ)
  const eigenReal = Math.cos(theta)
  const eigenImag = Math.sin(theta)

  // Sample vectors
  const vectors = [
    { x: 1, y: 0, color: '#EF4444', label: 'v₁' },
    { x: 0, y: 1, color: '#3B82F6', label: 'v₂' },
    { x: 1, y: 1, color: '#10B981', label: 'v₃' },
  ]

  const transform = (v: { x: number; y: number }) => ({
    x: matrix[0][0] * v.x + matrix[0][1] * v.y,
    y: matrix[1][0] * v.x + matrix[1][1] * v.y,
  })

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Rotation angle θ = {angle}°
        </label>
        <input
          type="range"
          min="0"
          max="180"
          value={angle}
          onChange={(e) => setAngle(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <div className="text-sm font-medium text-gray-700 mb-2 text-center">
            Matrix Action: Av
          </div>
          <svg viewBox="-2 -2 4 4" className="w-full max-w-xs mx-auto bg-white border border-gray-200 rounded">
            {/* Grid */}
            <line x1="-1.8" y1="0" x2="1.8" y2="0" stroke="#E5E7EB" strokeWidth="0.02" />
            <line x1="0" y1="-1.8" x2="0" y2="1.8" stroke="#E5E7EB" strokeWidth="0.02" />

            {/* Original and transformed vectors */}
            {vectors.map((v, i) => {
              const tv = transform(v)
              return (
                <g key={i}>
                  {/* Original */}
                  <line
                    x1="0"
                    y1="0"
                    x2={v.x}
                    y2={-v.y}
                    stroke={v.color}
                    strokeWidth="0.06"
                    opacity="0.4"
                  />
                  {/* Transformed */}
                  <line
                    x1="0"
                    y1="0"
                    x2={tv.x}
                    y2={-tv.y}
                    stroke={v.color}
                    strokeWidth="0.08"
                  />
                  <circle cx={tv.x} cy={-tv.y} r="0.08" fill={v.color} />
                </g>
              )
            })}

            {/* Labels */}
            <text x="1.5" y="0.2" fontSize="0.2" fill="#6B7280">x</text>
            <text x="0.1" y="-1.5" fontSize="0.2" fill="#6B7280">y</text>
          </svg>
        </div>

        <div className="space-y-3">
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-xs text-gray-500 mb-1">Rotation Matrix</div>
            <div className="font-mono text-sm grid grid-cols-2 gap-1 w-fit">
              <div className="bg-white p-1 rounded border text-center">{matrix[0][0].toFixed(2)}</div>
              <div className="bg-white p-1 rounded border text-center">{matrix[0][1].toFixed(2)}</div>
              <div className="bg-white p-1 rounded border text-center">{matrix[1][0].toFixed(2)}</div>
              <div className="bg-white p-1 rounded border text-center">{matrix[1][1].toFixed(2)}</div>
            </div>
          </div>

          <div className="bg-purple-50 p-3 rounded border border-purple-200">
            <div className="text-xs text-purple-600 mb-1">Eigenvalues (complex)</div>
            <div className="font-mono text-sm">
              λ = {eigenReal.toFixed(2)} ± {eigenImag.toFixed(2)}i
            </div>
            <div className="text-xs text-gray-500 mt-1">
              = e<sup>±iθ</sup>
            </div>
          </div>

          <div className="text-xs text-gray-600">
            Rotation matrices have <strong>complex eigenvalues</strong> (except at 0° and 180°).
            This is why quantum mechanics needs complex numbers!
          </div>
        </div>
      </div>
    </div>
  )
}

// Trace Visualization
function TraceViz() {
  const [a11, setA11] = useState(3)
  const [a22, setA22] = useState(5)
  const [a33, setA33] = useState(2)

  const trace = a11 + a22 + a33

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-center gap-4">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="grid grid-cols-3 gap-1 font-mono text-sm">
            <input
              type="number"
              value={a11}
              onChange={(e) => setA11(Number(e.target.value))}
              className="w-10 h-8 text-center border rounded bg-yellow-100 border-yellow-400"
            />
            <div className="w-10 h-8 flex items-center justify-center bg-gray-100 rounded">0</div>
            <div className="w-10 h-8 flex items-center justify-center bg-gray-100 rounded">0</div>

            <div className="w-10 h-8 flex items-center justify-center bg-gray-100 rounded">0</div>
            <input
              type="number"
              value={a22}
              onChange={(e) => setA22(Number(e.target.value))}
              className="w-10 h-8 text-center border rounded bg-yellow-100 border-yellow-400"
            />
            <div className="w-10 h-8 flex items-center justify-center bg-gray-100 rounded">0</div>

            <div className="w-10 h-8 flex items-center justify-center bg-gray-100 rounded">0</div>
            <div className="w-10 h-8 flex items-center justify-center bg-gray-100 rounded">0</div>
            <input
              type="number"
              value={a33}
              onChange={(e) => setA33(Number(e.target.value))}
              className="w-10 h-8 text-center border rounded bg-yellow-100 border-yellow-400"
            />
          </div>
        </div>

        <div className="text-center">
          <div className="text-sm text-gray-500">Tr(A) =</div>
          <div className="text-2xl font-bold text-purple-600">{trace}</div>
        </div>
      </div>

      <div className="text-center text-sm text-gray-600">
        The trace is the sum of diagonal elements: {a11} + {a22} + {a33} = {trace}
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm">
        <strong>Key property:</strong> Tr(AB) = Tr(BA) — the trace is cyclic!
        <br />
        This makes it useful for physics: it doesn't depend on the basis you choose.
      </div>
    </div>
  )
}

export default function LinearAlgebraPage() {
  return (
    <DocumentLayout
      title="Linear Algebra"
      description="Vectors, matrices, and the language of quantum mechanics"
      phase="math"
      currentIndex={1}
      prevLink={{ href: '/office-hours/math/00-prerequisites', title: 'Prerequisites' }}
      nextLink={{ href: '/office-hours/math/02-group-theory', title: 'Group Theory' }}
    >
      <Section title="1. Vectors">
        <p className="text-gray-700 mb-4">
          A <strong>vector</strong> is an ordered list of numbers. In physics, vectors represent
          positions, velocities, forces, and quantum states.
        </p>

        <Formula>
          v = (v₁, v₂, v₃) or |v⟩ = v₁|1⟩ + v₂|2⟩ + v₃|3⟩
        </Formula>

        <SubSection title="Vector Operations">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="bg-gray-50 p-3 rounded">
              <strong>Addition:</strong>
              <div className="font-mono mt-1">(a, b) + (c, d) = (a+c, b+d)</div>
            </div>
            <div className="bg-gray-50 p-3 rounded">
              <strong>Scalar multiplication:</strong>
              <div className="font-mono mt-1">λ(a, b) = (λa, λb)</div>
            </div>
            <div className="bg-blue-50 p-3 rounded border border-blue-200">
              <strong>Dot product:</strong>
              <div className="font-mono mt-1">u · v = u₁v₁ + u₂v₂ + u₃v₃</div>
            </div>
            <div className="bg-green-50 p-3 rounded border border-green-200">
              <strong>Cross product:</strong>
              <div className="font-mono mt-1">u × v = (u₂v₃ - u₃v₂, ...)</div>
            </div>
          </div>
        </SubSection>

        <KeyPoint>
          In quantum mechanics, we use <strong>Dirac notation</strong>: |ψ⟩ is a "ket" (column vector),
          ⟨ψ| is a "bra" (row vector), and ⟨φ|ψ⟩ is the inner product.
        </KeyPoint>
      </Section>

      <Section title="2. Matrices">
        <p className="text-gray-700 mb-4">
          A <strong>matrix</strong> is a rectangular array of numbers. Matrices represent
          linear transformations — operations that preserve addition and scalar multiplication.
        </p>

        <InteractiveBox title="Matrix Multiplication">
          <MatrixMultiplyViz />
        </InteractiveBox>

        <SubSection title="Important Matrix Types">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2 text-left">Type</th>
                  <th className="border border-gray-200 p-2 text-left">Property</th>
                  <th className="border border-gray-200 p-2 text-left">Physics Use</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2">Symmetric</td>
                  <td className="border border-gray-200 p-2 font-mono">A = Aᵀ</td>
                  <td className="border border-gray-200 p-2">Real observables</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Hermitian</td>
                  <td className="border border-gray-200 p-2 font-mono">A = A†</td>
                  <td className="border border-gray-200 p-2">Quantum observables</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Unitary</td>
                  <td className="border border-gray-200 p-2 font-mono">U†U = I</td>
                  <td className="border border-gray-200 p-2">Time evolution, rotations</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">Orthogonal</td>
                  <td className="border border-gray-200 p-2 font-mono">OᵀO = I</td>
                  <td className="border border-gray-200 p-2">3D rotations</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>
      </Section>

      <Section title="3. Eigenvalues and Eigenvectors">
        <p className="text-gray-700 mb-4">
          An <strong>eigenvector</strong> of matrix A is a special vector that only gets scaled when A acts on it:
        </p>

        <Formula label="Eigenvalue equation">
          A|v⟩ = λ|v⟩
        </Formula>

        <p className="text-gray-700 mb-4">
          Here λ is the <strong>eigenvalue</strong> — the scale factor.
        </p>

        <InteractiveBox title="Rotation Matrix and Complex Eigenvalues">
          <EigenvalueViz />
        </InteractiveBox>

        <KeyPoint>
          <strong>Quantum measurements give eigenvalues!</strong>
          <br />
          When you measure observable A on state |ψ⟩, you always get one of A's eigenvalues.
          The eigenvectors are the "definite value" states.
        </KeyPoint>
      </Section>

      <Section title="4. The Trace">
        <p className="text-gray-700 mb-4">
          The <strong>trace</strong> of a matrix is the sum of its diagonal elements:
        </p>

        <Formula>
          Tr(A) = a₁₁ + a₂₂ + ... + aₙₙ = Σᵢ aᵢᵢ
        </Formula>

        <InteractiveBox title="Trace Calculator">
          <TraceViz />
        </InteractiveBox>

        <SubSection title="Trace Properties">
          <div className="space-y-2 text-gray-700">
            <p><strong>Cyclic:</strong> Tr(ABC) = Tr(BCA) = Tr(CAB)</p>
            <p><strong>Linear:</strong> Tr(A + B) = Tr(A) + Tr(B)</p>
            <p><strong>Sum of eigenvalues:</strong> Tr(A) = λ₁ + λ₂ + ... + λₙ</p>
          </div>
        </SubSection>

        <Z2Connection
          formula="rank(G_SM) = Tr(Cartan) = 4"
          description="The rank of the Standard Model gauge group equals the trace of its Cartan generators"
        />
      </Section>

      <Section title="5. Connection to Z² Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="4Z² + 3 = α⁻¹"
            description="The '4' comes from rank(SU(3)×SU(2)×U(1)) = 2+1+1 = 4"
          />
          <Z2Connection
            formula="Tr(T_a T_b) = δ_ab/2"
            description="Generator normalization determines gauge coupling relations"
          />
          <Z2Connection
            formula="|ψ|² = ⟨ψ|ψ⟩"
            description="Probability from inner product structure"
          />
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Linear Algebra Matters</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Quantum states</strong> are vectors in Hilbert space</li>
            <li>• <strong>Observables</strong> are Hermitian matrices</li>
            <li>• <strong>Symmetries</strong> are represented by unitary matrices</li>
            <li>• <strong>Gauge groups</strong> are matrix Lie groups</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Multiply the matrices [[1,2],[3,4]] and [[0,1],[1,0]]. Is AB = BA?</li>
          <li>Find the eigenvalues of [[2,1],[1,2]]. Verify Tr(A) = λ₁ + λ₂.</li>
          <li>Show that rotation matrices satisfy RᵀR = I.</li>
          <li>Calculate Tr(AB) and Tr(BA) for two 2×2 matrices of your choice.</li>
          <li>Why must quantum observables be Hermitian? (Hint: eigenvalues)</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
