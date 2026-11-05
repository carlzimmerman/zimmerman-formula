#!/usr/bin/env python3
"""Hash-verified single-grid diagnostics; never a full convergence verdict."""
import argparse,json,platform
from pathlib import Path
import numpy as np
import scipy
import audit_inputs as A
import bullet_source as B
import grid3d as D
import sampling3d as S

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--field',required=True);parser.add_argument('--tag',required=True);parser.add_argument('--mutate',action='store_true');args=parser.parse_args()
 folder=(A.HERE/args.field).resolve();out=(A.HERE/args.tag).resolve()
 if A.HERE.resolve() not in folder.parents or A.HERE.resolve() not in out.parents:raise ValueError('Paths must be within lane')
 if folder==out:raise ValueError('Diagnostics must have a separate output directory')
 if args.mutate and 'mutate' not in out.parts:raise ValueError('Mutation requires separate mutate tree')
 result=json.loads((folder/'result.json').read_text())
 with np.load(folder/'checkpoint.npz',allow_pickle=False) as checkpoint:state=json.loads(str(checkpoint['state']))
 if state['status']!='complete' or state['identity']!=result['identity']:raise ValueError('Incomplete or mismatched field checkpoint')
 for filename,digest in state['outputs'].items():
  if A.sha(folder/filename)!=digest:raise ValueError('Changed field artifact')
 for filename,digest in result['identity']['source_hashes'].items():
  if A.sha(A.ROOT/filename)!=digest:raise ValueError('Stale field source')
 versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__)
 if result['identity']['versions']!=versions:raise ValueError('Field environment mismatch')
 config=result['identity']['arguments'];foot=config['foot'];epsilon=B.normalization(foot)['epsilon']
 grid=D.Grid(config['n'],config['half_width'],result['alpha'],result['centre_kpc'])
 phi=np.load(folder/'field.npy',allow_pickle=False)
 if A.sha(folder/'field.npy')!=result['field_sha256']:raise ValueError('Field/report hash mismatch')
 h=D.hessian(grid,phi);x,y,z=grid.coordinates()
 source=B.density(x*B.L0_KPC,y*B.L0_KPC,z*B.L0_KPC,np.asarray(result['source_components']))[1:-1,1:-1,1:-1]/B.RHO_REF
 residual=float(np.max(abs(D.operator(h,epsilon)-source))/max(1.,float(np.max(abs(source)))))
 minimum=D.principal_min(h,epsilon)
 finite=bool(np.all(np.isfinite(phi)) and all(np.all(np.isfinite(v)) for v in h))
 residual_eligible=finite and np.isfinite(residual) and residual<=1e-8 and np.isfinite(minimum) and minimum>0 and result['status']=='RESIDUAL CONVERGED'
 sampler=S.Sampler(grid,h,mutate=args.mutate);threshold=S.inherited_threshold(foot)
 obj=dict(field_identity=result['identity'],field_result_sha256=A.sha(folder/'result.json'),field_sha256=result['field_sha256'],mutate=args.mutate,residual=residual,principal_min=minimum,finite=finite,residual_eligible=bool(residual_eligible),max_hessian_norm=sampler.max_norm,inherited_threshold=threshold,threshold_scope='Inherited I6 data-calibrated value; not derived from the action or newly authenticated native data',source_hashes={A.relative(p):A.sha(p) for p in [Path(__file__).resolve(),Path(S.__file__).resolve(),Path(D.__file__).resolve(),Path(B.__file__).resolve(),Path(S.R.__file__).resolve(),S.THRESHOLDS,A.HERE/'SAMPLING_CONTRACT.md',A.HERE/'FROZEN_BULLET.md']},status='PILOT ONLY' if config['n']<=16 else 'SINGLE GRID ONLY',scope='No physical Bullet verdict until all frozen known-answer, field/box and disc convergence gates pass. kappa=1/2 FITTED; not theory closed')
 if config['source']=='bullet':
  sampled=sampler(list(S.POINTS.values()));point_values={name:float(sampled['s'][i]) for i,name in enumerate(S.POINTS)}
  obj['points']={name:dict(position_kpc=S.POINTS[name],s=point_values[name],norm=float(sampled['norm'][i]),tiny=bool(sampled['tiny'][i])) for i,name in enumerate(S.POINTS)}
  obj['discs']={name:[S.disc(sampler,position,threshold,nr,nt) for nr,nt in [(32,64),(64,128)]] for name,position in S.POINTS.items()}
  obj['threshold_diagnostics']=S.threshold_reading(point_values,threshold)
  obj['disc_quadrature_eligible']=all(abs(v[0]['mean_s']-v[1]['mean_s'])<=.01 and abs(v[0]['on_fraction']-v[1]['on_fraction'])<=.01 and v[0]['mean_on']==v[1]['mean_on'] and v[0]['tiny_samples']==v[1]['tiny_samples']==0 for v in obj['discs'].values())
 else:
  oracle=S.plummer_oracle(foot);obj['oracle']=oracle
  try:
   actual=sampler(oracle['points_kpc']);truth=np.asarray(oracle['s']);error=np.abs(actual['s']-truth)
   obj['plummer']=dict(s=actual['s'].tolist(),norm=actual['norm'].tolist(),tiny=actual['tiny'].tolist(),absolute_errors=error.tolist(),max_error=float(error.max()),threshold_flags_match=bool(np.array_equal(actual['s']>=threshold,oracle['on'])),oracle_line_met=bool(np.all(error<=.02) and not np.any(actual['tiny'])))
  except ValueError as exc:obj['plummer']=dict(status='NOT EVALUABLE',sampling_domain_error=str(exc),oracle_line_met=False)
 A.atomic(out/'samples.json',obj)
 print(json.dumps(dict(status=obj['status'],residual_eligible=obj['residual_eligible'],source=config['source'],mutate=args.mutate),indent=2))
if __name__=='__main__':main()
