"""Angularly averaged resonance loss after a prescribed pole shift; fixed shell kinetic energy."""
import json,math,sys
from pathlib import Path
from scipy.integrate import quad
m=1e6;delta=2e-9;w=1e-12;hc=1.973269804e-7;c=299792458.;beta0=math.sqrt(delta/m)
sigpeak=2*math.pi/(2*m)**2*hc**2;pref=4*c*sigpeak/beta0
checks=[]
def test(n,x):checks.append({'name':n,'passed':bool(x)});assert x,n
# Couplings fixed; daughter width remains a function of scattering energy, not shifted pole position.
def integrate(center,running=True,tol=1e-9):
 lo=math.atan(-center/w);hi=math.atan((delta-center)/w)
 def fn(theta):
  eps=max(0.,center+w*math.tan(theta))
  phase=math.sqrt(eps/delta) if running else 1.
  a=pref*4/(4*math.tan(theta)**2+(1+phase)**2)
  return a*w/(math.cos(theta)**2)/delta
 return quad(fn,lo,hi,epsabs=1e-28,epsrel=tol,points=[0] if lo<0<hi else None,limit=300)[0]
base=integrate(delta);U=1.9208763923634617e-9;nwall=1e25
rows=[]
for center in [delta+2e-10,delta+2e-11,delta,delta-2e-11,delta/2,2e-11,0.,-2e-11,-2e-10]:
 val=integrate(center);ref=integrate(center,tol=1e-11)
 test('quadrature '+str(center),abs(val/ref-1)<1e-8)
 exact=pref*w/delta*(math.atan((delta-center)/w)-math.atan(-center/w))
 test('constant-width analytic '+str(center),abs(integrate(center,False)/exact-1)<1e-9)
 shift=(delta-center)/2
 rows.append({'new_resonance_excess_eV':center,'loss_coefficient_m3_s':val,'loss_ratio_to_original':val/base,'implied_carrier_Uinside_eV_if_mass_shift_control':shift,'required_ninside_m3_if_nonnegative':nwall*shift/U if shift>=0 else None,'remaining_wall_height_eV':U-shift,'K_1neV_below_remaining_wall':bool(delta/2<U-shift)})
test('ten-width downward shift does not suppress',rows[3]['loss_ratio_to_original']>1)
test('above continuum suppresses',rows[0]['loss_ratio_to_original']<.01)
test('below continuum suppresses',rows[-1]['loss_ratio_to_original']<.01)
# Wall must exceed K+Uinside; for crossing threshold Uinside>=delta/2=K.
minimum_wall=delta
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'rows':rows,'baseline_a_m3_s':base,'minimum_wall_height_for_threshold_crossing_eV':minimum_wall,'wall_density_factor_needed_at_threshold':minimum_wall/U,'scope':'Prescribed pole shifts and frozen isotropic monoenergetic gas; no dynamical controller or stable inventory.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
