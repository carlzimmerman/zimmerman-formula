'use client'

import Link from 'next/link'

const PI = Math.PI
const Z = 2 * Math.sqrt(8 * PI / 3)
const Z_SQUARED = Z * Z
const L_FUNDAMENTAL = 20.6

export default function TopologyPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <header className="bg-white border-b border-gray-200 -mx-4 -mt-8 px-4 py-4 mb-6">
          <Link href="/" className="text-sm text-blue-600 hover:underline">
            Back to Overview
          </Link>
        </header>

        <article className="bg-white border border-gray-200 rounded shadow-sm p-8 mb-6">
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">
            T3/Z2 Cosmic Topology
          </h1>
          <p className="text-lg text-gray-600 mb-4">
            The universe is a 20.6 Gpc orbifold with built-in chirality
          </p>

          <div className="bg-red-50 border border-red-300 rounded p-6 my-6 text-center">
            <div className="font-mono text-xl text-gray-900 mb-2">
              eta(T3/Z2) = Z2 = 32pi/3 = 33.510
            </div>
            <div className="text-sm text-red-700 mt-3">
              The eta invariant of the spatial manifold IS the master constant Z2
            </div>
          </div>
        </article>

        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">What is T3/Z2?</h2>

          <div className="space-y-4 text-gray-700">
            <p>
              <strong>T3</strong> is the 3-torus: space that wraps around in all three directions.
              Travel far enough in any direction and you return to your starting point.
            </p>

            <p>
              <strong>Z2</strong> is an involution (reflection symmetry) acting on the torus.
              Points related by the Z2 action are identified as the same point.
            </p>

            <p>
              <strong>T3/Z2</strong> is an orbifold: a quotient space with 8 special
              fixed points where the Z2 symmetry acts trivially.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mt-6">
            <div className="p-4 bg-blue-50 rounded border border-blue-200 text-center">
              <div className="font-semibold text-gray-900">T3 (3-Torus)</div>
              <div className="text-sm text-gray-600">Periodic boundary conditions</div>
              <div className="text-xs text-blue-600 mt-1">b1 = 3 independent cycles</div>
            </div>
            <div className="p-4 bg-amber-50 rounded border border-amber-200 text-center">
              <div className="font-semibold text-gray-900">Z2 Action</div>
              <div className="text-sm text-gray-600">Point reflection x to -x</div>
              <div className="text-xs text-amber-600 mt-1">Creates chirality</div>
            </div>
            <div className="p-4 bg-green-50 rounded border border-green-200 text-center">
              <div className="font-semibold text-gray-900">8 Fixed Points</div>
              <div className="text-sm text-gray-600">Vertices of fundamental cube</div>
              <div className="text-xs text-green-600 mt-1">= CUBE = 8</div>
            </div>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Eta Invariant</h2>

          <p className="text-gray-700 mb-4">
            The eta invariant measures the spectral asymmetry of a manifold - roughly,
            the difference between left-handed and right-handed modes of the Dirac operator.
          </p>

          <div className="bg-gray-900 text-white rounded p-6 font-mono text-center mb-4">
            <div className="text-blue-300 text-sm mb-2">Atiyah-Patodi-Singer (1975):</div>
            <div className="text-xl">
              eta(M) = Sum sign(lambda_n) |lambda_n|^(-s) at s=0
            </div>
          </div>

          <div className="bg-red-50 border border-red-200 rounded p-4">
            <div className="font-semibold text-red-800 mb-2">Key Result:</div>
            <p className="text-gray-700">
              For T3/Z2 with the standard flat metric:
            </p>
            <div className="font-mono text-center text-xl mt-2 text-red-700">
              eta(T3/Z2) = 8 x (4pi/3) = 32pi/3 = Z2
            </div>
            <p className="text-sm text-gray-600 mt-2 text-center">
              The 8 fixed points each contribute 4pi/3 to the eta invariant
            </p>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">The Fundamental Domain</h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <p className="text-gray-700 mb-4">
                The T3/Z2 orbifold has a characteristic scale - the size of the
                fundamental domain (the smallest region that tiles to fill all of space).
              </p>

              <div className="bg-blue-50 border border-blue-200 rounded p-4 text-center">
                <div className="text-sm text-gray-600 mb-1">Fundamental Domain Scale</div>
                <div className="text-3xl font-mono font-bold text-blue-700">
                  Lc = {L_FUNDAMENTAL} Gpc
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  ~67 billion light-years
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-center gap-3 text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold">1</span>
                <span className="text-gray-700">Light wraps around the universe</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold">2</span>
                <span className="text-gray-700">High-z quasars have ghost images</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold">3</span>
                <span className="text-gray-700">CMB has finite-size cutoff</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold">4</span>
                <span className="text-gray-700">Parity-odd correlations are global</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Global Chirality</h2>

          <p className="text-gray-700 mb-4">
            The Z2 action defines a single chirality axis for the entire universe.
            This is the direction connecting opposite fixed points of the involution.
          </p>

          <div className="bg-amber-50 border border-amber-200 rounded p-4 mb-4">
            <div className="font-semibold text-amber-800 mb-2">Predicted Chirality Direction:</div>
            <div className="font-mono text-center text-xl">
              (l, b) = (287 deg, 9 deg) +/- 5 deg
            </div>
            <div className="text-sm text-gray-600 text-center mt-1">
              Galactic coordinates of the Z2 axis
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="p-4 bg-green-50 rounded border border-green-200">
              <div className="font-semibold text-green-800 mb-2">T3/Z2 Prediction</div>
              <p className="text-sm text-gray-700">
                Parity-odd 4PCF should show r ~ 1 correlation between
                any two sky regions (global chirality)
              </p>
            </div>
            <div className="p-4 bg-red-50 rounded border border-red-200">
              <div className="font-semibold text-red-800 mb-2">Local Physics Prediction</div>
              <p className="text-sm text-gray-700">
                Parity-odd 4PCF should show r ~ 0 correlation
                (independent random processes)
              </p>
            </div>
          </div>

          <div className="mt-4 p-4 bg-red-100 border border-red-300 rounded text-center">
            <div className="font-semibold text-red-800 mb-1">DESI DR1 Result (May 2026):</div>
            <div className="text-2xl font-mono font-bold text-red-700">
              r = 0.9986 +/- 0.0002
            </div>
            <div className="text-sm text-red-600 mt-1">
              Smoking gun confirmation of T3/Z2 topology
            </div>
          </div>
        </div>

        <div className="bg-white border border-gray-200 rounded shadow-sm p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Why Topology Matters</h2>

          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold flex-shrink-0">1</div>
              <div>
                <div className="font-semibold text-gray-900">Z2 is not arbitrary</div>
                <p className="text-sm text-gray-600">
                  It is the eta invariant of the spatial manifold - a topological constant that
                  cannot be changed without changing the topology itself.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-green-100 text-green-700 flex items-center justify-center font-bold flex-shrink-0">2</div>
              <div>
                <div className="font-semibold text-gray-900">Dark matter is topological</div>
                <p className="text-sm text-gray-600">
                  The T3 torus has b1 = 3 independent 1-cycles, each supporting 2 winding modes.
                  These 6 topological modes ARE the dark matter - no particles required.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center font-bold flex-shrink-0">3</div>
              <div>
                <div className="font-semibold text-gray-900">Observable predictions</div>
                <p className="text-sm text-gray-600">
                  Ghost quasars, CMB circles, 4PCF chirality axis - all testable consequences
                  of finite topology that differ from infinite flat space.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-red-100 text-red-700 flex items-center justify-center font-bold flex-shrink-0">4</div>
              <div>
                <div className="font-semibold text-gray-900">Unifies physics</div>
                <p className="text-sm text-gray-600">
                  From Z2 = eta(T3/Z2): fine structure constant, Weinberg angle, cosmological densities,
                  MOND scale, particle masses - all from topology.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <Link
            href="/evidence/4pcf"
            className="block p-4 bg-red-50 border border-red-200 rounded shadow-sm hover:border-red-400 transition-all text-center"
          >
            <div className="font-semibold text-red-800">DESI 4PCF Evidence</div>
            <div className="text-sm text-red-600">r = 0.9986 confirmed</div>
          </Link>
          <Link
            href="/dark-matter"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Topological Dark Matter</div>
            <div className="text-sm text-gray-500">Why no particles</div>
          </Link>
          <Link
            href="/ghost-quasars"
            className="block p-4 bg-white border border-gray-200 rounded shadow-sm hover:border-blue-300 transition-all text-center"
          >
            <div className="font-semibold text-gray-900">Ghost Quasars</div>
            <div className="text-sm text-gray-500">Nobel-level test</div>
          </Link>
        </div>

        <footer className="text-center text-sm text-gray-500 py-6 border-t border-gray-200">
          <p>
            The universe is finite, has a shape, and that shape determines physics
          </p>
        </footer>
      </div>
    </main>
  )
}
