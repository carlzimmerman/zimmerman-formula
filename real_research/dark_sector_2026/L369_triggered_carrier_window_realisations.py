#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L369 -- IS THE TRIGGERED CARRIER'S WINDOW A ONE-REALISATION ARTEFACT?  Three realisations, a 25 km/s kick grid, every gate
recomputed per realisation and pooled.

WHY.  L368 found that v_k = 650 km/s with C-H/K's p = 2 kernel switch passes every dark-sector gate on the record (S_8, the
forest, halo clearing, the two-sided X-COP gate, cosmic shear, KiDS), but in ONE grid cell of a 50 km/s grid in ONE 100 Mpc/h
realisation.  The X-COP side was thin (median retention 0.32 against a lower bound of 0.286, over 22 halos).  This lane asks
whether that window is a sampling accident of one box.

SETUP (L366/L367's construction and code, unchanged: x_c = 5, Gamma = 10 H, 100 Mpc/h, 256^3 mesh, 192^3 particles per
species).  Realisations: phase/kick seeds (7, 11) -- L366/L367's own -- and two new ones, (17, 21) and (29, 33).  Kicks
v_k in {600, 625, 650, 675, 700} km/s plus a LCDM run per realisation (18 runs).  Every gate is computed per realisation
exactly as L366 (S_8, forest, clearing, clusters), L367 (cosmic shear T(k) at z = 0.5, galaxy-peak retention at z = 0.3)
and L368 (KiDS with L360's machinery, loaded unedited) compute it, and on the POOLED sample (three boxes = 3 x 10^6
(Mpc/h)^3): S_8 ratio averaged, forest and shear from the summed power, clearing from the summed dense-cell fractions,
clusters as the median over all >= 1e14 Msun/h halos, galaxy retention over all pooled peaks.
PRE-DECLARED (before the run; thresholds are the record's, unchanged):
  H1 the POOLED sample has a non-empty full window (strict S_8, p = 2 switch) on the 25 km/s grid.
  H2 EVERY realisation, on its own, has a non-empty full window on the grid (it may sit at different kicks).
CHECKS
  C1 CONTROL: realisation (7, 11) reproduces L366's committed numbers (LCDM sigma_8; at 600/650/700 the S_8 ratio, forest,
     clearing and cluster median) and L367's T(k) exactly (deterministic code, same seeds).
  R1 = H1.  R2 = H2.  W (informational): the per-realisation and pooled gate tables; the common window.
MUTATE=1: every kick is 0 (the decayed carrier stays: nothing is cleared, clusters overshoot) -- R1 must FAIL (rc = 1).
L369_POOL sets the process-pool size (default 6; each run needs ~2.5 GB).

