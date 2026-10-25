import argparse,hashlib,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();checks=[]
def check(name,value):
 checks.append(dict(name=name,passed=bool(value)));assert value,name
for pattern in ['runs/*.json','pulse_runs/*.json','refined_runs/*.json','late_runs/*.json']:
 for f in sorted(P.glob(pattern)):
  d=json.loads(f.read_text());check(f.stem+' unchanged inputs',d['inputs_before']==d['inputs_after'])
  for q,v in d['inputs_after'].items():check(f.stem+' pin '+q,hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==v)
  check(f.stem+' measured RSS <1GB',d['peak_RSS_bytes']<1_000_000_000)
  check(f.stem+' raw checkpoint exists',f.with_suffix('.npz').is_file())
for name in ['equivalence','free_control','partition_control','checkpoint_control','gauss_control','flux_control','poisson_control','memory_control','support_screen']:
 d=json.loads((P/(name+'.json')).read_text());check(name+' retained structured output',bool(d))
d=json.loads((P/'runs/draco_joint_s07.json').read_text());h=d['history'][-1];check('coarse target T20 reached',abs(h['t']-20)<1e-10);check('coarse T20 NOT physically accepted',max(abs(h['Jz_relative_error']),h['angular_edge_fraction'])>.01)
for name in ['refinement_preflight','refinement_preflight_v2','refinement_preflight_v3','refinement_preflight_v4']:
 d=json.loads((P/(name+'.json')).read_text());check(name+' failed headroom preserved',not d['headroom_pass'] and d['peak_RSS_bytes']<1_000_000_000)
d=json.loads((P/'refinement_preflight_fallback.json').read_text());check('preregistered48x80 headroom passes',d['headroom_pass'] and d['peak_RSS_bytes']<750_000_000)
path=ROOT/a.output;path.write_text(json.dumps(dict(scope='record/provenance/gate audit only; mathematical controls in named scripts; no four-dwarf closure',checks=checks),indent=2)+'\n');print(len(checks),'checks passed')
