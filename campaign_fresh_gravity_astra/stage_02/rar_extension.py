"""AFG-008: positive effective source weights and exact RAR scale inversion."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space, solve_triangular
from scipy.optimize import brentq, minimize, LinearConstraint
from measurement import disk,psf,response,raw_moment,noise_moment,E3,inverse_moment_weights
from optimal_weights import estimator,moments


def positive_estimator(P,I,q,B,s2):
    h,meta=estimator(P,I,q,B,s2); n=P.shape[0]
    alpha=P.T@h[n:]
    if min(alpha)>=0:
        return h,dict(method='Unconstrained optimum already has positive source weights',min_alpha=float(min(alpha)))
    D=np.vstack([P,6*P*s2[None,:]])
    N=null_space(D.T,rcond=1e-12)
    design=moments(P,I,q,B,s2,1.)
    C=np.block([[np.diag(design[4]),np.diag(design[6])],[np.diag(design[6]),np.diag(design[8])]])
    L=np.linalg.cholesky(N.T@C@N)
    transform=N@solve_triangular(L.T,np.eye(len(L)),lower=False)
    signal=np.r_[np.zeros(n),P@(I*q*q*B)]
    k=signal@transform
    T=P.T@transform[n:,:]
    z0=k/(k@k)
    objective_scale=float(z0@z0)
    # Scale inequality units without changing its feasible set.
    scale=float(np.max(abs(T@z0)))
    constraints=[LinearConstraint(k[None,:],1.,1.),LinearConstraint(T/scale,0.,np.inf)]
    result=minimize(lambda z:.5*(z@z)/objective_scale,z0,jac=lambda z:z/objective_scale,
                    constraints=constraints,method='SLSQP',options=dict(ftol=1e-11,maxiter=500))
    assert result.success, result.message
    hc=transform@result.x
    # Mix an infinitesimal amount of a known positive feasible estimator to
    # handle any roundoff-scale negative source weights, retaining both equalities.
    l4,l2,ad,_=inverse_moment_weights(P,s2)
    C1=float(np.sum(ad*I*q*q*B)); hd=np.r_[-6*l2,l4]/C1
    ac=P.T@hc[n:]; ad=P.T@hd[n:]
    mix=0.
    if min(ac)<0:
        mix=float(np.max(np.maximum(0.,(-ac+1e-10)/(ad-ac))))
        hc=(1-mix)*hc+mix*hd
    alpha=P.T@hc[n:]
    assert min(alpha)>-1e-8 and abs(signal@hc-1)<1e-8
    assert np.max(abs(D.T@hc))<1e-7
    return hc,dict(method='Convex quadratic minimum with nonnegative effective source weights',
                   iterations=int(result.nit),solver_success=bool(result.success),
                   min_alpha=float(min(alpha)),roundoff_feasibility_mix=mix,
                   constraint_residual=float(np.max(abs(D.T@hc))))


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    pos,r,p,q,B,I,s2=disk(); rows=[]
    for width in [.05,.2,.4,.7,1.]:
        P=psf(pos,width); n=P.shape[0]; h,meta=positive_estimator(P,I,q,B,s2)
        h2,h4=h[:n],h[n:]; alpha=P.T@h4
        for a in [1.,E3]:
            g=response(B,a,'R'); u=np.sqrt(q*g)
            obs={k:P@(I*raw_moment(k,u,s2)) for k in [2,4,6,8]}
            T4=float(h2@(obs[2]-P@(I*s2))+h4@(obs[4]-P@(I*noise_moment(4,s2))))
            def predicted(scale): return float(np.sum(alpha*I*q*q*response(B,scale,'R')**2))
            recovered=brentq(lambda scale:predicted(scale)-T4,.01,20.,xtol=1e-11)
            assert abs(recovered/a-1)<1e-8
            step=a*1e-5
            derivative=(predicted(a+step)-predicted(a-step))/(2*step)
            variance=float(np.sum(h2*h2*obs[4]+2*h2*h4*obs[6]+h4*h4*obs[8]))
            assert derivative>0 and variance>0
            q_inferred=float(T4-np.sum(alpha*I*q*q*B*B))
            rows.append(dict(psf_sigma=width,scale=a,recovered_RAR_scale=float(recovered),
                source_weight_min=float(min(alpha)),estimator=meta,
                local_sigma_RAR_scale_at_10000_photons=float(np.sqrt(variance/10000)/derivative),
                wrong_Q_scale_from_same_moments=q_inferred))
    report=dict(checkpoint='AFG-008',rows=rows,
        interpretation='Nonnegative effective source weights give a strictly monotone RAR fourth-moment forward map; invert it separately from Q.',
        limitations=['Positive-weight constrained variance minimum uses Q scale-1 design covariance; it is a design criterion, not optimal for every RAR scale.',
                     'Local delta-method errors; all source and instrument maps known; no measured spectrum.'])
    (args.out/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=='__main__': main()
