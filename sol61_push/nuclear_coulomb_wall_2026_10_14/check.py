import math,json,sys
from pathlib import Path
from scipy.integrate import quad
from scipy.optimize import brentq
import numpy as np
hc=1.973269804e-7; alpha=1/137.035999084; NA=6.02214076e23
m=1.; MR=2.; g=1e-20; Z=82; rms=5.5062e-15
radius=math.sqrt(5/3)*rms
# Natural-lead number density with a Pb-208 radius proxy, explicitly approximate.
n=11350/.2072*NA; nn=n*hc**3
EC=3*Z*(Z-1)*alpha*hc/(5*radius)
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
average=quad(lambda x:3*x*x*(3-x*x)/2,0,1)[0]
ck('uniform_sphere_pair_energy',abs(average/2-3/5),1e-14)
Rbulk=g*EC*nn/(MR*MR)
# Planar Yukawa smoothing, dimensionless coordinate X=MR*x.
for X in [-3.,-1.,0.,1.,3.]:
    numeric=quad(lambda y:.5*math.exp(-abs(X-y)),0,max(40,X+40),points=[X] if X>0 else None,epsabs=1e-12)[0]
    exact=.5*math.exp(X) if X<=0 else 1-.5*math.exp(-X)
    ck('planar_Yukawa_matching',abs(numeric-exact),2e-12)
rows=[]
a=.01; localization=math.pi**2*hc**2/(8*m*a*a)
for lam in [1e-6,1e-15]:
    mu=math.sqrt(lam)*MR
    U=mu*g*EC*nn/(2*m*MR*MR)
    ck('tadpole_vs_effective_potential',abs(U/(mu*Rbulk/(2*m))-1),1e-14)
    C=-mu*g/(4*MR*MR); magnetic=abs(C*(195.3527711*10)**2/m)
    bound=U>localization
    row=dict(lambda_rep=lam,mu_eV=mu,Coulomb_only_wall_eV=U,
             magnetic_10T_depth_eV=magnetic,sphere_radius_m=a,
             infinite_wall_supports_s_state=bound)
    if bound:
        z0=a*math.sqrt(2*m*U)/hc
        x=brentq(lambda x:x/math.tan(x)+math.sqrt(z0*z0-x*x),math.pi/2+1e-10,min(math.pi-1e-10,z0-1e-10),xtol=1e-14)
        ck('spherical_level_matching',abs(x/math.tan(x)+math.sqrt(z0*z0-x*x)),2e-10)
        row['spherical_ground_energy_eV']=hc*hc*x*x/(2*m*a*a)
    row['planar_transmission']=[]
    for E in [1e-9,1e-8]:
        if E>=U:continue
        for d in [.001,.01]:
            q=math.sqrt(2*m*(U-E))/hc
            T=1/(1+U*U*math.sinh(q*d)**2/(4*E*(U-E)))
            row['planar_transmission'].append(dict(E_eV=E,thickness_m=d,T=T))
            if d==.001:
                kin=math.sqrt(2*m*E)/hc; ep=math.exp(q*d); em=1/ep
                mat=np.array([[1,-1,-1,0],[-1j*kin,-q,q,0],[0,ep,em,-1],[0,q*ep,-q*em,-1j*kin]],complex)
                rhs=np.array([-1,-1j*kin,0,0],complex)
                reflected,aa,bb,transmitted=np.linalg.solve(mat,rhs)
                ck('barrier_four_boundary_matching',abs(abs(transmitted)**2/T-1),1e-12)
                ck('barrier_flux_conservation',abs(abs(reflected)**2+abs(transmitted)**2-1),1e-12)
    rows.append(row)
mu_needed=1e-8*2*m*MR*MR/(g*EC*nn)
result=dict(material_inputs=dict(density_kg_per_m3=11350,molar_mass_kg_per_mol=.2072,
    Pb208_rms_radius_m=rms,uniform_sphere_radius_m=radius),
    assumptions='Local RF^2 valid through nuclear momenta; Coulomb-only material response; no independent counterterm cancellation',
    Coulomb_pair_energy_eV=EC,nuclei_per_m3=n,bulk_R_eV=Rbulk,mediator_range_m=hc/MR,
    inverse_nuclear_radius_eV=hc/radius,
    cm_sphere_threshold_eV=localization,
    mu_for_10neV_barrier_eV=mu_needed,lambda_for_10neV_barrier=mu_needed**2/MR**2,
    cases=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
