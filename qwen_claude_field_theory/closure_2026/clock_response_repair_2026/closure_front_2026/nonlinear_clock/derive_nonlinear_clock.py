#!/usr/bin/env python3
"""Exact frozen clock elimination and bounded independent branch controls.

This is a flat, stationary, zero-clock-current reduction of the unchanged
action. It is not a metric solution, an on-shell cosmological construction,
or a physical MOND force calculation. No parameters are fitted.
"""
import argparse
import json
from pathlib import Path

import mpmath as mp
import sympy as S


def derive():
    checks = {}

    def check(name, expression):
        result = S.factor(S.cancel(S.simplify(expression)))
        if result != 0:
            raise AssertionError((name, result))
        checks[name] = True

    p, z, e = S.symbols("p z e", real=True)
    q = S.symbols("q", nonzero=True, real=True)
    d, ell, U, Delta = S.symbols("d ell U Delta", positive=True)
    Wc, lamX = S.symbols("Wc lambda_X", real=True)
    A, k, C = Wc-2*d*ell, q*q-ell, Wc-2*d*q*q
    s = S.sqrt(1-z*z)
    D = ell+p*p-2*p*q*z+k*z*z
    Y = (p-q*z)**2/(1-z*z)
    Q = (q-z*p)/s
    W = Wc+2*d*ell*(S.sqrt(1+Y/ell)-1)
    L = A*s+2*d*S.sqrt(ell)*S.sqrt(D)
    # Prove radicand identity; s>0 selects the positive square-root product.
    check("canonical_sW_radicand_identity", (1-z*z)*(1+Y/ell)-D/ell)
    J = -A*z/s+2*d*S.sqrt(ell)*(k*z-p*q)/S.sqrt(D)
    check("direct_action_clock_current", S.diff(L,z)-J)
    # Independent covariant-current construction, with W and W_Y in D form.
    W_D = Wc+2*d*ell*(S.sqrt(D)/(S.sqrt(ell)*s)-1)
    WY_D = d*S.sqrt(ell)*s/S.sqrt(D)
    Jr_cov = -z*W_D/s-2*Q*WY_D*(p-q*z)/(1-z*z)
    check("covariant_clock_current", J-Jr_cov)
    Fw = -d*S.sqrt(ell)*(p-q*z)/S.sqrt(D)
    check("envelope_partial_scalar_flux", Fw+S.diff(L,p)/2)
    check("joint_parity", L.xreplace({p:-p,z:-z})-L)
    check("clock_block_at_origin", S.diff(J,z).subs({p:0,z:0})+C)
    check("clock_mixing_at_origin", S.diff(J,p).subs({p:0,z:0})+2*d*q)
    quartic = S.expand(4*d*d*ell*(k*z-p*q)**2*(1-z*z)-A*A*z*z*D)
    check("squared_relation_quartic_degree", max(S.degree(quartic,z),4)-4)

    T = S.series(L.subs({p:e*p,z:e*z}),e,0,5).removeO().expand()
    L2, L4 = T.coeff(e,2), T.coeff(e,4)
    a = -2*d*q/C
    b = d*q*Wc**2*(Wc-2*d*ell)/(ell*C**4)
    H4 = -d*Wc*(Wc**3-8*Wc*d*d*ell*q*q+8*d**3*ell*q**4)/(4*ell*C**4)
    check("linear_clock_solution", S.diff(L2,z).subs(z,a*p))
    check("cubic_clock_solution", S.diff(L4,z).subs(z,a*p)-C*b*p**3)
    check("reduced_clock_quadratic", L2.subs(z,a*p)-d*Wc*p*p/C)
    check("reduced_clock_quartic", L4.subs(z,a*p)-H4*p**4)
    check("principal_schur_coefficient", -2*(-S.Symbol("PX")+d*Wc/C)-(2*S.Symbol("PX")-2*d*Wc/C))
    P = -U*S.log((Delta+2*d*p*p)/Delta)/2-lamX*p*p
    PT = S.series(P,p,0,7).removeO().expand()
    check("canonical_P_quadratic", PT.coeff(p,2)+U*d/Delta+lamX)
    check("canonical_P_quartic", PT.coeff(p,4)-U*d*d/Delta**2)
    check("canonical_P_sextic", PT.coeff(p,6)+4*U*d**3/(3*Delta**3))
    check("uncompleted_linear_cancellation", (U*d/Delta-d*Wc/C).subs(Wc,U).subs(Delta,U-2*d*q*q))
    # Completed histories are fixed inputs, not independent fitting parameters.
    lamW = S.symbols("lambda_W", real=True)
    full_linear = (U*d/Delta+lamX-d*Wc/C).subs(Wc,U+lamW)
    expected_linear = lamX+2*d*d*q*q*lamW/(Delta*(Delta+lamW))
    check("completed_linear_coefficient", (full_linear-expected_linear).subs(Delta,U-2*d*q*q))

    # Wc=0 gives an exact Y=0 alignment for |p|<|q|. Check algebra before roots.
    check("zero_Wc_exact_alignment_Y", Y.subs(z,p/q))
    check("zero_Wc_clock_current_covariant", (-z*S.Symbol("W")/s-2*Q*S.Symbol("WY")*(p-q*z)/(1-z*z)).subs({z:p/q,S.Symbol("W"):0}))
    check("zero_Wc_regular_linear_alignment", a.subs(Wc,0)-1/q)
    check("zero_Wc_cubic_alignment", b.subs(Wc,0))
    check("zero_Wc_reduced_quartic", H4.subs(Wc,0))
    check("zero_Wc_nonzero_clock_block", C.subs(Wc,0)+2*d*q*q)
    # A=0 exact branch, with k!=0 and timelike/domain exclusions stated separately.
    check("A_zero_exact_clock_numerator", (k*z-p*q).subs(z,p*q/k))
    check("A_zero_exact_reduced_radicand", D.subs(z,p*q/k)-ell*(1-p*p/k))
    check("A_zero_cubic_tilt_vanishes", b.subs(Wc,2*d*ell))

    # Critical C=0: use weights p~e^3,z~e, keeping through weight six.
    Lcrit = L.subs(Wc,2*d*q*q)
    TC = S.series(Lcrit.subs({p:e**3*p,z:e*z}),e,0,7).removeO().expand()
    LC4, LC6 = TC.coeff(e,4), TC.coeff(e,6)
    check("critical_weight4", LC4-(-2*d*q*p*z-d*k*q*q*z**4/(4*ell)))
    check("critical_weight6", LC6-(d*p*p+d*k*q*p*z**3/ell+d*k*q*q*(q*q-2*ell)*z**6/(8*ell**2)))
    ac, bc, t = S.symbols("a_c b_c t", nonzero=True, real=True)
    a3 = -2*ell/(k*q)

    def reduce_ac(expr):
        num, den = S.together(expr).as_numer_denom()
        return S.factor(S.rem(num,ac**3-a3,ac)/den)

    JC = S.diff(LC4+LC6,z).subs({p:t**3,z:ac*t+bc*t**3}).expand()
    check("critical_cuberoot_balance", reduce_ac(JC.coeff(t,3)))
    check("critical_next_tilt", reduce_ac(JC.coeff(t,5).subs(bc,q/(2*k))))
    eff4 = LC4.subs({p:1,z:ac})
    eff6 = LC6.subs({p:1,z:ac})
    check("critical_reduced_weight4", reduce_ac(eff4+S.Rational(3,2)*d*q*ac))
    check("critical_reduced_weight6", reduce_ac(eff6+d*q*q/(2*k)))
    # Derive the same critical flux directly from the exact envelope current.
    FT = S.series(Fw.subs({p:t**3,z:ac*t+q*t**3/(2*k)}),t,0,4).removeO().expand()
    check("critical_flux_cuberoot", FT.coeff(t,1)-d*q*ac)
    check("critical_flux_next_linear", reduce_ac(FT.coeff(t,3)-d*q*q/(2*k)))
    # Exceptional critical q^2=ell: its current never vanishes for p!=0.
    qpos = S.sqrt(ell)
    Jex = S.simplify(J.subs({q:qpos,Wc:2*d*ell}))
    check("exceptional_q2_ell_current", Jex+2*d*ell*p/S.sqrt(ell+p*p-2*qpos*p*z))
    check("critical_q_zero_current_at_z_zero", J.subs({q:0,Wc:0,z:0}))
    check("q_zero_regular_exact_z_zero", J.subs({q:0,z:0}))
    check("critical_q_zero_reduced_W", L.subs({q:0,Wc:0,z:0})-2*d*ell*(S.sqrt(1+p*p/ell)-1))

    formulae = {
        "D": str(D), "A": str(A), "C": str(C), "L_W": str(L),
        "J_tau_r": str(J), "F_W": str(Fw), "squared_quartic": str(quartic),
        "regular_z_linear": str(a), "regular_z_cubic": str(b),
        "regular_LW_quadratic": str(d*Wc/C), "regular_LW_quartic": str(H4),
        "regular_F_linear_completed": str(expected_linear),
        "regular_F_cubic": str(-2*(H4+U*d*d/Delta**2)),
        "critical_a_cubed": str(a3), "critical_z_next": str(q/(2*k)),
        "critical_LW_4over3": str(-S.Rational(3,2)*d*q*ac),
        "critical_LW_quadratic": str(-d*q*q/(2*k)),
        "critical_FW_cuberoot": str(d*q*ac), "critical_FW_linear": str(d*q*q/(2*k)),
    }
    return checks, formulae, (p,z,q,d,ell,Wc,quartic)


