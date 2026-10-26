# CA1_covariant_self_coupling — RESULT: SHAPE ONLY, FOOTINGS SPLIT. The slope has a covariant origin; the amplitude needs one new constant

Frozen criteria 7926bab64c (committed alone; no amendment). κ = ½ FITTED. Footings canonical / alt are graded separately and
never pooled. Cold dark energy is a field paired with dark energy. "Scattering" here means scattering of the field's
excitations on its mass shell (CFG723 B/D5), not a dark-matter particle. Nothing here says the data favour the framework or
ΛCDM. Not "theory closed".

**Question (PAPER61 OPEN item).** Is there a covariant self-coupling of the cold dark energy that reproduces the core law?
The law needs a cross-section per mass s(σ) ∝ σ^(−n), with n = 0.784 / 0.496 (OS1) and LN2's normalisation
K = 9σ_ref^(1+n)/(4πG t Σ_a0²). The second question is whether a₀ or Λ fix its scales.

## Answer

1. **Yes for the slope.** Exchanging a *pair* of dark-energy quanta of Hubble range gives a pure power-law potential
   V = C_p/r^p on halo scales. Its classical cross-section is σ_T ∝ v^(−4/p) exactly, with no velocity scale (Lean
   `powerlaw_scaling`). Here Λ does real work: a dark-energy field mass m_φ ≲ ħ√(Gρ_Λ)/c² makes the range ~ Gpc, so n stays
   constant from 10 to 1500 km/s. That is what the data want, and a single Yukawa mediator cannot do it (point 3).
   - Canonical (n = 0.784) selects **p = 5**, n = 0.800. This is a dimension-6 current–current coupling
     (1/M²) J_χ^μ ψ̄γ_μψ to a light dark-energy fermion pair.
   - Alt (n = 0.496) selects **p = 7**, n = 0.571. This is a shift-symmetric derivative coupling (1/M²)|χ|²(∂φ)² to a
     quintessence-like scalar.
   - **No integer p serves both footings** (Lean `no_common_power`: the canonical window is {5}, the alt window is
     {7, 8, 9, 10}).
2. **No for the amplitude: the obstruction.** The normalisation always needs one new constant: the coupling scale M or the
   field mass m_χ.
   - From (G, c, a₀, ρ_Λ, t), every velocity is c·(a₀t/c)^d·(Gρ_Λt²)^a (Lean `velocity_monomial`, sympy). So nothing gives
     the ~70 km/s scale that the anchor carries. Writing σ_ref = c(a₀t/c)^k needs k = 4.19 (canonical) / 4.63 (alt): not an
     integer, and different on the two footings, so it is numerology.
   - The frozen no-new-constant menu M ∈ {E_Λ, E_Pl} × m_χc² ∈ {E_Λ, E_Pl, √(E_Λ E_Pl)} (E_Λ = 2.24 / 2.46 meV) misses G2
     by 10^1 to 10^58.
   - The closest cell is p = 7 with M = E_Pl, m_χ = E_Λ, at 10^−1.06 / 10^−0.97 of the target. That still fails G2's factor
     of 2, and it is not a valid cell anyway: a 2 meV quantum is in the quantum regime, while the classical power law needs
     m_χ ≥ 685 / 777 GeV (G6). It is reported as a coincidence, not a lead.
3. **The other candidates fail G1 (the slope), whatever their constants.**
   - Contact λ|χ|⁴ gives n = 0.
   - A Yukawa mediator whose range is tied to a₀ or Λ (c²/a₀, c/√(Gρ_Λ)) gives the Coulomb limit n ≥ 3.94 at every
     m_χ ≥ 1.3e-20 eV. Its large-β branch has σ_T/m ≥ πλ²/m ~ 1e62 cm²/g.
   - A free Yukawa does no better. No Born v★ (1–1e5 km/s), no classical β (attractive or repulsive, 1e-3–1e9) and no
     Hulthén s-wave cell (0 / 1089) keeps |n_eff − n| ≤ 0.10 on both the SPARC span (20–200 km/s) and the cluster span
     (400–1300 km/s). A single Yukawa's slope drifts too fast across two decades of speed. The closest are classical
     attractive, with n_eff 0.53 / 0.78 (canonical) and 0.49 / 0.64 (alt). Even if one passed, its v★ would be a new
     constant.
   - A superfluid / condensate fails twice. Its contact or phonon scattering gives n = 0. And the target itself has
     Kn = 539–2048 ≫ 1 and Γt = 1 (LN2), so the core is a long-mean-free-path gas, not a hydrodynamic condensate. This
     agrees with CFG122 and CFG723.

**What a₀ / Λ fix:** the mediator *range*. That is what makes the law scale-free and is exactly what the slope needs.
**What they do not fix:** the *strength*, M or m_χ. If M = E_Λ, the anchor requires m_χc² = 1.3e13 / 1.5e13 GeV (p = 5) or
5.0e6 / 5.7e6 GeV (p = 7) (canonical / alt). Each is a derived requirement, i.e. one new constant, not a prediction.

## Gate table (`ca1_self_coupling.out`)

