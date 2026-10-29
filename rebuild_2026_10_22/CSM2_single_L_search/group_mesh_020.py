import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import argparse,json,hashlib,sys,time
p=Path(__file__).resolve().parent;r=p.parents[1];ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True);t0=time.monotonic()
files=[Path(__file__),p/'GROUP_MESH_020_CRITERIA.md',p/'group_mesh_020_contract.json',p/'GROUP_SUBDIVISION_ROUTE.md',p/'group_regional.py',p/'group_regional_001/results.json',p/'group_regional_001/group_regional_evidence.npz',p/'GROUP_MESH_CONTINUATION.md',p/'group_mesh_020_input_inventory.json',p/'group_subdivision.py',p/'GROUP_MESH_020_ROUTE.md',p/'group_mesh_002.py',p/'group_mesh_003.py',p/'group_mesh_004.py',p/'group_mesh_005.py',p/'group_mesh_006.py',p/'group_mesh_007.py',p/'group_mesh_008.py',p/'group_mesh_009.py',p/'group_mesh_010.py',p/'group_mesh_011.py',p/'group_mesh_012.py',p/'group_mesh_013.py',p/'group_mesh_014.py',p/'group_mesh_015.py',p/'group_mesh_016.py',p/'group_mesh_017.py',p/'group_mesh_018.py',p/'group_mesh_019.py']
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();hashes={str(f.relative_to(r)):sha(f) for f in files};source=(p/'group_regional.py').read_text();tiles=[]
for tile,lo,hi in [(38,'3.00','3.01'),(39,'3.01','3.02')]:
 s=source.replace("p/'GROUP_REGIONAL_CRITERIA.md'","p/'GROUP_MESH_020_CRITERIA.md'").replace("p/'group_regional_contract.json'","p/'group_mesh_020_contract.json'")
 s=s.replace("p/'group_interval_001/group_interval_evidence.npz']","p/'group_interval_001/group_interval_evidence.npz',p/'group_regional.py',p/'group_regional_001/results.json',p/'group_regional_001/group_regional_evidence.npz',p/'GROUP_SUBDIVISION_ROUTE.md']")
 s=s.replace("L0=q(min(F('2.62'),F(2.62)))",f"L0=q(min(F('{lo}'),F({lo})))").replace("L1=q(max(F('3.5001'),F(3.5001)))",f"L1=q(max(F('{hi}'),F({hi})))")
 start=s.index("localV=dict(np.load(paths[14]))");end=s.index('DP=[',start)
 s=s[:start]+"broad=dict(np.load(paths[17]));bV=broad['velocity_bounds'];bP=broad['velocity_derivative_bounds']\nck('broad_velocity_contains_tile',np.all(bV[:,:,0]<=V[:,:,0]) and np.all(bV[:,:,1]>=V[:,:,1]))\nck('broad_derivative_contains_tile',np.all(bP[:,:,0]<=derivatives[:,:,0]) and np.all(bP[:,:,1]>=derivatives[:,:,1]))\n"+s[end:]
 sub=out/f'tile_{tile:03d}';sys.argv=[str(Path(__file__)),'--output',str(sub)];exec(compile(s,str(p/'group_regional.py'),'exec'),{'__file__':str(Path(__file__)), '__name__':'__main__'})
 d=json.loads((sub/'results.json').read_text());assert all(d['checks'].values());tiles.append(dict(tile=tile,domain=[lo,hi],status=d['status'],necessary_failure=d['common_scope_interval_failure'],negative_derivative=d['regional_negative_sign'],Z=d['statistics']['Z'],Z_prime=d['statistics']['Z_prime'],result=str((sub/'results.json').relative_to(r)),result_sha256=sha(sub/'results.json')))
checks={'two_declared_tiles':len(tiles)==2,'hashes_stable':all(sha(r/k)==v for k,v in hashes.items())};inventory=json.loads((p/'group_mesh_020_input_inventory.json').read_text())['tiles']
for d in tiles:inventory[d['tile']]=dict(tile=d['tile'],status=d['status'],result=d['result'])
inventory[88]=dict(tile=88,status='PRIOR_LOCAL_NECESSARY_FAILURE',result=str((p/'group_interval_001/results.json').relative_to(r)))
result=dict(checks=checks,tiles=tiles,coverage_inventory=inventory,fully_tested_tiles=41,total_tiles=89,global_L_exclusion=False,scope='Two new numerical mesh tiles only, prior local last tile reused; no full chain/global/original floating certification',input_sha256=hashes,runtime_seconds=time.monotonic()-t0)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print('subdivision',len(tiles),'new tiles',all(checks.values()));assert all(checks.values())
