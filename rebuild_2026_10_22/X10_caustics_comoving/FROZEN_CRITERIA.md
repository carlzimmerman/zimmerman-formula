# X10_caustics_comoving: with a co-moving khronon start, do X8's soft-side folds persist, and does a focal line form behind each moving mass? FROZEN CRITERIA

Written and committed (with `ASSUMPTION_LEDGER.md`) before any lane script exists and before any script of this lane has
produced a number. Rules: `rebuild_2026_10_22/BRIEF.md`, `doors_push_2026_10_22/BRIEF.md` + `BRIEF_E_AUDIT.md`. Lane launched
by the coordinator from X8's open items ("a co-moving start"; "O1's wake line cannot be separated from the at-rest start
transient"), V3_FULL_PICTURE §6 rows "Soft-side caustics in v3s" and "Dynamical state of moving subsystems". κ = ½ is
FITTED. Footings canonical a₀ = 9.3603e-11 m/s² and alt a₀ = 1.1312e-10 m/s², never pooled. No dark-matter particle. Never
"theory closed"; nothing here says the data favour the framework. Small jobs only: `OMP_NUM_THREADS=1 nice -n 15`,
< 1 GB RSS, each run ≤ 30 min (checkpoint/resume), at most three at once; the heavy queue and every other lane untouched;
no downloads.

## 0. What was read before freezing, and the not-blind statement

Read: `rebuild_2026_10_22/BRIEF.md`; X8 (README, FROZEN_CRITERIA + A1–A3, ASSUMPTION_LEDGER, `x8_core.py`, `x8_run.py`,
`x8_batch.py`, `x8_aggregate.py`, `x8_validate.py`); O1 README (§3(ii), the downstream focal line); H5 README (A2 Galilean
covariance, A3 steady response, A5 Danby–Camm); U1 README part (b) (the capture law); V3_FULL_PICTURE §1, §2, §6.

**Not blind.** I know X8's results: soft threshold events in all 6 O2 cases (t_c 14.16–16.50 Gyr, converged h 10/5), O1
t_i 9 NO-CAUSTIC, O1 t_i 3/6 unconverged, frozen reading UNDECIDED because N-dt moved the canonical O2 t_i 3 fold by
0.221 Gyr; positive halos fold within t_i + 0.5–2.1 Gyr after the v = 0 start; D-FOLLOW MW 0.51–0.76.

Scoping numbers computed before this freeze (no evolution of any co-moving state was run):
- **Capture radii** from the orbit formulas of `x8_core.py` (r_cap = 2GM_b/V_g², V_g the galaxy's speed at t_i in the
  barycentre frame; MW / M31, kpc): O2 (all t_i, V 68.8 / 41.2 km/s) 109 / 506; O1 t_i 3 (V 74.8 / 44.9) 92 / 427; O1 t_i 6
  (V 28.6 / 17.2) 631 / 2922; O1 t_i 9 (V 4.9 / 2.9) 21646 / 100214. Separations r(t_i): O2 1995 / 1657 / 1320; O1 745 / 988
  / 1045. Apocentre of O1 at t = 8.548 Gyr.
- **Soft-lobe extent**, read from X8's committed-run final arrays at h = 20 (`X8/work/*_h20.final.npz`, deconvolved particle
  signs, so approximate): a disc around the Newtonian null, thickness 60–200 kpc in z, R ≤ 320–880 kpc; nearest soft label
  to MW / M31: O2 t_i 3 823 / 1110, t_i 6 686 / 923, t_i 9 549 / 737 kpc; O1 t_i 3 308 / 421, t_i 6 410 / 554, t_i 9 436 / 584.
  So on O2 and on O1 t_i 3 each capture ball is ≥ 230 kpc from the lobe, except M31's on O1 t_i 3 (427 vs 421).

Hand estimates (nothing run):
- **A held region moving into material at rest.** With a sharp start the lattice pair straddling the boundary closes at V:
  the finite-difference J of those labels reaches 0 at ≈ 2h/V (MW on O2: 0.28 / 0.14 Gyr at h = 10 / 5). This is the
  contact surface of the posed start, a set of measure zero in the continuum; §3 excludes exactly those labels.
