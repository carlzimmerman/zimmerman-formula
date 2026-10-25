"""CCT-005 finite spherical moment/supply audit. See CONTRACT.md."""
import csv, hashlib, itertools, json, math, platform, resource, subprocess, time
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import brentq, linprog, minimize_scalar
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DS = ROOT / 'real_research/data/dsph'
G, PC, RC = .00430091, 3.085677581491367e16, 5.364
A0 = {'canonical': 9.3603e-11 * PC / 1e6, 'alt': 1.1312e-10 * PC / 1e6}
INPUTS = [DS/'lvd_dwarf_mw.csv', DS/'weisz2014_dl/table5.tsv',
          DS/'emiles_ml_dl/UBBVRIJHK_ku_iPp0.00.MAG',
          ROOT/'campaign_fresh_gravity/CFG827_dwarf_age_sfh_ml/cfg827_results.json',
          HERE/'CONTRACT.md', Path(__file__)]
def hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in INPUTS}
def tsv(p):
    lines = [l.rstrip('\n') for l in p.open() if not l.startswith('#') and l.strip()]
    keys = lines[0].split('\t')
    return [dict(zip(keys, map(str.strip, l.split('\t')))) for l in lines[3:] if len(l.split('\t')) == len(keys)]
def sfh_bins(r):
    keys = sorted([k for k in r if k.startswith('f') and k[1:].replace('.', '').isdigit()], key=lambda k:float(k[1:]), reverse=True)
    grid, f = np.array([float(k[1:]) for k in keys]), np.array([float(r[k]) for k in keys])
    assert np.min(np.diff(f)) >= -1e-12 and abs(f[-1]-1)<1e-12
    bins = [(13.3, float(f[0]))] if f[0]>0 else []
    bins += [(10**((grid[i-1]+grid[i])/2)/1e9,float(f[i]-f[i-1])) for i in range(1,len(f)) if f[i]>f[i-1]]
    return bins, dict(log_age_years=grid.tolist(), formed_before_fraction=f.tolist(), field=r.get('Field'), TMass_field=r.get('TMass'))
SSP = {}
for line in (DS/'emiles_ml_dl/UBBVRIJHK_ku_iPp0.00.MAG').read_text().splitlines()[1:]:
    v=line.split(); SSP.setdefault(float(v[2]), []).append([float(v[3]),float(v[4]),float(v[17])])
SSP={z:np.array(sorted(a)) for z,a in SSP.items()}
def population(bins,z,lum):
    arr=SSP[z]; m=l=0.
    for age,dm in bins:
        x=math.log10(age); y=np.log10(arr[:,0])
        surv=float(np.interp(x,y,arr[:,1])); ml=float(np.interp(x,y,arr[:,2]))
        m+=dm*surv; l+=dm*surv/ml
    assert abs(sum(dm for _,dm in bins)-1)<1e-10
    return dict(Z=z,upsilon=m/l,surviving_fraction=m,formed_mass=lum/l,stellar_mass=lum*m/l)

Q = {}
def quadrature(n):
    if n not in Q:
        x,w=leggauss(n); theta=(x+1)*math.pi/4
        Q[n]=(theta,w*math.pi/4)
    return Q[n]
def baryon_variance(a,components,a0,n=256,newton=False):
    t,w=quadrature(n); r=a*np.tan(t)
    gn=sum(G*m*r/(r*r+b*b)**1.5 for m,b in components)
    g=gn if newton else .5*(gn+np.sqrt(gn*gn+4*a0*gn))
    return float(a*np.sum(w*np.sin(t)**3*g))
def kernel(a,b,n=256):
    t,w=quadrature(n)
    I=float(np.sum(w*3*np.sin(t)**2*np.cos(t)/(1+(b/a)**2*np.tan(t)**2)**1.5))
    return G/(3*a)*I
