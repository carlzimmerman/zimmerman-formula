#!/usr/bin/env python3
"""Frozen EINSTEIN-JOIN-1: exact identities/bounds plus eight bounded IVPs.

The contraction proof is in PROOF.md. Floating IVPs illustrate it and do not
certify an interval enclosure, a spectrum, or the Einstein initial-value PDE.
"""
import argparse
import hashlib
import json
import math
import platform
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
import sympy as sp
from scipy.integrate import solve_ivp, quad

HERE = Path(__file__).resolve().parent
CHECKS = []


def check(name, value):
    assert bool(value), name
    CHECKS.append(name)


def exact_checks():
    E, d0, D = sp.symbols("E d0 D", positive=True)
    Le = d0 * E - d0**2 * sp.log(1 + E/d0)
    check("electric derivative D(E)", sp.simplify(sp.diff(Le, E)-E/(1+E/d0)) == 0)
    H = d0**2*(-D/d0-sp.log(1-D/d0))
    Ein = D/(1-D/d0)
    # Substitute the physical positive-E chart D=d0 E/(d0+E), so logarithm
    # simplification does not silently assume an unphysical D>d0 branch.
    legendre=(D*E-Le-H).subs(D,d0*E/(d0+E))
    check("Legendre energy", sp.simplify(sp.expand_log(legendre,force=True)) == 0)
    check("Hamiltonian derivative", sp.simplify(sp.diff(H, D)-Ein) == 0)
    check("phase energy derivative", sp.simplify(sp.diff(H-D**2/2, D)-(Ein-D)) == 0)
    # Metric variation of the actual normalized static current frame.  j^t is
    # fixed as a vector density, U^t=1/a and E=f/(a*b).  beta B^2=0 to first order.
    a, b, z, f = sp.symbols("a b z f", positive=True)
    density = a*b*z**2*Le.subs(E, f/(a*b))
    for label, scale, target in [
        ("Hilbert time stress", a, Le-E*sp.diff(Le, E)),
        ("Hilbert radial stress", b, Le-E*sp.diff(Le, E)),
        ("Hilbert transverse trace", z, 2*Le),
    ]:
        actual = sp.diff(density, scale)*scale/(a*b*z**2)
        check(label, sp.simplify(actual-target.subs(E, f/(a*b))) == 0)
    # Sum of Euler equations and gauge energy conservation, including anisotropy.
    hp, nup, rhoq, Er, Dr, rr, sqF = sp.symbols("hp nup rhoq Er Dr rr sqF")
    Pprime = -hp*nup + rhoq*Er/sqF
    Hprime = Er*(rhoq/sqF - 2*Dr/rr)
    check("total anisotropic conservation", sp.expand(Pprime-Hprime+hp*nup-2*Er*Dr/rr) == 0)
    # The two Einstein equations follow directly from these independent tensor components.
    r, G, eta = sp.symbols("r G eta", positive=True)
    m = sp.Function("m")(r)
    nu = sp.Function("nu")(r)
    FF = 1-2*G*eta*m/r
    Gtt = (FF-1)/r**2 + sp.diff(FF, r)/r
    Grr = (FF-1)/r**2 + 2*FF*sp.diff(nu, r)/r
    eps, pr = sp.symbols("eps pr")
    check("Einstein tt mass ODE", sp.simplify(Gtt.subs(sp.diff(m,r), 4*sp.pi*r**2*eta*eps)+8*sp.pi*G*eta**2*eps) == 0)
    nup_expr = G*eta*(m+4*sp.pi*eta*r**3*pr)/(r**2*FF)
    check("Einstein rr lapse ODE", sp.simplify(Grr.subs(sp.diff(nu,r),nup_expr)-8*sp.pi*G*eta**2*pr) == 0)
    # Exterior Maxwell tail; m is Misner-Sharp mass, M is ADM mass.
    M,Q = sp.symbols("M Q")
    mout = M-eta*Q**2/(8*sp.pi*r)
    Fout = 1-2*G*eta*mout/r
    check("Maxwell exterior mass derivative", sp.simplify(sp.diff(mout,r)-4*sp.pi*r**2*eta*(Q/(4*sp.pi*r**2))**2/2) == 0)
    check("RN coefficient", sp.expand(Fout-(1-2*G*eta*M/r+G*eta**2*Q**2/(4*sp.pi*r**2))) == 0)
    check("RN lapse equation", sp.simplify(sp.diff(Fout,r)/(2*Fout)-nup_expr.subs({m:mout,pr:-(Q/(4*sp.pi*r**2))**2/2})) == 0)
    # Junction algebra is checked without subtracting two almost equal roots.
    aa, kk, R, mm, sig, Hi, Ho, P = sp.symbols("aa kk R mm sig Hi Ho P", positive=True)
    bb = aa-kk*R
    mp_shell = mm+R*(aa**2-bb**2)/(2*G*eta)
    ui = G*eta*(mm+4*sp.pi*eta*R**3*(P-Hi))/(R**2*aa)
    vo = G*eta*(mp_shell-4*sp.pi*eta*R**3*Ho)/(R**2*bb)
    J = vo-ui+kk
    kexpr = 4*sp.pi*G*sig*eta**2
    Lres = P-Hi+Ho-sig*(ui+2*aa/R-sp.Rational(3,2)*kk)
    relation = sp.factor((J+4*sp.pi*G*R*eta**2*Lres/bb).subs(kk,kexpr))
    # a^2=1-2G eta m/R is needed by the normal Einstein constraint.
    relation = sp.factor(relation.subs(mm,R*(1-aa**2)/(2*G*eta)))
    check("second Israel equation equals wall quadratic", relation == 0)
    mw=4*sp.pi*sig*R**2*eta
    check("junction shell mass redshift and binding", sp.simplify((mp_shell-mm).subs(kk,kexpr)-(mw*aa-G*eta*mw**2/(2*R))) == 0)
    check("NG wall quadratic coefficient", sp.simplify(sp.Rational(3,2)*sig*kexpr-6*sp.pi*G*eta**2*sig**2) == 0)
    # Exact rational bounds for the entire eta interval and full function box.
    ff=F(1341,250); gg=F(1,10**8); et=F(1,10**4)
    kb=ff*(1+ff)/100; kc=F(1,100)
    wb=2*kb; wc=2*kc*ff; P0=kb+kc*ff**2
    check("fixed EOS pressure below one", 0<P0<1)
    check("central enthalpy bounds", F(3,5)<wb<1 and F(1,10)<wc<1)
    check("critical zeta below 1/2500 using pi<4", 16*gg < F(1,2500)**2)
    vmax=F(32,5); ymin=F(53,10); ymax=F(537,100)
    Fl=1-F(1,10**9); X=F(1,1000)
    # sqrt(F)>F for 0<F<1 is a conservative rational replacement throughout.
    check("uniform F lower bound", 1-F(32,3)*gg*et*vmax>Fl)
    check("uniform pole margin", F(1,2500)*ymax/3<X)
    Hcap=X**2/(2*(1-X))
    check("gauge energy cap", Hcap<F(1,10**6))
    check("v lower self-map", F(99,100)*(1+ff)>F(63,10))
    check("v upper self-map", 1+ff+et*(P0+Hcap)<vmax)
    check("y lower self-map", F(99,100)*ff>ymin)
    check("y upper self-map", ff/Fl<ymax)
    check("positive matter radial pressure", F(99,100)**2*P0>Hcap)
    check("strict inward dark force on product box", F(63,10)-ymax/((1-X)*Fl)>0)
    check("hydrostatic drop fits 1 percent box", 25*gg < F(1,100)*min(wb,wc))
    check("bulk mass bound", F(16,3)*vmax<35)
    # Lipschitz constants use ||dw_a||<=w_a0 N, ||dv||,||dy||<=100 N.
    dFcap=F(32,3)*gg*et*100
    check("F variation bound", dFcap<F(2,10**9))
    check("inverse F variation bound", dFcap/Fl**2<F(3,10**9))
    check("inverse sqrt F variation bound", dFcap/(2*Fl**2)<F(2,10**9))
    check("electric field cap", (F(1,2500)*ymax/3)/(1-X)<F(1,1000))
    dHcap=F(1,1000)*F(1,2500)*100/3
    check("gauge Hamiltonian variation cap",dHcap<=F(1,75000))
    check("v Lipschitz row", (1+ff+et*(2*P0+dHcap))/100<F(7,100))
    check("y Lipschitz row", (ff/Fl+ff*F(2,10**9))/100<F(61,1000))
    dCcap=F(100,3)+et*(2*P0+dHcap)
    dAcap=16*gg*(dCcap/Fl+3*F(3,10**9))
    dbcap=((1+et)*dAcap+et*16*gg*3/Fl)/2/wb
    electriccap=F(16,3)*gg*(100/(1-X)**2/Fl+ymax/(1-X)*F(2,10**9))
    dccap=((1+et)*dAcap+et*16*gg*3/Fl+electriccap)/2/wc
    check("baryon enthalpy Lipschitz row", dbcap<F(1,1000))
    check("dark enthalpy Lipschitz row", dccap<F(1,1000))
    check("uniform contraction below 0.08", max(F(7,100),F(61,1000),F(1,1000))<F(2,25))
    loadmin=F(99,100)**2*P0-X**3/(3*(1-X))
    sigtest=F(51,100)*P0
    Acaplower=2*Fl
    Bcap=24*gg*et**2
    check("strict positive wall load",loadmin>0)
    check("weak wall root upper crossing",Acaplower*sigtest-Bcap*sigtest**2>P0)
    check("wall quadratic increasing",Acaplower-2*Bcap*sigtest>F(199,100))
    check("ordinary orientation b positive",Fl-16*gg*sigtest*et**2>F(99,100))
    return {"P0":str(P0),"sigma_test":str(sigtest),"q_upper":"2/25",
            "F_lower":str(Fl),"x_upper":str(X),"eta_range":["0","1/10000"],
            "v_lipschitz_upper":"7/100","y_lipschitz_upper":"61/1000",
            "w_lipschitz_upper":"1/1000","actual_exact_check_count":len(CHECKS)}