Run from the repository root:  python3 real_research/dark_sector_2026/L369_triggered_carrier_window_realisations.py
"""
import os, sys, json, math, time, io, contextlib, tempfile, shutil
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import L366_triggered_carrier_cluster_retention as L6           # noqa: E402  (L366's construction and code, unchanged)
import L367_triggered_carrier_cosmic_shear as L7                # noqa: E402  (L367's peak finder and P(k) bins, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L369_triggered_carrier_window_realisations"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L369", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_POOLED, EXPECT_EVERY = True, True                          # H1, H2: set before the run


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


def quiet_exec(src, ns):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, ns)
    return ns


L2 = L6.L2
Om, Hnorm, Om_a, ZI = L6.Om, L6.Hnorm, L6.Om_a, L6.ZI
WB, WC, LBOX, NG, NP, RHO_M = L6.WB, L6.WC, L6.LBOX, L6.NG, L6.NP, L6.RHO_M
KG = L7.KG
SEEDS = ((7, 11), (17, 21), (29, 33))
VK = (600.0, 625.0, 650.0, 675.0, 700.0)
TAGS = tuple(f"v{int(v)}" for v in VK)
SW = ("p=1, x_c0=1.5", "p=2, x_c0=2.0")
FOOT = ("canonical", "alt")


def run(cfg):
    """L366/L367's run with the seeds exposed and both sets of outputs (z = 3, 2, 0.5, 0.3, 0)."""
    name, sp, sk, xc, vk, gamma, tmp = cfg
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

    def density(xb, xcar):
        return (s.deposit(xb, np.full(n, WB)) + s.deposit(xcar, np.full(n, WC))) * NG ** 3 / n

    def accel(rho, a):
        gr = s.grad(s.poisson(1.5 * Om * (rho - 1.0) / a))
        return -np.stack([s.interp(gg, xb) for gg in gr], 1), -np.stack([s.interp(gg, xcar) for gg in gr], 1)

    a = ai; dlna = 0.02; zs = [3.0, 2.0, 0.5, 0.3, 0.0]; out = {}
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
                if z >= 2.0:                                           # L366's forest and clearing outputs
                    kpar, p1d = s.flux_p1d(xb, pb, a, z)
                    rec.update(kpar=kpar.tolist(), p1d=p1d.tolist())
                    rhoc2 = s.deposit(xcar, np.full(n, 1.0)) * NG ** 3 / n
                    dense = rho > 50.0
                    rec["carrier_in_dense"] = float(rhoc2[dense].sum() / max(rho[dense].sum(), 1e-30))
                elif z == 0.5:                                         # L367's shear output
                    rec["pk"] = L7.pk_bins(s, rho - 1.0)
                else:                                                  # z = 0.3 (L367's retention) and z = 0 (L366's)
                    if z == 0.0:
                        rec["sigma8"] = L6.sigma8(s, rho - 1.0)
                    rhoc = s.deposit(xcar, np.full(n, WC)) * NG ** 3 / n
                    np.save(os.path.join(tmp, f"{name}_z{z}_rho.npy"), rho.astype(np.float32))
                    np.save(os.path.join(tmp, f"{name}_z{z}_rhoc.npy"), rhoc.astype(np.float32))
                out[str(z)] = rec; zs.remove(z)
    return name, out


def load(tmp, name, z, f):
    return np.load(os.path.join(tmp, f"{name}_z{z}_{f}.npy")).astype(float)


