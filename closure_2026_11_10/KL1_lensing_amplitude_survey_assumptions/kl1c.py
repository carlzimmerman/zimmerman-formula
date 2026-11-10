#!/usr/bin/env python3
"""KL1 PART C (FROZEN_CRITERIA_PARTC.md 190161a7f7; AMENDMENT_C1 fe976ca7d3): the lensing rows for one footing and one survey group.
The KiDS-Legacy release is untrusted data: run with python3 -I, the release folder passed as an argument.
  group 'legacy':  KiDS-Legacy: KC1, C0 (R1; R1b, R2, R2b), C2 (AD), GATE = C0 + C2, gate edges, C1 brackets, C3 (a, b, c), MP5.
  group 'deskids': DES Y3 and KiDS-1000: the same rows without C3; KC2 and MC0 on KiDS-1000.
Machinery: Part A's kl1_lib (CO2's shear path, KL1's fit copy, the covariance at the model, the scan rule) and Part B's generic
loader (copied from kl1_partb.py, unchanged); C0's corrections copied from CO2's co2_posthoc.py; C1 / C2 layouts from kl1c_gas.json;
C3's prior from kl1c_ia.json.

  OMP_NUM_THREADS=1 nice -n 10 python3 -I kl1c.py <footing> <legacy|deskids> <release folder>  -> parts/partc_<footing>_<group>.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing. Gravity-only S0 box; inherited halo list in R."""
import os, sys, json, math, time, re, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import astropy.io.fits as fits
from scipy.optimize import minimize
from scipy.stats import chi2 as CH
import kl1_lib as K1
FT, GRP, REL = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3]); assert FT in K1.FOOTS and GRP in ("legacy", "deskids")
T0 = time.time(); LOG = []
OUTF = os.path.join(HERE, "parts", f"partc_{FT}_{GRP}.json")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
G, SURV = K1.G, K1.SURV

# ------------------------------------------------------------------ Part B's generic loader (copied from kl1_partb.py, unchanged)
def load_generic(name, fn, e_lo, e_hi, cut_p, cut_m, Lchol, mu_u):
    F = fits.open(fn); cov = np.array(F["COVMAT"].data, float); nzt = F["NZ_SOURCE"].data; hd = F["NZ_SOURCE"].header
    rows = [(s, int(r["BIN1"]), int(r["BIN2"]), int(r["ANGBIN"]), float(r["ANG"]), float(r["VALUE"])) for s, ext in (("+", "xiP"), ("-", "xiM")) for r in F[ext].data]
    nb = int(F["xiP"].header["N_ZBIN_1"]); e = np.geomspace(e_lo, e_hi, int(F["xiP"].header["N_ANG"]) + 1)
    keep = np.array([(cut_p[0] <= r[4] <= cut_p[1]) if r[0] == "+" else (cut_m[0] <= r[4] <= cut_m[1]) for r in rows])
    S = dict(name=name, generic=True, cov=cov, rows=rows, pubkeep=keep, zmid=np.array(nzt["Z_MID"], float), nz=[np.array(nzt[f"BIN{i+1}"], float) for i in range(nb)],
             nbin=nb, edges=list(zip(e[:-1], e[1:])), angbin0=min(r[3] for r in rows), L=Lchol, mu_u=np.asarray(mu_u, float),
             sig_e=np.array([hd[f"SIG_E_{i+1}"] for i in range(nb)], float), ngal=np.array([hd[f"NGAL_{i+1}"] for i in range(nb)], float))
    S["Hp"], S["Hm"], S["Ap"], S["Am"] = G["hankel"](S["edges"])
    S["pairs"] = [(a, b) for a in range(1, nb + 1) for b in range(a, nb + 1)]; pid = {p: i for i, p in enumerate(S["pairs"])}
    S["ip_all"] = np.array([pid[(min(r[1], r[2]), max(r[1], r[2]))] for r in rows]); S["ia_all"] = np.array([r[3] - S["angbin0"] for r in rows])
    S["isp_all"] = np.array([r[0] == "+" for r in rows]); S["b1_all"] = np.array([r[1] for r in rows]) - 1; S["b2_all"] = np.array([r[2] for r in rows]) - 1
    S["d_all"] = np.array([r[5] for r in rows]); S["Jp_raw"], S["Jm_raw"], S["Om_bin"] = K1._jbar(S)
    return S
