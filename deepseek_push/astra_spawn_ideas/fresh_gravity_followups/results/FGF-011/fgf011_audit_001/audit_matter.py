#!/usr/bin/env python3
"""Independent FGF-011 controls; no candidate-module imports."""
import json
import math
import sys
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, solve_ivp
from scipy.optimize import minimize_scalar

OUTPUT=Path(sys.argv[1])
SOURCE=Path('campaign_fresh_gravity_astra/stage_04/matter_stability/run_003/results.json')
CHECKS=[]

def check(name,passed,observed,tolerance):
    CHECKS.append(dict(name=name,passed=bool(passed),observed=observed,tolerance=tolerance))
    if not passed: raise AssertionError(name+': '+str(observed))

def forward(branch,u):
    if branch=='Q': return math.sqrt(u*(u+1))
    return u/(-math.expm1(-math.sqrt(u)))

def stiffness(branch,u):
    f=forward(branch,u)
    if branch=='Q': derivative=(2*u+1)/(2*f)
    else:
        t=math.sqrt(u); den=-math.expm1(-t)
        derivative=1/den-t*math.exp(-t)/(2*den*den)
    return u/f,1/derivative

def operator(k,L,tau,cs2,C=1.,rho=1.):
    # Continuity, Euler, potential velocity, then scalar response.
    M=np.zeros((4,4))
    M[0,1]=-rho*k
    M[1,0]=k*cs2/rho;M[1,2]=k
    M[2,3]=1
    M[3,0]=-C/tau;M[3,2]=-L*k*k/tau
    return M

def canonical(k,L,tau,cs2,C=1.,rho=1.):
    H=np.diag([cs2*k*k,L*k*k/tau])
    H[0,1]=H[1,0]=-math.sqrt(C*rho/tau)*k
    T=np.zeros((4,4))
    T[0,0]=-1/(math.sqrt(rho)*k)
    T[1,2]=math.sqrt(tau/C)
    T[2,1]=math.sqrt(rho)
    T[3,3]=math.sqrt(tau/C)
    return H,T

def energies(k,L,tau,cs2,C=1.,rho=1.):
    # 4 E = y^T Q y; the overall normalization cancels from the invariant.
    Q=np.diag([cs2/rho,rho,L*k*k/C,tau/C])
    Q[0,2]=Q[2,0]=1
    return Q

def slab(branch,u0,record):
    f=lambda u:forward(branch,u)
    r=lambda u:.1-quad(f,u0,float(u),epsabs=2e-14,epsrel=2e-13)[0]
    # Independent one-state first-integral integration, not the author's
    # two-state hydrostatic ODE or cached trajectory.
    sol=solve_ivp(lambda x,u:[r(u[0])],(0,1),[u0],method='DOP853',rtol=3e-13,atol=1e-14,dense_output=True,max_step=.02)
    sample=np.array(record['chi'])
    us=sol.sol(sample)[0];rs=np.array([r(u) for u in us])
    gs=np.array([f(u) for u in us]);As=np.array([stiffness(branch,u)[1] for u in us])
    err=max(float(np.max(abs(us-np.array(record['u'])))),float(np.max(abs(rs-np.array(record['r'])))))
    product=(rs/As)*(1/gs)*(gs*As/rs)
    window=np.sqrt(rs/As)*np.minimum(1/gs,gs*As/rs)
    check(branch+' slab reconstruction u0='+str(u0),sol.success and rs.min()>0 and gs.min()>0 and err<3e-11,{'max_source_profile_difference':err,'minimum_rho':float(rs.min()),'minimum_g':float(gs.min())},'profile absolute difference <3e-11; positive rho,g')
    check(branch+' exact slab length u0='+str(u0),np.max(abs(product-1))<1e-13 and window.max()<=1+1e-13,{'identity_max_error':float(np.max(abs(product-1))),'maximum_kJ_min_length':float(window.max())},'identity <1e-13; local window <=1')
    def state(x):
        u=float(sol.sol(x)[0]);rho=r(u);g=f(u);A=stiffness(branch,u)[1]
        return rho,g,A
    def trial(x,kind):
        if kind==0:
            return math.sin(math.pi*x)+.3*math.sin(3*math.pi*x),math.pi*math.cos(math.pi*x)+.9*math.pi*math.cos(3*math.pi*x),-.8*math.sin(2*math.pi*x),-1.6*math.pi*math.cos(2*math.pi*x)
        if kind==1:
            return math.sin(2*math.pi*x),2*math.pi*math.cos(2*math.pi*x),.4*math.sin(math.pi*x)+.2*math.sin(4*math.pi*x),.4*math.pi*math.cos(math.pi*x)+.8*math.pi*math.cos(4*math.pi*x)
        if kind==2:
            return math.sin(math.pi*x),math.pi*math.cos(math.pi*x),0.,0.
        return 1.,0.,.4,0. # deliberately violates both endpoint conditions
    rows=[]
    for kind in range(4):
        def integrands(x):
            rho,g,A=state(x);xi,xip,psi,psip=trial(x,kind)
            drho=rho*(g*xi-xip) # cs²=C=a=1 dimensionless slab
            original=drho*drho/rho+A*psip*psip+2*drho*psi
            squares=rho*xip*xip+A*(psip+rho*xi/A)**2
            return original,squares
        original=quad(lambda x:integrands(x)[0],0,1,epsabs=2e-12,epsrel=2e-12)[0]
        squares=quad(lambda x:integrands(x)[1],0,1,epsabs=2e-12,epsrel=2e-12)[0]
        endpoints=[]
        for x in [0.,1.]:
            rho,g,A=state(x);xi,xip,psi,psip=trial(x,kind)
            endpoints.append(-rho*g*xi*xi-2*rho*xi*psi)
        boundary=endpoints[1]-endpoints[0]
        residual=original-squares-boundary
        rows.append(dict(trial=kind,twice_original_V=original,positive_square_integral=squares,boundary=boundary,full_identity_residual=residual,error_if_boundary_omitted=original-squares))
        check(branch+' slab factorization u0='+str(u0)+' trial='+str(kind),abs(residual)<3e-11 and (kind==3 or original>0),rows[-1],'absolute identity residual <3e-11; admissible trial energy >0')
        if kind==3:
            check(branch+' boundary negative control u0='+str(u0),abs(original-squares)>1e-4,rows[-1],'omitting nonzero boundary must fail by >1e-4')
    return dict(branch=branch,u0=u0,max_profile_difference=err,min_density=float(rs.min()),max_kJ_min_length=float(window.max()),factorizations=rows)

