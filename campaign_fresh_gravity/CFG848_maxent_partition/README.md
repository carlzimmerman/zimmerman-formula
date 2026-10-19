# CFG848: the maximum-entropy partition of tethered and free cold energy. WRONG SIGN (dSph-like) / ILL-POSED (elliptical-like); no concentrated free core in any cell

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in cf0aad80f, before any script existed. The script is
`cfg848_maxent.py` (single core, `nice -n 19`, under 1 GB; main about 4 min, MUTATE about 2 min).
- Main run: exit 0, because K1, K2, K3 and the K3 pre-statement check pass. Output `cfg848.out`, `cfg848_results.json`.
- `CFG848_MUTATE=1` (tether removed: one ordinary Newtonian species): exit 1, because it bites. Output `cfg848_MUTATE.out`,
  `cfg848_results_MUTATE.json`.

κ = ½ is FITTED. Both footings are scored separately and never pooled. No dark-matter particle species is added: the cold
energy's mass is still required, and its amount (5.364 × the catchment baryons) is an input. This is not "theory closed", and
nothing here says the data favour the framework over ΛCDM.

## The question

Codex's reciprocal two-population functional (`real_research/analytic_review_2026_10_18_codex/KINETIC_PARTITION.md`) has
tethered cold mass (it feels the tether, and the tether responds to tethered mass only) and free cold mass (all mass gravitates).
Codex selects neither the free fraction f nor the temperature. This lane asks: in the fully relaxed state (maximum
non-degenerate Lynden-Bell entropy, one common β, fixed catchment stock 5.364 N M_b, fixed total energy, a reflecting sphere at
the record's turnaround radius), what is f(r)? Does relaxation put the cold energy into a concentrated free core, an excess over
the law at g_bar ≈ 1e-12 m/s², with no new constant? If it did, relaxation (structure, not colour) would predict the record's
empirical rule (excess only in gas-poor, pressure-supported systems: dSphs +0.44 dex, red lenses +0.20 dex).

Units G = a0 = M_b = 1. Hernquist baryons (a point baryon makes the Boltzmann density non-integrable). t ⇌ f conversion is
allowed (chemical equilibrium), which extends Codex's functional, since Codex conserves the populations separately. The graded
number is Δ(r_g) = log10[M_dyn/M_dyn,law] at g_bar = 0.01 a0.

## Verdict (primary cells: R = r_ta, E = E_INF, N = 10)

| system | footing | class | Δ(r_g) at r_ta | Δ(r_g) at R_fill (truncation bracket) |
|---|---|---|---|---|
| P1 dSph-like (10^6.5 M_⊙, a = 3 r_M; r_ta = 681 / 749 r_M) | can | **WRONG SIGN** | −1.026 | −0.745 (same class) |
| P1 | alt | **WRONG SIGN** | −1.020 | −0.745 (same class) |
| P2 elliptical-like (10^10.5 M_⊙, a = 0.3 r_M; r_ta = 147 / 161 r_M) | can | **ILL-POSED (a)**: no local entropy maximum at E_INF | none | −0.621 (a maximum exists there) |
| P2 | alt | **ILL-POSED (a)** | none | −0.621 |

**Lane reading.** No cell, in any declared bracket, gives a positive excess at r_g. Where the relaxed state exists, it is a large
deficit (the cold energy evaporates into the catchment volume). Where it does not exist, the free component collapses into the
baryon core without bound (gravothermal: the mean-field entropy is unbounded). Maximum-entropy relaxation of this functional does
not produce a concentrated free core of sensible amplitude. It therefore does not derive the empirical relaxed/gas-poor rule. No
new constant was introduced. No energy choice on the stable branch would rescue it (see the turning-point diagnostic below).

## Key numbers

**The relaxed state, P1 canonical, R = r_ta.** β = 28.9, so σ² = 0.069 × (V_f²/2). The cold mass inside r_g is 0.0176 M_b,
against the law's 4.9 M_b. The free fraction profile is nearly flat and rises gently inward:

| r | local f_free | enclosed F(<r) |
|---|---|---|
| 3.5 | 0.783 | 0.786 |
| 7.0 (r_g) | 0.781 | 0.784 |
| 14 | 0.780 | 0.782 |
| 341 (R/2) | 0.731 | 0.750 |

f_free(r_g) − f_free(R/2) = 0.050, which just meets the "rising inward" condition. It is moot, because Δ is negative.

**Analytic pre-statement, confirmed.** Φ_t − Φ_f = ∫_r^∞ (M_t/s² + M_t²/s⁴) ds > 0 at every radius, and it decreases outward. So
in every extremum the free fraction exceeds ½ and rises inward. The minimum over all computed model-C extrema is +0.0207 (K3b).
In this functional the free label is the lower-energy state at every radius, so relaxation with conversion makes about ¾ of the
stock free. Once that happens, nothing holds the profile on the law.

**Energy window.** Local maxima exist only for E ≥ E_turn, the first turning point of the linear series:

| box | E_turn | E_INF | E_LAW |
|---|---|---|---|
| P1, r_ta, can | −0.443 | −0.117 | −1.864 |
| P1, r_ta, alt | −0.238 | −0.107 | −1.864 |
| P1, R_fill | −14.71 | −1.154 | −1.864 |
| P2, r_ta, can | +6.678 | −0.538 | −3.352 |
| P2, r_ta, alt | +7.390 | −0.491 | −3.352 |
| P2, R_fill | −9.74 | −1.312 | −3.352 |

- Relaxing an already settled law halo (E_LAW) has no maximum in any r_ta box.
- In the R_fill box, E_LAW does have a maximum, with Δ(r_g) = −0.732 (P1) and −0.573 (P2).
- For P2 (a deep baryon well) the stable branch ends at positive energy, at β = 4.34 (can) and 4.46 (alt).

**Turning-point diagnostic (not graded, added after the graded result).** This is the most concentrated state that is still a
local maximum.
- r_ta boxes: Δ(r_g) = −0.985 (P1 can), −0.995 (P1 alt), −1.005 / −1.013 (P2), −1.00 / −1.01 (N = 5.6).
- R_fill boxes: +0.084 (P1), −0.289 (P2).

So no energy on the stable branch reaches the 0.15 dex window. An excess would need a state past the turning point, which is
unstable.

**Brackets (reported; by the frozen rule they do not change the class).**
- N = 5.6: both systems are ILL-POSED (a) (P1 E_turn +0.239 > E_INF −0.079). P1's class is therefore N-dependent: WRONG SIGN at
  N = 10, no maximum at N = 5.6. Disclosed.
- E_LAW: no maximum at r_ta. At R_fill it is a deficit, as above.

**Diagnostic, no conversion (NC: all tethered, populations conserved as in Codex), at E_INF.**
- P1: M_t(r_g) = 0.76 of the law, Δ(r_g) = −0.11 dex (can and alt).
- P2: 0.50 / 0.48 of the law, Δ(r_g) = −0.27 / −0.28 dex. Δ(r_h) = −0.007 there, because the inner core stays pinned.

Relaxation without conversion keeps the inner tethered profile near the law but short, with no excess.

**The tether is dynamically almost irrelevant in the relaxed profile.** The MUTATE turning-point states (one ordinary species)
have the same Δ(r_g) as the main model to about 0.01 dex (−0.979 vs −0.985 for P1 can). The tether matters through the energy
budget: the tethered initial stock has no self-gravity, so E_INF sits above the stable-branch minimum for P1. The same ordinary
stock at rest is below it everywhere.

## Controls

- **K1 (law limit, NC model, P1 can box): PASS.**
  - At β = 2e4: M_t(r_g)/M_law = 0.99930, and E = −1.86028 vs E_LAW = −1.86439 (0.22%).
  - E_LAW is at or below every NC series energy: the law is the all-tethered ground state.
- **K2 (Antonov): PASS.** Λ = 0.3346 at density contrast 708.6.
- **K3 (Codex identity): PASS.** sympy gives σ_f² − σ_t² = f²GM_b/3r + fV_f²/2 exactly, and both Jeans residuals are 0.
- **K3b (pre-statement): PASS.** min(Φ_t − Φ_f) = 0.0207 > 0.
- **MUTATE (tether removed, each model's own E_INF): every cell ILL-POSED (a).** An ordinary cold stock at rest inside R lies
  below the Antonov-type limit. It bites, because P1's class differs from the main run.

## Deviations, all disclosed

1. **Hot end.** The frozen text says the series is "stepped up from p = 0.05". Model C's hot end is at p ≈ ln ½, because half
   the stock is free at high temperature. The series starts at its hot end.
2. **Continuation.** Fixed-p stepping was replaced by pseudo-arclength continuation in (p, ln β, ℓ_t), and the turning point is
   refined by a bounded minimisation of E along the arc. Both changes were made during control testing (K2 first gave contrast
   754 without the refinement; the NC shooting stalled). They were made before the final run. A development test of the P1
   primary cell, run with the arclength code, had already shown its result. The final run reproduces it identically.
3. **K1 solver.** Outward shooting of the NC model stalls at β ≈ 128. The pinned law is an outward-unstable manifold, the
   same mechanism as Codex's outward saddle.
   - The large-β part of K1 uses an independent solver: damped Newton on the convex NC free energy on a radial grid (`nc_grid`,
     N = 1600). It was cross-validated against the shooting at β = 20, 40, 55 (E agrees to about 1e-6).
   - It was written after the P1 primary result had been seen. It enters no graded cell.
   - K1 is evaluated at β = 2e4, consistent with the frozen "largest β reached (target ≥ 1e3)".
4. **NC diagnostic.** The ungraded NC state at E_INF is located with `nc_grid`, because the shooting cannot reach it. This
   was a post-result implementation fix. The JSON's shooting-only NC entries read "not reached (solver failure)"; the `nc_grid`
   entry is the diagnostic.
5. **Turning-point diagnostic.** Added after the graded result. Not graded.
6. LSODA prints step-size warnings to the console. They are not in the .out files and do not affect any converged state: every
   reported state has residuals below 1e-8.

## Limitations

- Spherical, isotropic and mean-field.
- Codex's deep-cubic, zero-stiffness force is used at all r, including inside r_M.
- The truncation is a reflecting box. Baryons are fixed.
- The receiver that a conversion channel needs is not modelled.
- Real violent relaxation is incomplete. This lane tests only its ideal maximum-entropy endpoint, so an excess from incomplete
  or history-dependent relaxation is not excluded here.
- Stability is judged by linear series only. Bifurcations off the series and disconnected branches are not searched.
- P1 and P2 are two representative systems, not samples.
- Nothing here derives κ or 5.364.

**Implication for the empirical rule.** If the excess is real bound cold mass, its concentration has to come from a
non-equilibrium, history-dependent process, or from a conversion law with its own receiver. The ideal relaxed endpoint of this
functional points the other way.

κ = ½ fitted; cold energy mass required; no dark-matter particle species added; not theory closed.
