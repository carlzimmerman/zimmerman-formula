"""Pin project evidence; one writer per area. Import has no side effects."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def capture(source,area):
    if area not in ('observational','foundational','audit','coordinator'):
        raise ValueError('Unknown disjoint source area')
    rel=Path(source)
    if rel.is_absolute():rel=rel.relative_to(ROOT)
    if '..' in rel.parts or '.git' in rel.parts:raise ValueError('project evidence only')
    original=ROOT/rel
    data=original.read_bytes();sha=hashlib.sha256(data).hexdigest()
    sid=area+'_'+hashlib.sha256(str(rel).encode()).hexdigest()[:12]+'_'+sha[:10]
    folder=HERE/'inputs'/area;folder.mkdir(parents=True,exist_ok=True)
    target=folder/(sid+rel.suffix)
    if target.exists() and target.read_bytes()!=data:raise ValueError('Snapshot collision')
    target.write_bytes(data)
    index=folder/'SOURCES.json'
    rows=json.loads(index.read_text())if index.exists()else []
    record={'id':sid,'source_path':str(rel),'snapshot_path':str(target.relative_to(HERE)),
            'sha256':sha,'bytes':len(data)}
    if not any(r['id']==sid for r in rows):rows.append(record)
    index.write_text(json.dumps(rows,indent=2)+'\n')
    return record

if __name__=='__main__':
    import sys
    print(json.dumps(capture(sys.argv[1],sys.argv[2]),indent=2))
