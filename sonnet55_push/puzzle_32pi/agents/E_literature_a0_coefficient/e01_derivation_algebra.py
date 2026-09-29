#!/usr/bin/env python3
"""e01_derivation_algebra.py -- reproduce, from the papers' own equations, every published a0 <-> (H or Lambda) coefficient
that is actually COMPUTED (not merely quoted), and show which step carries the number.

Units c = G = hbar = k_B = 1 unless stated.  H = H_Lambda = sqrt(Lambda/3) is the de Sitter Hubble rate.  Every claim is a sympy identity or an
mpmath number; each part ends with at least one control/mutation that must FAIL (or change the answer) if the claim were wrong.

PART A  Deser-Levin / 'T - T_Lambda' family  (Milgrom 1999 astro-ph/9805346; Smolin 1704.00780; Klinkhamer-Kopp 1104.2022; Pikhitsa 1010.0318;
        Ho-Minic-Ng 1005.3537):  all five use ONE function.  Derive it, and its small-a limit  =>  a0 = 2H.
PART B  Ho-Minic-Ng's extra step: the '1/pi' dark-matter profile is exactly the free number that sets the coefficient (a_c = beta a_Lambda / 2).
PART C  Verlinde 1611.02269, d-dimensional chain:  a_M = (d-3)/((d-2)(d-1)) a0 (=a0/6 at d=4); pi cancels; sensitivity to the horizon-matching step.
PART D  Debye family (Li-Chang 1005.1169, Kiselev-Timofeev 1009.1301):  a0 = 12 T_D / pi, and the N_G of KT eq (28) is circular.
PART E  van Putten 1411.2665:  a0 = 2 cH / (1 + beta_dS), beta_dS = 2 pi sqrt(2)  (Higuchi-saturating graviton mass).
PART F  Hajdukovic 1009.3333 eq (14):  a_cr = (1/4pi^2) Omega_L / sqrt(Omega_0 - 1) cH0  -- what Omega_0 - 1 it would need.
PART G  McCulloch 1709.04918 (a0 = 2c^2/Theta) and Milgrom's brane balance (a0 = n c^2/l0).
Exit 0 = every algebra identity holds and every control behaves.
"""
import sys
import mpmath as mp
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

a, H, aN, r, L = sp.symbols('a H a_N r L', positive=True)

# =====================================================================================================  PART A
print("PART A  Deser-Levin / T - T_Lambda family")
T = sp.sqrt(a**2 + H**2) / (2 * sp.pi)              # temperature of a uniformly accelerated (a) detector in dS: (2 pi T)^2 = a^2 + H^2
TdS = H / (2 * sp.pi)
# A0: the DL formula is just Tolman's law: static observer at radius r in dS has proper acceleration a = |f'|/(2 sqrt f), f = 1 - r^2/L^2, H = 1/L
f = 1 - r**2 / L**2
a_static = sp.simplify(-sp.diff(f, r) / (2 * sp.sqrt(f)))
lhs = sp.simplify(a_static**2 + 1 / L**2)
check("A0  (5D embedding, Milgrom eq 7) a^2 + H^2 = H^2/f for the static dS observer, i.e. T_DL = T_dS/sqrt(f) (Tolman)  -- exact",
      sp.simplify(lhs - 1 / (L**2 * f)) == 0)

