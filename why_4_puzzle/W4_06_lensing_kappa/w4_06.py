#!/usr/bin/env python3
"""W4-06 -- is there a 4 in weak lensing? kappa fitted to KiDS-1000 isolated blue lenses (Brouwer+21 RAR files).

Criteria: FROZEN_CRITERIA.md (committed alone, 6f967094d). Observational lane (obs class), not a derivation.
Data: real_research/data/lensing_rar/brouwer2021_rar/ (read only). Loader copied unchanged from CFG829.
Light: numpy, one process, seconds. Run from the repo root:
    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_06_lensing_kappa/w4_06.py > why_4_puzzle/W4_06_lensing_kappa/w4_06.out
    W4_06_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_06_lensing_kappa/w4_06.py \
        > why_4_puzzle/W4_06_lensing_kappa/w4_06_MUTATE.out
MUTATE: g_obs x 1.21 (kappa must rise by ~1.46 in the deep regime); exit 1 when it bites.
kappa = 1/2 FITTED. Not theory closed.
"""
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
CFG885 = os.path.join(REPO, "campaign_fresh_gravity", "CFG885_kids_rar_native_distances", "cfg885_results.json")
MUT = os.environ.get("W4_06_MUTATE") == "1"
SUF = "_MUTATE" if MUT else ""
checks = []


def check(name, detail, ok, kind="K"):
    checks.append({"name": name, "detail": detail, "pass": bool(ok), "kind": kind})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# === COMPUTE BEGIN (I1 scans this block: no footing a0 value and no measured kappa upstream of the fit) ===
G_SI, C_SI = 6.67430e-11, 2.99792458e8
RHO_CRIT = 8.533238720309458e-27          # GF1 register (H0 67.4)
OMEGA_L = 0.685                           # GF1 register; converts a fitted a0 <-> kappa only
S = {"rho_DE": C_SI * math.sqrt(G_SI * OMEGA_L * RHO_CRIT), "rho_crit": C_SI * math.sqrt(G_SI * RHO_CRIT)}
G_pc, PCm = 4.52e-30, 3.086e16            # CFG829's ESD -> acceleration constants
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
nu_s = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / np.maximum(y, 1e-15)))
BLUE = ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0)
W = (10 ** -13.3, 10 ** -11.9)
WC = (10 ** -11.9, 10 ** -10.9)
KGRID = np.exp(np.linspace(math.log(0.05), math.log(5.0), 4001))


def load(esd, cov, binmin=None):           # copied from CFG829 (without its MUTATE factor)
    d = np.loadtxt(os.path.join(B, esd)); gb, esdt, bias = d[:, 0], d[:, 1], d[:, 4]
    go = 4 * G_pc * esdt / bias * PCm
    c = np.loadtxt(os.path.join(B, cov)); n = len(gb); Cm = np.zeros((n, n))
    sel = c if binmin is None else c[(np.isclose(c[:, 0], binmin)) & (np.isclose(c[:, 1], binmin))]

    def idx(x):
        k = int(np.argmin(np.abs(gb / x - 1))); return k if abs(gb[k] / x - 1) < 1e-3 else None
    for row in sel:
        i, j = idx(row[2]), idx(row[3])
        if i is not None and j is not None:
            Cm[i, j] = row[4] / row[6]
    Cm *= (4 * G_pc * PCm) ** 2
    return gb, go, Cm


def amp(gb, go, Cm, gl, win):              # CFG829's amplitude estimator (for K1)
    m = (gb >= win[0]) & (gb < win[1])
    Ci = np.linalg.inv(Cm[np.ix_(m, m)]); a = gl[m] @ Ci @ gl[m]
    return float(gl[m] @ Ci @ go[m] / a), float(a ** -0.5), int(m.sum())


