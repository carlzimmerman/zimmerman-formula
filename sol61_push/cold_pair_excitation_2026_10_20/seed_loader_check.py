"""Test initial-state loading by exact replay, before mode-seed evolution."""
from pathlib import Path
import sys,json,subprocess,hashlib,struct,resource
import numpy as np

binary,out=map(Path,sys.argv[1:3]);binary=binary.resolve()
here=Path(__file__).resolve().parent
checks=[]
def ck(name,value):
    checks.append({'name':name,'pass':bool(value)})
    if not value:raise AssertionError(name)
def execute(tag,seed,*,kind='snapshot',dx=.75,nr=48,nz=128,T=5):
    d=out/tag;d.mkdir()
    argv=[str(binary),str(here/'profile_Q80000.bin'),str(d),str(nr),str(nz),str(dx),
          '.005',str(T),'24','0','0','.9217883882803886',kind,'5','0',str(seed)]
    proc=subprocess.run(argv,capture_output=True,text=True)
    (d/'stdout.txt').write_text(proc.stdout);(d/'stderr.txt').write_text(proc.stderr)
    return proc,d
for tag,nr,nz,dx in [('iso_dx075_dt005',48,128,.75),('moving_dx05_dt005',72,192,.5)]:
    base=here/'preflight_v2_run_001'/tag
    proc,d=execute(tag,base/'snap_t000000000.bin',nr=nr,nz=nz,dx=dx)
    ck(tag+' accepts recorded initial state',proc.returncode==0)
    for ti in [0,5000]:
        a=(d/f'snap_t{ti:09d}.bin').read_bytes();b=(base/f'snap_t{ti:09d}.bin').read_bytes()
        ck(tag+f' t{ti} complete snapshot byte-identical replay',a==b)
    ck(tag+' full diagnostic history identical replay',(d/'log.jsonl').read_bytes()==(base/'log.jsonl').read_bytes())
    row=json.loads(proc.stdout)
    ck(tag+' RAM below1GB',row['peak_rss_macos_bytes']<1000000000)
base=(here/'preflight_v2_run_001/iso_dx075_dt005/snap_t000000000.bin').read_bytes()
bad=[]
for name,offset,fmt,value in [('magic',0,'8s',b'WRONG000'),('nr',8,'i',49),
                               ('dx',16,'d',.5),('nonzero_time',24,'d',1.),
                               ('nonfinite_field',32,'d',float('nan'))]:
    content=bytearray(base);struct.pack_into('<'+fmt,content,offset,value)
    bad.append((name,content))
bad.extend([('truncated',base[:-8]),('trailing_byte',base+b'x')])
for name,content in bad:
    seed=out/(name+'.bin');seed.write_bytes(content)
    proc,_=execute('reject_'+name,seed,T=0)
    ck(name+' invalid seed rejected',proc.returncode!=0)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('check driver RAM below1GB',rss<1000000000)
result={'scope':'Exact existing static/moving full-field replay and invalid-input rejection, not a mode/dwarf result',
        'checks':checks,'all_checks_pass':all(x['pass'] for x in checks),'n_checks':len(checks),'peak_rss_bytes_macos':rss}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
