"""Order-K static response to a K-normalized chiral mode at fixed total Q.

This constructs the zero-frequency perturbative correction, not a full
nonlinear trajectory or a nonlinear fundamental-frequency shift.
"""
from pathlib import Path
import json, sys, math, resource, time
import numpy as np
from numpy.polynomial.legendre import leggauss, legval
from scipy.sparse import bmat, csc_matrix
from scipy.sparse.linalg import spsolve
from radial_tools import operators, P

profiles, modes, out = map(Path, sys.argv[1:4])
rows=[]; checks=[]; start=time.monotonic()
def ck(name, value): checks.append({'name':name, 'pass':bool(value)})

def quadratic(z, f, h):
    u,s,x,v,t=z
    g,a,M,lam=P['g'],P['a'],P['M_chi'],P['lambda']
    F=np.sqrt(2)*f
    return np.array([
        lam*F*(3*u*u+v*v)+np.sqrt(2)*g*(s*u+t*v)+a*x*u,
        g/np.sqrt(2)*(u*u-v*v),
        .5*(-.75*M+6*h)*x*x+.5*a*(u*u+v*v),
        2*lam*F*u*v+np.sqrt(2)*g*(-s*v+t*u)+a*x*v,
        np.sqrt(2)*g*u*v])

# Independent numerical harmonic-product expansion, including its sign.
xs, weights=leggauss(24)
coeffs={0:1/math.sqrt(4*math.pi), 2:-math.sqrt(5)/(7*math.sqrt(math.pi)),
        4:1/(14*math.sqrt(math.pi))}
absY22sq=15/(32*math.pi)*(1-xs*xs)**2
expanded=np.zeros_like(xs)
for ell,C in coeffs.items():
    pol=np.zeros(ell+1); pol[-1]=1
    yl=math.sqrt((2*ell+1)/(4*math.pi))*legval(xs,pol)
    ck(f'angular product coefficient ell{ell}',
       abs(2*math.pi*np.sum(weights*yl*absY22sq)-C)<1e-13)
    expanded+=C*yl
ck('angular product pointwise identity',np.max(abs(expanded-absY22sq))<1e-14)

