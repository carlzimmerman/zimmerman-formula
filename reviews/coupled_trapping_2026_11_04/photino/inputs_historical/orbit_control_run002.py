"""Unbackreacted two-state conversion control on immutable zero-loss orbits.

Both carrier species are assigned the same conserved comoving momentum
shape for this diagnostic. Gauge emissions/energy are counted, no Pauli,
Bose, inverse scattering, Goldstino or non-gauge branches. This is not an
energy-consistent history once emission or carrier mass work is appreciable.
"""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
from scipy.interpolate import CubicSpline,PchipInterpolator
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from source import atx,E,G,XI,GSM,MP


def mass(x):
    a=math.sqrt(2/(31*E));A=np.array([[E*x/2,-E*a/2,5*G*a],[-E*a/2,0,5*G*x],[5*G*a,5*G*x,0.]])
    return float(min(abs(np.linalg.eigvalsh(A))))


def table(step):
    cross=json.loads((HERE/'run_source004/result.json').read_text())['threshold_x']
    grid=np.unique(np.r_[np.arange(0,25+step/2,step),cross-1e-4,cross,cross+1e-4])
    rows=[atx(float(x)) for x in grid]
    out={}
    for key in ('light_fermion_over_mu','lightest_scalar_over_mu','gauge_channels_total_over_mu','reverse_gauge_channels_total_over_mu'):
        out[key]=PchipInterpolator(grid,[r[key] for r in rows])
    out['Ef']=PchipInterpolator(grid,[r['gauge_channels_total_over_mu']*(r['mean_photino_pstar_over_mu'] or 0) for r in rows])
    out['Es']=PchipInterpolator(grid,[r['reverse_gauge_channels_total_over_mu']*(r['reverse_mean_photino_pstar_over_mu'] or 0) for r in rows])
    return out,rows


def orbit_rates(packet,run,tab,nodes):
    V=CubicSpline(packet['grid'],packet['T0_potential_mu4'],bc_type=((1,packet['origin_force']),(2,0)))
    mg=np.linspace(0,200,4001);ms=CubicSpline(mg,[mass(float(x)) for x in mg])
    q=np.array(run['q_centers']);f=np.array(run['initial_f']);edges=np.array(run['q_edges']);W=(edges[1:]**3-edges[:-1]**3)/3
    Nsum=float(W@f);z,zw=leggauss(nodes);theta=(z+1)*math.pi/2;tw=zw*math.pi/2
    result=[]
    for h in run['history']:
        t=h['Tc_over_mu'];xl=h['x_inner'];xr=h['x_outer'];half=(xr-xl)/2;mid=(xr+xl)/2
        xs=mid-half*np.cos(theta);dx=half*np.sin(theta)
        mm=ms(xs);en=np.sqrt(mm[:,None]**2+(t*q[None,:])**2)
        rho=24/(2*math.pi**2)*t**3*(en@(W*f));delta=h['energy']-V(xs)-rho
        if min(delta)<=0:raise ValueError(('orbit energy does not enclose quadrature',run['kind'],h['N'],float(min(delta))))
        w=tw*dx/np.sqrt(delta);period=math.sqrt(124)*sum(w);w/=sum(w)
        Df=(mm[:,None]/en)@(W*f)/Nsum
        ss=tab['lightest_scalar_over_mu'](xs);Ds=(ss[:,None]/np.sqrt(ss[:,None]**2+(t*q[None,:])**2))@(W*f)/Nsum
        gf=tab['gauge_channels_total_over_mu'](xs);gs=tab['reverse_gauge_channels_total_over_mu'](xs)
        H=math.sqrt(math.pi**2*GSM/90)*(t/XI)**2*run['mu_GeV']/MP
        result.append(dict(N=h['N'],Tc_over_mu=t,x_inner=xl,x_outer=xr,period_mu_inverse=float(period),
            aF=float(w@(gf*Df)/H),aS=float(w@(gs*Ds)/H),
            eF=float(w@tab['Ef'](xs)/H),eS=float(w@tab['Es'](xs)/H),
            Gamma_over_oscillation=float(max(w@(gf*Df),w@(gs*Ds))*period/(2*math.pi))))
    n0=24/(2*math.pi**2)*run['history'][0]['Tc_over_mu']**3*Nsum
    return result,n0


