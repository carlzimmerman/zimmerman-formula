"""Exact labeled-tree amplitudes for the specified complex carrier at threshold.

Polynomial in g_c/m; m=lambda_rep=1 in normalized amplitudes. All internal
invariants are rational, since the final spatial momentum is sqrt(3)*m.
No finite-temperature, finite-width, loop or cosmological rate is claimed.
"""
import itertools
import json
import math
import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

out=Path(sys.argv[1]); assert out.is_dir()
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)}); assert value,name

def partitions(items,k):
    """Unordered set partitions into nonempty subsets, ordered by first label."""
    if k==1:
        yield (tuple(items),); return
    if len(items)<k: return
    first=items[0]; rest=items[1:]
    for size in range(len(rest)+1):
        for selected in itertools.combinations(rest,size):
            chosen=set(selected)
            remainder=tuple(i for i in rest if i not in chosen)
            if len(remainder)<k-1: continue
            for tail in partitions(remainder,k-1):
                yield ((first,)+selected,)+tail

def poly_add(a,b):
    out=dict(a)
    for power,c in b.items(): out[power]=out.get(power,F(0))+c
    return {p:c for p,c in out.items() if c}

def poly_mul(a,b):
    out={}
    for p,c in a.items():
        for q,d in b.items(): out[p+q]=out.get(p+q,F(0))+c*d
    return {p:c for p,c in out.items() if c}

def vertex(charges,lam):
    qq=sorted(charges)
    if qq in ([-2,1,1],[-1,-1,2]): return {1:F(2)}
    if qq==[-1,-1,1,1]: return {0:4*lam}
    return {}

def amplitude(charges,momenta,Msq,lam):
    # A subtree charge is the sum of its external incoming charges. It
    # attaches at the next vertex carrying that incoming charge. Its own
    # root vertex therefore carries the opposite charge.
    def charge(items): return sum(charges[i] for i in items)
    def denominator(items):
        energy=sum(momenta[i][0] for i in items)
        zz=sum(momenta[i][1] for i in items)
        return energy*energy-3*zz*zz-(F(1) if abs(charge(items))==1 else Msq)
    @lru_cache(None)
    def current(items):
        qq=charge(items)
        if abs(qq) not in (1,2): return {}
        if len(items)==1: return {0:F(1)}
        result={}
        for child_count in (2,3):
            for parts in partitions(items,child_count):
                coupling=vertex([-qq]+[charge(child) for child in parts],lam)
                if not coupling: continue
                product=coupling
                for child in parts: product=poly_mul(product,current(child))
                result=poly_add(result,product)
        if not result: return {}
        den=denominator(items)
        assert den, ('on-shell internal propagator',items)
        return {power:c/den for power,c in result.items()}
    # Root is tagged external leg zero; no root propagator.
    result={}
    remaining=tuple(range(1,len(charges)))
    for child_count in (2,3):
        for parts in partitions(remaining,child_count):
            product=vertex([charges[0]]+[charge(child) for child in parts],lam)
            if not product: continue
            for child in parts: product=poly_mul(product,current(child))
            result=poly_add(result,product)
    return {power:-c for power,c in result.items()}

