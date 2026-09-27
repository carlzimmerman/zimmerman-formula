# XR20 — can a₀ and Λ come from one field?

The chain's top declares P1, a₀ = κ c √(G ρ_Λ), with κ = ½ fitted (equivalently Z = 5.7888). FP5 (`a26136bc4`) found
no term of the core that ties a₀ to Λ: promoted to a free field, α = a₀/c² obeys an equation that switches MOND off
(D3), and the khronon's only background scale is K = 3H, the rival footing (D4). This lane writes five ties into the
chain's root action (FP7, the AQUAL-type repair) and varies each one. Dimensional analysis already fixes the √(Gρ) form
(FP0 C1). The only question is whether a₀ becomes a consequence of the field that sets Λ, with κ as the only coupling.

Scripts (each writes its own `.out`, `_MUTATE.out`, `_results[_MUTATE].json`):
- `XR20_a0_lambda_tie.py`: ties T1–T4 in the root action (sympy, 1+1 toys, a lattice Dirac count, SPARC).
- `XR20_evolving_de_a0z.py`: tie T5 (a quintessence-like field), its a₀(z) track and the record's a₀(z) evidence.

Nothing outside this folder was edited. **κ = ½ stays fitted; no tie here derives it. The closure target stays open.**

## The answer

**One construction ties a₀ to Λ without breaking the flat law: the Henneaux–Teitelboim unimodular multiplier (T1).**
- dΛ = 0 is a field equation there, so a₀ is exactly constant in space and time.
- It is a **tie, not a derivation**. α(Λ) = κ √(Λ/8π) is a coupling function written into the action; κ stays fitted.
- On shell it is observationally identical to P1 as declared. What it changes is the bookkeeping: a₀ and Λ are now
  one integration constant.

The four-form (T2) also ties them, but its feedback breaks the MOND scalar's health. The khronon's K (T3) is the rival
law. Sequestering (T4) gives a constant a₀ that is not tied to the observed ρ_Λ. An evolving dark energy (T5) ties a₀
to V(φ), and then the flat law holds only as far as w = −1 does.

| tie | local DOF added | FRW | PPN | local a₀ variation | a₀(z) | status |
|---|---|---|---|---|---|---|
| T1 HT unimodular | 0 (+1 global) | unchanged | unchanged | 0, exactly | flat, exactly | **TIED** |
| T2 BT four-form | 0 (+1 global) | unchanged | unchanged at 1 AU | 0.265% / 0.388% low at the RAR knee | flat | **FAILS** (health) |
| T3 khronon K | 0 | background unchanged | not established | O(0.1–1) (estimate) | ∝ H(z): +0.576 dex at z = 2.5 | **FAILS** (flat law) |
| T4 sequestering | 0 (global numbers) | keeps the residual ⟨τ⟩/4 ≤ 0 | unchanged | 0 | flat | **NOT TIED** |
| T5 quintessence, α ∝ √V | +1 scalar | GR + the field | unchanged | ≤ 3.4 × 10⁻¹¹ | tracks √V(z) | **TIED** (flat only if w = −1) |

Where two numbers appear they are canonical / alt (a₀ = 9.3603 / 11.312 × 10⁻¹¹ m s⁻²; on ρ_Λ the alt footing is
κ = 0.6043).

### T1 — Henneaux–Teitelboim: TIED, and the flat law is exact

Λ → Λ(x), plus 2Λ ∂_m T^m (the 3-form multiplier), with α = α(Λ).

- **Field equations (T1a).** The multiplier's equations are ∂_t Λ = ∂_x Λ = 0. On shell, φ's equation is the root's
  at α(Λ₀).
- **Where the MOND sector's ∂L/∂Λ goes (T1b).** Only into the unimodular clock:
  ∂_m T^m = √−g [1 − (κ²/8π) F], where F = sJ′ − J is the MOND term's α-conjugate density. The clock-rate shift is
  2.65 × 10⁻³ / 3.87 × 10⁻³ at the RAR knee and 0.48 / 0.71 at y = 100. T^m appears nowhere else, so nothing observes
  it; only its global charge, the total 4-volume conjugate to Λ₀, is physical.
- **Why this works where FP5 D3 failed.** FP5 D3 promoted α to a free field; its equation, √−g · 4σF = 0, forces
  F = 0, i.e. no MOND. In T1 the multiplier's divergence absorbs that same term. This lane re-derives D3 for the root
  and reproduces FP5's committed numbers (C1).
