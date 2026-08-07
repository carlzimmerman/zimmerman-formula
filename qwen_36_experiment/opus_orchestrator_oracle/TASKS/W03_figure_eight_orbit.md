# W03 — The figure-eight three-body orbit
COST: M | script: `wacky_figure_eight_orbit.py`

> WACKY TASK. No framework rules apply. Two things still do: **every check must be able to fail**, and
> **refine once and report the shift**. `../03_NUMERIC_HAZARDS.md` applies to any float arithmetic.
> Put the script in `real_research/reviews/` like any other, prefixed `wacky_`.

## The idea
Chenciner and Montgomery (2000) proved a remarkable three-body solution exists: three equal masses chase
each other around a **single figure-eight curve**, all with the same period. It is stable. Integrate it.

## Do
1. Use the standard initial conditions (equal masses, G = 1). The canonical values are
   x₁ = −x₃ ≈ 0.97000436, y₁ = −y₃ ≈ −0.24308753, x₂ = y₂ = 0, with v₂ ≈ (−0.93240737, −0.86473146) and
   v₁ = v₃ = −v₂/2. Verify total momentum and angular momentum are zero to machine precision *first*.
2. Integrate with a symplectic integrator (leapfrog or Yoshida 4th order) for 10 periods. Plot the orbit.
3. **The real check: energy conservation.** Report the relative drift over 10 periods, then repeat at 4×
   smaller timestep and confirm it drops by the expected power of your integrator's order. A non-symplectic
   integrator will secularly drift — demonstrate that too, as the control.
4. Then test stability: perturb the initial conditions by 1e-6 and 1e-3, and measure how long the figure
   eight survives. Report the Lyapunov-like divergence rate.

## Why
You asked whether the three-body problem is solved. It is not in general — but this is one of the handful of
exact periodic solutions known, and watching it hold together is worth the hour.
