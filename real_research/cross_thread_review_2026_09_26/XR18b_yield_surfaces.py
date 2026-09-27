#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18b (3 of 4) -- H_K1's YIELD SURFACES AND ZERO-FIELD POINTS: criterion B, the degenerate exponents, and cold matter
(items 4 and 5 of the re-audit: XR18's A1/A2 and B4/B4b re-run at H_K1's yield level, plus the zeros H_K1 no longer plugs).

WHY.  XR18 found, for FP9's H_Y: criterion B's causal part holds at the yield surfaces (0 violations in 649,056 root
evaluations), C_L ~ d^(1/2) and C_T ~ d^(-1/2) there, and cold (pressureless) matter at a yield surface grows faster the
finer it is resolved, Gamma ~ d_min^(-1/4), 20-44 H at 1 kpc and 204-451 H at the xi floor -- bounded by xi, but
resolution-dependent in any particle-mesh (PM) run.  H_K1 moves the yield: y_th(z) = max(0, 2q) x 8 pi G rho_bar L/a0 is
1e-3 - 9e-3 above z_q0 = 0.635 (larger than H_Y's, so the surfaces sit deeper inside the hosts) and ZERO below it.  With no
yield below z_q0, the zeros of the band-passed field -- halo centres, saddles of the web -- are no longer plugged: there the
P2 susceptibility dx/dy = 1/(2 sqrt(y)) diverges at a POINT, not on a surface.

PRE-DECLARED HYPOTHESES (written into this file before its first full run; exploratory runs disclosed in XR18b_README.md:
XR18's B4b recipe run on H_K1's hosts at z = 0.7-4 (Gamma(xi/10) = 190-374 H, p ~ 0.25), made before this file existed)
 H1 [load-bearing] CRITERION B's CAUSAL PART AT H_K1's BACKGROUNDS: on DE12's hosts (z = 0.7, 0.8, 1, 2.5, 4 with H_K1's yield:
    the yielded side approaching d/r_Y = 1e-12, the plug, zero field; z = 0.25 without a yield: the whole profile to 50 Mpc,
    including the exponentially vanishing far field), every angle, alpha_c in {9.62e-14, 3.2e-9}, c_2 in {7.29e-3, 0.1, oo},
    lambda in {0, 1e-9, 1e-3, 0.03, 1, 100}, h in {0, 0.3, 1}: every root U = omega^2/k^2 of FP7's block is real and >= 0.
    (XR18b_symbol_channel S5 proves it for any C_phi >= 0; this is the numerical check on the real profiles.)  MUTATE's sign-
    flipped yield must fail.
 H2 [load-bearing] THE DEGENERATE EXPONENTS: at H_K1's surfaces C_L ~ d^(0.50 +- 0.02) and C_T ~ d^(-0.50 +- 0.02) (fits over
    d/r_Y = 1e-10 .. 1e-5, all 30 hosts); at a zero of the band-passed field below z_q0 (a Gaussian-cored halo centre) C_L and
    C_T ~ r^(0.50 +- 0.02) (fits over r/sigma = 1e-8 .. 1e-4): the zero is a degenerate POINT for phi's symbol.
 H3 [load-bearing] COLD MATTER AT H_K1's YIELD SURFACES (XR18's B4b recipe, the isolated surface mode, 30 hosts at z = 0.7, 0.8,
    1, 2.5, 4): Gamma ~ d_min^(-p), p in [0.20, 0.30] (fit over 40 xi <= d_min <= min(1 kpc, 0.01 r_Y)), saturating within 10%
    between xi/3 and xi/10: bounded by xi, resolution-dependent below it; Gamma(xi/10)/H printed against XR18's 204-451 H.
 H4 [load-bearing] COLD MATTER AT THE UNPLUGGED ZEROS BELOW z_q0 (the exact radial sector about a Gaussian-cored centre,
    sigma = 1 kpc, central density 1e2, 1e4, 1e6 rho_bar, z = 0.25 and 0.5, both footings, the cold medium the core itself):
    the l = 0 growth rate grows with resolution, Gamma ~ d_min^(-p) with p in [0.20, 0.30] (fit over 40 xi <= d_min <= sigma/30),
    and saturates within 10% between xi/3 and xi/10 -- the same resolution-dependence as at a yield surface, now at every
    zero of the band-passed field below z_q0; the web's own zeros (1-D local form Gamma^2 = 4 pi G rho (1 + 1/sqrt(s d)),
    s = y_rms/L) are printed.
The writer's expectation: H1 and H2 pass; H3 passes with Gamma(xi) of the same order as XR18's; H4 passes (and is the new
liability: below z_q0 H_K1 has cold-matter resolution-dependence at points, where H_Y had plugs).

