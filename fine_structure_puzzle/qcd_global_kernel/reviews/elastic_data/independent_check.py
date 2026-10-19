#!/usr/bin/env python3
import hashlib,json,re,sys,tarfile
from decimal import Decimal as D, getcontext
from pathlib import Path
getcontext().prec=65
base=Path('fine_structure_puzzle/qcd_global_kernel/proton_elastic_data')
review=Path('fine_structure_puzzle/qcd_global_kernel/reviews/elastic_data')
pins=json.loads((review/'AUDITED_PINS.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in pins.items())
receipt=json.loads((base/'SOURCE_RECEIPTS.json').read_text())
for item in receipt['retained_files']:
 p=Path(item['path']);assert p.stat().st_size==item['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
with tarfile.open(base/'sources/1812.10311v2.tar') as archive:
 for name in ['table_ffs.tex','EM_PRD.tex']:
  member=[x for x in archive.getmembers() if Path(x.name).name==name]
  assert len(member)==1
  assert archive.extractfile(member[0]).read()==(base/'sources/src'/name).read_bytes()
rows=[]
for line in (base/'sources/src/table_ffs.tex').read_text().splitlines():
 if not line.startswith('0.'):continue
 cells=[x.strip() for x in line.split('&')]
 q=D(cells[0])
 if q==0:
  assert cells[5]=='NA';continue
 parsed=[]
 for cell in [cells[2],cells[5]]:
  number,error=re.fullmatch(r'([0-9]+[.][0-9]+)\(([0-9]+)\)',cell).groups()
  central=D(number); sigma=D(error)*D(10)**central.as_tuple().exponent
  parsed.append((central,sigma,cell))
 rows.append((q,*parsed))
assert len(rows)==19
inputs=json.loads((base/'INPUTS.json').read_text())
for (q,(e,se,ep),(m,sm,mp)), row in zip(rows,inputs['rows']):
 assert q==D(row['Q2_GeV2'])
 for label,val,sig,printed in [('GE',e,se,ep),('GM',m,sm,mp)]:
  assert (val,sig,printed)==(D(row[label]['central']),D(row[label]['sigma']),row[label]['printed'])
pi=D('3.141592653589793238462643383279502884197169399375105820974944592307816')
norm=1/(2*pi*pi);mass=D('0.9389')
assert mass==D(inputs['source_mass_GeV'])
z=[q.sqrt()/(2*mass) for q,*_ in rows]
assert all(a<b for a,b in zip(z,z[1:]))
w=[(z[1]-z[0])/2]+[(z[i+1]-z[i-1])/2 for i in range(1,18)]+[(z[-1]-z[-2])/2]
values=[]; ceiling=D(0);dispersive=D(0);subtraction=D(0);point_diffs=[];sensitivity_diffs=[]
author=json.loads((base/'run_001/RESULTS.json').read_text())
for i,(zi,wi,(_, (e,se,_),(m,sm,_))) in enumerate(zip(z,w,rows)):
 t=zi*zi;d=1+t;r=d.sqrt()-zi
 a=r+zi*(2-t)/(2*d*d);b=3*zi*t/(d*d);c=-2*t*r+zi*t*(2*t-1)/(2*d*d)
 val=a*e*e+b*e*m+c*m*m;values.append(val)
 de=2*a*e+b*m;dm=b*e+2*c*m
 ceiling+=norm*wi*(abs(de)*se+abs(dm)*sm)
 h=D('1e-12')
 fun=lambda ee,mm:a*ee*ee+b*ee*mm+c*mm*mm
 assert abs((fun(e+h,m)-fun(e-h,m))/(2*h)-de)<D('1e-45')
 assert abs((fun(e,m+h)-fun(e,m-h))/(2*h)-dm)<D('1e-45')
 f1=(e+t*m)/d
 su=-3*zi*(m*m-f1*f1)/2
 ev=3*zi*m*m/(2*d)+(e*e-2*t*m*m)/d*(d*d.sqrt()-zi**3-3*zi/2)
 assert abs(val-ev-su)<D('1e-60')
 dispersive+=norm*wi*ev;subtraction+=norm*wi*su
 ap=author['points'][i]
 point_diffs.append(abs(val-D(ap['Born_B'])))
 sensitivity_diffs.extend([abs(norm*wi*de-D(ap['dI_dGE'])),abs(norm*wi*dm-D(ap['dI_dGM']))])
result=norm*sum(wi*bi for wi,bi in zip(w,values))
segment=norm*sum((z[i+1]-z[i])*(values[i+1]+values[i])/2 for i in range(18))
assert abs(result-segment)<D('1e-60')
assert abs(sum(w)-(z[-1]-z[0]))<D('1e-60')
assert abs(sum(wi*zi for wi,zi in zip(w,z))-(z[-1]**2-z[0]**2)/2)<D('1e-60')
checks={'I_tab_M_u_over_m':result,'elastic_dispersive_component':dispersive,'Born_subtraction_component':subtraction,'coefficient_per_alpha_4piI':4*pi*result,'linearized_statistical_covariance_ceiling_at_fixed_inputs':ceiling}
for key,value in checks.items(): assert abs(value-D(author[key]))<D('1e-43')
assert max(point_diffs+sensitivity_diffs)<D('1e-43')
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in pins.items())
out={'status':'passed','independent_implementation':'stdlib Decimal quadratic Sachs coefficients; direct TeX parsing; no author imports','points':19,'segments':18,'values':{k:str(v) for k,v in checks.items()},'max_author_point_difference':str(max(point_diffs)),'max_author_sensitivity_difference':str(max(sensitivity_diffs)),'source_archive_members_match':True,'receipt_hashes_match':True,'changed_pins':[],'limitations':'Finite printed-point functional only; algebra premise and normalization conditional; no continuum integral or total uncertainty/alpha/mass prediction.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
