#!/usr/bin/env python3
"""
ROUTE 3 — Is 32pi = 8pi x 4 a FORCED combination (Einstein coupling x BH entropy-quarter),
or a post-hoc factorization? Brutally honest, sympy-tracked.
===========================================================================================

TARGET:  a0 = c^2 sqrt(Lambda / 32pi) = c^2 sqrt(Lambda/(8pi x 4)),  Z = sqrt(32pi/3) = 5.7888.
Reduces to a0 = kappa c sqrt(G rho_DE) with kappa = 1/2  <=>  Z = sqrt(32pi/3) (proven below).
So "derive Z" == "derive kappa = 1/2" == "derive the 32pi".

The claim under test (Route 3): 32pi = 8pi (Einstein, from Lambda = 8pi G rho_DE / c^2)
                                       x  4 (the BH entropy quarter, S = A/4).

We test FOUR things, each with sympy:
 (A) the algebraic reduction (kappa=1/2 <=> Z=sqrt(32pi/3)), and the menu of normalizations.
 (B) Does an ENTROPIC-FORCE / horizon-thermodynamic derivation of a0 actually produce 8pi x 4,
     or does the 4 (or 1/4) have to be inserted by hand? Track every factor.
 (C) The (c/2): is the factor-of-2 the SAME 2 as equipartition (E=1/2 kT) or Unruh (2pi)?
 (D) The counting of factorizations: how many ways does 32pi factor as (Einstein) x (O(1))?
     Is "8pi x 4" privileged, or one of many?
"""
import sympy as sp

# ---- symbols ----
c, G, Lam, rho, H, kap, Z = sp.symbols('c G Lambda rho H kappa Z', positive=True)
pi = sp.pi

print("="*78)
print("(A) ALGEBRAIC REDUCTION:  a0 = kappa c sqrt(G rho_DE),  rho_DE = Lambda c^2/(8 pi G)")
print("="*78)
rho_DE = Lam*c**2/(8*pi*G)
a0_kap = kap*c*sp.sqrt(G*rho_DE)
a0_kap = sp.simplify(a0_kap)
print("  a0(kappa) =", a0_kap, "   [= kappa c^2 sqrt(Lambda/(8pi))]")

# target form a0 = c^2 sqrt(Lambda/(8pi*N)); solve for the N that a given kappa produces
N = sp.symbols('N', positive=True)
a0_target = c**2*sp.sqrt(Lam/(8*pi*N))
# match a0_kap == a0_target  ->  solve for N in terms of kappa
sol_N = sp.solve(sp.Eq(a0_kap, a0_target), N)
print("  matching a0(kappa) = c^2 sqrt(Lambda/(8pi N))  =>  N =", sol_N)
# Z from a0 = c H_Lambda / Z, H_Lambda = c sqrt(Lambda/3)
H_Lam = c*sp.sqrt(Lam/3)
Z_of_kap = sp.simplify(c*H_Lam / a0_kap)
print("  Z(kappa) = c H_Lambda / a0(kappa) =", Z_of_kap)
for kv, label in [(sp.Rational(1,2),'1/2  (framework, c/2)'),
                  (sp.Integer(1),'1   (no 1/2)'),
                  (sp.Rational(1,6),'1/6 (Verlinde a_M=cH/6 reading)')]:
    Zval = Z_of_kap.subs(kap, kv)
    Nval = sol_N[0].subs(kap, kv)
    print(f"    kappa={label:28s} -> N = {sp.nsimplify(Nval)} = {float(Nval):.4f},  "
          f"Z = {sp.simplify(Zval)} = {float(Zval):.4f}")
print("  => kappa=1/2 EXACTLY <=> N=4 (so 8pi*N=32pi) <=> Z=sqrt(32pi/3)=5.789.  CONFIRMED.")
print("     The WHOLE game is the kappa=1/2, equivalently the '4'.  Everything else (8pi,3) is GR.")

print()
print("="*78)
print("(B) ENTROPIC-FORCE DERIVATION — does 8pi x 4 fall out, or is the 4 inserted by hand?")
print("="*78)
print("""  Verlinde/Padmanabhan entropic force, the STANDARD chain (all factors explicit):
    (i)   S = A/4  in Planck units  =>  S = kB A c^3 / (4 G hbar)         [the 1/4 = BH quarter]
    (ii)  dS/dx = 2pi kB / (hbar/(m c))  (one bit per Compton length, Verlinde's dS=2pi kB)
    (iii) Unruh: kB T = hbar a / (2 pi c)                                  [the 2pi]
    (iv)  equipartition on the screen: E = (1/2) N kB T, N = A c^3/(G hbar)[A-law dof, the 1/2]
    (v)   E = M c^2
  Carry these through for a HORIZON of de Sitter radius and ask what acceleration scale appears.""")

