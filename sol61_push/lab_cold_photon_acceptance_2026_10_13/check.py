"""Laboratory-frame cold acceptance of an assumed narrow scalar pole.

Gaussian independent beam errors, near-head-on kinematics, CW overlap only.
"""
import json
import math
from pathlib import Path
import sys

import mpmath as mp
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[2]
source=json.loads((ROOT/'sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())
pole=json.loads((ROOT/'sol61_push/threshold_resonance_2026_10_13/run/results.json').read_text())
m=1e6
delta=pole['parameters']['resonance_excess_eV']
width=source['reduced_muon_case']['photon_width_eV']
sigma_peak=pole['parameters']['peak_sigma_m2']
Kstar=delta/2
Kcut=1e-8  # chosen laboratory kinetic-energy ceiling for EACH daughter
r=math.sqrt(2*m*Kstar)
R=math.sqrt(2*m*Kcut)
P_all=2*(R-r)
P_max=2*math.sqrt(R*R-r*r)
checks=[]


def check(name,condition):
    checks.append({'name':name,'passed':bool(condition)})
    assert condition,name


def acceptance(P):
    if P<=P_all:
        return 1.0
    if P>=P_max:
        return 0.0
    q=P/2
    return (R*R-r*r-q*q)/(2*q*r)


def cold_fraction(sz,st):
    if st==0:
        return 2/(math.sqrt(2*math.pi)*sz)*quad(
            lambda P:math.exp(-P*P/(2*sz*sz))*acceptance(P),0,P_max,
            points=[P_all],epsabs=1e-12,epsrel=1e-10)[0]
    norm=1/((2*math.pi)**1.5*sz*st*st)
    def radial(P):
        angular=2*quad(lambda u:math.exp(-P*P*((1-u*u)/st**2+u*u/sz**2)/2),
                       0,1,epsabs=1e-12,epsrel=1e-10)[0]
        return P*P*acceptance(P)*angular
    return 2*math.pi*norm*quad(radial,0,P_max,points=[P_all],epsabs=1e-12,epsrel=1e-9)[0]


# Independent geometric control: intersection of two spheres for q=P/2.
volume=4*math.pi*quad(lambda P:P*P*acceptance(P),0,P_max,points=[P_all],epsabs=1e-13)[0]
lens=16*math.pi/3*(2*R+r)*(R-r)**2
check('accepted momentum volume matches sphere intersection',abs(volume/lens-1)<1e-12)

# High-precision Lorentz transformation independently checks the NR energy cut.
mp.mp.dps=65
mm=mp.mpf(str(m)); dd=mp.mpf(str(delta)); MR=2*mm+dd
pstar=mp.sqrt((MR/2)**2-mm**2)
max_energy_error=mp.mpf(0)
for Pfactor in [.2,.7,1.,1.2]:
    P=mp.mpf(str(Pfactor*P_max))
    for u in [-1,0,.4,1]:
        exact=mp.sqrt(MR*MR+P*P)/2-mm+P*pstar/MR*u
        approximate=dd/2+P*P/(8*mm)+P*mp.sqrt(mm*dd)/(2*mm)*u
        max_energy_error=max(max_energy_error,abs(exact-approximate))
check('NR daughter energies versus exact Lorentz transformation',max_energy_error/mp.mpf(str(Kcut))<mp.mpf('1e-11'))

# Independent numerical pole area in dimensionless detuning: sigma/peak=1/(1+x^2).
area=sigma_peak*math.pi*width
area_numeric=sigma_peak*width*quad(lambda x:1/(1+x*x),-math.inf,math.inf,epsabs=1e-12)[0]
check('constant-width narrow pole area',abs(area_numeric/area-1)<1e-12)

sigma_E=5000.0  # ASSUMED per-beam RMS; not an interpretation of a quoted FWHM
sz=math.sqrt(2)*sigma_E
sigma_sum=sz
averaged_sigma=area/(math.sqrt(2*math.pi)*sigma_sum)
flux=1e8  # assumed photons/s in each of two otherwise unspecified beams
beam_area=1e-6
length=.002
c=299792458.
luminosity=2*length*flux*flux/(beam_area*c)
uncut_rate=luminosity*averaged_sigma
rows=[]
for angular_sigma in [0,1e-8,1e-7,1e-6,1e-5,1e-3]:
    st=m*angular_sigma
    fraction=cold_fraction(sz,st)
    check('acceptance probability range '+str(angular_sigma),0<fraction<=1)
    rows.append({'net_misalignment_component_rms_rad':angular_sigma,
                 'transverse_total_momentum_component_rms_eV':st,
                 'both_daughters_cold_fraction':fraction,
                 'cold_pairs_per_s_CW_benchmark':uncut_rate*fraction})

# In the broad transverse-distribution limit, its density is essentially
# constant throughout the accepted momentum lens.
asymptotic=volume/((2*math.pi)**1.5*sz*(m*1e-3)**2)
check('broad momentum distribution geometric limit',abs(rows[-1]['both_daughters_cold_fraction']/asymptotic-1)<1e-7)
check('transverse spread suppresses accepted fraction',all(rows[j+1]['both_daughters_cold_fraction']<rows[j]['both_daughters_cold_fraction'] for j in range(len(rows)-1)))

result={'all_pass':all(c['passed'] for c in checks),'checks':checks,
        'parameters':{'m_eV':m,'pole_excess_eV':delta,'Kstar_eV':Kstar,'Kcut_each_eV':Kcut,
                      'gamma_each_eV':width,'per_beam_energy_rms_eV':sigma_E,
                      'each_beam_flux_per_s':flux,'beam_area_m2':beam_area,'overlap_length_m':length},
        'all_angles_accepted_P_eV':P_all,'any_angle_accepted_P_eV':P_max,
        'accepted_momentum_volume_eV3':volume,'max_NR_energy_error_eV':float(max_energy_error),
        'narrow_pole_area_m2_eV':area,'bandwidth_averaged_sigma_m2':averaged_sigma,
        'CW_luminosity_per_m2_s':luminosity,'uncut_pairs_per_s_CW_benchmark':uncut_rate,
        'rows':rows,'non_claims':['Gaussian independent errors and assumed CW overlap are not a real source joint phase-space distribution',
                                'Leading narrow-pole approximation; no full off-shell, source feasibility or background calculation',
                                'No trapping, charge separation, detector efficiency or verified particles',
                                'Published source specifications cited in report are contextual, not inputs proving these two beams exist']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
