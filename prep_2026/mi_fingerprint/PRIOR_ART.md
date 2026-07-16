# PRIOR ART + DATA RECON — MI fingerprint suite (Lane RA)
Date: 2026-07-16. Scope: what has actually been done to distinguish modified INERTIA (MI)
from modified gravity (MG) with rotation-curve / RAR data; what is open; what the repo banks.
All quotes verbatim from the fetched papers (arXiv PDFs extracted locally with pdftotext).

Framework context (NOT standard MOND): de Sitter–Unruh modified inertia,
a0 = cH_Lambda/Z = 9.36e-11 m/s^2 (Z = sqrt(32pi/3)); ALT footing 1.13e-10 (rho_total/cH0) — run BOTH;
framework interpolation nu(y) = sqrt(1 + 1/y), i.e. g_obs = sqrt(g_bar^2 + g_bar*a0).
Concrete covariant MI action: passive frame u^mu + Herglotz–Nevanlinna kernel K(box_u/a0^2),
||K|| <= 1, causal-retarded, sum rule ∫dmu(t)/|t| = 1 (Zenodo concept 21253644;
scripts zimmerman-formula/reviews/mi_formal_completion_2026/ — READ-ONLY).

---

## 1. The papers (actual statistics, data, verdicts)

### 1.1 Milgrom 1994, Ann. Phys. 229, 384 (arXiv:astro-ph/9303012) — MI foundations
"Dynamics with a Nonstandard Inertia-Acceleration Relation: An Alternative to Dark Matter in Galactic Systems."
- Abstract (verbatim, key parts): "We investigate particle laws of motion derived from nonstandard
  kinetic actions of a special form. ... Galilei-invariant such theories must be strongly non-local;
  this is a blessing, as such theories need not suffer from the illnesses that are endemic to
  higher-derivative theories. ... Exact solutions are obtained for circular orbits, which pertain to
  rotation curves of disk galaxies. We also explore, in passing, theories that depart from the
  conventional Newtonian dynamics for very low frequencies."
- THE CIRCULAR-ORBIT THEOREM: in any MI theory of this class, circular orbits in an axisymmetric
  potential satisfy the ALGEBRAIC relation mu(V^2/(R a0)) V^2/R = g_N exactly, ring by ring.
  This is the load-bearing kinematic fingerprint: MI => rotation curves sit EXACTLY on the algebraic
  curve; MG (AQUAL/QUMOND) => radius-dependent geometric deviations (the field equation mixes radii).
- Also the origin of the frequency remark ("theories that depart ... for very low frequencies") —
  the frequency lane (b) has a 1994 pedigree but no concrete kernel was ever supplied. Milgrom's later
  models use only frequency RATIOS (see 1.6); a dimensionful frequency scale is NOT in the literature.

### 1.2 Milgrom 1999, Phys. Lett. A 253, 273 (arXiv:astro-ph/9805346) — dS-Unruh prior art
"The Modified Dynamics as a Vacuum Effect." Abstract (verbatim, key part):
"An observer on a constant-acceleration (a) trajectory in a de Sitter universe with cosmological
constant L sees Unruh radiation of temperature T ∝ [a^2+a0^2]^(1/2), with a0=(L/3)^(1/2). The
temperature excess over what an inertial observer sees, T(a)-T(0), turns out to depend on a in the
same way that MOND inertia does. An actual inertia-from-vacuum mechanism is still a far cry off."
- This is the closest ancestor of the framework's premise. Differences to keep straight:
  Milgrom's quadrature is at the TEMPERATURE level and his mu comes from the temperature EXCESS;
  the framework puts the quadrature at the ACCELERATION level (g_obs = sqrt(g_bar^2 + g_bar a0)),
  fixes a0 = cH_Lambda/Z with Z = sqrt(32pi/3) derived from the horizon footing, and now has a
  covariant action. Milgrom explicitly flags "no actual mechanism"; the framework claims the action.

