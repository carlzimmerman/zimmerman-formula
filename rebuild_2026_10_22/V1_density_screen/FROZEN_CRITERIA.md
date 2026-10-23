# V1_density_screen: can a well-posed, one-constant, potential-type density screen replace γ_L / L★? FROZEN CRITERIA

Written and committed before the lane script exists and before any lane number. Rules: `rebuild_2026_10_22/BRIEF.md`,
`doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md`. κ = ½ is FITTED. Footings canonical a₀ = 9.36e-11 m/s² and alt
a₀ = 1.13e-10 m/s² (record values 9.3603e-11 / 1.1312e-10 where a reused lane uses them), never pooled. No dark-matter
particle. Never "theory closed"; nothing here says the data favour the framework. Final verdict words: PASS / CONDITIONAL /
NO-GO for "a well-posed one-constant density screen replaces γ_L". The assumption ledger is `ASSUMPTION_LEDGER.md`
(committed with this file).

## 0. The owner's request, what was read, and the not-blind statement

Request (verbatim): "open a lane testing a well-posed density-type screen that replaces gamma_L/L* one-for-one (no extra
constant): Cassini, outer globulars, dwarfs, WB prediction, and well-posedness at saddles."

Read before freezing: `covariant_push_2026_10_22/THEORY_V3_DRAFT.md`; `rebuild_2026_10_22/H4_v3_saddle_stability/`
(README, ledger, results json); `doors_push_2026_10_22/D10_native_Lstar/` (README, script, solver, results json);
`D7c_q2_rar_gate/README.md`; `D7d_screened_q2/` (README, script inputs, solver); `E2_field_equation/README.md` and its
R2 code; `rebuild_2026_10_22/S1_v3_hosted_small/` (README, CSV, script statistic); `P4_v3_galaxy_tiles/` (README, solver,
T1 and T4 code, results json); `F1_cluster_cores/` results json; `STANDING.md` L700–790 (the screening squeeze:
potential-keyed screening has the wrong ordering, density-keyed screening screens stars and not gas, Hui–Nicolis–Stubbs);
`prep_2026/sigma_spread/MG_ZERO.md` (C5: chameleon G_eff is a function of x); `prep_2026/gaia_dr4_prep/
NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md` (read only; nothing under `prep_2026/gaia_dr4_prep/` is edited).

**Not blind.** Before this file:
1. Plumbing prototypes (scratch, not committed, no fit and no S_95 / S_C computed): a uniform-S wrapper of D10's
   Solver2D reproduces D10's stored AQUAL and Newton σ_p for Pal 4 at two Υ nodes exactly, and gives σ_p at S = 0.5, 0.1
   for those two nodes; a uniform-S wrapper of D7d's Route N reproduces D7d's AQUAL Q₂ at the BN11 inputs on grid G1
   (3.935e-26) and gives Q₂ at S = 0.5, 0.2 on G1 at the BN11 inputs only (≈ 0.46 and 0.18 of the S = 1 value).
