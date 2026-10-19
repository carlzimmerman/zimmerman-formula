# Lane AS3 -- AS2 with its one failed gate re-anchored on CPR's internally consistent data (pre-registration)

Written 2026-10-19 BEFORE any AS3 script existed. No SM fixed point, no f_g at a fixed point and no alpha^-1(0) (P) has been computed in the
Codello-Percacci-Rahmede (CPR) scheme by any lane: AS2 stopped at a gate before its trial. So this pre-registration is still blind to the trial.
Amend only by appending an "Amendment" section at the bottom.

## What AS3 is

AS3 is lane AS2 (`../AS2_fg_cpr_scheme/AS2_PREREGISTRATION.md`, commit c1789e555, plus its Amendment 1, commit 8ce28c967, written before any
AS2 run) with exactly ONE change: gate G-CPR-EH (ii). Every other section of AS2 applies unchanged and is incorporated by reference: the scheme
(every choice cited to CPR arXiv:0805.2909), the type-I matter rule, the flat-background f_g definition in the same gauge and eta convention and
its stop rule, gates G-MAT, HK-CPR, G-CPR-EH (i), G-CPR-R2 (i) and (ii), G0, the trials (THE graded trial = R^2 with SM matter N_S = 4,
N_D = 45/2, N_V = 12; EH with SM matter = reported reference), the fixed-point selection rule, the classes, the reported-not-graded systematics,
the MUTATE controls, and the statement of what each outcome means. kappa and Z enter nowhere; even AGREES is not a derivation of alpha
(alpha_2, the hadronic offset and the masses are measured; convergence is untested).

## Why the gate changes (disclosed: this change is made AFTER seeing the AS2 gate output)

AS2 (run commit 7df554f35; re-run independently on 2026-10-19 with identical output) failed G-CPR-EH (ii): its pure-gravity n = 1 root is
Lambda~ = 0.12927, G~ = 0.98417 against CPR Table 1's 0.1297, 0.9878 (-0.33 percent, -0.37 percent; tolerance 0.1 percent). The AS2 diagnostic
`as2_diag_cpr_n1.py` shows that CPR's printed n = 1 row is inconsistent with CPR's own other published numbers:
* the derived root has g~0 = 0.0052261 (CPR Table 1: 0.005226) and critical exponents 2.3824 +- 2.1682 i (CPR Table 2: 2.382 +- 2.168 i);
* at CPR's printed point (g~0, g~1) = (0.005226, -0.02014) the beta functions of the flow that reproduces CPR's closed form exactly are NOT zero
  (1.0e-4, -2.9e-4), and the exponents there (2.380 +- 2.187 i) disagree with CPR's Table 2;
* the printed row is consistent with g~1 = -0.020214 having been printed as -0.02014 (betas 5e-7 there).
The same pipeline reproduces CPR's closed form exactly at R^0, R^1, R^2 and the independent n = 2 row (Table 1) to 1 percent with Table 2's
exponents. The re-anchored gate below uses only CPR numbers that are mutually consistent. Because it was written after seeing AS2's gate output,
this is a post-hoc gate design; it concerns the validation of the pipeline against a published computation, not the alpha trial, and no trial
number exists. It is recorded here as such.

## The one changed gate

**G-CPR-EH (ii), re-anchored.** For pure gravity (n = 1), some real root of the derived flow must reproduce, to 0.1 percent each:
* CPR Table 1, n = 1: g~0* = 0.005226;
* CPR Table 2, n = 1: Re theta = 2.382 and |Im theta| = 2.168.
CPR Table 1's n = 1 entries g~1*, Lambda~*, G~* are NOT gated (shown inconsistent above); the derived values are reported next to the printed ones.
MUTATE_1 and MUTATE_2 of AS2 must still make this gate (and the others they target) FAIL.

## Execution

Reuse the AS2 code by import or by copying it into this directory with only the gate changed (diff to be shown in the report). Same compute
rules as AS2 (one core, nice 19, < 2 GB RSS, one process at a time beside any live 1024^3 run). Commit locally; do not push.

## Amendment 1 (appended after the runs; nothing above was edited)

* **Outcome.** Every gate passes:
  * G-MAT, HK-CPR, G-CPR-EH (i), G-CPR-R2 (i) and (ii), and G0;
  * G-CPR-EH (ii) re-anchored: g~0* = 0.0052261, theta = 2.3824 +- 2.1682 i;
  * the classifier controls.

  MUTATE_1, MUTATE_2 and MUTATE_3 break their targeted checks.  The f_g stop rule was not triggered: the beta-limit is finite, the
  +-infinity limits agree, parity holds, and f_g is xi-independent.
* **EH reference:** unique admissible root (g, lambda) = (0.967159, -1.22293), f_g = 0.03883093, P_EH = 95.57847.
* **Graded R^2 trial:** two admissible roots, (1.006220, -1.264456, -0.0037661) and (0.988607, -1.297727, 0.0055494), so the verdict is
  **NOT DIAGNOSTIC**.  Reported, not graded, P at those roots: 95.26961 and 95.70584.
* **as3_trial.py ran once** (no fix, no re-run): 1120 s, peak RSS 1.35 GB.
* **as3_roots_report.py was added after that run**, to report f_g and P at every admissible root, as the frozen rule "all are reported"
  requires.  It also re-derives f_g by an exact second route (restriction to the kernel of the gauge fixing), which agrees identically.
  No class changes.
* **Caveat carried from AS1:** in CPR's gauge f_g reduces to the TT-mode contribution, because the conformal mode decouples from the
  conformally invariant Maxwell term.  Eichhorn-Versteegen's printed TT-approximation formula is not reproduced by this TT computation
  (the reason has not been identified), although the same machinery reproduces their full alpha = 0, beta = 1 f_g exactly.
