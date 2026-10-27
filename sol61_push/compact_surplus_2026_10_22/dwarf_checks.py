import ast,argparse,json,csv,glob,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,solve_bvp,quad
from scipy.optimize import brentq,minimize_scalar
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);args=pa.parse_args()
p=Path('sol61_push/compact_surplus_2026_10_22');tree=ast.parse((p/'checks.py').read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['interior','exterior','one']];exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p/'checks.py'),'exec'))
G,Msun,PC=6.674e-11,1.989e30,3.0857e16;ellpc=440.4221297174536
L={}
for f in ['lvd_dwarf_mw.csv','lvd_dwarf_m31.csv','lvd_dwarf_local_field.csv']:
 for r in csv.DictReader(open('real_research/data/dsph/'+f)):L[r['name']]=r
base=Path('campaign_fresh_gravity')
r27=json.loads((base/'CFG827_dwarf_age_sfh_ml/cfg827_results.json').read_text())['rows'];r24=json.loads((base/'CFG824_dwarf_age_fossil/cfg824_results.json').read_text())['rows'];r28=json.loads((base/'CFG828_dwarf_excess_rotation_vs_dispersion/cfg828_results.json').read_text());r59=json.loads((base/'CFG859_extra_speed_vs_ufds/cfg859_results.json').read_text())
def num(v):
 try:return float(v)
 except:return None
nu=lambda y:1/(-np.expm1(-np.sqrt(np.maximum(y,1e-15))))
Q={}
for line in open('real_research/data/SPARC_Lelli2016c.mrt'):
 v=line.split()
 if len(v)>=18 and v[1].isdigit():
  try:Q[v[0]]=dict(inc=float(v[5]),q=int(v[17]),Mb=(.5*float(v[7])+1.33*float(v[13]))*1e9)
  except ValueError:pass
out=[];checks=[]
for foot,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
 def dwarf(nm,so,ups):
  r=L[nm];rh=4/3*(num(r.get('rhalf_sph_physical')) or num(r.get('rhalf_physical')));m=ups*10**(.4*(4.83-num(r['M_V'])));gn=G*m/2*Msun/(rh*PC)**2
  return (rh,so,gn*nu(gn/a0)*rh*PC/3/1e6)
 rows=r28[foot+'|nu_e']['rows'];host=lambda nm:L[nm].get('host') or 'field'
 mw=[dwarf(r['name'],r24[r['name']]['so'],r27[r['name']]['ups']) for r in rows if host(r['name'])=='mw' and r['delta']>.05]
 other=[dwarf(r['name'],r24[r['name']]['so'],r27[r['name']]['ups']) for r in rows if host(r['name']) in ['m_031','field']]
 ufd=[dwarf(nm,num(L[nm]['vlos_sigma']),2.2) for nm in r59[foot+'|secondary (literature sigma)']['names']]
 cache={}
 def model(logs):
  key=float(logs)
  if key not in cache:
   sc=np.exp(key);row=one(sc,0.,0.,2e-6,25);ins,_=interior(sc,0.,0.,2e-9);cache[key]=(row,ins)
  row,ins=cache[key]
  def mass(rpc):
   x=rpc/ellpc
   if x>=row['R']:return row['mass_c']
   q,s=ins.sol(x);z=q/x**2;y=(z+np.sqrt(z*z+4*z))/2;return x*x*y
  return row,mass
 def residual(items,logs):
  row,mass=model(logs)
  return np.array([np.log(so/np.sqrt(sl2+a0*(ellpc*PC)**2*mass(r)/(r*PC)/3/1e6)) for r,so,sl2 in items])
 fit=minimize_scalar(lambda logs:float(np.mean(residual(mw,logs)**2)),bounds=(np.log(.01),np.log(2.)),method='bounded',options={'xatol':2e-4})
 row,mass=model(fit.x);summary={}
 for name,items in [('calibration',mw),('m31_field',other),('ufd',ufd)]:
  e=residual(items,fit.x);summary[name]=dict(n=len(items),mean_log_sigma=float(e.mean()),se=float(e.std(ddof=1)/np.sqrt(len(e))),rms=float(np.sqrt(np.mean(e*e))),rms_law=float(np.sqrt(np.mean([np.log(so/np.sqrt(sl2))**2 for r,so,sl2 in items]))))
 ds=[];ds0=[]
 for fn in sorted(glob.glob('real_research/data/sparc_data/*_rotmod.dat')):
  nm=Path(fn).name.replace('_rotmod.dat','');g=Q.get(nm)
  if not g or g['q']>2 or g['inc']<30 or g['Mb']>3e9:continue
  vv=[];vv0=[]
  for line in open(fn):
   if line.startswith('#') or not line.strip():continue
   R,V,eV,Vg,Vd,Vb=map(float,line.split()[:6])
   if V<=0 or R<=0 or eV/V>=.10:continue
   gb=(Vg*abs(Vg)+.5*Vd*abs(Vd)+.7*Vb*abs(Vb))*1e6/(R*1000*PC)
   if gb<=0:continue
   gl=gb*nu(gb/a0);go=V*V*1e6/(R*1000*PC);gx=a0*ellpc**2*mass(R*1000)/(R*1000)**2
   vv.append(np.log10(go/(gl+gx)));vv0.append(np.log10(go/gl))
  if vv:ds.append(np.median(vv));ds0.append(np.median(vv0))
 summary['sparc']=dict(n=len(ds),mean_dex=float(np.mean(ds)),se=float(np.std(ds,ddof=1)/np.sqrt(len(ds))),law_mean_dex=float(np.mean(ds0)))
 summary.update(footing=foot,s_center=float(np.exp(fit.x)),mass_Msun=row['mass_c']*a0*(ellpc*PC)**2/G/Msun,edge_pc=row['R']*ellpc,optimizer_success=bool(fit.success),boundary_optimum=bool(abs(fit.x-np.log(.01))<.001 or abs(fit.x-np.log(2))<.001))
 out.append(summary);print(json.dumps(summary,indent=2),flush=True)
 checks.append(dict(name='coverage_'+foot,passed=[len(mw),len(other),len(ufd),len(ds)]==[10 if foot=='canonical' else 9,17,21,56]));checks.append(dict(name='interior_optimizer_'+foot,passed=bool(fit.success and not summary['boundary_optimum'])))
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(dict(checks=checks,rows=out),indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