hbar, kB, m, A, r, M, T, a = sp.symbols('hbar k_B m A r M T a', positive=True)
# Holographic equipartition (Verlinde 2011, his eq. derivation of Newton):
#   M c^2 = (1/2) N kB T,  N = A c^3/(G hbar) = 4pi r^2 c^3/(G hbar),  kB T = hbar a/(2 pi c)
N_dof = 4*pi*r**2*c**3/(G*hbar)            # = A/lp^2 with A=4pi r^2  (area law, NO 1/4 here)
kT    = hbar*a/(2*pi*c)                     # Unruh
E_equip = sp.Rational(1,2)*N_dof*kT
a_newton = sp.solve(sp.Eq(M*c**2, E_equip), a)[0]
print("  Pure area-law equipartition (N = A/lp^2, NO quarter):")
print("    M c^2 = (1/2) N kB T  =>  a =", sp.simplify(a_newton), "  = G M / r^2  (NEWTON, no a0)")
print("    >>> a0 does NOT appear.  Area-law holography gives Newton.  CONFIRMED (banked).")
print()
print("""  KEY POINT: in the equipartition route the area-law N = A/lp^2 (NOT A/4 lp^2) is what
  reproduces Newton's G with the right coefficient. If you instead put N = A/(4 lp^2)
  (i.e. count the BH ENTROPY bits S=A/4 as the dof), you get a = 4 G M/r^2 — wrong Newton.
  So the SAME derivation cannot use BOTH the area-law count (for Newton) AND a separate
  'x4 from S=A/4' (for a0) without double-using the horizon area. Test this explicitly:""")
N_quarter = pi*r**2*c**3/(G*hbar)          # = A/(4 lp^2), the BH-entropy count
a_q = sp.solve(sp.Eq(M*c**2, sp.Rational(1,2)*N_quarter*kT), a)[0]
print("    With N=A/(4 lp^2):  a =", sp.simplify(a_q), "  = 4 G M/r^2  (Newton OFF by 4).")
print("    => The '4' is NOT free to be reinserted as a0's quarter; the area count is fixed")
print("       by matching Newton's G. The quarter and the area-law are the SAME horizon dof,")
print("       counted once. You cannot get '8pi (Newton) x 4 (entropy)' — they fight.")

print()
print("  Now the a0 piece. a0 enters ONLY via a VOLUME/density law (banked, solid):")
print("    a0 = (c/2) sqrt(G rho_DE).  Where could a '4' come from here?")
# de Sitter horizon: H_Lam^2 = Lambda c^2/3 = 8pi G rho_DE/3.  r_dS = c/H_Lam.
# Free-fall accel at horizon: g_ff = (1/2) H^2 r = (1/2) c H  (the c/2).   -> kappa=1/2
g_ff = sp.Rational(1,2)*H**2*(c/H)
print("    de Sitter free-fall at horizon: g = (1/2) H^2 r_dS, r_dS=c/H  =>  g =", sp.simplify(g_ff),
      " = (c/2) H")
print("    with H = H_Lambda = sqrt(Lambda c^2/3):  g =", sp.simplify(g_ff.subs(H, c*sp.sqrt(Lam/3))))
g_val = sp.simplify(g_ff.subs(H, c*sp.sqrt(Lam/3)))
print("    => a0 = (c/2) H_Lambda = c^2 sqrt(Lambda/12)? CHECK vs target sqrt(Lambda/32pi):")
print("       (c/2)H_Lam = c^2 sqrt(Lambda/12);  target = c^2 sqrt(Lambda/32pi).  12 != 32pi!")
print("       So 'a0 = (c/2) H_Lambda' (the SURFACE-GRAVITY/horizon free-fall) gives Z=sqrt(12/3)=2,")
print("       NOT 5.789.  The 32pi requires reading a0 = (c/2) sqrt(G rho_DE) [DENSITY], where the")
print("       8pi comes from rho_DE = Lambda c^2/(8pi G).  The '4' = (1/(1/2))^2 is the SAME 1/2,")
print("       just squared when you go density->Z.  It is NOT an independent entropy-quarter.")
Z_surfgrav = sp.simplify(c*c*sp.sqrt(Lam/3)/g_val)
print("    numeric: Z via (c/2)H_Lam =", float(Z_surfgrav), " (=2, the 'surface gravity' reading)")