_orig_spec = G["nuis_spec"]
def nuis_spec_gen(S, widen, ia):
    if not S.get("generic"): return _orig_spec(S, widen, ia)
    nb = S["nbin"]; mu = S["mu_u"]
    x0 = np.r_[mu, 0.5 if ia else 0.0]; lo = np.r_[mu - 5 * widen, -6.0 if ia else 0.0]; hi = np.r_[mu + 5 * widen, 6.0 if ia else 0.0]
    unpack = lambda x: dict(dz=S["L"] @ x[:nb], A=float(x[nb])); prior = lambda x: float(np.sum(((x[:nb] - mu) / widen) ** 2))
    return x0, lo, hi, unpack, prior
G["nuis_spec"] = nuis_spec_gen
def register(S):
    SURV[S["name"]] = S; K1.SUP[S["name"]] = K1.support_mask(S, K1.RUN1, K1.PS0)
    K1.SUP_HALF[S["name"]] = K1.support_mask(S, dict(K1.RUN1, k_hi=K1.RUN1["k_hi"] / 2), K1.PS0)
if GRP == "legacy":
    ini = open(os.path.join(REL, "chains_and_config_files", "xipm", "KiDS_Legacy_priors.ini")).read()
    MU_LEG = [float(re.search(rf"uncorr_bias_{i}\s*=\s*gaussian\s+(\S+)\s+1\.0", ini).group(1)) for i in range(1, 7)]
    LEG = load_generic("Legacy", os.path.join(REL, "data", "KiDS_Legacy_xipm.fits"), 2.0, 300.0, (2.0, 300.0), (4.0, 300.0), np.linalg.cholesky(np.loadtxt(os.path.join(REL, "data", "Nz_covariance.txt"))), MU_LEG)
    register(LEG)

# ------------------------------------------------------------------ C3: per-bin alignment amplitudes (a KL1 copy of CFG592's C_ell)
_orig_cell = G["C_ell"]
def C_ell_pb(S, par, Pm, bg):
    A = par["A"]
    if np.ndim(A) == 0: return _orig_cell(S, par, Pm, bg)
    q, I, wchi = G["kernels"](S, par["dz"], bg)
    F = -G["C1RHO"] * G["Om"] / G["DZG"] * (((1 + G["ZG"]) / 1.62) ** par.get("eta", 0.0))
    PW = Pm * wchi[None, :]; Ig = I * F[None, :]; A = np.asarray(A, float)
    GG = np.einsum("lj,aj,bj->abl", PW, q, q); GI = np.einsum("lj,aj,bj->abl", PW, q, Ig) * A[None, :, None]; II = np.einsum("lj,aj,bj->abl", PW, Ig, Ig) * (A[:, None] * A[None, :])[:, :, None]
    Cab = GG + GI + GI.transpose(1, 0, 2) + II
    return np.array([Cab[a - 1, b - 1] for a, b in S["pairs"]])
G["C_ell"] = C_ell_pb                                         # theory() looks it up here; a scalar A takes CFG592's own path
IA = json.load(open(os.path.join(HERE, "kl1c_ia.json")))
LMAT, C0V, MU_IA, FR, LMPIV = np.array(IA["Lmat"]), np.array(IA["c0"]), np.array(IA["mu_u"]), np.array(IA["f_r"]), IA["log10_m_piv"]
def amps(p): return p[0] * FR * 10 ** (p[1] * (p[2:8] - LMPIV))
def c3_spec(S, mode):
    nb = S["nbin"]; mu = S["mu_u"]
    if mode == "b":
        x0 = np.r_[mu, MU_IA]; lo = np.r_[mu - 5, MU_IA - 5]; hi = np.r_[mu + 5, MU_IA + 5]
        unpack = lambda x: dict(dz=S["L"] @ x[:nb], A=amps(LMAT @ x[nb:] + C0V))
        prior = lambda x: float(np.sum((x[:nb] - mu) ** 2) + np.sum((x[nb:] - MU_IA) ** 2))
        return x0, lo, hi, unpack, prior, [x0, np.r_[mu, MU_IA - np.r_[1.0, np.zeros(7)]]]
    Afix = np.array(IA["A_i_prior_mean"] if mode == "a" else IA["A_i_posterior_mean"])
    x0 = mu.copy(); unpack = lambda x: dict(dz=S["L"] @ x[:nb], A=Afix); prior = lambda x: float(np.sum((x[:nb] - mu) ** 2))
    return x0, mu - 5, mu + 5, unpack, prior, [x0]
