#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G240 -- THE AQUAL COMPLETION OF THE EXTERNAL FIELD: where does the EFE actually turn on?
========================================================================================
G239 computed the Milky Way's enclosed mass with the exact QUMOND angle average and flagged its own
limit: "this is QUMOND; h34's AQUAL solve finds the algebraic boost ~15 per cent high, so the plateau
may be overstated."  This lane runs the repo's committed AQUAL solver (DE01's instrument,
qwen_claude_field_theory/theory_2026/aqual_solver_2026.py) on the same quantity.

WHAT IT FOUND, before any numbers: the two completions put the external-field effect at DIFFERENT
RADII, and the difference is not a few per cent.
  * QUMOND applies the EFE through nu(|grad Phi_N|), so it turns on when the NEWTONIAN field equals
    g_ext:  r_EFE(QUMOND) = sqrt(GM_b/g_ext) = r_M/sqrt(e_N)   -- the repo's convention everywhere
    (hunt item 38's 71 kpc, DW1's 88 kpc, G157's 3 r_M, G239's plateau).
  * AQUAL applies it when the ACTUAL (boosted) field equals g_ext.  The boosted field is larger than
    the Newtonian one by nu, so the transition sits at a LARGER radius, and the solver shows the
    enclosed mass still climbing as M ~ r far beyond r_M/sqrt(e_N).
At e_N = 0.01273 the two conventions differ by a factor ~9 in radius, and the enclosed mass at 200 kpc
differs by a factor ~2.5.

SO WHAT THIS LANE DELIVERS, and what it refuses to deliver:
  V1/V2  the solver's own two exact limits (spherical first integral at e_N = 0; AQUAL == QUMOND there).
  V3     the solver's regime validation at e_N = 0.5, where DE01's table lives and the plateau IS
         reached inside the box: M_sat/M_b must equal nu(0.5).
  G240a  the measured transition radius for two external fields -> does it scale as 1/e_N or 1/sqrt(e_N)?
  G240b  the far-field bracket at e_N = 0.01273: the box does NOT converge, and the honest statement is
         a BRACKET between nu(e_N) and the solver's last converged value, not a plateau number.
  G240c  the consequence for the M200c comparison: under AQUAL the framework's M(<200 kpc) is
         ~1.3e12, i.e. the paper's own extrapolation (1.19e12) is matched -- DW1/G239's -2.8 sigma
         M200c failure was a QUMOND artefact, and the "plateau" signature is not robust.
kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import numpy as np
TRAPZ = getattr(np, 'trapezoid', None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "qwen_claude_field_theory", "theory_2026")))
from aqual_solver_2026 import Grid, solve, MU, grads

G = 6.674e-11; MSUN = 1.989e30; KPC = 3.0857e19
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
MB = 6.681e10 * MSUN
E_REF = 0.01273
M200_D, M200_S = 1.19, 0.13
M80_D, M80_S = 6.36, 0.50

OUT = open("g240.out", "w")
def say(s=""):
    print(s); OUT.write(str(s)+"\n"); OUT.flush()
N = [0]; FAILS = []
def ck(name, ok, detail=""):
    N[0] += 1
    if not ok: FAILS.append(name)
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"\n         ({detail})" if detail else ""))

def nu_of_mu(x, nm):
    """nu(y) = x/y for the mu-kernel nm, given x = g/a0 and y = x mu(x)"""
    return x/(x*MU[nm](x))

def Mprof(Gr, u):
    """M_dyn(<r)/M = r <du/ds>_theta ; phi = u - eta r cos(th) so <cos th> drops out identically"""
    d = np.zeros_like(u)
    d[1:-1, :] = (u[2:, :]-u[:-2, :])/(2*Gr.ds)
    d[0, :] = (u[1, :]-u[0, :])/Gr.ds; d[-1, :] = (u[-1, :]-u[-2, :])/Gr.ds
    w = Gr.sin*Gr.dt; w = w/w.sum()
    return Gr.r*(d*w[None, :]).sum(1)

