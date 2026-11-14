"""LGS4 fitting helpers: best fit (Nelder-Mead then Powell from several starts), numerical Hessian, and a plain
random-walk Metropolis sampler with a fixed Gaussian proposal (Laplace covariance, scaled 2.38^2 / d), four chains,
Gelman-Rubin check."""
import numpy as np
from scipy.optimize import minimize

STEP = dict(h=2e-3, obc=2e-3, wb=5e-5, w0=0.02, wa=0.05, dm=0.004)


def best_fit(fun, starts):
    best = None
    for s in starts:
        r = minimize(fun, np.array(s, float), method="Nelder-Mead", options=dict(maxiter=6000, maxfev=6000, xatol=1e-6, fatol=1e-6))
        r = minimize(fun, r.x, method="Powell", options=dict(maxiter=6000, xtol=1e-7, ftol=1e-10))
        r = minimize(fun, r.x, method="Nelder-Mead", options=dict(maxiter=6000, maxfev=6000, xatol=1e-7, fatol=1e-8))
        if best is None or r.fun < best.fun:
            best = r
    return best


def hessian(fun, x, steps):
    n = len(x); H = np.zeros((n, n)); f0 = fun(x)
    for i in range(n):
        ei = np.zeros(n); ei[i] = steps[i]
        H[i, i] = (fun(x + ei) - 2 * f0 + fun(x - ei)) / steps[i] ** 2
        for j in range(i + 1, n):
            ej = np.zeros(n); ej[j] = steps[j]
            H[i, j] = H[j, i] = (fun(x + ei + ej) - fun(x + ei - ej) - fun(x - ei + ej) + fun(x - ei - ej)) / (4 * steps[i] * steps[j])
    return H


def laplace_cov(chi2fun, x, steps):
    """covariance = 2 * inverse Hessian of chi2."""
    return 2 * np.linalg.inv(hessian(chi2fun, x, steps))


def metropolis(chi2fun, inprior, x0, cov, nstep, nchain=4, seed=1, burn=5000):
    d = len(x0); L = np.linalg.cholesky(cov * 2.38 ** 2 / d)
    chains, acc = [], []
    for c in range(nchain):
        rng = np.random.default_rng(seed + 1000 * c)
        x = None
        for _ in range(1000):
            t = x0 + np.linalg.cholesky(cov) @ rng.standard_normal(d)
            if inprior(t):
                x = t; break
        fx = chi2fun(x); out = np.empty((nstep, d)); na = 0
        for i in range(nstep):
            y = x + L @ rng.standard_normal(d)
            if inprior(y):
                fy = chi2fun(y)
                if np.log(rng.random()) < -0.5 * (fy - fx):
                    x, fx = y, fy; na += 1
            out[i] = x
        chains.append(out[burn:]); acc.append(na / nstep)
    ch = np.array(chains)                                  # (nchain, n, d)
    n = ch.shape[1]; m = ch.mean(axis=1); W = ch.var(axis=1, ddof=1).mean(axis=0); B = n * m.var(axis=0, ddof=1)
    rhat = np.sqrt(((n - 1) / n * W + B / n) / W)
    return ch.reshape(-1, d), dict(acceptance=[float(a) for a in acc], rhat_minus_1=[float(r - 1) for r in rhat])
