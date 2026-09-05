#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""f30 -- the door the coherence length opens: a screened scalar has no post-Newtonian parameters.

WHAT KILLED THE AETHER-SCALAR HOSTS HERE.  AeST and its generalisations were closed on the preferred-frame parameters
(alpha_1 = -4 c_14 - 4(2-K_B)/(J_Y+1), un-tunable: doorA_alpha1_generality_theorem 12/12; alpha_2 1e4-1e5 x over).  The
second term is the MOND scalar's: it exists because, at Solar-System scales, the scalar's static field of the Sun is a
1/r potential (times a fraction f of the Newtonian one), and every PPN parameter is a coefficient of a 1/r-type
post-Newtonian potential.

WHAT THE BIHARMONIC TERM DOES (addendum section F).  With xi^2 (D^2 phi)^2 in the action the scalar's static Green's
function is (1 - e^{-r/xi})/r instead of 1/r: inside xi the potential is  -f G M/xi + f G M r/(2 xi^2) - f G M r^2/(6 xi^3) + ...
-- a constant, a uniform force, and a uniform effective density.  NO 1/r term.  So the scalar's contributions to
gamma, beta, alpha_1, alpha_2 vanish at leading order inside xi, and the alpha_1 lock -- computed with an unscreened
scalar -- does not apply.  What replaces it are two NEW constraints this file computes:
   (1) the uniform effective density -f M/(4 pi xi^3) inside Saturn's orbit must clear the ephemeris bound
       (the same bound f29 S4 applied to the smoothed-QUMOND phantom), which ties f to xi;
   (2) at galactic scales (r >> xi) the scalar's full force returns, so the Newtonian-regime G_eff = G (1 + f) differs
       from the Solar-System G by f: the high-acceleration end of the RAR bounds f.
The aether's own preferred-frame parameters are then those of Einstein-aether, which has a viable post-GW170817
region (c_13 ~ 0 for c_T = 1; alpha_1 = -4 c_14 with c_14 <~ 2.5e-5; Oost, Mukohyama & Wang 2018) -- cited, not recomputed.
The uniform force f G M/(2 xi^2) acts on every body in the Solar System equally and is unobservable in relative motions.

