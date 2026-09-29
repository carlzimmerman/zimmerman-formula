# Z1 -- is there ANY scale at which the three SM gauge couplings come together? (pre-registration)

Written 2026-09-29 BEFORE `z1_common_scale.py` was run. Motivation: the user's rule allows only kappa = 1/2 and Z as free constants, so a zero-knob boundary rule of the form 'the couplings are equal (in a stated normalisation) at the scale X'
has only X to fix, and X must come from kappa, Z, pi, integers. Lane Y1 (commit f73411efe) gives the Standard Model couplings with validated 4-loop running and 1-sigma errors of 0.23% (a_Y), 0.021% (a_2), 0.12% (a_3) at M_P.
If NO scale exists at which the three couplings agree (in any group-theory normalisation) within the error, then NO choice of X can rescue an equal-couplings rule, and the scale question becomes irrelevant.

## Method (declared)
* Use lane Y1's validated central trajectory (y1_lib.run_central, mu_max = 1e21 GeV); a_i = 1/alpha_i with a_Y the hypercharge coupling in the standard normalisation and a_1 = (3/5) a_Y the GUT-normalised one.
* For each mu on a grid of 4000 log-spaced points from 1.1 m_t to 1e21 GeV compute, in the two normalisations N = Y (a_Y, a_2, a_3) and N = GUT (a_1, a_2, a_3), the relative spread S_N(mu) = (max - min)/mean of the three values.
* Report min over mu of S_N, the scale where it occurs, and that minimum in units of the combined 1-sigma uncertainty of the spread (Y1's per-coupling errors at that scale, combined in quadrature).
* Also report, for each of the three pairs, the crossing scale (if any) and the miss of the third coupling there, in % and in sigma.
* Positive control: a one-loop supersymmetric-style continuation (MSSM b = (33/5, 1, -3), starting at 1 TeV from the SM central values) must find a minimum spread below 3% at a scale between 1e15 and 1e17 GeV.

## Criteria (declared)
* C1 (no common scale): min over mu of S_GUT exceeds 5% and min of S_Y exceeds 3%, each by more than 10 combined sigma. Expected: TRUE (the known ~11% miss of a_3 at the a_1 = a_2 crossing for GUT; ~5% at M_P for Y).
* C2 (positive control): the supersymmetric-style run finds a minimum spread below 3% at 1e15-1e17 GeV. Expected: TRUE.
* C3 (corollary): therefore no zero-knob 'couplings equal at a scale X built from kappa, Z, pi, integers' rule with a Standard-Model desert can pass, for ANY X. This is a statement about the desert; adding charged matter changes the running (lanes U3, X1).
* MUTATE control: the positive control is run with the SM coefficients instead of the MSSM ones; C2 must FAIL (and only C2): exit 1; exit 3 if broken.

## Reading rules
alpha stays an INPUT; kappa = 1/2 FITTED; nothing here derives anything. It closes one door (equal couplings at a scale, SM desert) for every possible X.

## Amendment 1 (2026-09-29, after the run; disclosed, no criterion changed)

The prose expectation in the pre-registration ('the known ~11% miss of a_3 ... ~5% at M_P') described a different quantity (the third coupling's miss at a pairwise crossing) from the one the criteria test (the minimum relative spread (max - min)/mean over all scales). The measured minima are 8.37% (Y normalisation, at 3.4e19 GeV) and 7.62% (GUT normalisation, at 1.7e14 GeV), i.e. 31 and 30 combined sigma; the declared thresholds (5% and 3%, each by more than 10 sigma) pass. The first control run used a label comparison that reported 'broken' for the wrong reason; fixed to compare the check ID.
