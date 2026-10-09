#!/usr/bin/env python3
"""CFG521 analysis (FROZEN_CRITERIA.md): CFG518's census placement in small boxes (L = 50, fallback 25; L = 100 reported) at 256^3,
each run vs the matched S0 of the same box/seed/resolution.  Gate over k <= k_Nyq/4 with sigma8 (box modes) and sigma(4).
CFG521_MUTATE=1 writes cfg521_analysis_MUTATE.out / cfg521_results_MUTATE.json with the MUTATE run in the DC-can slot."""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg521_work"); MUT = os.environ.get("CFG521_MUTATE", "0") == "1"
J = lambda f: os.path.join(W, f)
def tag(sw="RES", foot="canonical", mode="census", nocomp=False, L=50, npg=256):
    return f"cfg521_{sw}_TA{'_NOCOMP' if nocomp else ''}_MIXA_MASSCONS_fret{mode}_FLAT_{foot}_N{npg}" + (f"_L{L:g}" if L != 200 else "") + ".json"
L_, OUT = [], {"mutate_analysis": MUT}
def P(s=""): print(s); L_.append(s)
ld = lambda p: json.load(open(p)) if os.path.exists(p) else None

def rat(d, d0, L):
    s, s0 = d["snap"]["z0"], d0["snap"]["z0"]; kmax = math.pi * 256 / (4 * L)
    k, Pk = np.array(s["k"]), np.array(s["P"]); pr = Pk / np.interp(k, np.array(s0["k"]), np.array(s0["P"]))
    m, m1 = k <= kmax, k <= 1.0
    sn = d["snap"]; g = lambda key, nm="z0": sn[nm].get(key)
    return dict(L=L, kmax=kmax, s8=s["sigma8"] / s0["sigma8"], s4=s["sigma4"] / s0["sigma4"], s2=s["sigma2"] / s0["sigma2"],
                s8_box_S0=s0["sigma8"], pdev=float(np.max(np.abs(pr[m] - 1))), k_at_pdev=float(k[m][np.argmax(np.abs(pr[m] - 1))]),
                pdev_k1=float(np.max(np.abs(pr[m1] - 1))),
                P_at={str(x): float(np.interp(x, k, pr)) for x in (0.3, 1.0, 3.0) if x <= kmax},
                q_max_all=max((v.get("q_max") or 0.0) for v in sn.values()),
                overdraw_all=max((v.get("overdraw_mass") or 0.0) for v in sn.values()),
                cap_any=any(bool(v.get("cap_active")) for v in sn.values()),
                fret_catch={n: g("fret_mass_mean_catch", n) for n in ("z1", "z0.5", "z0")},
                fret_le02={n: g("fret_mass_frac_le02", n) for n in ("z1", "z0.5", "z0")},
                fret_e={n: g("fret_e_mean", n) for n in ("z1", "z0.5", "z0")},
                hosts_z0=g("hosts"), n_catch_z0=g("n_catch"), e_sum={n: sn[n].get("e_sum") for n in ("z1", "z0.5", "z0")},
                runtime_s=d.get("runtime_s"))
def cat(r):
    if abs(r["s8"] - 1) > 0.2 or abs(r["s4"] - 1) > 0.2: return "FAIL"
    return "GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and abs(r["s4"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION"
f3 = lambda x: "nan" if x is None else f"{x:.3f}"

# ---- K0 engine identity
a, b = ld(J(tag(L=200, npg=128))), ld(os.path.join(W, "k0_ref", "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N128.json"))
K0 = None
if a and b:
    ds = max(abs(a["snap"][n]["sigma8"] - b["snap"][n]["sigma8"]) for n in b["snap"])
    dp = max(float(np.max(np.abs(np.array(a["snap"][n]["P"]) / np.array(b["snap"][n]["P"]) - 1))) for n in b["snap"])
    K0 = ds <= 1e-6 and dp <= 1e-5; OUT["K0"] = dict(d_sigma8=ds, max_dP_rel=dp, pass_=K0)
    P(f"K0 engine identity (L = 200, 128^3, census canonical, cfg521 vs cfg518 copy): |d s8| {ds:.2e}, max|dP/P| {dp:.2e} -> {'PASS' if K0 else 'FAIL'}")
else:
    P("K0: PENDING")
s0a, s0b = ld(J(tag(sw="S0", L=200, npg=128))), ld(os.path.join(EXT, "cfg359_work", "cfg359_S0_FLAT_canonical_N128.json"))
if s0a and s0b:
    ds = abs(s0a["snap"]["z0"]["sigma8"] / s0b["snap"]["z0"]["sigma8"] - 1)
    dp = float(np.max(np.abs(np.array(s0a["snap"]["z0"]["P"]) / np.interp(s0a["snap"]["z0"]["k"], s0b["snap"]["z0"]["k"], s0b["snap"]["z0"]["P"]) - 1)))
    OUT["S0_L200_vs_CFG359"] = dict(d_s8_rel=ds, max_dP_rel=dp)
    P(f"  (reported) cfg521 S0 L = 200 128^3 vs CFG359 S0 N128: |s8 ratio - 1| {ds:.2e}, max|P ratio - 1| {dp:.2e}")

