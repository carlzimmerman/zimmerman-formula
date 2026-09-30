"""Frozen-curvature weak-static diagnostic, not a full metric/clock solution."""
import argparse
import json
import math
import numpy as np
from scipy.integrate import solve_bvp
from scipy.optimize import brentq

G=1/(8*math.pi)
K=16.
ELL=10.
L=0.01
COMPACTNESS=0.001
qstar=brentq(lambda q:-2/q**3+2*q+3*ELL*(q**-2+q*q)/(2+3*ELL*q),3**(-0.25),1,xtol=1e-14)
H=math.sqrt(2*(qstar**-2+qstar*qstar)/(3*(2+3*ELL*qstar)))
C=4.5*H*H*ELL
D=12*math.pi*G*(2*K*K)**(1/3)
checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
def base_force(q,delta):
    return delta*(2*(q*q+q*qstar+qstar*qstar)/(q**3*qstar**3)+2)
def source(q,b): return K*(b/(12*math.pi*G*K*q))**1.5
def local_delta(b):
    if b==0: return 0.
    def scaled(delta):
        q=qstar+delta
        return delta*(2*(q*q+q*qstar+qstar*qstar)/qstar**3+2*q**3)+K*(b/(12*math.pi*G*K))**1.5*q**1.5
    return brentq(scaled,-qstar*(1-1e-12),0.,xtol=1e-20)
def local_root(b): return qstar+local_delta(b)
rows=[]
cases=((0.001,1.,1e-6,0.01),(0.0001,1.,1e-6,0.01),(0.00001,1.,1e-6,0.01),(0.000001,1.,1e-6,0.01),(0.000001,1e-14,1e-6,0.01),(0.000001,1e-14,1e-7,0.01),(0.000001,1e-14,1e-6,0.02),(0.000001,1.,1e-6,0.02))
for radius,Z,inner_factor,L in cases:
    gm=COMPACTNESS*radius
    r=np.geomspace(radius*inner_factor,L,1000)
    if Z<1:
        boundary_length=math.sqrt(Z/(6/qstar**4+2))
        extra=L-np.geomspace(boundary_length/100,min(L/2,100*boundary_length),180)
        r=np.unique(np.concatenate((r,extra)))
    def flux(r): return gm*r/(r*r+radius*radius)**1.5
    def ode(x,y):
        r=radius*np.exp(x)
        q=qstar+y[0]
        if np.any(q<=0): raise ValueError('nonpositive q in boundary iteration')
        return np.vstack((y[1],r*r*(base_force(q,y[0])+source(q,flux(r)))/Z-y[1]))
    def bc(left,right): return np.array([left[1],right[0]])
    if Z==1:
        guess=np.zeros((2,len(r)))
    else:
        deltas=np.array([local_delta(b) for b in flux(r)])
        roots=qstar+deltas
        b=flux(r); src=source(roots,b)
        fp=6/roots**4+2-1.5*src/roots
        blog=np.zeros_like(r)
        blog[1:]=1/r[1:]-3*r[1:]/(r[1:]*r[1:]+radius*radius)
        derivative=-1.5*src*blog/fp
        boundary_delta=local_delta(float(flux(L)))
        layer=boundary_delta*np.exp((r-L)/boundary_length)
        guess=np.vstack((deltas-layer,r*(derivative-layer/boundary_length)))
        guess[0,-1]=0
    x=np.log(r/radius)
    sol=solve_bvp(ode,bc,x,guess,tol=1e-6,max_nodes=20000)
    label=str((radius,Z,inner_factor,L))
    check('BVP convergence '+label,sol.success)
    if not sol.success:
        print('failed case',label,'nodes',len(sol.x),'residual max',float(np.max(sol.rms_residuals)),'residual radius',float(radius*np.exp(sol.x[np.argmax(sol.rms_residuals)])),'boundary',bc(sol.y[:,0],sol.y[:,-1]))
        raise RuntimeError(sol.message)
    sample=np.geomspace(radius*inner_factor,L,1000)
    q=qstar+sol.sol(np.log(sample/radius))[0]
    check('positive scalar '+label,float(np.min(q))>0)
    check('boundary residual '+label,float(np.max(np.abs(bc(sol.y[:,0],sol.y[:,-1]))))<1e-10)
    peak=radius/math.sqrt(2)
    qp=float(qstar+sol.sol(math.log(peak/radius))[0]); bp=float(flux(peak))
    pp=math.sqrt(bp/(12*math.pi*G*K*qp))
    qa=local_root(bp); pa=math.sqrt(bp/(12*math.pi*G*K*qa))
    ratio=1+pp/bp
    adratio=1+pa/bp
    if Z==1:
        check('gradient-retained branch stays near cosmic scalar '+label,float(np.max(np.abs(q/qstar-1)))<1e-3)
    else:
        check('small kinetic normalization approaches local root '+label,abs(qp/qa-1)<0.01)
    ps=np.sqrt(flux(sample)/(12*math.pi*G*K*q))
    gs=flux(sample)+ps
    potential_estimate=float(np.trapz(gs,sample))
    curvature_proxy=float(np.max((H*sample)**2/(ps*(12*math.pi*G*K*qstar))))
    check('weak sourced potential estimate '+label,potential_estimate<0.01)
    check('small static curvature correction proxy '+label,curvature_proxy<0.01)
    rows.append({'potential_integral_estimate':potential_estimate,'maximum_static_curvature_proxy':curvature_proxy,'source_radius' :radius,'inner_radius':radius*inner_factor,'outer_radius':L,'Z':Z,'bare_GM':gm,'compactness_GM_over_R':COMPACTNESS,'solver_nodes':len(sol.x),'largest_collocation_residual':float(np.max(sol.rms_residuals)),'minimum_q':float(np.min(q)),'maximum_relative_q_departure':float(np.max(np.abs(q/qstar-1))),'peak_flux_radius':peak,'peak_b':bp,'q_at_peak':qp,'local_root_q_at_peak':qa,'g_over_b_at_peak':ratio,'local_relaxation_g_over_b_at_peak':adratio,'formal_adiabatic_Newton_ratio':1+1/D})
small=[r for r in rows if r['Z']<1]
check('small-Z peak independent of inner and outer boundaries',max(abs(r['q_at_peak']/small[0]['q_at_peak']-1) for r in small)<1e-5)
locked=[r for r in rows if r['Z']==1 and r['source_radius']==1e-6]
check('locked peak independent of outer boundary',max(abs(r['q_at_peak']/locked[0]['q_at_peak']-1) for r in locked)<1e-5)
result={'passed' :all(c['passed'] for c in checks),'checks':checks,'qstar':qstar,'H':H,'fixed_curvature_scalar_force':C,'D':D,'outer_radii':[0.01,0.02],'samples':rows}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
for row in rows: print(json.dumps(row))
raise SystemExit(0 if result['passed'] else 1)