- **Deep-MOND halo stiffness.** ω² = Kρ_ph((1 + x)² − 1) ≈ 2GM_b/r³ in the deep halo, so the adiabaticity ωr/V = (r_cap/r)^½:
  U1's capture radius is also the radius inside which a halo can follow its galaxy.
- **Danby–Camm focusing outside the held ball.** Wind labels at impact parameter b ≳ r_cap reach the axis in ~b/(GM_b/bV):
  ~5–6 Gyr for MW on O2 (focus ~200–400 kpc behind), ~24 Gyr for M31 on O2 (its held ball is 506 kpc). So if a focal line
  forms in the windows, MW's is the candidate.
- **MW's held ball reaches the soft lobe** ~1–1.5 Gyr before X8's O2 fold times (hand arithmetic from the numbers above).
- No expectation for either verdict.

## 1. The theory and the solver (X8, unchanged)

v3s and its weak-field PN system exactly as X8 FROZEN §1 with AMENDMENT A1: Q1 finite elements on the axisymmetric (R, z)
grid, the hold law, Poisson, the khronon Euler equation with the switched stiffness γ_L∇ρ₊, quadratic-B-spline
energy-conserving ring particles, the exact discrete v3s switched static equilibrium as the initial state, fast-diagonalisation
Laplacian + Newton–PCG, the Anderson hold-law fixed point (tol 1e-7), the adaptive step dt = min(dt₀, 0.15/ω_max(t)) with
floor dt₀/50 (flag F4), MallocMediumZone = 0. Imported read-only from `rebuild_2026_10_22/X8_soft_side_caustics/x8_core.py`
(commit 72515e7e75); the X8 production driver `x8_run.py` is copied into `x10_run.py` with provenance, and only the start
(§2), the label exclusions (§3) and the added diagnostics (§6) change. Cases (§2 of X8): MW 6e10 M☉, M31 1e11 M☉, Plummer
ε = 20 kpc, on the review's kinematic orbits O1 (Newtonian timing Kepler) and O2 (constant velocity), t_i ∈ {3, 6, 9} Gyr,
window [t_i, t_end] with t_end the time r = 300 kpc (O1 16.483, O2 18.067 Gyr), both footings: **12 cases**, the same grids
(fine zone, B_out 20 Mpc, q 1.08), Dirichlet data (the spherical AQUAL potential of M_MW + M_M31 about the fixed barycentre),
validated region and diagnostic cadence (0.02 Gyr). Resolutions h ∈ {20, 10, 5} kpc for all 12 cases (h = 10 and 5
decide; h = 20 is reported for the trend, as in X8). No case is added or removed after any number.

## 2. The co-moving start (the only change to the physics set-up)

**Positions and masses** at t_i: X8's exact discrete v3s switched static equilibrium of the two masses at r(t_i) (unchanged;
the khronon is force-balanced at t_i to the same 1e-8 of |g_b|, and the soft set is X8's).

**Velocities.** Each galaxy g ∈ {MW, M31} moves at V_g = ż_g(t_i) along z on its prescribed orbit. For each label q (its
node position at t_i) define the specific Newtonian binding energy to galaxy g's baryons alone, in g's frame, of an element
at rest in the barycentre frame:

    e_g(q) = V_g²/2 − G M_g / ( |q − x_g(t_i)|² + ε² )^½ .

- **Held by g**: e_g(q) < 0 ≤ e_g′(q) (bound to g, not bound to the other galaxy g′). These labels start with v = V_g ẑ:
  the Galilean boost of the static equilibrium (§2a).
- **Common**: e_MW(q) < 0 and e_M31(q) < 0 (bound to both): held by the pair, which is at rest in the barycentre frame:
  v = 0.
- **Background**: e_MW(q) ≥ 0 and e_M31(q) ≥ 0: the host/background khronon at rest, v = 0.

