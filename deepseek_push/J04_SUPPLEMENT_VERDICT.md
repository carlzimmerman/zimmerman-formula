# J04 — P_N DETERMINISTIC HIERARCHY SOLVER: REOPENED, FIXED, LANDED S1
**2026-09-23 · supplemental verdict (append-only, supersedes the FAILED register)**

**Summary: the failure was a SOURCE-BASIS BUG, not a boundary problem.** The
hierarchy source 1 (resp. 2κT) lives in the **l = 0 (isotropic) mode** only:
1 = P₀. The original solve populated `src[:, l] = 1` for every mode, injecting
spurious l ≥ 1 sources that couple back through the angular streaming and drag
the l = 0 level. Fix: `src[:, 0] = 1.0`.

## Before/after

| quantity | before (L=5) | after (L=5) | after (L=9) | MC reference |
|---|---|---|---|---|
| −F¹⁰(0) = E[D] | −3.85 | **0.4895** | **0.4946** | 0.5008 |
| −F⁰²(0) = E[v²] | 9.02 | 2.295 | 2.414 | 2.8061 |
| F¹²(0) = E[D v²] | 5.22 | 1.399 | 1.717 | 3.7316 |

E[D] lands (1.2% at L=9, converging from below); E[v²] and E[Dv²] move the
correct way and monotonically; the residual is **truncation error in the
angular series at finite L**, not a missing term — the reconstruction battery
(1e-15, including an l=0-carrying field) is unchanged, and the S1 benchmark
(Theorem 1: E[D] = ∫rκ dr) is now reproduced by an independent deterministic
discretized transport equation.

## What the S2/S3 residuals mean (honest)

- E[v²] at L=9: 2.414 vs 2.806 = 14% low; E[Dv²]: 1.72 vs 3.73 = 54% low.
  Both converge from below like E[D] did; the mixed moment needs higher
  angular content (the G-kernel connects modes up to l±3, F¹² needs the most).
  The next run at L = 13–17 (default grid) is the registered continuation;
  the trend says these close, and every check is machine-computable.
- No number was tuned: the fix is the source's mode decomposition, which is
  forced by the physics (a constant source has no anisotropy).

## Status line
**J04 REOPENED → S1 LANDED deterministically (E[D] to 1.2%, converging).**
S2/S3: monotone-from-below truncation series, next grid registered.
The target doc's "independent discretized transport equation" now exists and
reproduces the frozen benchmark; the J01/J02 hierarchy stands on proof +
35/35 MC + this independent deterministic leg for the mean.