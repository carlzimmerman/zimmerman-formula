# AG6C: a relativistic completion of PAPER49's static action

**Verdict (frozen rule): PARTIAL.** I built one covariant, single-metric candidate in which cold energy is a genuine matter
sector, C1 ("dielectric cold dust"). It passes gates (i) lensing = dynamics, (ii) GW speed and (iii) Solar System. It passes
gate (iv)'s static-background checks across the full range 1e-4 to 1e4 a0, including deep MOND. It **fails** gate (iv)'s
general-background check H3, so (iv) fails as frozen.

The lane also leaves two **scoped no-gos** that are forced on whole classes, not only on C1:
- **NG1 (positivity).** No medium with non-negative density can reproduce L49 exactly near field null points, because L49's
  own static solution needs negative cold density there. This supplies the first new prediction (section 5).
- **NG2 (superluminality).** Any Lorentz-invariant U(1) realisation of the tether is superluminal, v² = 1 + g/a0. Its
  Lagrangian is also non-analytic on every null field.

C1 falls under CFG941's theorem D-T; it does not evade it (section 6).

Settings: κ = ½ FITTED. Both footings were used everywhere (9.3603e-11 / 1.1312e-10), never pooled. Cold energy's mass is
required, and no particle species was added. Not "theory closed"; nothing here says the data favour the framework.
- Criteria: `FROZEN_CRITERIA.md`, committed alone before any script (e926935c3).
- These results are not committed.

## 1. The action (C1)

S = ∫d⁴x √−g [ c⁴R/16πG + L_b + L_cold + L_dark ]:
- **L_cold** is a cold fluid with rest density ρ ≥ 0.
  - Its internal energy is (γ/2)ρ², an n = 1 polytrope (γ = KL*²/2).
  - It carries a charge under a massless dark U(1), coupling −qJ^μA_μ, at the BPS / extremal ratio q = √G m. At this
    ratio, like elements' dark repulsion cancels their gravity exactly.
- **L_dark** = (a0²/K) sgn X [s − ln(1+s)], with s = √(2|X|)/a0 and X = −F_μνF^μν/4. This is the exact Legendre dual of
  W_full.
- Baryons carry no dark charge, and the visible photon does not couple to the dark U(1).
- Cosmic dark-charge neutrality needs a non-clustering neutralising background. It is **not constructed** here.

What the action does:
- PAPER49's P is the dark electric displacement, P = D/K.
- ∂ₜP = −j is the Maxwell displacement-current equation, and ∇·P = ρ_c − ρ̄ is Gauss's law.
- The "critical tether" is the BPS no-force condition. The saturation wall u → a0 is a maximal displacement field.

## 2. Gate-by-gate (C1)

| gate | result | number | script |
|---|---|---|---|
| S0.1 Legendre duality | PASS (exact) | D = a0E/(a0+E); E·D − L = W_full(D) | `ag6c_s0_static.py` |
| S0.2 EL map, any geometry, γ = 0 | PASS | non-spherical test field: residual 1.2e-172 at 40 digits | same |
| S0.3 stiffness | PASS for radial P only | C1 carries γ(∇·P)²/2, not L49's curl part (differs by γ∇×∇×P) | same |
| S0.5 BPS tolerance | reported | 1% law fidelity needs \|q²/Gm² − 1\| ≤ 1.95e-4 (y = 1e-4) / 4.8e-4 (y = 6e-4); δ < 0 gives Jeans-class growth | same |
| **(i)** lensing = dynamics | **PASS** | max \|M_dyn/M_lens − 1\| = 3.4e-6 (1e8–1e14 M☉, to 100 r_M, L* = 1 kpc); line 1e-3 | `ag6c_gates_i_ii.py` |
| **(ii)** GW speed | **PASS** | no ∂h in the matter action at O(h²); \|δc/c\| ≤ 1.7e-34 at 100 Hz; light on the same cone | same |
| **(iii)** Solar System | **PASS** | PPN = GR (Einstein–Hilbert + minimal coupling); at L* = 24 pc: \|Q2\| ≤ 3.8e-8 of the Park+2026 ceiling, 1 AU pull 0.0066, Saturn monopole 0.055 of bounds | `ag6c_gate_iii.py` |
| (iii) control K | PASS | CFG770's L49 Q2 / pull / Saturn reproduced to 0 relative deviation; C1's Q2 = 0.80–0.86 × L49's | same |
| **(iv)** H1 kinetic positivity | PASS | l_X = 1/(1+s) > 0 on both branches; ρ > 0 | `ag6c_gate_iv.py` |
| H2 hyperbolicity coefficient | PASS | l_X + 2X l_XX = 1/(1+s)² > 0 | same |
| **H3 general (E, B) backgrounds** | **FAIL** | 133 / 2000 random backgrounds have \|Im ω\|/\|ω\| > 1e-6 (127 above 0.1) | same |
| H4 static backgrounds, 1e-4..1e4 a0 | PASS | coupled dust + NLED + gravity: max growth 2.6e-12 (no growing mode); linear energy positive-definite | same |

