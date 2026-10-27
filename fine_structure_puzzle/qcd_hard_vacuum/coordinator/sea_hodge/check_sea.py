import itertools,json,sys,math
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
base=Path(__file__).parent;inp=json.loads((base/'INPUTS.json').read_text());mp.mp.dps=inp['gaussian_decimal_digits'];checks=0

def test(v):
 global checks
 assert v;checks+=1

def cells(n,k):
 out=[]
 for axes in itertools.combinations(range(5),k):
  for x in itertools.product(*[range(n) if j in axes else range(n+1) for j in range(5)]):
   if any(x[j] in (0,n) for j in range(5) if j not in axes):out.append((axes,x))
 return out

def shift(x,j):
 y=list(x);y[j]+=1;return tuple(y)

def rank2(rows):
 piv={}
 for r in rows:
  while r:
   j=r.bit_length()-1
   if j in piv:r^=piv[j]
   else:piv[j]=r;break
 return len(piv)

def edge_phase(x,y):
 j=next(j for j in range(5) if x[j]!=y[j]);low=x if x[j]<y[j] else y
 return (1 if x[j]<y[j] else -1)*(-1)**sum(low[:j])

rows=[];gaussian=[]
for n in inp['enumerated_n']:
 cc=[cells(n,k) for k in range(5)];counts=[len(c) for c in cc]
 expected=[math.comb(5,k)*n**k*((n+1)**(5-k)-(n-1)**(5-k)) for k in range(5)]
 test(counts==expected);test(sum((-1)**k*counts[k] for k in range(5))==2)
 vi={x:i for i,(axes,x) in enumerate(cc[0])};ei={e:i for i,e in enumerate(cc[1])}
 er=[];adj=[[] for _ in vi]
 for idx,((j,),x) in enumerate(cc[1]):
  u,v=vi[x],vi[shift(x,j)];er.append((1<<u)^(1<<v));adj[u].append((v,idx));adj[v].append((u,idx))
 pr=[];sparse=[]
 for (j,k),x in cc[2]:
  oriented=[(((j,),x),1),(((k,),shift(x,j)),1),(((j,),shift(x,k)),-1),(((k,),x),-1)]
  pairs=[(ei[e],sgn) for e,sgn in oriented];sparse.append(pairs)
  bits=0;vertexbits=0
  for i,sgn in pairs:bits^=1<<i;vertexbits^=er[i]
  test(vertexbits==0);pr.append(bits)
  cycle=[x,shift(x,j),shift(shift(x,j),k),shift(x,k)]
  for direction in (cycle,list(reversed(cycle))):
   for offset in range(4):
    cyc=direction[offset:]+direction[:offset]
    test(math.prod(edge_phase(cyc[i],cyc[(i+1)%4]) for i in range(4))==-1)
 r0,r1=rank2(er),rank2(pr);test(r0==counts[0]-1);test(r1==counts[1]-counts[0]+1)
 test(r1==30*n**4+20*n**2-1)
 sq=sum((F(x)**2 for x in inp['charges']),F(0));coef=sq*F(r1,6)
 test(coef==sq*F(30*n**4+20*n**2-1,6))
 rows.append(dict(n=n,cell_counts=counts,rank_d0_mod2=r0,rank_d1_mod2=r1,coefficient_W_u_over_beta_kappa4=str(coef)))
 if n!=inp['gaussian_n']:continue
 seen={0};stack=[0];tree=set()
 while stack:
  u=stack.pop()
  for v,idx in adj[u]:
   if v not in seen:seen.add(v);stack.append(v);tree.add(idx)
 test(len(tree)==r0)
 cotree=[i for i in range(counts[1]) if i not in tree];test(len(cotree)==r1);ci={e:i for i,e in enumerate(cotree)}
 fps=[[(ci[i],sgn) for i,sgn in row if i in ci] for row in sparse]
 for prescription in inp['gaussian_weights']:
  ws=[mp.mpf(1) if prescription=='1' else mp.mpf(1)+mp.mpf(i%7)/8 for i in range(counts[2])]
  gram=mp.matrix(r1,r1)
  for w,row in zip(ws,fps):
   for i,a in row:
    for j,b in row:gram[i,j]+=w*a*b
  cov=gram**-1
  variances=[sum(a*b*cov[i,j] for i,a in row for j,b in row) for row in fps]
  trace=sum(w*c for w,c in zip(ws,variances));test(abs(trace-r1)<mp.mpf('1e-30'))
  test(all(c>0 for c in variances))
  if prescription=='1':test(max(abs(c-mp.mpf(r1)/counts[2]) for c in variances)<mp.mpf('1e-30'))
  gaussian.append(dict(n=n,weights=prescription,tree_edges=len(tree),physical_photon_coordinates=r1,weighted_variance_sum=mp.nstr(trace,35),max_variance=mp.nstr(max(variances),25),min_variance=mp.nstr(min(variances),25)))

# An orthogonal direct matrix derivative checks the hopping contact/current factor.
def tr(a):return sum(a[i,i] for i in range(a.rows))
matrix_checks=[]
for q in [mp.mpf(2)/3,-mp.mpf(1)/3]:
 for flux in [mp.mpf(1)/3,mp.mpf(7)/5]:
  second=mp.mpf(0);ret=mp.mpf(0)
  for theta in [mp.mpf(1)/3,mp.mpf(2)/5,-mp.mpf(11)/15]:
   h=mp.matrix(4,4);hp=mp.matrix(4,4);hpp=mp.matrix(4,4)
   for i,j,z in [(0,1,mp.mpc(1)),(1,2,mp.mpc(1)),(2,3,mp.mpc(1)),(3,0,-mp.exp(1j*theta))]:h[i,j]=z;h[j,i]=-mp.conj(z)
   hp[3,0]=1j*q*flux*h[3,0];hp[0,3]=-1j*q*flux*h[0,3]
   hpp[3,0]=-(q*flux)**2*h[3,0];hpp[0,3]=-(q*flux)**2*h[0,3]
   second+=4*tr(h**3*hpp)+4*sum(tr(h**j*hp*h**(2-j)*hp) for j in range(3))
   ret+=mp.cos(theta)
  got=second/8;target=q*q*flux*flux*ret
  test(abs(got-target)<mp.mpf('1e-30'))
  matrix_checks.append(dict(q=mp.nstr(q,12),flux=mp.nstr(flux,12),coefficient_W_u_kappa4=mp.nstr(got.real,30),imaginary_residual=mp.nstr(got.imag,8),predicted=mp.nstr(target,30)))

result=dict(assertion_tested='Actual closed cubical cell counts, mod2 boundary/rank checks, every staggered square phase, independent tree-gauge Gaussian flux trace and direct hopping-matrix second derivatives for the declared finite model.',checks=checks,rows=rows,gaussian_controls=gaussian,direct_hopping_controls=matrix_checks,analytic_coefficient='W_u|beta kappa4 = beta kappa4 S_Q (30 n^4+20 n^2-1)/6',physical_A_computed=False,physical_R_computed=False,physical_alpha_input=False,continuum_QCD_matching=False,limitations=['Finite heavy-hopping lattice Taylor coefficient, not full determinant at physical parameters.','Ambient-phase fermion continuum spin/taste/metric equivalence unverified.','Polyhedral cubical S4, not smooth round sphere; n discrete.','Real H1 theorem analytic; finite-field ranks are bounded implementation checks.','No bound on omitted orders or continuum physical matching.'])
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,enumerated_n=inp['enumerated_n'],gaussian_controls=len(gaussian),direct_matrix_controls=len(matrix_checks),physical_R=False)))
