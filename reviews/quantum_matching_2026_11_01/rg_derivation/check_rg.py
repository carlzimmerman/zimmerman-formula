"""Independent explicit SU(5) tensor/RG contractions and exact CS dictionary.

No TP01 mass implementation is imported. No running solution or potential
pressure root is evaluated. --out names a fresh bounded-run result file.
"""
import argparse
import json
import math
from pathlib import Path
import resource
import sys

import numpy as np
import sympy as S


def su5_basis():
    out=[]
    for i in range(5):
        for j in range(i+1,5):
            a=np.zeros((5,5),complex);a[i,j]=a[j,i]=1/math.sqrt(2);out.append(a)
            b=np.zeros((5,5),complex);b[i,j]=-1j/math.sqrt(2);b[j,i]=1j/math.sqrt(2);out.append(b)
    for k in range(1,5):
        a=np.zeros((5,5),complex)
        for j in range(k):a[j,j]=1/math.sqrt(k*(k+1))
        a[k,k]=-k/math.sqrt(k*(k+1));out.append(a)
    return np.asarray(out)


def raw_yukawa(T,h,lam):
    d=np.empty((24,24,24),complex)
    for a in range(24):
        for b in range(24):
            anti=(T[a]@T[b]+T[b]@T[a])/2
            d[a,b]=np.einsum('ij,cji->c',anti,T)
    Y=np.zeros((49,49,49),complex)
    for a in range(24):
        Y[0,1+a,1+a]=Y[1+a,0,1+a]=Y[1+a,1+a,0]=h
    for a in range(24):
        for b in range(24):
            for c in range(24):
                v=lam*d[a,b,c]
                Y[1+a,1+b,25+c]=v
                Y[1+a,25+c,1+b]=v
                Y[25+c,1+a,1+b]=v
    return Y,d


def expected(h,lam,g):
    one=[12*h*h,h*h+21*lam*lam/10-10*g*g,21*lam*lam/20-10*g*g]
    two=[-24*h**4-252*h*h*lam*lam/5+240*g*g*h*h,
         -13*h**4-21*h*h*lam*lam/5-1323*lam**4/200+21*g*g*lam*lam+50*g**4,
         -21*h*h*lam*lam/10-441*lam**4/100+21*g*g*lam*lam/2+50*g**4]
    return np.r_[one[0],np.repeat(one[1],24),np.repeat(one[2],24)],np.r_[two[0],np.repeat(two[1],24),np.repeat(two[2],24)]


