#!/usr/bin/env python3
"""Independent final raw-heldout arithmetic/classification check; no fits."""
import ast,hashlib,json,math,os,platform,resource,sys,time
from pathlib import Path
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import numpy as np
import scipy
from scipy.stats import chi2
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];REB=ROOT/'rebuild_2026_10_22';START=time.time();PIN={}
def rd(p):
 data=p.read_bytes();PIN[str(p.relative_to(ROOT))]=hashlib.sha256(data).hexdigest();return data.decode()
def ld(p):return json.loads(rd(p))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rd(Path(__file__).resolve());rd(HERE/'FINAL_REVIEW_PROTOCOL.md')
primary=ld(HERE/'run_006_final/results.json');challenge=ld(HERE/'run_011_challenge_actual_floor/results.json');coordinator=ld(HERE.parent/'reconciliation_001/results.json');rd(HERE.parent/'reconcile.py')
levels=dict(primary['levels']);level='2.5090648745652686';levels[level]=challenge['levels'][level]
xs=rd(REB/'X51_dwarf_cooling_floor/x51_dwarfs.py');xl=rd(REB/'X5_mw_joint_baryons/x5_lib.py');gd=rd(REB/'GD2_route_e_mw_x5_box/gd2_x5_box.py');p4=rd(REB/'P4_v3_galaxy_tiles/p4_v3_galaxy_tiles.py')
ns={'np':np};xt=ast.parse(xs);exec(compile(ast.Module(body=[n for n in xt.body if isinstance(n,ast.FunctionDef) and n.name=='boot'],type_ignores=[]),'original_X51_boot','exec'),ns)
# Extract literal frozen scalar cuts from their actual source assignments.
constants={}
for source in (xl,gd):
 for n in ast.parse(source).body:
  if isinstance(n,ast.Assign):
   try:val=ast.literal_eval(n.value)
   except (ValueError,TypeError):
    if isinstance(n.value,ast.Tuple):
     for target in n.targets:
      if isinstance(target,ast.Tuple):
       for name,expr in zip(target.elts,n.value.elts):
        if isinstance(name,ast.Name):
         try:constants[name.id]=ast.literal_eval(expr)
         except (ValueError,TypeError):pass
    continue
   for target in n.targets:
    if isinstance(target,ast.Name):constants[target.id]=val
    elif isinstance(target,ast.Tuple):
     for name,value in zip(target.elts,val):
      if isinstance(name,ast.Name):constants[name.id]=value
s=p4[p4.index('R0_MW = 8.122'):p4.index('def rho_mcm(R, z):')];pn={'math':math};exec(compile(s,'original_P4_family_constants','exec'),pn)
R0=pn['R0_MW'];ep=ROOT/'real_research/data/mw_rc_eilers2019_table1.tsv';text=rd(ep);ix=next(i for i,l in enumerate(text.splitlines()) if l.startswith('R_kpc\t'));d=np.genfromtxt(ep,names=True,skip_header=ix)
vE=float(np.interp(R0,d['R_kpc'],d['vc_kms']));eE=float(np.interp(R0,d['R_kpc'],np.hypot(.5*(d['sig_minus']+d['sig_plus']),.02*d['vc_kms'])))
cuts=dict(VC_BRIEF=constants['VC_BRIEF'],VC_BRIEF_LINE=constants['VC_BRIEF_LINE'],Eilers_V=vE,Eilers_error=eE,KZ_BR=constants['KZ_BR'],KZ_BR_E=constants['KZ_BR_E'],LINE_KZ=float(chi2.ppf(.99,43)),LINE_OU=constants['LINE_OU'],Rd_prior=list(constants['RD_TAG']),Mstar_prior=list(constants['MSTAR_TAG']),R0_kpc=R0)
# Both stellar discs have the same R_d and their normalization fractions sum
# to one. Thus Mstar=2pi(Sigma_b-gas_at_R0)exp(R0/Rd)Rd²+M_bb, directly from Family.params.
gas=pn['S0_HI']*math.exp(-4/R0-R0/7)+pn['S0_H2']*math.exp(-12/R0-R0/1.5)
def lines(row):return {'L1':abs(row['vc_R0']-cuts['VC_BRIEF'])<=cuts['VC_BRIEF_LINE'] and abs(row['vc_R0']-vE)<=2*eE,'L2a':row['chi2_Kz']<=cuts['LINE_KZ'],'L2b':abs(row['K_R0']-cuts['KZ_BR'])<=2*cuts['KZ_BR_E'],'L3':row['chi2_Ou']<=cuts['LINE_OU']}
classes=('MW ultra-faint','bright M31','M31 others','MW classical','LG field');bads=[];nclass=0;nline=0;nbox=0;nextract=0;maxerr=0.;detail={}
for L,x in levels.items():
 detail[L]={}
 for foot in ('canonical','alt'):
  rr=x['dwarfs']['rows'][foot];rng=np.random.default_rng(20261026);cs={}
  for cl in classes:
   q=[z for z in rr if z['cls']==cl];median,sd=ns['boot'](np.array([z['E'] for z in q]),np.array([z['s'] for z in q]),rng);ref=x['dwarfs']['footings'][foot]['classes'][cl];Z=median/sd
   for k,v in [('median',median),('sd',sd),('Z',Z)]:
    err=abs(v-ref[k]);maxerr=max(maxerr,err)
    if err>1e-12:bads.append([L,foot,cl,k,v,ref[k]])
   if len(q)!=ref['N']:bads.append([L,foot,cl,'N',len(q),ref['N']])
   if abs(Z-coordinator['details'][L][foot]['dwarfs']['class_Z'][cl])>1e-12:bads.append([L,foot,cl,'coordinator_Z'])
   nclass+=1;cs[cl]=dict(N=len(q),median=median,sd=sd,Z=Z)
  mw={}
  for bg in ('A_c2b_refit','B_cfg886_bg'):
   key=foot+'|'+bg;computed=[]
   for cell in x['mw']['cells']:
    row=cell['rows'][key];calc=lines(row);computed.append((cell,calc))
    for k,v in calc.items():
     nline+=1
     if bool(v)!=bool(row[k]):bads.append([L,key,k,'cell_line'])
   mc=x['mw']['mcmillan']['rows'][key];mcl=lines(mc)
   for k,v in mcl.items():
    nline+=1
    if bool(v)!=bool(mc[k]):bads.append([L,key,k,'McMillan_line'])
   vk=[cell for cell,l in computed if all(l[k] for k in ('L1','L2a','L2b'))];allpass=[cell for cell,l in computed if all(l.values())];inprior=[]
   for cell in allpass:
    star=2*math.pi*(cell['sig_b']*1e6-gas)*math.exp(R0/cell['R_d'])*cell['R_d']**2+cell['M_bb']
    if constants['RD_TAG'][0]<=cell['R_d']<=constants['RD_TAG'][1] and constants['MSTAR_TAG'][0]<=star<=constants['MSTAR_TAG'][1]:inprior.append(cell)
   cls='FEASIBLE IN PRIORS' if inprior else 'FEASIBLE (WIDE PRIORS ONLY)' if allpass else 'V+K ONLY' if vk else 'INFEASIBLE';box=x['mw']['box'][key]
   if cls!=box['cls']:bads.append([L,key,'classification',cls,box['cls']])
   nbox+=1
   coord=coordinator['details'][L][foot]['mw'][bg]
   if coord['VK_count']!=len(vk) or coord['all_four_count']!=len(allpass) or coord['classification']!=cls or coord['McMillan_lines']!=mcl:bads.append([L,key,'coordinator_MW_extraction'])
   nextract+=1;mw[bg]=dict(VK_count=len(vk),all_four_count=len(allpass),classification=cls,McMillan_lines=mcl)
  detail[L][foot]=dict(classes=cs,mw=mw)
