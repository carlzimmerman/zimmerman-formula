# TASKS_SEEDED — seed-promoted task specs (PROMOTE-duty output)

Each spec is keyed by a bold id and read by the SEEDED-TASK duty via `grep -A 14
"<id>"` — keep every spec within 14 lines of its own header line. Sources per spec:
the matching seeds/refereed + seeds/interp of the same number.

**S0006 — a0* co-location (golden sub-peak ↔ n_s shortlist).** REF passed.
Falsifiable H: one dimensionless a0* is (1) the golden-ratio sub-peak of the a0-bump
cluster response R(a0), a0* = a0_peak/phi (phi=1.61803), AND (2) the broken quantum
behind n_s=0.9649 via shortlist {1-a0*, 1-a0*/phi, a0*/phi, a0*+1-a0*/phi}; a0-line
g^2-gb^2=a0*gb with sin^2theta_W=gb^2/(g^2+gb^2) → 0.2312 @3sigma. Wildcard = a0*.
METHOD: A) a0*_A from bullet1 golden sub-peak → predict sin^2; B) a0*_B from bullet2
fitting n_s to shortlist; C) co-locate. FDR pre-reg: 4-way fit, NO catalog search (no
mm_search.py) — fix the 4 members + 1/phi + sin^2 convention a priori BEFORE reading
R(a0); no re-fit. PASS iff K1&K2&K3 absent AND a0*_A==a0*_B in framework tol.
KILL: K1 |sin^2(a0*_A)-0.2312|>3σ (bullet1); K2 no shortlist member →0.9649 in tol
(bullet2); K3 a0*_A≠a0*_B >tol (shared-number). One→REFUTED (success), two→DISCARD.
CAVEATS: CONVENTION-grade ≠ hit; 3σ+tolerance convention-dependent — expect K1/K3 to
fire = valid REFUTE. kappa=1/2 NOT used (fitted 0.551±0.043). All dimless → dual-
footing N/A. R(a0) data absent → BLOCKED, name the file needed.

**S0007 — Q/Y sector split S_QY footing-invariance ↔ m_W/m_Z.** REF passed.
Falsifiable H: the framework's footing-invariant Q/Y sector split S_QY (the "one field, two
jobs" ratio of two sector charges) equals m_W/m_Z = cos theta_W = 0.8814. (a) Compute S_QY
from the framework charge bookkeeping on footing A = 9.3619e-11 and footing B = 1.1279e-10.
(b) Require |S_QY - 0.8814| < 0.005 on BOTH footings AND |S_QY(A) - S_QY(B)| < 0.001
(footing-invariance).
METHOD: derive the two sector charges INDEPENDENTLY of target 0.8814 (no 0.8814 in any
input), then form S_QY = Q_sector/Y_sector a posteriori; report S_QY(A), S_QY(B). FDR
pre-reg: fix WHICH two charges + the ratio convention a priori BEFORE comparing to 0.8814
(anti-retrodiction guard #3); NO catalog search (no mm_search.py) — the split is one
named bookkeeping ratio, so the only freedom (charge selection) is pre-fixed.
KILL: K1 |S_QY - 0.8814| > 0.005 either footing; K2 footing-variant |S_QY(A)-S_QY(B)|
> 0.001; K3 retrodiction (0.8814 fed in). One → REFUTED (success), two → DISCARD.
CAVEAT: dimensionless ratio → both footings apply, BOTH reported (dual-footing rule).
kappa=1/2 NOT used (fitted 0.551±0.043).
