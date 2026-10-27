"""Independent reconstruction from the potential and saved branch inputs.

Does not import the implementation under review or rerun its spectra.
"""
import hashlib
import json
import sys
from pathlib import Path
import sympy as s
import numpy as np

root = Path.cwd()
source = root/'sol61_push/closure_particle_bridge_2026_10_16/mediator_phase_matching_run_002/results.json'
checks=[]
def zero(name, value):
    assert s.factor(value)==0, (name,value)
    checks.append({'name':name,'pass':True,'kind':'exact_identity'})
def close(name,value,target):
    assert abs(value-target)<2e-7,(name,value,target)
    checks.append({'name':name,'pass':True,'kind':'saved_row_numeric'})

rho, X, chi, lam, aa, MM, mu = s.symbols('rho X chi lambda a M mu',real=True)
II=rho*rho/2
V=II+lam*II*II+aa*chi*II+MM*MM*chi*chi/2+mu*chi**3/3+chi**4/4
grand=V-II*X
stationary={X:1+2*lam*II+aa*chi}
zero('canonical radial Hessian',s.diff(grand,rho,2).subs(stationary)-4*lam*II)
zero('canonical radial mediator mixing',s.diff(grand,rho,chi)-aa*rho)
Bh=s.diff(grand,chi,2)
zero('negative-chi mediator curvature',Bh.subs({mu:-3*MM/8,chi:-s.Symbol('x')})-(MM*MM+3*MM*s.Symbol('x')/4+3*s.Symbol('x')**2))
Ar,BB,hh,kap,xx,ss=s.symbols('Ar B h kappa X s',positive=True)
H=s.Matrix([[Ar,hh],[hh,BB]])
Q=(Ar+ss)*(BB+ss)-hh*hh
inverse=(H+ss*s.eye(2)).inv()[0,0]
zero('Schur inverse amplitude kernel',inverse-(BB+ss)/Q)
Aeff=Ar-hh*hh/BB
zero('adiabatic Schur compressibility',inverse.subs(ss,0)-1/Aeff)
delta=4*kap*xx*inverse
zero('first dispersive kernel derivative',s.diff(delta,ss).subs(ss,0)+4*kap*xx*(BB*BB+hh*hh)/(Ar*BB-hh*hh)**2)
A,C,E,d,T,z,K,D0,D1,b,cs=s.symbols('A C E d T z K Delta0 Delta1 b cs',real=True)
f=(A*z-C)*((kap+D0)*z-E)-d*d*T*z
reduced=(A*z-C)*((kap+D0-D1*(1-z)*K)*z-E)-d*d*T*z
coef=s.diff(reduced.subs(z,cs+b*K),K).subs(K,0)
zero('low-mode k4 shift equation',coef-(s.diff(f,z).subs(z,cs)*b-D1*(A*cs-C)*cs*(1-cs)))
QK=(Ar+K-z)*(BB+K-z)-hh*hh
full=(A*z-C*K)*((kap*z-E*K)*QK+4*kap*xx*z*(BB+K-z))-d*d*z*K*T*QK
zero('zero-wave physical gaps',full.subs(K,0)/(A*kap*z*z)-((Ar+4*xx-z)*(BB-z)-hh*hh))
g,y,Z=s.symbols('gamma y Z0',positive=True)
q=Z+g*y
rr=q*y*y/xx
sub={A:Z+2*g*y,C:g*y*(1+T),E:kap-rr*T,d*d:q*rr}
cone=s.expand(full.subs(z,K)/(K*K*(Ar*BB-hh*hh)))
cone=s.factor(cone.subs(sub))
zero('all-frequency light-cone identity',cone-(4*kap*xx/Aeff*(q-g*y*T)-g*y*rr*T*T))
front=s.factor(((A-C)*(kap-E)-d*d*T).subs(sub).subs(T,1))
zero('radial principal negative determinant',front+g*q*y**3/xx)

# Derive the large-M expansion from the coexistence polynomial directly.
t,c=s.symbols('t c',real=True)
x=1+c*t
ell=2-t
pol=ell*x**4*t**3+3*ell*x**3*t**2/4+(137*ell/64-1)*x*x*t+(3*ell/4-s.Rational(1,2))*x-1
zero('large-M coexistence first correction',s.diff(pol,t).subs({t:0,c:-s.Rational(81,32)}))
xxexp=1-s.Rational(81,32)*t
Ibar=s.sqrt((xxexp*xxexp/2+t*xxexp**3/8+t*t*xxexp**4/4)/(2-t))
zero('large-M I leading coefficient',Ibar.subs(t,0)-s.Rational(1,2))
zero('large-M I constant correction',s.diff(Ibar,t).subs(t,0)+s.Rational(69,64))

rows=json.loads(source.read_text())['rows']
expected={1:(.58239319,1.24988856,1.0619341,5.8777788),10:(.85761376,1.76202050,8.7031882,28.2248769),100:(.98080432,1.96560586,97.9786194,295.5389269),1000:(.99800837,1.99638083,997.8581013,2995.0306121)}
numeric=[]
for row in rows:
    M=row['M_over_m'];I=row['phase_I_exact'];x=row['phase_negative_chi'];X=row['omega_squared_exact']
    mat=np.array([[4*(2-1/M)*I,2*M*np.sqrt(2*I)],[2*M*np.sqrt(2*I),M*M+3*M*x/4+3*x*x]])
    ae=mat[0,0]-mat[0,1]**2/mat[1,1]
    values=(np.sqrt(np.linalg.eigvalsh(mat)[0]),np.sqrt(np.linalg.eigvalsh(mat+np.diag([4*X,0]))[0]),2*I,8*I*X/ae)
    for name,val,target in zip(('kernel gap','physical gap','kappa','Delta0'),values,expected[int(M)]):
        close('saved M '+str(M)+' '+name,float(val),target)
    numeric.append({'M':M,'kernel_gap':values[0],'physical_gap':values[1],'kappa':values[2],'Delta0':values[3]})

out={'claim_id':'CE-CONT-CLOCK-INDEPENDENT-REVIEW','status':'completed','n_checks':len(checks),'all_pass':True,'checks':checks,'numeric_reconstruction':numeric,'saved_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scope':'Independent analytic-reconstruction controls and saved branch table reconstruction; no rerun or independent certification of 1224 spectra or reported group-speed crossing.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
