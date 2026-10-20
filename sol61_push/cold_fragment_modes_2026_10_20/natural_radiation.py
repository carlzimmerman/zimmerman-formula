"""Natural scalar second-harmonic loss coefficient of a unit-K quadrupole."""
from pathlib import Path
import json,sys,resource,time,math
import numpy as np
from radial_tools import operators,P
from outgoing_library import outgoing_solve,hankel_polynomial

mode_dir=Path(sys.argv[1]);profiles=Path(sys.argv[2]);out=Path(sys.argv[3]);rows=[];checks=[];start=time.monotonic()
def ck(n,v):checks.append({'name':n,'pass':bool(v)})
# Independent explicit ell4 boundary-polynomial control.
z=3.2
ck('correct ell4 outgoing polynomial',abs(hankel_polynomial(4,z)-(1-10j/z-45/z**2+105j/z**3+105/z**4))<1e-13)
for Q in [80000,160000]:
    for L,N in [(40.,399),(60.,599),(60.,1199)]:
        name=f'Q{Q}_L{int(L)}_N{N}.npz';m=np.load(mode_dir/name)
        op=operators(profiles/f'Q{Q}.npz',Q,L,N,4);Om=2*float(m['Omega'])
        ck(f'{Q} {L} {N} matched background',abs(op['record']['omega']-float(m['omega']))<1e-12)
        ck(f'{Q} {L} {N} same radial grid',np.max(abs(op['r']-m['r']))<1e-12)
        F=m['source'].reshape(-1)
        s=outgoing_solve(op,Om,F,P,m=4)
        v=s['summary'];gamma=v['K_continuum_total']
        ck(f'{Q} {L} {N} positive natural outgoing power',gamma>0)
        ck(f'{Q} {L} {N} onlyPsi open',[c['name'] for c in v['channels'] if c['open']]==['Psi+'])
        ck(f'{Q} {L} {N} work balance',v['source_work_relative_difference']<1e-6)
        ck(f'{Q} {L} {N} linear residual',v['linear_relative_residual']<1e-8)
        ck(f'{Q} {L} {N} intrinsic J per K',abs(v['Jz_edge_total']/v['K_edge_total']/(2/float(m['Omega']))-1)<1e-8)
        ck(f'{Q} {L} {N} charge per K',abs(v['Q_edge_total']/v['K_edge_total']*Om-1)<1e-8)
        scaled=outgoing_solve(op,Om,.25*F,P,m=4)['summary']
        ck(f'{Q} {L} {N} half-mode amplitude fourth-power loss',abs(scaled['K_edge_total']/v['K_edge_total']-1/16)<1e-9)
        v.update(Q_target=Q,Omega_parent=float(m['Omega']),gamma_for_unit_K_mode=gamma,
                 gamma_edge=v['K_edge_total'],parent_mode_file=name,
                 parent_K_normalization=float(m['K_normalization']),
                 mode_energy_half_life_for_K0_1=1/gamma,
                 parent_period=2*math.pi/float(m['Omega']),
                 weak_rate_ratio_for_K0_1=gamma/float(m['Omega']),
                 scalar_loss_law='dK_mode/dt=-gamma*K_mode^2 to leading weak-amplitude order; t in1/m, K in m units',
                 charge_and_energy='Q_remdot=-Q_outdot, E_remdot=-E_outdot, with slow remnant omega and mode/background charge adjustment; no fixed-Q remnant assumption')
        rows.append(v)
        np.savez_compressed(out/f'response_{name}',r=op['r'],y=s['y'].reshape(5,N),force=m['source'],
                            circular_last=s['circular_last'],circular_ghost=s['circular_ghost'],Omega=Om)
        print(json.dumps({k:v[k] for k in ['Q','L','N','Omega_parent','gamma_for_unit_K_mode','source_work_relative_difference','mode_energy_half_life_for_K0_1']}),flush=True)
for Q in [80000,160000]:
    a,b,c=[next(t for t in rows if t['Q_target']==Q and t['L']==L and t['N']==N) for L,N in [(40.,399),(60.,599),(60.,1199)]]
    ck(f'{Q} natural coefficient box convergence',abs(a['gamma_for_unit_K_mode']/b['gamma_for_unit_K_mode']-1)<.05)
    ck(f'{Q} natural coefficient mesh convergence',abs(b['gamma_for_unit_K_mode']/c['gamma_for_unit_K_mode']-1)<.05)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('measured RSS below1GB',rss<1_000_000_000)
result={'scope':'Leading scalar-matter self-radiation coefficient of specified chiral bound mode, not imposed drive or merger efficiency.',
        'assumptions':['Same explicit alternative action','Positive-energy localized l2m2 eigenmode with exp(+iOmega t) and dphiY=-imY',
                       'Weak amplitude and slowly varying background; scalar2Omega response only','Mode K=A² after normalization; static and fundamental nonlinear corrections are higher-order for the computed2Omega loss',
                       'Metric/GW emission not included','No frequency degeneracy/resonance invalidating single-mode adiabatic reduction assumed; needs nonlinear validation'],
        'rows':rows,'checks':checks,'n_checks':len(checks),'all_checks_pass':all(x['pass'] for x in checks),
        'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
        'non_claims':['No amplitude or phase distribution of a real merger','No fraction of stationary binding gap put into this mode','No direct galactic orbital J flux or dwarf mass-budget closure','No continuum error theorem or full nonlinear time-domain confirmation']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
