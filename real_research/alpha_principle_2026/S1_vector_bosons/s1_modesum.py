"""s1_modesum.py -- exact (ODE) covariance, adiabatic subtraction and k-r quadrature for the S1 mode sums.  See s1_lib.py for conventions.

Scaled problem (k = 1): the integrand of f = Int k^2 dk Int dr I(k, r) is  I(k, r) = Tr[Q~_J Gamma~](tau' = -k; k_z = r, k_perp = sqrt(1-r^2)),
where Gamma~ is the covariance of the k = 1 problem evolved from tau' = -T (second-order adiabatic vacuum) to tau' = -k.  (Derivation: W = k^{-1/2} w, Pi = k^{1/2} pi.)
"""
import math
import numpy as np
from scipy.integrate import solve_ivp
import s1_lib as L

_MODELS = {}
NORD = 4        # highest adiabatic order computed for the series (initial data use order 2 only)


def get_model(kind, c, scheme):
    key = (kind, c, scheme)
    if key not in _MODELS:
        _MODELS[key] = L.Model(kind, c=c, scheme=scheme)
    return _MODELS[key]


def exact_nodes(model, r, lam, mu, taus, T=3000.0, rtol=1e-13, atol=1e-16, init_order=4):
    """Gamma_d (= balanced-frame covariance) at tau' in `taus` (ascending, all in (-T, 0))."""
    kz, kp = r, math.sqrt(max(0.0, 1 - r * r))
    n = model.n
    ser0, Gam0, U0, res0 = L.current_series(model, -T, kz, kp, lam, mu, order=init_order)
    G_init = sum(Gam0[n][0] for n in range(init_order + 1))

    def rhs(t, y):
        G = y.reshape(n, n)
        A = model.A_dressed(t, kz, kp, lam, mu)
        return (A @ G + G @ A.T).ravel()

    sol = solve_ivp(rhs, (-T, taus[-1]), G_init.ravel(), method="DOP853", t_eval=taus, rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(sol.message)
    return [sol.y[:, i].reshape(n, n) for i in range(len(taus))], G_init


def integrand_nodes(model, r, lam, mu, ks, T=3000.0, nord=None):
    """For k in ks (ascending): exact integrand I_ex, adiabatic series (orders 0..2) -> remainder.  Returns arrays."""
    ks = np.asarray(ks)
    taus = np.sort(-ks)                      # ascending tau' (most negative first = largest k)
    Gs, _ = exact_nodes(model, r, lam, mu, taus, T=T)
    kz, kp = r, math.sqrt(max(0.0, 1 - r * r))
    ex, ad = [], []
    for tau_, G in zip(taus, Gs):
        ser, Gam, U, res = L.current_series(model, tau_, kz, kp, lam, mu, order=(NORD if nord is None else nord))
        ex.append(L.current_exact(model, tau_, kz, kp, lam, mu, G, U))
        ad.append(ser)
    ex = np.array(ex)[::-1]                  # back to ascending k
    ad = np.array(ad)[::-1]
    return ex, ad


# ------------------------------------------------------------------ quadrature
from concurrent.futures import ProcessPoolExecutor


def k_grid(K=200.0, kmin=1e-12, nseg=60, ngl=12):
    xg, wg = np.polynomial.legendre.leggauss(ngl)
    edges = np.exp(np.linspace(math.log(kmin), math.log(K), nseg + 1))
    ks, ws = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        ks.extend(list(0.5 * (b - a) * xg + 0.5 * (b + a)))
        ws.extend(list(0.5 * (b - a) * wg))
    return np.array(ks), np.array(ws)


def _rnode(args):
    kind, c, scheme, r, lam, mu, ks, T, nord = args
    m = get_model(kind, c, scheme)
    ex, ad = integrand_nodes(m, r, lam, mu, ks, T=T, nord=nord)
    return ex, ad


def f_point(kind, c, scheme, lam, mu, K=40.0, kmin=1e-12, nseg=60, ngl=12, nr=24, T=3000.0, workers=12, return_parts=False, order_used=2, tail_powers=(3, 4, 5), fit_from=0.25):
    """f = Int k^2 dk Int dr [I_exact - adiabatic series through `order_used`]  (+ fitted tail beyond K).  The pipeline convention: f_pipeline = - f_KA.
    Tail: g(k) = k^2 Int dr R(k, r) is fitted on the Gauss nodes with fit_from*K <= k <= K to sum_j c_j / k^j, j in tail_powers, and integrated from K to infinity.
    (K = 40: double-precision noise of exact - adiabatic is ~1e-10 absolute in the integrand, so larger K only adds noise; the FIRST development runs with K = 200 and the
    three-node tail of the scalar-QED reference script showed exactly this.)"""
    ks, ws = k_grid(K, kmin, nseg, ngl)
    xr, wr = np.polynomial.legendre.leggauss(nr)
    jobs = [(kind, c, scheme, r, lam, mu, ks, T, max(2, order_used)) for r in xr]
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as ex_:
            outs = list(ex_.map(_rnode, jobs))
    else:
        outs = [_rnode(j) for j in jobs]
    EX = np.array([o[0] for o in outs])      # (nr, nk)
    AD = np.array([o[1] for o in outs])      # (nr, nk, 3)
    ad_sum = AD[:, :, :order_used + 1].sum(axis=2)
    R = EX - ad_sum
    g = (wr[:, None] * R).sum(axis=0) * ks**2          # k^2 * Int dr remainder
    total = float(np.sum(ws * g))
    sel = ks >= fit_from * K
    kk, gg = ks[sel], g[sel]
    Amat = np.array([[k ** (-j) for j in tail_powers] for k in kk])
    coef, *_ = np.linalg.lstsq(Amat, gg, rcond=None)
    tail = float(sum(cj * K ** (1 - j) / (j - 1) for cj, j in zip(coef, tail_powers)))
    fit_res = float(np.max(np.abs(Amat @ coef - gg)) / max(1e-300, np.max(np.abs(gg))))
    f = total + tail
    if return_parts:
        return f, dict(total=total, tail=tail, coef=coef, fit_res=fit_res, ks=ks, EX=EX, AD=AD, R=R, wr=wr, g=g)
    return f


def _gjob(args):
    kind, c, scheme, r, lam, mu, ks, T = args
    m = get_model(kind, c, scheme)
    taus = np.sort(-ks)
    Gs, _ = exact_nodes(m, r, lam, mu, taus, T=T, init_order=4)
    import math as _m
    kz, kp = r, _m.sqrt(max(0.0, 1 - r * r))
    ex = []
    for tau_, G in zip(taus, Gs):
        U, _ = m.U(tau_, kz, kp, lam, mu)
        ex.append(L.current_exact(m, tau_, kz, kp, lam, mu, G, U))
    return np.array(ex)[::-1]


def raw_g(kind, c, scheme, lam, mu, ks, T=6000.0, nr=28, workers=12):
    """g(k) = k^2 Int_{-1}^{1} dr I_exact(k, r) for the EXACT vacuum (no subtraction), ks ascending."""
    ks = np.asarray(ks, dtype=float)
    xr, wr = np.polynomial.legendre.leggauss(nr)
    jobs = [(kind, c, scheme, r, lam, mu, ks, T) for r in xr]
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as ex_:
            outs = list(ex_.map(_gjob, jobs))
    else:
        outs = [_gjob(j) for j in jobs]
    return (wr[:, None] * np.array(outs)).sum(axis=0) * ks**2


def uv_fit(g, ks, powers=(1, -1, -3)):
    A = np.array([[k**p for p in powers] for k in ks])
    coef, *_ = np.linalg.lstsq(A, g, rcond=None)
    res = np.max(np.abs(A @ coef - g)) / np.max(np.abs(g))
    return coef, res
