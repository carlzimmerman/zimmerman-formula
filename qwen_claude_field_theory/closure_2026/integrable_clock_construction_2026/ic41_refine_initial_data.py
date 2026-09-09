"""Bounded high-precision Newton refinement of actual IC41 constraint data."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import ic41_free_initial_gradients as free


def newton_step(fn,x,h):
    values=mp.matrix(fn(x));J=mp.matrix(len(values),len(x))
    for j in range(len(x)):
        perturbed=list(x);perturbed[j]+=h
        diff=mp.matrix(fn(perturbed))-values
        for i in range(len(values)):J[i,j]=diff[i]/h
    delta=mp.lu_solve(J,-values)
    sv=mp.svd(J,compute_uv=False)
    return dict(delta=list(delta),matrix=J,determinant=mp.det(J),singular_values=list(sv),
                rank=sum(v>64*mp.eps*sv[0] for v in sv))


def refine(source,dps=60,steps=4):
    records=[]
    for line in Path(source).read_text().splitlines():
        try:row=json.loads(line)
        except json.JSONDecodeError:continue
        if isinstance(row,dict) and row.get('event')=='evaluation':records.append(row)
    if not records:raise ValueError('No complete IC41 evaluation records')
    best=min(records,key=lambda row:row['norm'])
    with mp.workdps(dps):
        x=[mp.mpf(str(v)) for v in best['coordinates']];cache={};count=0;history=[]
        fmt=lambda v:mp.nstr(v,dps-10)
        def fn(x):
            nonlocal count
            key=tuple(v._mpf_ for v in x)
            if key in cache:return cache[key][0]
            if not (-2<x[0]<2 and -100<x[1]<100 and -mp.log(4)<x[2]<mp.log(4) and -10<x[3]<10):
                raise ValueError('Refinement left the declared search box')
            out=free.field_result(U0=fmt(x[0]),U1=fmt(x[1]),qprime=fmt(-100*mp.exp(x[2])),
                                  Sprime=fmt(x[3]),dps=dps,order=3)
            values=[a/mp.mpf(b) for a,b in zip(free.condition_vector(out),['1e7','1e10','1e9','1e12'])]
            count+=1;cache[key]=(values,out)
            print(json.dumps(dict(event='evaluation',evaluation=count,coordinates=[fmt(v) for v in x],
                scaled_conditions=[fmt(v) for v in values],result=out)),flush=True)
            return values
        for i in range(steps):
            before=mp.norm(fn(x));update=newton_step(fn,x,mp.mpf('1e-12'))
            accepted=False
            for k in range(6):
                candidate=[a+b/(2**k) for a,b in zip(x,update['delta'])]
                after=mp.norm(fn(candidate))
                if after<before:x=candidate;accepted=True;break
            record=dict(iteration=i,norm_before=fmt(before),norm_after=fmt(after),accepted=accepted,
                determinant=fmt(update['determinant']),rank=update['rank'],
                matrix=[[fmt(update['matrix'][i,j]) for j in range(4)] for i in range(4)],
                singular_values=[fmt(v) for v in update['singular_values']])
            history.append(record);print(json.dumps(dict(event='iteration',**record)),flush=True)
            if not accepted:break
        final=cache[tuple(v._mpf_ for v in x)]
        return dict(event='summary',dps=dps,evaluations=count,coordinates=[fmt(v) for v in x],
            scaled_norm=fmt(mp.norm(final[0])),result=final[1],iterations=history,
            full_theory='OPEN',non_claim='Numerical necessary-condition root only; not an exact existence certificate')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',required=True)
    p.add_argument('--dps',type=int,default=60);p.add_argument('--steps',type=int,default=4)
    p.add_argument('--strict',action='store_true');a=p.parse_args()
    print(json.dumps(refine(a.input,a.dps,a.steps),indent=2));raise SystemExit(2 if a.strict else 0)
