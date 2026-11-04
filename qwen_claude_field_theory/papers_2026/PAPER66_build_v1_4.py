#!/usr/bin/env python3
"""Rebuild PAPER66 and bind the PDF to exact source inputs; no publication.
Run: TECTONIC=/path/to/tectonic python3 PAPER66_build_v1_4.py
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STEM = 'PAPER66_alma_release_predictions_2026'
SOURCES = [STEM+'.tex'] + [f'PAPER66_tables_{c}.tex' for c in 'abc'] + ['PAPER66_validation_v1_4.tex']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    compiler = os.environ.get('TECTONIC') or shutil.which('tectonic')
    if not compiler:
        raise SystemExit('Set TECTONIC to the installed compiler path')
    before = {name: sha(HERE/name) for name in SOURCES}
    with tempfile.TemporaryDirectory(prefix='paper66_build_') as tmp:
        proc = subprocess.run([compiler, '--keep-logs', '--outdir', tmp, str(HERE/(STEM+'.tex'))], text=True, capture_output=True)
        log = proc.stdout + proc.stderr
        (HERE/'PAPER66_build_v1_4.out').write_text(log)
        if proc.returncode:
            raise SystemExit(log)
        texlog = (Path(tmp)/(STEM+'.log')).read_text(errors='replace')
        (HERE/'PAPER66_build_v1_4.log').write_text(texlog)
        for bad in ('Overfull \\hbox', 'Overfull \\vbox', 'undefined references', 'undefined citations'):
            if bad in texlog:
                raise SystemExit('Build requires layout/reference repair: '+bad)
        if before != {name: sha(HERE/name) for name in SOURCES}:
            raise SystemExit('Inputs changed during build')
        shutil.copyfile(Path(tmp)/(STEM+'.pdf'), HERE/(STEM+'.pdf'))
    manifest = dict(version='1.4', source_sha256=before, pdf_sha256=sha(HERE/(STEM+'.pdf')),
                    compiler=subprocess.check_output([compiler,'--version'],text=True).strip(),
                    status='built; visual inspection recorded separately', published=False)
    (HERE/'PAPER66_build_v1_4.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Built source-bound PAPER66 v1.4 PDF; no publication')

if __name__ == '__main__':
    main()
