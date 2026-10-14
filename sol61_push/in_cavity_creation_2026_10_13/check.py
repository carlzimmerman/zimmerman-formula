"""Static prescribed wall, planar subbarrier leakage, ideal photon-beam yield."""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
checks=[]
def test(name,x):
 checks.append({'name':name,'passed':bool(x)});assert x,name
# Dimensionless independent Schrödinger transfer-matrix integration.
for E in [.1,.5,.9]:
 for width in [.3,1.,3.]:
  k=math.sqrt(E);kap=math.sqrt(1-E)
  A=np.array([[0.,1.],[1-E,0.]])
  sol=solve_ivp(lambda x,y:(A@y.reshape(2,2)).ravel(),(0,width),np.eye(2).ravel(),rtol=1e-11,atol=1e-12)
  P=sol.y[:,-1].reshape(2,2)
  amp=2j*k*np.exp(-1j*k*width)/(1j*k*(P[0,0]+P[1,1])+k*k*P[0,1]-P[1,0])
  exact=1/(1+math.sinh(kap*width)**2/(4*E*(1-E)))
  test('transfer '+str((E,width)),sol.success and abs(abs(amp)**2/exact-1)<1e-9)
hc=1.973269804e-7;hb=6.582119569e-16;c=299792458.;ev=1.602176634e-19
m=1e6;M=1e7;nS=1e25;h=1.;U=h*nS*hc**3/(4*m*M);C=-(1/137.035999084)*h/(48*math.pi*M*M)
rows=[]
# K stored separately: adding neV to 1 MeV loses accuracy in ordinary float64.
for K in [1e-10,1e-9,1.8e-9]:
 beta=math.sqrt(K*(2*m+K))/(m+K);velocity=c*beta
 for width in [1e-5,1e-4]:
  z=math.sqrt(2*m*(U-K))*width/hc
  T=1/(1+U*U*math.sinh(z)**2/(4*K*(U-K)))
  rows.append({'K_eV':K,'width_m':width,'kappa_width':z,'planar_transmission':T,'velocity_m_s':velocity})
K=1e-9;E=m+K;beta=math.sqrt(K*(2*m+K))/E
sig=C*C*(4*E*E)*beta/(8*math.pi)*hc*hc
power=1e6;area=1e-6;length=.002;volume=area*length
ng=power/(area*E*ev*c);rate=2*c*ng*ng*sig*volume
bench={'m_eV':m,'messenger_mass_eV':M,'nS_m3':nS,'U_wall_eV':U,'C_eVminus2':C,'K_eV':K,'production_sigma_m2':sig,'per_beam_power_W':power,'beam_area_m2':area,'overlap_length_m':length,'ideal_pair_rate_s_inv':rate,'mean_wait_years':1/rate/(365.25*86400),'relative_excess_photon_energy_K_over_m':K/m,'hbar_over_K_seconds':hb/K,'one_dimensional_1mm_box_ground_energy_eV':math.pi**2*hc*hc/(2*m*.001**2)}
test('all subbarrier',all(row['K_eV']<U for row in rows))
test('free-space threshold approximates weakly shifted cavity modes',bench['one_dimensional_1mm_box_ground_energy_eV']<K/1000)
# At fixed energy and beam geometry pair rate scales as product of beam powers.
test('photon flux energy accounting',math.isclose(ng*c*area*E*ev,power,rel_tol=1e-12))
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'barriers':rows,'benchmark':bench,'non_claims':['Prescribed static wall, not physical reservoir solution','Planar single-event leakage is not a 3D lifetime','Beam bandwidth and reservoir stability not realized; ideal event rate is not measured']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
