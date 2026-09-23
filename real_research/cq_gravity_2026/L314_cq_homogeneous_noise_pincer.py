#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L314 -- THE HOMOGENEOUS-NOISE PINCER: the published postquantum classical-gravity theory cannot rectify into
the phantom, because its noise does not know where the matter is.

L313 left one live corner: constraint-violating quasi-static scalar noise can carry a phantom that passes
the KiDS lensing gate at 1.6 sigma.  L313 also recorded that the noise would have to TRACK the phantom
(rms ~1e3 x the mean field at r_M) and that nothing supplies that.  This lane asks whether the PUBLISHED
theory -- constant couplings D0, beta (OR24 eq. 4; the covariant D_{mn rs} of the CQ path integral) --
can supply it.

  S1 EXACT: the Newtonian CQ action  I = -c0 int (lap Phi - 4 pi G m)^2  with Phi = Phi_cl + dPhi and
     lap Phi_cl = 4 pi G m is  -c0 int (lap dPhi)^2: the fluctuation action has NO m(x) in it.  The noise is
     translation-invariant whatever the matter does, so <|grad dPhi|^2> is UNIFORM, and so is the rectified
     rho_eff in every averaging convention (L313's forms are linear in the variances with constant
     coefficients).
  S2 SHAPE: a uniform rho_eff added to baryons gives v^2 = GM/r + (4 pi/3) G rho r^2, i.e. a lensing-RAR slope
     d ln g_obs/d ln g_bar -> -1/2 at low g_bar, vs the committed KiDS +0.537 +/- 0.026 (L248).
  S3 MAGNITUDE: to supply the phantom at the MOND radius of a galaxy of baryonic mass M_b the uniform density
     must be rho_ph(r_M) = a0^{3/2}/(4 pi G sqrt(G M_b)); being uniform, it is ALSO the cosmic mean density of
     that component today.  Compared with the whole cosmic dark-matter density Omega_dm rho_crit.
  S4 RELATIVISTIC LEAK: the covariant weight sqrt(-g) D(g) modulates the variance only at O(Phi/c^2) ~ (v/c)^2;
     the phantom's own contrast across a galaxy is ~1e4.
  MUTATE=1 uses a background with lap Phi_cl = 1.1 x 4 pi G m: the cross term survives and S1 must FAIL.

Run from the repository root:  python3 real_research/cq_gravity_2026/L314_cq_homogeneous_noise_pincer.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L314_cq_homogeneous_noise_pincer"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L314", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__)
c_SI, G_SI = 2.99792458e8, 6.67430e-11
MPC, KPC, MSUN = 3.0856775814913673e22, 3.0856775814913673e19, 1.98892e30
H0, OMEGA_L, OMEGA_DM = 67.4, 0.685, 0.265
RHO_CRIT = 3 * (H0 * 1e3 / MPC)**2 / (8 * math.pi * G_SI)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
L248 = json.load(open(os.path.join(REPO, "fable_independent_2026", "L248_results.json")))
SLOPE_LOW, SLOPE_ERR = L248["slope_low"], L248["slope_low_err"]

# ============================================================================================ S1
banner("S1  THE FLUCTUATION ACTION IS SOURCE-FREE (exact)")
x, y, z = sp.symbols("x y z", real=True)
Gs, c0, beta = sp.symbols("G c0 beta", positive=True)
m = sp.Function("m")(x, y, z)
dP = sp.Function("dPhi")(x, y, z)
lap = lambda f: sum(sp.diff(f, v, 2) for v in (x, y, z))
lapPcl = (sp.Rational(11, 10) if MUTATE else 1) * 4 * sp.pi * Gs * m      # lap Phi_cl (the saddle solves Poisson)
integrand = -c0 * (1 - beta) / Gs**2 * (lapPcl + lap(dP) - 4 * sp.pi * Gs * m)**2
resid = sp.simplify(sp.expand(integrand - (-c0 * (1 - beta) / Gs**2 * lap(dP)**2)))
has_m = resid.has(m)
check("S1 around the saddle the OR24 action is -c0(1-beta)/G^2 (lap dPhi)^2 with NO m(x): the noise statistics "
      "are translation-invariant for ANY matter distribution", f"residual after removing (lap dPhi)^2: {resid}",
      resid == 0 and not has_m,
      "<|grad dPhi|^2> is the same in a galaxy, in a void and in the lab -- the rectified rho_eff is UNIFORM")

