"""L015780 finite-aperture mass + spherical Jeans diagnostic.

Not an oblate/rotating dynamical fit. The elliptical light aperture correction
is exact for the adopted COOLEST point; spherical Jeans uses its geometric Re.
"""
import argparse,csv,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.integrate import cumulative_trapezoid,quad
from scipy.special import gammaincinv,gammainc,gammaln
from scipy.stats import ncx2,norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astropy.io import fits
BASE=Path(__file__).resolve().parents[2];ROOT=BASE.parent
sys.path.insert(0,str(BASE/'light_shapes'))
from fit_light_shapes import Renderer
sys.path.insert(0,str(BASE/'dynamics'))
from jeans_diagnostic import sersic_profile,aperture_dispersion,projected_pressure,jeans_pressure,benchmark,G,A0,geometry
INPUT=BASE/'l015780_inputs'
BETAS=[-.3,0.,.3];SEEINGS=[.8,1.2,1.6]

def aperture_factor():
    info=json.loads((INPUT/'dataset/info.json').read_text())
    light=json.loads((INPUT/'results/coolest_sersic.json').read_text())['lensing_entities'][0]['light_model'][0]['parameters']
    get=lambda k:light[k]['point_estimate']['value']
    n,re,q=get('n'),get('theta_eff'),get('q');cx,cy=get('center_x'),get('center_y');phi=np.pi/2+np.deg2rad(get('phi'))
    pix=info['pixel_scale'];assert pix==.1
    a=fits.getdata(INPUT/'results/pre_psf.fits','VIS_GALAXY_0');yy,xx=np.indices(a.shape)
    X=(xx-(a.shape[1]-1)/2)*pix;Y=(yy-(a.shape[0]-1)/2)*pix
    mask=(X-info['mask_centre'][1])**2+(Y+info['mask_centre'][0])**2<info['mask_radius']**2
    p=np.array([cx,cy,np.log(re/np.sqrt(q)),np.log(n),q,phi])
    vals=[float(Renderer(np.ones((1,1)),shape=a.shape,fine=f).render(p)[mask].sum()) for f in [False,True]]
    assert abs(vals[1]-vals[0])<1e-6
    b=gammaincinv(2*n,.5);inf=get('I_eff')/pix**2*2*np.pi*re*re*n*np.exp(b+gammaln(2*n)-2*n*np.log(b))
    return dict(fraction_pixel_union=vals[1],fraction_base_renderer=vals[0],pixel_integration_abs_difference=abs(vals[1]-vals[0]),
        fraction_released_map_over_analytic_infinite=float(a[mask].sum()/inf),map_sum=float(a[mask].sum()),analytic_infinite_flux=float(inf),
        included_pixel_centers=int(mask.sum()),cutout_shape=list(a.shape),mask=info,n=n,Re_geometric_arcsec=re,Re_major_arcsec=re/np.sqrt(q),q=q,
        center_west_arcsec=cx,center_north_arcsec=cy,phi_west_radians=phi,log10_mass_correction=float(-np.log10(vals[1])))

def aperture_kernel(r,beta,ap,seeing_sigma,ntheta=128):
    """Linear acceleration-to-aperture-second-moment kernel.

    Projected aperture numerator =4pi int p(r)r^2 A(r)dr, where
    A=int sin(t)(1-beta sin²(t)) W(r sin(t))dt. Exchange the Jeans
    and aperture integrals to evaluate the numerator directly against nu*g.
    """
    maxR=ap+10*seeing_sigma if seeing_sigma else ap
    hi=np.arcsin(np.minimum(maxR/r,1.));z,w=np.polynomial.legendre.leggauss(ntheta)
    t=(z[None,:]+1)*hi[:,None]/2;st=np.sin(t);R=r[:,None]*st
    W=ncx2.cdf((ap/seeing_sigma)**2,2,(R/seeing_sigma)**2) if seeing_sigma else np.ones_like(R)
    angular=np.sum(w[None,:]*st*(1-beta*st*st)*W,axis=1)*hi/2
    primitive=cumulative_trapezoid(4*np.pi*r**(3-2*beta)*angular,np.log(r),initial=0)
    return r**(2*beta+1)*primitive

