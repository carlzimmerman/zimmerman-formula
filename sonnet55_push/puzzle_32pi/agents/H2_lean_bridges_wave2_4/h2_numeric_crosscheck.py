"""Independent numerical / symbolic cross-check (mpmath, sympy, numpy) of the NUMBERS and FORMULAS that the Lean certificates of this directory prove exactly.
Purpose: guard against a mis-stated Lean statement (Lean checks the proof, not that the statement is the physical one) -- in particular the surface-gravity formula of P2,
the BH-normalisation bounds of P2, the wall accelerations of P1, the D-dimensional Friedmann coefficients of P6 (recomputed here from the metric with sympy) and the offset
integrals of P7.  Each check has a control (a wrong constant / a wrong formula) that must FAIL.  Exit 0 iff every check passes and every control fails."""
import sys
import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 30
ok = []


def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)


def ctrl(name, cond_that_must_be_false):
    good = not bool(cond_that_must_be_false); ok.append(good); print(("PASS " if good else "FAIL ") + "control: " + name)


pi = mp.pi
Zp = mp.sqrt(32 * pi / 3)                 # the puzzle Z

# =====================================================================================================================================
# P1: walls in de Sitter
# =====================================================================================================================================
def eta(P, Q):
    return -P[0] * Q[0] + P[1] * Q[1] + P[2] * Q[2] + P[3] * Q[3] + P[4] * Q[4]


def wall_covariant_acc_sq(Lv, Rv, tau0):
    """differentiate the embedding worldline numerically, project tangentially to the hyperboloid, return (eta T T, eta U U, eta A A)"""
    cv = mp.sqrt(Lv ** 2 - Rv ** 2)
    X = lambda t: [Rv * mp.sinh(t / Rv), Rv * mp.cosh(t / Rv), 0, 0, cv]
    U = [mp.diff(lambda t: X(t)[i], tau0) for i in range(5)]
    A = [mp.diff(lambda t: X(t)[i], tau0, 2) for i in range(5)]
    x0 = X(tau0)
    k = eta(A, x0) / Lv ** 2
    T = [A[i] - k * x0[i] for i in range(5)]
    return eta(T, T), eta(U, U), eta(A, A)


worst = 0
for (Lv, Rv) in [(1, 0.5), (1, 0.9), (2.3, 2.29), (5, 3)]:
    Lv = mp.mpf(Lv); Rv = mp.mpf(Rv)
    tt, uu, aa = wall_covariant_acc_sq(Lv, Rv, mp.mpf('0.37'))
    worst = max(worst, abs(tt - (1 / Rv ** 2 - 1 / Lv ** 2)), abs(uu + 1), abs(aa - 1 / Rv ** 2))
chk("P1 wall worldline (numerical derivatives): eta U U = -1, eta A A = 1/R^2, tangential acceleration^2 = 1/R^2 - 1/L^2 (4 cases, err %.1e)" % worst, worst < 1e-15)
tt, uu, aa = wall_covariant_acc_sq(mp.mpf(1), mp.mpf('0.5'), mp.mpf('0.37'))
ctrl("acceleration^2 = 1/R^2 (the p06 identification) is false for a wall in dS", abs(tt - 1 / mp.mpf('0.5') ** 2) < 1e-6)

# static coordinates: Christoffel symbols in the static patch of dS (sympy), observer at r = c
t_, r_, th_, ph_, Ls, cs = sp.symbols('t r theta phi L c', positive=True)
xs = [t_, r_, th_, ph_]
f_ = 1 - r_ ** 2 / Ls ** 2
gm = sp.diag(-f_, 1 / f_, r_ ** 2, r_ ** 2 * sp.sin(th_) ** 2)
gmi = gm.inv()
Gam = [[[sum(gmi[i, l] * (sp.diff(gm[l, j], xs[k]) + sp.diff(gm[l, k], xs[j]) - sp.diff(gm[j, k], xs[l])) for l in range(4)) / 2 for k in range(4)] for j in range(4)] for i in range(4)]
ut = 1 / sp.sqrt(f_.subs(r_, cs))
accv = [sum(Gam[i][j][k].subs({r_: cs, th_: sp.pi / 2}) * ([ut, 0, 0, 0][j]) * ([ut, 0, 0, 0][k]) for j in range(4) for k in range(4)) for i in range(4)]
a2s = sp.simplify(sum(gm[i, j].subs({r_: cs, th_: sp.pi / 2}) * accv[i] * accv[j] for i in range(4) for j in range(4)))
chk("P1 static observer at r = c: acceleration^2 = (c/L^2)^2/(1 - c^2/L^2) (Christoffel symbols)", sp.simplify(a2s - (cs / Ls ** 2) ** 2 / (1 - cs ** 2 / Ls ** 2)) == 0)
Rw = sp.sqrt(Ls ** 2 - cs ** 2)
chk("P1 ... equals 1/R^2 - 1/L^2 with R^2 = L^2 - c^2", sp.simplify((cs / Ls ** 2) ** 2 / (1 - cs ** 2 / Ls ** 2) - (1 / Rw ** 2 - 1 / Ls ** 2)) == 0)

