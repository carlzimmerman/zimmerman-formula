# Lane M -- red-team review of the negative alpha results (pre-registration)

Written 2026-09-28 BEFORE any script in this directory was written or run.
Amendments are appended at the bottom, never edited in place.

## Disclosure of what was done before this file
I READ the pre-registrations, scripts' printed outputs and the AH1-AH6 files of every lane that has results (A-G, AH1-AH6) and the I0 and J
pre-registrations (no I or J results exist yet; they are out of scope). While reading I noticed BY EYE, and therefore before pre-registering,
one suspected defect: lane A's a3 script sets `bY = 3/5 * 41/10` (line 77) although the hypercharge coefficient in the alpha_Y normalisation is
5/3 * 41/10 = 41/6 (lane B and lane C use 41/6). This is tested below (M1), not assumed. I also noticed that lane E reports its bound
`zeta_max = 6.5e-8` as NOT reproducing the repo's `zeta < 4e-9`. I have not run anything.

## What is attacked
Every negative verdict of lanes A, B, C, D, E, F, G and AH1-AH6 (AH5, AH3 included). Lanes H, I, J, K are NOT attacked or duplicated.

## Criteria (declared now)
* An objection STANDS only if I can show, by a committed script (exit 0, MUTATE control exits 1) or by a cited primary source that I actually
  read, that the lane closed a branch by an assumption, convention, truncation or fixed variable that is unjustified AND that changing it
  (a) changes a number the lane's verdict used by more than the lane's own stated tolerance, or (b) re-opens a branch that would pass
  lane D's bar (P < 1e-3, miss <= 5e-10, zero fitted reals, scale stated).
* FAILS if the flip does not change the verdict-relevant number, or the lane already declared the point in its scope-out.
* UNTESTABLE if it needs an input that is walled (SM masses), unread full text, or a new calculation beyond this lane's budget.
* "Conclusion stronger than evidence" = a sentence in a lane file or commit message whose claim exceeds what the committed scripts show.
* A defect that produces a spurious POSITIVE hint counts as a finding as much as one that closes a branch.

## Everything that will be run (fixed list; count = 5 scripts + 3 source checks; nothing else is scored)
* m1_lane_a_running_check.py -- recompute lane A's I5 with b_Y = 41/6 derived from field content (exact Fractions), cross-check against
  lane B's and lane F's numbers, recompute the required BH size k and the 'Z within 0.6%' post-hoc remark; report whether it survives.
  Prediction (stated now): 1/alpha_em(m_P) = 104.9 not 132.4; the 0.6% remark does not survive (Z/k_req ~ 1.13). MUTATE: b_Y = 3/5*41/10
  must reproduce lane A's 132.4 and thereby FAIL the 'agrees with lane B to 1%' check.
* m2_lane_b_sign_and_precision.py -- (i) the SU(2) sign restriction f >= 0 of B's E4: with ONE universal gravity coefficient f, list which of
  U(1)_Y, SU(2), SU(3) have an interacting fixed point for each sign; (ii) the precision needed of f_g for 1e-3 in alpha_em and the
  implied spread across the published truncation and the f_g = 0 case. Prediction: universal sign gives a fixed point for U(1) only (f>0) or
  for the non-abelian groups only (f<0), never both, so the sign restriction is harmless; B's verdict stands. MUTATE: flip b_Y sign.
* m3_ds_gauge_coupling.py -- what dimensionless coupling does the MacDowell-Mansouri SO(4,1) structure carry? Match the EH and cosmological
  terms of c * eps F F with F = R - (Lambda/3) e e to fix c, then read the gauge coupling; compare with alpha. Prediction: 1/g^2 ~ 1/(G Lambda),
  g^2/(4 pi) = O(1) * x ~ 1e-121, so the dS gauge structure cannot supply alpha and the objection that 'the programme's own structure could
  fix the traded parameter' FAILS for the dS gauge structure. MUTATE: wrong EH coefficient must fail the cosmological-term consistency check.
* m4_lane_c_content_and_cutoff.py -- (i) C2c toy versus the proper SM chain: what 1/alpha_em(Lambda) is left at Lambda = M_red/sqrt(N) when W,
  Higgs are included (should be ~106, not 0); (ii) self-consistent species cutoff: extra charged content n_x needed for hypercharge emergence
  when Lambda = M_red/sqrt(N_SM + 4 n_x) and the extra states sit at 1 TeV (declared, one value, not scanned). Prediction: the required content is
  ~ 2.5x the SM Weyl hypercharge sum, no integer/forced value; self-consistency shifts the requirement by < 5%. MUTATE: drop the N-dependence
  of Lambda must NOT change verdict but must fail the 'self-consistent' identity check.
