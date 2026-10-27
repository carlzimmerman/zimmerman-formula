"""CFG408: X43 re-scored with MEASURED stellar fractions instead of f* = 0.20 (KiDS cluster keys via X43 child runs; X-COP via CFG407's machinery).
Criteria: FROZEN_CRITERIA.md (34cb560b1d). One injection in X30's prep: Mb = Mg*(1 + 0.20) -> Mb = Mg*(1 + __FS__[i]).
Run:  nice python3 cfg408_measured_fstar.py            -> KiDS children ID/FTERC/FUP/FCLUSTER/FFROZEN/FXCOP + X-COP part
      MUTATE=1 nice python3 cfg408_measured_fstar.py   -> f* = 0.60 everywhere (KiDS G-OUT-M3 pred must rise, X-COP Delta must fall; rc 1)
      python3 cfg408_measured_fstar.py --x43 TAG       -> internal: one X43 run reading cfg408_fstar_TAG.json
Single thread. kappa = 1/2 FITTED; not theory closed."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json, time, io, contextlib, subprocess, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
REB = os.path.join(REPO, "rebuild_2026_10_22"); X43SRC = os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")
XC = os.path.join(REPO, "real_research", "data", "xcop")
INJ_OLD, INJ_NEW = 'Mb = Mg*(1 + 0.20)', 'Mb = Mg*(1 + __FS__[i])'

def x43_source(tag):
    src = open(X43SRC).read()
    reps = [('HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)', f'HERE = {HERE!r}; REB = {REB!r}'),
            ('TAG = "_MUTATE" if MUTATE else ""', f'TAG = {"_" + tag!r}'),
            ('NX = {"__file__": X30SRC, "__name__": "x30_ro"}; sys.argv = [X30SRC]',
             f'assert codeX.count({INJ_OLD!r}) == 1; codeX = codeX.replace({INJ_OLD!r}, {INJ_NEW!r}); '
             'NX = {"__file__": X30SRC, "__name__": "x30_ro", "__FS__": __FS__}; sys.argv = [X30SRC]')]
    for o, n in reps:
        assert src.count(o) == 1, o
        src = src.replace(o, n)
    return src

# =============================================================== KiDS child: one X43 run with per-cluster f*
if "--x43" in sys.argv:
    tag = sys.argv[sys.argv.index("--x43") + 1]
    FS = np.array(json.load(open(os.path.join(HERE, f"cfg408_fstar_{tag}.json")))["fstar"], float)
    G = {"__file__": X43SRC, "__name__": "x43_cfg408", "__FS__": FS}; sys.argv = [X43SRC]; rc = 0
    try: exec(compile(x43_source(tag), X43SRC, "exec"), G)
    except SystemExit as e: rc = e.code
    NX = G["NX"]; arr = {"T3M": np.asarray(NX["T3M"]), "I": np.asarray(NX["I"]), "TID": np.asarray(NX["TID"])}
    for (f, hk), c in NX["MEAS"].items(): arr[f"d__{f}__{hk}"] = np.asarray(c["d"])
    np.savez(os.path.join(HERE, f"cfg408_x43_{tag}_arrays.npz"), **arr)
    json.dump({"tag": tag, "x43_rc": rc, "M": NX["M"]}, open(os.path.join(HERE, f"cfg408_x43_{tag}_meas.json"), "w"), default=float)
    sys.exit(0)

MUT = os.environ.get("MUTATE") == "1"; os.environ.pop("MUTATE", None)
OUT, CONTROLS = [], []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def K(name, ok, val, part): CONTROLS.append({"name": name, "pass": bool(ok), "value": val, "part": part}); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")
T0 = time.time()
P("CFG408 X43 with measured stellar fractions (KiDS keys + X-COP)" + ("  [MUTATE: f* = 0.60]" if MUT else "")); P("=" * 110)

# =============================================================== f* inputs: CFG922 census (A1 primary, frozen reported) -> X7/X30's 326 clusters
D922 = os.path.join(LANES, "CFG922_cluster_core_baryon_recheck")
CA1 = json.load(open(os.path.join(D922, "cfg922_census_A1.json"))); CFR = json.load(open(os.path.join(D922, "cfg922_census.json")))
def ratios(C, k): return np.array([c[k] / c["gas_cyl"] for c in C["eRASS1"]], float)
cov = np.array([c["coverage"] for c in CA1["eRASS1"]], float); meas = cov >= 0.5
rc_, ru_ = ratios(CA1, "S_cen"), ratios(CA1, "S_up")
k2a = (f"{np.median(rc_[meas]):.4f}", f"{np.percentile(ru_[meas], 84):.4f}", int((~meas).sum()))
d687 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
X7 = np.load(os.path.join(REB, "X7_cluster_core_significance", "x7_measure_percluster.npz"), allow_pickle=True)
Mgl = np.asarray(X7["Mgas500"], float); T3M = np.digitize(Mgl, np.quantile(Mgl, [1 / 3, 2 / 3])); N7 = len(Mgl)   # X30's line 91 verbatim
match = np.full(N7, -1)
for i in range(N7):
    d2 = ((d687["ra"] - X7["ra"][i]) * np.cos(np.radians(X7["dec"][i]))) ** 2 + (d687["dec"] - X7["dec"][i]) ** 2
    j = int(np.argmin(d2))
    if math.sqrt(d2[j]) * 3600 <= 30: match[i] = j
nm = int((match >= 0).sum())
P("\nCONTROLS (inputs)")
K("K2 census read: A1 ratio_cen_median 0.0340, ratio_up_84 0.2165, n_not_measured 33; >= 300/326 X7 clusters matched within 30\"",
  k2a == ("0.0340", "0.2165", 33) and nm >= 300, f"{k2a}; matched {nm}/{N7}; unmatched X7 idx {np.where(match < 0)[0].tolist()}", "KiDS")
def terc_fill(per):                                  # per-cluster values on matched X7 clusters -> tercile medians (T3M on observed Mgas500)
    med = [float(np.median(per[(match >= 0) & (T3M == t)])) for t in range(3)]
    return np.array([med[T3M[i]] for i in range(N7)]), med
def on_x7(r): return np.array([r[match[i]] if match[i] >= 0 else np.nan for i in range(N7)])
FTERC, medT = terc_fill(on_x7(rc_)); FUP, medU = terc_fill(on_x7(ru_)); FFROZ, medF = terc_fill(on_x7(ratios(CFR, "S_cen")))
pc = on_x7(rc_); FCL = np.where(np.isfinite(pc), pc, FTERC)
P(f"  tercile medians of f* (light / middle / heavy observed Mgas500): A1 central {' / '.join(f'{x:.4f}' for x in medT)}; "
  f"A1 upper {' / '.join(f'{x:.4f}' for x in medU)}; frozen central {' / '.join(f'{x:.4f}' for x in medF)}")

# X-COP f* (7 measured at q = 1 for K4; per-h-cell q applied later)
from astropy.io import fits
J5 = json.load(open(os.path.join(XC, "xcop_r500_ettori2019.json"))); NAMES = sorted(n for n in J5 if os.path.isdir(os.path.join(XC, n)))
def lli(x, xp, fp): return float(np.exp(np.interp(math.log(x), np.log(xp), np.log(fp))))
XD = {}
for n in NAMES:
    hm = fits.open(os.path.join(XC, n, f"{n}_hydro_mass.fits"))[1].data; fg = fits.open(os.path.join(XC, n, f"{n}_fgas_profile.fits"))[1].data
    msf = os.path.join(XC, n, f"{n}_mstar.fits"); ms = fits.open(msf)[2].data if os.path.exists(msf) else None
    XD[n] = dict(z=J5[n]["z"], R500=J5[n]["R500"], R200=J5[n]["R200"], M500=J5[n]["M500"], r_h=np.array(hm["RADIUS"], float) / 1e3,
                 M_f=np.array(hm["M_FORW"], float), x_g=np.array(fg["RADIUS"], float), M_g=np.array(fg["MGAS"], float),
                 r_s=None if ms is None else np.array(ms["RADIUS"], float) / 1e3, M_s=None if ms is None else np.array(ms["MSTAR"], float))
STARS7 = [n for n in NAMES if XD[n]["M_s"] is not None]
f7 = {n: lli(XD[n]["R500"], XD[n]["r_s"], XD[n]["M_s"]) / lli(1.0, XD[n]["x_g"], XD[n]["M_g"]) for n in STARS7}
ref4 = dict(A85=0.035, A644=0.071, A1795=0.062, A2029=0.074, A2142=0.065, A2319=0.048, ZW1215=0.053)
K("K4 X-COP f* re-read (q = 1, 3 decimals) equals CFG407's post-hoc printout", all(round(f7[n], 3) == ref4[n] for n in ref4),
  ", ".join(f"{n} {f7[n]:.3f}" for n in STARS7), "X-COP")
F7MED = float(np.median(list(f7.values()))); P(f"  X-COP-7 median f* = {F7MED:.4f} (fallback for {', '.join(n for n in NAMES if n not in STARS7)}; F-XCOP constant)")

VAR = {"ID": np.full(N7, 0.20)}
if MUT: VAR["MUT"] = np.full(N7, 0.60)
else: VAR.update({"FTERC": FTERC, "FUP": FUP, "FCLUSTER": FCL, "FFROZEN": FFROZ, "FXCOP": np.full(N7, F7MED)})
for tag, fs in VAR.items():
    json.dump({"tag": tag, "fstar": fs.tolist()}, open(os.path.join(HERE, f"cfg408_fstar_{tag}.json"), "w"))

# =============================================================== KiDS part: X43 children
P("\nKIDS PART: X43 child runs (one injection in X30's prep)")
env = dict(os.environ, PYTHONHASHSEED="0")
for tag in VAR:
    t1 = time.time()
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--x43", tag], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    P(f"  child {tag}: rc {r.returncode} [{time.time() - t1:.0f} s]" + (f"  stderr tail: {r.stderr.strip()[-300:]}" if r.returncode else ""))
RX = {t: json.load(open(os.path.join(HERE, f"x43_collapse_core_results_{t}.json"))) for t in VAR}
MX = {t: json.load(open(os.path.join(HERE, f"cfg408_x43_{t}_meas.json"))) for t in VAR}
AX = {t: np.load(os.path.join(HERE, f"cfg408_x43_{t}_arrays.npz")) for t in VAR}
REF = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
FEET, HKS, BN = ("canonical", "alt"), ("h0672", "h0686"), ("INNER", "MID", "OUTER")
dev1 = max(abs(RX["ID"]["footings"][f]["clusters"]["cells"][hk][k][fld] - c[fld]) for f in FEET for hk in HKS
           for k, c in REF["footings"][f]["clusters"]["cells"][hk].items() for fld in ("meas", "s", "pred", "Z"))
K("K1 KiDS identity: f* = 0.20 through the injection reproduces every committed X43 cluster cell (<= 1e-9)", dev1 <= 1e-9, f"max |diff| {dev1:.2e}", "KiDS")
K("T3M identity: the child's X30 tercile assignment equals the one used to build f*", bool(np.array_equal(AX["ID"]["T3M"], T3M)), "", "KiDS")
TM = AX["ID"]["T3M"]; I = AX["ID"]["I"]; TID = AX["ID"]["TID"]
def R_of(t, f, hk, sel, bi): return float(AX["ID"][f"d__{f}__{hk}"][sel, bi].sum() / AX[t][f"d__{f}__{hk}"][sel, bi].sum())
k5t = "MUT" if MUT else "FTERC"; devA = devS = 0.0
for f in FEET:
    for hk in HKS:
        cl = f"{f}|{hk}"
        for b in BN:
            bi = BN.index(b)
            for t in range(3):
                for key, sel in ((f"KT_terc|{b}", I[TID == t]), (f"M_terc|{b}", np.where(TM == t)[0])):
                    Rr = R_of(k5t, f, hk, sel, bi); o0, o1 = MX["ID"]["M"][cl][key][t], MX[k5t]["M"][cl][key][t]
                    devA = max(devA, abs(o1["A"] / (o0["A"] * Rr) - 1)); devS = max(devS, abs(o1["s"] / (o0["s"] * Rr) - 1))
k5 = devA <= 1e-6 and devS <= 1e-6
K(f"K5 stored-X7 rescale exactness ({k5t} vs ID; in-run KT/M_terc A and s = ID x R to 1e-6); failure marks G-OUT-M* APPROXIMATE", k5,
  f"max rel dev A {devA:.2e}, s {devS:.2e}", "K5")
X7KEYS = {"G-OUT-Mall": None, "G-OUT-M1": 0, "G-OUT-M2": 1, "G-OUT-M3": 2}
def grade(t):
    out = {}
    for f in FEET:
        cells = {hk: {} for hk in HKS}
        for hk in HKS:
            for k, c in RX[t]["footings"][f]["clusters"]["cells"][hk].items():
                meas_, s, pred = c["meas"], c["s"], c["pred"]
                if k in X7KEYS and t != "ID":
                    tt = X7KEYS[k]; sel = np.arange(len(TM)) if tt is None else np.where(TM == tt)[0]
                    Rr = R_of(t, f, hk, sel, 2); meas_, s = meas_ * Rr, s * Rr
                cells[hk][k] = dict(meas=meas_, s=s, pred=pred, Z=(meas_ - pred) / s)
        keys = list(cells["h0672"]); fails = [k for k in keys if not all(abs(cells[hk][k]["Z"]) <= 2 for hk in HKS)]
        out[f] = dict(cells=cells, fails=fails, sign={k: ("OVER" if cells["h0672"][k]["pred"] > cells["h0672"][k]["meas"] else "UNDER") for k in fails},
                      groups_Z=RX[t]["footings"][f]["groups"]["Z"])
    return out
GB = {t: grade(t) for t in VAR}
refF = {f: sorted(x.split(" ")[0] for x in REF["footings"][f]["clusters"]["fails"]) for f in FEET}
for t in VAR:
    for f in FEET:
        g = GB[t][f]
        P(f"  {t:8s} {f:9s}: fails {[k + ' (' + g['sign'][k] + ')' for k in g['fails']] or 'none'} | groups Z {g['groups_Z']:+.2f} (out of scope)")
        if f == "canonical":
            for k in g["cells"]["h0672"]:
                c0, c1 = g["cells"]["h0672"][k], g["cells"]["h0686"][k]
                P(f"       {k:10s} h0672 meas {c0['meas']:+.3f}+-{c0['s']:.3f} pred {c0['pred']:+.3f} Z {c0['Z']:+.2f} | h0686 Z {c1['Z']:+.2f}"
                  + ("  FAIL" if k in g["fails"] else "") + ("  [APPROX]" if (k in X7KEYS and t != "ID" and not k5) else ""))

# =============================================================== X-COP part (CFG407 machinery with own f*)
P("\nX-COP PART (CFG407's statistic over [R500, R200]; X43 recipe gas 'P'; M_b = Mg_P (1 + f*))")
src = x43_source("XCOPHEAD"); cut = "\nfor f in FEET:\n"; assert src.count(cut) == 1
G = {"__file__": X43SRC, "__name__": "x43_cfg408_head", "__FS__": np.full(N7, 0.20)}; argv0 = sys.argv; sys.argv = [X43SRC]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(cut)], X43SRC, "exec"), G)
sys.argv = argv0
NX = G["NX"]; sig_core, solve_r0, B, MSUNE = (G[k] for k in ("sig_core", "solve_r0", "B", "MSUNE"))
gas, r_ta_com, RG, RM, MSUN, DM, DA_lcdm, HV = (NX[k] for k in ("gas", "r_ta_com", "RG", "RM", "MSUN", "DM", "DA_lcdm", "HV"))
L1 = dict(Om=0.2976016, h=0.6856427, wb=0.0223081); OBn = L1["wb"] / L1["h"] ** 2; RATIO_N = (L1["Om"] - OBn) / OBn
G946, MPC946 = 6.67430e-11, 3.0856775814913673e22; RHOMn = L1["Om"] * 3 * (L1["h"] * 100e3 / MPC946) ** 2 / (8 * math.pi * G946)
def r_ta_nat(Mb_kg): return (3 * (L1["Om"] / OBn) * Mb_kg / (4 * math.pi * NX["DTA"] * RHOMn)) ** (1 / 3)
def qof(n, hk): z = XD[n]["z"]; return (float(DM(z, HV[hk])) / (1 + z)) / DA_lcdm(z)
def fstar_x(n, hk, mode):
    if mode == "ID": return 0.20
    if mode == "MUT": return 0.60
    return (f7[n] if n in f7 else F7MED) * qof(n, hk) ** -0.5
def predict(n, foot, hk, mode, native=False, prof=False):
    d = XD[n]; z = d["z"]; q = qof(n, hk); R500 = d["R500"] * q; Mg500 = lli(1.0, d["x_g"], d["M_g"]) * q ** 2.5
    Mg, _ = gas(Mg500, R500, "P")
    if prof and d["M_s"] is not None:
        rs = d["r_s"] * q; msv = d["M_s"] * q ** 2 * MSUN; sl = rs[-1]
        Ms = np.exp(np.interp(np.log(RG), np.log(rs), np.log(msv))); Ms[RG < rs[0]] = msv[0] * (RG[RG < rs[0]] / rs[0]) ** 3
        Ms[RG > sl] = msv[-1] * Mg[RG > sl] / float(np.interp(sl, RG, Mg)); Mb = Mg + Ms
    else:
        Mb = Mg * (1 + fstar_x(n, hk, mode))
    Mbt = float(Mb[-1])
    rta, Mfair, tag = (r_ta_nat(Mbt) / (1 + z), RATIO_N * Mbt, "B_cfg886_bg") if native else (r_ta_com(Mbt) / (1 + z), 5.364 * Mbt, "A_c2b_refit")
    Mtot = (Mfair + Mbt) / MSUNE; s, _ = sig_core(foot, tag, Mtot); r0 = solve_r0(Mfair, rta, s)
    return (Mb + math.pi * s * r0 ** 2 * B(np.minimum(RM, rta) / r0)) / MSUN
def deltas(mode, b, names=None, native=False, prof=False):
    res = {}; names = NAMES if names is None else names
    for foot in FEET:
        for hk in HKS:
            Di = []
            for n in names:
                d = XD[n]; q = qof(n, hk); rk = d["R500"] * q * (d["R200"] / d["R500"]) ** (np.arange(5) / 4)
                Mx = predict(n, foot, hk, mode, native, prof); Mh = np.array([lli(r / q, d["r_h"], d["M_f"]) * q for r in rk])
                Mp = np.exp(np.interp(np.log(rk), np.log(RG), np.log(Mx))); Di.append(float(np.log10(Mh / (1 - b) / Mp).mean()))
            Di = np.array(Di); m, se = float(Di.mean()), float(Di.std(ddof=1) / math.sqrt(len(Di)))
            res[f"{foot}|{hk}"] = dict(mean=m, se=se, Z=m / se, Di=dict(zip(names, Di.tolist())), N=len(names))
    return res
c407 = json.load(open(os.path.join(LANES, "CFG407_xcop_outer_mass_x43", "cfg407_results.json")))["results"]["PRIMARY"]["0.0"]
xid = deltas("ID", 0.0)
k3 = max(abs(xid[c]["mean"] - c407[c]["mean"]) for c in xid)
K("K3 X-COP identity: f* = 0.20 reproduces CFG407's PRIMARY Delta (b = 0) in all four cells (<= 1e-9)", k3 <= 1e-9, f"max |diff| {k3:.1e}", "X-COP")
def classify(r0_, r3_):
    cls = {c: ("EXCESS CONFIRMED" if r0_[c]["mean"] >= 2 * r0_[c]["se"] else ("X43 OVERPREDICTS" if r3_[c]["mean"] <= -2 * r3_[c]["se"] else "CONSISTENT")) for c in r0_}
    u = set(cls.values()); return (u.pop() if len(u) == 1 else "MIXED"), cls

if MUT:
    xm = deltas("MUT", 0.0)
    okK = all(GB["MUT"][f]["cells"]["h0672"]["G-OUT-M3"]["pred"] > GB["ID"][f]["cells"]["h0672"]["G-OUT-M3"]["pred"] for f in FEET)
    okX = all(xm[c]["mean"] < xid[c]["mean"] for c in xm)
    K("MUTATE f* = 0.60: KiDS G-OUT-M3 pred rises (both footings) and X-COP Delta falls (all cells)", okK and okX,
      {"M3 pred ID->MUT": {f: (round(GB['ID'][f]['cells']['h0672']['G-OUT-M3']['pred'], 4), round(GB['MUT'][f]['cells']['h0672']['G-OUT-M3']['pred'], 4)) for f in FEET},
       "X-COP Delta ID->MUT": {c: (round(xid[c]['mean'], 4), round(xm[c]['mean'], 4)) for c in xm}}, "MUT")
    json.dump({"lane": "CFG408", "mutate": True, "controls": CONTROLS}, open(os.path.join(HERE, "cfg408_results_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg408_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1)

XR = {"X-PRIMARY": {b: deltas("F", b) for b in (0.0, 0.3)}, "X-7": {b: deltas("F", b, names=STARS7) for b in (0.0, 0.3)},
      "X-PROF": {b: deltas("F", b, names=STARS7, prof=True) for b in (0.0, 0.3)}, "X-NAT": {b: deltas("F", b, native=True) for b in (0.0, 0.3)}}
XS = {}
for v, rv in XR.items():
    ov, cls = classify(rv[0.0], rv[0.3]); XS[v] = dict(overall=ov, cells=cls)
    P(f"  {v}: {ov}")
    for c in rv[0.0]:
        a, b3 = rv[0.0][c], rv[0.3][c]
        P(f"    {c:16s} b=0: {a['mean']:+.3f} +- {a['se']:.3f} (Z {a['Z']:+.2f}, N {a['N']}) | b=0.3: {b3['mean']:+.3f} +- {b3['se']:.3f} -> {cls[c]}")
P("  per cluster Delta_i (X-PRIMARY, canonical|h0672, b = 0): " + ", ".join(f"{n} {v:+.3f}" for n, v in XR["X-PRIMARY"][0.0]["canonical|h0672"]["Di"].items()))

# =============================================================== readings
validK = all(c["pass"] for c in CONTROLS if c["part"] == "KiDS"); validX = all(c["pass"] for c in CONTROLS if c["part"] == "X-COP")
def readK(f):
    new, ref = set(GB["FTERC"][f]["fails"]), set(refF[f])
    return "X43 GAINS" if new < ref else ("X43 HOLDS" if new == ref else "X43 LOSES (new: " + ", ".join(f"{k} ({GB['FTERC'][f]['sign'][k]})" for k in sorted(new - ref)) + ")")
RK = {f: (readK(f) if validK else "INVALID") for f in FEET}
RXc = XS["X-PRIMARY"]["overall"] if validX else "INVALID"
m3u = all(("G-OUT-M3" in GB["FTERC"][f]["fails"]) and GB["FTERC"][f]["sign"].get("G-OUT-M3") == "UNDER" for f in FEET)
m3any = any("G-OUT-M3" in GB["FTERC"][f]["fails"] for f in FEET)
if not (validK and validX): comb = "INVALID"
elif RXc == "X43 OVERPREDICTS" and m3u: comb = "CONTRADICTORY"
elif m3u and RXc == "EXCESS CONFIRMED": comb = "BOTH CONFIRM UNDER-SUPPLY"
elif m3u: comb = "KIDS ONLY"
elif not m3any and RXc == "EXCESS CONFIRMED": comb = "X-COP ONLY"
elif not m3any: comb = "NEITHER"
else: comb = "UNRESOLVED (G-OUT-M3 fails on one footing only)"
P(f"\nREADING (frozen): KiDS [F-TERC] canonical {RK['canonical']} | alt {RK['alt']}; X-COP [X-PRIMARY] {RXc}; COMBINED: {comb}")
P(f"  reported KiDS variants: " + "; ".join(f"{t} fails {GB[t]['canonical']['fails']}" for t in VAR if t not in ("ID", "FTERC")))
P(f"controls {sum(c['pass'] for c in CONTROLS)}/{len(CONTROLS)} (K5 only marks keys APPROXIMATE); runtime {time.time() - T0:.0f} s")
json.dump({"lane": "CFG408", "mutate": False, "controls": CONTROLS, "fstar": {"tercile_A1_central": medT, "tercile_A1_upper": medU, "tercile_frozen": medF,
           "xcop7": f7, "xcop7_median": F7MED, "matched": nm}, "kids": {"grades": GB, "reading": RK, "ref_fails": refF, "K5_dev": [devA, devS]},
           "xcop": {"results": {v: {str(b): r for b, r in rv.items()} for v, rv in XR.items()}, "summary": XS, "reading": RXc}, "combined": comb},
          open(os.path.join(HERE, "cfg408_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg408.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (validK and validX) else 2)
