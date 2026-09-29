# B1 pre-registration: the Multiple Point Principle (MPP) as a mechanism for the UV gauge couplings

*Written 2026-09-29 BEFORE any published number was fetched and BEFORE any B1 computation was run. Everything about the MPP literature below is from memory and is marked RECALLED; none of it may be used in a verdict. Later amendments are appended at the bottom, never edited in.*

## The mechanism (as recalled)

The Multiple Point Principle (Froggatt, Nielsen, Bennett) says: nature sits at a point of parameter space where several vacua of the same theory are degenerate. Applied to gauge couplings (Bennett and Nielsen, Int.J.Mod.Phys. A9 (1994), "Predictions for non-Abelian fine structure constants from multicriticality"; the U(1) follow-up, 1995; Froggatt and Nielsen 1996), the claim is that at the Planck scale the three Standard Model couplings sit at the critical (phase-transition or triple-point) values of the corresponding lattice gauge theories: compact U(1) (Wilson or Villain), SU(2) and SU(3), with the generalized (fundamental plus adjoint) action supplying the multicritical point. The lattice critical coupling (a pure number from lattice Monte Carlo) is converted to 1/alpha_i(M_P) by the paper's own group factors and its U(1) charge-lattice factor. There are no adjustable knobs in the claimed prediction.

## Independence from this programme

This route is EXTERNAL to the kappa = 1/2, Z = sqrt(32 pi/3) framework. It uses neither. A pass would not support the framework, and a fail says nothing about it. Nothing here touches the walled sector's status.

## Targets (lane Y1, validated running, imported read-only)

1/alpha_i(M_P) at M_P = 1.22089e19 GeV: (Y, SU(2), SU(3)) = (55.234, 49.203, 52.971), relative errors (0.23%, 0.021%, 0.12%). Obtained by importing y1_lib exactly as `../A1_kz_rule_search/a1_kz_rule_search.py` does (sys.path inserts of Y1_running_precision, B_rg_asymptotic_safety, N1_joint_couplings, U3_invented_uv_boundary, D_calibration_bar; `L.run_central(mu_max=1e21)`; `tr.A(mu)` returns (1/aY, 1/a2, 1/a3)). The script reads these from the running code; the numbers above are the expected values, checked at run time.

## Declared criteria (fixed now)

1. **Verified-only rule.** A published number enters a verdict only if I read it in the primary text (arXiv abstract or full text or a published table) and record the source id and a short quotation. A number I recall but cannot read is UNVERIFIED and is never used. If the essential conversion numbers cannot be verified, the lane's outcome for that coupling is UNVERIFIED (not a pass, not a fail).
2. **Pass per coupling.** The MPP prediction passes a coupling only if the Y1 target lies within k = 2 of the prediction's own STATED uncertainty (combined in quadrature with the Y1 error), AND that uncertainty is derived from the cited lattice errors or the papers' own stated range, not chosen after seeing the target. If a paper states a prediction without an uncertainty, I derive one only from the cited lattice errors on the critical coupling; if that is impossible the coupling is UNDECIDABLE.
3. **Informative pass.** A pass is called INFORMATIVE only if the stated prediction uncertainty is 5% or smaller; a pass with a wider band is WEAK (it excludes little). This threshold is declared here, before the numbers are known.
4. **Zero-knob.** The route passes "zero-knob" only if the U(1) charge-normalisation convention and the choice of lattice action are fixed by the cited papers, not tuned. If either has to be picked by me, the route is not zero-knob and any agreement is reported as such.
5. **Fail.** A coupling FAILS if the prediction with its stated uncertainty (criterion 2) excludes the target at more than 2 sigma. The route FAILS if two or more of the three couplings fail.
6. **Undecidable.** Missing uncertainty, missing conversion rule, or a convention the papers do not fix.

## Ceiling stated in advance

Even a complete pass fixes the Planck-scale couplings to at best a few percent, given the size of lattice critical-coupling uncertainties, the generalized-action spread and the Planck-scale threshold ambiguity. The low-energy alpha = 1/137.035999177 could NOT then be reproduced to more than about 2 digits by this route. "Exact to many decimals" is not reachable by this mechanism. A pass would be a mechanism-level result, not a derivation of the measured digits; a fail closes one published mechanism class.

## Expected outcome

UNKNOWN. I recall that the authors claimed agreement with the running couplings at a level of order ten percent or better, but I do not recall the numbers and do not use that recollection. Whether the claimed agreement survives against Y1's precise targets, with an uncertainty derived from lattice errors, is exactly what this lane tests.

## Control

`python3 b1_mpp_confrontation.py MUTATE` perturbs a converting factor (the U(1) charge factor) and must change the verdict (exit 1 if the control fires; exit 3 if broken). The real run exits 0 iff all declared internal checks pass; the verdict is reported, not asserted.

## Optional step

If, and only if, the primary source supplies a mechanism relating the Planck-scale MPP couplings to the low-energy alpha, I will run Y1's running down to the Thomson limit with propagated error and report how many digits that supports.

## Amendments

### Amendment 1 (written after reading the primary texts, BEFORE writing or running b1_mpp_confrontation.py; no Y1 number was compared to any MPP number when this was written, beyond having seen that the papers print their own comparison values)

