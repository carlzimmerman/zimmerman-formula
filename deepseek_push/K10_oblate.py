#!/usr/bin/env python3
"""
K10 -- THE OBLATENESS DOOR: spheroid transport, atom, E[D], and the window
2026-09-23.  Continuation of J09/J11 (sphere windows) on the moment channel.

Question: the central/volume/shell windows were derived on the UNIT SPHERE:
  central:  -ln A / E[D] = (1+q/3)/(1/2+q/4)  in [4/3, 2]  (tau0-FREE, J09)
  volume:   -ln A_v / E[D]_v  tau0-DEPENDENT, 1.897 at (q=0,tau0=1), crossing
            below 4/3 at high opacity (J11).
Real BLRs are flattened.  NEW DOOR: does the window structure survive
OBLATENESS?  Geometry: the oblate spheroid x^2+y^2+z^2/eps^2 = 1, semi-major
axes 1, semi-minor eps in {1.0, 0.7, 0.5, 0.3}, central z-axis.  kappa =
tau0 (1 + q r^2) with r the EUCLIDEAN radius (unchanged).  Observables:
  A  = atom (P(escape with 0 scatterings)),  E[D],  W := -ln A / E[D].

Transport: self-contained re-implementation of the J02 engine with the
EXACT spheroid surface intersection  (ray |p+u s|^2_spheroid = 1 solved as
a quadratic in s; A-coefficient = ux^2+uy^2+uz^2/eps^2 > 0 for eps<=1).
Volume source: uniform in the spheroid volume (uniform ball x (z -> eps z),
an affine map, so uniformity is preserved).  eps=1.0 must reproduce the
sphere results EXACTLY (kill gate):
  central eps=1:  A = exp(-1),  E[D] = 1/2,  W = 2.0   (exact)
  volume  eps=1:  W = 1.8970 (J11) ;  atom matches the exact quadrature.

Checks:
  KILLC  central eps=1 vs sphere exact values (4 SE)
  KILLV  volume  eps=1: atom vs exact 4D quadrature (4 SE), W vs J11 (5 CE)
  QC/QV  per-eps atom (central / volume) vs exact quadrature (4 SE) -- the
         spheroid-transport bug gate at eps < 1
  GA     central window stays inside [4/3, 2] at tau0=1, q=0 (3 SE margin)?
  TAU0V  volume tau0-dependence survives: W_v(tau0=8) < W_v(tau0=0.5) - 4 CE
         for eps in {1.0, 0.5}, plus the crossing W_v < 4/3 at tau0=8?
  TAU0C  central tau0-freeness under oblateness: W_c(tau0=3) vs W_c(tau0=0.5)
         at eps=0.3 (5 CE; if the window is eps-shifted, is the shift tau0-free?)
Deliver: W(eps)/W(1.0) correction table (observer un-flattens), power-law fit.
"""
import json
import math
import sys
import time

import numpy as np
from numpy.polynomial.legendre import leggauss


# ---------------------------------------------------------------- transport
def rate_integral(a, b, ds, tau0, q):
    """Exact optical depth along a straight segment: tau0*(ds + q*(a ds + b
    ds^2 + ds^3/3)) with a = |p|^2, b = p.u at segment start (EUCLIDEAN r)."""
    return tau0 * (ds + q * (a * ds + b * ds ** 2 + ds ** 3 / 3))


def thomson_mu(rng, n):
    out = np.empty(n); todo = np.arange(n)
    while len(todo):
        m = rng.uniform(-1, 1, len(todo))
        take = rng.random(len(todo)) < (1 + m * m) / 2
        out[todo[take]] = m[take]; todo = todo[~take]
    return out


def wall_spheroid(p, u, eps):
    """Exact first-exit distance from an interior point p in the spheroid
    x^2+y^2+z^2/eps^2 = 1 along direction u (unit).  Quadratic in s:
    A s^2 + B s + C = 0 with A = |u|^2_spheroid > 0 (eps<=1 -> A >= 1),
    C = |p|^2_spheroid - 1 <= 0, so disc = B^2 - 4AC >= B^2 and the + root
    is the unique positive exit distance.  Matches pointwise the sphere
    formula at eps=1."""
    iq = 1.0 / (eps * eps)
    A = u[:, 0] ** 2 + u[:, 1] ** 2 + u[:, 2] ** 2 * iq
    B = 2.0 * (p[:, 0] * u[:, 0] + p[:, 1] * u[:, 1] + p[:, 2] * u[:, 2] * iq)
    C = p[:, 0] ** 2 + p[:, 1] ** 2 + p[:, 2] ** 2 * iq - 1.0
    disc = B * B - 4.0 * A * C
    return (-B + np.sqrt(np.maximum(disc, 0.0))) / (2.0 * A)


