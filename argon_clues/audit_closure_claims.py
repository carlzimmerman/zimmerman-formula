"""argon_clues: audit of the pasted 'complete closure' (kappa=1/2 'three proofs', 32pi^2 -> 32pi/3)."""
import sympy as s
R, L, c, G = s.symbols('R Lambda c G', positive=True)
def chk(n, ok, note=''): print(('PASS ' if ok else 'FAIL ') + n + (' | ' + note if note else ''))
Z2 = 32*s.pi/3
chk('Vol(S4)=8pi^2R^4/3 from chi=2 and G4=24/R^4', s.simplify(2*32*s.pi**2/(24/R**4) - 8*s.pi**2*R**4/3) == 0)
chk('4 Vol/R^4 = 32pi^2/3', s.simplify(4*8*s.pi**2/3 - 32*s.pi**2/3) == 0)
chk('Z^2 = (32pi^2/3)/pi', s.simplify(32*s.pi**2/3/s.pi - Z2) == 0,
    'arithmetic only: the 1/3 (from int r^2 dr = R^3/3, a 3-volume) is mixed into a dimensionless 4-volume ratio, and "/pi from half-period" is chosen to land on Z^2')
# kappa from active density: Raychaudhuri rho+3P/c^2 with P=-rho c^2 -> -2 rho
act = 1 + 3*(-1)
chk('de Sitter active density = -2 rho_DE', act == -2, 'this would give coefficient 2 (or 2^(1/2)), not 1/2; the pasted "8pi*2^2=32pi" inserts the 2^2 by hand')
# what coefficient would each reading give for a0 = k c sqrt(G rho)?
for lab, k in [('kappa=1/2 (fitted)', s.Rational(1, 2)), ('Milgrom cH/2pi, H=H_L', None)]:
    if k is None:
        print('INFO  ' + lab + ': a0 = c H_L/(2pi) = (c^2/2pi) sqrt(Lambda/3) -> kappa = sqrt(8pi/3)/(2pi)... = %s' % s.N(s.sqrt(8*s.pi/3)/(2*s.pi*1), 5)
              + ' vs 0.5: 2pi-footing differs by factor %s' % s.N((s.sqrt(Z2)/(2*s.pi))**-1*1, 5))
    else:
        print('INFO  ' + lab + ': a0 = c H_L/Z, Z=%s' % s.N(s.sqrt(Z2), 6))
# Deser-Levin threshold: T_eff = hbar/(2 pi k c) sqrt(g^2 + (cH)^2): crossover at g = cH_L, i.e. Z=1
chk('Deser-Levin crossover scale is c H_L (Z=1), observed a0 = cH_L/5.789', False,
    'the dS temperature has no 5.789 in it; a gate built from T_eff transitions at g~cH_L, a factor 5.8 above a0. The unexplained Z is exactly what the proof needs and does not supply')
chk('"kappa = 21" in the pasted text', False, 'garbled; the repo value is kappa=1/2 (FITTED), Z=5.7888, never 21')
