"""Prescribed source assembly, with its external work explicitly recorded.

This is a finite experiment on the existing effective response model.
No baryon dynamics, drag, cold mass, or metric completion is introduced.
"""
import ast
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / 'campaign_fresh_gravity/CFG596_lean_pm_1024/cfg596_pm.py'
names = {'Y_P', 'H_P', 'DELTA', 'LYG', 'YG', 'DH_MONO', 'H_MONO'}
nodes = [n for n in ast.parse(SRC.read_text()).body if
         (isinstance(n, ast.FunctionDef) and n.name in {'h_rar', 'dh_rar', 'nu_mono'}) or
         (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets))]
env = {'np': np, 'brentq': brentq}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SRC), 'exec'), env)
pt = np.r_[0., env['H_MONO']]
bt = np.r_[0., env['YG']]
assert np.all(np.diff(pt) > 0) and np.all(np.diff(bt) > 0)
sl = np.diff(bt) / np.diff(pt)
wt = np.r_[0., np.cumsum(.5 * (bt[1:] + bt[:-1]) * np.diff(pt))]


def W(p):
    z = abs(p)
    j = np.clip(np.searchsorted(pt, z) - 1, 0, len(pt) - 2)
    d = z - pt[j]
    return wt[j] + bt[j] * d + .5 * sl[j] * d*d


def b(p):
    return np.sign(p) * np.interp(abs(p), pt, bt)


def ramp(t, T):
    if T == 0 or t >= T:
        return 1., 0.
    s = max(0., t / T)
    return s*s*s*(10-15*s+6*s*s), 30*s*s*(1-s)**2/T


checks = []


def check(name, value, tol):
    checks.append(dict(name=name, value=float(value), tolerance=tol,
                       passed=bool(np.isfinite(value) and abs(value) <= tol)))


def run(T, R, n, dt):
    dr = R/n
    rf = np.arange(n+1)*dr
    r = (rf[:-1]+rf[1:])/2
    vol = np.diff(rf**3)/3
    length = np.full(n, dr)
    length[-1] = dr/2
    area = rf[1:]**2
    fw = area*length
    rho = np.where(r < 8, np.exp(-r*r/8), 0.)
    rho /= np.dot(rho, vol)
    d0 = np.cumsum(rho*vol)/area
    p0 = np.interp(d0, bt, pt)
    g0 = d0+p0
    phi0 = -np.cumsum((g0*length)[::-1])[::-1]

    def grad(phi):
        return (np.r_[phi[1:], 0.] - phi)/length

    def div(f):
        return np.diff(np.r_[0., area*f])/vol

    def acc(phi, p, lam):
        q = grad(phi)
        return div(q-p)-lam*rho, q-p-b(p)

    def energy(phi, p, v, w, lam):
        q = grad(phi)
        return float(np.dot(.5*v*v+lam*rho*phi, vol) +
                     np.dot(.5*w*w+.5*(q-p)**2+W(p), fw))

    zero = np.zeros(n)
    hs = energy(phi0, p0, zero, zero, 1.)
    assert hs < 0
    norm = abs(hs)
    ar, ap = acc(phi0, p0, 1.)
    tag = str((T, R, n, dt))
    check('static residual '+tag, max(np.max(abs(ar)), np.max(abs(ap))), 1e-7)
    ar, ap = acc(zero, zero, 0.)
    check('no source zero RHS '+tag, max(np.max(abs(ar)), np.max(abs(ap))), 1e-14)
    # Deterministic arbitrary fields check the discrete integration-by-parts identity.
    testphi = np.sin(r/(1+R))
    testflux = np.cos(rf[1:]/(1+R))
    ibp = np.dot(testphi*div(testflux), vol)+np.dot(grad(testphi)*testflux, fw)
    check('adjoint identity '+tag, ibp/(1+R**2), 1e-12)

    phi, p, v, w = [zero.copy() for _ in range(4)]
    lam, ld = ramp(0., T)
    af, ap = acc(phi, p, lam)
    work = 0.
    power = 0.
    end = T+640
    sel = (rf[1:] >= 2) & (rf[1:] <= 20)
    samples = []
    snapshots = []
    maxe = 0.
    maxp = 0.
    for step in range(round(end/dt)+1):
        t = step*dt
        if step % round(10/dt) == 0:
            q = grad(phi)
            h = energy(phi, p, v, w, lam)
            ee = (h-work)/norm
            maxe = max(maxe, abs(ee))
            samples.append(dict(time=t, mass_fraction=lam,
                force_rms_fractional_error=float(np.sqrt(np.mean(((q[sel]-g0[sel])/g0[sel])**2))),
                min_force=float(q[sel].min()), energy=h, external_work=work,
                work_balance_error=ee, excess_above_final_static=(h-hs)/norm))
            if t >= end-80:
                snapshots.append(q[sel].copy())
        if step == round(end/dt):
            break
        v += .5*dt*af
        w += .5*dt*ap
        phi += dt*v
        p += dt*w
        maxp = max(maxp, float(np.max(abs(p))))
        lam, ld = ramp((step+1)*dt, T)
        newpower = ld*float(np.dot(rho*phi, vol))
        work += .5*dt*(power+newpower)
        power = newpower
        af, ap = acc(phi, p, lam)
        v += .5*dt*af
        w += .5*dt*ap
    check('work balance '+tag, maxe, .002)
    check('table upper support '+tag, max(0., maxp/pt[-1]-1), 0.)
    late = [s for s in samples if s['time'] >= end-80]
    return dict(T=T, R=R, N=n, dt=dt, end=end, samples=samples,
        formation=all(s['force_rms_fractional_error'] <= .1 and s['min_force'] >= 0 for s in late),
        worst_late_error=max(s['force_rms_fractional_error'] for s in late),
        static_energy=hs, max_work_balance_error=maxe, max_p=maxp,
        r=rf[1:][sel].tolist(), force=grad(phi)[sel].tolist(),
        target=g0[sel].tolist(), late_force=[a.tolist() for a in snapshots])


mode = sys.argv[1]
outdir = HERE/sys.argv[2]
if mode == 'screen':
    rows = []
    for T in (0, 80, 320):
        row = run(T, 768, 6144, .02)
        rows.append(row)
        print(json.dumps({k: row[k] for k in ('T', 'formation', 'worst_late_error', 'max_work_balance_error')}), flush=True)
    selected = min(rows, key=lambda row: row['worst_late_error'])['T']
elif mode == 'verify':
    prior = json.loads((HERE/'screen/results.json').read_text())
    selected = prior['selected_T']
    coarse = next(row for row in prior['rows'] if row['T'] == selected)
    rows = [run(selected, 768, 12288, .01), run(selected, 1536, 12288, .02)]
    for label, row in zip(('refinement', 'outer boundary'), rows):
        differences = [np.linalg.norm(np.interp(coarse['r'], row['r'], f)-np.array(c))/np.linalg.norm(coarse['target'])
                       for f, c in zip(row['late_force'], coarse['late_force'])]
        check(label+' all late force profiles', max(differences), .03)
        check(label+' worst late RMS difference', abs(row['worst_late_error']-coarse['worst_late_error']), .03)
else:
    raise ValueError(mode)
out = dict(rows=rows, selected_T=selected, checks=checks,
           all_checks_pass=all(c['passed'] for c in checks))
(outdir/'results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(dict(selected_T=selected, checks=checks,
    summaries=[{k: r[k] for k in ('T','R','N','formation','worst_late_error','max_work_balance_error')} for r in rows]), indent=2), flush=True)
assert out['all_checks_pass']
