#!/usr/bin/env python3
"""SI1_spec_isolated_route_e (criteria ed3c0f8bb1): route E vs the law on P2's spectroscopically isolated stack. P2's own text runs read-only through its verdict loop, then route E tables go through the same stack code.
    OMP_NUM_THREADS=1 nice -n 15 python3 si1_grade.py <kids_source_cache_dir> <work_dir> [--mutate] [--scan]
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
SHERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(SHERE); P2F = os.path.join(REB, "P2_spec_isolated_lensing", "p2_spec_isolated_lensing.py")
CACHE, WORK = sys.argv[1], sys.argv[2]; MUTS = "--mutate" in sys.argv; SCAN = "--scan" in sys.argv
T = open(P2F).read(); CUT = "# ---- K4: cross-shear null of Delta (S3)"; assert T.count(CUT) == 1; T = T[:T.index(CUT)]
A = 'OATS = {"central": {}, "fhot0": dict(fhot=0.0), "fhot1": dict(fhot=1.0), "Ms-0.2": dict(dMs=-0.2), "Ms+0.2": dict(dMs=0.2),\n        "h0.672": dict(h=0.672), "h0.686": dict(h=0.686)}'
assert T.count(A) == 1; T = T.replace(A, 'OATS = {"central": {}, "Ms-0.2": dict(dMs=-0.2), "Ms+0.2": dict(dMs=0.2)}')      # only the variants this lane reports
sys.argv = [P2F, CACHE, WORK, "--phase=B"]; N = {"__file__": P2F, "__name__": "p2_ro"}; exec(compile(T, P2F, "exec"), N)
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy import stats
OUT = []
def P(s): print(s, flush=True); OUT.append(str(s))
AQ, RG, LMG, EDGES, RCEN, RANGE, H0N, A0, NP_, MEAS, SETS, TOWN, GT, OATS, DGR, LMB_T, NSUBB, SG, TGL, WGL, FOOTS = (N[k] for k in ("AQ", "RGRID_PC", "LMG", "EDGES", "RCEN", "RANGE", "H0N", "A0", "NP_", "MEAS", "SETS", "TOWN", "GT", "OATS", "DGR", "LMB_T", "NSUBB", "SG", "TGL", "WGL", "FOOTS"))
bin_avg, point_part, tnbr, primary, amps, L3, L1, idxS3, idxS1, lMs_nat, lM70, z_g, VER = (N[k] for k in ("bin_avg", "point_part", "tnbr", "primary", "amps", "L3", "L1", "idxS3", "idxS1", "lMs_nat", "lM70", "z_g", "VER"))
Gpc = 4.30091e-3; G_SI, MSUN, MPC = N["G_SI"], N["MSUN"], N["MPC"]
EM1J = json.load(open(os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent_results.json")))["rows"]["A_c2b_refit"]["R1"]; BA, BB = EM1J["a"], EM1J["b"]
HB = json.load(open(os.path.join(REB, "F3_growth_audit", "f3_growth_audit_results.json")))["K2"]["A_c2b_refit"]["params"]["h"]
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
SCT = sorted((math.log10(float(k)), math.log10(v[0])) for k, v in X43J["sigma_coll_table"].items()); SC_LM, SC_LS = np.array([a for a, _ in SCT]), np.array([b for _, b in SCT])
def sigma_coll(M):
    l = math.log10(M)
    if l < SC_LM[0]: s = (SC_LS[1] - SC_LS[0]) / (SC_LM[1] - SC_LM[0]); return 10 ** (SC_LS[0] + s * (l - SC_LM[0]))
    if l > SC_LM[-1]: s = (SC_LS[-1] - SC_LS[-2]) / (SC_LM[-1] - SC_LM[-2]); return 10 ** (SC_LS[-1] + s * (l - SC_LM[-1]))
    return 10 ** float(np.interp(l, SC_LM, SC_LS))
CE = json.load(open(os.path.join(REB, "CE1_converged_eta_grade", "ce1_results.json")))["eta"]; ETAV = [CE[str(e)]["med"] for e in (12, 13, 14)]
NOM, NH, NWB = 0.2976016, 0.6856427, 0.0223081; NOB = NWB / NH ** 2; FC = (NOM - NOB) / NOM; RHOM0 = 2.775e11 * NH ** 2 * NOM / 1e18; DTA = 5.55; RHOC = 2.775e11 * HB ** 2 / 1e18
def eta_conv(M): return float(np.interp(math.log10(M), [12, 13, 14], ETAV))
def B(x): x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
SAT = {"n": 0}
def solve_r0(M, R, S):
    lm = lambda lr: math.log(math.pi * S * math.exp(2 * lr) * float(B(R / math.exp(lr))))
    pk = minimize_scalar(lambda lr: -lm(lr), bounds=(math.log(R * 1e-6), math.log(R * 1e3)), method="bounded", options={"xatol": 1e-10}); lpk = float(pk.x)
    if lm(lpk) < math.log(M): SAT["n"] += 1; return math.exp(lpk)
    return math.exp(brentq(lambda lr: lm(lr) - math.log(M), math.log(R * 1e-7), lpk, xtol=1e-14))
SIGA = {f: A0[f] * 3.0857e16 / 1e6 / (2 * math.pi * Gpc) for f in FOOTS}
_w = MEAS["WW"][L3].sum(1); _z = z_g[idxS3]; _o = np.argsort(_z); ZT = float(_z[_o][np.searchsorted(np.cumsum(_w[_o]), 0.5 * _w.sum())])
def halo_of(foot, r_pc, Ms, Mc, Mbt, dlm, prof):
    """M_h(<r) [Msun] at r_pc; X53's M200 relation, FC1's rule, BL1's r_ta."""
    M200 = 10 ** (BA + BB * (math.log10(Ms + Mc) - 10) + dlm); R200 = (3 * M200 / (4 * math.pi * 200 * RHOC)) ** (1 / 3)
    Mt = M200 / FC; S = max(SIGA[foot], FC * eta_conv(Mt) * sigma_coll(Mt)); r0 = solve_r0(M200, R200, S)
    rta = (3 * (M200 + Mbt) / (4 * math.pi * DTA * RHOM0)) ** (1 / 3) / (1 + ZT); rc = max(rta, R200) if prof == "E" else R200
    return math.pi * S * r0 ** 2 * B(np.minimum(r_pc, rc) / r0), dict(M200=M200, R200=R200, S=S, r0=r0, rta=rta)
