"""Survey-conditional exploratory Jeans fit; see CONTRACT.md."""
import csv, hashlib, json, math, resource, subprocess, time
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import minimize
from scipy.special import logsumexp, ndtr
from numpy.polynomial.legendre import leggauss

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
G=.00430091; A0={'canonical':9.3603e-11*3.085677581491367e10,'alt':1.1312e-10*3.085677581491367e10}
INPUTS=[HERE/'data/members.tsv',HERE/'data/ReadMe.txt',ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv',HERE/'CONTRACT.md',Path(__file__)]
def hashes():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUTS}
def num(v):
    try:return float(v)
    except (TypeError,ValueError):return float('nan')
def load():
    lines=[l.rstrip('\n') for l in INPUTS[0].open() if l.strip() and not l.startswith('#')]
    keys=lines[0].split('\t');rows=[dict(zip(keys,map(str.strip,l.split('\t')))) for l in lines[3:]]
    assert len(rows)==612 and len({r['GaiaDR3'] for r in rows})==612
    cat=next(r for r in csv.DictReader(INPUTS[2].open()) if r['name']=='Sextans')
    selected=[r for r in rows if num(r['Pmem'])>.07 and num(r['CombSN'])>16 and num(r['Gmag'])<19.7 and 0<num(r['e_Vel'])<5 and np.isfinite(num(r['[Fe/H]']))]
    arr=lambda key:np.array([num(r[key]) for r in selected])
    dx=np.deg2rad(arr('RA_ICRS')-float(cat['ra']))*math.cos(math.radians(float(cat['dec'])))
    dy=np.deg2rad(arr('DE_ICRS')-float(cat['dec']));pa=math.radians(float(cat['position_angle']));q=1-float(cat['ellipticity'])
    angular=np.sqrt((dx*math.sin(pa)+dy*math.cos(pa))**2+((dx*math.cos(pa)-dy*math.sin(pa))/q)**2)
    distance=float(cat['distance']);R=angular*distance*1000*math.sqrt(q)
    # First order perspective velocity from observed transverse motion.
    perspective=4.74047*distance*(float(cat['pmra'])*dx+float(cat['pmdec'])*dy)
    aa=np.deg2rad([.339,.62])*distance*1000*math.sqrt(q)
    return dict(R=R,v=arr('Vel')-perspective,perspective=perspective,ev=arr('e_Vel'),fe=arr('[Fe/H]'),efe=arr('e_[Fe/H]'),aa=aa,
        ids=[r['GaiaDR3'] for r in selected],counts={'catalogue_rows':len(rows),'photometric_likely':sum(num(r['Pmem'])>.07 for r in rows),'FLAMES_velocity_likely':sum(num(r['Pmem'])>.07 and bool(r['Vel']) for r in rows),'selected':len(selected)},
        coverage={'R_pc_percentiles':np.percentile(R,[0,10,50,90,100]).tolist(),'elliptical_deg_percentiles':np.percentile(np.rad2deg(angular),[0,10,50,90,100]).tolist(),
                  'spectra_at_R_gt_1500pc':int(np.sum(R>1500))},cat=cat)

def projection(R,a,gfun,beta=0.,rt=None,nr=4096,nz=128):
    """Solve Jeans pressure, project along z; no truncation of observed aperture."""
    rr=np.geomspace(.001,1e6,nr);lr=np.log(rr)
    nu=(1+(rr/a)**2)**(-2.5)
    if rt:nu*=np.exp(-(rr/rt)**4)
    integrand=nu*gfun(rr)*rr**(2*beta)
    # Reverse cumulative integral avoids subtracting two nearly equal totals.
    integ=-cumulative_trapezoid(integrand[::-1],rr[::-1],initial=0)[::-1]
    pressure=rr**(-2*beta)*integ
    x,w=leggauss(nz);theta=(x+1)*math.pi/4;w=w*math.pi/4
    z=a*np.tan(theta);jac=a/np.cos(theta)**2
    rad=np.sqrt(R[:,None]**2+z[None,:]**2)
    pp=np.interp(np.log(rad),lr,pressure)
    nn=(1+(rad/a)**2)**(-2.5)
    if rt:nn*=np.exp(-(rad/rt)**4)
    numerator=np.sum(w*jac*(1-beta*R[:,None]**2/rad**2)*pp,axis=1)
    denominator=np.sum(w*jac*nn,axis=1)
    return numerator/np.maximum(denominator,1e-300)

