"""Small linear disturbances; exact mode propagation, no simulation imports."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import ast
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SRC = ROOT/'campaign_fresh_gravity/CFG596_lean_pm_1024/cfg596_pm.py'
# Only the exact force-kernel definitions/table assignments, not the PM engine.
tree = ast.parse(SRC.read_text())
names = {'Y_P','H_P','DELTA','LYG','YG','DH_MONO','H_MONO'}
nodes = []
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name in {'h_rar','dh_rar','nu_mono'}:
        nodes.append(n)
    elif isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets):
        nodes.append(n)
env = {'np':np, 'brentq':brentq}
exec(compile(ast.Module(body=nodes,type_ignores=[]), str(SRC), 'exec'), env)
y, h = env['YG'], env['H_MONO']
gtab = y+h
rows = []
checks = []
def check(name, value, tolerance):
    checks.append(dict(name=name, value=float(value), tolerance=tolerance,
                       passed=bool(abs(value)<=tolerance)))

def packet(g0, n):
    b0 = float(np.exp(np.interp(np.log(g0), np.log(gtab), np.log(y))))
    # nu_mono interpolates H linearly in log10(y), so take that exact
    # piecewise derivative at the solved background, away from knots.
    j = np.clip(np.searchsorted(y,b0)-1,0,len(y)-2)
    hp = (h[j+1]-h[j])/np.log(y[j+1]/y[j])/b0
    bp = 1/(1+hp)
    a = 1/(1-bp)
    check('kernel inversion '+str(g0), b0*env['nu_mono'](b0)/g0-1, 1e-7)
    length=512.; dx=length/n; x=(np.arange(n)-n/2)*dx
    k=2*np.pi*np.fft.fftfreq(n,dx)
    # Suppress the Nyquist coefficient to keep differentiated real fields real.
    phi=np.fft.fft(np.exp(-x*x/(2*8.**2)))
    phi[n//2]=0; phi[0]=0
    init=np.stack([phi,1j*k*phi/a],axis=-1)
    H=np.zeros((n,2,2),complex)
    H[:,0,0]=k*k; H[:,1,1]=a
    H[:,0,1]=1j*k; H[:,1,0]=-1j*k
    ev, vec=np.linalg.eigh(H)
    check('nonnegative omega2 '+str((g0,n)),min(0,float(ev.min())),1e-10)
    omega=np.sqrt(np.maximum(ev,0))
    coeff=np.einsum('nji,nj->ni',vec.conj(),init)
    central=abs(x)<24
    samples=[]; initial_energy=None
    for t in (0,50,100,150):
        field=np.einsum('nij,nj->ni',vec,coeff*np.cos(omega*t))
        velocity=np.einsum('nij,nj->ni',vec,-coeff*omega*np.sin(omega*t))
        q=np.fft.ifft(1j*k*field[:,0]).real
        p=np.fft.ifft(field[:,1]).real
        v=np.fft.ifft(velocity,axis=0).real
        energy=.5*((q-p)**2+(a-1)*p*p+np.sum(v*v,axis=1))
        total=float(energy.sum()*dx)
        if t==0:
            initial_energy=total
            check('zero-time identity '+str((g0,n)),np.max(abs(field-init)),1e-10)
        check('energy '+str((g0,n,t)),total/initial_energy-1,1e-9)
        samples.append(dict(time=t,energy=total,central_fraction=float(energy[central].sum()*dx/total)))
    return dict(g=g0,N=n,b=b0,Bprime=bp,long_wave_speed=float(np.sqrt(bp)),
                stiffness=a,samples=samples,local_escape=samples[-1]['central_fraction']<.10)

for g0 in (.001,.01,.1,1.):
    pair=[packet(g0,n) for n in (1024,2048)]
    check('resolution central fractions '+str(g0),max(abs(a['central_fraction']-b['central_fraction'])
          for a,b in zip(pair[0]['samples'],pair[1]['samples'])),.01)
    rows.extend(pair)
k=.1
H=np.array([[k*k,1j*k],[-1j*k,1.]])
check('vacuum stationary null mode',np.linalg.norm(H@np.array([1.,1j*k])),1e-14)
bad=H.copy(); bad[1,1]=.99
negative=float(np.linalg.eigvalsh(bad)[0])
checks.append(dict(name='negative mismatch mutation',value=negative,passed=negative< -1e-6))
out=dict(rows=rows,controls=checks,all_checks_pass=all(c['passed'] for c in checks),
         vacuum='Nonzero null perturbation is stationary in the linearised vacuum model; strict linear attraction absent.',
         interpretation='Finite linear propagation only. Unit response coefficients chosen, not derived. No physical relaxation time inferred.')
(HERE/'run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_checks_pass=out['all_checks_pass'],fine_grid=[r for r in rows if r['N']==2048],mutation=negative),indent=2))
assert out['all_checks_pass']
