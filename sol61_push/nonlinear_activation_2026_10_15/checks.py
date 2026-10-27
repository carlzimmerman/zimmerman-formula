"""Floquet test of an assigned damped Mathieu oscillator, not a dark device."""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

p=Path(__file__).parent
Q=1000.; period=math.pi
rows=[]
for h in [0., .001, .002, .02]:
    def rhs(t,z):
        M=z.reshape(2,2)
        A=np.array([[0.,1.],[-(1+h*math.cos(2*t)),-1/Q]])
        return (A@M).reshape(4)
    sol=solve_ivp(rhs,[0,period],np.eye(2).reshape(4),method='DOP853',rtol=1e-12,atol=1e-14)
    M=sol.y[:,-1].reshape(2,2)
    rate=math.log(max(abs(np.linalg.eigvals(M))))/period
    approx=h/4-1/(2*Q)
    expected_det=math.exp(-period/Q)
    assert abs(np.linalg.det(M)-expected_det)<2e-11
    rows.append({'h_assigned':h,'Q_dark_assigned':Q,'growth_per_omega0_exact_numerical':rate,'small_modulation_approximation':approx})
assert rows[0]['growth_per_omega0_exact_numerical']<0
assert rows[1]['growth_per_omega0_exact_numerical']<0
assert rows[3]['growth_per_omega0_exact_numerical']>0
assert abs(rows[3]['growth_per_omega0_exact_numerical']-rows[3]['small_modulation_approximation'])<2e-7
c=299792458.; hbar_eVs=6.582119569e-16
result={'model':'a_ddot+omega0/Q*a_dot+omega0^2*(1+h*cos(2omega0*t))*a=0',
 'rows':rows,'determinant_check':'all four monodromies satisfy Liouville determinant within 2e-11',
 'illustrative_f_84Hz_h_002_Q1000_amplitude_efold_s':1/(rows[3]['growth_per_omega0_exact_numerical']*2*math.pi*84),
 'dirichlet_sphere_R_1m_relativistic_gradient_energy_eV':math.pi*hbar_eVs*c,
 'nonclaims':['No measured dark mode, coupling, confinement, Q or saturation','EM cavity Q is not dark mode Q','Growth consumes pump energy','No thrust or density accumulation calculated']}
(p/'run_v1/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
