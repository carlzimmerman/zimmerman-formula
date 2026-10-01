from fractions import Fraction as F
from pathlib import Path
import json,sys
import numpy as np

candidate=Path(sys.argv[1]);output=Path(sys.argv[2])
oldpath=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-028/fgf028_run_001/numeric_001/response_rows.npz')
old=np.load(oldpath,allow_pickle=False);new=np.load(candidate,allow_pickle=False)
Uf=np.asarray(old['combined_pressure']);Hf=np.asarray(new['combined_pressure'])
assert Uf.shape==(15,15) and Hf.shape==(15,16)
assert np.array_equal(Hf[:,:15],Uf)
assert np.array_equal(Hf[:,-1],new['new_column'])
H=[[F(float(x)) for x in row] for row in Hf]
L=[F(0)]*16;L[5]=-5;L[6]=5
dot=lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))
def rref(rows):
    a=[list(r) for r in rows];p=[];k=0
    for j in range(len(a[0])):
        i=next((i for i in range(k,len(a)) if a[i][j]),None)
        if i is None:continue
        a[k],a[i]=a[i],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
        for i in range(len(a)):
            if i!=k:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
        p.append(j);k+=1
        if k==len(a):break
    return a,p
R,piv=rref(H);assert piv==list(range(15))
v=[-r[-1] for r in R]+[F(1)]
assert all(dot(row,v)==0 for row in H)
sensitivity=dot(L,v);assert sensitivity!=0
assert len(rref(H+[L])[1])==16
# Independently solve full transpose, not block-subset elimination.
T,p=rref([list(col)+[x] for col,x in zip(zip(*[row[:15] for row in H]),L[:15])])
assert p==list(range(15));dual=[row[-1] for row in T]
assert [dot(dual,col) for col in zip(*[row[:15] for row in H])]==L[:15]
assert sensitivity==-dot(dual,[row[-1] for row in H])
# Independent rational monotone baseline: 1e-5/(1+x)^2, not worker exponential.
nodes=[F(str(x)) for x in [0,.18,.36,.54,.72,.90,1.10,1.28,1.46,1.64,1.82,2,2.5,3,4,5]]
base=[F(1,100000)/(1+x)**2 for x in nodes]
gaps=[base[i]-(base[i+1] if i<15 else 0) for i in range(16)]
dv=[v[i]-(v[i+1] if i<15 else 0) for i in range(16)]
eps=min(m/abs(d) for m,d in zip(gaps,dv) if d)/2
witnesses=[]
for sign in [-1,1]:
    w=[x+sign*eps*y for x,y in zip(base,v)]
    wg=[w[i]-(w[i+1] if i<15 else 0) for i in range(16)]
    assert min(wg)>0 and all(dot(row,w)==dot(row,base) for row in H)
    witnesses.append({'sign':sign,'pressure_exact':list(map(str,w)),'target_exact':str(dot(L,w)),'minimum_gap':float(min(wg))})
assert F(witnesses[1]['target_exact'])-F(witnesses[0]['target_exact'])==2*eps*sensitivity
coordinate=[F(0)]*15+[F(1)]
assert len(rref(H+[coordinate])[1])==16
assert len(rref(H+[H[0]])[1])==15
wrong=L[:];wrong[-1]=sensitivity
assert dot(wrong,v)==2*sensitivity # negative target mutation is detected
assert len(rref([row[:15] for row in H]+[L[:15]])[1])==15
res={'claim':'exact ambiguity after one support release in saved finite operator',
     'rank_H':15,'rank_with_target':16,'null_direction_exact':list(map(str,v)),
     'target_sensitivity_dp5_exact':str(sensitivity),'target_sensitivity_dp5':float(sensitivity),
     'old_dual_exact':list(map(str,dual)),'baseline_kind':'rational 1e-5/(1+x)^2',
     'baseline_exact':list(map(str,base)),'epsilon_exact':str(eps),'epsilon':float(eps),
     'target_baseline':float(dot(L,base)),'target_difference':float(2*eps*sensitivity),
     'relative_target_width':float(abs(2*eps*sensitivity/dot(L,base))),
     'witnesses':witnesses,'all_checks_passed':True,
     'controls':{'old_columns_bitwise_unchanged':True,'released_offset':False,
     'fixed_p5_restores_old_identification':True,'new_coordinate_restores_rank':True,
     'duplicate_row_does_not':True,'wrong_target_detected':True},
     'limits':['exact on binary64 matrix only','synthetic profiles, not observed fit','no calibrated errors or force']}
output.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:res[k] for k in ['rank_H','rank_with_target','target_sensitivity_dp5','epsilon','relative_target_width','all_checks_passed']}))
