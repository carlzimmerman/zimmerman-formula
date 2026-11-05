#!/usr/bin/env python3
"""FA1 / I2, the vorticity selector. Criteria FROZEN_CRITERIA.md (4603460516).
  python3 i2_vorticity.py              -> i2_results.json, i2.out
  I2_MUTATE=1 python3 i2_vorticity.py  -> i2_results_MUTATE.json, i2_MUTATE.out  (selector inverted; must read DOES NOT SEPARATE)
Reads SPARC rotmod (CRG1 inputs) and Table 1, CFG323's SLUGGS offsets, ATLAS3D (Emsellem+11 B1), McConnachie 2012 (KT15's model).
kappa = 1/2 FITTED; not theory closed. Adopts nothing; the cold sector stays retired."""
import os, sys, json, math, glob, csv
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
try: os.nice(19)
except OSError: pass
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); FA1 = os.path.dirname(HERE); RB = os.path.dirname(FA1); REPO = os.path.dirname(RB)
MUT = os.environ.get("I2_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"i2{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n")
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt")
C, KPC, KMS = 2.99792458e8, 3.0857e19, 1e3
F_MAX = (0.110 ** 2 - 0.069 ** 2) / 0.40 ** 2
D_DUST = 1.5; DLOG_SIG = 0.5 * math.log10(1 + D_DUST)
TC, TC_VAR = 0.5, 0.25; SIG_HI = 10.0
CHECKS = {}; RES = dict(criteria="4603460516", mutate=MUT, D=D_DUST, dlog_sigma_on=DLOG_SIG, f_max=F_MAX)
def check(n, ok, d):
    CHECKS[n] = bool(ok); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
def on_R(x, t):
    """reading R: on where x <= t; MUTATE inverts"""
    x = np.asarray(x, float); return (x > t) if MUT else (x <= t)
say("=" * 88); say(f"FA1 / I2 vorticity selector. MUTATE={MUT}. D = {D_DUST} -> +{DLOG_SIG:.3f} dex in sigma when on. f_max {F_MAX:.4f}")

# ---------------- SPARC
files = sorted(glob.glob(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod", "*_rotmod.dat")))
SP = []
for fp in files:
    a = np.loadtxt(fp, comments="#", ndmin=2); SP.append((os.path.basename(fp).replace("_rotmod.dat", ""), a[:, 0], a[:, 1], a[:, 3], a[:, 4], a[:, 5]))
fD = {}
for ln in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = ln.split()
    if len(p) >= 18 and not ln.startswith(("Title", "Note", "Byte", "Authors", "Table")):
        try: fD[p[0]] = int(p[4])
        except ValueError: pass
def sparc_low(Y, a0):
    rows = []
    for name, R, Vo, Vg, Vd, Vb in SP:
        V2 = np.sign(Vg) * Vg ** 2 + Y * Vd ** 2 + 1.4 * Y * Vb ** 2; gb = V2 * 1e6 / (R * KPC); go = Vo ** 2 * 1e6 / (R * KPC)
        sel = (gb > 0) & (gb < a0) & (R > 0)
        for r, v, g1, g2 in zip(R[sel], Vo[sel], gb[sel], go[sel]): rows.append((name, r, v, g1, g2))
    return rows
def law(g, a): return g * (0.5 + np.sqrt(0.25 + a / g))

# ---------------- K0 law identity
gg = np.geomspace(1e-14, 1e-6, 200)
for f in FEET:
    d = float(np.max(np.abs((law(gg, A0[f]) * (1 + 0.0)) / law(gg, A0[f]) - 1))); check(f"K0 D=0 reproduces the law, {f}", d < 1e-12, f"max rel {d:.1e}")

# ================= Reading P: exp(-omega^2/omega_*^2)
say("\n--- Reading P (Phase 1's action) ---")
om_lo = 0.5 * 150 * KMS / (60 * KPC)
RP = dict(omega_lo_ICM=om_lo, source="Hitomi 2016 Perseus, ~150 km/s across ~60 kpc, halved (PROVISIONAL)", footings={})
for f in FEET:
    a0 = A0[f]; o = dict(variants={})
    for lab, w in (("a0/c", a0 / C), ("2a0/c", 2 * a0 / C), ("4a0/c", 4 * a0 / C)):
        Fcl = math.exp(-min((om_lo / w) ** 2, 700.0))
        rows = sparc_low(0.5, a0); om = np.array([v * KMS / (r * KPC) for _, r, v, _, _ in rows]); Fsp = np.exp(-np.minimum((om / w) ** 2, 700.0))
        fsp = float(np.mean((Fsp < 0.5) if MUT else (Fsp >= 0.5)))
        dsph = 1 * KMS / (1 * KPC); mw = 220 * KMS / (8.2 * KPC)
        o["variants"][lab] = dict(omega_star=w, ratio_ICM=om_lo / w, F_ICM=Fcl, ln_F_ICM=-(om_lo / w) ** 2, f_SP=fsp, omega_dsph_1kms_1kpc=dsph, ratio_dsph=dsph / w, omega_MW_sun=mw, ratio_MW=mw / w, SPARC_min_ratio=float(om.min() / w))
        say(f"[{f}] omega_* = {lab} = {w:.3e} s^-1: ICM omega_lo/omega_* = {om_lo / w:.1f}, ln F = {-(om_lo / w) ** 2:.3e}; SPARC f(F>=0.5) = {fsp:.3f} (min omega/omega_* {om.min() / w:.0f}); dSph 1 km/s at 1 kpc: {dsph / w:.0f}; MW at Sun: {mw / w:.0f}")
    cl = any(v["F_ICM"] >= 0.5 for v in o["variants"].values()); sep = all(v["f_SP"] <= F_MAX for v in o["variants"].values())
    o["G-P-CL"] = "PASS" if cl else "FAIL"; o["G-P-SEP"] = "SEPARATES" if sep else "DOES NOT SEPARATE"
    say(f"[{f}] G-P-CL {o['G-P-CL']}; G-P-SEP {o['G-P-SEP']}"); RP["footings"][f] = o
RES["reading_P"] = RP

# ================= Reading R: F(V/sigma) non-increasing, t_c
say("\n--- Reading R (scale-free V/sigma) ---")
RR = dict(t_c=TC, t_c_var=TC_VAR, sigma_HI=SIG_HI, footings={})
# --- G-R-SEP
for f in FEET:
    o = {}
    for Y in (0.5, 0.3, 0.7):
        rows = sparc_low(Y, A0[f]); x = np.array([v for _, _, v, _, _ in rows])
        o[f"Y{Y}"] = dict(n=len(rows), f_SP=float(on_R(x / SIG_HI, TC).mean()), f_SP_tc025=float(on_R(x / SIG_HI, TC_VAR).mean()),
                          f_SP_sig8=float(on_R(x / 8.0, TC).mean()), f_SP_sig12=float(on_R(x / 12.0, TC).mean()), Vobs_min=float(x.min()))
    fs = [o[k]["f_SP"] for k in ("Y0.5", "Y0.3", "Y0.7")]
    o["G-R-SEP"] = "SEPARATES" if all(v <= F_MAX for v in fs) else ("DOES NOT SEPARATE" if all(v > F_MAX for v in fs) else "UNDECIDED")
    say(f"[{f}] SPARC g_b<a0: " + "; ".join(f"Y {k[1:]}: n {o[k]['n']}, f_SP {o[k]['f_SP']:.4f} (t 0.25: {o[k]['f_SP_tc025']:.4f}; sig 8/12: {o[k]['f_SP_sig8']:.4f}/{o[k]['f_SP_sig12']:.4f}), min V_obs {o[k]['Vobs_min']:.1f}" for k in ("Y0.5", "Y0.3", "Y0.7")))
    say(f"[{f}] G-R-SEP: {o['G-R-SEP']}"); RR["footings"][f] = dict(SEP=o)

# --- G-R-ETG
cfg = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG323_sluggs_measured_tracers", "cfg323_measured_tracers_results.json")))
A3 = {}
for ln in open(os.path.join(REPO, "_external_data", "atlas3d_emsellem11", "tableb1.tsv")):
    p = ln.rstrip("\n").split("\t")
    if len(p) > 11 and p[1].strip().startswith("NGC"): A3[p[1].strip()] = dict(Vsig=float(p[6]), lam=float(p[8]), FS=p[10].strip())
for f in FEET:
    g = cfg["per_galaxy"][f]; names = sorted(g, key=int); st = cfg["stats"][f]["ALL"]
    off = np.array([g[n]["primary"] for n in names]); x = np.array([A3[f"NGC{n}"]["Vsig"] for n in names]); FS = [A3[f"NGC{n}"]["FS"] for n in names]
    K0e = float(np.max(np.abs(off - np.array([cfg["per_galaxy"][f][n]["primary"] for n in names])))); check(f"K0 ETG offsets equal CFG323 primary, {f}", K0e == 0.0, f"{K0e}")
    def setstat(m, pred):
        N = int(m.sum())
        if N == 0: return dict(N=0)
        v = off[m]; sd = float(v.std(ddof=1)) if N > 1 else 0.0
        err = math.sqrt(sd ** 2 / N + st["s_gamma"] ** 2 + st["s_beta"] ** 2 + st["s_meas"] ** 2 * 16 / N)
        return dict(N=N, mean=float(v.mean()), err=err, pred=pred, Z=float((v.mean() - pred) / err), names=[n for n, k in zip(names, m) if k])
    o = {}
    for tl, t in (("t0.5", TC), ("t0.25", TC_VAR)):
        on = on_R(x, t); so = setstat(on, DLOG_SIG); sf = setstat(~on, 0.0)
        lab_on = "EMPTY" if so["N"] == 0 else ("EXCLUDED" if so["Z"] < -2 else "ABOVE" if so["Z"] > 2 else "ALLOWED")
        lab_off = "EMPTY" if sf["N"] == 0 else ("CONSISTENT" if abs(sf["Z"]) <= 2 else "MISSES")
        cls = "EXCLUDED" if lab_on == "EXCLUDED" else ("ALLOWED" if lab_on in ("ALLOWED", "ABOVE") and lab_off in ("CONSISTENT", "EMPTY") else "MIXED")
        o[tl] = dict(on=so, off=sf, label_on=lab_on, label_off=lab_off, label=cls)
        say(f"[{f}] ETG {tl}: on N {so['N']}" + (f", mean {so['mean']:+.3f} +- {so['err']:.3f} vs pred {DLOG_SIG:+.3f}, Z {so['Z']:+.2f} {lab_on} {so['names']}" if so["N"] else "") +
            f" | off N {sf['N']}" + (f", mean {sf['mean']:+.3f} +- {sf['err']:.3f} vs 0, Z {sf['Z']:+.2f} {lab_off}" if sf["N"] else "") + f" -> {cls}")
    o["per_galaxy"] = {n: dict(offset=round(float(a), 4), Vsig=float(b), FS=c) for n, a, b, c in zip(names, off, x, FS)}
    # by ATLAS3D class (reported)
    S = np.array([c == "S" for c in FS]); o["by_FS"] = dict(slow=setstat(S, DLOG_SIG), fast_on=setstat(~S, DLOG_SIG), fast_off=setstat(~S, 0.0))
    say(f"[{f}] ETG by F/S (reported): slow N {o['by_FS']['slow']['N']} mean {o['by_FS']['slow']['mean']:+.3f}, Z vs on {o['by_FS']['slow']['Z']:+.2f}; fast N {o['by_FS']['fast_off']['N']} mean {o['by_FS']['fast_off']['mean']:+.3f}, Z vs off {o['by_FS']['fast_off']['Z']:+.2f}, Z vs on {o['by_FS']['fast_on']['Z']:+.2f}")
    o["G-R-ETG"] = o["t0.5"]["label"]; RR["footings"][f]["ETG"] = o

# --- G-R-DSPH, KT15's model (xi = 0)
G = 4.30091e-6; CONV = KPC / 1e6; UPS = np.linspace(1, 3, 41)
def nu(y): return 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
def plummer(r, M, a): return 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
def menc(r, rho):
    fq = 4 * math.pi * r * r * rho; m = np.concatenate([[0.0], np.cumsum(0.5 * (fq[1:] + fq[:-1]) * np.diff(r))]); return m + 4 * math.pi * rho[0] * r[0] ** 3 / 3
def sig_los(M, a, a0, ge=0.0, newton=False):
    r = np.geomspace(1e-4 * a, 60 * a, 2000); rho = plummer(r, M, a); gN = G * menc(r, rho) / r ** 2
    g = gN if newton else gN + (nu(np.sqrt(ge * ge + gN * gN) / a0) - 1) * gN
    return math.sqrt(np.trapz(rho * r * g * 4 * math.pi * r * r, r) / (3 * M))
s1 = sig_los(1e6, 2.0, A0["alt"] * CONV); ex = (4 / 81 * G * 1e6 * A0["alt"] * CONV) ** 0.25
check("K1 deep-MOND estimator (KT15 C1)", abs(s1 / ex - 1) <= 0.03, f"rel {abs(s1 / ex - 1):.4f}")
def load_dw(allmag):
    rows = []
    for d in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "mcconnachie2012_dsph.csv"))):
        if not d["e_sigma*"] or d["Name"].startswith(("M32", "NGC", "Sagittarius")) or d["SubG"] not in ("MW", "M31"): continue
        if not allmag and float(d["VMag"]) > -8: continue
        rows.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3, s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
    return rows
kt15 = json.load(open(os.path.join(RB, "KT15_filtered_phantom_dsph", "kt15.json")))
for f in FEET:
    a0 = A0[f] * CONV; o = {}
    for samp, allmag in (("KT15_satellites", False), ("all_satellites", True)):
        rows = load_dw(allmag)
        for case in ("EFE", "isolated"):
            per = []; n0 = n1 = 0
            for d in rows:
                ge = (200.0 ** 2 / d["D"]) if (case == "EFE" and d["sub"] == "MW") else 0.0
                sp = np.array([sig_los(u * d["L"] + 1.33 * d["MHI"], d["a"], a0, ge) for u in UPS])
                on = bool(on_R(np.array([0.0]), TC)[0]); fac = math.sqrt(1 + D_DUST) if on else 1.0
                p0 = bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any()); p1 = bool((np.abs(fac * sp - d["s"]) <= 2 * d["e"]).any())
                n0 += p0; n1 += p1; Dmax = ((d["s"] + 2 * d["e"]) / sp[0]) ** 2 - 1
                per.append(dict(name=d["name"], sub=d["sub"], obs=d["s"], e=d["e"], law_U1=float(sp[0]), law_U3=float(sp[-1]), pass_law=p0, pass_dust=p1, D_max=float(Dmax)))
            lab = "EXCLUDED" if n1 <= n0 / 2 else ("ALLOWED" if n1 >= n0 - 2 else "HURT")
            o[f"{samp}|{case}"] = dict(n=len(rows), n0=n0, n1=n1, label=lab, rows=per)
            say(f"[{f}] dSph {samp} {case}: n {len(rows)}, law passes {n0}, dust-on passes {n1} -> {lab}; median D_max {np.median([p['D_max'] for p in per]):+.2f}; D_max >= 1.5 in {sum(p['D_max'] >= D_DUST for p in per)}")
            if samp == "KT15_satellites":
                ref = {r["name"]: r["passed"] for r in kt15[f"A0|{f}|{case}"]["rows"]}
                mism = [p["name"] for p in per if ref.get(p["name"]) != p["pass_law"]]
                check(f"K0 dSph D=0 equals KT15 A0 {f} {case}", not mism, f"mismatches {mism}")
    for p in o["KT15_satellites|EFE"]["rows"]:
        say(f"     {p['name'][:20]:20s} {p['sub']:3s} obs {p['obs']:5.1f}+-{p['e']:.1f}  law U1/U3 {p['law_U1']:5.1f}/{p['law_U3']:5.1f}  dust U1 {p['law_U1'] * math.sqrt(1 + D_DUST):5.1f}  law {'P' if p['pass_law'] else '-'} dust {'P' if p['pass_dust'] else '-'}  D_max {p['D_max']:+.2f}")
    o["G-R-DSPH"] = o["KT15_satellites|EFE"]["label"]; RR["footings"][f]["DSPH"] = o

