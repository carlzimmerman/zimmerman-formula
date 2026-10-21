"""Finite collision diagnostics and conditional mode-reference sensitivity.

Core aperture charge is not a bound-mass estimator. Symplectic coordinates
are not automatically persistent mode energies in a nonlinear remnant.
"""
from pathlib import Path
import sys,json,math,resource,time
import numpy as np
from scipy.sparse.linalg import norm as sparse_norm
from pair_projection import analyze_snapshot,read_snapshot

here=Path(__file__).resolve().parent;root=here.parents[1]
old=root/'sol61_push/cold_fragment_modes_2026_10_20'
sys.path.insert(0,str(old))
from radial_tools import operators,P
from outgoing_library import outgoing_solve

refs,out=map(Path,sys.argv[1:3]);start=time.monotonic();checks=[]
def ck(n,v):checks.append({'name':n,'pass':bool(v)})
cases=['pair_inphase','pair_dt_half','pair_dx_fine','pair_antiphase',
       'isolated_static','isolated_moving','pair_separation','pair_faster']
summary=[]
def jsonlines(path):return [json.loads(x) for x in path.read_text().splitlines()]
for name in cases:
    run=here/(name+'_run_001');d=json.loads((run/'results.json').read_text())
    m=json.loads((run/'manifest.json').read_text());ck(name+' completed recorded controls',m['run']['status']=='completed' and d['all_checks_pass'])
    logs=jsonlines(run/'evolution/log.jsonl');energy=jsonlines(run/'evolution/enclosed_energy.jsonl')
    a,b=logs[0],logs[-1];ea,eb=energy[0],energy[-1]
    qout_change=a['Q20']-b['Q20'];eout_change=eb['Eout20']-ea['Eout20']
    summary.append({'case':name,'initial':a,'final':b,'final_positive_face_energy':eb,
                    'Q15_fraction_final':b['Q15']/b['Q'],'Q20_fraction_final':b['Q20']/b['Q'],
                    'net_Q_transport_out_of_radius20':qout_change,
                    'outside20_positive_energy_change':eout_change,
                    'outside_energy_per_net_outward_Q':eout_change/qout_change if qout_change else None,
                    'E20_over_Q20_final':eb['E20']/b['Q20'],
                    'warning':'Aperture transport and local inventory, not asymptotic escape or automatically bound charge.'})

gamma=[]
for Q in [136000,140000]:
    name=f'Q{Q}_L60_N1199.npz';m=np.load(refs/name);profile=refs/('profile_'+name)
    z=m['mode'];r=m['r'];Om=float(m['Omega']);om=float(m['omega']);u,s,x,v,t=z/r
    f,b,h=m['background_fields'];F=math.sqrt(2)*f;g,a,M,lam=P['g'],P['a'],P['M_chi'],P['lambda']
    nn=np.array([lam*F*(3*u*u+v*v)+math.sqrt(2)*g*(s*u+t*v)+a*x*u,
                 g/math.sqrt(2)*(u*u-v*v),.5*(-.75*M+6*h)*x*x+.5*a*(u*u+v*v),
                 2*lam*F*u*v+math.sqrt(2)*g*(-s*v+t*u)+a*x*v,math.sqrt(2)*g*u*v])
    components=[]
    for ell,C in [(0,1/math.sqrt(4*math.pi)),(2,math.sqrt(5)/(7*math.sqrt(math.pi))),(4,3/(7*math.sqrt(math.pi)))]:
        op=operators(profile,Q,60.,1199,ell)
        ck(f'Q{Q}ell{ell} matching stationary reference',abs(op['record']['omega']-om)<1e-11)
        sol=outgoing_solve(op,2*Om,(-C*r*nn).reshape(-1),P,m=0);s0=sol['summary']
        ck(f'Q{Q}ell{ell} positive outgoing flux',s0['K_continuum_total']>0)
        ck(f'Q{Q}ell{ell} source work',s0['source_work_relative_difference']<1e-6)
        ck(f'Q{Q}ell{ell} residual',s0['linear_relative_residual']<1e-8)
        ck(f'Q{Q}ell{ell} only Psi open',[q['name'] for q in s0['channels'] if q['open']]==['Psi+'])
        components.append(s0)
        np.savez_compressed(out/f'outgoing_Q{Q}_ell{ell}.npz',r=r,y=sol['y'],force=-C*r*nn)
    gamma.append({'Q':Q,'Omega':Om,'omega':om,'gamma_Y20':sum(x['K_continuum_total'] for x in components),'components':components,
                  'scope':'New weak-mode coefficient at this discrete reference, not a collision-wide cooling law.'})

projections=[]
for case in ['pair_inphase','pair_dt_half','pair_dx_fine','pair_separation']:
  for Q in [136000,140000]:
    tag=f'Q{Q}_L60_N1199.npz';mode=refs/tag;profile=refs/('profile_'+tag)
    om=float(np.load(mode)['omega'])
    for ti in range(80,241,20):
      snap=here/(case+'_run_001')/'evolution'/f'snap_t{ti*1000:09d}.bin'
      for frame in ['reference_omega','fitted_omega']:
        result=analyze_snapshot(snap,mode,profile,Qref=Q,
                                carrier_frequency=om if frame=='reference_omega' else None)
        ck(f'{case}Q{Q}t{ti}{frame} finite projection',np.isfinite(result['conditional_K_coordinate']))
        result.update(case=case,frame=frame)
        projections.append(result)
