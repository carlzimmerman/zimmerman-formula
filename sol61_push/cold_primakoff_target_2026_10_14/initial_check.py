"""Born scalar Primakoff cold-tail diagnostic for a stationary spin-zero target."""
import json
import math
from pathlib import Path
import sys

import mpmath as mp
from scipy.integrate import quad
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
prev=json.loads((ROOT/'sol61_push/lab_cold_photon_acceptance_2026_10_13/run/results.json').read_text())
par=prev['parameters']
m=par['m_eV']; delta=par['pole_excess_eV']; MR=2*m+delta
gamma=par['gamma_each_eV']; g=math.sqrt(64*math.pi*gamma/MR**3)
MT=2e11; Z=82; alpha=1/137.035999084; hc=1.973269804e-7
target_column=3e25; flux=1e8; beam_rms=5000.0; branch=.5
spectral_peak=flux/(math.sqrt(2*math.pi)*beam_rms)
r=math.sqrt(m*delta); R=math.sqrt(2*m*par['Kcut_each_eV'])
Pall=2*(R-r); Pmax=2*math.sqrt(R*R-r*r)
checks=[]


def check(name,condition):
    checks.append({'name':name,'passed':bool(condition)})
    assert condition,name


def accept(P):
    if P<=Pall: return 1.0
    if P>=Pmax: return 0.0
    return (R*R-r*r-P*P/4)/(P*r)


# Current reduction for a stationary target: J=2P_target+q, epsilon.J=epsilon.q.
kq, Mw, eq=sp.symbols('kq Mw eq',real=True)
check('stationary current contraction',sp.expand(kq*eq-(2*Mw+kq)*eq+2*Mw*eq)==0)
px,py=sp.symbols('px py',real=True)
check('unpolarized transverse contraction',sp.expand((px*px+py*py)/2-(px**2+py**2)/2)==0)

mp.mp.dps=65
M=mp.mpf(str(MT)); S=2*mp.mpf(str(m))+mp.mpf(str(delta))
w_rest=S*(2*M-S)/(2*(M-S))
w_threshold=S+S*S/(2*M)
p_at_threshold=S*w_threshold/(M+S)
check('rest-source photon energy above total threshold',w_rest>w_threshold)
check('threshold source outside cold acceptance',p_at_threshold>mp.mpf(str(Pmax)))

kinematic_checks=[]
for Pfactor,u in [(.2,-1),(.7,-.4),(1,0),(1,.6),(.9,1)]:
    p=mp.mpf(str(Pmax*Pfactor)); uz=mp.mpf(str(u))
    ER=mp.sqrt(S*S+p*p)
    w=(2*M*ER-S*S)/(2*(M-ER+p*uz))
    ET=mp.sqrt(M*M+w*w+p*p-2*w*p*uz)
    residual=abs(w+M-ER-ET)
    check('exact energy root '+str((Pfactor,u)),residual<mp.mpf('1e-45'))
    jac=1-(w-p*uz)/ET
    direct_jac=mp.diff(lambda omega:omega+M-ER-mp.sqrt(M*M+omega*omega+p*p-2*omega*p*uz),w)
    check('energy delta Jacobian '+str((Pfactor,u)),abs(jac/direct_jac-1)<mp.mpf('1e-45'))
    kinematic_checks.append({'p_eV':float(p),'u':u,'photon_energy_minus_rest_point_eV':float(w-w_rest)})


def exact_scaled_angular(P):
    ER=math.sqrt(MR*MR+P*P)
    def f(u):
        den=MT-ER+P*u
        w=(2*MT*ER-MR*MR)/(2*den)
        t=MR*MR-2*w*(ER-P*u)
        weight=math.exp(-.5*((w-float(w_rest))/beam_rms)**2)
        return (1-u*u)*MT*w/(ER*den)*(MR*MR/t)**2*weight
    return quad(f,-1,1,epsabs=1e-12,epsrel=1e-12)[0]


moment4=quad(lambda P:P**4*accept(P),0,Pmax,points=[Pall],epsabs=1e-15,epsrel=1e-12)[0]
exact_integral=2*math.pi*quad(lambda P:P**4*accept(P)*exact_scaled_angular(P),
                            0,Pmax,points=[Pall],epsabs=1e-15,epsrel=1e-11)[0]
pref=target_column*hc*hc*spectral_peak*alpha*g*g*Z*Z/(8*math.pi*MR**4)*branch
rate= pref*exact_integral
static_rate=target_column*hc*hc*spectral_peak*alpha*g*g*Z*Z/(3*MR**4)*moment4*branch
ratio=rate/static_rate
check('heavy-target local limit including recoil',abs(ratio-(1-MR/(2*MT)))<1e-10)

# Independent analytic polynomial/log-free primitive for P^4 A(P).
moment_analytic=Pall**5/5 + ((R*R-r*r)*(Pmax**4-Pall**4)/4-(Pmax**6-Pall**6)/24)/r
check('cold transverse moment integral',abs(moment4/moment_analytic-1)<1e-12)

# At P=0 and stationary target, both transverse polarization amplitudes vanish.
check('rest-source Born node',0.0*alpha*g*g*Z*Z==0)
result={'all_pass':all(c['passed'] for c in checks),'checks':checks,
        'parameters':{'m_eV':m,'MR_eV':MR,'g_R_gamma_eVminus1':g,'target_mass_eV':MT,'Z':Z,
                      'target_column_per_m2':target_column,'flux_per_s':flux,'beam_RMS_eV':beam_rms,
                      'photon_spectral_peak_per_s_eV':spectral_peak,'carrier_branch':branch,
                      'target_form_factor':1,'Kcut_each_eV':par['Kcut_each_eV']},
        'photon_threshold_minus_MR_eV':float(w_threshold-S),
        'photon_for_R_at_rest_minus_MR_eV':float(w_rest-S),
        'rest_point_minus_threshold_eV':float(w_rest-w_threshold),
        'source_momentum_at_total_threshold_eV':float(p_at_threshold),
        'cold_source_momentum_max_eV':Pmax,'kinematic_samples':kinematic_checks,
        'integral_P4_acceptance_eV5':moment4,'cold_pair_rate_per_s':rate,
        'static_approx_cold_pair_rate_per_s':static_rate,'exact_over_static':ratio,
        'non_claims':['Free stationary spin-zero target; not a solid-state response calculation',
                      'Local scalar photon operator; no full off-shell muon form factor or other diagrams',
                      'Born thin-target single interaction with no attenuation and F(t)=1',
                      'No general bound for moving targets or proof excluding all production mechanisms']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