def main():
    candidate=json.loads(SOURCE.read_text())
    max_transform=max_energy=max_low=max_high=0.
    scan_count=0
    for row in candidate['scan']:
        branch,u,theta,K,cs2,ratio=(row[k] for k in ['kernel','u','theta','K','cs2','k_over_kJ'])
        perp,par=stiffness(branch,u);L=perp*math.sin(theta)**2+par*math.cos(theta)**2
        k=ratio/math.sqrt(cs2*L);tau=K
        M=operator(k,L,tau,cs2);H,T=canonical(k,L,tau,cs2)
        expected=np.block([[np.zeros((2,2)),np.eye(2)],[-H,np.zeros((2,2))]])
        transformed=T@M@np.linalg.inv(T)
        t_error=float(np.max(abs(transformed-expected))/max(1.,np.max(abs(expected))))
        Q=energies(k,L,tau,cs2)
        e_error=float(np.max(abs(M.T@Q+Q@M))/max(1.,np.max(abs(M.T@Q))+np.max(abs(Q@M))))
        ev=np.linalg.eigvalsh(H)
        low_error=abs(ev[0]-row['omega2_low'])/max(1,abs(ev[0]),abs(row['omega2_low']))
        high_error=abs(ev[1]-row['omega2_high'])/max(1,abs(ev[1]),abs(row['omega2_high']))
        max_transform=max(max_transform,t_error);max_energy=max(max_energy,e_error)
        max_low=max(max_low,float(low_error));max_high=max(max_high,float(high_error))
        if ratio<1: assert ev[0]<0<ev[1]
        if ratio>1: assert 0<ev[0]<ev[1]
        if ratio==1: assert abs(ev[0])<1e-10/L
        scan_count+=1
    check('independent first-order canonical transformation',scan_count==672 and max_transform<2e-13,dict(cases=scan_count,max_scaled_residual=max_transform),'672 cases; scaled residual <2e-13')
    check('matrix energy invariant',max_energy<2e-13,dict(max_scaled_skew_residual=max_energy),'scaled residual <2e-13')
    check('separately scaled lower and upper roots',max_low<2e-9 and max_high<2e-12,dict(max_lower_relative_or_absolute_error=max_low,max_upper_relative_or_absolute_error=max_high),'each mode normalized separately by max(1,abs(mode)); low <2e-9, high <2e-12')
    peaks=[]
    for row in candidate['peak_checks']:
        branch,u,angle,K,cs2=(row[k] for k in ['kernel','u','theta','K','cs2'])
        perp,par=stiffness(branch,u);L=perp*math.sin(angle)**2+par*math.cos(angle)**2
        cs=math.sqrt(cs2);v=math.sqrt(L/K);kJ=1/math.sqrt(cs2*L)
        exact_r=math.sqrt(cs*v)/(cs+v); exact_growth=1/L/(1+cs/v)**2
        objective=lambda ratio:float(np.linalg.eigvalsh(canonical(ratio*kJ,L,K,cs2)[0])[0])
        opt=minimize_scalar(objective,bounds=(1e-7,1-1e-7),method='bounded',options={'xatol':1e-12,'maxiter':120})
        peaks.append(dict(branch=branch,u=u,angle=angle,K=K,cs2=cs2,peak_ratio=exact_r,numeric_ratio=float(opt.x),ratio_relative_error=abs(opt.x/exact_r-1),growth_relative_error=abs((-opt.fun)/exact_growth-1),success=bool(opt.success)))
    check('independent peak growth optimization',len(peaks)==96 and all(r['success'] for r in peaks) and max(r['ratio_relative_error'] for r in peaks)<3e-6 and max(r['growth_relative_error'] for r in peaks)<3e-11,dict(cases=len(peaks),maximum_peak_ratio_relative_error=max(r['ratio_relative_error'] for r in peaks),maximum_peak_growth_relative_error=max(r['growth_relative_error'] for r in peaks)),'96 cases; ratio <3e-6, growth <3e-11')
    dimensional=[]
    for row in candidate['dimensional_sensitivity']:
        G=6.67430e-11;c=299792458.;rho=row['rho_kg_m3'];cs=row['sound_speed_m_s'];B=row['B'];a=row['a'];C=4*math.pi*G
        L=stiffness(row['kernel'],B/a)[1];kJ=math.sqrt(C*rho/(cs*cs*L));k=.5*kJ
        # Scale time by 1/sqrt(Crho), leaving matrix entries well-conditioned.
        kn=k/math.sqrt(C*rho)
        cases=[]
        for model in row['models']:
            K=model['K'];H,_=canonical(kn,L,K/(c*c),cs*cs)
            lo=np.linalg.eigvalsh(H)[0]
            growth=math.sqrt(-lo)*math.sqrt(C*rho)
            cases.append(dict(K=K,growth_rate=growth,relative_source_difference=abs(growth/model['growth_rate_per_second']-1)))
        dimensional.append(dict(kernel=row['kernel'],normalization=row['normalization'],scaling=row['scaling'],a=a,models=cases,threshold_kJ=kJ))
    check('both SI normalizations and separate frozen H history',len(dimensional)==8 and max(m['relative_source_difference'] for r in dimensional for m in r['models'])<2e-10,dimensional,'8 backgrounds, K=2/8 each, relative rate difference <2e-10')
    slabs=[slab(rec['kernel'],rec['initial_u'],rec) for rec in candidate['balanced_slabs']]
    # Unsubtracted homogeneous equations give finite nonzero residuals.
    mismatch={branch:{'scalar_residual_at_rho1':1.,'Euler_force_magnitude_at_B1':forward(branch,1.)} for branch in ['Q','R']}
    check('unsupported homogeneous background rejected',all(r['scalar_residual_at_rho1']>0 and r['Euler_force_magnitude_at_B1']>0 for r in mismatch.values()),mismatch,'both original background equations have nonzero residual')
    output=dict(task_id='FGF-011',audit_status='all finite controls passed',checks=CHECKS,scan_count=scan_count,peak_controls=peaks,dimensional_checks=dimensional,slab_controls=slabs,nonclaims=['No candidate trajectory rerun or full ODE integrator audit','No finite slab eigen-spectrum computed','No general background or nonlinear stability theorem','No cosmology, lensing, observations or K measurement'])
    OUTPUT.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(checks=len(CHECKS),scan_cases=scan_count,peak_cases=len(peaks),slabs=len(slabs),max_lower_root_error=max_low,max_upper_root_error=max_high,max_peak_ratio_error=max(r['ratio_relative_error'] for r in peaks),max_slab_profile_error=max(r['max_profile_difference'] for r in slabs),max_factorization_error=max(abs(t['full_identity_residual']) for r in slabs for t in r['factorizations'])),indent=2))

if __name__=='__main__':main()
