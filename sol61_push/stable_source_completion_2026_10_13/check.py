"""Explicit tree-level scalar-potential completion; a chosen model family."""
import json,sys
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def test(name,x):
 checks.append(dict(name=name,passed=bool(x)))
 assert x,name
R,y,z,q,ss=s.symbols('R y z q ss',real=True)
m,MR,MS,mu,A,lr,ls,h,eta=s.symbols('m MR MS mu A lr ls h eta',positive=True)
lam=A*A/(2*MS*MS)+eta
expanded=m*m*y+4*m*m*z+q+lr*y*y+MR*MR*R*R/2+mu*R*y+(MS*MS+A*R+lam*R*R/2)*ss+ls*ss*ss+h*y*ss
squares=m*m*y+4*m*m*z+q+MR*MR/2*(R+mu*y/(MR*MR))**2+(lr-mu*mu/(2*MR*MR))*y*y+(MS+A*R/(2*MS))**2*ss+eta*R*R*ss/2+ls*ss*ss+h*y*ss
test('full potential identity',s.simplify(expanded-squares)==0)
test('messenger quadratic coefficient',s.simplify(s.diff(expanded,R,2).diff(ss)-lam)==0)
test('original carrier quartic preserved',s.simplify(s.diff(expanded,y,2)/2-lr)==0)
curvature=s.diff(s.sqrt(MS*MS+A*R+lam*R*R/2),R,2).subs(R,0)
test('minimal completion static curvature zero',s.simplify(curvature.subs(eta,0))==0)
mp.mp.dps=60
mv=mp.mpf('1e6');ms=mp.mpf('1e7');mr=2*mv;av=mp.mpf('2589.916240914449');muv=mp.mpf('47.41245315244753');lrv=mp.mpf('1e-6')
n=mp.mpf('5e24')*mp.mpf('1.973269804e-7')**3
lambda0=av**2/(2*ms**2);residual=lrv-muv**2/(2*mr**2)
test('remaining repulsive quartic positive',residual>0)
R0=-av*n/(2*ms*mr**2);dphi=muv*R0/(2*mv);U=n/(4*mv*ms);D0=mp.mpf('2e-9')-2*U
cubic=-n*av**2/(2*mr*ms*(4*ms**2-mr**2));slope=n/(4*ms*mr)
rows=[]
for etastr in ['0','1e-6','1e-4','1e-3']:
 et=mp.mpf(etastr);lv=lambda0+et;shift=cubic+lv*slope;D=D0+shift-2*dphi
 test('open pole eta '+etastr,D>0)
 rows.append(dict(eta=float(et),lambda_RS=float(lv),source_shift_eV=float(shift),corrected_D_eV=float(D),source_shift_over_vacuum_linewidth=float(shift/mp.mpf('2e-12'))))
result=dict(checks=checks,all_pass=all(t['passed'] for t in checks),lambda_RS_minimal_completion=float(lambda0),remaining_repulsive_quartic=float(residual),removed_quartic_fraction=float((lrv-residual)/lrv),rows=rows,non_claims=['Chosen renormalized tree potential, not symmetry-selected or data-inferred','No loop stability or naturalness certification','Medium shifts retain free-constituent and leading-density approximations','No actual messenger medium, photon source, stable inventory, or modified gravity'])
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
