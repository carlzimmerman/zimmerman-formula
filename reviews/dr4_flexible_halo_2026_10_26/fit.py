"""Bounded positive-density halo mimicry experiment, not an observational forecast."""
import sys,json,hashlib,pathlib
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import least_squares
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
ROOT=pathlib.Path(__file__).resolve().parents[2]
SRC=ROOT/'rebuild_2026_10_22/S3_v3_mw_seals'
sys.path.insert(0,str(SRC))
import s3_mw as M
G=M.G
train=np.array([(r,z) for r in (7.,9.,11.,13.,15.,17.) for z in (.3,.7,1.2,2.,3.)])
test=np.array([(r,z) for r in (8.,10.,12.,14.,16.) for z in (.5,.95,1.6,2.5)])
pts=np.concatenate([train,test]); n=len(train)
def halo(p,points,order=128):
    # Homoeoidal density rho(m)=rho_s/[m/rs(1+m/rs)^2], m^2=R^2+z^2/q^2.
    rho,rs,q=np.exp(p)
    x,w=leggauss(order); s=(x+1)/2; w=w/2
    u=1/s**2-1; jac=2/s**3
    R,z=points.T; R=R[:,None]; z=z[:,None]
    m=np.sqrt(R**2/(1+u)+z**2/(q*q+u))
    dens=rho/((m/rs)*(1+m/rs)**2)
    common=dens*jac*w
    fr=2*np.pi*G*q*R[:,0]*np.sum(common/(1+u)**2/np.sqrt(q*q+u),axis=1)
    fz=2*np.pi*G*q*z[:,0]*np.sum(common/(1+u)/(q*q+u)**1.5,axis=1)
    return np.column_stack([fr,fz])
def mn(p,points):
    mass,a,b=np.exp(p); R,z=points.T; h=np.sqrt(z*z+b*b); d=(R*R+(a+h)**2)**1.5
    return G*mass*np.column_stack([R/d,(a+h)*z/h/d])
def model(p,points,kind):
    if kind=='spherical': return halo([p[0],p[1],0.],points)
    if kind in ('oblate_moderate','oblate_free'): return halo(p[:3],points)
    return halo([p[0],p[1],0.],points)+mn(p[2:5],points)
# Independent spherical analytic benchmark and quadrature refinement.
p=np.log([1e7,15.,1.]); rr=np.linalg.norm(pts,axis=1); enclosed=4*np.pi*1e7*15**3*(np.log1p(rr/15)-rr/(15+rr))
exact=G*enclosed[:,None]*pts/rr[:,None]**3
bench=float(np.max(abs(halo(p,pts)/exact-1))); assert bench<1e-10
quad_error=max(float(np.max(abs(halo(np.log([1e7,15,q]),pts,128)/halo(np.log([1e7,15,q]),pts,256)-1))) for q in (.08,.3,.6,1.))
assert quad_error<1e-7
# Independent Poisson divergence check against the specified oblate density.
pcheck=np.log([1e7,15.,.3]); h=1e-3
rad=np.array([h,0.]); vert=np.array([0.,h])
f=halo(pcheck,pts)
div=(halo(pcheck,pts+rad)[:,0]-halo(pcheck,pts-rad)[:,0])/(2*h)+f[:,0]/pts[:,0]+(halo(pcheck,pts+vert)[:,1]-halo(pcheck,pts-vert)[:,1])/(2*h)
mell=np.sqrt(pts[:,0]**2+(pts[:,1]/.3)**2)
rho=1e7/((mell/15)*(1+mell/15)**2)
poisson_error=float(np.max(abs(div/(4*np.pi*G*rho)-1)))
assert poisson_error<1e-5
fields={}
for tag,grid in [('main',M.GRID_MAIN),('fine',M.GRID_FINE)]:
    mw=M.MW(grid,tag=tag); g=mw.g
    def sample(phi,pb):
        return np.column_stack([RegularGridInterpolator((g.Rc,g.zc),d)(pts) for d in g.cell_derivs(phi,pb)])
    stars=sample(mw.PhiN_s,mw.PBN_s); bary=sample(*mw.phiN(1.))
    for foot in ('canonical','alt'):
        key=f'{tag}|{foot}|s1.000000|eN0.000000|'
        path=SRC/'_cache_final'/('mw_'+hashlib.sha1(key.encode()).hexdigest()[:16]+'.npz')
        with np.load(path,allow_pickle=False) as a: total=sample(a['Phi'],{k:a['PB_'+k] for k in ('R','B','T')})
        fields[tag,foot]=(total,bary,stars)