iso=[]
for ti in [0,80,120,160,200,240]:
    mode=old/'natural_run_002/Q80000_L60_N1199.npz';profile=old/'profile_origin/run_001/Q80000.npz'
    om=float(np.load(mode)['omega'])
    r=analyze_snapshot(here/'isolated_static_run_001/evolution'/f'snap_t{ti*1000:09d}.bin',mode,profile,Qref=80000,carrier_frequency=om)
    iso.append(r)

fits=[]
for case in ['pair_inphase','pair_dt_half','pair_dx_fine','pair_separation']:
  for Q in [136000,140000]:
    a=[x for x in projections if x['case']==case and x['Q_reference']==Q and x['frame']=='reference_omega' and x['time']>=120]
    tt=np.array([x['time'] for x in a]);cc=np.array([x['coordinate_real']+1j*x['coordinate_imag'] for x in a])
    best=None
    for freq in np.linspace(.04,.075,701):
        basis=np.array([np.ones_like(tt),np.exp(1j*freq*tt),np.exp(2j*freq*tt)]).T
        fit=np.linalg.lstsq(basis,cc,rcond=None)[0];res=np.linalg.norm(basis@fit-cc)/max(np.linalg.norm(cc),1e-300)
        if best is None or res<best['relative_complex_residual']:
            best={'Omega_fit':float(freq),'relative_complex_residual':float(res),'constant_complex':[float(fit[0].real),float(fit[0].imag)],'fundamental_abs_squared':float(abs(fit[1])**2),'second_harmonic_abs_squared':float(abs(fit[2])**2)}
    best.update(case=case,Q_reference=Q,Omega_reference=a[0]['Omega_reference'],window=[120,240],n_samples=len(a),
                exploratory_fit='Complex constant + positive-time fundamental + second harmonic; finite frequency search .04..075, step.00005. Not independent confirmation or automatic mode acceptance.')
    fits.append(best)

# Scientific figures: data/coordinates labelled in action units and finite scope.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
fig,axes=plt.subplots(1,5,figsize=(14,4.6),constrained_layout=True)
for ax,(case,ti,label) in zip(axes,[('pair_inphase',0,'Initial pair'),('pair_inphase',60,'In phase, t=60'),('pair_inphase',140,'In phase, t=140'),('pair_inphase',240,'In phase, t=240'),('pair_antiphase',240,'Opposite phase, t=240')]):
    ss=read_snapshot(here/(case+'_run_001')/'evolution'/f'snap_t{ti*1000:09d}.bin')
    rr=ss['rho'];zz=ss['z'];d=ss['fields'];ir=rr<25;iz=abs(zz)<35
    density=np.asarray(d[0][np.ix_(iz,ir)])**2+np.asarray(d[1][np.ix_(iz,ir)])**2
    im=ax.pcolormesh(rr[ir],zz[iz],density,shading='nearest',norm=LogNorm(vmin=.001,vmax=80),cmap='magma')
    ax.set_title(label);ax.set_xlabel('cylindrical radius');ax.set_aspect('equal')
axes[0].set_ylabel('z (action units)');fig.colorbar(im,ax=axes,label=r'$|\Psi|^2$',shrink=.8)
fig.suptitle('Same-action head-on fields: finite collision diagnostic')
fig.savefig(out/'pair_density.png',dpi=160);plt.close(fig)

fig,ax=plt.subplots(1,2,figsize=(11,4),constrained_layout=True)
for case,style in [('pair_inphase','-'),('pair_dt_half','--'),('pair_dx_fine',':'),('pair_antiphase','-.')]:
    logs=jsonlines(here/(case+'_run_001')/'evolution/log.jsonl')
    ax[0].plot([x['t'] for x in logs],[x['Q15']/x['Q'] for x in logs],style,label=case)
ax[0].set(xlabel='time (action units)',ylabel='charge fraction within radius15');ax[0].legend(fontsize=8)
for case,style in [('pair_inphase','-'),('pair_dt_half','--'),('pair_dx_fine',':')]:
    a=[x for x in projections if x['case']==case and x['Q_reference']==136000 and x['frame']=='reference_omega']
    ax[1].plot([x['time'] for x in a],[x['conditional_K_coordinate'] for x in a],style,marker='o',label=case)
ax[1].set(xlabel='time (action units)',ylabel='conditional quadrupole coordinate |c|²');ax[1].legend(fontsize=8)
fig.suptitle('Central concentration and conditional mode content; no dwarf inference')
fig.savefig(out/'pair_diagnostics.png',dpi=160);plt.close(fig)

rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;ck('analysis RSS below1GB',rss<1_000_000_000)
result={'scope':'Actual field evolution summaries, conditional matched-reference mode coordinates and new reference radiation coefficients. No galaxy capture/stock closure.',
        'summary':summary,'reference_radiation':gamma,'conditional_projections':projections,'isolated_static_projections':iso,'exploratory_fits':fits,
        'checks':checks,'n_checks':len(checks),'all_checks_pass':all(x['pass'] for x in checks),'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
        'non_claims':['A coherent component fit is exploratory and not a nonlinear normal-mode theorem',
                      'No accepted mode-energy fraction without reference/amplitude/frame checks',
                      'No asymptotic escape or orbital J (all head-onJ0)','No physical unit scale or population/phase distribution',
                      'No four-dwarf mass/profile/stellar-heating fit']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