2. Hand reasoning (nothing run): (i) a scalar whose effective potential restores it toward its ambient value obeys a
   maximum principle outside a compact body, so the body's screened zone ends within a few body radii (the Sun cannot
   screen r_M ≈ 0.04 pc or Saturn); (ii) thin-shell-screened stars carry a ψ-charge bounded by their "capacitance"
   4πM²R★, so a stellar system made of screened stars is transparent to ψ; (iii) in the linear regime a body is screened
   only if its central Newtonian potential (including its host's) is comparable to a star's surface potential GM★/R★,
   while stars stay unscreened only if M² ≳ M★/(4πR★): together these make screening potential-keyed, and Pal 4's
   potential is far below the Sun's surface potential; (iv) the screen's own fifth force and the MOND sector's back-reaction
   on ψ are controlled by the same ratio v²/M², in opposite directions. I expect a NO-GO or at best a CONDITIONAL. These
   estimates set no threshold below; every number in the verdict comes from the committed script.

## 1. The screen (the action), the insertion point and the constants

v3 (THEORY_V3_DRAFT §1) with the stiffness removed, γ_L → 0, and its P sector (the J term — the only part of the action
that produces the MOND response, C4/E2) multiplied by s(ψ) = ψ², plus a symmetron-type scalar ψ coupled to the matter
trace through the Jordan-frame factor A(ψ):

  L/√−g = R/(4K) + ψ²[P^μA_μ − W(K|P|)] + μ_K²(Q−1)²/(2K) − (v²/2)[(∂ψ)² + (μ_ψ²/2)(ψ² − 1)²],  matter on Ã g, A = 1 + v²ψ²/(2M²),

K = 4πG. Weak-field PN form (H4 A1 with the P sector multiplied, γ_L = 0):
L = −|∇φ|²/(2K) − ρ_m φ + ψ²[P·∇Ξ − W(K|P|)] + μ_K²Ξ²/(2K) − (v²/2)[(∇ψ)² − ψ̇² + (μ_ψ²/2)(ψ²−1)²] − ρ_m c² v²ψ²/(2M²).

Insertion point (justification, to be checked in Part A): (a) at s = 1 it is v3 at γ_L = 0, i.e. AQUAL μ = x/(1+x)
exactly (the law is untouched); (b) at s = 0 the static limit is Newton exactly and GR + BS dust (the growth sector and the
tensor modes) are untouched; (c) it is a single multiplicative insertion; for uniform s the static equation is
AQUAL with μ_S(x) = 1 − s(1 − μ(x)) = 1 − s/(1+x). The alternative insertion a₀ → s·a₀ is noted in the ledger; every
structural result of Part B concerns ψ's dynamics and is insertion-independent.

Constants of the screen: ρ_* = μ_ψ²M² (critical density; **the one constant swapped for L★**), λ_C = 1/μ_ψ (vacuum Compton
length), and v²/M² (fifth-force and back-reaction strength). Uniform medium: ψ² = max(0, 1 − ρ/ρ_*), so s = 1 − ρ/ρ_* below
ρ_* and 0 above. The owner allows one constant. λ_C and v²/M² must be shown to decouple from every tested verdict or to be
tied to a₀, c, G, Λ with no freedom; otherwise the count is reported as ≥ 2 and plainly.

## 2. Checks and results (script prints `ID PASS/FAIL value threshold`; exit 0 iff all checks PASS)

Results lines (R*) are reported, not pass/fail; verdict lines (V*) apply the rules of §3.

**Part A — sympy, exact (residuals identically 0):**
- A1: uniform s: eliminating P from the PN Lagrangian gives ∇·[μ_S ∇φ] = Kρ_m with μ_S = 1 − s/(1+x); s = 1 → μ = x/(1+x);
  s = 0 → μ_S = 1.
- A2: ψ's static equation divided by v² is v-independent at zero back-reaction: ∇²ψ = μ_ψ²ψ(ψ² − 1) + (ρ/M²)ψ; the uniform
  solution is ψ² = 1 − ρ/ρ_* (ρ < ρ_*), 0 (ρ ≥ ρ_*); the back-reaction term is −(2/v²)ψ L_P⁰ (L_P⁰ = on-shell P·∇φ − W) and
  the fifth-force acceleration is −c²(v²/2M²)∇ψ².
- A3: the exterior comparison function: for ρ = ρ_a < ρ_* outside a body of radius R with 0 ≤ ψ(R) ≤ ψ_a, u = ψ_a − ψ obeys
  ∇²u ≥ 0 (subharmonic), hence u(r) ≤ u(R)·R/r and 1 − s(r)/s_a ≤ 2R/r.
- A4 (dispersion, S = ψ², γ_L = 0, μ_K and ψ mixing kept, 1D WKB along P̄, H4's first-order background term kept): the
  3×3 (δφ, δσ, δψ) quadratic form; with zero mixing det = 0 gives ω² = ρ_τ[k²/χ_S − K], χ_S = s k²/(K M_θ) + μ_K²/K,
  ρ_τ = s D·P + μ_K²(Q̄−1)/K; at s = 1 this is H4's γ_L = 0 relation; lim_{k→∞} ω² is finite for every s > 0.
- A5 (bracketing): with the mixing c ≠ 0 the low-frequency root obeys |ω²| ≤ |b/a| (b/a the uncoupled khronon value) for
  every k when ρ_τ < 0 (proof by the sign of the quadratic at 0 and at b/a).

**Part B — regimes of the screen (numerical symmetron BVP, dimensionless, own 1D radial solver):**
- B1 (exterior bound): for a uniform-density body (R = 1) in an ambient s_a ∈ {0.3, 0.9}, both linear and thin-shell
  cases (ρ_body/M² · R² ∈ {0.1, 10, 1e3}), the solved ψ obeys u(r) ≤ ψ_a R/r at every r ≥ R to 1e-6 (PASS line).
- B2 (thin-shell charge): the exterior charge fraction q = (r·u(r) at r = 30R, Yukawa removed)/(linear prediction) falls
  below 0.1 when ρ_body R²/M² ≥ 100 (PASS line); reported for the grid.
- R-B3 (Regime A, stars linear: ρ_*λ_C² ≥ M★/(4πR★), surface criterion, Sun as the reference star): the necessary
  condition for a body to reach s ≤ s_t is |Φ_N,c| ≥ (1 − √s_t)·GM★/R★ (linear theory, Yukawa dropped: favourable to
  screening), Φ_N,c the body's central Newtonian potential including its host's. Reported for Pal 4, Pal 14, NGC 2419
  (Υ_V = 1.6 and the P1 +2σ end, MW brackets E_lo/E_mid/E_hi of D10) at s_t = S_95 (Part C), and for the Sun's ambient
  (MW baryons, D10 Hernquist brackets and P4's McMillan17 Newtonian potential at R₀) at s_t = S_pl and S_C (Part D).
  Shortfall factor = required/available.
- R-B4 (Regime B, stars thin-shell: ρ_*λ_C² < M★/(4πR★)): a gas-free stellar system's ψ-charge ≤ N★·4πM²R★; the GC
  self-screening requirement N★R★/a ≥ (1 − √S_95) is reported as a shortfall factor; then the GC can be screened only by
  its ambient diffuse (gas) density.

**Part C — the one-constant fit to the outer globulars (D10's data and statistic, reused read-only):**
- Same clusters (NGC 2419, Pal 4, Pal 14 primary; Pal 3 reported), same likelihood tables (D10 json `lik_tables`,
  binaries f_b = 0.3, e_c), same Υ priors P1/P2/P3, same E-P estimator, same MW brackets E_lo/E_mid/E_hi, both footings:
  18 cells. Parameter: a common uniform screening level S_GC ∈ [0, 1] at the clusters (s at the cluster site), solved with
  D10's Solver2D at L★ = 0 with the phantom flux multiplied by S. Grid S ∈ {0, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1}.
  Two field treatments: (F-D10) D10's MW field law; (F-S) self-consistent, the MW halo at the same uniform S
  (g μ_S(g) = g_N, Hernquist brackets). χ²(S) = −2 Σ lnL; S_95 = largest S with χ²(S) − min_S χ² ≤ 3.84 (linear in S).
- C1 PASS iff S = 1 reproduces D10's stored AQUAL σ_p and S = 0 its Newton σ_p, both to ≤ 1e-6 relative, on every stored
  (footing, bracket, cluster, Υ) node used.
- C2 PASS iff the S = 1 and S = 0 χ² columns reproduce D10's band-cell Δχ²_AQUAL and Δχ²_Newton (relative to D10's own
  minimum over its L★ grid) to ≤ 0.01 in all 18 cells (same machinery check).
- R-C3: S_95 per cell, both treatments; the fit "exists in a regime" iff that regime can reach s ≤ S_95 at the GC sites.

**Part D — (a) Cassini Q₂ and planets (the screen's s at the Sun):**
- Q₂(S) from D7d's Route N at L★ = 0 with the phantom rows multiplied by S, D7d's fields E0–E3 (total field fixed at the
  measured value), Richardson G1/G2, S ∈ {1, 0.3, 0.15}, both footings; BN11/Hees sign.
- D1 PASS iff S = 1 reproduces D7d's K4 BN11 AQUAL value (3.8181e-26, Richardson) to ≤ 1e-3 and S = 0 gives Q₂ = 0.
- D2 PASS iff S = 1 at E0–E3 agrees with E2's R1 AQUAL values (canonical 2.200, 3.127, 3.557, 4.097 e-26 and the alt row
  from E2's json) to ≤ 3 %.
- R-D3: S_C = largest S passing Hees 2σ [−3e-27, 9e-27] at all four fields (linear interpolation in S between solved
  points; Q₂ monotone in S checked), per footing; also the Park band [−2.0e-27, 5.2e-27].
- R-D4: planets: anomalous sunward acceleration at uniform s, from g μ_S(g) = g_N at Earth / Mars / Saturn, against D7d's
  bounds (8.7e-15, 1.4e-15, 7.0e-15 m/s²); S_pl = largest s passing all three.
- Scoring (V-a): in each regime, s_Sun = the smallest s the regime allows at the Sun (Part B); PASS iff s_Sun ≤ min(S_C, S_pl).

**Part E — (b) dwarfs:**
- E1 PASS iff a uniform-S wrapper at S = 1 reproduces S1's per-system `logG_emb0` (E-W, central y, E_mid) to ≤ 1e-6 on
  every system of both footings.
- R-E2: the screen's satellite prediction in the regime where the fit exists: MW satellites with d_host ≤ R_GC(Pal 4)
  = 104.05 kpc at s = S_95 (most favourable value allowed by the fit if the halo's visible density does not rise outward:
  ledger premise P-mono), at s = 0 (strict symmetric phase); others at s = 1 (no γ_L in this theory). Variant: M31
  satellites treated like MW ones. Statistic: median over systems of S1's central per-system Δ = log(g_obs/g_bar) − logG
  (central values; S1's MC bootstrap is not rerun); Δ_shift = new − v3, where v3 is the same statistic on S1's
  `Delta_v3_Lfloor` column. Field dwarfs (host "field") are reported only.
- Scoring (V-b): PASS iff |Δ_shift| ≤ 0.05 dex on both footings in the fit's regime; FAIL otherwise. "Newly screened"
  systems (s < 0.9 where v3 had none) are counted.

**Part F — (c) wide binaries at 20 kAU:**
- γ_v(S) for a 1+1 M☉ circular binary, orientation-averaged (3-point Gauss–Legendre in cos θ, as E2), from the linear EFE
  response of μ_S at the frozen PREREG fields (primary 1.778e-10, alternative 2.078e-10 m/s²), anchored to E2's nonlinear
  AQUAL value at S = 1: γ_v(S) − 1 = (γ_lin(S) − 1)·(γ_E2 − 1)/(γ_lin(1) − 1). F1 PASS iff γ_lin(1) is within 0.02 of
  E2's γ_v (anchoring error disclosed). R-F2: γ_v − 1 at the s_Sun of each regime, against DR4's registered readings
  (Arm A floor 1.1614 / 1.1917; medium-first 1.000). No pass line (prediction). Nothing in `prep_2026/gaia_dr4_prep/` is
  written.

**Part G — (d) guard: the SPARC RAR (P4's T1 statistic):**
- G1 PASS iff this lane's loader + P4's iso_perUps statistic (one Υ per galaxy on P4's UPS grid, eV weights, isolated
  algebraic law) reproduces P4's rms and median Υ (0.05409 / 0.52 canonical, 0.05372 / 0.44 alt) to ≤ 1e-4 / exactly.
- R-G2: the same statistic with the uniform-s law (g μ_S(g) = g_N) at s = S_95 and s = 0 (the configuration implied by a
  visible halo, as the fit needs for the MW).
- R-G3 (thin slab): P4's axisymmetric AQUAL solver with s = 0 inside |z| < z_s and s = 1 outside, for two exponential
  discs (Σ₀ = 3 Σ_M and 0.3 Σ_M, R_d = 1, z_s = 0.1 R_d and 0.3 R_d, isolated), both footings; in-plane shift
  Δlog g(R) at R = 0.5–6 R_d against the s = 1 solve on the same grid.
- Scoring (V-d): PASS iff the configuration the fit implies keeps rms ≤ P4's + 0.010 dex and median Υ within 0.05 of P4's
  on both footings; CONDITIONAL iff the slab-only configuration passes (max |Δlog g| ≤ 0.01 dex) but the halo-screened one
  fails and which one applies rests on an unmeasured input (circumgalactic gas); FAIL iff both fail.

**Part H — (e) well-posedness:**
- H1 (numeric, A4's dispersion with the mixing, ρ_τ < 0, s ∈ {1, 0.5, 0.1, 0.01}, μ_K ∈ {0, 1}, mixing c ∈ {0, 1, 10}):
  Γ_max(k) over k ∈ [1e-3, 1e8] (units 1/ℓ): PASS iff Γ_max(1e8)/Γ_max(1e5) ≤ 1.01 (bounded) in every case and
  Γ_max ≤ √|b/a|·(1 + 1e-6) (A5).
- H2 (mutate target): the same scan with H4's γ_L term restored gives Γ_max(1e8)/Γ_max(1e5) ∈ [900, 1100] (unbounded,
  reproduces H4). PASS iff so.
- R-H3: e-folds on H4's regions (read-only json: median |ρ_τ|, x_median, T): N = Γ·T with Γ = √(K|ρ_τ|((1+x)² − s)) at
  s = 1 (must equal H4's N_bounded to ≤ 1e-6: check H3) and s = 0. R-H4: the Sun's would-be phantom in the Galactic field
  without γ_L (D·P = ∇·[(1−μ(|g|))g]/K, g = Newtonian Sun + uniform x_e = 1.15, 2.6): min D·P, the rate, N over 4.6 Gyr and
  over 60 Myr, with the s-scaling of its metric coupling stated. R-H5: symmetron tachyonic rate (c/λ_C)√(1 − ρ/ρ_*).
- Scoring (V-e): ILL-POSED iff any Γ_max grows with k without bound; BOUNDED iff growing modes exist with a k-independent
  cap; HEALTHY iff none.

**Part I — constants and (f):**
- I1 (λ_C decoupling): PASS iff every tested verdict (GC fit exists, Sun screened, satellites screened, SPARC) is the same in
  Regime A and Regime B. FAIL means λ_C does not decouple.
- I2 (v²/M² window): at the screening transition the fit implies (MW halo at R ≥ R_GC(Pal 4), x from the MW law there):
  back-reaction ratio ≤ 0.1 needs ΔΦ_5 = c²v²/(2M²) ≥ 10|L_P⁰|/ρ_*; the fifth-force allowance is ΔΦ_5 ≤ 0.1·2|Φ_N(R_s)|
  (strict) and ≤ (300 km/s)² (generous). The window exists iff ρ_*(= ρ_gas at the transition) ≥ 10|L_P⁰|/allowance; the
  implied gas mass inside R_s (monotone premise) is compared with the MW baryon mass (6e10, E_hi). PASS iff the implied mass
  ≤ M_b under the generous allowance on both footings.
- R-I3 (f): only if the fit's regime changes them: MW K_z(R₀, 1.1 kpc) and v_c(R₀) at uniform s = S_95 and 0 (P4 solver,
  McMillan17 baryons; data 66.4 ± 2.2 M☉/pc² and Eilers v_c), cluster cores (F1's Newtonian-baryon A_MID 9.82 ± 0.63
  read-only if the ICM is screened).
- K-RSS: peak RSS < 1 GB (parent and every child).

## 3. Verdict rules (applied mechanically by the script)

- Count line: ONE CONSTANT iff I1 and I2 PASS; otherwise "≥ 2 constants" (named).
- Fit line: the fit EXISTS in a regime iff that regime allows s ≤ S_95 at the three primary GC sites in every cell of the
  P1 central band (E_mid) on both footings.
- **PASS**: one constant, the fit exists, V-a PASS, V-b PASS, V-d PASS, V-e not ILL-POSED.
- **CONDITIONAL**: one constant, the fit exists, V-e not ILL-POSED, and V-a/V-b/V-d pass only under a named unmeasured input.
- **NO-GO**: otherwise. The README states which legs fail and why, and which v3 failures the screen does not touch
  (dust sector: satellites under T3, clusters, growth).

## 4. Mutation

`--mutate` moves the insertion point: s multiplies the whole gravitational response (source and phantom) instead of the
phantom alone, in every wrapper (GC solver, Q₂ rows, RAR law, dispersion), and drops nothing else. C1 (S = 0 Newton), D1
(S = 0 → Q₂ = 0) and G1-type limits must FAIL; H2 is replaced by the γ_L-restored scan, which must read unbounded.
Outputs `v1_density_screen_MUTATE.out`, `v1_density_screen_results_MUTATE.json`. The mutate run does validations only.

## 5. Compute

`OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, single thread, minutes; no PM; no downloads; heavy queue untouched; record
scripts imported read-only (D10 solver, D7d solver, P4 solver), record json read-only.
