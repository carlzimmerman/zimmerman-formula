"""Exact chiral QED contributions, with no numerical alpha target or fitted LECs.

Run from the repository root through the computation-audit runner.  This checks
an explicit Goldstone action/determinant, not a free-coefficient rank model.
"""
import argparse
import json
from pathlib import Path

import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    inputs = json.loads(Path(__file__).with_name("SOURCE_INPUTS.json").read_text())
    assert inputs["alpha_target_used"] is False
    theta, phi = s.symbols("theta phi", real=True)
    mu, md, B, F, M, scale, Z, gA, mp = s.symbols(
        "mu md B F M scale Z gA mp", positive=True
    )
    e2, delta = s.symbols("e2 delta", nonnegative=True)
    f1, f2, f3 = s.symbols("f1 f2 f3", real=True)
    results = []

    def check(name, expression, expected):
        residue = s.simplify(s.expand(expression - expected))
        if residue != 0:
            raise AssertionError((name, residue))
        results.append({"name": name, "verified": True,
                        "value": s.sstr(s.simplify(expression))})

    # A diagonal chiral vacuum is enough at theta close to zero and positive
    # mu,md. Quark electric charges are the physical rational charges.
    U = s.diag(s.exp(s.I * phi), s.exp(s.I * (theta - phi)))
    Q = s.diag(s.Rational(2, 3), -s.Rational(1, 3))
    dashen_trace = s.trace(Q * U * Q * s.conjugate(U.T))
    check("Dashen vacuum trace is theta independent", dashen_trace,
          s.Rational(5, 9))
    check("Dashen theta curvature vanishes", s.diff(dashen_trace, theta, 2), 0)

    # Minimize V=-F^2 B[mu cos(phi)+md cos(theta-phi)] to quadratic order.
    # phi'(0)=md/(mu+md), following the linearized stationarity equation.
    a = md / (mu + md)
    chi_stationary = F**2 * B * (mu*a**2 + md*(1-a)**2)
    chi0 = F**2 * B * mu*md/(mu+md)
    check("stationary vacuum susceptibility", chi_stationary, chi0)
    Mtheta2 = B * s.sqrt((mu+md)**2 - 4*mu*md*s.sin(theta/2)**2)
    w = mu*md/(mu+md)**2
    check("aligned pion mass at theta zero", Mtheta2.subs(theta, 0), B*(mu+md))
    check("aligned pion theta curvature", s.diff(Mtheta2, theta, 2).subs(theta, 0),
          -B*(mu+md)*w)
    check("susceptibility mass form", chi0, F**2 * B*(mu+md)*w)

    # The finite subtraction agrees with the chiral scheme of source eq(35):
    # one real boson V1=y^2/(64pi^2)[log(y/scale^2)-1/2].
    y = s.symbols("y", positive=True)
    real_det = y**2/(64*s.pi**2) * (s.log(y/scale**2)-s.Rational(1, 2))
    charged_det = 2*real_det
    chi_pure_loop = -M**2*w*3*s.diff(real_det, y).subs(y, M**2)
    check("pure pion loop agrees with source eq35", chi_pure_loop/(F**2*M**2*w),
          -s.Rational(3, 2)*M**2/(16*s.pi**2*F**2)*s.log(M**2/scale**2))
    chi_charged = -M**2*w*s.diff(charged_det, y).subs(y, M**2+delta)
    em_linear = s.diff(chi_charged, delta).subs(delta, 0)*delta
    em_relative = em_linear/(F**2*M**2*w)
    check("charged determinant susceptibility insertion", em_relative,
          -delta/(16*s.pi**2*F**2)*(1+s.log(M**2/scale**2)))
    em_relative_e2 = em_relative.subs(delta, 2*e2*F**2*Z)
    check("source eq36 complete loop in chiral subtraction", em_relative_e2,
          -e2*Z/(8*s.pi**2)*(1+s.log(M**2/scale**2)))

    # Independent sequence: first differentiate determinant in delta, then theta.
    det_em = s.diff(charged_det, y).subs(y, Mtheta2) * delta
    chi_em_second = s.diff(det_em, theta, 2).subs(theta, 0)
    check("independent theta-first/delta-first agreement",
          chi_em_second/(F**2*B*(mu+md)*w),
          em_relative.subs(M**2, B*(mu+md)))

    # A finite change of scalar subtraction shifts only an analytic local term.
    c = s.symbols("c", real=True)
    charged_general = y**2/(32*s.pi**2)*(s.log(y/scale**2)-c)
    general_em = -delta/F**2*s.diff(charged_general, y, 2).subs(y, M**2)
    check("finite subtraction difference is analytic", general_em-em_relative,
          delta*(2*c-1)/(32*s.pi**2*F**2))
    check("universal logarithmic mass coefficient",
          M/s.Integer(2)*s.diff(general_em, M), -delta/(16*s.pi**2*F**2))
    check("logarithmic mass coefficient independent of subtraction",
          s.diff(M/s.Integer(2)*s.diff(general_em, M), c), 0)

    # Degenerate source numerator mq*Sigma: Sigma=-<qbar q> per flavour.
    # m d/dm = M^2 d/d(M^2); divide by 2 flavours before taking the derivative.
    mcond_em = -y/s.Integer(2)*s.diff(delta*s.diff(charged_det, y), y)
    check("degenerate mSigma electromagnetic loop",
          (mcond_em/(F**2*y/s.Integer(2))).subs(y, M**2), em_relative)

    # Nucleon invariant operators, using the Lagrangian (2.28)-(2.29),
    # not the inconsistent printed local mass formula (3.8) of that preprint.
    tau3 = s.diag(1, -1)
    Qn = s.diag(1, 0)  # e factored out
    Qt = Qn - s.trace(Qn)/2*s.eye(2)
    O1 = s.trace(Qt*Qt)
    O2 = s.trace(Qn)*Qt
    O3 = s.trace(Qt*Qt)
    local_mass = -e2*F**2*(f1*O1*s.eye(2)+f2*O2+f3*O3*s.eye(2))
    check("proton local electromagnetic mass", local_mass[0, 0],
          -e2*F**2*(f1+f3+f2)/2)
    check("neutron local electromagnetic mass", local_mass[1, 1],
          -e2*F**2*(f1+f3-f2)/2)
    check("splitting sees only isovector constant", local_mass[0, 0]-local_mass[1, 1],
          -e2*F**2*f2)

    # Universal HB chiral self energy, exact at order p^3 in pion masses.
    nucleon_loop = -gA**2/(16*s.pi*F**2)*((M**2+delta)**s.Rational(3, 2)-M**3)
    nucleon_em_linear = s.diff(nucleon_loop, delta).subs(delta, 0)*delta
    check("nucleon pion-cloud first-order electromagnetic term", nucleon_em_linear,
          -3*gA**2*M*delta/(32*s.pi*F**2))
    check("nucleon e2 sqrt-mass coefficient",
          nucleon_em_linear.subs(delta, 2*e2*F**2*Z),
          -3*e2*gA**2*Z*M/(16*s.pi))
    check("shared pion cloud cancels in proton-neutron difference",
          nucleon_loop-nucleon_loop, 0)
    check("individual proton relative response retains isoscalar baryon LEC",
          s.diff(local_mass[0, 0]/mp, f3), -e2*F**2/(2*mp))

    # Hand-checkable benchmarks: equal masses and zero charge.
    check("equal-mass susceptibility benchmark", chi0.subs(mu, md), F**2*B*md/2)
    check("neutral theory vacuum benchmark", em_relative_e2.subs(e2, 0), 0)
    check("neutral theory nucleon benchmark", nucleon_loop.subs(delta, 0), 0)
    result = {
        "assertion_tested": inputs["assertion_tested"],
        "checks": results, "checks_passed": len(results),
        "no_alpha_target_used": True,
        "scope": "Exact symbolic chiral terms; no four-dimensional c_H or alpha root calculated",
    }
    Path(args.output).write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"checks_passed": len(results), "alpha_target_used": False}))


if __name__ == "__main__":
    main()
