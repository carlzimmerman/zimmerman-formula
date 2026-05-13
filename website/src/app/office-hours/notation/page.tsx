'use client'

import { useState } from 'react'
import DocumentLayout, { Section, SubSection, KeyPoint, InteractiveBox } from '@/components/DocumentLayout'

// Symbol Search Component
function SymbolSearch({ symbols }: { symbols: { symbol: string; name: string; meaning: string; usage: string }[] }) {
  const [search, setSearch] = useState('')

  const filtered = symbols.filter(s =>
    s.symbol.toLowerCase().includes(search.toLowerCase()) ||
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.meaning.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="space-y-4">
      <input
        type="text"
        placeholder="Search symbols (e.g., 'Z²', 'torus', 'coupling')..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none"
      />
      <div className="max-h-96 overflow-y-auto space-y-2">
        {filtered.map((s, i) => (
          <div key={i} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
            <div className="flex items-start gap-4">
              <span className="text-2xl font-mono text-blue-600 min-w-[80px]">{s.symbol}</span>
              <div className="flex-1">
                <div className="font-medium text-gray-900">{s.name}</div>
                <div className="text-sm text-gray-600">{s.meaning}</div>
                <div className="text-xs text-purple-600 mt-1">Used in: {s.usage}</div>
              </div>
            </div>
          </div>
        ))}
        {filtered.length === 0 && (
          <div className="text-gray-500 text-center py-4">No symbols found matching "{search}"</div>
        )}
      </div>
    </div>
  )
}

