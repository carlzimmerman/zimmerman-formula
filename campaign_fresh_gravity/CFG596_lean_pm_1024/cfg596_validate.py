#!/usr/bin/env python3
"""CFG596 validation gates (FROZEN_CRITERIA.md section 2, commit f6c27d401), read-only on every reference file.
  V-E  exact mode reproduces cfg527_pm.py bit for bit: (a) VEa vs CFG527 LRcan L200 N256 JSON + z0 npz; (b) VEb vs CFG530 S0_L100_N256.
  V-G  VEa z = 0 gravitating P(k), sigma8 vs cfg555_527_LRcan_L200.json (<= 1e-5 relative, every bin).
  V-L  lean mode (VLs, VLr) vs CFG530 S0 / LRcan L100 N256: STRICT 1e-5 (P at k <= k_hi, sigma8); SCIENCE 1e-3 P, 1e-4 sigma8, 1e-3 B (z = 0).
  V-M  peak resident memory per job (watchdog samples and the engine's own ru_maxrss); 1024^3 model; production first steps when present.
  Reported: VMs (lean S0 N512) vs CFG530 S0_L100_N512.
  python3 cfg596_validate.py -> cfg596_validate.out / cfg596_validate.json"""
import os, sys, json, glob, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg596_work"); R530 = os.path.join(EXT, "cfg530_work", "runs"); W527 = os.path.join(EXT, "cfg527_work")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def mine(job):
    f = [x for x in glob.glob(os.path.join(W, job, "cfg596_*.json"))]; return (json.load(open(f[0])), f[0]) if f else (None, None)
def ref530(run):
    f = [x for x in glob.glob(os.path.join(R530, run, "cfg527_*.json"))][0]; return json.load(open(f)), f
def cmp_runs(a, b, kmax=None, keys=("zi", "z1", "z0.5", "z0")):
    out = {}
    for z in keys:
        ka = np.array(a["snap"][z]["k"]); pa = np.array(a["snap"][z]["P"]); pb = np.array(b["snap"][z]["P"])
        m = np.ones(len(ka), bool) if kmax is None else ka <= kmax * (1 + 1e-9)
        out[z] = dict(maxrelP=float(np.max(np.abs(pb[m] / pa[m] - 1))), relsig8=float(abs(b["snap"][z]["sigma8"] / a["snap"][z]["sigma8"] - 1)),
                      diag={k: [a["snap"][z].get(k), b["snap"][z].get(k)] for k in ("q_max", "n_catch", "e_sum", "src_sum") if k in a["snap"][z]})
    return out
RES = dict(lane="CFG596 validation", date="2026-10-10", criteria_commit="f6c27d401", gates={})

# ---------------- V-E (a) and V-G
a_ref = json.load(open(os.path.join(W527, "cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N256_drawSHELL.json")))
VEa, fVEa = mine("VEa")
if VEa:
    c = cmp_runs(a_ref, VEa)
    pr = np.load(os.path.join(W527, "cfg527_RES_TA_NOFILT_MASSCONS_fretcensus_FLAT_canonical_N256_drawSHELL_z0.npz"))["pos"]
    pm = np.load(glob.glob(os.path.join(W, "VEa", "*_z0pos.npz"))[0])["pos"]
    pos_eq = bool(np.array_equal(pr, pm)); diag_eq = all(v[0] == v[1] for z in c for v in c[z]["diag"].values())
    passE = all(c[z]["maxrelP"] <= 1e-12 and c[z]["relsig8"] <= 1e-12 for z in c) and pos_eq
    RES["gates"]["V-E(a)"] = dict(cmp=c, z0_positions_identical=pos_eq, diag_identical=diag_eq, PASS=passE,
                                  bitwise=all(c[z]["maxrelP"] == 0 and c[z]["relsig8"] == 0 for z in c))
    P(f"V-E(a) exact LRcan L200 N256 vs CFG527: " + "; ".join(f"{z}: max|dP/P| {c[z]['maxrelP']:.1e}, |ds8/s8| {c[z]['relsig8']:.1e}" for z in c)
      + f"; z0 positions identical {pos_eq}; diag (q_max, n_catch, e_sum, src_sum) identical {diag_eq} -> {'PASS' if passE else 'FAIL'}")
    g = json.load(open(os.path.join(EXT, "cfg555_work", "cfg555_527_LRcan_L200.json")))
    pg = np.array(VEa["snap"]["z0"]["P_grav"]); rg = np.array(g["P_grav"])
    dG = float(np.max(np.abs(pg / rg - 1))); dS = float(abs(VEa["snap"]["z0"]["sigma8_grav"] / g["s8_grav"] - 1))
    RES["gates"]["V-G"] = dict(maxrelPgrav=dG, relsig8grav=dS, PASS=bool(dG <= 1e-5 and dS <= 1e-5))
    P(f"V-G gravitating field vs CFG555 (527_LRcan_L200): max|dPgrav/Pgrav| {dG:.2e}, |ds8g| {dS:.2e} -> {'PASS' if dG <= 1e-5 and dS <= 1e-5 else 'FAIL'}")
else: P("V-E(a): not run")

