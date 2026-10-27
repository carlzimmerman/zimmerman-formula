#!/usr/bin/env python3
"""Independent mask, positive bounded calibration, metric and source-flux checks."""
import argparse
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import erf

HERE=Path(__file__).resolve().parent
PACKET=HERE.parent


def bounded_lsq(A,y,lo,hi):
    """Enumerate all lower/free/upper active sets; no scipy optimization import."""
    best=None
    for state in itertools.product([-1,0,1],repeat=A.shape[1]):
        state=np.array(state);fixed=state!=0;free=~fixed
        x=np.zeros(len(state));x[state==-1]=lo[state==-1];x[state==1]=hi[state==1]
        rhs=y-A[:,fixed]@x[fixed]
        if free.any():x[free]=np.linalg.lstsq(A[:,free],rhs,rcond=None)[0]
        if np.any(x<lo-1e-9) or np.any(x>hi+1e-9):continue
        obj=float(np.sum((A@x-y)**2))
        if best is None or obj<best[0]:best=obj,x.copy()
    assert best is not None
    return best


def integral_disk(radius,values,support):
    radius=np.array(radius);values=np.array(values)
    nodes=np.unique(np.r_[0.,radius[(radius>0)&(radius<support)],support])
    total=0.
    for a,b in zip(nodes[:-1],nodes[1:]):
        ya,yb=np.interp([a,b],radius,values)
        slope=(yb-ya)/(b-a)
        total+=ya*(b*b-a*a)/2+slope*((b**3-a**3)/3-a*(b*b-a*a)/2)
    return total


def continuous_component_flux(p):
    flux=[np.pi*(integral_disk(p['radius'],p['sbr_sw'],p['support_arcsec'])+
                 integral_disk(p['radius'],p['sbr_ne'],p['support_arcsec']))]
    for j in [1,2]:
        arm=p['arm'+str(j)]
        def f(r):
            width=max(float(np.interp(r,p['radius'],arm['width'])),1e-6)
            amp=float(np.interp(r,p['radius'],arm['sbr']))
            # Exactly integrate the nearest-wrapped Gaussian around a full ring.
            half=min(np.pi,np.deg2rad(p.get('arm_wedge_deg',360)/2))
            return amp*np.sqrt(2*np.pi)*width*erf(half*r/(np.sqrt(2)*width))
        val,err=quad(f,0,p['support_arcsec'],points=p['radius'],epsabs=1e-8,epsrel=1e-9,limit=200)
        flux.append(val)
    return np.array(flux)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True)
    results=json.loads((PACKET/'nominal_run001/results.json').read_text())
    a=np.load(PACKET/'nominal_run001/arrays.npz')
    U,Z,X=np.meshgrid(a['U'],a['Z'],a['X'],indexing='ij')
    safe=np.ones(X.shape,bool)
    for x,z,u,w in [(-72,80,-24.8,56),(112,92,39.2,40),(120,-76,39.2,52)]:
        for s in [-1,1]:safe &= ~((abs(X-s*x)<=70)&(abs(Z-s*z)<=70)&(abs(U-s*u)<=w/2+6.18+8.24))
    masks={'training':(abs(Z)<=10)&(abs(X)<=230)&(abs(U)<=105)&safe,
           'validation':(abs(Z)>=50)&(abs(X)<=230)&(abs(U)<=105)&safe,
           'guarded_validation':(abs(Z)>=70)&(abs(X)<=230)&(abs(U)<=105)&safe}
    checks=[]
    def ck(name,value,tol):
        checks.append({'name':name,'error':float(value),'tolerance':float(tol),'passed':bool(value<=tol)})
    for name,m in masks.items():
        key='training_mask' if name=='training' else name+'_mask'
        ck('reconstructed '+name+' mask',np.count_nonzero(m!=a[key]),0)
    ck('paired safe support',np.count_nonzero(safe!=safe[::-1,::-1,::-1]),0)
    data=a['data_binned'].astype(float);blanks=a['blanks_binned'].astype(float)
    sd=blanks.std(0,ddof=1);train=masks['training'];floor=np.median(sd[train])*.5
    detail={}
    for model,record in results['models'].items():
        components=a[model+'_components_binned'].astype(float)
        p=record['parameters'];meta=record['render_metadata']
        intrinsic=np.array([v['intrinsic_integrated_flux_Jy_km_s'] for v in meta['components']])
        live=intrinsic>1e-10
        expected=np.array([4.8e8,4.9e7,4.3e7])/(2.356e5*6.6**2)
        frac=np.array([.26/4.8,.7/4.9,.3/4.3])
        if not live[1:].any():expected[0]=expected.sum();frac[0]=.1
        lo=np.maximum(.001,expected*(1-frac)/np.maximum(intrinsic,1e-30))
        hi=expected*(1+frac)/np.maximum(intrinsic,1e-30)
        scale=np.maximum(sd[train],floor)
        A=components[:,train].T[:,live]/scale[:,None];y=data[train]/scale
        obj,x=bounded_lsq(A,y,lo[live],hi[live])
        coeff=np.zeros(3);coeff[live]=x
        ck(model+' coefficients independent active-set solution',np.max(abs(coeff-record['bounded_fit']['coefficients'])),1e-7)
        prediction=np.einsum('i,ijkl->jkl',coeff,components)
        ck(model+' prediction',np.max(abs(prediction-a[model+'_bounded_prediction'])),2e-8)
        metrics={}
        for name,m in masks.items():
            residual=data-prediction
            key='train' if name=='training' else name
            val=float(np.sqrt(np.mean((residual[m]/np.maximum(sd[m],floor))**2)))
            ref=record['bounded_fit']['metrics'][key]['RMS_in_empirical_blank_scatter']
            ck(model+' '+name+' RMS recomputation',abs(val-ref),5e-7)
            metrics[name]={'RMS_in_blank_scatter':val,'bins':int(m.sum())}
        continuum=continuous_component_flux(p)
        relative=abs(intrinsic-continuum)/np.maximum(continuum,1e-30)
        # This is a finite quadrature benchmark only, not proof all profiles converge.
        ck(model+' source-flux quadrature vs exact-angular/continuous-radial integral',relative.max(),.005)
        detail[model]={'coefficients':coeff.tolist(),'weighted_training_objective':obj,
            'intrinsic_saved_flux':intrinsic.tolist(),'continuous_flux':continuum.tolist(),
            'source_flux_relative_errors':relative.tolist(),'metrics':metrics,
            'source_flux_note':'Independent analytic angular and piecewise/quadrature radial integration; no production renderer imports.'}
    result={'all_passed':all(v['passed'] for v in checks),'checks':checks,'details':detail,
      'production_code_imported':False,'new_actual_data_fit':False,
      'interpretation':'Finite saved-result/source normalization reconstruction; no discovery significance or fullfit posterior.'}
    (out/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 0 if result['all_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
