"""Exact finite observation-row validator; does not authenticate physical data."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json
import numpy as np
SRC=Path('deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-019/fgf019_run_001/numeric_001/operator_and_witness.npz')
SHA='f27b6da0437825255d71462f6cb7e91d2becfb6152b99b74cf7f6ac4f013c96c'
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def trans(a):return list(map(list,zip(*a)))
def mul(a,b):return [[dot(row,col) for col in trans(b)] for row in a]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def rref(a):
 a=[list(row) for row in a]; piv=[]; row=0
 if not a:return a,piv
 for col in range(len(a[0])):
  found=next((i for i in range(row,len(a)) if a[i][col]),None)
  if found is None:continue
  a[row],a[found]=a[found],a[row];p=a[row][col];a[row]=[v/p for v in a[row]]
  for i in range(len(a)):
   if i!=row:
    p=a[i][col]
    if p:a[i]=[v-p*w for v,w in zip(a[i],a[row])]
  piv.append(col);row+=1
  if row==len(a):break
 return a,piv

def rank(a):return len(rref(a)[1])
def solution(a,b,n):
 reduced,piv=rref([row+[v] for row,v in zip(a,b)])
 if n in piv:return None
 sol=[F(0)]*n
 for row,col in enumerate(piv):sol[col]=reduced[row][-1]
 assert all(dot(row,sol)==v for row,v in zip(a,b));return sol

def nullbasis(a,n):
 red,piv=rref(a);free=[j for j in range(n) if j not in piv];basis=[]
 for j in free:
  v=[F(0)]*n;v[j]=1
  for i,col in enumerate(piv):v[col]=-red[i][j]
  assert all(dot(row,v)==0 for row in a);basis.append(v)
 return basis

def encode(v):
 if isinstance(v,list):return [encode(z) for z in v]
 return str(v)

def build():
 assert hashlib.sha256(SRC.read_bytes()).hexdigest()==SHA
 x=np.load(SRC);H=[[F(float(z)) for z in row[:15]] for row in x['H']];l=[F(float(z)) for z in x['L'][:15]]
 A=[row[:12] for row in H];O=[row[12:] for row in H];I=eye(12)
 aug,piv=rref([row+i for row,i in zip(A,I)]);assert piv==list(range(12))
 inv=[row[12:] for row in aug];assert mul(A,inv)==I and mul(inv,A)==I
 K=mul(inv,O);w=mul([l[:12]],inv)[0];m=[a-b for a,b in zip(l[12:],mul([w],O)[0])]
 N=[[-z for z in row] for row in K]+eye(3)
 assert mul(H,N)==[[F(0)]*3 for _ in range(12)] and mul([l],N)==[m]
 assert [a+b for a,b in zip(mul([w],H)[0],[F(0)]*12+m)]==l
 base=[F(float(z)) for z in x['baseline'][:15]]
 return H,l,inv,K,w,m,N,base

def analyze(C,H,l,inv,K,w,m,N):
 Ci=[row[:12] for row in C];Co=[row[12:] for row in C]
 R=[[a-b for a,b in zip(row,k)] for row,k in zip(Co,mul(Ci,K))] if C else []
 alpha=solution(trans(R) if R else [[] for _ in range(3)],m,len(R))
 rk=rank(R);full=rank(H+C);augmented=rank(H+C+[l]);ident=alpha is not None
 assert ident==(rk==rank(R+[m]))==(full==augmented)
 out={'residual_rows_exact':encode(R),'residual_rank':rk,'pressure_nullity':15-full,'target_identifiable':ident,'augmented_pressure_rank':full,'rank_with_target':augmented}
 if ident:
  y=[a-b for a,b in zip(w,mul([alpha],mul(Ci,inv))[0])]
  assert [a+b for a,b in zip(mul([y],H)[0],mul([alpha],C)[0])]==l
  out.update({'extra_row_coefficients_alpha_exact':encode(alpha),'old_bin_coefficients_exact':encode(y),'reconstruction_exact':True})
 else:
  v=next(v for v in nullbasis(R,3) if dot(m,v))
  nv=mul(N,[[z] for z in v]);nv=[z[0] for z in nv]
  assert all(dot(row,nv)==0 for row in H+C) and dot(l,nv)!=0
  out.update({'surviving_outer_direction_exact':encode(v),'surviving_full_direction_exact':encode(nv),'target_change_exact':str(dot(l,nv))})
 return out

META=['annulus_edges_target_radius','mask_weight_rule','beam_transfer_source','convolution_convention','geometry_distance','outer_support','basis_nodes','post_convolution_offset','source_hashes']
def validate(payload,data):
 assert payload['operator_sha256']==SHA and payload['coefficient_encoding']=='rational_strings'
 assert payload['pressure_column_count']==15 and payload['offset_fixed_y']=='0'
 rows=payload['rows']; assert len(rows)>0 and len(rows)<=32
 C=[]
 for row in rows:
  assert all(key in row['provenance'] for key in META)
  assert row['provenance']['outer_support']=='p(5)=0; zero outside 5 target radii'
  assert row['provenance']['basis_nodes']==[0,.18,.36,.54,.72,.90,1.10,1.28,1.46,1.64,1.82,2,2.5,3,4,5]
  assert row['provenance']['post_convolution_offset']=='fixed and subtracted; separately declared offset coefficient'
  assert isinstance(row['offset_coefficient'],str);F(row['offset_coefficient'])
  assert len(row['pressure_coefficients'])==15 and all(isinstance(z,str) for z in row['pressure_coefficients'])
  C.append(list(map(F,row['pressure_coefficients'])))
 out=analyze(C,*data[:7]);out.update({'metadata_presence_checked':True,'authenticated_observation':False,'scientific_scope':'Exact supplied-row algebra only; metadata truth, row construction, response calibration and uncertainty need independent review.'});return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--candidate');args=p.parse_args();out=Path(args.output);out.mkdir(exist_ok=True);data=build();H,l,inv,K,w,m,N,base=data
 if args.candidate:
  result=validate(json.loads(Path(args.candidate).read_text()),data);(out/'candidate_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'target_identifiable':result['target_identifiable'],'authenticated_observation':False}));return
 assert all(m)
 controls={}
 aligned=[F(0)]*12+m;negative=[F(0)]*12+[m[1],-m[0],F(0)]
 cases={'no_extra_rows':[],'aligned_target_row':[aligned],'orthogonal_negative_row':[negative],'duplicate_old_row':[H[0]],'single_outer_coordinate':[[F(0)]*12+[F(1),F(0),F(0)]],'three_outer_coordinates':[[F(0)]*12+row for row in eye(3)]}
 for name,C in cases.items():controls[name]=analyze(C,*data[:7])
 assert controls['aligned_target_row']['target_identifiable'] and controls['aligned_target_row']['pressure_nullity']==2
 assert controls['three_outer_coordinates']['target_identifiable'] and controls['three_outer_coordinates']['pressure_nullity']==0
 for name in ['no_extra_rows','orthogonal_negative_row','duplicate_old_row','single_outer_coordinate']:assert not controls[name]['target_identifiable']
 # Explicit strict monotone witness in direction v=m^T annihilated by negative row.
 v=m;direction=[row[0] for row in mul(N,[[z] for z in v])]
 gaps=[base[i]-(base[i+1] if i<14 else F(0)) for i in range(15)]
 dg=[direction[i]-(direction[i+1] if i<14 else F(0)) for i in range(15)]
 eps=min(g/(4*abs(h)) for g,h in zip(gaps,dg) if h)
 plus=[a+eps*b for a,b in zip(base,direction)];minus=[a-eps*b for a,b in zip(base,direction)]
 for pressure in [plus,minus]:
  assert all(pressure[i]>(pressure[i+1] if i<14 else F(0)) for i in range(15))
  assert all(dot(row,pressure)==dot(row,base) for row in H+[negative])
 assert dot(l,plus)!=dot(l,minus)
 provenance={'annulus_edges_target_radius':'SYNTHETIC ROW; no actual annulus','mask_weight_rule':'synthetic algebra only','beam_transfer_source':'not an instrument row','convolution_convention':'not constructed physically','geometry_distance':'inherited basis only','outer_support':'p(5)=0; zero outside 5 target radii','basis_nodes':[0,.18,.36,.54,.72,.90,1.10,1.28,1.46,1.64,1.82,2,2.5,3,4,5],'post_convolution_offset':'fixed and subtracted; separately declared offset coefficient','source_hashes':{'operator_npz':SHA}}
 fixture={'operator_sha256':SHA,'coefficient_encoding':'rational_strings','pressure_column_count':15,'offset_fixed_y':'0','synthetic_only':True,'rows':[{'pressure_coefficients':encode(aligned),'offset_coefficient':'1','provenance':provenance}]}
 fixture_result=validate(fixture,data);assert fixture_result['target_identifiable'] and not fixture_result['authenticated_observation']
 damaged=json.loads(json.dumps(fixture));damaged['rows'][0]['pressure_coefficients']=encode(negative);assert not validate(damaged,data)['target_identifiable']
 malformed=json.loads(json.dumps(fixture));malformed['rows'][0]['provenance']['outer_support']='different support'
 try:validate(malformed,data)
 except AssertionError:reject=True
 else:reject=False
 assert reject
 (out/'synthetic_candidate_rows.json').write_text(json.dumps(fixture,indent=2)+'\n')
 result={'operator_sha256':SHA,'inner_inverse_exact':encode(inv),'K_exact':encode(K),'measured_bin_row_w_exact':encode(w),'missing_outer_row_m_exact':encode(m),'missing_outer_row_m_float':list(map(float,m)),'null_basis_N_exact':encode(N),'each_outer_coordinate_changes_target':True,'irrelevant_outer_plane':'m v=0; relevant directions have m v nonzero','controls':controls,'negative_strict_witness':{'v_exact':encode(v),'epsilon_exact':str(eps),'pressure_plus_exact':encode(plus),'pressure_minus_exact':encode(minus),'gradient_plus':float(dot(l,plus)),'gradient_minus':float(dot(l,minus)),'equal_old_and_negative_row_data_exact':True,'strict_monotonicity_exact':True},'candidate_validator_controls':{'aligned_identifies':True,'changed_to_negative_does_not_identify':True,'wrong_support_rejected':reject,'never_authenticates_observation':True},'exact_checks':{'left_inverse':True,'right_inverse':True,'target_decomposition':True,'null_basis':True,'rowspace_criteria_equivalent':True,'all_three_m_coefficients_nonzero':True},'limitations':['Stored finite operator and exact synthetic model only','No actual added annulus response constructed','Row metadata presence does not authenticate it','No covariance, confidence, continuum gradient or force conclusion','Necessity applies to linear family and strict feasible interior, not every boundary-only feasible set']}
 (out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'missing_row':list(map(float,m)),'controls':{k:v['target_identifiable'] for k,v in controls.items()},'strict_witness_gradients':[float(dot(l,plus)),float(dot(l,minus))]}))
if __name__=='__main__':main()
