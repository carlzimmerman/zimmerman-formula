import json,sys,resource
from pathlib import Path
import sympy as S
import mpmath as mp
from pressure_scan import cw,masses,deriv

def exact():
    X,h,lam,g,f=S.symbols('X h lam g f',positive=True);a,b,c=S.symbols('a b c',positive=True)
    s2=0;s4=0
    for r,mult in [(S.Rational(2),8),(S.Rational(-3),3),(S.Rational(-1,2),12)]:
        m=(1+r)*h*X;q=r*lam*a;split=(1+r)*c
        H1=S.Matrix([[m*m+q*q+split,-m*q],[-m*q,q*q]])
        H2=S.Matrix([[m*m+q*q-split,m*q],[m*q,q*q]])
        if r==S.Rational(-1,2):
            v=S.Matrix([5*g*a,-5*g*b]);H1+=v*v.T
            MF=S.Matrix([[m,q,5*g*a],[q,0,5*g*b],[5*g*a,5*g*b,0]])
            mv2=25*g*g*(a*a+b*b)
        else:MF=S.Matrix([[m,q],[q,0]]);mv2=0
        s2+=mult*(S.trace(H1)+S.trace(H2)-2*S.trace(MF**2)+3*mv2)
        s4+=mult*(S.trace(H1**2)+S.trace(H2**2)-2*S.trace(MF**4)+3*mv2**2)
    sub={a:S.sqrt(2*f*h/(30*h*h+lam*lam)),b:h*X/lam,c:lam*lam*f*h/(30*h*h+lam*lam)}
    val=S.factor(s4.subs(sub));target=6*f*f*h*h*lam*lam*(29*lam*lam-200*g*g)/(30*h*h+lam*lam)**2
    return {'STrM2_zero':S.simplify(s2.subs(sub))==0,
            'STrM4_formula_identity':S.simplify(val-target)==0,'STrM4':str(val),
            'STrM4_X_derivative_zero':S.simplify(S.diff(val,X))==0}

def bisect(fun,lo,hi):
    lo,hi=map(mp.mpf,(lo,hi));fl=fun(lo)
    for _ in range(90):
        mid=mp.sqrt(lo*hi);fm=fun(mid)
        if fl*fm>0:lo=mid;fl=fm
        else:hi=mid
    return mp.sqrt(lo*hi)

