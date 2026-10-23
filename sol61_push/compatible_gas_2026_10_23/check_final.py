import json,sys,numpy as np
from gas_v4 import Gas
m=Gas(64,fmol=0,xe=0);y=m.initial();t=m.ti;k,d,_=m.eval(t,y);yy=y.copy();yy[m.sl[0]][:10]*=-1;yy[m.sl[1]][:10]*=-1;kk,dd,_=m.eval(t,yy)
sign=np.ones(m.n);sign[:10]=-1
out={'signed_orbit_energy_difference':dd['energy']-d['energy'],'signed_force_error':float(max(abs(kk[m.sl[1]]-sign*k[m.sl[1]])))}
# A homogeneous gas at rest in comoving coordinates has u proportional A^-2.
m=Gas(32,amp=0,fmol=0,xe=0);y=m.initial();t=m.ti;k,d,_=m.eval(t,y);out['homogeneous_gas_acceleration']=float(max(abs(k[m.sl[3]])));out['homogeneous_thermal_rate_error']=float(max(abs(k[m.sl[8]]+2*(2/(3*t))*y[m.sl[8]])))
out['pass']=abs(out['signed_orbit_energy_difference'])<1e-12 and out['signed_force_error']<1e-10 and out['homogeneous_gas_acceleration']<1e-10 and out['homogeneous_thermal_rate_error']<1e-10
json.dump(out,open(sys.argv[1],'w'),indent=2);print(out)