- **Degrees of freedom (T1c).** Lattice Dirac count: the constraints are first class, the MOND coupling generates no
  secondary constraint, and 2N − 2(N − 1) = 2 phase-space dimensions remain. That is one global degree of freedom and
  no local mode, so FP7's count of 4 is unchanged.
- **FRW and PPN (T1d).** The HT term is metric-free, so FP7 B1 (GR + Λ) and D2 (γ = 1, the khronometric α₁ and α₂)
  carry over exactly.
- **Caveat (T1e, reported).** The tie is to the HT integration constant. A matter vacuum energy moves the observed Λ
  but not a₀: Δlog a₀ = −0.023 dex at ρ_vac = 0.1 ρ_Λ. The cosmological-constant problem is now shared by a₀; it is
  no worse than for P1 as declared.

### T2 — Brown–Teitelboim four-form: tied, but the feedback FAILS health

(Z_q/2) q² replaces −2Λ, with α = β|q|. Z_q is the four-form's stiffness, not the framework's Z = 5.7888.

**Tied (T2a).** The conserved quantity is the conjugate Π = L_q = Z_q q + 4β² q F, not q. Two consequences:
- The flux amplitude cancels, α₀²/Λ₀ = 4β²/Z_q = κ²/8π, so κ is the one coupling.
- Locally, a₀_loc/a₀ = 1/(1 + (κ²/8π) F(y_loc)): the MOND sector's energy density against ρ_Λ.

**Invisible in the RAR (T2b, T2c).**

| y | a₀_loc/a₀ (can / alt) |
|---|---|
| 1 (the RAR knee) | 0.9974 / 0.9961 |
| 10 | 0.957 / 0.937 |
| 100 | 0.51 / 0.28 |

Over SPARC (3391 points, FP1's C0 statistic):
- the largest per-point shift is 0.0011 / 0.0015 dex;
- the RAR scatter moves by −0.0001 / −0.0002 dex;
- for comparison, the median per-point error is 0.037 dex and the scatter 0.108 dex.

**The fold (T2d, T2d2).** Past a point, the four-form's Legendre map q → Π at fixed Y degenerates.
- **Where.** y_fold = 6.872 / 5.654. Two independent routes agree to 2.5 × 10⁻¹⁴: the peak of the slaved scalar force
  u(y), and L_qq|_Y = 0 from 40-digit differences of J_P2 itself.
- **What happens past it.** The scalar force falls as g_N grows: u goes from 0.470 at the fold to 0.45 / 0.38 / 0.25
  at y = 20 / 50 / 100. At the switch-off y_off = 16π/κ² = 201 / 138 the flux vanishes and MOND turns off.
- **Why it is fatal.** On the whole band, C_L,eff = dy/du < 0. That is the non-monotone kernel FP7's health condition
  forbids (ν_mono was built to exclude it).
- **Checked in FP7's own quadratic form** (its committed T and V at y = 20):
  - one ω² is negative, −1.67 (ck)², and it scales with k² (Hadamard);
  - the e-fold time at k = 1/kpc is 2.5 × 10³ yr for λ = 1 and 4.9 × 10⁵ yr at FP7's σ₈ edge λ = 1.07 × 10⁷;
  - control: at fixed α both roots are positive.
- **Also on FP14's zero-knob root** (T2d3; λ = 0, with c₂ finite or → ∞, using FP14 L2's committed one-mode formulas):
  ω²/(ck)² = −1.68 at finite c₂ and −155 at c₂ → ∞ (y = 20, canonical), against +12.1 and +1120 at fixed α. FP7's T and
  V at λ = 0 reproduce FP14's formula to 10⁻⁹. The failure does not depend on the scalar's inertia or on c₂.

**Where the band sits (T2e).** This is H2b, pre-declared EXPECT FALSE, and it fell as expected.
- 7.6% / 7.7% of SPARC points at Υ = 0.7.
- A shell from 561 to 3036 AU around every solar-mass star; MOND is off inside 561 AU.
- Wide binaries (1.5 M☉) at 2–3 kAU, where a₀ is 11% / 13% low at 2 kAU.

**The fold is generic (T2f, T2g, reported).**
- The C-H core's ν_mono folds at y = 5.2 / 2.9.
- k04's own saturated kernel folds at y = 2.4 / 2.3.
- Power-law four-forms P ∝ qⁿ fold at y = 7.9 / 6.9 / 5.6 for n = 1.5 / 2 / 3.

### T3 — the khronon's K: FAILS the flat law