HF = 0.5 if MUTS else 1.0
def town_H(foot, dlm=0.0, prof="E", dMs=0.0, fhot=0.5):
    tab = np.empty((len(LMG), 15)); Rpe = EDGES * 1e6
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * np.log10(0.70 / H0N); lmc = lm + (-0.69 * lm70 + 6.63); Ms = 10 ** (lm + dMs); Mc = 10 ** lmc; Mh_ = fhot * 10 ** lm
        Mb = Ms + Mc + Mh_ * np.minimum(1.0, (RG / 1e5) ** 3); Mh, _ = halo_of(foot, RG, Ms, Mc, Ms + Mc + Mh_, dlm, prof); M = Mb + HF * Mh
        tab[gi] = bin_avg(Rpe, lambda R: AQ.delta_sigma(R, RG, M, "const"))
    return np.stack([tab, tab], 1)                                # two identical nodes: y_e = 0 only, P2's interpolation stays as written
def ext_of(m):
    """P2's ext_profile with a given dimensionless M(<s) on SG (constant tail)."""
    lr = np.log(SG); dMdr = np.gradient(m, lr) / SG; ch = np.cosh(AQ.TT); sh = np.sinh(AQ.TT); th_ = np.tanh(AQ.TT)
    w = np.full(AQ.TT.size, AQ.TT[1] - AQ.TT[0]); w[0] *= 0.5; w[-1] *= 0.5; Sig = np.empty(SG.size); Mcyl = np.empty(SG.size)
    for c0 in range(0, SG.size, 100):
        R = SG[c0:c0 + 100]; r = R[:, None] * ch[None, :]; fv = np.interp(np.log(r), lr, dMdr, left=dMdr[0], right=0.0)
        Mcyl[c0:c0 + 100] = np.interp(np.log(R), lr, m) + np.sum(fv * (1 - th_) * R[:, None] * sh * w, axis=1)
        Sig[c0:c0 + 100] = np.sum(fv / ch * w, axis=1) / (2 * math.pi * R)
    return 2 * math.pi * SG ** 2 * Sig, Mcyl
