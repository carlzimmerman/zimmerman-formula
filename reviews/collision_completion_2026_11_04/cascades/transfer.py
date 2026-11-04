"""Conservative dilute neutral cascade response, including coherent parent pulse.

`build_transfer` is a reusable vacuum transport operator. It does not assume
that neutral daughters thermalize, and retains each massive neutral force.
Quantum/inverse transport instead uses reaction.full_events.
"""
import sys,json,time,math,resource,copy
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix,bmat,kron,eye
from scipy.sparse.linalg import expm_multiply
from network import ROOT
from reaction import full_events

def build_transfer(data,pnodes=None,angles=6):
 p=np.unique(np.r_[0.,np.geomspace(1e-6,.001,12),np.linspace(.001,.08,60),.1,.2,.3]) if pnodes is None else np.asarray(pnodes)
 pairs=data['singlet_channel_Gamma'];reachable={d for key in pairs for d in key.split('|')}
 while True:
  old=set(reachable)
  for c in data['channels']:
   if c['parent'] in reachable:reachable.update(c['daughters'])
  if old==reachable:break
 by={g['id']:g for g in data['groups']};assert not any(by[g]['charged'] for g in reachable)
 d=dict(data,channels=[c for c in data['channels'] if c['parent'] in reachable]);ev=full_events(d,1.,p,np.ones(len(p)),angles=angles)
 # Vacuum one-body number operator, independent of fictitious quadrature W:
 # coefficient/parent measure = Γ M/E times angular weight.
 r=len(ev.coefficient);P=coo_matrix((ev.coefficient/ev.measure[ev.index[:,0]],(np.arange(r),ev.index[:,0])),shape=(r,len(ev.measure))).tocsr();A=ev.S@P
 active=np.concatenate([np.arange(ev.by[g]*len(p),(ev.by[g]+1)*len(p)) for g in sorted(reachable)]);A=A[active][:,active].tocsr();lookup={int(v):i for i,v in enumerate(active)};B=np.zeros((len(active),16));M=math.sqrt(2*data['e']);injection={}
 def split(nodes,e):
  lo=int(np.clip(np.searchsorted(nodes,e)-1,0,len(nodes)-2));a=float(np.clip((e-nodes[lo])/(nodes[lo+1]-nodes[lo]),0,1));return lo,lo+1,1-a,a
 for key,gamma in pairs.items():
  j,k=key.split('|');m1,m2=by[j]['mass'],by[k]['mass'];e1=(M*M+m1*m1-m2*m2)/(2*M);e2=M-e1;v=np.zeros(len(active))
  for gid,en in ((j,e1),(k,e2)):
   gi=ev.by[gid];a,b,wa,wb=split(ev.energies[gi],en);v[lookup[gi*len(p)+a]]+=wa;v[lookup[gi*len(p)+b]]+=wb
  injection[key]=v;B+=v[:,None]*np.array(gamma).T.ravel()[None,:]
 force=np.repeat([g.get('dm2_dx',0.) for g in ev.groups],len(p))/(2*np.maximum(ev.energy,1e-300))
 return dict(A=A,B=csr_matrix(B),events=ev,active=active,energies=ev.energy[active],force=force[active],p=p,reachable=sorted(reachable),injection=injection,by=by)

def main(out):
 start=time.monotonic();data=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_network001/result.json').read_text())['cases'][-2];basis=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_basis002/result.json').read_text());data['singlet_channel_Gamma']=basis['Gamma_by_daughter_pair_CT09_mu'];pole=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_pole002/result.json').read_text());G=np.array(pole['production_Gram_mu2']);gamma=np.array(pole['Gamma_other_matrix_mu']);rho0=G/np.trace(G);tr=build_transfer(data);L=-(kron(csr_matrix(gamma),eye(4))+kron(eye(4),csr_matrix(gamma)))/2;Op=bmat([[L,None],[tr['B'],tr['A']]],format='csr');initial=np.r_[rho0.ravel(),np.zeros(len(tr['active']))];M=pole['Mpole'];energy=np.r_[M*np.eye(4).ravel(),tr['energies']];energyres=float(np.max(abs(energy@Op)));trace=float(Op.diagonal().sum());rows=[]
 times=np.unique(np.r_[0.,np.geomspace(1e7,3e12,65)])
 # Fresh expm from each previous checkpoint avoids a stiff dense-grid solve.
 state=initial.copy();old=0.
 for t in times:
  if t>old:state=expm_multiply(Op*(t-old),state,traceA=trace*(t-old));old=t
  rho=state[:16].reshape(4,4);Y=state[16:];nums={gid:0. for gid in tr['reachable']};forces={gid:0. for gid in tr['reachable']};energygroups={gid:0. for gid in tr['reachable']};ev=tr['events'];n=len(tr['p'])
  for z,flat in enumerate(tr['active']):
   gid=ev.groups[flat//n]['id'];nums[gid]+=Y[z];forces[gid]+=Y[z]*tr['force'][z];energygroups[gid]+=Y[z]*tr['energies'][z]
  rows.append(dict(time_mu=float(t),singlet_survival=float(np.trace(rho)),number=nums,force=forces,energy=energygroups,neutral_force_per_parent=float(tr['force']@Y),total_energy=float(energy@state),min_number=float(Y.min()),rho_min_eigenvalue=float(np.linalg.eigvalsh(rho).min())))
 checks=dict(energy_generator=energyres<1e-22,energy_evolution=max(abs(r['total_energy']/M-1) for r in rows)<1e-8,positive_number=min(r['min_number'] for r in rows)>-1e-12,parent_density_PSD=min(r['rho_min_eigenvalue'] for r in rows)>-1e-12,all_reachable_neutral=not any(tr['by'][g]['charged'] for g in tr['reachable']))
 result=dict(claim_id='CC10_COHERENT_PARENT_NEUTRAL_CASCADE_TRANSFER',cases=rows,checks=checks,parent_rho0_CT09=rho0.tolist(),parent_Gamma_CT09_mu=gamma.tolist(),reachable=tr['reachable'],p_nodes_mu=tr['p'].tolist(),energy_generator_max_error=energyres,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Unit coherent four-singlet parent pulse atrest at exactpole; every open physical tree cascade retains daughter momentum, delay, energy and force. Dilute vacuum transfer only; no neutral inverse stimulation/Pauli, expansion or late abundance claim. All reachable parents below broken-vector threshold, so SSS/FFS tree coverage complete here.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,'late force',rows[-1]['neutral_force_per_parent'],'runtime',result['runtime_seconds']);assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
