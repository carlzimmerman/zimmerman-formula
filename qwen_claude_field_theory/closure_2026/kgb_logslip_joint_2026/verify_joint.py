#!/usr/bin/env python3
"""Independent original-inverse refinement; a local health failure stops promotion."""
import json
import mpmath as mp
import joint
from reference import logslip_reference as ref


def run(dps=65):
    start=joint.solve([306704.14201367765,.18007338443212362,3057.78268757124,4754.976244115166])
    if not start['accepted_numerical_joint']:raise ArithmeticError('double starting point not matched')
    with mp.workdps(dps):
        to=lambda v:mp.mpf(str(v));f,j=to(start['f']),to(start['j'])
        a,b=start['states'];y1=to(start['y1']);X,F=mp.mpf('.5'),mp.mpf('.525')
        v0=tuple(map(to,(f,a['w'],b['y'],a['U'],b['U'],b['w'],j)))
        def states(v):
            ff,w1,y2,U1,U2,w2,jj=v
            return ref.normalized(mp.mpf('1e-6'),y1,X,U1,w1,F),ref.normalized(mp.mpf('2e-6'),y2,X,U2,w2,F)
        def values(v):
            a,b=states(v);ff,jj=v[0],v[6]
            return ref.jets(a,ff,jj),ref.jets(b,ff,jj),ref.next_derivatives(a,ff,jj),ref.next_derivatives(b,ff,jj)
        va,vb,na,nb=values(v0)
        scale=[max(abs(x),abs(y),1) for x,y in zip(list(va)+list(na),list(vb)+list(nb))]
        def equations(*v):
            va,vb,na,nb=values(v)
            return tuple(q/scale[i] for i,q in enumerate(list(va-vb)+list(na-nb)))
        solution=tuple(mp.findroot(equations,v0,tol=mp.mpf(10)**(-dps+15),maxsteps=20))
        rows=states(solution);f,j=solution[0],solution[6]
        for a in rows:
            if min(a[k] for k in ('y','X','U','B','F','Dcoord'))<=0 or not a['w'] or not f or F-X*f==0:
                raise ValueError('refined state outside regular chart')
        health=[ref.evaluate(a,f,j) for a in rows]
        va,vb,na,nb=values(solution)
        relative=[abs(x-y)/max(abs(x),abs(y),1) for x,y in zip(list(va)+list(na),list(vb)+list(nb))]
        thirds=[ref.third_jets(a,f,j,mp.mpf('17')) for a in rows]
        third_relative=[abs(x-y)/max(abs(x),abs(y),1) for x,y in zip(*thirds)]
        return ref.serial(dict(dps=dps,solution=solution,states=[{k:a[k] for k in ('eps','y','X','U','w','F')} for a in rows],
            actual_seven_relative=relative,physical_third_jet_relative=third_relative,
            accepted_joint_point=max(relative+third_relative)<mp.mpf('1e-35'),
            health=health,angular_speed_squared=[-h['angular']/h['kinetic'] for h in health],
            promotion=max(relative+third_relative)<mp.mpf('1e-35') and all(h['strict_EF_scalar_cone'] for h in health),
            scope='One independently refined point. Healthy promotion still requires higher preservation, source and cosmological closure.'))


if __name__=='__main__':print(json.dumps(run(),allow_nan=False))