def fit_two(aa,res):
    if min(res)<=0: return {'status':'nonpositive residual; positive-cold exact fit unavailable'}
    target=res[1]/res[0]
    def fun(logb):
        b=10**logb
        return kernel(aa[1],b)/kernel(aa[0],b)-target
    lo,hi=-3.,5.
    if fun(lo)*fun(hi)>0: return dict(status='no root in 0.001..100000 pc',ratio=target)
    b=10**brentq(fun,lo,hi,xtol=1e-11); m=res[0]/kernel(aa[0],b)
    return dict(status='moment fit only',scale_pc=b,cold_mass=m,
                cold_inside_MR=m*aa[0]**3/(aa[0]**2+b*b)**1.5,
                cold_inside_MP=m*aa[1]**3/(aa[1]**2+b*b)**1.5,
                moment_relative_residual=max(abs(m*kernel(a,b)/v-1) for a,v in zip(aa,res)))

def shell_bound(aa,res,n=401):
    """Nonnegative shell relaxation; no assumption shells dynamically survive."""
    if min(res)<=0: return {'status':'nonpositive residual'}
    ratio=res[1]/res[0]; lower=aa[0]/aa[1]; upper=(aa[1]/aa[0])**2
    if not lower<ratio<upper:
        return dict(status='ratio outside positive spherical shell range',ratio=ratio,allowed_limits=[lower,upper])
    t=(ratio/lower)**(2/3)
    support_min=math.sqrt((t-1)/(1/aa[0]**2-t/aa[1]**2))
    radii=np.r_[0.,np.geomspace(.1,1e5,n)]
    matrix=np.array([G/(3*a)*(1+(radii/a)**2)**(-1.5)*1e6 for a in aa])
    lp=linprog(np.ones(len(radii)),A_eq=matrix,b_eq=res,bounds=(0,None),method='highs')
    if not lp.success: return dict(status='finite shell LP failed',message=lp.message)
    inds=np.where(lp.x>1e-8)[0]
    # Continuum dual certificate. For every nonnegative cold distribution,
    # Mc >= (resMP-c*resMR)/max_r(KMP-c*KMR). Find max analytically,
    # including r=0 and infinity, then optimize this valid bound in c.
    def dual(c,detail=False):
        ar,ap=aa; t=(ap*ap/(c*ar*ar))**.4
        rr=(ap*ap-t*ar*ar)/(t-1) if abs(t-1)>1e-14 else -1
        points=[0.]+([math.sqrt(rr)] if rr>0 else [])
        h=lambda r:G/3*(ap*ap/(r*r+ap*ap)**1.5-c*ar*ar/(r*r+ar*ar)**1.5)
        hmax=max([0.]+[h(r) for r in points])
        value=(res[1]-c*res[0])/hmax if hmax>0 else -1e100
        return (value,hmax,points) if detail else -value
    opt=minimize_scalar(dual,bounds=(1e-8,upper*(1-1e-8)),method='bounded',options={'xatol':1e-12})
    bound,hmax,points=dual(opt.x,True)
    dense=G/3*(aa[1]**2/(radii*radii+aa[1]**2)**1.5-opt.x*aa[0]**2/(radii*radii+aa[0]**2)**1.5)
    assert max(dense)<=hmax*(1+1e-10)
    assert bound<=lp.fun*1e6*(1+1e-8)
    return dict(status='continuum dual bound plus finite grid upper witness',min_support_radius_pc=support_min,
        continuum_mass_lower_bound=bound,dual_c=float(opt.x),dual_max_kernel=hmax,dual_stationary_radii=points,
        min_mass_on_grid=float(lp.fun*1e6),active_radii_pc=radii[inds].tolist(),
        active_masses=(lp.x[inds]*1e6).tolist(),equality_relative_error=float(np.max(np.abs(matrix@lp.x/np.array(res)-1))))

