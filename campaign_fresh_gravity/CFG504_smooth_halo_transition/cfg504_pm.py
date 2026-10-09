#!/usr/bin/env python3
"""CFG504 halo catalogues and per-halo particle pair-count profiles on our own S0 (LCDM-equivalent) PM snapshots, z = 0
(FROZEN_CRITERIA.md sections 2-3, 7; criteria commit 333a5fce4). No lensing data are read here.

Finder (frozen): spherical overdensity at Delta_ta (run JSON) on particles, seeded by local maxima (3x3x3, periodic) of the CIC density
on the run's mesh with rho/rho_bar > 20; centre = CoM of particles within one mesh cell of the seed, iterated twice; M_ta from the
particle counts on 50 log radii 0.5 cell .. 12 Mpc/h; de-duplicated heavier-first within the larger r_ta; keep log M_ta >= 12.3.
Implementation detail (disclosed): before centre refinement, seeds are pre-screened with M_ta measured around the seed cell centre,
keeping log M_ta >= 12.0 (0.3 dex margin); M_ta is then re-measured at the refined centre.
Profiles: per halo, cumulative pair counts on 49 log edges 0.15-20 Mpc/h (periodic dual-tree counts), at most 1000 halos per bin.
MUTATE SHUF (cfg411 512^3 only): the same catalogue against uniform random particle positions (seed 504), resolved bins only.
Output: ../../../_external_data/cfg504_work/cfg504_pm_<run>.npz ; cfg504_pm.out ; cfg504_pm_results.json
Run: nice -n 15 python3 -u cfg504_pm.py   (4 forked worker processes; one 512^3 load at a time)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import math, json, time, subprocess
import multiprocessing as mp_
import numpy as np
from scipy.ndimage import maximum_filter
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg504_work")
os.makedirs(WORK, exist_ok=True)
RUNS = [("S0_512_a", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512", True),
        ("S0_512_b", "cfg424_work/cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360", False),
        ("S0_256_s360", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360", False),
        ("S0_256_s361", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed361", False),
        ("S0_256_s359", "cfg359_work/cfg359_S0_FLAT_canonical_N256", False)]
ONLY = os.environ.get("CFG504_RUNS")                     # optional comma list of run names (for resuming)
h = 0.6736
OMPM = (0.02237 + 0.1200) / h ** 2
RHOM_H = OMPM * 2.77536627e11                           # (Msun/h) / (Mpc/h)^3
BINS = [("U1", 12.3, 12.6), ("U2", 12.6, 12.9), ("U3", 12.9, 13.2), ("U4", 13.2, 13.5),
        ("R1", 13.5, 13.8), ("R2", 13.8, 14.1), ("R3", 14.1, 14.4), ("R4", 14.4, 15.2)]
EDGES = np.geomspace(0.15, 20.0, 49)
NMAX = 1000
T0 = time.time()
LOG = []
RES = {"lane": "CFG504", "script": "cfg504_pm", "runs": {}, "checks": {}}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def no_other_512():
    r = subprocess.run(["pgrep", "-f", "N512|512 0 MIXA|cfg4[0-9][0-9]_pm.py .* 512"], capture_output=True, text=True)
    pids = [p for p in r.stdout.split() if p.strip() and int(p) != os.getpid()]
    return len(pids) == 0, pids


def cic3(pos, N, L):                                     # CFG502's CIC (copied)
    x = pos / (L / N); i0 = np.floor(x).astype(np.int64); d = x - i0
    rho = np.zeros(N ** 3)
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (d[:, 0] if dx else 1 - d[:, 0]) * (d[:, 1] if dy else 1 - d[:, 1]) * (d[:, 2] if dz else 1 - d[:, 2])
                idx = (((i0[:, 0] + dx) % N) * N + (i0[:, 1] + dy) % N) * N + (i0[:, 2] + dz) % N
                rho += np.bincount(idx, weights=w, minlength=N ** 3)
    return rho.reshape(N, N, N)


def so_mass(tree, cen, L, cell, Dta, mp, rg):
    """M_ta, r_ta (and M200m, r200m) from particle counts on radii rg, progressive (only seeds still above Delta_ta are queried)."""
    n = len(cen)
    dens = np.full((n, len(rg)), np.nan)
    active = np.arange(n)
    for j, r in enumerate(rg):
        if len(active) == 0:
            break
        c = tree.query_ball_point(cen[active], r, return_length=True, workers=4)
        dens[active, j] = c * mp / (4 * math.pi / 3 * r ** 3) / RHOM_H
        active = active[dens[active, j] >= Dta]
    out = {}
    for lab, D in (("ta", Dta), ("200m", 200.0)):
        M = np.zeros(n); R = np.zeros(n)
        for i in range(n):
            dd = dens[i]
            ok = np.isfinite(dd)
            if not ok[0] or dd[0] < D:
                continue
            below = np.where(ok & (dd < D))[0]
            if len(below) == 0:
                continue
            j = below[0]
            f = (math.log(dd[j - 1]) - math.log(D)) / (math.log(dd[j - 1]) - math.log(dd[j]))
            R[i] = math.exp(math.log(rg[j - 1]) + f * (math.log(rg[j]) - math.log(rg[j - 1])))
            M[i] = D * RHOM_H * 4 * math.pi / 3 * R[i] ** 3
        out[lab] = (M, R)
    return out


_TREE = None
_L = None


def _count_one(c):
    t1 = cKDTree(np.asarray(c, float)[None, :], boxsize=_L)
    return t1.count_neighbors(_TREE, EDGES).astype(np.int64)


def per_halo_counts(tree, cen, L):
    global _TREE, _L
    _TREE, _L = tree, L
    ctx = mp_.get_context("fork")
    with ctx.Pool(4) as pool:
        out = pool.map(_count_one, list(cen), chunksize=4)
    return np.array(out)


def cfg502_peaks(pos, tree, L, N, Dta, mp):
    """CFG502's peak code (copied from cfg502_pm.py) for control C10: cell-centre peaks, M_ta from 80 radii 0.15-6 Mpc/h, dedup."""
    rho = cic3(pos, N, L); rho /= rho.mean()
    pk = (rho == maximum_filter(rho, size=3, mode="wrap")) & (rho > 20.0)
    cand = (np.argwhere(pk) + 0.5) * (L / N)
    rg = np.geomspace(0.15, 6.0, 80)
    cnt = np.array([[len(x) for x in tree.query_ball_point(cand, rr_, workers=4)] for rr_ in rg]).T
    dens = cnt * mp / (4 * math.pi / 3 * rg ** 3) / RHOM_H
    Mta = np.zeros(len(cand)); rta = np.zeros(len(cand))
    for i in range(len(cand)):
        above = dens[i] >= Dta
        if not above[0]:
            continue
        j = int(np.argmin(above)) if not above.all() else len(rg) - 1
        if j == 0:
            continue
        f = (math.log(dens[i, j - 1]) - math.log(Dta)) / (math.log(dens[i, j - 1]) - math.log(dens[i, j]))
        rta[i] = math.exp(math.log(rg[j - 1]) + f * (math.log(rg[j]) - math.log(rg[j - 1])))
        Mta[i] = Dta * RHOM_H * 4 * math.pi / 3 * rta[i] ** 3
    ok = Mta > 0
    cand, Mta, rta = cand[ok], Mta[ok], rta[ok]
    o = np.argsort(-Mta); cand, Mta, rta = cand[o], Mta[o], rta[o]
    keep = np.ones(len(cand), bool); tc = cKDTree(cand, boxsize=L)
    for i in range(len(cand)):
        if not keep[i]:
            continue
        for j in tc.query_ball_point(cand[i], rta[i]):
            if j > i:
                keep[j] = False
    return cand[keep], Mta[keep]


