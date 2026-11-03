#!/usr/bin/env python3
"""NP1 core: BF1/SY1 data and leaves (read from their lanes, unedited), Gaussian-process rule for log10 B on the leaves, gates 1-4, hull and reach,
CX1's centre rows for the other lines. See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import os, sys, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True; os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize, linprog
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
SYD = os.path.join(RB, "SY1_free_constant_law_search"); CXD = os.path.join(RB, "CX1_leaf_collision")
sys.path.insert(0, SYD)
import sy1_data as DD
from sy1_leaves import A0C, CL, D_leaf, slope_1d
XT, XH, ST, SH = DD.XT, DD.XH, DD.ST, DD.SH; LTA = DD.lt_rows(); law = DD.law; X_ALL = DD._B["X"]
FOOT = dict(canonical=A0C, alt=DD.ALT); ARMS = ("L3", "L5"); LAMS = (0.25, 0.5, 1.0, 2.0, 4.0)
XM, XR, SF, SM, LTT = DD.XM0, DD.XR0, DD.SF, DD.SM, 0.10
STARTS = ((1.0, 0.3, 0.05, 0.10), (0.5, 0.5, 0.10, 0.15), (2.0, 0.2, 0.03, 0.05), (0.3, 1.0, 0.20, 0.20))
def rms(d): return float(np.sqrt(np.mean(d * d)))

# ---------- leaves and features
def feats_from(c, arm):
    F = [np.log10(c["y"]), np.log10(c["ell"]), c["f"]]
    if arm == "L5": F += [c["s"], np.arcsinh(c["D"])]
    return np.column_stack(F)
def feats(A, arm): return feats_from(DD._cols(A), arm)
def target(A, a0, gobs=None): return np.log10((A[:, 1] if gobs is None else gobs) / law(A[:, 0], a0))

# ---------- Gaussian process: ARD squared exponential, prior mean 0 (the plain law), noise per row
def _sq(Za, Zb):
    d = (Za * Za).sum(1)[:, None] + (Zb * Zb).sum(1)[None, :] - 2 * Za @ Zb.T; return np.maximum(d, 0.0)
def kern(Za, Zb, ell, sf2): return sf2 * np.exp(-0.5 * _sq(Za / ell, Zb / ell))
def noise_vec(cls, sX, sS, extra=None):
    v = np.where(cls == 0, sX * sX, sS * sS).astype(float)
    if extra is not None: m = cls == 2; v[m] = extra[m] ** 2
    return v
def ml_fit(Z, t, cls):
    """Step A: type-II ML for log ell_d, log sf, log sX, log sS; analytic gradient; 4 fixed starts."""
    n, d = Z.shape; D2 = [(Z[:, k][:, None] - Z[:, k][None, :]) ** 2 for k in range(d)]; isX = cls == 0; isS = cls == 1
    def nll(p):
        ell = np.exp(p[:d]); sf2 = np.exp(2 * p[d]); sX, sS = np.exp(p[d + 1]), np.exp(p[d + 2])
        E = np.zeros((n, n))
        for k in range(d): E += D2[k] / ell[k] ** 2
        Kf = sf2 * np.exp(-0.5 * E); K = Kf + np.diag(noise_vec(cls, sX, sS))
        try: c = cho_factor(K, lower=True)
        except np.linalg.LinAlgError: return 1e10, np.zeros_like(p)
        a = cho_solve(c, t); Ki = cho_solve(c, np.eye(n)); f = 0.5 * t @ a + np.log(np.diag(c[0])).sum() + 0.5 * n * math.log(2 * math.pi)
        W = np.outer(a, a) - Ki; g = np.empty_like(p)
        for k in range(d): g[k] = -0.5 * np.sum(W * Kf * D2[k]) / ell[k] ** 2
        g[d] = -0.5 * np.sum(W * Kf) * 2; dW = np.diag(W); g[d + 1] = -0.5 * dW[isX].sum() * 2 * sX * sX; g[d + 2] = -0.5 * dW[isS].sum() * 2 * sS * sS
        return f, g
    bnd = [(math.log(0.02), math.log(50.0))] * d + [(math.log(1e-3), math.log(10.0)), (math.log(1e-3), 0.0), (math.log(1e-3), 0.0)]; best = None
    for l0, s0, x0, q0 in STARTS:
        p0 = np.r_[np.full(d, math.log(l0)), math.log(s0), math.log(x0), math.log(q0)]
        r = minimize(nll, p0, jac=True, method="L-BFGS-B", bounds=bnd, options=dict(maxiter=300))
        if best is None or r.fun < best.fun: best = r
    p = best.x; return dict(ell=np.exp(p[:d]), sf2=float(np.exp(2 * p[d])), sX=float(np.exp(p[d + 1])), sS=float(np.exp(p[d + 2])), nll=float(best.fun), conv=bool(best.success))
def posterior(Z, t, cls, ell, sf2, nv):
    K = kern(Z, Z, ell, sf2) + np.diag(nv); c = cho_factor(K, lower=True); return cho_solve(c, t)
def predict(Zq, Z, alpha, ell, sf2, chunk=2000):
    out = np.empty(len(Zq))
    for i in range(0, len(Zq), chunk): out[i:i + chunk] = kern(Zq[i:i + chunk], Z, ell, sf2) @ alpha
    return out
def cv_lambda(Z, t, cls, sysid, hp):
    """Step B: 4-fold grouped CV by system; loss = half (X-COP mse + SPARC mse); ties to larger lambda."""
    fold = np.empty(len(t), int)
    for c_ in (0, 1):
        m = cls == c_; u = sorted(set(sysid[m].tolist())); ix = {s: i % 4 for i, s in enumerate(u)}; fold[m] = [ix[s] for s in sysid[m]]
    nv = noise_vec(cls, hp["sX"], hp["sS"]); L = {}
    for lam in LAMS:
        e = {0: [], 1: []}
        for k in range(4):
            tr = fold != k; te = ~tr; a = posterior(Z[tr], t[tr], cls[tr], lam * hp["ell"], hp["sf2"], nv[tr]); p = predict(Z[te], Z[tr], a, lam * hp["ell"], hp["sf2"])
            for c_ in (0, 1): e[c_] += list((t[te] - p)[cls[te] == c_])
        L[lam] = 0.5 * (np.mean(np.square(e[0])) + np.mean(np.square(e[1])))
    best = min(L.values()); lam = max(l for l in LAMS if L[l] <= best * (1 + 1e-12)); return lam, {str(k): float(v) for k, v in L.items()}

class Rule:
    """Frozen rule: m(F) = GP posterior mean at standardised features; g = law(g_b, a0_foot) 10^m."""
    def __init__(s, arm, mu, sd, Z, alpha, ell, sf2, meta=None): s.arm, s.mu, s.sd, s.Z, s.alpha, s.ell, s.sf2, s.meta = arm, mu, sd, Z, alpha, ell, sf2, meta or {}
    def std(s, F): return (F - s.mu) / s.sd
    def m(s, F):
        F = np.asarray(F, float); ok = np.all(np.isfinite(F), 1); out = np.full(len(F), np.nan)
        if ok.any(): out[ok] = predict(s.std(F[ok]), s.Z, s.alpha, s.ell, s.sf2)
        return out
    def save(s, p): np.savez(p, arm=s.arm, mu=s.mu, sd=s.sd, Z=s.Z, alpha=s.alpha, ell=s.ell, sf2=s.sf2)
def train_set(arm, a0, gobs_X=None, gobs_S=None, tgt=None):
    F = np.vstack([feats(XT, arm), feats(ST, arm)]); t = np.r_[target(XT, a0, gobs_X), target(ST, a0, gobs_S)] if tgt is None else tgt
    cls = np.r_[np.zeros(len(XT), int), np.ones(len(ST), int)]; sysid = np.r_[XT[:, 4].astype(int), ST[:, 4].astype(int)]; return F, t, cls, sysid
def fit_rule(arm, F, t, cls, sysid):
    mu, sd = F.mean(0), F.std(0); Z = (F - mu) / sd; hp = ml_fit(Z, t, cls); lam, L = cv_lambda(Z, t, cls, sysid, hp); ell = lam * hp["ell"]
    a = posterior(Z, t, cls, ell, hp["sf2"], noise_vec(cls, hp["sX"], hp["sS"]))
    return Rule(arm, mu, sd, Z, a, ell, hp["sf2"], dict(ml=dict(ell=hp["ell"].tolist(), sf=math.sqrt(hp["sf2"]), sX=hp["sX"], sS=hp["sS"], nll=hp["nll"], conv=hp["conv"]), lam=lam, cv=L, n=len(t)))
def refit_fixed(base, F, t, cls, extra_sd, lam_mult=1.0):
    """Oracle: same standardisation, lengths, amplitude, class noises; extra rows (cls 2) with their own sd."""
    Z = base.std(F); ml = base.meta["ml"]; nv = noise_vec(cls, ml["sX"], ml["sS"], extra_sd); ell = base.ell * lam_mult
    a = posterior(Z, t, cls, ell, base.sf2, nv); return Rule(base.arm, base.mu, base.sd, Z, a, ell, base.sf2, dict(base.meta, oracle=True, lam_mult=lam_mult, n=len(t)))

# ---------- gates 1-4 on BF1/SY1's rows
def gates14(rule, a0, plant=None):
    """plant: dict of planted g_obs arrays for XT, ST, XH, SH, LT (else real). SPARC lines are 1.05 x the REAL law's rms on the same rows."""
    P = plant or {}; o = {}
    def d(A, k): return target(A, a0, P.get(k)) - rule.m(feats(A, rule.arm))
    dx, ds, dxh, dsh, dl = d(XT, "XT"), d(ST, "ST"), d(XH, "XH"), d(SH, "SH"), d(LTA, "LT")
    lS, lH = SF * rms(target(ST, a0)), SF * rms(target(SH, a0))
    o["g1"] = dict(mean=float(dx.mean()), rms=rms(dx), ok=bool(np.all(np.isfinite(dx)) and abs(dx.mean()) <= XM and rms(dx) <= XR))
    o["g2"] = dict(rms=rms(ds), med=float(np.median(ds)), line=lS, ok=bool(np.all(np.isfinite(ds)) and rms(ds) <= lS and abs(np.median(ds)) <= SM))
    o["g3S"] = dict(rms=rms(dsh), med=float(np.median(dsh)), line=lH, ok=bool(np.all(np.isfinite(dsh)) and rms(dsh) <= lH and abs(np.median(dsh)) <= SM))
    o["g3X"] = dict(mean=float(dxh.mean()), rms=rms(dxh), ok=bool(np.all(np.isfinite(dxh)) and abs(dxh.mean()) <= XM and rms(dxh) <= XR))
    o["g3"] = dict(ok=o["g3S"]["ok"] and o["g3X"]["ok"])
    o["g4"] = dict(med=float(np.median(dl)), ok=bool(np.all(np.isfinite(dl)) and abs(np.median(dl)) <= LTT))
    o["_res"] = dict(XH=dxh, SH=dsh, LT=dl, XT=dx, ST=ds); return o