def main():
    start=time.time(); before=hashes()
    lvd={r['name']:r for r in csv.DictReader((DS/'lvd_dwarf_mw.csv').open())}
    sfh={}
    for r in tsv(DS/'weisz2014_dl/table5.tsv'):
        if r['ID'] not in sfh: sfh[r['ID']]=sfh_bins(r)
    result=dict(assertion_tested='finite spherical virial constraints; not formation/heating closure',
                a0=A0,cosmic_ratio_assumed=RC, galaxies={}, sextans_two_population=[],checks={})
    fields=['M_V','M_V_em','M_V_ep','distance','distance_em','distance_ep','rhalf_sph_physical',
            'rhalf_sph_physical_em','rhalf_sph_physical_ep','rhalf_physical','ellipticity',
            'vlos_sigma','vlos_sigma_em','vlos_sigma_ep','mass_HI_ul','ref_vlos','ref_structure']
    prior=json.loads(INPUTS[3].read_text())['rows']
    for name in ['Draco','Sextans','Fornax','Leo I']:
        r=lvd[name]; lum=10**(.4*(4.83-float(r['M_V']))); a=float(r['rhalf_sph_physical']); sig=float(r['vlos_sigma'])
        if name in sfh:
            bins,raw=sfh[name]; pops=[population(bins,z,lum) for z in [-1.31,-1.71,-.71]]
            raw['bin_centres_Gyr_and_formed_fractions']=bins
            result['checks'][name+'_ML_relative_error']=abs(pops[0]['upsilon']/prior[name]['ups']-1)
        else:
            # Deliberately no invented Sextans SFH curve. Old populations only sensitivity.
            pops=[population([(age,1.)],z,lum) for age in [11.5,13.3] for z in [-2.32,-1.71,-1.31]]
            raw={'status':'absent from Weisz table5; old-burst sensitivity, not measured global SFH'}
        out=dict(observations={k:r[k] for k in fields}, luminosity_V=lum,SFH=raw,populations=pops,moments={})
        for foot,a0 in A0.items():
            mm=[]
            for p in pops:
                s2=baryon_variance(a,[(p['stellar_mass'],a)],a0)
                extra=sig*sig-s2; pointmin=max(0.,3*a*extra/G)
                mm.append(dict(upsilon=p['upsilon'],stellar_mass=p['stellar_mass'],sigma_baryon=math.sqrt(s2),
                               residual_variance=extra,point_mass_lower_bound=pointmin,
                               min_initial_baryons_at_full_cold_retention=pointmin/RC,
                               min_initial_baryons_over_formed_stars=pointmin/(RC*p['formed_mass']),
                               cold_mass_if_same_scale=max(0.,extra/kernel(a,a)),
                               crossing_time_Myr=.977792*a/sig))
            out['moments'][foot]=mm
        result['galaxies'][name]=out
    # Actual two-population numbers: Tolstoy+2025, arXiv:2504.02787v1 Table 2.
    datum=dict(source='https://arxiv.org/html/2504.02787v1', table=2,
        radii_deg=[.339,.62],radii_errors_deg=[.021,.05],sigma_kms=[7.,10.5],
        sigma_low=[6.6,9.8],sigma_high=[7.4,11.3],number_fractions=[.63,.37],
        warning='number fractions are not stellar mass fractions; no joint covariance/selection likelihood')
    result['sextans_data']=datum
    sr=lvd['Sextans']; distance=float(sr['distance'])*1000
    for circularize,foot,p,fM in itertools.product([False,True],A0,result['galaxies']['Sextans']['populations'],[.1,.3,.5,.7,.9]):
        aa=np.tan(np.deg2rad(datum['radii_deg']))*distance
        if circularize: aa*=math.sqrt(1-float(sr['ellipticity']))
        comps=[(p['stellar_mass']*fM,aa[0]),(p['stellar_mass']*(1-fM),aa[1])]
        base=[baryon_variance(a,comps,A0[foot]) for a in aa]
        fits=[]
        # Central plus all independent sigma corners: sensitivities, not confidence regions.
        sigpairs=[datum['sigma_kms']]+list(itertools.product(*zip(datum['sigma_low'],datum['sigma_high'])))
        for pair in sigpairs:
            residual=[s*s-b for s,b in zip(pair,base)]
            fit=fit_two(aa,residual)
            fit['shell_relaxation']=shell_bound(aa,residual)
            fit.update(sigma_pair=list(pair),point_mass_lower_bounds=[max(0.,3*a*v/G) for a,v in zip(aa,residual)])
            if 'cold_mass' in fit:
                fit['min_initial_baryons_over_formed_stars']=fit['cold_mass']/(RC*p['formed_mass'])
            fits.append(fit)
        result['sextans_two_population'].append(dict(circularized=circularize,footing=foot,
            upsilon=p['upsilon'],formed_mass=p['formed_mass'],mass_fraction_MR=fM,
            tracer_scales_pc=aa.tolist(),baryon_sigma=np.sqrt(base).tolist(),fits=fits))
    a,m=485.89,1e6
    newt=baryon_variance(a,[(m,a)],A0['canonical'],newton=True)
    result['checks']['Newtonian_Plummer_relative_error']=abs(newt/(math.pi*G*m/(32*a))-1)
    result['checks']['quadrature_relative_error']=abs(baryon_variance(a,[(m,a)],A0['canonical'],512)/baryon_variance(a,[(m,a)],A0['canonical'],256)-1)
    fits=[f for row in result['sextans_two_population'] for f in row['fits'] if 'cold_mass' in f]
    result['checks']['max_fit_moment_relative_error']=max(f['moment_relative_residual'] for f in fits)
    result['checks']['max_kernel_order_relative_error']=max(abs(kernel(a,f['scale_pc'],512)/kernel(a,f['scale_pc'],256)-1) for row in result['sextans_two_population'] for f in row['fits'] if 'cold_mass' in f for a in row['tracer_scales_pc'])
    # Double shell grid for one central example; grid-only convergence is not a continuum proof.
    example=result['sextans_two_population'][0]
    res=[s*s-b*b for s,b in zip([7.,10.5],example['baryon_sigma'])]
    fine=shell_bound(example['tracer_scales_pc'],res,801)
    result['shell_grid_check']=dict(coarse=example['fits'][0]['shell_relaxation'],fine=fine)
    result['counts']=dict(rows=len(result['sextans_two_population']),tested_fits=5*len(result['sextans_two_population']),finite_fits=len(fits))
    # Explicitly conditional common-size/common-capture null, not a consequence
    # of a universal field action. This asks whether SFH normalization alone suffices.
    shared=[]
    for row in result['sextans_two_population']:
        fit=row['fits'][0]
        if 'cold_mass' not in fit: continue
        ratio=fit['cold_mass']/row['formed_mass']; b=fit['scale_pc']
        pred={}
        for name in ['Draco','Fornax','Leo I']:
            gal=result['galaxies'][name]; ac=float(gal['observations']['rhalf_sph_physical'])
            pred[name]=[math.sqrt(baryon_variance(ac,[(p['stellar_mass'],ac)],A0[row['footing']])+ratio*p['formed_mass']*kernel(ac,b)) for p in gal['populations']]
        shared.append(dict(footing=row['footing'],cold_scale_pc=b,cold_per_formed_mass=ratio,predicted_sigma=pred))
    result['same_size_same_capture_null']=shared
    # Orthogonal direct radial quadrature checks cold kernel and force virial.
    from scipy.integrate import quad
    direct=quad(lambda r: G*m*r*r/(r*r+a*a)**1.5 * 3*r*r/a**3*(1+(r/a)**2)**(-2.5)/3,0,np.inf,epsabs=1e-9)[0]
    result['checks']['direct_radial_Newtonian_relative_error']=abs(direct/newt-1)
    assert max(result['checks'].values())<1e-7
    after=hashes(); assert before==after
    (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    receipt=dict(input_hashes_before=before,input_hashes_after=after,
        revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
        elapsed_seconds=time.time()-start,peak_rss_native_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        rss_units='bytes on macOS',status='completed finite calculation; physical formation unestablished',
        result_sha256=hashlib.sha256((HERE/'results.json').read_bytes()).hexdigest())
    (HERE/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(dict(counts=result['counts'],checks=result['checks'],seconds=receipt['elapsed_seconds']),indent=2))
if __name__=='__main__': main()
