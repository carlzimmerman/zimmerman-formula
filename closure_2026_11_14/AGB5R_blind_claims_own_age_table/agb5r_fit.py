"""AGB5R estimators: plain weighted line and the structural (errors-in-both-variables) fit. Own code."""
import numpy as np
from scipy.optimize import minimize

S25 = -0.030  # mag/Gyr; A = beta / S25
SCAT = 0.10   # added in quadrature to sigma_HR in the plain weights


def design(t, step, zterm=False):
    cols = [np.ones_like(t["age"]), t["age"]]
    names = ["alpha", "beta"]
    if step:
        cols.append(t["L"] - 0.5)
        names.append("g")
    if zterm:
        cols.append(t["z"])
        names.append("cz")
    return np.column_stack(cols), names


def wls(X, y, w):
    XtW = X.T * w
    M = XtW @ X
    cov = np.linalg.inv(M)
    p = cov @ (XtW @ y)
    r = y - X @ p
    chi2 = float(np.sum(w * r * r))
    return p, cov, chi2


def plain(t, step, zterm=False, hr="hr", y=None):
    X, names = design(t, step, zterm)
    yy = t[hr] if y is None else y
    w = 1.0 / (t["shr"] ** 2 + SCAT ** 2)
    p, cov, chi2 = wls(X, yy, w)
    dof = len(yy) - X.shape[1]
    out = {n: float(p[i]) for i, n in enumerate(names)}
    out.update({"s_" + n: float(np.sqrt(cov[i, i])) for i, n in enumerate(names)})
    out["A"] = out["beta"] / S25
    out["sA"] = out["s_beta"] / abs(S25)
    out["chi2"] = chi2
    out["dof"] = dof
    out["sA_scaled"] = out["sA"] * np.sqrt(max(chi2 / dof, 1e-300))
    out["n"] = int(len(yy))
    return out


# ---------------- structural fit ----------------

def _nll(p, x, sx, y, sy, L, step):
    if step:
        alpha, beta, g, mu0, mu1, tau, sint = p
        mu = np.where(L > 0.5, mu1, mu0)
        off = g * (L - 0.5)
    else:
        alpha, beta, mu0, tau, sint = p
        mu = mu0
        off = 0.0
    t2 = tau * tau
    a = t2 + sx * sx
    c = beta * t2
    d = beta * beta * t2 + sint * sint + sy * sy
    det = a * d - c * c
    if np.any(det <= 0):
        return 1e30
    r1 = x - mu
    r2 = y - (alpha + off + beta * mu)
    q = (d * r1 * r1 - 2 * c * r1 * r2 + a * r2 * r2) / det
    return 0.5 * float(np.sum(np.log(det) + q))


def _hessian(f, p, h):
    n = len(p)
    H = np.zeros((n, n))
    f0 = f(p)
    for j in range(n):
        ej = np.zeros(n); ej[j] = h[j]
        H[j, j] = (f(p + ej) - 2 * f0 + f(p - ej)) / h[j] ** 2
        for k in range(j + 1, n):
            ek = np.zeros(n); ek[k] = h[k]
            H[j, k] = H[k, j] = (f(p + ej + ek) - f(p + ej - ek) - f(p - ej + ek) + f(p - ej - ek)) / (4 * h[j] * h[k])
    return H


def structural(t, step, hr="hr", age_err_scale=1.0, y=None):
    x = t["age"]
    sx = t["sage"] * age_err_scale
    yy = t[hr] if y is None else y
    sy = t["shr"]
    L = t["L"] if step else np.zeros_like(x)
    f = lambda p: _nll(p, x, sx, yy, sy, L, step)
    # starts from the plain line
    pl = plain(t, step, hr=hr, y=yy)
    vx = max(np.var(x) - np.mean(sx ** 2), 0.25)
    starts = []
    for tau0 in (np.sqrt(vx), 1.0, np.std(x)):
        for sint0 in (0.05, 0.12, 0.25):
            for bfac in (1.0, 1.6, 2.5):
                if step:
                    m0 = np.mean(x[L < 0.5]); m1 = np.mean(x[L > 0.5])
                    starts.append([pl["alpha"], pl["beta"] * bfac, pl["g"], m0, m1, tau0, sint0])
                else:
                    starts.append([pl["alpha"], pl["beta"] * bfac, np.mean(x), tau0, sint0])
    best = None
    for s in starts:
        r = minimize(f, np.array(s, float), method="BFGS", options={"gtol": 1e-9, "maxiter": 5000})
        r = minimize(f, r.x, method="Nelder-Mead", options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 40000, "maxfev": 80000})
        r = minimize(f, r.x, method="BFGS", options={"gtol": 1e-10, "maxiter": 5000})
        if best is None or r.fun < best.fun:
            best = r
    p = best.x.copy()
    p[-1] = abs(p[-1]); p[-2] = abs(p[-2])
    scale = np.array([0.1, 0.01] + ([0.05] if step else []) + ([1.0, 1.0] if step else [1.0]) + [0.5, 0.05])
    hs = []
    for hf in (1e-3, 3e-3):
        H = _hessian(f, p, scale * hf)
        cov = np.linalg.inv(H)
        hs.append(np.sqrt(cov[1, 1]))
    names = (["alpha", "beta", "g", "mu0", "mu1", "tau", "sint"] if step else ["alpha", "beta", "mu0", "tau", "sint"])
    out = {n: float(p[i]) for i, n in enumerate(names)}
    out["s_beta"] = float(hs[0])
    out["s_beta_hcheck"] = float(hs[1])
    if step:
        out["s_g"] = float(np.sqrt(cov[2, 2]))
    out["A"] = out["beta"] / S25
    out["sA"] = out["s_beta"] / abs(S25)
    out["nll"] = float(best.fun)
    out["n"] = int(len(x))
    out["sint_at_zero"] = bool(out["sint"] < 1e-4)
    out["age_err_scale"] = age_err_scale
    return out


def combine(rows):
    w = np.array([1.0 / r["sA"] ** 2 for r in rows])
    A = np.array([r["A"] for r in rows])
    Ac = float(np.sum(w * A) / np.sum(w))
    sc = float(1.0 / np.sqrt(np.sum(w)))
    return {"A": Ac, "sA": sc, "beta": Ac * S25, "s_beta": sc * abs(S25)}


def w1_word(A, sA):
    d0 = (A - 0.0) ** 2 / sA ** 2
    d1 = (A - 1.0) ** 2 / sA ** 2
    if d1 >= 9 and d0 < 4:
        w = "AGE BIAS EXCLUDED AT 3 SIGMA"
    elif 4 <= d1 < 9 and d0 < 4:
        w = "AGE BIAS DISFAVOURED"
    elif d0 >= 9 and d1 < 4:
        w = "AGE BIAS REQUIRED AT 3 SIGMA"
    elif 4 <= d0 < 9 and d1 < 4:
        w = "AGE BIAS FAVOURED"
    elif d0 < 4 and d1 < 4:
        w = "UNDECIDED"
    else:
        w = "NEITHER"
    return w, float(d0), float(d1)
