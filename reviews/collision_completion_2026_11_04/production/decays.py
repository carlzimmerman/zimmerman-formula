"""Conditional NR neutral-adjoint decay/photino production in SM RD cosmology.

Exact gauge widths are frozen inputs. Soft gaugino widths are conditional
matching estimates, never promoted here to an on-shell branching result.
"""
import os,sys,math,json,time,resource,hashlib
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'reviews/coupled_trapping_2026_11_04/photino'))
from phase_space import free_stream as reference_free_stream
T0=2.3486541805581e-13;HBAR=6.582119569e-25;MPL=2.435e18
MPC_KM=3.0856775814913673e19;C_KM_S=299792.458;H0_KM_S_MPC=67.4;OM=.315
H0=H0_KM_S_MPC/MPC_KM;MU=2e6;DM_S=.44e-9;NEUTRINO_ONE=7/8*(4/11)**(4/3)

class Cosmology:
 def __init__(self,resolution=16385):
  table=np.loadtxt(HERE/'standardmodel2018.dat');T,gr,_,gs,_=table.T
  self.gs0=float(gs[0]);self.gr0=float(gr[0]);self.T=T;self.gr=gr;self.gs=gs
  self.lT=np.log(T);self.gsi=PchipInterpolator(self.lT,np.log(gs));self.gri=PchipInterpolator(self.lT,np.log(gr))
  a=T0/T*(self.gs0/gs)**(1/3);order=np.argsort(a);aa=a[order]
  Hrad=np.sqrt(math.pi**2*gr[order]/90)*T[order]**2/MPL/HBAR
  self.OR=(math.sqrt(math.pi**2*self.gr0/90)*T0*T0/MPL/HBAR/H0)**2;self.OL=1-OM-self.OR
  self.lasm=np.log(aa);self.lHsm=np.log(Hrad)
  self.hi=PchipInterpolator(self.lasm,self.lHsm)
  tt=np.r_[0,cumulative_trapezoid(1/Hrad,self.lasm)]+1/(2*Hrad[0])
  self.tsm=tt;self.at=PchipInterpolator(np.log(tt),self.lasm);self.ta=PchipInterpolator(self.lasm,np.log(tt))
  self.Ta=PchipInterpolator(self.lasm,np.log(T[order]))
  self.grid=np.linspace(self.lasm[0],0,resolution);self.ag=np.exp(self.grid)
  old=self.grid<self.lasm[-1]
  Hr=np.empty(resolution);Hr[old]=np.exp(self.hi(self.grid[old]));Hr[~old]=H0*math.sqrt(self.OR)/self.ag[~old]**2
  H=np.sqrt(Hr**2+H0**2*(OM/self.ag**3+self.OL))
  integrand=C_KM_S/MPC_KM/(self.ag*H);dl=np.diff(self.grid)
  self.weights=np.r_[dl[0]/2,(dl[:-1]+dl[1:])/2,dl[-1]/2]*integrand
  self.chi0=PchipInterpolator(self.grid,np.r_[0,cumulative_trapezoid(integrand,self.grid)])
  self.age=PchipInterpolator(self.grid,np.r_[0,cumulative_trapezoid(1/H,self.grid)])
 def birth(self,t):return np.exp(self.at(np.log(t)))
 def temperature(self,a):
  a=np.asarray(a);v=np.empty_like(a);early=a<math.exp(self.lasm[-1]);v[early]=np.exp(self.Ta(np.log(a[early])));v[~early]=T0/a[~early];return v
 def time_at_a(self,a):return np.exp(self.ta(np.log(a)))
 def travel(self,alpha,ab):
  alpha=np.atleast_1d(alpha);ab=np.atleast_1d(ab)
  # All injected particles have p*/m>2e7, so below birth their virtual
  # v differs from 1 by <1e-15. Subtract the massless pre-birth prefix.
  v=alpha[:,None]/np.sqrt(alpha[:,None]**2+self.ag[None,:]**2)
  return v@self.weights-self.chi0(np.log(ab))

def exponential_nodes(n=96):
 # u=Gamma t=r^2 removes the sqrt(u) early-RD endpoint cusp.
 z,w=leggauss(n);r=(z+1)*math.sqrt(35)/2;weights=w*math.sqrt(35)/2*2*r*np.exp(-r*r)
 return r*r,weights

