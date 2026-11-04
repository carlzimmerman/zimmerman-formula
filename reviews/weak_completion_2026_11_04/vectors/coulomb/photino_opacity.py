"""Actual cold C+chi->F narrow-line optical depth, including the tree current."""
import sys,json,time,resource,math
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(HERE.parent));sys.path.insert(0,str(ROOT/'reviews/coupled_trapping_2026_11_04/photino'));sys.path.insert(0,str(ROOT/'reviews/weak_completion_2026_11_04/integration'))
import numpy as np
from gauge_basis_v1 import build
from source import atx,width
from common import CommonBackground

def main(out):
 start=time.monotonic();x=25.4000254000381;b=build(x);src=atx(x);common=CommonBackground().at(x);by={g['id']:g for g in common['groups']};actual={g['id']:g for g in b['s']['groups']};MC=by['Sc_0']['mass'];mchi=by['F1_1']['mass'];idsC=np.array(actual['Sc_0']['indices']);idchi=np.array(actual['F1_1']['indices'])-98;parents=[];H2=0
 for name in ('Fc_0','Fc_1','Fc_2'):
  P=actual[name];ids=np.array(P['indices'])-98;M=by[name]['mass'];y=b['yuk'][np.ix_(ids,idchi,idsC)];norm=float(np.sum(abs(y)**2)/len(ids));H2+=float(np.sum(abs(y)**2)/len(idsC));Gamma=float(np.sum(width(M,mchi,MC,y))/len(ids));# Loop-Majorana phase only affects an O(mchi/deltaM) interference term.
  if name=='Fc_0':Gamma=src['widths_over_mu']['U1']
  ps=math.sqrt((M-MC-mchi)*(M+MC+mchi)*(M-MC+mchi)*(M+MC-mchi))/(2*M);Er=(M*M-MC*MC-mchi*mchi)/(2*MC);pr=math.sqrt(max(0,Er*Er-mchi*mchi));parents.append(dict(parent=name,mass_mu=M,C_mass_mu=MC,chi_mass_mu=mchi,partial_Gamma_Cchi_mu=Gamma,tree_yukawa_norm2_per_parent=norm,pstar_mu=ps,chi_resonance_energy_mu=Er,chi_resonance_momentum_mu=pr,spin_colour_ratio=by[name]['degeneracy']/(by['Sc_0']['degeneracy']*by['F1_1']['degeneracy'])))
 packet=json.loads((ROOT/'reviews/weak_completion_2026_11_04/decay/INTERFACE.json').read_text());birth=[]
 for p in packet['parents']:
  if p['id'] not in ('S8_0','S3_0'):continue
  ms=by[p['id']]['mass']
  for c in p['channels']:
   if 'chi' not in c['daughters']:continue
   other=next((v for v in c['daughters'] if v!='chi'),'chi');mapping={'chi':'F1_1','lambda8':'F8_0','lambda2':'F3_0'};mo=by[mapping[other]]['mass'];E=(ms*ms+mchi*mchi-mo*mo)/(2*ms);birth.append(dict(parent=p['id'],daughters=c['daughters'],rest_chi_energy_mu=E,rest_chi_momentum_mu=math.sqrt(max(0,E*E-mchi*mchi)),width_mu=c['width_mu'],can_cross_Fc0_line=bool(E>parents[0]['chi_resonance_energy_mu'])))
 old=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/kinetics/run_hybrid_bw_001/result.json').read_text())['case'];stage=json.loads((ROOT/'reviews/collision_completion_2026_11_04/memory/run_stage001/result.json').read_text());split=json.loads((HERE.parent/'run_cold_split002/result.json').read_text());kernels=json.loads((HERE.parent/'run_late_kernels001/result.json').read_text());omega=kernels['omega'];N0=old['history'][0]['N'];Nend=old['history'][-1]['N'];T0=old['history'][0]['Tc_over_mu'];H0=old['history'][0]['H_over_oscillation']*omega;sscoef=2*math.pi**2/45*106.75/.02**3;rows=[];curves={};line=parents[0];pstar=line['pstar_mu'];ratio=line['spin_colour_ratio'];Gamma=line['partial_Gamma_Cchi_mu']
 inputs={'old_hybrid':([h['N'] for h in old['history']],[h['Y_charged'] for h in old['history']]),'memory_noelastic':([r['N'] for r in stage['rows']],[r['Y_charged'] for r in stage['rows']]),'memory_elastic':([N0]+[r['N'] for r in split['histories']['elastic']],[split['initial_charged_yield']]+[r['charged_yield'] for r in split['histories']['elastic']])}
 for name,(Ns,Ys) in inputs.items():
  Ns=np.array(Ns);Ys=np.array(Ys)
  def thermal(N):
   T=T0*np.exp(-(N-N0));H=H0*np.exp(-2*(N-N0));Y=np.interp(N,Ns,Ys);return sscoef*T**3*Y,H
  n,H=thermal(Ns);tau=2*math.pi**2*ratio*n*Gamma/(H*pstar**3);curves[name]=dict(N=Ns.tolist(),tau_line=tau.tolist());off=[]
  # Full redshift traversal; Eborn up to the complete neutral parent mass is conservative
  # for every boosted S8/S3 daughter in the fixed rest-parent cascade packet.
  for Nb in (N0,(N0+Nend)/2,Nend):
   for Eb in [v['rest_chi_energy_mu'] for v in birth]+[kernels['parent_mass']]:
    pborn=math.sqrt(max(0,Eb*Eb-mchi*mchi));Nline=Nb+math.log(pborn/line['chi_resonance_momentum_mu']) if pborn>line['chi_resonance_momentum_mu'] else None
    tauline=0
    if Nline is not None:
     nn,hh=thermal(Nline);tauline=2*math.pi**2*ratio*nn*Gamma/(hh*pstar**3)
    grid=np.linspace(Nb,Nb+16,10001);EE=np.sqrt(mchi*mchi+pborn*pborn*np.exp(-2*(grid-Nb)));nn,hh=thermal(grid);res=np.array([p['chi_resonance_energy_mu'] for p in parents]);delta=np.min(abs(EE[:,None]-res[None,:]),axis=1);u_min=res.min()+EE/(1+2*EE/MC);numer=MC+max(p['mass_mu'] for p in parents)+2*EE;h2bound=4*H2;amp=h2bound*EE*numer/MC*(1/np.maximum(delta,1e-300)+1/u_min);sigma=amp*amp/(8*math.pi*MC*MC);outside=delta>.1*line['chi_resonance_energy_mu'];integrand=np.where(outside,nn/hh*sigma,0.);tauoff=float(np.trapz(integrand,grid));off.append(dict(birth_N=Nb,birth_chi_energy_mu=Eb,line_crossing_N=Nline,line_crossing_within_saved_window=bool(Nline is not None and Nline<=Nend),narrow_line_tau=float(tauline),off_resonant_current_norm_bound_tau=tauoff,future_after_Nend_uses_conserved_comoving_C_upper_bound=bool(grid[-1]>Nend)))
  rows.append(dict(population=name,max_tau_line_saved_window=float(max(tau)),min_tau_line_saved_window=float(min(tau)),max_resonant_absorption_probability=float(-math.expm1(-max(tau))),Gamma_in_over_H_range=[float(Gamma/max(H)),float(Gamma/min(H))],paths=off))
 # Verify the inverse/decay spin factor and delta-function area numerically in a narrow BW window.
 nn=sscoef*T0**3*stage['initial_Y_charged'];HH=H0;M=parents[0]['mass_mu'];Gtotal=max(src['gauge_channels_total_over_mu'],Gamma);Mdec=8*math.pi*M*M*Gamma/pstar;gammaE=M*Gtotal/(2*MC);z,w=np.polynomial.legendre.leggauss(128);theta=z*math.atan(1000);E=line['chi_resonance_energy_mu']+gammaE*np.tan(theta);p2=E*E-mchi*mchi;numeric=nn*ratio*Mdec/(4*MC*MC*HH)*float(w@(1/p2))*math.atan(1000);pred=2*math.pi**2*ratio*nn*Gamma/(HH*pstar**3);bwrelative=abs(numeric/(pred*(2*math.atan(1000)/math.pi))-1);maxv2=0
 for f,T in ((2*np.array(stage['initial_fS']),T0),(2*np.array(stage['final_fS']),stage['rows'][-1]['Tc'])):
  e=np.array(stage['q_edges']);I=np.sum(f*(e[1:]**3-e[:-1]**3)/3);maxv2=max(maxv2,float(T*T/MC**2*np.sum(f*(e[1:]**5-e[:-1]**5)/5)/I))
 checks=dict(spin_ratio=bool(ratio==1),inverse_BW_area=bool(bwrelative<1e-8),hot_births_access_line=bool(all(v['can_cross_Fc0_line'] for v in birth)),higher_parents_inaccessible=bool(all(p['chi_resonance_energy_mu']>kernels['parent_mass'] for p in parents[1:])),NR_targets=bool(maxv2<1e-4),finite_opacity=bool(all(r['max_tau_line_saved_window']<.01 for r in rows)))
 Path(out).write_text(json.dumps(dict(parents=parents,neutral_birth_channels=birth,C_chi_yukawa_norm2_sum_per_C=H2,opacity_cases=rows,curves=curves,inverse_BW_area_relative_error=bwrelative,target_max_mean_v2=maxv2,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='ActualoldcoldCpopulation, exactcurrentpartialGammaF→Cχ andmatchedpolemass. Narrowlineintegratedabsorptiontau=2pi²gF/(gC gχ)nCΓin/(H pstar³), independenttotalwidth, verifiedBWarea. TargetDoppler/NRcorrectionsO(v²)reported. AllboostedS8/S3birthenergiescoveredbyuniformline-opacityupperenvelope, plusrestexamples. Offresonantelasticcurrentdiagramnormboundexcludeswide10%resonancebandalreadycoveredbylineestimate. Latehomogeneouscoldwindowonly; earlywarmχsurvivalnotassumed. FuturecolumnsconditionalonconservedcomovingCboundandfixedpole; nofullmediumopacityclaim.'),indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
