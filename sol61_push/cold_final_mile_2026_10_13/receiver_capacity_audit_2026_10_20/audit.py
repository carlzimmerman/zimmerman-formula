"""Independent reported-only stellar guard, not a source rerun or frozen regrade."""
from pathlib import Path
import ast,json,hashlib,math,subprocess,sys,resource,time
import numpy as np
R=Path('/Users/carlzimmerman/new_physics/zimmerman-formula');S=R/'campaign_fresh_gravity/CFG918_dwarf_receiver_capacity';source=(S/'cfg918.py').read_text();d=json.loads((S/'cfg918_results.json').read_text());paths=[S/n for n in ['cfg918.py','cfg918_results.json','FROZEN_CRITERIA.md','README.md','cfg918_results_REFINE.json']];hs={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths};checks=[]
def ck(n,c):
 checks.append({'name':n,'pass':bool(c)});assert c,n
for path,h in hs.items():ck('committed source '+path,hashlib.sha256(subprocess.check_output(['git','-C',str(R),'show','bb9b20525:'+path])).hexdigest()==h)
ck('source script hash agrees with result',hs[str((S/'cfg918.py').relative_to(R))]==d['script_sha256'])
for p,h in d['input_hashes'].items():ck('input '+p,hashlib.sha256((R/p).read_bytes()).hexdigest()==h)
# Extract only definitions; do not execute source main, top-level I/O, or mutate it.
needed={'M_pl','phi_pl','M_set','phi_set','phi_ext','simpson_log','simpson_lin','core_profile','core','family','jcap'}
nodes=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in needed];ns={'math':math,'np':np,'G':d['constants']['G'],'RC_CORE':104.,'NR':80,'NX':60};exec(compile(ast.Module(body=nodes,type_ignores=[]),'<source-definitions-only>','exec'),ns)
G=ns['G'];rows=[];guards=[];n=co=0
for f,branches in d['results'].items():
 for br,ds in branches.items():
  for name,obj in ds.items():
   b=obj['base'];a=b['a'];rad=b['R']
   ck(f+' '+br+' '+name+' mass partition',abs((b['Mx']+b['Mout'])/b['Mrem']-1)<1e-12)
   for g,gr in obj['geoms'].items():
    for rb,e in gr['rb'].items():
     for k,arr in e['opt'].items():
      for q in arr:
       c=q['cfg']
       if not c:continue
       n+=1
       if math.isclose(c['r1'],c['r2'],rel_tol=1e-12) and c['mA']>0:co+=1
       ck('saved endpoint CS '+str(n),q['Jcap']<=c['CS_bound']*(1+1e-12))
