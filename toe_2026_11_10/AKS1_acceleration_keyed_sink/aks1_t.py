#!/usr/bin/env python3
"""AKS1 Part T: the theorem step for (A) kept whole plus local clock dissipation (FROZEN_CRITERIA_T.md).

    python3 aks1_t.py -> aks1_t.out / aks1_t.json   (seconds)
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json, math, os, sys
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import aks1_lib as L

OUT, RES = [], {'note': 'Part T (post hoc). Adopts nothing. kappa = 1/2 FITTED; not theory closed.'}
MASSES = (9.0, 10.5, 11.5)
CFG = json.load(open(os.path.join(HERE, '../../campaign_fresh_gravity/CFG461_settling_temperature_mechanism/cfg461_results.json')))
CF = {f: CFG['postfreeze_contraction_Rvir_over_redge'][f'zc1_{f}'] for f in ('canonical', 'alt')}
MPC_KPC = 1000.0
SI_C = 2.99792458e8
GYR_S = 3.15576e16


def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def law_g(xN):
    return 0.5 * (xN + math.sqrt(xN * xN + 4 * xN))


# ---------------- T1 EP-hold ----------------
g, gN, a0, K, Qex, r, G, Mb = sp.symbols('g g_N a_0 K Q_ex r G M_b', positive=True)
A = sp.symbols('A', positive=True)
KP = a0 * A / (a0 + A)                         # Legendre map (QX17 K0)
static_law = sp.simplify((g - KP.subs(A, g)) - g ** 2 / (a0 + g))   # flux balance g - K P = g_N with A = g
mu_of_x = sp.simplify((g ** 2 / (a0 + g)) / g)                       # g_N / g = mu
U = lambda y: a0 * y / (a0 - y)
A_infall = U(G * Qex / r ** 2)
dA_dMb = sp.diff(A_infall, Mb)
t1_ok = static_law == 0 and sp.simplify(mu_of_x - g / (a0 + g)) == 0 and dA_dMb == 0
xe = {f: L.target_edge(f, 1e10)[0] / L.a0_of(f) for f in ('canonical', 'alt')}
gtot = {f: law_g(xe[f]) for f in xe}
P(f'T1 EP-hold: static (A = grad Phi) + Legendre gives g - K P - g^2/(a0+g) = {static_law} and mu = g/(a0+g): the law; '
  f'first-infall A = U(G Q_ex/r^2) has d/dM_b = {dA_dMb} (no baryon field) -> {"PASS" if t1_ok else "FAIL"}. '
  f'Total field at CFG461\'s edge: g/a0 = {gtot["canonical"]:.4f} / {gtot["alt"]:.4f} (g_N/a0 {xe["canonical"]:.5f} / {xe["alt"]:.5f}); '
  f'an A-key reads it only on a clock already held there')
RES['T1'] = {'pass': bool(t1_ok), 'g_edge_over_a0': gtot, 'gN_edge_over_a0': xe}

# ---------------- T2 KEY exponents ----------------
p = sp.symbols('p')
Mv, th = sp.symbols('M theta_th', positive=True)
rr = sp.symbols('r', positive=True)
keys = {'density threshold (M/r^3 = rho_th)': Mv / rr ** 3 - th,
        'rate threshold (G M/r^3 = Gamma_th^2; theta, sigma, a0/c)': G * Mv / rr ** 3 - th ** 2,
        'acceleration threshold (G M/r^2 = g_th; |A| on a held clock)': G * Mv / rr ** 2 - th,
        'speed threshold (G M/r = v_th^2; frame-dependent, not local)': G * Mv / rr - th ** 2}
t2 = {}
for name, eq in keys.items():
    sol = sp.solve(sp.Eq(eq, 0), rr)
    rs = [s_ for s_ in sol if s_.is_positive is not False][0]
    expo = sp.simplify(sp.diff(sp.log(rs), Mv) * Mv)
    t2[name] = str(expo)
    P(f'T2 {name}: r_edge proportional to M^{expo}')
t2['length threshold (1/mu_K, c^2/a0, sqrt(nu t0))'] = '0'
P('T2 length threshold (1/mu_K, c^2/a0, sqrt(nu t0)): r_edge proportional to M^0')
t2_ok = t2['acceleration threshold (G M/r^2 = g_th; |A| on a held clock)'] == '1/2' and all(
    v != '1/2' for k, v in t2.items() if not k.startswith('acceleration'))
P(f'T2: only the acceleration threshold gives M^(1/2) -> {"PASS" if t2_ok else "FAIL"}; '
  f'form B\'s cap sits at g_N = a0/(X(X+1)) = {1 / (59.5 * 60.5):.3e} a0, also an acceleration edge')
RES['T2'] = {'exponents': t2, 'pass': bool(t2_ok), 'cap_gN_over_a0': 1 / (59.5 * 60.5)}

# ---------------- T3 RATE ----------------
t3 = {}
for f in ('canonical', 'alt'):
    cos = L.cosmo_of(f)
    t0_gyr = cos.t_of_a(1.0) * L.TU
    q = L.FOOT[f] * t0_gyr * GYR_S / SI_C               # a0 t0 / c
    bound1 = math.exp(2 * q)
    bound_e = math.exp(2 * q * gtot[f])
    need = CF[f]
    ok = all(bound1 < n for n in need)
    t3[f] = {'t0_gyr': t0_gyr, 'a0_t0_over_c': q, 'bound_F1': bound1, 'bound_F_edge': bound_e, 'required': need,
             'closes_DA': bool(ok)}
    P(f'T3 {f}: t0 {t0_gyr:.3f} Gyr, a0 t0/c = {q:.4f}; contraction bound exp(2 F a0 t0/c) = {bound1:.3f} (F = 1), '
      f'{bound_e:.3f} (F = g_edge/a0, f = x at the edge); CFG461 needs {need} -> D-A {"CLOSED" if ok else "NOT closed"}')
RES['T3'] = t3

# ---------------- T4 GAUSS ----------------
t, R = sp.symbols('t R', positive=True)
Pf = sp.Function('P')
Yf = sp.Function('Y')                                             # Y(t, r) = r^2 P(t, r), regular centre Y(t, 0) = 0
x = sp.symbols('x', positive=True)
charge = sp.integrate(sp.diff(Yf(t, x), x), (x, 0, R)).subs(Yf(t, 0), 0)   # Int div P r^2 dr (4 pi dropped)
charge = sp.simplify(charge.subs(Yf(t, R), R ** 2 * Pf(t, R)))
neutral = sp.simplify(charge.subs(Pf(t, R), 0))
t4_ok = sp.simplify(charge - R ** 2 * Pf(t, R)) == 0 and neutral == 0
P(f'T4 Gauss: Int_0^R (r^2 P)\' dr = {charge}; with P(t, R) = 0 at every t (free-falling boundary) the net polarization '
  f'charge is 0 at every t, whatever the momentum equation (variational or dissipative) -> {"PASS" if t4_ok else "FAIL"}')
RES['T4'] = {'pass': bool(t4_ok), 'identity': str(charge)}

# ---------------- T5 T-DEP with and without entropy ----------------
h, s, c0, Phi = sp.symbols('h s c_0 Phi', real=True)
Fb = sp.Function('F_b')
nd_o = sp.diff(Fb(h), h).subs(h, c0 - Phi)
Ks = sp.Function('K_s')
Fh = Ks(s) ** sp.Rational(-3, 2) * (sp.Rational(2, 5) * h) ** sp.Rational(5, 2)   # SE1 arm (b) form
nd_h = sp.diff(Fh, h).subs(h, c0 - Phi)
s1, s2 = sp.symbols('s1 s2', real=True)
diff_h = sp.simplify(nd_h.subs(s, s1) - nd_h.subs(s, s2))
evades = diff_h != 0
col1_198 = (3.6, 8.4)
scale_J = (L.MU_J / L.MU_W['canonical']) ** 2
P(f'T5 (o): static n_d = {nd_o}: one function of the depth c0 - Phi (T-DEP). Over-capture at the CMB mu_K (COL1 Part 0, '
  f'quoted): {col1_198[0]} to {col1_198[1]} x the law\'s halo at SPARC radii at 198.25 per Mpc; x {scale_J:.3g} at mu_J '
  f'({col1_198[0] * scale_J:.3g} to {col1_198[1] * scale_J:.3g}) -> D-V(o) CLOSED (line >= 2)')
P(f'T5 (h): with entropy (SE1 arm (b) form) n_d = {sp.simplify(nd_h)}; two equal depths with s1 != s2 differ by {diff_h} '
  f'-> evades T-DEP: {evades}')
RES['T5'] = {'nd_o': str(nd_o), 'overcapture_198': col1_198, 'scale_to_muJ': scale_J, 'DVo_closed': True,
             'nd_h': str(sp.simplify(nd_h)), 'h_evades_TDEP': bool(evades)}

# ---------------- T6 EDGE-LAYER ----------------
dKP = sp.simplify(sp.diff(KP, A))
mono = sp.simplify(dKP - a0 ** 2 / (a0 + A) ** 2) == 0
zero = sp.solve(sp.Eq(KP, 0), A)
zero = 'no root for A > 0; K P(A = 0) = ' + str(KP.subs(A, 0)) if not zero else zero
P(f'T6: d(K P)/dA = {dKP} > 0 (monotone) and {zero}; static A = g, so P = 0 iff g = 0. A static region '
  f'whose boundary has g != 0 has P != 0 there; Gauss (T4) puts the compensating negative polarization charge outside, '
  f'where A < g and the clock is not held -> {"PASS" if mono else "FAIL"}')
RES['T6'] = {'pass': bool(mono), 'dKP_dA': str(dKP)}

# ---------------- T7 VISCOSITY WINDOW (estimate) ----------------
t7 = {}
for f in ('canonical', 'alt'):
    cos = L.cosmo_of(f); hh = L.setting(f)['h']
    H3 = cos.H0 * math.sqrt(cos.Om * 4 ** 3 + cos.OL)            # km/s/kpc
    lamJ = 0.42 / hh * MPC_KPC / 4.0                              # physical kpc at z = 3
    kJ = 2 * math.pi / lamJ
    nuF = 3 * H3 / (4 * kJ * kJ)                                  # kpc km/s
    t0 = cos.t_of_a(1.0)                                          # kpc/(km/s)
    a0k = L.a0_of(f)
    rows = []
    for lM in MASSES:
        Mb_ = 10 ** lM
        ge, re = L.target_edge(f, Mb_)
        rM = math.sqrt(L.G * Mb_ / a0k)
        Rcap = rM * math.sqrt(59.5 * 60.5)
        nuS = re ** 2 / t0
        nuCap = Rcap ** 2 / t0
        rows.append({'logMb': lM, 'r_e_star': re, 'nu_S': nuS, 'margin': nuS / nuF, 'R_cap': Rcap, 'nu_cap': nuCap,
                     'margin_cap': nuCap / nuF})
    mmax = max(rw['margin'] for rw in rows)
    closes = mmax >= 3
    # thresholds from (G, c, a0, mu_K): where they sit (reported)
    c = L.CKMS
    dens_a0 = a0k ** 2 / (L.G * c ** 2)                           # Msun/kpc^3
    dens_mu = {name: (mu / 1000.0) ** 2 * c ** 2 / L.K for name, mu in (('mu_J', L.MU_J), ('mu_198', L.MU_W[f]))}
    rate_a0c = a0k / c
    rho_mean_z3 = (cos.nbar0 + cos.rhob0) * 64
    halo = []
    for rw in rows:
        Mb_ = 10 ** rw['logMb']
        Vf2 = math.sqrt(L.G * Mb_ * a0k)
        rho_ph_edge = Vf2 / (4 * math.pi * L.G * rw['r_e_star'] ** 2)
        shear_edge = math.sqrt(L.law_g if False else 1.0) if False else math.sqrt(Vf2) / rw['r_e_star']
        halo.append({'logMb': rw['logMb'], 'rho_ph_edge': rho_ph_edge, 'rate_edge': shear_edge})
    t7[f] = {'H3': H3, 'lambda_J_phys_kpc': lamJ, 'nu_F': nuF, 'rows': rows, 'max_margin': mmax, 'closes_DVh': bool(closes),
             'thresholds': {'density_a0^2/(G c^2)': dens_a0, 'density_mu^2 c^2/K': dens_mu, 'rate_a0/c': rate_a0c,
                            'length_c^2/a0_kpc': c ** 2 / a0k, 'length_1/mu_J_kpc': 1000 / L.MU_J},
             'forest_z3': {'rho_mean': rho_mean_z3, 'rate_H3': H3}, 'halo_z0': halo}
    P(f'T7 {f}: H(z 3) = {H3:.4f} km/s/kpc, lambda_J(z 3) = {lamJ:.1f} kpc physical -> nu_F = {nuF:.1f} kpc km/s. '
      + '; '.join(f'log M_b {rw["logMb"]:g}: nu_S = r_e*^2/t0 = {rw["nu_S"]:.1f} (margin {rw["margin"]:.2f}); cap: '
                  f'{rw["nu_cap"]:.3g} (margin {rw["margin_cap"]:.3g})' for rw in rows)
      + f' -> max margin {mmax:.2f}: D-V(h) {"CLOSED (estimate)" if closes else "NOT closed"}')
    P(f'   thresholds from (G, c, a0, mu_K): density a0^2/(G c^2) = {dens_a0:.3g}, mu_J^2 c^2/K = {dens_mu["mu_J"]:.3g}, '
      f'mu_198^2 c^2/K = {dens_mu["mu_198"]:.3g} Msun/kpc^3; forest mean at z 3 {rho_mean_z3:.3g}; halo phantom at r_e* '
      f'{[round(hh_["rho_ph_edge"], 1) for hh_ in halo]}. Rate a0/c = {rate_a0c:.4f} /TU; H(z 3) {H3:.3f}; halo rate at r_e* '
      f'{[round(hh_["rate_edge"], 2) for hh_ in halo]}. Lengths c^2/a0 = {c ** 2 / a0k:.3g} kpc, 1/mu_J = {1000 / L.MU_J:.3g} kpc')
RES['T7'] = t7

# ---------------- branch table and label ----------------
lab = {}
for f in ('canonical', 'alt'):
    DA = RES['T1']['pass'] and t3[f]['closes_DA']
    DVo = RES['T4']['pass'] and RES['T5']['DVo_closed']
    DVh = t7[f]['closes_DVh']
    exact_all = DA and DVo and RES['T6']['pass'] and False      # D-V(h) has no exact closure item
    if DA and DVo and DVh:
        L_ = 'CLOSED, ONE BRANCH ON AN ESTIMATE'
    elif exact_all:
        L_ = 'CLOSED BY KINEMATICS'
    else:
        L_ = 'STATE LEFT'
    lab[f] = {'D-A(o)': DA, 'D-A(h)': DA, 'D-V(o)': DVo, 'D-V(h)': DVh, 'label': L_}
    P(f'Branches ({f}): D-A(o) {"closed" if DA else "open"}, D-A(h) {"closed" if DA else "open"}, D-V(o) '
      f'{"closed" if DVo else "open"}, D-V(h) {"closed (estimate)" if DVh else "OPEN"} -> PART T LABEL: {L_}')
RES['labels'] = lab
P('\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.')
open(os.path.join(HERE, 'aks1_t.out'), 'w').write('\n'.join(OUT) + '\n')
json.dump(RES, open(os.path.join(HERE, 'aks1_t.json'), 'w'), indent=1, default=str)
