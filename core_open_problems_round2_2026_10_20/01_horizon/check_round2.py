#!/usr/bin/env python3
"""Standalone finite checks for raw_derivation.md; no repository imports.

Usage: python3 check_round2.py /tmp/horizon-round2-results.json
Dependencies: sympy==1.14.0, mpmath==1.3.0; Python >=3.9.
All dimensional test parameters are expressed in a single consistent set of
dimensionless units. No numerical value here is an empirical prediction.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path

import mpmath as mp
import sympy as sp

mp.mp.dps = 60
checks = []
tables = {}


def check(name, condition, detail=None):
    row = {"name": name, "passed": bool(condition)}
    if detail is not None:
        row["detail"] = detail
    checks.append(row)
    if not condition:
        raise AssertionError(name + (": " + str(detail) if detail else ""))


def close(name, actual, expected, tol=mp.mpf("1e-42")):
    error = abs(actual - expected) / max(abs(expected), mp.mpf("1e-50"))
    check(name, error < tol, {"relative_error": mp.nstr(error, 12),
                             "tolerance": str(tol)})


def number(x):
    return mp.nstr(x, 25)


def exact(name, expression):
    check(name, sp.simplify(expression) == 0, str(sp.simplify(expression)))


# 1. Symbolic spectral subtraction; independent convergent dispersion integral.
w, a = sp.symbols("omega alpha", positive=True)
rate = w / (2 * sp.pi * (sp.exp(2 * sp.pi * w / a) - 1))
rate_minus = rate.subs(w, -w)
exact("spectral_commutator", rate_minus - rate - w / (2 * sp.pi))
thermal_sum = w / (4 * sp.pi) * ((sp.exp(2 * sp.pi * w / a) + 1)
                                / (sp.exp(2 * sp.pi * w / a) - 1))
exact("symmetric_noise", (rate_minus + rate) / 2 - thermal_sum)


def F(omega, alpha):
    if not omega:
        return alpha / (4 * mp.pi ** 2)
    return omega / (2 * mp.pi * mp.expm1(2 * mp.pi * omega / alpha))


def rho(omega, alpha):
    return F(-omega, alpha) - F(omega, alpha)


alphas = list(map(mp.mpf, ["0.2", "1", "5"]))
omegas = list(map(mp.mpf, ["0.03", "0.4", "2"]))
spectra = []
for alpha in alphas:
    for omega in omegas:
        spectral = rho(omega, alpha)
        noise = (F(-omega, alpha) + F(omega, alpha)) / 2
        close("commutator_numeric_%s_%s" % (alpha, omega), spectral,
              omega / (2 * mp.pi))
        close("noise_numeric_%s_%s" % (alpha, omega), noise,
              omega / (4 * mp.pi) * mp.coth(mp.pi * omega / alpha))
        spectra.append({"alpha": number(alpha), "omega": number(omega),
                        "rho": number(spectral), "noise": number(noise)})
tables["spectra"] = spectra

dispersion = []
for alpha in alphas:
    for nu in map(mp.mpf, ["0.2", "1", "4"]):
        def integrand(x):
            if x == 0:
                return -1 / (2 * mp.pi ** 2)
            return -nu ** 2 * rho(x, alpha) / (mp.pi * x * (x ** 2 + nu ** 2))
        # This subtracted dispersion integral converges without a UV cutoff.
        value = mp.quad(integrand, [0, nu, 10 * nu, mp.inf])
        close("retarded_dispersion_%s_%s" % (alpha, nu), value,
              -nu / (4 * mp.pi), mp.mpf("1e-38"))
        dispersion.append({"alpha": number(alpha), "imaginary_frequency": number(nu),
                           "G_R(i_nu)-G_R(0)": number(value)})
tables["dispersion"] = dispersion

M, Om, lam = map(mp.mpf, ["1", "1.3", "0.7"])
probe = mp.mpf("0.4")
responses = []
variances = []
for alpha in alphas:
    def chi(omega):
        return 1 / (M * (Om ** 2 - omega ** 2) - 1j * lam ** 2 * rho(omega, alpha) / 2)
    ch = chi(probe)
    power = probe * ch.imag / 2  # unit amplitude applied force
    check("passive_driven_work_%s" % alpha, power > 0)
    responses.append({"alpha": number(alpha), "Re_chi": number(ch.real),
                      "Im_chi": number(ch.imag), "mean_work_unit_source": number(power)})
    def qvar_integrand(x):
        noise = (F(-x, alpha) + F(x, alpha)) / 2
        return lam ** 2 * abs(chi(x)) ** 2 * noise / mp.pi
    var = mp.quad(qvar_integrand, [0, Om / 2, Om * mp.mpf("0.9"), Om,
                                  Om * mp.mpf("1.1"), 2 * Om, 10 * Om, mp.inf])
    variances.append(var)
    responses[-1]["stationary_Q_variance"] = number(var)
for idx in (1, 2):
    close("same_mean_work_%s" % idx, mp.mpf(responses[idx]["mean_work_unit_source"]),
          mp.mpf(responses[0]["mean_work_unit_source"]), mp.mpf("1e-23"))
check("noise_variance_increases_with_alpha", variances[0] < variances[1] < variances[2])
tables["driven_oscillator"] = {"M": str(M), "Omega_R": str(Om), "lambda": str(lam),
                               "source_frequency": str(probe), "rows": responses}

# 2. Actual finite-dimensional Hamiltonian, not an assumed band spectrum.
I = sp.I
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -I], [I, 0]])
sz = sp.diag(1, -1)
ident = sp.eye(2)
gammas = [sp.kronecker_product(sx, ident), sp.kronecker_product(sz, ident)]
gammas += [sp.kronecker_product(sy, s) for s in (sx, sy, sz)]
for i in range(5):
    for j in range(i, 5):
        check("clifford_%d_%d" % (i, j),
              gammas[i] * gammas[j] + gammas[j] * gammas[i]
              == (2 * sp.eye(4) if i == j else sp.zeros(4)))
q1, q2, p1, p2, p3, h = sp.symbols("q1 q2 p1 p2 p3 h", real=True)
Ham = q1 * gammas[0] + q2 * gammas[1]
Ham += h * (p1 * gammas[2] + p2 * gammas[3] + p3 * gammas[4])
e2 = q1 ** 2 + q2 ** 2 + h ** 2 * (p1 ** 2 + p2 ** 2 + p3 ** 2)
check("Hamiltonian_square", sp.simplify(Ham ** 2 - e2 * sp.eye(4)) == sp.zeros(4))
exact("Hamiltonian_trace", sp.trace(Ham))
t = sp.symbols("t")
exact("Hamiltonian_characteristic_degeneracy", Ham.charpoly(t).as_expr() - (t ** 2 - e2) ** 2)

P, A, hp, L, K, C0, b2, G = sp.symbols("P A h L K C0 b2 G", positive=True)
d = hp * P
Ef = -A * ((L ** 2 + d ** 2) ** sp.Rational(3, 2) - d ** 3) / 3
Vrem = Ef + A * L ** 3 / 3 + A * L * d ** 2 / 2
R = A * hp ** 2 * P * (L - sp.sqrt(L ** 2 + d ** 2) + d)
exact("force_from_potential", sp.diff(Vrem, P) - R)
exact("critical_quadratic", sp.diff(Ef, P, 2).subs(P, 0) + A * L * hp ** 2)
R_series = sp.series(R, P, 0, 5).removeO()
exact("residual_series", R_series - (A * hp ** 3 * P ** 2 - A * hp ** 4 * P ** 3 / (2 * L)))
g = sp.symbols("g", positive=True)
beta = A * hp ** 3
delta = -A * hp ** 4 / (2 * L)
P_inv = g / K - beta * g ** 2 / K ** 3 + (2 * beta ** 2 / K ** 5 - delta / K ** 4) * g ** 3
exact("inverse_series_equation", sp.series(K * P_inv + beta * P_inv ** 2 + delta * P_inv ** 3 - g,
                                           g, 0, 4).removeO())
gNseries = sp.series(beta * P_inv ** 2 + delta * P_inv ** 3, g, 0, 4).removeO()
a0 = K ** 2 / beta
expected_series = g ** 2 / a0 - (2 / a0 ** 2 + A * hp ** 4 / (2 * L * K ** 3)) * g ** 3
exact("deep_source_law_next_term", gNseries - expected_series)
required_quartic = beta ** 2 / K + A * hp ** 4 / (2 * L)
exact("extra_quartic_needed_for_CFG695", (delta + required_quartic) / K ** 3 - 2 / a0 ** 2 + 1 / a0 ** 2)
exact("high_gap_force_slope", sp.limit(R / P, P, sp.oo) - A * hp ** 2 * L)
exact("high_gap_force_constant", sp.limit(R - A * hp ** 2 * L * P, P, sp.oo) + A * hp * L ** 2 / 2)

# SI exponents (kg, m, s), independently verifying the dimensional coefficient.
dim_K = sp.Matrix([-1, 3, -2])
dim_A = sp.Matrix([-2, -7, 4])
dim_h = sp.Matrix([0, 4, -2])
check("SI_acceleration_dimension", 2 * dim_K - dim_A - 3 * dim_h == sp.Matrix([0, 1, -2]))

# Independent quadratures of the occupied energy and counterterm-subtracted force.
zeroT = []
for x in map(mp.mpf, ["0.0001", "0.03", "0.3", "1", "3", "100"]):
    cuts = [0, x, 1] if x < 1 else [0, 1]
    energy_integral = -mp.quad(lambda q: q * mp.sqrt(q * q + x * x), cuts)
    energy_closed = -((1 + x * x) ** mp.mpf("1.5") - x ** 3) / 3
    close("occupied_energy_%s" % x, energy_integral, energy_closed)
    rem_integral = -mp.quad(lambda q: q * mp.sqrt(q * q + x * x) - q ** 2 - x ** 2 / 2, cuts)
    rem_closed = energy_closed + mp.mpf(1) / 3 + x ** 2 / 2
    close("subtracted_energy_%s" % x, rem_integral, rem_closed, mp.mpf("1e-40"))
    force_integral = x * mp.quad(lambda q: 1 - q / mp.sqrt(q * q + x * x), cuts)
    force_closed = x * (1 - mp.sqrt(1 + x * x) + x)
    close("force_integral_%s" % x, force_integral, force_closed)
    slope_integral = mp.quad(lambda q: 1 - q ** 3 / (q * q + x * x) ** mp.mpf("1.5"), cuts)
    slope_closed = 1 + 2 * x - (1 + 2 * x * x) / mp.sqrt(1 + x * x)
    close("positive_slope_integral_%s" % x, slope_integral, slope_closed)
    check("positive_force_slope_%s" % x, slope_integral > 0 and force_integral > 0)
    total_g = x + force_closed  # K=A=h=Lambda=1, hence a0=1
    zeroT.append({"Delta_over_Lambda": number(x), "epsilon_f_A_Lambda3": number(energy_closed),
                  "Vrem_A_Lambda3": number(rem_closed), "gN_A_h_Lambda2": number(force_closed),
                  "g_for_unit_parameters": number(total_g), "u": number(x),
                  "gN_over_g": number(force_closed / total_g),
                  "simple_mu_same_a0": number(total_g ** 2 / (1 + total_g))})
tables["zero_temperature_cutoff"] = zeroT

# Exact force-law inversion using direct integral root evaluation rather than a
# truncated series, and a separate low-field/high-field scaling discriminator.
def unit_R(p):
    return p * (1 - mp.sqrt(1 + p * p) + p)

law_rows = []
for field in map(mp.mpf, ["0.0001", "0.01", "0.1", "1", "10"]):
    pol = mp.findroot(lambda p: p + unit_R(p) - field, (field / 2, field))
    check("positive_root_%s" % field, 0 < pol < field)
    close("on_shell_source_%s" % field, field - pol, unit_R(pol))
    law_rows.append({"g": number(field), "P": number(pol), "gN": number(field - pol),
                     "gN_over_g_squared": number((field - pol) / field ** 2)})
tables["inverted_force_law_unit_parameters"] = law_rows
smallp = mp.mpf("1e-9")
close("deep_coefficient_limit_sample", unit_R(smallp) / (smallp + unit_R(smallp)) ** 2,
      1, mp.mpf("3e-9"))
largep = mp.mpf("1e8")
close("unbounded_polarization_high_field_sample", unit_R(largep) / (largep + unit_R(largep)),
      mp.mpf("0.5"), mp.mpf("3e-9"))

# 3. Finite-temperature determinant differentiated under the regulated integral.
def logcosh(x):
    return abs(x) + mp.log1p(mp.exp(-2 * abs(x))) - mp.log(2)


def thermal_R(p, temp, retune=False):
    upper = mp.sqrt(1 + p * p)
    bare = 2 * temp * logcosh(1 / (2 * temp)) if retune else mp.mpf(1)
    return p * (bare - 2 * temp * (logcosh(upper / (2 * temp)) - logcosh(p / (2 * temp))))


thermal_rows = []
for temp in map(mp.mpf, ["0.03", "0.2", "1"]):
    linear = 1 - 2 * temp * logcosh(1 / (2 * temp))
    cubic = 1 / (4 * temp) - mp.tanh(1 / (2 * temp)) / 2
    check("positive_thermal_linear_%s" % temp, linear > 0)
    check("positive_retuned_cubic_%s" % temp, cubic > 0)
    for p in map(mp.mpf, ["0.0001", "0.03", "0.3", "1", "3"]):
        def derivative(q):
            en = mp.sqrt(q * q + p * p)
            return q / en * mp.tanh(en / (2 * temp))
        direct = p * (1 - mp.quad(derivative, [0, min(p, mp.mpf(1)), 1]))
        closed = thermal_R(p, temp)
        close("finite_T_force_%s_%s" % (temp, p), direct, closed)
        # Finite-difference differentiation of the *free energy* is independent
        # of the analytical force antiderivative used in closed.
        def omega(dgap):
            return -2 * temp * mp.quad(
                lambda q: q * (mp.log(2) + logcosh(mp.sqrt(q * q + dgap * dgap) / (2 * temp))),
                [0, 1])
        differentiated = p + mp.diff(omega, p)
        close("finite_T_free_energy_derivative_%s_%s" % (temp, p), differentiated, closed,
              mp.mpf("1e-38"))
        thermal_rows.append({"T_over_Lambda": number(temp), "Delta_over_Lambda": number(p),
                             "fixed_T0_tuning_force": number(closed),
                             "retuned_force": number(thermal_R(p, temp, True))})
    tiny = mp.mpf("1e-8") * temp
    close("fixed_tuning_linear_asymptote_%s" % temp, thermal_R(tiny, temp) / tiny, linear,
          mp.mpf("1e-14"))
    close("retuned_cubic_asymptote_%s" % temp, thermal_R(tiny, temp, True) / tiny ** 3, cubic,
          mp.mpf("1e-14"))
tables["finite_temperature"] = thermal_rows

# 4. An exact parameter deformation, not a numerical fit for a0 or kappa.
eps = C0 - A * L ** 3 / 3
kappa2 = a0 ** 2 / (G * eps)
kap = sp.symbols("kappa_target", positive=True)
Cchosen = A * L ** 3 / 3 + K ** 4 / (A ** 2 * hp ** 6 * G * kap ** 2)
exact("arbitrary_kappa_counterterm", kappa2.subs(C0, Cchosen) - kap ** 2)
W = C0 + b2 * P ** 2 / 2 + Ef
shift = sp.symbols("delta_C")
for order in range(1, 5):
    exact("constant_preserves_P_derivative_%d" % order,
          sp.diff(W.subs(C0, C0 + shift) - W, P, order))
obs = sp.Matrix([b2 - A * hp ** 2 * L, a0, eps])
jac = obs.jacobian([b2, hp, C0])
exact("independent_parameter_Jacobian", jac.det() + 3 * K ** 2 / (A * hp ** 4))
family = []
for kval in [sp.Rational(1, 4), sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)]:
    # K and G must obey K=4*pi*G even in dimensionless illustrative units.
    choices = {K: 1, A: 1, hp: 1, L: 1, G: 1 / (4 * sp.pi), kap: kval}
    counterterm = sp.simplify(Cchosen.subs(choices))
    epsilon = sp.simplify(counterterm - sp.Rational(1, 3))
    exact("consistent_counterterm_family_%s" % kval,
          sp.sqrt(1 / ((1 / (4 * sp.pi)) * epsilon)) - kval)
    family.append({"kappa_target": str(kval), "K": "1", "G": "1/(4*pi)",
                   "A_h_Lambda": "all one", "C0": str(counterterm),
                   "a0": "1", "epsilon_vac": str(epsilon)})
tables["counterterm_family"] = family

result = {
    "claim_id": "HORIZON-R2-2026-10-20",
    "status": "completed",
    "checked_assertions": len(checks),
    "all_passed": all(row["passed"] for row in checks),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "software": {"python": platform.python_version(), "sympy": sp.__version__, "mpmath": mp.__version__},
    "precision_decimal_digits": mp.mp.dps,
    "checks": checks,
    "tables": tables,
    "scope": "Finite numerical checks and symbolic identities for the explicitly regulated models. No empirical normalization or universal physics theorem."
}
destination = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("horizon-round2-results.json")
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "checks": len(checks), "all_passed": result["all_passed"],
                  "output": str(destination), "script_sha256": result["script_sha256"]}))
