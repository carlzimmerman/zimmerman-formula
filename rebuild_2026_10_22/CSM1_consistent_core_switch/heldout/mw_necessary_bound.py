#!/usr/bin/env python3
"""Fixed-box radial-speed necessary relaxation; not a new model grade."""
import ast,hashlib,json,math,os,platform,resource,sys,time
from pathlib import Path
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS'):os.environ[k]='1'
import numpy as np
import scipy
from scipy.optimize import brentq,minimize_scalar
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REB=ROOT/'rebuild_2026_10_22';OUT=HERE/'mw_bound_001';OUT.mkdir(exist_ok=True)
START=time.time();inputs={}
def rd(p):
 s=p.read_bytes();inputs[str(p.relative_to(ROOT))]=hashlib.sha256(s).hexdigest();return s.decode()
def ld(p):return json.loads(rd(p))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rd(Path(__file__).resolve());rd(HERE/'MW_NECESSARY_BOUND_PROTOCOL.md');rd(HERE/'MW_BURKERT_MONOTONICITY.md')
base=ld(HERE/'run_006_final/baseline.json');res=ld(HERE/'run_006_final/results.json');tab=ld(HERE/'run_006_final/sigma_table.json')
gd2=rd(REB/'GD2_route_e_mw_x5_box/gd2_x5_box.py');xl=rd(REB/'X5_mw_joint_baryons/x5_lib.py');p4=rd(REB/'P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py')
ns=dict(np=np,math=math,brentq=brentq,minimize_scalar=minimize_scalar)
t=ast.parse(gd2);exec(compile(ast.Module(body=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in ('B','solve_r0')],type_ignores=[]),'gd2_scalar_functions','exec'),ns)
G=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='G' for x in n.targets))
floors=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='SIG_A0' for x in n.targets));floors={f:v/1e6 for f,v in floors.items()}
R0=next(ast.literal_eval(n.value) for n in ast.parse(p4).body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='R0_MW' for x in n.targets))
xt=ast.parse(xl);vc,half=next(ast.literal_eval(n.value) for n in xt.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Tuple) and any(isinstance(v,ast.Name) and v.id=='VC_BRIEF' for v in x.elts) for x in n.targets))
# The authoritative P4 formula for the second L1 interval is parsed from the
# original Eilers data with the same hypotenuse error convention.
epath=ROOT/'real_research/data/mw_rc_eilers2019_table1.tsv';rd(epath);d=np.genfromtxt(epath,names=True,comments='#',skip_header=10)
# Header discovery avoids depending on the descriptive comment count.
lines=epath.read_text().splitlines();ix=next(i for i,l in enumerate(lines) if l.startswith('R_kpc\t'));d=np.genfromtxt(epath,names=True,skip_header=ix)
vE=float(np.interp(R0,d['R_kpc'],d['vc_kms']));eE=float(np.interp(R0,d['R_kpc'],np.hypot(.5*(d['sig_minus']+d['sig_plus']),.02*d['vc_kms'])))
cut=max(vc-half,vE-2*eE);upper=min(vc+half,vE+2*eE)
f3=ld(REB/'F3_growth_audit/f3_growth_audit_results.json');h=f3['K2']['A_c2b_refit']['params']['h'];rc=3*(100*h/1e3)**2/(8*math.pi*G)
S9=ld(REB/'X48_native_cf_zoom/x48_analyze_results_ng48_A2.json')['cf_by_mass'];S9=[S9[k] for k in ('1e+12','1e+13','1e+14')];B1=3*math.log(2)-math.pi/2
cells=base['mw']['cells'];assert len(cells)==175
siggrid=next(ast.literal_eval(n.value) for n in xt.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='SIG_B_GRID' for x in n.targets));mbbgrid=next(ast.literal_eval(n.value) for n in xt.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='MBB_GRID' for x in n.targets))
assert len({(c['sig_b'],c['M_bb'],c['R_d']) for c in cells})==175
assert set(c['sig_b'] for c in cells)==set(siggrid) and set(c['M_bb'] for c in cells)==set(mbbgrid) and len(set(c['R_d'] for c in cells))==7
B=ns['B'];solve=ns['solve_r0'];xpk=brentq(lambda x:4*x**3/((1+x)*(1+x*x)*float(B(x)))-2,.001,100.)
def owncol(L,M):return 4/(3*B1)*(L*float(np.interp(math.log10(M),[12.,13.,14.],S9))/S9[2])**1.25*10**float(np.interp(math.log10(M),tab['lg'],tab['lsc']['A_c2b_refit']))
def halo(M,R,Sigma):
 r0,sat=solve(M,R,Sigma*1e6);mass=math.pi*Sigma*1e6*r0*r0*float(B(R0/r0));return dict(v2=G*mass/R0,r0=r0,saturated=sat,M_R=math.pi*Sigma*1e6*r0*r0*float(B(R/r0)))
