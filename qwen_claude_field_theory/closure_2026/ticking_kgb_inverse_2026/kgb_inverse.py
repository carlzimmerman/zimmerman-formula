#!/usr/bin/env python3
"""Ticking shift-symmetric KGB: variation, inverse static construction, health.

S=int sqrt(-g)[m R/2 + P(X)-G(X) box(phi)] + Sm[g], X=-dphi^2/2.
The exact worked power-law solution has Lambda=0. It is NOT a universal
exponential-MOND action. Its one fixed power selects one flat circular speed.
"""
import argparse
from functools import lru_cache
import json
import sympy as s


def radial_variation():
    A,B,R,q,p=s.symbols('A B R q p',positive=True)
    Ap,Bp,Rp,pp,A2,B2,R2,p2=s.symbols('Ap Bp Rp pp A2 B2 R2 p2',real=True)
    jets=[A,B,R,p,Ap,Bp,Rp,pp];nexts=[Ap,Bp,Rp,pp,A2,B2,R2,p2]
    D=lambda f:sum(s.diff(f,x)*v for x,v in zip(jets,nexts))
    X=q*q/(2*A)-p*p/(2*B);P=s.Function('P');Gx=s.Function('Gx')
    measure=s.sqrt(A*B)*R*R
    L=measure*(P(X)+Gx(X)*D(X)*p/B)
    EL=lambda x,xp:s.diff(L,x)-D(s.diff(L,xp))
    rho=s.simplify(-2*A*EL(A,Ap)/measure)
    pr=s.simplify(2*B*EL(B,Bp)/measure)
    pt=s.simplify(R*EL(R,Rp)/(2*measure))
    Jr=s.simplify(-EL(p,pp)/measure)
    PX=P(X).fdiff()
    target=PX*p/B+Gx(X)*X*Ap/(A*B)-2*Gx(X)*p*p*Rp/(B*B*R)
    zero_current=s.solve(Jr,PX)[0]
    r0,p0,t0=[s.simplify(e.subs(PX,zero_current)) for e in (rho,pr,pt)]
    # Vary g_tr before setting it to zero: stationary is not automatically static.
    C,Cp=s.symbols('C Cp',real=True)
    det=A*B+C*C;Xc=(B*q*q-2*C*q*p-A*p*p)/(2*det)
    DXc=D(Xc)+s.diff(Xc,C)*Cp
    Lc=s.sqrt(det)*R*R*(P(Xc)+Gx(Xc)*(C*q+A*p)*DXc/det)
    off={C:0,Cp:0}
    ELC=s.diff(Lc,C).subs(off)-D(s.diff(Lc,Cp).subs(off))
    mixed_flux=s.simplify(-A*ELC/measure)
    residuals=[s.simplify(Jr-target),s.simplify(pr-P(X)-p*Jr),
               s.simplify(r0-(2*X*Gx(X)*D(X)/p-P(X))),s.simplify(p0-P(X)),
               s.simplify(2*B*X*(t0-p0)-p*p*(r0+p0)),s.simplify(mixed_flux-q*Jr)]
    return dict(L_reduced=L,X=X,radial_current=Jr,rho=rho,pr=pr,pt=pt,
                mixed_energy_flux=mixed_flux,zero_current_rho=r0,zero_current_pr=p0,
                zero_current_pt=t0,identity_residuals=residuals,
                static_clock_limit=s.simplify((rho+pt).subs(q,0)),
                ticking_rho_plus_pt=s.factor(r0+t0))


@lru_cache(None)
def principal_template():
    """Differentiate the expanded scalar EL after eliminating Ricci with Einstein.
    Eta has signature (-+++); the returned sign gives canonical P=X positive
    time kinetic coefficient. No sound speed or matrix entry is supplied.
    """
    m,X,G1,G2,P,P1,P2=s.symbols('m X G1 G2 P P1 P2',real=True)
    v=s.Matrix(s.symbols('v0:4',real=True));eta=s.diag(-1,1,1,1)
    H=s.zeros(4);hvars={}
    for i in range(4):
        for j in range(i,4):
            hvars[i,j]=s.Symbol('H'+str(i)+str(j),real=True)
            H[i,j]=H[j,i]=hvars[i,j]
    vc=eta*v;dX=-H*vc;box=s.trace(eta*H)
    vdX=(vc.T*dX)[0];dX2=(dX.T*eta*dX)[0];H2=s.trace(eta*H*eta*H)
    T=(P1-G1*box)*v*v.T+P*eta-G1*(dX*v.T+v*dX.T)+eta*G1*vdX
    trace=s.trace(eta*T)
    Rvv=(vc.T*(T-eta*trace/2)*vc)[0]/m
    E=P1*box+P2*vdX-G1*(box**2-H2-Rvv)-G2*(box*vdX+dX2)
    M=s.zeros(4)
    for (i,j),h in hvars.items():
        M[i,j]=M[j,i]=-s.diff(E,h)/(1 if i==j else 2)
    return dict(m=m,X=X,G1=G1,G2=G2,P=P,P1=P1,P2=P2,v=v,H=H,M=M,E=E,T=T)


