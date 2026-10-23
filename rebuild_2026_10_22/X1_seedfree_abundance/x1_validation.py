"""X1 validation: truncated Wigner (TW) vs Codex's exact reduced Hamiltonians (FROZEN_CRITERIA §2 + AMENDMENT A1).

  v0                      builder identity vs Codex's Model (p = 1e3, cut 12, number 8, charge 2, V = 100)
  v1a / v1b <n>           one-cell wavefunction (Codex's CellWavefunction) vs TW (signed weights / coherent Phi)
  v2                      12-oscillator absorption benchmark vs TW12 (signed product weights)
  v3 <A|B> <nu> <n> <rwa|full> [--free] [--mutate]
Each call writes validation/<name>.json. Units m_Phi = 1. Run with OMP_NUM_THREADS=1 nice -n 15.
"""
import json, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; OUT = HERE/'validation'; OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE/'provenance'))
from x1_fock import FockK0, observables_exact, MX
import x1_tw_reduced as TW

T_VAL = 500.; NUM = 101; NTRAJ = 20000


def dump(name, obj):
    def conv(o):
        if isinstance(o, np.ndarray): return o.tolist()
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, complex): return [o.real, o.imag]
        raise TypeError(type(o))
    (OUT/f'{name}.json').write_text(json.dumps(obj, default=conv))


def v0():
    from quantum_fock_solver import Model
    cm = Model(energy_cut=12., number_cut=8, charge=2, volume=100., p=1e3)
    k0 = cm.states[:, [1, 4, 7, 10]]; others = np.delete(cm.states, [1, 4, 7, 10], axis=1)
    mine = FockK0(nmax=[8, 8, 8, 8], volume=100., ecut=12., ncut=8, charge=2)
    idx, ok = mine.lookup(k0)
    perm_ok = bool(ok.all() and len(set(idx.tolist())) == mine.dim == len(k0) and not others.any())
    d = {}
    for name, A, B in (('H0', cm.H0, mine.H0), ('H3', cm.H3, mine.H3), ('H4', cm.H4, mine.H4)):
        Bp = B[idx][:, idx].toarray(); d[name] = float(np.max(np.abs(A.toarray()-Bp)))
    res = dict(states=len(k0), permutation_ok=perm_ok, max_abs_diff=d, pass_=perm_ok and max(d.values()) < 1e-12)
    dump('v0', res); print(res)


def union_basis(scenario, nhi):
    """Reachable states of H_RWA from the coherent initial state (N+ = n_a + 2 n_c and N- conserved)."""
    pairs = []
    for nc in range(nhi+1):
        if scenario == 'A':
            for k in range(nhi-nc+1): pairs.append((2*k, nc))           # n_a even, n_a/2 + n_c <= nhi
        else:
            for na in range(nhi-2*nc+1): pairs.append((na, nc))         # n_a + 2 n_c <= nhi
    pairs = np.array(pairs)
    P, Mi = np.meshgrid(np.arange(len(pairs)), np.arange(len(pairs)), indexing='ij')
    a = pairs[P.ravel()]; b = pairs[Mi.ravel()]
    return np.stack([a[:, 0], b[:, 0], a[:, 1], b[:, 1]], axis=1)


def gammas(scenario, n):
    g = np.sqrt(n/2)
    return [0, 0, g, g] if scenario == 'A' else [g, g, 0, 0]


