# DH1_dark_energy_heater: can a dark-energy-keyed term heat the cold sector to ~600 km/s with no knob?

Criteria: `FROZEN_CRITERIA.md` + `ASSUMPTION_LEDGER.md` (7ca9858740, committed alone, before any script or number). No
amendment. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. The cold component is cold dark energy
(a gravitating field component, w ≈ 0; never matter, never a particle). No knob fitted or scanned. Not "theory closed".
Nothing here says the data favour the framework or ΛCDM. Every number is from `dh1_derive.out` / `dh1_results.json`.

## Verdict (frozen classes): **OBSTRUCTION**, both footings

No candidate passes G1 (knob), G2 (time), G3 (kinetic) and G4 (split) together. Every candidate fails at least two gates,
for derived reasons. The obstruction is four statements:

1. **A homogeneous drive cannot heat a cold collisionless sheet (D3, K2).** Dark-energy quantities are uniform in space
   (Λ exactly; a dynamical DE up to matter-sourced perturbations, which act like rescaled gravity). In the Hamiltonian
   H = A(t)p²/2 + B(t)x·p + C(t)·x + Φ, the drive enters only ∂²H/∂p² and ∂²H/∂x∂p. Those terms rescale and shift the
   sheet. The fold source ∂²H/∂x² is Φ'' alone. So a single-stream medium stays single-stream: the fine-grained dispersion
   stays zero. Numerically, a 1-D sheet under a random drive has 0 folds and zero momentum spread; a cos well folds it
   (2531 folds). A per-mass "heat" source is not Hamiltonian, so it is not an action term at all.
2. **On systems gravity has already mixed, the drive only rescales: heating ∝ σ², so c_s = A(t)σ, r = 1 (D4).** SPARC needs
   A ≥ 2.695 / 2.856 (c_s,need over σ = 70.5 km/s). KT clusters allow A ≤ 1.424 / 1.472 (X26 sheet over σ = 517.1 km/s).
   The two ranges do not overlap. X26 excluded the r = 1 line at every c_* (JSON `any = false`, both footings).
3. **The natural dark-energy clock is too shallow (D1, D2).** A heater ∝ d(ρ_DE/ρ_m)/dt gives u = (3/5)εc²f exactly, so
   c_s ∝ a^1.5 and X22's p = 2, the same background law as X24b (its 1/5 is reproduced). At c_s,need today this gives
   c_s(z = 3 / 2) = 23.75 / 36.57 km/s against the edge 5.94 / 12.19 (canonical). It still fails with the record's
   native DE drift (CFG689 sqrtX 0.909: 21.3 / 33.5 km/s) and at the most forgiving normalisation (11.4 / 17.6). Reaching
   p ≥ 3 needs S ∝ f^n with n ≥ 5/3, which is a chosen exponent. A step trigger at a knob-free epoch passes timing. But
   those epochs are z(ä = 0) = 0.632 and z(Ω_Λ = Ω_m) = 0.296, and the Milgrom crossing a₀ = cH/2π (κ = ½) lies in the
   future (z = −0.27). A step still has to release a latent energy, and statement 1 blocks it.
4. **The amplitude is a fitted number.** With c and dark-energy ratios only, the natural specific energy is O(c²): ε = 1
   gives a cosmic c_s of 2.8e5 km/s, and ρ_Λc²/ρ_c per unit mass is 2.58 c². The window needs ε = 1.1e-7 to 1.4e-6
   (canonical) or 2.2e-7 to 9.2e-7 (alt). That is X24b's ε problem in a different key, not a derived value.

**Escapes it leaves open (not dark-energy-keyed, not knob-free):**
- a stochastic non-gravitational force with its own length ℓ well below the system scale. The dark-energy sector's only
  lengths are c/H₀ ≈ 4.45 Gpc and c²/a₀ ≈ 31 / 26 Gpc, and L★ ≥ 21.7 / 22.9 pc is a lower bound, not a value;
- a collisional channel, which R6 and the Bullet exclude.

**Even a working heater lands on excluded ground (inherited, not regraded):**
- every end state that meets the cluster terciles has c_s/σ_KT = 1.075–1.424 (canonical) or 1.150–1.472 (alt). X30's
  OUTER band fails all those sheet points (Z −5.4 to −11);
- X32's collisionless reading at those c_s is EXCLUDED in all four combinations (that lane's verdict is UNDECIDED on its
  K4).

## Per candidate (canonical; alt is the same in class except H6 G4)

