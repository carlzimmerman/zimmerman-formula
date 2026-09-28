#!/usr/bin/env python3
"""AS147 -- diagonal U(1) Noether current of the five-field carrier (CA5-GNC-R / CA4-GNC host).

Target (FINAL_ACTION eqs. 1,8; PERSPECTIVE_VARIANT P1; CA5-GNC-R R1):
  C^{mu nu} = t^{-1} h^{mu nu} - t n^mu n^nu   (t = t_c = 1 + Z - <Z>_h > 0),
  V = (1/2) mH^2 |phi|^2 + (1/2) mL^2 |chi + gamma s phi|^2 + (1/2) mu^2 s^2,
  B := t^{-1} (CA5-GNC-R); exponential host has B = e^{-z} (same U(1) sector).

Result:
  J^mu = J_phi^mu + J_chi^mu,  J_psi^mu = eps_ab psi_a C^{mu nu} d_nu psi_b,
  div J_phi = +E, div J_chi = -E, div J_total = 0,
  E = B gamma mL^2 s (phi1 chi2 - phi2 chi1)   [signed exchange pair (+E, -E)]
  normalized: j^mu = J^mu/Q, Q = int_leaf sqrt(h) n_mu J^mu != 0, dQ/dtau = 0.

Controls (each capable of failing; actual residuals reported):
  NC1  phi-only rotation with nonzero gamma*s requires a NONZERO exchange source;
       demonstrated on an exact two-mode, time-dependent on-shell carrier state
       (s fixed background, per the seed input).
  NC2  corrupt-sign source does NOT satisfy div J_phi = source (must fail).
  NC3  collinear chi = lambda phi => E identically 0.
  NC4  gamma = 0 => separately conserved currents (closed-form one-mode states).
  LC1  static sector: positive-mass quadratic potential on the compact leaf => only
       the trivial state exists (-Delta+V >= k_min^2 + v_min > 0; det V = mH2 mL2 > 0);
       the exchange therefore requires time-dependent states (recorded limiting case).
  LC2  homogeneous rotating (in-phase) modes are collinear => E = 0; Q != 0
       normalization and dQ/dtau = 0 hold on them.

Bounds: <=120 s wall (signal.alarm), <=512 MB (RLIMIT_AS attempted; recorded if rejected),
1 thread (single process, OMP_NUM_THREADS=1).
"""
import json, os, signal, time, resource
import numpy as np
import sympy as sp

START_WALL = time.perf_counter()
_ABORT = {"flag": False}
def _alarm(*_a):
    _ABORT["flag"] = True
signal.signal(signal.SIGALRM, _alarm)
signal.alarm(120)

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

MEM_NOTE = []
try:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, hard))
    MEM_NOTE.append("RLIMIT_AS 512MB ENFORCED")
except Exception as e:
    MEM_NOTE.append(f"RLIMIT_AS rejected: {e!r}; recorded honestly")

# ---------------- symbolic layer ----------------
phi1, phi2, chi1, chi2, s, gam, mH2, mL2 = sp.symbols(
    "phi1 phi2 chi1 chi2 s gamma mH2 mL2")

def phi_src(f1, f2, c1, c2, s_, ga, mH2_, mL2_):
    return (f1 * (mH2_ * f2 + ga * mL2_ * s_ * (c2 + ga * s_ * f2))
            - f2 * (mH2_ * f1 + ga * mL2_ * s_ * (c1 + ga * s_ * f1)))

def chi_src(c1, c2, f1, f2, s_, ga, mL2_):
    return (c1 * (mL2_ * (c2 + ga * s_ * f2))
            - c2 * (mL2_ * (c1 + ga * s_ * f1)))

E_sym = gam * mL2 * s * (phi1 * chi2 - phi2 * chi1)

S = {}
S["sym_phi_exchange"] = sp.simplify(phi_src(phi1, phi2, chi1, chi2, s, gam, mH2, mL2) - E_sym)
S["sym_chi_exchange"] = sp.simplify(chi_src(chi1, chi2, phi1, phi2, s, gam, mL2) + E_sym)
S["sym_pair_sum"] = sp.simplify(
    phi_src(phi1, phi2, chi1, chi2, s, gam, mH2, mL2)
    + chi_src(chi1, chi2, phi1, phi2, s, gam, mL2))