def mc_pairs(fS, Mcyl, U, V):
    """P2's mc_table formula on (U, V) pairs: projected mass inside a circle of radius U whose centre is V from the profile centre."""
    lS = np.log(SG); out = np.empty(len(U))
    for c0 in range(0, len(U), 20000):
        u = U[c0:c0 + 20000, None]; v = V[c0:c0 + 20000, None]; a = np.abs(u - v); b = u + v; s = a + (b - a) * (1 - np.cos(TGL[None, :])) / 2; ds = (b - a) * np.sin(TGL[None, :]) / 2
        arg = np.clip((s * s + v * v - u * u) / (2 * s * v), -1, 1); integ = np.interp(np.log(s), lS, fS) / s * (np.arccos(arg) / np.pi) * ds
        inner = np.where(v[:, 0] < u[:, 0], np.interp(np.log(np.maximum(u[:, 0] - v[:, 0], 1e-12)), lS, Mcyl), 0.0); out[c0:c0 + 20000] = inner + np.sum(integ * WGL[None, :], axis=1)
    return out
def g_halo(foot, lmb, dgrid, dlm=0.0, prof="E"):
    """gtable for the halo around a neighbour of native log M_b: bin-averaged tangential DeltaSigma, shape (15, len(dgrid)); the baryons stay in P2's point_part."""
    lm_g = np.arange(5.0, 13.0, 0.01); lm70g = lm_g - 2 * np.log10(0.70 / H0N); lcg = lm_g + (-0.69 * lm70g + 6.63); lbg = np.log10(1.5 * 10 ** lm_g + 10 ** lcg)
    lm_ = float(np.interp(lmb, lbg, lm_g)); Ms = 10 ** lm_; Mc = 10 ** float(np.interp(lm_, lm_g, lcg)); Mb = 10 ** lmb
    rM = math.sqrt(G_SI * Mb * MSUN / A0[foot]) / MPC; Mh, _ = halo_of(foot, SG * rM * 1e6, Ms, Mc, Mb, dlm, prof); fS, Mcyl = ext_of(HF * Mh / Mb)
    out = np.empty((15, len(dgrid)))
    Rs_all = np.exp(np.concatenate([np.linspace(np.log(EDGES[k]), np.log(EDGES[k + 1]), NSUBB) for k in range(15)]))
    uu = np.repeat(Rs_all / rM, len(dgrid)); vv = np.tile(dgrid / rM, len(Rs_all)); Mcc = mc_pairs(fS, Mcyl, uu, vv).reshape(15, NSUBB, len(dgrid))
    for k in range(15):
        R1, R2 = EDGES[k], EDGES[k + 1]; hstep = (np.log(R2) - np.log(R1)) / (NSUBB - 1); wS = np.ones(NSUBB); wS[1:-1:2] = 4; wS[2:-1:2] = 2; wS *= hstep / 3
        out[k] = Mb * (2 * np.sum(Mcc[k] * wS[:, None], axis=0) - (Mcc[k][-1] - Mcc[k][0])) / (math.pi * ((R2 * 1e6) ** 2 - (R1 * 1e6) ** 2))
    return out
def build(foot, dlm=0.0, prof="E"):
    key = f"H|{foot}|{dlm:+.3f}|{prof}"
    GT[key] = np.empty((len(LMB_T), 1, 15, len(DGR)))
    for ti, lmb in enumerate(LMB_T): GT[key][ti, 0] = g_halo(foot, float(lmb), DGR, dlm, prof)
    for oat, kw in (("central", {}), ("Ms-0.2", dict(dMs=-0.2)), ("Ms+0.2", dict(dMs=0.2))):
        if oat != "central" and (dlm != 0.0 or prof != "E"): continue
        TOWN[(key, oat)] = town_H(foot, dlm, prof, **kw)
    return key, tnbr(key, node=0)
