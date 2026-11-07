# QX17C: convergent solver for the static spherical v3s equations (2026-11-06)

**Label: CERTIFIED (solver).** Criteria 77dc5bfff9; script `qx17c.py`; outputs `qx17c.*` and `qx17c_MUTATE.*`.
Adopts nothing. kappa = 1/2 FITTED. Not theory closed.

QX17B S-sph **stays FAIL as frozen** (c3cebe6cd6). This lane solves the same problem with a different method and grades
the same gates. They now pass, converged, on both footings.

## Why QX17B's solver failed

The equation's restoring length is Lstar, so its fast modes grow like exp(+-k s), with s = r/Lstar and k ~ 1. solve_bvp
in x = ln s judges its error by the ODE residual, which these fast modes multiply by roughly k s. Across s up to 3e9 (the
KNOWN case) it keeps refining the mesh until it runs out of nodes.

## Method

- **Unknown:** Y(s), from the exact centre (Y(0) = 0) to s_out.
- **Discretisation:** conservative vector-Laplacian finite differences. The discrete mass telescopes, so weak-mode
  G = gN + Y exactly.
- **Solve:** damped Newton on a tridiagonal system. Full GR mode uses defect correction, with B, m and TOV p_m from
  quadrature.
- **Outer boundary:** the decaying k_1 Bessel mode about law S.
- **Convergence:** every solve converges in 1-6 Newton steps to a scaled residual of 1e-13 to 5e-12.
- **Run time:** 5 s for everything, against hours for solve_bvp.

**Residual scale, defined after the freeze.** The criteria said "scaled residual <= 1e-9" without defining the scale. The
first scale (|lhs| + |rhs|) sat on a round-off floor (~1e-6), for two reasons:
- near the centre, the row is a difference of two flux terms of order 1e10;
- at the outer row, Y - Y_S had dropped below Y's own round-off.

The scale used is the sum of absolute values of every term entering the row (the standard round-off-aware norm). This
changes only the Newton stopping test. No gate number depends on it, and each gate number is also checked by C2/C3.

## Gates (both footings, not pooled)

| gate | tol | canonical | grid x2 change | s_out x10 change | alt | verdict |
|---|---|---|---|---|---|---|
| G1 KNOWN (Lstar = 1e-3 pc gives law S, 1-30 kpc) | 1e-3 | 3.8e-7 | 3.1e-7 | 6.7e-9 | 3.9e-7 | PASS both |
| G2 Sun y/g*, 10 AU to 1e-3 Lstar | 1e-2 | 7.1e-6 | 5.3e-6 | 5e-11 | 7.1e-6 | PASS both |
| G3 Sun full vs weak, 2 R_sun to 1e3 Lstar | 10 U = 2.1e-5 | 4.1e-6 | 1e-11 | 5e-15 | 4.1e-6 | PASS both |
| G4 galaxy full, law S at 1-30 kpc | 1e-2 | 3.7e-6 | 2.7e-7 | 1.1e-8 | 4.8e-6 | PASS both |
| G5 galaxy full vs weak | 10 U = 9.6e-6 | 5.4e-7 | 1.1e-12 | 2e-14 | 5.5e-7 | PASS both |
| X1 weak exterior vs QX17B's converged solve_bvp | 1e-3 | Sun 1.6e-4, galaxy 4.9e-6 | | | Sun 3.8e-4, galaxy 4.9e-6 | PASS both |

C1 (Newton) holds in every run. C2 and C3 hold for every gate: each change is at most 10 % of the tolerance, and most are
far below.

**MUTATE** (phantom-mass feedback dropped, G = gN): converges (C1), and G1 and G4 FAIL at 0.78 on both footings, as
required. G2, G3 and G5 still pass under MUTATE. They do not test the phantom mass, so they cannot see this mutation.

## What the solutions say

- **Sun (full GR).** y/g* = 1.0000028 / 1.0000070 / 1.0000070 at 1 / 10 / 100 AU. The extra field is the constant
  hedgehog g* = GM/Lstar^2, to 7e-6.
- **GR corrections are small.** Full minus weak is 4.1e-6 relative for the Sun and 5.4e-7 for the galaxy, both about 2
  U_max or less.
- **Galaxy (1e10 Msun ball).** Law S to 4e-6 at 1-30 kpc.
- **Law S as Lstar -> 0.** Law S to 4e-7 at Lstar = 1e-3 pc.

**Isolated point Sun, far field (not gated; no Galactic field, no other stars):**

| r / Lstar | 1 | 3 | 10 | 30 | 100 | 1000 |
|---|---|---|---|---|---|---|
| g / g_lawS, canonical | 0.0036 | 0.0059 | 0.018 | 0.051 | 0.156 | 0.71 |
| g / g_lawS, alt | 0.0031 | 0.0051 | 0.015 | 0.044 | 0.137 | 0.67 |

**Correction to QX17B §3.** QX17B said the isolated Sun reaches law S "around 1e3 Lstar". That was an extrapolation. The
converged solve gives 0.71 / 0.67 at 1e3 Lstar (~22 kpc), still short of law S.

A lone star's screening reaches far: its far field approaches law S only slowly. A smooth galaxy shows law S cleanly.
Whether a galaxy built from screened stars does is **open**; granularity is untested. Do not cite this as a result about
real galaxies.
