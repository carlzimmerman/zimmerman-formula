#!/usr/bin/env python3
"""X53_outer_lensing_law_vs_halos: KiDS-1000 isolated-lens Delta Sigma (B21 Fig. 3) -- the law as fundamental (L) against
route E's a0-floor Burkert cold dark energy halos truncated at R200 (H), each with and without CFG805's two-halo term.

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (61b837fcd4, committed alone before any script or number).
F2's data/inventory machinery (sections 1 and 4) and CFG805's two-halo code are executed read-only in namespaces.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x53_outer_lensing.py                 -> .out, _results.json
    X53_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x53_outer_lensing.py    -> _MUTATE (no truncation; law mu Newtonian)
kappa = 1/2 FITTED; footings never pooled; cold dark energy is not matter; no dark-matter particle; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, time, resource, contextlib
import numpy as np
from scipy.optimize import brentq, minimize_scalar, lsq_linear
from scipy.integrate import quad
from scipy import stats

T0 = time.time()
MUT = os.environ.get("X53_MUTATE") == "1"
SFX = "_MUTATE" if MUT else ""
HERE = '/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/CSM1_consistent_core_switch/calibration/run_006_challenge/x53_off_shpS9_L2.5090595510216196_corrected_own'
REB = '/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22'
REPO = os.path.dirname(REB)
OUT, CHK = [], {}
RES = dict(lane="X53_outer_lensing_law_vs_halos", criteria="61b837fcd4", mutate=MUT)
np.seterr(all="ignore")


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, val):
    CHK[name] = bool(ok); P(f"  {name}: {'PASS' if ok else 'FAIL'}  ({val})")


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


# ============================================================ F2 machinery (read-only: sections 1 and 4)
F2SRC = os.path.join(REB, "F2_outer_lensing", "f2_outer_lensing.py")
TF = open(F2SRC).read()
s1 = TF[:TF.index("# ============================================================================ 2. K0")]
s4 = TF[TF.index("# ============================================================================ 4. lens inventory"):
        TF.index("# ============================================================================ 5. Track A")]
NF = {"__file__": F2SRC, "__name__": "f2_ro"}
argv0 = sys.argv; sys.argv = [F2SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s1 + "\n" + s4, F2SRC, "exec"), NF)
sys.argv = argv0
AQ, C, R, Y = NF["AQ"], NF["C"], NF["R"], NF["Y"]
IDX_ALL, IDX_PRIM, INV, LMG, RGRID_PC = NF["IDX_ALL"], NF["IDX_PRIM"], NF["INV"], NF["LMG"], NF["RGRID_PC"]
data_native, stack_model, sel_of, chi_flat = NF["data_native"], NF["stack_model"], NF["sel_of"], NF["chi_flat"]
Gpc, a0u, A0 = NF["Gpc"], NF["a0u"], NF["A0"]
FOOTS = ("canonical", "alt")
H_NAT, OM_NAT = 0.679, NF["OM_NAT"]
CENTRAL0 = dict(h=H_NAT, dMs=0.0, dcold=0.0, fhot=0.5, ye="zero", pz=1.0)          # F2 L4 (y_e = 0)
if MUT:
    AQ.nu_simple = lambda y: np.ones_like(np.asarray(y, float))                   # MUTATE: law mu Newtonian
Rn, Yn, FN = data_native(H_NAT); Cn = C * FN * FN
P(f"X53_outer_lensing_law_vs_halos{'  [MUTATE: no truncation (100 R200); law nu = 1]' if MUT else ''}   criteria 61b837fcd4")
P("kappa = 1/2 FITTED; footings never pooled; (L) isolated AQUAL mu = x/(1+x); (H) route E Newtonian + a0-floor Burkert cold dark energy halos")
P(f"F2 machinery loaded read-only; native factor f = {FN:.4f} [{time.time() - T0:.0f} s]")

# ============================================================ step 0 (stop rule) read from x53_step0
S0 = json.load(open('/Users/carlzimmerman/new_physics/zimmerman-formula/rebuild_2026_10_22/X53_outer_lensing_law_vs_halos/x53_step0_results.json'))
for k, v in S0["rows"].items():
    P(f"  step0 {k:30s} {v['value']:+9.2f} (frozen {v['frozen']:+.2f}): {'PASS' if v['pass_'] else 'FAIL'}")
check("K0_step0", S0["step0_pass"], "x53_step0_results.json")

# ============================================================ route-E halo pieces
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))
F3 = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]
BG = {t: dict(a=EM1J["rows"][t]["R1"]["a"], b=EM1J["rows"][t]["R1"]["b"], h=F3[t]["params"]["h"]) for t in ("A_c2b_refit", "B_cfg886_bg")}
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
SCT = sorted((math.log10(float(k)), math.log10(v[0])) for k, v in X43J["sigma_coll_table"].items())
SC_LM, SC_LS = np.array([a for a, _ in SCT]), np.array([b for _, b in SCT])
def sigma_coll(M):                     # Msun/pc^2; log-log interpolation of X43's committed table, linear extrapolation outside
    l = math.log10(M)
    if l < SC_LM[0]:
        s = (SC_LS[1] - SC_LS[0]) / (SC_LM[1] - SC_LM[0]); return 10 ** (SC_LS[0] + s * (l - SC_LM[0]))
    if l > SC_LM[-1]:
        s = (SC_LS[-1] - SC_LS[-2]) / (SC_LM[-1] - SC_LM[-2]); return 10 ** (SC_LS[-1] + s * (l - SC_LM[-1]))
    return 10 ** float(np.interp(l, SC_LM, SC_LS))
B1 = 3 * math.log(2) - math.pi / 2
X48J = json.load(open(os.path.join(REB, "X48_native_cf_zoom", "x48_analyze_results_ng48.json")))
CF48 = sorted((math.log10(float(k)), v) for k, v in X48J["cf_by_mass"].items() if v is not None)
CF48_L, CF48_C = np.array([a for a, _ in CF48]), np.array([b for _, b in CF48])
def eta_of(M, cfmode):
    cf = float(np.interp(math.log10(M), [12.0, 13.0, 14.0], [3.994077644910099, 2.823781842637895, 2.5090595510216196]))
    return 4.0 / (3.0 * B1) * cf ** 1.25
def B(x):
    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)
SAT = {"n": 0}
def solve_r0(Mtot, Rout, Sig):        # X38 A1: compact root; saturation counted
    lm = lambda lr: math.log(math.pi * Sig * math.exp(2 * lr) * float(B(Rout / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(Rout * 1e-6), math.log(Rout * 1e3)), method="bounded", options={"xatol": 1e-10})
    lpk = float(pk.x)
    if lm(lpk) < math.log(Mtot):
        SAT["n"] += 1; return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(Mtot), math.log(Rout * 1e-7), lpk, xtol=1e-14))
SIGA0 = {f: a0u(f) / (2 * math.pi * Gpc) for f in FOOTS}       # Msun/pc^2
P(f"  Sigma_a0 = a0/(2 pi G): canonical {SIGA0['canonical']:.1f}, alt {SIGA0['alt']:.1f} Msun/pc^2 (X38: 106.9 / 129.2)")
P(f"  EM1 R1 relation: bg A a {BG['A_c2b_refit']['a']} b {BG['A_c2b_refit']['b']} h {BG['A_c2b_refit']['h']:.4f}; bg B a {BG['B_cfg886_bg']['a']} b {BG['B_cfg886_bg']['b']}")
XOVER = {}
for f in FOOTS:
    for cm in ("cf4", "x48"):
        XOVER[(f, cm)] = brentq(lambda l: eta_of(10 ** l, cm) * sigma_coll(10 ** l) - SIGA0[f], 8.0, 16.0)
    P(f"  crossover eta Sigma_coll = Sigma_a0 [{f}]: c_f 4 -> 10^{XOVER[(f, 'cf4')]:.2f}; X48 ng48 c_f(M) -> 10^{XOVER[(f, 'x48')]:.2f} Msun  (X43: 12.09 / 12.43)")
RES["crossover_logM"] = {f"{k[0]}|{k[1]}": v for k, v in XOVER.items()}
# K_B
r0t, Rt, St = 1000.0, 10000.0, SIGA0["canonical"]
quadM = quad(lambda r: 4 * math.pi * r * r * (St / r0t) * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t)), 0, Rt, epsabs=0, epsrel=1e-12, limit=400)[0]
cfM = math.pi * St * r0t ** 2 * float(B(Rt / r0t))
check("K_B_burkert_closed_form", abs(cfM / quadM - 1) < 1e-6, f"{cfM / quadM - 1:+.1e}")


def halo_setup(foot, logMbrel, cfg_h):
    """M200 [Msun], R200 [pc], r0 [pc], Sigma_core [Msun/pc^2], above-floor flag."""
    bg = BG[cfg_h["bg"]]
    lM200 = bg["a"] + bg["b"] * (logMbrel - 10.0); M200 = 10 ** lM200
    Ez2 = 1.0 if cfg_h["zR200"] is None else OM_NAT * (1 + cfg_h["zR200"]) ** 3 + 1 - OM_NAT
    rhoc = 2.775e11 * bg["h"] ** 2 * Ez2 / 1e18                                  # Msun/pc^3
    R200 = (3 * M200 / (4 * math.pi * 200 * rhoc)) ** (1 / 3)
    sc = eta_of(M200, cfg_h["cf"]) * sigma_coll(M200)
    Sig = max(SIGA0[foot], sc)
    return LENS_RECORD(foot, M200, R200, solve_r0(M200, R200, Sig), Sig, sc, SIGA0[foot])


def mass_H(foot, lm, h, cfg_h, halo=True):
    """M(<r) on RGRID_PC for one lens of native log M* lm (F2 inventory, Newtonian) + truncated route-E halo."""
    lm70 = lm - 2 * np.log10(0.70 / h)
    lmc = lm + (-0.69 * lm70 + 6.63)
    Ms, Mc = 10 ** lm, 10 ** lmc; Mhot = 0.5 * Ms
    Mb = Ms + Mc + Mhot * np.minimum(1.0, (RGRID_PC / 1e5) ** 3)
    if not halo:
        return Mb, None
    M200, R200, r0, Sig, above = halo_setup(foot, math.log10(Ms + Mc), cfg_h)
    rcut = 100 * R200 if MUT else R200
    Mh = math.pi * Sig * r0 ** 2 * B(np.minimum(RGRID_PC, rcut) / r0)
    return LF_M(Mb, Mh, RGRID_PC, Gpc, a0u(foot), "lensing", above), (M200, R200, Sig, above)


def stack_H(foot, cfg_h, halo=True):
    """lens-weighted stacked Delta Sigma at native radii (as F2's stack_model), plus per-lens halo meta per bin."""
    h = H_NAT; out = np.empty((4, 15)); meta = {}
    for b in range(4):
        tab = np.empty((len(LMG), 15)); mt = np.empty((len(LMG), 3))
        for gi, lm in enumerate(LMG):
            M, mm = mass_H(foot, lm, h, cfg_h, halo)
            tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, M, "linear" if (halo and LAST["law"]) else "const")
            mt[gi] = (math.log10(mm[0]), mm[1], float(mm[3])) if mm else (np.nan, np.nan, 0.0)
        lMs_nat = INV[b]["logMs70"] + 2 * np.log10(0.70 / h) + 2 * np.log10(INV[b]["qDA"])
        w = INV[b]["w"]
        vals = np.array([np.interp(lMs_nat, LMG, tab[:, i]) for i in range(15)])
        out[b] = vals @ w / w.sum()
        if halo:
            lM200 = np.interp(lMs_nat, LMG, mt[:, 0]); R200 = np.interp(lMs_nat, LMG, mt[:, 1]); ab = np.interp(lMs_nat, LMG, mt[:, 2]) > 0.5
            o = np.argsort(R200); cw = np.cumsum(w[o])
            meta[b] = dict(R200_med_kpc=float(R200[o][np.searchsorted(cw, 0.5 * cw[-1])] / 1e3),
                           lM200_wmean=float(np.sum(w * lM200) / w.sum()), lM200_max=float(lM200.max()),
                           frac_w_above_crossover=float(w[ab].sum() / w.sum()))
    return out, meta


