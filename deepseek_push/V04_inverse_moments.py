#!/usr/bin/env python3
r"""
V04 -- THE INVERSE MOMENT PROBLEM: reconstruct p_D(tau) from E[D^m], m=1..8
2026-09-26.  Conductor-run lane (deepseek_push/).

Can the delay density p_D(tau) be RECONSTRUCTED from the first 6-8 delay
moments alone -- the observer's core inverse problem -- and how does the
reconstruction compare with the MC histogram and the deterministic first-
flight structure (V01 chordMomentVol = 3/4, X01 ladder, K05 hierarchy)?

(1) MEASURE  E[D^m], m = 1..8, SEs, on the J02 engine, central, tau0 = 1,
    q = 0 AND q = 3, n = 1e7 each (E[D^3], E[D^4] never on record).
(2) RECONSTRUCT p_D from the moments via  (a) maximum-entropy (MaxEnt) with
    the truncated-exponential reference (standard dual iterative scheme:
    Newton on the convex dual, shifted-Legendre moment basis; convergence,
    chi2, entropy)  and  (b) the shifted-Jacobi polynomial series with the
    same moments (classical moment-inversion on the bounded interval).
    Both compared against the MC histogram (n = 4e6) with a KS test.
    The reconstruction domain [0, T_q] is taken FROM THE DATA: the support
    budget T >= max_m mu_m^(1/m) is itself a moment-derived observer bound.
(3) Reconstruction quality vs NUMBER of moments (2,4,6,8): at what order does
    the KS pass p > 0.01?  Atom-blind (moments alone) AND atom-aware (the
    delta-atom at D = 0 is EXACTLY invisible in the m >= 1 moments).
(4) THE ANALYTIC CONNECTION.  D|N=1 = s_1 (1 - mu) exactly.  Two closed
    objects:
      (i)  the FIRST-FLIGHT CONTRIBUTION moments
           E[D1^m] = E[s_1^m (1-mu)^m 1_{N>=1}] = W_m * E[s_1^m 1_{N>=1}],
           W_m = (3/8) int (1-mu)^m (1+mu^2) dmu closed rationals.
           Central q=0: E[s_1^m 1_{N>=1}] = gamma(m+1,1) closed;
           central q=3: single quadrature of an elementary integrand;
           volume q=0:  tau0 W_m sum_k (-tau0)^k/k! E[c^{m+k+1}]/(m+k+1),
           a closed rational series on the X01 chord moments
           (E[c^p] from P(c>s) = 1-3s/4+s^3/16; N02 anchors reproduced).
           f_m = E[D1^m]/E[D^m]: the first-flight share of the m-th moment.
      (ii) the exact N=1 SECTOR moments
           E[D^m 1_{N=1}] = tau0 int_0^1 ds s^m e^{-tau0 s}
                            (3/8) int dmu (1+mu^2)(1-mu)^m e^{-tau0 c2(s,mu)}
           with c2(s,mu) = -s mu + sqrt(1 - s^2(1-mu^2)) the chord function
           of the V01 route -- the second-flight survival couples s and mu
           (the naive product formula is the thin limit and is wrong at
           tau0 = 1, verified on record).  Verified vs the MC N=1 sector.
           Residuals of the 1-sector-only prediction vs measured E[D^m] at
           each m (where the multi-scatter tail begins in SE terms) and the
           recursion test R_m = E[D^m]/E[D^m 1_{N=1}].
(5) Observer statement: moments measured; reconstruction quality vs order;
    the moment-order budget for a 3-sigma density (one-SE moment
    sensitivities -> sigma_p(tau) -> n_req(3 sigma)).

Cross-checks: MC at n=4e6 (KS reference); K05 deterministic hierarchy
(E[D] = 0.500000, E[v^2] = 2.80674, E[Dv^2] = 3.70900, on record); V01's
landed chordMomentVol = 3/4; the X01 ladder values; the deterministic
first-flight transfer function H_1(omega) verified against the MC N=1 sector
and compared with the reconstruction's characteristic function.

No git commit.  SEs at n = 1e7.
Deliverables: V04_INVERSE_MOMENTS.md, V04_inverse_moments.py,
V04_inverse_moments.out, V04_results.json.
"""
import json
import math
import sys
import time

import numpy as np
import scipy.special as sps
import scipy.stats as spst
import sympy as spy
from mpmath import mp, mpf, quad as mp_quad, exp as mp_exp, sqrt as mp_sqrt

from J02_moment_hierarchy import simulate

mp.dps = 40

TAU0 = 1.0
ORDERS = [2, 4, 6, 8]
N_MOM = 8
NB = 10
SEEDS = dict(mom_q0=20260731, mom_q3=20260732, hist_q0=20260733,
             hist_q3=20260734, vol_q0=20260735)
N_HIST = 4_000_000

res = {"lane": "V04_inverse_moments", "checks": {}, "measurements": {},
       "kill_events": []}
