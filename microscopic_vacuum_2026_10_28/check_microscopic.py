"""Frozen MV28 spectrum experiment; write JSON to argv[1]."""
import json
import math
import sys
from pathlib import Path
import numpy as np
import scipy
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq

N=np.array([[0.,1.,0.],[1.,0.,0.],[0.,0.,0.]])

def symbolic():
    x,r,y=sp.symbols('x r y',positive=True)
    n=sp.Matrix([[0,1,0],[1,0,0],[0,0,0]])
    m=sp.Matrix([[0,x,1],[x,r,0],[1,0,0]])
    f=m*m;p=f+y*r*n;z=f-y*r*n
    a,c=sp.symbols('a c',real=True)
    grav=sp.exp(a+c*a*a/4)*((1+a+c*a*a/2)**2/(1+c*a)-3*a)
    expr={
      'fermion_determinant':m.det()+r,
      'positive_block_determinant':p.det()-r*r*(1-y*y-2*x*y),
      'negative_block_determinant':z.det()-r*r*(1-y*y+2*x*y),
      'supertrace_mass_squared':sp.trace(p)+sp.trace(z)-2*sp.trace(f),
      'supertrace_mass_fourth':sp.trace(p*p)+sp.trace(z*z)-2*sp.trace(f*f)-4*y*y*r*r,
      'canonical_gravity_no_quadratic_mass':sp.diff(grav.subs(c,0),a).subs(a,0),
      'canonical_gravity_quartic_coefficient':sp.diff(grav.subs(c,0),a,2).subs(a,0)-1,
      'Kahler_gravity_mass_response':sp.diff(grav,a).subs(a,0)+c,
    }
    us,uss=sp.symbols('us uss',positive=True)
    expr['pressure_response']=((uss-3*us)/3)/((sp.Rational(3,5))*(2+uss/us))-5*us*(uss-3*us)/(9*(2*us+uss))
    return {k:bool(sp.simplify(v)==0) for k,v in expr.items()}

def traces(A,Ap,App,Q=1.):
    eig,vec=np.linalg.eigh(A)
    if np.min(eig)<=0:raise ValueError('Nonpositive squared mass')
    logs=np.log(eig/(Q*Q))
    hp=2*eig*(logs-1)
    B=vec.T@Ap@vec
    C=vec.T@App@vec
    D=np.empty((3,3))
    for i in range(3):
        for j in range(3):
            lo=min(eig[i],eig[j]);hi=max(eig[i],eig[j]);t=(hi-lo)/lo
            if t<1e-5:
                correction=t/2-t*t/6+t**3/12-t**4/20
            else:correction=(1+t)/t*math.log1p(t)-1
            D[i,j]=2*(math.log(lo/(Q*Q))+correction)
    return (float(np.sum(eig*eig*(logs-1.5))),float(hp@np.diag(B)),
            float(hp@np.diag(C)+np.sum(D*B*B)),eig)

def cw(x,r,y,Q=1.):
    M=np.array([[0.,x,1.],[x,r,0.],[1.,0.,0.]])
    F=M@M;Ap=M@N+N@M;App=2*N@N;split=y*r*N
    p=traces(F+split,Ap,App,Q);z=traces(F-split,Ap,App,Q);f=traces(F,Ap,App,Q)
    norm=64*math.pi**2*y*y*r*r
    values=np.array([(p[i]+z[i]-2*f[i])/norm for i in range(3)])
    return (*values,float(min(np.min(p[3]),np.min(z[3]))))

def mp_cw(x,r,y):
    n=mp.matrix([[0,1,0],[1,0,0],[0,0,0]])
    m=mp.matrix([[0,x,1],[x,r,0],[1,0,0]]);f=m*m
    def h(A):
        vals=mp.eigsy(A,eigvals_only=True)
        return sum(t*t*(mp.log(t)-mp.mpf('1.5')) for t in vals)
    return (h(f+y*r*n)+h(f-y*r*n)-2*h(f))/(64*mp.pi**2*y*y*r*r)

def mp_second(x,r,y):
    with mp.workdps(65):
        x,r,y=map(lambda t:mp.mpf(str(t)),[x,r,y]);h=mp.mpf('0.0002')
        vals=[mp_cw(x+i*h,r,y) for i in [-2,-1,0,1,2]]
        return float((-vals[0]+16*vals[1]-30*vals[2]+16*vals[3]-vals[4])/(12*h*h))

def source_origin(r):
    return -(2*r*r*(r*r+3)*math.log(r)-(3*r**4-2*r*r-1))/(4*math.pi**2*(r*r-1)**3)

def portal(x,x0,r,y):
    c,cp,cpp,minmass=cw(x,r,y)
    us=x*cp;uss=x*x*cpp+x*cp;stiff=2*us+uss
    bulk=5*us*(uss-3*us)/(9*stiff)
    Khat_lambda2=x**3*cp/(2*x0*x0)
    return {'x':x,'U_s_over_f2_lambda2':us,'W_ss_over_f2_lambda2':stiff,
            'bulk_over_f2_lambda2':bulk,'K_over_f2_lambda2':Khat_lambda2,
            'minimum_transverse_mass2_over_m1_2':minmass}