| candidate (covariant term) | n_eff SPARC / clusters (can; alt same) | G1 can | G1 alt | G2 | G3 | G4 Kn min (can / alt) | G5 merger cm²/g (can) | G6 |
|---|---|---|---|---|---|---|---|---|
| C0 −λ\|χ\|⁴ | 0 / 0 | FAIL | FAIL | solvable | FAIL | 231 / 279 | 0.154 | ok |
| C1a Yukawa, range c²/a₀ or c/√(Gρ_Λ) | ≥ 3.94 | FAIL | FAIL | FAIL (≥ 1e62) | FAIL | — | FAIL | — |
| C1b free Yukawa (Born, classical, Hulthén) | no shape within 0.10 on both spans | FAIL | FAIL | solvable | FAIL (v★ new) | — | — | — |
| C2 p = 3, g\|χ\|²φ² | 1.333 / 1.333 | FAIL | FAIL | solvable (m_χ 1.3 GeV at λ = 1, violates G6) | FAIL | 560 / 676 | 0.0016 | m_χ ≥ 347 GeV |
| **C2 p = 5**, (1/M²) J_χ·ψ̄γψ | **0.800 / 0.800** | **PASS** | FAIL | one free scale | FAIL (best 10^−8.4) | 667 / 806 | 0.0105 | m_χ ≥ 556 GeV |
| C2 p = 6 (London, reported only) | 0.667 | FAIL | FAIL | — | — | 559 / 676 | 0.0165 | — |
| **C2 p = 7**, (1/M²)\|χ\|²(∂φ)² | **0.571 / 0.571** | FAIL | **PASS** | one free scale | FAIL (best 10^−1.0, invalid by G6) | 493 / 596 | 0.0229 | m_χ ≥ 685 GeV |
| C3 condensate | 0 | FAIL | FAIL | — | — | needs Kn < 1: FAIL | — | — |

The selected candidates pass G4 (Kn ≫ 1, as LN2 requires) and G5 (merger ≤ 0.708 cm²/g, CFG725) with wide margins.
s★(σ_ref) is 0.1545 / 0.1058 cm²/g (canonical / alt).

**Lane class: CA1 SHAPE ONLY + CA1 FOOTINGS SPLIT.** Each footing names one covariant candidate that matches n with no
velocity scale, but they are different operators. Neither footing's candidate meets the normalisation without a new
constant.

## Checks and controls

- K1: Kn through the G4 formula equals LN2's closed form (1e-16). K2: the thermal average returns n_eff = k for pure power
  laws (1e-16). K3: the Born limits are 0 and 3.79. K4: 0.11 GB, one thread, 8 s. Main run exit 0.
- **MUTATE=1** (n → n + 0.6, `_MUTATE` outputs). The C2 selection moves from [5] / [7] to [3] / [] on both footings, so it
  **BITES**; exit 1 as frozen. The selection follows the target n; it is not built in.
- **Lean 4 + Mathlib** (`CA1Certs.lean`, no `sorry`). Eight theorems use only the standard axioms (`CA1Certs.out`):
  - `contact_excluded`, `coulomb_excluded`;
  - `powerlaw_scaling` (n = 4/p);
  - `canonical_window` (p = 5 only), `alt_window` (7 ≤ p ≤ 10), `no_common_power`;
  - `pair_exchange_powers` (operator dimension gives 5 and 7);
  - `velocity_monomial`.

  `CA1Certs_MUTATE.lean` changes four statements (p = 6; 6 ≤ p; f = 2a − d; ℓ^(−2/p)), and every one fails to compile
  (exit 1, `CA1Certs_MUTATE.out`). Compile: `cd fable_independent_2026/lean_2026 && lake env lean
  ../../rebuild_2026_10_22/CA1_covariant_self_coupling/CA1Certs.lean`. Lean certifies algebra from the stated premises
  only, not the physics premises.

Run: `nice -n 10 python3 ca1_self_coupling.py` and `MUTATE=1 nice -n 10 python3 ca1_self_coupling.py`.

## Disclosures

- **PROVISIONAL, recalled from memory, nothing downloaded:**
  - the Tulin–Yu–Zurek classical fits and the Hulthén phase (C1b);
  - the pair-exchange coefficients c₃ = 1/(64π³), c₅ = c₇ = 1/(4π³);
  - which operators give which powers (p = 3 non-derivative scalar pair, p = 5 current–current fermion pair, p = 7 derivative
    scalar pair). The dimension counting behind 5 and 7 is certified; the existence and sign of each potential are not.

  These enter only C1b (whose G1 fail is a shape result), the amplitudes and the G3 menu. The menu misses are many orders
  of magnitude, far beyond any O(1) coefficient error.
- A_p (3.59 for p = 5, 3.43 for p = 7) is computed for a repulsive potential. Attractive 1/r^p with p > 2 has classical
  capture, so its O(1) coefficient differs. This does not affect the slope.
- σ_T is the momentum-transfer cross-section. G2's factor 2 covers σ_V / σ_tot and the rate × age = 1 convention.
- C2's quantum crossover sets a lower bound on m_χ (G6), not a value. A p = 5 candidate also needs light dark-energy
  *fermions*. A p = 7 candidate needs a dynamical, shift-symmetric dark-energy scalar; a pure cosmological constant has no
  quanta to exchange.
- Inherited, not re-tested: OS1's dwarf failure. A scale-free σ^(−n) cannot flatten below 20 km/s, so this lane does not
  rescue the dwarfs.

## Next (not run)

A lane with frozen criteria could pick the p = 7 derivative scalar coupling (the quintessence-like branch, alt footing) and
ask whether one constant M is shared with something already measured in the record, for example the a₀(z) drift from
CFG689. That would turn the new constant into a cross-check. The canonical footing's p = 5 needs a fermionic dark-energy
sector, which nothing in the record has.