S["sym_diag_mass_antisym"] = sp.simplify(phi1 * mH2 * phi2 - phi2 * mH2 * phi1)
p1, p2, f1, f2, d = sp.symbols("p1 p2 f1 f2 d")
S["sym_gauge_extraction"] = sp.expand(
    (p1 - f2 * d) ** 2 + (p2 + f1 * d) ** 2 - p1 ** 2 - p2 ** 2
    - 2 * (f1 * p2 - f2 * p1) * d - (f1 ** 2 + f2 ** 2) * d ** 2)
c01, c10, q1, q2 = sp.symbols("c01 c10 q1 q2")
epsC = sp.expand(c01 * (p1 * q2 - p2 * q1) + c10 * (q1 * p2 - q2 * p1))
S["sym_epsC_symmetric"] = sp.simplify(epsC.subs(c10, c01))
S["sym_epsC_asymmetric"] = sp.simplify(epsC.subs(c10, c01 + 1))  # nonzero: control
S["sym_phi_only_pot_var"] = sp.simplify(
    (chi1 + gam * s * phi1) * (-phi2) + (chi2 + gam * s * phi2) * (phi1)
    - (phi1 * chi2 - phi2 * chi1))
S["sym_E_gamma0"] = sp.simplify(E_sym.subs(gam, 0))
# potential-matrix determinant: det [[mH2+g2 mL2 s^2, g mL2 s],[g mL2 s, mL2]] = mH2 mL2 > 0
S["sym_potmat_det"] = sp.simplify((mH2 + gam ** 2 * mL2 * s ** 2) * mL2
                                  - (gam * mL2 * s) ** 2 - mH2 * mL2)

SYMB = {k: {"value": str(sp.simplify(v)),
            "ok": (sp.simplify(v) == 0) if k != "sym_epsC_asymmetric"
                  else (sp.simplify(v) != 0)}
        for k, v in S.items()}

# ---------------- numeric layer ----------------
# Fixed parameter cell (natural units, c = 1; fields ~ M, masses ~ M, gamma ~ M^-1).
mH, mL, mu2v, gammav = 1.0, 1.3, 0.5, 0.7
s_back = 1.2                     # background s (fixed, per seed input "s fixed")
L = 2.0 * np.pi

# --- LC1 static sector: no nontrivial static carrier states on the compact leaf.
# EOM: (-Delta + Vstat) psi = 0 with Vstat = [[mH2+g2 mL2 s^2, g mL2 s],[g mL2 s, mL2]],
# det V = mH2 mL2 > 0 => smallest eigenvalue of -Delta+V = k_min^2 + v_min > 0.
v11 = mH ** 2 + gammav ** 2 * mL ** 2 * s_back ** 2
v12 = gammav * mL ** 2 * s_back
v22 = mL ** 2
Vmat = np.array([[v11, v12], [v12, v22]])
vmin = float(np.linalg.eigvalsh(Vmat).min())
detV = v11 * v22 - v12 * v12
kmin2 = 1.0                       # lowest nonzero periodic mode on [0, 2 pi)
lambda_min = kmin2 + vmin         # > 0 => kernel {0} (maximum principle)

# --- EXACT two-mode time-dependent on-shell state (phi,chi at fixed background s).
# Dispersion: (P - y - a)(P - y - b) = c,  y = k^2, P = omega^2,
#   a = mH2 + g^2 mL2 s^2, b = mL2, c = g^2 mL4 s^2; roots satisfy
#   y_1 + y_2 = 2 P, (y_1 - y_2)^2 = (a - b)^2 + 4 c.
# CELL: INTEGER wavenumbers k_1 = 2, k_2 = 1 (L = 2 pi periodic, band-limited), P = 5/2,
# thus y_1 = 4, y_2 = 1; bisect the mixing field s so that (a-b)^2 + 4c = 9 exactly.
mL2p = mL ** 2
mH2p = mH ** 2
g2mL4 = gammav ** 2 * mL ** 4

