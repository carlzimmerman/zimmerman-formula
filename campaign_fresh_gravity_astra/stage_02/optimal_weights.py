"""AFG-007: estimate the Q scale directly while cancelling unknown local u²."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from measurement import disk, psf, raw_moment, response, noise_moment, E3, estimate


def moments(P,I,q,B,s2,a):
    u=np.sqrt(q*response(B,a))
    return {n:P@(I*raw_moment(n,u,s2)) for n in [2,4,6,8]}


def estimator(P,I,q,B,s2):
    n=P.shape[0]
    nuisance=np.vstack([P,6*P*s2[None,:]])
    signal=np.r_[np.zeros(n),P@(I*q*q*B)]
    N=null_space(nuisance.T,rcond=1e-12)
    if N.shape[1]==0:
        return None,dict(null_dimension=0,observations=n,source_cells=P.shape[1],
                         status='No exact linear invariant at stated numerical rank tolerance')
    design=moments(P,I,q,B,s2,1.)
    C=np.block([[np.diag(design[4]),np.diag(design[6])],
                [np.diag(design[6]),np.diag(design[8])]])
    target=N.T@signal
    if np.linalg.norm(target)<1e-12*np.linalg.norm(signal):
        return None,dict(null_dimension=N.shape[1],status='Signal also projected out')
    reduced=N.T@C@N
    v=np.linalg.solve(reduced,target)
    h=N@v/float(target@v)
    residual=nuisance.T@h
    return h,dict(null_dimension=N.shape[1],observations=n,source_cells=P.shape[1],
                   design_scale=1.,singular_value_relative_cutoff=1e-12,
                   nuisance_max_absolute_residual=float(np.max(abs(residual))),
                   signal_normalization=float(h@signal),
                   condition_of_reduced_covariance=float(np.linalg.cond(reduced)),
                   status='Constructed exact linear estimator within floating residual')


def evaluate(h,P,I,q,B,s2,a,true_width_factor=1.):
    n=P.shape[0]; h2,h4=h[:n],h[n:]
    true=moments(P,I,q,B,s2*true_width_factor**2,a)
    y2=true[2]-P@(I*s2)
    y4=true[4]-P@(I*noise_moment(4,s2))-P@(I*q*q*B*B)
    value=float(h2@y2+h4@y4)
    variance=float(np.sum(h2*h2*true[4]+2*h2*h4*true[6]+h4*h4*true[8]))
    assert variance>0
    return dict(scale=a,true_width_factor=true_width_factor,estimated_scale=value,
                bias=value-a,sigma_at_10000_photons=float(np.sqrt(variance/10000)))


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    pos,r,p,q,B,I,s2=disk(); rows=[]
    for width in [.05,.2,.4,.7,1.]:
        P=psf(pos,width); h,meta=estimator(P,I,q,B,s2)
        assert h is not None
        tested=[]
        for a in [1.,E3]:
            result=evaluate(h,P,I,q,B,s2,a)
            assert abs(result['bias'])<1e-7
            direct=estimate(P,I,q,B,s2,a)
            result['direct_estimator_sigma']=direct['sigma_scale_at_10000_photons']
            result['direct_over_optimized_sigma']=direct['sigma_scale_at_10000_photons']/result['sigma_at_10000_photons']
            if a==1.:
                assert result['sigma_at_10000_photons']<=direct['sigma_scale_at_10000_photons']*(1+1e-8)
            tested.append(result)
        width_sensitivity=[evaluate(h,P,I,q,B,s2,1.,factor) for factor in [.9,1.1]]
        rows.append(dict(psf_sigma=width,estimator=meta,scale_tests=tested,width_calibration_tests=width_sensitivity))
    # Coarsen 8x8 pixels into nonoverlapping 2x2 blocks, retaining every photon.
    R=np.zeros((16,64))
    for iy in range(8):
        for ix in range(8): R[(iy//2)*4+ix//2,iy*8+ix]=1
    coarse=[]
    for kind,smap in [('varying',s2),('constant',np.full_like(s2,.025))]:
        P=R@psf(pos,.4); h,meta=estimator(P,I,q,B,smap)
        if kind=='varying': assert h is None
        else:
            assert h is not None
            val=evaluate(h,P,I,q,B,smap,E3)
            assert abs(val['bias'])<1e-8
            meta['scale_test']=val
        coarse.append(dict(width_map=kind,estimator=meta))
    report=dict(checkpoint='AFG-007',full_resolution=rows,coarsened=coarse,
                interpretation='Minimum variance among linear estimators cancelling arbitrary source u² with known maps, at the stated design covariance. Not minimum among all nonlinear model fits.',
                limitations=['All baryon, emissivity, geometry and response maps are known synthetic inputs.',
                             'Numerical row-space ranks are tolerance-dependent; no real detector tested.'])
    (args.out/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=='__main__': main()
