import argparse,hashlib,json,pathlib
Q=pathlib.Path(__file__).resolve().parent;ROOT=Q.parents[1];p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();checks=[]
def check(name,value):
 checks.append(dict(name=name,passed=bool(value)));assert value,name
files=list(Q.glob('late_runs/*.json'))+list(Q.glob('binding_runs/*.json'))+list(Q.glob('binding_phase_runs/*.json'))+list(Q.glob('radial_runs/*.json'))+[Q/'assembly_screen.json'];check('11 numerical producer records',len(files)==11)
for f in files:
 d=json.loads(f.read_text());check(str(f.relative_to(Q))+' unchanged pins',d['inputs_before']==d['inputs_after']);check(str(f.relative_to(Q))+' measured headroom',d['peak_RSS_bytes']<750_000_000)
 for k,v in d['inputs_after'].items():check(str(f.relative_to(Q))+' pin '+k,hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v)
 if f.parent.name=='late_runs':
  check(f.stem+' interval finished',d['status']=='finished requested interval' and abs(d['history'][-1]['t']-.2)<1e-12);check(f.stem+' mass identity',d['finite_mass_residual']<1e-10)
for name in ['FINAL_RESULTS','summary','summary_v2','wave_error','wave_error_v2','claude_check']:
 d=json.loads((Q/(name+'.json')).read_text());check(name+' unchanged pins',d['inputs_before']==d['inputs_after'])
 for k,v in d['inputs_after'].items():check(name+' pin '+k,hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v)
d=json.loads((Q/'FINAL_RESULTS.json').read_text());check('12 window cases retained',len(d['binding'])==12);check('radial lower bounds positive',all(x['radial_phase_lower_bound_on_total_bulk_rest_self_energy']>0 for x in d['binding']));check('four time levels retained',len(d['timestep'])==4);check('core energy gain on all levels',all(x['core_outward_E']<0 and x['core_delta_E']>0 for x in d['timestep']));check('full state order NOT falsely accepted',d['wave_errors'][-2]['relative_L2']/d['wave_errors'][-1]['relative_L2']<3);check('initial selector empty both grids',all(not x['desired_intervals'] and x['root_gap']<0 for x in d['initial_energy_sign_screen']));check('11 validated manifests',len(json.loads((Q/'manifest_validation.json').read_text())['records'])==11)
(ROOT/a.output).write_text(json.dumps(dict(scope='packet integrity and exact finite implications; not a continuum or four-dwarf proof',checks=checks),indent=2)+'\n');print(len(checks),'checks passed')
