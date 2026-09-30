#!/usr/bin/env python3
"""CFG221 -- the frozen decision rule for the pooled z > 3.5 two-sided test, and its operating characteristics on mocks.
Frozen criteria: FROZEN_CRITERIA.md here (46df63032 + ADDENDUM 1 70fff09bb + ADDENDUM 2 cde8112c9), committed before any run.  kappa = 1/2 FITTED, NOT DERIVED.
The rule: marginal bootstrap (discs resampled and the shared gas calibration tau_k ~ N(0, sigma_k^2) redrawn in every resample); DISFAVOURED-under / -over / NOT from the marginal 95% CI of the median delta;
FLAT-SEPARATED / RIVAL-SEPARATED only if the status holds in all four kernel/footing cells and after dropping any one disc.  Mocks: the six CRISTAL detections' z, radius and baryon errors (CFG219's template) at R_out.
A description of THIS rule on THIS template, not a claim about any real sample.  No sentence says the data favour a framework.
Run:  python3 campaign_fresh_gravity/CFG221_z35_decision_rule/cfg221_decision_rule.py        (about 10 minutes on 16 cores; MUTATE=1 runs only the response control)
"""
import os, sys, io, json, math, time, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.pop("MUTATE", "").strip() == "1"        # CFG219's prefix must not see MUTATE (its own MUTATE branch exits)
SFX = "_MUTATE" if MUT else ""
path19 = os.path.join(CFG, "CFG219_z35_preflight", "cfg219_preflight.py")
src19 = open(path19).read()
ns19 = {"__file__": path19, "__name__": "cfg219"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src19[:src19.index("# ------------------------------------------------------------------------------------------------ the per-disc table")], "cfg219", "exec"), ns19)
K, A0S, LAWS, make_base, cristal_rows = (ns19[k] for k in ("K", "A0S", "LAWS", "make_base", "cristal_rows"))

CELLS = [("nu_mono", "canonical"), ("nu_mono", "alt"), ("P2", "canonical"), ("P2", "alt")]
NUF = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
SIGMA = np.array([0.30, 0.30, 0.40])                       # dust, CO, [CII]: the frozen marginalised prior widths (dex on the gas mass)
SCEN = {"OPT": 0.0, "REAL": 0.21, "REAL27": 0.23}          # extra per-disc scatter on log D (dex): total 0.14 -> 0.25 / 0.27 with the baryon noise
NGRID = (6, 13, 20, 30, 36, 50)
NB, K_MOCK, SEED = 500, 100, 221
BASE = make_base(cristal_rows(), radius="Rout")


def gen_mock(base, N, truth, c, extra, rng, gen_cell=("nu_mono", "canonical"), noise=True):
    n = len(base["z"])
    idx = np.arange(n) if N == n else rng.integers(0, n, N)
    nu, a0 = NUF[gen_cell[0]], A0S[gen_cell[1]]
    if noise:
        es = rng.normal(0, 1, N) * base["sig_star"][idx]
        eg = rng.normal(0, 1, N) * base["sig_gas"][idx]
        eta = rng.normal(0, 1, N) * extra
        ck = rng.normal(0, 1, 3) * SIGMA if isinstance(c, str) else np.full(3, float(c))
    else:
        es = eg = eta = np.zeros(N); ck = np.zeros(3)
    cls = base["cls"][idx].astype(int)
    Mst, Mgt = base["Ms"][idx], base["Mg"][idx]
    gt = (Mst + Mgt) * base["cg"][idx]
    gobs = gt * nu(gt / (a0 * base["F"][truth][idx])) * 10 ** eta
    return dict(gobs=gobs, cg=base["cg"][idx], z=base["z"][idx], cls=cls, Ms=Mst * 10 ** es, Mg=Mgt * 10 ** (eg + ck[cls]), F={l: base["F"][l][idx] for l in LAWS})


def drop(mock, keep):
    return {k: ({l: a[keep] for l, a in v.items()} if isinstance(v, dict) else v[keep]) for k, v in mock.items()}


def statuses(mock, laws, B, rng, sigma=SIGMA):
    N = len(mock["gobs"])
    IB = rng.integers(0, N, size=(B, N))
    ck = rng.normal(0, 1, (B, 3)) * sigma[None, :]
    cc = np.take_along_axis(ck, mock["cls"][IB], axis=1)
    gbar = (mock["Ms"][IB] + mock["Mg"][IB] * 10 ** cc) * mock["cg"][IB]
    D = mock["gobs"][IB] / gbar
    res, med = {}, {}
    for cell in CELLS:
        nu, a0 = NUF[cell[0]], A0S[cell[1]]
        for law in laws:
            m = np.median(np.log10(D / nu(gbar / (a0 * mock["F"][law][IB]))), axis=1)
            lo, hi = np.percentile(m, [2.5, 97.5])
            res[(cell, law)] = "under" if hi < 0 else ("over" if lo > 0 else "not")
            med[(cell, law)] = (float(lo), float(hi))
    return res, med


