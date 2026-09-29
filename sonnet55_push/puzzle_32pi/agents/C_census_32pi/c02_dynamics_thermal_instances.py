#!/usr/bin/env python3
"""c02_dynamics_thermal_instances.py -- census lane C: instances where 32 pi (or its neighbours) sits in a DYNAMICAL or THERMAL coefficient.

  D1  Friedmann coefficient 8 pi/3 from Einstein's G_tt (sympy, FRW) and from Newton (energy of a shell)
  D2  free-fall time  t_ff = sqrt(3 pi/(32 G rho)) from the integral (sympy exact + mpmath quadrature), its decomposition, and the
      identity Z sqrt(G rho) t_ff = pi (a tautology, flagged as such)
  D3  Jeans: dispersion relation omega^2 = c_s^2 k^2 - 4 pi G rho, lambda_J = sqrt(pi c_s^2/(G rho))  (4 pi, not 32 pi)
  D4  Stefan-Boltzmann pi^2/60 from  int x^3/(e^x-1) = pi^4/15;  Hawking photon-only power 1/(15360 pi G^2 M^2), lifetime 5120 pi G^2 M^3
      (the 15360 pi and 5120 pi contain 32 pi only as 32 x 480 and 32 x 160: numerology, see the census) and the decomposition into
      (8 pi)^4/(pi^2 x 16 pi) x 60
  D5  Casimir  -pi^2/(720 d^3) by dimensional regularisation + zeta(-3) = 1/120
  D6  Euler-Heisenberg  e^4/(360 pi^2 m^4)  and the Schwinger rate  (eE)^2/(4 pi^3) exp(-pi m^2/eE)  from the proper-time integral
Controls (each MUST be caught): wrong free-fall coefficient, Jeans without the 4 pi, wrong sigma, wrong lifetime, wrong Casimir zeta value,
wrong Schwinger prefactor.
Exit 0 = every check and every control behaves.
"""
import sys
import mpmath as mp
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

pi = sp.pi
G, rho, R, Mm, r = sp.symbols('G rho R M r', positive=True)

