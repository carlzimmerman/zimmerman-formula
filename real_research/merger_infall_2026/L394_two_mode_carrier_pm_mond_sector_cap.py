#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""L394 -- L372's TWO-MODE CARRIER ON M*'s SWITCH AND CAP: the particle-mesh box (L373/L393's two-mode construction, three
realisations pooled) with the switch reading the MOND sector (baryons + their phantom) under MS5's mean-curvature region cap,
at the linear gate p = 1, x_c0 = 2.5 -- M*'s switch and cap, with L372's carrier in place of L388's single kick.

WHY.  MS1 (2a5def6d9): once the gate is an action term, only the MOND-sector reading (baryons + their phantom) keeps the
  carrier Newtonian; the matter and curvature readings leak a force onto it.  MS3 and MS5 (61a3a0858): cosmic shear, scored
  resolution-free, needs every MOND region to stop at l_cap = v_cap/(H sqrt(x_c)) (1.75 Mpc at z = 0.5, v_cap = 325 km/s),
  and MS5 writes that cap as an action term through the mean curvature of the MOND field's equipotentials.  M*, the model the
  threads converge on (cross_thread_review_2026_09_26/ANSWER_AS_IT_STANDS.md), carries L388's single density-triggered kick
  (575-650 km/s); its particle-mesh run is L396 and its Harvey stage L397.  L372's two-mode carrier (a uniform late decay
  plus a vacuum-gated slow kick) was built to pass Harvey and X-COP together; L373 (p = 2, matter switch) found no window
  (X-COP floor; Harvey S2 +0.116), and L393 runs it on the curvature switch at the linear gate (a labelled comparison).  This
  lane asks whether the two-mode carrier has a window on M*'s own switch and cap -- a labelled carrier variant of M*, never
  pooled with M*'s cell.
METHOD.  L393's run2 (L377's full construction + mode U + the vacuum-gated trigger G + the z = 0.4 snapshot) with L396's
  switch "msck", copied verbatim: x_ms = 1.5 Omega_m(a)(rho_b + max(delta_ph,all, 0)) (the baryons plus the positive
  untruncated phantom); the cap x_cap = v_cap^2 kappa_X^2/H(a)^2 with kappa_X = (1/2) div(grad Phi_X/|grad Phi_X|) of the
  MOND-sector potential (the baryons' Newtonian potential + the untruncated phantom's), fourth-order differences, physical
  units, not binding where |grad Phi_X| vanishes; U = (x_ms^-4 + x_cap^-4)^(-1/4) (MS5's smooth min); switched where
  U [Omega_L(a)/Omega_L0] > x_c0 (a sharp gate, w = 0); the phantom then solved on that mask (L377's operator).  Everything
  else as L393: mode U (Gamma ~ Omega_L(a)^2, 3000 km/s), mode G (the mesh trigger x~ > 5 on the phantom-inclusive x~, gated
  by [Omega_L(a)/Omega_L0]^2, rate 10 H), seeds (7, 11), (17, 21), (29, 33), canonical a0; cells f_U(0) = 0.25 at v_G = 600,
  750, 900, 1050 km/s, and f_U(0) = 0.20, 0.30 at 900.
GATES (pre-declared; L393's arithmetic, pooled): S_8 ratio >= 0.922 strict / 0.899 alternative; forest <= 0.10; X-COP
  retention inside L354's two-sided bounds; COSMIC SHEAR ON MS3's HALO MODEL at the cell's own convention and cap (MS3's
  "door", r_cap = 1.75 Mpc at z = 0.5 -- MS5's kappa-form cap reproduces it exactly on spherical profiles; L396's score):
  worst R(k = 0.1-1 h/Mpc) <= 1.2 on both footings with the cell's own pooled retention by halo mass at the lens epoch (the
  z = 0.4 medians in L371's bins at MS3's centres, galaxies (1e13) at the z = 2 fixed-cell clearing); Harvey on every pooled
  cell passing X-COP, with the retention measured at z = 0.4, through L371's shapes (intact control, S1, S2) and L370's
  region operator at the cell p = 1, x_c0 = 2.5 with L370's absolute-density mask (the operator L397 uses for M*'s Harvey;
  XR5 and L392 find the switch operator moves beta by <= 0.002): excess beta <= +0.10 on all three estimators, both shapes.
  Reported, not gated: the z = 2 clearing (the vacuum gate keeps high-z halos by design); the halo-model shear uncapped
  (MS3's X1: expected to fail), with L396's retention construction (z = 0 medians), and with the galaxy anchor replaced by
  the lowest z = 0.4 bin; the switched and capped fractions; the box's own matter transfer T(k) at z = 0.5.
PRE-DECLARED (before the main run).  H: on M*'s switch and cap at the linear gate the two-mode carrier has a window -- a
  pooled cell passes S_8 (alt), forest, X-COP, shear (halo model, capped) and Harvey (both shapes).
CHECKS
  C1 CONTROL: the (7, 11) LCDM run reproduces L366's committed LCDM sigma_8 exactly (same code path, same seeds).
  C2 CONTROL: the Harvey stage runs at the mesh's cell (p1_x2.5) with L370's absolute mask.
  C3 CONTROL (re-scores only): the full-projection betas reproduce the previously written Harvey numbers.
  C4 CONTROL: MS3's halo model, loaded here, reproduces MS3's committed K1 (1.75 Mpc cap, door) and X1 (uncapped, door and
     upper) with L388's retention, both footings (1e-9).
  C5 CONTROL: this lane's mesh mean curvature is 1/r within 5% at r = 1, 2, 3 Mpc/h for a spherical blob (L396's C5).
  C6 SAME SWITCH AS M*: on a lognormal test field at z = 2 and z = 0.4 this lane's switch returns exactly what L396's own
     function returns (mask fraction, potential, phantom), with switched cells at one epoch at least; L396 is read from the
     repository at run time and its commit recorded.  C5 and C6 run before the mesh runs.
  R1 = H.   W (reported) per-realisation and pooled gate tables, switched and capped fractions, retention, the z = 2
     clearing, the shear variants;  W2 (reported) the Harvey edge-layer check (line of sight capped at +-3 and +-1.5 Mpc).