# ============================================================ CFG805 two-halo template (read-only exec of its own code)
C5SRC = os.path.join(REPO, "campaign_fresh_gravity", "CFG805_two_halo_t1x", "cfg805.py")
T5 = open(C5SRC).read()
c5 = T5[T5.index("# --- T1x P_grav"):T5.index("# --- data")]
jl = [l for l in c5.splitlines() if l.startswith("J = json.load(open(")]
assert len(jl) == 1
T1X = os.path.join(REPO, "..", "_external_data", "cfg650_work", "T1x", "cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json")
c5 = c5.replace(jl[0], "J = json.load(open(T1X_PATH))")
N5 = {"json": json, "math": math, "np": np, "quad": quad, "MUT": False, "T1X_PATH": T1X, "P": lambda s="": OUT.append("  [cfg805 code] " + str(s))}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(c5, C5SRC, "exec"), N5)
esd2h = N5["esd2h"]
REX = [0.343, 0.442, 0.433, 0.429]
T2 = np.array(TEMPLATE_CACHE, dtype=float)                           # CFG805's own template (B21 radius labels)
P(f"  CFG805 two-halo template rebuilt (b=1, bin 2 at 0.5/1/2.6 Mpc: " + " / ".join(f"{np.interp(x, R[1], T2[1]):.2f}" for x in (0.5, 1.0, 2.6)) + " Msun/pc^2; CFG805: -0.53 / 1.80 / 1.57)")
check("K_2h_template_matches_CFG805", all(abs(np.interp(x, R[1], T2[1]) - v) < 0.006 for x, v in ((0.5, -0.53), (1.0, 1.80), (2.6, 1.57))), "3 printed values")
T2n = T2 * FN
P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")