// Quick Reference Card
function QuickRef({ title, items }: { title: string; items: { sym: string; val: string }[] }) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-purple-50 p-4 rounded-lg border border-blue-200">
      <h4 className="font-semibold text-gray-900 mb-3">{title}</h4>
      <div className="space-y-2">
        {items.map((item, i) => (
          <div key={i} className="flex justify-between items-center text-sm">
            <span className="font-mono text-purple-700">{item.sym}</span>
            <span className="text-gray-600">{item.val}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

const allSymbols = [
  // Core Framework
  { symbol: 'Z²', name: 'Z-squared', meaning: 'The fundamental geometric constant = 32π/3 ≈ 33.51', usage: 'All derivations' },
  { symbol: 'T³', name: '3-torus', meaning: 'Three-dimensional torus = S¹ × S¹ × S¹', usage: 'Compactification, topology' },
  { symbol: 'T³/Z₂', name: 'Orbifold', meaning: 'The 3-torus with Z₂ identification x ~ -x', usage: 'Central geometric structure' },
  { symbol: 'Z₂', name: 'Cyclic group of order 2', meaning: 'The parity group {1, -1}', usage: 'Orbifold action, chirality' },

  // Coupling Constants
  { symbol: 'α', name: 'Fine structure constant', meaning: 'EM coupling ≈ 1/137', usage: 'QED, electromagnetism' },
  { symbol: 'α⁻¹', name: 'Inverse fine structure constant', meaning: '= 4Z² + 3 ≈ 137.04', usage: 'Framework derivation' },
  { symbol: 'αₛ', name: 'Strong coupling constant', meaning: '= 4/Z² ≈ 0.119 at M_Z', usage: 'QCD, strong force' },
  { symbol: 'sin²θ_W', name: 'Weak mixing angle', meaning: '= 3/13 ≈ 0.2308', usage: 'Electroweak unification' },

  // Cosmological Parameters
  { symbol: 'Ω_Λ', name: 'Dark energy density', meaning: '= 13/19 ≈ 0.684', usage: 'Cosmology, holographic' },
  { symbol: 'Ω_m', name: 'Matter density', meaning: '= 6/19 ≈ 0.316', usage: 'Cosmology' },
  { symbol: 'r', name: 'Tensor-to-scalar ratio', meaning: '= 1/(2Z²) ≈ 0.015', usage: 'Inflation, CMB' },
  { symbol: 'nₛ', name: 'Spectral index', meaning: '≈ 0.967', usage: 'Primordial fluctuations' },
  { symbol: 'ε', name: 'Slow-roll parameter', meaning: '= 1/(32π) ≈ 0.00995', usage: 'Inflation' },
  { symbol: 'ρ_Λ', name: 'Vacuum energy density', meaning: '~ e^(-8Z²) M_P⁴', usage: 'CC problem' },

  // Framework Integers
  { symbol: 'GAUGE = 12', name: 'Gauge integer', meaning: 'Number of cube edges = SM gauge bosons', usage: 'Mode counting' },
  { symbol: 'BEKENSTEIN = 4', name: 'Bekenstein integer', meaning: 'Number of body diagonals = spacetime dimensions', usage: 'Holography' },
  { symbol: 'N_gen = 3', name: 'Generation number', meaning: 'Number of cube axes = fermion generations', usage: 'Particle physics' },
  { symbol: 'n_B = 16', name: 'Bosonic modes', meaning: '8 fixed points × 2 twisted sector modes', usage: 'Mode counting' },
  { symbol: 'n_F = 3', name: 'Fermionic modes', meaning: 'Chiral zero modes after GSO projection', usage: 'Mode counting' },
  { symbol: 'N_total = 19', name: 'Total modes', meaning: '16 + 3 = total topological DoF', usage: 'Mode counting' },

  // Topological Invariants
  { symbol: 'b₁(T³)', name: 'First Betti number', meaning: '= 3, counts independent 1-cycles', usage: 'Topology, generations' },
  { symbol: 'χ', name: 'Euler characteristic', meaning: 'Topological invariant = V - E + F', usage: 'Topology' },
  { symbol: 'I_ab', name: 'Intersection number', meaning: '= 3, D-brane intersection', usage: 'sin²θ_W derivation' },
  { symbol: 'N_EW', name: 'Electroweak capacity', meaning: '= 16 - 3 = 13', usage: 'sin²θ_W derivation' },
  { symbol: 'H_n(M)', name: 'Homology group', meaning: 'n-th homology of manifold M', usage: 'Algebraic topology' },
  { symbol: 'H^n(M)', name: 'Cohomology group', meaning: 'n-th cohomology of manifold M', usage: 'Algebraic topology' },

  // Differential Geometry
  { symbol: 'g_μν', name: 'Metric tensor', meaning: '4D spacetime metric', usage: 'General relativity' },
  { symbol: 'h_ij', name: 'Induced 3-metric', meaning: 'Spatial metric on hypersurface', usage: 'ADM formalism' },
  { symbol: 'N', name: 'Lapse function', meaning: 'Proper time between slices', usage: 'ADM formalism' },
  { symbol: 'N^i', name: 'Shift vector', meaning: 'Spatial coordinate evolution', usage: 'ADM formalism' },
  { symbol: 'σ_ij', name: 'Shear tensor', meaning: 'Encodes cubic anisotropy', usage: 'Framework, ADM' },
  { symbol: 'R', name: 'Ricci scalar', meaning: 'Scalar curvature', usage: 'General relativity' },
  { symbol: 'R_μν', name: 'Ricci tensor', meaning: 'Contracted Riemann tensor', usage: 'General relativity' },
  { symbol: 'R^ρ_σμν', name: 'Riemann tensor', meaning: 'Spacetime curvature tensor', usage: 'Differential geometry' },
  { symbol: 'Γ^λ_μν', name: 'Christoffel symbols', meaning: 'Connection coefficients', usage: 'Differential geometry' },
  { symbol: '∇_μ', name: 'Covariant derivative', meaning: 'Derivative preserving tensor character', usage: 'Differential geometry' },

  // Quantum Mechanics & QFT
  { symbol: 'ψ, Ψ', name: 'Wave function / Spinor', meaning: 'Quantum state / Fermionic field', usage: 'QM, QFT' },
  { symbol: 'Ψ_L, Ψ_R', name: 'Left/right-handed spinors', meaning: 'Chiral components of spinor', usage: 'Chirality' },
  { symbol: 'γ^μ', name: 'Dirac gamma matrices', meaning: 'Satisfy {γ^μ, γ^ν} = 2g^μν', usage: 'Dirac equation' },
  { symbol: 'γ⁵', name: 'Chirality matrix', meaning: '= iγ⁰γ¹γ²γ³, defines L/R projections', usage: 'Chirality' },
  { symbol: 'D̸', name: 'Dirac operator', meaning: '= γ^μ D_μ, covariant Dirac operator', usage: 'Index theory' },
  { symbol: 'η_p', name: 'Fermionic parity', meaning: '= -1 for orbifold projection', usage: 'Chirality theorem' },
  { symbol: 'F_μν', name: 'Field strength tensor', meaning: 'Electromagnetic field tensor', usage: 'Gauge theory' },
  { symbol: 'G^a_μν', name: 'Gluon field strength', meaning: 'SU(3) field strength', usage: 'QCD' },
  { symbol: 'Φ', name: 'Higgs doublet', meaning: '= (φ⁺, φ⁰)^T, 4 real components', usage: 'Electroweak' },
  { symbol: 'v', name: 'Higgs VEV', meaning: '= M_P × e^(-Z²) × α ≈ 249 GeV', usage: 'Hierarchy problem' },

  // Index Theory
  { symbol: 'Â(R)', name: 'A-roof genus', meaning: 'Characteristic class in index theorem', usage: 'APS theorem' },
  { symbol: 'ch(E)', name: 'Chern character', meaning: 'Characteristic class of bundle E', usage: 'Index theory' },
  { symbol: 'η(s)', name: 'Eta function', meaning: 'Spectral asymmetry function', usage: 'APS theorem' },
  { symbol: 'η(0)', name: 'Eta invariant', meaning: 'Spectral asymmetry at s=0', usage: 'APS theorem' },
  { symbol: 'Index(D̸)', name: 'Index of Dirac operator', meaning: '= n_+ - n_- (zero mode count)', usage: 'Index theory' },

  // Scales & Constants
  { symbol: 'M_P', name: 'Planck mass', meaning: '≈ 1.22 × 10¹⁹ GeV', usage: 'Quantum gravity' },
  { symbol: 'M_Z', name: 'Z boson mass', meaning: '≈ 91.2 GeV', usage: 'Electroweak scale' },
  { symbol: 'ℏ', name: 'Reduced Planck constant', meaning: '= h/(2π)', usage: 'Quantum mechanics' },
  { symbol: 'c', name: 'Speed of light', meaning: '≈ 3 × 10⁸ m/s', usage: 'Relativity' },
  { symbol: 'G', name: 'Newton constant', meaning: 'Gravitational coupling', usage: 'Gravity' },

  // Group Theory
  { symbol: 'SU(N)', name: 'Special unitary group', meaning: 'N×N unitary matrices with det=1', usage: 'Gauge theory' },
  { symbol: 'SU(3)_C', name: 'Color group', meaning: 'QCD gauge group', usage: 'Strong force' },
  { symbol: 'SU(2)_L', name: 'Weak isospin', meaning: 'Weak force gauge group', usage: 'Weak force' },
  { symbol: 'U(1)_Y', name: 'Hypercharge', meaning: 'Hypercharge gauge group', usage: 'Electroweak' },
  { symbol: 'G_SM', name: 'Standard Model group', meaning: '= SU(3)×SU(2)×U(1)', usage: 'Standard Model' },
  { symbol: 'rank(G)', name: 'Rank of group', meaning: 'Dimension of Cartan subalgebra = 4', usage: 'Gauge structure' },
  { symbol: 'dim(G)', name: 'Dimension of group', meaning: 'Number of generators', usage: 'Gauge structure' },

  // Holography & String Theory
  { symbol: 'AdS_5', name: 'Anti-de Sitter space', meaning: '5D spacetime with negative curvature', usage: 'Holography' },
  { symbol: 'z', name: 'Holographic coordinate', meaning: 'Radial AdS direction ~ 1/μ', usage: 'Holographic RG' },
  { symbol: 'β(g)', name: 'Beta function', meaning: 'RG flow of coupling g', usage: 'Renormalization' },
  { symbol: 'β_holo', name: 'Holographic beta function', meaning: '= -β_QFT (opposite sign)', usage: 'Holography' },
  { symbol: 'N_surface', name: 'Surface degrees of freedom', meaning: '= n_B = 16', usage: 'Holographic equipartition' },
  { symbol: 'N_bulk', name: 'Bulk degrees of freedom', meaning: '= n_F = 3', usage: 'Holographic equipartition' },
]

export default function NotationPage() {
  return (
    <DocumentLayout
      title="Notation & Symbols Reference"
      description="Complete guide to all mathematical notation used in the Z² Framework"
      phase="math"
      currentIndex={9}
      prevLink={{ href: '/office-hours/math/08-intersection-theory', title: 'Intersection Theory' }}
      nextLink={{ href: '/office-hours/physics/00-classical-mechanics', title: 'Classical Mechanics' }}
    >
      <Section title="Quick Reference Cards">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <QuickRef title="Core Framework" items={[
            { sym: 'Z²', val: '= 32π/3 ≈ 33.51' },
            { sym: 'T³/Z₂', val: 'Orbifold space' },
            { sym: '8', val: 'Fixed points' },
            { sym: '4π/3', val: 'Per fixed point' },
          ]} />
          <QuickRef title="The Four Pillars" items={[
            { sym: 'α⁻¹', val: '= 4Z² + 3 = 137.04' },
            { sym: 'αₛ', val: '= 4/Z² = 0.119' },
            { sym: 'sin²θ_W', val: '= 3/13 = 0.2308' },
            { sym: 'v', val: '= M_P·e^(-Z²)·α = 249 GeV' },
          ]} />
          <QuickRef title="Mode Counting" items={[
            { sym: 'n_B', val: '= 16 (bosonic)' },
            { sym: 'n_F', val: '= 3 (fermionic)' },
            { sym: 'N_total', val: '= 19' },
            { sym: 'N_EW', val: '= 13' },
          ]} />
          <QuickRef title="Cosmology" items={[
            { sym: 'Ω_Λ', val: '= 13/19 = 0.684' },
            { sym: 'Ω_m', val: '= 6/19 = 0.316' },
            { sym: 'r', val: '= 1/(2Z²) = 0.015' },
            { sym: 'ρ_Λ', val: '~ e^(-8Z²) M_P⁴' },
          ]} />
          <QuickRef title="Framework Integers" items={[
            { sym: 'GAUGE', val: '= 12 (cube edges)' },
            { sym: 'BEKENSTEIN', val: '= 4 (diagonals)' },
            { sym: 'N_gen', val: '= 3 (axes)' },
            { sym: 'rank(G_SM)', val: '= 4' },
          ]} />
          <QuickRef title="Topology" items={[
            { sym: 'b₁(T³)', val: '= 3' },
            { sym: 'I_ab', val: '= 3' },
            { sym: 'χ(T³/Z₂)', val: '= 4' },
            { sym: 'H₁(T³)', val: '= Z³' },
          ]} />
        </div>
      </Section>

      <Section title="Searchable Symbol Index">
        <InteractiveBox title="Symbol Search">
          <SymbolSearch symbols={allSymbols} />
        </InteractiveBox>
      </Section>

      <Section title="1. Core Framework Symbols">
        <SubSection title="The Fundamental Constant">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200 text-center my-4">
            <div className="text-3xl font-mono text-blue-800 mb-2">Z² = 8 × (4π/3) = 32π/3 ≈ 33.51</div>
            <div className="text-sm text-blue-600">The geometric constant from which all Standard Model parameters derive</div>
          </div>
          <p className="text-gray-700">
            <strong>Z²</strong> represents the phase space volume of a sphere inscribed in a cube:
            8 vertices × unit sphere volume (4π/3). This is derived from the algebraic resolution
            of orbifold singularities on T³/Z₂.
          </p>
        </SubSection>

        <SubSection title="The Orbifold Structure">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
            <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
              <div className="text-xl font-mono text-purple-800 text-center mb-2">T³ = S¹ × S¹ × S¹</div>
              <div className="text-sm text-purple-600 text-center">3-torus: product of three circles</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
              <div className="text-xl font-mono text-purple-800 text-center mb-2">T³/Z₂</div>
              <div className="text-sm text-purple-600 text-center">Orbifold with Z₂ identification: x ~ -x</div>
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="2. Coupling Constants">
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-3 text-left">Symbol</th>
                <th className="border border-gray-200 p-3 text-left">Name</th>
                <th className="border border-gray-200 p-3 text-left">Framework Formula</th>
                <th className="border border-gray-200 p-3 text-left">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-3 font-mono">α⁻¹</td>
                <td className="border border-gray-200 p-3">Fine structure constant inverse</td>
                <td className="border border-gray-200 p-3 font-mono">4Z² + 3</td>
                <td className="border border-gray-200 p-3">137.04 (0.004% error)</td>
              </tr>
              <tr className="bg-gray-50">
                <td className="border border-gray-200 p-3 font-mono">αₛ</td>
                <td className="border border-gray-200 p-3">Strong coupling</td>
                <td className="border border-gray-200 p-3 font-mono">4/Z²</td>
                <td className="border border-gray-200 p-3">0.119 (1.24% error)</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-3 font-mono">sin²θ_W</td>
                <td className="border border-gray-200 p-3">Weak mixing angle</td>
                <td className="border border-gray-200 p-3 font-mono">I_ab / N_EW = 3/13</td>
                <td className="border border-gray-200 p-3">0.2308 (0.17% error)</td>
              </tr>
              <tr className="bg-gray-50">
                <td className="border border-gray-200 p-3 font-mono">v</td>
                <td className="border border-gray-200 p-3">Higgs VEV</td>
                <td className="border border-gray-200 p-3 font-mono">M_P × e^(-Z²) × α</td>
                <td className="border border-gray-200 p-3">249 GeV (1.12% error)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="3. Topological Notation">
        <SubSection title="Homology & Betti Numbers">
          <div className="space-y-3">
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-blue-600 min-w-[100px]">H_n(M)</span>
              <span className="text-gray-700">n-th homology group of manifold M (measures n-dimensional holes)</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-blue-600 min-w-[100px]">b_n(M)</span>
              <span className="text-gray-700">n-th Betti number = rank(H_n(M))</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-blue-600 min-w-[100px]">b₁(T³) = 3</span>
              <span className="text-gray-700">Three independent 1-cycles on T³ → three fermion generations</span>
            </div>
          </div>
        </SubSection>

        <SubSection title="Intersection Theory">
          <div className="space-y-3">
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-blue-600 min-w-[100px]">I_ab</span>
              <span className="text-gray-700">Intersection number of D-brane stacks a and b</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-blue-600 min-w-[100px]">Π_a · Π_b</span>
              <span className="text-gray-700">Homological intersection of cycles</span>
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="4. Differential Geometry">
        <SubSection title="Metric & Connection">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">g_μν</span>
              <span className="text-gray-700 ml-2">Spacetime metric tensor</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">h_ij</span>
              <span className="text-gray-700 ml-2">Induced spatial metric</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">Γ^λ_μν</span>
              <span className="text-gray-700 ml-2">Christoffel connection</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">∇_μ</span>
              <span className="text-gray-700 ml-2">Covariant derivative</span>
            </div>
          </div>
        </SubSection>

        <SubSection title="Curvature">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">R^ρ_σμν</span>
              <span className="text-gray-700 ml-2">Riemann tensor</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">R_μν</span>
              <span className="text-gray-700 ml-2">Ricci tensor</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">R</span>
              <span className="text-gray-700 ml-2">Ricci scalar</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">G_μν</span>
              <span className="text-gray-700 ml-2">Einstein tensor</span>
            </div>
          </div>
        </SubSection>

        <SubSection title="ADM Formalism">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">N</span>
              <span className="text-gray-700 ml-2">Lapse function</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">N^i</span>
              <span className="text-gray-700 ml-2">Shift vector</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">K_ij</span>
              <span className="text-gray-700 ml-2">Extrinsic curvature</span>
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <span className="font-mono text-purple-600">σ_ij</span>
              <span className="text-gray-700 ml-2">Shear tensor</span>
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="5. Quantum Field Theory">
        <SubSection title="Spinors & Chirality">
          <div className="space-y-3">
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-green-600 min-w-[80px]">Ψ</span>
              <span className="text-gray-700">Dirac spinor field</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-green-600 min-w-[80px]">Ψ_L, Ψ_R</span>
              <span className="text-gray-700">Left- and right-handed chiral components</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-green-600 min-w-[80px]">γ^μ</span>
              <span className="text-gray-700">Dirac gamma matrices, {'{γ^μ, γ^ν} = 2g^μν'}</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-green-600 min-w-[80px]">γ⁵</span>
              <span className="text-gray-700">Chirality matrix = iγ⁰γ¹γ²γ³</span>
            </div>
          </div>
        </SubSection>

        <SubSection title="Gauge Fields">
          <div className="space-y-3">
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-green-600 min-w-[80px]">A_μ</span>
              <span className="text-gray-700">Gauge potential (vector field)</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-green-600 min-w-[80px]">F_μν</span>
              <span className="text-gray-700">Field strength tensor = ∂_μA_ν - ∂_νA_μ</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-green-600 min-w-[80px]">G^a_μν</span>
              <span className="text-gray-700">Gluon field strength (SU(3) gauge field)</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-green-600 min-w-[80px]">D_μ</span>
              <span className="text-gray-700">Gauge covariant derivative = ∂_μ + igA_μ</span>
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="6. Index Theory">
        <SubSection title="APS Index Theorem">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200 my-4">
            <div className="text-center font-mono text-blue-800 mb-2">
              Index(D̸) = ∫_M Â(R) ∧ ch(E) - (η(0) + h)/2
            </div>
            <div className="text-sm text-blue-600 text-center">Atiyah-Patodi-Singer Index Theorem</div>
          </div>
          <div className="space-y-3">
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-orange-600 min-w-[80px]">D̸</span>
              <span className="text-gray-700">Dirac operator = γ^μD_μ</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-orange-600 min-w-[80px]">Â(R)</span>
              <span className="text-gray-700">A-roof genus (characteristic class)</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-orange-600 min-w-[80px]">ch(E)</span>
              <span className="text-gray-700">Chern character of vector bundle E</span>
            </div>
            <div className="flex items-start gap-4 p-3 bg-gray-50 rounded">
              <span className="font-mono text-orange-600 min-w-[80px]">η(0)</span>
              <span className="text-gray-700">Eta invariant (spectral asymmetry)</span>
            </div>
          </div>
        </SubSection>
      </Section>

      <Section title="7. Group Theory">
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50">
                <th className="border border-gray-200 p-3 text-left">Group</th>
                <th className="border border-gray-200 p-3 text-left">Dimension</th>
                <th className="border border-gray-200 p-3 text-left">Rank</th>
                <th className="border border-gray-200 p-3 text-left">Role in SM</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="border border-gray-200 p-3 font-mono">SU(3)_C</td>
                <td className="border border-gray-200 p-3">8</td>
                <td className="border border-gray-200 p-3">2</td>
                <td className="border border-gray-200 p-3">Color (strong force)</td>
              </tr>
              <tr className="bg-gray-50">
                <td className="border border-gray-200 p-3 font-mono">SU(2)_L</td>
                <td className="border border-gray-200 p-3">3</td>
                <td className="border border-gray-200 p-3">1</td>
                <td className="border border-gray-200 p-3">Weak isospin</td>
              </tr>
              <tr>
                <td className="border border-gray-200 p-3 font-mono">U(1)_Y</td>
                <td className="border border-gray-200 p-3">1</td>
                <td className="border border-gray-200 p-3">1</td>
                <td className="border border-gray-200 p-3">Hypercharge</td>
              </tr>
              <tr className="bg-purple-50">
                <td className="border border-gray-200 p-3 font-mono font-bold">G_SM</td>
                <td className="border border-gray-200 p-3 font-bold">12</td>
                <td className="border border-gray-200 p-3 font-bold">4</td>
                <td className="border border-gray-200 p-3 font-bold">Total (= cube edges)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Section>

      <Section title="8. Physical Scales">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-900 mb-3">Energy Scales</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="font-mono">M_P</span>
                <span>1.22 × 10¹⁹ GeV (Planck)</span>
              </div>
              <div className="flex justify-between">
                <span className="font-mono">M_GUT</span>
                <span>~10¹⁶ GeV (GUT scale)</span>
              </div>
              <div className="flex justify-between">
                <span className="font-mono">M_Z</span>
                <span>91.2 GeV (Z boson)</span>
              </div>
              <div className="flex justify-between">
                <span className="font-mono">v</span>
                <span>246 GeV (Higgs VEV)</span>
              </div>
            </div>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold text-gray-900 mb-3">Fundamental Constants</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="font-mono">c</span>
                <span>2.998 × 10⁸ m/s</span>
              </div>
              <div className="flex justify-between">
                <span className="font-mono">ℏ</span>
                <span>1.055 × 10⁻³⁴ J·s</span>
              </div>
              <div className="flex justify-between">
                <span className="font-mono">G</span>
                <span>6.674 × 10⁻¹¹ m³/kg·s²</span>
              </div>
              <div className="flex justify-between">
                <span className="font-mono">e</span>
                <span>1.602 × 10⁻¹⁹ C</span>
              </div>
            </div>
          </div>
        </div>
      </Section>

      <KeyPoint>
        <strong>Reading the v8.8.8 Paper:</strong> After completing this curriculum, you should recognize
        all symbols and notation used in the manuscript. The key insight is that all Standard Model
        parameters emerge from the single geometric constant Z² = 32π/3, derived from the T³/Z₂ orbifold
        structure.
      </KeyPoint>
    </DocumentLayout>
  )
}
