import hashlib,json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];tool=pathlib.Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py');rows=[]
for f in sorted((P/'run_manifests').glob('*.json')):
 q=subprocess.run(['/opt/homebrew/bin/python3',str(tool),str(f),'--root',str(ROOT)],capture_output=True,text=True);rows.append(dict(manifest=str(f.relative_to(ROOT)),manifest_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),exit_code=q.returncode,stdout=q.stdout,stderr=q.stderr));assert q.returncode==0,(str(f),q.stdout,q.stderr)
(P/'manifest_validation.json').write_text(json.dumps(dict(validator=str(tool),validator_sha256=hashlib.sha256(tool.read_bytes()).hexdigest(),records=rows,scope='schema and current artifact hashes, not mathematical acceptance'),indent=2)+'\n');print(len(rows),'manifests validated')
