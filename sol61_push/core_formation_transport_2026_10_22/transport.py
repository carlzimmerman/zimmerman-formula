import argparse,json,csv,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import erf
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();here=Path('sol61_push/core_formation_transport_2026_10_22');prior=Path('sol61_push/moving_core_population_2026_10_22');dw=json.loads(Path('sol61_push/compact_surplus_2026_10_22/dwarf_run2/result.json').read_text())['rows'][0];pop=json.loads((prior/'run/result.json').read_text());tr=json.loads((prior/'transport_run/result.json').read_text());ene=json.loads((here/'run/result.json').read_text())
m=dw['mass_Msun'];rc=dw['edge_pc'];G=4.30091727e-3;pc_per_kms_Gyr=.00097779222168;F=erf(1)-2*np.exp(-1)/np.sqrt(np.pi);checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v)
ff=4/np.sqrt(np.pi)*quad(lambda x:x*x*np.exp(-x*x),0,1)[0];ck('Maxwell_fraction_integral',abs(F-ff)<1e-12,F)
examples=[]
for v,ri in [(10,1000),(20,1000),(30,3000),(200,10000),(1000,500000)]:
 bmin=max(2*rc,G*m/v**2);rf=max(3*bmin,10*G*m/v**2);ln=np.log(ri/bmin);naive=v*ri**2/(2*G*m*F*ln)*pc_per_kms_Gyr if ln>0 else None
 tim=quad(lambda r:v*r/(G*m*F*np.log(r/bmin)),rf,ri,epsabs=1e-9)[0]*pc_per_kms_Gyr if ri>rf else None
 examples.append(dict(Vc=v,rstart_pc=ri,bmin_pc=bmin,valid_stop_pc=rf,initial_mass_ratio=G*m/(v*v*ri),naive_constant_log_time_Gyr=naive,controlled_time_to_stop_Gyr=tim))
ck('declared_controlled_examples',sum(x['controlled_time_to_stop_Gyr'] is not None for x in examples)==3,'three valid outer intervals, two rejected')
L={}
for name in ['lvd_dwarf_mw.csv','lvd_dwarf_m31.csv','lvd_dwarf_local_field.csv']:
 for r in csv.DictReader(open('real_research/data/dsph/'+name)):L[r['name']]=r
root=Path('campaign_fresh_gravity');r24=json.loads((root/'CFG824_dwarf_age_fossil/cfg824_results.json').read_text())['rows'];r27=json.loads((root/'CFG827_dwarf_age_sfh_ml/cfg827_results.json').read_text())['rows'];r28=json.loads((root/'CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json').read_text())['canonical|nu_e']['rows']
def num(v):
 try:return float(v)
 except:return None
rows=[]
for r in r28:
 nm=r['name'];d=L[nm]
 if d.get('host')!='mw' or r['delta']<=.05:continue
 rh=4/3*(num(d.get('rhalf_sph_physical')) or num(d.get('rhalf_physical')));sig=r24[nm]['so'];ms=r27[nm]['ups']*10**(.4*(4.83-num(d['M_V'])));v=np.sqrt(3)*sig;mdyn=v*v*rh/G;bmin=max(2*rc,G*m/v**2);rf=max(3*bmin,10*G*m/v**2)
 heatratio=2*m/ms*np.log(3*rh/rc) if 3*rh>rc else None
 rows.append(dict(name=nm,rhalf_pc=rh,sigma_kms=sig,Mstar=ms,Mdyn_half=mdyn,core_to_enclosed_mass=m/mdyn,rhalf_over_two_rc=rh/(2*rc),valid_at_rhalf=bool(rh>rf),DeltaE_over_stellar_K=heatratio,max_stellar_fraction_for_10percent_K=min(1,.1/heatratio) if heatratio and heatratio>0 else None))
ck('dwarf_membership',len(rows)==10,len(rows))
vesc2=2*G*m/rc;caps=[]
for v in [10,20,100,1000]:caps.append(dict(v_inf=v,minimum_loss_fraction_for_bound_pair=v*v/(v*v+vesc2),focusing_factor=1+vesc2/v**2,incoming_orbital_energy_per_total_mass_kms2=v*v/8,static_merge_export_per_total_mass_kms2=v*v/8+ene['merger_release_per_initial_total_mass_kms2']))
ck('capture_ordering',all(caps[i]['minimum_loss_fraction_for_bound_pair']<caps[i+1]['minimum_loss_fraction_for_bound_pair'] for i in range(3)),caps)
ellpc=440.4221297174536;pc=3.085677581491367e16;a0=9.3603e-11;eps=tr['eta_rho_scale_max_99growth'];omega=np.sqrt(a0/(ellpc*pc)/eps);cL=np.sqrt(a0*ellpc*pc/eps)/1e3;Myr=31557600e6;omegadyn=np.sqrt(G*m/rc**3)*1e3/pc
waves=dict(eta_rho_scale=eps,gap_omega_per_Myr=omega*Myr,core_omega_per_Myr=omegadyn*Myr,core_frequency_over_gap=omegadyn/omega,longitudinal_speed_kms=cL,passage_frequency_over_gap={str(v):v*1e3/(rc*pc)/omega for v in [10,20,100,1000]},eta_rho_scale_for_cL_1000kms=a0*ellpc*pc/1e12)
ck('gap_core_ratio',waves['core_frequency_over_gap']<1,waves)
cl=pop['clusters'][0];N=cl['N_median'];M=cl['mass_median'];b=cl['b_median_Mpc']*1e6;vc=np.sqrt(G*M/b);tcross=b/vc*pc_per_kms_Gyr;relax=.1*N/np.log(N)*tcross
ck('cluster_gravity_relaxation_slow',relax>1e4,relax)
out=dict(checks=checks,examples=examples,dwarfs=rows,capture=caps,vescape_contact_kms=np.sqrt(vesc2),waves=waves,cluster_crossing_Gyr=tcross,cluster_relaxation_estimate_Gyr=relax,df_coefficient=1/(2*F),non_claims=['No equal-mass friction-only model','No gas drag transferred from collisionless formula','No predicted orbit history or deposition fraction','No full-action capture rate'])
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
