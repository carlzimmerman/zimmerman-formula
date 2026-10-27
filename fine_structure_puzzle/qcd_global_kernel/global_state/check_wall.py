"""Exact and high-precision audit of a defined conditional wall partition model.

No physical QCD parameters or target values are used. The output is a fresh
caller-specified JSON result; code, contract and receipts are frozen beforehand.
"""
import itertools
import json
import sys
from pathlib import Path

import mpmath as mp
import sympy as sp


def main(output):
    names = []

    def exact(name, expression):
        value = sp.simplify(expression)
        if value != 0:
            raise AssertionError((name, value))
        names.append(name)

    H, u = sp.symbols("H u", positive=True)
    A = sp.Function("A")(u)
    sigma = sp.Function("sigma")(u)
    L = sp.Function("L")(H, u)
    V = 8 * sp.pi**2 / (3 * H**4)
    c3 = 2 * sp.pi**2
    s = c3 * sigma / H**3
    stress = lambda W: -H * sp.diff(W, H) / (4 * V)
    Wtarget = 32 * sp.pi**2 * A / (9 * H**3)
    exact("required_W_normalization", stress(Wtarget) - A * H)
    exact("V_times_AH_gives_three_quarters", stress(V * A * H) - 3 * A * H / 4)
    B = H * sp.diff(L, H) + 3 * s
    q = sp.diff(L, u) - sp.diff(s, u)
    r = sp.exp(L - s)
    p = r / (1 + r)
    f = B / (4 * V)
    fu = (H * sp.diff(L, H, u) + 3 * sp.diff(s, u)) / (4 * V)
    exact("forced_metric_derivative", stress(s - L) - f)
    exact("forced_charge_derivative", sp.diff(f, u) - fu)
    exact("unconditioned_metric_derivative", stress(-sp.log(1 + r)) - p * f)
    exact("population_charge_derivative", sp.diff(p, u) - p * (1 - p) * q)
    exact("unconditioned_charge_derivative", sp.diff(p * f, u) - p * fu - p * (1 - p) * q * f)
    exact("wall_stress_coefficient", 3 * c3 / (4 * V * H**4) - sp.Rational(9, 16))

    # Orthogonal finite-sector implementation: rational weights and their
    # independent derivatives, rather than differentiating exp(L-s) again.
    a, b = sp.symbols("a b", positive=True)
    aH, bH, au, bu, aHu, bHu = sp.symbols("aH bH au bu aHu bHu")
    norm = 1 + a + b
    meanB = H * (aH + bH) / norm
    meanq = (au + bu) / norm
    Bu = [H * (aHu / a - aH * au / a**2), H * (bHu / b - bH * bu / b**2)]
    meanBu = (a * Bu[0] + b * Bu[1]) / norm
    meanBq = H * (aH * au / a + bH * bu / b) / norm
    direct_u = H * ((aHu + bHu) / norm - (aH + bH) * (au + bu) / norm**2)
    exact("two_sector_covariance_completion", direct_u - meanBu - meanBq + meanB * meanq)
    N = sp.Function("N")(H, u)
    exact("radius_dependent_multiplicity", stress(-N * sp.log(1 + r)) - (H * sp.diff(N, H) * sp.log(1 + r) + N * p * B) / (4 * V))
    exact("Poisson_metric_derivative", stress(-r) - r * B / (4 * V))
    exact("Poisson_charge_derivative", sp.diff(r * B, u) - r * (sp.diff(B, u) + q * B))
    g = sp.Function("g")(u)
    exact("radius_independent_degenerate_vacua", stress(-sp.log(g)))

    k, nu, eta, sig = sp.symbols("k nu eta sig", positive=True)
    Lpoly = sp.log(k) + nu * sp.log(H)
    exact("polynomial_prefactor_forced_stress", stress(c3 * sig / H**3 - Lpoly) / H - sp.Rational(9, 16) * sig - nu * H**3 / (4 * (8 * sp.pi**2 / 3)))
    exact("area_entropy_effective_tension", stress(c3 * sig / H**3 - c3 * eta / H**3 - Lpoly) - stress(c3 * (sig - eta) / H**3 - Lpoly))
    slope = sp.symbols("slope", positive=True)
    # Use the literal partition ratio in this independent critical check.
    critical_W = -sp.log(1 + k * sp.exp(-c3 * slope * u / H**3))
    critical_derivative = sp.diff(stress(critical_W) / H, u).subs(u, 0)
    exact("critical_noncommuting_charge_limit", critical_derivative - sp.Rational(9, 16) * slope * k / (1 + k))
    chi = sp.symbols("chi", real=True)
    exact("equatorial_area_stationarity", sp.diff(sp.sin(chi)**3, chi).subs(chi, sp.pi / 2))
    exact("equatorial_area_negative_mode", sp.diff(sp.sin(chi)**3, chi, 2).subs(chi, sp.pi / 2) + 3)

    base = Path(__file__).resolve().parent
    fixture = json.loads((base / "INPUTS.json").read_text())["numerical_fixture"]
    raw_cases = list(itertools.product(fixture["sigma0"], fixture["kappa0"], fixture["nu0"], fixture["h"], fixture["u"]))
    if len(raw_cases) != fixture["cases"]:
        raise AssertionError("case count differs from frozen contract")
    precision_outputs = []
    maxima = {}
    rows = []
    for dps, tolerance in zip(fixture["decimal_precisions"], fixture["relative_tolerances"]):
        mp.mp.dps = dps
        omega = 8 * mp.pi**2 / 3
        c = 2 * mp.pi**2
        errors = []
        values = []
        for s0_raw, k0_raw, nu0, h_raw, u_raw in raw_cases:
            def number(raw):
                parts = str(raw).split("/")
                return mp.mpf(parts[0]) / mp.mpf(parts[1]) if len(parts) == 2 else mp.mpf(raw)

            s0, k0, h, uv = map(number, (s0_raw, k0_raw, h_raw, u_raw))

            def sigma_num(v):
                return s0 * (1 + v + v**2 / 5)

            def logk(x, v):
                return mp.log(k0) + (nu0 + v / 3) * mp.log(x) + v / 5

            def forced_W(x, v):
                return c * sigma_num(v) / x**3 - logk(x, v)

            def vacuum_W(x, v):
                return -mp.log1p(mp.exp(-forced_W(x, v)))

            vol = omega / h**4
            wall_s = c * sigma_num(uv) / h**3
            wall_su = c * s0 * (1 + 2 * uv / 5) / h**3
            prob = mp.exp(-forced_W(h, uv))
            prob /= 1 + prob
            Bn = nu0 + uv / 3 + 3 * wall_s
            fn = Bn / (4 * vol)
            fun = (mp.mpf(1) / 3 + 3 * wall_su) / (4 * vol)
            qn = mp.log(h) / 3 + mp.mpf(1) / 5 - wall_su
            direct = [
                -h * mp.diff(lambda x: forced_W(x, uv), h) / (4 * vol),
                -h * mp.diff(forced_W, (h, uv), (1, 1)) / (4 * vol),
                -h * mp.diff(lambda x: vacuum_W(x, uv), h) / (4 * vol),
                -h * mp.diff(vacuum_W, (h, uv), (1, 1)) / (4 * vol),
            ]
            closed = [fn, fun, prob * fn, prob * fun + prob * (1 - prob) * qn * fn]
            for left, right in zip(direct, closed):
                err = abs(left - right) / max(abs(left), abs(right), mp.mpf("1e-100000"))
                if err >= mp.mpf(tolerance):
                    raise AssertionError(("numerical derivative", dps, raw_cases.index((s0_raw, k0_raw, nu0, h_raw, u_raw)), str(err)))
                errors.append(err)
            values.append(closed)
            if dps == fixture["decimal_precisions"][-1]:
                rows.append({"sigma0": s0_raw, "kappa0": k0_raw, "nu0": nu0, "h": h_raw, "u": u_raw,
                             "log10_wall_probability": mp.nstr(mp.log10(prob), 25),
                             "forced_rho_over_H": mp.nstr(fn / h, 25),
                             "unconditioned_rho_over_H": mp.nstr(prob * fn / h, 25),
                             "unconditioned_charge_rho_over_H": mp.nstr(closed[-1] / h, 25)})
        maxima[str(dps)] = mp.nstr(max(errors), 12)
        precision_outputs.append(values)

    stability = []
    for earlier, later in zip(*precision_outputs):
        for low, high in zip(earlier, later):
            err = abs(low - high) / max(abs(low), abs(high), mp.mpf("1e-100000"))
            if err >= mp.mpf(fixture["precision_stability_relative_tolerance"]):
                raise AssertionError(("precision stability", str(err)))
            stability.append(err)
    result = {
        "status": "completed",
        "outcome": "implementation and finite assertion verified in stated range",
        "exact_check_count": len(names),
        "exact_checks": names,
        "numerical_cases_per_precision": len(raw_cases),
        "derivative_comparisons_per_precision": 4 * len(raw_cases),
        "precisions": fixture["decimal_precisions"],
        "maximum_relative_derivative_errors": maxima,
        "maximum_precision_stability_relative_error": mp.nstr(max(stability), 12),
        "rows": rows,
        "physical_QCD_A_computed": False,
        "alpha_selected": False,
        "universal_result_basis": "analytic positive-tension bound in DERIVATION.md, not the finite grid",
        "residual_risks": ["mpmath derivatives are high precision checks, not interval certificates", "No microscopic wall measure or QCD ensemble is evaluated", "No bound applies across a zero of effective tension without new uniformity input"]
    }
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: val for key, val in result.items() if key not in ("rows", "exact_checks")}, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