# Israel junction solved numerically (independent of the closed form)
rng = np.random.default_rng(20260929)
worst = 0; worstB = 0
for _ in range(20):
    E = mp.mpf(rng.uniform(0.5, 2)); e = mp.mpf(rng.uniform(0.05, 0.9)) * E; s = mp.mpf(rng.uniform(0.01, 0.5))
    Hi2 = 8 * pi / 3 * (E - e) ** 2 / 2; Ho2 = 8 * pi / 3 * E ** 2 / 2
    sol = mp.findroot(lambda A, B: [A - B - 4 * pi * s, A ** 2 - B ** 2 - (Ho2 - Hi2)], (mp.mpf(1), mp.mpf(0.5)))
    A, B = sol[0], sol[1]
    dP = e * E - e ** 2 / 2
    worst = max(worst, abs(A - (dP / (3 * s) + 2 * pi * s)), abs(B - (dP / (3 * s) - 2 * pi * s)))
    worstB = max(worstB, abs((A + B) / 2 - dP / (3 * s)), abs((Hi2 + A ** 2) - (Ho2 + B ** 2)))
chk("P1 Israel: numerically solved (A, B) = DeltaP/(3 sigma) +- 2 pi sigma (20 random cases, err %.1e)" % worst, worst < 1e-15)
chk("P1 mean of the two sides = DeltaP/(3 sigma) and 1/R^2 = H_in^2 + A^2 = H_out^2 + B^2 (err %.1e)" % worstB, worstB < 1e-15)
ctrl("A = DeltaP/(3 sigma) + pi sigma is false", worst < 1e-15 and abs(A - (dP / (3 * s) + pi * s)) < 1e-6)
Hn = mp.sqrt(4 * pi / 3)      # H_out for E = 1
chk("P1 probe target: r = 3/(2 sqrt2) gives r E/3 = H_out/Z (E = 1)", abs(3 / (2 * mp.sqrt(2)) / 3 - Hn / Zp) < 1e-25)
ctrl("r = 3/2 does not give r E/3 = H_out/Z", abs(mp.mpf(3) / 2 / 3 - Hn / Zp) < 1e-3)

# =====================================================================================================================================
# P2: Schwarzschild-de Sitter surface gravity
# =====================================================================================================================================
worst = 0
for (Mv, Lv) in [(0.1, 1.0), (0.15, 1.0), (0.05, 2.0), (0.3, 3.0)]:
    Mv = mp.mpf(Mv); Lv = mp.mpf(Lv)
    roots = sorted([mp.re(z) for z in mp.polyroots([1, 0, -Lv ** 2, 2 * Mv * Lv ** 2], maxsteps=200, extraprec=100) if mp.re(z) > 0])
    rb, rc = roots
    for rr, sgn in [(rb, 1), (rc, -1)]:
        fp = mp.diff(lambda r: 1 - 2 * Mv / r - r ** 2 / Lv ** 2, rr)
        kap = sgn * fp / 2
        pred = sgn * (1 - 3 * rr ** 2 / Lv ** 2) / (2 * rr)
        worst = max(worst, abs(kap - pred))
chk("P2 kappa = f'/2 = (1 - 3 r^2/L^2)/(2 r) at both horizons of SdS (numerical derivative, err %.1e)" % worst, worst < 1e-20)
Mv = mp.mpf('0.15'); Lv = mp.mpf(1)
rb = sorted([mp.re(z) for z in mp.polyroots([1, 0, -1, 2 * Mv], maxsteps=200, extraprec=100) if mp.re(z) > 0])[0]
kapb = mp.diff(lambda r: 1 - 2 * Mv / r - r ** 2, rb) / 2
ctrl("kappa_b = (1 - r^2/L^2)/(2r) (the naive formula) is false", abs(kapb - (1 - rb ** 2) / (2 * rb)) < 1e-6)
xb = (mp.sqrt(1 + 3 * Zp ** 2) - 1) / (3 * Zp)
chk("P2 root x_b = (sqrt(1 + 3Z^2) - 1)/(3Z) = %s solves kappa_b L = 1/Z" % mp.nstr(xb, 8), abs((1 - 3 * xb ** 2) / (2 * xb) - 1 / Zp) < 1e-25 and abs(xb - mp.mpf('0.522632')) < 1e-6)
xn = -1 / Zp + mp.sqrt(1 + 1 / Zp ** 2)
ctrl("the brief's root -1/Z + sqrt(1 + 1/Z^2) does NOT solve kappa_b L = 1/Z", abs((1 - 3 * xn ** 2) / (2 * xn) - 1 / Zp) < 1e-6)
chk("P2 ... it solves the naive equation (1 - x^2)/(2x) = 1/Z instead", abs((1 - xn ** 2) / (2 * xn) - 1 / Zp) < 1e-25)
xc = (1 + mp.sqrt(1 + 3 * Zp ** 2)) / (3 * Zp)
chk("P2 cosmological root x_c = %s solves kappa_c L = 1/Z, x_c < 1 (Z > 1)" % mp.nstr(xc, 8), abs((3 * xc ** 2 - 1) / (2 * xc) - 1 / Zp) < 1e-25 and xc < 1)
Mstar = xb * (1 - xb ** 2) / 2; MN = 1 / (3 * mp.sqrt(3))
chk("P2 M*/M_Nariai = %s (audit 0.98695), area x Lambda = 12 pi x_b^2 = %s (audit 10.3)" % (mp.nstr(Mstar / MN, 7), mp.nstr(12 * pi * xb ** 2, 6)),
    abs(Mstar / MN - mp.mpf('0.98695')) < 1e-5 and abs(12 * pi * xb ** 2 - mp.mpf('10.3')) < 0.05)
