"""Tree contact calculation only; unknown physical Wilson coefficient."""
import json, math, sys
from pathlib import Path
import sympy as s
E,C=s.symbols('E C', positive=True)
g=s.diag(1,-1,-1,-1)
k1=s.Matrix([E,0,0,E]); k2=s.Matrix([E,0,0,-E])
pol=[s.Matrix([0,1,0,0]),s.Matrix([0,0,1,0])]
def dot(a,b): return (a.T*g*b)[0]
def amp(a,b): return 4*C*(dot(k1,k2)*dot(a,b)-dot(k1,b)*dot(k2,a))
checks=[]
def check(name,value):
    checks.append({'name':name,'passed':bool(value)})
    assert value,name
for i,p in enumerate(pol):
    check('Ward k1 '+str(i),s.simplify(amp(k1,p))==0)
    check('Ward k2 '+str(i),s.simplify(amp(p,k2))==0)
avg=s.expand(sum(amp(a,b)**2 for a in pol for b in pol)/4)
check('polarization average',s.simplify(avg-32*C*C*E**4)==0)
# Independent covariant contraction of T^{mu nu}, with two physical helicities averaged.
T=dot(k1,k2)*g-k2*k1.T
cov=sum(g[i,i]*g[j,j]*T[i,j]**2 for i in range(4) for j in range(4))*4*C*C
check('covariant vs transverse',s.simplify(cov-avg)==0)
# Integrating PDG d sigma/dt over range Delta t=s beta gives beta |M|^2/(16 pi s).
beta=s.symbols('beta',positive=True)
sigma=s.simplify(avg*beta/(16*s.pi*(4*E**2)))
check('cross section',s.simplify(sigma-C*C*(4*E**2)*beta/(8*s.pi))==0)
# Charge neutrality of each vertex, unlike isolated creation of positive charge.
for name,q in [('cubic',-2+1+1),('phi polarizability',-1+1),('chi polarizability',-2+2)]:
    check(name+' neutral',q==0)
m=1e6; hc=1.973269804e-7; c=299792458.; rows=[]
for kinetic in [0.,1e-6,.001,1.,5.]:
    e=m+kinetic
    b=math.sqrt(kinetic*(2*m+kinetic))/e
    coeff=(4*e*e)*b/(8*math.pi)*hc*hc # sigma in m² if C supplied in eV^-2
    rows.append(dict(kinetic_each_eV=kinetic,photon_each_eV=e,beta=b,speed_m_s=c*b,sigma_m2_per_C_eVminus2_squared=coeff))
    check('mass shell K='+str(kinetic),math.isclose((b*e)**2,kinetic*(2*m+kinetic),rel_tol=1e-12,abs_tol=1e-16))
check('threshold zero',rows[0]['sigma_m2_per_C_eVminus2_squared']==0)
check('optical below threshold',(4*1.8**2)<4*m*m)
out={'checks':checks,'all_pass':all(x['passed'] for x in checks),'averaged_M_squared':str(avg),'sigma_natural':str(sigma),'rows':rows,'minimum_input_J_per_kg_kept_with_equal_discarded_antimatter':2*c*c,'non_claims':['No measured C or full loop form factor','No manufacturing yield, separation, trap or condensate preparation','Not a Lean proof or empirical evidence']}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
