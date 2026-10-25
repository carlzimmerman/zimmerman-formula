"""Independent finite corner enumeration and LP feasibility verification."""
import importlib.util,itertools,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import sympy as sp
p=Path(__file__).parent
spec=importlib.util.spec_from_file_location('audit',p/'audit.py'); a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
maximum_error=0.; corner_count=0; lp_count=0
for mode in ['aqual','selective']:
 a.SELECTIVE=mode=='selective'; result=json.loads((p/f'run_{mode}/result.json').read_text())
 for footing,cells in result['footings'].items():
  for name,cell in cells.items():
   d=a.read(name); A=a.inv.FOOTINGS[footing]*d['r']**2/(a.G*a.MSUN)
   for i,row in enumerate(cell['shells']):
    for t in [1,2,3]:
     endpoint=[]
     for k in [i,i+1]:
      limits=[(max(d['h'][k]-t*d['he'][k],0),d['h'][k]+t*d['he'][k]),(max(d['gas'][k]-t*d['ge'][k,0],0),d['gas'][k]+t*d['ge'][k,1]),(max(d['star'][k]-t*d['se'][k,0],0),d['star'][k]+t*d['se'][k,1])]
      values=[]
      for h,g,s in itertools.product(*limits):
       B=g+s
       c=h-.5*(B+np.sqrt(B*B+4*A[k]*B)) if a.SELECTIVE else h*h/(h+A[k])-B
       values.append(c)
      endpoint.append(values)
     deltas=np.array([y-x for x in endpoint[0] for y in endpoint[1]])
     for value,key in [(deltas.min(),f'box{t}_min'),(deltas.max(),f'box{t}_max')]:
      err=abs(value-row[key])/max(abs(value),1); maximum_error=max(maximum_error,err); assert err<1e-11
     corner_count+=len(deltas)
   for hydro,label in [(True,'hydro_only_repair'),(False,'all_box_relaxation')]:
    t=cell[label]['t']
    for shift in ([1e-5] if t==0 else [-1e-5,1e-5]):
     lo,hi=a.bounds(d,A,t+shift,hydro); lo=np.maximum(lo,0)/1e14; hi=hi/1e14
     expected=shift>0
     if np.any(lo>hi): success=False
     else:
      mat=np.zeros((5,6))
      for i in range(5): mat[i,i]=1; mat[i,i+1]=-1
      res=linprog(np.zeros(6),A_ub=mat,b_ub=np.zeros(5),bounds=list(zip(lo,hi)),method='highs')
      success=res.success
     assert success==expected,(mode,footing,name,label,t,shift,success)
     lp_count+=1
r,g,a0,G,alpha,Bprime=sp.symbols('r g a0 G alpha Bprime',positive=True)
f=g*g/(a0+g)
explicit=2*r*r/G*f+r*r/G*sp.diff(f,g)*(-alpha*g)-Bprime
claimed=r*r/G*f*(2-alpha*(g+2*a0)/(g+a0))-Bprime
assert sp.simplify(explicit-claimed)==0
out={'corner_evaluations':corner_count,'maximum_corner_relative_error':maximum_error,'independent_LP_tests':lp_count,'source_slope_identity':'PASS','status':'PASS'}
(p/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
