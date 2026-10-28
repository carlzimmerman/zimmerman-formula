#!/usr/bin/env python3
"""Fresh finite scalar audit of completed calibration primitive logs only."""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from classy import Class
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REB=ROOT/'rebuild_2026_10_22';CSM=HERE.parent
FILES=[HERE/'CALIBRATION_REVIEW_CRITERIA.md',HERE/'review_calibration_v2.py',
       REB/'F3_growth_audit/f3_growth_audit_results.json',REB/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json',
       ROOT/'real_research/derivation_chain_2026/FP0_core_postulates_results.json',
       REB/'X43_collapse_core_floor/x43_collapse_core_results.json',
       CSM/'calibration/calibrate_audited.py',REB/'EM1_emergent_dust_law/em1_emergent_results.json']
RESULTS=[CSM/'calibration'/n/'results.json' for n in ('run_003_audited','run_004_replay','run_005_MUTATE','run_008_exact_challenge')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 sourcefiles=[]
 for p in RESULTS:
  j=read(p)
  mf=read(p.parent/'manifest.json');sourcefiles.append(p.parent/'manifest.json')
  sourcefiles.extend(Path(a).resolve() for a in mf['command'] if isinstance(a,str) and a.endswith('.py') and Path(a).is_file())
  for e in j['levels'].values():
   for stream in ('own','basin','lens','pure'):
    for t in e[stream]['transforms']:
     sourcefiles.append(Path(t['source']))
 allfiles=sorted(set(FILES+RESULTS+sourcefiles));hashes={str(p.relative_to(ROOT)):sha(p) for p in allfiles}
 f3=read(FILES[2])['K2'];shapej=read(FILES[3])['cf_by_mass'];shape=[shapej[k] for k in ('1e+12','1e+13','1e+14')];fp=read(FILES[4])['numbers'];actuala0={'canonical':fp['a0_canonical'],'alt':fp['a0_rho_total']};rounded={'canonical':9.3603e-11,'alt':1.1312e-10};amp=4/(3*(3*math.log(2)-math.pi/2));q=lambda x:float(np.interp(x,[12.,13.,14.],shape))/shape[2]
 funcs={}
 for tag in ('A_c2b_refit','B_cfg886_bg'):
  p=f3[tag]['params'];cc=Class();cc.set({'omega_b':p['omega_b'],'omega_cdm':p['omega_cdm'],'h':p['h'],'ln10^{10}A_s':p['lnAs'],'n_s':p['n_s'],'tau_reio':p['tau'],'N_ur':3.044,'output':'mPk','P_k_max_h/Mpc':200.,'z_max_pk':10.});cc.compute();h=p['h'];rhom=float(cc.Omega_m())*2.775e11*h*h;k=np.logspace(-4,math.log10(150),3000);pk=np.array([cc.pk_lin(float(v*h),0) for v in k])*h**3;lg=np.linspace(7,16.5,191);s2=[]
  for x in lg:
   rr=(3*10**x/(4*math.pi*rhom))**(1/3)*h;kr=k*rr;win=3*(np.sin(kr)-kr*np.cos(kr))/kr**3;s2.append(float(np.trapz(k**3*pk*win**2/(2*math.pi**2),np.log(k))))
  zg=np.linspace(0,30,3001);dg=np.array([cc.scale_independent_growth_factor(float(z)) for z in zg]);dg/=dg[0]
  def sigma(x,rhom=rhom,s2=s2,dg=dg):
   d=1.686/(1.686+.974*math.sqrt(max(float(np.interp(x-math.log10(2),lg,s2))-float(np.interp(x,lg,s2)),0)));zf=float(np.interp(-d,-dg,zg)) if d<1 else 0;rho=18*math.pi**2*rhom*(1+zf)**3;return rho*(3*(10**x/2)/(4*math.pi*rho))**(1/3)/1e12
  funcs[tag]=sigma;cc.struct_cleanup();cc.empty()
 ss=sorted((math.log10(float(k)),math.log10(v[0])) for k,v in read(FILES[5])['sigma_coll_table'].items());sx,sy=np.array(ss).T
 def coarse(x):
  if x<sx[0]:return 10**(sy[0]+(sy[1]-sy[0])/(sx[1]-sx[0])*(x-sx[0]))
  if x>sx[-1]:return 10**(sy[-1]+(sy[-1]-sy[-2])/(sx[-1]-sx[-2])*(x-sx[-1]))
  return 10**float(np.interp(x,sx,sy))
 rel=read(FILES[7])['rows']['A_c2b_refit']['R1'];lmstar=10.;lmc=lmstar-.69*(lmstar-2*math.log10(.70/.679))+6.63;testlm=rel['a']+rel['b']*(math.log10(10**lmstar+10**lmc)-10)
 out=dict(input_sha256=hashes,checks={},records={});allerr=[];allfloor=[];allflag=[];allcore=[];baserr=[];basflag=[];normalwrap=0;mutwrap=0;baselines=[];source_exits=[];internal={};normal_controls=[];classified=[]
 def check(k,ok,d):out['checks'][k]=dict(pass_=bool(ok),detail=d);print(k,'PASS' if ok else 'FAIL',json.dumps(d,sort_keys=True),flush=True)
 for path in RESULTS:
  j=read(path);mut='MUTATE' in str(path);rec={};baselines.extend(j.get('baseline',{}).get('checks',{}).values())
  if not mut:normal_controls.extend(j['checks'].values())
  for lab,e in j['levels'].items():
   lev=float(lab);one={}
   if not mut:normal_controls.extend(v==0 if k=='decision_violations' else bool(v) for k,v in e['checks'].items())
   for stream in ('own','basin','lens','pure'):
    item=e[stream];err=[];flerr=[];flag=0;zeros=0;coreerr=[]
    for z in item['core_columns']:
     x=math.log10(z['mass']);f=z['footing'];eta=amp*(lev*q(x))**1.25
     if z['kind']=='x43':col=eta*funcs[z['tag']](x)*1.98847e30/3.0857e16**2;floor=actuala0[f]/(2*math.pi*6.67430e-11)
     else:col=eta*coarse(x);floor=rounded[f]*3.0857e16/1e6/(2*math.pi*4.30091e-3)
     if z['column']==0:zeros+=1;col=0
     else:err.append(abs(col/z['column']-1))
     flerr.append(abs(floor/z['floor']-1));flag+=int(bool(col>floor)!=z['expected'])
     if 'core' in z:coreerr.append(abs(max(col,floor)/z['core']-1))
    one[stream]=dict(columns=len(item['core_columns']),zero_eta_controls=zeros,max_relative_error=max(err,default=0),max_relative_floor_error=max(flerr,default=0),predicate_disagreements=flag,max_relative_core_error=max(coreerr,default=0));allerr+=err;allfloor+=flerr;allflag.append(flag);allcore+=coreerr
    wrap=sum(z['actual']!=z['expected'] for z in item['flags']);mutwrap+=wrap if mut else 0;normalwrap+=0 if mut else wrap;source_exits.extend(item['source_exits'])
    if stream in ('lens','pure'):ic=item['result'].get('_source_checks',{})
    else:ic=item['result'][0].get('checks',{})
    internal[str(path)+'|'+lab+'|'+stream]=ic
    if not mut:
     normal_controls.extend(z['status']==(0 if all(ic.values()) else 1) for z in item['source_exits'])
     for name,value in ic.items():
      reason=None
      if stream in ('own','basin') and name in ('K0','K0x38'):reason='Inherited old gas-budget or unconditional-floor-halo expected value'
      if stream=='lens' and name.startswith('K_T_truncation_'):
       foot=name.removeprefix('K_T_truncation_');testcol=amp*(lev*q(testlm))**1.25*coarse(testlm);testfloor=rounded[foot]*3.0857e16/1e6/(2*math.pi*4.30091e-3)
       if not testcol>testfloor:reason='Witness is law branch; old point-mass truncated-halo condition inapplicable'
      if reason:classified.append(dict(run=str(path.relative_to(ROOT)),L=lev,stream=stream,check=name,observed=value,reason=reason))
      else:normal_controls.append(value)
    for z in item['decisions']:
     for kind,masskey,corekey,flagkey in (('selected','Mselector','selected_core_SI','expected'),('own','Mown','own_core_SI','own_expected')):
      xx=math.log10(z[masskey]);ff=z['footing'];col=amp*(lev*q(xx))**1.25*funcs[z['tag']](xx)*1.98847e30/3.0857e16**2;floor=actuala0[ff]/(2*math.pi*6.67430e-11);baserr.append(abs(max(col,floor)/z[corekey]-1));basflag.append(bool(col>floor)==z[flagkey])
   rec[lab]=one
  out['records'][str(path.relative_to(ROOT))]=rec
 challenge=read(RESULTS[-1]);lev=float(next(iter(challenge['levels'])));ratio=amp*(lev*q(12.3))**1.25*funcs['A_c2b_refit'](12.3)*1.98847e30/3.0857e16**2/(actuala0['canonical']/(2*math.pi*6.67430e-11))
 check('K0_scalar_columns',max(allerr)<1e-10,dict(max_relative_error=max(allerr),n_positive_columns=len(allerr)))
 check('K1_actual_floors',max(allfloor)<1e-12,dict(max_relative_error=max(allfloor)))
 check('K2_direct_predicates',not any(allflag),dict(disagreements=sum(allflag)))
 check('K3_lens_max_core',max(allcore)<1e-12,dict(max_relative_error=max(allcore)))
 check('K4_basin_and_own_columns',max(baserr)<1e-10 and all(basflag),dict(max_relative_error=max(baserr),flag_disagreements=sum(not z for z in basflag),n_checks=len(basflag)))
 check('K5_actual_flag_mutant',normalwrap==0 and mutwrap>0,dict(normal_violations=normalwrap,mutant_violations=mutwrap))
 check('K6_baseline_controls',bool(baselines) and all(baselines),dict(n_old_comparisons=len(baselines)))
 check('K7_definition_corrected_challenge',abs(ratio-1)<1e-12,dict(L=lev,column_over_actual_floor_at_logM12_3=ratio))
 check('K8_inputs_stable',hashes=={str(p.relative_to(ROOT)):sha(p) for p in allfiles},'Declared artifacts unchanged')
 check('K9_normal_harness_controls',all(normal_controls),dict(n_controls=len(normal_controls),failed_count=sum(not v for v in normal_controls)))
 out['source_exits']=source_exits;out['internal_source_checks']=internal;out['inapplicable_legacy_controls']=classified;out['lens_KT_test_logM200']=testlm;out['scope']='Independent scalar reconstruction and code/record review of actual primitive columns; observational likelihood not independently rerun.'
 (args.output/'results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');n=sum(v['pass_'] for v in out['checks'].values());print(f'CSM1_CALIBRATION_REVIEW COMPLETE: {n}/{len(out["checks"])} checks PASS.');return 0 if n==len(out['checks']) else 1
if __name__=='__main__':raise SystemExit(main())
