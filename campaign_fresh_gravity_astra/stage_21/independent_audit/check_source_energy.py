from pathlib import Path
import json,sys
import mpmath as mp
XS=['0.1','0.01','0.001'];RS=['0.001','0.03','0.3','1'];ORIENT=['parallel_plus','parallel_minus','transverse']

def evaluate(dps):
 with mp.workdps(dps):
  roots=[];q_primitive=[];cache={};rows=[];zero=[]
  def source(t,law):
   if not t:return mp.mpf(0)
   return t*mp.sqrt(1+t*t) if law=='Q' else t*t/(-mp.expm1(-t))
  def constitutive(x,law):
   key=(law,x)
   if key in cache:return cache[key]
   if not x:
    result=(mp.mpf(0),mp.mpf(0),mp.mpf(0),mp.mpf(0));cache[key]=result;return result
   if law=='Q':
    y=2*x*x/(mp.sqrt(1+4*x*x)+1);t=mp.sqrt(y);lam=2*x/mp.sqrt(1+4*x*x)
   else:
    lo=mp.mpf(0);hi=x
    for _ in range(int(dps*3.5)+35):
     mid=(lo+hi)/2
     if source(mid,law)<x:lo=mid
     else:hi=mid
    t=(lo+hi)/2;y=t*t;v=-mp.expm1(-t)
    fx=(2*t*v-t*t*mp.exp(-t))/(v*v);lam=2*t/fx
   residual=abs(source(t,law)-x)/x;roots.append(residual)
   assert residual<mp.mpf(10)**(-dps+10)
   # Independent energy integration in source coordinate, not inverse-gradient variable.
   w=x*y-mp.quad(lambda s:2*s*source(s,law),[0,t])
   assert w>0 and lam>0
   if law=='Q':
    exact=x*mp.sqrt(1+4*x*x)/4+mp.asinh(2*x)/8-x/2
    discrepancy=abs(w-exact)/w;q_primitive.append(discrepancy)
    assert discrepancy<mp.mpf(10)**(-dps+15)
   result=(w,y,lam,y/x);cache[key]=result;return result
  enc=lambda z:mp.nstr(z,dps)
  for law in ['Q','RAR']:
   for xs in XS:
    x=mp.mpf(xs);w,y,lam,mu=constitutive(x,law)
    zero.append({'law':law,'amplitude':xs,'cubic_ratio_3w_over_h3':enc(3*w/x**3),'zero_background_stiffness':0})
    for rs in RS:
     r=mp.mpf(rs);h=r*x
     for orient in ORIENT:
      hp=h if orient=='parallel_plus' else -h if orient=='parallel_minus' else mp.mpf(0)
      new=abs(x+hp) if orient!='transverse' else mp.sqrt(x*x+h*h)
      wn=constitutive(new,law)[0];D=wn-w-y*hp
      H=(lam if orient!='transverse' else mu)*h*h/2
      rem=D-H;rel=rem/H
      assert D>0 and H>0
      assert (rel<0 if orient=='parallel_minus' else rel>0)
      if orient=='parallel_minus':
       wrong=wn-w-y*h;assert wrong<0
       if rs=='1':assert new==0 and wn==0
      deep=r/3 if orient=='parallel_plus' else -r/3 if orient=='parallel_minus' else 2*((1+r*r)**mp.mpf('1.5')-1)/(3*r*r)-1
      rows.append({'law':law,'x':xs,'ratio':rs,'orientation':orient,'increment':enc(D),'quadratic':enc(H),'remainder':enc(rem),'relative_remainder':enc(rel),'deep_relative_remainder':enc(deep),'lambda_parallel':enc(lam),'lambda_transverse':enc(mu),'speed_squared_parallel_over_c2_K2':enc(lam/2),'speed_squared_transverse_over_c2_K2':enc(mu/2)})
  assert len(rows)==72 and len(zero)==6
  for law in ['Q','RAR']:
   z=[mp.mpf(v['cubic_ratio_3w_over_h3']) for v in zero if v['law']==law]
   assert 0<z[0]<z[1]<z[2]<1
  return {'dps':dps,'rows':rows,'zero_background':zero,'max_inverse_relative_residual':enc(max(roots)),'max_Q_primitive_relative_discrepancy':enc(max(q_primitive))}
low=evaluate(80);high=evaluate(110)
with mp.workdps(110):
 differences={key:mp.mpf(0) for key in ['increment','quadratic','remainder','relative_remainder']}
 for a,b in zip(low['rows'],high['rows']):
  assert all(a[k]==b[k] for k in ['law','x','ratio','orientation'])
  for k in differences:
   discrepancy=abs(mp.mpf(a[k])-mp.mpf(b[k]))/abs(mp.mpf(b[k]));differences[k]=max(differences[k],discrepancy)
 assert all(v<mp.mpf('1e-55') for v in differences.values())
 summary=[]
 for law in ['Q','RAR']:
  for r in RS:
   chosen=[row for row in high['rows'] if row['law']==law and row['ratio']==r]
   summary.append({'law':law,'ratio':r,'max_abs_relative_remainder':float(max(abs(mp.mpf(v['relative_remainder'])) for v in chosen))})
 result={'status':'passed','source_representation':'w=x*t^2-integral_0^t 2s*f(s^2) ds','arithmetic':'mpmath arbitrary precision, not rigorous interval arithmetic','cases_per_law':36,'cases_total':72,'orientations':ORIENT,'relative_precision_tolerance':'1e-55','max_relative_precision_discrepancies':{k:mp.nstr(v,25) for k,v in differences.items()},'low_precision':low,'high_precision':high,'finite_summary':summary,'controls':{'positive_convex_increment_and_Hessian':True,'signed_parallel_linear_subtraction':True,'anti_parallel_ratio1_exact_zero_final_gradient':True,'RAR_monotone_source_bracket':True,'Q_analytic_primitive':True,'zero_background_cubic_approach_on_three_amplitudes':True,'precision_crosscheck':True},'raw_limit_statement':'Both raw iterated increments and raw remainders approach zero; only normalized approximation is nonuniform','restoration':{'W':'a^2 w','field_energy_density':'a^2 w/(4piG)','gradient':'a x','a0_values_m_s2':['9.3619e-11','1.1279e-10'],'K':2},'limits':['finite high-precision checks, not interval certification','no nonlinear PDE wellposedness/instability or ghost conclusion','no physical metric, empirical error or mass inference']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'passed','cases_total':72,'max_relative_precision_discrepancies':result['max_relative_precision_discrepancies'],'finite_summary':summary},indent=2))