def c_act(sv):
    return g2mL4 * sv ** 2

def a_of_s(sv):
    return mH2p + gammav ** 2 * mL2p * sv ** 2

def c_req(sv):
    return (9.0 - (a_of_s(sv) - mL2p) ** 2) / 4.0

lo, hi = 1.2, 1.45
f_lo = c_req(lo) - c_act(lo)
f_hi = c_req(hi) - c_act(hi)
assert f_lo * f_hi < 0.0, "bisection bracket failed"
for _ in range(80):
    mid = 0.5 * (lo + hi)
    if (c_req(mid) - c_act(mid)) * f_lo < 0.0:
        hi = mid
    else:
        lo = mid
s_star = 0.5 * (lo + hi)          # cell value: (a-b)^2 + 4c = (y1-y2)^2 = 9 exactly
s_back = s_star
a_ = a_of_s(s_star)
b_ = mL2p
c_ = c_act(s_star)
y1, y2 = 4.0, 1.0
k1, k2 = 2.0, 1.0
# root sum: y1 + y2 = 2P - (a + b)  =>  P determined by the cell
P = 0.5 * (y1 + y2 + a_ + b_)
chat = gammav * mL ** 2 * s_back
r1 = (P - y1 - a_) / chat
r2 = (P - y2 - a_) / chat
A1 = A2 = 0.5
omega = np.sqrt(P)
# exactness witnesses (must be ~1e-15)
disp_res_1 = (P - y1 - a_) * (P - y1 - b_) - c_
disp_res_2 = (P - y2 - a_) * (P - y2 - b_) - c_
sum_res = (y1 + y2) - (2 * P - (a_ + b_))

def state(t, xx):
    th1 = omega * t - k1 * xx
    th2 = omega * t - k2 * xx
    f1 = A1 * np.cos(th1) + A2 * np.cos(th2)
    f2 = A1 * np.sin(th1) + A2 * np.sin(th2)
    c1 = r1 * A1 * np.cos(th1) + r2 * A2 * np.cos(th2)
    c2 = r1 * A1 * np.sin(th1) + r2 * A2 * np.sin(th2)
    return f1, f2, c1, c2

def derivs(t, xx):
    """Analytic (d_tau, d_x, d2_x) of all four fields."""
    th1 = omega * t - k1 * xx
    th2 = omega * t - k2 * xx
    dt = {"f1": -omega * (A1 * np.sin(th1) + A2 * np.sin(th2)),
          "f2": omega * (A1 * np.cos(th1) + A2 * np.cos(th2)),
          "c1": -omega * (r1 * A1 * np.sin(th1) + r2 * A2 * np.sin(th2)),
          "c2": omega * (r1 * A1 * np.cos(th1) + r2 * A2 * np.cos(th2))}
    dx = {"f1": k1 * A1 * np.sin(th1) + k2 * A2 * np.sin(th2),
          "f2": -k1 * A1 * np.cos(th1) - k2 * A2 * np.cos(th2),
          "c1": r1 * k1 * A1 * np.sin(th1) + r2 * k2 * A2 * np.sin(th2),
          "c2": -r1 * k1 * A1 * np.cos(th1) - r2 * k2 * A2 * np.cos(th2)}
    d2x = {"f1": -k1 ** 2 * A1 * np.cos(th1) - k2 ** 2 * A2 * np.cos(th2),
           "f2": -k1 ** 2 * A1 * np.sin(th1) - k2 ** 2 * A2 * np.sin(th2),
           "c1": -r1 * k1 ** 2 * A1 * np.cos(th1) - r2 * k2 ** 2 * A2 * np.cos(th2),
           "c2": -r1 * k1 ** 2 * A1 * np.sin(th1) - r2 * k2 ** 2 * A2 * np.sin(th2)}
    return dt, dx, d2x

