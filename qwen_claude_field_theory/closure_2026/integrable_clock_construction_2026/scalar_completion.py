#!/usr/bin/env python3
"""IC-2: exact FLRW scalar action and a constructive kinetic/UV repair.

Conventions: T=t; bar h_ij=B^2 exp(2 eps z cos(k x)) delta_ij;
ln N=1/4+eps n cos(k x); u=2/3+eps v cos(k x);
N^x=eps shift sin(k x). The displayed nonzero-mode L2 is twice the
spatially averaged eps^2 coefficient, divided by m exp(-1/2) B^3.
h=Bdot/B is constant, x=e^(2/3) k^2/(h^2 B^2), and xdot=-2 h x.

This derives a quadratic scalar sector of one exact witness. It supplies
neither a nonlinear Dirac count nor a physical domain-of-dependence proof.
The selected repair has positive kinetic coefficient at every x>=0 and
UV physical speed squared 4/9, but a finite negative-frequency band remains.
"""
import argparse
from functools import lru_cache
import json
import platform

import sympy as s


@lru_cache(None)
def derive():
    ep = s.Symbol("eps", real=True)
    coord = s.symbols("xcoord ycoord zcoord", real=True)
    B, m, h, k, ell = s.symbols("B m h k ell", positive=True)
    z, zd, n, v, shift = s.symbols("z zd n v shift", real=True)
    alpha, beta, gamma = s.symbols("alpha beta gamma", real=True)
    Tcal, x, d, e = s.symbols("Tcal x d e", real=True)
    C, S = s.cos(k*coord[0]), s.sin(k*coord[0])
    f = s.exp(-s.Rational(1, 2))
    xi = s.Rational(1, 4)+ep*n*C
    u = s.Rational(2, 3)+ep*v*C
    N = s.exp(xi)
    scale = B*s.exp(ep*z*C)
    metric = s.eye(3)*scale**2
    inverse = s.eye(3)/scale**2
    volume = scale**3

    # Raw spatial connection and Ricci tensor: no presumed scalar R formula.
    connection = [[[s.simplify(sum(inverse[a,l]*(
        s.diff(metric[l,j], coord[i])+s.diff(metric[l,i], coord[j])
        -s.diff(metric[i,j], coord[l])) for l in range(3))/2)
        for j in range(3)] for i in range(3)] for a in range(3)]
    ricci = s.zeros(3)
    for i in range(3):
        for j in range(3):
            ricci[i,j] = s.simplify(sum(
                s.diff(connection[a][i][j], coord[a])
                -s.diff(connection[a][i][a], coord[j])
                +sum(connection[a][a][l]*connection[l][i][j]
                     -connection[a][j][l]*connection[l][i][a]
                     for l in range(3)) for a in range(3)))
    curvature = s.simplify(s.trace(inverse*ricci))

    # Actual Lie derivative in the ADM velocity numerator.
    shift_vector = s.Matrix([ep*shift*S, 0, 0])
    metric_dot = 2*(h+ep*zd*C)*metric
    lie = s.Matrix(3, 3, lambda i,j: sum(
        shift_vector[l]*s.diff(metric[i,j], coord[l])
        +metric[l,j]*s.diff(shift_vector[l], coord[i])
        +metric[i,l]*s.diff(shift_vector[l], coord[j])
        for l in range(3)))
    Knum = inverse*(metric_dot-lie)/2
    kinetic_raw = m*volume*s.exp((3*u-4)*xi)*(
        s.trace(Knum*Knum)-s.trace(Knum)**2)/2

    # Potential derivatives are taken on U itself, before using the witness.
    U = lambda c: (1-c)*(s.log(1-c)**2-2*s.log(1-c)+2)-2
    a0sq = 27*h*h*f/(8*ell*ell)
    U0 = s.Rational(5,9)*(ell*ell+2*ell+2)-2
    Lambda = 6*h*h*f-a0sq*U0
    V = Lambda+a0sq*U(u*u)
    potential_raw = -m*volume*s.exp((3*u-2)*xi)*V
    clock_raw = 3*m*h*h*volume*s.exp((3*u-4)*xi)

    grad_xi = s.Matrix([s.diff(xi, q) for q in coord])
    grad_u = s.Matrix([s.diff(u, q) for q in coord])
    cross = (grad_xi.T*inverse*grad_u)[0]
    usq = (grad_u.T*inverse*grad_u)[0]
    spatial_raw = m*volume*s.exp(u*xi)*(
        curvature+4*u*xi*cross+2*xi*xi*usq)/2

    def witness_logs(expr):
        # Substitute before expand(): otherwise SymPy rewrites log(5/9) as
        # log(5)-2log(3), obscuring the exact background cancellations.
        return s.expand(expr.subs(s.log(s.Rational(5,9)), -ell), log=False)

    def average_quadratic(expr):
        # Twice average of eps^2 coefficient = average of the second derivative.
        jet = witness_logs(s.diff(expr, ep, 2).subs(ep, 0))
        jet = s.expand(jet).subs({C*C:s.Rational(1,2), S*S:s.Rational(1,2), C*S:0})
        return s.factor(jet.subs({C:0, S:0}))

    norm = m*f*B**3
    T_exact = -s.Rational(27,16)+s.Rational(54,5)/ell
    # Tcal is introduced only after actual differentiation; its definition is
    # invertible in the expressions here and has no expected ranks as input.
    def compress(expr):
        return s.factor(expr.subs(1/ell, s.Rational(5,54)*(Tcal+s.Rational(27,16))))

    raw0 = average_quadratic(kinetic_raw+potential_raw+clock_raw)/norm
    # This normalized expression is d[-9 m f B^3 h z^2]/dt / norm.
    background_boundary = -9*h*(3*h*z*z+2*z*zd)
    L0 = compress(s.factor(raw0-background_boundary))
    spatial_polynomial = s.factor(average_quadratic(spatial_raw)/(m*B*s.exp(s.Rational(1,6))*k*k))

    # Derive the correction using physical volume and physical contractions.
    # J is second order on this homogeneous witness, so the background trace
    # Q=3h/N0 suffices and no perturbed-Q terms contribute at this order.
    Acoef, Bcoef, Ccoef = s.symbols("A_J B_J C_J", real=True)
    w = (u-1)*xi
    physical_inverse = s.exp(-2*w)*inverse
    J = Acoef*(grad_xi.T*physical_inverse*grad_xi)[0]
    J += Bcoef*(grad_xi.T*physical_inverse*grad_u)[0]
    J += Ccoef*(grad_u.T*physical_inverse*grad_u)[0]
    Q_background = 3*h*s.exp(-s.Rational(1,4))
    correction_raw = m*N*volume*s.exp(3*w)*Q_background**2*J/(2*a0sq)
    correction_polynomial = s.factor(average_quadratic(correction_raw)/(m*B*s.exp(s.Rational(1,6))*k*k))
    correction_factor = s.factor(s.diff(correction_polynomial,n,2)/(2*Acoef))
    correction_polynomial = s.factor(correction_polynomial.subs({
        Acoef:alpha/correction_factor, Bcoef:beta/correction_factor,
        Ccoef:gamma/correction_factor}))
    Qtest, gn, gu = s.symbols("Qtest grad_lnN grad_u", real=True)
    correction_jet = Qtest**2*(Acoef*gn*gn+Bcoef*gn*gu+Ccoef*gu*gu)
    first_variation = [s.diff(correction_jet,q) for q in (Qtest,gn,gu)]
    static_first = [q.subs(Qtest,0) for q in first_variation]
    homogeneous_first = [q.subs({gn:0,gu:0}) for q in first_variation]
    L = s.expand(L0+h*h*x*(spatial_polynomial+correction_polynomial))

    # Solve the actual shift equation first, then the remaining auxiliary one.
    nsol = s.solve(s.diff(L,shift), n)[0]
    after_shift = s.expand(L.subs(n,nsol))
    vsol = s.factor(s.solve(s.diff(after_shift,v),v)[0])
    shiftsol = s.factor(s.solve(s.diff(L,n),shift)[0].subs(n,nsol).subs(v,vsol))
    solutions = {n:s.factor(nsol.subs(v,vsol)), v:vsol, shift:shiftsol}
    constraint_residuals = [s.factor(s.diff(L,q).subs(solutions, simultaneous=True))
                            for q in (n,v,shift)]
    reduced_explicit = s.factor(after_shift.subs(v,vsol))
    dmap = s.Rational(1,6)+3*alpha/8+beta/2
    emap = s.Rational(3,16)+9*alpha/64+3*beta/8+gamma
    # Change coefficient coordinates algebraically after eliminating fields.
    recode = {beta:2*d-s.Rational(1,3)-3*alpha/4,
              gamma:e-s.Rational(1,16)+9*alpha/64-3*d/4}
    reduced = s.factor(reduced_explicit.subs(recode, simultaneous=True))
    a = s.factor(s.diff(reduced,zd,2)/2)
    bcoef = s.factor(s.diff(reduced,z,zd)/h)
    c = s.factor(s.diff(reduced,z,2)/(2*h*h))
    # The measure is time dependent: d(B^3 h b)/dt=B^3 h^2(3b-2x b').
    g = s.factor(c-3*bcoef/2+x*s.diff(bcoef,x))
    kinetic_numerator = s.factor(4*(Tcal+e*x)*a)

    # The genuine uniform mode is differentiated independently, with no shift.
    uniform_raw = (kinetic_raw+potential_raw+clock_raw).subs(k,0)
    uniform = compress(witness_logs(s.diff(uniform_raw,ep,2).subs(ep,0))/(2*norm)
                       -background_boundary)
    zero_solutions = s.solve([s.diff(uniform,q) for q in (n,v)], (n,v), dict=True)[0]
    zero_reduced = s.factor(uniform.subs(zero_solutions, simultaneous=True))
    zero_kinetic = s.factor(s.diff(zero_reduced,zd,2)/2)
    zero_residuals = [s.factor(s.diff(uniform,q).subs(zero_solutions, simultaneous=True))
                      for q in (n,v)]

    raw_R_expected = (4*ep*k*k*z*C-2*ep*ep*k*k*z*z*S*S)/scale**2
    d0 = -2*n+3*v/4
    expected0 = (-3*zd*zd-6*h*d0*zd+2*k*shift*(zd+h*d0)
                 -18*h*h*n*v+h*h*(Tcal+s.Rational(27,4))*v*v)
    qdir = s.simplify(s.trace(Knum*Knum)-s.trace(Knum)**2)
    common_rate = h+ep*zd*C+ep*ep*k*shift*z*S*S
    qexpected = -6*common_rate**2+4*ep*k*shift*C*common_rate
    boundary_derivative = h*h*(3*bcoef-2*x*s.diff(bcoef,x))*z*z/2+h*bcoef*z*zd
    baseline = {alpha:0,d:s.Rational(1,6),e:s.Rational(3,16)}
    residuals = {
        "raw_ricci":s.simplify(curvature-raw_R_expected),
        "raw_kinetic":s.simplify(qdir-qexpected),
        "homogeneous_quadratic":s.factor(L0-expected0),
        "correction_quadratic":s.factor(correction_polynomial-alpha*n*n-beta*n*v-gamma*v*v),
        "momentum_constraint":s.factor(nsol-zd/(2*h)-3*v/8),
        "reduced_action":s.factor(reduced-a*zd*zd-h*bcoef*z*zd-h*h*c*z*z),
        "time_boundary":s.factor(reduced-boundary_derivative-a*zd*zd-h*h*g*z*z),
        "zero_mode_no_potential":s.factor(zero_reduced-zero_kinetic*zd*zd),
        "pure_tensor_correction":correction_polynomial.subs({n:0,v:0}),
    }
    return dict(m=m,B=B,h=h,k=k,ell=ell,z=z,zd=zd,n=n,v=v,shift=shift,
                alpha=alpha,beta=beta,gamma=gamma,Tcal=Tcal,x=x,d=d,e=e,
                T_exact=T_exact,connection=connection,ricci=ricci,Knum=Knum,
                L=L,L0=L0,spatial_polynomial=spatial_polynomial,
                correction_factor=correction_factor,correction_polynomial=correction_polynomial,
                static_correction_first_variation=static_first,
                homogeneous_correction_first_variation=homogeneous_first,
                dmap=dmap,emap=emap,solutions=solutions,after_shift=after_shift,
                reduced=reduced,a=a,bcoef=bcoef,c=c,g=g,
                kinetic_numerator=kinetic_numerator,zero_mode_kinetic=zero_kinetic,
                zero_mode_solutions=zero_solutions,zero_mode_residuals=zero_residuals,
                baseline_uv_kinetic_over_x=s.limit(a.subs(baseline)/x,x,s.oo),
                ir_g_over_x=s.limit(g/x,x,0),
                constraint_residuals=constraint_residuals,residuals=residuals)


