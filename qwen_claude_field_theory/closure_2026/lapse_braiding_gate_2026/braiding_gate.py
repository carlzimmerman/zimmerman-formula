"""Changed-primary gate: EH[N^(2 eta)g] + fixed physical exponential f + Sm[g].

eta!=-1 for invertibility. Local static transverse principal scalar analysis
and a separate exact flat homogeneous action with canonical physical matter.
No full nonlinear gravitational count is inferred from the principal model.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sympy as s
import conformal_action
import transformed_lapse
import anisotropic_primary


def pb(f, g, q, p):
    return s.expand(sum(s.diff(f, x)*s.diff(g, y)-s.diff(f, y)*s.diff(g, x)
                        for x, y in zip(q, p)))


def linear_dirac(H, primary, q, p):
    """Finite linear Dirac algorithm with weak preservation and computed rank.

    Constant-coefficient quadratic H only. At each stage take left null vectors
    of the actual multiplier matrix; independent unresolved drift becomes a
    new constraint. Stop only once every preservation equation closes weakly.
    """
    # Prefer pn over pz when eliminating a mixed primary. This avoids an
    # artificial division by eta that would obscure the regular eta=0 control.
    phase = q+list(reversed(p))
    cons = list(primary)
    stages = [list(primary)]

    def weak(expr):
        matrix = s.Matrix(cons).jacobian(phase)
        indices = matrix.rref()[1]
        solved = s.solve(cons, [phase[i] for i in indices], dict=True)[0]
        return s.factor(expr.subs(solved, simultaneous=True))

    for _ in range(8):
        multiplier_matrix = s.Matrix([[pb(c, a, q, p) for a in primary] for c in cons])
        drift = s.Matrix([weak(pb(c, H, q, p)) for c in cons])
        nulls = multiplier_matrix.T.nullspace()
        added = []
        for null in nulls:
            condition = weak((null.T*drift)[0])
            if condition != 0:
                cons.append(condition)
                added.append(condition)
        if added:
            stages.append(added)
            continue
        multipliers = s.symbols("u0:"+str(len(primary)))
        equations = list(multiplier_matrix*s.Matrix(multipliers)+drift)
        solved = s.solve(equations, multipliers, dict=True)
        solved = solved[0] if solved else {}
        residuals = [s.factor(e.subs(solved)) for e in equations]
        if any(r != 0 for r in residuals):
            raise AssertionError("Unclosed preservation equation")
        break
    else:
        raise RuntimeError("Constraint iteration bound reached; no closure claimed")
    Omega = s.Matrix([[pb(c, a, q, p) for a in cons] for c in cons])
    rank = Omega.rank()
    first = len(cons)-rank
    return dict(primary=primary, constraints=cons, stages=stages,
                matrix=Omega, determinant=s.factor(Omega.det()), rank=rank,
                first_class=first, second_class=rank,
                dof=s.Rational(2*len(q)-2*first-rank, 2),
                multipliers=solved, preservation_residuals=residuals)


def homogeneous():
    """Exact minisuperspace BEFORE mode expansion: a means transformed scale.

    Physical a_phys=a/N^eta, physical lapse N, canonical minimal scalar sigma.
    Bare f vanishes identically on these homogeneous fields before variation.
    """
    a, N, m = s.symbols("a N m", positive=True)
    eta, Lam = s.symbols("eta Lambda", real=True)
    ad, sd = s.symbols("ad sd", real=True)
    sigma = s.symbols("sigma", real=True)
    pa, pn, ps = momenta = list(s.symbols("pa pn ps", real=True))
    coords = [a, N, sigma]
    L = -3*m*a*ad**2/N**(1+eta)-m*Lam*a**3*N**(1+eta)+a**3*sd**2/(2*N**(1+3*eta))
    velocities = s.solve([pa-s.diff(L, ad), ps-s.diff(L, sd)], (ad, sd), dict=True)[0]
    H = s.powsimp(s.expand((pa*ad+ps*sd-L).subs(velocities)), force=True)
    C = s.factor(pb(pn, H, coords, momenta))
    value_pa2 = s.solve(C, pa**2)[0]
    bracket = s.factor(pb(pn, C, coords, momenta))
    on_constraint = s.factor(s.powsimp(bracket.subs(pa**2, value_pa2), force=True))
    Omega = s.Matrix([[0, on_constraint], [-on_constraint, 0]])
    rank = Omega.rank()
    multiplier = s.symbols("uN")
    drift = pb(C, H, coords, momenta)
    # Generic stratum only: eta not in {0,-1,-1/3}, ps!=0, a,N,m>0.
    u_solution = s.factor(drift/bracket)
    preserving = s.simplify(pb(C, H+multiplier*pn, coords, momenta).subs(multiplier, u_solution))
    gr_H = H.subs(eta, 0)
    gr_C = pb(pn, gr_H, coords, momenta)
    gr_Omega = s.Matrix([[pb(f, g, coords, momenta) for g in (pn, gr_C)] for f in (pn, gr_C)])
    gr_rank = gr_Omega.rank()
    gr_preserve = s.simplify(pb(gr_C, gr_H+multiplier*pn, coords, momenta))
    # Redo the exceptional branch, rather than inserting it in a generic
    # quotient. At eta=-1/3, C implies A=0 and its drift implies pa=0 if ps!=0.
    A = -pa**2/(12*m*a)+m*Lam*a**3
    exceptional_H = H.subs(eta, -s.Rational(1, 3))
    exceptional_C = pb(pn, exceptional_H, coords, momenta)
    exceptional_drift = s.factor(pb(exceptional_C, exceptional_H, coords, momenta))
    exceptional_pa = s.solve(exceptional_drift, pa)[0]
    exceptional_Lam = s.solve(A.subs(pa, exceptional_pa), Lam)[0]
    exceptional_pa_drift = s.factor(pb(pa, exceptional_H, coords, momenta).subs(
        {pa: exceptional_pa, Lam: exceptional_Lam}))
    vacuum_differential = [s.simplify(s.diff(C, variable).subs({ps: 0, pa: 0, Lam: 0}))
                           for variable in coords+momenta]
    return dict(a=a, N=N, m=m, eta=eta, ps=ps, L=L, H=H,
                primary=[pn], secondary=[C], lapse_bracket_on_constraint=on_constraint,
                generic_matrix=Omega, generic_rank=rank,
                generic_dof=s.Rational(2*len(coords)-2*(2-rank)-rank, 2),
                generic_multiplier=u_solution, generic_preservation_residual=preserving,
                gr_matrix=gr_Omega, gr_rank=gr_rank,
                gr_dof=s.Rational(2*len(coords)-2*(2-gr_rank)-gr_rank, 2),
                gr_preservation_residual=gr_preserve,
                real_branch_pa_squared=value_pa2,
                generic_domain="a,N,m>0; eta outside {0,-1,-1/3}; ps!=0; real_branch_pa_squared>0",
                exception_minus_third=dict(
                    secondary=exceptional_C,
                    secondary_implies_A=s.simplify(exceptional_C+2*A/(3*N**s.Rational(1, 3))),
                    secondary_drift=exceptional_drift, drift_implies_pa=exceptional_pa,
                    secondary_then_implies_Lambda=exceptional_Lam,
                    pa_drift_on_final_surface=exceptional_pa_drift),
                vacuum_secondary_differential=vacuum_differential,
                exceptions="eta=-1 map singular; eta=-1/3 has no consistent ps!=0 homogeneous branch; ps=0 changes rank and ps=Lambda=0 is irregular; eta=0 independently recomputed",
                cosmological_constant_scope="EH seed includes optional -2 Lambda; set Lambda=0 for the zero-potential seed",
                scope="Exact homogeneous metric-plus-canonical-matter count, not a full inhomogeneous gravitational count")


@lru_cache(None)
def derive():
    raw = conformal_action.derive()
    z, n, v, zd, nd = (raw[x] for x in ("z", "n", "v", "zd", "nd"))
    m, eta, alpha, k = (raw[x] for x in ("m", "eta", "alpha", "k"))
    pz, pn, pv = momenta = list(s.symbols("pz pn pv", real=True))
    coords = [z, n, v]
    L = raw["L"]
    zd_solution = s.solve(pz-s.diff(L, zd), zd)[0]
    primary = [s.factor(pn-s.diff(L, nd).subs(zd, zd_solution)), pv]
    legendre = s.expand((pz*zd+pn*nd-L).subs(zd, zd_solution))
    H = s.factor(legendre.subs(nd, 0))
    legendre_residual = s.simplify(legendre-H-nd*primary[0])
    canonical = linear_dirac(H, primary, coords, momenta)
    unmodified = linear_dirac(H.subs(alpha, 0), primary, coords, momenta)
    eta_zero = linear_dirac(H.subs({eta: 0, alpha: 1}), [c.subs(eta, 0) for c in primary], coords, momenta)
    Z = s.symbols("Z", real=True)
    secondary = canonical["constraints"][len(primary):]
    aux = s.solve([c.subs({z: Z-eta*n, pn: eta*pz}, simultaneous=True)
                   for c in secondary], (n, v), dict=True)[0]
    Hred = s.factor(H.subs(z, Z-eta*n).subs(aux))
    z_static = s.solve(s.diff(L.subs({zd: 0, nd: 0, v: 0}), z), z)[0]
    static_reduced = s.factor(L.subs({zd: 0, nd: 0, v: 0}).subs(z, z_static))
    poisson_coefficient = s.factor(-s.diff(static_reduced, n, 2)/(2*m*k**2))
    newton_coefficient = poisson_coefficient.subs(alpha, 0)
    canonical.update(eta=eta, alpha=alpha, m=m, k=k, pn=pn, pz=pz,
                     H=H, Hred=Hred, scalar_velocity_hessian=s.hessian(L, (zd, nd)),
                     z_tilde_velocity=s.diff(Hred, pz),
                     gamma_static=s.factor(-z_static/n),
                     poisson_coefficient=poisson_coefficient,
                     G_measured=1/(8*s.pi*m*newton_coefficient),
                     mu_measured=s.factor(poisson_coefficient/newton_coefficient),
                     primary_derivation_residual=legendre_residual,
                     canonical_coordinate="Z=z+eta*n; its momentum remains pz after auxiliary reduction")
    eta_zero["Hred"] = s.simplify(Hred.subs({eta: 0, alpha: 1}))
    hom = homogeneous()
    residue = list(raw["residuals"].values())+[legendre_residual]
    for sector in (canonical, unmodified, eta_zero):
        residue += sector["preservation_residuals"]
    residue += [hom["generic_preservation_residual"], hom["gr_preservation_residual"]]
    return dict(canonical=canonical, unmodified=unmodified, eta_zero=eta_zero,
                homogeneous=hom, residuals=residue)


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
    if any(s.simplify(x) != 0 for x in d["residuals"]):
        raise AssertionError("Changed-primary variational or preservation residual failed")
    transformed = transformed_lapse.run()
    anisotropic = anisotropic_primary.run()
    extra_maps = {name: fn() for name, fn in (
        ("point_map", conformal_action.derive_general_map),
        ("gradient_map", conformal_action.derive_gradient_map))}
    algebra_checks = (transformed["checks_passed"] and anisotropic["algebra_checks_passed"]
                      and all(s.simplify(r) == 0 for item in extra_maps.values()
                              for r in item["residuals"].values()))
    if not algebra_checks:
        raise AssertionError("An independently imported action/bracket audit failed")
    return encode(dict(two_tensor_gate=bool(d["canonical"]["dof"] == 0),
                       algebra_checks_passed=algebra_checks,
                       transformed_affine_screen=transformed,
                       anisotropic_primary_screen=anisotropic,
                       other_map_derivations=extra_maps,
                       result=d,
                       status="CONFORMAL_BRAIDING_EXTRA_SCALAR_DATA" if d["canonical"]["dof"] != 0 else "NOT_REFUTED",
                       limitation="One scalar canonical pair in this principal model is not a computed ghost sign, propagating wave dispersion, or full nonlinear count"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--require-two-tensor", action="store_true")
    args = ap.parse_args()
    result = run()
    if args.output:
        with args.output.open("x") as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write("\n")
    print(result["status"])
    print("Primary:", result["result"]["canonical"]["primary"])
    print("Scalar bracket rank:", result["result"]["canonical"]["rank"])
    print("Scalar pairs:", result["result"]["canonical"]["dof"])
    print("Static Psi/Phi:", result["result"]["canonical"]["gamma_static"])
    print("Homogeneous lapse bracket:", result["result"]["homogeneous"]["lapse_bracket_on_constraint"])
    raise SystemExit(2 if args.require_two_tensor and not result["two_tensor_gate"] else 0)


if __name__ == "__main__":
    main()
