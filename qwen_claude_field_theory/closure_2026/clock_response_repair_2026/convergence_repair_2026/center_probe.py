#!/usr/bin/env python3
"""Compare center jets used by radial projection and lapse preservation."""
import json
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'nonlinear_evolution_2026'))
from evolve import derivatives,evolve
from project import radial_profiles


def run(n):
    out=evolve(.02,.3,points=n,tend=.005,dt=.00025,outer=3.)
    state=out['state'];A,b,k,h,Q,u,w,D,_=state;r=out['r'];ac=b[0]
    bs,qs,us,ws,ds=radial_profiles(r,b,Q,u,w,D)
    q=Q[0];u1=float(us(0,1));j=out['model'].jets(.005,q*q,0.)
    h0=(j['P_t']-j['V_t']+6*q*j['W_Y']*u1/ac**2)/(3*j['W'])
    rhoc=2*q*q*j['P_X']-j['P']+j['V']-6*out['model'].gamma*q**3*h0+6*out['model'].gamma*q*q*u1/ac**2
    exactA2=3*float(bs(0,2))+ac**3*(rhoc+D[0]/ac**3+.7-3*h0*h0)/3
    return dict(points=n,fd_A2=float(derivatives(A,r[1])[1][0]),projection_A2=exactA2,
                fd_b2=float(derivatives(b,r[1])[1][0]),projection_b2=float(bs(0,2)),
                fd_Q2=float(derivatives(Q,r[1])[1][0]),projection_Q2=float(qs(0,2)),
                fd_u1=float(derivatives(u,r[1],True)[0][0]),projection_u1=u1)


if __name__=='__main__':
    for n in (129,257):print(json.dumps(run(n)),flush=True)
