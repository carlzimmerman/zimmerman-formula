#!/usr/bin/env python3
"""DP1 finite implementation checks. Run from repository root; no downloaded data."""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "run_002" / "results.json"
CHECKS = []


def check(name, condition, details):
    CHECKS.append({"name": name, "passed": bool(condition), "details": details})
    if not condition:
        raise AssertionError(name + ": " + str(details))


def law(branch, u):
    u = np.asarray(u)
    if branch == "Q":
        f = np.sqrt(u * (u + 1))
        fp = (2 * u + 1) / (2 * f)
        mu = np.sqrt(u / (u + 1))
    else:
        t = np.sqrt(u)
        d = -np.expm1(-t)
        f = u / d
        fp = (d - 0.5 * t * np.exp(-t)) / d**2
        mu = d
    return f, fp, mu, 1 / fp


def boosted(branch, x, y):
    # Dimensionless harmonic Phi_N=(x²+2y²-3z²)/2 at z=0.
    v = np.array([x, 2 * y])
    b = np.linalg.norm(v)
    return v * float(law(branch, b)[0] / b)


def circulation(branch, side):
    p = 1 / math.sqrt(5)
    low, high = p - side / 2, p + side / 2
    options = {"epsabs": 1e-14, "epsrel": 1e-12}
    edges = [
        quad(lambda x: boosted(branch, x, low)[0], low, high, **options)[0],
        quad(lambda y: boosted(branch, high, y)[1], low, high, **options)[0],
        -quad(lambda x: boosted(branch, x, high)[0], low, high, **options)[0],
        -quad(lambda y: boosted(branch, low, y)[1], low, high, **options)[0],
    ]
    return math.fsum(edges) / side**2


def q_inverse(g):
    return 2 * g**2 / (math.sqrt(1 + 4 * g**2) + 1)


def q_primitive(g):
    return g * math.sqrt(1 + 4 * g**2) / 4 + math.asinh(2 * g) / 8 - g / 2


def inverse_and_primitive(branch, g, a):
    v = g / a
    if branch == "Q":
        return a * q_inverse(v), a*a * q_primitive(v)
    t = brentq(lambda t: t*t / (-math.expm1(-t)) - v, 1e-15,
               max(2, 2*math.sqrt(v)), xtol=1e-14)
    primitive = quad(lambda s: 2*s**3 * float(law("R", s*s)[1]), 0, t,
                     epsabs=1e-13, epsrel=1e-12)[0]
    return a*t*t, a*a*primitive


def local_fields(branch, t, x, y, variable_scale):
    # Smooth manufactured nonspherical/time-dependent solution. Its source is
    # defined from the PDE, not claimed to represent observed or free matter.
    co, si = math.cos(0.7*t), math.sin(0.7*t)
    p = np.array([1.3-0.1*math.sin(x)*math.sin(y)*co,
                  0.8+0.1*math.cos(x)*math.cos(y)*co])
    pt = -0.07*math.cos(x)*math.sin(y)*si
    ptt = -0.049*math.cos(x)*math.sin(y)*co
    hessian = -0.1*co*np.array([[math.cos(x)*math.sin(y), math.sin(x)*math.cos(y)],
                               [math.sin(x)*math.cos(y), math.cos(x)*math.sin(y)]])
    a = 1+0.1*math.sin(0.3*t) if variable_scale else 1
    adot = 0.03*math.cos(0.3*t) if variable_scale else 0
    g = np.linalg.norm(p)
    b, W = inverse_and_primitive(branch, g, a)
    _, _, mu, lp = law(branch, b/a)
    A = mu*np.eye(2)+(lp-mu)*np.outer(p,p)/(g*g)
    rho = float(np.sum(A*hessian)-2*ptt)  # K=2, c=1, 4 pi G=1
    energy = pt*pt+W
    flux = -pt*float(mu)*p
    momentum = -2*pt*p
    stress = float(mu)*np.outer(p,p)+np.eye(2)*(pt*pt-W)
    scale_source = (2*W-g*b)*adot/a
    return {"energy": energy, "flux": flux, "momentum": momentum,
            "stress": stress, "rho": rho, "p": p, "phi_t": pt,
            "scale_source": scale_source}


