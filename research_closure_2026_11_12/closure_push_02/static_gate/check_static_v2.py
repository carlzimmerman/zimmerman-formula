#!/usr/bin/env python3
"""Finite static-gate checks. Reference-profile tests are not field solutions."""
import argparse,json,math
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_bvp,cumulative_trapezoid,simpson
from scipy.optimize import brentq
import sympy as sp

A0=9.3603e-11; G=6.674e-11; MSUN=1.989e30; MPC=3.0857e22; C=299792458.
I0=4.0369171448880406e-8; LSTAR_MPC=22e-6

def gate(u):
    """Literal flat gate, with underflow to zero allowed. Positive accepted inputs."""
    with np.errstate(under='ignore',over='ignore',invalid='ignore'):
        S=np.exp(-u**3)
        return S,-3*u*u*S,(9*u**4-6*u)*S

def symbolic():
    x=sp.symbols('x',positive=True); m,d,l=sp.symbols('m d l',positive=True)
    f=sp.Function('f')(x); p=sp.Function('p')(x); b=sp.Function('b')(x)
    Z=sp.diff(p,x)+2*p/x; S=sp.Function('S'); u=Z/d
    Lag=x*x*(-sp.diff(f,x)**2/2+p*sp.diff(f,x)+p+sp.log(1-p)+m*m*f*f*S(u)/2-l*l*Z*Z/4-b*f)
    ef=sp.diff(Lag,f)-sp.diff(sp.diff(Lag,sp.diff(f,x)),x)
    ep=sp.diff(Lag,p)-sp.diff(sp.diff(Lag,sp.diff(p,x)),x)
    B=l*l*Z/2-m*m*f*f*sp.Subs(sp.Derivative(S(sp.Symbol('t')),sp.Symbol('t')),sp.Symbol('t'),u)/(2*d)
    expected_f=x*x*(sp.diff(f,x,2)+2*sp.diff(f,x)/x-Z+m*m*f*S(u)-b)
    expected_p=x*x*(sp.diff(f,x)+sp.diff(B,x)-p/(1-p))
    rf=sp.simplify(ef-expected_f); rp=sp.simplify(ep-expected_p)
    assert rf==0 and rp==0
    # Mutant deletes precisely the gate contribution to B. It must fail identically.
    mutant=sp.simplify(ep-x*x*(sp.diff(f,x)+l*l*sp.diff(Z,x)/2-p/(1-p)))
    assert mutant!=0
    # Independent closed-form point-source profile identities.
    s=sp.sqrt(1+4*x*x); y=(1+s)/(2*x*x); pp=2/(1+s); ZZ=2/(x*s)
    assert sp.simplify(y-pp/(1-pp))==0
    assert sp.simplify(sp.diff(pp,x)+2*pp/x-ZZ)==0
    assert sp.simplify(sp.diff(y-pp,x)+2*(y-pp)/x)==0
    return {'Euler_Lagrange_f_residual':str(rf),'Euler_Lagrange_p_residual':str(rp),'delete_gate_gradient_mutation_detected':True,'point_AQUAL_identities_exact':True}

def reference(x,R=60.):
    s=np.sqrt(1+4*x*x); y=(1+s)/(2*x*x); p=2/(1+s)
    Z=2/(x*s); Zp=-2*(1+8*x*x)/(x*x*(1+4*x*x)**1.5)
    f=np.arcsinh(2*x)-(1+s)/(2*x)-np.arcsinh(2*R)
    return f,y,p,Z,Zp

def gradient_audit():
    x=np.geomspace(1.,60.,4001); f,y,p,Z,Zp=reference(x)
    a=A0/C**2*MPC; ZR=Z[-1]; rows=[]
    for Mb in [1e9,1e10,1e11,1e12]:
      rM=math.sqrt(G*MSUN*Mb/A0)/MPC; eps=a*rM
      for mu in [198.25,25120.]:
        m=mu*rM
        def calc(uR):
            d=ZR/uR; u=Z/d; S,Sp,Spp=gate(u)
            gval=eps*m*m*f*f*Sp/(2*d)
            derivative=(m*m/d)*(f*y*Sp+f*f*Spp*Zp/(2*d))
            ratio=np.abs(derivative/y)
            return {'u_R':uR,'d':d,'xi':2*a*d/(I0*rM),'S_R':float(S[-1]),'max_abs_G':float(np.max(np.abs(gval))),'max_grad_G_over_g':float(np.max(ratio)),'x_at_max_grad':float(x[np.argmax(ratio)]),'local_dust_over_Pi_R':float(m*m*abs(f[-1])*S[-1]/ZR),'min_u':float(u.min()),'max_u':float(u.max())}
        umass=(2*math.log(mu))**(1/3)
        mass=calc(umass)
        root=brentq(lambda u:math.log(max(calc(u)['max_grad_G_over_g'],1e-300)/1e-3),umass,8.,xtol=1e-12)
        rows.append({'Mb_Msun':Mb,'mu_per_Mpc':mu,'rM_Mpc':rM,'epsilon':eps,'mass_only_ceiling':mass,'gradient_tolerance_boundary':calc(root)})
    return {'profile':'point simple-mu AQUAL, 1<=r/rM<=60, potential matched at60 to Kepler value; reference only','sample_count':len(x),'rows':rows}