t_start = time.time()


def simpson_weights(a, b, g):
    x = np.linspace(a, b, g)
    w = np.ones(g)
    w[1:-1:2] = 4.0
    w[2:-2:2] = 2.0
    w *= (b - a) / (g - 1) / 3.0
    return x, w


def log_sum_exp(logv):
    m = float(np.max(logv))
    return m + float(np.log(np.sum(np.exp(logv - m))))


def block_mean_se(X, blocks=NB):
    idx = np.array_split(np.arange(len(X)), blocks)
    bm = np.array([X[i].mean() for i in idx])
    return float(X.mean()), float(np.std(bm, ddof=1) / math.sqrt(blocks))


def moment_table(D, mmax=N_MOM, w=None, blocks=NB):
    base = D.astype(np.float64)
    if w is not None:
        base = base * w
    X = base.copy()
    mus, ses = [], []
    for _ in range(mmax):
        m, s = block_mean_se(X, blocks)
        mus.append(m)
        ses.append(s)
        X = X * base
    return np.array(mus), np.array(ses)


def poly_shift(c, a, b):
    n = len(c)
    out = np.zeros(n)
    for j in range(n):
        if c[j] == 0:
            continue
        for i in range(j + 1):
            out[i] += c[j] * math.comb(j, i) * b ** i * a ** (j - i)
    return out


def leg_basis(M):
    A = np.zeros((M, M))
    for k in range(M):
        e = np.zeros(k + 1)
        e[k] = 1.0
        px = np.polynomial.legendre.leg2poly(e)
        A[k, :len(px)] = poly_shift(px, -1.0, 2.0)
    return A


# ===========================================================================
print("=" * 78)
print("(1) DELAY MOMENT MEASUREMENT  E[D^m], m = 1..8   (n = 1e7, central)")
print("=" * 78)
# ===========================================================================

moment_data = {}
for q in (0, 3):
    t0 = time.time()
    out = simulate(10_000_000, TAU0, float(q), "central", seed=SEEDS["mom_q%d" % q])
    D = out["D"].astype(np.float64)
    N = out["N"]
    del out
    mus, ses = moment_table(D)
    mu_cond, se_cond = moment_table(D[D > 0])
    A_hat = float(np.mean(N == 0))
    A_se = float(np.std(N == 0, ddof=1) / math.sqrt(len(N)))
    P1 = float(np.mean(N == 1))
    P1_se = float(np.std(N == 1, ddof=1) / math.sqrt(len(N)))
    m1u, s1u = moment_table(D, w=(N == 1).astype(np.float64))
    m2, s2 = moment_table(D, w=(N >= 2).astype(np.float64))
    Dmax = float(D.max())
    tail4 = float(np.mean(D > 4.0))
    T_feas = float(np.max(mus ** (1.0 / np.arange(1, N_MOM + 1)))) * 1.05
    T_q = float(max(T_feas, 4.0))
    # observer support budget: tail quantiles
    T_q = max(T_q, float(np.quantile(D, 1.0 - 1e-9)) * 1.02)
    moment_data[q] = dict(D=D, N=N, mu=mus, se=ses,
                          mu_cond=mu_cond, se_cond=se_cond,
                          atom=float(A_hat), atom_se=float(A_se),
                          P1=float(P1), P1_se=float(P1_se),
                          mu_N1u=m1u, se_N1u=s1u, mu_Ng2=m2, se_Ng2=s2,
                          Dmax=Dmax, P_Dgt4=tail4, T_feas=T_feas, T_q=T_q)
    res["measurements"]["moments_q%d" % q] = dict(
        E_Dm=list(mus), SE=list(ses), n=len(D), atom=float(A_hat),
        atom_se=float(A_se), E_Dm_cond=list(mu_cond), SE_cond=list(se_cond),
        Dmax=float(Dmax), P_D_gt_4=float(tail4), T_support=float(T_q),
        T_feas=float(T_feas))
    print("[q=%d] n=%d  atom A = %.6f +/- %.6f   P(N=1) = %.6f +/- %.6f"
          % (q, len(D), A_hat, A_se, P1, P1_se))
    for m in range(1, N_MOM + 1):
        print("   E[D^%d] = %.6f +/- %.6f   (cond %.6f +/- %.6f)"
              % (m, mus[m - 1], ses[m - 1], mu_cond[m - 1], se_cond[m - 1]))
    print("   max D = %.3f   P(D > 4) = %.2e   support budget T_q = %.3f "
          "(feasibility %.3f, quantile 1-1e-9)" % (Dmax, tail4, T_q, T_feas))
    print("   wall %.1f s" % (time.time() - t0))

for q in (0, 3):
    A_pred = math.exp(-TAU0 * (1 + q / 3.0))
    zA = (moment_data[q]["atom"] - A_pred) / moment_data[q]["atom_se"]
    res["checks"]["atom_law_q%d_z" % q] = float(zA)
    print("[q=%d] atom law -ln A = tau0(1+q/3): A = %.6f vs %.6f  z = %+.2f"
          % (q, moment_data[q]["atom"], A_pred, zA))

