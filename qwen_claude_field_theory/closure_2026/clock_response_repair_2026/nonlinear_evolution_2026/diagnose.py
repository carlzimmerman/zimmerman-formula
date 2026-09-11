#!/usr/bin/env python3
"""Locate errors and test the time consistency of radial constraint projection.

Projection residuals alone do not verify the metric evolution equations.
The directional derivative below independently measures whether projection
changes the prescribed metric time derivatives. All quantities are code units.
"""
import argparse
import json
import numpy as np
from evolve import Evolution, evolve
from project import project_state


def diagnose(points, tend):
    if tend:
        run=evolve(.02,.3,points=points,tend=tend,dt=.00025,outer=3.)
        state=run['state']
    system=Evolution(.02,.3,points,3.,tend+.001,1e-6)
    if not tend:state=system.initial
    state=project_state(tend,state,system.r,system.model)
    f=system.fields(tend,state);rhs,_=system.rhs(tend,state)
    errors={}
    for i,name in enumerate(('hamiltonian','momentum','clock')):
        for cut in (2*system.dr,.1,.3):
            mask=(system.r>cut)&(system.r<2.8)
            ids=np.flatnonzero(mask);ix=ids[np.argmax(abs(f['constraints'][mask,i]))]
            errors[name+'_cut_'+str(cut)]={'max':float(abs(f['constraints'][ix,i])),
                                         'radius':float(system.r[ix])}
    tangency=[]
    for step in (1e-5,5e-6):
        projected=project_state(tend+step,state+step*rhs,system.r,system.model)
        mismatch=(projected-state)/step-rhs
        tangency.append({'step':step,'A':float(max(abs(mismatch[0,:-3]))),
                         'h':float(max(abs(mismatch[3,:-3]))),
                         'k':float(max(abs(mismatch[2,:-3])))})
    return {'points':points,'time':tend,'constraints':errors,'projection_tangency':tangency}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--time',type=float,default=.005)
    parser.add_argument('--points',type=int,nargs='+',default=[65,129,257]);args=parser.parse_args()
    for n in args.points:print(json.dumps(diagnose(n,args.time)),flush=True)
