#!/usr/bin/env python3
"""Compare exact clock-constraint preservation with discrete center jets."""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'nonlinear_evolution_2026'))
from evolve import Evolution
from project import project_state,regular_center,radial_profiles
from center import center_expressions


def exact_identity():
    matrix,rhs=center_expressions()
    byname={str(z):z for e in list(matrix)+list(rhs) for z in e.free_symbols}
    def symbol(name):return byname.get(name,s.Symbol(name,real=True))
    ac,q,u1,H,N,N2,Q2,Hd,Qd=s.symbols('a_c Q_c u1 K_c N_c N2 Q2 Hdot_c Qdot_c',real=True)
    W,Wt,WY,WYt,Ptt,Vtt,PXt=map(symbol,['W','W_t','W_Y','W_Yt','P_tt','V_tt','P_Xt'])
    ud=N2*q+N*Q2
    numerator=Ptt-Vtt+2*q*PXt*Qd+6*(Qd*WY*u1+q*WYt*u1+q*WY*ud-2*q*WY*u1*N*H)/ac**2
    chain=3*W*Hd+3*H*Wt-numerator
    action=(matrix*s.Matrix([Hd,Qd,N2])-rhs*s.Matrix([N,1]))[2]
    residual=s.cancel(action-chain)
    if residual!=0:raise AssertionError(str(residual))
    return dict(action_center_preservation_matches_chain_rule=True,
                derivative_defect_multiplier=str(2*q*WY/(ac**2*W)),
                continuum_gradient_jet_rate=str(ud))


def run():
    print(json.dumps(dict(kind='exact',**exact_identity())),flush=True)
    with np.load(HERE.parent/'convergence_repair_2026/run_002/states.npz') as data:
        for index in (1,2):
            r=data['r_'+str(index)];raw=data['state_'+str(index)]
            system=Evolution(.02,.3,len(r),3.,.022,1e-6);t=.02
            state=project_state(t,raw,r,system.model)
            f=system.fields(t,state);rate,_=system.rhs(t,state)
            c=regular_center(t,state,r,system.model);q=c['Q_c'];ac=c['a_c'];u1=c['u1'];H=c['K_c']
            j=system.model.jets(t,q*q,0.);N=f['N'][0];N2=f['rate'][0,3];Qd=f['rate'][0,2]
            actual_Hd=f['rate'][0,1]
            ud_exact=N2*q+N*c['Q2']
            rate_profiles=radial_profiles(r,rate[1],rate[4],rate[5],rate[6],rate[7])
            ud_discrete=float(rate_profiles[2](0.,1))
            def chain(ud):
                numerator=j['P_tt']-j['V_tt']+2*q*j['P_Xt']*Qd
                numerator+=6*(Qd*j['W_Y']*u1+q*j['W_Yt']*u1+q*j['W_Y']*ud-2*q*j['W_Y']*u1*N*H)/ac**2
                return numerator/(3*j['W'])-H*j['W_t']/j['W']
            multiplier=2*q*j['W_Y']/(ac**2*j['W'])
            direct=[]
            for ep in (1e-4,1e-5,1e-6):
                plus=regular_center(t+ep,state+ep*rate,r,system.model)['K_c']
                minus=regular_center(t-ep,state-ep*rate,r,system.model)['K_c']
                direct.append(dict(step=ep,defect=(plus-minus)/(2*ep)-actual_Hd))
            row=dict(points=len(r),Hdot_action=actual_Hd,
                     continuum_chain_defect=chain(ud_exact)-actual_Hd,
                     discrete_chain_defect=chain(ud_discrete)-actual_Hd,
                     gradient_rate_exact=ud_exact,gradient_rate_discrete=ud_discrete,
                     predicted_defect=multiplier*(ud_discrete-ud_exact),multiplier=multiplier,
                     direct_differences=direct)
            if abs(row['continuum_chain_defect'])>1e-10:raise AssertionError(row)
            if abs(row['discrete_chain_defect']-row['predicted_defect'])>1e-10:raise AssertionError(row)
            print(json.dumps(row),flush=True)


if __name__=='__main__':run()