def fit(d,base,kernel,mask=None,fixed_mass=None,contamination=0.,fit_scale=False):
    mask=np.ones(len(d['R']),dtype=bool) if mask is None else mask
    R=d['R'][mask];v=d['v'][mask];ev=d['ev'][mask];fe=d['fe'][mask];efe=d['efe'][mask]
    # Conditioning on observed radius and metallicity; no inverse-completeness weighting.
    phot=np.array([-math.log(math.pi*a*a)-2*np.log1p((R/a)**2) for a in d['aa']]).T
    if 'phot' in d:phot=d['phot'][mask]
    met=np.array([-.5*np.log(2*math.pi*(efe**2+s*s))-.5*(fe-m)**2/(efe**2+s*s) for m,s in [(-2.09,.30),(-2.81,.13)]]).T
    def objective(x):
        # mass unit 1e8 Msun; x[0] log mass, x[1] systemic, x[2] logit population fraction
        mass=np.exp(x[0]) if fixed_mass is None else fixed_mass/1e8;f=1/(1+np.exp(-x[2]))
        logprior=phot+met+np.log([f,1-f]);logprior-=logsumexp(logprior,axis=1)[:,None]
        kk=kernel(x[3]) if fit_scale else kernel
        var=base[mask]+mass*kk[mask]+ev[:,None]**2
        logvel=-.5*(np.log(2*math.pi*var)+(v[:,None]-x[1])**2/var)
        norm=ndtr((260-d['perspective'][mask,None]-x[1])/np.sqrt(var))-ndtr((180-d['perspective'][mask,None]-x[1])/np.sqrt(var))
        logvel-=np.log(np.maximum(norm,1e-30))
        ll=logsumexp(logprior+logvel,axis=1)
        if contamination:ll=np.logaddexp(np.log1p(-contamination)+ll,math.log(contamination/80))
        return -float(np.sum(ll))
    bounds=[(-9,14),(210,240),(-4,4)]+([(math.log(30),math.log(30000))] if fit_scale else [])
    starts=[([lm,227.,.5]+([math.log(b)] if fit_scale else [])) for lm in [-1.,3.] for b in ([600,1800,5000] if fit_scale else [1])]
    sols=[minimize(objective,x,method='L-BFGS-B',bounds=bounds) for x in starts]
    s=min(sols,key=lambda z:z.fun)
    return dict(nll=float(s.fun),cold_mass=float(np.exp(s.x[0])*1e8) if fixed_mass is None else fixed_mass,mean_velocity=float(s.x[1]),
        **({'cold_scale_pc':float(np.exp(s.x[3]))} if fit_scale else {}),
        population_fraction=float(1/(1+np.exp(-s.x[2]))),optimizer_success=bool(s.success),optimizer_message=str(s.message),n=int(np.sum(mask)))

