"""Neutral two-sign weak-field comparison; no S2 halo or observational fit."""
import json
from pathlib import Path
import numpy as np
import sympy as s

dest=Path(__file__).parent/'run_v2'/'results.json'
checks={}
def exact(name,x):
    checks[name]=s.simplify(x)==0
m,n,q,G,k,gs,gx,h=s.symbols('m n q G k gs gx h',positive=True)
Ag=4*s.pi*G*m*n
Ae=q*q*n/m
C=4*s.pi*G*n
# Squared-frequency matrix for delta n_+,delta n_-; 4piG is rationalized
# gravity, and div E=q(delta n_+-delta n_-).
t=h*h*k**4/(4*m*m)
P=s.Matrix([[t+n*gs*k*k/m-Ag+Ae,n*gx*k*k/m-Ag-Ae],
            [n*gx*k*k/m-Ag-Ae,t+n*gs*k*k/m-Ag+Ae]])
T=s.Matrix([[1,1],[1,-1]])
diag=s.simplify(T*P*T/2)
wm=t+n*(gs+gx)*k*k/m-8*s.pi*G*m*n
wc=t+n*(gs-gx)*k*k/m+2*q*q*n/m
exact('mass_mode',diag[0,0]-wm)
exact('charge_mode',diag[1,1]-wc)
exact('no_linear_mode_mixing',diag[0,1]**2+diag[1,0]**2)
exact('baryon_source_has_no_charge_projection',(T*s.Matrix([C,C]))[1])
exact('critical_plasma_equals_jeans', (2*q*q*n/m-8*s.pi*G*m*n).subs(q*q,4*s.pi*G*m*m))
d,z=s.symbols('d z',positive=True)
zstar=2*m*n*d/(h*h)
poly=h*h*z*z/(4*m*m)-n*d*z/m+2*q*q*n/m
exact('fastest_k',s.diff(poly,z).subs(z,zstar))
exact('minimum',poly.subs(z,zstar)-(2*q*q*n/m-n*n*d*d/(h*h)))
exact('critical_density_threshold',(2*q*q*n/m-n*n*d*d/(h*h)).subs(q*q,4*s.pi*G*m*m).subs(n,8*s.pi*G*m*h*h/(d*d)))
# Physical dimensional comparisons; illustrative densities, not a likelihood.
GN=6.67430e-11; hb=1.054571817e-34; cc=299792458.; eV=1.602176634e-19
secGyr=365.25*86400*1e9; pc=3.085677581491367e16
physical=[]
for label,rhoGeV in [('galaxy_example',.3),('cluster_example',.035)]:
    rho=rhoGeV*1e9*eV/(cc*cc)*1e6
    op=np.sqrt(4*np.pi*GN*rho)
    physical.append(dict(label=label,density_GeV_cm3=rhoGeV,
        inverse_plasma_Gyr=1/op/secGyr,plasma_period_Gyr=2*np.pi/op/secGyr,
        comparison_330_inverse_plasma_Gyr=330/op/secGyr))
mass=1e-22*eV/(cc*cc); vd=1e5
op=np.sqrt(4*np.pi*GN*(.3*1e9*eV/(cc*cc)*1e6))
benchmark=dict(assigned_mass_eV=1e-22,assigned_demixing_speed_km_s=100,
    wavelength_pc=2*np.pi*hb/(np.sqrt(2)*mass*vd)/pc,
    inverse_growth_Myr=1/np.sqrt((mass*vd*vd/hb)**2-op*op)/(secGyr/1000),
    threshold_speed_km_s=np.sqrt(hb*op/mass)/1000)