def exact_dictionary():
    f,h,lam,g,L,X=S.symbols('f h lam g L X',positive=True)
    GX,GA,GB=S.symbols('GX GA GB',real=True)
    D=30*h*h+lam*lam;U=f*f*lam*lam/D
    generic={f:f*GX,h:h*(GX+2*GA),lam:lam*(GB+2*GA),g:S.Integer(0)}
    def flow(v,betas):return sum(betas[p]*S.diff(v,p) for p in betas)
    eff=(lam*lam*GX+30*h*h*GB)/D
    checks={}
    def zero(name,v):
        val=S.factor(v);checks[name]=bool(val==0);assert val==0,(name,str(val))
    zero('f_eff_running_generic',flow(S.log(f)+S.log(lam)-S.log(D)/2,generic)-eff)
    zero('T_running_generic',flow(S.log(D)/2-S.log(lam),generic)-GX+eff)
    zero('B_characteristic_generic',flow(S.log(h)-S.log(lam),generic)-GX+GB)
    drift=flow((S.log(2)+S.log(f)+S.log(h)-S.log(D))/2,generic)+GA
    zero('A_normal_drift_generic',drift-lam*lam*(GX-GB)/D)
    G1X=12*h*h;G1A=h*h+S.Rational(21,10)*lam*lam-10*g*g;G1B=S.Rational(21,20)*lam*lam-10*g*g
    G2X=-24*h**4-S.Rational(252,5)*h*h*lam*lam+240*g*g*h*h
    G2A=-13*h**4-S.Rational(21,5)*h*h*lam*lam-S.Rational(1323,200)*lam**4+21*g*g*lam*lam+50*g**4
    G2B=-S.Rational(21,10)*h*h*lam*lam-S.Rational(441,100)*lam**4+S.Rational(21,2)*g*g*lam*lam+50*g**4
    betas={f:f*G1X/L,h:h*(G1X+2*G1A)/L,lam:lam*(G1B+2*G1A)/L,g:-5*g**3/L}
    beta2={f:f*G2X/L**2,h:h*(G2X+2*G2A)/L**2,lam:lam*(G2B+2*G2A)/L**2,g:g**3*(150*g*g-10*h*h-S.Rational(63,2)*lam*lam)/L**2}
    s4=6*f*f*h*h*lam*lam*(29*lam*lam-200*g*g)/D**2
    C1=flow(U,betas);C2=flow(U,beta2)
    zero('one_loop_CS_full_supertrace',C1-s4/(2*L))
    zero('two_loop_U0_running_generic',C2-2*U*(lam*lam*G2X+30*h*h*G2B)/(L**2*D))
    critical={g*g:S.Rational(29,200)*lam*lam}
    drift_critical=S.factor(flow(29*lam*lam-200*g*g,betas).subs(critical))
    zero('critical_surface_drift',drift_critical-S.Rational(29,4)*lam*lam*(16*h*h+13*lam*lam)/L)
    gammaeff=(lam*lam*G1X+30*h*h*G1B)/(L*D)
    geffdot=S.factor(flow(gammaeff,betas).subs(critical))
    oldratio=S.Rational(29,12)*h*h*lam*lam*(16*h*h+13*lam*lam)/(L**2*D)
    zero('old_LL_curvature_dictionary',S.Rational(2,9)*geffdot-oldratio)
    return {'checks':checks,'C1':str(S.factor(C1)),'C2':str(S.factor(C2)),
            'critical_surface_drift':str(drift_critical),'gamma_eff_dot_critical':str(geffdot),
            'two_loop_gamma_coefficients':{'X':str(G2X),'A':str(G2A),'B':str(G2B)}}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    T=su5_basis();cas=np.r_[0.,np.full(48,5.)]
    gram=np.einsum('aij,bji->ab',T,T);assert np.max(abs(gram-np.eye(24)))<1e-13
    rows=[]
    for h,lam,g in [(1.,0.,0.),(0.,1.,0.),(1.,1.,0.),(1.,1.,1.),(0.,1.,1.),(1.,0.,1.),(.03,.02,.01)]:
        Y,d=raw_yukawa(T,h,lam)
        assert np.max(abs(Y-Y.transpose(2,1,0)))<1e-13
        P=.5*np.einsum('npq,rpq->nr',Y,Y.conj(),optimize=True)
        one=P-2*g*g*np.diag(cas)
        quartic=-np.einsum('imn,nr,mrj->ij',Y.conj(),P,Y,optimize=True)
        gramY=np.einsum('ipq,jpq->ij',Y.conj(),Y,optimize=True)
        gaugeY=2*np.einsum('ipq,p,jpq->ij',Y.conj(),cas,Y,optimize=True)-cas[:,None]*gramY
        pure=2*g**4*np.diag(cas*10+2*cas**2-3*5*cas)
        two=quartic+g*g*gaugeY+pure
        exp1,exp2=expected(h,lam,g)
        gauge_trace=float(np.einsum('ijk,ijk,k->',Y.conj(),Y,cas).real/24)
        row={'h':h,'lambda':lam,'g':g,'one_loop_matrix_max_error':float(np.max(abs(one-np.diag(exp1)))),
             'two_loop_matrix_max_error':float(np.max(abs(two-np.diag(exp2)))),
             'gauge_Yukawa_trace':gauge_trace,'gauge_trace_expected':10*h*h+31.5*lam*lam,
             'symmetric_group_contraction_max_error':float(np.max(abs(np.einsum('abc,abd->cd',d,d.conj())-2.1*np.eye(24))))}
        assert max(row['one_loop_matrix_max_error'],row['two_loop_matrix_max_error'],abs(row['gauge_Yukawa_trace']-row['gauge_trace_expected']),row['symmetric_group_contraction_max_error'])<2e-10,row
        rows.append(row)
    exact=exact_dictionary();rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    assert rss<1073741824
    result={'claim_id':'TP02-INDEPENDENT-RG','coefficient_cases':rows,'exact_dictionary':exact,'peak_RSS_bytes':rss,
            'software':{'python':sys.version,'numpy':np.__version__,'sympy':S.__version__},
            'non_claims':['No pressure/RG evolution or complete finite2loop threshold run','Finite contractions support only declared cases; universal coefficients use explicit group reduction in DERIVATION.md']}
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'coefficient_cases':len(rows),'exact_identities':len(exact['checks']),'max_two_loop_matrix_error':max(r['two_loop_matrix_max_error'] for r in rows),'peak_RSS_bytes':rss}))

if __name__=='__main__':main()
