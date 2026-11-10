#!/usr/bin/env python3
"""MK1 row 6 (criteria b1fbded1e2, amendment A1 916f4e0e22): KiDS host-free lenses, ONE1's frozen statistic and gate (1.6 R_h veto,
KO1 tie rule, R_s = A(outer)/A(inner), k fitted on the inner window per jackknife, neighbours carrying the same profile, five shuffles
subtracted), with the static dust of action (A) inside form B's cap: own halo and every neighbour at its own m = mu_K r_M(k M_b).
Also: KA2 (ONE1 at mu_K = 0 through these tables), KA6 (tables at m = 0 = ONE1's), the uncapped reading (own halo, no neighbours,
S4's zero point), and the MUTATE arms M-NOCAP, M-2X, M-SIGN (separate outputs).
    python3 mk1_kids.py            -> mk1_kids.json / .out, mk1_kids_MUTATE.json / .out ; part files in parts/kids/
ONE1's one1_kids.py is executed read-only up to its section 7 (data, estimator, fitter, neighbour trees); nothing of ONE1's is written.
Preemptible: every (variant, footing, mu_K) result is a part file; a rerun skips finished parts.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, math, time, signal, warnings, resource
import numpy as np
from scipy.interpolate import CubicSpline
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import mk1_lib as LB
ONE1D = os.path.join(REPO, "fable52_push", "ONE1_counted_once")
PARTS = os.path.join(HERE, "parts", "kids"); os.makedirs(PARTS, exist_ok=True)
CRIT = "b1fbded1e2 (A1 916f4e0e22)"; T0 = time.time(); OUT = []; OUTM = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def PM(s=""): print("[MUTATE] " + s, flush=True); OUTM.append(str(s))
def tm(): return f"[{time.time() - T0:.0f} s, {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30:.2f} GB]"
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.update(flag=True))

# ---------------------------------------------------------------- ONE1's sections 1-6, read-only
src = open(os.path.join(ONE1D, "one1_kids.py")).read()
cut = src.index("# =================================================================== 7. known answers on the kernel and the projection")
NS = dict(__file__=os.path.join(ONE1D, "one1_kids.py"), __name__="one1_prefix")
exec(compile(src[:cut], os.path.join(ONE1D, "one1_kids.py"), "exec"), NS)
J = type("NS", (), NS)
P(f"MK1 row 6 KiDS (criteria {CRIT}). ONE1 sections 1-6 executed read-only; host-free 1.6 R_h lenses {int(J.HF[1.6].sum()):,}  {tm()}")
XP = J.XP; A0 = J.A0; G = J.G; Mpc = J.Mpc; A0C = J.A0C; FOOT = J.FOOT; NPAT = J.NPAT
UG, LUG = J.UG, J.LUG

# ---------------------------------------------------------------- tables
LM0, DLM, NM = -4.0, 0.05, 101                   # own-halo ratio table: log10 m from -4 to +1
MGRID = 10 ** (LM0 + DLM * np.arange(NM))
LMH0, DLMH, NMH = -3.5, 0.1, 46                  # neighbour kernels: log10 m from -3.5 to +1 (index 0 = m 0)
MGRID_H = 10 ** (LMH0 + DLMH * np.arange(NMH))
LAMS = list(np.geomspace(0.3, 3.0, 11))

def own_table(X, sig):
    fn = os.path.join(PARTS, f"own_X{X:.4f}_s{int(sig):+d}.npz")
    if os.path.exists(fn):
        d = np.load(fn); return dict(R=d["R"], ok=d["ok"], xc=d["xc"], phineg=d["phineg"], mono=d["mono"])
    B = LB.capped_branch(list(MGRID), X, sig); R = np.ones((NM + 1, len(UG))); ok = np.zeros(NM + 1, bool); xc = np.full(NM + 1, np.nan)
    p0 = LB.capped_profile(0.0, X); R[0] = LB.dsig_profile(UG, p0) / J.D_INF; ok[0] = True; xc[0] = p0["xc"]
    phineg = np.ones(NM + 1, bool); mono = np.ones(NM + 1, bool)
    for i, p in enumerate(B):
        if p["ok"]:
            R[i + 1] = LB.dsig_profile(UG, p) / J.D_INF; ok[i + 1] = True; xc[i + 1] = p["xc"]; phineg[i + 1] = p["phi_neg"]; mono[i + 1] = p["kap_mono"]
        else:
            R[i + 1] = np.nan
    np.savez(fn, R=R, ok=ok, xc=xc, phineg=phineg, mono=mono)
    return dict(R=R, ok=ok, xc=xc, phineg=phineg, mono=mono)

def nb_tables(X, sig):
    """stacked neighbour kernel tables: index 0 = m 0 (dust-free), 1.. = MGRID_H; folded entries flagged."""
    fn = os.path.join(PARTS, f"nbH_X{X:.4f}_s{int(sig):+d}.npz")
    if os.path.exists(fn):
        d = np.load(fn); return dict(HL=d["HL"], HU=d["HU"], CC=d["CC"], LD=d["LD"], fb=float(d["fb"]), xc=d["xc"], ok=d["ok"])
    p0 = LB.capped_profile(0.0, X); T0_ = LB.build_H_prof(p0, X); nd = len(T0_["DG"])
    HL = np.zeros((NMH + 1, nd, LB.NW), np.float32); HU = np.zeros_like(HL); CC = np.zeros((NMH + 1, nd)); xc = np.full(NMH + 1, np.nan); ok = np.zeros(NMH + 1, bool)
    HL[0], HU[0], CC[0], xc[0], ok[0] = T0_["HL"], T0_["HU"], T0_["CC"], p0["xc"], True
    B = LB.capped_branch(list(MGRID_H), X, sig)
    for i, p in enumerate(B):
        if not p["ok"]: continue
        T = LB.build_H_prof(p, X); HL[i + 1], HU[i + 1], CC[i + 1], xc[i + 1], ok[i + 1] = T["HL"], T["HU"], T["CC"], p["xc"], True
    HL = HL.astype(np.float32); HU = HU.astype(np.float32)
    np.savez(fn, HL=HL, HU=HU, CC=CC, LD=T0_["LD"], fb=T0_["fb"], xc=xc, ok=ok)
    return dict(HL=HL, HU=HU, CC=CC, LD=T0_["LD"], fb=T0_["fb"], xc=xc, ok=ok)

# ---------------------------------------------------------------- own-halo cells with dust (bilinear in log u, log10 m)
LU0, DLU = LUG[0], LUG[1] - LUG[0]
def cells_dust(a0, k, mu_m, TAB, CH=6000):
    """model cells (n1, 10): g_law(k g_bar) x DeltaSigma_dust(u; m) / DeltaSigma_inf(u), m = mu_K r_M(k M_b) per lens.
    Returns (cells, n_folded_lenses, n_clipped). Computed in chunks of CH lenses (memory)."""
    C = np.zeros((J.n1, 10)); nf = 0; ncl = 0; R = TAB["R"]
    for c0 in range(0, J.n1, CH):
        sl = slice(c0, min(c0 + CH, J.n1))
        g = k * J.GB1[sl]; f = J.glaw(g, a0); lu = 0.5 * np.log(a0 / g)
        if mu_m <= 0:
            rat = np.interp(lu, LUG, R[0])
        else:
            m = mu_m * np.sqrt(G * k * J.Mg1[sl] / a0)
            lm = np.log10(m); fm = (lm - LM0) / DLM; ncl += int(np.sum(fm > NM - 1))
            im = np.clip(np.floor(fm).astype(np.int64), -1, NM - 2); am = np.clip(fm - im, 0.0, 1.0)
            low = fm < 0
            r0i = np.where(low, 0, im + 1); r1i = np.where(low, 1, im + 2); wm = np.where(low, np.clip(m / MGRID[0], 0, 1), am)
            fu = (lu - LU0) / DLU; iu = np.clip(np.floor(fu).astype(np.int64), 0, len(UG) - 2); au = np.clip(fu - iu, 0.0, 1.0)
            a_ = r0i[:, None, None]; b_ = r1i[:, None, None]; w_ = wm[:, None, None]
            rat = (1 - w_) * ((1 - au) * R[a_, iu] + au * R[a_, iu + 1]) + w_ * ((1 - au) * R[b_, iu] + au * R[b_, iu + 1])
            nf += int((~(TAB["ok"][r0i] & TAB["ok"][r1i])).sum())
        C[sl] = np.where(J.OKC1[sl], (f * rat * J.WGL[None, None, :]).sum(-1) / 2, 0.0)
    return C, nf, ncl

def own_sums_dust(f, mu_m, TAB):
    out = {mk: np.zeros((len(J.KGRID), NPAT, 10)) for mk in J.MASKS}; nfold = np.zeros(len(J.KGRID), int)
    for ik, k in enumerate(J.KGRID):
        C, nf, _ = cells_dust(A0[f], k, mu_m, TAB); nfold[ik] = nf
        C = np.nan_to_num(C, nan=0.0); W = J.WW1 * C
        for mk, msk in J.MASKS.items(): out[mk][ik] = J.psum(W, msk)
    return out, nfold

# ---------------------------------------------------------------- neighbour pairs, streamed per lens chunk (real + 5 shuffles; ONE1's search)
def pair_chunks(X, pos):
    """yields (li, j, d) for position set pos (None = real, else shuffle index), search radius R_h + lmax r_t0 (lmax = 1.1 max(LAMS):
    the M-SIGN branch has x_c <= 1.07 x_t, A1 test)."""
    xt = math.sqrt(X * (X + 1)); rt0 = xt * np.sqrt(G * J.mN / A0C); lmax = max(LAMS) * 1.1
    Lx = J.XL1 if pos is None else J.XL1[J.PERMS[pos]]; Ls = J.SELF1 if pos is None else J.SELF1[J.PERMS[pos]]
    for (ii, tree) in J.TREES:
        if tree is None: continue
        rext = lmax * rt0[ii].max()
        for i0 in range(0, J.n1, 400):
            i1 = min(i0 + 400, J.n1); th = (J.RH1[i0:i1] + rext) / J.DAl1[i0:i1]
            lists = tree.query_ball_point(Lx[i0:i1], r=2 * np.sin(np.minimum(th, math.pi) / 2))
            c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(c.sum())
            if tot == 0: continue
            li = i0 + np.repeat(np.arange(len(c)), c); j = ii[np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot)]
            keep = (j != Ls[li]) & (np.abs(J.chiN[j] - J.chil1[li]) < 230.0); li, j = li[keep], j[keep]
            d = 2 * np.arcsin(np.minimum(np.linalg.norm(J.xN[j] - Lx[li], axis=1) / 2, 1.0)) * J.DAl1[li]
            keep = d < (J.RH1[li] + lmax * rt0[j])
            if keep.any(): yield li[keep], j[keep], d[keep]

def nb_term(X, mu_m, HT):
    """net neighbour term per unit k (len(LAMS), n1, 10): real minus the mean of five shuffles. Each neighbour j at lambda carries
    total (1 + X) M_b,j, its capped dust profile at m_j = mu lambda r_MC,j (table nearest in log10 m), end radius lambda x_c(m_j) r_MC,j."""
    rMC = np.sqrt(G * J.mN / A0C); nset = 1 + len(J.PERMS)
    real = np.zeros((len(LAMS), J.n1, 10)); shuf = np.zeros((len(LAMS), J.n1, 10)); nfold = 0; npair = 0
    for iset, pos in enumerate([None] + list(range(len(J.PERMS)))):
        acc = real if iset == 0 else shuf
        for li, j, d in pair_chunks(X, pos):
            if iset == 0: npair += len(j)
            pref = 4 * G * (1 + X) * J.mN[j] / math.pi; R1c = J.R1e[li]; R2c = J.R2e[li]; OKc = J.OKC1[li]; RHc = J.RH1[li]
            for il, lam in enumerate(LAMS):
                if mu_m > 0:
                    m = mu_m * lam * rMC[j]; fi = (np.log10(m) - LMH0) / DLMH
                    ti = np.where(fi < -0.5, 0, np.clip(np.rint(fi).astype(np.int64), 0, NMH - 1) + 1)
                else:
                    ti = np.zeros(len(j), np.int64)
                okp = HT["ok"][ti]
                if iset == 0: nfold = max(nfold, int(np.sum(~okp & (d < RHc + lam * HT["xc"][0] * rMC[j]))))
                xc = np.where(okp, HT["xc"][ti], HT["xc"][0]); rt = lam * xc * rMC[j]
                sel = d < (RHc + rt)
                for cb in range(10):
                    r1, r2, okc = R1c[:, cb], R2c[:, cb], OKc[:, cb]
                    K = np.zeros(len(j)); act = okc & (d < r2 + rt) & sel
                    if act.any():
                        a_ = np.where(act)[0]; rta = rt[a_]
                        inside = r1[a_] > d[a_] + rta
                        K[a_[inside]] = 2 * np.log(r2[a_[inside]] / r1[a_[inside]])
                        g_ = a_[~inside]
                        if len(g_):
                            h2 = LB.H_eval_multi(r2[g_] / rt[g_], d[g_] / rt[g_], HT, ti[g_])
                            K[g_] = h2 - LB.H_eval_multi(r1[g_] / rt[g_], d[g_] / rt[g_], HT, ti[g_])
                    val = np.where(okc, pref * K / (r2 ** 2 - r1 ** 2), 0.0)
                    acc[il, :, cb] += np.bincount(li, weights=val, minlength=J.n1)
    return real - shuf / (nset - 1), nfold, npair


# ---------------------------------------------------------------- one grading point
def grade_point(f, X, mu_m, TAB, HT, with_nb=True):
    OS, nfo = own_sums_dust(f, mu_m, TAB); res = {}
    lam_of_k = np.sqrt(J.KGRID * A0C / A0[f]); kval = (lam_of_k >= min(LAMS)) & (lam_of_k <= max(LAMS))
    nb_fold = 0
    if with_nb:
        NBn, nb_fold, npair = nb_term(X, mu_m, HT)
    for mk in [("KO1", 1.6, s) for s in ("all", "late", "early")] + [("KO1", 1.0, "all")]:
        S_own = OS[mk]
        if with_nb:
            NBS = np.stack([J.psum(J.WW1 * NBn[il], J.MASKS[mk]) for il in range(len(LAMS))]); cs = CubicSpline(np.log(LAMS), NBS, axis=0)
            S_nb = np.stack([J.KGRID[ik] * cs(math.log(min(max(lam_of_k[ik], min(LAMS)), max(LAMS)))) for ik in range(len(J.KGRID))])
            r = J.fit(mk, f, S_own + S_nb, kvalid=kval)
        else:
            r = J.fit(mk, f, S_own)
        res[mk] = r
    g = {}
    if any(res[("KO1", 1.6, s)] is None for s in ("all", "late", "early")):
        return dict(status="FAIL", reason="no k fit (model never reaches the data's inner amplitude)", own_folded_max=int(nfo.max()), nb_folded=nb_fold)
    for sub in ("all", "late", "early"):
        q = res[("KO1", 1.6, sub)]; g[f"G-K1 {sub}"] = dict(diff=q["diff"], sigma=q["s_diff"], z=q["z"], ok=bool(abs(q["diff"]) <= 2 * q["s_diff"]), Rs_model=q["Rs_model"], Rs_data=q["Rs_data"], k=q["k"])
    qa = res[("KO1", 1.6, "all")]; g["G-K2 all profile"] = dict(chi2=qa["chi2"], line=9.49, ok=bool(qa["chi2"] <= 9.49))
    qe, ql = res[("KO1", 1.6, "early")], res[("KO1", 1.6, "late")]
    dd = qe["diff"] - ql["diff"]; sd = J.jk(qe["diff_l"] - ql["diff_l"]); g["G-K3 type difference"] = dict(diff=dd, sigma=sd, z=dd / sd, ok=bool(abs(dd) <= 2 * sd))
    folded = int(nfo.max()) > 0 or nb_fold > 0
    st = "PASS" if (all(v["ok"] for v in g.values()) and not folded) else "FAIL"
    q10 = res[("KO1", 1.0, "all")]
    return dict(status=st, nb_pairs=(npair if with_nb else 0), lines=g, failing=[k for k, v in g.items() if not v["ok"]] + (["no capped state for some lenses (folded)"] if folded else []),
                own_folded_max=int(nfo.max()), nb_folded=nb_fold, reported_1p0_all=dict(z=q10["z"], Rs_model=q10["Rs_model"]) if q10 else None)

def run_point(tag, f, X, sig, mu, TAB, HT, with_nb=True):
    fn = os.path.join(PARTS, f"pt_{tag}_{f}_{mu:.6g}.json")
    if os.path.exists(fn): return json.load(open(fn))
    t0 = time.time(); r = grade_point(f, X, mu / Mpc, TAB, HT, with_nb); r["mu_K"] = mu; r["seconds"] = time.time() - t0
    json.dump(clean(r), open(fn, "w"), indent=1); return json.load(open(fn))

def clean(o):
    if isinstance(o, dict): return {(str(k) if not isinstance(k, tuple) else "|".join(map(str, k))): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o

def line_of(r):
    if "lines" not in r: return f"mu {r['mu_K']:.4g}: {r['status']} ({r.get('reason')})"
    g = r["lines"]
    return (f"mu {r['mu_K']:.4g}: z all/late/early {g['G-K1 all']['z']:+.2f}/{g['G-K1 late']['z']:+.2f}/{g['G-K1 early']['z']:+.2f}; R_s model all {g['G-K1 all']['Rs_model']:.3f} "
            f"(k {g['G-K1 all']['k']:.2f}); chi2 {g['G-K2 all profile']['chi2']:.2f}; type diff z {g['G-K3 type difference']['z']:+.2f}; folded own/nb {r['own_folded_max']}/{r['nb_folded']} -> {r['status']}")

def scan(tag, f, X, sig, TAB, HT, coarse, with_nb=True, printer=P):
    """coarse grid, then two log-midpoints between the last pass and the first fail (refined once more if they straddle)."""
    pts = {}
    for mu in coarse:
        if STOP["flag"]: raise SystemExit("SIGTERM: stopped between points; rerun resumes")
        r = run_point(tag, f, X, sig, mu, TAB, HT, with_nb); pts[mu] = r; printer(f"  [{tag} {f}] " + line_of(r) + f"  {tm()}")
    def bound(pts):
        ms = sorted(pts); last = None
        for mu in ms:
            if pts[mu]["status"] == "PASS": last = mu
            else: return last, mu
        return last, None
    for rnd in range(2):
        lo, hi = bound(pts)
        if lo is None or hi is None: break
        mids = list(np.geomspace(lo, hi, 4)[1:3]) if lo > 0 else [hi / 10.0, hi / 3.0]
        for mu in mids:
            mu = float(f"{mu:.4g}")
            if mu in pts: continue
            r = run_point(tag, f, X, sig, mu, TAB, HT, with_nb); pts[mu] = r; printer(f"  [{tag} {f}] refine " + line_of(r) + f"  {tm()}")
    lo, hi = bound(pts)
    return dict(points={f"{k:.6g}": v for k, v in sorted(pts.items())}, upper_bound=lo, first_fail=hi)

COARSE = [0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
RES = dict(lane="MK1", row="6 KiDS host-free, capped", criteria=CRIT, X=XP, LAMS=LAMS, note=LB.NOTE, KA={}, rows={})
MUT = dict(lane="MK1", row="6 KiDS MUTATE", criteria=CRIT, arms={})

# ---------------------------------------------------------------- KA6: tables at m = 0 against ONE1's
for f in FOOT:
    X = XP[f]; TAB = own_table(X, 1.0); sel = (UG >= 0.3) & (UG <= 1000)
    d6a = float(np.max(np.abs(TAB["R"][0][sel] - J.rho_tab(X)[sel])))
    T1 = J.build_H(X); HT = nb_tables(X, 1.0)
    d6b = float(max(np.max(np.abs(HT["HL"][0] - T1["HL"])), np.max(np.abs(HT["HU"][0] - T1["HU"])), np.max(np.abs(HT["CC"][0] - T1["CC"]))))
    RES["KA"][f"KA6 {f}"] = dict(own_ratio_maxdiff=d6a, kernel_maxdiff=d6b, ok=bool(d6a <= 1e-3 and d6b <= 1e-3))
    br = [(float(MGRID[i]), float(TAB["xc"][i + 1])) for i in range(0, NM, 10)]
    P(f"KA6 [{f}] X {X:.4f}: own ratio at m 0 vs ONE1 rho_tab max |d| {d6a:.1e}; kernel at m 0 vs ONE1 build_H max |d| {d6b:.1e} -> {'PASS' if RES['KA'][f'KA6 {f}']['ok'] else 'FAIL'}; "
      f"branch folded entries own {int((~TAB['ok']).sum())}, kernel {int((~HT['ok']).sum())}; phi<0 everywhere {bool(TAB['phineg'][TAB['ok']].all())}, dust monotone {bool(TAB['mono'][TAB['ok']].all())}  {tm()}")
    P(f"   branch x_c(m): " + ", ".join(f"m {a:.0e}: {b:.2f}" for a, b in br))
    RES.setdefault("branch", {})[f] = dict(m=MGRID.tolist(), xc=TAB["xc"][1:].tolist())
    del T1

# ---------------------------------------------------------------- KA2 and the primary scan, per footing
REF = {"canonical": dict(z=(-1.141, -1.459, -0.651), Rs=1.003, chi2=1.915), "alt": dict(z=(-0.232, -1.231, 0.214), Rs=0.847, chi2=0.868)}
for f in FOOT:
    X = XP[f]; TAB = own_table(X, 1.0); HT = nb_tables(X, 1.0)
    r0 = run_point("primary", f, X, 1.0, 0.0, TAB, HT)
    g = r0["lines"]; zs = (g["G-K1 all"]["z"], g["G-K1 late"]["z"], g["G-K1 early"]["z"])
    dz = max(abs(a - b) for a, b in zip(zs, REF[f]["z"])); dR = abs(g["G-K1 all"]["Rs_model"] - REF[f]["Rs"]); dc = abs(g["G-K2 all profile"]["chi2"] - REF[f]["chi2"])
    ok = bool(dz <= 0.02 and dR <= 0.005 and dc <= 0.1); RES["KA"][f"KA2 {f}"] = dict(z=zs, Rs=g["G-K1 all"]["Rs_model"], chi2=g["G-K2 all profile"]["chi2"], dz=dz, dRs=dR, dchi2=dc, ok=ok)
    P(f"KA2 [{f}] mu_K 0 through MK1's tables: z {zs[0]:+.3f}/{zs[1]:+.3f}/{zs[2]:+.3f} (ONE1 {REF[f]['z']}), R_s {g['G-K1 all']['Rs_model']:.4f} ({REF[f]['Rs']}), chi2 {g['G-K2 all profile']['chi2']:.3f} ({REF[f]['chi2']}) "
      f"-> max |dz| {dz:.3f}, |dRs| {dR:.4f}, |dchi2| {dc:.3f}: {'PASS' if ok else 'FAIL'}  {tm()}")
    P(f"=== PRIMARY capped scan [{f}] X {X:.4f}")
    RES["rows"][f"primary {f}"] = scan("primary", f, X, 1.0, TAB, HT, [0.0] + COARSE)
    P(f"[{f}] capped upper bound: {RES['rows'][f'primary {f}']['upper_bound']} (first fail {RES['rows'][f'primary {f}']['first_fail']})  {tm()}")

# ---------------------------------------------------------------- uncapped reading (the old bound; also MUTATE M-NOCAP): own halo, no neighbours
def uncapped_table(f, mu):
    fn = os.path.join(PARTS, f"unc_{f}_{mu:.6g}.npz")
    if os.path.exists(fn):
        d = np.load(fn); return dict(R=d["R"], ok=d["ok"], xc=d["xc"])
    a0 = A0[f]; R = np.ones((NM + 1, len(UG))); ok = np.ones(NM + 1, bool)
    rMs = np.sqrt(G * np.outer(J.KGRID, J.Mg1) / a0); mlo, mhi = (mu / Mpc) * rMs.min() / 1.3, (mu / Mpc) * rMs.max() * 1.3
    for i, m in enumerate(MGRID):
        if not (mlo <= m <= mhi or (i < NM - 1 and MGRID[i + 1] >= mlo and m <= mhi)): R[i + 1] = np.nan; ok[i + 1] = False; continue
        rM = m / (mu / Mpc); x3 = 3 * Mpc / rM; xend = 30 * Mpc / rM
        if x3 < 1.0: R[i + 1] = np.nan; ok[i + 1] = False; continue
        p = LB.uncapped_profile(m, x3, xend); q = LB.uncapped_profile(0.0, x3, xend)
        if not p["ok"]: R[i + 1] = np.nan; ok[i + 1] = False; continue
        R[i + 1] = LB.dsig_profile(UG, p) / LB.dsig_profile(UG, q)     # pure dust effect: m -> 0 gives exactly the law with no end
    np.savez(fn, R=R, ok=ok, xc=np.full(NM + 1, np.nan)); return dict(R=R, ok=ok, xc=np.full(NM + 1, np.nan))

for f in FOOT:
    P(f"=== UNCAPPED reading [{f}] (law with no end + dust, S4 zero point, own halo only, k fitted, no neighbours)")
    pts = {}
    r = run_point("uncapped", f, np.inf, 1.0, 0.0, dict(R=np.ones((NM + 1, len(UG))), ok=np.ones(NM + 1, bool)), None, with_nb=False); pts[0.0] = r
    P(f"  [uncapped {f}] " + line_of(r) + "  (ONE1's law with no end, own halo, no neighbours)")
    for mu in COARSE:
        TABu = uncapped_table(f, mu); r = run_point("uncapped", f, np.inf, 1.0, mu, TABu, None, with_nb=False); pts[mu] = r
        P(f"  [uncapped {f}] " + line_of(r) + f"  {tm()}")
    ms = sorted(pts); last = None; ff = None
    for mu in ms:
        if pts[mu]["status"] == "PASS": last = mu
        else: ff = mu; break
    RES["rows"][f"uncapped {f}"] = dict(points={f"{k:.6g}": v for k, v in sorted(pts.items())}, upper_bound=last, first_fail=ff,
                                        note="own halo only, no neighbours (as ONE1's law-with-no-end reading); coarse grid only")
    P(f"[{f}] uncapped upper bound (coarse grid): {last} (first fail {ff})")

ka_ok = all(v["ok"] for v in RES["KA"].values()); RES["KA_all_pass"] = ka_ok
P(f"Known answers (row 6): {sum(v['ok'] for v in RES['KA'].values())} of {len(RES['KA'])} PASS")
json.dump(clean(RES), open(os.path.join(HERE, "mk1_kids.json"), "w"), indent=1)
open(os.path.join(HERE, "mk1_kids.out"), "w").write("\n".join(OUT + [f"runtime {time.time() - T0:.0f} s", LB.NOTE]) + "\n")

# ---------------------------------------------------------------- MUTATE arms (separate outputs)
PM("M-NOCAP = the uncapped reading above (mk1_kids.json rows 'uncapped *'); compared with the capped bound in mk1_grade.py")
def passing(sc): return [float(k) for k, v in sc["points"].items() if v["status"] == "PASS"]
for f in FOOT:
    X2 = 2 * XP[f]; TAB2 = own_table(X2, 1.0); TAB1 = own_table(XP[f], 1.0)
    PM(f"M-2X [{f}] share doubled X {X2:.3f}: lens's own halo only, no neighbours (as ONE1's M2: the doubled halos' neighbour search is ~4x longer), "
       f"against the primary's own-halo-only reading on the same grid")
    arm = scan("M2X_own", f, X2, 1.0, TAB2, None, [0.0] + COARSE, with_nb=False, printer=PM)
    ref = scan("primary_own", f, XP[f], 1.0, TAB1, None, [0.0] + COARSE, with_nb=False, printer=PM)
    MUT["arms"][f"M-2X {f}"] = dict(arm=arm, primary_own_only=ref, upper_bound=arm["upper_bound"], first_fail=arm["first_fail"], passing=passing(arm),
                                    primary_own_upper=ref["upper_bound"], primary_own_passing=passing(ref))
    PM(f"[{f}] M-2X own halo: passing grid points {passing(arm)} (upper bound {arm['upper_bound']}); primary own halo: passing {passing(ref)} (upper bound {ref['upper_bound']})  {tm()}")
for f in FOOT:
    X = XP[f]; TAB = own_table(X, -1.0); HT = nb_tables(X, -1.0)
    PM(f"M-SIGN [{f}] dust sign flipped (branch folds at m ~ 1.3e-3, A1)")
    MUT["arms"][f"M-SIGN {f}"] = scan("MSIGN", f, X, -1.0, TAB, HT, [0.0, 0.03, 0.1, 0.3, 1.0], printer=PM)
    PM(f"[{f}] M-SIGN upper bound {MUT['arms'][f'M-SIGN {f}']['upper_bound']} (first fail {MUT['arms'][f'M-SIGN {f}']['first_fail']})  {tm()}")
json.dump(clean(MUT), open(os.path.join(HERE, "mk1_kids_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "mk1_kids_MUTATE.out"), "w").write("\n".join(OUTM + [LB.NOTE]) + "\n")
P(f"done {tm()}")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