def tail_scales():
    xe=.013184165725664278; mue=xe/(1+xe); Le=1/(1+xe); eta=2*Le
    rows=[]
    for mu in [198.25,25120.]:
      for direct,v in [('transverse',1/(1+xe)),('parallel',1/(1+xe)**2)]:
        beta=LSTAR_MPC**2*v/2; aa=1-v-beta*mu*mu
        disc=math.sqrt(aa*aa+4*beta*mu*mu)
        # Stable quadratic roots, product=-mu²/beta.
        positive=2*mu*mu/(aa+disc) if aa>=0 else (-aa+disc)/(2*beta)
        negative=-mu*mu/(beta*positive)
        residual=abs(beta*positive**2+aa*positive-mu*mu)/(mu*mu)
        assert residual<1e-10 and negative<0<positive
        rows.append({'mu_per_Mpc':mu,'direction':direct,'v':v,'beta_Mpc2':beta,'osc_inverse_k_pc':1e6/math.sqrt(positive),'yukawa_decay_pc':1e6/math.sqrt(-negative),'no_stiffness_inverse_k_pc':1e6*math.sqrt(1-v)/mu,'positive_root_relative_residual':residual})
    transition=[]
    for mu in [198.25,25120.]:
      for rt in [.01,.1,1.]:
        rcharge=(mu*rt)**2/(math.e*eta)
        transition.append({'mu_per_Mpc':mu,'transition_r_Mpc':rt,'pole_eta':eta,'abs_gate_gradient_over_g':1.5*rcharge,'HQ_over_Pi':rcharge,'H_PiPi_over_gamma':3*(mu*rt)**2*(rt/LSTAR_MPC)**2/(math.e*eta**2),'gamma_gradient_over_g':1.5*eta*(LSTAR_MPC/rt)**2})
    limits=[{'mu_per_Mpc':mu,'largest_transition_r_pc_for_gate_gradient_1e_minus3':1e6*math.sqrt(1e-3*2*math.e*eta/3)/mu} for mu in [198.25,25120.]]
    return {'xe':xe,'mu_e':mue,'L_e':Le,'Lstar_pc':LSTAR_MPC*1e6,'directional_roots':rows,'EFE_pole_transition_reference':transition,'perturbative_transition_bounds':limits}