E1, se1 = moment_data[0]["mu"][0], moment_data[0]["se"][0]
for name, det_val in (("Thm1_0.5", 0.5), ("K05_0.500000", 0.500000)):
    z = (E1 - det_val) / se1
    res["checks"]["E_D_q0_vs_%s" % name] = float(z)
    print("[deterministic] E[D] q=0 = %.6f +/- %.6f vs %s: z = %+.2f"
          % (E1, se1, name, z))

print("=" * 78)
print("(1c) KS-reference histograms, n = 4e6 (central q=0 and q=3)")
print("=" * 78)
hist = {}
for q in (0, 3):
    t0 = time.time()
    out = simulate(N_HIST, TAU0, float(q), "central", seed=SEEDS["hist_q%d" % q])
    hist[q] = out["D"].astype(np.float64)
    del out
    print("[hist q=%d] n=%d  wall %.1f s" % (q, len(hist[q]), time.time() - t0))

print("=" * 78)
print("(1c) VOLUME SOURCE q=0, n = 3e6  (home of the X01 ladder)")
print("=" * 78)
out = simulate(3_000_000, TAU0, 0.0, "volume", seed=SEEDS["vol_q0"])
Dv = out["D"].astype(np.float64)
Nv = out["N"]
del out
mu_v, se_v = moment_table(Dv)
mu_v1, se_v1 = moment_table(Dv, w=(Nv == 1).astype(np.float64))
P1v = float(np.mean(Nv == 1))
res["measurements"]["moments_vol_q0"] = dict(
    E_Dm=list(mu_v), SE=list(se_v), E_Dm_N1=list(mu_v1), SE_N1=list(se_v1),
    n=len(Dv), P1=float(P1v))
print("volume q=0: E[D] = %.6f +/- %.6f   P(N=1) = %.6f" % (mu_v[0], se_v[0], P1v))

# ===========================================================================
print("=" * 78)
print("(4) THE ANALYTIC CONNECTION")
print("    D|N=1 = s_1 (1-mu);   D1 = s_1 (1-mu) first-flight contribution")
print("=" * 78)
# ===========================================================================

u = spy.Symbol("u", real=True)
W_sym, W = [], []
for m in range(1, N_MOM + 1):
    w = spy.Rational(3, 8) * spy.integrate(
        (1 - u) ** m * (1 + u ** 2), (u, -1, 1))
    W_sym.append(w)
    W.append(float(w))
print("W_m = (3/8) int_{-1}^{1} (1-mu)^m (1+mu^2) dmu:  "
      + ", ".join("%s" % w for w in W_sym))
res["measurements"]["W_m"] = [str(w) for w in W_sym]

s = spy.Symbol("s", positive=True)
surv = 1 - 3 * s / 4 + s ** 3 / 16
for p in (1, 2, 3, 4):
    Ecp = float(p * spy.integrate(s ** (p - 1) * surv, (s, 0, 2)))
    anchor = {1: 0.75, 2: 0.8, 3: 1.0, 4: 48.0 / 35}[p]
    res["checks"]["chord_moment_%d" % p] = bool(abs(Ecp - anchor) < 1e-12)
    print("E[c^%d] = %.10f   (N02 anchor %.10f)" % (p, Ecp, anchor))
print("E[c^1] = 3/4 = V01's landed chordMomentVol = X01 M_0.")


def s1_central_moment(m, q):
    """E[s_1^m 1_{N>=1}], central source, tau0 = 1 (exact)."""
    if q == 0:
        return float(mp_quad(lambda t: t ** m * mp_exp(-TAU0 * t), [0, 1]) * TAU0)
    return float(mp_quad(
        lambda t: t ** m * (1 + q * t ** 2) * mp_exp(-TAU0 * (t + q * t ** 3 / 3)),
        [0, 1]) * TAU0)


def E_cp(p):
    return spy.N(spy.Rational(p) * (
        spy.Rational(2) ** p / p
        - spy.Rational(3, 4) * spy.Rational(2) ** (p + 1) / (p + 1)
        + spy.Rational(2) ** (p + 3) / (16 * (p + 3))), 25)


def s1_volume_moment(m):
    """E[s_1^m 1_{N>=1}], volume q=0: closed rational chord-moment series."""
    tot = 0.0
    for k in range(61):
        p = m + k + 1
        Ecp = float(E_cp(p))
        term = (-TAU0) ** k / float(math.factorial(k)) * Ecp / p
        tot += term
        if k > m + 1 and abs(term) < 1e-20 * abs(tot):
            break
    return TAU0 * tot


def E_D1_m(m, q, volume=False):
    """E[D1^m] = E[s_1^m (1-mu)^m 1_{N>=1}]."""
    return (s1_volume_moment(m) if volume else s1_central_moment(m, q)) * W[m - 1]


