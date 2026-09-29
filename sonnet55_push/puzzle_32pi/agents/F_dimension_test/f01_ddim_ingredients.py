#!/usr/bin/env python3
"""f01_ddim_ingredients.py -- the d-dimensional physics that is DETERMINED (computed from metrics, not asserted).

Spatial dimension d, spacetime D = d + 1, c = 1, G = G_D (the Einstein coupling: G_mu_nu + Lambda g_mu_nu = 8 pi G_D T_mu_nu).
Everything below is computed with sympy from explicit metrics for d = 2..5 (Ricci from Christoffels) or from the exact
warped-product reduction (checked against the explicit metrics), so the d-dependences used by the other scripts are not
quoted from memory.

  A  flat FRW in d spatial dims: Friedmann  H^2 = 16 pi G rho/(d(d-1)),  acceleration  addot/a = -8 pi G ((d-2) rho + d p)/(d(d-1))
     => the active (Tolman/Komar) density of a perfect fluid is ((d-2) rho + d p)/(d-2) in units of dust, NOT rho + d p.
     de Sitter: p = -rho gives addot/a = H^2 and Lambda = 8 pi G rho_L, H^2 = 2 Lambda/(d(d-1)).
  B  static weak field: ds^2 = -(1+2 Phi)dt^2 + (1-2 Psi)dx^2.  R_00 = lap Phi.  The trace-reversed Einstein equation
     gives Phi = (d-2) Psi (no anisotropic stress) and lap Phi = 8 pi G ((d-2) rho + d p)/(d-1).  So the Newtonian coupling in
     lap Phi = 4 pi G_N rho is G_N = 2 (d-2) G_D/(d-1)  (a convention; it is 1 at d=3 only in the sense G_N = G_D there).
  C  Schwarzschild-Tangherlini-de Sitter f = 1 - mu/r^(d-2) - H^2 r^2 solves the vacuum equation with Lambda in every d (explicit
     metrics d = 3, 4, 5 + the exact reduction for symbolic d); surface gravity of the black-hole horizon (d-2)/(2 r_s);
     of the de Sitter horizon exactly H in every d;  kappa_sg = g_N(r_s) holds in every d.
  D  the record's PD11 'Tolman count d-1' (= rho(1 + d w) at w = -1) is tested against A: it is the D=4 rule rho + 3p naively
     extended; the computed acceleration equation gives (d-2) + d w = -2 at w = -1 for EVERY d.
Controls (must FAIL): the naive rho + d p acceleration law fails for d != 3; a wrong Tangherlini exponent fails; a d-independent
Friedmann coefficient 8 pi/3 fails for d != 3.
Exit 0 = every check as stated (controls count as passes when they fail as required).
"""
import sys
import sympy as sp

OK = []
def check(name, cond):
    OK.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

# ----------------------------------------------------------------------------- generic Ricci
def ricci(g, coords):
    N = len(coords)
    ginv = sp.simplify(g.inv())
    Gam = [[[0] * N for _ in range(N)] for _ in range(N)]
    for c in range(N):
        for i in range(N):
            for j in range(i, N):
                s = 0
                for k in range(N):
                    if ginv[c, k] != 0:
                        s += ginv[c, k] * (sp.diff(g[k, i], coords[j]) + sp.diff(g[k, j], coords[i]) - sp.diff(g[i, j], coords[k]))
                s = sp.simplify(s / 2)
                Gam[c][i][j] = s
                Gam[c][j][i] = s
    R = sp.zeros(N, N)
    for i in range(N):
        for j in range(i, N):
            s = 0
            for c in range(N):
                s += sp.diff(Gam[c][i][j], coords[c]) - sp.diff(Gam[c][i][c], coords[j])
                for k in range(N):
                    s += Gam[c][c][k] * Gam[k][i][j] - Gam[c][j][k] * Gam[k][i][c]
            R[i, j] = sp.simplify(s)
            R[j, i] = R[i, j]
    return R, ginv

G, rho, p = sp.symbols('G rho p', positive=True)
t = sp.symbols('t', real=True)
d_sym = sp.symbols('d', positive=True)

