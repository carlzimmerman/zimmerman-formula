#!/usr/bin/env python3
"""Exact pre-author photon-mass projector verification, stdlib only."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
import sys


class Poly:
    # Coefficients of x^i s^j, exact rationals.
    def __init__(self, t=None):
        self.t = {k: F(v) for k, v in (t or {}).items() if v}

    def __add__(self, b):
        d = dict(self.t)
        for k, v in b.t.items():
            d[k] = d.get(k, F(0)) + v
        return Poly(d)

    def __neg__(self):
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, b):
        return self + (-b)

    def __mul__(self, b):
        d = {}
        for (i, j), c in self.t.items():
            for (k, l), e in b.t.items():
                key = i + k, j + l
                d[key] = d.get(key, F(0)) + c * e
        return Poly(d)

    def scale(self, a):
        return Poly({k: a*v for k, v in self.t.items()})

    def ds(self):
        return Poly({(i, j-1): j*c for (i, j), c in self.t.items() if j})

    def divide_s(self, n):
        assert all(j >= n for i, j in self.t)
        return Poly({(i, j-n): c for (i, j), c in self.t.items()})

    def value(self, x, s):
        return sum((c*x**i*s**j for (i, j), c in self.t.items()), F(0))

    def __eq__(self, b):
        return self.t == b.t


one = Poly({(0, 0): 1})
x = Poly({(1, 0): 1})
s = Poly({(0, 1): 1})
r = x + s


def euler_minus(numerator, denominator_power, root):
    # (E-root)[N/(x+s)^p], sharing denominator power p+1.
    return (s*(numerator.ds()*r - numerator.scale(denominator_power))
            - numerator*r.scale(root), denominator_power+1)


def projected(numerator, roots, normalizer):
    p = 1
    for root in roots:
        numerator, p = euler_minus(numerator, p, F(root))
    return numerator.divide_s(2).scale(normalizer), p


def ordinary_polynomial(roots):
    coefficients = [F(1)]
    for root in roots:
        new = [F(0)]*(len(coefficients)+1)
        for j, c in enumerate(coefficients):
            new[j] -= root*c
            new[j+1] += c
        coefficients = new
    return coefficients


def value(c, a):
    return sum((v*a**j for j, v in enumerate(c)), F(0))


def main(output):
    roots = [F(0), F(1), F(2), F(1,2), F(3,2)]
    n, p = projected(one, roots, F(2,3))
    expected = s*(x.scale(3)-s)*(x-s.scale(3))
    assert p == 6 and n == expected.scale(-5)
    np, pp = projected(x, roots, F(2,3))
    assert pp == p and np == x*n  # P_s=x D_s dictionary.
    nnb, pnb = projected(one, [F(0),F(1),F(2)], F(1,2))
    assert pnb == 4 and nnb == s.scale(-3)
    signs = [n.value(F(t),F(1)) for t in [0,1,4]]
    assert signs[0] < 0 < signs[1] and signs[2] < 0

    ep = ordinary_polynomial(roots)
    eprime2 = sum((j*c*F(2)**(j-1) for j,c in enumerate(ep) if j), F(0))
    assert eprime2 == F(3,2)
    assert eprime2*F(2,3) == 1
    for a in roots:
        assert value(ep,a) == 0

    stencil = ordinary_polynomial([F(1),F(2),F(4),F(8),F(16)])
    assert stencil == list(map(F,[-1024,1984,-1240,310,-31,1]))
    for eigenvalue in [1,2,4,8,16]:
        assert value(stencil,F(eigenvalue)) == 0
    logarithmic_moment = sum((j*c*16**j for j,c in enumerate(stencil)),F(0))
    assert logarithmic_moment == 322560
    stencil_l1 = sum(abs(c) for c in stencil)
    assert stencil_l1 == 4590
    next_born_error_log4 = value(stencil,F(32))/logarithmic_moment
    assert next_born_error_log4 == 31

    # Rebuild parent B(z) through z^3 using arbitrary rational q,kappa,a.
    # q=F1(0), a=coefficient of z^2 in F1. The cancellation is checked
    # exhaustively in a declared rational grid, independent of radii fits.
    series_cases = 0
    for q in [F(-1),F(0),F(1),F(2,3)]:
        for kappa in [F(-2),F(0),F(1,3),F(3)]:
            for a in [F(-3,2),F(0),F(5,7)]:
                A2 = 2*q*a+kappa*kappa
                bracket2 = q*q+A2-3*(q+kappa)**2
                B1 = -q*q+(3*q*q-q*q)/2
                B2 = q*q/2+bracket2
                B3 = -bracket2+(6*q*a-A2)/2
                assert B1 == 0
                assert B2 == 2*q*a-F(3,2)*q*q-6*q*kappa-2*kappa*kappa
                assert B3 == 2*q*q+6*q*kappa+F(3,2)*kappa*kappa
                series_cases += 1

    # Beta integral: int_0^infinity y^2/(1+y)^4 dy=1/3.
    beta_moment = F(factorial(2)*factorial(0),factorial(3))
    assert beta_moment == F(1,3)
    # With angular trace H=6pi(a-b)Q^2 and f=1/(2M) int H D,
    # Pi_NB D=-3s/(Q^2+s)^4 gives -3(a-b)/(16pi M).
    gamma_nb_times_pi_M_over_a_minus_b = F(-3)*F(6,2)*F(1,16)*beta_moment
    assert gamma_nb_times_pi_M_over_a_minus_b == F(-3,16)
    # Born d*z^3 integral gives -d*s^2 log(s)/(64pi^2 M^4).
    gamma_b_times_pi2_M4_over_d = -F(1,2)*F(1,2)*F(1,16)
    assert gamma_b_times_pi2_M4_over_d == F(-1,64)

    # Local u*c*s*A^2 N†N/M^3 yields an s^2 log(s) tadpole at order u,
    # if admitted with this electromagnetic counting. The projector keeps
    # it exactly as any other same-power logarithm; it cannot distinguish it.
    contact_projector_multiplier = eprime2*F(2,3)
    assert contact_projector_multiplier == 1

    result = {
        "status":"exact bounded assertions passed",
        "full_D_kernel":"-5*s*(3*x-s)*(x-3*s)/(x+s)^6",
        "full_P_kernel":"x times the full D kernel; x=Q^2",
        "full_kernel_signs_at_x_over_s_0_1_4":["negative","positive","negative"],
        "nb_D_kernel":"-3*s/(x+s)^4",
        "euler_polynomial_ascending":[str(c) for c in ep],
        "normalization_derivative_at_2":str(eprime2),
        "q4_stencil_ascending":[str(c) for c in stencil],
        "q4_log_moment":str(logarithmic_moment),
        "q4_l1_weights":str(stencil_l1),
        "q4_next_s5over2_error_times_log4_over_sqrt_s":str(next_born_error_log4),
        "born_series_rational_cases":series_cases,
        "gamma_NB_times_pi_M_over_a_minus_b":str(gamma_nb_times_pi_M_over_a_minus_b),
        "gamma_B_times_pi2_M4_over_d":str(gamma_b_times_pi2_M4_over_d),
        "same_power_contact_log_projector_multiplier":str(contact_projector_multiplier),
        "non_claims":["No current tensor or QCD data computed", "No numerical EFT remainder bound",
                      "No massive-photon EFT contact matching identity proved",
                      "No full f(0), M_u(0), A, R or alpha"]}
    Path(output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"passed":True,"full_kernel_positive":False,
                      "q4_log_moment":str(logarithmic_moment),
                      "born_series_cases":series_cases}))


if __name__ == "__main__":
    main(sys.argv[1])
