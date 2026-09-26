#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L372 -- A CARRIER FOR HARVEY AND X-COP TOGETHER.  Part 1: the single-channel pincer.  Part 2: a two-channel carrier that
passes both, with the forest, S_8, the galaxy gate and KiDS kept.

WHY.  Harvey+2015 needs group cores (lensing M200 1e14-3e14, z ~ 0.2-0.6) to keep most of their collisionless carrier: L370
(B3, B6, B7) and L371 show that a hollowed or depleted core lets the displaced gas drag the lensing peak (measured
<beta> = -0.04 +/- 0.07).  X-COP needs massive clusters at z ~ 0.05 to keep only 0.22-0.77 of their carrier inside R500
(L354's two-sided gate, as L366 reads it).  The carriers on the record each fail one side: L357 (vacuum-gated, 3000 km/s
kicks) empties group cores; L366 (ungated, ~650 km/s) loses group carrier through their progenitors.

PART 1 -- ONE CHANNEL: L357's trigger (p = 2; 'cleared', x_v0 = 2000; 'cap', x_v0 = 1000) at a finite kick v_k from 600 to
  3000 km/s.  Pre-declared hypothesis (from a coarse run of this lane): a PINCER -- escape is monotonic in potential depth,
  so any kick that strips massive clusters to X-COP's ceiling strips group cores harder.  Slow kicks pass forest, S_8,
  galaxies and KiDS and Harvey but fail X-COP (clusters recapture); fast kicks pass X-COP and fail Harvey.
PART 2 -- TWO CHANNELS: the carrier X has two decay modes.
  U  spatially uniform, L319's rate law Gamma_U = Gamma_0 [Omega_L(a)/Omega_L,0]^2 (fraction f_U(0) decayed today), fast
     daughters v_U = 3000 km/s.  It removes carrier from every host by nearly the same fraction and keeps each host's SHAPE
     (cusp) -- the depletion X-COP needs without hollowing group cores.  In the deepest cluster cores (central escape speed
     ~4600 km/s for A2319) its daughters are partly retained: that is computed, not assumed (L321's retained()).
  G  L357's vacuum-gated density trigger with a SLOW kick v_G (750-1050 km/s): galaxies (escape speeds 300-900 km/s) lose
     their daughters, groups and clusters recapture theirs.
  Combination (stated approximation): the retained fractions multiply, host by host (the modes act on the same parents;
  treating them as independent is exact when either is small and conservative for Harvey, where U is applied as the full
  uniform factor 1 - f_U(z)).  Forest and S_8: L319's solver on the product survival S_U S_G, with every decayed particle
  given v_U (the conservative bound, more free streaming) and, as the other bound, v_G.
  Grid: f_U(0) in {0.20, 0.25, 0.30, 0.35}, v_G in {750, 900, 1050} km/s, G on ('cleared', x_v0 = 2000, p = 2).  (A coarse
  run of this lane placed the grid: at f_U(0) = 0.35 channel U's 3000 km/s daughters cost S_8 0.737 < 0.748 while X-COP
  already passed strictly, so the window, if any, lies at smaller f_U.)
GATES (all pre-declared, both footings where they apply): forest T^2(k = 5) at z = 3, 2 >= 0.9952 (strict) or 0.9 (loose);
  S_8 >= 0.767 (strict) or 0.748 (alternative); X-COP two-sided, strict or after 6% non-thermal support (L322/L354);
  galaxies <= 0.06 dex in L321's three hosts; KiDS-1000 web-blind kernel Delta chi^2 <= +9 (L355/L357); Harvey: L370's
  machinery, population-mean excess beta <= +0.10 on all three estimators (100 / 150 kpc apertures, projected-NFW fit).
CHECKS
  C1 CONTROL: L357's committed best cell (p = 2, cleared, x_v0 = 2000, v_k = 3000) reproduced (forest 0.9984, S_8 0.772,
     X-COP 1.08 / 1.13; tolerances 0.002 / 0.003 / 0.02).
  P1 THE PINCER: no single-channel cell passes both X-COP (alternative set) and Harvey, while a slow cell that fails X-COP
     passes Harvey and the fast cell that passes X-COP fails Harvey.
  W1 THE TWO-CHANNEL WINDOW: a two-channel cell passes forest + S_8 + X-COP + galaxies + KiDS + Harvey together (strict or
     alternative threshold set).
  W2 (reported) the full gate table, and the S_8 of each passing cell with the other free-streaming bound (v_G).
