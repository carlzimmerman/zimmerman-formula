"""VCDM+f(s)+sB(K), B=-K^2/(K^2+K0^2): a new action, not a patch to old claims.

Exact scalar canonical closure of the transverse static principal action;
independent FLRW and homogeneous reductions. No rank/determinant/count inputs.
The local principal test does not certify nonlinear/global constraint closure.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys
import sympy as s
import adm_principal
import cuscuton_screen

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vcdm_flrw_gate_2026"))
import vcdm_flrw as flrw_seed


def pb(f, g, coords, momenta):
    return s.expand(sum(s.diff(f, q)*s.diff(g, p)-s.diff(f, p)*s.diff(g, q)
                        for q, p in zip(coords, momenta)))


def close_linear(H, primary, coords, momenta):
    """Preserve primary constraints, select independent linear secondaries,
    solve their preservation, and verify every resulting equation explicitly.
    Only for the constant-coefficient quadratic systems constructed below.
    """
    raw = [s.factor(pb(p, H, coords, momenta)) for p in primary]
    jac = s.Matrix(raw).jacobian(coords+momenta)
    pivots = jac.T.rref()[1]
    secondary = [raw[i] for i in pivots]
    cons = primary+secondary
    Omega = s.Matrix([[pb(c, d, coords, momenta) for d in cons] for c in cons])
    rank = Omega.rank()
    multipliers = s.symbols("u0:"+str(len(primary)))
    Ht = H+sum(u*p for u, p in zip(multipliers, primary))
    preserve = [s.factor(pb(c, Ht, coords, momenta)) for c in secondary]
    solved = s.solve(preserve, multipliers, dict=True)[0]
    residuals = [s.simplify(x.subs(solved)) for x in preserve]
    if any(x != 0 for x in residuals):
        raise AssertionError("Constraint preservation has an unresolved condition")
    first = len(cons)-rank
    return dict(H=H, primary=primary, secondary=secondary, matrix=Omega,
                determinant=s.factor(Omega.det()), rank=rank, first_class=first,
                second_class=rank, dof=s.Rational(2*len(coords)-2*first-rank, 2),
                multipliers=solved, preservation_residuals=residuals)


def canonical(d):
    m, b, alpha, k = (d[x] for x in ("m", "b", "alpha", "k"))
    z, zd, n, v = (d[x] for x in ("z", "zd", "n", "v"))
    p, pn, pv = momenta = list(s.symbols("p pn pv", real=True))
    coords = [z, n, v]
    L = d["L"]
    velocity = s.solve(p-s.diff(L, zd), zd)[0]  # b!=0 only
    H = s.factor((p*zd-L).subs(zd, velocity))
    result = close_linear(H, [pn, pv], coords, momenta)
    aux_solution = s.solve(result["secondary"], (n, v), dict=True)[0]
    Hred = s.factor(H.subs(aux_solution))
    coefficient = s.diff(Hred, p, 2)
    kinetic = s.factor(1/coefficient)
    # Hamilton's equations are used at b=-1/3 instead of inverting coefficient.
    z_velocity = s.diff(Hred, p)
    p_velocity = -s.diff(Hred, z)
    speed2 = s.factor(coefficient*s.diff(Hred, z, 2)/k**2)
    result.update(m=m, b=b, alpha=alpha, k=k, p=p, z=z, Hred=Hred,
                  kinetic=kinetic, speed2=speed2,
                  euler_lagrange=dict(momentum=s.diff(L, zd),
                                     lapse=s.diff(L, n), shift=s.diff(L, v)),
                  auxiliary_solution=aux_solution)
    critical = close_linear(H.subs(b, -s.Rational(1, 3)), [pn, pv], coords, momenta)
    critical.update(z_velocity=s.factor(z_velocity.subs(b, -s.Rational(1, 3))),
                    p_velocity=s.factor(p_velocity.subs(b, -s.Rational(1, 3))))
    # Rebuild Legendre transform where all three velocities are absent.
    zero_H = -L.subs(b, 0)
    trace_zero = close_linear(zero_H, momenta, coords, momenta)
    vacuum = close_linear(zero_H.subs(alpha, 1), momenta, coords, momenta)
    return result, critical, trace_zero, vacuum


def switch_properties():
    K = s.symbols("K", real=True)
    H, K0, acc2 = s.symbols("H K0 acc2", positive=True)
    B = -K**2/(K**2+K0**2)
    return dict(K=K, K0=K0, H=H, B=B,
                B0=B.subs(K, 0), Bprime0=s.diff(B, K).subs(K, 0),
                Bsecond0=s.diff(B, K, 2).subs(K, 0),
                trace_hessian=s.factor(acc2*s.diff(B, K, 2)),
                b_static=s.factor(acc2*s.diff(B, K, 2).subs(K, 0)/2),
                alpha_flrw=s.factor(1+B.subs(K, 3*H)))


def static_invariance():
    # Preserving the ORIGINAL zero trace Hessian for all s>0 requires B''=0.
    # A linear B is not automatically a boundary term when multiplied by s(x).
    K, c0, c1, x = s.symbols("K c0 c1 x", real=True)
    B = s.Function("B")
    general = s.dsolve(s.Eq(s.diff(B(K), K, 2), 0))
    affine = c0+c1*K
    acc2, shift = s.Function("acc2")(x), s.Function("shift")(x)
    # Local unit-volume shift contribution K=-d_x N^x in the static variation.
    Lshift = -c1*acc2*s.diff(shift, x)
    shift_eq = s.diff(Lshift, shift)-s.diff(s.diff(Lshift, s.diff(shift, x)), x)
    allowed = s.solve([affine.subs(K, 0), shift_eq.coeff(s.diff(acc2, x))],
                      (c0, c1), dict=True)[0]
    return dict(c0=c0, c1=c1, general_trace_degenerate_B=general,
                affine_hessian=s.diff(affine, K, 2),
                linear_shift_equation=shift_eq, allowed_constants=allowed,
                scope="Only sB(K) additions preserving zero trace Hessian at all K,s and arbitrary unchanged static branches; not all possible degenerate completions")


def general_local_deformation():
    """Uniform analytic reduction for C^2 F(s,K), on product domains I x J.

    F_KK=0 integrates in K to A(s)K+C(s). The code checks that reduction and
    the independent shift/static-coefficient restrictions. Completeness of
    this integration is the elementary calculus argument in DECISION.md,
    not a finite scan over trial functions.
    """
    x, invariant, K, H = s.symbols("x invariant K H", real=True)
    A, C = s.Function("A"), s.Function("C")
    sigma, shift = s.Function("sigma")(x), s.Function("shift")(x)
    F = A(invariant)*K+C(invariant)
    Lshift = -A(sigma)*s.diff(shift, x)
    ELshift = s.diff(Lshift, shift)-s.diff(s.diff(Lshift, s.diff(shift, x)), x)
    shift_coefficient = s.simplify(ELshift/s.diff(sigma, x)).subs(sigma, invariant)
    # Requirement: unchanged arbitrary static branch with the fixed original f.
    conditions = [shift_coefficient, s.diff(F.subs(K, 0), invariant)]
    solved = s.solve(conditions, (s.diff(A(invariant), invariant),
                                  s.diff(C(invariant), invariant)), dict=True)[0]
    return dict(integrated_form=F, trace_hessian=s.diff(F, K, 2),
                shift_equation=ELshift, static_restrictions=conditions,
                derivative_solution=solved,
                integration_residual=s.simplify(F-(F.subs(K, 0)+K*s.diff(F, K).subs(K, 0))),
                allowed_lapse_gradient_change=s.simplify(s.diff(F, invariant).subs(K, 3*H).subs(solved)),
                scope="C^2 F(s,K) on connected product domain I x J with 0 in J; regular first-derivative extension to s=0 for FLRW; no added operators/multipliers; zero trace Hessian at every s,K; fixed exact static law and arbitrary unchanged static momentum equation")


@lru_cache(None)
def derive():
    adm = adm_principal.derive()
    regular, critical, trace_zero, vacuum = canonical(adm)
    switch = switch_properties()
    fd = flrw_seed.derive_nonzero_mode()
    alpha_new = switch["alpha_flrw"]
    Knew = s.factor(fd["kinetic"].subs(fd["alpha"], alpha_new))
    speed_new = s.factor(fd["omega2"].subs(fd["alpha"], alpha_new))
    k2 = s.symbols("kappa_squared", positive=True)
    auxdet = s.factor(fd["auxiliary_determinant"].subs(fd["alpha"], alpha_new))
    pole = s.solve(s.denom(Knew).subs(fd["k"]**2, fd["a"]**2*k2), k2)[0]
    hom = flrw_seed.derive_homogeneous()
    # The extra action vanishes identically for spatially homogeneous lapse,
    # before homogeneous variation. Reusing this exact action reduction is valid.
    resid = list(adm["residuals"].values())
    for sector in (regular, critical, trace_zero, vacuum):
        resid.extend(sector["preservation_residuals"])
    resid.extend([fd["boundary_residual"], fd["background_tadpole_residual"]])
    resid.extend(hom["preservation_residuals"]+hom["stiff_solution_residuals"])
    return dict(nonzero=regular, critical=critical, trace_zero=trace_zero,
                vacuum=vacuum, switch=switch, static_invariance=static_invariance(),
                general_local_deformation=general_local_deformation(),
                flrw=dict(D=fd["D"], Z=fd["Z"], kinetic=Knew,
                          UV_kinetic=s.factor(s.limit(Knew, fd["k"], s.oo)),
                          UV_speed2=s.factor(s.limit(speed_new/fd["physical_k2"], fd["k"], s.oo)),
                          H_zero_then_UV_kinetic=s.factor(s.limit(Knew.subs(switch["H"], 0), fd["k"], s.oo)),
                          auxiliary_determinant=auxdet, positive_pole_kappa2=s.factor(pole),
                          limitation="UV recovery is not full stability: auxiliary elimination is singular at the displayed positive wave number; not by itself a physical pole proof"),
                homogeneous=hom, residuals=resid,
                scope="Static results are local nonzero-mode principal symbols on a regular nonzero-acceleration branch; not a full nonlinear gravitational Dirac count or a constructed global galaxy")


def encode(obj):
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, s.MatrixBase):
        return encode(obj.tolist())
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    if isinstance(obj, s.Integer):
        return int(obj)
    if isinstance(obj, s.Basic):
        return str(obj)
    return obj


def run():
    d = derive()
    if any(s.simplify(r) != 0 for r in d["residuals"]):
        raise AssertionError("Variational/canonical derivation check failed")
    regular = d["nonzero"]
    # Fixed dimensionless counterexample fixture, not an observational fit.
    # alpha=1/2 means y=log(2); r=1/12 fixes K0 relative to that acceleration.
    fixture = {regular["m"]: 1, regular["b"]: -s.Rational(1, 12),
               regular["alpha"]: s.Rational(1, 2), regular["k"]: 1}
    kinetic = regular["kinetic"].subs(fixture)
    speed2 = regular["speed2"].subs(fixture)
    accepted = regular["dof"] == 0 and kinetic > 0 and speed2 >= 0
    separate_screen = cuscuton_screen.run()
    if not separate_screen["checks_passed"]:
        raise AssertionError("Independent cuscuton derivation consistency check failed")
    return encode(dict(status="STATIC_PRINCIPAL_GATE_PASSED" if accepted else "EXPANSION_SWITCH_STATIC_SCALAR_GATE_FAILED",
                       acceptance=bool(accepted), derivation=d,
                       independent_cuscuton_screen=separate_screen,
                       fixture=dict(kinetic=kinetic, speed2=speed2),
                       non_claim="A gate PASS would not certify a full theory; rejection is scoped to this action/regular branch"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--require-two-tensor", action="store_true")
    args = ap.parse_args()
    result = run()
    if args.output:
        with args.output.open("x") as stream:
            json.dump(result, stream, sort_keys=True, indent=2)
            stream.write("\n")
    print(result["status"])
    d = result["derivation"]
    for key in ("rank", "dof", "kinetic", "speed2"):
        print("Static", key+":", d["nonzero"][key])
    print("FLRW UV speed squared:", d["flrw"]["UV_speed2"])
    print("FLRW auxiliary elimination pole:", d["flrw"]["positive_pole_kappa2"])
    print("Zero-field rank:", d["vacuum"]["rank"])
    print("Counterexample fixture:", result["fixture"])
    raise SystemExit(2 if args.require_two_tensor and not result["acceptance"] else 0)


if __name__ == "__main__":
    main()
