#!/usr/bin/env python3
"""NP2 core: NP1's Gaussian-process leaf rule (imported read-only from ../NP1_nonparametric_rule/np1_core.py) projected onto the admissible set, g rising with g_b along the
stars-only and gas-only directions (FROZEN_CRITERIA C1); Upsilon-profiled SPARC rows (C3); admissibility checker (C4); gates for mode U; hull report.
See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import os, sys, math, pickle
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True; os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import numpy as np
from scipy.linalg import cho_factor, cho_solve, cholesky, solve_triangular
from scipy.optimize import nnls
from scipy.stats import qmc
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); NP1D = os.path.join(RB, "NP1_nonparametric_rule")
sys.path.insert(0, NP1D)
import np1_core as C
DD = C.DD; LN10 = math.log(10.0); EPS = 0.05; LAMS = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0); NC_FINAL, NC_CV = 2 ** 15, 2 ** 13; ADD, ROUNDS, TIGHT, WMAX, WMAX_CV = 300, 80, 1e-3, 4000, 2000   # TIGHT: solve at eps + 1e-3 so the nnls tolerance can't leave a 1e-6 violation (AMENDMENT_A1)
UPS = np.round(np.arange(0.30, 1.2000001, 0.01), 2)   # CRG1 SPEC set E, crg1_sparc.UPS; bulge 1.4 x disc (crg1_sparc.gB_mat)
WIDE = dict(logy=(-8.0, 14.0), logell=(-18.0, -2.0), f=(0.0, 1.0), s=(-4.0, 5.0))

# ---------- the law's slope and the admissible directions
def law_slope(y, a0):
    """sigma_law = d log g_law / d log g_b at g_b = y A0C, footing a0."""
    x = np.clip(np.asarray(y, float) * C.A0C / a0, 1e-30, 1e30); q = np.sqrt(0.25 * x * x + x); return x * (0.5 + (0.5 * x + 1) / (2 * q)) / (0.5 * x + q)   # scale-free form, overflow-safe
def directions(F, arm):
    """Raw-leaf change per unit log10 y (i.e. per unit log10 g_b) for stars-only, gas-only, fixed share; s and ell held."""
    n, d = F.shape; base = np.zeros((n, d)); base[:, 0] = 1.0; f = F[:, 2]
    if arm == "L5": D = np.sinh(F[:, 4]); base[:, 4] = LN10 * D / np.sqrt(1 + D * D)
    st = base.copy(); st[:, 2] = -f * LN10; ga = base.copy(); ga[:, 2] = (1 - f) * LN10
    return dict(stars=st, gas=ga, share=base)
def feats_from_box(P, arm):
    """P columns: log y, log ell, f (, s). L5 appends asinh D from SY1's D formula."""
    if arm == "L3": return P.copy()
    u = np.log10(np.maximum(2.0 + P[:, 3], 1e-300)) + P[:, 0] - math.log10(16 * math.pi) - P[:, 1]   # log10 D, SY1's D formula, overflow-safe
    aD = np.where(P[:, 3] <= -2.0, 0.0, np.where(u > 300, math.log(2) + u * LN10, np.arcsinh(10 ** np.minimum(u, 300)))); return np.column_stack([P, aD])

# ---------- kernel pieces in standardised coordinates
def _K(A, B, ell, sf2): return C.kern(A, B, ell, sf2)
def K_XD(X, Zc, Vc, ell, sf2):
    """cov(m(x_i), v_j . grad m(z_j)) = k(x_i, z_j) v_j.(x_i - z_j)/ell^2."""
    K = _K(X, Zc, ell, sf2); Vl = Vc / ell ** 2; return K * ((X @ Vl.T) - (Vl * Zc).sum(1)[None, :])
