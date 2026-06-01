'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Complex Number Plane Visualization
function ComplexPlaneViz() {
  const [real, setReal] = useState(3)
  const [imag, setImag] = useState(4)

  const magnitude = Math.sqrt(real * real + imag * imag)
  const angle = Math.atan2(imag, real) * 180 / Math.PI

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Real part (x)</label>
          <input
            type="range"
            min="-5"
            max="5"
            step="0.5"
            value={real}
            onChange={(e) => setReal(Number(e.target.value))}
            className="w-full"
          />
          <div className="text-center font-mono">{real}</div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Imaginary part (y)</label>
          <input
            type="range"
            min="-5"
            max="5"
            step="0.5"
            value={imag}
            onChange={(e) => setImag(Number(e.target.value))}
            className="w-full"
          />
          <div className="text-center font-mono">{imag}i</div>
        </div>
      </div>

      <svg viewBox="-6 -6 12 12" className="w-full max-w-xs mx-auto bg-white border border-gray-200 rounded">
        {/* Grid */}
        <defs>
          <pattern id="grid" width="1" height="1" patternUnits="userSpaceOnUse">
            <path d="M 1 0 L 0 0 0 1" fill="none" stroke="#E5E7EB" strokeWidth="0.02" />
          </pattern>
        </defs>
        <rect x="-6" y="-6" width="12" height="12" fill="url(#grid)" />

        {/* Axes */}
        <line x1="-5.5" y1="0" x2="5.5" y2="0" stroke="#9CA3AF" strokeWidth="0.05" />
        <line x1="0" y1="-5.5" x2="0" y2="5.5" stroke="#9CA3AF" strokeWidth="0.05" />

        {/* Labels */}
        <text x="5.3" y="0.4" fontSize="0.4" fill="#6B7280">Re</text>
        <text x="0.2" y="-5.2" fontSize="0.4" fill="#6B7280">Im</text>

        {/* Vector */}
        <line x1="0" y1="0" x2={real} y2={-imag} stroke="#3B82F6" strokeWidth="0.1" />
        <circle cx={real} cy={-imag} r="0.2" fill="#3B82F6" />

        {/* Magnitude arc */}
        {magnitude > 0.5 && (
          <circle cx="0" cy="0" r={magnitude} fill="none" stroke="#3B82F6" strokeWidth="0.03" strokeDasharray="0.1,0.1" />
        )}
      </svg>

      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <div className="bg-gray-50 p-2 rounded">
          <div className="text-gray-500">z =</div>
          <div className="font-mono">{real} + {imag}i</div>
        </div>
        <div className="bg-blue-50 p-2 rounded">
          <div className="text-gray-500">|z| =</div>
          <div className="font-mono">{magnitude.toFixed(2)}</div>
        </div>
        <div className="bg-purple-50 p-2 rounded">
          <div className="text-gray-500">θ =</div>
          <div className="font-mono">{angle.toFixed(1)}°</div>
        </div>
      </div>
    </div>
  )
}

