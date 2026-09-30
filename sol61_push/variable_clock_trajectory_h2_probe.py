"""Bounded homogeneous radiation/clock trajectories, dimensionless toy units."""
import argparse
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as s

RHO0=1e8
NEND=12.
GRID=np.linspace(0,NEND,1201)
checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
def potential(q): return q**-2+q*q
def slope(q): return -2*q**-3+2*q
def constraint_h2(n,q,w,ell):
    denominator=3*(2+3*ell*q)-q*q*w*w
    if denominator<=0: raise ValueError('nonpositive expanding-branch constraint denominator')
    return 2*(RHO0*math.exp(-4*n)+potential(q))/denominator
def deriv(n,state,ell,independent=False):
    x,w=state[:2]
    q=math.exp(x)
    H2=state[2] if independent else constraint_h2(n,q,w,ell)
    rho=RHO0*math.exp(-4*n)
    S=2+3*ell*q
    v=q*w
    hp=-(4*rho/(3*H2)+v*v)/S-3*ell*v/S
    wp=-w*w-(3+hp)*w-(slope(q)+4.5*ell*H2)/(H2*q)
    return [w,wp,2*hp*H2] if independent else [w,wp]
def root(ell,rho):
    return brentq(lambda q:slope(q)+3*ell*(rho+potential(q))/(2+3*ell*q),1e-9,1,xtol=1e-14)
# Orthogonal exact check: the absolute lapse-constraint error is conserved
# by the independently evolved acceleration/scalar equations.
Q,V,H,R,P,U,UP,S,SP=s.symbols('Q V H R P U UP S SP',real=True)
hdot=-(R+P+V*V)/S-SP*H*V/S
v_dot=-3*H*V-UP-s.Rational(3,2)*SP*H*H
E_dot=s.Rational(3,2)*SP*V*H*H+3*S*H*hdot-UP*V-V*v_dot+3*H*(R+P)
check('exact absolute constraint-error conservation',s.simplify(E_dot)==0)
rows=[]
for ell,offset,w0 in ((0.1,1.,4/3),(1.,1.,4/3),(10.,1.,4/3),(10.,0.9,0.),(10.,1.1,0.)):
    label=str((ell,offset,w0))
    q0=root(ell,RHO0)*offset
    initial=[math.log(q0),w0]
    sol=solve_ivp(lambda n,y:deriv(n,y,ell),(0,NEND),initial,method='Radau',rtol=1e-8,atol=1e-10,max_step=0.02,t_eval=GRID)
    check('integration completed '+label,sol.success and sol.t[-1]==NEND)
    if not sol.success: raise RuntimeError(sol.message)
    qs=np.exp(sol.y[0]); ws=sol.y[1]
    hs=np.array([constraint_h2(n,q,w,ell) for n,q,w in zip(GRID,qs,ws)])
    ss=2+3*ell*qs
    kin=0.5*hs*(qs*ws)**2
    rhos=RHO0*np.exp(-4*GRID)
    pot=potential(qs)
    denominators=3*ss-(qs*ws)**2
    qvac=root(ell,0.)
    hvac=2*potential(qvac)/(3*(2+3*ell*qvac))
    check('positive constraint denominator '+label,float(np.min(denominators))>0)
    check('late vacuum approached '+label,abs(qs[-1]/qvac-1)<1e-5 and abs(hs[-1]/hvac-1)<1e-5 and abs(ws[-1])<1e-4)
    # Standard reference uses bare G, not yet an observed Newton calibration.
    expansion_bare=3*hs/rhos
    rows.append({'ell':ell,'q_offset':offset,'initial_log_q_derivative':w0,'function_evaluations':sol.nfev,'q_initial':q0,'q_final':float(qs[-1]),'q_vacuum':qvac,'lambda_initial':1+ell*q0,'lambda_final':1+ell*float(qs[-1]),'H_squared_final':float(hs[-1]),'H_squared_vacuum':hvac,'final_log_q_derivative':float(ws[-1]),'minimum_constraint_denominator':float(np.min(denominators)),'maximum_scalar_kinetic_fraction_of_total':float(np.max(kin/(rhos+pot+kin))),'initial_H_squared_over_bare_GR_radiation':float(expansion_bare[0]),'selected_states':[{'N':float(GRID[i]),'rho':float(rhos[i]),'q':float(qs[i]),'lambda':float(1+ell*qs[i]),'kinetic_fraction':float(kin[i]/(rhos[i]+pot[i]+kin[i]))} for i in (0,100,200,400,600,800,1200)]})
    if ell==10 and offset==1:
        initial_full=initial+[hs[0]]
        alt=solve_ivp(lambda n,y:deriv(n,y,ell,True),(0,NEND),initial_full,method='Radau',rtol=2e-12,atol=2e-14,max_step=0.005,t_eval=GRID)
        check('independent acceleration integration completed',alt.success and alt.t[-1]==NEND)
        aq=np.exp(alt.y[0]); aw=alt.y[1]; ah=alt.y[2]
        ach=np.array([constraint_h2(n,q,w,ell) for n,q,w in zip(GRID,aq,aw)])
        residual=float(np.max(np.abs(ah/ach-1)))
        qdifference=float(np.max(np.abs(aq/qs-1)))
        hdifference=float(np.max(np.abs(ah/hs-1)))
        check('independent constraint preservation',residual<1e-6)
        check('independent trajectory agreement',qdifference<1e-5 and hdifference<1e-5)
        rows[-1]['independent_constraint_max_relative_residual']=residual
        rows[-1]['independent_max_relative_q_difference']=qdifference
        rows[-1]['independent_max_relative_H_squared_difference']=hdifference
result={'passed':all(c['passed'] for c in checks),'checks':checks,'domain':{'rho_initial':RHO0,'e_folds':[0,NEND],'A_B_M2_Z':1,'ordinary_matter':'radiation only'},'trajectories':rows}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(str(sum(c['passed'] for c in checks))+'/'+str(len(checks))+' checks passed')
for row in rows: print(json.dumps({k:v for k,v in row.items() if k!='selected_states'}))
raise SystemExit(0 if result['passed'] else 1)