HART = lambda p: (NP_ - p - 2) / (NP_ - 1)
def cov_of(st): return (NP_ - 1) / NP_ * (st["dj"] - st["dj"].mean(0)).T @ (st["dj"] - st["dj"].mean(0))
def compare(sL, sH, msk=None):
    msk = np.ones(15, bool) if msk is None else msk; d = sL["d"][msk]; C = cov_of(sL)[np.ix_(msk, msk)]; p = int(msk.sum()); Ci = HART(p) * np.linalg.inv(C)
    cL = float((d - sL["m"][msk]) @ Ci @ (d - sL["m"][msk])); cH = float((d - sH["m"][msk]) @ Ci @ (d - sH["m"][msk])); dm = sH["m"][msk] - sL["m"][msk]
    return dict(chi2_L=cL, chi2_H=cH, dchi2=cH - cL, D=float(math.sqrt(max(dm @ Ci @ dm, 0))), p=p, pL=float(stats.chi2.sf(cL, p)), pH=float(stats.chi2.sf(cH, p)))
def cls(c):
    if c["D"] < 3: return "NOT POWERED"
    s = 2 * c["D"]; nearL = abs(c["dchi2"] - c["D"] ** 2) <= 2 * s; nearH = abs(c["dchi2"] + c["D"] ** 2) <= 2 * s
    if c["dchi2"] >= 0 and nearL: return "LAW PREFERRED"
    if c["dchi2"] <= 0 and nearH: return "ROUTE E PREFERRED"
    return "NEITHER" if not nearL and not nearH else ("LAW PREFERRED" if nearL and c["dchi2"] >= 0 else "ROUTE E PREFERRED" if nearH and c["dchi2"] <= 0 else "NEITHER")
RES = dict(criteria="ed3c0f8bb1", f_c=FC, z_ta=ZT, mutate=MUTS, k={}, foot={}); OK = True
P(f"\nSI1 route E vs the law on P2's spectroscopic stack; f_c {FC:.5f}; z_ta (S3 weighted median) {ZT:.3f}; EM1 a {BA} b {BB}; kappa = 1/2 FITTED; footings never pooled; not theory closed" + (" [MUTATE halo x 0.5]" if MUTS else ""))
P2J = json.load(open(os.path.join(REB, "P2_spec_isolated_lensing", "p2_spec_isolated_lensing_results.json")))["verdict"]
if not MUTS:
    dd = dm = 0.0
    for foot in FOOTS:
        pr = P2J[foot]["profile"]; sa = primary(foot, "a"); sig = np.sqrt(sa["var"]); dd = max(dd, float(np.max(np.abs(sa["d"] - np.array(pr["d"])) / sig))); dm = max(dm, float(np.max(np.abs(sa["m"] - np.array(pr["m_a"])) / sig)))
    k1 = dd <= 1e-6 and dm <= 1e-6; OK &= k1; RES["k"]["K1"] = dict(d=dd, m=dm, ok=k1); P(f"K1 rebuilt stack vs P2's committed Delta {dd:.1e} sigma; law model vs committed m_a {dm:.1e} sigma: {'PASS' if k1 else 'FAIL'}")
    # K2 (i) offset -> 0 equals the centred bin average of the same halo; (ii) uniform sheet
    lmb_t = 10.5; foot = "canonical"; lm_g = np.arange(5.0, 13.0, 0.01); lm70g = lm_g - 2 * np.log10(0.70 / H0N); lcg = lm_g + (-0.69 * lm70g + 6.63); lbg = np.log10(1.5 * 10 ** lm_g + 10 ** lcg)
    lm_ = float(np.interp(lmb_t, lbg, lm_g)); Ms_ = 10 ** lm_; Mc_ = 10 ** float(np.interp(lm_, lm_g, lcg)); Mb_t = 10 ** lmb_t; rM_t = math.sqrt(G_SI * Mb_t * MSUN / A0[foot]) / MPC
    g0 = g_halo(foot, lmb_t, np.array([1e-9]))[:, 0]; Mh_s, _m = halo_of(foot, SG * rM_t * 1e6, Ms_, Mc_, Mb_t, 0.0, "E")
    cent = bin_avg(EDGES * 1e6, lambda R: AQ.delta_sigma(R / (rM_t * 1e6), SG, Mh_s, "const") / (rM_t * 1e6) ** 2); k2a = float(np.max(np.abs(g0 / cent - 1)))
    dfine = np.logspace(-4, np.log10(80.0), 1500); gs = g_halo(foot, lmb_t, dfine) + point_part(np.full(dfine.size, Mb_t), dfine).T
    k2b = float(np.max(np.abs(np.trapz(gs * 2 * np.pi * dfine[None, :], dfine, axis=1)) / np.trapz(np.abs(gs) * 2 * np.pi * dfine[None, :], dfine, axis=1)))
    k3 = 0.0
    for lM in (11.5, 12.0, 13.0):
        M = 10 ** lM; R = (3 * M / (4 * math.pi * 200 * RHOC)) ** (1 / 3); r0 = solve_r0(M, R, 150.0); k3 = max(k3, abs(math.pi * 150.0 * r0 ** 2 * float(B(R / r0)) / M - 1))
    ok2 = k2a <= 1e-3 and k2b <= 1e-2 and k3 <= 1e-8; OK &= ok2; RES["k"].update(K2a=k2a, K2b=k2b, K3=k3); P(f"K2 offset->0 vs centred {k2a:.1e}; uniform sheet {k2b:.1e}; K3 M_h(R200) {k3:.1e}: {'PASS' if ok2 else 'FAIL'}")
