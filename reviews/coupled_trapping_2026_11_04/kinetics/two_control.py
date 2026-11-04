"""Independent discrete charge-count and two-body energy moment controls."""
import sys,os
sys.dont_write_bytecode=True
import json,time,math,resource
import numpy as np
from pathlib import Path
from two_species import Two,ROOT,HERE

def main(out):
 start=time.monotonic();p=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())['points'][0];s=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text())['points'][0]['spins'][0];m=Two(p,s,bins=16,orbitn=12);m.setup();rows=[]
 for x in (.1,1.,3.,3.8375,5.,10.,25.):
  t=.004 if x<5 else .001;A,events=m.conversion(x,t);F=float(m.mass(x));S=.003/2*math.sqrt(x*x+2/(31*.003));a=0 if F>S else 1;ma=max(F,S);mb=min(F,S);u=np.r_[m.W*m.f0/m.norm,np.zeros(m.n)] if a==0 else np.r_[np.zeros(m.n),m.W*m.f0/m.norm];en=np.r_[np.sqrt(F*F+(t*m.q)**2),np.sqrt(S*S+(t*m.q)**2)];q=-float(en@(A@u));key='gauge_channels_total_over_mu' if a==0 else 'reverse_gauge_channels_total_over_mu';gamma=float(np.interp(x,m.rx,[r[key] for r in m.sources]));exact=gamma*(ma*ma-mb*mb)/(2*ma);off=A.copy();np.fill_diagonal(off,0);rows.append(dict(x=x,t=t,parent='F' if a==0 else 'S',max_columnsum_abs=float(max(abs(A.sum(axis=0)))),min_offdiagonal=float(off.min()),energy_source=q,exact_massless_gaugino_energy_source=exact,relative_energy_error=abs(q/exact-1) if exact else 0.))
 checks=dict(conversion_number_conservation=max(r['max_columnsum_abs'] for r in rows)<1e-23,positive_deposition=min(r['min_offdiagonal'] for r in rows)>=0,energy_moment=max(r['relative_energy_error'] for r in rows)<.005)
 result=dict(claim_id='CT09_TWO_SPECIES_OPERATOR_CONTROLS',checks=checks,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Finite momentumgrid, actual interpolated vacuumwidth, masslessgaugino boost. Independent exact two-body meanenergy moment. No actual gaugino occupation/inverse factors.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
