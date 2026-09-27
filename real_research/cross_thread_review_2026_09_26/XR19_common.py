#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR19 shared machinery (imported by XR19_front_physics.py and XR19_web_runaway.py; runs nothing on import except small
tables).  Every rate here is FK1's / FP10's own formula, with FK1's normalisation; nothing new is fitted.

  * FK1's cosmology (H0 = 67.36, Omega_m = 0.3138, flat) and the LCDM growth D(z), f(z), df/dlna from the exact ODE.
  * FK1's constants read from its committed JSON: E_need(m) (N1), eps/m^2(v_k) (K2), q = 1.75 (N2).
  * delta = m v_k^2 / 2 (the energy per daughter, FK1 K2) in 1/s; the trigger coupling
        G_t(z) = sqrt(4 H(z) delta E_need / pi)                          (FK1 N3 / XR12: K4 at the trigger)
    and the vacuum gate (lambda ~ K^(-2q), K = 3H):  rho_t(z)/rho_bar(z) = delta_t0 E(z)^(2q + 1/2) / (1+z)^3
    (FK1 N2; q = 1.75 gives E^4, the linear cell's delta_t0 = (2/3) 2.5 / Omega_m = 5.31).  G(rho, z) = G_t(z) rho/rho_t(z).
  * The sweep gain.  A pair mode whose detuning runs D(t) = D1 t + alpha t^2 through the resonance |D| < G grows by
        int sqrt(G^2 - D^2) dt = G^(3/2) alpha^(-1/2) I(beta),   beta = D1 / sqrt(alpha G)
    (amplitude e-folds, FK1's convention), I(0) = C4 = 1.7480 (XR12 S1's second-order sweep) and I(beta) -> pi/(2 beta) for
    beta >> 1, which is FK1 K4's pi G^2/(4 H delta) at D1 = 2 H delta.  I(beta) integrates ONE passage (the connected window
    around t = 0).
  * The kinetic (Doppler-broadened) rate of a multistream pump of 1D dispersion sigma: gamma = sqrt(pi) G^2/(m v_k sigma)
    (FP10 A5's golden rule; FP10's convention, carried with a factor-1/2 bracket for the occupation-consistent reading).
  * Zel'dovich elements: for deformation eigenvalues d_i = D(z) lambda_i the physical strain eigenvalues are
    e_i = H (1 - f d_i/(1 - d_i)) and the density 1/prod(1 - d_i); their time derivatives follow from D, f, df/dlna.
    A daughter's relative velocity w = v - u obeys dw/dt = -T w (S1 in XR19_front_physics), so along a direction n the
    detuning rate is D1 = 2 delta e_nn and the curvature alpha = delta (2 |T n|^2 - n.Tdot.n).
  * A plane Zel'dovich pancake (exact before shell crossing) and a vectorised RK4 ray integrator for the exact detuning of a
    daughter pair along its path, used to calibrate the local zero-strain (cone) formula.
