"""AFG-004–006 synthetic measurement operators, exact controls and noise checks."""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

SEED=27092026
E3=float(np.sqrt(.315*4**3+.685))
A0={'canonical':9.3619e-11,'alternative':1.1279e-10}
KPC=3.085677581491367e19


def response(B,a,kernel='Q'):
    if kernel=='Q': return np.sqrt(B*B+a*B)
    return B/(-np.expm1(-np.sqrt(B/a)))


def noise_moment(order,s2,kind='gaussian'):
    if order==0: return np.ones_like(s2)
    if order%2: return np.zeros_like(s2)
    j=order//2
    if kind=='uniform': return (3*s2)**j/(2*j+1)
    return math.prod(range(1,order,2))*s2**j


def raw_moment(order,u,s2,kind='gaussian'):
    return sum(math.comb(order,j)*u**(order-j)*noise_moment(j,s2,kind)
               for j in range(0,order+1,2))


def disk():
    axis=(np.arange(8)-3.5)*.5
    x,y=np.meshgrid(axis,axis)
    pos=np.column_stack([x.ravel(),y.ravel()])
    inc=np.deg2rad(55.)
    r=np.sqrt(pos[:,0]**2+(pos[:,1]/np.cos(inc))**2)
    p=np.sin(inc)*pos[:,0]/r
    q=p*p*r
    B=.1*r/(1+r*r)**1.5
    I=np.exp(-r/1.5); I/=I.sum()
    s2=.015+.01*r/(1+r)+.008*np.sin(2*pos[:,0])**2
    return pos,r,p,q,B,I,s2


def psf(pos,width):
    d2=np.sum((pos[:,None,:]-pos[None,:,:])**2,axis=2)
    P=np.exp(-d2/(2*width*width))
    return P/P.sum(axis=0)


def inverse_moment_weights(P,s2):
    l4=np.ones(P.shape[0])
    alpha=P.T@l4
    l2=np.linalg.lstsq(P.T,alpha*s2,rcond=1e-12)[0]
    return l4,l2,alpha,alpha*s2-P.T@l2


def estimate(P,I,q,B,s2,a,kind='gaussian',kernel='Q'):
    g=response(B,a,kernel); u=np.sqrt(q*g)
    l4,l2,alpha,residual=inverse_moment_weights(P,s2)
    M={n:P@(I*raw_moment(n,u,s2,kind)) for n in [2,4,6,8]}
    C0=float(np.sum(alpha*I*q*q*B*B))
    C1=float(np.sum(alpha*I*q*q*B))
    known2=P@(I*s2)
    known4=P@(I*noise_moment(4,s2,kind))
    T4=l4@(M[4]-known4)-6*l2@(M[2]-known2)
    recovered=float((T4-C0)/C1)
    predicted_bias=float(6*np.sum(I*residual*q*g)/C1)
    var_per_photon=float(np.sum(l4*l4*M[8]+36*l2*l2*M[4]-12*l4*l2*M[6])/C1**2)
    assert var_per_photon>0
    if kernel=='Q':
        assert abs(recovered-a-predicted_bias)<1e-8*max(1.,a,abs(recovered))
    return dict(scale=a,kernel=kernel,broadening=kind,recovered_scale=recovered,
                predicted_adjoint_residual_bias=predicted_bias,
                relative_adjoint_residual=float(np.linalg.norm(residual)/np.linalg.norm(alpha*s2)),
                weight_norm=float(np.linalg.norm(l2)),condition_number=float(np.linalg.cond(P)),
                sigma_scale_at_10000_photons=float(np.sqrt(var_per_photon/10000)))


