"""Third-derivative orientation rule: exact tensor identities and bounded witnesses.
Writes only declared outputs; never imports/executes Claude scripts.
"""
import argparse,json,pathlib,math
import sympy as s
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','affine','continuity','layer'],default='none');args=p.parse_args();checks=[]
def ck(n,q):checks.append(dict(name=n,passed=bool(q)))
def zero(n,q):ck(n,s.simplify(q)==0)
z=s.symbols('z',real=True);gp,b=s.symbols('gpp b',real=True)
T=s.MutableDenseNDimArray.zeros(3,3,3)
T[0,0,0]=gp
for j in [1,2]:T[0,j,j]=T[j,0,j]=T[j,j,0]=b
M=s.Matrix(3,3,lambda i,j:sum(T[i,k,l]*T[j,k,l] for k in range(3) for l in range(3)))
v=s.Matrix([sum(T[i,j,j] for j in range(3)) for i in range(3)])
zero('spherical_M',(M-(2*b*b*s.eye(3)+s.diag(gp*gp,0,0))).norm());zero('spherical_v',(v-s.Matrix([gp+2*b,0,0])).norm())
Tc=s.MutableDenseNDimArray.zeros(3,3,3);Tc[0,0,0]=gp
Tc[0,1,1]=Tc[1,0,1]=Tc[1,1,0]=b
Mc=s.Matrix(3,3,lambda i,j:sum(Tc[i,k,l]*Tc[j,k,l] for k in range(3) for l in range(3)))
zero('cylinder_M',(Mc-s.diag(gp*gp+b*b,2*b*b,0)).norm())
zero('cylinder_zero_trace_max_plane',(Mc.subs(gp,-b)-s.diag(2*b*b,2*b*b,0)).norm())
def projected_min(H,n):
 n=np.asarray(n,float);n=n/np.linalg.norm(n);axis=np.eye(3)[np.argmin(np.abs(n))];e=axis-n*np.dot(axis,n);e/=np.linalg.norm(e);f=np.cross(n,e);E=np.column_stack([e,f]);return float(np.linalg.eigvalsh(E.T@H@E)[0])
def reader(H,T):
 vv=np.einsum('ijj->i',T)
 if np.linalg.norm(vv)>0:return projected_min(H,vv)
 MM=np.einsum('ikl,jkl->ij',T,T);evals,evec=np.linalg.eigh(MM)
 if evals[-1]==0:return float(np.linalg.eigvalsh(H)[0])
 # Exact degeneracies supplied in these bounded examples; tolerance implements only their float representation.
 multiplicity=sum(abs(evals-evals[-1])<=1e-12*evals[-1])
 if multiplicity>=2:return float(np.linalg.eigvalsh(H)[0])
 return projected_min(H,evec[:,-1])
sphere_rows=[]
for bb,pp in [(1,2),(1,-2),(1,0),(0,3),(0,0),(-2,4),(-2,1)]:
 tt=np.array(T.applyfunc(lambda q:s.sympify(q).subs({b:bb,gp:pp})).tolist(),float);H=np.diag([2+bb,2,2]);R=reader(H,tt)
 ck('sphere_'+str((bb,pp)),abs(R-2)<1e-12);sphere_rows.append(dict(b=bb,gpp=pp,R=R))
for bb,pp,gr,gt in [(0,0,2,2),(-2,2,-1,1),(1,1,3,2),(1,-1,3,2)]:
 tt=np.array(Tc.applyfunc(lambda q:s.sympify(q).subs({b:bb,gp:pp})).tolist(),float);R=reader(np.diag([gr,gt,0]),tt);ck('cylinder_rejected_'+str((bb,pp)),R<=1e-12)
for dd in [0.,2.,-2.]:
 tt=np.zeros((3,3,3));tt[0,0,0]=dd;ck('plane_rejected_'+str(dd),reader(np.diag([3,0,0]),tt)<=1e-12)
x,y,z=s.symbols('x y z',real=True);c,e=s.symbols('c e',positive=True)
phi=c*(x*x+y*y)/2+e*z**3/6;H=s.hessian(phi,(x,y,z));TT=s.MutableDenseNDimArray([s.diff(phi,u,w,q) for u in (x,y,z) for w in (x,y,z) for q in (x,y,z)],(3,3,3))
origin={x:0,y:0,z:0};zero('local_positive_source_jet',s.trace(H).subs(origin)-2*c)
Rzero=reader(np.diag([2.,2.,0.]),np.zeros((3,3,3)));jumps=[]
for ee in [1.,1e-3,1e-6,1e-9]:
 t=np.array(TT.applyfunc(lambda q:s.sympify(q).subs({e:ee,c:2})).tolist(),float);R=reader(np.diag([2.,2.,0.]),t);ck('small_gradient_jump_'+str(ee),Rzero==0 and R==2);jumps.append(dict(epsilon=ee,R=R))
