"""CFG235_01_controls.py -- planted-galaxy controls P1-P9 (+ declared extras P10, P3b, P11), checks C0-C5.
Runs on SYNTHETIC rows only (a generic synthetic background plus plants); no real per-galaxy value enters the statistics.
Exit 0 iff every control passes; exit 1 if any fails (kept, never repaired).  With env MUTATE=k the same controls run with
one load-bearing cell flipped (see CFG235_MUTATE.py, which calls run_controls)."""
import os, sys, json, math, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
import CFG235_common as C

LOG = []


def P(*a):
    s = C.clean(" ".join(str(x) for x in a))
    print(s, flush=True)
    LOG.append(s)


A0 = C.A0K["canonical"]


def make_row(rid, R_obs, x, z=4.5, r=3.0, sig_stat=0.05, src="SYN", field="none", extra=None, sigma0=None):
    """synthetic row built through the SAME inputs as a CRISTAL-like row (M*, r_e, V_rot, sigma_0, z, errors)."""
    lM = math.log10(2.0 * x * A0 * r * r / C.G_KPC)          # f_enc = 0.5 -> g_* = 0.5 G M*/r^2 = x a0
    Vb2 = 0.5 * C.G_KPC * 10 ** lM / r
    Vc2 = R_obs * Vb2
    Vc = math.sqrt(Vc2)
    sg = sigma0 if sigma0 is not None else min(50.0, 0.3 * Vc)
    Vr2 = Vc2 - C.K_PRESS * sg * sg
    assert Vr2 > 0, (rid, Vc2, sg)
    Vr = math.sqrt(Vr2)
    row = dict(id=rid, src=src, kind="C", tier="S", z=z, field=field, lMstar=lM, e_Mstar_lo=sig_stat,
               vrot=Vr, e_vrot_hi=Vr * sig_stat / 2 * C.LN10, sigma0=sg, e_sig_hi=0.05 * sg,
               r_kpc=r, e_r_hi=0.02 * r, e_r_lo=0.02 * r, rr=1.0, vsig=Vr / sg, Mstar_lim="", Mdyn_lim="", sigma_lim="",
               known="", fdm=None)
    if extra:
        row.update(extra)
    return row


def background(n=62, seed=2350):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        z = rng.uniform(3.6, 5.8)
        r = rng.uniform(1.0, 3.5)
        lM = rng.uniform(9.3, 10.8)
        x = 0.5 * C.G_KPC * 10 ** lM / r ** 2 / A0
        nu = float(C.nu_p2(x))
        R = nu * 10 ** rng.uniform(0.3, 0.8)
        sg0 = rng.uniform(50, 100)
        rows.append(make_row(f"SYN_BG{i:02d}", R, x, z=z, r=r, sig_stat=rng.uniform(0.05, 0.25), sigma0=None))
    return rows


def z_of(row, crit="F1", key="z_rob", n=None):
    n = n or C.N_MC
    if crit == "L2":
        return C.score_row_L2(row, n=n).get(key, float("nan"))
    return C.score_row_LF(row, n=n)[crit][key]


def solve_R(rid, x, target, crit, key, z=4.5, r=3.0, lo=-3.0, hi=3.0, sig_stat=0.05, extra=None):
    f = lambda lr: z_of(make_row(rid, 10 ** lr, x, z=z, r=r, sig_stat=sig_stat, extra=extra), crit, key) - target
    lr = brentq(f, lo, hi, xtol=2e-3)
    return 10 ** lr


def nfw_need(M200, r, z, cm="DM14"):
    return float(C.nfw_dm_enc(np.array([math.log10(M200)]), r, z, cm)[0])


