"""Bounded checks of the independently derived local bulk formulas.

Regenerate only into a fresh runner output directory, passed as argv[1].
This program does not read project reports or fit any physical observable.
"""
import json
import pathlib
import sys
import mpmath as mp
import sympy as s

mp.mp.dps = 60
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
checks = {}
E1, E2, E3, B1, B2, B3 = s.symbols("E1 E2 E3 B1 B2 B3", real=True)
F = s.Matrix([[0, B3, -B2, E1], [-B3, 0, B1, E2],
              [B2, -B1, 0, E3], [-E1, -E2, -E3, 0]])
assert s.expand(s.trace((2*s.I*F)**2) - 8*(E1**2+E2**2+E3**2+B1**2+B2**2+B3**2)) == 0
checks["spin_trace"] = "tr_L(2iF)^2=8(E^2+B^2), exact"

p, m, e, t, r, v, L, n = s.symbols("p m e t r v L n", positive=True)
bubble = s.atan(p/(2*m))/(4*s.pi*p)
assert s.expand(s.series(bubble, p, 0, 4).removeO() - (1/(8*s.pi*m)-p**2/(96*s.pi*m**3))) == 0
magfac = t/s.sinh(t)
assert s.series(magfac, t, 0, 4).removeO() == 1-t**2/6
# The diagonal scalar heat kernel for h=a+E*x factors into a 1D oscillator
# and two free dimensions. This checks electric orbital terms without a
# momentum bubble or integration by parts.
osc = s.sqrt(2*e*t/s.sinh(2*e*t))*s.exp(-m**2*(s.tanh(e*t)/e-t))
osc2 = s.simplify(s.diff(osc, e, 2).limit(e, 0)/2)
assert s.simplify(osc2 - (-t**2/3+m**2*t**3/3)) == 0
checks["local_series"] = {
    "bubble": str(s.series(bubble, p, 0, 4)),
    "magnetic_heat_kernel": str(s.series(magfac, t, 0, 4)),
    "electric_oscillator_E2_factor": str(osc2),
}

numerical = []
tol = mp.mpf("1e-50")
for mass in (mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)):
    for mom in (mp.mpf("0.25"), mp.mpf(1), mp.mpf(3)):
        integral = mp.quad(lambda z: 1/mp.sqrt(mass**2+z*(1-z)*mom**2), [0, 1])/(8*mp.pi)
        formula = mp.atan(mom/(2*mass))/(4*mp.pi*mom)
        err = abs(integral-formula)
        assert err < tol
        numerical.append({"test":"bubble_feynman_parameter", "m":str(mass), "p":str(mom), "absolute_error":mp.nstr(err, 12)})
    i2 = mp.quad(lambda k: k*k/(k*k+mass*mass)**2, [0, 1, mp.inf])/(2*mp.pi**2)
    assert abs(i2-1/(8*mp.pi*mass)) < tol
    orbital_b = mp.quad(lambda z: z**(-mp.mpf("0.5"))*mp.exp(-mass*mass*z), [0, 1, mp.inf])/(6*(4*mp.pi)**mp.mpf("1.5"))
    # Integrable endpoint singularity limits this direct quadrature's accuracy.
    assert abs(orbital_b-1/(48*mp.pi*mass)) < mp.mpf("1e-30")
    numerical.append({"test":"spin_radial_and_magnetic_heat_integrals", "m":str(mass), "spin_I2":mp.nstr(i2, 45), "orbital_B_coefficient":mp.nstr(orbital_b, 45)})
checks["quadrature"] = numerical

kk = []
for x in (mp.mpf(1)/7, mp.mpf(1)/3, mp.mpf("0.5"), mp.mpf("0.8")):
    limit = -mp.digamma(x)-mp.digamma(1-x)-2*mp.euler
    for cutoff in (16, 128, 1024):
        direct = 1/x+mp.fsum(1/(k+x)+1/(k-x)-mp.mpf(2)/k for k in range(1,cutoff+1))
        finite_digamma = mp.digamma(cutoff+1+x)+mp.digamma(cutoff+1-x)-mp.digamma(x)-mp.digamma(1-x)-2*mp.harmonic(cutoff)
        assert abs(direct-finite_digamma) < tol
        remainder = limit-direct
        bound = x*x/(cutoff*cutoff*(1-x*x/(cutoff+1)**2))
        assert remainder > 0 and remainder < bound
        kk.append({"x":mp.nstr(x,30), "N":cutoff, "F":mp.nstr(limit,45), "truncation_remainder":mp.nstr(remainder,15), "proved_tail_bound":mp.nstr(bound,15)})
assert abs(-2*mp.digamma(mp.mpf("0.5"))-2*mp.euler-4*mp.log(2)) < tol
checks["kk_harmonic_subtraction"] = kk

h = v-1/r
static_primitive = -s.Rational(11,6)*(1+n*n)*s.log(h)
assert s.simplify(s.diff(static_primitive,r)+s.Rational(11,6)*(1+n*n)/(r*r*h)) == 0
V3 = h*h/(3*L)-h**3/(3*s.pi)+L*h**4/(12*s.pi**2)
radialV = s.expand(4*s.pi*r*r*V3)
assert radialV.coeff(r,-2) == L/(3*s.pi)
checks["tail_coefficients"] = {
    "Gamma_static_derivative_1overR": str(s.Rational(11,6)*(1+n*n)/v),
    "Gamma_GPY_1overR": str(-L/(3*s.pi)),
    "center_unit_logweight_one_loop_1overR_over_L": str((1-22*s.log(2))/(3*s.pi)),
    "center_unit_numeric_over_L": mp.nstr((1-22*mp.log(2))/(3*mp.pi),40),
}
checks["status"] = "All finite symbolic identities and bounded numerical checks passed. This is not a full determinant or boundary-domain verification."
(out/"checks.json").write_text(json.dumps(checks, indent=2)+"\n")
print(json.dumps({"status":"passed", "bubble_cases":9,"radial_heat_pairs":3,"kk_cases":12,"result":str(out/"checks.json")}))

