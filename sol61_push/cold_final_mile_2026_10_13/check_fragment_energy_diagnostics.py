"""CE-FM-082C: logs and one96³ checkpoint, below1GB, no evolution."""
import json,math,hashlib,sys,struct
from pathlib import Path
import numpy as np
try:
 import os;os.nice(19)
except OSError:pass
b=Path('sol61_push/cold_final_mile_2026_10_13');receipt=json.loads((b/'fragment_raw_input_receipt.json').read_text());src=json.loads(Path('argon_push/ARGON11_nonlinear_fragmentation_2026-10-17/argon11_results.json').read_text());checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
for name,v in receipt['external_inputs'].items():ck('initial raw hash '+Path(name).name,hashlib.sha256(Path(name).read_bytes()).hexdigest()==v['sha256'])
logs={};summary={}
for tag,x in src.items():
 data={}
 for line in Path('/Users/carlzimmerman/new_physics/_external_data/argon11_work/log_'+tag+'.txt').read_text().splitlines():
  if not line or line.startswith('#'):continue
  a=[float(z) for z in line.split()];data[round(a[0],4)]=a
 arr=[data[k] for k in sorted(data)];logs[tag]=arr;dq=max(abs(a[1]/arr[0][1]-1) for a in arr);de=max(abs(a[2]/arr[0][2]-1) for a in arr)
 ck(tag+' raw charge drift replay',abs(dq-x['K1']['dQ'])<1e-14);ck(tag+' raw Hamiltonian drift replay',abs(de-x['K1']['dE'])<1e-14)
 A=next((a for a in x['series'] if a['f_core']>=.5),None);ck(tag+' first threshold epoch',x['tA']==(None if A is None else A['t']))
 if A:
  k3=A['Nl']>=3 and A['nndev']<=.25 and A['EQ_med']<1;ck(tag+' saved K3 arithmetic',k3==x['K3']['FRAGMENTS'])
 summary[tag]={'K1_charge':dq,'K1_energy':de,'tA':x['tA'],'K3_source_replayed':x['K3']['FRAGMENTS']}
# External latest R1 checkpoint is6 native-double fields after native64-bit long.
w=Path('/Users/carlzimmerman/new_physics/_external_data/argon11_work');N=96;n=N**3;ck('known raw checkpoint size',(w/'ckpt_R1.bin').stat().st_size==8+6*n*8)
step=struct.unpack('q',(w/'ckpt_R1.bin').open('rb').read(8))[0];ck('checkpoint time agrees with snapshot',step==70000)
f=np.memmap(w/'ckpt_R1.bin',dtype=np.float64,mode='r',offset=8,shape=(6,N,N,N));pr,pi,vr,vi,c,vc=f
I=pr*pr+pi*pi;V=I+1.99*I*I+200*c*I+5000*c*c-12.5*c*c*c+.25*c**4
base=float(np.sum(vr*vr+vi*vi+.5*vc*vc+V));grad4=0.;gradcentral=0.;correction=0.
for field,weight in [(pr,1.),(pi,1.),(c,.5)]:
 for axis in range(3):
  plus=np.roll(field,-1,axis=axis);minus=np.roll(field,1,axis=axis);dc=(plus-minus)/2;d2=plus-2*field+minus
  lap4=(-np.roll(field,-2,axis=axis)+16*plus-30*field+16*minus-np.roll(field,2,axis=axis))/12
  grad4-=weight*float(np.sum(field*lap4));gradcentral+=weight*float(np.sum(dc*dc));correction+=weight*float(np.sum(d2*d2))/3
E4=base+grad4;Ecentral=base+gradcentral;Q=float(np.sum(2*(pr*vi-pi*vr)));snap=np.memmap(w/'snap_R1_t00700.0.bin',dtype=np.float32,mode='r',shape=(3,n));Esnap=float(np.sum(snap[2],dtype=np.float64));last=logs['R1'][-1]
ck('checkpoint Hamiltonian matches raw log',abs(E4/last[2]-1)<1e-10);ck('checkpoint charge matches raw log',abs(Q/last[1]-1)<1e-10);ck('centered-gradient energy matches snapshot',abs(Ecentral/Esnap-1)<1e-7);ck('operator energy gap exact identity',abs((grad4-gradcentral)/correction-1)<1e-10);ck('snapshot energy below conserved Hamiltonian',Esnap<E4)
for name,v in receipt['external_inputs'].items():ck('final raw hash '+Path(name).name,hashlib.sha256(Path(name).read_bytes()).hexdigest()==v['sha256'])
res={'claim_id':'CE-FM-082C','n_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'checks':checks,'raw_logs_replayed':summary,'R1_end':{'E_Hamiltonian':E4,'E_snapshot':Esnap,'relative_snapshot_deficit':1-Esnap/E4,'positive_gradient_correction':correction,'snapshot_charge_relative_error':Q/last[1]-1},'scope':'Eight raw log conservation replays, saved gate arithmetic and one96³ energy-definition reconciliation. No raw connected-component reclassification, convergence proof, scattering law or escape spectrum certified.'}
Path(sys.argv[1]).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='checks'},indent=2))