def principal_at(mass,gradient,hessian,G1,G2):
    a=principal_template()
    subs={a['m']:mass,a['G1']:G1,a['G2']:G2,a['P']:0,a['P1']:0,a['P2']:0}
    subs.update(dict(zip(a['v'],gradient)))
    subs.update({a['H'][i,j]:hessian[i,j] for i in range(4) for j in range(i,4)})
    def canonical(e):
        e=s.factor(s.simplify(e))
        # Factor radicands before simplification. No force=True or unproved
        # square-root sign replacement: positive parameter assumptions apply.
        for _ in range(2):
            e=e.replace(lambda z:z.is_Pow and z.exp==s.S.Half,
                        lambda z:s.sqrt(s.factor(z.base)))
            e=s.factor(e)
        return s.simplify(e)
    return a['M'].subs(subs,simultaneous=True).applyfunc(canonical)


def general_inverse():
    """Local inverse with nonzero radial pressure; Ward supplies current closure.

    This is a branchwise identity, not the missing cross-mass consistency solve.
    X' and p must be nonzero, beta>0, and rho+pr nonzero.
    """
    A,B,R,X,beta=s.symbols('A B R X beta',positive=True)
    Ap,Rp,Xp,p,rho,pr,prp,q=s.symbols('Ap Rp Xp p rho pr prp q',real=True)
    pt=pr+beta*(rho+pr)
    GX=p*(rho+pr)/(2*X*Xp);PX=prp/Xp
    J=PX*p/B+GX*X*Ap/(A*B)-2*GX*p**2*Rp/(B**2*R)
    # Divide out p before substituting p^2; preserves the chosen nonzero branch.
    reduced=s.factor(J*B*Xp/p).subs(p**2,2*B*X*beta)
    ward=prp+(rho+pr)*Ap/(2*A)+2*(pr-pt)*Rp/R
    residuals=[s.factor(2*X*GX*Xp/p-pr-rho),
               s.factor(pr+GX*p*Xp/B-pt).subs(p**2,2*B*X*beta)]
    return dict(beta_definition='(pt-pr)/(rho+pr)',X=q*q/(2*A*(1+beta)),
                p_squared=B*q*q*beta/(A*(1+beta)),P='pr(r)',GX=GX,
                current_ward_residual=s.factor(reduced-ward),
                stress_residuals=[s.factor(x) for x in residuals],
                scope='Local monotone X branch; universal P(X),G(X) across masses not established')


