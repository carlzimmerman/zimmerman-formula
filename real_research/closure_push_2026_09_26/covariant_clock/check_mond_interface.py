#!/usr/bin/env python3
"""Exact static polar-clock source plus finite weighted-cycle response check."""
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as s


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True); args=ap.parse_args(); checks={}
    def exact(name,expr):
        val=s.factor(s.simplify(expr)); assert val==0,(name,val)
        checks[name]={'passed':True,'residual':str(val)}
    def bounded(name,val,ok):
        assert bool(ok),(name,val); checks[name]={'passed':True,'measured':val}
    C,a0,x,N,R,Omega,lam,m,X,q,k2,u=s.symbols('C a0 x N R Omega lambda m X q k2 mu2',positive=True)
    F=2*(1-C)*a0*a0*x*x+4*C*a0*a0*(1-(1+x)*s.exp(-x))
    A=x*x+2*(1+x)*s.exp(-x)-2
    exact('measured_G_exact_AQUAL_primitive',-2*a0*a0*x*x+F+2*C*a0*a0*A)
    exact('acceleration_first_variation_vector_coefficient',s.diff(F,x)/(a0*a0*x)-4*(1-C*(1-s.exp(-x))))
    grad2,V=s.symbols('gradR2 V',real=True)
    staticL=Omega**2*R**2/(2*N)-N*(grad2/2+V)
    rho=Omega**2*R**2/(2*N**2)+grad2/2+V
    exact('exact_static_lapse_density',-s.diff(staticL,N)-rho)
    potential=m*m*R*R/2+lam*R**4/4
    rsquared=(2*X-m*m)/lam
    P=(2*X-m*m)**2/(4*lam)
    exact('TF_radial_stationarity', (2*X*R-s.diff(potential,R)).subs(R,s.sqrt(rsquared)))
    exact('TF_effective_P', (X*R*R-potential).subs(R**2,rsquared)-P)
    PX=s.diff(P,X); PXX=s.diff(P,X,2)
    rhoTF=2*X*PX-P
    exact('TF_energy_density',rhoTF-(2*X-m*m)*(6*X+m*m)/(4*lam))
    exact('TF_lapse_susceptibility',2*X*s.diff(rhoTF,X)-2*X*(6*X-m*m)/lam)
    exact('TF_temporal_kinetic_coefficient',PX+2*X*PXX-(6*X-m*m)/lam)
    c0=s.symbols('vacuum_constant',real=True)
    exact('constant_vacuum_cannot_remove_susceptibility',s.diff(rhoTF+c0,X)-s.diff(rhoTF,X))

    nu,r=s.symbols('nu deltaR',real=True)
    radial_linear=(-k2-u)*r-2*q*R*nu
    response=-2*q*R*nu/(k2+u)
    exact('gradient_retaining_radial_response',radial_linear.subs(r,response))
    drho=2*R*q*r-R*R*q*nu
    susceptibility=R*R*q*(1+4*q/(k2+u))
    exact('gradient_retaining_density_susceptibility',drho.subs(r,response)+susceptibility*nu)
    dp=-R*R*q*nu
    active_susceptibility=4*R*R*q*(1+q/(k2+u))
    exact('pressure_and_active_trace_susceptibility',(drho+3*dp).subs(r,response)+active_susceptibility*nu)
    substitutions={u:2*lam*R*R,q:m*m+lam*R*R}
    exact('TF_limit_of_gradient_response',susceptibility.subs(k2,0).subs(substitutions)-((q*(3*q-m*m)/lam).subs(q,m*m+lam*R*R)))
    exact('high_k_density_response_does_not_vanish',s.limit(susceptibility,k2,s.oo)-R*R*q)
    # A general P(X) can have constant rho only with vanishing temporal kinetic.
    b,c=s.symbols('b c',real=True)
    Pzero=b*s.sqrt(X)+c
    exact('constant_density_P_solution',2*X*s.diff(Pzero,X)-Pzero+c)
    exact('constant_density_cancels_temporal_kinetic',s.diff(Pzero,X)+2*X*s.diff(Pzero,X,2))
    # Constant active rho+3p requires negative relative kinetic/gradient signs.
    Pactive=-b/X+c
    exact('constant_active_density_P_solution',s.diff(2*X*s.diff(Pactive,X)+2*Pactive,X))
    exact('active_cancellation_opposite_kinetic_sign',s.diff(Pactive,X)+2*X*s.diff(Pactive,X,2)+3*s.diff(Pactive,X))

    # Exact finite-graph variational radial equation, with fixed prescribed N.
    size=32; dx=2*np.pi/size; xx=dx*np.arange(size); mode=2
    D=np.zeros((size,size)); Interp=np.zeros((size,size))
    for i in range(size):
        j=(i+1)%size; D[i,i]=-1/dx; D[i,j]=1/dx
        Interp[i,i]=Interp[i,j]=.5
    m2num,lnum,rbase,qbase=1.,.5,1.,1.5
    direction=np.cos(mode*xx)
    def solve_static(epsilon):
        ell=epsilon*direction; mass=dx*np.exp(ell); weights=dx*np.exp(Interp@ell)
        Lap=-(D.T@(weights[:,None]*D))/mass[:,None]
        qlocal=qbase*np.exp(-2*ell)
        rr=np.full(size,rbase)
        residual_norm=0.
        for iteration in range(15):
            residual=Lap@rr+(qlocal-m2num)*rr-lnum*rr**3
            residual_norm=float(np.max(np.abs(residual)))
            if residual_norm<3e-12: break
            jac=Lap+np.diag(qlocal-m2num-3*lnum*rr*rr)
            rr-=np.linalg.solve(jac,residual)
        assert residual_norm<3e-12 and np.min(rr)>0,(residual_norm,rr.min())
        potential=.5*m2num*rr*rr+.25*lnum*rr**4
        # This is the exact graph lapse source from varying node and edge weights.
        gradient_source=.5*(Interp.T@(weights*(D@rr)**2))/mass
        density=.5*qlocal*rr*rr+potential+gradient_source
        return rr,density,residual_norm
    kh2=4*np.sin(mode*dx/2)**2/dx**2
    stiffness=2*lnum*rbase*rbase
    predicted_r=-2*qbase*rbase/(kh2+stiffness)*direction
    predicted_rho=-rbase*rbase*qbase*(1+4*qbase/(kh2+stiffness))*direction
    rows=[]
    for step in [1e-3,1e-4,1e-5]:
        rp,ep,res_p=solve_static(step); rm,em,res_m=solve_static(-step)
        rows.append({'step':step,'radial_derivative_error':float(np.max(np.abs((rp-rm)/(2*step)-predicted_r))),
                     'density_derivative_error':float(np.max(np.abs((ep-em)/(2*step)-predicted_rho))),
                     'static_equation_residual':max(res_p,res_m)})
    bounded('nonlinear_static_graph_matches_gradient_retaining_response',rows,
            rows[-1]['radial_derivative_error']<2e-8 and rows[-1]['density_derivative_error']<5e-8)
    mismatch=float(np.max(np.abs(predicted_rho+qbase*rbase*rbase*direction)))
    bounded('negative_control_freezing_amplitude_misses_source',mismatch,mismatch>.1)
    output={'result':'minimal common MOND plus polar-clock action has a nonconstant independent lapse source; constant vacuum subtraction does not cancel it',
            'number_of_checks':len(checks),'checks':checks,
            'graph':{'nodes':size,'mode':mode,'discrete_wave_number_squared':float(kh2),'predicted_density_susceptibility':float(-predicted_rho[0])},
            'non_claims':['Not a full solution of common-action metric and clock constraints','No borrowing the bare-action no-slip relation','Weak-static AQUAL uses measured G and specified approximation; exact statement is the static lapse source','No all-theory no-go for extra constrained fields or interactions','Finite graph has a prescribed lapse and tests the radial/source response, not a galaxy fit']}
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__': main()