On FRW, K = 3 ȧ/(aN) (sympy). So a₀ = κ_K c K gives a₀(z)/a₀(0) = E(z) whatever κ_K is: 1.322, 1.791, 3.769, 8.294 at
z = 0.5, 1, 2.5, 5. That is +0.576 dex at z = 2.5, the ρ_total rival, and L37 kills it at recombination (S8b).

It is not locally constant either (T3c, reported estimate):
- the MOND term now depends on K, shifting the khronon's λ by O(c₂) at the knee and by 0.9 at y = 10;
- by CV4 K1's leaf-harmonic K, δK/K = 2κ_K² F/c₂, which is 2–17% at the knee over L340's c₂ window.
- On FP14's CMC root (c₂ → ∞, a multiplier) that estimate scales away as 1/c₂. K is then 3H(t) on every leaf, and the
  K tie is exactly the rival law with no local variation. This is a reading of the formulas, not a separate check.

### T4 — sequestering: constant, NOT TIED

The global equations give Λ_s = ⟨T⟩/4 and σ′ = λ⁴μ⁴ Vol. The Einstein equation keeps only τ_mn − (⟨τ⟩/4) g_mn, so the
vacuum energy cancels there.

- Any α of a global variable is exactly constant, so the flat law holds.
- But Λ_s = −V_vac + ⟨τ⟩/4 carries the vacuum energy (dΛ_s/dV_vac = −1).
- The kept residual is ≤ 0 for every component with w ≤ 1/3.
- The record's k02 had already closed the version built on the MOND scalar's own spacetime average: ≤ 2.3 × 10⁻⁵ ρ_Λ
  today, going to zero in the de Sitter future.

### T5 — evolving dark energy: TIED to V(φ); how a₀(z) moves against the data

A coupling function α(φ) reads the potential, and V = (ρ − p)/2 for any scalar (E1). So the field tie is neither FP0
R3b's density mapping (a₀ ∝ √ρ_DE) nor L273 Part 4's pressure mapping. It is their weighted mean.

The published fits are DESI DR2 BAO + CMB + SNe w₀wₐCDM (arXiv:2503.14738):
- DESY5 (w₀, wₐ) = (−0.752, −0.86), the representative fit;
- Pantheon+ (−0.838, −0.62);
- Union3 (−0.667, −1.09).

Δlog a₀ in dex:

| track | z = 0.5 | z = 1 | z = 2.5 |
|---|---|---|---|
| √V, DESY5 CPL | +0.058 | +0.051 | −0.034 |
| √V, Pantheon+ / Union3 CPL | +0.037 / +0.080 | +0.029 / +0.075 | −0.038 / −0.027 |
| density √ρ_DE (FP0 R3b), DESY5 | +0.025 | +0.004 | −0.099 |
| pressure (L273 P4), DESY5 | +0.095 | +0.102 | +0.030 |
| canonical thawing field, w₀ of DESY5 / Pantheon+ / Union3 | +0.064 / +0.041 / +0.087 | +0.090 / +0.057 / +0.124 | **+0.111 / +0.070 / +0.156** |
| rival a₀ ∝ H(z) | | +0.254 | +0.572 |

- **Realisability (E3).** The CPL fits cross w = −1 at z = 0.405 / 0.354 / 0.440. Beyond that point the kinetic share
  (1 + w)ρ/2 is negative, so only a ghost can follow them.
- **A healthy field (E4).** A thawing field (exponential potential, λ = 1.27 / 1.03 / 1.46) with the same w₀ has V
  falling in time, so a₀ rises monotonically into the past.
- **Local variation (E6).** The field's response to the MOND sector moves a₀ by 7 × 10⁻¹⁴ / 8 × 10⁻¹⁴ at a galaxy's
  centre and 3.1 × 10⁻¹¹ / 3.4 × 10⁻¹¹ at a cluster's. It is suppressed by (H₀r/c)².
- **Field content (E7).** One scalar is added. Around FRW the MOND term starts at O(ε³), so there is no quadratic mixing.

**Against the record's a₀(z) evidence (E5, E5b):**
- **MUSE-DARK III** (apparent +0.377 dex at z = 1; the record reads it as non-diagnostic). No track reaches it.
  - The CPL √V tracks close 8–20% of the gap.
  - The thawing fields close 15–33%; the smallest remaining gap is 0.252 dex.
  - The rival H(z) law closes 67%.
- **The deep-MOND Jeanneau refit** (Δb = +0.140 ± 0.272 at z = 1.06). Every track lies within 1σ (pulls +0.52 to
  +0.87), but each sits slightly farther than flat (+0.51), because the refit leans toward a lower a₀.