def run_one(name, base, do_shuf):
    t = time.time()
    J = json.load(open(os.path.join(EXT, base + ".json")))
    L = float(J["L"]); N = int(J["mesh"]); Dta = float(J["snap"]["z0"]["Delta_ta"])
    if N >= 512:
        ok, pids = no_other_512()
        if not ok:
            P(f"[{name}] another 512^3 job is running (pids {pids}); waiting is not automated -> SKIPPED")
            return None
    pos = np.load(os.path.join(EXT, base + "_z0.npz"))["pos"].astype(np.float64)
    pos %= L
    NP = len(pos); mp = RHOM_H * L ** 3 / NP; cell = L / N
    rho = cic3(pos, N, L); rho /= rho.mean()
    pk = (rho == maximum_filter(rho, size=3, mode="wrap")) & (rho > 20.0)
    seeds = (np.argwhere(pk) + 0.5) * cell
    del rho
    P(f"\n[{name}] N {NP:,}, mesh {N} (cell {cell:.3f} Mpc/h), m_p {mp:.3e} Msun/h, Delta_ta {Dta:.3f}; seeds {len(seeds)} "
      f"({time.time() - t:.0f} s)")
    tree = cKDTree(pos, boxsize=L, leafsize=32, balanced_tree=False, compact_nodes=False)
    rg = np.geomspace(0.5 * cell, 12.0, 50)
    so0 = so_mass(tree, seeds, L, cell, Dta, mp, rg)
    pre = so0["ta"][0] >= 10 ** 12.0
    cen = seeds[pre]
    P(f"  pre-screen (log M_ta >= 12.0 at the seed cell centre): {pre.sum()} seeds ({time.time() - t:.0f} s)")
    for it in range(2):
        lists = tree.query_ball_point(cen, cell, workers=4)
        newc = np.empty_like(cen)
        for i, li in enumerate(lists):
            if len(li) == 0:
                newc[i] = cen[i]; continue
            d = pos[li] - cen[i]
            d -= L * np.round(d / L)
            newc[i] = (cen[i] + d.mean(0)) % L
        cen = newc
    so = so_mass(tree, cen, L, cell, Dta, mp, rg)
    Mta, rta = so["ta"]; M200m, r200m = so["200m"]
    ok = Mta > 0
    cen, Mta, rta, M200m, r200m = cen[ok], Mta[ok], rta[ok], M200m[ok], r200m[ok]
    o = np.argsort(-Mta); cen, Mta, rta, M200m, r200m = cen[o], Mta[o], rta[o], M200m[o], r200m[o]
    keep = np.ones(len(cen), bool); tc = cKDTree(cen, boxsize=L)
    for i in range(len(cen)):
        if not keep[i]:
            continue
        for j in tc.query_ball_point(cen[i], rta[i]):
            if j > i:
                keep[j] = False
    cen, Mta, rta, M200m, r200m = cen[keep], Mta[keep], rta[keep], M200m[keep], r200m[keep]
    lM = np.log10(Mta)
    m = lM >= 12.3
    cen, Mta, rta, M200m, r200m, lM = cen[m], Mta[m], rta[m], M200m[m], r200m[m], lM[m]
    P(f"  catalogue: {len(cen)} halos with log M_ta >= 12.3 after refinement + de-duplication ({time.time() - t:.0f} s)")
    rng = np.random.default_rng(504)
    sel = {}; rec = {}
    for lab, a, b in BINS:
        ii = np.where((lM >= a) & (lM < b))[0]
        nall = len(ii)
        if len(ii) > NMAX:
            ii = np.sort(rng.choice(ii, NMAX, replace=False))
        sel[lab] = ii
        rmed = float(np.median(rta[ii])) if len(ii) else float("nan")
        rec[lab] = dict(n_all=int(nall), n_used=int(len(ii)), r_ta_median=rmed, logM_ta_median=float(np.median(lM[ii])) if len(ii) else None,
                        resolved=bool(len(ii) > 0 and rmed >= 5 * cell),
                        r200m_over_rta_median=float(np.median((r200m[ii] / rta[ii])[r200m[ii] > 0])) if len(ii) and (r200m[ii] > 0).any() else None)
        P(f"  bin {lab} {a}-{b}: {nall} halos (used {len(ii)}), median r_ta {rmed:.2f} Mpc/h = {rmed / cell:.1f} cells, "
          f"{'RESOLVED' if rec[lab]['resolved'] else 'unresolved'}; median r200m / r_ta {rec[lab]['r200m_over_rta_median']}")
    allsel = np.unique(np.concatenate([sel[l] for l, _, _ in BINS]))
    cnt = per_halo_counts(tree, cen[allsel], L)
    P(f"  per-halo counts for {len(allsel)} halos done ({time.time() - t:.0f} s)")
    out = dict(cen=cen, Mta=Mta, rta=rta, M200m=M200m, r200m=r200m, sel_idx=allsel, counts=cnt, nbar=NP / L ** 3, L=L, cell=cell,
               Dta=Dta, mp=mp, EDGES=EDGES)
    for lab, _, _ in BINS:
        out[f"bin_{lab}"] = sel[lab]
    # control C11 (reported): per-halo counts sum = one dual-tree count of the same halos (top non-empty bin)
    labs = [l for l, _, _ in BINS if len(sel[l])]
    lt = labs[-1]
    th = cKDTree(cen[sel[lt]], boxsize=L)
    direct = th.count_neighbors(tree, EDGES).astype(np.int64)
    summed = cnt[np.searchsorted(allsel, sel[lt])].sum(0)
    c11 = float(np.max(np.abs(direct - summed) / np.maximum(direct, 1)))
    RES["checks"][f"C11_{name}"] = dict(ok=c11 < 1e-9, load_bearing=False, msg=f"bin {lt}: max rel {c11:.1e}")
    P(f"  [{'PASS' if c11 < 1e-9 else 'FAIL'}] C11 (reported) per-halo counts sum = dual-tree count, bin {lt}: max rel {c11:.1e}")
    # control C10 (load-bearing) on the 256^3 seed360 run
    if name == "S0_256_s360":
        c2, M2 = cfg502_peaks(pos, tree, L, N, Dta, mp)
        s2 = np.log10(M2) >= 13.3
        tm = cKDTree(c2[s2], boxsize=L)
        mine = lM >= 13.3
        dd, jj = tm.query(cen[mine], distance_upper_bound=cell)
        okm = np.isfinite(dd)
        dl = np.abs(lM[mine][okm] - np.log10(M2[s2][jj[okm]]))
        med = float(np.median(dl)) if okm.any() else float("inf")
        ok10 = med < 0.05
        RES["checks"]["C10"] = dict(ok=bool(ok10), load_bearing=True,
                                    msg=f"{okm.sum()} of {mine.sum()} halos (log M_ta >= 13.3) matched within 1 cell to CFG502 peaks; "
                                        f"median |d log M_ta| {med:.4f} dex (90th pct {float(np.percentile(dl, 90)) if okm.any() else float('nan'):.3f})")
        P(f"  [{'PASS' if ok10 else 'FAIL'}] C10 finder vs CFG502 peak code: {RES['checks']['C10']['msg']}")
    del tree
    if do_shuf:
        rs = np.random.default_rng(504)
        pos = rs.uniform(0.0, L, size=(NP, 3))
        tree = cKDTree(pos, boxsize=L, leafsize=32, balanced_tree=False, compact_nodes=False)
        rsel = np.unique(np.concatenate([sel[l] for l, _, _ in BINS if rec[l]["resolved"]]))
        out["shuf_idx"] = rsel
        out["shuf_counts"] = per_halo_counts(tree, cen[rsel], L)
        P(f"  MUTATE SHUF: uniform random particles (seed 504), {len(rsel)} resolved-bin halos counted ({time.time() - t:.0f} s)")
        del tree
    del pos
    np.savez(os.path.join(WORK, f"cfg504_pm_{name}.npz"), **out)
    RES["runs"][name] = dict(base=os.path.basename(base), L=L, mesh=N, cell=cell, m_p=mp, Delta_ta=Dta, n_halos=int(len(cen)), bins=rec,
                             elapsed_s=round(time.time() - t, 1))
    P(f"  [{name}] done ({time.time() - t:.0f} s)")
    return True


if __name__ == "__main__":
    prev = os.path.join(HERE, "cfg504_pm_results.json")
    if ONLY and os.path.exists(prev):
        RES = json.load(open(prev))
    for name, base, shuf in RUNS:
        if ONLY and name not in ONLY.split(","):
            continue
        run_one(name, base, shuf)
        json.dump(RES, open(prev, "w"), indent=1)
    RES["elapsed_s"] = round(time.time() - T0, 1)
    json.dump(RES, open(prev, "w"), indent=1)
    with open(os.path.join(HERE, "cfg504_pm.out"), "a" if ONLY else "w") as f:
        f.write("\n".join(LOG) + "\n")
    bad = [k for k, c in RES["checks"].items() if c["load_bearing"] and not c["ok"]]
    sys.exit(1 if bad else 0)