def fit(S, D, Pm, Cinv=None, ia="nla", c3=None):
    if c3 is None: return K1.fit(S, D, Pm, ia=ia, Cinv=Cinv)
    x0, lo, hi, unpack, prior, starts = c3_spec(S, c3); d = D["d"]; Ci = D["Cinv"] if Cinv is None else Cinv
    def f(x):
        r = d - G["theory"](S, D, unpack(x), Pm, "PM"); return float(r @ Ci @ r) + prior(x)
    best = None
    for xs in starts:
        r = minimize(f, xs, method="L-BFGS-B", bounds=list(zip(lo, hi)), options=dict(maxiter=400, ftol=1e-12, gtol=1e-8))
        if best is None or r.fun < best.fun: best = r
    par = unpack(best.x); r_ = d - G["theory"](S, D, par, Pm, "PM"); c2d = float(r_ @ Ci @ r_)
    out = dict(chi2=float(best.fun), chi2_data=c2d, N=D["N"], p=float(CH.sf(c2d, D["N"])), A_i=[float(v) for v in np.atleast_1d(par["A"])], x=[float(v) for v in best.x])
    out["label"] = K1.lab(out["p"]); out["dz_pulls"] = [float(v) for v in (best.x[:S["nbin"]] - S["mu_u"])]
    if c3 == "b": out["ia_pulls"] = [float(v) for v in (best.x[S["nbin"]:] - MU_IA)]
    return out

# ------------------------------------------------------------------ C0: the box's draw (copied from co2_posthoc.py)
K, SN, PZ0 = K1.K, K1.SN, K1.PZ0
rr = np.array(SN["zi"]["P"]) / (SN["zi"]["D"] ** 2 * G["P_lin0"](K))
def weight(k1, k2): return np.clip(1 - np.log(np.maximum(K, k1) / k1) / math.log(k2 / k1), 0, 1)
CORR = {"R1": rr ** weight(0.3, 1.0), "R1b": rr ** weight(0.2, 0.5)}
def load200(rel):
    J2 = json.load(open(os.path.join(G["EXT"], *rel))); S2 = J2["snap"]; k2 = np.array(S2["z0"]["k"])
    def splice(z, key):
        p2 = np.exp(np.interp(np.log(K), np.log(k2), np.log(np.array(S2[key]["P"])))); out = PZ0[z].copy(); m = K < 0.5; out[m] = p2[m]; return out
    return {0.0: splice(0.0, "z0"), 0.5: splice(0.5, "z0.5"), 1.0: splice(1.0, "z1")}
PZV = {None: PZ0, "R1": {z: PZ0[z] / CORR["R1"] for z in PZ0}, "R1b": {z: PZ0[z] / CORR["R1b"] for z in PZ0},
       "R2": load200(("cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json")), "R2b": load200(("cfg424_work", "cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360.json")),
       "R1_wrong": {z: PZ0[z] * CORR["R1"] for z in PZ0}}
def Pm_of(Rk, s8, pz):
    K1.setP(PZV[pz]); return K1.Pmat(K1.run_of(Rk, (s8 / K1.S8E) ** 2, "resp"), "F")