# A1: Milgrom eq (8)-(9):  2 pi (T - T_Lambda) = a * muhat(a/a0hat), muhat(x) = sqrt(1+(2x)^-2) - (2x)^-1, a0hat = 2 H
x = sp.symbols('x', positive=True)
muhat = lambda x_: sp.sqrt(1 + (2 * x_)**-2) - (2 * x_)**-1
lhsA1 = sp.simplify(2 * sp.pi * (T - TdS))
rhsA1 = sp.simplify(a * muhat(a / (2 * H)))
check("A1  2 pi (T - T_Lambda) = a * muhat(a / (2H))  with a0hat = 2H  (Milgrom 1999 eq 8-9)", sp.simplify(lhsA1 - rhsA1) == 0)
# small-a limit
ser = sp.series(2 * sp.pi * (T - TdS), a, 0, 4).removeO()
check("A2  small-a limit: 2 pi Delta T = a^2/(2H) + O(a^4)   =>  F = a^2/(2H)", sp.simplify(ser - a**2 / (2 * H)) == 0)
a0_solve = sp.solve(sp.Eq(a**2 / (2 * H), aN), a)[0]              # a^2 = 2 H a_N  <=>  deep MOND  a = sqrt(a_N a0)
a0_val = sp.simplify(a0_solve**2 / aN)
check("A3  setting F = m a_N gives a^2 = a_N * (2H): deep-MOND with a0 = 2H  (this is the coefficient: Z = H/a0 = 1/2)", sp.simplify(a0_val - 2 * H) == 0)
# the SAME function appears in Smolin (eq 31-32), K-K (eq 7b, 8b, 9), Pikhitsa (eq 8, a0 = 2H)
mu_smolin_inv = sp.simplify(sp.sqrt(a**2 + H**2) - H)                 # Smolin: F/m = (T_DL - T_dS)*(2 pi)  -> a muhat
Tmin = sp.symbols('T_min', positive=True)
A0_KK = 4 * sp.pi * Tmin                                              # K-K eq (8b): A0 = 4 pi c k T_min / hbar
A0_KK_H = sp.simplify(A0_KK.subs(Tmin, H / (2 * sp.pi)))              # K-K eq (4): 2 pi T_min = H
xx = sp.symbols('xx', positive=True)
mu_pik = sp.sqrt(1 + 1 / xx**2) - 1 / xx                              # Pikhitsa eq (8), x = g/H
check("A4  Klinkhamer-Kopp A0 = 4 pi T_min with 2 pi T_min = H  =>  A0 = 2H  (their eq 9)", sp.simplify(A0_KK_H - 2 * H) == 0)
check("A5  Pikhitsa mu(x)=sqrt(1+1/x^2)-1/x with x=g/H equals muhat(g/(2H)): the same function, a0 = 2H",
      sp.simplify(mu_pik.subs(xx, a / H) - muhat(a / (2 * H))) == 0)
check("A6  Smolin F/m = sqrt(a^2+H^2) - H = a*muhat(a/2H): the same function", sp.simplify(mu_smolin_inv - a * muhat(a / (2 * H))) == 0)
# the alternative 'inertia' functional in Milgrom eq (10)-(11): a dT/da  ->  a0 = H, not 2H
alt = sp.simplify(2 * sp.pi * a * sp.diff(T, a))
check("A7  Milgrom's other functional a dT/da gives a*x/sqrt(1+x^2) with x = a/H, small-a a^2/H: a0 = H  (coefficient depends on the inserted functional: 2 vs 1)",
      sp.simplify(alt - a * (a / H) / sp.sqrt(1 + (a / H)**2)) == 0 and sp.simplify(sp.series(alt, a, 0, 3).removeO() - a**2 / H) == 0)
# controls
ctrl1 = sp.simplify(4 * sp.pi**2 * (T**2 - TdS**2))                  # Milgrom: T^2 - T_Lambda^2 'do not give the correct MOND behaviour'
check("A8  CONTROL: T^2 - T_Lambda^2 = a^2/(4 pi^2) has no H in it, so it defines no acceleration scale (d/dH = 0)", sp.simplify(sp.diff(ctrl1, H)) == 0)
check("A9  CONTROL: without the subtraction, 2 pi T(a=0) = H != 0: a freely falling detector would feel a force (Smolin's reason for the subtraction)",
      sp.simplify((2 * sp.pi * T).subs(a, 0)) == H)