### 1.3 Petersen & Lelli 2020, A&A 636, A56 (arXiv:2001.03348) — the Q test. VERDICT: MG-leaning NULL
- Statistic: the global deep-MOND parameter Q ≡ <V^2>/V_inf^2 with
  <V^2> ≡ M^-1 ∫ 2πr Σ(r) V^2(r) dr (Milgrom 2012, PRL 109, 251103). Predictions:
  "MI predicts Q = 0.73 ± 0.01 and MG predicts Q = 2/3 for disk-only galaxies everywhere in the
  deep MONDian regime." (2/3 ≈ 0.667; a ~10% discriminant, ~5% in rms velocity.)
  NOTE: Q is a deep-MOND GLOBAL invariant — to leading order independent of the choice of nu and of a0.
- Data cuts (from mock-galaxy systematics study): "max[g_obs] ≲ 0.4 a0 (acceleration scale
  requirement), max[r] ≳ 3 r_d (sampled range requirement) and the spacing between points is
  ≲ 1.3 r_d (resolution requirement). Imposing these criteria on the SPARC database leaves 15 galaxies."
- Result (verbatim): "Before correcting for systematic effects, the arithmetic mean and median of Q is
  given by <Q(m)> = {0.63 ± 0.09, 0.64 ± 0.07}, respectively. After correction <Q(c)> ≈ {0.63 ± 0.08,
  0.65 ± 0.06}." "...these measurements line up closely with the predictions of MG both before and
  after correction, although the prediction of MI is still within 1.5σ."
- Abstract verdict (verbatim): "the average and median values of Q seem to favor MG theories, albeit
  both MG and MI predictions are in agreement with the data within 1.5σ."
- EMPIRICAL STANDING: a statistically underpowered MG lean; NOT a kill either way.
- Companion method paper: Petersen & Frandsen, MNRAS 496, 1077 (2020) — DM vs MOND-MI geometry in
  (g_N, g_tot) space ("g2-space"); radial information discriminates MI from DM. (Different statistic;
  no MI-vs-MG verdict.)

### 1.4 Chae 2022, ApJ 941, 55 (arXiv:2207.11069) — inner/outer split. VERDICT: claims MG, MI disfavored
- Statistic: split each SPARC RC VISUALLY into inner rising part vs outer quasi-flat part
  (median transition radius 2.6 R_d; for ~30% of galaxies the RC rises to the last point and all
  points are "inner"). On the (log g_bar, log g_obs) plane, fit each part with the EFE-calibrated
  AQUAL fitting function (his Eq. 6, from Chae & Milgrom 2022, ApJ 928, 24):
  g_MOND = g_bar nu(y_1.1) [1 + tanh(1.1 e_N/(g_bar/a0))^1.2 * nu_hat(y_1.1)/3],
  with the SIMPLE IF nu(y) = 0.5 + sqrt(0.25 + 1/y) — NOT the framework nu, NOT the RAR IF.
  Free parameters per part: a0 and the external-field strength e_tilde = sqrt(g_N,ext/a0).
  Second statistic: orthogonal residuals Delta_perp from the algebraic MOND curve.
- Data: SPARC, Q=1,2, i_obs >= 30 deg, UGC 06787 removed -> 152 galaxies, 3097 points; NO S/N>10 cut
  (deliberately, to keep inner points). Fixed Upsilon_disk = 0.5, Upsilon_bulge = 0.7 (3.6um), gas x1.33.
- Results (v2 text, verbatim): "The MCMC fit ... returns e = 0.082+0.013-0.018 with
  a0 = 1.205+0.034-0.033 e-10 (outer) and e = 0.157+0.007-0.007 with a0 = 1.105+0.050-0.048 e-10
  (inner). The inferred values of a0 are consistent, but the inferred e values show a 5.1σ difference.
  The orthogonal residual of the inner part ... (-0.031 ± 0.004) is also ≈ 5σ different from that of
  the outer part (-0.010 ± 0.002)." Universal-curve hypothesis "ruled out at 5σ". Conservative cut
  (only galaxies with BOTH parts, a0 fixed at 1.20): e_inner = 0.141 ± 0.011 vs e_outer = 0.074+0.013-0.019,
  "≈ 3.9σ". Bulgeless L < 1e11 subsample (111 galaxies): "nearly the same".
