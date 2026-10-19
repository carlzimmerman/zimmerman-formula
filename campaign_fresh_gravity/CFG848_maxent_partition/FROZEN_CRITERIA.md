# CFG848 FROZEN CRITERIA: the maximum-entropy partition of tethered and free cold energy (before any script)

**Source.** Path 1 of the 2026-10-19 review of Codex's work (`real_research/analytic_review_2026_10_18_codex/`, read as data:
KINETIC_PARTITION.md, README.md, finite_halo_2026_10_18/, warm_radial_2026_10_18/, smooth_exact_2026_10_18/). Codex built a
reciprocal two-population energy functional (tethered cold mass feels the tether and the tether responds to tethered mass only;
all mass gravitates), a constant-fraction Jeans family, the impossibility of equal dispersions for f > 0, and an outward-saddle
of a constant fraction. Codex selects neither the fraction nor the temperature.

**Question.** In the fully relaxed (maximum-entropy, Lynden-Bell-type) state of Codex's own functional, with one common inverse
temperature β, a fixed total catchment cold stock, a fixed total energy and a truncation at the turnaround radius, what is the
free fraction profile f(r)? Does relaxation put cold energy into a concentrated free component in the inner galaxy (an excess
over the law at low g_bar) with no new constant?

**Why.** The record (CFG828, CFG829, CFG840, CFG845, CFG846; THEORY_CANONICAL_2026-10-18.md) shows an empirical rule: the excess
over the law appears only in gas-poor, pressure-supported systems (satellite dSphs +0.44 dex, red lenses +0.20 dex at
g_bar < 1e-12 m/s²); discs and gas-rich systems sit on the law. If relaxation converts tethered into concentrated free cold
energy, structure (relaxed vs unrelaxed), not colour, would carry the excess.

**Record check (done before freezing).** Lynden-Bell / maximum entropy was used before for amplitude or temperature only:
CFG461 C1a/C1b (Lynden-Bell temperature fails the c-test; in a box the SIS is the unstable centre of the Emden spiral, not a
maximum; Antonov λ = −0.3346 at contrast 708.6 reproduced); CFG497 B6 (degenerate Lynden-Bell "not formulable" without a
phase-space cap, i.e. a particle mass); CFG550 (b) (Lynden-Bell T as a Lagrange multiplier: posited, too hot); CFG637 Method B
(non-degenerate Lynden-Bell = lowered Maxwellian bounded at r_ta, temperature from the infall energy) and CFG781 (Method B did
not converge). CFG130/155: the f(E) of the law's target is not a Lynden-Bell extremum. No lane has asked for the maximum-entropy
PARTITION between tethered and free populations. No prior no-go covers it; CFG461's Antonov result is a warning that a
maximum may not exist.

## Units and functional (Codex's, unchanged except the declared baryon profile)
Units G = a0 = M_b = 1, so r_M = √(GM_b/a0) = 1, A = √(a0 M_b/G) = 1, V_f² = √(G M_b a0) = 1; energies in M_b V_f².

E = K_t + K_f + ∫Φ_b d(M_t + M_f) − ½∫₀^∞ [(M_t + M_f)² − M_t²]/r² dr + ⅓∫₀^∞ M_t³/r⁴ dr.

- Forces (Codex): a_t = −(M_b(r) + M_f)/r² + M_t²/r⁴, a_f = −(M_b(r) + M_t + M_f)/r².
- Mean-field potentials Φ_i = (1/4πr²) δU/δρ_i, zero at infinity:
  Φ_t(r) = −∫_r^∞ [(M_b + M_f)/s² − M_t²/s⁴] ds,  Φ_f(r) = −∫_r^∞ (M_b + M_t + M_f)/s² ds.
- **Baryons: Hernquist sphere** M_b(r) = r²/(r + a)², Φ_b = −1/(r + a). Declared regularisation: for a point baryon the
  Boltzmann density ∝ exp(β/r) is not integrable at r → 0, so the maximum-entropy problem is ill-posed for Codex's point mass.
  Codex's own regular warm populations (BOUNDARY_MATCHING.md) also use smooth baryons. a is the galaxy's observed baryonic
  scale, not a new constant of the theory.
