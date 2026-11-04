"""Independent saved-profile and coefficient audit; writes only REVIEW.md.

No field solve is performed. Local tensor probes use deterministic float64
jets; population and refinement grades are reconstructed from saved profiles.
"""
import argparse, hashlib, importlib.util, json, math, resource, signal, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
VALIDATOR = '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py'
import power_model as J
np, C = J.np, J.M.C
RUNS = [('full_125_001',1.25,[1.5,2.,2.5,3.,3.5,4.],'original'),
        ('full_150_001',1.5,[1.5,2.,2.5,3.,3.5,4.],'original'),
        ('full_175_001',1.75,[1.5,2.,2.5,3.,3.5,4.],'original'),
        ('adaptive_125_mid_001',1.25,[2.75],'adaptive'),
        ('adaptive_1125_001',1.125,[3.],'adaptive')]

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text())
def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def manifest(run,pins):
    path=BASE/run/'manifest.json'
    if not path.exists(): return False
    m=load(path)
    assert m['run']['status']=='completed',(run,m['run'])
    q=subprocess.run([sys.executable,VALIDATOR,'--root',str(ROOT),str(path)],capture_output=True,text=True,timeout=15)
    assert q.returncode==0,(run,q.stdout,q.stderr)
    pins[str(path.relative_to(ROOT))]=digest(path)
    result=path.with_name('results.json');pins[str(result.relative_to(ROOT))]=digest(result)
    return True

def tensor_audit():
    A=module(BASE.parent/'analytic/law.py','review_power_tensor')
    jets=[([.3,-.4],[.2,.1,-.3,.4]),([0,0],[0,0,0,0]),([0,0],[1,.2,-1,.3]),
          ([1,2],[0,0,0,0]),([1e-6,-2e-6],[1e2,2e1,-3e1,4e1]),
          ([1e6,-2e6],[1e-4,2e-4,-3e-4,4e-4]),([1e-8,2e-8],[1e-8,2e-8,-3e-8,4e-8]),
          ([-2,.7],[.5,-.4,.2,-.1])]
    maximum={k:0. for k in ['A','B','energy','z']};count=0;ends={}
    old2=module(BASE.parents[1]/'KT38_weak_field_curvature/mw/weak_model.py','review_power_two_mw')
    for p in [1.,1.125,1.25,1.5,1.75,2.]:
        J.set_power(p)
        for ell in [0.,.1,3.,10.]:
            for gv,hv in jets:
                g=np.array(gv,dtype=float)[:,None];h=np.array(hv,dtype=float)[:,None]
                a,b,e,z=J.Generalized.coefficients(g,h,ell)
                G=np.array([*gv,0.]);H=np.array([[hv[0],hv[1],0.],[hv[1],hv[2],0.],[0.,0.,hv[3]]])
                q=A.tensor_terms(G,H,ell,p=p)
                target={'A':q['A'][:2],'B':np.array([q['B'][0,0],q['B'][0,1],q['B'][1,1],q['B'][2,2]]),'energy':q['energy'],'z':q['z']}
                actual={'A':a[:,0],'B':b[:,0],'energy':e[0]+float(g[:,0]@g[:,0]),'z':z[0]}
                for k in maximum:
                    error=float(np.max(np.abs(actual[k]-target[k])))/max(float(np.max(np.abs(target[k]))),1e-300)
                    maximum[k]=max(maximum[k],error);assert error<5e-14,(p,ell,k,error)
                count+=1
        if p in (1.,2.):
            old=J.J.Generalized if p==1 else old2.Generalized;error=0.
            for gv,hv in jets:
                g=np.array(gv,dtype=float)[:,None];h=np.array(hv,dtype=float)[:,None]
                for x,y in zip(J.Generalized.coefficients(g,h,3.),old.coefficients(g,h,3.)):
                    error=max(error,float(np.max(np.abs(x-y)))/max(float(np.max(np.abs(y))),1e-300))
            ends[str(p)]=error;assert error<5e-14
    J.set_power(1.5)
    return dict(cases=count,powers=[1,1.125,1.25,1.5,1.75,2],lengths_kpc=[0,.1,3,10],
                max_relative_tensor_API_discrepancies=maximum,MW_endpoint_discrepancies=ends)

