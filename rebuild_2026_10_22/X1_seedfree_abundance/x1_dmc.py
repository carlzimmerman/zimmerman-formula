"""X1: bath-assisted absorption X + Phi + Phibar -> Phi + Phi at temperatures T >> m (AMENDMENT A3).

Codex computed the complete tree amplitude and its MB thermal average only for T/m <= 2. Here the same amplitude
  M = sum_{j=2..4} [ 8 g lam / d_j + 8 g^3 / (d_j D_j) ],  all-incoming momenta q0 (X, charge 2), q1 (Phi), q2 (Phibar),
  q3 = -p3, q4 = -p4 (outgoing Phi),  d_j = (q0+q_j)^2 - mP^2,  D_j = (sum_{k in {2,3,4}\\j} q_k)^2 - M^2,
is Monte-Carlo averaged (i) with Codex's convention (three MB incoming momenta, vacuum masses) to validate against the
stored table, and (ii) for the X condensate (X at rest) in the Phi bath with Hartree quasi-particle masses and Bose
factors f1 f2 (1+f3)(1+f4), for T up to 1e7 m. Output: D(T) in the network convention (event rate = D n_X n^2 / 2,
n = both Phi charges), and the per-X absorption rate of the condensate Gamma_rest = D_rest n^2 / 2.
"""
import json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
m = .001; M = 2*m*np.sqrt(1+.02**2); g = 2.168e-6; lam = .00881292


def mdot(a, b): return a[..., 0]*b[..., 0]-np.sum(a[..., 1:]*b[..., 1:], axis=-1)


def amplitude(q, mP):
    tot = 0.
    for j in (2, 3, 4):
        d = mdot(q[0]+q[j], q[0]+q[j])-mP*mP
        oth = [k for k in (2, 3, 4) if k != j]; s2 = q[oth[0]]+q[oth[1]]
        D = mdot(s2, s2)-M*M
        tot = tot+8*g*lam/d+8*g**3/(d*D)
    return tot


def sample_thermal(rng, N, T, ms, stat):
    """Isotropic momenta from the (unnormalised) density p^2 f(E). Proposal: half Gamma(3, T_eff), half log-uniform on
    [1e-3 min(ms,T), 60 T] (covers the Bose-enhanced infrared); returns 4-momenta and weights w = p^2 f / proposal."""
    Teff = max(T, .5*np.sqrt(2*ms*T)); lo, hi = 1e-3*min(max(ms, 1e-30), T), 60*Teff
    half = N//2
    p = rng.permutation(np.concatenate([rng.gamma(3., Teff, half), np.exp(rng.uniform(np.log(lo), np.log(hi), N-half))]))
    prop = .5*p*p*np.exp(-p/Teff)/(2*Teff**3)+.5*np.where((p >= lo) & (p <= hi), 1/(p*np.log(hi/lo)), 0.)
    E = np.sqrt(p*p+ms*ms)
    f = np.exp(-E/T) if stat == 'MB' else 1/np.expm1(E/T)
    c = rng.uniform(-1, 1, N); ph = rng.uniform(0, 2*np.pi, N); s = np.sqrt(1-c*c)
    four = np.stack([E, p*s*np.cos(ph), p*s*np.sin(ph), p*c], axis=1)
    return four, p*p*f/prop, f


