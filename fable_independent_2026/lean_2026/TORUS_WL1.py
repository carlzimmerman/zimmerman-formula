# One-parameter continuous Wilson-line families (criteria TORUS_WL1_CRITERIA.md, commit bcbc4ea9a)
import numpy as np
from scipy.optimize import brentq
def theta(a,nu,T,L=12):
    l=np.arange(-L,L+1).reshape((-1,)+(1,)*np.ndim(nu))
    return np.exp(1j*np.pi*(a+l)**2*T+2j*np.pi*(a+l)*nu).sum(0)
def psi(j,M,tau,z): return np.exp(1j*np.pi*M*z*z.imag/tau.imag)*theta(j/M,M*z,M*tau)
N=64
G={}
def grid(tau):
    if tau not in G:
        x=(np.arange(N)+0.5)/N; X,Y=np.meshgrid(x,x,indexing='ij'); G[tau]=(X+tau*Y, tau.imag/N**2)
    return G[tau]
def modes(M,tau,zeta):
    z,dA=grid(tau); ps=[psi(j,M,tau,z+zeta) for j in range(M)]
    return np.array([p/np.sqrt((abs(p)**2).sum()*dA) for p in ps]),dA
def spectrum(tau,zL,zR,k):
    pL,dA=modes(3,tau,zL); pR,_=modes(3,tau,zR); pH,_=modes(6,tau,(zL+zR)/2)
    m=np.einsum('iab,jab->ij',pL,pR*np.conj(pH[k]))*dA
    return np.sort(np.linalg.svd(m,compute_uv=False))
R=206.768283
def Q_of(sv): s=np.sqrt(sv); return sv.sum()/s.sum()**2
fams={'F1':lambda x,t:(x,0),'F2':lambda x,t:(x,x),'F3':lambda x,t:(x,-x),'F4':lambda x,t:(x*t,0)}
taus={'i':1j,'omega':np.exp(2j*np.pi/3)}
sols=[]
for tn,tau in taus.items():
  for fn,f in fams.items():
    for k in range(6):
        xs=np.linspace(0,1,401)[:-1]
        def g(x):
            sv=spectrum(tau,*f(x,tau),k)
            if sv[0]<=1e-14*sv[2] or sv[1]/sv[0]<1+1e-9: return np.nan
            return np.log(sv[1]/sv[0]/R)
        v=np.array([g(x) for x in xs])
        for a,b,va,vb in zip(xs,xs[1:],v,v[1:]):
            if np.isfinite(va) and np.isfinite(vb) and va*vb<0:
                x=brentq(g,a,b,xtol=1e-13); sv=spectrum(tau,*f(x,tau),k)
                sols.append((tn,fn,k,x,Q_of(sv),sv[2]/sv[1]))
print(f"fitted solutions (m_mu/m_e = 206.768): {len(sols)}")
for s in sols: print("  tau=%-5s %s H=k%d x=%.6f  Q=%.6f  dQ=%+.2e  m_tau/m_mu=%.3f"%(s[0],s[1],s[2],s[3],s[4],s[4]-0.666661,s[5]))
if sols:
    Qs=np.array([s[4] for s in sols]); spread=max(Qs.max()-Qs.min(),1e-9)
    hits=[s for s in sols if abs(s[4]-0.666661)<3e-5]
    print(f"Q spread {Qs.min():.4f}..{Qs.max():.4f}; Koide-band hits {len(hits)}; chance expectation {len(sols)*6e-5/spread:.4f}")
    print("VERDICT:", "PASS" if hits and len(hits)>len(sols)*6e-5/spread else "KILL")
else: print("VERDICT: KILL (no family reaches m_mu/m_e)")
