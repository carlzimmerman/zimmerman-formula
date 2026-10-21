"""Finite radial Hessians and the fixed-Q quadratic-energy correction."""
from pathlib import Path
import json,sys,math,time,resource
import numpy as np
from scipy.sparse import diags,bmat,eye,csr_matrix
from scipy.sparse.linalg import eigsh,eigs,splu,LinearOperator
from profile_source_v2 import regenerate,P,PRIOR

outdir=Path(sys.argv[1]);checks=[];rows=[];start=time.monotonic()
def ck(n,v):checks.append({'name':n,'pass':bool(v)})

def blocks(sol,rec,L,N,ell):
    dr=L/(N+1);r=dr*np.arange(1,N+1)
    f,fp,b,bp,h,hp,q=sol.sol(r);om=rec['omega']
    H=diags([-np.ones(N-1),2*np.ones(N),-np.ones(N-1)],[-1,0,1],format='csc')/(dr*dr)
    H+=diags(ell*(ell+1)/r**2,format='csc')
    D=P['MX2']-4*om*om;B=P['M_chi']**2-.75*P['M_chi']*h+3*h*h
    Vu=1-om*om+6*P['lambda']*f*f+P['a']*h+2*P['g']*b
    Vv=1-om*om+2*P['lambda']*f*f+P['a']*h-2*P['g']*b
    C=diags(2*P['g']*f);A=diags(np.sqrt(2)*P['a']*f)
    Z=csr_matrix((N,N))
    amp=bmat([[H+diags(Vu),C,A],[C,H+D*eye(N),Z],[A,Z,H+diags(B)]],format='csc')
    phase=bmat([[H+diags(Vv),C],[C,H+D*eye(N)]],format='csc')
    pot=np.zeros((N,3,3));pot[:,0,0]=Vu;pot[:,1,1]=D;pot[:,2,2]=B
    pot[:,0,1]=pot[:,1,0]=2*P['g']*f;pot[:,0,2]=pot[:,2,0]=np.sqrt(2)*P['a']*f
    bound=float(np.linalg.eigvalsh(pot).min())
    aa=np.concatenate([2*np.sqrt(2)*om*r*f,8*np.sqrt(2)*om*r*b,np.zeros(N)])
    pp=np.concatenate([np.sqrt(2)*r*f,2*np.sqrt(2)*r*b])
    trans=np.concatenate([np.sqrt(2)*r*fp,np.sqrt(2)*r*bp,r*hp])
    return r,dr,amp,phase,aa,pp,trans,bound,(f,b,h,Vu,Vv,B,D)

def low(H,lower,k=5,rank=None):
    n=H.shape[0];sigma=lower-1.
    lu=splu(H-sigma*eye(n,format='csc'))
    if rank is None:
        op=H;inv=LinearOperator((n,n),matvec=lu.solve)
    else:
        u=rank;w=lu.solve(u);den=1+np.dot(u,w)
        inv=LinearOperator((n,n),matvec=lambda v:lu.solve(v)-w*(np.dot(w,v)/den))
        op=LinearOperator((n,n),matvec=lambda v:H@v+u*np.dot(u,v))
    vals,vec=eigsh(op,k=k,sigma=sigma,which='LM',OPinv=inv,tol=1e-10,maxiter=5000)
    order=np.argsort(vals);vals=vals[order];vec=vec[:,order]
    residual=[float(np.linalg.norm(op@vec[:,i]-vals[i]*vec[:,i])) for i in range(k)]
    return vals,vec,residual