def grade(q,stats):
    K,vo,vc,K0=np.array(q['K']),np.array(q['vc_Ou']),q['vc'],q['K0']
    ck=float(np.sum(((K-C.BR_K)/C.BR_E5)**2));co=float(np.sum(((vo-C.OV)/C.OE)**2))
    xx=np.asarray(C.BR_R)-C.R0;yy=np.log(np.maximum(K,1e-9))
    slope=float(np.sum((xx-xx.mean())*(yy-yy.mean()))/np.sum((xx-xx.mean())**2))
    h=-1/slope if slope<0 else float('inf')
    flags={'L1':abs(vc-C.L.VC_BRIEF)<=C.L.VC_BRIEF_LINE and abs(vc-C.vE)<=2*C.eE,
           'L2a':ck<=C.LK,'L2b':abs(K0-C.KZ)<=2*C.KZE,'L3':co<=C.LO,'Lh':abs(h-C.HLIT)<=2*C.HE}
    D=max(ck/C.LK,abs(vc-C.vE)/(2*C.eE),co/C.LO,abs(K0-C.KZ)/(2*C.KZE))
    for k,v in flags.items(): assert bool(q[k])==bool(v),(k,q[k],v)
    for k,v in [('cK',ck),('cO',co),('D',D)]:
        stats['max_grade_scalar_relative_error']=max(stats['max_grade_scalar_relative_error'],abs(q[k]-v)/max(abs(v),1.))
    if q['h'] is None:
        assert slope>=0 and not flags['Lh'] and q['h_status']=='positive infinity: fitted log-K slope is nonnegative'
        stats['positive_infinite_h_count']+=1
    else:
        assert math.isfinite(h)
        stats['max_fitted_slope_absolute_error']=max(stats['max_fitted_slope_absolute_error'],abs(-1/q['h']-slope))
        stats['max_h_relative_error']=max(stats['max_h_relative_error'],abs(q['h']-h)/max(abs(h),1.))
    passed=all(flags[k] for k in ['L1','L2a','L2b','L3']);assert q['all_four']==passed
    stats['rows_regraded']+=1
    return flags,D

def counters():
    return dict(rows_regraded=0,positive_infinite_h_count=0,max_grade_scalar_relative_error=0.,max_fitted_slope_absolute_error=0.,max_h_relative_error=0.)

def finish_stats(s):
    assert s['max_grade_scalar_relative_error']<2e-11 and s['max_fitted_slope_absolute_error']<1e-12
    s['flag_or_summary_mismatches']=0

