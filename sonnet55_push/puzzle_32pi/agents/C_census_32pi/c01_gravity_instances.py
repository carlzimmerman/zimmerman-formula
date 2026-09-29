#!/usr/bin/env python3
"""c01_gravity_instances.py -- census lane C: the GRAVITATIONAL instances of 32 pi (and 16 pi, 8 pi) recomputed from scratch.

Everything below is derived (sympy / numpy), not quoted.  G = c = 1 unless stated.
  A  Einstein-Hilbert action to O(eps^2) for a TT plane wave h_+(t,z): kinetic normalisation, energy density, and the
     independent Isaacson route (t_mu_nu = -<G^(2)_mu_nu>/8pi).  Result: rho_GW = <hdot_ij hdot_ij>/(32 pi) = <hdot_+^2 + hdot_x^2>/(16 pi)
  B  canonical graviton normalisation: kappa^2 = 32 pi (tensor convention) vs 16 pi (per-polarisation convention)
  C  quadrupole formula: the angular integral 8 pi/5 cancels the 32 pi; Peters 32/5, 64/5, chirp 96/5 pi^(8/3)  (no 32 pi survives)
  D  Larmor: the integral of sin^2 = 8 pi/3 (same number as the Friedmann coefficient, different origin)
  E  black-hole thermodynamics: Kerr area 8 pi M r_+, first law kappa/8pi = (1/2pi)(1/4), Smarr, Komar 1/4pi, ADM 1/16pi,
     and the sharp bound  A kappa^2 <= pi  over Kerr-Newman (equality only for Schwarzschild)
  F  Nariai / de Sitter horizon-area census A*Lambda
Controls (each MUST be caught): a wrong Isaacson coefficient, a wrong canonical kappa^2, a projector without the trace term, a wrong
Kerr first law, the reverse inequality A kappa^2 >= pi/2.
Exit 0 = every check and every control behaves.
"""
import itertools
import sys
import numpy as np
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

pi = sp.pi

