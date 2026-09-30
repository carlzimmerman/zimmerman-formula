#!/usr/bin/env python3
"""z02: the MOMENT arithmetic and the CUTOFF MAP.  For each kernel shape, and for the Sciama kernel at its PHYSICAL strength, what cutoff R_c does the
record's requirement M1 = (2/3) c/a0 = (4/3) t_Lambda imply?  (c = 1 inside formulas; t_L = (G rho_Lambda)^(-1/2); R* = c t_L.)
Kernel notation (record): K(s) = M0 k(s/T)/T with k unit-normalised, M0 = N = int K ds (free), M1 = int s K ds = M0 m1 T."""
import sympy as sp
from sympy import pi, sqrt, Rational as Rat, symbols
import mpmath as mp
import sys

PASS = FAIL = CO = CB = 0


def chk(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print("  ok  ", n, d)
    else: FAIL += 1; print("  FAIL", n, d)


def ctrl(n, c, d=""):
    global CO, CB
    if not c: CO += 1; print("  ctrl-ok ", n, d)
    else: CB += 1; print("  CTRL-BAD", n, d)


def zero(e): return sp.simplify(e) == 0


xx, T, M0, tL, a0 = symbols('x T M0 t_L a0', positive=True)
# the requirement (record): M1 = (2/3) c/a0 with c/a0 = 2 t_L  =>  M1 = (4/3) t_L
M1_req = Rat(4, 3) * tL
chk("requirement: a0 = c/(2 t_L)  =>  (2/3) c/a0 = (4/3) t_L", zero(Rat(2, 3) / (1 / (2 * tL)) - M1_req))

print("== M1: unit-normalised shapes: first moment, and the cutoff they imply (at weight M0) ==")
shapes = {
    "sharp r dr (Sciama weight, [0,1])": (2 * xx, (0, 1)),
    "uniform dr ([0,1]; 1/r^2-type weight)": (sp.Integer(1), (0, 1)),
    "exponential (record's minimal kernel)": (sp.exp(-xx), (0, sp.oo)),
    "Yukawa r e^{-r/R} dr (= record's gamma-2)": (xx * sp.exp(-xx), (0, sp.oo)),
}
table = {}
for nm, (k, (lo, hi)) in shapes.items():
    m0 = sp.integrate(k, (xx, lo, hi)); m1 = sp.integrate(xx * k, (xx, lo, hi))
    Tsol = sp.solve(sp.Eq(M0 * m1 * T, M1_req), T)[0]            # scale time T (cutoff for the sharp/uniform shapes, decay time for exp/Yukawa)
    table[nm] = (m0, m1, sp.simplify(Tsol / tL))
    print(f"   {nm:44s}: m0 = {m0}, m1 = {m1}, T/t_L = {sp.simplify(Tsol/tL)}  => R_c/R* = {sp.simplify(Tsol/tL)}")
    assert zero(m0 - 1)
chk("sharp r dr: m1 = 2/3, T = (2)t_L/M0 : at M0 = 1 R_c = 2 R* = c^2/a0 (X3's identification)", table["sharp r dr (Sciama weight, [0,1])"][1] == Rat(2, 3) and zero(table["sharp r dr (Sciama weight, [0,1])"][2].subs(M0, 1) - 2))
chk("uniform: m1 = 1/2 -> R_c = (8/3) R* at M0 = 1", table["uniform dr ([0,1]; 1/r^2-type weight)"][1] == Rat(1, 2) and zero(table["uniform dr ([0,1]; 1/r^2-type weight)"][2].subs(M0, 1) - Rat(8, 3)))
chk("exponential: m1 = 1 -> lambda = (4/3) t_L at M0 = 1 (record's mi_local_source_for_K: N = 4/3 with lambda = t_L is the SAME requirement at lambda = t_L)", table["exponential (record's minimal kernel)"][1] == 1 and zero(table["exponential (record's minimal kernel)"][2].subs(M0, 1) - Rat(4, 3)))
chk("Yukawa/gamma-2: m1 = 2 -> R = (2/3) R* at M0 = 1 (X3: c^2/(3 a0))", table["Yukawa r e^{-r/R} dr (= record's gamma-2)"][1] == 2 and zero(table["Yukawa r e^{-r/R} dr (= record's gamma-2)"][2].subs(M0, 1) - Rat(2, 3)))
vals = [table[k][2].subs(M0, 1) for k in table]
chk("the SAME requirement M1 = (4/3) t_L gives four different cutoffs 2, 8/3, 4/3, 2/3 (x R*) for four shapes: 'R_c = c^2/a0' is a statement about ONE shape, not about the requirement", len(set(vals)) == 4)
chk("and for every shape R_c is proportional to 1/M0: the weight is a free parameter in the record, so the cutoff is not determined by the requirement at all", all(zero(table[k][2] * M0 - table[k][2].subs(M0, 1)) for k in table))

print("\n== M2: which moment the record uses (control: a wrong moment must be detected) ==")
Ts = symbols('Ts', positive=True)
ksharp = 2 * xx
M0s = sp.integrate(ksharp, (xx, 0, 1)); M1s = sp.integrate(xx * ksharp, (xx, 0, 1)); M2s = sp.integrate(xx ** 2 * ksharp, (xx, 0, 1))
sol_first = sp.solve(sp.Eq(M1s * Ts, M1_req), Ts)[0]
chk("FIRST moment (record: Theta = M1 |a|/c): sharp kernel gives T = 2 t_L = c/a0", zero(sol_first - 2 * tL))
ctrl("control (wrong moment): using the RMS lag sqrt(M2) = T/sqrt(2) instead of the mean lag M1 = (2/3)T still gives T = 2 t_L", zero(sp.solve(sp.Eq(sp.sqrt(M2s) * Ts, M1_req), Ts)[0] - 2 * tL), f"(it gives T = {sp.N(sp.solve(sp.Eq(sp.sqrt(M2s) * Ts, M1_req), Ts)[0].subs(tL, 1), 5)} t_L)")
ctrl("control (wrong moment): a UNIFORM weight has the sharp kernel's first moment (2/3) T", zero(sp.integrate(xx * 1, (xx, 0, 1)) - Rat(2, 3)))
ctrl("control (wrong requirement): the record's PRE-correction requirement M1 = c/a0 gives the same T = 2 t_L", zero(sp.solve(sp.Eq(M1s * Ts, 2 * tL), Ts)[0] - 2 * tL))
print("   (the last control shows R_c = c^2/a0 relies on the (2/3) of the memory-force step; without it R_c = (3/2) c^2/a0 = 3 R*)")
chk("with the pre-correction requirement M1 = c/a0 = 2 t_L the sharp kernel would need T = 3 t_L = (3/2) c^2/a0", zero(sp.solve(sp.Eq(M1s * Ts, 2 * tL), Ts)[0] - 3 * tL))

print("\n== M3: the 'clean' R_c = c^2/a0 is the cancellation of TWO UNRELATED factors of 2/3 ==")
f_ren, f_ker = Rat(2, 3), M1s
chk("factor 1: 2/3 from the memory-force renormalisation a0 -> (2/3) a0 of the ACTION (z01 K4; mu_eff = mu + (Y/2) mu' -> (3/2) Y)", f_ren == Rat(2, 3))
chk("factor 2: 2/3 = int x (2x) dx, the MEAN LAG of the r dr weight on [0,1] (a property of the kernel shape)", f_ker == Rat(2, 3))
chk("they cancel: T = (f_ren/f_ker) c/a0 = c/a0; any other shape gives T = (2/3) c/(a0 m1) != c/a0 (m1 = 1/2, 1, 2 above)", zero(f_ren / f_ker - 1))
ctrl("control: with the exponential shape (m1 = 1) the two factors still cancel", zero(f_ren / table["exponential (record's minimal kernel)"][1] - 1))

print("\n== M4: the record's own admissible shapes cannot see the shape (only M1), so identification by shape is not an option ==")
mp.mp.dps = 25


def theta_shape(kfun, Tsc, Om, v, tmax):
    """Theta = int K(s) 2 v |sin(Om s/2)| ds, NR circular orbit, K integrates to 1 over [0,tmax]; quadrature with zero breakpoints"""
    f = lambda ss: kfun(ss) * 2 * v * abs(mp.sin(Om * ss / 2))
    per = 2 * mp.pi / Om
    n = int(mp.ceil(tmax / per)); tot = mp.mpf(0)
    for j in range(n):
        a, b = j * per, min((j + 1) * per, tmax)
        if b > a: tot += mp.quad(f, [a, (a + b) / 2, b])
    return tot


Om, v = mp.mpf(1), mp.mpf("0.001")
M1val = mp.mpf("0.02")          # same first moment for all shapes, ~ x = Om*M1 = 0.02 << 1 (short memory)
sh = {"sharp r dr": (lambda s_: 2 * s_ / mp.mpf(1.5 * M1val) ** 2, 1.5 * M1val),
      "exponential": (lambda s_: mp.e ** (-s_ / M1val) / M1val, 60 * M1val),
      "gamma-2": (lambda s_: s_ * mp.e ** (-s_ / (M1val / 2)) / (M1val / 2) ** 2, 60 * M1val),
      "box": (lambda s_: 1 / (2 * M1val), 2 * M1val)}
vals = {}
for nm, (kf, tm) in sh.items():
    m1n = mp.quad(lambda s_: s_ * kf(s_), [0, tm]); m0n = mp.quad(kf, [0, tm])
    vals[nm] = theta_shape(kf, None, Om, v, tm) / (M1val * Om * v)
    print(f"   {nm:11s}: M0 = {mp.nstr(m0n, 8)}, M1 = {mp.nstr(m1n, 8)}, Theta/(M1 |a|/c) = {mp.nstr(vals[nm], 8)}")
chk("four shapes at the same M1 (sharp r dr, exponential, gamma-2, box) give the same Theta = M1|a|/c to O((Omega M1)^2) ~ 1e-4: the shape is invisible to the action, so 'the record's kernel IS the r dr kernel' has no observable content",
    all(abs(vals[k] - 1) < 5e-3 for k in vals), f"max |ratio - 1| = {mp.nstr(max(abs(vals[k]-1) for k in vals), 3)}")
ctrl("control (wrong moment): a kernel whose first moment is 1.2 M1 gives the same Theta/(M1|a|/c)", abs(theta_shape(sh['exponential'][0], None, Om, v, 60 * M1val) * 1.2 / (M1val * Om * v) - 1) < 5e-3)

print("\n== M5: Sciama's PHYSICAL kernel: strength is fixed by G rho, so the cutoff cannot be chosen freely ==")
Gr, Tt, u = symbols('G_rho T_t u', positive=True)             # G rho_Lambda = 1/t_L^2
w_S = 4 * pi * Gr * u                                          # F/m = -int w_S(u) a(t-u) du /c^2 * c^2 ; X3's premise; c = 1: [w_S] = 1/time
M0_S = sp.integrate(w_S, (u, 0, Tt)); M1_S = sp.integrate(u * w_S, (u, 0, Tt))
chk("Sciama weight 4 pi G rho r dr/c^2 = 4 pi G rho u du: zeroth moment M0 = 2 pi G rho T^2 (= X3's I), first moment M1 = (4 pi/3) G rho T^3 (dimension of K: 1/time)", zero(M0_S - 2 * pi * Gr * Tt ** 2) and zero(M1_S - Rat(4, 3) * pi * Gr * Tt ** 3))
chk("mean lag M1/M0 = (2/3) T (this is what X3 calls 'the first moment of the sharp Sciama kernel' -- it is the first moment of the NORMALISED weight)", zero(M1_S / M0_S - Rat(2, 3) * Tt))
sub = {Gr: 1 / tL ** 2}
# (a) X3's cutoff T = c/a0 = 2 t_L
M0a = sp.simplify(M0_S.subs(sub).subs(Tt, 2 * tL)); M1a = sp.simplify(M1_S.subs(sub).subs(Tt, 2 * tL))
chk("(a) at X3's cutoff T = 2 t_L the physical strength is M0 = 8 pi (X3's I = 8 pi) and the physical first moment is (32 pi/3) t_L", zero(M0a - 8 * pi) and zero(M1a - Rat(32, 3) * pi * tL))
chk("    the record requires (4/3) t_L: the physical Sciama kernel at T = c/a0 overshoots the requirement by exactly 8 pi = 25.13; a0_eff = a0/(8 pi)", zero(M1a / M1_req - 8 * pi))
# (b) physical strength AND the requirement
Tb = sp.solve(sp.Eq(M1_S.subs(sub), M1_req), Tt)
Tb = [t_ for t_ in Tb if t_.is_positive][0] if len(Tb) > 1 else Tb[0]
Tb = sp.simplify(Tb)
M0b = sp.simplify(M0_S.subs(sub).subs(Tt, Tb))
print(f"   (b) physical strength + M1 = (4/3) t_L : T = {Tb}, T/t_L = {sp.N(Tb.subs(tL, 1), 6)}; M0 = {M0b} = {sp.N(M0b.subs(tL,1), 6)}")
chk("(b) physical strength AND M1 = (4/3) t_L fix T = pi^(-1/3) t_L (R_c = 0.683 R*, NOT 2 R*) and M0 = 2 pi^(1/3) = 2.93", zero(Tb - pi ** Rat(-1, 3) * tL) and zero(M0b - 2 * pi ** Rat(1, 3)))
ctrl("control: at the physical strength R_c = c^2/a0 = 2 R* satisfies the requirement", zero(M1a - M1_req))
# (c) Sciama closure M0 = 1
Tc = sp.simplify(sp.solve(sp.Eq(M0_S.subs(sub), 1), Tt)[0])
M1c = sp.simplify(M1_S.subs(sub).subs(Tt, Tc)); a0c = sp.simplify(Rat(2, 3) / M1c)
chk("(c) Sciama closure (M0 = I = 1) sets T = t_L/sqrt(2 pi) = R_S/c, M1 = (2/3) T; the record's relation a0 = (2/3)c/M1 then gives a0^2 t_L^2 = 2 pi (X3's R_S row), a factor 8 pi above the puzzle's 1/4", zero(Tc - tL / sqrt(2 * pi)) and zero(a0c ** 2 * tL ** 2 - 2 * pi) and zero(2 * pi / Rat(1, 4) - 8 * pi))
# consistency: for a free strength N (M0 = N), the map "strength = Sciama physical" is one equation N = 2 pi T^2/t_L^2 with N T = 2 t_L  (Map 1, sharp)
Nn, T2 = symbols('N T2', positive=True)
sol = sp.solve([sp.Eq(Nn, 2 * pi * T2 ** 2 / tL ** 2), sp.Eq(Nn * T2, 2 * tL)], [Nn, T2], dict=True)
chk("solving 'M0 = 2 pi T^2/t_L^2' with 'M0 T = c/a0 = 2 t_L' (sharp shape, M1 = (2/3) M0 T = (2/3) c/a0) gives N^3 = 8 pi: N = (8 pi)^(1/3) = 2.93", any(zero(s_[Nn] - (8 * pi) ** Rat(1, 3)) for s_ in sol))
# Yukawa (screened) physical kernel w = 4 pi G rho u e^{-u/L}
Lq = symbols('L_q', positive=True)
wY = 4 * pi * Gr * u * sp.exp(-u / Lq)
M0Y = sp.integrate(wY, (u, 0, sp.oo)); M1Y = sp.integrate(u * wY, (u, 0, sp.oo))
LY = sp.simplify(sp.solve(sp.Eq(M1Y.subs(sub), M1_req), Lq)[0]); M0Yv = sp.simplify(M0Y.subs(sub).subs(Lq, LY))
print(f"   screened physical kernel: L = {LY}, L/t_L = {sp.N(LY.subs(tL, 1), 6)}, M0 = {sp.N(M0Yv.subs(tL, 1), 6)}")
chk("screened (Yukawa) physical kernel 4 pi G rho r e^{-r/L} dr: M1 = (4/3) t_L gives L = (6 pi)^(-1/3) t_L (0.376 t_L) and M0 = 4 pi/(6 pi)^(2/3) = 1.77", zero(LY - (6 * pi) ** Rat(-1, 3) * tL) and zero(M0Yv - 4 * pi / (6 * pi) ** Rat(2, 3)))
chk("in ALL physical-strength cases M0 = O(1..25): the record needs M0 = N >= 2.1e6 (z01 K6); see z04 for what that does", all(float(v_.subs(tL, 1)) < 30 for v_ in (M0a, M0b, M0Yv)))

print("\n== M6: dimension of the two weights: K (record) and the Sciama weight w_S are both 1/time; the record's ACCELERATION weight is a different function ==")
# record, general orbits (eq 11): Theta = (1/c) int ds K(s) s |a(tau - s/2)| = (1/c) int du W(u) |a(tau-u)|, W(u) = 4 u K(2u)
Kg = sp.Function('K')
uu, ss = symbols('uu ss', positive=True)
W_of_K = lambda Kf: 4 * uu * Kf.subs(ss, 2 * uu)
Kphys = 4 * pi * Gr * ss                                            # record's K := Sciama weight (dimension 1/time, no free constant)
W_phys = sp.simplify(W_of_K(Kphys))
chk("if the record's K is Sciama's weight (K := 4 pi G rho s: dimension 1/time like K, with no extra time constant introduced), the record's acceleration weight is W(u) = 4 u K(2u) = 32 pi G rho u^2 (a u^2 ramp), NOT Sciama's linear ramp: the record's Theta and Sciama's force are different functionals of the same kernel", zero(W_phys - 32 * pi * Gr * uu ** 2))
ctrl("control: W(u) = 4 u K(2u) is linear in u for the r dr kernel", zero(sp.diff(W_phys, uu, 2)))
# exact rectilinear rapidity gap (monotone motion): Theta = int K(s) int_0^s a(tau-u) du ds = int du a(tau-u) Kbar(u), Kbar(u) = int_u^inf K(s) ds
Cs = symbols('C_s', positive=True)
Kb = sp.integrate(Cs * ss, (ss, uu, Tt))
chk("exact-gap acceleration weight of the record for K = C s on [0,T] is the TAIL Kbar(u) = C (T^2 - u^2)/2 (decreasing parabola) -- not Sciama's rising ramp either; DC gain int Kbar du = M1", zero(Kb - Cs * (Tt ** 2 - uu ** 2) / 2) and zero(sp.integrate(Kb, (uu, 0, Tt)) - sp.integrate(ss * Cs * ss, (ss, 0, Tt))))
ctrl("control: the tail weight is linear in u", zero(sp.diff(Kb, uu, 2)))
chk("DC gain of the record's acceleration weight = M1 (eq. after 11): int W du = int s K ds", zero(sp.integrate(W_of_K(Kphys), (uu, 0, Tt / 2)) - sp.integrate(ss * Kphys, (ss, 0, Tt))))

print(f"\n== TOTAL: {PASS} pass, {FAIL} fail; controls rejected {CO}, not rejected {CB} ==")
sys.exit(0 if FAIL == 0 and CB == 0 else 1)