def branch_controls(symbols):
    """Compare certified rational polynomial isolation against unsquared roots.

    Polynomial intervals certify only squared roots. Evaluation of the
    unsquared relation and direct solve are floating controls, not interval
    proofs. Signs and domains are rechecked at both 60 and 90 decimal digits.
    """
    p,z,q,d,ell,Wc,quartic = symbols
    cases = [
        ("regular_positive_C",S.Rational(1,2),S.Integer(3)),
        ("regular_negative_C",S.Rational(1,2),S.Integer(1)),
        ("zero_Wc_alignment",S.Integer(2),S.Integer(0)),
        ("A_zero_exact",S.Integer(2),S.Integer(4)),
        ("critical_positive_k",S.Rational(1,2),S.Integer(2)),
        ("critical_negative_k",S.Integer(2),S.Integer(2)),
        ("critical_exceptional",S.Integer(1),S.Integer(2)),
    ]
    rows=[]
    for name,el,w in cases:
        for pv in [S.Rational(1,100),S.Rational(1,1000),S.Rational(1,10**6),S.Rational(-1,1000)]:
            poly=S.Poly(quartic.subs({d:1,q:1,ell:el,Wc:w,p:pv}),z)
            intervals=poly.intervals(eps=S.Rational(1,10**70))
            precision_runs=[]
            for digits in (60,90):
                with mp.workdps(digits):
                    def cast(x): return mp.mpf(str(S.N(x,digits)))
                    lval,wval,pval=map(cast,(el,w,pv))
                    kval=1-lval
                    Aval=wval-2*lval
                    def discr(x): return lval+pval*pval-2*pval*x+kval*x*x
                    def current(x):
                        return -Aval*x/mp.sqrt(1-x*x)+2*mp.sqrt(lval)*(kval*x-pval)/mp.sqrt(discr(x))
                    def flux(x): return -mp.sqrt(lval)*(pval-x)/mp.sqrt(discr(x))
                    accepted=[]
                    excluded=0
                    for (left,right),mult in intervals:
                        zr=cast((left+right)/2)
                        if abs(zr)>=1 or discr(zr)<=0:
                            excluded+=mult
                            continue
                        residual=abs(current(zr))
                        if residual<mp.mpf("1e-45"):
                            accepted.append((zr,mult))
                        else:
                            excluded+=mult
                    if name=="critical_exceptional":
                        assert not accepted
                        precision_runs.append({"digits":digits,"admissible_unsquared_roots":0,"excluded_squared_multiplicity":excluded})
                        continue
                    if w!=2:
                        aa=-mp.mpf(2)/(wval-2)
                        bb=wval*wval*(wval-2*lval)/(lval*(wval-2)**4)
                        approx=aa*pval+bb*pval**3
                    else:
                        aa=mp.sign(-2*lval/kval)*abs(-2*lval/kval)**(mp.mpf(1)/3)
                        approx=aa*mp.sign(pval)*abs(pval)**(mp.mpf(1)/3)+pval/(2*kval)
                    assert accepted, (name,pv,"no admissible root")
                    zr,mult=min(accepted,key=lambda pair:abs(pair[0]-approx))
                    # Direct unsquared nonlinear solve from an independently
                    # derived asymptotic predictor, not the isolated root.
                    direct=mp.findroot(current,(approx*mp.mpf(".97"),approx*mp.mpf("1.03")),solver="secant",tol=mp.mpf("1e-50"),verify=True)
                    assert abs(direct-zr)<mp.mpf("1e-44")
                    assert abs(zr)<1 and discr(zr)>0 and 3+2*pval*pval>0
                    assert abs(current(direct))<mp.mpf("1e-45")
                    # Envelope identity checked independently by solving the
                    # clock equation at neighboring p in arbitrary precision.
                    def stationary_L(pp):
                        def dd(x): return lval+pp*pp-2*pp*x+kval*x*x
                        def jj(x): return -Aval*x/mp.sqrt(1-x*x)+2*mp.sqrt(lval)*(kval*x-pp)/mp.sqrt(dd(x))
                        zz=mp.findroot(jj,(direct*mp.mpf(".999"),direct*mp.mpf("1.001")),tol=mp.mpf("1e-50"))
                        return Aval*mp.sqrt(1-zz*zz)+2*mp.sqrt(lval)*mp.sqrt(dd(zz))
                    step=mp.mpf("1e-14")*abs(pval)
                    fd=-(stationary_L(pval+step)-stationary_L(pval-step))/(4*step)
                    assert abs(fd-flux(zr))<mp.mpf("1e-22")*max(1,abs(flux(zr)))
                    if name=="zero_Wc_alignment": assert abs(zr-pval)<mp.mpf("1e-45")
                    if name=="A_zero_exact": assert abs(zr-pval/kval)<mp.mpf("1e-45")
                    precision_runs.append({
                        "digits":digits,"admissible_unsquared_roots":len(accepted),
                        "excluded_squared_multiplicity":excluded,
                        "selected_z":mp.nstr(zr,35),"selected_F_W":mp.nstr(flux(zr),35),
                        "direct_vs_isolated_error":mp.nstr(abs(direct-zr),5),
                        "asymptotic_tilt_error":mp.nstr(abs(zr-approx),12),
                        "current_residual":mp.nstr(abs(current(zr)),5),
                        "envelope_difference_error":mp.nstr(abs(fd-flux(zr)),5),
                        "timelike_margin":mp.nstr(1-zr*zr,20),
                        "log_numerator":mp.nstr(3+2*pval*pval,20),
                    })
            assert precision_runs[0]["admissible_unsquared_roots"]==precision_runs[1]["admissible_unsquared_roots"]
            if name!="critical_exceptional":
                with mp.workdps(50):
                    assert abs(mp.mpf(precision_runs[0]["selected_z"])-mp.mpf(precision_runs[1]["selected_z"]))<mp.mpf("1e-33")
            rows.append({"case":name,"d":"1","q":"1","ell":str(el),"Wc":str(w),"U_log_control":"5","p":str(pv),"precision_runs":precision_runs})
    return rows


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    checks,formulae,symbols=derive()
    rows=branch_controls(symbols)
    result={
        "scope":"Frozen flat radial zero-clock-current reduction; unchanged canonical action; no metric or full PDE certification",
        "symbolic_checks":checks,"symbolic_check_count":len(checks),"formulae":formulae,
        "branch_controls":rows,"branch_parameter_cases":len(rows),
        "precision_digits":[60,90],"randomness_used":False,
        "residual_risks":["Numerical unsquared-root filtering is not an interval proof.","The zero radial clock current is a regular-center boundary choice in the frozen stationary problem.","Wc=U+lambda_W uses the fixed canonical history; sampled Wc cases are algebraic controls, not demonstrated cosmological solutions.","Clock-critical C=0 is distinct from metric-reduced G=0.","No physical metric force, all-background stability, full constraint rank, or exact MOND law is inferred."],
    }
    serialized=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.write_text(serialized)
    print(json.dumps({"symbolic_check_count":len(checks),"branch_parameter_cases":len(rows),"precision_digits":[60,90],"result":"all stated finite checks passed","formulae":formulae},indent=2,sort_keys=True))


if __name__=="__main__":
    main()