def K_DD(Zc, Vc, ell, sf2):
    Vl = Vc / ell ** 2; vz = (Vl * Zc).sum(1)
    a = Zc @ Vl.T; a -= vz[None, :]   # a[j,k] = v_k.(z_j - z_k)/ell^2
    M = a.T * a; del a; M += Vc @ Vl.T  # v_j.v_k/ell^2 - (v_j.(z_j-z_k)/ell^2)(v_k.(z_j-z_k)/ell^2), with v_j.(z_j-z_k) = -a[k,j]
    M *= _K(Zc, Zc, ell, sf2); return M

class CRule:
    """Frozen admissible rule: m(x) = sum_i alpha_i k(x, x_i) + sum_j beta_j v_j.grad_z k(x, z_j), standardised coordinates; g = law(g_b, a0_foot) 10^m."""
    def __init__(s, arm, mu, sd, Z, alpha, ell, sf2, Zc=None, Vc=None, beta=None, meta=None):
        s.arm, s.mu, s.sd, s.Z, s.alpha, s.ell, s.sf2, s.meta = arm, np.asarray(mu, float), np.asarray(sd, float), Z, alpha, np.asarray(ell, float), float(sf2), meta or {}
        d = Z.shape[1]; s.Zc = np.zeros((0, d)) if Zc is None else Zc; s.Vc = np.zeros((0, d)) if Vc is None else Vc; s.beta = np.zeros(0) if beta is None else beta
    def std(s, F): return (F - s.mu) / s.sd
    def m_std(s, Zq, chunk=2000):
        out = np.empty(len(Zq))
        for i in range(0, len(Zq), chunk):
            q = Zq[i:i + chunk]; v = _K(q, s.Z, s.ell, s.sf2) @ s.alpha
            if len(s.beta): v += K_XD(q, s.Zc, s.Vc, s.ell, s.sf2) @ s.beta
            out[i:i + chunk] = v
        return out
    def m(s, F):
        F = np.asarray(F, float); ok = np.all(np.isfinite(F), 1); out = np.full(len(F), np.nan)
        if ok.any(): out[ok] = s.m_std(s.std(F[ok]))
        return out
    def dgrad_std(s, Zq, U, chunk=500):
        """U_c . grad m at Zq_c, U in standardised units."""
        out = np.empty(len(Zq)); ell2 = s.ell ** 2
        for i in range(0, len(Zq), chunk):
            q = Zq[i:i + chunk]; u = U[i:i + chunk] / ell2; uq = (u * q).sum(1)
            K = _K(q, s.Z, s.ell, s.sf2); v = -(uq * (K @ s.alpha) - (K * (u @ s.Z.T)) @ s.alpha)
            if len(s.beta):
                Kc = _K(q, s.Zc, s.ell, s.sf2); Vl = s.Vc / ell2; a = uq[:, None] - u @ s.Zc.T; b = q @ Vl.T - (Vl * s.Zc).sum(1)[None, :]; e = u @ s.Vc.T
                v += (Kc * (e - a * b)) @ s.beta
            out[i:i + chunk] = v
        return out
    def slopes(s, F, a0):
        """S_v for stars, gas, share at raw leaves F."""
        Zq = s.std(F); y = 10 ** np.clip(F[:, 0], -300, 300); sl = law_slope(y, a0); return {k: sl + s.dgrad_std(Zq, v / s.sd) for k, v in directions(F, s.arm).items()}
    def save(s, p): np.savez(p, arm=s.arm, mu=s.mu, sd=s.sd, Z=s.Z, alpha=s.alpha, ell=s.ell, sf2=s.sf2, Zc=s.Zc, Vc=s.Vc, beta=s.beta)
    @staticmethod
    def load(p, meta=None):
        R = dict(np.load(p)); return CRule(str(R["arm"]), R["mu"], R["sd"], R["Z"], R["alpha"], R["ell"], float(R["sf2"]), R["Zc"], R["Vc"], R["beta"], meta)

