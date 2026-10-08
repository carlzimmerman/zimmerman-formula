# CFG494 FROZEN CRITERIA: is the supply postulate supplied by adiabatic initial conditions?

Written and committed alone, before any script or number of this lane. κ = ½ is FITTED. Both footings (a₀ = 9.3603e-11 and
1.1312e-10 m/s²) are scored separately and never pooled. No dark-matter particle is added: the cold fluid's mass is still
required and its amount (Ω_c/Ω_b = S = 5.364) is an input. This is not "theory closed".

## The question

PAPER45 v2.1's growth fix rests on one postulate: each galaxy's settled cold fluid equals S × its own baryons, which puts the
law's edge at r_edge = r_M/ln(1/(1 − f_b)) = 5.8498 r_M. CFG461, CFG462, CFG488 and CFG490 did not derive it dynamically.

New angle: adiabatic primordial perturbations give cold/baryon = S in every Lagrangian volume element. So the cold fluid that
started in the same Lagrangian region as a galaxy's baryons (their "Lagrangian partner") has mass S × the galaxy's ORIGINAL
baryons by construction. Can the postulate be restated as "the settled cold fluid is the Lagrangian partner of the galaxy's
baryons", and is that restatement a derivation?

## The two readings (both scored; none dropped)

- **LP-G (galaxy partner).** The settled cold fluid is the Lagrangian partner of the baryons that dissipated into the galaxy.
  The partner set L_gal is the set of Lagrangian labels q whose baryons reached the galaxy (CFG488's R1: inner-first).
  - LP-G/LIVE: partners of later-expelled baryons unsettle; the edge is 5.8498 r_M of the present baryons.
  - LP-G/SET: partners of expelled baryons stay settled; the edge is r_M/ln(1 + f_ret,gal/S), with f_ret,gal = present /
    ever-dissipated baryons. The initial conditions do not supply f_ret,gal; if no derivation of it appears here, LP-G/SET
    has no prediction and cannot pass (c).
- **LP-H (halo partner).** The settled cold fluid is the Lagrangian partner of ALL baryons in the halo's collapsed
  Lagrangian patch, i.e. every cold parcel that has turned around. This set is defined by gravity alone.
  - LP-H/inf: the patch is CFG118's z = 0 turnaround catchment in the H-N infall model (23.63 M_b of cold; record value),
    edge r_M/ln(1 + M_b/M_c,catch) for a point host.
  - LP-H/law: the patch is the law's own turnaround (cfg100 `r_ta_law`, per lens/node): total mass M_ta = ν(r_ta) M_b, cold
    partner (1 − f_b) M_ta, edge where the point-host ν_mono phantom M_b(ν(1/x²) − 1) = (1 − f_b) ν(r_ta) M_b.
- Placement: both readings use free inside-out fill of the law's phantom (the only placement that carries the law, CFG488
  (1)) for galaxies AND clusters. In-place cluster numbers are reported, not scored.
- The settling drive, its mobility and its energy sink are inherited (CFG462/CFG490) and not counted for or against here.

## Model (offline numerics)

- H-N (scored): CFG118's point-core secondary infall in Planck18 ΛCDM, run through CFG488's infall worker functions
  (`cfg488_infall.py`, imported read-only; CFG118's `shellcore.c` compiled read-only to a temp dir). N = 20,000 shells;
  q = r_peri/r_ta ∈ {0.05, 0.1, 0.2} (the record's bracket). One run per q at M_sim = 1e10 serves all masses (the set-up is
  self-similar: radii ∝ M^(1/3), times unchanged). N = 5,000 is a reported resolution check.
- H-B (reported only): CFG488's Einstein–de Sitter configuration, shells of total matter in the cosmic ratio.
- Partner labels (H-N): shell k carries baryons b_k = m/S (smooth in the dynamics, as CFG118/488); L_gal = the innermost
  shells with Σ b_k = M_b (fractional boundary shell k_b). Partner cold = Σ_{k ∈ L_gal} m. This equals S M_b only through the
  initial composition, which is the point of the new angle and is allowed.
- Dissipation time (scored): t_d = 2 t_ta(k_b), the first collapse of the outermost partner shell (the last galaxy baryons fall
  in). Reported: t_ta(k_b), z = 2, z = 1, z = 0.
- Cells: M_b = 1e9, 10^10.5, 10^11.5 M☉ × 2 footings.

## Quantities

At time t, for a sphere of radius R about the centre (instantaneous shell positions; shellcore drifts exactly):
- completeness C(R) = partner cold inside R / (S M_b);
- purity Π(R) = partner cold inside R / all cold inside R.

Spheres:
- R_ta(t): the turnaround radius at t (the radius of the shell whose t_ta = t, interpolated) = the record's catchment;
- R_200(t): mean enclosed (core + cold) density = 200 ρ_crit(t);
- R_edge: 5.8498 r_M of the cell (physical; contains f_b, so it is a RESTATEMENT selector, reported only);
- R_S(t): the sphere enclosing exactly S M_b of cold (contains S: restatement selector, reported only).
Energy rank (reported only, S inserted): purity of the most-bound S M_b of cold at t_d (E = v²/2 + j²/2r² + Φ(r), Φ from the
enclosed core + shells; v by a finite difference of two snapshots).

## Criteria

**(a) G9.** The cold parcel's own Lagrangian label q is G9-allowed data (its own history). The partner SET must also be
selectable without reading the other species.
- LP-H: the set "has turned around" is the parcel's own orbit history and the total-mass field: G9-CLEAN by construction
  (declared now).
- LP-G: L_gal is defined by baryon fate (which baryons cooled into the galaxy). It is G9-compliant only if a label-free,
  S-free selector picks it out: (a) PASSES for LP-G iff at t_d, for at least one of R_ta(t_d), R_200(t_d), both C ≥ 0.9 and
  Π ≥ 0.9, in every q and cell. Otherwise LP-G is G9-FAIL as CFG488 (finding 5).

**(b) Pairing.** C(R_ta(t_d)) ∈ [0.9, 1.1] at M_b = 1e9, 10^10.5, 10^11.5 (all q, both footings) with the partner mass
computed from the labels, never set to S M_b. For LP-H the scored ratio is (the settled partner cold inside R_ta) / (S M_b of
the galaxy), i.e. the halo partner against the postulate's 5.364 M_b.

**(c) Depleted halo / lensing.** PASS iff BOTH:
- (c1) KiDS window: the lensing-weighted median x_edge/r_ta over CFG413's 1,953 lens groups (CFG488's grouping and weights,
  cfg100 `r_ta_law`) lies in [0.3, 0.5] on both footings, with no fitted f_ret;