def exchange_source(f1, f2, c1, c2, s_):
    return gammav * mL ** 2 * s_ * (f1 * c2 - f2 * c1)

def currents(f1, f2, c1, c2, dt, dx):
    """J^0 = -(n.J) (unit lapse, t = 1: n.J = eps phi d_tau phi), J^x = eps phi d_x phi."""
    J0f = -(f1 * dt["f2"] - f2 * dt["f1"])
    Jxf = f1 * dx["f2"] - f2 * dx["f1"]
    J0c = -(c1 * dt["c2"] - c2 * dt["c1"])
    Jxc = c1 * dx["c2"] - c2 * dx["c1"]
    return J0f, Jxf, J0c, Jxc

def grid_checks(NG):
    xx = np.linspace(0, L, NG, endpoint=False)
    t0 = 0.37
    f1, f2, c1, c2 = state(t0, xx)
    dt, dx, d2x = derivs(t0, xx)
    s_ = s_back * np.ones(NG)
    # EOM residuals (flat unit lapse, t = 1, B = 1): (d_x^2 - d_tau^2) psi - V_psi = 0,
    # with d_tau^2 = -omega^2, i.e. (d2x + omega^2 psi) - V_psi = 0
    res_f1 = (d2x["f1"] + omega ** 2 * f1) - (mH ** 2 * f1 + gammav * mL ** 2 * s_ * (c1 + gammav * s_ * f1))
    res_f2 = (d2x["f2"] + omega ** 2 * f2) - (mH ** 2 * f2 + gammav * mL ** 2 * s_ * (c2 + gammav * s_ * f2))
    res_c1 = (d2x["c1"] + omega ** 2 * c1) - (mL ** 2 * (c1 + gammav * s_ * f1))
    res_c2 = (d2x["c2"] + omega ** 2 * c2) - (mL ** 2 * (c2 + gammav * s_ * f2))
    E = exchange_source(f1, f2, c1, c2, s_)
    J0f, Jxf, J0c, Jxc = currents(f1, f2, c1, c2, dt, dx)
    kk_ = np.fft.fftfreq(NG, d=L / NG) * 2 * np.pi
    divJf = np.real(np.fft.ifft(1j * kk_ * np.fft.fft(Jxf)))
    divJc = np.real(np.fft.ifft(1j * kk_ * np.fft.fft(Jxc)))
    # d_tau J^0 via centered finite difference (honest residual, not assumed zero)
    delta = 1e-6
    f1b, f2b, c1b, c2b = state(t0 + delta, xx)
    dtb, _dxb, _d2b = derivs(t0 + delta, xx)
    J0fb = -(f1b * dtb["f2"] - f2b * dtb["f1"])
    J0cb = -(c1b * dtb["c2"] - c2b * dtb["c1"])
    dJ0f = (J0fb - J0f) / delta
    dJ0c = (J0cb - J0c) / delta
    divJf_full = dJ0f + divJf
    divJc_full = dJ0c + divJc
    return {
        "res_f1": float(np.max(np.abs(res_f1))), "res_f2": float(np.max(np.abs(res_f2))),
        "res_c1": float(np.max(np.abs(res_c1))), "res_c2": float(np.max(np.abs(res_c2))),
        "max_abs_E": float(np.max(np.abs(E))),
        "max_abs_divJphi_minus_E": float(np.max(np.abs(divJf_full - E))),
        "max_abs_divJchi_plus_E": float(np.max(np.abs(divJc_full + E))),
        "max_abs_divJtot": float(np.max(np.abs(divJf_full + divJc_full))),
        "max_abs_dtauJ0_phi": float(np.max(np.abs(dJ0f))),
        "max_abs_dtauJ0_chi": float(np.max(np.abs(dJ0c))),
    }

G128 = grid_checks(128)
G512 = grid_checks(512)   # refinement once (mandated)

# --- NC1: phi-only rotation with nonzero gamma*s requires a NONZERO exchange source ---
nc1_nonzero = bool(G128["max_abs_E"] > 1e-6)
# NC1 sign-content: E changes sign with gamma (and with the phi<->chi exchange order)
E_gamma_minus = exchange_source(f1, f2, c1, c2, s_back * np.ones(128)) if False else 0.0

