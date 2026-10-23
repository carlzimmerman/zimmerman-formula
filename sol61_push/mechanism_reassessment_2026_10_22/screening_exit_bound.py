"""Energy-based obstruction to indefinite passive Phi screening of X.

This is a conditional stability bound, not a conversion or relic simulator.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.special import gamma
from scipy.optimize import brentq
p=Path(__file__).parent
source=json.loads((p/'coupled_fragmentation_96_run/results.json').read_text())['source']
q,v=np.fromfile(p/'coupled_fragmentation_96_run/fine96_final.bin').reshape(2,4,96,96,96)
dx=32/96
Ephi=.5*np.mean(np.sum(v[:2]**2,axis=0))+.25*np.mean(np.sum(q[:2]**2,axis=0)**2)
Ephi+=sum(.5*np.mean(np.sum((np.roll(q[:2],-1,axis=ax)-q[:2])**2,axis=0))/dx**2 for ax in [1,2,3])
H=source['H_GeV'];lam=.00881292;m=.001;g=2.168e-6;M=2*m*np.sqrt(1+.02**2)
F=H*source['conformal_scale_over_H'];A0=H*np.linalg.norm(source['background_over_H'][2:])/np.sqrt(2)
aX=np.sqrt(H/M)
# Exact free homogeneous radiation solution approaches amplitude
# B A0 (aX/a)^(3/2), with B^2=8 Gamma(5/4)^2/pi.
B=np.sqrt(8*gamma(1.25)**2/np.pi)
Cphi=lam*F**4*Ephi
screen=6*np.sqrt(lam*Cphi)
pump=2*g*B*A0*aX**1.5
def polynomial(a):return pump*np.sqrt(a)-m*m*a*a-screen
atop=(pump/(4*m*m))**(2/3)
lower=brentq(lambda z:polynomial(np.exp(z)),np.log(aX),np.log(atop))
upper=brentq(lambda z:polynomial(np.exp(z)),np.log(atop),np.log((pump/(m*m))**(2/3)*1.01))
lower,upper=np.exp(lower),np.exp(upper)
aprobe=2*lower
gap=pump/aprobe**1.5-m*m-screen/aprobe**2
ratio=(m*m+screen/aprobe**2)/(pump/aprobe**1.5)
Gamma=g*g/(8*np.pi*M)*np.sqrt(1-4*m*m/M**2)
gst=106.75;Mpl=2.435e18
checks=dict(root_residual=max(abs(polynomial(a))/screen for a in [lower,upper])<1e-6,
 negative_curvature_window=gap>0,late_free_envelope=lower/aX>100,
 stored_energy_positive=Ephi>0)
checks={k:bool(v) for k,v in checks.items()}
out=dict(checks=checks,all_pass=all(checks.values()),
 Phi_conformal_energy_dimensionless=float(Ephi),radiation_energy_constant_GeV4=float(Cphi),
 free_X_envelope_factor=float(B),
 negative_Rayleigh_bound_window_a=[float(lower),float(upper)],
 first_crossing_H_GeV=float(H/lower**2),
 first_crossing_visible_T_GeV=float((90/(np.pi**2*gst))**.25*np.sqrt(Mpl*H)/lower),
 vacuum_Gamma_over_H_at_first_crossing=float(Gamma*lower**2/H),
 probe=dict(a=float(aprobe),X_envelope_GeV=float(B*A0*(aX/aprobe)**1.5),
   negative_curvature_scale_GeV=float(np.sqrt(gap)),scale_over_m=float(np.sqrt(gap)/m),
   scale_over_X_frequency=float(np.sqrt(gap)/M),
   fraction_cycle_with_negative_upper_bound_either_direction=float(2*np.arccos(ratio)/np.pi)),
 scope='If Phi positive energy stays below Cphi/a^4 and a homogeneous radial X reservoir follows its free radiation-era envelope, some instantaneous Hessian eigenvalue must become negative in this window. Earlier energy exchange or departure from the assumed X motion invalidates that continuation rather than providing a final yield. No Floquet growth or nonlinear conversion efficiency is inferred.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
sys.exit(0 if out['all_pass'] else 1)
