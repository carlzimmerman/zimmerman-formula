#!/usr/bin/env python3
"""CFG524 analysis (FROZEN_CRITERIA.md): compensation drawn only from the unsettled reservoir (R2 literal, R1 switch-free; SC = MUTATE = cfg521).
Small boxes (L = 50, 25) vs CFG521's matched S0 with CFG521's gate (k <= k_Nyq/4, sigma8 + sigma4); L = 200 vs CFG359 S0 N256 with the CFG361 cuts (k <= 1);
L = 100 reported.  Writes cfg524_analysis.out and cfg524_results.json."""
import os, json, math, hashlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W, W521, W518 = (os.path.join(EXT, d) for d in ("cfg524_work", "cfg521_work", "cfg518_work"))
L_, OUT = [], {}
def P(s=""): print(s); L_.append(s)
ld = lambda p: json.load(open(p)) if os.path.exists(p) else None
def tag(draw, foot="canonical", mode="census", L=50, npg=256, pre="cfg524"):
    t = f"{pre}_RES_TA_MIXA_MASSCONS_fret{mode}_FLAT_{foot}_N{npg}" + (f"_L{L:g}" if L != 200 else "")
    return t + (f"_draw{draw}" if draw else "") + ".json"
S0 = {50: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L50.json"),
      25: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L25.json"),
      100: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L100.json"),
      200: os.path.join(EXT, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json"),
      "200_512": os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json")}
KN = lambda L, npg=256: math.pi * npg / (4 * L)

P("CFG524: compensation drawn only from the unsettled cold-energy reservoir. Matched S0 controls (reused):")
OUT["S0"] = {}
for k, p in S0.items():
    d = ld(p)
    if d is None: P(f"  {k}: MISSING {os.path.basename(p)}"); continue
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    cfgf = {x: d.get(x) for x in ("switch", "np", "mesh", "L", "rmin", "z_i", "nsteps", "amp")}
    OUT["S0"][str(k)] = dict(file=os.path.basename(p), sha256=sha, cfg=cfgf, sigma8_z0=d["snap"]["z0"]["sigma8"])
    P(f"  L{k}: {os.path.basename(p)} sha256 {sha[:16]}  cfg {cfgf}  box sigma8(z0) {d['snap']['z0']['sigma8']:.4f}")

# ---- MUTATE reproduction (engine integrity)
P("\nMUTATE (draw SC) reproduction of CFG521 DC-can (|d s8|/s8 and max|dP/P| <= 1e-8 at every snapshot):")
REPRO = {}
for Lb in (50, 25):
    a, b = ld(os.path.join(W, tag("SC", L=Lb))), ld(os.path.join(W521, tag(None, L=Lb, pre="cfg521")))
    if not (a and b): REPRO[Lb] = None; P(f"  L{Lb}: PENDING"); continue
    ds = max(abs(a["snap"][n]["sigma8"] / b["snap"][n]["sigma8"] - 1) for n in b["snap"])
    dp = max(float(np.max(np.abs(np.array(a["snap"][n]["P"]) / np.array(b["snap"][n]["P"]) - 1))) for n in b["snap"])
    REPRO[Lb] = dict(d_sigma8_rel=ds, max_dP_rel=dp, pass_=bool(ds <= 1e-8 and dp <= 1e-8))
    P(f"  L{Lb}: |d s8|/s8 {ds:.2e}, max|dP/P| {dp:.2e} -> {'PASS' if REPRO[Lb]['pass_'] else 'FAIL'}")
OUT["mutate_repro"] = {str(k): v for k, v in REPRO.items()}

def ratio_curve(d, d0, n="z0"):
    s, s0 = d["snap"][n], d0["snap"][n]; k = np.array(s["k"])
    return k, np.array(s["P"]) / np.interp(k, np.array(s0["k"]), np.array(s0["P"]))
def at_k(k, pr, x): return float(pr[np.argmin(np.abs(k - x))]) if x <= k.max() * 1.01 else None
def rat(d, d0, L, npg=256):
    s, s0, sn = d["snap"]["z0"], d0["snap"]["z0"], d["snap"]; k, pr = ratio_curve(d, d0)
    m, m1 = k <= KN(L, npg), k <= 1.0
    snaps = [v for v in sn.values()]
    r = dict(L=L, kmax=KN(L, npg), s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr[m] - 1))),
             k_at_pdev=float(k[m][np.argmax(np.abs(pr[m] - 1))]), pdev_k1=float(np.max(np.abs(pr[m1] - 1))),
             P_at={str(x): at_k(k, pr, x) for x in (0.1, 0.3, 1.0, 3.0, 4.0, 8.0)},
             k4_by_z={n: at_k(*ratio_curve(d, d0, n), 4.0) for n in ("z1", "z0.5", "z0") if n in d0["snap"]},
             q_max_all=max((v.get("q_max") or 0.0) for v in snaps), overdraw_all=max((v.get("overdraw_mass") or 0.0) for v in snaps),
             cap_snaps=sum(bool(v.get("cap_active")) for v in snaps), cap_n_max=max((v.get("cap_n") or 0) for v in snaps),
             cap_e_removed_max=max((v.get("cap_e_removed_frac") or 0.0) for v in snaps),
             res_frac={n: sn[n].get("res_frac") for n in ("z1", "z0.5", "z0")},
             draw_rho_z0=s.get("draw_rho_mean"), sc_rho_z0=s.get("sc_rho_mean"),
             fret_catch_z0=s.get("fret_mass_mean_catch"), e_sum={n: sn[n].get("e_sum") for n in ("z1", "z0.5", "z0")},
             runtime_s=d.get("runtime_s"))
    if "sigma4" in s and "sigma4" in s0:
        r.update(s4=s["sigma4"] / s0["sigma4"], s2=s["sigma2"] / s0["sigma2"])
    return r
