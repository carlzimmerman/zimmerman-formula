"""Known-map local recovery versus exact scale/source/geometry ambiguity."""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares

HERE=Path(__file__).resolve().parent
STAGE2=HERE.parents[1]/'stage_02'
sys.path.insert(0,str(STAGE2))
from measurement import disk,psf,response,raw_moment,E3


def derivative_a(B,a,kernel):
    if kernel=='Q':return B/(2*response(B,a))
    t=np.sqrt(B/a);d=-np.expm1(-t)
    return B*t*np.exp(-t)/(2*a*d*d)


def forward(P,I,q,B,s2,a,lam,kernel):
    g=response(B,a,kernel)
    return P@(I*(q*g+lam*s2))


def derivatives(P,I,q,B,s2,a,kernel):
    return np.column_stack([P@(I*q*derivative_a(B,a,kernel)),P@(I*s2)])


def aggregation(kind):
    if kind=='64_pixels':return np.eye(64)
    if kind=='one_aperture':return np.ones((1,64))
    R=np.zeros((16,64))
    for iy in range(8):
        for ix in range(8):R[(iy//2)*4+ix//2,iy*8+ix]=1
    return R


def recovery():
    pos,r,p,q,B,I,s2=disk(); rows=[]
    for kernel in ['Q','R']:
        for width in [.2,.7,1.]:
            for shape in ['64_pixels','16_pixels','one_aperture']:
                P=aggregation(shape)@psf(pos,width)
                for a in [1.,E3]:
                    lam=1.44  # actual width is 20% above the uncalibrated baseline
                    truth=forward(P,I,q,B,s2,a,lam,kernel)
                    # Fixed design weighting, not an oracle covariance at the true scale.
                    design_u=np.sqrt(q*response(B,1.,kernel))
                    variance=P@(I*raw_moment(4,design_u,s2))
                    J=derivatives(P,I,q,B,s2,a,kernel)
                    step=a*1e-5
                    fd=(forward(P,I,q,B,s2,a+step,lam,kernel)-forward(P,I,q,B,s2,a-step,lam,kernel))/(2*step)
                    assert np.max(abs(fd-J[:,0]))<1e-9
                    JW=J/np.sqrt(variance[:,None])
                    singular=np.linalg.svd(JW,compute_uv=False)
                    rank=int(np.linalg.matrix_rank(JW,tol=singular[0]*1e-10))
                    cosine=float(JW[:,0]@JW[:,1]/(np.linalg.norm(JW[:,0])*np.linalg.norm(JW[:,1])))
                    row=dict(kernel=kernel,PSF_width=width,pixels=shape,true_a=a,true_variance_multiplier=lam,
                             local_rank=rank,weighted_column_cosine=cosine)
                    if shape=='one_aperture':
                        assert rank==1
                        # Construct a second positive-width scale giving the same mean.
                        alt_a=a*.8
                        alt_lam=float((truth[0]-forward(P,I,q,B,s2,alt_a,0.,kernel)[0])/(P@(I*s2))[0])
                        assert alt_lam>0
                        assert abs(forward(P,I,q,B,s2,alt_a,alt_lam,kernel)[0]/truth[0]-1)<1e-12
                        row.update(alternative_scale=alt_a,alternative_variance_multiplier=alt_lam)
                    else:
                        assert rank==2
                        fits=[]
                        for start in [[.2,.2],[1.,1.],[5.,3.],[9.,.5]]:
                            result=least_squares(lambda v:(forward(P,I,q,B,s2,v[0],v[1],kernel)-truth)/np.sqrt(variance),
                                start,jac=lambda v:derivatives(P,I,q,B,s2,v[0],kernel)/np.sqrt(variance[:,None]),
                                bounds=([.01,0.],[20.,20.]),xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=1000)
                            assert result.success and np.linalg.norm(result.x-[a,lam])<1e-7
                            fits.append(result.x.tolist())
                        fixed=least_squares(lambda v:(forward(P,I,q,B,s2,v[0],1.,kernel)-truth)/np.sqrt(variance),
                                            [1.],bounds=([.01],[20.]),gtol=1e-13,xtol=1e-13,ftol=1e-13)
                        row.update(multistart_solutions=fits,scale_if_width_is_wrongly_fixed=float(fixed.x[0]))
                    rows.append(row)
    return rows


def full_spectrum_invariance():
    pos,r,p,q,B,I,s2=disk(); P=psf(pos,.4); results=[]
    velocity=np.linspace(-3,3,701)
    def spectrum(a,beta,geometry,kernel):
        u=np.sign(p)*np.sqrt(geometry*q*response(beta*B,a,kernel))
        source=np.exp(-.5*((velocity[None,:]-u[:,None])/np.sqrt(s2[:,None]))**2)/np.sqrt(2*np.pi*s2[:,None])
        return P@(I[:,None]*source)
    for kernel in ['Q','R']:
        baseline=spectrum(1.,1.,1.,kernel)
        for c in [.5,E3,10.]:
            altered=spectrum(c,c,1/c,kernel)
            error=float(np.max(abs(altered-baseline))/np.max(baseline))
            assert error<1e-12
            results.append(dict(kernel=kernel,a_multiplier=c,baryon_multiplier=c,
                                geometry_multiplier=1/c,full_spectrum_relative_max_error=error))
    return results


def rank_is_not_global_uniqueness():
    saved=json.loads((STAGE2/'run_001/results.json').read_text())['unknown_width_degeneracy']
    B=np.array(saved['B_over_a_reference']);I=np.array(saved['weights']);q=np.ones_like(B)
    out=[]
    for model in saved['models']:
        a=model['scale'];s2=model['width_variance'];g=response(B,a);ga=derivative_a(B,a,'Q')
        J=np.array([[I@ga,1.],[I@(2*g*ga+6*s2*ga),I@(6*g+6*s2)]])
        determinant=float(np.linalg.det(J))
        normalized=J/np.linalg.norm(J,axis=0)
        singular=np.linalg.svd(normalized,compute_uv=False)
        assert np.linalg.matrix_rank(normalized,tol=1e-10)==2
        out.append(dict(scale=a,width_variance=s2,second_fourth_local_jacobian_determinant=determinant,
                        column_normalized_smallest_singular_value=float(singular[-1])))
    return dict(two_distinct_models_with_identical_second_fourth_moments=out,
                conclusion='Both solutions are locally identifiable; local full rank does not imply a unique global solution.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    result=dict(checkpoint='AFG-JI-01',spatial_recovery=recovery(),
                exact_full_spectrum_degeneracy=full_spectrum_invariance(),
                global_uniqueness_control=rank_is_not_global_uniqueness(),
                non_claims=['No measured spectra or empirical calibration; baryon/geometry rescalings are unconstrained test parameters, not established plausible errors.',
                            'Multistart finite recovery is not a proof of global identification.',
                            'Width-shape known with one unknown multiplier is a stronger assumption than arbitrary unknown cell widths.'])
    (args.out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':main()