def summarize(cos,M,mchi,width,branch,n=96,reference=False):
 tau=HBAR/(MU*width);u,w=exponential_nodes(n);ab=cos.birth(tau*u);alpha=M/(2*mchi)*ab
 fs=cos.travel(alpha,ab);v=alpha/np.sqrt(1+alpha*alpha);anr=alpha
 qu=np.array([-math.log1p(-q) for q in (.1,.5,.9)]);qa=cos.birth(tau*qu);qal=M/(2*mchi)*qa
 qfs=cos.travel(qal,qa);median_alpha=float(qal[1])
 result=dict(total_width_mu=width,lifetime_seconds=tau,photino_branch_conditional=branch,
  mean_decay_temperature_GeV=float(w@cos.temperature(ab)),median_decay_temperature_GeV=float(cos.temperature(qa)[1]),
  mean_birth_scale_factor=float(w@ab),mean_p0_over_mchi=float(w@alpha),mean_v0_km_s=float(C_KM_S*(w@v)),
  mean_free_streaming_kpc=float(1000*(w@fs)),mean_v_recombination=float(w@(alpha/np.sqrt(alpha*alpha+(1/1090)**2))),
  median_NR_redshift=1/median_alpha-1,median_NR_photon_temperature_GeV=T0/median_alpha,
  median_NR_age_years=float(cos.age(math.log(median_alpha))/(365.25*86400)),
  decay_quantiles=[dict(number_quantile=q,time_seconds=float(tau*uu),a_birth=float(a),alpha=float(al),free_streaming_kpc=float(1000*f)) for q,uu,a,al,f in zip((.1,.5,.9),qu,qa,qal,qfs)],
  quadrature_norm=float(w.sum()),quadrature_mean_u=float(w@u))
 if reference:
  ref=np.array([reference_free_stream(float(al),float(a)) for al,a in zip(alpha,ab)])
  result['CT09_reference_mean_free_streaming_kpc']=float(1000*(w@ref));result['SM_vs_CT09_reference_relative_difference']=float((w@fs)/(w@ref)-1)
 return result

def normalization(cos,states,rows,yields,label):
 rhos=[];chis=[];radiation=[];dominance=[]
 photon_over_s=3*T0/(2*cos.gs0)
 for s,r in zip(states,rows):
  name=s['id'];Y=yields[name];M=s['mass']*MU;B=r['photino_branch_conditional'];a=r['mean_birth_scale_factor']
  rest=Y*M;rho_dr=rest*a*(1-B);Ychi=Y*B;rhochi=Ychi*states[0]['mchi_mu']*MU
  rhos.append(rest);chis.append(rhochi);radiation.append(rho_dr)
  # Parent/radiation ratio before depletion at the median temperature is
  # deliberately conservative: no exponential suppression is included.
  temp=r['median_decay_temperature_GeV'];gr=math.exp(cos.gri(math.log(temp)));gs=math.exp(cos.gsi(math.log(temp)))
  dominance.append(4/3*gs/gr*rest/temp)
  srow=dict(id=name,Y_parent=Y,Y_chi_conditional=Ychi,rest_if_stable_GeV_per_s=rest,
   gauge_DR_today_GeV_per_s=rho_dr,gauge_Delta_Neff=rho_dr/photon_over_s/NEUTRINO_ONE,
   chi_rest_DM_fraction_conditional=rhochi/DM_S,parent_over_SM_radiation_undepleted_at_median=dominance[-1])
  if len(rhos)==1:subrows=[srow]
  else:subrows.append(srow)
 return dict(normalization=label,states=subrows,rest_if_stable_DM_multiple=sum(rhos)/DM_S,
  gauge_Delta_Neff=sum(radiation)/photon_over_s/NEUTRINO_ONE,
  chi_rest_DM_fraction_conditional=sum(chis)/DM_S,undepleted_parent_over_SM_radiation_median_sum=sum(dominance),
  interpretation='Yield normalization only. Fixed pole masses and early-NR parents are assumed; no physical full-history abundance is inferred.')

