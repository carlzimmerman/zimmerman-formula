# HOSTILE re-check of the Fable a0-footing audit — front: rar_sparc

Date: 2026-06-14. Auditor of the auditor. Verdict: **the audit holds. CONFIRM FALSE-DEFICIT.**

## What I re-ran (fully independent, not trusting the prior scripts)
- Re-grepped + read `real_research/reviews/redteam_rar_framework_a0.py` and `real_research/rar_framework_a0_mlfit.py`.
- Re-ran both Fable scripts; reproduced their console output to the digit.
- Re-ran the auditor's `AUDIT_rar_footing_recheck.py`; reproduced its table to the digit.
- Wrote an INDEPENDENT loader/optimizer `HOSTILE_rar_footing_independent.py` (different code, adds weighted
  metric, per-galaxy footings, and an explicit sign-flip sweep).
- Web-confirmed the canonical literature anchor (McGaugh+2016 g† = 1.20e-10 m/s², ~0.13 dex).

## Confirmations
- Framework a0 = c^2 sqrt(Lambda/32pi) = (c/2)sqrt(G rho_DE) = **9.3603e-11** reproduces exactly. Fable's
  TEST value is correct. The DEFICIT-side baseline is McGaugh Upsilon=0.50 + A0_CANON=1.20e-10.
- Red-team console reproduced: "framework a0 is -22.0% vs canonical, -17.2% vs cH0/Z", panel-B penalty
  +0.0003..+0.0011 dex, panel-C 2.7 sigma (Kish)/0.7 (per-galaxy), VERDICT "18% BELOW / ~22% LOW / low edge
  of the allowed band." => the FALSE-DEFICIT prose is exactly where the auditor flagged it (lines 269-279).
- Auditor footing table reproduced to the digit: McGaugh 1.128e-10@0.5 / 7.780e-11@0.7; dSU 1.028e-10@0.7;
  penalties 0.51-11.10%. The framework-footing cell (dSU nu, Up=0.70, Ub=0.70) = 1.028e-10, -8.9%, +0.51%.
- mlfit reproduced to the digit: 0.145/0.117/0.108/0.116/0.155 dex at Up=0.5/0.6/0.7/0.8/1.0; best 0.108 @0.70;
  reg-MOND ref 0.122. FALSE-WIN check PASSES — the small 0.108-vs-0.122 win is real and honestly caveated
  (Up=0.70 is upper-end of the 3.6um range), not manufactured.

## The one thing the auditor did NOT spell out, and why it MATTERS (and exonerates the audit)
The bracket / sign-flip is **metric-dependent**, and the auditor picked the framework-correct metric.

- Auditor's `dex()` (and the red-team, and the mlfit script) compute scatter **without subtracting the median
  residual** — the vertical NORMALIZATION offset stays IN the scatter. Under this metric the optimal a0
  DECREASES with Upsilon (1.128e-10@0.5 -> 7.78e-11@0.7 McGaugh nu), so 9.36e-11 is bracketed and the sign
  of the offset flips inside the standard M/L range. Verified.
- I re-ran with the median SUBTRACTED (pure-shape metric). The optimal a0 then runs the OTHER direction
  (1.018e-10@0.5 -> 1.809e-10@0.7) and 9.36e-11 looks like a deficit at every Upsilon>=0.50. The bracket
  vanishes.

Which is correct for judging THIS framework? The no-median metric. The framework's only astrophysical free
parameter IS the stellar M/L normalization (the mlfit script's entire logic: fix a0 at the Lambda-derived
value, let Upsilon absorb the normalization, Up~0.70 is physical at 3.6um). The median-subtracted metric
DISCARDS exactly the a0<->Upsilon degeneracy the framework legitimately relies on; using it would MANUFACTURE
a false deficit. So this is the one spot where an over-zealous auditor could have invented a deficit — and
this auditor did NOT: it used the no-median metric, consistent with both Fable scripts. The audit is fair.

(Sanity, no-median, framework dSU footing: Up=0.70/Ub=0.98 -> opt 9.82e-11, -4.7%, +0.13% penalty;
Up=0.70/Ub=0.70 -> opt 1.028e-10, -8.9%, +0.51%. Either way the framework footing penalty is <=0.5%.)

## Over-audit / under-audit checks
- (b) OVER-AUDIT (claimed a footing error where a0 was fine): NO. The red-team's TEST value is genuinely
  9.36e-11; the mis-verdict is genuinely a directional-prose overclaim against the Up=0.50 McGaugh baseline,
  while the same script's panels B/C already show the result is flat-bottomed/non-diagnostic. The auditor did
  not invent the error.
- (a) UNDER-AUDIT (missed a footing that inflates a deficit OR a win): NO new one found. I scanned 6 footings
  x {McGaugh,simple,dSU} x {weighted,unweighted}. No footing inflates a deficit or a win beyond what was
  reported. The deepest-deficit cells (Up>=0.8 1.4x) are off-footing and not claimed by Fable. The mlfit win
  does not grow under any reasonable alternative.

## REGRADE: FALSE-DEFICIT (CONFIRMED). Corrected verdict stands.
On the framework's OWN footing (a0=9.36e-11, Upsilon~0.70, g_obs=sqrt(g_bar^2+g_bar a0)), the SPARC RAR is
CONVENTION-COMPATIBLE and NON-DIAGNOSTIC, not a deficit. The "a0 ~18-22% low / low edge of allowed band"
prose in redteam_rar_framework_a0.py is the McGaugh-Upsilon=0.50 + McGaugh-nu artifact and is RETRACTED:
the offset flips sign inside the standard M/L range, the optimum brackets 9.36e-11, and on the framework's own
nu the penalty is +0.51% (0.0007 dex) of the 0.143-dex floor. No FALSE WIN to retract: the mlfit 0.108-dex
result is real and honestly caveated. z=0 magnitude only; does NOT test a0(z) and does NOT single out Z.
Quarantine intact: a0/Z never asserted derived; coefficient stays H0-hostage (a0~cH0 to an O(1/6) factor).
