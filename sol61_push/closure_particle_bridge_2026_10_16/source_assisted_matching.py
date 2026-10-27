"""Exact source-pole factorization and the pole-free source-assisted tree.

Fraction arithmetic; dimensionless m=1. Spatial squared weights make
on-shell irrational momenta exact without floating square roots.
"""
import itertools
import json
import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

out=Path(sys.argv[1]);assert out.is_dir()
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)});assert value,name

def partitions(items,k):
    if k==1:
        yield (tuple(items),);return
    if len(items)<k:return
    first,rest=items[0],items[1:]
    for n in range(len(rest)+1):
        for chosen in itertools.combinations(rest,n):
            remain=tuple(i for i in rest if i not in chosen)
            if len(remain)<k-1:continue
            for tail in partitions(remain,k-1):yield ((first,)+chosen,)+tail

def tree_terms(charges,lam):
    full=tuple(range(len(charges)))
    def qq(s):return sum(charges[i] for i in s)
    def vertex(q):
        if sorted(q) in ([-2,1,1],[-1,-1,2]):return 1,F(2)
        if sorted(q)==[-1,-1,1,1]:return 0,4*lam
        return None
    @lru_cache(None)
    def current(s):
        if abs(qq(s)) not in (1,2):return ()
        if len(s)==1:return ((0,F(1),()),)
        result=[]
        for k in (2,3):
            for parts in partitions(s,k):
                v=vertex([-qq(s)]+[qq(t) for t in parts])
                if v is None:continue
                products=[(v[0],v[1],())]
                for part in parts:
                    products=[(a+d,b*e,c+f) for a,b,c in products for d,e,f in current(part)]
                result.extend((a,b,c+((s,abs(qq(s))),)) for a,b,c in products)
        return tuple(result)
    result=[]
    for k in (2,3):
        for parts in partitions(full[1:],k):
            v=vertex([charges[0]]+[qq(t) for t in parts])
            if v is None:continue
            products=[(v[0],-v[1],())]
            for part in parts:
                products=[(a+d,b*e,c+f) for a,b,c in products for d,e,f in current(part)]
            result.extend(products)
    return result

def evaluate(terms,momenta,weights,Msq,strip=()):
    full=set(range(len(momenta)))
    def key(s):
        a,b=tuple(sorted(s)),tuple(sorted(full-set(s)))
        return min((a,b),key=lambda x:(len(x),x))
    wanted=set(key(s) for s in strip)
    result={}
    for power,coefficient,props in terms:
        if not wanted.issubset({key(s) for s,q in props}):continue
        value=coefficient
        for s,q in props:
            if key(s) in wanted:continue
            p=[sum(momenta[i][j] for i in s) for j in range(4)]
            denominator=p[0]**2-sum(weights[j]*p[j+1]**2 for j in range(3))-(F(1) if q==1 else Msq)
            assert denominator,('unremoved real intermediate state',s)
            value/=denominator
        result[power]=result.get(power,F(0))+value
    return {p:c for p,c in result.items() if c}

def shifted(poly,power,factor):return {k+power:v*factor for k,v in poly.items()}

records=[]
for mass in (F(5001,2500),F(5,2),F(3)):
    for ratio in (F(1),F(2),F(4)):
        lam=1+1/ratio;Msq=mass*mass
        charge6=[1,1,-1,-1,-1,1]
        t6=tree_terms(charge6,lam)
        check('six-point topology count '+str((mass,ratio)),len(t6)==36)
        ef=(mass+2)/2
        weights=(Msq/4-1,Msq/4-1,ef*ef-1)
        moms=[(mass/2,1,0,0),(mass/2,-1,0,0),(F(1),0,0,0),(F(1),0,0,0),(-ef,0,0,-1),(-ef,0,0,1)]
        q5=[2,-1,-1,-1,1]
        p5=[(mass,0,0,0)]+moms[2:]
        t5=tree_terms(q5,lam)
        check('five-point topology count '+str((mass,ratio)),len(t5)==6)
        r6=evaluate(t6,moms,weights,Msq,strip=((0,1),))
        a5=evaluate(t5,p5,weights,Msq)
        check('single source pole factorization '+str((mass,ratio)),r6==shifted(a5,1,F(2)))

        # Both incoming same-charge pairs at their physical source mass.
        weights=(Msq/4-1,Msq/4-1,Msq-1)
        moms=[(mass/2,1,0,0),(mass/2,-1,0,0),(mass/2,0,1,0),(mass/2,0,-1,0),(-mass,0,0,-1),(-mass,0,0,1)]
        p4=[(mass,0,0,0),(mass,0,0,0)]+moms[4:]
        a4=evaluate(tree_terms([2,-2,-1,1],lam),p4,weights,Msq)
        rdouble=evaluate(t6,moms,weights,Msq,strip=((0,1),(2,3)))
        check('double source pole factorization '+str((mass,ratio)),rdouble==shifted(a4,2,F(4)))
        p5=[(mass,0,0,0)]+moms[2:]
        r5=evaluate(t5,p5,weights,Msq,strip=((1,2),))
        check('nested five-point source pole '+str((mass,ratio)),r5==shifted(a4,1,F(2)))

        # Different physical crossing: X+Phi+Phi* -> Phi+Phi, all
        # incoming particles at rest. The entire tree is pole-free.
        ef=(mass+2)/2;weights=(F(1),F(1),ef*ef-1)
        mixedq=[2,1,-1,-1,-1]
        mixedp=[(mass,0,0,0),(F(1),0,0,0),(F(1),0,0,0),(-ef,0,0,-1),(-ef,0,0,1)]
        mixed=evaluate(tree_terms(mixedq,lam),mixedp,weights,Msq)
        expected={1:8*lam*(mass+1)/(mass*(mass+2)),
                  3:-2*(5*mass+8)/(mass**2*(mass+1)*(mass+2))}
        check('mixed source-assisted threshold formula '+str((mass,ratio)),mixed==expected)
        # Crossing of the six-daughter channel 3Phi+Phi* -> 2Phi:
        # its single real-source cut is exactly this pole-free 3to2.
        cutweights=(Msq/4-1,F(1),ef*ef-1)
        cutmoms=[(mass/2,1,0,0),(mass/2,-1,0,0),(F(1),0,0,0),(F(1),0,0,0),(-ef,0,0,-1),(-ef,0,0,1)]
        cut=evaluate(tree_terms([1,1,1,-1,-1,-1],lam),cutmoms,cutweights,Msq,strip=((0,1),))
        check('crossed six-point source cut '+str((mass,ratio)),cut==shifted(mixed,1,F(2)))
        g2=(Msq-4)/ratio
        reduced=mixed[1]+mixed[3]*g2
        check('mixed source-assisted threshold nonzero '+str((mass,ratio)),reduced>0)
        records.append({'M_over_m':str(mass),'r_lambda':str(ratio),
                        'threshold_M5_over_g_times_lambda_rep_over_m_squared':str(reduced),
                        'threshold_polynomial':{str(k):str(v) for k,v in mixed.items()}})

result={'verdict':'Exact physical source-pole residues require source-assisted 3to2 channels; mixed source/daughter crossing has a pole-free nonzero threshold amplitude',
        'records':records,'checks':checks,
        'non_claims':['Tree factorization is not a complete distributional RIS subtraction',
                      'No finite-temperature five/six-point reaction density in this exact script',
                      'Unstable external source treated in narrow quasiparticle description',
                      'No abundance, galaxy law, dark-energy magnitude or global novelty established']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('records','checks')},indent=2))
print('All %d exact controls passed.'%len(checks))