def fit_kappa(gb, go, Cm, win, nu, s):
    m = (gb >= win[0]) & (gb < win[1])
    n = int(m.sum())
    if n < 3:
        return {"n": n, "status": "NOT DIAGNOSTIC (<3 points)"}
    Ci = np.linalg.inv(Cm[np.ix_(m, m)])
    g, o = gb[m], go[m]
    chi = np.array([(o - g * nu(g / (k * s))) @ Ci @ (o - g * nu(g / (k * s))) for k in KGRID])
    i = int(np.argmin(chi)); kb = float(KGRID[i]); cmin = float(chi[i])
    edge = i in (0, len(KGRID) - 1)
    lo = hi = None
    left = np.where(chi[:i] >= cmin + 1)[0]
    right = np.where(chi[i:] >= cmin + 1)[0]
    if len(left):
        lo = float(KGRID[left[-1]])
    if len(right):
        hi = float(KGRID[i + right[0]])
    chi_at = lambda k: float(np.interp(math.log(k), np.log(KGRID), chi))
    return {"n": n, "kappa": kb, "lo": lo, "hi": hi, "chi2_min": cmin, "edge": edge,
            "dchi2_0461_vs_05": chi_at(math.sqrt(2 / (3 * math.pi))) - chi_at(0.5),
            "chi2_at_half": chi_at(0.5), "status": "ok"}
# === COMPUTE END ===


# grading constants (CFG493 primary; grading only, never upstream of a fit)
REF = {"rho_DE": (0.417, 0.095), "rho_crit": (0.345, 0.078)}


def sig(f):
    if f.get("lo") is None or f.get("hi") is None:
        return None
    return 0.5 * (f["hi"] - f["lo"])