- **The z ≈ 2.5 zero point** (pre-registered ±0.13; ΛCDM's emergent scale is +0.334). The published fits through √V
  stay inside the band (−0.038 to −0.027 dex), which moves them away from ΛCDM (2.8σ against flat's 2.6σ). A healthy
  thawing field moves toward ΛCDM:
  - +0.070 to +0.156 dex at z = 2.5;
  - the separation from ΛCDM drops to 1.37σ for the Union3-matched field;
  - that field leaves the ±0.13 band, so **H5d fails on it**.

So the direction depends on the realisation:
- the phantom-crossing fits read through √V move a₀(z) slightly toward MUSE at z ≈ 1 and away from ΛCDM at z = 2.5;
- a healthy dark energy moves it toward both and can erode the z ≈ 2.5 test.

## Reading notes for other owners (flagged, not edited)

1. **FP0 R3b / L273 Part 4.** No local coupling function realises a₀ ∝ √ρ_DE. A field tie reads V = (ρ − p)/2 (E1),
   so R3b's DERIVED status rests on a density tie the action does not supply.
2. **kappa_closure/k04 F6.** Z_eff > 0 is the flux stiffness at fixed s. It does not test the slaved kernel's
   monotonicity, and under k04's own kernel the slaved boost already falls above y ≈ 2.4 (T2f).
3. **The chain's L2b** ("a₀ as a field", POSTULATED in FP5) can become **TIED** through T1. That is a coupling
   function of one integration constant, not a derivation, and κ stays fitted.
4. **The z ≈ 2.5 rotator (PAPER7).** If the dark energy is a healthy thawing field and a₀ is tied to it, the
   prediction at z = 2.5 is +0.07 to +0.16 dex, not 0.00.

## Checks

| script | main | MUTATE |
|---|---|---|
| `XR20_a0_lambda_tie.py` | 27/28, 0 load-bearing failures, **rc = 0**. The one FAIL is T2e = H2b (pre-declared EXPECT FALSE, reported). | 26/28, **rc = 1**. HEADLINE-FLAT fails: the headline tie reads K instead of the HT field, giving a₀(z)/a₀(0) = 1.32, 1.79, 3.77, 8.29, 20514 at z = 0.5, 1, 2.5, 5, 1100. |
| `XR20_evolving_de_a0z.py` | 14/16, 0 load-bearing failures, **rc = 0**. FAILs: E4b = H5c (the thawing rise exceeds the pre-declared +0.10 on two fits) and E5 = H5d (the Union3-matched thawing field leaves ±0.13), both reported. | 12/16, **rc = 1**. E-FLAT (+0.572 dex at z = 2.5) and E-MUSE (a gap of only 0.123 dex) fail when the tie reads ρ_total. |

The controls reproduce committed numbers exactly:
- **C1.** FP5 D3: minimum 9.782 × 10⁻⁴ at s = 10⁶ and deep value 0.3333, re-derived from FP5's own ν_mono.
- **C2.** FP0 R3 and FP5 D4 (1.322, 1.791, 3.769, 8.294; +0.576 dex).
- **C3.** FP5 D5 (Λ/α² = 100.531 = 32π, and 68.834), to 10⁻¹².
- **C4.** FP7's static law at one point: x_e = 0.4501, μ_T = 4.507, μ_L = 49.64.
- **C5.** k04's F3 rows, verbatim, through this lane's solver in k04's convention.
- **C6.** FP1's C0 (0.1083 dex, 175 galaxies) and FP7's 0.0370 dex over 3391 points.
- **Part 2.** FP0 R3b's 0.7956 to 10⁻¹²; L273's 14 table lines verbatim; L276's MUSE point (19σ from flat at face
  value); the Jeanneau refit's 0.51σ; L274's +0.334.

## Pre-declaration and disclosures

- **Hypotheses.** H1–H4 and H5a–H5e were written into each script's docstring before any code of the lane ran. They
  came from pencil-and-paper algebra done while planning, including H2b's fold estimate (y ≈ 7). No component probes
  were run.
- **Part 1 debug runs.** Every run wrote the lane's own output paths; only the final ordered pair (MUTATE, then main)
  is kept.
  1. MUTATE run 1 crashed at C5 on a scipy tolerance floor (brentq rtol must be ≥ 8.9 × 10⁻¹⁶), after C1–C4 had passed.
  2. MUTATE run 2 completed. Review then found that the family solver's early exit declared "switched off" whenever a
     family has two roots. That zeroed two reported numbers: the n = 1.5 peak (0.10, now 7.88) and ν_mono's u(100)
     (0.000, now 0.221). No load-bearing number changed; P2's family has one root. After this run T2d2 was added (the
     fold's consequence in FP7's quadratic form), to test the instability rather than assert it.
  3. MUTATE run 3 crashed in the numeric-identity helper: sympy's `subs` partially matched a first derivative inside a
     mixed second derivative, and the atom order depended on hash randomisation. It now does one exact `xreplace` in a
     deterministic order, and the output was verified identical under two `PYTHONHASHSEED` values.
  4. T2d2's inertia scaling (λ = 1.07 × 10⁷) and a ledger wording fix (a hard-coded 0.26% replaced by the computed
     0.265%) were added, and the ordered pair was run.
  5. FP14 (`03db97f14`, the zero-knob core: λ = 0, c₂ → ∞) landed in the chain while this lane was running. T2d3 was
     added to test the four-form's failure on that root, and the ordered pair (MUTATE, then main) was run again. These
     are the kept outputs. No earlier number changed.