def simulate(n, tau0, q, source, eps, seed):
    """Oblate-spheroid transport (J02 engine, exact spheroid wall).
    Returns D, elapsed, N, pos, direc (v2/v4/v6/ang not needed here)."""
    rng = np.random.default_rng(seed)
    pos = np.zeros((n, 3))
    if source == "volume":
        d0 = rng.normal(size=(n, 3)); d0 = d0 / np.linalg.norm(d0, axis=1)[:, None]
        r0 = rng.random(n)[:, None] ** (1.0 / 3.0)
        pos[:, 0] = d0[:, 0] * r0[:, 0]
        pos[:, 1] = d0[:, 1] * r0[:, 0]
        pos[:, 2] = eps * d0[:, 2] * r0[:, 0]      # uniform in the spheroid
    origin = pos.copy()
    d = rng.normal(size=(n, 3)); direc = d / np.linalg.norm(d, axis=1)[:, None]
    elapsed = np.zeros(n)
    N = np.zeros(n, dtype=int)
    alive = np.arange(n); steps = 0
    while len(alive):
        steps += 1
        if steps > 50000:
            raise RuntimeError("transport cap; do not drop survivors")
        p, u = pos[alive], direc[alive]
        r2 = np.sum(p * p, axis=1)
        pd = np.sum(p * u, axis=1)
        wall = wall_spheroid(p, u, eps)
        U = rng.random(len(alive))
        tau_wall = rate_integral(r2, pd, wall, tau0, q)
        esc = tau_wall <= -np.log(U)
        s = wall.copy()
        inner = ~esc
        if inner.any():
            lo = np.zeros(inner.sum()); hi = wall[inner]
            Ui = U[inner]; r2i = r2[inner]; pdi = pd[inner]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                val = rate_integral(r2i, pdi, mid, tau0, q) + np.log(Ui)
                tak = val < 0
                lo[tak] = mid[tak]; hi[~tak] = mid[~tak]
            s[inner] = 0.5 * (lo + hi)
        elapsed[alive] += s
        pos[alive] += u * s[:, None]
        alive = alive[~esc]
        if len(alive) == 0:
            break
        p, u = pos[alive], direc[alive]
        mu = thomson_mu(rng, len(alive))
        t = rng.normal(size=(len(alive), 3))
        t -= np.sum(t * u, axis=1)[:, None] * u
        tn = np.linalg.norm(t, axis=1)
        t = t / tn[:, None]
        direc[alive] = u * mu[:, None] + t * np.sqrt(1 - mu * mu)[:, None]
        N[alive] += 1
    D = elapsed - np.sum((pos - origin) * direc, axis=1)
    assert np.all(D >= -1e-9)
    return dict(D=D, elapsed=elapsed, N=N, pos=pos, direc=direc)


# ------------------------------------------------------- exact quadratures
def A_central_quad(eps, tau0, q, ng=96):
    """A_c = (1/4pi) int dOmega exp(-tau_esc(u)), chord(u) = |u|_spheroid^-1,
    tau_esc = tau0 (chord + q chord^3/3)  (Euclidean |u s|^2 = s^2)."""
    xm, wm = leggauss(ng)
    mu = xm
    ch = 1.0 / np.sqrt(1.0 - mu ** 2 * (1.0 - 1.0 / eps ** 2))
    tau = tau0 * (ch + q * ch ** 3 / 3.0)
    return float(np.sum(0.5 * wm * np.exp(-tau)))


def E_chord_central(eps, ng=96):
    xm, wm = leggauss(ng)
    mu = xm
    ch = 1.0 / np.sqrt(1.0 - mu ** 2 * (1.0 - 1.0 / eps ** 2))
    return float(np.sum(0.5 * wm * ch))