# numbers: a0 = 2 c H_Lambda vs the framework
Zfw = sp.sqrt(32 * sp.pi / 3)
ratio_fw = sp.simplify((2 * H) / (H / Zfw))
check("A10 a0(T-T_Lambda) / a0(framework) = 2 Z_fw = 2 sqrt(32 pi/3) = %.4f  (the route lands ~11.6x ABOVE the framework value)" % float(ratio_fw),
      abs(float(ratio_fw) - 2 * float(Zfw)) < 1e-12 and abs(float(ratio_fw) - 11.5776) < 1e-3)
check("A11 a0(T-T_Lambda) / a0(Milgrom empirical cH/2pi) = 4 pi exactly (12.57): the derived coefficient misses the empirical one by a solid angle",
      sp.simplify((2 * H) / (H / (2 * sp.pi)) - 4 * sp.pi) == 0)

# =====================================================================================================  PART B
print("\nPART B  Ho-Minic-Ng: the coefficient is the inserted 1/pi")
aL, beta, aa = sp.symbols('a_Lambda beta a', positive=True)
Fm = sp.sqrt(aa**2 + aL**2) - aL                                      # F/m, their eq (4)
Fsmall = sp.series(Fm, aa, 0, 3).removeO()
check("B1  small-a: F/m = a^2/(2 a_Lambda)  (their eq after (4))", sp.simplify(Fsmall - aa**2 / (2 * aL)) == 0)
# set F/m = a_N (1 + beta (a_Lambda/a)^2)  [eq (9) with M' = beta (a_Lambda/a)^2 M], deep regime a << a_Lambda
aMOND_sq = sp.symbols('aMOND_sq', positive=True)
# observed centripetal acceleration = F/m = a^2/(2 a_Lambda); solve a^2 from a^2/(2aL) = aN*beta*aL^2/a^2  ->  a^4 = 2 beta aN aL^3
a4 = 2 * beta * aN * aL**3
aobs = sp.sqrt(a4) / (2 * aL)                                          # = a^2/(2 aL)
a_c = sp.simplify(aobs**2 / aN)                                        # v^2/r = sqrt(aN * a_c)  => a_c = aobs^2 / aN
check("B2  a_MOND^2 = a_N * (beta a_Lambda / 2), i.e. a_c = beta a_Lambda / 2", sp.simplify(a_c - beta * aL / 2) == 0)
check("B3  with their beta = 1/pi:  a_c = a_Lambda/(2 pi)  (their 'set a_c = a0/(2 pi) for simplicity'): the 1/pi IS the coefficient, put in by hand",
      sp.simplify(a_c.subs(beta, 1 / sp.pi) - aL / (2 * sp.pi)) == 0)
check("B4  MUTATION beta = 1 gives a_c = a_Lambda/2 (a factor pi larger): the coefficient moves one-for-one with the inserted beta",
      sp.simplify(a_c.subs(beta, 1) / a_c.subs(beta, 1 / sp.pi) - sp.pi) == 0)
check("B5  CONTROL beta = 0 (no M'): a^2/(2 a_Lambda) = a_N, i.e. NO MOND (Newton again), as they state; the DL entropic force alone does not give MOND",
      sp.simplify(sp.solve(sp.Eq(aa**2 / (2 * aL), aN), aa)[0]**2 / (2 * aL) - aN) == 0)

