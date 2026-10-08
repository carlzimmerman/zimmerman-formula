# CFG488 FROZEN CRITERIA: co-settling shell by shell as the supply rule behind the 5.85 r_M edge

Committed alone, before any script exists. kappa = 1/2 is FITTED and fixed. Both footings (a0 = 9.3603e-11 and
1.1312e-10 m/s^2) are scored separately and never pooled. No dark-matter particle is added: the cold fluid's MASS is still
required and its amount (Omega_c/Omega_b = 5.364) is an input. No knob scans. Never "theory closed". Offline theory +
numerics only; no downloads (local committed record files only).

## The question (CFG462's open gap)

The zero-knob growth fix (CFG424/425/439, PAPER45 v2.1) uses r_edge = r_M/ln(1/(1 - f_b)) = 5.8498 r_M, the radius where
the law's phantom has used up exactly the cosmic share 5.364 M_b (T10 S6; CFG423). CFG462 showed the khronon lapse does not
stop settling there: with the catchment supply the edge goes to 23-30 r_M or fills the catchment, and the edge appears only
when the supply is set to exactly 5.364 M_b (its SHARE control, "a restatement, not a test"). The gap is the SUPPLY: why does
a halo settle only the cold fluid that came with its present baryons?

CFG462's untested idea, tested here: CO-SETTLING per Lagrangian shell.

## The rule (stated precisely)

- Label every matter element by its Lagrangian coordinate q at z_i = 100. Every Lagrangian shell [q, q + dq] starts with
  baryons and cold fluid in the cosmic ratio: dm_c(q) = (Omega_c/Omega_b) dm_b(q), Omega_c/Omega_b = 5.364.
