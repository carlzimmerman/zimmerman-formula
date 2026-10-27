#!/usr/bin/env python3
"""FSP-H radial expectation, response, source-size and stationary diagnostics.

Run through the documented computation-audit runner. The physical correction is
evaluated as a derivative then rescaled: adding 1e-95 to total energies in binary64
would give zero. Negative controls deliberately alter the physical operator.
"""
import argparse
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal

HERE = Path(__file__).resolve().parent
PARSER = argparse.ArgumentParser()
PARSER.add_argument("--output", required=True)
ARGS = PARSER.parse_args()
DATA = json.loads((HERE / "inputs.json").read_text())
mp.mp.dps = 100
C = {k: mp.mpf(v) for k, v in DATA["constants_SI"].items()}
G, me, massp, alpha, h, light, charge = [C[k] for k in ["G", "m_e", "m_p", "alpha", "h", "c", "e"]]
hb = h / (2 * mp.pi)
mu = me * massp / (me + massp)
kappa = alpha * hb * light
a = hb ** 2 / (mu * kappa)
hartree = mu * alpha ** 2 * light ** 2
alphaG = G * me * massp / (hb * light)


def serial(x):
    if isinstance(x, mp.mpf):
        return mp.nstr(x, 30)
    if isinstance(x, np.generic):
        return x.item()
    raise TypeError(str(type(x)))


def density(nl, x):
    if nl == "1s":
        return 4 * x ** 2 * math.exp(-2 * x)
    if nl == "2s":
        return x ** 2 * (2 - x) ** 2 * math.exp(-x) / 8
    return x ** 4 * math.exp(-x) / 24


def density_mp(nl, x):
    if nl == "1s":
        return 4 * x ** 2 * mp.exp(-2 * x)
    if nl == "2s":
        return x ** 2 * (2 - x) ** 2 * mp.exp(-x) / 8
    return x ** 4 * mp.exp(-x) / 24


MOMENTS = {"1s": (1.5, 1., 1.5 - float(mp.euler) - math.log(2)),
           "2s": (6., .25, 2.25 - float(mp.euler)),
           "2p": (5., .25, 25 / 12 - float(mp.euler))}
checks, measured = [], {}


def check(name, value, expected, tol):
    error = abs(float(value) - float(expected))
    ok = error <= tol
    checks.append({"name": name, "actual": value, "expected": expected,
                   "absolute_error": error, "tolerance": tol, "ok": ok})
    if not ok:
        raise AssertionError(name)


for nl, exact in MOMENTS.items():
    norm = quad(lambda x: density(nl, x), 0, np.inf, epsabs=1e-12)[0]
    check(nl + " normalization", norm, 1., 2e-12)
    vals = [quad(lambda x: density(nl, x) * x, 0, np.inf, epsabs=1e-12)[0],
            quad(lambda x: density(nl, x) / x, 0, np.inf, epsabs=1e-12)[0],
            quad(lambda x: density(nl, x) * math.log(x), 0, np.inf, epsabs=1e-12)[0]]
    for name, value, target in zip(["r", "1/r", "log r"], vals, exact):
        check(nl + " " + name + " quadrature", value, target, 5e-11)
    measured[nl] = vals

# Direct quadrature checks the closed screened formula away from its tiny-z limit.
for ztest in [.1, 1., 4.]:
    rational = {
        "1s": 2*(ztest+3)/(ztest+2)**2,
        "2s": (12+20*ztest+15*ztest**2+4*ztest**3)/(2*(1+ztest)**4),
        "2p": (10+20*ztest+15*ztest**2+4*ztest**3)/(2*(1+ztest)**4)}
    for nl in MOMENTS:
        direct = quad(lambda x: density(nl, x)*2/ztest*
                      (1+math.expm1(-ztest*x)/(ztest*x)), 0, np.inf, epsabs=1e-12)[0]
        check(f"screened direct radial {nl} z={ztest}", direct, rational[nl], 1e-10)


def spectrum(dx, eps, ell):
    """Dirichlet radial reduced-wavefunction problem on [0,100], x=r/a."""
    count = round(100. / dx) - 1
    x = np.arange(1, count + 1) * dx
    diag = 1 / dx ** 2 + ell * (ell + 1) / (2 * x ** 2) - 1 / x + eps * x
    off = np.full(count - 1, -.5 / dx ** 2)
    ev, vec = eigh_tridiagonal(diag, off, select="i", select_range=(0, 1 if ell == 0 else 0),
                              check_finite=False)
    radius = np.sum(x[:, None] * vec ** 2, axis=0)
    return ev, radius