def propagate(rows,substeps):
    N=np.array([r['N'] for r in rows]);pF=1.;events=0.;energy=0.;trace=[]
    arrays={k:np.array([r[k] for r in rows]) for k in ('aF','aS','eF','eS')}
    for j in range(len(N)-1):
        dn=(N[j+1]-N[j])/substeps
        for n in range(substeps):
            pos=N[j]+(n+.5)*dn
            a,b,ef,es=[float(np.interp(pos,N,arrays[k])) for k in ('aF','aS','eF','eS')]
            total=a+b
            if total>0:
                eq=b/total;decay=-math.expm1(-total*dn);IF=eq*dn+(pF-eq)*decay/total
                pF=eq+(pF-eq)*(1-decay)
            else:IF=pF*dn
            IS=dn-IF;events+=a*IF+b*IS;energy+=ef*IF+es*IS
        trace.append(dict(N=float(N[j+1]),fermion_fraction=pF,scalar_fraction=1-pF,gauge_emissions_per_initial_carrier=events,
            direct_photinos_per_initial_carrier=events/6,emitted_gauge_energy_over_mu_per_initial_carrier=energy))
    return dict(final=trace[-1],history=trace)


def main(out):
    start=time.monotonic();stat=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())
    fine,raw=table(.05);coarse,_=table(.1);cases=[]
    for packet in stat['points']:
        kind=packet['kind'];run=json.loads((HERE.parent/'kinetics'/f'run_{kind}_zero2_001/result.json').read_text())['cases'][0]
        configs=[]
        for name,tab,nodes,substeps in [('preferred',fine,24,32),('orbit12',fine,12,32),('rate_grid_01',coarse,24,32),('time16',fine,24,16)]:
            rows,n0=orbit_rates(packet,run,tab,nodes);p=propagate(rows,substeps);p.update(name=name,nodes=nodes,substeps=substeps,
                maximum_rate_over_oscillation=max(r['Gamma_over_oscillation'] for r in rows),initial_energy_per_carrier_over_mu=run['history'][0]['energy']/n0,
                emitted_over_initial_hidden_energy=p['final']['emitted_gauge_energy_over_mu_per_initial_carrier']/(run['history'][0]['energy']/n0),rates=rows)
            configs.append(p)
        maincase=configs[0];events=maincase['final']['gauge_emissions_per_initial_carrier'];initialY=run['history'][0]['Y_charged']
        vac=next(v for v in json.loads((HERE/'run_source004/result.json').read_text())['vacua'] if v['kind']==kind)
        cases.append(dict(kind=kind,control_configs=configs,unblocked_direct_photino_yield=events/6*initialY,
            fraction_full_DM=events/6*initialY/vac['target_photino_yield'],
            relative_controls={z['name']:abs(z['final']['gauge_emissions_per_initial_carrier']/events-1) for z in configs[1:]}))
    checks=dict(positive_energy_and_rates=all(min(r[k] for c in cases for q in c['control_configs'] for r in q['rates'])>=0 for k in ('aF','aS','eF','eS')),
        normalized_two_state=all(0<=q['final']['fermion_fraction']<=1 for c in cases for q in c['control_configs']),
        slow_conversion_per_orbit=all(q['maximum_rate_over_oscillation']<.01 for c in cases for q in c['control_configs']),
        source_grid_control=max(c['relative_controls']['rate_grid_01'] for c in cases)<.02,
        time_control=max(c['relative_controls']['time16'] for c in cases)<.01,
        orbit_control=max(c['relative_controls']['orbit12'] for c in cases)<.1)
    checks={k:bool(v) for k,v in checks.items()}
    result=dict(claim_id='CT09_UNBACKREACTED_TWO_CARRIER_ORBIT_CONTROL',checks=checks,cases=cases,
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Counterfactual carrier-conserved zero-loss orbit, same frozen momentum shape assigned to F and S, leading gauge decays only, no Pauli/Bose/inverse scatterings or feedback. Emitted physical energy per carrier summed over births is a work diagnostic, not an energy ledger or an upper bound on actual annihilating/cascading histories.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,cases=[{k:v for k,v in c.items() if k!='control_configs'}|{'preferred':c['control_configs'][0]['final'],'emitted_over_initial_hidden_energy':c['control_configs'][0]['emitted_over_initial_hidden_energy']} for c in cases],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes']),indent=2));assert all(checks.values()),checks


if __name__=='__main__':
    try:main(sys.argv[1])
    finally:print('observed_peak_RSS_bytes='+str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),flush=True)