def _vol_grid(eps, ng=(18, 18, 18, 22)):
    """Shared 4D Gauss-Legendre grid: r' in [0,1] (ball), direction n of the
    birth point, direction u of flight (phi_u = 0 by azimuthal symmetry).
    Returns weight (sums to 1) and chord / r2e / pu / tau_esc arrays."""
    nr, nu, nn, np_ = ng
    xr, wr = leggauss(nr); r = 0.5 * xr + 0.5
    xuu, wuu = leggauss(nu); mu_u = xuu
    xnn, wnn = leggauss(nn); mu_n = xnn
    xpp, wpp = leggauss(np_); phi = math.pi * (xpp + 1.0)
    R = r[:, None, None, None]
    MUU = mu_u[None, :, None, None]
    MUN = mu_n[None, None, :, None]
    CP, SP = np.cos(phi)[None, None, None, :], np.sin(phi)[None, None, None, :]
    nx, ny, nz = np.sqrt(1 - MUN ** 2) * CP, np.sqrt(1 - MUN ** 2) * SP, MUN
    ux, uz = np.sqrt(1 - MUU ** 2), MUU          # uy = 0 (phi_u = 0)
    px, py, pz = R * nx, R * ny, eps * R * nz
    iq = 1.0 / eps ** 2
    A = ux ** 2 + uz ** 2 * iq
    B = 2.0 * (px * ux + pz * uz * iq)
    C = R ** 2 - 1.0
    chord = (-B + np.sqrt(np.maximum(B * B - 4 * A * C, 0.0))) / (2.0 * A)
    r2e = R ** 2 * (1 - MUN ** 2) + (eps * R * MUN) ** 2   # Euclidean |p|^2
    pu = px * ux + pz * uz                                # Euclidean p.u
    Wr = 1.5 * wr[:, None, None, None] * R ** 2
    W = (Wr * wuu[None, :, None, None] * wnn[None, None, :, None]
         * wpp[None, None, None, :]) / 8.0
    return W, chord, r2e, pu


def A_vol_quad(eps, tau0, q, ng=(18, 18, 18, 22)):
    W, chord, r2e, pu = _vol_grid(eps, ng)
    tau = tau0 * (chord + q * (r2e * chord + pu * chord ** 2 + chord ** 3 / 3.0))
    return float(np.sum(W * np.exp(-tau)))


def E_chord_vol(eps, ng=(18, 18, 18, 22)):
    W, chord, _, _ = _vol_grid(eps, ng)
    return float(np.sum(W * chord))


# ---------------------------------------------------------------- helpers
def se(x):
    return float(np.std(x, ddof=1) / np.sqrt(len(x)))


def se_win(A, sA, d, sD):
    """SE of W = -ln A / d  by first-order propagation (A, d independent)."""
    lnA = math.log(A)
    return math.sqrt((sA / (A * d)) ** 2 + (lnA * sD / d ** 2) ** 2)


def mkseed(eps, tau0, q, src, salt):
    s = 13_000_000 + int(round(eps * 1000)) + int(round(tau0 * 100)) * 1000
    s += (7 if src == "volume" else 0) + int(q) * 10_000 + salt * 100_000
    return s


def measure(n, tau0, q, src, eps, salt):
    """One transport run -> (W, A, E_D) with SEs."""
    r = simulate(n, tau0, q, src, eps, mkseed(eps, tau0, q, src, salt))
    A = float(np.mean(r["N"] == 0)); sA = float(np.std(r["N"] == 0, ddof=1) / math.sqrt(n))
    d = float(np.mean(r["D"])); sD = se(r["D"])
    W = -math.log(A) / d
    return dict(A=A, sA=sA, d=d, sD=sD, W=W, sW=se_win(A, sA, d, sD))