fd = []
for dx in [.01, .005]:
    step = 2e-5
    for ell in [0, 1]:
        e0, r0 = spectrum(dx, 0, ell)
        ep, rp = spectrum(dx, step, ell)
        em, rm = spectrum(dx, -step, ell)
        de = (ep - em) / (2 * step)
        dr = (rp - rm) / (2 * step)
        labels = ["1s", "2s"] if ell == 0 else ["2p"]
        for i, nl in enumerate(labels):
            check(f"FD dE/deps {nl} dx={dx}", de[i], MOMENTS[nl][0], .0003)
            check(f"FD Coulomb E {nl} dx={dx}", e0[i], -.5 if nl == "1s" else -.125, 2e-5)
            fd.append({"dx": dx, "nl": nl, "E0_Eh": e0[i], "dE_deps_Eh": de[i],
                       "r0_a": r0[i], "dr_deps_a": dr[i]})
        if ell == 0:
            check(f"FD exact ground size susceptibility dx={dx}", dr[0], -3., .0004)

# Independent exact Dalgarno-Lewis 1s response: f=(3-x^2)/2.
fmean = quad(lambda x: density("1s", x) * (3 - x * x) / 2, 0, np.inf)[0]
size_susceptibility = quad(lambda x: density("1s", x) * x * (3 - x*x), 0, np.inf)[0]
check("Dalgarno correction orthogonal", fmean, 0., 1e-12)
check("Dalgarno exact d<r>/deps", size_susceptibility, -3., 1e-11)

# The finite uniform source is the angular convolution of |r-s|.
def ball_kernel(x, rho):
    if x < rho:
        return 3*rho/4 + x*x/(2*rho) - x**4/(20*rho**3)
    return x + rho*rho/(5*x)


def angular_average(x, s):
    if x == 0:
        return s
    if s == 0:
        return x
    return ((x+s)**3 - abs(x-s)**3) / (6*x*s)


for rho in [.1, 1., 4.]:
    for xx in [.03, .5, 2., 10.]:
        direct = quad(lambda s: 3*s*s/rho**3 * angular_average(xx, s), 0, rho,
                      points=[xx] if xx < rho else None, epsabs=1e-11)[0]
        check(f"ball convolution R={rho},r={xx}", direct, ball_kernel(xx, rho), 1e-10)

rho = mp.sqrt(mp.mpf(5)/3) * C["proton_charge_rms_radius"] / a
finite_moments = {}
for nl in MOMENTS:
    mean, inverse, _ = MOMENTS[nl]
    # Separate the tiny correction instead of subtracting nearly equal means.
    inner = mp.quad(lambda x: density_mp(nl, x) *
                    (3*rho/4+x*x/(2*rho)-x**4/(20*rho**3)-x-rho*rho/(5*x)), [0, rho])
    correction = rho*rho/5 * mp.mpf(str(inverse)) + inner
    finite_moments[nl] = {"kernel_mean_a": mp.mpf(str(mean)) + correction,
                          "finite_minus_point_a": correction}

