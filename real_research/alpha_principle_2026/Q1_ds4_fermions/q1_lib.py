"""Shared helpers for lane Q1 (Dirac fermion in dS_4).  Not a script; imported by q1_1, q1_2, q1_3.

Units H = 1, planar patch a = -1/tau, evaluation at tau = -1 (a = 1).  L = eE/H^2, M = m/H.
2x2 block Hamiltonian (k_perp along x):  h = sigma_z p(tau) + sigma_x kp + sigma_y M a(tau),  p = k r + L/tau, M a = -M/tau, r = cos(theta) = k_z/k.
"""
import sys
sys.dont_write_bytecode = True
import math
import numpy as np
import mpmath as mp
import sympy as sp

PI = math.pi
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
ID2 = np.eye(2, dtype=complex)


def h_matrix(tau, k, r, L, M, sperp=+1):
    p = k * r + L / tau
    Ma = -M / tau
    kp = sperp * k * math.sqrt(max(0.0, 1.0 - r * r))
    return p * SZ + kp * SX + Ma * SY


# ------------------------------------------------------------------ Whittaker mode
def B_matrix(L, M):
    r0 = math.hypot(L, M)
    return (L * SZ - M * SY) / r0, r0


def whit_and_deriv(kappa, nu, z):
    """W_{kappa,nu}(z) and dW/dz via DLMF 13.15.23 (z W' = (z/2 - kappa) W - W_{kappa+1,nu})."""
    W = mp.whitw(kappa, nu, z)
    W1 = mp.whitw(kappa + 1, nu, z)
    dW = (mp.mpf(1) / 2 - kappa / z) * W - W1 / z
    return W, dW


def mode_spinor(k, r, L, M, tau=-1.0, s=+1, sperp=+1, index_shift=True):
    """Xi = (i d_tau + h)(phi w_s), phi = W_{kappa, nu_s}(2 i k tau), kappa = -i L r, nu_s = 1/2 - i s r0.
    index_shift=False is the MUTATE index (nu_s = - i s r0, the scalar-type index without the spin-1/2 shift)."""
    B, r0 = B_matrix(L, M)
    ev, evec = np.linalg.eigh(B)
    idx = 0 if ev[0] > 0 else 1                       # eigenvalue +1
    if s < 0:
        idx = 1 - idx
    w = evec[:, idx]
    kappa = -1j * mp.mpf(L) * mp.mpf(r)
    nu = (mp.mpf(1) / 2 if index_shift else mp.mpf(0)) - 1j * s * mp.mpf(r0)
    z = 2j * mp.mpf(k) * mp.mpf(tau)
    W, dW = whit_and_deriv(kappa, nu, z)
    phi = complex(W)
    dphi = complex(dW * 2j * mp.mpf(k))
    h = h_matrix(tau, k, r, L, M, sperp)
    return 1j * dphi * w + phi * (h @ w)


def sz_from_spinor(v):
    a, b = abs(v[0]) ** 2, abs(v[1]) ** 2
    return (a - b) / (a + b)


def sz_pair(k, r, L, M, tau=-1.0):
    """s_z(+k_perp) + s_z(-k_perp) from the exact Whittaker mode (s = +1 eigenvector); the Whittaker function is evaluated once."""
    B, r0 = B_matrix(L, M)
    ev, evec = np.linalg.eigh(B)
    w = evec[:, 0 if ev[0] > 0 else 1]
    kappa = -1j * mp.mpf(L) * mp.mpf(r)
    nu = mp.mpf(1) / 2 - 1j * mp.mpf(r0)
    z = 2j * mp.mpf(k) * mp.mpf(tau)
    W, dW = whit_and_deriv(kappa, nu, z)
    phi = complex(W)
    dphi = complex(dW * 2j * mp.mpf(k))
    tot = 0.0
    for sp_ in (+1, -1):
        v = 1j * dphi * w + phi * (h_matrix(tau, k, r, L, M, sp_) @ w)
        tot += sz_from_spinor(v)
    return tot


# ------------------------------------------------------------------ adiabatic expansion (Bloch vector), symbolic
_AD_CACHE = {}


def build_adiabatic(order=2):
    """lambdified z-component of s_0 + s_1 + s_2 (order-truncated) for the sperp = +1 block, and the sperp = -1 block
    is obtained by kp -> -kp.  Arguments (tau, k, r, L, M, sgn) with sgn = sperp.  Returns f(tau,k,r,L,M,sgn)."""
    if order in _AD_CACHE:
        return _AD_CACHE[order]
    t, k, r, L, M, sg = sp.symbols("t k r L M sg", real=True)
    kp = sg * k * sp.sqrt(1 - r ** 2)
    n = sp.Matrix([kp, -M / t, k * r + L / t])            # Bloch vector of h = n . sigma
    om = sp.sqrt((n.T * n)[0])
    nh = n / om
    dn = nh.diff(t)
    s0 = nh
    s1 = -nh.cross(dn) / (2 * om)
    ds1 = s1.diff(t)
    s2 = -((s1.T * s1)[0]) * nh / 2 - nh.cross(ds1) / (2 * om)
    total = s0
    if order >= 1:
        total = total + s1
    if order >= 2:
        total = total + s2
    fz = sp.lambdify((t, k, r, L, M, sg), total[2], modules="numpy", cse=True)
    _AD_CACHE[order] = fz
    return fz


