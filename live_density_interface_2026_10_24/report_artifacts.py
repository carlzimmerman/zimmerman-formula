import argparse,json,runpy,shutil,hashlib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();p=Path(__file__).parent;dest=Path(a.output)
runpy.run_path(str(p/'assessment.py'))
runpy.run_path(str(p/'plot_results.py'))
out={}
for name in ['assessment.json','joint_result.png']:
    shutil.copy2(p/name,dest.parent/name);out[name]=hashlib.sha256((p/name).read_bytes()).hexdigest()
dest.write_text(json.dumps(out,indent=2)+'\n')