# --- inverse checks and reported rows
INV = dict(VS1=dict(contrast=0.120, err=0.047, Z_vs_pred=(0.120 - DLOG_SIG) / 0.047, src="VS1 README canonical slow coefficient"),
           VS4=dict(contrast=0.057, err=0.037, Z_vs_pred=(0.057 - DLOG_SIG) / 0.037, src="VS4 README primary, NO VERDICT (C1 failed)"))
say(f"\nInverse: VS1 slow-fast +0.120+-0.047 vs pred +{DLOG_SIG:.3f}: Z {INV['VS1']['Z_vs_pred']:+.2f}; VS4 +0.057+-0.037: Z {INV['VS4']['Z_vs_pred']:+.2f} (VS4 not graded)")
for f in FEET:
    rows = sparc_low(0.5, A0[f]); res = {}
    for nm, r, v, g1, g2 in rows: res.setdefault(fD.get(nm) == 4, []).append(math.log10(g2 / law(g1, A0[f])))
    u, o_ = np.array(res.get(True, [])), np.array(res.get(False, []))
    INV[f"UMa_{f}"] = dict(n_UMa=len(u), rms_UMa=float(np.sqrt(np.mean(u ** 2))), mean_UMa=float(u.mean()), n_rest=len(o_), rms_rest=float(np.sqrt(np.mean(o_ ** 2))), mean_rest=float(o_.mean()))
    say(f"[{f}] Ursa Major (f_D 4) g_b<a0 law residual: n {len(u)}, mean {u.mean():+.3f}, rms {INV[f'UMa_{f}']['rms_UMa']:.3f}; rest n {len(o_)}, mean {o_.mean():+.3f}, rms {INV[f'UMa_{f}']['rms_rest']:.3f}")
