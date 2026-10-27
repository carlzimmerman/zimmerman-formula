"""Harmonic coherent elastic recoil audit, not a material response calculation."""
import json
import math
from pathlib import Path
import sys

import mpmath as mp
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
previous=json.loads((ROOT/'sol61_push/cold_primakoff_target_2026_10_14/run_covariant/results.json').read_text())
MT=previous['parameters']['target_mass_eV']
Q=2e6  # leading momentum transfer for photon -> nearly resting 2 MeV scalar
hc=1.973269804e-7
kB=8.617333262e-5
N=1e23
recoil=Q*Q/(2*MT)
checks=[]


def check(name,value):
    checks.append({'name':name,'passed':bool(value)})
    assert value,name


# Independent thermal number-state sum. <n|exp(iQx)|n>=exp(-eta/2)L_n(eta).
# eta=Q^2/(2M Omega), z=exp(-Omega/kT). This validates the thermal AMPLITUDE,
# not a claim that its square is the entire elastic/inelastic rate fraction.
mp.mp.dps=80
oscillator_checks=[]
for eta_string in ['0.1','1','5']:
    eta=mp.mpf(eta_string)
    for z_string in ['0.1','0.5','0.8']:
        z=mp.mpf(z_string)
        Lprev=mp.mpf(1); Lcur=1-eta
        total=Lprev+z*Lcur
        for n in range(2,601):
            Lnext=((2*n-1-eta)*Lcur-(n-1)*Lprev)/n
            total+=z**n*Lnext
            Lprev,Lcur=Lcur,Lnext
        numeric=(1-z)*mp.exp(-eta/2)*total
        exact=mp.exp(-eta*(1+z)/(2*(1-z)))
        error=abs(numeric/exact-1)
        check('thermal oscillator characteristic '+str((eta_string,z_string)),error<mp.mpf('1e-40'))
        oscillator_checks.append({'eta':float(eta),'z':float(z),'relative_error':float(error)})

rows=[]
for phonon_energy in [.01,.03,.1]:
    for temperature in [0.,4.,300.]:
        coth=1. if temperature==0 else 1/math.tanh(phonon_energy/(2*kB*temperature))
        exponent=recoil/phonon_energy*coth
        sigma=hc*math.sqrt(coth/(2*MT*phonon_energy))
        check('displacement and recoil expressions '+str((phonon_energy,temperature)),
              abs((Q*sigma/hc)**2/exponent-1)<1e-13)
        log_f=-exponent/math.log(10)
        rows.append({'phonon_energy_eV':phonon_energy,'temperature_K':temperature,
                     'projected_rms_displacement_m':sigma,'minus_log_f_coherent':exponent,
                     'log10_f_coherent':log_f,'log10_max_coherent_peak_over_N':math.log10(N)+log_f})

# Independent finite Fourier examples of integrated lattice structure factors.
# Grid has at least N sites, so no two occupied lattice sites alias.
fourier=[]
for n,grid in [(3,32),(17,128),(64,512)]:
    occupied=np.zeros(grid,dtype=complex); occupied[:n]=1
    structure=np.abs(np.fft.fft(occupied))**2
    check('lattice integrated structure '+str(n),abs(float(structure.mean())/n-1)<1e-13)
    check('lattice peak '+str(n),abs(float(structure.max())/(n*n)-1)<1e-13)
    fourier.append({'N':n,'momentum_samples':grid,'mean_structure':float(structure.mean()),
                    'max_structure':float(structure.max())})

required_sigma=hc/Q*math.sqrt(math.log(N))
required_phonon=recoil/math.log(N)
check('necessary zero-temperature stiffness boundary',abs(N*math.exp(-recoil/required_phonon)-1)<1e-13)
out={'all_pass':all(c['passed'] for c in checks),'checks':checks,
     'parameters':{'target_mass_eV':MT,'momentum_transfer_eV':Q,'coherent_site_count_assumed':N,
                   'recoil_energy_eV':recoil,'kb_eV_per_K':kB},
     'thermal_amplitude_controls':oscillator_checks,'rows':rows,'fourier_controls':fourier,
     'max_projected_rms_for_peak_equal_N_m':required_sigma,
     'min_zero_temperature_phonon_energy_for_peak_equal_N_eV':required_phonon,
     'non_claims':['Harmonic mode energies assigned, not a measured crystal phonon spectrum',
                   'Coherent elastic component only; no inclusive phonon-assisted cold rate',
                   'Peak structure factors are not integrated production gains',
                   'No universal bound for all materials or proof of a manufacturing protocol']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
