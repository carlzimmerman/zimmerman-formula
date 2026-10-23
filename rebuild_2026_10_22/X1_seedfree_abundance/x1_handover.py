"""X1 hand-over E1 -> E2 and the E2 Boltzmann evolution to X onset (FROZEN_CRITERIA §2, AMENDMENT A3).

1. Hand-over criterion on a TW lattice run: energy fraction in shells with n < n* (n* from the V3 validation) and the
   trailing 100-tau mean of the Phi coherent fraction f0.
2. K11 overlap: classical-statistics Boltzmann (no condensate) started from the TW shell spectrum at 0.75 tau_end,
   compared with TW at tau_end (L1 of the shell energy spectrum on k <= 0.7 k_Nyquist).
3. E2 (CONDITIONAL if the criterion is not met): quantum Boltzmann from the TW fluctuation spectrum at tau_end to tau_on,
   and the two stationary endpoints of number- and energy-conserving 2<->2 kinetics (BE with mu, plus a condensate) and of
   full chemical equilibrium (mu = 0 with all Phi energy), giving the Hartree mass at X onset and the tachyonic-window
   ratio r = 2 (g/H) a^2 |X0/H| / m_H^2 (conformal units).
Usage: python3 x1_handover.py <lattice_job> <nstar>
"""
import json, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from x1_boltzmann import Boltz

HERE = Path(__file__).resolve().parent
m = .001; M = 2*m*np.sqrt(1+.02**2); g = 2.168e-6; lam = .00881292


def shell_to_grid(km, nb, cnt, p, kcut):
    ok = (np.array(cnt) > 0) & (km > 0) & (km <= kcut)
    f = np.interp(p, km[ok], np.maximum(nb[ok], 0.), left=max(nb[ok][0], 0.), right=0.)
    f[p > kcut] = 0.
    return f


