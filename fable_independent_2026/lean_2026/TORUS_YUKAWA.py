# Magnetized-torus Yukawa door (criteria: TORUS_YUKAWA_CRITERIA.md, commit c650a9ddb)
import numpy as np
def theta(a,nu,T,L=12):
    l=np.arange(-L,L+1)[:,None,None]
    return np.exp(1j*np.pi*(a+l)**2*T+2j*np.pi*(a+l)*nu).sum(0)
def modes(M,tau,N):
    x=(np.arange(N)+0.5)/N; X,Y=np.meshgrid(x,x,indexing='ij'); z=X+tau*Y
    pre=np.exp(1j*np.pi*M*z*z.imag/tau.imag)
    ps=[pre*theta(j/M,M*z,M*tau) for j in range(M)]
    dA=tau.imag/N**2
    ps=[p/np.sqrt((abs(p)**2).sum()*dA) for p in ps]
    return ps,dA,z
def gates(M,tau,N=96):
    ps,dA,z=modes(M,tau,N)
    G=np.array([[ (np.conj(a)*b).sum()*dA for b in ps] for a in ps])
    orth=abs(G-np.eye(M)).max()
    # periodicity of |psi|: evaluate directly at shifted points
    zs=np.array([0.13+0.27j,0.41+0.08j]); 
    def ev(j,z): return np.exp(1j*np.pi*M*z*z.imag/tau.imag)*theta(j/M,M*np.array([[z]]),M*tau)[0,0]
    per=max(abs(abs(ev(j,w+1))-abs(ev(j,w))) + abs(abs(ev(j,w+tau))-abs(ev(j,w))) for j in range(M) for w in zs)/max(abs(ev(0,w)) for w in zs)
    return orth,per
def yuk(tau,N=96):
    p3,dA,_=modes(3,tau,N); p6,_,_=modes(6,tau,N)
    return np.array([[[ (p3[i]*p3[j]*np.conj(p6[k])).sum()*dA for k in range(6)] for j in range(3)] for i in range(3)])
def Q_of(m):
    s=np.sqrt(m); return m.sum()/s.sum()**2
taus={'i':1j,'omega':np.exp(2j*np.pi/3)}
for tn,tau in taus.items():
    for M in (3,6):
        o,p=gates(M,tau); print(f"gate tau={tn} M={M}: orthonormality err {o:.1e}, periodicity err {p:.1e}")
print()
for tn,tau in taus.items():
    Y=yuk(tau)
    for hn in ['k0','k1','k2','k3','k4','k5','uniform']:
        h=np.ones(6) if hn=='uniform' else np.eye(6)[int(hn[1])]
        m=np.einsum('ijk,k->ij',Y,h); sv=np.sort(np.linalg.svd(m,compute_uv=False))
        if sv[0]<1e-12*sv[-1]: print(f"tau={tn:5s} H={hn:7s}: masses {sv/sv[-1]} (massless state)"); continue
        Q=Q_of(sv); print(f"tau={tn:5s} H={hn:7s}: m/m_max={np.round(sv/sv[-1],5)}  Q={Q:.6f}  dQ={Q-0.666661:+.2e}  m2/m1={sv[1]/sv[0]:.3g} m3/m2={sv[2]/sv[1]:.3g}")
print("\nleptons: m_mu/m_e=206.77, m_tau/m_mu=16.82")
# secondary: tau = i t scan
print("\nsecondary scan tau = i t:")
for hn in ['k0','k1','k2','k3','uniform']:
    h=np.ones(6) if hn=='uniform' else np.eye(6)[int(hn[1])]
    prev=None; cross=[]
    for t in np.linspace(0.5,5,46):
        sv=np.sort(np.linalg.svd(np.einsum('ijk,k->ij',yuk(1j*t,64),h),compute_uv=False))
        Q=Q_of(sv) if sv[0]>1e-12*sv[-1] else np.nan
        if prev is not None and np.isfinite(Q) and np.isfinite(prev[1]) and (Q-2/3)*(prev[1]-2/3)<0: cross.append((prev[0],t))
        prev=(t,Q)
    print(f"  H={hn}: Q at t=0.5..5 ends {prev[1]:.4f}; crossings of 2/3 in t-intervals {cross}")
