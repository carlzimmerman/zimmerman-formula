# RESUME HERE — state as of 2026-08-20, end of session

## Published
- **v3 (current): DOI 10.5281/zenodo.22044021** — concept `10.5281/zenodo.22036262`
- v1 (22036263) **superseded**: it claimed "one of six mechanisms survives". **WITHDRAWN.**

## The one-line state
**No mechanism survived. The obstruction is ARM-LEVEL, not mechanism-level, and that is proved** —
all four mechanisms reduce to `div[(1 - mu_v/B^2) grad Phi] = 4 pi G rho_b` for a general
`Phi(x,y,z)` with no symmetry assumed. **Which field carries the halo cannot move the Cassini
quadrupole. Only the interpolation function can.** So searching for another mechanism is the wrong
search.

## The calculation that decides the programme (RUN THIS FIRST)
> Does an interpolation `nu(y)` exist that simultaneously (a) fits the SPARC RAR at <= 0.06 dex
> intrinsic with Upsilon inside the Spitzer prior, (b) gives `Q2 <= 5.2e-27 s^-2` at
> `g_ext = 1.9-2.6 a0` computed with the **AQUAL** (not QUMOND) quadrupole, and (c) keeps the 1-AU
> monopole inside per-planet EPM budgets?

**YES** -> the modified-Poisson arm survives and every mechanism reopens.
**NO** -> the arm is closed by a no-go; only entropic / nonlocal / multi-streaming remain.
Validate any Q2 pipeline against the published anchors `q(1)=0.094, q(1.5)=0.159, q(2)=0.221`
BEFORE trusting a single number from it.

**A workflow on exactly this was IN FLIGHT at session end** — run id `wf_fc86867a-c1d`, six routes
(squeeze / revive-C / verlinde / vainshtein / caustics / maxent-nonlocal). Resume with
`Workflow({scriptPath: ".../find-a-survivor-wf_fc86867a-c1d.js", resumeFromRunId: "wf_fc86867a-c1d"})`
— completed agents replay from cache. **Check its journal.jsonl before assuming anything.**

## What is genuinely BANKED (survives everything)
- The halo is a **unique functional of rho_b with ZERO free data** and an **attractor in radius**
  (forward integration from a 10x spurious dark point mass converges by 100 r_M). A real theorem.
- **p_r - p_t is unobservable in the weak field** (exact flat direction). The equation-of-state
  route is not the constraint.
- **Every STATIC single k-essence has p_t = -rho**, any F. the framework's condensate `phi = Q0 t + psi(r)`
  is what escapes it.
- **The khronon cannot produce the amplitude law**, by a scaling theorem (a0 is an acceleration and
  cannot be built from c and G alone).

## DO NOT CITE (new to this session)
- **"one mechanism survives"** — withdrawn in v2.
- **"the amplitude law is a derivation"** — it is EQUIVALENT to `v_c^4 = G M_b a0`, i.e. to flat
  curves at the BTFR value. Four mechanisms return the identical Bekenstein-Milgrom 1984 phantom
  density.
- **"coefficient 1.000000 supports the framework's kernel"** — `mu = x/(1+x)` and `mu = x/sqrt(1+x^2)` give
  it too. It measures the deep-MOND normalisation and nothing else.
- **"1278x / 1544x" ephemeris** — UNDERSTATES by ~27x. Correct: **33,435x / 40,282x** on Mars.
  Two independent derivations. ADVERSE; propagate as a corpus correction.
- **"identifying the scalar with the condensate fixes the double count"** — it does not. The cross
  term is `-kappa^2 s^3/(24 pi)`, needing `s* = 6.7062` against a hard cap `s <= 1/2`.

## Never tried, ranked (a stated limitation of the published work)
1. **Verlinde / entropic** — the ONE published derivation of exactly this amplitude law; its scale
   `cH_0/6 = 1.0914e-10` is **within 3.3% of the ALT footing**. Not a field equation, so it escapes
   every theorem that killed the six.
2. **Caustics / multi-streaming** — could supply the support with NO second field and NO modified
   Poisson, dodging Q2 structurally. Note: the amplitude law IS "singular isothermal sphere with
   `sigma = v_c/sqrt(2)`" exactly, on both footings — a statement about a TEMPERATURE.
