"""Cubic static response with a dynamical charged-host clock.
Compares adiabatic low-energy and canonical principal clock coefficients.
"""
import json,sys,math
from pathlib import Path
import sympy as s
import mpmath as mp
out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
parent=json.loads((base/'mediator_phase_matching_run_002/results.json').read_text());phase=next(r for r in parent['rows'] if r['M_over_m']==10)
I0=phase['phase_I_exact'];w2=phase['omega_squared_exact'];M=10.;x=phase['phase_negative_chi'];L=1.9;a=20.
Bh=M*M+3*M*x/4+3*x*x;Ar=4*L*I0;h2=2*a*a*I0;Aeff=Ar-h2/Bh;cs2=Aeff/(Aeff+4*w2)
checks=[]
def check(n,v):checks.append({'name':n,'passed':bool(v)});assert v,n
y,g,z,ww,kappa,cc=s.symbols('y gamma Z0 omega2 kappa cs2',positive=True)
F_y=g*y;Kr=2*g*y;Kt=z+2*g*y;q=Kt-F_y;d2=q*q*y*y/ww;E=kappa-q*y*y/ww
canonical=s.expand((Kt-Kr)*(kappa-E)-d2)
check('canonical common-cone determinant identity',s.simplify(canonical+q*g*y**3/ww)==0)
adiabatic=s.expand((Kt-Kr)*(kappa/cc-E)-d2)
check('adiabatic common-cone determinant identity',s.simplify(adiabatic-(z*kappa*(1/cc-1)-q*g*y**3/ww))==0)
# At fixed medium, Kt>=Kr gives subluminal radial response, but not full modes.
check('fixed-clock temporal margin',s.simplify(Kt-Kr-z)==0)
mp.mp.dps=60;rows=[]
for eps in (1.,1e-6):
 kk=mp.mpf(str(2*I0/eps));omega2=mp.mpf(str(w2));speed=mp.mpf(str(cs2))
 for yy in (.001,.1,1.,10.,100.):
  yv=mp.mpf(str(yy));A=1+2*yv;C=2*yv;qv=1+yv;dv2=qv*qv*yv*yv/omega2;Ev=kk-qv*yv*yv/omega2
  for mode in ('adiabatic','canonical_principal'):
   B=kk/speed if mode=='adiabatic' else kk
   total=A*Ev+B*C+dv2;discriminant=total**2-4*A*B*C*Ev
   largest=(total+mp.sqrt(discriminant))/(2*A*B);smallest=(total-mp.sqrt(discriminant))/(2*A*B)
   cone=(A-C)*(B-Ev)-dv2
   rows.append({'epsilon':eps,'gradient_y':yy,'clock_model':mode,'min_speed_squared':float(smallest),'max_speed_squared':float(largest),
    'excess_max_speed_squared_over_one':float(largest-1),'clock_spatial_stiffness':float(Ev),'common_cone_determinant':float(cone),
    'positive_energy_and_common_cone':bool(Ev>0 and cone>=0 and largest<=1 and smallest>=0),
    'scope':'Low-energy clock integrates out massive amplitudes; canonical principal test assumes derivative response ansatz continues above that gap, not an established UV completion'})
result={'checks':checks,'host_I':I0,'host_omega2':w2,'host_adiabatic_cs2':cs2,'response_parameters':'F=gamma y³/3,gamma=Z0=1,Kt=Z0+2gamma y; physical u from charged theta',
 'rows':rows,'non_claims':['No derivation of response coefficients from mediator or full covariant lensing/metric action','Canonical principal obstruction conditional on retaining this local derivative coupling above amplitude gap; another matched UV completion may change it','Finite low-energy cone control not all-frequency causality/quantum certificate; weak epsilon increases inventory','No dark-energy normalization selection']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
