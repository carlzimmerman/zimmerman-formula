#!/usr/bin/env python3
"""Action-derived two-scalar matter gate for the IC11 plateau, not global closure.

Ordinary massless matter is minimally coupled to physical g=exp(2w)*gtilde.
Its Einstein-frame pressure is exp(2w)*Y. The proposed auxiliary-curvature
repair changes the response to matter while preserving the vacuum envelope.
All constants use the frozen m=h0=1 IC10 normalization.
"""
import argparse
from functools import lru_cache
import json
import sympy as sp
import mpmath as mp
import ic10_local_clock as original


@lru_cache(None)
def build(balanced=False):
    source = original.build()
    S, w, P0 = source['S'], source['w'], source['P']
    Y, b = sp.symbols('Y b', real=True)
    X = sp.exp(-2*S)/2
    f = sp.Rational(5,64)*(2*X)**16
    B = sp.diff(P0,w,2)
    C = -sp.diff(P0,S,w)/(2*X)
    A = (sp.diff(P0+f,S,2)+2*sp.diff(P0+f,S))/(4*X*X)
    coefficient = (1/B+A/(C*C))/2 if balanced else b
    L = P0+f-coefficient*sp.diff(P0,w)**2/2+sp.exp(2*w)*Y
    terms = [L, sp.diff(L,w), sp.diff(L,S), sp.diff(L,Y), sp.diff(L,w,2),
             sp.diff(L,S,2), sp.diff(L,Y,2), sp.diff(L,S,w), sp.diff(L,Y,w), sp.diff(L,S,Y)]
    return dict(S=S,w=w,Y=Y,b=b,P0=P0,f=f,L=L,coefficient=coefficient,
                domain=sp.lambdify((S,w),(B,C),'mpmath',cse=True),
                evaluate=sp.lambdify((S,w,Y,b),terms,'mpmath',cse=True),
                raw=sp.lambdify((S,w,Y,b),L,'mpmath',cse=True))


def raw(S,w,Y,b):
    balanced = b=='balanced'
    return build(balanced)['raw'](S,w,Y,0 if balanced else b)


def state(S,Y,b):
    balanced = b=='balanced'
    S,Y,b = map(mp.mpf,(S,Y,0 if balanced else b))
    if S<=0 or Y<0 or b<0:
        raise ValueError('Require S>0, Y>=0, b>=0 in this chart')
    ev = build(balanced)['evaluate']
    seed = original.state(S)['w']
    w = mp.findroot(lambda w:ev(S,w,Y,b)[1],seed,
                    df=lambda w:ev(S,w,Y,b)[4],solver='newton',
                    tol=mp.power(10,-mp.mp.dps+8))
    if abs(mp.im(w))>mp.power(10,-mp.mp.dps+8) or not -S/2<mp.re(w)<0:
        raise ValueError('Matter auxiliary root outside -S/2<w<0')
    w = mp.re(w)
    if balanced and any(v==0 for v in build(True)['domain'](S,w)):
        raise ValueError('Balanced coefficient undefined at B=0 or C=0')
    L,Lw,LS,LY,Lww,LSS,LYY,LSw,LYw,LSY = ev(S,w,Y,b)
    if abs(Lw)>mp.power(10,-mp.mp.dps+8):
        raise ValueError('Matter auxiliary root residual exceeds tolerance')
    X = mp.exp(-2*S)/2
    # Derivatives at fixed velocities, then the actual auxiliary Schur complement.
    K = mp.matrix([[(LSS+LS-LSw*LSw/Lww)/(2*X),
                     mp.sqrt(Y/X)*(-LSY+LSw*LYw/Lww)],
                   [mp.sqrt(Y/X)*(-LSY+LSw*LYw/Lww),
                     LY+2*Y*(LYY-LYw*LYw/Lww)]])
    D = mp.diag([-LS/(2*X),LY])
    kinetic = list(mp.eigsy(K,eigvals_only=True))
    speeds = list(mp.eig(K**-1*D,left=False,right=False))
    cone_margin = list(mp.eigsy(K-D,eigvals_only=True))
    energy = -LS+2*Y*LY-L
    H = mp.sqrt(energy/(3*mp.exp(-mp.mpf(1)/6))) if energy>0 else mp.nan
    velocities = mp.matrix([mp.sqrt(2*X),mp.sqrt(2*Y)])
    vdot = -3*H*(K**-1)*D*velocities
    Sdot,Ydot = -vdot[0]/velocities[0], velocities[1]*vdot[1]
    wdot = -(LSw*Sdot+LYw*Ydot)/Lww
    r = mp.exp(S-2*w-mp.mpf(1)/6)*H
    return dict(S=S,Y=Y,b=b,repair='balanced' if balanced else 'constant',w=w,X=X,pressure=L,constraint=Lw,Lww=Lww,
                K=K,D=D,kinetic_eigenvalues=kinetic,speeds_squared=speeds,
                cone_margin_eigenvalues=cone_margin,energy=energy,activation_r=r,
                inside_eta_one=abs(r*r-1)<=mp.mpf(1)/4,
                physical_H=mp.exp(-w)*(H+wdot),
                healthy_causal=all(v>0 for v in kinetic) and D[0,0]>0 and D[1,1]>0
                    and min(cone_margin)>=-mp.mpf('1e-35'))


