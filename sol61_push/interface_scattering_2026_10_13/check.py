import math,json,sys
from pathlib import Path
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
old=json.loads((Path(__file__).parent/'INPUT_WELL.json').read_text());mu=old['bulk_interaction_chemical_potential_eV'];E=old['quasiparticle_energy_eV']/mu

def scatter(depth,angle,h,L=16.):
 beta=depth/mu-1;y0=math.sqrt(mu/(2*depth));x0=math.sqrt(2)*math.atanh(y0);x1=math.asinh(math.sqrt(2*beta)/y0)/math.sqrt(beta)
 N=round(2*L/h);h=2*L/N;x=np.linspace(-L,L,N+1);count=N+1
 yy=np.empty(count);inside=x<0
 yy[inside]=np.tanh((x0-x[inside])/math.sqrt(2));yy[~inside]=math.sqrt(2*beta)/np.sinh(math.sqrt(beta)*(x[~inside]+x1))
 ktot2=math.sqrt(1+E*E)-1;parallel=ktot2*math.sin(angle)**2
 k=math.sqrt(ktot2-parallel);ko2=E-beta-parallel
 decay_in=math.sqrt(math.sqrt(1+E*E)+1+parallel);decay_v=math.sqrt(E+beta+parallel)
 A=math.sqrt(1+E*E);u=math.sqrt((A/E+1)/2);v=-math.sqrt((A/E-1)/2)
 left=np.array([[u,u,1,1],[v,v,E+A,E+A],[1j*k*u,-1j*k*u,decay_in,-decay_in],[1j*k*v,-1j*k*v,decay_in*(E+A),-decay_in*(E+A)]],complex)
 if ko2>0:
  ko=math.sqrt(ko2);right=np.array([[1,1,0,0],[0,0,1,1],[1j*ko,-1j*ko,0,0],[0,0,-decay_v,decay_v]],complex)
 else:
  ko=0.;d=math.sqrt(-ko2);right=np.array([[1,1,0,0],[0,0,1,1],[-d,d,0,0],[0,0,-decay_v,decay_v]],complex)
 PL=np.linalg.inv(left);PR=np.linalg.inv(right)
 W=np.where(inside,-1,beta)+2*yy*yy+parallel
 mat=lil_matrix((2*count,2*count),dtype=complex);rhs=np.zeros(2*count,complex)
 for i in range(1,N):
  mat[i,i-1]=mat[i,i+1]=1/h**2;mat[i,i]=-2/h**2-W[i]+E;mat[i,count+i]=-yy[i]**2
  j=count+i;mat[j,j-1]=mat[j,j+1]=1/h**2;mat[j,j]=-2/h**2-W[i]-E;mat[j,i]=-yy[i]**2
 def boundary(row,coef,side,val):
  at=0 if side=='left' else N
  mat[row,at]+=coef[0];mat[row,count+at]+=coef[1]
  stencil=[(0,-3),(1,4),(2,-1)] if side=='left' else [(N,3),(N-1,-4),(N-2,1)]
  for idx,fac in stencil:
   mat[row,idx]+=coef[2]*fac/(2*h);mat[row,count+idx]+=coef[3]*fac/(2*h)
  rhs[row]=val
 boundary(0,PL[0],'left',1);boundary(count,PL[3],'left',0)
 boundary(N,PR[1],'right',0);boundary(count+N,PR[3],'right',0)
 sol=spsolve(mat.tocsr(),rhs);U=sol[:count];V=sol[count:]
 zl=np.array([U[0],V[0],(-3*U[0]+4*U[1]-U[2])/(2*h),(-3*V[0]+4*V[1]-V[2])/(2*h)])
 zr=np.array([U[-1],V[-1],(3*U[-1]-4*U[-2]+U[-3])/(2*h),(3*V[-1]-4*V[-2]+V[-3])/(2*h)])
 refl=abs((PL@zl)[1])**2;trans=ko/(k*(u*u+v*v))*abs((PR@zr)[0])**2 if ko else 0.
 residual=np.max(abs(mat@sol-rhs));assert residual<1e-7
 assert abs(refl+trans-1)<.004
 return dict(depth_eV=depth,angle_degrees=angle*180/math.pi,h=h,L=L,reflection=float(refl),transmission=float(trans),flux_error=float(abs(refl+trans-1)),open_channel=bool(ko2>0),linear_residual=float(residual))
rows=[]
for depth in [1.,1.5,2.]:
 for h in [.04,.02,.01]:
  r=scatter(depth,0,h);rows.append(r);print(r,flush=True)
for depth in [1.,1.5,2.]:
 for angle in [30,60,80]:
  r=scatter(depth,math.radians(angle),.02);rows.append(r);print(r,flush=True)
ref=scatter(1,0,.02,L=20);base=next(r for r in rows if r['depth_eV']==1 and r['angle_degrees']==0 and r['h']==.02)
assert abs(ref['transmission']-base['transmission'])<.001
ktot2=math.sqrt(1+E*E)-1;max_depth=mu*(E-ktot2+1)
out=dict(cases=rows,domain_refinement=ref,all_angles_open_depth_upper_eV=max_depth,
 scope='Leading one-field planar GP wall and BdG scattering, no source-field mixing or microscopic trap implementation. Flux conservation and grid/domain refinement are numerical checks.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
