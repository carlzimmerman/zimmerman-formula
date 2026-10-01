import json,sys
from pathlib import Path
from functools import lru_cache
import mpmath as mp
BASE=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-007/fgf007_run_001')
OUT=BASE/'numeric_001/results.json'
XS=['.1','.01','.001']; RS=['.001','.03','.3','1']; LAWS=['Q','RAR']

def evaluate(digits):
 mp.mp.dps=digits
 tol=mp.mpf('1e-40'); invtol=mp.mpf('1e-45')
 checks={'inverse':mp.mpf(0),'primitive_agreement':mp.mpf(0),'Q_primitive':mp.mpf(0)}
 def f(t): return t*t/(-mp.expm1(-t)) if t else mp.mpf(0)
 def fp(t):
  if not t:return mp.mpf(1)
  d=-mp.expm1(-t)
  return t*(2*d-t*mp.exp(-t))/(d*d)
 @lru_cache(None)
 def inv(x):
  if not x:return mp.mpf(0)
  lo=mp.mpf(0); hi=x
  while hi-lo>mp.power(10,-digits+8)*x:
   mid=(hi+lo)/2
   if f(mid)<x:lo=mid
   else:hi=mid
  t=(hi+lo)/2
  err=abs(f(t)/x-1); checks['inverse']=max(checks['inverse'],err)
  assert err<invtol
  return t
 def bq(x):return 2*x*x/(mp.sqrt(1+4*x*x)+1)
 def bqp(x):return 2*x/mp.sqrt(1+4*x*x)
 def rp(t):
  d=-mp.expm1(-t)
  return 2*d*d/(2*d-t*mp.exp(-t)) if t else mp.mpf(0)
 @lru_cache(None)
 def primitive(law,x):
  if law=='Q':return x*mp.sqrt(1+4*x*x)/4+mp.asinh(2*x)/8-x/2
  t=inv(x)
  return mp.quad(lambda s:s*s*fp(s),[0,t])
 rows=[]; backgrounds=[]; zero=[]
 for law in LAWS:
  for sx in XS:
   x=mp.mpf(sx); t0=inv(x) if law=='RAR' else None
   b=bq(x) if law=='Q' else t0*t0
   bp=bqp(x) if law=='Q' else rp(t0)
   bpp=mp.diff(bqp,x) if law=='Q' else mp.diff(rp,t0)/fp(t0)
   if law=='Q':
    assert abs((b*b+b)/(x*x)-1)<tol
    wp=primitive(law,x); qi=mp.quad(bq,[0,x])
    checks['Q_primitive']=max(checks['Q_primitive'],abs(wp/qi-1))
    assert abs(wp/qi-1)<tol
   backgrounds.append({'law':law,'x':x,'b':b,'b_prime':bp,'lambda_perp':b/x,'speed_parallel_squared_over_c_squared':bp/2,'speed_transverse_squared_over_c_squared':b/(2*x),'parallel_r_coefficient':x*bpp/(3*bp),'transverse_r_squared_coefficient':(x*bp/b-1)/4})
   assert 0<bp/2<=1 and 0<b/(2*x)<=1
   zero.append({'law':law,'absolute_amplitude_over_a':x,'zero_background_exact_w':primitive(law,x),'leading_cubic':x**3/3,'exact_over_leading_cubic':primitive(law,x)/(x**3/3),'zero_background_hessian':mp.mpf(0)})
   for sr in RS:
    r=mp.mpf(sr); h=r*x
    for orient in ['parallel_plus','parallel_minus','transverse']:
     sign=1 if orient=='parallel_plus' else -1
     y=mp.sqrt(x*x+h*h) if orient=='transverse' else x+sign*h
     H=b*h*h/(2*x) if orient=='transverse' else bp*h*h/2
     if law=='RAR':
      t1=inv(y)
      if orient=='transverse':delta=mp.quad(lambda s:s*s*fp(s),[t0,t1])
      else:delta=mp.quad(lambda s:(s*s-t0*t0)*fp(s),[t0,t1])
     else:
      if orient=='transverse':delta=mp.quad(bq,[x,y])
      else:delta=mp.quad(lambda v:bq(v)-b,[x,y])
     alt=primitive(law,y)-primitive(law,x)-(sign*b*h if orient!='transverse' else 0)
     err=abs(alt/delta-1);checks['primitive_agreement']=max(checks['primitive_agreement'],err)
     assert err<tol and delta>0 and H>0
     deep=(2*((1+r*r)**mp.mpf('1.5')-1)/(3*r*r)) if orient=='transverse' else (1+sign*r/3)
     ratios=delta/H
     dimensional=[]
     for sa in ['9.3619e-11','1.1279e-10']:
      a=mp.mpf(sa)
      dimensional.append({'a_m_per_s_squared':a,'g0_m_per_s_squared':a*x,'amplitude_m_per_s_squared':a*h,'delta_W_m_squared_per_s_fourth':a*a*delta,'hessian_W_m_squared_per_s_fourth':a*a*H,'energy_density_rule':'Divide W by 4*pi*G; no G numeric value assumed.'})
     rows.append({'law':law,'x':x,'amplitude_ratio':r,'orientation':orient,'exact_increment':delta,'hessian_increment':H,'exact_over_hessian':ratios,'signed_relative_difference_to_hessian':ratios-1,'hessian_relative_error_to_exact':abs(H/delta-1),'deep_limit_exact_over_hessian':deep,'primitive_relative_agreement':err,'dimensional':dimensional})
 assert len(rows)==72
 return rows,backgrounds,zero,checks

low,_,_,lc=evaluate(60)
high,backgrounds,zero,hc=evaluate(90)
maxrel=mp.mpf(0)
for a,b in zip(low,high):
 assert (a['law'],a['orientation'])==(b['law'],b['orientation'])
 for key in ['exact_increment','hessian_increment','exact_over_hessian']:
  maxrel=max(maxrel,abs(a[key]/b[key]-1))
assert maxrel<mp.mpf('1e-40')
def encode(obj):
 if isinstance(obj,mp.mpf):return mp.nstr(obj,55)
 if isinstance(obj,list):return [encode(x) for x in obj]
 if isinstance(obj,dict):return {k:encode(v) for k,v in obj.items()}
 return obj
summary=[]
for sr in RS:
 subset=[r for r in high if r['amplitude_ratio']==mp.mpf(sr)]
 summary.append({'amplitude_ratio':sr,'max_abs_delta_over_hessian_minus_one':max(abs(r['signed_relative_difference_to_hessian']) for r in subset),'max_hessian_relative_error_to_exact':max(r['hessian_relative_error_to_exact'] for r in subset)})
result={'domain':{'background_ratios':XS,'amplitude_ratios':RS,'laws':LAWS,'orientations':['parallel_plus','parallel_minus','transverse'],'rows':72,'precisions_decimal_digits':[60,90],'K':2,'randomness':False},'rows':high,'background_coefficients':backgrounds,'zero_background_controls':zero,'summary':summary,'checks':{'low_precision':lc,'high_precision':hc,'max_60_90_relative_difference':maxrel,'all_assertions_passed':True},'limits':['High-precision floating quadrature/inversion, not rigorous interval certification.','No finite result establishes PDE well-posedness, ghost, global or physical-metric stability.','Zero-field leading cubic law and limiting statements have separate analytic derivations.','Relative-error denominators are explicit; both raw iterated energy limits vanish.']}
OUT.write_text(json.dumps(encode(result),indent=2)+'\n')
print(json.dumps(encode({'rows':72,'summary':summary,'checks':result['checks']}),indent=2))