G=1e-8; f=1341/250; Kc=.01; Kb=f*(1+f)/100; zeta=math.sqrt(4*math.pi*G)
wb0=2*Kb; wc0=2*Kc*f; P0=Kb+Kc*f*f


def ham(D):
    # Convergent positive series avoids cancellation of -x-log(1-x).
    return sum(D**j/j for j in range(2,13))


def rhs(eta):
    def fun(r,Y):
        wb,wc,m,Q,Sb,Sc,chi,phi=Y
        rb=wb/(2*Kb); rc=wc/(2*Kc); P=Kb*rb*rb+Kc*rc*rc
        Fm=1-2*G*eta*m/r; D=Q/(4*math.pi*r*r); E=D/(1-D); H=ham(D)
        A=G*(m+4*math.pi*eta*r**3*(P-H))/(r*r*Fm)
        N=math.exp(eta*chi)
        return [-(1+eta*wb)*A,-(1+eta*wc)*A+zeta*E/math.sqrt(Fm),
                4*math.pi*r*r*(rb+rc+eta*(P+H)),
                4*math.pi*r*r*zeta*rc/math.sqrt(Fm),
                4*math.pi*r*r*rb/math.sqrt(Fm),4*math.pi*r*r*rc/math.sqrt(Fm),
                A,-N*E/math.sqrt(Fm)]
    return fun