# ============================================================ fitting / statistics
def fit(m, idx, use2h=True, T=None, bmax=np.inf):
    s = sel_of(idx); Cs = Cn[np.ix_(s, s)]; Lc = np.linalg.cholesky(Cs)
    r0 = np.linalg.solve(Lc, (Yn - m).ravel()[s])
    bb = np.zeros(4)
    if use2h:
        TT = T2n if T is None else T
        A = np.zeros((60, 4))
        for b in range(4):
            A[15 * b:15 * b + 15, b] = TT[b]
        A = np.linalg.solve(Lc, A[s])
        bb = lsq_linear(A, r0, bounds=(0.0, bmax)).x
    mf = m + (bb[:, None] * (T2n if T is None else T))
    r = (Yn - mf).ravel()[s]
    x2 = float(r @ np.linalg.solve(Cs, r))
    per = []
    for b in range(4):
        sb = np.array(idx) + 15 * b; rb = (Yn - mf).ravel()[sb]
        per.append(float(rb @ np.linalg.solve(Cn[np.ix_(sb, sb)], rb)))
    return dict(chi2=x2, n=len(s), b=bb.tolist(), per_bin=per, p=float(stats.chi2.sf(x2, len(s) - (4 if use2h else 0)))), mf


def cls_of(d):
    return "LAW" if d >= 9 else ("HALOS" if d <= -9 else "NOT DIAGNOSTIC")