# ---------- constraint set and the projected fit
def _rss():
    import resource; return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def box_points(Ftr, arm, ell_std, sd, n, seed):
    """Sobol points in the constraint box: train range padded by 3 frozen lengths per continuous leaf; f in [0, 1]. Returns raw features."""
    k = 3 if arm == "L3" else 4; cols = [0, 1, 2] if arm == "L3" else [0, 1, 2, 3]; lo, hi = [], []
    for j in cols:
        if j == 2: lo.append(0.0); hi.append(1.0); continue
        pad = 3 * ell_std[j] * sd[j]; lo.append(Ftr[:, j].min() - pad); hi.append(Ftr[:, j].max() + pad)
    P = qmc.scale(qmc.Sobol(k, scramble=True, seed=seed).random(n), lo, hi); return feats_from_box(P, arm)
def wide_points(arm, n=2 ** 16, seed=20261104):
    k = 3 if arm == "L3" else 4; keys = ["logy", "logell", "f", "s"][:k]
    P = qmc.scale(qmc.Sobol(k, scramble=True, seed=seed).random(n), [WIDE[q][0] for q in keys], [WIDE[q][1] for q in keys]); return feats_from_box(P, arm)
def constrained_fit(arm, mu, sd, Z, t, cls, ell, sf2, nv, Fc, a0, log=None, wmax=WMAX):
    """Posterior mode of the GP projected onto {S_v >= EPS on every point of Fc, v in stars, gas}. Dual NNQP on an active set."""
    n = len(t); Kc = cho_factor(C.kern(Z, Z, ell, sf2) + np.diag(nv), lower=True); a0v = cho_solve(Kc, t)
    Dr = directions(Fc, arm); Zc_all = np.vstack([(Fc - mu) / sd] * 2); Vc_all = np.vstack([Dr["stars"] / sd, Dr["gas"] / sd])
    c_all = np.tile(EPS - law_slope(10 ** np.clip(Fc[:, 0], -300, 300), a0), 2); c_tgt = c_all + TIGHT; W = np.zeros(0, int); mu_ = np.zeros(0); rule = CRule(arm, mu, sd, Z, a0v, ell, sf2); conv = False; nviol = None
    for rnd in range(ROUNDS + 1):
        g = rule.dgrad_std(Zc_all, Vc_all); viol = c_all - g; bad = np.nonzero(viol > 1e-6)[0]; nviol = len(bad)
        if log: log(f"      round {rnd}: active {len(W)}, violations {nviol}, worst {viol.max():+.4f}, RSS {_rss():.2f} GB")
        if nviol == 0: conv = True; break
        if rnd == ROUNDS: break
        new = bad[np.argsort(-viol[bad])]; new = new[~np.isin(new, W)][:ADD]
        if len(new) == 0 or len(W) + len(new) > wmax: break   # AMENDMENT_A2: working-set cap for the 1 GB RSS limit; hitting it = not converged
        W = np.r_[W, new]; Zw, Vw = Zc_all[W], Vc_all[W]
        KXD = K_XD(Z, Zw, Vw, ell, sf2); S = cho_solve(Kc, KXD); A = K_DD(Zw, Vw, ell, sf2) - KXD.T @ S; A = 0.5 * (A + A.T); A[np.diag_indices_from(A)] += 1e-9 * max(np.mean(np.diag(A)), 1e-12)
        b = c_tgt[W] - KXD.T @ a0v; L = cholesky(A, lower=True); mu_, _ = nnls(L.T, solve_triangular(L, b, lower=True), maxiter=50 * len(W))
        keep = mu_ > 0; rule = CRule(arm, mu, sd, Z, a0v - S[:, keep] @ mu_[keep], ell, sf2, Zw[keep], Vw[keep], mu_[keep]); 
        # AMENDMENT_A3: the working set only grows (shedding slack functionals made the active set cycle); capped at wmax
    rule.meta = dict(conv=conv, rounds=rnd, active=int((mu_ > 0).sum()) if len(mu_) else 0, working=len(W), viol_left=int(nviol)); return rule