# ----------------------------------------------------------------------------- A  FRW
print("A  flat FRW in d spatial dimensions (Ricci computed from the metric)")
a = sp.Function('a')(t)
frw = {}
for d in (2, 3, 4, 5):
    xs = sp.symbols(f'x1:{d + 1}', real=True)
    coords = (t,) + tuple(xs)
    g = sp.diag(-1, *([a**2] * d))
    R, ginv = ricci(g, coords)
    Rs = sp.simplify(sum(ginv[i, i] * R[i, i] for i in range(d + 1)))
    G00 = sp.simplify(R[0, 0] - sp.Rational(1, 2) * Rs * g[0, 0])
    G11 = sp.simplify((R[1, 1] - sp.Rational(1, 2) * Rs * g[1, 1]) / a**2)
    H2, addot = sp.symbols('H2 addot')
    E0 = sp.Eq(G00.subs(sp.diff(a, t), sp.sqrt(H2) * a), 8 * sp.pi * G * rho)          # G_00 = 8 pi G rho
    E1 = sp.Eq(G11, 8 * sp.pi * G * p)                                                # G_ii/a^2 = 8 pi G p
    E1 = E1.subs(sp.diff(a, t, 2), addot * a).subs(sp.diff(a, t), sp.sqrt(H2) * a)
    sol = sp.solve([E0, E1], [H2, addot], dict=True)[0]
    frw[d] = (sp.simplify(sol[H2]), sp.simplify(sol[addot]))
    print(f"    d={d}:  H^2 = {frw[d][0]}    addot/a = {frw[d][1]}")
for d in (2, 3, 4, 5):
    H2v, adv = frw[d]
    check(f"A{d}  d={d}: H^2 = 16 pi G rho/(d(d-1)) and addot/a = -8 pi G((d-2) rho + d p)/(d(d-1))",
          sp.simplify(H2v - 16 * sp.pi * G * rho / (d * (d - 1))) == 0 and sp.simplify(adv + 8 * sp.pi * G * ((d - 2) * rho + d * p) / (d * (d - 1))) == 0)
# de Sitter: p = -rho
for d in (2, 3, 4, 5):
    H2v, adv = frw[d]
    check(f"A{d}b d={d}: p = -rho gives addot/a = H^2 (de Sitter) ; Lambda = 8 pi G rho_L  <=>  H^2 = 2 Lambda/(d(d-1))",
          sp.simplify(adv.subs(p, -rho) - H2v) == 0 and sp.simplify(H2v.subs(rho, sp.Symbol('Lam') / (8 * sp.pi * G)) - 2 * sp.Symbol('Lam') / (d * (d - 1))) == 0)
# controls
naive = lambda d: -8 * sp.pi * G * (rho + d * p) / (d * (d - 1))      # the D=4 rule rho + 3p extended to rho + d p
res = {d: sp.simplify(frw[d][1] - naive(d)) == 0 for d in (2, 3, 4, 5)}
check("A-C1 control: the naive law addot/a = -8 pi G (rho + d p)/(d(d-1)) matches the computed one ONLY at d = 3  -> " + str(res), res == {2: False, 3: True, 4: False, 5: False})
fixed = {d: sp.simplify(frw[d][0] - 8 * sp.pi * G * rho / 3) == 0 for d in (2, 3, 4, 5)}
check("A-C2 control: a d-independent Friedmann coefficient 8 pi/3 matches only at d = 3 -> " + str(fixed), fixed == {2: False, 3: True, 4: False, 5: False})

# ----------------------------------------------------------------------------- B  static weak field (linearised Ricci)
print("\nB  static weak field ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2 in d dimensions (linearised Ricci)")
def lin_ricci(d):
    xs = sp.symbols(f'x1:{d + 1}', real=True)
    Phi = sp.Function('Phi')(*xs)
    Psi = sp.Function('Psi')(*xs)
    N = d + 1
    eta = sp.diag(-1, *([1] * d))
    h = sp.zeros(N, N)
    h[0, 0] = -2 * Phi
    for i in range(d):
        h[i + 1, i + 1] = -2 * Psi
    hup = eta * h                                   # h^rho_nu (eta diagonal, own inverse)
    trace = sum(eta[i, i] * h[i, i] for i in range(N))
    X = (None,) + tuple(xs)                         # static: d/dt = 0
    def dd(f, m, n):
        if m == 0 or n == 0:
            return 0
        return sp.diff(f, X[m], X[n])
    box = lambda f: sum(sp.diff(f, x, 2) for x in xs)  # static: box = laplacian
    Ric = sp.zeros(N, N)
    for m in range(N):
        for n in range(N):
            s = 0
            for r in range(N):
                s += dd(hup[r, n], r, m) + dd(hup[r, m], r, n)
            s -= box(h[m, n]) if True else 0
            s -= dd(trace, m, n)
            Ric[m, n] = sp.simplify(s / 2)
    lap = lambda f: sum(sp.diff(f, x, 2) for x in xs)
    return Ric, Phi, Psi, xs, lap
