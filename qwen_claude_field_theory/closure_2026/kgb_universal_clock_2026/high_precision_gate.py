#!/usr/bin/env python3
"""Independent arbitrary-precision initial matching and next preservation.

The numerical roots are not interval-enclosed proofs. Next preservation tests
one shared j, and never supplies separate curvature values to the two halos.
"""
import argparse
import json
import mpmath as mp
import reduced_match as r


def normalized(eps,y,X,U,w,F):
    mu=-mp.expm1(-y);lam=mu+y*mp.exp(-y)
    rr=eps/mp.sqrt(y*mu);ry=-rr*lam/(2*y*mu);yr=1/ry
    B=1/(1-2*rr*y);Br=2*(y+rr*yr)*B*B;g=y*B
    rho=4*y*y*mp.exp(-y)/(rr*lam);b=Br/(2*B)
    p=mp.sqrt(B*U);Q=2*X+U;aa=g+2/rr
    P=(2*w*aa+mp.mpf('1.5')*w*w/F)/B
    L=2*F*rho+2*w*(g+b)/B+3*w*w/(F*B)
    S=2*F*aa*rho+4*w*(rr*g-1)/(rr*rr*B)
    gamma=p*rr*S/(2*Q*w);W=B*(L-X*rr*S/Q)/2
    H=((2/rr+w/F)*U-(2*g+w/F)*X)/p
    return dict(eps=eps,y=y,X=X,U=U,w=w,F=F,r=rr,ry=ry,B=B,g=g,p=p,Q=Q,
        P=P,H=H,kappa=2*P/F+H*gamma,gamma=gamma,W=W,Rrad=aa+3*w/(2*F),
        Dcoord=1+rr*w/(2*F))


def parts(a):
    eps,y,X,U,w,F=(a[k] for k in ('eps','y','X','U','w','F'))
    A=mp.matrix([-2*a['gamma']*a['Rrad']/a['p'],-a['gamma']/U])
    point=mp.matrix([y,X,U,w,F])
    L1=mp.matrix([1/(a['ry']*w),0,-2*a['g']*a['Q']/w,a['W']/w,1])
    B=mp.matrix([mp.diff(lambda t:normalized(eps,*(point+t*L1))[key],0)
                 for key in ('kappa','gamma')])
    return A,B


def next_drift(a,f):
    """L0+f L1 applied to E=A+f B, with f fixed (j=0)."""
    eps,y,X,U,w,F=(a[k] for k in ('eps','y','X','U','w','F'))
    point=mp.matrix([y,X,U,w,F])
    flow=mp.matrix([f/(a['ry']*w),1,-2-2*f*a['g']*a['Q']/w,f*a['W']/w,f])
    def E(t,index):
        A,B=parts(normalized(eps,*(point+t*flow)))
        return A[index]+f*B[index]
    return mp.matrix([mp.diff(lambda t:E(t,i),0) for i in range(2)])


def next_control(N,B):
    den=mp.fdot(B,B)
    if not den:
        # Zero/zero permits every j; return zero only as one witness.
        return (mp.mpf(0),N.copy()) if not mp.norm(N) else (None,N.copy())
    j=-mp.fdot(N,B)/den
    return j,N+j*B


def check_map(f,F,X):
    if not all(mp.isfinite(v) for v in (f,F,X)) or F<=0 or X<=0 or not f or not F-X*f:
        raise ValueError('singular or unsupported field/clock map')


def pair(theta,u1):
    dw1,y2,u2=[mp.exp(v) for v in theta]
    eps1,eps2,y1,X,F=map(mp.mpf,('1e-6','2e-6','.1','.5','.525'))
    base=normalized(eps1,y1,X,eps1*u1,-1,F)
    a=normalized(eps1,y1,X,eps1*u1,-mp.mpf('.05')*dw1*base['g'],F)
    bb=normalized(eps2,y2,X,eps2*u2,-1,F);aa=bb['g']+2/bb['r']
    disc=aa*aa+mp.mpf('1.5')*bb['B']*a['P']/F
    if not mp.isfinite(disc) or disc<=0:
        raise ValueError('pressure quadratic outside real regular branch')
    w2=bb['B']*a['P']/(aa+mp.sqrt(disc))
    b=normalized(eps2,y2,X,eps2*u2,w2,F)
    if min(a['Dcoord'],b['Dcoord'],a['B'],b['B'])<=0:
        raise ValueError('target coordinate branch is not regular and orientation-preserving')
    return a,b