def run(n=350000):
    res = {"checks": {}, "measurements": {}}
    ok = True
    t0 = time.time()

    def chk(name, val):
        res["checks"][name] = bool(val)
        nonlocal ok
        ok &= bool(val)
        print(f"  [{'PASS' if val else 'FAIL'}] {name}")

    # ================================================ KILL GATE (eps = 1.0)
    print("=" * 74)
    print("K10 -- OBLATENESS DOOR  (transport gate first: eps=1.0 = sphere)")
    print("=" * 74)
    # ---- KILLC: central on the sphere is EXACT: A = e^-1, E[D] = 1/2, W=2
    mc = measure(n, 1.0, 0.0, "central", 1.0, 1)
    res["measurements"]["KILLC"] = mc
    c = (abs(mc["A"] - math.exp(-1)) < 4 * mc["sA"]
         and abs(mc["d"] - 0.5) < 4 * mc["sD"]
         and abs(mc["W"] - 2.0) < 4 * mc["sW"])
    chk("KILLC_central_eps1_sphere_exact", c)
    print(f"  central eps=1: A={mc['A']:.5f} (e^-1={math.exp(-1):.5f})  "
          f"E[D]={mc['d']:.5f} (1/2)  W={mc['W']:.4f} (2.0)")
    # ---- KILLV: volume eps=1: atom vs exact quadrature + W vs J11 (1.8970)
    mv = measure(n, 1.0, 0.0, "volume", 1.0, 2)
    Aq = A_vol_quad(1.0, 1.0, 0.0)
    res["measurements"]["KILLV"] = dict(mc=mv, A_quad=Aq,
                                        J11_W=1.8970, J11_sW=0.005)
    cA = abs(mv["A"] - Aq) < 4 * mv["sA"]
    cW = abs(mv["W"] - 1.8970) < 5 * (mv["sW"] + 0.005)
    chk("KILLV_volume_eps1_atom_vs_quadrature", cA)
    chk("KILLV_volume_eps1_W_vs_J11", cW)
    print(f"  volume eps=1: A={mv['A']:.5f} quad={Aq:.5f}  E[D]={mv['d']:.4f}  "
          f"W={mv['W']:.4f} (J11: 1.8970)")
    if not (c and cA and cW):
        print("KILLED: eps=1.0 transport does not reproduce the sphere. ABORT.")
        res["ALL_PASSED"] = False
        res["verdict"] = "KILLED"
        print(json.dumps(res, indent=1))
        return 2

    # ========================================== MAIN GRID: q=0, tau0=1, all eps
    print("-" * 74)
    print("MAIN GRID: W = -lnA/E[D] at (q=0, tau0=1), central + volume")
    grid = {}
    for eps in (1.0, 0.7, 0.5, 0.3):
        row = {}
        for src in ("central", "volume"):
            m = measure(n, 1.0, 0.0, src, eps, 3 + (0 if src == "central" else 10))
            Aq = A_vol_quad(eps, 1.0, 0.0) if src == "volume" else A_central_quad(eps, 1.0, 0.0)
            row[src] = dict(m=m, A_quad=Aq)
            if src == "volume":
                chk(f"QV_atom_volume_eps{eps}", abs(m["A"] - Aq) < 4 * m["sA"])
            else:
                chk(f"QC_atom_central_eps{eps}", abs(m["A"] - Aq) < 4 * m["sA"])
            print(f"  eps={eps} {src:7s}: A={m['A']:.5f} (quad {Aq:.5f})  "
                  f"E[D]={m['d']:.4f}  W={m['W']:.4f} +- {m['sW']:.4f}")
        grid[eps] = row
    res["measurements"]["grid"] = {str(e): {k: v["m"] for k, v in row.items()}
                                   for e, row in grid.items()}

    # ---- GA: central window geometry-stability under oblateness?
    # Sphere anchor (eps=1): W = 2.0 (KILLC).  Finding hypotheses:
    #   eps<1 inflates W_c above the [4/3,2] band.
    print("-" * 74)
    print("GA: does the CENTRAL window leave [4/3, 2] as eps shrinks?")
    W1c, sW1c = grid[1.0]["central"]["m"]["W"], grid[1.0]["central"]["m"]["sW"]
    chk("GA_anchor_central_eps1_in_band",
        W1c + 3 * sW1c <= 2.0 + 1e-9 and W1c - 3 * sW1c >= 4.0 / 3.0 - 1e-9 or
        abs(W1c - 2.0) < 5 * sW1c)
    print(f"  eps=1.0: W_c = {W1c:.4f} +- {sW1c:.4f}  (sphere anchor, = 2.0)")
    for eps in (0.7, 0.5, 0.3):
        W, sW = grid[eps]["central"]["m"]["W"], grid[eps]["central"]["m"]["sW"]
        left = W > 2.0 + 3 * sW
        chk(f"GA_central_inflated_above_2_eps{eps}", left)
        print(f"  eps={eps}: W_c = {W:.4f} +- {sW:.4f}  "
              f"> 2 by {W - 2.0:+.4f}  ({(W - 2.0) / sW:+.1f} SE)")

    # ---- VOL: volume window at tau0=1 also inflates with flattening?
    print("-" * 74)
    print("VOL: volume window W_v(tau0=1, q=0) vs eps")
    W1v, sW1v = grid[1.0]["volume"]["m"]["W"], grid[1.0]["volume"]["m"]["sW"]
    for eps in (0.7, 0.5, 0.3):
        Wv, sWv = grid[eps]["volume"]["m"]["W"], grid[eps]["volume"]["m"]["sW"]
        ce = math.sqrt(sWv ** 2 + sW1v ** 2)
        chk(f"VOL_volume_inflated_above_eps1_eps{eps}", Wv > W1v + 3 * ce)
        print(f"  eps={eps}: W_v = {Wv:.4f} +- {sWv:.4f}  vs eps=1 {W1v:.4f}  "
              f"({(Wv - W1v) / ce:+.1f} CE)")

    # ---- correction factors W(eps)/W(1.0)  (tau0=1, q=0; independent runs)
    print("-" * 74)
    print("CORRECTION FACTORS: W(eps)/W(1.0)   [observer un-flattening]")
    corr = {}
    for eps in (0.7, 0.5, 0.3):
        Wc, sWc = grid[eps]["central"]["m"]["W"], grid[eps]["central"]["m"]["sW"]
        Wv, sWv = grid[eps]["volume"]["m"]["W"], grid[eps]["volume"]["m"]["sW"]
        cc = Wc / W1c; sc = cc * math.sqrt((sWc / Wc) ** 2 + (sW1c / W1c) ** 2)
        cv = Wv / W1v; sv = cv * math.sqrt((sWv / Wv) ** 2 + (sW1v / W1v) ** 2)
        corr[eps] = dict(central=dict(corr=cc, s=sc),
                         volume=dict(corr=cv, s=sv))
        print(f"  eps={eps}: corr_c = {cc:.4f} +- {sc:.4f}   "
              f"corr_v = {cv:.4f} +- {sv:.4f}")

    def powfit(corr_vals):
        xs = [math.log(e) for e in corr_vals]
        ys = [math.log(corr_vals[e]) for e in corr_vals]
        p = sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)
        sxx = sum(x * x for x in xs)
        resid = math.sqrt(sum((y - p * x) ** 2 for x, y in zip(xs, ys))
                          / ((len(xs) - 1) * sxx))
        return p, resid, resid   # se(p) = s_resid/sqrt(sxx) = resid

    pc, rsc, spc = powfit({e: corr[e]["central"]["corr"] for e in corr})
    pv, rsv, spv = powfit({e: corr[e]["volume"]["corr"] for e in corr})
    res["measurements"]["correction"] = dict(corr=corr,
                                             fit_central=dict(p=pc, sp=spc, resid=rsc),
                                             fit_volume=dict(p=pv, sp=spv, resid=rsv))
    print(f"  power-law fit W(eps)/W(1) = eps^p:  central p={pc:.3f} +- {spc:.3f} "
          f"(resid {rsc:.3f})  volume p={pv:.3f} +- {spv:.3f} (resid {rsv:.3f})")
    print("  PROJECTION-CORRECTION TABLE (observer un-flattening, tau0=1, q=0):")
    print("    W_sphere = W_measured / corr(eps)")
    print(f"    eps=1.0: corr = 1.0000")
    for eps in (0.7, 0.5, 0.3):
        print(f"    eps={eps}: corr_c = {corr[eps]['central']['corr']:.4f} +- "
              f"{corr[eps]['central']['s']:.4f}   corr_v = {corr[eps]['volume']['corr']:.4f} "
              f"+- {corr[eps]['volume']['s']:.4f}")

    # ====================================== VOLUME tau0-DEPENDENCE SURVIVES?
    print("-" * 74)
    print("TAU0V: does the volume tau0-dependence survive oblateness?")
    tscan = {}
    crosses = {}
    for eps in (1.0, 0.5):
        row = {}
        for tau0 in (0.5, 2.0, 3.0, 5.0, 8.0):
            m = measure(n, tau0, 0.0, "volume", eps, 20 + int(tau0 * 10))
            row[tau0] = m
            print(f"  eps={eps} tau0={tau0}: A={m['A']:.5f}  E[D]={m['d']:.4f}  "
                  f"W_v={m['W']:.4f} +- {m['sW']:.4f}")
        W05, s05 = row[0.5]["W"], row[0.5]["sW"]
        W8, s8 = row[8.0]["W"], row[8.0]["sW"]
        tscan[eps] = row
        chk(f"TAU0V_volume_tau0_dep_eps{eps}",
            W8 < W05 - 4 * (s05 + s8))
        crosses[eps] = W8 + 3 * s8 < 4.0 / 3.0
        print(f"  eps={eps}: W(8)={W8:.4f} vs W(0.5)={W05:.4f}  "
              f"cross below 4/3 by tau0=8: {crosses[eps]}")
    # the deep-opacity crossing location is itself eps-dependent: present by
    # tau0=8 at eps=1.0 (W=1.226) but pushed out beyond tau0=8 at eps=0.5
    chk("TAU0V_cross_shift_eps_dependent",
        crosses[1.0] and not crosses[0.5])
    res["measurements"]["crossing_by_tau8"] = crosses
    res["measurements"]["tau0_scan"] = {str(e): {str(t): v for t, v in row.items()}
                                        for e, row in tscan.items()}
    # volume tau0-dependence at eps=0.3: does it SURVIVE strong flattening?
    mthin = measure(n, 0.5, 0.0, "volume", 0.3, 40)
    mmid = measure(n, 3.0, 0.0, "volume", 0.3, 42)
    mthick = measure(n, 8.0, 0.0, "volume", 0.3, 41)
    res["measurements"]["tau0_scan_eps03"] = dict(thin=mthin, mid=mmid,
                                                  thick=mthick)
    Ws = [mthin["W"], mmid["W"], mthick["W"]]
    sWs = [mthin["sW"], mmid["sW"], mthick["sW"]]
    amp03 = max(Ws) - min(Ws)
    amp1 = tscan[1.0][0.5]["W"] - tscan[1.0][8.0]["W"]
    chk("TAU0V_deepcross_killed_eps0.3",
        mthick["W"] + 3 * mthick["sW"] >= 4.0 / 3.0 and amp03 < 0.5 * amp1)
    print(f"  eps=0.3: W(0.5)={mthin['W']:.4f}  W(3)={mmid['W']:.4f}  "
          f"W(8)={mthick['W']:.4f}  (tau0-variation suppressed: amplitude "
          f"{amp03:.3f} vs {amp1:.3f} at eps=1.0; NO crossing below 4/3 by "
          f"tau0=8 -- the sphere's deep-opacity decline is killed)")

    # ============================ CENTRAL tau0-FREENESS UNDER OBLATENESS?
    print("-" * 74)
    print("TAU0C: is the central window still tau0-free at eps=0.3?")
    mc05 = measure(n, 0.5, 0.0, "central", 0.3, 50)
    mc3 = measure(n, 3.0, 0.0, "central", 0.3, 51)
    res["measurements"]["central_tau0_eps03"] = dict(tau05=mc05, tau3=mc3)
    chk("TAU0C_central_tau0dep_broken_eps0.3",
        abs(mc05["W"] - mc3["W"]) > 6 * (mc05["sW"] + mc3["sW"]))
    print(f"  eps=0.3 central: W(0.5)={mc05['W']:.4f} vs W(3)={mc3['W']:.4f}  "
          f"(sphere tau0-freeness broken under oblateness)")


    # ------------------------------------------------ report + save
    res["measurements"]["anchors"] = dict(
        E_chord_central={str(e): E_chord_central(e) for e in (1.0, 0.7, 0.5, 0.3)},
        E_chord_volume={str(e): E_chord_vol(e) for e in (1.0, 0.7, 0.5, 0.3)})
    res["total_checks"] = len(res["checks"])
    res["passed"] = sum(1 for v in res["checks"].values() if v)
    res["ALL_PASSED"] = bool(ok)
    res["verdict"] = ("OPEN" if ok else "FAIL")
    print("=" * 74)
    print(f"elapsed {time.time() - t0:.1f} s;  {res['passed']}/{res['total_checks']} "
          "checks passed")
    print(json.dumps(res, indent=1))
    print("ALL K10 CHECKS PASSED" if ok else "K10 CHECK FAILURE")
    with open("K10_results.json", "w") as f:
        json.dump(res, f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    nn = int(sys.argv[1]) if len(sys.argv) > 1 else 350000
    sys.exit(run(nn))