- Published/final abstract (verbatim): "Taken at face value there is a 6.9σ difference between the
  inner and outer parts on an acceleration plane which would be inconsistent with current proposals
  of modified inertia. Removing galaxies with possible systematic concerns such as central bulges or
  special inclinations does not change this trend." (v2 said 5.1σ; the published version upgraded the
  headline to 6.9σ and added "Taken at face value".)
- Direction of the effect: the INNER points sit BELOW the algebraic curve (g_obs lower than algebraic
  MOND), exactly the sign AQUAL predicts from disk flattening; CDM halos also put inner below outer
  but with the wrong shape overall.
- Chae's own MI framing (verbatim): "Modified gravity predicts an EFE-unrelated systematic deviation
  of the inner rising part ... from the algebraic MOND relation in axisymmetric flattened systems
  while modified inertia does not for circular orbits in axisymmetric systems (Milgrom 1994)."

### 1.5 Milgrom 2023 (arXiv:2310.14334), "MOND as manifestation of modified inertia" — THE REBUTTAL
- Direct hit on Chae 2022 (verbatim, his Ref. [22] = Chae 2022): "We note in this connection that the
  rotation-curve analysis of Ref. [22], which claimed to have found preference for AQUAL over MI,
  used for the MI MOND prediction the exact algebraic relation (44). This analysis thus did not test
  MI MOND, and would require reevaluation in light of the above conclusions."
- Mechanism: real tracers are not on exact circular orbits. Vertical (z) motion enters the inertia
  functional; in his two-frequency toy treatment the algebraic relation mu(V^2/Ra0) V^2/R = g_N is
  replaced by (his Eq. 46-47) a corrected relation whose bracket involves a_z/a_R and the frequency
  ratio via theta_i(omega_z/omega). Verbatim: "the correction due to z motion reduces the value of the
  predicted rotational speed relative to that predicted by the algebraic relation", it "is small at
  large radii, becomes important at small radii, and brings the predicted MI velocities closer to
  those predicted by AQUAL." I.e. the correction has the SAME SIGN and SAME LOCATION as Chae's signal.
- Also on the Q test (verbatim): "Another implication of the necessity of the above corrections it to
  reduce the predicted value of the Q parameter ... for MI relative to the value for MG, perhaps
  reducing the difference between them and diminishing the value of this parameter as a discriminant."
- Also predicts trajectory-dependence (thick vs thin disk tracers rotate at different speeds; cites
  the observed ~5% MW thick-disk lag) and extra intrinsic RAR scatter from the correction.
- IMPORTANT caveat cutting the other way: these theta corrections are MODEL-DEPENDENT ("secondary"
  predictions). What is robust ("primary") in MI: the algebraic relation holds EXACTLY only for
  exactly circular trajectories; noncircular contamination modifies it in a computable, model-keyed way.
- STATUS: no published re-evaluation of the inner/outer test with MI z-corrections exists (checked to
  2026-07); Chae has not published a rebuttal of the rebuttal. The 6.9σ number therefore tests
  "algebraic-relation-exact-for-all-tracers MI", not MI per se.

### 1.6 Milgrom 2022, PRD 106, 064060 (arXiv:2208.07073) — concrete time-nonlocal MI toy models
- Abstract (verbatim, key parts): "Models of 'modified-inertia' formulation of MOND are described and
  applied to nonrelativistic many-body systems. They involve time-nonlocal equations of motion. ...
  The models make all the salient MOND predictions. Yet, they differ from existing 'modified-gravity'
  formulations in some second-tier predictions. ... what determines the EFE, in the case of a dominant
  external field, is mu(theta <a_ex>/a0) ... theta > 1 is an extra factor that depends on the frequency
  ratio of the external- and internal-field variations. Only ratios of frequencies enter, and a0
  remains the only new dimensioned constant."