def residual(theta,u1):
    a,b=pair(theta,u1);A1,B1=parts(a);A2,B2=parts(b);A=A1-A2;B=B1-B2
    return ((a['H']-b['H'])/(1+abs(a['H'])+abs(b['H'])),
        (a['gamma']-b['gamma'])/(1+abs(a['gamma'])+abs(b['gamma'])),
        (A[0]*B[1]-A[1]*B[0])/(mp.norm(A)*mp.norm(B)))


def run(u1='.03',dps=50):
    seed=r.solve((1.5,.08,float(u1)),u1=float(u1))
    if not seed['accepted_initial_root']:raise ArithmeticError('double starting seed not matched')
    with mp.workdps(dps):
        u=mp.mpf(u1);start=tuple(mp.log(mp.mpf(str(v))) for v in seed['parameters'])
        theta=mp.findroot(lambda *v:residual(v,u),start,tol=mp.mpf(10)**(-dps+12),maxsteps=30)
        a,b=pair(theta,u);A1,B1=parts(a);A2,B2=parts(b);A=A1-A2;B=B1-B2
        f=-mp.fdot(A,B)/mp.fdot(B,B)
        check_map(f,a['F'],a['X'])
        N=next_drift(a,f)-next_drift(b,f)
        j,err=next_control(N,B)
        norm_product=mp.norm(N)*mp.norm(B)
        normalized_obstruction=(N[0]*B[1]-N[1]*B[0])/norm_product if norm_product else (mp.mpf(0) if not mp.norm(N) else None)
        pivot=next((i for i in range(2) if B[i]),None)
        pivot_j=-N[pivot]/B[pivot] if pivot is not None else j
        pivot_res=N[1-pivot]+pivot_j*B[1-pivot] if pivot is not None else mp.norm(err)
        text=lambda v:None if v is None else mp.nstr(v,dps-5)
        return dict(u1=u1,dps=dps,parameters=[text(mp.exp(v)) for v in theta],f=text(f),
            Dfield=text(2*(a['F']-a['X']*f)),
            initial_normalized_residual=[text(v) for v in residual(theta,u)],
            first_preservation_relative=text(mp.norm(A+f*B)/(mp.norm(A)+abs(f)*mp.norm(B))),
            next_N=[text(v) for v in N],next_B=[text(v) for v in B],
            normalized_next_obstruction=text(normalized_obstruction),
            next_control_sector='zero_B' if not mp.norm(B) else 'nonzero_B',
            least_squares_j=text(j),least_squares_relative=text(mp.norm(err)/mp.norm(N) if mp.norm(N) else 0),
            pivot_j=text(pivot_j),pivot_remaining_residual=text(pivot_res),
            states=[{key:text(row[key]) for key in ('eps','y','X','U','w','F','Dcoord')} for row in (a,b)],
            scope='Arbitrary-precision pointwise matching and necessary next tangency; not interval-enclosed or full Dirac closure')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-next-preservation',action='store_true')
    args=parser.parse_args()
    rows=[]
    for u in ('.03','.128','.5'):
        for dps in (50,80):
            try:row=run(u,dps)
            except (ValueError,ArithmeticError,ZeroDivisionError) as exc:row=dict(u1=u,dps=dps,error=str(exc))
            rows.append(row);print('PRECISION_GATE='+json.dumps(row),flush=True)
    print('SUMMARY='+json.dumps(dict(attempts=len(rows),evaluated=sum('error' not in q for q in rows),
        scope='Three prescribed initial data at two precisions; no claim that all seeds or all actions are excluded')))
    if args.require_next_preservation and any('error' in row or row['normalized_next_obstruction'] is None or
            abs(mp.mpf(row['normalized_next_obstruction']))>mp.mpf('1e-25') for row in rows):
        return 2
    return 0


if __name__=='__main__':raise SystemExit(main())