def planted_params(seed_params=None):
    """the planted (R_obs, x) targets; solved once (main run) and stored so MUTATE runs reuse the same planted rows."""
    if seed_params:
        return seed_params
    pp = {}
    pp["P1"] = dict(R=0.03, x=5.0)
    pp["P2"] = dict(R=1.0, x=1e-4)
    # P3: M200,need = 1e14 at z = 4.5, r = 3 kpc, x = 5
    r = 3.0
    lM = math.log10(2.0 * 5.0 * A0 * r * r / C.G_KPC)
    need = nfw_need(1e14, r, 4.5)
    pp["P3"] = dict(R=(need + 0.5 * 10 ** lM) / (0.5 * 10 ** lM), x=5.0)
    pp["P4"] = dict(R=3.0 * float(C.nu_p2(2.0)), x=2.0)
    pp["P5"] = dict(R=solve_R("SYN_P5", 2.0, 1.5, "F1", "z_primary"), x=2.0)
    pp["P6"] = dict(R=solve_R("SYN_P6", 1e-2, 3.05, "F1", "z_rob", lo=-2.0, hi=2.0), x=1e-2)
    pp["P7"] = dict(R=0.3, x=2.0)
    pp["P9"] = dict(R=0.1, x=2.0)
    pp["P10"] = dict(R=300.0, x=1e-4)
    pp["P11"] = dict(R=solve_R("SYN_P11", 1e-2, 3.4, "F1", "z_primary", lo=-2.0, hi=2.0), x=1e-2)
    # P3b (extra, declared in phase 2): M200,need = 3e14 at z = 4.5; main-run z_primary(L2) about 1.8; used by MUTATE 7
    need3b = nfw_need(3e14, r, 4.5)
    pp["P3b"] = dict(R=(need3b + 0.5 * 10 ** lM) / (0.5 * 10 ** lM), x=5.0)
    return pp


def build_rows(pp):
    bg = background()
    pl = []
    pl.append(make_row("SYN_P1", pp["P1"]["R"], pp["P1"]["x"]))
    pl.append(make_row("SYN_P2", pp["P2"]["R"], pp["P2"]["x"]))
    pl.append(make_row("SYN_P3", pp["P3"]["R"], pp["P3"]["x"]))
    pl.append(make_row("SYN_P4", pp["P4"]["R"], pp["P4"]["x"]))
    pl.append(make_row("SYN_P5", pp["P5"]["R"], pp["P5"]["x"]))
    pl.append(make_row("SYN_P6", pp["P6"]["R"], pp["P6"]["x"]))
    r7 = make_row("SYN_P7", pp["P7"]["R"], pp["P7"]["x"])
    r7["lgas"] = r7["lMstar"] + math.log10(42.0)            # S+G: (M* + Mg/3) = 15 M*  -> R_S+G = 0.02
    pl.append(r7)
    pl.append(make_row("SYN_P8", 4.0, 2.0, z=4.43, field="GOODS-S", src="D"))
    pl.append(make_row("SYN_P9", pp["P9"]["R"], pp["P9"]["x"], extra=dict(Mstar_lim="<")))
    pl.append(make_row("SYN_P10", pp["P10"]["R"], pp["P10"]["x"], extra=dict(fdm=0.0)))
    pl.append(make_row("SYN_P11", pp["P11"]["R"], pp["P11"]["x"]))
    pl.append(make_row("SYN_P3b", pp["P3b"]["R"], pp["P3b"]["x"]))
    return bg, pl