3. **Revive Mechanism C** — its ghost refutation covariantised the mediator as a GAUGE vector where
   AeST's is a Lagrange-multiplier-constrained UNIT TIMELIKE vector. May be an artefact.
4. Vainshtein / k-mouflage — the only class that screens the FORCE (the hole that killed two).
5. Nonlocal (Mashhoon, Deser-Woodard); max-entropy; QUMOND; BIMOND.

## Standing
`kappa = 1/2` is **FITTED**. All numbers both footings: `a0 = 9.3619e-11` canonical /
`1.1279e-10` alt. Clusters still ~2x short (pre-existing, inherited).

---

## ⭐ UPDATE — THE ARM IS **NOT** CLOSED (route1B, 25/25)

The kernel question RESUME_HERE named as decisive has an answer: **YES, a kernel exists.**
`route1B_monotone_escape_2026.py`. And Route 1's own monotone no-go **does not reproduce** —
withdrawn, direction: it **manufactured a deficit**.

The standard published family `mu_n(x) = x/(1+x^n)^(1/n)` is monotone (`dmu/dx > 0` proved
symbolically, so AQUAL stays strictly convex and the "unique functional of rho_b" theorem
survives) and clears the squeeze. 175 real SPARC curves, Upsilon refit per kernel, AQUAL:

| kernel | Ups | RAR rms | chi2/dof | **Q2/ceiling** can/alt | 1-AU monopole / Mars |
|---|---|---|---|---|---|
| RouteA/MS08 | 0.62 | 0.0998 | 7.6 | 7.77 / 8.52 (21.6/23.7 sig) | 0 |
| **a0-line (framework)** | 0.70 | 0.1083 | 21.1 | **5.59 / 6.39 (15.3/17.6 sig)** | 3.34e4 / 4.03e4 |
| mu3 | 0.81 | 0.1179 | 34.0 | 1.55 / 2.44 | 2.80 / 3.70 |
| **mu5** | 0.84 | 0.1233 | 42.4 | **0.39 / 0.82** | 2.7e-8 / 4.2e-8 |
| **mu10** | 0.85 | 0.1266 | 49.1 | **0.08 / 0.21** | 4e-28 |

`mu10` clears across the FULL +-2 sigma of the *measured* Gaia `g_ext` on **both footings**
(0.050-0.351x); `mu5` clears everywhere canonical, and everywhere alt except -2 sigma.

**⭐ AND a0 IS UNTOUCHED: the deep-MOND limit is identical for every `mu_n` to 5e-7 at
y = 1e-12.** So `a0 = kappa c sqrt(G rho_Lambda)`, the amplitude law, the BTFR and the
BTFR-based kappa all survive the kernel swap intact. **The solar system is a statement about
the TRANSITION region, not about a0.**

**THE COST, stated plainly:** the RAR fit degrades, rms 0.1083 -> 0.1266 dex and chi2/dof
21.1 -> 49.1. The a0-line is the better RAR fit; `mu_n` is the only one that survives Cassini.
That trade is the real content and must not be hidden.

## ⚠️ THE BINDING OBSTRUCTION HAS MOVED
**Gate 5 (the double count) is failed or vacuous on EVERY route, and it is KERNEL-INDEPENDENT.
That, not Cassini, is now the wall.** No choice of `mu_n` touches it.

## Other results this run
- **Mechanism C's parallel-mode ghost DOES NOT EXIST** on the framework's own a0-line:
  `K_par = 1 - 2x/sqrt(1+4x^2) > 0` for every real x, no root (400 samples, 26 decades).
  `c_T = 1` exactly; transverse modes `c^2 = 1` exactly; Cherenkov cleared. **v2's ghost kill was
  wrong** — flagging it as contested was right. C still dies on gates 2/3.
- **Verlinde**: clears the amplitude law term-for-term (sympy residual 0) and has the fleet's only
  force-screen that comes from *counting* rather than a chosen mu (entropy budget saturating at
  `r_* = 4256 AU` for the Sun; every planet inside; residual EXACTLY zero). But **health CANNOT BE
  POSED** (no action, no field equations, no DOF), and read as published it is 3.77e8x the Mars
  budget. **It genuinely escapes the arm-level Q2 proof by falsifying its hypothesis** — Eq (7.40)
  is an algebraic map, not a PDE for general Phi, so entropic gravity has no EFE at all.