# BH normalisation scan
def bh_scan(fr):
    Mv = MN * fr
    roots = sorted([mp.re(z) for z in mp.polyroots([1, 0, -1, 2 * Mv], maxsteps=200, extraprec=100) if mp.re(z) > 0])
    rb, rc = roots
    s = Mv ** (mp.mpf(1) / 3); D = 1 - 3 * s ** 2
    kb = (1 - 3 * rb ** 2) / (2 * rb); kc = (3 * rc ** 2 - 1) / (2 * rc)
    return kb ** 2 / D, kc ** 2 / D
fracs = [mp.mpf(x) for x in ('0.001', '0.05', '0.3', '0.7', '0.95', '0.999', '0.999999')]
vals = [bh_scan(fr) for fr in fracs]
chk("P2 BH normalisation: kappa_b^2/f(r*) >= 3 (min over the scan %s)" % mp.nstr(min(v[0] for v in vals), 8), all(v[0] >= 3 - mp.mpf('1e-9') for v in vals))
chk("P2 BH normalisation: 1 < kappa_c^2/f(r*) <= 3 (range %s .. %s)" % (mp.nstr(min(v[1] for v in vals), 6), mp.nstr(max(v[1] for v in vals), 8)),
    all(1 < v[1] <= 3 + mp.mpf('1e-9') for v in vals))
ctrl("kappa_b^2/f(r*) >= 4 is false (it approaches 3 at Nariai)", all(v[0] >= 4 for v in vals))
ctrl("kappa_c^2/f(r*) <= 2 is false", all(v[1] <= 2 for v in vals))

# =====================================================================================================================================
# P3: record's iff, enthalpy family, kernel moment, Sciama, N count
# =====================================================================================================================================
c_ = mp.mpf('2.9979'); G_ = mp.mpf('6.6743'); rho_ = mp.mpf('1.234')
def M1_of_kappa(k):
    return mp.mpf(2) / 3 * c_ / (k * c_ * mp.sqrt(G_ * rho_))
tL = 1 / mp.sqrt(G_ * rho_)
chk("P3 M1(kappa = 1/2) = (4/3) t_Lambda, M1(2/3) = t_Lambda, M1(1/3) = 2 t_Lambda (family M1 = (1 + w) t, kappa = 2/(3(1 + w)))",
    abs(M1_of_kappa(mp.mpf(1) / 2) - mp.mpf(4) / 3 * tL) < 1e-25 and abs(M1_of_kappa(mp.mpf(2) / 3) - tL) < 1e-25 and abs(M1_of_kappa(mp.mpf(1) / 3) - 2 * tL) < 1e-25)
ctrl("M1(kappa = 1/2) = t_Lambda is false", abs(M1_of_kappa(mp.mpf(1) / 2) - tL) < 1e-6)
T = mp.mpf('1.7')
chk("P3 sharp kernel 2 tau/T^2: total weight 1, first moment 2T/3 (quad)", abs(mp.quad(lambda t: 2 * t / T ** 2, [0, T]) - 1) < 1e-25 and abs(mp.quad(lambda t: t * 2 * t / T ** 2, [0, T]) - 2 * T / 3) < 1e-25)
ctrl("first moment is T/2 for the sharp kernel", abs(mp.quad(lambda t: t * 2 * t / T ** 2, [0, T]) - T / 2) < 1e-6)
Gv = mp.mpf('0.7'); rv = mp.mpf('1.9'); cv = mp.mpf('1.3')
H = mp.sqrt(8 * pi * Gv * rv / 3); Rs = cv / mp.sqrt(Gv * rv); RH = cv / H
Isc = lambda R: 2 * pi * Gv * rv * R ** 2 / cv ** 2
chk("P3 Sciama I(R) = 2 pi G rho R^2/c^2: I(R_H) = 3/4, I(R*) = 2 pi, I(2R*) = 8 pi", abs(Isc(RH) - mp.mpf(3) / 4) < 1e-25 and abs(Isc(Rs) - 2 * pi) < 1e-25 and abs(Isc(2 * Rs) - 8 * pi) < 1e-25)
Phi = mp.quad(lambda r: 4 * pi * r ** 2 / r, [0, RH])
chk("P3 potential of a uniform ball at the centre: int 4 pi r^2 (1/r) dr = 2 pi R^2", abs(Phi - 2 * pi * RH ** 2) < 1e-25)
RS = cv / mp.sqrt(2 * pi * Gv * rv)
rr = lambda R: (cv ** 2 / R) ** 2 / (Gv * rv * cv ** 2)
chk("P3 Rindler conversion a_c^2/(G rho c^2): R_H -> 8 pi/3, R_S -> 2 pi, R* -> 1, 2R* -> 1/4; closure I(R_S) = 1",
    abs(rr(RH) - 8 * pi / 3) < 1e-25 and abs(rr(RS) - 2 * pi) < 1e-25 and abs(rr(Rs) - 1) < 1e-25 and abs(rr(2 * Rs) - mp.mpf(1) / 4) < 1e-25 and abs(Isc(RS) - 1) < 1e-25)
