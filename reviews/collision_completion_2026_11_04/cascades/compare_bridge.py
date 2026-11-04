"""Direct/averaged warm bridge: counts, action and weighted momentum shapes."""
import sys,json,time,resource,math
from pathlib import Path
import numpy as np
from network import ROOT

def main(out,direct=None,averaged=None):
 start=time.monotonic();base=ROOT/'reviews/collision_completion_2026_11_04/cascades';D=json.loads((Path(direct) if direct else base/'run_warm_direct_consistent001/result.json').read_text());A=json.loads((Path(averaged) if averaged else base/'run_warm_averaged001/result.json').read_text());dh=D['history'];ah=A['case']['history'];groups=dh[0]['groups'];q=np.array(D['q']);W=np.array(D['W']);n=len(q);Yd=np.array(D['state']['Y']).reshape(-1,n);Ya=np.array(A['state']['Y']).reshape(-1,n);fd=np.array(dh[-1]['f']).reshape(-1,n);fa=np.array(ah[-1]['f']).reshape(-1,n);deg=Yd.sum(axis=1)/np.maximum((fd*W[None,:]).sum(axis=1)/(2*np.pi**2),1e-300);measure=deg[:,None]*W[None,:]/(2*np.pi**2)
 def compare(d,a,ff_d,ff_a):
  rows=[]
  for s,g in enumerate(groups):
   nd,na=float(d[s].sum()),float(a[s].sum());norm=max(nd,1e-300);absdiff=abs(a[s]-d[s]);j=int(np.argmax(abs(ff_a[s]-ff_d[s])));rows.append(dict(group=g,direct_number=nd,averaged_number=na,number_relative_error=na/norm-1,number_weighted_L1=float(absdiff.sum()/norm),normalized_shape_L1=float(sum(abs(a[s]/max(na,1e-300)-d[s]/norm))),max_occupation_difference=float(abs(ff_a[s,j]-ff_d[s,j])),max_difference_q=float(q[j]),number_error_from_df_gt_point1=float(np.sum(absdiff[abs(ff_a[s]-ff_d[s])>.1])/norm)))
  return rows
 endpoint=compare(Yd,Ya,fd,fa);t=np.array([h['time_mu'] for h in dh]);period=D['initial_period_mu'];mask=t>=t[-1]-period-1e-6;ts=t[mask];snapf=np.array([h['f'] for h in dh])[mask].reshape(-1,len(groups),n);snapY=snapf*measure[None,:,:];duration=ts[-1]-ts[0];Ymean=np.trapz(snapY,ts,axis=0)/duration;fmean=Ymean/measure;center=(ts[-1]+ts[0])/2;ta=np.array([h['time_mu'] for h in ah]);AA=np.array([h['f'] for h in ah]);fmid=np.array([np.interp(center,ta,AA[:,i]) for i in range(AA.shape[1])]).reshape(-1,n);Yamid=fmid*measure;orbit_mean=compare(Ymean,Yamid,fmean,fmid)
  # Total charged count includes all six charged scalar/fermion groups.
 charged=np.array([g.startswith('Sc_') or g.startswith('Fc_') for g in groups]);nd=float(Yd.sum(axis=1)@charged);na=float(Ya.sum(axis=1)@charged);Jdi=dh[0]['action'];Jdf=dh[-1]['action'];Jai=ah[0]['action'];Jaf=ah[-1]['action'];deltaD=Jdf-Jdi;deltaA=Jaf-Jai
 action=dict(direct_initial=Jdi,direct_final=Jdf,averaged_initial=Jai,averaged_final=Jaf,direct_fractional_drift=deltaD/Jdi,averaged_fractional_drift=deltaA/Jai,endpoint_relative_error=Jaf/Jdf-1,drift_relative_error=(deltaA-deltaD)/deltaD)
 checks=dict(same_N=abs(D['state']['N']-A['state']['N'])<1e-12,same_grid=bool(np.array_equal(q,np.array(A['case']['q'])) and np.array_equal(W,np.array(A['case']['W']))),direct_pass=bool(all(D['checks'].values())),averaged_pass=bool(all(A['checks'].values())),positive=bool(min(Yd.min(),Ya.min())>=0))
 result=dict(claim_id='CC10_WARM_DIRECT_AVERAGED_COMPARISON',checks=checks,final_N=D['state']['N'],action=action,charged_endpoint_relative_error=na/nd-1,all_species_number_weighted_L1=float(sum(abs(Ya-Yd).ravel())/sum(Yd.ravel())),endpoint_by_group=endpoint,last_cycle_mean_comparison=dict(time_start=float(ts[0]),time_end=float(ts[-1]),averaged_comparison_time=float(center),by_group=orbit_mean),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Sameimmutablewarmcheckpoint; direct3periodfield versus6phaseaveraged smallsteps, all25groups/current commonmasses andenergyledger. Endpoint distributions differ by fastphase; lastcycle means use eight directtimeintervals and linearlyinterpolated averagedf. Agreement values are measured finiteerrors, no universal averaging theorem. Angularquadrature2 still needs independentrefinement.')
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(checks,'chargederr',result['charged_endpoint_relative_error'],'action',action)
 for r in endpoint:
  if r['group'] in ('F1_1','F3_0','F8_0','Sc_0','Fc_0'):print(r)
 assert all(checks.values()),checks
if __name__=='__main__':main(*sys.argv[1:])