results={'scope':'isolated static v3; fixed target census; halo force fits, no selection function or observed covariance', 'points_kpc':pts.tolist(),'training_count':n,'heldout_count':len(test),'controls':{'spherical_relative_error':bench,'quadrature_relative_error':quad_error,'oblate_poisson_relative_error':poisson_error},'fits':[]}
for foot in ('canonical','alt'):
    total,bary,stars=fields['fine',foot]
    results.setdefault('grid_difference',{})[foot]=float(np.max(abs(fields['main',foot][0]/total-1)))
    for kind in ('spherical','oblate_moderate','oblate_free','halo_plus_disc'):
      for nuisance in (False,True):
        lo=[np.log(1e3),np.log(.5)]; hi=[np.log(1e10),np.log(100.)]
        if 'oblate' in kind: lo+=[np.log(.6 if kind=='oblate_moderate' else .08)]; hi+=[0.]
        if kind=='halo_plus_disc': lo+=list(np.log([1e7,.1,.03])); hi+=list(np.log([2e11,30.,5.]))
        if nuisance: lo+=[M.SM]; hi+=[M.SP]
        def residual(p,points,sl):
            scale=p[-1] if nuisance else 1.
            return ((bary[sl]+(scale-1)*stars[sl]+model(p,points,kind)-total[sl])/total[sl]).ravel()
        sols=[]
        for rs,q in ((5.,.3),(15.,.6),(40.,.9)):
            p=list(np.log([1e7,rs]))
            if 'oblate' in kind:p+=[np.log(max(q,.61) if kind=='oblate_moderate' else q)]
            if kind=='halo_plus_disc':p+=list(np.log([2e10,5.,.3]))
            if nuisance:p+=[1.]
            sol=least_squares(residual,p,bounds=(lo,hi),args=(train,slice(0,n)),max_nfev=400,ftol=1e-11,xtol=1e-11,gtol=1e-11)
            sols.append(sol)
        best=min(sols,key=lambda s:np.sum(s.fun**2)); assert best.success
        rt=residual(best.x,test,slice(n,None)).reshape(-1,2)
        params=np.exp(best.x[:-1] if nuisance else best.x).tolist()
        result=dict(footing=foot,model=kind,stellar_nuisance=nuisance,physical_parameters=params,stellar_scale=float(best.x[-1]) if nuisance else 1.,train_rms_fraction=float(np.sqrt(np.mean(best.fun**2))),heldout_rms_fraction=float(np.sqrt(np.mean(rt**2))),heldout_max_fraction=float(np.max(abs(rt))),heldout_R_rms=float(np.sqrt(np.mean(rt[:,0]**2))),heldout_z_rms=float(np.sqrt(np.mean(rt[:,1]**2))),heldout_residuals=rt.tolist(),multistart_costs=[float(np.sum(s.fun**2)) for s in sols],bound_active=best.active_mask.tolist())
        # Hypothetical 40 independent, equal-fractional-error force measurements, parameters fixed by training.
        result['toy_3sigma_equal_fractional_error']=float(np.linalg.norm(rt)/3)
        if kind=='halo_plus_disc':
            mass,a,b=params[2:5]; R=8.122
            def density(z):
                h=np.sqrt(z*z+b*b)
                return b*b*mass/(4*np.pi)*(a*R*R+(a+3*h)*(a+h)**2)/((R*R+(a+h)**2)**2.5*h**3)
            result['disc_local_density_Msun_pc3']=density(0)/1e9
            result['disc_column_within_1p1kpc_Msun_pc2']=2*quad(density,0,1.1)[0]/1e6
            result['disc_total_column_Msun_pc2']=2*quad(density,0,np.inf)[0]/1e6
        result['toy_SNR_2percent_independent']=float(np.linalg.norm(rt)/.02)
        result['toy_SNR_5percent_independent']=float(np.linalg.norm(rt)/.05)
        result['toy_SNR_2percent_plus_1percent_signal_aligned_systematic']=float(np.linalg.norm(rt)/np.sqrt(.02**2+rt.size*.01**2))
        results['fits'].append(result)
        print(foot,kind,nuisance,'rms%',round(result['heldout_rms_fraction']*100,3),'max%',round(result['heldout_max_fraction']*100,3),'params',params,'s',result['stellar_scale'],flush=True)
assert all(np.isfinite(r['heldout_rms_fraction']) for r in results['fits'])
results['direct_acceleration_displacement_microas']=.5*2e-10*(5.5*365.25*86400)**2/(3.085677581e19)*206264806247.
path=ROOT/sys.argv[1];path.write_text(json.dumps(results,indent=2)+'\n')