- **A "tuned-zero" bump kernel does NOT reach 0.000x the ceiling** (1.08-1.68x). Do not cite it.

## Owed / unrun
- **Vainshtein / k-mouflage is UNRUN, not dead** — it produced no script and no verdict. It is the
  only class that screens the FORCE.
- **Caustics errored mid-response**; its synthesis row is from a PARTIAL and is not reliable.
- `mu_n` needs: a relativistic host, gate 4 (health) is UNDETERMINED for it, and gate 5 fails.

## 2026-09-04 (night) — for the field-theory lead: read these two files before the next covariant attempt
- `hunt_2026/SUPPORT_BRIEF_FOR_ASTRA_2026-09-04.md` and `..._ADDENDUM.md`.
- The one-line state above ("which field carries the halo cannot move the Cassini quadrupole; only the interpolation
  function can") now has its other half: the interpolation function cannot either. With a_0 AND the disc M/L profiled,
  every Cassini-safe member of the mu_n family loses to the RAR kernel on SPARC in >= 99.9% of paired galaxy resamples
  (f25), and the RAR kernel itself gives 6.2-8.8x the Park 2026 ceiling in QUMOND and exact AQUAL (f23, f24). No
  one-argument static law mu(g/a_0) passes both. A second ACCELERATION argument is already excluded on the ledger (u02).
  What separates the Sun at 0.1 pc from a galaxy at 10 kpc at the SAME acceleration is a LENGTH: the static limit must
  carry a coherence length xi, 0.1 pc << xi <~ 200 pc, below which the phantom switches off. Consequences: Cassini passes,
  globular clusters Newtonian (3 of 4 outer-halo rows are, f27), and Gaia DR4 wide binaries gamma_v = 1.00 -- the
  opposite of the pre-registered 1.16-1.23. The localised (Helmholtz-filter) version is closed as a local theory
  (Theorem 8); a non-localisable or healing-length (medium) version has not been written. That is the open door.
- f28 (4/4) closes the one-argument class on the mu_n family: the Cassini boundary is n = 4 (0.59x canonical, 1.10x
  alt); every n >= 3 loses on SPARC in >= 99.8% of paired resamples with a_0 and M/L free; n = 1 is tolerated on
  galaxies and 6x over on Cassini. No member passes both.
- f26 (the matched QUMOND disc forward solve you asked for; 8 checks, 2 hypothesis fails): the disc correction is
  0.02-0.04 dex and identical for exp and RAR to 0.002 dex (exp vs RAR stays undecided); it weakens the mu_10
  rejection to 90-95% of resamples (disfavoured, not rejected, on the forward solve); and it makes the RAR kernel's
  fit WORSE -- SPARC discs follow the algebraic relation better than the QUMOND disc field of the same kernel (f18's
  curl-sign result on the full sample). The data do not want the modified-gravity disc field either.
- f29 (12/12) makes the length concrete: QUMOND on a Helmholtz-smoothed Newtonian potential, (1 - xi^2 nabla^2) Phi~
  = Phi_N, Phi~ a CONSTRAINT. Cassini needs only xi >= 0.03-0.04 pc (one solar MOND radius; below that it is WORSE);
  the Cassini <-> wide-binary lock is broken by a length -- the pre-registered 1.21 at 20-30 kAU survives at xi =
  0.04-0.05 pc and the KNEE moves from ~6 to ~15-20 kAU (at 6 kAU: 1.15 framework vs 1.02); xi >= 0.3 pc gives flat
  1.00. Three of four outer-halo globulars want xi ~ 50-140 pc. THE ONE-LINE PROBLEM: find the covariant action whose
  static limit is (i)-(iii) with Phi~ a constraint that adds no propagating DOF. Your Dirac chain with Phi~ as a third
  constrained variable is the calculation. Addendum section E has the tables.
- CORRECTION + CANDIDATE (f29 13/13; addendum sections E-F): the binding Solar-System floor is the phantom MONOPOLE inside
  Saturn's orbit (Pitjev-Pitjeva), xi >= 0.045 pc, not the quadrupole's 0.03; at xi = 0.05 pc the pre-registered boost at
  20-30 kAU still survives. Section F writes an explicit local candidate action: aether-frame scalar, the framework's F,
  plus xi^2 (D^2 phi)^2 -- AQUAL with a healing length; K w^2 = mu k_perp^2 + (x mu)' k_par^2 + xi^2 k^4 > 0 (no ghost, no
  Ostrogradsky, no gradient instability); the scalar is k^4-screened inside xi ~ 9000 AU, which reopens the alpha_1 lock
  as a calculation. Four calculations decide it: the biharmonic static solve for the Sun (your AQUAL solver + one term),
  PPN with the screened scalar (your aqual_solar_gate with xi), the Dirac count with the aether, the FLRW background.
