"""Spherical constant-anisotropy aperture Jeans diagnostic, not a full model.
Units kpc, km/s, Msun. DESI fiber diameter1.5arcsec; Gaussian seeing scenarios.
"""
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.special import gammaincinv,gammaln
from scipy.stats import ncx2
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parent
sys.path.insert(0,str(ROOT/'euclid_for_j0332_fit_2026_11_13'))
from aqual_lensing import geometry
G=4.30091e-6;A0=9.3603e-11*3.085677581491367e19/1e6

def sersic_profile(n,re,nr=5000,nquad=256):
    lr=np.linspace(-16,10,nr);x=np.exp(lr);b=gammaincinv(2*n,.5)
    z,w=np.polynomial.legendre.leggauss(nquad);t=(z+1)*np.pi/4;w*=np.pi/4;sec=1/np.cos(t)
    logSigma0=2*n*np.log(b)-np.log(2*np.pi*n)-gammaln(2*n)
    logpref=logSigma0+np.log(b/(np.pi*n))
    nu=np.exp(logpref+(1/n-1)*lr)*np.sum(w*sec**(1/n)*np.exp(-b*(x[:,None]*sec)**(1/n)),axis=1)
    mf=cumulative_trapezoid(4*np.pi*nu*x**3,lr,initial=0)
    def sigma(R):return np.exp(logSigma0-b*(R/re)**(1/n))/re**2
    return x*re,nu/re**3,mf,sigma

def jeans_pressure(r,nu,acc,beta=0.):
    lr=np.log(r);integrand=nu*acc*r**(2*beta+1)
    integral=-cumulative_trapezoid(integrand[::-1],lr[::-1],initial=0)[::-1]
    return integral*r**(-2*beta)

def projected_pressure(R,r,p,beta=0.,nodes=256):
    x,w=np.polynomial.legendre.leggauss(nodes);t=(x+1)*np.pi/4;w*=np.pi/4
    radii=R[:,None]/np.cos(t)
    val=np.exp(np.interp(np.log(radii),np.log(r),np.log(np.maximum(p,1e-300)),right=-1000))
    return 2*R*np.sum(val*(1-beta*np.cos(t)**2)/np.cos(t)**2*w,axis=1)

def aperture_dispersion(r,nu,acc,sigma,re,ap,beta=0.,seeing_sigma=0.,nrproj=400,nlos=256):
    pressure=jeans_pressure(r,nu,acc,beta)
    maxr=ap+10*seeing_sigma if seeing_sigma>0 else ap
    R=np.geomspace(re*1e-6,maxr,nrproj)
    projected=projected_pressure(R,r,pressure,beta,nlos)
    weight=ncx2.cdf((ap/seeing_sigma)**2,2,(R/seeing_sigma)**2) if seeing_sigma>0 else np.ones_like(R)
    num=np.trapz(2*np.pi*R**2*weight*projected,np.log(R))
    den=np.trapz(2*np.pi*R**2*weight*sigma(R),np.log(R))
    return np.sqrt(num/den),den

