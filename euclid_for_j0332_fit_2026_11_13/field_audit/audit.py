"""Independent flattened Newtonian projection and finite AQUAL convergence audit."""
import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import quad
from scipy.special import gammainc, gammaincinv, gammaln

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('aqual_lensing',ROOT/'euclid_for_j0332_fit_2026_11_13/aqual_lensing.py')
lens=importlib.util.module_from_spec(spec);spec.loader.exec_module(lens)


def analytic_elliptical(u,v,q,rs_arcsec,n,mass):
    """Elliptically stratified projected surface density, exact 1D quadrature.

    u,v and major-axis scale are arcsec. Sigma has units Msun/kpc^2.
    q=1 recovers alpha=mean(kappa,<R)*R with no extra factor two.
    Endpoint substitution t=s^(2n) regularizes high-n central cusp.
    """
    scale,ratio=lens.geometry()
    dl=scale*lens.ARCSEC
    sigmacrit=lens.C**2/(4*np.pi*lens.G*dl*ratio)
    b=gammaincinv(2*n,.5)
    sigma0=np.exp(2*n*np.log(b)-np.log(2*np.pi*n)-gammaln(2*n))*mass/(q*(rs_arcsec*scale)**2)
    def f(s,power):
        t=s**(2*n)
        d=1-(1-q*q)*t
        m=np.sqrt(t*(u*u+v*v/d))
        kappa=sigma0*np.exp(-b*(m/rs_arcsec)**(1/n))/sigmacrit
        return 2*n*s**(2*n-1)*kappa/d**power
    au=q*u*quad(lambda s:f(s,.5),0,1,epsabs=1e-11,epsrel=1e-11,limit=300)[0]
    av=q*v*quad(lambda s:f(s,1.5),0,1,epsabs=1e-11,epsrel=1e-11,limit=300)[0]
    return au,av