def main():
    signal.alarm(180);resource.setrlimit(resource.RLIMIT_CPU,(150,150))
    ap=argparse.ArgumentParser();ap.add_argument('--require-complete',action='store_true');ap.add_argument('--update-review',action='store_true');args=ap.parse_args()
    pins={};pending=[];controls=[];population=J.E.population();best_lookup={};summaries=[];run_summaries=[]
    for name,p in [('checks_1125_001',1.125),('checks_125_001',1.25),('checks_150_001',1.5),('checks_175_001',1.75)]:
        if not manifest(name,pins):pending.append(name);continue
        d=load(BASE/name/'results.json');assert d['power']==p and d['all_checks_pass']
        controls.append(dict(run=name,power=p,all_checks_pass=True,
            worst_best_energy_relative=max(min(x['energy_relative'] for x in row['steps']) for row in d['variational']),
            worst_best_reciprocity_relative=max(min(x['reciprocity_relative'] for x in row['steps']) for row in d['variational']),
            max_spherical_polar_relative=max(x['spurious_polar_relative'] for x in d['spherical_2d'])))
    tensor=tensor_audit()
    for name,p,lengths,selection in RUNS:
        if not manifest(name,pins):pending.append(name);continue
        d=load(BASE/name/'results.json');assert d['power']==p and d['parameters']['power']==p
        control=load(ROOT/d['parameters']['invariants']);assert control['power']==p and control['all_checks_pass']
        assert d['cells']==population and d['selected_indices']==list(range(1375)) and set(d['footings'])=={'canonical','alt'}
        assert d['runtime_seconds']>0
        stats=counters()
        for foot,data in d['footings'].items():
            assert [s['ell_kpc'] for s in data['scans']]==lengths
            for scan in data['scans']:
                rows=scan['rows'];assert len(rows)==1375;good=[];strict=[];values=[];line_counts={k:0 for k in ['L1','L2a','L2b','L3','Lh']}
                for i,row in enumerate(rows):
                    assert row['index']==i and row['cell']==population[i] and row['ell_kpc']==scan['ell_kpc'] and row['source_stats']['finite']
                    flags,D=grade(row['corrected'],stats)
                    for k in flags:line_counts[k]+=bool(flags[k])
                    if row['corrected']['all_four']:good.append(i)
                    if row['corrected']['all_four'] and flags['Lh']:strict.append(i)
                    values.append((D,i))
                sm=scan['summary'];assert sm['pass_indices']==good and sm['n_pass']==len(good) and sm['n_strict']==len(strict)
                assert sm['lines']==line_counts and sm['n_tested']==1375 and sm['best_D_index']==min(values)[1]
                best=rows[sm['best_D_index']]
                best_lookup[foot,p,scan['ell_kpc']]=best
                summaries.append(dict(run=name,selection=selection,footing=foot,power=p,ell_kpc=scan['ell_kpc'],
                    n_pass=len(good),n_strict=len(strict),best_D_index=sm['best_D_index'],best_D=min(values)[0]))
        finish_stats(stats);run_summaries.append(dict(run=name,**stats))
    refinement=None
    if not manifest('refine_001',pins):pending.append('refine_001')
    else:
        d=load(BASE/'refine_001/results.json');assert d['complete'];cases=d['selection']['cases'];assert len(cases)==10
        assert load(BASE/'selection.json')==d['selection']
        keys={(c['footing'],c['power'],c['ell_kpc'],c['index']) for c in cases};assert len(keys)==10
        for c in cases:
            b=best_lookup[c['footing'],c['power'],c['ell_kpc']];assert b['index']==c['index']
            assert b['corrected']==c['production_score']
            source_run=Path(c['scan']).parent.name
            options=[x for x in summaries if x['run']==source_run and x['footing']==c['footing']]
            chosen=min(options,key=lambda x:x['best_D'])
            assert (chosen['power'],chosen['ell_kpc'],chosen['best_D_index'])==(c['power'],c['ell_kpc'],c['index'])
        grouped={key:[] for key in keys};stats=counters();coarse_error=0.
        for row in d['rows']:
            key=(row['footing'],row['power'],row['ell_kpc'],row['index']);assert key in grouped
            assert row['cell']==population[row['index']] and row['source_stats']['finite'];grade(row['score'],stats);grouped[key].append(row)
            if (row['refine'],row['rmin'],row['outer'])==(2,.005,1):
                old=best_lookup[key[:3]]['corrected'];coarse_error=max(coarse_error,max(abs(row['score'][k]-old[k])/max(abs(old[k]),1.) for k in ['vc','K0','cK','cO','D']))
        expected={(2,.005,1),(3,.005,1),(4,.005,1),(5,.005,1),(3,.0025,1),(3,.005,2)}
        refined=[]
        for key,rows in sorted(grouped.items()):
            assert {(r['refine'],r['rmin'],r['outer']) for r in rows}==expected and len(rows)==6
            finest=next(r for r in rows if r['refine']==5)['score']
            refined.append(dict(footing=key[0],power=key[1],ell_kpc=key[2],index=key[3],
                pass_configurations=sum(r['score']['all_four'] for r in rows),strict_configurations=sum(r['score']['all_four'] and r['score']['Lh'] for r in rows),
                min_D=min(r['score']['D'] for r in rows),max_D=max(r['score']['D'] for r in rows),
                finest={k:finest[k] for k in ['vc','K0','cK','cO','h','D','all_four','Lh']}))
        assert coarse_error<1e-7;finish_stats(stats)
        refinement=dict(**stats,max_coarse_literal_relative_error=coarse_error,selected=refined)
    for f in [BASE/'power_model.py',BASE/'checks.py',BASE/'search.py',BASE/'refine.py',BASE/'selection.json',BASE/'verify_review.py',BASE.parent/'PLAN.md',BASE.parent/'ADAPTIVE_PLAN.md',BASE.parent/'analytic/law.py',BASE.parents[1]/'KT37_generalized_action/mw/generalized_v3.py',BASE.parents[1]/'KT37_generalized_action/analytic/law.py']:
        pins[str(f.relative_to(ROOT))]=digest(f)
    report=dict(scope='Independent finite-coefficient and saved-profile audit; no field solve rerun.',
        limits=dict(wall_alarm_seconds=180,cpu_seconds=150,randomness=False),complete=not pending,pending=pending,
        tensor_API=tensor,controls=controls,population_runs=run_summaries,population_summaries=summaries,
        refinement=refinement,input_sha256=pins)
    if args.require_complete:
        assert not pending,pending
        assert sum(s['rows_regraded'] for s in run_summaries)==55000
        assert refinement['rows_regraded']==60
    payload=json.dumps(report,indent=2,allow_nan=False)
    if args.update_review:
        path=BASE/'REVIEW.md';text=path.read_text().split('<!-- GENERATED_AUDIT -->')[0].rstrip()
        path.write_text(text+'\n\n<!-- GENERATED_AUDIT -->\n## Reproducible audit record\n\n```json\n'+payload+'\n```\n')
    print(json.dumps(dict(complete=report['complete'],pending=pending,tensor_cases=tensor['cases'],
        population_rows=sum(x['rows_regraded'] for x in run_summaries),
        population_pass_counts=[{k:s[k] for k in ['power','ell_kpc','footing','n_pass','n_strict']} for s in summaries],
        refined_rows=None if refinement is None else refinement['rows_regraded']),indent=2))

if __name__=='__main__':main()
