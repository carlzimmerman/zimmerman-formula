#!/usr/bin/env python3
"""Compute the clock-preservation source and solve for N on constrained slices.

No evolution theorem: this is one epoch, a periodic plane family, float64.
The geometric H0 flows are independently checked against canonical variations.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as s
from constraint_data import model, solve_case


def source_coefficients():
    A,m,v,X,Y=s.symbols('A m v X Y',real=True)
    q=1/(1+m);U=m*q*A;d=A*U/(2*q*(q*A+U));ell=q*q*m/2
    H=s.sqrt((s.Rational(7,10)+A)/3);O=A/(s.Rational(7,10)+A)
    mn=m*(3*O/2+3*v*(m+1)/(m+2))
    vn=(v-1)*(3*O*(3*m*m+8*m+6)/(2*(m+1)*(m+2))
                +3*v*(m*m+2*m+2)/(m+2)**2-2)
    def dt(f):return H*(-3*A*s.diff(f,A)+mn*s.diff(f,m)+vn*s.diff(f,v))
    P=-U*s.log((U-2*d*X)/(U-2*d*q*q))/2
    W=U+2*d*ell*(s.sqrt(1+Y/ell)-1)
    # Partial clock derivatives at fixed X,Y, not material derivatives along Q.
    values=[dt(dt(U)),dt(dt(P)),dt(W),s.diff(dt(W),Y)]
    point={A:s.Rational(1,10),m:s.Rational(1,10),v:s.Rational(1,2)}
    return s.lambdify((X,Y),[z.subs(point) for z in values],'numpy',cse=True)


def canonical_source_flow_check():
    a,b,c,pa,pb,pc,W,WY,cx,M=s.symbols('a b c pa pb pc W WY cx M',real=True)
    vol=s.exp(a+b+c);Y=s.exp(-2*a)*cx*cx
    # -delta H0/d log h_ii = delta(vol W)/delta log h_ii.
    pdot=[vol*(W-2*WY*Y),vol*W,vol*W]
    ps=[pa,pb,pc];K=-sum(ps)/(2*M*vol)
    Kx=(pa-sum(ps)/2)/(M*vol);Z=Kx*Y
    kd=sum(s.diff(K,p)*f for p,f in zip(ps,pdot))
    zd=sum(s.diff(Z,p)*f for p,f in zip(ps,pdot))
    assert s.simplify(kd-(-3*W/2+WY*Y)/M)==0
    assert s.simplify(zd-(-W*Y/2-WY*Y*Y)/M)==0
    return True


def case(amplitude,nmode,coeff):
    row,solution=solve_case(amplitude,nmode)
    if 'lowest_eigenvalues' not in row:raise AssertionError('constraint solve failed')
    fun,par=model();n=8*nmode;x=2*np.pi*np.arange(n)/n
    modes=np.arange(1,nmode+1)[:,None];cos=np.cos(modes*x)
    wave=np.fft.fftfreq(n,1/n)
    def diff(f,order=1):return np.fft.ifft((1j*wave)**order*np.fft.fft(f)).real
    conf=solution[:nmode]@cos;shear=solution[nmode:2*nmode]@cos
    Q=row['Q_zero_mode'];chix=-amplitude*par['q']*np.sin(x)
    gx=diff(conf);hxx=np.exp(-2*conf);Y=hxx*chix**2;X=Q*Q-Y
    P,PX,PXX,Pt,PtX,W,WY,WYY=[np.broadcast_to(z,(n,)) for z in fun(X,Y)]
    Vtt,Ptt,Wt,WYt=[np.broadcast_to(z,(n,)) for z in coeff(X,Y)]
    J=np.exp(-3*conf)*diff(np.exp(conf)*WY*chix)
    K=(Pt-par['Vt']+(4/3)*WY*Y*shear+2*Q*J)/(W-(2/3)*WY*Y)
    kx=(K+2*shear)/3;ky=(K-shear)/3;Z=kx*Y
    B=2*PX+4*Q*Q*PXX;rho=2*Q*Q*PX-P+par['U']
    R=hxx*(-4*diff(conf,2)-2*gx*gx)
    C=R+K*K-(kx*kx+2*ky*ky)-2*rho-2*par['Lambda']
    T=par['Vt']-Pt+W*K-2*WY*Z-2*Q*J
    # Normal C[1] flows, including off-shell terms in the functional bracket.
    dy=-2*Z
    dq=(2*np.exp(-3*conf)*diff(np.exp(conf)*PX*chix)-2*Q*PX*K+2*Q*PXX*dy)/B
    dx=2*Q*dq-dy
    dk=-R-K*K+PX*(3*Q*Q-Y)-3*P+3*par['U']+3*par['Lambda']+3*C/4
    dz=2*diff(conf,2)*hxx*Y-K*Z-2*kx*kx*Y+Y*(PX*(Q*Q+Y)-P+par['U'])+par['Lambda']*Y+Y*C/4
    dj=np.exp(-3*conf)*diff(np.exp(conf)*(WYY*dy*chix-2*WY*kx*chix))+WY*hxx*chix*diff(K)
    mass=-(K*T-PtX*dx+WY*dy*K+W*dk-2*WYY*dy*Z-2*WY*dz-2*dq*J-2*Q*dj)
    principal=W-2*Q*Q*WY-2*Y*WY-4*Q*Q*Y*WYY
    a2=np.exp(conf)*principal;volume=np.exp(3*conf);step=2*np.pi/n
    edge=np.fft.ifft(np.fft.fft(a2)*np.exp(1j*wave*step/2)).real
    matrix=np.diag(volume*mass+(edge+np.roll(edge,1))/step**2)
    for j in range(n):matrix[j,(j+1)%n]-=edge[j]/step**2;matrix[(j+1)%n,j]-=edge[j]/step**2
    eigen=np.linalg.eigvalsh(matrix)
    # Independent reconstruction must agree with the original constraint solver.
    assert abs(eigen[0]-row['lowest_eigenvalues'][0])<1e-8
    # d/dtau + {., H0}: h and chi do not move; Q does move at fixed canonical p_chi.
    Q0dot=-2*(J+Q*PtX)/B
    K0dot=-3*W/2+WY*Y
    Z0dot=-W*Y/2-WY*Y*Y
    J0dot=np.exp(-3*conf)*diff(np.exp(conf)*WYt*chix)
    source=Vtt-Ptt-2*Q*PtX*Q0dot+Wt*K+W*K0dot-2*WYt*Z-2*WY*Z0dot-2*Q0dot*J-2*Q*J0dot
    rhs=volume*source;lapse=np.linalg.solve(matrix,rhs)
    residual=np.max(np.abs(matrix@lapse-rhs))
    if amplitude==0:assert np.max(np.abs(lapse-1))<1e-9
    # Mutation: reversing the source changes the lapse sign. No positive N is assigned.
    opposite=np.linalg.solve(matrix,-rhs)
    assert np.max(np.abs(opposite+lapse))<1e-10
    return dict(amplitude=amplitude,modes=nmode,mesh=n,min_source=float(source.min()),
        min_lapse=float(lapse.min()),max_lapse=float(lapse.max()),residual=float(residual),
        positive_lapse=bool(lapse.min()>0),min_operator_eigenvalue=float(eigen[0]),
        source_reversal_control=float(opposite.max()),constraint_residual=row['full_C_residual'])


def main():
    assert canonical_source_flow_check()
    coeff=source_coefficients()
    rows=[case(e,n,coeff) for e in (0.,.001,.01,.05) for n in (8,16)]
    return dict(canonical_H0_metric_flows_checked=True,cases=rows,full_theory_status='OPEN',
        scope='Actual preservation source and lapse on eight plane-symmetric constrained slices; not nonlinear time evolution')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    result=main()
    if a.result_file:a.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
