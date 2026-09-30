#!/usr/bin/env python3
"""CFG221 v2 -- the SECONDARY decision rule for the pooled z > 3.5 two-sided test, and its operating characteristics on mocks.
Frozen criteria: FROZEN_CRITERIA_V2.md here (e0a9be1b4), committed before v2 was run on anything; v1 (FROZEN_CRITERIA.md + addenda, lane 251985c27) stays the PRIMARY rule.
v2 changes the verdict only: the primary cell (nu_mono, canonical) alone; a ONE-SIDED 5% marginal bound per law (the 95th percentile of the resampled medians below 0 = DISFAVOURED-under,
the 5th percentile above 0 = DISFAVOURED-over); B = 10,000 everywhere; the other three kernel/footing cells and the leave-one-out fits are REPORTED, not conditions.
Both verdicts are always shown side by side and v1 governs any headline.  Judged by the SAME controls, C2 above all; if v2 fails C2 that is recorded and the iteration stops (no v3).
kappa = 1/2 FITTED, NOT DERIVED.  A description of THIS rule on THIS template, not a claim about any real sample.  No sentence says the data favour a framework.
Run:  python3 campaign_fresh_gravity/CFG221_z35_decision_rule/cfg221_v2.py        (MUTATE=1 runs only the response control)
"""
import os, sys, json, math, time
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
MUT = os.environ.get("MUTATE", "").strip() == "1"
import cfg221_decision_rule as M                     # the shared generator and definitions (its driver sits under __main__); it pops MUTATE from the environment itself

SFX = "_MUTATE" if MUT else ""
B2 = 10_000
PRIM = ("nu_mono", "canonical")
NG2 = (6, 13, 20, 36, 50)


def stat_v2(m):
    lo5, hi95 = np.percentile(m, [5, 95])
    return "under" if hi95 < 0 else ("over" if lo5 > 0 else "not")


def statuses_v2(mock, laws, B, rng, sigma=M.SIGMA, cells=None):
    """status of each law in each requested cell from one marginal bootstrap; also the two-sided 95% CI edges (for C4) in the primary cell."""
    N = len(mock["gobs"])
    IB = rng.integers(0, N, size=(B, N))
    ck = rng.normal(0, 1, (B, 3)) * sigma[None, :]
    cc = np.take_along_axis(ck, mock["cls"][IB], axis=1)
    gbar = (mock["Ms"][IB] + mock["Mg"][IB] * 10 ** cc) * mock["cg"][IB]
    D = mock["gobs"][IB] / gbar
    res, edges = {}, {}
    for cell in (cells or M.CELLS):
        nu, a0 = M.NUF[cell[0]], M.A0S[cell[1]]
        for law in laws:
            m = np.median(np.log10(D / nu(gbar / (a0 * mock["F"][law][IB]))), axis=1)
            res[(cell, law)] = stat_v2(m)
            edges[(cell, law)] = (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))
    return res, edges


def verdict2(res, lo_law, hi_law, cell=PRIM):
    if res[(cell, hi_law)] == "under" and res[(cell, lo_law)] == "not":
        return "LO"
    if res[(cell, lo_law)] == "over" and res[(cell, hi_law)] == "not":
        return "HI"
    return "NONE"


def rule2(mock, lo_law, hi_law, B, rng, sigma=M.SIGMA, robust=True):
    """the v2 verdict (primary cell) and, when it is a separation and robust=True, the REPORTED robustness: all four cells agree; leave-one-out survives."""
    res, _ = statuses_v2(mock, (lo_law, hi_law), B, rng, sigma)
    v = verdict2(res, lo_law, hi_law)
    cells_ok = loo_ok = None
    if v != "NONE" and robust:
        cells_ok = all(verdict2(res, lo_law, hi_law, c) == v for c in M.CELLS)
        N = len(mock["gobs"])
        loo_ok = True
        for j in range(N):
            r2, _ = statuses_v2(M.drop(mock, np.arange(N) != j), (lo_law, hi_law), B, rng, sigma, cells=[PRIM])
            if verdict2(r2, lo_law, hi_law) != v:
                loo_ok = False
                break
    return v, cells_ok, loo_ok, res


