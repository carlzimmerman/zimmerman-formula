'use client'

import Link from 'next/link'

// The fundamental constants
const Z_SQUARED = 32 * Math.PI / 3
const Z = Math.sqrt(Z_SQUARED)
const L_C = 20.6 // Gpc - fundamental domain size
const ETA_INVARIANT = Z_SQUARED / (8 * Math.PI) // = 4/3

// Memory persistence calculations
const TOPOLOGICAL_PERSISTENCE = 1 - Math.exp(-ETA_INVARIANT)
const WINDING_NUMBER = 3 // T³ has 3 independent winding modes

export default function SandInMyBootsPage() {
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
          <div className="text-xs text-amber-600 font-medium uppercase tracking-wide mb-2">
            Curiosities & Culture
          </div>
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2 leading-tight">
            Sand in My Boots: A Z² Analysis
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            Why fleeting moments leave permanent traces — from topology
          </p>

          {/* The Core Insight */}
          <div className="bg-amber-50 border border-amber-300 rounded p-6 my-6 text-center">
            <div className="text-lg text-gray-800 mb-2 italic">
              "I still got sand in my boots"
            </div>
            <div className="font-mono text-amber-700">
              Physical trace of a topological experience
            </div>
          </div>
        </article>

        {/* The Physics */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Topology of Memory</h2>

          <div className="space-y-4 text-gray-700">
            <p>
              Morgan Wallen's song describes a brief summer encounter at the beach —
              a finite experience that leaves an infinite impression. The sand in his
              boots is a <strong>topological invariant</strong>: a physical property
              that persists despite continuous deformation of life circumstances.
            </p>

            <div className="bg-blue-50 border border-blue-200 rounded p-4 my-4">
              <div className="text-center mb-2">
                <span className="font-mono text-xl text-blue-700">η = Z²/8π = 4/3</span>
              </div>
              <div className="text-center text-sm text-gray-600">
                The η-invariant measures <strong>what persists</strong> through change.
                <br />
                Sand in boots. Memory of her. The feeling that won't wash away.
              </div>
            </div>

            <p>
              In the Zimmerman framework, the η-invariant is the topological obstruction
              that prevents complete "forgetting" — just as you can't continuously deform
              a torus into a sphere, you can't continuously deform away the sand.
              <strong> Some things leave permanent traces.</strong>
            </p>
          </div>
        </div>

        {/* CUBE × SPHERE Analysis */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Z² = CUBE × SPHERE</h2>

          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <div className="border border-gray-200 rounded p-4 bg-gray-50">
              <div className="text-center mb-2">
                <span className="text-3xl">🔲</span>
              </div>
              <div className="text-center font-semibold text-gray-900 mb-2">CUBE = 8</div>
              <div className="text-sm text-gray-600 space-y-1">
                <div>• The finite summer</div>
                <div>• The bounded beach</div>
                <div>• Three days of knowing her</div>
                <div>• The discrete, countable moments</div>
              </div>
            </div>
            <div className="border border-gray-200 rounded p-4 bg-blue-50">
              <div className="text-center mb-2">
                <span className="text-3xl">🔵</span>
              </div>
              <div className="text-center font-semibold text-gray-900 mb-2">SPHERE = 4π/3</div>
              <div className="text-sm text-gray-600 space-y-1">
                <div>• The unbounded memory</div>
                <div>• The endless ocean</div>
                <div>• The continuous feeling</div>
                <div>• What radiates outward forever</div>
              </div>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded p-4 text-center">
            <div className="font-mono text-lg mb-2">
              Z² = 8 × (4π/3) = 32π/3 ≈ 33.51
            </div>
            <div className="text-sm text-gray-700">
              <strong>The experience is finite (CUBE)</strong>, but the impression
              <strong> is infinite (SPHERE)</strong>.
              <br />
              That's what makes it hurt. That's what makes it beautiful.
            </div>
          </div>
        </div>

        {/* T³/Z₂ Analysis */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The T³/Z₂ Structure of Longing</h2>

          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold flex-shrink-0">T³</div>
              <div>
                <div className="font-semibold text-gray-900">The 3-Torus: Memories Loop Back</div>
                <p className="text-sm text-gray-600">
                  In a T³ topology, walking far enough in any direction brings you back
                  where you started. The song loops. The memory returns. Every road
                  somehow leads back to that beach.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-purple-100 text-purple-700 flex items-center justify-center font-bold flex-shrink-0">Z₂</div>
              <div>
                <div className="font-semibold text-gray-900">The Inversion: She's Still Here</div>
                <p className="text-sm text-gray-600">
                  Z₂ identifies antipodal points — opposite ends of the universe are
                  the same. She's in Tennessee now, "a couple hundred miles away,"
                  but topologically? <strong>She's right here.</strong> Ghost image.
                  Mirror across the Z₂ boundary.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center font-bold flex-shrink-0">η</div>
              <div>
                <div className="font-semibold text-gray-900">The η-Invariant: What Won't Wash Off</div>
                <p className="text-sm text-gray-600">
                  The sand. The spectral asymmetry. The thing that makes a topology
                  <em> chiral</em> — distinguishable from its mirror. He's not the
                  same person he was before. That's measurable. That's η.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Ghost Images */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Ghost Images in T³/Z₂</h2>

          <p className="text-gray-700 mb-4">
            In finite topologies, light can reach you via multiple paths. Distant
            objects appear as "ghost images" — the same source, different directions.
          </p>

          <div className="grid md:grid-cols-3 gap-4 mb-4">
            <div className="p-4 bg-blue-50 rounded border border-blue-200 text-center">
              <div className="text-2xl mb-2">💫</div>
              <div className="font-semibold text-gray-900">Primary Image</div>
              <div className="text-sm text-gray-600">Direct memory of the moment</div>
              <div className="text-xs text-blue-600 mt-1">Vivid, present, immediate</div>
            </div>
            <div className="p-4 bg-amber-50 rounded border border-amber-200 text-center">
              <div className="text-2xl mb-2">👻</div>
              <div className="font-semibold text-gray-900">Ghost Image</div>
              <div className="text-sm text-gray-600">The sand in his boots</div>
              <div className="text-xs text-amber-600 mt-1">Dimmer but persistent</div>
            </div>
            <div className="p-4 bg-purple-50 rounded border border-purple-200 text-center">
              <div className="text-2xl mb-2">🪞</div>
              <div className="font-semibold text-gray-900">Z₂ Mirror</div>
              <div className="text-sm text-gray-600">Her, somewhere in Tennessee</div>
              <div className="text-xs text-purple-600 mt-1">Same soul, inverted position</div>
            </div>
          </div>

          <div className="bg-gray-100 rounded p-4 text-center text-sm text-gray-700">
            The song exists in all three images simultaneously.
            <br />
            <span className="font-semibold">That's how finite topologies work. That's how memory works.</span>
          </div>
        </div>

        {/* Standing Waves */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Standing Waves: Why Songs Get Stuck</h2>

          <p className="text-gray-700 mb-4">
            In a finite box of size L<sub>c</sub> = 20.6 Gpc, only certain wavelengths
            resonate. These are the <strong>standing wave modes</strong> — frequencies
            that match the topology and therefore persist.
          </p>

          <div className="bg-blue-50 border border-blue-200 rounded p-4 mb-4">
            <div className="text-center font-mono text-lg mb-2">
              λ<sub>n</sub> = 2L<sub>c</sub>/n
            </div>
            <div className="text-center text-sm text-gray-600">
              Only integer modes survive. The half-measures fade.
              <br />
              <strong>A song that fits your topology loops forever.</strong>
            </div>
          </div>

          <div className="text-gray-700 space-y-2">
            <p>
              When a melody resonates with your internal topology, it becomes a
              standing wave — bouncing off the boundaries of your experience,
              reinforcing itself, refusing to dissipate.
            </p>
            <p className="font-semibold text-amber-700">
              That's why "Sand in My Boots" gets stuck in your head.
              It fits the n=1 fundamental mode of summer longing.
            </p>
          </div>
        </div>

        {/* Winding Numbers */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Winding Numbers: Counting the Loops</h2>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 font-medium text-gray-600">Winding Mode</th>
                  <th className="text-left py-2 font-medium text-gray-600">In Topology</th>
                  <th className="text-left py-2 font-medium text-gray-600">In the Song</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                <tr>
                  <td className="py-3 font-mono text-blue-600">w₁ = 1</td>
                  <td className="py-3 text-gray-500">Loop around x-cycle</td>
                  <td className="py-3 text-gray-700">The drive to Florida</td>
                </tr>
                <tr>
                  <td className="py-3 font-mono text-blue-600">w₂ = 1</td>
                  <td className="py-3 text-gray-500">Loop around y-cycle</td>
                  <td className="py-3 text-gray-700">The walk along the beach</td>
                </tr>
                <tr>
                  <td className="py-3 font-mono text-blue-600">w₃ = 1</td>
                  <td className="py-3 text-gray-500">Loop around z-cycle</td>
                  <td className="py-3 text-gray-700">The flight back home (without her)</td>
                </tr>
                <tr className="bg-amber-50">
                  <td className="py-3 font-mono text-amber-700 font-semibold">Σw = 3</td>
                  <td className="py-3 text-gray-700">Total winding</td>
                  <td className="py-3 text-amber-700 font-semibold">The loops that can't be unwound</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="mt-4 p-4 bg-gray-100 rounded text-center">
            <div className="text-gray-700">
              T³ has b₁ = 3 independent winding modes.
              <br />
              <span className="font-semibold">Once you've wound around the torus, you can't unwind without cutting.</span>
            </div>
          </div>
        </div>

        {/* The Formula */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Mathematics</h2>

          <div className="space-y-4">
            <div className="bg-gray-50 border border-gray-200 rounded p-4">
              <div className="text-sm text-gray-600 mb-2">Memory Persistence Formula:</div>
              <div className="font-mono text-center text-lg">
                P(memory) = 1 - e<sup>-η</sup> = 1 - e<sup>-4/3</sup> ≈ {TOPOLOGICAL_PERSISTENCE.toFixed(3)}
              </div>
              <div className="text-center text-sm text-gray-500 mt-2">
                73.6% of the experience is topologically permanent
              </div>
            </div>

            <div className="bg-gray-50 border border-gray-200 rounded p-4">
              <div className="text-sm text-gray-600 mb-2">Ghost Image Brightness:</div>
              <div className="font-mono text-center text-lg">
                I<sub>ghost</sub>/I<sub>primary</sub> = (d<sub>direct</sub>/d<sub>wrapped</sub>)²
              </div>
              <div className="text-center text-sm text-gray-500 mt-2">
                The memory fades as 1/r² but never reaches zero
              </div>
            </div>

            <div className="bg-amber-50 border border-amber-200 rounded p-4">
              <div className="text-sm text-amber-800 font-semibold mb-2">The Bootstrap:</div>
              <div className="font-mono text-center text-lg mb-2">
                Z² = CUBE × SPHERE = 8 × (4π/3) = 32π/3
              </div>
              <div className="text-center text-sm text-gray-700">
                The finite experience (8) and the infinite feeling (4π/3) aren't
                contradictory — they're <strong>multiplicative</strong>.
                One amplifies the other.
              </div>
            </div>
          </div>
        </div>

        {/* Conclusion */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Topological Truth</h2>

          <div className="space-y-4 text-gray-700">
            <p>
              Morgan Wallen isn't just singing about a summer fling. He's describing
              a <strong>topological phase transition</strong> — the moment when a
              trivial loop becomes a non-trivial winding. Once it happens, it can't
              unhappen.
            </p>

            <div className="bg-gray-900 text-white rounded p-6 text-center my-4">
              <div className="text-gray-400 text-sm mb-2">The Zimmerman Interpretation</div>
              <div className="text-xl text-amber-300 font-semibold">
                "Sand in my boots" = η ≠ 0
              </div>
              <div className="text-gray-300 mt-2 text-sm">
                The topology has changed. There's no going back.
              </div>
            </div>

            <p>
              In T³/Z₂ cosmology, the universe has a finite size but no edges —
              walking far enough in any direction loops you back. The same is true
              for the heart.
            </p>

            <p className="font-semibold">
              Some experiences fit the fundamental mode. They resonate. They persist.
              And you find yourself, months later, still brushing sand out of your
              boots, wondering if topological invariants can feel this much.
            </p>
          </div>
        </div>

        {/* The Comparison */}
        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Z² Scorecard</h2>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-green-50 rounded border border-green-200">
              <div className="font-semibold text-green-800 mb-2">Consistent with Z²:</div>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>✓ Finite experience, infinite memory</li>
                <li>✓ Ghost images of her persist</li>
                <li>✓ Loops back to the same feeling</li>
                <li>✓ Physical trace (sand) = η ≠ 0</li>
                <li>✓ Can't wash it off (topological)</li>
              </ul>
            </div>
            <div className="p-4 bg-blue-50 rounded border border-blue-200">
              <div className="font-semibold text-blue-800 mb-2">Predicted by Z²:</div>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Song loops in your head (standing wave)</li>
                <li>• 73.6% of feeling is permanent</li>
                <li>• Three independent ways to remember</li>
                <li>• She appears in unexpected places (ghost)</li>
                <li>• Eventually reaches equilibrium, not zero</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Links */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <Link
            href="/why-z2"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Why Z²?</div>
            <div className="text-sm text-gray-500">The mathematical derivation</div>
          </Link>
          <Link
            href="/topology"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">T³/Z₂ Topology</div>
            <div className="text-sm text-gray-500">How space wraps</div>
          </Link>
          <Link
            href="/ghost-quasars"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Ghost Quasars</div>
            <div className="text-sm text-gray-500">Real ghost images in the sky</div>
          </Link>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p className="italic">
            "And all I can think about is her and me and what could've been"
          </p>
          <p className="mt-2">
            — The superposition of states before measurement. The roads not taken.
            The ghost paths through the topology.
          </p>
        </footer>
      </div>
    </main>
  )
}