def vector_error(numeric,reference):
    return np.sqrt(np.sum((numeric-reference)**2,axis=1))/np.sqrt(np.sum(reference**2,axis=1))


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    q=.813;n=5.8687;mass=1e12;rearc=1.13918/np.sqrt(q)
    scale,ratio=lens.geometry();rekpc=rearc*scale
    radii=np.array([.5,1.,1.5,2.,3.]); angles=np.array([0.,45.,90.])
    rad,ang=np.meshgrid(radii,angles,indexing='ij');rad=rad.ravel();ang=ang.ravel()
    u=rad*np.cos(np.deg2rad(ang));v=rad*np.sin(np.deg2rad(ang))
    reference=np.array([analytic_elliptical(x,y,q,rearc,n,mass) for x,y in zip(u,v)])
    circular=np.array([analytic_elliptical(r,0,1,rearc,n,mass)[0] for r in radii])
    b=gammaincinv(2*n,.5)
    circular_exact=4*lens.G*mass*gammainc(2*n,b*(radii/rearc)**(1/n))/(lens.C**2*radii*scale)*ratio*lens.ARCSEC
    circular_error=float(np.max(abs(circular/circular_exact-1)))
    assert circular_error<1e-9
    records=[];fields={}; comparisons={}
    configs=[(256,48,500.),(512,96,500.),(512,96,1000.)]
    for inc in [90.,60.]:
        # Fixed observed flattening; intrinsic oblate qi changes with inclination.
        qi=np.sqrt((q*q-np.cos(np.deg2rad(inc))**2)/np.sin(np.deg2rad(inc))**2)
        for mu_one in [True,False]:
            for nr,nt,rmax in configs:
                start=time.monotonic()
                field=lens.make_field(mass,rekpc,n,qi,nr=nr,nt=nt,rmax_re=rmax,mu_one=mu_one,tol=1e-9)
                vals={}
                for nlos in [192,384,768]:
                    vals[str(nlos)]=np.array(lens.projected_deflection(field,u,v,inc,nlos=nlos)).T
                # Explicit residual even though Newtonian solve reports zero by construction.
                matrix=lens.fv.assemble(field['grid'],field['phi'],lens.fv.a0_kpc(field['a0']),mu_one)
                lr,ld=lens.spherical_density_table(n)
                def rho(R,z):
                    m=np.sqrt(R*R+(z/qi)**2)/rekpc
                    return mass/(qi*rekpc**3)*np.exp(np.interp(np.log(m),lr,ld))
                cells=field['grid'].deposit(rho,nsub=5)
                rhs=4*np.pi*lens.G*cells.ravel()
                residual=float(np.linalg.norm(matrix@field['phi'].ravel()-rhs)/np.linalg.norm(rhs))
                assert residual<2e-9
                label=f'inc{int(inc)}_'+('newtonian' if mu_one else 'aqual')+f'_{nr}_{nt}_{int(rmax)}'
                rec={'label':label,'inclination_deg':inc,'projected_q':q,'intrinsic_q':float(qi),'mu_one':mu_one,
                     'nr':nr,'nt':nt,'rmax_re':rmax,'deposited_mass_fraction_error':float(field['deposited_mass']/mass-1),
                     'reported_solver_residual':float(field['residual']),'explicit_discrete_residual':residual,
                     'solver_iterations':field['iterations'],'seconds':time.monotonic()-start,
                     'deflections':{k:a.tolist() for k,a in vals.items()},
                     'LOS_192_vs_768_max_vector_relative_difference':float(max(vector_error(vals['192'],vals['768']))),
                     'LOS_384_vs_768_max_vector_relative_difference':float(max(vector_error(vals['384'],vals['768'])))}
                if mu_one:
                    err=vector_error(vals['768'],reference)
                    rec['analytic_newtonian_relative_vector_error']=err.tolist()
                    rec['analytic_newtonian_max_relative_vector_error']=float(max(err))
                records.append(rec);fields[label]=vals['768']
                print(json.dumps({k:v for k,v in rec.items() if k not in ['deflections','analytic_newtonian_relative_vector_error']}),flush=True)
    for inc in [90,60]:
        for theory in ['newtonian','aqual']:
            prefix=f'inc{inc}_{theory}_'
            low=fields[prefix+'256_48_500'];fine=fields[prefix+'512_96_500'];far=fields[prefix+'512_96_1000']
            comparisons[prefix+'mesh_256_to_512']={'max_vector_relative_change':float(max(vector_error(low,fine))),'pointwise_vector_relative_change':vector_error(low,fine).tolist()}
            comparisons[prefix+'outer_500_to_1000']={'max_vector_relative_change':float(max(vector_error(fine,far))),'pointwise_vector_relative_change':vector_error(fine,far).tolist()}
    result={'assertion_tested':'For one oblate Sersic lens at 15 arc positions and two inclinations, projected Newtonian finite-volume field agrees with analytic elliptical Sersic lensing and AQUAL deflection is stable over the specified mesh/domain/LOS variations.',
            'inputs':{'mass_Msun':mass,'sersic_n':n,'Re_geometric_mean_arcsec':1.13918,'Re_major_arcsec':float(rearc),'Re_major_kpc':float(rekpc),'q_projected':q,'a0_m_s2':9.3603e-11,'radii_arcsec':radii.tolist(),'angles_deg':angles.tolist(),'geometry_scale_kpc_per_arcsec':float(scale),'Dls_Ds':float(ratio)},
            'points':[{'u_arcsec':float(x),'v_arcsec':float(y),'radius_arcsec':float(r),'angle_deg':float(a)} for x,y,r,a in zip(u,v,rad,ang)],
            'analytic_newtonian_reference':reference.tolist(),'circular_limit_relative_error':circular_error,'field_runs':records,'comparisons':comparisons,
            'non_claims':['No image likelihood, covariance, full parameter-domain certification or theory validation.','Mesh convergence does not establish absolute AQUAL accuracy; the analytic absolute comparison is Newtonian only.','Outer-domain comparison at fixed nr also changes radial spacing, so its difference combines boundary and discretization effects.','All inclinations share projected q=.813; intrinsic flattening varies accordingly.']}
    newton_err=max(r['analytic_newtonian_max_relative_vector_error'] for r in records if r['mu_one'])
    finest_newton=max(r['analytic_newtonian_max_relative_vector_error'] for r in records if r['mu_one'] and r['nr']==512)
    mesh_aqual=max(v['max_vector_relative_change'] for k,v in comparisons.items() if 'aqual' in k and 'mesh' in k)
    los=max(r['LOS_192_vs_768_max_vector_relative_difference'] for r in records)
    result['summary']={'max_all_Newtonian_absolute_vector_error':newton_err,'max_512_Newtonian_absolute_vector_error':finest_newton,'max_AQUAL_mesh_relative_change':mesh_aqual,'max_LOS192_relative_change':los,'target_relative_tolerance':.002,'finite_02percent_target_passed':bool(max(newton_err,mesh_aqual,los)<.002)}
    result['outcome']='finite numerical checks passed at stated points' if result['summary']['finite_02percent_target_passed'] else 'numerical target not reached; inspect measured errors'
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary']),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);main(p.parse_args().output)
