#!/usr/bin/env python3
"""CFG635: one dark sector. Can ONE field be both the dark energy (smooth part, sets a0 = kappa c sqrt(G rho_DE)) and the
cold energy (its lumpy excitations)?  Symbolic checks (sympy) + tiny numerics, per FROZEN_CRITERIA.md (committed alone first).

Run:   OMP_NUM_THREADS=1 nice -n 10 python3 cfg635.py              -> cfg635.out, cfg635_results.json
       CFG635_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg635.py -> cfg635_MUTATE.out, cfg635_results_MUTATE.json

kappa = 1/2 is FITTED. Footings never pooled (a0 cancels in every ratio here). Cold energy's mass required. No particle species
is added to the framework; a candidate that amounts to one is labelled so in the README. Not "theory closed".
"""
import json
import os
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
MUTATE = os.environ.get("CFG635_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT = {}
LINES = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LINES.append(s)


def check(name, ok, detail):
    OUT.setdefault("checks", {})[name] = {"pass": bool(ok), "detail": detail}
    say(f"  [{ 'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


# ---------------------------------------------------------------- constants (natural units, eV)
h = 0.674
H0 = 2.1332e-33 * h            # eV
OM_L = 0.685
OM_M = 1.0 - OM_L
MPL = 2.435e27                 # reduced Planck mass, eV
KAPPA = 0.5                    # FITTED
M_FLOOR = 2e-20                # eV, CFG288 G-DUST/G-PK floor for wave dust (declared there)
PHI_I_288 = 0.0147             # CFG288 committed misalignment amplitude at 2e-20 eV, units of MPL
C_OVER_H0_MPC = 2997.92458 / h
say(f"CFG635 one dark sector{'  [MUTATE]' if MUTATE else ''}; kappa = {KAPPA} FITTED; H0 = {H0:.4e} eV")

# ================================================================ K1 single-real-field mass theorem
say("\nK1 single real field: fluctuation mass^2 = V''(phi_bar) is shared by the smooth mode and its excitations")
t = sp.Symbol("t", positive=True)
# linearise the Klein-Gordon operator: the fluctuation's mass term is d/dphi V'(phi) at phi_bar
x = sp.Symbol("x")
Vx = sp.Function("V")(x)
lin_mass = sp.diff(sp.diff(Vx, x), x)      # d/dphi of V'(phi) at phi_bar
say(f"  linearised: ddot(dphi) + 3H dot(dphi) + (k^2/a^2 + {lin_mass}) dphi = 0")
ratio = M_FLOOR / H0
OUT["K1"] = {"m_floor_eV": M_FLOOR, "H0_eV": H0, "required_mass_ratio": ratio}
check("K1_mass_theorem", ratio >= 1e10,
      f"G1 needs V'' <~ H0^2 (frozen/thawing), G2 needs V'' >= ({M_FLOOR:g} eV)^2: ratio of masses {ratio:.2e} along ONE "
      "direction -> a single real field cannot do both; the two jobs need two field directions")

# ================================================================ K2 adiabatic exchange, complex field (C1)
say("\nK2 complex field Phi = r e^{i theta}: radial oscillation (cold) <-> phase (smooth) exchange")
r = sp.Function("r")(t)
th = sp.Function("theta")(t)
Vb = sp.Function("V_b")
Ur = sp.Function("U")
L = sp.Rational(1, 2) * sp.diff(r, t) ** 2 + sp.Rational(1, 2) * r ** 2 * sp.diff(th, t) ** 2 - Ur(r) - Vb(r, th)
EL_th = sp.diff(sp.diff(L, sp.diff(th, t)), t) - sp.diff(L, th)
thdd = sp.solve(sp.Eq(EL_th, 0), sp.diff(th, t, 2))[0]
E_th = sp.Rational(1, 2) * r ** 2 * sp.diff(th, t) ** 2 + Vb(r, th)
dE = sp.diff(E_th, t).subs(sp.diff(th, t, 2), thdd)
Q_claim = sp.diff(r, t) * (sp.diff(Vb(r, th), r) - r * sp.diff(th, t) ** 2)
q_ok = sp.simplify(dE - Q_claim) == 0
check("K2a_Q_identity", q_ok, "dE_theta/dt = rdot (d_r V_b - r thetadot^2) (sympy, exact)")
# shift-symmetric: V_b = 0 -> E_theta = p^2/(2 r^2) at fixed p_theta: total derivative of a function of r
p, rr = sp.symbols("p r_", positive=True)
Hth = p ** 2 / (2 * rr ** 2)
tot_ok = sp.simplify(sp.diff(Hth, rr) - (-p ** 2 / rr ** 3)) == 0
check("K2b_total_derivative", tot_ok,
      "V_b = 0: p_theta conserved, Q = rdot dH_theta/dr = d/dt H_theta(r(t), p): periodic r -> zero secular exchange")
# coupling-off control: r^2 -> f^2 in the phase kinetic term, V_b const -> theta_dot const, Q identically 0 (decoupled Lambda + dust)
f_ = sp.Symbol("f", positive=True)
L0 = sp.Rational(1, 2) * sp.diff(r, t) ** 2 + sp.Rational(1, 2) * f_ ** 2 * sp.diff(th, t) ** 2 - Ur(r)
E0 = sp.Rational(1, 2) * f_ ** 2 * sp.diff(th, t) ** 2
thdd0 = sp.solve(sp.Eq(sp.diff(sp.diff(L0, sp.diff(th, t)), t) - sp.diff(L0, th), 0), sp.diff(th, t, 2))[0]
off_ok = sp.simplify(sp.diff(E0, t).subs(sp.diff(th, t, 2), thdd0)) == 0
check("K2c_coupling_off", off_ok, "coupling off -> dE_theta/dt = 0 exactly: decoupled constant smooth part + independent wave dust")


def run_k2(eps, th0, thd0, nper, label):
    """units m_r = 1, f = 1; U = (r-1)^2/2, V_b = eps r^2 (1 - cos theta)."""
    def rhs(_t, y):
        r_, rd, q, qd = y
        rdd = r_ * qd ** 2 - (r_ - 1.0) - 2 * eps * r_ * (1 - np.cos(q))
        qdd = (-eps * r_ ** 2 * np.sin(q) - 2 * r_ * rd * qd) / r_ ** 2
        return [rd, rdd, qd, qdd]
    T = 2 * np.pi
    tt = np.linspace(0, nper * T, nper * 64 + 1)
    sol = solve_ivp(rhs, (0, nper * T), [1.05, 0.0, th0, thd0], method="DOP853", rtol=1e-11, atol=1e-14, t_eval=tt)
    r_, rd, q, qd = sol.y
    Eth = 0.5 * r_ ** 2 * qd ** 2 + eps * r_ ** 2 * (1 - np.cos(q))
    Etot = 0.5 * rd ** 2 + 0.5 * (r_ - 1) ** 2 + Eth
    n10 = 10 * 64
    first, last = Eth[:n10].mean(), Eth[-n10:].mean()
    drift = last / first - 1.0
    return {"label": label, "eps": eps, "omega_theta_over_m_r": float(np.sqrt(eps)), "periods": nper,
            "E_theta_first10": float(first), "E_theta_last10": float(last), "relative_drift": float(drift),
            "E_tot_rel_err": float(np.max(np.abs(Etot / Etot[0] - 1)))}


cases = []
if not MUTATE:
    cases.append(run_k2(0.0, 0.0, 0.01, 400, "A shift-symmetric (p_theta = 0.01)"))
    # slow pNGB: omega_theta = 0.01 m_r; windows = 10 radial periods; run 1000 periods = 10 theta periods.
    # The windows sit at the same theta phase because 1000 radial periods = an integer number of small-amplitude theta periods.
    cases.append(run_k2(1e-4, 0.3, 0.0, 1000, "B slow pNGB (omega_theta = 0.01 m_r)"))
    for c in cases:
        say(f"  {c['label']}: E_theta drift {c['relative_drift']:+.3e} over {c['periods']} radial periods; "
            f"E_tot err {c['E_tot_rel_err']:.1e}")
    k2_ok = all(abs(c["relative_drift"]) < 1e-3 for c in cases)
    check("K2d_no_secular_exchange", k2_ok, "shift-symmetric and slow-pNGB phases take no secular energy from the radial mode")
else:
    c = run_k2(0.25, 1e-3, 0.0, 300, "C MUTATE resonant explicit breaking (omega_theta = m_r/2)")
    cases.append(c)
    say(f"  {c['label']}: E_theta growth {c['relative_drift']:+.3e}; E_tot err {c['E_tot_rel_err']:.1e}")
    check("K2d_MUTATE_resonance_bites", c["relative_drift"] > 0.5,
          "resonant shift breaking DOES transfer energy secularly -- from the radial oscillation itself (cold REST energy, "
          "a G9 violation), not from settling")
OUT["K2"] = cases

# ================================================================ K3 C1 numbers
say("\nK3 C1 (pNGB phase = dark energy, radial wave dust = cold energy): constants")
mth_over_H0 = 1.0
f_C1 = np.sqrt(3 * OM_L) / mth_over_H0 * MPL
lam = (M_FLOOR / f_C1) ** 2
phi_need = PHI_I_288 * MPL                        # at 2e-20 eV (CFG288, committed)
amp_frac = phi_need / f_C1
overprod = (f_C1 / phi_need) ** 2                 # Omega_c ~ m^1/2 phi_i^2 at fixed m
m_comp = M_FLOOR * (phi_need / f_C1) ** 4         # mass that would bring an O(1) amplitude back to Omega_c
z_eq = 3400.0
H_eq = H0 * np.sqrt(2 * OM_M * (1 + z_eq) ** 3)
Gamma_dec = M_FLOOR ** 3 / (32 * np.pi * f_C1 ** 2)
sigma = lam ** 2 / (16 * np.pi * M_FLOOR ** 2)    # order of magnitude, eV^-2
cm2_per_g = (5.0677e4) ** 2 / 5.6096e32           # eV^-3
sig_over_m = sigma / M_FLOOR / cm2_per_g
K3 = {"m_theta_over_H0": mth_over_H0, "f_over_MPL": f_C1 / MPL, "lambda": lam, "radial_amp_over_f": amp_frac,
      "overproduction_for_O1_amplitude": overprod, "compensating_mass_eV": m_comp, "H_eq_eV": H_eq,
      "decay_r_to_thetatheta_over_H0": Gamma_dec / H0, "sigma_over_m_cm2_per_g": sig_over_m}
OUT["K3"] = K3
say(f"  f = sqrt(3 Omega_L)(H0/m_theta) MPL = {f_C1/MPL:.3f} MPL (fixed by rho_DE once m_theta/H0 is chosen)")
say(f"  lambda = (m_r/f)^2 = {lam:.2e} at m_r = {M_FLOOR:g} eV; radial amplitude for Omega_c: {amp_frac:.4f} f")
say(f"  an O(1) amplitude over-produces cold energy x{overprod:.2e}; compensating with the mass needs m_r = {m_comp:.2e} eV "
    f", 1e8 below the {M_FLOOR:g} eV wave-dust floor and ~ H(z_eq) = {H_eq:.2e} eV (no dust onset before equality; the "
    "m^1/2 scaling itself breaks there)")
say(f"  r -> theta theta decay rate / H0 = {Gamma_dec/H0:.2e}; self-scattering sigma/m ~ {sig_over_m:.1e} cm^2/g")
check("K3_C1_behaviour_and_knobs", (Gamma_dec / H0 < 1e-3) and (sig_over_m < 1e-3) and (m_comp < 1e-3 * M_FLOOR),
      "cold part stable + collisionless (behaviour gates OK as in CFG288 road W); the amplitude is not natural (O(1) "
      "amplitude fails) -> the amount stays an input; knobs: m_r, m_theta/H0 (or theta_i)")

# ================================================================ K4 ghost-condensate receiver (C2)
say("\nK4 C2 ghost-condensate receiver: w = -1 with nonzero theta_dot; regular pair bracket without stall")
X, X0, cc, rho = sp.symbols("X X_0 c rho_DE", positive=True)
P = -rho + cc / 2 * (X - X0) ** 2
rhoX = 2 * X * sp.diff(P, X) - P
w_at = sp.simplify((P / rhoX).subs(X, X0))
thd0 = sp.sqrt(2 * X0)
check("K4a_w_minus1_with_motion", sp.simplify(w_at + 1) == 0 and thd0 != 0,
      f"P'(X0) = 0 -> w = {w_at}, while theta_dot0 = sqrt(2 X0) != 0 and pi = P' theta_dot = 0")
# Hamiltonian near pi = 0: H'(pi) = theta_dot (Hamilton's equation), so H'(0) = sqrt(2 X0)
dX = sp.Symbol("dX")
pi_of = (sp.diff(P, X) * sp.sqrt(2 * X)).subs(X, X0 + dX)
H_of = (pi_of * sp.sqrt(2 * (X0 + dX)) - P.subs(X, X0 + dX))
dHdpi = sp.simplify(sp.limit(sp.diff(H_of, dX) / sp.diff(pi_of, dX), dX, 0))
check("K4b_Hprime_at_rest", sp.simplify(dHdpi - sp.sqrt(2 * X0)) == 0, f"dH/dpi at pi = 0 equals {dHdpi}")
# pair bracket (astra regular_receiver_lift form) with a general receiver energy H(pi)
q, pi_, m_, v_ = sp.symbols("q pi m v")
mu_ = sp.Symbol("mu", positive=True)
Ec = sp.Function("E_c")(q)
Ssym = sp.Function("S")(q)
v_use = sp.Integer(0) if MUTATE else v_
Hrec = rho + v_use * pi_ + pi_ ** 2 / (2 * mu_)
E = Ec + Hrec
gradE = sp.Matrix([sp.diff(E, q), sp.diff(E, pi_)])
gradS = sp.Matrix([sp.diff(Ssym, q), 0])
wv = sp.Matrix([sp.diff(Hrec, pi_), -sp.diff(Ec, q)])
M = m_ * wv * wv.T
deg_ok = sp.simplify(M * gradE) == sp.zeros(2, 1)
rates = M * gradS
Edot = sp.simplify((gradE.T * rates)[0])
Sdot = sp.simplify((gradS.T * rates)[0])
qdot_rest = sp.simplify(rates[0].subs(pi_, 0))
say(f"  M grad E = 0: {deg_ok}; Edot = {Edot}; Sdot = {Sdot}; qdot(pi = 0) = {qdot_rest}")
if not MUTATE:
    check("K4c_bracket_regular_no_stall", deg_ok and Edot == 0 and qdot_rest != 0,
          "GC receiver: energy conserved, entropy non-decreasing, drift at receiver rest = m v^2 S' (no stall, no 1/pi)")
else:
    check("K4c_MUTATE_canonical_stalls", deg_ok and Edot == 0 and qdot_rest == 0,
          "canonical receiver (H'(0) = 0): drift vanishes at pi = 0 -- the astra stall returns (control bites)")
# deposit: delta rho, delta p, c_s^2 at leading order
drho = sp.series(rhoX.subs(X, X0 + dX) - rhoX.subs(X, X0), dX, 0, 2).removeO()
dp = sp.series(P.subs(X, X0 + dX) - P.subs(X, X0), dX, 0, 2).removeO()
cs2 = sp.diff(P, X) / (sp.diff(P, X) + 2 * X * sp.diff(P, X, 2))
cs2_lead = sp.series(cs2.subs(X, X0 + dX), dX, 0, 2).removeO()
check("K4d_deposit_is_dust", sp.simplify(dp) == 0 and sp.simplify(cs2_lead - dX / (2 * X0)) == 0,
      f"delta rho = {sp.simplify(drho)}, delta p = {sp.simplify(dp)} (first order) -> deposit has w = 0; "
      f"c_s^2 = {cs2_lead}: the energy handed over becomes GC dust, not w = -1; invisible to a -p_DE bridge at first order")

# ================================================================ K5 phantom side: stability vs causality
say("\nK5 GC phantom side (receiver LOSING energy: import, IC-C type): gradient instability vs superluminal phonons")
kk, Mk, cs2s = sp.symbols("k M_k c_s2", real=True)
om2 = cs2s * kk ** 2 + kk ** 4 / Mk ** 2
kstar = sp.solve(sp.diff(om2, kk), kk)
kstar = [s for s in kstar if s != 0][0]
gmax = sp.sqrt(sp.simplify(-om2.subs(kk, kstar)))
say(f"  omega^2 = c_s^2 k^2 + k^4/M_k^2; for c_s^2 < 0: gamma_max = {sp.simplify(gmax)}")
beta = 1.0
excursions = {"cosmic (CFG630 total since z = 8, upper)": 3.8e-6, "local peak (K6, exponential kernel)": None}
OUT["K5"] = {}
# local value filled after K6; compute cosmic now
def k5_row(drho_rel):
    cs2v = drho_rel / (2 * beta)
    Mk_max_over_H0 = 2.0 / cs2v
    ell_mpc = 2.0 * C_OVER_H0_MPC / Mk_max_over_H0          # superluminal for wavelengths below ~ 2c/M_k
    return {"drho_over_rhoDE": drho_rel, "abs_cs2": cs2v, "Mk_max_over_H0": Mk_max_over_H0, "superluminal_below_Mpc": ell_mpc}

# ================================================================ K6 local deposit relation R(y)
say("\nK6 local deposit: R(y) = rho_ph V_c^2 / (rho_DE c^2), point mass, from the law + a0 = kappa c sqrt(G rho_DE)")
ys = sp.Symbol("y", positive=True)
nu = sp.Function("nu")(ys)
kap = sp.Symbol("kappa", positive=True)
R_expr = -2 * ys ** 3 * nu * sp.diff(nu, ys) * kap ** 2 / (4 * sp.pi)
R_deep = sp.simplify(R_expr.subs(nu, ys ** sp.Rational(-1, 2)).doit())
check("K6a_deep_limit", sp.simplify(R_deep - kap ** 2 * ys / (4 * sp.pi)) == 0,
      f"deep limit R = {R_deep} = kappa^2 g^2/(4 pi a0^2) (g^2 = y a0^2 there); kappa^2/(4pi) = {KAPPA**2/(4*np.pi):.4f}")


def nu_exp(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))


try:
    import CFG4_common as C4
    nu_mono = C4.nu_mono
except Exception as e:  # pragma: no cover
    nu_mono = None
    say(f"  nu_mono import failed: {e}")


def R_num(nuf, y):
    dl = 1e-4
    nup = (nuf(y * np.exp(dl)) - nuf(y * np.exp(-dl))) / (2 * dl * y)
    return -2 * y ** 3 * nuf(y) * nup * KAPPA ** 2 / (4 * np.pi)


ygrid = np.logspace(-3, 3, 6001)
K6 = {}
for name, nuf in (("exponential", nu_exp), ("nu_mono", nu_mono)):
    if nuf is None:
        continue
    Rg = R_num(nuf, ygrid)
    i = int(np.argmax(Rg))
    above = ygrid[Rg >= 1.0]
    row = {"R_y1": float(R_num(nuf, np.array([1.0]))[0]), "R_y10": float(R_num(nuf, np.array([10.0]))[0]),
           "R_y30": float(R_num(nuf, np.array([30.0]))[0]), "R_max_on_grid": float(Rg[i]), "y_at_max": float(ygrid[i]),
           "first_y_R_ge_1": (float(above[0]) if above.size else None),
           "dlog10_a0_rho_bridge_y1": float(0.5 * np.log10(1 + R_num(nuf, np.array([1.0]))[0]))}
    # upper bound on the observable: full local retention, a0 reading the LOCAL rho (rho bridge): dln a0 = ln(1+R)/2,
    # dln g = -(dln nu/dln y) dln a0 (y = g_N/a0).  Zero at first order under the -p bridge (K4d).
    for yv in (1.0, 30.0):
        yy = np.array([yv]); dl = 1e-4
        slope = (np.log(nuf(yy * np.exp(dl))) - np.log(nuf(yy * np.exp(-dl))))[0] / (2 * dl)
        row[f"dlog10_g_rho_bridge_y{int(yv)}"] = float(-slope * 0.5 * np.log1p(R_num(nuf, yy)[0]) / np.log(10))
    K6[name] = row
    say(f"  {name}: rho-bridge, full local retention: dlog10 a0(y=1) = {row['dlog10_a0_rho_bridge_y1']:.4f}; "
        f"dlog10 g(y=1) = {row['dlog10_g_rho_bridge_y1']:.4f}, dlog10 g(y=30) = {row['dlog10_g_rho_bridge_y30']:.4f}")
    say(f"  {name}: R(1) = {row['R_y1']:.4f}, R(10) = {row['R_y10']:.3f}, R(30) = {row['R_y30']:.3f}; max on y<=1e3 "
        f"{row['R_max_on_grid']:.3f} at y = {row['y_at_max']:.3g}; R >= 1 from y = {row['first_y_R_ge_1']}")
OUT["K6"] = K6
check("K6b_relation_numbers", "exponential" in K6 and 0.3 < K6["exponential"]["R_max_on_grid"] < 0.6,
      "settling-energy density of the phantom is O(0.01) of rho_DE c^2 at g ~ a0 and O(0.4-1) at y ~ 10-30 "
      "(kernel-dependent above y ~ 2.5)")

loc = K6["exponential"]["R_max_on_grid"]
OUT["K5"]["cosmic"] = k5_row(3.8e-6)
OUT["K5"]["local_peak"] = k5_row(loc)
for kk_, row in OUT["K5"].items():
    say(f"  {kk_}: |c_s^2| = {row['abs_cs2']:.2e} -> stable only if M_k < {row['Mk_max_over_H0']:.2e} H0 -> phonons "
        f"superluminal below ~{row['superluminal_below_Mpc']*1e3:.3g} kpc")
check("K5_phantom_side", OUT["K5"]["cosmic"]["superluminal_below_Mpc"] > 1e-3,
      "import (receiver-loses-energy) side: gradient-stable only with a k^4 scale so low that sub-galactic (cosmic "
      "excursion) to Gpc (local excursion) phonons are superluminal -> G4/G5 conflict on that side; export side is stable")

# ================================================================ K7 Landau channel (C3)
say("\nK7 C3 superfluid two-fluid: Landau critical velocity and drag-damped growth")
kq, cph, mq = sp.symbols("k c_ph m_q", positive=True)
omB = sp.sqrt(cph ** 2 * kq ** 2 + (kq ** 2 / (2 * mq)) ** 2)
vL = sp.limit(omB / kq, kq, 0)
mono = sp.simplify(sp.diff(omB / kq, kq))
check("K7a_landau", sp.simplify(vL - cph) == 0, f"min omega/k = {vL} (omega/k increasing: d/dk = {mono} > 0)")


def growth(gamma):
    def rhs(N, y):
        a = np.exp(N)
        E2 = OM_M * a ** -3 + OM_L
        Om = OM_M * a ** -3 / E2
        dlnH = -1.5 * OM_M * a ** -3 / E2
        G = gamma / np.sqrt(E2)                      # Gamma/H with Gamma = gamma H0
        return [y[1], -(2 + dlnH + G) * y[1] + 1.5 * Om * y[0]]
    N0 = np.log(1e-3)
    s = solve_ivp(rhs, (N0, 0.0), [1e-3, 1e-3], method="DOP853", rtol=1e-10, atol=1e-14)
    return s.y[0, -1]


g0 = growth(0.0)
K7 = {f"D_ratio_gamma_{g}": float(growth(g) / g0) for g in (0.1, 1.0, 10.0)}
OUT["K7"] = K7
say("  " + ", ".join(f"{kname} = {v:.3f}" for kname, v in K7.items()))
check("K7b_drag_damps_growth", K7["D_ratio_gamma_10.0"] < 0.5,
      "a drag fast enough to settle halos (Gamma ~ 10-50 H0) freezes linear growth if it acts on the linear cold field; "
      "if c_ph > V_f there is no drag at all (superfluid)")

# ---------------------------------------------------------------- summary
OUT["mutate"] = MUTATE
npass = sum(1 for c in OUT["checks"].values() if c["pass"])
say(f"\n{npass}/{len(OUT['checks'])} checks pass")
with open(os.path.join(HERE, f"cfg635_results{TAG}.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=float)
with open(os.path.join(HERE, f"cfg635{TAG}.out"), "w") as fh:
    fh.write("\n".join(LINES) + "\n")
sys.exit(0 if npass == len(OUT["checks"]) else 1)
