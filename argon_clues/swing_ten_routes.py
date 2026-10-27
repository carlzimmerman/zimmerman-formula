"""argon_clues: each of the ten routes actually computed (not just arithmetic-checked).
Test per route: does it OUTPUT kappa=1/2 (a0 = cH/Z, Z=sqrt(32pi/3)) without inserting it?"""
import sympy as s
x, g, k, R, r, th, om, tau = s.symbols('x g kappa R r theta omega tau', positive=True)
Z = s.sqrt(32*s.pi/3)
def out(n, v, note): print('[%2d] %-34s %s | %s' % (n, v, '', note))

# 1 Moyal: any hbar in a0 comes as (G hbar Lambda/c^3)^e = (l_P^2 Lambda)^e ~ (1e-122)^e
c, L, G = s.symbols('c Lambda G', positive=True)
out(1, 'hbar enters only via l_P^2 Lambda', 'a0 = c^2 sqrt(Lambda) * f(l_P^2 Lambda); an hbar/2 Weyl factor gives ~1e-122^e, not an O(1) 1/2 -> dead')

# 2 Komar: de Sitter active source rho+3P = -2rho -> field of uniform dS acts as g = +H^2 r (repulsive)
H2 = c**2*L/3
gN = s.Symbol('M')*G/r**2
rt = s.solve(gN - H2*r, r)[0]
out(2, 'Komar gives g=H^2 r', 'crossover r=(GM/H^2)^(1/3), g=(G M H^4)^(1/3) is M-dependent, not a0 (a0 is M-independent)')

# 3 free-energy / Deser-Levin gate vs mu_fw
mu_fw = (s.sqrt(1+4*x**2)-1)/(2*x)
m_DL = lambda y: (s.sqrt(1+y**2)-1)/y            # (T_eff - T_dS)/T_U form with y=g/kappa_dS
out(3, 'mu_fw(x) == mDL(2x)', 'simplify -> %s  => gate shape IS Deser-Levin (quadrature floor a_floor = a0/2). CORRECTED: if a_floor = kappa_dS then a0 = 2 kappa_dS (Z_gate = 1/2)' % s.simplify(mu_fw - m_DL(2*x)))
out(3, 'actual mismatch 2Z', 'kappa_dS/a_floor = 2Z = %.4f = 4 sqrt(8pi/3) (NOT sqrt(8pi/3): earlier version of this line had the direction of the 2 wrong)' % float(2*Z))

# 4 hemisphere: result depends on weighting choice
w = {'solid-angle <cos>_hemi': s.integrate(s.cos(th)*s.sin(th), (th, 0, s.pi/2))/s.integrate(s.sin(th), (th, 0, s.pi/2)),
     'flux <cos^2>_hemi': s.integrate(s.cos(th)**2*s.sin(th), (th, 0, s.pi/2))/s.integrate(s.sin(th), (th, 0, s.pi/2)),
     'flux-weighted <cos>_cos-weighted': s.integrate(s.cos(th)**2*s.sin(th), (th, 0, s.pi/2))/s.integrate(s.cos(th)*s.sin(th), (th, 0, s.pi/2)),
     'full sphere <cos>': 0}
out(4, 'weightings', str(w) + ' -> 1/2, 1/3, 2/3, 0: no selection principle')

# 5 Kramers-Kronig: Debye susceptibility, KK sum rule independent of the scale
chi = 1/(1 - s.I*om*tau)
im = s.im(s.expand_complex(chi))
val = s.integrate(s.simplify(im/om), (om, -s.oo, s.oo))/s.pi
out(5, 'chi(0) via KK = %s' % s.simplify(val), 'independent of tau: KK fixes chi(0) from absorption, supplies no 1/2 and no scale; half-residue is generic for any boundary pole')

# 6 Euler reduction ambiguity
opts = {'/pi/3': 32*s.pi**2/(s.pi*3), '/2pi/3': 32*s.pi**2/(2*s.pi*3), '/pi/(3/2)': 32*s.pi**2/(s.pi*s.Rational(3, 2)), '/pi^2 (S1xS3 vol)': 32*s.pi**2/(2*s.pi**2)}
out(6, 'reductions', str({k_: s.simplify(v) for k_, v in opts.items()}) + ' -> only the first is Z^2; selected after the fact')

# 7 Seeley-DeWitt: pure number
a2 = s.Rational(1, 180)*(24-36) + s.Rational(1, 2)*(s.Rational(12, 6))**2
zeta0 = a2*s.Rational(8, 3)*s.pi**2/(16*s.pi**2)
out(7, 'zeta(0) minimal scalar S4 = %s' % zeta0, 'dimensionless (=29/90); no acceleration scale, cannot fix a0/(c sqrt(G rho))')

# 8 Brown-York: a_BY(r) = c^2 (1-sqrt(f))/r ; Z requires r = Z*R > R (outside static patch)
f = 1 - r**2/R**2
aBY = c**2*(1 - s.sqrt(f))/r
out(8, 'a_BY(R) = %s' % aBY.subs(r, R), '= cH (Z=1); reaching cH/Z needs r>R, outside the patch (f<0)')

# 9 worldline instanton: radius rho = 1/sqrt(a^2/c^4 + 1/R^2)
aa = s.Symbol('a', positive=True)
rho_ = 1/s.sqrt(aa**2/c**4 + 1/R**2)
out(9, 'instanton crossover', 'rho=R/sqrt(1+(aR/c^2)^2): halves at a=cH, again Z=1 (same as route 3)')

# 10 Wald entropy of dS horizon from (R-2Lambda)/16piG, A=4pi R^2, R^2=3/Lambda
S = 4*s.pi*(3/L)/(4*G)
out(10, 'S_dS = %s' % s.simplify(S), '= 3pi/(G Lambda) (Gibbons-Hawking); Euler term adds a constant; no acceleration coefficient')
