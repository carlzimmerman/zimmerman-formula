'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, Formula, KeyPoint, Z2Connection, InteractiveBox } from '@/components/DocumentLayout'

// Topological Equivalence Visualization
function TopologyEquivalenceViz() {
  const shapes = [
    { name: 'Sphere', holes: 0, emoji: '🔵', examples: 'Ball, egg, cube' },
    { name: 'Torus', holes: 1, emoji: '🍩', examples: 'Donut, coffee cup' },
    { name: 'Double Torus', holes: 2, emoji: '8️⃣', examples: 'Figure-8, pretzel' },
  ]

  const [selected, setSelected] = useState(1)

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-4">
        {shapes.map((shape, i) => (
          <button
            key={i}
            onClick={() => setSelected(i)}
            className={`p-4 rounded-lg border-2 transition-all ${
              selected === i
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="text-4xl mb-2">{shape.emoji}</div>
            <div className="font-medium text-sm">{shape.name}</div>
          </button>
        ))}
      </div>

      <div className="bg-gray-50 p-4 rounded-lg text-center">
        <div className="text-lg font-medium">{shapes[selected].name}</div>
        <div className="text-3xl font-bold text-purple-600 my-2">
          {shapes[selected].holes} hole{shapes[selected].holes !== 1 ? 's' : ''}
        </div>
        <div className="text-sm text-gray-600">
          Topologically equivalent to: {shapes[selected].examples}
        </div>
      </div>

      <div className="bg-amber-50 p-3 rounded border border-amber-200 text-sm text-center">
        <strong>The famous joke:</strong> A topologist can't tell the difference between a coffee mug and a donut!
        <br />
        Both have exactly one hole (the handle / the hole).
      </div>
    </div>
  )
}

// Torus Visualization
function TorusViz() {
  const [showCycles, setShowCycles] = useState({ alpha: true, beta: true })

  return (
    <div className="space-y-4">
      <svg viewBox="0 0 300 200" className="w-full max-w-md mx-auto">
        {/* Torus body */}
        <ellipse cx="150" cy="100" rx="120" ry="60" fill="none" stroke="#9CA3AF" strokeWidth="3" />
        <ellipse cx="150" cy="100" rx="40" ry="20" fill="#fafafa" stroke="#9CA3AF" strokeWidth="3" />

        {/* Alpha cycle */}
        {showCycles.alpha && (
          <g>
            <ellipse
              cx="150"
              cy="100"
              rx="80"
              ry="40"
              fill="none"
              stroke="#3B82F6"
              strokeWidth="4"
              strokeDasharray="10,5"
            />
            <circle cx="230" cy="100" r="8" fill="#3B82F6" />
            <text x="250" y="105" className="text-lg fill-blue-600 font-bold">α</text>
          </g>
        )}

        {/* Beta cycle */}
        {showCycles.beta && (
          <g>
            <path
              d="M 150 40 Q 210 100 150 160 Q 90 100 150 40"
              fill="none"
              stroke="#EF4444"
              strokeWidth="4"
              strokeDasharray="10,5"
            />
            <circle cx="150" cy="40" r="8" fill="#EF4444" />
            <text x="165" y="35" className="text-lg fill-red-600 font-bold">β</text>
          </g>
        )}
      </svg>

      <div className="flex justify-center gap-6">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showCycles.alpha}
            onChange={(e) => setShowCycles({ ...showCycles, alpha: e.target.checked })}
            className="w-5 h-5 text-blue-600 rounded"
          />
          <span className="text-blue-600 font-medium">α cycle (around hole)</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showCycles.beta}
            onChange={(e) => setShowCycles({ ...showCycles, beta: e.target.checked })}
            className="w-5 h-5 text-red-600 rounded"
          />
          <span className="text-red-600 font-medium">β cycle (around tube)</span>
        </label>
      </div>

      <div className="grid grid-cols-2 gap-4 text-center">
        <div className="bg-blue-50 p-3 rounded border border-blue-200">
          <div className="text-sm text-blue-600">First Betti number</div>
          <div className="text-2xl font-bold text-blue-700">b₁(T²) = 2</div>
          <div className="text-xs text-gray-500">Two independent loops</div>
        </div>
        <div className="bg-purple-50 p-3 rounded border border-purple-200">
          <div className="text-sm text-purple-600">For T³ = T² × S¹</div>
          <div className="text-2xl font-bold text-purple-700">b₁(T³) = 3</div>
          <div className="text-xs text-gray-500">Three generations!</div>
        </div>
      </div>
    </div>
  )
}

// Compactness Visualization
function CompactnessViz() {
  const [showEscape, setShowEscape] = useState(false)

  return (
    <div className="space-y-4">
      <div className="flex justify-center gap-8">
        {/* Compact: Circle */}
        <div className="text-center">
          <svg viewBox="-1.5 -1.5 3 3" className="w-32 h-32 mx-auto">
            <circle cx="0" cy="0" r="1" fill="#DBEAFE" stroke="#3B82F6" strokeWidth="0.1" />
            {/* Points that can't escape */}
            {[0, 60, 120, 180, 240, 300].map((angle, i) => (
              <circle
                key={i}
                cx={0.6 * Math.cos((angle * Math.PI) / 180)}
                cy={0.6 * Math.sin((angle * Math.PI) / 180)}
                r="0.1"
                fill="#3B82F6"
              />
            ))}
          </svg>
          <div className="font-medium text-blue-700 mt-2">Compact (S¹)</div>
          <div className="text-xs text-gray-500">Bounded, no escape!</div>
        </div>

        {/* Non-compact: Line */}
        <div className="text-center">
          <svg viewBox="-2 -1 4 2" className="w-32 h-32 mx-auto">
            <line x1="-1.8" y1="0" x2="1.8" y2="0" stroke="#EF4444" strokeWidth="0.1" />
            <text x="-1.9" y="0.3" fontSize="0.4" fill="#EF4444">...</text>
            <text x="1.5" y="0.3" fontSize="0.4" fill="#EF4444">...</text>
            {/* Point escaping */}
            <circle
              cx={showEscape ? 1.5 : 0}
              cy="0"
              r="0.12"
              fill="#EF4444"
              className="transition-all duration-1000"
            />
          </svg>
          <div className="font-medium text-red-700 mt-2">Non-compact (ℝ)</div>
          <div className="text-xs text-gray-500">Extends to infinity</div>
        </div>
      </div>

      <button
        onClick={() => setShowEscape(!showEscape)}
        className="mx-auto block px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg text-sm"
      >
        {showEscape ? 'Reset' : 'Watch point escape →'}
      </button>

      <div className="bg-green-50 p-3 rounded border border-green-200 text-sm">
        <strong>Key insight:</strong> T³ is compact (it wraps around), so physics on T³ has
        discrete energy levels — this is why we get specific numbers like 3 generations!
      </div>
    </div>
  )
}

export default function TopologyPage() {
  return (
    <DocumentLayout
      title="Topology Basics"
      description="The study of shape, continuity, and what doesn't change under deformation"
      phase="math"
      currentIndex={3}
      prevLink={{ href: '/office-hours/math/02-group-theory', title: 'Group Theory' }}
      nextLink={{ href: '/office-hours/math/04-differential-geometry', title: 'Differential Geometry' }}
    >
      <Section title="1. What is Topology?">
        <p className="text-gray-700 mb-4">
          Topology studies properties that don't change under continuous deformation —
          stretching, bending, twisting, but <strong>not</strong> cutting or gluing.
        </p>

        <InteractiveBox title="Topological Equivalence">
          <TopologyEquivalenceViz />
        </InteractiveBox>

        <KeyPoint>
          <strong>Topology counts holes!</strong> The number of holes is a topological invariant —
          it doesn't change under continuous deformation.
        </KeyPoint>
      </Section>

      <Section title="2. Manifolds">
        <p className="text-gray-700 mb-4">
          A <strong>manifold</strong> is a space that looks locally like ℝⁿ (flat space).
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 my-4">
          <div className="bg-gray-50 p-3 rounded text-center">
            <div className="text-2xl mb-1">○</div>
            <div className="font-medium">Circle S¹</div>
            <div className="text-sm text-gray-500">1D manifold</div>
          </div>
          <div className="bg-gray-50 p-3 rounded text-center">
            <div className="text-2xl mb-1">🌍</div>
            <div className="font-medium">Sphere S²</div>
            <div className="text-sm text-gray-500">2D manifold</div>
          </div>
          <div className="bg-purple-50 p-3 rounded text-center border border-purple-200">
            <div className="text-2xl mb-1">🍩</div>
            <div className="font-medium">Torus T²</div>
            <div className="text-sm text-purple-600">S¹ × S¹</div>
          </div>
        </div>

        <Formula label="The 3-torus">
          T³ = S¹ × S¹ × S¹
        </Formula>

        <p className="text-gray-700 mt-4">
          T³ is a 3D manifold that wraps around in all three directions — like a
          3D video game where exiting one side puts you on the opposite side.
        </p>
      </Section>

      <Section title="3. The Torus and Its Cycles">
        <InteractiveBox title="Torus T² with Homology Cycles">
          <TorusViz />
        </InteractiveBox>

        <SubSection title="Why Cycles Matter">
          <p className="text-gray-700 mb-4">
            The α and β cycles represent the two "independent ways to go around" the torus.
            They can't be shrunk to a point — they're topologically protected!
          </p>
        </SubSection>

        <Z2Connection
          formula="b₁(T³) = 3"
          description="Three independent cycles on T³ → three generations of particles"
        />
      </Section>

      <Section title="4. Compactness">
        <p className="text-gray-700 mb-4">
          A space is <strong>compact</strong> if it's "finite" in a topological sense —
          roughly, you can't escape to infinity.
        </p>

        <InteractiveBox title="Compact vs Non-Compact">
          <CompactnessViz />
        </InteractiveBox>

        <SubSection title="Examples">
          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-200 p-2">Space</th>
                  <th className="border border-gray-200 p-2">Compact?</th>
                  <th className="border border-gray-200 p-2">Why?</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="border border-gray-200 p-2">[0, 1] (closed interval)</td>
                  <td className="border border-gray-200 p-2 text-green-600">✓ Yes</td>
                  <td className="border border-gray-200 p-2">Bounded and closed</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">(0, 1) (open interval)</td>
                  <td className="border border-gray-200 p-2 text-red-600">✗ No</td>
                  <td className="border border-gray-200 p-2">Missing endpoints</td>
                </tr>
                <tr>
                  <td className="border border-gray-200 p-2">ℝ (real line)</td>
                  <td className="border border-gray-200 p-2 text-red-600">✗ No</td>
                  <td className="border border-gray-200 p-2">Unbounded</td>
                </tr>
                <tr className="bg-purple-50">
                  <td className="border border-gray-200 p-2">T³ (3-torus)</td>
                  <td className="border border-gray-200 p-2 text-green-600">✓ Yes</td>
                  <td className="border border-gray-200 p-2">Wraps around</td>
                </tr>
              </tbody>
            </table>
          </div>
        </SubSection>
      </Section>

      <Section title="5. Euler Characteristic">
        <p className="text-gray-700 mb-4">
          The <strong>Euler characteristic</strong> χ is a topological invariant computed from vertices, edges, and faces:
        </p>

        <Formula>χ = V - E + F</Formula>

        <div className="grid grid-cols-3 gap-3 my-4 text-center">
          <div className="bg-gray-50 p-3 rounded">
            <div className="font-medium">Sphere</div>
            <div className="text-2xl font-bold text-blue-600">χ = 2</div>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <div className="font-medium">Torus</div>
            <div className="text-2xl font-bold text-purple-600">χ = 0</div>
          </div>
          <div className="bg-gray-50 p-3 rounded">
            <div className="font-medium">Double Torus</div>
            <div className="text-2xl font-bold text-orange-600">χ = -2</div>
          </div>
        </div>

        <KeyPoint>
          <strong>χ = 2 - 2g</strong> where g is the number of holes (genus).
          The Euler characteristic encodes the topology!
        </KeyPoint>
      </Section>

      <Section title="6. Connection to Z² Framework">
        <div className="space-y-3">
          <Z2Connection
            formula="T³/Z₂"
            description="Compactify on the orbifold T³/Z₂ to get the Standard Model"
          />
          <Z2Connection
            formula="b₁(T³) = 3"
            description="Three independent cycles = three generations"
          />
          <Z2Connection
            formula="8 fixed points"
            description="Z₂ action creates 8 fixed points on T³, giving twisted sector modes"
          />
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg mt-6">
          <h4 className="font-semibold text-gray-900 mb-2">Why Topology Matters</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• <strong>Compactness</strong> gives discrete spectra (particle masses)</li>
            <li>• <strong>Topology</strong> determines particle generations via Betti numbers</li>
            <li>• <strong>Orbifold singularities</strong> create gauge group structure</li>
            <li>• <strong>Euler characteristic</strong> appears in index theorems</li>
          </ul>
        </div>
      </Section>

      <Section title="Exercises">
        <ol className="list-decimal list-inside space-y-3 text-gray-700">
          <li>Why is a coffee mug topologically equivalent to a donut but not to a bowl?</li>
          <li>Calculate χ for a cube: V = 8, E = 12, F = 6. What surface is it equivalent to?</li>
          <li>T³ = S¹ × S¹ × S¹. How many independent 1-cycles does it have?</li>
          <li>Is a cylinder (without end caps) compact? Why or why not?</li>
          <li>What is the Euler characteristic of a Möbius strip?</li>
        </ol>
      </Section>
    </DocumentLayout>
  )
}
