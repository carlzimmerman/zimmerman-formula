"""Separately dated sextic scalar phase + reciprocal local response candidate.
No identification with old repulsive MeV carrier. No formation/metric proof.
"""
import json,sys,math
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.integrate import solve_bvp,simpson,cumulative_trapezoid
from scipy.special import expit
out=Path(sys.argv[1]);assert out.is_dir()
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)});assert value,name
f,ms,lam,g,om=sy.symbols('f m lambda g omega',positive=True)
f02=lam/(2*g);om02=ms**2-lam**2/(4*g)
V=ms**2*f**2-lam*f**4+g*f**6
check('positive potential decomposition',sy.simplify(V-(om02*f**2+g*f**2*(f**2-f02)**2))==0)
x=sy.symbols('x',real=True);a=sy.symbols('a',positive=True)
profile=f02/(1+sy.exp(2*a*x));fp2=sy.diff(profile,x)**2/(4*profile)
check('planar wall first integral',sy.simplify((fp2-g*profile*(profile-f02)**2).subs(a,sy.sqrt(g)*f02))==0)
sigma=sy.integrate(2*sy.sqrt(g)*f*(f02-f*f),(f,0,sy.sqrt(f02)))
check('wall tension integral',sy.simplify(sigma-sy.sqrt(g)*f02*f02/2)==0)
# Dimensionless example, m=lambda=g=1; chargeN is not auxiliaryQ.
m=1.;L=1.;G=1.;f0sq=.5;omega0=math.sqrt(.75);sigma0=.125;K0=.1;beta=1.
def response(ff,rr,source):
    s=ff*ff/f0sq;K=K0*(1-s)**2;B=beta*s
    D=source*rr/(1+rr*rr)**1.5
    pp=2*D/(K+np.sqrt(K*K+4*B*D)+1e-300)
    W=K*pp*pp/2+B*pp**3/3
    Wf=(K0*(s-1)*pp*pp+beta*pp**3/3)*2*ff/f0sq
    return pp,W,Wf,D,K,B
