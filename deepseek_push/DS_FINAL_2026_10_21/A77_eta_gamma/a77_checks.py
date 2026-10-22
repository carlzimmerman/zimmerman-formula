#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A77 -- DOES THE MEDIUM'S OWN THERMODYNAMICS FIX ITS SOUND SPEED?

Lane A77_eta_gamma.  Reads A69 (nothing in the action forces eta = gamma;
c_T^2 = gamma/eta = m_T^2 L*^2/2; the P stress is dust at O(eps); the elastic
pressure speed is sqrt(gamma rho_c) = 0.7204 m/s, NOT sqrt(gamma/eta);
gamma/eta < 1.916e-07 only IF the pressure were c_T^2 rho), A68 (the P-sector
coefficients: Z = K(2+3beta)/beta + eta p^2, m_T^2 = K/eta, c_T^2 = gamma/eta,
the gapless k^4 mode), A16 (the Gamma = 2 polytrope: c_s^2 = gamma rho_c,
lambda_J = sqrt2 pi L*, M_J at the switch) and A63 (the Langmuir gate), and
A72 (a0 = cH_Lambda/2pi from the thermal wavelength at T_dS).

The candidate closure tested here:

  (1/2) m_P <v^2> = (3/2) k_B T_dS  with  m_P = hbar/(c L*)
  =>  sigma_c^2 = 3 k_B T_dS / m_P ;  and if  c_T = sigma_c
  =>  gamma/eta = (sigma_c/c)^2 = 7.72e-10 .

Action (frozen, K = 4 pi G, c = 1, signature -+++), P sector only:

  L/(N sqrt h) = P^i D_i ln N - W(u) + (eta/2) E_i E^i
                 - (alpha/2)(D_i P^i)^2 - (gamma/4) F_ij F^ij
  u = K|P|,  E_i = (Pdot_i - Lie_N P_i)/N,  F_ij = d_iP_j - d_jP_i,
  W(u) = (a0^2/K)[-u/a0 - ln(1-u/a0)],  alpha = gamma (A68 D16).

Every number printed by this script is a number quoted in report.md.
Exit code 0 iff every check passes.

Usage
  python3 a77_checks.py [--json-out a77_results.json] [--mutate NAME]
  A77_MUTATE=NAME python3 a77_checks.py
Mutations: ct_light, a0_thermal, rho_c_x2, lstar_25, gamma_x2,
           soft_equipartition, no_pressure
