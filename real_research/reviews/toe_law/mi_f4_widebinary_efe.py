#!/usr/bin/env python3
"""
Trilemma calc #1d: F4's wide-binary / EFE phenomenology (next-bite (b) of MI_COUPLING_FAMILY.md).
Modified INERTIA takes the external field through each star's TOTAL acceleration (the mu-argument is the full
worldline acceleration), not through the field equation: boost B = nu(|y_ext zhat + y_int nhat|), averaged over
the internal-orbit orientation nhat. This is the standard first-pass vector-MI prescription (flagged: true MI
evaluates the kernel on the full helical trajectory; eccentric-orbit time variation is second order for the
median statistic). Same prescription applied to three nu shapes (apples-to-apples): F4/standard, simple, McGaugh
RAR. Footings: framework a0 = 9.36e-11 (primary) and canonical 1.2e-10 (convention row). g_ext = 2.15e-10 (solar
neighbourhood, measured, footing-independent). Velocity boost = sqrt(B) (circular-orbit estimator).
Output: the deep-bin boost table, placement inside the WB-3 DR3 degeneracy, and the DR4 fork (kill conditions
both ways). Inline, no swarms.  C. Zimmerman 2026-06-10.
"""
import numpy as np
rng=np.random.default_rng(20260610)
def nu_std(y):    return np.sqrt((y+np.sqrt(y*y+4))/(2*y))      # F4 (susceptibility) shape, exact MI inversion
def nu_simple(y): return 0.5+np.sqrt(0.25+1/y)
def nu_rar(y):    return 1.0/(1.0-np.exp(-np.sqrt(y)))
SHAPES={'F4/standard':nu_std,'simple':nu_simple,'McGaugh RAR':nu_rar}
g_ext=2.15e-10

def boost(nu,y_int,y_ext,n=200000):
    u=rng.uniform(-1,1,n)                                   # cos(angle between internal accel and external field)
    ytot=np.sqrt(y_ext**2+y_int**2+2*y_ext*y_int*u)
    return np.mean(nu(ytot))

for a0,lab in [(9.36e-11,'framework 9.36e-11'),(1.2e-10,'canonical 1.2e-10')]:
    y_ext=g_ext/a0
    print(f"\n=== a0 = {lab}:  y_ext = g_ext/a0 = {y_ext:.2f} ===")
    print(f"  {'y_int=g_N/a0':>12s} | "+" | ".join(f"{k:>12s}" for k in SHAPES)+"   (VELOCITY boost, %)")
    for y_int in (1.0,0.5,0.18,0.06,0.018):
        row=[]
        for k,nu in SHAPES.items():
            B=boost(nu,y_int,y_ext)
            row.append(100*(np.sqrt(B)-1))
        print(f"  {y_int:12.3f} | "+" | ".join(f"{v:11.1f}%" for v in row))

print("""
PLACEMENT vs the WB program (Banik-exact, WB-3 deprojection MC):
  Newton-MC deep-bin medians were 0.588 / 0.639 (g/a0 = 0.18 / 0.018); data 0.647+-0.02 / 0.816+-0.075.
  F4's ~+2-4% velocity boost shifts the Newton medians to ~0.60 / 0.66 -- INSIDE the boost<->contamination
  degeneracy band (the data sit ~2-3 sigma above flat-Newton and are absorbable by f_triple ~ 0.16 either way).
  => F4 is fully CONSISTENT with the DR3 wide-binary state, like Newton and like soft-MOND. No discrimination now.

THE DR4 FORK (the deliverable -- F4 INVERTS it):
  Under the same vector-MI prescription at the framework a0, the deep-bin velocity boost is
     F4/standard: ~+2-4%     simple: ~+13-16%     McGaugh RAR: ~+11-14%
  -- F4's sharp knee (nu(2.3) = 1.08 vs 1.33/1.28) makes its WB signal ~4-6x SMALLER than soft-shape MOND.
  * If Gaia DR4 (3D velocities) finds a CLEAN NULL at ~3% sensitivity: soft-shape MOND (simple/RAR-as-MI) is
    killed, but F4 SURVIVES (its signal sits at/below that sensitivity).
  * If DR4 finds a +10-15% boost: F4 is KILLED while soft shapes are confirmed.
  * Only a measurement at the ~2% level cleanly tests F4 itself.
  Both kill conditions pre-registered here, before DR4. Caveats: vector-MI prescription is first-pass (full
  trajectory-kernel MI may differ at the few-% level -- flagged, not hidden); the a0 normalization for F4 is the
  framework's empirical value (the bath coefficient remains Z-off, per MI_COUPLING_FAMILY.md -- no claim).""")