def main():
    start=time.time();pins=hashes();d=load(); R=d['R']; aa=d['aa'];Mstar=5e5
    checks={};a=500.;mass=1e7;testR=np.array([0.,100.,500.,1500.])
    got=projection(testR,a,lambda r:G*mass*r/(r*r+a*a)**1.5)
    exact=3*math.pi*G*mass/(64*a)/np.sqrt(1+(testR/a)**2)
    checks['matched_Plummer_projection_relative_error']=float(np.max(abs(got/exact-1)))
    assert checks['matched_Plummer_projection_relative_error']<2e-4
    results=[];profiles=[];robust=[];continuous=[];bgrid=np.geomspace(30,30000,121)
    for foot,a0 in A0.items():
      for beta,rt in [(0.,None),(-.5,None),(0.,3000.)]:
        dd=dict(d)
        if rt:
            xx,ww=leggauss(128);tt=(xx+1)*math.pi/4;ww*=math.pi/4
            logs=[]
            for a in aa:
                z=a*np.tan(tt);rad=np.sqrt(R[:,None]**2+z*z)
                nn=(1+(rad/a)**2)**(-2.5)*np.exp(-(rad/rt)**4)
                normr=np.geomspace(.001,1e5,4096)
                norm=np.trapz(4*math.pi*normr**2*(1+(normr/a)**2)**(-2.5)*np.exp(-(normr/rt)**4),normr)
                logs.append(np.log(2*np.sum(ww*a/np.cos(tt)**2*nn,axis=1)/norm))
            dd['phot']=np.array(logs).T
        def gb(r):
            gn=sum(G*Mstar*.5*r/(r*r+a*a)**1.5 for a in aa)
            return .5*(gn+np.sqrt(gn*gn+4*a0*gn))
        base=np.array([projection(R,a,gb,beta,rt) for a in aa]).T
        kernels=[]
        for b in bgrid:
            kernel=np.array([projection(R,a,lambda r:G*1e8*r/(r*r+b*b)**1.5,beta,rt) for a in aa]).T
            kernels.append(kernel)
            f=fit(dd,base,kernel)
            results.append(dict(footing=foot,beta=beta,tracer_taper_pc=rt,cold_scale_pc=float(b),**f))
        logkern=np.log(np.array(kernels));lb=np.log(bgrid)
        def interp_kernel(logb):
            ix=min(len(lb)-2,max(0,int(np.searchsorted(lb,logb)-1)))
            f=(logb-lb[ix])/(lb[ix+1]-lb[ix])
            return np.exp((1-f)*logkern[ix]+f*logkern[ix+1])
        best=fit(dd,base,interp_kernel,fit_scale=True)
        continuous.append(dict(footing=foot,beta=beta,tracer_taper_pc=rt,**best))
        direct=np.array([projection(R,a,lambda r:G*1e8*r/(r*r+best['cold_scale_pc']**2)**1.5,beta,rt) for a in aa]).T
        checks[f'{foot}_{beta}_{rt}_kernel_interpolation_error']=float(np.max(abs(interp_kernel(math.log(best['cold_scale_pc']))/direct-1)))
        assert checks[f'{foot}_{beta}_{rt}_kernel_interpolation_error']<.001
        if beta==0 and rt is None:
            for label,mask,contam in [('inner_R_lt_1500pc',R<1500,0.),('contamination_5percent',None,.05)]:
                robust.append(dict(footing=foot,label=label,**fit(dd,base,interp_kernel,mask,contamination=contam,fit_scale=True)))
        if foot=='canonical' and rt is None:
            for mass in [2.5e7,5e7,1e8,2e8,4e8,8e8]:
                profiles.append(dict(beta=beta,fixed_mass=mass,**fit(dd,base,interp_kernel,fixed_mass=mass,fit_scale=True)))
    # Actual coverage sensitivities, not published sigma-corner fits.
    sensitivities=[]
    for foot in A0:
        lane=[r for r in results if r['footing']==foot and r['beta']==0 and r['tracer_taper_pc'] is None]
        best=min(lane,key=lambda r:r['nll']);b=best['cold_scale_pc'];a0=A0[foot]
        def gb(r):
            gn=sum(G*Mstar*.5*r/(r*r+a*a)**1.5 for a in aa)
            return .5*(gn+np.sqrt(gn*gn+4*a0*gn))
        base=np.array([projection(R,a,gb) for a in aa]).T
        kern=np.array([projection(R,a,lambda r:G*1e8*r/(r*r+b*b)**1.5) for a in aa]).T
        for label,mask in [('inner_R_lt_1500pc',R<1500),('exclude_velocity_variance_gt_3',np.ones(len(R),bool))]:
            if label.startswith('exclude'):continue # no unused catalogue cut masquerading as a test
            sensitivities.append(dict(footing=foot,label=label,scale_fixed_pc=b,**fit(d,base,kern,mask)))
        # Numerical convergence at winning profile.
        improved=projection(R,aa[0],lambda r:G*1e8*r/(r*r+b*b)**1.5,nr=8192,nz=256)
        checks[foot+'_projection_refinement_error']=float(np.max(abs(improved/kern[:,0]-1)))
    out=dict(scope='exploratory conditional velocity likelihood; not posterior or formation solution',
        counts=d['counts'],coverage=d['coverage'],selected_ids=d['ids'],tracer_scales_pc=aa.tolist(),
        stellar_mass=Mstar,results=results,continuous_best=continuous,robust=robust,mass_profiles=profiles,sensitivities=sensitivities,checks=checks)
    (HERE/'survey_results.json').write_text(json.dumps(out,indent=2)+'\n')
    assert pins==hashes()
    receipt=dict(status='completed',input_hashes=pins,revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        seconds=time.time()-start,peak_RSS_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        result_hash=hashlib.sha256((HERE/'survey_results.json').read_bytes()).hexdigest())
    (HERE/'survey_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(counts=d['counts'],coverage=d['coverage'],checks=checks,seconds=receipt['seconds']),indent=2))
    for foot in A0:
      for beta,rt in [(0.,None),(-.5,None),(0.,3000.)]:
        lane=[r for r in results if r['footing']==foot and r['beta']==beta and r['tracer_taper_pc']==rt]
        print('BEST',min(lane,key=lambda r:r['nll']))
if __name__=='__main__':main()
