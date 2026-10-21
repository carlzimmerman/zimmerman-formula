"""Charge-consistent finite-grid stationary Hessians and nearby gyro modes."""
from pathlib import Path
import json,math,sys,time,resource
import numpy as np
from scipy.sparse import bmat,eye,csr_matrix
from scipy.sparse.linalg import eigsh,eigs,LinearOperator,splu
from radial_tools import operators,P

profile_dir=Path(sys.argv[1]);out=Path(sys.argv[2]);rows=[];checks=[];start=time.monotonic()
def ck(n,x):checks.append({'name':n,'pass':bool(x)})
def lowest(H,lower,rank=None):
    n=H.shape[0];sigma=lower-1.;lu=splu(H-sigma*eye(n,format='csc'))
    if rank is None:op=H;inv=LinearOperator((n,n),matvec=lu.solve)
    else:
        w=lu.solve(rank);den=1+rank@w
        inv=LinearOperator((n,n),matvec=lambda v:lu.solve(v)-w*((w@v)/den))
        op=LinearOperator((n,n),matvec=lambda v:H@v+rank*(rank@v))
    va,ve=eigsh(op,k=5,sigma=sigma,which='LM',OPinv=inv,tol=1e-10,maxiter=5000)
    ix=np.argsort(va);va=va[ix];ve=ve[:,ix]
    return va,[float(np.linalg.norm(op@ve[:,i]-va[i]*ve[:,i])) for i in range(5)]

for Q in [80000,160000]:
    profile=profile_dir/f'Q{Q}.npz'
    for L,N in [(40.,399),(60.,599),(60.,1199)]:
        for ell in [0,1,2]:
            d=operators(profile,Q,L,N,ell);r=d['r'];W=d['W'];G=d['G'];om=d['record']['omega']
            f,b,h=d['fields'];Vu=1-om*om+6*P['lambda']*f*f+P['a']*h+2*P['g']*b
            Vv=1-om*om+2*P['lambda']*f*f+P['a']*h-2*P['g']*b;D=P['MX2']-4*om*om;B=P['M_chi']**2-.75*P['M_chi']*h+3*h*h
            pot=np.zeros((N,3,3));pot[:,0,0]=Vu;pot[:,1,1]=D;pot[:,2,2]=B
            pot[:,0,1]=pot[:,1,0]=2*P['g']*f;pot[:,0,2]=pot[:,2,0]=np.sqrt(2)*P['a']*f
            lo=float(np.linalg.eigvalsh(pot).min());lop=float(np.min(.5*(Vv+D-np.sqrt((Vv-D)**2+16*P['g']**2*f*f))))
            va,ra=lowest(d['amp'],lo);vp,rp=lowest(d['phase'],lop)
            rec={**d['record'],'ell':ell,'amplitude_lowest':va.tolist(),'phase_lowest':vp.tolist(),
                 'amplitude_eigen_residuals':ra,'phase_eigen_residuals':rp}
            if ell==0:
                vc,rc=lowest(d['amp'],lo,d['a'][:3*N]/np.linalg.norm(d['p']))
                rec['fixed_charge_amplitude_lowest']=vc.tolist();rec['fixed_charge_eigen_residuals']=rc
                ck(f'{Q} {L} {N} fixed-charge positive',vc[0]>1e-4)
                ck(f'{Q} {L} {N} phase zero restored',abs(vp[0])<1e-7 and d['record']['phase_zero_relative_residual']<1e-7)
                ck(f'{Q} {L} {N} one radial unconstrained negative',sum(va<0)==1)
            ck(f'{Q} {L} {N} l{ell} eigen residual',max(ra+rp)<1e-5)
            ck(f'{Q} {L} {N} l{ell} fixed charge background',abs(d['record']['Q']/Q-1)<1e-10)

            Z=csr_matrix(W.shape);I=eye(W.shape[0],format='csc')
            A=bmat([[Z,I],[-W,-G]],format='csc').astype(complex)
            modes=[]
            for target in [.035,.065,.12]:
                vals,vec=eigs(A,k=8,sigma=1j*target,which='LM',tol=1e-9,maxiter=3000,ncv=40)
                for j,lam in enumerate(vals):
                    v=vec[:,j];z=v[:5*N];res=float(np.linalg.norm(A@v-lam*v))
                    dens=np.sum(abs(z.reshape(5,N))**2,axis=0);norm=float(dens.sum())
                    local=float(dens[r<15].sum()/norm);tail=float(dens[r>.75*L].sum()/norm)
                    kenergy=float(np.real(abs(lam)**2*np.vdot(z,z)+np.vdot(z,W@z)))
                    qdelta=lam*np.dot(d['p'],z)+np.dot(d['a'],z)
                    qnorm=(abs(lam)*np.linalg.norm(d['p'])+np.linalg.norm(d['a']))*np.linalg.norm(z)
                    modes.append({'target':target,'lambda_real':float(lam.real),'Omega':float(lam.imag),
                                  'abs_lambda':float(abs(lam)),'residual':res,'norm_fraction_r_lt15':local,
                                  'norm_fraction_r_gt75pctL':tail,'quadratic_K_coefficient':kenergy,
                                  'linear_charge_relative':float(abs(qdelta)/qnorm) if qnorm and ell==0 else None})
            rec['gyro_modes']=modes;rec['Psi_positive_threshold']=1-om;rec['X_positive_threshold']=math.sqrt(P['MX2'])-2*om
            ck(f'{Q} {L} {N} l{ell} gyro residual',max(v['residual'] for v in modes)<1e-6)
            if ell==2:ck(f'{Q} {L} {N} l2 static positive',va[0]>0 and vp[0]>0)
            rows.append(rec)
            print(json.dumps({'Q':Q,'L':L,'N':N,'ell':ell,'amp0':va[0],'phase0':vp[0],
                              'fixed0':rec.get('fixed_charge_amplitude_lowest',[None])[0],
                              'mode_candidates':[{k:v[k] for k in ['lambda_real','Omega','norm_fraction_r_lt15']} for v in modes if v['Omega']>1e-3 and v['Omega']<1-om and v['norm_fraction_r_lt15']>.5]}),flush=True)

rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('measured RSS below1GB',rss<1_000_000_000)
result={'scope':'Variational finite-grid backgrounds and spectra; source/refinement/raw complex eigenvalues retained, no outgoing or nonlinear-stability theorem.',
        'parameters':P,'rows':rows,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(x['pass'] for x in checks),
        'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
        'important':'Tiny real symmetry splittings, especially l1 translation on a radial grid, require continuum/refinement interpretation. No nonzero eigenvalue is silently discarded.'}
out.write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
