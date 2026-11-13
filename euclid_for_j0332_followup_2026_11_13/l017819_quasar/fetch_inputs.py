"""Fetch the named L017819 Euclid target only, retaining per-file provenance."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
INPUT = HERE / 'inputs'
FETCH = HERE.parent / 'external_spectroscopic_matches/fetch.py'

if __name__ == '__main__':
    record = json.loads((INPUT / 'portal_lens_record_network.json').read_text())
    assert record['id'] == 'Tile102140883RA2311901412524DEC0441637579847'
    pictures = {'rgb.png', 'vis_pix_fit.png', 'vis_lp_fit.png',
                'vis_lp_image_with_positions.png', 'segmentation.png', 'fit_sersic.png'}
    tasks = [(tree, name) for tree, names in record['files'].items()
             for name in names if not name.endswith('.png') or name in pictures]

    def fetch(item):
        tree, name = item
        dest = INPUT / tree / name
        url = 'https://euclid-eclipse-lenses.org/files/' + record['id'] + '/' + tree + '/' + name
        if dest.exists():
            raise RuntimeError('Refusing to overwrite ' + str(dest))
        proc = subprocess.run([sys.executable, str(FETCH), url, str(dest),
                               '--max-bytes', '12000000'], capture_output=True, text=True)
        print(tree + '/' + name, proc.returncode, flush=True)
        return dict(path=str(dest.relative_to(HERE)), url=url, returncode=proc.returncode,
                    stdout=proc.stdout, stderr=proc.stderr)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, tasks))
    (INPUT / 'fetch_summary.json').write_text(json.dumps(results, indent=2) + '\n')
    raise SystemExit(int(any(row['returncode'] for row in results)))
