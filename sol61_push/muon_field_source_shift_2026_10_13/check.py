"""Leading soft one-loop muon determinant in a prescribed magnetic field."""
import json,sys
from pathlib import Path
import sympy as s
import mpmath as mp
mp.mp.dps=90
D=mp.mpf
prior=json.loads(Path('sol61_push/ordinary_lepton_source_2026_10_13/run/results.json').read_text())['reduced_muon_case']
mag=json.loads(Path('sol61_push/muon_portal_magnetic_storage_2026_10_13/run/results.json').read_text())
y=D(str(prior['yukawa']));mu=-D(str(prior['equal_width_mu_R_phi_eV']))
alpha=1/D('137.035999084');MR=D('2e6');m=D('1e6');ml=D('105658375.5')
bconv=D(str(mag['B_eV_squared_per_tesla']));gamma=D(str(prior['photon_width_eV']))
checks=[]
def ck(name,v):
 checks.append({'name':name,'passed':bool(v)})
 assert v,name
R,A,Y,L,M,B=s.symbols('R A Y L M B',positive=True)
pot=M**2*R**2/2-A*B**2/(3*s.pi)*s.log(1+Y*R/L)
ck('linear magnetic tadpole',s.simplify(s.diff(pot,R).subs(R,0)+A*B**2*Y/(3*s.pi*L))==0)
ck('quadratic source curvature',s.simplify(s.diff(pot,R,2).subs(R,0)-M**2-A*B**2*Y**2/(3*s.pi*L**2))==0)
rows=[]
for bt in [1,10,100]:
 bn=D(bt)*bconv
 eta=alpha*y*y*bn*bn/(3*mp.pi*MR*MR*ml*ml)
 x=2*eta/(1+mp.sqrt(1+4*eta))
 r0=ml*x/y
 V=lambda r: MR*MR*r*r/2-alpha*bn*bn/(3*mp.pi)*mp.log1p(y*r/ml)
 der=MR*MR*r0-alpha*bn*bn*y/(3*mp.pi*ml*(1+x))
 ck('stationary '+str(bt),abs(der/(MR*MR*r0))<D('1e-70'))
 curv=MR*MR+alpha*bn*bn*y*y/(3*mp.pi*ml*ml*(1+x)**2)
 ck('curvature derivative '+str(bt),abs(mp.diff(V,r0,2)/curv-1)<D('1e-70'))
 # Rationalized differences preserve tiny shifts relative to MeV masses.
 ds=(curv-MR*MR)/(mp.sqrt(curv)+MR)
 U=mu*r0/(mp.sqrt(m*m+mu*r0)+m)
 ds_lead=alpha*y*y*bn*bn/(6*mp.pi*ml*ml*MR)
 U_lead=mu*alpha*y*bn*bn/(6*mp.pi*m*ml*MR*MR)
 ck('soft shift leading agreement '+str(bt),abs(ds/ds_lead-1)<D('1e-25') and abs(U/U_lead-1)<D('1e-25'))
 ck('source moves upward '+str(bt),ds>0 and U<0)
 # Lorentzian centered halfway across [-2|U|,0]; diagnostic, not capture rate.
 v=abs(U)
 weight=2/mp.pi*mp.atan(2*v/gamma)
 weight_quad=mp.quad(lambda z: v*(gamma/2)/mp.pi/((v*z)**2+(gamma/2)**2),[-1,1])
 ck('spectral window integral '+str(bt),abs(weight/weight_quad-1)<D('1e-70'))
 rows.append({'B_T':bt,'R0_eV':float(r0),'yR0_over_m_mu':float(x),
 'source_curvature_mass_shift_eV':float(ds),'daughter_shift_eV':float(U),
 'source_shift_over_well_depth':float(ds/v),
 'local_pair_excess_increase_eV':float(ds-2*U),
 'required_vacuum_delta_low_eV':float(-2*v-ds),
 'required_vacuum_delta_high_eV':float(-ds),
 'photon_width_over_pair_window':float(gamma/(2*v)),
 'centered_Lorentzian_window_weight':float(weight),
 'muon_weak_field_parameter_eB_over_m2':float(mp.sqrt(4*mp.pi*alpha)*bn/ml**2)})
ck('previous attractive shift reproduced',abs(rows[1]['daughter_shift_eV']/mag['U_10T_eV']-1)<1e-13)
result={'all_pass':all(c['passed'] for c in checks),'checks':checks,'rows':rows,
 'source_derivative_expansion_parameter_MR2_over_m_mu2':float((MR/ml)**2),
 'conventions':'m_mu(R)=m_mu+yR; mu<0 gives attraction; leading F^2 logarithmic determinant',
 'non_claims':['Static curvature is only the leading derivative approximation to the time-like pole',
 'Lorentzian interval weight is not a branching fraction or production bound',
 'No bound-state pair spectral function, global constraints, or device geometry']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
