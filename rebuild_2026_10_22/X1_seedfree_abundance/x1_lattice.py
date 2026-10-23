"""X1 E1: truncated-Wigner (TW) 3D expanding lattice from the actual high-H state, no seed (FROZEN_CRITERIA §2).

Conformal fields phi = a Phi/H_inf, x = a X/H_inf; tau = H_inf eta; comoving k in units of a_e H_inf; a = 1 + tau
(instant reheating). Initial state: box zero mode from the stochastic box ensemble (x1_stochastic.py), every other lattice
mode from the de Sitter Bunch-Davies Hankel state at the end of inflation sampled as a Wigner Gaussian (half-quanta).
Weyl counterterm of normal ordering w.r.t. the massless conformal lattice vacuum. Velocity Verlet (C kernel).

Job contract (compute_queue/JOB_CONTRACT.md): SIGTERM/SIGINT -> checkpoint at the next step boundary -> exit 75;
--resume exits 0 at once if the result exists, else continues from the newest checkpoint (bit-identical), else starts;
outputs and checkpoints written atomically (tmp + fsync + os.replace); rolling checkpoint every --ckpt-every outputs.

Usage: python3 x1_lattice.py --job NAME --N 64 [--L 78.54] [--variant TW_full|TW_kc|CSA|XI16] [--patch p50]
       [--seed 1] [--tau-end 2000] [--dt-div 20] [--out-every 10] [--threads 1] [--resume] [--stop-after-steps K]
"""
import argparse, ctypes, json, os, signal, subprocess, sys, time
from pathlib import Path
import numpy as np
from scipy.special import hankel1, h1vp
import scipy.fft as sfft

HERE = Path(__file__).resolve().parent
m = .001; M = 2*m*np.sqrt(1+.02**2); g = 2.168e-6; lam = .00881292
H_PRIMARY = 1.3445177278709404e10
YIELD_EXIT = int(os.environ.get('HEAVYQ_YIELD_EXIT', '75'))
STOP = []


def kernel():
    so = HERE/'x1_lattice_kernel.so'; src = HERE/'x1_lattice_kernel.c'
    if not so.exists() or so.stat().st_mtime < src.stat().st_mtime:
        tmp = HERE/f'x1_lattice_kernel.{os.getpid()}.so'
        subprocess.check_call(['cc', '-O2', '-fcx-limited-range', '-fPIC', '-shared', '-o', str(tmp), str(src), '-lpthread'])
        os.replace(tmp, so)
    lib = ctypes.CDLL(str(so))
    P = np.ctypeslib.ndpointer(dtype=np.complex128, flags='C_CONTIGUOUS')
    D = np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS')
    lib.x1_force.argtypes = [ctypes.c_int, ctypes.c_double, P, P, P, P, ctypes.c_double, ctypes.c_double, ctypes.c_double,
                             ctypes.c_double, ctypes.c_double, ctypes.c_int]
    lib.x1_steps.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int, P, P, P, P, P, P, D, D, D,
                             ctypes.c_double, ctypes.c_double, ctypes.c_int]
    return lib


