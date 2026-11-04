"""Actual corrected warm-state vector transport impact and finite advances."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,math,resource
import numpy as np
from common import CommonBackground,CommonOrbit,extend_numbers,OLD,T0
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/vectors'))
from transport_v3 import VectorFactory

def main(output,table):
 start=time.monotonic();prior=json.loads((OLD/'history/run_refine002/result.json').read_text());case=prior['case'];st=prior['state'];q=np.array(case['q']);W=np.array(case['W']);N=st['N'];bg=CommonBackground();model=CommonOrbit(bg,q,W,8);model.J0=st['J0'];model.last_x=st['xmid'];Y=extend_numbers(st['Y'],bg.base.groups,bg.groups,len(q));orb=model.orbit(N,Y,J=st['J']);factory=VectorFactory(table);ev=factory.averaged_events(bg,orb['xs'],orb['weights'],T0*math.exp(-N),q,W,angle_order=4);f=Y/model.measure;available=1+model.eta*f;C=ev.number_rhs(f,available);parts=ev.local_events
 local_energy=[];CS=[];CV=[];vv=[]
 for w,p in zip(ev.phase_weights,parts):
  c=p.number_rhs(f,available);cs=p.scalar_fermion_operator.number_rhs(f,available);cv=p.vector_operator.number_rhs(f,available);local_energy.append(float(p.energy@c));CS.append(cs);CV.append(cv);vv.append(float(np.sum(cv.reshape(model.ns,model.n).sum(axis=1)[25:])))
 cs=ev.phase_weights@np.array(CS);cv=ev.phase_weights@np.array(CV);charged=np.repeat(model.charged,model.n);normal=2*math.pi**2/45*106.75/(.02**3);toyield=1/normal
 def moments(c):
  n=c.reshape(model.ns,model.n).sum(axis=1);return dict(charged_number_rate_mu=float(n@model.charged),photino_number_rate_mu=float(n[model.by['F1_1']]),vector_number_rate_mu=float(sum(n[25:])),charged_yield_derivative_N=float((n@model.charged)*toyield/model.hubble(N)),photino_yield_derivative_N=float(n[model.by['F1_1']]*toyield/model.hubble(N)))
 gross=float(sum(ev.number_gross(f,available)));escale=max(float(max(ev.energy))*gross,1e-300);force=model.gas(orb['xs'],N,Y)['force_by'];checks=dict(thirty_group_measure=len(ev.groups)==30,statistics_match=bool(np.array_equal(ev.eta,model.eta)),physical_initial_bounds=bool(min(f)>=0 and max(f[model.eta<0])<=1),linear_operator_sum=bool(max(abs(C-cs-cv))<1e-20),local_energy=bool(max(abs(np.array(local_energy)))/escale<1e-12),vector_birth=bool(sum((cv.reshape(model.ns,model.n).sum(axis=1))[25:])>0))
 out=dict(claim_id='CC11_VECTOR_IMPACT_CORRECTED_WARM',checks={k:bool(v) for k,v in checks.items()},N=N,xs=orb['xs'].tolist(),phase_weights=orb['weights'].tolist(),scalar_fermion=moments(cs),vector=moments(cv),total=moments(C),vector_birth_by_group=[dict(id=g['id'],rate=float(cv.reshape(model.ns,model.n).sum(axis=1)[i])) for i,g in enumerate(model.groups) if g['kind']=='V'],local_energy_relative=float(max(abs(np.array(local_energy)))/escale),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual corrected warm snapshot with initially empty vector populations. Full L/T vector1<->2 contributions and inverse gains compared to retained SF operator. A frozen-state derivative, not an evolved final abundance or common cold history.')
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));assert all(checks.values()),checks
if __name__=='__main__':main(*sys.argv[1:])