def cat_small(r):
    if abs(r["s8"] - 1) > 0.2 or abs(r["s4"] - 1) > 0.2: return "FAIL"
    return "GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and abs(r["s4"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION"
def cat_361(r):
    if abs(r["s8"] - 1) > 0.2: return "FAIL"
    return "GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev_k1"] <= 0.10 else "TENSION"
f3 = lambda x: "  -  " if x is None else f"{x:.3f}"

RUNS = {"R2-can": ("R2", "canonical", "census"), "R2-alt": ("R2", "alt", "census"), "R1-can": ("R1", "canonical", "census"),
        "R1-alt": ("R1", "alt", "census"), "K1 (f_ret=1, R2)": ("R2", "canonical", "one"), "MUTATE (SC)": ("SC", "canonical", "census")}
BOX = {}
for Lb in (50, 25, 100, 200):
    d0 = ld(S0[Lb])
    if d0 is None: continue
    gate = "CFG361 cuts, k <= 1" if Lb == 200 else (f"CFG521 gate, k <= {KN(Lb):.2f}" if Lb in (50, 25) else f"reported, k <= {KN(Lb):.2f}")
    P(f"\nL = {Lb} Mpc/h, 256^3 ({gate})")
    P(f"  {'run':18s} {'s8':>7s} {'s4':>7s} {'maxdev':>7s} {'(k)':>5s} {'k<=1':>6s}  P/P_S0 @0.3/1/3/4/8          verdict     q_max  cap(snaps/n/e-rm)  res_frac(z0)  draw-rho/sc-rho(z0)")
    BOX[Lb] = {}
    for n, (dr, ft, md) in RUNS.items():
        d = ld(os.path.join(W, tag(dr, ft, md, L=Lb)))
        if d is None: continue
        r = rat(d, d0, Lb); r["verdict"] = cat_361(r) if Lb == 200 else cat_small(r); BOX[Lb][n] = r
        pa = "/".join(f3(r["P_at"][x]) for x in ("0.3", "1.0", "3.0", "4.0", "8.0"))
        P(f"  {n:18s} {r['s8']:7.4f} {r.get('s4', float('nan')):7.4f} {r['pdev']:7.4f} {r['k_at_pdev']:5.2f} {r['pdev_k1']:6.4f}  {pa:28s} {r['verdict']:10s} "
          f"{r['q_max_all']:.3f}  {r['cap_snaps']}/{r['cap_n_max']}/{r['cap_e_removed_max']:.2e}  {f3(r['res_frac']['z0'])}  "
          f"{f3(r['draw_rho_z0'])}/{f3(r['sc_rho_z0'])}")
    k1 = BOX[Lb].get("K1 (f_ret=1, R2)")
    for n in ("R2-can", "R1-can"):
        dc = BOX[Lb].get(n)
        if dc and k1 and k1["e_sum"]["z0"]:
            P(f"  Sum e {n} / K1: " + "  ".join(f"{z} {dc['e_sum'][z] / k1['e_sum'][z]:.3f}" for z in ("z1", "z0.5", "z0")))
OUT["boxes"] = {str(k): v for k, v in BOX.items()}

# ---- old-draw references (from JSON) for the convergence trend at k = 4
OLD = {}
for Lb, p, p0 in ((200, os.path.join(W518, "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256.json"), S0[200]),
                  (100, os.path.join(W521, tag(None, L=100, pre="cfg521")), S0[100]),
                  (50, os.path.join(W521, tag(None, L=50, pre="cfg521")), S0[50]), (25, os.path.join(W521, tag(None, L=25, pre="cfg521")), S0[25])):
    a, b = ld(p), ld(p0)
    if a and b: OLD[Lb] = at_k(*ratio_curve(a, b), 4.0)
