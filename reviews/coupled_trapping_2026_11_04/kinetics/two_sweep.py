"""Extended cooling for a pinned conditional two-species gravity packet."""
import sys,os
sys.dont_write_bytecode=True
from pathlib import Path
import json,time,math,resource
import numpy as np
from two_species import Two,evolve_two,ROOT,HERE

def main(out,kind,profile,Tend,bins):
 start=time.monotonic();Tend=float(Tend);bins=int(bins);stat=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text());spins=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text());p=dict(next(z for z in stat['points'] if z['kind']==kind));s=next(z for z in spins['points'] if z['kind']==kind)['spins'][0];packet=None
 if profile!='base':
  rows=json.loads((ROOT/profile).read_text())['rows'];packet=rows[-1];r=packet['global_profile'];p.update(grid=r['grid'],T0_potential_mu4=r['V0_origin_subtracted_mu4'],origin_force=r['origin_force'],origin_curvature=r['origin_curvature'],mu_GeV=float(packet['constants']['MU']))
 model=Two(p,s,bins=bins,orbitn=16,absorbing=True)
 if packet:model.grid=np.unique(np.r_[0,np.linspace(.001,10,100),np.linspace(10,40,180)])
 run=evolve_two(model,math.log(s['TD_over_mu']/Tend),.001);run.update(kind=kind,profile=profile,mu_GeV=p['mu_GeV'],bulk_bins=bins,end_Tc=Tend)
 result=dict(claim_id='CT09_TWO_SPECIES_EXTENDED',case=run,checks={'cooling_reached':run['reason']=='target cooling reached','energy_ledger':bool(max(abs(h['energy_ledger_error']) for h in run['history'])<.02),'local_averaging_hierarchy':bool(model.maxlocal<.1)},runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Same conditional emptygaugino/unblockedsink two-species network as two_species.py, extendedcooling. Pinned retunedprofiles changephysicalgravityparameters andmu; priorprotected conditional x0,Tc0 retained. NoPauli/inversegaugino, noactualneutralcascade orfinalphotinoabundance. Turningpoints muststayinsideprofiledomain; no extrapolatedglobalcold-vacuum conclusion.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes')}));print(kind,profile,run['reason'],run['history'][-1]);assert all(result['checks'].values())
if __name__=='__main__':main(*sys.argv[1:])