def main(out):
 start=time.monotonic();cos=Cosmology();coarse=Cosmology(8193)
 vv=json.loads((HERE.parent/'neutral_loop/run004/result.json').read_text());gc=json.loads((HERE.parent/'neutral_loop/run_gaugino003/result.json').read_text())
 case=next(c for c in vv['cases'] if abs(c['x']-25.4000254000381)<1e-9 and c['e']==.003);mchi=abs(gc['baseline_threshold_real'][11][11])
 states=[];baseline=[];gaugeonly=[];scans=[];checks={};refinement=[]
 for s,g in zip(case['states'],gc['states']):
  M=s['mass'];wg=s['width'];wc=g['soft_mixed_photino_width'];w=wg+wc;B=wc/w
  states.append(dict(id=s['id'],mass=M,mchi_mu=mchi,gauge_width_mu=wg,soft_chi_width_mu=wc,pstar_over_mchi=M/(2*mchi)))
  r=summarize(cos,M,mchi,w,B,reference=True);r.update(id=s['id'],scenario='conditional_soft_chi_plus_exact_gauge');baseline.append(r)
  ro=summarize(cos,M,mchi,wg,0,reference=False);ro.update(id=s['id'],scenario='exact_gauge_only_shape_diagnostic_no_chi_production');gaugeonly.append(ro)
  rr=summarize(coarse,M,mchi,w,B,n=48);err=abs(rr['mean_free_streaming_kpc']/r['mean_free_streaming_kpc']-1);refinement.append(dict(id=s['id'],grid_and_quadrature_refinement_relative_error=err));checks['refinement_'+s['id']]=err<2e-4
  for factor in (.1,.3,1.,3.,10.,30.,100.):
   a=summarize(cos,M,mchi,factor*w,B);a.update(id=s['id'],family='common_total_width_multiplier_fixed_branch',factor=factor);scans.append(a)
   ww=wg+factor*wc;bb=factor*wc/ww;a=summarize(cos,M,mchi,ww,bb);a.update(id=s['id'],family='conditional_soft_partial_width_multiplier_exact_gauge_floor',factor=factor);scans.append(a)
  # Monoenergetic 1-kpc threshold and actual exponential cold fraction.
  R=M/(2*mchi)
  logalpha=brentq(lambda la:cos.travel(np.array([math.exp(la)]),np.array([math.exp(la)/R]))[0]-.001,-35,-5)
  alpha_cold=math.exp(logalpha);birth_cold=alpha_cold/R;tcold=float(cos.time_at_a(birth_cold));coldfrac=-math.expm1(-tcold/r['lifetime_seconds'])
  # A required common-rate multiplier is only a timing discriminator; it
  # is not a computed new microscopic width or an altered production epoch.
  required=math.exp(brentq(lambda lk:math.log(summarize(cos,M,mchi,w*math.exp(lk),B,n=48)['mean_free_streaming_kpc']),0,60))
  r['one_kpc_mono_source_threshold']=dict(alpha=alpha_cold,a_birth=birth_cold,time_seconds=tcold,photon_temperature_GeV=float(cos.temperature(np.array([birth_cold]))[0]),
   fraction_of_exponential_chi_decays_below_one_kpc=coldfrac,required_common_width_multiplier_for_mean_one_kpc=required)
  checks['probability_'+s['id']]=abs(r['quadrature_norm']-1)<1e-12 and abs(r['quadrature_mean_u']-1)<1e-12
  checks['source_mass_hierarchy_'+s['id']]=R>2e7
 memory=json.loads((HERE.parent/'memory/run_stage001/result.json').read_text());warm=json.loads((HERE.parent/'integration/run_warm001/result.json').read_text())
 late={s['id']:memory['neutral_terminal_group_yields'][s['id']]['number_yield'] for s in states}
 factor=.02**3/(2*math.pi**2/45*106.75);h=warm['case']['history'][-1]
 early={s['id']:h['comoving_number_by_group'][warm['case']['groups'].index(s['id'])]*factor for s in states}
 norms=[]
 for label,ys in (('late_finite_resonance_stage_terminal_yields',late),('early_warm_checkpoint_yield_transplant_to_fixed_pole',early)):
  norms.append(normalization(cos,states,baseline,ys,label+'_conditional_soft_chi'))
  norms.append(normalization(cos,states,gaugeonly,ys,label+'_exact_gauge_only'))
  for ratefactor in (.1,100.):
   selected=[next(z for z in scans if z['id']==s['id'] and z['family']=='common_total_width_multiplier_fixed_branch' and z['factor']==ratefactor) for s in states]
   norms.append(normalization(cos,states,selected,ys,label+'_conditional_rate_factor_'+str(ratefactor)))
 checks['late_stable_intermediate_83_84']=abs(norms[0]['rest_if_stable_DM_multiple']/83.84242347042143-1)<1e-6
 checks['all_width_scan_hotter_than_one_kpc']=all(z['mean_free_streaming_kpc']>1 for z in scans)
 checks['RD_test_population_subdominant']=all(z['undepleted_parent_over_SM_radiation_median_sum']<.1 for z in norms)
 eosfile=HERE/'standardmodel2018.dat'
 result=dict(claim_id='CC10_CONDITIONAL_COSMOLOGICAL_NEUTRAL_DECAYS',checks=checks,states=states,baseline=baseline,gauge_only=gaugeonly,width_scans=scans,normalizations=norms,refinement=refinement,
  cosmology=dict(Tgamma0_GeV=T0,H0_km_s_Mpc=H0_KM_S_MPC,Omega_m=OM,Omega_r=cos.OR,Omega_Lambda=cos.OL,g_rho_low=cos.gr0,g_s_low=cos.gs0,Mpl_reduced_GeV=MPL,
   EOS_source='https://arxiv.org/src/1803.01038v2/anc/standardmodel2018.dat',EOS_sha256=hashlib.sha256(eosfile.read_bytes()).hexdigest(),EOS_interpolation='PCHIP in logT/logg; entropy-conserved a(T); early time integral dln(a)/H_SM; late LCDM including matter and Lambda'),
  runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  scope='Early NR parents, fixed pole masses, constant local widths, exponential decay and collisionless chi propagation. Gauge-only widths are computed inputs; every chi abundance/branch is conditional on soft not-yet-on-shell matching. Normalization packets are distinct finite stages, not a completed common history.',
  non_claims=['No physical full-history terminal abundance','No thermal scattering, inverse decay, entropy injection or evolving-X width solution','No assertion that all radiation is visible or that unbroken model gauge bosons thermalize with SM','One-kpc criterion applies to this produced component; a tiny warm fraction is not an all-DM exclusion'])
 Path(out).write_text(json.dumps(result,indent=2)+'\n')
 for r in baseline:print(r['id'],'tau',r['lifetime_seconds'],'Tmedian',r['median_decay_temperature_GeV'],'FS_kpc',r['mean_free_streaming_kpc'],'v0_km_s',r['mean_v0_km_s'],'zNRmedian',r['median_NR_redshift'],flush=True)
 print(checks,flush=True);assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