P("\nConvergence trend: P/P_S0 at k = 4 h/Mpc (z = 0, nearest bin), L = 200 / 100 / 50 / 25")
TR = {"old draw (CFG518/521 census can)": [OLD.get(Lb) for Lb in (200, 100, 50, 25)]}
for n in ("R2-can", "R1-can", "R2-alt", "R1-alt"):
    TR[n] = [BOX.get(Lb, {}).get(n, {}).get("P_at", {}).get("4.0") if BOX.get(Lb, {}).get(n) else None for Lb in (200, 100, 50, 25)]
for n, v in TR.items(): P(f"  {n:34s} " + " / ".join(f3(x) for x in v))
OUT["trend_k4"] = TR
for n in ("R2-can", "R1-can", "MUTATE (SC)"):
    r = BOX.get(50, {}).get(n)
    if r: P(f"  L50 {n} P/P_S0 at k = 4 by z (z1 / z0.5 / z0): " + " / ".join(f3(r["k4_by_z"].get(z)) for z in ("z1", "z0.5", "z0")))

# ---- decision per draw rule
P("\nDecision (per draw rule):")
mu_ok = [BOX.get(Lb, {}).get("MUTATE (SC)", {}).get("verdict") for Lb in (50, 25)]
repro_ok = [REPRO.get(Lb) and REPRO[Lb]["pass_"] for Lb in (50, 25)]
VER = {}
for D in ("R2", "R1"):
    names = [(Lb, f"{D}-{f}") for Lb in (50, 25) for f in ("can", "alt")]
    big = [(200, f"{D}-{f}") for f in ("can", "alt")]
    vs = {f"L{Lb} {n}": (BOX.get(Lb, {}).get(n) or {}).get("verdict") for Lb, n in names + big}
    if None in vs.values() or None in repro_ok or None in mu_ok:
        v = "PENDING"
    elif not all(repro_ok):
        v = "INVALID (MUTATE reproduction fails)"
    elif "GROWTH OK" in mu_ok:
        v = "INCONCLUSIVE (MUTATE is GROWTH OK)"
    elif all(x == "GROWTH OK" for x in vs.values()):
        v = "PASS (256^3)"
    elif not any(vs[f"L{Lb} {n}"] == "GROWTH OK" for Lb, n in names):
        v = "FAIL"
    else:
        v = "PARTIAL (not GROWTH OK: " + ", ".join(k for k, x in vs.items() if x != "GROWTH OK") + ")"
    VER[D] = dict(verdict=v, runs=vs); P(f"  {D}: {v}")
    P("      " + "; ".join(f"{k}: {x}" for k, x in vs.items()))
nP = sum(VER[D]["verdict"].startswith("PASS") for D in VER)
lane = "PENDING" if any(VER[D]["verdict"] == "PENDING" for D in VER) else ("PASS" if nP == 2 else
       f"SPLIT ({' / '.join(D + ' ' + VER[D]['verdict'].split(' (')[0] for D in VER)})" if nP == 1 else
       f"R2 {VER['R2']['verdict'].split(' (')[0]}, R1 {VER['R1']['verdict'].split(' (')[0]}")
OUT["verdicts"] = VER; OUT["lane_verdict"] = lane; P(f"LANE VERDICT (256^3): {lane}")

# ---- 512^3 (only after a 256^3 pass)
v5 = "PENDING" if (lane == "PENDING" or nP > 0) else "not run (no draw rule passed at 256^3)"
for D in ("R2", "R1"):
    d5, d0 = ld(os.path.join(W, tag(D, L=200, npg=512))), ld(S0["200_512"])
    if d5 and d0:
        r5 = rat(d5, d0, 200, 512); r5["verdict"] = cat_361(r5); OUT[f"512_{D}"] = r5
        v5 = f"{D}: " + ("CONFIRMED" if r5["verdict"] == "GROWTH OK" else "NOT CONFIRMED")
        P(f"  512^3 {D}-can L200 vs CFG411 S0 N512: s8 {r5['s8']:.4f} max|P-1|(k<=1) {r5['pdev_k1']:.4f} P@4 {f3(r5['P_at']['4.0'])} -> {r5['verdict']}")
OUT["verdict_512"] = v5; P(f"512^3: {v5}")
P("\nkappa = 1/2 FITTED; footings never pooled; cold energy MASS still required; not theory closed.")
open(os.path.join(HERE, "cfg524_analysis.out"), "w").write("\n".join(L_) + "\n")
json.dump(OUT, open(os.path.join(HERE, "cfg524_results.json"), "w"), indent=1)
