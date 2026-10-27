
import hashlib,json,os,runpy,sys
from pathlib import Path
script, mirror, record, writable = map(Path,sys.argv[1:5])
reads={}; recording=False
def audit(event,args):
 global recording
 if recording or event!='open': return
 filename,mode,flags=args
 if not isinstance(filename,(str,bytes,os.PathLike)): return
 p=Path(filename).absolute()
 write=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
 if write:
  resolved=p.resolve()
  # Temporary CLASS builds and ordinary OS null device are allowed.
  if not (resolved.is_relative_to(writable.resolve()) or str(resolved).startswith('/private/tmp/') or str(resolved).startswith('/private/var/folders/') or str(resolved)=='/dev/null'):
   raise PermissionError('reproduction blocked write outside output scope: '+str(p))
 else:
  try:
   if p.is_file() and (str(p).startswith(str(mirror)) or '/zimmerman-formula/' in str(p)):
    recording=True
    reads[str(p)]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'resolved':str(p.resolve())}
  finally: recording=False
sys.addaudithook(audit)
sys.path.insert(0,str(script.parent))
try:
 runpy.run_path(str(script),run_name='__main__')
finally:
 recording=True
 for name,row in reads.items():
  p=Path(name)
  row['sha256_after']=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
 record.write_text(json.dumps(reads,indent=2))
