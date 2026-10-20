# CFG938: the cold-energy medium as a relativistic continuum

**Lane label: COVARIANT PARENT CONDITIONAL.** A fluid EFT of comoving label fields gives a covariant parent of canonical
S2 in its longitudinal sector (exact for spherical systems):
- static limit = the law to 2.2e-16;
- ∇_μT^{μν} = 0;
- isotropic FRW background with w = 0 and no tether background;
- linearly well-posed: ω² ≥ 0, which cures CFG660's √k growth;
- slip ≤ 1.5e-5.

These hold under five conditions. There are also three flags of equal weight: C3 FAIL is inherited; there is no linear
self-gravity of the tethered medium (D2); and there is no gravity between tethered components (differential free fall).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (7a0d41e8b), block CFG930–939.
- **Settings:** κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy's mass required; no particle
  species added; not "theory closed"; nothing here says the data favour the framework.
- **Main text:** `DERIVATION.md`. Script: `cfg938.py` (sympy + small numpy/scipy). One process, peak RSS 0.15 GB, about
  7 s, with an RSS guard at 1 GB.
  - `CFG938_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg938.py` → `cfg938_K.out`, `cfg938_results_K.json`. Exit 0.
  - `CFG938_MUTATE=1 …` → `cfg938_MUTATE.out`, `cfg938_results_MUTATE.json`. Exit 1 by design (all teeth bite).
  - `OMP_NUM_THREADS=1 nice -n 10 python3 cfg938.py` → `cfg938.out`, `cfg938_results.json`. Exit 0 (all 30 checks pass).
  - Run 1 is kept: `cfg938_firstrun_S3efail.*`. It had a numerical integrator bug, disclosed as A1.
- **Inputs (read only):** the record's SPARC file for NGC 3198 (Υ = 0.61); `CFG4_common.A0` (footings); CFG847's five
  systems; declared cosmological inputs for the early-universe number (Ω_b 0.0493, Ω_c/Ω_b 5.364, H₀ 67.4,
  T_CMB 2.7255 K, N_eff 3.046). Nothing was downloaded. No other lane's files were edited.

## The derived action

  S = ∫√−g [ c⁴R/16πG − mc²n − W_full(u) − (3γ/4K²) τ_μν τ^μν + λ(D_μD^μχ − K m n) ] + S_b,

with:
- u² = h^{μν}∂_μχ∂_νχ;
- τ_μν the traceless medium-frame tidal tensor of χ;
- W_full(u) = [−a₀u − a₀² ln(1 − u/a₀)]/K;
- γ = KL*²/2.

Its static weak-field limit is S2 with ∇·P = δρ_c, because K P_L = ∇χ and P·∇Φ = −δρ_cΦ + div.

## Results

| item | result | check |
|---|---|---|
| K1 SPARC reduction (NGC 3198, 43 radii) | max \|g/g_law − 1\| = 2.2e-16 both footings (line 1e-6) | K1 |
| K2 FRW | ρ = m/a³, p = 0, w = 0 exactly; stress isotropic | K2 |
| K3 Newtonian limit | √−g(−mc²n) = −ρc² − ρΦ; Ψ drops out | K3 |
| what P is | electric part of the 2-form with J = ∂·Q; ∇·P = ρ − ρ̄ and ∂ₜP_L = −j_L exact; linear P = −ρ̄ξ | S2a |
| tether | the medium's minimal gravitational coupling: **forced** | S2b |
| W(K\|P\|) | not a strain function, not local (enclosed mass) → extra structure forced; u = \|Dχ\|, χ the medium's own potential | S2c |
| stiffness | (γ/2)δρ_c² for a fluid; local EoS form BBN-excluded if the medium exists then (ratio 1.3e3–2.3e6 at z = 4e8); χ-tidal form background-free | S2d |
| why no anisotropy | fluid stress always isotropic; solid needs shear strain; P ≡ 0 and tether scalars ≡ 0 on FRW | S1 |
| static stress | p_r = −W, p_t = p_r + D u/K: **exactly CFG660's field-aligned stress** | S3c |
| settling | no drift in the ideal action; drift = overdamped tether force (ατ = τ_d R′); books close with E_W + heat (CFG932 omitted E_W) | S3d, S3e |
| slip | worst s_∇ 5.8e-6, s_847 1.54e-5 (≤ 1.9e-5; ≪ 1e-2) | S4 |
| dispersion | ω² = γρ₀k² + Kρ₀[R′cos²θ + (R/u)sin²θ] ≥ 0; Im ω = 0 at all k (CFG660: ∝ √k) | S5a, S5b |
| inertia | positive iff ρ_c c² > D(u)u/K; margin 5.9e4–2.5e8 on CFG847 systems | S5c |
| growth flag | tethered medium feels baryons only: δ ∝ a^0.61 vs class A a¹; T2x pass does not transfer | S6 |
| tethered–tethered gravity | ⟨L⟩_ID = πGB(B + 2C₁ + 2C₂)/k²: no C₁C₂ term → differential free fall in host-medium fields (0.03–0.17 a₀ at 50–250 kpc) | S8 |

**MUTATE:**
- M1: no tether → Newton exactly (g = g_N), and K1 fails (law deviation 0.83 / 0.84).
- M2: γ → −γ → gradient instability, Im ω ∝ k (slope 1.0000).
- M3: W_rem in place of W_full → K1 fails (1.6 / 1.9).

All teeth bite.

## CFG678 scorecard (20 gates)

| status | gates |
|---|---|
| PASS | A5, C2 |
| CONDITIONAL | A1, A2, B3, C1 |
| FAIL | C3 |
| NOT DECIDED | C4 |
| PENDING | D3 |
| UNTESTED | A3, A4, A6, B1, B2, D1, D2 (D2 with the a^0.61 flag) |
| DECLARED | A7, E1, E2, E3 |

Per-gate sources are in DERIVATION §8. Relative to CFG678's specification for the next action: **B3/A2 move from FAIL to
CONDITIONAL**, B1 stays unpassed, C3 stays FAIL, and D2 is newly flagged for this parent.

## Reading

1. The "P thing" has a covariant home. P is the electric part of the 2-form potential of the medium's conserved current.
   The tether is just the medium's gravity. The record's field-aligned stress (CFG660) is the stress tensor of the
   tether sector, and the action makes it well-posed.
2. The price is one non-propagating extra field (the medium's own potential χ, plus a multiplier). It is forced because
   u = K|P| is an enclosed-mass quantity that no strain function can express.
3. **Particle in disguise: yes, for the mass** (F = −mc²n is cold matter). The tether sector is not a particle.
4. The same structure that makes the law the medium's equilibrium also removes the medium's gravity on tethered medium.
   - **(a)** Linear growth is suppressed (a D2 problem for this parent).
   - **(b)** A satellite's tethered medium does not feel its host's medium.

   Both follow from S2 + ID itself (CFG888, astra's audit §4), not from the covariantisation. Each needs its own test.

## Disclosures

These are in full in DERIVATION §11:
- **A1:** the S3e integrator step fix (run 1 kept).
- **A2:** S8 was added during scoring. It corrected my own over-generous C1 draft; the flag text was fixed to the
  computed numbers.
- K, MUTATE and main were rerun from the final script.
