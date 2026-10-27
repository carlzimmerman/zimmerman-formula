#!/usr/bin/env python3
"""Finite controls for the explicitly conditional occupied-landscape route."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.linalg import eigh
from scipy.special import lambertw


ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
OUT = parser.parse_args().output


def close(a, b, tol=2e-9):
    assert abs(a-b) <= tol * max(1.0, abs(a), abs(b)), (a, b)


def pair_checks():
    # Integrate a sphere intersection independently by perpendicular slices.
    intersect = quad(lambda z: math.pi*(1-(z-0.5)**2), -0.5, 0)[0]
    intersect += quad(lambda z: math.pi*(1-(z+0.5)**2), 0, 0.5)[0]
    union = 8*math.pi/3-intersect
    close(intersect, 5*math.pi/12)
    close(union, 9*math.pi/4)
    n = 0.037
    b = union*n
    p = lambda r: 3*b*r*r*math.exp(-b*r**3)
    norm = quad(p, 0, np.inf, epsabs=2e-12)[0]
    intensity = quad(lambda r: 2*math.pi*n*n*r*r*math.exp(-b*r**3),
                     0, np.inf, epsabs=2e-12)[0]
    close(norm, 1)
    close(intensity, 8*n/27)
    return {"sphere_intersection": intersect, "sphere_union": union,
            "pair_pdf_integral": norm, "pair_intensity": intensity,
            "node_fraction_in_pairs": 2*intensity/n}


def pushforward_checks():
    # Exact exponential-barrier diagnostic with variable subsystem d=D*r.
    B, D, xi, J0, npair = 0.003, 0.7, 1.2, 2.1, 0.13
    b = B/xi**3
    A = J0/(D*xi)
    rows = []
    for x in (0.2, 1., 3., 7., 12.):
        delta = A*math.exp(-x)/x
        recovered = float(lambertw(A/delta).real)
        close(recovered, x)
        analytic = 3*npair*D*xi*B*x**4/(delta*(1+x))*math.exp(-B*x**3)
        r = xi*x
        p = 3*b*r*r*math.exp(-b*r**3)
        jac = xi*x/(delta*(1+x))
        direct = npair*(D*r)*p*jac
        close(analytic, direct)
        # Independent centered finite difference of the inverse map.
        eta = 2e-5
        rlo = xi*float(lambertw(A/(delta*(1-eta))).real)
        rhi = xi*float(lambertw(A/(delta*(1+eta))).real)
        numeric_jac = (rlo-rhi)/(2*eta*delta)
        close(numeric_jac, jac, 4e-9)
        rows.append({"x": x, "delta": delta, "weighted_density": analytic,
                     "relative_jacobian_error": abs(numeric_jac/jac-1)})
    # Compare moments using r versus transformed variable x (not a histogram).
    direct_moment = quad(lambda r: npair*D*r*3*b*r*r*math.exp(-b*r**3),
                         0, np.inf)[0]
    x_moment = quad(lambda x: 3*npair*D*xi*B*x**3*math.exp(-B*x**3),
                    0, np.inf)[0]
    close(direct_moment, x_moment)
    # The local logarithmic raw-gap slope is -1-2/x+3 B x^2.
    slopes = [{"x": x, "slope_dlogrho_dlogOmega": -1-2/x+3*B*x*x}
              for x in (5., 10., 20., 40.)]
    return {"parameters": {"B": B, "D": D, "xi": xi, "J0": J0},
            "samples": rows, "weighted_count_moment": direct_moment,
            "raw_gap_slopes": slopes}


def wkb_checks():
    # Units hbar=mu_reduced=G*m*M_b=1; E=-1/2 is FIXED as r increases.
    rows = []
    for r in (12., 20., 50., 100., 200., 500., 1000.):
        edge = (r-math.sqrt(r*r-8*r))/2
        integrand = lambda x: math.sqrt(max(0., 1-2/x-2/(r-x)))
        action, error = quad(integrand, edge, r-edge,
                             epsabs=1e-9, epsrel=1e-11, limit=120)
        rows.append({"r": r, "turning_point": edge, "action": action,
                     "action_over_r": action/r, "quad_error_estimate": error})
    slope = (rows[-1]["action"]-rows[-2]["action"])/500
    assert 0.99 < slope < 1
    return {"fixed_binding_energy": -0.5, "samples": rows,
            "last_secant_slope": slope,
            "non_claim": "Not a numerical full two-center splitting or threshold-level spectrum."}


def lcao_checks():
    rows = []
    for x in (4., 8., 12., 20., 40.):
        overlap = math.exp(-x)*(1+x+x*x/3)
        C = -1/x+math.exp(-2*x)*(1+1/x)
        K = -(1+x)*math.exp(-x)
        H00, H01 = -0.5+C, -0.5*overlap+K
        # Generalized eigenvalue diagonalization is well conditioned here,
        # but direct subtraction loses the exponentially small split at x=40.
        J = (C*overlap-K)/(1-overlap*overlap)
        vals = eigh(np.array([[H00,H01],[H01,H00]]),
                    np.array([[1.,overlap],[overlap,1.]]), eigvals_only=True)
        if x <= 20:
            close((vals[1]-vals[0])/2, J, 2e-14)
        assert J > 0
        asymptotic = (2*x/3)*math.exp(-x)
        rows.append({"r_over_a": x, "overlap": overlap,
                     "J_over_hartree": J, "J_over_leading_LCAO_asymptotic": J/asymptotic})
    assert abs(rows[-1]["J_over_leading_LCAO_asymptotic"]-1) < 0.001
    return {"samples": rows,
            "non_claim": "Exact algebra within two translated 1s orbitals; not an exact two-center spectrum or exact asymptotic prefactor."}


def source_checks():
    m, M, a, r, u = 0.8, 5., 0.4, 3.1, 0.7
    alpha, beta = M/(M+m), m/(M+m)
    mu = m*M/(M+m)
    s = r*u/2
    # Relative-coordinate 1s packet; both baryons recoil for each q fluctuation.
    def source(k):
        Fd = (1+(a*alpha*k/2)**2)**-2
        Fh = (1+(a*beta*k/2)**2)**-2
        x = k*s
        return (m*Fd*math.sin(alpha*x)-M*Fh*math.cos(x)*math.sin(beta*x))/k
    predicted = mu*((1+beta)*s**3/3-a*a*(alpha-beta)*s/2)
    rows = []
    for k in (0.02, 0.01, 0.005, 0.0025):
        value = source(k)
        rows.append({"k": k, "D": value, "D_over_k2": value/k**2,
                     "relative_coefficient_error": abs(value/k**2/predicted-1)})
    assert rows[-1]["relative_coefficient_error"] < 2e-6
    close(m*alpha-M*beta, 0)
    # Check direct sum over scalar and both baryon centers versus compact form.
    k = 0.4
    Fd = (1+(a*alpha*k/2)**2)**-2
    Fh = (1+(a*beta*k/2)**2)**-2
    direct = m*Fd*math.sin(k*alpha*s)/k
    direct += (M/2)*Fh*(math.sin(k*(-beta*s+s))+math.sin(k*(-beta*s-s)))/k
    close(direct, source(k))
    return {"parameters": {"m": m, "host_M": M, "packet_a": a, "r": r, "cos_theta": u},
            "exact_affine_source": m*alpha-M*beta,
            "predicted_k2_coefficient": predicted, "small_k_samples": rows,
            "direct_particle_source": direct, "compact_source": source(k)}


def bath_checks():
    # Natural units. Test full Bogoliubov radial integral and independent angle quadrature.
    gamma, n0, m, g2, rd = 0.3, 0.4, 0.9, 0.6, 1.7
    c = math.sqrt(g2*n0/m)
    coefficient = gamma**2*n0*rd**2/(48*math.pi**2*m*c**7)
    rows = []
    def spectral(E):
        # E_q=sqrt(eps_q*(eps_q+2*g2*n0)); monotone q>0.
        mu = g2*n0
        eps = E*E/(math.sqrt(mu*mu+E*E)+mu)
        q = math.sqrt(2*m*eps)
        deriv = (eps+mu)/E*q/m
        angular = quad(lambda u: math.sin(q*rd*u/2)**2, -1, 1,
                       epsabs=1e-16)[0]
        return gamma**2*n0/(4*math.pi**2)*q*q*(eps/E)*angular/deriv
    for E in (0.01, 0.003, 0.001, 0.0003):
        val = spectral(E)
        rows.append({"E": E, "J": val, "J_over_E5": val/E**5,
                     "relative_low_E_error": abs(val/E**5/coefficient-1)})
    assert rows[-1]["relative_low_E_error"] < 3e-6
    E, T, J = 0.003, 0.11, spectral(0.003)
    nb = 1/math.expm1(E/T)
    down, up = 2*math.pi*J*(nb+1), 2*math.pi*J*nb
    close(up/down, math.exp(-E/T))
    peq = up/(up+down)
    close(peq, 1/(1+math.exp(E/T)))
    return {"parameters": {"gamma": gamma, "n0": n0, "m": m, "g2": g2, "r_D": rd},
            "sound_speed": c, "predicted_E5_coefficient": coefficient,
            "samples": rows, "detailed_balance_up_over_down": up/down,
            "Gibbs_excited_probability": peq,
            "non_claim": "These are conditional bath matrix elements, not a formation or capture calculation."}


def sector_occupation_checks():
    # Exact hard-core two-well Fock states |00>,|10>,|01>,|11>.
    eb, J, beta, muq = -0.7, 0.013, 4.1, -0.71
    N = np.diag([0., 1., 1., 2.])
    P1 = np.diag([0., 1., 1., 0.])
    rows = []
    for V in (-0.04, -0.01, 0., 0.03):
        H = np.diag([0., eb, eb, 2*eb+V])
        H[1, 2] = H[2, 1] = -J
        values, vectors = np.linalg.eigh(H-muq*N)
        weights = np.exp(-beta*values)
        expected_p1 = float(np.sum(weights*np.diag(vectors.T@P1@vectors))/sum(weights))
        z = math.exp(-beta*(eb-muq))
        partition = 1+2*z*math.cosh(beta*J)+z*z*math.exp(-beta*V)
        p1 = 2*z*math.cosh(beta*J)/partition
        close(p1, expected_p1)
        max_p1 = math.cosh(beta*J)/(math.cosh(beta*J)+math.exp(-beta*V/2))
        zstar = math.exp(beta*V/2)
        pstar = 2*zstar*math.cosh(beta*J)/(1+2*zstar*math.cosh(beta*J)+zstar*zstar*math.exp(-beta*V))
        close(max_p1, pstar)
        width = V+2*J
        if width > 0:
            mumid = eb+V/2
            grand = [0., eb-J-mumid, 2*eb+V-2*mumid]
            assert grand[1] < min(grand[0], grand[2])
        else:
            # At N=0/N=2 crossing, N=1 is above both.
            mumid = eb+V/2
            assert eb-J-mumid > 0
        rows.append({"V_LR": V, "f1_partition": p1, "f1_direct_Fock": expected_p1,
                     "max_f1_at_fixed_T": max_p1, "T0_single_sector_mu_window_width": width})
    return {"parameters": {"E_b": eb, "J": J, "beta": beta, "mu_Q": muq},
            "samples": rows,
            "non_claim": "Hard-core projection, pair isolation and a reservoir are assumptions; no scalar capture rate is supplied."}


result = {"assertion_tested": "Finite checks of mutual-Poisson pair intensity, variable-dipole pushforward, fixed-level Coulomb WKB action and two-1s LCAO splitting, complete host recoil source, contact-phonon E^5/detailed balance, and hard-core sector occupations.",
          "versions": {"numpy": np.__version__, "scipy": scipy.__version__},
          "pairs": pair_checks(), "pushforward": pushforward_checks(),
          "fixed_level_wkb": wkb_checks(), "two_center_LCAO": lcao_checks(),
          "physical_source": source_checks(),
          "contact_bath": bath_checks(), "hard_core_occupation": sector_occupation_checks(),
          "all_assertions_passed": True}
OUT.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"all_assertions_passed": True,
                  "output": str(OUT), "pair_node_fraction": result["pairs"]["node_fraction_in_pairs"],
                  "wkb_last_secant_slope": result["fixed_level_wkb"]["last_secant_slope"],
                  "source_k2_relative_error": result["physical_source"]["small_k_samples"][-1]["relative_coefficient_error"],
                  "bath_E5_relative_error": result["contact_bath"]["samples"][-1]["relative_low_E_error"]}))
