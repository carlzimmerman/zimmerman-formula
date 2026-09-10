#!/usr/bin/env python3
"""Eliminate the complete real F_XX axis in the regular local EF diagnostic.

This applies ONLY to inverse-derived P/G jets at fixed background and F,F_X.
The exact conditional algebra is certified separately in variation/ConeWindow.
No local acceleration-scale fit or independent choice of principal coefficients.
"""
import json
import numpy as np
import nonaffine_inverse as n


def light_minimum(k,r,t,b):
    points=[0.,1.]
    if r>t and 0<abs(b)/(r-t)<1:points.append(abs(b)/(r-t))
    return min(k+t-2*abs(b)*x+(r-t)*x*x for x in points)


def construct(I,r,b,beta):
    if beta<=0:raise ValueError('timelike regular beta>0 required')
    gap=I+r-2*abs(b)
    if r>=0 or gap<=0:return None
    delta=min(gap/2,-r/(2*beta))
    return I-delta,-beta*delta


def select_control(k,b,r,t,beta,slope):
    I=k-t/beta;gap=I+r-2*abs(b)
    result=dict(invariant=I,gap=gap,beta=beta,slope=slope)
    if slope==0:
        healthy=k>abs(b) and r<0 and t<0 and light_minimum(k,r,t,b)>0
        result.update(status='fixed_healthy' if healthy else 'fixed_unhealthy',j=0.)
        return result
    target=construct(I,r,b,beta)
    if target is None:
        result.update(status='excluded_all_curvatures',j=None)
        return result
    result.update(status='constructed',j=(target[0]-k)/slope,target_kinetic=target[0],target_angular=target[1])
    return result


def inspect_window(eps,y,X,U,z,F=.525,f=.05,verify_correlation=True):
    kwargs=dict(F0=F,f0=f,X0=X)
    a=n.inspect(eps,y,X,U,z,j0=0.,**kwargs)
    step=abs(f)/eps
    fields=('kinetic','cross','radial','angular')
    v=np.array([a[k] for k in fields]);beta=U/(2*X)
    C,C1,D=2*F,2*f,2*(F-X*f);p=np.sqrt(n.old.metric(eps,y)['B']*U)
    # On-shell variation: alpha*(rho_E+Ptilde), NOT angular stress.
    slope=4*C*X*a['GX']*z/(C1*D*D*p)
    correlation=None
    if verify_correlation:
        plus=n.inspect(eps,y,X,U,z,j0=step,**kwargs)
        minus=n.inspect(eps,y,X,U,z,j0=-step,**kwargs)
        vp=np.array([plus[k] for k in fields]);vm=np.array([minus[k] for k in fields])
        predicted=step*slope*np.array([1.,0.,0.,beta])
        scale=np.maximum(np.maximum(abs(v),abs(predicted)),1.)
        correlation=float(max(np.max(abs(vp-v-predicted)/scale),np.max(abs(vm-v+predicted)/scale)))
        if correlation>2e-7:raise ArithmeticError('derived curvature correlation failed')
    result=select_control(*v,beta,slope)
    result.update(y=y,X=X,U=U,z=z,F=F,f=f,base=a,correlation_residual=correlation)
    if result['status']=='constructed':
        result['selected']=n.inspect(eps,y,X,U,z,j0=result['j'],**kwargs)
        if not result['selected']['strict_EF']:
            raise ArithmeticError('constructive window failed direct principal test')
    result['scope']='Entire real F_XX axis at fixed regular local state, conditional EF vacuum principal diagnostic; not CMB or global closure'
    return result


def main():
    rows=[];eps=1e-6
    for y in (.001,.01,.1,1.,2.,10.,100.):
        for b in (.05,.25,.75,1.25,4.):
            for d in (1.1,1.5,2.5):
                X,U,_=n.old.initial(eps,y,.1,b,d)
                z=-d*n.old.metric(eps,y)['g']
                row=inspect_window(eps,y,X,U,z)
                row.update(bscale=b,dscale=d);rows.append(row)
    counts={status:sum(r['status']==status for r in rows) for status in sorted(set(r['status'] for r in rows))}
    print('CURVATURE_WINDOW='+json.dumps(dict(rows=rows,counts=counts,attempts=len(rows)),allow_nan=False))
    return 0


if __name__=='__main__':raise SystemExit(main())