MUTATE=1 switches channel U off (f_U = 0 in every two-channel cell): X-COP must fail and W1 must flip (rc = 1).
LIMITS (stated): L357/L321's static, full-depth, phase-mixed retention (no assembly history -- L366's PM machinery is the
  next check for a passing cell); one gate exponent; Harvey on the canonical footing; U's partial retention computed only in
  X-COP's reference cluster.

Run from the repository root:  python3 real_research/merger_infall_2026/L372_gated_slow_kick_carrier.py
"""
import os, sys, json, math, time, io, contextlib, warnings
from concurrent.futures import ThreadPoolExecutor
import numpy as np
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
FAST = os.environ.get("FAST", "0") == "1"                             # smoke test only; never committed
SLUG = "L372_gated_slow_kick_carrier" + ("_MUTATE" if MUTATE else "") + ("_FAST" if FAST else "")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L372", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: channel U switched off (f_U = 0) -- X-COP must fail and W1 must flip ***")

# ------------------------------------------------------------------------------------------------ L357's machinery, unedited
P57 = os.path.join(REPO, "real_research", "dark_sector_2026", "L357_virialization_triggered_carrier.py")
_s57 = open(P57).read()
_head57 = _s57.split("# ================================================================================ CONTROLS")[0]
_head57 = _head57.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
os.environ["L357_THREADS"] = "4"
_mut, os.environ["MUTATE"] = os.environ.get("MUTATE", "0"), "0"      # the loaded lanes' own MUTATE stays off
L57 = {"__name__": "l357", "__file__": P57}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_head57, L57)
os.environ["MUTATE"] = _mut
L57["MUTATE"] = False
exec(_s57[_s57.index("def gal_eps(pic, xv, vk):"):_s57.index("# the galaxy gate AT the strict forest floor")], L57)
for k_ in ("history", "solve_hist", "retained_core", "rho_thr", "CL", "CLREF", "cl_ratio", "cl_mass_fn", "FOOT", "KPC_M",
           "OL_z", "GE_CL", "gal_eps", "gal_shifts", "nfw21", "mfn", "y_of", "hernquist", "M200_KIDS", "c200_55", "RHOC_ZL",
           "ZL", "LOGMS", "rr55", "esd_of_M", "MS", "Rd55", "Rp55", "MPCm", "FB", "kids_score", "T2_53", "S8_LCDM", "Lm",
           "G19", "a_grid", "RHOC0_KPC", "Ez2"):
    globals()[k_ + "_57"] = L57[k_]
retained_L321 = Lm_57["retained"]                                     # L321's uniform decay (Newtonian orbits, as L354/L357)
surv_triggered = G19_57["surv_triggered"]                             # L319's Lambda-triggered survival S(a) on a_grid
P(f"  L357 machinery loaded (L319 solver, halo model, L321 retention, L355 KiDS): LCDM S_8 {S8_LCDM_57:.4f}   [{time.time() - T0:.0f}s]")
NT, P_GATE = 0.06, 2.0


def x_eff(x_v0, z):
    return x_v0 * (OL_z_57(0) / OL_z_57(z)) ** P_GATE


def xcop_eps_G(pic, x_v0, vk):
    rv_ = rho_thr_57(x_eff(x_v0, CLREF_57["z"]), CLREF_57["z"], CLREF_57["rhoc"])
    return retained_core_57(cl_mass_fn_57, CLREF_57["M200"], CLREF_57["c"], CLREF_57["R500"], GE_CL_57, vk, rv_, pic,
                            rhoc=CLREF_57["rhoc"])[0]


def xcop_from_eps(eps):
    """L357's xcop(): L321's X-COP median at this retention, both footings (sets the shared A0: serial only)."""
    out = {"eps": eps}
    for f_ in FOOT_57:
        Lm_57["A0"] = FOOT_57[f_] * KPC_M_57 / 1e6
        med = float(np.median([cl_ratio_57(c_, eps, "additive") for c_ in CL_57]))
        out[f_] = dict(ratio=med, strict=abs(med - 1) <= 0.2, alt=abs(med * (1 - NT) - 1) <= 0.2)
    return out


def kids_templates_vk(x_eff_zl, picture, vk, scale=1.0):
    """L357's kids_templates with the finite kick (L357 passed v_k = 1e5, full escape) and a uniform carrier factor."""
    T, rvs = [], []
    for b in range(4):
        M200 = M200_KIDS_57[b]; c = float(c200_55_57(M200))
        Mn, r200, rs = nfw21_57(M200, c, RHOC_ZL_57)
        pro = np.geomspace(0.02 * rs, 0.999 * r200, 40)
        rv_ = rho_thr_57(x_eff_zl, ZL_57, RHOC_ZL_57)
        rho_s = M200 / (4 * math.pi * rs ** 3 * mfn_57(c)); yv = float(y_of_57(np.array([rho_s / rv_]))[0]) * rs
        rvs.append(min(yv, r200))
        Mb_fn = hernquist_57(1.3 * 10 ** LOGMS_57[b], 3.0)
        _, ratio_p, _ = retained_core_57(Mb_fn, M200, c, r200, 0.0, vk, rv_, picture, rhoc=RHOC_ZL_57, probes=pro, N=8000)
        r_kpc = rr55_57 / KPC_M_57
        Mc = scale * (1 - FB_57) * Mn(np.minimum(r_kpc, r200)) * np.interp(np.log(r_kpc), np.log(pro), ratio_p)
        dS = esd_of_M_57(Mc * MS_57 + 1.0, 1.0)
        T.append(np.interp(Rd55_57[b], Rp55_57 / MPCm_57, dS))
    return T, rvs


