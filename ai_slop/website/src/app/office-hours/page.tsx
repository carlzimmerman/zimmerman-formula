'use client'

import Link from 'next/link'
import { useState } from 'react'

const mathDocs = [
  { id: '00-prerequisites', title: 'Prerequisites', desc: 'Algebra, calculus, complex numbers, Euler\'s formula', time: '1-2 hrs' },
  { id: '01-linear-algebra', title: 'Linear Algebra', desc: 'Vectors, matrices, eigenvalues, trace', time: '2-3 hrs' },
  { id: '02-group-theory', title: 'Group Theory', desc: 'Lie groups, SU(2), SU(3), U(1), Z₂ symmetry', time: '3-4 hrs' },
  { id: '03-topology', title: 'Topology Basics', desc: 'Manifolds, compactness, continuity', time: '2-3 hrs' },
  { id: '04-differential-geometry', title: 'Differential Geometry', desc: 'Metrics, curvature, geodesics', time: '3-4 hrs' },
  { id: '05-algebraic-topology', title: 'Algebraic Topology', desc: 'Homology, Betti numbers (b₁ = 3)', time: '3-4 hrs' },
  { id: '06-orbifolds', title: 'Orbifolds', desc: 'T³/Z₂ geometry, 8 fixed points', time: '2-3 hrs' },
  { id: '07-index-theory', title: 'Index Theory', desc: 'APS theorem, eta invariant', time: '3-4 hrs' },
  { id: '08-intersection-theory', title: 'Intersection Theory', desc: 'D-brane intersections, I_ab = 3', time: '2-3 hrs' },
]

const physicsDocs = [
  { id: '00-classical-mechanics', title: 'Classical Mechanics', desc: 'Lagrangian, Hamiltonian, Noether\'s theorem', time: '2-3 hrs' },
  { id: '01-special-relativity', title: 'Special Relativity', desc: 'Lorentz transformations, GPS proof', time: '2-3 hrs' },
  { id: '02-quantum-mechanics', title: 'Quantum Mechanics', desc: 'Wave functions, spin, uncertainty', time: '3-4 hrs' },
  { id: '03-quantum-field-theory', title: 'Quantum Field Theory', desc: 'Feynman diagrams, propagators, vacuum', time: '4-5 hrs' },
  { id: '04-gauge-theory', title: 'Gauge Theory', desc: 'Standard Model gauge structure', time: '3-4 hrs' },
  { id: '05-general-relativity', title: 'General Relativity', desc: 'Einstein equations, curved spacetime', time: '3-4 hrs' },
  { id: '06-adm-formalism', title: 'ADM Formalism', desc: '3+1 decomposition, Hamiltonian gravity', time: '2-3 hrs' },
  { id: '07-cosmology', title: 'Cosmology', desc: 'Ω_Λ = 13/19, dark energy', time: '2-3 hrs' },
  { id: '08-string-theory', title: 'String Theory', desc: 'Strings, D-branes, compactification', time: '3-4 hrs' },
  { id: '09-holography', title: 'Holography', desc: 'AdS/CFT, IR fixed points', time: '3-4 hrs' },
]

const keyConnections = [
  { formula: 'Z² = 32π/3', topic: 'Orbifolds', desc: 'Singularity resolution on T³/Z₂' },
  { formula: 'α⁻¹ = 4Z² + 3', topic: 'Index Theory', desc: 'APS eta invariant + rank(G)' },
  { formula: 'sin²θ_W = 3/13', topic: 'Intersection Theory', desc: 'D-brane intersection number' },
  { formula: 'Ω_Λ = 13/19', topic: 'Holography', desc: 'Degrees of freedom counting' },
  { formula: '3 generations', topic: 'Algebraic Topology', desc: 'b₁(T³) = 3 Betti number' },
]

