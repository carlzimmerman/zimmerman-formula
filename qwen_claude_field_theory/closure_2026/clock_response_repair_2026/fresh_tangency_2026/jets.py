#!/usr/bin/env python3
"""Measure spatial-jet and mixed-derivative defects, without changing a rate."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'nonlinear_evolution_2026'))
from evolve import Evolution, derivatives
from project import radial_profiles, regular_center, project_state
from equations import constraint_rates


def measure(system,state,t):
    r=system.r
    state=project_state(t,state,r,system.model)
    fields=system.fields(t,state)
    rates,_=system.rhs(t,state)
    profiles=radial_profiles(r,*state[[1,4,5,6,7]])
    rateprofiles=radial_profiles(r,*rates[[1,4,5,6,7]])
    center=regular_center(t,state,r,system.model)
    differences={}
    for name,index,order,odd in [('br',0,1,False),('brr',0,2,False),('Qr',1,1,False),
                                  ('Qrr',1,2,False),('ur',2,1,True)]:
        values=state[[1,4,5,6,7][index]]
        differences[name]=profiles[index](r,order)-derivatives(values,system.dr,odd)[order-1]
    # Projection uses its radial ODE, not the derivative of an interpolated A/h.
    # Compare those exact algebraic ODE rates with the jets fed to evolution.
    radial=np.zeros((3,len(r)))
    radial[2,0]=state[2,0]
    for i,x in enumerate(r[1:],1):
        A,b,k,h,Q,u,w,D=state[:8,i]
        bv=profiles[0](x);bp=profiles[0](x,1);bpp=profiles[0](x,2)
        vals=system.model.jets(t,Q*Q-u*u/A**2,u*u/A**2)
        vals.update(A=A,R=x*bv,Rr=bv+x*bp,Rrr=2*bp+x*bpp,h=h,Q=Q,
                    Qr=profiles[1](x,1),cr=u,crr=profiles[2](x,1),w=w,
                    rho=D/(A*b*b*np.sqrt(1+w*w/A**2)))
        radial[:,i]=constraint_rates(vals)
    differences['Ar_ODE_minus_FD']=radial[0]-fields['Ar']
    differences['hr_ODE_minus_FD']=radial[1]-fields['hr']
    differences['k_constraint_minus_sample']=radial[2]-state[2]
    ks=radial_profiles(r,state[2],state[4],state[5],state[6],state[7])[0]
    differences['kr_spline_minus_FD']=ks(r,1)-derivatives(state[2],system.dr)[0]
    N=fields['N'];Nr=fields['Nr'];Q=fields['Q']
    Qr,Qrr=derivatives(Q,system.dr)
    # This is the second radial derivative substituted into the action's
    # preserved-clock row; the center uses the actual regular equation.
    action_mixed=fields['rate'][:,3]*Q+2*Nr*Qr+N*Qrr
    action_mixed[0]=fields['rate'][0,3]*Q[0]+N[0]*center['Q2']
    measured_mixed=rateprofiles[2](r,1)
    raw_rate=Nr*Q+N*Qr
    rawprofiles=radial_profiles(r,rates[1],rates[4],raw_rate,rates[6],rates[7])
    differences['mixed_corrected']=measured_mixed-action_mixed
    differences['mixed_raw']=rawprofiles[2](r,1)-action_mixed
    differences['center_correction_radial_effect']=measured_mixed-rawprofiles[2](r,1)
    results={}
    for name,error in differences.items():
        results[name]={}
        for low in (0.,.1,.3):
            ids=np.flatnonzero((r>=low)&(r<2.8))
            at=ids[np.argmax(abs(error[ids]))]
            results[name][str(low)]={'maximum':float(abs(error[at])),
                                    'signed':float(error[at]),'radius':float(r[at])}
    return dict(points=len(r),jets=results,
                center_mixed_defect=float(differences['mixed_corrected'][0]))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--states',type=Path,nargs='+',required=True)
    parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();rows=[]
    for path in args.states:
        with np.load(path) as saved:
            r=saved['r'];state=saved['state']
        system=Evolution(.02,.3,len(r),3.,.022,1e-6)
        row=measure(system,state,.02);row['input']=str(path)
        rows.append(row);print(json.dumps(row),flush=True)
    args.result_file.write_text(json.dumps(dict(scope='Derivative diagnostics only',cases=rows),indent=2)+'\n')


if __name__=='__main__':main()