# ============================================================================================ S2
banner("S2  SHAPE: a uniform rectified density is not the deep-MOND law")
gb, Mb, rho = sp.symbols("g_b M_b rho", positive=True)
r_of_gb = sp.sqrt(Gs * Mb / gb)
g_obs = gb + sp.Rational(4, 3) * sp.pi * Gs * rho * r_of_gb
slope_lim = sp.limit(sp.diff(sp.log(g_obs), gb) * gb, gb, 0)
zS = (SLOPE_LOW - float(slope_lim)) / SLOPE_ERR
check("S2 uniform rho_eff: d ln g_obs/d ln g_bar -> %s at low g_bar vs the committed KiDS %.3f +/- %.3f (L248)"
      % (slope_lim, SLOPE_LOW, SLOPE_ERR), f"{zS:.1f} sigma", zS > 5,
      "rotation rises as v ~ r instead of flattening; the lensing RAR would turn DOWN, it measures +0.54")

# ============================================================================================ S3
banner("S3  MAGNITUDE: the uniform density a galaxy's phantom needs, vs the whole cosmic dark matter")
rows = {}
worst = None
for fk, a0 in A0.items():
    for lm in (8, 9, 10, 11, 12):
        M = 10**lm * MSUN
        rM = math.sqrt(G_SI * M / a0)
        rho_rM = a0**1.5 / (4 * math.pi * G_SI * math.sqrt(G_SI * M))
        rho_10 = rho_rM / 100.0                       # rho_ph ~ r^-2: at 10 r_M
        rat = rho_rM / (OMEGA_DM * RHO_CRIT)
        rat10 = rho_10 / (OMEGA_DM * RHO_CRIT)
        rows[f"{fk}_1e{lm}"] = dict(r_M_kpc=rM / KPC, rho_rM=rho_rM, over_dm=rat, over_dm_at_10rM=rat10)
        worst = rat10 if worst is None else min(worst, rat10)
        P(f"    {fk:9s} M_b = 1e{lm:2d}: r_M = {rM/KPC:7.2f} kpc  rho_ph(r_M) = {rho_rM:.2e} kg/m^3 = "
          f"{rat:9.0f} x Omega_dm rho_crit   (at 10 r_M: {rat10:7.1f} x)")
OUT["numbers"]["magnitude"] = rows
cap_frac = 1.0 / max(v["over_dm"] for v in rows.values() if True)
H_blow = math.sqrt(1 + min(v["over_dm"] for v in rows.values()) * OMEGA_DM)
check("S3 even for the most massive galaxy on the most favourable footing, a UNIFORM density large enough to be "
      "the phantom at r_M exceeds the entire cosmic dark-matter density by >= 1e3, and still exceeds it at 10 r_M",
      f"min over M_b and footings: {min(v['over_dm'] for v in rows.values()):.0f} x at r_M, {worst:.1f} x at 10 r_M; "
      f"it would raise H0 by >= {H_blow:.0f} x", min(v["over_dm"] for v in rows.values()) > 1e3 and worst > 1,
      "the pincer: strong enough for galaxies => overcloses the universe; capped by cosmology => <= 1e-3 of "
      "the phantom")

# ============================================================================================ S4
banner("S4  THE RELATIVISTIC LEAK: how much source-dependence the covariant weight can add")
v_gal = (G_SI * 1e11 * MSUN * A0["canonical"])**0.25
leak = (v_gal / c_SI)**2
need = 100.0**2                                    # rho_ph contrast between 1 and 100 r_M-scale radii (r^-2)
check("S4 the covariant weight sqrt(-g) D(g) makes the variance source-dependent only at O(Phi/c^2) ~ (v/c)^2 = "
      "%.1e; the phantom must vary by ~%.0e across a galaxy" % (leak, need),
      f"shortfall ~{need/leak:.0e}", need / leak > 1e8,
      "no relativistic correction of a constant-coupling theory turns uniform noise into a halo-shaped one")

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  The published classical-quantum theory (constant D0, beta) produces metric noise whose statistics are
  exactly independent of the matter (S1), so whatever it rectifies into is uniform: the wrong shape
  ({zS:.0f} sigma on the KiDS slope) and, if large enough to matter in galaxies, >= 1e3 x the cosmic dark matter.
  L313's live corner therefore survives ONLY for a diffusion kernel D0(x) that is made to track the phantom,
  i.e. with the MOND law written into the noise by hand -- a reparametrisation, not a derivation.
  CQ gravity: CLOSED as a source of the phantom and of kappa; OPEN only as a host that would need the law as input.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
