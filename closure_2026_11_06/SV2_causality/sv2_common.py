"""SV2 shared machinery: AC18's leaf kernel H and the monomial coefficients of g_hat, rebuilt verbatim from
action_search_2026_11_05/AC18_constraint_causality/ac18.py (criteria 5ba6bdfd7c), without AC18's side effects.

Kappa = 1/2 FITTED; not theory closed. Single thread.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50
X, Y, Z = sp.symbols("x y z", real=True)
xs = sp.symbols("x_bg", positive=True)
a_ = 1 / (1 + xs)
b_ = xs / (1 + xs)
S_ = sp.sqrt(X ** 2 + Y ** 2 + Z ** 2 / (1 - b_))
Gb = 1 / (4 * sp.pi * sp.sqrt(1 - b_) * S_)
H = -xs * sp.diff(Gb, Z, 2)                      # off-origin kernel of k^2/(k.Mt^-1.k) (AC18 A2)
Hnum = sp.lambdify((X, Y, Z, xs), H, "mpmath")

kx, ky, kz = sp.symbols("k_x k_y k_z", real=True)
k2 = kx ** 2 + ky ** 2 + kz ** 2
c_, G_, m_, vs, Pi_, tp, tt = sp.symbols("c G m v_s Pi tp tt", positive=True)
es = sp.Matrix(sp.symbols("e1 e2 e3", real=True))
kappa = (sp.Matrix([kx, ky, kz]).T * es)[0]
ORDER = 4
sinc_ser = sum((-1) ** n * (c_ ** 2 * k2) ** n * (tt - tp) ** (2 * n + 1) / sp.factorial(2 * n + 1) for n in range(2))
exp_ser = sum((-sp.I * kappa * vs * tp) ** n / sp.factorial(n) for n in range(1, ORDER))
phihat = sp.expand(sp.integrate(sp.expand(-4 * sp.pi * G_ * c_ ** 2 * m_ * sinc_ser * exp_ser), (tp, 0, tt)))
lam = sp.symbols("lam")
_tr = sp.expand(phihat.subs({kx: lam * kx, ky: lam * ky, kz: lam * kz}))
phihat_tr = sum(_tr.coeff(lam, n) for n in range(0, ORDER))
Tsym, Tp = sp.symbols("T Tp")
ghat = sp.expand(Pi_ * sp.integrate((Tsym - tt) * phihat_tr, (tt, 0, Tsym)))   # g_hat, AC18 step 2
ARGS = (Tsym, Pi_, G_, c_, m_, vs, es[0], es[1], es[2])
COEF = []
for mono, coef in sp.Poly(ghat, kx, ky, kz).terms():
    if sum(mono) == 0:
        continue
    cdv = sp.integrate(coef.subs(Tsym, Tp), (Tp, 0, Tsym))                       # Int_0^T
    cdq = -Pi_ * sp.integrate((Tsym - Tp) * coef.subs(Tsym, Tp), (Tp, 0, Tsym))  # -Pi Int_0^T (T - T')
    COEF.append((mono, sp.lambdify(ARGS, cdv, "mpmath"), sp.lambdify(ARGS, cdq, "mpmath"), sum(mono)))

_cache = {}


def dH(xo, xb, n):
    """d^n H at xo (H homogeneous of degree -3), mpmath numerical differentiation at 50 digits (AC18 method)."""
    key = (tuple(mp.nstr(c, 40) for c in xo), mp.nstr(xb, 20), tuple(n))
    if key in _cache:
        return _cache[key]
    r = mp.sqrt(sum(c * c for c in xo))
    u = tuple(c / r for c in xo)
    if sum(n) == 0:
        v = Hnum(*u, xb) / r ** 3
    else:
        v = mp.diff(lambda a, b, c: Hnum(a, b, c, xb), u, tuple(n)) / r ** (3 + sum(n))
    _cache[key] = v
    return v


def add(n, j, k=1):
    nn = list(n)
    nn[j] += k
    return tuple(nn)


def response(xo, xb, T, Pi_v, Gv, cv, m, vsv, esv, want=("dv", "Q"), max_deg=3):
    """Outside-cone leading-order response (AC18 chain).
    dv_j  = K sum c_dv (-i)^|a| d_j d^a H                      (khronon flow, AC18)
    Q_ij  = K sum c_dq (-i)^|a| d_i d_j d^a H                  (Q_ij = -Pi Int (t-t') d_i d_j Xi; tr Q = dq)
    dvlap_j = K sum c_dv (-i)^|a| (-lap) d_j d^a H / Pi       (lambda channel per unit lambda'', iter_2)
    Each returned with the sum of |terms| (for the floor)."""
    K = 4 * mp.pi * Gv
    args = (T, Pi_v, Gv, cv, m, vsv, *esv)
    out = {"dv": [mp.mpc(0)] * 3, "dv_abs": [mp.mpf(0)] * 3, "dv_dip": [mp.mpc(0)] * 3,
           "Q": [[mp.mpc(0)] * 3 for _ in range(3)], "Q_abs": [[mp.mpf(0)] * 3 for _ in range(3)],
           "dvlap": [mp.mpc(0)] * 3, "dvlap_abs": [mp.mpf(0)] * 3}
    for mono, fdv, fdq, deg in COEF:
        if deg > max_deg:
            continue
        ph = (-1j) ** deg
        cvv = fdv(*args)
        if "dv" in want:
            for j in range(3):
                val = K * cvv * ph * dH(xo, xb, add(mono, j))
                out["dv"][j] += val; out["dv_abs"][j] += abs(val)
                if deg == 1:
                    out["dv_dip"][j] += val
        if "Q" in want:
            cq = fdq(*args)
            for i in range(3):
                for j in range(i, 3):
                    val = K * cq * ph * dH(xo, xb, add(add(mono, i), j))
                    out["Q"][i][j] += val; out["Q_abs"][i][j] += abs(val)
        if "dvlap" in want:
            for j in range(3):
                for l in range(3):
                    val = -K * cvv * ph * dH(xo, xb, add(add(mono, j), l, 2)) / Pi_v
                    out["dvlap"][j] += val; out["dvlap_abs"][j] += abs(val)
    for i in range(3):
        for j in range(i):
            out["Q"][i][j] = out["Q"][j][i]; out["Q_abs"][i][j] = out["Q_abs"][j][i]
    return out


Msun, pc = mp.mpf("1.98847e30"), mp.mpf("3.0856775814913673e16")
cv, Gv = mp.mpf(299792458), mp.mpf("6.67430e-11")
FOOT = {"canonical": {"a0": "9.3603e-11", "rho0": "0.0447", "x": "1.15", "Lstar_pc": "21.68"},
        "alt": {"a0": "1.1312e-10", "rho0": "0.0514", "x": "2.6", "Lstar_pc": "22.85"}}
e_s = [1 / mp.sqrt(3)] * 3
DIRS = {"+e": (0, 0, 1), "-e": (0, 0, -1), "perp_x": (1, 0, 0), "perp_y": (0, 1, 0),
        "45_xz": (1 / mp.sqrt(2), 0, 1 / mp.sqrt(2)), "45_y-z": (0, 1 / mp.sqrt(2), -1 / mp.sqrt(2))}
GRID = [(1, 1e9), (1, 1e10), (10, 1e10)]          # AC18's outside-cone cells
EPS = mp.mpf(2) ** -52
