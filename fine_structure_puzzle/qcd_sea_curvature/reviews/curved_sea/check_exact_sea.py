from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math,platform,sys,time
root=Path('/Users/carlzimmerman/new_physics/zimmerman-formula')
own=root/'fine_structure_puzzle/qcd_sea_curvature/reviews/curved_sea'
target=root/'fine_structure_puzzle/qcd_sea_curvature/sea_lattice'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
start=time.time()
files=[target/n for n in ['DERIVATION.md','REPORT.md','INPUTS.json','SOURCE_RECEIPTS.json']]
hashes={str(p.relative_to(root)):sha(p) for p in files}
inputs=json.loads((target/'INPUTS.json').read_text())
rows=[]
for x in inputs['rows']:
    p=F(x['central_display'])/10000
    err=F(x['statistical_error_display'])/10000
    rows.append({'ensemble':x['ensemble'],'P_fm3':str(p),'statistical_error_fm3':str(err),'raw_U_slope_numerator_without_1_over_pi_alpha_ref':str(-p/4),'slope_statistical_error_numerator_without_1_over_pi_alpha_ref':str(err/4),'C_sum_t2_numerator_without_1_over_alpha_ref':str(-6*p)})
assert rows[0]['raw_U_slope_numerator_without_1_over_pi_alpha_ref']=='-7/200000'
assert rows[0]['slope_statistical_error_numerator_without_1_over_pi_alpha_ref']=='3/100000'
assert rows[1]['raw_U_slope_numerator_without_1_over_pi_alpha_ref']=='-1/400000'
assert rows[1]['slope_statistical_error_numerator_without_1_over_pi_alpha_ref']=='9/200000'

def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b): c[i+j]+=u*v
    return c
c=[7,-112,243,-128]
assert sum(F(a,k) for k,a in enumerate(c,1))==0
assert sum(F(a,k**3) for k,a in enumerate(c,1))==0
assert sum(a*k for k,a in enumerate(c,1))==0
numerator=[F(0)]*4
for k,a in enumerate(c,1):
    poly=[F(1)]
    for l in range(1,5):
        if l!=k: poly=mul(poly,[F(l*l),F(1)])
    for i,b in enumerate(poly):numerator[i]+=2*a*k*b
assert numerator==[0,0,5040,0]
F_at_one=2*sum(F(a*k,1+k*k) for k,a in enumerate(c,1))
assert F_at_one==F(252,85)
integral=4992*math.log(2)-2916*math.log(3)
assert abs(integral-256.637291599)<1e-8
receipt=json.loads((target/'SOURCE_RECEIPTS.json').read_text())
source_checks=[]
for source in receipt['sources'][:2]:
    for a in source.get('artifacts',[]):
        p=Path(a['path']); actual=sha(p)
        assert actual==a['sha256']
        source_checks.append({'source':source['id'],'path':str(p),'sha256':actual,'receipt_match':True})
assert hashes=={str(p.relative_to(root)):sha(p) for p in files}
result={'status':'completed','verdict':'implementation and finite assertion verified in stated range','argv':[sys.executable,str(Path(__file__).resolve())],'runtime_seconds':time.time()-start,'python':sys.version,'platform':platform.platform(),'target_hashes':hashes,'source_receipt_checks':source_checks,'rows':rows,'profile_moments':'integral h=0; integral tau^2 h=0; sum ck*k=0, exact rational arithmetic','profile_transform_numerator_ascending':list(map(str,numerator)),'profile_F_at_one':str(F_at_one),'profile_integral_approx':integral,'limits':['Printed marginal errors only; alpha_ref kept symbolic','Signed profile is a mathematical counterexample for these moment constraints, not a physical QCD tensor','No Git revision metadata observed; no target files modified','Source interpretation issue about Figure S3 diagram2 is recorded separately in SEA_REVIEW.md']}
(own/'SEA_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['source_receipt_checks','target_hashes','rows']},indent=2))
