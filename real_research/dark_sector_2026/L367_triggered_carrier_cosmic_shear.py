#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L367 -- COSMIC SHEAR FOR THE VIRIALIZATION-TRIGGERED CARRIER: does L366's joint window survive the gate that closed the
parallel constructions (L363, L364)?

WHY.  L366 found a joint window for the virialization-triggered carrier (x_c = 5, v_k ~ 650 km/s): S_8 (matter only),
the forest, halo clearing and the two-sided X-COP gate.  But lensing sees the MOND PHANTOM as well as matter.  L363
showed the bound-region phantom ADDED to a full matter field fails cosmic shear; L364 showed a kicked, free-streaming
carrier can hand its small-scale power to the phantom, and wrote the gate as a bound on the total-matter transfer at the
lens epoch:
      R(k) = T(k)^2 + 2 r_x(k) T(k) s(k) + s(k)^2 <= 1.2   <=>   T(k) <= T_max(k) = -r_x s + sqrt(r_x^2 s^2 + 1.2 - s^2),
with s^2 = P_ph/P_NL and r_x the matter-phantom correlation measured by L363's region kernel on GP3's mock (z = 0.5), for
the two kernel switch cells (p = 1, x_c0 = 1.5; p = 2, x_c0 = 2.0) and both footings.  The phantom depends on the kernel's
switch only (the carrier is kernel-invisible, L353), so this lane reads L364's committed T_max and measures the carrier's
T(k) = sqrt(P_model/P_LCDM) at z = 0.5 -- NONLINEAR, from the particle-mesh runs, where L364 had to assume the one-halo
power scales with the linear transfer.

METHOD: L366's construction and code, unchanged (100 Mpc/h, 256^3 mesh, 192^3 particles per species, x_c = 5, Gamma =
10 H, same seed), with outputs at z = 0.5 (total-matter P(k) in bins centred on L364's k-grid, +-20%) and z = 0.3 (the
carrier's retention in low-mass peaks, for the KiDS side).  Runs: LCDM and v_k in {600, 650, 700} km/s.
PRE-DECLARED
  * COSMIC SHEAR passes for a kick iff T(k) <= T_max(k) at every k in {0.1, 0.2, 0.3, 0.5, 0.7, 1.0} h/Mpc for at least one
    switch cell, on both footings.
  * HYPOTHESIS (set before the run): it passes with the p = 2 switch cell and fails with p = 1.
CHECKS
  C1 CONTROL: LCDM against itself gives T = 1 exactly.
  S1 THE GATE AT THE WINDOW (v_k = 650): as hypothesised.
  S2 (informational) retention of the carrier at z = 0.3 within 0.5 Mpc/h of group- and galaxy-mass peaks (KiDS's side;
     galaxy halos are sub-cell at this mesh, so this is indicative only).
MUTATE=1: v_k = 0 (the decayed carrier stays and keeps clustering: T ~ 1): the p = 2 pass must FAIL (rc = 1).

Run from the repository root:  python3 real_research/dark_sector_2026/L367_triggered_carrier_cosmic_shear.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import L366_triggered_carrier_cluster_retention as L6           # noqa: E402  (L366's construction and code, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L367_triggered_carrier_cosmic_shear"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L367", "mutate": MUTATE, "checks": {}, "numbers": {}}


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
    P("\n" + "=" * 110); P(t); P("=" * 110)


L2 = L6.L2
Om, Hnorm, Om_a, ZI = L6.Om, L6.Hnorm, L6.Om_a, L6.ZI
WB, WC, LBOX, NG, NP, RHO_M = L6.WB, L6.WC, L6.LBOX, L6.NG, L6.NP, L6.RHO_M
KG = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]


def peaks_fast(s, rho, npk=200, sep=2.0):
    """local maxima of the 1 Mpc/h-smoothed density (26-neighbour filter), strongest first, >= sep apart."""
    from scipy.ndimage import maximum_filter
    sm = s.smooth(rho, 1.0)
    cand = np.argwhere(sm == maximum_filter(sm, size=3, mode="wrap"))
    cand = cand[np.argsort(sm[tuple(cand.T)])[::-1]]
    pts = []
    for ijk in cand:
        pos = (ijk + 0.5) * s.d
        if all(np.linalg.norm(((pos - p_ + LBOX / 2) % LBOX) - LBOX / 2) >= sep for p_ in pts):
            pts.append(pos)
            if len(pts) >= npk:
                break
    return np.array(pts)


def pk_bins(s, delta):
    f = np.fft.fftn(delta); Pw = np.abs(f) ** 2
    kk = np.sqrt(s.K2); kk[0, 0, 0] = 0
    return {q: float(Pw[(kk >= 0.8 * q) & (kk <= 1.2 * q)].mean()) for q in KG}