def evaluate_even(poly,g2):
    assert all(power%2==0 for power in poly)
    return sum(c*g2**(power//2) for power,c in poly.items())

def explicit_six_diagrams(qq,moms,Msq,lam):
    """Independent topology enumeration: 9 quartic/quartic, 18 mixed,
    9 four-cubic trees; no off-shell-current recursion."""
    positive=[i for i,q in enumerate(qq) if q==1]
    negative=[i for i,q in enumerate(qq) if q==-1]
    def d(items,field_mass2):
        en=sum(moms[i][0] for i in items)
        zz=sum(moms[i][1] for i in items)
        return en*en-3*zz*zz-field_mass2
    sq,sm,sc=F(0),F(0),F(0)
    counts=[0,0,0]
    # Unique triple with two positive and one negative external fields.
    for pair in itertools.combinations(positive,2):
        for neg in negative:
            sq+=1/d(pair+(neg,),F(1));counts[0]+=1
    # The endpoint cubic has a same-charge external pair; the middle
    # cubic has one external of opposite charge; the quartic has the rest.
    for same,opposite in ((positive,negative),(negative,positive)):
        for pair in itertools.combinations(same,2):
            for single in opposite:
                rest=tuple(i for i in range(6) if i not in pair+(single,))
                sm+=1/(d(pair,Msq)*d(rest,F(1)));counts[1]+=1
    # Two endpoint pairs, one positive and one negative; the single
    # internal daughter joins their two inner cubic vertices.
    for pp in itertools.combinations(positive,2):
        for mm in itertools.combinations(negative,2):
            remaining_negative=next(i for i in negative if i not in mm)
            sc+=1/(d(pp,Msq)*d(mm,Msq)*d(pp+(remaining_negative,),F(1)))
            counts[2]+=1
    assert counts==[9,18,9]
    return {0:-16*lam*lam*sq,2:-16*lam*sm,4:-16*sc}

rows=[]
for u2 in (F(1,10000),F(1,2500),F(1,100),F(1,4)):
    for rr in (F(1),F(2),F(4)):
        delta=4*u2; Msq=4+delta; g2=delta/rr; lam=1+1/rr
        rest4=[(F(1),F(0)),(F(1),F(0)),(F(-1),F(0)),(F(-1),F(0))]
        same=amplitude([1,1,-1,-1],rest4,Msq,lam)
        opp=amplitude([1,-1,-1,1],rest4,Msq,lam)
        check('same-charge 4pt analytic u2=%s r=%s'%(u2,rr),evaluate_even(same,g2)==-4)
        check('crossed 4pt analytic u2=%s r=%s'%(u2,rr),
              evaluate_even(opp,g2)==-4*(lam-g2/Msq))
        moms=[(F(1),F(0))]*4+[(F(-2),F(-1)),(F(-2),F(1))]
        qq=[1,1,-1,-1,-1,1] # 2Phi 2Phi* -> Phi Phi*
        full=amplitude(qq,moms,Msq,lam)
        direct=explicit_six_diagrams(qq,moms,Msq,lam)
        check('independent 36-diagram polynomial u2=%s r=%s'%(u2,rr),full==direct)
        check('six-point pure quartic control u2=%s r=%s'%(u2,rr),full.get(0)==12*lam*lam)
        total=evaluate_even(full,g2)
        z=delta/(Msq+2)
        closed=12+24*(1-z)/rr+16*(1-z)**2/rr**2
        check('closed coefficient positive form u2=%s r=%s'%(u2,rr),total==closed and total>12)
        # A different rooted labeling checks the recursion's crossing and
        # permutation bookkeeping, including both final labels.
        for root in (1,2,4,5):
            order=[root]+[i for i in range(6) if i!=root]
            again=amplitude([qq[i] for i in order],[moms[i] for i in order],Msq,lam)
            check('root permutation u2=%s r=%s root=%s'%(u2,rr,root),again==full)
        check('specified 4to2 tree channel nonzero u2=%s r=%s'%(u2,rr),total!=0)
        rows.append({'u2':str(u2),'rlambda':str(rr),
                    'polynomial_in_g_over_m':{str(p):str(c) for p,c in full.items()},
                    'M4to2_over_lambda_rep_squared_over_m_squared':str(total)})

selected=next(r for r in rows if r['u2']=='1/2500' and r['rlambda']=='2')
coefficient=float(F(selected['M4to2_over_lambda_rep_squared_over_m_squared']))
# Rate screen for only the specified 2+2- -> +- channel in a dilute,
# nonrelativistic uncorrelated neutral gas. It omits the inverse gain and
# all other number-changing channels. It is not an abundance evolution.
prior=json.loads((Path(__file__).parent/'thermal_charge_run_002/results.json').read_text())
base=json.loads((Path(__file__).parent/'run_003/results.json').read_text())
m=.001; hbarc=1.973269804e-14; gev_g=1.7826619216279e-24
sigmanat=.3*gev_g/hbarc**2
lamrep=math.sqrt(8*math.pi*m**3*sigmanat)
number_rows=[]
for T,gs,gr in ((1e-6,3.91,3.36),(.001,10.75,10.75)):
    entropy=2*math.pi**2/45*gs*T**3
    n=base['portal']['yield_daughters']*entropy
    matrix=coefficient*lamrep**2/m**2
    # Initial identical factors 2! 2!, distinguishable final Phi/Phi*.
    # R=sqrt(3)|M|^2 n_+^2 n_-^2/(1024 pi m^4); Gamma_N=2R/n.
    gamma=math.sqrt(3)*matrix**2*n**3/(8192*math.pi*m**4)
    hh=1.66*math.sqrt(gr)*T*T/1.2209e19
    # Redshifted monochromatic control only, explicitly not the evolved gas.
    a=2.348e-13/T*(3.91/gs)**(1/3)
    um=base['collisionless_control']['a_nr']/a
    number_rows.append({'T_visible_GeV':T,'p_over_m_collisionless_control':um,
                        'Gamma_number_loss_one_channel_over_H':gamma/hh})

result={'verdict':'Complete vacuum tree threshold amplitude of one allowed mixed-charge 4to2 channel is nonzero at the sampled carrier points',
        'selected':selected,'rows':rows,'number_loss_screens':number_rows,
        'checks':checks,
        'non_claims':['No finite-temperature or in-medium amplitude',
                      'No near-resonance resummation or relativistic 4to2 rate',
                      'No Boltzmann evolution or abundance verdict',
                      'All channels and inverse rates remain necessary',
                      'Threshold rate at p/m near one is not quantitatively controlled',
                      'No global novelty or whole-theory closure']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('rows','checks')},indent=2))
print('All %d bounded controls passed.'%len(checks))