export default function OfficeHours() {
  const [expandedMath, setExpandedMath] = useState(true)
  const [expandedPhysics, setExpandedPhysics] = useState(true)

  return (
    <main className="min-h-screen bg-[#fafafa]">
      <div className="max-w-4xl mx-auto px-4 py-6 md:py-8">
        {/* Header */}
        <div className="mb-6">
          <Link href="/" className="text-blue-600 hover:underline text-sm mb-2 inline-block">
            ← Back to Framework
          </Link>
          <h1 className="text-2xl md:text-3xl font-semibold text-gray-900 mb-2">
            Office Hours with Claude
          </h1>
          <p className="text-gray-600">
            Learn the mathematical and physics foundations of the Z² Framework
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <Link
            href="/office-hours/visualizations"
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg p-4 hover:from-purple-700 hover:to-blue-700 transition-all"
          >
            <h2 className="text-lg font-semibold mb-1">🎮 Interactive Visualizations</h2>
            <p className="text-purple-100 text-sm">
              Explore Z₂ groups, torus topology, wave functions & more
            </p>
          </Link>
          <Link
            href="/office-hours/notation"
            className="bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-lg p-4 hover:from-orange-600 hover:to-red-600 transition-all"
          >
            <h2 className="text-lg font-semibold mb-1">📖 Notation Reference</h2>
            <p className="text-orange-100 text-sm">
              All symbols used in the v8.8.8 paper with searchable index
            </p>
          </Link>
        </div>

        {/* Learning Philosophy */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 md:p-6 mb-6">
          <h2 className="text-lg font-semibold text-blue-900 mb-2">📚 How to Learn</h2>
          <ul className="text-blue-800 text-sm space-y-1">
            <li>• Complete <strong>Math</strong> first, then <strong>Physics</strong></li>
            <li>• Each topic builds on the previous</li>
            <li>• Work through examples with pen and paper</li>
            <li>• Every topic shows its Z² framework connection</li>
          </ul>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          <div className="bg-white border border-gray-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-blue-600">20</div>
            <div className="text-xs text-gray-500">Documents</div>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-green-600">~50</div>
            <div className="text-xs text-gray-500">Hours Total</div>
          </div>
          <div className="bg-white border border-gray-200 rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-purple-600">100+</div>
            <div className="text-xs text-gray-500">Concepts</div>
          </div>
        </div>

        {/* Math Section */}
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm mb-4 overflow-hidden">
          <button
            onClick={() => setExpandedMath(!expandedMath)}
            className="w-full p-4 md:p-5 flex items-center justify-between bg-gradient-to-r from-blue-50 to-white hover:from-blue-100 transition-colors"
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">📐</span>
              <div className="text-left">
                <h2 className="text-lg font-semibold text-gray-900">Phase 1: Mathematics</h2>
                <p className="text-sm text-gray-500">9 documents · ~22 hours</p>
              </div>
            </div>
            <span className="text-gray-400 text-xl">{expandedMath ? '−' : '+'}</span>
          </button>

          {expandedMath && (
            <div className="border-t border-gray-100">
              {mathDocs.map((doc, idx) => (
                <Link
                  key={doc.id}
                  href={`/office-hours/math/${doc.id}`}
                  className="flex items-start gap-3 p-4 border-b border-gray-50 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-sm font-medium">
                    {idx + 1}
                  </div>
                  <div className="flex-grow min-w-0">
                    <div className="font-medium text-gray-900">{doc.title}</div>
                    <div className="text-sm text-gray-500 truncate">{doc.desc}</div>
                  </div>
                  <div className="flex-shrink-0 text-xs text-gray-400 hidden sm:block">
                    {doc.time}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Physics Section */}
        <div className="bg-white border border-gray-200 rounded-lg shadow-sm mb-6 overflow-hidden">
          <button
            onClick={() => setExpandedPhysics(!expandedPhysics)}
            className="w-full p-4 md:p-5 flex items-center justify-between bg-gradient-to-r from-green-50 to-white hover:from-green-100 transition-colors"
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">⚛️</span>
              <div className="text-left">
                <h2 className="text-lg font-semibold text-gray-900">Phase 2: Physics</h2>
                <p className="text-sm text-gray-500">10 documents · ~30 hours</p>
              </div>
            </div>
            <span className="text-gray-400 text-xl">{expandedPhysics ? '−' : '+'}</span>
          </button>

          {expandedPhysics && (
            <div className="border-t border-gray-100">
              {physicsDocs.map((doc, idx) => (
                <Link
                  key={doc.id}
                  href={`/office-hours/physics/${doc.id}`}
                  className="flex items-start gap-3 p-4 border-b border-gray-50 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 text-green-700 flex items-center justify-center text-sm font-medium">
                    {idx + 10}
                  </div>
                  <div className="flex-grow min-w-0">
                    <div className="font-medium text-gray-900">{doc.title}</div>
                    <div className="text-sm text-gray-500 truncate">{doc.desc}</div>
                  </div>
                  <div className="flex-shrink-0 text-xs text-gray-400 hidden sm:block">
                    {doc.time}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>

        {/* Z² Connections */}
        <div className="bg-gradient-to-br from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-4 md:p-6 mb-6">
          <h2 className="text-lg font-semibold text-purple-900 mb-4">🔗 Key Z² Connections</h2>
          <div className="space-y-3">
            {keyConnections.map((conn) => (
              <div key={conn.formula} className="flex items-center gap-3 bg-white/60 rounded-lg p-3">
                <div className="font-mono text-sm font-medium text-purple-700 whitespace-nowrap">
                  {conn.formula}
                </div>
                <div className="text-gray-400">→</div>
                <div className="flex-grow">
                  <div className="text-sm font-medium text-gray-800">{conn.topic}</div>
                  <div className="text-xs text-gray-500">{conn.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* The Four Pillars */}
        <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">🏛️ The Four Pillars</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="font-mono text-blue-700 text-lg">α⁻¹ = 4Z² + 3</div>
              <div className="text-sm text-gray-600">= 137.04 (0.004% error)</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="font-mono text-green-700 text-lg">αₛ = 4/Z²</div>
              <div className="text-sm text-gray-600">= 0.119 (1.24% error)</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="font-mono text-purple-700 text-lg">sin²θ_W = 3/13</div>
              <div className="text-sm text-gray-600">= 0.2308 (0.17% error)</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="font-mono text-orange-700 text-lg">v = M_P·e^(-Z²)·α</div>
              <div className="text-sm text-gray-600">= 249 GeV (1.12% error)</div>
            </div>
          </div>
        </div>

        {/* GitHub Link */}
        <div className="text-center py-4">
          <a
            href="https://github.com/carlzimmerman/zimmerman-formula/tree/main/office_hours_with_claude"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
            </svg>
            View markdown source on GitHub
          </a>
        </div>

        {/* Footer */}
        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <Link href="/" className="text-blue-600 hover:underline">
            ← Back to Zimmerman Framework
          </Link>
        </footer>
      </div>
    </main>
  )
}