def light_throughput(surface,re,ap,seeing_sigma,nr=1200):
    R=np.geomspace(re*1e-7,ap+10*seeing_sigma if seeing_sigma else ap,nr)
    W=ncx2.cdf((ap/seeing_sigma)**2,2,(R/seeing_sigma)**2) if seeing_sigma else np.ones_like(R)
    return float(np.trapz(2*np.pi*R*R*surface(R)*W,np.log(R)))

def quantile_density(x,p):
    p=p/np.trapz(p,x);cdf=cumulative_trapezoid(p,x,initial=0);return np.interp([.025,.16,.5,.84,.975],cdf,x).tolist()

def make_predictions(n,re,ap,scale,logm,nr=5000,nabel=256,ntheta=128,nlight=1200):
    r,nu,mf,surface=sersic_profile(n,re,nr,nabel);mass=10**logm
    gn=G*mass[:,None]*mf[None,:]/r[None,:]**2;acc=.5*(gn+np.sqrt(gn*gn+4*A0*gn));lr=np.log(r)
    values={};lights={};kernels={}
    for seeing in SEEINGS:
        ss=seeing*scale/2.354820045
        den=light_throughput(surface,re,ap,ss,nlight);lights[seeing]=den
        for beta in BETAS:
            key=(beta,seeing);kernel=aperture_kernel(r,beta,ap,ss,ntheta);kernels[key]=kernel
            values[key]=np.sqrt(np.trapz(nu[None,:]*acc*kernel[None,:],lr,axis=1)/den)
    return values,lights,dict(r=r,nu=nu,mf=mf,surface=surface,kernels=kernels)

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);af=aperture_factor()
    cat=next(x for x in csv.DictReader(open(ROOT/'euclid_eclipse_screen_2026_11_13/run_02/screen_all_15072.csv')) if x['unique_identifier']=='EUCL-DR1-L015780')
    desi=next(x for x in csv.DictReader(open(ROOT/'euclid_for_j0332_fit_2026_11_13/desi_crossmatch/matches_1arcsec.csv')) if x['Unique_Identifier']=='EUCL-DR1-L015780')
    fast=json.loads((INPUT/'fastspec_target_rows.json').read_text());v3=fast['30_SPECPHOT']
    zl=float(desi['Z']);scale=geometry(zl)[0];re=af['Re_geometric_arcsec']*scale;ap=.75*scale
    m_ap=float(cat['eclipse_log_survived_mass_med']);lo=float(cat['eclipse_log_survived_mass_low']);hi=float(cat['eclipse_log_survived_mass_upp']);m0=m_ap+af['log10_mass_correction']
    obs={'v21':{'sigma':float(desi['VDISP']),'error':float(desi['VDISP_error_kms'])},'v30':{'sigma':v3['VDISP'],'error':1/np.sqrt(v3['VDISP_IVAR'])}}
    central=dict(aperture=af,logM_aperture_SED_median=m_ap,logM_infinite_SED_median=m0,SED_error_lower=lo,SED_error_upper=hi,
        adopted_SED_redshift_transport_dex=0.,zl=zl,scale_kpc_per_arcsec=scale,Re_spherical_kpc=re,fiber_radius_arcsec=.75,observations=obs)
    (out/'central.json').write_text(json.dumps(central,indent=2)+'\n');print(json.dumps(central),flush=True)
    checks={'plummer_existing_analytic':benchmark()}
    # A grid containing the SED median avoids a quadrature convention at the
    # discontinuity of the two-half-normal, equal-tail mass-prior surrogate.
    logm=m0+np.linspace(-1.2,1.4,1301);values,lights,raw=make_predictions(af['n'],re,ap,scale,logm)
    r,nu,mf,surface=[raw[k] for k in ['r','nu','mf','surface']];mid=int(np.argmin(abs(logm-m0)))
    checks['Abel_total_mass_fraction']=float(mf[-1]);assert abs(mf[-1]-1)<2e-4
    radius_test=np.array([.05,.2,.75,2.,5.])*scale
    projected=projected_pressure(radius_test,r,nu,0.,512)
    checks['Abel_reprojection_max_relative']=float(np.max(abs(projected/surface(radius_test)-1)))
    assert checks['Abel_reprojection_max_relative']<.001
    # Independent Jeans->LOS->aperture quadrature versus exchanged-integral kernel.
    gn=G*10**m0*mf/r**2;acc=.5*(gn+np.sqrt(gn*gn+4*A0*gn));direct=[]
    for beta in BETAS:
        for seeing in SEEINGS:
            s,den=aperture_dispersion(r,nu,acc,surface,re,ap,beta,seeing*scale/2.354820045,nrproj=800,nlos=512)
            direct.append(dict(beta=beta,seeing=seeing,kernel_sigma=float(values[(beta,seeing)][mid]),direct_sigma=s,relative_difference=float(values[(beta,seeing)][mid]/s-1),direct_light=den))
    checks['independent_direct_projection']=direct;assert max(abs(x['relative_difference']) for x in direct)<.001
    offsets=json.loads((BASE/'l015780_joint/observational_audit/fiber_light_offsets.json').read_text());off=offsets['fiber_light_separation_arcsec']*scale
    ss=1.2*scale/2.354820045;RR=np.geomspace(re*1e-6,ap+off+10*ss,800)
    angles=np.arange(64)*2*np.pi/64;dist2=RR[:,None]**2+off**2+2*RR[:,None]*off*np.cos(angles)
    ww=ncx2.cdf((ap/ss)**2,2,dist2/ss**2).mean(axis=1)
    proj=projected_pressure(RR,r,jeans_pressure(r,nu,acc),nodes=512)
    den_off=np.trapz(2*np.pi*RR**2*ww*surface(RR),np.log(RR));sig_off=np.sqrt(np.trapz(2*np.pi*RR**2*ww*proj,np.log(RR))/den_off)
    checks['measured_fiber_offset_sensitivity']={'offset_arcsec':off/scale,'beta':0.,'seeing_fwhm_arcsec':1.2,'sigma_centered':float(values[(0.,1.2)][mid]),'sigma_offset':float(sig_off),'light_offset':float(den_off),'relative_sigma_difference':float(sig_off/values[(0.,1.2)][mid]-1)}
    fine,finelight,_=make_predictions(af['n'],re,ap,scale,np.array([m0-.3,m0,m0+.3]),nr=10000,nabel=512,ntheta=256,nlight=2400)
    convergence=[]
    for key in values:
        coarse=np.interp([m0-.3,m0,m0+.3],logm,values[key]);rel=fine[key]/coarse-1
        convergence.append(dict(beta=key[0],seeing=key[1],relative_sigma_differences=rel.tolist(),relative_light_difference=finelight[key[1]]/lights[key[1]]-1))
    checks['resolution_doubling']=convergence;assert max(max(abs(np.array(x['relative_sigma_differences']))) for x in convergence)<.001
    den0=light_throughput(surface,re,ap,0.);exactden=gammainc(2*af['n'],gammaincinv(2*af['n'],.5)*(ap/re)**(1/af['n']))
    checks['no_seeing_aperture_light']={'numeric':den0,'analytic':float(exactden),'relative_difference':float(den0/exactden-1)}
    assert abs(den0/exactden-1)<.001
    # The kernel has an independent analytic Plummer aperture benchmark.
    pr=np.geomspace(1e-7,1e5,9000);pnu=3/(4*np.pi)*(1+pr*pr)**(-2.5);pg=pr/(1+pr*pr)**1.5;plchecks=[]
    for aa in [.25,1.,4.]:
        val=np.trapz(pnu*pg*aperture_kernel(pr,0.,aa,0.),np.log(pr))/(aa*aa/(1+aa*aa))
        exact=np.pi/32*(1-(1+aa*aa)**(-1.5))/(aa*aa/(1+aa*aa))
        plchecks.append({'aperture':aa,'relative_second_moment_error':float(val/exact-1)})
    checks['Plummer_exchanged_kernel']=plchecks;assert max(abs(x['relative_second_moment_error']) for x in plchecks)<.001
    # Equal probability on either side of catalogue median, with 16/84 offsets.
    sig=np.where(logm<m0,lo,hi);prior=norm.pdf((logm-m0)/sig)/sig
    prior[mid]=.5*norm.pdf(0)*(1/lo+1/hi)
    prior/=np.trapz(prior,logm);records=[];columns={'log10_total_mass':logm,'SED_prior_density_per_dex':prior}
    for key,pred in values.items():
        beta,seeing=key;row=dict(beta=beta,seeing_fwhm_arcsec=seeing,fiber_light_fraction=lights[seeing],sigma_at_SED_median_kms=float(pred[mid]),
            sigma_at_SED_16_84_kms=np.interp([m0-lo,m0+hi],logm,pred).tolist(),mass_conditioned={})
        columns[f'sigma_beta{beta}_seeing{seeing}']=pred
        for name,o in obs.items():
            like=np.exp(-.5*((pred-o['sigma'])/o['error'])**2);post=prior*like
            row['mass_conditioned'][name]=dict(dynamics_only_best_logM=float(np.interp(o['sigma'],pred,logm)),
                dynamics_only_equal_tailed_observed_sigma_16_84_logM=np.interp([max(o['sigma']-o['error'],0),o['sigma']+o['error']],pred,logm).tolist(),
                SED_and_dynamics_logM_quantiles=quantile_density(logm,post),SED_median_observational_error_only_pull=(pred[mid]-o['sigma'])/o['error'])
            columns[f'{name}_likelihood_beta{beta}_seeing{seeing}']=like
            columns[f'{name}_posterior_beta{beta}_seeing{seeing}']=post/np.trapz(post,logm)
        records.append(row)
    with (out/'mass_scan.csv').open('w') as file:
        writer=csv.writer(file);writer.writerow(columns);writer.writerows(zip(*columns.values()))
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    colors={-.3:'tab:blue',0.:'tab:green',.3:'tab:orange'};styles={.8:':',1.2:'-',1.6:'--'}
    for (beta,seeing),pred in values.items():
        axes[0].plot(logm,pred,color=colors[beta],ls=styles[seeing],label=f'beta {beta}, seeing {seeing}"')
        like=np.exp(-.5*((pred-obs['v21']['sigma'])/obs['v21']['error'])**2);post=prior*like;post/=np.trapz(post,logm)
        axes[1].plot(logm,post,color=colors[beta],ls=styles[seeing])
    for ax in axes:ax.set_xlim(m0-.35,m0+.45);ax.axvline(m0,color='k',lw=.8);ax.set_xlabel('log10 total stellar mass / Msun')
    o=obs['v21'];axes[0].axhspan(o['sigma']-o['error'],o['sigma']+o['error'],color='grey',alpha=.2);axes[0].axhline(o['sigma'],color='grey');axes[0].set_ylim(150,500)
    axes[0].set_ylabel('Aperture dispersion (km/s)');axes[0].legend(fontsize=7,ncol=2)
    axes[1].plot(logm,prior,color='k',label='Aperture-corrected SED prior');axes[1].set_ylabel('Conditional density per dex');axes[1].legend(fontsize=8)
    fig.suptitle('L015780 spherical constant-beta fixture; seeing scenarios, no rotation');fig.tight_layout();fig.savefig(out/'mass_dynamics.png',dpi=160);plt.close(fig)
    result=dict(central=central,checks=checks,scenarios=records,quantile_levels=[.025,.16,.5,.84,.975],
        mass_grid=dict(min=float(logm[0]),max=float(logm[-1]),nodes=len(logm),step=float(logm[1]-logm[0])),
        prior_convention='Equal-tail two-half-normal surrogate for catalogue logmass median and asymmetric offsets; no new SED/redshift fit.',
        non_claims=['Spherical geometric-Re fixture, not flattened or rotating Jeans model.','Seeing/anisotropy are scenarios, not measured or marginalized priors.',
        'DESI v21 and v30 are alternative measurements, not independent datasets to multiply.','No full stellar-population, environment, source-redshift or image likelihood in this calculation.',
        'Infinite outer stellar wings and constant M/L are assumptions, not observed mass.','Conditional mass quantiles are not calibrated theory exclusion or full-model posterior.'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':checks,'scenarios':records}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
