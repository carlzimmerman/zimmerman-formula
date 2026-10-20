#!/usr/bin/env python3
"""W4-10 -- is there ONE 4? kappa in every KiDS-1000 isolated-lens subsample (B21), with W4-06's committed estimator.

Criteria: FROZEN_CRITERIA.md (committed alone, 61810a121). Observational lane (obs). Reuses w4_06.py (load, fit_kappa, S, W, nu_s)
by import; B21 files read only. Light: numpy, one process, seconds. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_10_one_kappa_lensing/w4_10.py > why_4_puzzle/W4_10_one_kappa_lensing/w4_10.out
    W4_10_MUTATE=1 ... > .../w4_10_MUTATE.out      (universal mock sky; must read UNIVERSAL everywhere; exit 1 when it bites)
kappa = 1/2 FITTED. Not theory closed.
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("w4_06", os.path.join(REPO, "why_4_puzzle", "W4_06_lensing_kappa", "w4_06.py"))
w6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w6)
MUT = os.environ.get("W4_10_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
checks = []


def check(name, detail, ok, kind="K"):
    checks.append({"name": name, "detail": detail, "pass": bool(ok), "kind": kind})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


PART = {
    "C colour": {"blue": ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
                 "red": ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5)},
    "S Sersic": {"n<2": ("Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0),
                 "n>2": ("Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0)},
    "M mass": {f"M{i} (logM* from {m})": (f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt",
                                           "Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt", m)
               for i, m in ((1, 8.5), (2, 10.3), (3, 10.6), (4, 10.8))},
}
REPORT = {"isolated dwarfs": ("Fig-10_RAR-KiDS-isolated-dwarfs_Nobins.txt", "Fig-10_RAR-KiDS-isolated-dwarfs_covmatrix.txt", None),
          "all KiDS": ("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt", "Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt", None),
          "all KiDS + hot gas": ("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt", "Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt", None),
          "GAMA all": ("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt", "Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt", None)}
MASS_CENTRE = {"M1": (8.5 + 10.3) / 2, "M2": (10.3 + 10.6) / 2, "M3": (10.6 + 10.8) / 2, "M4": (10.8 + 11.0) / 2}


def chi2_sf(x, k):
    """survival function of chi2 with k dof (regularised upper incomplete gamma, series/continued fraction)"""
    try:
        from scipy.stats import chi2
        return float(chi2.sf(x, k))
    except ImportError:
        a, z = k / 2.0, x / 2.0
        if z <= 0:
            return 1.0
        term, s, n = 1.0 / a, 1.0 / a, 0
        while abs(term) > 1e-14 * abs(s) and n < 10000:
            n += 1
            term *= z / (a + n)
            s += term
        p_low = s * math.exp(-z + a * math.log(z) - math.lgamma(a))
        return max(0.0, 1.0 - p_low)


def fit(spec_, rng=None, kappa_mock=None):
    f, c, bm = spec_
    gb, go, Cm = w6.load(f, c, bm)
    m = (gb >= w6.W[0]) & (gb < w6.W[1])
    pd = bool(m.sum() >= 1 and np.all(np.linalg.eigvalsh(Cm[np.ix_(m, m)]) > 0)) if m.sum() else False
    if kappa_mock is not None and m.sum() >= 1:
        Lc = np.linalg.cholesky(Cm[np.ix_(m, m)])
        go = go.copy()
        go[m] = gb[m] * w6.nu_s(gb[m] / (kappa_mock * w6.S["rho_DE"])) + Lc @ rng.standard_normal(int(m.sum()))
    r = w6.fit_kappa(gb, go, Cm, w6.W, w6.nu_s, w6.S["rho_DE"])
    r["posdef"] = pd
    if r.get("status") == "ok" and r["lo"] is not None and r["hi"] is not None and not r["edge"]:
        r["sigma"] = 0.5 * (r["hi"] - r["lo"])
        r["usable"] = True
    else:
        r["usable"] = False
    return r


def main():
    print("W4-10  is there ONE kappa? KiDS-1000 isolated-lens subsamples (B21), W4-06 estimator, CFG829 window, rho_DE"
          + ("  [MUTATE: universal mock sky]" if MUT else ""))
    print("obs lane. kappa = 1/2 FITTED. Not theory closed.\n")
    blue_real = fit(PART["C colour"]["blue"])
    check("K1 reproduce W4-06 blue PRIMARY", f"kappa {blue_real['kappa']:.3f} [{blue_real['lo']:.3f}, {blue_real['hi']:.3f}] "
          "vs 0.520 [0.433, 0.614]", abs(blue_real["kappa"] - 0.520) < 2e-3 and abs(blue_real["lo"] - 0.433) < 2e-3
          and abs(blue_real["hi"] - 0.614) < 2e-3, "B")
    rng = np.random.default_rng(101)
    kmock = blue_real["kappa"] if MUT else None

    res, tests, posdef_bad = {}, {}, []
    for pname, subs in PART.items():
        print(f"\npartition {pname}")
        rows = {}
        for sname, sp_ in subs.items():
            r = fit(sp_, rng, kmock)
            rows[sname] = r
            if not r["posdef"]:
                posdef_bad.append(sname)
            if r.get("status") == "ok":
                print(f"  {sname:22s} kappa {r['kappa']:.3f} [{r['lo'] or float('nan'):.3f}, {r['hi'] or float('nan'):.3f}]"
                      f"  n {r['n']}  chi2 {r['chi2_min']:.1f}{'  EDGE' if r['edge'] else ''}{'' if r['usable'] else '  (dropped)'}")
            else:
                print(f"  {sname:22s} {r.get('status')} (dropped)")
        use = {k: v for k, v in rows.items() if v["usable"]}
        if len(use) >= 2:
            w = np.array([1 / v["sigma"] ** 2 for v in use.values()])
            kk = np.array([v["kappa"] for v in use.values()])
            kbar = float((w * kk).sum() / w.sum())
            chi = float((w * (kk - kbar) ** 2).sum())
            dof = len(use) - 1
            p = chi2_sf(chi, dof)
            verdict = "UNIVERSAL" if p > 0.05 else ("NOT UNIVERSAL" if p < 0.0027 else "INTERMEDIATE")
        else:
            kbar, chi, dof, p, verdict = None, None, None, None, "NOT DIAGNOSTIC"
        tests[pname] = {"kbar": kbar, "chi2": chi, "dof": dof, "p": p, "verdict": verdict,
                        "dropped": [k for k, v in rows.items() if not v["usable"]]}
        print(f"  T1 {pname}: kappa_bar {kbar if kbar is None else round(kbar, 3)}, chi2 {chi if chi is None else round(chi, 2)}"
              f" / {dof} dof, p {p if p is None else f'{p:.2e}'} -> {verdict}")
        res[pname] = rows

    print("\nreport-only subsamples")
    rep = {}
    for sname, sp_ in REPORT.items():
        r = fit(sp_, rng, kmock)
        rep[sname] = r
        if not r["posdef"]:
            posdef_bad.append(sname)
        if r.get("status") == "ok":
            print(f"  {sname:22s} kappa {r['kappa']:.3f} [{r['lo'] or float('nan'):.3f}, {r['hi'] or float('nan'):.3f}]  "
                  f"n {r['n']}{'  EDGE' if r['edge'] else ''}")
        else:
            print(f"  {sname:22s} {r.get('status')}")
    check("K2 covariance blocks positive definite", f"failures {posdef_bad or 'none'}", not posdef_bad, "B")

    blue = res["C colour"]["blue"]
    t2 = t3 = t4 = None
    if rep["all KiDS + hot gas"]["usable"] and blue["usable"]:
        h = rep["all KiDS + hot gas"]
        z2 = (h["kappa"] - blue["kappa"]) / math.hypot(h["sigma"], blue["sigma"])
        t2 = {"kappa_all": rep["all KiDS"].get("kappa"), "kappa_hot": h["kappa"], "z_vs_blue": z2,
              "restores": abs(z2) <= 2}
        print(f"\nT2 hot gas: kappa(all) {rep['all KiDS'].get('kappa', float('nan')):.3f} -> kappa(all + hot gas) "
              f"{h['kappa']:.3f}; vs blue z {z2:+.2f} -> {'restores one kappa' if abs(z2) <= 2 else 'does NOT restore one kappa'}")
    if rep["GAMA all"]["usable"] and rep["all KiDS"]["usable"]:
        g, kd = rep["GAMA all"], rep["all KiDS"]
        z3 = (g["kappa"] - kd["kappa"]) / math.hypot(g["sigma"], kd["sigma"])
        t3 = {"z": z3}
        print(f"T3 GAMA vs KiDS all: {g['kappa']:.3f} vs {kd['kappa']:.3f}, z {z3:+.2f}")
    mrows = [(MASS_CENTRE[k.split()[0]], v["kappa"], v["sigma"]) for k, v in res["M mass"].items() if v["usable"]]
    if len(mrows) >= 2:
        x = np.array([r[0] for r in mrows]); y = np.array([r[1] for r in mrows]); s = np.array([r[2] for r in mrows])
        w = 1 / s ** 2
        X = np.vstack([np.ones_like(x), x]).T
        cov = np.linalg.inv(X.T @ (w[:, None] * X))
        beta = cov @ X.T @ (w * y)
        t4 = {"slope": float(beta[1]), "sigma": float(math.sqrt(cov[1, 1])), "z": float(beta[1] / math.sqrt(cov[1, 1]))}
        print(f"T4 mass trend: d kappa / d log M* = {beta[1]:+.3f} +- {math.sqrt(cov[1, 1]):.3f} (z {t4['z']:+.2f})")

    v = {k: t["verdict"] for k, t in tests.items()}
    if any(x == "NOT DIAGNOSTIC" for x in v.values()) and sum(x == "NOT DIAGNOSTIC" for x in v.values()) >= 2:
        lane = "NOT DIAGNOSTIC"
    elif all(x == "UNIVERSAL" for x in v.values()):
        lane = "ONE KAPPA"
    else:
        early_high = (res["C colour"]["red"].get("kappa", 0) > blue["kappa"]) and \
                     (res["S Sersic"]["n>2"].get("kappa", 0) > res["S Sersic"]["n<2"].get("kappa", 0))
        typed = v["C colour"] == "NOT UNIVERSAL" or v["S Sersic"] == "NOT UNIVERSAL"
        lane = "ONE KAPPA FOR LATE TYPES ONLY" if (typed and early_high) else (
            "NO SINGLE KAPPA" if any(x == "NOT UNIVERSAL" for x in v.values()) else "INTERMEDIATE")
    print(f"\nLANE VERDICT: {lane}   (partitions: {v})")
    json.dump({"mutate": MUT, "partitions": res, "report": rep, "T1": tests, "T2": t2, "T3": t3, "T4": t4,
               "lane_verdict": lane, "checks": checks},
              open(os.path.join(HERE, f"w4_10_results{SUF}.json"), "w"), indent=1, default=float)
    n_pass = sum(x["pass"] for x in checks)
    print(f"\nchecks: {n_pass}/{len(checks)} pass")
    if MUT:
        try:
            base = json.load(open(os.path.join(HERE, "w4_10_results.json")))["lane_verdict"]
        except OSError:
            base = None
        univ = all(x == "UNIVERSAL" for x in v.values())
        bite = univ and base is not None and base != lane
        print(f"MUTATE: mock sky reads UNIVERSAL in every partition {univ}; real-data verdict '{base}' differs {bite}")
        sys.exit(1 if bite and n_pass == len(checks) else 2)
    sys.exit(0 if n_pass == len(checks) else 1)


if __name__ == "__main__":
    main()