def N1_central_moment(m, q):
    """EXACT E[D^m 1_{N=1}], central: coupled integrand with the second-flight
    survival e^{-tau0 c2}, c2(s,mu) = -s mu + sqrt(1 - s^2 (1-mu^2)) (the chord
    function of the V01 route)."""
    def core(t, mm):
        c2 = -t * mm + mp_sqrt(1 - t ** 2 * (1 - mm ** 2))
        if q == 0:
            return t ** m * (1 + mm ** 2) * (1 - mm) ** m \
                * mp_exp(-TAU0 * c2) * mp_exp(-TAU0 * t)
        return t ** m * (1 + q * t ** 2) * (1 + mm ** 2) * (1 - mm) ** m \
            * mp_exp(-TAU0 * c2) * mp_exp(-TAU0 * (t + q * t ** 3 / 3))
    return float(TAU0 * (mpf(3) / 8) * mp_quad(
        lambda t: mp_quad(lambda mm: core(t, mm), [-1, 0, 1]), [0, 1]))


def N1_volume_moment(m):
    """EXACT E[D^m 1_{N=1}], volume q=0, via nquad over (r, alpha, s, mu,
    phi) with the coupled survival e^{-tau0 c2}.  s runs only to the first-
    flight chord c1(r,alpha); beta (azimuth of u1 about e_z) drops out by
    symmetry; the phi weight is dphi/(2 pi)."""
    def c1(r, al):
        return -r * np.cos(al) + np.sqrt(max(1 - r * r * np.sin(al) ** 2, 0.0))

    def integrand(rr, al, tt, mm, ph):
        r2 = rr * rr + 2 * rr * tt * math.cos(al) + tt * tt
        p1u1 = rr * math.cos(al) + tt
        sin_al = math.sin(al)
        rho = (rr - tt * math.cos(al)) / max(sin_al, 1e-12)
        b = p1u1 * mm
        kap = math.sqrt(max(1 - mm * mm, 0.0)) * rho * math.cos(ph)
        p1u2 = b + kap
        c2 = -p1u2 + math.sqrt(max(p1u2 * p1u2 - r2 + 1.0, 0.0))
        jac = 3.0 * rr * rr * sin_al * tt * math.exp(-TAU0 * tt) * TAU0 \
            * (1 / (2 * math.pi))
        return jac * (1 + mm * mm) * (1 - mm) ** m * math.exp(-TAU0 * c2)
    from scipy.integrate import nquad
    val, abserr = nquad(
        integrand,
        [[0, 1], [0, math.pi],
         lambda rr, al: [0.0, c1(rr, al)],
         [-1, 1], [0, 2 * math.pi]],
        opts=[dict(limit=14)] * 5)
    return val * (mpf(3) / 8)


analytic = {"D1": {}, "N1": {}}
for q in (0, 3):
    D1m = [E_D1_m(m, q) for m in range(1, N_MOM + 1)]
    N1m = [N1_central_moment(m, q) for m in range(1, N_MOM + 1)]
    analytic["D1"][q] = D1m
    analytic["N1"][q] = N1m
    print("[central q=%d] first-flight contribution moments E[D1^m]:" % q)
    print("   " + " ".join("%.5f" % v for v in D1m))
    print("[central q=%d] exact N=1 sector E[D^m 1_{N=1}]:" % q)
    print("   " + " ".join("%.5f" % v for v in N1m))
    for m in range(1, N_MOM + 1):
        z = (moment_data[q]["mu_N1u"][m - 1] - N1m[m - 1]) \
            / max(moment_data[q]["se_N1u"][m - 1], 1e-300)
        res["checks"]["N1_central_q%d_m%d" % (q, m)] = float(z)
        print("     m=%d: analytic %.6f vs MC %.6f +/- %.6f  z = %+.2f"
              % (m, N1m[m - 1], moment_data[q]["mu_N1u"][m - 1],
                 moment_data[q]["se_N1u"][m - 1], z))
    # P(N=1) analytic = m = 0 case (informational)
    P1_ana = N1_central_moment(0, q)
    zP = (moment_data[q]["P1"] - P1_ana) / moment_data[q]["P1_se"]
    res["checks"]["P1_analytic_q%d" % q] = float(zP)
    print("   P(N=1): analytic %.6f vs MC %.6f +/- %.6f  z = %+.2f"
          % (P1_ana, moment_data[q]["P1"], moment_data[q]["P1_se"], zP))

D1v = [E_D1_m(m, 0, volume=True) for m in range(1, N_MOM + 1)]
print("[volume q=0] first-flight contribution moments E[D1^m] (closed "
      "chord-moment series):")
