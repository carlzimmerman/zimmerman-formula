"""Bounded same-action constitutive audit; NO relativistic closure certificate.

Units c=1. Phi is physical lapse, Psi is spatial curvature (g03t reverses
those names). Static tau=t, Qbar=Q0->0, xi=0; common 1/(16*pi*G) convention.
The nonlinear constitutive function is retained in the leading weak-field
action. Sources and perturbations obey the boundary conditions in the note.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path

import sympy as s
from sympy.calculus.euler import euler_equations


@lru_cache(None)
def derive_static():
    x, e = s.symbols("x epsilon", real=True)
    Phi, Psi, chi = [s.Function(n)(x) for n in ("Phi", "Psi", "chi")]
    A, alpha, G, rho, jt = s.symbols("A alpha G rho jtot", real=True)
    # Calculate the three-dimensional Ricci scalar, with fields depending on
    # x only. Isotropy restores the gradient contractions below; this is not
    # a one-dimensional Einstein action. No Ricci formula is supplied as input.
    h = s.eye(3) * s.exp(-2*e*Psi)
    hi = h.inv()
    def d(expr, i):
        return s.diff(expr, x) if i == 0 else s.S.Zero
    Gamma = [[[s.simplify(sum(hi[a, l]*(d(h[l, c], b) + d(h[l, b], c)
                   - d(h[b, c], l)) for l in range(3))/2)
               for c in range(3)] for b in range(3)] for a in range(3)]
    Ric = s.Matrix(3, 3, lambda i, j: sum(
        d(Gamma[k][i][j], k) - d(Gamma[k][i][k], j)
        + sum(Gamma[k][i][j]*Gamma[l][k][l]
              - Gamma[l][i][k]*Gamma[k][j][l] for l in range(3))
        for k in range(3)))
    R = s.simplify(sum(hi[i, j]*Ric[i, j] for i in range(3) for j in range(3)))
    eh_raw = s.expand(s.series((1+e*Phi)*s.exp(-3*e*Psi)*R, e, 0, 3).removeO()).coeff(e, 2)
    eh_ibp = 2*s.diff(Psi, x)**2 - 4*s.diff(Phi, x)*s.diff(Psi, x)
    # Their difference is a calculated total derivative, not silently dropped.
    eh_res = s.simplify(eh_raw - eh_ibp - s.diff(4*(Phi-Psi)*s.diff(Psi, x), x))
    J = s.Function("J")
    Y = s.diff(chi, x)**2
    L = eh_ibp + alpha*s.diff(Phi, x)**2 + 2*A*s.diff(Phi, x)*s.diff(chi, x) - A*J(Y) - 16*s.pi*G*rho*Phi
    fields = (Phi, Psi, chi)
    els = [s.expand(eq.lhs) for eq in euler_equations(L, fields, (x,))]
    Yarg = s.Symbol("Yarg")
    Jy = s.diff(J(Yarg), Yarg).subs(Yarg, Y)
    expected = [4*s.diff(Psi, x, 2) - 2*alpha*s.diff(Phi, x, 2)
                - 2*A*s.diff(chi, x, 2) - 16*s.pi*G*rho,
                4*s.diff(Phi-Psi, x, 2),
                2*A*(s.diff(Jy*s.diff(chi, x), x) - s.diff(Phi, x, 2))]
    # Derive the constant-coefficient response by varying the same density.
    Lconst = L.subs(J(Y), jt*Y)
    ec = [eq.lhs for eq in euler_equations(Lconst, fields, (x,))]
    laps = s.symbols("lap_Phi lap_Psi lap_chi")
    equations = [eq.subs(dict(zip([s.diff(f, x, 2) for f in fields], laps))) for eq in ec]
    solved = s.solve(equations, laps, dict=True)[0]
    gn_ratio = s.simplify(s.limit(solved[laps[0]]/(4*s.pi*G*rho), jt, s.oo))
    boost = s.factor(solved[laps[0]]/(4*s.pi*G*rho*gn_ratio))
    return dict(A=A, alpha=alpha, jtot=jt, density=L, ricci=R,
                eh_ibp_residual=eh_res, el_equations=els,
                el_residuals=[s.simplify(a-b) for a, b in zip(els, expected)],
                slip=s.simplify(solved[laps[0]]-solved[laps[1]]),
                G_ratio=gn_ratio, boost=boost,
                B=s.simplify(A/(2-alpha)), linear_solution=solved)


def exponential_carrier():
    y, B, a0 = s.symbols("y B a0", positive=True)
    mu = 1-s.exp(-y)
    source = y*mu
    p = s.simplify((y-source)/B)
    Y = a0**2*p**2
    required_Jy = s.simplify(y/p)
    # Integrate along the proposed branch; this does not assume global
    # invertibility of y -> Y or a single-valued primitive on both branches.
    integrand = required_Jy*s.diff(Y, y)
    antiderivative = s.integrate(integrand, y)
    primitive = s.simplify(antiderivative-antiderivative.subs(y, 0))
    stiffness = s.simplify(s.diff(source, y)/s.diff(p, y))
    return dict(y=y, B=B, a0=a0, mu=mu, p=p, Y=Y,
                required_Jy=required_Jy, primitive=primitive,
                primitive_residual=s.simplify(s.diff(primitive, y)-required_Jy*s.diff(Y, y)),
                flux_residual=s.simplify((required_Jy-B)*p-source),
                dp_dy=s.diff(p, y), stiffness=stiffness,
                low_field_Jy=s.limit(required_Jy, y, 0, dir="+"))


def constrained_completion():
    y, B = s.symbols("y B", positive=True)
    p = y*s.exp(-y)/B
    Wlow = s.integrate(p, (y, 0, y))
    cap = s.simplify(p.subs(y, 1))
    Whigh = Wlow.subs(y, 1)+cap*(y-1)
    F = s.simplify(y*p-Wlow)
    # Metric lapse equation is y - B p = source, not y - p = source.
    mu_sat = s.simplify((y-B*cap)/y)
    return dict(y=y, B=B, cap=cap, Wlow=Wlow, Whigh=Whigh,
                conjugate_parametric=F,
                join_value_residual=s.simplify((Wlow-Whigh).subs(y, 1)),
                join_slope_residual=s.simplify(s.diff(Wlow-Whigh, y).subs(y, 1)),
                fenchel_residual=s.simplify(s.diff(F, y)-y*s.diff(p, y)),
                mu_sat=mu_sat, mu_exact=1-s.exp(-y))


def poisson(f, g, q, p):
    return s.expand(sum(s.diff(f, qi)*s.diff(g, pi)-s.diff(f, pi)*s.diff(g, qi)
                        for qi, pi in zip(q, p)))


def static_constraint_case(name, k, H):
    """Actual real-mode brackets for the STATIC saddle functional only.

    No clock/metric kinetic terms: this calculation cannot count relativistic
    modes. k=None means one real homogeneous mode, otherwise a cosine/sine
    pair on a periodic box. External perturbative source is time-independent
    and zero; a nonzero homogeneous source fails integrated compatibility.
    """
    if k is None:
        q = list(s.symbols("phi jx jy jz"))
        j = s.Matrix(q[1:])
        L = -(j.T*H*j)[0]/2
    else:
        q = list(s.symbols("phi_c jcx jcy jcz phi_s jsx jsy jsz"))
        jc, js, kv = s.Matrix(q[1:4]), s.Matrix(q[5:]), s.Matrix(k)
        L = (jc.dot(kv)*q[4]-js.dot(kv)*q[0]
             -(jc.T*H*jc)[0]/2-(js.T*H*js)[0]/2)
    p = list(s.symbols("p0:"+str(len(q))))
    Ham = -L
    primary = p
    secondary_raw = [poisson(c, Ham, q, p) for c in primary]
    jac = s.Matrix(secondary_raw).jacobian(q)
    # Row independence is computed, not prescribed per sector.
    pivots = jac.T.rref()[1]
    secondary = [secondary_raw[i] for i in pivots]
    constraints = primary+secondary
    omega = s.Matrix([[poisson(c, d, q, p) for d in constraints] for c in constraints])
    rank = omega.rank()
    first = len(constraints)-rank
    multipliers = s.symbols("u0:"+str(len(q)))
    Htotal = Ham+sum(u*pi for u, pi in zip(multipliers, p))
    preserve = [poisson(c, Htotal, q, p) for c in secondary]
    # Homogeneous linear preservation determines/limits multipliers only.
    # Verify that no remainder (candidate tertiary constraint) is suppressed.
    remainder = s.Matrix(preserve).subs(dict.fromkeys(multipliers, 0))
    return dict(name=name, q_count=len(q), primary_count=len(primary),
                independent_secondary_count=len(secondary), primary=primary,
                secondary=secondary, pb_matrix=omega.tolist(), pb_rank=rank,
                first_class_linear_static=first, second_class_linear_static=rank,
                computed_static_only_dof=s.Rational(2*len(q)-2*first-rank, 2),
                antisymmetric=omega == -omega.T,
                preservation=preserve,
                preservation_remainder=sum(abs(v) for v in remainder))


def static_constraint_examples():
    regular, plateau = s.diag(2, 3, 3), s.diag(0, 3, 3)
    return [static_constraint_case("regular_parallel", (1, 0, 0), regular),
            static_constraint_case("plateau_parallel", (1, 0, 0), plateau),
            static_constraint_case("plateau_transverse", (0, 1, 0), plateau),
            static_constraint_case("regular_zero_mode", None, regular),
            static_constraint_case("plateau_zero_mode", None, plateau)]


def total_potential_kernel():
    y = s.symbols("y", positive=True)
    primitive = y**2+2*(1+y)*s.exp(-y)-2
    mu = s.simplify(s.diff(primitive, y)/(2*y))
    longitudinal = s.simplify(s.diff(y*mu, y))
    return dict(y=y, primitive=primitive, mu=mu, longitudinal=longitudinal,
                constitutive_residual=s.simplify(mu-(1-s.exp(-y))),
                longitudinal_residual=s.simplify(longitudinal-(1+(y-1)*s.exp(-y))),
                deep_mond_coefficient=s.limit(mu/y, y, 0, dir="+"),
                newtonian_limit=s.limit(mu, y, s.oo),
                zero_eigenvalues=[s.limit(z, y, 0, dir="+") for z in (mu, longitudinal)])


def metric_route_screen():
    """Algebraic screen of a NEW VCDM+f candidate, not inherited closure."""
    K, KT2, phi, lam, V = s.symbols("K KT2 varphi lambda V", real=True)
    y, a0 = s.symbols("y a0", positive=True)
    # VCDM normalization M^2 N sqrt(h), Eq 36 of arXiv:2004.12549v2.
    # KT2=K_ij K^ij-K^2/3. Spatial multiplier D_i varphi=0 retained
    # in the theory, but irrelevant to this algebraic lambda elimination.
    kinetic = (KT2-s.Rational(2, 3)*K**2)/2 - s.Rational(3, 4)*lam**2-lam*(K+phi)-V
    lam_sol = s.solve(s.diff(kinetic, lam), lam)[0]
    reduced = s.expand(kinetic.subs(lam, lam_sol))
    f = 2*a0**2*(1-(1+y)*s.exp(-y))
    fs = s.simplify(s.diff(f, y)/(2*a0**2*y))
    return dict(lambda_solution=lam_sol, reduced_kinetic=reduced,
                trace_velocity_hessian=s.diff(reduced, K, 2),
                canonical_trace_over_M2sqrt_h=s.simplify(s.Rational(3, 2)*s.diff(reduced, K)),
                f=f, f_s=fs, static_mu=s.simplify(1-fs),
                homogeneous_f=s.limit(f, y, 0, dir="+"),
                homogeneous_f_s=s.limit(fs, y, 0, dir="+"),
                non_claim="No full constraints, FLRW perturbations, or causal transfer proved here")


def encode(obj):
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    if isinstance(obj, s.Integer):
        return int(obj)
    if isinstance(obj, s.Basic):
        return str(obj)
    return obj


def run():
    d = derive_static()
    exp = exponential_carrier()
    dual = constrained_completion()
    total = total_potential_kernel()
    corner = {d["A"]: s.Rational(9, 5), d["alpha"]: s.Rational(1, 100000)}
    checks = [d["eh_ibp_residual"], *d["el_residuals"], d["slip"],
              exp["primitive_residual"], exp["flux_residual"],
              dual["join_value_residual"], dual["join_slope_residual"],
              dual["fenchel_residual"], total["constitutive_residual"], total["longitudinal_residual"]]
    if any(s.simplify(r) != 0 for r in checks):
        raise AssertionError("A derived variational/constitutive identity failed")
    constraints = static_constraint_examples()
    for row in constraints:
        if not row["antisymmetric"] or row["preservation_remainder"] != 0:
            raise AssertionError("Static constraint preservation/bracket inconsistency")
    return encode(dict(status="SCOPED_OBSTRUCTION_AND_STATIC_REPAIR; FULL_THEORY_OPEN",
                       static=d, exact_carrier=exp, constrained_variant=dual,
                       total_potential=total, static_constraints=constraints,
                       metric_route_screen=metric_route_screen(),
                       corner_B=s.simplify(d["B"].subs(corner)),
                       bare_Y_low_field_boost_exact=d["boost"].subs(corner).subs(d["jtot"], 1),
                       bare_Y_low_field_boost_float=float(d["boost"].subs(corner).subs(d["jtot"], 1)),
                       bare_Y_low_field_G_over_bare=float((d["G_ratio"]*d["boost"]).subs(corner).subs(d["jtot"], 1)),
                       non_claims=["No covariant Dirac closure, PPN, or cosmological stability certification",
                                   "Static Fourier counts are not gravitational DOF counts",
                                   "No universal MOND no-go or novelty claim",
                                   "Finite xi and Qbar corrections are outside this reduction"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        # Exclusive creation prevents overwriting an earlier scientific result.
        with args.output.open("x") as stream:
            stream.write(payload)
    print(json.dumps({k: result[k] for k in ("status", "corner_B", "bare_Y_low_field_boost_float")}, indent=2))
    print("Static bracket ranks:", [(r["name"], r["pb_rank"]) for r in result["static_constraints"]])


if __name__ == "__main__":
    main()
