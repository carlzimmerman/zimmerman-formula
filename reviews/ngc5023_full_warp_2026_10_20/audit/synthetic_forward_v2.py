#!/usr/bin/env python3
"""Independent finite source/response controls; does not import production renderer."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.special import ndtr
from scipy.signal import fftconvolve
from numpy.polynomial.laguerre import laggauss


def triad(pa, inc):
    a,i=np.deg2rad(pa),np.deg2rad(inc)
    m=np.stack([np.sin(a),np.cos(a),np.zeros_like(a)],axis=-1)
    q=np.stack([np.cos(a)*np.cos(i),-np.sin(a)*np.cos(i),np.sin(i)],axis=-1)
    n=np.stack([np.cos(a)*np.sin(i),-np.sin(a)*np.sin(i),-np.cos(i)],axis=-1)
    return m,q,n


def clouds(nphi=192,nz=16,asymmetric=False,arm=False):
    r=np.array([8.,16.,24.,32.])
    rw=np.array([.1,.25,.35,.3])
    phi=(np.arange(nphi)+.5)*2*np.pi/nphi
    zz,zw=laggauss(nz)
    zz=np.r_[-zz[::-1],zz]*1.5
    zw=np.r_[zw[::-1],zw]*.5
    R,P,Z=np.meshgrid(r,phi,zz,indexing='ij')
    W=np.broadcast_to(rw[:,None,None]*zw[None,None,:]/nphi,R.shape).copy()
    pa=28+3*(R/32)**2
    inc=89-5*(R/32)**2
    if asymmetric:pa+=np.where(np.cos(P)>0,1.,-1.)*(R/32)**2
    if arm:
        phase=.6+1.1*np.log(R/8)
        d=np.arctan2(np.sin(P-phase),np.cos(P-phase))
        d2=np.arctan2(np.sin(P-phase-np.pi),np.cos(P-phase-np.pi))
        overdensity=np.exp(-.5*(d/.35)**2)+.55*np.exp(-.5*(d2/.35)**2)
        W*=1+overdensity
        W/=W.sum()
    m,q,n=triad(pa,inc)
    xyz=R[...,None]*np.cos(P)[...,None]*m+R[...,None]*np.sin(P)[...,None]*q+Z[...,None]*n
    vel=(70-0.2*abs(Z))*np.sin(np.deg2rad(inc))*np.cos(P)
    return xyz.reshape(-1,3),vel.ravel(),W.ravel()


def beam_kernel():
    # Rotated elliptical beam, sigma major4/minor2 pixels.
    a=np.deg2rad(37.)
    u=np.array([np.sin(a),np.cos(a)]);v=np.array([np.cos(a),-np.sin(a)])
    cov=16*np.outer(u,u)+4*np.outer(v,v)
    y,x=np.mgrid[-24:25,-24:25];p=np.stack([x,y],axis=-1)
    b=np.exp(-.5*np.einsum('...i,ij,...j->...',p,np.linalg.inv(cov),p))
    return b/b.sum(),cov


def render(xyz,vel,w):
    # Array axes channel,north,east. Values are integrated flux per channel/pixel.
    x,y=xyz[:,0]+80,xyz[:,1]+80
    lo_x,lo_y=np.floor(x).astype(int),np.floor(y).astype(int)
    fx,fy=x-lo_x,y-lo_y
    edges=np.linspace(-140,140,71)
    widths=np.diff(edges)
    spectrum=ndtr((edges[1:,None]-vel)/10)-ndtr((edges[:-1,None]-vel)/10)
    a=np.zeros((70,161,161))
    for dx,dy,pw in [(0,0,(1-fx)*(1-fy)),(1,0,fx*(1-fy)),(0,1,(1-fx)*fy),(1,1,fx*fy)]:
        xx,yy=lo_x+dx,lo_y+dy
        ok=(xx>=0)&(xx<161)&(yy>=0)&(yy<161)
        for k in range(len(a)):
            np.add.at(a[k],(yy[ok],xx[ok]),w[ok]*pw[ok]*spectrum[k,ok])
    kernel,cov=beam_kernel()
    for k in range(len(a)):a[k]=fftconvolve(a[k],kernel,mode='same')
    return a,edges,widths


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True)
    checks=[]
    def check(name,value,bound,condition=None):
        passed=(value<=bound) if condition is None else bool(condition)
        checks.append({'name':name,'value':float(value),'bound':float(bound),'passed':bool(passed)})
    m,q,n=triad(np.array([0,28,37,120,220]),np.array([0,45,89,90,115]))
    matrices=np.stack([m,q,n],axis=-1)
    check('orthonormal ring basis',np.max(abs(np.einsum('...ji,...jk->...ik',matrices,matrices)-np.eye(3))),1e-14)
    check('right handed basis',np.max(abs(np.cross(m,q)-n)),1e-14)
    xyz,v,w=clouds()
    check('vertical/radial/azimuth flux normalization',abs(w.sum()-1),1e-14)
    check('cloud central moment zero',np.max(abs((xyz*w[:,None]).sum(0))),1e-12)
    cube,edges,width=render(xyz,v,w)
    check('projected beam/channel integrated flux',abs(cube.sum()-1),1e-10)
    check('symmetric warped lagged cube point parity',np.max(abs(cube-cube[::-1,::-1,::-1])),1e-14)
    # Correct Jy/arcsec2 and Jy/beam conventions preserve aperture flux.
    beam_area=np.pi/(4*np.log(2))*(4*2.354820045)*(2*2.354820045)
    jy_beam=(cube/width[:,None,None])*beam_area
    check('Jy per beam integrated flux conversion',abs((jy_beam*width[:,None,None]).sum()/beam_area-1),1e-10)
    # Verify numerical channel integration against high-order direct quadrature.
    xg,wg=np.polynomial.legendre.leggauss(64)
    left,right=-12.,16.;mu=3.7;sig=10.
    integ=(right-left)/2*np.sum(wg*np.exp(-.5*(((right-left)/2*xg+(right+left)/2-mu)/sig)**2)/(np.sqrt(2*np.pi)*sig))
    exact=ndtr((right-mu)/sig)-ndtr((left-mu)/sig)
    check('Gaussian CDF channel integral',abs(integ-exact),1e-14)
    # No cos(i) factor: changing inclination changes morphology but not weights/flux.
    x2,v2,w2=clouds(asymmetric=True)
    c2,_,_=render(x2,v2,w2)
    check('side dependent geometry preserves source flux',abs(c2.sum()-1),1e-10)
    asym=float(np.sum(abs(c2-c2[::-1,::-1,::-1]))/2)
    check('side dependent warp breaks parity',asym,1e-5,asym>1e-5)
    x3,v3,w3=clouds(arm=True)
    c3,_,_=render(x3,v3,w3)
    arm_asym=float(np.sum(abs(c3-c3[::-1,::-1,::-1]))/2)
    check('unequal arms break parity',arm_asym,1e-3,arm_asym>1e-3)
    check('component flux survives arm width/shape normalization',abs(c3.sum()-1),1e-10)
    # A small controlled quadrature sequence, not a universal convergence theorem.
    low,_,_=render(*clouds(96,8,arm=True))
    high,_,_=render(*clouds(384,32,arm=True))
    e1=np.sum(abs(low-c3));e2=np.sum(abs(c3-high))
    check('quadrature second refinement contracts',e2,e1,e2<e1)
    check('quadrature tested relative L1 error',e2,.025)
    result={'all_passed':all(c['passed'] for c in checks),'checks':checks,
       'actual_cube_analyzed':False,'production_renderer_imported':False,
       'fixture':'Four flux-normalized rings; radial warp, exponentialverticalquadrature, velocitylag, rotatedellipticalbeam, exactGaussianchannelintegration.',
       'non_claims':['Not the published preferredmodel','No claim of convergence for every actualdigitizedmodel','No actualresidual or uncertaintyinference']}
    (out/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 0 if result['all_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
