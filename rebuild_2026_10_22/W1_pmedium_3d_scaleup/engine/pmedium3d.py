#!/usr/bin/env python3
"""W1 engine: the SE-20261023 discretized expanding action (sol61_push/spatial_expansion_2026_10_23/model.py),
ported for speed and preemption. See ../FROZEN_CRITERIA.md section 2.

Same Model constants, initial state (instantaneous field minimum + tangent), KDK integrator with exact EdS drift
integrals, timestep rule, guards, energy/work bookkeeping and diagnostic rows as SE. Changes: TSC deposit/gather in C
(engine/tsc_kernels.c, same arithmetic and order), one force evaluation per step (SE's second evaluate repeats the same
positions and fields), checkpoint/resume under compute_queue/JOB_CONTRACT.md, a footing switch, and the lane's aperture /
binding-certificate snapshots (read-only diagnostics).

Usage: python3 pmedium3d.py --n 32 --amp 0.03 --footing canonical --threads 1 --outdir ../runs [--resume] [--mutate drop_h_cold]
Exit 0 = complete, 75 = checkpointed after SIGTERM/SIGINT.
"""
import argparse
import ctypes
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

HERE = Path(__file__).resolve().parent
A0_CAN, A0_ALT = 9.3603e-11, 1.1312e-10
R_REF_KPC = .3214846542759978
APERTURES_KPC = (R_REF_KPC, 1.44, 2.88)
CENTRE_KPC = 1.44
STOP = []
YIELD_EXIT = int(os.environ.get("HEAVYQ_YIELD_EXIT", "75"))


# ----------------------------------------------------------------------------------------------- C kernels
def _load_lib():
    src = HERE / "tsc_kernels.c"
    flags = ["-O3", "-mcpu=native", "-ffp-contract=off", "-fno-fast-math", "-fPIC", "-shared"]
    tag = hashlib.sha256(src.read_bytes() + " ".join(flags).encode()).hexdigest()[:16]
    build = HERE / "build"
    build.mkdir(exist_ok=True)
    lib = build / f"tsc_{tag}.so"
    if not lib.exists():
        tmp = build / f".tsc_{tag}.{os.getpid()}.so"
        subprocess.run(["cc", *flags, "-o", str(tmp), str(src), "-lpthread", "-lm"], check=True)
        os.replace(tmp, lib)
    L = ctypes.CDLL(str(lib))
    dp = ctypes.POINTER(ctypes.c_double)
    L.tsc_deposit.argtypes = [ctypes.c_int64, ctypes.c_double, ctypes.c_int64, dp, ctypes.c_double, dp, ctypes.c_int]
    L.tsc_gather.argtypes = [ctypes.c_int64, ctypes.c_double, ctypes.c_int64, dp, dp, dp, ctypes.c_int]
    L.pair_rows.argtypes = [ctypes.c_int64, dp, dp, ctypes.c_double, dp, ctypes.c_int]
    return L, tag


LIB, LIB_TAG = _load_lib()


def _ptr(a):
    return a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))


