#!/usr/bin/env python3
"""Stream the two primary public HALOGAS cubes with explicit byte/checksum limits."""
import datetime
import hashlib
import json
from pathlib import Path
import time
import urllib.request

HERE = Path(__file__).resolve().parent
DATA = HERE / 'data'
DATA.mkdir(exist_ok=True)
FILES = [('NGC5023-HR-cube.fits', 289422720, 'ac29e70c0b5a36b3941c266b2c935fad'),
         ('NGC5023-LR-cube.fits', 289422720, '171c4d421e7d9d14662633912fdbf122')]
records = []
for name, expected_bytes, expected_md5 in FILES:
    final = DATA / name
    if final.exists():
        raise RuntimeError('Refusing to overwrite acquired input ' + name)
    url = 'https://zenodo.org/records/3715549/files/' + name + '?download=1'
    part = DATA / (name + '.partial')
    start = time.monotonic()
    sha, md5, count = hashlib.sha256(), hashlib.md5(), 0
    print('Acquiring', name, flush=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'NGC5023-public-research/1.0'})
    with urllib.request.urlopen(req, timeout=40) as response, part.open('xb') as stream:
        headers, resolved = dict(response.headers), response.url
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            count += len(chunk)
            if count > expected_bytes or time.monotonic() - start > 240:
                raise RuntimeError('Acquisition byte/time limit exceeded')
            stream.write(chunk)
            sha.update(chunk)
            md5.update(chunk)
    assert count == expected_bytes and md5.hexdigest() == expected_md5, 'Primary checksum mismatch'
    part.rename(final)
    record = {'url': url, 'resolved_url': resolved, 'path': str(final.relative_to(HERE.parents[1])),
              'bytes': count, 'sha256': sha.hexdigest(), 'md5': md5.hexdigest(),
              'expected_md5': expected_md5, 'catalog_checksum_matches': True,
              'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'runtime_seconds': time.monotonic() - start, 'headers': headers}
    records.append(record)
    (DATA / 'ACQUISITION.json').write_text(json.dumps({'source': 'HALOGAS DR1 v2, Zenodo 3715549',
        'acquisition_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'files': records, 'limits': {'bytes_per_file': expected_bytes, 'seconds_per_file': 240,
        'stream_chunk_bytes': 1048576, 'hard_memory_cap': None}}, indent=2) + '\n')
    print('Verified', name, count, sha.hexdigest(), flush=True)