def integrate(eta,rtol,atol,max_step):
    r0=1e-6
    am=4*math.pi*(1+f+eta*P0)/3
    ar=G*(am+4*math.pi*eta*P0)
    Y0=[wb0-(1+eta*wb0)*ar*r0*r0/2,
        wc0+(-(1+eta*wc0)*ar+4*math.pi*G*f/3)*r0*r0/2,
        am*r0**3,zeta*4*math.pi*f*r0**3/3,
        4*math.pi*r0**3/3,4*math.pi*f*r0**3/3,
        ar*r0*r0/2,-zeta*f*r0*r0/6]
    sol=solve_ivp(rhs(eta),(r0,1),Y0,method="DOP853",dense_output=True,
                  rtol=rtol,atol=atol,max_step=max_step)
    check("IVP reached R eta=%s tol=%s"%(eta,rtol),sol.success and sol.t[-1]==1.)
    grid=np.linspace(r0,1,1001); Y=sol.sol(grid)
    wb,wc,m,Q,Sb,Sc,chi,phi=Y
    rb=wb/(2*Kb); rc=wc/(2*Kc); P=Kb*rb*rb+Kc*rc*rc
    Fm=1-2*G*eta*m/grid; D=Q/(4*math.pi*grid**2)
    check("IVP stays in positive density/pole domain eta=%s tol=%s"%(eta,rtol),
          np.min(rb)>.99 and np.min(rc)>.99*f and np.max(D)<.001 and np.min(Fm)>1-1e-9)
    check("Gauss counts actual proper dark stock eta=%s tol=%s"%(eta,rtol),
          np.max(np.abs(Q-zeta*Sc))<2e-16)
    if eta:
        chem=np.expm1(eta*chi)/eta+np.exp(eta*chi)*wb
        chemc=np.expm1(eta*chi)/eta+np.exp(eta*chi)*wc+zeta*phi
    else:
        chem=chi+wb; chemc=chi+wc+zeta*phi
    check("chemical first integrals eta=%s tol=%s"%(eta,rtol),
          max(np.ptp(chem),np.ptp(chemc))<1e-13)
    # Orthogonal dense-output quadratures, rather than redundant ODE variables.
    def qint(index):
        def fun(rr):
            vals=sol.sol(max(rr,r0)); rb_=vals[0]/(2*Kb);rc_=vals[1]/(2*Kc)
            if index==0: e=rb_
            elif index==1:e=rc_
            elif index==2:e=Kb*rb_**2
            elif index==3:e=Kc*rc_**2
            else:e=ham(vals[3]/(4*math.pi*max(rr,r0)**2))
            return 4*math.pi*rr*rr*e
        return quad(fun,0,1,epsabs=2e-12,epsrel=2e-12,limit=100)[0]
    ints=[qint(i) for i in range(5)]
    masssum=ints[0]+ints[1]+eta*sum(ints[2:])
    check("mass integrates rest plus internal plus gauge eta=%s tol=%s"%(eta,rtol),abs(m[-1]-masssum)<2e-11)
    bound=wall_match(eta,float(m[-1]),float(Q[-1]),float(P[-1]),float(chi[-1]))
    return {"eta":eta,"rtol":rtol,"atol":atol,"max_step":max_step,
            "nfev":sol.nfev,"accepted_mesh_points":len(sol.t),
            "rho_b_edge":float(rb[-1]),"rho_c_edge":float(rc[-1]),
            "P_edge":float(P[-1]),"Misner_Sharp_mass_inside":float(m[-1]),
            "proper_baryon_rest_stock":float(Sb[-1]),"proper_dark_rest_stock":float(Sc[-1]),
            "charge":float(Q[-1]),"D_edge":float(D[-1]),"F_in_edge":float(Fm[-1]),
            "integrated_coordinate_rest_b":ints[0],"integrated_coordinate_rest_c":ints[1],
            "internal_energy_b":ints[2],"internal_energy_c":ints[3],"gauge_energy_inside":ints[4],
            "mass_accounting_error":float(m[-1]-masssum),
            "neutral_chemical_oscillation":float(np.ptp(chem)),
            "charged_chemical_oscillation":float(np.ptp(chemc)),"wall":bound}


