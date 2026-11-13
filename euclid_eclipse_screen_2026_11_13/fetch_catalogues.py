"""Fetch only three public catalogue archives; verify publisher MD5 checksums."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / 'inputs'
FILES = {
    'ECLIPSE_object_catalogue.zip': '56433fecbdc459046ffe9eca44bb4dcf',
    'ECLIPSE_D_dr1_redshifts_and_physical_properties.zip': 'cb31dbd65a3586ab13f52cff2df67f6b',
    'ECLIPSE_lens_models.zip': '84e046af2d93b95f1f5dc99ebe7edfec',
}

def fetch(item):
    name, expected = item
    dest = INPUTS / name
    url = 'https://zenodo.org/records/19654904/files/' + name + '?download=1'
    if not dest.exists():
        temp = dest.with_suffix('.part')
        req = urllib.request.Request(url, headers={'User-Agent': 'ECLIPSE-feasibility-screen/1.0'})
        with urllib.request.urlopen(req, timeout=60) as response, temp.open('wb') as out:
            total = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > 350_000_000:
                    raise ValueError('Archive exceeds declared download bound')
                out.write(chunk)
        temp.rename(dest)
    data = dest.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    if md5 != expected:
        raise ValueError('Publisher MD5 mismatch for ' + name + ': ' + md5)
    entry = {'url': url, 'file': str(dest.relative_to(ROOT)), 'bytes': len(data),
             'md5': md5, 'expected_md5': expected, 'sha256': hashlib.sha256(data).hexdigest(),
             'verified_utc': datetime.now(timezone.utc).isoformat()}
    print(json.dumps(entry), flush=True)
    return entry

if __name__ == '__main__':
    INPUTS.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(fetch, FILES.items()))
    (ROOT / 'download_manifest.json').write_text(json.dumps(results, indent=2) + '\n')
