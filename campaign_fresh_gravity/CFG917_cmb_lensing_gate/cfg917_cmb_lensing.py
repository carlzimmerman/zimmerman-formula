#!/usr/bin/env python3
"""CFG917 Part B (FROZEN_CRITERIA.md, commit 0289e4ad4): each run's own Limber C_L^phiphi from its MEASURED gravitating P(k, z) against
the raw Planck PR4 lensing bandpowers (CMB-marginalised, conservative L 8-400, published covariance and linear fiducial correction).
Statistic dchi2 = chi2(F) - chi2(S0) per pair; shear-scorer classes; robustness AGG / ZHOLD / ZREL / KCUT / KLOW / BG; K1-K6; MUTATE first.

    CFG917_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg917_cmb_lensing.py --pair NC1x     (FIRST; -> cfg917_NC1x_MUTATE.out/json)
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg917_cmb_lensing.py --pair NC1x                     (-> cfg917_NC1x.out/json)
pairs: NC1x, NC2x (native, control NCS0); T1x, T2x (inherited, control CFG596 P0); P1 (CFG596 candidate B, context / M3 only).
Requires cfg917_camb_ktests.json (K3d, K3e).  One process, numpy/scipy only, < 1 GB.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys, json, math, glob, time, argparse, hashlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.stats import chi2 as CHI2
import cfg917_lib as LB

T0 = time.time()
ap = argparse.ArgumentParser(); ap.add_argument("--pair", required=True, choices=["NC1x", "NC2x", "T1x", "T2x", "P1"]); ARGS = ap.parse_args()
MUTATE = os.environ.get("CFG917_MUTATE", "0") == "1"
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
CHECKS = {}
def check(name, desc, ok, detail="", gating=True):
    CHECKS[name] = dict(desc=desc, ok=bool(ok), detail=detail, gating=gating)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if gating else ' (reported)'} {name}: {desc} -- {detail}")

W654, W650, W596 = (os.path.join(LB.EXT, d) for d in ("cfg654_work", "cfg650_work", "cfg596_work"))
def one(pat):
    f = [x for x in glob.glob(pat) if not x.endswith("job.json")]
    if len(f) != 1: raise SystemExit(f"expected exactly one run JSON for {LB.rel(pat)}, found {len(f)} (run not finished?)")
    return f[0]
P0J = lambda: one(os.path.join(W596, "P0", "cfg596_S0_canonical_*_lean.json"))
PAIRS = {"NC1x": lambda: (one(os.path.join(W654, "NC1x", "cfg654cmb_cfg650_*_RES_canonical_*.json")), one(os.path.join(W654, "NCS0", "cfg654cmb_cfg650_na_S0_*.json"))),
         "NC2x": lambda: (one(os.path.join(W654, "NC2x", "cfg654cmb_cfg650_*_RES_alt_*.json")), one(os.path.join(W654, "NCS0", "cfg654cmb_cfg650_na_S0_*.json"))),
         "T1x": lambda: (one(os.path.join(W650, "T1x", "cfg650_m1m2m3_RES_canonical_*.json")), P0J()),
         "T2x": lambda: (one(os.path.join(W650, "T2x", "cfg650_m1m2m3_RES_alt_*.json")), P0J()),
         "P1": lambda: (one(os.path.join(W596, "P1", "cfg596_RES_canonical_*_lean.json")), P0J())}
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()

D = LB.load_pr4(); XFFP = LB.load_ffp10(); AGGT = LB.load_pl18_agg()
NDOF = D["n"]; NAGG = len(AGGT["8-2048"])
fF, fS = PAIRS[ARGS.pair]()
RF, RS = LB.load_run(fF), LB.load_run(fS)
KIND = LB.inputs_of(RS); assert LB.inputs_of(RF) == KIND, "both arms must carry the same input set"
INP = LB.Inputs(KIND); OTHER = LB.Inputs("inherited" if KIND != "inherited" else "native_cmb")
FOOT = RF["meta"]["foot"]
RES = dict(lane="CFG917", part="B", criteria_commit="0289e4ad4", pair=ARGS.pair, mutate=MUTATE, inputs=KIND, foot=FOOT,
           settings="kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed; raw PR4 "
                    "bandpowers; no LCDM fit, no CAMB/CLASS nonlinear spectrum, halofit, HMcode or BAHAMAS in any model or verdict",
           files=dict(F=LB.rel(fF), S0=LB.rel(fS)), sha256=dict(F=sha(fF)[:16], S0=sha(fS)[:16]),
           data=dict(primary="Planck PR4 lensing, PlanckPR4LensingMarged, " + LB.STEM + "_CMBmarged (L 8-400, 9 bands)",
                     aggressive="Planck 2018 VIII Table 1 MV 8-2048 (typed in XR26_cmb.py), amplitudes vs FFP10, diagonal"))
P(f"CFG917 Part B  pair {ARGS.pair} ({KIND}, {FOOT})  MUTATE={MUTATE}")
P(f"  F  = {RES['files']['F']}\n  S0 = {RES['files']['S0']}")
P(f"  background: Om {INP.Om:.6f}, Or {INP.Or:.3e}, h {INP.h:.6f}; chi_* = {INP.chi_star:.1f} Mpc/h (z* = {LB.Z_STAR:g}); other background chi_* = {OTHER.chi_star:.1f}")

ZG = LB.zgrid(); ZG2 = LB.zgrid(800, 1200)

def build(F, S, **kw):
    return LB.PairModel(F, S, INP, **kw)

def proj(M, arm, zg=ZG, zrule="lin", klow=False, bg=None, inject=None, masks=None):
    f = lambda k, a, z: M.P(arm, k, a, zrule=zrule, klow=klow, inject=inject)
    return LB.limber_X(f, INP, zg, INP.Om, bg=bg, masks=masks)

def stats_pair(XF, XS):
    cF, cS = LB.pr4_chi2(D, XF), LB.pr4_chi2(D, XS)
    return dict(chi2_F=cF, chi2_S0=cS, dchi2=cF - cS)

def members(M, Mcut, zg=ZG):
    """robustness members (FROZEN B3), each: chi2_F, chi2_S0, dchi2 (data: primary PR4 unless AGG)."""
    out = {}
    XF, XS = proj(M, "F", zg), proj(M, "S0", zg)
    out["_primary"] = stats_pair(XF, XS); out["_X"] = (XF, XS)
    aF, AmF = LB.agg_chi2(AGGT, XF, XFFP); aS, AmS = LB.agg_chi2(AGGT, XS, XFFP)
    out["AGG"] = dict(chi2_F=aF, chi2_S0=aS, dchi2=aF - aS, A_F=AmF, A_S0=AmS)
    for nm, kw in (("ZHOLD", dict(zrule="hold")), ("ZREL", dict(zrule="rel")), ("KLOW", dict(klow=True)), ("BG", dict(bg=OTHER))):
        out[nm] = stats_pair(proj(M, "F", zg, **kw), proj(M, "S0", zg, **{k: v for k, v in kw.items() if k != "klow"}))
    out["KCUT"] = stats_pair(proj(Mcut, "F", zg), proj(Mcut, "S0", zg))
    return out

ROB = ["AGG", "ZHOLD", "ZREL", "KCUT", "KLOW", "BG"]
def klass(d, rob):
    if d >= 9 and min([d] + rob) >= 9: return "EXCLUDED"
    if d >= 4: return "TENSION"
    if d < 4 and max(rob) < 9: return "CONSISTENT"
    return "NOT DIAGNOSTIC"

# ================================================================== data-integrity K4 / K5 and the model
P("\nK4 / K5 (inputs)")
devD = max(abs(INP.D(s["a"]) / s["D"] - 1) for R_ in (RF, RS) for s in R_["snaps"].values())
check("K4a", "this code's growth D_X at every stored snapshot = stored D (<= 1e-5 rel)", devD <= 1e-5, f"max rel dev {devD:.2e}")
zi = min(RS["snaps"], key=lambda n: RS["snaps"][n]["a"])
devzi = float(np.max(np.abs(RF["snaps"][zi]["Pg"] / RS["snaps"][zi]["Pg"] - 1)))
check("K4b", "P_grav,F(z_i) = P_grav,S0(z_i) in every bin (<= 1e-6 rel): shared realisation", devzi <= 1e-6, f"max rel dev {devzi:.2e}")
M0 = build(RF, RS, vc=True)
devk = float(np.max(np.abs(M0.kbar / M0.ks[:M0.vc_bins] - 1)))
check("K4c", f"lattice mode-averaged |k| = stored k_b on the {M0.vc_bins} variance-corrected bins (<= 1e-5 rel)", devk <= 1e-5, f"max rel dev {devk:.2e}")
k4d = {n: float(np.max(np.abs(s["Pg"] / s["P"] - 1))) for n, s in RS["snaps"].items()}
check("K4d", "S0 max|P_grav/P - 1| per snapshot", True, ", ".join(f"{n} {v:.1e}" for n, v in k4d.items()), gating=False)
x = M0.x; Wb = M0.Wb
chisv = float(np.mean((x - 1) ** 2 / (2 / Wb))); mx = float((Wb * x).sum() / Wb.sum()); smx = math.sqrt(2 / Wb.sum())
k5 = (0.2 <= chisv <= 3.0) and abs(mx - 1) <= 3 * smx
check("K5", "z_i field = input linear spectrum x Gaussian realisation: reduced chi2_sv in [0.2, 3] and |mean x - 1| <= 3 sigma", k5,
      f"chi2_sv/n {chisv:.2f} (n {len(x)}), mode-weighted mean x {mx:.4f} +- {smx:.4f}; x_b " + " ".join(f"{v:.3f}" for v in x))
VC = bool(k5)
if not VC:
    P("  K5 FAILED -> frozen fallback: realisation-variance correction dropped (C_b = 1), raw measured spectra are the primary [FLAG]")
M = build(RF, RS, vc=VC); Mcut = build(RF, RS, vc=VC, kcut_div=8.0)
RES["model"] = dict(support=[M.k_lo, M.k_top, M.nsup], kcut_top=Mcut.k_top, vc=VC, vc_bins=M.vc_bins, C_b=M.C[:M.vc_bins].tolist(),
                    a_nodes=M.A.tolist(), a_i=M.a_i, R_lo=M.Rlo.tolist(), x_b=x.tolist(), W_b=Wb.tolist())
for kq in (0.1, 0.3, 0.5, 1.0):
    P(f"  measured P_grav,F/P_grav,S0 at k = {kq}: " + ", ".join(f"a {a:.3f}: {math.exp(np.interp(math.log(kq), np.log(M.ks), np.log(M.node['F'][i] / M.node['S0'][i]))):.4f}"
                                                         for i, a in enumerate(M.A)))

def run_pair_full(Mp, Mpc, label):
    t = members(Mp, Mpc)
    pr = t["_primary"]; rob = [t[m]["dchi2"] for m in ROB]
    P(f"\n  [{label}] PRIMARY (PR4 marged 8-400, 9 bands): chi2 F {pr['chi2_F']:.3f} (p {CHI2.sf(pr['chi2_F'], NDOF):.3f}), "
      f"S0 {pr['chi2_S0']:.3f} (p {CHI2.sf(pr['chi2_S0'], NDOF):.3f}) -> dchi2 {pr['dchi2']:+.4f}")
    P("    robustness dchi2: " + ", ".join(f"{m} {t[m]['dchi2']:+.4f}" for m in ROB) + f"   [AGG chi2 F {t['AGG']['chi2_F']:.2f} / S0 {t['AGG']['chi2_S0']:.2f}, {NAGG} bands]")
    return t, klass(pr["dchi2"], rob)

if MUTATE:
    P("\nMUTATE set (FROZEN B5)")
    # M1: F == S0
    M1 = build(RS, RS, vc=VC); M1c = build(RS, RS, vc=VC, kcut_div=8.0)
    t1 = members(M1, M1c); mx1 = max(abs(t1["_primary"]["dchi2"]), *[abs(t1[m]["dchi2"]) for m in ROB])
    check("M1", "F == S0 -> dchi2 = 0 (<= 1e-12) on the primary and every member", mx1 <= 1e-12, f"max |dchi2| {mx1:.1e}")
    # M2: +-10% amplitude injected on the P grid
    XS = proj(M, "S0"); cS = LB.pr4_chi2(D, XS); rep = {}
    okm2 = True
    for sgn in (+1, -1):
        f_ = 1 + 0.10 * sgn
        XF = LB.limber_X(lambda k, a, z: M.P("S0", k, a) * f_, INP, ZG, INP.Om)          # P_F = (1 +- 0.10) P_S0 on the P grid
        dpipe = LB.pr4_chi2(D, XF) - cS
        Bi = f_ * (LB.wsum(D["W"], XS) + LB.wsum(D["M"], XS)) - D["F"]; r_ = Bi - D["d"]
        dind = LB.qform(r_, D["Cinv"]) - cS
        rel_ = abs(dpipe - dind) / max(abs(dind), 1e-30); rep[f"{sgn:+d}"] = dict(pipeline=dpipe, independent=dind, rel=rel_)
        okm2 &= rel_ <= 1e-8
        P(f"    M2 {f_:.2f} x S0: pipeline dchi2 {dpipe:+.4f}, independent binned-vector {dind:+.4f} (rel {rel_:.1e})")
    sym = 0.5 * (rep["+1"]["pipeline"] + rep["-1"]["pipeline"])
    check("M2", "+-10% amplitude injection: pipeline = independent (<= 1e-8 rel) AND (dchi2+ + dchi2-)/2 >= 9", okm2 and sym >= 9,
          f"symmetric mean {sym:.2f}; S0 chi2 {cS:.3f}")
    RES["M2"] = dict(rep, symmetric_mean=sym)
    # M3: context, CFG596 P1 vs P0 (the KiDS-EXCLUDED candidate B), inherited inputs
    try:
        f1, f0 = PAIRS["P1"](); R1, R0 = LB.load_run(f1), LB.load_run(f0)
        INP_SAVE, OTHER_SAVE = INP, OTHER
        INP = LB.Inputs("inherited"); OTHER = LB.Inputs("native_cmb")
        Mp = LB.PairModel(R1, R0, INP, vc=True); Mpc = LB.PairModel(R1, R0, INP, vc=True, kcut_div=8.0)
        t3, c3 = run_pair_full(Mp, Mpc, "M3 context: CFG596 P1 vs P0 (KiDS-EXCLUDED candidate B)")
        RES["M3_context"] = dict(primary=t3["_primary"], members={m: t3[m] for m in ROB}, class_if_scored=c3)
        P(f"    M3 context class (no bite requirement): {c3}")
        INP, OTHER = INP_SAVE, OTHER_SAVE
    except SystemExit as ex:
        P(f"    M3 context unavailable: {ex}")
    RES["mutate_bites"] = CHECKS["M1"]["ok"] and CHECKS["M2"]["ok"]
    P(f"  MUTATE bites: {RES['mutate_bites']}")
else:
    P("\nPART B scoring (FROZEN B2-B3)")
    # coverage masks on the S0 primary
    kl, kt = M.k_lo, M.k_top
    masks = {"i_z<=1_support": lambda k, z: ((k >= kl) & (k <= kt)) * (z <= 1.0),
             "ii_z>1_support": lambda k, z: ((k >= kl) & (k <= kt)) * (z > 1.0),
             "iii_k<k_lo": lambda k, z: (k < kl) * 1.0, "iv_k>k_top": lambda k, z: (k > kt) * 1.0}
    XS_full, XSm = proj(M, "S0", masks=masks)
    wb = 1 / D["err"] ** 2; cov = {}
    for m, Xm in XSm.items():
        fb = LB.wsum(D["W"], Xm) / LB.wsum(D["W"], XS_full); cov[m] = dict(f_b=fb.tolist(), f=float((wb * fb).sum() / wb.sum()))
    P("  coverage of the S0 bandpowers (inverse-variance band summary): " + ", ".join(f"{m} {v['f']:.3f}" for m, v in cov.items()))
    RES["coverage"] = cov
    T, CL = run_pair_full(M, Mcut, "gravitating field (VERDICT)")
    pr = T["_primary"]; XF, XS = T["_X"]
    aF, sF = LB.pr4_amp(D, XF); aS, sS = LB.pr4_amp(D, XS)
    bF, bS = LB.pr4_binned(D, XF), LB.pr4_binned(D, XS)
    P(f"    best-fit amplitude (context): A_F {aF:.4f} +- {sF:.4f}, A_S0 {aS:.4f} +- {sS:.4f}")
    P("    per-band (B - d)/err  F: " + " ".join(f"{v:+.2f}" for v in (bF - D["d"]) / D["err"]) + "\n                       S0: " + " ".join(f"{v:+.2f}" for v in (bS - D["d"]) / D["err"]))
    P("    per-band B_F/B_S0: " + " ".join(f"{v:.4f}" for v in bF / bS))
    RES["primary"] = dict(pr, p_F=float(CHI2.sf(pr["chi2_F"], NDOF)), p_S0=float(CHI2.sf(pr["chi2_S0"], NDOF)), ndof=NDOF, A_F=[aF, sF], A_S0=[aS, sS],
                          resid_F=((bF - D["d"]) / D["err"]).tolist(), resid_S0=((bS - D["d"]) / D["err"]).tolist(), ratio_b=(bF / bS).tolist(),
                          B_F=bF.tolist(), B_S0=bS.tolist(), d=D["d"].tolist())
    RES["members"] = {m: T[m] for m in ROB}
    for m in ("AGG", "BG", "ZHOLD", "ZREL", "KCUT", "KLOW"):
        if m == "AGG":
            RES["members"][m]["p_F"] = float(CHI2.sf(T[m]["chi2_F"], NAGG)); RES["members"][m]["p_S0"] = float(CHI2.sf(T[m]["chi2_S0"], NAGG))
    # context: particle field F, raw (no variance correction)
    Mpart = build(RF, RS, vc=VC, field_F="P")
    XFp = proj(Mpart, "F"); cp = LB.pr4_chi2(D, XFp)
    Mraw = build(RF, RS, vc=False); XFr, XSr = proj(Mraw, "F"), proj(Mraw, "S0"); sr = stats_pair(XFr, XSr)
    P(f"  context: particle-field F dchi2 {cp - pr['chi2_S0']:+.4f} (chi2 {cp:.3f}); raw spectra (C_b = 1): chi2 F {sr['chi2_F']:.3f}, S0 {sr['chi2_S0']:.3f}, dchi2 {sr['dchi2']:+.4f}")
    RES["context"] = dict(particle_field_F=dict(chi2_F=cp, dchi2=cp - pr["chi2_S0"]), raw_no_variance_correction=sr)

    P("\nK tests")
    # K1 F == S0 through the full member set
    M1 = build(RS, RS, vc=VC); M1c = build(RS, RS, vc=VC, kcut_div=8.0)
    t1 = members(M1, M1c); mx1 = max(abs(t1["_primary"]["dchi2"]), *[abs(t1[m]["dchi2"]) for m in ROB])
    check("K1", "F == S0 (S0 JSON as both arms) -> dchi2 = 0 (<= 1e-12) on the primary and every member", mx1 <= 1e-12, f"max |dchi2| {mx1:.1e}")
    # K2 CFG649 emulation on CFG596 P1 vs P0 through this code path
    try:
        f1, f0 = PAIRS["P1"](); R1, R0 = LB.load_run(f1), LB.load_run(f0); IH = LB.Inputs("inherited")
        late = sorted([n for n in R0["snaps"] if n in R1["snaps"] and R0["snaps"][n]["a"] >= 0.5 - 1e-9], key=lambda n: R0["snaps"][n]["a"])
        AN = np.array([R0["snaps"][n]["a"] for n in late]); AZI = min(s["a"] for s in R0["snaps"].values())
        kb = R0["snaps"][late[0]]["k"]; sup = kb <= math.pi * int(R0["meta"]["np"]) / (4 * float(R0["meta"]["L"])) + 1e-9; KS = kb[sup]
        PSN = np.array([R0["snaps"][n]["Pg"][sup] for n in late]); RN = np.array([R1["snaps"][n]["Pg"][sup] / R0["snaps"][n]["Pg"][sup] for n in late])
        KLO, KHI = KS[0], KS[-1]; D1 = IH.D(0.5); NK = PSN[0] / (IH.Plin0(KS) * D1 ** 2)
        mh = KS >= KHI / 2
        def ia(vals, a):
            a = min(max(a, AN[0]), AN[-1]); j = int(np.clip(np.searchsorted(AN, a) - 1, 0, len(AN) - 2)); t = (a - AN[j]) / (AN[j + 1] - AN[j])
            return vals[j] * (1 - t) + vals[j + 1] * t
        def base1(k, a, z):
            D2 = IH.D(a) ** 2; v = IH.Plin0(k) * D2
            pn = np.exp(ia(np.log(PSN), a)) if z <= 1.0 else IH.Plin0(KS) * D2 * (1 + (NK - 1) * (D2 / D1 ** 2))
            ins = (k >= KLO) & (k <= KHI); v[ins] = np.exp(np.interp(np.log(k[ins]), np.log(KS), np.log(pn)))
            hi = k > KHI
            if hi.any():
                sl = np.polyfit(np.log(KS[mh]), np.log(pn[mh]), 1)[0]; v[hi] = pn[-1] * (k[hi] / KHI) ** sl
            return v
        def ratio(k, a, z):
            def at(aa):
                r = ia(RN, aa); v = np.ones_like(k); ins = (k >= KLO) & (k <= KHI); v[ins] = np.interp(np.log(k[ins]), np.log(KS), r); v[k > KHI] = r[-1]
                return v
            if z <= 1.0: return at(a)
            return 1.0 + (at(AN[0]) - 1.0) * max(0.0, (a - AZI) / (AN[0] - AZI))
        zg49 = np.concatenate([np.geomspace(1e-3, 1.0, 300), np.geomspace(1.0, 50.0, 401)[1:]])
        XSe = LB.limber_X(base1, IH, zg49, IH.Om, Lmin=8, Lmax=2048)
        XFe = LB.limber_X(lambda k, a, z: base1(k, a, z) * ratio(k, a, z), IH, zg49, IH.Om, Lmin=8, Lmax=2048)
        Ab = np.array([XFe[lo:hi + 1].mean() / XSe[lo:hi + 1].mean() for lo, hi, A_, sA, fid in AGGT["8-400"]])
        wA = np.array([1 / sA ** 2 for lo, hi, A_, sA, fid in AGGT["8-400"]]); dA = float((wA * Ab).sum() / wA.sum() - 1)
        st = json.load(open(os.path.join(LB.CFG, "CFG649_cmb_safety", "cfg649_cfg596_P1_canonical.json")))["B_grav"]["canonical"]["8-400"]["dA"]
        check("K2", "CFG649 canonical (base-1, Z-b, K-a) on CFG596 P1 vs P0 through this code path = stored dA(8-400) (<= 5e-4 abs)",
              abs(dA - st) <= 5e-4, f"this path {dA:+.5f} vs stored {st:+.5f} (|d| {abs(dA - st):.1e})")
        RES["K2"] = dict(this_path=dA, stored=st)
    except SystemExit as ex:
        check("K2", "CFG649 reproduction", False, f"inputs unavailable: {ex}")
    # K3 likelihood / normalisation
    fidb = LB.wsum(D["W"], XFFP); d3a = float(np.max(np.abs(fidb / (D["d"] / D["ahat"]) - 1)))
    check("K3a", "PR4 windows on FFP10 PP vs PP_b/Ahat_b (Ahat printed to 3 decimals)", d3a <= 5e-3, f"max rel dev {d3a:.2e}", gating=False)
    corr = LB.wsum(D["M"], XFFP); d3b = float(np.max(np.abs(corr / D["F"] - 1)))
    check("K3b", "linear-correction fiducial values = sum_L M_b(L) X_L^FFP10 (<= 2% per band)", d3b <= 0.02, f"max rel dev {d3b:.2e}")
    P("  [N/A] K3c: no published chi2 exists for the on-disk fiducial model file (FFP10); K3e substitutes (frozen)")
    try:
        cj = json.load(open(os.path.join(LB.HERE, "cfg917_camb_ktests.json")))
        check("K3d", "Limber normalisation vs CAMB linear (native), PR4-binned, <= 3% every band (cfg917_camb_ktests.json)", cj["K3d"]["ok"],
              "max |dev| " + f"{max(abs(v) for v in cj['K3d']['dev']):.4f}")
        check("K3e", "package unit test -2 lnL = 8.368 reproduced <= 0.15 (cfg917_camb_ktests.json)", cj["K3e"]["ok"], f"{cj['K3e']['chi2']:.4f}")
    except FileNotFoundError:
        check("K3d", "cfg917_camb_ktests.json", False, "MISSING"); check("K3e", "cfg917_camb_ktests.json", False, "MISSING")
    # K6 grid convergence (doubled z nodes) on every reported chi2
    t2 = members(M, Mcut, zg=ZG2); dd = []
    for m in ["_primary"] + ROB:
        for q in ("chi2_F", "chi2_S0"): dd.append(abs(t2[m][q] - T[m][q]))
    check("K6", "doubling both z-node counts changes every reported chi2 by <= 0.01", max(dd) <= 0.01, f"max |change| {max(dd):.1e}")

    # ---------------- class
    mfn = os.path.join(LB.HERE, f"cfg917_{ARGS.pair}_MUTATE.json")
    bites = json.load(open(mfn)).get("mutate_bites") if os.path.exists(mfn) else None
    gate_ok = all(v["ok"] for v in CHECKS.values() if v["gating"])
    cls = CL
    flags = []
    if not gate_ok: cls = "NOT DIAGNOSTIC"; flags.append("gating K test failed: " + ", ".join(k for k, v in CHECKS.items() if v["gating"] and not v["ok"]))
    if bites is None: cls = "NOT DIAGNOSTIC"; flags.append("PROVISIONAL: MUTATE output missing (run CFG917_MUTATE=1 first)")
    elif not bites: cls = "NOT DIAGNOSTIC"; flags.append("MUTATE does not bite")
    if RES["primary"]["p_F"] < 0.01: flags.append("ABSOLUTE MISFIT (p_F < 0.01)")
    if not VC: flags.append("K5 fallback: variance correction dropped")
    RES["class_rule_value"] = CL; RES["class"] = cls; RES["flags"] = flags; RES["mutate_bites"] = bites
    rob = [T[m]["dchi2"] for m in ROB]
    P(f"\nCLASS ({ARGS.pair}, {FOOT} footing, {KIND} inputs): {cls}   [dchi2 {pr['dchi2']:+.4f}; robustness min {min(rob):+.4f}, max {max(rob):+.4f}]"
      + (("; flags: " + "; ".join(flags)) if flags else ""))
    P("  A CONSISTENT class does not mean the data favour the framework. Part A (CFG649 checklist) is reported separately.")

RES["checks"] = CHECKS; RES["runtime_s"] = time.time() - T0
try:
    import resource; RES["maxrss_gb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
except Exception:
    pass
P(f"\nruntime {RES['runtime_s']:.0f} s; maxrss {RES.get('maxrss_gb', 0):.2f} GB. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
def _clean(o):
    if isinstance(o, dict): return {str(k): _clean(v) for k, v in o.items() if k != "_X"}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return o
base = os.path.join(LB.HERE, f"cfg917_{ARGS.pair}" + ("_MUTATE" if MUTATE else ""))
json.dump(_clean(RES), open(base + ".json", "w"), indent=1)
open(base + ".out", "w").write("\n".join(OUT) + "\n")
