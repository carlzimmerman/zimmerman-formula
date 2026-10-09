#!/usr/bin/env python3
"""CFG527 analysis (FROZEN_CRITERIA.md): growth (Gate 2), controls (Gate 3), stability, and the per-footing decision, reading Gate 1 from
cfg527_profiles.json.  Matched S0 controls reused (sha256 recorded).  Writes cfg527_analysis.out and cfg527_results.json.
Also the declared halo-concentration ratio c/c_S0 (CFG524 post-hoc definition, reported)."""
import os, json, math, hashlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W, W521, W518, W524 = (os.path.join(EXT, d) for d in ("cfg527_work", "cfg521_work", "cfg518_work", "cfg524_work"))
L_, OUT = [], {"lane": "CFG527", "date": "2026-10-09",
               "settings": "kappa = 1/2 FITTED; footings never pooled; a0 flat; nu_mono; cold energy MASS required; not theory closed"}
def P(s=""): print(s); L_.append(s)
ld = lambda p: json.load(open(p)) if os.path.exists(p) else None
def t527(mix, draw, L, foot="canonical", mode="census", nocomp=False, npg=256):
    return os.path.join(W, f"cfg527_RES_TA{'_NOCOMP' if nocomp else ''}_{mix}_MASSCONS_fret{mode}_FLAT_{foot}_N{npg}" + (f"_L{L:g}" if L != 200 else "") + f"_draw{draw}.json")