def balance_residual(branch, variable_scale, step):
    t,x,y=0.6,0.4,0.7
    center=local_fields(branch,t,x,y,variable_scale)
    tp,tm=[local_fields(branch,t+s*step,x,y,variable_scale) for s in [1,-1]]
    xp,xm=[local_fields(branch,t,x+s*step,y,variable_scale) for s in [1,-1]]
    yp,ym=[local_fields(branch,t,x,y+s*step,variable_scale) for s in [1,-1]]
    energy_dt=(tp["energy"]-tm["energy"])/(2*step)
    flux_div=(xp["flux"][0]-xm["flux"][0]+yp["flux"][1]-ym["flux"][1])/(2*step)
    momentum_dt=(tp["momentum"]-tm["momentum"])/(2*step)
    stress_div=(xp["stress"][0]-xm["stress"][0]+yp["stress"][1]-ym["stress"][1])/(2*step)
    e_res=energy_dt+flux_div+center["rho"]*center["phi_t"]-center["scale_source"]
    p_res=momentum_dt+stress_div-center["rho"]*center["p"]
    return {"step":step,"energy_balance_residual":float(e_res),
            "max_momentum_balance_residual":float(np.max(np.abs(p_res))),
            "energy_residual_if_scale_exchange_omitted":float(e_res+center["scale_source"]),
            "required_scale_exchange":float(center["scale_source"])}


def evolve(K, D, steps, cycles=10):
    omega = math.sqrt(D / K)  # c=1, |k|=1.
    duration = cycles * 2 * math.pi / omega
    dt = duration / steps
    theta = math.acos(1 - omega**2 * dt**2 / 2)
    prev, current = 1., math.cos(theta)
    energies = []
    max_error = 0.
    for n in range(steps):
        energy = 0.5 * K * ((current - prev) / dt)**2 + 0.5 * D * prev * current
        energies.append(energy)
        max_error = max(max_error, abs(current - math.cos((n + 1) * omega * dt)))
        prev, current = current, (2 - omega**2 * dt**2) * current - prev
    energies = np.asarray(energies)
    return {"steps": steps, "dt": dt, "omega": omega,
            "duration": duration, "max_continuum_error": max_error,
            "relative_discrete_energy_range": float(np.ptp(energies) / abs(energies.mean()))}


