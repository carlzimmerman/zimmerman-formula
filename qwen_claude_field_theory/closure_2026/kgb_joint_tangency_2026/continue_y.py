#!/usr/bin/env python3
"""Deterministic high-precision continuation in physical target acceleration.

Locate a joint-gate bracket; failures are not branch exclusions. a0 is never
changed between targets. Stdout is the scientific result, including failures.
"""
import argparse
from dataclasses import replace
import json
import mpmath as mp
import parametric as p


def run(ys, u1='.03', dps=40):
    with mp.workdps(dps):
        u = mp.mpf(u1)
        theta = tuple(mp.log(mp.mpf(x)) for x in
                      ('4164.89540032022', '.1537936934617971', '.02600582459994482'))
        # Establish the requested u1 at y1=.1 before varying y1.
        if u1 != '.03':
            steps = max(2, int(abs(mp.log(u/mp.mpf('.03')))*3)+1)
            for k in range(1, steps+1):
                uk = mp.mpf('.03') * (u/mp.mpf('.03'))**(mp.mpf(k)/steps)
                theta = tuple(mp.findroot(lambda *v:p.residual(v,uk), theta,
                              tol=mp.mpf(10)**(-dps+10), maxsteps=40))
        successful = {mp.mpf('.1'):theta}
        for yy in ys:
            spec = replace(p.Spec(), y1=yy)
            nearest = min(successful, key=lambda t:abs(mp.log(t/mp.mpf(yy))))
            try:
                theta = tuple(mp.findroot(lambda *v:p.residual(v,u,spec), successful[nearest],
                              tol=mp.mpf(10)**(-dps+10), maxsteps=40))
                row = p.gate(theta,u,spec)
                successful[mp.mpf(yy)] = theta
                fmt = lambda v:mp.nstr(v,dps-5)
                result = dict(y1=yy,u1=u1,dps=dps,parameters=[fmt(mp.exp(v)) for v in theta],
                              f=fmt(row['f']),j=fmt(row['j']),
                              next_obstruction=fmt(row['next_obstruction']),
                              next_relative=list(map(fmt,row['next_relative'])),
                              joint_accepted=row['joint_accepted'],
                              initial_residual=list(map(fmt,p.residual(theta,u,spec))))
            except (ValueError, ZeroDivisionError, TypeError) as exc:
                result = dict(y1=yy,u1=u1,dps=dps,error=str(exc))
            print(json.dumps(result),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--u1',default='.03')
    parser.add_argument('--dps',type=int,default=40)
    parser.add_argument('--ys',nargs='+',default=['.1','.08','.05','.03','.01','.003','.001','.15','.2','.3','.5','1','2','3'])
    args=parser.parse_args()
    run(args.ys,args.u1,args.dps)