def fU_of_z(fU0, z):
    if fU0 <= 0: return 0.0
    S, _ = surv_triggered(fU0, 2)
    return float(1 - np.interp(1 / (1 + z), a_grid_57, S))


# ================================================================================================ C1
banner("C1  CONTROL: L357's committed best cell (p = 2, cleared, x_v0 = 2000, v_k = 3000)")
S, _ = history_57(2000.0, P_GATE, "cleared", 3000.0)
sol = solve_hist_57(S, 3000.0)
xc0 = xcop_from_eps(xcop_eps_G("cleared", 2000.0, 3000.0))
c1 = dict(T2=min(sol["t2"], sol["t3"]), S8=sol["S8"], xcop=(xc0["canonical"]["ratio"], xc0["alt"]["ratio"]))
check("C1 CONTROL: L357's committed best cell reproduced (forest 0.9984 +/- 0.002, S_8 0.772 +/- 0.003, X-COP 1.08/1.13 +/- 0.02)",
      f"T^2 {c1['T2']:.4f}, S_8 {c1['S8']:.3f}, X-COP {c1['xcop'][0]:.3f}/{c1['xcop'][1]:.3f}",
      abs(c1["T2"] - 0.9984) < 0.002 and abs(c1["S8"] - 0.772) < 0.003 and abs(c1["xcop"][0] - 1.08) < 0.02
      and abs(c1["xcop"][1] - 1.13) < 0.02)
OUT["numbers"]["C1"] = c1

# ================================================================================================ channel G on its own
banner("PART 1  ONE CHANNEL: L357's trigger with a finite kick (forest, S_8, X-COP, galaxies, KiDS)")
VK1 = [750.0, 3000.0] if FAST else [600.0, 750.0, 900.0, 1050.0, 1200.0, 2000.0, 3000.0]
CELLS1 = [("cleared", 2000.0, v) for v in VK1] + ([] if FAST else [("cap", 1000.0, v) for v in (750.0, 1050.0, 3000.0)])


