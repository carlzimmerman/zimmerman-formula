"""Independent GH-moment, constrained-optimality and numerical rank checks."""
import argparse
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.hermite import hermgauss
from scipy.linalg import null_space, solve_triangular
from scipy.optimize import lsq_linear
from measurement import disk,psf,response,raw_moment,E3,inverse_moment_weights
from optimal_weights import estimator,moments
from rar_extension import positive_estimator


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    pos,r,p,q,B,I,s2=disk(); nodes,weights=hermgauss(8); weights/=np.sqrt(np.pi)
    results=[]
    for width in [.05,.4,1.]:
        P=psf(pos,width); n=len(P); h,meta=positive_estimator(P,I,q,B,s2)
        h2,h4=h[:n],h[n:]
        design=moments(P,I,q,B,s2,1.)
        C=np.block([[np.diag(design[4]),np.diag(design[6])],[np.diag(design[6]),np.diag(design[8])]])
        D=np.vstack([P,6*P*s2[None,:]]); signal=np.r_[np.zeros(n),P@(I*q*q*B)]
        N=null_space(D.T,rcond=1e-12); L=np.linalg.cholesky(N.T@C@N)
        transform=N@solve_triangular(L.T,np.eye(len(L)),lower=False)
        z=np.linalg.lstsq(transform,h,rcond=None)[0]
        k=signal@transform; T=P.T@transform[n:]
        alpha=P.T@h4; active=alpha<1e-7*max(alpha)
        # KKT: z = lambda k + T_active^T mu, mu >=0. Lambda is unrestricted.
        A=np.column_stack([k,-k,T[active].T])
        dual=lsq_linear(A,z,bounds=(0,np.inf),tol=1e-12,max_iter=1000)
        stationarity=float(np.linalg.norm(A@dual.x-z)/np.linalg.norm(z))
        assert stationarity<1e-5
        hu,_=estimator(P,I,q,B,s2)
        l4,l2,alpha_d,_=inverse_moment_weights(P,s2)
        C1=float(np.sum(alpha_d*I*q*q*B)); hd=np.r_[-6*l2,l4]/C1
        v=float(h@C@h); vu=float(hu@C@hu); vd=float(hd@C@hd)
        assert vu<=v*(1+1e-7) and v<=vd*(1+1e-7)
        for a in [1.,E3]:
            for kernel in ['Q','R']:
                u=np.sqrt(q*response(B,a,kernel))
                vals=u[:,None]+np.sqrt(2*s2)[:,None]*nodes[None,:]
                # Independent joint expectation over source, detected pixel and line velocity.
                raw=h2[:,None,None]*vals[None,:,:]**2+h4[:,None,None]*vals[None,:,:]**4
                mean=float(np.sum(P[:,:,None]*I[None,:,None]*weights[None,None,:]*raw))
                second=float(np.sum(P[:,:,None]*I[None,:,None]*weights[None,None,:]*raw**2))
                M={j:P@(I*raw_moment(j,u,s2)) for j in [2,4,6,8]}
                expected_mean=float(h2@M[2]+h4@M[4])
                expected_second=float(np.sum(h2*h2*M[4]+2*h2*h4*M[6]+h4*h4*M[8]))
                error_mean=abs(mean-expected_mean)/max(1.,abs(mean))
                error_second=abs(second/expected_second-1)
                assert error_mean<1e-9 and error_second<1e-9
                results.append(dict(psf_sigma=width,scale=a,kernel=kernel,
                    GH_relative_second_moment_error=error_second,GH_scaled_mean_error=error_mean,
                    KKT_relative_stationarity_residual=stationarity,
                    constrained_variance=v,unconstrained_lower_variance=vu,direct_upper_variance=vd))
    R=np.zeros((16,64))
    for iy in range(8):
        for ix in range(8):R[(iy//2)*4+ix//2,iy*8+ix]=1
    P=R@psf(pos,.4); D=np.vstack([P,6*P*s2[None,:]])
    singular=np.linalg.svd(D.T,compute_uv=False)
    rank_checks={str(cut):int(sum(singular>singular[0]*cut)) for cut in [1e-10,1e-12,1e-14]}
    assert set(rank_checks.values())=={32}
    report=dict(checkpoint='AFG-004-008-audit',joint_moment_checks=results,
                coarse_nuisance_rank=rank_checks,coarse_smallest_relative_singular_value=float(singular[-1]/singular[0]),
                scope='Self-review with independent quadrature and finite KKT/rank checks, not an independent agent or empirical validation.')
    (args.out/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=='__main__':main()
