#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cfg816_r.py -- the Gaia DR4 R statistic, scored by the rules frozen in FROZEN_CRITERIA.md (CFG816; CFG800's rule with Amendment 22's sigma_R).

MODES
  python3 cfg816_r.py                 controls C0-C3 on synthetic pairs (C4 = the DR3 code-path run is NOT RUN here: it needs the owner's yes and a download)
  python3 cfg816_r.py --mutate        MUTATE: multiply v-tilde at x > 1 by 1.2 on a synthetic null; the script must detect it (exit 1)
  python3 cfg816_r.py --dr3 TABLE     C4: the same code on the registered DR3 sample (writes cfg816_r_dr3_results.json)
  python3 cfg816_r.py --dr4 TABLE     THE RUN, ONCE, after DR4 is public and only on the owner's yes (writes cfg816_r_dr4_results.json; refuses a second run)

PAIR TABLE (CSV, one row per pair; built from the registered pipeline's stage-G pair array)
  sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc            (the registered ingest_csv columns)
  plx_err_frac, ruwe1, ruwe2, ipd1, ipd2, vt_err         (Cookson checklist inputs; REQUIRED, never silently skipped)
  drv_kms (blank if a pair has no radial velocity), nss1, nss2 (1 = a DR4 non-single-star solution)
The table is assumed already degrouped and HR-filtered as in the registered pipeline; this script applies the numeric cuts of section 3.

INTERPRETATIONS made while implementing the frozen text (also listed in README.md; none changes a frozen threshold):
  I1  N for sigma_tot = the number of pairs that ENTER R (numerator + denominator); the numerator-only value is printed as a sensitivity.
  I2  The bootstrap resamples pairs WITHIN each regime (stratified), so the vectorised medians are exact for fixed regime sizes.
  I3  C2 (coverage) is applied to the bootstrap sigma alone, because sigma_tot contains an assumed 0.02 systematic that synthetic data do not carry and would over-cover by design;
      coverage with sigma_R is printed too. The class KILLED null-rate is checked with sigma_R.
  I4  C2 uses 300 resamples per repeat (the real run uses 2000).
  I5  C4's pass rule is: R - 1 < 2 sigma_R on the DR3 primary (the frozen text says only "no 20% boost"). The first draft also required (1.20 - R)/sigma_R > 1; it was DROPPED on
      2026-10-17, after the DR3 pair table was built (counts known, no R value computed): the registered catalogue gives only 175 + 173 pairs in the two regimes, so sigma_R ~ 0.18 and that leg
      would demand R < 1.02, failing a flat truth about 40% of the time. (1.20 - R)/sigma_R is still printed, as information.
  I6  C0 (added; not in the frozen list): the v-tilde computed here equals the registered pipeline's ingest_csv v-tilde (read-only import).
  I8  The f_tail comparison (frozen: "differs between regimes by more than its 2 sigma") uses a binomial z-test, which is invalid with few events. It is applied only if BOTH regimes
      hold at least 5 pairs with v-tilde > 2; otherwise it is reported "n/a (<5 events)" and does not trigger CONTAMINATION-LIMITED. Found by MUTATE: on a clean synthetic sample
      (f_tail ~ 0) one or two stray events gave a spurious 2.1 sigma difference.
  I7  C5 (added; not in the frozen list): the CSV path and the contamination rule, end to end on synthetic pairs: a boost carried only by NSS-flagged pairs must come out
      CONTAMINATION-LIMITED, a boost carried by every pair must come out KILLED, and a table written and read back must reproduce the in-memory statistic exactly.
"""
import os, sys, json, math, csv, argparse, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "prep_2026", "gaia_dr4_prep"))          # read-only import of the registered pipeline

# ---------------------------------------------------------------- frozen constants (FROZEN_CRITERIA.md sections 1-3)
A0_PRIMARY, A0_BRANCHES = 1.2e-10, (9.36e-11, 1.13e-10)
X_NEWT, X_MOND, RMAX_NUM_KAU, RMAX_NUM_COOKSON = 0.3, 1.0, 50.0, 30.0
SIG_FIT_N0, SIG_FIT, SIG_SYS = 30000., 0.019, 0.02
SEED, B_RUN, KILL_MIN, CONS_MIN, K_KILL, K_CONS = 20261216, 2000, 0.01, 0.01, 3.0, 2.0
ARM = {"Newton / Arm C": 1.0, "Arm A canon": 1.1614, "Arm A alt": 1.1917, "MOND 1.15": 1.15, "MOND 1.20": 1.20}
D_MAX_PC, PLX_FRAC, RUWE_MAX, DRV_MAX, VT_ERR_MAX = 130., 0.025, 1.25, 10., 0.1
BRANCHES = [  # name, dict of overrides of the primary
    ("primary",          {}),
    ("vt<=2",            {"vt_max": 2.0}),
    ("vt<=1.5",          {"vt_max": 1.5}),
    ("parallax<=1%",     {"plx": 0.01}),
    ("r_sky<=30kAU",     {"rmax_num": RMAX_NUM_COOKSON}),
    ("NSS-screened",     {"nss": True}),
    ("a0=9.36e-11",      {"a0": A0_BRANCHES[0]}),
    ("a0=1.13e-10",      {"a0": A0_BRANCHES[1]}),
]
PRIMARY = dict(a0=A0_PRIMARY, vt_max=2.5, plx=PLX_FRAC, rmax_num=RMAX_NUM_KAU, nss=False)

try:
    import wide_binary_pipeline as WBP              # read-only; the module only defines functions and constants at import
    G, MSUN, KAU = WBP.G, WBP.MSUN, WBP.KAU
except Exception as e:                              # never silent: the control C0 then reports it
    WBP = None
    G, MSUN, KAU = 6.6743e-11, 1.989e30, 1.495978707e14
    WBP_ERR = repr(e)

OUT = []
def P(s=""):
    OUT.append(s); print(s)


# ---------------------------------------------------------------- the statistic
def vtilde(t):
    return t["v_perp_kms"] * 1e3 / np.sqrt(G * (t["M1_msun"] + t["M2_msun"]) * MSUN / (t["sep_kAU"] * KAU))

def xval(t, a0):
    return t["sep_kAU"] * KAU / np.sqrt(G * (t["M1_msun"] + t["M2_msun"]) * MSUN / a0)

def base_mask(t, cfg):
    vt, m = vtilde(t), np.ones(len(t["sep_kAU"]), bool)
    m &= t["d_pc"] < D_MAX_PC
    m &= t["plx_err_frac"] <= cfg["plx"]
    m &= (t["ruwe1"] < RUWE_MAX) & (t["ruwe2"] < RUWE_MAX)
    m &= (t["ipd1"] == 0) & (t["ipd2"] == 0)
    m &= np.isnan(t["drv_kms"]) | (np.abs(t["drv_kms"]) < DRV_MAX)
    m &= vt <= cfg["vt_max"]
    m &= t["vt_err"] < VT_ERR_MAX
    if cfg["nss"]:
        m &= (t["nss1"] == 0) & (t["nss2"] == 0)
    return m

def sigma_tot(N):
    return math.hypot(SIG_FIT * math.sqrt(SIG_FIT_N0 / N), SIG_SYS)

def boot_median_ratio(a, b, rng, B):
    """stratified bootstrap of median(a)/median(b); chunked to keep memory small"""
    out = np.empty(B); done = 0
    step = max(1, int(2_000_000 // max(len(a), len(b))))
    while done < B:
        k = min(step, B - done)
        ma = np.median(a[rng.integers(0, len(a), (k, len(a)), dtype=np.int32)], axis=1)
        mb = np.median(b[rng.integers(0, len(b), (k, len(b)), dtype=np.int32)], axis=1)
        out[done:done + k] = ma / mb; done += k
    return out

def classify(R, sR):
    if R - 1 >= KILL_MIN and R - 1 >= K_KILL * sR:
        return "KILLED"
    if abs(R - 1) < CONS_MIN and K_CONS * sR <= CONS_MIN:
        return "CONSISTENT"
    return "UNDECIDED"

def statistic(t, cfg, rng, B):
    vt = vtilde(t); x = xval(t, cfg["a0"]); bm = base_mask(t, cfg)
    num = bm & (x > X_MOND) & (t["sep_kAU"] <= cfg["rmax_num"])
    den = bm & (x < X_NEWT)
    n1, n2 = int(num.sum()), int(den.sum())
    if n1 < 20 or n2 < 20:
        return dict(ok=False, n_num=n1, n_den=n2, note="fewer than 20 pairs in a regime: no statistic")
    a, b = vt[num], vt[den]
    R = float(np.median(a) / np.median(b))
    sb = float(boot_median_ratio(a, b, rng, B).std(ddof=1)) if B else float("nan")
    N = n1 + n2
    st, st_numonly = sigma_tot(N), sigma_tot(n1)
    sR = max(st, sb) if B else st
    p1, p2 = float((a > 2).mean()), float((b > 2).mean())
    ev1, ev2 = int((a > 2).sum()), int((b > 2).sum())
    pp = (p1 * n1 + p2 * n2) / N
    sdiff = math.sqrt(max(pp * (1 - pp), 1e-12) * (1 / n1 + 1 / n2))
    ftd = abs(p1 - p2) / sdiff if (ev1 >= 5 and ev2 >= 5) else float("nan")      # I8
    return dict(ok=True, R=R, n_num=n1, n_den=n2, N=N, sigma_tot=st, sigma_tot_numonly=st_numonly, sigma_boot=sb, sigma_R=sR,
                cls=classify(R, sR), f_tail_num=p1, f_tail_den=p2, f_tail_diff_sigma=ftd, f_tail_events=(ev1, ev2),
                dist={k: (R - v) / sR for k, v in ARM.items()})

def score(t, rng, B, label):
    res = {}
    for name, ov in BRANCHES:
        cfg = dict(PRIMARY); cfg.update(ov)
        res[name] = statistic(t, cfg, rng, B)
    P(f"=== {label}: R statistic, primary and branches (never pooled; raw numbers first, class words second)")
    for name, r in res.items():
        if not r["ok"]:
            P(f"  {name:14s} {r['note']} (n_num {r['n_num']}, n_den {r['n_den']})"); continue
        d = "  ".join(f"{k} {v:+.2f}" for k, v in r["dist"].items())
        P(f"  {name:14s} R {r['R']:.4f} (R-1 {r['R']-1:+.4f})  sigma_tot {r['sigma_tot']:.4f} sigma_boot {r['sigma_boot']:.4f} -> sigma_R {r['sigma_R']:.4f}"
          f"  N {r['N']} (num {r['n_num']}, den {r['n_den']})  f_tail {r['f_tail_num']:.3f}/{r['f_tail_den']:.3f} (diff {'n/a (<5 events)' if np.isnan(r['f_tail_diff_sigma']) else format(r['f_tail_diff_sigma'], '.1f') + ' sig'}; events {r['f_tail_events'][0]}/{r['f_tail_events'][1]})  [{r['cls']}]")
        P(f"                 distance of R to each registered number, in sigma_R: {d}")
    pr, ns = res["primary"], res["NSS-screened"]
    final = pr["cls"] if pr["ok"] else "NO DATA"
    if pr["ok"] and pr["cls"] == "KILLED":
        if (ns["ok"] and ns["cls"] != "KILLED") or pr["f_tail_diff_sigma"] > 2.0:
            final = "CONTAMINATION-LIMITED (not KILLED)"
    P(f"  PRIMARY LABEL: {final}   [KILLED = CFG740's stiffness construction only; Arms A/B/C and the settling model are scored by their own rows; the prereg gamma-hat is run separately]")
    return res, final


# ---------------------------------------------------------------- synthetic pairs (controls)
def synth(N, rng, R_true=1.0, mutate=1.0):
    sig = 0.489 / math.sqrt(2 * math.log(2))                       # Rayleigh with median 0.489
    M = np.full(N, 1.8)
    x = np.exp(rng.uniform(math.log(0.05), math.log(5.0), N))      # log-uniform in x = r_sky/r_M at a0 = 1.2e-10
    rM = np.sqrt(G * M * MSUN / A0_PRIMARY) / KAU                  # kAU
    s = x * rM
    vt = rng.rayleigh(sig, N) * np.where(x > 1, R_true * mutate, 1.0)
    vp = vt * np.sqrt(G * M * MSUN / (s * KAU)) / 1e3
    z = np.zeros(N)
    return dict(sep_kAU=s, v_perp_kms=vp, M1_msun=M / 2, M2_msun=M / 2, d_pc=np.full(N, 100.), plx_err_frac=np.full(N, 0.01),
                ruwe1=np.full(N, 1.0), ruwe2=np.full(N, 1.0), ipd1=z, ipd2=z, vt_err=np.full(N, 0.05), drv_kms=np.full(N, np.nan), nss1=z, nss2=z)


# ---------------------------------------------------------------- controls
def control_C0(rng):
    if WBP is None:
        return False, f"registered pipeline NOT importable: {WBP_ERR}"
    t = synth(500, rng)
    path = os.path.join(HERE, "cfg816_c0_tmp.csv")
    try:
        with open(path, "w") as f:
            f.write("sep_kAU,v_perp_kms,M1_msun,M2_msun,d_pc\n")
            for i in range(500):
                f.write(f"{t['sep_kAU'][i]!r},{t['v_perp_kms'][i]!r},{t['M1_msun'][i]!r},{t['M2_msun'][i]!r},{t['d_pc'][i]!r}\n")
        gN, vt_reg, _ = WBP.ingest_csv(path)
    finally:
        if os.path.exists(path): os.remove(path)
    err = float(np.max(np.abs(vt_reg / vtilde(t) - 1)))
    return err < 1e-12, f"max relative difference of v-tilde vs the registered ingest_csv = {err:.2e}"

def control_C1(rng):
    rows, ok = [], True
    for N in (1421, 30000):
        for Rt in (1.00, 1.05, 1.20):
            hit = 0
            for _ in range(200):
                r = statistic(synth(N, rng, R_true=Rt), PRIMARY, rng, 200)
                hit += abs(r["R"] - Rt) <= 2 * r["sigma_R"]
            frac = hit / 200; ok &= frac >= 0.95
            rows.append(dict(N=N, R_true=Rt, frac_within_2sigmaR=frac))
    return ok, rows

def control_C2(rng):
    N, reps, half, bs, cover_b, cover_R, killed = 1421, 1000, [], [], 0, 0, 0
    Rs = []
    for _ in range(reps):
        r = statistic(synth(N, rng), PRIMARY, rng, 300)
        cover_b += abs(r["R"] - 1.0) <= r["sigma_boot"]; cover_R += abs(r["R"] - 1.0) <= r["sigma_R"]
        killed += (r["cls"] == "KILLED"); Rs.append(r["R"]); bs.append(r["sigma_boot"])
    cb, cR, kr = cover_b / reps, cover_R / reps, killed / reps
    ok = 0.63 <= cb <= 0.73 and kr < 0.01
    return ok, dict(N=N, repeats=reps, coverage_bootstrap_sigma=cb, coverage_sigma_R=cR, killed_rate_null=kr,
                    empirical_std_of_R=float(np.std(Rs)), mean_sigma_boot=float(np.mean(bs)))

def control_C3():
    cases = [(1.083, 0.028, "UNDECIDED"), (1.085, 0.028, "KILLED"), (1.001, 0.028, "UNDECIDED"), (1.005, 0.004, "CONSISTENT"),
             (1.005, 0.006, "UNDECIDED"), (1.009, 0.002, "CONSISTENT"), (1.011, 0.002, "KILLED"), (1.05, 0.02, "UNDECIDED")]
    ok = all(classify(R, s) == w for R, s, w in cases)
    table = {N: round(sigma_tot(N), 4) for N in (1421, 5000, 10000, 30000, 100000)}
    ok &= [table[n] for n in (1421, 5000, 10000, 30000, 100000)] == [0.0896, 0.0507, 0.0385, 0.0276, 0.0225]
    kill = {N: round(1 + 3 * sigma_tot(N), 3) for N in table}
    return ok, dict(class_cases=[(R, s, classify(R, s), w) for R, s, w in cases], sigma_tot=table, kill_threshold_R=kill,
                    note="CONSISTENT is unavailable at every N: sigma_sys alone is 0.02 > 0.005")

def control_C5(rng):
    N = 30000
    # (a) contamination: half the pairs carry an NSS flag and only they are boosted x1.2 at x>1
    t = synth(N, rng); flag = (rng.random(N) < 0.5)
    vt0 = vtilde(t); x = xval(t, A0_PRIMARY)
    t["v_perp_kms"] = t["v_perp_kms"] * np.where(flag & (x > 1), 1.2, 1.0)
    t["nss1"] = flag.astype(float)
    res_a, lab_a = score(t, rng, 300, "C5a contamination (boost only on NSS-flagged pairs)")
    ok_a = lab_a.startswith("CONTAMINATION-LIMITED") and res_a["primary"]["cls"] == "KILLED" and res_a["NSS-screened"]["cls"] != "KILLED"
    # (b) genuine boost on every pair, half of them NSS-flagged: must stay KILLED
    t2 = synth(N, rng, R_true=1.2); t2["nss1"] = (rng.random(N) < 0.5).astype(float)
    res_b, lab_b = score(t2, rng, 300, "C5b genuine boost (every pair x1.2 at x>1)")
    ok_b = lab_b == "KILLED"
    # (c) CSV round trip reproduces the statistic exactly
    path = os.path.join(HERE, "cfg816_c5_tmp.csv"); cols = list(t2.keys())
    try:
        with open(path, "w") as f:
            f.write(",".join(cols) + "\n")
            for i in range(N):
                f.write(",".join("" if np.isnan(t2[c][i]) else repr(float(t2[c][i])) for c in cols) + "\n")
        t3 = read_table(path)
    finally:
        if os.path.exists(path): os.remove(path)
    r1 = statistic(t2, PRIMARY, np.random.default_rng(1), 0); r3 = statistic(t3, PRIMARY, np.random.default_rng(1), 0)
    ok_c = abs(r1["R"] - r3["R"]) < 1e-12 and r1["n_num"] == r3["n_num"]
    return ok_a and ok_b and ok_c, dict(contamination_label=lab_a, genuine_label=lab_b, csv_round_trip_R=(r1["R"], r3["R"]),
                                          ok=dict(contamination=ok_a, genuine=ok_b, csv=ok_c))

def read_table(path):
    need = ["sep_kAU", "v_perp_kms", "M1_msun", "M2_msun", "d_pc", "plx_err_frac", "ruwe1", "ruwe2", "ipd1", "ipd2", "vt_err", "drv_kms", "nss1", "nss2"]
    rows = list(csv.DictReader(open(path)))
    if not rows: sys.exit("empty table")
    miss = [c for c in need if c not in rows[0]]
    if miss: sys.exit(f"REFUSING: table lacks required columns {miss} (checklist inputs are never silently skipped)")
    return {c: np.array([float(r[c]) if r[c] != "" else np.nan for r in rows]) for c in need}


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutate", action="store_true"); ap.add_argument("--dr3"); ap.add_argument("--dr4")
    a = ap.parse_args()
    rng = np.random.default_rng(SEED)
    R = dict(lane="CFG816", seed=SEED)
    if a.dr4 or a.dr3:
        tag = "dr4" if a.dr4 else "dr3"
        # DEPARTURE opt-in (added 2026-10-18, after the official C4 was made): CFG825_DEPARTURE_TAG=<word> lets a SECOND --dr3 run score a
        # different input as a tagged departure (information only, listed under "Departures" in the README). It writes ONLY
        # cfg816_r_dr3_<word>_DEPARTURE.out / ..._DEPARTURE_results.json, refuses if those exist, never writes the official files, and is refused with --dr4.
        dep = os.environ.get("CFG825_DEPARTURE_TAG", "")
        if dep and (tag == "dr4" or not dep.isalnum()): sys.exit("REFUSING: CFG825_DEPARTURE_TAG is allowed only with --dr3 and must be alphanumeric.")
        stem = f"cfg816_r_{tag}_{dep}_DEPARTURE" if dep else f"cfg816_r_{tag}"
        resf = os.path.join(HERE, f"{stem}_results.json")
        if os.path.exists(resf): sys.exit(f"REFUSING: {resf} exists. The {tag.upper()} run is done once; a change goes under 'Departures' in the README, with its reason.")
        if dep: P(f"DEPARTURE '{dep}' (information only): a second DR3 run on a different input; the official C4 is cfg816_r_dr3_results.json and is not touched.")
        t = read_table(a.dr4 or a.dr3)
        res, final = score(t, rng, B_RUN, f"{tag.upper()} table {os.path.basename(a.dr4 or a.dr3)}")
        R.update(mode=tag, branches=res, primary_label=final)
        if dep: R.update(departure=dep, note="information only; NOT the official C4")
        if tag == "dr3":
            p = res["primary"]
            c4 = bool(p["ok"] and p["R"] - 1 < 2 * p["sigma_R"])
            R["C4_rule_information_only" if dep else "C4_pass"] = c4
            P(f"  C4 {'rule applied as information only (departure)' if dep else '(DR3 code path, interpretation I5)'}: {'PASS' if c4 else 'FAIL'}   (R-1)/sigma_R = {(p['R']-1)/p['sigma_R']:+.2f}; information only: (1.20-R)/sigma_R = {(1.20-p['R'])/p['sigma_R']:+.2f}")
        json.dump(R, open(resf, "w"), indent=1, default=float)
        open(os.path.join(HERE, f"{stem}.out"), "w").write("\n".join(OUT) + "\n")
        return 0
    if a.mutate:
        t = synth(30000, rng, mutate=1.2)
        res, final = score(t, rng, 300, "MUTATE (v-tilde x 1.2 at x>1 on a synthetic null)")
        p = res["primary"]; detected = bool(p["ok"] and abs(p["R"] - 1.2) < 0.03 and (p["R"] - 1) / p["sigma_R"] > 3)
        P(f"  MUTATE: R = {p['R']:.4f}; (R-1)/sigma_R = {(p['R']-1)/p['sigma_R']:.1f}; detected = {detected}")
        R.update(mode="MUTATE", result=res["primary"], detected=detected)
        json.dump(R, open(os.path.join(HERE, "cfg816_r_MUTATE_results.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, "cfg816_r_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
        return 1 if detected else 0
    P("CFG816 controls on synthetic pairs (Rayleigh v-tilde, median 0.489; x log-uniform 0.05-5; M = 1.8 Msun)")
    ok0, d0 = control_C0(rng);           P(f"  C0 (added; v-tilde matches the registered ingest_csv): {'PASS' if ok0 else 'FAIL'}  {d0}")
    ok3, d3 = control_C3();              P(f"  C3 class table / Amendment 22 arithmetic: {'PASS' if ok3 else 'FAIL'}  sigma_tot {d3['sigma_tot']}  kill threshold R {d3['kill_threshold_R']}")
    ok1, d1 = control_C1(rng);           P(f"  C1 injection recovery (200 repeats each): {'PASS' if ok1 else 'FAIL'}  {[(r['N'], r['R_true'], r['frac_within_2sigmaR']) for r in d1]}")
    ok2, d2 = control_C2(rng);           P(f"  C2 coverage / null KILLED rate (interpretations I3, I4): {'PASS' if ok2 else 'FAIL'}  {d2}")
    ok5, d5 = control_C5(rng);           P(f"  C5 (added) CSV path and contamination rule end to end: {'PASS' if ok5 else 'FAIL'}  {d5}")
    P("  C4 DR3 code-path run: NOT RUN (needs the owner's yes and a download). CONTROLS ARE INCOMPLETE until it is run.")
    R.update(mode="controls", C0=dict(ok=ok0, detail=d0), C1=dict(ok=ok1, rows=d1), C2=dict(ok=ok2, detail=d2), C3=dict(ok=ok3, detail=d3), C5=dict(ok=ok5, detail=d5), C4="not_run",
             all_run_controls_pass=bool(ok0 and ok1 and ok2 and ok3 and ok5))
    json.dump(R, open(os.path.join(HERE, "cfg816_r_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg816_r.out"), "w").write("\n".join(OUT) + "\n")
    return 0 if R["all_run_controls_pass"] else 2

if __name__ == "__main__":
    sys.exit(main())