def g_job(cell):
    pic, xv, vk = cell
    S, _ = history_57(xv, P_GATE, pic, vk)
    return cell, dict(SG=S, sol=solve_hist_57(S, vk), epsG=xcop_eps_G(pic, xv, vk),
                      galG=gal_eps_57(pic, x_eff(xv, 0.0), vk), kidsG=kids_templates_vk(x_eff(xv, ZL_57), pic, vk))


with ThreadPoolExecutor(4) as ex:
    GRAW = dict(ex.map(g_job, CELLS1))
P(f"    channel-G retention and histories done for {len(GRAW)} cells   [{time.time() - T0:.0f}s]")


def score(cell_label, sol, eps_xcop, gal_eps, kids_T):
    """the non-Harvey gates for one cell (serial: shared state)."""
    r = dict(t2=sol["t2"], t3=sol["t3"], S8=sol["S8"])
    r["xcop"] = xcop_from_eps(eps_xcop)
    r["gal_shift"] = gal_shifts_57(gal_eps)
    ks = kids_score_57(kids_T)
    r["kids"] = {f"{k[0]}|{k[1]}": v["dchi2"] for k, v in ks.items()}
    T2 = min(r["t2"], r["t3"])
    r["forest_strict"], r["forest_loose"] = T2 >= T2_53_57, T2 >= 0.9
    r["S8_strict"], r["S8_alt"] = r["S8"] >= 0.767, r["S8"] >= 0.748
    r["xcop_strict"] = all(r["xcop"][f_]["strict"] for f_ in ("canonical", "alt"))
    r["xcop_alt"] = all(r["xcop"][f_]["alt"] for f_ in ("canonical", "alt"))
    r["gal_max"] = max(abs(v) for f_ in r["gal_shift"] for v in r["gal_shift"][f_].values())
    r["gal_ok"] = r["gal_max"] <= 0.06
    r["kids_ok"] = all(r["kids"][f"web-blind kernel|{f_}"] <= 9.0 for f_ in ("canonical", "alt"))
    P(f"    {cell_label}: forest T2 {T2:.4f}; S8 {r['S8']:.3f}; X-COP eps {eps_xcop:.2f} -> {r['xcop']['canonical']['ratio']:.2f}/"
      f"{r['xcop']['alt']['ratio']:.2f}; galaxies {r['gal_max']:+.3f} dex; KiDS {r['kids']['web-blind kernel|canonical']:+.1f}/"
      f"{r['kids']['web-blind kernel|alt']:+.1f}")
    return r


ROWS1 = {}
for cell in CELLS1:
    g = GRAW[cell]
    ROWS1[cell] = score(f"G {cell[0]:7s} x_v0 {cell[1]:5.0f} v_k {cell[2]:5.0f}", g["sol"], g["epsG"], g["galG"], g["kidsG"][0])

# ================================================================================================ channel U + G
banner("PART 2  TWO CHANNELS: uniform fast mode U (L319's rate law, v_U = 3000 km/s) + slow triggered mode G")
FU0S = [0.35] if FAST else [0.20, 0.25, 0.30, 0.35]
VG2 = [750.0] if FAST else [750.0, 900.0, 1050.0]
V_U = 3000.0
CELLS2 = [(fu, vg) for fu in FU0S for vg in VG2]
ZREF = CLREF_57["z"]


def u_xcop_job(fu):
    """channel U's retention in X-COP's reference cluster: L321's retained() with the fraction decayed by z_ref."""
    fz = 0.0 if MUTATE else fU_of_z(fu, ZREF)
    if fz <= 0: return fu, 1.0
    return fu, retained_L321(cl_mass_fn_57, CLREF_57["M200"], CLREF_57["c"], CLREF_57["R500"], GE_CL_57, "newtonian",
                             V_U, fz, rhoc=CLREF_57["rhoc"])[0]