def oc_cell2(task):
    scen, truth, c, N, i, gen_cell, sscale = task
    sigma = np.array([0.30, 0.30, 0.40]) * sscale
    M.SIGMA = sigma                                                   # gen_mock reads the module global for the PRIOR draw
    rng = np.random.default_rng(np.random.SeedSequence([221, 20000 + i]))
    cnt = {"LO": 0, "HI": 0, "NONE": 0, "sep_cells": 0, "sep_loo": 0, "sep_both": 0}
    for _ in range(M.K_MOCK):
        v, cells_ok, loo_ok, _ = rule2(M.gen_mock(M.BASE, N, truth, c, M.SCEN[scen], rng, gen_cell), "FLAT", "H(z)", B2, rng, sigma)
        cnt[v] += 1
        if v != "NONE":
            cnt["sep_cells"] += bool(cells_ok); cnt["sep_loo"] += bool(loo_ok); cnt["sep_both"] += bool(cells_ok and loo_ok)
    return task, cnt


def build_tasks():
    tasks, i = [], 0
    gen = ("nu_mono", "canonical")
    for truth in ("FLAT", "H(z)"):
        for c in (0.0, 0.30, -0.30, 0.60, -0.60, "PRIOR"):
            for N in NG2:
                tasks.append(("REAL", truth, c, N, i, gen, 1.0)); i += 1
        for N in (13, 36):
            tasks.append(("OPT", truth, 0.0, N, i, gen, 1.0)); i += 1
        for c in (0.0, "PRIOR"):
            for N in (20, 36):
                tasks.append(("REAL", truth, c, N, i, ("P2", "alt"), 1.0)); i += 1                     # MISMATCH sensitivity
            for N in (13, 20, 36, 50):
                tasks.append(("REAL", truth, c, N, i, gen, 0.5)); i += 1                                # prior-width sweep at 0.5
    return tasks