# ----------------------------------------------------------------------------------------------- model
class Model:
    """Constants and operators verbatim from SE model.py (Model.__init__) and fragment_radiation model.py (grad, div)."""

    def __init__(self, n=8, amp=.001, zi=1100, footing="canonical", threads=1, mutate=None):
        self.n = n; self.eta = .005; self.a = .005; self.b = self.d = .125; self.amp = amp; self.zi = zi
        self.t0 = .012074272908402984; self.ell = .0004404221297174536; self.M0 = 130257985.45037776
        if footing == "alt":
            self.t0 = self.t0 * np.sqrt(A0_CAN / A0_ALT); self.M0 = self.M0 * (A0_ALT / A0_CAN)
        elif footing != "canonical":
            raise ValueError(footing)
        self.footing = footing; self.threads = threads; self.mutate = mutate
        H0 = 67.4 * 1000 / 3.085677581491367e22 * 365.25 * 86400 * 1e9
        self.Hi = H0 * np.sqrt(.315) * (1 + zi) ** 1.5 * self.t0; self.ti = 2 / (3 * self.Hi); self.J0 = 1.5 * self.Hi ** 2; self.fb = 1 / 6.364; self.fc = 1 - self.fb
        rhom = .315 * 3 * (67.4 * 1000 / 3.085677581491367e22) ** 2 / (8 * np.pi * 6.67430e-11) * 3.085677581491367e22 ** 3 / 1.98847e30
        self.RL = (3 * 1.0952264e7 / (4 * np.pi * rhom)) ** (1 / 3); self.Lcom = 2 * np.pi * self.RL; self.box = self.Lcom / (1 + zi) / self.ell; self.dx = self.box / n; self.vol = self.dx ** 3 / (4 * np.pi)
        self.mc = self.fc * self.J0 * self.box ** 3 / (4 * np.pi * n ** 3); self.mb = self.fb * self.J0 * self.box ** 3 / (4 * np.pi * n ** 3)
        k = 4 * np.sin(np.pi * np.fft.fftfreq(n)) ** 2 / self.dx ** 2; self.k2 = k[:, None, None] + k[None, :, None] + k[None, None, :]; self.safe = self.k2.copy(); self.safe[0, 0, 0] = 1
        grid = (np.arange(n) + .5) * self.dx - self.box / 2; Q = np.array(np.meshgrid(grid, grid, grid, indexing='ij')).reshape(3, -1).T; k0 = 2 * np.pi / self.box
        self.disp = -amp / (3 * k0) * np.sin(k0 * Q); self.x0 = Q + self.disp

    # fragment_radiation_2026_10_22/model.py, verbatim
    def grad(self, h): return np.array([(np.roll(h, -1, axis=i) - h) / self.dx for i in range(3)])

    def div(self, P): return sum((P[i] - np.roll(P[i], 1, axis=i)) / self.dx for i in range(3))

    def dep(self, x, m):
        x = np.ascontiguousarray(x, dtype=np.float64)
        rho = np.zeros((self.n,) * 3)
        LIB.tsc_deposit(self.n, self.dx, len(x), _ptr(x), m / self.vol, _ptr(rho), self.threads)
        return rho

    def gather(self, x, F):
        x = np.ascontiguousarray(x, dtype=np.float64); F = np.ascontiguousarray(F, dtype=np.float64)
        out = np.empty_like(x)
        LIB.tsc_gather(self.n, self.dx, len(x), _ptr(x), _ptr(F), _ptr(out), self.threads)
        return out

    # SE model.py fields(), verbatim except deposition and the solver budget for n >= 32 (FROZEN_CRITERIA section 3)
    def fields(self, x, A=1):
        rho = self.dep(x, self.mc); rho = (rho - rho.mean()) / A ** 3
        inv = lambda z: np.fft.ifftn(np.fft.fftn(z) / (self.a + self.d * self.k2 / A ** 2)).real

        def fg(y):
            h = y.reshape(rho.shape); g = self.grad(h) / A; s = np.sqrt(np.sum(g * g, axis=0)); zz = inv(h * h)
            return np.sum(.5 * h * h + s - np.log1p(s) - rho * h + .125 * h * h * zz), (h + .5 * h * zz - self.div(g / (1 + s)) / A - rho).ravel()
        h0 = np.fft.ifftn(np.fft.fftn(rho) / (1 + self.k2 / A ** 2)).real
        if np.linalg.norm(rho) < 1e-12: return np.zeros((3,) + (rho.shape)), np.ones_like(rho), 0.
        maxiter = 1000 if self.n <= 16 else 20000
        op = minimize(fg, h0.ravel(), jac=True, method='L-BFGS-B', options={'ftol': 1e-14, 'gtol': 1e-9, 'maxiter': maxiter}); h = op.x.reshape(rho.shape); g = self.grad(h) / A; s = np.sqrt(np.sum(g * g, axis=0))
        self.last_minimizer = dict(nit=int(op.nit), success=bool(op.success), message=str(op.message))
        return -g / (1 + s), 1 + .5 * inv(h * h), float(np.linalg.norm(fg(op.x)[1]) / np.linalg.norm(rho))

    # SE model.py evaluate(), force part (positions and fields only)
    def forces(self, xc, xb, P, c, A):
        rc = self.dep(xc, self.mc); rb = self.dep(xb, self.mb); rc = (rc - rc.mean()) / A ** 3; rb = (rb - rb.mean()) / A ** 3
        phi = np.fft.ifftn(-A * A * np.fft.fftn(rc + rb) / self.safe).real; phi -= phi.mean(); div = self.div(P) / A; e = rc - div; h = e / c; p = np.sqrt(np.sum(P * P, axis=0))
        if p.max() >= .985 or c.min() <= .1: raise ValueError('field_domain_guard')
        W = -p - np.log1p(-p); gc = self.grad(c) / A
        fcold = phi if self.mutate == "drop_h_cold" else (phi + h)
        forcec = self.gather(xc, fcold); forceb = self.gather(xb, phi)
        forceP = -A ** 3 * (P / (1 - p) + self.grad(h) / A) / self.eta; forcechi = A ** 3 * (.5 * h * h - self.a * (c - 1) + self.d * self.div(gc) / A) / self.b
        return dict(rc=rc, rb=rb, phi=phi, div=div, e=e, h=h, p=p, W=W, gc=gc, fc=forcec, fb=forceb, fP=forceP, fchi=forcechi)

    # SE model.py evaluate(), energy/work/diag part (momenta enter here only)
    def energy(self, F, A, P, c, pc, pb, Q, V):
        rc, rb, phi, div, e, h, p, W, gc = (F[k] for k in ('rc', 'rb', 'phi', 'div', 'e', 'h', 'p', 'W', 'gc'))
        Tm = .5 * (self.mc * np.sum(pc * pc) + self.mb * np.sum(pb * pb)) / A ** 2; Tf = .5 * self.vol * (self.eta * np.sum(Q * Q) + self.b * np.sum(V * V)) / A ** 3
        Ug = .5 * A ** 3 * self.vol * np.sum((rc + rb) * phi); UW = A ** 3 * self.vol * np.sum(W); Uc = .5 * self.a * A ** 3 * self.vol * np.sum((c - 1) ** 2); Ugrad = .5 * self.d * A ** 3 * self.vol * np.sum(gc * gc); Um = .5 * A ** 3 * self.vol * np.sum(e * h)
        energy = Tm + Tf + Ug + UW + Uc + Ugrad + Um
        work = -2 * Tm - 3 * Tf - Ug + 3 * (UW + Uc + Um) + Ugrad + A ** 3 * self.vol * np.sum(h * (-3 * rc + div))
        diag = dict(contrast_c_max=float(rc.max() / (self.fc * self.J0 / A ** 3)), contrast_b_max=float(rb.max() / (self.fb * self.J0 / A ** 3)), rms_c=float(np.sqrt(np.mean(rc ** 2)) / (self.fc * self.J0 / A ** 3)), Pmax=float(p.max()), chi_min=float(c.min()), chi_max=float(c.max()), cell_kpc=self.dx * A * self.ell * 1000, energy=float(energy), energy_scale=float(Tm + Tf + abs(Ug) + UW + Uc + Ugrad + Um))
        return energy, work, diag

    # SE model.py groups(), verbatim
    def groups(self, x, A):
        x = (x + self.box / 2) % self.box; link = .2 * self.dx; pairs = cKDTree(x, boxsize=self.box).query_pairs(link, output_type='ndarray'); ii = pairs[:, 0] if len(pairs) else []; jj = pairs[:, 1] if len(pairs) else []; graph = coo_matrix((np.ones(len(pairs)), (ii, jj)), shape=(len(x), len(x))).tocsr(); num, labels = connected_components(graph, directed=False); counts = np.bincount(labels)
        return dict(max_members=int(max(counts)), groups_ge32=int(sum(counts >= 32)), particle_mass_Msun=self.mc * self.M0, core_radius_cells=.3214846542759978 / (self.dx * A * self.ell * 1000), link_comoving=link)

    # ------------------------------------------------------------------ lane diagnostics (FROZEN_CRITERIA sections 4, 6)
    def minimage(self, d):
        return d - self.box * np.round(d / self.box)

    def certificate(self, F, A, H, xc, xb, P, c, pc, pb, Q, V, hubble=True, apertures_kpc=APERTURES_KPC, centre_kpc=CENTRE_KPC):
        n = self.n; rc = F['rc']
        idx = np.array(np.unravel_index(int(np.argmax(rc)), rc.shape), dtype=float)
        cen = (idx - n / 2) * self.dx
        Rc = centre_kpc / (1000 * self.ell) / A
        it = 0
        for it in range(50):
            d = self.minimage(xc - cen); sel = np.sum(d * d, axis=1) <= Rc * Rc
            if not sel.any(): break
            shift = d[sel].mean(axis=0); cen = self.minimage(cen + shift)
            if np.max(np.abs(shift)) < 1e-10 * self.dx: break
        dc_ = self.minimage(xc - cen); db_ = self.minimage(xb - cen)
        g = (np.arange(n) - n / 2) * self.dx
        cells = np.array(np.meshgrid(g, g, g, indexing='ij')).reshape(3, -1).T
        dcell = self.minimage(cells - cen); rcell2 = np.sum(dcell * dcell, axis=1)
        vol = self.vol
        dens = dict(Tf=(.5 * vol * (self.eta * np.sum(Q * Q, axis=0) + self.b * V * V) / A ** 3).ravel(),
                    UW=(A ** 3 * vol * F['W']).ravel(), Uc=(.5 * self.a * A ** 3 * vol * (c - 1) ** 2).ravel(),
                    Ugrad=(.5 * self.d * A ** 3 * vol * np.sum(F['gc'] * F['gc'], axis=0)).ravel(),
                    Um=(.5 * A ** 3 * vol * F['e'] * F['h']).ravel(),
                    Ug=(.5 * A ** 3 * vol * (F['rc'] + F['rb']) * F['phi']).ravel(),
                    Wx=(A ** 3 * vol * F['h'] * (-3 * F['rc'] + F['div'])).ravel())
        rhoc_bar = self.mc * n ** 3 / self.box ** 3
        out = dict(z=(1 + self.zi) / A - 1, lnA=float(np.log(A)), centre=cen.tolist(), centre_iterations=it + 1, apertures=[])
        for Rk in apertures_kpc:
            R = Rk / (1000 * self.ell) / A
            sc = np.sum(dc_ * dc_, axis=1) <= R * R; sb = np.sum(db_ * db_, axis=1) <= R * R; scell = rcell2 <= R * R
            Nc, Nb = int(sc.sum()), int(sb.sum())
            rec = dict(R_kpc=Rk, R_cells=Rk / (self.dx * A * self.ell * 1000), N_c=Nc, N_b=Nb, N_cells=int(scell.sum()),
                       M_c_Msun=Nc * self.mc * self.M0, M_b_Msun=Nb * self.mb * self.M0,
                       delta_ap_c=Nc * self.mc / (rhoc_bar * 4 / 3 * np.pi * R ** 3) - 1)
            d = np.concatenate([dc_[sc], db_[sb]]); pv = np.concatenate([pc[sc], pb[sb]])
            m = np.concatenate([np.full(Nc, self.mc), np.full(Nb, self.mb)])
            Ef = {k: float(np.sum(v[scell])) for k, v in dens.items()}
            E_field = Ef['Tf'] + Ef['UW'] + Ef['Uc'] + Ef['Ugrad'] + Ef['Um']
            if len(m) >= 2:
                u = (H * A * d if hubble else 0) + pv / A
                ucm = (m[:, None] * u).sum(axis=0) / m.sum()
                K = float(np.sum(.5 * m * np.sum((u - ucm) ** 2, axis=1)))
                U = -self.pair_energy(A * d, m, (A * self.dx) ** 2)
                Kc = float(np.sum(.5 * m[:Nc] * np.sum((u[:Nc] - (m[:Nc, None] * u[:Nc]).sum(axis=0) / max(m[:Nc].sum(), 1e-300)) ** 2, axis=1))) if Nc >= 2 else 0.
                Uc_ = -self.pair_energy(A * d[:Nc], m[:Nc], (A * self.dx) ** 2) if Nc >= 2 else 0.
                Tm = float(np.sum(m * np.sum(pv * pv, axis=1)) / (2 * A ** 2))
            else:
                K = U = Kc = Uc_ = Tm = 0.
            E_H = Tm + Ef['Tf'] + Ef['Ug'] + Ef['UW'] + Ef['Uc'] + Ef['Ugrad'] + Ef['Um']
            W_A = -2 * Tm - 3 * Ef['Tf'] - Ef['Ug'] + 3 * (Ef['UW'] + Ef['Uc'] + Ef['Um']) + Ef['Ugrad'] + Ef['Wx']
            rec.update(K=K, U=U, E_field=E_field, E_iso=K + U + E_field, matter_KU=K + U, virial_2K_over_U=(2 * K / abs(U) if U else None),
                       cold_only_KU=Kc + Uc_, field_parts=Ef, E_H=E_H, W_A=W_A, Tm_peculiar=Tm)
            out['apertures'].append(rec)
        return out

    def pair_energy(self, r, m, eps2):
        r = np.ascontiguousarray(r, dtype=np.float64); m = np.ascontiguousarray(m, dtype=np.float64)
        rows = np.zeros(len(m))
        LIB.pair_rows(len(m), _ptr(r), _ptr(m), eps2, _ptr(rows), self.threads)
        return float(np.sum(rows))


