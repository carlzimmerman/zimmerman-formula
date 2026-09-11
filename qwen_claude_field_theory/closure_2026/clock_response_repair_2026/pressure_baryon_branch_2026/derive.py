#!/usr/bin/env python3
"""Derive isotropic-pressure sources and the preserved initial clock equation."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent


def derive():
    spec=importlib.util.spec_from_file_location('spherical_action',HERE.parent/'spherical_baryon_bridge/action/derive.py')
    m=importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):spec.loader.exec_module(m)
    p,rho,H,q,kd,hd,qd,lap=s.symbols('p rho H q kd hd qd lap',real=True)
    # Matter source: L_b=N A R² P_b(Z), at theta_r=0, Z=theta_t²/N².
    Nt,At,Rt,Tt,Z=s.symbols('N_b A_b R_b theta_t Z',positive=True)
    P=s.Function('P_b')
    matter=Nt*At*Rt**2*P(Tt*Tt/(Nt*Nt))
    density=2*Z*s.diff(P(Z),Z)-P(Z)
    checks={}
    def check(name,e):
        checks[name]=s.simplify(e)==0
        if not checks[name]:raise AssertionError(name+': '+str(s.simplify(e)))
    zmap={Tt**2/Nt**2:Z}
    check('matter_lapse_source',s.diff(matter,Nt).subs(zmap)+At*Rt**2*density)
    check('matter_radial_pressure',s.diff(matter,At).subs(zmap)-Nt*Rt**2*P(Z))
    check('matter_angular_pressure',s.diff(matter,Rt).subs(zmap)-2*Nt*At*Rt*P(Z))
    N,A,r,M,g=m.N,m.A,m.r,m.M2,m.gamma
    sub={m.R:r,m.Rr:1,m.jets['R',0,2]:0,m.u:0,m.ur:0,
         m.At:N*A*H,m.Rt:N*r*H,m.ct:N*q,
         m.jets['A',2,0]:A*(N*kd+m.Nt*H+N*N*H*H),
         m.jets['R',2,0]:r*(N*hd+m.Nt*H+N*N*H*H),
         m.jets['c',2,0]:m.Nt*q+N*qd,
         m.jets['A',1,1]:m.Nr*A*H+N*m.Ar*H,
         m.jets['R',1,1]:m.Nr*r*H+N*H,
         m.jets['c',1,1]:m.Nr*q,m.jets['c',1,2]:m.jets['N',0,2]*q}
    sub.update({z:0 for (name,i,j),z in m.jets.items() if name=='v'})
    pull=lambda e:s.cancel(e.subs(sub,simultaneous=True))
    ham=pull(m.E['N'])/(A*r*r)-rho
    ar=s.solve(ham,m.Ar)[0]
    nr2=A*A*lap-(2/r-m.Ar/A)*m.Nr
    equations=[pull(m.E['A'])/(r*r)+N*p,pull(m.E['R'])/(A*r)+2*N*p,
               -pull(m.E['c'])/(A*r*r)]
    equations=[s.cancel(e.subs(m.jets['N',0,2],nr2).subs(m.Ar,ar)) for e in equations]
    sol=s.solve(equations,[kd,hd,qd],dict=True)[0]
    # This initial family is embedded in the original homogeneous solution.
    # Impose its Friedmann constraint, retaining arbitrary local rho and p.
    Lambda=next(z for z in ham.free_symbols if str(z)=='Lambda')
    bg_lambda=3*H*H-(2*q*q*m.PX-m.P+m.V-6*g*H*q**3)/M
    sol={key:s.cancel(value.subs(Lambda,bg_lambda)) for key,value in sol.items()}
    J=2*q*m.PX-6*g*H*q*q
    Bh=2*m.PX+4*q*q*m.PXX-12*g*H*q+6*g*g*q**4/M
    C=2*q*m.PXt+3*g*q*q*m.W/M
    theta=H+g*q**3/M
    check('Qdot_pressure_enters_as_rho_plus_3p',sol[qd]+(N*(3*J*theta+g*q*q*(rho+3*p)/M)+C)/Bh)
    check('Kdot_pressure_enters_as_rho_plus_3p',sol[kd]+2*sol[hd]-lap+
          (N*(3*q*J+rho+3*p)+3*m.W)/(2*M)+3*g*q*q*sol[qd]/M)
    # Before background restriction, constant terms are retained independently.
    Ptt,Vtt=s.symbols('P_tt V_tt',real=True)
    preserved=Vtt-Ptt+3*H*m.Wt+m.W*(sol[kd]+2*sol[hd])-2*q*m.PXt*sol[qd]-2*q*q*m.WY*lap
    stiffness=m.W-2*q*q*m.WY
    lb=m.W/(2*M)-g*q*q*C/(M*Bh)
    check('lapse_principal_coefficient',s.diff(preserved,lap)-stiffness)
    check('lapse_density_source',s.diff(preserved,rho)+lb*N)
    check('lapse_pressure_source',s.diff(preserved,p)+3*lb*N)
    check('pressure_does_not_source_hamiltonian',s.diff(ham,p))
    # Independent angular equation determines geodesic areal acceleration.
    # Homogeneous energy identity: rho_clock=3M²H²-M²Lambda.
    h_expected=(m.Nr/(A*A*r)-N*((1-1/(A*A))/(2*r*r)+q*J/(2*M)+p/(2*M))
                -m.W/(2*M)-g*q*q*sol[qd]/M)
    check('angular_pressure_acceleration',sol[hd]-h_expected)
    return dict(checks=checks,stiffness=str(stiffness),lambdab=str(lb),
        source='rho_b+3p_b',lapse='S Delta_h N - lambda0*(N-1) - lambdab*(rho_b+3p_b)*N=0',
        scope='initial homogeneous-clock expanding slice; no frozen-chi-gradient evolution assumed')

if __name__=='__main__':print(json.dumps(derive(),indent=2))
