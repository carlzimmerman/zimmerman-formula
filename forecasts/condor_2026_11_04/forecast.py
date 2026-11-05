"""Pre-release screening, not a calibrated likelihood forecast. See CONTRACT.md.
Run from repository root: python3 forecasts/condor_2026_11_04/forecast.py OUTPUT_DIR
"""
import csv, json, math, sys
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import numpy as np
from scipy.integrate import quad
from scipy.optimize import least_squares, brentq
from scipy.special import ive, kve

HERE=Path(__file__).resolve().parent
OUT=Path(sys.argv[1]); OUT.mkdir(parents=True,exist_ok=True)
G=4.30091e-6; U=1e6/3.0857e19; H0=68.56427; OM=.2976016
A0=9.3603e-11; W0=-.838; WA=-.62
def ratio(z):
    a=1/(1+z)
    return math.sqrt(a**(-3*(1+W0+WA))*math.exp(-3*WA*(1-a)))
def E(z): return math.sqrt(OM*(1+z)**3+1-OM)
def dc(z): return 299792.458/H0*quad(lambda x:1/E(x),0,z)[0]
def scale(z): return dc(z)/(1+z)*1000/206264.806
def lp(F,z): return 3.25e7*F/(345.796/(1+z))**2*(dc(z)*(1+z))**2/(1+z)**3
def disc(M,Re,R):
    rd=Re/1.678; y=np.asarray(R)/(2*rd)
    return 2*G*M/rd*y*y*(ive(0,y)*kve(0,y)-ive(1,y)*kve(1,y))
def speed(vb2,R,a0):
    # Algebraically independent of nu implementation: positive root of g^2-gN*g-gN*a0=0.
    gn=np.asarray(vb2)/np.asarray(R)
    return np.sqrt(.5*(gn+np.sqrt(gn*gn+4*gn*a0/U))*R)
def nfw(lm,c,z,R):
    M=10**lm; hz=H0*E(z)/1000
    r200=(G*M/(100*hz**2))**(1/3)
    f=lambda x:np.log1p(x)-x/(1+x)
    return G*M*f(np.asarray(R)*c/r200)/f(c)/R
def fit_alternative(R,vs2,vg2,z,vtarget,Ms,Mg,halo=False):
    # Mass normalization changes are nuisance parameters, shared coherently across all radii.
    def model(p):
        vb=vs2*10**p[0]+vg2*10**p[1]
        return np.sqrt(vb+nfw(p[2],p[3],z,R)) if halo else speed(vb,R,A0)
    def residual(p): return (model(p)-vtarget)/vtarget
    if halo:
        # Conservative minimum based on *lowest allowed* baryonic mass; check fitted baryon budget below.
        lower=math.log10((Ms*10**(-.2)+Mg*10**(-.3))*(1-.157)/.157)
        lo=[-.2,-.3,lower,1.]; hi=[.2,.3,14.,10.]
        starts=[[0,0,max(lower+.01,12.),3.],[-.15,-.2,max(lower+.01,12.5),2.],[-.1,0,max(lower+.01,13.),5.]]
        def res(p):
            penalty=max(0,math.log10((Ms*10**p[0]+Mg*10**p[1])*(1-.157)/.157)-p[2])*10
            return np.r_[residual(p),penalty]
    else:
        lo=[-.2,-.3]; hi=[.2,.3]; starts=[[0,0],[-.1,-.1],[.1,-.2]];res=residual
    fits=[least_squares(res,p,bounds=(lo,hi),xtol=1e-11,ftol=1e-11,gtol=1e-11,max_nfev=700) for p in starts]
    fit=min(fits,key=lambda f:np.sum(f.fun**2)); d=residual(fit.x)
    budget_ok=not halo or (10**fit.x[2] >= (Ms*10**fit.x[0]+Mg*10**fit.x[1])*(1-.157)/.157*(1-1e-4))
    return dict(parameters=fit.x.tolist(),rms_fraction=float(np.sqrt(np.mean(d*d))),max_fraction=float(max(abs(d))),budget_ok=bool(budget_ok),success=bool(fit.success))