ctrl("Rindler ratio at 2R* is 1/2", abs(rr(2 * Rs) - mp.mpf(1) / 2) < 1e-6)
# mu slope: finite difference
Ncv = mp.mpf('2.37'); sv = mp.mpf('0.61')
mu = lambda g: 1 - (1 - (g / sv) / (1 + g / sv)) ** Ncv
chk("P3 mu(g) = 1 - (1 - p)^N, p = (g/s)/(1 + g/s): mu'(0) = N/s (finite difference)", abs(mp.diff(mu, 0) - Ncv / sv) < 1e-15)
# c(N)
for Nv in [3, 2.5, 4, 7]:
    Nv = mp.mpf(Nv)
    cnum = mp.quad(lambda x: 2 * x * (1 + x / Nv) ** (-Nv), [0, 1, 10, 100, mp.inf])
    chk("P3 offset integral int 2x (1 + x/N)^(-N) dx = 2N^2/((N-1)(N-2)) at N = %s (%s)" % (mp.nstr(Nv, 3), mp.nstr(cnum, 8)), abs(cnum - 2 * Nv ** 2 / ((Nv - 1) * (Nv - 2))) < 1e-10)
Ts = (mp.mpf(10) ** 2, mp.mpf(10) ** 4, mp.mpf(10) ** 6)
part = [mp.quad(lambda x: 2 * x * (1 + x / 2) ** (-2), [0, 1, 10, 100, Tt]) for Tt in Ts]
closed = [8 * (mp.log((2 + Tt) / 2) + 2 / (2 + Tt) - 1) for Tt in Ts]
chk("P3 N = 2: partial integrals grow without bound and equal 8(ln((2+T)/2) + 2/(2+T) - 1) (%s, %s, %s)" % tuple(mp.nstr(p_, 5) for p_ in part),
    part[0] < part[1] < part[2] and all(abs(a - b) < 1e-10 for a, b in zip(part, closed)))

# =====================================================================================================================================
# P4: MacDowell-Mansouri ratios
# =====================================================================================================================================
Lv = mp.mpf('1.7'); hb = mp.mpf('0.9'); Gv = mp.mpf('0.6')
ig = Lv ** 2 / (16 * pi * hb * Gv)
rhoL = 3 / (8 * pi * Gv * Lv ** 2)
V4 = mp.quad(lambda t: mp.sin(t) ** 3, [0, pi]) * mp.quad(lambda t: mp.sin(t) ** 2, [0, pi]) * mp.quad(lambda t: mp.sin(t), [0, pi]) * 2 * pi * Lv ** 4
chk("P4 Vol(S^4_L) by sine-power quadrature = 8 pi^2 L^4/3; (12/L^4) Vol = 32 pi^2", abs(V4 - 8 * pi ** 2 * Lv ** 4 / 3) < 1e-20 and abs(12 / Lv ** 4 * V4 - 32 * pi ** 2) < 1e-20)
chk("P4 S_dS/hbar = pi L^2/(hbar G) = 2 x 8 pi^2/g^2 with 1/g^2 = L^2/(16 pi hbar G)", abs(pi * Lv ** 2 / (hb * Gv) - 2 * 8 * pi ** 2 * ig) < 1e-20)
ratio = (hb * ig * 12 / Lv ** 4 / 4) / rhoL
chk("P4 YM action density/rho_Lambda per chirality = 1/2, pair = 1 (%s)" % mp.nstr(ratio, 8), abs(ratio - mp.mpf(1) / 2) < 1e-20)
chk("P4 with the Lagrangian's 1/4 omitted the pair ratio is 4", abs(hb * ig * 12 / Lv ** 4 * 2 / rhoL - 4) < 1e-20)
ctrl("per-chirality ratio is 1", abs(ratio - 1) < 1e-6)
chk("P4 (1/4) ig |F|^2 Vol = 8 pi^2 ig per chirality", abs(mp.mpf(1) / 4 * ig * 12 / Lv ** 4 * V4 - 8 * pi ** 2 * ig) < 1e-20)