def ad_pair(k, r, L, M, tau=-1.0, order=2):
    f = build_adiabatic(order)
    return float(f(tau, k, r, L, M, +1)) + float(f(tau, k, r, L, M, -1))


# ------------------------------------------------------------------ published closed form HFY (3.12) (transcribed from the LaTeX source of arXiv:1603.04165)
def hfy_closed(Lv, Mv, dps=40, variant="printed"):
    """J_HFY(L, M) = <J^3>_ren/(e a^3 H^3), eq. (3.12) of arXiv:1603.04165 (minimal order-2 adiabatic subtraction).
    variant = "printed": the Ei term carries s e^{+2 pi r s} exactly as printed in the LaTeX source;
    variant = "amended": s e^{-2 pi r s} (Amendment 1(a) of the pre-registration: the 1/L^2 pole cancels and the term does not grow like e^{4 pi r})."""
    mp.mp.dps = dps
    L = mp.mpf(Lv)
    M = mp.mpf(Mv)
    r = mp.sqrt(L ** 2 + M ** 2)
    pi = mp.pi
    csch = lambda x: 1 / mp.sinh(x)
    t1 = 1 + 4 * L ** 2 / 15 + mp.mpf(4) / 3 * mp.log(M)
    t2 = 3 * M ** 2 / L ** 2 * (1 + r / (2 * L) * mp.log((r - L) / (r + L)))
    t3 = (r * csch(2 * pi * r) / (6 * pi ** 3 * L ** 2)
          * ((45 - pi ** 2 * (11 - 12 * L ** 2 + 8 * r ** 2)) * mp.cosh(2 * pi * L)
             - (45 - pi ** 2 * (11 - 72 * L ** 2 + 8 * r ** 2)) * mp.sinh(2 * pi * L) / (2 * pi * L)))
    ssum = 0
    for s in (+1, -1):
        ssum += s * mp.e ** ((2 if variant == 'printed' else -2) * pi * r * s) * (mp.ei(2 * pi * s * (r + L)) - mp.ei(2 * pi * s * (r - L)))
    t4 = -3 * r * M ** 2 * csch(2 * pi * r) / (4 * L ** 3) * ssum

    def integrand(x):
        poly = 1 + r ** 2 - (1 + 3 * L ** 2 + 3 * r ** 2) * x ** 2 + 5 * L ** 2 * x ** 4
        tot = 0
        for s in (+1, -1):
            tot += s * (mp.e ** (2 * pi * L * x) - mp.e ** (-2 * pi * r * s)) * mp.re(mp.psi(0, 1j * (L * x + r * s)))
        return poly * tot
    t5 = -csch(2 * pi * r) / 2 * mp.quad(integrand, [-1, -0.5, 0, 0.5, 1])
    return float(L / (4 * pi ** 2) * (t1 + t2 + t3 + t4 + t5))


def hfy_weak(Mv):
    """sigma_HFY(M) = lim J/L, HFY (4.3): (1/(3 pi^2)) [ln M - Re psi(iM) - pi M (4M^2+1)/(3 sinh(2 pi M))]."""
    mp.mp.dps = 40
    M = mp.mpf(Mv)
    return float((mp.log(M) - mp.re(mp.psi(0, 1j * M)) - mp.pi * M * (4 * M ** 2 + 1) / (3 * mp.sinh(2 * mp.pi * M))) / (3 * mp.pi ** 2))


# ------------------------------------------------------------------ scalar comparator: Kobayashi-Afshordi (2.58), copied from AH4 (already validated there)
def scalar_closed_f(lam, mu_phys):
    """f(lambda, mu) with <J_z> = e a H^3/(4 pi^2) f  (AH4 / K&A eq. 2.58)."""
    mp.mp.dps = 30
    lam = mp.mpf(lam)
    m = mp.mpf(mu_phys)
    mw = mp.sqrt(mp.mpf(9) / 4 - lam ** 2 - m ** 2)
    s2 = mp.sin(2 * mp.pi * mw)
    pi = mp.pi
    T1 = (45 + 4 * pi ** 2 * (-2 + 3 * lam ** 2 + 2 * mw ** 2)) * mw * mp.cosh(2 * pi * lam) / (12 * pi ** 3 * lam * s2)
    T2 = (45 + 8 * pi ** 2 * (-1 + 9 * lam ** 2 + mw ** 2)) * mw * mp.sinh(2 * pi * lam) / (24 * pi ** 4 * lam ** 2 * s2)

    def integrand(rr):
        poly = -1 + 4 * mw ** 2 + (7 + 12 * lam ** 2 - 12 * mw ** 2) * rr ** 2 - 20 * lam ** 2 * rr ** 4
        e1 = (mp.e ** (2 * pi * rr * lam) + mp.e ** (2j * pi * mw)) * mp.psi(0, mp.mpf(1) / 2 + mw + 1j * rr * lam)
        e2 = (mp.e ** (2 * pi * rr * lam) + mp.e ** (-2j * pi * mw)) * mp.psi(0, mp.mpf(1) / 2 - mw + 1j * rr * lam)
        return mp.re(1j * lam / (16 * s2) * poly * (e1 - e2))
    integ = mp.quad(integrand, [-1, -0.5, 0, 0.5, 1])
    return float(-2 * lam ** 3 / 15 + (lam / 3) * mp.log(m) + mp.re(T1) - mp.re(T2) + integ)
