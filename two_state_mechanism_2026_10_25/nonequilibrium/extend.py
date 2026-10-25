import argparse,json
from pathlib import Path
import numpy as np
from kinetics_v3 import Rates,parcel,PROFILES,BASE

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();rates=Rates(BASE/'run_refine/results.json');rows=[]
 for alpha in [.15,.2]:
  for mass in np.geomspace(1e7,1e11,9):
   states=[parcel(rates,alpha,float(mass),Mb,b) for Mb,b in PROFILES]
   f=[s['molecular_mass_fraction'] for s in states]
   rows.append(dict(alpha=alpha,mass_eV=float(mass),states=states,applicable=all(s['applicable'] for s in states),target=f[2]>=.8 and max(f[0],f[1],f[3])<=.2))
 eligible=[r for r in rows if r['applicable']];best=max(eligible,key=lambda r:r['states'][2]['molecular_mass_fraction']) if eligible else None
 summary=dict(points=len(rows),profile_runs=4*len(rows),eligible_points=len(eligible),targets=sum(r['target'] for r in rows),eligible_targets=sum(r['target'] for r in eligible),best=best,max_energy_error=max(s['errors']['energy_absolute'] for r in rows for s in r['states']))
 Path(a.output).write_text(json.dumps(dict(summary=summary,rows=rows),indent=2)+'\n')
 print('points',len(rows),'eligible',len(eligible),'best',None if best is None else [best['alpha'],best['mass_eV'],[s['molecular_mass_fraction'] for s in best['states']]])
if __name__=='__main__':main()
