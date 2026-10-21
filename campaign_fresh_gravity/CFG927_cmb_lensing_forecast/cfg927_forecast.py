#!/usr/bin/env python3
"""CFG927 sealed forecast (FROZEN_CRITERIA.md, commit 8791d53c3): Fisher-style Gaussian dchi2 between each run's own Limber C_L^phiphi
(CFG917's machinery, read-only, projector extended to L 3000) and its same-pipeline control, per declared survey noise model and L range,
with the box support cut honoured per L.  K1-K3, K6 here (K4, K5, K7 in cfg927_noise.py); MUTATE first.

    CFG927_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg927_forecast.py --pair T1x    (FIRST; -> cfg927_T1x_MUTATE.out/json)
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg927_forecast.py --pair T1x                    (-> cfg927_T1x.out/json)
pairs: T1x, T2x (inherited, control CFG596 P0); NC1x (native, control NCS0); P1 (CFG596 candidate B, KiDS-EXCLUDED, control P0).
Requires cfg927_noise.json.  One process, numpy/scipy only, < 1 GB.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, json, math, glob, time, argparse, hashlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE)
D917 = os.path.join(CFG, "CFG917_cmb_lensing_gate")
sys.path.insert(0, D917)
import cfg917_lib as LB                                    # read-only, unchanged

ap = argparse.ArgumentParser(); ap.add_argument("--pair", required=True, choices=["T1x", "T2x", "NC1x", "P1"]); ARGS = ap.parse_args()
MUTATE = os.environ.get("CFG927_MUTATE", "0") == "1"
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
CHECKS = {}
def check(name, desc, ok, detail="", gating=True):
    CHECKS[name] = dict(desc=desc, ok=bool(ok), detail=detail, gating=gating)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if gating else ' (reported)'} {name}: {desc} -- {detail}")
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()

# ------------------------------------------------------------------ run files (globs copied verbatim from cfg917_cmb_lensing.py PAIRS)
W654, W650, W596 = (os.path.join(LB.EXT, d) for d in ("cfg654_work", "cfg650_work", "cfg596_work"))
def one(pat):
    f = [x for x in glob.glob(pat) if not x.endswith("job.json")]
    if len(f) != 1: raise SystemExit(f"expected exactly one run JSON for {LB.rel(pat)}, found {len(f)} (run not finished?)")
    return f[0]
P0J = lambda: one(os.path.join(W596, "P0", "cfg596_S0_canonical_*_lean.json"))
PAIRS = {"NC1x": lambda: (one(os.path.join(W654, "NC1x", "cfg654cmb_cfg650_*_RES_canonical_*.json")), one(os.path.join(W654, "NCS0", "cfg654cmb_cfg650_na_S0_*.json"))),
         "T1x": lambda: (one(os.path.join(W650, "T1x", "cfg650_m1m2m3_RES_canonical_*.json")), P0J()),
         "T2x": lambda: (one(os.path.join(W650, "T2x", "cfg650_m1m2m3_RES_alt_*.json")), P0J()),
         "P1": lambda: (one(os.path.join(W596, "P1", "cfg596_RES_canonical_*_lean.json")), P0J())}

# ------------------------------------------------------------------ stored CFG917 values (K2 targets, vc flag)
if ARGS.pair == "P1":
    S917 = json.load(open(os.path.join(D917, "cfg917_T1x_MUTATE.json")))
    K2T = dict(primary=S917["M3_context"]["primary"]["dchi2"], **{m: v["dchi2"] for m, v in S917["M3_context"]["members"].items()})
    VC = True                                              # CFG917 M3 built P1 vs P0 with vc=True
    K2SRC = "cfg917_T1x_MUTATE.json M3_context"
else:
    S917 = json.load(open(os.path.join(D917, f"cfg917_{ARGS.pair}.json")))
    K2T = dict(primary=S917["primary"]["dchi2"], **{m: v["dchi2"] for m, v in S917["members"].items()})
    VC = bool(S917["model"]["vc"])
    K2SRC = f"cfg917_{ARGS.pair}.json"

NZ = json.load(open(os.path.join(HERE, "cfg927_noise.json")))
GRADED = ["ACT-DR6-like", "SO-baseline-like", "S4-like"]
MOD = {nm: dict(NX=np.array(NZ["models"][nm]["NX"]), fsky=NZ["models"][nm]["params"]["fsky"], Lmin=NZ["models"][nm]["params"]["Lmin"]) for nm in GRADED}
MOD["CV-limited"] = dict(NX=np.zeros(3001), fsky=0.40, Lmin=30)
SCAN = {k: np.array(v["NX"]) for k, v in NZ["scan"].items()}
LMAXES = [400, 763, 1000, 2000, 3000]
LMX = 3000
ROB = ["ZHOLD", "ZREL", "KCUT", "KLOW", "BG"]

D = LB.load_pr4(); XFFP = LB.load_ffp10(); AGGT = LB.load_pl18_agg()
fF, fS = PAIRS[ARGS.pair]()
RF, RS = LB.load_run(fF), LB.load_run(fS)
KIND = LB.inputs_of(RS); assert LB.inputs_of(RF) == KIND, "both arms must carry the same input set"
INP = LB.Inputs(KIND); OTHER = LB.Inputs("inherited" if KIND != "inherited" else "native_cmb")
FOOT = RF["meta"]["foot"]
RES = dict(lane="CFG927", pair=ARGS.pair, mutate=MUTATE, criteria_commit="8791d53c3", inputs=KIND, foot=FOOT,
           settings="kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed; a forecast, "
                    "not a measurement; framework-native models only (no LCDM fit, no CAMB/CLASS nonlinear spectrum, halofit, HMcode or BAHAMAS)",
           files=dict(F=LB.rel(fF), S0=LB.rel(fS)), sha256=dict(F=sha(fF)[:16], S0=sha(fS)[:16], cfg917_lib=sha(LB.__file__)[:16],
                                                               noise_json=sha(os.path.join(HERE, "cfg927_noise.json"))[:16]),
           k2_source=K2SRC, vc=VC)
P(f"CFG927 forecast  pair {ARGS.pair} ({KIND} inputs, {FOOT} footing)  MUTATE={MUTATE}")
P(f"  F  = {RES['files']['F']}\n  S0 = {RES['files']['S0']}\n  cfg917_lib sha256 {RES['sha256']['cfg917_lib']}; variance correction vc = {VC}")

ZG = LB.zgrid(); ZG2 = LB.zgrid(800, 1200)

# ------------------------------------------------------------------ extended projector: verbatim copy of LB.limber_X, output length Lmax+1
def limber_ext(Pfun, inp, zg, Om, bg=None, Lmin=2, Lmax=LMX, masks=None):
    B = inp if bg is None else bg
    chi = B.chi(zg); cs = B.chi_star; Ls = np.arange(Lmin, Lmax + 1, dtype=float)
    pref = (1.5 * Om / LB.CKMS_H ** 2) ** 2
    I = np.zeros((len(Ls), len(zg))); Im = {m: np.zeros_like(I) for m in (masks or {})}
    for j, (z, c) in enumerate(zip(zg, chi)):
        k = (Ls + 0.5) / c; p = Pfun(k, 1.0 / (1.0 + z), z)
        w = pref * ((1 + z) * (cs - c) / cs) ** 2
        I[:, j] = w * p
        for m, f in (masks or {}).items(): Im[m][:, j] = w * p * f(k, z)
    fac = 4.0 / (Ls + 0.5) ** 4 * (Ls * (Ls + 1)) ** 2 / (2 * math.pi)
    def proj(II):
        X = np.zeros(Lmax + 1); X[Lmin:Lmax + 1] = fac * LB._trapz(II, chi, axis=1); return X
    out = proj(I)
    if masks: return out, {m: proj(v) for m, v in Im.items()}
    return out

def projE(Mx, arm, zg=ZG, zrule="lin", klow=False, bg=None, masks=None):
    f = lambda k, a, z: Mx.P(arm, k, a, zrule=zrule, klow=klow)
    return limber_ext(f, INP, zg, INP.Om, bg=bg, masks=masks)

def projL(Mx, arm, zg=ZG, zrule="lin", klow=False, bg=None):          # CFG917's own projector (L <= 2500)
    f = lambda k, a, z: Mx.P(arm, k, a, zrule=zrule, klow=klow)
    return LB.limber_X(f, INP, zg, INP.Om, bg=bg)

MEMBER_KW = {"primary": ({}, {}), "ZHOLD": (dict(zrule="hold"), dict(zrule="hold")), "ZREL": (dict(zrule="rel"), dict(zrule="rel")),
             "KLOW": (dict(klow=True), {}), "BG": (dict(bg=OTHER), dict(bg=OTHER))}
def all_X(Mx, Mxc, proj=projE, zg=ZG):
    out = {}
    for nm, (kF, kS) in MEMBER_KW.items(): out[nm] = (proj(Mx, "F", zg, **kF), proj(Mx, "S0", zg, **kS))
    out["KCUT"] = (proj(Mxc, "F", zg), proj(Mxc, "S0", zg))
    return out

def fisher(XF, XS, NX, fsky, lo, hi):
    L = np.arange(lo, hi + 1); d = XF[L] - XS[L]
    return float((fsky * (2 * L + 1) / 2 * d * d / (XS[L] + NX[L]) ** 2).sum())
def fisher_cum(XF, XS, NX, fsky, lo):
    L = np.arange(lo, LMX + 1); d = XF[L] - XS[L]
    return L, np.cumsum(fsky * (2 * L + 1) / 2 * d * d / (XS[L] + NX[L]) ** 2)
def klass(v): return "DISCRIMINATING" if v >= 9 else ("MARGINAL" if v >= 4 else "BLIND")

def support(Mx, zg=ZG):
    kl, kt = Mx.k_lo, Mx.k_top
    masks = {"khi": lambda k, z: (k > kt) * 1.0, "klo": lambda k, z: (k < kl) * 1.0, "zhi": lambda k, z: np.full_like(k, 1.0 if z > 1.0 else 0.0)}
    XF, mF = projE(Mx, "F", zg, masks=masks); XS, mS = projE(Mx, "S0", zg, masks=masks)
    L = np.arange(8, LMX + 1)
    sS = mS["khi"][L] / XS[L]
    dh = mF["khi"][L] - mS["khi"][L]; dX = XF[L] - XS[L]; den = np.abs(dh) + np.abs(dX - dh)
    sD = np.where(den > 0, np.abs(dh) / np.where(den > 0, den, 1.0), 0.0)
    ok = (sS <= 0.10) & (sD <= 0.10)
    bad = np.where(~ok)[0]
    Lsup = int(L[bad[0]] - 1) if len(bad) else LMX
    rep = {}
    for q in (400, 763, 1000, 2000, 3000):
        i = q - 8; dq = XF[q] - XS[q]
        sh = lambda reg: dict(S0=float(mS[reg][q] / XS[q]), dX=(float((mF[reg][q] - mS[reg][q]) / dq) if dq != 0 else 0.0))
        rep[str(q)] = dict(s_S0_khi=float(sS[i]), s_dX_khi=float(sD[i]), klo=sh("klo"), zhi=sh("zhi"), ratio_XF_XS=float(XF[q] / XS[q]))
    return dict(L_sup=Lsup, L_sup_label=("≥ 3000" if Lsup >= LMX else str(Lsup)), max_s_S0=float(sS.max()), max_s_dX=float(sD.max()), at=rep)

def cells(XX, Lsup):
    """forecast cells (FROZEN section 6) from a dict member -> (XF, XS)."""
    out = {}
    for nm, m in MOD.items():
        lo = m["Lmin"]; row = {}
        for hi in LMAXES:
            prim = fisher(*XX["primary"], m["NX"], m["fsky"], lo, hi)
            mem = {r: fisher(*XX[r], m["NX"], m["fsky"], lo, hi) for r in ROB if r in XX}
            comp = hi <= Lsup
            cl = klass(prim) if comp else "NOT COMPUTABLE"
            robust = comp and all(klass(v) == klass(prim) for v in mem.values())
            cell = dict(L=[lo, hi], dchi2=prim, class_=cl, members=mem, robust=bool(robust),
                        member_range=[min(mem.values()), max(mem.values())] if mem else None, sd_realised=2 * math.sqrt(max(prim, 0.0)))
            if not comp: cell["computable_part"] = dict(L=[lo, Lsup], dchi2=fisher(*XX["primary"], m["NX"], m["fsky"], lo, Lsup))
            row[str(hi)] = cell
        Lc, cum = fisher_cum(*XX["primary"], m["NX"], m["fsky"], lo)
        hit = np.where(cum >= 9)[0]
        L9 = int(Lc[hit[0]]) if len(hit) else None
        row["L_9"] = (None if L9 is None else (L9 if L9 <= Lsup else f">= L_sup ({Lsup}), not computable"))
        row["cum_every_50"] = {str(int(l)): float(c) for l, c in zip(Lc, cum) if int(l) % 50 == 0 or int(l) == LMX}
        out[nm] = row
    return out

def scan_rows(XX, Lsup):
    hi = min(LMX, Lsup); out = {}
    for k, NX in list(SCAN.items()) + [("0", np.zeros(3001))]:
        prim = fisher(*XX["primary"], NX, 0.40, 30, hi); mem = {r: fisher(*XX[r], NX, 0.40, 30, hi) for r in ROB if r in XX}
        out[k] = dict(dT=float(k), dchi2=prim, class_=klass(prim), member_range=[min(mem.values()), max(mem.values())] if mem else None)
    pts = sorted(((float(k), v["dchi2"]) for k, v in out.items() if float(k) > 0), key=lambda t: t[0])   # ascending dT
    cv = out["0"]["dchi2"]
    if cv < 9: d9 = "unreachable at f_sky 0.4"
    elif pts[-1][1] >= 9: d9 = "> 20"
    elif pts[0][1] < 9: d9 = "< 0.5"
    else:
        d9 = None
        for (a, fa), (b, fb) in zip(pts[:-1], pts[1:]):
            if fa >= 9 > fb:
                t_ = (math.log(9) - math.log(fa)) / (math.log(fb) - math.log(fa)); d9 = float(math.exp(math.log(a) + t_ * (math.log(b) - math.log(a)))); break
    return dict(L=[30, hi], rows=out, dT_9=d9)

def pr4_asimov(XF, XS):
    dB = LB.wsum(D["W"], XF - XS) + LB.wsum(D["M"], XF - XS)
    return LB.qform(dB, D["Cinv"])

# ------------------------------------------------------------------ models
M = LB.PairModel(RF, RS, INP, vc=VC); Mcut = LB.PairModel(RF, RS, INP, vc=VC, kcut_div=8.0)
RES["model"] = dict(support=[M.k_lo, M.k_top, M.nsup], kcut_top=Mcut.k_top, vc=VC)
P(f"  support {M.k_lo:.4f}-{M.k_top:.3f} h/Mpc ({M.nsup} bins); KCUT top {Mcut.k_top:.3f}; background Om {INP.Om:.6f}, h {INP.h:.6f}, chi_* {INP.chi_star:.1f} Mpc/h")

P("\nbox support cut (FROZEN section 3)")
SUP = support(M)
P(f"  L_sup = {SUP['L_sup_label']} (max over L 8-3000: s_S0 {SUP['max_s_S0']:.4f}, s_dX {SUP['max_s_dX']:.4f}; threshold 0.10)")
for q, v in SUP["at"].items():
    P(f"    L {q}: k>k_top share S0 {v['s_S0_khi']:.4f}, dX {v['s_dX_khi']:.4f}; k<k_lo share S0 {v['klo']['S0']:.3f}, dX {v['klo']['dX']:.3f}; "
      f"z>1 share S0 {v['zhi']['S0']:.3f}, dX {v['zhi']['dX']:.3f}; X_F/X_S0 {v['ratio_XF_XS']:.4f}")
RES["support_cut"] = SUP
LSUP = SUP["L_sup"]

if MUTATE:
    P("\nMUTATE set (FROZEN section 8)")
    M1 = LB.PairModel(RS, RS, INP, vc=VC); M1c = LB.PairModel(RS, RS, INP, vc=VC, kcut_div=8.0)
    X1 = all_X(M1, M1c); C1 = cells(X1, LMX)
    mx1 = max(abs(c["dchi2"]) for row in C1.values() for k, c in row.items() if k in map(str, LMAXES))
    mx1 = max(mx1, *[abs(v) for row in C1.values() for k, c in row.items() if k in map(str, LMAXES) for v in c["members"].values()])
    check("M1", "F == S0 -> forecast dchi2 = 0 (<= 1e-12) in every model, range and member", mx1 <= 1e-12, f"max |dchi2| {mx1:.1e}")
    XS = projE(M, "S0"); rep = {}; ok_id = True; s4 = {}
    for sgn in (+1, -1):
        eps = 0.05 * sgn
        XFi = limber_ext(lambda k, a, z: M.P("S0", k, a) * (1 + eps), INP, ZG, INP.Om)
        r_ = {}
        for nm in GRADED:
            m = MOD[nm]; lo = m["Lmin"]; hi = min(LMX, LSUP); L = np.arange(lo, hi + 1)
            pipe = fisher(XFi, XS, m["NX"], m["fsky"], lo, hi)
            ana = float(eps ** 2 * (m["fsky"] * (2 * L + 1) / 2 * XS[L] ** 2 / (XS[L] + m["NX"][L]) ** 2).sum())
            rel_ = abs(pipe - ana) / ana; ok_id &= rel_ <= 1e-8
            r_[nm] = dict(L=[lo, hi], pipeline=pipe, analytic=ana, rel=rel_, class_=klass(pipe))
        s4[f"{sgn:+d}"] = r_["S4-like"]["pipeline"]; rep[f"{1 + eps:.2f}"] = r_
        P(f"    M2 {1 + eps:.2f} x S0: " + "; ".join(f"{nm} L {v['L'][0]}-{v['L'][1]} dchi2 {v['pipeline']:.2f} (analytic {v['analytic']:.2f}, rel {v['rel']:.1e}) {v['class_']}"
                                                for nm, v in r_.items()))
    okM2 = ok_id and min(s4.values()) >= 9
    check("M2", "+-5% amplitude: pipeline = analytic (<= 1e-8 rel) AND S4-like over L 30-min(3000, L_sup) >= 9 for both signs", okM2,
          f"S4-like dchi2 +5% {s4['+1']:.2f}, -5% {s4['-1']:.2f}; identity {'holds' if ok_id else 'FAILS'}")
    RES["M2"] = rep
    m3 = {}
    for sgn in (+1, -1):
        eps = 0.05 * sgn; kl, kt = M.k_lo, M.k_top
        XFb = limber_ext(lambda k, a, z: M.P("S0", k, a) * (1 + eps * ((k >= kl) & (k <= kt)) * (1.0 if z <= 1.0 else 0.0)), INP, ZG, INP.Om)
        m3[f"{1 + eps:.2f}"] = {nm: {str(hi): dict(dchi2=fisher(XFb, XS, MOD[nm]["NX"], MOD[nm]["fsky"], MOD[nm]["Lmin"], hi),
                                                  class_=klass(fisher(XFb, XS, MOD[nm]["NX"], MOD[nm]["fsky"], MOD[nm]["Lmin"], hi)) if hi <= LSUP else "NOT COMPUTABLE")
                                    for hi in LMAXES} for nm in GRADED}
        P(f"    M3 context, box-only {1 + eps:.2f} (k_lo <= k <= k_top, z <= 1): " +
          "; ".join(f"{nm} " + ", ".join(f"{hi}: {m3[f'{1 + eps:.2f}'][nm][str(hi)]['dchi2']:.2f}" for hi in LMAXES) for nm in GRADED))
    RES["M3_context"] = m3
    RES["mutate_bites"] = CHECKS["M1"]["ok"] and CHECKS["M2"]["ok"]
    P(f"  MUTATE bites: {RES['mutate_bites']}")
else:
    P("\nforecast (FROZEN sections 4-6)")
    XX = all_X(M, Mcut)
    CEL = cells(XX, LSUP); SC = scan_rows(XX, LSUP)
    asim = pr4_asimov(projL(M, "F"), projL(M, "S0"))
    for nm, row in CEL.items():
        tag = " (context, ceiling; no class weight)" if nm == "CV-limited" else ""
        P(f"  {nm}{tag}: f_sky {MOD[nm]['fsky']}, L_min {MOD[nm]['Lmin']}; L_9 = {row['L_9']}")
        for hi in LMAXES:
            c = row[str(hi)]
            P(f"    L {c['L'][0]}-{hi}: dchi2 {c['dchi2']:.3f}  {c['class_']}{'' if c['class_'] == 'NOT COMPUTABLE' else (' ROBUST' if c['robust'] else ' RULE-DEPENDENT')}"
              f"  [members {c['member_range'][0]:.3f}..{c['member_range'][1]:.3f}: " + ", ".join(f"{r} {v:.3f}" for r, v in c["members"].items()) + "]"
              + (f"  computable part L {c['computable_part']['L'][0]}-{c['computable_part']['L'][1]}: {c['computable_part']['dchi2']:.3f}" if "computable_part" in c else ""))
    P(f"  noise scan (f_sky 0.40, beam 1.4', L {SC['L'][0]}-{SC['L'][1]}): " + ", ".join(f"dT {k}: {v['dchi2']:.2f}" for k, v in SC["rows"].items())
      + "; dT_9 = " + (SC["dT_9"] if isinstance(SC["dT_9"], str) else f"{SC['dT_9']:.2f} uK-arcmin"))
    P(f"  PR4 Asimov (context; PR4 8-400 covariance, dB = (W + M) dX): {asim:.4f}")
    RES["cells"] = CEL; RES["noise_scan"] = SC; RES["pr4_asimov_8_400"] = asim
    reading = {}
    for nm in GRADED:
        hit = [hi for hi in LMAXES if CEL[nm][str(hi)]["class_"] == "DISCRIMINATING"]
        reading[nm] = (f"DISCRIMINATING from L {CEL[nm][str(hit[0])]['L'][0]}-{hit[0]} ({'ROBUST' if CEL[nm][str(hit[0])]['robust'] else 'RULE-DEPENDENT'})"
                       if hit else f"not within L <= {min(LMX, LSUP)}")
    RES["reading"] = reading
    P("  reading: " + "; ".join(f"{k}: {v}" for k, v in reading.items()))

    P("\nK tests")
    # K1 F == S0
    M1 = LB.PairModel(RS, RS, INP, vc=VC); M1c = LB.PairModel(RS, RS, INP, vc=VC, kcut_div=8.0)
    X1 = all_X(M1, M1c); C1 = cells(X1, LMX)
    v1 =[abs(c["dchi2"]) for row in C1.values() for k, c in row.items() if k in map(str, LMAXES)]
    v1 += [abs(v) for row in C1.values() for k, c in row.items() if k in map(str, LMAXES) for v in c["members"].values()]
    XL1F, XL1S = projL(M1, "F"), projL(M1, "S0")
    v1 += [abs(pr4_asimov(XL1F, XL1S)), abs(LB.pr4_chi2(D, XL1F) - LB.pr4_chi2(D, XL1S))]
    check("K1", "F == S0 -> 0 (<= 1e-12) in every cell, member, PR4 Asimov and PR4 dchi2", max(v1) <= 1e-12, f"max |dchi2| {max(v1):.1e}")
    # K2 CFG917 PR4-range reproduction through this path
    XL = all_X(M, Mcut, proj=projL)
    got = {m: LB.pr4_chi2(D, XL[m][0]) - LB.pr4_chi2(D, XL[m][1]) for m in XL}
    aF, _ = LB.agg_chi2(AGGT, XL["primary"][0], XFFP); aS, _ = LB.agg_chi2(AGGT, XL["primary"][1], XFFP); got["AGG"] = aF - aS
    dev2 = {m: abs(got[m] - K2T[m]) for m in K2T}
    check("K2", f"CFG917 PR4 8-400 dchi2 (primary + AGG/ZHOLD/ZREL/KCUT/KLOW/BG) reproduced vs {K2SRC} (<= 1e-6 abs)", max(dev2.values()) <= 1e-6,
          ", ".join(f"{m} {got[m]:+.4f} (|d| {dev2[m]:.1e})" for m in K2T))
    RES["K2"] = dict(this_path=got, stored=K2T)
    # K3 extended projector vs LB.limber_X on L 2-2500
    d3 = 0.0
    for arm in ("F", "S0"):
        a_, b_ = XX["primary"][0 if arm == "F" else 1][2:2501], XL["primary"][0 if arm == "F" else 1][2:2501]
        d3 = max(d3, float(np.max(np.abs(a_ / b_ - 1))))
    check("K3", "extended projector = LB.limber_X on L 2-2500 (<= 1e-12 rel, both arms, primary)", d3 <= 1e-12, f"max rel dev {d3:.1e}")
    # K6 doubled z grid
    SUP2 = support(M, zg=ZG2)
    XX2 = {"primary": (projE(M, "F", ZG2), projE(M, "S0", ZG2))}
    C2 = cells(XX2, SUP2["L_sup"]); d6 = []
    for nm in MOD:
        for hi in LMAXES:
            a_, b_ = CEL[nm][str(hi)]["dchi2"], C2[nm][str(hi)]["dchi2"]; d6.append((abs(a_ - b_), max(0.01, 0.01 * abs(a_))))
    ok6 = all(x <= tol for x, tol in d6) and SUP2["L_sup"] == LSUP
    check("K6", "doubling the z nodes changes every primary forecast cell by <= max(0.01, 1%) and leaves L_sup unchanged", ok6,
          f"max |change| {max(x for x, _ in d6):.2e}; L_sup {LSUP} -> {SUP2['L_sup']}")
    # noise K tests (from cfg927_noise.json)
    for k in ("K4", "K5", "K7"):
        c = NZ["checks"][k]; check(k, c["desc"] + " (cfg927_noise.json)", c["ok"], c["detail"], gating=c["gating"])
    # ---------------- status
    mfn = os.path.join(HERE, f"cfg927_{ARGS.pair}_MUTATE.json")
    bites = json.load(open(mfn)).get("mutate_bites") if os.path.exists(mfn) else None
    gate_ok = all(v["ok"] for v in CHECKS.values() if v["gating"])
    flags = []
    if not gate_ok: flags.append("gating K test failed: " + ", ".join(k for k, v in CHECKS.items() if v["gating"] and not v["ok"]))
    if bites is None: flags.append("MUTATE output missing (run CFG927_MUTATE=1 first)")
    elif not bites: flags.append("MUTATE does not bite")
    if flags:
        for row in CEL.values():
            for hi in LMAXES: row[str(hi)]["class_rule_value"] = row[str(hi)]["class_"]; row[str(hi)]["class_"] = "NOT DIAGNOSTIC (forecast)"
    RES["gate_ok"] = gate_ok; RES["mutate_bites"] = bites; RES["flags"] = flags
    P(f"\nSTATUS ({ARGS.pair}, {FOOT} footing, {KIND} inputs): gating K {'PASS' if gate_ok else 'FAIL'}; MUTATE bites {bites}"
      + (("; flags: " + "; ".join(flags)) if flags else ""))
    P("  A forecast is not a measurement; DISCRIMINATING means a survey of that kind could tell the two arms apart, not that either is right.")

RES["checks"] = CHECKS; RES["runtime_s"] = time.time() - T0
try:
    import resource; RES["maxrss_gb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
except Exception:
    pass
P(f"\nruntime {RES['runtime_s']:.0f} s; maxrss {RES.get('maxrss_gb', 0):.2f} GB. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
def _clean(o):
    if isinstance(o, dict): return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return o
base = os.path.join(HERE, f"cfg927_{ARGS.pair}" + ("_MUTATE" if MUTATE else ""))
json.dump(_clean(RES), open(base + ".json", "w"), indent=1)
open(base + ".out", "w").write("\n".join(OUT) + "\n")