- THE DOOR (f30 5/5; addendum section G): inside xi the screened scalar has NO 1/r potential, so its PPN contributions
  (gamma, beta, alpha_1, alpha_2) are absent at leading order (6e-9 at 1 AU) -- the alpha_1 lock was computed with an
  unscreened scalar and does not apply; the aether's own alpha's are Einstein-aether's (viable post-GW170817 region).
  Your "Vainshtein / k-mouflage UNRUN -- the only class that screens the force" is this, with a length. The kernel's
  CORE sets a fork: a single biharmonic term (cuspy, Coulomb-minus-Yukawa) gives a constant sunward force
  f_ph G M/(2 xi^2) that the alpha = 1 ephemeris gate bounds -> xi >= 0.8 pc, DR4 flat 1.00; a smooth-cored two-length
  operator keeps the 0.05-0.1 pc window and the pre-registered boost. First calculation: the full PPN expansion with
  the k^4 term. It decides whether the host class is open before any action is varied.
- ROADMAP EXECUTION (2026-09-04 night): G00, G01, G02 of FRIED_CHICKEN_ROADMAP_2026-09-04 are done and committed; the
  first handoff in the requested format is `FABLE_HANDOFF_2026-09-04.md`. T-A (strict exact AQUAL): FAIL on Cassini by two
  discretisations (Q2 = +2.10e-26, 4-5x the ceiling on both footings, all three g_ext inputs; 1e-11 convergence reached by
  the second scheme). T-B (double-filter, exact inverse exponential kernel): SURVIVES statically, floors 0.02/0.03 pc (Gaussian,
  canonical/alt) and 0.03 pc (Helmholtz) after the external-field conversion fix caught by g02b (astra's tidal identity
  reproduced to 1.4%/0.6%), two-body OPEN. 2026-09-04 night: the lead is directed to review the handoff and start G03
  (`MESSAGE_TO_ASTRA_2026-09-04_START_G03.md`). Next is G03 -- with the k^4 PPN constraint: the covariant filter must realise the
  coherent stiffening of the scalar's full quadratic form (f31c A), since local fourth-order operators fail alpha_1.
- G02c (2026-09-04 night): the two-body finite-mass force from the action (`g02c_two_body_force.py`, 36 checks): Milgrom's deep-MOND
  two-body force to 1%, F = -dE/dx to 0.3%, the no-net-phantom-force theorem verified; aligned wide binaries: total-mass one-body
  reduction within 2.5% except an 8-10% spike at d = sqrt(G M_tot/g_e); T-B at the Cassini floor keeps the aligned boost < 1%
  inside 15 kAU. Perpendicular orientation NOT computed. The ten hardest open questions for the lead:
  `TEN_HARDEST_QUESTIONS_FOR_THE_LEAD_2026-09-04.md`.
- f32 (2026-09-04 late): the operator that realises f31c's coherent stiffening from an action: xi^2 |grad_perp V|^2 added to Y
  inside J (V = q.dphi, the aether-frame spatial gradient; V_bg = 0 makes it multiply the whole Y sector): alpha_1 identical to
  (A) at all 12 ladder points; scalar alpha_2 drag suppressed 3.6e-5 at (xi k)^2 = 1e4 (c2 = c4 = 1/10); purely spatial =>
  no new mode, Bogoliubov dispersion (xi = healing length). Not a derivation of xi, not T-B literally, host still aether-scalar
  (spec req 2). `ONE_NEW_THING_2026-09-04.md`.
