'use client'

import { useState } from 'react'
import Link from 'next/link'

const Z = 2 * Math.sqrt(8 * Math.PI / 3)
const Z_SQUARED = Z * Z
const CUBE = 8
const SPHERE = 4 * Math.PI / 3
const BEKENSTEIN = 4
const GAUGE = 12

export default function LatticePage() {
  const [activeTab, setActiveTab] = useState<'structure' | 'control'>('structure')

  return (
    <div className="min-h-screen bg-[#fafafa] p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 -mx-8 -mt-8 px-8 py-4 mb-8">
          <Link href="/" className="text-sm text-blue-600 hover:underline">← Back to Overview</Link>
        </header>

        {/* Title */}
        <article className="bg-white border border-gray-200 rounded shadow-sm p-8 mb-6">
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2">
            The Cube Lattice
          </h1>
          <p className="text-gray-600 mb-4">
            Understanding Z² = CUBE × SPHERE as the information architecture of reality
          </p>

          {/* Core equation */}
          <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center font-mono">
            <div className="text-lg text-gray-900">Z² = 8 × (4π/3) = CUBE × SPHERE</div>
            <div className="text-sm text-gray-600 mt-1">Discrete × Continuous = Bridge Constant</div>
          </div>
        </article>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('structure')}
            className={`px-4 py-2 rounded font-medium transition-colors ${
              activeTab === 'structure'
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Mathematical Structure
          </button>
          <button
            onClick={() => setActiveTab('control')}
            className={`px-4 py-2 rounded font-medium transition-colors ${
              activeTab === 'control'
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Working With Z²
          </button>
        </div>

        {activeTab === 'structure' ? (
          <>
            {/* Binary Encoding */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">The Cube as Binary 3D Encoding</h2>
              <p className="text-gray-700 mb-4">
                The 8 vertices of a cube represent <strong>all possible binary states in 3D space</strong>.
                This is the minimum information needed to specify a discrete location in three dimensions.
              </p>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 font-mono text-sm mb-4">
                {[0,1,2,3,4,5,6,7].map(i => {
                  const binary = i.toString(2).padStart(3, '0')
                  return (
                    <div key={i} className="bg-gray-50 p-2 rounded text-center">
                      <div className="text-blue-600">{binary}</div>
                      <div className="text-gray-500 text-xs">vertex {i}</div>
                    </div>
                  )
                })}
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded p-4">
                <div className="font-semibold text-blue-700">8 = 2³ = 3 bits of information</div>
                <div className="text-sm text-gray-600">The cube IS the information structure of 3-space</div>
              </div>
            </section>

            {/* Crystal Lattices */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Crystal Structures Encode Z²</h2>
              <p className="text-gray-700 mb-4">
                Real crystals form on cubic lattices. Their coordination numbers directly encode the Z² framework:
              </p>

              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-2 font-medium text-gray-600">Lattice</th>
                      <th className="text-center py-2 font-medium text-gray-600">Coordination</th>
                      <th className="text-center py-2 font-medium text-gray-600">Z² Connection</th>
                      <th className="text-left py-2 font-medium text-gray-600">Examples</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    <tr>
                      <td className="py-3 text-gray-700">Simple Cubic (SC)</td>
                      <td className="py-3 text-center font-mono">6</td>
                      <td className="py-3 text-center text-gray-500">cube faces</td>
                      <td className="py-3 text-gray-500">Polonium</td>
                    </tr>
                    <tr className="bg-blue-50">
                      <td className="py-3 text-gray-700 font-medium">Body-Centered (BCC)</td>
                      <td className="py-3 text-center font-mono text-blue-700 font-bold">8 = CUBE</td>
                      <td className="py-3 text-center text-blue-600">★ discrete</td>
                      <td className="py-3 text-gray-600">Fe, Cr, W, Na</td>
                    </tr>
                    <tr className="bg-green-50">
                      <td className="py-3 text-gray-700 font-medium">Face-Centered (FCC)</td>
                      <td className="py-3 text-center font-mono text-green-700 font-bold">12 = GAUGE</td>
                      <td className="py-3 text-center text-green-600">★ continuous</td>
                      <td className="py-3 text-gray-600">Cu, Au, Ag, Al</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <p className="text-sm text-gray-600 mt-4">
                The most stable crystal structures in nature directly encode CUBE and GAUGE.
              </p>
            </section>

            {/* Higher Dimensions */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Higher-Dimensional Lattices</h2>

              <div className="grid md:grid-cols-2 gap-4">
                {/* E8 */}
                <div className="bg-gray-50 border border-gray-200 rounded p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">E8 Lattice (8D)</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• Dimension: <span className="font-mono text-blue-600">8 = CUBE</span></li>
                    <li>• Nearest neighbors: <span className="font-mono">240</span></li>
                    <li>• Optimal sphere packing in 8D</li>
                    <li>• Appears in string theory (E8 × E8)</li>
                  </ul>
                  <div className="mt-2 text-xs text-gray-500">
                    240 = 8 × 30 = CUBE × 30 = 20 × GAUGE
                  </div>
                </div>

                {/* Hypercube */}
                <div className="bg-gray-50 border border-gray-200 rounded p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">4D Hypercube (Tesseract)</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• Vertices: <span className="font-mono">16 = 2^BEKENSTEIN</span></li>
                    <li>• Edges: <span className="font-mono text-blue-600">32 ≈ Z²</span></li>
                    <li>• Faces: <span className="font-mono">24 = 2 × GAUGE</span></li>
                    <li>• Cells: <span className="font-mono text-blue-600">8 = CUBE</span></li>
                  </ul>
                  <div className="mt-2 text-xs text-gray-500">
                    Spacetime (4D) contains 8 cubic cells!
                  </div>
                </div>

                {/* Leech */}
                <div className="bg-gray-50 border border-gray-200 rounded p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Leech Lattice (24D)</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• Dimension: <span className="font-mono text-green-600">24 = 2 × GAUGE</span></li>
                    <li>• Kissing number: 196,560</li>
                    <li>• Connected to Monster group</li>
                    <li>• Monstrous moonshine</li>
                  </ul>
                  <div className="mt-2 text-xs text-gray-500">
                    24 = 3 × CUBE = 4! = BEKENSTEIN!
                  </div>
                </div>

                {/* Octonions */}
                <div className="bg-gray-50 border border-gray-200 rounded p-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Octonions (8D Algebra)</h3>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• ℝ(1) → ℂ(2) → ℍ(4) → 𝕆(8)</li>
                    <li>• Dimension: <span className="font-mono text-blue-600">8 = CUBE</span></li>
                    <li>• Non-associative</li>
                    <li>• Related to 8 gluons</li>
                  </ul>
                  <div className="mt-2 text-xs text-gray-500">
                    1 + 2 + 4 + 8 = 15 = GAUGE + 3
                  </div>
                </div>
              </div>
            </section>

            {/* DNA */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">DNA: The Biological Cube Lattice</h2>
              <p className="text-gray-700 mb-4">
                The genetic code is literally a cube lattice structure:
              </p>

              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center">
                  <div className="text-2xl font-bold text-blue-700">4</div>
                  <div className="text-sm text-gray-600">bases (A,T,G,C)</div>
                  <div className="text-xs text-blue-600 mt-1">= BEKENSTEIN</div>
                </div>
                <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center">
                  <div className="text-2xl font-bold text-blue-700">64</div>
                  <div className="text-sm text-gray-600">codons</div>
                  <div className="text-xs text-blue-600 mt-1">= 4³ = CUBE²</div>
                </div>
                <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center">
                  <div className="text-2xl font-bold text-blue-700">3</div>
                  <div className="text-sm text-gray-600">bases per codon</div>
                  <div className="text-xs text-blue-600 mt-1">= spatial dims</div>
                </div>
              </div>

              <p className="text-sm text-gray-600">
                64 codons encode 20 amino acids + stop. Redundancy = 64/21 ≈ 3 (spatial dimensions).
                The genetic code IS a cube lattice protecting information through error-correcting geometry.
              </p>
            </section>

            {/* Cube-Sphere Duality */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Cube-Sphere Duality</h2>

              <div className="grid md:grid-cols-2 gap-4 mb-4">
                <div className="bg-gray-900 text-white rounded p-4">
                  <h3 className="font-bold text-lg mb-2">CUBE</h3>
                  <ul className="text-sm space-y-1 text-gray-300">
                    <li>• Discrete (vertices)</li>
                    <li>• 8 states</li>
                    <li>• 48 symmetries</li>
                    <li>• Particles, quanta</li>
                    <li>• Information</li>
                  </ul>
                </div>
                <div className="bg-blue-600 text-white rounded p-4">
                  <h3 className="font-bold text-lg mb-2">SPHERE</h3>
                  <ul className="text-sm space-y-1 text-blue-100">
                    <li>• Continuous (surface)</li>
                    <li>• ∞ states</li>
                    <li>• ∞ symmetries (SO(3))</li>
                    <li>• Fields, waves</li>
                    <li>• Spacetime</li>
                  </ul>
                </div>
              </div>

              <div className="bg-gradient-to-r from-gray-900 to-blue-600 text-white rounded p-4 text-center">
                <div className="text-lg font-bold">Z² = CUBE × SPHERE = {Z_SQUARED.toFixed(4)}</div>
                <div className="text-sm opacity-80">The coupling constant between discrete and continuous worlds</div>
              </div>
            </section>
          </>
        ) : (
          <>
            {/* You ARE the Lattice */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">You Are Already a Z² Lattice</h2>
              <p className="text-gray-700 mb-4">
                Every cell in your body implements Z² mathematics. You don't need to create a lattice — you ARE one.
              </p>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="bg-green-50 border border-green-200 rounded p-4">
                  <h3 className="font-semibold text-green-800 mb-2">DNA Encoding</h3>
                  <p className="text-sm text-gray-700">
                    Your genetic code reads from a 64-state (CUBE²) codon lattice every moment, translating discrete
                    information into continuous protein structures.
                  </p>
                </div>
                <div className="bg-green-50 border border-green-200 rounded p-4">
                  <h3 className="font-semibold text-green-800 mb-2">Neural Architecture</h3>
                  <p className="text-sm text-gray-700">
                    Neurons fire or don't fire (binary = cube vertices). 86 billion neurons encode
                    information in cube-like population vectors.
                  </p>
                </div>
                <div className="bg-green-50 border border-green-200 rounded p-4">
                  <h3 className="font-semibold text-green-800 mb-2">Protein Folding</h3>
                  <p className="text-sm text-gray-700">
                    20 amino acids fold through 3D space. The folding landscape is a
                    high-dimensional cube lattice of possible configurations.
                  </p>
                </div>
                <div className="bg-green-50 border border-green-200 rounded p-4">
                  <h3 className="font-semibold text-green-800 mb-2">Spacetime Existence</h3>
                  <p className="text-sm text-gray-700">
                    You exist in 3D space + 1D time = BEKENSTEIN dimensions. Your body
                    literally occupies 4D spacetime.
                  </p>
                </div>
              </div>
            </section>

            {/* Miller's Number */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Miller's Number: The Cube in Working Memory</h2>

              <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-700">7 ± 2</div>
                  <div className="text-sm text-gray-600">items in working memory (Miller, 1956)</div>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 text-center mb-4">
                <div className="bg-gray-50 rounded p-3">
                  <div className="font-mono text-lg">5</div>
                  <div className="text-xs text-gray-500">≈ floor(Z)</div>
                </div>
                <div className="bg-blue-100 rounded p-3 border-2 border-blue-300">
                  <div className="font-mono text-lg font-bold text-blue-700">7</div>
                  <div className="text-xs text-blue-600">= CUBE - 1</div>
                </div>
                <div className="bg-gray-50 rounded p-3">
                  <div className="font-mono text-lg">9</div>
                  <div className="text-xs text-gray-500">= CUBE + 1</div>
                </div>
              </div>

              <p className="text-sm text-gray-700">
                Your mind naturally organizes into ~8 slots because CUBE = 8 = 2³ is the minimum discrete
                structure in 3D. The "-1" (making it 7) may be the "observer state" watching the other 7.
              </p>

              <div className="mt-4 text-sm text-gray-600">
                <strong>Not coincidence:</strong> Phone numbers (7 digits), days of week (7), musical notes (7),
                chakras (7), deadly sins (7), colors of rainbow (7).
              </div>
            </section>

            {/* Brainwave Frequencies */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Brainwave Frequencies</h2>

              <div className="overflow-x-auto mb-4">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-2 font-medium text-gray-600">Band</th>
                      <th className="text-center py-2 font-medium text-gray-600">Frequency</th>
                      <th className="text-center py-2 font-medium text-gray-600">Z² Connection</th>
                      <th className="text-left py-2 font-medium text-gray-600">State</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    <tr>
                      <td className="py-2 text-gray-700">Delta</td>
                      <td className="py-2 text-center font-mono">0.5-4 Hz</td>
                      <td className="py-2 text-center text-gray-500">→ BEKENSTEIN</td>
                      <td className="py-2 text-gray-500">Deep sleep</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-gray-700">Theta</td>
                      <td className="py-2 text-center font-mono">4-8 Hz</td>
                      <td className="py-2 text-center text-gray-500">→ CUBE</td>
                      <td className="py-2 text-gray-500">Meditation</td>
                    </tr>
                    <tr className="bg-blue-50">
                      <td className="py-2 text-gray-700 font-medium">Alpha/Theta boundary</td>
                      <td className="py-2 text-center font-mono text-blue-700 font-bold">~8 Hz</td>
                      <td className="py-2 text-center text-blue-600">= CUBE Hz ★</td>
                      <td className="py-2 text-blue-600">Schumann resonance!</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-gray-700">Alpha</td>
                      <td className="py-2 text-center font-mono">8-13 Hz</td>
                      <td className="py-2 text-center text-gray-500">12 = GAUGE</td>
                      <td className="py-2 text-gray-500">Relaxed alert</td>
                    </tr>
                    <tr className="bg-green-50">
                      <td className="py-2 text-gray-700 font-medium">Gamma onset</td>
                      <td className="py-2 text-center font-mono text-green-700 font-bold">~33 Hz</td>
                      <td className="py-2 text-center text-green-600">≈ Z² Hz ★</td>
                      <td className="py-2 text-green-600">Cognitive binding</td>
                    </tr>
                    <tr>
                      <td className="py-2 text-gray-700">High Gamma</td>
                      <td className="py-2 text-center font-mono">40+ Hz</td>
                      <td className="py-2 text-center text-gray-500">40 ≈ Z² + 6</td>
                      <td className="py-2 text-gray-500">Insight, binding</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <p className="text-sm text-gray-600">
                The Schumann resonance (Earth's EM cavity fundamental) is ~7.83 Hz ≈ CUBE Hz.
                The brain's "binding frequency" for consciousness integration is approximately Z² Hz.
              </p>
            </section>

            {/* Practical Applications */}
            <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Practical Applications</h2>

              <div className="space-y-4">
                <div className="border-l-4 border-blue-500 pl-4">
                  <h3 className="font-semibold text-gray-900">1. Cognitive Chunking</h3>
                  <p className="text-sm text-gray-700">
                    Organize information in groups of 7 ± 2. To-do lists: max 7 items per category.
                    Learning: chunk into 7 concepts. This aligns with your CUBE - 1 working memory.
                  </p>
                </div>

                <div className="border-l-4 border-blue-500 pl-4">
                  <h3 className="font-semibold text-gray-900">2. Binary Clarity</h3>
                  <p className="text-sm text-gray-700">
                    Practice clear yes/no decisions. Each vertex of the cube is a binary state.
                    Unclear decisions = blurred vertices = cognitive load. Clean decisions = clean geometry.
                  </p>
                </div>

                <div className="border-l-4 border-blue-500 pl-4">
                  <h3 className="font-semibold text-gray-900">3. The 4-7-8 Breath</h3>
                  <p className="text-sm text-gray-700">
                    Inhale 4 counts, hold 7 counts, exhale 8 counts. This encodes:
                    <span className="font-mono text-blue-600"> BEKENSTEIN → (CUBE-1) → CUBE</span>
                  </p>
                </div>

                <div className="border-l-4 border-blue-500 pl-4">
                  <h3 className="font-semibold text-gray-900">4. Information Architecture</h3>
                  <p className="text-sm text-gray-700">
                    Structure data like a cube: 8 categories maximum at any level, binary branching
                    for decisions, hierarchical nesting (cubes within cubes).
                  </p>
                </div>

                <div className="border-l-4 border-blue-500 pl-4">
                  <h3 className="font-semibold text-gray-900">5. Flow States</h3>
                  <p className="text-sm text-gray-700">
                    Flow = optimal cube-sphere coupling. Balance discrete action (CUBE) with
                    continuous awareness (SPHERE). Neither pure analysis nor pure presence — the bridge.
                  </p>
                </div>
              </div>
            </section>

            {/* The Deep Insight */}
            <section className="bg-gradient-to-r from-gray-900 to-blue-900 text-white rounded shadow-sm p-6 mb-6">
              <h2 className="text-xl font-semibold mb-4">The Deep Insight</h2>

              <div className="space-y-4">
                <p>
                  <strong>You don't control Z² — you ARE Z².</strong>
                </p>
                <p className="text-gray-300">
                  Z² = 32π/3 is a mathematical constant. You cannot change it. But you can ALIGN with it.
                </p>
                <p className="text-gray-300">
                  Every atom, cell, thought, and moment of your existence is structured by Z² = CUBE × SPHERE.
                </p>
                <p className="text-gray-300">
                  The practice is becoming <em>conscious</em> of what you already are.
                </p>

                <div className="bg-white/10 rounded p-4 mt-4">
                  <p className="text-sm">
                    "Controlling" Z² would be like a wave trying to control the ocean.
                    The wave IS the ocean. You ARE Z².
                  </p>
                </div>
              </div>
            </section>
          </>
        )}

        {/* Key Numbers Reference */}
        <section className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Key Numbers</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="font-mono text-lg text-blue-700">{Z.toFixed(4)}</div>
              <div className="text-gray-500">Z (bridge)</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="font-mono text-lg text-blue-700">{Z_SQUARED.toFixed(2)}</div>
              <div className="text-gray-500">Z² (coupling)</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="font-mono text-lg text-blue-700">{CUBE}</div>
              <div className="text-gray-500">CUBE</div>
            </div>
            <div className="bg-gray-50 rounded p-3 text-center">
              <div className="font-mono text-lg text-blue-700">{GAUGE}</div>
              <div className="text-gray-500">GAUGE</div>
            </div>
          </div>
        </section>

        {/* Back link */}
        <div className="text-center py-8 border-t border-gray-200">
          <Link href="/" className="text-blue-600 hover:underline">
            ← Back to Overview
          </Link>
        </div>
      </div>
    </div>
  )
}