def evolve(N,dt,gxv=2.5,mode='charge',end=7.):
    # hbar=m=n_per_sign=1, q^2=.5, 4piG=.5 -> Omega_p^2=Omega_g^2=1.
    L=np.pi; x=np.arange(N)*L/N; wave=2*np.pi*np.fft.fftfreq(N,d=L/N)
    eps=1e-4; kick=eps*np.cos(2*x)
    plus=np.sqrt(1+kick).astype(complex)
    minus=np.sqrt(1+(-kick if mode=='charge' else kick)).astype(complex)
    qv=np.sqrt(.5); gsv=.5
    kinetic=np.exp(-1j*wave*wave*dt/4)
    def potentials(p,b):
        np_,nm=np.abs(p)**2,np.abs(b)**2
        masssrc=np_+nm-np.mean(np_+nm); charge=qv*(np_-nm)
        fmass=np.fft.fft(masssrc); fcharge=np.fft.fft(charge)
        ph=np.zeros(N,complex); el=np.zeros(N,complex)
        nonzero=wave!=0
        ph[nonzero]=-.5*fmass[nonzero]/wave[nonzero]**2
        el[nonzero]=fcharge[nonzero]/wave[nonzero]**2
        phi=np.fft.ifft(ph).real; electric=np.fft.ifft(el).real
        return np_,nm,phi,electric
    def measure(p,b,time):
        np_,nm,phi,el=potentials(p,b)
        kin=.5*np.mean(np.abs(np.fft.ifft(1j*wave*np.fft.fft(p)))**2+
                         np.abs(np.fft.ifft(1j*wave*np.fft.fft(b)))**2)
        contact=np.mean(.5*gsv*(np_**2+nm**2)+gxv*np_*nm)
        grav=.5*np.mean((np_+nm-2)*phi)
        field=.5*np.mean(qv*(np_-nm)*el)
        amp=float(np.mean((np_-nm)*np.cos(2*x)))
        return dict(t=time,charge_mode=amp,mass_rms=float(np.std(np_+nm)),
            numbers=[float(np.mean(np_)),float(np.mean(nm))],
            energy=float(kin+contact+grav+field),kinetic=float(kin),
            contact=float(contact),gravity=float(grav),electric=float(field),
            min_density=float(min(np_.min(),nm.min())))
    hist=[measure(plus,minus,0)]
    for i in range(round(end/dt)):
        plus=np.fft.ifft(np.fft.fft(plus)*kinetic)
        minus=np.fft.ifft(np.fft.fft(minus)*kinetic)
        np_,nm,phi,el=potentials(plus,minus)
        plus*=np.exp(-1j*dt*(gsv*np_+gxv*nm+phi+qv*el))
        minus*=np.exp(-1j*dt*(gsv*nm+gxv*np_+phi-qv*el))
        plus=np.fft.ifft(np.fft.fft(plus)*kinetic)
        minus=np.fft.ifft(np.fft.fft(minus)*kinetic)
        if (i+1)%round(.05/dt)==0: hist.append(measure(plus,minus,(i+1)*dt))
    e0=hist[0]['energy']; n0=hist[0]['numbers']
    linear=[v for v in hist if v['t']<=2]
    w2=1+(.5-gxv)*4+4
    expected=lambda time: eps*(np.cosh(np.sqrt(-w2)*time) if w2<0 else np.cos(np.sqrt(w2)*time))
    err=max(abs(v['charge_mode']-expected(v['t']))/eps for v in linear) if mode=='charge' else 0.
    return dict(N=N,dt=dt,gx=gxv,mode=mode,end=end,
        max_number_error=max(abs(v['numbers'][j]-n0[j]) for v in hist for j in [0,1]),
        max_relative_energy_error=max(abs(v['energy']-e0)/abs(e0) for v in hist),
        linear_absolute_error_in_seed_units=err,
        max_charge_mode=max(abs(v['charge_mode']) for v in hist),
        max_mass_rms=max(v['mass_rms'] for v in hist),history=hist)
rows=[evolve(128,.002),evolve(256,.001),evolve(256,.001,gxv=.5),
      evolve(256,.001,mode='mass')]
for i,rw in enumerate(rows):
    checks[f'number_conservation_{i}']=rw['max_number_error']<1e-9
    checks[f'energy_conservation_{i}']=rw['max_relative_energy_error']<1e-4
    if rw['mode']=='charge': checks[f'linear_prediction_{i}']=rw['linear_absolute_error_in_seed_units']<.01
checks['charge_amplification']=rows[1]['max_charge_mode']>.1
checks['stable_contact_control']=rows[2]['max_charge_mode']<.001
checks['mass_drive_no_charge']=rows[3]['max_charge_mode']<1e-10
checks['resolution_peak']=abs(rows[0]['max_charge_mode']/rows[1]['max_charge_mode']-1)<.01
checks={key:bool(value) for key,value in checks.items()}
result=dict(exact_and_finite_checks=checks,physical_examples=physical,demixing_benchmark=benchmark,
    runs=rows,nonclaims=['Not a MOND halo','Not production from vacuum',
    'Not an observed dark plasma','No cluster exclusion','No finite-temperature phase diagram',
    'Periodic Newtonian electrostatic comparison; no covariant completion'])
dest.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:value for key,value in result.items() if key!='runs'},indent=2))
print(json.dumps([{key:value for key,value in row.items() if key!='history'} for row in rows],indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
