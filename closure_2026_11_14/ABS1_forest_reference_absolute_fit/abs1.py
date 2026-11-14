#!/usr/bin/env python3
"""ABS1 (FROZEN_CRITERIA.md, adefae297a): the forest gate's reference flux power against the DESI DR1 P1D in absolute
terms, simple nuisance terms, and the gate re-evaluated with the reference's own power in place of the data.
Reads stored parts only (FWN2 parts_b, FWN1R parts; read-only); FWN1R's library imported read-only for the data loader.
  nice -n 19 python3 -I -B abs1.py -> abs1.json / abs1.out, abs1_MUTATE.json / abs1_MUTATE.out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import cho_solve, cho_factor, solve_triangular
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FWN1R = os.path.join(REPO, "closure_2026_11_14", "FWN1R_blind_split_f_ceiling")
FWN2 = os.path.join(REPO, "closure_2026_11_14", "FWN2_forest_flux_split_f4")
sys.path.insert(0, FWN1R)
import fwn1r_lib as X                                                    # read-only
ODIR = os.environ.get("ABS1_ODIR") or HERE
PB = os.path.join(FWN2, "parts_b"); P1 = os.path.join(FWN1R, "parts")
G2 = json.load(open(os.path.join(FWN2, "fwn2b_grade.json"))); G1 = json.load(open(os.path.join(FWN1R, "fwn1r_grade.json")))
OUT, OUTM = [], []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)

# ------------------------------------------------------------------ data
FD = X.forest_data()
cf, lower = FD["CF"]; Uc = np.tril(cf).T if lower else np.triu(cf); COV = Uc.T @ Uc
ZS, KS, PD, NB = FD["zs"], FD["ks"], FD["Pd"], FD["NB"]
ZB = X.ZB; ANCH = X.ANCH
BIN = np.array([ZB.index(round(float(z), 1)) for z in ZS])
def dchi2(d): return float(d @ cho_solve(FD["CF"], d))                  # the graders' form (ss1_cosmo line 237)

# ------------------------------------------------------------------ parts
def load(folder, stage, ft):
    out = {}
    for f in sorted(glob.glob(os.path.join(folder, f"{stage}_z*_s*_{ft}.json"))):
        d = json.load(open(f))
        for k in ("P3D", "expected"): d.pop(k, None)
        if stage == "br" and d["seed"] in out.get(d["z"], {}):
            e = out[d["z"]][d["seed"]]; e["flux"].update(d["flux"]); continue
        out.setdefault(d["z"], {})[d["seed"]] = d
    return out

def at_points(kv, Rz):                                                   # the graders' at_points, unchanged
    r = np.ones(NB)
    for z, R in Rz.items():
        s_ = ZS == round(z, 2); r[s_] = np.interp(np.log(KS[s_]), np.log(kv[z][1:]), R[1:])
    return r

def model_at(kv, Pz, keys=ZB):
    """ln P interpolated linearly in ln k between box modes; below k_v[1] held at the k_v[1] value."""
    m = np.full(NB, np.nan)
    for z in keys:
        s_ = ZS == round(z, 2); m[s_] = np.exp(np.interp(np.log(KS[s_]), np.log(kv[z][1:]), np.log(Pz[z][1:])))
    return m

# ------------------------------------------------------------------ fits
def chol_sel(sel, extra=None):
    C = COV[np.ix_(sel, sel)].copy()
    if extra is not None: C = C + np.diag(extra[sel])
    return np.linalg.cholesky(0.5 * (C + C.T))
def chi2_0(m, sel, L):
    w = solve_triangular(L, (m - PD)[sel], lower=True); return float(w @ w)
def fit_A(m, sel, L):
    bins = sorted(set(BIN[sel])); Xd = np.zeros((int(sel.sum()), len(bins)))
    bs = BIN[sel]; ms = m[sel]
    for j, b in enumerate(bins): Xd[bs == b, j] = ms[bs == b]
    Xw = solve_triangular(L, Xd, lower=True); yw = solve_triangular(L, PD[sel], lower=True)
    A, *_ = np.linalg.lstsq(Xw, yw, rcond=None); res = yw - Xw @ A
    return float(res @ res), {ZB[b]: float(a) for b, a in zip(bins, A)}
def fit_AT(m, sel, L, bounded=True, A0=None):
    bins = sorted(set(BIN[sel])); bs = BIN[sel]; ms = m[sel]; lk = np.log(KS[sel] / 0.01); ys = PD[sel]; nb = len(bins)
    idx = np.array([bins.index(b) for b in bs])
    def res(x):
        lnA, al = x[:nb], x[nb:]
        return solve_triangular(L, ms * np.exp(lnA[idx] + al[idx] * lk) - ys, lower=True)
    lo = np.r_[np.full(nb, -np.inf), np.full(nb, -1.0 if bounded else -np.inf)]
    hi = np.r_[np.full(nb, np.inf), np.full(nb, 1.0 if bounded else np.inf)]
    a0 = np.log([max(A0[ZB[b]], 1e-6) for b in bins]) if A0 else np.zeros(nb)
    best = None
    for al0 in (0.0, 0.5, -0.5):
        r_ = least_squares(res, np.r_[a0, np.full(nb, al0)], bounds=(lo, hi), method="trf", x_scale=1.0, xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=20000)
        c = float(r_.fun @ r_.fun)
        if best is None or c < best[0]: best = (c, r_.x)
    c, x = best
    return c, {ZB[b]: float(math.exp(x[i])) for i, b in enumerate(bins)}, {ZB[b]: float(x[nb + i]) for i, b in enumerate(bins)}

def all_fits(m, sel, extra=None, perbin=True):
    L = chol_sel(sel, extra); n = int(sel.sum()); nbin = len(set(BIN[sel]))
    c0 = chi2_0(m, sel, L); cA, A = fit_A(m, sel, L); cAT, A2, al = fit_AT(m, sel, L, True, A); cATu, A3, alu = fit_AT(m, sel, L, False, A)
    out = dict(N=n, nbins=nbin, chi2_0=c0, chi2_A=cA, chi2_AT=cAT, chi2_AT_unbounded=cATu, dof_0=n, dof_A=n - nbin, dof_AT=n - 2 * nbin,
               A=A, AT_A=A2, AT_alpha=al, ATu_A=A3, ATu_alpha=alu)
    if perbin:
        out["per_bin"] = {}
        for b in sorted(set(BIN[sel])):
            sb = sel & (BIN == b); Lb = chol_sel(sb)
            c0b = chi2_0(m, sb, Lb); cAb, Ab = fit_A(m, sb, Lb); cATb, A2b, alb = fit_AT(m, sb, Lb, True, Ab); cATub, _, alub = fit_AT(m, sb, Lb, False, Ab)
            out["per_bin"][f"{ZB[b]:.1f}"] = dict(N=int(sb.sum()), chi2_0=c0b, chi2_A=cAb, A=Ab[ZB[b]], chi2_AT=cATb, AT_A=A2b[ZB[b]], AT_alpha=alb[ZB[b]], chi2_AT_unbounded=cATub, ATu_alpha=alub[ZB[b]])
    return out

RES = dict(lane="ABS1", criteria="adefae297a", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.", footings={})
MUT = dict(lane="ABS1", note=RES["note"], footings={})

# KA1
KA1 = dict(NB=NB, md5=FD["md5"], pass_=bool(NB == 755 and FD["md5"] == "33d7fc21bfd3d745ed71a0bbe80ca433"))
P(f"known answer KA1 loader: {NB} points, md5 {FD['md5']} -> {'PASS' if KA1['pass_'] else 'FAIL'}")
RES["KA1"] = KA1

def stored(ft, nm, src):
    G = G2 if src == "b" else G1
    return G["footings"][ft]["cases"][nm]

for ft in X.FOOTS:
    PRb = load(PB, "prim", ft); PR1 = load(P1, "prim", ft); BRb = load(PB, "br", ft); BR1 = load(P1, "br", ft)
    seeds = [0, 1, 2, 3]
    assert all(set(PRb[z].keys()) >= set(seeds) and set(PR1[z].keys()) >= set(seeds) for z in ZB)
    kv = {z: np.array(PRb[z][0]["kv"]) for z in ZB}
    kf = {z: kv[z][1] for z in ZB}
    COVER = np.array([KS[i] >= kf[ZB[BIN[i]]] for i in range(NB)])
    R = dict(cases={}, known_answers={}, twins={})
    def psum(parts, z, nm, ss, tag="primary"): return sum(np.array(parts[z][s]["flux"][tag][nm]["p"]) for s in ss)
    def Rhat(parts, z, nm, ss, tag="primary"): return psum(parts, z, nm, ss, tag) / psum(parts, z, "R", ss, tag)
    def Dof(parts, nm, ss, scale, zs=ZB, sel=None, tag="primary"):
        r = at_points(kv, {z: Rhat(parts, z, nm, ss, tag) for z in zs}); d = (r - 1.0) * scale
        if sel is None: return dchi2(d)
        d = d[sel]; return float(d @ np.linalg.solve(COV[np.ix_(sel, sel)], d))
    def DSE(parts, nm, scale):
        D = Dof(parts, nm, seeds, scale); Dj = np.array([Dof(parts, nm, [s for s in seeds if s != j], scale) for j in seeds]); n = len(seeds)
        return D, math.sqrt((n - 1) / n * np.sum((Dj - Dj.mean()) ** 2)), Dj
    def Dnoise(parts, nm, scale):
        n = len(seeds); sig = {}
        for z in ZB:
            Rj = np.array([Rhat(parts, z, nm, [s for s in seeds if s != j]) for j in seeds]); sig[z] = np.sqrt((n - 1) / n * np.sum((Rj - Rj.mean(0)) ** 2, 0))
        return dchi2((at_points(kv, {z: 1.0 + sig[z] for z in ZB}) - 1.0) * scale)
    CASES = [("J3.5", PRb, "b"), ("J4", PRb, "b"), ("J4.5", PRb, "b"), ("J5", PRb, "b"), ("U4", PRb, "b"),
             ("J3", PR1, "1"), ("J5", PR1, "1"), ("J10", PR1, "1"), ("Jinf", PR1, "1"), ("C", PR1, "1")]
    # ---------------- KA2: stored D and SE reproduced with P_data
    ka2 = {}; ok2 = True
    for nm, parts, src in CASES:
        D, SE, _ = DSE(parts, nm, PD); st = stored(ft, nm, src)
        rd, rs = abs(D / st["D"] - 1), abs(SE / st["SE"] - 1); ok = rd <= 1e-6 and rs <= 1e-6; ok2 &= ok
        ka2[f"{nm}|{src}"] = dict(D=D, D_stored=st["D"], rel_D=rd, SE=SE, SE_stored=st["SE"], rel_SE=rs, ok=bool(ok))
        P(f"[{ft}] KA2 {nm:5s} ({'FWN2 parts_b' if src == 'b' else 'FWN1R parts'}): D {D:.6f} vs stored {st['D']:.6f} (rel {rd:.1e}); SE {SE:.5f} vs {st['SE']:.5f} (rel {rs:.1e})")
    R["known_answers"]["KA2"] = dict(rows=ka2, pass_=bool(ok2))
    # ---------------- KA4 mean flux
    dm = 0.0; dt = 0.0; nf = 0
    for parts in (PRb, PR1, BRb, BR1):
        for z in parts:
            for d in parts[z].values():
                for tag, fl in d["flux"].items():
                    st_ = 0.9 if tag == "tau_x0.9" else 1.1 if tag == "tau_x1.1" else 1.0
                    tg = math.exp(-st_ * X.tau_eff(z))
                    for v in fl.values():
                        dm = max(dm, abs(v["meanF"] - v["target"])); dt = max(dt, abs(v["target"] / tg - 1)); nf += 1
    R["known_answers"]["KA4"] = dict(max_abs_meanF_minus_target=dm, max_rel_target_vs_mine=dt, fields=nf, pass_=bool(dm <= 1e-4 and dt <= 1e-12))
    P(f"[{ft}] KA4 mean flux: max |meanF - target| {dm:.2e}, target vs exp(-s tau_eff) max rel {dt:.1e}, {nf} fields -> {'PASS' if R['known_answers']['KA4']['pass_'] else 'FAIL'}")
    # ---------------- KA5 one reference in both folders
    d5 = 0.0; n5 = 0
    for z in ZB:
        for s in seeds:
            a = np.array(PRb[z][s]["flux"]["primary"]["R"]["p"])[1:]; b = np.array(PR1[z][s]["flux"]["primary"]["R"]["p"])[1:]
            d5 = max(d5, float(np.max(np.abs(a / b - 1)))); n5 += 1
    R["known_answers"]["KA5"] = dict(max_rel=d5, files=n5, pass_=bool(d5 <= 1e-12 and n5 == 48))
    P(f"[{ft}] KA5 reference R parts_b vs FWN1R parts: max rel {d5:.1e} over {n5} files -> {'PASS' if R['known_answers']['KA5']['pass_'] else 'FAIL'}")
    # ---------------- KA3 data as model
    Pdz = {}
    c3 = all_fits(PD.copy(), COVER, perbin=False)
    ka3 = c3["chi2_0"] <= 1e-20 and c3["chi2_A"] <= 1e-16 and all(abs(a - 1) <= 1e-8 for a in c3["A"].values()) and all(abs(a) <= 1e-8 for a in c3["AT_alpha"].values()) and all(abs(a - 1) <= 1e-8 for a in c3["AT_A"].values())
    R["known_answers"]["KA3"] = dict(chi2_0=c3["chi2_0"], chi2_A=c3["chi2_A"], chi2_AT=c3["chi2_AT"], max_dA=max(abs(a - 1) for a in c3["A"].values()),
                                     max_dalpha=max(abs(a) for a in c3["AT_alpha"].values()), pass_=bool(ka3))
    P(f"[{ft}] KA3 data as model: chi2_0 {c3['chi2_0']:.2e}, chi2_A {c3['chi2_A']:.2e}, chi2_AT {c3['chi2_AT']:.2e}, max |A-1| {R['known_answers']['KA3']['max_dA']:.1e}, max |alpha| {R['known_answers']['KA3']['max_dalpha']:.1e} -> {'PASS' if ka3 else 'FAIL'}")
    kaok = KA1["pass_"] and all(v["pass_"] for v in R["known_answers"].values())
    P(f"[{ft}] all known answers: {'PASS' if kaok else 'FAIL'}")
    if os.environ.get("ABS1_KA_ONLY"):                                   # known answers first, before any new number is read
        RES["footings"][ft] = R; continue
    # ================= new numbers (read only after the known answers above)
    Pref = {z: psum(PRb, z, "R", seeds) / 4.0 for z in ZB}
    m = model_at(kv, Pref)
    seedm = np.array([model_at(kv, {z: np.array(PRb[z][s]["flux"]["primary"]["R"]["p"]) for z in ZB}) for s in seeds])
    var_mean = seedm.var(0, ddof=1) / 4.0
    pos = bool(np.all(m > 0) and np.all(np.isfinite(m)))
    F = all_fits(m, COVER)
    R["fit_primary"] = F
    P(f"[{ft}] ABSOLUTE FIT, {F['N']} covered points: chi2_0 {F['chi2_0']:.1f} (dof {F['dof_0']}); amplitude per bin {F['chi2_A']:.1f} (dof {F['dof_A']}); "
      f"amplitude + tilt per bin, tilt in [-1, 1] {F['chi2_AT']:.1f} (dof {F['dof_AT']}); unbounded tilt {F['chi2_AT_unbounded']:.1f}")
    for zk, v in F["per_bin"].items():
        P(f"[{ft}]   z {zk}: N {v['N']}  chi2_0 {v['chi2_0']:.1f}  chi2_A {v['chi2_A']:.1f} (A {v['A']:.3f})  chi2_AT {v['chi2_AT']:.1f} (A {v['AT_A']:.3f}, alpha {v['AT_alpha']:+.3f})  unbounded {v['chi2_AT_unbounded']:.1f} (alpha {v['ATu_alpha']:+.3f})")
    P(f"[{ft}]   joint fit amplitudes: " + " ".join(f"{z:.1f}:{a:.3f}" for z, a in F["A"].items()))
    P(f"[{ft}]   joint fit amp+tilt: " + " ".join(f"{z:.1f}:{F['AT_A'][z]:.3f}/{F['AT_alpha'][z]:+.3f}" for z in F["AT_A"]))
    # ratio model / data at fixed k
    rat = {}
    for z in ZB:
        s_ = ZS == round(z, 2); kk = KS[s_]
        md = lambda x: float(np.exp(np.interp(math.log(x), np.log(kv[z][1:]), np.log(Pref[z][1:])))) / float(np.exp(np.interp(math.log(x), np.log(kk), np.log(PD[s_]))))
        rat[f"{z:.1f}"] = dict(k0p003=md(0.003), k0p003_held=bool(0.003 < kf[z]), k0p01=md(0.01), k0p02=md(0.02), ktop=md(float(kk.max())), ktop_value=float(kk.max()))
    R["model_over_data"] = rat
    P(f"[{ft}] model / data at k 0.003 / 0.01 / 0.02 / top: " + "; ".join(f"z {k} {v['k0p003']:.3f}{'*' if v['k0p003_held'] else ''}/{v['k0p01']:.3f}/{v['k0p02']:.3f}/{v['ktop']:.3f}" for k, v in rat.items()) + "  (* model held below k_f)")
    # variants
    allp = np.ones(NB, bool)
    V1 = all_fits(m, allp, perbin=False); V2 = all_fits(m, COVER, extra=var_mean, perbin=False)
    sel3 = np.array([KS[i] >= 3 * kf[ZB[BIN[i]]] for i in range(NB)]); V3 = all_fits(m, sel3, perbin=False)
    R["variants"] = dict(v1_all_755_held=V1, v2_seed_variance_added=V2, v3_k_ge_3kf=V3)
    for tag, V in (("v1 all 755, held", V1), ("v2 + seed variance", V2), ("v3 k >= 3 k_f", V3)):
        P(f"[{ft}] variant {tag}: N {V['N']} chi2_0 {V['chi2_0']:.1f}; A {V['chi2_A']:.1f}; AT {V['chi2_AT']:.1f} (unbounded {V['chi2_AT_unbounded']:.1f})")
    # brackets at the anchors, seeds 0, 1
    selA = COVER & np.isin(ZS, ANCH); bs2 = [0, 1]
    mp = model_at(kv, {z: psum(PRb, z, "R", bs2) / 2.0 for z in ANCH}, keys=ANCH)
    BK = {"primary": all_fits(np.where(np.isnan(mp), 1.0, mp), selA, perbin=False)}
    for tag in ("lam_x0.5", "lam_x2", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1", "lam_91.4", "lam_138.6"):
        mb = model_at(kv, {z: psum(BRb, z, "R", bs2, tag) / 2.0 for z in ANCH}, keys=ANCH)
        BK[tag] = all_fits(np.where(np.isnan(mb), 1.0, mb), selA, perbin=False)
    R["brackets_anchors"] = BK
    P(f"[{ft}] anchors z 2.2, 3.0, 4.4 (seeds 0, 1; N {BK['primary']['N']}): " + "; ".join(f"{t} {v['chi2_0']:.0f} / {v['chi2_A']:.0f} / {v['chi2_AT']:.0f}" for t, v in BK.items()) + "  (chi2_0 / amp / amp+tilt)")
    # fit word
    N = F["N"]; L1 = N + 3 * math.sqrt(2 * N); L2 = (N - 24) + 3 * math.sqrt(2 * (N - 24))
    fitw = "NOT EVALUABLE" if not kaok else "REFERENCE FITS IN ABSOLUTE TERMS" if F["chi2_0"] <= L1 else "FITS ONLY WITH NUISANCE" if F["chi2_AT"] <= L2 else "DOES NOT FIT"
    R["fit_word"] = dict(word=fitw, line_0=L1, line_AT=L2)
    # ---------------- the gate with the reference's own power
    mg = m.copy(); mgD = np.where(COVER, m, PD); mgA = m * np.array([F["A"][ZB[b]] for b in BIN])
    GT = {}
    for nm, parts, src in CASES:
        D, SE, _ = ka2[f"{nm}|{src}"]["D"], ka2[f"{nm}|{src}"]["SE"], None
        Dp, SEp, Djp = DSE(parts, nm, mg); Dn = Dnoise(parts, nm, mg)
        Dpd = Dof(parts, nm, seeds, mgD); DpA = Dof(parts, nm, seeds, mgA)
        perbin = {}
        for z in ZB:
            sz = ZS == z; perbin[f"{z:.1f}"] = Dof(parts, nm, seeds, mg, sel=sz)
        GT[f"{nm}|{src}"] = dict(D=D, SE=SE, Dp=Dp, SEp=SEp, ratio=Dp / D, D_noise_p=Dn, KA_S_pass=bool(Dn <= 0.1 * max(Dp, 4.0)), Dp_data_at_uncovered=Dpd, Dpp_amplitude_model=DpA, per_bin_Dp=perbin, Dp_jack=Djp.tolist())
        P(f"[{ft}] GATE {nm:5s} ({'b' if src == 'b' else 'FWN1R'}): stored D {D:.4f} (SE {SE:.4f}) -> D' {Dp:.4f} (SE' {SEp:.4f}); D'/D {Dp / D:.4f}; data at uncovered {Dpd:.4f}; amplitude-refit model {DpA:.4f}; D_noise' {Dn:.3g}")
        P(f"[{ft}]   {nm:5s} per-bin D': " + " ".join(f"{k}:{v:.3g}" for k, v in perbin.items()))
    # labels
    LAB = {}
    for nm, src in (("J3.5", "b"), ("J4", "b"), ("J4.5", "b"), ("J5", "1"), ("J10", "1"), ("Jinf", "1")):
        G = G2 if src == "b" else G1; lab0 = G["footings"][ft]["labels"][nm]; base0 = lab0["label"].split(",")[0]
        oth = [f for f in lab0["known_answer_or_twin_failures"] if f != "KA_S"]
        g = GT[f"{nm}|{src}"]; ok = (not oth) and g["KA_S_pass"]
        Dp, SEp = g["Dp"], g["SEp"]
        lab = "FOREST ROW HOLDS AT FLUX LEVEL" if (ok and Dp + 2 * SEp < 4) else "FOREST ROW FAILS AT FLUX LEVEL" if Dp - 2 * SEp > 4 else "NO VERDICT"
        # scale factors (on D) at which the stored label would change, for the record's D and SE
        D, SE = g["D"], g["SE"]
        LAB[nm] = dict(stored=base0, stored_full=lab0["label"], new=lab, changed=bool(lab != base0), Dp=Dp, SEp=SEp,
                       D_scale_to_reach_holds_line=4 / (D + 2 * SE), D_scale_to_reach_fails_line=4 / (D - 2 * SE) if D - 2 * SE > 0 else None,
                       crossing=bool({lab, base0} == {"FOREST ROW HOLDS AT FLUX LEVEL", "FOREST ROW FAILS AT FLUX LEVEL"}))
        P(f"[{ft}] LABEL {nm:5s}: stored {base0} -> with the reference's own power {lab} (D' {Dp:.4f}, SE' {SEp:.4f}; D' +/- 2 SE' {Dp + 2 * SEp:.4f} / {Dp - 2 * SEp:.4f})" + ("  ** CHANGED **" if lab != base0 else ""))
    gate_ok = kaok and pos
    # TW4 (gate twin) evaluated before the word
    tw4 = 0.0
    for nm, parts, src in CASES:
        tw4 = max(tw4, abs(Dof(parts, nm, seeds, 1.2 * PD) / (1.44 * ka2[f"{nm}|{src}"]["D"]) - 1))
    R["twins"]["TW4"] = dict(max_rel=tw4, bites=bool(tw4 <= 1e-10))
    P(f"[{ft}] twin TW4 gate scale 1.2 x data: D' / (1.44 D) - 1 max {tw4:.1e} -> {'bites' if tw4 <= 1e-10 else 'DOES NOT BITE'}", m=True)
    ch = [nm for nm, v in LAB.items() if v["changed"]]
    gatew = "NOT EVALUABLE" if not (gate_ok and R["twins"]["TW4"]["bites"]) else ("GATE MOVES: a frozen label of FWN2 would change sides (" + "; ".join(f"{nm} {LAB[nm]['stored']} -> {LAB[nm]['new']}" for nm in ch) + ")") if ch else "GATE UNCHANGED BY THE ABSOLUTE LEVEL"
    R["gate_word"] = dict(word=gatew, changed=ch, crossing_holds_fails=[nm for nm, v in LAB.items() if v["crossing"]], model_positive=pos)
    R["labels"] = LAB; R["gate"] = GT
    # ceiling on f with D'
    pts = [(3.0, "J3|1"), (3.5, "J3.5|b"), (4.0, "J4|b"), (4.5, "J4.5|b"), (5.0, "J5|b"), (10.0, "J10|1")]
    def cross_at(U):
        for (f1, u1), (f2, u2) in zip(U[:-1], U[1:]):
            if (u1 - 4) * (u2 - 4) <= 0 and u1 > 0 and u2 > 0 and u1 != u2:
                return math.exp(math.log(f1) + (math.log(4) - math.log(u1)) * (math.log(f2) - math.log(f1)) / (math.log(u2) - math.log(u1)))
        return None
    CE = {}
    for lab_, k in (("D+2SE", 2), ("D", 0), ("D-2SE", -2)):
        CE[lab_] = dict(stored=cross_at([(f, GT[c]["D"] + k * GT[c]["SE"]) for f, c in pts]), new=cross_at([(f, GT[c]["Dp"] + k * GT[c]["SEp"]) for f, c in pts]))
    R["ceiling"] = CE
    P(f"[{ft}] ceiling on f (reported): " + "; ".join(f"{k} = 4 at f {v['stored']:.3f} stored -> {v['new']:.3f} with D'" if (v['stored'] and v['new']) else f"{k}: {v}" for k, v in CE.items()))
    # bracket estimates with the reference's own power (reported)
    selAA = np.isin(ZS, ANCH); BE = {}
    for nm, src in (("J3.5", "b"), ("J4", "b"), ("J4.5", "b")):
        Ap = Dof(PRb, nm, bs2, mg, zs=ANCH, sel=selAA); BE[nm] = {}
        for tag in ("lam_x0.5", "lam_x2", "gam_1.2", "gam_1.6", "tau_x0.9", "tau_x1.1", "lam_91.4", "lam_138.6"):
            Ab = Dof(BRb, nm, bs2, mg, zs=ANCH, sel=selAA, tag=tag); BE[nm][tag] = GT[f"{nm}|b"]["Dp"] * Ab / Ap
        P(f"[{ft}] {nm:5s} bracket estimates with D' (reported): " + "; ".join(f"{t} {v:.4g}" for t, v in BE[nm].items()))
    R["bracket_estimates_Dp"] = BE
    # ---------------- twins of the fit
    Ls = chol_sel(COVER); mc = m[COVER]; pc = PD[COVER]
    Ci = np.linalg.solve(COV[np.ix_(COVER, COVER)], np.c_[mc, pc]); mCm = float(mc @ Ci[:, 0]); mCP = float(mc @ Ci[:, 1]); PCP = float(pc @ Ci[:, 1])
    d1 = chi2_0(1.2 * m, COVER, Ls) - F["chi2_0"]; e1 = 0.44 * mCm - 0.4 * mCP
    dd = chi2_0(1.2 * PD, COVER, Ls); ed = 0.04 * PCP
    TW1 = dict(shift=d1, predicted=e1, rel=abs(d1 / e1 - 1), data_scaled=dd, data_predicted=ed, rel_data=abs(dd / ed - 1), PCP=PCP, bites=bool(abs(d1 / e1 - 1) <= 1e-8 and abs(dd / ed - 1) <= 1e-8))
    c2, A2s = fit_A(1.2 * m, COVER, Ls); c2d, _ = fit_A(1.2 * PD, COVER, Ls)
    rA = max(abs(A2s[z] * 1.2 / F["A"][z] - 1) for z in F["A"])
    TW2 = dict(chi2_A_scaled=c2, chi2_A=F["chi2_A"], rel=abs(c2 / F["chi2_A"] - 1), max_rel_A=rA, data_scaled_chi2_A=c2d, bites=bool(abs(c2 / F["chi2_A"] - 1) <= 1e-8 and rA <= 1e-8 and c2d <= 1e-12 * PCP))
    mt = m * (KS / 0.01) ** 0.1
    cT, _, alT = fit_AT(mt, COVER, Ls, True, F["A"]); cTu, _, alTu = fit_AT(mt, COVER, Ls, False, F["A"])
    TW3 = dict(chi2_AT_tilted=cT, chi2_AT=F["chi2_AT"], rel=abs(cT / F["chi2_AT"] - 1), chi2_ATu_tilted=cTu, chi2_ATu=F["chi2_AT_unbounded"], rel_unbounded=abs(cTu / F["chi2_AT_unbounded"] - 1),
               bites=bool(abs(cT / F["chi2_AT"] - 1) <= 1e-6), bites_unbounded=bool(abs(cTu / F["chi2_AT_unbounded"] - 1) <= 1e-6),
               alpha_at_bound=[f"{z:.1f}" for z, a in F["AT_alpha"].items() if abs(abs(a) - 1) < 1e-6])
    R["twins"].update(TW1=TW1, TW2=TW2, TW3=TW3)
    P(f"[{ft}] twin TW1 model x 1.2: chi2_0 rises by {d1:.4f}, predicted {e1:.4f} (rel {TW1['rel']:.1e}); data x 1.2: {dd:.4f} vs 0.04 P'C^-1P {ed:.4f} (P'C^-1P {PCP:.1f}) -> {'bites' if TW1['bites'] else 'DOES NOT BITE'}", m=True)
    P(f"[{ft}] twin TW2 amplitude on 1.2 x model: chi2_A {c2:.6f} vs {F['chi2_A']:.6f} (rel {TW2['rel']:.1e}), A x 1.2 max rel {rA:.1e}; on 1.2 x data chi2_A {c2d:.2e} -> {'bites' if TW2['bites'] else 'DOES NOT BITE'}", m=True)
    P(f"[{ft}] twin TW3 tilt 0.1: chi2_AT {cT:.6f} vs {F['chi2_AT']:.6f} (rel {TW3['rel']:.1e}) -> {'bites' if TW3['bites'] else 'DOES NOT BITE'}; unbounded {cTu:.6f} vs {F['chi2_AT_unbounded']:.6f} (rel {TW3['rel_unbounded']:.1e}) -> {'bites' if TW3['bites_unbounded'] else 'DOES NOT BITE'}; tilts at bound in the primary fit: {TW3['alpha_at_bound'] or 'none'}", m=True)
    if not (TW1["bites"] and TW2["bites"]): R["fit_word"]["word"] = "NOT EVALUABLE (fit twin did not bite)"
    P(f"[{ft}] FIT WORD: {R['fit_word']['word']}  (chi2_0 {F['chi2_0']:.1f} vs line {L1:.1f}; chi2_AT {F['chi2_AT']:.1f} vs line {L2:.1f})")
    P(f"[{ft}] GATE WORD: {R['gate_word']['word']}")
    RES["footings"][ft] = R; MUT["footings"][ft] = R["twins"]

json.dump(RES, open(os.path.join(ODIR, "abs1.json"), "w"), indent=1)
open(os.path.join(ODIR, "abs1.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
json.dump(MUT, open(os.path.join(ODIR, "abs1_MUTATE.json"), "w"), indent=1)
open(os.path.join(ODIR, "abs1_MUTATE.out"), "w").write("\n".join(OUTM) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
