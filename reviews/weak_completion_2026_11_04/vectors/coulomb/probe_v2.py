"""Actual cold scalar distributions: screened Born Coulomb rate and diffusion.

The static screening integral is integrated by parts, requiring only f>=0.
The relative-speed convolution is integrated on logarithmic relative momentum;
no RMS-speed replacement or angular cutoff substitutes for slow relative pairs.
"""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;VECTORS=HERE.parent;ROOT=HERE.parents[3];sys.path.insert(0,str(VECTORS));import numpy as np
from gauge_basis_v1 import build
E=.003;G=math.sqrt(29/200)*E;ALPHA=G*G/(4*math.pi);COLOUR=np.array([2/9,3/16,25/144]);SCREEN_FACTORS=np.array([12/6,12/4,12*5/12]);MU=2e6

def moments(u,m,md2):
 mu=m/2;r=4*mu*mu*np.asarray(u)**2/md2;L=np.log1p(r)-r/(1+r);F=r+1-1/(1+r)-2*np.log1p(r);small=r<1e-3
 if np.any(small):
  rr=r[small];L[small]=sum((-1)**n*(n-1)/n*rr**n for n in range(2,10));F[small]=sum((-1)**(n+1)*(n-2)/n*rr**n for n in range(3,11))
 sig=2*math.pi*ALPHA**2/(mu*mu*np.maximum(u,1e-300)**4)*L;sig2=sig*2/np.maximum(r,1e-300)*F/np.maximum(L,1e-300)
 return sig,sig2,L

def radial(edges,f,order):
 z,w=np.polynomial.legendre.leggauss(order);q=(edges[:-1,None]+edges[1:,None])/2+(edges[1:,None]-edges[:-1,None])*z/2;qw=(edges[1:,None]-edges[:-1,None])*w/2;return q.ravel(),qw.ravel(),np.repeat(f,order)

def relative_density(r,edges,f):
 # P(|q-q'|=r), exact radial convolution of piecewise-constant isotropic f.
 r=np.asarray(r);I=float(np.sum(f*(edges[1:]**3-edges[:-1]**3)/3));cum=np.r_[0,np.cumsum(f*(edges[1:]**2-edges[:-1]**2)/2)]
 def primitive(x):
  k=np.clip(np.searchsorted(edges,x,side='right')-1,0,len(f)-1);v=cum[k]+f[k]*(np.clip(x,edges[0],edges[-1])**2-edges[k]**2)/2;return np.where(x>=edges[-1],cum[-1],np.where(x<=0,0,v))
 answer=[];zg,wg=np.polynomial.legendre.leggauss(2)
 for rr in r:
  cuts=np.unique(np.clip(np.r_[edges,edges-rr,edges+rr,rr-edges],0,edges[-1]));a,b=cuts[:-1],cuts[1:];q=(a[:,None]+b[:,None])/2+(b[:,None]-a[:,None])*zg/2;w=(b-a)[:,None]*wg/2;k=np.clip(np.searchsorted(edges,q,side='right')-1,0,len(f)-1);conv=float(np.sum(w*q*f[k]*(primitive(q+rr)-primitive(abs(q-rr)))));answer.append(rr*conv/(2*I*I))
 return np.asarray(answer)

def analyze(edges,f,T,H,m,kernel=None,order=4,angular=96):
 # f is physical occupation of each of twelve real/spinless charged modes.
 q,w,fr=radial(edges,f,order);I=float(np.sum(w*q*q*fr));n=12*T**3/(2*math.pi**2)*I;ee=np.sqrt(m*m+(T*q)**2);md2=G*G*SCREEN_FACTORS/(2*math.pi**2)*T*np.sum(w*fr*(ee+(T*q)**2/ee));z,zw=np.polynomial.legendre.leggauss(angular)
 # Exact relative-speed density, resolving the screening and Born scales.
 lgedges=np.linspace(-12,math.log10(2*edges[-1]),151);zl,wl=np.polynomial.legendre.leggauss(6);lg=(lgedges[:-1,None]+lgedges[1:,None])/2+(lgedges[1:,None]-lgedges[:-1,None])*zl/2;r=10**lg.ravel();rw=(wl[None,:]*(lgedges[1:,None]-lgedges[:-1,None])/2*math.log(10)*10**lg).ravel();pr=relative_density(r,edges,f);u=T/m*r;gamma=np.zeros_like(r);Btrace=np.zeros_like(r);logs=[]
 for c,d in zip(COLOUR,md2):
  s,s2,L=moments(u,m,d);gamma+=c*u*s;Btrace+=c*2*(m/2)**2*u**3*s;logs.append(L)
 pairGamma=n*float(np.sum(rw*pr*gamma));pairB=n*float(np.sum(rw*pr*Btrace));bornbad=u<2.5*ALPHA;slowfracGamma=float(np.sum((rw*pr*gamma)[bornbad])/np.sum(rw*pr*gamma));slowfracB=float(np.sum((rw*pr*Btrace)[bornbad])/np.sum(rw*pr*Btrace));Pnorm=float(np.sum(rw*pr));qc=.75*(edges[1:]**4-edges[:-1]**4)/(edges[1:]**3-edges[:-1]**3);rrel=np.sqrt(np.maximum(0,qc[:,None,None]**2+q[None,:,None]**2-2*qc[:,None,None]*q[None,:,None]*z));vel=T/m*rrel;cospsi=(qc[:,None,None]-q[None,:,None]*z)/np.maximum(rrel,1e-300);dn=12*T**3/(2*math.pi**2)*(w*q*q*fr)[None,:,None]*zw[None,None,:]/2;drag=np.zeros(len(qc));Br=np.zeros(len(qc));Bt=np.zeros(len(qc));logrange=[]
 for c,d in zip(COLOUR,md2):
  s,s2,L=moments(vel,m,d);mu=m/2;drag+=c*np.sum(dn*mu*vel**2*s*cospsi,axis=(1,2))/(T*qc);Br+=c*np.sum(dn*mu*mu*vel**3*(s2*cospsi**2+(s-s2/2)*(1-cospsi**2)),axis=(1,2));Bt+=c*np.sum(dn*2*mu*mu*vel**3*s,axis=(1,2));logrange.append([float(np.min(L)),float(np.max(L))])
 prob=f*(edges[1:]**3-edges[:-1]**3)/3;prob/=prob.sum();hole=Br/(2*(T*np.diff(edges))**2*H);loss=None if kernel is None else np.asarray(kernel)@(6*T**3/(2*math.pi**2)*f*(edges[1:]**3-edges[:-1]**3)/3)/H
 return dict(n_mu3=n,Debye_masses_mu=np.sqrt(md2).tolist(),mean_Gamma_transport_over_H=pairGamma/H,mean_dp2_dt_over_p2H=pairB/(H*T*T*float(np.sum(w*q**4*fr)/I)),relative_density_normalization=Pnorm,low_relative_Born_alphaeff_over_v_gt1_rate_fraction=slowfracGamma,low_relative_Born_alphaeff_over_v_gt1_dp2_fraction=slowfracB,mean_velocity=float(T/m*np.sum(w*q**3*fr)/I),q_centers=qc.tolist(),probability=prob.tolist(),drag_over_H=(drag/H).tolist(),radial_dp2_over_p2H=(Br/(H*(T*qc)**2)).tolist(),bin_width_refill_over_H=hole.tolist(),number_loss_over_H_by_bin=None if loss is None else loss.tolist(),Btrace_pair_vs_tag_relative=float((prob@Bt)/pairB-1),max_physical_f=float(max(f)),quantum_final_Bose_factor_bound=(1+float(max(f)))**2,angular_nodes=angular,radial_nodes_per_cell=order)

