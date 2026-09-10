#!/usr/bin/env python3
"""Attack extension to a third mass without refitting the shared action.

H matching determines U3. H_X matching selects y3. H_XX matching then tests
whether the same P_XX can preserve that equality. Finite root search only.
"""
import json
import numpy as np
from scipy.optimize import brentq
import joint_static as j


def match(eps,y,X,P,H):
    v=j.coefficients(eps,y,X,eps,P)
    V=X*v['r']*v['g']; a=np.sqrt(v['B'])*v['r']
    d=np.sqrt(a*a+16*H*H*V)
    sqrtU=(a+d)/(4*H) if H>0 else 4*abs(H)*V/(a+d)
    return j.coefficients(eps,y,X,sqrtU*sqrtU,P)


def derivatives(v,px):
    """d(a,b)/dX along this halo with common P_X, excluding the P_XX*b term."""
    eps=v['eps']; X=v['X']
    values=np.array([X,np.log(v['y']),v['U']/eps,v['P']])
    tangent=np.array([1,px/(v['y']*v['ry']*v['W']),
                      (-2-2*v['g']*(2*X+v['U'])*px/v['W'])/eps,px])
    out=np.zeros(2); h=1e-25
    for i in range(4):
        z=values.astype(complex);z[i]+=1j*h
        a=j.coefficients(eps,np.exp(z[1]),z[0],eps*z[2],z[3])
        out+=np.imag([a['a'],a['b']])/h*tangent[i]
    return out


def extension(eps3, grid_points=401):
    eps=(1e-6,2e-6); X=.5; state=j.initial(*eps,.1,.3,.25)
    px,pxx=j.action_jet(X,state,eps)
    _,v1,v2=j.shared(X,state,eps)
    F1=v1['a']+px*v1['b']
    def residual(logy):
        v=match(eps3,np.exp(logy),X,0,v1['H'])
        return (v['a']+px*v['b']-F1)/max(abs(F1),1.)
    grid=np.linspace(np.log(.02),np.log(20.),grid_points)
    values=[residual(t) for t in grid]
    roots=[float(t) for t,value in zip(grid,values) if value==0]
    for i in range(len(grid)-1):
        if values[i]*values[i+1]<0:
            root=brentq(residual,grid[i],grid[i+1],xtol=1e-14)
            if abs(residual(root))<1e-7 and all(abs(root-r)>1e-8 for r in roots):roots.append(root)
    results=[];d1=derivatives(v1,px)
    for root in roots:
        v=match(eps3,np.exp(root),X,0,v1['H']); d3=derivatives(v,px)
        delta_b=v['b']-v1['b']
        second=(d3[0]-d1[0])+px*(d3[1]-d1[1])+pxx*delta_b
        scale=max(abs(d3[0]+px*d3[1]+pxx*v['b']),abs(d1[0]+px*d1[1]+pxx*v1['b']),1.)
        F3=v['a']+px*v['b']
        hxx1=v1['H']*(F1*F1+d1[0]+px*d1[1]+pxx*v1['b'])
        hxx3=v['H']*(F3*F3+d3[0]+px*d3[1]+pxx*v['b'])
        required=None if delta_b==0 else -((d3[0]-d1[0])+px*(d3[1]-d1[1]))/delta_b
        physical=j.local(v,px,pxx)
        results.append(dict(y=float(v['y']),U=float(v['U']),H_relative_error=float(abs(v['H']/v1['H']-1)),
                            first_derivative_relative_error=float(abs(residual(root))),
                            normalized_log_derivative_preservation_residual=float(abs(second)/scale),
                            HXX_relative_mismatch=float(abs(hxx3-hxx1)/max(abs(hxx1),abs(hxx3),1e-200)),
                            required_PXX=None if required is None else float(required),
                            physical=physical))
    return dict(epsilon3=eps3,grid_points=grid_points,y_range=[.02,20.],common_PX=float(px),common_PXX=float(pxx),
                sign_change_roots=results,
                scope='No guarantee of all roots; tangencies/even roots, other seeds and other metric completions not excluded.')


def main():
    for eps in (1e-6,1.5e-6,2e-6,3e-6,4e-6):
        for count in (401,801):print('THIRD_MASS='+json.dumps(extension(eps,count)),flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