def pool(F, arm, ell, sd, nc):
    """Enforcement pool (FROZEN_CRITERIA C1 set C, plus AMENDMENT_A2 refinement R): C = Sobol nc in the constraint box (seed 20261103); R = the fit's train rows,
    Sobol 2 nc in the constraint box (seed 20261105), Sobol 2 nc in the wide box (seed 20261106). The checker's wide set (seed 20261104) stays outside the pool."""
    return np.vstack([box_points(F, arm, ell, sd, nc, 20261103), F, box_points(F, arm, ell, sd, 2 * nc, 20261105), wide_points(arm, 2 * nc, 20261106)])
def fit_admissible(arm, F, t, cls, sysid, a0, log=None, ml=None):
    """Step A (NP1's ML, unconstrained), step B (lambda by grouped CV on the constrained fit, 2^13 constraint points), final constrained fit (2^15)."""
    mu, sd = F.mean(0), F.std(0); Z = (F - mu) / sd; hp = ml or C.ml_fit(Z, t, cls); nv = C.noise_vec(cls, hp["sX"], hp["sS"])
    fold = np.empty(len(t), int)
    for c_ in (0, 1):
        m = cls == c_; u = sorted(set(sysid[m].tolist())); ix = {s: i % 4 for i, s in enumerate(u)}; fold[m] = [ix[s] for s in sysid[m]]
    L = {}; cvinfo = {}
    for lam in LAMS:
        ell = lam * hp["ell"]; Fc = pool(F, arm, ell, sd, NC_CV); e = {0: [], 1: []}; info = []
        for k in range(4):
            tr = fold != k; te = ~tr; r = constrained_fit(arm, mu, sd, Z[tr], t[tr], cls[tr], ell, hp["sf2"], nv[tr], Fc, a0, wmax=WMAX_CV); p = r.m_std(Z[te]); info.append(r.meta)
            if not r.meta["conv"]: break   # AMENDMENT_A3: a lambda whose fold fit can't be made admissible is ineligible
            for c_ in (0, 1): e[c_] += list((t[te] - p)[cls[te] == c_])
        ok = len(info) == 4 and all(q["conv"] for q in info); L[lam] = 0.5 * (np.mean(np.square(e[0])) + np.mean(np.square(e[1]))) if ok else np.inf; cvinfo[str(lam)] = dict(loss=float(L[lam]), conv=ok, active=[q["active"] for q in info], eligible=ok)
        if log: log(f"    CV lam {lam}: loss {L[lam]:.6f}, folds converged {cvinfo[str(lam)]['conv']}, active {cvinfo[str(lam)]['active']}")
    best = min(L.values())
    if not np.isfinite(best): lam = LAMS[-1]; cvinfo["none_eligible"] = True
    else: lam = max(l for l in LAMS if L[l] <= best * (1 + 1e-12))
    ell = lam * hp["ell"]
    Fc = pool(F, arm, ell, sd, NC_FINAL); rule = constrained_fit(arm, mu, sd, Z, t, cls, ell, hp["sf2"], nv, Fc, a0, log)
    rule.meta = dict(ml=dict(ell=np.asarray(hp["ell"]).tolist(), sf=math.sqrt(hp["sf2"]), sX=hp["sX"], sS=hp["sS"], nll=hp.get("nll"), conv=hp.get("conv")), lam=lam, lam_at_edge=lam == LAMS[-1], cv=cvinfo, n=len(t), fit=rule.meta)
    return rule

# ---------- SPARC rows with Upsilon per galaxy (BF1's loader, Upsilon as input)
_G = {}
def sparc_gals():
    if _G: return _G["g"]
    Q = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb"))["gals"]; meta = {g["name"]: g for g in Q}; D = os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "sparc", "rotmod"); out = []
    for i, n in enumerate(sorted(meta)):
        if meta[n]["Q"] >= 3 or meta[n]["inc"] < 30: continue
        t = np.atleast_2d(np.loadtxt(os.path.join(D, n + "_rotmod.dat"), comments="#")); out.append(dict(i=i, name=n, r=t[:, 0], v=t[:, 1], e=t[:, 2], vg=t[:, 3], vd=t[:, 4], vb=t[:, 5]))
    _G["g"] = out; return out