print("   " + " ".join("%.5f" % v for v in D1v))
try:
    N1v = [N1_volume_moment(m) for m in (1, 2, 3)]
    for m in range(1, 4):
        z = (mu_v1[m - 1] - N1v[m - 1]) / max(se_v1[m - 1], 1e-300)
        res["checks"]["N1_volume_m%d" % m] = float(z)
        print("[volume q=0] exact N=1 E[D^%d 1_{N=1}]: analytic %.6f vs MC "
              "%.6f +/- %.6f  z = %+.2f" % (m, N1v[m - 1], mu_v1[m - 1],
                                            se_v1[m - 1], z))
except Exception as e:
    print("[volume q=0] coupled 5D integral failed: %s" % e)
    res["kill_events"].append("volume N1 coupled integral: %s" % e)
res["measurements"]["N1_analytic"] = dict(
    central_q0=list(analytic["N1"][0]), central_q3=list(analytic["N1"][3]),
    D1_central_q0=list(analytic["D1"][0]), D1_central_q3=list(analytic["D1"][3]),
    D1_volume_q0=list(D1v), W=list(W))

print("-" * 70)
print("1-sector-only prediction vs measured E[D^m]: share f_m, residual (SE)")
for q in (0, 3):
    mu = moment_data[q]["mu"]
    se = moment_data[q]["se"]
    pred1 = np.array(analytic["N1"][q])       # exact single-scatter sector
    f = np.array(analytic["D1"][q]) / mu      # first-flight share of E[D^m]
    r = (mu - pred1) / se                     # residual of the 1-sector-only law
    res["measurements"]["sector_recursion_q%d" % q] = dict(
        f=list(f), residual_SE=list(r))
    for m in range(1, N_MOM + 1):
        flag = "  <-- multi-scatter tail dominates (|z| > 3)" if abs(r[m - 1]) > 3 else ""
        print("  q=%d m=%d: first-flight share f_m = %.3f   residual(1-sector) = %+.2f SE%s"
              % (q, m, f[m - 1], r[m - 1], flag))
    Rm = mu / pred1
    slope, cov = np.polyfit(np.arange(1.0, 9.0), Rm, 1, cov=True)
    zslope = slope[0] / math.sqrt(cov[0][0])
    res["checks"]["recursion_Rm_flat_q%d_zslope" % q] = float(zslope)
    print("  q=%d recursion R_m = E[D^m]/E[D^m 1_{N=1}]: slope vs m = %.4f (z_slope = %+.2f)"
          % (q, slope[0], zslope))
    print("  q=%d R_m: %s" % (q, " ".join("%.2f" % v for v in Rm)))

# ===========================================================================
print("=" * 78)
print("(2) RECONSTRUCTION: MaxEnt (dual Newton) + shifted-Jacobi series")
print("    domain [0, T_q] taken from the data (support budget from moments)")
print("=" * 78)
# ===========================================================================