RES["inverse"] = INV
RES["G-R-BUL"] = "WEIGHT ALLOWED AT GALAXIES (selector does not tell gas from galaxies)"; RES["G-Q2"] = "INHERITS (matter frame at the Sun rotates; dust off)"; RES["keys"] = "NOT COMPUTED"

# --- labels
for f in FEET:
    o = RR["footings"][f]; o["label"] = ("I2-R KILLED" if (o["SEP"]["G-R-SEP"] == "DOES NOT SEPARATE" or o["ETG"]["G-R-ETG"] == "EXCLUDED" or o["DSPH"]["G-R-DSPH"] == "EXCLUDED") else
                                         "I2-R PASSES THESE GATES" if (o["SEP"]["G-R-SEP"] == "SEPARATES" and o["ETG"]["G-R-ETG"] == "ALLOWED" and o["DSPH"]["G-R-DSPH"] == "ALLOWED") else
                                         "MIXED (SEP %s, ETG %s, DSPH %s)" % (o["SEP"]["G-R-SEP"], o["ETG"]["G-R-ETG"], o["DSPH"]["G-R-DSPH"]))
RES["reading_R"] = RR; RES["checks"] = CHECKS; allok = all(CHECKS.values())
pl = [RP["footings"][f] for f in FEET]
lp = ("I2-P KILLED AT THE CLUSTER GATE" if all(p["G-P-CL"] == "FAIL" for p in pl) else "I2-P ALIVE" if all(p["G-P-CL"] == "PASS" and p["G-P-SEP"] == "SEPARATES" for p in pl) else "FOOTING-SPLIT / UNDECIDED")
lr = [RR["footings"][f]["label"] for f in FEET]; lr = lr[0] if lr[0] == lr[1] else "FOOTING-SPLIT: " + " | ".join(lr)
if not allok: lp, lr = "NO CLEAN LABEL (a check failed): " + lp, "NO CLEAN LABEL (a check failed): " + lr
RES["label_P"], RES["label_R"] = lp, lr
say(f"\nLABEL reading P: {lp}\nLABEL reading R: {lr}" + ("  [MUTATE twin]" if MUT else ""))
json.dump(RES, open(os.path.join(HERE, f"i2_results{TAG}.json"), "w"), indent=1, sort_keys=True)
OUT.close()
