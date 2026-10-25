import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,numpy as np
from scipy.special import erf
from sphere import Sphere
rows=[]
for ne in [16,32,64,128]:
 s=Sphere(ne,12,16,eta=.2);r=s.r[:,None,None];u=np.exp(-r*r/2)*s.sr[:,None,None]*s.sa[None,:,:];pot=s.poisson(u);h=s.moments(u,pot)
 exact=-np.pi**1.5*erf(s.r)/s.r
 row=dict(ne=ne,mass_error=abs(h['M']/np.pi**1.5-1),kinetic_error=abs(h['K']/(.75*.2**2*np.pi**1.5)-1),potential_weighted_error=float(np.sqrt(np.sum(abs(u)**2*(pot-exact[:,None,None])**2)/np.sum(abs(u)**2))),transform_error=float(np.max(abs(s.transform(s.transform(u),True)-u))),radial_unitarity=abs(np.sum(abs(s.radial(u,.1))**2)-h['M']),COM=h['COM'])
 # Symmetric Green and derivative of W for an unrelated smooth density perturbation.
 m=abs(u)**2;d=m*np.cos(s.r[:,None,None])*(1+.2*s.mu[None,:,None]);pd=s.poisson_mass(d);row['Green_symmetry']=abs(float(np.sum(m*pd)-np.sum(d*pot)));eps=1e-5;wp=.5*np.sum((m+eps*d)*s.poisson_mass(m+eps*d));wm=.5*np.sum((m-eps*d)*s.poisson_mass(m-eps*d));row['W_derivative_error']=abs(float((wp-wm)/(2*eps)-np.sum(d*pot)))
 rows.append(row)
assert rows[-1]['mass_error']<1e-8 and rows[-1]['kinetic_error']<1e-7
assert rows[-1]['potential_weighted_error']<rows[0]['potential_weighted_error']/50
assert all(x['transform_error']<1e-12 and x['radial_unitarity']<1e-12 and x['Green_symmetry']<1e-10 and x['W_derivative_error']<1e-8 for x in rows)
print(json.dumps(rows,indent=2))