- Deep-MOND circular orbits: V^4 = M G a0 / [theta_1(1) K(0)], normalized so the algebraic relation is
  exact for circular motion. "Only ratios of frequencies enter" is the crucial contrast point for
  lane (b): Milgrom deliberately avoids a new dimensionful frequency scale; the framework's Herglotz
  kernel K(box_u/a0^2) DOES carry an absolute scale (a0/c as a frequency), so its frequency fingerprint
  is structurally different from Milgrom's ratio-only theta models.

### 1.7 Follow-ups / adjacent 2023–2026
- Desmond, Hees & Famaey 2024, MNRAS 530, 1781 (arXiv:2401.04796) — RAR fits with the nu_n / nu_delta
  families + AQUAL-style flattening corrections. Famaey & Durakovic 2025 review (arXiv:2501.17006)
  summary (verbatim): "It is therefore interesting to note a slight preference for the straight
  algebraic relation of Eq. (3) (and exact for circular orbits only in modified inertia) over the
  modified gravity correction, although not with high significance." — i.e. the newest global RC fits
  lean the OPPOSITE way from Chae 2022 (algebraic/MI-like preferred, weakly). Same paper carries the
  3-15σ RAR-vs-Cassini-Q2 tension for AQUAL/QUMOND (MG); the framework's AeST(=MG) realization
  inherits it, an MI realization is the standard escape route (see memory: cassini standing).
- Famaey & Durakovic 2025 on the MI-vs-MG endgame (verbatim): "modified gravity MOND needs a new
  scale in addition to acceleration ... to pass Solar System constraints, or that MOND rather results
  from a more radical modification of inertia"; and on wide binaries: "the jury is still out on
  whether wide binaries in the Solar neighbourhood rule out the AQUAL/QUMOND behaviour expected for a
  n = 1 or δ = 1 interpolating function (Banik et al., 2024; Chae, 2024; Hernandez et al., 2024)".
