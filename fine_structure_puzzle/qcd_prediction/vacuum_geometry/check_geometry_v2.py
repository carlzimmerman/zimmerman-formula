"""Bounded checks of the analytic reductions in REPORT.md; no physical fit."""
import json
from pathlib import Path

import mpmath as mp
import sympy as s


def main():
    x, t, k, r, R = s.symbols("x t k r R", positive=True)
    h = s.coth(x) - 1/x
    numerator = h * (1 - x*x/s.sinh(x)**2)
    primitive = x**3/3 + x - x*x*s.coth(x)
    assert s.simplify(s.diff(primitive, x) - (x*s.coth(x)-1)**2) == 0
    # BPS equation gives r^2 H H' as the integrated gradient-squared norm.
    # Reconstruct the independent radial gradient-squared integrand.
    K = x/s.sinh(x)
    norm_integrand = x*x*s.diff(h, x)**2 + 2*K*K*h*h
    assert s.simplify(s.diff(numerator, x) - norm_integrand) == 0
    den = 1 + 3/x**2 - 3*s.coth(x)/x
    algebraic_measure = (1-t)**2/s.sqrt(1-3*t+3*t*t)
    measure_series = s.series(algebraic_measure, t, 0, 3)
    assert s.diff(algebraic_measure, t).subs(t, 0) == -s.Rational(1, 2)

    # Exact Green kernel: harmonic off its source, unit flux, zero at infinity.
    green = k*(s.coth(k*r)-1)/(4*s.pi)
    radial_laplacian = s.diff(green, r, 2) + 2*k*s.coth(k*r)*s.diff(green, r)
    assert s.simplify(radial_laplacian) == 0
    assert s.simplify(-4*s.pi*s.sinh(k*r)**2/k**2*s.diff(green, r)) == 1
    green_linear = s.limit((green-1/(4*s.pi*r))/k, k, 0, dir="+")
    print("Diagnostic raw SymPy Green limit:", repr(green_linear), flush=True)
    assert green_linear == -1/(4*s.pi)

    area = 4*s.pi*s.sinh(k*R)**2/k**2
    vol = s.pi*(s.sinh(2*k*R)-2*k*R)/k**3
    assert s.simplify(s.diff(vol, R)-area) == 0
    fixed_R_linear = s.limit((area/vol-3/R)/k, k, 0, dir="+")
    assert fixed_R_linear == 0
    # Write the large-radius ratio with y=exp(-2 k R), avoiding assumptions
    # in an asymptotic simplifier: ratio/k = 2(1-y)^2/(1-y^2+2 y log y).
    y = s.symbols("y", positive=True)
    infinite_R_ratio = s.limit(2*(1-y)**2/(1-y*y+2*y*s.log(y)), y, 0, dir="+")
    assert infinite_R_ratio == 2

    q1, q2, q3 = s.symbols("q1 q2 q3")
    charges = [q1, q2, q3]
    quadratic = sum(qi*qj for qi in charges for qj in charges)
    assert s.expand(quadratic - sum(charges)**2) == 0
    assert s.expand(quadratic.subs(q3, -q1-q2)) == 0

    # Orthogonal numerical check: directly integrate BPS norms rather than
    # evaluate the symbolic boundary primitive. The universal statements are
    # proved in REPORT.md; this grid is only a finite implementation check.
    mp.mp.dps = 70
    rows = []
    for z in [1, 2, 5, 10, 30]:
        z = mp.mpf(z)
        def hp(u):
            if abs(u) < mp.mpf("1e-12"):
                return mp.mpf(1)/3 - u*u/15 + 2*u**4/189
            return 1/u**2 - 1/mp.sinh(u)**2
        def hv(u):
            if abs(u) < mp.mpf("1e-12"):
                return u/3-u**3/45+2*u**5/945
            return mp.coth(u)-1/u
        def kval(u):
            return mp.mpf(1) if not u else u/mp.sinh(u)
        nquad = mp.quad(lambda u: u*u*hp(u)**2+2*kval(u)**2*hv(u)**2, [0, z])
        dquad = 3*mp.quad(lambda u: (u*hv(u))**2, [0, z])/z**3
        nexact = hv(z)*(1-z*z/mp.sinh(z)**2)
        dexact = 1+3/z**2-3*mp.coth(z)/z
        assert abs(nquad-nexact) < mp.mpf("1e-55")
        assert abs(dquad-dexact) < mp.mpf("1e-55")
        measure = nquad*nquad/mp.sqrt(dquad)
        rows.append({"x": str(z), "numerator_integral": mp.nstr(nquad, 30),
                     "denominator_integral": mp.nstr(dquad, 30),
                     "measure": mp.nstr(measure, 30),
                     "x_times_measure_minus_one": mp.nstr(z*(measure-1), 30),
                     "max_quadrature_residual": mp.nstr(max(abs(nquad-nexact), abs(dquad-dexact)), 8)})
    result = {
        "assertion_tested": "Exact symbolic identities and five independent BPS quadrature checks",
        "status": "passed", "sympy": s.__version__, "mpmath": mp.__version__,
        "zero_mode_measure_series_t_equals_1_over_x": str(measure_series),
        "green_kernel_linear_coefficient": str(green_linear),
        "area_volume_linear_fixed_radius": str(fixed_R_linear),
        "area_volume_over_kappa_infinite_radius": str(infinite_R_ratio),
        "quadrature_precision_decimal_digits": mp.mp.dps,
        "quadrature_tolerance": "1e-55", "quadrature_rows": rows,
        "non_claims": ["Not a QCD or de Sitter calculation", "No nonzero-mode determinant evaluated",
                       "Quadrature residual is not an interval error bound", "No physical alpha input"]}
    target = Path("fine_structure_puzzle/qcd_prediction/vacuum_geometry/runs/geometry-002/results.json")
    target.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "passed", "result": str(target)}))


if __name__ == "__main__":
    main()
