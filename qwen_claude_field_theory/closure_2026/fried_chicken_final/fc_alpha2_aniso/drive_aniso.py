import time,sys,itertools; sys.path.insert(0,'.')
import fc_alpha2_fp_solve as M
T=time.time()
print("=== ISO cert (must give alpha_1=-4K_B) ===",flush=True)
for kbv in [0.05,0.3]:
    r=M.solve('iso',kbv,10.0,0.2,1.0)
    ok = (r[0]=='ok' and abs(r[1].real+4*kbv)<1e-6)
    print(f"  ISO K_B={kbv}: {r[0]} alpha_1={r[1].real:+.6f} target={-4*kbv:+.3f} {'PASS' if ok else 'FAIL'}",flush=True)
print(f"  [iso {time.time()-T:.0f}s]\n=== 18-point ANISO alpha_2 sweep ===",flush=True)
print(f"{'K_B':>5}{'K2':>7}{'Q0':>5}{'JY':>4} | {'alpha_1':>10} | {'a2_perp':>13}{'a2_par':>13} | D2resid",flush=True)
grid=list(itertools.product([0.05,0.3],[10.0,300.0],[0.2,0.9],[1.0,2.0]))
res=[]
for kbv,k2v,q0v,jyv in grid:
    t0=time.time(); r=M.solve('aniso',kbv,k2v,q0v,jyv)
    if r[0]!='ok':
        print(f"{kbv:5}{k2v:7}{q0v:5}{jyv:4} | {r[0]}",flush=True); continue
    _,a1,a2p,a2l=r; d2=abs(a2p-a2l)
    a1ok = abs(a1.real+4*kbv)<1e-6
    res.append((kbv,k2v,q0v,jyv,a1.real,a2p.real,a2l.real,d2))
    print(f"{kbv:5}{k2v:7}{q0v:5}{jyv:4} | {a1.real:+10.5f}{'' if a1ok else '!'} | {a2p.real:13.6g}{a2l.real:13.6g} | {d2:.1e} [{time.time()-t0:.0f}s]",flush=True)
if res:
    import math
    valid=[r for r in res if r[7]<1e-6]           # D2-consistent points
    print(f"\n{len(valid)}/{len(res)} points pass [D2] channel agreement",flush=True)
    if valid:
        amin=min(valid,key=lambda r:abs(r[5]))
        print(f"min |alpha_2| over D2-consistent grid = {abs(amin[5]):.4g}  at (K_B,K2,Q0,JY)={amin[:4]}",flush=True)
        print(f"observational bound |alpha_2| < 1e-7 (Nordtvedt/lunar)  => {'PASS band exists' if abs(amin[5])<1e-7 else 'ALL POINTS EXCEED BOUND'}",flush=True)
print(f"[total {time.time()-T:.0f}s]",flush=True)
