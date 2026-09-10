#!/usr/bin/env python3
"""Independent seven-equation refinement, health, and one HIGHER gate.

Input is a search row containing parameters=[dw1,y2,u2,y1], u1, f, j.
The default is the discovered joint point, used as a reproducible control.
Solves five actual action-jet differences and two derivative differences using
independent arbitrary-precision directional differentiation. No theory PASS.
"""
import argparse
from dataclasses import replace
import json
from pathlib import Path
import sys
import mpmath as mp
import parametric as p

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'kgb_universal_clock_2026/health_search'))
import matched_seed_audit as audit

SEED=dict(parameters=[306704.1420152562,.1800733844324149,3057.7826875767923,.1],
          u1=4754.976244138632,f=3.29992587867242,j=38.55121957650046)


def refine(candidate=SEED,dps=60):
    with mp.workdps(dps):
        dw,y2,u2,y1=map(lambda v:mp.mpf(str(v)),candidate['parameters'])
        u1,f,j=map(lambda k:mp.mpf(str(candidate[k])),('u1','f','j'))
        spec=replace(p.Spec(),y1=str(y1))
        a,b=p.pair(tuple(mp.log(v) for v in (dw,y2,u2)),u1,spec)
        start=(f,a['w'],y2,u1,u2,b['w'],j)
        def states(v):
            ff,ww1,yy2,uu1,uu2,ww2,jj=v
            return [audit.normalized(mp.mpf('1e-6'),y1,mp.mpf('.5'),mp.mpf('1e-6')*uu1,ww1,mp.mpf('.525')),
                    audit.normalized(mp.mpf('2e-6'),yy2,mp.mpf('.5'),mp.mpf('2e-6')*uu2,ww2,mp.mpf('.525'))]
        def values(v):
            ff,_,_,_,_,_,jj=v;first,second=states(v)
            return (audit.jets(first,ff,jj),audit.jets(second,ff,jj),
                    audit.next_derivatives(first,ff,jj),audit.next_derivatives(second,ff,jj))
        va,vb,na,nb=values(start)
        scales=[max(abs(va[i]),abs(vb[i]),1) for i in range(5)]+[max(abs(na[i]),abs(nb[i]),1) for i in range(2)]
        def equations(*v):
            va,vb,na,nb=values(v)
            return tuple(q/scales[i] for i,q in enumerate(list(va-vb)+list(na-nb)))
        solution=mp.findroot(equations,start,tol=mp.mpf(10)**(-dps+15),maxsteps=20)
        f,w1,y2,u1,u2,w2,j=solution;rows=states(solution)
        p.h.check_map(f,rows[0]['F'],rows[0]['X'])
        for a in rows:
            if (not all(mp.isfinite(v) for v in a.values()) or not a['w'] or
                    min(a[k] for k in ('eps','y','X','U','F','B','r','p','Dcoord'))<=0):
                raise ValueError('refined state left regular physical chart')
        initial_res=list(equations(*solution))
        va,vb,na,nb=values(solution)
        actual_relative=[abs(x-y)/max(abs(x),abs(y),1) for x,y in zip(va,vb)]
        actual_relative += [abs(x-y)/max(abs(x),abs(y),1) for x,y in zip(na,nb)]
        health=[audit.evaluate(a,f,j) for a in rows]
        # Differentiate the next gate along the actual state and f_X=j flow,
        # holding j fixed. F_XXX=k then contributes k*B, not separate k_i.
        Ms=[];Bs=[]
        for row in rows:
            point=[row[k] for k in ('y','X','U','w','F')]+[f]
            flow=audit.flow(row,f,j)
            def next_at(t,i):
                moved=[x+t*v for x,v in zip(point,flow)]
                state=audit.normalized(row['eps'],*moved[:5])
                return audit.next_derivatives(state,moved[5],j)[i]
            Ms.append(mp.matrix([mp.diff(lambda t:next_at(t,i),0) for i in range(2)]))
            Bs.append(p.h.parts(p.h.normalized(*[row[k] for k in ('eps','y','X','U','w','F')]))[1])
        M,B=Ms[0]-Ms[1],Bs[0]-Bs[1]
        k,err=p.h.next_control(M,B)
        higher=[err[i]/(1+abs(M[i])+(abs(k*B[i]) if k is not None else 0)) for i in range(2)]
        fmt=lambda v:mp.nstr(v,dps-5)
        return dict(dps=dps,parameters=list(map(fmt,(abs(w1)/(mp.mpf('.05')*rows[0]['g']),y2,u2,y1))),
                    u1=fmt(u1),f=fmt(f),j=fmt(j),seven_residuals=list(map(fmt,initial_res)),
                    actual_relative_residuals=list(map(fmt,actual_relative)),
                    accepted_joint_point=max(map(abs,initial_res+actual_relative))<mp.mpf('1e-30'),
                    health=[{key:(bool(a[key]) if key=='strict_EF' else fmt(a[key])) for key in
                             ('kinetic','radial','angular','cross','strict_EF','Einstein_relative_error','current_relative_error','Dfield','Dcoord')}
                            for a in health],
                    higher_M=list(map(fmt,M)),higher_B=list(map(fmt,B)),required_FXXX=fmt(k) if k is not None else None,
                    higher_control_sector='nonzero_B' if mp.norm(B) else 'zero_B',higher_relative=list(map(fmt,higher)),
                    passed_higher_gate=k is not None and max(map(abs,higher))<mp.mpf('1e-30'),
                    scope='Necessary local joint compatibility and frozen EF health; not nonlinear closure, calibrated sources, or CMB')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--candidate-json',type=Path)
    parser.add_argument('--dps',type=int,nargs='+',default=[60,80]);args=parser.parse_args()
    candidate=json.loads(args.candidate_json.read_text()) if args.candidate_json else SEED
    for dps in args.dps:
        print('REFINED='+json.dumps(refine(candidate,dps),allow_nan=False),flush=True)
