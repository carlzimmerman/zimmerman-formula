#!/usr/bin/env python3
"""Uniform finite IC-2 horizon-band amplification; not full-theory closure.

The exact proof concerns each fixed k>0 with 0<x0<=x_star and all tau>=0,
tau=h(t-t0), p=dz/dtau. The norm is |z|+|p|/2, never a ratio through a
node of z. Numerical fundamental matrices are finite corroborating evidence.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform

# Cooperative numerical-library thread caps; no claim of OS CPU affinity.
for _thread_cap in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_thread_cap] = "1"

import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "scalar_completion.py"
PINNED_SOURCE_SHA256 = "801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745"


@lru_cache(None)
def derive():
    spec = importlib.util.spec_from_file_location("ic2_scalar_for_ir_growth", SOURCE)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    raw, repair = source.derive(), source.repair()
    x = raw["x"]
    d0 = s.Symbol("d0", positive=True)
    z, p = s.symbols("z p", real=True)
    a, g = [s.factor(repair[key].subs(raw["Tcal"],d0/8)) for key in ("a","g")]
    damping = s.factor(3-2*x*s.diff(a,x)/a)
    force = s.factor(g/a)
    # Integrate the actual rational force. There is no independently assumed
    # growth kernel: each partial-fraction term is integrated here.
    partial = s.apart(force/(4*x),x)
    primitive = sum(s.integrate(term,x) for term in s.Add.make_args(partial))
    Gamma = s.expand(primitive-primitive.subs(x,0),log=False)
    Gamma_stable = (-d0*s.log(1+x/d0)/18
                    +(4*d0-189)*s.log(1+x/(d0-54))/18-x/9)
    xstar = s.factor(repair["transition_x"].subs(raw["Tcal"],d0/8))
    d_exact = 8*repair["T_exact"]
    rho = s.factor(s.limit(force/x,x,0))
    denominator = (d0+x)*(d0+x-54)
    damping_square = (x+d0-81)**2+108*(d0-s.Rational(243,4))
    gap = s.Symbol("positive_gap",positive=True)
    xp = s.Symbol("positive_x",positive=True)
    # ell<4/5 gives d0>189/2; this stronger-than-needed bound is used
    # consistently in all coefficientwise positivity checks below.
    domain_sub = {d0:s.Rational(189,2)+gap,x:xp}
    damping_positive = s.factor(damping_square.subs(domain_sub))
    upper_difference = s.factor((rho-force/x).subs(domain_sub))

    sub = {raw["Tcal"]:d0/8,raw["zd"]:raw["h"]*p,raw["z"]:z}
    lapse = s.factor(repair["solutions"]["n"].subs(sub,simultaneous=True))
    aux = s.factor(repair["solutions"]["v"].subs(sub,simultaneous=True))
    physical_zeta = s.factor(z-lapse/3+aux/4)
    # Reuse the pinned Christoffel-derived Ricci tensor for the physical
    # conformal metric, including the actual physical background scale.
    ep = s.Symbol("eps",real=True)
    coord = s.Symbol("xcoord",real=True)
    zz = s.Symbol("physical_zeta",real=True)
    physical_scale = raw["B"]*s.exp(-s.Rational(1,12))
    physical_inverse = s.eye(3)*s.exp(-2*ep*zz*s.cos(raw["k"]*coord))/physical_scale**2
    physical_ricci = raw["ricci"].subs(raw["z"],zz)
    Hphys = raw["h"]*s.exp(-s.Rational(1,4))
    R3 = s.diff(s.trace(physical_inverse*physical_ricci),ep).subs(ep,0)
    R3 = s.factor(R3/(s.cos(raw["k"]*coord)*Hphys**2))
    R3 = s.factor(R3.subs(raw["k"]**2,x*raw["h"]**2*raw["B"]**2*s.exp(-s.Rational(2,3))))
    R3 = s.factor(R3.subs(zz,physical_zeta))
    observables = s.Matrix([lapse,aux,physical_zeta,R3])
    rows = observables.jacobian((z,p))

    tau, x0, W0, P0, bound = s.symbols("tau x0 W0 P0 bound",positive=True)
    velocity_envelope = s.exp(-2*tau)*(P0+rho*x0*bound*W0*tau)
    position_tail = s.exp(-2*tau)*(P0/2+rho*x0*bound*W0*(tau/2+s.Rational(1,4)))
    uniform_bound = s.exp(Gamma.subs(x,xstar))
    Cn = 1+27/d0
    Cv = s.Max(4*xstar/(d0+xstar),72/d0)
    residuals = {
        "damping_square":s.factor(denominator*(damping-2)-damping_square),
        "growth_primitive":s.factor(s.diff(Gamma,x)-force/(4*x)),
        "growth_origin":s.simplify(Gamma.subs(x,0)),
        "stable_growth_primitive":s.factor(s.diff(Gamma_stable-Gamma,x)),
        "stable_growth_origin":s.simplify((Gamma_stable-Gamma).subs(x,0)),
        "band_endpoint":s.simplify(force.subs(x,xstar)),
        "lapse_constraint":s.factor(lapse-p/2-3*aux/8),
        "auxiliary_constraint":s.factor(aux-(36*p-4*x*z)/(d0+x)),
        "physical_zeta":s.factor(physical_zeta-(2*d0+x)*z/(2*(d0+x))
                                 +(d0+x-27)*p/(6*(d0+x))),
        "physical_curvature":s.factor(R3-4*x*physical_zeta),
        "velocity_envelope":s.factor(s.diff(velocity_envelope,tau)+2*velocity_envelope
                                     -rho*x0*bound*W0*s.exp(-2*tau)),
        "position_tail":s.factor(s.diff(position_tail,tau)+velocity_envelope),
        "log_bound_origin":s.log(1),
    }
    # ln(1+y)<y follows by differentiating y-ln(1+y), with zero value at y=0.
    y = s.Symbol("y",positive=True)
    log_bound_derivative = s.factor(s.diff(y-s.log(1+y),y))
    d_lower = s.factor((8*raw["T_exact"]).subs(raw["ell"],s.Rational(4,5)))
    sign_checks = {
        "log_bound_derivative_positive":log_bound_derivative.is_positive,
        "d_lower_above_243_over_4":(d_lower-s.Rational(243,4)).is_positive,
        "damping_comparison_positive":damping_positive.is_positive,
        "force_linear_upper_bound_positive":upper_difference.is_positive,
    }
    return dict(x=x,d0=d0,z=z,p=p,a=a,g=g,damping=damping,force=force,
                Gamma=Gamma,Gamma_stable=Gamma_stable,rho=rho,d_exact=d_exact,x_star=xstar,
                x_star_numeric=float(xstar.subs(d0,d_exact)),
                uniform_bound=uniform_bound,
                uniform_bound_numeric=float(uniform_bound.subs(d0,d_exact).evalf(30)),
                damping_positive_expression=damping_positive,
                force_upper_difference=upper_difference,sign_checks=sign_checks,
                lapse=lapse,auxiliary=aux,physical_zeta=physical_zeta,
                physical_R3_over_H2=R3,observable_rows=rows,
                observable_bound_coefficients={"n":Cn,"v":Cv,"zeta_physical":1},
                velocity_envelope=velocity_envelope,position_tail=position_tail,
                residuals=residuals)


@lru_cache(None)
def _numeric_functions():
    d=derive()
    D=float(d["d_exact"])
    replacements={d["d0"]:D}
    fn=s.lambdify(d["x"],s.Matrix([d["damping"],d["force"],d["a"]]).subs(replacements),"numpy")
    rows=s.lambdify(d["x"],d["observable_rows"].subs(replacements),"numpy")
    # log1p evaluates the exact integrated expression stably near x=0.
    def Gamma(x):
        return -D*np.log1p(x/D)/18+(4*D-189)*np.log1p(x/(D-54))/18-x/9
    return fn,rows,Gamma


def fundamental(x0,tau_end=20.0,samples=801,rtol=1e-11,atol=1e-13,max_step=0.25):
    """Finite deterministic transfer; x0=0 is only the limiting-ODE control."""
    d=derive()
    if not np.isfinite(x0) or x0<0 or x0>d["x_star_numeric"]*(1+1e-14):
        raise ValueError("x0 must lie in [0,x_star]; zero is only an ODE control")
    if not np.isfinite(tau_end) or tau_end<=0 or samples<2:
        raise ValueError("A positive finite duration and at least two samples are required")
    fn,rows,Gamma=_numeric_functions()
    def rhs(tau,flat):
        beta,c,_=np.asarray(fn(x0*np.exp(-2*tau))).ravel()
        return (np.array([[0.,1.],[c,-beta]])@flat.reshape(2,2)).ravel()
    times=np.linspace(0,tau_end,samples)
    sol=solve_ivp(rhs,(0,tau_end),np.eye(2).ravel(),method="DOP853",t_eval=times,
                  rtol=rtol,atol=atol,max_step=max_step)
    if not sol.success:
        raise RuntimeError(sol.message)
    matrices=sol.y.T.reshape(-1,2,2)
    xs=x0*np.exp(-2*times)
    # Weighted induced 1-norm: S F S^-1, S=diag(1,1/2).
    weighted=matrices*np.array([[1.,2.],[0.5,1.]])
    transfer_norm=np.max(np.sum(np.abs(weighted),axis=1),axis=1)
    envelope=np.exp(Gamma(x0)-Gamma(xs))
    observable_transfer=np.array([np.max(np.abs(np.asarray(rows(xx))@F@np.diag([1.,2.])),axis=1)
                                  for xx,F in zip(xs,matrices)])
    early=times<=4
    a0=float(np.asarray(fn(x0)).ravel()[2])
    determinant_exact=np.array([np.exp(-3*t)*a0/float(np.asarray(fn(xx)).ravel()[2])
                                for t,xx in zip(times[early],xs[early])])
    wronskian_error=float(np.max(np.abs(np.linalg.det(matrices[early])-determinant_exact)))
    return dict(times=times,x=xs,matrices=matrices,weighted_transfer_norm=transfer_norm,
                envelope=envelope,observable_transfer=observable_transfer,
                early_wronskian_error=wronskian_error,nfev=sol.nfev,success=sol.success)


@lru_cache(None)
def numerical():
    d=derive()
    fractions=[1e-8,1e-4,0.01,0.1,0.25,0.5,0.75,1.0]
    cases=[]
    for fraction in fractions:
        x0=fraction*d["x_star_numeric"]
        coarse=fundamental(x0,rtol=1e-9,atol=1e-11,max_step=0.25)
        fine=fundamental(x0,rtol=1e-12,atol=1e-14,max_step=0.125)
        cases.append({
            "x0":x0,"fraction_of_band":fraction,
            "max_weighted_transfer_norm":float(np.max(fine["weighted_transfer_norm"])),
            "max_envelope_excess":float(np.max(fine["weighted_transfer_norm"]-fine["envelope"])),
            "max_refinement_difference":float(np.max(np.abs(coarse["matrices"]-fine["matrices"]))),
            "early_wronskian_error":fine["early_wronskian_error"],
            "final_fundamental_matrix":fine["matrices"][-1].tolist(),
            "observable_maxima":dict(zip(("n","v","zeta_physical","R3_over_H2"),
                                         np.max(fine["observable_transfer"],axis=0).tolist())),
            "nfev":[coarse["nfev"],fine["nfev"]],"success":bool(coarse["success"] and fine["success"]),
        })
    return {
        "method":"DOP853; fundamental matrix initialized to identity; no random sampling",
        "tau_interval":[0,20],"samples_per_case":801,
        "tolerances":[{"rtol":1e-9,"atol":1e-11,"max_step":0.25},
                      {"rtol":1e-12,"atol":1e-14,"max_step":0.125}],
        "cases":cases,"all_integrations_succeeded":all(c["success"] for c in cases),
        "max_weighted_transfer_norm":max(c["max_weighted_transfer_norm"] for c in cases),
        "max_refinement_difference":max(c["max_refinement_difference"] for c in cases),
        "max_envelope_excess":max(c["max_envelope_excess"] for c in cases),
        "max_early_wronskian_error":max(c["early_wronskian_error"] for c in cases),
        "scope":"Finite numerical corroboration only; determinant check restricted to tau<=4 to avoid late rank-one cancellation",
    }


def run():
    d,numeric=derive(),numerical()
    source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    exact=all(s.simplify(v)==0 for v in d["residuals"].values()) and all(d["sign_checks"].values())
    numerical_pass = (numeric["all_integrations_succeeded"]
                      and numeric["max_refinement_difference"]<1e-7
                      and numeric["max_envelope_excess"]<1e-7
                      and numeric["max_early_wronskian_error"]<1e-7)
    return {
        "model":"IC-2 uniform finite negative-frequency-band amplification",
        "source_file":"scalar_completion.py","source_sha256":source_hash,
        "input_hash_matches":source_hash==PINNED_SOURCE_SHA256,
        "arithmetic":"Exact symbolic identities and analytic differential inequalities; floating numerical corroboration separately labeled",
        "software":{"python":platform.python_version(),"sympy":s.__version__,"numpy":np.__version__,"scipy":scipy.__version__},
        "resource_scope":"Cooperative BLAS/OpenMP thread limits 1; small deterministic ODE; no OS affinity claim",
        "exact_checks_passed":bool(exact),"residuals":{k:str(v) for k,v in d["residuals"].items()},
        "numerical_consistency_passed":bool(numerical_pass),
        "sign_checks":{k:bool(v) for k,v in d["sign_checks"].items()},
        "domain":"Each fixed comoving k>0, 0<x0<=x_star, all future tau=h(t-t0)>=0, same exact expanding witness; no extra ordinary-matter perturbations",
        "state_norm":"W=|z|+|p|/2, p=dot(z)/h; arbitrary signed or complex amplitudes, no division by nodes",
        "coefficients":{"a":str(d["a"]),"damping":str(d["damping"]),"force":str(d["force"]),"rho":str(d["rho"])},
        "proof":{"Gamma":str(d["Gamma_stable"]),"x_star":str(d["x_star"]),
                 "uniform_factor":"exp(Gamma(x_star))","uniform_factor_approx":d["uniform_bound_numeric"],
                 "inequality":"W(tau)<=exp[Gamma(x0)-Gamma(x(tau))]W0<=exp[Gamma(x_star)]W0",
                 "velocity_bound":str(d["velocity_envelope"]),"position_tail_bound":str(d["position_tail"])},
        "physical_observables":{"n":str(d["lapse"]),"v":str(d["auxiliary"]),
                                "zeta_physical":str(d["physical_zeta"]),"R3_over_Hphys2":str(d["physical_R3_over_H2"]),
                                "bound_coefficients":{k:str(v) for k,v in d["observable_bound_coefficients"].items()},
                                "curvature_bound":"|delta R3/Hphys^2|<=4*x0*exp(-2*tau)*exp[Gamma(x_star)]*W0",
                                "gauge_scope":"n and v perturb background-constant physical scalars. R3 is the intrinsic scalar of the genuine-clock slices, whose background value is zero; not the four-dimensional Ricci scalar."},
        "numerical":numeric,"full_theory_closed":False,"physical_causality_proved":False,
        "remaining_gap":"A finite fixed-mode amplification bound is not a positivity-of-frequency theorem, observational fit, nonlinear estimate, extra-matter stability theorem, or physical domain-of-dependence theorem.",
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure",action="store_true")
    args=parser.parse_args()
    result=run()
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["exact_checks_passed"] or not result["input_hash_matches"]:
        return 1
    if not result["numerical_consistency_passed"]:
        return 1
    return 2 if args.require_full_closure else 0


if __name__=="__main__":
    raise SystemExit(main())
