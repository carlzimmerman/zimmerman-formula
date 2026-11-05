#!/usr/bin/env python3
"""AZ40 bounded canonical-coupling audit; does not certify full health."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time
import mpmath as mp
import sympy as S

start=time.time()
parser=argparse.ArgumentParser()
parser.add_argument('--mode',choices=['main','exponent','normalization','kinetic'],default='main')
mode=parser.parse_args().mode
here=Path(__file__).resolve().parent
out=here/mode
out.mkdir(exist_ok=True)
checks=[]
def check(name,ok,value=None):
    checks.append(dict(name=name,passed=bool(ok),value=value))
def z(expr):
    return S.simplify(S.trigsimp(expr))==0

# A: open-set identity fixes the derivative coupling; no kappa prediction.
P,a,s,rho,kap,ow=S.symbols('P a s rho kappa opw',positive=True)
X,V,G=S.symbols('X V G',positive=True)
aa=kap*S.sqrt(G*(X+V))
check('universal_tie_requires_X_dependence',z(S.diff(aa,X)-aa/(2*(X+V))))
W=a*(-P-a*S.log(1-P/a))
ar=a/(2*rho); arr=-a/(4*rho**2)
Wr=S.diff(W,a)*ar
Wrr=S.diff(W,a,2)*ar**2+S.diff(W,a)*arr
rb=4*S.pi/kap**2
keff=S.simplify((1-Wr-ow*rho*Wrr).subs(P,a*s/(1+s)).subs({a:1,rho:rb}))
h=2*(s-S.log(1+s))-s*s/(1+s)
eps=kap**2/(8*S.pi)
target=1+eps*(h-ow*s**3/(2*(1+s)))
check('CT14_fixed_P_kinetic_formula',z(keff-target))
check('constant_density_known_answer',z(target.subs(ow,0)-(1+eps*h)))
asym=S.limit(target/s**2,s,S.oo)
check('large_s_negative_quadratic_coefficient',z(asym+eps*ow/2))

def coef_rows(dps):
    with mp.workdps(dps):
        rows=[]
        for ss,oo in itertools.product(['10','108.9','10000'],['.05','.3']):
            sv,ov=mp.mpf(ss),mp.mpf(oo)
            hv=2*(sv-mp.log1p(sv))-sv*sv/(1+sv)
            val=1+(hv-ov*sv**3/(2*(1+sv)))/(32*mp.pi)
            rows.append(dict(s=ss,opw=oo,kinetic=mp.nstr(val,dps)))
        return rows
c40,c80=coef_rows(40),coef_rows(80)
with mp.workdps(90):
    coef_err=max(abs(mp.mpf(x['kinetic'])-mp.mpf(y['kinetic']))/(1+abs(mp.mpf(y['kinetic']))) for x,y in zip(c40,c80))
check('density_coefficient_precision_pair',coef_err<=mp.mpf('1e-30'),str(coef_err))

# B: exact FRW branch, in Mpl=1 units; Vstar=1 only fixes energy units.
b,y=S.symbols('beta y',positive=True)
BB=2*S.sqrt(3*(1-b))/(3*b)
power=-2*(1-b)/b
baseV=S.sinh(y)**power
trialV=baseV*S.sinh(y) if mode=='exponent' else baseV
rp=2*baseV/(1+b)
rd=rp/S.sinh(y)**2
H2=rp/(3*S.tanh(y)**2)
yn=3*b*S.tanh(y)/2
phin=BB*yn
phinn=S.diff(phin,y)*yn
hn=-S.Rational(3,2)*(1-b*S.tanh(y)**2)
kin=S.simplify(H2*phin**2/2)
ractual=kin+trialV
pphi=kin-trialV
xi=kap**2 if mode=='normalization' else 2*kap**2/(1+b)
# Divide by positive baseV before simplifying fractional hyperbolic powers.
expressions={
 'canonical_kinetic':kin/baseV-(1-b)/(1+b),
 'Friedmann':(3*H2-rd-ractual)/baseV,
 'dust_continuity':(S.diff(rd,y)*yn+3*rd)/rd,
 'scalar_continuity':(S.diff(ractual,y)*yn+3*(ractual+pphi))/baseV,
 'constant_equation_of_state':(pphi+b*ractual)/baseV,
 'KG':(H2*(phinn+(3+hn)*phin)+S.diff(trialV,y)/BB)/baseV,
 'absolute_density_tie':xi*trialV/(kap**2*ractual)-1,
 'tie_logarithmic_slope':S.diff(trialV,y)/trialV/2-S.diff(ractual,y)/ractual/2,
 'H_log_derivative':S.diff(H2,y)*yn/(2*H2)-hn,
}
simplified={name:S.simplify(S.expand_power_base(e,force=True)) for name,e in expressions.items()}
for name,e in simplified.items():
    check('branch_symbolic_'+name,z(e),str(S.simplify(e)))

def numerical_branch():
    rows=[]
    with mp.workdps(60):
        for bs,ys in itertools.product(['1/3','2/3','9/10'],['1/10','1','3']):
            def rat(st):
                parts=st.split('/')
                return mp.mpf(parts[0])/(mp.mpf(parts[1]) if len(parts)>1 else 1)
            bv,yv=rat(bs),rat(ys)
            scale=2*mp.sqrt(3*(1-bv))/(3*bv)
            vb=lambda yy:mp.sinh(yy)**(-2*(1-bv)/bv)
            vt=lambda yy:vb(yy)*(mp.sinh(yy) if mode=='exponent' else 1)
            rn=lambda yy:2*vb(yy)/(1+bv)
            dust=lambda yy:rn(yy)/mp.sinh(yy)**2
            h2=lambda yy:rn(yy)/(3*mp.tanh(yy)**2)
            yyN=lambda yy:3*bv*mp.tanh(yy)/2
            pn=lambda yy:scale*yyN(yy)
            ke=lambda yy:h2(yy)*pn(yy)**2/2
            ra=lambda yy:ke(yy)+vt(yy)
            pr=lambda yy:ke(yy)-vt(yy)
            hlog=mp.diff(h2,yv)*yyN(yv)/(2*h2(yv))
            ratio=1 if mode=='normalization' else 2/(1+bv)
            residuals={
              'Friedmann':(3*h2(yv)-dust(yv)-ra(yv))/(1+3*h2(yv)),
              'dust_continuity':(mp.diff(dust,yv)*yyN(yv)+3*dust(yv))/(1+3*dust(yv)),
              'scalar_continuity':(mp.diff(ra,yv)*yyN(yv)+3*(ra(yv)+pr(yv)))/(1+3*ra(yv)),
              'KG':(h2(yv)*(mp.diff(pn,yv)*yyN(yv)+(3+hlog)*pn(yv))+mp.diff(vt,yv)/scale)/(1+abs(mp.diff(vt,yv)/scale)),
              'absolute_density_tie':ratio*vt(yv)/ra(yv)-1,
              'tie_logarithmic_slope':mp.diff(vt,yv)/vt(yv)/2-mp.diff(ra,yv)/ra(yv)/2,
            }
            rows.append(dict(beta=bs,y=ys,residuals={k:mp.nstr(v,60) for k,v in residuals.items()}))
    return rows
branch=numerical_branch()
for key in branch[0]['residuals']:
    worst=max(abs(mp.mpf(r['residuals'][key])) for r in branch)
    check('branch_60digit_'+key,worst<=mp.mpf('1e-40'),str(worst))

# C: rederive the lapse/P constraint and velocity blocks from the action.
k,D,v=S.symbols('k D v',positive=True)
Phi,pol,phidot,sigdot=S.symbols('Phi pol phidot sigdot',real=True)
sign=-1 if mode=='kinetic' else 1
L=-k*k*Phi*Phi/2+k*pol*Phi-k*pol*sigdot-D*pol*pol/2+sign*phidot**2/2-v*Phi*phidot
con=S.Matrix([Phi,pol]); vel=S.Matrix([phidot,sigdot])
C=S.hessian(L,con)
Bc=S.Matrix(2,2,lambda i,j:S.diff(L,con[i],vel[j]))
A=S.hessian(L,vel)
K=S.simplify(A-Bc.T*C.inv()*Bc)
det=S.factor(K.det())
check('static_constraint_blocks_from_action',C==S.Matrix([[-k*k,k],[k,-D]]) and Bc==S.Matrix([[-v,0],[0,-k]]))
check('canonical_reduced_K11',z(K[0,0]-(1+v*v*D/(k*k*(D-1)))))
check('canonical_reduced_determinant',z(det-(k*k+v*v)/(D-1)))
check('zero_v_known_answer',all(z(e) for e in K.subs(v,0)-S.diag(1,k*k/(D-1))))

def principal_rows(dps):
    with mp.workdps(dps):
        rows=[]
        for ss,kk,gg,vv in itertools.product(['.1','1','108.9','10000'],['1','100'],['0','1'],['0','1','10']):
            sv,kv,gv,velv=map(mp.mpf,[ss,kk,gg,vv])
            dv=(1+sv)**2+gv*kv**2
            cm=mp.matrix([[-kv**2,kv],[kv,-dv]])
            bc=mp.matrix([[-velv,0],[0,-kv]])
            reduced=mp.matrix([[sign,0],[0,0]])-bc.T*(cm**-1)*bc
            dd=mp.det(reduced)
            rows.append(dict(s=ss,k=kk,gamma=gg,v=vv,K11=mp.nstr(reduced[0,0],dps),determinant=mp.nstr(dd,dps)))
        return rows
p40,p80=principal_rows(40),principal_rows(80)
with mp.workdps(90):
    perr=max(abs(mp.mpf(x['determinant'])-mp.mpf(y['determinant']))/(1+abs(mp.mpf(y['determinant']))) for x,y in zip(p40,p80))
for name,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
    check(name+'_principal_precision_pair',perr<=mp.mpf('1e-30'),str(perr))
    check(name+'_principal_positive',all(mp.mpf(r['K11'])>0 and mp.mpf(r['determinant'])>0 for r in p80))
    check(name+'_zero_v_positive',all(mp.mpf(r['K11'])>0 and mp.mpf(r['determinant'])>0 for r in p80 if r['v']=='0'))
    check(name+'_density_large_s_negative',all(mp.mpf(r['kinetic'])<0 for r in c80 if r['s']=='10000'))

result=dict(label='NO VERDICT',scope='Full coupled action health unresolved; restricted algebraic obstruction and branch checks',
 mode=mode,kappa='1/2 FITTED; not theory closed',footings={'canonical':9.3603e-11,'alt':1.1312e-10},
 checks=checks,density_rows_40=c40,density_rows_80=c80,branch_rows=branch,
 principal_rows_40=p40,principal_rows_80=p80,kinetic_matrix=str(K),determinant=str(det),
 asymptotic_density_coefficient=str(asym),free_coefficient='kappa_squared=xi*(1+beta)/2 on the selected branch',
 source_hashes={str(p.relative_to(here.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
   for p in [Path(__file__),here/'FROZEN_CRITERIA.md',here.parent.parent/'reviews/missing_links_2026_11_04/FROZEN_CRITERIA.md',
             here.parent.parent/'complete_theory_2026_11_04/CT14_Cpp_health/ct14_h2_static.py']},
 seconds=time.time()-start,max_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
failed=[c['name'] for c in checks if not c['passed']]
print(json.dumps(dict(mode=mode,passed=len(checks)-len(failed),total=len(checks),failed=failed,
                     seconds=result['seconds']),indent=2))
raise SystemExit(bool(failed))