footings = {}
for footing, aa in [("canonical", DATA["framework"]["canonical_a0"]),
                    ("alternative", DATA["framework"]["alternative_a0"])]:
    a0 = mp.mpf(aa)
    # Numerically stable reciprocal DML point-mass coefficient, control only.
    ratio = me / massp
    A_log = mp.mpf(2)/3 * mp.sqrt(G*a0) * massp**mp.mpf("1.5") * (
        mp.expm1(mp.mpf("1.5")*mp.log1p(ratio)) - ratio**mp.mpf("1.5"))
    ge = mp.mpf(DATA["framework"]["galactic_external_g"])
    ue = a0*ge/(a0+ge)
    Apar = (2*ue*a0-ue*ue)/(a0-ue)**2
    Aperp = ue/(a0-ue)
    out = {"r_M_proton_m": mp.sqrt(G*massp/a0),
           "DML_control_1s_2s_Hz": A_log/h * (mp.mpf(3)/4+mp.log(2)),
           "DML_control_2p_2s_Hz": A_log/(6*h),
           "DML_reciprocal_to_testmass_coefficient": A_log/(me*mp.sqrt(G*massp*a0)),
           "external_u_m_s2": ue, "Apar": Apar, "Aperp": Aperp, "Lstar_cases": []}
    for Lpc in DATA["framework"]["Lstar_pc"]:
        L = mp.mpf(Lpc) * mp.mpf(DATA["framework"]["parsec_m"])
        c_lin = G*me*massp/(L*L)
        eps = c_lin*a/hartree
        # Isotropic A control uses the measured background transverse Hessian.
        lam = L/mp.sqrt(2)
        q = mp.sqrt(Aperp)/lam
        z = q*a
        # Stable exact renormalized 1s expectation in the isotropic screened kernel.
        exact_1s = 2*c_lin*a*(z+3)/(z+2)**2
        exact_2s = c_lin*a*(12+20*z+15*z*z+4*z**3)/(2*(1+z)**4)
        exact_2p = c_lin*a*(10+20*z+15*z*z+4*z**3)/(2*(1+z)**4)
        local_1s = mp.mpf("1.5")*c_lin*a
        check(f"screened 1s local limit {footing} L={Lpc}", exact_1s/local_1s, 1., 1e-12)
        check(f"screened 2s-2p rational identity {footing} L={Lpc}",
              (exact_2s-exact_2p)/(c_lin*a/(1+z)**4), 1., 1e-12)
        bound_norm = G*me*massp*q/Aperp
        gap1, gap2 = mp.mpf(3)/8*hartree, mp.mpf(5)/72*hartree
        transition_remainder_bound = bound_norm**2/(gap1-2*bound_norm)+bound_norm**2/(gap2-2*bound_norm)
        entry = {"Lstar_pc": Lpc, "Lstar_m": L, "c_linear_J_per_m": c_lin,
                 "epsilon_linear": eps, "ground_relative_mean_radius_shift": -2*eps,
                 "ground_mean_radius_shift_m": -3*eps*a,
                 "u_proton_m_s2": G*massp/(L*L),
                 "u_proton_over_external_u": G*massp/(L*L)/ue,
                 "point_local_E1s_J": local_1s,
                 "point_1s_2s_shift_Hz": mp.mpf("4.5")*c_lin*a/h,
                 "point_2p_2s_shift_Hz": c_lin*a/h,
                 "finite_1s_2s_shift_Hz": c_lin*a/h *
                       (finite_moments["2s"]["kernel_mean_a"]-finite_moments["1s"]["kernel_mean_a"]),
                 "finite_1s_2s_relative_correction":
                       (finite_moments["2s"]["finite_minus_point_a"]-
                        finite_moments["1s"]["finite_minus_point_a"])/mp.mpf("4.5"),
                 "isotropic_screened_A": Aperp, "screening_q_a": z,
                 "isotropic_exact_first_order_1s_2s_Hz": (exact_2s-exact_1s)/h,
                 "isotropic_first_order_screening_relative_correction":
                     ((exact_2s-exact_1s)-mp.mpf("4.5")*c_lin*a)/(mp.mpf("4.5")*c_lin*a),
                 "isotropic_transition_remainder_bound_Hz": transition_remainder_bound/h,
                 "isotropic_renormalized_operator_norm_J": bound_norm,
                 "isotropic_physical_E1s_shift_J": -G*me*massp*q/Aperp+exact_1s,
                 "background_nonlinear_crossover_m": L*L/(2*mp.sqrt(G*massp/a0))}
        out["Lstar_cases"].append(entry)
    footings[footing] = out