checks=dict(four_levels=len(levels)==4,class_summaries_40=nclass==40,primitive_lines_11264=nline==11264,classifications_16=nbox==16,coordinator_MW_extractions_16=nextract==16,no_mismatches=not bads,inputs_stable=all(sha(ROOT/p)==v for p,v in PIN.items()))
result=dict(scope='Independent raw-heldout final check; source-specific parent/dwarf profiles; no fitting or new candidate.',checks=checks,counts=dict(class_summaries=nclass,primitive_MW_line_decisions=nline,MW_box_classifications=nbox,coordinator_MW_extractions=nextract),max_abs_class_stat_difference=maxerr,exact_cuts=cuts,mismatches=bads,details=detail,input_sha256=PIN,prose_scope='MODEL parent formula and X51 dwarf-profile exception are distinct. Markdown background/aggregate wording handled by coordinator; these checks do not certify later prose revisions.')
output=HERE/'FINAL_REVIEW.json';output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');code=0 if all(checks.values()) else 1
manifest=dict(schema_version=2,claim_id='CSM1_FINAL_RAW_HELDOUT_REVIEW',repository=dict(commit='2c6b17d683c1a69a1c95754c255de1cc6f79800a',dirty=True),command=[sys.executable,'-I',str(Path(__file__).resolve())],environment=dict(software=[dict(name='Python',version=platform.python_version()),dict(name='numpy',version=np.__version__),dict(name='scipy',version=scipy.__version__)],hardware=platform.platform()),mathematics=dict(assertion_tested='Recompute40classbootstrap summaries,11264primitive MWline decisions,16classifications and coordinator extraction against original cuts.',coefficient_domain='float64',conventions='Original X51 boot seed/order; native X5/GD2 cuts and P4 family prior tags.',inputs=['Authoritative heldout primary/challenge and coordinator reconciliation primitives'],bounds=dict(levels=[float(v) for v in levels],footings=['canonical','alt'],backgrounds=['A_c2b_refit','B_cfg886_bg'],box_cells=175),non_claims=['Does not validate inherited astrophysical assumptions.','Does not assert source-independent universal halo/dwarf profile.','Does not change grades or fit a parameter.']),randomness=dict(used=True,generator='numpy PCG64',seed=20261026),run=dict(started_at=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(START)),runtime_seconds=time.time()-START,exit_status=code,status='completed' if code==0 else 'failed',resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=1),observed_peak_RSS_GB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9),outputs=[dict(path=str(output.relative_to(ROOT)),sha256=sha(output),kind='result')],checks=[dict(name=k,pass_=v) for k,v in checks.items()],result='All independent raw-heldout and extraction checks pass' if code==0 else 'Mismatch found',residual_risks=['Same original numerical library/bootstrap conventions; no physical validation.'],input_artifacts=[dict(path=p,sha256=v,sha256_after=sha(ROOT/p)) for p,v in sorted(PIN.items())],declared_results=[str(output.relative_to(ROOT))])
(HERE/'FINAL_REVIEW_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps(dict(checks=checks,counts=result['counts'],max_abs_class_stat_difference=maxerr,mismatches=bads),indent=2));sys.exit(code)
