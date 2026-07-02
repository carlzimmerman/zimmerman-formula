#!/usr/bin/env python3
"""
ADVERSARIAL VERIFIER (lane B3): independent refit of the extracted MIGHTEE RAR
with a DIFFERENT estimator than the lane's MNR/Gauss-Hermite machinery:
  - x-errors propagated into y via the local model slope (standard ODR-style
    linearization), y-only Gaussian likelihood, sigma_int profiled on a grid.
  - NO Gaussian hyperprior on true x (that's the MNR-specific piece).
Checks (signs and rough magnitudes, not exact equality):
  1. shape: framework nu vs MLS nu, a0 free each -> who wins, by how much
  2. placement of a0 = 9.36e-11 on the framework-nu profile
  3. galaxy-level correlation stress: refit with per-point errors REPLACED by
     an effective inflation sqrt(80/19) (worst-case effective-N deflation) ->
     how much do the sigmas deflate
"""
import numpy as np
from scipy.optimize import minimize_scalar

d = np.loadtxt('mightee_rar_extracted.csv', delimiter=',')
x, y, sx, sy = d[:,0], d[:,1], d[:,2], d[:,3]
n = len(x)

def F_fw(logg, a0):
    g = 10.**logg
    return 0.5*np.log10(g*g + g*a0)

def F_mls(logg, a0):
    g = 10.**logg
    return logg - np.log10(1. - np.exp(-np.sqrt(g/a0)))

def m2l(F, a0, infl=1.0):
    """profile sigma_int; x-err propagated via local slope."""
    eps = 1e-4
    slope = (F(x+eps, a0) - F(x-eps, a0))/(2*eps)
    s2base = (sy**2 + (slope*sx)**2)*infl**2
    r = y - F(x, a0)
    def nll(si):
        st2 = s2base + si*si
        return np.sum(np.log(2*np.pi*st2) + r*r/st2)
    opt = minimize_scalar(nll, bounds=(0., 0.5), method='bounded',
                          options=dict(xatol=1e-6))
    return opt.fun, opt.x

la = np.linspace(-10.6, -9.3, 261)
for infl, tag in ((1.0, 'per-point errors as extracted'),
                  (np.sqrt(80/19.), 'worst-case galaxy-level deflation (errors x sqrt(80/19))')):
    pf = np.array([m2l(F_fw, 10.**l, infl)[0] for l in la])
    pm = np.array([m2l(F_mls, 10.**l, infl)[0] for l in la])
    ifw, iml = np.argmin(pf), np.argmin(pm)
    m936 = m2l(F_fw, 9.36e-11, infl)[0]
    m113 = m2l(F_fw, 1.13e-10, infl)[0]
    m120 = m2l(F_mls, 1.20e-10, infl)[0]
    print('== %s ==' % tag)
    print('  framework a0-free: a0=%.2fe-10, -2lnL=%.2f' % (10.**la[ifw]*1e10, pf[ifw]))
    print('  MLS       a0-free: a0=%.2fe-10, -2lnL=%.2f' % (10.**la[iml]*1e10, pm[iml]))
    print('  SHAPE Delta(-2lnL) fw-MLS = %+.2f  (%s)' %
          (pf[ifw]-pm[iml], 'framework better' if pf[ifw] < pm[iml] else 'MLS better'))
    print('  9.36e-11 on fw profile: dChi2=%.1f -> %.1f sigma' %
          (m936-pf[ifw], np.sqrt(max(m936-pf[ifw], 0))))
    print('  1.13e-10 on fw profile: dChi2=%.1f -> %.1f sigma' %
          (m113-pf[ifw], np.sqrt(max(m113-pf[ifw], 0))))
    print('  1.20e-10 on MLS profile: dChi2=%.1f -> %.1f sigma' %
          (m120-pm[iml], np.sqrt(max(m120-pm[iml], 0))))

# jackknife over galaxies is impossible (colours not exported); instead block
# bootstrap over contiguous x-sorted blocks of ~4 (proxy for per-galaxy groups)
rng = np.random.default_rng(1)
o = np.argsort(x)
blocks = np.array_split(o, 19)
wins = 0; deltas = []
for b in range(200):
    idx = np.concatenate([blocks[i] for i in rng.integers(0, 19, 19)])
    xs, ys, sxs, sys_ = x[idx], y[idx], sx[idx], sy[idx]
    def m2l_b(F, a0):
        eps = 1e-4
        slope = (F(xs+eps, a0)-F(xs-eps, a0))/(2*eps)
        s2b = sys_**2 + (slope*sxs)**2
        r = ys - F(xs, a0)
        def nll(si):
            st2 = s2b + si*si
            return np.sum(np.log(2*np.pi*st2) + r*r/st2)
        return minimize_scalar(nll, bounds=(0., 0.5), method='bounded').fun
    lag = np.linspace(-10.2, -9.4, 41)
    bf = min(m2l_b(F_fw, 10.**l) for l in lag)
    bm = min(m2l_b(F_mls, 10.**l) for l in lag)
    deltas.append(bf-bm); wins += (bf < bm)
deltas = np.array(deltas)
print('== block bootstrap (19 x-blocks, 200 resamples; proxy for galaxy clustering) ==')
print('  framework shape-wins in %d/200 resamples; Delta(-2lnL) median %+.2f, 16-84%% [%+.2f, %+.2f]'
      % (wins, np.median(deltas), *np.percentile(deltas, [16, 84])))
print('EXIT 0')
