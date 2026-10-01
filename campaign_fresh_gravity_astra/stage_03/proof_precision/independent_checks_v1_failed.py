"""Independent checks: no imports from campaign implementations. Binary64 + rationals."""
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


def gaussian_moments(u, variance, top=12):
    # Integration-by-parts recurrence, independently of binomial implementation.
    m = [np.ones_like(u), u]
    for n in range(2, top + 1):
        m.append(u*m[-1]+(n-1)*variance*m[-2])
    return m


def main(out):
    E = math.sqrt(.315*64+.685)
    # Exact counterexample within stated I>=0 hypothesis.
    widths = [F(1,25), F(4,25)]
    alpha, I, l2 = [F(1), F(1)], [F(1), F(0)], F(1,25)
    delta = [widths[i]-l2 for i in range(2)]
    assert delta != [0,0] and [I[i]*delta[i] for i in range(2)] == [0,0]
    support = dict(P=[[1,1]],I=[1,0],squared_widths=list(map(str,widths)),
                   l4=1,l2=str(l2),full_S5_residual=list(map(str,delta)),
                   effective_residual=['0','0'],
                   conclusion='Exact correction holds for every supported velocity despite full S5 failing.')

    w=np.array([.9,.1]); shape=np.array([.01,1.])
    def hh(a, b):
        g=np.sqrt(b*b+a*b); U=w@g
        return w@(g*g)-3*U*U
    k=brentq(lambda t:hh(E,t*shape)-hh(1,t*shape),.01,10,xtol=2e-14)
    B=k*shape; observed2=w@np.sqrt(B*B+E*B)+.1
    ambiguous=[]
    for a in [1,E]:
        g=np.sqrt(B*B+a*B); u=np.sqrt(g); v=observed2-w@g
        m=[float(w@x) for x in gaussian_moments(u,v)]
        J=m[6]-15*m[4]*m[2]+30*m[2]**3
        grad=np.array([-15*m[4]+90*m[2]**2,-15*m[2],1])
        cov=np.array([[m[i+j]-m[i]*m[j] for j in [2,4,6]] for i in [2,4,6]])
        vv=float(grad@cov@grad)
        ambiguous.append(dict(a=a,width_variance=float(v),m2=m[2],m4=m[4],m6=m[6],J6=J,var_J6=vv))
    assert abs(ambiguous[0]['m4']-ambiguous[1]['m4'])<2e-14
    photons=9*max(x['var_J6'] for x in ambiguous)/(ambiguous[0]['J6']-ambiguous[1]['J6'])**2
    convex=[]
    for a in [0,1e-4,1,E,1e4]:
        g=np.sqrt(B*B+a*B)
        pair=1.5*w[0]*w[1]*g[0]*g[1]*(1/(B[0]+a)-1/(B[1]+a))**2
        direct=-6*((w@(B/g)/2)**2+(w@g)*(w@(-B*B/(4*g**3))))
        assert pair>0 and abs(pair-direct)<2e-15
        convex.append(dict(a=a,pairwise_H_second=float(pair),derivative_H_second=float(direct)))

    # Independent PSF/raw moment and compound-Poisson variance check by
    # numerical integration of the actual one-photon polynomial.
    P=np.array([[.8,.3],[.2,.7]])
    flux=np.array([.4,.6]); widths=np.array([.03,.12]); q=np.array([.5,1.4]); baryon=np.array([.02,.4])
    l4=np.array([.8,1.3]); al=P.T@l4
    l2=np.linalg.solve(P.T,widths*al)
    C0=al@(flux*q*q*baryon*baryon); C1=al@(flux*q*q*baryon)
    psf=[]
    for a in [1,E]:
        intrinsic=np.sqrt(q*np.sqrt(baryon*baryon+a*baryon))
        for kind in ['gaussian','uniform']:
            numeric_mean=0.; numeric_second=0.; m2=np.zeros(2); m4=np.zeros(2)
            for i in range(2):
                s=math.sqrt(widths[i])
                lo,hi=(-12*s,12*s) if kind=='gaussian' else (-math.sqrt(3)*s,math.sqrt(3)*s)
                def pdf(e):
                    return math.exp(-e*e/(2*widths[i]))/(s*math.sqrt(2*math.pi)) if kind=='gaussian' else 1/(hi-lo)
                moments={n:quad(lambda e:(intrinsic[i]+e)**n*pdf(e),lo,hi,epsabs=1e-12)[0] for n in [2,4,6,8]}
                for j in range(2):
                    prob=flux[i]*P[j,i]
                    def phi(e):
                        v=intrinsic[i]+e
                        return l4[j]*v**4-6*l2[j]*v*v
                    numeric_mean+=prob*quad(lambda e:phi(e)*pdf(e),lo,hi,epsabs=1e-12)[0]
                    numeric_second+=prob*quad(lambda e:phi(e)**2*pdf(e),lo,hi,epsabs=1e-12)[0]
                    m2[j]+=prob*moments[2]; m4[j]+=prob*moments[4]
            k4=(3 if kind=='gaussian' else 9/5)*widths**2
            offset=-l4@(P@(flux*k4))+6*l2@(P@(flux*widths))
            recovered=(numeric_mean+offset-C0)/C1
            u=intrinsic
            if kind=='gaussian':
                mm=gaussian_moments(u,widths,8)
            else:
                h=np.sqrt(3*widths)
                mm=[((u+h)**(n+1)-(u-h)**(n+1))/(2*h*(n+1)) for n in range(9)]
            mapped={n:P@(flux*mm[n]) for n in [4,6,8]}
            s8=sum(l4*l4*mapped[8]+36*l2*l2*mapped[4]-12*l4*l2*mapped[6])
            assert abs(recovered-a)<1e-11 and abs(s8/numeric_second-1)<1e-11
            psf.append(dict(a=a,kind=kind,recovered=float(recovered),
                            poisson_variance_per_expected_photon=float(numeric_second/C1**2),
                            relative_S8_error=float(s8/numeric_second-1)))

    def law(b,a,kernel):
        return np.sqrt(b*b+a*b) if kernel=='Q' else b/(-np.expm1(-np.sqrt(b/a)))
    # Direct full-response normal integrations, without the original
    # implementation's baryon-plus-phantom split or exact second-moment insertion.
    def averaged(q,E,S,kernel,n,L):
        def f(z):
            b=q*np.exp(-S/2+math.sqrt(S)*z)
            return float(law(b,E,kernel)**n)*math.exp(-z*z/2)/math.sqrt(2*math.pi)
        return quad(f,-L,L,epsabs=1e-11,epsrel=2e-11,limit=300)[0]
    bounds=[]
    for z in [1,3,5]:
        ee=math.sqrt(.315*(1+z)**3+.685)
        for q in [1e-4,.01,.1,1]:
            for kernel in ['Q','R']:
                target=law(q,1,kernel)
                S=brentq(lambda ss:averaged(q,ee,ss,kernel,1,20)-target,0,50,xtol=1e-10)
                m1=averaged(q,ee,S,kernel,1,24)
                m2=averaged(q,ee,S,kernel,2,24)
                K=m2/m1**2
                bound=(q+ee)/(q+1) if kernel=='Q' else ee*(-np.expm1(-np.sqrt(q)))**2/q
                assert K>=max(1,bound)-1e-8 and abs(m1/target-1)<1e-8
                if kernel=='Q': assert abs(m2/(q*q*math.exp(S)+ee*q)-1)<1e-9
                bounds.append(dict(z=z,q=q,kernel=kernel,S=S,CV=math.sqrt(math.expm1(S)),K=K,lower_bound=float(max(1,bound))))
    # Positive finite RAR weights: monotonicity and independent root inversion.
    scales=np.logspace(-8,8,121); weights=np.array([.1,.7,.2]); bb=np.array([1e-3,.2,3.]); qq=np.array([.5,2,1])
    curves=np.array([sum(weights*qq**2*law(bb,a,'R')**2) for a in scales])
    assert np.all(np.diff(curves)>0)
    roots=[]
    for a in [1,E]:
        t=sum(weights*qq**2*law(bb,a,'R')**2)
        root=brentq(lambda aa:sum(weights*qq**2*law(bb,aa,'R')**2)-t,1e-8,1e3)
        assert abs(root/a-1)<1e-10
        roots.append(float(root))
    result=dict(support_counterexample=support,width_ambiguity=dict(B=B.tolist(),models=ambiguous,photons_3sigma=photons),
                convexity=convex,psf_and_variance=psf,transition_and_bounds=bounds,positive_RAR_inversion=roots,
                nonclaims=['Finite numerical checks do not prove universal theorems.','No new empirical spectra or physical gravity completion.'])
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status='all independent checks passed',ambiguity_photons=photons,transition_cases=len(bounds)),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    main(parser.parse_args().out)
