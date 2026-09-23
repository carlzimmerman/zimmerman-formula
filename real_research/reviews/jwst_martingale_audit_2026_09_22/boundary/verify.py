"""Exact extrema audit plus finite check with the existing transport solver."""
import json
import runpy
from pathlib import Path
import numpy as np
import sympy as S

z,k=S.symbols('z k',real=True)
q=S.Rational
h=z*z/3-2*k*z/5
star=S.solve(S.diff(h,z),z)[0]
threshold_min=S.solve(star-1,k)[0]
threshold_max=S.solve(h.subs(z,1)-h.subs(z,0),k)[0]
hstar=S.factor(h.subs(z,star))
exact={
 'convex':S.diff(h,z,2)==q(2,3),
 'stationary_square':S.expand(h-hstar-(z-star)**2/3)==0,
 'minimum_threshold':threshold_min==q(5,3),
 'maximum_threshold':threshold_max==q(5,6),
 'k1_refutes_wrong_min':h.subs({k:1,z:q(3,5)})<h.subs({k:1,z:1}),
 'k2_refutes_max_one_third':max(h.subs({k:2,z:0}),h.subs({k:2,z:1}))==0,
 'vacuum_minus_sign':q(1,3)-h.subs({k:0,z:1})==0,
 'vacuum_plus_sign_fails':q(1,3)+h.subs({k:0,z:1})!=0,
}
fixtures=[]
for rate in [q(1,4),q(5,6),q(1),q(5,3),q(2),q(5)]:
    candidates=[S.Integer(0),S.Integer(1)]
    if 0<=star.subs(k,rate)<=1: candidates.append(star.subs(k,rate))
    lo=hstar.subs(k,rate) if rate<=threshold_min else h.subs({k:rate,z:1})
    hi=h.subs({k:rate,z:1}) if rate<=threshold_max else S.Integer(0)
    def predicate(shift,lower,upper):
        values=[h.subs({k:rate,z:point})+shift for point in candidates]
        return all(lower<=v<=upper for v in values) and lower in values and upper in values
    flags=[predicate(0,lo,hi),predicate(1,lo+1,hi+1),not predicate(0,lo+q(1,10),hi)]
    assert all(flags)
    fixtures.append({'k':str(rate),'minimum':str(lo),'maximum':str(hi),'main_positive_negative_rejection':flags})

simulate=runpy.run_path('real_research/reviews/bhstar_scattering_clock_2026_09_21/transport.py')['simulate']
def stats(x):
    avg=float(np.mean(x));se=float(np.std(x,ddof=1)/np.sqrt(len(x)))
    return {'mean':avg,'se':se,'z_score':avg/se if se else None}

rows=[]
for i,rate in enumerate([.25,1.,2.,5.]):
    n=120000;seed=9225100+i
    paths=simulate(n,rate,0.,0.,'central',seed)
    D=paths['delay'];Z=paths['time']-D
    hz=Z*Z/3-2*rate*Z/5
    p0=7*rate**2/20+1/3
    residual=stats(D*D+hz-p0)
    wrong_sign=stats(D*D-hz-p0)
    omitted=stats(D*D-p0)
    mean_check=stats(D-rate/2)
    lo_h=-3*rate**2/25 if rate<=5/3 else 1/3-2*rate/5
    hi_h=max(0.,1/3-2*rate/5)
    lower=1/3+rate**2/10-hi_h
    upper=1/3+rate**2/10-lo_h
    variance=float(np.var(D,ddof=1))
    variance_se=float(np.std((D-D.mean())**2,ddof=1)/np.sqrt(n))
    checks={
     'raw_second_identity_within_6se':abs(residual['z_score'])<6,
     'mean_identity_within_6se':abs(mean_check['z_score'])<6,
     'wrong_sign_rejected_over_6se':abs(wrong_sign['z_score'])>6,
     'omitted_boundary_rejected_over_6se':abs(omitted['z_score'])>6,
     'outgoing_geometry':bool(np.all((Z>=-1e-10)&(Z<=1+1e-10))),
     'bounds_with_sampling_tolerance':lower-6*variance_se<=variance<=upper+6*variance_se,
    }
    rows.append({'k':rate,'n':n,'seed':seed,'steps':paths['steps'],'raw_second_residual':residual,
     'wrong_sign_residual':wrong_sign,'omitted_boundary_residual':omitted,'mean_delay_residual':mean_check,
     'variance':variance,'variance_se_approx':variance_se,'lower':lower,'upper':upper,
     'mean_exit_projection':float(Z.mean()),'mean_exit_projection_squared':float(np.mean(Z*Z)),
     'checks':checks})

out={'scope':'Exact extrema plus finite Monte Carlo consistency; uses preexisting solver, no second transport implementation or novelty claim',
 'h':str(h),'stationary_point':str(star),'minimum_threshold':str(threshold_min),'maximum_threshold':str(threshold_max),
 'exact_checks':{key:bool(value) for key,value in exact.items()},'rational_fixtures':fixtures,'transport':rows}
Path('real_research/reviews/jwst_martingale_audit_2026_09_22/boundary/certified/result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert all(exact.values()) and all(all(row['checks'].values()) for row in rows)