runs=[]
for Rguess in (20.,40.):
    Ntarget=4*math.pi/3*(2*omega0*f0sq)*Rguess**3
    previous=None
    for source in (0.,.01,.05):
        for refinement in (1,2):
            radius_max=Rguess+50
            mesh=np.linspace(0,radius_max,int(500*refinement))
            if previous is None:
                omega_guess=omega0+2*sigma0/(2*omega0*f0sq*Rguess)
                amp=math.sqrt((1+math.sqrt(1-3*(1-omega_guess**2)))/3)
                u=expit(-(mesh-Rguess));ff=amp*np.sqrt(u);df=-ff*(1-u)/2
                integral=cumulative_trapezoid(8*math.pi*omega_guess*mesh*mesh*ff*ff,mesh,initial=0)
                initial=np.array([ff,df,integral]);par=np.array([omega_guess])
            else:
                initial=previous.sol(mesh);par=previous.p
            def rhs(r,y,p):
                ff,df,nn=y;omega=p[0]
                pp,W,Wf,D,K,B=response(ff,r,source)
                return np.array([df,ff*(1-omega*omega-2*ff*ff+3*ff**4)+Wf/2,
                    8*math.pi*omega*r*r*ff*ff])
            def bc(left,right,p):return np.array([left[1],left[2],right[0],(right[2]-Ntarget)/Ntarget])
            singular=np.zeros((3,3));singular[1,1]=-2
            sol=solve_bvp(rhs,bc,mesh,initial,p=par,S=singular,tol=2e-6/refinement,bc_tol=1e-9,max_nodes=10000)
            check('BVP convergence '+str((Rguess,source,refinement)),sol.success)
            previous=sol
            omega=float(sol.p[0]);rr=np.linspace(0,radius_max,8001)
            ff,df,nn=sol.sol(rr);pp,W,Wf,D,K,B=response(ff,rr,source)
            weight=4*math.pi*rr*rr
            integral=lambda a:float(simpson(weight*a,x=rr))
            I2=integral(ff**2);I4=integral(ff**4);I6=integral(ff**6);T=integral(df**2)
            N=2*omega*I2;Ehost=omega*omega*I2+T+I2-I4+I6
            response_binding=integral(W-D*pp)
            E=Ehost+response_binding
            virial=2*T-3*I4+6*I6+integral(Wf*(1.5*ff+rr*df))
            scale=2*T+3*I4+6*I6+abs(response_binding)
            check('fixed charge quadrature '+str((Rguess,source,refinement)),abs(N/Ntarget-1)<2e-6)
            check('localized frequency '+str((Rguess,source,refinement)),omega0<omega<1)
            check('nodeless amplitude '+str((Rguess,source,refinement)),float(np.min(ff))>-1e-8)
            check('fixed-charge scaling stationarity '+str((Rguess,source,refinement)),abs(virial)/scale<2e-5)
            # actual threshold flags are data, never asserted into passing.
            outer_half=float(rr[np.argmin(abs(ff*ff-f0sq/2))])
            interval=(rr>5)&(rr<.75*outer_half)
            ratio=np.divide(K,B*pp,out=np.full_like(K,np.inf),where=B*pp>0)
            cubic=interval&(ratio<.1)
            # Exact force roots verified where sourced.
            if source>0:
                nonzero=rr>0
                check('force roots '+str((Rguess,source,refinement)),float(np.max(abs((K*pp+B*pp*pp)[nonzero]/D[nonzero]-1)))<1e-10)
            row={'R_initial_guess':Rguess,'source_strength':source,'refinement':refinement,
                'charge_target':Ntarget,'charge_relative_error':N/Ntarget-1,'omega':omega,'omega0':omega0,
                'radius_half_density':outer_half,'radius_over_planar_wall_length':outer_half/2,
                'host_energy_over_mN':Ehost/N,'reduced_total_energy_over_mN':E/N,
                'response_binding':response_binding,'scaling_residual_relative':virial/scale,
                'interior_quadratic_to_cubic_ratio_max':float(np.max(ratio[interval])) if source>0 else None,
                'cubic_interval_rmin':float(np.min(rr[cubic])) if np.any(cubic) else None,
                'cubic_interval_rmax':float(np.max(rr[cubic])) if np.any(cubic) else None,
                'host_free_particle_binding_gate':bool(Ehost/N<1),
                'max_solver_rms_residual':float(np.max(sol.rms_residuals)),
                'tail_amplitude_at_Rminus5':float(sol.sol(radius_max-5)[0])}
            # exterior matching: residual host amplitude small at far radii.
            tailr=np.geomspace(radius_max,1e6,100)
            pext=source*tailr/(1+tailr*tailr)**1.5/K0
            energyext=K0*pext**2/2
            row['exterior_shell_energy_log_slope']=float(np.polyfit(np.log(tailr[-20:]),np.log(4*math.pi*tailr[-20:]**3*energyext[-20:]),1)[0]) if source>0 else None
            runs.append(row)
            if refinement==2:
                low=runs[-2]
                check('frequency refinement '+str((Rguess,source)),abs(omega-low['omega'])<2e-6)
                check('energy refinement '+str((Rguess,source)),abs(row['reduced_total_energy_over_mN']-low['reduced_total_energy_over_mN'])<2e-6)
                if source>0:check('exterior integrable band tail '+str((Rguess,source)),abs(row['exterior_shell_energy_log_slope']+1)<1e-6)
                # Save profiles for physical interpretation/reproducibility.
                np.savez_compressed(out/('profile_R'+str(int(Rguess))+'_S'+str(source)+'.npz'),r=rr,f=ff,df=df,p=pp,D=D,W=W,quadratic_to_cubic_ratio=ratio)
result={'candidate':'Separate sextic charged host plus local reciprocal phase response; fixed external Plummer source','parameters':{'m':m,'lambda':L,'g6':G,'f0_squared':f0sq,'omega0':omega0,'sigma_planar':sigma0,'planar_length':2.,'K0':K0,'beta':beta},'checks':checks,'runs':runs,
 'non_claims':['Not the old positive-square MeV carrier or derived neutral abundance','Chosen nonrenormalizable sextic and switching functions; no UV matching or protected criticality','No formation, charge separation, dynamic stability, metric/lensing or cosmological closure','Source-centered spherical branch only; BVP stationary solutions not proof of global fixed-charge minimum','Local cubic functional, not finite-cutoff nodal determinant; no automatic band/frame matching']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'controls':len(checks),'runs':runs},indent=2))
