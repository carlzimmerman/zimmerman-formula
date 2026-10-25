"""Conservative interval envelope for implemented log-PCHIP rate ratios."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.special import lambertw
from kinetics_v3 import Rates,BASE

def envelope(rates,upper):
 # On each interval each log(k_b/k_A) is a cubic. Its maximum lies at an
 # endpoint or a real derivative root; sum of separate maxima bounds the sum.
 p=rates.lk;bounds=[]
 for i in range(len(p.x)-1):
  hi=min(p.x[i+1],np.log(upper))-p.x[i]
  if hi<0:continue
  total=0.
  for b in range(1,len(rates.D)+1):
   c=p.c[:,i,b]-p.c[:,i,0]
   candidates=[0.,hi]
   for z in np.roots(np.array([3*c[0],2*c[1],c[2]])):
    if abs(z.imag)<1e-12 and 0<z.real<hi:candidates.append(float(z.real))
   total+=np.exp(max(np.polyval(c,x) for x in candidates))
  bounds.append(total)
 rmax=float(max(bounds))*(1+1e-12)
 t=float(rmax*lambertw(1/rmax).real)
 return dict(T_range=[float(rates.Ts[0]),upper],rate_ratio_upper=rmax,molecular_count_cap=t,molecular_mass_cap=201/101*t,scope='Uniform for implemented log-PCHIP rate table; floating point envelope, not interval-arithmetic certification of exact Coulomb rates')

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();r=Rates(BASE/'run_refine/results.json')
 out=[envelope(r,T) for T in [.05,.3]]
 assert all(x['molecular_mass_cap']<.8 for x in out)
 Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
