"""Same-action DISCRETE references bracketing retained-charge diagnostics.

No pair evolution and no true-origin BVP claim. Seeds a variational radial
Newton solve from the pinned Q160k continuum profile, then normalizes ell2.
"""
from pathlib import Path
import json,math,resource,sys,time

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.sparse import diags,bmat,eye,csr_matrix
from scipy.sparse.linalg import eigsh,eigs,splu,LinearOperator

ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'sol61_push/cold_fragment_modes_2026_10_20'
sys.path.insert(0,str(OLD))
from radial_tools import operators,P

def v0(n):
    return np.cos(np.arange(n)*.731)+.3*np.sin(np.arange(n)*1.17)

def lowest(H,lower):
    sigma=lower-1.;n=H.shape[0]
    lu=splu(H-sigma*eye(n,format='csc'))
    values,vectors=eigsh(H,k=3,sigma=sigma,which='LM',OPinv=LinearOperator((n,n),matvec=lu.solve),
                         v0=v0(n),tol=1e-10,maxiter=3000)
    order=np.argsort(values);values=values[order];vectors=vectors[:,order]
    res=[float(np.linalg.norm(H@vectors[:,i]-values[i]*vectors[:,i])) for i in range(3)]
    return values,res

def main(seed,out):
    start=time.monotonic();rows=[];checks=[]
    def ck(name,value):checks.append({'name':name,'pass':bool(value)})
    for Q in [136000,140000]:
      for N in [599,1199]:
        L=60.;tag=f'Q{Q}_L60_N{N}'
        op=operators(seed,Q,L,N,2)
        r,dr,W,G=op['r'],op['dr'],op['W'],op['G'];f,b,h=op['fields'];rec=op['record'];om=rec['omega']
        Vu=1-om*om+6*P['lambda']*f*f+P['a']*h+2*P['g']*b
        Vv=1-om*om+2*P['lambda']*f*f+P['a']*h-2*P['g']*b
        D=P['MX2']-4*om*om;B=P['M_chi']**2-.75*P['M_chi']*h+3*h*h
        pot=np.zeros((N,3,3));pot[:,0,0]=Vu;pot[:,1,1]=D;pot[:,2,2]=B
        pot[:,0,1]=pot[:,1,0]=2*P['g']*f;pot[:,0,2]=pot[:,2,0]=np.sqrt(2)*P['a']*f
        lo=float(np.linalg.eigvalsh(pot).min())
        lop=float(np.min(.5*(Vv+D-np.sqrt((Vv-D)**2+16*P['g']**2*f*f))))
        ampvals,ampres=lowest(op['amp'],lo);phasevals,phaseres=lowest(op['phase'],lop)
        phase0=op['phase']-diags(np.tile(6/r**2,2))
        phasevector=op['p'][3*N:]
        phasezero=float(np.linalg.norm(phase0@phasevector)/np.linalg.norm(phasevector))
        A=bmat([[csr_matrix(W.shape),eye(5*N)],[-W,-G]],format='csc').astype(complex)
        vals,vec=eigs(A,k=8,sigma=0.,which='LM',v0=v0(A.shape[0]),tol=1e-11,maxiter=4000,ncv=32)
        order=np.argsort(abs(vals));vals=vals[order];vec=vec[:,order]
        candidates=[];raw=[]
        for j,ev in enumerate(vals):
            zz=vec[:5*N,j];norm=np.linalg.norm(zz)
            local=float(np.sum(abs(zz.reshape(5,N)[:,r<15])**2)/np.sum(abs(zz)**2))
            pencil=float(np.linalg.norm((W+ev*G+ev*ev*eye(5*N))@zz)/norm)
            entry={'lambda_real':float(ev.real),'Omega':float(ev.imag),'local_norm_fraction_r_lt15':local,'pencil_residual':pencil}
            raw.append(entry)
            if ev.imag>0 and abs(ev.real)<1e-7 and local>.9 and ev.imag<1-om:
                candidates.append(j)
        if not candidates:raise RuntimeError(tag+' has no resolved localized positive subthreshold candidate')
        pick=min(candidates,key=lambda j:vals[j].imag);ev=vals[pick];Om=float(ev.imag);Z=vec[:5*N,pick].copy()
        peak=int(np.argmax(abs(Z[:N])));Z*=np.exp(-1j*np.angle(Z[peak]))
        knorm=float(dr*np.real(Om*Om*np.vdot(Z,Z)+np.vdot(Z,W@Z)))
        ck(tag+' positive mode normalization',knorm>0)
        Z/=math.sqrt(knorm)
        K=float(dr*np.real(Om*Om*np.vdot(Z,Z)+np.vdot(Z,W@Z)))
        residual=float(np.linalg.norm((W-Om*Om*eye(5*N)+1j*Om*G)@Z)/np.linalg.norm(Z))
        zy=Z.reshape(5,N);u,s,x,v,t=zy
        cp=(u+1j*v)/np.sqrt(2);cm=(u-1j*v)/np.sqrt(2)
        xp=(s+1j*t)/np.sqrt(2);xm=(s-1j*t)/np.sqrt(2)
        J=float(dr*np.sum(4*((om+Om)*abs(cp)**2-(om-Om)*abs(cm)**2
                            +(2*om+Om)*abs(xp)**2-(2*om-Om)*abs(xm)**2+Om*abs(x)**2)))
        locality=float(np.sum(abs(zy[:,r<15])**2)/np.sum(abs(zy)**2))
        tail=float(np.sum(abs(zy[:,r>.75*L])**2)/np.sum(abs(zy)**2))
        first_positive=min((v.imag for v in vals if v.imag>1e-7),default=math.inf)
        ck(tag+' same-grid field residual',rec['field_residual_scaled']<1e-9)
        ck(tag+' same-grid Q',abs(rec['Q']/Q-1)<1e-11)
        ck(tag+' ell0 phase Noether identity',phasezero<1e-7)
        ck(tag+' ell2 amplitude and phase positive',ampvals[0]>0 and phasevals[0]>0)
        ck(tag+' symmetric eigen residuals',max(ampres+phaseres)<1e-6)
        ck(tag+' all nearest-zero pencil residuals',max(x['pencil_residual'] for x in raw)<1e-6)
        ck(tag+' selected lowest positive among nearest-zero candidates',abs(Om-first_positive)<1e-8)
        ck(tag+' unit canonical K',abs(K-1)<1e-8)
        ck(tag+' canonical mode pencil residual',residual<1e-7)
        ck(tag+' chiral normalization J=2K/Omega',abs(J/(2/Om)-1)<1e-7)
        ck(tag+' localized scalar-subthreshold mode',locality>.9 and 0<Om<1-om)
        record={**rec,'reference_kind':'same-action finite variational radial stationary solution',
                'Omega':Om,'K_normalization':K,'mode_pencil_residual':residual,
                'phase0_Noether_relative_residual':phasezero,
                'ell2_amplitude_lowest':ampvals.tolist(),'ell2_phase_lowest':phasevals.tolist(),
                'raw_nearest_zero_eigenvalues':raw,'mode_norm_fraction_r_lt15':locality,
                'mode_norm_fraction_r_gt45':tail,'J_if_chiral_m2':J,'J_if_axisymmetric_m0':0.,
                'Psi_positive_threshold':1-om,
                'mode_file':tag+'.npz','profile_file':'profile_'+tag+'.npz',
                'charge_interpretation':'Qtarget labels reference; exact discrete integrated charge is in Q. This does not identify the actual bound charge of a collision.'}
        np.savez_compressed(out/(tag+'.npz'),r=r,mode=zy,Zmode=zy,omega=om,Omega=Om,Q=Q,
                            Q_integrated_discrete=rec['Q'],E=rec['E'],K_normalization=K,
                            background_fields=np.array([f,b,h]),ell=2,metadata_json=json.dumps(record))
        # Compatible profile is interpolation of the DISCRETE solution, not a BVP.
        bg=np.array([f,b,h]);bg0=(4*bg[:,0]-bg[:,1])/3
        rp=np.r_[0.,r,L];fieldnodes=np.column_stack([bg0,bg,np.zeros(3)])
        spline=CubicSpline(rp,fieldnodes,axis=1,bc_type=((1,np.zeros(3)),(2,np.zeros(3))))
        derivative=spline(rp,1)
        qdis=8*math.pi*om*dr*r*r*(f*f+4*b*b)
        cumulative=np.r_[0.,np.cumsum(qdis)/rec['Q'],1.]
        yy=np.array([fieldnodes[0],derivative[0],fieldnodes[1],derivative[1],fieldnodes[2],derivative[2],cumulative])
        profmeta={'reference_kind':'INTERPOLATED DISCRETE stationary reference; NOT a true-origin BVP',
                  'origin':'quadratic even extrapolation (4f(dr)-f(2dr))/3; cubic profile has derivative0 at origin',
                  'outer':'Dirichlet fields0 atL; natural second derivative for interpolation only',
                  'Q_target':Q,'Q_integrated_discrete':rec['Q'],'E_discrete':rec['E'],
                  'q_row':'normalized discrete cumulative charge diagnostic, not a BVP integrated variable',
                  'radial_grid':{'L':L,'N':N,'dr':dr}}
        np.savez_compressed(out/('profile_'+tag+'.npz'),r=rp,y=yy,omega=om,Q=Q,E=rec['E'],
                            Q_integrated_discrete=rec['Q'],metadata_json=json.dumps(profmeta))
        ck(tag+' compatible interpolated origin derivatives',np.max(abs(yy[[1,3,5],0]))<1e-12)
        ck(tag+' compatible interpolated cumulative charge',abs(yy[6,-1]-1)<1e-12)
        rows.append(record)
        print(json.dumps({k:record[k] for k in ['Q_target','N','omega','Omega','E','Q','mode_pencil_residual','mode_norm_fraction_r_lt15']}),flush=True)
    for Q in [136000,140000]:
        coarse,fine=[r for r in rows if r['Q_target']==Q]
        ck(str(Q)+' mode frequency mesh consistency',abs(coarse['Omega']/fine['Omega']-1)<.01)
        ck(str(Q)+' stationary energy mesh consistency',abs(coarse['E']/fine['E']-1)<1e-4)
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    ck('measured RSS below1GB',rss<1_000_000_000)
    result={'scope':'Q136k/Q140k same-action DISCRETE reference sensitivity bracket; no pair evolution or true-origin BVP.',
            'parameters':P,'rows':rows,'checks':checks,'n_checks':len(checks),
            'all_checks_pass':all(c['pass'] for c in checks),'peak_rss_bytes_macos':rss,
            'runtime_seconds':time.monotonic()-start,
            'non_claims':['Aperture stock does not prove a unique bound remnant Q',
                          'Lowest mode is a resolved finite nearest-zero candidate, not an interval continuum theorem',
                          'Interpolated profiles are not fresh continuum BVP solutions',
                          'Q160k radiation coefficient is not recomputed/transferred to these backgrounds',
                          'No actual collision excitation, orbital transport or dwarf closure']}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    raise SystemExit(0 if result['all_checks_pass'] else 1)

if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
