"""Normalize a localized chiral quadrupole and derive its natural 2Omega source.

No imposed drive is used here. This is a weak-amplitude matter-sector
expansion about each finite-grid stationary fragment, not a merger spectrum.
"""
from pathlib import Path
import sys,json,math,resource,time
import numpy as np
from scipy.sparse import bmat,eye,csr_matrix
from scipy.sparse.linalg import eigs
from radial_tools import operators,P

profiles=Path(sys.argv[1]);out=Path(sys.argv[2]);rows=[];checks=[];start=time.monotonic()
def ck(n,v):checks.append({'name':n,'pass':bool(v)})
C=math.sqrt(5/(14*math.pi))
for Q,target in [(80000,.07547),(160000,.05599)]:
    for L,N in [(40.,399),(60.,599),(60.,1199)]:
        d=operators(profiles/f'Q{Q}.npz',Q,L,N,2);r=d['r'];dr=d['dr'];W=d['W'];G=d['G'];f,b,h=d['fields']
        A=bmat([[csr_matrix(W.shape),eye(5*N)],[-W,-G]],format='csc').astype(complex)
        va,ve=eigs(A,k=4,sigma=1j*target,which='LM',tol=1e-11,maxiter=3000,ncv=24)
        j=int(np.argmin(abs(va-1j*target)));lam=va[j];Omega=float(lam.imag);z=ve[:5*N,j]
        # Fix the otherwise arbitrary eigenvector phase before constructing z*z.
        peak=int(np.argmax(abs(z[:N])));z*=np.exp(-1j*np.angle(z[peak]))
        K=float(dr*np.real(Omega*Omega*np.vdot(z,z)+np.vdot(z,W@z)))
        ck(f'{Q} {L} {N} positive mode K',K>0)
        z/=math.sqrt(K)
        res=float(np.linalg.norm((W-Omega*Omega*eye(5*N)+1j*Omega*G)@z)/np.linalg.norm(z))
        # Order u,s,xi,v,t. Local canonical fields = reduced radial fields/r.
        u,s,xi,v,t=z.reshape(5,N)/r
        F=np.sqrt(2)*f;g,a,M,ellam=P['g'],P['a'],P['M_chi'],P['lambda']
        Nu=ellam*F*(3*u*u+v*v)+np.sqrt(2)*g*(s*u+t*v)+a*xi*u
        Nv=2*ellam*F*u*v+np.sqrt(2)*g*(-s*v+t*u)+a*xi*v
        Ns=g/np.sqrt(2)*(u*u-v*v)
        Nt=np.sqrt(2)*g*u*v
        Nx=.5*(-.75*M+6*h)*xi*xi+.5*a*(u*u+v*v)
        source=-C*r*np.array([Nu,Ns,Nx,Nv,Nt])
        # Independently calculate physical intrinsic J using circular sidebands.
        yy=z.reshape(5,N);cp=(yy[0]+1j*yy[3])/np.sqrt(2);cm=(yy[0]-1j*yy[3])/np.sqrt(2)
        xp=(yy[1]+1j*yy[4])/np.sqrt(2);xm=(yy[1]-1j*yy[4])/np.sqrt(2)
        om=d['record']['omega'];m=2
        J=dr*np.sum(2*m*((om+Omega)*abs(cp)**2-(om-Omega)*abs(cm)**2
                    +(2*om+Omega)*abs(xp)**2-(2*om-Omega)*abs(xm)**2+Omega*abs(yy[2])**2))
        knorm=float(dr*np.real(Omega*Omega*np.vdot(z,z)+np.vdot(z,W@z)))
        local=float(np.sum(abs(yy[:,r<15])**2)/np.sum(abs(yy)**2))
        ck(f'{Q} {L} {N} mode residual',res<1e-7)
        ck(f'{Q} {L} {N} unit mode energy',abs(knorm-1)<1e-8)
        ck(f'{Q} {L} {N} intrinsic J/K normalization',abs(float(J)/(m/Omega)-1)<1e-7)
        ck(f'{Q} {L} {N} linearly trapped scalar mode',0<Omega<1-om)
        ck(f'{Q} {L} {N} onlyPsi plus at2Omega',1-om<2*Omega<math.sqrt(P['MX2'])-2*om)
        ck(f'{Q} {L} {N} localized mode',local>.9)
        ck(f'{Q} {L} {N} nonzero quadratic source',np.linalg.norm(source)>0)
        name=f'Q{Q}_L{int(L)}_N{N}.npz'
        np.savez_compressed(out/name,r=r,mode=z.reshape(5,N),source=source,omega=om,Omega=Omega,Q=Q,L=L,N=N,
                            ell_parent=2,m_parent=2,ell_source=4,m_source=4,gaunt=C,K_normalization=knorm,
                            background_fields=np.array([f,b,h]))
        row={**d['record'],'Omega':Omega,'eigenvalue_real':float(lam.real),'mode_residual':res,
             'K_normalization':knorm,'intrinsic_J_normalization':float(J),'expected_J':m/Omega,
             'mode_norm_fraction_r_lt15':local,'harmonic_frequency':2*Omega,
             'Psi_positive_threshold':1-om,'X_positive_threshold':math.sqrt(P['MX2'])-2*om,
             'quadratic_source_norm_squared':float(dr*np.sum(abs(source)**2)),
             'mode_file':name,'gaunt_Y22_squared_to_Y44':C}
        rows.append(row);print(json.dumps({k:row[k] for k in ['Q','L','N','Omega','K_normalization','intrinsic_J_normalization','quadratic_source_norm_squared']}),flush=True)

rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('measured RSS below1GB',rss<1_000_000_000)
result={'scope':'Unit-K chiral quadrupole modes and natural scalar second-harmonic sources; actual outgoing response is separate.',
        'conventions':'Canonical real field=A[Z Y22 e^(+iOmega t)+c.c.], dphiY=-imY; Kmode=A², Jmode=+2/Omega*Kmode. Natural 2Omega forcing coefficient is for A², ell4,m4. Mode sources are not arbitrary external drives.',
        'rows':rows,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(x['pass'] for x in checks),
        'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
        'limits':['No mode excitation amplitude or merger probability derived','No full nonlinear decay trajectory','Metric/GW radiation not included','Exported intrinsic J is not already galaxy orbital J']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