# ------------------------------------------------------------------ inputs from Parts A / B and the halo-model side
HM, ROWS = K1.HM, K1.ROWS
NU = json.load(open(os.path.join(HERE, "kl1_nu.json"))); GC = json.load(open(os.path.join(HERE, "kl1c_gas.json")))
PA = json.load(open(os.path.join(HERE, "parts", f"rows_{FT}.json"))); PB = json.load(open(os.path.join(HERE, "parts", f"partb_{FT}.json")))
S8_CO2 = ROWS["P2"][FT]["sigma8"]; S8_NU = NU["A1"][FT]["sigma8_nu"]
R = dict(co1=np.array(HM["primary"][FT]["R_tot"]), **{k: np.array(v["R_tot"]) for k, v in GC["rows"][FT].items()})
FID = dict(KiDS=PA["rows"]["A0"]["KiDS"]["best_sigma8"], DES=PA["rows"]["A0"]["DES"]["best_sigma8"], Legacy=PB["rows"]["B0"]["best_sigma8"])
REF = dict(KiDS=PA["rows"]["ALL"]["KiDS"]["at_target"]["chi2"], DES=PA["rows"]["ALL"]["DES"]["at_target"]["chi2"], Legacy=PB["rows"]["BALL"]["at_target"]["chi2"])

# ------------------------------------------------------------------ A2 machinery (copied from kl1.py, unchanged)
CTX = {}
def make_ctx(sn, s8_fid, area=None):
    S = SURV[sn]; pub = np.where(S["pubkeep"])[0]
    Pm = Pm_of(R["co1"], s8_fid, None); C = K1.cell_full(S, Pm)
    G1, N1 = K1.gauss_cov(S, pub, C); Cp = S["cov"][np.ix_(pub, pub)]
    dg, dn, dp = np.diag(G1), np.diag(N1), np.diag(Cp); nf = dn / dg
    if area is None:
        nd = nf >= 0.8; area = float(1.0 / np.median(dp[nd] / dg[nd])) if nd.sum() else float("nan")
    Gf = G1 / area; xi = K1.xi_nominal(S, Pm)
    return dict(pub=pub, pos={int(g): i for i, g in enumerate(pub)}, area=area, R=Cp - Gf, xi_fid=xi, s8_fid=s8_fid)
def cov_model(sn, ctx, Pm, kmask, gamma):
    S = SURV[sn]; kept = np.where(kmask)[0]; kp = np.array([ctx["pos"][int(g)] for g in kept])
    G1, _ = K1.gauss_cov(S, kept, K1.cell_full(S, Pm)); xi = K1.xi_nominal(S, Pm)
    s = np.clip(xi[kept] / ctx["xi_fid"][kept], 0.5, 3.0)
    C = G1 / ctx["area"] + ctx["R"][np.ix_(kp, kp)] * np.outer(s, s) ** (gamma / 2.0)
    try: Lc = np.linalg.cholesky(C)
    except np.linalg.LinAlgError: return None, None
    return np.linalg.inv(C), float(2 * np.sum(np.log(np.diag(Lc))))
def run_row(sn, st):
    S = SURV[sn]; kmask = K1.keep_mask(sn, 0.9, False); D = K1.subset(S, kmask)
    Rk, pz, gam = R[st["R"]], st.get("pz"), st.get("cov")
    if gam is not None and sn not in CTX: CTX[sn] = make_ctx(sn, FID[sn])
    def ev(s8):
        Pm = Pm_of(Rk, s8, pz); Ci, ld = (None, None)
        if gam is not None:
            Ci, ld = cov_model(sn, CTX[sn], Pm, kmask, gam)
            if Ci is None: return dict(chi2=float("nan"), p=float("nan"), not_pd=True)
        r = fit(S, D, Pm, Cinv=Ci, ia=st.get("ia", "nla"), c3=st.get("c3"))
        if ld is not None: r["logdet"] = ld
        return r
    tgt = st["s8"]; out = dict(settings=dict(st), N=D["N"], target_sigma8=tgt); main = ev(tgt); out["at_target"] = main
    if main.get("not_pd"): out["label"] = "NO VERDICT (covariance not positive definite)"; return out
    out["label"] = main["label"]
    if st.get("scan", True):
        cache = {}
        def evc(s):
            k = round(s, 6)
            if k not in cache: cache[k] = ev(s)
            return cache[k]
        sc = K1.scan(evc); best = ev(sc["best_sigma8"])
        out.update(scan=sc, best=best, best_sigma8=sc["best_sigma8"], width=sc["width"], gap_widths=(tgt - sc["best_sigma8"]) / sc["width"], dchi2_target_vs_best=main["chi2"] - best["chi2"])
        if gam is not None:
            ss = np.array(sorted(cache)); c2 = np.array([cache[s]["chi2"] + cache[s]["logdet"] for s in ss]); i = int(np.argmin(c2))
            lo_, hi_ = max(i - 2, 0), min(i + 3, len(ss)); co = np.polyfit(ss[lo_:hi_], c2[lo_:hi_], 2)
            sb = float(-co[1] / (2 * co[0])) if co[0] > 0 else float(ss[i]); wd = 1 / math.sqrt(co[0]) if co[0] > 0 else float("nan")
            out["with_logdet"] = dict(best_sigma8=sb, width=wd, gap_widths=(tgt - sb) / wd)
    return out
