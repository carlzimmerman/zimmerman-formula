import json,sys,numpy as np
from gas_v3 import rates
kb=1.380649e-16;mp=1.67262192369e-24;G=6.67430e-8;X=.76;mu=1.22;Msun=1.98847e33
out=[]
for T in [100,200,300,500,1000,2000]:
 low,lte,_=rates(np.array(float(T)),np.array(1.));n=lte/low;rho=mp*n/X;cs=np.sqrt(kb*T/(mu*mp));ff=np.sqrt(3*np.pi/(32*G*rho));jeans=np.pi**2.5*cs**3/(6*G**1.5*np.sqrt(rho))/Msun
 for f in [1e-6,1e-4,1e-3]:
  cool=1.5*kb*T/(X*mu*f*n*low)*2
  out.append(dict(T=T,fH2=f,ncrit=float(n),tcool_over_tff_min=float(cool/ff),isothermal_gas_Jeans_Msun=float(jeans)))
json.dump(out,open(sys.argv[1],'w'),indent=2);print(json.dumps(out,indent=2))