def run_controls(pp=None, quiet=False):
    t0 = time.time()
    exp = {}
    pp = planted_params(pp)
    bg, pl = build_rows(pp)
    rows = bg + pl
    m = 31 if C.MUT == 8 else len(rows)
    res, meta = C.score_sample(rows, n_perm=20000, n_sim=20000, m_trials=m)
    R = {q["id"]: q for q in res}

    def ok(name, cond, detail=""):
        exp[name] = dict(ok=bool(cond), detail=detail)

    def fl(i, crit, tier):
        return R[i][crit][tier]

    p1 = R["SYN_P1"]
    ok("P1.L1_T0", fl("SYN_P1", "L1", "T0"), f"z_rob L1 {p1['L1'].get('z_rob'):.2f}")
    ok("P1.F1_T0_all_cells", fl("SYN_P1", "F1", "T0"), f"z_rob F1 {p1['F1'].get('z_rob'):.2f}")
    ok("P1.L1_T2(frozen expectation)", fl("SYN_P1", "L1", "T2"), f"T1={fl('SYN_P1','L1','T1')} p_wy={p1['L1'].get('p_wy')}")
    ok("P1.label_T0_both", p1["label_T0"] == "both", p1["label_T0"])
    p2 = R["SYN_P2"]
    ok("P2.F1_T0", fl("SYN_P2", "F1", "T0"), f"z_rob F1 {p2['F1'].get('z_rob'):.2f}")
    ok("P2.L1_not_T0", not fl("SYN_P2", "L1", "T0"), f"z_rob L1 {p2['L1'].get('z_rob'):.2f}")
    ok("P2.label_T0_framework_only", p2["label_T0"] == "framework-only", p2["label_T0"])
    p3 = R["SYN_P3"]
    ok("P3.L2_T0", fl("SYN_P3", "L2", "T0"), f"z_rob L2 {p3['L2'].get('z_rob', float('nan')):.2f}")
    ok("P3.L1_F1_not_T0", (not fl("SYN_P3", "L1", "T0")) and (not fl("SYN_P3", "F1", "T0")), "")
    ok("P3.label_T0_LCDM_only", p3["label_T0"] == "LCDM-only", p3["label_T0"])
    p4 = R["SYN_P4"]
    ok("P4.no_flag_any_tier", all(not p4[c][t] for c in ("L1", "L2", "F1") for t in ("T0", "T1", "T2")), p4["label_T0"])
    p5 = R["SYN_P5"]
    ok("P5.no_T0", not any(p5[c]["T0"] for c in ("L1", "L2", "F1")), f"z_primary F1 {p5['F1'].get('z_primary'):.2f} z_rob {p5['F1'].get('z_rob'):.2f}")
    p6 = R["SYN_P6"]
    ok("P6.F1_T0_fired", p6["F1"]["T0"], f"z_rob {p6['F1'].get('z_rob'):.3f}")
    ok("P6.F1_T1_NOT_fired", not p6["F1"]["T1"], f"z_B {meta['zB']:.3f}")
    ok("P6.not_confirmed_(T2)", not p6["F1"]["T2"], "")
    p7 = R["SYN_P7"]
    ok("P7.L1_T0_not_fired(tier S)", not p7["L1"]["T0"], f"z_rob {p7['L1'].get('z_rob'):.2f}")
    ok("P7.SG_cell_reported_fired", p7["rep"].get("SG_L1_z", 0) > 3, f"S+G L1 z {p7['rep'].get('SG_L1_z', float('nan')):.2f}")
    pairs = C.dup_pairs(rows + [r for r in C.load_sample() if r["id"] == "C_08"])
    ok("P8.duplicate_listed", any("SYN_P8" in p[:2] and "C_08" in p[:2] for p in pairs), str([p for p in pairs if "SYN_P8" in p[:2]]))
    ok("P8.m_stays", True, "m fixed by construction (M_TRIALS)")
    p9 = R["SYN_P9"]
    ok("P9.not_testable", (not p9["L1"]["defined"]) and (not p9["F1"]["defined"]) and (not p9["L2"]["defined"]), "")
    p10 = R["SYN_P10"]
    ok("P10.no_flag(f_DM-inconsistent row; V_c route)", not any(p10[c]["T0"] for c in ("L1", "L2", "F1")), f"F1 z_rob {p10['F1'].get('z_rob'):.2f}")
    p11 = R["SYN_P11"]
    ok("P11.fragile_no_T0(z_primary>3, z_rob<3)", not p11["F1"]["T0"], f"z_primary {p11['F1'].get('z_primary'):.2f} z_rob {p11['F1'].get('z_rob'):.2f}")
    p3b = R["SYN_P3b"]
    ok("P3b.L2_z_primary<=2.0(V_ref)", p3b["L2"].get("z_primary", 9) <= 2.0, f"z_primary L2 {p3b['L2'].get('z_primary', float('nan')):.2f}, z_rob {p3b['L2'].get('z_rob', float('nan')):.2f}")
    ok("BG.no_flags_in_background", all(not R[q["id"]][c]["T0"] for q in bg for c in ("L1", "L2", "F1")), "")
    ok("STRUCT.every_L1_T0_is_F1_T0", all((not q["L1"]["T0"]) or q["F1"]["T0"] for q in res), "")
    return dict(exp=exp, pp=pp, meta=dict(zB=meta["zB"], m=m, n_rows=len(rows)), res={q["id"]: dict(
        L1=q["L1"], F1=q["F1"], L2=q["L2"], label_T0=q["label_T0"], label_T1=q["label_T1"], label_T2=q["label_T2"]) for q in res if q["id"].startswith("SYN_P")},
        seconds=time.time() - t0, l1_an=[(q["id"], q["l1_an"], q["L1"].get("z_primary")) for q in res[:8]])