The charge sign does not enter the rule. Axis labels follow the same rule (their radial velocity is zero as in X8).

**(2a) Why the boost.** The PN system is Galilean-covariant (H5 A2, sympy, residual 0): under x = x′ + Vt,
σ′ = σ + V·x′ + V²t/2, Ξ′ = Ξ and v′ = v − V. So the static switched equilibrium of an isolated mass, given v = V
everywhere while the mass moves at V and the boundary data follow it, is an exact solution that translates rigidly (X8 V-a2
tested this to 6 Gyr). Near each galaxy the two-body equilibrium is that galaxy's own equilibrium plus the other's tide.

**(2b) Why this extent.** e_g < 0 is U1's literal capture law ("holds dust only where 2GM_b/r ≥ V_rel²"; H5 A2/A3: the
stream feels the baryons' Newtonian potential, |V + δv|² = V² + 2GM_b/r), written with the Plummer potential the code uses,
so for a point mass the held ball is r < r_cap = 2GM_b/V². By the hand estimate of §0 it is also the radius inside which
the halo can follow its galaxy adiabatically. No new constant: G, M_g, ε and V_g are the case's own inputs.

**Consequences, fixed by the rule (not chosen per case).** O2 (all t_i) and O1 t_i 3: each galaxy holds its own ball
(radii ≈ (r_cap² − ε²)^½). O1 t_i 6: MW's ball lies inside M31's, so MW holds nothing and its halo starts at rest (common);
M31 holds its ball outside MW's. O1 t_i 9: every label is common, so the start equals X8's at-rest start (the galaxies move
at ≤ 5 km/s there). The held sets, their sizes and the number of soft labels in them are printed (D-HELD).

**What the start is not.** A velocity jump at a held-region boundary is a contact surface (a vortex sheet plus, on the
leading side, a closing normal velocity); the start is irrotational inside each region but not across it. A smooth
irrotational co-moving start must compress the material ahead of each galaxy on the transition scale anyway (§0); no
smoothing function is introduced, because it would be a new choice.

## 3. Label exclusions (constant-free, scale h)

A label is a **straddle label** if any label in its J stencil (its ±1 neighbours in R_q and in z_q on the label lattice;
for R_q = h the axis extrapolation uses R_q = h and 2h) has a different initial velocity class (held by MW, held by M31,
at rest). Its finite-difference J spans the contact surface and goes to 0 kinematically (§0). Straddle labels are excluded
from S, the threshold events, D-STIFF, D-GRADED and the wake statistic of §5b; they are reported separately (D-EDGE). With
the at-rest start there are no straddle labels, so every X8 statistic is unchanged. The excluded layer has thickness ~h, so
its measure → 0 with h.

## 4. Checks (scripts print `ID PASS/FAIL value threshold`; exit 0 iff all PASS)

