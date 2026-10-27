"""Read-only current repo context; headlines never become verified premises."""
from pathlib import Path
import subprocess
from config import CONFIG

def digest(obligation=None):
    root = CONFIG['root'].parent.parent
    try:
        r = subprocess.run(['git','log','-12','--format=%h %s'],cwd=root,
                           capture_output=True,text=True,timeout=10)
        commits = r.stdout.splitlines()
    except (OSError,subprocess.SubprocessError): commits=[]
    data=[]
    directories = [root/'real_research/data',root/'data',root/'fable_independent_2026/data']
    if obligation == 'cluster-source-closure': directories.insert(0, root/'real_research/data/xcop')
    seen=set()
    for directory in directories:
        if not directory.exists(): continue
        for p in sorted(directory.rglob('*')):
            if len(data)>=80: break
            if p not in seen and p.is_file() and p.suffix in ('.csv','.tsv','.fits','.dat','.json') and p.resolve().is_relative_to(root):
                seen.add(p)
                entry={'path':str(p.relative_to(root)),'bytes':p.stat().st_size}
                if p.suffix in ('.csv','.tsv'):
                    with p.open(errors='replace') as f: entry['header']=f.readline(500).strip()
                elif p.suffix == '.fits':
                    try:
                        from astropy.io import fits
                        with fits.open(p, mode='readonly', memmap=True) as hdus:
                            table = next((h for h in hdus if isinstance(h, (fits.BinTableHDU, fits.TableHDU))), None)
                            if table is not None:
                                entry['columns'] = [{'name':c.name, 'unit':c.unit} for c in table.columns][:24]
                                entry['columns_truncated'] = len(table.columns) > 24
                    except (ImportError, OSError, ValueError) as e:
                        entry['header_error'] = str(e)[:200]
                data.append(entry)
    return {'recent_commit_subjects_unverified':commits,'available_inputs':data}