- Let Gal(t) be the set of shells whose baryons are in the galaxy at time t (the baryons that source the law's g_N).
- **CO-SETTLING (LIVE):** the cold fluid of shell q is eligible to settle at t iff q is in Gal(t). Cold fluid whose baryons
  never reached the galaxy, are still in the hot halo, or were expelled stays UNSETTLED (cold, CDM-like) on its orbit.
  **SET variant (used for (4) only):** eligible iff q was EVER in Gal (the partners of expelled baryons stay settled).
- Eligible cold fluid settles "into the phantom sourced by those same baryons". The law is nonlinear, so that phrase has
  more than one reading. Five are declared (below); all are scored, none is dropped after the run.
- **Composition identity (stated in advance):** for ANY history, the eligible cold mass is sum_q in Gal (Omega_c/Omega_b)
  dm_b(q) = (Omega_c/Omega_b) M_b,gal = 5.364 M_b,gal. In the code the eligible shells are selected by their cumulative
  baryon content (the run's own Omega_b/Omega_c times their cold mass) <= M_b,gal, never by a cold-mass number. The 5.364
  enters only as the shells' composition, an initial condition. The history can enter only through WHERE the eligible cold
  fluid settles.

## Accretion histories (declared)

- **H-N (scored), framework-native.** Under the mass-conserving rule the phantom IS the settled cold fluid, so the field
  outside the settled region is the enclosed real mass (Gauss), and inside it the law's field equals the enclosed real mass
  as well. The law's own collapse of a shell is therefore the Newtonian collapse of the total matter inside it, followed by
  settling. The record's committed configuration for that is CFG118's: a static point baryon core of M_b from z_i = 100
  (the galaxy's baryons, assembled early), Planck18 background (H0 = 67.4, Omega_m = 0.315), cold shells uniform in
  enclosed cold mass at Omega_c rho_crit(z_i) on the Hubble flow out to the Lagrangian mass at 3 r_ta(z=0), the other
  baryons a smooth non-clustering background, angular momentum fixed at first turnaround so r_peri/r_ta = q, shell
  crossing allowed, time-averaging over each radius's last dynamical time. Copied machinery; CFG118's `shellcore.c` is
  compiled read-only from its committed path into a temporary directory (sha256 recorded). Shell composition uses
  f_b = 1/(1 + 5.364) = 0.157134 (CFG118 used 0.157; checked by K4). N = 20000; q = 0.05, 0.1, 0.2 (CFG118's brackets,
  all reported, none chosen after the run). The point-core problem is exactly self-similar in M_b (r ∝ M_b^(1/3) at
  fixed time), so one run per q at M_b = 1e10 is rescaled to every mass; r_M(M, footing) converts to r_M units.
- **H-B (reported only), Bertschinger.** CFG118's C2 configuration: Einstein-de Sitter, one collisionless background
  (Omega = 1 in the shells), point seed, read at a = 1; shells carry cold and baryons in the cosmic ratio, so the eligible
  shells are those with cumulative shell mass <= M_b/f_b and their cold part is (1 - f_b) of that.
- **Retention.** R1 (scored): inner-first; the galaxy's baryons are those of the innermost Lagrangian shells. R2 (reported):
  uniform; every shell that has turned around by z = 0 gives the same fraction of its baryons, set by M_b,gal.

## The five readings (formulations)

Hosts: the baryons are a point mass M_b (scored; the H-N host and the definition host of 5.8498 r_M). Hernquist
a = 0.3 r_M (CFG462's scored host) is reported for the scale-free readings, with a = 0.3 r_M(t) as the galaxy grows. The
target is the law's phantom of the baryons, M_ph(<r) = (nu(g_N/a0) - 1) M_b(<r), nu_mono (FP1's committed table via
CFG4_common, read-only). The baryon growth M_b(t) for CS-M/CS-F follows the eligible shells in Lagrangian order (R1).

- **CS-P (pooled, LIVE, free transport):** the eligible cold fluid fills the present target inside-out:
  M_s(<r) = min(M_ph(<r), S_p), S_p = the eligible cold mass (CFG462's F-H equilibrium). History-blind by construction.
- **CS-I (pooled, inward-only transport):** an eligible parcel at radius r0 can settle only at r <= r0 (settling loses
  energy). Settled total S_I = min over cuts r of [M_ph(<r) + P(>r)] (P = the time-averaged eligible pool from H-N);
  settled profile min(M_ph(<r), S_I); the rest of the pool stays where it is, unsettled ("stranded"). Cross-checked by an
  innermost-first greedy fill (K5).
- **CS-0 (in place, no transport):** settled density = min(rho_pool, rho_ph) per 0.05-dex radial bin (0.1 dex reported).
- **CS-M (per shell, marginal phantom, frozen at accretion):** each increment dM_b of the galaxy's baryons, accreted when the
  galaxy holds M_b', brings (Omega_c/Omega_b) dM_b of cold fluid, which fills the increment's own phantom
  d_M M_ph(<r; M') dM_b inside-out until used, and stays there.
- **CS-F (per shell, proportional share, frozen at accretion):** the increment's cold fluid fills its proportional share
  (dM_b/M') M_ph(<r; M') of the phantom at its accretion, inside-out until used, and stays there.

## Gates

- **Edge r_e** := the radius enclosing 99.9% of the formulation's settled cold mass (the support boundary and r_99 are
  also reported). r_edge = 5.8498 r_M(true a0).
- **P1 (the user's line):** |log10(r_e/r_edge)| <= 0.05 at M_b = 1e9, 10^10.5, 10^11.5 x both footings (6 cells). For the
  history-dependent readings (CS-I, CS-0) a pass needs at least one q bracket, the same q at every mass and footing (CFG118's
  rule).
- **P1b (the law is carried):** the eligible cold fluid inside r (settled + stranded) satisfies
  |M_elig,in(<r)/M_ph(<r) - 1| <= 0.05 for all r in [0.1, 0.8] r_edge, all 6 cells (same-q rule).
- **Criterion (1)** for a formulation = P1 and P1b, with no 5.364 M_b inserted (the eligible supply is computed from the
  shells' composition, as above).
- **R-EQ flag (the CFG462 restatement test):** a formulation is RESTATEMENT-EQUIVALENT if its settled profile equals
  CFG462's SHARE control, min(M_ph(<r), 5.364 M_b), to 1e-6 relative in every cell AND is unchanged (to 1e-9) when the
  history is swapped (H-N q-brackets, H-B, R2). An R-EQ pass of (1) is the definition of r_edge with the supply relabelled.
- **Criterion (2), clusters.** Record (read from CFG453's committed JSON, `D1[foot]`, medians over the X-COP clusters at
  R500): nu_cl - 1, x_T15 and x_A at hydrostatic bias b = 0 and 0.3. The record's unsettled fraction of the dark mass inside
  R500 is u_rec = 5.364 x_A/x_T15; the scored range per footing is [u_rec(b=0), u_rec(b=0.3)] (for reference:
  canonical [0.4334, 0.6275], alt [0.3675, 0.5840]). CFG383's bracket u = 0.3-0.7 is reported.
  Prediction (closed box, declared: the cold fluid that came with the baryons now inside R500 is inside R500, and no
  ineligible cold fluid is inside R500): eligible cold inside R500 = 5.364 M_b(<R500).
  - Free-placement readings (CS-P, CS-M, CS-F): the eligible cold fluid is placed into the target; inside R500 it fills
    M_ph(<R500) and the surplus is placed beyond R500 (CS-M/CS-F: their own placement profile at x500). Unsettled cold
    inside R500 = 0, so u_pred = 0.
  - In-place readings (CS-I, CS-0): the target inside R500 fills from local eligible fluid (5.364 > nu - 1); the surplus
    cannot move out and stays unsettled: u_pred = 1 - (nu_cl - 1)/5.364 (CS-0 evaluated cumulatively, as CS-I; declared).
  - (2) passes iff u_pred lies in the record range on BOTH footings. Reported sensitivity: ineligible cold inside R500 =
    max(0, x_T15 - 5.364) M_b.
- **Criterion (3), G9 (no direct baryon-cold coupling; matter couples to gravity only).** Classes, applied to each
  formulation as literally stated and to its best gravitational surrogate:
  - G9-CLEAN: the cold parcel's settling decision, drive and stop are functionals of the gravitational fields (metric,
    lapse/khronon, sourced by the total stress-energy) along its own worldline, its own fluid state, and comoving labels set
    by those, with no species-split field and no number inserted beyond kappa, G and the fields themselves.
  - G9-TENSION: needs a species-split gravitational field (the baryons' own Newtonian field, or the cold fluid's own
    enclosed mass): a second elliptic solve keyed to one species (CFG462's F-H class).
  - G9-FAIL: needs any baryon state other than through gravity, in particular the identity or fate of the baryons that
    share its Lagrangian label after the species have separated (a two-species label: a direct baryon-cold coupling).
  - The argument is written out in the README. The numerical part is the per-parcel signal: the fractional change of the
    gravitational field on an eligible cold shell when its OWN partner baryons go to the galaxy vs stay on the shell's
    orbit, f_b-weighted shell mass / enclosed mass at its time-averaged radius, at N = 5000 and 20000 (must scale as 1/N,
    i.e. vanish in the continuum), against the collective signal (all the galaxy's baryons in the core vs on the eligible
    orbits) at r_edge.
  - (3) passes iff the formulation scored in (1) and (2) is G9-CLEAN.
- **(4), depletion (reported with frozen labels; not part of PASS).** f_ret = present/ever-in-galaxy baryons.
  - LIVE: edge = 5.8498 r_M(present) for any f_ret. SET: edge = r_M/ln(1 + f_ret/5.364) (PAPER45's general form; exact for
    nu_mono and a point mass).
  - KiDS: CFG413's lens groups (read-only `lr_lenses.npz`, `cfg110_perlens.npz`; grouping 0.01 dex in M_gal x 0.03 in z as
    CFG413), r_ta = cfg100 `r_ta_law` per group (read-only import), group weight = sum of WW over its lenses and the 15
    bins. x_edge = r_edge/r_ta per group; weighted median and 16-84%.
  - Window [0.3, 0.5] r_ta (CFG413's x_min 0.23-0.3 and best fit 0.4-0.5 reported). LIVE: MATCH iff the weighted median
    x_edge is in the window on both footings, else MISS. SET: the f_ret that puts the median at 0.5 and at 0.3 is reported
    and compared with PAPER45 v1's census retention 0.07-0.10; SET is labelled CONDITIONAL (f_ret,gal is not predicted;
    under co-settling the partners of never-accreted baryons never settle, so f_ret,gal >= the halo-level census value).

## Verdicts (lane)

- **PASS:** one formulation passes (1), (2) and (3) together.
- **FAIL (RESTATEMENT ONLY):** no formulation passes all three, and every formulation that passes (1) is R-EQ.
- **FAIL:** otherwise. The failing criteria are listed per formulation.

## MUTATE (`CFG488_MUTATE=1`): cosmic ratio x 2

Omega_c/Omega_b -> 10.728 at fixed Omega_m (f_b' = 0.085265): the H-N runs are repeated with the new split (shell cold
density and smooth baryons), eligible shells re-selected by composition, the scale-free readings re-run with S' = 10.728;
the law, the host and r_edge (5.8498 r_M) stay TRUE. H-B is not re-run (reported-only in the main run). Predicted shift of a
supply-keyed edge: Delta_S = log10(x_e(S')/x_e(S)) for CS-P and CS-F (+0.2828 dex, point mass), log10(x_k(S')/x_k(S)) for
CS-M (x_k: the marginal exhaustion radius, from nu + y nu' - 1 = S), and Delta_S of CS-P for CS-I and CS-0 (a co-settling
edge keyed to the ratio must move by it). Teeth DETECTED iff CS-P (the R-EQ control) and every formulation that passed P1 in
the main run move by their predicted shift +- 0.02 dex in all 6 cells and then fail P1 against the true r_edge. The MUTATE
run exits 1 iff the teeth are detected. (2) is recomputed with S' (reported).

## Controls (the main run exits 0 only if K1-K5 pass; K6 reported)

- **K1 (sympy):** the composition identity; x_e = 1/ln(1 + 1/S) for nu_mono and a point mass (nu - 1 = 1/(e^(1/x) - 1));
  the marginal-edge equation; the CS-M telescoping M_s(<r) = M_ph(<r; M_b) - M_ph(<r; M_b x^2/x_k^2).
- **K2:** CS-P with the point host gives 5.8498 r_M to 1e-4 relative (CFG462 K3).
- **K3:** CS-M by direct numerical superposition of increments equals the telescoped closed form to 1e-4 relative on
  [0.05, 0.95] x_k r_M.
- **K4:** the H-N runs reproduce CFG118's point-core set-up: M_ta(z=0)/M_b = 23.64 and r_ta0(1e10) = 508.0 kpc within 1%,
  and the measured zero-velocity radius equals the single-shell prediction within 1%. The cold mass inside the measured
  r_ta at z = 0 is reported.
- **K5:** CS-I's min-cut total equals the innermost-first greedy fill to 1e-9 relative (same bins).
- **K6 (reported):** N = 5000 H-N runs reproduce the CS-I and CS-0 edges within 0.05 dex (CFG118's C3 failed for local
  ratios; a K6 failure is kept and disclosed, and any CS-I/CS-0 verdict within 0.05 dex of a gate line is flagged).

## Reported rows (load-bearing for the reading, not verdict inputs)

- **Contamination:** the INELIGIBLE (unsettled) cold fluid of H-N inside r_M, 0.5 r_edge and r_edge, as a fraction of
  M_ph(<r) and in cosmic-share units, per q. Flag "law contaminated" if it exceeds 10% of M_ph(<r_edge) at every q.
- R2, H-B, Hernquist a = 0.3 r_M, 0.1-dex CS-0 bins, the f_b-test d ln y_e/d ln f_b of each formulation (from the MUTATE
  pair; a genuine nu = Omega_m/Omega_b edge needs 2.18).

## Expected before running (stated so a fail is not manufactured after the fact)

By the composition identity the eligible supply is 5.364 M_b for any history. I expect: CS-P lands on 5.8498 r_M exactly (point
host; +0.018 dex Hernquist), is R-EQ, and fails clusters (u = 0: a closed-box cluster's cold fluid is all eligible and is
placed into the target, the surplus beyond R500). CS-M puts its edge near 11.7 r_M (+0.30 dex) and under-fills the law
inside. CS-F's edge is the last increment's, at r_edge, but it over-fills the deep law by up to ~2x. CS-I and CS-0 inherit
CFG118's too-concentrated infall pool and its M^(1/3) scale: stranding, edges that drift with mass, the law not carried; but
they give clusters u = 1 - (nu - 1)/5.364 = 0.452 / 0.389, inside the range. G9: the literal rule needs a two-species label
(G9-FAIL); its surrogates are at best G9-TENSION and restate the share. Depletion: LIVE puts KiDS lenses near x ~ 0.05-0.1
(MISS); SET reaches the window only if f_ret,gal is near the census 0.07-0.10. Expected lane verdict: FAIL (RESTATEMENT
ONLY). If the numbers say otherwise, the numbers win.

Outputs: script, .out, _MUTATE.out, results JSON (both modes), README. Commit locally; do not push.
