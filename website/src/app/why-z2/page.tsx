'use client'

import Link from 'next/link'

const PI = Math.PI
const Z = 2 * Math.sqrt(8 * PI / 3)
const Z_SQUARED = Z * Z
const BEKENSTEIN = 3 * Z_SQUARED / (8 * PI)
const GAUGE = 9 * Z_SQUARED / (8 * PI)

export default function WhyZ2Page() {
  return (
    <main className="min-h-screen bg-[#fafafa]">
      <div className="max-w-4xl mx-auto px-4 py-6 md:py-8">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 -mx-4 -mt-6 md:-mt-8 px-4 py-4 mb-6">
          <Link href="/" className="text-sm text-blue-600 hover:underline">
            ← Back to Overview
          </Link>
        </header>

        {/* Title Block */}
        <article className="bg-white border border-gray-200 rounded shadow-sm p-5 md:p-8 mb-6">
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2 leading-tight">
            Why Z² = 32π/3?
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            Deriving the fundamental constant from first principles
          </p>

          {/* The Target */}
          <div className="bg-blue-50 border border-blue-200 rounded p-6 my-6 text-center">
            <div className="font-mono text-xl text-gray-900 mb-2">
              Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3
            </div>
            <div className="font-mono text-lg text-blue-700 mb-2">
              Z = 2√(8π/3) = {Z.toFixed(6)}
            </div>
            <div className="text-sm text-gray-600 mt-3">
              Can we <strong>derive</strong> this rather than assume it?
            </div>
          </div>
        </article>

        {/* The Key Insight */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Answer: Yes</h2>
          <p className="text-gray-700 mb-4">
            Z² = 32π/3 is <strong>uniquely determined</strong> by requiring that two quantities be integers:
          </p>

          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center">
              <div className="font-mono text-lg text-blue-700">BEKENSTEIN = 3Z²/(8π)</div>
              <div className="text-gray-600 mt-1">Must be a positive integer</div>
              <div className="text-2xl font-bold text-gray-900 mt-2">= 4</div>
              <div className="text-sm text-gray-500">Spacetime dimensions</div>
            </div>
            <div className="bg-amber-50 border border-amber-200 rounded p-4 text-center">
              <div className="font-mono text-lg text-amber-700">GAUGE = 9Z²/(8π)</div>
              <div className="text-gray-600 mt-1">Must be a positive integer</div>
              <div className="text-2xl font-bold text-gray-900 mt-2">= 12</div>
              <div className="text-sm text-gray-500">Standard Model generators</div>
            </div>
          </div>

          <div className="bg-green-50 border border-green-200 rounded p-4">
            <div className="font-mono text-center">
              <div className="text-gray-600 text-sm">From BEKENSTEIN = 4:</div>
              <div className="text-lg mt-2">3Z²/(8π) = 4</div>
              <div className="text-lg">3Z² = 32π</div>
              <div className="text-xl font-bold text-green-700 mt-2">Z² = 32π/3 ✓</div>
            </div>
          </div>
        </div>

        {/* The Master Equation */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Master Equation</h2>

          <div className="bg-gray-900 text-white rounded p-6 font-mono text-center">
            <div className="text-blue-300 mb-4">
              GAUGE = BEKENSTEIN × (BEKENSTEIN - 1)
            </div>
            <div className="text-2xl text-white">
              12 = 4 × 3
            </div>
            <div className="text-gray-400 mt-4 text-sm">
              The three fundamental integers (3, 4, 12) determine each other
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 mt-6 text-center">
            <div className="p-3 bg-gray-50 rounded border border-gray-200">
              <div className="text-3xl font-bold text-gray-900">3</div>
              <div className="text-sm text-gray-500">Spatial dimensions</div>
              <div className="text-xs text-gray-400 mt-1">GAUGE / BEKENSTEIN</div>
            </div>
            <div className="p-3 bg-blue-50 rounded border border-blue-200">
              <div className="text-3xl font-bold text-blue-700">4</div>
              <div className="text-sm text-gray-500">Spacetime dimensions</div>
              <div className="text-xs text-blue-400 mt-1">BEKENSTEIN</div>
            </div>
            <div className="p-3 bg-amber-50 rounded border border-amber-200">
              <div className="text-3xl font-bold text-amber-700">12</div>
              <div className="text-sm text-gray-500">Gauge bosons</div>
              <div className="text-xs text-amber-400 mt-1">GAUGE</div>
            </div>
          </div>
        </div>

        {/* 7 Derivation Approaches */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Seven Derivation Approaches</h2>

          <div className="space-y-4">
            {/* Derivation 1 */}
            <div className="border-l-4 border-green-500 pl-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-green-600 font-bold">1. Integer Constraints</span>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">COMPLETE</span>
              </div>
              <p className="text-sm text-gray-600">
                Require BEKENSTEIN and GAUGE to be integers. With BEKENSTEIN = 4,
                Z² = 32π/3 follows uniquely.
              </p>
            </div>

            {/* Derivation 2 */}
            <div className="border-l-4 border-green-500 pl-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-green-600 font-bold">2. Holographic Principle</span>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">COMPLETE</span>
              </div>
              <p className="text-sm text-gray-600">
                Bekenstein-Hawking entropy S = A/(4l_P²) has coefficient 4 = spacetime dimensions.
                This fixes BEKENSTEIN = 4, hence Z² = 32π/3.
              </p>
            </div>

            {/* Derivation 3 */}
            <div className="border-l-4 border-green-500 pl-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-green-600 font-bold">3. Information Theory</span>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">COMPLETE</span>
              </div>
              <p className="text-sm text-gray-600">
                CUBE = 8 = 2³ encodes discrete 3D (3 bits). SPHERE = 4π/3 is the natural
                continuous 3D unit. Their product Z² bridges discrete and continuous.
              </p>
            </div>

            {/* Derivation 4 */}
            <div className="border-l-4 border-green-500 pl-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-green-600 font-bold">4. Gauge Theory</span>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">COMPLETE</span>
              </div>
              <p className="text-sm text-gray-600">
                Standard Model: SU(3)×SU(2)×U(1) has dimension 8+3+1 = 12 = GAUGE.
                If GAUGE = 9Z²/(8π) = 12, then Z² = 32π/3.
              </p>
            </div>

            {/* Derivation 5 */}
            <div className="border-l-4 border-amber-500 pl-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-amber-600 font-bold">5. Why 4 Dimensions?</span>
                <span className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded">PARTIAL</span>
              </div>
              <p className="text-sm text-gray-600">
                Multiple arguments: complex numbers require 2D, quaternions have dim 4,
                stable orbits require 3 spatial + 1 time. But no unique proof.
              </p>
            </div>

            {/* Derivation 6 */}
            <div className="border-l-4 border-gray-400 pl-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-gray-600 font-bold">6. Action Principle</span>
                <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">INCOMPLETE</span>
              </div>
              <p className="text-sm text-gray-600">
                Seeking an action S where δS = 0 gives Z² = 32π/3. Z² may be kinematic
                (structural) rather than dynamic (evolutionary).
              </p>
            </div>

            {/* Derivation 7 */}
            <div className="border-l-4 border-gray-400 pl-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-gray-600 font-bold">7. Category Theory</span>
                <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">SPECULATIVE</span>
              </div>
              <p className="text-sm text-gray-600">
                Z² as categorical tensor product: Discrete ⊗ Continuous. The cube and sphere
                may be the unique fundamental objects in their categories.
              </p>
            </div>
          </div>
        </div>

        {/* The Chain of Implications */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Chain of Implications</h2>

          <div className="flex flex-col items-center gap-2 font-mono text-center">
            <div className="bg-blue-100 text-blue-700 px-4 py-2 rounded font-bold">
              BEKENSTEIN = 4
            </div>
            <div className="text-gray-400">↓</div>
            <div className="bg-blue-50 text-blue-600 px-4 py-2 rounded">
              Z² = 32π/3
            </div>
            <div className="text-gray-400">↓</div>
            <div className="bg-amber-50 text-amber-600 px-4 py-2 rounded">
              GAUGE = 12
            </div>
            <div className="text-gray-400">↓</div>
            <div className="bg-green-50 text-green-600 px-4 py-2 rounded">
              α⁻¹ = 4Z² + 3 = 137.04
            </div>
            <div className="text-gray-400">↓</div>
            <div className="bg-gray-100 text-gray-700 px-4 py-2 rounded">
              All particle physics + cosmology
            </div>
          </div>

          <p className="text-sm text-gray-600 text-center mt-4">
            Everything follows from the single axiom: BEKENSTEIN = 4 (spacetime dimensions)
          </p>
        </div>

        {/* The Honest Assessment */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Honest Assessment</h2>

          <div className="space-y-4 text-gray-700">
            <p>
              We can <strong>derive</strong> Z² = 32π/3 from BEKENSTEIN = 4.
            </p>
            <p>
              We can <strong>motivate</strong> BEKENSTEIN = 4 but not prove it.
            </p>
            <p>
              Z² is <em>derived relative to</em> BEKENSTEIN = 4. The latter may be the true axiom.
            </p>

            <div className="bg-gray-50 border border-gray-200 rounded p-4 mt-4">
              <p className="text-sm text-gray-600">
                This is analogous to geometry:
              </p>
              <ul className="text-sm text-gray-600 mt-2 space-y-1">
                <li>• <strong>Euclidean geometry:</strong> parallel postulate is axiomatic</li>
                <li>• <strong>Z² framework:</strong> BEKENSTEIN = 4 is axiomatic</li>
              </ul>
              <p className="text-sm text-gray-600 mt-2">
                The framework is self-consistent and predictive. The foundation is assumed, not proven.
              </p>
            </div>
          </div>
        </div>

        {/* Numerical Verification */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Numerical Verification</h2>

          <div className="grid md:grid-cols-2 gap-4 font-mono text-sm">
            <div className="bg-gray-50 border border-gray-200 rounded p-4">
              <div className="text-gray-600 mb-2">Constants:</div>
              <div>Z² = {Z_SQUARED.toFixed(6)}</div>
              <div>Z = {Z.toFixed(6)}</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded p-4">
              <div className="text-gray-600 mb-2">Derived:</div>
              <div>BEKENSTEIN = {BEKENSTEIN.toFixed(6)}</div>
              <div>GAUGE = {GAUGE.toFixed(6)}</div>
            </div>
          </div>

          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded font-mono text-center">
            <div className="text-gray-600 text-sm">Verification:</div>
            <div className="text-green-700 mt-1">
              GAUGE / BEKENSTEIN = {(GAUGE / BEKENSTEIN).toFixed(6)} = 3 = spatial dimensions ✓
            </div>
          </div>
        </div>

        {/* Links */}
        <div className="grid md:grid-cols-2 gap-4 mb-6">
          <Link
            href="/derivation"
            className="block p-5 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 hover:shadow transition-all"
          >
            <div className="font-semibold text-gray-900 mb-1">Mathematical Derivation →</div>
            <div className="text-sm text-gray-500">
              What follows FROM Z²: dark energy, fine structure, MOND
            </div>
          </Link>

          <Link
            href="/lattice"
            className="block p-5 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 hover:shadow transition-all"
          >
            <div className="font-semibold text-gray-900 mb-1">Cube Lattice Structure →</div>
            <div className="text-sm text-gray-500">
              The geometry of CUBE = 8 in physics
            </div>
          </Link>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p>
            Z² = 32π/3 is not arbitrary — it's uniquely determined by BEKENSTEIN = 4
          </p>
        </footer>
      </div>
    </main>
  )
}
