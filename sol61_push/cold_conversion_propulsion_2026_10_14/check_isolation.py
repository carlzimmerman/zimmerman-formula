"""CCP-002: a conversion threshold is not photon invisibility."""
import json
from pathlib import Path
import sys
import numpy as np
from numpy.polynomial.legendre import leggauss
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def ck(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    if not ok:raise AssertionError(name)
apertures=[]
for deg in [15.,30.,60.,90.]:
    ct=np.cos(np.deg2rad(deg));analytic=(1-ct*ct)/4
    vals=[]
    for count in [64,128]:
        z,w=leggauss(count);mu=(1+ct)/2+(1-ct)*z/2
        # Isotropic probability density dmu/2; backward projection mu.
        vals.append(np.dot(w,mu)*(1-ct)/4)
    ck('angular momentum %g'%deg,abs(vals[1]-analytic)<1e-14 and abs(vals[0]-vals[1])<1e-14)
    aperture=dict(half_angle_degrees=deg,escaping_prompt_power_fraction=(1-ct)/2,escaping_mean_cosine=(1+ct)/2,thrust_over_total_prompt_power_div_c=analytic)
    ck('flux identity %g'%deg,abs(aperture['escaping_prompt_power_fraction']*aperture['escaping_mean_cosine']-analytic)<1e-14)
    apertures.append(aperture)

alpha=.0072973525643;me=.51099895069
re=alpha*197.3269804/me*1e-15 # m
scatter=[]
for energy in [.1,.49986703053103493,1.,5.]:
    x=energy/me
    closed=2*np.pi*re**2*((1+x)/x**3*(2*x*(1+x)/(1+2*x)-np.log1p(2*x))+np.log1p(2*x)/(2*x)-(1+3*x)/(1+2*x)**2)
    nums=[]
    for count in [64,128]:
        z,w=leggauss(count);ratio=1/(1+x*(1-z))
        diff=re**2/2*ratio**2*(ratio+1/ratio-(1-z*z))
        ck('differential positive %g %d'%(energy,count),min(diff)>0)
        nums.append(2*np.pi*np.dot(w,diff))
    ck('KN quadrature convergence %g'%energy,abs(nums[0]/nums[1]-1)<1e-10)
    ck('KN independent integral %g'%energy,abs(nums[1]/closed-1)<1e-10)
    scatter.append(dict(energy_MeV=energy,free_electron_sigma_barn=closed/1e-28,numerical_analytic_ratio=nums[1]/closed))
result=dict(status='angular momentum and free-electron interaction verified',assertions=len(checks),apertures=apertures,Compton=scatter,scope='Ideal angular escape mask and free electron only. No real material collimator, attenuation or complete isolation.')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