def main():
    print("W4-06  kappa from KiDS-1000 isolated blue-lens lensing (B21)" + ("  [MUTATE g_obs x1.21]" if MUT else ""))
    print("law g_obs = g_bar nu(g_bar/(kappa s)), s = c sqrt(G rho); obs lane. kappa = 1/2 FITTED. Not theory closed.\n")
    src = open(os.path.abspath(__file__)).read()
    block = src.split("# === COMPUTE BEGIN")[1].split("# === COMPUTE END")[0]
    forbidden = [r"9\.36", r"9\.3603", r"1\.13\d*e-10", r"1\.1312", r"1\.2e-10", r"0\.417", r"0\.45\b", r"0\.465",
                 r"0\.53\b", r"0\.551", r"5\.78", r"0\.1727"]
    hits = [x for x in forbidden if re.search(x, block)]
    check("I1 forbidden inputs", f"tokens in the compute block: {hits or 'none'}", not hits, "B")

    gb, go, Cm = load(*BLUE)
    if MUT:
        go, Cm = go * 1.21, Cm * 1.21 ** 2
    print(f"blue lenses: {len(gb)} points, g_bar {gb.min():.2e} .. {gb.max():.2e}; s(rho_DE) = {S['rho_DE']:.5e}, "
          f"s(rho_crit) = {S['rho_crit']:.5e}")

    # K1: CFG829's primary amplitude with the law at kappa = 1/2 (computed, not typed)
    A, sA, nA = amp(gb, go, Cm, gb * nu_e(gb / (0.5 * S["rho_DE"])), W)
    k1_ok = abs(A - 1.016) < 1e-3 and abs(sA - 0.086) < 1e-3
    check("K1 reproduce CFG829", f"A = {A:.4f} +- {sA:.4f} ({nA} pts) vs CFG829 1.016 +- 0.086", k1_ok if not MUT else True,
          "B" if MUT else "K")

    res = {}
    print("\nfits (kappa best, Delta chi2 = 1 interval, n points, chi2_min, Delta chi2(0.461 - 0.5))")
    for foot in ("rho_DE", "rho_crit"):
        for kn, nu in (("nu_simple", nu_s), ("nu_e", nu_e)):
            for wn, win in (("W", W), ("WC", WC), ("W+WC", (W[0], WC[1])), ("all", (0, 1))):
                f = fit_kappa(gb, go, Cm, win, nu, S[foot])
                res[f"{foot}|{kn}|{wn}"] = f
                if f["status"] != "ok":
                    print(f"  {foot:8s} {kn:9s} {wn:5s} {f['status']}")
                    continue
                print(f"  {foot:8s} {kn:9s} {wn:5s} kappa {f['kappa']:.3f} [{f['lo'] or float('nan'):.3f}, "
                      f"{f['hi'] or float('nan'):.3f}]  n {f['n']:2d}  chi2 {f['chi2_min']:.1f}  "
                      f"dchi2 {f['dchi2_0461_vs_05']:+.2f}{'  EDGE' if f['edge'] else ''}")

    # systematics on the PRIMARY (rho_DE, nu_simple, W) and its rho_crit twin
    T = json.load(open(CFG885))["T_window_range"]["Fig-8_RAR-KiDS-isolated_Colorbin_1.txt"]
    syst = {}
    print(f"\nsystematics on the PRIMARY (S2 T bracket from CFG885: {T[0]:.4f}, {T[1]:.4f})")
    for foot in ("rho_DE", "rho_crit"):
        rows = {}
        for lab, (gbx, gox, Cx, win) in {
            "S1 M* -0.2 dex": (gb * 10 ** -0.2, go, Cm, W), "S1 M* +0.2 dex": (gb * 10 ** 0.2, go, Cm, W),
            f"S2 T {T[0]:.3f}": (gb, go * T[0], Cm * T[0] ** 2, W), f"S2 T {T[1]:.3f}": (gb, go * T[1], Cm * T[1] ** 2, W),
            "S3 window -0.3 dex": (gb, go, Cm, (W[0] * 10 ** -0.3, W[1] * 10 ** -0.3)),
            "S3 window +0.3 dex": (gb, go, Cm, (W[0] * 10 ** 0.3, W[1] * 10 ** 0.3))}.items():
            f = fit_kappa(gbx, gox, Cx, win, nu_s, S[foot])
            rows[lab] = f
            ks = f"kappa {f['kappa']:.3f} [{f['lo'] or float('nan'):.3f}, {f['hi'] or float('nan'):.3f}] n {f['n']}" \
                if f["status"] == "ok" else f["status"]
            print(f"  {foot:8s} {lab:20s} {ks}")
        syst[foot] = rows

    # mock recovery (K2), on the PRIMARY
    rng = np.random.default_rng(101)
    m = (gb >= W[0]) & (gb < W[1])
    L = np.linalg.cholesky(Cm[np.ix_(m, m)])
    prim = res["rho_DE|nu_simple|W"]
    k2 = {}
    for ktrue in (0.30, 0.50):
        rec = []
        for _ in range(50):
            mock = go.copy()
            mock[m] = gb[m] * nu_s(gb[m] / (ktrue * S["rho_DE"])) + L @ rng.standard_normal(int(m.sum()))
            f = fit_kappa(gb, mock, Cm, W, nu_s, S["rho_DE"])
            rec.append(f["kappa"])
        med = float(np.median(rec))
        s_stat = sig(prim) or float("nan")
        k2[ktrue] = {"median": med, "spread16_84": [float(np.percentile(rec, 16)), float(np.percentile(rec, 84))]}
        check(f"K2 mock recovery kappa_true {ktrue}", f"median {med:.3f} within the mocks' own 1-sigma (16-84%: "
              f"{k2[ktrue]['spread16_84'][0]:.3f}-{k2[ktrue]['spread16_84'][1]:.3f}); PRIMARY sigma_stat {s_stat:.3f}",
              abs(med - ktrue) <= (k2[ktrue]["spread16_84"][1] - k2[ktrue]["spread16_84"][0]) / 2, "B")

    ok3 = all((not r["edge"]) and r["lo"] is not None and r["hi"] is not None
              for k_, r in res.items() if k_.endswith("|W") and r["status"] == "ok")
    check("K3 interior minimum and brackets (PRIMARY windows)", f"{ok3}", ok3, "B")
    k4 = 0.5 * A ** 2
    print(f"\nK4 (report): deep-limit 1/2 A^2 = {k4:.3f} vs fitted PRIMARY (nu_e, rho_DE) "
          f"{res['rho_DE|nu_e|W']['kappa']:.3f}")

    # grading
    print("\ngrading")
    grade = {}
    for foot in ("rho_DE", "rho_crit"):
        f = res[f"{foot}|nu_simple|W"]
        s_stat = sig(f)
        ks = [r["kappa"] for r in syst[foot].values() if r["status"] == "ok"]
        env = (min(ks), max(ks))
        s1 = [syst[foot]["S1 M* -0.2 dex"]["kappa"], syst[foot]["S1 M* +0.2 dex"]["kappa"]]
        s_s1 = 0.5 * abs(s1[0] - s1[1])
        kref, sref = REF[foot]
        z_stat = (f["kappa"] - kref) / math.hypot(s_stat, sref)
        z_tot = (f["kappa"] - kref) / math.hypot(math.hypot(s_stat, s_s1), sref)
        frac = math.hypot(s_stat, s_s1) / f["kappa"]
        dchi = f["dchi2_0461_vs_05"]
        sep = "SEPARATED" if abs(dchi) >= 9 else ("NOT SEPARATED" if abs(dchi) < 1 else "WEAK")
        if f["edge"] or f["n"] < 3:
            verdict = "NOT DIAGNOSTIC"
        elif frac <= 0.028:
            verdict = "DECISIVE"
        elif abs(z_tot) <= 2:
            verdict = "CONSISTENT, NOT DECISIVE"
        elif abs(z_tot) <= 3:
            verdict = "TENSION"
        else:
            verdict = "DISAGREE"
        grade[foot] = {"kappa": f["kappa"], "sigma_stat": s_stat, "S1_halfwidth": s_s1, "envelope": env,
                       "z_stat": z_stat, "z_total": z_tot, "frac_sigma_total": frac, "dchi2_0461_vs_05": dchi,
                       "half_vs_0461": sep, "verdict": verdict}
        print(f"  {foot:8s} kappa_lens = {f['kappa']:.3f} +- {s_stat:.3f} (stat) +- {s_s1:.3f} (S1 M*); systematic envelope "
              f"{env[0]:.3f}-{env[1]:.3f}; vs CFG493 {kref} +- {sref}: z_stat {z_stat:+.2f}, z_total {z_tot:+.2f}; "
              f"sigma_total/kappa {frac:.1%}; 1/2 vs 0.461 dchi2 {dchi:+.2f} ({sep}) -> {verdict}")
    lane = grade["rho_DE"]["verdict"]
    print(f"\nLANE VERDICT (rho_DE, the canonical footing): {lane}; rho_crit: {grade['rho_crit']['verdict']}")

    out = {"mutate": MUT, "s": S, "K1": {"A": A, "sA": sA, "n": nA}, "fits": res, "systematics": syst, "K2": k2,
           "grade": grade, "lane_verdict": lane, "checks": checks}
    json.dump(out, open(os.path.join(HERE, f"w4_06_results{SUF}.json"), "w"), indent=1, default=float)
    n_pass = sum(c["pass"] for c in checks)
    print(f"\nchecks: {n_pass}/{len(checks)} pass")
    if MUT:
        try:
            base = json.load(open(os.path.join(HERE, "w4_06_results.json")))
            kb = base["grade"]["rho_DE"]["kappa"]
            ratio = grade["rho_DE"]["kappa"] / kb
            bite = abs(ratio - 1) > 0.01
            print(f"MUTATE: kappa ratio vs normal run {ratio:.3f} (expected ~1.46 in the deep regime); bites {bite}; "
                  f"bookkeeping passes {all(c['pass'] for c in checks if c['kind'] == 'B')}")
            sys.exit(1 if bite and all(c["pass"] for c in checks if c["kind"] == "B") else 2)
        except OSError:
            sys.exit(2)
    sys.exit(0 if n_pass == len(checks) else 1)


if __name__ == "__main__":
    main()