All MUTATEs bite:
- q² = 1.01 and the W_full double count break S0;
- μ = 1 removes the negative domain;
- a non-lensing response gives 0.98, and photon = dark U(1) gives a 9e11 s lead;
- L* = 1e-4 pc misses the bounds by 1.6e9×;
- in H4, a wrong-sign dark kinetic term is flagged, X − X² is gradient-class, q² = 0.99 is Jeans-class, and ρ < 0 is
  gradient-class.

**Reading H3** (disclosed diagnosis, H3c). The H3 failures are genuine, not numerical: Maxwell and a causal L(X) give real ω
to the 1e-8 noise floor. I boosted each failing background to its own rest frame (E′ ∥ B′):
- **31 are well posed there.** They fail only because the forced superluminal cone is boosted past the lab-time slices.
- **102 are ill posed in every frame.** The (E′, B′) Hessian has the wrong signature. The line (subdominant parallel field)²
  ≥ √(2|X|) (in a0 units) predicts all 133 cases exactly. The dispersion is scale-free, so Im ω ∝ |k|: a gradient
  instability.
- **Static galaxies never meet the line.** For dark fields of non-relativistic cold currents (B′ ~ (v/c)E′), the line needs
  e ≳ (c/v)²: 1e6 / 9e4 / 1e4 a0 at 300 / 1000 / 3000 km/s.

**Causality.** This is reported, not one of the four gates.
- Criterion A fails for every e > 0: v_max² = 1 + e (forced; NG2).
- The owner's criterion B holds wherever √(1+e)·v_bulk/c < 1. That is ≤ 0.334 everywhere tabulated except e = 1e4 at
  3000 km/s, where it is 1.001. It holds for realistic configurations, not by construction.

## 3. Forced vs chosen