# ---------- hull and reach
def hull_mask(Ztr, Zq):
    from scipy.spatial import ConvexHull
    try: V = Ztr[ConvexHull(Ztr).vertices]
    except Exception: V = Ztr
    A = np.vstack([V.T, np.ones(len(V))]); out = np.zeros(len(Zq), bool)
    for i, z in enumerate(Zq):
        if not np.all(np.isfinite(z)): continue
        r = linprog(np.zeros(len(V)), A_eq=A, b_eq=np.r_[z, 1.0], bounds=(0, None), method="highs"); out[i] = r.status == 0
    return out
def reach(rule, Zq, chunk=2000):
    out = np.empty(len(Zq))
    for i in range(0, len(Zq), chunk): out[i:i + chunk] = np.sqrt(_sq(Zq[i:i + chunk] / rule.ell, rule.Z / rule.ell).min(1))
    return out

# ---------- CX1's centre rows for lines BF1/SY1 don't load
CX_LINES = ("G", "L", "Dw", "Dw-UFD", "IC1613")
def cx_rows(foot):
    """Centre leaves, centre log B at the footing, and CX1's MC sd of log B per row (CX1's systems() and mc(), U50, ASSUMED x1)."""
    sys.path.insert(0, CXD); import cx1_rows as C
    S = [s for s in C.systems(foot) if s.line in CX_LINES]; MU, COV, META, _ = C.mc(S, foot); a0 = FOOT[foot]; R = []
    sdmap = {(si, k): math.sqrt(COV[j][4, 4]) for j, (si, k) in enumerate(META)}
    for si, s in enumerate(S):
        r = np.asarray(s.rows["r"], float); gb = np.asarray(s.rows["gb"], float); gg = np.asarray(s.rows["gg"], float); go = np.asarray(s.rows["gobs"], float); sl = slope_1d(gb, r)
        for k in range(len(r)):
            if (si, k) not in sdmap: continue
            y = gb[k] / A0C; ell = r[k] * A0C / CL ** 2; f = min(1.0, max(0.0, gg[k] / gb[k]))
            R.append(dict(line=s.line, name=s.name, y=y, ell=ell, f=f, s=sl[k], D=float(D_leaf(np.array([y]), np.array([sl[k]]), np.array([ell]))[0]), logB=float(np.log10(go[k] / law(gb[k], a0))), sd=sdmap[(si, k)]))
    return R
def cx_feats(R, arm): return feats_from({k: np.array([q[k] for q in R]) for k in ("y", "ell", "f", "s", "D")}, arm)
