'use client';

/**
 * ActionExplorer — the flagship action, term by term.
 * The scaffold is Aether-Scalar-Tensor theory (Skordis & Złośnik 2021, PRL 127, 161302 —
 * theirs, credited). The framework's contribution is the promotion 𝒜(Q) = a₀²(Q) =
 * κ²G(−K(Q)) and the offset-DBI K — click each term.
 */

import { useState } from 'react';

const TERMS = [
  {
    id: 'eh',
    tex: '(R − 2Λ_bare)/16πG',
    name: 'Einstein–Hilbert + bare Λ',
    color: 'text-gray-200 hover:text-white',
    body:
      'Plain general relativity. Where gradients are strong (the inner Solar System, compact ' +
      'objects) everything below switches off and this term governs alone — Newtonian residual ' +
      'e^(−√y) ≈ 10⁻³⁴⁵⁷ at Earth’s orbit.',
  },
  {
    id: 'aether',
    tex: '𝓛_aether[A, g]',
    name: 'the unit-timelike aether',
    color: 'text-purple-300 hover:text-purple-200',
    body:
      'Skordis–Złośnik’s vector field A^μ (A^μA_μ = −1): it carries the cosmic frame that a ' +
      'MOND-type theory needs, and its kinetic structure keeps gravitational waves at exactly the ' +
      'speed of light (c_T = 1, GW170817-safe). Entirely theirs — credited, not claimed.',
  },
  {
    id: 'galaxy',
    tex: '(𝒜(Q)/8πG) · 𝓕_Y(Y/𝒜(Q))',
    name: 'the galaxy sector — where a₀ lives',
    color: 'text-cyan-300 hover:text-cyan-200',
    body:
      'Y is the spatial gradient of the scalar (the field of a galaxy); 𝓕_Y encodes the ' +
      'interpolation kernel. THE PROMOTION: the constant a₀² is replaced by 𝒜(Q) = κ²G(−K(Q)) ' +
      '— the MOND scale IS the dark sector’s pressure. Today −K = ρ_Λ, so ' +
      'a₀ = κc√(Gρ_Λ) = 9.36×10⁻¹¹ m s⁻² falls out to the digit. κ = ½ is FITTED, not derived ' +
      '(measured 0.551 ± 0.043).',
  },
  {
    id: 'kq',
    tex: 'K(Q) = −M⁴ + μ²Λ_D²[1 − √(1 − (Q−Q₀)²/Λ_D²)]',
    name: 'the cosmology sector — an offset DBI',
    color: 'text-emerald-300 hover:text-emerald-200',
    body:
      'Q is the temporal part of the scalar (the cosmological mode). One bounded function does ' +
      'three jobs: at the minimum, w = −1 EXACTLY (dark energy, the vacuum never rolls); small ' +
      'excitations have density linear in the displacement (dust — the dark matter the CMB ' +
      'needs); and the square-root wall bounds the pressure (the early stiff phase is killed, ' +
      'and a₀ switches off toward recombination). β ≡ μ²Λ_D²/M⁴ = 1 is selected, not derived. ' +
      'The background rate Q₀ — free in AeST across four orders of magnitude — is pinned by ' +
      'galaxy-scale phenomenology to 0.0024–0.0146 Mpc⁻¹ (DOI 10.5281/zenodo.21937958).',
  },
  {
    id: 'bump',
    tex: 'A_b · (Y/𝒜)/(1 + Y/𝒜)² · (Q − Q₀)²',
    name: 'the a₀-bump — the cluster response',
    color: 'text-amber-300 hover:text-amber-200',
    body:
      'A response peaked exactly at the framework’s own acceleration scale: negligible in ' +
      'galaxies and the Solar System, active in cluster cores where g crosses a₀. The live ' +
      'candidate for the cluster residual — carried with its full health matrix (c_T = 1 exact, ' +
      'no-ghost theorem) and its open items stated.',
  },
  {
    id: 'matter',
    tex: 'S_m[g, ψ]',
    name: 'matter — one metric',
    color: 'text-rose-300 hover:text-rose-200',
    body:
      'Everything we are made of couples to g_μν alone. That single fact is why lensing comes ' +
      'out right without dark halos: Φ = Ψ, γ_PPN = 1, and the 21σ lensing exclusion that ' +
      'killed the modified-inertia arm is cleared at 0.6σ here.',
  },
];

export default function ActionExplorer() {
  const [active, setActive] = useState('galaxy');
  const term = TERMS.find((t) => t.id === active)!;

  return (
    <div className="rounded-xl border border-gray-700 bg-black/40 p-5">
      <h3 className="mb-3 text-lg font-semibold text-white">The action — click each term</h3>

      <div className="rounded-lg bg-gray-900/80 p-4 font-mono text-sm leading-relaxed text-gray-400">
        <span className="text-gray-500">S = ∫ d⁴x √−g {'{'} </span>
        {TERMS.slice(0, 5).map((t, i) => (
          <span key={t.id}>
            <button
              onClick={() => setActive(t.id)}
              className={`${t.color} ${active === t.id ? 'underline decoration-dotted underline-offset-4' : ''}`}
            >
              {t.tex}
            </button>
            {i < 4 && <span className="text-gray-600"> + </span>}
          </span>
        ))}
        <span className="text-gray-500"> {'}'} + </span>
        <button
          onClick={() => setActive('matter')}
          className={`${TERMS[5].color} ${active === 'matter' ? 'underline decoration-dotted underline-offset-4' : ''}`}
        >
          {TERMS[5].tex}
        </button>
      </div>

      <div className="mt-4 rounded-md border border-gray-700 bg-gray-900/40 p-4">
        <div className="mb-1 text-sm font-semibold text-white">{term.name}</div>
        <p className="text-sm leading-relaxed text-gray-300">{term.body}</p>
      </div>

      <p className="mt-3 text-xs text-gray-500">
        Q ≡ A^μ∇_μφ (temporal), Y ≡ (g^{'{μν}'} + A^μA^ν)∇_μφ∇_νφ (spatial): the SAME scalar field,
        split by the aether into a cosmology sector and a galaxy sector. That split is why one
        Lagrangian can fit the CMB and the rotation curves at once — and why the dark-energy triumph
        and the galaxy-scale dark-matter question are the same property of the same field.
      </p>
    </div>
  );
}
