#!/usr/bin/env python3
"""CFG595 analysis (FROZEN_CRITERIA.md 0bd1e4a93): measured cold supply vs the assumed (1 - f_b) M_ta, its convergence, and the
gravitating P(k) with the measured supply.  Reads the engine's supply tables and the cfg595_measure.py caches in
../_external_data/cfg595_work; writes cfg595_analysis.out / cfg595_results.json (or *_MUTATE.* with CFG595_MUTATE=1).
  python3 cfg595_analysis.py            CFG595_MUTATE=1 python3 cfg595_analysis.py   (exit 1 = both teeth bite)"""
import os, sys, json, glob, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W595, W530 = os.path.join(EXT, "cfg595_work"), os.path.join(EXT, "cfg530_work")
MEAS_DIR = os.path.join(W595, "measure")
MUT = os.environ.get("CFG595_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUT else ""
h = 0.6736; Om = (0.02237 + 0.1200) / h ** 2; FB = 0.02237 / (0.02237 + 0.1200)
RHO_CELL = 0.315 * 2.775e11
BINS = [(12.0, 12.5), (12.5, 13.0), (13.0, 13.5), (13.5, 14.0), (14.0, 14.5), (14.5, 16.0)]
FOOTS = {"can": "canonical", "alt": "alt"}
lines = []
def P(*a):
    s = " ".join(str(x) for x in a); lines.append(s); print(s)

# ------------------------------------------------------------------ supply tables
def run_table(job, z):
    f = glob.glob(os.path.join(W595, "runs", job, f"cfg595_*_{z}_table.npz"))
    return np.load(f[0]) if f else None
def run_json(job):
    f = glob.glob(os.path.join(W595, "runs", job, "cfg595_*.json"))
    return json.load(open(f[0])) if f else None
def saved_table(job):
    f = os.path.join(MEAS_DIR, f"cfg595_530_{job}_ASSUMED_z0_table.npz")
    return np.load(f) if os.path.exists(f) else None
def c530_json(job):
    f = glob.glob(os.path.join(W530, "runs", job, "cfg527_*.json"))
    return json.load(open(f[0])) if f else None

def supply_stats(t, L, N, mutate=False):
    A = t["A_nom"]; S = A.copy() if mutate else t["S"]; Apm = t["A_PM"]; Sin = t["S_in"]; M = np.log10(t["M_sys"]); a = float(t["a"])
    dx = L / N
    E = t["E_catch"][t["sysid"]] * a / (1.5 * Om) * RHO_CELL * dx ** 3 if "E_catch" in t.files else None
    bins = []
    for lo, hi in BINS:
        m = (M >= lo) & (M < hi); n = int(m.sum())
        b = dict(lo=lo, hi=hi, n=n, flag_lt5=n < 5)
        if n:
            b.update(median_rho=float(np.median(S[m] / A[m])), mw_rho=float(S[m].sum() / A[m].sum()), mw_S_over_APM=float(S[m].sum() / Apm[m].sum()),
                     mw_APM_over_Anom=float(Apm[m].sum() / A[m].sum()))
            if E is not None: b["mw_E_over_Anom"] = float(E[m].sum() / A[m].sum())
        bins.append(b)
    single = (t["n_peaks"] == 1) & (t["B_ncomp_single"] == 1)
    out = dict(n_sys=int(len(A)), Q=float(S.sum() / A.sum()), Q_vs_APM=float(S.sum() / Apm.sum()), APM_over_Anom=float(Apm.sum() / A.sum()),
               Sin_over_APM=float(Sin.sum() / Apm.sum()), bins=bins,
               E_over_Anom=float(E.sum() / A.sum()) if E is not None else None, E_over_S=float(E.sum() / S.sum()) if E is not None else None,
               B_unattached_frac=float(t["B_cold_unattached"] / t["B_cold_total"]), B_largest_share=float(t["B_largest_share"]),
               n_Bcomp=int(t["n_Bcomp"]), hosts_inB_frac=float(np.mean(t["host_inB"])),
               C2_closure_rel=float(abs(t["S"].sum() + t["B_cold_unattached"] - t["B_cold_total"]) / t["B_cold_total"]),
               C3_single_n=int(single.sum()), C3_single_median_Sin_over_APM=float(np.median(Sin[single] / Apm[single])) if single.any() else None,
               single_peak_Q=float(S[t["n_peaks"] == 1].sum() / A[t["n_peaks"] == 1].sum()) if (t["n_peaks"] == 1).any() else None,
               E_sum_s_units=float(t["E_catch"].sum()) if "E_catch" in t.files else None)
    return out

def verdict_supply(Q):
    return "MEASURED SUPPLY SMALLER" if Q <= 0.80 else ("LARGER" if Q >= 1.25 else "SIMILAR")

R = dict(lane="CFG595", date="2026-10-10", criteria_commit="0bd1e4a93", mutate=MUT, supply={}, convergence={}, pk={}, controls={}, verdicts={})
P(f"CFG595 analysis{' (MUTATE: S := A_nom, MEAS P := ASSUMED P)' if MUT else ''} -- criteria FROZEN_CRITERIA.md (0bd1e4a93)")
P("rho = S / A_nom, S = cold mass of the bound-region (raw switch f_sw > 0) components holding a system's peaks, A_nom = (1 - f_b) M_ta (largest peak).")
P("")
P("1. MEASURED SUPPLY per state (ASSUMED-supply states = the CFG530 runs)")
c1 = []
for L in (100, 200):
    for N in (128, 256, 512):
        for ft in ("can", "alt"):
            for z in ("z1", "z0.5", "z0"):
                key = f"L{L}_N{N}_{ft}_{z}"
                job = f"ASSUMED_{ft}_L{L}_N{N}"
                t = run_table(job, z) if L == 100 and N <= 256 else (saved_table(f"LR{ft}_L{L}_N{N}") if z == "z0" else None)
                if t is None: continue
                st = supply_stats(t, L, N, MUT)
                cj = c530_json(f"LR{ft}_L{L}_N{N}")
                if cj and st["E_sum_s_units"] is not None:
                    js = cj["snap"][z]
                    st["C1_esum_rel"] = abs(st["E_sum_s_units"] - js["e_sum"]) / max(abs(js["e_sum"]), 1e-30)
                    st["C1_ncatch_eq"] = int(len(t["E_catch"])) == int(js["n_catch"])
                    c1.append(st["C1_esum_rel"] <= 1e-5 and st["C1_ncatch_eq"])
                R["supply"][key] = st
                P(f"  {key:22s} n_sys {st['n_sys']:5d}  Q = S/A_nom {st['Q']:.3f}  S/A_PM {st['Q_vs_APM']:.3f}  A_PM/A_nom {st['APM_over_Anom']:.3f}"
                  f"  S_in/A_PM {st['Sin_over_APM']:.3f}  E/A_nom {st['E_over_Anom']:.3f}  E/S {st['E_over_S']:.3f}  B unattached {st['B_unattached_frac']:.3f}"
                  f"  largest B {st['B_largest_share']:.3f}  C1 {st.get('C1_esum_rel', float('nan')):.1e}/{st.get('C1_ncatch_eq')}  C2 {st['C2_closure_rel']:.1e}")
                P("      bins (logM: n, median rho, sum S/sum A_nom, sum E/sum A_nom): " + "; ".join(
                    f"[{b['lo']},{b['hi']}) {b['n']}{'*' if b['flag_lt5'] else ''} {b.get('median_rho', float('nan')):.2f} {b.get('mw_rho', float('nan')):.2f} {b.get('mw_E_over_Anom', float('nan')):.2f}"
                    for b in st['bins'] if b['n'] > 0))
R["controls"]["C1_pass"] = bool(c1) and all(c1); R["controls"]["C1_n"] = len(c1)
c2 = [v["C2_closure_rel"] for v in R["supply"].values()]
R["controls"]["C2_max"] = max(c2) if c2 else None; R["controls"]["C2_pass"] = bool(c2) and max(c2) <= 1e-6
P(f"  C1 (measurement = engine e_sum, n_catch): {'PASS' if R['controls']['C1_pass'] else 'FAIL'} ({len(c1)} states);  C2 closure max {R['controls']['C2_max']:.1e} -> {'PASS' if R['controls']['C2_pass'] else 'FAIL'}")
P("  C3 (reported): single-peak single-component systems, median S_in/A_PM: " + ", ".join(
    f"{k} {v['C3_single_median_Sin_over_APM']:.3f} (n {v['C3_single_n']})" for k, v in R["supply"].items() if k.endswith("_z0") and v["C3_single_median_Sin_over_APM"] is not None))
P("")
P("2. VERDICT ON THE SUPPLY (primary L100 N256 z = 0) and CONVERGENCE (L100 z = 0, N256 vs N512)")
for ft in ("can", "alt"):
    p = R["supply"].get(f"L100_N256_{ft}_z0"); q5 = R["supply"].get(f"L100_N512_{ft}_z0")
    if not p: continue
    v = verdict_supply(p["Q"])
    zq = {z: R["supply"][f"L100_N256_{ft}_{z}"]["Q"] for z in ("z1", "z0.5", "z0") if f"L100_N256_{ft}_{z}" in R["supply"]}
    conv = None
    if q5:
        dQ = abs(p["Q"] - q5["Q"]); dbin = []
        for b2, b5 in zip(p["bins"], q5["bins"]):
            if b2["n"] >= 5 and b5["n"] >= 5: dbin.append(abs(b2["mw_rho"] - b5["mw_rho"]))
        conv = "CONVERGED" if dQ <= 0.10 and all(d <= 0.15 for d in dbin) else "NOT CONVERGED"
        R["convergence"][ft] = dict(Q_N128=R["supply"].get(f"L100_N128_{ft}_z0", {}).get("Q"), Q_N256=p["Q"], Q_N512=q5["Q"], dQ=dQ,
                                    max_dbin=max(dbin) if dbin else None, verdict=conv)
    R["verdicts"][f"supply_{ft}"] = dict(Q=p["Q"], verdict=v, smaller_by=1 - p["Q"] if v == "MEASURED SUPPLY SMALLER" else None, Q_by_z=zq,
                                         convergence=conv, Q_vs_APM=p["Q_vs_APM"], APM_over_Anom=p["APM_over_Anom"])
    P(f"  {FOOTS[ft]:9s}: Q = {p['Q']:.3f} -> {v};  Q(z = 1 / 0.5 / 0) = " + " / ".join(f"{x:.3f}" for x in zq.values())
      + (f";  N128 / N256 / N512 = {R['convergence'][ft]['Q_N128']:.3f} / {p['Q']:.3f} / {q5['Q']:.3f} (max bin diff {R['convergence'][ft]['max_dbin']:.3f}) -> {conv}" if q5 else ""))
    P(f"             decomposition: S / A_PM = {p['Q_vs_APM']:.3f} (measured vs the cold the PM's turnaround-ball cover actually holds);"
      f" A_PM / A_nom = {p['APM_over_Anom']:.3f}; settled E / A_nom = {p['E_over_Anom']:.3f}")

# ------------------------------------------------------------------ P(k)
def mcache(name, sup):
    f = os.path.join(MEAS_DIR, f"cfg595_{name}_{sup}.json")
    return json.load(open(f)) if os.path.exists(f) else None
def s0_json(L, N):
    f = glob.glob(os.path.join(W530, "runs", f"S0_L{L}_N{N}", "cfg527_S0_*.json"))
    return json.load(open(f[0])) if f else None
def rstats(k, Pg, s8g, s0):
    k = np.array(k); s0z = s0["snap"]["z0"]
    r = np.array(Pg) / np.interp(k, np.array(s0z["k"]), np.array(s0z["P"]))
    m1 = k <= 1.0; m12 = (k > 1.0) & (k <= 2.0)
    return dict(maxdev_k_le_1=float(np.max(np.abs(r[m1] - 1))), k_at=float(k[m1][np.argmax(np.abs(r[m1] - 1))]),
                mean_r_1_2=float(np.mean(r[m12])) if m12.any() else None, r_05=float(np.interp(0.5, k, r)), r_1=float(np.interp(1.0, k, r)),
                r_2=float(np.interp(2.0, k, r)), s8_ratio=float(s8g / s0z["sigma8"]))
c555 = json.load(open(os.path.join(HERE, "..", "CFG555_growth_on_gravitating_field", "cfg555_results.json")))["cfg530"]
P("")
P("3. GRAVITATING P(k) RATIO framework / S0 (same pipeline, same L and N), z = 0  [max|r-1| k<=1 (k at) | mean r 1<k<=2 | r(0.5/1/2) | s8 ratio]")
rows = []
for L, N in ((100, 128), (100, 256)):
    s0 = s0_json(L, N)
    for ft in ("can", "alt"):
        for sup in ("ASSUMED", "MEAS", "ZERO"):
            job = f"{sup}_{ft}_L{L}_N{N}"; c = mcache(job, sup)
            if c is None: continue
            if MUT and sup == "MEAS":
                c = mcache(f"ASSUMED_{ft}_L{L}_N{N}", "ASSUMED") or c
            st = rstats(c["k"], c["P_grav"], c["s8_grav"], s0); st["src_absmax_rel"] = c["src_absmax_rel"]
            st["meas_last"] = c["info"].get("meas_last"); st["dynamic"] = True
            R["pk"][job] = st; rows.append(job)
        sc = mcache(f"ASSUMED_{ft}_L{L}_N{N}_static", "MEAS")
        if sc is not None:
            st = rstats(sc["k"], sc["P_grav"], sc["s8_grav"], s0); st["dynamic"] = False; R["pk"][f"STATIC_MEAS_{ft}_L{L}_N{N}"] = st; rows.append(f"STATIC_MEAS_{ft}_L{L}_N{N}")
for L, N in ((100, 512), (200, 128), (200, 256), (200, 512)):
    s0 = s0_json(L, N) if not (L == 200 and N == 512) else None
    if s0 is None: continue
    for ft in ("can", "alt"):
        for sup in ("ASSUMED", "MEAS"):
            c = mcache(f"530_LR{ft}_L{L}_N{N}", sup)
            if c is None: continue
            st = rstats(c["k"], c["P_grav"], c["s8_grav"], s0); st["dynamic"] = sup == "ASSUMED"
            nm = f"{'SAVED_ASSUMED' if sup == 'ASSUMED' else 'STATIC_MEAS'}_{ft}_L{L}_N{N}"; R["pk"][nm] = st; rows.append(nm)
for nm in rows:
    s = R["pk"][nm]
    P(f"  {nm:28s} {s['maxdev_k_le_1']:.3f} ({s['k_at']:.2f}) | {s['mean_r_1_2'] if s['mean_r_1_2'] is None else round(s['mean_r_1_2'], 3)} | "
      f"{s['r_05']:.3f}/{s['r_1']:.3f}/{s['r_2']:.3f} | {s['s8_ratio']:.4f}" + (f"   in-run S/A_nom {s['meas_last']['Q']:.3f}, x-cap frac {s['meas_last']['x_cap_frac']:.3f}" if s.get("meas_last") else ""))

# ------------------------------------------------------------------ MU1 / MU2
P("")
P("4. CONTROLS")
mu1 = []
for ft in ("can", "alt"):
    for N in (128, 256):
        a_ = run_json(f"ASSUMED_{ft}_L100_N{N}"); b_ = c530_json(f"LR{ft}_L100_N{N}")
        if not a_ or not b_: continue
        dP = max(float(np.max(np.abs(np.array(a_["snap"][z]["P"]) / np.array(b_["snap"][z]["P"]) - 1))) for z in ("z1", "z0.5", "z0"))
        ds = max(abs(a_["snap"][z]["sigma8"] / b_["snap"][z]["sigma8"] - 1) for z in ("z1", "z0.5", "z0"))
        g = R["pk"].get(f"ASSUMED_{ft}_L100_N{N}"); ref = c555[f"530_LR{ft}_L100_N{N}"]["gravitating"]["pdev"]
        dg = abs(g["maxdev_k_le_1"] - ref) if g else None
        ok = dP <= 1e-6 and ds <= 1e-6 and dg is not None and dg <= 1e-4
        mu1.append(ok); R["controls"][f"MU1_{ft}_N{N}"] = dict(dP=dP, ds8=ds, dgrav=dg, ref_cfg555=ref, pass_=ok)
        P(f"  MU1 assumed reinserted {ft} L100 N{N}: particle P/s8 vs CFG530 (z1,z0.5,z0) max rel {dP:.1e}/{ds:.1e}; grav max|r-1| {g['maxdev_k_le_1'] if g else float('nan'):.4f} vs CFG555 {ref:.4f} (|d| {dg if dg is not None else float('nan'):.1e}) -> {'PASS' if ok else 'FAIL'}")
mu2 = []
for ft in ("can", "alt"):
    a_ = run_json(f"ZERO_{ft}_L100_N128"); s0 = s0_json(100, 128)
    if not a_: continue
    dP = max(float(np.max(np.abs(np.array(a_["snap"][z]["P"]) / np.array(s0["snap"][z]["P"]) - 1))) for z in ("z1", "z0.5", "z0"))
    ds = max(abs(a_["snap"][z]["sigma8"] / s0["snap"][z]["sigma8"] - 1) for z in ("z1", "z0.5", "z0"))
    g = R["pk"].get(f"ZERO_{ft}_L100_N128"); sa = g["src_absmax_rel"] if g else None
    ok = dP <= 1e-6 and ds <= 1e-6 and sa is not None and sa <= 1e-6
    mu2.append(ok); R["controls"][f"MU2_{ft}"] = dict(dP=dP, ds8=ds, src_absmax_rel=sa, pass_=ok)
    P(f"  MU2 supply zero {ft} L100 N128: particle P/s8 vs S0 (z1,z0.5,z0) max rel {dP:.1e}/{ds:.1e}; max|src|/peak {sa if sa is not None else float('nan'):.1e} -> {'PASS' if ok else 'FAIL'}")
R["controls"]["MU1_pass"] = bool(mu1) and all(mu1); R["controls"]["MU2_pass"] = bool(mu2) and all(mu2)

# ------------------------------------------------------------------ excess verdict
P("")
P("5. VERDICTS (per footing; never pooled)")
for ft in ("can", "alt"):
    m = R["pk"].get(f"MEAS_{ft}_L100_N256"); a_ = R["pk"].get(f"ASSUMED_{ft}_L100_N256")
    if m is None or a_ is None: continue
    if m["maxdev_k_le_1"] > 0.10: ve = "EXCESS PERSISTS"
    elif abs(m["s8_ratio"] - 1) <= 0.05: ve = "EXCESS REMOVED"
    else: ve = "PARTIAL"
    rem = 1 - m["maxdev_k_le_1"] / a_["maxdev_k_le_1"]
    rem12 = 1 - abs(m["mean_r_1_2"] - 1) / abs(a_["mean_r_1_2"] - 1) if abs(a_["mean_r_1_2"] - 1) > 0 else None
    blocked = not (R["controls"]["MU1_pass"] and R["controls"]["MU2_pass"])
    R["verdicts"][f"excess_{ft}"] = dict(verdict=ve if not blocked else ve + " (BLOCKED: MU control failed)", MEAS=m, ASSUMED=a_,
                                         frac_removed_k_le_1=rem, frac_removed_k_1_2=rem12)
    sv = R["verdicts"].get(f"supply_{ft}", {})
    P(f"  {FOOTS[ft]:9s}: SUPPLY {sv.get('verdict')} (Q {sv.get('Q', float('nan')):.3f}; {sv.get('convergence')});  EXCESS with measured supply: max|r-1|(k<=1) "
      f"{m['maxdev_k_le_1']:.3f} vs assumed {a_['maxdev_k_le_1']:.3f} (removed {rem:+.2f}); mean r(1-2) {m['mean_r_1_2']:.3f} vs {a_['mean_r_1_2']:.3f} "
      f"(removed {rem12:+.2f}); s8 {m['s8_ratio']:.4f} vs {a_['s8_ratio']:.4f} -> {R['verdicts'][f'excess_{ft}']['verdict']}")
P("")
P("kappa = 1/2 FITTED; footings never pooled; cold energy mass still required; S0 = same-pipeline reference only (no verdict against data); not theory closed.")
json.dump(R, open(os.path.join(HERE, f"cfg595_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg595_analysis{SUF}.out"), "w").write("\n".join(lines) + "\n")
if MUT:
    t1 = all(v.get("verdict") == "SIMILAR" for k, v in R["verdicts"].items() if k.startswith("supply_"))
    t2 = all(v["verdict"].startswith("EXCESS PERSISTS") and abs(v["frac_removed_k_le_1"]) < 1e-12 for k, v in R["verdicts"].items() if k.startswith("excess_"))
    print(f"MUTATE teeth: supply->SIMILAR {t1}; excess->PERSISTS with 0 removed {t2}")
    sys.exit(1 if (t1 and t2) else 0)