NEWT = {}
FT = {}
H_PRIMARY = dict(bg="A_c2b_refit", cf="x48", zR200=None)
for foot in FOOTS:
    P(f"\n=== [{foot}]  a0 {A0[foot]:.4e} m/s^2")
    mL = stack_model(foot, Rn, CENTRAL0)
    SAT["n"] = 0
    mH, meta = stack_H(foot, H_PRIMARY)
    satH = SAT["n"]; SAT["n"] = 0
    mN, _ = stack_H(foot, H_PRIMARY, halo=False)
    NEWT[foot] = mN
    for b in range(4):
        P(f"  bin {b + 1}: <log M200> {meta[b]['lM200_wmean']:.2f} (max {meta[b]['lM200_max']:.2f}); median R200 {meta[b]['R200_med_kpc']:.0f} kpc; "
          f"lens weight above the c_f=4 crossover {meta[b]['frac_w_above_crossover']:.3f}")
    P(f"  saturated halo solves (grid points): {satH}")
    fo = dict(meta=meta, saturated=satH)
    # K_L: F2 L4 reproduced
    rL_all, _ = fit(mL, IDX_ALL, use2h=False)
    refL = {"canonical": 160.70164004429935, "alt": 127.59993186489119}[foot]
    check(f"K_L_F2_L4_reproduced_{foot}", abs(rL_all["chi2"] - refL) < 0.05, f"chi2_all {rL_all['chi2']:.3f} vs F2 {refL:.3f}")
    # K_N: phantom present at the last radius
    ratN = mL[:, -1] / mN[:, -1]
    check(f"K_N_phantom_present_{foot}", bool(np.all(ratN > 3)), f"L / Newtonian baryons at 2.6 Mpc: {np.round(ratN, 2).tolist()}")
    # K_T: truncation (test lens native log M* 10.0)
    lmT = 10.0; Mt, mm = mass_H(foot, lmT, H_NAT, H_PRIMARY)
    Rtest = 2.6e6; dsT = float(AQ.delta_sigma(np.array([Rtest]), RGRID_PC, Mt, "const")[0])
    Mtot = 10 ** lmT * 1.5 + 10 ** (lmT + (-0.69 * (lmT - 2 * np.log10(0.70 / H_NAT)) + 6.63)) + mm[0]
    devT = dsT / (Mtot / (math.pi * Rtest ** 2)) - 1
    check(f"K_T_truncation_{foot}", mm[1] < 1e6 and abs(devT) < 0.01, f"R200 {mm[1] / 1e3:.0f} kpc; DS(2.6 Mpc) / point mass - 1 = {devT:+.2e}")
    models = {}
    for lab, idx in (("primary", IDX_PRIM), ("all", IDX_ALL)):
        r = {}
        r["L"], _ = fit(mL, idx, False); r["H"], _ = fit(mH, idx, False)
        r["L2H"], mfL = fit(mL, idx, True); r["H2H"], mfH = fit(mH, idx, True)
        r["dchi2_H_minus_L"] = r["H"]["chi2"] - r["L"]["chi2"]
        r["dchi2_H2H_minus_L2H"] = r["H2H"]["chi2"] - r["L2H"]["chi2"]
        r["per_bin_dchi2_noH2"] = [r["H"]["per_bin"][b] - r["L"]["per_bin"][b] for b in range(4)]
        r["per_bin_dchi2_2h"] = [r["H2H"]["per_bin"][b] - r["L2H"]["per_bin"][b] for b in range(4)]
        models[lab] = (mfL, mfH)
        fo[lab] = r
        P(f"  [{lab}, c_f 4] n {r['L']['n']}:  L {r['L']['chi2']:.1f}  H {r['H']['chi2']:.1f}  dchi2(H-L) {r['dchi2_H_minus_L']:+.1f}   |   "
          f"L2H {r['L2H']['chi2']:.1f} (b {np.round(r['L2H']['b'], 2).tolist()})  H2H {r['H2H']['chi2']:.1f} (b {np.round(r['H2H']['b'], 2).tolist()})  "
          f"dchi2(H2H-L2H) {r['dchi2_H2H_minus_L2H']:+.1f}")
        P(f"      per bin dchi2 (block-diagonal) no 2h {np.round(r['per_bin_dchi2_noH2'], 1).tolist()}; with 2h {np.round(r['per_bin_dchi2_2h'], 1).tolist()}; "
          f"p: L {r['L']['p']:.1e} H {r['H']['p']:.1e} L2H {r['L2H']['p']:.1e} H2H {r['H2H']['p']:.1e}")
    D0 = fo["all"]["dchi2_H2H_minus_L2H"]; c0 = cls_of(D0)
    # S1: exclusion at each bin's median R200 (both models)
    T2s1 = np.array([esd2h(R[b], meta[b]["R200_med_kpc"] / 1e3) for b in range(4)]) * FN
    a1, _ = fit(mL, IDX_ALL, True, T=T2s1); b1, _ = fit(mH, IDX_ALL, True, T=T2s1); D1 = b1["chi2"] - a1["chi2"]
    # S2: b_eff <= 1
    a2, _ = fit(mL, IDX_ALL, True, bmax=1.0); b2, _ = fit(mH, IDX_ALL, True, bmax=1.0); D2 = b2["chi2"] - a2["chi2"]
    P(f"  S1 (2h exclusion at median R200 {[round(meta[b]['R200_med_kpc']) for b in range(4)]} kpc): L2H {a1['chi2']:.1f} H2H {b1['chi2']:.1f} dchi2 {D1:+.1f} -> {cls_of(D1)}")
    P(f"  S2 (b_eff <= 1): L2H {a2['chi2']:.1f} (b {np.round(a2['b'], 2).tolist()}) H2H {b2['chi2']:.1f} (b {np.round(b2['b'], 2).tolist()}) dchi2 {D2:+.1f} -> {cls_of(D2)}")
    dom = (cls_of(D1) != c0) or (cls_of(D2) != c0)
    vf = "NOT DIAGNOSTIC" if (c0 == "NOT DIAGNOSTIC" or dom) else c0
    fo["S1"] = dict(L2H=a1, H2H=b1, dchi2=D1, cls=cls_of(D1)); fo["S2"] = dict(L2H=a2, H2H=b2, dchi2=D2, cls=cls_of(D2))
    fo["class_raw"] = c0; fo["systematics_dominate"] = dom; fo["verdict"] = vf
    P(f"  CLASS [{foot}] (all radii, with 2h, c_f 4): dchi2 {D0:+.1f} -> {c0}; systematics dominate: {dom} -> {('OUTER LENSING DISCRIMINATES: ' + vf) if vf in ('LAW', 'HALOS') else vf}")
    # ---------------- reported: variants (c_f X48; R200 at z_eff; bg B)
    var = {}
    zeff = float(np.mean([INV[b]["zeff"] for b in range(4)]))
    for vlab, cfg_h in ():
        mV, metaV = stack_H(foot, cfg_h); SAT["n"] = 0
        o = {}
        for lab, idx in (("primary", IDX_PRIM), ("all", IDX_ALL)):
            hv, _ = fit(mV, idx, False); hv2, _ = fit(mV, idx, True)
            o[lab] = dict(H=hv["chi2"], H2H=hv2["chi2"], dchi2_noH2=hv["chi2"] - fo[lab]["L"]["chi2"], dchi2_2h=hv2["chi2"] - fo[lab]["L2H"]["chi2"], b=hv2["b"])
        o["frac_above_crossover"] = [metaV[b]["frac_w_above_crossover"] for b in range(4)]
        var[vlab] = o
        P(f"  (reported) {vlab}: dchi2(H-L) primary {o['primary']['dchi2_noH2']:+.1f} all {o['all']['dchi2_noH2']:+.1f}; dchi2(H2H-L2H) primary {o['primary']['dchi2_2h']:+.1f} "
          f"all {o['all']['dchi2_2h']:+.1f}; weight above crossover {np.round(o['frac_above_crossover'], 3).tolist()}")
    fo["variants"] = var
    # ---------------- reported: where L and H differ by > 1 sigma
    sig = np.sqrt(np.diag(Cn)).reshape(4, 15)
    mfL, mfH = models["all"]
    diff = {}
    for lab, a_, b_ in (("no 2h", mL, mH), ("with 2h (fitted b)", mfL, mfH)):
        z_ = np.abs(a_ - b_) / sig
        first = []
        for b in range(4):
            ii = np.where(z_[b] > 1)[0]
            first.append(float(Rn[b][ii[0]]) if ii.size else None)
        diff[lab] = dict(first_R_Mpc=first, z=z_.tolist(), ratio_L_over_H=(a_ / b_).tolist())
        P(f"  (reported) {lab}: first native R (Mpc) with |L - H| > 1 sigma per bin: {[None if v is None else round(v, 3) for v in first]}; "
          f"|L-H|/sigma at 2.6 Mpc {np.round(z_[:, -1], 2).tolist()}; L/H at 0.035 / 0.31 / 2.6 Mpc bin 2: "
          f"{a_[1, 0] / b_[1, 0]:.2f} / {np.interp(0.31, Rn[1], a_[1] / b_[1]):.2f} / {a_[1, -1] / b_[1, -1]:.2f}")
    fo["differ"] = diff
    P("  (reported) stacked Delta Sigma bin 2 (native Msun/pc^2) at R " + str(np.round(Rn[1], 3).tolist()))
    P("     data " + str(np.round(Yn[1], 2).tolist()))
    P("     sigma " + str(np.round(sig[1], 2).tolist()))
    P("     L    " + str(np.round(mL[1], 2).tolist()))
    P("     H    " + str(np.round(mH[1], 2).tolist()))
    P("     Newtonian baryons " + str(np.round(mN[1], 2).tolist()))
    fo["profiles"] = dict(R=Rn.tolist(), data=Yn.tolist(), sigma=sig.tolist(), L=mL.tolist(), H=mH.tolist(), Newt=mN.tolist(), L2H=mfL.tolist(), H2H=mfH.tolist())
    # ---------------- reported: can the two-halo term mimic either model?  and survey forecast
    s = sel_of(IDX_ALL); Ci = np.linalg.inv(Cn[np.ix_(s, s)]); Lc = np.linalg.cholesky(Cn[np.ix_(s, s)])
    A = np.zeros((60, 4))
    for b in range(4):
        A[15 * b:15 * b + 15, b] = T2n[b]
    Aw = np.linalg.solve(Lc, A[s])
    mim = {}
    for lab, d in (("H + b T2 mimics L", (mL - mH).ravel()[s]), ("L + b T2 mimics H", (mH - mL).ravel()[s])):
        dw = np.linalg.solve(Lc, d); e0 = float(dw @ dw)
        bb = lsq_linear(Aw, dw, bounds=(0.0, np.inf)).x; res = float(np.sum((dw - Aw @ bb) ** 2))
        mim[lab] = dict(dchi2_expected=e0, residual=res, absorbed=1 - res / max(e0, 1e-300), b=bb.tolist())
        P(f"  (reported) {lab}: expected dchi2 {e0:.1f}; after b T2 (b {np.round(bb, 2).tolist()}) residual {res:.1f}; absorbed {100 * (1 - res / max(e0, 1e-300)):.0f} %")
    fc = {}
    for lab, truth, alt_m in (("truth L2H, fit H2H", mfL, mH), ("truth H2H, fit L2H", mfH, mL)):
        dw = np.linalg.solve(Lc, (truth - alt_m).ravel()[s]); bb = lsq_linear(Aw, dw, bounds=(0.0, np.inf)).x
        e = float(np.sum((dw - Aw @ bb) ** 2))
        fc[lab] = dict(dchi2_expected=e, N_factor_for_25=(25.0 / e if e > 0 else None))
        P(f"  (reported) forecast, {lab}: expected dchi2 {e:.1f} at the present sample; lens-number factor for dchi2 25: {25.0 / max(e, 1e-300):.2f}")
    fo["mimic"] = mim; fo["forecast"] = fc
    FT[foot] = fo
    P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