with ThreadPoolExecutor(3) as ex:
    EPS_U = dict(ex.map(u_xcop_job, FU0S))
P("    channel U in the reference cluster (retained inside R500): " + ", ".join(
    f"f_U(0) {fu:.2f} -> f_U(z_ref) {fU_of_z(fu, ZREF):.3f}, retained {EPS_U[fu]:.3f} (uniform would be {1 - fU_of_z(fu, ZREF):.3f})"
    for fu in FU0S) + f"   [{time.time() - T0:.0f}s]")
ROWS2 = {}
for (fu, vg) in CELLS2:
    fu_eff = 0.0 if MUTATE else fu
    g = GRAW[("cleared", 2000.0, vg)]
    SU, _ = surv_triggered(fu_eff, 2) if fu_eff > 0 else (np.ones_like(a_grid_57), 0.0)
    S2 = SU * g["SG"]
    sol_c = solve_hist_57(S2, V_U)                                     # conservative: every decayed particle at v_U
    sol_g = solve_hist_57(S2, vg)                                      # the other bound
    fz0, fzl = fU_of_z(fu_eff, 0.0), fU_of_z(fu_eff, ZL_57)
    galU = {k: v * (1 - fz0) for k, v in g["galG"].items()}
    T_U = [t * (1 - fzl) for t in g["kidsG"][0]]                       # the carrier's ESD is linear in its mass
    r = score(f"U+G f_U(0) {fu:.2f} v_G {vg:5.0f}", sol_c, g["epsG"] * EPS_U[fu] if fu_eff > 0 else g["epsG"], galU, T_U)
    r["S8_vG"] = sol_g["S8"]; r["fU_z"] = {"0": fz0, "0.25": fzl, "0.4": fU_of_z(fu_eff, 0.4), "zref": fU_of_z(fu_eff, ZREF)}
    ROWS2[(fu, vg)] = r

# ================================================================================================ Harvey
banner("HARVEY  (L370's machinery): the slow and fast one-channel references, and every two-channel cell passing the rest")
P70 = os.path.join(HERE, "L370_boosted_infall_mergers.py")
_s70 = open(P70).read()
_head70 = _s70.split("# ============================================================================================================ C1")[0]
_head70 = _head70.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
_mut, os.environ["MUTATE"] = os.environ.get("MUTATE", "0"), "0"
L70 = {"__name__": "l370", "__file__": P70}
exec(_head70, L70)
os.environ["MUTATE"] = _mut
L70["MUTATE"] = False
RealHalo, cum_mass, m_in, RG, A0K, SW_DEF, Grid, phantom_felt = (L70[k] for k in (
    "RealHalo", "cum_mass", "m_in", "RG", "A0K", "SW_DEF", "Grid", "phantom_felt"))
from scipy.optimize import brentq
from scipy.interpolate import PchipInterpolator
ZH, NH, LH = 0.4, (160 if FAST else 400), 10000.0
GH = Grid(NH, LH); DXH = GH.dx
XSUB, HARV_BETA, HARV_ERR = 400.0, -0.04, 0.07
L70.update(dict(GH=GH, DXH=DXH, NH=NH, LH=LH))
exec(_s70[_s70.index("def centroid(S, x0, y0, Rap, it=12):"):_s70.index("HB = []")], L70)
centroid, nfw_fit_centre, paint_at = L70["centroid"], L70["nfw_fit_centre"], L70["paint_at"]
RHOC_H = RHOC0_KPC_57 * Ez2_57(ZH)
EST = ("100", "150", "fit")
CONF = [(Msub, dSG, orient) for Msub in (1e14, 3e14) for dSG in (60.0, 120.0) for orient in ("perp", "toward_main")]
FGAS_S, FSTAR_S = 0.10, 0.02