def D_of_T(T, mode='rest', stat='BE', mP=None, N=400000, seed=1, thermalX=False):
    """mode='codex': X thermal MB, vacuum masses, MB statistics, no Bose final factors (Codex's convention).
    mode='rest': X at rest (condensate), Hartree mass mP, statistics stat with Bose final factors."""
    rng = np.random.default_rng(seed)
    if mode == 'codex':
        mP = m; stat = 'MB'
    q1, w1, f1 = sample_thermal(rng, N, T, mP, stat); q2, w2, f2 = sample_thermal(rng, N, T, mP, stat)
    if mode == 'codex':
        q0, w0, f0 = sample_thermal(rng, N, T, M, 'MB')
    elif thermalX:
        q0, w0, f0 = sample_thermal(rng, N, T, M, stat)
    else:
        q0 = np.zeros((N, 4)); q0[:, 0] = M; w0 = np.ones(N)
    P = q0+q1+q2; s = mdot(P, P); pst2 = s/4-mP*mP; ok = pst2 > 0; pst = np.sqrt(np.maximum(pst2, 0))
    c = rng.uniform(-1, 1, N); ph = rng.uniform(0, 2*np.pi, N); sn = np.sqrt(1-c*c)
    Ek = np.sqrt(pst2+mP*mP); k = np.stack([pst*sn*np.cos(ph), pst*sn*np.sin(ph), pst*c], axis=1)
    beta = P[:, 1:]/P[:, :1]; b2 = np.sum(beta**2, 1); gam = 1/np.sqrt(np.maximum(1-b2, 1e-300)); bk = np.sum(beta*k, 1)
    p3 = k+((gam-1)*bk/np.maximum(b2, 1e-300)+gam*Ek)[:, None]*beta; E3 = gam*(Ek+bk)
    p4 = P[:, 1:]-p3; E4 = P[:, 0]-E3
    q = [q0, q1, q2, -np.concatenate([E3[:, None], p3], 1), -np.concatenate([E4[:, None], p4], 1)]
    A2 = np.where(ok, amplitude(q, mP)**2, 0.)
    if stat == 'BE' and mode == 'rest':
        bose = (1+1/np.expm1(E3/T))*(1+1/np.expm1(E4/T))
    else:
        bose = 1.
    ph2 = np.where(ok, pst/(4*np.pi*np.sqrt(np.maximum(s, 1e-300))), 0.)
    # Gamma per X (rest) or per-X average (codex): (1/2E0) int dPi1 f1 dPi2 f2 int dPhi2 |M|^2 bose / 2
    E0 = q0[:, 0]; E1 = q1[:, 0]; E2 = q2[:, 0]
    meas = (4*np.pi/(2*np.pi)**3)**2*w1*w2/(2*E1)/(2*E2)        # d^3p/((2pi)^3 2E) with p^2 f folded into w
    integ = meas*ph2*A2*bose/2/(2*E0)
    if mode == 'codex' or thermalX:
        integ = integ*w0                                           # thermal average over X momenta (normalised below)
        nX_w = np.mean(w0)
    Gam = np.mean(integ); err = np.std(integ)/np.sqrt(N)
    nPhi1 = (4*np.pi/(2*np.pi)**3)*np.mean(w1)                     # density of one charge (one dof)
    n = 2*nPhi1
    if mode == 'codex' or thermalX:
        Gam = Gam/nX_w; err = err/nX_w
    return dict(T=T, mP=mP, Gamma=Gam, Gamma_err=err, n=n, D=2*Gam/n**2, D_err=2*err/n**2)


def meff_bath(T):
    m2 = m*m+lam*T*T/3
    for _ in range(60):
        mm = np.sqrt(m2); p = np.linspace(1e-6, 60*T+30*mm, 20000); E = np.sqrt(p*p+mm*mm)
        hf = np.trapz(p*p/np.expm1(E/T)/E, p)/(2*np.pi**2); new = m*m+4*lam*hf
        if abs(new-m2) < 1e-12*new: return np.sqrt(new)
        m2 = new
    return np.sqrt(m2)


if __name__ == '__main__':
    tab = json.loads((HERE/'provenance/bath_assisted_conversion_run_results.json').read_text())
    val = []
    for r in tab['rates'][::2]:
        res = D_of_T(r['T_over_m']*m, mode='codex', N=400000, seed=7)
        val.append(dict(T_over_m=r['T_over_m'], D_codex=r['D_MB_GeV_minus5'], D_mc=res['D'], D_mc_err=res['D_err'],
                        rel=res['D']/r['D_MB_GeV_minus5']-1))
        print('codex', val[-1], flush=True)
    rest = []
    for x in np.geomspace(.03, 1e7, 30):
        T = x*m; mP = meff_bath(T)
        res = D_of_T(T, mode='rest', stat='BE', mP=mP, N=400000, seed=11)
        rth = D_of_T(T, mode='rest', stat='BE', mP=mP, N=400000, seed=12, thermalX=True)
        rest.append(dict(T_over_m=x, mP=mP, D_rest=res['D'], D_rest_err=res['D_err'], n=res['n'], Gamma_rest=res['Gamma'],
                         D_thermalX=rth['D'], D_thermalX_err=rth['D_err']))
        print('rest', {k: (f'{v:.4g}' if isinstance(v, float) else v) for k, v in rest[-1].items()}, flush=True)
    out = dict(validation_vs_codex=val, rest=rest, max_rel_dev_validation=max(abs(v['rel']) for v in val),
               scope='Tree amplitude of Codex (all six diagrams), MC thermal averages. Hartree quasi-particle masses in the '
                     'bath; no thermal widths, no RIS subtraction for the crossed channel (not included).')
    (HERE/'x1_dmc_results.json').write_text(json.dumps(out, indent=1))
