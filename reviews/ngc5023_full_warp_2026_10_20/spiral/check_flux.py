#!/usr/bin/env python3
"""Check digitized arm normalization against quoted component masses."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import erf

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
out=Path(args.output);out.mkdir(exist_ok=True)
here=Path(__file__).resolve().parent
p=json.loads((here/'run002/profiles.json').read_text());nodes=np.array(p['radii_arcsec'])
answer={'source':'Figure11 digitization and Table4 nominal masses atpaper6.6Mpc',
 'meaning':'Finite normalization benchmark, not a distance or HI mass inference',
 'formula':'F=integral A(R)*sqrt(2pi)*w(R)*erf(pi*R/(sqrt(2)*w(R)))dR, minimalwrappedGaussian overa fullring',
 'arms':{},'angular_integral_checks':[]}
for name in ['arm1','arm2']:
 a=p[name];am=np.array(a['amplitude_Jy_km_s_arcsec2']);ww=np.array(a['width_arcsec'])
 def f(r,wedge=False):
  aa=np.interp(r,nodes,am);w=np.interp(r,nodes,ww)
  angle=np.pi/4 if wedge else np.pi
  return aa*np.sqrt(2*np.pi)*w*erf(angle*r/(np.sqrt(2)*w))
 exact=sum(quad(f,l,h,epsabs=1e-11,epsrel=1e-10)[0] for l,h in zip(nodes[:-1],nodes[1:]))
 wedge=sum(quad(lambda r:f(r,True),l,h,epsabs=1e-11,epsrel=1e-10)[0] for l,h in zip(nodes[:-1],nodes[1:]))
 grid=np.linspace(0,360,20001);trap=np.trapz(f(grid),grid)
 mass=exact*2.356e5*6.6**2
 answer['arms'][name]={'fullring_flux_Jy_km_s':exact,'finegrid_trapezoid_flux':float(trap),
   'fractional_quadrature_difference':float(abs(trap/exact-1)),
   'mass_Msun_at_paper_6_6Mpc':mass,'quoted_mass_Msun':a['mass_Msun'],
   'mass_fractional_difference':mass/a['mass_Msun']-1,
   'centered_90degree_wedge_flux_diagnostic':wedge,
   'wedge_fractional_reduction':1-wedge/exact,
   'not_a_recovered_AZ_width':'Wedge entry only quantifies an unspecified structural alternative.'}
for radius,width in [(1,13),(20,14),(100,24),(240,37),(360,46)]:
 q=quad(lambda phi:np.exp(-.5*(radius*phi/width)**2)*radius,-np.pi,np.pi,epsabs=1e-10)[0]
 form=np.sqrt(2*np.pi)*width*erf(np.pi*radius/(np.sqrt(2)*width))
 answer['angular_integral_checks'].append({'radius_arcsec':radius,'width_arcsec':width,
       'direct_angular':q,'analytic_arc':float(form),'relative_error':float(abs(q/form-1))})
assert all(v['fractional_quadrature_difference']<1e-6 for v in answer['arms'].values())
assert all(abs(v['mass_fractional_difference'])<.02 for v in answer['arms'].values())
assert max(v['relative_error'] for v in answer['angular_integral_checks'])<1e-9
answer['all_checks_passed']=True
(out/'checks.json').write_text(json.dumps(answer,indent=2)+'\n')
print(json.dumps(answer,indent=2))