if __name__ == "__main__":
    P(__doc__)
    NPOOL = int(os.environ.get("L369_POOL", "6"))
    TMP = tempfile.mkdtemp(prefix="L369_")
    vks = tuple(0.0 for _ in VK) if MUTATE else VK
    if MUTATE:
        P("  MUTATE: v_k = 0 in every window run (one run per realisation, used for every kick)")
    cfgs = []
    for sp, sk in SEEDS:
        cfgs.append((f"s{sp}_lcdm", sp, sk, float("inf"), 0.0, 0.0, TMP))
        if MUTATE:
            cfgs.append((f"s{sp}_v0", sp, sk, 5.0, 0.0, 10.0, TMP))
        else:
            cfgs += [(f"s{sp}_{t}", sp, sk, 5.0, v, 10.0, TMP) for t, v in zip(TAGS, vks)]
    P(f"  {len(cfgs)} runs, pool {NPOOL}, temporary fields in {os.path.basename(TMP)}")
    with Pool(NPOOL) as pool:
        res = dict(pool.map(run, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")
    nm = lambda sp, t: f"s{sp}_v0" if MUTATE else f"s{sp}_{t}"

    # ------------------------------------------------------------------------------ L368's KiDS machinery (L360's, unedited)
    TM = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]["T_max"]
    P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
    N60 = quiet_exec(open(P60).read().split("BASE = {")[0], {"__name__": "l360", "__file__": P60})
    fit_comb, carrier_esd, fit_model, A052, XE59 = N60["fit_comb"], N60["carrier_esd"], N60["fit_model"], N60["A0"], N60["XE59"]
    BASE = {f_: fit_model(A052[f_], 0.0, "none", True)[0] for f_ in FOOT}
    TC_FULL = carrier_esd(float("inf"), "cleared")
    XE = {c_: round(XE59[(float(c_.split(",")[0][2:]), float(c_.split("=")[2]))], 4) for c_ in SW}

    def kids(S, cell):
        TC = [S * t_ for t_ in TC_FULL]
        return {f_: float(fit_comb(A052[f_], XE[cell], TC, [1.0])[0] - BASE[f_]) for f_ in FOOT}

    est = L6.eps_bounds(); lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())

    # ------------------------------------------------------------------------------ per-realisation measurements
    s = L2.Sim(LBOX, NG, NP)
    M = {}
    for sp, _ in SEEDS:
        L = f"s{sp}_lcdm"
        rho_l, rc_l = load(TMP, L, 0.0, "rho"), load(TMP, L, 0.0, "rhoc")
        pk = L6.peaks(s, rho_l)
        Mh = np.array([L6.sphere_sum(s, rho_l, p_, 1.0) * RHO_M for p_ in pk])
        Mc_l = np.array([L6.sphere_sum(s, rc_l, p_, 1.0) for p_ in pk])
        rho3, rc3 = load(TMP, L, 0.3, "rho"), load(TMP, L, 0.3, "rhoc")
        pk3 = L7.peaks_fast(s, rho3, npk=200, sep=2.0)
        Mh3 = np.array([L6.sphere_sum(s, rho3, p_, 0.5) * RHO_M for p_ in pk3])
        Mc3 = np.array([L6.sphere_sum(s, rc3, p_, 0.5) for p_ in pk3])
        gal = (Mh3 >= 1e12) & (Mh3 < 3e13)
        M[sp] = dict(Mh=Mh, Mh3=Mh3, sel=Mh >= 1e14, n_cl=int((Mh >= 1e14).sum()), runs={})
        for t in TAGS:
            r_ = res[nm(sp, t)]
            rc0 = load(TMP, nm(sp, t), 0.0, "rhoc"); rc03 = load(TMP, nm(sp, t), 0.3, "rhoc")
            eps = np.array([L6.sphere_sum(s, rc0, p_, 1.0) for p_ in pk]) / Mc_l
            eps3 = np.array([L6.sphere_sum(s, rc03, p_, 0.5) for p_ in pk3]) / Mc3
            M[sp]["runs"][t] = dict(
                s8=r_["0.0"]["sigma8"] / res[L]["0.0"]["sigma8"],
                p1d={z: (np.array(r_[z]["p1d"]), np.array(res[L][z]["p1d"]), np.array(res[L][z]["kpar"])) for z in ("3.0", "2.0")},
                cid=(r_["2.0"]["carrier_in_dense"], res[L]["2.0"]["carrier_in_dense"]),
                pk=({q: r_["0.5"]["pk"][q] for q in KG}, {q: res[L]["0.5"]["pk"][q] for q in KG}),
                eps=eps, eps3=eps3,
                S_bins=[float(np.median(eps3[(Mh3 >= b0) & (Mh3 < b1)])) for b0, b1 in ((1e12, 1e13), (1e13, 3e13))
                        if ((Mh3 >= b0) & (Mh3 < b1)).any()],
                eps3_gal=eps3[gal], Mh3_gal=Mh3[gal])
    shutil.rmtree(TMP, ignore_errors=True)

    def gates(rows):
        """rows: list of per-realisation run records for one kick (one record = one realisation; several = pooled)."""
        s8 = float(np.mean([r["s8"] for r in rows]))
        fdev = 0.0
        for z in ("3.0", "2.0"):
            px = sum(r["p1d"][z][0] for r in rows); pl = sum(r["p1d"][z][1] for r in rows); kp = rows[0]["p1d"][z][2]
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(px[m] / pl[m] - 1))))
        g3 = sum(r["cid"][0] for r in rows) / max(sum(r["cid"][1] for r in rows), 1e-30)
        eps = np.concatenate([r["eps_sel"] for r in rows]); med = float(np.median(eps)) if len(eps) else float("nan")
        T = {q: math.sqrt(sum(r["pk"][0][q] for r in rows) / sum(r["pk"][1][q] for r in rows)) for q in KG}
        e3 = np.concatenate([r["eps3_gal"] for r in rows]); m3 = np.concatenate([r["Mh3_gal"] for r in rows])
        S = float(np.mean([np.median(e3[(m3 >= b0) & (m3 < b1)]) for b0, b1 in ((1e12, 1e13), (1e13, 3e13)) if ((m3 >= b0) & (m3 < b1)).any()]))
        g = dict(S8=s8, forest=fdev, G3=g3, eps_cl=med, n_cl=int(len(eps)), T=T, S=S, cells={})
        base = (s8 >= 0.922) and (fdev <= 0.10) and (g3 <= 0.30) and (lo <= med <= hi)
        for c_ in SW:
            sh = all(T[q] <= TM[f"{c_}/{f_}"][str(q)] for q in KG for f_ in FOOT)
            kd = kids(S, c_); kok = all(v <= 4.0 for v in kd.values())
            g["cells"][c_] = dict(shear=bool(sh), kids=kd, kids_ok=bool(kok), full=bool(base and sh and kok))
        return g

    for sp, _ in SEEDS:
        for t in TAGS:
            M[sp]["runs"][t]["eps_sel"] = M[sp]["runs"][t]["eps"][M[sp]["sel"]]

    def line(tag, g):
        c2, c1 = g["cells"]["p=2, x_c0=2.0"], g["cells"]["p=1, x_c0=1.5"]
        return (f"    {tag:>12s}: S8 {g['S8']:.3f} | forest {g['forest']:.3f} | cleared {g['G3']:.2f}{'' if g['G3'] <= 0.3 else ' X'} | " +
                (f"X-COP eps {g['eps_cl']:.2f}{'' if lo <= g['eps_cl'] <= hi else (' UNDER' if g['eps_cl'] < lo else ' OVER')} (n={g['n_cl']}) | "
                 if g['n_cl'] else "X-COP: no halo >= 1e14 X | ") +
                f"shear p2 {'ok' if c2['shear'] else 'X'} p1 {'ok' if c1['shear'] else 'X'} | KiDS S={g['S']:.3f} p2 "
                f"{c2['kids']['canonical']:+.1f}/{c2['kids']['alt']:+.1f} | FULL p2 {'YES' if c2['full'] else 'no'}, p1 {'YES' if c1['full'] else 'no'}")

    # ------------------------------------------------------------------------------ C1: reproduction of L366/L367
    banner("C1  CONTROL: realisation (7, 11) reproduces L366 and L367")
    R66 = json.load(open(os.path.join(HERE, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]
    R67 = json.load(open(os.path.join(HERE, "L367_triggered_carrier_cosmic_shear_results.json")))["numbers"]
    dev = [abs(res["s7_lcdm"]["0.0"]["sigma8"] / R66["runs"]["lcdm"]["0.0"]["sigma8"] - 1)]
    dev.append(float(np.max(np.abs(np.array(res["s7_lcdm"]["2.0"]["p1d"]) / np.array(R66["runs"]["lcdm"]["2.0"]["p1d"]) - 1))))
    if not MUTATE:
        for t in ("v600", "v650", "v700"):
            g1 = gates([M[7]["runs"][t]]); r66 = R66["retention"][t]
            dev += [abs(g1["S8"] / r66["s8_ratio"] - 1), abs(g1["forest"] - r66["flux_dev"]), abs(g1["G3"] / r66["G3"] - 1),
                    abs(g1["eps_cl"] / r66["median_cl"] - 1)]
            dev += [abs(g1["T"][q] / float(R67["transfer"][t]["T"][str(q)] if str(q) in R67["transfer"][t]["T"] else R67["transfer"][t]["T"][q]) - 1) for q in KG]
    check("C1 realisation (7, 11) reproduces L366's LCDM sigma_8 and forest power" + ("" if MUTATE else
          ", and at 600/650/700 L366's S_8 ratio, forest, clearing and cluster median and L367's T(k)") + " (same seeds, same code)",
          f"max relative deviation {max(dev):.1e} over {len(dev)} numbers", max(dev) < 1e-6)

    # ------------------------------------------------------------------------------ tables
    banner("THE GATE TABLE, PER REALISATION AND POOLED")
    P(f"    X-COP two-sided (L354 via L366): {lo:.3f} <= eps <= {hi:.3f}; clearing <= 0.30; forest <= 0.10; S8 >= 0.922 (strict)")
    TAB = {}; WIN = {}
    for sp, _ in SEEDS:
        P(f"  realisation ({sp}): {M[sp]['n_cl']} halos >= 1e14 Msun/h")
        TAB[str(sp)] = {}
        for t in TAGS:
            g = gates([M[sp]["runs"][t]]); TAB[str(sp)][t] = g; P(line(t, g))
        WIN[str(sp)] = [t for t in TAGS if TAB[str(sp)][t]["cells"]["p=2, x_c0=2.0"]["full"]]
    P("  POOLED (three realisations)")
    TAB["pooled"] = {}
    for t in TAGS:
        g = gates([M[sp]["runs"][t] for sp, _ in SEEDS]); TAB["pooled"][t] = g; P(line(t, g))
    WIN["pooled"] = [t for t in TAGS if TAB["pooled"][t]["cells"]["p=2, x_c0=2.0"]["full"]]
    common = [t for t in TAGS if all(t in WIN[str(sp)] for sp, _ in SEEDS)]
    P(f"\n    full windows (p = 2, strict S8): " + "; ".join(f"{k_}: {v or 'none'}" for k_, v in WIN.items()) + f"; common to all three: {common or 'none'}")
    spread = {t: (float(np.nanmin([TAB[str(sp)][t]["eps_cl"] for sp, _ in SEEDS])), float(np.nanmax([TAB[str(sp)][t]["eps_cl"] for sp, _ in SEEDS])))
              for t in TAGS}
    P("    cluster-median spread across realisations: " + ", ".join(f"{t}: {a_:.2f}-{b_:.2f}" for t, (a_, b_) in spread.items()))
    OUT["numbers"].update(eps_bounds=dict(lo=lo, hi=hi), windows=WIN, common=common, eps_spread=spread,
                          table={k_: {t: {kk: vv for kk, vv in g.items()} for t, g in v.items()} for k_, v in TAB.items()},
                          n_clusters={str(sp): M[sp]["n_cl"] for sp, _ in SEEDS})
    check("W (informational) per-realisation and pooled gate tables, the common window and the cluster-median spread", "see tables",
          True, "reported either way", load_bearing=False)

    banner("R1, R2  THE HYPOTHESES (set before the run)")
    check("R1 = H1: the POOLED three-realisation sample has a non-empty full window (strict S_8, p = 2 switch, every gate, both footings)",
          f"pooled window: {WIN['pooled'] or 'none'}", bool(WIN["pooled"]) == EXPECT_POOLED)
    check("R2 = H2: EVERY realisation on its own has a non-empty full window on the 25 km/s grid",
          "; ".join(f"({k_}): {v or 'none'}" for k_, v in WIN.items() if k_ != "pooled"),
          all(bool(WIN[str(sp)]) for sp, _ in SEEDS) == EXPECT_EVERY)

    banner("VERDICT")
    P(f"""  Full window (p = 2 switch, strict S_8, every gate): pooled {WIN['pooled'] or 'none'}; per realisation """ +
      "; ".join(f"({sp}) {WIN[str(sp)] or 'none'}" for sp, _ in SEEDS) + f"""; common {common or 'none'}.
  LIMITS: three 100 Mpc/h boxes (one mesh, 0.39 Mpc/h), galaxy retention sub-cell, the trigger posited (no action), MOND on
  baryons inside halos not modelled, L354's X-COP response as the map from retention to M_dyn/M_HSE.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
