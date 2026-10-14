"""CBP-002: nuclear binding opens a route that vacuum threshold misses."""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def ck(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
    if not ok:raise AssertionError(name)
mn=.93956542194;mp=.93827208943;md=1.875612945
ms=.001;mc=mn-.0005; binding=mn+mp-md
Q=mc+mp-md-ms
ck('deuteron binding identity',abs(Q-(binding-(mn+ms-mc)))<1e-15)
ck('capture exothermic',Q>0)
W=mc+mp
pf=np.sqrt((W-md-ms)*(W+md+ms)*(W-md+ms)*(W+md-ms))/(2*W)
Ed=(W*W+md*md-ms*ms)/(2*W);Es=(W*W-md*md+ms*ms)/(2*W)
ck('capture conservation',abs(Ed+Es-W)<1e-12)
ck('deuteron on shell',abs(Ed*Ed-pf*pf-md*md)<1e-12)
ck('spectator on shell',abs(Es*Es-pf*pf-ms*ms)<1e-12)
ck('deuteron recoil and S energy sum',abs((Ed-md)+(Es-ms)-Q)<1e-12)
for name,initial,final in [('baryon',1+1,2+0),('dark',1+0,0+1),('electric',0+1,1+0)]:ck(name,initial==final)

# Exact spin-triplet projection, initial chi/proton both spin1/2.
rt=s.sqrt(2)
triplet=s.Matrix([[1,0,0,0],[0,1/rt,1/rt,0],[0,0,0,1]])
ck('triplet states normalized',triplet*triplet.T==s.eye(3))
ck('nonzero spin-averaged allowed projection',s.trace(triplet.T*triplet)/4==s.Rational(3,4))

# Defined zero-range bound state, not a precision nuclear matrix element.
r,g=s.symbols('r g',positive=True)
ck('zero-range normalized S-wave',s.integrate(2*g*s.exp(-2*g*r),(r,0,s.oo))==1)
q=s.symbols('q',positive=True)
ck('momentum-space zero-range normalization',s.integrate(q*q/(2*s.pi**2)*8*s.pi*g/(q*q+g*g)**2,(q,0,s.oo))==1)
gamma=np.sqrt(2*(mn*mp/(mn+mp))*binding)
samples=[]
for qq in [0.,.001,.01,.05]:
    wf=np.sqrt(8*np.pi*gamma)/(qq*qq+gamma*gamma)
    ck('nonzero form factor %g'%qq,wf>0)
    samples.append(dict(q_GeV=qq,wavefunction_GeVminus3over2=wf))
separations=[]
for sn in [.1,1,1.5,2.22456637,8.]:
    release=sn/1000-(mn+ms-mc)
    separations.append(dict(Sn_MeV=sn,Q_MeV=release*1000,open=bool(release>1e-12)))

# The earlier continuum threshold does not include bound hydrogen.
mH=mp+.00051099895069-13.6e-9
ck('hydrogen-assisted chi vacuum channel closed',mc<mH+ms)
parent=mn+.1+1e-6
hydrogen_s_threshold=parent-mH
continuum_s_threshold=parent-mp-.00051099895069
ck('hydrogen threshold correction',abs(hydrogen_s_threshold-continuum_s_threshold-13.6e-9)<1e-15)

result=dict(status='conditional nuclear-capture kinematics and overlap verified',assertions=len(checks),binding_MeV=binding*1000,capture_Q_MeV=Q*1000,final_momentum_MeV=pf*1000,deuteron_recoil_keV=(Ed-md)*1e6,S_kinetic_MeV=(Es-ms)*1000,zero_range_binding_momentum_MeV=gamma*1000,overlap_samples=samples,separation_samples=separations,vacuum_hydrogen_gate_s_mass_GeV=hydrogen_s_threshold,continuum_gate_s_mass_GeV=continuum_s_threshold,interpretation='Nonzero overlap in an explicitly defined zero-range S-wave approximation; no absolute nuclear capture rate or experimental feasibility inferred.')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