def fold(S):
    """Locate a velocity-space auxiliary fold, not a field Dirac-rank verdict."""
    S=mp.mpf(S)
    ev=build(True)['evaluate']
    seed=original.state(S)['w']+mp.mpf('.0001')
    w,Y=mp.findroot(lambda w,Y:(ev(S,w,Y,0)[1],ev(S,w,Y,0)[4]),
                    (seed,mp.mpf('.001')),tol=mp.power(10,-mp.mp.dps+8))
    if not -S/2<w<0 or Y<=0:
        raise ValueError('Fold outside stated chart')
    values=ev(S,w,Y,0)
    L,Lw,LS,LY,Lww,LSS,LYY,LSw,LYw,LSY=values
    X=mp.exp(-2*S)/2
    bare=mp.matrix([[(LSS+LS)/(2*X),-mp.sqrt(Y/X)*LSY],
                    [-mp.sqrt(Y/X)*LSY,LY+2*Y*LYY]])
    mixing=mp.matrix([-LSw/mp.sqrt(2*X),mp.sqrt(2*Y)*LYw])
    inverse=bare**-1
    canonical=Lww-(mixing.T*inverse*mixing)[0]
    bracket=mp.matrix([[0,canonical],[-canonical,0]])
    momentum=inverse+inverse*mixing*mixing.T*inverse/canonical
    return dict(S=S,w=w,Y=Y,constraint=Lw,Lww=Lww,
                canonical_auxiliary_coefficient=canonical,
                canonical_auxiliary_bracket=bracket,
                canonical_auxiliary_rank=sum(v>mp.mpf('1e-30') for v in mp.svd(bracket)[1]),
                reduced_momentum_hessian=momentum,
                reduced_momentum_eigenvalues=list(mp.eigsy(momentum,eigvals_only=True)))


def report():
    mp.mp.dps=50
    rows=[]
    for b in ('0','.01','balanced'):
        for S in ('.03','.05','.1','.2'):
            for Y in ('0','.0001','.01','.1'):
                try:
                    bg=state(S,Y,b)
                except (ValueError,ZeroDivisionError) as error:
                    rows.append(dict(S=S,Y=Y,repair=b,status='auxiliary root unresolved',
                                     error=str(error).splitlines()[0],healthy_causal=False))
                    continue
                row={k:mp.nstr(bg[k],22) for k in
                     ('S','Y','b','w','pressure','constraint','Lww','energy','activation_r','physical_H')}
                row.update({k:[mp.nstr(v,22) for v in bg[k]] for k in
                            ('kinetic_eigenvalues','speeds_squared','cone_margin_eigenvalues')})
                row.update({k:bg[k] for k in ('inside_eta_one','healthy_causal')})
                row['repair']=bg['repair']
                rows.append(row)
    return dict(candidate='IC11 pressure plus auxiliary-curvature trial',full_theory='OPEN',
                rows=rows,velocity_auxiliary_fold={k:mp.nstr(v,24) for k,v in fold('.1').items()},
                nonclaims=['Aligned homogeneous massless matter backgrounds only',
                'Matter roots outside eta=1 are continuation controls, not full-action solutions',
                'A root-solver failure is not proof that all real roots are absent',
                'Lww=0 alone is not a fixed-canonical-momentum Dirac-rank calculation',
                'No combined transition, all-matter stability, PPN, cluster or galaxy-pair fit'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-full-closure',action='store_true')
    args=parser.parse_args()
    print(json.dumps(report(),indent=2))
    raise SystemExit(2 if args.require_full_closure else 0)
