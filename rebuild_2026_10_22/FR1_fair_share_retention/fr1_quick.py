import json,os,glob,numpy as np
HH=("h0672","h0686")
def cells(R):
    c=R["grader"]["canonical"]["clusters"]["cells"];O={}
    for h in HH:
        m=R["M_outer"][f"canonical|{h}"];O[h]={k:dict(v) for k,v in c[h].items()}
        for k,A in [("G-OUT-Mall",m["all"])]+[(f"G-OUT-M{t+1}",m["terc"][t]) for t in range(3)]:
            v=O[h][k];s=v["s"]*A/v["meas"];v.update(meas=A,s=s,Z=(A-v["pred"])/s)
    return O
for f in sorted(glob.glob('cache_jobs/*.json')):
    R=json.load(open(f));O=cells(R);b=sorted({k for h in HH for k,v in O[h].items() if abs(v["Z"])>2});x=R["footings"]["canonical"]
    print(os.path.basename(f)[:-5],15-len(b),'M3 %+.2f %+.2f'%(O['h0672']['G-OUT-M3']['Z'],O['h0686']['G-OUT-M3']['Z']),'X %+.3f %.3f'%(x['mean'],x['rms']),b,R['zn1'].get('no_fs'),R['zn1'].get('no_tail'))