@lru_cache(None)
def repair():
    raw=derive()
    x,T,ell=raw["x"],raw["Tcal"],raw["ell"]
    # A=0; choose d=0 to avoid a negative high-k kinetic term when alpha=0.
    # e=1/8 is a simple interior point of 3/44 <= e < 3/8 (0<c_UV^2<=1).
    selected={raw["alpha"]:0,raw["d"]:0,raw["e"]:s.Rational(1,8)}
    original={raw["alpha"]:0,raw["beta"]:-s.Rational(1,3),raw["gamma"]:s.Rational(1,16)}
    a,b,c,g=[s.factor(raw[j].subs(selected)) for j in ("a","bcoef","c","g")]
    Texact=raw["T_exact"].subs(ell,s.log(s.Rational(9,5)))
    D=72/(5*ell)-s.Rational(45,4)
    T_from_D=3*D/4+s.Rational(27,4)
    # Sign proof: ln(9/5)<4/5 by ln(1+y)<y. Hence D>27/4 and T>27/4.
    positive_kinetic=3*(8*(T-s.Rational(27,4))+x)/(8*T+x)
    auxiliary_denominator=T+x/8
    positive_auxiliary=(T-s.Rational(27,4))+s.Rational(27,4)+x/8
    transition=-2*T-s.Rational(81,4)+3*s.sqrt(64*T*T-48*T+729)/4
    g_numerator=s.factor(s.cancel(g/x).as_numer_denom()[0])
    ir=s.factor(s.limit(g/x,x,0))
    # Exact equation in x: 4a x² z_xx+(-2a x+4x² a_x)z_x-gz=0.
    rho=s.Symbol("rho",real=True)
    indicial=s.factor(a.subs(x,0)*(4*rho*(rho-1)-2*rho))
    roots=s.solve(indicial,rho)
    c1=s.factor(-ir/(2*a.subs(x,0)))
    series_residual=s.factor(s.limit(((-2*a*x+4*x*x*s.diff(a,x))*c1-g*(1+c1*x))/x,x,0))
    # Convert the coordinate frequency using physical A=B exp(-1/12) and
    # physical proper time d tau=N0 dt; do not inherit the bar-metric speed.
    physical_scale=raw["B"]*s.exp(-s.Rational(1,12))
    N0=s.exp(s.Rational(1,4))
    speed=-raw["h"]**2*g*physical_scale**2/(a*raw["k"]**2*N0**2)
    speed=s.factor(speed.subs(raw["k"]**2,
        x*raw["h"]**2*raw["B"]**2*s.exp(-s.Rational(2,3))))
    # Executed coefficientwise sign certificates, with the analytic logarithm
    # bound stated separately. No numerical samples stand in for all x>=0.
    Tgap=s.Symbol("Tgap",positive=True)
    xpos=s.Symbol("x_nonnegative",nonnegative=True)
    sign_sub={T:s.Rational(27,4)+Tgap,x:xpos}
    kinetic_sign=s.factor(a.subs(sign_sub))
    ir_sign=s.factor(ir.subs(sign_sub))
    Tgap_lower=s.factor((raw["T_exact"]-s.Rational(27,4)).subs(ell,s.Rational(4,5)))
    kinetic_positive=bool(kinetic_sign.is_positive and Tgap_lower.is_positive)
    # A positive g/x and positive a near zero disprove the all-x frequency
    # assertion. If this diagnostic were inconclusive it would return None.
    all_frequency=None
    if ir_sign.is_positive and kinetic_positive:
        all_frequency=False
    residuals={
        "kinetic_positive_decomposition":s.factor(a-positive_kinetic),
        "auxiliary_positive_decomposition":s.factor(auxiliary_denominator-positive_auxiliary),
        "T_D_identity":s.factor(raw["T_exact"]-T_from_D),
        "selected_d":s.factor(raw["dmap"].subs(original)),
        "selected_e":s.factor(raw["emap"].subs(original)-s.Rational(1,8)),
        "transition_root":s.simplify(g_numerator.subs(x,transition)),
        "future_series":series_residual,
    }
    return dict(a=a,bcoef=b,c=c,g=g,T_exact=Texact,
                coefficients={"A":0,"B_J":-1/(4*ell*ell),"C":3/(64*ell*ell)},
                solutions={str(q):s.factor(val.subs(original)) for q,val in raw["solutions"].items()},
                uv_physical_speed_squared=s.limit(speed,x,s.oo),
                physical_effective_speed_squared=speed,
                ir_g_over_x=s.factor(ir.subs(T,Texact)),
                transition_x=transition,transition_x_numeric=float(transition.subs(T,Texact)),
                future_indicial_roots=roots,future_constant_branch_c1=c1,
                kinetic_sign_expression=kinetic_sign,ir_sign_expression=ir_sign,
                T_gap_lower_bound=Tgap_lower,
                kinetic_positive_for_all_x=kinetic_positive,
                all_wavelength_frequency_nonnegative=all_frequency,
                causality_proved=False,residuals=residuals)


