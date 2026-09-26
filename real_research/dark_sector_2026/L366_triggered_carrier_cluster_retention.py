#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L366 -- CLUSTER RETENTION OF THE VIRIALIZATION-TRIGGERED CARRIER UNDER ITS ASSEMBLY HISTORY, and the joint window that
decides L365's candidate.

WHY.  L365 found a narrow window for the virialization-triggered carrier (x_c = 5, v_k ~ 560-720 km/s): S_8, the forest
and halo clearing all pass.  Clusters decide it.  L354 scored X-COP with the carrier decaying at z = 0 in the full-depth
cluster well and needs v_k >= 1000-1200 km/s; for a local trigger that is a proxy of unknown sign -- the carrier decays
earlier in shallower progenitors, but the growing cluster (v_esc ~ 2000-3000 km/s) can recapture daughters kicked at
~700 km/s.  This lane measures the retention directly, in a volume that forms group- and cluster-mass halos.

METHOD: L365's two-species construction, unchanged in physics, in a 100 Mpc/h box with a 256^3 mesh and 192^3 particles
per species -- the SAME trigger resolution (0.39 Mpc/h cells) and particle mass as L365, in 8x the volume.  A bincount
CIC deposit replaces np.add.at for speed (C2 checks it against L362's reference deposit).  Runs: LCDM, trigger-off, and
x_c = 5 at v_k in {550, 600, 650, 700, 850} km/s.
  * HALOS: the 40 highest peaks of the LCDM z = 0 total density (Gaussian-smoothed on 1 Mpc/h, peaks >= 4 Mpc/h apart);
    M(<1 Mpc/h) from the mesh.  Each halo's CARRIER mass within R = 1 Mpc/h (comoving; ~R500 of an X-COP cluster) is
    measured at the same position in every run (same phases), giving the retention eps = M_c,model / M_c,LCDM.
  * THE GATE (L354's committed table read as the X-COP response; the record's criterion is TWO-SIDED, |M_dyn/M_HSE - 1|
    <= 0.2 after the non-thermal correction): clusters pass iff eps_lo <= eps <= eps_hi, where ratio_nt(eps_hi) = 1.2 and
    ratio_nt(eps_lo) = 0.8 on L354's rows, per footing.  Scored on the median over halos with M(<1 Mpc/h) >= 1e14 Msun/h
    AND on the five most massive (X-COP-like) halos.
  * S_8, the forest and halo clearing (L365's G3: dense-cell carrier at z = 2 <= 30% of LCDM's) are re-measured in the
    larger box, so every gate is scored in one volume.
HISTORY (stated, not hidden).  The first run of this script used a ONE-SIDED gate (eps <= eps_hi only) and the pre-run
hypothesis "clusters RECAPTURE: eps > eps_hi, the window closes".  That hypothesis was FALSIFIED: at v_k = 700 km/s the
22 cluster-mass halos keep a median eps = 0.21 (range 0.04-0.68) against eps_hi = 0.77.  The one-sided gate omitted the
record's undershoot side; this version applies the two-sided criterion, adds v_k = 600 and 650 km/s, keeps per-halo
retention against mass, and measures G3 in this box.  Hypothesis for this run (set after the first, before this one):
a JOINT window exists near v_k ~ 600 km/s.
CHECKS
  C1 CONTROL: trigger off reproduces LCDM exactly (retention 1).
  C2 CONTROL: the bincount deposit equals L362's np.add.at deposit on the ICs to 1e-10.
  R1 THE JOINT WINDOW: a kick passing S_8 (strict or alternative), the forest, G3 and the two-sided cluster gate
     (median over >= 1e14 halos, both footings).
  R2 (informational) the same with the five most massive halos only.
MUTATE=2 gives the window runs v_k = 0 (nothing escapes: galaxies keep their carrier, clusters overshoot) -- R1 must flip.

Run from the repository root:  python3 real_research/dark_sector_2026/L366_triggered_carrier_cluster_retention.py
"""
import os, sys, json, math, time
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "g03_audit_2026"))
import L362_forest_pincer_convergence as L2                   # noqa: E402

MUTATE = os.environ.get("MUTATE", "0")
SLUG = "L366_triggered_carrier_cluster_retention"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L366", "mutate": MUTATE, "checks": {}, "numbers": {}}


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


Om, Hnorm, Om_a, ZI, h = L2.Om, L2.Hnorm, L2.Om_a, L2.ZI, L2.h
OB = 0.02237 / h ** 2
WB, WC = OB / Om, 1 - OB / Om
LBOX, NG, NP = 100.0, 256, 192
RHO_M = 2.775e11 * Om                                   # Msun/h per (Mpc/h)^3
EXPECT_WINDOW = True                                    # set after the first run (see HISTORY), before this one


def deposit_fast(s, x, w):
    NGl = s.NG; i0, i1, f = s._cic(x); rho = np.zeros(NGl ** 3)
    for dx in (0, 1):
        wx = f[:, 0] if dx else 1 - f[:, 0]; ix = i1[:, 0] if dx else i0[:, 0]
        for dy in (0, 1):
            wy = f[:, 1] if dy else 1 - f[:, 1]; iy = i1[:, 1] if dy else i0[:, 1]
            for dz in (0, 1):
                wz = f[:, 2] if dz else 1 - f[:, 2]; iz = i1[:, 2] if dz else i0[:, 2]
                rho += np.bincount((ix * NGl + iy) * NGl + iz, weights=w * wx * wy * wz, minlength=NGl ** 3)
    return rho.reshape(NGl, NGl, NGl)


def sigma8(s, delta):
    f = np.fft.fftn(delta); Pw = np.abs(f) ** 2 / s.NG ** 6
    kk = np.sqrt(s.K2); kk[0, 0, 0] = 0; x = kk * 8.0
    with np.errstate(divide="ignore", invalid="ignore"):
        W = np.where(x > 0, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-12) ** 3, 1.0)
    W[0, 0, 0] = 0.0
    return float(np.sqrt(np.sum(Pw * W ** 2)))


def run(cfg):
    name, xc, vk, gamma = cfg
    s = L2.Sim(LBOX, NG, NP)
    s.deposit = lambda x, w: deposit_fast(s, x, w)
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

    a = ai; dlna = 0.02; zs = [3.0, 2.0, 0.0]; out = {}
    rho = density(xb, xcar); ab, ac = accel(rho, a)
    while zs:
        da = a * (np.exp(dlna) - 1); dt = da / (a * Hnorm(a))
        pb += 0.5 * dt * ab; pcar += 0.5 * dt * ac
        xb = (xb + dt * pb / a ** 2) % LBOX; xcar = (xcar + dt * pcar / a ** 2) % LBOX
        a = a + da
        rho = density(xb, xcar)
        if gamma > 0 and cold.any():
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
                if z >= 2.0:
                    kpar, p1d = s.flux_p1d(xb, pb, a, z)
                    rec.update(kpar=kpar.tolist(), p1d=p1d.tolist())
                    rhoc2 = s.deposit(xcar, np.full(n, 1.0)) * NG ** 3 / n
                    dense = rho > 50.0
                    rec["carrier_in_dense"] = float(rhoc2[dense].sum() / max(rho[dense].sum(), 1e-30))
                else:
                    rec["sigma8"] = sigma8(s, rho - 1.0)
                    rhoc = s.deposit(xcar, np.full(n, WC)) * NG ** 3 / n      # carrier density (mean WC)
                    np.save(os.path.join(HERE, f"_L366_{name}_rho.npy"), rho.astype(np.float32))
                    np.save(os.path.join(HERE, f"_L366_{name}_rhoc.npy"), rhoc.astype(np.float32))
                out[str(z)] = rec; zs.remove(z)
    return name, out


def peaks(s, rho, npk=40, sep=4.0):
    sm = s.smooth(rho, 1.0)
    order = np.argsort(sm.ravel())[::-1]
    pts = []
    for flat in order:
        ijk = np.array(np.unravel_index(flat, sm.shape)); pos = (ijk + 0.5) * s.d
        if all(np.linalg.norm(((pos - p_ + LBOX / 2) % LBOX) - LBOX / 2) >= sep for p_ in pts):
            pts.append(pos)
            if len(pts) >= npk:
                break
    return np.array(pts)


def sphere_sum(s, field, pos, R):
    g = (np.arange(NG) + 0.5) * s.d
    d2 = sum(((((g - pos[i] + LBOX / 2) % LBOX) - LBOX / 2) ** 2)[tuple(slice(None) if j == i else None for j in range(3))]
             for i in range(3))
    return float(field[d2 <= R ** 2].sum() * s.d ** 3)


def eps_bounds():
    L4 = json.load(open(os.path.join(HERE, "L354_carrier_lagrangian_additive_window_results.json")))["numbers"]["W1"]["table"]
    out = {}
    for foot in ("canonical", "alt"):
        pts = sorted([(r["eps"], r["ratio_nt"]) for k_, rows in L4.items() if k_.startswith(foot) for r in rows])
        e = np.array([p_[0] for p_ in pts]); r = np.array([p_[1] for p_ in pts])
        cf = np.polyfit(e, r, 1)                                  # ratio_nt vs eps is close to linear across L354's rows
        out[foot] = (float((0.8 - cf[1]) / cf[0]), float((1.2 - cf[1]) / cf[0]))
    return out


if __name__ == "__main__":
    P(__doc__)
    VK = (550.0, 600.0, 650.0, 700.0, 850.0)
    vks = {"0": VK, "2": tuple(0.0 for _ in VK)}[MUTATE]
    if MUTATE != "0":
        P(f"  MUTATE={MUTATE}: the window runs use v_k = {vks[0]:.0f} km/s")
    cfgs = [("lcdm", float("inf"), 0.0, 0.0), ("trigger_off", 5.0, 700.0, 0.0)]
    TAGS = tuple(f"v{int(v)}" for v in VK)
    for tag, vk in zip(TAGS, vks):
        cfgs.append((f"x5_{tag}", 5.0, vk, 10.0))

    # C2 before the heavy runs
    s0 = L2.Sim(LBOX, 64, 48); xr = np.random.default_rng(3).random((20000, 3)) * LBOX; wr = np.random.default_rng(4).random(20000)
    dref = s0.deposit(xr, wr); dfast = deposit_fast(s0, xr, wr)
    c2 = float(np.max(np.abs(dref - dfast)))

    with Pool(len(cfgs)) as pool:
        res = dict(pool.map(run, cfgs))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")

    banner("CONTROLS")
    s = L2.Sim(LBOX, NG, NP)
    rho_l = np.load(os.path.join(HERE, "_L366_lcdm_rho.npy")).astype(float)
    rc_l = np.load(os.path.join(HERE, "_L366_lcdm_rhoc.npy")).astype(float)
    rc_off = np.load(os.path.join(HERE, "_L366_trigger_off_rhoc.npy")).astype(float)
    d1 = float(np.max(np.abs(rc_off - rc_l)))
    check("C1 trigger off (Gamma = 0) reproduces the LCDM carrier field exactly", f"max |difference| = {d1:.1e}", d1 < 1e-5)
    check("C2 the bincount CIC deposit equals L362's np.add.at deposit", f"max |difference| = {c2:.1e}", c2 < 1e-10)

    banner("HALOS AND RETENTION (z = 0, R = 1 Mpc/h)")
    pk = peaks(s, rho_l)
    Mh = np.array([sphere_sum(s, rho_l, p_, 1.0) * RHO_M for p_ in pk])
    Mc_l = np.array([sphere_sum(s, rc_l, p_, 1.0) for p_ in pk])
    P(f"    40 peaks; M(<1 Mpc/h) = {Mh.min():.2e} .. {Mh.max():.2e} Msun/h; >= 1e14: {(Mh >= 1e14).sum()}, >= 5e13: {(Mh >= 5e13).sum()}")
    est = eps_bounds()
    P(f"    X-COP within 20% (L354, two-sided): canonical {est['canonical'][0]:.3f} <= eps <= {est['canonical'][1]:.3f};  "
      f"alt {est['alt'][0]:.3f} <= eps <= {est['alt'][1]:.3f}")
    lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())
    order = np.argsort(Mh)[::-1]; top5 = order[:5]
    sel = Mh >= 1e14
    RET = {}
    for tag in TAGS:
        rc = np.load(os.path.join(HERE, f"_L366_x5_{tag}_rhoc.npy")).astype(float)
        eps = np.array([sphere_sum(s, rc, p_, 1.0) for p_ in pk]) / Mc_l
        r_ = res[f"x5_{tag}"]
        s8r = r_["0.0"]["sigma8"] / res["lcdm"]["0.0"]["sigma8"]
        fdev = 0.0
        for z in ("3.0", "2.0"):
            kp = np.array(res["lcdm"][z]["kpar"]); rr = np.array(r_[z]["p1d"]) / np.array(res["lcdm"][z]["p1d"])
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(rr[m] - 1))))
        g3 = r_["2.0"]["carrier_in_dense"] / max(res["lcdm"]["2.0"]["carrier_in_dense"], 1e-30)
        med, med5 = float(np.median(eps[sel])), float(np.median(eps[top5]))
        RET[tag] = dict(eps_halos=eps.tolist(), median_cl=med, median_top5=med5, s8_ratio=s8r, flux_dev=fdev, G3=g3,
                        s8_strict=s8r >= 0.922, s8_alt=s8r >= 0.899, forest=fdev <= 0.10, cleared=g3 <= 0.30,
                        clusters=lo <= med <= hi, clusters_top5=lo <= med5 <= hi)
        P(f"    v_k {tag[1:]:>4s}: S8 {s8r:.3f}  forest {fdev:.3f}  G3 {g3:.2f}  |  cluster eps median (>=1e14, {sel.sum()}) {med:.2f}, "
          f"top-5 {med5:.2f}  ->  S8 {'ok' if s8r >= 0.922 else ('alt' if s8r >= 0.899 else 'FAIL')}, forest {'ok' if fdev <= 0.1 else 'FAIL'}, "
          f"cleared {'yes' if g3 <= 0.3 else 'NO'}, clusters {'ok' if lo <= med <= hi else ('OVER' if med > hi else 'UNDER')} (top-5 "
          f"{'ok' if lo <= med5 <= hi else ('OVER' if med5 > hi else 'UNDER')})")
    P("    per-halo retention vs mass at v_k 600/650/700 (the 10 most massive): " + "; ".join(
        f"{Mh[i]:.1e}: " + "/".join(f"{RET[t]['eps_halos'][i]:.2f}" for t in ('v600', 'v650', 'v700')) for i in order[:10]))
    OUT["numbers"].update(halo_mass=Mh.tolist(), eps_bounds=est, retention=RET, runs={k_: v for k_, v in res.items()})
    for tag in ("lcdm", "trigger_off") + tuple(f"x5_{t}" for t in TAGS):
        for f_ in ("rho", "rhoc"):
            try:
                os.remove(os.path.join(HERE, f"_L366_{tag}_{f_}.npy"))
            except OSError:
                pass

    banner("R1  THE JOINT WINDOW")
    joint_s = [t for t in TAGS if RET[t]["s8_strict"] and RET[t]["forest"] and RET[t]["cleared"] and RET[t]["clusters"]]
    joint_a = [t for t in TAGS if RET[t]["s8_alt"] and RET[t]["forest"] and RET[t]["cleared"] and RET[t]["clusters"]]
    top_a = [t for t in TAGS if RET[t]["s8_alt"] and RET[t]["forest"] and RET[t]["cleared"] and RET[t]["clusters_top5"]]
    has = bool(joint_s or joint_a)
    OUT["numbers"]["verdict"] = dict(lo=lo, hi=hi, joint_strict=joint_s, joint_alt=joint_a, joint_alt_top5=top_a)
    check(f"R1 {'A JOINT WINDOW EXISTS' if EXPECT_WINDOW else 'NO JOINT WINDOW'}: a kick passing S_8, the forest, halo clearing and the "
          "two-sided cluster gate (median over >= 1e14 Msun/h halos, both footings) in one volume",
          f"strict {joint_s or 'none'}; alternative {joint_a or 'none'}", has == EXPECT_WINDOW,
          "hypothesis set after the first (one-sided) run, before this one -- see HISTORY")
    check("R2 (informational) the joint window scored on the five most massive (X-COP-like) halos",
          f"alternative-threshold window with top-5 clusters: {top_a or 'none'}", True, "reported either way", load_bearing=False)

    banner("VERDICT")
    P(f"""  Two-sided X-COP gate on the cluster retention: {lo:.2f} <= eps <= {hi:.2f}.  Joint window (S_8, forest, halo clearing,
  clusters): strict {joint_s or 'none'}, alternative {joint_a or 'none'} (top-5 clusters: {top_a or 'none'}).
  LIMITS: 100 Mpc/h box, 0.39 Mpc/h mesh, 1 Mpc/h aperture, L354's X-COP response as the map from retention to M_dyn/M_HSE,
  MOND on baryons inside halos not modelled, one realisation.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'' if MUTATE == '0' else '_MUTATE'}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