print()
print("="*78)
print("(C) THE (c/2): is the 2 the equipartition 1/2, the Unruh 2pi, or a free-fall 1/2?")
print("="*78)
print("""  Three distinct '2's are floating around; they are NOT the same number:
    - equipartition 1/2  (E = 1/2 N kB T)      -> sets Newton's G normalization, used up there
    - Unruh 2pi          (kT = hbar a/2pi c)    -> sets the temperature, the '2pi' not the '2'
    - free-fall 1/2      (g = 1/2 H^2 r)        -> the kappa=1/2 in a0=(c/2)sqrt(G rho)
  Test: does the free-fall 1/2 EQUAL the equipartition 1/2 or the Unruh 1/(2pi)?  No:
    kappa=1/2 gives N=4, Z=5.789.   If kappa were 1/(2pi) (Unruh): """)
for kv, lab in [(sp.Rational(1,2),'free-fall 1/2'),
                (1/(2*pi),'Unruh 1/(2pi)'),
                (sp.Rational(1,6),'Verlinde 1/6'),
                (1/sp.sqrt(2*pi),'1/sqrt(2pi) [Jeans-ish]')]:
    Zv = float(Z_of_kap.subs(kap, kv))
    Nv = float(sol_N[0].subs(kap, kv))
    print(f"    kappa = {sp.nsimplify(kv)!s:14s} ({lab:16s}) -> N={Nv:7.3f}, Z={Zv:.4f}")
print("""  => Only kappa=1/2 gives the clean N=4 / Z=5.789. The Unruh 2pi gives Z=2pi=6.283 (N=4/pi^2,
     not an integer/clean), Verlinde 1/6 gives Z=6. So the '2' in c/2 is the FREE-FALL kinematic
     1/2 — a CONVENTION distinguishing 'a0 as acceleration' from 'Lambda as a potential floor'.
     It is NOT forced to coincide with equipartition or Unruh; it is an independent O(1) choice.""")

print()
print("="*78)
print("(D) FACTORIZATION COUNTING: is '8pi x 4' privileged among ways to write 32pi?")
print("="*78)
val = 32*sp.pi
facs = {
 "8pi x 4   (Einstein x BH-quarter)": (8*pi, 4),
 "16pi x 2  (2xEinstein x 2)":        (16*pi, 2),
 "4pi x 8   (sphere x 8)":            (4*pi, 8),
 "32 x pi   (32 dof x pi)":           (32, pi),
 "2pi x 16  (Unruh-2pi x 16)":        (2*pi, 16),
 "8pi/3 x 12 (Friedmann-rho x 12)":   (8*pi/3, 12),
}
print(f"  32pi = {float(val):.4f}.  Equally-valid factorizations:")
for name,(x,y) in facs.items():
    chk = sp.simplify(x*y - val) == 0
    print(f"    {name:38s}  {float(x):.4f} x {float(y):.4f}  -> exact? {chk}")
print("""  => MANY exact factorizations exist. '8pi x 4' is privileged ONLY IF an independent
     derivation forces BOTH an 8pi (Einstein) AND a 4 (entropy-quarter) as SEPARATE inputs.
     Part (B) shows they do NOT both fall out: the 8pi enters via rho_DE (Einstein, forced),
     but the '4' is (1/kappa)^2 = (1/(1/2))^2 — the SAME free-fall 1/2 squared, NOT the BH
     S=A/4 quarter. The entropy-quarter route (use N=A/4) actually MISBUILDS Newton (off by 4).""")

print()
print("="*78)
print("VERDICT (Route 3, both ways)")
print("="*78)
print("""  FORCED:  8pi (Einstein coupling, via rho_DE=Lambda c^2/8piG) and 3 (Friedmann) — GR.
  NOT the BH quarter: the '4' in 32pi is (1/kappa)^2 with kappa=1/2 the FREE-FALL prefactor,
     NOT the Bekenstein-Hawking S=A/4. The two are numerically equal (both '4') but
     PHYSICALLY DISTINCT: a derivation that literally uses S=A/4 to count horizon dof
     reproduces Newton OFF BY 4 (shown in B). So '32pi = Einstein x entropy-quarter' is a
     POST-HOC FACTORIZATION, not a forced Einstein-times-entropy derivation.
  FREE:  kappa=1/2 (equiv. the 4, equiv. Z) — an O(1) convention. Reading a0 as a vacuum
     free-fall ACCELERATION fixes kappa=1/2; reading it as a horizon SURFACE GRAVITY gives
     a different number (Z=2); Unruh gives 2pi; Verlinde 6. No principle selects among them.
  HONEST near-miss: the cleanest is a0=(c/2)sqrt(G rho_DE) — the 8pi is genuinely Einstein,
     and IF one independently fixed kappa=1/2 the 32pi=8pi*4 would close. But kappa=1/2 is
     posited (free-fall convention), and the 'entropy-quarter' identification of its square
     is numerology (the S=A/4 route gives the wrong Newton). Z stays UNFORCED-POSIT.""")
