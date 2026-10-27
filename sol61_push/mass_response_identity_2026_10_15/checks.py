"""Longitudinal continuity, positive two-field lift and signed-density controls."""
import json
from pathlib import Path
import sympy as s
import mpmath as mp
mp.mp.dps=70
out=Path(__file__).parent/'run_v1/results.json'
Im,If,kap,gam,k,z,W=s.symbols('Im If kap gam k z W',positive=True)
M=s.diag(Im,If)
V=s.Matrix([[kap+W,-kap],[-kap,kap+gam*k*k]])
checks={}
def exact(name,expr): checks[name]=s.simplify(expr)==0
det=s.expand((V-z*M).det())
exact('mode_polynomial',det-(Im*If*z*z-(If*(kap+W)+Im*(kap+gam*k*k))*z+kap*gam*k*k+W*(kap+gam*k*k)))
R=kap/(kap+gam*k*k)
Ieff=Im+If*R*R
exact('positive_added_inertia',Ieff-Im-If*R*R)
exact('static_reduction', (s.Matrix([1,R]).T*V*s.Matrix([1,R]))[0]-W-kap*gam*k*k/(kap+gam*k*k))
zh=kap*(Im+If)/(Im*If)
exact('zero_k_low_vector',(V.subs({k:0,W:0})*s.Matrix([1,1])).norm()**2)
exact('zero_k_high_vector',sum(v*v for v in ((V.subs({k:0,W:0})-zh*M)*s.Matrix([-If/Im,1]))))
exact('low_k_speed',s.diff(det.subs(W,0),k,2).subs({k:0,z:0})/(-2*s.diff(det.subs(W,0),z).subs({k:0,z:0}))-gam/(Im+If))
AA=1/(Im+If); BB=If/(Im*(Im+If))
chi=(kap-If*z)/det.subs({k:0,W:0})
exact('zero_k_spectral_decomposition',chi-(AA/(-z)+BB/(zh-z)))
exact('spectral_total',AA+BB-1/Im)
exact('fast_mass_fraction',BB/(AA+BB)-If/(Im+If))
rr,A=s.symbols('r A',positive=True)
dens=A*(3-2*rr*rr)*s.exp(-rr*rr)
exact('density_divergence',s.diff(A*rr**3*s.exp(-rr*rr),rr)/rr**2-dens)
exact('total_signed_mass',s.integrate(4*s.pi*rr*rr*dens,(rr,0,s.oo)))
exact('density_minimum',s.diff(dens,rr).subs(rr,s.sqrt(s.Rational(5,2)) ))
exact('minimum_value',dens.subs(rr,s.sqrt(s.Rational(5,2)))+2*A*s.exp(-s.Rational(5,2)))
rows=[]
for eps in ['.01','1e-6','1e-12']:
 for delta in ['.001','.1','10']:
  for ww in ['0','.1']:
   # Im=kap=1, If=eps, gamma k^2=delta. Positive held curvature W=ww.
   e,d,w=map(mp.mpf,[eps,delta,ww])
   tr=(1+w)+(1+d)/e
   determinant=(d+w*(1+d))/e
   high=(tr+mp.sqrt(tr*tr-4*determinant))/2
   low=determinant/high
   alow=(1+d-e*low)/(e*(high-low))
   ahigh=(e*high-(1+d))/(e*(high-low))
   # Independent normalized eigenvectors determine the same residues.
   def weight(root):
    ratio=1+w-root
    return 1/(1+e*ratio*ratio)
   # ratio here is Q/P from the first row, kap=Im=1.
   residual=max(abs(alow-weight(low)),abs(ahigh-weight(high)),abs(alow+ahigh-1))
   assert low>0 and high>0 and alow>0 and ahigh>0 and residual<mp.mpf('1e-50')
   rows.append(dict(epsilon=eps,gradient_to_lock=delta,W_to_lock=ww,
       slow_frequency_squared=float(low),fast_frequency_squared=float(high),
       fast_fraction_of_mass_response=float(ahigh),
       fast_fraction_of_static_response=float((ahigh/high)/(alow/low+ahigh/high)),
       spectral_eigenvector_error=float(residual)))
checks['positive_mode_and_residue_grid']=True
checks['spectral_and_eigenvector_grid']=True
v=mp.mpf('84.08885956972138'); c=mp.mpf('299792458')
eps=(v/c)**2
result=dict(checks={key:bool(val) for key,val in checks.items()},grid=rows,
   illustrative_speed_ratio=dict(mass_displacement_speed_m_s=float(v),bare_auxiliary_speed_m_s=float(c),
    epsilon=float(eps),zero_k_fast_mass_response_fraction=float(eps/(1+eps)),
    common_mode_speed_m_s=float(v/mp.sqrt(1+eps))),
   density_control=dict(minimum_contrast_per_A=float(-2*mp.exp(-mp.mpf('2.5')))),
   nonclaims=['No general no-go for entrainment or altered current maps',
    'No full S2 nonlinear or relativistic completion','No halo formation simulation',
    'No universal speed limit on force signals or local relaxation'])
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:val for key,val in result.items() if key!='grid'},indent=2))
print('Mode/residue cases:',len(rows))
assert all(checks.values())