def ratio_profile(H, pic, xv, vk):
    Mb_tab = cum_mass(H.rho_b)
    Mb_fn = lambda r: np.interp(np.asarray(r, float), RG, Mb_tab)
    rv_ = rho_thr_57(x_eff(xv, ZH), ZH, RHOC_H)
    pro = np.geomspace(10.0, 2.0 * H.R200, 24)
    _, q, _ = retained_core_57(Mb_fn, H.M200, H.c, H.R200, 0.0, vk, rv_, pic, rhoc=RHOC_H, probes=pro)
    return pro, np.asarray(q)


def solve_processed(M200L, pic, xv, vk, uscale, fgas, fstar):
    """the construction's real halo, its carrier processed by G (retained_core at z = 0.4) and U (uniform factor),
    solved so that real + phantom gives the lensing M200."""
    pro, q = ratio_profile(RealHalo(M200L, ZH, fgas, fstar, "intact"), pic, xv, vk)
    f = PchipInterpolator(np.log(pro), np.clip(q, 0.0, 2.0))

    def build(M):
        H = RealHalo(M, ZH, fgas, fstar, "intact")
        Mc0 = cum_mass(H.rho_c)
        qr = np.where(RG < pro[0], q[0], np.where(RG > pro[-1], q[-1], f(np.log(np.clip(RG, pro[0], pro[-1])))))
        H.rho_c = uscale * np.maximum(np.gradient(qr * Mc0, RG) / (4 * math.pi * RG ** 2), 0.0)
        H.rho = H.rho_b + H.rho_c
        return H
    M = brentq(lambda M: build(M).lensing(A0K["canonical"], SW_DEF)["M200L"] - M200L, 0.2 * M200L, 6.0 * M200L, rtol=1e-6)
    return build(M)


RES = {}
for (Msub, dSG, orient) in CONF:                                       # LCDM: the same components, all real (as L370/L371)
    gx, gy = (XSUB, dSG) if orient == "perp" else (XSUB - dSG, 0.0)
    ux, uy = ((0.0, 1.0) if orient == "perp" else (-1.0, 0.0))
    HsL, _ = L70["solve_real"](Msub, ZH, A0K["canonical"], SW_DEF, "intact", fgas=FGAS_S, fstar=FSTAR_S, kernel=False)
    SL = (paint_at(HsL.rho_c + HsL.rho_s, XSUB, 0.0, m_in(HsL.rho_c + HsL.rho_s, 1e9))
          + paint_at(HsL.rho_g, gx, gy, m_in(HsL.rho_g, 1e9))).sum(axis=2) * DXH
    res = dict(gx=gx, gy=gy, ux=ux, uy=uy, dSG=dSG)
    for Rap in (100.0, 150.0):
        cx, cy = centroid(SL, XSUB, 0.0, Rap); res[f"LCDM_{Rap:.0f}"] = (cx - XSUB) * ux + cy * uy
    fx, fy = nfw_fit_centre(SL, XSUB, 0.0); res["LCDM_fit"] = (fx - XSUB) * ux + fy * uy
    RES[(Msub, dSG, orient)] = res
ic0 = NH // 2; icx = int(round((XSUB + LH / 2) / DXH))


