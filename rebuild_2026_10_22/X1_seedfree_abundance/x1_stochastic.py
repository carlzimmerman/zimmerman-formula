"""X1 E0: stochastic light-field inflation for the coarse fields (no seed: all fields start at zero).

R0  re-implements Codex's Langevin algorithm (stochastic_source.py, copied in provenance/) with the same seed, patches
    and steps, and compares with Codex's stored fine-run moments.
BOX the lattice box zero mode: the same drift, horizon-crossing noise for N_e - N_box e-folds and drift only for the last
    N_box = ln(1/k_min) e-folds (the in-box modes are represented explicitly on the lattice), seed 2026102301, dN = .01.
    Conformal velocities are the slow-roll attractor of the same drift. Units: fields in H_inf, a_e = 1.
Usage: python3 x1_stochastic.py [--kmin 0.08] [--Ne 60]
"""
import json, sys, hashlib
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
m = .001; M = 2*m*np.sqrt(1+.02**2); g = 2.168e-6; lam = .00881292
H_PRIMARY = 1.3445177278709404e10


def drift(z, H):
    f1, f2, x1, x2 = z.T; r2 = f1*f1+f2*f2; c = np.sqrt(2)*g/H
    return -np.array([(m/H)**2*f1+c*(x1*f1+x2*f2)+lam*r2*f1,
                      (m/H)**2*f2+c*(-x1*f2+x2*f1)+lam*r2*f2,
                      (M/H)**2*x1+(g/H)/np.sqrt(2)*(f1*f1-f2*f2),
                      (M/H)**2*x2+c*f1*f2]).T/3


def r0_reproduction(H=H_PRIMARY):
    """Identical algorithm and RNG call order to Codex's stochastic_source.py."""
    patches = 4096; dt = .02; duration = 60.; rng = np.random.default_rng(20261022)
    coarse = np.zeros((patches, 4)); fine = coarse.copy()
    for j in range(round(duration/dt)):
        n1 = rng.standard_normal(fine.shape)*np.sqrt(dt/2)/(2*np.pi)
        n2 = rng.standard_normal(fine.shape)*np.sqrt(dt/2)/(2*np.pi)
        coarse += dt*drift(coarse, H)+n1+n2
        fine += dt/2*drift(fine, H)+n1
        fine += dt/2*drift(fine, H)+n2
    def mom(z):
        return dict(phi_variance=float(np.mean(np.sum(z[:, :2]**2, axis=1)/2)),
                    X_variance=float(np.mean(np.sum(z[:, 2:]**2, axis=1)/2)))
    return mom(coarse), mom(fine), fine


def box_ensemble(H=H_PRIMARY, kmin=0.08, Ne=60., dN=.01, patches=4096, seed=2026102301):
    Nbox = np.log(1/kmin); n_noise = round((Ne-Nbox)/dN); n_total = round(Ne/dN)
    rng = np.random.default_rng(seed); z = np.zeros((patches, 4))
    for j in range(n_total):
        z += dN*drift(z, H)
        if j < n_noise:
            z += rng.standard_normal(z.shape)*np.sqrt(dN)/(2*np.pi)
    dzdN = drift(z, H)                   # slow-roll attractor dz/dN
    return z, dzdN, dict(N_box=Nbox, N_noise=n_noise*dN, N_drift=(n_total-n_noise)*dN)


def select_patches(z):
    phi2 = np.sum(z[:, :2]**2, axis=1)/2; x2 = np.sum(z[:, 2:]**2, axis=1)/2
    mp, mx = np.median(phi2), np.median(x2)
    med = int(np.argmin(np.log(phi2/mp)**2+np.log(x2/mx)**2))
    out = {'p50': med}
    for name, q in (('p10', 10), ('p90', 90)):
        tp = np.percentile(phi2, q)
        out[name] = int(np.argmin(np.log(phi2/tp)**2+np.log(x2/mx)**2))
    return out, dict(phi2_median=float(mp), X2_median=float(mx),
                     phi2_p10=float(np.percentile(phi2, 10)), phi2_p90=float(np.percentile(phi2, 90)),
                     X2_p10=float(np.percentile(x2, 10)), X2_p90=float(np.percentile(x2, 90)))


def conformal_zero_mode(zrow, dzrow):
    """Rotate global U(1) so Phi0 is real; return (phi0, pi0, x0, px0) conformal at a=1, a'=1 (H units)."""
    phi = (zrow[0]+1j*zrow[1])/np.sqrt(2); x = (zrow[2]+1j*zrow[3])/np.sqrt(2)
    dphi = (dzrow[0]+1j*dzrow[1])/np.sqrt(2); dx = (dzrow[2]+1j*dzrow[3])/np.sqrt(2)
    th = np.angle(phi); r1 = np.exp(-1j*th); r2 = np.exp(-2j*th)
    phi, dphi, x, dx = phi*r1, dphi*r1, x*r2, dx*r2
    # chi = a Phi/H ; chi' = a' Phi/H + a dPhi/dtau, dPhi/dtau = dPhi/dN at a = 1 (tau = H eta)
    return complex(phi), complex(phi+dphi), complex(x), complex(x+dx)


if __name__ == '__main__':
    kmin = float(sys.argv[sys.argv.index('--kmin')+1]) if '--kmin' in sys.argv else 0.08
    Ne = float(sys.argv[sys.argv.index('--Ne')+1]) if '--Ne' in sys.argv else 60.
    stored = json.loads((HERE/'provenance/stochastic_source_run_results.json').read_text())
    c, f, fine = r0_reproduction()
    samples_match = bool(np.array_equal(np.array(stored['final_field_samples_over_H']), fine))
    r0 = dict(coarse=c, fine=f, stored_fine={k: stored['fine'][k] for k in ('phi_variance', 'X_variance')},
              d_phi=abs(f['phi_variance']-stored['fine']['phi_variance']),
              d_X=abs(f['X_variance']-stored['fine']['X_variance']), samples_bitwise_identical=samples_match)
    z, dz, meta = box_ensemble(kmin=kmin, Ne=Ne)
    sel, quant = select_patches(z)
    zm = {k: conformal_zero_mode(z[i], dz[i]) for k, i in sel.items()}
    np.savez(HERE/f'x1_box_ensemble_kmin{kmin:g}_Ne{Ne:g}.npz', z=z, dzdN=dz)
    out = dict(R0=r0, box=dict(kmin=kmin, Ne=Ne, **meta, selected=sel, quantiles=quant,
               zero_modes={k: dict(phi0=[v[0].real, v[0].imag], pi0=[v[1].real, v[1].imag],
                                   x0=[v[2].real, v[2].imag], px0=[v[3].real, v[3].imag],
                                   z=z[sel[k]].tolist()) for k, v in zm.items()},
               ensemble_phi2=float(np.mean(np.sum(z[:, :2]**2, axis=1)/2)),
               ensemble_X2=float(np.mean(np.sum(z[:, 2:]**2, axis=1)/2))))
    p = HERE/f'x1_stochastic_kmin{kmin:g}_Ne{Ne:g}.json'
    p.write_text(json.dumps(out, indent=1))
    print(json.dumps(out['R0'], indent=1)); print(json.dumps({k: v for k, v in out['box'].items() if k != 'zero_modes'}, indent=1))
    for k, v in out['box']['zero_modes'].items(): print(k, v)