def v3(scenario, nu, n, mode, free=False, mutate=False):
    t0 = time.time(); V = n/nu; driven = 'X' if scenario == 'A' else 'phi'
    g = 0. if free else TW.G; lam = 0. if free else TW.LAM
    gam = gammas(scenario, n); half = n/2; nhi = int(np.ceil(half+6*np.sqrt(half)+4))
    if mode == 'rwa':
        model = FockK0(states=union_basis(scenario, nhi), volume=V, rwa=True, g=g, lam=lam)
    else:
        Wbar = 2*n if scenario == 'A' else n
        model = FockK0(Wmax=int(Wbar+8*np.sqrt(Wbar)+10), volume=V, rwa=False, g=g, lam=lam)
    if model.dim > 3e5 and mode == 'full':
        dump(f'v3_{scenario}_nu{nu:g}_n{n}_{mode}', dict(skipped=True, dim=model.dim)); print('skip', model.dim); return
    psi0, loss = model.coherent(gam)
    ex = observables_exact(model, model.evolve(psi0, T_VAL, NUM), driven); times = ex['t']; t1 = time.time()
    rng = np.random.default_rng(int(1000*nu+n+(0 if scenario == 'A' else 500)))
    a0, w = TW.sample_modes(gam, NTRAJ, rng)
    if mode == 'rwa':
        tt, ah, drift = TW.TW4RWA(volume=V, g=g, lam=lam).run(a0, T_VAL, NUM, .1)
    else:
        tt, ah, drift = TW.TW4Full(volume=V, c=.5, g=g, lam=lam).run(a0, T_VAL, NUM, .02)
    tw = TW.tw_observables(ah, w, driven, mutate=mutate)
    # bootstrap-free sampling error of <N> (driven species) from per-trajectory spread
    nd = (2, 3) if driven == 'X' else (0, 1)
    per = TW.occ(ah[:, :, nd[0]], mutate)+TW.occ(ah[:, :, nd[1]], mutate)
    sem_N = per.std(axis=1)/np.sqrt(NTRAJ)
    res = dict(scenario=scenario, nu=nu, n=n, V=V, mode=mode, free=free, mutate=mutate, dim=model.dim,
               coherent_truncation_loss=loss, times=times,
               exact={k: v for k, v in ex.items()}, tw={k: v for k, v in tw.items()}, tw_sem_Ndriven=sem_N,
               tw_energy_drift=drift, wall_exact=t1-t0, wall_tw=time.time()-t1)
    tag = ('_free' if free else '')+('_MUTATE' if mutate else '')
    dump(f'v3_{scenario}_nu{nu:g}_n{n}_{mode}{tag}', res)
    print(scenario, nu, n, mode, 'dim', model.dim, 'loss', loss, 'wall', round(t1-t0, 1), round(time.time()-t1, 1))


def v1a():
    from quantum_wavefunction import CellWavefunction
    model = CellWavefunction(32, 12.); psi = model.initial_x_excitation()
    times = [0.]; diags = [model.diagnostics(psi)]
    for k in range(4):
        psi = model.evolve(psi, .01, 50); times.append(.5*(k+1)); diags.append(model.diagnostics(psi))
    rng = np.random.default_rng(11); N = 400000; w_ = np.array([1., 1., MX, MX])[:, None]
    q = rng.standard_normal((4, N))/np.sqrt(2*w_); p = rng.standard_normal((4, N))*np.sqrt(w_/2)
    wt = 2*(w_[2]*q[2]**2+p[2]**2/w_[2])-1
    tt, hq, hp = TW.TWCell().run(q, p, 2., 5, .01)
    W = wt/wt.sum(); tw = []
    for k in range(5):
        Q, Pp = hq[k], hp[k]
        occ = [float(np.sum(W*((Pp[i]**2+w_[i, 0]**2*Q[i]**2)/(2*w_[i, 0])))-.5) for i in range(4)]
        f2 = np.sum(W*Q[0]**2); x2 = np.sum(W*Q[2]**2)
        tw.append(dict(bare_occupations=occ, phi_fourth_connected=float(np.sum(W*Q[0]**4)-3*f2**2),
                       phi_X_squared_connected=float(np.sum(W*Q[0]**2*Q[2]**2)-f2*x2)))
    err_occ = max(abs(tw[k]['bare_occupations'][i]-diags[k]['bare_occupations'][i]) for k in range(5) for i in range(4))
    err_k4 = max(abs(tw[k]['phi_fourth_connected']-diags[k]['phi_fourth_connected']) for k in range(5))
    # sampling floor of the signed estimator for occupations
    floor = float(np.std(wt*(Pp[0]**2+Q[0]**2)/2)/np.sqrt(N))
    res = dict(times=times, exact=diags, tw=tw, max_err_occ=err_occ, max_err_phi_fourth=err_k4, sampling_floor_occ=floor,
               ntraj=N)
    dump('v1a', res); print({k: v for k, v in res.items() if k not in ('exact', 'tw')})