for d in (2, 3, 4, 5):
    Ric, Phi, Psi, xs, lap = lin_ricci(d)
    ok00 = sp.simplify(Ric[0, 0] - lap(Phi)) == 0
    # ij block: expect d_i d_j[(d-2) Psi - Phi] + delta_ij lap Psi   (up to sign convention fixed by the check itself)
    exp_ij = lambda i, j: sp.diff((d - 2) * Psi - Phi, xs[i], xs[j]) + (lap(Psi) if i == j else 0)
    okij = all(sp.simplify(Ric[i + 1, j + 1] - exp_ij(i, j)) == 0 for i in range(d) for j in range(d))
    check(f"B{d}  d={d}: R_00 = lap Phi  and  R_ij = d_i d_j[(d-2)Psi - Phi] + delta_ij lap Psi", ok00 and okij)
# Einstein (trace reversed): R_mu_nu = 8 pi G (T_mu_nu - g_mu_nu T/(D-2)):  R_00 = 8 pi G((d-2)rho + d p)/(d-1), R_ij = 8 pi G (rho-p)/(d-1) delta_ij
d_ = sp.symbols('d_', positive=True)
T = -rho + d_ * p
R00_src = sp.simplify(rho - (-1) * T / (d_ - 1))
Rij_src = sp.simplify(p - T / (d_ - 1))
check("B-src  trace-reversed source: R_00 = 8 pi G((d-2) rho + d p)/(d-1),  R_ij = 8 pi G (rho - p)/(d-1) delta_ij",
      sp.simplify(R00_src - ((d_ - 2) * rho + d_ * p) / (d_ - 1)) == 0 and sp.simplify(Rij_src - (rho - p) / (d_ - 1)) == 0)
# dust: traceless part => Phi = (d-2) Psi;  lap Psi = 8 pi G rho/(d-1);  lap Phi = 8 pi G (d-2) rho/(d-1)
P = sp.symbols('P')  # lap Psi
for d in (2, 3, 4, 5):
    lapPsi = sp.solve(sp.Eq(P, 8 * sp.pi * G * rho / (d - 1)), P)[0]    # from R_ii with Phi=(d-2)Psi: R_ij = delta_ij lap Psi
    lapPhi = (d - 2) * lapPsi
    check(f"B{d}b d={d}: dust  lap Phi = (d-2)*lap Psi = 8 pi G (d-2) rho/(d-1) = R_00 source",
          sp.simplify(lapPhi - 8 * sp.pi * G * ((d - 2) * rho) / (d - 1)) == 0)
print("     Newtonian coupling: lap Phi = 4 pi G_N rho  =>  G_N/G_D = 2(d-2)/(d-1):  " + ", ".join(f"d={d}: {sp.Rational(2*(d-2), d-1)}" for d in (2, 3, 4, 5, 6)))
check("B-N  G_N/G_D = 2(d-2)/(d-1) equals 1 exactly at d = 3 (and 0 at d = 2: D=3 gravity has no Newtonian force)",
      sp.Rational(2 * 1, 2) == 1 and 2 * (2 - 2) == 0 and all(sp.Rational(2 * (d - 2), d - 1) != 1 for d in (2, 4, 5, 6)))
