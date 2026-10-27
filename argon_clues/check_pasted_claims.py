"""argon_clues: audit of the pasted cold-energy / black-hole / horizon synthesis.
Each claim is recomputed; PASS/FAIL printed and written to check_pasted_claims.json.
Constants CODATA; H_Lambda from Planck-like H0=67.4, Omega_L=0.685 (only used for numbers, not identities)."""
import json, sys
from pathlib import Path
import sympy as s
import mpmath as mp

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
res = []
def rec(name, ok, detail=''):
    res.append({'claim': name, 'ok': bool(ok), 'detail': str(detail)})
    print(('PASS ' if ok else 'FAIL ') + name + (' | ' + str(detail) if detail else ''))

# ---- symbolic identities
L, G, c, M, H, x = s.symbols('Lambda G c M H x', positive=True)
Z = s.sqrt(32*s.pi/3)
HL = c*s.sqrt(L/3)
a0 = HL*c/Z
rec('a0 = c^2 sqrt(Lambda/32pi)', s.simplify(a0 - c**2*s.sqrt(L/(32*s.pi))) == 0)
rho = L*c**2/(8*s.pi*G)
rec('a0 = (c/2) sqrt(G rho_DE)', s.simplify(a0 - c/2*s.sqrt(G*rho)) == 0)
rs, RdS = 2*G*M/c**2, c/HL
rec('r_MOND^2 = (Z/2) r_s R_dS', s.simplify(G*M/a0 - Z/2*rs*RdS) == 0)
Mcrit = c**4/(4*G*Z*a0)
rec('M_crit = c^2 R_dS/(4G)', s.simplify(Mcrit - c**2*RdS/(4*G)) == 0)
# Nariai: 9 G^2 M^2 Lambda = c^4 -> M_N = c^2/(3 G sqrt(Lambda)) = c^2 R_dS/(3 sqrt3 G)
MN = c**2/(3*G*s.sqrt(L))
rec('Nariai M_N = c^2 R_dS/(3 sqrt3 G)', s.simplify(MN - c**2*RdS/(3*s.sqrt(3)*G)) == 0)
rec('pasted M_crit equals Nariai mass', False,
    'ratio M_crit/M_N = %s ~ %.4f (different mass; the pasted "Nariai" label is wrong)'
    % (s.nsimplify(s.simplify(Mcrit/MN)), float(s.simplify(Mcrit/MN))))
rec('T_dS = hbar a0 Z/(2 pi c k) identity: a0 = sqrt(3pi/8) c kT/hbar',
    s.simplify(2*s.pi/Z - s.sqrt(3*s.pi/8)) == 0)

# ---- mu_fw limits
mu = (s.sqrt(1+4*x**2)-1)/(2*x)
hi = s.series(mu.subs(x, 1/s.Symbol('e', positive=True)), s.Symbol('e', positive=True), 0, 3).removeO()
e = s.Symbol('e', positive=True)
rec('mu_fw(x>>1) = 1 - 1/(2x) + 1/(8x^2)  [pasted: 1 - 1/(8x^2)]',
    s.simplify(hi - (1 - e/2 + e**2/8)) == 0, 'leading correction is 1/(2x), not 1/(8x^2)')
rec('mu_fw(x<<1) -> x', s.limit(mu/x, x, 0) == 1)

# ---- scalings with rho_DE
r = s.Symbol('rho', positive=True)
a0r = c/2*s.sqrt(G*r); TdS = a0r/Z*c*0+a0r  # T_dS ∝ a0
rM = s.sqrt(G*M/a0r)
rec('a0, T_dS ∝ rho^(1/2)', s.simplify(s.diff(s.log(a0r), r)*r - s.Rational(1, 2)) == 0)
rec('r_MOND ∝ rho^(-1/4)  [pasted: rho^(+1/4)]', s.simplify(s.diff(s.log(rM), r)*r + s.Rational(1, 4)) == 0)

# ---- numbers
mp.mp.dps = 30
Gn, cn, hb, kB = mp.mpf('6.67430e-11'), mp.mpf(299792458), mp.mpf('1.054571817e-34'), mp.mpf('1.380649e-23')
Ms, Mpc = mp.mpf('1.98847e30'), mp.mpf('3.0856775814913673e22')
H0 = mp.mpf('67.4')*1000/Mpc; OL = mp.mpf('0.685')
HLn = H0*mp.sqrt(OL); Zn = mp.sqrt(32*mp.pi/3)
a0n = cn*HLn/Zn; Tn = hb*HLn/(2*mp.pi*kB)
rec('numbers', True, 'Z=%.4f  a0=%.3e m/s^2  T_dS=%.2e K (pasted 2.3e-30)  R_dS=%.2f Gpc'
    % (Zn, a0n, Tn, cn/HLn/Mpc/1000))
for lab, m in [('1 Msun', 1), ('4e6 Msun', 4e6), ('6.5e9 Msun (M87)', 6.5e9)]:
    Mk = mp.mpf(m)*Ms; kBH = cn**4/(4*Gn*Mk)
    rec('BH ' + lab, True, 'kappa_BH/a0 = %.2e (x>>1 so mu_fw=1)  r_MOND = %.2e m = %.2f pc  r_MOND/r_s = %.2e'
        % (kBH/a0n, mp.sqrt(Gn*Mk/a0n), mp.sqrt(Gn*Mk/a0n)/3.0857e16, mp.sqrt(Gn*Mk/a0n)/(2*Gn*Mk/cn**2)))
MC = cn**2*(cn/HLn)/(4*Gn)
rec('M_crit numeric', True, '%.2e Msun; Nariai %.2e Msun' % (MC/Ms, cn**2*(cn/HLn)/(3*mp.sqrt(3)*Gn)/Ms))

# ---- a0(z) ; flat Lambda vs CPL dark energy
def rho_ratio(z, w0, wa):
    return (1+z)**(3*(1+w0+wa))*mp.e**(-3*wa*z/(1+z))
rec('a0(z=3)/a0(0), constant Lambda', True, '1.000 exactly (rho_DE constant)')
for w0, wa in [(-0.75, -0.85), (-0.85, -0.5), (-0.95, -0.2)]:
    rec('a0(z=3)/a0(0), CPL w0=%.2f wa=%.2f' % (w0, wa), True, '%.3f' % mp.sqrt(rho_ratio(3, w0, wa)))
rec('0.74 is NOT a framework number: it needs CPL w0~-0.75, wa~-0.85; Lambda gives 1', True,
    'conditional on the dark-energy fit, not a prediction of the MM geometry')

(out/'check_pasted_claims.json').write_text(json.dumps(res, indent=1))
print('\n%d PASS, %d FAIL (FAIL = the pasted statement is wrong)' % (sum(r['ok'] for r in res), sum(not r['ok'] for r in res)))
