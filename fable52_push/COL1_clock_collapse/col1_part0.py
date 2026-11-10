#!/usr/bin/env python3
"""COL1 Part 0: static dust of action (A) around a point baryon mass, no time evolution.

    python3 col1_part0.py            -> col1_part0.json / col1_part0.out

Criteria: FROZEN_CRITERIA.md section 3. Units kpc, km/s, Msun. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, sys
import numpy as np

HERE = __file__.rsplit('/', 1)[0] if '/' in __file__ else '.'
G = 4.30091e-6
K = 4 * math.pi * G
KPC_M = 3.0857e19
FOOT = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
KD1 = json.load(open(HERE + '/../../closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json'))
LOGM = [9.4, 10.45, 10.7, 10.9]
RADII = [10.0, 30.0, 100.0, 300.0]
RREF = [1000.0, 300.0, 3000.0]
OUT = []


def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s); OUT.append(s)


def mus_for(f):
    s = KD1['footings'][f]
    return [('0', 0.0), ('0.1 (S4 galaxy bound)', 0.1), ('QX2 cluster', 1.78 if f == 'canonical' else 1.74),
            ('3.71 (brief)', 3.71), ('KD1 mu_B1a (cold at z 3400)', s['B1']['mu_B1a']),
            ('KD1 mu_B1b (BBN)', s['B1']['mu_B1b'])]


def law_g(gN, a0):
    return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * a0))


def grid(rmax):
    return np.logspace(-4, math.log10(rmax), 200001)


def cumtrap(y, x):
    return np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))])


def test_field(Mb, a0, mu, Rref):
    """Law potential of the point mass, zero at Rref; static dust with no back-reaction."""
    r = grid(max(Rref, 300.0) * 1.0001)
    g = law_g(G * Mb / r ** 2, a0)
    # psi(r) = Int_r^Rref g dr' = C - Phi
    Ig = cumtrap(g, r)
    psi = np.interp(Rref, r, Ig) - Ig
    Md = (mu ** 2 / G) * cumtrap(psi * r ** 2, r)
    return r, g, psi, Md


def self_consistent(Mb, a0, mu, Rref, iters=3):
    """Back-reaction: law applied to baryons + dust, three iterations (MK1/QX8 practice); n_d kept signed."""
    r = grid(max(Rref, 300.0) * 1.0001)
    Md = np.zeros_like(r); hist = []
    for _ in range(iters + 1):
        g = law_g(G * (Mb + Md) / r ** 2, a0)
        Ig = cumtrap(g, r)
        psi = np.interp(Rref, r, Ig) - Ig
        Mnew = (mu ** 2 / G) * cumtrap(psi * r ** 2, r)
        hist.append(float(np.interp(100.0, r, Mnew)))
        Md = Mnew
    return r, psi, Md, hist


def main():
    res = {'criteria': 'FROZEN_CRITERIA.md section 3', 'note': 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.',
           'footings': {}}
    P('COL1 Part 0: static dust -mu_K^2 Phi/K around a point baryon mass. kappa = 1/2 FITTED; not theory closed.')
    for f, a0si in FOOT.items():
        a0 = a0si * KPC_M / 1e6
        s = KD1['footings'][f]['setting']
        h = s['h']; od = s['omega_d']; I0 = s['I0_Mpc-2']
        nbar = od * 277.5366  # Msun/kpc^3 (rho_crit = 2.775366e11 h^2 Msun/Mpc^3)
        Rf = res['footings'][f] = {'a0_kms2_per_kpc': a0, 'nbar_today': nbar, 'I0_Mpc-2': I0, 'mu': {}}
        P(f'\n=== footing {f}: a0 {a0:.2f} (km/s)^2/kpc, mean clock charge today {nbar:.3f} Msun/kpc^3, I0 {I0:.4e} Mpc^-2')
        # FRW arithmetic (FB1 / brief check)
        w0_of = lambda mu: I0 / (4 * mu ** 2)
        mu_half_1090 = math.sqrt(I0 * 1091.0 ** 3 / 4)
        mu_fb1 = math.sqrt(I0 / (4 * 1e-9))
        Rf['frw_check'] = {'mu_at_w0_1e-9 (FB1 rule)': mu_fb1, 'w_z1090_at_FB1_rule': 1e-9 / (1e-9 + 1091.0 ** -3),
                           'mu_where_w_z1090_eq_half': mu_half_1090,
                           'mu_for_w_z3400_le_0.01': math.sqrt(I0 * 3401.0 ** 3 * 0.99 / (4 * 0.01))}
        P(f'FRW: FB1 rule w0 < 1e-9 gives mu_K > {mu_fb1:.3f}/Mpc, where w(z 1090) = {Rf["frw_check"]["w_z1090_at_FB1_rule"]:.3f};'
          f' w(z 1090) = 1/2 at mu_K = {mu_half_1090:.3f}/Mpc; w(z 3400) <= 0.01 needs {Rf["frw_check"]["mu_for_w_z3400_le_0.01"]:.2f}/Mpc (KD1 198.25)')
        for name, mu_Mpc in mus_for(f):
            mu = mu_Mpc / 1000.0
            w0 = w0_of(mu_Mpc) if mu_Mpc > 0 else float('inf')
            row = {'mu_per_Mpc': mu_Mpc}
            if mu_Mpc > 0:
                row['w_z1090'] = w0 / (w0 + 1091.0 ** -3); row['w_z3400'] = w0 / (w0 + 3401.0 ** -3)
                row['jeans_length_kpc'] = 2 * math.pi / mu
                row['one_over_mu_kpc'] = 1 / mu
                row['cs_mean_today_kms'] = math.sqrt(K * nbar) / mu
                row['cs_mean_z10_kms'] = math.sqrt(K * nbar * 11 ** 3) / mu
            P(f'\n-- mu_K = {mu_Mpc:.6g}/Mpc [{name}]' + ('' if mu_Mpc == 0 else
              f': w(z1090) {row["w_z1090"]:.3g}, w(z3400) {row["w_z3400"]:.3g}; Jeans length 2pi/mu {row["jeans_length_kpc"]:.4g} kpc;'
              f' c_s at mean today {row["cs_mean_today_kms"]:.4g} km/s, at z 10 {row["cs_mean_z10_kms"]:.4g} km/s'))
            row['masses'] = {}
            for lm in LOGM:
                Mb = 10 ** lm
                Rd = 10 ** (-3.31 + 0.35 * lm)
                mr = row['masses'][str(lm)] = {'R_d_kpc': Rd, 'Rref': {}}
                for Rref in RREF:
                    r, g, psi, Md = test_field(Mb, a0, mu, Rref)
                    Mph = r ** 2 * (g - G * Mb / r ** 2) / G
                    d = {}
                    for R in RADII + [2 * Rd, 3 * Rd, 4 * Rd]:
                        md = float(np.interp(R, r, Md)); mph = float(np.interp(R, r, Mph))
                        d[f'{R:.4g}'] = {'Md_over_Mb': md / Mb, 'Md_over_Mph': md / mph, 'Mph_over_Mb': mph / Mb,
                                         'Md_newton_over_Mb': (mu * R) ** 2 / 2,
                                         'cs_static_kms': math.sqrt(max(float(np.interp(R, r, psi)), 0.0))}
                    mr['Rref'][f'{Rref:.0f}'] = d
                # self-consistent (Rref 1 Mpc) for mu <= 198
                if 0 < mu_Mpc < 1e3:
                    r, psi, Md, hist = self_consistent(Mb, a0, mu, 1000.0)
                    neg = r[(psi < 0) & (r < 1000.0)]
                    conv = abs(hist[-1] - hist[-2]) <= 0.01 * max(abs(hist[-1]), 1e-300)
                    mr['self_consistent_1Mpc'] = {f'{R:.4g}': float(np.interp(R, r, Md)) / Mb for R in RADII}
                    mr['self_consistent_1Mpc']['M_d(<100)_by_iteration_over_Mb'] = [x / Mb for x in hist]
                    mr['self_consistent_1Mpc']['converged_1pct'] = bool(conv)
                    mr['self_consistent_1Mpc']['first_r_nd_negative_kpc'] = float(neg[0]) if len(neg) else None
                t = mr['Rref']['1000']
                P(f'  log M_b {lm}: R_d {Rd:.2f} kpc; test field, zero at 1 Mpc: M_d/M_b at 10/30/100/300 kpc = '
                  + ' / '.join(f'{t[f"{R:.4g}"]["Md_over_Mb"]:.3g}' for R in RADII)
                  + '; M_d/M_ph = ' + ' / '.join(f'{t[f"{R:.4g}"]["Md_over_Mph"]:.3g}' for R in RADII)
                  + '; M_ph/M_b = ' + ' / '.join(f'{t[f"{R:.4g}"]["Mph_over_Mb"]:.3g}' for R in RADII))
                P('     SPARC radii 2/3/4 R_d: M_d/M_ph = ' + ' / '.join(f'{t[f"{k * Rd:.4g}"]["Md_over_Mph"]:.3g}' for k in (2, 3, 4))
                  + '; M_d/M_b = ' + ' / '.join(f'{t[f"{k * Rd:.4g}"]["Md_over_Mb"]:.3g}' for k in (2, 3, 4))
                  + f'; static c_s at 10/100 kpc = {t["10"]["cs_static_kms"]:.1f} / {t["100"]["cs_static_kms"]:.1f} km/s')
                for Rref in (300.0, 3000.0):
                    tt = mr['Rref'][f'{Rref:.0f}']
                    P(f'     zero at {Rref / 1000:g} Mpc: M_d/M_b at 10/30/100/300 = ' + ' / '.join(f'{tt[f"{R:.4g}"]["Md_over_Mb"]:.3g}' for R in RADII))
                if 'self_consistent_1Mpc' in mr:
                    sc = mr['self_consistent_1Mpc']
                    P(f'     self-consistent (law on baryons + dust, 3 iterations, zero at 1 Mpc): M_d/M_b at 10/30/100/300 = '
                      + ' / '.join(f'{sc[f"{R:.4g}"]:.3g}' for R in RADII)
                      + f'; M_d(<100)/M_b by iteration {["%.3g" % x for x in sc["M_d(<100)_by_iteration_over_Mb"]]}; converged {sc["converged_1pct"]};'
                      f' n_d < 0 from r = {sc["first_r_nd_negative_kpc"]}')
            Rf['mu'][name] = row
    json.dump(res, open(HERE + '/col1_part0.json', 'w'), indent=1)
    open(HERE + '/col1_part0.out', 'w').write('\n'.join(OUT) + '\n\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n')


if __name__ == '__main__':
    main()