What was found while fetching (facts, not verdicts): the wanted numbers are in D.L. Bennett and H.B. Nielsen, hep-ph/9311321 (non-Abelian, 1993/94), and D.L. Bennett's thesis hep-ph/9607341 and the journal paper hep-ph/9607278 (all three couplings; U(1) added). The arXiv id hep-ph/9411438 named in the task was recalled wrongly (it is an unrelated heavy-quark paper) and is not used. Froggatt-Nielsen 1996 concerns the Higgs/top criticality, not the gauge couplings, and is not used.

What this changes in the plan (declared now):

1. **Which numbers are the prediction.** The papers print their own Planck-scale predictions. The script takes as CENTRAL values the papers' printed ones: SU(2) 49.5 and SU(3) 56.7 (Table 13 of hep-ph/9607341 / Table 8 of hep-ph/9607278, 'continuum corrected continuum limit', i.e. three times the exponentiated per-group value 16.5 and 18.9), and for U(1) the authors' viewpoint-a headline: the mean of the four rows they mark as most correct in their Table 12, which the abstract of hep-ph/9607278 quotes as 56 +- 5. Viewpoint b (59.7 +- 3.5) is reported as the alternative. The SU(2) and SU(3) numbers are ALSO recomputed from the printed lattice triple-point couplings and the printed formula as an arithmetic check, not as a replacement.
2. **Uncertainty, two ways, fixed now.** PRIMARY: the paper's own stated uncertainty at the Planck scale (SU(2): 6 and 3.5 in quadrature; SU(3): 6 and 6 in quadrature; U(1) viewpoint a: 4.5; the papers say the absolute uncertainty in 1/alpha is the same at all scales). SECONDARY (tighter): my own propagation of the papers' quoted Monte Carlo errors (5% on beta_adj, 10% or 20% on beta_f) plus the papers' exponentiated-versus-not spread, multiplied by N_gen = 3; for U(1) the paper's viewpoint b. A coupling is called PASS ROBUST only if it passes under both. Criterion 2 (2 sigma) and criterion 3 (informative only if sigma/prediction <= 5%) stand unchanged.
3. **U(1) cannot be recomputed from lattice couplings by me.** The U(1) prediction is (enhancement factor ~6.5 from a hexagonal-lattice model with a first-order-ness interpolation) x (continuum coupling from a fit to Monte Carlo data at a modelled Delta gamma_eff). I can only transcribe the printed table rows and check their internal arithmetic (1/alpha_cont x enhancement = prediction). The printed lattice critical value in the fit is Wilson beta_c = 1.0106 and Villain 0.643 (the recalled 1.0111 in the task text is not used). So the U(1) row of this lane tests the PAPER'S OWN NUMBER against Y1, not an independent recomputation; this is stated in the result.
4. **Zero-knob status.** The authors themselves present many variants (Wilson vs Villain action, three treatments of Z2/Z3 discrete subgroups, tau = 0.79 vs 1, exponentiated vs not, viewpoints a and b). I fix the U(1) choice to their headline (viewpoint a) before comparing, and report the full spread of their variants and how many of them a 2-sigma criterion would accept. The SU(2)/SU(3) triple points are read off published figures by the authors (graphical extraction, quoted 5-20% Monte Carlo uncertainty); the underlying lattice papers (Bhanot, Bachas-Dashen, Drouffe-Zuber) were NOT read by me. The gauge group SMG^3 (three generations) and the N_gen weakening factor are assumptions of the model, not lattice results. The route is therefore zero-knob only in the sense that the authors' choices are fixed by their papers; the U(1) factor '6' was introduced in 1993 as 'phenomenologically desirable' and only later given a derivation.
5. **Optional step (low-energy alpha).** The thesis supplies a mechanism: alpha^-1(0) = alpha_Y^-1(M_Z) + alpha_2^-1(M_Z) + a constant, the constant being the measured running from M_Z to zero. I will report the analogous prediction using Y1's targets to fix the running difference (boundary shift additive), with propagated uncertainty and the number of digits it supports, and state that the constant is measured input (charged-fermion masses, hadronic vacuum polarisation), so this is not an alpha derivation.

### Amendment 2 (written after the FIRSTRUN, which is kept as b1_mpp_confrontation_FIRSTRUN.out and exited 1)

The first run of the script failed one declared internal check: C2 for SU(3) (recomputed per-group 1/alpha of 18.02 not exponentiated and 19.41 exponentiated against the printed 17.7 and 18.9). Cause, checked by hand: the papers print the SU(3) adjoint contribution 4 pi (3/8) 5.4 = 25.45 as '25' and carry the rounded 25 and 1.7 through the tables; the printed table is arithmetically self-consistent with those rounded intermediates but is 0.3 to 0.5 per group (about 1.5 in 1/alpha at the Planck scale) below an unrounded recomputation. This is a property of the source, not a script error. Amendment: the SU(3) C2 check is split into (i) a REPORTED discrepancy, (ii) a hard check that the papers' own rounded intermediates reproduce the printed values, and (iii) a sensitivity line showing the SU(2) and SU(3) statuses under the unrounded centrals. The primary verdict continues to use the printed central values, as fixed in Amendment 1. No threshold, target, uncertainty or criterion was changed.

### Amendment 3 (context line added after the second run; changes no verdict)

Because every pass in this lane is WEAK (stated uncertainty 8 to 15% of the prediction), the script now also prints how easily a prediction of that width would pass by chance under a declared broad prior (each 1/alpha_i(M_P) uniform on [20,100]). It is context for reading the result, not a criterion, and it enters no exit code.