**Forced:**
- In a single-metric, minimally coupled matter completion: c_T = c, PPN = GR, and lensing = dynamics to O(v²/c²).
- The medium's inertia is its density (the equivalence principle).
- Cancelling the medium's self-gravity needs a long-range repulsion. That means spin 1 (even spin attracts like charges),
  massless (range ≳ Mpc), with the exact BPS ratio (= D-T's c₂ = 1).
- Given U(1), L_dark is the unique Legendre dual of W_full.
- Hence (NG2) concave D(E) gives v² = (dE/dD)/(E/D) = a0/(a0 − u) = 1 + g/a0.
- The cubic (2|X|)^{3/2} term is non-analytic on the whole null cone, because both Lorentz invariants vanish on null fields.
- NG1: positivity forces the clipping at null points.

**Chosen:**
- the U(1) realisation, rather than an anchor solid (C3, considered, not run);
- the pressure form of the stiffness;
- no kinetic mixing with the photon;
- the odd continuation of L_dark to X < 0;
- L(X) without Y-dependence (L(X, Y) extensions not explored);
  - **ERRATUM (2026-10-22, doors push D9):** L(X, Y) is no longer unexplored: NG2 extends to every Lorentz-invariant L(X, Y) — the Lorentz-violation factor Λ_LV = 1 for all of them (U4a, exact), so v_max² ≥ 1 + g/a₀ and a Lorentz-invariant U(1)-dielectric parent with the enforced Gauss identity is superluminal (D9 V2). Treat L(X, Y) as covered. See `doors_push_2026_10_22/D9_uv_parent/README.md` and `MAP.md`.
- the neutralising background (unconstructed).

## 4. Candidate C2 (Blanchet–Le Tiec dipolar fluid)

H5: the NR reduction of J_μ Dξ^μ/dτ gives L = σv²/2 + Π̇·v − V. The kinetic Hessian is indefinite, and H = p_x p_Π − σp_Π²/2
+ V is linear in p_x, so it is unbounded below (an Ostrogradsky-type ghost).
- This is conditional on the BLT form, recalled from memory (PROVISIONAL; not checked against the primary text).
- L68 already closed C2 in its internal sector (the monopole has G/ε).

## 5. Scoped no-go NG1 and the first new prediction

S0.4 solves L49's own static equation for two equal masses (AQUAL, simple μ, γ = 0; `ag6c_s0_saddle.py`). Near the saddle,
it needs **negative cold density** in a thin pancake in the mid-plane (|z| ≤ 0.05d, R ≤ 0.43d).

- **Converged mid-plane values.** ρ_ph = −0.404 / −0.240 / −0.114 × √(GMa0)/(Gd²) at R = 0.1 / 0.2 / 0.3 d. This is −89 ρ̄
  (F1: 8e10 M☉ each at 0.77 Mpc) and −33 ρ̄ (F2: 2e13 M☉ each at 5 Mpc) at R = 0.2d, canonical footing.
- **The minimum itself is resolution-dependent.** It diverges weakly at the null point, as R^−0.21 (Hölder structure, cf.
  XC5). Even the coarsest run gives −79 to −232 ρ̄.
- **Cross-check.** A full simple-μ solve agrees with the deep-MOND solve within 4%.

Consequences:
1. **No medium with ρ ≥ 0 reproduces L49 there.** This holds for C1, CFG938's parent and any WEC completion. The medium is
   evacuated instead.
2. **L49 read literally as a medium with inertia ρ_c is gradient-unstable there.** (H6) ω² = ρ_c(λ_V + γk²) < 0, with
   e-fold 0.55 Gyr at k = 2π/L* and faster at larger k. This is the PAPER8 trap: the deep-MOND null points.
3. **Prediction.** Any real-medium completion has cold convergence ≥ −ρ̄ everywhere. It therefore lacks AQUAL's
   negative-phantom trough. For an edge-on mid-plane line of sight, the unsuppliable column is −1.9 / −2.1 M☉/pc² for the
   MW–M31-like pair and −4.6 / −5.1 M☉/pc² for the cluster pair (canonical / alt). Detectability was not assessed, and no
   data were used.

Secondary prediction (unmeasurable): slip M_dyn/M_lens − 1 = −3e-6 for clusters (dark tension).

## 6. Relation to CFG938 and theorem D-T (coordinator's overlap notice)

**CFG938** (covariant fluid-EFT parent, CONDITIONAL):
- Same skeleton: cold dust in one metric, P as the electric part of the current's 2-form, the tether as the medium's own
  gravity.
- CFG938 carries u with a **non-propagating** potential χ (D²χ = Kmn, multiplier λ). Its P is therefore curl-free, and it
  is exact only for spherical systems.
- C1 replaces (χ, λ) by a **propagating** U(1) whose Gauss law sources D = ε(E)E. That makes the match to L49 exact in every
  geometry at γ = 0 (S0.2).
- The price is NG2 and the H3 backgrounds. CFG938's elliptic χ avoids them but needs a preferred frame (forced there:
  "rest frame = cosmic frame"; cf. PAPER9).
