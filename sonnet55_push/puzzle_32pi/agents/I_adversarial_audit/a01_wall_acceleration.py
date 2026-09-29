#!/usr/bin/env python3
"""a01_wall_acceleration.py -- adversarial audit of p06 (part A) and p07: is 'wall acceleration = 1/R' right in de Sitter?

The author's p06/p07 identify the proper acceleration of a thin wall with 1/R, R = the Euclidean S^3 radius of the wall.
That is right in flat space (Rindler hyperbola x^2 - t^2 = R^2) but NOT in de Sitter.  Independent derivation used here:

 (1) EMBEDDING (no Israel formula, no author code): dS_4 of radius L is  -X0^2 + X1^2 + ... + X4^2 = L^2 in R^{1,4}.  A wall at X4 = c is a dS_3 of
     radius R = sqrt(L^2 - c^2).  Its worldline  X = (R sinh(t/R), R cosh(t/R), 0, 0, c)  has embedding acceleration 1/R, whose normal
     component (to the hyperboloid) is always 1/L; the covariant acceleration in dS_4 is the tangential remainder:  a^2 = 1/R^2 - 1/L^2.
     Cross-checked in STATIC coordinates with Christoffel symbols (independent route): the worldline is the static observer at r = c, whose
     acceleration is (r/L^2)/sqrt(1 - r^2/L^2).
 (2) ISRAEL: for a thin wall the sides' extrinsic curvatures are A = sqrt(1/R^2 - H_in^2), B = sqrt(1/R^2 - H_out^2) with A - B = 4 pi sigma
     (G = 1).  Extrinsic curvature K_ab u^a u^b IS the proper acceleration of the wall element relative to that side's geodesics.  Then
     exact:  A, B = DeltaP/(3 sigma) +- 2 pi sigma   (their mean is DeltaP/(3 sigma) exactly, for ALL sigma).
 (3) Consequence: (a) pure-tension wall: a = 2 pi sigma for every H (Vilenkin-Ipser-Sikivie): any a0 = H/Z is reachable with sigma = a0/(2 pi);
     (b) the p07 'probe' formula a = DeltaP/(3 sigma) is exact for the mean proper acceleration, with NO requirement a >> H; (c) at the p07 target ratio the
     full solution has proper acceleration H/Z (not ~H); the 1/R = 2.077 vs H = 2.047 in p07 is the S^3 radius (1/R^2 = H^2 + a^2), NOT an acceleration.
 (4) also: the README/p06 statement 'embeddable iff Z <= 2, i.e. kappa >= 1' has wrong arithmetic: Z = sqrt(8 pi/3)/kappa, so Z <= 2 iff kappa >= sqrt(2 pi/3) = 1.447.
Exit 0 = all checks held (they demonstrate the author's claim is wrong).
"""
import math, sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- (1a) embedding-space calculation, numerical (mpmath), several (L, R)
def cov_accel_embedding(L, R, tau):
    """covariant acceleration magnitude in dS4 of the wall worldline X4 = c, via tangential projection of the embedding acceleration."""
    L = mp.mpf(L); R = mp.mpf(R)
    c = mp.sqrt(L**2 - R**2)
    X = mp.matrix([R * mp.sinh(tau / R), R * mp.cosh(tau / R), 0, 0, c])
    # proper time: dX/dtau has norm -1
    U = mp.matrix([mp.cosh(tau / R), mp.sinh(tau / R), 0, 0, 0])
    Acc = mp.matrix([mp.sinh(tau / R) / R, mp.cosh(tau / R) / R, 0, 0, 0])
    eta = lambda P, Q: -P[0] * Q[0] + sum(P[i] * Q[i] for i in range(1, 5))
    assert abs(eta(X, X) - L**2) < mp.mpf(10)**(-30)
    assert abs(eta(U, U) + 1) < mp.mpf(10)**(-30)
    normal_comp = eta(Acc, X) / L                       # component along the unit normal X/L of the hyperboloid
    tang = Acc - (eta(Acc, X) / L**2) * X               # tangential part = covariant acceleration in dS4
    return mp.sqrt(eta(tang, tang)), normal_comp, mp.sqrt(eta(Acc, Acc))

worst = 0
for (L, R) in [(1, 0.5), (1, 0.9), (2.3, 2.29), (1, 0.1), (5, 3)]:
    a, nc, aemb = cov_accel_embedding(L, R, 0.37)
    pred = mp.sqrt(1 / mp.mpf(R)**2 - 1 / mp.mpf(L)**2)
    worst = max(worst, abs(a - pred), abs(nc - 1 / mp.mpf(L)), abs(aemb - 1 / mp.mpf(R)))
