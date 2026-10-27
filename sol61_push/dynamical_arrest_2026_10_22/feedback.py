import argparse,ast,json,csv,glob
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,solve_bvp,quad
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();p=Path('sol61_push/core_formation_transport_2026_10_22');prev=Path('sol61_push/compact_surplus_2026_10_22');en=json.loads((p/'run/result.json').read_text());old=json.loads((prev/'dwarf_run2/result.json').read_text())['rows'][0];tree=ast.parse((prev/'checks.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['interior','exterior']],type_ignores=[]),str(prev/'checks.py'),'exec'))
G,Msun,PC=6.674e-11,1.989e30,3.0857e16;a0=9.3603e-11;ellpc=440.4221297174536;nu=lambda y:1/(-np.expm1(-np.sqrt(np.maximum(y,1e-15))));L={}
for f in ['lvd_dwarf_mw.csv','lvd_dwarf_m31.csv','lvd_dwarf_local_field.csv']:
 for r in csv.DictReader(open('real_research/data/dsph/'+f)):L[r['name']]=r
base=Path('campaign_fresh_gravity');r27=json.loads((base/'CFG827_dwarf_age_sfh_ml/cfg827_results.json').read_text())['rows'];r24=json.loads((base/'CFG824_dwarf_age_fossil/cfg824_results.json').read_text())['rows'];r28=json.loads((base/'CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json').read_text())['canonical|nu_e']['rows'];unames=json.loads((base/'CFG859_extra_speed_vs_ufds/cfg859_results.json').read_text())['canonical|secondary (literature sigma)']['names']
def num(v):
 try:return float(v)
 except:return None
host=lambda nm:L[nm].get('host') or 'field';mw=[r['name'] for r in r28 if host(r['name'])=='mw' and r['delta']>.05];other=[r['name'] for r in r28 if host(r['name']) in ['m_031','field']]
Q={}
for line in open('real_research/data/SPARC_Lelli2016c.mrt'):
 v=line.split()
 if len(v)>=18 and v[1].isdigit():
  try:Q[v[0]]=dict(inc=float(v[5]),q=int(v[17]),Mb=(.5*float(v[7])+1.33*float(v[13]))*1e9)
  except ValueError:pass
checks=[];rows=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v)
ck('calibration_UFD_disjoint',not set(mw)&set(unames),sorted(set(mw)&set(unames)))
epseta=json.loads(Path('sol61_push/moving_core_population_2026_10_22/transport_run/result.json').read_text())['eta_rho_scale_max_99growth']
deformations=json.loads(Path('sol61_push/dynamical_arrest_2026_10_22/run2/result.json').read_text())['rotation']
for deformation in deformations:
 label='progenitor' if deformation['rot_fraction_initial']==0 else 'spin_'+str(deformation['rot_fraction_initial']);t=deformation['t'];row=en['canonical'];ins,_=interior(row['sc'],0,0,1e-11);R=row['R']
 def vals(x):
  q,s=ins.sol(x);z=q/x**2;y=(z+np.sqrt(z*z+4*z))/2;yp=(s-2*z/x)/(y*(2+y)/(1+y)**2)
  return y,y/(1+y),yp/(1+y)**2
 def mass(rpc):
  x=t*rpc/ellpc
  return row['m'] if x>=R else x*x*vals(x)[0]
 ck('mass_endpoint_'+label,abs(R*R*vals(R)[0]/row['m']-1)<1e-8,row['m'])
 summary={}
 for name,names in [('calibration',mw),('m31_field',other),('ufd',unames)]:
  es=[]
  for nm in names:
   d=L[nm];rh=4/3*(num(d.get('rhalf_sph_physical')) or num(d.get('rhalf_physical')));ups=2.2 if name=='ufd' else r27[nm]['ups'];so=num(d['vlos_sigma']) if name=='ufd' else r24[nm]['so'];mb=ups*10**(.4*(4.83-num(d['M_V'])));gn=G*mb/2*Msun/(rh*PC)**2;sl2=gn*nu(gn/a0)*rh*PC/3/1e6;sx2=a0*(ellpc*PC)**2*mass(rh)/(rh*PC)/3/1e6;es.append(np.log(so/np.sqrt(sl2+sx2)))
  summary[name]=dict(n=len(es),mean_log_sigma=float(np.mean(es)),se=float(np.std(es,ddof=1)/np.sqrt(len(es))),rms=float(np.sqrt(np.mean(np.array(es)**2))))
 ds=[]
 for fn in sorted(glob.glob('real_research/data/sparc_data/*_rotmod.dat')):
  nm=Path(fn).name.replace('_rotmod.dat','');g=Q.get(nm)
  if not g or g['q']>2 or g['inc']<30 or g['Mb']>3e9:continue
  vv=[]
  for line in open(fn):
   if line.startswith('#') or not line.strip():continue
   r,v,ev,vg,vd,vb=map(float,line.split()[:6])
   if v<=0 or r<=0 or ev/v>=.10:continue
   gb=(vg*abs(vg)+.5*vd*abs(vd)+.7*vb*abs(vb))*1e6/(r*1000*PC)
   if gb<=0:continue
   gl=gb*nu(gb/a0);go=v*v*1e6/(r*1000*PC);gx=a0*ellpc**2*mass(r*1000)/(r*1000)**2;vv.append(np.log10(go/(gl+gx)))
  if vv:ds.append(np.median(vv))
 summary['sparc']=dict(n=len(ds),mean_dex=float(np.mean(ds)),se=float(np.std(ds,ddof=1)/np.sqrt(len(ds))))
 ex=exterior(R,vals(R)[1],0,35,2e-8)
 jin=quad(lambda x:x*x*vals(x)[2]**2+2*vals(x)[1]**2,1e-10,R,epsabs=1e-11)[0]
 def fo(x):
  h,w=ex.sol(x);return x*x*(-2*w/x-h)**2+2*w*w
 jj=jin+quad(fo,R,R+35,epsabs=1e-11)[0];coef=t**3*jj/(3*row['m']);beta=1/(1+coef*epseta)
 fb=1/6.364;fc=1-fb;N0=-np.log(1101.);nf=-np.log(11.);ai=np.exp(N0)
 growth=[]
 for k in [.1,1]:
  def pre(N,Y):
   b,bp,c,cp=Y;S=1/(1+(k*.0004404221297174536/np.exp(N))**2);return[bp,-.5*bp+1.5*(fb*b+fc*c),cp,-.5*cp+1.5*(fb*b+fc*S*c)]
  sol=solve_ivp(pre,(N0,nf),[ai]*4,method='DOP853',rtol=1e-10,atol=1e-15);assert sol.success
  def post(N,Y):
   b,bp,c,cp=Y;gv=1.5*(fb*b+fc*c);return[bp,-.5*bp+gv,cp,-.5*cp+beta*gv]
  sol=solve_ivp(post,(nf,0),sol.y[:,-1],method='DOP853',rtol=1e-10,atol=1e-15);assert sol.success;growth.append(dict(k=k,amplitude=float(fb*sol.y[0,-1]+fc*sol.y[2,-1])))
 summary.update(label=label,mass_ratio=row['m']/en['canonical']['m'],edge_pc=R*ellpc/t,homology_t=t,rot_fraction_initial=deformation['rot_fraction_initial'],inertia_coefficient=coef,beta=beta,late_growth=growth);rows.append(summary)
 ck('coverage_'+label,[summary[n]['n'] for n in ['calibration','m31_field','ufd','sparc']]==[10,17,21,56],'unchanged samples')
 if label=='progenitor':
  err=max(abs(summary[n]['mean_log_sigma']-old[n]['mean_log_sigma']) for n in ['calibration','m31_field','ufd']);err=max(err,abs(summary['sparc']['mean_dex']-old['sparc']['mean_dex']));ck('predecessor_reproduced',err<1e-5,err)
out=dict(checks=checks,rows=rows,calibration_names=mw)
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