def run():
    raw, fixed = derive(), repair()
    checks={**raw["residuals"], **{"repair_"+k:v for k,v in fixed["residuals"].items()}}
    checks.update({"constraint_"+str(i):v for i,v in enumerate(raw["constraint_residuals"])})
    checks.update({"zero_constraint_"+str(i):v for i,v in enumerate(raw["zero_mode_residuals"])})
    checks.update({"static_transfer_"+str(i):v for i,v in enumerate(raw["static_correction_first_variation"])})
    checks.update({"homogeneous_transfer_"+str(i):v for i,v in enumerate(raw["homogeneous_correction_first_variation"])})
    passed=all(s.simplify(v)==0 for v in checks.values())
    baseline_all_kinetic=None
    if raw["baseline_uv_kinetic_over_x"].is_negative:
        baseline_all_kinetic=False
    return {
        "model":"IC-2 scalar completion on the exact constant-(u,N) expanding witness",
        "software":{"python":platform.python_version(),"sympy":s.__version__},
        "arithmetic":"Exact rational/symbolic algebra; transition decimal is labeled numerical",
        "normalization":"Twice average of eps^2 action / [m exp(-1/2) B^3], k != 0",
        "domain":"m,kappa>0; h=sqrt(kappa/(6m)); ell=ln(9/5); x>=0; no extra matter perturbation",
        "checks":{k:str(v) for k,v in checks.items()},"check_count":len(checks),
        "exact_checks_passed":passed,"full_theory_closed":False,
        "raw_action":str(raw["L"]),
        "general":{"a":str(raw["a"]),"b":str(raw["bcoef"]),"c":str(raw["c"]),
                   "g_after_time_IBP":str(raw["g"]),"d":str(raw["dmap"]),"e":str(raw["emap"]),
                   "kinetic_numerator":str(raw["kinetic_numerator"]),
                   "IR_g_over_x_independent_of_correction":str(raw["ir_g_over_x"])},
        "unmodified":{"UV_a_over_x":str(raw["baseline_uv_kinetic_over_x"]),
                      "positive_all_x_kinetic":baseline_all_kinetic},
        "repair":{
            "coefficients":{k:str(v) for k,v in fixed["coefficients"].items()},
            "a":str(fixed["a"]),"g":str(fixed["g"]),
            "solutions":{k:str(v) for k,v in fixed["solutions"].items()},
            "physical_effective_speed_squared":str(fixed["physical_effective_speed_squared"]),
            "UV_physical_speed_squared":str(fixed["uv_physical_speed_squared"]),
            "kinetic_positive_for_all_x":fixed["kinetic_positive_for_all_x"],
            "positivity_proof":"ln(9/5)<4/5 gives D>27/4; Tcal=3D/4+27/4>27/4; a=3[8(Tcal-27/4)+x]/(8Tcal+x)>0",
            "gradient_sign":"g>0 for 0<x<x_star, g=0 at x_star, g<0 for x>x_star; frequency=-h^2 g/a",
            "x_star":str(fixed["transition_x"]),"x_star_numeric":fixed["transition_x_numeric"],
            "all_wavelength_frequency_nonnegative":fixed["all_wavelength_frequency_nonnegative"],
            "causality_proved":fixed["causality_proved"],
            "future_indicial_roots":[str(v) for v in fixed["future_indicial_roots"]],
            "future_constant_branch_c1":str(fixed["future_constant_branch_c1"]),
            "future_scope":"For each fixed nonzero comoving k, x decays exponentially. The regular-singular exponents 0 and 3/2 imply bounded future z and decaying auxiliaries; this is not an all-time amplification or curvature/causality bound."},
        "zero_mode":{"kinetic":str(raw["zero_mode_kinetic"]),
                     "scope":"Genuinely uniform action varied without the k-divided shift equation; coefficient D/3>0, distinct from the k->0 nonzero-mode limit."},
        "open_obligations":["Interpret and bound the finite negative-frequency band using physical observables",
                            "Nonlinear constraint closure and added ordinary-matter perturbations",
                            "Physical Cauchy domain of dependence, not just short-wavelength speed",
                            "Static and homogeneous compatibility of the new action beyond these vanishing correction terms"],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-all-wavelength-frequency",action="store_true")
    parser.add_argument("--require-full-closure",action="store_true")
    args=parser.parse_args()
    result=run()
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["exact_checks_passed"]:
        return 1
    if args.require_full_closure or (args.require_all_wavelength_frequency and
            not result["repair"]["all_wavelength_frequency_nonnegative"]):
        return 2
    return 0


if __name__=="__main__":
    raise SystemExit(main())