- (c2) early-type absolute levels: with the phantom fully settled and truncated at the reading's edge, CFG485's R8 early-type
  χ² (released per-class block, free two-halo, 6 dof) is ≤ 12.59 (p ≥ 0.05) on both footings.
A reading with no derived f_ret (LP-G/SET) has no prediction and FAILS (c) (labelled CONDITIONAL).

**(d) Clusters.** The predicted unsettled fraction of the dark mass inside R500 lies in the record range ([0.433, 0.628]
canonical, [0.368, 0.584] alt; CFG453 medians via CFG488) on both footings, under the reading's scored (free) placement.
- LP-G: only dissipated cluster baryons (stars, BCG, ICL) have settled partners: settled = min(M_ph(<R500), S f_* M_b),
  u = 1 − settled/x_T15 M_b (b = 0 and 0.3 both inside the range to pass). f_* = 0.05–0.20 is RECALLED (U), not on disk;
  the f_* needed to enter the range is reported.
- LP-H: closed box, all cluster cold is partner; free placement gives u = 0 (CFG488); in-place reported.

**Restatement rule.** A pass that holds only through R_edge, R_S or any quantity containing f_b or S as a selector (not as the
initial composition) is RESTATEMENT and FAILS, as in CFG462/488.

**Lane verdict.**
- DERIVES iff one reading passes (a) AND (b) AND ((c) OR (d)).
- Otherwise NOT DERIVED, with the per-criterion table. If a reading passes (b) only as the composition identity while failing
  (a), the label is "RESTATEMENT (initial-condition relabel)".

## Controls (load-bearing; exit 0 iff all pass)

- K1: the H-N runs reproduce CFG488/CFG118: M_ta/M_b = 23.632 ± 1%, r_ta0 = 507.94 kpc ± 1%; partner cold = S M_b to 1e-9.
- K2: at t = t_ta(k_b)/2 (before the boundary shell can have crossed) the purity in the sphere of the boundary shell's own
  radius is ≥ 0.99 (shell order preserved before collapse; checks the label bookkeeping).
- K3: CFG488's KiDS numbers reproduced: LIVE median 0.0377 / 0.0327 ± 0.001.
- K4: CFG485's R8 early-type χ² at 5.8498 r_M, fully settled, reproduced: 30.5 / 38.1 ± 0.5.
- K5: x_e(S) = 1/ln(1 + 1/S) = 5.8498 and the ν_mono point phantom at x_e equals S M_b to 1e-6.

## MUTATE (`CFG494_MUTATE=1`, writes *_MUTATE.*; exit 1 = teeth detected)

Isocurvature initial conditions: the shells' cold/baryon ratio varies with Lagrangian mass coordinate by a factor 2 across
the catchment, ratio(m) = S · 2^(1/2 − m/M_ta,cold) for m ≤ M_ta,cold (S/√2 beyond); cold shells and dynamics unchanged, the
labels (b_k = m/ratio_k) change. The pairing prediction must break: teeth = C(R_ta(t_d)) relative to S M_b leaves [0.9, 1.1]
in every q and cell. Reported: a mean-preserving random per-shell ratio (log₂-uniform over a factor 2, seed 494), which is
expected to average out (small-scale isocurvature cannot break the pairing; only coherent, galaxy-scale isocurvature can).

## Expectations written now (not verdict inputs)

- LP-G: C(R_ta(t_d)) ≈ 1 (all partners have turned around by t_d), so (b) likely passes as the composition identity; Π at
  R_ta and R_200 well below 0.9 (later shells crowd in), so (a) likely fails; (c) LIVE misses KiDS (0.038, CFG488) and the
  early-type levels (CFG485); (d) u ≈ 0.8–0.9, outside the range.
- LP-H: (a) clean; (b) ≈ 23.63/5.364 = 4.4, FAIL; (c1) LP-H/inf near 0.16 r_ta (miss), LP-H/law near 0.8 r_ta (miss);
  (d) free placement u = 0, FAIL.
- Overall expectation: NOT DERIVED. The run decides.

## Outputs

`cfg494_adiabatic.py`, `cfg494.out`, `cfg494_MUTATE.out`, `cfg494_results.json`, `cfg494_results_MUTATE.json`, plain
`README.md`. Committed locally; not pushed.