CHECKS
  K1 CONTROL: XR18's committed B4b rates for H_Y (all 24 hosts, every resolution) reproduced with XR18's OWN functions
     (hy_host, x_yield, cum_Q2, r_yield, radial_operator, growth, host_grid, node_Q2w: their text extracted from
     XR18_second_variation.py and run on FP9's and DE12's machinery; nothing of XR18 is executed at top level).
  K2 CONTROL: XR18's committed A2 slopes (C_L, C_T at H_Y's surfaces, 24 hosts) reproduced with XR18_yield_surface's own
     host_profile and r_yield (text extracted) and this lane's stiffness code.
  A1 = H1.  A2 = H2.  B4 (reported: XR18's whole-domain version, which mixes an interior dense-gas mode at z >= 2.5).
  B4b = H3.  Z1 = H4.
MUTATE=1 flips the yield term's sign (J_P2 - 2 y_th sqrt(Y)): C_T = (F_P2 - y_th)/x < 0 near every surface, and A1 must FAIL
(a negative root: a Hadamard instability), rc = 1.

SCOPE.  Frozen backgrounds (DE12's hosts: point-mass baryons for the MOND field, gas f_b (rho_NFW + rho_bar); a Gaussian core
for the zero-field centre), the l = 0 sector exact, cold matter as the adversarial case (pressure or dispersion caps it).
The nonlinear free-boundary problem stays open (XR18 A4/A5).  At most 2 threads.  kappa = 1/2 is FITTED (Z = 5.7888);
nothing here derives it, and nothing here closes the theory.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18b_yield_surfaces.py
"""
import os, sys, io, json, math, time, re, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as sp
from scipy.linalg import eigh
from scipy.optimize import brentq
from scipy.special import gammainc
import XR18b_common as XC

L = XC.Lane("XR18b_yield_surfaces", "XR18b/yield_surfaces")
P, check, banner = L.P, L.check, L.banner
MUT = L.mutate
SGN = -1.0 if MUT else 1.0
P(__doc__.split("CHECKS")[0].strip())
if MUT:
    P("\n  *** MUTATE=1: the yield term's sign is flipped (J_P2 - 2 y_th sqrt(Y)) -- A1 must FAIL ***")

# ================================================================================================ machinery (read-only)
NS9, D12 = XC.load_base()
M6 = NS9["M6"]; A0 = dict(NS9["A0"]); FOOTS = ("canonical", "alt")
x_P2 = NS9["x_P2"]; gfrac = M6["gfrac_smooth"]; G6 = M6["G6"]; MPCm = M6["MPCm"]
KPC, MS = D12["KPC"], D12["MS"]
xns = dict(np=np, math=math, eigh=eigh, x_P2=x_P2, L_phys=NS9["L_phys"], y_th_z=NS9["y_th_z"], gfrac=gfrac,
           shell_frac=M6["shell_frac"], MPCm=MPCm, G6=G6, transition=D12["transition"], KPC=KPC, MS=MS, A0=A0,
           LLh=NS9["LL_of"](1.3, 2.0), FLh=(1e-6, 4.0, NS9["YIELD"]), Z_N=2.0)
exec(XC.extract_defs(os.path.join(XC.HERE, "XR18_second_variation.py"),
                     ["hy_host", "x_yield", "cum_Q2", "r_yield", "radial_operator", "growth", "host_grid", "node_Q2w"]), xns)
hy_host_HY = xns["hy_host"]
HK = XC.hk1_forms(M6, A0)
XI_PC = XC.XI_PC
R18 = json.load(open(os.path.join(XC.HERE, "XR18_second_variation_results.json")))["numbers"]
Y18 = json.load(open(os.path.join(XC.HERE, "XR18_yield_surface_results.json")))["numbers"]
F7 = json.load(open(os.path.join(XC.CHAIN, "FP7_aqual_type_repair_results.json")))["numbers"]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
P(f"\n  machinery: FP9 (FP6 inside) and DE12's host definitions exec'd read-only; XR18's radial functions extracted as text; "
  f"a0 = {A0['canonical']:.4e} / {A0['alt']:.4e}; H_K1: L(1) = {HK['L_of'](1.0) * 1e3:.1f} kpc, y_th(1) = {HK['yth_of'](1.0, 'canonical'):.3e}   {L.el()}")


def hk1_host(z, Mb, foot, r):
    """H_K1's point-mass background on DE12's host (the counterpart of XR18's hy_host): y_N, y_bp, y_th, L [m], a0."""
    a0 = A0[foot]; Lz = HK["L_of"](z) * MPCm; yth = HK["yth_of"](z, foot)
    yN = G6 * Mb * MS / (r ** 2 * a0)
    return dict(yN=yN, ybp=yN * (1 - gfrac(r / Lz)), yth=yth, L=Lz, a0=a0)


# ================================================================================================ K1 XR18's B4b on H_Y
banner("K1  CONTROL: XR18's committed B4b (H_Y, 24 hosts) with XR18's OWN radial functions")


def b4b_rates(z, Mb, f, hostfun, dms=(1000.0, 300.0, 100.0, 30.0, 10.0, 3.0, 1.0)):
    """XR18's B4b recipe verbatim in structure: the surface mode on |r - r_Y| <= max(30 d_min, 10 xi), 60 nodes per side."""
    xns["hy_host"] = hostfun
    xi_pc = XI_PC[f]; xi_m = xi_pc * KPC / 1e3
    tr = xns["transition"](z, Mb, f, 0.25)
    bgf = hostfun(z, Mb, f, tr["r"])
    rY = xns["r_yield"](tr["r"], bgf["ybp"], bgf["yth"], yfun=lambda q: hostfun(z, Mb, f, q)["ybp"])
    rates = {}
    for dpc in dms + (xi_pc / 3, xi_pc / 10):
        dm = dpc * KPC / 1e3; half = max(30 * dm, 10 * xi_m)
        if half >= 0.5 * rY:
            continue
        dd = np.geomspace(dm, half, 60)
        r = np.unique(np.concatenate([rY - dd[::-1], [rY], rY + dd]))
        rho = np.exp(np.interp(np.log(r), np.log(tr["r"]), np.log(tr["rho_b"])))
        Q2w, bg = xns["node_Q2w"](r, z, Mb, f)
        K, Mm = xns["radial_operator"](r, rho, Q2w, 0.0, bg["L"], cold_xi=xi_m)
        rates[dpc] = xns["growth"](K, Mm) / tr["H"]
    dfit = np.array([d for d in dms if 40 * xi_pc <= d <= min(1000.0, 0.01 * rY / KPC * 1e3) and d in rates])
    p_b = -float(np.polyfit(np.log(dfit), np.log([rates[d] for d in dfit]), 1)[0]) if len(dfit) >= 3 else float("nan")
    sat = abs(rates[xi_pc / 10] / rates[xi_pc / 3] - 1) if (xi_pc / 3 in rates and xi_pc / 10 in rates) else float("nan")
    return rY, rates, p_b, sat, len(dfit)


GAL18 = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in FOOTS]
k1dev = 0.0; nk1 = 0
for (z, Mb, f) in GAL18:
    rY, rates, p_b, sat, nf = b4b_rates(z, Mb, f, hy_host_HY)
    ref = R18["B4b"][KEY(z, Mb, f)]["rates"]
    for k_, v in rates.items():
        k1dev = max(k1dev, abs(v / ref[str(k_)] - 1)); nk1 += 1
check("K1 CONTROL: XR18's committed B4b surface-mode rates for H_Y (24 hosts, every resolution d_min = 1 kpc .. xi/10) reproduced with "
      "XR18's own radial functions (text extracted, run on FP9's and DE12's machinery)", f"max relative deviation {k1dev:.1e} over {nk1} rates",
      k1dev <= 1e-12)
P(f"    {L.el()}")

# ================================================================================================ the block's roots
alm, c2m, Cph, lmm, sgm, kk7, ww7 = sp.symbols("alpha_c c_2 C_phi lam_ sigma k omega", real=True)
det7 = sp.sympify(re.sub(r"\blambda\b", "lam_", F7["B3"]["det"]), locals={"alpha_c": alm, "c_2": c2m, "C_phi": Cph, "lam_": lmm,
                                                                          "sigma": sgm, "k": kk7, "omega": ww7})
Us = sp.Symbol("U")
PU = sp.expand(sp.cancel(det7.subs(ww7, sp.sqrt(Us) * kk7) / (64 * kk7 ** 10)))
PUinf = sp.expand(sp.limit(PU / c2m, c2m, sp.oo))
cf_fin = sp.lambdify((alm, c2m, Cph, lmm, sgm), [PU.coeff(Us, 2), PU.coeff(Us, 1), PU.coeff(Us, 0)], "numpy")
cf_inf = sp.lambdify((alm, Cph, lmm, sgm), [PUinf.coeff(Us, 2), PUinf.coeff(Us, 1), PUinf.coeff(Us, 0)], "numpy")


def roots_ok(C, lam, hv, ac, c2):
    """all roots U real and >= 0 (quadratic for lambda > 0; linear at lambda = 0; U = 0 roots allowed)."""
    C = np.asarray(C, float)
    a2, a1, a0_ = cf_inf(ac, C, lam, hv) if c2 is None else cf_fin(ac, c2, C, lam, hv)
    a2, a1, a0_ = [np.broadcast_to(np.asarray(v_, float), C.shape).astype(float) for v_ in (a2, a1, a0_)]
    if lam == 0:
        with np.errstate(divide="ignore", invalid="ignore"):
            U = np.where(a1 != 0, -a0_ / np.where(a1 != 0, a1, 1.0), 0.0)
        return np.isfinite(U) & (U >= -1e-300)
    disc = a1 * a1 - 4 * a2 * a0_
    sq = np.sqrt(np.maximum(disc, 0.0))
    Up, Um = (-a1 + sq) / (2 * a2), (-a1 - sq) / (2 * a2)
    tol = 1e-12 * np.maximum(np.abs(Up), np.abs(Um)) + 1e-300
    return (disc >= -1e-12 * a1 * a1) & (Up >= -tol) & (Um >= -tol)


def FP2(x):
    return x * x / (1 - 2 * x)


def CL_of(x):
    return 2 * x * (1 - x) / (1 - 2 * x) ** 2


def CT_of(x, yth):
    with np.errstate(divide="ignore", invalid="ignore"):
        return (FP2(x) + SGN * yth) / x


def x_static(ybp, yth):
    return x_P2(np.maximum(ybp - yth, 0.0)) if SGN > 0 else x_P2(ybp + yth)


def host_profile(z, Mb, f, hostfun):
    bgfun = lambda r: hostfun(z, Mb, f, r)["ybp"]
    yth = hostfun(z, Mb, f, np.array([1.0]))["yth"]
    rr = np.geomspace(1e-3, 50, 40000) * MPCm
    rY = xns["r_yield"](rr, bgfun(rr), yth, yfun=bgfun) if yth > 0 else float("nan")
    return yth, bgfun, rY


# ================================================================================================ K2 XR18's A2 slopes on H_Y
banner("K2  CONTROL: XR18's committed A2 slopes (H_Y's surfaces, 24 hosts) with this lane's profile code")
# XR18_yield_surface's own host_profile and r_yield (text extracted; it uses FP6's M_sun, XR18_second_variation DE12's)
yns = dict(np=np, math=math, brentq=brentq, A0=A0, L_phys=NS9["L_phys"], y_th_z=NS9["y_th_z"], gfrac=gfrac, G6=G6, MPCm=MPCm,
           MSUN=M6["MSUN"], LLh=NS9["LL_of"](1.3, 2.0), FLh=(1e-6, 4.0, NS9["YIELD"]))
exec(XC.extract_defs(os.path.join(XC.HERE, "XR18_yield_surface.py"), ["r_yield", "host_profile"]), yns)
k2dev = 0.0
for (z, Mb, f) in GAL18:
    a0_, Lz_, yth, bgfun, rY = yns["host_profile"](z, Mb, f)
    d = np.geomspace(1e-10, 1e-5, 40)
    x = x_P2(np.maximum(bgfun(rY * (1 - d)) - yth, 0.0))
    sL = float(np.polyfit(np.log(d), np.log(CL_of(x)), 1)[0])
    sT = float(np.polyfit(np.log(d), np.log((FP2(x) + yth) / x), 1)[0])
    ref = Y18["A2"][KEY(z, Mb, f)]
    k2dev = max(k2dev, abs(sL - ref["slope_CL"]), abs(sT - ref["slope_CT"]))
check("K2 CONTROL: XR18's committed A2 exponents at H_Y's yield surfaces (C_L and C_T slopes over d/r_Y = 1e-10..1e-5, 24 hosts) "
      "reproduced with XR18_yield_surface's own host_profile and r_yield (text extracted) and this lane's stiffness code", f"max absolute deviation {k2dev:.1e}", k2dev <= 1e-9)

# ================================================================================================ A1 criterion B
banner("A1  CRITERION B's CAUSAL PART AT H_K1's BACKGROUNDS: every root real and >= 0 (c_2 = 7.29e-3, 0.1, oo; lambda down to 1e-9)")
GALK = [(z, Mb, f) for z in (0.25, 0.7, 0.8, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in FOOTS]
THETA = np.radians([0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0])
ACS, C2S, LAMS, HS = (9.62e-14, 3.2e-9), (7.29e-3, 0.1, None), (0.0, 1e-9, 1e-3, 0.03, 1.0, 100.0), (0.0, 0.3, 1.0)
a1 = {}; nv_tot = 0; nc_tot = 0
for (z, Mb, f) in GALK:
    yth, bgfun, rY = host_profile(z, Mb, f, hk1_host)
    if np.isfinite(rY):
        rs = np.concatenate([rY * (1 - np.geomspace(1e-12, 0.9, 120)), rY * (1 + np.geomspace(1e-12, 3.0, 40))])
    else:
        rs = np.geomspace(1e-3, 50.0, 200) * MPCm
    x = x_static(bgfun(rs), yth)
    pts = [(xv, "flow") for xv in x[x > 0]] + [(0.0, "plug")] * int(np.sum(x <= 0)) + [(0.0, "zero field")]
    nv = nc = 0
    for (xv, kind) in pts:
        if kind != "flow" and SGN > 0 and yth > 0:
            for ac in ACS:                                           # plug under the yield: phi rigid; the khronon at E = alpha_c
                for c2 in (7.29e-3, 0.1):
                    UK = c2 * (2 - ac) / (ac * (2 + 3 * c2)); nc += 1; nv += int(not (UK > 0))
                nc += 1                                              # c_2 = oo: U_K = (2 - alpha_c)/(3 alpha_c) > 0
            continue
        if kind != "flow" and SGN < 0:
            xv = 1e-12                                               # MUTATE: x = 0 is a stationary state with C_T -> -oo
        if kind != "flow" and SGN > 0 and yth == 0:
            xv = 0.0                                                 # below z_q0: exact zero field, C_T = C_L = 0 (degenerate)
        CT = CT_of(xv, yth) if xv > 0 else (0.0 if yth == 0 else np.inf)
        Cth = CT * np.sin(THETA) ** 2 + CL_of(xv) * np.cos(THETA) ** 2
        for ac in ACS:
            for c2 in C2S:
                for lam in LAMS:
                    for hv in HS:
                        if lam == 0 and hv == 0:
                            continue
                        ok = roots_ok(Cth, lam, hv, ac, c2)
                        nc += len(Cth); nv += int(np.sum(~ok))
    a1[KEY(z, Mb, f)] = dict(r_Y_kpc=rY / KPC if np.isfinite(rY) else None, n_cells=nc, violations=nv, yth=yth)
    nv_tot += nv; nc_tot += nc
P("    hosts: " + "; ".join(f"{k_}: r_Y {('%.1f kpc' % v['r_Y_kpc']) if v['r_Y_kpc'] else 'none (no yield)'}, {v['violations']}/{v['n_cells']}"
                          for k_, v in list(a1.items())[::6]))
check("A1 [H1, pre-declared] CRITERION B's CAUSAL PART AT H_K1's BACKGROUNDS: on DE12's hosts at z = 0.7-4 (H_K1's yield: yielded side "
      "to d/r_Y = 1e-12, plug, zero field) and z = 0.25 (no yield: the whole profile to 50 Mpc), every angle, alpha_c at both ends, "
      "c_2 = 7.29e-3, 0.1, oo, lambda = 0, 1e-9, 1e-3, 0.03, 1, 100, h = 0, 0.3, 1: every root U of FP7's block is real and >= 0",
      f"violations {nv_tot} of {nc_tot} (root, cell) evaluations", nv_tot == 0 and nc_tot > 0,
      "S5 of XR18b_symbol_channel proves it for every C_phi >= 0; below z_q0 the zero-field points carry a U = 0 (non-propagating) root, "
      "a degenerate cone, which criterion B allows")
L.out["numbers"]["A1"] = a1
P(f"    {L.el()}")

# ================================================================================================ A2 exponents
banner("A2  THE DEGENERATE EXPONENTS: surfaces above z_q0 (C_L ~ d^1/2, C_T ~ d^-1/2); a zero-field centre below it (C ~ r^1/2)")
a2 = {}; sl, st = [], []
for (z, Mb, f) in [g_ for g_ in GALK if g_[0] > 0.635]:
    yth, bgfun, rY = host_profile(z, Mb, f, hk1_host)
    d = np.geomspace(1e-10, 1e-5, 40)
    x = x_static(bgfun(rY * (1 - d)), yth)
    with np.errstate(invalid="ignore", divide="ignore"):
        sL = float(np.polyfit(np.log(d), np.log(CL_of(x)), 1)[0]); sT = float(np.polyfit(np.log(d), np.log(np.abs(CT_of(x, yth))), 1)[0])
    a2[KEY(z, Mb, f)] = dict(slope_CL=sL, slope_CT=sT); sl.append(sL); st.append(sT)
# the Gaussian-cored centre below z_q0: y_bp = G M [gfrac(r/sigma) - gfrac(r/sqrt(sigma^2 + L^2))]/(a0 r^2) -> s r at the centre.
# FP6's gfrac_smooth = erf(x/sqrt 2) - sqrt(2/pi) x e^(-x^2/2) cancels catastrophically for x < ~1e-6; the same function in stable
# form is the regularised incomplete gamma P(3/2, x^2/2) (the chi-3 CDF), checked against gfrac_smooth where both are accurate.
gstab = lambda x: gammainc(1.5, 0.5 * np.asarray(x, float) ** 2)
xx_ = np.geomspace(1e-2, 6.0, 400); gdev = float(np.max(np.abs(gstab(xx_) / gfrac(xx_) - 1)))
cz = {}
for f in FOOTS:
    for z in (0.25, 0.5):
        a = 1 / (1 + z); Lz = HK["L_of"](z) * MPCm; sig = KPC
        rho_bar = M6["Om"] * M6["rho_crit0"] / a ** 3
        Mc = 1e4 * rho_bar * (2 * math.pi) ** 1.5 * sig ** 3
        yb = lambda r: G6 * Mc * (gstab(r / sig) - gstab(r / math.sqrt(sig ** 2 + Lz ** 2))) / (A0[f] * r ** 2)
        rr = np.geomspace(1e-8, 1e-4, 40) * sig
        x = x_P2(yb(rr))
        cz[(f, z)] = (float(np.polyfit(np.log(rr), np.log(CL_of(x)), 1)[0]), float(np.polyfit(np.log(rr), np.log(x / (1 - 2 * x)), 1)[0]))
P(f"    above z_q0 ({len(sl)} hosts): C_L slopes [{min(sl):.4f}, {max(sl):.4f}], C_T slopes [{min(st):.4f}, {max(st):.4f}]")
P("    zero-field centre (1e4 rho_bar, sigma = 1 kpc): C_L / C_T slopes in r: " + ", ".join(f"{k_[0][:3]} z={k_[1]}: {v[0]:.4f}/{v[1]:.4f}" for k_, v in cz.items())
  + f"  (stable enclosed fraction P(3/2, x^2/2) vs FP6's gfrac_smooth on x = 0.01-6: {gdev:.1e})")
a2_ok = (all(abs(s_ - 0.5) <= 0.02 for s_ in sl) and all(abs(s_ + 0.5) <= 0.02 for s_ in st)
         and all(abs(v[0] - 0.5) <= 0.02 and abs(v[1] - 0.5) <= 0.02 for v in cz.values()) and gdev < 1e-9)
check("A2 [H2, pre-declared] THE DEGENERATE EXPONENTS: at H_K1's yield surfaces C_L ~ d^(0.50 +- 0.02) and C_T ~ d^(-0.50 +- 0.02) "
      "(all 30 hosts above z_q0); at a zero-field centre below z_q0 C_L and C_T ~ r^(0.50 +- 0.02): a degenerate point",
      f"surfaces: C_L [{min(sl):.4f}, {max(sl):.4f}], C_T [{min(st):.4f}, {max(st):.4f}]; centre: "
      + ", ".join(f"{v[0]:.4f}/{v[1]:.4f}" for v in cz.values()), a2_ok,
      "above z_q0 H_K1's surfaces carry H_Y's structure (XR18 A2/A3: well posed in the energy norm, not in C^1); below z_q0 the "
      "transverse stiffness no longer diverges -- both stiffnesses vanish at the zero")
L.out["numbers"]["A2"] = dict(surfaces=a2, centre={f"{k_[0]}/{k_[1]}": v for k_, v in cz.items()})

# ================================================================================================ B4 / B4b cold matter at H_K1's surfaces
banner("B4 B4b  COLD MATTER AT H_K1's YIELD SURFACES: growth against resolution, and the xi filter's cap")
GALY = [g_ for g_ in GALK if g_[0] > 0.635]
DMINS = (3000.0, 1000.0, 300.0, 100.0, 30.0, 10.0, 3.0, 1.0, 0.3, 0.1)
b4, b4b = {}, {}
for (z, Mb, f) in GALY:
    xns["hy_host"] = hk1_host
    xi_m = XI_PC[f] * KPC / 1e3
    rows = {}
    for dpc in DMINS + (XI_PC[f], XI_PC[f] / 3, XI_PC[f] / 10):
        r, rho, rY, tr = xns["host_grid"](z, Mb, f, N=160, Ng=90, dmin_abs=dpc * KPC / 1e3, lo_fac=0.5, hi_fac=2.0)
        Q2w, bg = xns["node_Q2w"](r, z, Mb, f)
        K, Mm = xns["radial_operator"](r, rho, Q2w, 0.0, bg["L"], cold_xi=xi_m)
        rows[dpc] = xns["growth"](K, Mm) / tr["H"]
    dfit = np.array([d for d in DMINS if d >= 40 * XI_PC[f]])
    pf_ = -float(np.polyfit(np.log(dfit), np.log([rows[d] for d in dfit]), 1)[0])
    b4[KEY(z, Mb, f)] = dict(p=pf_, sat=abs(rows[XI_PC[f] / 10] / rows[XI_PC[f] / 3] - 1), G_xi=rows[XI_PC[f]], G_1kpc=rows[1000.0])
    rY, rates, p_b, sat, nf = b4b_rates(z, Mb, f, hk1_host)
    b4b[KEY(z, Mb, f)] = dict(r_Y_kpc=rY / KPC, rates={str(k_): v for k_, v in rates.items()}, p=p_b, n_fit=nf, sat=sat,
                             G_xi10=rates.get(XI_PC[f] / 10, float("nan")), G_1kpc=rates.get(1000.0, float("nan")))
    P(f"    {KEY(z, Mb, f):22s} r_Y {rY / KPC:7.1f} kpc: surface mode Gamma/H at 1 kpc {rates.get(1000.0, float('nan')):.3g}, 1 pc {rates[1.0]:.3g}, "
      f"xi/10 {rates[XI_PC[f] / 10]:.3g}; p = {p_b:.3f} ({nf} pts), saturation {sat:.1%} | whole-domain (B4) p = {pf_:.3f}")
pb = [v["p"] for v in b4b.values()]; sb = [v["sat"] for v in b4b.values()]; gx = [v["G_xi10"] for v in b4b.values()]
g1 = [v["G_1kpc"] for v in b4b.values() if np.isfinite(v["G_1kpc"])]
check("B4 (reported) XR18's whole-domain version at H_K1's surfaces ([r_Y/2, 2 r_Y], 3 kpc .. 40 xi): mixes the surface mode with "
      "interior dense-gas modes where r_Y is small (as XR18 found at z >= 2.5)",
      f"p in [{min(v['p'] for v in b4.values()):.3f}, {max(v['p'] for v in b4.values()):.3f}]; saturation max {max(v['sat'] for v in b4.values()):.1%}",
      True, load_bearing=False)
b4b_ok = all(np.isfinite(pb)) and min(pb) >= 0.20 and max(pb) <= 0.30 and all(np.isfinite(sb)) and max(sb) < 0.10
check("B4b [H3, pre-declared] COLD MATTER AT H_K1's YIELD SURFACES (the isolated surface mode, 30 hosts at z = 0.7-4): Gamma ~ d_min^(-p), "
      "p in [0.20, 0.30] (40 xi <= d_min <= min(1 kpc, 0.01 r_Y)), saturating within 10% between xi/3 and xi/10",
      f"p in [{np.nanmin(pb):.3f}, {np.nanmax(pb):.3f}]; saturation max {np.nanmax(sb):.1%}; Gamma(1 kpc)/H in [{min(g1):.3g}, {max(g1):.3g}]; "
      f"Gamma(xi/10)/H in [{np.nanmin(gx):.3g}, {np.nanmax(gx):.3g}] (XR18, H_Y: 204-451)", b4b_ok,
      "bounded by xi, resolution-dependent below it: a PM run of cold particles is capped only by its cell size, exactly as under H_Y; "
      "H_K1's surfaces sit deeper in the hosts (r_Y 40-1300 kpc against H_Y's 4-4300), which barely moves the rates")
L.out["numbers"]["B4"] = b4; L.out["numbers"]["B4b"] = b4b
P(f"    {L.el()}")

# ================================================================================================ Z1 cold matter at the unplugged zeros
banner("Z1  COLD MATTER AT THE UNPLUGGED ZEROS BELOW z_q0: the exact radial sector about a Gaussian-cored centre")


def core_rates(z, f, dens, sig_kpc=1.0):
    a = 1 / (1 + z); Lz = HK["L_of"](z) * MPCm; sig = sig_kpc * KPC
    rho_bar = M6["Om"] * M6["rho_crit0"] / a ** 3
    rho_c = dens * rho_bar
    Mc = rho_c * (2 * math.pi) ** 1.5 * sig ** 3
    a0 = A0[f]; xi_m = XI_PC[f] * KPC / 1e3
    yfun = lambda r: G6 * Mc * (gstab(r / sig) - gstab(r / math.sqrt(sig ** 2 + Lz ** 2))) / (a0 * r ** 2)
    rhof = lambda r: rho_c * np.exp(-r ** 2 / (2 * sig ** 2))
    Hz = D12["Hz"](z)
    rates = {}
    for dpc in (100.0, 30.0, 10.0, 3.0, 1.0, 0.3, 0.1, XI_PC[f], XI_PC[f] / 3, XI_PC[f] / 10):
        dm = dpc * KPC / 1e3
        r = np.unique(np.concatenate([np.geomspace(dm, 0.3 * sig, 140), np.geomspace(0.3 * sig, 4 * sig, 60)]))
        edges = np.concatenate([[r[0]], 0.5 * (r[1:] + r[:-1]), [r[-1]]])
        re_ = np.unique(np.concatenate([edges, r]))
        X = xns["cum_Q2"](re_, yfun, 0.0)
        Q2w = np.diff(np.interp(edges, re_, X))
        K, Mm = xns["radial_operator"](r, rhof(r), Q2w, 0.0, Lz, cold_xi=xi_m)
        rates[dpc] = xns["growth"](K, Mm) / Hz
    s = G6 * Mc * (4 * math.pi / 3) * (1 - (sig / math.sqrt(sig ** 2 + Lz ** 2)) ** 3) / ((2 * math.pi) ** 1.5 * sig ** 3 * a0)
    gN = math.sqrt(4 * math.pi * G6 * rho_c) / Hz
    return rates, s, gN


z1 = {}
for f in FOOTS:
    for z in (0.25, 0.5):
        for dens in (1e2, 1e4, 1e6):
            rates, s, gN = core_rates(z, f, dens)
            dfit = np.array([d for d in (100.0, 30.0, 10.0, 3.0, 1.0, 0.3, 0.1) if 40 * XI_PC[f] <= d <= 1000.0 / 30])
            p_ = -float(np.polyfit(np.log(dfit), np.log([rates[d] for d in dfit]), 1)[0])
            sat = abs(rates[XI_PC[f] / 10] / rates[XI_PC[f] / 3] - 1)
            z1[(f, z, dens)] = dict(rates={str(k_): v for k_, v in rates.items()}, p=p_, sat=sat, s=s, Gamma_Newton=gN,
                                    G_xi10=rates[XI_PC[f] / 10])
            P(f"    {f[:3]} z = {z} centre {dens:.0e} rho_bar (s = {s:.2e}/m): Gamma/H at d_min = 30 pc {rates[30.0]:.3g}, 1 pc {rates[1.0]:.3g}, "
              f"xi/10 {rates[XI_PC[f] / 10]:.3g} (Newton alone {gN:.3g}); p = {p_:.3f}; saturation {sat:.1%}")
# the web's own zeros: the 1-D local form with the xi cap (reported)
NSf = XC.load_fp19()
webz = {}
for f in FOOTS:
    for z in (0.0, 0.25, 0.5):
        a = 1 / (1 + z); i = int(np.argmin(np.abs(NSf["AGR"] - a))); Lp = NSf["LK_head"](a)
        yr = float(NSf["rms_bp_L"](i, [Lp], A0[f])[0]); s = yr / (Lp * MPCm)
        Om_z = M6["Om"] / a ** 3 / NSf["Ez"](a) ** 2
        for dlab, dm in (("PM cell 50 kpc", 50 * KPC), ("1 kpc", KPC), ("1 pc", KPC / 1e3), ("xi", XI_PC[f] * KPC / 1e3)):
            webz[(f, z, dlab)] = math.sqrt(1.5 * Om_z * (1 + 1 / math.sqrt(s * dm)))           # Gamma/H at mean density
P("    the web's zeros at mean density (1-D local form, s = y_rms/L): " + "; ".join(
    f"z = {z}: " + ", ".join(f"{dl} {webz[('canonical', z, dl)]:.3g}" for dl in ("PM cell 50 kpc", "1 kpc", "1 pc", "xi")) for z in (0.0, 0.25, 0.5)) + "  [Gamma/H]")
pz = [v["p"] for v in z1.values()]; sz = [v["sat"] for v in z1.values()]
z1_ok = min(pz) >= 0.20 and max(pz) <= 0.30 and max(sz) < 0.10
check("Z1 [H4, pre-declared] COLD MATTER AT THE UNPLUGGED ZEROS BELOW z_q0: about a Gaussian-cored centre (1e2-1e6 rho_bar, z = 0.25 "
      "and 0.5, both footings) the exact l = 0 growth rate scales as d_min^(-p), p in [0.20, 0.30] (40 xi <= d_min <= sigma/30), "
      "saturating within 10% between xi/3 and xi/10",
      f"p in [{min(pz):.3f}, {max(pz):.3f}]; saturation max {max(sz):.1%}; Gamma(xi/10)/Gamma_Newton in "
      f"[{min(v['G_xi10'] / v['Gamma_Newton'] for v in z1.values()):.2f}, {max(v['G_xi10'] / v['Gamma_Newton'] for v in z1.values()):.2f}]; "
      f"web zeros at mean density: {webz[('canonical', 0.25, 'PM cell 50 kpc')]:.2g} H at a 50 kpc cell -> {webz[('canonical', 0.25, 'xi')]:.3g} H at xi (z = 0.25)",
      z1_ok,
      "below z_q0 H_K1 carries the yield surface's cold-matter resolution-dependence to every zero of the band-passed field (halo "
      "centres, saddles): H_Y plugged those points (y_th > 0 at every z); a PM run must show convergence there or give the matter a "
      "physical width")
L.out["numbers"]["Z1"] = {f"{k_[0]}/{k_[1]}/{k_[2]:.0e}": v for k_, v in z1.items()}
L.out["numbers"]["Z1_web"] = {f"{k_[0]}/{k_[1]}/{k_[2]}": v for k_, v in webz.items()}

banner("VERDICT")
nlb = sum(1 for _, ok, lb in L.ch if lb and not ok)
pf = {k_: ("PASS" if L.out["checks"][k_]["ok"] else "FAIL") for k_ in ("A1", "A2", "B4b", "Z1")}
P(f"""  Item 5 (criterion B).  Every root of FP7's block is real and >= 0 at H_K1's backgrounds{' [MUTATE: sign-flipped yield]' if MUT else ''} ({nv_tot} violations in {nc_tot};
    A1: {pf['A1']}); the surfaces above z_q0 carry H_Y's degenerate exponents and the zeros below it are degenerate points (A2: {pf['A2']}).
  Item 4 (cold matter).  At H_K1's yield surfaces the isolated surface mode grows as d_min^(-p), p = {np.nanmin(pb):.3f}-{np.nanmax(pb):.3f},
    capped at xi: {np.nanmin(gx):.3g}-{np.nanmax(gx):.3g} H (XR18/H_Y: 204-451 H) -- resolution-dependent (B4b: {pf['B4b']}).  Below z_q0 the same
    d_min^(-1/4) growth appears at every zero of the band-passed field, which H_K1 no longer plugs: p = {min(pz):.3f}-{max(pz):.3f}, capped at xi
    (Z1: {pf['Z1']}); at the web's zeros at mean density ~{webz[('canonical', 0.25, 'PM cell 50 kpc')]:.1f} H at a 50 kpc cell, {webz[('canonical', 0.25, 'xi')]:.0f} H at xi.
  Not 'closed'.  kappa = 1/2 FITTED.  {sum(1 for _, o_, _l in L.ch if o_)}/{len(L.ch)} checks pass; load-bearing failures: {nlb}.""")
L.out["ledger"] = [
    dict(link="XR18b-A1", status="DERIVED" if L.out["checks"]["A1"]["ok"] else "FAILS", what="criterion B's causal part at H_K1's backgrounds"),
    dict(link="XR18b-B4b", status="CONSTRAINT", what="cold matter at H_K1's yield surfaces: d_min^(-1/4), capped at xi (190-374 H)"),
    dict(link="XR18b-Z1", status="CONSTRAINT", what="below z_q0 the same resolution-dependence at every zero of the band-passed field (unplugged)"),
]
L.finish()