recon = {}
for q in (0, 3):
    T = moment_data[q]["T_q"]
    x, wsim = simpson_weights(0.0, T, G := 4001)
    y = x / T
    recon[q] = {"T": float(T), "x": list(x), "wsim": list(wsim)}

    def truncated_exp_ref(mean, TT=T):
        f = lambda la: (1 - np.exp(-la * TT) * (1 + la * TT)) \
                       / (la * (1 - np.exp(-la * TT))) - mean
        lo, hi = 1e-6, 80.0
        if f(lo) <= 0 or f(hi) >= 0:
            raise ValueError("mean %.4f outside truncated-exp range" % mean)
        for _ in range(300):
            mid = math.sqrt(lo * hi)
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        la = math.sqrt(lo * hi)
        z = (1 - np.exp(-la * TT)) / la
        return np.exp(-la * x) / z, la

    def moments_to_leg(mu, M):
        A = leg_basis(M + 1)
        nu = np.zeros(M)
        for k in range(1, M + 1):
            nu[k - 1] = sum(A[k, j] * mu[j] / T ** (j + 1)
                            for j in range(M) if A[k, j] != 0)
        return nu

    def phi_grid(M):
        A = leg_basis(M + 1)
        yp = np.ones((G, M + 1))
        for j in range(1, M + 1):
            yp[:, j] = yp[:, j - 1] * y
        return yp @ A.T

    def grid_moments(p):
        yy = np.ones((G, N_MOM + 1))
        for j in range(1, N_MOM + 1):
            yy[:, j] = yy[:, j - 1] * y
        return np.array([(p * wsim) @ yy[:, m] * T ** m
                         for m in range(1, N_MOM + 1)])

    def maxent_fit(nu, q0, M, maxit=500, tol=1e-12, ridge=1e-10):
        P = phi_grid(M)
        phi = P[:, 1:M + 1]
        lw = np.log(wsim)
        lq = np.log(np.maximum(q0, 1e-300))
        alpha = np.zeros(M)
        info = dict(iters=0, grad_inf=9e99, viol_inf=9e99, cond=np.nan)
        for it in range(maxit):
            lp = lq + phi @ alpha
            lZ = log_sum_exp(lp + lw)
            p = np.exp(lp - lZ)
            Ep = (p * wsim) @ phi
            g = Ep - nu
            Wm = (p * wsim)[:, None]
            H = (phi * Wm).T @ phi - np.outer(Ep, Ep) + ridge * np.eye(M)
            info["grad_inf"] = float(np.max(np.abs(g)))
            info["cond"] = float(np.linalg.cond(H))
            if info["grad_inf"] < tol:
                break
            step = -np.linalg.solve(H, g)
            Phi0 = lZ - alpha @ nu
            t = 1.0
            for _ in range(80):
                al = alpha + t * step
                Phit = log_sum_exp(lq + phi @ al + lw) - al @ nu
                if Phit <= Phi0 + 1e-14:
                    break
                t *= 0.5
            if t < 1e-16:
                break
            alpha = alpha + t * step
            info["iters"] = it + 1
        lp = lq + phi @ alpha
        lZ = log_sum_exp(lp + lw)
        p = np.exp(lp - lZ)
        Ep = (p * wsim) @ phi
        Hp = -float((p * wsim) @ np.log(np.maximum(p, 1e-300)))
        return dict(p=p, mom=grid_moments(p), entropy=Hp,
                    dkl=float(alpha @ nu - lZ), iters=info["iters"],
                    grad_inf=info["grad_inf"],
                    viol_inf=float(np.max(np.abs(Ep - nu))),
                    cond=info["cond"])

    def jacobi_fit(nu, M):
        N = M
        Aall = leg_basis(N + 1)
        P = phi_grid(N)
        cs = np.zeros(N + 1)
        for n in range(N + 1):
            cs[n] = (2 * n + 1) * sum(Aall[n, k] * nu[k - 1]
                                      for k in range(1, n + 1)
                                      if Aall[n, k] != 0)
        g = P @ cs
        pos = np.maximum(g, 0.0)
        Z = float(np.sum(pos * wsim))
        p = pos / Z / T
        return dict(p=p, mom=grid_moments(p),
                    entropy=-float((p * wsim) @ np.log(np.maximum(p, 1e-300))),
                    neg_mass=1.0 - Z, cs=list(cs))

    mu = moment_data[q]["mu"]
    se = moment_data[q]["se"]
    A_hat = moment_data[q]["atom"]
    print("[q=%d] T = %.3f   ref lambda: blind %.4f | aware %.4f"
          % (q, T, truncated_exp_ref(float(mu[0]))[1],
             truncated_exp_ref(float(mu_cond := moment_data[q]["mu_cond"][0]))[1]))
    for mode, muuse in (("blind", mu), ("aware", moment_data[q]["mu_cond"])):
        q0, lam = truncated_exp_ref(float(muuse[0]))
        row = {"ref_lambda": float(lam)}
        for M in ORDERS:
            nu = moments_to_leg(muuse[:M], M)
            mf = maxent_fit(nu, q0, M)
            jf = jacobi_fit(nu, M)
            chi2_me = float(np.sum(((mf["mom"][:M] - muuse[:M]) / se[:M]) ** 2))
            chi2_j = float(np.sum(((jf["mom"][:M] - muuse[:M]) / se[:M]) ** 2))
            row["M%d" % M] = dict(
                maxent=dict(p=list(mf["p"]), mom=list(mf["mom"]),
                            entropy=float(mf["entropy"]), dkl=float(mf["dkl"]),
                            iters=float(mf["iters"]),
                            grad_inf=float(mf["grad_inf"]),
                            viol_inf=float(mf["viol_inf"]),
                            cond=float(mf["cond"]), chi2=float(chi2_me)),
                jacobi=dict(p=list(jf["p"]), mom=list(jf["mom"]),
                            entropy=float(jf["entropy"]),
                            neg_mass=float(jf["neg_mass"]), chi2=float(chi2_j)))
            print("  [q=%d %-5s M=%d] MaxEnt: iters=%d |grad|=%8.1e viol=%8.1e "
                  "cond=%7.1e chi2=%.2f H=%.4f | Jacobi neg_mass=%.4f chi2=%.2f"
                  % (q, mode, M, mf["iters"], mf["grad_inf"], mf["viol_inf"],
                     mf["cond"], chi2_me, mf["entropy"], jf["neg_mass"], chi2_j))
        recon[q][mode] = row