* m5_lane_d_independent_count.py -- independent re-implementation (numpy, written from D's declared grammar, not from D's code) of the distinct
  value counts and hit counts of E1(12) and E2(6) around 137.035999177; compare with D's printed numbers (E1(12): 38,948 distinct, 1 hit at 1e-3;
  E2(6): 8,820,869 distinct, 289 at 1e-3, 1 at 1e-5). Pass if agreement within 2% on counts and the hit counts. MUTATE: remove the sqrt operation
  must change the counts (control must fail the 'matches D' check).
* Source checks (WebFetch, reported not scored): (S1) arXiv:2508.03563 abstract/intro: is f_g regulator/gauge dependent and can it vanish;
  (S2) Salam-Sezgin 6D gauged supergravity: does the football vacuum leave a flat modulus that controls 4D gauge couplings (lane F's
  'SUSY could fix chat' scope-out); (S3) if S1/S2 unreachable, they are reported as UNTESTABLE, not guessed.

## Deliverables
(1) table lane -> strongest objection -> tested? -> verdict; (2) top five under-tested branches ranked by plausibility with one pre-registerable
test each; (3) explicit list of conclusions stronger than evidence.

## Scope / not done
No new derivation attempt of alpha. SM masses walled; kappa = 1/2 fitted; no dark-matter particle; nothing written outside this directory.
The honest expected outcome (stated in advance): the negative results are essentially sound; found defects are one bug (lane A I5) and wording
over-statements, not a re-opened branch.

## Amendment 1 (2026-09-28, after running m3)
The threshold I wrote in m3's last check ("alpha_MM < 1e-118 alpha for kN in [0.01, 100]") was mis-set by me: the closed form gives alpha_MM/alpha up to 2.1e-117 at kN = 0.01.
The physics statement is unchanged (the structure supplies ~ (16/3) x / kN ~ 1e-121 +- 2 decades, i.e. >= 116 orders below alpha); threshold changed to 1e-115 and disclosed here.
The MUTATE control fails the cosmological-term match as required.

## Amendment 2 (2026-09-28, results vs the predictions stated above; nothing above edited)
* M1: prediction confirmed. Lane A a3 line 77 has b_Y = 3/5*41/10 = 2.46 instead of 41/6 = 6.83; correct 1/alpha_em(m_P) = 104.94 (lane B 104.92, lane F 104.94), not 132.39; required k = 5.12, Z/k = 1.130 (13 %), so the 'within 0.6 % of Z' remark is void. MUTATE reproduces 132.39 and fails.
* M2: prediction confirmed (a universal f gives an interacting fixed point for U(1)_Y only with f>0 and for SU(2), SU(3) only with f<0); f_g needs 0.18 % precision for 1e-3.
* M3: prediction confirmed (alpha_MM ~ (16/3) x / kN ~ 1e-121). Threshold slip disclosed in Amendment 1.
* M4: partly different from the prediction: the EXTRA content needed for hypercharge emergence is 1.7x the SM fermion Weyl hypercharge sum (8.6 unit-Y Dirac fermions at 1 TeV), i.e. ~2.7x the total, consistent with lane C's 2.55; self-consistency shifts it by 0.6 % (< 5 % predicted). The proper SM chain leaves 1/alpha_em(Lambda) = 107 (not 0).
* M5: prediction confirmed; my independent enumerator reproduces D's E1(12) (38,948; 19; 1) exactly and E2(6) (8,820,273 vs 8,820,869; 3047; 289; 1) to 7e-5.
* Sources: S1 (2508.03563 abstract) confirms regulator/gauge dependence, does NOT itself state that f_g can vanish (lane B's reading of the introduction is unverified by me); S2 (web search summary of hep-th/0212091 etc.) confirms the Salam-Sezgin football keeps a flat direction S 'to all orders in perturbation theory'; the dependence of 4D gauge couplings on S is recalled, not read.
* All 19 scripts of lanes A-G plus D1-D3, AH1, AH5, AH6 were re-run from a scratch copy: real runs exit 0; every MUTATE run exits 1 (lane C's via --mutate). AH2, AH4 (long mode sums) were not re-run.