# Exact full-Plummer virial response to spherical shell: G M/(3a)*(1+(r/a)^2)^(-3/2).
for name in ['Fornax','Leo I']:
 obj=d['results']['canonical']['B0'][name];b=dict(obj['base']);b['sMs']=b['Ms']*b['s'];b['name']=name;b['branch']='B0';a=b['a'];rad=b['R'];gr=obj['geoms']['G1'];base=math.pi*G*b['Ms']/(32*a)+G*b['sMs']/(3*a*math.sqrt(1+(rad/a)**2));k=next(k for k in gr['rb']['RE']['opt'] if k.startswith('1.0|C|'));q=gr['rb']['RE']['opt'][k][-1];c=q['cfg'];A=G*c['mA']/(3*a)*(1+(c['r1']/a)**2)**(-1.5)
 rows.append({'name':name,'source_footing':'canonical','source_mass_branch':'B0','geometry':'G1','receiver':'RE','core':'C','phiK':1.,'lambda_c':1.,'shellA_radius_over_R':c['r1']/rad,'Jcap_over_Jreq':q['Jcap']/q['Jreq'],'observed_sigma':b['sig'],'baseline_plus_A_sigma_lower_bound':math.sqrt(base+A),'baseline_sigma2':base,'A_sigma2':A})
 ck(name+' selected endpoint lower bound exceeds central observation',base+A>b['sig']**2)
 # Separate post-hoc partial guard on PH1 family at r>=2R, fixed same endpoint.
 cr=ns['core'](b,'C',rad);fam=ns['family'](b,cr,gr['rmax_set'][-1],b['Mout'],rin=2*rad)
 Et=gr['E_init_corners']['lam1.0|phiK1.0'];Jreq=gr['patch']['J1'];K=Et-fam['Epart'];ok=(K>=fam['Klo']);JA=fam['JA'];J=np.where(ok,JA+fam['C']*np.sqrt(np.maximum(K,0)),-np.inf);ga=G*fam['mA']/(3*a)*(1+(fam['r1']/a)**2)**(-1.5);guard=base+ga<=b['sig']**2;best=float(np.max(np.where(guard,J,-np.inf)));count=int(np.sum(ok & guard & (J>=Jreq)))
 mcore,dmcore=ns['core_profile']('C',b['Mx'],rad);corevar=G/(3*a)*ns['simpson_log'](lambda rr:(1+(rr/a)**2)**(-1.5)*dmcore(rr),rad*1e-7,rad,n=10001);Bvar=G*fam['mB']/(3*a)*(1+(fam['r2']/a)**2)**(-1.5);fullvar=base+corevar+ga+Bvar;fullguard=fullvar<=b['sig']**2;fullbest=float(np.max(np.where(fullguard,J,-np.inf)));fullpass=ok & fullguard & (J>=Jreq);fullcount=int(np.sum(fullpass));ib=int(np.argmax(np.where(fullguard,J,-np.inf)));fullopt=({'rA_pc':float(fam['r1'][ib]),'rB_pc':float(fam['r2'][ib]),'mA_Msun':float(fam['mA'][ib]),'mB_Msun':float(fam['mB'][ib]),'sigma_stars_static_snapshot':math.sqrt(float(fullvar[ib]))} if math.isfinite(fullbest) else None)
 guards.append({'full_static_snapshot_upper_guard_count':fullcount,'full_static_snapshot_Jcap_over_Jreq':fullbest/Jreq if math.isfinite(fullbest) else None,'full_static_snapshot_optimum':fullopt,'core_sigma2':corevar,'name':name,'guard':'baseline plus circular shell A only; core and B positive contribution omitted','rmin_over_R':2.,'grid_nr':80,'grid_nx':60,'Jreq':Jreq,'best_guarded_Jcap':best if math.isfinite(best) else None,'guarded_capacity_ratio':best/Jreq if math.isfinite(best) else None,'number_of_grid_candidates_passing_necessary_partial_guard_and_J':count,'status':'partial guard does not eliminate capacity' if count else 'no candidate in declared family for this endpoint'})
 del fam
ck('source unchanged during audit',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in hs.items()))
res={'record':'CFG918-provisional-envelope-stellar-guard-2026-10-20','status':'finalized source snapshot independently pinned','source_result_commit':'bb9b20525','audit_observed_head':subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD']).decode().strip(),'source_hashes':hs,'checks':checks,'n_checks':len(checks),'saved_optima_count':n,'coincident_saved_endpoint_optima_nonzero_A':co,'selected_endpoint_stellar_bounds':rows,'separate_PH1_partial_guard':guards,'scope':'Saved source mass/CS checks plus new conditional full-Plummer stellar lower bound and restricted two-dwarf endpoint search. Not frozen regrade; no actual transport, all-spin/four-dwarf closure, measured selection function or uncertainty fit. Uses source function definitions for family, not independent full optimizer.'};res['software']={'python':sys.version.split()[0],'numpy':np.__version__};res['peak_rss_bytes_macos']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;assert res['peak_rss_bytes_macos']<1_000_000_000;Path(sys.argv[1] if len(sys.argv)>1 else '/private/tmp/ce918_endpoint_receipt.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['n_checks','saved_optima_count','coincident_saved_endpoint_optima_nonzero_A','selected_endpoint_stellar_bounds','separate_PH1_partial_guard']},indent=1))