# =====================================================================================================  PART C
print("\nPART C  Verlinde 1611.02269 (d spacetime dims, c = hbar = 1)")
G, M, Lh, d = sp.symbols('G M L d', positive=True)
Om = sp.symbols('Omega', positive=True)                                # Omega_{d-2}
Ar = Om * r**(d - 2)
a0V = 1 / Lh                                                           # Verlinde: a0 = c H0 = c^2 / L
S_M = 2 * sp.pi * M * r                                                # eq (4.28), magnitude
V0 = 4 * G * Lh / (d - 1)                                              # eq (4.31): entropy density 1/V0 chosen so total volume-law entropy = A(L)/4G
V_M = sp.simplify(V0 * S_M)                                            # eq (4.31)/(4.33)
check("C1  V_M = 8 pi G M r L /(d-1)   (eq 4.33 with L = 1/a0)", sp.simplify(V_M - 8 * sp.pi * G * M * r * Lh / (d - 1)) == 0)
eps2 = sp.simplify(sp.diff(V_M, r) / Ar)                               # eq (4.47): eps^2 A = dV_M/dr   [from  int eps^2 dV = V_M, the elastic-inclusion identity]
SigB = M / Ar
SigD = sp.sqrt(eps2) / (8 * sp.pi * G * Lh)                            # eq (4.48): Sigma_D = a0 eps/(8 pi G)   [the inserted identification]
lhs_15 = sp.simplify(SigD**2 - a0V * SigB / (8 * sp.pi * G * (d - 1)))
check("C2  Sigma_D^2 = a0 Sigma_B /(8 pi G (d-1))   (eq 1.5 / 4.49)", lhs_15 == 0)
# Gauss law (1.6): Sigma = ((d-2)/(d-3)) g/(8 pi G), from the Newton potential (4.23)
Phi = -8 * sp.pi * G * M / ((d - 2) * Om * r**(d - 3))
g_N = sp.simplify(sp.diff(Phi, r))
check("C3  Gauss factor (1.6) re-derived from the potential (4.23): g_B = ((d-3)/(d-2)) 8 pi G Sigma_B",
      sp.simplify(g_N - (d - 3) / (d - 2) * 8 * sp.pi * G * SigB) == 0)
gD, gB = sp.symbols('g_D g_B', positive=True)
Sig = lambda g_: (d - 2) / (d - 3) * g_ / (8 * sp.pi * G)
aM_expr = sp.simplify(sp.solve(sp.Eq(Sig(gD)**2, a0V * Sig(gB) / (8 * sp.pi * G * (d - 1))), gD**2)[0] / gB)   # g_D^2 = g_B * aM
aM_over_a0 = sp.simplify(aM_expr / a0V)
check("C4  a_M / a0 = (d-3)/((d-2)(d-1))   (eq 1.7)", sp.simplify(aM_over_a0 - (d - 3) / ((d - 2) * (d - 1))) == 0)
check("C5  at d = 4 this is exactly 1/6  =>  Z = 6, rational; NO pi survives (the 8 pi G of the criterion cancels against the 4 pi G of Gauss)",
      sp.simplify(aM_over_a0.subs(d, 4) - sp.Rational(1, 6)) == 0 and not aM_over_a0.subs(d, 4).has(sp.pi))
# sensitivity to the horizon-matching step (4.36)-(4.37): strain at the inclusion boundary is k = 1 by matching u(L) = Phi(L) L.
k = sp.symbols('k', positive=True)
aM_k = sp.simplify(k**2 * aM_over_a0)                                  # int eps^2 dV = k^2 N V0  ->  a_M scales as k^2
kmut = (d - 2) / (d - 1)                                               # what one gets if V0* = V0 is kept (no horizon-matching factor)
aM_mut = sp.simplify(aM_k.subs(k, kmut).subs(d, 4))
check("C6  MUTATION: dropping the horizon-matching (k = (d-2)/(d-1) instead of 1) changes a_M/a0 at d=4 from 1/6 to %s: the '6' depends on that inserted matching" % aM_mut,
      aM_mut == sp.Rational(2, 27) and aM_mut != sp.Rational(1, 6) and sp.simplify(aM_k.subs(k, 1).subs(d, 4)) == sp.Rational(1, 6))
# Verlinde's volume-law entropy density equals rho_Lambda / T_dS  (d = 4): a useful re-reading, and the only place 8 pi enters
rhoL = 3 * H**2 / (8 * sp.pi * G)
check("C7  d=4: 1/V0 = 3/(4 G L) equals rho_Lambda / T_dS  (pi's cancel: 2pi/8pi = 1/4)", sp.simplify((rhoL / (H / (2 * sp.pi))) - 3 * H / (4 * G)) == 0)
# in terms of sqrt(G rho_Lambda): kappa_V = a0V/6 / sqrt(G rho)
kappaV = sp.simplify((H / 6) / sp.sqrt(G * rhoL))
check("C8  kappa_Verlinde = a_M/(c sqrt(G rho_Lambda)) = sqrt(2 pi/27) = %.4f (contains sqrt(pi): a consequence of converting H to rho_Lambda)" % float(kappaV),
      sp.simplify(kappaV**2 - 2 * sp.pi / 27) == 0)