- 2026-09-05 morning: the lead is directed to strip the machine paths from its seven files and continue G03 (`MESSAGE_TO_ASTRA_2026-09-05_STRIP_PATHS_CONTINUE_G03.md`); its G03 start and two-body work are committed and pushed (d21a0db77, 084d6cbdf).
- 2026-09-05 late morning: f33 (clock host) 0 FAIL — the candidate 'clock + one dynamical MOND scalar + xi^2|grad_perp V|^2' passes the static PPN ladder at the Cassini floor; FINAL_THEORY_CANDIDATE_2026-09-05.md (13-requirement scorecard), CAUSALITY_EXPLAINER_2026-09-05.md (req 7 vs req 9; the xi term outside J restores ellipticity at zero field — uncomputed), g03b proxy floors 0.03/0.05 pc; PAPER4 deposited, DOI 10.5281/zenodo.22347632.
- 2026-09-05 midday: g03c zero-field limit with the xi term OUTSIDE J: symbol uniformly elliptic at y = 0, point-mass BVP (damped Newton, 60k nodes) Newton-exact inside, deep-MOND outside with the analytic correction -xi^2/(r_M r) confirmed to 0.1%, deviation at r_M scales as (xi/r_M)^2 then saturates (phantom kept at r_M: 0.37 for xi = r_M); the bare law's saddle-point (field-null) anomaly is erased by 1e-29 at the Earth-Sun saddle: a null prediction. Requirement 9 row moved to PASS (spherical + symbol).
- 2026-09-05 afternoon: f34 TIME-DEPENDENT scalar sector (metric + khronon + MOND scalar + operator, clock rest frame): tensor omega^2 = k^2; both scalar modes healthy (real positive omega^2, positive norms) at the PPN corner PROVIDED the MOND scalar's time-kinetic sign is K_2 < 0 in the pipeline convention (K_2 = +10 is tachyonic; the static ladders never saw that sign); MOND scalar branch Bogoliubov omega^2 = c_s^2 k^2 (1 + xi^2 k^2), khronon branch c_s^2 ~ 4e4 (1/c_14); f33b re-derives the PPN corner at K_2 = -10, c_2 = 1: 0 FAIL. Scorecard rows 2 and 7 updated.
- 2026-09-05 evening: g03d EXACT fourth-order Solar-System solve of the candidate's static law (metric Newton untouched + MOND scalar with div[mu grad psi] - xi^2 Delta^2 psi = -div[(mu-1) grad Phi_0]), axisymmetric, both footings, three field inputs, 11/11: floors xi >= 0.03 pc canonical / 0.05 pc alt (Q2 binds at 0.02 pc; the Saturn monopole binds alt at 0.03 pc); xi -> 0 reproduces G01 to 0.05%; the isolated case matches g03c to 0.2%. Requirement 10-adjacent Solar-System gates for the operator's own law are now computed, not proxied.
- 2026-09-05 night: g03e FLRW (minisuperspace, pipeline convention): G_cos/G = 1/(1 + (c13 + 3 c2)/2), scalar dust from a^3 K' conserved, operator inert at k = 0; BBN -> c2 <= 0.05 (0.1 at the edge). f35 measured G: clock part = Einstein-aether exactly; the MOND scalar's Newtonian share f_s ~ 0.9/J_Y is SCREENED below xi -> scale-dependent G (fifth force of range xi) -> needs J_Y,N >~ 30. f34b: c2 = 0.01-0.1 healthy at J_Y = 1 and 30. Scorecard rows 8, 10 updated; the corner is now J_Y,N >~ 30, K2 ~ -300, c2 <= 0.05, c14 = 1e-5, c13 = 0.
- 2026-09-05 late: g03f wide-binary bound on the fifth force from DR3 (El-Badry, pipeline cuts, 25k pairs at g > 8 a0, 0.2-2.8 kAU, differential in s): f_s = +0.08 +/- 0.23 (xi = 0.02 pc, 95% < 0.46), +0.13 +/- 0.44 (0.03 pc, 95% < 0.9 stat / 1.4 with subsample spread); mass-ratio halves disagree > 3 sigma -> systematics-limited at f_s ~ 0.5; data require only J_Y,N >~ 1-2 (the 'few per cent -> 30' was an assumption). Scorecard row 10 corrected.
- 2026-09-05 night — THE NUMBER: g03g (3-D FFT-Picard solver of the candidate's static law for a pair in the registered Galactic field, self-force subtraction, validated: 2-D agreement 6%, boost converged 0.01%, AQUAL anisotropic Coulomb law at 100 kAU to 2-4%) + g03h (the frozen DR4 estimator run on the candidate-boosted pipeline MC): gamma_v = 1.032 canonical / 1.040 alt (DR4-sized +/- 0.015) vs the registered band 1.16-1.23 and Newton 1.000. Force-boost curve at the Cassini floor: 1.002 (3 kAU) -> 1.064 (30 kAU) canonical. Overlooked handle: the aligned/perpendicular boost ordering flips with separation near 15-20 kAU (perpendicular larger below, aligned larger above) -- readable by the registered anisotropy statistic; crossing set by xi. Open numerical item: a common-mode scalar force (1.2% of Newton, resolution-independent) that cancels in equal-mass relative accelerations.
- 2026-09-05 late night: g03j THEOREM — the exact exponential kernel cannot be carried by a healthy single-valued scalar beyond g_N = 0.632 a0 (its scalar force peaks at y_tot = 1 and the longitudinal stiffness is negative for 1 < y < 38 = the FC-KH band = f21's phantom maximum); the candidate's kernel is exponential below y_tot = 1 and monotone-scalar above, with a +0.02-0.05 dex RAR bump at 2-10 a0 (BIG-SPARC-testable) and a Solar-System constant force a0/e that only the coherence length screens (0.14 of the sunward gate at Neptune). THE_ACTION_2026-09-05.md: the candidate written out in full (fields, action, parameter table, kernel, limits, five predictions that can lose, open list). Scorecard row 1 rewritten.
- 2026-09-05 late night: g03i THE SIGN-FLIP EQUATION: s_x = (2.5 +/- 0.1) xi + 0.3 kAU (s_x/xi = 2.58, 2.48, 2.52 canonical over xi = 0.03-0.08 pc; alt 2.58, 2.67), independent of r_e (s_x/r_e 2.5-6.8): perpendicular pairs boosted more inside s_x, aligned more outside; 16.0 kAU at the canonical floor, 26.6 kAU alt. Neither bare AQUAL nor bare QUMOND flips. Readable by the registered anisotropy statistic.
- 2026-09-05 late night: g03k DERIVES the 2.5: the screened anisotropic Green's function Phi_hat = -4 pi G M (1 + xi^2 k^2)/[mu_e k^2 (1 + L cos^2) + xi^2 k^4] makes the crossing s_x = x_x(y_e) xi exactly (r_e-independent); quadrature x_x = 2.51 (canonical) / 2.63 (alt) vs the 3-D scan 2.53 +/- 0.05 / 2.63 +/- 0.05; x_x runs 3.14 -> 2.38 over y_e = 1 -> 3.
- 2026-09-05 late night: g03l SPARC vs the monotone-completed kernel (f25 design, a0 + Upsilon profiled, 999 paired resamplings): undecided vs the exponential kernel ([-0.0001, +0.0003] dex^2 for p = 0-0.25), mildly disfavoured vs nu_RAR at 95-99% like mu_exp itself; the bump is neither seen nor excluded by SPARC -> BIG-SPARC. Derivation g03k committed (cd715a418).
- 2026-09-05 late night: g03m dark sector at the Jeans level: the scalar dust's local stiffness = J_Y(y_local) ⇒ environment-dependent Jeans length; capture order as |K2| grows: cluster R500 (2.6e6) -> cluster core (2.5e8) -> galaxy outskirts/KiDS (5e9) -> galaxy core (2e10): a factor-2000 |K2| window where clusters capture and galaxies do not. Fractions (14%/32-46%) need accretion; Coma UDG untouched. A door, not a fix.
