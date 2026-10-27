"""Exploratory reduced-model checks; not a relativistic or observational test."""
import json
from pathlib import Path
import numpy as np
import sympy as s

out = Path(__file__).parent / 'run'
checks = []
def check(name, passed, value=None):
    checks.append(dict(name=name, passed=bool(passed), value=value))

G, q, n, b, a0, r, M, alpha, a, beta, B, gamma = s.symbols(
    'G q n b a0 r M alpha a beta B gamma', positive=True)
g = n + 4*s.pi*G*q
U = 2*s.pi*G*q*q+b*q**3/3
reduced = s.expand(U-g*g/(8*s.pi*G)+n*n/(8*s.pi*G))
check('longitudinal constraint energy', s.simplify(reduced-(b*q**3/3-n*q)) == 0)
check('spherical stationary equation', s.simplify(s.diff(reduced,q)-(b*q*q-n)) == 0)
check('BTFR coefficient', s.simplify((4*s.pi*G)**2*G*M/(16*s.pi**2*G**2/a0)-G*M*a0) == 0)
v2 = alpha*B/a
mass = 4*s.pi*a*beta*B**2/alpha
check('old scalar cubic energy normalization', s.simplify(beta*B**3/3-mass*v2/(12*s.pi)) == 0)
p = B/r-gamma/(beta*r*r)
energy = beta*p**3/3+gamma*(s.diff(p,r)**2+2*p*p/r**2)/2
t = s.symbols('t')
series = s.series(energy.subs(r,1/t),t,0,5).removeO()
check('stiffness subleading energy', s.simplify(series-(beta*B**3*t**3/3+gamma*B**2*t**4/2)) == 0)

# Periodic discrete Helmholtz decomposition, odd grid avoids Nyquist ambiguity.
rng = np.random.default_rng(120126)
N = 9
k1 = np.fft.fftfreq(N)*N
k = np.array(np.meshgrid(k1,k1,k1,indexing='ij'))
k2 = np.sum(k*k,axis=0)
safe = np.where(k2>0,k2,1)
Q = rng.normal(size=(3,N,N,N))
Qk = np.fft.fftn(Q,axes=(1,2,3))
QLk = k*np.sum(k*Qk,axis=0)/safe
QL = np.fft.ifftn(QLk,axes=(1,2,3)).real
QT = Q-QL
phi = rng.normal(size=(N,N,N))
gn = np.fft.ifftn(1j*k*np.fft.fftn(phi),axes=(1,2,3)).real
Gn = 0.7
bn = 1.3
norm = np.sqrt(np.sum(Q*Q,axis=0))
metric_g = gn+4*np.pi*Gn*QL
raw = np.mean(2*np.pi*Gn*norm**2+bn*norm**3/3-np.sum(metric_g**2,axis=0)/(8*np.pi*Gn))
red = np.mean(2*np.pi*Gn*np.sum(QT**2,axis=0)+bn*norm**3/3-np.sum(Q*gn,axis=0)-np.sum(gn**2,axis=0)/(8*np.pi*Gn))
check('3D raw vs reduced energy', abs(raw-red)<1e-10, float(abs(raw-red)))
orth = np.mean(np.sum(QL*QT,axis=0))
check('Helmholtz orthogonality', abs(orth)<1e-12, float(abs(orth)))

min_eig = float('inf')
count = 0
for amp in [0.,1e-6,.01,1.,100.]:
    for wave in [0.001,.1,1.,100.]:
        for angle in np.linspace(0,np.pi,7):
            v = np.array([np.sin(angle),0.,np.cos(angle)])
            H = 4*np.pi*Gn*np.diag([1.,1.,0.])+bn*amp*(np.eye(3)+np.outer(v,v))+.2*wave**2*np.eye(3)
            ev = np.linalg.eigvalsh(H)
            min_eig = min(min_eig,float(ev[0]))
            count += 1
check('positive reduced Hessian sample', min_eig>0, dict(matrices=count,minimum=min_eig))
# A below-critical quadratic coefficient must produce a vacuum long-wave instability.
mutant = np.linalg.eigvalsh(4*np.pi*Gn*(np.diag([1.,1.,0.])-.01*np.eye(3))+.2*.001**2*np.eye(3))[0]
check('negative critical mismatch detected', mutant<0, float(mutant))
# Flipping the gravitational sign must spoil the cancellation.
wrong = s.expand(U+g*g/(8*s.pi*G)-n*n/(8*s.pi*G))
check('wrong gravity sign rejected', s.diff(wrong,q,2).subs(q,0) != 0)

SI_G, c, solar, kpc = 6.67430e-11,299792458.,1.98847e30,3.085677581491367e19
ratios = [dict(M_solar=m,r_kpc=rr,energy_density_over_required_density=SI_G*m*solar/(3*c*c*rr*kpc))
          for m in [1e10,1e11] for rr in [30.,100.]]
result = dict(checks=checks,all_pass=all(x['passed'] for x in checks),energy_ratios=ratios,
              scope='Fixed sources, instantaneous Newtonian constraint, chosen positive polarization inertia. No lensing, relativistic cone, formation, or live-matter stability verification.')
out.mkdir(exist_ok=True)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['all_pass'] else 1)