def halo():
    w,m=s.symbols('w m',positive=True);r=s.symbols('r',positive=True)
    # Exact flat-rotation ansatz. Tensor geometry is independently differentiated.
    t,theta,phi=s.symbols('t theta phi',real=True);coords=[t,r,theta,phi]
    A=r**(2*w);B=1+2*w
    metric=s.diag(-A,B,r*r,r*r*s.sin(theta)**2);inverse=metric.inv()
    Gamma=[[[s.simplify(sum(inverse[a,d]*(s.diff(metric[d,c],coords[b])+
            s.diff(metric[d,b],coords[c])-s.diff(metric[b,c],coords[d]))/2 for d in range(4)))
            for c in range(4)] for b in range(4)] for a in range(4)]
    Ricci=s.Matrix(4,4,lambda a,b:s.simplify(sum(s.diff(Gamma[c][a][b],coords[c])-
          s.diff(Gamma[c][a][c],coords[b])+sum(Gamma[c][c][d]*Gamma[d][a][b]-
          Gamma[c][b][d]*Gamma[d][a][c] for d in range(4)) for c in range(4))))
    Einstein=inverse*Ricci-s.eye(4)*s.trace(inverse*Ricci)/2
    geometric=[s.simplify(-m*Einstein[0,0]),s.simplify(m*Einstein[1,1]),s.simplify(m*Einstein[2,2])]
    X=1/(A*(2+w));p=s.sqrt(B*w*X)
    # Inverse construction from the Einstein density, not an assigned G power.
    GX=s.factor(geometric[0]*p/(2*X*s.diff(X,r)))
    n=s.Symbol('n',positive=True)
    power=s.solve(s.diff(GX,r)/GX-(n-1)*s.diff(X,r)/X,n)[0]
    GXX=s.factor(s.diff(GX,r)/s.diff(X,r))
    box=(s.diff(p,r)+(s.diff(A,r)/(2*A)+2/r)*p)/B
    xp=s.diff(X,r)
    rho=-(GX*box)/A-GX*xp*p/B
    pr=-GX*box*p*p/B-GX*xp*p/B
    pt=GX*xp*p/B
    current=-GX*(box*p+xp)/B
    # Local orthonormal frame at r=1; choose q=-1 consistently with expansion.
    p1=p.subs(r,1)
    H=s.Matrix([[-w*p1/B,w/s.sqrt(B),0,0],[w/s.sqrt(B),-w*p1/B,0,0],
                [0,0,p1/B,0],[0,0,0,p1/B]])
    M=principal_at(m,s.Matrix([-1,p1/s.sqrt(B),0,0]),H,GX.subs(r,1),GXX.subs(r,1))
    Mb=s.Symbol('baryon_mass',positive=True)
    fixed_velocity=s.solve(s.Eq(n,power),w)[0]
    return dict(symbols=(w,m),metric_A=A,metric_B=B,X=X,phi_radial_gradient=p,
                Einstein_stress=geometric,action_G_derivative=GX,power_index=s.factor(power),
                action_G_second_derivative=GXX,
                Einstein_residuals=[s.factor(s.simplify(a-b)) for a,b in zip((rho,pr,pt),geometric)],
                current_residual=s.factor(current),principal_matrix=M,kinetic=M[0,0],
                radial_speed2=s.factor(-M[1,1]/M[0,0]),angular_speed2=s.factor(-M[2,2]/M[0,0]),
                fixed_action_velocity_squared=fixed_velocity,
                fixed_action_velocity_mass_derivative=s.diff(fixed_velocity,Mb))


def cosmology():
    n,Q,g0,m=s.symbols('n Q g0 m',positive=True)
    q=-Q;X=Q*Q/2;GX=-g0*n*X**(n-1);GXX=(n-1)*GX/X
    H=s.factor(2*q*X*GX/m)  # Nonzero root of 3mH^2=6HqXG_X.
    J=6*H*X*GX
    Qdot=s.factor(-3*H*J/s.diff(J,Q));qdot=-Qdot
    Hdot=s.diff(H,Q)*Qdot
    rho=6*H*q*X*GX;pressure=-2*X*GX*qdot
    Hess=s.diag(qdot,-H*q,-H*q,-H*q)
    M=principal_at(m,s.Matrix([q,0,0,0]),Hess,GX,GXX)
    return dict(H=H,shift_charge=J,Qdot=Qdot,rho=rho,pressure=pressure,
                equation_of_state=s.factor(pressure/rho),
                scale_factor_power=s.factor(-H*H/Hdot),
                kinetic_in_units_X2GX2_over_m=s.factor(M[0,0]/(X*X*GX*GX/m)),
                speed2=s.factor(-M[1,1]/M[0,0]),
                background_residuals=[s.simplify(3*m*H*H-rho),
                    s.simplify(-m*(2*Hdot+3*H*H)-pressure),s.simplify(s.diff(J,Q)*Qdot+3*H*J)])


@lru_cache(None)
def derive():
    return dict(variation=radial_variation(),general_inverse=general_inverse(),halo=halo(),cosmology=cosmology(),
                status='OPEN: constructive exact halo and expanding clock branch, NOT a universal exponential MOND theory')


def serial(a):
    if isinstance(a,dict):return {str(k):serial(v) for k,v in a.items()}
    if isinstance(a,(list,tuple)):return [serial(v) for v in a]
    return str(a)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--require-closure',action='store_true')
    args=parser.parse_args();a=derive();print(json.dumps(serial(a),indent=2))
    residuals=(a['variation']['identity_residuals']+a['halo']['Einstein_residuals']+
               a['cosmology']['background_residuals']+a['general_inverse']['stress_residuals']+
               [a['general_inverse']['current_ward_residual']])
    if any(x!=0 for x in residuals):return 1
    return 2 if args.require_closure else 0


if __name__=='__main__':raise SystemExit(main())
