#!/usr/bin/env python3
"""Bidirectional pressure/density/expansion reconstruction and kernel inversion.

Exact symbolic identities plus declared synthetic (not fitted) cosmologies.
Energy density epsilon and pressure p both use J/m^3; a is scale factor.
"""
import argparse,json,math
from pathlib import Path
import sympy as s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    a=s.symbols('a',positive=True)
    G,c,kappa,g=s.symbols('G_N c kappa g',positive=True)
    Pi0,D,M,Ck=s.symbols('Pi0 D M Ck',real=True)
    E=s.Function('epsilon')(a);Pi=s.Function('Pi')(a);A=s.Function('a0')(a);F=s.Function('F')(a)
    checks={}
    def exact(name,expr):
        v=s.factor(s.simplify(expr));assert v==0,(name,v);checks[name]={'passed':True,'residual':str(v)}
    # Continuity with p=-Pi: (a³ epsilon)'=3a² Pi.
    exact('continuity_integrating_factor',s.diff(a**3*E,a)-3*a*a*Pi-a*a*(a*s.diff(E,a)+3*(E-Pi)))
    Econst=Pi0+D/a**3
    exact('constant_pressure_inverse_family',a*s.diff(Econst,a)+3*(Econst-Pi0))
    exact('invisible_dust_kernel',a*s.diff(D/a**3,a)+3*D/a**3)
    w=-Pi0/Econst
    exact('constant_pressure_variable_w',a*s.diff(w,a)-3*w*(1+w))
    # Density promotion epsilon=a0²/(kappa² G_N), constant couplings.
    Ed=A*A/(kappa*kappa*G)
    wd=-1-s.Rational(2,3)*a*s.diff(A,a)/A
    exact('density_inverse_equation_of_state',a*s.diff(Ed,a)+3*(1+wd)*Ed)
    wp=s.Function('w')(a)
    Ep=-A*A/(kappa*kappa*G*wp)
    continuity=s.factor((a*s.diff(Ep,a)+3*(1+wp)*Ep)/Ep)
    exact('pressure_inverse_w_ODE',continuity-(2*a*s.diff(A,a)/A-a*s.diff(wp,a)/wp+3*(1+wp)))
    # FLRW effective stress: independent of how dark sector is split.
    gc=g*G;K=Ck/a**2
    Et=3*c*c*(F+K)/(8*s.pi*gc)
    Pt=-c*c*(a*s.diff(F,a)+3*F+K)/(8*s.pi*gc)
    exact('curved_FLRW_effective_continuity',a*s.diff(Et,a)+3*(Et+Pt))
    dust=M/a**3
    EX=Et-dust
    exact('subtract_conserved_ordinary_dust',a*s.diff(EX,a)+3*(EX+Pt))
    Q=a*s.diff(F,a)+3*F
    exact('pressure_dust_shift_invariance',(a*s.diff(F+D/a**3,a)+3*(F+D/a**3))-Q)
    # Flat p_ordinary=0 and pressure promotion: inverse expansion is first order.
    B=8*s.pi*g/(kappa*kappa*c*c)
    exact('pressure_to_expansion_ODE',kappa*kappa*G*(-Pt.subs(Ck,0))-kappa*kappa*c*c*Q/(8*s.pi*g))
    Fconst=B*Pi0/3+D/a**3 # Pi0 here denotes a constant a0² only in this local expression.
    exact('constant_a0_squared_expansion_family',a*s.diff(Fconst,a)+3*Fconst-B*Pi0)
    # Synthetic CPL history tests the two different promotions exactly.
    w0,wa,E0=s.symbols('w0 wa E0',real=True)
    wc=w0+wa*(1-a)
    ec=E0*a**(-3*(1+w0+wa))*s.exp(3*wa*(a-1))
    pic=-wc*ec
    exact('synthetic_CPL_continuity',a*s.diff(ec,a)+3*(1+wc)*ec)
    exact('synthetic_CPL_pressure_inverse',a*s.diff(pic,a)/pic-(a*s.diff(wc,a)/wc-3*(1+wc)))
    # Algebraic MOND laws, ONLY their isolated spherical unfiltered regime.
    r,go=s.symbols('r g_obs',positive=True)
    L=-s.log(1-r);gb=r*go
    arar=gb/L**2;aexp=go/L
    exact('RAR_inverse_exponential',s.exp(-L)-(1-r))
    exact('RAR_inverse_y',gb/arar-L*L)
    exact('AQUAL_inverse_x',go/aexp-L)
    exact('two_law_inverse_ratio',aexp/arar-L/r)
    # Differentiate with gbar held fixed; r=gbar/gobs, dr/dlngobs=-r.
    cond_rar=s.simplify((go*s.diff(arar,go)-r*s.diff(arar,r))/arar)
    cond_exp=s.simplify((go*s.diff(aexp,go)-r*s.diff(aexp,r))/aexp)
    exact('RAR_inverse_condition_number',cond_rar-2*r/((1-r)*L))
    exact('AQUAL_inverse_condition_number',cond_exp-1-r/((1-r)*L))
    exact('RAR_deep_limit_condition_number',s.limit(cond_rar,r,0)-2)
    exact('AQUAL_deep_limit_condition_number',s.limit(cond_exp,r,0)-2)
    # Test domain via independent forward calculations at varied acceleration.
    inverse_rows=[]
    for ratio in [1e-3,.03,.2,.7,.95,.999]:
        obs=1.7;bar=ratio*obs;ll=-math.log1p(-ratio)
        rr=bar/(ll*ll);ex=obs/ll
        rar_forward=bar/(-math.expm1(-math.sqrt(bar/rr)))
        exp_forward=obs*(-math.expm1(-obs/ex))
        assert abs(rar_forward/obs-1)<1e-12 and abs(exp_forward/bar-1)<1e-12
        inverse_rows.append({'gbar_over_gobs':ratio,'a0_RAR':rr,'a0_AQUAL':ex,
                             'RAR_log_condition_gobs':2*ratio/((1-ratio)*ll),
                             'AQUAL_log_condition_gobs':1+ratio/((1-ratio)*ll)})
    # Numerical synthetic history, not DESI/galaxy data or a fit.
    rows=[]
    for zz in [0,.5,1,2,3,5]:
        av=1/(1+zz);wv=-.8-.4*(1-av)
        ev=av**(.6)*math.exp(-1.2*(av-1))
        den=math.sqrt(ev);pres=math.sqrt((-wv/.8)*ev)
        qpress=(-wv/.8)*ev
        null=pres*pres/qpress
        density_as_pressure=den*den/qpress
        assert abs(null-1)<1e-12
        rows.append({'z':zz,'w':wv,'epsilon_ratio':ev,'a0_density_ratio':den,
                     'a0_pressure_ratio':pres,'pressure_null':null,
                     'wrong_density_as_pressure_null':density_as_pressure})
    assert abs(rows[-1]['wrong_density_as_pressure_null']-1)>.2
    out={'scope':'Exact conditional inversions; no data fit and no microscopic dark-energy identification',
         'checks':checks,'algebraic_kernel_inverse_controls':inverse_rows,
         'synthetic_CPL_parameters':{'w0':-.8,'wa':-.4,'label':'chosen illustration only'},
         'synthetic_history':rows,
         'pressure_null_test':'[a0(z)/a0(0)]² Q(0)/Q(z)=1, Q=3H²−(1+z)d(H²)/dz',
         'null_hypotheses':['Flat FLRW Einstein-form background with constant Gcosm/GN and kappa',
                            'Ordinary pressure negligible or separately subtracted',
                            'a0²=−kappa² GN p_X and Q>0',
                            'No assumption about pressureless dark-matter fraction'],
         'non_claims':['No physical stress identification from kinematic reconstruction alone',
                       'No galaxy-to-a0 inversion for arbitrary filtered/gated nonspherical configurations',
                       'No data calibration, selection or covariance analysis',
                       'No universal inversion of unknown gravitational field equations']}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'symbolic_checks':len(checks),'kernel_controls':len(inverse_rows),'synthetic_epochs':len(rows),'passed':True}))

if __name__=='__main__':main()
