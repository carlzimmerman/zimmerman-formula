#!/usr/bin/env python3
"""Necessary nonlinear auxiliary-symbol compatibility for IC-4.

Constant spatial xi,u and flat barred metric, arbitrary fixed local momentum.
The differentiated object is the Hamiltonian, not a velocity Hessian. A
rank-one gradient block is not a Dirac count or a locality certificate.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

import sympy as s

HERE = Path(__file__).resolve().parent
BASE = "6708f1e3e"
INPUTS = {
    "IC4_ACTION.md":"cb37292e21e0b1fbeef59a20f7800cb3d32c0cd20a46d36fd286cc3dd0f467a8",
    "scalar_completion.py":"801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745",
    "local_clock_wave.py":"a88d84135ea99263c62ecc339feffc76830623fb70b394222a1843174be7511d",
    "quadratic_dirac.py":"8c5476ac217df3f3b146f7293ff69e91d4e72e8c4665e1ebfc2fd26fde98a1e0",
}


def load(name):
    path = HERE / name
    if hashlib.sha256(path.read_bytes()).hexdigest() != INPUTS[name]:
        raise RuntimeError("Pinned executable input changed: "+name)
    spec = importlib.util.spec_from_file_location("auxiliary_symbol_"+path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean(value):
    if isinstance(value, s.MatrixBase):
        return value.applyfunc(lambda v:s.factor(s.simplify(v)))
    return s.factor(s.simplify(value))


@lru_cache(None)
def derive():
    m, volume, a0sq, h = s.symbols("m volume a0_squared h", positive=True)
    xi, u, pi_trace, piTF2 = s.symbols("xi u pi_trace piTF_squared", real=True)
    A, B, Cj, Fc, Rbar = s.symbols("A_J B_J C_J F_curvature Rbar", real=True)
    gxi, gu = s.symbols("gradient_xi gradient_u", real=True)
    gradients = (gxi, gu)
    zero = {gxi:0, gu:0, Rbar:0}
    w = (u-1)*xi
    Ckin = m*volume*s.exp((3*u-4)*xi)/2
    Dplus = m*volume*s.exp(u*xi)/2
    Efac = s.exp(-2*w)/a0sq
    Jbar = A*gxi**2+B*gxi*gu+Cj*gu**2
    Qgrad = 4*u*xi*gxi*gu+2*xi**2*gu**2
    Z = Efac*(Jbar+Fc*Rbar)
    trace_coefficient = -s.Rational(2,3)+Z
    # Exact rational Hamiltonian from the proposed nonlinear Legendre map.
    Hkin = (piTF2+pi_trace**2/(9*trace_coefficient))/Ckin
    Hgradient = -Dplus*Qgrad
    Hamiltonian = Hkin+Hgradient
    # Local orthonormal barred frame; rotational invariance restores hbar^ij.
    Hgg = s.hessian(Hamiltonian, gradients).subs(zero).applyfunc(clean)
    rho = clean(pi_trace**2*Efac/(4*Ckin*Dplus))
    rho_symbol = s.Symbol("rho", nonnegative=True)
    Kgradient = -Hgg/Dplus
    Kcontrol = s.Matrix([[2*rho*A,rho*B+4*u*xi],
                         [rho*B+4*u*xi,2*rho*Cj+4*xi**2]])
    residuals = {"rational_Hessian":clean(Kgradient-Kcontrol),
                 "rho_simplification":clean(rho-pi_trace**2*s.exp(-6*w)/(m*m*volume**2*a0sq)),
                 "tracefree_independence":clean(Hgg.diff(piTF2)),
                 "flat_fixed_metric_curvature_independence":clean(Hgg.diff(Fc))}

    # Import the selected action coefficients, not an asserted expected symbol.
    wave = load("local_clock_wave.py").derive()
    T, ell, x = wave["T"], wave["ell"], wave["x"]
    coefficient_map = {A:wave["action_coefficients"]["A_J"],
                       B:wave["action_coefficients"]["B_J"],
                       Cj:wave["action_coefficients"]["C_J"]}
    alpha, beta, gamma = [clean(4*ell**2*coefficient_map[j]/3) for j in (A,B,Cj)]
    f = s.exp(-s.Rational(1,2))
    witness = {xi:s.Rational(1,4),u:s.Rational(2,3),
               pi_trace:-3*m*volume*f*h,a0sq:27*h*h*f/(8*ell**2)}
    rho0 = clean(rho.subs(witness, simultaneous=True))
    G0 = clean((-Hgg/(2*Dplus)).subs(coefficient_map).subs(witness, simultaneous=True))
    residuals["witness_rho"] = clean(rho0-8*ell**2/3)
    slope = clean(G0[0,1]/G0[0,0])
    residuals["witness_outer_square"] = clean(G0-2*alpha*s.Matrix([[1,slope],[slope,slope**2]]))
    residuals["witness_null_vector"] = clean(G0*s.Matrix([-slope,1]))

    # Twice averaged epsilon^2 convention: H2=kbar^2 phi^T Hgg phi/2,
    # so its field Hessian is kbar^2 Hgg (no remaining cosine factor).
    # x=e^(2/3) kbar^2/h^2 and F_mode=m volume exp(-1/2).
    physical_mode_prefactor = m*volume*f
    normalized_gradient = clean(Hgg.subs(coefficient_map).subs(witness, simultaneous=True)
                                 *s.exp(-s.Rational(2,3))/physical_mode_prefactor)
    residuals["witness_mode_normalization"] = clean(normalized_gradient+G0)
    dirac = load("quadratic_dirac.py").derive_ic4()
    # Symbols are the same named, equally assumed raw-action symbols.
    qH = clean(dirac["auxiliary_hessian"]/(dirac["F"]*dirac["h"]**2))
    Mactual = -qH
    residuals["quadratic_Hamiltonian_principal_bridge"] = clean(qH.diff(x)-normalized_gradient)
    residuals["quadratic_affine_gradient"] = clean(qH.diff(x,2))

    # Vary pi independently of xi,u, holding barred volume and action parameters.
    lam, j = s.symbols("lambda_rho trace_ratio", real=True)
    # Use the checked rho-parametrized result of Hamiltonian differentiation.
    Kparam = s.Matrix([[2*rho_symbol*A,rho_symbol*B+4*u*xi],
                       [rho_symbol*B+4*u*xi,2*rho_symbol*Cj+4*xi**2]])
    Ggeneral = clean((Kparam/2).subs(coefficient_map).subs(rho_symbol,rho0*lam))
    residuals["nonlinear_normalized_matrix"] = clean(
        Ggeneral-s.Matrix([[2*alpha*lam,beta*lam+2*u*xi],
                           [beta*lam+2*u*xi,2*gamma*lam+2*xi**2]]))
    detG = clean(Ggeneral.det())
    lambda_physical = j*j*s.exp(-6*(w+s.Rational(1,12)))
    physical_det = detG.subs(lam,lambda_physical)
    witness_j = {xi:s.Rational(1,4),u:s.Rational(2,3),j:1}
    derivatives = {name:clean(s.diff(physical_det,variable).subs(witness_j))
                   for name,variable in (("trace_ratio",j),("xi",xi),("u",u))}
    static_det = clean(detG.subs(lam,0))
    fixed_field_det = clean(detG.subs({xi:s.Rational(1,4),u:s.Rational(2,3)}))

    # Solve the determinant equation; no desired rank is fed to a rank routine.
    C_required = clean(s.solve(Kparam.det(),Cj)[0])
    identity_residual = clean(Kparam.subs(Cj,C_required).det())
    square_strength, square_slope = s.symbols("square_strength square_slope", real=True)
    target_polynomial = square_strength*(gxi+square_slope*gu)**2
    required_J_coefficients = {
        A:square_strength/rho_symbol,
        B:(2*square_strength*square_slope-4*u*xi)/rho_symbol,
        Cj:(square_strength*square_slope**2-2*xi**2)/rho_symbol}
    residuals["required_square_coefficient_matching"] = clean(
        (rho_symbol*Jbar+Qgrad).subs(required_J_coefficients,simultaneous=True)-target_polynomial)
    residuals["required_determinant_identity"] = identity_residual

    # Exact finite-gradient realization differs from merely linearizing in Z.
    # Solve the full trace denominator for a desired gradient polynomial Rg.
    rg, aa, ee, Zsymbol = s.symbols("gradient_difference kinetic_weight E Z", real=True)
    Zrequired = clean(s.solve(s.Eq(aa*Zsymbol/(1-3*Zsymbol/2),rg),Zsymbol)[0])
    exact_completion_residual = clean(aa*Zrequired/(1-3*Zrequired/2)-rg)
    eps = s.Symbol("epsilon", real=True)
    # Here aa=pi^2/(4 Ckin Dplus), rho=aa*E; rg is degree two in gradients.
    Jrequired = clean(Zrequired.subs({aa:rho_symbol/ee})/ee)
    linear_jet_residual = clean(s.diff(Jrequired.subs(rg,eps**2*rg),eps,2).subs(eps,0)/2-rg/rho_symbol)
    residuals["exact_rational_square_completion"] = exact_completion_residual
    residuals["exact_square_linear_gradient_jet"] = linear_jet_residual
    # Independent exact trace identity, not a zero substituted for the result.
    trace_change = pi_trace**2/(9*Ckin)*(
        1/(-s.Rational(2,3)+Zsymbol)-1/(-s.Rational(2,3)))
    residuals["exact_trace_denominator_difference"] = clean(
        trace_change+pi_trace**2*Zsymbol/(4*Ckin*(1-3*Zsymbol/2)))

    # A proposed new Hamiltonian square in an expanding neighborhood. This is
    # only a compatibility target; a smooth static/expanding patch is separate.
    target_H = -2*Dplus*alpha*(gxi+slope*gu)**2
    original_gradient_jet = clean((s.Matrix(gradients).T*Hgg*s.Matrix(gradients))[0]/2)
    matching = clean((target_H-original_gradient_jet.subs(coefficient_map)).subs(witness,simultaneous=True))
    correction = target_H-original_gradient_jet.subs(coefficient_map)
    homogeneous_residual = clean(correction.subs({gxi:0,gu:0}))
    homogeneous_first = s.Matrix([clean(s.diff(correction,variable).subs({gxi:0,gu:0}))
                                 for variable in (xi,u,pi_trace,gxi,gu)])
    target_hessian = clean(s.hessian(target_H,gradients))
    residuals["square_patch_witness_jet"] = matching
    residuals["square_patch_homogeneous"] = homogeneous_residual
    residuals["square_patch_homogeneous_first_variations"] = homogeneous_first
    residuals["square_target_determinant"] = clean(target_hessian.det())

    # If chi_a=-delta H/delta phi_a, the constant-field principal part is
    # chi_a=Hgg_ab Delta delta phi_b. Thus {chi_a,p_b}=-kbar^2 Hgg_ab.
    kbar2 = s.Symbol("bar_wave_number_squared",positive=True)
    lap = s.Matrix(s.symbols("laplacian_delta_xi laplacian_delta_u"))
    secondary_principal = Hgg*lap
    secondary_primary = -kbar2*secondary_principal.jacobian(lap)
    residuals["secondary_primary_sign"] = clean(secondary_primary+kbar2*Hgg)

    return dict(m=m,volume=volume,a0sq=a0sq,h=h,xi=xi,u=u,pi_trace=pi_trace,piTF2=piTF2,
        A_J=A,B_J=B,C_J=Cj,F_curvature=Fc,Rbar=Rbar,gxi=gxi,gu=gu,w=w,
        Ckin=Ckin,Dplus=Dplus,Efac=Efac,Jbar=Jbar,Qgrad=Qgrad,Z=Z,
        Hamiltonian=Hamiltonian,gradient_hessian=Hgg,rho=rho,rho_symbol=rho_symbol,rho0=rho0,
        T=T,ell=ell,x=x,alpha=alpha,beta=beta,gamma=gamma,coefficient_map=coefficient_map,
        G_witness=G0,square_slope=slope,witness_normalization_residual=residuals["witness_mode_normalization"],
        quadratic_M=Mactual,quadratic_bridge_residual=residuals["quadratic_Hamiltonian_principal_bridge"],
        G_nonlinear=Ggeneral,lambda_rho=lam,trace_ratio=j,lambda_physical=lambda_physical,
        determinant=detG,determinant_derivatives=derivatives,
        fixed_field_determinant=fixed_field_det,static_normalized_determinant=static_det,
        required_C_J=C_required,required_identity_residual=identity_residual,
        required_square_coefficients=required_J_coefficients,
        exact_square_Z=Zrequired,exact_square_J=Jrequired,
        exact_square_completion_residual=exact_completion_residual,
        exact_completion_linear_jet_residual=linear_jet_residual,
        square_target_H=target_H,square_matching_residual=matching,
        homogeneous_correction_residual=homogeneous_residual,
        homogeneous_first_variations=homogeneous_first,
        square_principal_determinant=clean(target_hessian.det()),
        wave_number_squared=kbar2,secondary_primary_fourier_symbol=secondary_primary,
        residuals=residuals)


def encode(value):
    if isinstance(value,dict):
        return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,s.MatrixBase):
        return encode(value.tolist())
    if isinstance(value,(tuple,list)):
        return [encode(v) for v in value]
    if isinstance(value,s.Basic):
        return str(value)
    return value


@lru_cache(None)
def run():
    d = derive()
    values = d["residuals"]
    checks = {name:all(s.simplify(v)==0 for v in (list(value) if isinstance(value,s.MatrixBase) else [value]))
              for name,value in values.items()}
    hashes = {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in INPUTS}
    return encode(dict(base=BASE,software=dict(python=platform.python_version(),sympy=s.__version__),
        input_sha256=hashes,input_hashes_match=hashes==INPUTS,
        exact_checks_passed=all(checks.values()),exact_checks=checks,exact_residuals=values,
        nonlinear_gradient_hessian=d["gradient_hessian"],rho=d["rho"],
        normalized_nonlinear_symbol=d["G_nonlinear"],lambda_physical=d["lambda_physical"],
        witness_symbol=d["G_witness"],quadratic_minus_M=-d["quadratic_M"],
        quadratic_M_determinant=clean(d["quadratic_M"].det()),
        determinant=d["determinant"],fixed_field_determinant=d["fixed_field_determinant"],
        witness_determinant_derivatives=d["determinant_derivatives"],
        static_determinant=d["static_normalized_determinant"],
        required_C_J=d["required_C_J"],required_square_coefficients=d["required_square_coefficients"],
        exact_rational_Z_for_square=d["exact_square_Z"],exact_rational_J_for_square=d["exact_square_J"],
        witness_matching_square_H=d["square_target_H"],
        full_nonlinear_closure_proved=False,
        scope="Necessary auxiliary spatial-principal compatibility at constant spatial fields and Rbar=0, fixed barred metric and independent fixed local momenta. No full coupled symbol, all-gradient ellipticity, constraint closure, matter-sector lift, or causality claim.",
        construction_condition="An outer-square Hamiltonian can match the IC4 witness jet and the flat homogeneous reduction. A smooth patch equal to the original Hamiltonian near pi=0 is one sufficient static-compatible choice; the original static gradient Hessian is generically indefinite. A single regular rank-one symbol everywhere cannot also equal that static symbol.",
        exact_completion_domain="The algebraic finite-gradient Z/J formulas require pi!=0 and nonzero displayed denominators; the original Legendre map also requires t!=0. They are compatibility formulas, not a globally regular completed action."))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-nonlinear-closure",action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["input_hashes_match"] or not result["exact_checks_passed"]:
        return 1
    return 2 if args.require_full_nonlinear_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