"""
import os, json, math
import numpy as np
from scipy.integrate import solve_ivp, quad

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# ------------------------------------------------------------------------------------------------ constants (FK1's)
C_KMS = 2.99792458e5
HBAR_EVS, C_MS, EV_J = 6.582119569e-16, 2.99792458e8, 1.602176634e-19
H0_SI = 67.36 * 1e3 / 3.0857e22                     # 1/s
OM, OL = 0.3138, 0.6862
H0_KPC = 67.36e-3                                    # km/s/kpc
TU = 3.0857e16                                       # s per kpc/(km/s)
DT0_LIN = (2.0 / 3.0) * 2.5 / OM                     # the linear cell's matter reading, 5.3100
Q_GATE = 1.75
C4 = float(quad(lambda u: math.sqrt(1 - u ** 4), -1, 1)[0])      # 1.748038
IQ = 2 * math.gamma(1.25)                            # int exp(-u^4) du = 1.8128 (kinetic second-order window)

FK1 = json.load(open(os.path.join(REPO, "real_research", "dark_fluid_kick_2026", "FK1_kick_as_phase_change_results.json")))["numbers"]
ENEED = {k_: float(v_["efolds"]) for k_, v_ in FK1["N1"]["by_mass"].items()}          # m [eV string] -> E_need
EPS_M2 = {float(k_): float(v_) for k_, v_ in FK1["K2"]["eps_over_m2"].items()}


def E(z): return np.sqrt(OM * (1 + z) ** 3 + OL)
def OMz(z): return OM * (1 + z) ** 3 / E(z) ** 2
def H_si(z): return H0_SI * E(z)


def _growth():
    def rhs(lna, y):
        z = math.exp(-lna) - 1.0; om = float(OMz(z))
        return [y[1], -(2 - 1.5 * om) * y[1] + 1.5 * om * y[0]]
    return solve_ivp(rhs, [math.log(1e-3), 0.3], [1e-3, 1e-3], dense_output=True, rtol=1e-11, atol=1e-14)


_GS = _growth()
_D0 = float(_GS.sol(0.0)[0])


def Dz(z): return float(_GS.sol(-math.log(1 + z))[0]) / _D0
def fz(z):
    y = _GS.sol(-math.log(1 + z)); return float(y[1] / y[0])
def dfdlna(z):
    om, f = float(OMz(z)), fz(z); return 1.5 * om - f * f - (2 - 1.5 * om) * f


# ------------------------------------------------------------------------------------------------ FK1's rates
def delta_split(m_ev, vk):
    """energy per daughter delta = m v_k^2/2 in frequency units [1/s] (FK1 K2 to O(v^2/c^2))."""
    return m_ev / HBAR_EVS * (vk / C_KMS) ** 2 / 2


def G_t(z, m_ev, vk, En):
    """the pair coupling at the trigger density [1/s]: pi G_t^2/(4 H delta) = E_need (FK1 K4/N3; XR12's G_t)."""
    return np.sqrt(4 * H_si(z) * delta_split(m_ev, vk) * En / math.pi)


def rho_t_over_mean(z, dt0=DT0_LIN, q=Q_GATE):
    """the gated trigger density in units of the mean carrier density at z (FK1 N2): dt0 E^(2q+1/2)/(1+z)^3."""
    return dt0 * E(z) ** (2 * q + 0.5) / (1 + z) ** 3


def fk1_n1(m_ev, vk=600.0, sig=100.0):
    """FK1 N1's e-folds, from its own lines: N_f = n_t (2 pi)^3/(4 pi k_k^2 dk) at rho_t = 1e3 rho_m0, sigma = 100 km/s."""
    H0 = 67.36 * 1e3 / 3.0857e22; rho_m0 = OM * 3 * H0 ** 2 / (8 * math.pi * 6.674e-11)
    m_kg = m_ev * EV_J / C_MS ** 2; hbar_SI = HBAR_EVS * EV_J
    n_t = 1e3 * rho_m0 / m_kg
    k_k = m_kg * vk * 1e3 / hbar_SI; dk = m_kg * sig * 1e3 / hbar_SI
    return math.log(n_t * (2 * math.pi) ** 3 / (4 * math.pi * k_k ** 2 * dk) / 0.5)


# ------------------------------------------------------------------------------------------------ the one-passage sweep integral
def _Ibeta(b):
    roots = []
    for c in (-1.0, 1.0):
        disc = b * b + 4 * c
        if disc >= 0:
            roots += [(-b - math.sqrt(disc)) / 2, (-b + math.sqrt(disc)) / 2]
    lo = max([r for r in roots if r < 0]); hi = min([r for r in roots if r > 0])
    return quad(lambda t: math.sqrt(max(1 - (b * t + t * t) ** 2, 0.0)), lo, hi, limit=400, points=[0.0])[0]


_BG = np.concatenate([[0.0], np.geomspace(1e-4, 1e5, 500)])
_IB = np.array([_Ibeta(b) for b in _BG])


def I_beta(b):
    b = np.abs(np.asarray(b, float))
    return np.where(b > _BG[-1], math.pi / (2 * np.maximum(b, 1e-300)), np.interp(b, _BG, _IB))


def sweep_gain(G, D1, alpha, cal=1.0):
    """amplitude e-folds of one passage of D(t) = D1 t + alpha t^2 through |D| < G.  cal multiplies the second-order part
    only (it is 1 in the first-order limit, where the formula is exact): factor cal + (1 - cal)(1 - exp(-|beta|))."""
    G = np.asarray(G, float)
    alpha = np.maximum(np.abs(np.asarray(alpha, float)), 1e-300)
    beta = np.asarray(D1, float) / np.sqrt(alpha * np.maximum(G, 1e-300))
    c = cal + (1 - cal) * (1 - np.exp(-np.abs(beta)))
    return G ** 1.5 / np.sqrt(alpha) * I_beta(beta) * c


def kinetic_rate(G, m_ev, vk, sig_kms):
    """FP10 A5: gamma = sqrt(pi) G^2 / (m v_k sigma) [1/s]; m v_k sigma = 2 delta sigma / v_k in frequency units."""
    return math.sqrt(math.pi) * np.asarray(G) ** 2 / (2 * delta_split(m_ev, vk) * np.asarray(sig_kms) / vk)


def cone_gain_kinetic(G, alpha, m_ev, vk, sig_kms):
    """a zero-strain (D1 = 0) passage through a Doppler-broadened resonance of width Delta = m v_k sigma:
    int gamma exp(-(alpha t^2/Delta)^2) dt = IQ sqrt(pi) G^2 / sqrt(Delta alpha)."""
    Dl = 2 * delta_split(m_ev, vk) * np.asarray(sig_kms) / vk
    return IQ * math.sqrt(math.pi) * np.asarray(G) ** 2 / np.sqrt(Dl * np.maximum(np.abs(alpha), 1e-300))


# ------------------------------------------------------------------------------------------------ Zel'dovich elements
def zeldovich_strain(d, z):
    """d: (..., k) deformation eigenvalues D lambda_i (< 1, single stream).  Returns e_i/H and (de_i/dt)/H^2."""
    f, fl, om = fz(z), dfdlna(z), float(OMz(z))
    dm = np.minimum(d, 1 - 1e-9)
    g = f * dm / (1 - dm)
    dg = fl * dm / (1 - dm) + f * f * dm / (1 - dm) ** 2               # (d g/dt)/H with d(d_i)/dt = H f d_i
    e = 1 - g
    edot = -1.5 * om * (1 - g) - dg                                      # Hdot/H^2 = -1.5 Omega_m(z)
    return e, edot


def cone_alpha_hat(e_neg, e_pos, edot_neg, edot_pos):
    """alpha/(delta H^2) on the zero-strain cone between a contracting axis (e_neg < 0) and an expanding one (e_pos > 0):
    n_neg^2 = e_pos/(e_pos - e_neg); |T n|^2 = -e_neg e_pos; alpha/delta = 2 |T n|^2 - n.Tdot.n."""
    n2 = e_pos / (e_pos - e_neg)
    return 2 * (-e_neg * e_pos) - (n2 * edot_neg + (1 - n2) * edot_pos)


# ------------------------------------------------------------------------------------------------ background in time (kpc, km/s units)
def _bg_time():
    def rhs(lna, y):
        z = math.exp(-lna) - 1.0; om = float(OMz(z)); Hh = H0_KPC * float(E(z))
        return [1.0 / Hh, y[2], -(2 - 1.5 * om) * y[2] + 1.5 * om * y[1]]
    a0 = 1e-3
    s = solve_ivp(rhs, [math.log(a0), 0.3], [2 / (3 * H0_KPC * math.sqrt(OM)) * a0 ** 1.5, a0, a0], dense_output=True,
                  rtol=1e-11, atol=1e-14)
    lna = np.linspace(math.log(a0), 0.3, 40001)
    Y = s.sol(lna)
    return lna, Y[0], Y[1] / float(s.sol(0.0)[1]), Y[2] / Y[1]


LNA_T, T_OF, D_OF, F_OF = _bg_time()


def t_of_z(z): return float(np.interp(-math.log(1 + z), LNA_T, T_OF))


def bg_t(t):
    lna = np.interp(t, T_OF, LNA_T); a = np.exp(lna); z = 1 / a - 1
    return a, z, H0_KPC * E(z), np.interp(lna, LNA_T, D_OF), np.interp(lna, LNA_T, F_OF)


class Pancake:
    """plane Zel'dovich pancake: comoving x = q - D (A/k) sin(k q); lengths in kpc, velocities km/s, time kpc/(km/s)."""

    def __init__(self, z_c, d_c, lam_comov_kpc):
        self.k = 2 * math.pi / lam_comov_kpc
        a, z, H, D, f = bg_t(t_of_z(z_c))
        self.A = d_c / float(D); self.tc = t_of_z(z_c); self.zc = z_c; self.dc = d_c

    def flow(self, r, t, q0):
        a, z, H, D, f = bg_t(t)
        x = r / a; k, A = self.k, self.A
        q = q0.copy()
        for _ in range(30):
            q -= (q - D * A / k * np.sin(k * q) - x) / (1 - D * A * np.cos(k * q))
        c = np.cos(k * q); s = np.sin(k * q)
        u = H * r - a * H * f * D * A / k * s
        ex = H * (1 - f * D * A * c / (1 - D * A * c))
        rho = 1 / (1 - D * A * c)
        return u, ex, rho, H, z, q, D * A


def pancake_rays(pc, nx, x0_frac, m_ev=2e-19, vk=600.0, En=178.05, dt0=DT0_LIN, s_frac=1.0, nstep=3000, span_H=0.25,
                 q_gate=Q_GATE, stimulated=True, return_paths=False, signs=(+1.0, -1.0)):
    """vectorised over the emission directions nx (component along the collapse axis); the pair is tangent to the local
    pump at (r0, t_c) with |w| = v_k.  Integrates dr/dt = u + w_x, dw_x/dt = -e_x w_x, dw_y/dt = -H w_y forward and backward
    (signs) over span_H/H (stopping before shell crossing) and returns int sqrt(max(G^2 - D^2, 0)) dt (amplitude e-folds);
    stimulated=False (the MUTATE of XR19_front_physics) removes the stimulated growth: the exponent is identically 0."""
    a, z, H, D, f = bg_t(pc.tc)
    lam_phys = a * 2 * math.pi / pc.k
    r0 = x0_frac * lam_phys / 2
    dl = delta_split(m_ev, vk)
    nx = np.asarray(nx, float); ny = np.sqrt(np.maximum(1 - nx ** 2, 0.0))
    span = span_H / float(H)
    total = np.zeros_like(nx); paths = []

    def rhs(r_, wx_, wy_, t_, q_):
        u_, ex_, rho_, H_, z_, q2, dA = pc.flow(r_, t_, q_)
        return u_ + wx_, -ex_ * wx_, -H_ * wy_, q2

    for sgn in signs:
        h = sgn * span / nstep
        r = np.full_like(nx, r0); wx = vk * nx; wy = vk * ny; t = pc.tc
        q = np.full_like(nx, r0 / a)
        acc = np.zeros_like(nx); prev = None; path = []
        for i in range(nstep + 1):
            u, ex, rho, Hh, zz, q, dA = pc.flow(r, t, q)
            if dA >= 0.995: break                                      # stop before the caustic
            rr = s_frac * rho / rho_t_over_mean(zz, dt0, q_gate)
            G = G_t(zz, m_ev, vk, En) * rr
            Dd = dl * ((wx ** 2 + wy ** 2) / vk ** 2 - 1)
            integ = np.sqrt(np.maximum(G ** 2 - Dd ** 2, 0.0)) if stimulated else np.zeros_like(G)
            if prev is not None: acc += 0.5 * (integ + prev) * abs(h) * TU
            prev = integ
            if return_paths: path.append((t, r.copy(), wx.copy(), wy.copy(), Dd.copy(), G.copy()))
            if i == nstep: break
            k1 = rhs(r, wx, wy, t, q)
            k2 = rhs(r + 0.5 * h * k1[0], wx + 0.5 * h * k1[1], wy + 0.5 * h * k1[2], t + 0.5 * h, k1[3])
            k3 = rhs(r + 0.5 * h * k2[0], wx + 0.5 * h * k2[1], wy + 0.5 * h * k2[2], t + 0.5 * h, k2[3])
            k4 = rhs(r + h * k3[0], wx + h * k3[1], wy + h * k3[2], t + h, k3[3])
            r = r + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            wx = wx + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            wy = wy + h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
            t = t + h
        total += acc
        paths.append(path)
    return (total, paths) if return_paths else total


def pancake_local_cone(pc, m_ev=2e-19, vk=600.0, En=178.05, dt0=DT0_LIN, s_frac=1.0, q_gate=Q_GATE):
    """the local zero-strain formula at the pancake centre: C4 G^(3/2)/sqrt(alpha); returns (gain, n_x on the cone, G, alpha,
    delta, rho/rho_t, E_need check from K4)."""
    a, z, H, D, f = bg_t(pc.tc)
    d = float(D) * pc.A
    e, ed = zeldovich_strain(np.array([d, 0.0]), float(z))
    ca = float(cone_alpha_hat(e[0], e[1], ed[0], ed[1]))
    Hs = float(H) / TU
    dl = delta_split(m_ev, vk)
    rr = s_frac * (1 / (1 - d)) / float(rho_t_over_mean(float(z), dt0, q_gate))
    G = float(G_t(float(z), m_ev, vk, En)) * rr
    alpha = dl * Hs * Hs * ca
    nx2 = e[1] / (e[1] - e[0])
    Eh = math.pi * float(G_t(float(z), m_ev, vk, En)) ** 2 / (4 * Hs * dl)
    return C4 * G ** 1.5 / math.sqrt(alpha), math.sqrt(nx2), G, alpha, dl, rr, Eh