SCOPE.  A labelled carrier variant of M* (L372's two modes in place of L388's single kick), never pooled with M*'s cell.  The
  carrier's trigger and kicks are posited (no action).  The gate is sharp (M* allows w <= 0.25; MS4: the width does not move
  cosmic shear).  The G trigger is the record's mesh proxy (x_c = 5; the mesh cannot resolve L372's x_v0 = 1000-2000).  Harvey
  uses L370's region operator (sigma = 0) at the cell with L370's absolute mask, as L397 does for M*; XR5 (H1): the sigma = 1
  action operator and the PM operator give the same Harvey centroid to |delta beta| <= 0.002 (toward-main).  The halo model
  is one lens epoch (z = 0.5) with isolated regions (MS3's caveats); the galaxy anchor (the z = 2 clearing) is conservative
  for this carrier, which clears late by design.  At z = 2 the cap confines regions to ~0.2 Mpc/h physical (~1.7 cells).
  High-z galaxies keep their carrier (L372's limit).
MUTATE=1 switches mode U off in every decaying run; it is run only if R1 passes.
L394_POOL (default 4), L394_HPOOL (2), L394_RESUME=1 (re-score from the mesh checkpoint), L394_SMOKE=1 (64^3 code test;
  writes nothing here).  Logs go to a scratch path and are copied into this directory at commit.

Run from the repository root:  python3 real_research/merger_infall_2026/L394_two_mode_carrier_pm_mond_sector_cap.py
"""
import os, sys, json, math, time, tempfile, shutil, io, contextlib, warnings
import numpy as np
from multiprocessing import Pool
warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
sys.path.insert(0, DS)
import L377_full_construction_pm as L77                        # noqa: E402  (L377's full construction and helpers, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L394_two_mode_carrier_pm_mond_sector_cap"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L394", "cell": "p=1, x_c0=2.5",
               "switch": "msck: the MOND-sector reading (baryons + positive untruncated phantom) under MS5's mean-curvature cap "
                         "(v_cap = 325 km/s, smooth min n = 4) -- L396's switch, verbatim (M*'s)",
               "carrier": "L372's two modes (U + vacuum-gated G): a labelled carrier variant of M*, never pooled with it",
               "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_WINDOW = True                                             # R1, set before the run
L6, L7, L2 = L77.L6, L77.L7, L77.L2
Om, OL, Hnorm, Om_a, ZI, h = L77.Om, L77.OL, L77.Hnorm, L77.Om_a, L77.ZI, L77.h
WB, WC, LBOX, NG, NP, RHO_M, KG = L77.WB, L77.WC, L77.LBOX, L77.NG, L77.NP, L77.RHO_M, L77.KG
SMOKE = os.environ.get("L394_SMOKE", "0") == "1"
SEEDS = ((7, 11),) if SMOKE else ((7, 11), (17, 21), (29, 33))
if SMOKE:
    NG, NP = 64, 48
    L6.NG = NG                                                     # L366's sphere_sum reads its module's NG
V_U, P_U, P_G = 3000.0, 2, 2
CELLS = [(0.25, 900.0)] if SMOKE else [(0.25, 600.0), (0.20, 900.0), (0.25, 750.0), (0.25, 900.0), (0.25, 1050.0), (0.30, 900.0)]
P_SW, X_SW, SW_KEY, BRANCH = 1.0, 2.5, "p1_x2.5", "msck"                  # the linear gate; M*'s switch (L396's cell)
VCAP2 = (325.0 / 100.0) ** 2                                             # MS5's v_cap = 325 km/s in the code's (100 km/s)^2 (L395/L396)
TAGS = [f"u{int(round(100 * fu))}_g{int(vg)}" for fu, vg in CELLS]
MBINS = (("6.0e+13-1.0e+14", 6e13, 1e14, 7.75e13), ("1.0e+14-1.5e+14", 1e14, 1.5e14, 1.22e14),
         ("1.5e+14-2.5e+14", 1.5e14, 2.5e14, 1.94e14), ("2.5e+14-1.0e+17", 2.5e14, 1e17, 5.0e14))   # L371's bins, MS3's centres


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


def gamma0_U(fu0):
    """Gamma_0 (code time units, H0 = 1) so that 1 - exp(-Gamma_0 int [Omega_L(a)/Omega_L0]^2 dt) = f_U(0), L319's law."""
    if fu0 <= 0: return 0.0
    a = np.geomspace(1 / (1 + ZI), 1.0, 20001)
    w = ((OL / (Om * a ** -3 + OL)) / OL) ** P_U / (a * Hnorm(a))
    I = float(np.sum(0.5 * (w[1:] + w[:-1]) * np.diff(a)))
    return -math.log(1 - fu0) / I


def grad4(f, d):
    """fourth-order central differences (periodic): the mean curvature needs them at 3-5 cells (L396's C5)."""
    return [(-np.roll(f, -2, i) + 8 * np.roll(f, -1, i) - 8 * np.roll(f, 1, i) + np.roll(f, 2, i)) / (12 * d) for i in range(3)]


def div4(v, d):
    return sum((-np.roll(v[i], -2, i) + 8 * np.roll(v[i], -1, i) - 8 * np.roll(v[i], 1, i) + np.roll(v[i], 2, i)) / (12 * d) for i in range(3))


def kappa_mesh(Phi, d):
    """the mean curvature (1/2) div(grad Phi/|grad Phi|) of Phi's level sets, fourth order; +inf where |grad Phi| vanishes."""
    gX = grad4(Phi, d)
    gm = np.sqrt(gX[0] ** 2 + gX[1] ** 2 + gX[2] ** 2)
    ok = gm > 1e-12 * float(gm.max()) + 1e-300
    kap = 0.5 * div4([np.where(ok, g / np.where(ok, gm, 1.0), 0.0) for g in gX], d)
    return kap, ok


SWDIAG = {"steps": 0, "capped_max": 0.0, "switched_max": 0.0}


def phantom_msck(s, rb, rho, a, a0c):
    """L396's switch 'msck', verbatim (the msck branch of its phantom_swk): the MOND-sector reading (the baryons plus the
    positive untruncated phantom) under MS5's mean-curvature cap, smooth min n = 4, at p = 1, x_c0 = 2.5; the phantom is then
    solved on that mask (L377's operator).  C6 checks it against L396's own function at run time."""
    gate = (OL / (Om * a ** -3 + OL) / OL) ** P_SW
    phib = s.poisson(1.5 * Om * (rb - WB) / a)
    gb = [-(1.0 / a) * g for g in s.grad(phib)]
    nu1 = L77.nu_vec(np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / a0c) - 1.0

    def solve(f):
        w = [np.where(f, nu1 * g, 0.0) for g in gb]
        divw = s.div(w)
        return s.poisson(-a * divw), -(2 * a * a / (3 * Om)) * divw

    Phi_all, dph_all = solve(np.ones(rho.shape, bool))
    xms = 1.5 * Om_a(a) * (rb + np.maximum(dph_all, 0.0))
    kap, ok = kappa_mesh(phib + Phi_all, s.d)                   # the MOND-sector potential's level sets (comoving)
    kap = kap / a                                                 # physical mean curvature of the equipotentials
    xcap = np.where(ok, VCAP2 * kap ** 2 / Hnorm(a) ** 2, np.inf)
    U = (np.maximum(xms, 1e-300) ** -4 + np.maximum(xcap, 1e-300) ** -4) ** -0.25
    f = U * gate > X_SW
    f0 = xms * gate > X_SW
    SWDIAG["steps"] += 1
    if f0.any():
        SWDIAG["capped_max"] = max(SWDIAG["capped_max"], float((f0 & ~f).sum() / f0.sum()))
    SWDIAG["switched_max"] = max(SWDIAG["switched_max"], float(f.mean()))
    if not f.any():
        return None, None, 0.0
    Phi, dph = solve(f)
    return Phi, dph, float(f.mean())


def run2(cfg):
    """L377's run() with mode U (uniform, v_U), the vacuum gate on mode G's trigger, and a z = 0.4 snapshot."""
    name, sp, sk, xc, vg, gamma, fu0, tmp, mode, a0 = cfg
    SWDIAG.update(steps=0, capped_max=0.0, switched_max=0.0)       # per run (a pool worker runs several)
    a0c = a0 / L77.ACC_UNIT
    g0U = gamma0_U(fu0)
    s = L2.Sim(LBOX, NG, NP)
    s.deposit = lambda x, w: L6.deposit_fast(s, x, w)
    rng = np.random.default_rng(sp)
    kk = np.sqrt(s.K2); kk[0, 0, 0] = s.kf
    Pk = np.vectorize(lambda q: L2.P_lin(q, ZI))(np.clip(kk, s.kf, 60.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    delta0 = np.real(np.fft.ifftn(white * np.sqrt(Pk * NG ** 3 / LBOX ** 3)))
    psi = [-gg for gg in s.grad(s.poisson(delta0))]
    q = (np.arange(NP) + 0.5) * LBOX / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([s.interp(pp, Q) for pp in psi], 1)
    del QX, QY, QZ, psi, white, delta0, Pk, kk
    ai = 1 / (1 + ZI); fg = Om_a(ai) ** 0.55
    xb = (Q + disp) % LBOX; pb = ai ** 2 * Hnorm(ai) * fg * disp
    del Q, disp
    xcar, pcar = xb.copy(), pb.copy()
    n = len(xb); cold = np.ones(n, bool)
    krng = np.random.default_rng(sk)
    urng = np.random.default_rng(sk + 1000)                           # mode U's own stream (the G stream stays L377's)
    nU = 0

    def fields(xb, xcar, a):
        rb = s.deposit(xb, np.full(n, WB)) * NG ** 3 / n
        rho = rb + s.deposit(xcar, np.full(n, WC)) * NG ** 3 / n
        ph = phantom_msck(s, rb, rho, a, a0c) if mode != "none" else (None, None, 0.0)
        return rho, ph

    def accel(rho, ph, a):
        gr = s.grad(s.poisson(1.5 * Om * (rho - 1.0) / a))
        ab = -np.stack([s.interp(gg, xb) for gg in gr], 1)
        if mode == "full" and ph[0] is not None:
            ab -= np.stack([s.interp(gg, xb) for gg in s.grad(ph[0])], 1)
        return ab, -np.stack([s.interp(gg, xcar) for gg in gr], 1)

    a = ai; dlna = 0.02; zs = [3.0, 2.0, 0.5, 0.4, 0.0]; out = {}
    rho, ph = fields(xb, xcar, a); ab, ac = accel(rho, ph, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * Hnorm(a))
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        xb = (xb + dt * pb / a ** 2) % LBOX; xcar = (xcar + dt * pcar / a ** 2) % LBOX
        a = a + da
        rho, ph = fields(xb, xcar, a)
        gate = ((OL / (Om * a ** -3 + OL)) / OL) ** P_G
        if g0U > 0 and cold.any():                                     # mode U: uniform, rate Gamma_0 [Omega_L/Omega_L0]^2
            idx = np.where(cold)[0]
            pU = 1 - math.exp(-g0U * ((OL / (Om * a ** -3 + OL)) / OL) ** P_U * dt)
            hit = idx[urng.random(len(idx)) < pU]
            if len(hit):
                nh = urng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                pcar[hit] += a * (V_U / 100.0) * nh
                cold[hit] = False; nU += len(hit)
        if gamma > 0 and cold.any():                                   # mode G: L377's trigger, gated by the vacuum
            xt = 1.5 * Om_a(a) * (rho - 1.0)
            if mode in ("full", "trigger") and ph[1] is not None:
                xt = xt + 1.5 * Om_a(a) * ph[1]
            idx = np.where(cold)[0]
            xp = s.interp(xt, xcar[idx])
            hit = idx[(xp * gate > xc) & (krng.random(len(idx)) < 1 - math.exp(-gamma * Hnorm(a) * dt))]
            if len(hit):
                nh = krng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                pcar[hit] += a * (vg / 100.0) * nh
                cold[hit] = False
        ab, ac = accel(rho, ph, a)
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                rec = {"decayed": float(1 - cold.mean()), "decayed_U": nU / n, "switched": ph[2]}
                if z >= 2.0:
                    kpar, p1d = s.flux_p1d(xb, pb, a, z)
                    rec.update(kpar=kpar.tolist(), p1d=p1d.tolist())
                    rhoc2 = s.deposit(xcar, np.full(n, 1.0)) * NG ** 3 / n
                    dense = rho > 50.0
                    rec["carrier_in_dense"] = float(rhoc2[dense].sum() / max(rho[dense].sum(), 1e-30))
                    if z == 2.0:                                           # L379's fixed-cell clearing needs the fields
                        np.save(os.path.join(tmp, f"{name}_z2.0_rho.npy"), rho.astype(np.float32))
                        np.save(os.path.join(tmp, f"{name}_z2.0_rhoc.npy"), rhoc2.astype(np.float32))
                elif z == 0.5:
                    rec["pk"] = L7.pk_bins(s, rho - 1.0)
                else:
                    if z == 0.0:
                        rec["sigma8"] = L6.sigma8(s, rho - 1.0)
                    rhoc = s.deposit(xcar, np.full(n, WC)) * NG ** 3 / n
                    np.save(os.path.join(tmp, f"{name}_z{z}_rho.npy"), rho.astype(np.float32))
                    np.save(os.path.join(tmp, f"{name}_z{z}_rhoc.npy"), rhoc.astype(np.float32))
                out[str(z)] = rec; zs.remove(z)
    out["sw_diag"] = dict(SWDIAG)
    return name, out


# ================================================================================================ Harvey (L371's machinery)
def harvey_block(EPSM, VKG):
    """L371's machinery, loaded unedited (its functions), with the group retention measured here and the S2 kick = v_G.
    EPSM = {1e14: eps, 3e14: eps, 1e15: eps}.  Returns the population-mean excess beta for shapes S1 and S2."""
    s71 = open(os.path.join(HERE, "L371_harvey_slow_kick_carrier.py")).read()
    s70 = open(os.path.join(HERE, "L370_boosted_infall_mergers.py")).read()
    head70 = s70.split("# ============================================================================================================ C1")[0]
    head70 = head70.replace('P(__doc__.split("CHECKS")[0].strip())', "pass")
    mut, os.environ["MUTATE"] = os.environ.get("MUTATE", "0"), "0"
    G = {"__name__": "l371", "__file__": os.path.join(HERE, "L371_harvey_slow_kick_carrier.py")}
    exec(head70, G); G["MUTATE"] = False
    # the mesh runs' cell (p = 1, x_c0 = 2.5) with L370's absolute mask -- L397's Harvey operator for M* (not L370's default cell)
    G["SWITCH"][SW_KEY] = (P_SW, X_SW)                               # the linear gate (L370's file untouched)
    G["SW_DEF"] = SW_KEY
    os.environ["MUTATE"] = mut
    G.update(dict(RealHalo=G["RealHalo"], os=os, json=json, math=math, np=np, time=time, REPO=REPO, HERE=HERE))
    from scipy.optimize import brentq
    from scipy.interpolate import PchipInterpolator
    G.update(brentq=brentq, PchipInterpolator=PchipInterpolator)
    ZH, NH, LH = 0.4, (120 if SMOKE else 400), 10000.0
    GH = G["Grid"](NH, LH); DXH = GH.dx
    G.update(ZH=ZH, NH=NH, LH=LH, GH=GH, DXH=DXH, XSUB=400.0, HARV_BETA=-0.04, HARV_ERR=0.07, FGAS_S=0.10, FSTAR_S=0.02,
             RN=1000.0 / G["h"] / (1 + ZH), VK=VKG, EPS={"med": EPSM})
    exec(s70[s70.index("def centroid(S, x0, y0, Rap, it=12):"):s70.index("HB = []")], G)          # L370's Harvey helpers
    exec(s71[s71.index("def q_static(args):"):s71.index("# ================================================================================================ S2's shape")], G)
    GATES = np.array([25.0, 50.0, 100.0, 150.0, 250.0, 400.0, 700.0, G["RN"]])
    QTAB = {}
    for Ml in (1e14, 3e14, 1e15):
        fg, fs = (0.10, 0.02) if Ml < 1e15 else (0.125, 0.015)
        H0 = G["RealHalo"](Ml, ZH, fg, fs, "intact")
        QTAB[Ml] = (GATES, np.array(G["q_static"]((H0.M200, H0.c, G["cum_mass"](H0.rho_b), GATES))))
    paint_at, centroid, nfw_fit_centre, phantom_felt, m_in = (G[k] for k in ("paint_at", "centroid", "nfw_fit_centre", "phantom_felt", "m_in"))
    A0K, SW_DEF = G["A0K"], G["SW_DEF"]
    sys.path.insert(0, HERE)
    a0H = A0K["canonical"]

    def solve_b(M200L, shape, eps, qtab, fgas, fstar, kernel=True):
        """L371's solve_l366 at the mesh's cell, L370's absolute mask (as L373 and L397)."""
        return G["solve_l366"](M200L, shape, eps, qtab, fgas, fstar, kernel=kernel)
    CONF = [(Msub, dSG, orient) for Msub in (1e14, 3e14) for dSG in (60.0, 120.0) for orient in ("perp", "toward_main")]
    # line-of-sight projection depths: the full box (gated, as pre-declared) and two caps -- XR5's edge-layer check
    # (the far edge layer of a switched region, projected, can move a centroid; reported, not gated)
    CAPS = (("full", None), ("3Mpc", 3000.0), ("1.5Mpc", 1500.0))
    kz = NH // 2

    def proj(a3, cap):
        if cap is None:
            return a3.sum(axis=2) * DXH
        n_ = int(round(cap / DXH))
        return a3[:, :, kz - n_:kz + n_].sum(axis=2) * DXH

    def offsets(S, ux, uy):
        o = {}
        for Rap in (100.0, 150.0):
            cx, cy = centroid(S, 400.0, 0.0, Rap); o[f"{Rap:.0f}"] = (cx - 400.0) * ux + cy * uy
        fx, fy = nfw_fit_centre(S, 400.0, 0.0); o["fit"] = (fx - 400.0) * ux + fy * uy
        return o
    RES = {}
    for (Msub, dSG, orient) in CONF:
        gx, gy = (400.0, dSG) if orient == "perp" else (400.0 - dSG, 0.0)
        ux, uy = ((0.0, 1.0) if orient == "perp" else (-1.0, 0.0))
        HsL = solve_b(Msub, "intact", 1.0, None, 0.10, 0.02, kernel=False)
        A3 = (paint_at(HsL.rho_c + HsL.rho_s, 400.0, 0.0, m_in(HsL.rho_c + HsL.rho_s, 1e9))
              + paint_at(HsL.rho_g, gx, gy, m_in(HsL.rho_g, 1e9)))
        RES[(Msub, dSG, orient)] = dict(gx=gx, gy=gy, ux=ux, uy=uy, dSG=dSG, L={c_: offsets(proj(A3, cap), ux, uy) for c_, cap in CAPS})
        del A3
    ic0 = NH // 2; icx = int(round((400.0 + LH / 2) / DXH))
    OUTB = {}
    for shape in ("intact", "S1", "S2"):                           # intact: the matched control (the kernel's own shift)
        Hm = solve_b(1e15, shape, EPSM[1e15], QTAB[1e15], 0.125, 0.015)
        bm = paint_at(Hm.rho_b, 0.0, 0.0, m_in(Hm.rho_b, 1e9)); cm = paint_at(Hm.rho_c, 0.0, 0.0, m_in(Hm.rho_c, 1e9))
        rph = phantom_felt(GH, bm, bm + cm, ZH, a0H, SW_DEF, [(ic0, ic0, ic0)])[2]
        A3 = bm + cm + rph
        SMAIN = {c_: proj(A3, cap) for c_, cap in CAPS}
        del A3, rph
        beta = {c_: {e: [] for e in ("100", "150", "fit")} for c_, _ in CAPS}; core = {}
        for Msub in (1e14, 3e14):
            Hs = solve_b(Msub, shape, EPSM[Msub], QTAB[Msub], 0.10, 0.02)
            core[Msub] = m_in(Hs.rho_c, 150.0) / m_in(Hs.rho_b, 150.0)
            ss = paint_at(Hs.rho_s, 400.0, 0.0, m_in(Hs.rho_s, 1e9)); cs = paint_at(Hs.rho_c, 400.0, 0.0, m_in(Hs.rho_c, 1e9))
            for (Ms_, dSG, orient) in CONF:
                if Ms_ != Msub:
                    continue
                r_ = RES[(Msub, dSG, orient)]
                gs = paint_at(Hs.rho_g, r_["gx"], r_["gy"], m_in(Hs.rho_g, 1e9))
                rb = bm + ss + gs; rreal = rb + cm + cs
                rph = phantom_felt(GH, rb, rreal, ZH, a0H, SW_DEF, [(ic0, ic0, ic0), (icx, ic0, ic0)])[2]
                A3 = rreal + rph
                for c_, cap in CAPS:
                    o = offsets(proj(A3, cap) - SMAIN[c_], r_["ux"], r_["uy"])
                    for e in ("100", "150", "fit"):
                        beta[c_][e].append((o[e] - r_["L"][c_][e]) / dSG)
                del gs, rb, rreal, rph, A3
            del ss, cs
        del bm, cm, SMAIN
        bc = {c_: {e: float(np.mean(v)) for e, v in d.items()} for c_, d in beta.items()}
        b = bc["full"]
        OUTB[shape] = dict(beta=b, beta_caps=bc, core=core, ok=all(b[e] <= -0.04 + 2 * 0.07 for e in b), switch=f"{SW_DEF}|L370 absolute mask")
    return OUTB


def harvey_job(args):
    """one cell's Harvey block (a Pool task)."""
    t, EPSM, vg = args
    with contextlib.redirect_stdout(io.StringIO()):
        return t, harvey_block(EPSM, vg)


def load_ms3():
    """MS3's halo-model machinery (L363's resolution-free halo model with MS3's cap and edge conventions), loaded unedited up
    to its scenarios; only MS3's own MUTATE flag (its first occurrence) is held False.  (L395 loads it the same way.)"""
    p3 = os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector.py")
    src = open(p3).read()
    flag = 'MUTATE = os.environ.get("MUTATE", "0") == "1"'
    assert src.index(flag) < src.index(".replace(" + repr(flag)[0] + flag), "MS3's own flag must come first"
    src = src.replace(flag, "MUTATE = False", 1).split("cut = lambda Mc")[0]
    ns = {"__name__": "ms3_in_l393", "__file__": p3}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, "MS3(L393)", "exec"), ns)
    return ns


def retention_fn(anchor, mh, ee):
    """MS3's construction of the carrier's retention by halo mass: galaxies (1e13) at `anchor`, then the pooled medians of
    the retention `ee` in L371's bins at MS3's centres (log-linear between, flat outside)."""
    lx, ly = [math.log10(1e13)], [float(anchor)]
    for _, b0, b1, cen in MBINS:
        m_ = (mh >= b0) & (mh < b1)
        if m_.any():
            lx.append(math.log10(cen)); ly.append(float(np.median(ee[m_])))
    return (lambda M: float(np.interp(math.log10(M), lx, ly, left=ly[0], right=ly[-1]))), dict(zip([f"{10 ** x:.2e}" for x in lx], ly))


def c5_curvature():
    """C5 (L396's): the mesh mean curvature of a spherical blob's potential is 1/r (a = 1, comoving = physical)."""
    Lb, Nb = 40.0, 128
    s = L2.Sim(Lb, Nb, 8)
    g = (np.arange(Nb) + 0.5) * s.d - Lb / 2
    X, Y, Z = np.meshgrid(g, g, g, indexing='ij'); R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    blob = np.exp(-0.5 * (R / 0.3) ** 2); blob = blob / blob.mean() - 1.0
    kap, _ = kappa_mesh(s.poisson(blob), s.d)
    out = []
    for rq in (1.0, 2.0, 3.0):
        vals = []
        for ax in range(3):
            for sgn in (1, -1):
                idx = [Nb // 2] * 3; idx[ax] = Nb // 2 + sgn * int(round(rq / s.d)) - (1 if sgn < 0 else 0)
                i = tuple(idx); vals.append(kap[i] * R[i])
        out.append(dict(r=rq, kappa_times_r=float(np.mean(vals))))
    return out


def c6_same_switch():
    """C6: this lane's msck switch against L396's own function on a lognormal test field at z = 2 and z = 0.4."""
    import subprocess, importlib
    p96 = os.path.join(DS, "L396_msc_cell_575.py")
    rec = dict(path=os.path.relpath(p96, REPO))
    if not os.path.exists(p96):
        return False, dict(rec, error="L396 not found")
    git = lambda *a_: subprocess.run(["git", "-C", REPO] + list(a_), capture_output=True, text=True).stdout.strip()
    rec.update(commit=git("log", "-1", "--format=%h", "--", p96) or "uncommitted",
               modified_since_commit=bool(git("status", "--porcelain", "--", p96)))
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            importlib.import_module("L396_msc_cell_575")            # sets up L395's cell and execs L396's switch into L377's namespace
        ref = L77.phantom_swk
    except Exception as e:                                          # recorded, not raised: the check fails
        return False, dict(rec, error=f"import failed: {e!r}")
    s = L2.Sim(LBOX, 64, 8)
    rng = np.random.default_rng(20260926)
    kk = np.sqrt(s.K2)
    g = np.real(np.fft.ifftn(np.fft.fftn(rng.normal(size=(64, 64, 64))) * np.exp(-0.5 * (kk * 2.0) ** 2)))
    rho = np.exp(2.0 * g / g.std()); rho /= rho.mean()              # lognormal matter, smoothed on ~2 Mpc/h
    rb = WB * rho * np.exp(0.3 * rng.normal(size=rho.shape)); rb *= WB / rb.mean()
    a0c = L77.A0["canonical"] / L77.ACC_UNIT
    ok, rows = True, {}
    for z in (2.0, 0.4):
        a = 1.0 / (1.0 + z)
        SWDIAG.update(steps=0, capped_max=0.0, switched_max=0.0)
        mine = phantom_msck(s, rb, rho, a, a0c)
        theirs = ref(s, rb, rho, a, a0c, "msck")
        same = (mine[0] is None) == (theirs[0] is None) and mine[2] == theirs[2]
        dmax = 0.0
        if same and mine[0] is not None:
            dmax = max(float(np.max(np.abs(mine[0] - theirs[0]))), float(np.max(np.abs(mine[1] - theirs[1]))))
            same = dmax == 0.0
        ok = ok and same
        rows[str(z)] = dict(switched=mine[2], capped_frac=SWDIAG["capped_max"], max_abs_diff=dmax, identical=bool(same))
    informative = any(r_["switched"] > 0 for r_ in rows.values())
    return bool(ok and informative), dict(rec, epochs=rows, informative=informative)


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: mode U switched off in every decaying run -- X-COP must fail and R1 must flip ***")
    if SMOKE: P("\n  *** L394_SMOKE=1: code test on a 64^3 mesh, one realisation, one cell; nothing is written here ***")
    banner("C5, C6  THE CAP'S CURVATURE OPERATOR AND THE SAME-SWITCH CHECK (before the mesh runs)")
    c5 = c5_curvature()
    check("C5 CONTROL: this lane's mesh mean curvature of a spherical blob's potential is 1/r to within 5% at r = 1, 2, 3 Mpc/h "
          "(L396's C5)", "; ".join(f"r = {r_['r']:.0f}: kappa r = {r_['kappa_times_r']:.4f}" for r_ in c5),
          all(abs(r_["kappa_times_r"] - 1) < 0.05 for r_ in c5))
    ok6, c6 = c6_same_switch()
    check("C6 SAME SWITCH AS M*: on a lognormal test field at z = 2 and z = 0.4 this lane's switch returns exactly L396's own "
          "msck output (switched fraction, potential, phantom), with switched cells at one epoch at least", f"{c6}", ok6,
          "the run is on L396's switch definition as recorded here (its commit and whether the file had changed)")
    OUT["numbers"].update(C5=c5, C6=c6)
    NPOOL = int(os.environ.get("L394_POOL", "4"))
    CKPT = os.path.join(tempfile.gettempdir(), f"L394_ckpt{'_MUTATE' if MUTATE else ''}{'_SMOKE' if SMOKE else ''}.pkl")
    RESUME = os.environ.get("L394_RESUME", "0") == "1" and os.path.exists(CKPT)
    TMP = tempfile.mkdtemp(prefix="L394_")
    cfgs = []
    for sp, sk in SEEDS:
        cfgs.append((f"s{sp}_lcdm", sp, sk, float("inf"), 0.0, 0.0, 0.0, TMP, "none", L77.A0["canonical"]))
        cfgs += [(f"s{sp}_{t}", sp, sk, L77.XC_TRIG, vg, 10.0, 0.0 if MUTATE else fu, TMP, "full", L77.A0["canonical"])
                 for t, (fu, vg) in zip(TAGS, CELLS)]
    P(f"\n  {len(cfgs)} runs, pool {NPOOL}; mode U: Gamma_0 = " + ", ".join(f"{gamma0_U(fu):.3f} H0 (f_U(0) = {fu:.2f})"
                                                                         for fu in sorted({c[0] for c in CELLS})))
    if RESUME:                                                     # the mesh runs are the slow part: resume after them
        import pickle
        res, M, GRP = (lambda d: (d["res"], d["M"], d["GRP"]))(pickle.load(open(CKPT, "rb")))
        P(f"  RESUMED from {CKPT} (the mesh runs and their measurements, unchanged)")
    else:
        with Pool(NPOOL) as pool:
            res = dict(pool.map(run2, cfgs, chunksize=1))
        P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")

    # ------------------------------------------------------------------------------------------ C1
    banner("C1  CONTROL")
    s66 = json.load(open(os.path.join(DS, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["runs"]["lcdm"]["0.0"]["sigma8"]
    d1 = abs(res["s7_lcdm"]["0.0"]["sigma8"] / s66 - 1)
    check("C1 CONTROL: the (7, 11) LCDM run reproduces L366's committed LCDM sigma_8 (same code path, same seeds)",
          f"relative deviation {d1:.1e}", d1 < 1e-9)

    # ------------------------------------------------------------------------------------------ C4: MS3's halo model
    banner("C4  CONTROL: MS3's halo model, loaded here")
    M3 = load_ms3()
    R_of, XLIN, A0M = M3["R_of"], M3["XLIN"], M3["A0"]
    assert abs(XLIN - X_SW * M3["E2"] ** P_SW) < 1e-12, (XLIN, M3["E2"])      # MS3's lens-epoch threshold is this cell's
    M3R = json.load(open(os.path.join(REPO, "real_research", "mond_sector_gate_2026",
                                      "MS3_cosmic_shear_bound_mond_sector_results.json")))["numbers"]
    c4 = []
    for f_ in ("canonical", "alt"):
        c4.append(abs(max(R_of(XLIN, A0M[f_], 1.75, "door", M3["ret_L388"])[0].values()) - M3R["K1"]["1.75"][f_]["worst"]))
        for cv in ("door", "upper"):
            c4.append(abs(max(R_of(XLIN, A0M[f_], math.inf, cv, M3["ret_L388"])[0].values())
                          - M3R["X1"][f"{cv}/L388 retention/{f_}"]["worst"]))
    check("C4 CONTROL: MS3's halo model, loaded here, reproduces MS3's committed K1 (1.75 Mpc cap, door) and X1 (uncapped, "
          "door and upper) with L388's retention, both footings", f"max |diff| {max(c4):.1e} over {len(c4)} numbers", max(c4) < 1e-9)

    # ------------------------------------------------------------------------------------------ measurements
    est = L6.eps_bounds(); lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())
    s = L2.Sim(LBOX, NG, NP)
    ld = lambda nm, z, f: np.load(os.path.join(TMP, f"{nm}_z{z}_{f}.npy")).astype(float)
    if not RESUME:
        M, GRP = {}, {}
        for sp, _ in SEEDS:
            Lr = f"s{sp}_lcdm"
            M[sp], GRP[sp] = {}, {}
            dl = ld(Lr, 2.0, "rho") > 50.0                                 # LCDM's dense cells at z = 2: L379's fixed cells
            fix_l = float(ld(Lr, 2.0, "rhoc")[dl].sum())
            for z in (0.0, 0.4):
                rho_l, rc_l = ld(Lr, z, "rho"), ld(Lr, z, "rhoc")
                pk = L6.peaks(s, rho_l) if z == 0.0 else L6.peaks(s, rho_l, npk=60)   # z = 0 exactly as L378
                Mh = np.array([L6.sphere_sum(s, rho_l, p_, 1.0) * RHO_M for p_ in pk])
                Mc_l = np.array([L6.sphere_sum(s, rc_l, p_, 1.0) for p_ in pk])
                for t in TAGS:
                    eps = np.array([L6.sphere_sum(s, ld(f"s{sp}_{t}", z, "rhoc"), p_, 1.0) for p_ in pk]) / Mc_l
                    if z == 0.0:
                        r_ = res[f"s{sp}_{t}"]
                        M[sp][t] = dict(s8=r_["0.0"]["sigma8"] / res[Lr]["0.0"]["sigma8"],
                                        p1d={zz: (np.array(r_[zz]["p1d"]), np.array(res[Lr][zz]["p1d"]), np.array(res[Lr][zz]["kpar"])) for zz in ("3.0", "2.0")},
                                        cid=(r_["2.0"]["carrier_in_dense"], res[Lr]["2.0"]["carrier_in_dense"]),
                                        fix=(float(ld(f"s{sp}_{t}", 2.0, "rhoc")[dl].sum()), fix_l),
                                        pk=({qq: r_["0.5"]["pk"][qq] for qq in KG}, {qq: res[Lr]["0.5"]["pk"][qq] for qq in KG}),
                                        eps_sel=eps[Mh >= 1e14], eps0=eps, Mh0=Mh, swd=r_.get("sw_diag"),
                                        decU=r_["0.0"]["decayed_U"], dec=r_["0.0"]["decayed"],
                                        dec_z04=(r_["0.4"]["decayed_U"], r_["0.4"]["decayed"]))
                    else:
                        GRP[sp][t] = dict(M=Mh, eps=eps)
        shutil.rmtree(TMP, ignore_errors=True)
        import pickle
        pickle.dump(dict(res=res, M=M, GRP=GRP), open(CKPT, "wb"))
        P(f"  checkpoint written: {CKPT}")
    else:
        shutil.rmtree(TMP, ignore_errors=True)

    def gates(rows):                                             # L378's gate arithmetic, plus L379's fixed-cell clearing
        s8 = float(np.mean([r["s8"] for r in rows])); fdev = 0.0
        for z in ("3.0", "2.0"):
            px = sum(r["p1d"][z][0] for r in rows); pl = sum(r["p1d"][z][1] for r in rows); kp = rows[0]["p1d"][z][2]
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(px[m] / pl[m] - 1))))
        g3 = sum(r["cid"][0] for r in rows) / max(sum(r["cid"][1] for r in rows), 1e-30)
        g3f = sum(r["fix"][0] for r in rows) / max(sum(r["fix"][1] for r in rows), 1e-30)
        eps = np.concatenate([r["eps_sel"] for r in rows]); med = float(np.median(eps)) if len(eps) else float("nan")
        T = {qq: math.sqrt(sum(r["pk"][0][qq] for r in rows) / sum(r["pk"][1][qq] for r in rows)) for qq in KG}
        return dict(S8=s8, forest=fdev, G3=g3, G3_fixed=g3f, eps_cl=med, n_cl=int(len(eps)), T_box=T,
                    s8_ok=s8 >= 0.899, s8_strict=s8 >= 0.922, forest_ok=fdev <= 0.10, xcop_ok=bool(lo <= med <= hi))

    banner("GATES: per realisation and pooled (X-COP two-sided %.3f-%.3f; S8 >= 0.922 strict / 0.899 alt; forest <= 0.10)" % (lo, hi))
    TAB = {}
    for key, rows_of in [(str(sp), lambda t, sp=sp: [M[sp][t]]) for sp, _ in SEEDS] + [("pooled", lambda t: [M[sp][t] for sp, _ in SEEDS])]:
        TAB[key] = {}
        for t in TAGS:
            g = gates(rows_of(t)); TAB[key][t] = g
            P(f"    {key:>6s} {t:10s}: S8 {g['S8']:.3f}{'' if g['s8_ok'] else ' X'} | forest {g['forest']:.3f}{'' if g['forest_ok'] else ' X'} | "
              f"X-COP eps {g['eps_cl']:.3f}{'' if g['xcop_ok'] else (' UNDER' if g['eps_cl'] < lo else ' OVER')} (n={g['n_cl']}) | "
              f"box T(k = {max(KG):g}) {g['T_box'][max(KG)]:.3f} (reported) | z = 2 clearing (reported) own-set {g['G3']:.2f}, "
              f"fixed cells {g['G3_fixed']:.2f}")
    for t in TAGS:
        P(f"    switch ({t}; max over steps, per box): switched " + ", ".join(f"{M[sp][t]['swd']['switched_max']:.4f}" for sp, _ in SEEDS)
          + "; capped (of the uncapped switch) " + ", ".join(f"{M[sp][t]['swd']['capped_max']:.3f}" for sp, _ in SEEDS))
        P(f"    decayed by z = 0 ({t}): " + ", ".join(f"box {sp}: U {M[sp][t]['decU']:.3f} / all {M[sp][t]['dec']:.3f}" for sp, _ in SEEDS))
    GR = {}                                                        # group retention at z = 0.4, pooled
    for t in TAGS:
        Ms = np.concatenate([GRP[sp][t]["M"] for sp, _ in SEEDS]); Es = np.concatenate([GRP[sp][t]["eps"] for sp, _ in SEEDS])
        b1 = (Ms >= 5e13) & (Ms < 1e14); b3 = (Ms >= 1.5e14) & (Ms < 3e14); bm = Ms >= 3e14
        GR[t] = {1e14: float(np.median(Es[b1])) if b1.any() else float("nan"), 3e14: float(np.median(Es[b3])) if b3.any() else float("nan"),
                 1e15: float(np.median(Es[bm])) if bm.any() else float("nan"), "n": (int(b1.sum()), int(b3.sum()), int(bm.sum()))}
        P(f"    retention inside 1 Mpc/h at z = 0.4 ({t}): 5e13-1e14 {GR[t][1e14]:.2f} (n={GR[t]['n'][0]}), 1.5e14-3e14 "
          f"{GR[t][3e14]:.2f} (n={GR[t]['n'][1]}), >= 3e14 {GR[t][1e15]:.2f} (n={GR[t]['n'][2]})")

    # ------------------------------------------------------------------------------------------ cosmic shear (halo model)
    banner("COSMIC SHEAR on MS3's resolution-free halo model at the cell's convention (door) and cap (1.75 Mpc at z = 0.5): "
           "worst R(k = 0.1-1) <= 1.2 on both footings (canonical/alt); the gate is the first variant")
    SH = {}
    for t in TAGS:
        anchor = TAB["pooled"][t]["G3_fixed"]                          # MS3's galaxy anchor: the z = 2 fixed-cell clearing
        m4 = np.concatenate([GRP[sp][t]["M"] for sp, _ in SEEDS]); e4 = np.concatenate([GRP[sp][t]["eps"] for sp, _ in SEEDS])
        m0 = np.concatenate([M[sp][t]["Mh0"] for sp, _ in SEEDS]); e0 = np.concatenate([M[sp][t]["eps0"] for sp, _ in SEEDS])
        r04, tab04 = retention_fn(anchor, m4, e4)
        r0, tab0 = retention_fn(anchor, m0, e0)
        bins04 = list(tab04.values())[1:]
        rfl, tabfl = retention_fn(bins04[0] if bins04 else anchor, m4, e4)
        var = {"gate (z = 0.4, door, 1.75 Mpc)": (r04, tab04, 1.75),
               "uncapped (z = 0.4, door)": (r04, tab04, math.inf),
               "L396's construction (z = 0, door, 1.75 Mpc)": (r0, tab0, 1.75),
               "flat galaxy anchor (z = 0.4, door, 1.75 Mpc)": (rfl, tabfl, 1.75)}
        SH[t] = {}
        for nm, (rf, tb, rc_) in var.items():
            w = {f_: max(R_of(XLIN, A0M[f_], rc_, "door", rf)[0].values()) for f_ in ("canonical", "alt")}
            SH[t][nm] = dict(worst=w, ok=all(v <= 1.2 for v in w.values()), retention=tb)
        g0 = SH[t]["gate (z = 0.4, door, 1.75 Mpc)"]
        TAB["pooled"][t]["shear_hm"], TAB["pooled"][t]["shear_hm_worst"] = g0["ok"], g0["worst"]
        P(f"    {t}: " + "; ".join(f"{nm} {v['worst']['canonical']:.2f}/{v['worst']['alt']:.2f}{'' if v['ok'] else ' X'}"
                                    for nm, v in SH[t].items()))
        P(f"      retention by halo mass used by the gate: " + ", ".join(f"{k}: {v:.2f}" for k, v in tab04.items()))
    P(f"    [{time.time() - T0:.0f}s]")

    # ------------------------------------------------------------------------------------------ Harvey
    PREV_JSON = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
    PREV = json.load(open(PREV_JSON))["numbers"].get("harvey", {}) if (os.path.exists(PREV_JSON) and not SMOKE) else {}
    banner("HARVEY (L371's machinery) on every pooled cell passing X-COP, with the retention measured at z = 0.4")
    todo = []
    for (fu, vg), t in zip(CELLS, TAGS):
        if TAB["pooled"][t]["xcop_ok"] or SMOKE:
            fb = next((GR[t][k] for k in (3e14, 1e14, 1e15) if np.isfinite(GR[t][k])), 1.0)
            todo.append((t, {k: (GR[t][k] if np.isfinite(GR[t][k]) else fb) for k in (1e14, 3e14, 1e15)}, vg))
    HV = {}
    if todo:
        with Pool(min(int(os.environ.get("L394_HPOOL", "2")), len(todo))) as pool:   # 400^3 QUMOND grids: memory-bound
            HV = dict(pool.map(harvey_job, todo, chunksize=1))
    for t, EPSM, vg in todo:
        P(f"    {t}: retention used {EPSM[1e14]:.2f}/{EPSM[3e14]:.2f}/{EPSM[1e15]:.2f}; excess beta (100/150/fit) intact "
          + "/".join(f"{HV[t]['intact']['beta'][e]:+.3f}" for e in ("100", "150", "fit")) + "; S1 "
          + "/".join(f"{HV[t]['S1']['beta'][e]:+.3f}" for e in ("100", "150", "fit")) + "; S2 "
          + "/".join(f"{HV[t]['S2']['beta'][e]:+.3f}" for e in ("100", "150", "fit"))
          + f"; core carrier/baryons(<150 kpc) S1 {HV[t]['S1']['core'][1e14]:.2f}/{HV[t]['S1']['core'][3e14]:.2f}"
          + f" -> {'PASS' if HV[t]['S1']['ok'] and HV[t]['S2']['ok'] else 'FAIL'}")
    for t, EPSM, vg in todo:
        for sh in ("intact", "S1", "S2"):
            P(f"      {t} {sh:6s} edge-layer check, excess beta (100/150/fit) by projection depth: " + "; ".join(
                f"{c_} " + "/".join(f"{HV[t][sh]['beta_caps'][c_][e]:+.3f}" for e in ("100", "150", "fit"))
                for c_ in ("full", "3Mpc", "1.5Mpc")))
    if todo:
        dmax = max(abs(HV[t][sh]["beta_caps"][c_][e] - HV[t][sh]["beta_caps"]["full"][e]) for t in HV for sh in HV[t]
                   for c_ in ("3Mpc", "1.5Mpc") for e in ("100", "150", "fit"))
        s2fit = {t: {c_: HV[t]["S2"]["beta_caps"][c_]["fit"] for c_ in ("full", "3Mpc", "1.5Mpc")} for t in HV}
        check("W2 (reported) XR5's edge-layer check: excess beta with the line-of-sight projection capped at +-3 and +-1.5 Mpc "
              "(the gate stays on the full projection, as pre-declared)", f"max |beta(cap) - beta(full)| {dmax:.3f}; S2 fit by depth {s2fit}",
              True, load_bearing=False)
        OUT["numbers"]["edge_layer_check"] = dict(max_abs_shift=dmax, s2_fit=s2fit)
    if not todo:
        P("    no pooled cell passes X-COP: Harvey not run")
    P(f"    [{time.time() - T0:.0f}s]")

    if PREV and HV:
        diffs = [abs(HV[t][sh]["beta"][e] - PREV[t][sh]["beta"][e]) for t in HV if t in PREV for sh in HV[t] if sh in PREV[t]
                 for e in ("100", "150", "fit")]
        check("C3 CONTROL: the full-projection betas reproduce the previously committed Harvey numbers (the depth caps are "
              "added beside them, not in their place)", f"max |difference| {max(diffs) if diffs else float('nan'):.1e} over "
              f"{len(diffs)} numbers", bool(diffs) and max(diffs) < 1e-9)
    SW_MESH = f"{SW_KEY}|L370 absolute mask"
    used = sorted({HV[t][sh]["switch"] for t in HV for sh in HV[t]})
    check("C2 CONTROL: the Harvey stage runs at the mesh's cell (p = 1, x_c0 = 2.5) with L370's absolute mask (L397's operator)",
          f"mesh {SW_MESH}; Harvey {used or 'not run (no cell passes X-COP)'}", all(u == SW_MESH for u in used))

    # ------------------------------------------------------------------------------------------ verdict
    banner("R1  THE HYPOTHESIS (set before the run)")
    ok_all = lambda t: (TAB["pooled"][t]["s8_ok"] and TAB["pooled"][t]["forest_ok"] and TAB["pooled"][t]["xcop_ok"]
                        and TAB["pooled"][t]["shear_hm"] and t in HV and HV[t]["S1"]["ok"] and HV[t]["S2"]["ok"])
    WIN = [t for t in TAGS if ok_all(t)]
    WIN_strict = [t for t in WIN if TAB["pooled"][t]["s8_strict"]]
    FAILS = {t: [nm for nm, bad in (("S8", not TAB["pooled"][t]["s8_ok"]), ("forest", not TAB["pooled"][t]["forest_ok"]),
                                    ("X-COP", not TAB["pooled"][t]["xcop_ok"]), ("shear", not TAB["pooled"][t]["shear_hm"]),
                                    ("Harvey", t in HV and not (HV[t]["S1"]["ok"] and HV[t]["S2"]["ok"]))) if bad] for t in TAGS}
    for t in TAGS:
        P(f"    pooled {t}: {'PASSES EVERY GATE' if t in WIN else 'fails ' + ', '.join(FAILS[t])}")
    check("R1 = H: on M*'s switch and cap the two-mode carrier has a window -- a pooled cell passes S_8 (alt), forest, X-COP, "
          "shear (MS3's halo model, capped) and Harvey (both core shapes)", f"window {WIN or 'none'} (with strict S_8: {WIN_strict or 'none'})",
          bool(WIN) == EXPECT_WINDOW)
    check("W (reported) the gate tables, group and cluster retention, and the z = 2 clearing (not gated: the vacuum gate "
          "keeps high-z halos by design)", "see above", True, load_bearing=False)
    E04 = (Om * 1.4 ** 3 + OL)
    OUT["numbers"]["model"] = dict(
        switch=dict(p=P_SW, x_c0=X_SW, x_c_eff_z04=X_SW * E04 ** P_SW, branch=BRANCH, harvey_key=SW_MESH),
        mesh_operator="L377 phantom()'s operator (Newtonian field of ALL baryons, constitutive response masked) with M*'s switch "
                      "(L396's msck, verbatim): U = smooth-min_4(1.5 Omega_m(a)(rho_b + max(delta_ph,all, 0)), v_cap^2 kappa_X^2/H^2) "
                      "[Omega_L(a)/Omega_L0] > x_c0, kappa_X = (1/2) div(grad Phi_X/|grad Phi_X|), Phi_X = the baryons' Newtonian + the "
                      "untruncated phantom potential, v_cap = 325 km/s, p = 1, x_c0 = 2.5, sharp (w = 0)",
        action_status="MS1/MS5: the MOND-sector reading with the kappa-form cap is leak-free as an action term; the carrier's "
                      "trigger and kicks are posited",
        harvey_operator="L370/L361 region operator (each region's phantom from its own baryons, sigma = 0) at the cell p1_x2.5 with "
                        "L370's absolute-density mask -- L397's Harvey operator for M*",
        kernel="nu_mono (L352)", a0_footing="canonical", carrier="Newtonian only (L353)",
        retention_epochs=dict(xcop="z = 0, inside 1 Mpc/h of LCDM's peaks", harvey="z = 0.4, pooled medians by mass bin"),
        harvey_shapes=["intact (matched control)", "S1 (scaled cusp)", "S2 (phase-mixed daughters at v_G)"],
        shear_gate="MS3's resolution-free halo model (L363), door convention, r_cap = 1.75 Mpc at z = 0.5 (MS5's kappa-form cap on "
                   "spherical profiles; L396's score), worst R(k = 0.1-1) <= 1.2 on both footings, the cell's own pooled retention: "
                   "z = 0.4 medians in L371's bins at MS3's centres, galaxies (1e13) at the z = 2 fixed-cell clearing",
        scope="a labelled carrier variant of M* (L372's two modes in place of L388's single kick), never pooled with M*'s cell "
              "(L396); sharp gate; the G trigger is the mesh proxy; sigma = 0 Harvey operator (XR5 H1: sigma = 1 agrees to "
              "|delta beta| <= 0.002, toward-main)")
    OUT["numbers"].update(table=TAB, shear_halo_model=SH, groups_z04={t: {str(k): v for k, v in d.items()} for t, d in GR.items()},
                          harvey={t: {sh: dict(beta=v["beta"], ok=v["ok"], core={str(k): c for k, c in v["core"].items()})
                                      for sh, v in d.items()} for t, d in HV.items()},
                          window=WIN, window_strict_S8=WIN_strict, fails=FAILS, eps_bounds=dict(lo=lo, hi=hi),
                          decayed={t: {str(sp): dict(U=M[sp][t]["decU"], total=M[sp][t]["dec"], z04=M[sp][t]["dec_z04"])
                                       for sp, _ in SEEDS} for t in TAGS},
                          cells={t: dict(f_U0=fu, v_G=vg, v_U=V_U) for t, (fu, vg) in zip(TAGS, CELLS)})
    banner("VERDICT")
    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    P(f"  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
    if SMOKE:
        P("  smoke test: no results written")
    else:
        outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
        json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
        P(f"  wrote {outname}")
    P(f"rc={0 if n_fail == 0 else 1}")
    sys.exit(0 if n_fail == 0 else 1)
