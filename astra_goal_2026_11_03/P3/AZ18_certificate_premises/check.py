from pathlib import Path
import subprocess,json,hashlib,re
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
inputs=[D/'CRITERIA.md',D/'Certificate.lean',D/'Mutate.lean',Path(__file__),ROOT/'deepseek_push/lean/PD07_kappa_half_certified.lean',ROOT/'qwen38_push/lean/Q010_kappa_closure.lean']
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
runs={}
for name in ['Certificate','Mutate']:
 p=subprocess.run(['lean',str((D/(name+'.lean')).relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 log=p.stdout+p.stderr;(D/(name+'.log')).write_text(log)
 runs[name]={'exit':p.returncode,'log_sha256':hashlib.sha256(log.encode()).hexdigest()}
cert=(D/'Certificate.log').read_text();mut=(D/'Mutate.log').read_text()
code=(D/'Certificate.lean').read_text()
checks={'accepted_certificate':runs['Certificate']['exit']==0,'five_axiom_reports':cert.count('depends on axioms:')==5,'standard_axioms_only':all(x.strip() in ['propext','Classical.choice','Quot.sound'] for z in re.findall(r'axioms: \[([^\]]*)\]',cert) for x in z.split(',')),'no_proof_placeholders':not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe)\b',code),'mutation_rejected':runs['Mutate']['exit']!=0 and 'false' in mut.lower(),'inputs_unchanged':all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items())}
label='PASS' if all(checks.values()) else 'NO VERDICT'
out={'label':label,'scope':'Premise audit only, not physical derivation','disclaimer':'κ = ½ FITTED; not theory closed','footings':{k:{'audit':label,'physical_derivation':'NOT EVALUABLE'} for k in ['canonical','alt']},'checks':checks,'runs':runs,'inputs':hashes,'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'lean':subprocess.check_output(['lean','--version'],text=True).strip()}
(D/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
raise SystemExit(not all(checks.values()))