def benchmark():
    r=np.geomspace(1e-7,1e5,9000);nu=3/(4*np.pi)*(1+r*r)**(-2.5);gn=r/(1+r*r)**1.5
    p=jeans_pressure(r,nu,gn);exactp=nu/(6*np.sqrt(1+r*r));sel=(r>.01)&(r<10)
    pe=float(np.max(abs(p[sel]/exactp[sel]-1)))
    R=np.array([.01,.1,.5,1.,3.,10.]);projected=projected_pressure(R,r,p)
    surface=1/(np.pi*(1+R*R)**2);exactlos=3*np.pi/64/np.sqrt(1+R*R)
    loserr=float(np.max(abs(projected/surface/exactlos-1)))
    aps=[]
    for a in [.25,1.,4.]:
        sig,_=aperture_dispersion(r,nu,gn,lambda R:1/(np.pi*(1+R*R)**2),1.,a)
        exact=np.pi/32*(1-(1+a*a)**(-1.5))/(a*a/(1+a*a))
        aps.append({'aperture':a,'sigma_squared_numeric':sig*sig,'analytic':exact,'relative_error':sig*sig/exact-1})
    assert pe<3e-5 and loserr<4e-5 and max(abs(z['relative_error']) for z in aps)<.001
    return dict(plummer_pressure_max_relative=pe,plummer_projected_max_relative=loserr,plummer_apertures=aps)

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);tests=benchmark();records=[]
    with open(ROOT/'euclid_for_j0332_fit_2026_11_13/desi_crossmatch/matches_1arcsec.csv') as f:matches=list(csv.DictReader(f))
    wanted={r['Unique_Identifier'] for r in matches}
    with open(ROOT/'euclid_eclipse_screen_2026_11_13/run_02/screen_all_15072.csv') as f:catalog={r['unique_identifier']:r for r in csv.DictReader(f) if r['unique_identifier'] in wanted}
    for spec in matches:
        c=catalog[spec['Unique_Identifier']]
        if not c['eclipse_log_survived_mass_med']:
            records.append(dict(id=spec['Unique_Identifier'],status='missing_Euclid_stellar_mass'));continue
        zl=float(spec['Z']);zp=float(c['eclipse_median_phz']);scale=geometry(zl)[0];scalephoto=geometry(zp)[0]
        mass_shift=2*np.log10(scale/scalephoto*((1+zl)/(1+zp))**2)
        m0=float(c['eclipse_log_survived_mass_med'])+mass_shift
        re=float(c['eclipse_effective_radius'])*scale;n=float(c['eclipse_sersic_index'])
        r,nu,mf,surface=sersic_profile(n,re);scenarios=[]
        for mass_label,delta in [('low68',-float(c['eclipse_log_survived_mass_low'])),('median',0.),('upper68',float(c['eclipse_log_survived_mass_upp']))]:
            mass=10**(m0+delta);gn=G*mass*mf/r**2;acc=.5*(gn+np.sqrt(gn*gn+4*A0*gn))
            for beta in [-.3,0.,.3]:
                for seeing in [.8,1.2,1.6]:
                    predicted,light=aperture_dispersion(r,nu,acc,surface,re,.75*scale,beta,seeing*scale/2.354820045)
                    scenarios.append(dict(mass=mass_label,beta=beta,seeing_fwhm_arcsec=seeing,predicted_sigma_kms=predicted,fiber_light_fraction=light))
        gn=G*10**m0*mf/r**2;versions={}
        for name,factor in [('Newton',0.),('a0_half',.5),('canonical',1.),('a0_twice',2.)]:
            g=gn if factor==0 else .5*(gn+np.sqrt(gn*gn+4*A0*factor*gn))
            versions[name]=aperture_dispersion(r,nu,g,surface,re,.75*scale,0,1.2*scale/2.354820045)[0]
        central=versions['canonical'];observed=float(spec['VDISP']);err=float(spec['VDISP_error_kms'])
        record=dict(id=spec['Unique_Identifier'],zl=zl,photoz=zp,flux_distance_only_logmass_shift=mass_shift,adopted_logmass=m0,re_kpc=re,sersic_n=n,shape_axis_ratio=float(c['axis_ratio_proxy']),observed_sigma_kms=observed,observed_error_kms=err,central_prediction_kms=central,observational_error_only_pull=(observed-central)/err,versions=versions,scenario_min_kms=min(x['predicted_sigma_kms'] for x in scenarios),scenario_max_kms=max(x['predicted_sigma_kms'] for x in scenarios),mass_integral=mf[-1],final_sample=c['final_sample'],lens_model_success=c['lens_model_success'],scenarios=scenarios)
        assert abs(mf[-1]-1)<2e-4
        records.append(record);print(json.dumps({k:v for k,v in record.items() if k!='scenarios'}),flush=True)
    result=dict(assertion_tested='Finite spherical aperture-Jeans predictions versus actual DESI velocity dispersions with explicit mass/anisotropy/seeing scenarios',benchmarks=tests,records=records,non_claims=['Not flattened rotating galaxy dynamics','No measured seeing or anisotropy prior','No dynamics inference for sources with absent or rejected mass fits','No spectroscopic remeasurement or systematic error calibration','Mass photoz correction is flux-distance only, not SED refit','No theory confirmation or exclusion from observational-error-only pulls'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
