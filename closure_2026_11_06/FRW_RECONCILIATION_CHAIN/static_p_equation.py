"""Exact first variation of the native AC2q polarization terms (on branch) for a static,
x-dependent lapse N(x) and leaf volume sqrt(h)(x), homogeneous clock rate v.
Density (leaf divergence D = (sqrt h P^x)'/sqrt h, B = sqrt h P^x, A_x = N'/N):
    N sqrt h [ P.A - gamma D^2/2 - 2 gamma X D ],  X = v^2/(2N^2)
  = B N' - gamma N (B')^2/(2 sqrt h) - gamma v^2 B'/N.
Compares the Euler derivative with the unweighted PN density used in AC7 Q2 / AC8."""
import sympy as sp
x = sp.Symbol('x'); g, v = sp.symbols('gamma v', positive=True)
N = sp.Function('N')(x); s = sp.Function('sqrth')(x); B = sp.Function('B')(x)
L = B*sp.diff(N, x) - g*N*sp.diff(B, x)**2/(2*s) - g*v**2*sp.diff(B, x)/N
EL = sp.euler_equations(L, [B], [x])[0].lhs
D = sp.diff(B, x)/s
target = sp.diff(N, x)*(1 - g*v**2/N**2) + g*sp.diff(N*D, x)
print('full-measure Euler derivative == N_x (1 - gamma v^2/N^2) + gamma (N D)_x :',
      sp.simplify(EL - target) == 0)
# unweighted PN density of AC8 (no N sqrt h): P phi' - gamma/2 [(P' + C2)^2 - C2^2], C2 = v^2/(1+phi)^2
phi = sp.Function('phi')(x); P = sp.Function('P')(x)
C2 = v**2/(1+phi)**2
Lpn = P*sp.diff(phi, x) - g/2*((sp.diff(P, x)+C2)**2 - C2**2)
ELpn = sp.expand(sp.euler_equations(Lpn, [P], [x])[0].lhs)
off_pn = sp.simplify(ELpn - sp.diff(phi, x) - g*sp.diff(P, x, 2))
off_full = sp.simplify((target - sp.diff(N, x) - g*sp.diff(N*D, x)).subs(N, 1+phi))
print('PN offset   :', sp.factor(off_pn), ' -> relative', sp.factor(off_pn/sp.diff(phi, x)))
print('exact offset:', sp.factor(off_full), ' -> relative', sp.factor(off_full/sp.diff(phi, x)))
print('ratio PN/exact at phi->0:', sp.limit(off_pn/off_full, phi, 0) if False else sp.simplify((off_pn/off_full)))

# Lapse (Poisson-side) variation of the clock + stiffness terms at fixed B, sqrt h:
# N sqrt h [X - 2 gamma X D] = sqrt h v^2/(2N) - gamma v^2 B'/N
Nn = sp.Symbol('N', positive=True); Bp, sh = sp.symbols('Bp sqrth', positive=True)
Lclock = sh*v**2/(2*Nn) - g*v**2*Bp/Nn
dN = sp.diff(Lclock, Nn); Dsym = Bp/sh
print('dL/dN (clock+stiffness) == -sqrt h v^2 (1 - 2 gamma D)/(2 N^2):',
      sp.simplify(dN + sh*v**2*(1 - 2*g*Dsym)/(2*Nn**2)) == 0)
print('AC8 PN Poisson term: s^2 (1 - 2 gamma div P)/(1+phi)^3 -> same (1 - 2 gamma D) factor, measure power N^-2 vs (1+phi)^-3')
