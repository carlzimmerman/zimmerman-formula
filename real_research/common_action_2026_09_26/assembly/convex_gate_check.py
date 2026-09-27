"""Convex activation primitive: exact ramp and finite Jensen controls.

The general analytic argument applies to any convex constitutive J. Grid
illustrations use its deep-MOND power, not an empirical nu_mono refit.
"""
import argparse,json,sys
from pathlib import Path
import sympy as s
import numpy as np


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    r,p,ell,theta,delta=s.symbols('r p ell theta delta',positive=True)
    f=35*r**4-84*r**5+70*r**6-20*r**7
    gg=7*r**5-14*r**6+10*r**7-s.Rational(5,2)*r**8
    checks={}
    def exact(name,value):
        residual=s.simplify(s.expand(value));assert residual==0,(name,residual)
        checks[name]={'passed':True,'residual':str(residual)}
    exact('ramp_derivative',s.diff(gg,r)-f)
    exact('ramp_monotonicity_factor',s.diff(f,r)-140*r**3*(1-r)**3)
    exact('ramp_zero',gg.subs(r,0))
    exact('ramp_half_integral',gg.subs(r,1)-s.Rational(1,2))
    exact('activation_upper',f.subs(r,1)-1)
    for order in [1,2,3,4]:
        exact('C4_join_zero_'+str(order),s.diff(gg,r,order).subs(r,0))
        exact('C4_join_one_'+str(order),s.diff(gg,r,order).subs(r,1)-(1 if order==1 else 0))
    exact('max_ramp_curvature',s.diff(f,r).subs(r,s.Rational(1,2))-s.Rational(35,16))
    # Scalar jet Hessian of G(J(p)+ell*d-theta). The matrix identity is general.
    d=s.symbols('d',real=True);J=s.Function('J')(p);G=s.Function('G')
    arg=J+ell*d-theta;E=G(arg)
    mat=s.hessian(E,(p,d))
    gp=s.Subs(s.Derivative(G(s.Symbol('z')),s.Symbol('z')),s.Symbol('z'),arg)
    # Use direct derivatives in the expected factorization to avoid assuming a primitive.
    z=s.symbols('z');Gprime=s.diff(G(z),z).subs(z,arg);Gsecond=s.diff(G(z),z,2).subs(z,arg)
    vec=s.Matrix([s.diff(J,p),ell])
    want=s.diag(Gprime*s.diff(J,p,2),0)+Gsecond*(vec*vec.T)
    for i in range(2):
        for j in range(2):exact(f'composition_Hessian_{i}_{j}',mat[i,j]-want[i,j])
    exact('composition_Hessian_determinant',mat.det()-ell**2*Gprime*Gsecond*s.diff(J,p,2))
    old=f*s.Rational(8,3)*p**s.Rational(3,2)
    olddet=s.simplify(s.hessian(old,(p,r)).det().subs(r,s.Rational(1,2)))
    exact('product_gate_negative_joint_Hessian',olddet+s.Rational(1225,16)*p)
    # Weighted divergence is a boundary term for full activation.
    xx=s.symbols('x',real=True);N=s.Function('N')(xx);W=s.Function('W')(xx);F=s.Function('F')(xx)
    LN=lambda u:s.diff(N*s.diff(u,xx),xx)/N
    exact('weighted_density_boundary',N*LN(W)-s.diff(N*s.diff(W,xx),xx))
    exact('weighted_adjoint_identity',N*F*LN(W)-N*W*LN(F)
          -s.diff(N*(F*s.diff(W,xx)-W*s.diff(F,xx)),xx))

    nn=96;xxn=2*np.pi*np.arange(nn)/nn
    freq=np.fft.fftfreq(nn,1/nn);xi=.15
    heat=np.exp(-.5*xi*xi*freq*freq)
    def deriv(v):return np.fft.ifft(1j*freq*np.fft.fft(v)).real
    def filt(v):return np.fft.ifft(heat*np.fft.fft(v)).real
    lapse=np.exp(.4*np.cos(xxn));acc=deriv(np.log(lapse))
    ellv=.8;th=.12;width=.08
    def ramp(z):
        rr=np.clip(z/width,0,1)
        mid=width*(7*rr**5-14*rr**6+10*rr**7-2.5*rr**8)
        return np.where(z<=0,0,np.where(z>=width,z-width/2,mid))
    def energy(u):
        w=filt(u);dw=deriv(w);lnw=deriv(lapse*dw)/lapse
        jj=(8/3)*np.abs(dw)**1.5
        return float(np.mean(lapse*(2*(deriv(u)-acc)**2+ramp(jj+ellv*lnw-th))))
    rng=np.random.default_rng(2609264)
    margins=[]
    for _ in range(64):
        def draw():
            coeff=rng.normal(size=(2,5))
            return sum((coeff[0,k-1]*np.cos(k*xxn)+coeff[1,k-1]*np.sin(k*xxn))/k**2 for k in range(1,6))
        u,v=draw(),draw();weight=float(rng.uniform(.1,.9))
        gap=weight*energy(u)+(1-weight)*energy(v)-energy(weight*u+(1-weight)*v)
        strong=2*weight*(1-weight)*float(np.mean(lapse*deriv(u-v)**2))
        assert gap>=strong-1e-11,(gap,strong)
        margins.append(gap-strong)
    # Homogeneous zero is inactive; an active zero of W' occurs at a minimum.
    amplitude=.5
    active_min_argument=ellv*amplitude-th
    inactive_max_argument=-ellv*amplitude-th
    assert active_min_argument>width and inactive_max_argument<0
    result={'checks':checks,'passed':True,'seed':2609264,
            'finite_Jensen_controls':{'pairs':64,'grid':nn,'xi':xi,'min_excess_above_strong_convexity':min(margins)},
            'zero_controls':{'homogeneous_argument':-th,'cosine_minimum_argument':active_min_argument,
                             'cosine_maximum_argument':inactive_max_argument},
            'ramp_curvature_upper':'35/(16 delta)',
            'software':{'python':sys.version,'sympy':s.__version__,'numpy':np.__version__},
            'non_claims':['No full metric-clock Hessian theorem','No validated empirical gate replacement',
                          'No exact off/on mask force: interface terms remain','No global continuum solution proof']}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_checks':len(checks),'finite_Jensen_pairs':64,'min_margin':min(margins),'passed':True}))


if __name__=='__main__':main()
