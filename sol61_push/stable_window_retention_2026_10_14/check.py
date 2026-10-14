"""Finite spherical-shell poles for two conditional miscible parameter candidates."""
import json,math,sys
from pathlib import Path
import mpmath as mp
prior=json.loads(Path('sol61_push/neutral_stable_window_2026_10_14/run/results.json').read_text())
hc=mp.mpf('1.973269804e-7');hb=mp.mpf('6.582119569e-16');mp.mp.dps=90
checks=[]
def ck(name,e,t):
 assert e<t,(name,e,t)
 checks.append(dict(name=name,error=float(e),tolerance=t))
def calc(row,a,d,precision):
 with mp.workdps(precision):
  hc=mp.mpf('1.973269804e-7');hb=mp.mpf('6.582119569e-16');a=mp.mpf(str(a));d=mp.mpf(str(d));U=mp.mpf(str(row['scaled_barrier_eV']));an=a/hc
  z0=an*mp.sqrt(2*U)
  eqinf=lambda z:z/mp.tan(z)+mp.sqrt(z0*z0-z*z)
  root=mp.findroot(eqinf,(mp.pi/2+mp.mpf('1e-30'),min(z0,mp.pi)-mp.mpf('1e-30')),solver='bisect',tol=mp.mpf('1e-70'),maxsteps=300)
  def eq(z):
   q=mp.sqrt(z0*z0-z*z);th=mp.tanh(q*d/a)
   return z/mp.tan(z)-(1j*z-q*th)/(1-1j*z*th/q)
  # Continue outwards from the infinitely thick reference for this width.
  zz=mp.findroot(eq,(root-1j*mp.mpf('1e-8'),root-1j*mp.mpf('2e-8')),tol=mp.mpf('1e-65'),maxsteps=100)
  E=zz*zz/(2*an*an);width=-2*mp.im(E)
  assert width>0
  q=mp.sqrt(z0*z0-zz*zz);ua=mp.sin(zz);up=zz*mp.cos(zz)
  ub=ua*mp.cosh(q*d/a)+up/q*mp.sinh(q*d/a);upb=q*ua*mp.sinh(q*d/a)+up*mp.cosh(q*d/a)
  boundary=abs(upb-1j*zz*ub)/max(abs(ub),abs(upb))
  # Independent outgoing boundary propagated by a transfer matrix.
  ck('pole_equation_'+str(a)+'_'+str(d)+'_'+str(precision),abs(eq(zz)),1e-50)
  ck('transfer_boundary_'+str(a)+'_'+str(d)+'_'+str(precision),boundary,1e-35)
  return dict(radius_m=float(a),thickness_m=float(d),barrier_eV=float(U),energy_eV=float(mp.re(E)),width_eV=float(width),lifetime_s=float(hb/width),reference_energy_eV=float(root*root/(2*an*an)),subbarrier=bool(mp.re(E)<U),barrier_decay_exponent=float(mp.sqrt(z0*z0-root*root)*d/a),relative_real_energy_shift=float(abs(mp.re(E)/(root*root/(2*an*an))-1)))
rows=[]
for candidate,index,a,ds in [('near_resonant_large',0,.2,[.1,.5,1.,2.]),('detuned_small',2,.02,[.01,.1,.3,.5])]:
 ref=prior['rows'][index]
 series=[]
 for d in ds:
  r=calc(ref,a,d,90);r['candidate']=candidate;r['mu_eV']=ref['selected_mu_eV'];r['detuning_eV']=ref['detuning_eV'];series.append(r)
 # Precision confirmation on longest-lived row.
 rr=calc(ref,a,ds[-1],110)
 ck('precision_refinement_'+candidate,abs(rr['width_eV']/series[-1]['width_eV']-1),1e-12)
 assert all(series[i+1]['lifetime_s']>series[i]['lifetime_s'] for i in range(len(series)-1))
 rows.extend(series)
result=dict(scope='Outgoing l=0 finite-shell resonances using assigned Coulomb-only barriers; tunneling only, not total retention or preparation success',rows=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