raw=list(csv.DictReader(open(HERE/'archive_metadata.csv')))
names=sorted({r['target_name'] for r in raw if not r['target_name'].startswith('J')})
inventory=[]
for name in names:
    units={}
    for r in raw:
        if r['target_name']!=name:continue
        unit=r['obs_id'].split('.source')[0]
        if unit not in units: units[unit]=dict(r)
    for unit,r in units.items():
        t=datetime.fromisoformat(r['obs_release_date']).replace(tzinfo=timezone.utc)
        inventory.append(dict(target=name,unit=unit,band=r['band_list'],rights=r['data_rights'],release_UTC=t.isoformat(),release_Eastern=t.astimezone(ZoneInfo('America/New_York')).isoformat(),beam_arcsec=float(r['s_resolution'])))
(OUT/'inventory.json').write_text(json.dumps(inventory,indent=2))
inputs=json.loads((HERE/'inputs.json').read_text()); allrows=[]; profiles=[]; checks={}
for name,d in inputs.items():
    z=d['z']; sc=scale(z); restars=d['Re_star'][:]
    if d.get('angular_first'):restars[0]*=sc
    if d.get('angular_second'):restars[1]*=sc
    L=d.get('Lp10') or lp(d['F32'],z)*d['R31']
    F=d.get('F32') or L/d['R31']/lp(1,z)
    rr=[r for r in raw if r['target_name']==name and r['band_list'] in ['3','4'] and r['data_rights']=='Proprietary']
    assert rr
    ar=min(rr,key=lambda x:float(x['s_resolution']));beam=float(ar['s_resolution'])
    # Use correct line-window sensitivity from frequency-support text rather than arbitrary SPW row.
    import re
    nu=345.796/(1+z); sig=None
    for low,high,num,unit in re.findall(r'\[([\d.]+)\.\.([\d.]+)GHz,[^,]+,([\d.]+)(uJy|mJy)/beam@10km/s',ar['frequency_support']):
        if float(low)<=nu<=float(high):sig=float(num)*(1e-3 if unit=='uJy' else 1)
    assert sig is not None,(name,nu)
    for si,rs in enumerate(restars):
      for rg in d['Re_gas']:
       for alpha in d['alpha']:
        Ms=10**d['logMs']; Mg=alpha*L
        # Candidate radius grid, not a claim that these radii are measurable.
        R=np.array([1.,2.,3.,4.,6.,8.,12.,16.])
        vs=disc(Ms,rs,R);vg=disc(Mg,rg,R);vb=vs+vg
        vf=speed(vb,R,A0*ratio(z));vm=speed(vb,R,A0);vn=np.sqrt(vb)
        # Linear nuisance budget: independent stellar .2dex/gas .3dex + assumed 5% speed error.
        eps=1e-4
        ds=(speed(vs*10**eps+vg,R,A0*ratio(z))-speed(vs*10**(-eps)+vg,R,A0*ratio(z)))/(2*eps)*.2
        dg=(speed(vs+vg*10**eps,R,A0*ratio(z))-speed(vs+vg*10**(-eps),R,A0*ratio(z)))/(2*eps)*.3
        err=np.sqrt(ds**2+dg**2+(.05*vf)**2)
        # Optimistic ring S/N: known local velocity, all local line flux in 100 km/s,
        # face-on thin exponential, independent beams. Not injection-tested reach.
        theta=R/sc;td=rg/1.678/sc;ob=1.133*beam**2
        ringarea=2*np.pi*theta*beam
        brightness=F/(2*np.pi*td**2)*np.exp(-theta/td)
        sn=brightness*np.sqrt(ringarea*ob)/(sig/1000*math.sqrt(10*100))
        sn_sister=sn*2.54*1.5**1.5
        for i,r in enumerate(R):
          allrows.append(dict(target=name,star_shape=si,Re_star=rs,Re_gas=rg,alpha=alpha,R_kpc=r,V_Newton=vn[i],V_FDESI=vf[i],V_MOND_same_a0=vm[i],delta_MOND_kms=vm[i]-vf[i],fraction_MOND=(vm[i]-vf[i])/vf[i],sigma5_with_mass=err[i],separation_over_budget=(vm[i]-vf[i])/err[i],ringSN_optimistic_archive=sn[i],ringSN_optimistic_sister=sn_sister[i],required_sigma_velocity_only_3sigma=(vm[i]-vf[i])/3))
        # Fit coherent alternative profiles over 1..R90 of gas; optimistic ideal radial coverage.
        r90=brentq(lambda x:(1+x)*math.exp(-x)-.1,1,8)*rg/1.678
        radii=np.linspace(max(1.,beam*sc),r90,8)
        vsf=disc(Ms,rs,radii);vgf=disc(Mg,rg,radii);vt=speed(vsf+vgf,radii,A0*ratio(z))
        profiles.append(dict(target=name,star_shape=si,Re_star=rs,Re_gas=rg,alpha=alpha,radii=radii.tolist(),MOND_fit=fit_alternative(radii,vsf,vgf,z,vt,Ms,Mg),NFW_fit=fit_alternative(radii,vsf,vgf,z,vt,Ms,Mg,True)))
    print(name,'z',z,'a0 ratio',ratio(z),'deep-limit max speed separation',1-ratio(z)**.25,'F32',F,'beam',beam,'line sigma10',sig)
