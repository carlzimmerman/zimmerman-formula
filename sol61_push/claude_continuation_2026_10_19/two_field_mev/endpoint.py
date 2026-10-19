"""PLAN C5: continuation fits toward Gamma_phys and the endpoint in physical units.

Reads results/tf_limit.json (C2/C4), results/gr/continue*.json (C1), results/partC3/summary_C3.json (C3).
Corrections X(Gamma) - X(0) are fitted locally as A Gamma^p between successive Gamma.
"""
import glob, json, math
import numpy as np
from common import physical_benchmark, dump, HBARC_MEV_CM, HBAR_MEV_S, KG_PER_MEV, M_SUN_KG

tf = json.load(open('results/tf_limit.json'))
gr = []
for fn in sorted(glob.glob('results/gr/continue*.json')):
    gr += [r for r in json.load(open(fn)) if r.get('status') == 0]
gr = sorted({r['G']: r for r in gr}.values(), key=lambda r: -r['G'])
c3 = json.load(open('results/partC3/summary_C3.json'))
pb = physical_benchmark()
Gp = pb['Gamma_phys']
lam = pb['lambda_tot']
m_MeV = pb['m_MeV']


def local_powers(G, X, X0):
    G = np.asarray(G, float)
    dX = np.abs(np.asarray(X, float) - X0)
    out = []
    for i in range(len(G) - 1):
        if dX[i] > 0 and dX[i + 1] > 0:
            p = math.log(dX[i] / dX[i + 1]) / math.log(G[i] / G[i + 1])
            A = dX[i + 1] / G[i + 1] ** p
            out.append(dict(G_pair=[G[i], G[i + 1]], p=p, A=A, correction_at_Gamma_phys=A * Gp ** p))
    return out


fits = {}
TF = tf['GR_TF_limit']
for key, x0 in [('one_minus_omega', TF['one_minus_omega']), ('v_ADM', TF['v_ADM']), ('Q_scaled', TF['Q_scaled']),
                ('z99', TF['z99']), ('C99', TF['C99'])]:
    G = [r['G'] for r in gr]
    X = [r[key] for r in gr]
    fits[key] = dict(TF_limit=x0, values=dict(zip([f'{g:.3e}' for g in G], X)),
                     rel_dev=[x / x0 - 1 for x in X], local_powers=local_powers(G, X, x0))
# edge scaling: z(f^2 = 1e-4 f_c^2) - z_surface(TF)
zs = TF['z_surface']
edge = {}
for lev in ('z_f2_1e_4', 'z_f2_1e_6'):
    G = np.array([r['G'] for r in gr])
    ell = np.array([r[lev] - zs for r in gr])
    good = ell > 0
    pw = [math.log(ell[i] / ell[i + 1]) / math.log(G[i] / G[i + 1]) for i in range(len(G) - 1) if good[i] and good[i + 1]]
    coef = np.polyfit(np.log(G[good]), np.log(ell[good]), 1) if good.sum() >= 2 else [float('nan'), float('nan')]
    edge[lev] = dict(ell=ell.tolist(), local_exponents=pw, global_exponent=float(coef[0]),
                     ell_at_Gamma_phys=float(math.exp(coef[1]) * Gp ** coef[0]))
# edge with a boundary-layer-scaled level: f^2 = c Gamma^(1/3) f_c^2 (c fixed so that level = 1e-4 at
# Gamma = 1e-8). A fixed level is contaminated because the layer's own density scale ~ Gamma^(1/3).
c_lev = 1e-4 / (1e-8) ** (1 / 3)
rows = []
for fn in sorted(glob.glob('results/gr/continue_*_G*.npz')):
    d = np.load(fn)
    G = float(d['G'])
    z, f = d['z'], d['f']
    fc = f[0]
    lev = c_lev * G ** (1 / 3)
    i = np.where(f * f > lev * fc * fc)[0][-1]
    zc = float(np.interp(lev * fc * fc, [f[i + 1] ** 2, f[i] ** 2], [z[i + 1], z[i]]))
    rows.append((G, zc - zs, float(z[1] - z[0])))
rows.sort(key=lambda t: -t[0])
Gs = np.array([t[0] for t in rows])
el = np.array([t[1] for t in rows])
pw = [math.log(el[i] / el[i + 1]) / math.log(Gs[i] / Gs[i + 1]) for i in range(len(Gs) - 1)]
cf = np.polyfit(np.log(Gs), np.log(el), 1)
edge['scaled_level'] = dict(level_coefficient=c_lev, Gamma=Gs.tolist(), ell=el.tolist(), local_exponents=pw,
                            global_exponent=float(cf[0]), ell_at_Gamma_phys=float(math.exp(cf[1]) * Gp ** cf[0]),
                            saved_grid_dz=[t[2] for t in rows])
# stability fits: s^2 natural vs hydro anchor (finest hydro grid)
hyd = {s['l']: s['s2_natural'] for s in tf['hydro'][-1]['sectors']}
stab = {}
for key, vals in c3['s2_by_l'].items():
    l, n = (int(t) for t in key.split('_'))
    anchor = hyd[l][n] if not (l == 1) else hyd[1][n]
    G = [float(g) for g in vals]
    X = [vals[g] for g in vals]
    stab[key] = dict(anchor=anchor, values=vals, rel_dev=[x / anchor - 1 for x in X], local_powers=local_powers(G, X, anchor))
# endpoint in physical units (leading TF order)
L_m = HBARC_MEV_CM / 100 / m_MeV                     # 1/m in metres
sqG = math.sqrt(Gp)
M_MeV = (m_MeV / lam) * TF['v_ADM'] / Gp ** 1.5
qc_nr = tf['NR_TF_limit']['q_center']               # z-independent central charge density (TF)
modes = {}
for l, s2 in hyd.items():
    for n, s in enumerate(s2[:3]):
        if s <= 0:
            continue
        sig_hat = math.sqrt(s * 4 * math.pi * Gp * qc_nr)   # units of m
        om = sig_hat * m_MeV / HBAR_MEV_S                    # rad/s
        modes[f'{l}_{n}'] = dict(s2_natural=s, sigma_rad_s=om, period_s=2 * math.pi / om)
end = dict(Gamma_phys=Gp, benchmark=pb,
           R_surface_m=TF['z_surface'] / sqG * L_m, R99_m=TF['z99'] / sqG * L_m,
           M_ADM_MeV=M_MeV, M_ADM_kg=M_MeV * KG_PER_MEV, M_ADM_Msun=M_MeV * KG_PER_MEV / M_SUN_KG,
           Q_charge_units=TF['Q_scaled'] / Gp ** 1.5 / lam, C99=TF['C99'], one_minus_omega=TF['one_minus_omega'],
           central_Phi_amplitude_MeV=tf['branch']['f_c'] * m_MeV / math.sqrt(lam),
           edge_layer_m={k: v['ell_at_Gamma_phys'] / sqG * L_m for k, v in edge.items()},
           modes=modes)
dump('results/endpoint.json', dict(fits=fits, edge=edge, stability_fits=stab, endpoint=end))
print(json.dumps(end, indent=1, default=float))
print(json.dumps(edge, indent=1))