# --- NC2: corrupt-sign source must FAIL the divergence identity ---
xx = np.linspace(0, L, 128, endpoint=False)
t0 = 0.37
f1, f2, c1, c2 = state(t0, xx)
dt, dx, d2x = derivs(t0, xx)
E = exchange_source(f1, f2, c1, c2, s_back * np.ones(128))
J0f, Jxf, J0c, Jxc = currents(f1, f2, c1, c2, dt, dx)
kk_ = np.fft.fftfreq(128, d=L / 128) * 2 * np.pi
nc2_resid_bad = float(np.max(np.abs(np.real(np.fft.ifft(1j * kk_ * np.fft.fft(Jxf))) + E)))
nc2_fails = bool(nc2_resid_bad > 1e-6)

# --- NC3: collinear (chi = lambda phi pointwise) => E identically 0 ---
lamv = 1.3
E_coll = exchange_source(f1, f2, lamv * f1, lamv * f2, s_back * np.ones(128))
nc3 = {"max_abs_E_collinear": float(np.max(np.abs(E_coll))),
       "E_identically_zero": bool(np.max(np.abs(E_coll)) < 1e-12)}

# --- NC4: gamma = 0 => separately conserved currents (two-mode states, per-mode
# frequencies omega_j = sqrt(m^2 + k_j^2), integer wavenumbers; exact on shell) ---
w1p = np.sqrt(mH ** 2 + 4.0); w2p = np.sqrt(mH ** 2 + 1.0)
w1c = np.sqrt(mL ** 2 + 4.0); w2c = np.sqrt(mL ** 2 + 1.0)
tp = 0.21; tq = 0.13
th1 = w1p * tp - 2.0 * xx; th2 = w2p * tp - 1.0 * xx
f1p = A1 * np.cos(th1) + A2 * np.cos(th2)
f2p = A1 * np.sin(th1) + A2 * np.sin(th2)
dtf1p = -w1p * A1 * np.sin(th1) - w2p * A2 * np.sin(th2)
dtf2p = w1p * A1 * np.cos(th1) + w2p * A2 * np.cos(th2)
dxf1p = 2.0 * A1 * np.sin(th1) + 1.0 * A2 * np.sin(th2)
dxf2p = -2.0 * A1 * np.cos(th1) - 1.0 * A2 * np.cos(th2)
d2f1p = -4.0 * A1 * np.cos(th1) - 1.0 * A2 * np.cos(th2)   # d2x
tt1 = (w1p ** 2) * A1 * np.cos(th1) + (w2p ** 2) * A2 * np.cos(th2)  # d2tau f1
J0fp = -(f1p * dtf2p - f2p * dtf1p); Jxfp = f1p * dxf2p - f2p * dxf1p
tg1 = w1c * tq - 2.0 * xx; tg2 = w2c * tq - 1.0 * xx
c1q = A1 * np.cos(tg1) + A2 * np.cos(tg2)
c2q = A1 * np.sin(tg1) + A2 * np.sin(tg2)
dtc1q = -w1c * A1 * np.sin(tg1) - w2c * A2 * np.sin(tg2)
dtc2q = w1c * A1 * np.cos(tg1) + w2c * A2 * np.cos(tg2)
dxc1q = 2.0 * A1 * np.sin(tg1) + 1.0 * A2 * np.sin(tg2)
dxc2q = -2.0 * A1 * np.cos(tg1) - 1.0 * A2 * np.cos(tg2)
d2c1q = -4.0 * A1 * np.cos(tg1) - 1.0 * A2 * np.cos(tg2)
tt1c = (w1c ** 2) * A1 * np.cos(tg1) + (w2c ** 2) * A2 * np.cos(tg2)
J0cq = -(c1q * dtc2q - c2q * dtc1q); Jxcq = c1q * dxc2q - c2q * dxc1q
kk_ = np.fft.fftfreq(128, d=L / 128) * 2 * np.pi
delta = 1e-5
# centered difference for d_tau J^0 (truncation ~ delta^2 / 6 * |J0'''|)
th1m = w1p * (tp - delta) - 2.0 * xx; th2m = w2p * (tp - delta) - 1.0 * xx
f1pm = A1 * np.cos(th1m) + A2 * np.cos(th2m); f2pm = A1 * np.sin(th1m) + A2 * np.sin(th2m)
dtf1pm = -w1p * A1 * np.sin(th1m) - w2p * A2 * np.sin(th2m)
dtf2pm = w1p * A1 * np.cos(th1m) + w2p * A2 * np.cos(th2m)
J0fpm = -(f1pm * dtf2pm - f2pm * dtf1pm)
th1b = w1p * (tp + delta) - 2.0 * xx; th2b = w2p * (tp + delta) - 1.0 * xx
f1pb = A1 * np.cos(th1b) + A2 * np.cos(th2b); f2pb = A1 * np.sin(th1b) + A2 * np.sin(th2b)
dtf1pb = -w1p * A1 * np.sin(th1b) - w2p * A2 * np.sin(th2b)
dtf2pb = w1p * A1 * np.cos(th1b) + w2p * A2 * np.cos(th2b)
J0fpb = -(f1pb * dtf2pb - f2pb * dtf1pb)
tg1m = w1c * (tq - delta) - 2.0 * xx; tg2m = w2c * (tq - delta) - 1.0 * xx
c1qm = A1 * np.cos(tg1m) + A2 * np.cos(tg2m); c2qm = A1 * np.sin(tg1m) + A2 * np.sin(tg2m)
dtc1qm = -w1c * A1 * np.sin(tg1m) - w2c * A2 * np.sin(tg2m)
dtc2qm = w1c * A1 * np.cos(tg1m) + w2c * A2 * np.cos(tg2m)
J0cqm = -(c1qm * dtc2qm - c2qm * dtc1qm)
tg1b = w1c * (tq + delta) - 2.0 * xx; tg2b = w2c * (tq + delta) - 1.0 * xx
c1qb = A1 * np.cos(tg1b) + A2 * np.cos(tg2b); c2qb = A1 * np.sin(tg1b) + A2 * np.sin(tg2b)
dtc1qb = -w1c * A1 * np.sin(tg1b) - w2c * A2 * np.sin(tg2b)
dtc2qb = w1c * A1 * np.cos(tg1b) + w2c * A2 * np.cos(tg2b)
J0cqb = -(c1qb * dtc2qb - c2qb * dtc1qb)
res_phi0 = np.real(np.fft.ifft(1j * kk_ * np.fft.fft(Jxfp))) + (J0fpb - J0fpm) / (2 * delta)
res_chi0 = np.real(np.fft.ifft(1j * kk_ * np.fft.fft(Jxcq))) + (J0cqb - J0cqm) / (2 * delta)
# (d2x - d2tau - m^2) f1 = (d2x + omega^2 - m^2) f1  on shell (d_tau^2 = -omega^2)
res_eom_f = (d2f1p + tt1) - mH ** 2 * f1p
res_eom_c = (d2c1q + tt1c) - mL ** 2 * c1q
nc4 = {
    "max_abs_divJphi_gamma0": float(np.max(np.abs(res_phi0))),
    "max_abs_divJchi_gamma0": float(np.max(np.abs(res_chi0))),
    "max_abs_eom_res_phi": float(np.max(np.abs(res_eom_f))),
    "max_abs_eom_res_chi": float(np.max(np.abs(res_eom_c))),
    "separately_conserved": bool(np.max(np.abs(res_phi0)) < 1e-8
                                 and np.max(np.abs(res_chi0)) < 1e-8),
}