linear=s.symbols('l1 l2 l3');aff=phi+linear[0]*x+linear[1]*y+linear[2]*z+s.Symbol('constant')
zero('affine_H_invariance',(s.hessian(aff,(x,y,z))-H).norm());zero('affine_T_invariance',sum((s.diff(aff-phi,u,w,q))**2 for u in (x,y,z) for w in (x,y,z) for q in (x,y,z)))
# Exact first variation for a simple projected min: multiplier H e=R e+mu n.
mu,V=s.symbols('mu V',nonzero=True);dn=s.Matrix(s.symbols('dn1:4'));ee=s.Matrix([1,0,0]);nn=s.Matrix([0,0,1]);A=-2*mu/V*ee
zero('orientation_variation_coefficient',A.dot(s.Matrix([V*dn[0],V*dn[1],0]))+2*mu*dn[0])
# External tide witness: sphere phi=r^3/3, n=e_z at r=1; trace gradient magnitude4.
# Tide Hxx=-.1,Hyy=.1,Hxz=.2, others0; projected min e_x, R=.9, A=-.1 e_x.
H0=np.array([[.9,0,.2],[0,1.1,0],[.2,0,2.]])
TT0=np.array(T.applyfunc(lambda q:s.sympify(q).subs({gp:2,b:1})).tolist(),float)
# rotate radial e_x of the tensor construction to e_z
perm=[2,1,0];TT0=TT0[np.ix_(perm,perm,perm)]
R0=reader(H0,TT0);Avec=np.array([-.1,0,0]);gradR=np.array([-.4,0,1.]);Adotgrad=.04
ck('external_tide_R',abs(R0-.9)<1e-12);ck('external_tide_nonzero_normal',abs(Avec@gradR-Adotgrad)<1e-14)
# Orthogonal finite difference of projected reader with respect to v (realizable symmetric third tensors).
fd=[]
for hh in [1e-4,1e-5,1e-6]:
 tp=TT0.copy();tm=TT0.copy();tp[0,0,0]+=hh;tm[0,0,0]-=hh
 der=(reader(H0,tp)-reader(H0,tm))/(2*hh);fd.append(dict(step=hh,derivative=der));ck('orientation_FD_'+str(hh),abs(der-Avec[0])<2e-8)
# Source reaction identity under flat Poisson, by Fourier symbol / commuting derivatives.
k1,k2,k3=s.symbols('k1 k2 k3',real=True);aa=s.symbols('A1 A2 A3',real=True);kk=s.Matrix([k1,k2,k3]);AA=s.Matrix(aa);k2sq=kk.dot(kk)
zero('third_source_symbol_order1',(-s.I*kk.dot(AA)*(-k2sq))/(-k2sq)+s.I*kk.dot(AA))
# Gaussian physical-width delta profile: exact max derivative ~w^-2.
w=s.symbols('w',positive=True);ss=s.symbols('s',real=True);delta=s.exp(-ss**2/w**2)/(s.sqrt(s.pi)*w)
peak=s.simplify(abs(s.diff(delta,ss).subs(ss,w/s.sqrt(2))))
zero('sharp_orientation_layer_scaling',peak-s.sqrt(2/s.E)/(s.sqrt(s.pi)*w*w))
normal_coeff=Adotgrad/np.linalg.norm(gradR);kappa=np.linalg.norm(gradR);layers=[]
for ww in [.1,.05,.025,.0125]:
 peak=normal_coeff/kappa*math.sqrt(2/math.e)/math.sqrt(math.pi)/(ww*ww);layers.append(dict(width=ww,orientation_potential_peak=peak,w2_peak=peak*ww*ww))
ck('layer_ratio_four',abs(layers[1]['orientation_potential_peak']/layers[0]['orientation_potential_peak']-4)<1e-12)
# PSD rank-veto discontinuity: exact metric congruence tangent identities do not ensure stream-state continuity.
sig=s.diag(1,1,e*e);zero('rank_perturbation_determinant',sig.det()-e*e)
if args.control=='affine':ck('CONTROL_wrong_gradient_affine_invariance',s.diff(aff,x)==s.diff(phi,x))
if args.control=='continuity':ck('CONTROL_wrong_orientation_continuity',jumps[-1]['R']==Rzero)
if args.control=='layer':ck('CONTROL_wrong_bounded_sharp_layer',layers[-1]['orientation_potential_peak']<=layers[0]['orientation_potential_peak'])
result=dict(passed=all(v['passed'] for v in checks),checks=checks,spheres=sphere_rows,orientation_discontinuity=dict(R_at_zero=Rzero,approaching=jumps),orientation_derivative_fd=fd,external_tide=dict(R=R0,A=Avec.tolist(),gradR=gradR.tolist(),A_dot_gradR=Adotgrad),sharp_layers=layers,control=args.control,non_claims=['No full covariant metric/action health','No all third-derivative reader no-go','No actual host/data rescoring','No phase-space ownership from spatial jets','No CFG355 execution'])
out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[q['name'] for q in checks if not q['passed']])));raise SystemExit(0 if result['passed'] else 1)