def main(path,prior):
    mp.mp.dps=60;h=lam=mp.mpf('.6');g=mp.sqrt(mp.mpf(29)/200)*lam
    def du(x,n=1):return mp.diff(lambda t:cw(x*mp.exp(t),h,lam,g),mp.mpf(0),n)
    xmin=bisect(lambda x:du(x),mp.mpf('1.6'),mp.mpf('1.8'))
    xp=bisect(lambda x:du(x,2)-3*du(x),mp.mpf('1.9'),mp.mpf('2.1'))
    xr=bisect(lambda x:du(x,2)+2*du(x),mp.mpf('2.1'),mp.mpf('4'))
    prior=json.loads(Path(prior).read_text());ref=next(v for v in prior['summaries'] if v['h']==.6 and v['lambda']==.6)
    shape=[];gap=[];errors=[]
    for ratio in map(mp.mpf,('1.05','1.12','1.2','1.3','1.5')):
        x=xmin*ratio;d=du(x);dd=du(x,2);wss=2*d+dd
        dfd,ddfd=deriv(x,h,lam,g,mp.mpf('.0025'));errors.append(max(abs(d-dfd),abs(dd-ddfd)))
        physical=[v for name,mult,es,ef,ev in masses(x,h,lam,g) for v in es if v>mp.mpf('1e-35')]
        physical.extend([2*h]*4);min_gap=min(physical)
        T2=(30*h*h+lam*lam)*x*x/(lam*lam)
        radial=wss/(2*T2)
        def density(t):
            xx=x*mp.exp(t);us=du(xx)
            return (us*mp.exp(2*t)/2)**(mp.mpf(3)/5)
        def pressure(t):
            xx=x*mp.exp(t);return du(xx)/3-lam*lam/(lam*lam+30*h*h)-cw(xx,h,lam,g)
        direct=mp.diff(pressure,0)/mp.diff(lambda t:mp.log(density(t)),0)
        expected=5*d*(dd-3*d)/(9*(2*d+dd))
        gap.append({'X_over_min':float(ratio),'X':float(x),'U_s':float(d),'U_ss':float(dd),'Wss':float(wss),
                    'tree_transverse_min_positive_m2':float(min_gap),'canonical_radial_m2':float(radial),
                    'abs_radial_m2_over_transverse_gap':float(abs(radial/min_gap)),
                    'dP_dlnrho_direct':float(direct),'dP_dlnrho_formula':float(expected),
                    'pressure_identity_abs_error':float(abs(direct-expected))})
    z0=h*xmin/mp.sqrt(h*lam*lam/(30*h*h+lam*lam))
    universal=cw(xmin,h,lam,g)/(h*lam*lam/(30*h*h+lam*lam))**2
    for hh,ll in [('.3','1'),('1','.3'),('.6','.6')]:
        H,L=map(mp.mpf,(hh,ll));G=mp.sqrt(mp.mpf(29)/200)*L;c=H*L*L/(30*H*H+L*L);x=z0*mp.sqrt(c)/H
        shape.append({'h':hh,'lambda':ll,'z_min':str(z0),'CW_over_c2':str(cw(x,H,L,G)/c**2),
                      'universal_shape_abs_difference':str(abs(cw(x,H,L,G)/c**2-universal))})
    loop=[]
    for vv in map(mp.mpf,('.03','.1','.3','.6','1')):
        hh=ll=vv;gg=mp.sqrt(mp.mpf(29)/200)*ll;cc=hh*ll*ll/(30*hh*hh+ll*ll);xx=z0*mp.sqrt(cc)/hh
        one=mp.diff(lambda t:cw(xx*mp.exp(t),hh,ll,gg),0,2)
        tree=ll*ll/(ll*ll+30*hh*hh)
        oldratio=mp.mpf(29)/(12*(16*mp.pi**2)**2)*hh*hh*ll*ll*(16*hh*hh+13*ll*ll)/(ll*ll+30*hh*hh)
        oldcurv=9*tree*oldratio
        loop.append({'h_equals_lambda':float(vv),'one_loop_threshold_Uss':float(one),
                     'old_leading_log_two_loop_Uss':float(oldcurv),'two_loop_LL_over_one_loop_threshold':float(oldcurv/one)})
    exact_checks=exact();checks={k:v for k,v in exact_checks.items() if isinstance(v,bool)}
    checks.update(positive_source_samples=all(r['U_s']>0 for r in gap),
                  direct_pressure_identity=max(r['pressure_identity_abs_error'] for r in gap)<1e-40,
                  independent_derivative_abs_difference=max(errors)<mp.mpf('1e-12'),
                  universal_shape_three_controls=max(mp.mpf(r['universal_shape_abs_difference']) for r in shape)<mp.mpf('1e-40'),
                  positive_transverse_gaps=all(r['tree_transverse_min_positive_m2']>0 for r in gap))
    out={'claim_id':'TP01_EXACT_GAP','checks':checks,'exact_supertraces':exact_checks,
         'direct_derivative_roots':{'X_min':str(xmin),'X_pressure':str(xp),'pressure_X_over_min':str(xp/xmin),
                                    'X_radial_end':str(xr),'radial_X_over_min':str(xr/xmin),
                                    'scan_min_relative_difference':str(abs(xmin/mp.mpf(ref['minima'][0]['X'])-1)),
                                    'scan_pressure_relative_difference':str(abs(xp/mp.mpf(ref['pressure_boundaries'][0]['X'])-1))},
         'universal_shape':shape,'gap_and_pressure':gap,'omitted_order_diagnostic':loop,
         'max_independent_derivative_abs_difference':str(max(errors)),
         'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'non_claims':['Tree transverse gaps do not establish quantum transverse positivity','Massless R phase/gauginos/Goldstino are retained, not integrated out',
                       'The comparison of orders is a diagnostic, not a controlled error bound or RG-resummed prediction']}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
