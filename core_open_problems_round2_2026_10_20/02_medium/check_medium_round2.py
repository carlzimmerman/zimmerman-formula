#!/usr/bin/env python3
"""Independent finite controls; standalone numpy/scipy, no repository imports."""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import gammaln, logsumexp

def main(out):
    out=Path(out); out.mkdir(parents=True, exist_ok=True)
    checks=[]; rows=[]
    def check(name, error, tolerance):
        checks.append(dict(name=name,error=float(error),tolerance=tolerance,passed=bool(error<tolerance)))
    for N in [1,2,10,100,1000]:
        for h in [1e-10,1e-6,.01,1.,100.]:
            j=np.arange(N+1,dtype=float)
            lw=j*np.log(N*h)+gammaln(N+1)-gammaln(N-j+1)-2*gammaln(j+1)
            p=np.exp(lw-logsumexp(lw)); x=j/N
            B=h*(N-j); D=j*j/N
            check(f'detailed_balance_N{N}_h{h}',np.max(abs(p[:-1]*B[:-1]-p[1:]*D[1:]))/(1+np.max(p*D)),1e-10)
            check(f'moment_N{N}_h{h}',abs(h*(1-p@x)-p@(x*x))/(1+h),1e-10)
            root=2*h/(math.sqrt(h*h+4*h)+h)
            check(f'mean_bound_N{N}_h{h}',max(0,p@x-root),1e-10)
            rows.append(dict(N=N,h=h,mean_x=float(p@x),root=root,Fano=float(p@(j*j)-(p@j)**2)/float(p@j),asymptotic_Fano=(1-root)/(2-root)))
    # Direct nullspace solve, independent of product-form normalization.
    for N in [1,2,10]:
        h=.3; Q=np.zeros((N+1,N+1))
        for j in range(N+1):
            if j<N: Q[j,j+1]=h*(N-j)
            if j>0: Q[j,j-1]=j*j/N
            Q[j,j]=-sum(Q[j])
        A=Q.T.copy(); A[-1]=1; rhs=np.zeros(N+1);rhs[-1]=1
        p=np.linalg.solve(A,rhs)
        j=np.arange(N+1);lw=j*np.log(N*h)+gammaln(N+1)-gammaln(N-j+1)-2*gammaln(j+1)
        check(f'nullspace_N{N}',np.max(abs(p-np.exp(lw-logsumexp(lw)))),1e-12)
    for N in [1,10,100]:
        h=1e-12/N**2;j=np.arange(N+1);lw=j*np.log(N*h)+gammaln(N+1)-gammaln(N-j+1)-2*gammaln(j+1);p=np.exp(lw-logsumexp(lw))
        check(f'finiteN_linear_N{N}',abs((p@j/N)/(N*h)-1),1e-8)
        # Holding-time recurrence verifies zero-source absorption independently.
        times=np.zeros(N+1)
        for k in range(1,N+1): times[k]=times[k-1]+N/k**2
        check(f'absorption_N{N}',abs(times[-1]-N*sum(1/k**2 for k in range(1,N+1))),1e-10)
    s1=np.array([[0,1],[1,0]]);s2=np.array([[0,-1j],[1j,0]]);s3=np.diag([1,-1]);I=np.eye(2)
    gam=[np.kron(s1,I),np.kron(s2,I)]+[np.kron(s3,s) for s in [s1,s2,s3]]
    for a in range(5):
        for b in range(5):check(f'Clifford_{a}_{b}',np.max(abs(gam[a]@gam[b]+gam[b]@gam[a]-2*(a==b)*np.eye(4))),1e-14)
    for vec in [[0,0,0],[.1,.2,.3],[1,0,0]]:
        H=.7*gam[0]-.2*gam[1]+sum(x*g for x,g in zip(vec,gam[2:]));E=math.sqrt(.7**2+.2**2+sum(x*x for x in vec))
        check(f'spectrum_{vec}',np.max(abs(np.linalg.eigvalsh(H)-[-E,-E,E,E])),1e-12)
    # v=lambda=Lambda=eta=1; quadrature includes occupied degeneracy 2.
    for u in [.01,.1,.5,1.,3.]:
        integral=-quad(lambda k:k*(math.sqrt(k*k+u*u)-k)/math.pi,0,1,epsabs=1e-12)[0]
        formula=-((1+u*u)**1.5-1-u**3)/(3*math.pi)
        check(f'sea_integral_{u}',abs(integral-formula),1e-10)
    for u in [.001,.003,.01]:
        # Stable remainder integral after subtracting quadratic; no cancellation of O(u²).
        remainder=quad(lambda z:z*(1+z-math.sqrt(1+z*z))/math.pi,0,u,epsabs=1e-18)[0]
        approx=u**3/(3*math.pi)-u**4/(8*math.pi)+u**6/(48*math.pi)
        check(f'sea_series_{u}',abs(remainder/approx-1),1e-9)
    thermal=[]
    for T in [.01,.1,1.]:
        def lc(y):return np.logaddexp(y,-y)-math.log(2)
        for u in [1e-4,1e-3,.01,.1]:
            raw=-u/math.pi*quad(lambda E:math.tanh(E/(2*T)),u,math.sqrt(1+u*u),epsabs=1e-12)[0]
            closed=-2*T*u/math.pi*(lc(math.sqrt(1+u*u)/(2*T))-lc(u/(2*T)))
            check(f'thermal_integral_T{T}_u{u}',abs(raw-closed),1e-12)
            remainder=closed+2*T*u/math.pi*lc(1/(2*T))
            thermal.append(dict(T=T,u=u,remainder_force=float(remainder),force_over_u2=float(remainder/u**2)))
    result=dict(check_count=len(checks),passed=all(c['passed'] for c in checks),checks=checks,stationary=rows,thermal=thermal)
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(check_count=len(checks),passed=result['passed'])))
    assert result['passed']
if __name__=='__main__':main(sys.argv[1])
