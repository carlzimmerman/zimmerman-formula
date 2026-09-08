#!/usr/bin/env python3
"""IC-4: action-derived healthy local scalar wave on one exact FLRW branch.

This is a new action revision, not a reassignment of IC-2's results. The
curvature coupling is varied before its coefficients are solved. The domain
is the pinned flat expanding witness, linear scalar perturbations, k>0, no
additional ordinary-matter perturbations. Nonlinear constraints, matching to
galaxies, all-background characteristics and PPN remain unproved.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

SOURCE = Path(__file__).with_name("scalar_completion.py")
SOURCE_HASH = "801e50f8a3485842eec9bafd58d4f652c42200050917da6d9f0360aea5ff7745"


@lru_cache(None)
def derive():
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_HASH:
        raise RuntimeError("The pinned input changed; rederive and reaudit before reuse")
    spec = importlib.util.spec_from_file_location("ic4_pinned_scalar", SOURCE)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    raw = source.derive()
    m, B, h, k, ell, T, x, z, n, v = [raw[q] for q in
        ("m", "B", "h", "k", "ell", "Tcal", "x", "z", "n", "v")]
    ep, coord = s.symbols("eps xcoord", real=True)
    y, shift, p, q = s.symbols("y shift_scaled p_R q_R", real=True)
    Ac, Bc = s.symbols("A_curvature B_curvature", real=True)
    sigma = s.Symbol("sigma", positive=True)
    C, S = s.cos(k*coord), s.sin(k*coord)
    xi, u = s.Rational(1,4)+ep*n*C, s.Rational(2,3)+ep*v*C
    w = (u-1)*xi
    bar_scale = B*s.exp(ep*z*C)
    Rbar = s.trace(raw["ricci"])/bar_scale**2
    # Q is the actual trace of the barred metric velocity numerator / lapse.
    Q = s.trace(raw["Knum"])*s.exp(-xi)
    f = s.exp(-s.Rational(1,2))
    a0sq = 27*h*h*f/(8*ell*ell)
    coupling = Ac*(xi-s.Rational(1,4))+Bc*(u-s.Rational(2,3))
    density = m*s.exp(xi)*bar_scale**3*s.exp(3*w)*Q**2/a0sq*s.exp(-2*w)*Rbar*coupling/2
    jet = s.expand(s.diff(density, ep, 2).subs(ep,0))
    averaged = jet.subs({C*C:s.Rational(1,2),S*S:s.Rational(1,2),C*S:0}).subs({C:0,S:0})
    correction = s.factor(averaged/(m*f*B**3*h*h))
    correction = s.factor(correction.subs(k*k,x*h*h*B*B*s.exp(-s.Rational(2,3))))
    factor = s.factor(s.diff(correction,z,n)/Ac/x)
    density_residual = s.factor(correction-factor*x*z*(Ac*n+Bc*v))

    # Rank-one spatial coefficients are a solved constructive family from the
    # preceding checkpoint. No matrix rank or physical count is used as input.
    e = s.Rational(1,8)
    alpha, d = 81*e/T**2, -9*e/T
    beta = s.factor(2*d-s.Rational(1,3)-3*alpha/4)
    gamma = s.factor(e-s.Rational(1,16)+9*alpha/64-3*d/4)
    jselect = {raw["alpha"]:alpha,raw["beta"]:beta,raw["gamma"]:gamma}
    L = s.expand(raw["L"].subs(jselect).subs({raw["zd"]:h*y,raw["shift"]:h*shift/k})/h**2)
    L += correction.subs({Ac:p/factor,Bc:q/factor})
    fields = (n,v,shift)
    equations = [s.diff(L,a) for a in fields]
    matrix, rhs = s.linear_eq_to_matrix(equations,fields)
    sol = dict(zip(fields,(matrix.inv()*rhs).applyfunc(s.factor)))
    # First demand no position-source inverse in the physical auxiliary u.
    q_choice = s.solve(s.together(s.diff(sol[v],z)).as_numer_denom()[0],q)[0]
    Lq = s.factor(L.subs(q,q_choice))
    solq = {a:s.factor(b.subs(q,q_choice)) for a,b in sol.items()}
    reducedq = s.factor(Lq.subs(solq,simultaneous=True))
    aq = s.factor(s.diff(reducedq,y,2)/2)
    bq = s.factor(s.diff(reducedq,z,y))
    cq = s.factor(s.diff(reducedq,z,2)/2)
    gq = s.factor(cq-3*bq/2+x*s.diff(bq,x))
    # sigma is a stated design parameter; the resulting speed is subsequently
    # derived from the corrected action, not inserted into the output.
    p_choice = s.solve(s.Eq(gq,-aq*sigma*x),p)[0]
    q_choice = s.factor(q_choice.subs(p,p_choice))
    selected = {p:p_choice,q:q_choice}
    Lfixed = s.factor(L.subs(selected,simultaneous=True))
    solved = {a:s.factor(b.subs(selected,simultaneous=True)) for a,b in sol.items()}
    reduced = s.factor(Lfixed.subs(solved,simultaneous=True))
    a = s.factor(s.diff(reduced,y,2)/2)
    b = s.factor(s.diff(reduced,z,y))
    c = s.factor(s.diff(reduced,z,2)/2)
    g = s.factor(c-3*b/2+x*s.diff(b,x))
    friction = s.factor(3-2*x*s.diff(a,x)/a)
    force = s.factor(g/a)
    constraints = [s.factor(s.diff(Lfixed,j).subs(solved,simultaneous=True)) for j in fields]
    physical_scale = B*s.exp(-s.Rational(1,12))
    lapse0 = s.exp(s.Rational(1,4))
    speed = s.factor((-h*h*g/a)*physical_scale**2/(lapse0**2*k*k))
    speed = s.factor(speed.subs(k*k,x*h*h*B*B*s.exp(-s.Rational(2,3))))

    # Momentum includes the b*z cross term; do not falsely identify velocity
    # locality with locality in constrained canonical initial data.
    P = s.Symbol("P_normalized",real=True)
    y_from_P = s.solve(s.Eq(s.diff(reduced,y),P),y)[0]
    readouts = {"n":solved[n],"v":solved[v],
                "zeta_physical":z-solved[n]/3+solved[v]/4}
    canonical = {j:s.factor(expr.subs(y,y_from_P)) for j,expr in readouts.items()}
    local = {j:not s.cancel(expr).as_numer_denom()[1].has(x) for j,expr in canonical.items()}
    def Dt(expr):
        return s.factor(-2*x*s.diff(expr,x)+y*s.diff(expr,z)
                        +(-friction*y+force*z)*s.diff(expr,y))
    clock_residual = s.factor(Dt(Dt(solved[n]))+5*Dt(solved[n])+(6+sigma*x)*solved[n])
    energy = (y*y+sigma*x*z*z)/2
    energy_residual = s.factor(Dt(energy)+3*y*y+sigma*x*z*z)
    zero_a = raw["zero_mode_kinetic"]
    zero_n = s.factor(raw["zero_mode_solutions"][n].subs(raw["zd"],h*y))
    zero_v = s.factor(raw["zero_mode_solutions"][v].subs(raw["zd"],h*y))
    zero_n_match = s.factor(zero_n.subs(y,P/(2*zero_a))-canonical["n"].subs(x,0))
    zero_v_match = s.factor(zero_v.subs(y,P/(2*zero_a))-canonical["v"].subs(x,0))
    # Product-jet checks transfer only the explicitly stated branches.
    Qj,Rj,fj = s.symbols("Q_jet R_jet f_jet",real=True)
    product = Qj**2*Rj*fj
    bridges = {"static_action":product.subs(Qj,0)}
    for j in (Qj,Rj,fj):
        bridges["static_variation_"+str(j)] = s.diff(product,j).subs(Qj,0)
        bridges["witness_variation_"+str(j)] = s.diff(product,j).subs({Rj:0,fj:0})
    bridges["homogeneous_reduction"] = product.subs(Rj,0)
    bridges["pure_TT_correction"] = correction.subs({n:0,v:0})
    gap = s.Symbol("positive_T_gap",positive=True)
    apos = s.factor(a.subs(T,s.Rational(27,4)+gap))
    lower = s.factor((raw["T_exact"]-s.Rational(27,4)).subs(ell,s.Rational(4,5)))
    # r=sqrt(sigma*x) obeys r'=-r; these are independent elementary solutions.
    r = s.Symbol("r",positive=True)
    mode_functions = [s.cos(r)+r*s.sin(r),s.sin(r)-r*s.cos(r)]
    mode_residuals = [s.simplify(r*r*s.diff(j,r,2)-2*r*s.diff(j,r)+r*r*j) for j in mode_functions]
    # Construct compact physical wave packets without reconstructing a shift
    # by an inverse Laplacian. This is a restricted Cauchy-data construction,
    # not an assertion that every nonlinear constrained datum admits this map.
    Uwave, Ud = s.symbols("U_wave U_wave_prime",real=True)
    Uprime = Dt(y/x)
    z_packet = s.factor(s.solve(s.Eq(Uprime.subs(y,x*Uwave),Ud),z)[0])
    packet_sub = {z:z_packet,y:x*Uwave}
    packet_readouts = {j:s.factor(expr.subs(packet_sub,simultaneous=True)) for j,expr in readouts.items()}
    packet_readouts["shift_potential_scaled"] = s.factor((solved[shift]/x).subs(packet_sub,simultaneous=True))
    packet_readouts["trace_momentum_normalized"] = s.factor(s.diff(reduced,y).subs(packet_sub,simultaneous=True))
    packet_residuals = {
        "potential_wave":s.factor(Dt(Uprime)+Uprime+sigma*x*(y/x)),
        "potential_first_equation":s.factor(Uprime+y/x+sigma*z),
        "z_reconstruction":s.factor(z_packet+(Ud+Uwave)/sigma),
        "z_derivative_reconstruction":s.factor(-2*x*s.diff(z_packet,x)+Ud*s.diff(z_packet,Uwave)
                                                +(-Ud-sigma*x*Uwave)*s.diff(z_packet,Ud)-x*Uwave),
        "shift_momentum_identity":s.factor(solved[shift]-s.diff(reduced,y)/2),
        "packet_trace_momentum":s.factor(packet_readouts["trace_momentum_normalized"]
                                          -2*x*packet_readouts["shift_potential_scaled"]),
    }
    packet_local = {j:not s.cancel(expr).as_numer_denom()[1].has(x) for j,expr in packet_readouts.items()}
    packet = {"readouts":packet_readouts,"residuals":packet_residuals,"differential_readouts":packet_local}
    coefficients = {"A_J":3*alpha/(4*ell*ell),"B_J":3*beta/(4*ell*ell),
                    "C_J":3*gamma/(4*ell*ell),"A_curvature":p_choice/factor,
                    "B_curvature":q_choice/factor}
    return dict(raw=raw,T=T,x=x,ell=ell,z=z,y=y,n=n,v=v,P=P,
                target_speed_squared=sigma,coupling_factor=factor,density_residual=density_residual,
                correction=correction,selected_p=p_choice,selected_q=q_choice,
                action_coefficients=coefficients,L=Lfixed,solutions=solved,
                constraint_residuals=constraints,constraint_matrix=matrix.subs(selected,simultaneous=True),
                a=a,b=b,c=c,g=g,friction=friction,physical_speed_squared=speed,
                kinetic_positive=bool(apos.is_positive and lower.is_positive),
                canonical_readouts=canonical,canonical_readouts_local=local,
                clock_wave_residual=clock_residual,energy_residual=energy_residual,
                zero_a=zero_a,zero_n=zero_n,zero_v=zero_v,
                zero_lapse_canonical_match=zero_n_match,zero_aux_canonical_match=zero_v_match,
                bridge_residuals=bridges,mode_function_residuals=mode_residuals,
                mode_functions=mode_functions,packet=packet)


@lru_cache(None)
def numerical():
    d = derive()
    selected_speed = float(d["physical_speed_squared"].subs(d["target_speed_squared"],s.Rational(1,3)))
    cases = []
    times = np.linspace(0,6,241)
    for x0 in (1e-4,1.,100.,10000.):
        def rhs(tau,flat):
            return (np.array([[0.,1.],[-selected_speed*x0*np.exp(-2*tau),-3.]])@flat.reshape(2,2)).ravel()
        runs = [solve_ivp(rhs,(0.,6.),np.eye(2).ravel(),method="DOP853",t_eval=times,
                          rtol=rtol,atol=atol,max_step=step)
                for rtol,atol,step in ((1e-9,1e-11,0.1),(1e-12,1e-14,0.05))]
        if not all(result.success for result in runs):
            raise RuntimeError("Scalar-wave integration did not finish")
        coarse,fine = [result.y.T.reshape(-1,2,2) for result in runs]
        with mp.workdps(60):
            r0 = mp.sqrt(mp.mpf(str(selected_speed))*mp.mpf(str(x0)))
            def basis(r):
                return mp.matrix([[mp.cos(r)+r*mp.sin(r),mp.sin(r)-r*mp.cos(r)],
                                  [-r*r*mp.cos(r),-r*r*mp.sin(r)]])
            inverse = basis(r0)**-1
            exact = np.array([[[float(t) for t in row] for row in (basis(r0*mp.exp(-float(time)))*inverse).tolist()]
                              for time in times])
        scale = np.maximum(1.,np.abs(exact))
        energy = (fine[:,1,:]**2+selected_speed*x0*np.exp(-2*times)[:,None]*fine[:,0,:]**2)/2
        energy_increase = np.max(np.maximum(0.,np.diff(energy,axis=0))/energy[0,:])
        cases.append({"x0":x0,"scaled_analytic_error":float(np.max(np.abs(fine-exact)/scale)),
                      "scaled_refinement_error":float(np.max(np.abs(fine-coarse)/scale)),
                      "relative_energy_increase":float(energy_increase),
                      "final_transfer":fine[-1].tolist(),"nfev":[j.nfev for j in runs]})
    return {"physical_speed_squared":selected_speed,"tau_interval":[0.,6.],"samples":len(times),
            "all_integrations_succeeded":True,"cases":cases,
            "maximum_scaled_analytic_error":max(j["scaled_analytic_error"] for j in cases),
            "maximum_scaled_refinement_error":max(j["scaled_refinement_error"] for j in cases),
            "maximum_relative_energy_increase":max(j["relative_energy_increase"] for j in cases),
            "scope":"Finite transfer check at four x0 values; exact mode formulas evaluated at 60 decimal digits"}


def run():
    d, numeric = derive(),numerical()
    checks = {"density":d["density_residual"],"clock_wave":d["clock_wave_residual"],
              "energy":d["energy_residual"],"zero_lapse_canonical_match":d["zero_lapse_canonical_match"],
              "zero_aux_canonical_match":d["zero_aux_canonical_match"],
              "kinetic_independent_of_x":s.diff(d["a"],d["x"]),
              "full_frequency_matching":s.factor(d["g"]+d["a"]*d["target_speed_squared"]*d["x"]),
              "physical_speed_matching":s.factor(d["physical_speed_squared"]-d["target_speed_squared"]),
              "friction_matching":s.factor(d["friction"]-3),**d["bridge_residuals"]}
    checks.update({"constraint_"+str(i):v for i,v in enumerate(d["constraint_residuals"])})
    checks.update({"exact_mode_"+str(i):v for i,v in enumerate(d["mode_function_residuals"])})
    checks.update({"packet_"+k:v for k,v in d["packet"]["residuals"].items()})
    return {"candidate":"IC-4 local scalar-wave construction", "base":"0a9f9fa33",
            "source_sha256":SOURCE_HASH,"status":"OPEN","full_theory_closed":False,
            "domain":"Same flat expanding witness; k>0 linear scalar sector without extra matter; 0<sigma<=1",
            "action":"S_IC1+(m/2)integral sqrt(-g) Q^2/a0^2 [J+Rhat*(A_curvature*(lnN-1/4)+B_curvature*(u-2/3))]; Rhat=exp(-2w)*R[bar h]",
            "action_coefficients":{k:str(v) for k,v in d["action_coefficients"].items()},
            "constant_definitions":"ell=ln(9/5); Tcal=-27/16+54/(5ell); one explicit witness selects sigma=1/3",
            "software":{"python":platform.python_version(),"sympy":s.__version__,"numpy":np.__version__,"scipy":scipy.__version__,"mpmath":mp.__version__},
            "exact_checks_passed":all(s.simplify(v)==0 for v in checks.values()),
            "exact_residuals":{k:str(v) for k,v in checks.items()},
            "scalar":{"a":str(d["a"]),"b":str(d["b"]),"c":str(d["c"]),"g":str(d["g"]),
                      "positive_kinetic":d["kinetic_positive"],"physical_speed_squared":str(d["physical_speed_squared"]),
                      "equation":"z''+3z'+sigma*x*z=0; x'=-2x, tau=h*t",
                      "clock_equation":"n''+5n'+(6+sigma*x)*n=0; delta X_clock=-exp(-1/2)*n",
                      "energy_identity":"E=(y^2+sigma*x*z^2)/2; E'=-3y^2-sigma*x*z^2",
                      "canonical_readouts":{k:str(v) for k,v in d["canonical_readouts"].items()},
                      "canonical_readouts_local":d["canonical_readouts_local"]},
            "zero_mode":{"a":str(d["zero_a"]),"n":str(d["zero_n"]),"v":str(d["zero_v"]),
                         "warning":"Not equal to k->0 kinetic coefficient. Canonical n/v readouts match; global initial-data spaces still require separate treatment."},
            "physical_wave_packets":{
                "potential":"U_wave=y/x; U_wave''+U_wave'+sigma*x*U_wave=0 for k>0",
                "readouts":{k:str(v) for k,v in d["packet"]["readouts"].items()},
                "differential_readouts":d["packet"]["differential_readouts"],
                "shift_conversion":"N^i=-(N0^2/(h*A_physical^2))*partial_i(shift_potential_scaled)",
                "domain":"Flat R3, smooth compact initial U_wave,U_wave_prime; no homogeneous change or extra matter; exact linearized equations",
                "support":"Local damped-wave evolution followed only by spatial/time differentiation constructs finite-support physical metric scalar packets. No assertion about arbitrary global or nonlinear Cauchy data."},
            "numerical":numeric,
            "open_obligations":["Full nonlinear Dirac closure and separately justified clock classification",
                                "Physical initial-data lift and all-background characteristic/strong-coupling analysis",
                                "Static galactic embedding and independent metric/PPN calculations",
                                "y=0 branch control and ordinary-matter realistic cosmology",
                                "No empirical validation or global novelty claim in this computation"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-full-closure",action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(json.dumps(result,indent=2,sort_keys=True))
    numerical_ok = (result["numerical"]["maximum_scaled_analytic_error"]<1e-7
                    and result["numerical"]["maximum_scaled_refinement_error"]<1e-7
                    and result["numerical"]["maximum_relative_energy_increase"]<1e-8)
    if (not result["exact_checks_passed"] or not result["scalar"]["positive_kinetic"]
            or not all(result["scalar"]["canonical_readouts_local"].values())
            or not all(result["physical_wave_packets"]["differential_readouts"].values()) or not numerical_ok):
        return 1
    return 2 if args.require_full_closure else 0


if __name__ == "__main__":
    raise SystemExit(main())