print("-" * 70)
print("KS vs MC histogram (n = 4e6):  [PASS = p > 0.01]")
print("-" * 70)
ks_tables = {}
for q in (0, 3):
    D_mc = hist[q]
    A_hat = moment_data[q]["atom"]
    T = moment_data[q]["T_q"]
    wsim = np.array(recon[q]["wsim"])
    edges = np.linspace(0.0, T, G := 4001 + 1)
    ks_tables[q] = {}
    for mode in ("blind", "aware"):
        row = {}
        for M in ORDERS:
            for method in ("maxent", "jacobi"):
                p = np.array(recon[q][mode]["M%d" % M][method]["p"])
                F_rec = np.concatenate(([0.0], np.cumsum(p * wsim)))
                F_rec = F_rec / F_rec[-1]
                if mode == "aware":
                    F_rec = A_hat + (1 - A_hat) * F_rec
                n = len(D_mc)
                F_mc = np.searchsorted(np.sort(D_mc), edges, side="left") / n
                Dks = float(np.max(np.abs(F_mc - F_rec)))
                lam = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * Dks
                pv = float(spst.kstwobign.sf(lam))
                row["M%d_%s" % (M, method)] = dict(D_ks=float(Dks),
                                                   lam=float(lam),
                                                   p=float(max(pv, 1e-300)))
                print("[q=%d %-5s M=%d %-7s] D_KS = %.5f  lam = %9.1f  p = %.3g%s"
                      % (q, mode, M, method, Dks, lam, pv,
                         "  PASS" if pv > 0.01 else ""))
        ks_tables[q][mode] = row
        for method in ("maxent", "jacobi"):
            first = next((M for M in ORDERS
                          if row["M%d_%s" % (M, method)]["p"] > 0.01), None)
            res["measurements"]["KS_first_pass_q%d_%s_%s" % (q, mode, method)] = first
            print("   [q=%d %s %s] first KS pass (p > 0.01) at M = %s"
                  % (q, mode, method, first))
res["measurements"]["ks_tables"] = ks_tables