def show(name, sn, o):
    m = o["at_target"]
    if m.get("not_pd"): P(f"  {name:14s} {sn:6s}: covariance NOT positive definite -> NO VERDICT"); return
    s = f"  {name:14s} {sn:6s}: sigma8 {o['target_sigma8']:.4f}: chi2 {m['chi2']:.2f} (data {m['chi2_data']:.2f}, N {m['N']}), p {m['p']:.2e} -> {m['label']}"
    if "best_sigma8" in o: s += f"; best {o['best_sigma8']:.4f} +- {o['width']:.4f} (p {o['best']['p']:.3f}), gap {o['gap_widths']:+.2f}" + (" [EDGE]" if o["scan"]["edge_hit"] else "")
    if "with_logdet" in o: s += f" (ln det {o['with_logdet']['gap_widths']:+.2f})"
    if "A_i" in m and len(m["A_i"]) > 1: s += "; A_i " + " ".join(f"{v:.2f}" for v in m["A_i"])
    P(s + f"   [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------------ rows (frozen order)
BASE = dict(s8=S8_NU, R="A3_NR", cov=2.0)
SPEC = [("KC1", dict(BASE, scan=False)),
        ("C0_R1", dict(BASE, pz="R1")), ("C0_R1b", dict(BASE, pz="R1b")), ("C0_R2", dict(BASE, pz="R2")), ("C0_R2b", dict(BASE, pz="R2b")),
        ("C2_AD", dict(BASE, R="A3_AD")),
        ("GATE", dict(BASE, R="A3_AD", pz="R1")),
        ("GATE_R1b", dict(BASE, R="A3_AD", pz="R1b")), ("GATE_R2", dict(BASE, R="A3_AD", pz="R2")), ("GATE_R2b", dict(BASE, R="A3_AD", pz="R2b")),
        ("GATE_g0", dict(BASE, R="A3_AD", pz="R1", cov=0.0, scan=False)), ("GATE_g3", dict(BASE, R="A3_AD", pz="R1", cov=3.0, scan=False)),
        ("BRACKET_C1a", dict(BASE, R="C1a_AD", pz="R1")), ("BRACKET_C1b", dict(BASE, R="C1b_AD", pz="R1")),
        ("BRACKET_C1a_NR", dict(BASE, R="C1a_NR", pz="R1", scan=False)), ("BRACKET_C1b_NR", dict(BASE, R="C1b_NR", pz="R1", scan=False))]
if GRP == "legacy":
    SPEC += [("C3a_prior_mean", dict(BASE, R="A3_AD", pz="R1", c3="a")), ("C3b_own_prior", dict(BASE, R="A3_AD", pz="R1", c3="b")),
             ("C3c_posterior_mean", dict(BASE, R="A3_AD", pz="R1", c3="c")), ("MP5", dict(BASE, R="A3_AD", pz="R1", s8=0.90, scan=False))]
SNS = ["Legacy"] if GRP == "legacy" else ["DES", "KiDS"]
RES = json.load(open(OUTF)) if os.path.exists(OUTF) else dict(lane="KL1", part="C", criteria="190161a7f7", amendment_C1="fe976ca7d3", foot=FT, group=GRP,
                                                              note="kappa = 1/2 FITTED; not theory closed; adopts nothing; gravity-only S0; inherited halo list in R",
                                                              target_sigma8=S8_NU, KA={}, rows={}, MUTATE={})
def save(): json.dump(RES, open(OUTF, "w"), indent=1, default=float)
P(f"KL1 PART C [{FT}, {GRP}]: target sigma8 {S8_NU:.4f}; surveys {SNS}; C1 is a {GC['C1_conversion']['primary']['decision']} by the frozen rule.")
# KC5b: equal per-bin amplitudes take CFG592's path exactly
if "KC5b" not in RES["KA"]:
    S = SURV[SNS[0]]; x0, _, _, unpack, _ = G["nuis_spec"](S, 1.0, True); par = unpack(x0); Pm = Pm_of(R["co1"], S8_NU, None)
    a = _orig_cell(S, par, Pm, "PM"); b = C_ell_pb(S, dict(par, A=np.full(S["nbin"], par["A"])), Pm, "PM"); d = float(np.max(np.abs(b / a - 1)))
    RES["KA"]["KC5b"] = dict(max_rel=d, pass_=bool(d <= 1e-12)); P(f"  KC5b equal per-bin amplitudes against CFG592's C_ell: max rel {d:.1e} -> {'PASS' if d <= 1e-12 else 'FAIL'}")
for name, st in SPEC:
    for sn in SNS:
        key = f"{name}|{sn}"
        if key in RES["rows"]: continue
        o = run_row(sn, st); RES["rows"][key] = o; show(name, sn, o)
        if name == "KC1":
            d = o["at_target"]["chi2"] - REF[sn]; RES["KA"][f"KC1_{sn}"] = dict(chi2=o["at_target"]["chi2"], ref=REF[sn], d=d, pass_=bool(abs(d) <= 0.01))
            P(f"  KC1 {sn}: base replay chi2 {o['at_target']['chi2']:.3f} against Part {'B' if sn == 'Legacy' else 'A'}'s {REF[sn]:.3f} -> {'PASS' if abs(d) <= 0.01 else 'FAIL'}")
        if name == "MP5":
            RES["MUTATE"]["MP5"] = dict(p=o["at_target"]["p"], bites=bool(o["at_target"]["p"] < 0.0027)); P(f"  MP5 (MUTATE): p {o['at_target']['p']:.2e} -> {'bites' if o['at_target']['p'] < 0.0027 else 'DOES NOT BITE'}")
        save()
if GRP == "deskids":
    # KC2: CO2's post hoc best sigma8 on KiDS-1000 (A0 settings) with R1 and R2; MC0: the correction the wrong way
    a0 = dict(s8=S8_CO2, R="co1")
    for tag, pz in (("KC2_R1", "R1"), ("KC2_R2", "R2"), ("MC0_wrong", "R1_wrong")):
        key = f"{tag}|KiDS"
        if key not in RES["rows"]: RES["rows"][key] = run_row("KiDS", dict(a0, pz=pz)); show(tag, "KiDS", RES["rows"][key]); save()
    ref2 = dict(canonical=(0.7391, 0.7454), alt=(0.7373, 0.7435))[FT]; b1, b2 = RES["rows"]["KC2_R1|KiDS"]["best_sigma8"], RES["rows"]["KC2_R2|KiDS"]["best_sigma8"]
    RES["KA"]["KC2"] = dict(R1=b1, R2=b2, ref=ref2, pass_=bool(abs(b1 - ref2[0]) <= 5e-4 and abs(b2 - ref2[1]) <= 5e-4))
    a0b = PA["rows"]["A0"]["KiDS"]["best_sigma8"]; dR1 = b1 - a0b; dW = RES["rows"]["MC0_wrong|KiDS"]["best_sigma8"] - a0b
    RES["MUTATE"]["MC0"] = dict(d_R1=dR1, d_wrong=dW, bites=bool(dR1 * dW < 0 and abs(dW) >= 0.5 * abs(dR1)))
    P(f"  KC2 KiDS-1000 best sigma8 with R1 {b1:.4f}, R2 {b2:.4f} (CO2 post hoc {ref2[0]}, {ref2[1]}) -> {'PASS' if RES['KA']['KC2']['pass_'] else 'FAIL'};  "
      f"MC0 (MUTATE) R1 moves the best by {dR1:+.4f}, the wrong way by {dW:+.4f} -> {'bites' if RES['MUTATE']['MC0']['bites'] else 'DOES NOT BITE'}")
    save()
K1.setP(PZ0)
P(f"done ({time.time() - T0:.0f} s)")
open(OUTF.replace(".json", ".out"), "a").write("\n".join(LOG) + "\n")
