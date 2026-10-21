#!/usr/bin/env python3
"""Execute source-anchored forward models and protected-strip calibration."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import lsq_linear
from forward_model import load_preferred,load_author_base,render

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'ngc5023_cube_2026_10_20'
sys.path.insert(0,str(OLD))
from cube_analysis import Cube,BLANK_CENTERS

XC=(np.arange(30)-14.5)*20
ZC=(np.arange(12)-5.5)*20
UC=(np.arange(20)-9.5)*12.36
UU,ZZ,XX=np.meshgrid(UC,ZC,XC,indexing='ij')
FEATURES=[(-72,80,-24.8,56),(112,92,39.2,40),(120,-76,39.2,52)]


def bin20(a):
    return a.reshape(20,3,12,5,30,5).sum((1,3,5))*16*4.12


def outside_features(radius=40.,beam_guard=20.):
    m=np.ones(XX.shape,bool)
    for x,z,u,width in FEATURES:
        for s in [-1,1]:
            m &= ~((abs(XX-s*x)<=radius+10+beam_guard)&(abs(ZZ-s*z)<=radius+10+beam_guard)&
                   (abs(UU-s*u)<=width/2+6.18+8.24))
    return m


def regions():
    safe=outside_features(40,20)
    train=(abs(ZZ)<=10)&(abs(XX)<=230)&(abs(UU)<=105)&safe
    valid=(abs(ZZ)>=50)&(abs(XX)<=230)&(abs(UU)<=105)&safe
    guarded=valid&(abs(ZZ)>=70)
    return train,valid,guarded


def fit_components(model,data,blanks,metadata,source_bounded=True):
    train,valid,guarded=regions()
    sd=blanks.std(0,ddof=1)
    floor=np.median(sd[train])*.5
    scale=np.maximum(sd[train],floor)
    A=model[:,train].T.astype(float);y=data[train].astype(float)
    intrinsic=np.array([c['intrinsic_integrated_flux_Jy_km_s'] for c in metadata['components']])
    alive=intrinsic>1e-10
    lows,highs=np.zeros(3),np.full(3,3.)
    if source_bounded:
        expected=np.array([4.8e8,4.9e7,4.3e7])/(2.356e5*6.6**2)
        fractions=np.array([.26/4.8,.7/4.9,.3/4.3])
        # Actual baseline contains all gas in half-disks, not preferred disk-only.
        if not alive[1:].any():expected[0]=expected.sum();fractions[0]=.1
        lows=np.maximum(.001,expected*(1-fractions)/np.maximum(intrinsic,1e-30))
        highs=expected*(1+fractions)/np.maximum(intrinsic,1e-30)
    fit=lsq_linear(A[:,alive]/scale[:,None],y/scale,bounds=(lows[alive],highs[alive]),tol=1e-10)
    coeff=np.zeros(3);coeff[alive]=fit.x
    prediction=np.tensordot(coeff,model,axes=(0,0))
    residual=data-prediction
    metrics={}
    for name,m in [('train',train),('validation',valid),('guarded_validation',guarded)]:
        metrics[name]={'bins':int(m.sum()),'RMS_flux_Jy_km_s':float(np.sqrt(np.mean(residual[m]**2))),
          'RMS_in_empirical_blank_scatter':float(np.sqrt(np.mean((residual[m]/np.maximum(sd[m],floor))**2))),
          'median_abs_in_blank_scatter':float(np.median(abs(residual[m])/np.maximum(sd[m],floor))),
          'signed_flux_residual_Jy_km_s':float(residual[m].sum())}
    return {'coefficients':coeff.tolist(),'coefficient_bounds':[lows.tolist(),highs.tolist()],
            'success':bool(fit.success),'fit_source_mass_bounded':source_bounded,
            'metrics':metrics,'statistical_scope':'RMS/blank-scatter diagnostics, not chi-square or a joint likelihood'},prediction


def prepare_data():
    cube=Cube('HR',0.);a=cube.sample();blanks=[];centers=[]
    for x,z in BLANK_CENTERS:
        b=cube.sample(dx=x,dz=z)
        if np.isfinite(b).all():blanks.append(bin20(b));centers.append([x,z])
    return a,np.array(blanks),{'metadata':cube.metadata,'blank_centers':centers}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output);out.mkdir(exist_ok=True)
    a,blanks,datainfo=prepare_data();d=bin20(a)
    archive={'data_native':a,'data_binned':d,'blanks_binned':blanks,'X':XC,'Z':ZC,'U':UC}
    train,valid,guarded=regions()
    archive.update({'training_mask':train,'validation_mask':valid,'guarded_validation_mask':guarded})
    result={'data':datainfo,'models':{},'no_cosmology':True,'no_gravity_law':True,
        'region_definition':'training|z|<=10arcsec;validation|z|>=50;guarded>=70;x<=230,u<=105. Symmetric knownfeature40arcsec boxes enlarged by binhalfwidth10 and nativebeamguard20; velocityFWZI/2+6.18+8.24.',
        'interpretation':'Exploratory reconstruction. Spatial/velocity bins correlated; beam couples train/validation. No independent-pixel significance.'}
    for name,p in [('author_base',load_author_base()),('preferred_reconstructed',load_preferred())]:
        print('Rendering',name,flush=True)
        m,meta=render(p);mb=np.array([bin20(x) for x in m])
        bounded,pred=fit_components(mb,d,blanks,meta,True)
        free,freepred=fit_components(mb,d,blanks,meta,False)
        result['models'][name]={'parameters':p,'render_metadata':meta,'bounded_fit':bounded,'free_amplitude_diagnostic':free,
           'unfitted_training_RMS_flux':float(np.sqrt(np.mean((d[train]-mb.sum(0)[train])**2)))}
        archive[name+'_components_native']=m;archive[name+'_components_binned']=mb
        archive[name+'_bounded_prediction']=pred;archive[name+'_free_prediction']=freepred
        print(name,bounded,flush=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    np.savez_compressed(out/'arrays.npz',**archive)


if __name__=='__main__':main()
