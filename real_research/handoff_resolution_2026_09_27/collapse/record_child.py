import sys,os,pathlib,hashlib,json,runpy
script=pathlib.Path(sys.argv[1]); output=pathlib.Path(sys.argv[2]); own=pathlib.Path(__file__).resolve().parent
repo=own.parents[2]; records={}; active=False
sys.dont_write_bytecode=True

def hook(event,args):
    global active
    if active or event!='open':return
    path,mode,flags=args
    if not isinstance(path,(str,bytes,os.PathLike)):return
    active=True
    try:
        p=pathlib.Path(path).resolve()
        write=(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)) if isinstance(flags,int) else any(x in (mode or '') for x in 'wax+')
        if write and not p.is_relative_to(own):raise PermissionError('Audit guard refuses write outside collapse lane: '+str(p))
        if not write and p.is_relative_to(repo) and p.is_file() and str(p) not in records:
            records[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
    finally:active=False
sys.addaudithook(hook)
try:
    sys.argv=[str(script)];runpy.run_path(str(script),run_name='__main__')
finally:
    active=True
    rows=[{'path':p,'before':h,'after':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()} for p,h in records.items()]
    output.write_text(json.dumps(rows,indent=2))
