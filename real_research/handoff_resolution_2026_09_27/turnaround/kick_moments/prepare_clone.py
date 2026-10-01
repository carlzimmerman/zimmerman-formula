from pathlib import Path
import hashlib,json,difflib
here=Path(__file__).resolve().parent;source=here.parents[1]/'collapse/engine_constant_j_force_refresh.py'
old=source.read_text();new=old.replace('import CFG5_common as C','import CFG5_common as C\nfrom exact_moments import kick_moments')
assert new!=old
new=new.replace('        fgal=None):','        fgal=None, trigger_cadence=5):')
new=new.replace('if trigger and nstep % 5 == 0:','if trigger and nstep % trigger_cadence == 0:')
start=new.index('                nh = rng.normal(');end=new.index('                budget["converted"]',start)
new=new[:start]+'                vt = J[fire] / R[fire]\n                fe, vr2, vt2 = kick_moments(V[fire], vt, phi[fire], vk)\n'+new[end:]
(here/'engine_exact.py').write_text(new)
(here/'engine_exact.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(source),tofile='engine_exact.py')))
(here/'clone_provenance.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'clone_sha256':hashlib.sha256(new.encode()).hexdigest(),'changes':['import exact_moments','optional trigger_cadence default5','replace64-direction sampler with exact conditional moments'],'note':'Historical engine docstring retained unchanged; sampler description superseded by patch.'},indent=2))