S0 = {50: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L50.json"),
      25: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L25.json"),
      100: os.path.join(W521, "cfg521_S0_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L100.json"),
      200: os.path.join(EXT, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json"),
      "200_512": os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json")}
KN = lambda L, npg=256: math.pi * npg / (4 * L)
RUNS = {"LR-can": ("NOFILT", "SHELL", "canonical", "census", False), "LR-alt": ("NOFILT", "SHELL", "alt", "census", False),
        "K1": ("NOFILT", "SHELL", "canonical", "one", False), "MUTATE A": ("MIXA", "SC", "canonical", "census", False),
        "MUTATE B": ("NOFILT", "SHELL", "canonical", "census", True), "SHF": ("MIXA", "SHELL", "canonical", "census", False)}
NOFILT_RUNS = ("LR-can", "LR-alt", "K1", "MUTATE B")
f3 = lambda x: "  -  " if x is None else f"{x:.3f}"

P("CFG527: law-respecting engine (shell draw outside the census edge, unfiltered retained-baryon source). Matched S0 controls (reused):")
OUT["S0"] = {}
for k, p in S0.items():
    d = ld(p)
    if d is None: P(f"  {k}: MISSING"); continue
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    OUT["S0"][str(k)] = dict(file=os.path.basename(p), sha256=sha, sigma8_z0=d["snap"]["z0"]["sigma8"])
    P(f"  L{k}: {os.path.basename(p)} sha256 {sha[:16]}  sigma8(z0) {d['snap']['z0']['sigma8']:.4f}")

# ---- Gate 3a: MUTATE A reproduction of CFG521 DC-can
P("\nMUTATE A (SC draw + MIX-A) reproduction of CFG521 DC-can (|d s8|/s8 and max|dP/P| <= 1e-8 at every snapshot):")
REPRO = {}
for Lb in (50, 25):
    a = ld(t527("MIXA", "SC", Lb)); b = ld(os.path.join(W521, f"cfg521_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L{Lb}.json"))
    if not (a and b): REPRO[Lb] = None; P(f"  L{Lb}: PENDING"); continue
    ds = max(abs(a["snap"][n]["sigma8"] / b["snap"][n]["sigma8"] - 1) for n in b["snap"])
    dp = max(float(np.max(np.abs(np.array(a["snap"][n]["P"]) / np.array(b["snap"][n]["P"]) - 1))) for n in b["snap"])
    REPRO[Lb] = dict(d_sigma8_rel=ds, max_dP_rel=dp, pass_=bool(ds <= 1e-8 and dp <= 1e-8))
    P(f"  L{Lb}: |d s8|/s8 {ds:.2e}, max|dP/P| {dp:.2e} -> {'PASS' if REPRO[Lb]['pass_'] else 'FAIL'}")
OUT["mutate_A_repro"] = {str(k): v for k, v in REPRO.items()}

def ratio_curve(d, d0, n="z0"):
    s, s0 = d["snap"][n], d0["snap"][n]; k = np.array(s["k"])
    return k, np.array(s["P"]) / np.interp(k, np.array(s0["k"]), np.array(s0["P"]))
def at_k(k, pr, x): return float(pr[np.argmin(np.abs(k - x))]) if x <= k.max() * 1.01 else None
def rat(d, d0, L, npg=256):
    s, s0, sn = d["snap"]["z0"], d0["snap"]["z0"], d["snap"]; k, pr = ratio_curve(d, d0)
    m, m1 = k <= KN(L, npg), k <= 1.0
    snaps = list(sn.values())
    fin = all(all(math.isfinite(v[x]) for x in ("sigma8", "e_sum", "src_sum") if v.get(x) is not None)
              and bool(np.all(np.isfinite(v["P"]))) and v.get("finite", True) for v in snaps)
    kny2 = math.pi * npg / (2 * L)
    r = dict(L=L, kmax=KN(L, npg), s8=s["sigma8"] / s0["sigma8"], pdev=float(np.max(np.abs(pr[m] - 1))),
             k_at_pdev=float(k[m][np.argmax(np.abs(pr[m] - 1))]), pdev_k1=float(np.max(np.abs(pr[m1] - 1))),
             P_at={str(x): at_k(k, pr, x) for x in (0.3, 1.0, 2.0, 3.0, 4.0, 8.0)},
             k4_by_z={n: at_k(*ratio_curve(d, d0, n), 4.0) for n in ("z1", "z0.5", "z0") if n in d0["snap"]},
             P_at_kNy2=at_k(k, pr, kny2), finite=bool(fin),
             q_max_all=max((v.get("q_max") or 0.0) for v in snaps), overdraw_all=max((v.get("overdraw_mass") or 0.0) for v in snaps),
             cap_snaps=sum(bool(v.get("cap_active")) for v in snaps), cap_n_max=max((v.get("cap_n") or 0) for v in snaps),
             cap_e_removed_max=max((v.get("cap_e_removed_frac") or 0.0) for v in snaps),
             n_shell_empty_max=max((v.get("n_shell_empty") or 0) for v in snaps),
             e_frac_shell_empty_max=max((v.get("e_frac_shell_empty") or 0.0) for v in snaps),
             shell_frac={n: sn[n].get("shell_frac") for n in ("z1", "z0.5", "z0")},
             comp_in_edge_z0=s.get("comp_in_edge"), src_in_edge_z0=s.get("src_in_edge"),
             draw_rho_z0=s.get("draw_rho_mean"), sc_rho_z0=s.get("sc_rho_mean"),
             e_sum={n: sn[n].get("e_sum") for n in ("z1", "z0.5", "z0")}, n_catch_z0=s.get("n_catch"), runtime_s=d.get("runtime_s"))
    r["stable"] = bool(fin and r["P_at_kNy2"] is not None and r["P_at_kNy2"] <= 2.0)
    if "sigma4" in s and "sigma4" in s0:
        r.update(s4=s["sigma4"] / s0["sigma4"], s2=s["sigma2"] / s0["sigma2"])
    return r
def cat_small(r):
    if abs(r["s8"] - 1) > 0.2 or abs(r["s4"] - 1) > 0.2: return "FAIL"
    return "GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and abs(r["s4"] - 1) <= 0.05 and r["pdev"] <= 0.10 else "TENSION"
def cat_361(r):
    if abs(r["s8"] - 1) > 0.2: return "FAIL"
    return "GROWTH OK" if abs(r["s8"] - 1) <= 0.05 and r["pdev_k1"] <= 0.10 else "TENSION"

BOX = {}
for Lb in (200, 100, 50, 25):
    d0 = ld(S0[Lb])
    gate = "CFG361 cuts, k <= 1 (gating)" if Lb == 200 else ("CFG361 cuts, reported" if Lb == 100 else f"CFG521 gate vs S0, k <= {KN(Lb):.2f} (information)")
    P(f"\nL = {Lb} Mpc/h, 256^3 ({gate})")
    P(f"  {'run':9s} {'s8':>7s} {'s4':>7s} {'maxdev':>7s} {'(k)':>5s} {'k<=1':>6s}  P/P_S0 @0.3/1/2/3/4/8              verdict     q_max  cap(snaps/n/e-rm)  empty-shell(n/e)  shell_frac(z0)  draw/sc rho(z0)  P@kNy/2 stable")
    BOX[Lb] = {}
    for n, (mix, dr, ft, md, nc) in RUNS.items():
        d = ld(t527(mix, dr, Lb, ft, md, nc))
        if d is None: continue
        r = rat(d, d0, Lb); r["verdict_361"] = cat_361(r)
        if Lb in (50, 25): r["verdict_521"] = cat_small(r)
        r["verdict"] = r["verdict_361"] if Lb in (200, 100) else r["verdict_521"]
        BOX[Lb][n] = r
        pa = "/".join(f3(r["P_at"][x]) for x in ("0.3", "1.0", "2.0", "3.0", "4.0", "8.0"))
        P(f"  {n:9s} {r['s8']:7.4f} {r.get('s4', float('nan')):7.4f} {r['pdev']:7.4f} {r['k_at_pdev']:5.2f} {r['pdev_k1']:6.4f}  {pa:34s} {r['verdict']:10s} "
          f"{r['q_max_all']:.3f}  {r['cap_snaps']}/{r['cap_n_max']}/{r['cap_e_removed_max']:.2e}  {r['n_shell_empty_max']}/{r['e_frac_shell_empty_max']:.2e}  "
          f"{f3(r['shell_frac']['z0'])}  {f3(r['draw_rho_z0'])}/{f3(r['sc_rho_z0'])}  {f3(r['P_at_kNy2'])} {'yes' if r['stable'] else 'NO'}")
    k1 = BOX[Lb].get("K1"); lr = BOX[Lb].get("LR-can")
    if k1 and lr and k1["e_sum"]["z0"]:
        P("  Sum e LR-can / K1: " + "  ".join(f"{z} {lr['e_sum'][z] / k1['e_sum'][z]:.3f}" for z in ("z1", "z0.5", "z0")))
OUT["boxes"] = {str(k): v for k, v in BOX.items()}

# ---- trend at k = 4 (with the old-draw and CFG524 R2 references from JSON)
OLD = {}
for Lb, p in ((200, os.path.join(W518, "cfg518_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256.json")),
              (100, os.path.join(W521, "cfg521_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L100.json")),
              (50, os.path.join(W521, "cfg521_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L50.json")),
              (25, os.path.join(W521, "cfg521_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256_L25.json"))):
    a, b = ld(p), ld(S0[Lb])
    if a and b: OLD[Lb] = at_k(*ratio_curve(a, b), 4.0)
R2 = {}
for Lb in (200, 100, 50, 25):
    a, b = ld(os.path.join(W524, f"cfg524_RES_TA_MIXA_MASSCONS_fretcensus_FLAT_canonical_N256" + (f"_L{Lb}" if Lb != 200 else "") + "_drawR2.json")), ld(S0[Lb])
    if a and b: R2[Lb] = at_k(*ratio_curve(a, b), 4.0)
P("\nTrend: P/P_S0 at k = 4 h/Mpc (z = 0, nearest bin), L = 200 / 100 / 50 / 25")
TR = {"old draw (CFG518/521 can)": [OLD.get(Lb) for Lb in (200, 100, 50, 25)], "CFG524 R2-can": [R2.get(Lb) for Lb in (200, 100, 50, 25)]}
for n in ("LR-can", "LR-alt", "SHF", "MUTATE A", "K1"):
    TR[n] = [(BOX.get(Lb, {}).get(n) or {}).get("P_at", {}).get("4.0") for Lb in (200, 100, 50, 25)]
for n, v in TR.items(): P(f"  {n:28s} " + " / ".join(f3(x) for x in v))
OUT["trend_k4"] = TR
for n in ("LR-can", "LR-alt", "MUTATE A"):
    r = BOX.get(50, {}).get(n)
    if r: P(f"  L50 {n} P/P_S0 at k = 4 by z (z1 / z0.5 / z0): " + " / ".join(f3(r["k4_by_z"].get(z)) for z in ("z1", "z0.5", "z0")))

# ---- small-box r(k) convergence (CFG526 rule) at k = 2, 4
P("\nSmall-box r(k) = P/P_S0 convergence (|r50 - r25| <= 0.05 and |r100 - r50| <= 0.05), z = 0:")
CONV = {}
for n in ("LR-can", "LR-alt"):
    CONV[n] = {}
    for kx in ("2.0", "4.0"):
        r100, r50, r25 = ((BOX.get(Lb, {}).get(n) or {}).get("P_at", {}).get(kx) for Lb in (100, 50, 25))
        ok = None if None in (r100, r50, r25) else bool(abs(r50 - r25) <= 0.05 and abs(r100 - r50) <= 0.05)
        CONV[n][kx] = dict(r100=r100, r50=r50, r25=r25, converged=ok)
        P(f"  {n} k = {kx}: L100 {f3(r100)}  L50 {f3(r50)}  L25 {f3(r25)} -> {'converged' if ok else ('PENDING' if ok is None else 'NOT converged')}")
OUT["r_convergence"] = CONV

# ---- Gate 1 (from cfg527_profiles.json)
G1 = ld(os.path.join(HERE, "cfg527_profiles.json"))
P("\nGate 1 (cfg527_profiles.json):")
if G1:
    for f, v in G1["gate1"].items(): P(f"  [{f}] {v['verdict']}")
    P(f"  MUTATE A fails law consistency: {G1['MUTA_fails_law']}")
else:
    P("  PENDING")

# ---- stability (all NOFILT runs)
stab = {f"L{Lb} {n}": BOX[Lb][n]["stable"] for Lb in BOX for n in BOX[Lb] if n in NOFILT_RUNS}
P("\nStability (NOFILT runs; finite and P/P_S0(k_Nyq/2, z0) <= 2): " + ("all STABLE" if stab and all(stab.values()) else json.dumps(stab)))
P("  SHF (filter on) vs LR-can P/P_S0 at k_Nyq/2: " + "; ".join(f"L{Lb} {f3((BOX[Lb].get('SHF') or {}).get('P_at_kNy2'))} vs {f3((BOX[Lb].get('LR-can') or {}).get('P_at_kNy2'))}" for Lb in (50, 25) if Lb in BOX))
OUT["stability"] = stab

# ---- decision per footing
P("\nDecision (per footing):")
mb = (BOX.get(200, {}).get("MUTATE B") or {}).get("verdict_361")
P(f"  MUTATE B (no compensation, NOFILT, L200): {mb}  (must NOT be GROWTH OK)")
VER = {}
for f, n in (("canonical", "LR-can"), ("alt", "LR-alt")):
    g1 = (G1 or {}).get("gate1", {}).get(f, {}).get("verdict")
    g200 = (BOX.get(200, {}).get(n) or {}).get("verdict_361")
    conv = CONV[n]; rconv = [conv[k]["converged"] for k in conv]
    stab_f = [v for k, v in stab.items() if n in k]
    items = {"gate1": g1, "L200": g200, "MUTATE_B": mb, "r_converged_k2_k4": rconv, "stable": stab_f,
             "CFG521_small_box_vs_S0": {f"L{Lb}": (BOX.get(Lb, {}).get(n) or {}).get("verdict_521") for Lb in (50, 25)}}
    if None in (g1, g200, mb) or None in rconv or None in REPRO.values() or G1 is None:
        v = "PENDING"
    elif not all(r["pass_"] for r in REPRO.values()) or not all(stab_f):
        v = "INVALID (" + ("MUTATE A reproduction fails" if not all(r["pass_"] for r in REPRO.values()) else "UNSTABLE NOFILT run") + ")"
    elif g1 == "NOT DIAGNOSTIC" or not G1["MUTA_fails_law"]:
        v = "NOT DIAGNOSTIC (" + ("Gate 1 rule 1" if g1 == "NOT DIAGNOSTIC" else "MUTATE A passes law consistency") + ")"
    elif g1.startswith("NOT LAW-CONSISTENT"):
        v = f"FAIL ({g1})"
    elif g1 == "LAW-CONSISTENT" and g200 == "GROWTH OK" and mb != "GROWTH OK" and all(rconv):
        v = "PASS (256^3)"
    else:
        why = []
        if g200 != "GROWTH OK": why.append(f"L200 {g200}")
        if mb == "GROWTH OK": why.append("MUTATE B GROWTH OK -> L200 INCONCLUSIVE")
        if not all(rconv): why.append("small-box r(k) not converged at " + ", ".join(k for k in conv if not conv[k]["converged"]))
        v = "PARTIAL (" + "; ".join(why) + ")"
    VER[f] = dict(verdict=v, items=items); P(f"  [{f}] {v}")
    P("      " + json.dumps(items))
OUT["verdicts"] = VER

# ---- 512^3
d5, d05 = ld(t527("NOFILT", "SHELL", 200, npg=512)), ld(S0["200_512"])
both = all(VER[f]["verdict"].startswith("PASS") for f in VER)
if d5 and d05:
    r5 = rat(d5, d05, 200, 512); r5["verdict"] = cat_361(r5); OUT["512_LRcan"] = r5
    v5 = "CONFIRMED" if r5["verdict"] == "GROWTH OK" else "NOT CONFIRMED"
    P(f"\n512^3 LR-can L200 vs CFG411 S0 N512: s8 {r5['s8']:.4f}, max|P-1|(k<=1) {r5['pdev_k1']:.4f}, P@1/2/4 {f3(r5['P_at']['1.0'])}/{f3(r5['P_at']['2.0'])}/{f3(r5['P_at']['4.0'])}, "
      f"q_max {r5['q_max_all']:.3f}, cap snaps {r5['cap_snaps']} -> {r5['verdict']} -> {v5}")
else:
    v5 = "PENDING" if both else "not run (not both footings PASS at 256^3)"
OUT["verdict_512"] = v5; P(f"512^3: {v5}")
P("\nkappa = 1/2 FITTED; footings never pooled; cold energy MASS still required; not theory closed.")
open(os.path.join(HERE, "cfg527_analysis.out"), "w").write("\n".join(L_) + "\n")
json.dump(OUT, open(os.path.join(HERE, "cfg527_results.json"), "w"), indent=1)
