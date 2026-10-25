"""Independent integral identities, spin storage identity, stellar-force diagnostics."""
import json,hashlib,importlib.util,pathlib,math,resource
import numpy as np
from scipy.integrate import quad
from scipy.special import sph_harm
P=pathlib.Path(__file__).resolve().parent; ROOT=P.parents[1]
paths=[P/'eta1500_refine.json',P/'spectrum.py',pathlib.Path(__file__),ROOT/'sol61_push/cold_survey_capture_2026_10_24/survey.py',ROOT/'sol61_push/cold_survey_capture_2026_10_24/capture_results.json',ROOT/'sol61_push/cold_data_constraints_2026_10_24/results.json',ROOT/'sol61_push/cold_prestellar_waves_2026_10_24/runs/draco_hybrid.json',ROOT/'sol61_push/cold_survey_capture_2026_10_24/data/members.tsv',ROOT/'real_research/data/dsph/lvd_dwarf_mw.csv',ROOT/'sol61_push/cold_survey_capture_2026_10_24/survey_results.json']
paths+=list(P.glob('eta1500_refine_*.npz'))
def hashes(): return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
before=hashes()
spec=importlib.util.spec_from_file_location('survey',paths[3]);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
d=s.load(); prev=json.loads(paths[5].read_text())['galaxies'];models=json.loads(paths[4].read_text())['models'];run=json.loads(paths[0].read_text())
old=json.loads(paths[6].read_text());meanm=old['initial']['J']/old['physical']['eta_code']/old['initial']['M']
qnum=quad(lambda x:75*x**4/(1+x*x)**4.5/8,0,np.inf)[0]
wvir=quad(lambda x:3*x**4/(1+x*x)**4,0,np.inf)[0]
assert abs(qnum-15/28)<1e-12 and abs(wvir-3*np.pi/32)<1e-12
phi=np.linspace(0,2*np.pi,101,endpoint=False);theta=np.arccos(np.linspace(-.999,.999,70))
T,F=np.meshgrid(theta,phi,indexing='ij');checks=[]
for l in [1,2,4,16,32]:
    un=sum(abs(sph_harm(m,l,F,T))**2 for m in range(-l,l+1))/(2*l+1)
    polarized=(abs(sph_harm(0,l,F,T))**2+2*sum(abs(sph_harm(m,l,F,T))**2 for m in range(1,l+1)))/(2*l+1)
    checks.append(float(np.max(abs(polarized-un))))
assert max(checks)<1e-12
rows=[]
for m,res in zip(models,run['results']):
    name=m['name'];raw=np.load(P/f'eta1500_refine_{name.replace(" ","")}.npz');x=raw['x'];shell=raw['shell_mass_fraction'];cdf=np.cumsum(shell);h=x[1]-x[0];b=m['cold_scale_pc'];M=m['cold_mass'];a=s.A0['canonical'];rstar={'Draco':193.22,'Sextans':485.89,'Fornax':695.33,'Leo I':229.1}[name]
    def menc(r):return M*np.interp(r/b,np.r_[0,x+h/2],np.r_[0,cdf],left=0,right=cdf[-1])
    def gc(r):return s.G*menc(r)/r**2
    row={'name':name,'eta_ceiling_for_exact_target_pc_kms':1500/math.sqrt(res['quantum_floor_over_required']),'profile_fit_max_error':res['fit_max_aperture_relative_error'],'central_aperture_pc':rstar,'fitted_mass_inside_stellar_half_light_Msun':float(menc(rstar)),'target_mass_inside_stellar_half_light_Msun':float(M*rstar**3/(rstar*rstar+b*b)**1.5),'specific_spin_capacity_pc_kms':res['maximum_density_preserving_net_j_pc_kms']}
    source=5.364*200*m['formed_mass'];Jinitial=source*1500*meanm;capacity=M*row['specific_spin_capacity_pc_kms']
    row['minimum_initial_spin_fraction_needing_export_for_this_fit']=max(0,1-capacity/Jinitial)
    row['source_mass_Msun']=source;row['source_j_pc_kms']=1500*meanm
    if name=='Sextans':
        def gb(r):
            gn=sum(s.G*250000*r/(r*r+ar*ar)**1.5 for ar in d['aa'])
            return .5*(gn+np.sqrt(gn*gn+4*a*gn))
        var=np.array([s.projection(d['R'],ar,lambda r:gb(r)+gc(r)) for ar in d['aa']]).T
        fit=s.fit(d,var,np.zeros_like(var),fixed_mass=0.)
        refs=json.loads(paths[9].read_text())['continuous_best'];nll=min(z['nll'] for z in refs if z['footing']=='canonical' and z['beta']==0 and z['tracer_taper_pc'] is None)
        row['survey_fit_nll']=fit['nll'];row['survey_twice_nll_above_target']=2*(fit['nll']-nll)
    else:
        t,w=np.polynomial.legendre.leggauss(192);t=(t+1)*np.pi/4;w*=np.pi/4;r=rstar*np.tan(t)
        cold=rstar*np.sum(w*np.sin(t)**3*gc(r))
        base=prev[name]['moments']['canonical'][0]['sigma_baryon']**2
        row['stellar_global_sigma_kms']=float(np.sqrt(base+cold));row['observed_sigma_kms']=float(prev[name]['observations']['vlos_sigma'])
    rows.append(row)
after=hashes();assert before==after
out={'scope':'reconstruction and stationary ensemble diagnostics; no formation or live stellar heating test','checks':{'quantum_coefficient':qnum,'analytic_quantum_coefficient':15/28,'self_virial_coefficient':wvir,'analytic_self_virial_coefficient':3*np.pi/32,'max_density_change_under_m_polarization':max(checks)},'initial_mean_m_CCT007_shape':meanm,'inputs_before':before,'inputs_after':after,'maxrss_native':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'results':rows}
(P/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
for row in rows: print(row,flush=True)