- The model's law: the all-tethered at-rest state has zero tethered force, M_law(r) = r √M_b(r) = r²/(r + a), i.e.
  g_law = g_b + √(a0 g_b) (deep cubic, zero stiffness; Codex's force dictionary, used at all r, a declared limitation).

## Entropy and constraints
- **Entropy: non-degenerate Lynden-Bell (Boltzmann form)** S = −Σ_i ∫ F_i (ln F_i − 1) d³x d³v. Why: the catchment cold stock
  starts at rest, so its fine-grained phase-space density is unbounded; Lynden-Bell's degeneracy cap is then infinite and his
  entropy reduces exactly to this form. No particle mass enters (consistent with CFG497 B6 and CFG637 Method B).
- t and f are two internal states of one carrier: equal inertial mass, equal statistical weight, no internal energy offset (the
  functional has none; an offset would be a new constant).
- **PRIMARY model C (conversion allowed):** only the total stock M_t + M_f = M_c is fixed; the extremum is chemical
  equilibrium t ⇌ f (one common μ). This extends Codex's functional, which conserves the populations separately; the
  charge-carrying receiver a literal conversion needs is not modelled. The lane tests the thermodynamic endpoint only.
- Fixed total energy E = E_target. Support inside a reflecting sphere r ≤ R (Antonov / Lynden-Bell & Wood 1968 convention).
- Extremum: ρ_i(r) = λ exp[−β Φ_i(r)], one β and one λ for both labels; σ² = 1/β for both.
- **Analytic pre-statement (from Codex's forces, before any script):** Φ_t(r) − Φ_f(r) = ∫_r^∞ [M_t/s² + M_t²/s⁴] ds > 0, and it
  decreases outward. So in every model-C extremum ρ_f/ρ_t = exp[β(Φ_t − Φ_f)] > 1 at every radius and rises inward: the free
  fraction exceeds ½ everywhere and rises inward. The numerics decide existence of a local maximum at E_target, the amplitude
  and the excess over the law.

## Inputs (all from the record or the galaxy; none fitted here)
- Cold stock M_c = 5.364 N M_b, N = 1/f_ret. PRIMARY N = 10 (CFG804 bin 1; CFG823's dSph value). Bracket N = 5.6 (CFG804 bin 4).
- Systems: **P1 dSph-like** M_b = 10^6.5 M_⊙, a = 3 r_M (3D half-mass r_h = 2.414 a = 7.2 r_M, g_bar(r_h) ≈ 0.01 a0);
  **P2 elliptical-like (red lens)** M_b = 10^10.5 M_⊙, a = 0.3 r_M.
- **Truncation R.** PRIMARY R = r_ta, the catchment turnaround radius with the record's machinery:
  r_ta = [3 M_ta / (4π Δ_ta ρ̄_m0)]^{1/3}, M_ta = N M_b / f_b (CFG804 fixed point M_ta = M_b/(f_ret f_b); f_b = 1/6.364),
  Δ_ta(z = 0) = 11.8308 (CFG654 N0, cfg654_delta_ta.json), ρ̄_m0 = Ω_m 3H0²/(8πG) with declared H0 = 67.4 km/s/Mpc,
  Ω_m = 0.315 (r_ta ∝ (Ω_m H0²)^{-1/3}). Hand estimate r_ta ≈ 680 r_M (P1) and ≈ 147 r_M (P2), canonical; ×1.10 alt; the
  script prints the exact values. **Bracket R = R_fill**, the supply edge where the law exhausts the stock:
  R_fill √M_b(R_fill) = M_c (≈ 57 r_M for P1, ≈ 54 r_M for P2 at N = 10).
- **Energy.** PRIMARY E_INF = energy of the stock at rest, uniform inside R, all tethered (the energy collisionless infall from
  turnaround delivers; cold energy arrives tethered, the record's default; CFG637 Method B convention). Bracket (reported, not
  graded) E_LAW = energy of the at-rest law state (all tethered, M_t = r √M_b(r) up to R_fill, constant beyond; K = 0).
- Both footings (a0 = 9.3603e-11 canonical, 1.1312e-10 alt) separately; they differ only through r_ta / r_M. Never pooled.

## Numerical method
- Series of extrema at fixed (M_c, R, a), parameter p = ln[ρ_f(0)/ρ̄], ρ̄ = 3M_c/(4πR³), stepped up from 0.05 by continuation.
  At each p solve (M_t(R) + M_f(R) = M_c; ln ρ_t(0) + βΦ_t(0) = ln ρ_f(0) + βΦ_f(0)) for (β, ln ρ_t(0)) with scipy root, using
  Φ_i(0) = Φ_i(R) − ψ_i(R), Φ_t(R) = −1/(R + a) − F/R + T²/(3R³), Φ_f(R) = −1/(R + a) − (T + F)/R (T, F the totals).
  ODEs in s = ln r from r_in = 1e-6 min(a, 1) to R (solve_ivp, LSODA, rtol ≤ 1e-9), central series start.
- E = (3/2) M_c/β + U; U from the functional, with the exterior part −½(F² + 2TF)/R + T³/(9R³) in closed form.
- **Local maximum = stable branch** by the method of linear series (Katz 1978; Padmanabhan 1990), microcanonical: the hot end
  is a maximum; stability is lost at the first turning point of E along the series (first local minimum of E(p)). The relaxed
  state is the stable-branch extremum with E = E_target (bracketed root, refined). If E_target lies below every stable-branch
  energy, no local maximum exists at E_target. Bifurcations off the series are not searched (limitation).
- The series stops at p = 60 or on solver failure; if neither E_target nor a turning point is reached, that cell is
  "not reached" and counts as ILL-POSED (numerical), disclosed.
- Single core, nice -n 19, < 1 GB RAM. Script cfg848_maxent.py → cfg848.out, cfg848_results.json; MUTATE →
  cfg848_MUTATE.out, cfg848_results_MUTATE.json.

## Graded quantities
- Δ(r) = log10{[M_b(r) + M_t(r) + M_f(r)] / [M_b(r) + M_law(r)]} (total dynamical mass over the model's law).
- r_g: where g_bar = M_b(r)/r² = 0.01 a0 (≈ 1e-12 m/s², the record's threshold): r_g = 10 − a, i.e. 7.0 (P1), 9.7 (P2).
  Also reported: Δ at r_h = 2.414 a, 0.5 r_g, 2 r_g; f_free(r) = ρ_f/(ρ_t + ρ_f); enclosed F(<r) = M_f/(M_t + M_f); σ²/(V_f²/2).

## Classes (per PRIMARY cell: R = r_ta, E = E_INF, N = 10; each footing)
Applied in this order:
1. **ILL-POSED (a)** no local entropy maximum at E_target on the stable branch (or "not reached").
2. **OVERSHOOT** Δ(r_g) > 0.80 dex (relaxation concentrates far beyond the observed +0.2 to +0.44 dex).
3. **CONCENTRATED FREE CORE** 0.15 ≤ Δ(r_g) ≤ 0.80 dex AND f_free(r_g) − f_free(R/2) ≥ 0.05 (free fraction rising inward).
4. **INTERMEDIATE** 0.05 ≤ Δ(r_g) < 0.15, or Δ(r_g) in the window of 3 without f rising inward.
5. **NO FREE EXCESS** −0.05 < Δ(r_g) < 0.05, or f_free(r_g) < 0.05.
6. **WRONG SIGN** Δ(r_g) ≤ −0.05 dex.
7. **ILL-POSED (b)** if the class at R = R_fill (same E_INF convention, N = 10) differs from the class at R = r_ta, the answer
   needs a free truncation: the cell is ILL-POSED (truncation-dependent), both classes reported.
- Lane headline per system: canonical-footing class, alt reported (FOOTING-DEPENDENT if they differ). One headline if P1 and P2
  agree. The N = 5.6 and E_LAW brackets are reported and do not change the class (any disagreement disclosed).
- **New constant:** none may be introduced. If a pass appears only for an R or E outside the declared brackets, it is recorded
  as needing a new constant, not as a pass.

## Controls
- **K1 (law limit; conversion forbidden, all tethered, model NC)**, P1 primary box: at the largest β reached (target ≥ 1e3)
  |M_t(r_g)/M_law(r_g) − 1| < 0.02 and |E − E_LAW| < 0.02 |E_LAW|; and E_LAW ≤ every NC series energy (the law is the
  all-tethered ground state).
- **K2 (Antonov)**: baryons off, tether off, one species in a box: microcanonical turning point Λ = −ER/(GM²) within 0.002
  of 0.3346 and centre/edge density contrast in [690, 730].
- **K3 (Codex identity and the pre-statement)**: sympy from the isotropic Jeans equations with Codex's constant-f forces gives
  σ_f² − σ_t² = f²GM_b/(3r) + fV_f²/2 exactly; and min_r [Φ_t − Φ_f] > 0 on every computed model-C extremum.
- Main exit 0 only if K1–K3 pass.
- **Diagnostic (not graded):** the NC maximum-entropy state at E_INF for each primary cell (does relaxation without conversion
  keep the law?).
- **MUTATE** (CFG848_MUTATE=1, separate outputs): tether removed, i.e. all cold stock is ordinary one-species Newtonian mass (no
  cancellation, no cubic push), same baryons, M_c and R, E_target = that model's own E_INF (uniform at rest). It bites if, in at
  least one primary cell, its class differs from MAIN or |Δ_MUT(r_g) − Δ_MAIN(r_g)| ≥ 0.05 dex; MUTATE exits 1 if it bites. If
  it does not bite, that is reported as "the tether is dynamically irrelevant in the relaxed state".

## Limitations declared now
Spherical, isotropic, mean-field; Codex's deep-cubic zero-stiffness force at all r (not the full interpolation inside r_M);
reflecting truncation; baryons fixed; the conversion channel's receiver is not modelled; real violent relaxation is incomplete
(the maximum-entropy state is its ideal limit); stability by linear series only. Nothing here derives κ or 5.364.

κ = ½ fitted; cold energy mass required; no dark-matter particle species added; not theory closed. No claim that data favour the
framework over ΛCDM.
