"""Reconstruct actual oldmemory terminal momentum cohorts and cold C-lambda kicks."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'reviews/collision_completion_2026_11_04/cascades'));import numpy as np
from scipy.sparse.linalg import splu
from transfer import build_transfer

def kick(E,M,D):
 s=M*M+2*M*E;Q=4*M*M*E*E/s;r=Q/D;L=np.log1p(r)-r/(1+r);A2=D*(r+1-1/(1+r)-2*np.log1p(r));A3=D*D*(.5*r*r-2*r-1+1/(1+r)+3*np.log1p(r));I1=L-A2/Q;I2=(A2-A3/Q)/(4*M*M);return I1+I2,I1/(2*M)

def main(out):
 start=time.monotonic();stage=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());network=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_network001/result.json').read_text())['cases'][-2];basis=json.loads((ROOT/'reviews/collision_completion_2026_11_04/cascades/run_basis002/result.json').read_text());network['singlet_channel_Gamma']=basis['Gamma_by_daughter_pair_CT09_mu'];tr=build_transfer(network,angles=6);A=tr['A'];unstable=np.where(A.diagonal()<0)[0];stable=np.where(A.diagonal()==0)[0];lu=splu(A[unstable][:,unstable].tocsc());AZ=A[stable][:,unstable];keys=list(network['singlet_channel_Gamma']);terminal=[]
 for key in keys:
  inj=tr['injection'][key];terminal.append(inj[stable]-AZ@lu.solve(inj[unstable]))
 terminal=np.array(terminal);npnode=len(tr['p']);ev=tr['events'];flat=tr['active'][stable];gid=np.array([ev.groups[v//npnode]['id'] for v in flat]);pb=tr['p'][flat%npnode];Ns=np.array([r['N'] for r in stage['rows']]);rate=np.array([[r['channel_event_yield_per_N'][k] for k in keys] for r in stage['rows']]);source=rate@terminal;Nend=Ns[-1];Tc=stage['rows'][-1]['Tc'];send=2*math.pi**2/45*106.75*(Tc/.02)**3;G=math.sqrt(29/200)*.003;alpha=G*G/(4*math.pi);probe=json.loads((HERE.parent/'run_coulomb003/result.json').read_text());base=probe['cases'][1];H=base['H_mu'];m=.003/2*math.sqrt(25.4000254000381**2+2/(31*.003));scalar_md2=np.array(base['Debye_masses_mu'])**2;mdextra=np.zeros(3);records=[];cohorts=[]
 # Positive GL birth-time integration preserves each cohort's actual hard p.
 z,w=np.polynomial.legendre.leggauss(4)
 for j in range(len(Ns)-1):
  dn=Ns[j+1]-Ns[j]
  for zz,ww in zip(z,w):
   birth=(Ns[j]+Ns[j+1])/2+dn/2*zz;u=(birth-Ns[j])/dn;count=((1-u)*source[j]+u*source[j+1])*dn/2*ww;p=pb*np.exp(birth-Nend);cohorts.append((count,p))
 for group,rep,cavg in [('F8_0',0,3/8),('F3_0',1,2/3),('S8_0',0,3/8),('S3_0',1,2/3)]:
  mask=(gid==group)&(pb>0);mass=tr['by'][group]['mass'];Y=float(sum(count[mask].sum() for count,p in cohorts));screen=float(G*G*cavg*send*sum(np.sum(count[mask]*(np.sqrt(mass*mass+p[mask]**2)+p[mask]**2/np.sqrt(mass*mass+p[mask]**2))/p[mask]**2) for count,p in cohorts));mdextra[rep]+=screen;records.append(dict(group=group,number_yield=Y,reference_number_yield=stage['neutral_terminal_group_yields'][group]['number_yield'],screening_mass2=screen,min_physical_p=float(min(p[mask].min() for count,p in cohorts)),max_physical_p=float(max(p[mask].max() for count,p in cohorts))))
 totalmd=scalar_md2+mdextra;B=0;heat=0
 for group,rep,cavg in [('F8_0',0,.5),('F3_0',1,.5)]:
  mask=(gid==group)&(pb>0);b=0;hh=0
  for count,p in cohorts:
   kk,he=kick(p[mask],m,totalmd[rep]);b+=4*math.pi*alpha**2*cavg*send*float(count[mask]@kk);hh+=4*math.pi*alpha**2*cavg*send*float(count[mask]@he)
  # Continuous redshift broadens each finite terminal momentum stream.
  ps=pb[mask];src=source[:,mask];cuts=np.unique((ps[:,None]*np.exp(Ns[None,:]-Nend)).ravel());cuts=np.unique(np.r_[cuts,cuts*(1+1e-10),cuts*(1-1e-10)]);sumsource=np.zeros(len(cuts))
  for p0,stream in zip(ps,src.T):
   birth=Nend+np.log(cuts/p0);sumsource+=np.interp(birth,Ns,stream,left=0,right=0)
  deg=16 if rep==0 else 6;occ=2*math.pi**2*send/deg*sumsource/cuts**3;fmax=float(max(occ));r=next(a for a in records if a['group']==group);r.update(dp2_rate_mu3=b,kinetic_energy_heating_mu2=hh,max_continuous_stream_f=fmax,Pauli_final_factor_bound=max(0,1-fmax));B+=b;heat+=hh
 pmean2=float((base['mean_dp2_dt_over_p2H']) and probe['refined_stage_final']['mean_dp2_dt_over_p2H']);# Reconstruct charged mean p² independently from recorded cells.
 edges=np.array(stage['q_edges']);f=2*np.array(stage['final_fS']);I=np.sum(f*(edges[1:]**3-edges[:-1]**3)/3);p2=Tc*Tc*np.sum(f*(edges[1:]**5-edges[:-1]**5)/5)/I
 checks=dict(number_cohorts=bool(all(abs(r['number_yield']/r['reference_number_yield']-1)<1e-10 for r in records)),finite_positive=bool(B>0 and heat>0 and np.all(np.isfinite(totalmd))),Pauli_dilute=bool(max(r.get('max_continuous_stream_f',0) for r in records)<1e-4))
 Path(out).write_text(json.dumps(dict(records=records,scalar_screening_mass2=scalar_md2.tolist(),bath_screening_mass2=mdextra.tolist(),total_screening_mass2=totalmd.tolist(),C_lambda_dp2_over_p2H=B/(p2*H),C_lambda_kinetic_heating_over_KH=heat/(p2/(2*m)*H),C_self_dp2_over_p2H=base['mean_dp2_dt_over_p2H'],checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ActualCC10memorylate-neutralbirthcohorts reconstructed throughpositive terminal map andredshift, includinghardlambda3/8 bath anditscontinuousbirthtimePaulioccupation. HeavyC-at-rest screenedscalar-fermion Bornkick discriminator. Theseareonlylatecascadebaths; oldearlygauginoeventcountlacksfλ andisnotinventedasaFD bath. No selfconsistentchemicalhistoryclaim.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
