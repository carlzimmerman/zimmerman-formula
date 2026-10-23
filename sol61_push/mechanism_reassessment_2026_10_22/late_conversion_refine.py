"""Conditional late-window nonlinear tests; not a derived cosmological handoff."""
import json, sys, subprocess, hashlib, platform
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
OUT=ROOT/sys.argv[1]; OUT.mkdir(exist_ok=True)
source=json.loads((ROOT/'screening_exit_bound_v2_run/results.json').read_text())
m=.001; M=2*m*np.sqrt(1+.02**2); g=2.168e-6; lam=.00881292
A=source['probe']['X_envelope_GeV']; a=source['probe']['a']
Om=np.sqrt(2*g*A); F=Om/np.sqrt(lam); mp=m/Om; mx=M/Om; c=g/(np.sqrt(2)*lam*F)
period=2*np.pi/mx; rho=source['radiation_energy_constant_GeV4']/a**4
unit=Om**4/lam; bath=rho/unit; L=32.; seed=2026102301
rng=np.random.default_rng(seed)
master=np.fft.fftn(rng.normal(size=(2,2,64,64,64)),axes=(-3,-2,-1))/64**3

def initial(n,band,energy):
    inds=(np.fft.fftfreq(n)*n).astype(int); ii=inds%64
    coeff=master[:,:,ii[:,None,None],ii[None,:,None],ii[None,None,:]]
    k=2*np.pi*inds/L; km=np.sqrt(sum(x*x for x in np.meshgrid(k,k,k,indexing='ij')))
    mask=(km>=band[0])&(km<=band[1])
    fields=np.fft.ifftn(coeff*mask*n**3,axes=(-3,-2,-1)).real
    q=np.zeros((4,n,n,n)); v=q.copy(); q[:2]=fields[0]; v[:2]=fields[1]
    # v in conformal units is frequency weighted for a warm random wave state.
    for j in range(2):
        v[j]=np.fft.ifftn(np.fft.fftn(v[j])*np.sqrt(km**2+mp**2)).real
    # Enforce total neutral U(1) charge, without changing X's radial initial motion.
    charge=np.mean(q[0]*v[1]-q[1]*v[0]); den=np.mean(q[0]**2+q[1]**2)
    v[0]+=charge*q[1]/den; v[1]-=charge*q[0]/den
    dx=L/n
    quad=.5*np.mean(np.sum(v[:2]**2+mp**2*q[:2]**2,axis=0))
    quad+=sum(.5*np.mean(np.sum((np.roll(q[:2],1,axis=d)-q[:2])**2,axis=0))/dx**2 for d in (1,2,3))
    quart=.25*np.mean(np.sum(q[:2]**2,axis=0)**2)
    scale2=2*energy/(quad+np.sqrt(quad*quad+4*quart*energy)) if energy else 0.
    q[:2]*=np.sqrt(scale2); v[:2]*=np.sqrt(scale2)
    v[2]=mx*np.sqrt(2)*A/F
    return q,v

def run(name,n,dt,cycles,band=(.2,.8),energy=bath,coupling=c):
    q,v=initial(n,band,energy); end=round(cycles*period/dt)*dt
    ip=OUT/(name+'_initial.bin'); op=OUT/(name+'_final.bin'); hp=OUT/(name+'.csv')
    with ip.open('wb') as f:
        np.array([n,L,dt,end,0,mp,mx,coupling,1],dtype='<f8').tofile(f)
        q.astype('<f8').tofile(f); v.astype('<f8').tofile(f)
    subprocess.run([str(ROOT/'late_conversion_lattice'),str(ip),str(hp),str(op)],check=True)
    h=np.genfromtxt(hp,delimiter=',',names=True)
    ex=h['X_kinetic']+h['X_gradient']+h['X_potential']; ep=h['phi_gradient']+h['phi_kinetic_physical']+h['phi_potential']
    tail=h['z']>end-2*period
    z=h['z'][tail]; avg=lambda x:float(np.trapz(x[tail],z)/(z[-1]-z[0]))
    final=np.fromfile(op,dtype='<f8').reshape(2,4,n,n,n); qf,vf=final
    fq=np.fft.fftn(qf[:2],axes=(1,2,3))/n**3; fv=np.fft.fftn(vf[:2],axes=(1,2,3))/n**3
    ki=2*np.pi*np.fft.fftfreq(n,d=L/n); kg=np.meshgrid(ki,ki,ki,indexing='ij'); k2=sum(4*np.sin(x*L/n/2)**2/(L/n)**2 for x in kg)
    free=.5*np.sum(abs(fv)**2+(k2+mp**2)*abs(fq)**2,axis=0)
    edge=np.maximum.reduce([abs(x) for x in kg])>.6*np.pi*n/L
    # This is an energy-weighted physical wavenumber, NOT a particle speed.
    krms=np.sqrt(np.sum(free*sum(x*x for x in kg))/np.sum(free)) if free.sum() else 0
    out=dict(n=n,dt=dt,cycles=cycles,band=list(band),bath_energy_GeV4=energy*unit,
      initial_X_energy_GeV4=float(ex[0]*unit),
      mean_X_energy_loss_fraction=1-avg(ex)/ex[0],final_X_energy_loss_fraction=float(1-ex[-1]/ex[0]),
      mean_Phi_energy_gain_over_X=(avg(ep)-ep[0])/ex[0],mean_interaction_over_X=avg(h['interaction'])/ex[0],
      max_X_energy_loss_fraction=float(np.max(1-ex/ex[0])),
      mean_Phi_energy_GeV4=avg(ep)*unit,
      energy_error_over_X=float(np.max(abs(h['Econf']-h['Econf'][0]))/ex[0]),
      charge_absolute_error=float(np.max(abs(h['charge']-h['charge'][0]))),
      final_UV_free_energy_fraction=float(free[edge].sum()/free.sum()) if free.sum() else 0,
      final_energy_weighted_k_GeV=float(krms*Om),
      final_quartic_fraction=float(.25*np.mean(np.sum(qf[:2]**2,axis=0)**2)/(ep[-1])),
      time_GeV_inverse=end/Om)
    print(name,json.dumps(out),flush=True)
    return out

cases={}
for spec in [('space48',48,.02,4,(.2,.8),bath,c),('space64',64,.02,4,(.2,.8),bath,c),('hard64',64,.02,4,(.8,1.2),bath,c)]:
    cases[spec[0]]=run(*spec)
checks={
 'energy_each_below_1e-6':all(x['energy_error_over_X']<1e-6 for x in cases.values()),
 'charge_each_below_1e-8':all(x['charge_absolute_error']<1e-8 for x in cases.values()),
 'space_refinement_loss_difference_below_1e-5':abs(cases['space48']['mean_X_energy_loss_fraction']-cases['space64']['mean_X_energy_loss_fraction'])<1e-5,
 'UV_each_below_1percent':all(x['final_UV_free_energy_fraction']<.01 for x in cases.values())}
result=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),cases=cases,parameters=dict(m=m,M=M,g=g,lam=lam,A=A,a=a,Omega=Om,F=F,period=period,bath_energy_GeV4=rho,H_GeV=1.3445177278709404e10/a**2),scope='Conditional neutral warm wave families at the no-transfer late envelope. Bath radiation-energy extrapolation is a chosen test value, not an evolved late state. No quantum collision closure or relic abundance inferred.')
(OUT/'results.json').write_text(json.dumps(result,indent=2))
# A failed convergence check is retained explicitly rather than hidden.
sys.exit(0 if result['all_pass'] else 1)
