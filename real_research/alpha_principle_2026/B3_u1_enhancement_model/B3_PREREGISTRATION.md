# B3 pre-registration: how much of the Multiple Point Principle (MPP) U(1) pass is derived, and how much is chosen?

*Written 2026-09-30 BEFORE any new primary text was fetched for this lane and BEFORE any B3 computation was run. What I had read at this point: the campaign summary and the B1/B2 result files, ledger, pre-registration and scripts (the second-hand record of the papers). Everything about the papers that I state below comes from those lane files or from memory and is marked RECALLED where it does not; none of it enters a verdict until read in the primary text. Later amendments are appended at the bottom, never edited in.*

## Goal

Lanes B1 and B2 found that the MPP prediction for the hypercharge coupling, 1/alpha_Y(M_P) = 56.25 +- 4.5 (viewpoint a; 51.8 to 69.3 over eight printed variants), agrees with lane Y1's 55.234 (0.23% error). The SU(2) and SU(3) numbers come from lattice triple points that B2 could partly re-measure. The U(1) number cannot be recomputed from a lattice measurement: B2 showed the lattice input (Wilson beta_c = 1.0113 +- 0.0010) moves 1/alpha_Y by only +-0.012, and the value is set by two model inputs that are the authors' own: an enhancement factor (6 to 8.04; 6.5, 6.662 used) and a continuum correction Delta-gamma_eff (matching Y1 at enhancement 6.662 needs 0.0629; a shift of 0.01 moves 1/alpha_Y by 2.1). Also, in 1993 the factor 6 was introduced as "phenomenologically desirable" (BN93 footnote 7). This lane is THEORY-SIDE: it maps the U(1) argument link by link, re-derives what can be re-derived independently, and decides how much of the pass is derived, how much is a choice fixed by a principle before the comparison, and how much was tuned.

## Independence from the programme

MPP uses neither kappa = 1/2 nor Z = sqrt(32 pi/3). Nothing here supports or refutes the framework. alpha stays an INPUT.

## The chain to be mapped (links L1 to L8)

* **L1. Lattice critical coupling.** Compact U(1) lattice gauge theory (Wilson and Villain actions) has a phase transition (Coulomb to confinement) at beta_c (Wilson 1.0106 printed; Villain 0.643 printed; B2 measured 1.0113 +- 0.0010 for Wilson). Question: is this a measured lattice number? (Expected: yes. B2 validated it.)
* **L2. Lattice beta_c to a continuum fine-structure value alpha_crit.** The conversion beta = 1/e^2 (lattice normalisation) to alpha = e^2/4pi, plus the correction from the lattice-regulated Coulomb-phase coupling to the continuum coupling; the authors use a fit alpha_cont = 0.20 - 0.24 (Dgamma/(beta_c+Dgamma))^0.39 (as quoted in B2 from hep-ph/9607278 eq. (139)). Questions: where does this functional form come from (a fit to Monte Carlo data of an auxiliary quantity, an analytic argument, or an ansatz), and how many fitted parameters does it carry?
* **L3. The charge-lattice / hexagonal-lattice enhancement factor.** The MPP gauge group is SMG^3 broken to the diagonal. For the non-Abelian factors the effective coupling weakens by N_gen = 3. For U(1) the authors claim a weakening by N_gen(N_gen+1)/2 = 6 (second-order transition) up to about 6.5 to 8.04 (residual first-orderness, interpolated with a parameter tau = 0.79 or 1), from a charge-lattice (hexagonal) argument. Questions: what is the derivation (the structure of the allowed charge lattice of three U(1)s with the diagonal subgroup)? Is the factor 6 = N(N+1)/2 derived or postulated? Is the interpolation tau a fit?
* **L4. Hypercharge normalisation.** Which U(1) coupling is meant: g' with SM hypercharge Y (so that Q = T3 + Y, or Y/2), the SU(5) coupling 5/3 g'^2, and what is the minimal charge on the lattice? The Z6 quotient (SU(3) x SU(2) x U(1)_Y / Z6) fixes the allowed charges and therefore the lattice's effective minimal charge; the lattice beta_c is defined for a minimal charge 1. Questions: does the paper's alpha_Y use Y/2 or Y, and does the minimal charge used equal that of the lattice? A normalisation slip of 6/5 or 4 is much larger than the 0.23% match.
* **L5. Delta-gamma_eff (the continuum correction).** The extra term that shifts the effective Villain/Wilson coupling from the pure-U(1) critical value; the authors build it from contributions of discrete subgroups (Z2, Z3) of the nonabelian factors and monopole charge dependence ("Z2 only", "Z2+Z3", "(Z2+Z3)/2", "Z2/2+Z3"). Questions: what physical contribution is it (a one-loop lattice-to-continuum difference, extra non-U(1) matter, monopole-charge dependence), how is each of the four variants constructed, and was the choice among them (and the starred subset) made before or after comparison with the extrapolated data?
* **L6. Action choice.** Wilson versus Villain; fixed by the authors' headline or open.
* **L7. Combination.** 1/alpha_Y(M_P) = enhancement x 1/alpha_cont(Delta-gamma_eff, beta_c): pure arithmetic once L1 to L6 are fixed.
* **L8. Identification of the Planck scale and one-loop matching to Y1.** The papers do not state M_Planck; moving it by a factor 3 shifts Y1's 1/alpha_Y by 1.2. This is inherited from B1 and is only reported.

