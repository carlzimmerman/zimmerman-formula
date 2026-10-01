"""Independent algebraic audit of returned finite operator, not its map construction."""
from pathlib import Path
import json,sys
import numpy as np

source=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz')
with np.load(source,allow_pickle=False) as z: d={k:z[k] for k in z.files}
H=d['H']; L=d['L']; nodes=d['nodes']
assert H.shape==(12,16) and L.shape==(16,) and nodes.shape==(16,)
assert np.array_equal(H[:,:15],d['A']) and np.array_equal(H[:,-1],np.ones(12))
# Orthogonal projector built from a full QR decomposition of H transpose.
Q,R=np.linalg.qr(H.T,mode='complete')
assert np.linalg.matrix_rank(R[:12,:])==12
N=Q[:,12:]
target_null=N.T@L
relative_target=float(np.linalg.norm(target_null)/np.linalg.norm(L))
null_res=float(np.linalg.norm(H@N)/(np.linalg.norm(H)*np.linalg.norm(N)))
assert relative_target>1e-3 and null_res<1e-13
observations=[]; slopes=[]
for key in ['pressure_plus','pressure_minus']:
    p=d[key]; assert np.all(p[:15]>0) and np.all(np.diff(np.r_[p[:15],0.])<0)
    j=int(np.searchsorted(nodes,1.0)-1)
    direct=(p[j+1]-p[j])/(nodes[j+1]-nodes[j])
    assert abs(direct-L@p)<1e-18
    slopes.append(float(direct));observations.append(H@p)
res=float(np.linalg.norm(observations[0]-observations[1])/np.linalg.norm(H@d['baseline']))
assert res<1e-12 and abs(slopes[0]-slopes[1])>1e-9
# A derivative is identifiable in the reduced square model only after fixing nuisance values.
closed=H[:,:12]; dual=np.linalg.solve(closed.T,L[:12])
assert np.linalg.norm(dual@closed-L[:12])<1e-11
full_dual_error=float(np.linalg.norm(dual@H-L))
assert full_dual_error>1e-3  # deliberately wrong transfer of the closed-model estimator fails.
out={'scope':'Returned matrix algebra only; no independent map, beam or cosmology reconstruction',
     'independent_method':'Full QR null basis and direct slope from pressure-node locations',
     'relative_target_null_component':relative_target,'relative_null_residual':null_res,
     'witness_slopes':slopes,'witness_relative_observation_difference':res,
     'closed_estimator_full_model_error':full_dual_error,'all_checks_pass':True,
     'nonclaims':['No bounds on maximum feasible gradient width','No fit of the actual map','No statistical significance']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