# =====================================================================================================================================
# P5: extended thermodynamics
# =====================================================================================================================================
Pv = mp.mpf('-0.13'); rv = mp.mpf('0.83')
Mext = lambda r, P: r / 2 + 4 * pi * P * r ** 3 / 3
Tt = (1 + 8 * pi * Pv * rv ** 2) / (4 * pi * rv); S = pi * rv ** 2; Vv = 4 * pi * rv ** 3 / 3
chk("P5 first law: dM/dr = T dS/dr (%s), dM/dP = V (numerical derivatives)" % mp.nstr(mp.diff(lambda r: Mext(r, Pv), rv), 8),
    abs(mp.diff(lambda r: Mext(r, Pv), rv) - Tt * 2 * pi * rv) < 1e-20 and abs(mp.diff(lambda P: Mext(rv, P), Pv) - Vv) < 1e-20)
chk("P5 Smarr M = 2TS - 2PV and U = M - PV = r/2", abs(Mext(rv, Pv) - (2 * Tt * S - 2 * Pv * Vv)) < 1e-20 and abs(Mext(rv, Pv) - Pv * Vv - rv / 2) < 1e-20)
ctrl("Smarr with -PV (not -2PV) is false", abs(Mext(rv, Pv) - (2 * Tt * S - Pv * Vv)) < 1e-6)
Lv = mp.mpf('1.3'); PL = -3 / (8 * pi * Lv ** 2); rr_ = mp.mpf('0.6')
kap = (1 - 3 * rr_ ** 2 / Lv ** 2) / (2 * rr_)
chk("P5 at P = -3/(8 pi L^2): M(r, P) = r(1 - r^2/L^2)/2, T = kappa/(2 pi), Gibbs M - TS = (r/4)(1 + r^2/L^2)",
    abs(Mext(rr_, PL) - rr_ * (1 - rr_ ** 2 / Lv ** 2) / 2) < 1e-25 and abs((1 + 8 * pi * PL * rr_ ** 2) / (4 * pi * rr_) - kap / (2 * pi)) < 1e-25 and
    abs(Mext(rr_, PL) - kap / (2 * pi) * pi * rr_ ** 2 - rr_ / 4 * (1 + rr_ ** 2 / Lv ** 2)) < 1e-25)
X_ = 3 * rr_ ** 2 / Lv ** 2
chk("P5 kappa^2/|P| = 2 pi (1 - X)^2/X with X = 3 r^2/L^2", abs(kap ** 2 / (3 / (8 * pi * Lv ** 2)) - 2 * pi * (1 - X_) ** 2 / X_) < 1e-25)
Xb = ((16 * pi + 1) - mp.sqrt(32 * pi + 1)) / (16 * pi); Xcc = ((16 * pi + 1) + mp.sqrt(32 * pi + 1)) / (16 * pi)
chk("P5 the puzzle condition 8 pi (1 - X)^2 = X has two roots %s, %s = 3 x_b^2, 3 x_c^2 of P2 (both horizons)" % (mp.nstr(Xb, 8), mp.nstr(Xcc, 8)),
    abs(8 * pi * (1 - Xb) ** 2 - Xb) < 1e-25 and abs(Xb - 3 * xb ** 2) < 1e-25 and abs(Xcc - 3 * xc ** 2) < 1e-25)
ctrl("X = 1/3 (the T_b = T_dS point) solves the puzzle condition", abs(8 * pi * (1 - mp.mpf(1) / 3) ** 2 - mp.mpf(1) / 3) < 1e-3)
chk("P5 flat probe: |P|V/M = r^2/L^2 = S/S_dS = 8 pi/3 at r = Z L/2", abs((3 / (8 * pi * Lv ** 2)) * (4 * pi * (Zp * Lv / 2) ** 3 / 3) / (Zp * Lv / 4) - 8 * pi / 3) < 1e-20)
chk("P5 T_b = T_dS at x = 1/3 gives a0^2/(G rho_L) = 8 pi/3 (kappa^2 = 8 pi/3: Z = 1, NOT the kappa = 1 kernel)",
    abs((1 - 3 * (mp.mpf(1) / 3) ** 2) / (2 * mp.mpf(1) / 3) - 1) < 1e-25 and abs(1 / (3 / (8 * pi)) - 8 * pi / 3) < 1e-25)


# lane X3 table (P1: kappa_b = a0, P2: kappa_c = a0) against the closed forms certified in P5 (horizon_ratios, CP_over_S, CP_puzzle_values)
def X3row(x):
    return dict(PVM=-x ** 2 / (1 - x ** 2), TSM=(1 - 3 * x ** 2) / (2 * (1 - x ** 2)), SS=x ** 2, VV=x ** 3, CP=-2 * (1 - 3 * x ** 2) / (1 + 3 * x ** 2))
