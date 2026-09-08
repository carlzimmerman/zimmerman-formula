#!/usr/bin/env python3
"""Covariant curvature/source bridge on the pinned expanding witness.

Use the PHYSICAL measure sqrt(-g)=N sqrt(h), not N sqrt(bar h).
bar h=e^(-2w)h is an intrinsic metric on the clock leaves, w=(u-1)ln N.
bar R is its three-dimensional Ricci scalar; Rhat=e^(-2w)bar R.

Delta S=(m/2) integral sqrt(-g) Q^2/a0^2 * Rhat *
        [A_R(ln N-1/4)+B_R(u-2/3)].

The quadratic map and a corrected scalar reduction are derived below.
No additional higher-curvature operators, nonlinear DOF count, all-channel
causality, realistic cosmology, or static clock matching is certified.
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
BASE = "0a9f9fa33"


@lru_cache(None)
def pinned_scalar():
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise RuntimeError("Pinned raw scalar action changed; re-audit this bridge")
    spec = importlib.util.spec_from_file_location("bridge_pinned_scalar", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ricci_scalar(metric, coords):
    inverse = metric.inv()
    connection = [[[s.simplify(sum(inverse[a,l]*(
        s.diff(metric[l,j],coords[i])+s.diff(metric[l,i],coords[j])
        -s.diff(metric[i,j],coords[l])) for l in range(3))/2)
        for j in range(3)] for i in range(3)] for a in range(3)]
    ricci = s.Matrix(3,3,lambda i,j:s.simplify(sum(
        s.diff(connection[a][i][j],coords[a])-s.diff(connection[a][i][a],coords[j])
        +sum(connection[a][a][l]*connection[l][i][j]
             -connection[a][j][l]*connection[l][i][a] for l in range(3))
        for a in range(3))))
    return s.simplify(s.trace(inverse*ricci))


@lru_cache(None)
def geometry():
    ep = s.Symbol("eps",real=True)
    coords = s.symbols("xcoord ycoord zcoord",real=True)
    B,m,h,k,ell = s.symbols("B m h k ell",positive=True)
    z,zd,n,nd,v,vd,shift = s.symbols("z zd n nd v vd shift",real=True)
    AR,BR,x = s.symbols("A_R B_R x",real=True)
    C,S = s.cos(k*coords[0]),s.sin(k*coords[0])
    xi = s.Rational(1,4)+ep*n*C
    u = s.Rational(2,3)+ep*v*C
    N = s.exp(xi)
    w = (u-1)*xi
    wdot = (u-1)*ep*nd*C+xi*ep*vd*C
    barred = s.eye(3)*B**2*s.exp(2*ep*z*C)
    physical = s.exp(2*w)*barred
    barred_dot = 2*(h+ep*zd*C)*barred
    physical_dot = s.exp(2*w)*(barred_dot+2*wdot*barred)
    shift_vector = s.Matrix([ep*shift*S,0,0])
    def lie(metric):
        return s.Matrix(3,3,lambda i,j:sum(
            shift_vector[l]*s.diff(metric[i,j],coords[l])
            +metric[l,j]*s.diff(shift_vector[l],coords[i])
            +metric[i,l]*s.diff(shift_vector[l],coords[j]) for l in range(3)))
    W = (wdot-sum(shift_vector[i]*s.diff(w,coords[i]) for i in range(3)))/N
    Qcov = ((physical_dot-lie(physical))/(2*N)-physical*W).applyfunc(s.simplify)
    Qbar = (barred_dot-lie(barred))/(2*N)
    point_residual = (Qcov-s.exp(2*w)*Qbar).applyfunc(s.simplify)
    Q = s.simplify(s.trace(physical.inv()*Qcov))
    Rbar = ricci_scalar(barred,coords)
    Rhat = s.exp(-2*w)*Rbar
    measure = s.simplify(N*s.sqrt(physical.det()))
    F = AR*(xi-s.Rational(1,4))+BR*(u-s.Rational(2,3))
    a0sq = 27*h*h*s.exp(-s.Rational(1,2))/(8*ell**2)
    density = m*measure*Q**2*Rhat*F/(2*a0sq)
    # Average the actual second derivative of the FULL density. No Q or
    # measure perturbation is dropped before differentiation.
    jet = s.expand(s.diff(density,ep,2).subs(ep,0))
    twice_average = s.factor(jet.subs({C*C:s.Rational(1,2),S*S:s.Rational(1,2),C*S:0}))
    normalized = s.factor(twice_average/(m*s.exp(-s.Rational(1,2))*B**3*h**2))
    polynomial = s.factor(normalized.subs(k*k,x*h*h*B*B*s.exp(-s.Rational(2,3))))
    factor = s.factor(s.diff(polynomial,z,n)/(AR*x))

    # First-variation jet includes the measure. On Q=0 everywhere all its
    # derivative coefficients vanish; on the witness Rhat=F=0 they also do.
    Mj,Qj,Rj,Fj = s.symbols("measure_jet Q_jet Rhat_jet F_jet",real=True)
    action_jet = Mj*Qj**2*Rj*Fj
    variation = [s.diff(action_jet,q) for q in (Mj,Qj,Rj,Fj)]
    static = [t.subs(Qj,0) for t in variation]
    witness = [t.subs({Rj:0,Fj:0}) for t in variation]
    # At fixed background N,u, F vanishes identically for ANY metric. This
    # proves the pure-TT correction vanishes without a scalar/TT substitution.
    pure_metric = s.simplify(F.subs({n:0,v:0}))
    return dict(ell=ell,x=x,z=z,n=n,v=v,AR=AR,BR=BR,
                Q=Q,Rbar=Rbar,Rhat=Rhat,F=F,measure=measure,
                second_variation=twice_average,quadratic=polynomial,map_factor=factor,
                mapping_residual=s.factor(polynomial-factor*x*z*(AR*n+BR*v)),
                ricci_linear_residual=s.simplify(s.diff(Rbar,ep).subs(ep,0)-4*k*k*z*C/B**2),
                measure_residual=s.simplify(measure-N*s.exp(3*w)*B**3*s.exp(3*ep*z*C)),
                point_map_residuals=list(point_residual),
                Q_auxiliary_velocity_residuals=[s.simplify(s.diff(Q,q)) for q in (nd,vd)],
                quadratic_velocity_residuals=[s.simplify(s.diff(polynomial,q)) for q in (zd,nd,vd,shift)],
                static_first_variation=static,witness_first_variation=witness,
                pure_TT_correction=s.simplify(pure_metric*Qj**2*Rj))


@lru_cache(None)
def spatial_ibp():
    """Actual spatial divergence in a curved, one-coordinate geometry."""
    q,r,t = s.symbols("qcoord rcoord tcoord",real=True)
    Z,xi,u,J = [s.Function(name)(q) for name in ("Z","xi","u","trace_Knum")]
    AR,BR,xi_dot,u_dot = s.symbols("A_R B_R xi_dot u_dot",real=True)
    w = (u-1)*xi
    F = AR*(xi-s.Rational(1,4))+BR*(u-s.Rational(2,3))
    metric = s.eye(3)*s.exp(2*Z)
    R = ricci_scalar(metric,(q,r,t))
    # Q=J/N. Physical measure times e^-2w Rbar thus gives this density.
    density = s.exp(3*Z+w-xi)*J**2*F*R
    weight = s.exp(Z+w-xi)*J**2*F
    bulk = 4*s.diff(weight,q)*s.diff(Z,q)-2*weight*s.diff(Z,q)**2
    boundary = -4*weight*s.diff(Z,q)
    return dict(raw=density,bulk=bulk,boundary=boundary,
                divergence_residual=s.simplify(density-bulk-s.diff(boundary,q)),
                auxiliary_velocity_residuals=[s.diff(bulk,v) for v in (xi_dot,u_dot)],
                scope="Spatial IBP may introduce spatial derivatives of metric velocity J; no time IBP or Ndot/udot is used")


@lru_cache(None)
def reduction():
    raw,bridge = pinned_scalar().derive(),geometry()
    x,T,e = raw["x"],raw["Tcal"],raw["e"]
    z,n,v = raw["z"],raw["n"],raw["v"]
    y,S,p,q = s.symbols("y shift_scaled p_source q_source",real=True)
    speed = s.Symbol("c_scalar_squared",positive=True)
    alpha = 81*e/T**2
    d = -9*e/T
    beta = 2*d-s.Rational(1,3)-3*alpha/4
    gamma = e-s.Rational(1,16)+9*alpha/64-3*d/4
    base = raw["L"].subs({raw["alpha"]:alpha,raw["beta"]:beta,raw["gamma"]:gamma})
    base = s.expand(base.subs({raw["zd"]:raw["h"]*y,raw["shift"]:raw["h"]*S/raw["k"]})/raw["h"]**2)
    correction = bridge["quadratic"].subs({
        bridge["AR"]:p/bridge["map_factor"],bridge["BR"]:q/bridge["map_factor"]})
    L = s.expand(base+correction)
    nsol = s.solve(s.diff(L,S),n)[0]
    after_shift = s.factor(L.subs(n,nsol))
    m1 = s.factor(s.diff(after_shift,z,v)/x)
    qchoice = s.solve(m1,q)[0]
    shifted = after_shift.subs(q,qchoice)
    vsol = s.solve(s.diff(shifted,v),v)[0]
    reduced = s.factor(shifted.subs(v,vsol))
    a = s.factor(s.diff(reduced,y,2)/2)
    b = s.factor(s.diff(reduced,z,y))
    c = s.factor(s.diff(reduced,z,2)/2)
    g = s.factor(c-3*b/2+x*s.diff(b,x))
    pchoice = s.solve(s.Eq(g,-a*speed*x),p)[0]
    source_choice = {p:pchoice,q:s.factor(qchoice.subs(p,pchoice))}
    final_L = s.factor(L.subs(source_choice,simultaneous=True))
    fields = (n,v,S)
    equations = [s.diff(final_L,field) for field in fields]
    matrix,rhs = s.linear_eq_to_matrix(equations,fields)
    values = (matrix.inv()*rhs).applyfunc(s.factor)
    solutions = dict(zip(fields,values))
    residuals = [s.factor(eq.subs(solutions,simultaneous=True)) for eq in equations]
    final_reduced = s.factor(final_L.subs(solutions,simultaneous=True))
    b,c,g = [s.factor(expr.subs(p,pchoice)) for expr in (b,c,g)]
    boundary = (3*b-2*x*s.diff(b,x))*z*z/2+b*z*y
    yy = s.Symbol("y_prime",real=True)
    bulk = a*y*y+g*z*z
    momentum = s.diff(bulk,y)
    EL = s.factor(s.diff(bulk,z)-s.diff(momentum,x)*(-2*x)
                  -s.diff(momentum,z)*y-s.diff(momentum,y)*yy-3*momentum)
    acceleration = s.solve(EL,yy)[0]
    def Dt(expr):
        return s.factor(s.diff(expr,x)*(-2*x)+s.diff(expr,z)*y+s.diff(expr,y)*acceleration)
    lapse = solutions[n]
    lapse_first = Dt(lapse)
    lapse_second = Dt(lapse_first)
    gap,xpos = s.symbols("T_gap x_positive",positive=True)
    Tlower = s.factor((raw["T_exact"]-s.Rational(27,4)).subs(raw["ell"],s.Rational(4,5)))
    frequency = s.factor(-g/a)
    factor = bridge["map_factor"]
    return dict(T=T,x=x,y=y,speed=speed,e=e,
                alpha=alpha,beta=s.factor(beta),gamma=s.factor(gamma),
                AR=s.factor(pchoice/factor),BR=s.factor(source_choice[q]/factor),
                p=pchoice,q=source_choice[q],m1=m1,a=a,b=b,c=c,g=g,
                lapse=lapse,auxiliary=solutions[v],shift_scaled=solutions[S],
                constraint_determinant=s.factor(matrix.det()),
                constraint_residuals=residuals,
                bridge_to_action_residual=s.factor(correction-x*z*(p*n+q*v)),
                source_matching_residual=s.factor(m1-(1+3*p/8+q)),
                time_IBP_residual=s.factor(final_reduced-boundary-a*y*y-g*z*z),
                z_equation_residual=s.factor(EL+2*a*(yy+3*y+speed*x*z)),
                clock_equation_residual=s.factor(lapse_second+5*lapse_first+(6+speed*x)*lapse),
                frequency_squared=frequency,
                kinetic_positive=bool(s.factor(a.subs(T,s.Rational(27,4)+gap)).is_positive and Tlower.is_positive),
                frequency_positive_for_x_positive=bool(frequency.subs(x,xpos).is_positive),
                uniform_kinetic=raw["zero_mode_kinetic"])


def run():
    geom,ibp,red = geometry(),spatial_ibp(),reduction()
    residuals = (geom["point_map_residuals"]+geom["Q_auxiliary_velocity_residuals"]+
                 geom["quadratic_velocity_residuals"]+geom["static_first_variation"]+
                 geom["witness_first_variation"]+ibp["auxiliary_velocity_residuals"]+
                 red["constraint_residuals"]+
                 [geom[q] for q in ("mapping_residual","ricci_linear_residual","measure_residual","pure_TT_correction")]+
                 [ibp["divergence_residual"]]+[red[q] for q in
                  ("bridge_to_action_residual","source_matching_residual","time_IBP_residual","z_equation_residual","clock_equation_residual")])
    return {
        "status":"OPEN covariant operator bridge and nonzero-mode scalar reduction",
        "base":BASE,"input":{"path":str(SOURCE),"sha256":SOURCE_SHA256},
        "software":{"python":platform.python_version(),"sympy":s.__version__},
        "checks_passed":all(s.simplify(r)==0 for r in residuals),
        "residuals":[str(r) for r in residuals],"full_theory_closed":False,
        "operator":{"action":"(m/2) integral sqrt(-g) Q^2/a0^2 Rhat [A_R(lnN-1/4)+B_R(u-2/3)]",
                    "geometry":"bar h_mu_nu=e^(-2w)h_mu_nu on clock leaves; bar R is its intrinsic Ricci scalar; Rhat=e^(-2w)bar R",
                    "measure":"Physical sqrt(-g)=N exp(3w) sqrt(bar h); no new matter metric",
                    "equivalent_Rhat":"Rhat=R3(h)+4 Delta_h w-2 |D_h w|^2",
                    "quadratic_normalization":"L2/[m exp(-1/2) B^3 h^2], twice spatial average of eps^2 coefficient",
                    "quadratic":str(geom["quadratic"]),"map_factor":str(geom["map_factor"])},
        "constructed_scalar_family":{
            "domain":"e>0; 0<c_scalar_squared<=1; k>0; m,kappa>0; exact IC-1 witness parameters; Tcal=-27/16+54/(5 ln(9/5))",
            "alpha":str(red["alpha"]),"beta":str(red["beta"]),"gamma":str(red["gamma"]),
            "J_normalization":"J=(3/(4 ell^2))[alpha a^2+beta a.Du+gamma(Du)^2], ell=ln(9/5)",
            "A_R":str(red["AR"]),"B_R":str(red["BR"]),"p":str(red["p"]),"q":str(red["q"]),
            "a":str(red["a"]),"g":str(red["g"]),"lapse":str(red["lapse"]),
            "auxiliary":str(red["auxiliary"]),"shift_scaled":str(red["shift_scaled"]),
            "constraint_determinant":str(red["constraint_determinant"]),
            "kinetic_positive":red["kinetic_positive"],
            "frequency_squared_over_h_squared":str(red["frequency_squared"]),
            "frequency_positive_for_x_positive":red["frequency_positive_for_x_positive"],
            "local_equations":"z''+3z'+c_scalar_squared*x*z=0; n''+5n'+(6+c_scalar_squared*x)n=0, primes=d/d(ht)",
            "physical_clock":"delta[-grad(T)^2/2]=-exp(-1/2)n; constant background clock norm makes this linear readout gauge invariant",
            "example":"e=1/8, c_scalar_squared=1/3 gives fixed finite couplings; the formulas specify the action before variation"},
        "bridges":{"static":"Q=0 everywhere annihilates the correction and all first-variation coefficients",
                   "homogeneous":"At the exact flat witness Rhat=F=0, all first-variation coefficients vanish. The flat uniform reduced action is identically unchanged.",
                   "TT":"With unperturbed N,u at this witness, F=0 identically for any metric, hence the pure-TT quadratic correction vanishes",
                   "auxiliary_velocities":"Q_ij=e^(2w)(bar hdot-Lie_shift bar h)_ij/(2N); the barred-variable operator has no Ndot or udot. Spatial IBP may differentiate metric velocity spatially but introduces no auxiliary time derivative.",
                   "IBP_scope":ibp["scope"]},
        "uniform":{"kinetic":str(red["uniform_kinetic"]),"scope":"Separate exactly uniform action; no k-divided constraint is inherited"},
        "limitations":["No nonlinear functional secondary-constraint closure or full DOF count",
                       "No all-channel physical causal-support or metric/Weyl reconstruction theorem",
                       "Matter perturbations, boundary conditions and rank-changing backgrounds remain unanalysed",
                       "The preserved static equations still need their clock-source matching and PPN solution",
                       "This constructed coefficient family is not a parameter prediction or empirical fit"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure",action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["checks_passed"]:
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