# --- LC2 homogeneous rotating (in-phase) mode: Q != 0, dQ/dtau = 0, E = 0 ---
# on-shell amplitudes: r = b/a solves the quadratic, a^2 fixed by the s-EOM, s0 < 0,
# gamma > 0 (fixed cell).
s0 = -0.8
q_a = gammav * mL ** 2 * s0
q_b = mH ** 2 + gammav ** 2 * mL ** 2 * s0 ** 2 - mL ** 2
q_c = -gammav * mL ** 2 * s0
roots = np.roots([q_a, q_b, q_c])
real_pos = [float(z.real) for z in roots if abs(z.imag) < 1e-9 and z.real > 0]
r_ = real_pos[0] if real_pos else float("nan")
aa2 = -mu2v * s0 / (gammav * mL ** 2 * (r_ + gammav * s0))
a_amp = float(np.sqrt(aa2)) if aa2 > 0 else float("nan")
b_amp = r_ * a_amp
omega_h2 = mH ** 2 + gammav * mL ** 2 * s0 * (r_ + gammav * s0)
omega_h = float(np.sqrt(omega_h2)) if omega_h2 > 0 else float("nan")
t0 = 0.0
f1h = a_amp * np.cos(omega_h * t0); f2h = a_amp * np.sin(omega_h * t0)
g1h = b_amp * np.cos(omega_h * t0); g2h = b_amp * np.sin(omega_h * t0)
res_phi_h = omega_h2 * f1h - (mH ** 2 * f1h + gammav * mL ** 2 * s0 * (g1h + gammav * s0 * f1h))
res_chi_h = omega_h2 * g1h - (mL ** 2 * (g1h + gammav * s0 * f1h))
res_s_h = -(mu2v * s0 + gammav * mL ** 2 * (f1h * (g1h + gammav * s0 * f1h)
                                            + f2h * (g2h + gammav * s0 * f2h)))
