"""argon_clues: arithmetic audit of the ten 'prove kappa=1/2 / 32pi' routes. PASS = the stated arithmetic is right.
It says nothing on whether the route DERIVES kappa; see README_routes.md."""
import sympy as s
R, th, x, mu = s.symbols('R theta x mu', positive=True)
Z2 = 32*s.pi/3
out = []
def chk(n, ok, note=''):
    out.append((n, bool(ok), note)); print(('PASS ' if ok else 'FAIL ') + n + (' | ' + note if note else ''))

# S^4 Euler: G4 = Riem^2 - 4 Ric^2 + Rs^2 for radius R
Riem2, Ric2, Rs = 24/R**4, 36/R**4, 12/R**2
G4 = Riem2 - 4*Ric2 + Rs**2
V4 = 8*s.pi**2*R**4/3
chk('chi(S4)=2 via 1/(32pi^2) int G4', s.simplify(G4*V4/(32*s.pi**2) - 2) == 0)
chk('32pi^2 = 3 pi Z^2 (route 6)', s.simplify(3*s.pi*Z2 - 32*s.pi**2) == 0, 'tautology: Z^2 is defined as 32pi/3; dividing by pi and 3 is chosen after the fact')
chk('32pi^2 = (2pi)^2 * 2! * 4', s.simplify((2*s.pi)**2*2*4 - 32*s.pi**2) == 0, 'any factorisation works; no selection rule')
chk('4*Vol(S4,R=1) = 32pi^2/3 (route 9)', s.simplify(4*s.Rational(8, 3)*s.pi**2 - 32*s.pi**2/3) == 0, 'then /pi is again ad hoc; S4 volume is R^4 dimensional, a0 needs R^-1')
chk('hemisphere <cos> = 1/2 (route 4)', s.integrate(s.cos(th)*s.sin(th), (th, 0, s.pi/2))/s.integrate(s.sin(th), (th, 0, s.pi/2)) == s.Rational(1, 2),
    'arithmetic fine; nothing says a0/(c sqrt(G rho)) is a hemisphere cosine average (flux-weight, solid-angle weight, 2pi vs 4pi all give other numbers)')
chk('mu_fw solves mu^2 + mu/x - 1 = 0 (route 3)', s.simplify((((s.sqrt(1+4*x**2)-1)/(2*x))**2 + ((s.sqrt(1+4*x**2)-1)/(2*x))/x - 1)) == 0,
    'the 4 sets the shape; replacing x->x/2 or a0->2a0 changes it to 1+x^2: rescaling a0 is exactly the kappa freedom, not a derivation of it')
chk('rho_DE/4 = Lambda c^2/(32 pi G) (route 8)', s.simplify(s.Symbol('L')*s.Symbol('c')**2/(8*s.pi*s.Symbol('G'))/4 - s.Symbol('L')*s.Symbol('c')**2/(32*s.pi*s.Symbol('G'))) == 0,
    'a restatement of a0 = (c/2) sqrt(G rho) with kappa=1/2 already inserted (a0^2 = c^2 G rho /4)')
chk('1/2 * 1/(4pi)^2 = 1/(32pi^2) (route 7)', s.Rational(1, 2)/(4*s.pi)**2 == 1/(32*s.pi**2), 'no step turns a heat-kernel normalisation into an acceleration')
chk('route 1 (Moyal hbar/2)', False, 'a0 has no hbar; an hbar/2 Weyl factor cannot set a classical coefficient')
chk('route 2 (Komar 1/2)', True, 'real factor 2 (Komar mass 1/8piG vs 1/4piG) but it is a normalisation of M, already absorbed in G; does not pick kappa')
chk('route 5 (KK half-residue)', False, 'a half-residue arises for any pole on the contour; no pole at H_Lambda is derived, nothing links it to a0')
chk('route 10 (Wald/MM 32pi)', False, 'MM prefactor 1/(32 pi G) is the normalisation of the same 1/(16 pi G) EH term; the 32pi in a0 enters only via kappa=1/2 and Z=sqrt(32pi/3)=2 sqrt(8pi/3)')
