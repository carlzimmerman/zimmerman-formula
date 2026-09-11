#!/usr/bin/env python3
"""Experimental integrable clock-rate reconstruction, NOT enabled by default.

The action supplies S=(NQ)_{rr}. Integrate its even interpolant from the
regular center, then apply the existing center-jet closure to sampled rates.
All differentiated time-rate profiles are built from these actual samples;
there is no independently injected mixed derivative as in attribution.py.
"""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sys.path.insert(0,str(BASE/'nonlinear_evolution_2026'))
sys.path.insert(0,str(BASE/'origin_tangency_2026'))
from evolve import Evolution, derivatives
from project import project_state, match_odd_center_rate, radial_profiles
from tangent_linear import tangent
from integrated_jet import integrate_even_jet


class IntegratedEvolution(Evolution):
    primitive=staticmethod(integrate_even_jet)

    def fields(self,t,state):
        fields=super().fields(t,state)
        self.latest_fields=fields
        return fields

    def rhs(self,t,state):
        out,flux=super().rhs(t,state)
        f=self.latest_fields;Q=f['Q'];N=f['N'];Nr=f['Nr']
        Qr,Qrr=derivatives(Q,self.dr)
        target=f['rate'][:,3]*Q+2*Nr*Qr+N*Qrr
        target[0]=f['rate'][0,3]*Q[0]+N[0]*f['center_Qrr']
        self.raw_clock_rate=out[5].copy()
        out[5]=match_odd_center_rate(self.r,self.primitive(self.r,target),target[0])
        self.mixed_target=target
        return out,flux


def probe(n,state,system_type=IntegratedEvolution):
    system=system_type(.02,.3,n,3.,.022,1e-6);r=system.r
    state=project_state(.02,state,r,system.model)
    rates,_=system.rhs(.02,state)
    measured=radial_profiles(r,*rates[[1,4,5,6,7]])[2](r,1)
    mask=r<2.8
    clock_change=float(max(abs((rates[5]-system.raw_clock_rate)[mask])))
    mixed=float(max(abs((measured-system.mixed_target)[mask])))
    f=system.latest_fields
    kinematic=float(max(abs((rates[5]-f['Nr']*f['Q']-f['N']*f['Qr'])[mask])))
    points=np.r_[0.,(r[1:-1]+r[2:])/2]
    ratefit=CubicSpline(r[1:]**2,rates[5,1:]/r[1:])
    at_points=ratefit(points*points)+2*points*points*ratefit(points*points,1)
    target_points=CubicSpline(r*r,system.mixed_target)(points*points)
    collocation=float(max(abs(at_points-target_points)))
    result=tangent(system,state,.02,1e-5)
    result.update(clock_rate_change=clock_change,mixed_jet_error=mixed,
                  clock_kinematic_defect=kinematic,staggered_collocation_residual=collocation,
                  scope='Integrable sampled rate; not yet validated time evolution')
    return result


def evolve_probe(n,dt,system_type=IntegratedEvolution):
    system=system_type(.02,.3,n,3.,.022,1e-6)
    state=system.initial.copy();steps=int(np.ceil(.02/dt));dt=.02/steps
    flux_integral=0.
    for i in range(steps):
        t=i*dt
        k1,f1=system.rhs(t,state);k2,f2=system.rhs(t+dt/2,state+dt*k1/2)
        k3,f3=system.rhs(t+dt/2,state+dt*k2/2);k4,f4=system.rhs(t+dt,state+dt*k3)
        state+=dt*(k1+2*k2+2*k3+k4)/6
        state=project_state((i+1)*dt,state,system.r,system.model)
        flux_integral+=dt*(f1+2*f2+2*f3+f4)/6
    return state,system.snapshot(.02,state,flux_integral)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    parser.add_argument('--points',type=int,nargs='+',default=[129,257,513])
    parser.add_argument('--evolve',action='store_true');parser.add_argument('--dt',type=float,default=.00025)
    args=parser.parse_args();rows=[]
    for n in args.points:
        if args.evolve:
            state,snapshot=evolve_probe(n,args.dt)
            np.savez_compressed(args.result_file.parent/f'state_{n}.npz',
                                r=np.linspace(0,3,n),state=state)
        else:
            with np.load(BASE/f'fresh_tangency_2026/offset_001/state_{n}.npz') as saved:
                state=saved['state']
            snapshot=None
        row=probe(n,state);row['snapshot']=snapshot;rows.append(row)
        args.result_file.write_text(json.dumps(dict(cases=rows,full_theory_status='OPEN'),indent=2)+'\n')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