def v1b(n):
    from quantum_wavefunction import CellWavefunction
    model = CellWavefunction(32, 12.); f, h, x, y = model.fields; f0 = np.sqrt(2*n)
    psi = np.exp(-.5*((f-f0)**2+h*h+MX*(x*x+y*y)))+0j; psi /= np.linalg.norm(psi)
    times = [0.]; diags = [model.diagnostics(psi)]; t0 = time.time()
    for k in range(50):
        psi = model.evolve(psi, .01, 100); times.append(float(k+1)); diags.append(model.diagnostics(psi))
    t1 = time.time()
    rng = np.random.default_rng(12+n); N = 20000; w_ = np.array([1., 1., MX, MX])[:, None]
    q = rng.standard_normal((4, N))/np.sqrt(2*w_); q[0] += f0; p = rng.standard_normal((4, N))*np.sqrt(w_/2)
    tt, hq, hp = TW.TWCell().run(q, p, 50., 51, .01)
    tw = []
    for k in range(51):
        Q, Pp = hq[k], hp[k]
        occ = [float(np.mean((Pp[i]**2+w_[i, 0]**2*Q[i]**2)/(2*w_[i, 0]))-.5) for i in range(4)]
        f2 = np.mean(Q[0]**2); x2 = np.mean(Q[2]**2)
        tw.append(dict(bare_occupations=occ, phi_fourth_connected=float(np.mean(Q[0]**4)-3*f2**2),
                       phi_X_squared_connected=float(np.mean(Q[0]**2*Q[2]**2)-f2*x2),
                       f_mean=float(np.mean(Q[0])), f_var=float(np.var(Q[0]))))
    ex_occ = np.array([d['bare_occupations'] for d in diags]); tw_occ = np.array([d['bare_occupations'] for d in tw])
    res = dict(n=n, times=times, exact=diags, tw=tw, max_err_occ=float(np.max(np.abs(ex_occ-tw_occ))),
               max_err_occ_rel=float(np.max(np.abs(ex_occ-tw_occ))/n),
               max_boundary=float(max(d['boundary_probability'] for d in diags)),
               energy_drift=float(abs(diags[-1]['energy']/diags[0]['energy']-1)), wall_exact=t1-t0)
    dump(f'v1b_n{n}', res); print({k: v for k, v in res.items() if k not in ('exact', 'tw', 'times')})


def v2():
    from quantum_fock_solver import Model
    from scipy.linalg import eigh
    model = Model(energy_cut=12., number_cut=8, charge=2, volume=100.)
    ini = np.zeros(12, dtype=int); ini[[1, 4, 7]] = 1; i = model.index[tuple(ini)]
    h = model.hamiltonian().toarray(); ev, U = eigh(h)
    times = np.linspace(0, 10000, 201); hist = (np.exp(-1j*times[:, None]*ev)*U[i])@U.T
    p = np.abs(hist)**2; Nex = p@model.states
    fin = np.zeros(12, dtype=int); fin[[0, 2]] = 1; f = model.index[tuple(fin)]; Pabs = p[:, f]
    rng = np.random.default_rng(13); N = 4000
    a0, w = TW.sample_modes(np.zeros(12), N, rng, signed=(1, 4, 7))
    tw12 = TW.TW12(volume=100.)
    tt, ah = tw12.run(a0, 10000., 201, .1)
    W = w/w.sum(); Ntw = np.einsum('tnk,n->tk', np.abs(ah)**2-.5, W)
    per = (np.abs(ah[:, :, 2])**2-.5)*w
    sem = per.std(axis=1)/np.sqrt(N)
    res = dict(times=times, exact_N_phiplus_p=Nex[:, 2], exact_Pabs=Pabs, tw_N_phiplus_p=Ntw[:, 2], tw_sem=sem,
               max_exact_signal=float(Nex[:, 2].max()), max_abs_err=float(np.max(np.abs(Ntw[:, 2]-Nex[:, 2]))),
               median_sem=float(np.median(sem)), ntraj=N,
               trajectories_needed_to_resolve=float((np.median(sem)*np.sqrt(N)/max(Nex[:, 2].max(), 1e-300))**2))
    dump('v2', res); print({k: v for k, v in res.items() if not isinstance(v, np.ndarray)})


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'v0': v0()
    elif cmd == 'v1a': v1a()
    elif cmd == 'v1b': v1b(int(sys.argv[2]))
    elif cmd == 'v2': v2()
    elif cmd == 'v3':
        v3(sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5], free='--free' in sys.argv,
           mutate='--mutate' in sys.argv)
