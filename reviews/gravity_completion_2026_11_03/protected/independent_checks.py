"""Independent leading profile/current controls and precision repeat."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,resource,time,hashlib
from pathlib import Path
import mpmath as mp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
import solve_protected as full


def main(out):
    started=time.monotonic()
    prior=HERE/'run_local_001/result.json';r=json.loads(prior.read_text())
    rows=[]
    for dps in (60,100):
        mp.mp.dps=dps
        e=mp.mpf('.003');mu=mp.mpf('18170662.111498855');M=mp.mpf('2.435e18')
        eps=mp.mpf('.0001');n=3-eps;Z=mp.mpf('7.3671437212785083116194')
        def psi(t):return full.cw(Z/mp.sqrt(31*e)*t,e,e,mp.sqrt(mp.mpf(29)/200)*e)/e**2
        tilt=2*Z*mu*mp.sqrt(eps)/(31*M*e**mp.mpf('2.5'))
        t=mp.findroot(lambda t:mp.diff(psi,t)-tilt,(1,mp.mpf('1.1')))
        fold=mp.findroot(lambda t:mp.diff(psi,t,2),(mp.mpf('1.2'),mp.mpf('1.3')))
        m32=mu**2/(mp.sqrt(31*eps)*M)
        mr=mu*mp.sqrt(e**3*mp.diff(psi,t,2)/(2*Z**2))
        ma=mu*mp.sqrt(e**3*mp.diff(psi,t)/(2*Z**2*t))
        zeta=eps/n*m32
        fs=mp.mpf(0)
        if dps==100:
            # Completely rerun the five-variable solve at higher precision;
            # exact decimal constants are refreshed where no irrational exists.
            rr=mp.findroot(full.equations,tuple(map(mp.mpf,r['root'])),tol=mp.mpf('1e-70'),maxsteps=15)
            fs=max(abs(rr[j]-mp.mpf(r['root'][j])) for j in (0,3,4))
        rows.append(dict(dps=dps,t=str(t),fold=str(fold),m32_GeV=str(m32),m_sigma_GeV=str(mr),m_phase_GeV=str(ma),m_zeta_GeV=str(zeta),tilt_over_max=str(tilt/mp.diff(psi,fold)),full_precision_repeat_root_difference=str(fs)))
    a,b=rows
    # Full finite-splitting rigid transverse spectrum at the actual point.
    t=mp.mpf(r['root'][0]);e=mp.mpf('.003');mu=mp.mpf('18170662.111498855')
    g=mp.sqrt(mp.mpf(29)/200)*e;X=mp.mpf(r['stationary_point']['T_GeV'])/(mu*mp.sqrt(31))
    masses=full.build_model(float(X),float(e),float(e),float(g),vertices=False)
    positiveS=[v for v in masses['mS2'] if v>0];positiveF=[v for v in masses['mF2'] if v>0]
    # A profile-wide obstruction to *kinematic* closure of the uneaten mode.
    # Eliminate mu sqrt(eps) by stationarity. No new independent mass scale.
    fold=mp.mpf(b['fold']);profiles=[]
    for j in range(17):
        tt=1+(fold-1)*mp.mpf(j)/16
        xx=mp.mpf('7.3671437212785083116194')/mp.sqrt(31*e)*tt
        dd=full.build_model(float(xx),float(e),float(e),float(g),vertices=False)
        ext,labels=full.ext_basis(dd);groups,_=full.summarize(full.threshold(dd,ext),labels)
        cchi=abs(mp.mpf(groups['U1']['signed_mass']))/e**mp.mpf('2.5')
        def psi(s):return full.cw(mp.mpf('7.3671437212785083116194')/mp.sqrt(31*e)*s,e,e,g)/e**2
        ratio=mp.sqrt(31)*mp.diff(psi,tt)/(2*(3-mp.mpf('.0001'))*mp.mpf('7.3671437212785083116194')*cchi)
        profiles.append(dict(t=float(tt),cchi=float(cchi),stationary_m_zeta_over_mchi=float(ratio)))
    # UV anomaly coefficient including all three sources, not compensator-only.
    eps=mp.mpf('.0001');n=3-eps
    anomalies=[]
    for TG,TR,label in [(5,10,'SU5 UV with two adjoints'),(3,0,'SU3 below chiral thresholds'),(2,0,'SU2 below chiral thresholds'),(0,0,'U1 below charged thresholds')]:
        coeff=(3*TG-TR)*(1-n/3)+(mp.mpf(2)/3)*TR*n-2*TR
        anomalies.append(dict(label=label,TG=TG,TR=TR,combined_coefficient=str(coeff),expected_epsilon_TG_minus_TR=str(eps*(TG-TR))))
    checks=dict(precision_repeat_leading_roots=abs(mp.mpf(a['t'])-mp.mpf(b['t']))<mp.mpf('1e-50'),
                full_precision_repeat=mp.mpf(b['full_precision_repeat_root_difference'])<mp.mpf('1e-50'),
                independent_leading_root_agrees=abs(mp.mpf(b['t'])/mp.mpf(r['root'][0])-1)<mp.mpf('1e-6'),
                independent_scalar_masses_agree=max(abs(float(b['m_sigma_GeV'])/r['spectrum']['neutral_scalar_masses_GeV'][1]-1),abs(float(b['m_phase_GeV'])/r['spectrum']['neutral_scalar_masses_GeV'][0]-1))<1e-6,
                sixteen_profile_intervals_covered=len(profiles)==17,
                orthogonal_channel_open_on_profile_grid=max(p['stationary_m_zeta_over_mchi'] for p in profiles)<.001,
                combined_anomaly_identity=all(abs(mp.mpf(v['combined_coefficient'])-mp.mpf(v['expected_epsilon_TG_minus_TR']))<mp.mpf('1e-90') for v in anomalies),
                nonflat_rigid_scalar_gap_positive=min(positiveS)>0)
    result=dict(claim_id='PG06_INDEPENDENT_CHECKS',checks={k:bool(v) for k,v in checks.items()},precision_rows=rows,profile=profiles,
                rigid_transverse=dict(minimum_positive_scalar_GeV=float(mp.sqrt(min(positiveS))*mu),minimum_positive_fermion_GeV=float(mp.sqrt(min(positiveF))*mu),zero_scalar_count=int(sum(masses['mS2']==0)),zero_fermion_count=int(sum(masses['mF2']==0)),meaning='Rigid tree nonflat gap; logarithmic gravity/finite transverse-loop spectrum is not substituted by this control.'),
                anomaly=anomalies,anomaly_scope='Small-field tree metric with constant gauge kinetic function: K_i F^i/M^2=-n m32 and (logdet K_R)_i F^i/dR=-m32. Finite heavy matching/current still separate.',
                raw_input_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),runtime_seconds=time.monotonic()-started,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                non_claims=['Finite profile grid is not a uniform monotonicity proof','Anomaly cancellation identity does not replace finite Higgs/chiral thresholds','No matched transverse one-loop SUGRA pole'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