RES["footings"] = FT
# F2 isolation-leakage context (committed numbers, no new run)
F2J = json.load(open(os.path.join(REB, "F2_outer_lensing", "f2_outer_lensing_results.json")))
ctx = dict(gama_over_kids_iso_outer=F2J["posthoc"]["gama_over_kids_iso_outer"], kids_all_over_iso_outer=F2J["posthoc"]["kids_all_over_iso_outer"],
           S10_minus_Sstrict_out_canonical_ye0=F2J["trackB"]["canonical"]["zero"]["diff_out"])
RES["isolation_context_F2"] = ctx
P(f"\n  (context, F2 committed) GAMA spec-z / KiDS photo-z isolated outer: {ctx['gama_over_kids_iso_outer'][0]:.2f} +- {ctx['gama_over_kids_iso_outer'][1]:.2f}; "
  f"KiDS all / isolated: {ctx['kids_all_over_iso_outer'][0]:.2f} +- {ctx['kids_all_over_iso_outer'][1]:.2f}; S10 - S_strict outer amplitude (y_e 0, canonical): "
  f"{ctx['S10_minus_Sstrict_out_canonical_ye0']['d']:+.2f} +- {ctx['S10_minus_Sstrict_out_canonical_ye0']['s']:.2f}")

V = {f: FT[f]["verdict"] for f in FOOTS}
if not CHK.get("K0_step0", False):
    LANE = "UNDECIDED (step 0 failed)"
elif V["canonical"] == V["alt"]:
    LANE = ("OUTER LENSING DISCRIMINATES: " + V["canonical"]) if V["canonical"] in ("LAW", "HALOS") else V["canonical"]
else:
    LANE = f"UNDECIDED (footings disagree: {V})"
RES["verdict"] = LANE
P(f"\n=== VERDICT (both footings, frozen rule): {LANE}")
check("K_R_rss_below_1GB", rss() < 1.0, f"{rss():.2f} GB")
n = sum(CHK.values())
RES["checks"] = CHK
P(f"\nchecks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
json.dump(RES, open(os.path.join(HERE, "x62_x53copy_off_shpS9_L2.5090595510216196_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "x62_x53copy_off_shpS9_L2.5090595510216196.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)