r1 = X3row(xb); r2 = X3row(xc)
chk("P5 X3 table P1 (black-hole a0-horizon): PV/M = %s (lane -0.37579), TS/M = %s (0.12421), G/M = %s (0.87579), S/S_dS = %s (0.27314), V/V_dS = %s (0.14275), C_P/S = %s (-0.19849)" %
    tuple(mp.nstr(v, 5) for v in (r1['PVM'], r1['TSM'], 1 - r1['TSM'], r1['SS'], r1['VV'], r1['CP'])),
    abs(r1['PVM'] + mp.mpf('0.37579')) < 1e-5 and abs(r1['TSM'] - mp.mpf('0.12421')) < 1e-5 and abs(1 - r1['TSM'] - mp.mpf('0.87579')) < 1e-5 and
    abs(r1['SS'] - mp.mpf('0.27314')) < 1e-5 and abs(r1['VV'] - mp.mpf('0.14275')) < 1e-5 and abs(r1['CP'] + mp.mpf('0.19849')) < 1e-5)
chk("P5 X3 table P2 (cosmological a0-horizon): PV/M = %s (lane -0.68573), TS/M = %s (0.18573), G/M = -1 - TS/M = %s (-1.18573), S/S_dS = %s (0.40679), V/V_dS = %s (0.25945), C_P/S(cosm.) = %s (+0.19849)" %
    tuple(mp.nstr(v, 5) for v in (r2['PVM'], -r2['TSM'] * 0 + (3 * xc ** 2 - 1) / (2 * (1 - xc ** 2)), -1 - (3 * xc ** 2 - 1) / (2 * (1 - xc ** 2)), r2['SS'], r2['VV'], r2['CP'])),
    abs(r2['PVM'] + mp.mpf('0.68573')) < 1e-5 and abs((3 * xc ** 2 - 1) / (2 * (1 - xc ** 2)) - mp.mpf('0.18573')) < 1e-5 and
    abs(-1 - (3 * xc ** 2 - 1) / (2 * (1 - xc ** 2)) + mp.mpf('1.18573')) < 1e-5 and abs(r2['SS'] - mp.mpf('0.40679')) < 1e-5 and
    abs(r2['VV'] - mp.mpf('0.25945')) < 1e-5 and abs(r2['CP'] - mp.mpf('0.19849')) < 1e-5)
chk("P5 C_P/S = -/+ 2/sqrt(1 + 32 pi) = %s exactly at the two a0-horizons (CP_puzzle_values)" % mp.nstr(2 / mp.sqrt(1 + 32 * pi), 8),
    abs(r1['CP'] + 2 / mp.sqrt(1 + 32 * pi)) < 1e-25 and abs(r2['CP'] - 2 / mp.sqrt(1 + 32 * pi)) < 1e-25)
ctrl("C_P/S = -1/sqrt(1 + 32 pi) at the black-hole a0-horizon", abs(r1['CP'] + 1 / mp.sqrt(1 + 32 * pi)) < 1e-3)
chk("P5 barrier height of the off-shell free energy at T_b = T_dS: G_b = (r/4)(1 + x^2) at x = 1/3 equals 5 L/54", abs((mp.mpf(1) / 12) * (1 + mp.mpf(1) / 9) - mp.mpf(5) / 54) < 1e-25)

