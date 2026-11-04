"""A31 post-result diagnostic 2 (not a gate): full grade of the off-grid Qm minimax point.
Rival language, adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipe33.py')).read(); exec(src[:src.index('# ---------- (a) ----------')])
x0, x1 = 2.182, -7.605
CLIP[0] = CLIP[1] = 0
r = scan('Qm', np.array([x0]), np.array([x1]))[0]
for ft in ('S8', 'P'):
    d = r['d'][ft]; print(f'{ft}: kappa_eff {d["ke"]:.3f}; G3 ' + ' '.join(f'{d["gz"][z]:.3f}' for z in ZB) + '; GT ' + ' '.join(f'{d["gt"][z]:+.3f}' for z in ZB) + f'; G4 {d["sp"]:.3f}/{d["sp2"]:.3f}; flags ' + ''.join('P' if d['k'][g] else 'F' for g in ('G1', 'G2', 'G3', 'G4', 'GT')))
print(f'G2 slope (P) {r["sl"]:+.3f}; mapping clips: c outside [1.5,60] {CLIP[0]}, z_f at grid top {CLIP[1]}')
R = integ('Qm', [x0], [x1]); m = mfun(R, 0, 'S8'); L = LCF['S8']
for z in (.5, 1., 2.33, 10., 100.): print(f' z {z}: H/H_LCDM {np.sqrt(m["E2"](z) / L["E2"](z)):.3f}; rho_v/rho_v0 {m["rv"](z) / m["rv"](0.):.3f}; Omega_v {m["rv"](z) / m["E2"](z):.3f}; xi {x0 + x1 * (1 - 1 / (1 + z)):+.2f}; D/D_LCDM (S8) {m["D"](z) / L["D"](z):.3f}')
gi = r['d']['S8']['gi']; cm = []
for Mv in (1e10, 1e11, 1e12, 1e13):
    CLIP[0] = 0; g = g_iv(np.array([Mv]), 0., m, L)[0]; cm.append(g); print(f' log M200 {np.log10(Mv):.0f}: g {g / A0:.3f} a0 (LCDM {g_iv(np.array([Mv]), 0., L, L)[0] / A0:.3f}), clipped {CLIP[0]}')
grade('DIAG law swap a = g_i at off-grid Qm point', [law(g.gb, a) for g, a in zip(GS, gi)])
print('Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.')