def harvey(pic, xv, vk, uscale_z04):
    Hm = solve_processed(1e15, pic, xv, vk, uscale_z04, 0.125, 0.015)
    bm = paint_at(Hm.rho_b, 0.0, 0.0, m_in(Hm.rho_b, 1e9)); cm = paint_at(Hm.rho_c, 0.0, 0.0, m_in(Hm.rho_c, 1e9))
    _, _, rph, _ = phantom_felt(GH, bm, bm + cm, ZH, A0K["canonical"], SW_DEF, [(ic0, ic0, ic0)])
    SMAIN = (bm + cm + rph).sum(axis=2) * DXH
    del rph
    beta = {e: [] for e in EST}; core = {}
    for Msub in (1e14, 3e14):
        Hs = solve_processed(Msub, pic, xv, vk, uscale_z04, FGAS_S, FSTAR_S)
        core[Msub] = m_in(Hs.rho_c, 150.0) / m_in(Hs.rho_b, 150.0)
        ss = paint_at(Hs.rho_s, XSUB, 0.0, m_in(Hs.rho_s, 1e9)); cs = paint_at(Hs.rho_c, XSUB, 0.0, m_in(Hs.rho_c, 1e9))
        for (Ms_, dSG, orient) in CONF:
            if Ms_ != Msub:
                continue
            res = RES[(Msub, dSG, orient)]
            gs = paint_at(Hs.rho_g, res["gx"], res["gy"], m_in(Hs.rho_g, 1e9))
            rb = bm + ss + gs; rreal = rb + cm + cs
            _, _, rph, _ = phantom_felt(GH, rb, rreal, ZH, A0K["canonical"], SW_DEF, [(ic0, ic0, ic0), (icx, ic0, ic0)])
            S = (rreal + rph).sum(axis=2) * DXH - SMAIN
            for Rap in (100.0, 150.0):
                cx, cy = centroid(S, XSUB, 0.0, Rap)
                beta[f"{Rap:.0f}"].append(((cx - XSUB) * res["ux"] + cy * res["uy"] - res[f"LCDM_{Rap:.0f}"]) / dSG)
            fx, fy = nfw_fit_centre(S, XSUB, 0.0)
            beta["fit"].append(((fx - XSUB) * res["ux"] + fy * res["uy"] - res["LCDM_fit"]) / dSG)
            del gs, rb, rreal, rph
        del ss, cs
    del bm, cm, SMAIN
    b = {e: float(np.mean(v)) for e, v in beta.items()}
    return dict(beta=b, core=core, ok=all(b[e] <= HARV_BETA + 2 * HARV_ERR for e in EST))


def non_harvey_ok(r):
    return (r["forest_strict"] or r["forest_loose"]) and r["S8_alt"] and r["xcop_alt"] and r["gal_ok"] and r["kids_ok"]


HV = {}
for tag, cell in (("G slow", ("cleared", 2000.0, 750.0)), ("G fast", ("cleared", 2000.0, 3000.0))):
    HV[("1",) + cell] = harvey(*cell, 1.0)
    h = HV[("1",) + cell]
    P(f"    {tag} {cell}: excess beta " + "/".join(f"{h['beta'][e]:+.3f}" for e in EST)
      + f"; core carrier/baryons(<150 kpc) {h['core'][1e14]:.2f} / {h['core'][3e14]:.2f} -> {'PASS' if h['ok'] else 'FAIL'}   [{time.time() - T0:.0f}s]")
cand2 = sorted([c for c, r in ROWS2.items() if non_harvey_ok(r)], key=lambda c: -ROWS2[c]["S8"])[:6]
for (fu, vg) in cand2:
    us = 1 - ROWS2[(fu, vg)]["fU_z"]["0.4"]
    HV[("2", fu, vg)] = harvey("cleared", 2000.0, vg, us)
    h = HV[("2", fu, vg)]
    P(f"    U+G f_U(0) {fu:.2f} v_G {vg:5.0f} (U factor at z = 0.4: {us:.3f}): excess beta " + "/".join(f"{h['beta'][e]:+.3f}" for e in EST)
      + f"; core carrier/baryons(<150 kpc) {h['core'][1e14]:.2f} / {h['core'][3e14]:.2f} -> {'PASS' if h['ok'] else 'FAIL'}   [{time.time() - T0:.0f}s]")

# ================================================================================================ verdicts
banner("VERDICTS")
xc_h_1 = [c for c in CELLS1 if ROWS1[c]["xcop_alt"] and HV.get(("1",) + c, {}).get("ok", False)]
slow, fast = ("1", "cleared", 2000.0, 750.0), ("1", "cleared", 2000.0, 3000.0)
p1 = (len(xc_h_1) == 0 and not ROWS1[slow[1:]]["xcop_alt"] and HV[slow]["ok"]
      and ROWS1[fast[1:]]["xcop_alt"] and not HV[fast]["ok"])