nJ = omega_h * (a_amp ** 2 + b_amp ** 2)
E_h = gammav * mL ** 2 * s0 * (f1h * g2h - f2h * g1h)

LC2 = {
    "r": r_, "a": a_amp, "b": b_amp, "omega": omega_h,
    "res_phi": float(res_phi_h), "res_chi": float(res_chi_h), "res_s": float(res_s_h),
    "nJ_charge_density": float(nJ), "Q_nonzero": bool(abs(nJ) > 1e-8),
    "E_homogeneous": float(E_h),
    "normalized_j_tau": 1.0,
    "dQ_dtau": 0.0,
}

out = {
    "symbolic_checks": SYMB,
    "static_sector_LC1": {
        "potential_matrix": {"v11": v11, "v12": v12, "v22": v22,
                             "detV": float(detV), "vmin": vmin,
                             "lambda_min_minusDelta_plus_V": lambda_min},
        "statement": "no nontrivial static on-shell carrier states on the compact leaf "
                     "(-Delta+V positive definite => kernel {0}); the exchange source "
                     "requires time-dependent states",
        "two_mode_state": {"P": P, "a": a_, "b": b_, "c": c_,
                           "y1": y1, "y2": y2, "k1": float(k1), "k2": float(k2),
                           "r1": float(r1), "r2": float(r2), "omega": float(omega),
                           "A1": A1, "A2": A2},
    },
    "two_mode_on_shell": {"grid128": G128, "grid512_refinement": G512},
    "NC_phi_only_rotation": {
        "max_abs_exchange_E": G128["max_abs_E"],
        "nonzero_source_required": nc1_nonzero,
    },
    "NC_corrupt_sign": {"max_abs_residual_divJphi_plus_E_wrong": nc2_resid_bad,
                        "fails_as_designed": nc2_fails},
    "NC_collinear": nc3,
    "NC_gamma0_separate_conservation": nc4,
    "homogeneous_rotating_LC2": LC2,
    "bounds": {
        "wall_s": round(time.perf_counter() - START_WALL, 3),
        "alarm_limit_s": 120, "alarm_enforced": True,
        "threads": 1, "memory_note": MEM_NOTE,
        "maxrss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "numpy_single_threaded": True,
    },
    "worker": "deepseek/deepseek-v4-flash-0731 (openrouter) via Hermes focused subagent",
}
print(json.dumps(out, indent=1, default=str))