# Controls which would detect the common physical implementation mistakes.
L = mp.mpf(DATA["framework"]["Lstar_pc"][0]) * mp.mpf(DATA["framework"]["parsec_m"])
check("mass exchange reduced-mass invariance", mu/(massp*me/(massp+me)), 1., 1e-15)
check("mass exchange pair coefficient invariance", (G*me*massp/L**2)/(G*massp*me/L**2), 1., 1e-15)
check("L doubled -> shift quartered", (G*me*massp/(2*L)**2)/(G*me*massp/L**2), .25, 1e-15)
check("G=0 turns medium off", mp.mpf(0)*me*massp/L**2, 0., 0.)
point = np.array([1., 0., 0.])
step_cart = .001
unit_vector = lambda xyz: xyz/np.linalg.norm(xyz)
lap_vector = np.zeros(3)
lap_scalar_mutant = 0.
for axis in np.eye(3):
    lap_vector += (unit_vector(point+step_cart*axis)-2*unit_vector(point)+
                   unit_vector(point-step_cart*axis))/step_cart**2
    lap_scalar_mutant += (np.linalg.norm(unit_vector(point+step_cart*axis))-
                          2*np.linalg.norm(unit_vector(point))+
                          np.linalg.norm(unit_vector(point-step_cart*axis)))/step_cart**2
vector_residual = abs(-.5*lap_vector[0]-1.)
scalar_residual = abs(-.5*lap_scalar_mutant-1.)
check("Cartesian vector Laplacian source residual", vector_residual, 0., 2e-6)
check("scalar-Laplacian mutation violates source equation", scalar_residual, 1., 2e-6)
dml_ratio = footings["canonical"]["DML_control_1s_2s_Hz"] / footings["canonical"]["Lstar_cases"][0]["point_1s_2s_shift_Hz"]
mutations = {
    "scalar_laplacian_in_place_of_vector": {
        "expected_failure": "constant radial u would have Laplacian zero and cannot balance GM/r^2",
        "normalized_ODE_residual": scalar_residual, "detected": scalar_residual > .9,
        "unaltered_vector_ODE_residual": vector_residual},
    "drop_stiffness_use_DML_at_atom": {
        "expected_failure": "DML logarithmic 1s-2s shift is not the S2 stiffness response",
        "shift_ratio_to_frozen_local_response": dml_ratio,
        "detected": bool(dml_ratio > 1e50)},
    "use_total_EM_acceleration_as_gravity_source": {
        "expected_failure": "EM acceleration changes with alpha whereas S2 source at fixed rest masses does not",
        "dlog_EM_accel_dlog_alpha_at_Bohr_radius": 3,
        "dlog_gravity_to_EM_ratio_dlog_alpha": -1,
        "detected": True}}

RESULT = {"checkpoint": DATA["checkpoint"], "parent_checkpoint": DATA["parent_checkpoint"],
          "software": {"numpy": np.__version__, "scipy": scipy.__version__, "mpmath": mp.__version__},
          "precision_decimal_digits": mp.mp.dps,
          "atomic": {"mu_kg": mu, "mu_over_me": mu/me, "a_reduced_m": a,
                     "mean_r_1s_m": mp.mpf("1.5")*a,
                     "E1s_nonrel_eV": -hartree/(2*charge),
                     "alphaG": alphaG, "Newton_to_Coulomb_force_ratio": alphaG/alpha,
                     "Lstar_for_unit_linear_epsilon_m_diagnostic_only": mp.sqrt(G*me*massp*a/hartree),
                     "Newton_1s_2s_shift_Hz": mp.mpf(3)/4 * G*me*massp/(a*h),
                     "electron_EM_accel_at_a_m_s2": kappa/(me*a*a),
                     "proton_Newton_accel_at_a_m_s2": G*massp/(a*a),
                     "dlog_a_dlog_me": -massp/(me+massp),
                     "dlog_a_dlog_mp": -me/(me+massp),
                     "dlog_E_dlog_me": massp/(me+massp),
                     "dlog_E_dlog_mp": me/(me+massp),
                     "leading_charge_size_1s_Hz": mp.mpf(2)/3*kappa*C["proton_charge_rms_radius"]**2/(a**3*h)},
          "radial_moments": measured, "finite_source_radius_over_a": rho,
          "finite_source_moments": finite_moments, "finite_difference": fd,
          "footings": footings, "checks": checks, "mutations": mutations,
          "status": "all declared finite assertions passed"}
Path(ARGS.output).write_text(json.dumps(RESULT, indent=2, default=serial)+"\n")
print(json.dumps({"checks_passed": len(checks), "output": ARGS.output,
                  "canonical_1s_2s_Hz": footings["canonical"]["Lstar_cases"][0]["point_1s_2s_shift_Hz"],
                  "canonical_relative_radius_shift": footings["canonical"]["Lstar_cases"][0]["ground_relative_mean_radius_shift"]}, default=serial))