B = DD._B; PC, KMS2, A0B, CB = B["PC"], B["KMS2"], B["A0"], B["C"]
def gal_rows(g, Y):
    """BF1's row tuple (g_b, g_obs, ell, f, index) at Upsilon_disc Y, bulge 1.4 Y; same filters. Also returns the CRG1 weight per row."""
    m = abs(g["vg"]) * g["vg"] + Y * abs(g["vd"]) * g["vd"] + (1.4 * Y) * abs(g["vb"]) * g["vb"]; R = g["r"] * 1e3 * PC; ok = (g["r"] > 0) & (g["v"] > 0) & (m > 0)
    A = np.column_stack([m * KMS2 / R, g["v"] * g["v"] * KMS2 / R, R * A0B / CB ** 2, np.minimum(1.0, np.maximum(0.0, abs(g["vg"]) * g["vg"] / m)), np.full(len(m), float(g["i"]))])[ok]
    w = (1.0 / (np.maximum(g["e"], 1) / np.maximum(g["v"], 1)) ** 2)[ok]; return A, w
def sparc_at(par, Ymap=None):
    """All rows of parity par with Upsilon per galaxy index (default 0.5)."""
    rows = [gal_rows(g, 0.5 if Ymap is None else Ymap[g["i"]])[0] for g in sparc_gals() if g["i"] % 2 == par]; return np.vstack(rows)
def profile(par, a0, rule=None, arm=None):
    """Upsilon per galaxy of parity par: argmin over UPS of CRG1's weighted mean squared log10 residual, under the plain law (rule None) or a rule."""
    gals = [g for g in sparc_gals() if g["i"] % 2 == par]; blocks = []; meta = []
    for g in gals:
        for k, Y in enumerate(UPS):
            A, w = gal_rows(g, Y); blocks.append(A); meta.append((g["i"], k, w))
    Aall = np.vstack(blocks); mm = np.zeros(len(Aall))
    if rule is not None:
        Fs = [];
        for A in blocks: Fs.append(C.feats(A, arm))
        mm = rule.m(np.vstack(Fs))
    res = np.log10(Aall[:, 1]) - np.log10(C.law(Aall[:, 0], a0)) - mm; Q = {}; p = 0
    for (gi, k, w), A in zip(meta, blocks):
        r = res[p:p + len(A)]; p += len(A); q = float((w * r * r).sum() / w.sum()) if len(A) and np.all(np.isfinite(r)) else np.inf; Q.setdefault(gi, []).append(q)
    return {gi: float(UPS[int(np.argmin(q))]) if np.isfinite(q).any() else 0.5 for gi, q in Q.items()}

# ---------- mode-U gates 2 and 3 (SPARC lines), the rest from NP1's gates14
def u_sparc_gates(rule, a0, Ytr, Ytr_law, arm):
    """Gate 2: train at Ytr (U1) vs 1.05 x law rms at Ytr_law (U0). Gate 3: even galaxies profiled under the rule vs law profiled under the law."""
    rms = C.rms; o = {}
    ST1 = sparc_at(1, Ytr); d2 = C.target(ST1, a0) - rule.m(C.feats(ST1, arm)); l2 = C.SF * rms(C.target(sparc_at(1, Ytr_law), a0))
    o["g2U"] = dict(rms=rms(d2), med=float(np.median(d2)), line=l2, ok=bool(np.all(np.isfinite(d2)) and rms(d2) <= l2 and abs(np.median(d2)) <= C.SM), Y_med=float(np.median(list(Ytr.values()))))
    Yh = profile(0, a0, rule, arm); Yhl = profile(0, a0); SH1 = sparc_at(0, Yh); d3 = C.target(SH1, a0) - rule.m(C.feats(SH1, arm)); l3 = C.SF * rms(C.target(sparc_at(0, Yhl), a0))
    o["g3SU"] = dict(rms=rms(d3), med=float(np.median(d3)), line=l3, ok=bool(np.all(np.isfinite(d3)) and rms(d3) <= l3 and abs(np.median(d3)) <= C.SM), Y_med=float(np.median(list(Yh.values()))), Y_med_law=float(np.median(list(Yhl.values()))))
    return o, Yh, SH1

