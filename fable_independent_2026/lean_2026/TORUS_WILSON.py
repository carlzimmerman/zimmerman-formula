# Torus + discrete Wilson lines (criteria TORUS_WILSON_CRITERIA.md, commit 8ea12cecf)
import numpy as np, itertools
def theta(a,nu,T,L=12):
    l=np.arange(-L,L+1).reshape((-1,)+(1,)*np.ndim(nu))
    return np.exp(1j*np.pi*(a+l)**2*T+2j*np.pi*(a+l)*nu).sum(0)
def psi(j,M,tau,z):
    return np.exp(1j*np.pi*M*z*z.imag/tau.imag)*theta(j/M,M*z,M*tau)
N=72
def grid(tau):
    x=(np.arange(N)+0.5)/N; X,Y=np.meshgrid(x,x,indexing='ij'); return X+tau*Y, tau.imag/N**2
def modes(M,tau,zeta):
    z,dA=grid(tau); ps=[psi(j,M,tau,z+zeta) for j in range(M)]
    return [p/np.sqrt((abs(p)**2).sum()*dA) for p in ps],dA
def gate(tau,zL,zR):
    zH=(zL+zR)/2; pts=np.array([0.13+0.27j,0.41+0.08j,0.77+0.5j]); worst=0
    for w in pts:
        f=lambda z: psi(1,3,tau,z+zL)*psi(2,3,tau,z+zR)*np.conj(psi(3,6,tau,z+zH))
        for s in (1,tau): worst=max(worst,abs(f(w+s)-f(w))/abs(f(w)))
    return worst
def Q_of(m): s=np.sqrt(m); return m.sum()/s.sum()**2
taus={'i':1j,'omega':np.exp(2j*np.pi/3)}
Z3=lambda tau:[(p+q*tau)/3 for p in range(3) for q in range(3)]
g=max(gate(t,a,b) for t in taus.values() for a in Z3(t) for b in Z3(t))
print(f"single-valuedness gate (worst relative jump over all L,R Wilson lines): {g:.1e}")
rows=[]
for tn,tau in taus.items():
    for (iL,zL),(iR,zR) in itertools.product(enumerate(Z3(tau)),repeat=2):
        pL,dA=modes(3,tau,zL); pR,_=modes(3,tau,zR); pH,_=modes(6,tau,(zL+zR)/2)
        Y=np.array([[[ (pL[i]*pR[j]*np.conj(pH[k])).sum()*dA for k in range(6)] for j in range(3)] for i in range(3)])
        for hn in ['k0','k1','k2','k3','k4','k5','uniform']:
            h=np.ones(6) if hn=='uniform' else np.eye(6)[int(hn[1])]
            sv=np.sort(np.linalg.svd(np.einsum('ijk,k->ij',Y,h),compute_uv=False))
            nondeg= sv[0]>1e-10*sv[2] and sv[1]/sv[0]>1+1e-6 and sv[2]/sv[1]>1+1e-6
            rows.append((tn,iL,iR,hn,sv,nondeg,Q_of(sv) if sv[0]>0 else np.nan))
nd=[r for r in rows if r[5]]
specs={}
for r in rows: specs.setdefault((r[0],r[3],tuple(np.round(r[4]/r[4][2],8))),0); specs[(r[0],r[3],tuple(np.round(r[4]/r[4][2],8)))]+=1
print("distinct normalised spectra per (tau, Higgs):")
for (tn,hn,sp),c in sorted(specs.items()): print(f"  tau={tn:5s} H={hn:7s} spectrum {sp}  (x{c} of 81 Wilson-line pairs)")
if not nd:
    print("NO non-degenerate spectrum in 1134 configurations -> KILL (Koide band unreachable)"); raise SystemExit
Qs=np.array([r[6] for r in nd])
print(f"configurations {len(rows)}, non-degenerate {len(nd)}, Q range {np.nanmin(Qs):.4f}..{np.nanmax(Qs):.4f}")
band=[r for r in nd if abs(r[6]-0.666661)<3e-5]
dens=np.sum(abs(Qs-2/3)<0.01)/0.02; exp_hits=dens*6e-5
print(f"Koide-band hits {len(band)}; chance expectation {exp_hits:.3f} (empirical density {dens:.1f}/unit Q near 2/3)")
for r in band: print("  HIT",r[:4],"m2/m1=%.3g m3/m2=%.3g Q=%.6f"%(r[4][1]/r[4][0],r[4][2]/r[4][1],r[6]))
def hier(r): return abs(np.log(r[4][1]/r[4][0]/206.77))+abs(np.log(r[4][2]/r[4][1]/16.82))
best=sorted(nd,key=hier)[:5]
print("best hierarchy matches (non-degenerate):")
for r in best: print("  ",r[:4],"m2/m1=%.3g m3/m2=%.3g Q=%.5f"%(r[4][1]/r[4][0],r[4][2]/r[4][1],r[6]))
near=sorted(nd,key=lambda r:abs(r[6]-2/3))[:5]
print("closest Q to 2/3:")
for r in near: print("  ",r[:4],"m2/m1=%.3g m3/m2=%.3g Q=%.6f"%(r[4][1]/r[4][0],r[4][2]/r[4][1],r[6]))
