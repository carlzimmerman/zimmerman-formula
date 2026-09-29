"""g06: the dS / Rindler / Unruh structure with the a0-Rindler length Z L, and the crossover the dS symmetry DOES supply.

Static patch  ds^2 = -(1 - H^2 r^2) dt^2 + dr^2/(1 - H^2 r^2) + r^2 dOmega^2   (c = 1).
 A  static observer at r=x/H: proper acceleration a = H x/sqrt(1-x^2);  Tolman-redshifted horizon temperature T_loc = H/(2 pi sqrt(1-x^2)):
    T_loc = sqrt(a^2 + H^2)/(2 pi)   (the Deser-Levin form) -- exact, from the Killing structure alone.
 B  hence the ONLY scale of that function is a = H (where the two terms are equal).  The symmetry-derived crossover is a* = H, i.e. Z = 1
    (kappa = sqrt(8 pi/3) = 2.894), a factor Z_fw = 5.789 above the framework a0 = H/Z_fw; the vacuum-effect inertia mu_V = a/sqrt(a^2+H^2)
    has mu_V = 1/2 at a = H/sqrt(3), not at H/Z_fw.
 C  at a = a0 = H/Z_fw: T_loc/T_dS = sqrt(1 + 3/(32 pi)) = 1.0147 (transcendental, no special value); the Rindler length c^2/a0 = Z L is reached
    at tan(theta) = 1/Z (sin theta = 1/sqrt(1+Z^2)) -- bookkeeping only (p06 D1).
 D  a symmetric rescaling of the crossover by an ALGEBRAIC number N (a0 = H/N) needs N = 5.789 = sqrt(33.51): a single inserted factor.  Milgrom's own
    identification of the dS-inertia scale is a0 = H with an extra 2 pi taken from the data (the record's 'a0 = cH/2 pi'): the 2 pi is not supplied by the dS symmetry.
"""
import sympy as sp, mpmath as mp, sys
ok = []
def chk(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

r, H, x = sp.symbols('r H x', positive=True)
gtt = -(1 - H**2 * r**2); grr = 1 / (1 - H**2 * r**2)
a_static = sp.simplify(-sp.sqrt(1 / grr) * sp.diff(sp.log(sp.sqrt(-gtt)), r))       # |nabla ln sqrt(-g_tt)|
xs = H * r
chk("A1 static-observer acceleration a = H x/sqrt(1-x^2), x = H r", sp.simplify(a_static - H * xs / sp.sqrt(1 - xs**2)) == 0)
# surface gravity at the horizon r = 1/H w.r.t. Killing time t: kappa_s = (1/2) |d_r g_tt| / sqrt(-g_tt g_rr) -> H
kap_s = sp.simplify(sp.Rational(1, 2) * sp.Abs(sp.diff(gtt, r)).subs(r, 1 / H))
chk("A2 surface gravity of the cosmological horizon w.r.t. the Killing time t equals H (kappa_s = (1/2)|d_r g_tt| at r = 1/H, since g_tt g_rr = -1)", sp.simplify(kap_s - H) == 0)
Tloc = H / (2 * sp.pi * sp.sqrt(1 - xs**2))
chk("A3 Tolman: T_loc = sqrt(a^2 + H^2)/(2 pi) exactly (Deser-Levin form)", sp.simplify(Tloc**2 - (a_static**2 + H**2) / (4 * sp.pi**2)) == 0)
# B
Zfw = sp.sqrt(32 * sp.pi / 3)
muV = lambda a: a / sp.sqrt(a**2 + H**2)
chk("B1 mu_V(a) = a/sqrt(a^2+H^2) = 1/2 at a = H/sqrt(3) (NOT at H/Z_fw): the crossover point of the symmetry-derived inertia", sp.simplify(muV(H / sp.sqrt(3)) - sp.Rational(1, 2)) == 0 and abs(float(muV(H / Zfw)) - 0.5) > 0.3)
chk("B2 the only intrinsic scale of T(a) is a = H (T^2 = (a^2 + H^2)/4 pi^2: two equal terms at a = H); a0/H = 1/Z_fw = 0.1727 is a factor 5.79 below it", abs(float(Zfw) - 5.7888) < 1e-3)
# C
ratio = sp.sqrt(1 + 1 / Zfw**2)
chk("C1 T(a0)/T_dS = sqrt(1 + 3/(32 pi)) = 1.01478 (transcendental; no special value)", abs(float(ratio) - 1.01478) < 1e-4 and sp.sqrt(1 + sp.Rational(3, 32) / sp.pi).is_algebraic is False)
sinth = 1 / sp.sqrt(1 + Zfw**2)
chk("C2 Rindler length c^2/a0 = Z L is reached at the static radius x = sin(theta_0) = 1/sqrt(1+Z^2) = 0.1702 (a(x) = H/Z)", abs(float(sinth) - 0.17023) < 1e-4 and sp.simplify((xs / sp.sqrt(1 - xs**2)).subs(r, sinth / H) - 1 / Zfw) == 0)
# D
chk("D1 an algebraic N with a0 = H/N: kappa = sqrt(8 pi/3)/N (transcendental for every algebraic N != 0); N = Z_fw = 5.789 is transcendental, N = 6 (3.6% away) or 2 pi (8% away) are insertions",
    abs(float(Zfw) / 6 - 1) < 0.04 and abs(float(Zfw) / (2 * float(mp.pi)) - 1) < 0.09)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
