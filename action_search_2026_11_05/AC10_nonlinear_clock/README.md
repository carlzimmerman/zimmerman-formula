# AC10: AC2q nonlinear planar evolution: NO VERDICT (frozen). The first fold is v3s's to 0.3 %; nothing AC2q-specific regularizes it

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (552db86f89), committed alone
before any code. Two amendments were declared after the first results (A1-POST, A2-POST, below). They change check
code and edge handling only. The frozen verdict is reported as the verdict.

Scripts:
- `s1_reduction.py`: symbolic planar reduction.
- `ac10.py`: Lagrangian labels, DOP853, ladder N = 2000/4000/8000, checkpointed per row in `parts/`.
- `grade.py`: frozen lines plus the amendments; output in `grade.out` and `GRADE.json`.

## The question

CLOSURE.md said AC2q "inherits X14's caustics generic" by inference. AC10 tests that directly. It evolves AC2q's PN
system nonlinearly in planar symmetry: a cold khronon stream crossing a baryon sheet, X14 F2's setup. Each row is run
next to its v3s twin.

## What holds

- **S1, the reduction (sympy, exact): PASS.** In 1D, AC7's Lagrangian is v3s's label system with three changes:
  - the transported charge is Pi = D.P + s^2;
  - P sees only the excess Pi - s^2;
  - Poisson sees Pi.
  All corrections are s^2 O(eps) or O(gamma s^2). The Euler identity D_t v = Xi_x - phi_x is exact. In 1D the
  canonical clock gives no pressure on galactic scales. Its only scale is a Helmholtz screening length
  1/sqrt(K M s^2), which is Hubble-sized.
- **New analytic prediction (A2).** For a clock-only stream (no phantom), J'' = Omega^2 (1 - J) after the sheet
  kick, with Omega^2 = K s^2 (M - 1). So J = 1 - (K Sigma/(w Omega)) sin(Omega tau), and the stream folds iff
  Omega tau_f <= 1. v3s's charged threshold is 1/sqrt 2 (X14 F2).
  - At X14's fold locations Omega tau_f ~ 1e-2.
  - The physical clock charge therefore cannot stop the fold.
- **K1: PASS.** The coupled code equals an independent two-label integration: 1.282826355 both ways. The thin-sheet
  delay after crossing is 0.9994 v_cross/(K Sigma_b).
- **First fold, physical rows** (A2-POST reading: first fold over all cells, before any multistream state).
  - **Rows run:** a declared information subset of 12 AC2q rows plus their v3s twins out of the 240 frozen rows. Radii
    11 and 156 kpc; w = 68.75 km/s; low end of the M - 1 bracket; Lstar 21.7/22.9 pc; phantom, clock-only and
    soft streams; both footings.
  - **Folds:** every row folds.
  - **AC2q vs v3s:** AC2q's fold time is 1.0752-1.0782 tau_f against v3s's 1.0718-1.0773. The largest difference is
    1.9e-3 (canonical) / 3e-3 (alt).
  - **Convergence:** ladder change <= 2e-4, except two soft AC2q rows at 11 kpc, which are NOT CONVERGED.
  - So the stiffness switched on the charge, and the clock's s^2, do not change when or whether the stream folds.
- **X > 0 is not what fails.** Up to the fold, min X/X_bg = 0.99999985 (v stays at a few times w, far below c).
  At a fold v' diverges while v stays finite.
- **Controls bite.** MUTATE-A, a repulsive sheet: REGULAR (J_min 1.0). MUTATE-B, Mach 0.3 with the stiffness raised
  by hand: REGULAR (J_min 0.91). So the method can see pressure regularization when it is real.

## Why the frozen verdict is NO VERDICT

- **K2 and K3 fail as frozen.** The A1/A2 stress predictions were frozen with crossing speed w = 1. But the slab's
  own charge pushes its front, so the real crossing speed is 1.09-1.23. Late turnaround / phase-mixing folds (X14 F3)
  also occur before t_max on rows predicted not to fold.
  - Re-read with each cell's own crossing speed (A1-POST), A1 holds on both v3s rows: omega tau_f = 0.75 and 0.95
    (> 1/sqrt 2), with no first-passage fold.
  - A2 holds at 1.20 (> 1), with no first-passage fold.
  - On those three rows the numerics equal the exact F1d per-label equation to 8e-4 or better.
  - The marginal A2 row (Omega tau_f = 0.98) reaches J 0.009 rather than a fold. Edge streams cross into it, and F1d
    is no longer local there, so A1-POST does not pass either.
- **The interior reading is post-fold.** The front 5 % of cells (excluded by the frozen rule) fold first. Where the
  stiffness is on, the inviscid code then sends pressure spikes from those J -> 0 cells into the interior, which
  stalls at J about 0.18-0.19. That happens in **both** AC2q and v3s (v3s phantom rows read REGULAR too). It is the
  shock that X14 F5 predicts for a genuinely nonlinear pressure, outside the frozen scope ("no post-fold
  continuation"). It is not an AC2q regularization.
- **Rows:** only 12 of 240 AC2q rows were run. Each pressure-on ladder takes about 10 minutes on a shared machine.
- **Edge charge jumps.** A stiffness acting on a charge jump at the stream ends is a grid-scale force. A2-POST tapers
  the excess charge to the background inside the excluded edge cells only.

## What this settles and what it does not

**Settled at this level.** AC2q's planar PN dynamics are v3s's with the charge shifted by s^2. The first caustic forms
at the same time to 0.3 %. The clock's own pressure is Hubble-scale and cannot remove it. The CLOSURE inference is
supported, but no frozen label is earned.

**Not done:**
- a shock-capturing (viscous or Godunov) post-fold evolution;
- the full 240-row grid;
- 3D or spherical cases;
- the nonlinear hold law (constant M per row here);
- the moving Sun (AC11).

X14's conclusion stands for AC2q too: only a new constant (the beta class) could remove the fold.