# =====================================================================================================================================
# P6: D-dimensional FRW recomputed from the metric (sympy)
# =====================================================================================================================================
tt = sp.symbols('t')
aa = sp.Function('a')(tt)
Gs, rhos, ps = sp.symbols('G rho p')
for d in [2, 3, 4, 5]:
    xs = [tt] + list(sp.symbols('x1:%d' % (d + 1)))
    gmat = sp.diag(-1, *([aa ** 2] * d))
    gi = gmat.inv()
    n = d + 1
    Gm = [[[sum(gi[a, e] * (sp.diff(gmat[e, b], xs[c]) + sp.diff(gmat[e, c], xs[b]) - sp.diff(gmat[b, c], xs[e])) for e in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]
    def Ricc(b, c):
        r = 0
        for a in range(n):
            r += sp.diff(Gm[a][b][c], xs[a]) - sp.diff(Gm[a][b][a], xs[c])
            for e in range(n):
                r += Gm[a][a][e] * Gm[e][b][c] - Gm[a][c][e] * Gm[e][b][a]
        return sp.simplify(r)
    R00 = Ricc(0, 0); R11 = Ricc(1, 1)
    Rsc = sp.simplify(gi[0, 0] * R00 + sum(gi[i, i] * Ricc(i, i) for i in range(1, n)))
    G00 = sp.simplify(R00 - gmat[0, 0] * Rsc / 2)
    Hh = sp.diff(aa, tt) / aa
    chk("P6 d = %d: G_00 = d(d-1)/2 H^2 (so H^2 = 16 pi G rho/(d(d-1)) from G_00 = 8 pi G rho)" % d, sp.simplify(G00 - sp.Rational(d * (d - 1), 2) * Hh ** 2) == 0)
    # acceleration law from the trace-reversed field equations R_mu nu = 8 pi G (T_mu nu - T g_mu nu/(D - 2)), T_00 = rho, T_ij = p a^2 delta_ij
    Ttr = -rhos + d * ps
    eq00 = sp.Eq(R00, 8 * sp.pi * Gs * (rhos - Ttr * gmat[0, 0] / (d - 1)))
    addot = sp.symbols('addot')
    sol = sp.solve(eq00.subs(sp.diff(aa, tt, 2), addot), addot)[0] / aa
    chk("P6 d = %d: addot/a = -8 pi G ((d-2) rho + d p)/(d(d-1))" % d, sp.simplify(sol + 8 * sp.pi * Gs * ((d - 2) * rhos + d * ps) / (d * (d - 1))) == 0)
    if d == 3:
        chk("P6 d = 3: the coefficient is the 4D law -8 pi G (rho + 3p)/6 = -(4 pi G/3)(rho + 3p)", sp.simplify(sol + sp.Rational(4, 3) * sp.pi * Gs * (rhos + 3 * ps)) == 0)
    if d == 4:
        ctrl("d = 4: the 'Tolman count' rho + d p (without the (d-2)) does not reproduce the law", sp.simplify(sol + 8 * sp.pi * Gs * (rhos + d * ps) / (d * (d - 1))) == 0)
chk("P6 Z_V(d) = d(d-1)/(d-2): 6, 6, 20/3 at d = 3, 4, 5", [mp.mpf(d * (d - 1)) / (d - 2) for d in (3, 4, 5)] == [6, 6, mp.mpf(20) / 3])
chk("P6 Euler units (4 pi)^n n! = 32 pi^2, 384 pi^3, 6144 pi^4 (n = 2, 3, 4); Chern (2 pi)^n n! = 8 pi^2, 48 pi^3, 384 pi^4",
    all(abs((4 * pi) ** n * mp.factorial(n) - v) < 1e-15 for n, v in [(2, 32 * pi ** 2), (3, 384 * pi ** 3), (4, 6144 * pi ** 4)]) and
    all(abs((2 * pi) ** n * mp.factorial(n) - v) < 1e-15 for n, v in [(2, 8 * pi ** 2), (3, 48 * pi ** 3), (4, 384 * pi ** 4)]))
ctrl("(4 pi)^2 2! = 16 pi^2", abs((4 * pi) ** 2 * 2 - 16 * pi ** 2) < 1e-6)

# =====================================================================================================================================
# P7: offset family
# =====================================================================================================================================
def cnum(mu, X=mp.inf):
    return mp.quad(lambda x: (1 - mu(x)) * 2 * x, [0, 1, 3, 10, 30, 100, X])
chk("P7 bathtub: sharp mu = min(x, 1): c = 1/3 exactly (quad over [0, T], T >= 1)", abs(mp.quad(lambda x: (1 - min(x, 1)) * 2 * x, [0, 1, 5]) - mp.mpf(1) / 3) < 1e-25)
chk("P7 steep mu = min(2x, 1) (slope 2 > 1): c = 1/12 < 1/3", abs(mp.quad(lambda x: (1 - min(2 * x, 1)) * 2 * x, [0, mp.mpf(1) / 2, 5]) - mp.mpf(1) / 12) < 1e-25)
# 1 - mu computed stably: OR family (1 + x/N)^(-N); exponential; Milgrom mu_4 = (1 + x^-4)^(-1/4) via -expm1(-log1p(x^-4)/4)
def cnum1m(one_minus_mu):
    return mp.quad(lambda x: one_minus_mu(x) * 2 * x, [0, 1, 3, 10, 30, 100, mp.inf])
cs_ = [cnum1m(lambda x, N=N: (1 + x / N) ** (-N)) for N in (3, 5, 11)] + [cnum1m(lambda x: mp.exp(-x)),
                                                                            cnum1m(lambda x: -mp.expm1(-mp.log1p(x ** (-4)) / 4) if x > 0 else mp.mpf(1))]
chk("P7 c >= 1/3 for slope <= 1 concave shapes (OR N = 3, 5, 11; exponential; Milgrom n = 4): %s" % ", ".join(mp.nstr(v, 5) for v in cs_), all(v >= mp.mpf(1) / 3 for v in cs_))
ctrl("c >= 1/2 for all slope <= 1 shapes is false (sharp gives 1/3)", all(v >= 0.5 for v in cs_ + [mp.mpf(1) / 3]))
Nst = (3 + mp.sqrt(1 + 1 / pi)) / 2
chk("P7 N* = (3 + sqrt(1 + 1/pi))/2 = %s: (N-1)(N-2) = 1/(4 pi), c(N*) = 8 pi N*^2, kappa* = 1/N* = %s (not 1/2)" % (mp.nstr(Nst, 8), mp.nstr(1 / Nst, 6)),
    abs((Nst - 1) * (Nst - 2) - 1 / (4 * pi)) < 1e-25 and abs(2 * Nst ** 2 / ((Nst - 1) * (Nst - 2)) - 8 * pi * Nst ** 2) < 1e-20 and 0.4821 < 1 / Nst < 0.4822)
# W thresholds
Gv = mp.mpf('0.9'); Mv = mp.mpf('2.1'); Lam = mp.mpf('0.37')
r0 = mp.findroot(lambda r: -Gv * Mv / r ** 2 + Lam * r / 3, 2)
chk("P7 W: zero-force sphere of the Newtonian Lambda force has mean density 2 rho_Lambda", abs(3 * Mv / (4 * pi * r0 ** 3) - 2 * Lam / (8 * pi * Gv)) < 1e-20)
rst = mp.findroot(lambda r: mp.diff(lambda x: Gv * Mv * x - Lam * x ** 4 / 3, r), 1)
chk("P7 W: outermost stable circular orbit (dL^2/dr = 0) has mean density 8 rho_Lambda", abs(3 * Mv / (4 * pi * rst ** 3) - 8 * Lam / (8 * pi * Gv)) < 1e-20)
LL = mp.mpf('1.1')
chk("P7 W: rho_Lambda A_dS = 3/(8 pi L^2) x 4 pi L^2 = 3/2 = 6 F_max (F_max = 1/4)", abs(3 / (8 * pi * LL ** 2) * 4 * pi * LL ** 2 - mp.mpf(3) / 2) < 1e-25)

# =====================================================================================================================================
# P8: Omega_Lambda arithmetic
# =====================================================================================================================================
a0v = mp.mpf('1.0766e-10'); H0v = mp.mpf('67.4e3') / mp.mpf('3.0856775814913673e22'); cc = mp.mpf(299792458)
Om = 32 * pi * a0v ** 2 / (3 * H0v ** 2 * cc ** 2)
chk("P8 Omega_pred = %s (audit 0.906) with H0 = 67.4 km/s/Mpc = %s 1/s" % (mp.nstr(Om, 6), mp.nstr(H0v, 6)), abs(Om - mp.mpf('0.906')) < 1e-3)
chk("P8 a0 needed for Omega = 0.685: a0'/a0 = %s (-13.0%%)" % mp.nstr(mp.sqrt(mp.mpf('0.685') / Om), 5), abs(mp.sqrt(mp.mpf('0.685') / Om) - mp.mpf('0.87')) < 1e-3)
ctrl("Omega_pred with 8 pi in place of 32 pi is 0.906", abs(8 * pi * a0v ** 2 / (3 * H0v ** 2 * cc ** 2) - 0.906) < 1e-3)

# =====================================================================================================================================
# PuzzleChain: the family S_Z
# =====================================================================================================================================
for Zt in [mp.mpf(1), mp.sqrt(8 * pi / 3), Zp, mp.mpf(6), 2 * pi]:
    a0_ = 1 / Zt; Lam_ = mp.mpf(3); rho_ = Lam_ / (8 * pi)
    vals = dict(AL=(pi / a0_ ** 2) * Lam_, Uv=Lam_ / a0_ ** 2, Wv=rho_ / a0_ ** 2, N=mp.sqrt(rho_) / a0_, kap=a0_ / mp.sqrt(rho_), I=2 * pi * rho_ * (1 / a0_) ** 2, coff=8 * pi * rho_ / a0_ ** 2)
    tgt = dict(AL=32 * pi ** 2, Uv=32 * pi, Wv=4, N=2, kap=mp.mpf(1) / 2, I=8 * pi, coff=32 * pi)
    hit = {k: abs(vals[k] - tgt[k]) < 1e-20 for k in vals}
    isp = abs(Zt - Zp) < 1e-20
    chk("Chain family Z' = %s: all seven quantities hit their targets iff Z' = sqrt(32 pi/3): %s" % (mp.nstr(Zt, 6), "all hit" if all(hit.values()) else "none hit" if not any(hit.values()) else "MIXED"),
        (all(hit.values()) if isp else not any(hit.values())))
chk("Chain Z^2 kappa^2 = 8 pi/3 in the family (kappa = a0/sqrt(rho), Z = 1/a0 at H = 1)", abs((1 / mp.mpf('0.37')) ** 2 * ((mp.mpf('0.37') / mp.sqrt(3 / (8 * pi))) ** 2) - 8 * pi / 3) < 1e-25)
ctrl("Z^2 kappa^2 = 32 pi/3 is false", abs((1 / mp.mpf('0.37')) ** 2 * ((mp.mpf('0.37') / mp.sqrt(3 / (8 * pi))) ** 2) - 32 * pi / 3) < 1e-6)

print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