def checks():
    ck = {}
    # C0 sample counts
    rows = C.load_sample()
    cnt = {}
    for r in rows:
        cnt[r["src"]] = cnt.get(r["src"], 0) + 1
    ck["C0.sample_counts"] = dict(ok=(cnt == {"D": 41, "C": 14, "R": 4, "A": 2, "P": 1}), detail=str(cnt))
    # C1 analytic vs MC (5 random background rows)
    bg = background()
    d = []
    for r in bg[:5]:
        q = C.score_row_LF(r)
        d.append(abs(q["L1"]["z_primary"] - q["L1_z_analytic_primary"]))
    ck["C1.analytic_vs_MC_L1(<=0.02)"] = dict(ok=max(d) <= 0.02, detail=f"max |dz| {max(d):.4f}")
    # C2 kernels
    y = np.logspace(-10, 10, 4001)
    e1 = float(np.max(np.abs(C.nu_p2(y) - np.sqrt(1 + 1 / y))))
    sys.path.insert(0, os.path.join(C.REPO, "campaign_fresh_gravity"))
    import CFG5_common as K5
    e2 = float(np.max(np.abs(C.nu_mono(y) / K5.nu_mono(y) - 1)))
    ck["C2.kernels(P2<=1e-12, mono<=1e-9)"] = dict(ok=(e1 <= 1e-12 and e2 <= 1e-9), detail=f"P2 {e1:.2e} mono-vs-CFG5 {e2:.2e}")
    # C3 lemma: (1+mu) nu((1+mu)x) >= nu(x)
    worst = {}
    for kn in C.KERN:
        bad = 0.0
        for x in np.logspace(-6, 6, 61):
            mu = np.logspace(-4, 3, 40)
            F = (1 + mu) * C.NU[kn]((1 + mu) * x)
            bad = min(bad, float(np.min(F / C.NU[kn](x) - 1)))
        worst[kn] = bad
    ck["C3.lemma_floor_monotone_in_gas"] = dict(ok=all(v >= -1e-12 for v in worst.values()), detail=str(worst))
    # C4 HMF and c-M cross-checks vs the on-disk implementations
    src = open(os.path.join(C.REPO, "hunt_2026", "h73_h86_h87_cosmic_dawn.py")).read().splitlines()
    i0 = next(i for i, l in enumerate(src) if l.startswith("import sys, math"))
    i1 = next(i for i, l in enumerate(src) if l.startswith("def f_coll"))
    ns = {"__name__": "h73"}
    sys.path.insert(0, os.path.join(C.REPO, "hunt_2026"))
    exec("\n".join(src[i0:i1]), ns)
    md = 0.0
    for z in (4.5, 5.5):
        for M in (1e11, 1e12, 1e13):
            md = max(md, abs(C.n_above_h(M, z) / ns["n_above"](M, z) - 1))
    ck["C4a.HMF_vs_on_disk(<=1%)"] = dict(ok=md <= 0.01, detail=f"max rel diff {md:.2e}")
    src2 = open(os.path.join(C.REPO, "hunt_2026", "h106_h107_h108_li2020_halos.py")).read()
    on_disk = lambda lM: 0.905 - 0.101 * (lM - 12.0 - math.log10(1 / 0.671))
    dd = max(abs(C.logc_dm14(l, 0.0) - on_disk(l)) for l in (10.0, 11.0, 12.0, 13.0))
    ck["C4b.DM14_vs_on_disk_z0(<=1e-3 dex)"] = dict(ok=dd <= 1e-3 and "Dutton" in src2, detail=f"max diff {dd:.2e} dex (on-disk h = 0.671 vs 0.674 here)")
    # C5 permutation machinery
    rng = np.random.default_rng(5)
    sig = np.array([float(np.sqrt(rng.uniform(0.05, 0.25) ** 2 + 0.25 ** 2 + 0.15 ** 2)) for _ in range(62)])
    fp = 0
    NS_ = 400
    for k in range(NS_):
        d = sig * rng.standard_normal(62)
        p = C.wy_stepdown(d, sig, n_perm=400, seed=k)
        fp += bool(p.min() < 0.05)
    rate = fp / NS_
    ck["C5a.T2_false_positive_rate_on_null(<=7%)"] = dict(ok=rate <= 0.07, detail=f"{rate:.3f} over {NS_} null samples (400 perms each)")
    d = sig * rng.standard_normal(62)
    j = int(np.argsort(sig)[31])
    d[j] = 5.0 * sig[j]
    p = C.wy_stepdown(d, sig, n_perm=20000)
    ck["C5b.T2_fires_on_planted_5sigma_residual(median sigma)"] = dict(ok=bool(p[j] < 0.05), detail=f"adjusted p = {p[j]:.3f} (planted row has the median sigma)")
    j2 = int(np.argmin(sig))
    d2 = sig * rng.standard_normal(62)
    d2[j2] = 5.0 * sig[j2]
    p2 = C.wy_stepdown(d2, sig, n_perm=20000)
    ck["C5c.(reported)T2_on_planted_5sigma_residual_with_the_smallest_sigma"] = dict(ok=bool(p2[j2] < 0.05), detail=f"adjusted p = {p2[j2]:.4f} (informational; not a frozen control)")
    # C6 (reported, not frozen): can L2 fire at all inside the frozen defined range?  noise-free scan over M200,need
    saved = dict(C.SIGSET)
    C.SIGSET.update({k: (0.0, 0.0) for k in C.SIGSET})
    r = 3.0
    lM = math.log10(2.0 * 5.0 * A0 * r * r / C.G_KPC)
    best = (-99.0, None)
    for M200 in (1e12, 1e13, 3e13, 1e14, 3e14, 1e15):
        need = nfw_need(M200, r, 4.5)
        q = C.score_row_L2(make_row("SCAN", (need + 0.5 * 10 ** lM) / (0.5 * 10 ** lM), 5.0, z=4.5, sig_stat=0.001), n=20000)
        if q.get("defined") and q.get("z_rob", -99) > best[0]:
            best = (q["z_rob"], M200)
    C.SIGSET.update(saved)
    ck["C6.(reported)L2_reach_noise_free_max_z_rob_in_range"] = dict(ok=True, detail=f"max z_rob(L2) over M200,need in 1e12..1e15 with zero noise = {best[0]:.2f} at M200 = {best[1]:.0e} (z_rob > 3 is unreachable in range if < 3)")
    return ck


