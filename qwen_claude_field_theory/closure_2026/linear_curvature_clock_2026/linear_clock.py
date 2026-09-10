#!/usr/bin/env python3
"""Construct the zero auxiliary-self-gradient member of the curvature action.

Same action as elliptic_curvature_clock, minus 2m int N sqrt(h) (Dchi)^2.
This changes the constraint, not the prescribed MOND function. No full closure
is inferred from a frozen local calculation. Exact FLRW is unchanged because
the removed term and its first variation vanish on homogeneous fields.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import sympy as s

BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('curvature_base',BASE/'elliptic_curvature_clock_2026/compensator.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)


def null_beams(response):
    """Two positive-energy, freely streaming null-dust pairs.

    In real space each density is [f(x-te)+f(x+te)]/2 with f>=0.
    The particles follow the minimally coupled einbein action; free streaming
    is its leading flat/frozen-background limit, not a new force prescription.
    """
    m,q,alpha,w,rho,S=response['symbols']
    einbein=s.symbols('einbein',positive=True)
    vs=s.Matrix(s.symbols('v0:4',real=True));acc=s.Matrix(s.symbols('a0:4',real=True))
    edot=s.symbols('einbein_dot',real=True)
    metric=s.Matrix(4,4,s.symbols('g0:16',real=True))
    particle_L=(vs.T*metric*vs)[0]/(2*einbein)
    stress=s.Matrix(4,4,lambda i,j:2*s.diff(particle_L,metric[i,j]))
    eta=s.diag(-1,1,1,1)
    flat_L=particle_L.subs(dict(zip(list(metric),list(eta))))
    momenta=s.Matrix([s.diff(flat_L,v) for v in vs])
    coordinate_EL=momenta.jacobian(vs)*acc+momenta.diff(einbein)*edot
    constraint=s.diff(flat_L,einbein)
    nulls=[]
    for direction in (s.Matrix([1,1,0,0]),s.Matrix([1,-1,0,0]),
                      s.Matrix([1,0,0,1]),s.Matrix([1,0,0,-1])):
        nulls.append(s.simplify(constraint.subs(dict(zip(vs,direction)))))
    particle=dict(L=particle_L,flat_coordinate_EL=coordinate_EL,
                  einbein_EL=constraint,metric_variation_stress=stress,null_constraints=nulls)
    kx,ky,kz,t=s.symbols('kx ky kz t',real=True)
    profile=s.symbols('profile',real=True)
    mt,delta,R=s.symbols('mu_t anisotropy radius',positive=True)
    sources=[];ward=[]
    for k in (kx,kz):
        density=profile*s.cos(k*t)
        current=-s.I*profile*s.sin(k*t)
        stress=density
        ward.extend([s.simplify(s.diff(density,t)+s.I*k*current),
                     s.simplify(s.diff(current,t)+s.I*k*stress)])
        sources.append((density,current,stress))
    A,B=sources
    initial=[s.simplify((A[0]-B[0]).subs(t,0)),A[1].subs(t,0),B[1].subs(t,0),
             s.simplify((A[2]-B[2]).subs(t,0)),s.diff(A[0]-B[0],t).subs(t,0)]
    density_dd=s.simplify(s.diff(A[0]-B[0],t,2).subs(t,0)/profile)
    D=s.symbols('D',real=True)
    R00=response['R00'].subs(alpha,1-D/q)
    W=-w*w+2*D/3
    forcing=s.factor(W*R00)
    # Extract temporal contact coefficients from the derived wave equation.
    c_rho=s.expand(forcing).coeff(rho).coeff(w,2)
    c_stress=s.expand(forcing).coeff(S).coeff(w,2)
    q3=kx*kx+ky*ky+kz*kz;D3=mt*q3+delta*kz*kz
    delta_Rdd=s.factor(-(c_rho+c_stress).subs({D:D3,q:q3})*density_dd)
    local=(mt-1)*density_dd/(2*m)
    tail_symbol=s.factor(delta_Rdd-local)
    target=delta*kz*kz*(kz*kz-kx*kx)/(2*m*q3)
    x,y,z=s.symbols('x y z',real=True)
    green=1/(4*s.pi*s.sqrt(x*x+y*y+z*z))
    # q^{-1}=(-Delta)^{-1}; Z(Z-X) maps to d_z^4-d_z^2 d_x^2.
    kernel=delta*(s.diff(green,z,4)-s.diff(green,z,2,x,2))/(2*m)
    exterior=s.simplify(kernel.subs({x:0,y:R,z:0}))
    expected_forcing=q*(rho+S)/(3*m)+w*w*(S-D*rho/q)/(2*m)
    return dict(particle_variation=particle,ward_residuals=ward,initial_source_differences=initial,
                density_second_derivative_difference=density_dd,
                curvature_wave_forcing=forcing,
                response_equation_residual=s.factor(forcing-expected_forcing),
                curvature_second_derivative_difference=delta_Rdd,
                off_source_symbol=tail_symbol,tail_symbol_residual=s.factor(tail_symbol-target),
                exterior_tail=exterior,isotropic_tail=s.simplify(exterior.subs(delta,0)),
                interpretation='Positive null beams, same initial density/current/trace, differing compact stress direction; frozen weak-field comparison only.')


@lru_cache(None)
def derive():
    m,q=s.symbols('m q',positive=True);alpha,w=s.symbols('alpha omega',real=True)
    z,n,B,c,E,zd,Ed,pz,pn,pB,pc,pE=s.symbols('z n B chi E zd Ed pz pn pB pc pE',real=True)
    K=s.diag(zd+q*(B-Ed),zd,zd)
    Lkin=m*(s.trace(K*K)-s.trace(K)**2)/2+2*m*s.trace(K)**2/3
    V=m*q*(z*z+2*n*z+alpha*n*n+4*c*(z+n))
    L=s.expand(Lkin+V)
    vel=s.solve([s.diff(L,zd)-pz,s.diff(L,Ed)-pE],[zd,Ed])
    H=s.factor((pz*zd+pE*Ed-L).subs(vel))
    dc={name:old.engine.linear_dirac(H.subs(alpha,a),[z,E,n,B,c],[pz,pE,pn,pB,pc],[pn,pB,pc])
        for name,a in [('generic',alpha),('zero_field',s.S.One),('radial_turnover',s.S.Zero)]}
    Lg=L.subs(Ed,0)
    aux=s.solve([s.diff(Lg,x) for x in (n,B,c)],[n,B,c])
    red=s.factor(Lg.subs(aux));A=s.factor(s.diff(red,zd,2)/2)
    speed=s.factor(-s.diff(red,z,2)/(2*q*A))
    auxmatrix=s.hessian(V,[n,c])
    # Complex amplitudes are required for a Fourier response, unlike the
    # real canonical variables used above.
    zz,nn,bb,cc,vz,rho,S=s.symbols('zF nF BF chiF velocityF rho stress')
    Lf=Lg.subs({z:zz,n:nn,B:bb,c:cc,zd:vz})-nn*rho+zz*S-s.I*w*bb*rho
    eq=[s.diff(Lf,zz)+s.I*w*s.diff(Lf,vz)]+[s.diff(Lf,x) for x in (nn,bb,cc)]
    eq=[s.expand(e.subs(vz,-s.I*w*zz)) for e in eq]
    sol=s.solve(eq,[zz,nn,bb,cc])
    R=s.factor((-q*nn+s.I*w*q*bb+3*w*w*zz).subs(sol))
    high=s.factor(s.limit(R,w,s.oo))
    response=dict(symbols=(m,q,alpha,w,rho,S),equations=eq,solution=sol,
                  residuals=[s.simplify(e.subs(sol)) for e in eq],R00=R,high_frequency_R00=high)
    # Construct compact initial metric and auxiliary fields, including shift.
    D,f,v=s.symbols('D profile velocity_profile',real=True)
    z0=q*f;zd0=q*v;n0=-q*f;c0=-D*f/2;B0=-3*v/2
    conditions=[(alpha*n+z+2*c),(z+n),(2*q*B+3*zd)]
    initial={alpha:1-D/q,z:z0,zd:zd0,n:n0,c:c0,B:B0}
    zdd=-speed*q*z
    Rvac=s.factor(-q*aux[n]-q*s.diff(aux[B],zd)*zdd-3*zdd)
    R0=s.factor(Rvac.subs({alpha:1-D/q,z:z0}))
    Omega2=s.factor((speed*q).subs(alpha,1-D/q))
    R4=s.factor(Omega2**2*R0)
    # Denominator refers to spatial variables, not numerical constants.
    spatial_denominator=s.denom(s.cancel(9*R4))
    vacuum=dict(initial_z=z0,initial_zdot=zd0,initial_n=n0,initial_chi=c0,initial_B=B0,
                constraint_residuals=[s.factor(e.subs(initial,simultaneous=True)) for e in conditions],
                omega_squared=Omega2,R00=Rvac,
                curvature_identity_residual=s.factor(Rvac-q*(2-alpha)*z),
                initial_R00=R0,fourth_time_derivative=R4,
                fourth_derivative_denominator=spatial_denominator,
                first_order_residuals=[s.factor(zd+2*q*aux[B]/3),
                    s.factor(s.diff(aux[B],zd)*zdd+2*aux[c]),
                    s.factor(s.diff(aux[c],z)*zd-(1-alpha)*q*aux[B]/3)])
    p,a0=s.symbols('Phi_gradient a0',positive=True)
    g,j=s.symbols('Psi_gradient chi_gradient',real=True)
    fmond=2*a0*a0*(1-(1+p/a0)*s.exp(-p/a0))
    Lstat=m*(g*g-2*p*g+fmond+4*j*(p-g))
    flux=[s.diff(Lstat,x)/(2*m) for x in (p,g,j)]
    branch=s.solve(flux[1:],[g,j])
    static=dict(L=Lstat,independent_fluxes=flux,branch=branch,
                slip_residual=s.simplify(branch[g]-p),chi_gradient=branch[j],
                MOND_residual=s.simplify(-flux[0].subs(branch)-p*(1-s.exp(-p/a0))),
                G_measured=1/(8*s.pi*m))
    x=s.symbols('x');u=s.Function('u')(x);ch=s.Function('chi')(x)
    Lchi=s.exp(u)*(4*s.diff(ch,x)*s.diff(u,x)+2*ch*s.diff(u,x)**2)
    chi_EL=s.simplify((s.diff(Lchi,ch)-s.diff(s.diff(Lchi,s.diff(ch,x)),x))/s.exp(u))
    hp,hc,vp,vc,k,cb=s.symbols('hp hc vp vc k chi_bar',real=True)
    ht=s.Matrix([[hp,hc,0],[hc,-hp,0],[0,0,0]]);hdt=ht.subs({hp:vp,hc:vc})
    Ltt=m*s.exp(2*cb)*(s.trace(hdt*hdt)-k*k*s.trace(ht*ht))/8
    KT=s.hessian(Ltt,[vp,vc]);VT=-s.hessian(Ltt,[hp,hc]);w2=s.symbols('w2')
    return dict(principal=dict(symbols=(m,q,alpha),L=L,H=H,auxiliaries=aux,reduced_L=red,
                              kinetic=A,speed_squared=speed,auxiliary_hessian=auxmatrix,
                              auxiliary_determinant=s.factor(auxmatrix.det())),
                dirac=dc,static=static,vacuum=vacuum,response=response,
                homogeneous=old.homogeneous(),chi_spatial_EL=chi_EL,null_beams=null_beams(response),
                tensor=dict(kinetic=KT,frequency_squared=s.solve(s.det(w2*KT-VT),w2)),
                status='OPEN: local vacuum-wave repair; matter-coupled causal completion unproved')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--require-closure',action='store_true')
    args=parser.parse_args();a=derive()
    print(json.dumps(old.serializable(a),default=str,indent=2))
    checks=a['response']['residuals']+a['vacuum']['constraint_residuals']
    if any(x!=0 for x in checks) or not all(x['preservation_closed'] for x in a['dirac'].values()):
        return 1
    return 2 if args.require_closure else 0


if __name__=='__main__':
    raise SystemExit(main())