profiles=[]
for Q in [80000,160000]:
    sol,rec=regenerate(Q)
    ck(str(Q)+' regenerated energy',abs(rec['E']/next(v['E'] for v in json.loads((PRIOR/'run_001/results.json').read_text())['rows'] if v['Q']==Q and v['L']==60)-1)<1e-7)
    profiles.append({'Q':Q,'record':rec})
    rr=np.linspace(1e-4,60.,12001)
    np.savez_compressed(outdir/f'profile_Q{Q}.npz',r=rr,y=sol.sol(rr),omega=rec['omega'],Q=Q)
    for L,N in [(40.,399),(60.,599),(60.,1199)]:
        for ell in [0,1,2]:
            r,dr,amp,phase,aa,pp,tr,bound,parts=blocks(sol,rec,L,N,ell)
            va,za,ra=low(amp,bound)
            ff,bb,hh,Vu,Vv,B,D=parts
            phasebound=float(np.min(.5*(Vv+D-np.sqrt((Vv-D)**2+16*P['g']**2*ff**2))))
            vp,zp,rp=low(phase,phasebound)
            entry={'Q':Q,'L':L,'N':N,'dr':dr,'ell':ell,'amplitude_lowest_eigenvalues':va.tolist(),
                   'phase_lowest_eigenvalues':vp.tolist(),'amplitude_pointwise_lower_bound':bound,
                   'phase_pointwise_lower_bound':phasebound,'amplitude_eigen_residuals':ra,'phase_eigen_residuals':rp,
                   'phase_U1_relative_residual':float(np.linalg.norm(phase@pp)/np.linalg.norm(pp)),
                   'translation_relative_residual':float(np.linalg.norm(amp@tr)/np.linalg.norm(tr)),
                   'profile_monotone_signs':{'f_positive':bool(np.all(parts[0]>-1e-8)),
                                            'X_negative':bool(np.all(parts[1]<1e-8))}}
            if ell==0:
                vc,zc,rc=low(amp,bound,rank=aa/np.linalg.norm(pp))
                entry.update(fixed_charge_amplitude_lowest_eigenvalues=vc.tolist(),fixed_charge_eigen_residuals=rc)
                ck(f'{Q} L{L} N{N} fixedQ positive',vc[0]>0)
                ck(f'{Q} L{L} N{N} one negative radial amplitude among lowest5',sum(va<0)==1)
            ck(f'{Q} L{L} N{N} l{ell} resolved lowest eigenpairs',max(ra+rp)<1e-5)
            rows.append(entry)
            print(json.dumps({k:entry[k] for k in ['Q','L','N','ell','amplitude_lowest_eigenvalues','phase_lowest_eigenvalues']}) ,flush=True)

# Convergence controls target actual symmetry zero modes, not a guessed sign.
for Q in [80000,160000]:
    for kind,ell,key in [('phase',0,'phase_lowest_eigenvalues'),('translation',1,'amplitude_lowest_eigenvalues')]:
        coarse=next(t for t in rows if t['Q']==Q and t['L']==60 and t['N']==599 and t['ell']==ell)
        fine=next(t for t in rows if t['Q']==Q and t['N']==1199 and t['ell']==ell)
        ratio=abs(fine[key][0]/coarse[key][0])
        ck(f'{Q} {kind} zero-mode convergence',ratio<.4)
        ck(f'{Q} {kind} finest zero residual',abs(fine[key][0])<.01)
    # A cutoff continuum has positive levels too; this is only a finite matrix energy test.
    fine=next(t for t in rows if t['Q']==Q and t['N']==1199 and t['ell']==0)
    ck(f'{Q} fixedQ amplitude gap resolved',fine['fixed_charge_amplitude_lowest_eigenvalues'][0]>1e-4)

rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('measured RSS below1GB',rss<1_000_000_000)
result={'scope':'Finite second-order radial Dirichlet Hessians and fixed-charge energy correction; not outgoing spectrum or interval/continuum/nonlinear stability proof.',
        'parameters':P,'profiles':profiles,'rows':rows,'checks':checks,'n_checks':len(checks),
        'all_checks_pass':all(v['pass'] for v in checks),'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
        'normalization':'Canonical amplitudes sqrt2u,sqrt2v,sqrt2s,sqrt2t,xi transformed w=r z. Amp=(u,s,xi), phase=(v,t). FixedQ correction a aT/||p||², a=−Gp. All angular sectors use l(l+1)/r².'}
(outdir/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