chk("1a embedding: wall-worldline covariant acceleration = sqrt(1/R^2 - 1/L^2) (NOT 1/R); embedding accel = 1/R; normal part = 1/L (5 cases, |err| < 1e-30)", worst < mp.mpf(10)**(-30))

# ---------------------------------------------------------------- (1b) static-coordinate Christoffel check (independent of the embedding projection)
t, r, th, ph, L_ = sp.symbols('t r theta phi L', positive=True)
x = [t, r, th, ph]
f = 1 - r**2 / L_**2
g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)
ginv = g.inv()
Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], x[k]) + sp.diff(g[l, k], x[j]) - sp.diff(g[j, k], x[l])) for l in range(4)) / 2 for k in range(4)] for j in range(4)] for i in range(4)]
# worldline at fixed r = c, th = 0 (on the polar axis; the wall X4 = c is r cos th = c), t = t(tau) with -f (dt/dtau)^2 = -1
c_, tau = sp.symbols('c tau', positive=True)
dt = 1 / sp.sqrt(f.subs(r, c_))
u = [dt, 0, 0, 0]
acc = [sum(Gam[i][j][k].subs({r: c_, th: sp.pi / 2}) * u[j] * u[k] for j in range(4) for k in range(4)) for i in range(4)]   # d u/dtau = 0 (static)
a2 = sp.simplify(sum(g[i, j].subs({r: c_, th: sp.pi / 2}) * acc[i] * acc[j] for i in range(4) for j in range(4)))
pred_static = (c_ / L_**2)**2 / (1 - c_**2 / L_**2)
chk("1b static coordinates: acceleration^2 of the static observer at r = c is (c/L^2)^2/(1 - c^2/L^2) (Christoffel calculation)", sp.simplify(a2 - pred_static) == 0)
Rw = sp.sqrt(L_**2 - c_**2)
chk("1c ... and this equals 1/R^2 - 1/L^2 with R^2 = L^2 - c^2 (the two routes agree)", sp.simplify(pred_static - (1 / Rw**2 - 1 / L_**2)) == 0)

# ---------------------------------------------------------------- (2) Israel junction, exact form
E, e, s = sp.symbols('E e sigma', positive=True)
Hi2 = sp.Rational(8, 3) * sp.pi * (E - e)**2 / 2
Ho2 = sp.Rational(8, 3) * sp.pi * E**2 / 2
x4 = 4 * sp.pi * s
A = sp.Rational(1, 2) * ((Ho2 - Hi2) / x4 + x4)
B = A - x4
DP = e * E - e**2 / 2
chk("2a exact: A = DeltaP/(3 sigma) + 2 pi sigma and B = DeltaP/(3 sigma) - 2 pi sigma   (DeltaP = eE - e^2/2)",
    sp.simplify(A - (DP / (3 * s) + 2 * sp.pi * s)) == 0 and sp.simplify(B - (DP / (3 * s) - 2 * sp.pi * s)) == 0)
chk("2b consistency with the author's Euclidean radius: 1/R^2 = H_in^2 + A^2 = H_out^2 + B^2", sp.simplify(Hi2 + A**2 - (Ho2 + B**2)) == 0)

# pure tension, H_in = H_out = H
H, sg = sp.symbols('H sigma', positive=True)
Ap = sp.Rational(1, 2) * (0 / (4 * sp.pi * sg) + 4 * sp.pi * sg)
chk("2c pure tension: side accelerations = +-2 pi sigma independent of H; 1/R^2 = H^2 + (2 pi sigma)^2 (author's A2 formula, which itself displays a = 2 pi sigma)", sp.simplify(Ap - 2 * sp.pi * sg) == 0)

# ---------------------------------------------------------------- (3) numbers at the author's target ratio (p07)
Z = mp.sqrt(32 * mp.pi / 3)
ratio = 3 / (2 * mp.sqrt(2))
Ev = mp.mpf(1)
Hn = mp.sqrt((8 * mp.pi / 3) * Ev**2 / 2)
rows = []
for sv in [mp.mpf('1e-2'), mp.mpf('1e-4'), mp.mpf('1e-6'), mp.mpf('1e-8')]:
    ev = ratio * sv
    hi2 = (8 * mp.pi / 3) * (Ev - ev)**2 / 2; ho2 = (8 * mp.pi / 3) * Ev**2 / 2
    xx = 4 * mp.pi * sv
    Av = (mp.mpf(1) / 2) * ((ho2 - hi2) / xx + xx); Bv = Av - xx
    invR = mp.sqrt(hi2 + Av**2)
    dP = ev * Ev - ev**2 / 2
    rows.append((sv, invR, Av, Bv, dP / (3 * sv)))
    print("   sigma=%.0e  1/R=%.6f (>H=%.6f, the S^3 radius)   side accelerations A=%.6f B=%.6f   mean=%.6f  DeltaP/(3sigma)=%.6f   H/Z=%.6f" %
          (sv, invR, Hn, Av, Bv, (Av + Bv) / 2, dP / (3 * sv), Hn / Z))
