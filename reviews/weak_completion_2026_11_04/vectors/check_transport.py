import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'))
import numpy as np
from common import CommonBackground
from transport import VectorFactory
from basis import invariants
from rates import channels,matrix_element

def main(out):
 start=time.monotonic();bg=CommonBackground();factory=VectorFactory(HERE/'run_table001/result.json');prior=json.loads((ROOT/'reviews/collision_completion_2026_11_04/history/run_refine002/result.json').read_text());q=np.array(prior['case']['q']);W=np.array(prior['case']['W']);rows=[];refine=[];boost=[];tableerrors=[]
 for x in (3.8632233,5.,25.4000254000381):
  data=bg.at(x);t=.00465 if x<10 else .000001;ev=factory.full_events(data,t,q,W,angle_order=2);v=ev.vector_operator;f=1/(np.exp(np.minimum(v.energy/(.012 if x<10 else .02),700))-v.eta);a=1+v.eta*f;aud=v.audit(f,a);rng=np.random.default_rng(418);h=rng.normal(size=len(f));h*=np.maximum(f,.01)*v.measure;eps=1e-6;fp=f+eps*h/v.measure;fm=f-eps*h/v.measure;num=(v.number_rhs(fp)-v.number_rhs(fm))/(2*eps);analytic=v.number_jacobian(f)@h;jerr=float(np.linalg.norm(num-analytic)/max(np.linalg.norm(num),1e-100))
  physical=np.zeros(len(f));Y=np.array(prior['state']['Y']);physical[:len(Y)]=Y/v.measure[:len(Y)];physical[physical==0]=1e-35;rhs=v.number_rhs(physical);gross=v.number_gross(physical);widths={g['id']:sum(c['width'] for c in ev.channels if c['parent']==g['id']) for g in ev.groups};number_rhs=rhs.reshape(30,len(q)).sum(axis=1)
  rows.append(dict(x=x,t=t,audit=aud,jacobian_relative=jerr,vector_events=len(v.coefficient),channels=ev.channels,widths=widths,initial_vector_number_rhs=float(sum(number_rhs[i] for i,g in enumerate(ev.groups) if g['kind']=='V')),initial_charged_number_rhs=float(sum(number_rhs[i] for i,g in enumerate(ev.groups) if g['charged'])),physical_entropy_rate=float(-np.log(physical/(1+v.eta*physical))@rhs),occupied_forward_omission=float(v.omitted_by_parent@physical),gross_rate=float(sum(gross)),bosonic_vectors=bool(np.all(ev.eta[25*len(q):]==1))))
  # Positive quadrature refinement on a deliberately nonequilibrium interior state.
  ftest=.1*f*(1+.4*np.sin(np.arange(len(f))*.31));r=[]
  for order in (2,4,8):
   e=factory.full_events(data,t,q,W,angle_order=order).vector_operator;r.append(e.number_rhs(ftest))
  refine.append(dict(x=x,order2_to8=float(sum(abs(r[0]-r[2]))/max(sum(abs(r[2])),1e-100)),order4_to8=float(sum(abs(r[1]-r[2]))/max(sum(abs(r[2])),1e-100))))
  # Raw exact vs interpolated invariant rates at the same common kinematics.
  exact=invariants(x);ce=channels(exact,ev.groups);ct=channels(factory.table.at(x),ev.groups);ke=lambda c:(c['kind'],c['p'],c['j'],c['k']);de={ke(c):c for c in ce};dt={ke(c):c for c in ct};zz,wz=np.polynomial.legendre.leggauss(64);er=[]
  for key in de.keys()&dt.keys():
   c=de[key];M,m1,m2=ev.masses[[c['p'],c['j'],c['k']]];a0=float(wz@matrix_element(c,M,m1,m2,0*zz,zz,ev.groups));a1=float(wz@matrix_element(dt[key],M,m1,m2,0*zz,zz,ev.groups));er.append((abs(a1-a0),a0))
  tableerrors.append(dict(x=x,total_width_integrand_relative_L1=float(sum(a for a,b in er)/max(sum(b for a,b in er),1e-100)),largest_relative_for_significant_channel=max([a/b for a,b in er if b>1e-8*max(v for u,v in er)]+[0])))
  # Summing daughter L/T reproduces the same covariant inclusive width after boost.
  blocks={}
  for c in ce:
   if c['kind'].startswith('V_'):continue
   key=(c['p'],c['j'] if c['kind']!='S_VV' else -1,c['kind']);blocks.setdefault(key,[]).append(c)
  for key,cs in blocks.items():
   vals=[]
   for P in (0.,.04,.2):
    tot=0
    for c in cs:
     M,m1,m2=ev.masses[[c['p'],c['j'],c['k']]];tot+=float(wz@matrix_element(c,M,m1,m2,np.full_like(zz,P),zz,ev.groups))
    vals.append(tot)
   boost.append(dict(x=x,key=list(key),relative_spread=float((max(vals)-min(vals))/max(vals[0],1e-100))))
  print(x,len(v.coefficient),jerr,aud['energy_rhs_relative'],flush=True)
 checks=dict(Ward_and_projection=bool(all(c['controls']['scalar_Goldstone_Ward']<1e-10 and c['controls']['fermion_Goldstone_Ward']<1e-10 for c in json.loads((HERE/'run_table001/result.json').read_text())['cases'])),DB=bool(all(r['audit']['detailed_balance_RHS_relative']<1e-11 for r in rows)),energy=bool(all(r['audit']['energy_rhs_relative']<1e-13 for r in rows)),jacobian=bool(all(r['jacobian_relative']<1e-7 for r in rows)),entropy=bool(all(r['physical_entropy_rate']>=-1e-20 for r in rows)),vectors_bosons=bool(all(r['bosonic_vectors'] for r in rows)),boost_inclusive=bool(all(r['relative_spread']<1e-10 for r in boost)))
 result=dict(rows=rows,quadrature_refinement=refine,table_errors=tableerrors,boost_controls=boost,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Fixed-background physical vector channels; L/T explicit in cosmological frame, total widths compared under boosts. No evolution or candidate claim.');Path(out).write_text(json.dumps(result,indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
