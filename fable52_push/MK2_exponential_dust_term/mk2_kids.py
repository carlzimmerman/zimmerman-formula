#!/usr/bin/env python3
"""MK2 row f (criteria 3b4f515ff8, A1 5f2304176e, A2 0fe15b8cbf): KiDS host-free lenses, ONE1's frozen statistic and gate through MK1's
machinery, with the exponential dust. Per footing and c_s: the capped Hernquist (x_a 0.2) state with the dust at every mass by
continuation in increasing mass (A1). The dust enters as a difference (A1):
    own halo   DeltaSigma = ONE1's capped point mass + [DeltaSigma_Hern,dust - DeltaSigma_Hern,no dust]   (table in log10(k M_b))
    neighbours ONE1's phantom dM/dx + [dl/dx_Hern,dust - dl/dx_Hern,no dust]                          (kernels in log10(k M_j))
so with no dust every number is ONE1's (KA4). Folded masses (no capped state) make the c_s FAIL when they fall inside the k range the
fit uses (MK1's kval: lambda in [0.3, 3]).
    python3 mk2_kids.py -> mk2_kids.json / .out, part files parts/kids/
MK1's mk1_kids.py is executed read-only up to its scan section (ONE1's data, estimator, fitter, neighbour search); nothing of MK1's
or ONE1's is written. kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import json, math, time, warnings
import numpy as np
from scipy.interpolate import CubicSpline
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MK1D = os.path.join(REPO, "fable52_push", "MK1_one_dust_constant")
sys.path.insert(0, HERE)
import mk2_lib as L
src = open(os.path.join(MK1D, "mk1_kids.py")).read()
NS = dict(__file__=os.path.join(MK1D, "mk1_kids.py"), __name__="mk1_prefix")
exec(compile(src[:src.index("COARSE = [0.03")], os.path.join(MK1D, "mk1_kids.py"), "exec"), NS)
J = NS["J"]; LB = NS["LB"]; LAMS = NS["LAMS"]; FOOT = NS["FOOT"]; A0 = NS["A0"]; A0C = NS["A0C"]; G = NS["G"]; Mpc = NS["Mpc"]; XP = NS["XP"]
UG, LUG = NS["UG"], NS["LUG"]; MSUN = 1.989e30
PARTS = os.path.join(HERE, "parts", "kids"); os.makedirs(PARTS, exist_ok=True)
OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
def tm():
    import resource; return f"[{time.time() - T0:.0f} s, {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30:.2f} GB]"
KD1 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")))
RHO = {f: KD1["footings"][f]["setting"]["I0_Mpc-2"] * L.C_SI ** 2 / (8 * math.pi * L.G) / L.MPC ** 2 for f in FOOT}
XA = 0.2
LMO = np.arange(6.0, 14.0001, 0.05); LMH = np.arange(6.0, 14.0001, 0.2)
P(f"MK2 row f KiDS (criteria 3b4f515ff8; A1 5f2304176e; A2 0fe15b8cbf). X = {XP['canonical']:.4f} / {XP['alt']:.4f}; Hernquist x_a {XA}. {L.NOTE}")

# ---------------------------------------------------------------- the Hernquist states along increasing mass
BH = L.hernquist(XA); GRIDH = L.Grid(BH, 1e-5, 1e5, h=0.01)
def prof_of(st):
    k = len(st["Phi"]); x = np.exp(st["u"][:k]); Md = st["Md"]; m = x <= st["rc"]
    x, Md = x[m], Md[m]; Ms = np.array([BH(t) for t in x]) + Md
    ell = Ms * (0.5 + np.sqrt(0.25 + x * x / np.maximum(Ms, 1e-300))); dell = np.gradient(ell, x)
    return dict(x=x, ell=ell, dell=dell, xc=float(st["rc"]))
ST0 = {}
def nodust(f):
    if f not in ST0:
        st = L.shoot_fast(GRIDH, 0, 0, 1, 0, XP[f], 1.0, 1.0, -10.0, first=True); ST0[f] = (st, prof_of(st))
    return ST0[f]
def states(f, cs, lms):
    """capped Hernquist states with the dust, continuation in increasing mass from the no-dust state. None where folded."""
    a0 = A0[f]; st0, _ = nodust(f); Pv = st0["Phi0"]; out = []; alive = True
    for lm in lms:
        if not alive: out.append(None); continue
        M = 10 ** lm * MSUN; rM = math.sqrt(G * M / a0); s = math.sqrt(G * M * a0)
        st = L.shoot_fast(GRIDH, 1, 4 * math.pi * RHO[f] * rM ** 3 / M, (cs * 1e3) ** 2 / s, 0, XP[f], 1.0, 1.0, Pv)
        if not st["ok"]: alive = False; out.append(None); continue
        Pv = st["Phi0"]; out.append(st)
    return out

def own_table(f, cs):
    fn = os.path.join(PARTS, f"own_{f}_{cs:.6g}.npz")
    if os.path.exists(fn): d = np.load(fn); return dict(R=d["R"], ok=d["ok"], maxd=float(d["maxd"]))
    _, p0 = nodust(f); D0 = LB.dsig_profile(UG, p0); base = J.rho_tab(XP[f])
    sts = states(f, cs, LMO); R = np.full((len(LMO), len(UG)), np.nan); ok = np.zeros(len(LMO), bool); maxd = 0.0
    win = (UG >= 0.3) & (UG <= 3e3)
    for i, st in enumerate(sts):
        if st is None: continue
        d = (LB.dsig_profile(UG, prof_of(st)) - D0) / J.D_INF; R[i] = base + d; ok[i] = True; maxd = max(maxd, float(np.max(np.abs(d[win]))))
    np.savez(fn, R=R, ok=ok, maxd=maxd); return dict(R=R, ok=ok, maxd=maxd)

def nb_tables(f, cs):
    fn = os.path.join(PARTS, f"nbH_{f}_{cs:.6g}.npz")
    if os.path.exists(fn):
        d = np.load(fn); return dict(HL=d["HL"], HU=d["HU"], CC=d["CC"], LD=d["LD"], fb=float(d["fb"]), xc=d["xc"], ok=d["ok"])
    X = XP[f]; xt = math.sqrt(X * (X + 1)); T0_ = J.build_H(X); nd = len(T0_["DG"])
    HL = np.zeros((len(LMH) + 1, nd, LB.NW), np.float32); HU = np.zeros_like(HL); CC = np.zeros((len(LMH) + 1, nd)); xc = np.full(len(LMH) + 1, np.nan); ok = np.zeros(len(LMH) + 1, bool)
    HL[0], HU[0], CC[0], xc[0], ok[0] = T0_["HL"], T0_["HU"], T0_["CC"], xt, True
    _, p0 = nodust(f); sts = states(f, cs, LMH)
    for i, st in enumerate(sts):
        if st is None: continue
        pd = prof_of(st); xe = max(xt, pd["xc"], p0["xc"]); x = np.geomspace(1e-5, xe, 6000); lx = np.log(x)
        dm = np.where(x <= xt, x / np.sqrt(0.25 + x * x), 0.0)
        dm = dm + np.where(x <= pd["xc"], np.interp(lx, np.log(pd["x"]), pd["dell"]), 0.0) - np.where(x <= p0["xc"], np.interp(lx, np.log(p0["x"]), p0["dell"]), 0.0)
        T = LB.build_H_prof(dict(x=x, dell=dm, xc=xe, ell=None), X)
        HL[i + 1], HU[i + 1], CC[i + 1], xc[i + 1], ok[i + 1] = T["HL"], T["HU"], T["CC"], xe, True
    np.savez(fn, HL=HL, HU=HU, CC=CC, LD=T0_["LD"], fb=T0_["fb"], xc=xc, ok=ok)
    return dict(HL=HL, HU=HU, CC=CC, LD=T0_["LD"], fb=T0_["fb"], xc=xc, ok=ok)

# ---------------------------------------------------------------- own cells and sums (bilinear in log u and log10 k M_b)
LU0, DLU = LUG[0], LUG[1] - LUG[0]
def cells(f, k, TAB, kval_k, CH=6000):
    a0 = A0[f]; C = np.zeros((J.n1, 10)); nf = 0
    for c0 in range(0, J.n1, CH):
        sl = slice(c0, min(c0 + CH, J.n1)); g = k * J.GB1[sl]; fl = J.glaw(g, a0); lu = 0.5 * np.log(a0 / g)
        if TAB is None:
            rat = np.interp(lu, LUG, J.rho_tab(XP[f]))
        else:
            lm = np.log10(k * J.Mg1[sl] / MSUN); fm = (lm - LMO[0]) / 0.05; im = np.clip(np.floor(fm).astype(np.int64), 0, len(LMO) - 2); am = np.clip(fm - im, 0, 1)
            fu = (lu - LU0) / DLU; iu = np.clip(np.floor(fu).astype(np.int64), 0, len(UG) - 2); au = np.clip(fu - iu, 0, 1)
            R = TAB["R"]; a_ = im[:, None, None]; w_ = am[:, None, None]
            rat = (1 - w_) * ((1 - au) * R[a_, iu] + au * R[a_, iu + 1]) + w_ * ((1 - au) * R[a_ + 1, iu] + au * R[a_ + 1, iu + 1])
            bad = ~(TAB["ok"][im] & TAB["ok"][im + 1])
            if kval_k: nf += int(bad.sum())
            rat = np.where(np.isfinite(rat), rat, np.interp(lu, LUG, J.rho_tab(XP[f])))
        C[sl] = np.where(J.OKC1[sl], (fl * rat * J.WGL[None, None, :]).sum(-1) / 2, 0.0)
    return C, nf
def own_sums(f, TAB):
    out = {mk: np.zeros((len(J.KGRID), J.NPAT, 10)) for mk in J.MASKS}; lam = np.sqrt(J.KGRID * A0C / A0[f]); kval = (lam >= min(LAMS)) & (lam <= max(LAMS)); nf = 0
    for ik, k in enumerate(J.KGRID):
        C, n_ = cells(f, k, TAB, bool(kval[ik])); nf = max(nf, n_); W = J.WW1 * C
        for mk, msk in J.MASKS.items(): out[mk][ik] = J.psum(W, msk)
    return out, nf

# ---------------------------------------------------------------- neighbours (MK1's streamed pairs; kernel index by log10 k M_j)
def nb_term(f, HT):
    X = XP[f]; rMC = np.sqrt(G * J.mN / A0C); nset = 1 + len(J.PERMS)
    real = np.zeros((len(LAMS), J.n1, 10)); shuf = np.zeros((len(LAMS), J.n1, 10)); nfold = 0
    for iset, pos in enumerate([None] + list(range(len(J.PERMS)))):
        acc = real if iset == 0 else shuf
        for li, j, d in NS["pair_chunks"](X, pos):
            pref = 4 * G * (1 + X) * J.mN[j] / math.pi; R1c = J.R1e[li]; R2c = J.R2e[li]; OKc = J.OKC1[li]; RHc = J.RH1[li]
            for il, lam in enumerate(LAMS):
                if HT is None: ti = np.zeros(len(j), np.int64)
                else:
                    lm = np.log10(lam ** 2 * A0[f] / A0C * J.mN[j] / MSUN); fi = (lm - LMH[0]) / 0.2
                    ti = np.clip(np.rint(fi).astype(np.int64), 0, len(LMH) - 1) + 1
                HTc = HT if HT is not None else NOHT[f]
                okp = HTc["ok"][ti]
                if iset == 0: nfold = max(nfold, int(np.sum(~okp)))
                xc = np.where(okp, HTc["xc"][ti], HTc["xc"][0]); ti = np.where(okp, ti, 0); rt = lam * xc * rMC[j]; sel = d < (RHc + rt)
                for cb in range(10):
                    r1, r2, okc = R1c[:, cb], R2c[:, cb], OKc[:, cb]; K = np.zeros(len(j)); act = okc & (d < r2 + rt) & sel
                    if act.any():
                        a_ = np.where(act)[0]; inside = r1[a_] > d[a_] + rt[a_]
                        K[a_[inside]] = 2 * np.log(r2[a_[inside]] / r1[a_[inside]]); g_ = a_[~inside]
                        if len(g_):
                            K[g_] = LB.H_eval_multi(r2[g_] / rt[g_], d[g_] / rt[g_], HTc, ti[g_]) - LB.H_eval_multi(r1[g_] / rt[g_], d[g_] / rt[g_], HTc, ti[g_])
                    val = np.where(okc, pref * K / (r2 ** 2 - r1 ** 2), 0.0); acc[il, :, cb] += np.bincount(li, weights=val, minlength=J.n1)
    return real - shuf / (nset - 1), nfold
NOHT = {}
for f in FOOT:
    T0_ = J.build_H(XP[f]); NOHT[f] = dict(HL=T0_["HL"][None].astype(np.float32), HU=T0_["HU"][None].astype(np.float32), CC=T0_["CC"][None], LD=T0_["LD"], fb=T0_["fb"],
                                           xc=np.array([math.sqrt(XP[f] * (XP[f] + 1))]), ok=np.array([True]))

def grade(f, TAB, HT):
    OS, nfo = own_sums(f, TAB); NBn, nbf = nb_term(f, HT)
    lam_of_k = np.sqrt(J.KGRID * A0C / A0[f]); kval = (lam_of_k >= min(LAMS)) & (lam_of_k <= max(LAMS)); res = {}
    for mk in [("KO1", 1.6, s) for s in ("all", "late", "early")]:
        NBS = np.stack([J.psum(J.WW1 * NBn[il], J.MASKS[mk]) for il in range(len(LAMS))]); cs_ = CubicSpline(np.log(LAMS), NBS, axis=0)
        S_nb = np.stack([J.KGRID[ik] * cs_(math.log(min(max(lam_of_k[ik], min(LAMS)), max(LAMS)))) for ik in range(len(J.KGRID))])
        res[mk] = J.fit(mk, f, OS[mk] + S_nb, kvalid=kval)
    if any(v is None for v in res.values()): return dict(status="FAIL", reason="no k fit", own_folded=nfo, nb_folded=nbf)
    g = {}
    for sub in ("all", "late", "early"):
        q = res[("KO1", 1.6, sub)]; g[f"G-K1 {sub}"] = dict(z=q["z"], ok=bool(abs(q["diff"]) <= 2 * q["s_diff"]), Rs_model=q["Rs_model"], Rs_data=q["Rs_data"], k=q["k"])
    qa = res[("KO1", 1.6, "all")]; g["G-K2 all profile"] = dict(chi2=qa["chi2"], ok=bool(qa["chi2"] <= 9.49))
    qe, ql = res[("KO1", 1.6, "early")], res[("KO1", 1.6, "late")]; dd = qe["diff"] - ql["diff"]; sd = J.jk(qe["diff_l"] - ql["diff_l"])
    g["G-K3 type difference"] = dict(z=dd / sd, ok=bool(abs(dd) <= 2 * sd))
    folded = nfo > 0 or nbf > 0
    return dict(status="PASS" if all(v["ok"] for v in g.values()) and not folded else "FAIL", lines=g, own_folded=nfo, nb_folded=nbf,
                failing=[k for k, v in g.items() if not v["ok"]] + (["no capped state for some masses in the fitted k range"] if folded else []))
def line_of(r):
    if "lines" not in r: return f"{r['status']} ({r.get('reason')})"
    g = r["lines"]
    return (f"z all/late/early {g['G-K1 all']['z']:+.2f}/{g['G-K1 late']['z']:+.2f}/{g['G-K1 early']['z']:+.2f}; R_s model {g['G-K1 all']['Rs_model']:.3f} (k {g['G-K1 all']['k']:.2f}); "
            f"chi2 {g['G-K2 all profile']['chi2']:.2f}; type z {g['G-K3 type difference']['z']:+.2f}; folded {r['own_folded']}/{r['nb_folded']} -> {r['status']}")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
def point(f, cs):
    fn = os.path.join(PARTS, f"pt_{f}_{cs:.6g}.json")
    if os.path.exists(fn): return json.load(open(fn))
    t0 = time.time()
    if cs is None or cs >= 1e7:
        r = grade(f, None, None); r["dust"] = "none"
    else:
        TAB = own_table(f, cs)
        if TAB["maxd"] < 1e-4 and TAB["ok"].all():
            r = dict(point(f, 1e7)); r["dust"] = f"negligible (max |dDeltaSigma|/DeltaSigma_inf {TAB['maxd']:.1e} < 1e-4): the no-dust result"
        else:
            HT = nb_tables(f, cs); r = grade(f, TAB, HT); r["dust"] = f"max own |dDeltaSigma|/DeltaSigma_inf {TAB['maxd']:.3g}"
    r["cs"] = cs; r["seconds"] = time.time() - t0; json.dump(clean(r), open(fn, "w"), indent=1); return json.load(open(fn))

RES = dict(lane="MK2", row="f KiDS host-free, capped", criteria="3b4f515ff8 (A1 5f2304176e, A2 0fe15b8cbf)", note=L.NOTE, KA={}, rows={})
REF = {"canonical": (-1.141, -1.459, -0.651), "alt": (-0.232, -1.231, 0.214)}
GRIDF = [1000.0, 500.0, 300.0, 200.0, 150.0, 120.0, 100.0, 80.0, 60.0, 40.0]
for f in FOOT:
    r0 = point(f, 1e7); g = r0["lines"]; zs = (g["G-K1 all"]["z"], g["G-K1 late"]["z"], g["G-K1 early"]["z"]); dz = max(abs(a - b) for a, b in zip(zs, REF[f]))
    RES["KA"][f"KA4 KiDS no dust {f}"] = dict(z=zs, dz=dz, ok=bool(dz <= 0.02)); P(f"KA4 [{f}] no dust: z {zs[0]:+.3f}/{zs[1]:+.3f}/{zs[2]:+.3f} (ONE1 {REF[f]}) -> {'PASS' if dz <= 0.02 else 'FAIL'}  {tm()}")
    pts = {}
    for cs in GRIDF:
        r = point(f, cs); pts[cs] = r; P(f"  [{f}] c_s {cs:6.1f}: {line_of(r)}; {r.get('dust')}  {tm()}")
        if r["status"] != "PASS": break
    for _ in range(2):
        ok_ = [c for c in sorted(pts, reverse=True) if pts[c]["status"] == "PASS"]; lo = None
        for c in sorted(pts, reverse=True):
            if pts[c]["status"] == "PASS": lo = c
            else: break
        hi = next((c for c in sorted(pts, reverse=True) if pts[c]["status"] != "PASS"), None)
        if lo is None or hi is None: break
        for m in (float(f"{v:.4g}") for v in np.geomspace(hi, lo, 4)[1:3]):
            if m in pts: continue
            r = point(f, m); pts[m] = r; P(f"  [{f}] refine c_s {m:6.1f}: {line_of(r)}; {r.get('dust')}  {tm()}")
    lo = None
    for c in sorted(pts, reverse=True):
        if pts[c]["status"] == "PASS": lo = c
        else: break
    first_fail = next((c for c in sorted(pts, reverse=True) if pts[c]["status"] != "PASS"), None)
    RES["rows"][f"f {f}"] = dict(points={f"{k:g}": v for k, v in sorted(pts.items(), reverse=True)}, lower_bound=lo, first_fail=first_fail)
    P(f"[{f}] row f: c_s >= {lo} km/s passes (first fail {first_fail})  {tm()}")
RES["KA_all_pass"] = all(v["ok"] for v in RES["KA"].values())
json.dump(clean(RES), open(os.path.join(HERE, "mk2_kids.json"), "w"), indent=1)
open(os.path.join(HERE, "mk2_kids.out"), "w").write("\n".join(OUT + [f"runtime {time.time() - T0:.0f} s", L.NOTE]) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