def verdict_from(res, lo_law, hi_law):
    if all(res[(c, hi_law)] == "under" and res[(c, lo_law)] == "not" for c in CELLS):
        return "LO"
    if all(res[(c, lo_law)] == "over" and res[(c, hi_law)] == "not" for c in CELLS):
        return "HI"
    return "NONE"


def rule(mock, lo_law, hi_law, B, rng, loo=True, sigma=SIGMA):
    res, med = statuses(mock, (lo_law, hi_law), B, rng, sigma)
    v = verdict_from(res, lo_law, hi_law)
    if v != "NONE" and loo:
        N = len(mock["gobs"])
        for j in range(N):
            r2, _ = statuses(drop(mock, np.arange(N) != j), (lo_law, hi_law), B, rng, sigma)
            if verdict_from(r2, lo_law, hi_law) != v:
                return "NONE", res, med
    return v, res, med


def oc_cell(task):
    scen, truth, c, N, i, gen_cell, pair = task
    rng = np.random.default_rng(np.random.SeedSequence([SEED, i]))
    cnt = {"LO": 0, "HI": 0, "NONE": 0}
    for _ in range(K_MOCK):
        v, _, _ = rule(gen_mock(BASE, N, truth, c, SCEN[scen], rng, gen_cell), pair[0], pair[1], NB, rng)
        cnt[v] += 1
    return task, cnt


def build_tasks():
    tasks, i = [], 0
    pair = ("FLAT", "H(z)")
    for scen in ("OPT", "REAL"):
        for truth in ("FLAT", "H(z)"):
            for c in (0.0, 0.30, -0.30, 0.60, -0.60, "PRIOR"):
                for N in NGRID:
                    tasks.append((scen, truth, c, N, i, ("nu_mono", "canonical"), pair)); i += 1
    for truth in ("FLAT", "H(z)"):
        for c in (0.0, "PRIOR"):
            for N in (20, 36):
                tasks.append(("REAL27", truth, c, N, i, ("nu_mono", "canonical"), pair)); i += 1
                tasks.append(("REAL", truth, c, N, i, ("P2", "alt"), pair)); i += 1                # MISMATCH: truth generated with (P2, alt)
    pair2 = ("FLAT", "HORIZON")
    for truth in ("FLAT", "HORIZON"):
        for c in (0.0, 0.30, -0.30):
            for N in (13, 20):
                tasks.append(("REAL", truth, c, N, i, ("nu_mono", "canonical"), pair2)); i += 1
    return tasks


