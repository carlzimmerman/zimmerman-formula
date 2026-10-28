"""Independent CLASS/EPS and table audit of actual numeric columns reaching corrected scorer decisions."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import pathlib,json,math,argparse,hashlib,time,resource,sys
import numpy as np
from classy import Class
AP=argparse.ArgumentParser();AP.add_argument('--runs',nargs='+',required=True);AP.add_argument('--output',required=True);args=AP.parse_args();D=pathlib.Path(__file__).resolve().parent;ROOT=D.parents[2];REB=ROOT/'rebuild_2026_10_22';T0=time.time();H={}
def rd(p):
 p=pathlib.Path(p).resolve();H[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
F=rd(REB/'F3_growth_audit/f3_growth_audit_results.json')['K2'];S=rd(REB/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json')['cf_by_mass'];T=rd(REB/'X43_collapse_core_floor/x43_collapse_core_results.json')['sigma_coll_table'];S9=[S[k] for k in ('1e+12','1e+13','1e+14')];COL={};params={}
for tag,v in F.items():
 if tag not in ('A_c2b_refit','B_cfg886_bg'):continue
 p=v['params'];cc=Class();cfg={'omega_b':p['omega_b'],'omega_cdm':p['omega_cdm'],'h':p['h'],'ln10^{10}A_s':p['lnAs'],'n_s':p['n_s'],'tau_reio':p['tau'],'N_ur':3.044,'output':'mPk','P_k_max_h/Mpc':200.,'z_max_pk':10.};cc.set(cfg);cc.compute();params[tag]=cfg
 h=p['h'];rho=float(cc.Omega_m())*2.775e11*h*h;k=np.logspace(-4,math.log10(150),3000);power=np.array([cc.pk_lin(float(q*h),0) for q in k])*h**3;lm=np.linspace(7,16.5,191);s2=[]
 for l in lm:
  kr=k*(3*10**l/(4*math.pi*rho))**(1/3)*h;w=3*(np.sin(kr)-kr*np.cos(kr))/kr**3;s2.append(float(np.trapz(k**3*power*w*w/(2*math.pi**2),np.log(k))))
 zg=np.linspace(0,30,3001);growth=np.array([cc.scale_independent_growth_factor(float(z)) for z in zg]);growth/=growth[0];cc.struct_cleanup();cc.empty();COL[tag]=(rho,lm,np.asarray(s2),zg,growth)
def collapse(tag,m):
 rho,lm,s2,zg,growth=COL[tag];l=math.log10(m);half=float(np.interp(l-math.log10(2),lm,s2));full=float(np.interp(l,lm,s2));df=1.686/(1.686+.974*math.sqrt(max(half-full,0)));zf=float(np.interp(-df,-growth,zg)) if df<1 else 0.;rhof=18*math.pi**2*rho*(1+zf)**3;rf=(3*(m/2)/(4*math.pi*rhof))**(1/3);return rhof*rf/1e12
TL=sorted((math.log10(float(k)),math.log10(v[0])) for k,v in T.items());XL,YL=map(np.array,zip(*TL))
def table(m):
 l=math.log10(m)
 if l<XL[0]:return 10**(YL[0]+(YL[1]-YL[0])/(XL[1]-XL[0])*(l-XL[0]))
 if l>XL[-1]:return 10**(YL[-1]+(YL[-1]-YL[-2])/(XL[-1]-XL[-2])*(l-XL[-1]))
 return 10**float(np.interp(l,XL,YL))
FP=rd(ROOT/'real_research/derivation_chain_2026/FP0_core_postulates_results.json')['numbers'];A0X={'canonical':FP['a0_canonical'],'alt':FP['a0_rho_total']};A0={'canonical':9.3603e-11,'alt':1.1312e-10};b1=3*math.log(2)-math.pi/2;results={}
for rp in args.runs:
 r=rd(rp);bi=rd(pathlib.Path(rp).parent/'basin_inputs.json')['basins'];res={}
 for lev,v in r['levels'].items():
  L=float(lev);out={}
  for key in ('own','basin','lens','pure'):
   vals=v[key].get('core_columns',[]);errs=[];fe=[];bad=[];masses=[]
   for q in vals:
    m=q['mass'];eta=4/(3*b1)*(L*float(np.interp(math.log10(m),[12,13,14],S9))/S9[2])**1.25
    if q['kind']=='x43':col=eta*collapse(q['tag'],m)*1.98847e30/3.0857e16**2;floor=A0X[q['footing']]/(2*math.pi*6.67430e-11)
    else:col=eta*table(m);floor=A0[q['footing']]*3.0857e16/1e6/(2*math.pi*4.30091e-3)
    err=abs(col/q['column']-1) if q['column'] else 0.;col=col if q['column'] else 0.;fer=abs(floor/q['floor']-1);errs.append(err);fe.append(fer);masses.append(m)
    if bool(col>floor)!=q['expected']:bad.append(dict(q=q,independent_column=col,independent_floor=floor))
   out[key]=dict(n_columns=len(vals),zero_eta_inherited_control_records=sum(q['column']==0 for q in vals),max_relative_column_error=max(errs or [0]),max_relative_floor_error=max(fe or [0]),flag_disagreements=len(bad),disagreements=bad[:4],min_mass=min(masses or [0]),max_mass=max(masses or [0]),pass_=bool(vals) and max(errs)<1e-10 and max(fe)<1e-12 and not bad)
  for key in ('own','basin'):
   ds=v[key]['decisions'];badmass=[]
   for q in ds:
    expected=bi[q['tag']].get(q['name'],q['Mown']) if key=='basin' else q['Mown']
    if q['Mselector']!=expected:badmass.append(q['name'])
   out[key]['selected_mass_disagreements']=len(badmass);out[key]['selected_mass_records']=len(ds);out[key]['pass_']=out[key]['pass_'] and not badmass and len(ds)==700
  res[lev]=out
 results[str(pathlib.Path(rp).resolve())]=res
out=pathlib.Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True);z=dict(assertion_tested='Actual numeric X43/X53 core columns and direct inequalities agree with independently implemented CLASS/EPS or retained coarse-table arithmetic at every recorded mass on both backgrounds/footings',results=results,all_pass=all(x['pass_'] for a in results.values() for b in a.values() for x in b.values()),runtime_seconds=time.time()-T0,rss_GB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform=='darwin' else 1e6),input_hashes={p:dict(before=h,after=hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()) for p,h in H.items()},class_params=params)
(out/'results.json').write_text(json.dumps(z,indent=2)+'\n');print(json.dumps(z,indent=2));sys.exit(0 if z['all_pass'] else 1)