# ----------------------------------------------------------------------------- curvature machinery (diagonal or general metric)
def christoffel(g, X):
    n = len(X); gi = g.inv()
    return [[[sp.simplify(sum(gi[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(n)) / 2)
              for k in range(n)] for j in range(n)] for i in range(n)]

def ricci(g, X):
    n = len(X); G = christoffel(g, X)
    Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(n):
            e = 0
            for i in range(n):
                e += sp.diff(G[i][j][k], X[i]) - sp.diff(G[i][j][i], X[k])
                for l in range(n):
                    e += G[i][i][l] * G[l][j][k] - G[i][k][l] * G[l][j][i]
            Ric[j, k] = e
    return Ric

def einstein_and_R(g, X):
    Ric = ricci(g, X); gi = g.inv()
    R = sum(gi[i, j] * Ric[i, j] for i in range(len(X)) for j in range(len(X)))
    return Ric - g * R / 2, R

# ============================================================================= A. EH action and Isaacson coefficient
print("\nA  Einstein-Hilbert action of a TT plane wave, to second order in the amplitude")
t, z, x, y, eps = sp.symbols('t z x y epsilon', real=True)
X = [t, x, y, z]
hf = sp.Function('h')(t, z)                                    # plus polarisation h_xx = -h_yy = h
g = sp.diag(-1, 1 + eps * hf, 1 - eps * hf, 1)
G, Rs = einstein_and_R(g, X)
sqrtg = sp.sqrt(-g.det())
L = sp.series(sp.simplify(sqrtg * Rs), eps, 0, 3).removeO()
L2 = sp.expand(L.coeff(eps, 2))
L1 = sp.expand(L.coeff(eps, 1))
# L1 is a total derivative (its Euler-Lagrange expression vanishes identically)
from sympy.calculus.euler import euler_equations
el1 = euler_equations(L1, [hf], [t, z]) if sp.simplify(L1) != 0 else []
check("O(eps) term of sqrt(-g) R vanishes or is a total derivative for a TT wave (delta R = d d h - box h = 0)", len(el1) == 0 or sp.simplify(el1[0].lhs) == 0)
el2 = euler_equations(L2, [hf], [t, z])[0].lhs
htt, hzz = sp.diff(hf, t, 2), sp.diff(hf, z, 2)
el2 = sp.expand(sp.simplify(el2))
A0 = -el2.coeff(htt)
check("EL equation of the quadratic action is proportional to the wave operator h_tt - h_zz", sp.simplify(el2 + A0 * (htt - hzz)) == 0)
print(f"      kinetic coefficient A0 in  sqrt(-g)R|_eps^2  ~  (A0/2)(hdot^2 - h_z^2):  A0 = {A0}")
check("A0 = 1, i.e. (1/16 pi) sqrt(-g) R -> (1/32 pi)(hdot^2 - h_z^2) = (1/64 pi)(hdot_ij hdot_ij - ...), since h_ij h_ij = 2 h^2",
      sp.simplify(A0 - 1) == 0)
# energy density from the canonical (Hamiltonian) form of the quadratic Lagrangian
hd, hz = sp.symbols('hd hz', real=True)
rho_can = sp.Rational(1, 16) / pi * sp.Rational(1, 2) * A0 * (hd**2 + hz**2)      # (1/16pi) * (A0/2)(hd^2+hz^2)
# plane wave h = h0 cos(w(t-z)):  <hd^2> = <hz^2> = w^2 h0^2/2
w, h0, ph = sp.symbols('omega h0 phi', positive=True)
hw = h0 * sp.cos(ph)
avg = lambda expr: sp.integrate(expr, (ph, 0, 2 * pi)) / (2 * pi)
rho_avg = avg(rho_can.subs({hd: -w * h0 * sp.sin(ph), hz: w * h0 * sp.sin(ph)}))
print(f"      canonical route:  <T_tt> = {sp.simplify(rho_avg)}")
check("canonical route: <T_tt> = h0^2 w^2/(32 pi)   (matches gr-qc/0501041 eq.(5.40) as read)",
      sp.simplify(rho_avg - h0**2 * w**2 / (32 * pi)) == 0)

# independent Isaacson route:  8 pi t_mu_nu = - < G^(2)_mu_nu[h^(1)] >
Gser = G.applyfunc(lambda e: sp.series(sp.simplify(e), eps, 0, 3).removeO().coeff(eps, 2))
hexp = h0 * sp.cos(w * (t - z))
def on_wave(e):
    e = e.subs(hf, hexp).doit()
    e = sp.simplify(e.subs(t, (ph / w) + z))                     # phase phi = w(t-z)
    return sp.simplify(avg(sp.expand(sp.simplify(e))))
G00 = on_wave(Gser[0, 0]); G0z = on_wave(Gser[0, 3]); Gzz = on_wave(Gser[3, 3])
t00, t0z, tzz = -G00 / (8 * pi), -G0z / (8 * pi), -Gzz / (8 * pi)
print(f"      Isaacson route:   t_tt = {sp.simplify(t00)},  t_tz = {sp.simplify(t0z)},  t_zz = {sp.simplify(tzz)}")
check("Isaacson route: t_tt = h0^2 w^2/(32 pi)  (independent of the action route)", sp.simplify(t00 - h0**2 * w**2 / (32 * pi)) == 0)
check("null wave along +z: t_tz = -t_tt and t_zz = t_tt (energy flux = energy density, c = 1)",
      sp.simplify(t0z + t00) == 0 and sp.simplify(tzz - t00) == 0)
check("as a tensor contraction: <hdot_ij hdot_ij>/(32 pi) with h_ij h_ij = 2 h_+^2 gives the same number",
      sp.simplify(avg(2 * (w * h0 * sp.sin(ph))**2) / (32 * pi) - t00) == 0)
# CONTROL: a wrong coefficient (1/16 pi on the tensor contraction) must be rejected
wrong = avg(2 * (w * h0 * sp.sin(ph))**2) / (16 * pi)
check("CONTROL C-A1: coefficient 1/(16 pi) on <hdot_ij hdot_ij> is rejected", sp.simplify(wrong - t00) != 0)
print("      decomposition (script-verified pieces): 1/(32 pi) = (1/2)(1/8 pi)   [Einstein-Hilbert 1/16 pi = (1/2)(1/8 pi)]")
print("                                                          x (1/4)            [second-order expansion of sqrt(-g) R: (1/64pi) = (1/16pi)(1/4)]")
print("                                                          x 2                [energy = kinetic + gradient = 2 x kinetic for a wave]")
check("[bookkeeping] (1/2)(1/4)(2)/(8 pi) = 1/(32 pi)", sp.Rational(1, 2) * sp.Rational(1, 4) * 2 / (8 * pi) == 1 / (32 * pi))
check("[bookkeeping] and per polarisation the same statement reads <hdot_+^2 + hdot_x^2>/(16 pi): the '2' between 16 pi and 32 pi is e_ij e_ij = 2",
      sp.simplify(1 / (16 * pi) * 1 - 2 / (32 * pi)) == 0)

# ============================================================================= B. canonical normalisation kappa^2
print("\nB  canonical graviton normalisation")
kap2 = sp.symbols('kappa2', positive=True)
# L2 (tensor form) = (1/64 pi)(hdot_ij hdot_ij - ...) ; h_ij = kappa hhat_ij ; canonical: (1/2) hhat_dot_ij hhat_dot_ij
sol = sp.solve(sp.Eq(kap2 / (64 * pi), sp.Rational(1, 2)), kap2)[0]
check("tensor convention (Fierz-Pauli, h_mu_nu = kappa hhat, L = (1/2)(d hhat_ij)^2): kappa^2 = 32 pi   [1703.05448 eq.(2.9.11) as read]", sol == 32 * pi)
# per polarisation: L2 = (1/32 pi)(h_+dot)^2 canonical (1/2) phi_dot^2  -> h_+ = kappa_pol phi
sol_pol = sp.solve(sp.Eq(kap2 / (32 * pi), sp.Rational(1, 2)), kap2)[0]
check("per-polarisation convention (h_+ = kappa phi, L = (1/2) phidot^2): kappa^2 = 16 pi", sol_pol == 16 * pi)
check("the two conventions differ by exactly e_ij e_ij = 2", sp.simplify(sol / sol_pol - 2) == 0)
is_canonical = lambda k2: sp.simplify(k2 / (64 * pi) - sp.Rational(1, 2)) == 0     # tensor-canonical test:  kappa^2/(64 pi) = 1/2
check("kappa^2 = 32 pi passes the tensor-canonical test; CONTROL C-B1: kappa^2 = 8 pi and 16 pi are rejected by it",
      is_canonical(32 * pi) and not is_canonical(8 * pi) and not is_canonical(16 * pi))
check("kappa^2 = 32 pi = 8 pi x 4 with 4 = [EH half: 2] x [expansion 1/4 -> 8] x [canonical 1/2] -> (8 pi)(2)(4)(1/2)", 8 * pi * 2 * 4 * sp.Rational(1, 2) == 32 * pi)

# ============================================================================= C. quadrupole formula: the 32 pi cancels
print("\nC  quadrupole radiation: where the 32 pi goes")
nx, ny, nz = sp.symbols('nx ny nz', real=True)
n = sp.Matrix([nx, ny, nz]); Pm = sp.eye(3) - n * n.T
Isym = sp.symbols('I11 I12 I13 I22 I23')
I = sp.Matrix([[Isym[0], Isym[1], Isym[2]], [Isym[1], Isym[3], Isym[4]], [Isym[2], Isym[4], -Isym[0] - Isym[3]]])   # symmetric traceless
def TT_square(I, keep_trace_term=True):
    A = Pm * I * Pm
    tr = (Pm * I).trace()
    return sp.expand((A * A).trace() - (sp.Rational(1, 2) * tr**2 if keep_trace_term else 0))   # I^TT_ij I^TT_ij
def sphere_int(poly):
    poly = sp.Poly(sp.expand(poly), nx, ny, nz); tot = 0
    for (a, b, c), co in poly.terms():
        if a % 2 or b % 2 or c % 2: continue
        tot += co * 2 * sp.gamma(sp.Rational(a + 1, 2)) * sp.gamma(sp.Rational(b + 1, 2)) * sp.gamma(sp.Rational(c + 1, 2)) / sp.gamma(sp.Rational(a + b + c + 3, 2))
    return sp.simplify(tot)
IJ = sp.simplify((I * I).trace())
ang = sphere_int(TT_square(I))
check("int dOmega  Lambda_ij,kl I_ij I_kl = (8 pi/5) I_ij I_ij for any symmetric traceless I (exact, sympy)", sp.simplify(ang - sp.Rational(8, 5) * pi * IJ) == 0)
ang_bad = sphere_int(TT_square(I, keep_trace_term=False))
check("CONTROL C-C1: a projector without the trace term (-1/2 P_ij P_kl) does NOT give 8 pi/5", sp.simplify(ang_bad - sp.Rational(8, 5) * pi * IJ) != 0)
# flux: P = (r^2/32 pi G) int dOmega < hdot^TT_ij hdot^TT_ij >,  h^TT_ij = (2G/r) Lambda I_dd
Gn, r = sp.symbols('G r', positive=True)
Pfac = sp.simplify((r**2 / (32 * pi * Gn)) * (2 * Gn / r)**2 * sp.Rational(8, 5) * pi)
check("P = (G/5) <d3I_ij d3I_ij>: the prefactor (1/32 pi)(4)(8 pi/5) = 1/5 is PI-FREE (the 32 pi cancels against the solid-angle integral)", sp.simplify(Pfac - Gn / 5) == 0)

# circular binary
tt, Ga, Mm, mu, a_, om = sp.symbols('t G M mu a omega', positive=True)
nvec = sp.Matrix([sp.cos(om * tt), sp.sin(om * tt), 0])
Iq = mu * a_**2 * (nvec * nvec.T - sp.eye(3) / 3)
I3 = Iq.applyfunc(lambda e: sp.diff(e, tt, 3))
I3sq = sp.simplify((I3 * I3).trace())
check("d3I_ij d3I_ij = 32 mu^2 a^4 omega^6 for a circular orbit (2 components x (2w)^6 x (1/2)^2 = 32)", sp.simplify(I3sq - 32 * mu**2 * a_**4 * om**6) == 0)
Pq = sp.simplify(Ga / 5 * I3sq)
Pkepler = sp.simplify(Pq.subs(om, sp.sqrt(Ga * Mm / a_**3)))
check("Peters: P = (32/5) G^4 mu^2 M^3 / a^5", sp.simplify(Pkepler - sp.Rational(32, 5) * Ga**4 * mu**2 * Mm**3 / a_**5) == 0)
E = -Ga * Mm * mu / (2 * a_)
adot = sp.simplify(-Pkepler / sp.diff(E, a_))
check("Peters: da/dt = -(64/5) G^3 mu M^2 / a^3", sp.simplify(adot + sp.Rational(64, 5) * Ga**3 * mu * Mm**2 / a_**3) == 0)
ap = sp.symbols('ap', positive=True)
Tc = sp.simplify(sp.integrate((1 / (-adot)).subs(a_, ap), (ap, 0, a_)))
check("coalescence time a^4 (5/256)/(G^3 mu M^2): the 256/5 = 4 x 64/5 (no pi)", sp.simplify(Tc - sp.Rational(5, 256) * a_**4 / (Ga**3 * mu * Mm**2)) == 0)
# chirp: f = omega/pi, fdot
f = sp.symbols('f', positive=True)
Mc = sp.symbols('Mc', positive=True)
omega_a = sp.sqrt(Ga * Mm / a_**3)
omdot = sp.diff(omega_a, a_) * adot
fdot = sp.simplify(omdot / pi)
fdot_f = sp.simplify(fdot.subs(a_, (Ga * Mm / (pi * f)**2)**sp.Rational(1, 3)))
target = sp.Rational(96, 5) * pi**sp.Rational(8, 3) * (Ga * (mu**sp.Rational(3, 5) * Mm**sp.Rational(2, 5)))**sp.Rational(5, 3) * f**sp.Rational(11, 3)
pt = {Ga: 1.3, Mm: 2.1, mu: 0.7, f: 0.31}
pt2 = {Ga: 0.4, Mm: 5.3, mu: 1.9, f: 0.77}
ratio = lambda num, den, p: float((num / den).subs(p).evalf())
check("chirp: fdot = (96/5) pi^(8/3) (G Mc)^(5/3) f^(11/3), Mc = (mu^3 M^2)^(1/5)   [96 = 3 x 32; pi^(8/3) from omega = pi f]  (2 random parameter sets, ratio = 1 to 1e-12)",
      abs(ratio(fdot_f, target, pt) - 1) < 1e-12 and abs(ratio(fdot_f, target, pt2) - 1) < 1e-12)
badtarget = sp.Rational(32, 5) * pi**sp.Rational(8, 3) * (Ga * (mu**sp.Rational(3, 5) * Mm**sp.Rational(2, 5)))**sp.Rational(5, 3) * f**sp.Rational(11, 3)
check("CONTROL C-C2: a wrong chirp coefficient (32/5) is rejected", abs(ratio(fdot_f, badtarget, pt) - 1) > 0.5)

# ============================================================================= D. Larmor
print("\nD  Larmor (Heaviside-Lorentz, c = 1)")
th = sp.symbols('theta', positive=True)
sin2 = sp.integrate(sp.sin(th)**2 * sp.sin(th), (th, 0, pi)) * 2 * pi
check("int sin^2(theta) dOmega = 8 pi/3", sp.simplify(sin2 - 8 * pi / 3) == 0)
q, acc = sp.symbols('q a', positive=True)
PL = sp.simplify((q * acc / (4 * pi))**2 * sin2)
check("Larmor P = q^2 a^2/(6 pi) (HL) [= (2/3) e^2 a^2 in Gaussian]: 6 pi = 16 pi^2/(8 pi/3)", sp.simplify(PL - q**2 * acc**2 / (6 * pi)) == 0 and sp.simplify(16 * pi**2 / (8 * pi / 3) - 6 * pi) == 0)
print("      note: 8 pi/3 here is (4 pi)(2/3) [area x <sin^2>]; in Friedmann 8 pi G/3 = 2 x (4 pi/3) G [2 x ball volume / energy]. Same number, different origin.")
check("8 pi/3 = 4 pi x (2/3) = 2 x (4 pi/3)  (numerically equal, two different origins)", 4 * pi * sp.Rational(2, 3) == 2 * (4 * pi / 3))

# ============================================================================= E. black-hole thermodynamics, Komar, ADM
print("\nE  Kerr / Kerr-Newman thermodynamics, Komar, ADM")
M, aK, Q = sp.symbols('M a Q', positive=True)
rp = M + sp.sqrt(M**2 - aK**2 - Q**2); rm = M - sp.sqrt(M**2 - aK**2 - Q**2)
Aar = 4 * pi * (rp**2 + aK**2); kap = (rp - rm) / (2 * (rp**2 + aK**2)); Om = aK / (rp**2 + aK**2)
KerrA = Aar.subs(Q, 0); Kerrk = kap.subs(Q, 0); KerrO = Om.subs(Q, 0)
check("Kerr area A = 8 pi M r_+  (r_+ = M + sqrt(M^2-a^2))", sp.simplify(KerrA - 8 * pi * M * (M + sp.sqrt(M**2 - aK**2))) == 0)
check("first law dM = (kappa/8pi) dA + Omega dJ, J = aM  (both coefficients of dM and da; sympy)",
      sp.simplify(1 - (Kerrk / (8 * pi) * sp.diff(KerrA, M) + KerrO * aK)) == 0 and sp.simplify(Kerrk / (8 * pi) * sp.diff(KerrA, aK) + KerrO * M) == 0)
check("Smarr M = kappa A/(4 pi) + 2 Omega J", sp.simplify(M - (Kerrk * KerrA / (4 * pi) + 2 * KerrO * aK * M)) == 0)
check("CONTROL C-E1: the wrong first law dM = (kappa/4pi) dA + Omega dJ is rejected", sp.simplify(1 - (Kerrk / (4 * pi) * sp.diff(KerrA, M) + KerrO * aK)) != 0)
check("8 pi in kappa dA/(8 pi) = (2 pi)[Hawking T = kappa/2pi] x (4)[S = A/4]", sp.Integer(1) / (8 * pi) == 1 / (2 * pi) * sp.Rational(1, 4))
Sch = {aK: 0, Q: 0}
check("Schwarzschild: kappa = 1/(4M), A = 16 pi M^2, A kappa^2 = pi, T = 1/(8 pi M)",
      sp.simplify(kap.subs(Sch) - 1 / (4 * M)) == 0 and sp.simplify(Aar.subs(Sch) - 16 * pi * M**2) == 0
      and sp.simplify((Aar * kap**2).subs(Sch) - pi) == 0)
# sharp bound A kappa^2 <= pi over Kerr-Newman
Ak2 = sp.simplify(Aar * kap**2)
check("Kerr-Newman: A kappa^2 = pi (r_+ - r_-)^2/(r_+^2 + a^2)", sp.simplify(Ak2 - pi * (rp - rm)**2 / (rp**2 + aK**2)) == 0)
rng = np.random.default_rng(20260929)
worst = 0.0; hits_eq = 0
for _ in range(200000):
    Mv = 1.0; a2 = rng.random(); Q2 = rng.random() * (1 - a2)          # a^2 + Q^2 <= M^2
    s = np.sqrt(max(1 - a2 - Q2, 0)); rpv, rmv = 1 + s, 1 - s
    val = np.pi * (rpv - rmv)**2 / (rpv**2 + a2)
    worst = max(worst, val / np.pi)
check(f"200000 random Kerr-Newman holes: max A kappa^2/pi = {worst:.6f} <= 1 (sharp bound; algebraic proof: r_-<=r_+ gives (r_+-r_-)^2 <= r_+^2 + a^2)", worst <= 1 + 1e-12)
a2e = 1 - 1e-6; se = np.sqrt(1 - a2e); ext = np.pi * ((1 + se) - (1 - se))**2 / ((1 + se)**2 + a2e)   # near-extremal Kerr
check(f"CONTROL C-E2: the reverse bound 'A kappa^2 >= pi/2 for all holes' is rejected (near-extremal Kerr has A kappa^2/pi = {ext/np.pi:.2e})", ext < np.pi / 2)
# Komar and ADM for Schwarzschild
print("      Komar / ADM normalisations for Schwarzschild")
r_, Mo = sp.symbols('r M', positive=True)
f_ = 1 - 2 * Mo / r_
Komar = sp.simplify(1 / (4 * pi) * (sp.diff(f_, r_) / 2) * 4 * pi * r_**2)
check("Komar M = (1/4 pi) oint (f'/2) dA = M  (1/4pi = 2 x 1/8pi: the two terms of the antisymmetrised surface element)", sp.simplify(Komar - Mo) == 0)
# ADM, isotropic coordinates: g_ij = (1 + M/2r)^4 delta_ij, h_ij = g_ij - delta_ij to first order = (2M/r) delta_ij
hij = 2 * Mo / r_                                            # h_ij = hij * delta_ij (leading order)
# (d_j h_ij - d_i h_jj) n_i with h_jj = 3 hij: d_i(hij) - 3 d_i(hij) = -2 d_r hij
integrand = -2 * sp.diff(hij, r_)
ADM = sp.simplify(1 / (16 * pi) * integrand * 4 * pi * r_**2)
check("ADM M = (1/16 pi) oint (d_j h_ij - d_i h_jj) dS_i = M  (16 pi = 8 pi x 2: linearised G_00 = (1/2)(d d h - lap h))", sp.simplify(ADM - Mo) == 0)
check("CONTROL C-E3: an ADM prefactor 1/(8 pi) gives 2M, not M", sp.simplify(1 / (8 * pi) * integrand * 4 * pi * r_**2 - Mo) != 0)

# ============================================================================= F. horizon-area census
print("\nF  horizon area x Lambda for the horizons that really exist (G = c = 1)")
Lam, rr = sp.symbols('Lambda r', positive=True)
Mn = 1 / (3 * sp.sqrt(Lam)); rN = 1 / sp.sqrt(Lam)
fSdS = 1 - 2 * Mn / rr - Lam * rr**2 / 3
check("Nariai: f(r_N) = 0, f'(r_N) = 0 at r_N = 1/sqrt(Lambda), M_N = 1/(3 sqrt(Lambda))",
      sp.simplify(fSdS.subs(rr, rN)) == 0 and sp.simplify(sp.diff(fSdS, rr).subs(rr, rN)) == 0)
check("Nariai horizon: A Lambda = 4 pi (each of the two horizons)", sp.simplify(4 * pi * rN**2 * Lam - 4 * pi) == 0)
check("de Sitter horizon: A Lambda = 12 pi", sp.simplify(4 * pi * (3 / Lam) * Lam - 12 * pi) == 0)
mx = 0.0; mn = 1e9
for Mv in np.linspace(1e-6, float(1 / (3 * 1.0)) * (1 - 1e-9), 4000):         # Lambda = 1, 0 < M < M_N = 1/3
    roots = np.roots([-1 / 3, 0, 1, -2 * Mv]); rc = max(r_.real for r_ in roots if abs(r_.imag) < 1e-9 and r_.real > 0)
    Ac = 4 * np.pi * rc**2; mx = max(mx, Ac); mn = min(mn, Ac)
check(f"Schwarzschild-de Sitter, 4000 masses 0 < M < M_N: the cosmological-horizon area A_c Lambda stays in [{mn:.3f}, {mx:.3f}] within [4 pi, 12 pi] = [{4*np.pi:.3f}, {12*np.pi:.3f}]: 12 pi is the maximum, 4 pi the Nariai floor",
      mx <= 12 * np.pi + 1e-6 and mn >= 4 * np.pi - 1e-3)
check("the puzzle's Schwarzschild horizon (kappa = a0, Lambda = 32 pi a0^2): A Lambda = 32 pi^2 = (8 pi/3) x 12 pi", sp.simplify(32 * pi**2 - sp.Rational(8, 3) * pi * 12 * pi) == 0)
Mbh = sp.symbols('Mbh', positive=True); rsym = sp.symbols('r_s', positive=True)
rho_bar = sp.simplify(Mbh / (sp.Rational(4, 3) * pi * (2 * Mbh)**3))
check("mean density of a Schwarzschild ball (M inside the sphere of radius r_s = 2M): rho_bar = 3/(32 pi M^2) = 3/(8 pi r_s^2)   [Wikipedia 'Schwarzschild radius' as read]",
      sp.simplify(rho_bar - 3 / (32 * pi * Mbh**2)) == 0 and sp.simplify(rho_bar.subs(Mbh, rsym / 2) - 3 / (8 * pi * rsym**2)) == 0)
Lds = sp.symbols('L', positive=True); rhoL = (3 / Lds**2) / (8 * pi)
check("the de Sitter horizon radius L is exactly the Schwarzschild radius of a ball of density rho_Lambda: rho_bar(r_s = L) = 3/(8 pi L^2) = Lambda/(8 pi) = rho_Lambda",
      sp.simplify(3 / (8 * pi * Lds**2) - rhoL) == 0)
Zf_ = sp.sqrt(32 * pi / 3)
r_puz = Zf_ * Lds / 2
check("the puzzle's horizon r_s = Z L/2 = sqrt(8 pi/3) L has mean density rho_bar = (3/8 pi) rho_Lambda, i.e. rho_Lambda = (8 pi/3) rho_bar(r_s)  (the Friedmann 8 pi/3 again)",
      sp.simplify(r_puz**2 - 8 * pi * Lds**2 / 3) == 0 and sp.simplify(3 / (8 * pi * r_puz**2) / rhoL - 3 / (8 * pi)) == 0)
print("      => the puzzle's a0-horizon has A*Lambda 8 pi/3 = 8.4 times larger than the largest horizon any Lambda-universe can hold (this is p06's no-go, re-read).")

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