def wall_match(eta,m,Q,P,chi):
    mp.mp.dps=80
    ee,mm,qq,pp,ch=map(lambda x:mp.mpf(str(x)),(eta,m,Q,P,chi))
    gg=mp.mpf('1e-8');pi=mp.pi
    a=mp.sqrt(1-2*gg*ee*mm)
    D=qq/(4*pi);Hi=-D-mp.log(1-D);Ho=D*D/2;delta=Hi-Ho
    up=gg*ee*(mm+4*pi*ee*(pp-Hi))/a
    A=up+2*a;B=6*pi*gg*ee**2;load=pp-delta
    sigma=2*load/(A+mp.sqrt(A*A-4*B*load))
    k=4*pi*gg*sigma*ee**2;b=a-k
    mw=4*pi*sigma*ee
    masswall=mw*a-gg*ee*mw*mw/2
    tail=ee*qq*qq/(8*pi)
    mout=mm+masswall;ADM=mout+tail
    if eta:
        vo=gg*ee*(mout-4*pi*ee*Ho)/b
        J=vo-up+k
        check("80 digit time Israel residual eta=%s"%eta,abs(J)<mp.mpf('1e-70'))
        check("80 digit angular Israel residual eta=%s"%eta,abs((a-b)-k)<mp.mpf('1e-70'))
        check("80 digit RN metric junction eta=%s"%eta,abs(b*b-(1-2*gg*ee*ADM+gg*ee**2*qq*qq/(4*pi)))<mp.mpf('1e-70'))
    check("positive weak NG tension eta=%s"%eta,0<sigma<mp.mpf(str(.51*P0)) and b>0)
    # Positive deltaH and the full wall balance are checked at precision where
    # no leading pressure or electromagnetic subtraction is swallowed.
    check("80 digit wall load residual eta=%s"%eta,abs(A*sigma-B*sigma*sigma-load)<mp.mpf('1e-70'))
    result={"sigma":sigma,"wall_rest_mass":mw,"wall_mass_redshifted":mw*a,
            "wall_self_binding_mass":-gg*ee*mw*mw/2,
            "ADM_mass":ADM,"exterior_Maxwell_energy":qq*qq/(8*pi),
            "exterior_Maxwell_mass":tail,"phase_energy_jump":delta,
            "k":k,"F_out_edge":b*b,"central_lapse":b*mp.exp(-ee*ch),
            "RN_discriminant_G2M2_minus_GQ2_over4pi":gg**2*ADM**2-gg*qq**2/(4*pi)}
    return {key:mp.nstr(value,35) for key,value in result.items()}


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);args=parser.parse_args()
    defs=json.loads((HERE/'inputs/definitions.json').read_text())
    check("frozen definition version",defs['definition_version']=='EINSTEIN-JOIN-1')
    for row in json.loads((HERE/'inputs/source_manifest.json').read_text())['sources']:
        snap=HERE/'inputs'/Path(row['snapshot']).name
        check("source snapshot hash "+snap.name,hashlib.sha256(snap.read_bytes()).hexdigest()==row['sha256'])
    exact=exact_checks()
    runs=[]
    for eta in [0.,1e-8,1e-6,1e-4]:
        coarse=integrate(eta,1e-10,1e-13,.01)
        fine=integrate(eta,2e-12,2e-15,.0025)
        errors={key:abs(coarse[key]-fine[key]) for key in
                ['rho_b_edge','rho_c_edge','P_edge','Misner_Sharp_mass_inside','proper_baryon_rest_stock','proper_dark_rest_stock','charge']}
        check("two-tolerance IVP control eta=%s"%eta,max(errors.values())<2e-11)
        runs.append({'coarse':coarse,'fine':fine,'coarse_fine_absolute_differences':errors})
    out={'definition_version':defs['definition_version'],
         'software':{'Python':sys.version,'NumPy':np.__version__,'SciPy':scipy.__version__,
                     'SymPy':sp.__version__,'mpmath':mp.__version__,'platform':platform.platform()},
         'exact_rational_bounds':exact,'IVP_runs':runs,'checks':CHECKS,'check_count':len(CHECKS),
         'verdict':'Exact implemented identities/bounds passed. IVPs passed only within stated tolerances; analytic existence is proved separately.',
         'nonclaims':defs['nonclaims']}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'check_count':len(CHECKS),'example_eta':runs[-1]['fine']['eta'],
                      'sigma':runs[-1]['fine']['wall']['sigma'],'ADM_mass':runs[-1]['fine']['wall']['ADM_mass']},indent=2))


if __name__=='__main__':main()
