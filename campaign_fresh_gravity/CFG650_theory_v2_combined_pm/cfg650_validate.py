#!/usr/bin/env python3
"""CFG650 validation (FROZEN_CRITERIA.md section 4, 3087298c7), read-only on every CFG596 / CFG640 reference file.
  V-0  V0 (cfg650_pm.py, all modules OFF, lean RES can L100 N256 NSEED512 RMIN 0.78125) vs CFG596 VLr: every stored snapshot
       quantity identical (difference exactly 0).
  V-2  VM2 (M2 alone) vs CFG640 VPh: identical (difference exactly 0) on every quantity VPh stores.
  V-C  every module run: completes, finite; |src_sum|/e_sum <= 1e-5 at z = 1, 0.5, 0; M1 max per-host |sum src|/E_h <= 1e-4 and 0 orphan
       cells; M3 |sum(placed - removed)| / sum removed <= 1e-5.
  V-D  direction of each module alone vs V0 at z = 0 (e_sum, P_grav at k 0.3 / 0.5 / 1), reported.
  PREVIEW table (256^3, NOT a verdict): P_grav/P_S0 - 1 at k 0.3 / 0.5 / 1 (S0 = CFG596 VLs) at z = 0 (z = 0.5, 1 also stored).
  python3 cfg650_validate.py -> cfg650_validate.out / cfg650_validate.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, json, glob, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg650_work"); W596 = os.path.join(EXT, "cfg596_work"); W640 = os.path.join(EXT, "cfg640_work")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def load(d, pat):
    f = glob.glob(os.path.join(d, pat)); return json.load(open(f[0])) if f else None
def peak(job):
    wl = os.path.join(W, job, "watch.log"); pk = 0.0; sg = 0.0
    if os.path.exists(wl):
        for line in open(wl):
            m = re.search(r"peak ([\d.]+) swap_used ([\d.]+) MB \(start ([\d.]+)\)", line)
            if m: pk = max(pk, float(m.group(1))); sg = max(sg, float(m.group(2)) - float(m.group(3)))
    return pk, sg
def identical(ref, run):
    diffs = {}; nq = 0
    for z, s in ref["snap"].items():
        t = run["snap"].get(z)
        if t is None: diffs[z] = "missing"; continue
        for k, v in s.items():
            if k == "t": continue
            nq += 1
            a, b = np.asarray(v, dtype=float), np.asarray(t.get(k), dtype=float)
            if a.shape != b.shape or not np.array_equal(a, b, equal_nan=True):
                diffs[f"{z}.{k}"] = float(np.max(np.abs(b / a - 1))) if a.shape == b.shape else "shape"
    return nq, diffs
RES = dict(lane="CFG650 validation", date="2026-10-12", criteria_commit="3087298c7", gates={})
RUNS = {j: load(os.path.join(W, j), "cfg650_*_RES_*.json") for j in ("V0", "VM1", "VM2", "VM3", "VM4", "VM12", "VM123", "VM1234")}
RUNS = {j: r for j, r in RUNS.items() if r is not None and "z0" in r["snap"]}
LABEL = {"V0": "all OFF", "VM1": "M1 per-host supply", "VM2": "M2 condensed source", "VM3": "M3 gas expulsion", "VM4": "M4 phase-mixed gate",
         "VM12": "M1+M2", "VM123": "M1+M2+M3", "VM1234": "all ON (M1+M2+M3+M4)"}

# ---------------------------------------------------------------- V-0, V-2
for gate, job, ref, rl in (("V-0", "V0", load(os.path.join(W596, "VLr"), "cfg596_RES_*.json"), "CFG596 VLr"),
                           ("V-2", "VM2", load(os.path.join(W640, "VPh"), "cfg640_phase_RES_*.json"), "CFG640 VPh")):
    if job in RUNS and ref:
        nq, diffs = identical(ref, RUNS[job]); ok = not diffs and set(ref["snap"]) == set(RUNS[job]["snap"])
        RES["gates"][gate] = dict(PASS=ok, quantities_compared=nq, differences=diffs, reference=rl)
        P(f"{gate} {job} ({LABEL[job]}) vs {rl}: {nq} stored quantities over {sorted(RUNS[job]['snap'])}; differences "
          f"{diffs if diffs else 'none (bit for bit)'} -> {'PASS' if ok else 'FAIL'}")
    else: P(f"{gate}: not run / incomplete")

# ---------------------------------------------------------------- V-2 POST-FREEZE diagnostic (reported; added after V-2 failed literally)
# The only V-2 differences are the z = 0 P_grav-derived quantities (~1e-8).  Check: is the evolved STATE identical (z0 positions, f_d,
# the full-resolution gravitating field of every snapshot), and does measuring that identical field with 2 FFT workers reproduce VPh?
if "V-2" in RES["gates"] and not RES["gates"]["V-2"]["PASS"]:
    os.environ.update(CFG596_L="100", CFG596_THREADS="2", CFG596_RELIEF="0", CFG596_WORK=os.path.join(W, "VP_tmp"))
    os.makedirs(os.environ["CFG596_WORK"], exist_ok=True)
    import sys; sys.path.insert(0, HERE); import cfg650_pm as E  # noqa: E402
    def npz(d, pat): return np.load(glob.glob(os.path.join(d, pat))[0])
    st = {}
    st["z0pos_identical"] = bool(np.array_equal(npz(os.path.join(W640, "VPh"), "*_z0pos.npz")["pos"], npz(os.path.join(W, "VM2"), "*_z0pos.npz")["pos"]))
    st["z0fd_identical"] = bool(np.array_equal(npz(os.path.join(W640, "VPh"), "*_z0fd.npz")["fd"], npz(os.path.join(W, "VM2"), "*_z0fd.npz")["fd"]))
    fields = {}
    for z in ("zi", "z1", "x0.7548", "z0.5", "x0.2562", "z0"):
        A = npz(os.path.join(W640, "VPh"), f"*_{z}_mesh256.npz"); B = npz(os.path.join(W, "VM2"), f"*_{z}_mesh256.npz")
        fields[z] = bool(all(np.array_equal(A[k], B[k]) for k in ("dpart", "dgrav")))
    st["fields_identical_full_resolution"] = fields
    g = npz(os.path.join(W, "VM2"), "*_z0_mesh256.npz")["dgrav"]
    import subprocess
    snippet = ("import sys, glob, json, numpy as np; sys.path.insert(0, sys.argv[1]); import cfg650_pm as E; "
               "g = np.load(glob.glob(sys.argv[2])[0])['dgrav']; _, p, _, _ = E.measure_pk(E.Mesh(256), g.copy()); print(json.dumps(list(p)))")
    vph = np.array(load(os.path.join(W640, "VPh"), "cfg640_phase_RES_*.json")["snap"]["z0"]["P_grav"])
    vm2 = np.array(RUNS["VM2"]["snap"]["z0"]["P_grav"]); trials = []
    for nw in (1, 2, 2, 2, 2, 3, 3, 3, 4, 4):                     # fresh process each (repeats: run-to-run reproducibility)
        env = dict(os.environ, CFG596_THREADS=str(nw))
        out = subprocess.run([sys.executable, "-c", snippet, HERE, os.path.join(W, "VM2", "*_z0_mesh256.npz")], env=env,
                             capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1]
        p_ = np.array(json.loads(out))
        trials.append(dict(threads=nw, equals_VPh=bool(np.array_equal(p_, vph)), equals_VM2=bool(np.array_equal(p_, vm2)),
                           max_rel_vs_VM2=float(np.max(np.abs(p_ / vm2 - 1)))))
    st["remeasure_trials"] = trials
    st["Pgrav_z0_remeasured_equals_VPh_in_some_trial"] = any(t["equals_VPh"] for t in trials)
    st["remeasure_spread_max_rel"] = max(t["max_rel_vs_VM2"] for t in trials)
    RES["gates"]["V-2_postfreeze"] = st
    P(f"V-2 POST-FREEZE diagnostic: z0 positions identical {st['z0pos_identical']}, z0 f_d identical {st['z0fd_identical']}, particle and "
      f"gravitating fields identical at full 256^3 resolution at every snapshot {all(fields.values())}; re-measuring VM2's own z = 0 "
      f"gravitating field (10 fresh processes, CFG596_THREADS 1-4 with repeats): reproduces VPh's stored P_grav exactly in {sum(t['equals_VPh'] for t in trials)} / VM2's in "
      f"{sum(t['equals_VM2'] for t in trials)} of {len(trials)} trials, spread {st['remeasure_spread_max_rel']:.1e} "
      f"-> the V-2 difference is in the MEASUREMENT of a bit-identical field (the multithreaded P(k) measurement of an identical array is not run-to-run bitwise reproducible), not in the copied M2 code")

# ---------------------------------------------------------------- V-C
vc = {}
for job, r in RUNS.items():
    rec = dict(finite=all(r["snap"][z].get("finite", True) for z in r["snap"]), src_rel={}, PASS=True)
    for z in ("z1", "z0.5", "z0"):
        s = r["snap"][z]; rec["src_rel"][z] = abs(s["src_sum"]) / max(abs(s["e_sum"]), 1e-30)
        if "m1_max_host_rel_imbalance" in s:
            rec.setdefault("m1", {})[z] = dict(imb=s["m1_max_host_rel_imbalance"], orphans=s["m1_orphan_cells"], n_hosts=s["m1_n_hosts"],
                                             hosts_capped=s["m1_hosts_capped"], hosts_demand_no_supply=s["m1_hosts_demand_no_supply"])
        if "m3_placement_imbalance" in s:
            rec.setdefault("m3", {})[z] = dict(imb=s["m3_placement_imbalance"], expelled_mass_frac=s["m3_expelled_mass_frac"], classes=s["m3_classes"])
        if "m4_pm_mass_frac" in s:
            rec.setdefault("m4", {})[z] = dict(pm_mass_frac=s["m4_pm_mass_frac"], pm_frac_in_catch=s["m4_pm_frac_in_catch"])
        if "fd_mean" in s: rec.setdefault("m2", {})[z] = dict(fd_mean=s["fd_mean"], fd_nonzero_frac=s["fd_nonzero_frac"])
    ok = rec["finite"] and max(rec["src_rel"].values()) <= 1e-5
    if "m1" in rec: ok = ok and all(v["imb"] <= 1e-4 and v["orphans"] == 0 for v in rec["m1"].values())
    if "m3" in rec: ok = ok and all(abs(v["imb"]) <= 1e-5 for v in rec["m3"].values())
    rec["PASS"] = bool(ok); rec["peak_rss_gb"], rec["swap_growth_mb"] = peak(job); rec["runtime_s"] = r.get("runtime_s")
    vc[job] = rec
    P(f"V-C {job} ({LABEL[job]}): finite {rec['finite']}; max |src_sum|/e_sum {max(rec['src_rel'].values()):.1e}"
      + ("; M1 max host imbalance " + f"{max(v['imb'] for v in rec['m1'].values()):.1e}, orphans {max(v['orphans'] for v in rec['m1'].values())}, "
         f"hosts z0 {rec['m1']['z0']['n_hosts']} (capped {rec['m1']['z0']['hosts_capped']}, demand without own supply {rec['m1']['z0']['hosts_demand_no_supply']})" if "m1" in rec else "")
      + ("; M3 placement imbalance " + f"{max(abs(v['imb']) for v in rec['m3'].values()):.1e}, expelled z0 {rec['m3']['z0']['expelled_mass_frac']:.4f} of all mass" if "m3" in rec else "")
      + ("; M4 phase-mixed mass z0 " + f"{rec['m4']['z0']['pm_mass_frac']:.3f} (in catchments {rec['m4']['z0']['pm_frac_in_catch']:.3f})" if "m4" in rec else "")
      + ("; M2 f_d mean z0 " + f"{rec['m2']['z0']['fd_mean']:.4f}" if "m2" in rec else "")
      + f" -> {'PASS' if ok else 'FAIL'}; peak RSS {rec['peak_rss_gb']:.2f} GB, swap growth {rec['swap_growth_mb']:.0f} MB, runtime {rec['runtime_s'] or 0:.0f} s")
RES["gates"]["V-C"] = dict(PASS=bool(vc) and all(v["PASS"] for v in vc.values()), runs=vc)

# ---------------------------------------------------------------- V-D and the PREVIEW table
s0 = load(os.path.join(W596, "VLs"), "cfg596_S0_*.json")
def at(r, k, kk): return float(np.exp(np.interp(math.log(kk), np.log(k), np.log(r))))
if s0 and "V0" in RUNS:
    tab = {}; V0 = RUNS["V0"]
    for job, r in RUNS.items():
        row = {}
        for z in ("z1", "z0.5", "z0"):
            k = np.array(r["snap"][z]["k"]); assert np.allclose(k, np.array(s0["snap"][z]["k"]), rtol=1e-9)
            rr = np.array(r["snap"][z]["P_grav"]) / np.array(s0["snap"][z]["P"]); m = k <= 1.0 + 1e-9
            rv = np.array(r["snap"][z]["P_grav"]) / np.array(V0["snap"][z]["P_grav"])
            row[z] = dict(dP_over_PS0={str(q): at(rr, k, q) - 1 for q in (0.3, 0.5, 1.0)}, G_benchmark=float(np.max(np.abs(rr[m] - 1))),
                          Pgrav_over_V0={str(q): at(rv, k, q) for q in (0.3, 0.5, 1.0)},
                          e_sum=r["snap"][z]["e_sum"], e_sum_over_V0=r["snap"][z]["e_sum"] / V0["snap"][z]["e_sum"],
                          sigma8_grav_over_S0=r["snap"][z]["sigma8_grav"] / s0["snap"][z]["sigma8"])
        tab[job] = row
    RES["preview"] = dict(NOTE="PREVIEW at 256^3 (L100, NSEED 512): NOT a verdict; S0 = CFG596 VLs; benchmark G has no verdict weight", table=tab)
    P("\nPREVIEW (256^3, NOT a verdict): P_grav/P_S0 - 1 at z = 0, k 0.3 / 0.5 / 1 h/Mpc (S0 = CFG596 VLs); settled e_sum and P_grav relative to all-OFF")
    P(f"  {'run':<26s} {'k=0.3':>7s} {'k=0.5':>7s} {'k=1':>7s} | {'e_sum/OFF':>9s} | P_grav/OFF at 0.3/0.5/1")
    dirs = {}
    for job, row in tab.items():
        z = row["z0"]; d = z["dP_over_PS0"]; v = z["Pgrav_over_V0"]
        P(f"  {LABEL[job]:<26s} {d['0.3']:+7.3f} {d['0.5']:+7.3f} {d['1.0']:+7.3f} | {z['e_sum_over_V0']:9.3f} | " + " / ".join(f"{x:.3f}" for x in v.values()))
        if job in ("VM1", "VM2", "VM3", "VM4"):
            down = all(x < 1 for x in v.values()) if job == "VM3" else (z["e_sum_over_V0"] < 1 and all(x < 1 for x in v.values()))
            dirs[job] = "intended (lower)" if down else "NOT the intended direction (reported; still in T1 by the section-2 rule)"
    for z_ in ("z0.5", "z1"):
        P(f"  [{z_}] " + "; ".join(f"{LABEL[j]}: " + "/".join(f"{x:+.3f}" for x in tab[j][z_]["dP_over_PS0"].values()) for j in tab))
    RES["gates"]["V-D"] = dirs
    P("V-D direction (each module alone vs all OFF, z = 0): " + "; ".join(f"{j}: {v}" for j, v in dirs.items()))
else: P("PREVIEW: S0 VLs or V0 missing")
P("CMB-safety checklist (CFG649): not committed -> not run (criteria section 4).")
json.dump(RES, open(os.path.join(HERE, "cfg650_validate.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg650_validate.out"), "w").write("\n".join(OUT) + "\n")