# ----------------------------------------------------------------------------- D1 Friedmann
print("\nD1  the Friedmann coefficient 8 pi/3")
t, x, y, z = sp.symbols('t x y z', real=True)
a = sp.Function('a', positive=True)(t)
gF = sp.diag(-1, a**2, a**2, a**2); X = [t, x, y, z]
def christoffel(g, X):
    n = len(X); gi = g.inv()
    return [[[sp.simplify(sum(gi[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(n)) / 2)
              for k in range(n)] for j in range(n)] for i in range(n)]
def ricci(g, X):
    n = len(X); Gm = christoffel(g, X); Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(n):
            e = 0
            for i in range(n):
                e += sp.diff(Gm[i][j][k], X[i]) - sp.diff(Gm[i][j][i], X[k])
                for l in range(n):
                    e += Gm[i][i][l] * Gm[l][j][k] - Gm[i][k][l] * Gm[l][j][i]
            Ric[j, k] = e
    return Ric
RicF = ricci(gF, X); RF = sum(gF.inv()[i, i] * RicF[i, i] for i in range(4)); Gtt = sp.simplify(RicF[0, 0] - gF[0, 0] * RF / 2)
H = sp.diff(a, t) / a
check("Einstein tensor of flat FRW: G_tt = 3 H^2  (so 8 pi G rho = 3 H^2: H^2 = (8 pi/3) G rho; the 3 = dim SO(3))", sp.simplify(Gtt - 3 * H**2) == 0)
# Newton: shell of radius r, mass M = (4 pi/3) rho r^3, zero energy: (1/2) rdot^2 = G M/r
Hn2 = sp.simplify(2 * G * (4 * pi / 3 * rho * r**3) / r**3)
check("Newtonian zero-energy shell: H^2 = 2 G M/r^3 = (8 pi/3) G rho = 2 x (4 pi/3) G rho", sp.simplify(Hn2 - 8 * pi * G * rho / 3) == 0)

# ----------------------------------------------------------------------------- D2 free-fall
print("\nD2  free-fall time")
u = sp.symbols('u', positive=True)
Msym = sp.Rational(4, 3) * pi * rho * R**3
# r = R sin^2 u : dr = 2 R sin u cos u du ;  1/r - 1/R = cos^2 u /(R sin^2 u)
integrand = sp.simplify((2 * R * sp.sin(u) * sp.cos(u)) / sp.sqrt(2 * G * Msym * sp.cos(u)**2 / (R * sp.sin(u)**2)))
tff = sp.simplify(sp.integrate(integrand, (u, 0, pi / 2)))
check("t_ff = (pi/2) sqrt(R^3/(2 G M)) = sqrt(3 pi/(32 G rho))   (exact, substitution r = R sin^2 u)", sp.simplify(tff**2 - 3 * pi / (32 * G * rho)) == 0)
# independent numerical quadrature of int_0^R dr / sqrt(2GM(1/r - 1/R)) with G = 1, rho = 1
mp.mp.dps = 30
Mnum = mp.mpf(4) / 3 * mp.pi * 1 * 1**3
qq = mp.quad(lambda rr: 1 / mp.sqrt(2 * Mnum * (1 / rr - 1)), [0, 0.5, 1])
check("independent mpmath quadrature (G = rho = R = 1): t_ff = %s vs sqrt(3 pi/32) = %s" % (mp.nstr(qq, 12), mp.nstr(mp.sqrt(3 * mp.pi / 32), 12)),
      abs(qq - mp.sqrt(3 * mp.pi / 32)) < mp.mpf('1e-10'))
check("CONTROL C-D2a: sqrt(3 pi/(16 G rho)) (wrong) is rejected", abs(qq - mp.sqrt(3 * mp.pi / 16)) > 0.05)
print(f"      t_ff sqrt(G rho) = sqrt(3 pi/32) = {float(sp.sqrt(3 * pi / 32)):.6f}")
# decomposition: t_ff^2 G rho = (pi/2)^2 * 3/(8 pi)
check("[bookkeeping] G rho t_ff^2 = 3 pi/32 = (pi/2)^2 x 3/(8 pi): an ANGLE integral pi/2 squared times the Friedmann/Gauss factor 3/(8 pi)",
      sp.simplify((pi / 2)**2 * 3 / (8 * pi) - 3 * pi / 32) == 0)
check("t_ff = (pi/2)/H_rho with H_rho^2 = (8 pi/3) G rho: the 32 pi is 8 pi x 4 with 4 = (2/pi)^2 pi^2 -> the pi count is +1 in the numerator (3 pi/32), NOT 32 pi in the numerator",
      sp.simplify(tff - (pi / 2) / sp.sqrt(8 * pi * G * rho / 3)) == 0)
Zc = sp.sqrt(32 * pi / 3)
check("[tautology, flagged] Z sqrt(G rho) t_ff = pi  (i.e. (32 pi/3)(3 pi/32) = pi^2): it only says Z = 2 sqrt(8 pi/3) and t_ff = (pi/2)/sqrt(8 pi G rho/3)",
      sp.simplify(Zc * sp.sqrt(G * rho) * tff - pi) == 0)

# ----------------------------------------------------------------------------- D3 Jeans
print("\nD3  Jeans instability")
w, k, cs, rho0, dr_, dv_, dPhi = sp.symbols('omega k c_s rho0 drho dv dPhi')
# continuity, Euler (pressure via c_s^2), Poisson, plane waves exp(i(kx - wt))
eqs = [-sp.I * w * dr_ + sp.I * rho0 * k * dv_,
       -sp.I * w * dv_ + sp.I * k * cs**2 * dr_ / rho0 + sp.I * k * dPhi,
       -k**2 * dPhi - 4 * pi * G * dr_]
Mmat = sp.Matrix([[sp.diff(e, s) for s in (dr_, dv_, dPhi)] for e in eqs])
disp = sp.solve(sp.Eq(sp.simplify(Mmat.det()), 0), w**2)
check("dispersion relation  omega^2 = c_s^2 k^2 - 4 pi G rho0", len(disp) == 1 and sp.simplify(disp[0] - (cs**2 * k**2 - 4 * pi * G * rho0)) == 0)
kJ = sp.sqrt(4 * pi * G * rho0) / cs
lamJ = sp.simplify(2 * pi / kJ)
check("lambda_J = 2 pi/k_J = sqrt(pi c_s^2/(G rho)) : the coefficient is 4 pi (Poisson), no 32", sp.simplify(lamJ**2 - pi * cs**2 / (G * rho0)) == 0)
badk = sp.sqrt(G * rho0) / cs
check("CONTROL C-D3a: dropping the 4 pi (Poisson) gives k_J = sqrt(G rho)/c_s and is rejected", sp.simplify((cs**2 * badk**2 - 4 * pi * G * rho0)) != 0)

# ----------------------------------------------------------------------------- D4 Stefan-Boltzmann and Hawking
print("\nD4  Stefan-Boltzmann and Hawking evaporation (photons only, geometric cross section)")
xx = sp.symbols('x', positive=True)
I3 = sp.gamma(4) * sp.zeta(4)                                    # int_0^oo x^(s-1)/(e^x-1) dx = Gamma(s) zeta(s)
qI3 = mp.quad(lambda tt_: tt_**3 / (mp.e**tt_ - 1), [0, mp.inf])
check("int_0^oo x^3/(e^x - 1) dx = Gamma(4) zeta(4) = pi^4/15  (closed form and independent mpmath quadrature %s)" % mp.nstr(qI3, 12),
      sp.simplify(I3 - pi**4 / 15) == 0 and abs(qI3 - mp.pi**4 / 15) < mp.mpf('1e-15'))
Tt = sp.symbols('T', positive=True)
u_energy = 2 * 4 * pi / (2 * pi)**3 * Tt**4 * I3                # 2 polarisations, d^3k = 4 pi k^2 dk, hbar = c = k_B = 1
check("photon energy density u = (pi^2/15) T^4", sp.simplify(u_energy - pi**2 * Tt**4 / 15) == 0)
sigma = sp.simplify(u_energy / 4 / Tt**4)
check("sigma = u/(4 T^4) = pi^2/60", sp.simplify(sigma - pi**2 / 60) == 0)
Mh = sp.symbols('M', positive=True)
TH = 1 / (8 * pi * G * Mh); AH = 16 * pi * G**2 * Mh**2
P_H = sp.simplify(sigma * AH * TH**4)
check("P = sigma A T^4 = 1/(15360 pi G^2 M^2)", sp.simplify(P_H - 1 / (15360 * pi * G**2 * Mh**2)) == 0)
# lifetime: dM/dt = -P
Ms = sp.symbols('Ms', positive=True)
life = sp.integrate(-1 / P_H.subs(Mh, Ms), (Ms, Mh, 0))
check("evaporation time t = 5120 pi G^2 M^3", sp.simplify(life - 5120 * pi * G**2 * Mh**3) == 0)
check("CONTROL C-D4a: sigma = pi^2/30 (wrong) gives lifetime 2560 pi and is rejected",
      sp.simplify(sp.integrate(-1 / (sp.simplify((pi**2 / 30) * AH * TH**4)).subs(Mh, Ms), (Ms, Mh, 0)) - 5120 * pi * G**2 * Mh**3) != 0)
check("[bookkeeping] 15360 pi = 60 (8 pi)^4/((pi^2)(16 pi)):  60 = 4 x 15 from sigma=pi^2/60;  (8 pi)^4 from T^4;  pi^2 from sigma;  16 pi from A",
      sp.simplify(60 * (8 * pi)**4 / (pi**2 * 16 * pi) - 15360 * pi) == 0)
check("[numerology flag] 15360 pi = 32 pi x 480 and 5120 pi = 32 pi x 160 (a literal factor, not an origin; 15360 = 2^10 x 15, 5120 = 2^10 x 5)",
      15360 == 32 * 480 and 5120 == 32 * 160 and 15360 == 2**10 * 15 and 5120 == 2**10 * 5)
print("      caveat: the coefficient is model-dependent (species content, greybody factors); it is not a fundamental constant of gravity.")

# ----------------------------------------------------------------------------- D5 Casimir
print("\nD5  Casimir energy by dimensional regularisation")
D, m = sp.symbols('D m', positive=True)
Ireg = sp.gamma(-sp.Rational(1, 2) - D / 2) / ((4 * pi)**(D / 2) * sp.gamma(-sp.Rational(1, 2))) * m**(D + 1)   # int d^Dk/(2pi)^D sqrt(k^2+m^2)
I2 = sp.simplify(Ireg.subs(D, 2))
check("int d^2k/(2 pi)^2 sqrt(k^2+m^2) -> -m^3/(6 pi) (dim. reg.)", sp.simplify(I2 + m**3 / (6 * pi)) == 0)
dsep = sp.symbols('d', positive=True)
zeta3 = sp.zeta(-3)
check("zeta(-3) = 1/120", zeta3 == sp.Rational(1, 120) and abs(mp.zeta(-3) - mp.mpf(1) / 120) < 1e-20)
EA = sp.simplify(-(1 / (6 * pi)) * (pi / dsep)**3 * zeta3)     # sum_n (n pi/d)^3 = (pi/d)^3 zeta(-3); (1/2)(2 pol) = 1
check("E/A = -pi^2/(720 d^3)", sp.simplify(EA + pi**2 / (720 * dsep**3)) == 0)
check("force per area -dE/dd = -pi^2/(240 d^4)", sp.simplify(-sp.diff(EA, dsep) + pi**2 / (240 * dsep**4)) == 0)
check("CONTROL C-D5a: with zeta(-3) replaced by 1/12 the result -pi^2/(72 d^3) is rejected", sp.simplify(-(1 / (6 * pi)) * (pi / dsep)**3 * sp.Rational(1, 12) + pi**2 / (720 * dsep**3)) != 0)

# ----------------------------------------------------------------------------- D6 Euler-Heisenberg and Schwinger
print("\nD6  Euler-Heisenberg and Schwinger from the proper-time integral")
e, s, E, mm = sp.symbols('e s E m', positive=True)
xs = e * E * s
# weak-field: x cot x = 1 - x^2/3 - x^4/45 - ...
ser = sp.series(xs * sp.cot(xs), s, 0, 6).removeO()
check("x cot x = 1 - x^2/3 - x^4/45 + O(x^6)", sp.simplify(ser - (1 - xs**2 / 3 - xs**4 / 45)) == 0)
L4 = sp.simplify(-(1 / (8 * pi**2)) * sp.integrate(sp.expand(-(e * E)**4 * s**4 / 45 / s**3) * sp.exp(-mm**2 * s), (s, 0, sp.oo)))
check("L_(4) = e^4 E^4/(360 pi^2 m^4)   [hep-th/0406216 eq.(1.9) as read: e^4/(360 pi^2 m^4) (E^2-B^2)^2 + ...]", sp.simplify(L4 - e**4 * E**4 / (360 * pi**2 * mm**4)) == 0)
check("[bookkeeping] 360 pi^2 = 8 pi^2 x 45 (the proper-time loop 1/(8 pi^2) x the x^4 coefficient 1/45)", 360 * pi**2 == 8 * pi**2 * 45)
# Schwinger: residue of e^{-m^2 s} (eEs) cot(eEs)/s^3 at s_n = n pi/(eE)
resid = []
for nn in (1, 2, 3):
    sn = nn * pi / (e * E)
    f = sp.exp(-mm**2 * s) * (e * E * s) * sp.cot(e * E * s) / s**3
    rz = sp.simplify(sp.limit((s - sn) * f, s, sn))
    resid.append(sp.simplify(rz - (e * E)**2 / (nn**2 * pi**2) * sp.exp(-nn * pi * mm**2 / (e * E))) == 0)
check("residues at s_n = n pi/(eE):  (eE)^2/(n^2 pi^2) exp(-n pi m^2/eE)  (n = 1, 2, 3)", all(resid))
# Gamma = 2 Im L ; |Im L| = (1/8 pi^2) * pi * sum Res
n1 = sp.symbols('n', positive=True, integer=True)
Gam_n = 2 * (1 / (8 * pi**2)) * pi * (e * E)**2 / (n1**2 * pi**2)          # prefactor of exp(-n pi m^2/eE)/n^2 -> (eE)^2/(4 pi^3)
check("Gamma = 2 Im L = (eE)^2/(4 pi^3) sum_n exp(-n pi m^2/eE)/n^2   [hep-th/0406216 eq.(1.10),(1.11) as read; Wikipedia 'Schwinger effect']",
      sp.simplify(Gam_n * n1**2 - (e * E)**2 / (4 * pi**3)) == 0)
check("CONTROL C-D6a: prefactor (eE)^2/(8 pi^3) (forgetting Gamma = 2 Im L) is rejected", sp.simplify(Gam_n * n1**2 - (e * E)**2 / (8 * pi**3)) != 0)
check("[bookkeeping] Gamma prefactor = 2 x [1/(8 pi^2)] x [pi from the half residue] x [1/pi^2 from s_n^2]", sp.simplify(2 / (8 * pi**2) * pi / pi**2 - 1 / (4 * pi**3)) == 0)
print("      the exponent pi m^2/(eE) is a semicircle area (WKB action): a scale (the Schwinger field m^2/e) enters, and the ratio eE/m is an ACCELERATION")
print("      a = eE/m (a coupling ratio e/m times the field): this is the closest textbook 'acceleration set by sqrt(rho)' (rho = E^2/2), with e/m free.")

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
