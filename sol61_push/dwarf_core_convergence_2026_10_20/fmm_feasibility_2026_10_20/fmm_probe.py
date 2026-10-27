"""Bounded native-ARM FMM feasibility probe; not a production gravity backend.

This evaluates the unsoftened 3D Laplace law, with G in the existing experiment
units. It deliberately does not substitute that law for the existing Plummer
evolution. Requested FMM tolerance is not asserted to certify every force.
"""
import os
for _key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_key] = '1'
import argparse
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'vendor' / 'fmm3dpy_2_1_0'))
sys.path.insert(0, str(HERE.parent))
import fmm3dpy
from fast_gravity import G, gravity as direct_gravity


def fmm(x, m, tol):
    out = fmm3dpy.lfmm3d(eps=tol, sources=np.asfortranarray(x.T),
                         charges=4*np.pi*G*m, pg=2)
    if out.ier:
        raise RuntimeError('FMM ier=%s' % out.ier)
    a, phi = np.asarray(out.grad).T.copy(), -np.asarray(out.pot).copy()
    if not np.isfinite(a).all() or not np.isfinite(phi).all():
        raise FloatingPointError('nonfinite FMM output')
    return a, .5*float(m@phi), phi


def metrics(x, m, a, phi, ar, phir):
    err = np.linalg.norm(a-ar, axis=1)
    ref = np.linalg.norm(ar, axis=1)
    force = m[:, None]*a
    xc = x-np.average(x, axis=0, weights=m)
    torque = np.cross(xc, force)
    return dict(force_l2_relative=float(np.linalg.norm(a-ar)/np.linalg.norm(ar)),
                force_max_vector_relative=float(np.max(err/np.maximum(ref, 1e-300))),
                force_max_absolute=float(err.max()),
                force_median_magnitude=float(np.median(ref)),
                potential_max_relative=float(np.max(np.abs((phi-phir)/phir))),
                energy_relative=float(abs(m@(phi-phir)/(m@phir))),
                momentum_residual_relative=float(np.linalg.norm(force.sum(0))/np.linalg.norm(force, axis=1).sum()),
                torque_residual_relative=float(np.linalg.norm(torque.sum(0))/np.linalg.norm(torque, axis=1).sum()))


def sample_direct(x, m, ids):
    """Independent ordered NumPy sums at the selected existing source indices."""
    a, phi = [], []
    for i in ids:
        dr = x-x[i]
        r2 = np.einsum('ij,ij->i', dr, dr)
        r2[i] = np.inf
        invr = 1/np.sqrt(r2)
        phi.append(-G*np.sum(m*invr))
        a.append(G*np.sum((m*invr**3)[:, None]*dr, axis=0))
    return np.array(a), np.array(phi)


def run(output):
    started = time.perf_counter()
    result = dict(assertion_tested='Native ARM FMM3D 2.1.0 raw-Laplace errors, invariants and finite timings on declared saved/generated coordinates.',
                  non_claims=['No softened production backend implemented.', 'No evolution, profile convergence, universal error bound, or exact P/J conservation established.',
                              'Timings are a serial-wheel lower-scope probe; no million-particle runtime extrapolation is validated.'],
                  software=dict(python=sys.version, numpy=np.__version__, fmm3dpy='2.1.0', machine=platform.machine()),
                  cases=[])
    def save():
        result['elapsed_seconds'] = time.perf_counter()-started
        result['maxrss_bytes_macos'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        Path(output).write_text(json.dumps(result, indent=2)+'\n')
    rng = np.random.default_rng(20261020)
    # Orthogonal hand-computable normalization, gradient sign and self exclusion.
    x, m = np.array([[0.,0.,0.],[2.,0.,0.]]), np.array([3.,7.])
    a, u, phi = fmm(x,m,1e-12)
    assert np.allclose(phi, -G*np.array([7.,3.])/2, rtol=2e-14, atol=0.)
    assert np.allclose(a, G*np.array([[7./4,0.,0.],[-3./4,0.,0.]]), rtol=2e-14, atol=0.)
    assert abs(u+G*21/2) < 2e-14*abs(u)
    result['two_body_analytic'] = 'passed'
    save()
    path = HERE.parent/'run_pilot_gpu8k_iso'/'final.npz'
    z = np.load(path)
    domains = [('gaussian_4096',rng.normal(size=(4096,3))*1000., np.exp(rng.uniform(-1,1,4096))),
               ('saved_iso_9216',z['x'],z['m'])]
    result['snapshot_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    for name,x,m in domains:
        ar,ur,phir=direct_gravity(x,m,0.,threads=1)
        for tol in (1e-12,1e-14):
            t=time.perf_counter(); a,u,phi=fmm(x,m,tol); elapsed=time.perf_counter()-t
            row=dict(name=name,n=len(x),requested_tolerance=tol,seconds=elapsed,
                     **metrics(x,m,a,phi,ar,phir))
            result['cases'].append(row); print(json.dumps(row),flush=True); save()
    # Finite scaling probe, fresh deterministic isotropic coordinates at each N.
    # 32 sampled source targets include no self term and are independently summed.
    for n in (32768,131072,262144):
        x=rng.normal(size=(n,3))*1000.
        m=np.full(n,1.e8/n)
        t=time.perf_counter(); a,u,phi=fmm(x,m,1e-12); elapsed=time.perf_counter()-t
        ids=np.linspace(0,n-1,32,dtype=int)
        ar,phir=sample_direct(x,m,ids)
        error=np.linalg.norm(a[ids]-ar,axis=1)
        relative=error/np.linalg.norm(ar,axis=1)
        force=m[:,None]*a
        xc=x-np.average(x,axis=0,weights=m)
        torque=np.cross(xc,force)
        row=dict(name='gaussian_scaling',n=n,requested_tolerance=1e-12,seconds=elapsed,
                 direct_sample_count=len(ids),force_sample_max_vector_relative=float(relative.max()),
                 force_sample_max_absolute=float(error.max()),
                 potential_sample_max_relative=float(np.max(np.abs((phi[ids]-phir)/phir))),
                 momentum_residual_relative=float(np.linalg.norm(force.sum(0))/np.linalg.norm(force,axis=1).sum()),
                 torque_residual_relative=float(np.linalg.norm(torque.sum(0))/np.linalg.norm(torque,axis=1).sum()))
        result['cases'].append(row); print(json.dumps(row),flush=True); save()
    # Demonstrate cancellation failure independently of FMM truncation: a compact
    # uniform sphere equals Newton outside h, but subtracting a huge point field
    # before adding its tiny regularized field can erase an O(1) background.
    huge,background,tiny=1.e20,1.,1.e-20
    result['subtractive_cancellation_scalar_example']=dict(point_sum=float(huge+background),
        corrected=float((huge+background)-huge+tiny), exact_regularized=float(background+tiny),
        interpretation='Binary64 subtractive near correction has no unconditional relative-error guarantee; native near replacement avoids this example.')
    save()


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    run(parser.parse_args().output)