# ---- boxes
RUNS = {"DC-can": dict(), "DC-alt": dict(foot="alt"), "MUTATE (no compensation)": dict(nocomp=True), "K1 (f_ret = 1)": dict(mode="one")}
BOX = {}
for Lb in (50, 25, 100):
    s0 = ld(J(tag(sw="S0", L=Lb)))
    if s0 is None: continue
    P(f"\nL = {Lb} Mpc/h, 256^3 (k <= {math.pi * 256 / (4 * Lb):.2f} h/Mpc), vs matched S0 (box sigma8 {s0['snap']['z0']['sigma8']:.4f}, sigma4 {s0['snap']['z0']['sigma4']:.4f})")
    BOX[Lb] = {}
    for n, kw in RUNS.items():
        d = ld(J(tag(L=Lb, **kw)))
        if d is None: BOX[Lb][n] = None; continue
        r = rat(d, s0, Lb); r["verdict"] = cat(r); BOX[Lb][n] = r
        P(f"  {n:25s}: s8 {r['s8']:.4f}  s4 {r['s4']:.4f}  s2 {r['s2']:.4f}  max|P-1| {r['pdev']:.4f} (at k {r['k_at_pdev']:.2f})  k<=1 {r['pdev_k1']:.4f}  "
          f"P@" + "/".join(r["P_at"]) + " " + "/".join(f"{v:.3f}" for v in r["P_at"].values()) + f" -> {r['verdict']}")
        P(f"  {'':25s}  q_max {r['q_max_all']:.3f}  overdraw {r['overdraw_all']:.4f}  cap acted {r['cap_any']}  "
          f"f_ret catch z1/z0.5/z0 {f3(r['fret_catch']['z1'])}/{f3(r['fret_catch']['z0.5'])}/{f3(r['fret_catch']['z0'])}  "
          f"mass frac f_ret<=0.2 (z0) {f3(r['fret_le02']['z0'])}  e-weighted f_ret (z0) {f3(r['fret_e']['z0'])}")
    dc, k1 = BOX[Lb].get("DC-can"), BOX[Lb].get("K1 (f_ret = 1)")
    if dc and k1 and k1["e_sum"]["z0"]:
        P("  Sum e census / K1: " + "  ".join(f"{n} {dc['e_sum'][n] / k1['e_sum'][n]:.3f}" for n in ("z1", "z0.5", "z0")))
    if dc and dc.get("hosts_z0"):
        P("  resolved hosts at z = 0 (r_ON: count, log M_ta): " + "; ".join(f"{R}: {v[0]}, {v[1]}" for R, v in dc["hosts_z0"].items()))
OUT["boxes"] = {str(k): v for k, v in BOX.items()}

# ---- f_ret achievement and decision
def achieved(Lb):
    r = BOX.get(Lb, {}).get("DC-can"); return None if r is None else (r["fret_catch"]["z0"] is not None and r["fret_catch"]["z0"] <= 0.20)
a50, a25 = achieved(50), achieved(25)
scored = 50 if a50 else (25 if (a50 is False and a25) else None)
P(f"\nf_ret achievement (catchment mean <= 0.20 at z = 0): L = 50 {a50}; L = 25 {a25}; scored box: {scored}")
v = "PENDING"
if K0 is False:
    v = "INVALID (K0 fails)"
elif a50 is False and a25 is False:
    v = "NOT ACHIEVED"
elif scored and K0:
    B = BOX[scored]; c, al, mu = B.get("DC-can"), B.get("DC-alt"), B.get("MUTATE (no compensation)")
    if MUT and mu: c = mu; P("  MUTATE ANALYSIS: the no-compensation run is placed in the DC-can slot.")
    if c and al and mu:
        ok = [x["verdict"] == "GROWTH OK" for x in (c, al)]
        v = ("INCONCLUSIVE (MUTATE is GROWTH OK)" if mu["verdict"] == "GROWTH OK" else
             f"PASS (L = {scored}, 256^3)" if all(ok) else "PARTIAL" if any(ok) else "FAIL")
OUT["scored_box"] = scored; OUT["verdict"] = v; OUT["verdict_512"] = "PENDING (not run)"
P(f"LANE VERDICT: {v}\n512^3: PENDING (not run)")
P("\nkappa = 1/2 FITTED; footings never pooled; cold energy MASS still required; not theory closed.")
sfx = "_MUTATE" if MUT else ""
open(os.path.join(HERE, f"cfg521_analysis{sfx}.out"), "w").write("\n".join(L_) + "\n")
json.dump(OUT, open(os.path.join(HERE, f"cfg521_results{sfx}.json"), "w"), indent=1)