// Euler's Formula Visualization
function EulerFormulaViz() {
  const [theta, setTheta] = useState(45)

  const thetaRad = theta * Math.PI / 180
  const cosVal = Math.cos(thetaRad)
  const sinVal = Math.sin(thetaRad)

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Angle θ = {theta}° = {(theta * Math.PI / 180).toFixed(3)} rad
        </label>
        <input
          type="range"
          min="0"
          max="360"
          value={theta}
          onChange={(e) => setTheta(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <svg viewBox="-1.5 -1.5 3 3" className="w-full max-w-xs mx-auto bg-white border border-gray-200 rounded">
        {/* Unit circle */}
        <circle cx="0" cy="0" r="1" fill="none" stroke="#D1D5DB" strokeWidth="0.02" />

        {/* Axes */}
        <line x1="-1.3" y1="0" x2="1.3" y2="0" stroke="#9CA3AF" strokeWidth="0.02" />
        <line x1="0" y1="-1.3" x2="0" y2="1.3" stroke="#9CA3AF" strokeWidth="0.02" />

        {/* cos projection */}
        <line x1="0" y1="0" x2={cosVal} y2="0" stroke="#EF4444" strokeWidth="0.05" />
        <line x1={cosVal} y1="0" x2={cosVal} y2={-sinVal} stroke="#EF4444" strokeWidth="0.02" strokeDasharray="0.05,0.05" />

        {/* sin projection */}
        <line x1="0" y1="0" x2="0" y2={-sinVal} stroke="#3B82F6" strokeWidth="0.05" />
        <line x1="0" y1={-sinVal} x2={cosVal} y2={-sinVal} stroke="#3B82F6" strokeWidth="0.02" strokeDasharray="0.05,0.05" />

        {/* e^iθ vector */}
        <line x1="0" y1="0" x2={cosVal} y2={-sinVal} stroke="#8B5CF6" strokeWidth="0.06" />
        <circle cx={cosVal} cy={-sinVal} r="0.08" fill="#8B5CF6" />

        {/* Angle arc */}
        <path
          d={`M 0.3 0 A 0.3 0.3 0 ${theta > 180 ? 1 : 0} 0 ${0.3 * cosVal} ${-0.3 * sinVal}`}
          fill="none"
          stroke="#10B981"
          strokeWidth="0.03"
        />

        {/* Labels */}
        <text x="1.15" y="0.15" fontSize="0.15" fill="#6B7280">1</text>
        <text x="0.05" y="-1.1" fontSize="0.15" fill="#6B7280">i</text>
        <text x="-1.2" y="0.15" fontSize="0.15" fill="#6B7280">-1</text>
        <text x="0.05" y="1.2" fontSize="0.15" fill="#6B7280">-i</text>
      </svg>

      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <div className="bg-red-50 p-2 rounded border border-red-200">
          <div className="text-red-600 text-xs">cos θ</div>
          <div className="font-mono text-red-700">{cosVal.toFixed(3)}</div>
        </div>
        <div className="bg-blue-50 p-2 rounded border border-blue-200">
          <div className="text-blue-600 text-xs">sin θ</div>
          <div className="font-mono text-blue-700">{sinVal.toFixed(3)}</div>
        </div>
        <div className="bg-purple-50 p-2 rounded border border-purple-200">
          <div className="text-purple-600 text-xs">e^(iθ)</div>
          <div className="font-mono text-purple-700 text-xs">{cosVal.toFixed(2)} + {sinVal.toFixed(2)}i</div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-4 rounded-lg text-center">
        <div className="font-mono text-lg text-purple-800">
          e<sup>iθ</sup> = cos θ + i sin θ
        </div>
        <div className="text-sm text-gray-600 mt-2">
          At θ = π: e<sup>iπ</sup> = -1 → <strong>e<sup>iπ</sup> + 1 = 0</strong>
        </div>
      </div>
    </div>
  )
}

// Derivative Visualization
function DerivativeViz() {
  const [x, setX] = useState(1)
  const [h, setH] = useState(1)

  // f(x) = x²
  const f = (val: number) => val * val
  const df = 2 * x // exact derivative
  const approx = (f(x + h) - f(x)) / h // numerical approximation

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">x = {x}</label>
          <input
            type="range"
            min="-3"
            max="3"
            step="0.5"
            value={x}
            onChange={(e) => setX(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">h = {h.toFixed(2)}</label>
          <input
            type="range"
            min="0.01"
            max="2"
            step="0.01"
            value={h}
            onChange={(e) => setH(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      <svg viewBox="-4 -1 8 10" className="w-full max-w-sm mx-auto bg-white border border-gray-200 rounded">
        {/* Axes */}
        <line x1="-3.5" y1="0" x2="3.5" y2="0" stroke="#9CA3AF" strokeWidth="0.05" />
        <line x1="0" y1="-0.5" x2="0" y2="9" stroke="#9CA3AF" strokeWidth="0.05" />

        {/* Parabola f(x) = x² */}
        <path
          d="M -3 9 Q -2 4 -1 1 Q 0 0 1 1 Q 2 4 3 9"
          fill="none"
          stroke="#3B82F6"
          strokeWidth="0.08"
        />

        {/* Point at x */}
        <circle cx={x} cy={f(x)} r="0.15" fill="#EF4444" />

        {/* Point at x + h */}
        <circle cx={x + h} cy={f(x + h)} r="0.12" fill="#F97316" />

        {/* Secant line */}
        <line
          x1={x - 1}
          y1={f(x) - approx}
          x2={x + h + 1}
          y2={f(x) + approx * (h + 1)}
          stroke="#F97316"
          strokeWidth="0.05"
          strokeDasharray="0.1,0.1"
        />

        {/* Tangent line */}
        <line
          x1={x - 1.5}
          y1={f(x) - df * 1.5}
          x2={x + 1.5}
          y2={f(x) + df * 1.5}
          stroke="#10B981"
          strokeWidth="0.06"
        />

        {/* Labels */}
        <text x={x} y={f(x) + 0.6} fontSize="0.3" fill="#EF4444" textAnchor="middle">(x, x²)</text>
      </svg>

      <div className="grid grid-cols-2 gap-4 text-center text-sm">
        <div className="bg-orange-50 p-3 rounded border border-orange-200">
          <div className="text-orange-600 text-xs mb-1">Secant slope (approximation)</div>
          <div className="font-mono text-orange-700">[f(x+h) - f(x)] / h = {approx.toFixed(3)}</div>
        </div>
        <div className="bg-green-50 p-3 rounded border border-green-200">
          <div className="text-green-600 text-xs mb-1">Tangent slope (exact)</div>
          <div className="font-mono text-green-700">f'(x) = 2x = {df.toFixed(3)}</div>
        </div>
      </div>

      <div className="text-center text-sm text-gray-600">
        As h → 0, the secant line approaches the tangent line.
        <br />
        Error: {Math.abs(approx - df).toFixed(4)}
      </div>
    </div>
  )
}

export default function PrerequisitesPage() {
  return (
    <DocumentLayout
      title="Mathematical Prerequisites"
      description="Essential foundations: algebra, calculus, and complex numbers"
      phase="math"
      currentIndex={0}
      nextLink={{ href: '/office-hours/math/01-linear-algebra', title: 'Linear Algebra' }}
    >
      <Section title="1. Numbers: From Counting to Complex">
        <p className="text-gray-700 mb-4">
          Physics uses several number systems, each extending the previous one to solve new problems.
        </p>

        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-2 text-left">System</th>
                <th className="border border-gray-200 p-2 text-left">Symbol</th>
                <th className="border border-gray-200 p-2 text-left">Examples</th>
                <th className="border border-gray-200 p-2 text-left">New Capability</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-2">Natural</td>
                <td className="border border-gray-200 p-2 font-mono">ℕ</td>
                <td className="border border-gray-200 p-2">1, 2, 3, ...</td>
                <td className="border border-gray-200 p-2">Counting</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Integers</td>
                <td className="border border-gray-200 p-2 font-mono">ℤ</td>
                <td className="border border-gray-200 p-2">..., -2, -1, 0, 1, 2, ...</td>
                <td className="border border-gray-200 p-2">Subtraction (debts)</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Rationals</td>
                <td className="border border-gray-200 p-2 font-mono">ℚ</td>
                <td className="border border-gray-200 p-2">1/2, -3/4, 0.333...</td>
                <td className="border border-gray-200 p-2">Division (fractions)</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-2">Reals</td>
                <td className="border border-gray-200 p-2 font-mono">ℝ</td>
                <td className="border border-gray-200 p-2">π, √2, e</td>
                <td className="border border-gray-200 p-2">Limits, continuity</td>
              </tr>
              <tr className="bg-purple-50">
                <td className="border border-gray-200 p-2 font-medium">Complex</td>
                <td className="border border-gray-200 p-2 font-mono">ℂ</td>
                <td className="border border-gray-200 p-2">3 + 4i, e<sup>iπ</sup></td>
                <td className="border border-gray-200 p-2">√(-1), rotations</td>
              </tr>
            </tbody>
          </table>
        </div>

        <KeyPoint>
          <strong>Complex numbers are essential for quantum mechanics.</strong> The imaginary unit i = √(-1)
          allows us to describe wave functions, interference, and rotations naturally.
        </KeyPoint>
      </Section>

      <Section title="2. Complex Numbers">
        <SubSection title="The Imaginary Unit">
          <p className="text-gray-700 mb-4">
            Define <span className="font-mono">i = √(-1)</span>, so <span className="font-mono">i² = -1</span>.
          </p>
          <p className="text-gray-700 mb-4">
            A complex number has a <strong>real part</strong> and an <strong>imaginary part</strong>:
          </p>
          <Formula>z = x + iy</Formula>
        </SubSection>

        <InteractiveBox title="Complex Plane">
          <ComplexPlaneViz />
        </InteractiveBox>

        <SubSection title="Operations">
          <div className="space-y-2 text-gray-700">
            <p><strong>Addition:</strong> (a + bi) + (c + di) = (a+c) + (b+d)i</p>
            <p><strong>Multiplication:</strong> (a + bi)(c + di) = (ac - bd) + (ad + bc)i</p>
            <p><strong>Conjugate:</strong> z* = x - iy (flip the imaginary part)</p>
            <p><strong>Magnitude:</strong> |z| = √(x² + y²) = √(z · z*)</p>
          </div>
        </SubSection>

        <Z2Connection
          formula="|z|² = z · z*"
          description="This pattern appears throughout quantum mechanics: probability = |ψ|²"
        />
      </Section>

      <Section title="3. Euler's Formula">
        <p className="text-gray-700 mb-4">
          The most beautiful equation in mathematics connects exponentials, trigonometry, and complex numbers:
        </p>

        <Formula label="Euler's Formula">
          e<sup>iθ</sup> = cos θ + i sin θ
        </Formula>

        <InteractiveBox title="Euler's Formula on the Unit Circle">
          <EulerFormulaViz />
        </InteractiveBox>

        <SubSection title="Special Cases">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 my-4">
            <div className="bg-gray-50 p-3 rounded text-center">
              <div className="font-mono">e<sup>i·0</sup> = 1</div>
              <div className="text-sm text-gray-500">θ = 0</div>
            </div>
            <div className="bg-gray-50 p-3 rounded text-center">
              <div className="font-mono">e<sup>iπ/2</sup> = i</div>
              <div className="text-sm text-gray-500">θ = 90°</div>
            </div>
            <div className="bg-purple-50 p-3 rounded text-center border border-purple-200">
              <div className="font-mono">e<sup>iπ</sup> = -1</div>
              <div className="text-sm text-purple-600 font-medium">Euler's Identity!</div>
            </div>
          </div>
        </SubSection>

        <KeyPoint>
          <strong>Euler's identity: e<sup>iπ</sup> + 1 = 0</strong>
          <br />
          This connects the five most important constants: e, i, π, 1, and 0.
        </KeyPoint>
      </Section>

      <Section title="4. Calculus Essentials">
        <SubSection title="The Derivative">
          <p className="text-gray-700 mb-4">
            The derivative measures the <strong>instantaneous rate of change</strong>:
          </p>
          <Formula>
            f'(x) = lim<sub>h→0</sub> [f(x+h) - f(x)] / h
          </Formula>
        </SubSection>

        <InteractiveBox title="Derivative as Limit of Secants">
          <DerivativeViz />
        </InteractiveBox>

        <SubSection title="Key Derivatives">
          <div className="overflow-x-auto my-4">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">f(x)</th>
                  <th className="border border-gray-200 p-2">f'(x)</th>
                  <th className="border border-gray-200 p-2">Example Use</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2 font-mono">xⁿ</td>
                  <td className="border border-gray-200 p-2 font-mono">nxⁿ⁻¹</td>
                  <td className="border border-gray-200 p-2">Polynomial potentials</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2 font-mono">eˣ</td>
                  <td className="border border-gray-200 p-2 font-mono">eˣ</td>
                  <td className="border border-gray-200 p-2">Exponential decay</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2 font-mono">sin x</td>
                  <td className="border border-gray-200 p-2 font-mono">cos x</td>
                  <td className="border border-gray-200 p-2">Wave functions</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2 font-mono">ln x</td>
                  <td className="border border-gray-200 p-2 font-mono">1/x</td>
                  <td className="border border-gray-200 p-2">Entropy</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>

        <SubSection title="The Integral">
          <p className="text-gray-700 mb-4">
            The integral is the "reverse" of the derivative — it accumulates area under a curve:
          </p>
          <Formula>
            ∫ f(x) dx = F(x) + C where F'(x) = f(x)
          </Formula>

          <KeyPoint>
            <strong>Fundamental Theorem of Calculus:</strong> Differentiation and integration are inverse operations.
            <div className="font-mono mt-2">∫ₐᵇ f(x) dx = F(b) - F(a)</div>
          </KeyPoint>
        </SubSection>
      </Section>

      <Section title="5. Connection to Z² Framework">
        <p className="text-gray-700 mb-4">
          These prerequisites appear throughout the framework:
        </p>

        <div className="space-y-3">
          <Z2Connection
            formula="e^(iθ)"
            description="Complex exponentials describe quantum phases and wave functions"
          />
          <Z2Connection
            formula="∫ d³x"
            description="Integrals over 3-space appear in the action principle"
          />
          <Z2Connection
            formula="Z² = 32π/3"
            description="π appears because we're integrating over spheres!"
          />
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why These Matter</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Complex numbers:</strong> Quantum mechanics lives in ℂ</li>
            <li>• <strong>Euler's formula:</strong> Rotations, symmetries, Fourier analysis</li>
            <li>• <strong>Calculus:</strong> Everything is described by differential equations</li>
            <li>• <strong>π:</strong> Appears in Z² = 32π/3 because spheres have curved surfaces</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Calculate |3 + 4i| and verify it equals 5.</li>
          <li>Using Euler's formula, find e<sup>i(π/4)</sup> in the form a + bi.</li>
          <li>Differentiate f(x) = sin(2x) using the chain rule.</li>
          <li>Evaluate ∫₀^π sin(x) dx geometrically and algebraically.</li>
          <li>Show that i⁴ = 1. What does this tell you about powers of i?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
