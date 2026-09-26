#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L379 -- WHAT THE CLEARING GATE MEASURES: the z = 2 dense-cell carrier split by environment.  Is the clearing-vs-clusters
pinch a GALAXY constraint or a PROTOCLUSTER one?

WHY.  L369/L378: pooled over three realisations, the triggered carrier has no window -- clearing (G3: the carrier in cells
with 1 + delta > 50 at z = 2, relative to LCDM's, on the 0.39 Mpc/h mesh) needs kicks >= 725 km/s, X-COP clusters need
<= ~680.  G3 was introduced for RC100 (galaxies at z ~ 1-2.5 must sit in cleared halos) and KiDS (L365); both targets pass
when resolved (L376: 0.000 of LCDM's carrier inside R_e at z = 1-2; L375).  The G3 values themselves move with the kick
in every box (L369, box (17, 21): 0.72 -> 0.39 over 600-750 km/s), so the dense-cell carrier is retained DAUGHTERS, and the
densest cells at z = 2 on this mesh are plausibly protocluster cores -- the progenitors of the very clusters X-COP needs to
keep carrier.  If so, the pinch sets unobserved z = 2 protocluster cores against z = 0 clusters, and G3 is not measuring
RC100's galaxies.  This lane measures it.

SETUP: L377's run() with ONE change -- the z = 2 total and carrier fields are also saved (the source is transformed and the
replacement asserted to occur exactly once; C1 checks the arithmetic is untouched).  Full construction, canonical a_0,
v_k = 675 and 700 km/s, L369's three realisations, a LCDM run each (9 runs).  Every dense cell (1 + delta > 50, the
run's own field, as G3) is assigned to its nearest LCDM peak at z = 2 (periodic), and binned by that peak's mass within
0.5 Mpc/h comoving (~ r_200 of a 1e13 Msun halo at z = 2): galaxy (< 3e12), massive galaxy / group (3e12 - 1e13),
protocluster core (>= 1e13 Msun/h).  Two clearing measures per bin:
  (a) the record's G3: the run's carrier fraction in ITS OWN dense cells of that bin / LCDM's (as L365-L378);
  (b) fixed cells: the carrier mass the run keeps in LCDM's dense cells of that bin / LCDM's carrier there -- the fraction of
      LCDM's dense-region carrier still in place.
HISTORY.  A 128^3 code test (no physics result) showed that (a) drops cleared cells: where the carrier leaves, the cell's
density falls below 50 and it leaves the model's dense set, so (a) is computed over the cells that KEPT their carrier -- a
selection toward retaining regions.  Measure (b) was added, and made the hypothesis's measure, before the main run.
PRE-DECLARED (before the main run): H: pooled over the three boxes at 700 km/s, on the fixed-cell measure (b), the galaxy and
group environments (< 1e13) are cleared (<= 0.30) and the protocluster environment is not (> 0.30).
CHECKS
  C1 CONTROL: the overall G3 per box at 675 and 700 reproduces L378's committed values exactly.
  C2 CONTROL: the bins partition the dense cells (bin masses sum to the total, every run).
  R1 = H.  W (informational): both measures by bin, per box and pooled, at 675 and 700; the dense-cell mass share of each bin.
MUTATE=1: v_k = 0 (the decayed carrier stays): the galaxy bins are not cleared and R1 must FAIL (rc = 1).
L379_POOL sets the pool size (default 9).

Run from the repository root:  python3 real_research/dark_sector_2026/L379_clearing_by_environment.py
"""
import os, sys, json, math, time, inspect, tempfile, shutil
import numpy as np
from multiprocessing import Pool
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import L377_full_construction_pm as L77                        # noqa: E402  (L377's full-construction run)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L379_clearing_by_environment"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L379", "mutate": MUTATE, "checks": {}, "numbers": {}}
L6, L7, L2 = L77.L6, L77.L7, L77.L2
LBOX, NG, NP, RHO_M = L77.LBOX, L77.NG, L77.NP, L77.RHO_M
SEEDS = ((7, 11), (17, 21), (29, 33))
VK = (675.0, 700.0)
TAGS = tuple(f"v{int(v)}" for v in VK)
BINS = (("galaxy", 0.0, 3e12), ("group", 3e12, 1e13), ("protocluster", 1e13, 1e18))

# ---------------------------------------------------------------------------------- L377's run, plus the z = 2 fields
_SRC = inspect.getsource(L77.run)
_OLD = """                    rec["carrier_in_dense"] = float(rhoc2[dense].sum() / max(rho[dense].sum(), 1e-30))
"""
_NEW = _OLD + """                    if z == 2.0:
                        np.save(os.path.join(tmp, f"{name}_z2_rho.npy"), rho.astype(np.float32))
                        np.save(os.path.join(tmp, f"{name}_z2_rhoc.npy"), rhoc2.astype(np.float32))
"""
assert _SRC.count(_OLD) == 1
exec(compile(_SRC.replace(_OLD, _NEW).replace("def run(cfg):", "def run_z2(cfg):", 1), "L377.run+z2", "exec"), L77.__dict__)
run_z2 = L77.run_z2


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


if __name__ == "__main__":
    P(__doc__)
    TMP = tempfile.mkdtemp(prefix="L379_")
    cfgs = []
    for sp, sk in SEEDS:
        cfgs.append((f"s{sp}_lcdm", sp, sk, float("inf"), 0.0, 0.0, TMP, "none", L77.A0["canonical"]))
        cfgs += [(f"s{sp}_{t}", sp, sk, L77.XC_TRIG, 0.0 if MUTATE else v, 10.0, TMP, "full", L77.A0["canonical"])
                 for t, v in zip(TAGS, VK)]
    if MUTATE:
        P("  MUTATE: v_k = 0 in every decaying run")
    with Pool(int(os.environ.get("L379_POOL", "9"))) as pool:
        res = dict(pool.map(run_z2, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")

    banner("C1  CONTROL: the overall clearing per box reproduces L378")
    R78 = json.load(open(os.path.join(HERE, "L378_full_construction_pooled_results.json")))["numbers"]["table"]
    g3 = {(sp, t): res[f"s{sp}_{t}"]["2.0"]["carrier_in_dense"] / max(res[f"s{sp}_lcdm"]["2.0"]["carrier_in_dense"], 1e-30) for sp, _ in SEEDS for t in TAGS}
    if not MUTATE:
        dev = max(abs(g3[(sp, t)] / R78[str(sp)][t]["G3"] - 1) for sp, _ in SEEDS for t in TAGS)
        check("C1 the overall z = 2 clearing per box at 675 and 700 km/s reproduces L378's committed values (same code path)",
              f"max relative deviation {dev:.1e} over 6 numbers", dev < 1e-9)
    else:
        dev = abs(res["s7_lcdm"]["0.0"]["sigma8"] / json.load(open(os.path.join(HERE, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]["runs"]["lcdm"]["0.0"]["sigma8"] - 1)
        check("C1 the (7, 11) LCDM run reproduces L366's sigma_8", f"relative deviation {dev:.1e}", dev < 1e-9)

    banner("THE DENSE-CELL CARRIER AT z = 2 BY ENVIRONMENT")
    s = L2.Sim(LBOX, NG, NP)
    ld = lambda nm, f: np.load(os.path.join(TMP, f"{nm}_z2_{f}.npy")).astype(float)
    ACC = {t: {b[0]: [0.0, 0.0, 0.0, 0.0] for b in BINS} for t in TAGS}      # (a): [carrier_model, rho_model, carrier_lcdm, rho_lcdm]
    ACCF = {t: {b[0]: [0.0, 0.0] for b in BINS} for t in TAGS}               # (b): [model carrier in LCDM's cells, LCDM carrier there]
    PER = {}; part_dev = 0.0
    for sp, _ in SEEDS:
        L = f"s{sp}_lcdm"; rl, cl = ld(L, "rho"), ld(L, "rhoc")
        pk = L7.peaks_fast(s, rl, npk=4000, sep=1.0)
        Mp = np.array([L6.sphere_sum(s, rl, p_, 0.5) * RHO_M for p_ in pk])
        tree = cKDTree(pk, boxsize=LBOX)

        def binned(rho, rc):
            dense = (rho > 50.0).ravel(); idx = np.where(dense)[0]
            _, j = tree.query((np.array(np.unravel_index(idx, rho.shape)).T + 0.5) * s.d); m = Mp[j]
            out = {}
            for bn, b0, b1 in BINS:
                sel = idx[(m >= b0) & (m < b1)]
                out[bn] = (float(rc.ravel()[sel].sum()), float(rho.ravel()[sel].sum()), int(len(sel)))
            tot = (float(rc.ravel()[idx].sum()), float(rho.ravel()[idx].sum()))
            return out, tot

        idxl = np.where((rl > 50.0).ravel())[0]                      # LCDM's dense cells: the fixed cells of measure (b)
        _, jl = tree.query((np.array(np.unravel_index(idxl, rl.shape)).T + 0.5) * s.d); ml = Mp[jl]
        FIX = {bn: idxl[(ml >= b0) & (ml < b1)] for bn, b0, b1 in BINS}
        bl, tl = binned(rl, cl)
        part_dev = max(part_dev, abs(sum(v[1] for v in bl.values()) - tl[1]) / max(tl[1], 1e-30))
        PER[str(sp)] = {}
        for t in TAGS:
            rm_, cm_ = ld(f"s{sp}_{t}", "rho"), ld(f"s{sp}_{t}", "rhoc")
            bm, tm = binned(rm_, cm_)
            fixm = {bn: float(cm_.ravel()[FIX[bn]].sum()) for bn in FIX}; fixl = {bn: float(cl.ravel()[FIX[bn]].sum()) for bn in FIX}
            part_dev = max(part_dev, abs(sum(v[1] for v in bm.values()) - tm[1]) / max(tm[1], 1e-30))
            PER[str(sp)][t] = {}
            for bn, _, _ in BINS:
                for k_, v_ in enumerate((bm[bn][0], bm[bn][1], bl[bn][0], bl[bn][1])):
                    ACC[t][bn][k_] += v_
                ACCF[t][bn][0] += fixm[bn]; ACCF[t][bn][1] += fixl[bn]
                g = (bm[bn][0] / max(bm[bn][1], 1e-30)) / max(bl[bn][0] / max(bl[bn][1], 1e-30), 1e-30) if bl[bn][1] > 0 and bm[bn][1] > 0 else float("nan")
                PER[str(sp)][t][bn] = dict(G3=g, fixed=fixm[bn] / fixl[bn] if fixl[bn] > 0 else float("nan"), n_cells_model=bm[bn][2],
                                           n_cells_lcdm=bl[bn][2], mass_share_lcdm=bl[bn][1] / max(tl[1], 1e-30))
            P(f"    box ({sp:2d}) {t}: " + "; ".join(f"{bn}: (b) {PER[str(sp)][t][bn]['fixed']:.2f}, (a) {PER[str(sp)][t][bn]['G3']:.2f} "
                                                   f"[cells {PER[str(sp)][t][bn]['n_cells_model']}/{PER[str(sp)][t][bn]['n_cells_lcdm']}, "
                                                   f"LCDM dense-mass share {PER[str(sp)][t][bn]['mass_share_lcdm']:.2f}]" for bn, _, _ in BINS)
              + f"  | overall (a) {g3[(sp, t)]:.2f}")
    shutil.rmtree(TMP, ignore_errors=True)
    check("C2 the environment bins partition the dense cells (bin masses sum to the dense total in every run)",
          f"max relative deviation {part_dev:.1e}", part_dev < 1e-9)

    POOL = {t: {bn: ((a[0] / a[1]) / max(a[2] / max(a[3], 1e-30), 1e-30) if a[1] > 0 else float("nan")) for bn, a in ACC[t].items()} for t in TAGS}
    POOLF = {t: {bn: a[0] / max(a[1], 1e-30) for bn, a in ACCF[t].items()} for t in TAGS}
    for t in TAGS:
        P(f"    POOLED {t}: " + "; ".join(f"{bn}: (b) fixed cells {POOLF[t][bn]:.3f}, (a) own dense set {POOL[t][bn]:.3f}" for bn in POOL[t]))
    OUT["numbers"].update(per_box=PER, pooled_a=POOL, pooled_b_fixed=POOLF, overall_a=({f"{sp}/{t}": v for (sp, t), v in g3.items()}))
    check("W (informational) G3 by environment per box and pooled at 675 and 700 km/s", "see tables", True, "reported either way",
          load_bearing=False)

    banner("R1  THE HYPOTHESIS (set before the run)")
    p7 = POOLF["v700"]
    check("R1 = H: pooled at 700 km/s on the fixed-cell measure (b), the galaxy and group environments are cleared (<= 0.30) and "
          "the protocluster environment is not (> 0.30)", f"galaxy {p7['galaxy']:.3f}, group {p7['group']:.3f}, protocluster {p7['protocluster']:.3f}",
          p7["galaxy"] <= 0.30 and p7["group"] <= 0.30 and p7["protocluster"] > 0.30)

    banner("VERDICT")
    P(f"""  Pooled fixed-cell clearing at 700 km/s by environment: galaxy {p7['galaxy']:.3f}, group {p7['group']:.3f}, protocluster
  {p7['protocluster']:.3f}; the record's own-dense-set G3: {', '.join(f"{bn} {v:.3f}" for bn, v in POOL['v700'].items())}.
  LIMITS: 0.39 Mpc/h mesh; environments from the nearest LCDM peak's mass within 0.5 Mpc/h at z = 2; the full construction
  of L377 (switch on the matter-only branch, trigger posited).""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