- C1's polytrope stiffness inherits CFG938 S2d's and AG6D's early-universe exclusion unless it switches on late.

**Theorem D-T (CFG941):** C1 falls under it, and does not evade it.
- C1 has an always-on tether on a cold static medium whose phantom is its own mass. BPS q = √G m is c₂ = 1; S0.5 quantifies
  the tolerance (≤ 2e-4).
- So C1 has no linear self-gravity of the tethered medium. H4's longitudinal restoring force → 0 in deep MOND: neutral, not
  unstable.
- It also has no gravity between tethered components (BPS no-force), so the satellite hover / EFE problem and the
  suppressed growth apply. I did not recompute the growth exponent for C1.
- A medium-frame dispersive dielectric (polarisation with its own inertia) would plausibly remove NG2 and the null-cone
  singularity. It is not built here. It would still fall under D-T.
- I did not touch CFG944–947.

## 7. Files, commands, disclosures

All commands are run as `OMP_NUM_THREADS=1 nice -n 10 python3 <script>`; the whole set takes 68 s with peak RSS 0.38 GB.

| script (sha256 prefix) | output | exit code |
|---|---|---|
| `ag6c_s0_static.py` (c2cf9ade1413) | `ag6c_s0_static.out` | 0 |
| `ag6c_s0_saddle.py` (8918d5d28a66) | `ag6c_s0_saddle.out` | 0 |
| `ag6c_gates_i_ii.py` (ed9dc7814498) | `ag6c_gates_i_ii.out` | 0 |
| `ag6c_gate_iii.py` (be6584eaf490) | `ag6c_gate_iii.out` | 0 |
| `ag6c_gate_iv.py` (021db7b75952) | `ag6c_gate_iv.out` | 1 (H3, the finding) |

- MUTATE runs: `AG6C_MUTATE=1` for the first four scripts; `AG6C_MUTATE=a|b|c|d` for gate iv. Each writes `_MUTATE*`
  outputs and exits 1 by design.
- Results JSONs are alongside.

Disclosures (all fixes were made before the final runs; earlier outputs are kept):
- **S0.2.** The first run used float inputs, which capped the test at about 1e-16 against a 1e-20 line. It now uses rationals
  (`*_firstrun_floatinputs.out`).
- **S0.4, first run.** Plummer b = 0.04 gave a 3% mass deficit that broke the frozen 1% control. There was also a 2/3 error in
  the mirror and axis gradient (`*_firstrun_softening_mirrorgrad.out`).
- **S0.4, second run.** The resolution check I had added (not a frozen check) failed on C_min. That check was restated as the
  column plus fixed radii; C_min is reported as a bound (`*_secondrun_Cmin_unconverged.out`).
- **Gate iv.** The K-H3 line was moved from 1e-8 to 1e-6 because 1e-8 is the noise floor. H3c, H3b and the K-H3 control are
  disclosed additions. H4's MUTATE classifier was fixed twice: a k-independent growth masked case d, and a missing absolute
  floor misread roundoff in case c.
- **Not verified:**
  - BLT's exact covariant form;
  - detectability of the saddle trough;
  - C1's cosmology (neutralising background, BBN, growth exponent, ΔN_eff from dark photons);
  - L(X, Y) or dispersive repairs of H3.
    - **ERRATUM (2026-10-22, doors push D9):** L(X, Y) is no longer unexplored: NG2 extends to every Lorentz-invariant L(X, Y) — the Lorentz-violation factor Λ_LV = 1 for all of them (U4a, exact), so v_max² ≥ 1 + g/a₀ and a Lorentz-invariant U(1)-dielectric parent with the enforced Gauss identity is superluminal (D9 V2). Treat L(X, Y) as covered. See `doors_push_2026_10_22/D9_uv_parent/README.md` and `MAP.md`.

κ = ½ FITTED; cold energy's mass required; not theory closed.
