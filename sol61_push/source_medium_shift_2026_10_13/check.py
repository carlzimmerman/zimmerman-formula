"""Leading-density free-messenger response; quadratic source coupling left explicit."""
import json,math,sys
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def test(name,x):
 checks.append(dict(name=name,passed=bool(x)))
 assert x,name
w,M,A,n,lam,R=s.symbols('w M A n lam R',positive=True)
# Invariant amplitude Mcal uses vertex -iA; Pi=-n*Mcal/(2M).
amp=-A*A*(1/(w*w+2*M*w)+1/(w*w-2*M*w))
pi=s.factor(-n*amp/(2*M))
test('two crossed denominators',s.simplify(pi+n*A*A/(M*(4*M*M-w*w)))==0)
energy=n*s.sqrt(M*M+A*R+lam*R*R/2)
curvature=s.diff(energy,R,2).subs(R,0)
test('static fixed-density curvature',s.simplify(curvature-(n*lam/(2*M)-n*A*A/(4*M**3)))==0)
test('dynamic response static limit',s.simplify(s.limit(pi,w,0)+n*A*A/(4*M**3))==0)
test('linear density source tadpole',s.simplify(s.diff(energy,R).subs(R,0)-n*A/(2*M))==0)
mp.mp.dps=70
m=mp.mpf('1e6');MS=mp.mpf('1e7');MR=2*m # tiny vacuum excess kept separately
hc=mp.mpf('1.973269804e-7');nat=mp.mpf('5e24')*hc**3
mu=mp.mpf('47.41245315244753');ac=mp.mpf('2589.916240914449');delta=mp.mpf('2e-9')
U=nat/(4*m*MS);R0=-ac*nat/(2*MS*MR**2)
phi_tadpole=mu*R0/(2*m)
pi_cubic=-nat*ac**2/(MS*(4*MS**2-MR**2));shift_cubic=pi_cubic/(2*MR)
static=-nat*ac**2/(4*MS**3)/(2*MR)
slope=nat/(4*MS*MR);D0=delta-2*U
rows=[]
for coupling in ['-0.2','0','0.1','1']:
 l=mp.mpf(coupling);dm2=pi_cubic+l*nat/(2*MS)
 shift=dm2/(2*MR)
 # High precision sqrt checks the linear mass conversion; float64 would erase it.
 exact=mp.sqrt(MR**2+dm2)-MR
 test('mass conversion '+coupling,abs(shift-exact)<mp.mpf('1e-14')*max(abs(shift),mp.mpf('1e-40')))
 D=D0+shift-2*phi_tadpole
 rows.append(dict(lambda_RS=float(l),source_mass_shift_eV=float(shift),corrected_pair_excess_eV=float(D),pole_open=bool(D>0),shift_over_vacuum_total_linewidth=float(shift/mp.mpf('2e-12'))))
critical=-(D0+shift_cubic-2*phi_tadpole)/slope
result=dict(checks=checks,all_pass=all(t['passed'] for t in checks),parameters=dict(n_m3=5e24,n_natural_eV3=float(nat),U_in_eV=float(U),R_background_eV=float(R0),carrier_tadpole_shift_eV=float(phi_tadpole),source_cubic_shift_eV=float(shift_cubic),static_cubic_shift_eV=float(static),dynamic_over_static=float(shift_cubic/static),quadratic_source_shift_eV_per_lambda=float(slope),baseline_D_eV=float(D0)),rows=rows,lambda_threshold_pole_closure=float(critical),lambda_absolute_shift_for_one_vacuum_linewidth=float(mp.mpf('2e-12')/slope),opposite_mu_A_sign_D_at_lambda_zero=float(D0+shift_cubic+2*phi_tadpole),non_claims=['Leading-density free constituents only, not neutral-atom dynamic response','Other symmetry-allowed couplings and vacuum matching not fixed','Signed cubic product selected as positive in table; widths fix only magnitudes','No experimental viability or manufactured inventory'])
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