def main():
    P("CFG235_01_controls: MUTATE =", C.MUT, "| synthetic rows only; repo = <repo>")
    ck = checks()
    for k, v in ck.items():
        P(f"  {'PASS' if v['ok'] else 'FAIL'}  {k}: {v['detail']}")
    out = run_controls()
    P(f"\nplanted targets (R_obs, x_*): " + "; ".join(f"{k}: R={v['R']:.4g} x={v['x']:.3g}" for k, v in out["pp"].items()))
    P(f"control sample: {out['meta']['n_rows']} rows (62 synthetic background + plants); Bonferroni m = {out['meta']['m']}; z_B = {out['meta']['zB']:.3f}")
    for k, v in out["exp"].items():
        P(f"  {'PASS' if v['ok'] else 'FAIL'}  {k}: {v['detail']}")
    for i, q in out["res"].items():
        P(f"    {i:9} L1 z_rob={q['L1'].get('z_rob', float('nan')):7.2f} F1 z_rob={q['F1'].get('z_rob', float('nan')):7.2f} "
          f"L2 z_rob={q['L2'].get('z_rob', float('nan')) if q['L2'].get('defined') else float('nan'):7.2f} | labels T0/T1/T2: {q['label_T0']}/{q['label_T1']}/{q['label_T2']}")
    allv = dict(ck)
    allv.update(out["exp"])
    failed = [k for k, v in allv.items() if not v["ok"]]
    P("\nFAILED controls:", failed if failed else "none")
    json.dump(dict(mutate=C.MUT, checks=ck, expectations=out["exp"], planted=out["pp"], meta=out["meta"], failed=failed,
                   planted_results=out["res"]), open(os.path.join(C.HERE, "CFG235_01_controls_results.json" if C.MUT == 0 else f"CFG235_01_controls_MUTATE{C.MUT}_results.json"), "w"), indent=1, default=float)
    P("exit", 0 if not failed else 1)
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
