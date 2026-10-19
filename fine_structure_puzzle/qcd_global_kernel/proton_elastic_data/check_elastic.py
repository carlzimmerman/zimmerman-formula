#!/usr/bin/env python3
"""Full Born finite functional of published lattice points, no FF ansatz."""
import json,re,sys
from decimal import Decimal
from pathlib import Path
import mpmath as mp

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'INPUTS.json').read_text())
mp.mp.dps=data['precision_digits']
rows=data['rows']
out=Path(sys.argv[1])

# Independent read of the exact primary-source table validates transcription.
raw=[]
for line in (HERE/'sources/src/table_ffs.tex').read_text().splitlines():
 if not re.match(r'^\d',line): continue
 cols=[v.strip().replace('\\\\','').strip() for v in line.split('&')]
 if cols[5]=='NA': continue
 raw.append((cols[0],cols[2],cols[5]))
assert len(raw)==len(rows)==19
for got,r in zip(raw,rows):
 assert got==(r['Q2_GeV2'],r['GE']['printed'],r['GM']['printed'])
 for key in ['GE','GM']:
  num,err=re.fullmatch(r'(-?\d+\.\d+)\((\d+)\)',r[key]['printed']).groups()
  assert Decimal(r[key]['central'])==Decimal(num)
  assert Decimal(r[key]['sigma'])==Decimal(err)*Decimal(10)**(-len(num.split('.')[1]))

m=mp.mpf(data['source_mass_GeV'])
tol=mp.mpf(data['kernel_tolerance'])
fmt=lambda a:mp.nstr(a,data['saved_digits'])

def kernel(z,ge,gm):
 t=z*z
 f1=(ge+t*gm)/(1+t)
 a=(ge*ge+t*gm*gm)/(1+t)
 c=ge*ge-2*t*gm*gm
 return z*(3*f1*f1-a)/2+c/(mp.sqrt(1+t)+z)

zs=[mp.sqrt(mp.mpf(r['Q2_GeV2']))/(2*m) for r in rows]
assert all(zs[i]<zs[i+1] for i in range(len(zs)-1))
weights=[(zs[1]-zs[0])/2]+[(zs[i+1]-zs[i-1])/2 for i in range(1,len(zs)-1)]+[(zs[-1]-zs[-2])/2]
assert abs(sum(weights)-(zs[-1]-zs[0]))<tol
assert abs(sum(w*z for w,z in zip(weights,zs))-(zs[-1]**2-zs[0]**2)/2)<tol

point=[]
bs=[]; es=[]; subs=[]
gradient_errors=[]
sigma_ceiling=mp.mpf(0)
for r,z,w in zip(rows,zs,weights):
 ge,gm=mp.mpf(r['GE']['central']),mp.mpf(r['GM']['central'])
 se,sm=mp.mpf(r['GE']['sigma']),mp.mpf(r['GM']['sigma'])
 t=z*z
 f1=(ge+t*gm)/(1+t)
 bv=kernel(z,ge,gm)
 ev=3*z*gm*gm/(2*(1+t))+(ge*ge-2*t*gm*gm)/(1+t)*((1+t)**mp.mpf('1.5')-z**3-mp.mpf('1.5')*z)
 su=-mp.mpf('1.5')*z*(gm*gm-f1*f1)
 assert abs(bv-ev-su)<tol
 de=z*(3*f1-ge)/(1+t)+2*ge/(mp.sqrt(1+t)+z)
 dm=z*t*(3*f1-gm)/(1+t)-4*t*gm/(mp.sqrt(1+t)+z)
 err1=abs(de-mp.diff(lambda ee:kernel(z,ee,gm),ge))
 err2=abs(dm-mp.diff(lambda mm:kernel(z,ge,mm),gm))
 assert err1<tol and err2<tol
 gradient_errors += [err1,err2]
 gie=w*de/(2*mp.pi**2)
 gim=w*dm/(2*mp.pi**2)
 sigma_ceiling+=abs(gie)*se+abs(gim)*sm
 bs.append(bv);es.append(ev);subs.append(su)
 point.append({'Q2_GeV2':r['Q2_GeV2'],'Q_over_m':fmt(2*z),'z':fmt(z),'GE':r['GE'],'GM':r['GM'],'F1':fmt(f1),'Born_B':fmt(bv),'elastic_E':fmt(ev),'Born_subtraction':fmt(su),'nodal_weight_z':fmt(w),'dI_dGE':fmt(gie),'dI_dGM':fmt(gim)})

def segments(ys):
 return sum((zs[i+1]-zs[i])*(ys[i]+ys[i+1])/2 for i in range(len(zs)-1))/(2*mp.pi**2)
iv=segments(bs)
nodal=sum(w*b for w,b in zip(weights,bs))/(2*mp.pi**2)
elastic=segments(es)
sub=segments(subs)
assert abs(iv-nodal)<tol
assert abs(iv-elastic-sub)<tol

res={'schema':'fsp008.proton_elastic_data.results.v1','assertion_tested':'Published 19-point full-Born finite trapezoid functional of the stated light-current lattice proton form factors.','coupling':'u=e^2, alpha=u/(4*pi); no numerical alpha input.','source':'arxiv1812.10311v2 Table VI, cB211.072.64','flavor_scope':data['flavor_scope'],'source_mass_GeV':str(m),'Q2_window_GeV2':[rows[0]['Q2_GeV2'],rows[-1]['Q2_GeV2']],'point_count':len(rows),'segment_count':len(rows)-1,'I_tab_M_u_over_m':fmt(iv),'elastic_dispersive_component':fmt(elastic),'Born_subtraction_component':fmt(sub),'coefficient_per_alpha_4piI':fmt(4*mp.pi*iv),'linearized_statistical_covariance_ceiling_at_fixed_inputs':fmt(sigma_ceiling),'ceiling_per_alpha':fmt(4*mp.pi*sigma_ceiling),'quadrature_implementation_difference':fmt(abs(iv-nodal)),'component_sum_difference':fmt(abs(iv-elastic-sub)),'max_sensitivity_check_difference':fmt(max(gradient_errors)),'points':point,'non_claims':['Not a continuum integral with controlled quadrature error.','Not a complete flavor current or complete proton tensor.','No Q=0 magnetic moment or low/high endpoint extrapolation.','No non-Born or finite UV matching contribution.','No full nonlinear uncertainty or confidence interval from absent covariance.','Source empirical nucleon-mass scale calibration and extraction fits are conditional inputs.','No numerical alpha or cosmological ratio is predicted.']}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:res[k] for k in ['point_count','segment_count','I_tab_M_u_over_m','elastic_dispersive_component','Born_subtraction_component','coefficient_per_alpha_4piI','linearized_statistical_covariance_ceiling_at_fixed_inputs']},indent=2))