"""

import argparse
import json
import math
import os
import sys

import numpy as np
import sympy as sp

# --------------------------------------------------------------------------
# units and constants.  Natural units hbar = c = 1; energies in eV.
# --------------------------------------------------------------------------
C_LIGHT = 299792458.0
HBARC = 1.973269804e-7          # eV m
PC = 3.08567758116e16           # m
MPC = 3.08567758116e22          # m
G_EV = 6.708830746153224e-57    # eV^-2  (= l_Pl^2 with the unreduced M_Pl)
K_EV = 4.0 * math.pi * G_EV     # eV^-2  (= 4 pi G, the action's normalisation)
HBAR_EV_S = 6.582119569e-16     # eV s
KB_EV_K = 8.617333262e-5        # eV / K
G_SI = 6.67430e-11
MSUN_KG = 1.98892e30

# cosmology used only for the growth ODE and the record's cluster scales
H0_HUB = 0.674                  # h
OM_M = 0.3153
OM_L = 0.6847
H0_SI = 100.0 * H0_HUB * 1000.0 / MPC        # s^-1
H0_EV = H0_SI * HBAR_EV_S                    # eV
H_LAM_EV = H0_EV * math.sqrt(OM_L)           # eV, measured route (H0 sqrt(Omega_L))

# the record's inputs (A16/A20/A33/A65/A69/A51)
RHO_C_EV4 = 9.7249e-12          # cold-sector density (A69), eV^4
RHO_C_KG = 2.2566e-27           # kg m^-3
A0_CAN_SI = 9.36e-11            # canonical footing
A0_TH_SI = 8.620e-11            # thermal footing, a0 = c H_Lambda / 2 pi (A72)
KAPPA_MEAS = 0.371              # A51: kappa = 0.371 +- 0.119
KAPPA_SIG = 0.119
A0_PER_KAPPA = 2.2624e-10       # a0 = kappa * A0_PER_KAPPA
LSTAR_PC = 24.0

# external reference values quoted in the record (not recomputed here)
CS_EL_A16 = 0.720473            # m/s   (A16 K8)
CS2_EL_A16 = 0.519081           # m^2/s^2 (A16 K8)
S_A69_1E7 = 0.9737              # A69 table: S(k=0.2) at c_s^2 = 1e-7
MJ_EL_A16 = 0.0212              # Msun, elastic Jeans mass at the cosmic mean (A16)
LAMC_TASK_KPC = 612.0           # the candidate closure's own number
BOUND_A69 = 1.916e-07           # gamma/eta < 1.916e-07 at 95 % CL (A69 O7)
R_SP_MPC = 1.414                # A29: splashback of the cluster stack (central)
U_HALF_MPC = 1.065              # A29: u = 1/2 crossing
R_V_MPC = 1.6863                # A18: r_v at M_b = 1.4e14
R200C_MPC = R_SP_MPC / 1.367    # A29 eq. (5): r_sp = 1.367 r200c

# --------------------------------------------------------------------------
# inputs, and the mutation dials (one input each)
# --------------------------------------------------------------------------
BASE = dict(
    a0_si=A0_CAN_SI,        # footing of a0 (and hence of sigma_c^2 = a0 L*)
    lstar_pc=LSTAR_PC,      # the fitted L*
    rho_c_ev4=RHO_C_EV4,    # cold-sector density, eV^4
    rho_c_kg=RHO_C_KG,      # the same density in kg m^-3
    gamma_factor=1.0,       # dial on gamma = K L*^2 / 2
    eq_dof=3,               # degrees of freedom in (1/2)m<v^2> = (dof/2)k_BT
    ct_mode="sigma",        # 'sigma': c_T = sigma_c ; 'light': c_T = c
    pressure=True,          # pressure term in the growth ODE
    shear=True,             # the F_ij F^ij gradient term in the quadratic action
    eos_factor=1.0,         # stiffness of the Gamma = 2 polytrope, e = (f*gamma/2) drho^2
    hlam_factor=1.0,        # dial on the measured H_Lambda (hence on T_dS)
)

MUTATIONS = {
    "ct_light": dict(ct_mode="light"),                    # c_T = c     (eta = gamma)
    "a0_thermal": dict(a0_si=A0_TH_SI),                   # a0 = cH_L/2pi
    "rho_c_x2": dict(rho_c_ev4=2.0 * RHO_C_EV4, rho_c_kg=2.0 * RHO_C_KG),
    "lstar_25": dict(lstar_pc=25.0),
    "gamma_x2": dict(gamma_factor=2.0),
    "soft_equipartition": dict(eq_dof=1),                 # 1 dof instead of 3
    "no_pressure": dict(pressure=False),
    "no_shear": dict(shear=False),                        # drop F_ij F^ij: no transverse stiffness
    "eos_half": dict(eos_factor=0.5),                     # halve the polytrope stiffness
    "hlam_x3": dict(hlam_factor=3.0),                     # T_dS and cH_L/2pi tripled
}

RESULTS = []


def a0_to_eV(a_si):
    return a_si / C_LIGHT ** 2 * HBARC


def derive(P):
    """Every derived quantity, from the input dict alone."""
    D = {}
    D["a0_ev"] = a0_to_eV(P["a0_si"])
    D["lstar_ev"] = P["lstar_pc"] * PC / HBARC
    D["gamma"] = P["gamma_factor"] * K_EV * D["lstar_ev"] ** 2 / 2.0
    D["sig2"] = D["a0_ev"] * D["lstar_ev"]           # sigma_c^2 / c^2  = a0 L*
    D["sig_ms"] = math.sqrt(D["sig2"]) * C_LIGHT     # m/s
    D["ct2"] = 1.0 if P["ct_mode"] == "light" else D["sig2"]
    D["eta"] = D["gamma"] / D["ct2"]
    D["mt2"] = K_EV / D["eta"]                       # eV^2
    D["mt_ev"] = math.sqrt(D["mt2"])
    D["lamc_ev"] = 1.0 / D["mt_ev"]                  # eV^-1
    D["lamc_m"] = D["lamc_ev"] * HBARC
    D["lamc_kpc"] = D["lamc_m"] / MPC * 1e3
    D["cs_el2"] = P["eos_factor"] * D["gamma"] * P["rho_c_ev4"]   # c_s,el^2 / c^2
    D["cs_el_ms"] = math.sqrt(D["cs_el2"]) * C_LIGHT
    D["h_lam"] = P["hlam_factor"] * H_LAM_EV         # eV
    D["t_ds_ev"] = D["h_lam"] / (2.0 * math.pi)      # k_B T_dS, in eV
    D["m_p_ev"] = 1.0 / D["lstar_ev"]                # hbar/(c L*), in eV
    D["sig2_th3"] = P["eq_dof"] * D["t_ds_ev"] / D["m_p_ev"]
    D["sig_th3_ms"] = math.sqrt(D["sig2_th3"]) * C_LIGHT
    return D


def apply(P):
    D = derive(P)
    D["P"] = P
    return D


# --------------------------------------------------------------------------
# check machinery
# --------------------------------------------------------------------------
def ck(name, got, want, tol=1e-9, mode="rel", desc=""):
    """Evaluate one check: an expression `got` against an independently
    computed value `want`.  Nothing here is declared true."""
    got = float(got)
    want = float(want)
    if mode == "rel":
        err = abs(got - want) / max(abs(want), 1e-300)
        ok = bool(err <= tol)
    elif mode == "ge":
        err = got - want
        ok = bool(err >= 0.0)
    elif mode == "le":
        err = got - want
        ok = bool(err <= 0.0)
    else:
        err = abs(got - want)
        ok = bool(err <= tol)
    RESULTS.append(dict(name=name, got=got, want=want, err=float(err), tol=tol,
                        mode=mode, ok=ok, desc=desc))
    print(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  got={got:.10e}  "
          f"want={want:.10e}  {mode}-err={err:.2e}  {desc}")
    return ok


def banner(s):
    print("\n" + "=" * 78)
    print(s)
    print("=" * 78)


# --------------------------------------------------------------------------
# TASK 1 -- the equation of state: c_T^2 = gamma/eta from the action,
#           and the medium's thermodynamic sound speed dP/drho
# --------------------------------------------------------------------------
def task1(D):
    banner("TASK 1 -- c_T^2 = gamma/eta from the action vs c_therm^2 = dP/drho")
    out = {}
    eta, gam, Kc = sp.symbols("eta gamma K", positive=True)
    t, x, k, om = sp.symbols("t x k omega", real=True)
    A = sp.symbols("A", positive=True)
    Pf = sp.Function("P")

    # --- (a) the transverse quadratic action: (eta/2)Pdot^2 - (gamma/2)(dP)^2 - (K/2)P^2
    #     (transverse: D.P = 0 kills the alpha term; F_ijF^ij = 2(dP)^2 for D.P = 0)
    Pt = sp.Derivative(Pf(t, x), t)
    Px = sp.Derivative(Pf(t, x), x)
    gam_eff = gam if D["P"]["shear"] else sp.Integer(0)
    Lq = eta / 2 * Pt ** 2 - gam_eff / 2 * Px ** 2 - Kc / 2 * Pf(t, x) ** 2
    EL = (sp.diff(sp.diff(Lq, Pt), t) + sp.diff(sp.diff(Lq, Px), x)
          - sp.diff(Lq, Pf(t, x)))
    EL = sp.simplify(EL)
    print(f"  Euler-Lagrange of the transverse action:  {EL} = 0")
    # plane wave
    ansatz = A * sp.exp(sp.I * (k * x - om * t))
    ELw = EL.subs({Pf(t, x): ansatz})
    ELw = sp.simplify(ELw / ansatz)
    sol = sp.solve(sp.Eq(ELw, 0), om ** 2)
    if isinstance(sol, dict):
        sol = list(sol.values())[0]
    elif isinstance(sol, list) and isinstance(sol[0], dict):
        sol = list(sol[0].values())[0]
    elif isinstance(sol, list):
        sol = sol[0]
    om2_sym = sp.simplify(sol)
    print(f"  dispersion from the action:  omega^2 = {sp.simplify(om2_sym)}")

    num = {eta: 1.7, gam: 0.43, Kc: 2.9, k: 0.61}
    got = float(om2_sym.subs(num))
    want = (2.9 + 0.43 * 0.61 ** 2) / 1.7          # closed form (K + gamma k^2)/eta
    ck("K1", got, want, 1e-12, desc="omega^2 from the E-L equation = (K+gamma k^2)/eta")

    # --- (b) the k^2 coefficient is gamma/eta (the light-cone speed)
    ct2_sym = sp.limit(sp.simplify(om2_sym / k ** 2), k, sp.oo)
    print(f"  lim omega^2/k^2 = {ct2_sym}")
    got = float(ct2_sym.subs(num))
    ck("K2", got, 0.43 / 1.7, 1e-12,
       desc="c_T^2 = lim omega^2/k^2 = gamma/eta (symbolic limit vs ratio)")

    # --- (c) the gap: omega^2(0) = K/eta, and W''(0) = K from the potential
    gap = float(sp.simplify(om2_sym).subs({**num, k: 0}))
    ck("K3", gap, 2.9 / 1.7, 1e-12, desc="mass gap omega^2(0) = K/eta")
    u, a0s = sp.symbols("u a0", positive=True)
    W = a0s ** 2 / Kc * (-u / a0s - sp.log(1 - u / a0s))
    ser = sp.series(W, u, 0, 3).removeO()
    coeff_u2 = sp.simplify(ser.coeff(u, 2))
    print(f"  W(u) = ... + ({coeff_u2}) u^2 + ...   with u = K|P|  =>  mass term K/2 per component")
    # mass term in P: (1/2) * (2 coeff_u2 K^2) P^2  = coeff_u2*K^2 P^2 ; W''(P)=2 coeff_u2 K^2
    m2_from_W = sp.simplify(2 * coeff_u2 * Kc ** 2)
    num2 = {Kc: 2.9}
    ck("K4", float(m2_from_W.subs(num2)), 2.9, 1e-12,
       desc="d^2W/dP^2|_0 = K, so the gap is K/eta (W series vs K)")

    # --- (d) c_T^2 from a finite-difference slope of omega^2(k), not from the limit
    ks = [50.0, 51.0]
    w2 = [float(sp.simplify(om2_sym).subs({**num, k: q})) for q in ks]
    slope = (w2[1] - w2[0]) / (ks[1] ** 2 - ks[0] ** 2)
    ck("K5", slope, 0.43 / 1.7, 1e-9,
       desc="c_T^2 from the finite-difference slope of omega^2(k) at large k")

    # --- (e) the EOS of the cold sector (A16): p = rho de/drho - e, c_s^2 = dp/drho = gamma rho
    rho, rbar, g2 = sp.symbols("rho rhobar gamma", positive=True)
    e = g2 * D["P"]["eos_factor"] / 2 * (rho - rbar) ** 2
    p = sp.simplify(rho * sp.diff(e, rho) - e)
    cs2 = sp.simplify(sp.diff(p, rho))
    print(f"  Gamma = 2 EOS: e = (gamma/2)(rho-rhobar)^2, p = {p}, dp/drho = {cs2}")
    ck("K6", float(cs2.subs({g2: 1.0, rho: 1.0})), 1.0, 1e-15,
       desc="sympy: dp/drho = gamma rho  (the Gamma = 2 polytrope)")
    ck("K7", D["cs_el2"] * C_LIGHT ** 2, CS2_EL_A16, 1e-3,
       desc="gamma rho_c = 0.519081 m^2/s^2 (A16 K8)")
    ck("K8", D["cs_el_ms"], CS_EL_A16, 1e-3,
       desc="elastic sound speed = 0.720473 m/s (A16 K8)")

    # --- (f) c_T^2 / c_s,el^2 = 1/(eta rho_c) identically
    lhs = D["ct2"] / D["cs_el2"]
    rhs = 1.0 / (D["eta"] * D["P"]["rho_c_ev4"])
    ck("K9", lhs, rhs, 1e-12,
       desc="c_T^2/c_s,el^2 = 1/(eta rho_c): the two speeds differ by eta*rho_c")

    # --- (g) the hydrodynamic matching eta = 1/rho_c makes them equal
    Dhyd = apply({**D["P"]})
    ct2_hyd = Dhyd["gamma"] * Dhyd["P"]["rho_c_ev4"]      # gamma / (1/rho_c)
    ck("K10", ct2_hyd, D["cs_el2"], 1e-15,
       desc="eta = 1/rho_c (the only dimensionally available inertia) => c_T = c_s,el")

    # --- (h) the closure's eta*rho_c, i.e. how far from hydrodynamic it is
    ck("K11", D["eta"] * D["P"]["rho_c_ev4"], D["cs_el2"] / D["ct2"], 1e-12,
       desc="closure's eta rho_c = c_s,el^2/c_T^2 = 7.48e-9 (not 1)")

    # --- (i) equipartition: the exact factors
    ratio3 = D["sig2_th3"] / D["sig2"]
    closed3 = 3.0 * math.sqrt(32.0 * math.pi / 3.0) / (2.0 * math.pi)
    print(f"  m_P/T_dS = {D['m_p_ev']/D['t_ds_ev']:.6e};  "
          f"3 k_BT/(m_P a0 L*) = {ratio3:.6f};  closed form {closed3:.6f}")
    ck("K12", ratio3, closed3, 1e-4,
       desc="3 k_B T_dS/(m_P sigma_c^2) = 3 sqrt(32pi/3)/(2pi) = 2.76395")
    ratio1 = (D["t_ds_ev"] / D["m_p_ev"]) / D["sig2"]
    closed1 = math.sqrt(32.0 * math.pi / 3.0) / (2.0 * math.pi)
    ck("K13", ratio1, closed1, 1e-4,
       desc="k_B T_dS/(m_P sigma_c^2) = sqrt(32pi/3)/(2pi) = 0.92116 (per-dof)")
    a0_th_si = (D["h_lam"] / (2.0 * math.pi)) / D["a0_ev"] * D["P"]["a0_si"]
    print(f"  a0 from the thermal wavelength cH_L/2pi = {a0_th_si:.6e} m/s^2 "
          f"(declared thermal footing {A0_TH_SI:.6e})")
    ck("K14", a0_th_si, A0_TH_SI, 2e-3,
       desc="cH_L/2pi reproduces the declared thermal footing 8.620e-11")

    # --- (j) the a0 (and kappa) implied by the stated 3-dof equipartition
    dof = D["P"]["eq_dof"]
    a0_impl_si = dof * D["h_lam"] / (2.0 * math.pi) / D["a0_ev"] * D["P"]["a0_si"]
    print(f"  a0 implied by {dof}-dof equipartition: {a0_impl_si:.6e} m/s^2 "
          f"(= {dof} cH_L/2pi), kappa = {a0_impl_si/A0_PER_KAPPA:.6f}")
    ck("K15", a0_impl_si, dof * A0_TH_SI, 2e-3,
       desc="dof-dof equipartition implies a0 = dof*cH_L/2pi = 2.587e-10 m/s^2 (dof=3)")
    kappa_impl = a0_impl_si / A0_PER_KAPPA
    tension = (kappa_impl - KAPPA_MEAS) / KAPPA_SIG
    print(f"  that a0 gives kappa = {kappa_impl:.6f} (a0 per kappa = {A0_PER_KAPPA:.4e}), i.e. "
          f"{tension:.2f} sigma from A51's {KAPPA_MEAS}+-{KAPPA_SIG}")
    print("  A69 O16 (cited): Delta N_eff = 0.5933 for two thermalized bosonic modes vs Planck < 0.34")
    ck("K16", tension, 6.49, 5e-3,
       desc="the 3-dof version is 6.49 sigma from A51's kappa")

    # --- (k) Boltzmann suppression: m_P/T_dS
    mT = D["m_p_ev"] / D["t_ds_ev"]
    ck("K17", mT, 2.0 * math.pi / (D["h_lam"] * D["lstar_ev"]), 1e-10,
       desc="m_P/T_dS = 2pi/(H_L L*) = 1.408e9: the P particle is far above T_dS")
    L_eq_pc = (2.0 * math.pi / D["h_lam"]) * HBARC / PC
    ck("K18", L_eq_pc, (1.0 / D["t_ds_ev"]) * HBARC / PC, 1e-10,
       desc="L* at which m_P = T_dS: 2pi/H_L = 3.377e10 pc = 33.77 Gpc")
    print(f"  occupation e^(-m_P/T_dS) = {math.exp(-mT):.3e}   "
          f"(exp underflows; L*_eq/L* = {L_eq_pc/D['P']['lstar_pc']:.4e})")

    # --- (l) the O(1) band of the identification c_T^2 = coeff * sigma_c^2
    band = {}
    for coeff in (1.0 / 3.0, 5.0 / 9.0, 1.0):
        ct2b = coeff * D["sig2"]
        etab = D["gamma"] / ct2b
        lamc = math.sqrt(etab / K_EV) * HBARC / MPC * 1e3
        band[f"{coeff:.6f}"] = dict(ct_ms=math.sqrt(ct2b) * C_LIGHT / 1e3,
                                    ct2=ct2b, lamc_kpc=lamc)
        print(f"  c_T^2/sigma^2 = {coeff:.6f}: c_T = {math.sqrt(ct2b)*C_LIGHT/1e3:.4f} km/s, "
              f"gamma/eta = {ct2b:.6e}, lambda_C = {lamc:.4f} kpc")
    print(f"  the O(1) band spans lambda_C(1/3)/lambda_C(1) = "
          f"{band[f'{1.0/3.0:.6f}']['lamc_kpc']/band[f'{1.0:.6f}']['lamc_kpc']:.6f} = sqrt(3)")

    # K41 (lambda_C(1/3)/lambda_C(1) = sqrt3) deleted: a ratio of two sigma_c-scaled lengths, invariant
    # under every dial; the band itself is printed above.
    out.update(dict(dispersion=str(sp.simplify(om2_sym)), ct2_ct=float(ct2_sym.subs(num)),
                    band=band,
                    cs_el2=D["cs_el2"], cs_el_ms=D["cs_el_ms"],
                    ratio_3dof=ratio3, ratio_perdof=ratio1, a0_impl_si=a0_impl_si,
                    kappa_impl=kappa_impl, tension_sigma=tension,
                    mP_over_TdS=mT, L_eq_pc=L_eq_pc,
                    eta_rho_c=D["eta"] * D["P"]["rho_c_ev4"],
                    ct2_hydro=ct2_hyd, ratio_etarho_closure=lhs))
    return out


# --------------------------------------------------------------------------
# TASK 2 -- the closure's numbers and the data
# --------------------------------------------------------------------------
def Ez(a):
    return math.sqrt(OM_M * a ** -3 + OM_L)


def growth(cs2, k_hMpc, a_i=1e-3, n=2600, pressure=True):
    """Linear growth of a dark fluid with sound speed squared cs2 (units c^2)."""
    k = k_hMpc * H0_HUB / MPC
    la = np.linspace(math.log(a_i), 0.0, n)

    def rhs(lna, y):
        a = math.exp(lna)
        d, dp = y
        e = Ez(a)
        dlnH = -1.5 * OM_M * a ** -3 / e ** 2
        pres = 0.0 if not pressure else cs2 * (k * C_LIGHT) ** 2 / (a ** 2 * (H0_SI * e) ** 2)
        return np.array([dp, -(2.0 + dlnH) * dp
                         + (1.5 * OM_M * a ** -3 / e ** 2 - pres) * d])

    y = np.array([a_i, a_i])
    for i in range(n - 1):
        hh = la[i + 1] - la[i]
        k1 = rhs(la[i], y)
        k2 = rhs(la[i] + hh / 2, y + hh / 2 * k1)
        k3 = rhs(la[i] + hh / 2, y + hh / 2 * k2)
        k4 = rhs(la[i] + hh, y + hh * k3)
        y = y + hh / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        if not np.isfinite(y[0]):
            return float("nan")
    return float(y[0])


def growth_ivp(cs2, k_hMpc, a_i=1e-3, pressure=True):
    """The same ODE, integrated with an adaptive DOP853 (independent route)."""
    from scipy.integrate import solve_ivp
    k = k_hMpc * H0_HUB / MPC

    def rhs(lna, y):
        a = math.exp(lna)
        d, dp = y
        e = Ez(a)
        dlnH = -1.5 * OM_M * a ** -3 / e ** 2
        pres = 0.0 if not pressure else cs2 * (k * C_LIGHT) ** 2 / (a ** 2 * (H0_SI * e) ** 2)
        return [dp, -(2.0 + dlnH) * dp + (1.5 * OM_M * a ** -3 / e ** 2 - pres) * d]

    s = solve_ivp(rhs, [math.log(a_i), 0.0], [a_i, a_i], method="DOP853",
                  rtol=1e-11, atol=1e-14, dense_output=False)
    return float(s.y[0, -1])


def trapz(y, x):
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))


def growth_exact():
    a = np.linspace(1e-6, 1.0, 400000)
    f = 1.0 / (a * np.array([Ez(q) for q in a])) ** 3
    return 2.5 * OM_M * Ez(1.0) * trapz(f, a)


def jeans(cs_ms, rho_kg):
    kJ = math.sqrt(4.0 * math.pi * G_SI * rho_kg) / cs_ms
    lJ = 2.0 * math.pi / kJ
    MJ = 4.0 * math.pi / 3.0 * rho_kg * (lJ / 2.0) ** 3
    return kJ, lJ, MJ


def task2(D):
    banner("TASK 2 -- the closure's numbers against the data")
    out = {}
    print(f"  sigma_c = {D['sig_ms']:.6e} m/s ; (sigma_c/c)^2 = {D['sig2']:.10e}")
    ck("K19", D["sig2"], (8.33e3 / C_LIGHT) ** 2, 2e-3,
       desc="(sigma_c/c)^2 from a0L* = 7.7125e-10, vs 7.7206e-10 from 8.33 km/s")
    ck("K20", D["eta"], K_EV / D["mt2"], 1e-12,
       desc="eta = gamma/c_T^2 = K/m_T^2 (two routes)")
    ck("K21", D["lamc_m"] / MPC * 1e3, D["P"]["lstar_pc"] * PC / HBARC * HBARC /
       (math.sqrt(2.0) * math.sqrt(D["ct2"])) / MPC * 1e3, 1e-12,
       desc="lambda_C = sqrt(eta/K) = L*/(sqrt2 c_T) (611.1 kpc)")
    ck("K22", D["lamc_kpc"], LAMC_TASK_KPC, 1e-2,
       desc="lambda_C = 611 kpc (the closure's 612 kpc, 0.2 %)")
    # K23 (m_T/H0, a pure unit conversion) deleted: no dial can break it; the number is in HEADLINE.
    margin_ct = BOUND_A69 / D["ct2"]
    margin_eta = D["eta"] / (D["gamma"] / BOUND_A69)
    ck("K24", margin_ct, margin_eta, 1e-12,
       desc="the closure sits 248x below A69's bound, in c_T^2 and in eta")
    print(f"  eta = {D['eta']:.4f} eV^-4 ; m_T = {D['mt_ev']:.6e} eV ; "
          f"lambda_C = {D['lamc_kpc']:.4f} kpc ; eta*rho_c = "
          f"{D['eta']*D['P']['rho_c_ev4']:.4e}")

    # growth
    D0 = growth(0.0, 0.2, pressure=D["P"]["pressure"])
    ck("K25", D0, growth_exact(), 1e-8,
       desc="c_s = 0 growth = the exact LCDM growth function (ODE vs integral)")
    s17 = growth(1e-7, 0.2, pressure=D["P"]["pressure"])
    ck("K26", s17 / D0, S_A69_1E7, 5e-5,
       desc="S(k=0.2) at c_s^2 = 1e-7 reproduces A69's table (0.9737)")
    s02 = growth(D["ct2"], 0.2, pressure=D["P"]["pressure"]) / D0
    s02b = growth_ivp(D["ct2"], 0.2, pressure=D["P"]["pressure"]) / growth_ivp(
        0.0, 0.2, pressure=D["P"]["pressure"])
    ck("K27", s02, s02b, 1e-8,
       desc="S(k=0.2) at c_T = sigma_c: fixed-step RK4 vs adaptive DOP853")
    s05 = growth(D["ct2"], 0.5, pressure=D["P"]["pressure"]) / D0
    denom = 1.0 - s02
    k2_ratio = (1.0 - s05) / denom if denom != 0.0 else float("nan")
    ck("K28", k2_ratio, (0.5 / 0.2) ** 2, 1e-2,
       desc="1-S ~ k^2: (1-S(0.5))/(1-S(0.2)) = 6.25")
    sl = growth(D["ct2"], 3.0, pressure=D["P"]["pressure"]) / D0
    s5 = growth(D["ct2"], 5.0, pressure=D["P"]["pressure"]) / D0
    s10 = growth(D["ct2"], 10.0, pressure=D["P"]["pressure"]) / D0
    # half mode
    lo, hi = 0.5, 40.0
    for _ in range(30):
        mid = math.sqrt(lo * hi)
        if growth(D["ct2"], mid, pressure=D["P"]["pressure"]) / D0 > 0.5:
            lo = mid
        else:
            hi = mid
    k_half = 0.5 * (lo + hi)
    print(f"  growth: S(0.2)={s02:.6f}  S(0.5)={s05:.6f}  S(3)={sl:.4f}  "
          f"S(5)={s5:.4f}  S(10)={s10:.4f}  k_1/2={k_half:.4f} h/Mpc")
    ck("K29", 1.0 / k_half, 0.0896, 2e-2,
       desc="half-mode 1/k_1/2 = 0.090 h^-1 Mpc (k_1/2 = 11.2 h/Mpc)")
    sc = growth(1.0, 0.2, pressure=D["P"]["pressure"]) / D0
    print(f"  contrast: at eta = gamma (c_T = c) S(0.2) = {sc:.3e}")

    # Jeans with c_T
    kJ, lJ, MJ = jeans(D["sig_ms"], D["P"]["rho_c_kg"])
    kJ2, lJ2, MJ2 = jeans(D["sig_ms"], 200.0 * D["P"]["rho_c_kg"])
    ck("K30", lJ / MPC, D["sig_ms"] * math.sqrt(math.pi / (G_SI * D["P"]["rho_c_kg"])) / MPC, 1e-12,
       desc="lambda_J = 2pi c_T/sqrt(4pi G rho) = 1.2323 Mpc")
    ck("K31", MJ / MSUN_KG, math.pi * lJ ** 3 * D["P"]["rho_c_kg"] / 6.0 / MSUN_KG, 1e-12,
       desc="M_J = (4pi/3)rho(lambda/2)^3 = pi lambda^3 rho/6 = 3.266e10 Msun")
    print(f"  c_T Jeans: lambda_J = {lJ/MPC:.6f} Mpc, M_J = {MJ/MSUN_KG:.4e} Msun "
          f"(at 200 rho_c: {lJ2/MPC*1e3:.2f} kpc, {MJ2/MSUN_KG:.4e} Msun)")

    # lambda_C against the record's measured scales
    ratios = {k: D["lamc_kpc"] / (v * 1e3) for k, v in
              dict(r_sp=R_SP_MPC, u_half=U_HALF_MPC, r_v=R_V_MPC, r200c=R200C_MPC).items()}
    print("  external scales (record): r_sp=1.414 Mpc (A29), u=1/2 crossing 1.065 Mpc (A29), "
          "r_v=1.6863 Mpc (A18), r200c = r_sp/1.367 = 1.0344 Mpc (A29 eq. 5)")
    print("  A18 shape channel (cited): MID/OUTER = 0.966+-0.102 (native) vs 1.888+-0.203 (phantom), "
          "f_band = 0.8122")
    print("  lambda_C / measured scale:  " + "  ".join(f"{k}={v:.4f}" for k, v in ratios.items()))
    dev = min(abs(v - 1.0) for v in ratios.values())
    ck("K32", dev, 0.30, mode="ge",
       desc="no measured cluster scale sits at lambda_C (min |ratio-1| >= 0.30)")
    ck("K32b", D["ct2"], BOUND_A69, mode="le",
       desc="the closure is allowed by A69's bound (gamma/eta < 1.916e-07)")
    ck("K33", D["lamc_kpc"] / 82.3502, 7.42, 5e-3,
       desc="lambda_C / lambda_FS(sigma_c) = 7.42 (A16's 82.35 kpc)")

    out.update(dict(sigma_c_ms=D["sig_ms"], ct2=D["ct2"], eta=D["eta"], mt_ev=D["mt_ev"],
                    lamc_kpc=D["lamc_kpc"], margin_bound=margin_ct,
                    S_02=s02, S_05=s05, S_3=sl, S_5=s5, S_10=s10, k_half=k_half,
                    lam_half=1.0 / k_half, S_at_c=sc,
                    lamJ_ct_Mpc=lJ / MPC, MJ_ct=MJ / MSUN_KG,
                    lamJ_ct_200_Mpc=lJ2 / MPC, MJ_ct_200=MJ2 / MSUN_KG,
                    scale_ratios=ratios, min_scale_dev=dev))
    return out


# --------------------------------------------------------------------------
# TASK 3 -- the other direction: the elastic pressure
# --------------------------------------------------------------------------
def task3(D):
    banner("TASK 3 -- the medium's ACTUAL pressure is elastic (A16): which speed governs?")
    out = {}
    # elastic Jeans: k_J from c_s,el^2 k^2 = 4 pi G rho, closed form sqrt2/L*
    kJ_el = math.sqrt(4.0 * math.pi * G_SI * D["P"]["rho_c_kg"]) / D["cs_el_ms"]
    # numerical root of the same dispersion, independent of the closed form
    from scipy.optimize import brentq
    f = lambda kk: D["cs_el2"] * kk ** 2 - 4.0 * math.pi * G_SI * D["P"]["rho_c_kg"] / C_LIGHT ** 2
    kJ_num = brentq(f, 1e-22, 1e-16, xtol=1e-30, rtol=8.9e-16)
    ck("K34", kJ_el / kJ_num, 1.0, 1e-9,
       desc="elastic k_J: closed form vs numerical root of the dispersion")
    lJ_el = 2.0 * math.pi / kJ_el
    ck("K35", lJ_el / PC, math.sqrt(2.0) * math.pi * D["P"]["lstar_pc"], 3e-3,
       desc="elastic lambda_J = sqrt2 pi L* = 106.62 pc (density-free)")
    MJ_el = 4.0 * math.pi / 3.0 * D["P"]["rho_c_kg"] * (lJ_el / 2.0) ** 3
    ck("K36", MJ_el / MSUN_KG, MJ_EL_A16, 5e-3,
       desc="elastic M_J at the cosmic mean = 0.0212 Msun (A16)")
    # density independence
    cs_el_2x = D["cs_el_ms"] * math.sqrt(200.0)      # c_s^2 = gamma rho scales with rho
    kJ_el2 = math.sqrt(4.0 * math.pi * G_SI * 200.0 * D["P"]["rho_c_kg"]) / cs_el_2x
    ck("K37", kJ_el2 / kJ_el, 1.0, 1e-12,
       desc="dln(lambda_J,el)/dln(rho) = 0: 200x in density, same length")
    kJ_ct2 = math.sqrt(4.0 * math.pi * G_SI * 200.0 * D["P"]["rho_c_kg"]) / D["sig_ms"]
    ck("K38", kJ_ct2 / (math.sqrt(4.0 * math.pi * G_SI * D["P"]["rho_c_kg"]) / D["sig_ms"]),
       math.sqrt(200.0), 1e-12,
       desc="the c_T Jeans length does scale: 200x density -> sqrt(200)")
    # the pressure ratio: what a velocity dispersion would do to the pressure
    pr = D["sig2"] / D["cs_el2"]
    ck("K39", pr, (D["sig_ms"] / D["cs_el_ms"]) ** 2, 1e-12,
       desc="rho sigma_c^2 / p_el = (sigma_c/c_s,el)^2 = 1.336e8")
    # and the T that the elastic speed corresponds to, in units of T_dS
    T_el = D["cs_el2"] / D["sig2_th3"]
    ck("K40", T_el, (D["cs_el2"] / D["sig2"]) / (D["sig2_th3"] / D["sig2"]), 1e-12,
       desc="T implied by the elastic speed = 2.71e-9 T_dS (a cold solid), two routes")
    print(f"  elastic: lambda_J = {lJ_el/PC:.4f} pc, M_J(rho_c) = {MJ_el/MSUN_KG:.5e} Msun ; "
          f"rho sigma^2/p_el = {pr:.4e}")
    print("  A16 external anchors (cited): r_switch density 4.9609 Msun/pc^3, R_TF = 53.31 pc, "
          "M_J(r_switch) = 5.565e+08 Msun, V_f = 165.2 km/s")
    out.update(dict(kJ_el=kJ_el, lamJ_el_pc=lJ_el / PC, MJ_el=MJ_el / MSUN_KG,
                    pressure_ratio=pr, T_el_over_TdS=T_el))
    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--mutate", default=None)
    args = ap.parse_args()

    mut = args.mutate or os.environ.get("A77_MUTATE")
    P = dict(BASE)
    if mut:
        if mut not in MUTATIONS:
            raise SystemExit(f"unknown mutation {mut!r}; known: {sorted(MUTATIONS)}")
        P.update(MUTATIONS[mut])

    D = apply(P)
    print("A77 -- does the medium's own thermodynamics fix c_T = gamma/eta?")
    print(f"  mutation: {mut}" if mut else "  mutation: none")
    print(f"  a0 = {P['a0_si']:.6e} m/s^2 ({D['a0_ev']:.6e} eV), L* = {P['lstar_pc']} pc "
          f"({D['lstar_ev']:.6e} eV^-1)")
    print(f"  K = 4piG = {K_EV:.10e} eV^-2, gamma = K L*^2/2 = {D['gamma']:.10e} eV^-4")
    print(f"  rho_c = {P['rho_c_ev4']:.6e} eV^4, H_Lambda = {D['h_lam']:.6e} eV, "
          f"T_dS = {D['t_ds_ev']:.6e} eV = {D['t_ds_ev']/KB_EV_K:.4e} K")
    a0_th_now = (D["h_lam"] / (2.0 * math.pi)) / D["a0_ev"] * P["a0_si"]
    print(f"  H0 = {H0_SI*MPC/1e3:.1f} km/s/Mpc (h = {H0_HUB}), Omega_m = {OM_M}, Omega_L = {OM_L}, "
          f"m_P = 1/L* = {D['m_p_ev']:.6e} eV, "
          f"a0_th(computed)/a0_th(declared) = {a0_th_now/A0_TH_SI:.6f}, "
          f"a0_can/a0_th = {A0_CAN_SI/a0_th_now:.6f} (a0_can is "
          f"{A0_CAN_SI/a0_th_now*100-100:.2f} % above the thermal footing)")

    o1 = task1(D)
    o2 = task2(D)
    o3 = task3(D)

    npass = sum(1 for r in RESULTS if r["ok"])
    ntot = len(RESULTS)
    print("\n" + "-" * 78)
    print(f"A77 {'COMPLETE' if npass == ntot else 'INCOMPLETE'}: {npass}/{ntot} checks PASS.")
    if npass != ntot:
        print("  FAILED: " + ", ".join(r["name"] for r in RESULTS if not r["ok"]))
    print("-" * 78)

    # every headline number, so the report quotes only what this script prints
    print("\nHEADLINE NUMBERS")
    print(f"  sigma_c                 = {D['sig_ms']:.6f} m/s = {D['sig_ms']/1e3:.6f} km/s")
    print(f"  (sigma_c/c)^2           = {D['sig2']:.6e}")
    print(f"  c_s,el                  = {D['cs_el_ms']:.6f} m/s, c_s,el^2 = {D['cs_el2']:.6e}")
    print(f"  sigma_c^2 / c_s,el^2    = {D['sig2']/D['cs_el2']:.6e}")
    print(f"  3k_BT_dS/m_P / sigma_c^2= {o1['ratio_3dof']:.6f}  (3-dof equipartition)")
    print(f"  k_BT_dS/m_P / sigma_c^2 = {o1['ratio_perdof']:.6f}  (per-dof)")
    print(f"  sigma_th(3-dof)         = {D['sig_th3_ms']/1e3:.4f} km/s ; per-dof = "
          f"{math.sqrt(D['t_ds_ev']/D['m_p_ev'])*C_LIGHT/1e3:.4f} km/s")
    print(f"  a0 implied by 3-dof     = {o1['a0_impl_si']:.6e} m/s^2, kappa = {o1['kappa_impl']:.6f}")
    print(f"  tension vs A51          = {o1['tension_sigma']:.2f} sigma")
    print(f"  a0 thermal (cH_L/2pi)   = {(D['h_lam']/(2*math.pi))/D['a0_ev']*P['a0_si']:.6e}"
          f"  [declared {A0_TH_SI:.6e}]")
    print(f"  m_P/T_dS                = {o1['mP_over_TdS']:.6e}")
    print(f"  L* at m_P = T_dS        = {o1['L_eq_pc']:.6e} pc "
          f"(= {o1['L_eq_pc']/P['lstar_pc']:.3e} L*)")
    print(f"  eta (closure)           = {D['eta']:.6f} eV^-4 ; eta*rho_c = {o1['eta_rho_c']:.6e}")
    print(f"  eta (eta = 1/rho_c)     = {1.0/P['rho_c_ev4']:.6e} eV^-4")
    print(f"  c_T^2(eta=1/rho_c)      = {o1['ct2_hydro']:.6e} (== c_s,el^2)")
    print(f"  lambda_C                = {D['lamc_kpc']:.4f} kpc = {D['lamc_m']/PC:.6e} pc"
          f" = {D['lamc_kpc']*1e3/P['lstar_pc']:.4e} L*")
    lamc_hyd = math.sqrt((1.0 / P['rho_c_ev4']) / K_EV) * HBARC / MPC / 1e3
    print(f"  lambda_C(eta = 1/rho_c) = {lamc_hyd:.4e} Gpc ; gamma/eta = "
          f"{D['gamma']*P['rho_c_ev4']:.6e} ; ratio to the closure = "
          f"{D['ct2']/D['gamma']/P['rho_c_ev4']:.6e}")
    print(f"  m_T                     = {D['mt_ev']:.6e} eV, m_T/H0 = {o2['mt_ev']/H0_EV:.2f}")
    print(f"  gamma/eta               = {D['ct2']:.6e}, bound {BOUND_A69:.4e}, margin {o2['margin_bound']:.2f}")
    print(f"  S(0.2), S(0.5)          = {o2['S_02']:.6f}, {o2['S_05']:.6f}")
    print(f"  S(3), S(5), S(10)       = {o2['S_3']:.5f}, {o2['S_5']:.5f}, {o2['S_10']:.5f}")
    print(f"  k_1/2, lambda_1/2       = {o2['k_half']:.4f} h/Mpc, {o2['lam_half']:.5f} h^-1 Mpc")
    print(f"  S(0.2) at c_T = c       = {o2['S_at_c']:.3e}")
    print(f"  lambda_J(c_T), M_J(c_T) = {o2['lamJ_ct_Mpc']:.6f} Mpc, {o2['MJ_ct']:.6e} Msun")
    print(f"  at 200 rho_c            = {o2['lamJ_ct_200_Mpc']*1e3:.4f} kpc, {o2['MJ_ct_200']:.6e} Msun")
    print(f"  lambda_J(el), M_J(el)   = {o3['lamJ_el_pc']:.4f} pc, {o3['MJ_el']:.6e} Msun")
    print(f"  rho sigma^2 / p_el      = {o3['pressure_ratio']:.6e} ; c_T/c_s,el = "
          f"{math.sqrt(o3['pressure_ratio']):.4e}")
    print(f"  T_el / T_dS             = {o3['T_el_over_TdS']:.6e}")
    print(f"  lambda_C / scales       = " + ", ".join(f"{k}:{v:.4f}" for k, v in o2["scale_ratios"].items()))
    print(f"  min |lambda_C/scale - 1| = {o2['min_scale_dev']:.4f}")
    print(f"  lambda_C / lambda_FS    = {D['lamc_kpc']/82.3502:.4f}")
    print(f"  sigma_c/c               = {D['sig_ms']/C_LIGHT:.6e} = {D['sig_ms']/C_LIGHT:.4e} c")

    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(dict(mutation=mut, inputs=P, task1=o1, task2=o2, task3=o3,
                           checks=RESULTS, npass=npass, ntot=ntot), fh, indent=1, default=float)
        print(f"\nwrote {args.json_out}")

    return 0 if npass == ntot else 1


if __name__ == "__main__":
    sys.exit(main())
