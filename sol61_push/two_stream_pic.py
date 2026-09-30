#!/usr/bin/env python3
"""1D periodic electrostatic PIC: actual nonlinear stream-to-field energy transfer.

Normalized electron q/m=-1, epsilon=1, total number density=1, v=+/-1.
Fixed neutralizing background, CIC deposit/interpolation, spectral Poisson,
kick-drift-kick. This is a charged-plasma analogy, not dark MOND dynamics.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np


def evolve(k,grid,particles,dt,seed,end=80,tracked_mode=1,seed_harmonics=1):
    length=2*math.pi/k; dx=length/grid
    half=particles//2
    base=(np.arange(half)+.5)*length/half
    positions=np.tile(base,2)
    shift=np.zeros_like(positions)
    for harmonic in range(1,seed_harmonics+1):
        phase=0. if seed_harmonics==1 else math.sqrt(2)*harmonic**2
        shift+=(seed/(math.sqrt(seed_harmonics)*k*harmonic))*np.sin(k*harmonic*positions+phase)
    positions=(positions+shift)%length
    velocities=np.r_[np.ones(half),-np.ones(half)]
    waves=2*math.pi*np.fft.fftfreq(grid,d=dx)
    def field(pos):
        cell=pos/dx; index=np.floor(cell).astype(int)%grid; frac=cell-np.floor(cell)
        density=(np.bincount(index,weights=1-frac,minlength=grid)+np.bincount((index+1)%grid,weights=frac,minlength=grid))*grid/particles
        charge=1-density
        modes=np.fft.fft(charge)
        e_modes=np.zeros(grid,dtype=complex)
        use=waves!=0
        e_modes[use]=modes[use]/(1j*waves[use])
        # Nyquist derivative has no real-grid representation; set it to zero.
        e_modes[grid//2]=0
        e_grid=np.fft.ifft(e_modes).real
        force=-(e_grid[index]*(1-frac)+e_grid[(index+1)%grid]*frac)
        return force,e_grid,density
    force,E,density=field(positions)
    history=[]
    def record(t):
        kinetic=.5*float(np.mean(velocities**2)); electric=.5*float(np.mean(E**2))
        fundamental=2*abs(np.fft.fft(E)[1])/grid
        selected=2*abs(np.fft.fft(E)[tracked_mode])/grid
        history.append(dict(t=float(t),field_fundamental=float(fundamental),tracked_mode_field=float(selected),electric_energy=electric,kinetic_energy=kinetic,total_energy=kinetic+electric,density_mean=float(np.mean(density))))
    record(0)
    steps=int(round(end/dt)); stride=max(1,int(round(.2/dt)))
    for n in range(steps):
        velocities+=force*dt/2
        positions=(positions+velocities*dt)%length
        force,E,density=field(positions)
        velocities+=force*dt/2
        if (n+1)%stride==0: record((n+1)*dt)
    t=np.array([h['t'] for h in history]); amp=np.array([h['tracked_mode_field'] for h in history])
    total=np.array([h['total_energy'] for h in history])
    fit=(t>=8)&(t<=18)
    growth=float(np.polyfit(t[fit],np.log(np.maximum(amp[fit],1e-30)),1)[0])
    # The quiet displacement seeds BOTH the growing and oscillatory modes,
    # rather than the pure growing eigenvector used in the matrix check.
    kv=k*tracked_mode
    low=kv*kv+.5-.5*math.sqrt(1+8*kv*kv)
    high=kv*kv+.5+.5*math.sqrt(1+8*kv*kv)
    fraction=(high-kv*kv-1)/(high-low)
    mode_low=np.cosh(math.sqrt(-low)*t[fit]) if low<0 else np.cos(math.sqrt(low)*t[fit])
    exact_quiet=fraction*mode_low+(1-fraction)*np.cos(math.sqrt(high)*t[fit])
    quiet_fit=float(np.polyfit(t[fit],np.log(np.maximum(np.abs(exact_quiet),1e-30)),1)[0])
    peak=None
    for i in range(1,len(t)-1):
        if t[i]>18 and amp[i]>.02 and amp[i]>amp[i-1] and amp[i]>=amp[i+1]:
            peak=dict(t=float(t[i]),field_amplitude=float(amp[i]),bounce_frequency=math.sqrt(k*tracked_mode*amp[i]),electric_energy=history[i]['electric_energy'],kinetic_energy=history[i]['kinetic_energy'])
            break
    return dict(k=k,grid=grid,particles=particles,dt=dt,seed=seed,length=length,end=end,tracked_mode=tracked_mode,seed_harmonics=seed_harmonics,
                growth_fit=growth,exact_linear_quiet_start_fit=quiet_fit,first_nonlinear_peak=peak,max_field=float(np.max(amp)),
                relative_energy_drift=float(np.max(np.abs(total-total[0]))/total[0]),
                max_density_mean_error=max(abs(h['density_mean']-1) for h in history),history=history)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); rows=[]; checks=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}",flush=True)
    k=math.sqrt(3/8); gamma=1/(2*math.sqrt(2))
    cases=[('coarse',k,256,4096,.04,1e-4,1,1),('fine',k,512,16384,.02,1e-4,1,1),
           ('seed_changed',k,512,16384,.02,2e-4,1,1),('stable_control',1.2,512,16384,.02,1e-4,1,1),
           ('multimode_larger_box',k/4,1024,32768,.02,1e-4,4,8)]
    for name,kk,ng,np_,dt,seed,mode,harmonics in cases:
        r=evolve(kk,ng,np_,dt,seed,tracked_mode=mode,seed_harmonics=harmonics); r['name']=name; rows.append(r)
        check('number_conservation_'+name,r['max_density_mean_error']<1e-12,f'error={r["max_density_mean_error"]:.8g}')
        check('energy_transfer_budget_'+name,r['relative_energy_drift']<.005,f'max drift={r["relative_energy_drift"]:.8g}; kinetic+electric energy, fixed uniform neutralizer')
        if name!='stable_control':
            check('linear_growth_'+name,abs(r['growth_fit']/gamma-1)<.05,f'fit={r["growth_fit"]:.8g}, analytic={gamma:.8g}')
            check('quiet_start_transient_benchmark_'+name,abs(r['growth_fit']/r['exact_linear_quiet_start_fit']-1)<.01,f'PIC fit={r["growth_fit"]:.10g}, exact mixed-mode finite-window fit={r["exact_linear_quiet_start_fit"]:.10g}')
            check('nonlinear_field_from_stream_'+name,r['first_nonlinear_peak'] is not None and r['max_field']>.1,f'first peak={r["first_nonlinear_peak"]}; finite noise, no imposed pump phase')
        else:
            check('stable_wavelength_control',r['max_field']<.005,f'max field={r["max_field"]:.8g}; every box harmonic has kv>Omega_p')
    coarse,fine,changed=rows[:3]
    peak1=fine['first_nonlinear_peak']; peak0=coarse['first_nonlinear_peak']; peak2=changed['first_nonlinear_peak']
    resolution=abs(peak1['field_amplitude']/peak0['field_amplitude']-1) if peak1 and peak0 else math.inf
    seed_difference=abs(peak2['field_amplitude']/peak1['field_amplitude']-1) if peak1 and peak2 else math.inf
    check('saturation_resolution_check',resolution<.10,f'first-peak amplitude resolution difference={resolution:.8g}')
    check('saturation_seed_check',seed_difference<.10,f'doubling tiny seed changes first-peak amplitude by {seed_difference:.8g}; this is one distribution/box, not universality')
    if peak1:
        ratio=peak1['bounce_frequency']/gamma
        print(f'OBSERVATION bounce_frequency/gamma_at_first_peak={ratio:.10g}; the assumption of equality is not imposed.',flush=True)
    else: ratio=None
    data=dict(checks=checks,rows=rows,first_peak_bounce_to_linear_growth=ratio,
              verdict='Charged-stream kinetic energy can drive nonlinear oscillations without a supplied amplitude. No mapping to a MOND scale or 32pi is established.',
              non_claims=['Electrostatic 1D periodic plasma, not the non-Abelian dark medium','One cold distribution; two box sizes and bounded numerical refinement','First peak is not a stationary attractor','Grid PIC is approximate; refinement is bounded','No galaxy field or vacuum-energy calculation','No exact saturation coefficient or chirality selection'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not x['passed'] for x in checks)
    print(f'{len(checks)-failed}/{len(checks)} checks pass; theory and coefficient OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
