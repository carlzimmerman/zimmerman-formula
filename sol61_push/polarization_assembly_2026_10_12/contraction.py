"""Fixed-mass homologous baryon contraction; prescribed motion, accounted work."""
import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
tree = ast.parse((HERE/'calculate.py').read_text())
prefix = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'mode' for t in node.targets):
        break
    prefix.append(node)
env = {'__file__': str(HERE/'calculate.py')}
exec(compile(ast.Module(body=prefix, type_ignores=[]), str(HERE/'calculate.py'), 'exec'), env)
np, b, W, check = (env[k] for k in ('np', 'b', 'W', 'check'))
pt, bt = env['pt'], env['bt']


def run(n, dt):
    R, T, end = 768., 320., 960.
    dr = R/n
    rf = np.arange(n+1)*dr
    r = (rf[:-1]+rf[1:])/2
    vol = np.diff(rf**3)/3
    length = np.full(n, dr)
    length[-1] = dr/2
    area = rf[1:]**2
    fw = area*length

    def rho_at(t):
        lam, ld = env['ramp'](t, T)
        a = 16.-15.*lam
        rho = np.where(r < 8*a, np.exp(-r*r/(8*a*a)), 0.)
        rho /= np.dot(rho, vol)
        return rho, a

    def grad(phi):
        return (np.r_[phi[1:], 0.] - phi)/length

    def div(f):
        return np.diff(np.r_[0., area*f])/vol

    def acc(phi, p, rho):
        q = grad(phi)
        return div(q-p)-rho, q-p-b(p)

    def energy(phi, p, v, w, rho):
        q = grad(phi)
        return float(np.dot(.5*v*v+rho*phi, vol)+np.dot(.5*w*w+.5*(q-p)**2+W(p), fw))

    def static(rho):
        d = np.cumsum(rho*vol)/area
        p = np.interp(d, bt, pt)
        g = d+p
        phi = -np.cumsum((g*length)[::-1])[::-1]
        return phi, p, g

    rho, a = rho_at(0.)
    phi, p, gi = static(rho)
    rhof, _ = rho_at(T)
    phis, ps, gs = static(rhof)
    zero = np.zeros(n)
    v, w = zero.copy(), zero.copy()
    hi = energy(phi, p, v, w, rho)
    hs = energy(phis, ps, v, w, rhof)
    norm = abs(hs)
    for name, f, z, src in [('initial', phi, p, rho), ('final', phis, ps, rhof)]:
        u, h = acc(f, z, src)
        check(name+' static residual '+str(n), max(np.max(abs(u)), np.max(abs(h))), 1e-7)
    af, ap = acc(phi, p, rho)
    work = 0.
    maxe, maxmass, maxp = 0., 0., 0.
    sel = (rf[1:] >= 2)&(rf[1:] <= 20)
    samples, late_force = [], []
    for step in range(round(end/dt)+1):
        t = step*dt
        if step % round(10/dt) == 0:
            q = grad(phi)
            h = energy(phi, p, v, w, rho)
            ee = (h-hi-work)/norm
            maxe = max(maxe, abs(ee))
            samples.append(dict(time=t, scale=a, baryon_mass=float(np.dot(rho, vol)),
                force_rms_fractional_error=float(np.sqrt(np.mean(((q[sel]-gs[sel])/gs[sel])**2))),
                min_force=float(q[sel].min()), energy=h, external_work=work,
                work_balance_error=ee, excess_above_final_static=(h-hs)/norm))
            if t >= end-80:
                late_force.append(q[sel].tolist())
        if step == round(end/dt):
            break
        v += .5*dt*af
        w += .5*dt*ap
        oldphi = phi.copy()
        phi += dt*v
        p += dt*w
        newrho, a = rho_at((step+1)*dt)
        # Discrete source-work line integral: also accounts for the moving cut edge.
        work += float(np.dot((newrho-rho)*.5*(oldphi+phi), vol))
        rho = newrho
        maxmass = max(maxmass, abs(float(np.dot(rho, vol))-1))
        maxp = max(maxp, float(np.max(abs(p))))
        af, ap = acc(phi, p, rho)
        v += .5*dt*af
        w += .5*dt*ap
    check('mass conservation '+str(n), maxmass, 1e-12)
    check('work balance '+str(n), maxe, .002)
    check('table upper support '+str(n), max(0., maxp/pt[-1]-1), 0.)
    late = [s for s in samples if s['time'] >= end-80]
    return dict(R=R,N=n,dt=dt,T=T,end=end,samples=samples,
        initial_energy=hi,final_static_energy=hs,
        worst_late_error=max(s['force_rms_fractional_error'] for s in late),
        formation=all(s['force_rms_fractional_error']<=.1 and s['min_force']>=0 for s in late),
        max_mass_error=maxmass,max_work_balance_error=maxe,
        r=rf[1:][sel].tolist(),target=gs[sel].tolist(),late_force=late_force)


rows = []
for n, dt in [(6144,.02),(12288,.01)]:
    row = run(n,dt)
    rows.append(row)
    print(json.dumps({k:row[k] for k in ('N','formation','worst_late_error','max_mass_error','max_work_balance_error')}),flush=True)
coarse,fine=rows
diffs=[np.linalg.norm(np.interp(coarse['r'],fine['r'],f)-np.array(c))/np.linalg.norm(coarse['target'])
       for f,c in zip(fine['late_force'],coarse['late_force'])]
check('all late force refinement',max(diffs),.03)
check('worst RMS refinement',abs(fine['worst_late_error']-coarse['worst_late_error']),.03)
out=dict(rows=rows,checks=env['checks'],all_checks_pass=all(c['passed'] for c in env['checks']))
(HERE/'contraction/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['checks'],indent=2),flush=True)
assert out['all_checks_pass']