SAMPLES = (("S3", "primary"), ("S1", "reported"))
for foot in FOOTS:
    key, TNH = build(foot); keyT, TNT = (None, None) if MUTS else build(foot, prof="T"); F = {}
    if not MUTS: _, _m = halo_of(foot, RG, 10 ** 10.78, 10 ** (10.78 + (-0.69 * 10.78 + 6.63)), 1.2e11, 0.0, "E"); P(f"  [{foot}] halo at lg M* 10.78: lg M200 {math.log10(_m['M200']):.2f}, R200 {_m['R200'] / 1e3:.0f} kpc, r_ta {_m['rta'] / 1e3:.0f} kpc, S {_m['S']:.0f}, r0 {_m['r0'] / 1e3:.1f} kpc")
    for sm, role in SAMPLES:
        sL = primary(foot, "a", sample=sm); sb = primary(foot, "b", sample=sm); sH = primary(key, "a", sample=sm, tn=TNH); c = compare(sL, sH); cb = compare(sb, sH); F[sm] = dict(all=c, vs_b=cb, cls=cls(c), d=sL["d"].tolist(), sig=np.sqrt(sL["var"]).tolist(), m_L=sL["m"].tolist(), m_Lb=sb["m"].tolist(), m_H=sH["m"].tolist(), amps_H=amps(sH), amps_L=amps(sL))
        rin = compare(sL, sH, RANGE["in"]); rout = compare(sL, sH, RANGE["out"]); F[sm]["inner"] = rin; F[sm]["outer"] = rout
        lab = cls(c) if OK else f"NOT DECIDED ({cls(c)})"; F[sm]["label"] = lab
        P(f"\n  [{foot} {sm} {role}] chi2 L {c['chi2_L']:.1f} (p {c['pL']:.3f}), H {c['chi2_H']:.1f} (p {c['pH']:.3f}); dchi2 {c['dchi2']:+.1f}; D {c['D']:.2f} -> {lab}")
        P(f"     inner (R <= 0.31): L {rin['chi2_L']:.1f}, H {rin['chi2_H']:.1f}, dchi2 {rin['dchi2']:+.1f}, D {rin['D']:.2f}; outer (0.4-3): L {rout['chi2_L']:.1f}, H {rout['chi2_H']:.1f}, dchi2 {rout['dchi2']:+.1f}, D {rout['D']:.2f}; vs L(b): dchi2 {cb['dchi2']:+.1f}, D {cb['D']:.2f}")
        a_ = amps(sH); P(f"     A for H: in {a_['A_in']:.3f}+-{a_['sA_in']:.3f}, O1 {a_['A_O1']:.3f}+-{a_['sA_O1']:.3f}, O2 {a_['A_O2']:.3f}+-{a_['sA_O2']:.3f}")
        P("     R   " + " ".join(f"{x:6.3f}" for x in RCEN)); P("     d   " + " ".join(f"{x:6.2f}" for x in sL["d"])); P("     sig " + " ".join(f"{x:6.2f}" for x in np.sqrt(sL["var"]))); P("     L   " + " ".join(f"{x:6.2f}" for x in sL["m"])); P("     H   " + " ".join(f"{x:6.2f}" for x in sH["m"]))
        if not MUTS:
            sT = primary(keyT, "a", sample=sm, tn=TNT); cT = compare(sL, sT); F[sm]["trunc"] = cT; P(f"     H_T (cut at R200): chi2 {cT['chi2_H']:.1f}, dchi2 {cT['dchi2']:+.1f}")
            for oat in ("Ms-0.2", "Ms+0.2"):
                sLo = primary(foot, "a", oat=oat, sample=sm); sHo = primary(key, "a", oat=oat, sample=sm, tn=TNH); co = compare(sLo, sHo); F[sm][oat] = co; P(f"     {oat}: chi2 L {co['chi2_L']:.1f}, H {co['chi2_H']:.1f}, dchi2 {co['dchi2']:+.1f}, D {co['D']:.2f}")
            sLn = primary(foot, "a", sample=sm, no_nbr=True); sHn = primary(key, "a", sample=sm, no_nbr=True, tn=TNH); cn = compare(sLn, sHn); F[sm]["no_nbr"] = cn; P(f"     no neighbour term: chi2 L {cn['chi2_L']:.1f}, H {cn['chi2_H']:.1f}, dchi2 {cn['dchi2']:+.1f}, D {cn['D']:.2f}")
    if SCAN and not MUTS:
        sc = {}
        for dl in np.round(np.arange(-0.3, 0.7001, 0.1), 2):
            k_, tn_ = (key, TNH) if abs(dl) < 1e-9 else build(foot, float(dl)); row = {}
            for sm, _r in SAMPLES:
                sL = primary(foot, "a", sample=sm); sH = primary(k_, "a", sample=sm, tn=tn_); row[sm] = compare(sL, sH)["chi2_H"]
            sc[f"{dl:+.2f}"] = row; P(f"     shift {dl:+.2f}: chi2 H S3 {row['S3']:.1f}, S1 {row['S1']:.1f}")
            if abs(dl) > 1e-9: GT.pop(k_, None); [TOWN.pop(x, None) for x in list(TOWN) if x[0] == k_]
        F["scan"] = sc
    RES["foot"][foot] = F
    for k_ in [x for x in GT if x.startswith("H|")]: GT.pop(k_)
RES["saturated_solves"] = SAT["n"]; P(f"saturated r0 solves: {SAT['n']}")
if MUTS:
    B0 = json.load(open(os.path.join(SHERE, "si1_results.json")))["foot"]["canonical"]["S3"]; mH = np.array(RES["foot"]["canonical"]["S3"]["m_H"]); m0 = np.array(B0["m_H"]); okm = bool(np.all(mH <= m0 + 1e-12)) and abs(RES["foot"]["canonical"]["S3"]["all"]["chi2_H"] - B0["all"]["chi2_H"]) > 1e-3
    P(f"MUTATE halo x 0.5: m_H lower in every bin: {bool(np.all(mH <= m0 + 1e-12))}; chi2 H {B0['all']['chi2_H']:.1f} -> {RES['foot']['canonical']['S3']['all']['chi2_H']:.1f}: {'PASS' if okm else 'FAIL'}")
tag = "_MUTATE" if MUTS else ("_scan" if SCAN else "")
json.dump(RES, open(os.path.join(SHERE, f"si1_results{tag}.json"), "w"), indent=1, default=float); open(os.path.join(SHERE, f"si1{tag}.out"), "w").write("\n".join(OUT) + "\n")