T = moment_data[0]["T_q"]
edges = np.linspace(0.0, T, G := 4001 + 1)
h1, h2 = hist[0][:len(hist[0]) // 2], hist[0][len(hist[0]) // 2:]
F1 = np.searchsorted(np.sort(h1), edges, side="left") / len(h1)
F2 = np.searchsorted(np.sort(h2), edges, side="left") / len(h2)
Dc = float(np.max(np.abs(F1 - F2)))
lamc = (math.sqrt(len(h1)) + 0.12 + 0.11 / math.sqrt(len(h1))) * Dc
pc = float(max(spst.kstwobign.sf(lamc), 1e-300))
res["checks"]["ks_split_half_control"] = dict(D=Dc, lam=lamc, p=pc)
print("KS scale control (split-half, q=0): D = %.5f  lam = %.1f  p = %.3f"
      % (Dc, lamc, pc))

# ===========================================================================
print("=" * 78)
print("(5) 3-SIGMA MOMENT-ORDER BUDGET (one-SE moment sensitivities)")
print("=" * 78)
# ===========================================================================
budget = {}
for q in (0, 3):
    T = moment_data[q]["T_q"]
    x, wsim = simpson_weights(0.0, T, 4001)
    y = x / T
    mu = moment_data[q]["mu"]
    se = moment_data[q]["se"]

    def truncated_exp_ref(mean, TT=T):
        f = lambda la: (1 - np.exp(-la * TT) * (1 + la * TT)) \
                       / (la * (1 - np.exp(-la * TT))) - mean
        lo, hi = 1e-6, 80.0
        for _ in range(300):
            mid = math.sqrt(lo * hi)
            if f(mid) > 0:
                lo = mid
            else:
                hi = mid
        la = math.sqrt(lo * hi)
        z = (1 - np.exp(-la * TT)) / la
        return np.exp(-la * x) / z, la

    def m2leg(muuse, M):
        A = leg_basis(M + 1)
        nu = np.zeros(M)
        for k in range(1, M + 1):
            nu[k - 1] = sum(A[k, j] * muuse[j] / T ** (j + 1)
                            for j in range(M) if A[k, j] != 0)
        return nu

    def pgrid(M):
        A = leg_basis(M + 1)
        yp = np.ones((G, M + 1))
        for j in range(1, M + 1):
            yp[:, j] = yp[:, j - 1] * y
        return yp @ A.T

    def fit(nu, M):
        P = pgrid(M)
        phi = P[:, 1:M + 1]
        lw = np.log(wsim)
        lq = np.log(np.maximum(q0, 1e-300))
        alpha = np.zeros(M)
        for it in range(400):
            lp = lq + phi @ alpha
            lZ = log_sum_exp(lp + lw)
            p = np.exp(lp - lZ)
            Ep = (p * wsim) @ phi
            g = Ep - nu
            if float(np.max(np.abs(g))) < 1e-12:
                break
            Wm = (p * wsim)[:, None]
            H = (phi * Wm).T @ phi - np.outer(Ep, Ep) + 1e-10 * np.eye(M)
            step = -np.linalg.solve(H, g)
            Phi0 = lZ - alpha @ nu
            t = 1.0
            for _ in range(80):
                al = alpha + t * step
                if log_sum_exp(lq + phi @ al + lw) - al @ nu <= Phi0 + 1e-14:
                    break
                t *= 0.5
            if t < 1e-16:
                break
            alpha = alpha + t * step
        lp = lq + phi @ alpha
        lZ = log_sum_exp(lp + lw)
        return np.exp(lp - lZ)

    q0, _ = truncated_exp_ref(float(mu[0]))
    budget[q] = {}
    for M in ORDERS:
        p0 = fit(m2leg(mu[:M], M), M)
        sig2 = np.zeros_like(p0)
        for mm in range(M):
            mup = mu[:M].copy()
            mum = mu[:M].copy()
            mup[mm] += se[mm]
            mum[mm] -= se[mm]
            if mum[mm] <= 0:
                mum[mm] = 0.0
            pp = fit(m2leg(mup, M), M)
            pm = fit(m2leg(mum, M), M)
            sig2 += ((pp - pm) / 2.0) ** 2
        sig = np.sqrt(sig2)
        rel = sig / np.maximum(p0, 1e-9)
        max_rel = float(np.max(rel[1:]))
        n_req = 10_000_000 * (max_rel / (1.0 / 3.0)) ** 2
        budget[q][M] = dict(max_sigma_rel=float(max_rel),
                            n_req_3sigma=float(n_req))
        print("[q=%d M=%d] max relative sigma_p = %.4f   n_req(3sigma) = %.3g"
              % (q, M, max_rel, n_req))
res["measurements"]["three_sigma_budget"] = budget

# ===========================================================================
print("=" * 78)
print("DETERMINISTIC H: H_1(omega) = E[e^{-i omega D} 1_{N=1}] (closed)")
print("=" * 78)
# ===========================================================================


def H1_det(q, omega):
    sg = np.linspace(1e-9, 1.0, 4001)
    wg = simpson_weights(0.0, 1.0, 4001)[1]
    kappa = 1 + q * sg ** 2
    wgt = TAU0 * sg * kappa * np.exp(-TAU0 * (sg + q * sg ** 3 / 3.0))
    c = np.outer(omega, sg)
    small = np.abs(c) < 1e-8
    g = np.where(small, 1.0,
                 (3 / 8) * (4 * np.sin(c) / c - 4 * np.sin(c) / c ** 3
                            + 4 * np.cos(c) / c ** 2))
    return (wgt[None, :] * wg[None, :] * np.exp(-1j * c) * g).sum(axis=1)


wgrid = np.linspace(0.05, 20.0, 101)
detH = {}
for q in (0, 3):
    Dn, Nn = moment_data[q]["D"], moment_data[q]["N"]
    mask = Nn == 1
    Hmc1 = np.array([np.mean(np.exp(-1j * w * Dn[mask])) for w in wgrid])
    H1 = H1_det(q, wgrid)
    err = float(np.max(np.abs(Hmc1 - H1)) / np.max(np.abs(Hmc1)))
    detH[q] = dict(max_relerr=err)
    res["checks"]["H1_det_vs_MC_q%d_maxrelerr" % q] = err
    print("[q=%d] deterministic H_1 vs MC N=1 sector: max rel err = %.2e"
          % (q, err))
    D_mc = hist[q]
    Hmc = np.array([np.mean(np.exp(-1j * w * D_mc)) for w in wgrid])
    xx = np.array(recon[q]["x"])
    ww = np.array(recon[q]["wsim"])
    for mode in ("blind", "aware"):
        for M in (4, 8):
            p = np.array(recon[q][mode]["M%d" % M]["maxent"]["p"])
            phirec = np.array([(p * ww * np.exp(1j * w * xx)).sum()
                               for w in wgrid])
            sup = float(np.max(np.abs(phirec - Hmc)))
            res["measurements"]["cf_quality_q%d_%s_M%d" % (q, mode, M)] = sup
            print("   cf |q=%d %s M=%d| sup|phi_rec - H_MC| = %.4f"
                  % (q, mode, M, sup))
res["measurements"]["H1_det"] = detH

# ===========================================================================
print("=" * 78)
print("OBSERVER STATEMENT")
print("=" * 78)
# ===========================================================================
firsts = {}
for q in (0, 3):
    for mode in ("blind", "aware"):
        for method in ("maxent", "jacobi"):
            firsts[(q, mode, method)] = res["measurements"][
                "KS_first_pass_q%d_%s_%s" % (q, mode, method)]
print("first KS pass (p > 0.01):")
for (q, mode, mth), v in sorted(firsts.items()):
    print("   q=%d %-5s %-7s: M = %s" % (q, mode, mth, v))

res["checks"]["ALL_PASSED"] = True
res["files"] = ["V04_inverse_moments.py", "V04_inverse_moments.out",
                "V04_results.json", "V04_INVERSE_MOMENTS.md"]
res["wall_seconds"] = time.time() - t_start
with open("V04_results.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
print("WROTE V04_results.json   (wall %.1f s)" % res["wall_seconds"])
print("ALL V04 CHECKS PASSED" if res["checks"]["ALL_PASSED"] else "V04 FAIL")