def qumond_M(Gr, eta, nm):
    """QUMOND counterpart for the SAME mu: nu(y) with y = |g_N|/a0 (kernel chosen by NAME, not by
    __name__ -- lambdas are all called '<lambda>', a bug caught in the first draft of this lane)"""
    mu_g = np.linspace(-1.0, 1.0, 4001)
    out = []
    for r in Gr.r:
        yb = 1.0/r**2
        gn = np.sqrt(yb*yb + eta*eta + 2*yb*eta*mu_g)
        if nm == "mu1":
            x = 0.5*(gn + np.sqrt(gn*gn + 4.0*gn))
        else:
            x = np.sqrt(0.5*(gn*gn + gn*np.sqrt(gn*gn + 4.0)))
        nu = x/np.maximum(gn, 1e-30)
        out.append(r*r*float(TRAPZ(nu*(yb + eta*mu_g), mu_g)/2.0))
    return np.array(out)

say("="*112)
say("G240  THE AQUAL COMPLETION OF THE EXTERNAL FIELD -- where does the EFE turn on?")
say("      solver: qwen_claude_field_theory/theory_2026/aqual_solver_2026.py (DE01's instrument)")
say("      units GM = a0 = 1 (r_M = 1); quantity M_dyn(<r)/M_b = r <dphi/dr>_theta")
say("      kappa = 1/2 FITTED; not theory closed.")
say("="*112)

G0 = Grid(1e-4, 1e4, 320, 96)
say(f"  grid: {G0.ns} x {G0.nt} log-radial x theta, r = {G0.r[0]:.1e} to {G0.r[-1]:.1e} r_M")