def disk_experiments():
    pos,r,p,q,B,I,s2=disk()
    rows=[]
    for width in [.05,.2,.4,.7,1.]:
        P=psf(pos,width)
        assert np.max(abs(P.sum(axis=0)-1))<1e-14
        for a in [1.,E3]:
            for kind in ['gaussian','uniform']:
                row=estimate(P,I,q,B,s2,a,kind)
                row['psf_sigma_over_r_reference']=width
                rows.append(row)
    # R is a different law; the Q-specific inferred scale is not required to equal a.
    rar=estimate(psf(pos,.2),I,q,B,s2,1.,kernel='R')
    assert abs(rar['recovered_scale']-1)>.01
    # Independent integration of a source line, including a non-Gaussian LSF.
    moment_errors=[]
    u=float(np.sqrt(q[3]*response(B[3],E3)))
    variance=float(s2[3]); sig=np.sqrt(variance)
    for kind in ['gaussian','uniform']:
        for order in [2,4,6,8]:
            if kind=='gaussian':
                val=quad(lambda x:(u+x)**order*np.exp(-.5*(x/sig)**2)/(sig*np.sqrt(2*np.pi)),
                         -12*sig,12*sig,epsabs=1e-12)[0]
            else:
                half=np.sqrt(3*variance)
                val=quad(lambda x:(u+x)**order/(2*half),-half,half,epsabs=1e-12)[0]
            expected=float(raw_moment(order,u,variance,kind))
            moment_errors.append(abs(val/expected-1))
    assert max(moment_errors)<1e-10
    return rows,dict(source_cells=len(B),inclination_degrees=55,
                     radius_range_over_reference=[float(r.min()),float(r.max())],
                     B_range_over_reference=[float(B.min()),float(B.max())],
                     independent_line_quadrature_max_error=max(moment_errors),
                     wrong_kernel_control=rar)


def poisson_check():
    pos,r,p,q,B,I,s2=disk(); P=psf(pos,.4)
    a=E3; u=np.sign(p)*np.sqrt(q*response(B,a))
    l4,l2,alpha,residual=inverse_moment_weights(P,s2)
    C0=float(np.sum(alpha*I*q*q*B*B)); C1=float(np.sum(alpha*I*q*q*B))
    known2=P@(I*s2); known4=P@(I*noise_moment(4,s2))
    constant=float(-l4@known4+6*l2@known2-C0)
    M={n:P@(I*raw_moment(n,u,s2)) for n in [4,6,8]}
    budget,replicates=5000,400
    variance=float(np.sum(l4*l4*M[8]+36*l2*l2*M[4]-12*l4*l2*M[6])/(budget*C1*C1))
    rng=np.random.default_rng(SEED); cdf=np.cumsum(P,axis=0)
    inferred=[]
    for _ in range(replicates):
        N=int(rng.poisson(budget))
        source=rng.choice(len(I),size=N,p=I)
        pixel=np.sum(cdf[:,source]<rng.random(N)[None,:],axis=0)
        v=u[source]+rng.normal(size=N)*np.sqrt(s2[source])
        observed=float(np.sum(l4[pixel]*v**4-6*l2[pixel]*v*v)/budget)
        inferred.append((observed+constant)/C1)
    empirical=float(np.var(inferred,ddof=1)); ratio=empirical/variance
    zmean=float((np.mean(inferred)-a)/np.sqrt(variance/replicates))
    assert .7<ratio<1.3 and abs(zmean)<4
    return dict(seed=SEED,expected_photons=budget,replicates=replicates,
                actual_scale=a,mean_recovered=float(np.mean(inferred)),
                analytic_sigma=float(np.sqrt(variance)),empirical_sigma=float(np.sqrt(empirical)),
                empirical_over_analytic_variance=ratio,mean_offset_in_MC_standard_errors=zmean,
                assumptions='Poisson arrivals, known exposure flux and maps; no continuum, background or calibration uncertainty.')


def rank_counterexample():
    P=np.ones((1,2)); I=np.array([.5,.5]); s2=np.array([.04,.16])
    u2a=np.array([.2,.8]); u2b=u2a[::-1]
    second_a=float((P@(I*u2a))[0]); second_b=float((P@(I*u2b))[0])
    mixed_a=float((P@(I*s2*u2a))[0]); mixed_b=float((P@(I*s2*u2b))[0])
    _,_,_,residual=inverse_moment_weights(P,s2)
    assert second_a==second_b and abs(mixed_a-mixed_b)>.03
    return dict(second_moment_both=second_a,mixed_width_moment_A=mixed_a,
                mixed_width_moment_B=mixed_b,residual=residual.tolist(),
                scope='Second moments alone cannot supply a law-independent linear correction for this unresolved width map.')