def one_bvp(m,tol,previous=None):
    # Purpose: execute the fully coupled four-equation system on a smooth finite box.
    # ell=.2 is a solver benchmark, not a physical galaxy fit.
    ell=.2; d=.01; inner=.001; outer=60.; soft=.5
    x=np.geomspace(inner,outer,250)
    gn=x/(x*x+soft*soft)**1.5
    y=(gn+np.sqrt(gn*gn+4*gn))/2; p=y/(1+y)
    f=-x[-1]*y[-1]-np.flip(cumulative_trapezoid(np.flip(y),-np.flip(x),initial=0))
    Z=np.gradient(p,x)+2*p/x
    initial=np.vstack((f,y,p,Z)) if previous is None else previous.sol(x)
    trial_clip_count=[0]
    def fun(r,z):
        f,y,p,Z=z; u=Z/d
        clipped=np.clip(u,-2.,15.)
        trial_clip_count[0]+=int(np.count_nonzero(u!=clipped))
        S,Sp,Spp=gate(clipped)
        D=ell*ell/2-m*m*f*f*Spp/(2*d*d)
        b=3*soft*soft/(r*r+soft*soft)**2.5
        return np.vstack((y,b+Z-m*m*f*S-2*y/r,Z-2*p/r,(p/(1-p)-y+m*m*f*y*Sp/d)/D))
    def bc(za,zb):return np.array([za[1],za[2],zb[0]+outer*y[-1],zb[2]-p[-1]])
    with np.errstate(all='ignore'):
        sol=solve_bvp(fun,bc,x,initial,tol=tol,max_nodes=12000)
    r=np.geomspace(inner,outer,5001); z=sol.sol(r); dz=sol.sol(r,1); f,y,p,Z=z
    S,Sp,Spp=gate(Z/d)
    D=ell*ell/2-m*m*f*f*Spp/(2*d*d)
    b=3*soft*soft/(r*r+soft*soft)**2.5
    constitutive=y+ell*ell*dz[3]/2-m*m*f*y*Sp/d-m*m*f*f*Spp*dz[3]/(2*d*d)-p/(1-p)
    poisson=dz[1]+2*y/r-b-Z+m*m*f*S
    regular=bool(np.all(np.isfinite(z)) and np.min(Z)>=0 and np.min(p)>-1e-10 and np.max(p)<1 and np.min(D)>0)
    accepted=bool(sol.status==0 and regular and np.max(np.abs(constitutive))<50*tol and np.max(np.abs(poisson))<50*tol)
    flux_left=outer**2*y[-1]-inner**2*y[0]
    flux_right=simpson(r*r*(b+Z-m*m*f*S),x=r)
    record={'m':m,'tol':tol,'solver_status':int(sol.status),'solver_message':sol.message,'nodes':len(sol.x),'max_rms_residual':float(np.max(sol.rms_residuals)),'accepted_as_finite_benchmark':accepted,'positive_Pi_p_under1_positive_D':regular,'Dmin':float(np.min(D)),'pmin':float(np.min(p)),'pmax':float(np.max(p)),'umin':float(np.min(Z/d)),'umax':float(np.max(Z/d)),'max_constitutive_residual_unclipped':float(np.max(np.abs(constitutive))),'max_Poisson_residual_unclipped':float(np.max(np.abs(poisson))),'relative_integrated_Poisson_flux_residual':float(abs(flux_left-flux_right)/max(abs(flux_left),1)),'trial_clipped_evaluations':trial_clip_count[0],'accepted_gate_all_clipping_only_positive_underflow':bool(np.min(Z/d)>=0),'boundary_residual_max':float(np.max(np.abs(bc(sol.y[:,0],sol.y[:,-1]))))}
    return sol,record

def bvp_checks():
    records=[]; old=None; accepted=[]
    for m in [0.,1e-5,1e-4,3e-4,1e-3]:
        sol,row=one_bvp(m,1e-5,old); records.append(row)
        if row['accepted_as_finite_benchmark']:old=sol;accepted.append((m,sol))
    # Refinement is only applied to the last regular continuation solution.
    m,coarse=accepted[-1]; fine,row=one_bvp(m,2e-6,coarse);records.append(row)
    r=np.geomspace(.001,60,5001)
    difference=float(np.max(np.abs(fine.sol(r)-coarse.sol(r))))
    assert row['accepted_as_finite_benchmark'] and difference<.003
    return {'scope':'finite-box solver benchmark; ell=.2,d=.01,Plummer softening=.5,rmin=.001,rmax60, fixed outer f,p and inner y=p=0; no asymptotic halo verdict','records':records,'last_accepted_mesh_refinement_max_abs_difference':difference,'trial_clipping_policy':'Clipping is allowed only in Newton trial evaluations. Acceptance checks original unclipped equations; for u>15 gate and derivatives are below double underflow. Failed runs are not nonexistence proofs.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out={'symbolic':symbolic(),'gradient_audit':gradient_audit(),'tail_scales':tail_scales(),'bvp':bvp_checks()}
    # JSON-standard finite values only; rejected Newton iterates may otherwise contain NaNs.
    nonfinite=[]
    def json_finite(value,path='root'):
        if isinstance(value,dict):return {k:json_finite(v,path+'.'+k) for k,v in value.items()}
        if isinstance(value,list):return [json_finite(v,path+'['+str(i)+']') for i,v in enumerate(value)]
        if isinstance(value,float) and not math.isfinite(value):
            nonfinite.append({'path':path,'value':str(value)})
            return None
        return value
    clean=json_finite(out)
    clean['nonfinite_values_in_rejected_attempts']=nonfinite
    Path(args.output).write_text(json.dumps(clean,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'exact_variation':out['symbolic'],'reference_cases':len(out['gradient_audit']['rows']),'BVP_accepted':sum(x['accepted_as_finite_benchmark'] for x in out['bvp']['records']),'BVP_attempted':len(out['bvp']['records']),'tail_transition_bounds':out['tail_scales']['perturbative_transition_bounds']},indent=2))