Every check can fail.  Scope: leading-order scalings from the exact linear Green's function; the full PPN expansion
with the k^4 term, and the nonlinear regime, are the calculations named at the end.  Both footings where a_0 enters.
"""
import os, sys, math
import numpy as np
from scipy.integrate import trapezoid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import *

ck = Check()
PC = 3.0857e16; AU = 1.495978707e11; GM_SUN = 6.6743e-11*1.98892e30; MSUN = 1.98892e30
XI_FLOOR, XI_GC = 0.045*PC, 84*PC
R_SAT = 9.54*AU; RHO_BOUND = 1.1e-17                        # Pitjev & Pitjeva 2013 inside Saturn's orbit

P("=" * 118); P("f30 -- the PPN door: a scalar screened by a spatial biharmonic term has no 1/r potential inside xi"); P("=" * 118)

# ---------------------------------------------------------------- 1. the Green's function, verified
P("\n1.  the static Green's function of  nabla^2 phi - xi^2 nabla^4 phi = 4 pi G M delta^3  is  phi = -G M (1 - e^{-r/xi})/r")
xi = XI_FLOOR
k = np.logspace(-3, 3, 7)/xi
phi_k_exact = -4*math.pi*GM_SUN/(k**2*(1 + xi**2*k**2))                 # Fourier transform of the claimed phi
# apply the operator in Fourier space: (k^2 + xi^2 k^4) phi_k must equal -4 pi G M for every k
resid = np.max(np.abs((k**2 + xi**2*k**4)*phi_k_exact/(-4*math.pi*GM_SUN) - 1))
# and the claimed real-space form is the inverse transform of 1/(k^2(1+xi^2 k^2)) = 1/k^2 - 1/(k^2 + xi^-2): Coulomb minus Yukawa
ck("G1 the biharmonic operator's Green's function is Coulomb minus Yukawa, phi = -G M (1 - e^{-r/xi})/r: verified in Fourier "
   "space across six decades of k (the partial-fraction identity 1/[k^2(1+xi^2 k^2)] = 1/k^2 - 1/(k^2 + xi^-2))",
   resid < 1e-12 and abs(1/(k[3]**2*(1 + xi**2*k[3]**2)) - (1/k[3]**2 - 1/(k[3]**2 + xi**-2))) < 1e-12*abs(1/k[3]**2),
   f"max residual {resid:.1e}")
r = np.geomspace(0.1*AU, 1e3*PC, 2000)
def phi_s(r, xi): return -GM_SUN*(1 - np.exp(-r/xi))/r
def force_s(r, xi): return GM_SUN*(1 - np.exp(-r/xi)*(1 + r/xi))/r**2       # -dphi/dr, inward magnitude
S_force = lambda r, xi: 1 - np.exp(-r/xi)*(1 + r/xi)                          # ratio to the unscreened force G M/r^2
lim = np.array([S_force(rr, xi)/(rr**2/(2*xi**2)) for rr in (1e-4*xi, 1e-3*xi, 1e-2*xi)])
ck("G2 inside xi the scalar's force ratio to the unscreened one is r^2/(2 xi^2) -- the potential there is a constant plus a "
   "uniform force plus r^2, with no 1/r term (the leading-order statement the PPN argument rests on)",
   np.all(np.abs(lim - 1) < 0.02), f"S(r)/(r^2/2xi^2) = " + ", ".join(f"{v:.4f}" for v in lim) + " at r/xi = 1e-4, 1e-3, 1e-2")

# ---------------------------------------------------------------- 2. suppression factors at Solar-System radii
P("\n2.  how much of the scalar survives inside the Solar System")
P(f"    {'radius':>14s} " + " ".join(f"{'xi='+format(x/PC,'g')+' pc':>14s}" for x in (XI_FLOOR, 0.1*PC, 1*PC, XI_GC)))
RADII = (("1 AU", AU), ("Saturn 9.5 AU", R_SAT), ("Neptune 30 AU", 30*AU), ("Oort 1e4 AU", 1e4*AU), ("Oort 1e5 AU", 1e5*AU))
for nm, rr in RADII:
    P(f"    {nm:>14s} " + " ".join(f"{S_force(rr, x):14.2e}" for x in (XI_FLOOR, 0.1*PC, 1*PC, XI_GC)))
ck("P1 at every planetary radius and for every admissible xi the scalar's force is suppressed relative to an unscreened "
   "scalar by more than 1e-8 at 1 AU (where the alpha_1 bound from lunar laser ranging and gamma from Cassini live), 1e-6 at "
   "Saturn and 1e-5 at Neptune; the Oort cloud at 1e4-1e5 AU straddles xi and keeps 30-100% of it",
   S_force(AU, XI_FLOOR) < 1e-8 and S_force(R_SAT, XI_FLOOR) < 1e-6 and S_force(30*AU, XI_FLOOR) < 1e-5,
   f"S(1 AU) = {S_force(AU, XI_FLOOR):.1e}, S(Saturn) = {S_force(R_SAT, XI_FLOOR):.1e}, S(Neptune) = {S_force(30*AU, XI_FLOOR):.1e} at xi = 0.045 pc")
info("reading: the PPN parameters are coefficients of 1/r-type potentials; the screened scalar has none inside xi, so its")
info("contributions to gamma-1, beta-1, alpha_1, alpha_2 are absent at leading order and enter only through the (r/xi)^2 tail.")
info("The AeST alpha_1 lock (-4(2-K_B)/(J_Y+1), from an unscreened scalar) therefore does not apply to this host; the aether's")
info("own alpha_1 = -4 c_14 (with c_13 = 0 for c_T = 1) sits in Einstein-aether's viable post-GW170817 region (c_14 <~ 2.5e-5).")

# ---------------------------------------------------------------- 3. the two constraints that replace the lock
P("\n3.  what replaces the lock: (a) the interior force of the screened scalar, (b) G_eff at galactic scales")
# (a) THE KERNEL'S CORE DECIDES THE FLOOR.  The biharmonic (Helmholtz) Green's function (1 - e^{-r/xi})/r is Coulomb minus Yukawa:
#     inside xi its force is CONSTANT in magnitude and sunward, f G M/(2 xi^2) (G2), not the r-proportional force of a smooth-cored
#     (Gaussian) filter.  A constant sunward acceleration is what the repository's alpha = 1 ephemeris gate bounds: the exact
#     alpha = 1 law's a_0/2 sunward anomaly is 1278x over the planetary bound (project_alpha1_ephemeris_liability), i.e.
A_SUNWARD_BOUND = 0.5*A0["canonical"]/1278.0
info(f"planetary bound on a constant sunward acceleration: {A_SUNWARD_BOUND:.2e} m/s^2 (the repository's alpha = 1 ephemeris gate)")
P(f"    {'xi [pc]':>8s} {'f G M/(2 xi^2) at f=1':>22s} {'x bound':>9s} {'max f allowed':>14s}")
FMAX = {}
for x in (XI_FLOOR, 0.1*PC, 0.3*PC, 0.5*PC, 0.8*PC, 1.0*PC, 1.4*PC, 3*PC, XI_GC):
    a1 = GM_SUN/(2*x**2); FMAX[x] = A_SUNWARD_BOUND/a1
    P(f"    {x/PC:8.3f} {a1:22.2e} {a1/A_SUNWARD_BOUND:9.1e} {min(FMAX[x], 1.0):14.4f}")
xi_of_f = lambda f: math.sqrt(f*GM_SUN/(2*A_SUNWARD_BOUND))
# the phantom fraction the screened scalar carries at the Sun is NOT f = 1: in a MOND host the scalar's high-acceleration response is
# the phantom's, of order nu(e_N) - 1 in the Galactic external field (f29: e_N = 1.84 a_0)
f_ph = float(1.0/(1.0 - math.exp(-math.sqrt(1.84))) - 1.0)
info(f"the phantom fraction at the Sun in the Galactic field, nu(e_N) - 1 = {f_ph:.3f} (e_N = 1.84 a_0)  ->  cuspy-kernel floor xi >= {xi_of_f(f_ph)/PC:.2f} pc; "
     f"a scalar carrying the full Newtonian potential (f = 1) would need xi >= {xi_of_f(1.0)/PC:.2f} pc")
ck("C1 (the first replacement constraint, and it is the kernel's CORE that sets it) with the biharmonic operator's cuspy kernel the "
   "screened phantom exerts a constant sunward acceleration f_ph G M/(2 xi^2); the planetary bound then needs xi >= 0.8 pc for the "
   "phantom fraction nu(e_N) - 1 = 0.35 -- eighteen times the smooth-kernel floor of f29 (0.045 pc).  The f29 wide-binary window "
   "(xi ~ 0.05-0.1 pc) survives ONLY for a smooth-cored smoothing; a single biharmonic term does not give one",
   0.5*PC < xi_of_f(f_ph) < 1.5*PC and xi_of_f(f_ph) > 10*XI_FLOOR, f"floor {xi_of_f(f_ph)/PC:.2f} pc at f_ph = {f_ph:.2f}")
info("a smooth-cored local kernel needs the Yukawa cusps to cancel: 1/[k^2 (1+xi_1^2 k^2)(1+xi_2^2 k^2)] (sixth order in spatial")
info("derivatives, two lengths) has a finite force at the origin only if the two Yukawa terms' linear pieces cancel; that is the")
info("next design choice, not a free lunch: it is a second length.")
# (b) at r >> xi the full scalar force returns: G_eff = G (1+f) in the Newtonian regime of galaxies.  The RAR's high-acceleration end
gals = load_sparc(); gb = np.concatenate([g["gbar"] for g in gals]); go = np.concatenate([g["gobs"] for g in gals])
gid = np.concatenate([np.full(len(g["r"]), i) for i, g in enumerate(gals)])
FB = {}
for foot, a0 in A0.items():
    hi = (gb > 5*a0) & (go > 0)
    lg = np.log10(go[hi]/gb[hi]); ids = np.unique(gid[hi])
    per_gal = np.array([np.median(lg[gid[hi] == i]) for i in ids])
    med = float(np.median(per_gal)); rng = np.random.default_rng(30)
    boot = [np.median(rng.choice(per_gal, len(per_gal), replace=True)) for _ in range(2000)]
    FB[foot] = (med, float(np.std(boot)), len(ids), int(hi.sum()))
    info(f"{foot}: SPARC at g_bar > 5 a_0: {FB[foot][3]} points in {FB[foot][2]} galaxies, per-galaxy median log10(g_obs/g_bar) = {med:+.3f} +/- {FB[foot][1]:.3f} "
         f"(Upsilon_d = 0.5, 0.7 bulge) -> 1 + f = {10**med:.3f}; with the M/L calibration systematic of ~0.1 dex, f <~ {10**(med + 0.1) - 1:.2f}")
f_upper = max(10**(FB[f_][0] + 0.10) - 1 for f_ in FB)
ck("C2 (the second replacement constraint) the Newtonian-regime normalisation of the RAR bounds the scalar's high-acceleration "
   "fraction: with the stellar M/L calibration systematic (0.1 dex) allowed, f <~ 0.3 on both footings.  A MOND host whose "
   "scalar is the phantom (f -> nu - 1 -> 0 at high acceleration) satisfies this automatically",
   f_upper < 0.5, f"f <~ {f_upper:.2f}")
# (c) at the cuspy-kernel floor, the wide binaries: xi >= 0.8 pc puts them in f29's flat-1.00 regime
info("consequence for Gaia DR4 in the local biharmonic host: xi >= 0.8 pc lies in f29's regime W3 -- the binaries are Newtonian at every")
info("separation to 30 kAU (gamma_v = 1.00), consistent with a Banik-type null and inconsistent with a Chae-type boost; the pre-registered")
info("1.16-1.23 would be wrong in this host.  The smooth-kernel window (xi ~ 0.05-0.1 pc, boost survives) needs a two-length operator.")

# ---------------------------------------------------------------- 4. the door, stated
P("\n4.  the door")
P("    The aether-scalar hosts were closed here on preferred-frame PPN parameters sourced by an UNSCREENED MOND scalar.  With a")
P("    spatial biharmonic term the scalar has no 1/r potential inside xi: its PPN contributions are absent at leading order (P1).")
P("    What replaces the lock is not a wall but a fork set by the smoothing kernel's CORE: a single biharmonic term (cuspy kernel)")
P("    needs xi >= 0.8 pc, which puts Gaia DR4 at gamma_v = 1.00 and leaves the globulars' 50-140 pc as the natural range; a")
P("    smooth-cored kernel (two lengths, sixth order) allows xi ~ 0.05-0.1 pc with the pre-registered wide-binary boost intact.")
P("    Both satisfy the Solar System, the RAR's Newtonian end (C2), galaxies, lensing and the aether's own PPN region.  This is the")
P("    'Vainshtein / k-mouflage UNRUN' class of RESUME_HERE, realised with a length.  Not yet done, in order: the full PPN expansion")
P("    with the k^4 term; the nonlinear static solve for the Sun in this theory; the Dirac count with the aether; the FLRW background.")
sys.exit(ck.done())