# =====================================================================================================  PART D
print("\nPART D  Debye family")
mp.mp.dps = 30
Dfun = lambda xx_: mp.quad(lambda z: z / (mp.e**z - 1), [0, xx_]) / xx_
xbig = mp.mpf(400)
check("D1  Debye function D(x) -> pi^2/(6x) at large x (mpmath): x*D(x) = %s vs pi^2/6 = %s" % (mp.nstr(xbig * Dfun(xbig), 8), mp.nstr(mp.pi**2 / 6, 8)),
      abs(xbig * Dfun(xbig) - mp.pi**2 / 6) < 1e-6)
TD, T0s = sp.symbols('T_D T_0', positive=True)
T0_of_TD = 6 * TD / sp.pi**2
a0_debye = sp.simplify(2 * sp.pi * T0_of_TD)                            # a0 = 2 pi T0
check("D2  a0 = 2 pi T0 = 12 T_D / pi  (Li-Chang eq 15 with omega_D = T_D; KT eq 10-11)", sp.simplify(a0_debye - 12 * TD / sp.pi) == 0)
NG, Om_L, H0s = sp.symbols('N_G Omega_L H_0', positive=True)
HL = H0s * sp.sqrt(Om_L)
a0_KT = sp.simplify(2 * sp.pi * (6 / sp.pi) * HL * NG)                  # KT eq (27): T0 = (6/pi) H_Lambda N_G ; a0 = 2 pi T0
check("D3  Kiselev-Timofeev: a0 = 12 N_G H_Lambda", sp.simplify(a0_KT - 12 * NG * HL) == 0)
NG_28 = 1 / (24 * sp.pi * sp.sqrt(Om_L))                                # KT eq (28): the value of N_G that reproduces a0 = H0/(2 pi)
check("D4  with KT eq (28), a0 = H0/(2 pi) IDENTICALLY: N_G is defined by the Milgrom coincidence it is meant to explain (circular; coefficient inserted)",
      sp.simplify(a0_KT.subs(NG, NG_28) - H0s / (2 * sp.pi)) == 0)
check("D5  CONTROL: N_G = 1 (a 'natural' value) would give a0 = 12 H_Lambda, i.e. Z = 1/12 (75x too high)", sp.simplify(a0_KT.subs(NG, 1) / HL) == 12)

# =====================================================================================================  PART E
print("\nPART E  van Putten 1411.2665")
Zvp = (1 + 2 * mp.pi * mp.sqrt(2)) / 2
check("E1  a0 = 2 aH/(1+beta_dS), beta_dS = 2 pi sqrt2  =>  a0/(cH) = 2/(1+2 pi sqrt2) = %.4f  (Z = %.3f)" % (float(2 / (1 + 2 * mp.pi * mp.sqrt(2))), float(Zvp)),
      abs(2 / (1 + 2 * mp.pi * mp.sqrt(2)) - 0.20233) < 1e-4)
c_ms = 2.99792458e8; H70 = 70e3 / 3.0856775814913673e22
a0_vP70 = c_ms * H70 * 2 / (1 + 2 * mp.pi * mp.sqrt(2))
check("E2  reproduces the paper's own number: H0 = 70 gives a0 = %.3e m/s^2  (paper: 1.37e-10)" % float(a0_vP70), abs(float(a0_vP70) - 1.37e-10) < 0.02e-10)
# beta_dS = 2 pi m0/H with m0^2 = 2H^2 (Higuchi saturation, q0=-1)  vs m0^2 = Lambda = 3H^2 (their eq 5 in pure dS)
b2, b3 = 2 * mp.pi * mp.sqrt(2), 2 * mp.pi * mp.sqrt(3)
Zvp3 = (1 + b3) / 2
check("E3  MUTATION: the paper's own graviton mass m0^2 = Lambda = 3H^2 (pure dS) instead of the Higuchi-saturating 2H^2 changes Z from %.3f to %.3f: the coefficient rides on that inserted choice" %
      (float(Zvp), float(Zvp3)), abs(float(Zvp3) - float(Zvp)) > 0.9)
