"""CCT-008 finite bound-spectrum reconstruction; see CONTRACT.md."""
import argparse, hashlib, json, pathlib, resource, time
import numpy as np
import scipy
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import nnls
from scipy.integrate import quad
P=pathlib.Path(__file__).resolve().parent
ROOT=P.parents[1]
INPUT=ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json'
G=.00430091
A={'Draco':193.22,'Sextans':485.89,'Fornax':695.33,'Leo I':229.1}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(m,args):
    M,b,Ms=m['cold_mass'],m['cold_scale_pc'],m['stellar_mass']
    q=Ms/M; a=A[m['name']]/b; eps=args.eta/np.sqrt(G*M*b)
    n=args.nr; xmax=20.; h=xmax/(n+1); x=np.arange(1,n+1)*h
    pot=-1/np.sqrt(1+x*x)-q/np.sqrt(x*x+a*a)
    diag=eps*eps/(h*h)+pot
    off=np.full(n-1,-eps*eps/(2*h*h))
    apert=np.geomspace(.08,12,60)
    # Sum cell shell masses with linear subcell interpolation, consistent target grid.
    def cum(v): return np.interp(apert,x,np.cumsum(v,axis=0),left=0)
    target=x**3/(1+x*x)**1.5
    target_ap=apert**3/(1+apert*apert)**1.5
    # Cumulative grid uses cell-centered integration corrected below by h/2 shift.
    edges=np.r_[0,x+h/2]
    def cdf(v):
        c=np.vstack([np.zeros((1,v.shape[1])),np.cumsum(v,axis=0)])
        return np.array([np.interp(apert,edges,c[:,j]) for j in range(v.shape[1])]).T
    cols=[]; ids=[]; energies=[]; worst_res=0
    for l in range(args.lmax+1):
        d=diag+eps*eps*l*(l+1)/(2*x*x)
        ev,u=eigh_tridiagonal(d,off,select='i',select_range=(0,args.nrad-1))
        for j,e in enumerate(ev):
            if e>=0: continue
            v=u[:,j]
            Hv=d*v; Hv[:-1]+=off*v[1:]; Hv[1:]+=off*v[:-1]
            worst_res=max(worst_res,float(np.linalg.norm(Hv-e*v)))
            cols.append(v*v); ids.append((l,j)); energies.append(float(e))
    S=np.array(cols).T
    C=cdf(S)
    # Total normalized target at outer domain plus relative aperture fitting.
    AA=np.vstack([C/target_ap[:,None],np.ones((1,S.shape[1]))*3])
    yy=np.r_[np.ones(len(apert)),3*target[-1]]
    occ,res=nnls(AA,yy,maxiter=100000)
    fitted=C@occ
    shell=S@occ
    # Shell potential in G M / b units, exact thin-shell Green function.
    pfit=-np.cumsum(shell)/x-(np.cumsum((shell/x)[::-1])[::-1]-shell/x)
    maxp=float(np.max(np.abs(pfit+1/np.sqrt(1+x*x))/(1/np.sqrt(1+x*x))))
    err=float(np.max(abs(fitted/target_ap-1)))
    # Dimensionless T/M in G M/b units. Plummer amplitude-gradient lower bound.
    tq=quad(lambda r: eps*eps/8*3*r*r/(1+r*r)**2.5*(5*r/(1+r*r))**2,0,np.inf)[0]
    virself=3*np.pi/32
    virb=quad(lambda r:3*r*r/(1+r*r)**2.5*q*r*r/(r*r+a*a)**1.5,0,np.inf)[0]
    tneed=(virself+virb)/2
    # Isotropic Jeans rms angular index: <j²>/eta²= (2/5) <r³ g>/eta².
    j2=quad(lambda r:3*r*r/(1+r*r)**2.5*r**3*(r/(1+r*r)**1.5+q*r/(r*r+a*a)**1.5),0,np.inf)[0]*.4/(eps*eps)
    l_eff=(np.sqrt(1+4*j2)-1)/2
    states=[{'l':int(l),'radial_index':int(j),'mass_fraction':float(w),'energy_GM_over_b':e} for (l,j),w,e in zip(ids,occ,energies) if w>1e-7]
    angular=np.array([l*(l+1) for l,j in ids])
    out={'name':m['name'],'cold_mass':M,'cold_scale_pc':b,'eta_code':eps,'states_count':len(ids),'occupied_states':states,'max_eigenpair_residual':worst_res,'fit_max_aperture_relative_error':err,'potential_max_relative_error':maxp,'fit_total_fraction':float(sum(occ)),'target_domain_fraction':float(target[-1]),'quantum_T_min_GM_over_b':tq,'virial_T_required_GM_over_b':tneed,'quantum_floor_over_required':tq/tneed,'isotropic_Jeans_l_effective':l_eff,'fit_mean_l_lplus1':float(occ@angular/max(sum(occ),1e-30)),'fit_mass_l_gt4':float(sum(w for (l,j),w in zip(ids,occ) if l>4)),'finite_adequacy':err<.05 and maxp<.05,'apertures_pc':(apert*b).tolist(),'target_enclosed_mass':(target_ap*M).tolist(),'fitted_enclosed_mass':(fitted*M).tolist()}
    np.savez_compressed(P/f'{args.tag}_{m["name"].replace(" ","")}.npz',x=x,shell_mass_fraction=shell,occupation=occ,mode_ids=ids,energy=energies,target_potential=pot,fitted_cold_potential=pfit)
    print(m['name'],{k:out[k] for k in ['states_count','fit_max_aperture_relative_error','potential_max_relative_error','quantum_floor_over_required','isotropic_Jeans_l_effective','fit_mass_l_gt4']},flush=True)
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--nr',type=int,default=1536);p.add_argument('--lmax',type=int,default=32);p.add_argument('--nrad',type=int,default=20);p.add_argument('--eta',type=float,default=3000);p.add_argument('--tag',default='baseline');args=p.parse_args()
    files=[pathlib.Path(__file__),INPUT,P/'CONTRACT.md']; before={str(f.relative_to(ROOT)):sha(f) for f in files}
    start=time.time(); models=json.loads(INPUT.read_text())['models']; results=[run(m,args) for m in models]
    after={str(f.relative_to(ROOT)):sha(f) for f in files}; assert before==after
    out={'scope':'conditional density-matrix stationary spectral reconstruction; no formation or pure coherent-field closure','parameters':vars(args),'inputs_before':before,'inputs_after':after,'runtime_s':time.time()-start,'maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'software':{'numpy':np.__version__,'scipy':scipy.__version__},'results':results}
    (P/f'{args.tag}.json').write_text(json.dumps(out,indent=2)+'\n')