# ---------------- V-E (b)
VEb, _ = mine("VEb")
if VEb:
    b_ref, fb = ref530("S0_L100_N256"); c = cmp_runs(b_ref, VEb)
    pr = np.load(glob.glob(os.path.join(R530, "S0_L100_N256", "*_z0.npz"))[0])["pos"]; pm = np.load(glob.glob(os.path.join(W, "VEb", "*_z0pos.npz"))[0])["pos"]
    pos_eq = bool(np.array_equal(pr, pm)); passE = all(c[z]["maxrelP"] <= 1e-12 and c[z]["relsig8"] <= 1e-12 for z in c) and pos_eq
    RES["gates"]["V-E(b)"] = dict(cmp=c, z0_positions_identical=pos_eq, PASS=passE, bitwise=all(c[z]["maxrelP"] == 0 and c[z]["relsig8"] == 0 for z in c))
    P(f"V-E(b) exact S0 L100 N256 (NSEED 512) vs CFG530: " + "; ".join(f"{z}: {c[z]['maxrelP']:.1e} / {c[z]['relsig8']:.1e}" for z in c) + f"; z0 positions identical {pos_eq} -> {'PASS' if passE else 'FAIL'}")
else: P("V-E(b): not run")

# ---------------- V-L
khi = math.pi * 256 / (4 * 100.0)
tiers = {}
for job, run in (("VLs", "S0_L100_N256"), ("VLr", "LRcan_L100_N256")):
    m_, _ = mine(job)
    if not m_: P(f"V-L {job}: not run"); continue
    r_, _ = ref530(run); c = cmp_runs(r_, m_, kmax=khi)
    mp = max(c[z]["maxrelP"] for z in c); ms = max(c[z]["relsig8"] for z in c)
    rec = dict(cmp=c, max_relP=mp, max_relsig8=ms, STRICT=bool(mp <= 1e-5 and ms <= 1e-5), SCIENCE_P_s8=bool(mp <= 1e-3 and ms <= 1e-4))
    if job == "VLr":
        d = np.load(os.path.join(EXT, "cfg530_work", "profiles", "N256", "cfg526_LRcan_L100.npz"))
        kr = np.array(d["kgrav"]); Br = np.array(d["pgrav"]) / np.array(d["ppart"])
        km = np.array(m_["snap"]["z0"]["k"]); Bm = np.array(m_["snap"]["z0"]["P_grav"]) / np.array(m_["snap"]["z0"]["P"])
        assert np.allclose(kr, km, rtol=1e-6)
        sel = km <= khi * (1 + 1e-9); dB = float(np.max(np.abs(Bm[sel] - Br[sel])))
        rec.update(max_absdB_z0=dB, B_at_k1=[float(np.interp(1.0, km, Bm)), float(np.interp(1.0, kr, Br))]); rec["SCIENCE"] = bool(rec["SCIENCE_P_s8"] and dB <= 1e-3)
    else: rec["SCIENCE"] = rec["SCIENCE_P_s8"]
    RES["gates"][f"V-L {job}"] = rec
    P(f"V-L {job} lean vs CFG530 {run} (k <= {khi:.3f}): max|dP/P| {mp:.2e}, max|ds8/s8| {ms:.2e}" + (f", max|dB| (z0) {rec['max_absdB_z0']:.2e}" if job == "VLr" else "")
      + f" -> STRICT {'PASS' if rec['STRICT'] else 'FAIL'}, SCIENCE {'PASS' if rec['SCIENCE'] else 'FAIL'}")
    P("     per snapshot: " + "; ".join(f"{z}: {c[z]['maxrelP']:.1e} / {c[z]['relsig8']:.1e}" for z in c))

# ---------------- V-M
mem = {}
for job in ("VEa", "VEb", "VLs", "VLr", "VMs", "VMr", "P0", "P1", "P2"):
    wl = os.path.join(W, job, "watch.log")
    if not os.path.exists(wl): continue
    pk = 0.0; sw0 = None; swmax = 0.0
    for line in open(wl):
        mm = re.search(r"rss ([\d.]+) GB peak ([\d.]+) swap_used ([\d.]+) MB \(start ([\d.]+)\)", line)
        if mm: pk = max(pk, float(mm.group(2))); swmax = max(swmax, float(mm.group(3)) - float(mm.group(4)))
    m_, _ = mine(job)
    mem[job] = dict(watch_peak_rss_gb=pk, max_swap_growth_mb=swmax, engine_maxrss_gb=(m_ or {}).get("maxrss_gb") or ((m_ or {}).get("mem") or [[None, None]])[-1][1])
    P(f"V-M {job}: watchdog peak RSS {pk:.2f} GB, engine ru_maxrss {mem[job]['engine_maxrss_gb']}, swap growth {swmax:.0f} MB")
RES["memory"] = mem
VMs, _ = mine("VMs")
if VMs and "z0" in VMs["snap"]:
    r_, _ = ref530("S0_L100_N512"); c = cmp_runs(r_, VMs, kmax=math.pi * 512 / 400.0)
    RES["reported_VMs_vs_CFG530_S0_N512"] = c
    P("reported: lean S0 L100 N512 vs CFG530 S0_L100_N512 (k <= 4.02): " + "; ".join(f"{z}: {c[z]['maxrelP']:.1e} / {c[z]['relsig8']:.1e}" for z in c))
json.dump(RES, open(os.path.join(HERE, "cfg596_validate.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg596_validate.out"), "w").write("\n".join(OUT) + "\n")
