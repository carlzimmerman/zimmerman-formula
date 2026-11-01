"""DR7: the phase-space cap on a responded cold mass (FROZEN_CRITERIA.md). G cancels, so it is dropped. kappa = 1/2 FITTED, unused; not theory closed."""
import numpy as np
def jeans_P(r, M, Mo):
    """P(r) = int_r^edge rho M_tot / s^2 ds, as a sum over shells, for cold M and other mass Mo; P[-1] = 0."""
    s = np.sqrt(r[1:] * r[:-1]); dM = np.maximum(np.diff(M), 0.0); T = M + Mo; Mt = 0.5 * (T[1:] + T[:-1])
    return np.r_[np.cumsum((Mt / (4 * np.pi * s ** 4) * dM)[::-1])[::-1], 0.0]
def start_Q(r, M0, F):
    """Q_i^(1) = rho^(5/2) / P^(3/2) on the start state, r_s index, Q0."""
    P = jeans_P(r, M0, F * M0); rho = np.gradient(M0, np.log(r)) / (4 * np.pi * r ** 3); ok = (P > 0) & (rho > 0); Q = np.full(len(r), np.nan); Q[ok] = rho[ok] ** 2.5 / P[ok] ** 1.5; Q[0] = np.nan
    i_s = int(np.nanargmin(Q)); return Q, i_s, float(np.nanmax(Q[1:i_s + 1]))
def cap(r, Mb, M0, Mc, F, rho_mul=1.0, nit=200, tol=1e-4):
    """Returns M, info. M <= Mc, monotonic, rho <= rho_lim = Q0^(2/5) P_f^(3/5) on r <= r_s."""
    _, i_s, Q0 = start_Q(r, M0, F); K = Q0 ** 0.4 * rho_mul; dV = 4 * np.pi / 3 * np.diff(r ** 3); M = Mc.copy(); big = 10 * float(Mc[-1]) + 1.0; cv = 0.0
    for it in range(nit):
        lim = K * jeans_P(r, M, Mb) ** 0.6; d = np.sqrt(lim[1:] * lim[:-1]) * dV; d[i_s:] = big
        C = np.r_[lim[0] * 4 * np.pi / 3 * r[0] ** 3, 0.0 * d]; C[1:] = C[0] + np.cumsum(d); Mn = C + np.minimum.accumulate(Mc - C); Mn = np.minimum(Mn, Mc)
        pos = M > 0; cv = float(np.max(np.abs(Mn[pos] / M[pos] - 1))) if pos.any() else 0.0
        if cv <= tol or it == nit - 1: M = Mn; break
        M = 0.5 * (M + Mn)
    return M, dict(i_s=i_s, Q0=Q0, conv=cv, bound=bool(np.any(M < Mc * (1 - 1e-6))))