def main(job, nstar, out=None):
    d = json.loads((HERE/'lattice'/f'{job}.json').read_text()); rows = d['rows']; spec = d['spec']
    km = np.array(d['kmean']); cnt = np.array(d['shell_counts']); kny = np.pi*spec['N']/spec['L']
    taus = np.array([r['tau'] for r in rows]); f0 = np.array([r['f0_phi'] for r in rows])
    thr = [1, 2, 3, 5, 10, 20, 50, 100]; j = thr.index(min(thr, key=lambda t: abs(t-nstar))) if nstar in thr else None
    flow = np.array([np.interp(np.log(nstar), np.log(thr), r['frac_low']) for r in rows])
    win = np.array([f0[(taus > t-100) & (taus <= t)].mean() for t in taus])
    crit = dict()
    for name, frac in (('H1', .5), ('H2', .25)):
        ok = np.nonzero((flow > frac) & (win < .05))[0]
        crit[name] = float(taus[ok[0]]) if len(ok) else None
    # ---- K11 overlap: classical Boltzmann (no condensate) from 0.75 tau_end to tau_end
    kcut = 0.7*kny
    B = Boltz(pmax=kny, Np=64, classical=True); p = B.p
    ia = int(np.argmin(np.abs(taus-0.75*taus[-1]))); ib = len(rows)-1
    fa = shell_to_grid(km, np.array(rows[ia]['nbar']), cnt, p, kny)
    t0 = time.time()
    hist, info = B.evolve(fa, taus[ia], taus[ib], ntimes=6, rtol=1e-4)
    fb_bz = np.array(hist[-1]['f']); fb_tw = shell_to_grid(km, np.array(rows[ib]['nbar']), cnt, p, kny)
    E = np.sqrt(p**2+hist[-1]['mH2']); band = p <= kcut
    eps_bz = p**2*E*fb_bz; eps_tw = p**2*E*fb_tw; eps_a = p**2*E*fa
    L1 = float(np.sum(np.abs(eps_bz-eps_tw)[band])/np.sum(np.abs(eps_tw)[band]))
    L1_static = float(np.sum(np.abs(eps_a-eps_tw)[band])/np.sum(np.abs(eps_tw)[band]))
    overlap = dict(tau_a=float(taus[ia]), tau_b=float(taus[ib]), L1_boltzmann_vs_tw=L1, L1_no_evolution=L1_static,
                   pass_=L1 < .15, wall=time.time()-t0, boltz_info=info,
                   f0_window_at_tau_a=float(win[ia]), f0_window_at_tau_b=float(win[ib]))
    # ---- E2 to X onset (conformal; tau_on = sqrt(H/M) - 1)
    H = spec['H']; tau_on = np.sqrt(H/M)-1.
    BQ = Boltz(pmax=8., Np=96, classical=False)
    f_end = shell_to_grid(km, np.array(rows[ib]['nbar']), cnt, BQ.p, kny)
    t1 = time.time()
    hq, iq = BQ.evolve(f_end, taus[ib], tau_on, ntimes=30, rtol=1e-4)
    x0 = np.hypot(*d['meta']['zero_mode']['x0'])
    def ratio(mH2, a): return 2*(g/H)*a*a*x0/mH2 if mH2 > 0 else np.inf
    a_on = 1+tau_on
    e2 = dict(tau_start=float(taus[ib]), tau_on=float(tau_on), conditional=crit['H1'] is None,
              final=dict(tau=hq[-1]['tau'], n=hq[-1]['n'], rho=hq[-1]['rho'], mH2=hq[-1]['mH2'],
                         r_at_on=ratio(hq[-1]['mH2'], a_on) if hq[-1]['tau'] >= tau_on*(1-1e-9) else None),
              trajectory=[dict(tau=h['tau'], n=h['n'], rho=h['rho'], mH2=h['mH2']) for h in hq], info=iq, wall=time.time()-t1)
    # stationary endpoints with the full Phi energy (fluctuations + zero mode), conformal units
    Ephi = rows[-1]['Ephi_phys']
    # (i) full chemical equilibrium mu = 0, two dof, Hartree: rho = pi^2/15 T^4 (massless limit), mH^2 = lam T^2/3
    T_eq = (15*Ephi/np.pi**2)**.25; mH2_eq = lam*T_eq**2/3
    # (ii) number- and energy-conserving: n_fluct from the Boltzmann start + zero-mode quanta E0/omega0 (omega0 ~ quartic
    #      oscillation frequency of the zero mode, sqrt(lam)*amplitude*0.847 in conformal units)
    n_fl = BQ.moments(f_end, BQ.hartree(f_end))['n']
    amp = np.sqrt(max(rows[-1]['r2']-d['meta']['c'], 0.)*np.mean(win[-20:]))
    E0 = max(Ephi-BQ.moments(f_end, BQ.hartree(f_end))['rho'], 0.)
    om0 = 0.8472*np.sqrt(2*lam)*amp*np.sqrt(2) if amp > 0 else np.nan
    n_tot = n_fl+(E0/om0 if om0 == om0 and om0 > 0 else 0.)
    endpoints = dict(mu0=dict(T=T_eq, mH2=mH2_eq, r_at_on=ratio(mH2_eq, a_on)),
                     number_conserving=dict(n_fluct=n_fl, E0_zero_mode=E0, omega0=om0, n_total=n_tot,
                                            n_over_n_mu0=n_tot/(2*1.2020569/np.pi**2*T_eq**3*2/2)))
    res = dict(job=job, nstar=nstar, criterion=crit, frac_low_end=float(flow[-1]), f0_window_end=float(win[-1]),
               overlap_K11=overlap, E2=e2, endpoints=endpoints, X0_over_H=float(x0), Ephi=Ephi)
    (HERE/'handover').mkdir(exist_ok=True)
    (HERE/'handover'/f'{out or job}_nstar{nstar:g}.json').write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps({k: v for k, v in res.items() if k not in ('E2',)}, indent=1, default=float)[:3000])
    print('E2 final', e2['final'], 'info', iq)


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]))
