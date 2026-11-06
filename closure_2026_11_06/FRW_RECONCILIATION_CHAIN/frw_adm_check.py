"""Independent ADM reduction of the native AC2q action on scalar FRW.

Built from the general ADM expressions (Christoffels of h, K_ij with shift),
not from the frw_independent packet. Two divergence conventions are run:
  'leaf'      D = (1/sqrt h) d_i(sqrt h P^i)          (AC2 ACTION.md definition)
  'spacetime' D = nabla_mu P^mu = leaf + P.A           (control: what 1-2z needs)
"""
import sympy as sp

t, x, eta = sp.symbols('t x eta', real=True)
k, M, K, g, v, H, eps = sp.symbols('k M K gamma v H epsilon', positive=True)
a = sp.Function('a')(t)
Z = sp.Function('Z')(t)
al, ps, p = sp.symbols('alpha psi p', real=True)   # lapse, shift potential, polarization amps

zeta = eta*Z*sp.cos(k*x)
N = 1 + eta*al*sp.cos(k*x)
psi = eta*ps*sp.cos(k*x)          # shift potential, same profile as zeta
Nx_low = sp.diff(psi, x)           # lower-index shift N_x
h = sp.diag(*([a**2*sp.exp(2*zeta)]*3))
hinv = h.inv()
coords = [x, sp.Symbol('y'), sp.Symbol('zz')]
X1 = coords
# Christoffels of h (only x-dependence)
def d(f, i):
    return sp.diff(f, X1[i])
Gam = [[[sum(hinv[l, m]*(d(h[m, i], j)+d(h[m, j], i)-d(h[i, j], m)) for m in range(3))/2
         for j in range(3)] for i in range(3)] for l in range(3)]
Nlow = [Nx_low, 0, 0]
DN = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        DN[i, j] = d(Nlow[j], i) - sum(Gam[l][i][j]*Nlow[l] for l in range(3))
Kij = (sp.diff(h, t) - DN - DN.T)/(2*N)
Kmix = hinv*Kij
KK = sum(Kmix[i, j]*Kmix[j, i] for i in range(3) for j in range(3))
Ktr = Kmix.trace()
# 3-Ricci scalar for conformally flat h = a^2 e^{2 zeta} delta (3D): R = -e^{-2z}(4 lap z + 2 |grad z|^2)/a^2
R3 = -sp.exp(-2*zeta)*(4*sp.diff(zeta, x, 2)+2*sp.diff(zeta, x)**2)/a**2
sqh = sp.sqrt(h.det())
sqh = a**3*sp.exp(3*zeta)

# matter: phi=phibar(t), X = v^2/(2N^2) (shift drops: grad phi spatial = 0)
X = v**2/(2*N**2)
# proper polarization amplitude along x: P^x = -eta p sin(kx)/(a e^zeta)
Pup = [-eta*p*sp.sin(k*x)/(a*sp.exp(zeta)), 0, 0]
A_low = [d(sp.log(N), i) for i in range(3)]
PA = sum(Pup[i]*A_low[i] for i in range(3))
PP = sum(h[i, i]*Pup[i]**2 for i in range(3))
Dleaf = sum(d(sqh*Pup[i], i) for i in range(3))/sqh
V = (3-eps)*M*H**2
vsq = 2*M*eps*H**2     # background: eps = v^2/(2 M H^2)

def reduce(Dconv):
    D = Dleaf if Dconv == 'leaf' else Dleaf + PA
    Lm = N*sqh*(X - V + PA - K*PP/2 - g*D**2/2 - 2*g*X*D)
    Lg = M*N*sqh*(R3 + KK - Ktr**2)/2
    L = (Lg + Lm).subs(v, sp.sqrt(vsq))
    L2 = sp.diff(L, eta, 2).subs(eta, 0)/2
    # Fourier average over x
    L2 = sp.simplify(sp.integrate(sp.expand(L2), (x, 0, 2*sp.pi/k))*k/(2*sp.pi))
    L2 = sp.expand(L2.subs(sp.Derivative(a, t), a*H))
    return L2

def eliminate(L2):
    Zd = sp.Symbol('Zd'); Zs = sp.Symbol('Zs')
    L2 = L2.subs(sp.Derivative(Z, t), Zd).subs(Z, Zs)
    # P block couples only to lapse: every p-dependent term is free of Z, Zd and the shift
    Pblk = sp.expand(L2 - L2.subs(p, 0))
    print(' P block          :', sp.factor(Pblk))
    assert not (Pblk.free_symbols & {Zd, Zs, ps}), 'P couples beyond lapse'
    # polarization: algebraic
    psol = sp.solve(sp.diff(L2, p), p)[0]
    Lp = sp.expand(L2.subs(p, psol))
    # shift then lapse constraints
    ssol = sp.solve(sp.diff(Lp, ps), al)
    alsol = ssol[0]
    L3 = sp.simplify(Lp.subs(al, alsol))
    # after shift fixes alpha, the psi-dependent pieces must vanish
    assert sp.simplify(sp.diff(L3, ps)) == 0
    # lapse constraint now fixes psi; but psi already drops -> L3 has no psi
    L3 = sp.expand(L3)
    # integrate by parts Zs*Zd*c(t): -> -cdot/2 Zs^2, with adot=aH, Hdot=-eps H^2, eps const at this instant? keep epsdot symbol
    c = L3.coeff(Zs, 1).coeff(Zd, 1)
    at = sp.Symbol('at', positive=True)
    epsd = sp.Symbol('epsdot')
    cf = c.subs(a, at)
    cdot = (sp.diff(cf, at)*at*H + sp.diff(cf, H)*(-eps*H**2) + sp.diff(cf, eps)*epsd).subs(at, a)
    L4 = sp.expand(L3 - c*Zs*Zd - cdot/2*Zs**2)
    kin = sp.factor(L4.coeff(Zd, 2))
    mass = sp.factor(L4.coeff(Zs, 2))
    return alsol, sp.factor(psol), kin, mass

z = sp.Symbol('z')
for conv in ['leaf', 'spacetime']:
    L2 = reduce(conv)
    alsol, psol, kin, mass = eliminate(L2)
    q = k/a
    # normalize: expected (M a^3/4)[eps + f(z) q^2/(2 M H^2 (K+g q^2))] Zd^2 with averaging 1/2
    norm = M*a**3/2
    f = sp.simplify(((kin/norm - eps)*2*M*H**2*(K+g*q**2)/q**2).subs(M, eps*0+M))
    f_z = sp.factor(sp.simplify(f.subs(eps, z/(2*M*H**2*g))))  # z = gamma v^2 = 2 M eps H^2 gamma
    print('==', conv)
    print(' shift constraint: alpha =', alsol)
    print(' p solution       :', psol)
    print(' gradient coeff   :', sp.factor(mass/norm))
    print(' mixing factor f  :', f_z)
    # UV speed with physical dictionary K=1/(2M), gamma=Lstar^2/(4M)
    Ls = sp.Symbol('Ls', positive=True)
    c2 = sp.limit((-mass/kin*a**2/k**2).subs({K: 1/(2*M), g: Ls**2/(4*M)}), k, sp.oo)
    c2z = sp.simplify(c2.subs(eps, 2*z/(H**2*Ls**2)))   # eps*ell^2 = z, ell^2 = H^2 Ls^2/2
    print(' UV c^2 (physical):', sp.factor(c2z))
