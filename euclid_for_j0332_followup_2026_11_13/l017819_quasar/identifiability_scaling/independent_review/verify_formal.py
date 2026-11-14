import sys,json,subprocess,hashlib,re,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parents[2];workspace=ROOT/'fable_independent_2026/lean_2026';out=B/'run_01'
source=P/'ConditionalScaling_v1.lean';raw=source.read_text();sha=hashlib.sha256(source.read_bytes()).hexdigest();assert sha=='ad4524d3f24929571f39b96971165c74695608555473fd22024c32a060bda3e6'
assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',re.sub(r'#print axioms[^\n]*','',raw))
version=subprocess.run(['lake','env','lean','--version'],cwd=workspace,capture_output=True,text=True,timeout=15);assert version.returncode==0
positive=subprocess.run(['lake','env','lean',str(source.resolve())],cwd=workspace,capture_output=True,text=True,timeout=45);(out/'positive.stdout').write_text(positive.stdout);(out/'positive.stderr').write_text(positive.stderr);assert positive.returncode==0,positive.stdout+positive.stderr
axioms=re.findall(r"'ConditionalScaling\.([^']+)' depends on axioms: (\[[^\]]*\])",positive.stdout);assert len(axioms)==13,(len(axioms),positive.stdout)
for name,listed in axioms:
 assert 'sorryAx' not in listed
 allowed={'propext','Classical.choice','Quot.sound'};assert set(filter(None,[x.strip() for x in listed.strip('[]').split(',')]))<=allowed,(name,listed)
needle='(k*a)^2 = (c^2*G/4)*(k^2*rho)';assert raw.count(needle)==1;mutated=raw.replace(needle,'(k*a)^2 = (c^2*G/4)*(k^3*rho)');mf=out/'FalseDensityScaling.lean';mf.write_text(mutated)
negative=subprocess.run(['lake','env','lean',str(mf.resolve())],cwd=workspace,capture_output=True,text=True,timeout=45);(out/'negative.stdout').write_text(negative.stdout);(out/'negative.stderr').write_text(negative.stderr);msg=negative.stdout+negative.stderr;assert negative.returncode!=0
assert 'unsolved goals' in msg or 'tactic' in msg.lower(),msg
for bad in ['file not found','no such file','unknown module','unknown package','object file','unknown constant']:assert bad not in msg.lower(),msg
# Exact counterexample to mutation: c2,G1,rho1,a1,k2 -> h:1=1; mutated4=8 false.
r={'source_sha256':sha,'workspace':str(workspace),'lean_version':version.stdout.strip(),'positive_returncode':positive.returncode,'axioms':axioms,'false_mutation':'density_relation_scales RHS k^2rho changed to k^3rho','mutation_sha256':hashlib.sha256(mf.read_bytes()).hexdigest(),'negative_returncode':negative.returncode,'negative_failure_excerpt':msg[:2500],'false_mutation_exact_counterexample':{'c':2,'G':1,'rho':1,'a':1,'k':2,'premise_lhs':1,'premise_rhs':1,'mutated_lhs':4,'mutated_rhs':8},'scope':'Compile+axiom+falseproofguard; analyticPDE/cosmologicalapplicationnotcertified'};(out/'result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