def main():
    grid = np.geomspace(1e-8, 1e8, 1601)
    reports = {}
    normalizations = [9.3619e-11, 1.1279e-10]
    length = 3.085677581491367e19  # one kpc, used only to illustrate units
    for branch in ["Q", "R"]:
        f, fp, mu, lp = law(branch, grid)
        h = 1e-5
        numerical_fp = (law(branch, grid * (1 + h))[0]
                        - law(branch, grid * (1 - h))[0]) / (2 * h * grid)
        derivative_error = float(np.max(np.abs(numerical_fp / fp - 1)))
        check(branch + " independent central derivative", derivative_error < 2e-9,
              {"max_relative_error": derivative_error, "step_fraction": h})
        # Quotient λ_parallel/μ is checked against a separately expressed log slope.
        if branch == "Q":
            speed_ratio = 2 * (grid + 1) / (2 * grid + 1)
            curl_exact = 1 / (5 * math.sqrt(2))
        else:
            t = np.sqrt(grid)
            q = np.zeros_like(t)
            small = t < 700
            q[small] = t[small] / (2 * np.expm1(t[small]))
            speed_ratio = 1 / (1 - q)
            curl_exact = math.exp(-1) / (5 * (-math.expm1(-1))**2)
        check(branch + " positive spatial symbol", bool(np.all(mu > 0) and np.all(lp > 0)),
              {"min_mu": float(mu.min()), "min_lambda_parallel": float(lp.min())})
        # At high u, R's exponentially small difference rounds to zero in binary64.
        check(branch + " logarithmic slope identity", np.max(np.abs(lp / mu - speed_ratio)) < 2e-12,
              {"max_absolute_error": float(np.max(np.abs(lp / mu - speed_ratio)))})
        check(branch + " K=2 and K=8 subluminal grid", bool(np.max(lp) < 2),
              {"grid_max_lambda_parallel": float(lp.max())})
        loops = [{"side": s, "curl_from_circulation": circulation(branch, s)}
                 for s in [0.02, 0.01, 0.005, 0.0025]]
        errors = [abs(row["curl_from_circulation"] - curl_exact) for row in loops]
        check(branch + " shrinking loop curl witness", errors[-1] < 2e-6 and errors[-1] < errors[0] / 50,
              {"analytic_curl": curl_exact, "loops": loops, "absolute_errors": errors})
        fg, _, mg, lg = law(branch, np.array(1.))
        # Oblique perturbation makes both Hessian eigenvalues operational.
        theta = math.pi / 3
        D = float(mg * math.sin(theta)**2 + lg * math.cos(theta)**2)
        waves = {str(K): [evolve(K, D, n) for n in [1000, 2000, 4000]] for K in [2, 8]}
        for K, rows in waves.items():
            err = [r["max_continuum_error"] for r in rows]
            energy_error = max(r["relative_discrete_energy_range"] for r in rows)
            check(branch + " wave convergence K=" + K,
                  err[0] / err[1] > 3.8 and err[1] / err[2] > 3.8 and energy_error < 1e-9,
                  {"max_errors": err, "max_relative_discrete_energy_range": energy_error})
        response_time_ratio = waves["8"][-1]["duration"] / waves["2"][-1]["duration"]
        check(branch + " static degeneracy with distinct dynamics", abs(response_time_ratio - 2) < 1e-14,
              {"time_ratio_K8_over_K2": response_time_ratio, "static_mode_denominator_both": D})
        reports[branch] = {"curl_dimensionless": curl_exact,
            "curl_s_inverse_squared_at_one_kpc": [{"a_m_s2": a, "curl": curl_exact * a / length} for a in normalizations],
            "at_B_equals_a": {"g_over_a": float(fg), "lambda_perp": float(mg),
                "lambda_parallel": float(lg), "Lorentz_radial_speed_over_c": math.sqrt(float(lg / mg)),
                "K2_radial_speed_over_c": math.sqrt(float(lg / 2)),
                "K8_radial_speed_over_c": math.sqrt(float(lg / 8))},
            "grid": {"points": len(grid), "B_over_a_min": float(grid[0]), "B_over_a_max": float(grid[-1]),
                "min_Lorentz_radial_speed_squared_over_c2": float(speed_ratio.min()),
                "max_Lorentz_radial_speed_squared_over_c2": float(speed_ratio.max())},
            "loops": loops, "waves": waves}

    primitive = []
    for g in [0.01, 0.1, 1, 10, 100]:
        numerical, error_estimate = quad(q_inverse, 0, g, epsabs=1e-13, epsrel=2e-13)
        analytic = q_primitive(g)
        rel = abs(numerical - analytic) / numerical
        primitive.append({"g_over_a": g, "analytic_W_over_a2": analytic,
                          "quadrature": numerical, "relative_difference": rel,
                          "quadrature_error_estimate": error_estimate})
    check("Q primitive against inverse quadrature", max(x["relative_difference"] for x in primitive) < 2e-11,
          primitive)

    # This is a numerical search within a declared interval, not a proof of global optimality.
    r_opt = minimize_scalar(lambda t: -float(law("R", t * t)[3]), bounds=(0.01, 30), method="bounded",
                            options={"xatol": 1e-12})
    r_cross = brentq(lambda t: t - 2 * (-math.expm1(-t)), 1, 3, xtol=1e-14)
    check("R K=1 has a supermetric mode", bool(r_opt.success and -r_opt.fun > 1),
          {"numerical_max_lambda": -float(r_opt.fun), "at_t": float(r_opt.x),
           "positive_K1_crossing_t": r_cross, "positive_K1_crossing_B_over_a": r_cross**2})
    # Fixed g derivative with changing a: distinguish prescribed a(t) from a fit.
    a_derivatives = []
    for a in normalizations:
        g = a
        b = a * q_inverse(g / a)
        analytic_b_a = 0.5 * (a / math.sqrt(a*a + 4*g*g) - 1)
        step = a * 1e-5
        numerical_b_a = ((a + step) * q_inverse(g / (a + step))
                         - (a - step) * q_inverse(g / (a - step))) / (2 * step)
        check("Q varying a derivative " + str(a), abs(analytic_b_a - numerical_b_a) < 1e-10,
              {"analytic": analytic_b_a, "finite_difference": numerical_b_a})
        a_derivatives.append({"a": a, "fixed_g": g, "B": b, "partial_B_partial_a": analytic_b_a})
    redshifts = []
    for z in [0, 0.5, 1, 2, 3]:
        E2 = 0.315 * (1 + z)**3 + 0.685
        omega_m = 0.315 * (1 + z)**3 / E2
        redshifts.append({"z": z, "E": math.sqrt(E2), "Omega_m": omega_m,
            "minus_a_dot_over_aH": 1.5 * omega_m,
            "deep_external_injection_over_H_field_spatial_energy": 1.5 * omega_m,
            "a_vacuum_both": normalizations, "a_H_branch_both": [a * math.sqrt(E2) for a in normalizations]})
    balances={}
    for branch in ["Q","R"]:
        for variable in [False,True]:
            key=branch+("_variable_a" if variable else "_constant_a")
            rows=[balance_residual(branch,variable,h) for h in [0.002,0.001,0.0005]]
            balances[key]=rows
            e0,e1=abs(rows[0]["energy_balance_residual"]),abs(rows[-1]["energy_balance_residual"])
            p0,p1=rows[0]["max_momentum_balance_residual"],rows[-1]["max_momentum_balance_residual"]
            check(key+" local energy and momentum balance",e1<2e-8 and p1<2e-8 and e1<e0/10 and p1<p0/10,rows)
            if variable:
                check(key+" omission of scale exchange fails",abs(rows[-1]["energy_residual_if_scale_exchange_omitted"])>1e-3,rows[-1])
    result = {"claim_id": "DP1", "status": "all finite checks passed",
        "arithmetic": "binary64, deterministic; numerical bounds are not interval certified",
        "checks": CHECKS, "branches": reports, "Q_primitive": primitive,
        "R_numerical_K_threshold": {"max_lambda_in_t_0p01_to_30": -float(r_opt.fun),
            "t_at_max": float(r_opt.x), "B_over_a_at_max": float(r_opt.x**2),
            "K1_crossing_t": r_cross, "K1_crossing_B_over_a": r_cross**2,
            "global_analytic_sufficient_K": 2},
        "scale_derivative": a_derivatives, "separate_redshift_branches": redshifts,
        "manufactured_local_conservation_checks":balances,
        "non_claims": ["No nonspherical observational fit", "No relativistic or cosmological completion",
            "No global smooth nonlinear evolution theorem", "No general causality no-go",
            "No global numerical-max certification", "No determination of the kinetic coefficient"]}
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks_passed": len(CHECKS), "R_numerical_K_threshold": result["R_numerical_K_threshold"],
                      "at_B_equals_a": {key: reports[key]["at_B_equals_a"] for key in reports}}, indent=2))


if __name__ == "__main__":
    main()
