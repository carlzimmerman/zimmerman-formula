#!/usr/bin/env python3
"""QX26 (criteria c2cbd5086d / origin 44b5658218): does stellar IMF variation (Posacki+2015 alpha(sigma_e)) explain the
hot/early-type step?   python3 qx26.py [--mutate]   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "qx26_MUTATE" if MUT else "qx26"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- frozen relation and inputs
A_SL, A_IC = 0.38, -0.06                      # Posacki+2015: log alpha = 0.38 log(sigma_e/200) - 0.06, alpha vs Salpeter-pop
K_TO_S = 1 / 0.63                             # Salpeter / (Kroupa or Chabrier) mass ratio (Madau & Dickinson 2014)
def alpha(se): return 10 ** (A_SL * math.log10(se / 200.0) + A_IC)
def fK(se):    return max(alpha(se) * K_TO_S, 1.0)   # IMF mass factor relative to Kroupa/Chabrier, floored at 1 (bulges/groups)
SIG0 = dict(NGC720=239, NGC1407=271, NGC4125=226, NGC4261=309, NGC4472=282, NGC4649=331, NGC6482=302)
AP = 0.87
KIDS_SIG = (130, 170, 210); XCOP_SIG = (250, 300, 350); GRP_SIG = (200, 250, 300); BUL_SIG = (100, 150, 200)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G, MS, KPC = 6.674e-11, 1.989e30, 3.0857e19
def glaw(gN, a0): return 0.5 * gN + math.sqrt(0.25 * gN ** 2 + a0 * gN)
AX2 = 2.0 if MUT else 1.0                     # MUTATE: planted alpha x 2 (ellipticals)

# ---------------------------------------------------------------- (1) X-ray ellipticals (QX18 model, explicit factory)
DATA = os.path.join(REPO, "real_research", "data")
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv")) if not l.startswith("#")]
hdr, rows = rows[0], rows[1:]
def make(d):
    LK = float(d["LK_1e11"]) * 1e11; Re = float(d["Re_kpc"]); Mv = float(d["Mvir_1e12"]) * 1e12
    Rv = float(d["Rvir_kpc"]); c = float(d["c"]); a = Re / 1.8153; rs = Rv / c
    Mfit = float(d["ups_fit"]) * LK; Mh = Mv - Mfit; mc = math.log(1 + c) - c / (1 + c)
    def Mobs(r): return Mh * (math.log(1 + r / rs) - (r / rs) / (1 + r / rs)) / mc + Mfit * r ** 2 / (r + a) ** 2
    def Mst(r, ups): return ups * LK * r ** 2 / (r + a) ** 2
    return dict(name=d["name"], LK=LK, Re=Re, Mobs=Mobs, Mst=Mst, uk=float(d["ups_krou"]), us=float(d["ups_salp"]))
GAL = [make(dict(zip(hdr, r))) for r in rows]
def Mlaw(Mb, r_kpc, a0):
    r = r_kpc * KPC; gN = G * Mb * MS / r ** 2; return glaw(gN, a0) * r ** 2 / G / MS
def ell_D(a0, mode, sscale=1.0):
    per = {}
    for g in GAL:
        if mode == "kroupa": ups = g["uk"]
        else: ups = AX2 * alpha(AP * SIG0[g["name"]] * sscale) * g["us"]
        per[g["name"]] = float(np.mean([math.log10(g["Mobs"](m * g["Re"]) / Mlaw(g["Mst"](m * g["Re"], ups), m * g["Re"], a0)) for m in (2, 4, 8)]))
    return float(np.mean(list(per.values()))), per

def lab(F, line_ok):
    if F >= 0.8 and line_ok: return "STEP EXPLAINED BY IMF"
    if F >= 0.2: return "PARTLY"
    return "NOT"

RES = dict(tag=TAG, criteria="c2cbd5086d", relation="Posacki+2015 log a = 0.38 log(se/200) - 0.06", note="kappa = 1/2 FITTED; not theory closed", foot={})
P(f"QX26 {'MUTATE (alpha x2 on ellipticals)' if MUT else 'MAIN'}: IMF variation vs the hot/early-type step. kappa = 1/2 FITTED; not theory closed.")
P(f"alpha(sigma_e): 100 {alpha(100):.3f}, 150 {alpha(150):.3f}, 200 {alpha(200):.3f}, 250 {alpha(250):.3f}, 300 {alpha(300):.3f} (vs Salpeter); "
  f"factor vs Kroupa: {', '.join(f'{s} {alpha(s)*K_TO_S:.3f}' for s in (100,150,200,250,300))}")

# ---------------------------------------------------------------- (2) KiDS (QX21 T1 data, verbatim logic)
B21 = os.path.join(DATA, "lensing_rar", "brouwer2021_rar")
d0 = [np.loadtxt(os.path.join(B21, f"Fig-8_RAR-KiDS-isolated_Colorbin_{i}.txt")) for i in (1, 2)]
gb = d0[0][:, 0]; Lk = d0[0][:, 1] / d0[0][:, 4]; Ek = d0[1][:, 1] / d0[1][:, 4]
cv = np.loadtxt(os.path.join(B21, "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt"))
C30 = (cv[:, 4] / cv[:, 6]).reshape(2, 2, 15, 15).transpose(0, 2, 1, 3).reshape(30, 30)
K1 = np.arange(8, 15)
def dstat(Lv, Ev):
    n = len(K1); J = np.zeros((n, 30))
    for k, i in enumerate(K1): J[k, i] = -1.0 / Lv[i]; J[k, 15 + i] = 1.0 / Ev[i]
    Cd = J @ C30 @ J.T / np.log(10) ** 2; dv = np.log10(Ev[K1] / Lv[K1]); w = np.linalg.solve(Cd, np.ones(n))
    return float(w @ dv / w.sum()), float(1 / np.sqrt(w.sum()))
Dk, sk = dstat(Lk, Ek)
txt = open(os.path.join(REPO, "campaign_fresh_gravity", "CFG61_kids_colour_split.out")).read()
rr = re.findall(r"K1 g_bar ([0-9.e+-]+): R_med late [0-9.]+ early [0-9.]+ Mpc \| late +([0-9.]+) \(L +([0-9.]+), S +[0-9.]+\) \| early +([0-9.]+) \(L +([0-9.]+), S", txt)
assert len(rr) == 7
D_law = float(np.mean(np.log10(np.array([float(r[4]) for r in rr]) / np.array([float(r[2]) for r in rr]))))
DX = Dk - D_law; S_TOT = 0.064
def slope(g, a0, h=1e-4): return (math.log(glaw(g * (1 + h), a0)) - math.log(glaw(g * (1 - h), a0))) / (math.log(1 + h) - math.log(1 - h))

# ---------------------------------------------------------------- (4) X-COP + groups (QX20 points via QX5 loaders, read-only)
src = open(os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py")).read(); cut = src.index("XC, SP, EL, LE, GR = ")
NS = {"__file__": os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py"), "__name__": "qx5_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:cut], "qx5_lib", "exec"), NS); sys.argv = _a
XC, GR = NS["xcop"](), NS["groups"]()
def hot_means(a0, fx, fg, fst=0.5):
    x = []
    for z in XC:
        Ms_ = z["M_b"] - z["M_gas"]; Mb = z["M_gas"] + fx * Ms_
        x.append(math.log10(z["M_obs"] / Mlaw(Mb, z["r_kpc"], a0)))
    g = []
    for gp in GR:
        for p in gp["pts"]:
            Mb = p["M_gas"] * (1 + fg * fst); g.append(math.log10(p["M_obs"] / Mlaw(Mb, p["r_kpc"], a0)))
    return float(np.mean(x)), float(np.mean(g))

# ---------------------------------------------------------------- (3) SPARC bulges (QX8 algebraic grader, read-only import)
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field"))
_a = sys.argv; sys.argv = [sys.argv[0]]
import qx8 as Q8                                                    # noqa: E402
sys.argv = _a
SPG = Q8.load_sparc()
def sparc_grade(a0, fb):
    rows_ = []
    for q in SPG:
        R = q["R"] * Q8.KPC_S
        VB2 = np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + Q8.UPS[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * fb * Q8.UPS[None, :] * q["Vbul"][:, None] ** 2
        GB = VB2 * 1e6 / R[:, None]
        OK = (GB > 0) & (q["GO"] > 0)[:, None] & np.isfinite(GB) & (q["Vobs"] > 0)[:, None]
        qq = dict(q, GB=GB, OK=OK)
        lgp = np.log10(np.maximum(Q8.nu(np.where(OK, GB, 1.0) / a0) * np.where(OK, GB, 1.0), 1e-300))
        rows_.append(Q8.fit_one(qq, lgp))
    st = Q8.pooled(rows_); st["line"] = Q8.line(st); return st

# ---------------------------------------------------------------- grade
P4 = {"canonical": (0.054087, 0.52), "alt": (0.053718, 0.44)}
QX18 = {"canonical": 0.210, "alt": 0.189}
QX20 = {"canonical": dict(X=0.467499, G=0.263752), "alt": dict(X=0.434523, G=0.225997)}
okm = True
for f, a0 in A0.items():
    o = {}
    DKr, _ = ell_D(a0, "kroupa"); DI, per = ell_D(a0, "imf")
    Dlo, _ = ell_D(a0, "imf", 0.9); Dhi, _ = ell_D(a0, "imf", 1.1)
    FE = (DKr - DI) / DKr
    labs = {lab((DKr - x) / DKr, abs(x) <= 0.15) for x in (DI, Dlo, Dhi)}
    lE = lab(FE, abs(DI) <= 0.15); lE_tag = lE if len(labs) == 1 else lE + " [BRACKET-DEPENDENT]"
    o["ellipticals"] = dict(D_kroupa=DKr, D_imf=DI, D_sig_x09=Dlo, D_sig_x11=Dhi, F=FE, line_ok=abs(DI) <= 0.15, label=lE_tag, per_galaxy=per,
                            factor_vs_kroupa={g["name"]: AX2 * alpha(AP * SIG0[g["name"]]) * g["us"] / g["uk"] for g in GAL})
    P(f"[{f}] (1) X-ray ellipticals: Kroupa D {DKr:+.4f} -> IMF D {DI:+.4f} (sigma x0.9 {Dlo:+.4f}, x1.1 {Dhi:+.4f}); F {FE:.2f}; "
      f"|D|<=0.15 {abs(DI) <= 0.15} -> {lE_tag}")
    P(f"[{f}]     per galaxy (IMF): " + ", ".join(f"{k} {v:+.3f} (x{o['ellipticals']['factor_vs_kroupa'][k]:.2f})" for k, v in per.items()))
    if MUT:
        m_ok = FE > 1.0; okm = okm and m_ok
        P(f"[{f}] MUTATE alpha x2: F {FE:.2f} -> {'OVER-CORRECTS (bites)' if m_ok else 'NO POWER'}")
        RES["foot"][f] = o; continue
    # KA1
    ka1e = abs(DKr - QX18[f]); x1, g1 = hot_means(a0, 1.0, 1.0)
    ka1h = max(abs(x1 - QX20[f]["X"]), abs(g1 - QX20[f]["G"]))
    # KiDS
    kd = {}
    for se in KIDS_SIG:
        fk = alpha(se) * K_TO_S
        dl = float(np.mean([slope(gb[i], a0) * math.log10(fk) for i in K1]))
        kd[se] = dict(f=fk, Delta=dl, R=DX - dl, F=dl / DX, label=lab(dl / DX, abs(DX - dl) < 2 * S_TOT))
    labsK = {v["label"] for v in kd.values()}; lK = kd[170]["label"] + ("" if len(labsK) == 1 else " [BRACKET-DEPENDENT]")
    o["kids"] = dict(D=Dk, D_law=D_law, DX=DX, s_tot=S_TOT, bracket=kd, label=lK)
    P(f"[{f}] (2) KiDS early/late: D - D_law {DX:+.3f} +- {S_TOT}; " + "; ".join(
        f"sigma_e {se}: f {v['f']:.2f}, Delta {v['Delta']:+.3f}, R {v['R']:+.3f} ({v['R']/S_TOT:+.2f} sigma), F {v['F']:.2f}" for se, v in kd.items()) + f" -> {lK}")
    # X-COP + groups
    hx = {}
    for sx, sg in zip(XCOP_SIG, GRP_SIG):
        fx, fg = fK(sx), fK(sg); xm, gm = hot_means(a0, fx, fg)
        hx[sx] = dict(fx=fx, fg=fg, X=xm, G=gm, FX=(x1 - xm) / x1, FG=(g1 - gm) / g1)
    lX = lab(hx[300]["FX"], abs(hx[300]["X"]) <= 0.05); lG = lab(hx[300]["FG"], True)
    lX += "" if len({lab(v['FX'], abs(v['X']) <= 0.05) for v in hx.values()}) == 1 else " [BRACKET-DEPENDENT]"
    lG += "" if len({lab(v['FG'], True) for v in hx.values()}) == 1 else " [BRACKET-DEPENDENT]"
    o["xcop"] = dict(base=x1, bracket={k: dict(fx=v["fx"], X=v["X"], F=v["FX"]) for k, v in hx.items()}, label=lX)
    o["groups"] = dict(base=g1, bracket={k: dict(fg=v["fg"], G=v["G"], F=v["FG"]) for k, v in hx.items()}, label=lG)
    P(f"[{f}] (4) X-COP: base {x1:+.4f}; " + "; ".join(f"BCG sigma {k}: x{v['fx']:.2f} -> {v['X']:+.4f} (F {v['FX']:.3f})" for k, v in hx.items()) + f" -> {lX}")
    P(f"[{f}]     groups: base {g1:+.4f}; " + "; ".join(f"sigma {s}: x{v['fg']:.2f} -> {v['G']:+.4f} (F {v['FG']:.3f})" for s, v in zip(GRP_SIG, hx.values())) + f" -> {lG}")
    # dSphs
    a_need = 10 ** (2 * 0.20)
    o["dsph"] = dict(correction="none (sigma 7-12 km/s outside the relation; Kroupa floor)", F=0.0, label="NOT",
                     alpha_vs_kroupa_needed_deepMOND=a_need, relation_at_10kms_vs_kroupa=alpha(10) * K_TO_S)
    P(f"[{f}] (3a) dSphs: no correction (outside range) -> NOT; nulling +0.20 in deep MOND needs M* x{a_need:.2f}, "
      f"while the relation extrapolated to 10 km/s gives x{alpha(10)*K_TO_S:.2f} (lighter than Kroupa)")
    # SPARC bulges
    sp = {}
    for sb in (None,) + BUL_SIG:
        fb = 1.0 if sb is None else fK(sb); st = sparc_grade(a0, fb); sp["1.0" if sb is None else str(sb)] = dict(fb=fb, **st)
    ka2 = abs(sp["1.0"]["rms"] - P4[f][0]) <= 1e-5 and abs(sp["1.0"]["U_median"] - P4[f][1]) <= 1e-9
    brk = not all(v["line"] for v in sp.values())
    o["sparc"] = dict(grades=sp, breaks_sparc=brk, label="BREAKS SPARC" if brk else "SPARC PASS PRESERVED")
    P(f"[{f}] (3b) SPARC bulges: " + "; ".join(f"{k}: x{v['fb']:.2f} rms {v['rms']:.5f} @ U {v['U_median']:.2f} {'PASS' if v['line'] else 'FAIL'}" for k, v in sp.items())
      + f" -> {o['sparc']['label']}")
    o.update(KA1_ell=ka1e, KA1_hot=ka1h, KA1=bool(ka1e <= 1e-3 and ka1h <= 1e-3), KA2=bool(ka2))
    P(f"[{f}] KA1 Kroupa vs QX18 |{ka1e:.1e}|, vs QX20 X/G |{ka1h:.1e}| -> {'PASS' if o['KA1'] else 'FAIL'}; KA2 SPARC fb=1 vs P4 -> {'PASS' if ka2 else 'FAIL'}")
    RES["foot"][f] = o

if MUT: P(f"MUTATE: {'BITES' if okm else 'NO POWER'}")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (okm if MUT else True) else 1)
