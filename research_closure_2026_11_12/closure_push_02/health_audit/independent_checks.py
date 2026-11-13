#!/usr/bin/env python3
"""Independent finite-Pi ADM audit; does not import the author's checker."""
import argparse,json,time
from pathlib import Path
import sympy as s
import mpmath as mp


def main(output):
    start=time.perf_counter();checks={}
    def check(name,expression):checks[name]=s.simplify(expression)==0
    e,z,alpha,zd,zx,zxx,bx,bxx,h,M,k=s.symbols('e z alpha zd zx zxx bx bxx h M k')
    # Construct actual 3D covariant Kij for a scalar varying along x. The yy,zz
    # covariant shift derivatives contain Gamma^x_yy=-z_x, and must be retained.
    metric=s.exp(2*e*z)
    E=s.diag(metric*(h+e*zd)-e*bxx+e*e*zx*bx,
             metric*(h+e*zd)-e*e*zx*bx,metric*(h+e*zd)-e*e*zx*bx)
    mixedK=E/(metric*(1+e*alpha))
    dens=(1+e*alpha)*s.exp(3*e*z)*M*(s.trace(mixedK*mixedK)-s.trace(mixedK)**2)/2
    second=s.diff(dens,e,2).subs(e,0)/2
    expected=(-3*M*(zd-h*alpha)**2+2*M*bxx*(zd-h*alpha)
              -18*M*h*z*zd+9*M*h*h*alpha*z-s.Rational(27,2)*M*h*h*z*z
              +2*M*h*(z*bxx+zx*bx))
    check('full_scalar_Einstein_extrinsic_expansion',second-expected)
    # Last two shift terms are d_x(z beta_x); their bulk integral vanishes.
    spatial=M*(1+e*alpha)*s.exp(e*z)*(-4*e*zxx-2*e*e*zx*zx)/2
    spatial2=s.diff(spatial,e,2).subs(e,0)/2
    check('Einstein_spatial_curvature_expansion',spatial2-M*(-2*z*zxx-zx*zx-2*alpha*zxx))
    check('Fourier_integrated_curvature',spatial2.subs({zxx:-k*k*z,zx*zx:k*k*z*z})-M*k*k*(z*z+2*alpha*z))
    # Independent matter Taylor expansion at a center with P=0, divP=p.
    q,p,d,g,H0,Hq,Hp,Hqq,Hqp,Hpp=s.symbols('q p d g H0 Hq Hp Hqq Hqp Hpp')
    Q=q/(1+e*alpha);Pi=(p+e*d)*s.exp(-3*e*z);dq,dp=Q-q,Pi-p
    H=H0+Hq*dq+Hp*dp+Hqq*dq*dq/2+Hqp*dq*dp+Hpp*dp*dp/2
    density=(1+e*alpha)*s.exp(3*e*z)*(H-Pi-g*Pi*Pi/2)
    mat2=s.diff(density,e,2).subs(e,0)/2
    A=q*q*Hqq;c=1+g*p-Hp+q*Hqp;D=Hpp-g
    check('matter_lapse_square',s.diff(mat2,alpha,2)-A)
    check('matter_lapse_polarization_mixing',s.diff(mat2,alpha,d)+c)
    check('matter_divergence_square',s.diff(mat2,d,2)-D)
    check('metric_divergence_mixing_is_derivative_free',s.diff(mat2,z,d)+3*p*D)
    # High-frequency Legendre reduction at fixed chi=N U_Pi, independently of
    # any guessed scalar kinetic action. Solve its implicit Pi(N) explicitly
    # for this arbitrary quadratic Taylor representative.
    N,pp=s.symbols('N pp',nonzero=True);chi=Hp-1-g*p
    qdelta=q/N-q;pdelta=pp-p
    Ut=H0+Hq*qdelta+Hp*pdelta+Hqq*qdelta**2/2+Hqp*qdelta*pdelta+Hpp*pdelta**2/2-pp-g*pp**2/2
    ppN=p+(chi/N-chi-Hqp*qdelta)/D
    legendre=(N*Ut-chi*pp).subs(pp,ppN)
    check('independent_fixed_chi_lapse_Hessian',s.diff(legendre,N,2).subs(N,1)-(A-c*c/D))
    # Energy and pressure from separate metric variations.
    rho=q*Hq-H0+p+g*p*p/2;pressure=H0-p*Hp+g*p*p/2
    check('central_lapse_energy',-s.diff(density,alpha,e).subs(e,0)-rho)
    # d/de at alpha=0,z=1 gives 3*pressure; d and alpha are zero here.
    check('central_metric_pressure',s.diff(density,e).subs({e:0,alpha:0,d:0,z:1})/3-pressure)
    neff=q*Hq+p*(1+g*p-Hp)
    check('enthalpy',rho+pressure-neff)
    # Current time-jet compatibility, keeping Bdot and lambda terms.
    Qd,pd=s.symbols('Qd pd');B=1+g*p-Hp
    Bd=-Hqp*Qd-D*pd;bd=B/q;bdot=Bd/q-B*Qd/q**2
    rhocharge=Hq+bd*p
    rhocharge_dot=Hqq*Qd+Hqp*pd+bdot*p+bd*pd
    center_clock=q*(rhocharge_dot+3*h*rhocharge-p*bdot)
    energy_equation=q*Hqq*Qd+c*pd+3*h*neff
    check('clock_current_equals_Einstein_energy_time_jet',center_clock-energy_equation)
    # The crossed spatial-curvature coefficient must be differentiated in time.
    a,hdot,km=s.symbols('a hdot km',nonzero=True)
    cross=M*a*km*km/h
    crossdot=s.diff(cross,a)*a*h+s.diff(cross,h)*hdot
    check('time_cross_gradient',M*a*km*km-crossdot-M*a*km*km*hdot/h**2)
    checks['freeze_time_cross_mutation_fails']=s.simplify(M*a*km*km-M*a*km*km*hdot/h**2)!=0
    checks['omit_gate_HPi_mutation_fails']=s.simplify(c-(1+g*p+q*Hqp))!=0
    # Physical radial divergence, including all powers of the conformal factor.
    r=s.symbols('r',positive=True);psi=s.Function('psi')(r);v=s.Function('v')(r)
    geometric=s.diff(psi**6*r*r*(v/psi**2),r)/(psi**6*r*r)
    check('physical_radial_divergence',geometric-(s.diff(v,r)+2*v/r+4*s.diff(psi,r)*v/psi)/psi**2)
    # Flat gate explicit family and the finite-domain/nonflat exclusions.
    u=s.symbols('u',positive=True);gate=s.exp(-u**3)
    family=2*gate-s.diff(gate,u)**2/s.diff(gate,u,2)
    check('flat_gate_family_ratio',family-gate*(3*u**3-4)/(3*u**3-2))
    checks['flat_gate_u1_strict_negative']=s.simplify(family.subs(u,1))==-s.exp(-1)
    nonflat=s.exp(-u)
    checks['nonflat_exponential_is_exception']=s.simplify(s.diff(nonflat,u,2)-s.diff(nonflat,u)**2/(2*nonflat))==s.exp(-u)/2
    checks['finite_domain_flat_gate_is_exception']=s.diff(1-u**3,u,2)==-6*u
    Cf,Pc,S0,S1,S2=s.symbols('Cf Pc S0 S1 S2',nonzero=True)
    cf=1+g*Pc*u+Cf*(q*q-1)*S1/Pc
    df=Cf*(q-1)**2*S2/Pc**2-g
    af=2*Cf*q*q*S0-cf*cf/df
    check('generic_fixed_stiffness_large_q_limit',s.limit(af/(Cf*q*q),q,s.oo)-(2*S0-S1*S1/S2))
    nf=2*Cf*q*(q-1)*S0+Pc*u*(1+g*Pc*u-Cf*(q-1)**2*S1/Pc)
    check('generic_large_q_enthalpy_limit',s.limit(nf/(Cf*q*q),q,s.oo)-(2*S0-u*S1))
    # Independent high-precision parameter evaluation, not author's float code.
    mp.mp.dps=60;qq=1+mp.mpf('1e-6');CC=mp.mpf('1e6');gg=mp.mpf('1e-8')
    ss=mp.exp(-1);x=qq-1;HQ=2*CC*x*ss;HQQ=2*CC*ss;HP=-3*CC*x*x*ss
    HQP=-6*CC*x*ss;HPP=3*CC*x*x*ss;bb=1+gg-HP;cc=bb+qq*HQP;dd=HPP-gg
    aa=qq*qq*HQQ;ainf=aa-cc*cc/dd;enthalpy=qq*HQ+bb;rho0=CC*(qq*qq-1)*ss+1+gg/2
    hubble=mp.sqrt(2*rho0/3);sound2=enthalpy/ainf
    # Leading NR limit independently derived in current_transport; compare at
    # this near-Newtonian point, without using it as the full-GR proof.
    nr_ainf=HQQ-(1+HQP)**2/dd;nr_speed=(HQ+1)/nr_ainf
    checks['numerical_negative_Ainf_positive_enthalpy']=bool(ainf<0 and enthalpy>0 and rho0>0 and dd>0)
    checks['near_Newtonian_limit_agrees']=bool(abs(nr_speed/sound2-1)<1e-5)
    numbers={name:mp.nstr(val,50) for name,val in [('A0',aa),('c',cc),('D',dd),('Ainfinity',ainf),('enthalpy',enthalpy),('rho',rho0),('h',hubble),('speed_squared',sound2),('growth_per_k',mp.sqrt(-sound2)),('NR_speed_squared',nr_speed),('NR_relative_difference',abs(nr_speed/sound2-1))]}
    result={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':all(checks.values()),'count':len(checks),
            'independent_parameters':numbers,'runtime_seconds':time.perf_counter()-start,
            'scope':'Exact local ADM/Legendre/current identities and parameter calculation; no global background evolution, finite-k spectrum or UV completion'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_pass']


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