def one_case(r,y):
    bound=(1-y*y)/(2*y)
    grid=np.linspace(1e-4,0.98*bound,121)
    slopes=[cw(x,r,y)[1] for x in grid]
    brackets=[(grid[i],grid[i+1]) for i in range(len(grid)-1) if slopes[i]<0<slopes[i+1]]
    out={'r':r,'y':y,'transverse_bound_x':bound,'found_radial_minimum':bool(brackets)}
    if not brackets:return out
    x0=brentq(lambda x:cw(x,r,y)[1],*brackets[0],xtol=2e-11,rtol=2e-12)
    c,cp,cpp,minmass=cw(x0,r,y)
    mpcpp=mp_second(x0,r,y)
    # Independently form the full six-real-scalar block and compare its spectrum.
    m=np.array([[0.,x0,1.],[x0,r,0.],[1.,0.,0.]])
    F=m@m;split=y*r*N
    full=np.block([[F,split],[split,F]])
    block_eig=np.sort(np.r_[np.linalg.eigvalsh(F+split),np.linalg.eigvalsh(F-split)])
    full_error=float(np.max(np.abs(np.linalg.eigvalsh(full)-block_eig)))
    scale_derivative_error=max(abs(cw(x0,r,y,2.)[i]-cw(x0,r,y,0.5)[i]) for i in [1,2])
    ratios=[]
    for lam in [0.3,0.6,1.]:
        ratios.append({'lambda':lam,'V_over_f2':1+lam*lam*c,
                       'B_curv_over_f2':lam*lam*x0*x0*cpp/9,
                       'B_curv_over_V_model':lam*lam*x0*x0*cpp/(9*(1+lam*lam*c))})
    tail=np.linspace(x0+1e-5,0.98*bound,101)
    hvals=[x*cw(x,r,y)[2]-2*cw(x,r,y)[1] for x in tail]
    intervals=[(tail[i],tail[i+1]) for i in range(len(tail)-1) if hvals[i]>0>hvals[i+1]]
    boundary=None
    if intervals:
        xb=brentq(lambda x:x*cw(x,r,y)[2]-2*cw(x,r,y)[1],*intervals[0],xtol=2e-10)
        boundary=portal(xb,x0,r,y)
        boundary['x_over_v']=xb/x0
    samples=[];fd_errors=[]
    for fraction in [0.1,0.3,0.5,0.8]:
        x=x0+fraction*(0.98*bound-x0)
        row=portal(x,x0,r,y)
        # Independent finite-difference pressure/density derivatives use c and c',
        # rather than the matrix Hessian used by the response formula.
        h=1e-4*max(1,x)
        def p_and_logrho(t):
            cv,grad,_,_=cw(t,r,y)
            return t*grad/3-cv,0.6*math.log(t**3*grad/(2*x0*x0))
        pp,ll=zip(*(p_and_logrho(x+i*h) for i in [-2,-1,1,2]))
        dp=(pp[0]-8*pp[1]+8*pp[2]-pp[3])/(12*h)
        dl=(ll[0]-8*ll[1]+8*ll[2]-ll[3])/(12*h)
        fd=dp/dl
        error=abs(fd-row['bulk_over_f2_lambda2'])/(1+abs(fd))
        row['finite_difference_bulk']=fd;row['bulk_scaled_error']=error
        samples.append(row);fd_errors.append(error)
    out.update({'x0':x0,'c0':c,'c_prime0':cp,'c_second0':cpp,'mp_c_second0':mpcpp,
                'curvature_relative_error':abs(cpp/mpcpp-1),'min_transverse_mass2':minmass,
                'full_block_eigenvalue_max_error':full_error,'Q_derivative_max_difference':scale_derivative_error,
                'ratios':ratios,'pressure_zero':boundary,'portal_samples':samples,
                'max_bulk_fd_scaled_error':max(fd_errors)})
    return out

def main(path):
    checks=symbolic();cases=[one_case(r,y) for r in [3.,4.,5.] for y in [0.05,0.1,0.2]]
    accepted=[c for c in cases if c['found_radial_minimum']]
    origins=[]
    for r in [1.5,2.5,4.,5.]:
        got=cw(0,r,0.01)[2];expected=source_origin(r)
        origins.append({'r':r,'y':0.01,'c_second0':got,'small_y_reference':expected,'relative_error':abs(got/expected-1)})
    benchmark=next(c for c in cases if c['r']==4 and c['y']==0.2)
    checks.update({
      'nine_requested_cases_recorded':len(cases)==9,
      'published_nonzero_minimum_benchmark':bool(benchmark['found_radial_minimum'] and abs(benchmark['x0']-1.3)<0.15),
      'high_precision_curvature_agrees':bool(accepted and max(c['curvature_relative_error'] for c in accepted)<2e-5),
      'full_six_scalar_spectrum_agrees':bool(accepted and max(c['full_block_eigenvalue_max_error'] for c in accepted)<1e-10),
      'renormalization_scale_derivatives_agree':bool(accepted and max(c['Q_derivative_max_difference'] for c in accepted)<1e-8),
      'four_small_y_origin_benchmarks':max(c['relative_error'] for c in origins)<0.003,
      'independent_pressure_response_derivative':bool(accepted and max(c['max_bulk_fd_scaled_error'] for c in accepted)<1e-6),
    })
    out={'claim_id':'MV28_SPECTRUM','checks':{k:bool(v) for k,v in checks.items()},'cases':cases,'origin_benchmarks':origins,
         'model_discriminators':{'radial_minima':len(accepted),'positive_transverse_spectra':sum(c['min_transverse_mass2']>0 for c in accepted),'compressibility_zero_before_cutoff':sum(c['pressure_zero'] is not None for c in accepted)},
         'software':{'Python':sys.version.split()[0],'NumPy':np.__version__,'SciPy':scipy.__version__,'SymPy':sp.__version__,'mpmath':mp.__version__},
         'non_claims':['No universal numerical B/V','No full supergravity loop computation','No cosmological vacuum matching','No derivation of the relative-only portal','No metastable lifetime or R-Goldstone dynamics']}
    Path(path).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'checks':out['checks'],'model_discriminators':out['model_discriminators'],'benchmark':{k:benchmark.get(k) for k in ['x0','c0','c_second0','ratios','pressure_zero']}},indent=2))
    assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
