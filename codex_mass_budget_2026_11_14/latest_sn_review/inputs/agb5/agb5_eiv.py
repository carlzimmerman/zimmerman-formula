"""AGB5 errors-in-both-variables regression (criteria: FROZEN_CRITERIA.md).

Structural model, maximum likelihood. For host i in group k (k = mass group, or one group):
    true age x_i ~ N(mu_k, tau^2);   observed age = x_i + N(0, sx_i^2);
    y_i = alpha + g (L_i - 1/2) + beta x_i + N(0, sint^2 + sy_i^2).
The observed pair is bivariate normal, so the likelihood is closed form. This is the one-Gaussian case of the
LINMIX model of Kelly (2007), which the published slopes were fitted with."""
import numpy as np
from scipy.optimize import minimize


def nll(p, x, sx, y, sy, L, step):
    ng = 2 if step else 1
    alpha, beta, ls, lt = p[0], p[1], p[2], p[3]; mu = p[4:4 + ng]; g = p[4 + ng] if step else 0.0
    s2, t2 = np.exp(2*ls), np.exp(2*lt); grp = L.astype(int) if step else np.zeros(len(x), int)
    mx = mu[grp]; my = alpha + g*(L - 0.5) + beta*mx
    vxx = t2 + sx**2; vxy = beta*t2; vyy = beta**2*t2 + s2 + sy**2; det = vxx*vyy - vxy**2
    dx, dy = x - mx, y - my
    return 0.5*np.sum(np.log(det) + (vyy*dx**2 - 2*vxy*dx*dy + vxx*dy**2)/det)


def fit(x, sx, y, sy, L=None, step=False, sx_scale=1.0):
    """Returns dict(beta, sd_beta, g, sd_g, sint, tau). sx_scale multiplies the stated age errors."""
    L = np.zeros(len(x)) if L is None else L.astype(float); sx = sx*sx_scale
    b0 = np.polyfit(x, y, 1)[0]; ng = 2 if step else 1
    p0 = [np.mean(y) - b0*np.mean(x), b0, np.log(0.1), np.log(max(np.std(x), 0.3))] + [np.mean(x)]*ng + ([0.0] if step else [])
    best = None
    for scale in (1.0, 2.0, 0.5):
        q = np.array(p0); q[1] *= scale
        r = minimize(nll, q, args=(x, sx, y, sy, L, step), method="Nelder-Mead", options=dict(maxiter=40000, maxfev=40000, xatol=1e-9, fatol=1e-11))
        r = minimize(nll, r.x, args=(x, sx, y, sy, L, step), method="BFGS")
        if best is None or r.fun < best.fun: best = r
    p = best.x; n = len(p); H = np.zeros((n, n)); h = 1e-4*np.maximum(np.abs(p), 0.1)
    f = lambda q: nll(q, x, sx, y, sy, L, step)
    for i in range(n):
        for j in range(i, n):
            ei = np.zeros(n); ej = np.zeros(n); ei[i] = h[i]; ej[j] = h[j]
            H[i, j] = H[j, i] = (f(p + ei + ej) - f(p + ei - ej) - f(p - ei + ej) + f(p - ei - ej))/(4*h[i]*h[j])
    try:
        cov = np.linalg.inv(H)
    except np.linalg.LinAlgError:          # a resample can sit on a flat direction (age spread going to zero)
        cov = np.linalg.pinv(H)
    out = dict(beta=float(p[1]), sd_beta=float(np.sqrt(abs(cov[1, 1]))), sint=float(np.exp(p[2])), tau=float(np.exp(p[3])), nll=float(best.fun), n=len(x))
    if step: out.update(g=float(p[-1]), sd_g=float(np.sqrt(abs(cov[-1, -1]))))
    return out