## Status column (to be filled by the script and the result file, per link)

One of exactly four labels:
* **DERIVED-INDEP** : the paper derives it and I re-derived it independently (a different route, not a re-run of the paper's formula).
* **DERIVED-ARITH** : the paper derives it and I could only check arithmetic against its printed intermediates.
* **CHOSEN** : a phenomenological input or a selection among variants; the paper does not derive it from a principle independent of the answer.
* **UNDETERMINED** : I cannot tell from the sources or by a cheap computation.

## Declared criteria for the classification of the U(1) pass (fixed now)

1. The U(1) pass is **DERIVED** only if every link L1 to L6 is DERIVED-INDEP (L8 and the Planck-scale ambiguity are reported, not graded).
2. **CONDITIONAL** if at least one link is CHOSEN but the choice is fixed by a stated principle (named in the primary text, before the comparison with data is described) and the resulting prediction, under the other principled alternatives the paper itself considers, stays inside Y1's value within the paper's stated uncertainty.
3. **TUNED** if any link was selected because it improved the match to data, which I establish only from the paper text showing the order of events (e.g. a factor introduced as "phenomenologically desirable" or a variant retained as "most correct" by the comparison with the extrapolated couplings). I will cite the passage. If the text shows the order of events ambiguously, the classification is UNDETERMINED for that link and the pass is classed no better than CONDITIONAL-WEAK (conditional with an unresolved order of events); I do not guess.
4. A link graded CHOSEN or TUNED, but whose range is shown by the sensitivity test to leave the pass unchanged (all alternatives pass), is reported as "chosen but not decisive".

## Sensitivity test (declared now, before any number is computed)

Vary each chosen link over the range the papers themselves print or the physical alternatives, one at a time and then jointly:

* Enhancement factor: 3 (naive N_gen), 4, 6 (N(N+1)/2), 6.5, 6.662, 8.04 (also 6.5 with tau = 1, and the papers' per-row printed factors).
* Action: Wilson (beta_c 1.0106, and B2's 1.0113) versus Villain (0.643).
* Delta-gamma_eff: 0 to 0.11 (the printed rows range 0.040 to 0.109), plus every printed variant.
* Hypercharge normalisation alternatives, if L4 reading shows a real ambiguity (to be defined in an amendment after reading).

For each, report 1/alpha_Y(M_P), the spread, and which values pass Y1's 55.234 (+- 0.23%) at (a) the stated MPP uncertainty 4.5 (2 sigma), and (b) Y1's own error alone (i.e. a sharp "prediction" criterion, 2 sigma = about 0.25). The fraction of the declared grid that passes at 4.5 is reported as the "pass volume"; a pass volume near the area of the uniform-prior window means the U(1) match carries little information.

## Re-derivation test (script)

The script `b3_u1_chain.py` must reproduce the papers' printed 1/alpha_Y variants (51.8 to 69.3, eight rows, both tau) from the chain's formulae (1/alpha_cont from Delta-gamma and beta_c through the quoted fit; enhancement from the quoted tau interpolation or the printed per-row factors; product), with every link an explicit commented function. Declared internal checks: reproduction of each printed row within rounding; reproduction of the abstract's 56.25 mean; closure of the 6 = N(N+1)/2 identity for N = 3. The link classification is REPORTED, not asserted. The MUTATE control breaks one link (enhancement factor replaced by the naive 3, or the hypercharge normalisation swapped) and must flip a checked reproduction outcome: exit 1 when the control fires, 3 if broken. Real run exits 0 iff all declared internal checks pass. If a first run fails a check, FIRSTRUN output is kept.

## Cheap independent checks (candidates, to be given their own thresholds in an Amendment BEFORE each is run)

Candidate checks, only if cheap: (i) the charge-lattice weakening via a one-line effective-action argument; (ii) the hexagonal-lattice versus hypercubic critical-coupling ratio; (iii) the one-loop SM-content estimate of Delta-gamma using lane Y1 machinery; (iv) the hypercharge normalisation and Z6 minimal-charge bookkeeping. Any that is not cheap or not well posed is marked UNDETERMINED. I will not guess.

## Honest expected outcome

UNKNOWN. My prior (stated now): the enhancement factor and Delta-gamma_eff will turn out to be partly phenomenological (the 1993 footnote already says the 6 was introduced as phenomenologically desirable); I expect the U(1) pass to classify as CONDITIONAL at best, with the possibility of TUNED for the enhancement factor, and I expect the sensitivity test to show that a wide fraction of the printed range passes a 4.5 uncertainty (so the pass is weak even on its own terms). I hold this as a prior, not a finding; a finding that the chain is derived and robust would be reported as such.

## Ceiling (stated in advance)

Whatever the classification, MPP fixes the Planck-scale couplings to at best several percent (B1: 8 to 15%), so the low-energy alpha could be reproduced to about one to two digits; the measured value has eleven. This lane cannot change that ceiling. Nothing is claimed about the framework; alpha stays an INPUT, kappa = 1/2 FITTED.

## Reading and quoting rules

At most one short quote (under 15 words) per source; paraphrase otherwise. Every number: source and VERIFIED (read in the primary text) or RECALLED (never used in a verdict). No person's name and no home-directory path in any file I write (the paper authors are cited by arXiv id and the label BN93, BT96, BN96).

## Amendments


### Amendment 1 (written after READING the primary texts BN96 = hep-ph/9607278 (full U(1) sections 3 and 5), BN93 = hep-ph/9311321 (footnote 7), BT96 = hep-ph/9607341 (tables, same content as BN96), BNF97 = hep-ph/9710407, N25 = arXiv 2403.14034 (v3), and the compact-QED paper hep-lat/0210010; BEFORE writing or running b3_u1_chain.py. No B3 number has been computed yet; I have only checked by hand, while reading, that a few printed rows are self-consistent.)

What reading changed in the chain (facts, not verdicts):

* The chain as printed is: L2 alpha_cont = 0.20 - 0.24 (x)^0.39 (Wilson) or 0.20 - 0.33 (x)^0.52 (Villain), x = Dgamma/(beta_c + Dgamma) [BN96 (139),(140)], a fit by other authors to Coulomb-potential Monte Carlo data; L3 enhancement = 6 + 6(1.34-1) eta/tau with eta = DeltaW/0.377, DeltaW = 0.252 (Dgamma + Dgamma_corr1)^(1/3) (Wilson), 0.16 Dgamma^0.29 (Villain), tau = 0.79 or 1 [BN96 (131)-(138)]; the base value 6 is the length-squared of the diagonal vector (1,1,1) in a hexagonal (fcc, A3) identification lattice [BN96 (49),(126),(127)]; 8.04 = 6 x 1.34 is the 'volume approximation' [BN96 (128),(129)]. L5 Dgamma_eff = sum over N = 2,3 of (1/N^2) beta_crit,ZN DeltaS_ZN [1 + xi (sinh(2 beta)/beta_crit - 2 cosh(2 beta))] with xi = 0.04 [BN96 (122), Table 4], then an 'improved' version (Table 7) by an iterative <cos^p theta> factor. L4 normalisation: the lattice critical coupling is identified with the charge quantum of U(1)/Z6, i.e. the left-handed positron (y/2 = 1), by the 'ZNmax factor group rule' plus a self-described speculative argument (BN96 sec. 3.1.3).
* Order-of-events passages found (paraphrase unless quoted): BN93 footnote 7 calls the factor 6 'phenomenologically desirable' while the work was 'in progress'; BN96 sec. 5.x (before the hexagonal derivation is applied) states 'Phenomenologically, a factor of roughly 6 rather than 3 is needed' for the cubic-lattice failure; BT96 states the whole model is justifiable 'a posteori' by phenomenological success; BN96 states the hexagonal lattice was 'invented' as the way to realise multiple-point criticality for U(1)^3 (tightest packing = most phases); BNF97 says the interaction coupling was 'invented'. The text does not date the weighting of Z2 by 1/2 against the comparison with data. The printed star markers differ between the older table (Table 6) and the final table (Table 7) for the Wilson 1/2(Z2+Z3) row.
* A newer paper by one of the original authors (N25) says the Abelian coupling 'was not so well predicted' by the earlier attempt and replaces the U(1) lattice step by a different, fitted construction: the programme itself did not carry the U(1) chain forward.

Pre-registered independent checks (thresholds fixed NOW, before any is run):

* **CK1 (L3 base factor, pure algebra).** Enumerate the hexagonal identification lattices generated by the three axis vectors with Gram matrix g_ij = 1 on the diagonal and s_ij/2 off the diagonal, s_ij = +/-1. Require positive-definiteness, 12 equal-length nearest neighbours, and S3 permutation symmetry among the three U(1) factors (the AGUT confusion symmetry, BN96 sec. 2.2). Compute |d|^2/|nn|^2 for the diagonal d = (1,1,1). PASS (link L3-base = DERIVED-INDEP given the premises hexagonal-lattice and diagonal-subgroup identification) iff the S3-symmetric positive-definite class is unique and gives exactly 6; if another admissible sign class exists with a different diagonal ratio and is S3-symmetric, the link is CHOSEN. The premises themselves (SMG^3, tightest-packing principle) are listed as premises, not tested.
* **CK2 (L5, Z2 and Z3 critical couplings).** Compute the 4D Z2 and Z3 gauge-theory critical couplings from exact self-duality (e^J = 1 + sqrt(N), J = beta(1 - cos(2 pi k/N)) with k = 1) and compare with the printed beta_crit,Z2 = 0.44, beta_crit,Z3 = 0.67. PASS iff both agree within 0.005. (This tests only the critical couplings, not the plaquette jumps DeltaS.)
* **CK3 (L5 arithmetic).** Reproduce Table 4 (0.0473, 0.0393) from eq. (122) with the printed inputs: PASS iff within 0.0003. Reproduce the Table 7 improved Dgamma values by the iterative cos-power procedure: PASS iff all four Wilson and four Villain values within 3% (it is a reconstruction of an underspecified procedure; a failure is reported as 'not reproducible', link stays DERIVED-ARITH at best only for the part that reproduces).
* **CK4 (L2 and L3 arithmetic).** Reproduce, for all eight rows of Table 7, 1/alpha_cont (within 0.02), the enhancement at tau = 0.79 and tau = 1 (within 0.006) and the prediction (within 0.25). This is the re-derivation test of the script's declared internal checks.
* **CK5 (L3 / L2 input staleness).** Replace the 1985-era plaquette-jump input DeltaW(gamma = 0) = 0.016 by the modern value 0.0267 (hep-lat/0210010 gap, VERIFIED) and the printed beta_c = 1.0106 by 1.01113 (same paper, VERIFIED) and report the shift of 1/alpha_Y for the starred rows. No pass/fail; reported as a sensitivity (expected effect small).
* **CK6 (L4 normalisation).** Tabulate the alternative normalisations (positron unit q = 1 as used; q = 2 [Qour = Qmax/12]; doublet unit [x36]; Y instead of Y/2 [x4]; SU(5) 3/5 [reporting only, not a different coupling]) and report which alternatives land within 2 sigma of Y1. Report only.
* **CK7 (L5 plaquette jumps).** NOT run unless cheap: a Z2/Z3 Monte Carlo for DeltaS_ZN. If not run, the inputs 0.44 and 0.56 are marked 'literature value not independently verified' (UNDETERMINED for that sub-link).
* The remaining sub-links, namely the Luck-fit coefficients (0.20, 0.24, 0.39; 0.33, 0.52), the volume-approximation factor 1.34 and its B4, B6 coefficients, the linear interpolation in eta/tau, the cube-root law with A = 0.252 and 0.16, the weight 1/2 on Z2 and the 'Z3 full or half' ambiguity, are inherited model inputs: marked DERIVED-ARITH or CHOSEN or UNDETERMINED according to the text; no attempt to re-derive them.

Declared sensitivity grid (made concrete now): enhancement in {3, 4, 6.0, 6.5, 6.662, 8.04} (external, for the scan) AND the model's own interpolation; action in {Wilson, Villain}; Dgamma_eff in 0 to 0.12 in steps of 0.005 and the eight printed values; beta_c in {1.0106, 1.01113}; pass window: |1/alpha_Y - 55.234| <= 2 x sqrt(4.5^2 + 0.127^2) (the stated MPP uncertainty, 'wide') and <= 2 x 0.127 (the sharp Y1-only window). Pass volume = fraction of the (enhancement, Dgamma_eff) grid in the wide window, for Wilson with beta_c = 1.0106, restricted to enhancement in {6.0, 6.5, 6.662, 8.04} and Dgamma_eff in 0.04 to 0.11.

### Amendment 2 (after the first run of b3_u1_chain.py, kept as b3_u1_chain_FIRSTRUN.out)

The first run printed all checks as PASS but crashed at the very end while writing b3_results.json (a numpy integer was not JSON-serialisable; exit 1 from the traceback). This is a script bug in the output step, not a failed declared check; fixed by casting to float/int. No threshold, criterion or number was changed. What the first-run output showed is NOT the basis of any threshold below (it only motivated CK7).

CK7 is now declared cheap enough to run, with its threshold written BEFORE it is run: a small C Monte Carlo of the 4D Z2 and Z3 gauge theories (action beta * sum over plaquettes of cos(theta), theta in multiples of 2 pi/N) at the self-dual coupling (CK2), lattice 8^4, Metropolis, one cold-start and one hot-start chain, 400 thermalisation sweeps and 2000 measurement sweeps each, plaquette observable <cos theta> in each metastable phase; the jump DeltaS_ZN is the difference of the two chain averages. PASS (printed input confirmed) iff each jump agrees with the printed value (Z2 0.44, Z3 0.56) within 10%. The method measures metastable branches at the transition point, so a systematic bias is possible (finite size, metastability lifetime); a FAIL therefore marks the sub-link UNDETERMINED (not refuted), and a PASS marks it DERIVED-INDEP only for the jump value, not for its use in eq. (122). If a chain tunnels between phases (the two averages coincide or flip), the run is declared inconclusive and the sub-link stays UNDETERMINED.

### Amendment 3 (after the second and third runs)

(i) The first run of the MUTATE control (before CK7 was added) exited 3 ('control broken'): a bug in the script's control logic (it searched the failed-check list for the bare tag 'CK4' while the list holds full check names), not a property of the chain. The CK4 check itself had already printed FAIL under the mutation in that run. Fixed to match the check name; the rerun exits 1 as required. That first MUTATE output was overwritten and is not kept; the FIRSTRUN of the real script is kept (b3_u1_chain_FIRSTRUN.out, path in the traceback redacted).
(ii) CK7 was run after Amendment 2 with the threshold written there (10%): Z2 jump 0.414 against 0.44 (-5.9%), Z3 jump 0.538 against 0.56 (-4.0%): PASS. Single seed per chain, one lattice size; the caveat of Amendment 2 (metastable-branch averages) applies.
(iii) The CK3 reconstruction of the improved Delta gamma values reproduced all eight within 1% (declared tolerance 3%); the link L5d is therefore reported DERIVED-ARITH, with the caveat that the <cos^p theta> average is replaced by the power of the mean.
