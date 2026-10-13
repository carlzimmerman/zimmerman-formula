"""Weak-source force from the nodal-ring static kernel; dimensionless checks."""
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import quad
from scipy.special import dawsn
P=Path(__file__).parent
checks={}; rows=[]
# v_r=v_z=1; source wavevector angle to ring axis.
angles=[]
for angle in [0.,math.pi/6,math.pi/3,math.pi/2]:
    factor=quad(lambda t:math.sqrt(math.cos(angle)**2+math.sin(angle)**2*math.cos(t)**2),0,2*math.pi,epsabs=1e-11)[0]/(2*math.pi)
    angles.append(dict(angle=angle,kernel_factor=factor))
checks['axis_factor']=abs(angles[0]['kernel_factor']-1)<1e-12
checks['plane_factor']=abs(angles[-1]['kernel_factor']-2/math.pi)<1e-12
# Uniformly random tangents give isotropic angular average.
orient=quad(lambda u:math.sqrt(1-u*u),-1,1,epsabs=1e-12)[0]/2
checks['isotropic_average']=abs(orient-math.pi/4)<1e-12
# Abel-regulated Fourier identity: inverse of -2pi^2 exp(-eps*k)/k^2.
for eps in [.1,.3,1.]:
    integral=quad(lambda k:math.exp(-eps*k)*math.sin(k)/k if k else 1.,0,np.inf,epsabs=1e-10)[0]
    checks[f'abel_{eps}']=abs(integral-math.atan(1/eps))<1e-9
    def potential(r):return -math.atan(r/eps)/r
    step=1e-5
    derivative=(potential(1+step)-potential(1-step))/(2*step)
    exact=math.atan(1/eps)-eps/(1+eps*eps)
    checks[f'vector_derivative_{eps}']=abs(derivative-exact)<1e-9
# Gaussian baryon source rho(k)=M exp(-b^2 k^2/2), z=r/b.
# Normalize r*g_extra by alpha^2*M/(2*pi^2*a^2*eta).
for z in [.1,.3,1.,3.,10.,30.]:
    f=1-math.sqrt(2)/z*dawsn(z/math.sqrt(2))
    sine=quad(lambda t:math.exp(-t*t/(2*z*z)),0,np.inf,weight='sin',wvar=1.,epsabs=1e-11)[0]
    direct=1-sine/z**2
    checks[f'gaussian_force_{z}']=abs(direct-f)<1e-9
    checks[f'positive_force_{z}']=0<f<1
    rows.append(dict(r_over_b=z,normalized_speed_squared=float(f)))
checks['regular_centre']=abs(rows[0]['normalized_speed_squared']/(.1**2/3)-1)<.003
checks['flat_far_field']=abs(rows[-1]['normalized_speed_squared']-1)<.002
# For fixed source shape, linear response implies V^2 proportional to M.
masses=np.array([.01,.03,.1,.3,1.])
v4=(masses*rows[-1]['normalized_speed_squared'])**2
slope=float(np.polyfit(np.log(masses),np.log(v4),1)[0])
checks['weak_source_mass_exponent']=abs(slope-2)<1e-12
# Explicit validity diagnostic, not a nonlinear interpolation prescription.
# In units alpha=a=eta=h=v=1, P~M/(2*pi^2*r), gap/gradient=M/(2*pi^2).
weak=[dict(mass=float(M),gap_over_gradient=float(M/(2*math.pi**2))) for M in masses]
checks={k:bool(v) for k,v in checks.items()}
result=dict(checks=checks,all_pass=all(checks.values()),angles=angles,isotropic_average=orient,gaussian_profiles=rows,weak_mass_slope=slope,weak_validity=weak,
scope='Leading nodal patch static kernel, zero T/mu, weak-source linearization. Isotropic profile additionally assumes randomly oriented identical rings with equal radial/axial speeds. No full nonlinear sourced determinant, causal dynamics, or data fit.')
(P/'nodal_force_run'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));assert result['all_pass']