# ---------- admissibility checker (C4)
def check(rule, a0, extra_F=(), cand=None, cx=None):
    """Strict S_v > 0 at the wide Sobol set, train rows and extra rows, three directions; end-to-end NP1-post test through the RQ3 candidate if given."""
    out = {}; tot = 0
    for tag, F in [("wide", wide_points(rule.arm))] + list(extra_F):
        S = rule.slopes(F, a0); q = {k: int(np.sum(~(v > 0))) for k, v in S.items()}; q["min"] = float(min(np.nanmin(v) for v in S.values())); q["n"] = len(F); out[tag] = q; tot += sum(q[k] for k in ("stars", "gas", "share"))
    if cand is not None:
        RS, gq, foot = cand; o = {}
        for L in C.CX_LINES + ("SPARC",):
            if L == "SPARC": gb = C.SH[:, 0]; r = C.SH[:, 2] * C.CL ** 2 / C.A0C; gg = gb * C.SH[:, 3]
            else:
                q_ = [x for x in cx if x["line"] == L]; gb = np.array([x["y"] for x in q_]) * C.A0C; r = np.array([x["ell"] for x in q_]) * C.CL ** 2 / C.A0C; gg = gb * np.array([x["f"] for x in q_])
            dec = 0
            for k in range(len(gb)):
                g = np.geomspace(0.3, 3.0, 25) * gb[k]; v = gq(RS, dict(gb=g, gg=g * (gg[k] / gb[k]), r=np.full(25, r[k]), a0=a0)); dec += bool(np.any(~(np.diff(v) > 0)))
            o[L] = dict(n=len(gb), non_monotone=dec); tot += dec
        out["end_to_end"] = o
    out["violations"] = int(tot); out["admissible"] = tot == 0; return out

# ---------- hull report (NP1's method; SPARC holdout rows passed in)
def hull_report(rule, cx, arm, a0, SHx):
    rep = {}; kh = 4 if arm == "L5" else 3
    def loc(F): Zq = rule.std(F); return C.hull_mask(rule.Z[:, :kh], Zq[:, :kh]), C.reach(rule, Zq)
    for k, A in (("SPARC", SHx), ("XCOP", C.XH), ("LT", C.LTA)):
        h, r = loc(C.feats(A, arm)); d = C.target(A, a0) - rule.m(C.feats(A, arm)); q = dict(n=len(A), in_hull=float(h.mean()), reach1=float((r <= 1).mean()))
        if k == "SPARC": line = C.SF * C.rms(C.target(A[h], a0)) if h.any() else np.nan; q.update(inhull_rms=C.rms(d[h]) if h.any() else None, inhull_line=line, inhull_ok=bool(h.any() and C.rms(d[h]) <= line and abs(np.median(d[h])) <= C.SM))
        if k == "XCOP": q.update(inhull_mean=float(d[h].mean()) if h.any() else None, inhull_ok=bool(h.any() and abs(d[h].mean()) <= C.XM and C.rms(d[h]) <= C.XR))
        if k == "LT": q.update(inhull_med=float(np.median(d[h])) if h.any() else None, inhull_ok=bool(h.any() and abs(np.median(d[h])) <= C.LTT))
        rep[k] = q
    F = C.cx_feats(cx, arm); h, r = loc(F); line = np.array([q["line"] for q in cx])
    for L in C.CX_LINES:
        s = line == L; rep[L] = dict(n=int(s.sum()), in_hull=float(h[s].mean()) if s.any() else None, reach1=float((r[s] <= 1).mean()) if s.any() else None)
    return rep