# ----------------------------------------------------------------------------------------------- I/O helpers
def atomic_write_bytes(path, data):
    path = Path(path); tmp = path.with_name(f".{path.name}.tmp{os.getpid()}")
    with open(tmp, 'wb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def atomic_savez(path, **arrays):
    """np.savez-compatible archive with fixed zip timestamps (byte-reproducible), written tmp -> fsync -> os.replace."""
    import zipfile
    from numpy.lib import format as npf
    path = Path(path); tmp = path.with_name(f".{path.name}.tmp{os.getpid()}.npz")
    with open(tmp, 'wb') as f:
        with zipfile.ZipFile(f, 'w', zipfile.ZIP_STORED, allowZip64=True) as zf:
            for k, v in arrays.items():
                with zf.open(zipfile.ZipInfo(k + '.npy', date_time=(1980, 1, 1, 0, 0, 0)), 'w', force_zip64=True) as fid:
                    npf.write_array(fid, np.asanyarray(v), allow_pickle=False)
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def jdump(obj):
    return (json.dumps(obj, indent=1, default=lambda x: x.item() if hasattr(x, 'item') else str(x)) + "\n").encode()


def job_name(n, amp, footing, mutate, cfl=.6, zi=1100):
    seed = {0.001: 'weak', 0.03: 'strong', 0.0: 'null'}.get(amp, f"amp{amp:g}")
    s = f"n{n}_{seed}_{'can' if footing == 'canonical' else 'alt'}"
    if cfl != .6: s += f"_cfl{cfl:g}"
    if zi != 1100: s += f"_zi{zi:g}"
    if mutate: s += f"_MUTATE_{mutate}"
    return s


STATE_ARRAYS = ('xc', 'xb', 'pc', 'pb', 'P', 'c', 'Q', 'V')
STATE_SCALARS = ('t', 'step', 'work', 'E0', 'maxerr', 'maxscale', 'nextN', 'cert_k')


# ----------------------------------------------------------------------------------------------- evolution
def evolve(n=8, amp=.001, zi=1100, zend=10, cfl=.6, footing='canonical', threads=1, mutate=None, outdir=None,
           resume=False, ckpt_seconds=600., stop_after_steps=None, cert=True, log=print):
    """SE evolve(), with checkpoint/resume. Returns the result dict (also written when outdir is given)."""
    m = Model(n, amp, zi, footing, threads, mutate)
    name = job_name(n, amp, footing, mutate, cfl, zi)
    paths = None
    if outdir is not None:
        d = Path(outdir) / name; d.mkdir(parents=True, exist_ok=True)
        paths = dict(result=d / 'result.json', final=d / 'final_state.npz', ckpt=d / 'checkpoint.npz')
        if resume and paths['result'].exists():
            log(f"[{name}] result complete; nothing to do"); return json.loads(paths['result'].read_text())
    end = m.ti * ((1 + zi) / (1 + zend)) ** 1.5
    lnA_end = float(np.log((end / m.ti) ** (2 / 3)))
    cert_targets = [lnA_end - 1 + .1 * k for k in range(10)]
    wall0 = time.time(); run_info = dict(started=time.strftime('%Y-%m-%dT%H:%M:%S'), resumed_from_step=None)
    if paths and resume and paths['ckpt'].exists():
        z = np.load(paths['ckpt'])
        # np.load returns fresh writable arrays in their saved memory order (chi and V are Fortran-ordered, as ifftn makes them);
        # keeping that order keeps every NumPy reduction, hence the trajectory, bit-identical to an uninterrupted run.
        S = {k: z[k] for k in STATE_ARRAYS}
        for k in STATE_SCALARS: S[k] = z[k].item()
        meta = json.loads(str(z['meta']))
        rows, cert_rows, res, init_info = meta['rows'], meta['cert_rows'], meta['initial_residuals'], meta['init_info']
        xc, xb, pc, pb, P, c, Q, V = (S[k] for k in STATE_ARRAYS)
        t, step, work, E0, maxerr, maxscale, nextN, cert_k = (S[k] for k in STATE_SCALARS)
        step = int(step); cert_k = int(cert_k)
        A = (t / m.ti) ** (2 / 3)
        F = m.forces(xc, xb, P, c, A); E, Wk, diag = m.energy(F, A, P, c, pc, pb, Q, V)
        run_info['resumed_from_step'] = step
        log(f"[{name}] resumed at step {step}, z={(1 + zi) / A - 1:.3f}")
    else:
        xc = m.x0.copy(); xb = xc.copy(); pc = m.Hi * m.disp.copy(); pb = pc.copy(); P, c, res = m.fields(xc); mi0 = getattr(m, 'last_minimizer', None)
        eps = 1e-4; Pp, cp, rp = m.fields(xc + eps * m.disp, np.exp(eps)); mi1 = getattr(m, 'last_minimizer', None)
        Pm, cm, rm = m.fields(xc - eps * m.disp, np.exp(-eps)); mi2 = getattr(m, 'last_minimizer', None)
        Q = m.Hi * (Pp - Pm) / (2 * eps); V = m.Hi * (cp - cm) / (2 * eps); res = [res, rp, rm]; init_info = [mi0, mi1, mi2]
        t = m.ti; A = 1.; F = m.forces(xc, xb, P, c, A); E, Wk, diag = m.energy(F, A, P, c, pc, pb, Q, V)
        E0 = E; work = 0.; rows = []; cert_rows = []; step = 0; nextN = 0; maxerr = 0; maxscale = diag['energy_scale']; cert_k = 0
        log(f"[{name}] initial state: residuals {res}, minimizer {init_info}, {time.time() - wall0:.1f}s")
    reason = 'endpoint'; last_ckpt = time.time()

    def save_ckpt():
        meta = json.dumps(dict(rows=rows, cert_rows=cert_rows, initial_residuals=res, init_info=init_info))
        atomic_savez(paths['ckpt'], xc=xc, xb=xb, pc=pc, pb=pb, P=P, c=c, Q=Q, V=V, t=np.float64(t), step=np.int64(step),
                     work=np.float64(work), E0=np.float64(E0), maxerr=np.float64(maxerr), maxscale=np.float64(maxscale),
                     nextN=np.float64(nextN), cert_k=np.int64(cert_k), meta=np.array(meta))

    try:
        while t < end * (1 - 1e-12):
            if paths is not None and (STOP or (stop_after_steps is not None and step >= stop_after_steps)):
                save_ckpt(); log(f"[{name}] checkpoint at step {step}; yielding"); return None
            if paths is not None and time.time() - last_ckpt > ckpt_seconds:
                save_ckpt(); last_ckpt = time.time()
            A = (t / m.ti) ** (2 / 3); H = 2 / (3 * t); fc, fb, fP, fchi = F['fc'], F['fb'], F['fP'], F['fchi']; W = Wk
            maxscale = max(maxscale, diag['energy_scale']); err = abs(E - E0 - work) / max(maxscale, 1e-30); maxerr = max(maxerr, err)
            if np.log(A) >= nextN:
                rows.append(dict(z=(1 + zi) / A - 1, step=step, work_error=err, **diag, **m.groups(xc, A))); nextN += .15
            if cert and cert_k < 10 and np.log(A) >= cert_targets[cert_k]:
                cr = m.certificate(F, A, H, xc, xb, P, c, pc, pb, Q, V); cr.update(step=step, k=cert_k); cert_rows.append(cr); cert_k += 1
            dt = min(cfl * np.sqrt(m.eta) / np.sqrt(1 + 12 / (A * m.dx) ** 2), .015 / H, end - t)
            pc += dt * fc / 2; pb += dt * fb / 2; Q += dt * fP / 2; V += dt * fchi / 2
            tn = t + dt; An = (tn / m.ti) ** (2 / 3); I2 = 3 * m.ti ** (4 / 3) * (t ** (-1 / 3) - tn ** (-1 / 3)); I3 = m.ti ** 2 * (1 / t - 1 / tn)
            xc += pc * I2; xb += pb * I2; xc = (xc + m.box / 2) % m.box - m.box / 2; xb = (xb + m.box / 2) % m.box - m.box / 2; P += Q * I3; c += V * I3
            F = m.forces(xc, xb, P, c, An); pc += dt * F['fc'] / 2; pb += dt * F['fb'] / 2; Q += dt * F['fP'] / 2; V += dt * F['fchi'] / 2
            E, Wk, diag = m.energy(F, An, P, c, pc, pb, Q, V); work += .5 * (W + Wk) * np.log(An / A); t = tn; step += 1
            if step % 500 == 0:
                log(f"[{name}] step {step} z={(1 + zi) / An - 1:.3f} peak={diag['contrast_c_max']:.4f} wall={time.time() - wall0:.0f}s")
    except ValueError as ex:
        reason = str(ex)
    A = (t / m.ti) ** (2 / 3); H = 2 / (3 * t); err = abs(E - E0 - work) / max(maxscale, diag['energy_scale'], 1e-30); maxerr = max(maxerr, err)
    rows.append(dict(z=(1 + zi) / A - 1, step=step, work_error=err, **diag, **m.groups(xc, A)))
    if cert and reason == 'endpoint':
        cr = m.certificate(F, A, H, xc, xb, P, c, pc, pb, Q, V); cr.update(step=step, k=10); cert_rows.append(cr)
    out = dict(parameters=dict(n=n, amp=amp, zi=zi, zend=zend, cfl=cfl, footing=footing, a0=A0_CAN if footing == 'canonical' else A0_ALT,
                               t0_Gyr=m.t0, M0_Msun=m.M0, mutate=mutate, cold_box_mass_Msun=m.mc * n ** 3 * m.M0, Lcom_Mpc=m.Lcom,
                               box_code=m.box, dx_code=m.dx, Hi_code=m.Hi),
               initial_residuals=res, init_info=init_info, reason=reason, steps=step, max_work_error=maxerr, rows=rows, cert_rows=cert_rows)
    out['checks'] = [dict(name='reaches_target', passed=reason == 'endpoint'),
                     dict(name='static_residual', passed=bool(max(res) < 1e-5), value=max(res)),
                     dict(name='work_balance', passed=bool(maxerr < .01), value=maxerr)]
    out['engine'] = dict(file_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), kernel_tag=LIB_TAG,
                         kernel_sha256=hashlib.sha256((HERE / 'tsc_kernels.c').read_bytes()).hexdigest(), threads=threads,
                         numpy=np.__version__, python=sys.version.split()[0])
    final = dict(xc=xc, xb=xb, pc=pc, pb=pb, P=P, c=c, Q=Q, V=V, t=np.float64(t))
    if paths is not None:
        atomic_savez(paths['final'], **final)
        out['final_state_sha256'] = hashlib.sha256(paths['final'].read_bytes()).hexdigest()
        info = dict(run_info, wall_seconds=time.time() - wall0)
        atomic_write_bytes(paths['result'].with_name('run_info.json'), jdump(info))
        atomic_write_bytes(paths['result'], jdump(out))
        if paths['ckpt'].exists(): paths['ckpt'].unlink()
        log(f"[{name}] done: steps {step}, reason {reason}, peak {rows[-1]['contrast_c_max']:.6g}, wall {time.time() - wall0:.0f}s")
    out['_final'] = final
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True); ap.add_argument('--amp', type=float, required=True)
    ap.add_argument('--zi', type=float, default=1100); ap.add_argument('--zend', type=float, default=10); ap.add_argument('--cfl', type=float, default=.6)
    ap.add_argument('--footing', choices=['canonical', 'alt'], default='canonical')
    ap.add_argument('--threads', type=int, default=int(os.environ.get('HEAVYQ_THREADS', '1')))
    ap.add_argument('--mutate', choices=['drop_h_cold'], default=None)
    ap.add_argument('--outdir', default=str(HERE.parent / 'runs')); ap.add_argument('--resume', action='store_true')
    ap.add_argument('--ckpt-seconds', type=float, default=600.); ap.add_argument('--stop-after-steps', type=int, default=None)
    a = ap.parse_args()
    signal.signal(signal.SIGTERM, lambda s, f: STOP.append(s)); signal.signal(signal.SIGINT, lambda s, f: STOP.append(s))
    zi = int(a.zi) if a.zi == int(a.zi) else a.zi
    r = evolve(a.n, a.amp, zi, a.zend, a.cfl, a.footing, a.threads, a.mutate, a.outdir, a.resume, a.ckpt_seconds, a.stop_after_steps,
               log=lambda s: print(s, flush=True))
    sys.exit(0 if r is not None else YIELD_EXIT)


if __name__ == '__main__':
    main()
