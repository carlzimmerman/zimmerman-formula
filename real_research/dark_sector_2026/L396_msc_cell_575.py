#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L396 -- THE DECISIVE SAME-MODEL RUN: the MOND-sector switch with MS5's action-term cap (the mean curvature of the MOND field's
equipotentials) in the particle-mesh dynamics, scored with the SAME cap on MS3's halo model, at 575, 600 and 650 km/s in
three realisations.

WHY.  MS1 (mond_sector_gate_2026): once the gate is an action term the switch must read the MOND sector (baryons + their
phantom), never the carrier or the curvature.  MS3: cosmic shear, scored resolution-free, needs MOND regions capped near
1.75 Mpc at z = 0.5.  MS5 (committed 61a3a0858, 5/5): the cap as an action term is U_cap = C min(lap Phi_X, v_cap^2 kappa_X^2)
with kappa_X = (1/2) div(grad Phi_X/|grad Phi_X|) the mean curvature of the MOND field's equipotentials (1/r for every
spherical profile), so every region stops at l_cap(z) = v_cap/(H sqrt(x_c)): 1.75 Mpc at z = 0.5 -- MS3's hard cap.  The
earlier local form v_loc^2 = |grad Phi|^2/lap Phi, which L395's primary cell implements, is WITHDRAWN (MS5: it grows cluster
regions with their gas and fails shear).  L389 (provisional) found Harvey's phase-mixed shape passes only at 575 km/s.  This
lane runs the leak-free switch with the withdrawn-free cap, at 575-650 km/s, as ONE model: the PM dynamics and the shear score
use the same cap.