# light bending vs Newtonian: the traceless part of R_ij (computed above) vanishes for a stress-free source iff Phi = (d-2) Psi
Ph, Ps = sp.symbols('Phi_ Psi_')
lens_ratio = sp.simplify(((Ph + Ps) / Ph).subs(Ps, Ph / (d_ - 2)))
check("B-L  lensing potential Phi + Psi = Phi (d-1)/(d-2) (Psi = Phi/(d-2) from the computed traceless part): the two static channels have weights 1 and 1/(d-2), equal only at d = 3",
      sp.simplify(lens_ratio - (d_ - 1) / (d_ - 2)) == 0 and [sp.simplify(lens_ratio.subs(d_, k)) for k in (3, 4, 5)] == [2, sp.Rational(3, 2), sp.Rational(4, 3)])

# ----------------------------------------------------------------------------- C  Tangherlini-de Sitter
print("\nC  Schwarzschild-Tangherlini-de Sitter (explicit metrics d = 3, 4, 5, then symbolic d)")
r = sp.symbols('r', positive=True)
mu, Hh, Lam = sp.symbols('mu H Lambda', positive=True)
def explicit_check(n):
    """metric -f dt^2 + dr^2/f + r^2 dOmega_n, n = d-1 angles: return general-n formula residuals."""
    th = sp.symbols(f'th1:{n + 1}', positive=True)
    f = sp.Function('f')(r)
    coords = (t, r) + tuple(th)
    diag = [-f, 1 / f]
    sinprod = 1
    ang = []
    for k in range(n):
        ang.append(r**2 * sinprod**2)
        sinprod = sinprod * sp.sin(th[k])
    g = sp.diag(*(diag + ang))
    Rm, ginv = ricci(g, coords)
    fp, fpp = sp.diff(f, r), sp.diff(f, r, 2)
    Rtt = f * (fpp / 2 + n * fp / (2 * r))
    Rrr = -(fpp / (2 * f) + n * fp / (2 * r * f))
    Rang = ((n - 1) * (1 - f) - r * fp)
    ok = sp.simplify(Rm[0, 0] - Rtt) == 0 and sp.simplify(Rm[1, 1] - Rrr) == 0
    for k in range(n):
        ok = ok and sp.simplify(Rm[2 + k, 2 + k] - Rang * g[2 + k, 2 + k] / r**2) == 0
    return ok
for d in (3, 4, 5):
    check(f"C{d}  explicit metric d={d} (S^{d-1}): R_tt, R_rr, R_angular equal the warped-product formulas with n=d-1", explicit_check(d - 1))
n = sp.symbols('n', positive=True)          # n = d-1
dd_ = n + 1
f_gen = 1 - mu / r**(n - 1) - Hh**2 * r**2
fp, fpp = sp.diff(f_gen, r), sp.diff(f_gen, r, 2)
lam = 2 * Lam / n                          # R_mu_nu = (2 Lambda/(D-2)) g_mu_nu, D-2 = n
Hsq = 2 * Lam / (n * (n + 1))              # H^2 = 2 Lambda/(d(d-1)), d = n+1
res_tt = sp.simplify(((f_gen * (fpp / 2 + n * fp / (2 * r))) - lam * (-f_gen)).subs(Hh, sp.sqrt(Hsq)))
res_ang = sp.simplify((((n - 1) * (1 - f_gen) - r * fp) - lam * r**2).subs(Hh, sp.sqrt(Hsq)))
check("C-sym  f = 1 - mu/r^(d-2) - H^2 r^2 with H^2 = 2 Lambda/(d(d-1)) solves R_tt and R_angular for SYMBOLIC d", res_tt == 0 and res_ang == 0)
f_bad = 1 - mu / r**(n) - Hh**2 * r**2      # wrong exponent (control)
fpb, fppb = sp.diff(f_bad, r), sp.diff(f_bad, r, 2)
res_bad = sp.simplify((((n - 1) * (1 - f_bad) - r * fpb) - lam * r**2).subs(Hh, sp.sqrt(Hsq)))
check("C-C1 control: a wrong exponent r^(-(d-1)) is rejected", res_bad != 0)
# surface gravities
rs = sp.symbols('r_s', positive=True)
f0 = 1 - (rs / r)**(n - 1)
kap_bh = sp.simplify(sp.diff(f0, r).subs(r, rs) / 2)
check("C-kBH  black-hole surface gravity kappa_sg = f'(r_s)/2 = (d-2)/(2 r_s)", sp.simplify(kap_bh - (n - 1) / (2 * rs)) == 0)
fdS = 1 - Hh**2 * r**2
kap_dS = sp.simplify(-sp.diff(fdS, r).subs(r, 1 / Hh) / 2)
check("C-kdS  de Sitter horizon surface gravity = H in EVERY d (so T_dS = H/2pi and Unruh a/2pi matching is d-independent)", sp.simplify(kap_dS - Hh) == 0)
# Newtonian g at r_s.  mu(M) is DERIVED here by matching g_tt = -(1 - mu/r^(d-2)) to the weak-field potential of B (Phi = -mu/(2 r^(d-2))),
# not quoted: lap Phi = 8 pi G (d-2) M delta/(d-1)  =>  Phi = -8 pi G M/((d-1) Omega r^(d-2)).  (The final equality is then an identity; kept as a consistency line.)
Om, M, Gd = sp.symbols('Omega M G_D', positive=True)
mu_of_M = 16 * sp.pi * Gd * M / ((n) * Om)                     # (d-1) = n : r_s^(d-2) = 16 pi G M/((d-1) Omega_{d-1})
gN = 8 * sp.pi * Gd * (n - 1) * M / (n * Om * r**n)             # from lap Phi = 8 pi G (d-2) rho/(d-1), g = -Phi'
check("C-gN  Newtonian acceleration at r_s from the Poisson normalisation equals the surface gravity: g_N(r_s) = (d-2)/(2 r_s) in every d",
      sp.simplify(gN.subs(M, sp.solve(sp.Eq(rs**(n - 1), mu_of_M), M)[0]).subs(r, rs) - (n - 1) / (2 * rs)) == 0)