- **R-X8a (X8 reproduced with X8's own code).** X8's `x8_run.py` executed read-only with `X8_OUT` pointing into this lane's
  `work/` (nothing in X8's directory is written), for (canonical, O2, t_i 3, h 10) and (canonical, O1, t_i 9, h 10). PASS iff
  S.J, S_by_t0.J, event.t (or both None), first_fold.t (or both None), D_STIFF.J, D_STIFF.t and n_event_elements_max all
  equal X8's committed `runs/<tag>.json` within 1e-9·max(1, |value|).
- **R-X8b (this lane's driver with the at-rest start).** `x10_run.py --start rest` on the same two cases: the same fields
  and tolerance against X8's committed json. This shows that every difference in production comes from the start alone,
  and that the at-rest start reproduces X8's transient folds.
- **V-cm (the co-moving start is stationary).** One Plummer mass (ε = 20 kpc) on a single-mass box (fine zone R ≤ 500 kpc,
  z ∈ [−600, 1600] kpc, graded to 20 Mpc), its full switched static equilibrium boosted to V (all labels; Dirichlet data
  follow the mass, as X8 V-a2), run for T = 15.167 Gyr (the longest production window, O2 t_i 3, incl. the +0.1 Gyr
  confirmation tail). Two configurations at the largest boost each galaxy receives in production: MW (6e10 M☉) at
  74.8 km/s and M31 (1e11 M☉) at 44.9 km/s (O1 t_i 3 speeds; the O2 boosts are slower over the same distance); both
  footings; h ∈ {20, 10, 5}. Statistic: max over labels in the validated region (axis excluded, A1) with 2ε ≤ |q| ≤ 300 kpc
  of |J − 1| over the run. **PASS iff ≤ 0.1 at h = 10 and at h = 5 (X8 V-a2's line, unchanged) and the h = 5 value ≤ the
  h = 10 value (converging), in all four rows.** Reported: inside 2ε, the co-moving displacement, h = 20.
- **N-dt, N-box, N-tol.** As X8 §4 with A2 (dt₀ and the 0.15 halved; B_out = 10 Mpc; hold tol 1e-8), at h = 10, on the
  case that decides each verdict:
  - (a): (canonical, O2, t_i 3), X8's case. PASS iff, when the base has a soft threshold event, the variant has one with
    |Δt_c| ≤ 0.2 Gyr; when it has none, the variant has none and |ΔS| ≤ 0.02.
  - (b): the PRESENT cell (§5b) with the earliest h = 10 downstream event; if no cell is PRESENT, (canonical, O2, t_i 3,
    MW). PASS iff the downstream statistic passes the same two-branch rule (event time ±0.2 Gyr, or no event and |Δ min J|
    ≤ 0.02) and the upstream min J stays on the same side of 0.5 as in the base. If the deciding case is (canonical, O2,
    t_i 3), the three (a) runs serve both.
- **Inherited, not rerun:** X8's R0 (review reproduced), V-a1 (static), V-b (dispersion on both sides of D·P = 0) all PASS
  in X8 (`x8_validate_results.json`); the solver is imported unchanged and R-X8a/b show it reproduces X8 here.
- **MUTATE (`X10_MUTATE=1`): the boost of the wrong sign** (held labels start at −V_g). It must FAIL V-cm. Production
  MUTATE runs (12 cases at h = 10) are reported with no pass weight (D-STIFF, D-FOLLOW, S, the wake). Outputs keep
  `_MUTATE` in their names. R-X8b is the second control: the at-rest start must reproduce X8's folds.

## 5. Statistics and frozen verdicts

### 5a. Question (a): the soft-side folds

Per case, X8 §5 unchanged (J_crit = 0.05 sustained 0.1 Gyr per element; S = min soft J in the validated region over
[t_i, t_end]; h_mid = 10, h_fine = 5), with straddle labels excluded (§3):
- **CAUSTIC** iff a threshold event at both h = 10 and h = 5 with |t_c(5) − t_c(10)| ≤ max(0.5 Gyr, 0.1 (t_c(5) − t_i));
- **NO-CAUSTIC** iff no event at h = 10 or 5, S(5) ≥ 0.05 and |S(5) − S(10)| ≤ 0.05;
- **UNDECIDED** otherwise (NOT CONVERGED; or STRONG-COUPLING / BREAKDOWN FLAG if F1–F4 fires before any event and before
  t_end).

**Verdict (a), frozen classes:**
- **FOLDS PERSIST** iff R-X8a, R-X8b, V-cm and the (a) N-checks PASS and all 6 O2 cases are CAUSTIC.
- **FOLDS REMOVED BY THE CO-MOVING START** iff the same checks PASS and all 6 O2 cases are NO-CAUSTIC.
- **UNDECIDED** otherwise, naming the failed check(s) or the case classes (e.g. PARTIAL: n of 6 CAUSTIC).

The O1 classes are reported beside X8's, with no weight in (a).

### 5b. Question (b): a focal line behind each moving mass

For each case, galaxy g and diagnostic time t ∈ [t_i, t_end] with ż_g(t) ≠ 0, let u = sign ż_g(t). The axis zone is X8's
D-WAKE zone (current R ≤ 30 kpc, current position in the validated fine zone, R_q > 0; 2ε ≤ |z − z_g(t)| ≤ 1000 kpc on the
outer side, ≤ 0.5 r(t) on the inner side), restricted to **stiff labels** (positive discrete phantom at t_i: the wind's
charge, H5 A4/A5; the soft lobe belongs to (a)) that are not straddle labels. **Downstream** = (z − z_g)u < 0 (behind the
galaxy's current motion), **upstream** = (z − z_g)u > 0. Per cell (case, g) and h:
- J_down = min J over downstream labels and samples; J_up likewise; the time each minimum is reached;
- the **downstream event**: the earliest t_c at which some downstream label has J < 0.05 and keeps J < 0.05 at every
  sample in [t_c, t_c + 0.1 Gyr] (X8's per-element rule; zone membership is required at t_c only), t_c ≤ t_end; the first
  upstream J < 0.05 time likewise (reported).

Per cell:
- **PRESENT** iff at both h = 10 and 5 there is a downstream event, J_up > 0.5, and |t_c(5) − t_c(10)| ≤ max(0.5 Gyr,
  0.1 (t_c(5) − t_i));
- **ABSENT** iff at both h there is no downstream event, J_down ≥ 0.05, and |J_down(5) − J_down(10)| ≤ 0.05;
- **UNDECIDED** otherwise, named NOT SINGLED OUT (downstream events at both h, J_up ≤ 0.5 at either), NOT CONVERGED, or
  BREAKDOWN FLAG (as §5a).

**Verdict (b), frozen classes** (24 cells: 12 cases × 2 galaxies):
- **FOCAL LINE PRESENT** iff R-X8a, R-X8b, V-cm and the (b) N-checks PASS and at least one cell is PRESENT (the cells are
  named and counted);
- **FOCAL LINE ABSENT** iff the same checks PASS and all 24 cells are ABSENT;
- **UNDECIDED** otherwise, naming the failed check(s) or the cell classes.

No case or cell selection after any number; footings never pooled (each cell is per footing).

## 6. Diagnostics (reported only; no verdict weight)

- **D-ISO (isolated mass through a background at rest).** The V-cm box and masses, but at the O2 speeds (MW 68.75, M31
  41.25 km/s) with the §2 rule for one galaxy (held iff e_g < 0, else at rest) and fixed Dirichlet data about the start
  position (the far khronon is at rest); both footings, h ∈ {20, 10, 5}, T = 15.167 Gyr. The §5b wake statistics with the
  inner side also 1000 kpc, and the §5b cell class. The cleanest form of O1's claim: uniform motion, no second galaxy, no
  saddle.
- **D-EDGE.** Straddle labels: min J, first J ≤ 0 time, against the kinematic 2h/V.
- **D-HELD.** Per case: V_g, the held radii, label counts per class, soft labels held.
- **D-STIFF** (straddle-excluded), **D-FOLLOW** (X8's; ≈ 1 expected for a co-moving halo, X8 had MW 0.51–0.76), **D-GRADED**,
  **D-SC** (F1–F4, max x, hold iterations), X8's **D-WAKE** (any sign, unchanged definition), the §5b wake on all labels of
  any sign, and on at-rest (wind) labels only.
- **D-X8.** Side by side per case: X8's and this lane's S, t_c, first soft fold, first stiff J < 0.05.

## 7. What a result can and cannot say

It answers the question in X8's model with one change, the start: axisymmetric, head-on, prescribed kinematic orbits, Plummer
baryons, no Hubble flow, no other Local Group members, no dust, μ_K → 0, no back-reaction on the baryons. The co-moving start
is one bracket (held halos boosted, the rest at rest), X8's is the other (all at rest); neither is derived from a formation
history. It does not test non-axisymmetric encounters, a completion after a fold, or quantum strong coupling. A fold here is a
fold of the single-stream khronon in this model at resolved scales (≥ 5 kpc), not a data comparison.