def atomic_write_bytes(path, data):
    tmp = Path(str(path)+f'.tmp{os.getpid()}')
    with open(tmp, 'wb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def atomic_savez(path, **arrs):
    tmp = Path(str(path)+f'.tmp{os.getpid()}.npz')
    with open(tmp, 'wb') as f:
        np.savez(f, **arrs); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def background(tau, xi):
    a = 1.+tau                     # instant reheating: radiation era from the end of inflation, a'' = 0
    add = 0.                       # (1-6 xi) a''/a = 0 in radiation
    return a, add


def kgrid(N, L):
    dx = L/N; k1 = 2*np.pi*np.fft.fftfreq(N, d=dx)
    s = (2/dx*np.sin(k1*dx/2))**2
    klat2 = s[:, None, None]+s[None, :, None]+s[None, None, :]
    return np.sqrt(klat2), dx


def mode_functions(k, nu):
    """Conformal dS mode v and v' at eta = -1 (a = 1, H = 1) for index nu; k > 0 array."""
    ph = np.sqrt(np.pi)/2*np.exp(1j*np.pi*(nu/2+.25))
    return ph*hankel1(nu, k), ph*(-hankel1(nu, k)/2-k*h1vp(nu, k))


def real_field(rng, v, vp, V, mask):
    """Real field f(x) and f'(x) with Fourier modes sqrt(V)(v alpha_k + v* conj(alpha_{-k})), <|alpha|^2> = 1/2."""
    N = v.shape[0]
    al = (rng.standard_normal(v.shape)+1j*rng.standard_normal(v.shape))/2
    alm = np.conj(np.roll(al[::-1, ::-1, ::-1], 1, axis=(0, 1, 2)))      # conj(alpha_{-k})
    ft = np.sqrt(V)*(v*al+np.conj(v)*alm)*mask; fp = np.sqrt(V)*(vp*al+np.conj(vp)*alm)*mask
    dx3 = V/N**3
    return np.fft.ifftn(ft).real/dx3, np.fft.ifftn(fp).real/dx3


def build_ic(spec):
    N, L = spec['N'], spec['L']; k, dx = kgrid(N, L); V = L**3
    rng = np.random.default_rng(spec['seed'])
    kk = k.copy(); kk[0, 0, 0] = 1.
    if spec['variant'] == 'XI16':
        vL = vT = vX = np.exp(1j*kk)/np.sqrt(2*kk); vpL = vpT = vpX = -1j*kk*vL
        z0 = dict(phi0=[0, 0], pi0=[0, 0], x0=[0, 0], px0=[0, 0]); f0 = 0.
    else:
        st = json.loads((HERE/f"x1_stochastic_kmin{2*np.pi/L:.2g}_Ne60.json").read_text())
        z0 = st['box']['zero_modes'][spec['patch']]
        f0 = np.hypot(*z0['phi0'])*np.sqrt(2)                  # canonical real amplitude f = sqrt2 |Phi|/H
        nuL = np.sqrt(9/4-3*lam*f0**2+0j); nuT = np.sqrt(9/4-lam*f0**2+0j)
        vL, vpL = mode_functions(kk, nuL.real); vT, vpT = mode_functions(kk, nuT.real); vX, vpX = mode_functions(kk, 1.5)
    mask = np.ones_like(k); mask[0, 0, 0] = 0
    if spec['variant'] == 'TW_kc': mask[k > 2.] = 0
    if spec['variant'] == 'CSA': mask[k >= 1.] = 0
    f1, p1 = real_field(rng, vL, vpL, V, mask); f2, p2 = real_field(rng, vT, vpT, V, mask)
    x1, q1 = real_field(rng, vX, vpX, V, mask); x2, q2 = real_field(rng, vX, vpX, V, mask)
    phi = (f1+1j*f2)/np.sqrt(2)+complex(*z0['phi0']); pphi = (p1+1j*p2)/np.sqrt(2)+complex(*z0['pi0'])
    x = (x1+1j*x2)/np.sqrt(2)+complex(*z0['x0']); px = (q1+1j*q2)/np.sqrt(2)+complex(*z0['px0'])
    kpop = k[mask > 0]
    c = float(np.sum(1/(2*kpop))/V)
    Evac = float(2*np.sum(kpop)/V-2*lam*c*c)
    meta = dict(c=c, Evac=Evac, populated_modes=int(mask.sum()), f0=float(f0), zero_mode=z0, dx=dx)
    return [np.ascontiguousarray(a, dtype=np.complex128) for a in (phi, pphi, x, px)], meta


class Diag:
    def __init__(self, spec, meta):
        self.spec = spec; self.meta = meta; N, L = spec['N'], spec['L']
        self.k, self.dx = kgrid(N, L); self.V = L**3; self.dk = 2*np.pi/L
        self.shell = np.rint(self.k/self.dk).astype(np.int32); self.nsh = int(self.shell.max())+1
        self.cnt = np.bincount(self.shell.ravel(), minlength=self.nsh).astype(float)
        self.kmean = np.bincount(self.shell.ravel(), weights=self.k.ravel(), minlength=self.nsh)/np.maximum(self.cnt, 1)
        self.thr = [1, 2, 3, 5, 10, 20, 50, 100]; self.workers = 1

    def __call__(self, st, tau, H):
        phi, pphi, x, px = st; c = self.meta['c']; dx = self.dx; V = self.V
        a, add = background(tau, self.spec['xi']); mp2 = (m/H)**2*a*a-add; mx2 = (M/H)**2*a*a-add; ga = g/H*a
        r2 = np.abs(phi)**2; xm2 = np.abs(x)**2
        grad = lambda f: sum(np.mean(np.abs(np.roll(f, -1, axis=ax)-f)**2) for ax in range(3))/dx**2
        kin_p = np.mean(np.abs(pphi)**2); gr_p = grad(phi); quart = lam*np.mean(r2*r2-4*c*r2)
        kin_x = np.mean(np.abs(px)**2); gr_x = grad(x)
        cub = ga*np.mean(2*np.real(np.conj(x)*phi*phi))
        E = kin_p+gr_p+mp2*np.mean(r2)+quart+kin_x+gr_x+mx2*np.mean(xm2)+cub
        dEdtau = np.mean(2*(m/H)**2*a*r2+2*(M/H)**2*a*xm2)+g/H*np.mean(2*np.real(np.conj(x)*phi*phi))
        Q = np.mean(np.imag(np.conj(phi)*pphi)+2*np.imag(np.conj(x)*px))
        pbar = phi.mean(); xbar = x.mean(); pibar = pphi.mean()
        mH2 = 4*lam*(np.mean(r2)-c)
        f0 = abs(pbar)**2/max(np.mean(r2)-c, 1e-300); f0x = abs(xbar)**2/max(np.mean(xm2)-c, 1e-300)
        E0 = abs(pibar)**2+lam*(abs(pbar)**4-4*c*abs(pbar)**2)+mp2*abs(pbar)**2
        d = phi-pbar; re, im = d.real, d.imag
        def cums(y):
            k2 = np.mean(y*y); return [float(k2), float(np.mean(y**3)), float(np.mean(y**4)-3*k2*k2)]
        g4 = np.mean(np.abs(d)**4)/(2*np.mean(np.abs(d)**2)**2)-1
        # spectra
        dx3 = dx**3
        W = self.workers
        Fp = np.abs(sfft.fftn(phi, workers=W)*dx3)**2; Pp = np.abs(sfft.fftn(pphi, workers=W)*dx3)**2
        w2 = self.k**2+max(mH2, 0.)+mp2; w = np.sqrt(np.maximum(w2, 1e-30))
        n = ((Pp+w2*Fp)/(V*w)-1)/2; n[0, 0, 0] = 0
        Fx = np.abs(sfft.fftn(x, workers=W)*dx3)**2; Px = np.abs(sfft.fftn(px, workers=W)*dx3)**2
        wx = np.sqrt(np.maximum(self.k**2+mx2, 1e-30)); nx = ((Px+wx**2*Fx)/(V*wx)-1)/2; nx[0, 0, 0] = 0
        sh = self.shell.ravel()
        nbar = np.bincount(sh, weights=n.ravel(), minlength=self.nsh)/np.maximum(self.cnt, 1)
        nxbar = np.bincount(sh, weights=nx.ravel(), minlength=self.nsh)/np.maximum(self.cnt, 1)
        esh = np.bincount(sh, weights=(2*w*n).ravel(), minlength=self.nsh)/V
        epos = np.maximum(esh[1:], 0); tot = epos.sum()
        flow = [float(epos[nbar[1:] < t].sum()/tot) if tot > 0 else 0. for t in self.thr]
        Ephi_phys = kin_p+gr_p+quart+mp2*np.mean(r2)-(self.meta['Evac']/2-lam*c*c)
        return dict(tau=tau, a=a, E=float(E), dEdtau=float(dEdtau), Q=float(Q), phibar=[pbar.real, pbar.imag],
                    xbar=[xbar.real, xbar.imag], r2=float(np.mean(r2)), x2=float(np.mean(xm2)), mH2=float(mH2),
                    f0_phi=float(f0), f0_x=float(f0x), E0_phi=float(E0), Ephi_phys=float(Ephi_phys),
                    E_phys=float(E-self.meta['Evac']), cum_re=cums(re), cum_im=cums(im), g4=float(g4),
                    kin_phi=float(kin_p), grad_phi=float(gr_p), quart=float(quart), cubic=float(cub),
                    nbar=nbar.tolist(), nxbar=nxbar.tolist(), eshell=esh.tolist(), frac_low=flow)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--job', required=True); ap.add_argument('--N', type=int, default=32)
    ap.add_argument('--L', type=float, default=2*np.pi/.08); ap.add_argument('--variant', default='TW_full')
    ap.add_argument('--patch', default='p50'); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--tau-end', type=float, default=2000.); ap.add_argument('--dt-div', type=float, default=20.)
    ap.add_argument('--out-every', type=float, default=10.); ap.add_argument('--threads', type=int,
                    default=int(os.environ.get('HEAVYQ_THREADS', '1')))
    ap.add_argument('--H', type=float, default=H_PRIMARY); ap.add_argument('--ckpt-every', type=int, default=20)
    ap.add_argument('--resume', action='store_true'); ap.add_argument('--stop-after-steps', type=int, default=0)
    ap.add_argument('--outdir', default='lattice')
    A = ap.parse_args()
    signal.signal(signal.SIGTERM, lambda s, f: STOP.append(s)); signal.signal(signal.SIGINT, lambda s, f: STOP.append(s))
    od = HERE/A.outdir; od.mkdir(exist_ok=True)
    res_path = od/f'{A.job}.json'; ck_path = od/f'{A.job}.ckpt.npz'
    if A.resume and res_path.exists():
        print('result complete', res_path); sys.exit(0)
    spec = dict(N=A.N, L=A.L, variant=A.variant, patch=A.patch, seed=A.seed, tau_end=A.tau_end, dt_div=A.dt_div,
                out_every=A.out_every, H=A.H, xi=1/6 if A.variant == 'XI16' else 0.)
    lib = kernel(); t_start = time.time()
    dx = A.L/A.N; dt = dx/A.dt_div; every = max(1, round(A.out_every/dt)); nsteps_total = int(round(A.tau_end/dt))
    nsteps_total = (nsteps_total//every)*every
    if A.resume and ck_path.exists():
        z = np.load(ck_path, allow_pickle=False)
        st = [np.ascontiguousarray(z[k]) for k in ('phi', 'pphi', 'x', 'px')]
        step = int(z['step']); meta = json.loads(str(z['meta'])); rows = json.loads(str(z['rows']))
        assert json.loads(str(z['spec'])) == spec, 'checkpoint spec mismatch'
        print('resumed at step', step, flush=True)
    else:
        st, meta = build_ic(spec); step = 0; rows = []
    meta.update(dt=dt, steps_per_output=every, nsteps_total=nsteps_total)
    diag = Diag(spec, meta); diag.workers = max(1, A.threads); H = A.H; c = meta['c']
    phi, pphi, x, px = st; fphi = np.empty_like(phi); fx = np.empty_like(x)

    def params(s):
        a, add = background(s*dt, spec['xi']); return (m/H)**2*a*a-add, (M/H)**2*a*a-add, g/H*a
    p0 = params(step); lib.x1_force(A.N, dx, phi, x, fphi, fx, p0[0], p0[1], p0[2], lam, c, A.threads)
    if step == 0: rows.append(diag((phi, pphi, x, px), 0., H))

    def checkpoint():
        atomic_savez(ck_path, phi=phi, pphi=pphi, x=x, px=px, step=np.array(step), meta=np.array(json.dumps(meta)),
                     rows=np.array(json.dumps(rows)), spec=np.array(json.dumps(spec)))

    nout = 0; steps_this_run = 0
    while step < nsteps_total:
        if STOP or (A.stop_after_steps and steps_this_run >= A.stop_after_steps):
            checkpoint(); print('yield at step', step, flush=True); sys.exit(YIELD_EXIT)
        nxt = min((step//every+1)*every, step+200 if A.N >= 128 else (step//every+1)*every)
        if A.stop_after_steps: nxt = min(nxt, step+(A.stop_after_steps-steps_this_run))
        k = nxt-step
        pr = np.array([params(s+1) for s in range(step, nxt)]).T
        lib.x1_steps(A.N, dx, dt, k, phi, pphi, x, px, fphi, fx, np.ascontiguousarray(pr[0]), np.ascontiguousarray(pr[1]),
                     np.ascontiguousarray(pr[2]), lam, c, A.threads)
        step = nxt; steps_this_run += k
        if step % every == 0:
            rows.append(diag((phi, pphi, x, px), step*dt, H)); nout += 1
            if nout % A.ckpt_every == 0: checkpoint()
            r = rows[-1]
            if nout % 10 == 0:
                print(f"tau {r['tau']:.1f} f0 {r['f0_phi']:.4f} mH2 {r['mH2']:.4g} E {r['E']:.8g} Q {r['Q']:.3e} "
                      f"wall {time.time()-t_start:.0f}s", flush=True)
    # final checks
    E = np.array([r['E'] for r in rows]); taus = np.array([r['tau'] for r in rows]); dE = np.array([r['dEdtau'] for r in rows])
    W = np.concatenate([[0], np.cumsum(np.diff(taus)*(dE[1:]+dE[:-1])/2)])
    Ephys0 = rows[0]['E_phys']
    out = dict(spec=spec, meta=meta, rows=rows, kmean=diag.kmean.tolist(), shell_counts=diag.cnt.tolist(),
               energy_residual=float(np.max(np.abs(E-E[0]-W))/abs(Ephys0)),
               charge_drift=float(np.max(np.abs(np.array([r['Q'] for r in rows])-rows[0]['Q']))),
               charge_scale=float(np.mean(np.abs(phi)*np.abs(pphi))+2*np.mean(np.abs(x)*np.abs(px))),
               wall_s=time.time()-t_start, final_state_sha256=__import__('hashlib').sha256(
                   b''.join(a.tobytes() for a in (phi, pphi, x, px))).hexdigest())
    atomic_write_bytes(res_path, json.dumps(out).encode())
    if ck_path.exists(): ck_path.unlink()
    print('done', res_path, 'energy_residual', out['energy_residual'], 'charge_drift', out['charge_drift'], flush=True)
    sys.exit(0)


if __name__ == '__main__':
    main()
