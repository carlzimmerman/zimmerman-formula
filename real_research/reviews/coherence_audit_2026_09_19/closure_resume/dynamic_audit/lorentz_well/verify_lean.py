from pathlib import Path
import subprocess,sys,json,re
here=Path(__file__).resolve().parent
root=here.parents[5]
host=root/'fable_independent_2026/lean_2026'
out=Path(sys.argv[1]).resolve();out.mkdir(exist_ok=True)
source=here/'StaticWitness.lean'
version=subprocess.run(['lake','env','lean','--version'],cwd=host,text=True,capture_output=True,check=True).stdout.strip()
run=subprocess.run(['lake','env','lean',str(source)],cwd=host,text=True,capture_output=True)
print(version,flush=True);print(run.stdout,flush=True);print(run.stderr,flush=True)
assert run.returncode==0
assert 'sorryAx' not in run.stdout
names=['sqrtY_exact','determinant_bridge','oldDet_exact','newDet_exact','temporalHessian_exact','oldDet_positive','newDet_negative','temporalHessian_positive','timelike_and_supersonic','local_static_tradeoff']
for name in names:assert "'LorentzWellStaticWitness."+name+"' depends on axioms: [propext, Classical.choice, Quot.sound]" in run.stdout
# Independently recompute the actual rational event and bridge the exact values
# to the theorem statements proved from the Lean definitions.
subprocess.run([sys.executable,str(here/'static_witness.py'),str(out)],check=True)
raw=json.loads((out/'results.json').read_text());text=source.read_text()
for theorem,value in [('oldDet_exact',raw['old_static_determinant']),('newDet_exact',raw['new_static_determinant']),('temporalHessian_exact',raw['temporal_well_Hessian'])]:
 match=re.search(r'theorem '+theorem+r'\s*:\s*\w+\s*=\s*\(([-0-9]+)\s*/\s*([0-9]+)\s*:\s*ℝ\)',text)
 assert match,(theorem,'missing exact rational statement')
 assert match.group(1)+'/'+match.group(2)==value,(theorem,value)
summary={'lean_version':version,'exit_code':run.returncode,'axioms':['propext','Classical.choice','Quot.sound'],'proved_theorems':names,'exact_symbolic_to_Lean_rational_bridge':True,'scope':'One explicit timelike supersonic local jet: old static determinant positive, new negative, temporal well Hessian positive. The action-to-matrix derivation is not formalized; no global halo or dynamical-instability theorem.'}
(out/'lean_result.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2),flush=True)