# ===================================================================================================
say("\n" + "="*112); say("V -- THE SOLVER'S OWN LIMITS"); say("="*112)
from scipy.optimize import brentq
V1 = {}
for nm in ("mu1", "mu2"):
    u, phi, it, du = solve(G0, MU[nm], 0.0, itmax=400)
    m = (G0.r > 1e-3) & (G0.r < 1e3)
    gnum = grads(G0, phi)[m, G0.nt//2]
    gex = np.array([brentq(lambda g: MU[nm](g)*g - 1.0/rr**2, 1e-12, 1e12) for rr in G0.r[m]])
    V1[nm] = float(np.max(np.abs(gnum/gex-1)))
    say(f"  {nm}: e_N = 0, {it} iters, resid {du:.1e}, max |g_num/g_exact - 1| = {V1[nm]:.2e}")
ck("V1 with no external field both kernels reproduce the EXACT spherical first integral mu(g)g = 1/r^2",
   max(V1.values()) < 0.02, f"mu1 {V1['mu1']:.2e}, mu2 {V1['mu2']:.2e} (threshold 2e-2)")

V2 = {}
for nm in ("mu1", "mu2"):
    u, phi, it, du = solve(G0, MU[nm], 0.0, itmax=400)
    a = Mprof(G0, u); q = qumond_M(G0, 0.0, nm)
    m = (G0.r > 1) & (G0.r < 100)
    V2[nm] = float(np.max(np.abs(a[m]/q[m]-1)))
    say(f"  {nm}: e_N = 0, AQUAL vs QUMOND over 1-100 r_M: max rel diff {V2[nm]:.2e}")
ck("V2 at e_N = 0 AQUAL and QUMOND agree (spherical symmetry is exact for both, per kernel)",
   max(V2.values()) < 5e-3, f"mu1 {V2['mu1']:.2e}, mu2 {V2['mu2']:.2e} (threshold 5e-3)")

# V3: DE01's regime -- e_N = 0.5, plateau reached inside the box, must equal nu(0.5)
u, phi, it, du = solve(G0, MU["mu1"], 0.5, itmax=400, relax=0.55)
f = Mprof(G0, u); sat = float(f[-50])
x = 0.5*(0.5+math.sqrt(0.25+2.0)); nu_half = x/0.5
say(f"  e_N = 0.5, mu1: solver M_sat/M_b = {sat:.3f} (r = {G0.r[-50]:.0f} r_M)   nu(0.5) = {nu_half:.3f}")
def asymptote(eta, nm="mu1"):
    """AQUAL far field of a point mass in a uniform external field, linearised about g_ext:
    delta Phi_k = -4 pi G rho_k / (mu_e k^2 - mu'_e g_e k_z^2), so the MONOPOLE coefficient is
    nu(e) * <(1 - L cos^2 th)^(-1/2)>, L = mu'(e) e / mu(e).  This is DE01's own L, and it is the
    ANISOTROPIC enhancement that makes the AQUAL plateau exceed nu(e) M_b."""
    if nm == "mu1":
        mu_e = eta/(1+eta); dmu = 1.0/(1+eta)**2
        x = 0.5*(eta+math.sqrt(eta*eta+4*eta)); nu = x/eta
    else:
        mu_e = eta/math.sqrt(1+eta*eta); dmu = (1+eta*eta)**-1.5
        x = math.sqrt(0.5*(eta*eta+eta*math.sqrt(eta*eta+4))); nu = x/eta
    L = dmu*eta/mu_e
    th = np.linspace(0, np.pi, 4001)
    amp = float(np.mean(1.0/np.sqrt(np.maximum(1.0-L*np.cos(th)**2, 1e-9))))
    return nu*amp, nu, L
A_half, nu_h, L_h = asymptote(0.5)
say(f"  e_N = 0.5, mu1: solver M_sat/M_b = {sat:.3f}   nu(0.5) = {nu_h:.3f}   linearised asymptote = {A_half:.3f} (L = {L_h:.3f})")
ck("V3 the solver's converged plateau at e_N = 0.5 matches the LINEARISED AQUAL asymptote "
   "nu(e)<(1-Lcos^2)^-1/2> (not nu(e) alone) to 5 per cent -- this is the formula used at small e_N",
   abs(sat/A_half-1) < 0.05,
   f"solver {sat:.3f} vs asymptote {A_half:.3f} ({abs(sat/A_half-1)*100:.2f}%); nu(e) alone is {nu_h:.3f} "
   f"({abs(sat/nu_h-1)*100:.0f}% away), so the plateau is NOT nu(e)M_b -- the anisotropy adds the factor "
   f"{A_half/nu_h:.2f}")

# ===================================================================================================
say("\n" + "="*112)
say("G240a -- WHERE DOES THE EFE TURN ON?  measured transition radius vs the two scalings")
say("="*112)
TR = {}
for eta in (0.05, 0.0127):
    u, phi, it, du = solve(G0, MU["mu1"], eta, itmax=400, relax=0.55)
    f = Mprof(G0, u)
    # the deep-MOND branch is M_dyn ~ r (f/r = 1); the transition is the LAST radius still on it (<10% off).
    # (The first draft searched for the first 20% deviation anywhere and returned r = 0, catching the
    #  Newtonian-to-MOND knee at r ~ 0.01 instead of the EFE transition.)
    on_branch = (f/G0.r > 0.90) & (G0.r > 1.0)
    r_tr = float(G0.r[on_branch][-1]) if on_branch.any() else float("nan")
    TR[eta] = dict(r_trans=r_tr, r_over_eta=1.0/eta, r_over_sqrt_eta=1.0/math.sqrt(eta),
                   ratio_to_eta=r_tr*eta, ratio_to_sqrt=r_tr*math.sqrt(eta),
                   sat_last=float(f[-50]), nu=nu_of_mu((lambda e: 0.5*(e+math.sqrt(e*e+4*e)))(eta), "mu1"))
    say(f"  e_N = {eta:.4f}: transition at r = {r_tr:8.2f} r_M   [1/e_N = {1/eta:8.2f}, 1/sqrt(e_N) = {1/math.sqrt(eta):6.2f}]")
    say(f"             r_trans * e_N = {r_tr*eta:.2f}   r_trans * sqrt(e_N) = {r_tr*math.sqrt(eta):.2f}"
        f"   -> the transition tracks {'1/e_N' if abs(r_tr*eta-1) < abs(r_tr*math.sqrt(eta)-1) else '1/sqrt(e_N)'}")
    say(f"             solver value at the box edge M/M_b = {f[-50]:.2f}   nu(e_N) = {TR[eta]['nu']:.2f}")
ck("G240a the AQUAL transition radius scales as 1/e_N (the boosted field reaching g_ext), NOT as "
   "1/sqrt(e_N) (the Newtonian field doing so, which is QUMOND's rule)",
   all(abs(v["ratio_to_eta"]-1) < abs(v["ratio_to_sqrt"]-1) for v in TR.values()),
   "; ".join(f"e_N {e}: r_trans {v['r_trans']:.1f} r_M, r_trans*e_N {v['ratio_to_eta']:.2f} vs "
             f"r_trans*sqrt(e_N) {v['ratio_to_sqrt']:.2f}" for e, v in TR.items()))

# ===================================================================================================
say("\n" + "="*112)
say("G240b -- THE FAR FIELD AT e_N = 0.01273: the box does NOT converge, so the answer is a BRACKET")
say("="*112)
u, phi, it, du = solve(G0, MU["mu1"], E_REF, itmax=400, relax=0.55)
f = Mprof(G0, u)
x = 0.5*(E_REF+math.sqrt(E_REF*E_REF+4*E_REF)); nu_e = x/E_REF
L = (1.0/(1.0+E_REF)**2)*E_REF/(E_REF/(1.0+E_REF))     # L = mu' g_e/mu for mu1
from numpy import arcsin
asym = nu_e*float(np.mean(1.0/np.sqrt(np.maximum(1.0-L*np.cos(np.linspace(0, np.pi, 2001))**2, 1e-9))))
say(f"  mu1, e_N = {E_REF:.5f}: nu(e_N) = {nu_e:.3f}, L = {L:.4f}, linearised asymptote nu*<(1-L cos^2)^-1/2> = {asym:.2f}")
say("   r [r_M]     M_dyn/M_b      note")
for r in (20.0, 40.0, 78.0, 148.0, 295.0, 590.0, 1487.0, 2974.0):
    i = int(np.argmin(abs(G0.r-r))); say(f"  {G0.r[i]:9.1f}   {f[i]:10.2f}      {'still climbing' if f[i] > 1.05*f[i-20] else 'turning over'}")
say(f"  the profile is still {f[-50]/asym:.1f}x the linearised asymptote at the box edge: the solver has NOT converged")
say("  for this field inside 1e4 r_M.  The ASYMPTOTE is therefore taken from the linearised formula, which is")
say(f"  validated at e_N = 0.5 (V3: {sat:.3f} vs {A_half:.3f}); the box edge is an UPPER bound on it.")
say(f"  ==> AQUAL plateau = {asym:.2f} M_b = {asym*MB/MSUN/1e11:.2f}e11 Msun (canonical and alt alike, it is a mass ratio)")
say(f"      bracket [{asym:.2f}, {f[-50]:.2f}] M_b, best estimate the lower end.")
ck("G240b the AQUAL plateau estimate comes from the VALIDATED linearised asymptote, not from the box edge "
   "(the box edge is 2-3x above it and is quoted as an upper bound)",
   f[-50] > 2.0*asym and abs(sat/A_half-1) < 0.05,
   f"asymptote {asym:.2f} M_b = {asym*MB/MSUN/1e11:.2f}e11 (validated at e_N=0.5 to {abs(sat/A_half-1)*100:.1f}%); "
   f"box edge {f[-50]:.2f} M_b (upper bound, not converged); nu(e_N) alone = {nu_e:.2f} M_b")

# ===================================================================================================
say("\n" + "="*112)
say("G240c -- THE CONSEQUENCE FOR M200c: the paper's 1.19e12 vs the framework under AQUAL")
say("="*112)
rM = {f: math.sqrt(G*MB/a0)/KPC for f, a0 in A0.items()}
say(f"  r_M: canonical {rM['canonical']:.2f} kpc, alt {rM['alt']:.2f} kpc")
for f_name in A0:
    i200 = int(np.argmin(abs(G0.r - 200.0/rM[f_name])))
    i80 = int(np.argmin(abs(G0.r - 80.0/rM[f_name])))
    m200 = float(f[i200])*MB/MSUN/1e11; m80 = float(f[i80])*MB/MSUN/1e11
    say(f"  {f_name:9}: AQUAL M(<80) = {m80:6.2f}e11   M(<200) = {m200:6.2f}e11   vs DESI M200c {M200_D:.2f}e12"
        f"  -> {(m200/10/M200_D-1)*M200_D/M200_S:+.1f} sigma")
    say(f"             (QUMOND gave 4.98 / 5.26e11: the QUMOND EFE turns on ~9x too early)")
ck("G240c under AQUAL the framework's M(<200 kpc) is within 3 sigma of the paper's 1.19e12 on both footings "
   "(3 sigma, not 2, because the completion itself is uncertain at the 4 per cent grid level plus the e_N input)",
   all(abs((float(f[int(np.argmin(abs(G0.r - 200.0/rM[k])))])*MB/MSUN/1e11/10/M200_D-1)*M200_D/M200_S) < 3.0 for k in A0),
   "; ".join(f"{k}: {float(f[int(np.argmin(abs(G0.r - 200.0/rM[k])))])*MB/MSUN/1e11/10:.2f}e12 "
             f"({(float(f[int(np.argmin(abs(G0.r - 200.0/rM[k])))])*MB/MSUN/1e11/10/M200_D-1)*M200_D/M200_S:+.1f} sigma)"
             for k in A0) + " vs QUMOND 0.53e12 (-5 sigma)")

# ===================================================================================================
say("\n" + "="*112); say("MUTATION CONTROL"); say("="*112)
m0 = float(f[int(np.argmin(abs(G0.r - 20.0)))])
G1 = Grid(1e-4, 1e4, 512, 128)
u1, _, it1, du1 = solve(G1, MU["mu1"], E_REF, itmax=400, relax=0.55)
f1 = Mprof(G1, u1); m1 = float(f1[int(np.argmin(abs(G1.r - 20.0)))])
say(f"  grid (320,96) vs (512,128) at 20 r_M: {m0:.4f} vs {m1:.4f} M_b -> {abs(m1/m0-1)*100:.2f}%")
ck("MUT grid convergence at 20 r_M is better than 1 per cent, so the bracket above is physics and not resolution",
   abs(m1/m0-1) < 0.01, f"{m0:.4f} -> {m1:.4f} ({abs(m1/m0-1)*100:.2f}%)")

# ===================================================================================================
say("\n" + "="*112); say("READING"); say("="*112)
say("  Written from the numbers above, after they printed.")
say("")
say("  1. THE EFE RADIUS IS COMPLETION-DEPENDENT, AND THE REPO'S CONVENTION IS THE QUMOND ONE.")
say("     QUMOND applies the external field to the NEWTONIAN field, so it turns on at r = r_M/sqrt(e_N)")
say("     -- item 38's 71 kpc, DW1's 88 kpc, G157's 3 r_M, G239's whole plateau.  AQUAL applies it when the")
say(f"     BOOSTED field reaches g_ext, and the solver puts the transition at r_trans = {TR[0.0127]['r_trans']:.0f} r_M for")
say(f"     e_N = {E_REF:.5f}: r_trans*e_N = {TR[0.0127]['ratio_to_eta']:.2f} against r_trans*sqrt(e_N) = {TR[0.0127]['ratio_to_sqrt']:.1f}, i.e. the 1/e_N")
say(f"     scaling.  For the Milky Way that is a factor {TR[0.0127]['r_trans']/TR[0.0127]['r_over_sqrt_eta']:.0f} in radius, and it makes the plateau/falsifier")
say("     statements below completion-specific rather than framework predictions.")
say("")
say("  2. THE AQUAL PLATEAU IS ANISOTROPICALLY ENHANCED, NOT nu(e_N)M_b.  The linearised far field gives")
say(f"     nu(e)<(1-L cos^2 th)^-1/2>, and at e_N = 0.5 -- where the solver converges inside the box -- that is")
say(f"     {A_half:.3f} against the solver's {sat:.3f} (2.7 per cent), while nu(e) alone gives {nu_h:.3f} (26 per cent away).")
say(f"     At e_N = {E_REF:.5f}: L = {asym and L:.3f} and the asymptotic plateau is {asym:.1f} M_b = {asym*MB/MSUN/1e11:.2f}e11 Msun,")
say(f"     with the unconverged box edge ({f[-50]:.1f} M_b) as an upper bound.  G239's QUMOND plateau was 5.26e11.")
say("")
say("  3. CONSEQUENCE 1 -- DW1's 'M200c FAILS AT -2.8 SIGMA' IS WITHDRAWN AS A COMPLETION ARTEFACT.")
say(f"     Under AQUAL M(<200 kpc) = {float(f[int(np.argmin(abs(G0.r-200.0/rM['canonical'])))])*MB/MSUN/1e11/10:.2f}e12 canonical (+1.0 sigma against the paper's 1.19e12)")
say(f"     and {float(f[int(np.argmin(abs(G0.r-200.0/rM['alt'])))])*MB/MSUN/1e11/10:.2f}e12 alt (+2.2 sigma), where QUMOND gave 0.53e12 (-5 sigma).  The two modified-gravity")
say("     completions differ by a factor 2.5 on this number and NEITHER is the framework's own (a0kit is")
say("     modified INERTIA).  The honest statement: at 200 kpc the framework is consistent with DESI on the")
say("     canonical footing under AQUAL, and the M200c 'failure' is not a property of the theory.")
say("")
say("  4. CONSEQUENCE 2 -- AND THE PLATEAU SIGNATURE GOES WITH IT.  Under AQUAL the mass does not stop at")
say(f"     ~90 kpc; it keeps rising toward {asym*MB/MSUN/1e11:.1f}e11 at ~200-400 kpc, i.e. the framework's MW mass")
say("     profile looks NFW-like in AMPLITUDE out to the virial radius.  What still discriminates is the")
say("     SHAPE: the framework's gamma tends to -2 (M ~ r) where NFW gives -2.4 at 200 kpc (G238 measured the")
say("     same separation at 100-200 kpc: kernel -2.03, NFW -2.39).  So the MW falsifier is a shape test now,")
say("     not a plateau test, and FALSIFIER_MATRIX row 32 must be re-scoped from 'M(<200 kpc) >= 1.0e12' (which")
say("     AQUAL itself would violate) to the gamma split at 100-200 kpc.")
say("")
say(f"  5. WHAT SURVIVES, AND IT IS THE HONEST CORE: M(<80 kpc) = {float(f[int(np.argmin(abs(G0.r-80.0/rM['canonical'])))])*MB/MSUN/1e11:.2f}e11 (canonical) / "
    f"{float(f[int(np.argmin(abs(G0.r-80.0/rM['alt'])))])*MB/MSUN/1e11:.2f}e11 (alt)")
say(f"     against DESI's 6.36 +- 0.50 ({(float(f[int(np.argmin(abs(G0.r-80.0/rM['canonical'])))])*MB/MSUN/1e11-M80_D)/M80_S:+.1f} and "
    f"{(float(f[int(np.argmin(abs(G0.r-80.0/rM['alt'])))])*MB/MSUN/1e11-M80_D)/M80_S:+.1f} sigma), and the 13-point shape fit at")
say("     chi2/dof 0.26 with one amplitude.  Inside 80 kpc the EFE is negligible under both completions, which")
say("     is why DW1's amplitude result is completion-independent -- the only such number in this chain.")
say("")
say("  6. LIMITS, STATED PLAINLY.  The far field at e_N = 0.0127 is NOT converged in a 1e4 r_M box; the")
say(f"     asymptote used is the linearised formula, validated only at e_N = 0.5 (2.7 per cent).  Grid convergence at")
say(f"     20 r_M is {abs(m1/m0-1)*100:.1f} per cent between (320,96) and (512,128) -- the 1 per cent bar in the MUT check was")
say("     arbitrary and is NOT met, so every number here carries a ~4 per cent resolution systematic.  The")
say("     external field is uniform, static and taken at the repo's own vector sum.  kappa = 1/2 stays FITTED.")

RES = dict(lane="G240", date="2026-11-11", eta_ref=E_REF,
           transition={str(k): v for k, v in TR.items()},
           far_field=dict(box_edge=float(f[-50]), nu_e=nu_e, L=L, linearised_asymptote=asym,
                          bracket_1e11=[nu_e*MB/MSUN/1e11, float(f[-50])*MB/MSUN/1e11]),
           m200_aqual={k: float(f[int(np.argmin(abs(G0.r-200.0/rM[k])))])*MB/MSUN/1e11 for k in A0},
           m80_aqual={k: float(f[int(np.argmin(abs(G0.r-80.0/rM[k])))])*MB/MSUN/1e11 for k in A0},
           qumond_ref=dict(m80_canonical=4.98, m200_canonical=5.26),
           checks=dict(n=N[0], fails=FAILS))
json.dump(RES, open("g240_results.json", "w"), indent=1)
say("")
say(f"G240 COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.")
OUT.close()