| id | heater | G1 knob | G2 time | G3 kinetic | G4 split | G5 |
|---|---|---|---|---|---|---|
| H1 | ε c² d(ρ_DE/ρ_m)/dt per unit mass | FAIL (ε 1.1e-7–1.4e-6) | FAIL (p = 2) | FAIL (D3; not Hamiltonian) | not decisive: cosmic C 91–329 km/s (alt 131–268), only under the most forgiving bound/cosmic heat ratio β ∈ [1, 5] | reduces to X24b's background law |
| H1L | same with local ρ_m | FAIL | PASS | FAIL: it cools during collapse and is zero once virialised | FAIL: SPARC c_s = σ = 70.5 < 190 | X24b's local θ/3 sign |
| H2 | coherent coupled-DE drive (anti-friction) | FAIL (coupling β) | PASS (sheet stays cold) | FAIL (D3, D4: rescales only) | FAIL (r = 1; A ≥ 2.70 vs ≤ 1.42) | distinct; lands on X26's excluded virial line |
| H3 | step at ä = 0 / Ω_Λ = Ω_m / a₀ = cH/2π | FAIL (latent energy) | PASS (z 0.63 / 0.30 / future) | FAIL (D3) | FAIL (rescale ⇒ r = 1; shift ⇒ no dispersion) | distinct |
| H4 | a₀-triggered phase change (g < a₀) | FAIL | FAIL: the cosmic medium sits at x_rms 0.041 / 0.055 at z = 2 / 3 (alt 0.034 / 0.046), so the key fires before z = 2 | FAIL (uniform trigger region, D3) | FAIL: X22, x does not separate C from SPARC | with Λ, a₀ is constant: there is no a₀ epoch |
| H5 | wave-field excitation at rate ≤ 3H | FAIL (D) | PASS | FAIL: v ≤ 2√(3v_f H₀/k_f) = 31.1 / 32.1 km/s vs need 176.5 / 188.6 (SPARC quadrature) | FAIL (×5.7 / ×5.9 short) | bounded by the forest itself |
| H6 | random kick field, σ² = σ_well² + v_k² | FAIL (v_k, ℓ) | PASS | FAIL (no length in the DE sector) | canonical OPEN, v_k 204–329 km/s; alt FAIL (293 > 268); approximate (A9) | additive floor; its cluster c_s/σ falls in X30's failing range |

**Why each candidate escapes the closed forms, or does not.**
- H1 differs from X24b in its spatial key (q = 0, not −1) but has the identical background time law, so it fails the
  forest the same way. This answers the brief's example directly: a rate ∝ d(ρ_DE/ρ_m)/dt is X24b in time.
- H2 and H3 are structurally new (multiplicative, or a step). They fail on kinematics (statements 1–2), not on X23's or X24b's
  grounds.
- H4's key is the acceleration key that X22 and X19 already found does not separate.
- H5 is the only truly kinetic channel, and the forest bounds it about ×6 below the need.
- H6 is outside X26's multiplicative family. Its canonical window is open in the approximate reading, but it needs two
  knobs and a length the dark-energy sector does not have.

## Step 0 and checks (7/7 PASS, exit 0; MUTATE exit 1 as frozen)

| check | result |
|---|---|
| K0a X22 p = 2 / 3 rows under this lane's Jeans mapping c_s ∝ a^(p + 1 − d/2), d = 3 | max dev 2.8e-17; c_s,need 190.014 / 201.315 |
| K0b X26 σ medians, KT c_s range, virial line | 70.5 / 517.1; 555.9–736.1 / 594.6–761.4; any = false |
| K0c X29 survivors | 23 / 15; cosmic C₀ cap 328.8 / 267.9 km/s |
| K0d X35 read-back of CFG689 sqrtX(2.33) | 0.9094 / 0.9498 |
| K1 sympy D1–D5 | all True |
| K2 cold sheet: drive vs well | 0 folds, spread 0 / 2531 folds |
| K3 RSS | 0.09 GB |

**MUTATE** (`DH1_MUTATE=1`, outputs `*_MUTATE.*`):
- m1 sets the cooling exponent to 1, m2 dilutes matter as a⁻², m3 gives the drive a cos x term;
- K0a fails (dev 8.1e-2), K1 fails (D1, D2, D3), K2 fails (1846 folds);
- verdict UNDECIDED, exit 1.

## What this does not show

- **No N-body and no profile.** The inherited X30 / X32 classes are quoted, not regraded with the H6 σ-dependence.
- **G4 uses medians** (A8). H1's and H6's G4 windows are approximate (A9) and carry no weight in the verdict, which rests on
  G1–G3.
- **The trigger epochs use PROVISIONAL Ω_m = 0.315** (from memory). They are reported only. G2's PASS for a step holds at any
  z_t < 2.
- **The obstruction covers dark-energy-keyed, knob-free, collisionless heating only.** A heater with a new constant
  (a length ℓ and a velocity v_k), or a collisional one, is outside it. So is any change to the galaxy law itself.
- **The dwarf floor c₀ is not addressed** (separate lane).

## Run

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/DH1_dark_energy_heater/dh1_derive.py               # exit 0, < 5 s, 0.09 GB
PYTHONHASHSEED=0 DH1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/DH1_dark_energy_heater/dh1_derive.py  # exit 1 by design
```

Read-only inputs, with SHA-256 in the JSON:
- X22's JSON;
- X26's JSON and `.out`;
- X29's JSON;
- X35's JSON.