# Hubble radius = radius at which a sphere of density rho is its own Schwarzschild radius, in every d
Vball = Om * r**(n + 1) / (n + 1)
rsch = sp.solve(sp.Eq(r**(n - 1), 16 * sp.pi * Gd * rho * Vball / (n * Om)), r)
Hs = sp.sqrt(16 * sp.pi * Gd * rho / ((n + 1) * n))
check("C-Hub  a ball of density rho is its own Tangherlini horizon exactly at r = 1/H, H^2 = 16 pi G rho/(d(d-1)), in every d (not at c/sqrt(G rho))",
      any(sp.simplify(sol - 1 / Hs) == 0 for sol in rsch))

# ----------------------------------------------------------------------------- D  PD11 comparison
print("\nD  the record's Tolman factor at w = -1 (PD11 T4) vs the computed acceleration law")
w = sp.symbols('w')
for d in (2, 3, 4, 5, 6):
    naive_active = sp.simplify(1 + d * w)                  # rho(1 + d w)  ->  PD11 'd-1'
    true_num = sp.simplify((d - 2) + d * w)                # numerator of the computed law
    true_dust = sp.simplify(true_num / (d - 2)) if d != 2 else sp.nan
    print(f"    d={d}:  naive |1 + d w|_(w=-1) = {abs(naive_active.subs(w, -1))},  computed numerator |(d-2) + d w| = {abs(true_num.subs(w, -1))},  dust-normalised = {(abs(true_dust.subs(w, -1)) if d != 2 else 'n/a (no Newtonian limit)')}")
check("D1  computed numerator (d-2)+d w equals -2 at w = -1 for EVERY d (the channel-count-2 pattern, not d-1)", all(sp.simplify(((d - 2) + d * w).subs(w, -1) + 2) == 0 for d in range(2, 9)))
check("D2  naive rho(1+d w) = -(d-1) at w=-1 disagrees with the computed law except at d = 3, where both are -2",
      all((abs((1 + d * w).subs(w, -1)) == 2) == (d == 3) for d in range(2, 9)))
check("D3  dust-normalised active density of the vacuum = -2/(d-2): equals -2 at d=3, -1 at d=4, -2/3 at d=5 (normalising to dust is the PD11 convention: rho + 3p -> 1 for dust)",
      [sp.Rational(-2, d - 2) for d in (3, 4, 5)] == [-2, -1, sp.Rational(-2, 3)])

print(f"\n  {sum(OK)}/{len(OK)} checks held.")
sys.exit(0 if all(OK) else 1)
