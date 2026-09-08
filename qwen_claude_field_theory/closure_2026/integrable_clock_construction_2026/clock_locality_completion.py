#!/usr/bin/env python3
"""IC-3: a solved kinetic/clock-slope matching lemma, not full locality.

Retune J in S_IC1 + (m/2) integral sqrt(-g) Q^2 J/a0^2. This file
does NOT add the screened DQ operators or silently modify IC-2. It imports
one SHA-pinned raw scalar action and redoes its algebraic elimination.

Conventions are those of scalar_completion.py: x=k_physical^2/H_physical^2,
y=zdot/h, shift_scaled=k*shift/h, xdot/h=-2x. The dimensionless action
below is L2/(m exp(-1/2) B^3 h^2). All nonzero-mode calculations require
k>0, h>0 and the regular expanding background. No nonlinear lift is proved.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

import sympy as s


SOURCE = Path(__file__).resolve().with_name("scalar_completion.py")
SOURCE_SHA256 = "801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745"
BASE = "179aae239"


@lru_cache(None)
def source():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != SOURCE_SHA256:
        raise RuntimeError("Pinned scalar action changed; this derivation requires a new audit")
    spec = importlib.util.spec_from_file_location("ic3_pinned_scalar", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def local_symbol(expr, x):
    """Finite polynomial in spatial Laplacian, allowing constant parameters."""
    return not s.cancel(expr).as_numer_denom()[1].has(x)


@lru_cache(None)
def derive():
    raw = source().derive()
    x, T, alpha, d, e = [raw[q] for q in ("x", "Tcal", "alpha", "d", "e")]
    z, n, v = [raw[q] for q in ("z", "n", "v")]
    y, S, ratio = s.symbols("y shift_scaled ratio", real=True)
    recode = {raw["beta"]:2*d-s.Rational(1,3)-3*alpha/4,
              raw["gamma"]:e-s.Rational(1,16)+9*alpha/64-3*d/4}
    L = s.expand(raw["L"].subs(recode, simultaneous=True).subs({
        raw["zd"]:raw["h"]*y, raw["shift"]:raw["h"]*S/raw["k"]})/raw["h"]**2)
    fields = (n, v, S)
    equations = [s.diff(L, q) for q in fields]
    matrix, rhs = s.linear_eq_to_matrix(equations, fields)
    solved = (matrix.inv()*rhs).applyfunc(s.factor)
    solutions = dict(zip(fields, solved))
    constraints = [s.factor(q.subs(solutions, simultaneous=True)) for q in equations]
    reduced = s.factor(L.subs(solutions, simultaneous=True))
    a = s.factor(s.diff(reduced, y, 2)/2)
    b = s.factor(s.diff(reduced, z, y))
    c = s.factor(s.diff(reduced, z, 2)/2)
    # Time-dependent measure B^3 and xdot/h=-2x are retained in this IBP.
    g = s.factor(c-3*b/2+x*s.diff(b, x))
    D = T+e*x
    K = s.factor(4*D*a)
    lapse_y = s.factor(s.diff(solutions[n], y))
    lapse_z = s.factor(s.diff(solutions[n], z))
    A = s.factor(16*D*lapse_y)
    friction = s.factor(3-2*x*s.diff(a, x)/a)
    force = s.factor(g/a)
    clock_y = s.factor(-lapse_y*friction-2*x*s.diff(lapse_y, x)+lapse_z)
    clock_z = s.factor(lapse_y*force-2*x*s.diff(lapse_z, x))

    # Constructive rank-one coefficient ansatz, not a Hessian/DOF assertion.
    # For e>0 and T>27/4, K1>0, K0>0: K is genuinely linear here.
    ansatz = {alpha:e*ratio**2, d:e*ratio}
    Kr = s.Poly(s.expand(K.subs(ansatz)), x)
    Ar = s.Poly(s.expand(A.subs(ansatz)), x)
    matching = s.factor((Ar.nth(0)*Kr.nth(1)-Ar.nth(1)*Kr.nth(0))/e)
    roots = s.solve(matching, ratio)
    raw_checks = [s.factor(value-raw[key]) for value, key in
                  ((a,"a"), (b,"bcoef"), (c,"c"), (g,"g"))]
    return dict(raw=raw, x=x, T=T, alpha=alpha, d=d, e=e, z=z, y=y,
                n=n, v=v, S=S, ratio=ratio, L=L, reduced=reduced,
                solutions=solutions, constraint_matrix=matrix,
                constraint_residuals=constraints, raw_reduction_residuals=raw_checks,
                a=a, b=b, c=c, g=g, D=D, K=K, A=A,
                lapse_y=lapse_y, lapse_z=lapse_z, clock_y=clock_y, clock_z=clock_z,
                matching_polynomial=matching, matching_roots=roots,
                matching_scope="alpha*e=d^2, e>0; not a classification of repeated quadratic K roots")


@lru_cache(None)
def candidate():
    raw = derive()
    x,T,e = raw["x"],raw["T"],raw["e"]
    # First solved family: d/e=-9/T. Select its UV speed by solving the
    # action-derived expression, rather than inserting an expected speed.
    family = {raw["d"]:-9*e/T, raw["alpha"]:81*e/T**2}
    af,bf,cf,gf = [s.factor(raw[q].subs(family)) for q in ("a","b","c","g")]
    speed_family = s.limit(-gf/(af*x), x, s.oo)
    e_choice = s.solve(s.Eq(speed_family, s.Rational(1,3)), e)[0]
    selected = {raw["d"]:s.factor(-9*e_choice/T),
                raw["alpha"]:s.factor(81*e_choice/T**2), e:e_choice}
    a,b,c,g = [s.factor(raw[q].subs(selected)) for q in ("a","b","c","g")]
    D = s.factor(raw["D"].subs(selected))
    A = s.factor(raw["lapse_y"].subs(selected))
    B = s.factor(raw["lapse_z"].subs(selected))
    Ry = s.factor(raw["clock_y"].subs(selected))
    Rz = s.factor(raw["clock_z"].subs(selected))
    solutions = {q:s.factor(value.subs(selected)) for q,value in raw["solutions"].items()}

    alpha = selected[raw["alpha"]]
    dv = selected[raw["d"]]
    beta = s.factor(2*dv-s.Rational(1,3)-3*alpha/4)
    gamma = s.factor(e_choice-s.Rational(1,16)+9*alpha/64-3*dv/4)
    ell = raw["raw"]["ell"]
    physical_coefficients = {"A_J":3*alpha/(4*ell**2),
                             "B_J":3*beta/(4*ell**2),
                             "C_J":3*gamma/(4*ell**2)}
    mapping_checks = [s.factor(4*ell**2*physical_coefficients[q]/3-value)
                      for q,value in (("A_J",alpha),("B_J",beta),("C_J",gamma))]
    constitutive_checks = [s.factor(s.Rational(1,6)+3*alpha/8+beta/2-dv),
                           s.factor(s.Rational(3,16)+9*alpha/64+3*beta/8+gamma-e_choice)]

    # Both data classes use X f, so their longitudinal shift and trace-free
    # scalar ADM momenta are differential expressions, not inverse-Laplacian
    # tails. f is smooth compactly supported; take f>=0 for the pole witness.
    def initial_data(z0, y0):
        initial = {raw["z"]:z0, raw["y"]:y0}
        data = {str(q):s.factor(value.subs(initial, simultaneous=True))
                for q,value in solutions.items()}
        # The pinned action removed d[-9 m f B^3 h z^2]/dt. Restore its
        # -18 z contribution to the normalized original trace momentum.
        momentum = (s.diff(raw["L"], raw["y"])-18*raw["z"]).subs(
            raw["solutions"], simultaneous=True)
        data["trace_momentum"] = s.factor(momentum.subs(selected).subs(initial, simultaneous=True))
        data["physical_metric_scalar"] = s.factor(z0-data[str(raw["n"])]/3+data[str(raw["v"])]/4)
        data["shift_scaled_over_x"] = s.factor(data[str(raw["S"])]/x)
        return data

    velocity_data = initial_data(s.S.Zero, D*x)
    position_data = initial_data(D*x, s.S.Zero)
    velocity_slope = s.factor(Ry*D*x)
    # This polynomial is the repaired velocity-class slope. It is derived
    # independently from constant A and the lapse position coefficient.
    velocity_expected = s.factor(-3*A*D*x+B*D*x)
    position_slope = s.factor(Rz*D*x)
    position_polynomial = s.factor(A*g*D*x/a)
    position_tail = s.factor(position_slope-position_polynomial)
    # Separate the local polynomial from the nonzero screened inverse.
    tail_numerator, tail_denominator = s.cancel(position_tail).as_numer_denom()
    tail_quotient, tail_remainder = s.div(tail_numerator, tail_denominator, x)
    exterior_tail = s.factor(tail_remainder/tail_denominator)
    exterior_coefficient = s.factor(exterior_tail*D)

    gap = s.Symbol("T_gap", positive=True)
    domain = {T:s.Rational(27,4)+gap}
    Tlower = s.factor((raw["raw"]["T_exact"]-s.Rational(27,4)).subs(ell,s.Rational(4,5)))
    kinetic_positive = bool(s.factor(a.subs(domain)).is_positive and Tlower.is_positive)
    e_positive = bool(s.factor(e_choice.subs(domain)).is_positive and Tlower.is_positive)
    tail_positive = bool(s.factor(exterior_coefficient.subs(domain)).is_positive)
    # x already uses the PHYSICAL A=B exp(-1/12) and H=h exp(-1/4).
    # Hence (-h^2*g/a)/N0^2 divided by k^2/A0^2 is -g/(a*x).
    return dict(x=x,T=T,D=D,e=e_choice,alpha=alpha,beta=beta,gamma=gamma,
                action_coefficients=physical_coefficients,a=a,b=b,c=c,g=g,
                lapse_y=A,lapse_z=B,clock_y=Ry,clock_z=Rz,
                action_mapping_residuals=mapping_checks,
                constitutive_matching_residuals=constitutive_checks,
                kinetic_positive=kinetic_positive,e_positive=e_positive,
                uv_physical_speed_squared=s.factor(s.limit(-g/(a*x),x,s.oo)),
                velocity_initial_data=velocity_data,position_initial_data=position_data,
                velocity_initial_data_local=all(local_symbol(t,x) for t in velocity_data.values()),
                position_initial_data_local=all(local_symbol(t,x) for t in position_data.values()),
                velocity_slope=velocity_slope,velocity_slope_local=local_symbol(velocity_slope,x),
                velocity_pole_residual=s.factor(velocity_slope-velocity_expected),
                position_slope=position_slope,position_slope_local=local_symbol(position_slope,x),
                position_polynomial=position_polynomial,position_tail=position_tail,
                exterior_tail=exterior_tail,exterior_tail_coefficient=exterior_coefficient,
                position_tail_coefficient_positive=tail_positive,
                tail_division_residual=s.factor(position_tail-tail_quotient-exterior_tail))


@lru_cache(None)
def second_family():
    """The other solved first-slope family, followed through the next slope."""
    raw = derive()
    x,T,e = raw["x"],raw["T"],raw["e"]
    selected = {raw["d"]:-108*e/(8*T+27),
                raw["alpha"]:11664*e/(8*T+27)**2}
    a,g = [s.factor(raw[q].subs(selected)) for q in ("a","g")]
    D = raw["D"]
    K = s.factor(raw["K"].subs(selected))
    Ry,Rz = [s.factor(raw[q].subs(selected)) for q in ("clock_y","clock_z")]
    friction = s.factor(3-2*x*s.diff(a,x)/a)
    force = s.factor(g/a)
    # Differentiate the complete readout; f specifies data at one time only.
    # Do not evolve by differentiating the chosen initial profile D*x*f.
    Cy = s.factor(Rz-friction*Ry-2*x*s.diff(Ry,x))
    Cz = s.factor(Ry*force-2*x*s.diff(Rz,x))
    vy,vz = s.factor(Ry*D*x),s.factor(Rz*D*x)
    ay,az = s.factor(Cy*D*x),s.factor(Cz*D*x)
    pole = s.solve(K,x)[0]
    def residue(expr):
        numerator,denominator = s.cancel(expr).as_numer_denom()
        return s.factor(numerator.subs(x,pole)/s.diff(denominator,x).subs(x,pole))
    ry,rz = residue(ay),residue(az)
    numerator_y = s.cancel(ry).as_numer_denom()[0]
    numerator_z = s.cancel(rz).as_numer_denom()[0]
    position_only = s.solve(numerator_z,e)
    # solve(..., e) may drop an equation containing only the background
    # parameter T. Validate every proposed e against BOTH exact equations.
    compatible = [value for value in position_only
                  if s.simplify(numerator_y.subs(e,value))==0
                  and s.simplify(numerator_z.subs(e,value))==0]
    gap,epos = s.symbols("T_gap e_positive",positive=True)
    xpos = s.Symbol("x_nonnegative",nonnegative=True)
    sign_sub = {T:s.Rational(27,4)+gap,e:epos,x:xpos}
    return dict(a=a,K=K,ratio=-108/(8*T+27),pole=pole,
                kinetic_positive=bool(s.factor(a.subs(sign_sub)).is_positive),
                velocity_first=vy,position_first=vz,
                velocity_first_local=local_symbol(vy,x),position_first_local=local_symbol(vz,x),
                velocity_second=ay,position_second=az,
                velocity_second_local=local_symbol(ay,x),
                velocity_second_residue=ry,position_second_residue=rz,
                velocity_second_residue_positive=bool(s.factor(ry.subs(sign_sub)).is_positive),
                compatible_e_for_both_second_slopes=compatible,
                position_second_only_e=position_only)


def run():
    d,c,f2 = derive(),candidate(),second_family()
    residuals = (d["constraint_residuals"]+d["raw_reduction_residuals"]+
                 c["action_mapping_residuals"]+c["constitutive_matching_residuals"]+
                 [c["velocity_pole_residual"],c["tail_division_residual"]])
    return {
        "candidate":"IC-3: retuned J; solved constant-kinetic and velocity-clock matching",
        "status":"OPEN", "base":BASE,
        "input":{"path":str(SOURCE),"sha256":SOURCE_SHA256},
        "software":{"python":platform.python_version(),"sympy":s.__version__},
        "checks_passed":all(s.simplify(value)==0 for value in residuals),
        "residuals":[str(value) for value in residuals],
        "full_theory_closed":False,
        "clock_locality_completed":c["velocity_slope_local"] and c["position_slope_local"],
        "matching":{"condition":"K divides x^2 A Kprime for z=0, y=(T+ex) x f",
                    "polynomial":str(d["matching_polynomial"]),
                    "ratios_d_over_e":[str(t) for t in d["matching_roots"]],
                    "scope":d["matching_scope"]},
        "action":{"formula":"S_IC1 + (m/2) integral sqrt(-g) Q^2 [A_J a^2+B_J a.Du+C_J(Du)^2]/a0^2",
                  "coefficients":{k:str(v) for k,v in c["action_coefficients"].items()},
                  "constants":"ell=ln(9/5), Tcal=-27/16+54/(5 ell); these are fixed constructed coefficients",
                  "same_action_bridges":"J and its first variation vanish on homogeneous gradients; Q=0 kills the static correction; pure TT quadratic term unchanged on this background",
                  "new_auxiliary_velocity_pair":False,
                  "scope":"Point-map integrability is retained; no nonlinear Dirac rank or health assertion"},
        "repair":{"e":str(c["e"]),"alpha":str(c["alpha"]),"beta":str(c["beta"]),"gamma":str(c["gamma"]),
                  "a":str(c["a"]),"b":str(c["b"]),"c":str(c["c"]),"g":str(c["g"]),
                  "kinetic_positive":c["kinetic_positive"],"e_positive":c["e_positive"],
                  "UV_physical_speed_squared":str(c["uv_physical_speed_squared"]),
                  "n":str(c["lapse_y"]*d["y"]+c["lapse_z"]*d["z"]),
                  "n_dot_over_h":str(c["clock_y"]*d["y"]+c["clock_z"]*d["z"])},
        "velocity_data":{"initial":"z=0, y=(Tcal+ex) x f; f smooth compact",
                         "reconstructed":{k:str(v) for k,v in c["velocity_initial_data"].items()},
                         "local":c["velocity_initial_data_local"],
                         "n_dot_over_h":str(c["velocity_slope"]),"slope_local":c["velocity_slope_local"]},
        "remaining_clock_condition":{"initial":"z=(Tcal+ex) x f, y=0; f smooth, nonnegative, compact and nonzero",
                         "reconstructed":{k:str(v) for k,v in c["position_initial_data"].items()},
                         "local_initial_scalar_canonical_data":c["position_initial_data_local"],
                         "n_dot_over_h":str(c["position_slope"]),
                         "nonpolynomial_part":str(c["position_tail"]),
                         "exterior_coefficient_times_inverse_D":str(c["exterior_tail_coefficient"]),
                         "positive_coefficient":c["position_tail_coefficient_positive"],
                         "physical_readout":"X_clock=-grad(T)^2/2=1/(2N^2); delta X_clock=-exp(-1/2)n. The background X_clock is constant, so this linear scalar is gauge invariant.",
                         "scope":"Linear, constrained scalar action; scalar trace/TF momenta are local because trace_momentum and shift_scaled/x are polynomial. No nonlinear lift or full-theory causality theorem."},
        "second_constructed_family":{
            "d_over_e":str(f2["ratio"]),"a":str(f2["a"]),
            "kinetic_positive":f2["kinetic_positive"],
            "velocity_first":str(f2["velocity_first"]),"position_first":str(f2["position_first"]),
            "both_first_slopes_local":f2["velocity_first_local"] and f2["position_first_local"],
            "next_kinetic_root":str(f2["pole"]),
            "velocity_second_residue":str(f2["velocity_second_residue"]),
            "velocity_second_residue_positive":f2["velocity_second_residue_positive"],
            "position_second_only_e":[str(t) for t in f2["position_second_only_e"]],
            "compatible_e_for_both_second_slopes":[str(t) for t in f2["compatible_e_for_both_second_slopes"]],
            "scope":"A solved stronger first-slope matching family; the next derivative identity remains. No full classification of possible actions."},
        "uniform":{"kinetic":str(d["raw"]["zero_mode_kinetic"]),
                   "scope":"The genuinely uniform action is unchanged by retuning J; no k-divided momentum constraint or inherited full count."},
        "open_obligations":["Cancel the remaining physical clock readout pole while preserving this solved kinetic matching",
                            "Full nonlinear constraints, ordinary-matter perturbations, physical Cauchy lift and health",
                            "Static clock matching, PPN and realistic cosmology"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-clock-locality", action="store_true")
    parser.add_argument("--require-full-closure", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["checks_passed"]:
        return 1
    if args.require_full_closure or (args.require_clock_locality and not result["clock_locality_completed"]):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