def real_six():
    """The six real CRISTAL detections at table R_out as a rule input (the CFG220 inputs; NOT blind)."""
    path20 = os.path.join(CFG, "CFG220_cristal_outer_independent", "cfg220_outer_independent.py")
    s20 = open(path20).read()
    n20 = {"__file__": path20, "__name__": "cfg220"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(s20[:s20.index("# ------------------------------------------------------------------------------------------------ controls")], "cfg220", "exec"), n20)
    rows_for, DET, byid, gas_ratio = (n20[k] for k in ("rows_for", "DET", "byid", "gas_ratio"))
    rf = rows_for("table_Rout", DET, "fit", mutate=False)
    Ms = np.array([10 ** byid[r["id"]]["logMstar"] for r in rf]); Mg = np.array([10 ** byid[r["id"]]["logMstar"] * gas_ratio(byid[r["id"]]) for r in rf])
    cg = np.array([r["gbar"] / 10 ** byid[r["id"]]["logMfit"] for r in rf])
    z = np.array([r["z"] for r in rf])
    return dict(gobs=np.array([r["D"] * r["gbar"] for r in rf]), cg=cg, z=z, cls=np.zeros(len(rf), int), Ms=Ms, Mg=Mg,
                F={"FLAT": np.ones(len(rf)), "H(z)": np.array([ns19["Ez"](zz) for zz in z])}), n20


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
    # ------------------------------------------------------------------------------------------------ controls that need no mocks in bulk
    P("\nCONTROLS")
    rng = np.random.default_rng(SEED + 7)
    pair = ("FLAT", "H(z)")
    ok2 = True
    det2 = []
    for truth, want in (("FLAT", "LO"), ("H(z)", "HI")):
        for N in NGRID:
            mock = gen_mock(BASE, N, truth, 0.0, 0.0, rng, noise=False)
            if MUT:
                mock["gobs"] = mock["gobs"] * 1.5                                    # D x 1.5
            v, res, med = rule(mock, pair[0], pair[1], NB, rng)
            det2.append((truth, N, v, res[(CELLS[0], "FLAT")], res[(CELLS[0], "H(z)")]))
            if not MUT:
                ok2 &= v == want
    if not MUT:
        check("C2 noise-free mock (no measurement noise, no extra scatter, true offset 0): the correct separation at every N for both truths", f"{sum(d[2] == ('LO' if d[0] == 'FLAT' else 'HI') for d in det2)}/{len(det2)}", ok2)
    else:
        okm = all(d[2] != "LO" for d in det2 if d[0] == "FLAT")
        P("  noise-free FLAT-truth mock with D x 1.5, status of (flat, rival) in the primary cell per N: " + "; ".join(f"N={d[1]}: {d[3]}/{d[4]} -> {d[2]}" for d in det2 if d[0] == "FLAT"))
        check("C3 (MUTATE) the injected D x 1.5 destroys FLAT-SEPARATED at every N in the noise-free flat-truth mock", f"{okm}", okm)
        open(os.path.join(LANE, "cfg221_decision_rule_MUTATE.out"), "w").write("\n".join(out) + "\n")
        sys.exit(0 if all(CHK) else 1)
    # C4 and the real-data ILLUSTRATION
    six, n20 = real_six()
    zero = np.zeros(3)
    nomed = {law: float(np.median(np.log10(six["gobs"] / ((six["Ms"] + six["Mg"]) * six["cg"]) / NUF["nu_mono"]((six["Ms"] + six["Mg"]) * six["cg"] / (A0S["canonical"] * six["F"][law]))))) for law in ("FLAT", "H(z)")}
    cf = json.load(open(os.path.join(CFG, "CFG220_cristal_outer_independent", "cfg220_outer_independent_results.json")))["cells"]["ind|nu_mono|canonical|table_Rout"]
    c4 = max(abs(nomed["FLAT"] - cf["flat"][0]), abs(nomed["H(z)"] - cf["rival"][0]))
    r0, _ = statuses(six, pair, 10000, np.random.default_rng(SEED + 9), sigma=zero)
    head = (r0[(CELLS[0], "FLAT")], r0[(CELLS[0], "H(z)")])
    check("C4 the rule's machinery on the six real detections with the calibration collapsed (sigma = 0) reproduces CFG220's headline cell: medians (flat +0.106, rival -0.203) and both laws NOT-DISFAVOURED", f"medians {nomed['FLAT']:+.3f}, {nomed['H(z)']:+.3f} (max diff {c4:.1e}); statuses {head}", c4 < 1e-9 and head == ("not", "not"))
    v, res, med = rule(six, pair[0], pair[1], 10000, np.random.default_rng(SEED + 11))
    P(f"\nILLUSTRATION (the six real CRISTAL detections at table R_out; NOT blind, no verdict; sigma_dust = 0.30, B = 10,000): {v}-SEPARATED" if v != "NONE" else
      "\nILLUSTRATION (the six real CRISTAL detections at table R_out; NOT blind, no verdict; sigma_dust = 0.30, B = 10,000): NO-SEPARATION")
    for cell in CELLS:
        P(f"    {cell[0]:7s} {cell[1]:9s} flat {res[(cell, 'FLAT')]:5s} [{med[(cell, 'FLAT')][0]:+.3f}, {med[(cell, 'FLAT')][1]:+.3f}]   rival {res[(cell, 'H(z)')]:5s} [{med[(cell, 'H(z)')][0]:+.3f}, {med[(cell, 'H(z)')][1]:+.3f}]")
    # ------------------------------------------------------------------------------------------------ operating characteristics (parallel)
    import multiprocessing as mp
    tasks = build_tasks()
    P(f"\nOPERATING CHARACTERISTICS: {len(tasks)} cells x {K_MOCK} mocks, B = {NB}, {mp.cpu_count()} cores")
    ctx = mp.get_context("spawn")
    with ctx.Pool(processes=min(15, mp.cpu_count())) as pool:
        results = pool.map(oc_cell, tasks, chunksize=1)
    R = {}
    for (scen, truth, c, N, i, gen_cell, pair_), cnt in results:
        R[(scen, truth, str(c), N, gen_cell, pair_)] = cnt
    P(f"[{time.time() - t0:.0f} s]")

    def rates(scen, truth, c, N, gen=("nu_mono", "canonical"), pr=("FLAT", "H(z)")):
        cnt = R[(scen, truth, str(c), N, gen, pr)]
        good = "LO" if truth == pr[0] else "HI"
        bad = "HI" if truth == pr[0] else "LO"
        return cnt[good] / K_MOCK, cnt[bad] / K_MOCK

    for scen in ("REAL", "OPT"):
        P(f"\n  scenario {scen}: P(correct separation) / P(WRONG separation), by truth, true offset c (dex on the gas mass) and N = " + " ".join(f"{N:>9d}" for N in NGRID))
        for truth in ("FLAT", "H(z)"):
            for c in (0.0, 0.30, -0.30, 0.60, -0.60, "PRIOR"):
                P(f"    {truth:5s} c = {str(c):6s}  " + " ".join(f"{rates(scen, truth, c, N)[0]:4.2f}/{rates(scen, truth, c, N)[1]:4.2f}" for N in NGRID))
    P("\n  sensitivities (P(correct)/P(wrong)):")
    for truth in ("FLAT", "H(z)"):
        for c in (0.0, "PRIOR"):
            P(f"    REAL27 {truth:5s} c = {str(c):6s} N = 20: {rates('REAL27', truth, c, 20)[0]:.2f}/{rates('REAL27', truth, c, 20)[1]:.2f}, N = 36: {rates('REAL27', truth, c, 36)[0]:.2f}/{rates('REAL27', truth, c, 36)[1]:.2f}"
              f"   |  MISMATCH (truth from P2, alt) N = 20: {rates('REAL', truth, c, 20, ('P2', 'alt'))[0]:.2f}/{rates('REAL', truth, c, 20, ('P2', 'alt'))[1]:.2f}, N = 36: {rates('REAL', truth, c, 36, ('P2', 'alt'))[0]:.2f}/{rates('REAL', truth, c, 36, ('P2', 'alt'))[1]:.2f}")
    P("\n  extra pair FLAT vs HORIZON (REAL; P(correct)/P(wrong)):")
    for truth in ("FLAT", "HORIZON"):
        P(f"    {truth:8s} " + "  ".join(f"c = {c:+.2f} N = 13: {rates('REAL', truth, c, 13, pr=('FLAT', 'HORIZON'))[0]:.2f}/{rates('REAL', truth, c, 13, pr=('FLAT', 'HORIZON'))[1]:.2f}, N = 20: {rates('REAL', truth, c, 20, pr=('FLAT', 'HORIZON'))[0]:.2f}/{rates('REAL', truth, c, 20, pr=('FLAT', 'HORIZON'))[1]:.2f}" for c in (0.0, 0.30, -0.30)))
    # ------------------------------------------------------------------------------------------------ frozen classes
    lim = 0.05 + 2 * math.sqrt(0.05 * 0.95 / K_MOCK)
    worst = (0.0, None)
    for scen in ("REAL", "OPT"):
        for truth in ("FLAT", "H(z)"):
            for c in (0.0, 0.30, -0.30, "PRIOR"):
                for N in NGRID:
                    w = rates(scen, truth, c, N)[1]
                    if w > worst[0]:
                        worst = (w, (scen, truth, c, N))
    P("")
    check(f"C1 FALSE-SEPARATION-CONTROLLED: the WRONG-separation rate at c = 0, +-0.30 and PRIOR is <= {lim:.3f} for every N, both truths, both scenarios", f"worst {worst[0]:.2f} at {worst[1]}", worst[0] <= lim)
    feas = [N for N in NGRID if min(rates("REAL", "FLAT", 0.0, N)[0], rates("REAL", "H(z)", 0.0, N)[0]) >= 0.8]
    best = max(min(rates("REAL", "FLAT", 0.0, N)[0], rates("REAL", "H(z)", 0.0, N)[0]) for N in NGRID)
    P(f"\n  FEASIBLE (REAL, c = 0, P(correct) >= 0.8 for both truths): " + (f"N_feasible = {feas[0]}" if feas else f"NOT FEASIBLE up to N = {NGRID[-1]}; the best min(P(correct) over the two truths) is {best:.2f}"))
    for N in NGRID:
        P(f"    N = {N:2d}: REAL c = 0: FLAT {rates('REAL', 'FLAT', 0.0, N)[0]:.2f}, H(z) {rates('REAL', 'H(z)', 0.0, N)[0]:.2f};  OPT c = 0: FLAT {rates('OPT', 'FLAT', 0.0, N)[0]:.2f}, H(z) {rates('OPT', 'H(z)', 0.0, N)[0]:.2f}")
    P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - t0:.0f} s")
    js = {"controls": dict(passed=sum(CHK), n=len(CHK)), "feasible_N": (feas[0] if feas else None), "best_min_power": best,
          "results": {"|".join(map(str, k)): v for k, v in R.items()}}
    json.dump(js, open(os.path.join(LANE, "cfg221_decision_rule_results.json"), "w"), indent=1)
    open(os.path.join(LANE, "cfg221_decision_rule.out"), "w").write("\n".join(out) + "\n")
    sys.exit(0 if all(CHK) else 1)
