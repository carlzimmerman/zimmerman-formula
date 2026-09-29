import fitz, numpy as np, json
from extract import isnum, names
rc=json.load(open('rc_extracted.json'))
out={}
for n in names:
    p=fitz.open(f"../images/atlas/{n}_all.pdf")[0]
    W=p.rect.width
    words=p.get_text("words")
    cw=[w for w in words if w[4]=='(c)'][0]; cy=(cw[1]+cw[3])/2
    draws=[d for d in p.get_drawings() if d['rect'].x1<0.52*W and d['rect'].y0>cy-5]
    nums=[w for w in words if w[2]<0.52*W and w[1]>cy-5 and isnum(w[4])]
    ht=[d['rect'] for d in draws if d['rect'].height<0.01 and 1.5<d['rect'].width<2.6]
    ys=[];yv=[]
    for w in nums:
        if w[2]<40 and float(w[4])>=20:
            c=(w[1]+w[3])/2
            cand=[r for r in ht if abs(r.y0-c)<3.5]
            if cand:
                r=min(cand,key=lambda r:abs(r.y0-c)); ys.append(r.y0); yv.append(float(w[4]))
    B=np.polyfit(ys,yv,1); ppk=abs(B[0])   # km/s per pt
    # HI markers: black fs, width 4.4-4.7
    mk=[]
    for d in draws:
        r=d['rect']
        if d['type']=='fs' and 4.4<r.width<4.7 and d.get('fill') and d['fill']==(0.0,0.0,0.0):
            mk.append(((r.x0+r.x1)/2,(r.y0+r.y1)/2))
    vl=[d['rect'] for d in draws if d['rect'].width<0.01 and d['rect'].height>2.6]
    errs=[]
    for x,y in mk:
        c=[r for r in vl if abs(r.x0-x)<0.6 and r.y0<=y+0.3 and r.y1>=y-0.3 and r.height<200]
        if c:
            r=min(c,key=lambda r:r.height)
            errs.append((x,(r.y1-r.y0)/2*ppk))
        else: errs.append((x,None))
    errs.sort()
    out[n]=[e for x,e in errs]
    print(n, len(mk), [None if e is None else round(e) for x,e in errs][-6:])
json.dump(out,open('rc_errs.json','w'))