if __name__ == "__main__":
    out = []

    def P(s=""):
        print(s, flush=True); out.append(s)

    CHK = []

    def check(name, val, ok):
        CHK.append(bool(ok))
        P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")

    P(__doc__.split("Run:")[0].strip())
    t0 = time.time()
    P("\nCONTROLS")
    rng = np.random.default_rng(221 + 77)
    pair = ("FLAT", "H(z)")
    det = []
    for truth, want in (("FLAT", "LO"), ("H(z)", "HI")):
        for N in NG2:
            mock = M.gen_mock(M.BASE, N, truth, 0.0, 0.0, rng, noise=False)
            if MUT:
                mock["gobs"] = mock["gobs"] * 1.5
            v, cells_ok, loo_ok, res = rule2(mock, pair[0], pair[1], B2, rng)
            det.append((truth, N, v, cells_ok, loo_ok, res[(PRIM, "FLAT")], res[(PRIM, "H(z)")], want))
    if not MUT:
        ok2 = all(d[2] == d[7] for d in det)
        for d in det:
            P(f"    noise-free, truth {d[0]:5s} N = {d[1]:2d}: v2 verdict {d[2]:4s} (primary cell flat {d[5]}, rival {d[6]}); all four cells agree: {d[3]}; leave-one-out survives: {d[4]}")
        check("C2 noise-free mock (no noise, no extra scatter, true offset 0): the v2 verdict is the correct separation at every N for both truths", f"{sum(d[2] == d[7] for d in det)}/{len(det)}", ok2)
    else:
        okm = all(d[2] != "LO" for d in det if d[0] == "FLAT")
        P("  noise-free FLAT-truth mock with D x 1.5, primary-cell status of (flat, rival) per N: " + "; ".join(f"N={d[1]}: {d[5]}/{d[6]} -> {d[2]}" for d in det if d[0] == "FLAT"))
        check("C3 (MUTATE) the injected D x 1.5 destroys FLAT-SEPARATED(v2) at every N in the noise-free flat-truth mock", f"{okm}", okm)
        open(os.path.join(HERE, "cfg221_v2_MUTATE.out"), "w").write("\n".join(out) + "\n")
        sys.exit(0 if all(CHK) else 1)
    six, n20 = M.real_six()
    zero = np.zeros(3)
    nomed = {law: float(np.median(np.log10(six["gobs"] / ((six["Ms"] + six["Mg"]) * six["cg"]) / M.NUF["nu_mono"]((six["Ms"] + six["Mg"]) * six["cg"] / (M.A0S["canonical"] * six["F"][law]))))) for law in ("FLAT", "H(z)")}
    cf = json.load(open(os.path.join(os.path.dirname(HERE), "CFG220_cristal_outer_independent", "cfg220_outer_independent_results.json")))["cells"]["ind|nu_mono|canonical|table_Rout"]
    r0, e0 = statuses_v2(six, pair, B2, np.random.default_rng(221 + 9), sigma=zero, cells=[PRIM])
    edge_diff = max(abs(e0[(PRIM, "FLAT")][0] - cf["flat"][1]), abs(e0[(PRIM, "FLAT")][1] - cf["flat"][2]), abs(e0[(PRIM, "H(z)")][0] - cf["rival"][1]), abs(e0[(PRIM, "H(z)")][1] - cf["rival"][2]))
    c4 = max(abs(nomed["FLAT"] - cf["flat"][0]), abs(nomed["H(z)"] - cf["rival"][0]))
    check("C4 at sigma = 0 the v2 machinery reproduces CFG220's headline medians to 1e-9 and its two-sided 95% CI edges to 0.01 (the one-sided verdict thresholds are reported beside)",
          f"medians {nomed['FLAT']:+.3f}, {nomed['H(z)']:+.3f} (max diff {c4:.1e}); CI edges max diff {edge_diff:.3f}; one-sided statuses at sigma = 0: flat {r0[(PRIM, 'FLAT')]}, rival {r0[(PRIM, 'H(z)')]}", c4 < 1e-9 and edge_diff < 0.01)
    v, cells_ok, loo_ok, res = rule2(six, pair[0], pair[1], B2, np.random.default_rng(221 + 11))
    P(f"\nILLUSTRATION (the six real CRISTAL detections at table R_out; NOT blind, no verdict; sigma_dust = 0.30, B = 10,000): v2 {'FLAT-SEPARATED' if v == 'LO' else ('RIVAL-SEPARATED' if v == 'HI' else 'NO-SEPARATION')}")
    for cell in M.CELLS:
        P(f"    {cell[0]:7s} {cell[1]:9s} flat {res[(cell, 'FLAT')]:5s} rival {res[(cell, 'H(z)')]:5s}")
    import multiprocessing as mp
    tasks = build_tasks()
    P(f"\nOPERATING CHARACTERISTICS (v2): {len(tasks)} cells x {M.K_MOCK} mocks, B = {B2}, {mp.cpu_count()} cores")
    with mp.get_context("spawn").Pool(processes=min(15, mp.cpu_count())) as pool:
        results = pool.map(oc_cell2, tasks, chunksize=1)
    R = {}
    for (scen, truth, c, N, i, gen, ss), cnt in results:
        R[(scen, truth, str(c), N, gen, ss)] = cnt
    P(f"[{time.time() - t0:.0f} s]")
    K_ = M.K_MOCK
    gen0 = ("nu_mono", "canonical")

    def rates(scen, truth, c, N, gen=gen0, ss=1.0):
        cnt = R[(scen, truth, str(c), N, gen, ss)]
        good = "LO" if truth == "FLAT" else "HI"
        bad = "HI" if truth == "FLAT" else "LO"
        return cnt[good] / K_, cnt[bad] / K_, cnt

    P("\n  v2, scenario REAL: P(correct separation) / P(WRONG separation), by truth, true offset c (dex on the gas mass) and N = " + " ".join(f"{N:>9d}" for N in NG2))
    for truth in ("FLAT", "H(z)"):
        for c in (0.0, 0.30, -0.30, 0.60, -0.60, "PRIOR"):
            P(f"    {truth:5s} c = {str(c):6s}  " + " ".join(f"{rates('REAL', truth, c, N)[0]:4.2f}/{rates('REAL', truth, c, N)[1]:4.2f}" for N in NG2))
    P("\n  REPORTED robustness of the v2 separations (REAL, c = 0): of the mocks with the CORRECT v2 separation, the share in which all four cells agree / the leave-one-out survives")
    for truth in ("FLAT", "H(z)"):
        row = []
        for N in NG2:
            cnt = rates("REAL", truth, 0.0, N)[2]; good = "LO" if truth == "FLAT" else "HI"
            tot = max(cnt[good], 1)
            row.append(f"N={N}: {cnt['sep_cells']}/{cnt['LO'] + cnt['HI']} cells, {cnt['sep_loo']}/{cnt['LO'] + cnt['HI']} LOO")
        P(f"    {truth:5s} " + "; ".join(row))
    P("\n  sensitivities (P(correct)/P(wrong)): OPT c = 0; MISMATCH (truth from P2, alt); prior-width scale 0.5 (sigma_dust = sigma_CO = 0.15 dex)")
    for truth in ("FLAT", "H(z)"):
        P(f"    {truth:5s} OPT c=0: N=13 {rates('OPT', truth, 0.0, 13)[0]:.2f}/{rates('OPT', truth, 0.0, 13)[1]:.2f}, N=36 {rates('OPT', truth, 0.0, 36)[0]:.2f}/{rates('OPT', truth, 0.0, 36)[1]:.2f}"
          f"  | MISMATCH c=0: N=20 {rates('REAL', truth, 0.0, 20, ('P2', 'alt'))[0]:.2f}/{rates('REAL', truth, 0.0, 20, ('P2', 'alt'))[1]:.2f}, N=36 {rates('REAL', truth, 0.0, 36, ('P2', 'alt'))[0]:.2f}/{rates('REAL', truth, 0.0, 36, ('P2', 'alt'))[1]:.2f}"
          f"; PRIOR: N=20 {rates('REAL', truth, 'PRIOR', 20, ('P2', 'alt'))[0]:.2f}/{rates('REAL', truth, 'PRIOR', 20, ('P2', 'alt'))[1]:.2f}, N=36 {rates('REAL', truth, 'PRIOR', 36, ('P2', 'alt'))[0]:.2f}/{rates('REAL', truth, 'PRIOR', 36, ('P2', 'alt'))[1]:.2f}")
    sw_feas = None
    for truth in ("FLAT", "H(z)"):
        for c in (0.0, "PRIOR"):
            P(f"    scale 0.5 {truth:5s} c = {str(c):6s} N = 13 / 20 / 36 / 50: " + " ".join(f"{rates('REAL', truth, c, N, gen0, 0.5)[0]:.2f}/{rates('REAL', truth, c, N, gen0, 0.5)[1]:.2f}" for N in (13, 20, 36, 50)))
    lim = 0.05 + 2 * math.sqrt(0.05 * 0.95 / K_)
    worst = (0.0, None)
    for truth in ("FLAT", "H(z)"):
        for c in (0.0, 0.30, -0.30, "PRIOR"):
            for N in NG2:
                w = rates("REAL", truth, c, N)[1]
                if w > worst[0]:
                    worst = (w, (truth, c, N))
    P("")
    check(f"C1 FALSE-SEPARATION-CONTROLLED (v2): the WRONG-separation rate at c = 0, +-0.30 and PRIOR is <= {lim:.3f} for every N and both truths (REAL)", f"worst {worst[0]:.2f} at {worst[1]}", worst[0] <= lim)
    feas = [N for N in NG2 if min(rates("REAL", "FLAT", 0.0, N)[0], rates("REAL", "H(z)", 0.0, N)[0]) >= 0.8]
    best = max(min(rates("REAL", "FLAT", 0.0, N)[0], rates("REAL", "H(z)", 0.0, N)[0]) for N in NG2)
    P(f"\n  FEASIBLE (v2; REAL, c = 0, P(correct) >= 0.8 for both truths): " + (f"N_feasible = {feas[0]}" if feas else f"NOT FEASIBLE up to N = {NG2[-1]}; the best min over the two truths is {best:.2f}"))
    for N in NG2:
        P(f"    N = {N:2d}: v2 REAL c = 0: FLAT {rates('REAL', 'FLAT', 0.0, N)[0]:.2f}, H(z) {rates('REAL', 'H(z)', 0.0, N)[0]:.2f}")
    # the side-by-side with v1 (read from the v1 results; v1 governs any headline)
    v1 = json.load(open(os.path.join(HERE, "cfg221_decision_rule_results.json")))["results"]

    def v1rate(truth, c, N):
        cnt = v1[f"REAL|{truth}|{c}|{N}|('nu_mono', 'canonical')|('FLAT', 'H(z)')"]
        return (cnt["LO"] if truth == "FLAT" else cnt["HI"]) / K_

    P("\n  SIDE BY SIDE, REAL, c = 0, P(correct separation): v1 (the PRIMARY rule, governs any headline) | v2 (SECONDARY), N = " + " ".join(f"{N:>4d}" for N in (6, 13, 20, 36, 50)))
    for truth in ("FLAT", "H(z)"):
        P(f"    {truth:5s} v1 " + " ".join(f"{v1rate(truth, 0.0, N):4.2f}" for N in (6, 13, 20, 36, 50)) + "  |  v2 " + " ".join(f"{rates('REAL', truth, 0.0, N)[0]:4.2f}" for N in (6, 13, 20, 36, 50)))
    P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - t0:.0f} s")
    js = {"controls": dict(passed=sum(CHK), n=len(CHK)), "feasible_N": (feas[0] if feas else None), "best_min_power": best, "results": {"|".join(map(str, k)): v for k, v in R.items()}}
    json.dump(js, open(os.path.join(HERE, "cfg221_v2_results.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg221_v2.out"), "w").write("\n".join(out) + "\n")
    sys.exit(0 if all(CHK) else 1)
