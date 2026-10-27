"""argon_clues: what the pasted 'final_mile_proof' asserts actually test. Each assert is rerun with the choice it hard-codes varied."""
import sympy as sp
pi = sp.pi; th, ph = sp.symbols('th ph', positive=True)
Z2 = sp.Rational(32, 3)*pi
print('A1 Z^2 = 4*Vol(S4)/pi       :', sp.simplify(4*sp.Rational(8, 3)*pi**2/pi) == Z2, '| input choices: factor 4, divisor pi')
for lab, div in [('pi', pi), ('2pi', 2*pi), ('pi/2', pi/2)]:
    print('     divisor %-4s -> "Z^2" = %s   (script asserts only the pi case)' % (lab, sp.simplify(4*sp.Rational(8, 3)*pi**2/div)))
# A2: hemisphere integral is a theorem about the integral, not about a0
num = sp.integrate(sp.cos(th)*sp.sin(th), (th, 0, pi/2)); den = sp.integrate(sp.sin(th), (th, 0, pi/2))
print('A2 <cos> over hemisphere     :', num/den, '| true; the physics link to a0 is the unproven premise')
print('A3 Komar/Gauss = (1/8piG)/(1/4piG):', sp.Rational(1, 8)/sp.Rational(1, 4), '| ratio of two normalisation constants that are both already in G; M_Komar=M for Schwarzschild (no 1/2 in the physical mass)')
# A4: circularity: a0 is DEFINED with kappa from A2, then r_MOND identity checked
k, c, G, Lam, M = sp.symbols('k c G Lam M', positive=True)
a0 = k*c*sp.sqrt(G*Lam*c**2/(8*pi*G)); Z = sp.sqrt(Z2)
rM = sp.sqrt(G*M/a0)
rs, RdS = 2*G*M/c**2, sp.sqrt(3/Lam)
r = sp.simplify((rM**2)/(Z/2*rs*RdS))
print('A4 r_MOND/geomean ratio^2 as function of kappa:', r, '| = 1 only if kappa=1/2 is INSERTED (not output): the assert re-checks its own input')
# Komar mass of Schwarzschild: M_K = M exactly (so no free 1/2): Komar integral on S^2: (1/8piG)*2*(GM/r^2)*4 pi r^2 *... = M
rr = sp.symbols('rr', positive=True)
MK = sp.Rational(1, 8)/(pi*G)*2*(G*M/rr**2)*4*pi*rr**2   # (1/8piG) * 2 * g * A, factor 2 from antisymmetry
print('A5 Komar mass of Schwarzschild:', sp.simplify(MK), '(= M: the 1/8piG already includes the 1/2)')
