#!/usr/bin/env python3
"""a07_sds_surface_gravity.py -- adversarial audit of README section 8 ("no real horizon of this universe carries a0").

p06 shows: the Schwarzschild mass M_s = Z L/4 that has flat-space surface gravity a0 has NO horizon in Schwarzschild-de Sitter (M_s = 7.52 M_Nariai).  True.
README section 8 then says the object's a0 is 'a sub-Hubble acceleration that no real horizon of this universe carries'.  That is a different, universal claim, and it depends on the Killing normalisation:
in the f-normalisation (kappa_dS = H at M = 0) the surface gravity of the black-hole horizon r_b falls continuously from infinity (M -> 0) to ZERO at the Nariai mass, so a horizon with kappa = a0 = H/Z exists for a
definite mass M* < M_Nariai (near-Nariai black hole); in the Bousso-Hawking normalisation (check S5) every SdS horizon has kappa >= H and the README sentence is true.  The only thing p06 excludes is the FLAT-SPACE relation A = pi/a0^2, kappa = 1/(4M), i.e. the puzzle's own area formula.

Checks (L = 1, H = 1, Z = sqrt(32 pi/3)):
 S1  SdS horizon condition 2M = r - r^3 (L=1): horizons exist iff M <= 1/(3 sqrt 3) (= M_Nariai); reproduced by an independent method (extremum of r - r^3).
 S2  kappa_b(M) is continuous, decreasing from infinity to 0 on (0, M_Nariai): solve kappa_b = 1/Z, kappa_c = 1/Z; both have solutions.
 S3  at that mass the horizon area is ~ (4 pi/3) L^2, so A Lambda = 4 pi (Nariai-like), NOT 32 pi^2: the horizon carries a0 as a surface gravity but does not satisfy the puzzle's area relation.
 S4  the surface gravity of the CHARGE-free dS horizon itself is exactly H (kappa_c(M=0) = 1).\n S5  CAVEAT: the value of kappa depends on the Killing normalisation (none is canonical in dS).  With the Bousso-Hawking normalisation every SdS horizon has kappa >= H, so the README sentence is true there.
Exit 0 = all checks held (they show the README sentence is too strong).
"""
import math, sys
import mpmath as mp

mp.mp.dps = 30
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

Z = mp.sqrt(32 * mp.pi / 3)
a0 = 1 / Z
MN = 1 / (3 * mp.sqrt(3))
# S1
rmax = mp.findroot(lambda r: mp.diff(lambda x: x - x**3, r), 0.5)
chk("S1 max of r - r^3 is at r = 1/sqrt3 with value 2/(3 sqrt3) => M_Nariai = 1/(3 sqrt3) = %s (independent of p06's polynomial-root method)" % mp.nstr(MN, 10),
    abs(rmax - 1 / mp.sqrt(3)) < 1e-20 and abs((rmax - rmax**3) / 2 - MN) < 1e-20)

def horizons(M):
    # roots of r^3 - r + 2M = 0 (three real roots for 0 < M < M_N); the two positive ones are r_b < r_c
    rts = sorted([mp.re(z) for z in mp.polyroots([1, 0, -1, 2 * M], maxsteps=200, extraprec=100) if mp.re(z) > 0])
    assert len(rts) == 2
    return rts[0], rts[1]
def kap(r, M):
    return abs(2 * M / r**2 - 2 * r) / 2

def kappa_b(M):
    rb, rc = horizons(M)
    return kap(rb, M)
def kappa_c(M):
    rb, rc = horizons(M)
    return kap(rc, M)