def main(out):
 start=time.monotonic();old=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_hybrid_bw_001/result.json').read_text())['case'];stage=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());kern=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/kernels.json').read_text());packet=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance/run_leading001/result.json').read_text())['packet'];omega=math.sqrt(float(packet['local_profile']['radial_curvature_mu2'])/62);x=old['history'][-1]['x_minimum'];m=E/2*math.sqrt(x*x+2/(31*E));b=build(x);Sc=next(g for g in b['s']['groups'] if g['id']=='Sc_0');ids=np.array(Sc['indices']);traces={}
 for name in ('V8','V3','V1'):
  q=b['qs'][np.ix_(b['vgroups'][name],ids,ids)];metric=np.einsum('aij,bji->ab',q,q).real/len(ids);traces[name]=dict(factor=float(np.sum(metric*metric)),metric=metric.tolist())
 rows=[]
 for name,h,f,K in [('stage_initial',old['history'][0],2*np.array(stage['initial_fS']),kern['K'][0]),('stage_final',old['history'][-1],2*np.array(stage['final_fS']),kern['K'][-1]),('hybrid_final',old['history'][-1],2*np.array(old['final_f_S_number_normalization']),kern['K'][-1])]:
  T=h['Tc_over_mu'];H=h['H_over_oscillation']*omega;d=analyze(np.array(stage['q_edges']),f,T,H,m,K);d.update(name=name,Tc=T,H_mu=H);rows.append(d);print(name,d['mean_Gamma_transport_over_H'],d['mean_dp2_dt_over_p2H'],max(d['bin_width_refill_over_H']),flush=True)
 # Direct radial/angle refinement on the most depleted actual packet.
 ref=analyze(np.array(stage['q_edges']),2*np.array(stage['final_fS']),old['history'][-1]['Tc_over_mu'],old['history'][-1]['H_over_oscillation']*omega,m,kern['K'][-1],order=8,angular=192);base=rows[1];p=np.array(base['probability']);err=float(np.sum(p*abs(np.array(ref['radial_dp2_over_p2H'])-base['radial_dp2_over_p2H']))/np.sum(p*np.array(ref['radial_dp2_over_p2H'])))
 checks=dict(colour_trace=bool(abs(sum(v['factor'] for v in traces.values())-7/12)<1e-10),relative_density=bool(all(abs(r['relative_density_normalization']-1)<2e-5 for r in rows)),pair_tag_diffusion=bool(all(abs(r['Btrace_pair_vs_tag_relative'])<.03 for r in rows)),diffusion_refinement=bool(err<.02),Bose_dilute=bool(max(r['max_physical_f'] for r in rows)<1e-4))
 Path(out).write_text(json.dumps(dict(claim_id='CC11_ACTUAL_COLD_SCREENED_COULOMB_DISCRIMINATOR',colour_traces=traces,cases=rows,refined_stage_final=ref,weighted_radial_diffusion_refinement_relative=err,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Actual CT09 conditional late scalar packets plus CC10 changing-memory shape, twelve scalar modes with fphysical=2fnumber. Direct t-channel screened Born colour-averaged scalar Coulomb discriminator; exact relative-speed convolution, static isotropic Vlasov Debye masses. Identical u-channel/interference finite-log terms, bound/nonperturbative low-relative-speed scattering, dynamic screening and neutral/gaugino baths not included here; low-v contribution fractions separated. No assertion of full-history viability.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