def width_degeneracy():
    weights=np.array([.9,.1]); shape=np.array([.01,1.])
    def intrinsic(a,c):
        B=c*shape; g=response(B,a)
        U=float(weights@g); V=float(weights@(g*g)); W=float(weights@(g**3))
        return U,V-3*U*U,W-15*V*U+30*U**3
    c=brentq(lambda value:intrinsic(E3,value)[1]-intrinsic(1.,value)[1],.0001,1e4,xtol=1e-12)
    B=c*shape
    observed_second=intrinsic(E3,c)[0]+.1
    models=[]
    # Symmetric approaching/receding copies make the toy line mean zero.
    for a in [1.,E3]:
        g=response(B,a); u=np.sqrt(g)
        s2=observed_second-float(weights@g)
        moments={n:float(weights@raw_moment(n,u,s2)) for n in range(2,13,2)}
        J6=moments[6]-15*moments[4]*moments[2]+30*moments[2]**3
        grad=np.array([-15*moments[4]+90*moments[2]**2,-15*moments[2],1.])
        orders=[2,4,6]
        cov=np.array([[moments[i+j]-moments[i]*moments[j] for j in orders] for i in orders])
        variance=float(grad@cov@grad)
        # Numerical integration checks the observable line rather than only its expansion.
        sig=np.sqrt(s2)
        def density(v):
            return float(np.sum(weights*(np.exp(-.5*((v-u)/sig)**2)+np.exp(-.5*((v+u)/sig)**2)))/(2*sig*np.sqrt(2*np.pi)))
        limit=float(max(u)+12*sig)
        errors=[]
        for n in [2,4,6]:
            measured=quad(lambda v:v**n*density(v),-limit,limit,epsabs=1e-12)[0]
            errors.append(abs(measured/moments[n]-1))
        assert max(errors)<1e-10 and s2>0
        models.append(dict(scale=a,width_variance=s2,observed_m2=moments[2],observed_m4=moments[4],
                           observed_m6=moments[6],gaussian_invariant_J6=J6,
                           J6_asymptotic_variance_per_photon=variance,
                           spectral_quadrature_max_relative_error=max(errors),
                           width_kms_at_5kpc={k:float(np.sqrt(s2*a0*5*KPC)/1000) for k,a0 in A0.items()}))
    assert abs(models[0]['observed_m2']/models[1]['observed_m2']-1)<1e-12
    assert abs(models[0]['observed_m4']/models[1]['observed_m4']-1)<1e-10
    difference=abs(models[0]['gaussian_invariant_J6']-models[1]['gaussian_invariant_J6'])
    assert difference>.01
    derivatives=[]
    for a in np.logspace(-4,4,101):
        g=response(B,a); U=float(weights@g)
        Up=float(weights@(B/(2*g))); Upp=float(weights@(-B*B/(4*g**3)))
        Hpp=-6*(Up*Up+U*Upp)
        assert Hpp>=-1e-12
        derivatives.append(Hpp)
    N=9*max(m['J6_asymptotic_variance_per_photon'] for m in models)/difference**2
    return dict(weights=weights.tolist(),B_over_a_reference=B.tolist(),models=models,
                min_sampled_H_second_derivative=min(derivatives),J6_difference=difference,
                idealized_asymptotic_photons_for_3sigma_J6_separation=float(N),
                limitation='Toy asymptotic moment precision only: no nuisance fitting, real detector model, backgrounds or empirical spectrum.')


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    rows,meta=disk_experiments()
    result=dict(checkpoints=['AFG-004','AFG-005','AFG-006'],disk_metadata=meta,disk_runs=rows,
                poisson_validation=poisson_check(),rank_deficient_example=rank_counterexample(),
                unknown_width_degeneracy=width_degeneracy())
    (args.out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__': main()