THE SWITCH ON THE MESH (cell "msck"; p = 1, x_c0 = 2.5, L395's module-level cell): the MOND-sector reading
x_ms = 1.5 Omega_m(a)(rho_b + max(delta_ph,all, 0)) (MS3's door: the baryons plus the positive untruncated phantom); the cap
x_cap = v_cap^2 kappa_X^2/H(a)^2 with kappa_X = (1/2) div(n), n = grad Phi_X/|grad Phi_X|, Phi_X the MOND-sector potential
(baryons' Newtonian + untruncated phantom), physical units; where |grad Phi_X| vanishes (a potential minimum, kappa -> inf) the
cap does not bind; U = (x_ms^-4 + x_cap^-4)^(-1/4) (MS5's smooth min, n = 4); switched where U [Omega_L(a)/Omega_L0] > x_c0.
Everything else is L377's full construction (phantom felt by the baryons and read by the trigger, carrier Newtonian) with
L395's hooks (z = 2 fields + baryon NGP cells, z = 0.4 fields, kept in real_research/dark_sector_2026/_L396_fields/).
GATES (L395's): strict S_8, forest, the clearing rule (pooled L <= 0.30 AND B <= 0.30, XR2 section 5), two-sided X-COP,
cosmic shear on MS3's halo model with the cell's own pooled retention at the SAME cap ("door", r_cap = 1.75 Mpc).
PRE-DECLARED (before the run): H: the same-model cell has a pooled window at some kick in {575, 600, 650} km/s.
HISTORY: a first version of this lane ran L395's (withdrawn-cap) cell at 575 only; it was rebuilt on MS5's cap and extended to
600 and 650 before any run.
CHECKS
  C1 the (7, 11) LCDM run reproduces L366's sigma_8 exactly.
  C3 MS3's halo model reproduces MS3's committed K1 (1.75 Mpc, L388's retention) exactly.
  C4 the LCDM z = 2 fields reproduce L395's saved LCDM z = 2 fields exactly (one run set).
  C5 the mesh mean curvature (the production operator, fourth-order differences): for a spherical blob, kappa_X = 1/r to
     within 5% at r = 1, 2, 3 Mpc/h (a second-order first version was 14% low at 3 cells in a code test).
  K0 species identity in every LCDM run.
  R1 = H.  W (informational): per-box and pooled gates per kick, clearing by environment and flags, the cap's reach, the
     retention used, the z = 0.4 retention by mass (for Harvey at its own epoch, L397).
MUTATE=1: every kick is 0: R1 must FAIL (rc = 1).
L396_POOL sets the pool size (default 8).

Run from the repository root after L395:  python3 real_research/dark_sector_2026/L396_msc_cell_575.py
"""
import os, sys, json, math, time, inspect
import numpy as np
from multiprocessing import Pool
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import L395_two_switch_branches as L95                          # noqa: E402  (L395's cell, hooks, estimators, MS3 loader)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L396_msc_cell_575"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L396", "cell": "p=1, x_c0=2.5",
               "switch": "msck: MOND-sector reading (baryons + positive untruncated phantom) with MS5's mean-curvature cap "
                         "(v_cap = 325 km/s, smooth min n = 4) -- the same cap as the shear score",
               "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT = True                                                    # H, set before the run
L77, L6, L7, L2 = L95.L77, L95.L6, L95.L7, L95.L2
LBOX, NG, NP, RHO_M, KG, WB, WC = L95.LBOX, L95.NG, L95.NP, L95.RHO_M, L95.KG, L95.WB, L95.WC
SEEDS, THR, BINS, MBINS = L95.SEEDS, L95.THR, L95.BINS, L95.MBINS
VK = (575.0, 600.0, 650.0)
TAGS = tuple(f"v{int(v)}" for v in VK)
FIELDS = os.path.join(HERE, "_L396_fields" + ("_MUTATE" if MUTATE else ""))

# ---------------------------------------------------------------------------------- MS5's cap on the mesh, in L377's namespace
_SWK = '''
def grad4(f, d):
    """fourth-order central differences (periodic): the mean curvature needs them at 3-5 cells (C5)."""
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


def phantom_swk(s, rb, rho, a, a0c, swmode):
    """'msck': the MOND-sector reading with MS5's mean-curvature cap; any other mode goes to L395's phantom_sw."""
    if swmode != "msck":
        return phantom_sw(s, rb, rho, a, a0c, swmode)
    gate = (OL / (Om * a ** -3 + OL) / OL) ** P_GATE
    phib = s.poisson(1.5 * Om * (rb - WB) / a)
    gb = [-(1.0 / a) * g for g in s.grad(phib)]
    nu1 = nu_vec(np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / a0c) - 1.0

    def solve(f):
        w = [np.where(f, nu1 * g, 0.0) for g in gb]
        divw = s.div(w)
        return s.poisson(-a * divw), -(2 * a * a / (3 * Om)) * divw

    Phi_all, dph_all = solve(np.ones(rho.shape, bool))
    xms = 1.5 * Om_a(a) * (rb + np.maximum(dph_all, 0.0))
    kap, ok = kappa_mesh(phib + Phi_all, s.d)                   # the MOND-sector potential's level sets (comoving)
    kap = kap / a                                                 # physical mean curvature of the equipotentials
    xcap = np.where(ok, VCAP_CODE2 * kap ** 2 / Hnorm(a) ** 2, np.inf)
    U = (np.maximum(xms, 1e-300) ** -4 + np.maximum(xcap, 1e-300) ** -4) ** -0.25
    f = U * gate > X_C0
    f0 = xms * gate > X_C0
    SWDIAG["steps"] += 1
    if f0.any():
        SWDIAG["capped_max"] = max(SWDIAG["capped_max"], float((f0 & ~f).sum() / f0.sum()))
    SWDIAG["switched_max"] = max(SWDIAG["switched_max"], float(f.mean()))
    if not f.any():
        return None, None, 0.0
    Phi, dph = solve(f)
    return Phi, dph, float(f.mean())
'''
exec(compile(_SWK, "L396.phantom_swk", "exec"), L77.__dict__)
_T = inspect.getsource(L77.run)
for _a, _b in L95._REPS:                                         # L395's hooks, verbatim, with the call pointed at phantom_swk
    assert _T.count(_a) == 1, _a[:60]
    _T = _T.replace(_a, _b.replace("phantom_sw(", "phantom_swk("))
exec(compile(_T.replace("def run(cfg):", "def run_swk(cfg):", 1), "L377.run+L396", "exec"), L77.__dict__)
run_swk = L77.run_swk


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


def c5_curvature():
    """C5: the mesh mean curvature of a spherical blob's potential is 1/r (a = 1, comoving = physical)."""
    Lb, Nb = 40.0, 128
    s = L2.Sim(Lb, Nb, 8)
    g = (np.arange(Nb) + 0.5) * s.d - Lb / 2
    X, Y, Z = np.meshgrid(g, g, g, indexing='ij'); R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    blob = np.exp(-0.5 * (R / 0.3) ** 2); blob = blob / blob.mean() - 1.0
    kap, _ = L77.kappa_mesh(s.poisson(blob), s.d)                # the production operator
    out = []
    for rq in (1.0, 2.0, 3.0):
        vals = []
        for ax in range(3):
            for sgn in (1, -1):
                idx = [Nb // 2] * 3; idx[ax] = Nb // 2 + sgn * int(round(rq / s.d)) - (1 if sgn < 0 else 0)
                i = tuple(idx); vals.append(kap[i] * R[i])
        out.append(dict(r=rq, kappa_times_r=float(np.mean(vals))))
    return out


if __name__ == "__main__":
    P(__doc__)
    banner("C5  THE MESH MEAN CURVATURE (before the runs)")
    c5 = c5_curvature()
    for r_ in c5:
        P(f"    r = {r_['r']:.0f} Mpc/h: kappa x r = {r_['kappa_times_r']:.4f}")
    check("C5 the mesh mean curvature (the production operator) of a spherical blob's potential is 1/r to within 5% at r = 1, 2, 3 Mpc/h",
          f"{c5}", all(abs(r_["kappa_times_r"] - 1) < 0.05 for r_ in c5))
    OUT["numbers"]["C5"] = c5

    os.makedirs(FIELDS, exist_ok=True)
    A0C = L77.A0["canonical"]
    cfgs = [(f"s{sp}_lcdm", sp, sk, float("inf"), 0.0, 0.0, FIELDS, "none", A0C, "matter") for sp, sk in SEEDS]
    SRC = {}
    for sp, sk in SEEDS:
        if MUTATE:
            cfgs.append((f"s{sp}_msck_v0", sp, sk, L77.XC_TRIG, 0.0, 10.0, FIELDS, "full", A0C, "msck"))
            SRC.update({(sp, t): f"s{sp}_msck_v0" for t in TAGS})
        else:
            cfgs += [(f"s{sp}_msck_{t}", sp, sk, L77.XC_TRIG, v, 10.0, FIELDS, "full", A0C, "msck") for t, v in zip(TAGS, VK)]
            SRC.update({(sp, t): f"s{sp}_msck_{t}" for t in TAGS})
    if MUTATE:
        P("  MUTATE: v_k = 0 in every decaying run (one per realisation, used for every kick)")
    P(f"  {len(cfgs)} runs, pool {int(os.environ.get('L396_POOL', '8'))}, cell p = {L77.P_GATE}, x_c0 = {L77.X_C0}, v_cap^2 = {L77.VCAP_CODE2} (code)")
    with Pool(int(os.environ.get("L396_POOL", "8"))) as pool:
        res = dict(pool.map(run_swk, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")
    ld = lambda nm, z, f: np.load(os.path.join(FIELDS, f"{nm}_z{z}_{f}.npy"))

    banner("C1, C3, C4, K0  CONTROLS")
    R66 = json.load(open(os.path.join(HERE, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]
    d1 = abs(res["s7_lcdm"]["0.0"]["sigma8"] / R66["runs"]["lcdm"]["0.0"]["sigma8"] - 1)
    check("C1 the (7, 11) LCDM run reproduces L366's sigma_8", f"relative deviation {d1:.1e}", d1 < 1e-9)
    M3 = L95.load_ms3(); R_of, XLIN, A0M = M3["R_of"], M3["XLIN"], M3["A0"]
    K1c = json.load(open(os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector_results.json")))["numbers"]["K1"]["1.75"]
    c3 = {f_: max(R_of(XLIN, A0M[f_], 1.75, "door", M3["ret_L388"])[0].values()) for f_ in ("canonical", "alt")}
    dc3 = max(abs(c3[f_] - K1c[f_]["worst"]) for f_ in c3)
    check("C3 MS3's halo model reproduces MS3's committed K1 at the 1.75 Mpc cap with L388's retention (both footings)", f"max |diff| {dc3:.1e}", dc3 < 1e-9)
    F95 = os.path.join(HERE, "_L395_fields")
    if os.path.exists(os.path.join(F95, "s7_lcdm_z2_rho.npy")):
        d4 = max(float(np.max(np.abs(ld(f"s{sp}_lcdm", 2, "rho") - np.load(os.path.join(F95, f"s{sp}_lcdm_z2_rho.npy"))))) for sp, _ in SEEDS)
        check("C4 the LCDM z = 2 fields reproduce L395's saved LCDM z = 2 fields exactly (one run set)", f"max |difference| {d4:.1e}", d4 == 0.0)
    else:
        check("C4 (skipped: L395's fields not on disk)", "not run", True, load_bearing=False)
    k0 = max(float(np.max(np.abs(ld(f"s{sp}_lcdm", 2, "rho") - ld(f"s{sp}_lcdm", 2, "rhoc")))) for sp, _ in SEEDS)
    check("K0 species identity: in every LCDM run the z = 2 total and unit-weight carrier fields are equal", f"max |rho - rhoc2| = {k0:.1e}", k0 == 0.0)

    est = L6.eps_bounds(); lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())
    s = L2.Sim(LBOX, NG, NP)
    PER, EST = {}, {}
    for sp, _ in SEEDS:
        L = f"s{sp}_lcdm"
        rho_l2 = ld(L, 2, "rho").astype(float); c_l2 = WC * ld(L, 2, "rhoc").astype(float); bc_l = ld(L, 2, "bcell")
        pk2 = L7.peaks_fast(s, rho_l2, npk=4000, sep=1.0)
        Mp = np.array([L6.sphere_sum(s, rho_l2, p_, 0.5) * RHO_M for p_ in pk2]); tree = cKDTree(pk2, boxsize=LBOX)
        _, jj = tree.query((np.array(np.unravel_index(np.arange(NG ** 3), rho_l2.shape)).T + 0.5) * s.d)
        envmass = Mp[jj].reshape(rho_l2.shape); del jj
        rho_l0, rc_l0 = ld(L, 0.0, "rho").astype(float), ld(L, 0.0, "rhoc").astype(float)
        pk = L6.peaks(s, rho_l0)
        Mh = np.array([L6.sphere_sum(s, rho_l0, p_, 1.0) * RHO_M for p_ in pk]); sel = Mh >= 1e14
        Mc_l = np.array([L6.sphere_sum(s, rc_l0, p_, 1.0) for p_ in pk])
        rho_l4, rc_l4 = ld(L, 0.4, "rho").astype(float), ld(L, 0.4, "rhoc").astype(float)
        pk4 = L6.peaks(s, rho_l4)
        Mh4 = np.array([L6.sphere_sum(s, rho_l4, p_, 1.0) * RHO_M for p_ in pk4])
        Mc_l4 = np.array([L6.sphere_sum(s, rc_l4, p_, 1.0) for p_ in pk4])
        for t in TAGS:
            nm = SRC[(sp, t)]; r_ = res[nm]
            rho_m2 = ld(nm, 2, "rho").astype(float); c_m2 = WC * ld(nm, 2, "rhoc").astype(float); bc_m = ld(nm, 2, "bcell")
            ests = {"all": L95.estimators(rho_l2, c_l2, rho_m2, c_m2, bc_l, bc_m)}
            for bn, b0, b1 in BINS:
                ests[bn] = L95.estimators(rho_l2, c_l2, rho_m2, c_m2, bc_l, bc_m, sel=(envmass >= b0) & (envmass < b1))
            eps = np.array([L6.sphere_sum(s, ld(nm, 0.0, "rhoc").astype(float), p_, 1.0) for p_ in pk]) / Mc_l
            eps4 = np.array([L6.sphere_sum(s, ld(nm, 0.4, "rhoc").astype(float), p_, 1.0) for p_ in pk4]) / Mc_l4
            PER[(sp, t)] = dict(s8=r_["0.0"]["sigma8"] / res[L]["0.0"]["sigma8"],
                                p1d={z: (np.array(r_[z]["p1d"]), np.array(res[L][z]["p1d"]), np.array(res[L][z]["kpar"])) for z in ("3.0", "2.0")},
                                eps_sel=eps[sel], eps=eps, Mh=Mh, eps4=eps4, Mh4=Mh4, sw_diag=r_.get("sw_diag"))
            EST[(sp, t)] = ests
        for z_ in (0.3, 0.0):
            for f_ in (os.path.join(FIELDS, x) for x in os.listdir(FIELDS) if x.startswith(f"s{sp}_") and f"_z{z_}_" in x):
                os.remove(f_)

    def retention_fn(keys):                                       # L395's (MS3's) construction
        mh = np.concatenate([PER[k_]["Mh"] for k_ in keys]); ee = np.concatenate([PER[k_]["eps"] for k_ in keys])
        B = L95.combine([EST[k_]["all"] for k_ in keys])["B"]
        lx, ly = [math.log10(1e13)], [B]
        for _, b0, b1, cen in MBINS:
            m_ = (mh >= b0) & (mh < b1)
            if m_.any():
                lx.append(math.log10(cen)); ly.append(float(np.median(ee[m_])))
        return (lambda M: float(np.interp(math.log10(M), lx, ly, left=ly[0], right=ly[-1]))), dict(zip([f"{10 ** x:.2e}" for x in lx], ly))

    def gates(keys):                                              # L395's gates, the shear at the same (1.75 Mpc) cap
        rows = [PER[k_] for k_ in keys]
        s8 = float(np.mean([r["s8"] for r in rows])); fdev = 0.0
        for z in ("3.0", "2.0"):
            px = sum(r["p1d"][z][0] for r in rows); pl = sum(r["p1d"][z][1] for r in rows); kp = rows[0]["p1d"][z][2]
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(px[m] / pl[m] - 1))))
        eps = np.concatenate([r["eps_sel"] for r in rows]); med = float(np.median(eps)) if len(eps) else float("nan")
        ret, rtab = retention_fn(keys)
        worst = {f_: max(R_of(XLIN, A0M[f_], 1.75, "door", ret)[0].values()) for f_ in ("canonical", "alt")}
        sh = all(v <= 1.2 for v in worst.values())
        cl = L95.combine([EST[k_]["all"] for k_ in keys]); byb = {bn: L95.combine([EST[k_][bn] for k_ in keys]) for bn, _, _ in BINS}
        clear = cl["L"] <= 0.30 and cl["B"] <= 0.30
        flags = dict(estimator_dependent=bool((cl["L"] <= 0.30) != (cl["E"] <= 0.30)),
                     galaxy_bin_failure=bool(clear and byb["galaxy"].get("L", 0.0) > 0.30), C_below_half=bool(cl["C"] < 0.5))
        return dict(S8=s8, forest=fdev, eps_cl=med, shear_hm=bool(sh), shear_hm_worstR=worst, retention_used=rtab, clearing=cl,
                    clearing_by_bin=byb, clear=bool(clear), flags=flags, full=bool(s8 >= 0.922 and fdev <= 0.10 and clear and lo <= med <= hi and sh))

    banner("THE SAME-MODEL CELL (MOND-sector switch + MS5's cap) AT 575, 600, 650 km/s: per box and pooled")
    TAB = {}
    for key, keys_of in [(str(sp), lambda t, sp=sp: [(sp, t)]) for sp, _ in SEEDS] + [("pooled", lambda t: [(sp, t) for sp, _ in SEEDS])]:
        TAB[key] = {}
        for t in TAGS:
            g = gates(keys_of(t)); TAB[key][t] = g; c_ = g["clearing"]
            P(f"    {key:>6s} {t}: S8 {g['S8']:.3f} | forest {g['forest']:.3f} | clearing L {c_['L']:.3f} B {c_['B']:.3f} (D {c_['D']:.3f} "
              f"E {c_['E']:.3f} C {c_['C']:.2f}) | X-COP {g['eps_cl']:.3f}{'' if lo <= g['eps_cl'] <= hi else (' UNDER' if g['eps_cl'] < lo else ' OVER')} | "
              f"shear worst R {g['shear_hm_worstR']['canonical']:.2f}/{g['shear_hm_worstR']['alt']:.2f} {'ok' if g['shear_hm'] else 'X'}"
              f"  =>  {'ALL PASS' if g['full'] else 'no'}" + (f"  [{', '.join(k_ for k_, v_ in g['flags'].items() if v_)}]" if any(g["flags"].values()) else ""))
    WIN = [t for t in TAGS if TAB["pooled"][t]["full"]]
    RB4 = {}
    for t in TAGS:
        mh4 = np.concatenate([PER[(sp, t)]["Mh4"] for sp, _ in SEEDS]); ee4 = np.concatenate([PER[(sp, t)]["eps4"] for sp, _ in SEEDS])
        RB4[f"msck/{t}"] = {nm_: (float(np.median(ee4[(mh4 >= b0) & (mh4 < b1)])) if ((mh4 >= b0) & (mh4 < b1)).any() else None,
                                  int(((mh4 >= b0) & (mh4 < b1)).sum())) for nm_, b0, b1, _ in MBINS}
        P(f"    pooled {t} clearing by environment: " + "; ".join(f"{bn} L {d.get('L', float('nan')):.3f} B {d['B']:.3f}"
                                                               for bn, d in TAB["pooled"][t]["clearing_by_bin"].items())
          + f" | z = 0.4 retention by mass: {RB4[f'msck/{t}']}")
    DIAG = {f"{k_[0]}/{k_[1]}": v_["sw_diag"] for k_, v_ in PER.items()}
    P("    cap diagnostics (max fraction of would-be-switched cells removed by the cap; max switched fraction): "
      + "; ".join(f"{k_}: {d['capped_max']:.3f}/{d['switched_max']:.4f}" for k_, d in list(DIAG.items())[:6]))
    OUT["numbers"].update(table={k_: {t: {kk: vv for kk, vv in g.items()} for t, g in d.items()} for k_, d in TAB.items()}, windows={"msck": WIN},
                          retention_by_mass_z04=RB4, eps_bounds=dict(lo=lo, hi=hi), switch_diagnostics=DIAG,
                          C3=dict(computed=c3, committed={f_: K1c[f_]["worst"] for f_ in c3}),
                          per_box_sums={f"{k_[0]}/{k_[1]}": v_ for k_, v_ in EST.items()},
                          halos={f"{k_[0]}/{k_[1]}": dict(Mh=v_["Mh"], eps=v_["eps"], Mh_z04=v_["Mh4"], eps_z04=v_["eps4"]) for k_, v_ in PER.items()},
                          fields_dir=os.path.relpath(FIELDS, REPO))
    check("W (informational) per-box and pooled gates per kick, clearing by environment and flags, the cap's reach, the retention "
          "used, the z = 0.4 retention by mass", "see tables", True, "reported either way", load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    check("R1 = H: the same-model cell (MOND-sector switch + MS5's cap, the same cap in the dynamics and the shear score) has a pooled "
          "window at some kick in 575-650 km/s", f"pooled window: {WIN or 'none'}", bool(WIN) == EXPECT)

    banner("VERDICT")
    P(f"""  Same model (leak-free MOND-sector switch with MS5's mean-curvature cap in the dynamics AND the shear score), p = 1,
  x_c0 = 2.5, three realisations: pooled window {WIN or 'none'}.  LIMITS: three 100 Mpc/h boxes on a 0.39 Mpc/h mesh; the gate a
  prescribed mask each step; cosmic shear on the halo model is MS3's sufficient bound (isolated halos); v_cap a declared
  constant; the trigger posited.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