# S2: bracket in M
Ms_b = mp.findroot(lambda M: kappa_b(M) - a0, (MN * mp.mpf('0.5'), MN * mp.mpf('0.999')), solver='anderson')
Ms_c = mp.findroot(lambda M: kappa_c(M) - a0, (MN * mp.mpf('0.5'), MN * mp.mpf('0.999')), solver='anderson')
rb_b, rc_b = horizons(Ms_b)
print("   M*(kappa_b = a0) = %s M_N ; r_b = %s r_c = %s ; kappa_b = %s (a0 = %s)" % (mp.nstr(Ms_b / MN, 10), mp.nstr(rb_b, 8), mp.nstr(rc_b, 8), mp.nstr(kappa_b(Ms_b), 10), mp.nstr(a0, 10)))
chk("S2a a real black-hole horizon of SdS with surface gravity EXACTLY a0 = H/Z exists: M* = %s M_N < M_N (f-normalisation; the README sentence names no normalisation -- see S5)" % mp.nstr(Ms_b / MN, 8),
    Ms_b < MN and abs(kappa_b(Ms_b) - a0) < 1e-20)
chk("S2b likewise the cosmological horizon of a near-Nariai SdS spacetime has kappa_c = a0 at M = %s M_N" % mp.nstr(Ms_c / MN, 8), Ms_c < MN and abs(kappa_c(Ms_c) - a0) < 1e-20)
chk("S2c kappa_b -> 0 at the Nariai mass and -> infinity as M -> 0 (monotone check at 6 masses)",
    all(kappa_b(MN * f1) > kappa_b(MN * f2) for f1, f2 in [(0.01, 0.1), (0.1, 0.5), (0.5, 0.9), (0.9, 0.99), (0.99, 0.9999)]) and kappa_b(MN * mp.mpf('0.9999')) < 0.05)
# S3
Lam = 3
A_b = 4 * mp.pi * rb_b**2
print("   at M*: A_b Lambda = %s  (puzzle needs 32 pi^2 = %s; near-Nariai gives ~4 pi = %s)" % (mp.nstr(A_b * Lam, 8), mp.nstr(32 * mp.pi**2, 8), mp.nstr(4 * mp.pi, 8)))
chk("S3 the a0-horizon of SdS has A Lambda = %.2f, far from 32 pi^2 = %.1f: the puzzle's AREA relation (flat-space Smarr, A = pi/kappa^2) fails there, but the surface-gravity value a0 is realised" % (float(A_b * Lam), float(32 * mp.pi**2)),
    A_b * Lam < 30)
# S4
chk("S4 M = 0: the cosmological horizon has kappa = H = 1 exactly (f' = -2r at r = 1)", abs(kap(1, 0) - 1) < 1e-25)
# S5 normalisation dependence (the caveat that limits H2): Bousso-Hawking normalisation of the Killing vector, xi = d_t / sqrt(f(r*)), r* = (M L^2)^(1/3) where f' = 0
def f_of(r, M): return 1 - 2 * M / r - r**2
def kBH(which, M):
    rb, rc = horizons(M)
    rstar = M**(mp.mpf(1) / 3)
    return kap(rb if which == 'b' else rc, M) / mp.sqrt(f_of(rstar, M))
fr = [mp.mpf(x) for x in ('0.001', '0.05', '0.3', '0.7', '0.95', '0.999', '0.999999')]
kb_list = [kBH('b', MN * x) for x in fr]
kc_list = [kBH('c', MN * x) for x in fr]
print("   Bousso-Hawking-normalised kappa_b over M/M_N:", [mp.nstr(v, 5) for v in kb_list])
print("   Bousso-Hawking-normalised kappa_c over M/M_N:", [mp.nstr(v, 5) for v in kc_list])
chk("S5 in the Bousso-Hawking normalisation every SdS horizon has kappa >= H (kappa_b in [sqrt3 H, inf), kappa_c in [H, sqrt3 H]), so a0 = H/Z < H is NOT realised there: README 8's sentence is true in THAT normalisation and false in the f-normalisation of S2 -- the statement must name the Killing normalisation",
    min(kb_list) > mp.sqrt(3) * (1 - mp.mpf('1e-3')) and min(kc_list) > 1 - mp.mpf('1e-3') and max(kc_list) < mp.sqrt(3) * (1 + mp.mpf('1e-3')))
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
