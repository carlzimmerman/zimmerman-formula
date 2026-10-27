#!/usr/bin/env python3
"""FSP-002/B: exact checks of a specified shared-scalar EFT truncation.

Run from repository root with --output DIRECTORY. No alpha data or fitted
coefficient is imported. Symbolic identities are over positive real parameters.
The script checks identities; the report supplies their physical interpretation.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    checks = {}

    def zero(name, expr):
        value = s.simplify(expr)
        checks[name] = {"passed": value == 0, "residual": str(value)}
        assert value == 0, (name, value)

    x, B0, beta, a, p, C, MU, CN, y, kg, n, ne, rho0 = s.symbols(
        "x B0 beta a p C MU CN y kg n ne rho0", positive=True
    )
    B = B0 + beta*x**2/2
    Lam = MU*s.exp(-a*B)
    mN = CN*Lam
    me = y*MU*s.exp(-p*B)
    Vq = -C*Lam**4
    Vm = n*mN + ne*me
    alpha = 1/(4*s.pi*kg*B)
    zero("common_extremum_vacuum_stationary", s.diff(Vq, x).subs(x, 0))
    zero("common_extremum_mass_stationary", s.diff(mN, x).subs(x, 0))
    zero("common_extremum_alpha_stationary", s.diff(alpha, x).subs(x, 0))
    zero("qcd_curvature", s.diff(Vq,x,2).subs(x,0)
         - 4*a*beta*C*MU**4*s.exp(-4*a*B0))
    zero("matter_curvature", s.diff(Vm,x,2).subs(x,0)
         + beta*(a*n*CN*MU*s.exp(-a*B0)+p*ne*y*MU*s.exp(-p*B0)))

    # Independent hand differentiation in B, then the chain rule at B'=0.
    u = s.symbols("u", real=True)
    VB = -C*MU**4*s.exp(-4*a*u)+n*CN*MU*s.exp(-a*u)+ne*y*MU*s.exp(-p*u)
    zero("curvature_chain_rule_crosscheck", s.diff(Vq+Vm,x,2).subs(x,0)
         -beta*s.diff(VB,u).subs(u,B0))

    # Rank test in coordinates (B0, log MU, log y, rho0). r=me/mN>0,
    # Q=C Lambda^4>0, w=mN/(mN+me)=1/(1+r).
    r,Q=s.symbols("r Q",positive=True)
    w=1/(1+r)
    J=s.Matrix([[-a,1,0,0],
                [1/B0-(a-p)*w,0,-w,0],
                [4*a*Q,-4*Q,0,1]])
    v=s.Matrix([1,a,(1+r)/B0-(a-p),0])
    for i,entry in enumerate(J*v):
        zero("universal_kernel_%d"%i,entry)
    # Nonzero minor proves rank=3 on the whole stated positive domain.
    minor=J[:,[1,2,3]].det()
    zero("rank3_minor",minor+w)
    zero("alpha_changes_on_kernel",s.Matrix([[-1/B0,0,0,0]]).dot(v)+1/B0)
    J_fixed=J.col_join(s.Matrix([[0,1,0,0]]))
    fixed_det=s.factor(J_fixed.det())
    zero("fixed_physical_threshold_full_rank",fixed_det-a*w)

    # Finite counterfamily, not merely a first-order tangent. These are a
    # common physical matching threshold and Yukawa amplitude varied between
    # models, never a renormalization-scale change inside one matched theory.
    M,R,t=s.symbols("M R t",positive=True)
    MUt=M*s.exp(a*t)/CN
    yt=CN*s.exp(-(a-p)*t)/(R/(4*s.pi*kg*t)-1)
    mNt=CN*MUt*s.exp(-a*t)
    met=yt*MUt*s.exp(-p*t)
    Rt=4*s.pi*kg*t*(1+mNt/met)
    zero("family_baryon_mass_fixed",mNt-M)
    zero("family_atomic_product_fixed",Rt-R)
    zero("family_qcd_vacuum_fixed",(-C*(MUt*s.exp(-a*t))**4)+C*(M/CN)**4)
    zero("family_qcd_scalar_profile_fixed",
         (MUt*s.exp(-a*(t+beta*x**2/2)))-(M/CN)*s.exp(-a*beta*x**2/2))

    # A different actual stationarity selector: competition of a positive
    # runaway with a negative matched QCD condensate term.
    A,L=s.symbols("A L",positive=True)
    V=rho0+A*s.exp(-p*x)-C*L**4*s.exp(-4*a*x)
    xs=s.log(p*A/(4*a*C*L**4))/(p-4*a)
    # Use stationarity pX=4aY to avoid branch-sensitive power simplification.
    X,Y=s.symbols("X Y",positive=True)
    zero("runaway_stationary_equation",(-p*X+4*a*Y).subs(Y,p*X/(4*a)))
    zero("runaway_curvature",(p**2*X-16*a**2*Y).subs(Y,p*X/(4*a))-p*(p-4*a)*X)
    zero("runaway_energy",(X-Y).subs(Y,p*X/(4*a))-(1-p/(4*a))*X)
    # Orthogonal check at an exact finite stationary point x=0.
    A0=4*a*C*L**4/p
    zero("runaway_direct_stationary",s.diff(V,x).subs({x:0,A:A0}))
    zero("runaway_direct_curvature",s.diff(V,x,2).subs({x:0,A:A0})-4*a*(p-4*a)*C*L**4)

    # Leading atom R=mN/(alpha*mu_red). Reduced mass is essential.
    m_e,m_N,z=s.symbols("m_e m_N z",positive=True)
    mu=m_e*m_N/(m_e+m_N)
    R_atom=s.simplify(m_N/(z*mu))
    zero("reduced_mass_atomic_product",R_atom-(1+m_N/m_e)/z)
    de,dg,dal=s.symbols("de dg dal",real=True)
    logvariation=-dal-(de-dg)/(1+r)
    zero("atomic_log_derivative",
         (-dal + (m_e*s.diff(s.log(R_atom),m_e)*de
                    +m_N*s.diff(s.log(R_atom),m_N)*dg)).subs(m_e,r*m_N)-logvariation)

    result={
      "claim_id":"FSP002_B_SHARED_SCALAR",
      "assertion_tested":"Exact symbolic stationary-point, reduced-mass, finite-family, and Jacobian identities in the declared leading EFT truncation",
      "checks":checks,
      "check_count":len(checks),
      "all_passed":all(v["passed"] for v in checks.values()),
      "rank3_minor":str(s.factor(minor)),
      "fixed_threshold_determinant":str(fixed_det),
      "kernel_coordinates":[str(q) for q in v],
      "log_alpha_change_on_kernel":str(-1/B0),
      "finite_family_domain":"0 < t < R/(4*pi*kg), restricted further to any common perturbative EFT window",
      "runaway_stationary_x":str(xs),
      "runaway_stable_condition":"p > 4*a, for a,p,A,C,L positive and p != 4*a",
      "runaway_vacuum_energy_minus_rho0":"(1-p/(4*a))*X < 0 on stable branch",
      "non_claims":["No alpha(0) value derived", "No full SM or quantum-gravity completion", "No all-orders uniqueness theorem", "No claim that the canonical framework contains these interactions", "QCD vacuum coefficient is a matched candidate datum"]
    }
    (out/"results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":len(checks),"all_passed":result["all_passed"],"rank3_minor":str(minor),"fixed_threshold_determinant":str(fixed_det)},indent=2))


if __name__=="__main__":
    main()