- Wide binaries (adjacent, lane-b-relevant): Chae 2023 ApJ 952, 128; Chae 2024 (ApJ, "statistically
  pure binaries", arXiv:2309.10404); Chae 2024 ApJ ad61e9; Chae 2025 (Bayesian 3D, ApJ adce09);
  2026 "36 wide binaries with accurate 3D velocities" (arXiv:2601.21728) — claim ~40% low-acceleration
  boost consistent with AQUAL-class MG. Banik et al. 2024 MNRAS 527, 4573 claim Newtonian at ~16σ
  vs MOND. CONTESTED three ways. Milgrom's MI models predict a STRONGER, frequency-ratio-dependent
  EFE (theta(0) > 1) in WBs, i.e. MORE quenching than AQUAL — nobody has confronted the WB claims with
  a CONCRETE MI kernel prediction.
- Khelashvili, Rudakovskyi & Hossenfelder 2024 (arXiv:2401.10202, "SPARC galaxies prefer Dark Matter
  over MOND"): Bayesian per-galaxy comparison, cored DM vs RAR-parameterized MOND; "Overall, our
  analysis comes out in favor of dark matter." Not an MI test (no inner/outer split, RAR IF only),
  but a methodological caution: prior choice materially moves the inferred a0.
- Petersen & Lelli's called-for follow-up (SKA-pathfinder extended LSB RCs to sharpen Q) has NOT
  appeared as of 2026-07.

---

## 2. Open ground (what has NOT been done) — cite of absence, checked 2026-07-16

Searched arXiv/ADS-indexed literature via web search (queries: inner/outer MI reevaluation, Q parameter
follow-ups, modified inertia rotation curve tests 2023-2026, MI kernel frequency dependence, wide-binary
MI EFE). Findings of ABSENCE (each is a publishable lane):

1. NOBODY has run the ring-by-ring / inner-outer test with nu = sqrt(1+1/y). Chae 2022 used the
   SIMPLE IF (0.5 + sqrt(0.25+1/y)); Desmond et al. 2024 used the nu_n / nu_delta families (delta=1 =
   Lelli RAR form); Petersen-Lelli's Q is IF-independent by construction. The framework's nu is in
   none of these papers.
2. NOBODY has run it with a horizon-FIXED a0 (zero-parameter). Chae FITS a0 per part
   (1.205 vs 1.105 e-10, "consistent"); everyone else fits or marginalizes a0. A no-fit test at
   a0 = 9.36e-11 (canonical) and 1.13e-10 (alt footing) — where the only freedom is Upsilon — is undone.
   Note Chae's fitted inner-vs-outer a0 split (1.105 vs 1.205) brackets NEITHER footing cleanly;
   the framework must be confronted with the split honestly, both footings.
3. NOBODY has computed the inner-RC (noncircular/z-motion) correction from a CONCRETE kernel.
   Milgrom 2023 supplies only heuristic two-frequency toys with free theta_i(zeta) and says a full
   treatment "would require much work beyond our scope here". The framework's K(box_u/a0^2) with the
   Herglotz measure + sum rule ∫dmu/|t| = 1 is precisely the missing concrete object: the size AND sign
   of the ring-by-ring deviation for realistic tracer populations is computable, not postulated.
   Chae's measured inner offset (Delta_perp,inner - Delta_perp,outer = -0.021 ± 0.0045 dex) then becomes
   a NUMBER the kernel must hit (or undershoot => the test discriminates framework-MI from AQUAL again).
4. NOBODY has computed an acceleration-vs-frequency split at fixed g ~ a0. Milgrom's models admit only
   frequency RATIOS; the framework kernel carries the absolute scale a0/c. Wide binaries
   (omega ~ 1e-10..1e-11 s^-1) vs galaxy outskirts (omega ~ 1e-15..1e-16 s^-1) at the SAME g/a0 is
   exactly the lane where a dimensionful kernel is falsifiable and ratio-only models are not.
   No such calculation exists in the literature.
5. The Q parameter has never been recomputed for a SPECIFIC MI kernel (Milgrom 2023 says the
   z-corrections "perhaps" shrink Q_MI - Q_MG but computes nothing). Q_framework for K(box_u/a0^2) on
   the P&L 15-galaxy sample is undone.
6. Pressure-supported / eccentric-orbit RAR offset from a concrete MI kernel (lane c): Milgrom 2023
   notes noncircular trajectories "tell us practically nothing" so far and that constraining the A2
   sector "need[s] information from test particles on noncircular trajectories" — no one has computed
   where dispersion-supported systems should sit relative to the rotation-RAR in ANY concrete MI model.

---

## 3. The repo-root agentY files (READ-ONLY recon)

Files (all dated Jul 2 12:43, uncommitted at repo root):
- /Users/carlzimmerman/new_physics/zimmerman-formula/agentY_quasistatic.out (30.8 KB)
- /Users/carlzimmerman/new_physics/zimmerman-formula/agentY_gates.out (1.7 KB)
- /Users/carlzimmerman/new_physics/zimmerman-formula/agentY_eqs.pkl (177 KB)

What they bank: the LENS-ONLY SLIP SECTOR of the covariant completion (the v5-v10 lensing/disformal
arc) — i.e. FIELD-side (MG-realization) work, NOT MI-kernel quasistatics. Specifically:
- agentY_quasistatic.out: sympy quasi-static derivation for a khronon slip sector. [SA] tensor sector:
  c_T^2 = 1 identically, alpha_M = 0 identically (GW170817 exact pass). [SB] FRW quietness: khronon
  comoving on FRW => a_mu = 0 => slip sector off cosmologically (evades the 1809.03484 GW-decay kill).
  [SC] static spherical system: the four field equations (isotropic gauge), GR gate, the on-shell slip
  Psi' - Phi' and phantom Delta_Psi expressions, the lens-only condition Delta_Phi = 0 with two closure
  branches (branch 1: c30 = -(c10+c20)/Y; branch 2: (c10-c20)Y + c30 Y^2 = 2), and the J = Y/4 singular
  surface logged as a dead end.
- agentY_gates.out: numeric gates against banked agentW/agentI numbers — slip amplitude targets
  2(nu-1) at g_bar = 1e-13/1e-12/1e-11 (61.2/19.4/6.2, McGaugh nu, GATE OK), Cassini conjunction margin
  x1.3e7 (GATE OK), and [SGA] the kinematic-trackability check: the slip operator CAN carry nu(y);
  the matching integral c20(Y) is finite (trackable) for all four banked shapes INCLUDING
  "fw sqrt(1+1/y): c20(Y(y=0.1)) = -1.5473e+06 [finite: trackable]".
- agentY_eqs.pkl: dict of 11 sympy srepr strings — eqN/eqM/eqC/eqL (the four quasi-static field
  equations), cond_rb1/cond_rb (the rhob' and rhob lens-only conditions), rest2 (geometric remainder),
  slipgrad (the on-shell slip), DeltaPsi (the phantom), Ch2_b, branchPhi1 (= 2*J1*chi1).

Reuse vs supersede for THIS suite: neither. These files bank the MG/lensing-side slip sector and
should stay untouched (repo FROZEN). They are ORTHOGONAL to the MI fingerprint lanes, which live on
the trajectory side (kernel K acting along u, ring-by-ring exactness, frequency response). The one
directly reusable ingredient: the [SGA] gate confirms the framework nu = sqrt(1+1/y) is analytically
well-behaved in the matching-integral machinery (finite c20), and the banked slip-amplitude/Cassini
gate numbers are the cross-check targets any MI-side claim must not contradict. Do NOT cite agentY as
evidence about MI quasistatics — it is the khronon (field) sector.

---

## 4. Known failure modes / traps the Compute lanes must handle

From the papers themselves (these killed or weakened prior claims — build the gates in from the start):

1. BEAM SMEARING + inner-point data quality. Chae's signal lives in the INNER rising parts — exactly
   where HI beam smearing, bulge velocity dispersion (asymmetric drift), and noncircular streaming
   corrupt V_obs, and where SPARC errors are largest (the S/N<=10 points Chae deliberately kept are
   "mostly from the inner rising part"). Chae's robustness cuts (bulgeless, L<1e11: "nearly the same";
   both-parts-only: 3.9σ) mitigate but do not eliminate; SPARC does not model beam smearing per point.
   Any framework re-run must show the verdict survives (a) dropping the lowest-S/N inner points,
   (b) the bulgeless subsample, (c) an inner-radius floor (e.g. R > 2 beam widths where available).
2. INCLINATION. i < 30 deg already cut, but 1/sin(i) errors are correlated within a galaxy and inflate
   inner/outer coherence; Chae cites Banik et al. 2022 as the cautionary tale. Petersen-Lelli's Q
   partially cancels inclination (velocity ratios); the inner/outer offset does NOT cancel it.
3. UPSILON (M/L) DEGENERACY. Chae FIXES Upsilon = 0.5/0.7. The inner parts are disk/bulge dominated,
   so an Upsilon error moves inner g_bar directly (outer parts are gas-dominated and immune). A ~20-30%
   Upsilon shift slides inner points along g_bar and can mimic or erase a sub-0.03 dex offset.
   Desmond et al. 2024: freeing Upsilon changed the best-fit IF family (delta 1 -> 2.5, bulgeless).
   Framework lanes must scan Upsilon (at least 0.5 ± 0.1 grid + the repo's 0.70 mlfit convention —
   see real_research/rar_framework_a0_mlfit.py, 0.108 dex @ Upsilon=0.70) and show the MI/MG verdict
   per Upsilon. The memory rule applies: RAR-level "20% off" claims are interpolation/M-L artifacts.
4. EFE CONTAMINATION. Chae's discriminating parameter e_tilde ABSORBS everything that lowers inner
   g_obs — it is "EFE-shaped" but his own reading is that e_inner = 0.157 "cannot be due to the EFE"
   (cosmic value 0.071). If the fitting function forces deviations into an e-like parameter, any inner
   suppression (real MI kernel effect, Upsilon error, beam smearing) shows up as "impossible EFE" and
   gets scored for AQUAL. A framework re-run should fit the framework's OWN inner-correction shape,
   not Chae's Eq. (6), and treat the environmental EFE with the real per-galaxy field (repo:
   real_research/sparc_efe_real_externalfield.py, per-galaxy environment null banked).
5. THE MILGROM TRAP (tracer noncircularity). Do not repeat Chae's error in reverse: the framework's
   MI prediction for the inner parts is NOT the bare algebraic relation either — gas z-motion is small
   (cold gas near midplane) but radial streaming and finite thickness enter the kernel. The suite must
   COMPUTE the framework correction (lane c machinery) before scoring the inner offset, and quote both
   the bare-algebraic and kernel-corrected verdicts.
6. IF-FAMILY LEAKAGE. Chae's 6.9σ is measured against the SIMPLE IF; the residual of the data from the
   algebraic curve depends on which nu is the reference (his own Sanders 2019 discussion shows the
   standard-IF apparent agreement flipping sign against the simple IF). All framework runs must use
   nu = sqrt(1+1/y) as the reference curve and re-derive the inner/outer offsets from scratch —
   never transplant Chae's residuals.
7. A0 FOOTING FORK. Run canonical 9.36e-11 AND alt 1.13e-10 everywhere; show the spread. Chae's fitted
   inner/outer a0 (1.105/1.205e-10) straddle the alt footing and sit ~15-30% above canonical; a fixed-a0
   rerun changes the leverage arm of the test (his own conservative fixed-a0 variant dropped 5.1σ -> 3.9σ).
8. VERSION DRIFT IN THE TARGET NUMBER. v2 = 5.1σ, published = 6.9σ ("Taken at face value"). Pin which
   number is being confronted; reproduce the statistic from SPARC directly rather than quoting either.
9. SELECTION/PRIOR SENSITIVITY. Khelashvili et al. 2024: the inferred a0 credible interval is
   prior-dominated in Bayesian RC fits; MOND "preferred by galaxies which lack precise data". Any
   Bayesian lane must show prior-independence of the MI/MG discriminant.

---

## 5. Local data assets (for the Compute lanes)

- SPARC per-galaxy mass models: 175 files at
  /Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/sparc_data/*_rotmod.dat (READ-ONLY)
  + master table real_research/data/SPARC_Lelli2016c.mrt and sparc_master_clean.csv.
- Framework RAR baseline: real_research/rar_framework_a0_mlfit.py (0.108 dex @ Upsilon=0.70 — the
  mandatory pre-flight before relaying any framework deficit; memory rule).
- Gaia wide-binary dry run banked: /Users/carlzimmerman/new_physics/prep_2026/gaia_dr4_prep/
  wide_binary_pipeline.{py,out} — gates PASS at injected gamma = 1.00/1.09/1.33, sigma(gamma) = 0.019
  @ N=30k, 3σ separation of MI 1.09 vs Newton needs N ~ 12,187 pairs; both a0 footings wired in.
- agentY_* repo-root files: lens-only slip sector (Sec. 3) — read-only context, not to be superseded.

## 6. Bottom line for the suite

The MI-vs-MG rotation-curve question is CONTESTED, not settled: Chae 2022 claims 6.9σ (published;
5.1σ in v2) against "current proposals of modified inertia" using the exact algebraic relation as the
MI prediction; Milgrom 2023 answers that this "did not test MI MOND" because noncircular tracer motion
corrects the MI prediction toward AQUAL in exactly the inner regions; Petersen-Lelli's Q is a 1.5σ
MG-leaning null on 15 galaxies; the newest IF-family fits (Desmond et al. 2024, per the Famaey &
Durakovic 2025 review) show "a slight preference for the straight algebraic relation ... although not
with high significance" — the OPPOSITE lean. Nobody anywhere has used nu = sqrt(1+1/y), a fixed
horizon a0 (either footing), or a concrete kernel. All three compute lanes (ring-by-ring exactness,
frequency split at fixed g, off-circular offset) are open ground, and each has a pre-registered trap
list (Sec. 4). Verify wins and deficits with equal rigor; the Desmond-lean is NOT a framework win
until reproduced under the framework's own nu, and the Chae-lean is NOT a framework kill until the
kernel-corrected inner prediction is computed.