for Q in [80000,160000]:
  for L,N in [(40.,399),(60.,599),(60.,1199)]:
    name=f'Q{Q}_L{int(L)}_N{N}.npz'
    m=np.load(modes/name); z=m['mode']; Om=float(m['Omega']); om=float(m['omega'])
    op=operators(profiles/f'Q{Q}.npz',Q,L,N,0)
    r,dr=op['r'],op['dr']; f,b,h=op['fields']; aa=op['a'][:3*N]
    ck(f'{Q} {L} {N} matched background',abs(op['record']['omega']-om)<1e-12)
    local=z/r
    # Polynomial cross coefficient of |Y22|^2 in the time-independent source.
    cross=quadratic(local+local.conj(),f,h)-quadratic(local,f,h)-quadratic(local.conj(),f,h)
    ck(f'{Q} {L} {N} real DC force',np.max(abs(cross.imag))<1e-10)
    ck(f'{Q} {L} {N} no phase DC forcing',
       np.linalg.norm(cross[3:])/max(np.linalg.norm(cross[:3]),1e-300)<1e-9)
    cross=cross[:3].real

    u,s,x,v,t=z
    qraw=float(dr*np.sum(2*om*(abs(u)**2+abs(v)**2)
                        -4*Om*np.imag(u.conj()*v)
                        +8*om*(abs(s)**2+abs(t)**2)
                        -8*Om*np.imag(s.conj()*t)))
    cp=(u+1j*v)/np.sqrt(2); cm=(u-1j*v)/np.sqrt(2)
    xp=(s+1j*t)/np.sqrt(2); xm=(s-1j*t)/np.sqrt(2)
    qside=float(dr*np.sum(2*(om+Om)*abs(cp)**2+2*(om-Om)*abs(cm)**2
                         +4*(2*om+Om)*abs(xp)**2+4*(2*om-Om)*abs(xm)**2))
    ck(f'{Q} {L} {N} independent raw mode charge',abs(qraw-qside)<1e-10)

    dc={}; rhs0=(-coeffs[0]*r*cross).reshape(-1)
    inertia=float(4*math.pi*dr*np.dot(op['p'],op['p']))
    A=bmat([[op['amp'],csc_matrix((-math.sqrt(4*math.pi)*aa)[:,None])],
            [csc_matrix((math.sqrt(4*math.pi)*dr*aa)[None,:]),csc_matrix([[inertia]])]],format='csc')
    rhs=np.r_[rhs0,-qraw]; sol=spsolve(A,rhs)
    dc[0]=sol[:-1].reshape(3,N); dom=float(sol[-1])
    residual=float(np.linalg.norm(A@sol-rhs)/np.linalg.norm(rhs))
    linear=float(math.sqrt(4*math.pi)*dr*aa@sol[:-1]); freq=inertia*dom
    ck(f'{Q} {L} {N} bordered residual',residual<1e-9)
    ck(f'{Q} {L} {N} total charge cancellation',abs(qraw+linear+freq)<1e-8)
    ell_res={0:residual}
    for ell in [2,4]:
        oi=operators(profiles/f'Q{Q}.npz',Q,L,N,ell)
        rhsell=(-coeffs[ell]*r*cross).reshape(-1)
        vec=spsolve(oi['amp'],rhsell)
        dc[ell]=vec.reshape(3,N)
        ell_res[ell]=float(np.linalg.norm(oi['amp']@vec-rhsell)/np.linalg.norm(rhsell))
        ck(f'{Q} {L} {N} ell{ell} static residual',ell_res[ell]<1e-9)

    # Independent direct real-field angular integration of total Noether Q.
    # This is a truncated initial configuration, not an exact nonlinear mode.
    tx,tw=leggauss(12); ph=2*math.pi*np.arange(20)/20
    Y22=np.sqrt(15/(32*math.pi))*(1-tx[:,None]**2)*np.exp(-2j*ph[None,:])
    Y0={}
    for ell in [0,2,4]:
        pol=np.zeros(ell+1);pol[-1]=1
        Y0[ell]=np.sqrt((2*ell+1)/(4*math.pi))*legval(tx,pol)
    angular_weights=tw[:,None]*np.ones((1,len(ph)))*(2*math.pi/len(ph))
    qcheck=[]
    Dnorm=float(dr*sum(np.sum(d[0]**2+4*d[1]**2) for d in dc.values()))
    mode_rot=float(2*dr*np.sum(abs(u)**2+abs(v)**2+4*(abs(s)**2+abs(t)**2)))
    c2=om*Dnorm+dom*linear/om+dom*mode_rot
    c3=dom*Dnorm
    for K in [1.,.25,.0625]:
        qtotal=0.
        for j,rr in enumerate(r):
            zz=z[:,j,None,None]*Y22/rr
            fields=2*math.sqrt(K)*zz.real
            vel=2*math.sqrt(K)*(1j*Om*zz).real
            for ell,d in dc.items():
                fields[:3]+=K*d[:,j,None,None]/rr*Y0[ell][None,:,None]
            U=math.sqrt(2)*f[j]+fields[0]; V=fields[3]
            S=math.sqrt(2)*b[j]+fields[1]; T=fields[4]
            localq=U*vel[3]-V*vel[0]+(om+K*dom)*(U*U+V*V)
            localq+=2*(S*vel[4]-T*vel[1])+4*(om+K*dom)*(S*S+T*T)
            qtotal+=dr*rr*rr*float(np.sum(angular_weights*localq))
        delta=qtotal-op['record']['Q']
        predicted=K*(qraw+linear+freq)+K*K*c2+K**3*c3
        ck(f'{Q} {L} {N} direct angular charge K{K}',abs(delta-predicted)<1e-7)
        qcheck.append({'K':K,'direct_Q':qtotal,'delta_Q':delta,'predicted_truncated_delta_Q':predicted})

    # Per-unit-K static shift norms are diagnostics, not amplitude validity proofs.
    relative_dc={str(ell):float(np.sqrt(dr*np.sum(d*d))) for ell,d in dc.items()}
    np.savez_compressed(out/f'dc_{name}',r=r,delta_l0=dc[0],delta_l2=dc[2],delta_l4=dc[4],
                        delta_omega_per_K=dom,raw_mode_charge_per_K=qraw,
                        background_omega=om,Omega_parent=Om)
    row={'Q_target':Q,'L':L,'N':N,'dr':dr,'omega':om,'Omega':Om,
         'raw_mode_charge_per_K':qraw,'static_field_charge_per_K':linear,
         'frequency_charge_per_K':freq,'total_charge_correction_sum':qraw+linear+freq,
         'delta_omega_per_K':dom,'static_norms_per_K':relative_dc,
         'ell_relative_residuals':ell_res,'direct_charge_checks':qcheck}
    rows.append(row); print(json.dumps({k:row[k] for k in ['Q_target','L','N','raw_mode_charge_per_K','delta_omega_per_K','total_charge_correction_sum']}),flush=True)

for Q in [80000,160000]:
    a,b,c=[next(x for x in rows if x['Q_target']==Q and x['L']==L and x['N']==N)
           for L,N in [(40.,399),(60.,599),(60.,1199)]]
    ck(f'{Q} DC frequency coefficient box consistency',abs(a['delta_omega_per_K']/b['delta_omega_per_K']-1)<.02)
    ck(f'{Q} DC frequency coefficient mesh consistency',abs(b['delta_omega_per_K']/c['delta_omega_per_K']-1)<.02)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('measured peak RSS below1GB',rss<1_000_000_000)
result={'scope':'Finite order-K zero-frequency response at fixed total bound Noether charge; not a nonlinear evolution.',
        'conventions':'Canonical order(u,s,chi,v,t), reduced r fields; no-half chiral mode; K=A²; DC source cross=N2(z+z*)-N2(z)-N2(z*).',
        'angular_coefficients':coeffs,'rows':rows,'checks':checks,'n_checks':len(checks),
        'all_checks_pass':all(c['pass'] for c in checks),'peak_rss_bytes_macos':rss,
        'runtime_seconds':time.monotonic()-start,
        'non_claims':['No nonlinear fundamental frequency shift or full periodic solution',
                      'No fixed charge during subsequent outgoing radiation',
                      'No large-amplitude or long-time accuracy claim',
                      'No merger excitation fraction, capture kernel or galaxy transport closure']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