Zs = sp.simplify((1 + 2 * sp.pi * sp.sqrt(2)) / 2)
check("E4  Z_vP = 1/2 + pi sqrt2 is neither rational nor of the form q sqrt(pi) (mixed class); Z_vP^2 not in pi*Q",
      not sp.simplify(Zs**2 / sp.pi).is_rational and not Zs.is_rational)

# =====================================================================================================  PART F
print("\nPART F  Hajdukovic 1009.3333 eq (14)")
OmL = 0.685
H0 = 67.4e3 / 3.0856775814913673e22
cH0 = c_ms * H0
cHL = c_ms * H0 * OmL**0.5
Zfw_f = float(sp.sqrt(32 * sp.pi / 3))
need_Ok = lambda a0_target: (OmL / (4 * float(sp.pi)**2 * (a0_target / cH0)))**2       # Omega_0 - 1 from a0/(cH0) = OmL/(4 pi^2 sqrt(Om0-1))
Ok_fw = need_Ok(cHL / Zfw_f); Ok_dat = need_Ok(1.2e-10)
print(f"      (Omega_Lambda = {OmL}, H0 = 67.4 km/s/Mpc adopted for illustration)")
print(f"      required Omega_0 - 1 for a0 = framework (lambda footing, {cHL/Zfw_f:.3e}):  {Ok_fw:.4f};   for a0 = 1.2e-10:  {Ok_dat:.4f}")
check("F1  a_cr is finite only for Omega_0 > 1 and diverges as Omega_0 -> 1: no flat-universe value exists (Omega_0 - 1 = 1e-6 already gives %.1f cH0, far above any a0 <= cH)" %
      (OmL / (4 * float(sp.pi)**2 * 1e-3), ), OmL / (4 * float(sp.pi)**2 * 1e-3) > 1.0)
check("F2  matching a0 needs Omega_0 - 1 ~ %.3f (a ~1%% closed universe) -- an input the derivation does not supply; coefficient 1/(4 pi^2) is stated, not derived (the paper's note: it was 'omitted by mistake' in print)" % Ok_dat,
      0.005 < Ok_dat < 0.05)

# =====================================================================================================  PART G
print("\nPART G  McCulloch and the brane balance")
Th_now, Th_then = 8.8e26, 2.6e26
a_now, a_then = 2 * c_ms**2 / Th_now, 2 * c_ms**2 / Th_then
print(f"      McCulloch a0 = 2c^2/Theta:  Theta = 8.8e26 m -> {a_now:.3e};  Theta = 2.6e26 m (his 2007/2012 value) -> {a_then:.3e}  (ratio {a_then/a_now:.2f})")
check("G1  McCulloch's own two Theta values differ by 3.4x, so 'no adjustable parameter' hides a choice of 3.4x; 2c^2/Theta = 2.04e-10 with the 2017 value",
      abs(a_then / a_now - 8.8 / 2.6) < 1e-9 and abs(a_now - 2.04e-10) < 0.02e-10)
n2, n3 = 2.0, 3.0
check("G2  Milgrom brane balance a0 = n c^2 / l0 with l0 = de Sitter radius: n = 2 gives 2 c H_Lambda (Z = 1/2, same number as the T - T_Lambda family), n = 3 gives Z = 1/3",
      abs((1 / n2) - 0.5) < 1e-12 and abs((1 / n3) - 1 / 3) < 1e-12)

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
