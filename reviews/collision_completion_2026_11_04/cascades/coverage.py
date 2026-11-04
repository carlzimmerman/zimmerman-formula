"""Population diagnostics for kinematically possible omitted broken-vector exits."""
import sys,json,time,resource
from pathlib import Path
import numpy as np
from network import ROOT
from vertices import VertexBackground

def coverage(data,t,q,W,f):
 groups=data['groups'];m=np.array([g['mass'] for g in groups]);n=len(q);deg=np.array([g['degeneracy'] for g in groups]);Y=deg[:,None]*np.asarray(W)[None,:]*np.asarray(f).reshape(len(groups),n)/(2*np.pi**2);en=np.sqrt(m[:,None]**2+(t*np.asarray(q)[None,:])**2);num=Y.sum(axis=1);energy=np.sum(Y*en,axis=1);mins={kind:min(g['mass'] for g in groups if g['kind']==kind and g['charged']) for kind in ('S','F')};threshold=np.array([data['m_vector']+(0 if g['charged'] else mins[g['kind']]) for g in groups]);possible=m>threshold+1e-12
 return dict(eligible_groups=[g['id'] for g,b in zip(groups,possible) if b],number_fraction=float(num@possible/max(num.sum(),1e-300)),energy_fraction=float(energy@possible/max(energy.sum(),1e-300)),number_by_eligible_group={g['id']:float(v) for g,v,b in zip(groups,num,possible) if b},energy_by_eligible_group={g['id']:float(v) for g,v,b in zip(groups,energy,possible) if b})

def main(out):
 start=time.monotonic();bg=VertexBackground(ROOT/'reviews/collision_completion_2026_11_04/cascades/run_vertices001/result.json');c=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_coupled004/result.json').read_text())['cases'][0];q=np.array(c['q']);W=np.array(c['W']);rows=[]
 for h in c['history']:
  r=coverage(bg.at(h['x']),h['Tc'],q,W,h['f']);r.update(time_mu=h['time_mu'],N=h['N'],x=h['x']);rows.append(r)
 result=dict(claim_id='CC10_VECTOR_OPEN_POPULATION_COVERAGE',cases=rows,max_possible_vector_open_energy_fraction=max(r['energy_fraction'] for r in rows),max_possible_vector_open_number_fraction=max(r['number_fraction'] for r in rows),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,checks=dict(fractions_valid=all(0<=r['energy_fraction']<=1 and 0<=r['number_fraction']<=1 for r in rows)),scope='Conservative kinematic eligibility of omitted broken-vector exits along direct warm snapshots. Parent population fraction is not an omitted reaction-rate bound; actual vector vertices/widths not computed. Chargedparent thresholdmV; neutralparent thresholdmV+lowestchargedS/F; neutralSVV threshold2mV is included by this weaker sufficient eligibility test whenmC<mV.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(result['max_possible_vector_open_energy_fraction'],result['max_possible_vector_open_number_fraction'])
if __name__=='__main__':main(sys.argv[1])