- **Part 2 pre-run edits** (before any run):
  - a sloppy line in the docstring's tie paragraph was rewritten; no hypothesis text changed;
  - H5a's ±0.10 and H5c's +0.03..+0.10 became reported checks (E2b, E4b), with load-bearing checks on the
    pre-registered ±0.13 and on the direction and health of the thawing rise;
  - the thawing-field bracket was made robust.
- **Part 2 re-designation after run 1.** MUTATE run 1 showed that E5 = H5d fails on the healthy Union3-matched thawing
  field. Before the main run, E5 was re-designated reported (XR16's H-A2 precedent), with its text and thresholds
  unchanged. The verdict and ledger text, which had hard-coded "all inside ±0.13", were made data-driven.

## How it is computed

- **T1 and T2 varied.** sympy Euler–Lagrange equations on 1+1 toys with a background density √−g, using the root's
  concrete J_P2. Heavy identities are checked at random real points with exact node replacement, and FRW by
  minisuperspace.
- **Local a₀.** The root's spherical law, where P2 is exact (FP7 A2). F(y) is in closed form, with a series below
  x = 2 × 10⁻³, and matches direct quadrature to 2 × 10⁻¹².
- **The four-form family.** r(1 + εF(y/r)) = 1 is solved by bracketing on the physical branch, the first crossing
  below r = 1.
- **SPARC.** FP1's C0 statistic, verbatim, with ν replaced by the four-form's effective law (a cubic spline, 10⁻¹⁶ from
  exact solves).
- **Dirac count.** Poisson brackets on a periodic 5-site lattice.
- **T3.** The FRW K from the covariant divergence.
- **T4.** The global variations with the matter-scaling identity, checked on a scalar field.
- **T5.** The CPL fits at their central values; the bands are L273/L275's.
  - The thawing field uses the Copeland–Liddle–Wands autonomous system (dust + field, frozen at z = 30), shot to
    Ω_φ = 0.6847 and each fit's w₀.
  - The local variation is the static Green's-function response over a Hernquist galaxy (10¹¹ M☉, a = 2 kpc) and
    cluster (10¹⁴ M☉, a = 200 kpc).
  - The Jeanneau comparison uses the refit's median lever, 0.76. The lever range 0.6–1.0 moves each pull by ≤ 0.19 and
    changes no conclusion.

## Said plainly

- **T1 is the only construction that makes a₀ and Λ one field without harm, and it is a tie, not a derivation.** κ is
  a coupling, and the √Λ power is dimensional. On shell nothing observable differs from P1 as declared. The tie is to
  the HT integration constant, not to the total observed Λ.
- **T2's failure is a health failure, not a data failure.** Its RAR shift is invisible. Discs were not re-solved. The
  instability's rate depends on the MOND scalar's inertia λ and on c₂, but it is present at every value checked,
  including FP14's λ = 0 and c₂ → ∞.
- **T3's local numbers are estimates.** The khronon equation with the tie was not solved; its flat-law failure alone
  decides it.
- **T4 is a constant, not a tie.**
- **For T5, the thawing bracket is one potential shape.** The CPL fits are fits, not fields.
- **Unchanged.** κ = ½ is fitted and never derived here; the closure target stays open; the dark mass is still required.

## Reproduction

From the repository root:
```
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR20_a0_lambda_tie.py
python3 real_research/cross_thread_review_2026_09_26/XR20_a0_lambda_tie.py
MUTATE=1 python3 real_research/cross_thread_review_2026_09_26/XR20_evolving_de_a0z.py
python3 real_research/cross_thread_review_2026_09_26/XR20_evolving_de_a0z.py
```
Each run takes a few seconds on one thread.
