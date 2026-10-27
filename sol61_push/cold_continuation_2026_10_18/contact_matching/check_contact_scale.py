"""Conditional matching of a dilute scalar contact EOS to fluid pressure length."""
import json
import math
import sys
from pathlib import Path
GSI=6.67430e-11
c=299792458.
hbar=1.054571817e-34
GeV_J=1.602176634e-10
pc=3.0856775814913673e16
ellGeV=hbar*c/GeV_J
GN=GSI*GeV_J**2/(hbar*c**5)
checks=[]
def ck(name,condition):
    assert condition,name
    checks.append(name)

def length_pc(mGeV,lam):
    return math.sqrt(lam/(4*math.pi*GN*mGeV**4))*ellGeV/pc

rows=[]
for mEV in [1.,10.,1e3,1e6,2e6]:
    for lam in [1e-6,.01,1.]:
        m=mEV*1e-9
        L=length_pc(m,lam)
        recovered=4*math.pi*GN*m**4*(L*pc/ellGeV)**2
        ck('inverse coupling '+str((mEV,lam)),math.isclose(recovered,lam,rel_tol=2e-14))
        ck('mass inverse-square scaling '+str((mEV,lam)),math.isclose(length_pc(2*m,lam),L/4,rel_tol=2e-14))
        rows.append(dict(mass_eV=mEV,lambda_NR=lam,L_pressure_pc=L))
inverse=[]
for L in [24.,100.,300.,1000.]:
    mass=(1/(4*math.pi*GN*(L*pc/ellGeV)**2))**.25
    ck('unit-coupling mass ceiling '+str(L),math.isclose(length_pc(mass,1.),L,rel_tol=2e-14))
    for mEV in [1e6,2e6]:
        m=mEV*1e-9
        lam=4*math.pi*GN*m**4*(L*pc/ellGeV)**2
        ck('required coupling inversion '+str((L,mEV)),math.isclose(length_pc(m,lam),L,rel_tol=2e-14))
        inverse.append(dict(L_pressure_pc=L,mass_eV=mEV,required_lambda_NR=lam,mass_ceiling_eV_if_lambda_NR_le1=mass*1e9))
ck('GeV inverse conversion',1.9732e-16<ellGeV<1.9734e-16)
ck('natural gravitational constant range',6.70e-39<GN<6.72e-39)
out=dict(claim_id='CE-CONT-CONTACT-SCALE-2026-10-18',n_checks=len(checks),checks=checks,
         constants=dict(G_SI=GSI,hbar_J_s=hbar,c_m_s=c,GeV_J=GeV_J,pc_m=pc,G_GeV_minus2=GN,GeV_inv_m=ellGeV),
         derivation=['e=lambda_NR n²/(4m²)=lambda_NR rho²/(4m⁴)','kappa_fluid=lambda_NR/(2m⁴)','H_contact=kappa_fluid/(4piG)','L_contact²=2H_contact=lambda_NR/(4piGm⁴)'],rows=rows,inverse=inverse,
         non_claims=['lambda_NR<=1 is a chosen weak-contact regime, not a universal unitarity or observational bound','Pressure matching alone does not derive rational W or current constraint','Fragments, other phases, additional stiffness, relativistic/in-medium interactions can change the matching','No claimed carrier mass or experimental constraint'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(n_checks=len(checks),inverse=inverse),indent=2))