def run(cfg):
    name, xc, vk, gamma = cfg
    s = L2.Sim(LBOX, NG, NP)
    s.deposit = lambda x, w: L6.deposit_fast(s, x, w)
    rng = np.random.default_rng(7)
    kk = np.sqrt(s.K2); kk[0, 0, 0] = s.kf
    Pk = np.vectorize(lambda q: L2.P_lin(q, ZI))(np.clip(kk, s.kf, 60.0)); Pk[0, 0, 0] = 0
    white = np.fft.fftn(rng.normal(size=(NG, NG, NG)))
    delta0 = np.real(np.fft.ifftn(white * np.sqrt(Pk * NG ** 3 / LBOX ** 3)))
    psi = [-gg for gg in s.grad(s.poisson(delta0))]
    q = (np.arange(NP) + 0.5) * LBOX / NP
    QX, QY, QZ = np.meshgrid(q, q, q, indexing='ij'); Q = np.stack([QX.ravel(), QY.ravel(), QZ.ravel()], 1)
    disp = np.stack([s.interp(pp, Q) for pp in psi], 1)
    ai = 1 / (1 + ZI); fg = Om_a(ai) ** 0.55
    xb = (Q + disp) % LBOX; pb = ai ** 2 * Hnorm(ai) * fg * disp
    xcar, pcar = xb.copy(), pb.copy()
    n = len(xb); cold = np.ones(n, bool)
    krng = np.random.default_rng(11)

    def density(xb, xcar):
        return (s.deposit(xb, np.full(n, WB)) + s.deposit(xcar, np.full(n, WC))) * NG ** 3 / n

    def accel(rho, a):
        gr = s.grad(s.poisson(1.5 * Om * (rho - 1.0) / a))
        return -np.stack([s.interp(gg, xb) for gg in gr], 1), -np.stack([s.interp(gg, xcar) for gg in gr], 1)

    a = ai; dlna = 0.02; zs = [0.5, 0.3]; out = {}
    rho = density(xb, xcar); ab, ac = accel(rho, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * Hnorm(a))
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        xb = (xb + dt * pb / a ** 2) % LBOX; xcar = (xcar + dt * pcar / a ** 2) % LBOX
        a = a + da
        rho = density(xb, xcar)
        if gamma > 0 and cold.any():                                   # L365/L366's trigger, unchanged
            xt = 1.5 * Om_a(a) * (rho - 1.0)
            idx = np.where(cold)[0]
            xp = s.interp(xt, xcar[idx])
            hit = idx[(xp > xc) & (krng.random(len(idx)) < 1 - math.exp(-gamma * Hnorm(a) * dt))]
            if len(hit):
                nh = krng.normal(size=(len(hit), 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
                pcar[hit] += a * (vk / 100.0) * nh
                cold[hit] = False
        ab, ac = accel(rho, a)
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        for z in list(zs):
            if 1 / a - 1 <= z + 1e-9:
                rec = {"decayed": float(1 - cold.mean())}
                if z == 0.5:
                    rec["pk"] = pk_bins(s, rho - 1.0)
                else:
                    rhoc = s.deposit(xcar, np.full(n, WC)) * NG ** 3 / n
                    np.save(os.path.join(HERE, f"_L367_{name}_rho.npy"), rho.astype(np.float32))
                    np.save(os.path.join(HERE, f"_L367_{name}_rhoc.npy"), rhoc.astype(np.float32))
                out[str(z)] = rec; zs.remove(z)
    return name, out


if __name__ == "__main__":
    P(__doc__)
    VK = (600.0, 650.0, 700.0)
    vks = tuple(0.0 for _ in VK) if MUTATE else VK
    if MUTATE:
        P("  MUTATE: v_k = 0 in the window runs")
    TAGS = tuple(f"v{int(v)}" for v in VK)
    cfgs = [("lcdm", float("inf"), 0.0, 0.0), ("lcdm_twin", float("inf"), 0.0, 0.0)]
    cfgs += [(f"x5_{t}", 5.0, v, 10.0) for t, v in zip(TAGS, vks)]
    with Pool(len(cfgs)) as pool:
        res = dict(pool.map(run, cfgs))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")
    TM = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]

    banner("CONTROL")
    tw = max(abs(math.sqrt(res["lcdm_twin"]["0.5"]["pk"][q] / res["lcdm"]["0.5"]["pk"][q]) - 1) for q in KG)
    check("C1 LCDM against an identical LCDM run gives T(k) = 1 exactly (same phases, deterministic code)", f"max |T - 1| = {tw:.1e}", tw < 1e-12)

    banner("THE TRANSFER AT z = 0.5 vs WHAT COSMIC SHEAR ALLOWS (L364's T_max)")
    P("    T_max (L364): " + "; ".join(f"{c_}: " + ", ".join(f"{q}:{v_[q] if q in v_ else v_[str(q)]:.2f}" for q in KG) for c_, v_ in TM.items()))
    VER = {}
    for t in TAGS:
        T = {q: math.sqrt(res[f"x5_{t}"]["0.5"]["pk"][q] / res["lcdm"]["0.5"]["pk"][q]) for q in KG}
        cells = {}
        for c_, v_ in TM.items():
            tm = {q: (v_[q] if q in v_ else v_[str(q)]) for q in KG}
            cells[c_] = dict(ok=all(T[q] <= tm[q] for q in KG), worst=max(T[q] - tm[q] for q in KG))
        sw = {}
        for sc in ("p=1, x_c0=1.5", "p=2, x_c0=2.0"):
            sw[sc] = cells[f"{sc}/canonical"]["ok"] and cells[f"{sc}/alt"]["ok"]
        VER[t] = dict(T=T, cells=cells, switch_pass=sw, decayed_z05=res[f"x5_{t}"]["0.5"]["decayed"])
        P(f"    v_k {t[1:]}: T(k) " + ", ".join(f"{q}:{T[q]:.3f}" for q in KG) + "  ->  " +
          "; ".join(f"{sc}: {'PASS' if ok else 'FAIL'}" for sc, ok in sw.items()) +
          "   (worst T - T_max: " + ", ".join(f"{c_}: {d['worst']:+.3f}" for c_, d in cells.items()) + ")")
    OUT["numbers"]["transfer"] = VER

    banner("S2  THE KiDS SIDE (informational): carrier retention at z = 0.3 near low-mass peaks")
    s = L2.Sim(LBOX, NG, NP)
    rho_l = np.load(os.path.join(HERE, "_L367_lcdm_rho.npy")).astype(float)
    rc_l = np.load(os.path.join(HERE, "_L367_lcdm_rhoc.npy")).astype(float)
    pk = peaks_fast(s, rho_l, npk=200, sep=2.0)
    Mh = np.array([L6.sphere_sum(s, rho_l, p_, 0.5) * RHO_M for p_ in pk])
    Mcl = np.array([L6.sphere_sum(s, rc_l, p_, 0.5) for p_ in pk])
    bins = [(1e12, 1e13), (1e13, 3e13), (3e13, 1e14), (1e14, 1e16)]
    RET = {}
    for t in TAGS:
        rc = np.load(os.path.join(HERE, f"_L367_x5_{t}_rhoc.npy")).astype(float)
        eps = np.array([L6.sphere_sum(s, rc, p_, 0.5) for p_ in pk]) / Mcl
        RET[t] = {f"{lo:.0e}-{hi:.0e}": (float(np.median(eps[(Mh >= lo) & (Mh < hi)])) if ((Mh >= lo) & (Mh < hi)).any() else None,
                                         int(((Mh >= lo) & (Mh < hi)).sum())) for lo, hi in bins}
        P(f"    v_k {t[1:]}: retention within 0.5 Mpc/h at z = 0.3 by M(<0.5 Mpc/h): " +
          ", ".join(f"{b}: {v[0]:.2f} (n={v[1]})" if v[0] is not None else f"{b}: - (n=0)" for b, v in RET[t].items()))
    OUT["numbers"]["retention_z03"] = RET
    check("S2 (informational) the carrier's retention near group- and galaxy-mass peaks at z = 0.3 (KiDS wants ~0.2-0.3 of a LCDM "
          "halo, L355; galaxy halos are sub-cell here)", "; ".join(f"{t}: {RET[t]}" for t in TAGS), True, "reported either way",
          load_bearing=False)
    for tag in ("lcdm", "lcdm_twin") + tuple(f"x5_{t}" for t in TAGS):
        for f_ in ("rho", "rhoc"):
            try:
                os.remove(os.path.join(HERE, f"_L367_{tag}_{f_}.npy"))
            except OSError:
                pass

    banner("S1  THE GATE AT THE WINDOW (v_k = 650)")
    v = VER["v650"]["switch_pass"]
    check("S1 COSMIC SHEAR AT THE WINDOW (v_k = 650): PASSES with the p = 2 kernel switch and FAILS with p = 1 (both footings) "
          "-- the hypothesis set before the run", f"p = 2: {'PASS' if v['p=2, x_c0=2.0'] else 'FAIL'}; p = 1: {'PASS' if v['p=1, x_c0=1.5'] else 'FAIL'}",
          v["p=2, x_c0=2.0"] and not v["p=1, x_c0=1.5"], "T_max from L364 (L363's region kernel on GP3's mock at z = 0.5)")

    banner("VERDICT")
    P(f"""  The carrier's nonlinear matter transfer at z = 0.5 against cosmic shear's bound (L364):
  """ + "\n  ".join(f"v_k {t[1:]}: " + "; ".join(f"{sc}: {'PASS' if ok else 'FAIL'}" for sc, ok in VER[t]['switch_pass'].items()) for t in TAGS) + """
  LIMITS: one lens epoch (z = 0.5), P(k) not a projected xi_+-, r_x held at its full-matter value (L364's approximation),
  100 Mpc/h box (few modes at k = 0.1), one realisation.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
