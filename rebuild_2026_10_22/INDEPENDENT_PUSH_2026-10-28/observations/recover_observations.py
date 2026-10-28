#!/usr/bin/env python3
"""Offline, bounded diagnostics. No theory grade; see FROZEN_CRITERIA/AMENDMENTS."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys, csv, json, math, hashlib, io, contextlib, time, resource, re, platform, datetime, subprocess
from pathlib import Path
from html.parser import HTMLParser
import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid, simpson

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MUTATE = '--mutate' in sys.argv
TAG = '_MUTATE' if MUTATE else ''
DECLARED_RESULTS = [HERE/f'observations_results{TAG}.json']
START = time.time()
STARTED_AT = datetime.datetime.now(datetime.timezone.utc).isoformat()
COMMIT = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
G, MSUN, KPC, KEV, MP = 6.67430e-11, 1.98847e30, 3.0856775814913673e19, 1.602176634e-16, 1.67262192369e-27
MU = 0.62                         # Babyk 2018 section 4.2, not a fit
FEET = {'canonical':9.3603e-11,'alt':1.1312e-10}
OUT, CHECKS = [], {}
def say(s):
    print(s, flush=True); OUT.append(s)
def check(name, value, details):
    CHECKS[name] = bool(value)
    say(f'{name} {"PASS" if value else "FAIL"} {details}')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
INPUTS = [HERE/'sluggs_xray_inputs.csv', HERE/'ic1613_inputs.json', HERE/'clogs_highrichness_inputs.csv',
          HERE/'cga_Table5.html', HERE/'cga_Table6.html', ROOT/'real_research/data/kt2017_galaxies.tsv',
          ROOT/'real_research/data/kt2017_groups.tsv',
          ROOT/'rebuild_2026_10_22/RT1_lt_rotation_regrade/rt1_lt_rotation_regrade_results.json']
INPUTS += list((ROOT/'campaign_fresh_gravity/CFG528_sluggs_centrals_mechanism').glob('*.py'))
INPUTS += [Path(__file__).resolve()]
BEFORE = {str(p.relative_to(ROOT)):sha(p) for p in INPUTS}
AUDIT = {'active':True,'inside':False}
def audit_reads(event,args):
    if event!='open' or not AUDIT['active'] or AUDIT['inside']:return
    p,mode,flags=args
    if not isinstance(p,(str,bytes)):return
    path=Path(os.fsdecode(p)).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():return
    if mode is not None and any(c in mode for c in 'wax+'):return
    AUDIT['inside']=True
    try:BEFORE.setdefault(str(path.relative_to(ROOT)),sha(path))
    finally:AUDIT['inside']=False
sys.addaudithook(audit_reads)

# Input profiles only, from the established primary GC/tracer machinery; do not run its grade.
srcpath = ROOT/'campaign_fresh_gravity/CFG528_sluggs_centrals_mechanism/cfg528b_measured_tracers.py'
src = srcpath.read_text()
ns = {'__file__':str(srcpath),'__name__':'observations_readonly'}
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(src[:src.index('P("=" * 124)')],str(srcpath),'exec'),ns)
radius, logr = ns['RG'], ns['LR']
u = np.linspace(0.,14.,8001)
ch = np.cosh(u)

def jeans(R, force, populations):
    """Independent integrating-factor spherical Jeans + direct Abel projection.

    Tracer density and beta arrays are inherited measured-input functions;
    acceleration is newly supplied by X-ray data. scipy Simpson projection,
    independently formed reverse cumulative integral, no GC fit.
    """
    numerator = np.zeros(len(R)); denominator = np.zeros(len(R))
    for rho,beta in populations:
        factor = np.exp(cumulative_trapezoid(2*beta,logr,initial=0.))
        integrand = rho*factor*force*radius*KPC
        integral = -cumulative_trapezoid(integrand[::-1],logr[::-1],initial=0.)[::-1]
        pressure = integral/factor
        for j,rp in enumerate(R):
            r = rp*ch; lr = np.log(r)
            b = np.interp(lr,logr,beta)
            dens = np.exp(np.interp(lr,logr,np.log(np.maximum(rho,1e-300))))
            pres = np.exp(np.interp(lr,logr,np.log(np.maximum(pressure,1e-300))))
            numerator[j] += simpson((1-b/ch**2)*pres*r,x=u)
            denominator[j] += simpson(dens*r,x=u)
    return np.sqrt(numerator/denominator)/1000

vtest=250e3
stest=jeans(np.array([5.,10.,20.]),vtest**2/(radius*KPC),[(radius**-3,np.zeros_like(radius))])
target=vtest/math.sqrt(3)/1000*(1.1 if MUTATE else 1.)
check('K1_analytic_isothermal',np.max(np.abs(stest/target-1))<3e-5,
      f'max relative {np.max(np.abs(stest/target-1)):.3g}; threshold3e-5')
old = json.loads((ROOT/'campaign_fresh_gravity/CFG528_sluggs_centrals_mechanism/cfg528b_measured_tracers_results.json').read_text())
maxdiff=0.
for footing in FEET:
    for n in ns['CEN']:
        b=ns['B'][n]
        sig=jeans(b['Rb'],ns['field'](n,ns['A0'][footing],'K0'),ns['measured_pops'](n))
        offset=float(np.mean(np.log10(b['Sb'][b['outer']]/sig[b['outer']])))
        maxdiff=max(maxdiff,abs(offset-old['rows']['M K0'][footing]['per'][f'NGC{n}']))
check('K0_existing_GC_baseline',maxdiff<1e-4,f'max abs offset difference {maxdiff:.4g} dex; threshold1e-4')

res={'contract':'finite conditional diagnostic, not a regrade of GT1/HO2/RT1',
     'mutate':MUTATE,'constants':dict(G=G,MSUN=MSUN,KPC=KPC,KEV=KEV,MP=MP,mu=MU),
     'sluggs':{},'ic1613':{},'groups':{}}
for x in csv.DictReader((HERE/'sluggs_xray_inputs.csv').open()):
    n=int(x['ngc']); b=ns['B'][n]; pops=ns['measured_pops'](n)
    temp,beta,rc,ap,da=[float(x[k]) for k in ('kT_keV','beta','rc_kpc','aperture_kpc','DA_Mpc')]
    d=ns['GAL'][n]['D']; scale=d/da; ap*=scale; rc*=scale
    q=temp*KEV/(MU*MP)
    # Hydrostatic *total* acceleration; do not add stars again.
    force=3*beta*q*radius/(radius**2+rc**2)/KPC
    sig=jeans(b['Rb'],force,pops)
    sigcut=jeans(b['Rb'],force*(radius<=ap),pops)
    outer=b['outer']; rb=b['Rb'][outer]
    offsets=np.log10(b['Sb'][outer]/sig[outer])
    tail=1-(sigcut[outer]/sig[outer])**2
    # Profile-equation unit check uses the independently tabulated total mass.
    native_ap=float(x['aperture_kpc']); native_rc=float(x['rc_kpc'])
    mass=3*beta*q*(native_ap*KPC)**3/(G*((native_ap*KPC)**2+(native_rc*KPC)**2))/MSUN
    eT=float(x['kT_error_keV']); eb=float(x['beta_error'])
    r=dict(kT_keV=temp,kT_statistical_error_keV=eT,beta=beta,rc_kpc_at_sluggs_distance=rc,
           spectral_aperture_kpc_at_sluggs_distance=ap,source_DA_Mpc=da,sluggs_D_Mpc=d,
           gc_radii_kpc=rb.tolist(),gc_sigma_km_s=b['Sb'][outer].tolist(),
           predicted_sigma_km_s=sig[outer].tolist(),offset_log10_sigma=float(np.mean(offsets)),
           offsets_per_bin=offsets.tolist(),variance_force_fraction_beyond_aperture=tail.tolist(),
           projected_bins_within_aperture=int((rb<=ap).sum()),n_outer_bins=len(rb),
           asymptotic_vcirc_km_s=math.sqrt(3*beta*q)/1e3,
           asymptotic_vcirc_GT_beta_2over3_mu_06_km_s=math.sqrt(2*temp*KEV/(0.6*MP))/1e3,
           estimated_independent_stat_error_log10_sigma=math.hypot(eT/temp,eb/beta)/(2*math.log(10)),
           mass_at_native_aperture_Msun=mass,
           warnings=['Isothermal global kT and single beta model; conditional exterior continuation',
                     'Gas force is total force; adding stellar gravity would double-count',
                     'Correlated spectral and beta fit systematics absent; no significance assigned'])
    res['sluggs'][str(n)]=r
    say(f'NGC{n}: kT={temp:.3f} keV beta={beta:.2f}; Xray spectral aperture={ap:.1f} kpc; GC R={rb.round(1)}; '
        f'mean log(sigmaGC/sigmaX)={r["offset_log10_sigma"]:+.3f}; within aperture {r["projected_bins_within_aperture"]}/{len(rb)}')
    say('  variance-force fraction beyond spectral aperture '+str(np.round(tail,3).tolist()))
check('K2_four_unique_measured_temperatures',set(res['sluggs'])=={'4486','4365','4374','5846'},'four target IDs; all spectral kT, not virial estimates')

class TextParser(HTMLParser):
    def __init__(self):super().__init__();self.words=[]
    def handle_data(self,text):self.words.extend(text.split())
p=TextParser();p.feed((HERE/'cga_Table5.html').read_text(encoding='utf-16'))
for n in (4374,5846):
    j=p.words.index(f'N{n}'); vals=p.words[j:j+18]
    source_d=float(vals[2]); rmax=float(vals[5]); txm=float(vals[16]); etxm=float(vals[17])
    scaled=rmax*res['sluggs'][str(n)]['sluggs_D_Mpc']/source_d
    res['sluggs'][str(n)]['CGA2019_aperture_check']=dict(source_D_Mpc=source_d,measured_Rmax_kpc=rmax,
        measured_Rmax_kpc_at_sluggs_distance=scaled,emission_weighted_kT_to_Rmax_keV=txm,
        rounded_kT_error_keV=etxm,source='CGA2019 Table5 live public table retrieved 2026-10-28',
        note='Rmax is reliable measured gas coverage, not a promise of spherical HSE. Rounded zero errors are not zero uncertainty.')

ic=json.loads((HERE/'ic1613_inputs.json').read_text())
rt=json.loads((ROOT/'rebuild_2026_10_22/RT1_lt_rotation_regrade/rt1_lt_rotation_regrade_results.json').read_text())
i0=ic['original_HI_inclination_deg']; theta0=math.radians(i0)
for f in FEET:
    r=rt['lg'][f]['IC 1613']['MSED']; e0=r['E']; v0=r['V']
    corrected={}
    for angle in (21.,23.,32.,36.,37.,43.,48.):
        shift=2*math.log10(math.sin(theta0)/math.sin(math.radians(angle)))
        corrected[str(angle)]=dict(V_conditional_km_s=v0*10**(shift/2),E_conditional=e0+shift)
    ineed=math.degrees(math.asin(math.sin(theta0)*10**(e0/2)))
    # First-order propagation is descriptive; this is not the full angular posterior.
    i=math.radians(ic['inclination_general_deg']); ei=math.radians(ic['inclination_general_sigma_deg'])
    se_i=2*abs(math.cos(i)/math.sin(i))/math.log(10)*ei
    ec=corrected['32.0']['E_conditional']
    res['ic1613'][f]=dict(original=r,conditional_angles=corrected,inclination_for_zero_residual_deg=ineed,
                         inclination_only_first_order_sigma_E=se_i,
                         illustrative_Z_after_inclination_error=ec/math.hypot(se_i,r['sE']),
                         warning='Optimistic entire-speed scaling only: Oh2015 Table2 V is asymmetric-drift corrected. For fixed positive V_AD², Vnew²=(Vold²−V_AD²)f²+V_AD² <= Vold²f² when lowering inclination. Thus i32 E is a maximal correction; the zero-residual inclination is an upper bound in this fixed-pressure case. R and baryons held fixed; no gas refit, new likelihood or grade.')
    say(f'IC1613 {f}: angle zero-residual={ineed:.2f}deg; E(i32)={ec:+.3f}; angle-only delta-method sigmaE={se_i:.3f}; conditional V={corrected["32.0"]["V_conditional_km_s"]:.2f}km/s')
mass_ratio=ic['Mdyn_half_light_Msun']/ic['M_Wolf_same_radius_Msun']
res['ic1613']['new_dynamical_mass_to_Wolf_same_radius_ratio']=mass_ratio
check('K3_inclination_identity',all(abs(res['ic1613'][f]['conditional_angles']['48.0']['E_conditional']-rt['lg'][f]['IC 1613']['MSED']['E'])<1e-14 for f in FEET),'i48 recovers RT1 exactly')

# Exact positional association to existing optical member catalogue, no arbitrary new memberships.
def table_rows(path):
    lines=[l.rstrip('\n').split('\t') for l in path.open() if l.strip() and not l.startswith('#')]
    return [dict(zip([v.strip() for v in lines[0]],[v.strip() for v in r])) for r in lines[3:]]
members=[]
for r in table_rows(ROOT/'real_research/data/kt2017_galaxies.tsv'):
    try:members.append(dict(pgc=int(r['PGC']),pgc1=int(r['PGC1']),ra=float(r['RAJ2000']),de=float(r['DEJ2000']),hrv=float(r['HRV'])))
    except ValueError:continue
ktgroups={}
for r in table_rows(ROOT/'real_research/data/kt2017_groups.tsv'):
    try:ktgroups[int(next(iter(r.values())))]=r
    except ValueError:continue
def separation(ra,de):
    r,d=np.radians([ra,de]);ra2=np.radians([m['ra'] for m in members]);de2=np.radians([m['de'] for m in members])
    return 2*np.arcsin(np.sqrt(np.sin((de2-d)/2)**2+np.cos(d)*np.cos(de2)*np.sin((ra2-r)/2)**2))*180/np.pi*60
def galactic(ra,de):
    ra,de,rp,dp,ln=np.radians([ra,de,192.85948,27.12825,122.93192])
    b=np.arcsin(np.sin(de)*np.sin(dp)+np.cos(de)*np.cos(dp)*np.cos(ra-rp))
    l=(ln-np.arctan2(np.cos(de)*np.sin(ra-rp),np.sin(de)*np.cos(dp)-np.cos(de)*np.sin(dp)*np.cos(ra-rp)))%(2*np.pi)
    return math.degrees(l),math.degrees(b)
ga=json.loads((ROOT/'rebuild_2026_10_22/GA1_group_gas_audit/ga1_group_gas_audit_results.json').read_text())
existing={str(r['group']) for r in ga['runs']['PRIMARY']['table'] if 'dropped' not in r}
group_rows=[]
for r in csv.DictReader((HERE/'clogs_highrichness_inputs.csv').open()):
    ra,de,z=float(r['ra_deg']),float(r['dec_deg']),float(r['z'])
    sep=separation(ra,de);j=int(sep.argmin());m=members[j]
    l,b=galactic(ra,de)
    matched=bool(sep[j]<1. and abs(m['hrv']-299792.458*z)<500)
    row=dict(r,galactic_l=l,galactic_b=b,inside_original_HG_footprint=179.94<=l<=359.94 and abs(b)>=10,
             nearest_KT_member=m,nearest_separation_arcmin=float(sep[j]),BGE_member_match=matched,
             existing_GA_bright_group=matched and str(m['pgc1']) in existing)
    if matched:row['KT_group_catalogue_row']=ktgroups.get(m['pgc1'])
    row['candidate_only']=bool(matched and row['inside_original_HG_footprint'] and r['gas_morphology']=='GRP' and not row['existing_GA_bright_group'])
    group_rows.append(row)
res['groups']=dict(rows=group_rows,n_CLoGS_highrichness=len(group_rows),n_group_scale_halos=sum(r['gas_morphology']=='GRP' for r in group_rows),
                   candidate_only=[r['BGE'] for r in group_rows if r['candidate_only']],
                   new_graded_sample_count=0,
                   warning='Crossmatch discovery only. CLoGS selection differs from eRASS; no gas-mass normalization to HG radius; no matched-faint sensitivity recalibration; source R500 and M500 are Sun2009-scaled and excluded.')
say('CLoGS candidate-only associations inside original footprint, group-scale halo, absent GA BRIGHT: '+str(res['groups']['candidate_only']))
check('K4_CLoGS_coverage',len(group_rows)==26 and res['groups']['n_group_scale_halos']==14,'26 high-richness rows visited; 14 group-scale halos; no grading count upgrade')
hg1=json.loads((ROOT/'rebuild_2026_10_22/HG1_hot_gas_selector/hg1_hot_gas_selector.json').read_text())
hg2=json.loads((ROOT/'rebuild_2026_10_22/HG2_kids_lowg_hot_gas/hg2_kids_lowg_hot_gas.json').read_text())
o1=next(r for r in hg1['groups'] if r['name']=='39659')
o2=next(r for r in hg2['groups'] if r['name']=='39659')
candidate=next(r for r in group_rows if r['BGE']=='NGC 4261')
binid=int(np.floor(np.log10(o2['sigma'])/.1))
samebin=[r for r in hg2['groups'] if r.get('delta') is not None and np.isfinite(r['delta']) and int(np.floor(np.log10(r['sigma'])/.1))==binid]
byarm={arm:[r for r in samebin if r['flag']==arm] for arm in ('BRIGHT','FAINT')}
res['groups']['NGC4261_FAINT_counterexample']=dict(HG1_stored_row=o1,HG2_stored_row=o2,
    shared_bin_id=binid,shared_bin_members=byarm,
    n_bright_same_bin=len(byarm['BRIGHT']),n_faint_same_bin=len(byarm['FAINT']),
    in_shared_bin=bool(byarm['BRIGHT'] and byarm['FAINT']),
    CLoGS_kT_keV=1.36,CLoGS_kT_lower_error_keV=.02,CLoGS_kT_upper_error_keV=.03,
    CLoGS_detected_gas_radius_kpc=85.,HG_radius_kpc=o2['r_mpc']*1000,
    CLoGS_source_D_Mpc=float(candidate['D_Mpc']),HG_source_D_Mpc=o2['d_mpc'],
    CLoGS_detected_gas_radius_kpc_at_HG_distance=85.*o2['d_mpc']/float(candidate['D_Mpc']),
    HG_to_detected_radius_ratio=(o2['r_mpc']*1000)/(85.*o2['d_mpc']/float(candidate['D_Mpc'])),
    missing_fields=['Gas density normalization / cumulative gas mass and radial uncertainty at HG radius619kpc',
                    'Sensitivity-matched X-ray non-detections for all FAINT controls',
                    'Homogeneous 1-to-1 source matching and group-scale morphology selection'],
    interpretation='No selected eRASS match is not absence of a hot atmosphere. This is an actual label counterexample, not a promoted sample or recomputed D.')
check('K7_stored_FAINT_hot_halo_counterexample',candidate['BGE_member_match'] and candidate['gas_morphology']=='GRP' and o1['flag']==o2['flag']=='FAINT' and o2['mgas']==0.,
      f'KT39659=NGC4261; CLoGS group-scale hot halo; HG1/HG2 FAINT; shared bin {binid}: {len(byarm["BRIGHT"])} bright/{len(byarm["FAINT"])} faint')
AUDIT['active']=False
AFTER={p:sha(ROOT/p) for p in BEFORE}
check('K5_inputs_unchanged',BEFORE==AFTER,'all declared local inputs unchanged during run')
peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform=='darwin' else 1e6)
check('K6_resource_limit',peak<1.,f'peak RSS={peak:.3f}GB <1GB; one thread')
res['checks']=CHECKS;res['run']=dict(runtime_seconds=time.time()-START,peak_RSS_GB=peak,
    python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,input_hashes=BEFORE,
    input_hashes_after=AFTER,started_at=STARTED_AT,commit=COMMIT)
say(f'OBSERVATIONS COMPLETE: {sum(CHECKS.values())}/{len(CHECKS)} checks PASS.')
def finite_json(value):
    if isinstance(value,float) and not math.isfinite(value):return None
    if isinstance(value,dict):return {k:finite_json(v) for k,v in value.items()}
    if isinstance(value,list):return [finite_json(v) for v in value]
    return value
(HERE/f'observations_results{TAG}.json').write_text(json.dumps(finite_json(res),indent=2,sort_keys=True,allow_nan=False)+'\n')
(HERE/f'observations{TAG}.out').write_text('\n'.join(OUT)+'\n')
sys.exit(0 if all(CHECKS.values()) else 1)