rows=[];max_replay=0.;max_baryon_foot=0.
for i,c in enumerate(cells):
 row=dict(index=i,sig_b=c['sig_b'],M_bb=c['M_bb'],R_d=c['R_d'],Mb=c['Mb'],footings={});vs=[]
 for f in ('canonical','alt'):
  a=c['rows'][f+'|A_c2b_refit'];M=10**a['lgM200'];R=(3*M/(4*math.pi*200*rc))**(1/3);assert R0<R
  hb=halo(M,R,a['Sig_ratio']*floors[f]);vb2=a['vc_R0']**2-hb['v2'];assert vb2>0;vs.append(vb2)
  hp=halo(M,R,floors[f]);floorvc=math.sqrt(vb2+hp['v2'])
  vals={}
  for L in (3.75,3.9,4.):
   z=halo(M,R,max(floors[f],owncol(L,M)));v=math.sqrt(vb2+z['v2']);target=res['levels'][str(L)]['mw']['cells'][i]['rows'][f+'|A_c2b_refit']['vc_R0'];max_replay=max(max_replay,abs(v-target));vals[str(L)]=v
  row['footings'][f]=dict(M200=M,R200=R,Vb_R0=math.sqrt(vb2),floor_Vc=floorvc,floor_r0=hp['r0'],floor_saturated=hp['saturated'],floor_mass_fraction=hp['M_R']/M,registered_Vc=vals)
 max_baryon_foot=max(max_baryon_foot,abs(vs[0]-vs[1]));rows.append(row)
assert max_replay<1e-8 and max_baryon_foot<1e-7
summary={}
for f in ('canonical','alt'):
 winner=max(rows,key=lambda r:r['footings'][f]['floor_Vc']);mx=winner['footings'][f]['floor_Vc'];assert mx>=cut
 summary[f]=dict(necessary_L_lower_bound=0.,positive_envelope_root_exists=False,reason='L=0 floor-only relaxed halo already exceeds L1 lower speed at some frozen box cells; requested maximum-speed relaxation is vacuous.',max_floor_Vc=mx,winner=winner,number_floor_above_L1_lower=sum(r['footings'][f]['floor_Vc']>=cut for r in rows),number_floor_inside_L1_interval=sum(cut<=r['footings'][f]['floor_Vc']<=upper for r in rows))
oldho2=ld(REB/'HO2_sluggs_milkyway_heldout/ho2_heldout_results.json')
result=dict(checkpoint='CSM1_MW_NECESSARY_BOUND',status='vacuous necessary bound',protocol_sha256=inputs[str((HERE/'MW_NECESSARY_BOUND_PROTOCOL.md').relative_to(ROOT))],frozen_cut=dict(R0_kpc=R0,brief=[vc-half,vc+half],Eilers=[vE-2*eE,vE+2*eE],L1_intersection=[cut,upper],Eilers_central=vE,Eilers_error=eE),summary=summary,checks=dict(finite_box_count=len(rows),registered_speed_max_abs_residual_kms=max_replay,baryonic_v2_max_footing_disagreement=max_baryon_foot,min_R200_kpc=min(r['footings']['canonical']['R200'] for r in rows),xpk=xpk,pk_within_bounded_minimization=1e-3<1/xpk<1e3,all_floor_roots_within_compact_bracket=all(1e-7<r['footings'][f]['floor_r0']/r['footings'][f]['R200']<=1/xpk*(1+1e-6) for r in rows for f in ('canonical','alt')),all_floor_unsaturated=all(not r['footings'][f]['floor_saturated'] for r in rows for f in ('canonical','alt'))),carried_old_law_branch=dict(source='HO2 original, own-mass switch field path; not a new grade',box={f:oldho2['mw']['box'][f+'|A_c2b_refit'] for f in ('canonical','alt')}),non_claims=['No nonzero necessary lower L bound follows from the requested max-speed relaxation.','This does not assert any L=0 cell passes the full L1+Kz+outer-rotation tests.','Forcing halos on relaxes the LG branch, so cannot establish actual low-L feasibility.','Fixed finite baryonic box only; no larger baryonic family bound.'],rows=rows,input_sha256=inputs)
(OUT/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
resources=dict(runtime_seconds=time.time()-START,peak_RSS_GB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9);(OUT/'resources.json').write_text(json.dumps(resources,indent=2,sort_keys=True)+'\n')
manifest=dict(schema_version=2,claim_id='CSM1_MW_NECESSARY_BOUND',repository=dict(commit='2c6b17d683c1a69a1c95754c255de1cc6f79800a',dirty=True),command=[sys.executable,'-I',str(Path(__file__).resolve())],environment=dict(software=[dict(name='Python',version=platform.python_version()),dict(name='numpy',version=np.__version__),dict(name='scipy',version=scipy.__version__)],hardware=platform.platform()),mathematics=dict(assertion_tested='Evaluate relaxed forced-halo floor-only maximum radial speed over all175 fixed MW cells against actual frozen L1 lower cut; verify reconstruction at registered levels.',coefficient_domain='float64',conventions='Same GD2 compact root/saturation, native floor, spherical radial force; exact analytic monotonic proof separate.',inputs=['validated175-cell baryonic observables reconstructed from prior totalVc and exact baseline halo'],bounds=dict(cells=175,background='A_c2b_refit',footings=['canonical','alt'],L_checks=[0,3.75,3.9,4.]),non_claims=result['non_claims']),randomness=dict(used=False,generator='',seed=None),run=dict(started_at=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(START)),runtime_seconds=time.time()-START,exit_status=0,status='completed',resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=1)),outputs=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p),kind='result') for p in (OUT/'results.json',OUT/'resources.json')],checks=[],result='Requested necessary lower bound is L>=0 only; no positive root.',residual_risks=result['non_claims'],input_artifacts=[dict(path=p,sha256=v,sha256_after=sha(ROOT/p)) for p,v in sorted(inputs.items())],declared_results=[str((OUT/n).relative_to(ROOT)) for n in ('results.json','resources.json')])
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps(dict(summary={f:{k:v for k,v in x.items() if k!='winner'} for f,x in summary.items()},checks=result['checks'],cut=result['frozen_cut'],resources=resources),indent=2))
