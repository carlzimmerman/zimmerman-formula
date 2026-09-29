import fitz, sys, collections, re, json
import numpy as np
names="NGC0338 NGC1167 NGC1324 NGC2599 NGC2713 NGC2862 NGC5440 NGC5533 NGC5635 NGC5790 UGC02849 UGC02885 UGC08179 UGC12591 UGC12811".split()
def isnum(t):
    try: float(t.replace('−','-')); return True
    except: return False
def run(n, verbose=True):
    p=fitz.open(f"../images/atlas/{n}_all.pdf")[0]
    H=p.rect.height; W=p.rect.width
    words=p.get_text("words")
    # locate (c)
    cw=[w for w in words if w[4]=='(c)'][0]
    cy=(cw[1]+cw[3])/2
    reg=lambda r: r.x1<0.52*W and r.y0>cy-5
    draws=[d for d in p.get_drawings() if reg(d['rect'])]
    wds=[w for w in words if (w[2]<0.52*W and w[1]>cy-5)]
    # xlabels: numeric words at the bottom-most row
    nums=[w for w in wds if isnum(w[4])]
    ymax=max((w[1]+w[3])/2 for w in nums)
    xl=[w for w in nums if abs((w[1]+w[3])/2-ymax)<3]
    # vertical ticks (width 0, height 2)
    vt=[d['rect'] for d in draws if d['rect'].width<0.01 and 1.5<d['rect'].height<2.6]
    ht=[d['rect'] for d in draws if d['rect'].height<0.01 and 1.5<d['rect'].width<2.6]
    xs=[];vals=[]
    for w in xl:
        cx=(w[0]+w[2])/2
        cand=[r for r in vt if abs(r.x0-cx)<2.5]
        if cand:
            r=min(cand,key=lambda r:abs(r.y0-ymax))
            xs.append(r.x0); vals.append(float(w[4]))
    A=np.polyfit(vals,xs,1)  # x = A0*val + A1
    # main panel y labels: numeric words with x<40, y between top of c and residual
    yl=[w for w in nums if w[2]<40 and float(w[4])>=20 ]
    ys=[];yv=[]
    for w in yl:
        cy_=(w[1]+w[3])/2
        cand=[r for r in ht if abs(r.y0-cy_)<3.5]
        if cand:
            r=min(cand,key=lambda r:abs(r.y0-cy_)); ys.append(r.y0); yv.append(float(w[4]))
    B=np.polyfit(ys,yv,1) if len(ys)>=2 else None
    mk=collections.defaultdict(list)
    for d in draws:
        r=d['rect']
        if 3.5<r.width<7.5 and 3.5<r.height<7.5:
            key=(d['type'],round(r.width,1),str(d.get('fill') and tuple(round(c,2) for c in d['fill'])),str(d.get('color') and tuple(round(c,2) for c in d['color'])))
            mk[key].append(((r.x0+r.x1)/2,(r.y0+r.y1)/2))
    out={}
    if verbose:
        print("=====",n,"xcal",A,"nlab",len(xs),"ycal",B)
    for k,v in mk.items():
        R=[(x-A[1])/A[0] for x,y in v]
        V=[B[0]*y+B[1] for x,y in v] if B is not None else []
        if verbose:
            print(k,len(v))
        out[str(k)]=(R,V)
    return out
if __name__=="__main__":
    for n in (sys.argv[1:] or names):
        o=run(n)
        for k,(R,V) in o.items():
            idx=np.argsort(R)
            print("  ",k,"n=",len(R))
            print("     R:",[round(R[i],1) for i in idx])
            print("     V:",[round(V[i]) for i in idx])
