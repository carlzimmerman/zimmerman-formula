import json, numpy as np
res=json.load(open('rc_extracted.json'))
print("Lelli+16 algorithm (mean of 2 outermost; include next inward if |V_i - Vbar|/Vbar<=0.05; iterate) on extracted HI points")
out={}
for n,r in res.items():
    R=np.array(r['R']);V=np.array(r['V']);N=len(V)
    inc=[N-1,N-2]; 
    Vbar=V[inc].mean()
    i=N-3
    while i>=0 and abs(V[i]-Vbar)/Vbar<=0.05:
        inc.append(i); Vbar=V[inc].mean(); i-=1
    # rejected at first iteration? check third point
    first_ok = (N>=3 and abs(V[N-3]-V[[N-1,N-2]].mean())/V[[N-1,N-2]].mean()<=0.05)
    Rin=R[min(inc)]
    out[n]=dict(Vflat_alg=float(Vbar),Rin=float(Rin),Rout=float(R[-1]),npts=len(inc),first_ok=bool(first_ok),vtab=r['vtab'][0],Nhi=N)
    print(f"{n:9s} alg V_flat={Vbar:6.1f} (N={len(inc):2d}, R={Rin:5.1f}-{R[-1]:5.1f} kpc; 3-pt test passed={first_ok})  table={r['vtab'][0]}±{r['vtab'][1]}  diff={Vbar-r['vtab'][0]:+.0f}")
json.dump(out,open('lelli_alg.json','w'))
