"""Small hand-computable cap witness; not an astrophysical population forecast."""
from pathlib import Path
import ast,json,hashlib
import numpy as np
O=Path(__file__).resolve().parent
p=O/'corrected_statistic_audit.py';tree=ast.parse(p.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='summaries')
ns={'np':np,'P':{'VTCAP':6.}}
exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'),ns)
s=ns['summaries'];orbital=np.array([.5,.8,1.,1.]);noise=np.array([0.,0.,0.,4.99]);v0=orbital+noise;vg=1.05*orbital+noise;g=[np.ones(4,dtype=bool)]
mg,n=s(vg,g);mn,n0=s(v0,g);correct=float(np.exp(mg-mn)[0]-1)
mold,nold=s(vg,g,extra=v0<6);mold0,nold0=s(v0,g,extra=vg<6);mutant=float(np.exp(mold-mold0)[0]-1)
expected=.84/.9-1
assert abs(correct-expected)<1e-14
mutation_passes_correct_observable=abs(mutant-expected)<1e-14
assert not mutation_passes_correct_observable
out={'scope':'Constructed four-pair cap witness, not physical frequency or bias estimate.','orbital_component':orbital.tolist(),'fixed_additive_noise_component':noise.tolist(),'boost_applied_before_noise':True,'newton_vtilde':v0.tolist(),'boosted_vtilde':vg.tolist(),'symmetric_ratio_minus_one':correct,'counterfactual_intersection_ratio_minus_one':mutant,'hand_result':expected,'corrected_counts':[n,n0],'intersection_counts':[nold,nold0],'control_correct_observable_pass':True,'mutation_reverting_to_intersection_pass':mutation_passes_correct_observable,'script_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(O/'cap_control_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
