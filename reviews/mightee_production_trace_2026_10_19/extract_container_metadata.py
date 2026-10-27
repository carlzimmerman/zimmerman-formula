"""Read text metadata from a public SIF prefix; never execute the container."""
from pathlib import Path
import re,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DATA=ROOT/'_external_data/mightee_production_trace_2026_10_19'

def main():
    raw=(DATA/'container_prefix.bin').read_bytes();assert b'SIF_MAGIC' in raw[:64]
    texts=[b.decode('ascii') for b in re.findall(rb'[\x20-\x7e\n\r\t]{20,}',raw)]
    definitions=[s for s in texts if s.startswith('Bootstrap:')];assert definitions
    metadata=[]
    for s in texts:
        if s.startswith('{"data":{"attributes"'):
            try:metadata.append(json.loads(s))
            except ValueError:pass
    assert metadata
    (HERE/'public_container_definition.txt').write_text(definitions[0])
    (HERE/'public_container_metadata.json').write_text(json.dumps(metadata[0],indent=2))
    record=dict(prefix_sha256=hashlib.sha256(raw).hexdigest(),prefix_bytes=len(raw),container_executed=False,container_fully_downloaded=False,definition_sha256=hashlib.sha256(definitions[0].encode()).hexdigest(),labels=metadata[0]['data']['attributes']['labels'],pypher_recipe_lines=[line.strip() for line in definitions[0].splitlines() if 'pypher' in line.lower()],limitation='Text objects recovered from the SIF prefix; this does not inspect the installed filesystem, determine the exact installed PyPHER version or connect the image to the DR1 execution.')
    (HERE/'container_inspection.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2))

if __name__=='__main__':main()
