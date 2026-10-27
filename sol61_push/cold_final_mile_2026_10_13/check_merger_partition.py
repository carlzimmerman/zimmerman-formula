import json,sys
from fractions import Fraction as F
checks=0; examples=[]
for nroot in [2,3,4,10]:
    A=F(1); S=F(12); rp=S/nroot/A; rr=S/A
    def T(r):return min(A*r,S)
    def C(r):return min(nroot*A*r,S)
    def E(r):return max(F(0),C(r)-T(r))
    assert E(rp)==S*(1-F(1,nroot));checks+=1
    assert E(rr)==0 and C(rr)==S;checks+=1
    rmid=(rp+rr)/2
    assert E(rmid)<E(rp) and E(rmid)>0;checks+=1
    assert (E(rmid)-E(rp))/(rmid-rp)==-A;checks+=1
    # Holding the putative F=max(E) at larger radii double counts conserved mass.
    assert T(rr)+E(rp)>S;checks+=1
    examples.append(dict(N=nroot*nroot,r_progenitor_edge=str(rp),r_remnant_edge=str(rr),max_E=str(E(rp)),E_at_remnant_edge=str(E(rr)),mass_if_F_retained=str(T(rr)+E(rp))))
d=json.load(open('campaign_fresh_gravity/CFG726_merger_memory/cfg726_results.json'))
assert d['T_X']=='NOT RUN' and d['T_B']=='NOT RUN';checks+=1
assert sum(bool(v['ok']) for v in d['checks'].values())==10 and len(d['checks'])==13;checks+=1
assert all('FAILS' in v for v in d['verdict'].values());checks+=1
json.dump(dict(checks=checks,examples=examples,raw_verdict=d['verdict'],scope='Exact finite controls for the general cumulative partition reduction, not a score rerun'),open(sys.argv[1],'w'),indent=2)
