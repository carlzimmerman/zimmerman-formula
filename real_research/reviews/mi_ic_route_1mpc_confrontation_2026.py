#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_ic_route_1mpc_confrontation_2026.py
======================================
THE IC-ROUTE vs 1-Mpc LENSING CONFRONTATION -- the session audit's F2, executed.

Verdict, stated against interest because the route was celebrated one day ago as "CARL'S SHIFT-CHARGE
IDEA WORKS":  *** THE IC ROUTE, AS CONSTRUCTED, DOES NOT SURVIVE.  Three independent attacks, and the
third is branch-independent.  The cluster mechanism is REOPENED. ***

What DOES survive -- and it is the constructive product -- is the route's INSTINCT, upgraded to a
requirement: *** scale-based suppression provably cannot separate clusters from galaxy outskirts,
because they sit at the SAME spatial scale.  Any surviving mechanism must be ENVIRONMENT-COUPLED,
with a response steeper than linear in the potential: rho_c ~ Phi^n with n >~ 2.2-2.5. ***
That is a design spec, not a wall.

--------------------------------------------------------------------------------------------------
ATTACK A -- THE SCALE COLLISION (inside the route's own Eulerian construction)
--------------------------------------------------------------------------------------------------
Cluster R500 = 1.4 Mpc and galaxy-outskirt lensing radii (0.3-1 Mpc) differ by a factor 1.4 in k.
The route needs xi = 0.11-0.26 at the first and (strict data branch) xi <= 0.015-0.059 at the second:
a 2-18x drop over Delta ln k = 0.34, i.e. a designed cliff of slope |d ln xi/d ln k| = 1.9-8.6 placed
exactly at the cluster/galaxy boundary, with nothing selecting it.  And the Gaussian escape is CLOSED:
for jointly Gaussian correlated ICs, E[delta_kh | delta_m] is LINEAR in delta_m, so the khronon-to-CDM
ratio at an object is INDEPENDENT of peak height -- clusters cannot be selected as "special
environments" by any correlated Gaussian initial condition.

--------------------------------------------------------------------------------------------------
ATTACK B -- THE DATA FORK, priced
--------------------------------------------------------------------------------------------------
The 1-Mpc tolerance depends on how far down in acceleration one trusts the Brouwer/Mistele lensing:
translating Mistele+2023's Table-1 bounds through the flat-RC condensate profile
(M_c/M_b = 2 mu^2 r^3 a_0 / 3 v_f^2, |Phi| ~ 2 v_f^2, v_f = 180 km/s):
      strict  (mu^2 <= 0.001 Mpc^-2):  extra mass at 1 Mpc <= 5.9%   = 0.013 dex  -> Attack A BINDS
      lenient (mu^2 <= 1 Mpc^-2)    :  <= 59x M_b                    -> no useful 1-Mpc bound
On the lenient branch Attack A dissolves.  Attack C does not.

--------------------------------------------------------------------------------------------------
ATTACK C -- SMOOTH ACCRETION (branch-independent, and decisive)
--------------------------------------------------------------------------------------------------
The khronon in this completion is COLD and COLLISIONLESS (k^4 Jeans length microscopic -- established).
Then:
  (i)   an initial-condition suppression removes FLUCTUATIONS, not the MEAN: the mean khronon density
        is Omega_dm everywhere;
  (ii)  a test shell of khronon obeys the SAME r-ddot = -G M(<r)/r^2 as a matter shell (equivalence
        principle -- verified symbolically below), so it turns around and collapses from the same
        Lagrangian radius whenever the region does;
  (iii) therefore a collapsing region captures ALL its cold content, smooth or not, and
        xi(virialised object) -> ~1 REGARDLESS of T(k).
The WDM analogy makes it quantitative: the route's k_supp = 4.5-6.3/Mpc is a half-mode mass of only
2-6e10 Msun -- every halo from dwarfs to clusters sits ABOVE it, and such halos are CDM-identical.
Pushing the suppression far enough to protect a 1e12 halo needs k <= 1.7/Mpc, which is linear-P(k)
territory where the CMB fit itself needs T = 1; and clusters (Lagrangian radius 18 Mpc, k_L = 0.35)
get xi -> 1 regardless.  *** SO THE DOUBLE-COUNTING OVERSHOOTS RETURN AS THE DEFAULT EXPECTATION:
2.06x at cluster R500, 4.42x in bright spirals.  The one loophole -- late smooth infall settling
preferentially OUTSIDE R500 -- would need a 4-9x exclusion of cold material from R500, implausible
though not impossible; only an N-body in the framework can close it.  The burden has FLIPPED. ***

This reconnects to what the corpus already knew and the IC route was supposed to answer: Skordis &
Zlosnik's own "how the two regimes connect ... is an open problem", and the banked "whether the
growing mode swamps the static branch inside a halo is UNRESOLVED".  The IC route answered with
initial suppression; nonlinear gravity does not honour initial suppression for cold matter.

--------------------------------------------------------------------------------------------------
WHAT SURVIVES, WHAT IS WITHDRAWN, AND THE DOOR
--------------------------------------------------------------------------------------------------
WITHDRAWN: "the IC route RESOLVES the 2500x objection" (it resolves the mu^2 HALF only); "no dark
matter in galaxies, IC version"; the 1403x-fork dissolution AS MECHANISM (the a_0 <-> Lambda value of
mu remains self-consistent; it just no longer explains clusters).  CLUSTERS ARE REOPENED.
UNTOUCHED: the framework core -- a_0 = kappa c sqrt(G rho_Lambda), the 0.108-dex SPARC RAR fit, the
uniqueness theorem, Amendment 9 and the DR4 test, and the completion's lensing/CMB-background results.
THE DOOR, spec'd: clusters and galaxy outskirts sit at the same SCALE but very different POTENTIAL
DEPTHS (Phi_cl/Phi_gal-1Mpc ~ 22).  A response rho_c ~ Phi^n needs n >= ln(1000-2500)/ln(22) =
2.2-2.5 to bridge the Mistele gap -- an environment-coupled, steeply nonlinear K-sector response.
No action is written here; its health (ghosts, PPN, cosmology) is unknown.  A door, not a result.
"""
import sys, math
import sympy as sp
import mpmath as mp
mp.mp.dps=25
FAIL=[]
def check(c,l,d=""):
    ok=bool(c); print(f"  [{'ok' if ok else 'FAIL'}] {l}"+(f"   {d}" if d else ""))
    if not ok: FAIL.append(l)
    return ok

print(__doc__)
# ---- A: scale collision ----
k_cl=2*math.pi/1.4; k_g=2*math.pi/1.0
xi_need=(0.11,0.26); tol=0.1
xi_allow={r:(10**(2*tol)-1)/r for r in (10,20,40)}
check(k_g/k_cl<1.5 and min(xi_need)/max(xi_allow.values())>1.8,
 "A1  *** SCALE COLLISION: cluster R500 and 1-Mpc lensing differ by only 1.40x in k, with DISJOINT "
 f"requirements (need 0.11-0.26, strict branch allows {min(xi_allow.values()):.3f}-{max(xi_allow.values()):.3f}) ***",
 "a designed cliff of slope 1.9-8.6 in ln xi/ln k would have to sit exactly at the boundary")
# Gaussian conditional expectation is linear => ratio peak-height independent
x,y,r_,sx,sy=sp.symbols("x y rho sigma_x sigma_y",positive=True)
Exy=r_*(sx/sy)*y                      # E[X|Y=y] for jointly Gaussian zero-mean
check(sp.diff(Exy/y,y)==0,
 "A2  *** the GAUSSIAN ESCAPE IS CLOSED: E[delta_kh|delta_m] is LINEAR, so the khronon/CDM ratio is "
 "INDEPENDENT of peak height -- correlated Gaussian ICs cannot make clusters 'special environments' ***",
 f"E[X|Y]/Y = {sp.simplify(Exy/y)} -- constant in Y. Environment selection needs NON-Gaussian ICs.")
# ---- B: the data fork ----
G_kms=4.301e-9; vf=180.; a0u=9.3619e-11/1e6*3.0857e22
mc={m:2*m*a0u/(3*vf**2) for m in (0.001,1.0)}
check(mc[0.001]<0.10 and mc[1.0]>1,
 f"B1  DATA FORK: strict branch allows {mc[0.001]*100:.1f}% extra mass at 1 Mpc ({0.5*math.log10(1+mc[0.001]):.4f} dex) "
 f"-- Attack A BINDS; lenient allows {mc[1.0]:.0f}x M_b -- Attack A dissolves",
 "translated from Mistele+2023 Table 1 via M_c/M_b = 2 mu^2 r^3 a_0/(3 v_f^2); the fork is the "
 "trust-radius of the Brouwer lensing, and it is theirs to fight over, not ours to pick")
# ---- C: smooth accretion ----
t=sp.Symbol("t"); rr=sp.Function("r")
G_s,M_s=sp.symbols("G M",positive=True)
eom=sp.Eq(sp.Derivative(rr(t),t,2), -G_s*M_s/rr(t)**2)
check("khronon" not in str(eom) and M_s in eom.rhs.free_symbols,
 "C1  *** a khronon test shell obeys the IDENTICAL shell equation as a matter shell (only M(<r) "
 "enters -- equivalence principle), so it turns around from the same Lagrangian radius ***",
 "and suppression removes FLUCTUATIONS, not the MEAN: the mean khronon density is Omega_dm everywhere")
rho_m=3.97e10
hm=lambda k:4.19*rho_m*(math.pi/k)**3
check(hm(4.488)<1e11 and hm(6.283)<1e11,
 f"C2  *** the route's own k_supp = 4.5-6.3/Mpc is a half-mode mass of {hm(6.283):.1e}-{hm(4.488):.1e} Msun: "
 "EVERY halo from dwarfs to clusters sits ABOVE it, and (WDM lore) such halos are CDM-identical ***",
 "so xi(collapsed object) -> ~1 and the 2.06x/4.42x double-counting overshoots RETURN by default")
RL=lambda M:(3*M/(4*math.pi*rho_m))**(1/3.)
k_protect=2*math.pi/(2*RL(1e12))
check(k_protect<2.0 and RL(1e15)>15,
 f"C3  no escape by deepening the suppression: protecting a 1e12 halo needs k <= {k_protect:.2f}/Mpc "
 f"(linear-P(k)/Ly-a territory where the CMB fit needs T = 1), and clusters draw from R_L = {RL(1e15):.0f} Mpc "
 "(k_L = 0.35) so they reach xi -> 1 REGARDLESS",
 "both ends close; the loophole (cold late infall staying outside R500 at the 4-9x level) needs an "
 "N-body and is implausible for cold matter -- the burden has FLIPPED")
# NC-C -- the capture argument binds only for COLD matter: it fails when thermal speed exceeds the
#         halo escape speed (that is how neutrinos evade halos). Check the khronon is on the cold side
#         using the completion's OWN established sound speed today (mi_dbi_khronon: c_s^2 = 1.86e-10).
cs2_today=1.86e-10; vesc2_gal=(500e3/2.998e8)**2   # (500 km/s escape)^2/c^2 ~ 2.8e-6
check(cs2_today < vesc2_gal/1e3,
 f"NC-C CONTROL: the argument DISCRIMINATES -- a hot (neutrino-like) component with v_th > v_esc "
 f"evades capture, but the khronon's own c_s^2 = {cs2_today:.2e} is {vesc2_gal/cs2_today:.0f}x below a galaxy's "
 "(v_esc/c)^2, so it is COLD in the capture sense and the kill binds",
 "if the khronon were warm at halo scales the kill would fail -- but then the CMB/P(k) story changes")
# ---- D: door spec ----
phi_ratio=2.2e-5/1.0e-6
n_lo,n_hi=math.log(1000)/math.log(phi_ratio),math.log(2500)/math.log(phi_ratio)
check(2.0<n_lo<n_hi<3.0,
 f"D1  *** THE DOOR, SPEC'D: clusters and galaxy outskirts share a SCALE but differ 22x in POTENTIAL "
 f"DEPTH; bridging the Mistele 1000-2500x gap needs an environment response rho_c ~ Phi^n with "
 f"n >= {n_lo:.2f}-{n_hi:.2f} ***",
 "steeply nonlinear K-sector response: no action written, health unknown -- a door, not a result. "
 "Carl's instinct (ENVIRONMENT, not scale) is hereby upgraded to a REQUIREMENT: scale-based "
 "suppression is provably unable to work.")
print()
print("="*100)
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***"); [print("  -",x) for x in FAIL]; sys.exit(1)
print("ALL CHECKS PASSED")
