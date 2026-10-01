#!/usr/bin/env python3
"""Validate completed evidence records; never interpret metadata as physics."""
import argparse,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
p=argparse.ArgumentParser();p.add_argument('validator',type=Path);a=p.parse_args()
spec=importlib.util.spec_from_file_location('mathbox_manifest_validator',a.validator)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
rows=[]
for path in sorted(HERE.rglob('*manifest.json')):
 if 'mirror' in path.parts or '__pycache__' in path.parts:continue
 obj=json.loads(path.read_text());root=ROOT
 # Turnaround's legacy runner explicitly used its lane as the v1 path root.
 if obj.get('schema_version')==1 and obj.get('outputs') and all(str(x.get('path','')).startswith('runs/') for x in obj['outputs']):
  root=HERE/'turnaround'
 errors=mod.validate(obj,root=root,manifest_path=path)
 rows.append({'manifest':str(path.relative_to(ROOT)),'root':str(root.relative_to(ROOT)),
              'schema':obj.get('schema_version'),'errors':errors,
              'limitations':mod.legacy_limits(obj,root,path)})
out={'records':len(rows),'invalid':sum(bool(r['errors']) for r in rows),'rows':rows,
     'scope':'Checks recorded outputs and declared input freshness where supported. Does not prove scientific correctness or completeness of arbitrary dependency closure.'}
(HERE/'EVIDENCE_VALIDATION.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
for row in rows:
 if row['errors']:print(row['manifest'],row['errors'])
raise SystemExit(bool(out['invalid']))