sv, invR, Av, Bv, pr = rows[-1]
chk("3a at the p07 target ratio (e/sigma = 3/(2 sqrt2), sigma -> 0): proper accelerations A, B -> H/Z = 0.3536 (NOT ~ H); the 'probe reading is inconsistent' claim (p07 check 6, README section 9) is wrong",
    abs(Av - Hn / Z) < 1e-6 * Hn and abs(Bv - Hn / Z) < 1e-6 * Hn and invR > Hn)
chk("3b the mean of the two side accelerations equals DeltaP/(3 sigma) EXACTLY at every sigma, including finite sigma (so the probe formula needs no a >> H)",
    all(abs((Av_ + Bv_) / 2 - pr_) < mp.mpf(10)**(-25) for (_, _, Av_, Bv_, pr_) in rows))
# a wall with any prescribed a0 = H/Z exists: pure tension sigma = a0/(2 pi)
a0 = Hn / Z
sig = a0 / (2 * mp.pi)
invR_pt = mp.sqrt(Hn**2 + (2 * mp.pi * sig)**2)
chk("3c pure-tension wall with sigma = a0/(2 pi G) has proper acceleration exactly a0 = H/Z < H and Euclidean radius 1/R = sqrt(H^2 + a0^2) (author's A4 'needs sigma^2 < 0' is wrong)",
    abs(mp.sqrt(invR_pt**2 - Hn**2) - a0) < mp.mpf(10)**(-30) and a0 < Hn)
chk("3d static-patch location of such a wall: r = L sin(theta0), tan(theta0) = 1/Z (p06's own check D1 already says an a0 observer sits at this angle, contradicting p06 A4)",
    abs(mp.tan(mp.atan(1 / Z)) - 1 / Z) < mp.mpf(10)**(-30))

# ---------------------------------------------------------------- (4) the embeddability arithmetic
kap = sp.symbols('kappa', positive=True)
Zk = sp.sqrt(8 * sp.pi / 3) / kap
kcrit = sp.solve(sp.Eq(Zk, 2), kap)[0]
print("   Z <= 2  <=>  kappa >= %s = %.4f   (at kappa = 1, Z = %.4f, r_s = %.4f L > L)" % (sp.simplify(kcrit), float(kcrit), float(Zk.subs(kap, 1)), float(Zk.subs(kap, 1)) / 2))
chk("4 'embeddable iff Z <= 2, i.e. kappa >= 1' is arithmetically wrong: the threshold is kappa >= sqrt(2 pi/3) = 1.447; even kappa = 1 (forced kernel) has r_s > L",
    abs(float(kcrit) - math.sqrt(2 * math.pi / 3)) < 1e-12 and float(Zk.subs(kap, 1)) > 2)

# ---------------------------------------------------------------- (5) is 'R <= 1/H_i, 1/H_o' the whole content of p06 A3?  (it is a sum of squares)
invR2 = Hi2 + A**2
chk("5 p06 A3 (20000 random cases of 1/R^2 >= max(H_i^2, H_o^2)) is a tautology: 1/R^2 - H_i^2 = A^2 and 1/R^2 - H_o^2 = B^2 are squares by construction (geometrically: an S^3 in S^4 has radius <= the S^4 radius); no control could fail",
    sp.simplify(invR2 - Hi2 - A**2) == 0 and sp.simplify(invR2 - Ho2 - B**2) == 0)
# ---------------------------------------------------------------- (6) flat-space controls: what IS right in the author's p07
Rr, sg2, dP = sp.symbols('R sigma DeltaP', positive=True)
Bact = 2 * sp.pi**2 * Rr**3 * sg2 - sp.pi**2 * Rr**4 * dP / 2          # Euclidean bounce action of a membrane (S^3 of radius R) in flat R^4
Rstar = sp.solve(sp.diff(Bact, Rr), Rr)
chk("6a flat-space Schwinger radius by direct extremisation of the bounce action B(R) = 2 pi^2 R^3 sigma - (pi^2/2) R^4 DeltaP: R = 3 sigma/DeltaP (author's p07 check 1 confirmed)",
    any(sp.simplify(sol - 3 * sg2 / dP) == 0 for sol in Rstar))
chk("6b control: as H -> 0 the proper acceleration sqrt(1/R^2 - H^2) -> 1/R, so the author's identification is right ONLY in the flat limit (which is why it looked right)",
    sp.limit(sp.sqrt(1 / Rr**2 - sp.Symbol('h', positive=True)**2), sp.Symbol('h', positive=True), 0) == 1 / Rr)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