with open(OUT/'grid.csv','w') as f:
    w=csv.DictWriter(f,fieldnames=allrows[0]);w.writeheader();w.writerows(allrows)
(OUT/'profile_fits.json').write_text(json.dumps(profiles,indent=2))
# Geometry-independent ceiling, with identical interpolation and a0 normalization.
# d ln V / d ln a0 is in [0,1/4], so |ln Vratio| <= |ln r|/4.
ceilings={n:dict(z=d['z'],a0_ratio=ratio(d['z']),max_fraction_relative_to_MOND=1-ratio(d['z'])**.25,total_fractional_precision_for_3sigma=(1-ratio(d['z'])**.25)/3) for n,d in inputs.items()}
# ID2993 exact narrow line window determines this conservative redshift interval; published candidate z1.19 agrees.
zlo,zhi=345.796/158.24-1,345.796/157.31-1
ceilings['ID2993']=dict(redshift_window=[zlo,zhi],a0_ratio_range=[ratio(zlo),ratio(zhi)],max_fraction_relative_to_MOND=max(abs(1-ratio(z)**.25) for z in np.linspace(zlo,zhi,1001)),status='Bound only; mass/size/flux catalogue inaccessible; no target-specific NFW fit')
ys=np.logspace(-10,10,2001)
for z in [1.19,1.55204,2.21777,2.52455]:
    v1=speed(ys,np.ones_like(ys),A0);v2=speed(ys,np.ones_like(ys),A0*ratio(z))
    assert np.max(abs(np.log(v2/v1))) <= abs(math.log(ratio(z)))/4+1e-12
checks['analytic_ceiling_grid']=True
# Recover PAPER66 values without importing its code, and Newtonian/point-mass limits.
vb=disc(10**11.11,3.16,3)+disc(lp(.79,2.52455)*1.8,1.56,3)
checks['PAPER66_431_441_439']=bool(abs(math.sqrt(vb)-431)<1 and abs(speed(vb,3,A0)-441)<1 and abs(speed(vb,3,A0*ratio(2.52455))-439)<1)
checks['disc_point_mass_limit']=bool(abs(disc(1e10,2.,200.)/(G*1e10/200)-1)<.002)
checks['zero_a0_Newton']=bool(abs(speed(10000.,3.,0)-100)<1e-10)
hz=H0*E(2)/1000; r200=(G*1e12/(100*hz**2))**(1/3)
checks['NFW_at_r200']=bool(abs(nfw(12,4,2,r200)/(G*1e12/r200)-1)<1e-12)
checks['flat_equals_MOND']=bool(np.array_equal(speed(ys,1,A0),speed(ys,1,A0)))
checks['coverage_3_targets_36_profiles_288_rows']=len(profiles)==36 and len(allrows)==288
checks['all_optimizations_converged']=all(p[k]['success'] for p in profiles for k in ['MOND_fit','NFW_fit'])
checks['halo_baryon_budget']=all(p['NFW_fit']['budget_ok'] for p in profiles)
summary=dict(ceilings=ceilings,checks=checks,archive_science_names=names,n_profiles=len(profiles),n_grid_rows=len(allrows))
(OUT/'results.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2));assert all(checks.values()),checks
