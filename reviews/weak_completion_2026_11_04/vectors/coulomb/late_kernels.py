"""Occupation-independent actual neutral channels/work for conditional coldelastic stage."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];OLD=ROOT/'reviews/collision_completion_2026_11_04';sys.path.insert(0,str(OLD/'memory'));sys.path.insert(0,str(OLD/'cascades'))
import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse.linalg import splu
from response_api_v4 import band_kernel,M
from transfer import build_transfer

def main(out):
 start=time.monotonic();late=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_hybrid_bw_001/result.json').read_text())['case'];stage=json.loads((OLD/'memory/run_stage001/result.json').read_text());oldkern=json.loads((OLD/'memory/run_stage001/kernels.json').read_text());packet=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance/run_leading001/result.json').read_text())['packet'];gamma=json.loads((OLD/'cascades/run_basis002/result.json').read_text())['Gamma_by_daughter_pair_CT09_mu'];keys=list(gamma);hist=late['history'];edges=np.array(stage['q_edges']);Ns=np.array([h['N'] for h in hist]);omega=math.sqrt(float(packet['local_profile']['radial_curvature_mu2'])/62);H0=hist[0]['H_over_oscillation']*omega;data=json.loads((OLD/'cascades/run_network001/result.json').read_text())['cases'][-2];data['singlet_channel_Gamma']=gamma;tr=build_transfer(data,angles=6);A=tr['A'];uu=np.where(A.diagonal()<0)[0];ss=np.where(A.diagonal()==0)[0];lu=splu(A[uu][:,uu].tocsc());AZ=A[ss][:,uu];TT=[];delays=[]
 for key in keys:
  inj=tr['injection'][key];terminal=inj[ss]-AZ@lu.solve(inj[uu]);mom=AZ@lu.solve(lu.solve(inj[uu]));valid=terminal>1e-11;TT.append(terminal);delays.append(float(max(mom[valid]/terminal[valid],default=0)))
 stable_flat=tr['active'][ss];n=len(tr['p']);group=[tr['events'].groups[v//n]['id'] for v in stable_flat];p=tr['p'][stable_flat%n];mass=np.array([tr['by'][g]['mass'] for g in group]);dm=np.array([tr['by'][g].get('dm_dx',0) for g in group]);terminal_energy_error=float(np.max(abs(np.array(TT)@np.sqrt(mass*mass+p*p)/M-1)));indices=np.unique(np.round(np.linspace(0,len(hist)-1,17)).astype(int));cases=[];validation=[];partial=True;reason='started';checks={}
 fields=['K','scalar_field_power_pair','absolute_scalar_field_power_bound_pair','finite_width_energy_ledger_residual_pair','neutral_exit_energy_rate_pair','charged_mean_energy_rate_pair','parent_energy_density_pair']
 def compute(i):
  h=hist[i];k=band_kernel(xmid=h['x_minimum'],amplitude=(h['x_outer']-h['x_inner'])/2,omega=omega,Tc=h['Tc_over_mu'],edges=edges,radial=2,angular=12,channels=gamma);r=dict(index=int(i),N=h['N'],Tc=h['Tc_over_mu'],H=h['H_over_oscillation']*omega,channel_K=[k['channel_K'][key].tolist() for key in keys],max_boost_error=k['max_boost_error']);r.update({key:np.asarray(k[key]).tolist() for key in fields});return r
 def save():Path(out).write_text(json.dumps(dict(partial=partial,reason=reason,cases=cases,validation=validation,fields=fields,channel_keys=keys,terminal_transfer=np.array(TT).tolist(),terminal_group=group,terminal_p_mu=p.tolist(),terminal_mass_mu=mass.tolist(),terminal_dm_dx=dm.tolist(),maximum_H_delay=H0*max(delays),terminal_energy_relative_error=terminal_energy_error,omega=omega,parent_mass=M,initial_J=hist[0]['action'],q_edges=edges.tolist(),checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ActualCT09prescribedsloworbitchannelresolved4PresponseandCC10v4signedwork/finitewidthmoments; massivecascadepositiveabsorptionmapretainsactualterminalp,m,dm; noCoulomborchargedshapeevolutioninthispretable. Interpolationtobetestedagainstactualmiddlepoints; notfullcandidate.'),separators=(',',':'))+'\n')
 save()
 try:
  for i in indices:
   if time.monotonic()-start>200:reason='durable_wall_checkpoint';save();return
   c=compute(int(i));c['old_K_relative']=float(np.max(abs(np.array(c['K'])-oldkern['K'][int(i)]))/max(np.max(oldkern['K'][int(i)]),1e-300));c['channel_sum_relative']=float(np.max(abs(np.sum(c['channel_K'],axis=0)-c['K']))/max(np.max(c['K']),1e-300));cases.append(c);print(i,time.monotonic()-start,flush=True);save()
  # Baseline evolving f determines named comparison weights at omitted points.
  W=(edges[1:]**3-edges[:-1]**3)/3;Ks=np.array(oldkern['K'])
  def interp(N,grid,values):
   j=int(np.clip(np.searchsorted(grid,N)-1,0,len(grid)-2));a=(N-grid[j])/(grid[j+1]-grid[j]);return (1-a)*values[j]+a*values[j+1]
  def rhs(N,y):
   T=hist[0]['Tc_over_mu']*math.exp(-(N-Ns[0]));H=H0*math.exp(-2*(N-Ns[0]));return -interp(N,Ns,Ks)@(12*T**3/(2*math.pi**2)*W*np.exp(y))/H
  sol=solve_ivp(rhs,[Ns[0],Ns[-1]],np.log(stage['initial_fS']),rtol=3e-8,atol=2e-9,dense_output=True,max_step=.005)
  grid=np.array([c['N'] for c in cases]);channels=np.array([c['channel_K'] for c in cases]);totals=np.array([c['K'] for c in cases])
  for i in (2,7,22,46,70):
   c=compute(i);N=c['N'];f=np.exp(sol.sol(N));prob=W*f;prob/=prob.sum();pred=interp(N,grid,channels);kt=interp(N,grid,totals);pred*=np.array(c['K'])[None,:,:]/np.maximum(kt[None,:,:],1e-300);exact=np.array(c['channel_K']);ep=np.einsum('i,aij,j->a',prob,exact,prob);pp=np.einsum('i,aij,j->a',prob,pred,prob);validation.append(dict(index=i,N=N,total_channel_L1_relative=float(sum(abs(ep-pp))/sum(ep)),channel_rates_exact=ep.tolist(),channel_rates_interpolated=pp.tolist()));save()
  partial=False;reason='target_reached';checks=dict(oldK=bool(max(c['old_K_relative'] for c in cases)<1e-10),channel_sum=bool(max(c['channel_sum_relative'] for c in cases)<1e-10),channel_interpolation=bool(max(v['total_channel_L1_relative'] for v in validation)<.03),terminal_energy=bool(terminal_energy_error<1e-9),delay=bool(H0*max(delays)<1e-3));save();assert all(checks.values()),checks
 except BaseException as exc:reason=repr(exc);save();raise
if __name__=='__main__':main(sys.argv[1])