check("P1 THE PINCER: no single-channel cell passes both X-COP and Harvey; the slow cell fails X-COP and passes Harvey, the "
      "fast cell passes X-COP and fails Harvey",
      f"slow: X-COP {ROWS1[slow[1:]]['xcop']['canonical']['ratio']:.2f}/{ROWS1[slow[1:]]['xcop']['alt']['ratio']:.2f}, Harvey "
      f"{'pass' if HV[slow]['ok'] else 'fail'} (fit {HV[slow]['beta']['fit']:+.3f}); fast: X-COP "
      f"{ROWS1[fast[1:]]['xcop']['canonical']['ratio']:.2f}/{ROWS1[fast[1:]]['xcop']['alt']['ratio']:.2f}, Harvey "
      f"{'pass' if HV[fast]['ok'] else 'fail'} (fit {HV[fast]['beta']['fit']:+.3f})", p1,
      "escape is monotonic in potential depth: a kick that strips massive clusters to X-COP's ceiling strips group cores harder")
WIN = []
for (fu, vg), r in ROWS2.items():
    h = HV.get(("2", fu, vg))
    for tset in ("strict", "alt"):
        fo = r["forest_strict"] if tset == "strict" else (r["forest_strict"] or r["forest_loose"])
        if fo and (r["S8_strict"] if tset == "strict" else r["S8_alt"]) and (r["xcop_strict"] if tset == "strict" else r["xcop_alt"]) \
                and r["gal_ok"] and r["kids_ok"] and h is not None and h["ok"]:
            WIN.append((tset, fu, vg))
check("W1 THE TWO-CHANNEL WINDOW: a cell passes forest + S_8 + X-COP + galaxies + KiDS + Harvey together (strict or alternative)",
      WIN if WIN else "no cell", len(WIN) > 0,
      "the uniform mode depletes every host by nearly the same fraction and keeps its cusp (X-COP without hollowing group cores); "
      "the slow triggered mode clears galaxies while groups recapture")
table = {}
for (fu, vg), r in ROWS2.items():
    fl = []
    if not (r["forest_strict"] or r["forest_loose"]): fl.append("forest")
    if not r["S8_alt"]: fl.append(f"S8 {r['S8']:.3f}")
    if not r["xcop_alt"]: fl.append(f"X-COP {r['xcop']['canonical']['ratio']:.2f}/{r['xcop']['alt']['ratio']:.2f}")
    if not r["gal_ok"]: fl.append("galaxies")
    if not r["kids_ok"]: fl.append("KiDS")
    h = HV.get(("2", fu, vg))
    if h is not None and not h["ok"]: fl.append(f"Harvey {h['beta']['fit']:+.3f}")
    table[f"{fu}|{vg}"] = fl or ["PASSES EVERY GATE"]
    P(f"    U+G f_U(0) {fu:.2f} v_G {vg:5.0f}: " + ", ".join(table[f"{fu}|{vg}"]) + f"   (S_8 with v_G free streaming: {r['S8_vG']:.3f})")
check("W2 (reported) the two-channel gate table, with each cell's S_8 under the other free-streaming bound", table, True, load_bearing=False)
OUT["numbers"].update(
    part1={"|".join(map(str, c)): {k: v for k, v in r.items()} for c, r in ROWS1.items()},
    part2={f"{c[0]}|{c[1]}": r for c, r in ROWS2.items()},
    eps_U_ref={str(k): v for k, v in EPS_U.items()},
    harvey={"|".join(map(str, k)): v for k, v in HV.items()}, window=WIN)
banner("VERDICT")
n_ok = sum(1 for _, ok, _ in CH if ok); n_lb_fail = sum(1 for _, ok, lb in CH if (not ok) and lb)
P(f"  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}   [{time.time() - T0:.0f}s]")
with open(os.path.join(HERE, SLUG + "_results.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=lambda o: float(o) if np.isscalar(o) else str(o))
P(f"  wrote {SLUG}_results.json")
rc = 1 if n_lb_fail else 0
P(f"rc={rc}")
sys.exit(rc)
