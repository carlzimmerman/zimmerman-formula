"""Alternative source matching through known charged leptons; hypothetical scalar Yukawas."""
import json,math,sys
from pathlib import Path
import mpmath as mp
from scipy.integrate import quad
checks=[]
def test(name,x):
 checks.append(dict(name=name,passed=bool(x)))
 assert x,name
mp.mp.dps=60
alpha=mp.mpf(1)/mp.mpf('137.035999084');MR=mp.mpf('2e6');hb=mp.mpf('6.582119569e-16');target=mp.mpf('1e-12')
def form(tau):
 if tau<=1:f=mp.asin(mp.sqrt(tau))**2
 else:f=-(mp.log((1+mp.sqrt(1-1/tau))/(1-mp.sqrt(1-1/tau)))-1j*mp.pi)**2/4
 return 2*(tau+(tau-1)*f)/tau**2
# Primary source uses x=1/tau and half of A_1/2; independently check translation.
for tau in [mp.mpf('.0001'),mp.mpf('.25'),mp.mpf('3.8')]:
 x=1/tau
 f=mp.asin(1/mp.sqrt(x))**2 if x>1 else -(mp.log((1+mp.sqrt(1-x))/(1-mp.sqrt(1-x)))-1j*mp.pi)**2/4
 test('loop convention '+str(tau),abs(form(tau)-2*x*(1+(1-x)*f))<mp.mpf('1e-45'))
test('heavy lepton limit',abs(form(mp.mpf('1e-12'))/(mp.mpf(4)/3)-1)<mp.mpf('1e-12'))
def gamma_coeff(ml):return alpha**2*MR**3/(256*mp.pi**3*ml**2)*abs(form(MR**2/(4*ml**2)))**2
def da(ml,y):
 r=float(MR/ml)
 f=lambda z:(1-z)**2*(1+z)/((1-z)**2+r*r*z)
 direct=quad(f,0,1,epsabs=1e-12,epsrel=1e-11)[0]
 independent=mp.quad(lambda z:(1-z)**2*(1+z)/((1-z)**2+(MR/ml)**2*z),[0,.5,.9,.99,1])
 test('moment integral '+str(ml)+' '+str(y),abs(direct/float(independent)-1)<1e-9)
 return float(y*y/(8*mp.pi**2)*independent)
rows=[]
for name,ml in [('electron',mp.mpf('510998.95')),('muon',mp.mpf('105658375.5'))]:
 coeff=gamma_coeff(ml);y=mp.sqrt(target/coeff)
 beta2=1-4*ml**2/MR**2
 charged= y*y*MR/(8*mp.pi)*beta2**mp.mpf('1.5') if beta2>0 else mp.mpf(0)
 total=2*target+charged
 test('target photon width '+name,abs(coeff*y*y/target-1)<mp.mpf('1e-45'))
 rows.append(dict(loop=name,yukawa=float(y),photon_width_eV=float(target),charged_pair_width_eV=float(charged),carrier_branch=float(target/total),total_width_eV=float(total),rest_lifetime_s=float(hb/total),pole_cross_section_over_old_equal_width=float((2*target/total)**2),delta_a_lepton=da(ml,y)))
# A lower muon coupling is a diagnostic choice, not a best fit or allowed point.
ml=mp.mpf('105658375.5');y=mp.mpf('2e-4');gam=gamma_coeff(ml)*y*y;moment=da(ml,y)
reduced=dict(yukawa=float(y),photon_width_eV=float(gam),equal_width_mu_R_phi_eV=float(mp.mpf('47.41245315244753')*mp.sqrt(gam/target)),equal_width_broad_spectrum_area_over_original=float(gam/target),delta_a_muon=moment,residual_over_2025_reference_sigma=(moment-38e-11)/(63e-11),rest_lifetime_if_equal_carrier_width_s=float(hb/(2*gam)))
out=dict(checks=checks,all_pass=all(t['passed'] for t in checks),rows=rows,reduced_muon_case=reduced,reference_2025=dict(exp_minus_SM=38e-11,sigma=63e-11,source='https://arxiv.org/abs/2505.21476'),non_claims=['New neutral scalar Yukawas, not Standard Model production','Muon reference comparison is not a global allowed-region fit','No mediator constraints, cosmology, full electroweak completion or confinement','Electron effective two-photon amplitude is complex above threshold'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
