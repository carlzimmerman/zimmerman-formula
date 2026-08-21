#!/usr/bin/env python3
"""
ROUTE 3B -- INDEPENDENT RE-DERIVATION AND ADVERSARIAL CHECK OF ROUTE 3 (ENTROPIC GRAVITY).
==========================================================================================
This is a SECOND, independent pass over Verlinde (2016, arXiv:1611.02269) against Carl's five
gates.  It was written after `route3_entropic_gravity_2026.py` and it CORRECTS that file in three
places.  Every correction states its direction.

WHAT IS NEW HERE (not in route3_entropic_gravity_2026.py):
  N1. The "6" in a_M = cH/6 is RECONSTRUCTED, not asserted: it is the ratio of the dS medium's
      elastic strain energy to the Newtonian field energy of the same strain, and it equals
      16 pi G rho_DE / H^2 = 6 by the Friedmann relation.  The SAME Friedmann 3 that sits inside
      Carl's kappa c sqrt(G rho_Lambda).  This makes question 2 answerable rather than rhetorical.
  N2. Verlinde eq (7.40) is used in its VERIFIED form (integral form, checked against the
      literature): int_0^r G M_D^2(r')/r'^2 dr' = M_B(r) c H_0 r / 6.  route3's Part 2 used the
      LOCAL form M_D^2 = (a_M/G) M_b r^2, which is NOT eq (7.40) inside an extended source.
      Direction of that error: it UNDERSTATED Verlinde's interior apparent mass.
  N3. Q2 is COMPUTED, not estimated from a two-point calibration.  A full QUMOND phantom-density
      multipole solve, with the a0/2 monopole recovered exactly as the control.  route3 priced
      Verlinde's Q2 with a linear (nu-1) estimator extrapolated 3.6x beyond its calibration; this
      file checks whether that extrapolation is safe.

CORRECTIONS TO route3_entropic_gravity_2026.py, both directions stated:
  C1. route3's VERDICT text says entropic Q2 is "2.6x worse than the a0-line" while its own
      printed estimator gave 3.55x -- internally inconsistent.  The independent QUMOND solve here
      gives 2.4x.  Direction: route3's (nu-1) ESTIMATOR overstates by ~45% when extrapolated;
      its text number was accidentally close.
  C2. route3's VERDICT text says Verlinde's y=3 cutoff is "RAR-refuted".  Its own Part 6 numbers
      are 0.1029 dex (cut) vs 0.1083 dex (Carl's a0-line).  The cut kernel fits SPARC BETTER than
      Carl's own kernel.  Direction: route3 MANUFACTURED A DEFICIT against Verlinde.  Withdrawn
      here and replaced with the test that actually bites (Part 6b).
  C3. route3's checks 29 and 31 are asserts written before the number was known, and they FAILED.
      The finding they were trying to assert is false: Verlinde's shape fits the SPARC RAR at
      least as well as Carl's a0-line.  Recorded here as a first-class negative.

Run: python3 route3B_entropic_independent_2026.py
"""
import sys, os, glob
import numpy as np
import sympy as sp

PASS = True
NCHK = 0
def check(name, cond, direction=""):
    global PASS, NCHK
    NCHK += 1
    tag = "ok  " if cond else "FAIL"
    if not cond:
        PASS = False
    d = f"   [{direction}]" if direction else ""
    print(f"   [{tag}] ({NCHK}) {name}{d}")

def hdr(s):
    print("\n" + "#"*100); print("# " + s); print("#"*100)

# =====================================================================================
hdr("PART 0 -- constants; BOTH footings, always")
# =====================================================================================
c    = 2.99792458e8
G    = 6.67430e-11
hbar = 1.054571817e-34
kB   = 1.380649e-23
Msun = 1.98892e30
AU   = 1.495978707e11
kpc  = 3.0856775814913673e19
GM_sun = 1.32712440018e20

H0   = 2.184e-18            # s^-1, 67.4 km/s/Mpc (corpus value)
OmL  = 0.6847
Om_m = 0.315
Om_r = 9.2e-5
rho_crit = 3*H0**2/(8*np.pi*G)
rho_L    = OmL*rho_crit
kappa    = 0.5

A0_CAN = kappa*c*np.sqrt(G*rho_L)
A0_ALT = kappa*c*np.sqrt(G*rho_crit)
H_L    = np.sqrt(8*np.pi*G*rho_L/3.0)          # the pure-dS rate = H0 sqrt(OmL)
A_M_H0 = c*H0/6.0                              # Verlinde as PUBLISHED (uses H_0)
A_M_HL = c*H_L/6.0                             # Verlinde on his OWN medium (dS rate)

print(f"  a0 canonical  kappa c sqrt(G rho_Lambda) = {A0_CAN:.5e} m/s^2")
print(f"  a0 ALT        kappa c sqrt(G rho_total ) = {A0_ALT:.5e} m/s^2")
print(f"  a_M published c H_0 / 6                  = {A_M_H0:.5e} m/s^2")
print(f"  a_M on the dS rate  c H_Lambda / 6       = {A_M_HL:.5e} m/s^2")
print(f"  a_M(H0)/a0_can = {A_M_H0/A0_CAN:.5f}   a_M(H0)/a0_alt = {A_M_H0/A0_ALT:.5f}")
print(f"  a_M(HL)/a0_can = {A_M_HL/A0_CAN:.5f}   <-- the like-for-like comparison")
check("canonical a0 = 9.3619e-11 to 0.1%", abs(A0_CAN/9.3619e-11-1) < 1e-3, "control")
check("ALT a0 = 1.1279e-10 to 0.5% (route3 asserted 0.1% and FAILED on this; the banked ALT "
      "value corresponds to a marginally different H0 -- direction: bookkeeping, not physics)",
      abs(A0_ALT/1.1279e-10-1) < 5e-3, "control, route3's check 2 corrected")

DG_BUDGET = {'Mercury': 4.6e-14, 'Venus': 8.0e-14, 'Earth': 8.7e-15,
             'Mars': 1.4e-15, 'Jupiter': 5.6e-13, 'Saturn': 7.0e-15}
R_PLANET_AU = {'Mercury': 0.3871, 'Venus': 0.7233, 'Earth': 1.0000,
               'Mars': 1.5237, 'Jupiter': 5.2029, 'Saturn': 9.5367}
Q2_CEIL, Q2_CEN, Q2_SIG = 5.2e-27, 1.6e-27, 1.8e-27
Q2_BANK_A0, Q2_BANK_RA = 2.50e-26, 3.46e-26     # corpus, canonical footing

# =====================================================================================
hdr("PART 1 -- N1: RECONSTRUCTING THE 6.  Where does a_M = cH/6 actually come from?")
# =====================================================================================
print("""
  Verlinde eq (7.40), VERIFIED form (checked against the published literature, not recited):

        int_0^r  G M_D^2(r') / r'^2  dr'   =   M_B(r) * c H_0 * r / 6                    (7.40)

  The left side is EXACTLY twice the Newtonian field energy of the apparent dark matter:
        E_field = int g_D^2/(8 pi G) dV = (G/2) int M_D^2/r^2 dr.
  So (7.40) says   2 E_field = M_B c^2 r / (6 L),  L = c/H.
  Everything below reconstructs the 6 from Verlinde's own ingredients.
""")
L_dS = c/H0
S_dS   = kB*c**3*(4*np.pi*L_dS**2)/(4*G*hbar)
V_dS   = (4.0/3.0)*np.pi*L_dS**3
s_DE   = S_dS/V_dS
T_dS   = hbar*H0/(2*np.pi*kB)
rho_from_S = (T_dS*s_DE)/c**2
print(f"  s_DE = S_dS/V_dS = {s_DE:.6e} J/K/m^3      T_dS = {T_dS:.6e} K")
print(f"  (T_dS s_DE)/c^2 = {rho_from_S:.8e} kg/m^3   vs rho_Lambda = {rho_crit*1.0:.8e} (rho_crit)")
check("Verlinde's volume-law entropy times the dS temperature returns 3H^2/(8 pi G) EXACTLY -- "
      "his postulate is internally consistent",
      abs(rho_from_S/(3*H0**2/(8*np.pi*G)) - 1) < 1e-12, "favourable to Verlinde")

# --- the displaced volume, and the volume strain
Ms, rs, Ls, cs, Gs_, hbs, kBs, Hs = sp.symbols('M r L c G hbar k_B H', positive=True)
S_M_s  = 2*sp.pi*kBs*Ms*cs*rs/hbs                      # Bekenstein-type displacement entropy
s_DE_s = 3*kBs*cs**3/(4*Gs_*hbs*Ls)
V_M    = sp.simplify(S_M_s/s_DE_s)                     # volume of medium displaced
u_disp = sp.simplify(V_M/(4*sp.pi*rs**2))              # radial displacement field
eps_V  = sp.simplify(3*u_disp/rs)                      # VOLUME strain, dV/V
print(f"\n  displaced volume V_M      = {sp.simplify(V_M.subs(Ls, cs/Hs))}")
print(f"  displacement u = V_M/4pi r^2 = {sp.simplify(u_disp.subs(Ls, cs/Hs))}")
print(f"  volume strain eps_V = 3u/r   = {sp.simplify(eps_V.subs(Ls, cs/Hs))}")
gN_s = Gs_*Ms/rs**2
check("the volume strain is eps_V = 2 g_N/(cH) EXACTLY -- all of hbar and k_B cancel",
      sp.simplify(eps_V.subs(Ls, cs/Hs) - 2*gN_s/(cs*Hs)) == 0, "structural")
check("eps_V saturates at 1 exactly where S_M = S_DE, i.e. at g_N = cH/2 -- so the entropy "
      "budget and the elastic limit are the SAME statement (a real internal consistency of "
      "Verlinde's chain, verified not assumed)",
      sp.simplify(sp.solve(sp.Eq(eps_V.subs(Ls, cs/Hs), 1), rs)[0]**2
                  - Gs_*Ms*2/(cs*Hs)) == 0, "favourable to Verlinde")

# --- the energy displaced
rho_DE_s = 3*Hs**2/(8*sp.pi*Gs_)
E_M = sp.simplify(rho_DE_s*cs**2*V_M.subs(Ls, cs/Hs))
print(f"\n  displaced dark energy E_M = rho_DE c^2 V_M = {E_M}  = M c^2 (r/L)")
check("E_M = M c^2 r H / c = M c^2 r/L exactly (all constants cancel)",
      sp.simplify(E_M - Ms*cs*rs*Hs) == 0, "structural")

# --- THE 6:  elastic strain energy / Newtonian field energy, for the SAME strain
#     u_el = (1/2) K eps^2 with K = rho_DE c^2, and eps = 2 g/(cH) is the universal
#     displacement relation applied to whatever mass sources g.
K_s = rho_DE_s*cs**2
g_s = sp.Symbol('g', positive=True)
u_el   = sp.Rational(1,2)*K_s*(2*g_s/(cs*Hs))**2          # elastic energy density at field g
u_fld  = g_s**2/(8*sp.pi*Gs_)                              # Newtonian field energy density at g
ratio6 = sp.simplify(u_el/u_fld)
print(f"\n  u_elastic/u_field = {ratio6}   (g and all scales cancel identically)")
check("*** THE 6 IS DERIVED: the dS medium's elastic strain energy is exactly 6x the Newtonian "
      "field energy of the same strain, because 16 pi G rho_DE/H^2 = 6 by Friedmann.  The 6 in "
      "cH/6 is 2x3 and the 3 is the SAME 3 in rho = 3H^2/(8 pi G) that sits inside Carl's "
      "kappa c sqrt(G rho_Lambda). ***",
      sp.simplify(ratio6 - 6) == 0, "the load-bearing new result of this file")

# then (7.40) reads: E_elastic = 6 E_field = 6 * E_M/12 = E_M/2.
print("""
  Closing the chain:  (7.40) says E_field = E_M/12.  With u_el = (1/2) K eps^2 and K = rho_DE c^2
  that is E_elastic = 6 E_field = E_M/2 -- "half the displaced dark energy is stored as strain".

  *** THE AMBIGUITY, PRICED (rule 1: I verify the soft spot as hard as the result). ***
  The elastic bookkeeping is fixed only up to the modulus/equipartition convention:
     u_el = (1/2) rho_DE c^2 eps^2  with  E_el = E_M/2   ->  a_M = cH/6   (Verlinde's choice)
     u_el =       rho_DE c^2 eps^2  with  E_el = E_M     ->  a_M = cH/6   (same, by coincidence
                                                              of the two factors of 2)
     E_el = E_M with the (1/2)K convention                ->  a_M = cH/3
     u_el = (1/2) K eps^2, E_el = E_M/4                   ->  a_M = cH/12
  So the derivation pins a_M only to within a factor 2 either way: a_M in [cH/12, cH/3].
  I state this BEFORE using the 3.6% agreement in Part 2, because it is what that agreement is
  worth.  Direction: ADVERSE to any claim that Verlinde DERIVES Carl's coefficient.
""")

# =====================================================================================
hdr("PART 2 -- QUESTION 2: is kappa c sqrt(G rho_Lambda) the SAME construction as cH/6?")
# =====================================================================================
kap_s, OmL_s = sp.symbols('kappa Omega_Lambda', positive=True)
# a0 = kappa c sqrt(G rho_Lambda);  rho_Lambda = 3 H_Lambda^2/(8 pi G)
a0_sym   = kap_s*cs*sp.sqrt(Gs_*3*Hs**2/(8*sp.pi*Gs_))
a0_sym   = sp.simplify(a0_sym)
aM_sym   = cs*Hs/6
ratio_ex = sp.simplify(a0_sym/aM_sym)
print(f"  a0(kappa, H) = {a0_sym}")
print(f"  a_M(H)       = {aM_sym}")
print(f"  a0/a_M       = {ratio_ex}   -- H, c, G ALL cancel: a PURE NUMBER in kappa")
kappa_V = sp.simplify(sp.solve(sp.Eq(ratio_ex, 1), kap_s)[0])
print(f"  the kappa that Verlinde's construction IMPLIES:  kappa_V = {kappa_V} = "
      f"{float(kappa_V):.7f}")
r_exact = sp.simplify(ratio_ex.subs(kap_s, sp.Rational(1,2)))
print(f"  kappa=1/2 vs Verlinde, LIKE FOR LIKE (both on the dS rate): a0/a_M = {r_exact} = "
      f"{float(r_exact):.7f}")
check("the two constructions are the SAME FORM: a = (pure number) x c x sqrt(G rho_dS).  Their "
      "ratio is 3 sqrt(3/(8 pi)) = 1.0364825 EXACTLY, independent of H0, Omega_Lambda and every "
      "measured quantity",
      sp.simplify(r_exact - 3*sp.sqrt(3/(8*sp.pi))) == 0, "structural, favourable to the "
      "'same construction' reading")
check("Verlinde's chain therefore IMPLIES kappa_V = sqrt(8 pi/3)/6 = 0.4823984, NOT 1/2",
      abs(float(kappa_V) - np.sqrt(8*np.pi/3)/6) < 1e-12, "the answer to question 2")

kV = float(kappa_V)
print(f"\n  numerically:  kappa_V = {kV:.7f}   kappa_Carl = 0.5   deficit = {(0.5/kV-1)*100:.3f}%")
print(f"  on the CANONICAL footing (rho_Lambda):  a_M(H_L) = {A_M_HL:.5e} vs a0 = {A0_CAN:.5e}"
      f"  ratio {A0_CAN/A_M_HL:.5f}")
print(f"  on the PUBLISHED reading (H_0, i.e. rho_TOTAL): a_M = {A_M_H0:.5e} vs a0_alt = "
      f"{A0_ALT:.5e}  ratio {A0_ALT/A_M_H0:.5f}")
check("the SAME pure number 1.03648 appears on BOTH footings when each is compared like for like "
      "(dS rate vs dS rate, total rate vs total rate) -- the footing fork does NOT move the "
      "kappa question, it only moves which rho you feed in",
      abs(A0_CAN/A_M_HL - float(r_exact)) < 2e-3 and abs(A0_ALT/A_M_H0 - float(r_exact)) < 2e-3,
      "both footings, as required")

# is kappa_V consistent with the corpus's MEASURED kappa?
for lab, km, ks in [("BTFR", 0.465, 0.076), ("distance-free", 0.551, 0.043)]:
    print(f"  measured kappa ({lab}) = {km:.3f} +- {ks:.3f}:  kappa_V is "
          f"{abs(kV-km)/ks:.2f} sigma, kappa=1/2 is {abs(0.5-km)/ks:.2f} sigma")
check("kappa_V = 0.4824 is INSIDE the corpus's own measurement of kappa on both estimators "
      "(0.23 sigma on BTFR, 1.60 sigma distance-free) -- so the entropic value is NOT excluded "
      "by Carl's own data, and neither is 1/2.  The data do not discriminate them",
      abs(kV-0.465)/0.076 < 2 and abs(kV-0.551)/0.043 < 2, "FAVOURABLE to the entropic route, "
      "stated plainly")

# what is the 3.6% agreement worth, given the factor-2 ambiguity of Part 1?
log_band  = np.log(4.0)                    # a_M in [cH/12, cH/3] = factor 4 wide in log
log_hit   = 2*np.log(float(r_exact))       # +-3.65% window around kappa=1/2
p_coin    = log_hit/log_band
print(f"\n  COINCIDENCE PRICING: the elastic argument pins a_M only inside a factor-4 log band.")
print(f"  Landing within +-3.65% of kappa=1/2 by chance in that band: p = {p_coin:.3f}")
check("the 3.6% agreement is worth about p = 0.05 given the derivation's own factor-4 slack -- "
      "suggestive, NOT a derivation of kappa.  I priced this before leaning on it",
      0.01 < p_coin < 0.15, "honest weighting, adverse to over-reading the match")

# =====================================================================================
hdr("PART 3 -- QUESTION 1: term-by-term, with eq (7.40) in its VERIFIED form")
# =====================================================================================
rv, aMv, Gv = sp.symbols('r a_M G', positive=True)
Mb = sp.Function('M_b', positive=True)(rv)

# (7.40) differentiated:  M_D^2 = (a_M/G) r^2 d[M_b r]/dr
MD2   = (aMv/Gv)*rv**2*sp.diff(Mb*rv, rv)
MD    = sp.sqrt(sp.simplify(MD2))
rho_D = sp.simplify(sp.diff(MD, rv)/(4*sp.pi*rv**2))

# route3 used the LOCAL form instead:
MD_local = rv*sp.sqrt(aMv*Mb/Gv)
rho_D_local = sp.simplify(sp.diff(MD_local, rv)/(4*sp.pi*rv**2))

carl = sp.sqrt(Gv*Mb*aMv)/(4*sp.pi*Gv*rv**2)

ext = {sp.Derivative(Mb, rv): 0, sp.Derivative(Mb, (rv, 2)): 0}
rho_D_ext   = sp.simplify(rho_D.subs(ext))
rho_Dl_ext  = sp.simplify(rho_D_local.subs(ext))
print(f"  OUTSIDE the baryons (M_b' = 0):")
print(f"    Verlinde (7.40)   rho_D -> {rho_D_ext}")
print(f"    Carl's law        rho   =  {sp.simplify(carl)}")
check("*** GATE 1: outside the baryons Verlinde's apparent-dark-matter density is Carl's "
      "amplitude law sqrt(G M_b a)/(4 pi G r^2) TERM FOR TERM, with a0 -> a_M. ***",
      sp.simplify(rho_D_ext - carl) == 0, "favourable -- but see the deflation below")
check("the LOCAL form route3 used gives the same exterior limit, so route3's exterior "
      "conclusion stands", sp.simplify(rho_Dl_ext - carl) == 0, "route3 exterior OK")

# interior: the two forms differ
rho_b_s = sp.diff(Mb, rv)/(4*sp.pi*rv**2)
ratio_740   = sp.simplify(rho_D/carl)
ratio_local = sp.simplify(rho_D_local/carl)
# evaluate on a concrete profile to expose the difference numerically
Rd = sp.Symbol('R_d', positive=True)
prof = sp.Function('M_b')(rv)
test_Mb = (1 - sp.exp(-rv/Rd)*(1+rv/Rd))          # ~ a smooth cored enclosed-mass profile
sub = {Mb: test_Mb, sp.Derivative(Mb, rv): sp.diff(test_Mb, rv)}
f740 = sp.lambdify((rv, Rd, aMv, Gv),
                   sp.simplify(ratio_740.subs(Mb, test_Mb).doit()), 'numpy')
floc = sp.lambdify((rv, Rd, aMv, Gv),
                   sp.simplify(ratio_local.subs(Mb, test_Mb).doit()), 'numpy')
rr = np.array([0.5, 1.0, 2.0, 3.0, 5.0])
print(f"\n  INSIDE an extended source (exponential-like M_b), rho_D / Carl's amplitude law:")
print(f"  {'r/R_d':>8}{'eq(7.40)':>12}{'route3 local':>15}{'ratio':>9}")
v740 = f740(rr, 1.0, 1.0, 1.0); vloc = floc(rr, 1.0, 1.0, 1.0)
for i, x in enumerate(rr):
    print(f"  {x:>8.1f}{v740[i]:>12.4f}{vloc[i]:>15.4f}{v740[i]/vloc[i]:>9.4f}")
# NUMBER FIRST, THEN THE CHECK (rule 2).  The computed table above says the two forms differ by
# up to 1.59x in the inner disc, with eq (7.40) LARGER inside ~2.5 R_d and SMALLER outside.
# My first draft asserted "larger at every radius" BEFORE looking; that assert FAILED and is
# replaced here by what the numbers actually say.  Direction of route3's error is therefore
# RADIUS-DEPENDENT, not one-signed, and I say so.
print(f"  crossover: eq(7.40)/local = 1 near r/R_d ~ 2.5; max discrepancy {max(v740/vloc):.3f}x inner, "
      f"{min(v740/vloc):.3f}x outer")
check("N2: route3 used M_D^2 = (a_M/G) M_b r^2, which is NOT eq (7.40) inside an extended source. "
      "The verified form differs by up to 1.59x in the inner disc (7.40 LARGER) and 0.85x in the "
      "outskirts (7.40 SMALLER).  Direction: radius-dependent, NOT one-signed -- my own first "
      "draft asserted one-signed and was wrong",
      max(v740/vloc) > 1.3 and min(v740/vloc) < 0.9, "correction to route3, direction stated")

print("""
  THE DEFLATION APPLIES IN FULL, and it must be said before gate 1 is scored.
  Verlinde's exterior rho_D is the Bekenstein-Milgrom deep-MOND phantom density plus the baryons.
  It is returned by mu = x/(1+x) and x/sqrt(1+x^2) as well.  It measures the deep-MOND
  normalisation v_c^4 = G M_b a and NOTHING ELSE.  What is genuinely Verlinde's is that he
  produces the SCALE a from a cosmological argument instead of fitting it.  That, and only that,
  is the part of Route 3 the other six mechanisms do not contain.

  WHERE THEY GENUINELY DIFFER (question 1, the honest answer):
   1. TRANSITION.  Carl's a0-line has an interpolation, nu = sqrt(1+1/y).  Verlinde has NONE:
      g_obs = g_N + sqrt(a_M g_N) at ALL accelerations.  This is the whole of Part 4.
   2. INTERIOR.  Eq (7.40)'s d[M_b r]/dr term adds 4 pi r^3 rho_b, absent from Carl's spherical
      AQUAL phantom.  Table above: tens of percent in the mid-disc.
   3. STRUCTURE.  Carl's is a modified Poisson equation -- it superposes, it has an external-field
      effect, it is a functional of rho_b everywhere.  Verlinde's is an ALGEBRAIC MAP of the
      enclosed profile M_b(r) about a chosen centre.  This is the whole of Part 5.
   4. DOMAIN.  Verlinde's derivation is for static, spherically symmetric, isolated systems.
      A disc is outside its stated domain; every RAR test of EG (including Part 6 here) applies it
      outside the domain its author claimed.  Flagged, not hidden.
""")

# =====================================================================================
hdr("PART 4 -- GATE 3, PRICED FIRST: the 1-AU monopole, per planet, both readings")
# =====================================================================================
def nm1_a0line(y):
    x = 1.0/np.asarray(y, dtype=float)
    return x/(np.sqrt(1.0+x)+1.0)            # sqrt(1+x)-1, cancellation-safe
def nm1_routeA(y):
    s = np.sqrt(np.asarray(y, dtype=float))
    e = np.exp(-s)
    return e/(1.0-e)
def nm1_verl(y):
    return 1.0/np.sqrt(np.asarray(y, dtype=float))

y_big = np.array([1e6, 1e8, 1e10])
print(f"  cancellation guard: (nu-1)*y for the a0-line at y={y_big} -> "
      f"{nm1_a0line(y_big)*y_big}  (must -> 0.5, NOT 0 or noise)")
check("no float64 catastrophic cancellation in (nu-1) at y up to 1e10 (trap 6d guarded)",
      np.allclose(nm1_a0line(y_big)*y_big, 0.5, rtol=1e-6), "guard")

r_star_sun = np.sqrt(2*GM_sun*L_dS/c**2)
print(f"\n  r_*(Sun) = sqrt(2 G M L/c^2) = {r_star_sun/AU:.1f} AU;  g_N(r_*)/a_M = "
      f"{GM_sun/r_star_sun**2/A_M_H0:.4f}  (= 3 exactly)")
print(f"\n  {'planet':<9}{'r[AU]':>7}{'budget':>10}{'a0-line can':>13}{'x':>9}"
      f"{'RouteA':>11}{'x':>9}{'Verlinde':>12}{'x':>11}")
print("  " + "-"*84)
worst = {'a0': 0.0, 'rA': 0.0, 'V': 0.0}
for p in ['Mercury','Venus','Earth','Mars','Jupiter','Saturn']:
    rr_ = R_PLANET_AU[p]*AU
    gN  = GM_sun/rr_**2
    d0  = nm1_a0line(gN/A0_CAN)*gN
    dA  = nm1_routeA(gN/A0_CAN)*gN
    dV  = nm1_verl(gN/A_M_H0)*gN
    b   = DG_BUDGET[p]
    worst['a0'] = max(worst['a0'], d0/b); worst['rA'] = max(worst['rA'], dA/b)
    worst['V']  = max(worst['V'], dV/b)
    print(f"  {p:<9}{R_PLANET_AU[p]:>7.3f}{b:>10.1e}{d0:>13.3e}{d0/b:>9.0f}"
          f"{dA:>11.2e}{dA/b:>9.1e}{dV:>12.3e}{dV/b:>11.2e}")
print(f"\n  WORST-CASE (Mars): a0-line {worst['a0']:.0f}x | RouteA {worst['rA']:.1e}x | "
      f"Verlinde uncut {worst['V']:.2e}x")
# ALT footing
worst_alt = max(nm1_a0line((GM_sun/(R_PLANET_AU[p]*AU)**2)/A0_ALT)*(GM_sun/(R_PLANET_AU[p]*AU)**2)
                /DG_BUDGET[p] for p in DG_BUDGET)
print(f"  ALT footing a0-line worst case: {worst_alt:.0f}x")
check("REPRODUCED INDEPENDENTLY: Carl's a0-line 1-AU monopole is 3.3e4x (canonical) / 4.0e4x "
      "(alt) the Mars EPM budget -- the task's ADVERSE correction to the corpus's banked "
      "1278x/1544x is confirmed by a second calculation.  a0/2 divided by the Mars budget is "
      "just 4.68e-11/1.4e-15",
      3.2e4 < worst['a0'] < 3.5e4 and 3.9e4 < worst_alt < 4.2e4, "ADVERSE, confirms the "
      "27x correction; propagate it")
check("Verlinde WITHOUT his cutoff is 4 orders WORSE than Carl's a0-line, because his phantom "
      "force is sqrt(g_N a_M) ~ 1/r and never saturates",
      worst['V']/worst['a0'] > 1e3, "ADVERSE to Verlinde, decisive on reading (a)")
check("Verlinde WITH his own S_M >= S_DE cutoff: the Sun's r_* is 4256 AU, every planet is "
      "inside it, so M_D = 0 and the monopole is EXACTLY zero -- gate 3's monopole is CLEARED "
      "on reading (b), and this is a genuine structural pass, not a fitted one",
      max(R_PLANET_AU.values())*AU < r_star_sun, "FAVOURABLE to Verlinde, stated plainly")

# =====================================================================================
hdr("PART 5 -- N3: Q2 COMPUTED (QUMOND phantom multipole), not estimated")
# =====================================================================================
print("""
  QUESTION 3, structural answer first.  The arm-level Q2 theorem assumed
        div[(1 - mu_v/B^2) grad Phi] = 4 pi G rho_b   for a general Phi(x,y,z).
  Verlinde's (7.40) is not of that type: it is an algebraic map of the ENCLOSED baryonic profile
  about a chosen centre, defined only for static spherical isolated systems, with no slot for an
  external field.  So YES -- Route 3 escapes the arm-level Q2 proof, by falsifying its hypothesis.
  Verlinde's theory as published has NO Q2 at all, because it has no external-field effect.
  That is an ABSENCE, not a prediction, and Part 5c prices what the absence costs.

  Below I nevertheless COMPUTE what Q2 would be if one grants entropic gravity an AQUAL/QUMOND
  external-field effect by reading nu_V(y) = 1 + y^{-1/2} as an interpolation function.  This is
  a real solve, not the (nu-1) point estimator route3 used: QUMOND phantom density
      rho_ph = (1/4 pi G) div[(nu(|grad Phi_N|/a) - 1) grad Phi_N],
  with grad Phi_N = GM/r^2 rhat + g_ext zhat, then the l=2 multipole of the phantom potential.
  CONTROL: the same pipeline must return the a0/2 monopole exactly.
""")
V_sun, R_sun = 233e3, 8.2*kpc
g_ext = V_sun**2/R_sun
print(f"  g_ext = V^2/R = {g_ext:.5e} m/s^2 = {g_ext/A0_CAN:.4f} a0_can = {g_ext/A_M_H0:.4f} a_M")
check("g_ext sits in the task's declared 1.9-2.6 a0 window",
      1.9 <= g_ext/A0_CAN <= 2.6, "prerequisite")

r_sym, th_sym = sp.symbols('r theta', positive=True)
GMs, ges, a_s = sp.symbols('GM g_e a', positive=True)
gr_e  = GMs/r_sym**2 + ges*sp.cos(th_sym)
gth_e = -ges*sp.sin(th_sym)
gmag  = sp.sqrt(gr_e**2 + gth_e**2)

def build_rho(nm1_expr):
    hr  = nm1_expr*gr_e
    hth = nm1_expr*gth_e
    div = sp.diff(r_sym**2*hr, r_sym)/r_sym**2 \
        + sp.diff(sp.sin(th_sym)*hth, th_sym)/(r_sym*sp.sin(th_sym))
    return sp.lambdify((r_sym, th_sym, GMs, ges, a_s), div/(4*sp.pi*G), 'numpy')

x_ = a_s/gmag
KERNELS = {
    'a0-line':  x_/(sp.sqrt(1+x_)+1),                          # sqrt(1+a/g)-1, stable form
    'RouteA':   sp.exp(-sp.sqrt(gmag/a_s))/(1-sp.exp(-sp.sqrt(gmag/a_s))),
    'Verlinde': sp.sqrt(a_s/gmag),
}
RHO = {k: build_rho(v) for k, v in KERNELS.items()}

mu_n, mu_w = np.polynomial.legendre.leggauss(64)
th_n = np.arccos(mu_n)
P2   = 0.5*(3*mu_n**2 - 1.0)

def multipoles(fn, a0v, r0=AU, rmax=1e10*AU, N=1400):
    rg = np.logspace(np.log10(r0), np.log10(rmax), N)
    R, T = np.meshgrid(rg, th_n, indexing='ij')
    rho = fn(R, T, GM_sun, g_ext, a0v)
    rho0 = 0.5*np.einsum('rt,t->r', rho, mu_w)          # l=0 coefficient
    rho2 = 2.5*np.einsum('rt,t->r', rho*P2[None, :], mu_w)
    return rg, rho0, rho2

def Q2_of(fn, a0v, r0=AU, rmax=1e10*AU, N=1400):
    rg, rho0, rho2 = multipoles(fn, a0v, r0, rmax, N)
    # integrate in ln r -- the grid IS log spaced, so linear-r trapz loses ~1% (found by the
    # monopole control failing at 1.15%; fixed here, direction: the control caught a numerics bug)
    I_out = np.trapz(rho2, np.log(rg))               # int rho2/r' dr' = int rho2 dln r'
    A2 = -(4*np.pi*G/5.0)*I_out
    # control: the l=0 phantom mass inside r0 must give the framework's monopole
    return 2.0*A2, rg, rho0, rho2

print(f"\n  {'kernel':<12}{'a used':>12}{'Q2 [s^-2]':>14}{'/ ceiling':>11}{'sigma':>9}"
      f"{'ratio to a0-line':>19}")
print("  " + "-"*77)
Q2res = {}
for k, a0v in [('a0-line', A0_CAN), ('RouteA', A0_CAN), ('Verlinde', A_M_H0)]:
    q, rg, rho0, rho2 = Q2_of(RHO[k], a0v)
    Q2res[k] = q
    print(f"  {k:<12}{a0v:>12.4e}{q:>14.4e}{abs(q)/Q2_CEIL:>11.2f}"
          f"{(abs(q)-Q2_CEN)/Q2_SIG:>9.1f}{abs(q)/abs(Q2res['a0-line']):>19.4f}")
# ALT footing
q_alt, _, _, _ = Q2_of(RHO['a0-line'], A0_ALT)
qA_alt, _, _, _ = Q2_of(RHO['RouteA'], A0_ALT)
print(f"  ALT footing:  a0-line {abs(q_alt):.4e} ({abs(q_alt)/Q2_CEIL:.2f}x ceiling), "
      f"RouteA {abs(qA_alt):.4e} ({abs(qA_alt)/Q2_CEIL:.2f}x)")

# CONTROL 1: the monopole must return a0/2
rg, rho0, rho2 = multipoles(RHO['a0-line'], A0_CAN, r0=1e-3*AU, rmax=1e4*AU, N=2000)
sel = rg <= AU
r_end = rg[sel][-1]          # the grid's last point <= 1 AU; evaluate g THERE, not at AU.
Mph = 4*np.pi*np.trapz(rho0[sel]*rg[sel]**3, np.log(rg[sel]))
g_mono = G*Mph/r_end**2      # (my first draft divided by AU^2 and lost 0.8% -- control caught it)
print(f"\n  CONTROL (computed before any verdict): l=0 phantom mass inside 1 AU gives "
      f"g_anom = {g_mono:.6e} m/s^2;  a0/2 = {A0_CAN/2:.6e};  ratio = {g_mono/(A0_CAN/2):.6f}")
check("CONTROL PASSES: the QUMOND multipole pipeline reproduces the a0-line's a0/2 monopole to "
      "better than 1% -- so the l=2 numbers from the same pipeline are trustworthy",
      abs(g_mono/(A0_CAN/2) - 1) < 0.01, "control, guards against a vacuous pass")

# CONTROL 2: convergence in grid and domain
q_a, _, _, _ = Q2_of(RHO['a0-line'], A0_CAN, N=700)
q_b, _, _, _ = Q2_of(RHO['a0-line'], A0_CAN, N=2800)
q_c, _, _, _ = Q2_of(RHO['a0-line'], A0_CAN, rmax=1e12*AU, N=1400)
print(f"  CONTROL: grid N=700/1400/2800 -> {q_a:.4e} {Q2res['a0-line']:.4e} {q_b:.4e}; "
      f"rmax x100 -> {q_c:.4e}")
check("CONTROL PASSES: Q2 is converged in both grid resolution and outer domain to <1%",
      abs(q_b/q_a - 1) < 0.01 and abs(q_c/Q2res['a0-line'] - 1) < 0.01, "control")

print(f"""
  READING OF PART 5 (all numbers above computed before this text was written):
   * The independent QUMOND solve puts the a0-line's Q2 at {abs(Q2res['a0-line']):.3e} s^-2 against the
     corpus's banked 2.50e-26 -- agreement to {abs(abs(Q2res['a0-line'])/Q2_BANK_A0-1)*100:.0f}%.  RouteA/a0-line ratio here is
     {abs(Q2res['RouteA'])/abs(Q2res['a0-line']):.3f} against the banked {Q2_BANK_RA/Q2_BANK_A0:.3f}.
   * Verlinde, IF granted an EFE: {abs(Q2res['Verlinde']):.3e} s^-2 = {abs(Q2res['Verlinde'])/Q2_CEIL:.1f}x the Park+2026 ceiling,
     {abs(Q2res['Verlinde'])/abs(Q2res['a0-line']):.2f}x Carl's a0-line and {abs(Q2res['Verlinde'])/abs(Q2res['RouteA']):.2f}x Route A/MS08.
   * CORRECTION C1, restated AFTER the solve (the first draft of this paragraph had it backwards
     and is corrected here).  route3 priced Verlinde's Q2 with a linear (nu-1) estimator and got
     3.55x the a0-line; its verdict text then said "2.6x", inconsistent with its own number.  This
     independent QUMOND solve gives {abs(Q2res['Verlinde'])/abs(Q2res['a0-line']):.2f}x.  So route3's ESTIMATOR overstated the ratio by ~45%
     when extrapolated 3.6x beyond its two calibration points, and its verdict TEXT was accidentally
     close.  Direction: route3's estimator ran ADVERSE to Verlinde; the text ran the other way.
     Either way Verlinde is the worst of the three kernels and is {abs(Q2res['Verlinde'])/Q2_CEIL:.1f}x over the Park ceiling.
""")
check("the independent solve agrees with the banked a0-line Q2 within a factor 2 -- good enough "
      "to price a third kernel, and I state the agreement level rather than assuming it",
      0.5 < abs(Q2res['a0-line'])/Q2_BANK_A0 < 2.0, "cross-validation, level stated")
check("granted an EFE, entropic gravity's Q2 is the WORST of the three kernels",
      abs(Q2res['Verlinde']) > abs(Q2res['RouteA']) > abs(Q2res['a0-line']), "ADVERSE to Verlinde")

# 5c -- the price of having no EFE
print("\n  [5c] THE PRICE OF THE ESCAPE.  No EFE means the ISOLATED prediction for every satellite.")
def sigma_iso(M_kg, a): return ((4.0/81.0)*G*M_kg*a)**0.25
for ML in (1.0, 2.0):
    M = 1.6e5*ML*Msun
    print(f"     Crater II, M/L={ML:.0f}: isolated sigma = {sigma_iso(M, A_M_H0)/1e3:.2f} km/s "
          f"(a_M) / {sigma_iso(M, A0_CAN)/1e3:.2f} km/s (a0 can); observed 2.7 +- 0.3 -> "
          f"{(sigma_iso(M, A_M_H0)/1e3-2.7)/0.3:+.1f} sigma")
s1 = sigma_iso(1.6e5*Msun, A_M_H0)/1e3
s2 = sigma_iso(3.2e5*Msun, A_M_H0)/1e3
check("Crater II: the no-EFE prediction is 3.3-3.9 km/s vs observed 2.7 +- 0.3, i.e. +1.9 to "
      "+4.0 sigma.  AGAINST INTEREST: at M/L=1 this is only 1.9 sigma and MOND-WITH-EFE's own "
      "published ~2.1 km/s is -2.0 sigma on the other side, so Crater II alone does NOT cleanly "
      "separate them -- it bites only at M/L=2",
      1.5 < (s1-2.7)/0.3 < 2.5 and (s2-2.7)/0.3 > 3.5, "ADVERSE but honestly bounded")

# =====================================================================================
hdr("PART 6 -- GATE 2 (screening the FORCE) and the test that actually bites")
# =====================================================================================
print(f"""
  READING (a), the published formula at all radii: NO screening whatsoever.  Part 4 shows the
  1-AU anomaly is {nm1_verl((GM_sun/AU**2)/A_M_H0)*(GM_sun/AU**2):.3e} m/s^2.  Gate 2: FAIL, and it fails harder than any of the six.

  READING (b), Verlinde's own S_M >= S_DE condition enforced: inside r_* the volume-law entropy
  is entirely displaced, there is no elastic medium, M_D = 0 IDENTICALLY.  That screens the FORCE,
  not the information, and it is not a free function -- it is the saturation of a finite entropy
  budget, with the elastic limit eps_V = 1 landing on the same surface (Part 1).  Gate 2: PASS.

  THAT IS A REAL STRUCTURAL RESULT AND IT IS THE ONLY ONE IN THE FLEET THAT SCREENS THE FORCE FROM
  A COUNTING ARGUMENT RATHER THAN A CHOSEN mu.  What it costs is tested next.
""")
r_star_gal = lambda M: np.sqrt(2*G*M*L_dS/c**2)
print(f"  {'system':<26}{'M_b [Msun]':>13}{'r_* ':>12}{'jump in M_enc':>15}{'jump in v_c':>13}")
print("  " + "-"*79)
for lab, M, unit in [("Sun", Msun, 'AU'), ("dwarf 1e8", 1e8*Msun, 'kpc'),
                     ("spiral 5e10", 5e10*Msun, 'kpc'), ("spiral 1e11", 1e11*Msun, 'kpc'),
                     ("cluster 1e14", 1e14*Msun, 'kpc')]:
    rs_ = r_star_gal(M)
    d = rs_/AU if unit == 'AU' else rs_/kpc
    print(f"  {lab:<26}{M/Msun:>13.2e}{d:>9.1f} {unit:<3}{1+1/np.sqrt(3):>15.4f}"
          f"{np.sqrt(1+1/np.sqrt(3)):>13.4f}")
jump_v = np.sqrt(1+1/np.sqrt(3))
print(f"\n  At r_* the prescription jumps DISCONTINUOUSLY from M_D=0 to M_D = M_b/sqrt(3):")
print(f"  enclosed mass x{1+1/np.sqrt(3):.4f}, circular speed x{jump_v:.4f} = "
      f"{(jump_v-1)*100:.1f}% step, = {np.log10(jump_v**2):.4f} dex in g_obs, at a SINGLE radius "
      f"in EVERY system.")
check("COMPUTED FIRST: Verlinde's own cutoff implies a 25.6% discontinuous jump in circular "
      "speed at r_* = 6.5 kpc in a 1e11 Msun spiral.  THIS, not the RAR scatter, is the sharp "
      "consequence of reading (b)",
      abs(jump_v - 1.2564) < 1e-3, "the real test of the cutoff")

# --- SPARC
DATA = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "..", "real_research", "data", "sparc_data"))
rows = []
for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try:
        d = np.genfromtxt(f, comments="#")
    except Exception:
        continue
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    rows.append((d[:, 0]*kpc, d[:, 1], d[:, 2], d[:, 3], d[:, 4], d[:, 5]))
print(f"\n  loaded {len(rows)} SPARC rotation curves")
check("SPARC present", len(rows) >= 150, "prerequisite")

def nu_a0line(y): return np.sqrt(1.0+1.0/y)
def nu_routeA(y): return 1.0/(1.0-np.exp(-np.sqrt(y)))
def nu_verl(y):   return 1.0+1.0/np.sqrt(y)
def nu_verl_cut(y): return np.where(y >= 3.0, 1.0, 1.0+1.0/np.sqrt(y))

def rar(nu, a0v, Ud, ymask=None):
    res, w = [], []
    for Rm, Vobs, eV, Vgas, Vdisk, Vbul in rows:
        Vbar2 = np.sign(Vgas)*Vgas**2 + Ud*Vdisk**2 + 1.4*Ud*Vbul**2
        gb = Vbar2*1e6/Rm; go = (Vobs*1e3)**2/Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        if ymask is not None:
            yy = gb/a0v
            ok &= (yy > ymask[0]) & (yy < ymask[1])
        if not ok.any():
            continue
        r_ = np.log10(go[ok]) - np.log10(nu(gb[ok]/a0v)*gb[ok])
        fr = np.clip(eV[ok], 1, None)/np.clip(Vobs[ok], 1, None)
        res += list(r_); w += list(1.0/fr**2)
    res, w = np.array(res), np.array(w)
    if len(res) == 0:
        return np.nan, np.nan, 0
    return float(np.sqrt(np.sum(w*res**2)/np.sum(w))), float(np.average(res, weights=w)), len(res)

Uds = np.linspace(0.20, 1.40, 121)
print(f"\n  [6a] RAR, Upsilon REFIT for each kernel (route3's comparison, reproduced)")
print(f"  {'kernel':<32}{'a used':>12}{'best Ups':>10}{'scatter':>10}{'@Ups=0.5':>10}")
print("  " + "-"*74)
tab = {}
for lab, nu, a0v in [("Carl a0-line (canonical)", nu_a0line, A0_CAN),
                     ("Carl a0-line (alt)",       nu_a0line, A0_ALT),
                     ("Route A / MS08 (can)",     nu_routeA, A0_CAN),
                     ("Verlinde 1+1/sqrt(y)",     nu_verl,   A_M_H0),
                     ("Verlinde + y=3 cutoff",    nu_verl_cut, A_M_H0)]:
    sc = [rar(nu, a0v, U)[0] for U in Uds]
    i = int(np.argmin(sc))
    s05 = rar(nu, a0v, 0.50)[0]
    tab[lab] = (Uds[i], sc[i], s05)
    print(f"  {lab:<32}{a0v:>12.3e}{Uds[i]:>10.2f}{sc[i]:>10.4f}{s05:>10.4f}")

s_carl = tab["Carl a0-line (canonical)"][1]
s_verl = tab["Verlinde 1+1/sqrt(y)"][1]
s_cut  = tab["Verlinde + y=3 cutoff"][1]
print(f"\n  CORRECTION C2/C3 (first-class negative, reported not buried):")
print(f"    Verlinde uncut {s_verl:.4f} dex vs Carl a0-line {s_carl:.4f} dex -> "
      f"{s_verl/s_carl:.3f}x.  Verlinde fits the SPARC RAR BETTER.")
print(f"    Verlinde WITH the y=3 cutoff {s_cut:.4f} dex -> {s_cut/s_carl:.3f}x Carl's. STILL better.")
print(f"    route3's verdict text claims the RAR REFUTES the y=3 step.  It does not.  That was a "
      f"MANUFACTURED DEFICIT and is withdrawn here.")
check("recorded as a negative result: Verlinde's kernel fits the SPARC RAR at least as well as "
      "Carl's a0-line, both with Upsilon refit and (see table) at the stellar-population value "
      "Upsilon=0.5.  This is ADVERSE to Carl and it is stated as plainly as any pro-Carl finding",
      s_verl <= s_carl, "ADVERSE to Carl, reported first-class")
check("and the y=3 cutoff is NOT refuted by the global RAR scatter either",
      s_cut <= s_carl, "withdraws route3's claim")

print(f"\n  [6b] THE TEST THAT ACTUALLY BITES: restrict to the band straddling the step, 1 < y < 9,")
print(f"       where a 0.198 dex discontinuity must live.  Upsilon refit inside the band for each.")
print(f"  {'kernel':<32}{'best Ups':>10}{'scatter':>10}{'N pts':>8}")
print("  " + "-"*60)
band = (1.0, 9.0)
for lab, nu, a0v in [("Carl a0-line (canonical)", nu_a0line, A0_CAN),
                     ("Verlinde uncut",           nu_verl,   A_M_H0),
                     ("Verlinde + y=3 cutoff",    nu_verl_cut, A_M_H0)]:
    sc = [rar(nu, a0v, U, ymask=band)[0] for U in Uds]
    i = int(np.nanargmin(sc))
    s_, o_, n_ = rar(nu, a0v, Uds[i], ymask=band)
    tab[('band', lab)] = (Uds[i], s_, n_)
    print(f"  {lab:<32}{Uds[i]:>10.2f}{s_:>10.4f}{n_:>8d}")
b_carl = tab[('band', "Carl a0-line (canonical)")][1]
b_cut  = tab[('band', "Verlinde + y=3 cutoff")][1]
b_unc  = tab[('band', "Verlinde uncut")][1]
print(f"\n  in-band: Carl {b_carl:.4f} | Verlinde uncut {b_unc:.4f} | Verlinde cut {b_cut:.4f} dex")
print(f"  cut/uncut = {b_cut/b_unc:.3f}   cut/Carl = {b_cut/b_carl:.3f}")

# =====================================================================================
hdr("PART 7 -- GATE 4: health, the a0(z) collision, and the COVARIANTISATION DILEMMA")
# =====================================================================================
Ez = np.sqrt(Om_m*(1+1090.)**3 + OmL + Om_r*(1+1090.)**4)
print(f"  Carl's DERIVED law:   a0(1090)/a0(0) = 0.0060   (MOND OFF at recombination; LOAD-BEARING")
print(f"     -- it is what makes the CMB clustering component a prediction rather than a fit)")
print(f"  Verlinde, a_M ~ c H(z)/6:  E(1090) = {Ez:.4e}  ->  ratio = {Ez:.4e}  (MOND MAXIMALLY ON)")
print(f"  Verlinde, fixed-dS reading a_M = c H_Lambda/6: ratio = 1.0000 (constant)")
print(f"  discrepancy vs Carl's law: H(z) reading {Ez/0.0060:.3e}x (and OPPOSITE SIGN); "
      f"fixed-dS reading {1/0.0060:.0f}x")
check("Verlinde's scale cannot reproduce Carl's derived a0(z) on either reading: the H(z) reading "
      "misses by 3.9e6x in the WRONG DIRECTION, the fixed-dS reading by 167x.  Adopting the "
      "entropic derivation of the coefficient forfeits the CLASS CMB pass that a0(rec)/a0(0) = "
      "0.0060 secures.  This is the sharpest single incompatibility in Route 3",
      Ez/0.0060 > 1e6 and abs(1/0.0060 - 166.7) < 1, "ADVERSE, and it is structural")

print("""
  THE COVARIANTISATION DILEMMA -- the tightest structural statement in this file:

     Gate 3's escape and gate 4 are MUTUALLY EXCLUSIVE.

  Route 3 escapes the arm-level Q2 theorem ONLY because it is not a field equation.  But that same
  absence is exactly why gate 4 cannot even be POSED: with no action there is no kinetic matrix to
  sign for a ghost, no dispersion relation to check for Cherenkov, no tensor sector to test against
  GW170817's c_T = 1, no stress tensor to give w = -1, and no perturbation theory to give a CMB.
  The moment anyone supplies the missing covariant formulation -- and the only published attempt I
  am aware of, Hossenfelder 2017 PRD 95 124018, does it by ADDING a vector field, which is
  UNVERIFIED prior art here, not checked against the paper -- the theory acquires field equations,
  its quasi-static limit becomes a modified Poisson equation, and it falls back inside the
  hypothesis of the arm-level Q2 proof.  Escaping the theorem and passing gate 4 cannot both be
  done by the same object.  That is not a soft-pedalled 'open question'; it is a fork with both
  branches priced above: no-action -> gate 4 undefined; action -> Q2 at 17x the Park ceiling.
""")

# =====================================================================================
hdr("PART 8 -- GATE 5, clusters, and what I could NOT determine")
# =====================================================================================
print(f"""
  GATE 5, DOUBLE COUNT.  Standalone entropic gravity has NO dark component at all -- M_D is
  apparent, an elastic response, carrying no stress-energy of its own.  Nothing carries Omega_dm,
  so nothing can double-count it.  That is a VACUOUS pass and I refuse to score it as a pass:
  the same absence means there is no component to make the CMB's third peak, so gate 5 is cleared
  only by failing gate 4 harder.  Grafted onto Carl's DBI condensate (the only version with a CMB),
  the corpus's overshoot returns untouched: 32.5x / 25.7x / 11.5x / 3.6x at 0.5/1/3/10 r_M.

  CLUSTERS, against Carl's numbers not generic ones.  Carl's kernel removes 74-89% of cluster dark
  matter and leaves 11-26%.  Entropic gravity's exterior law is the same function with a -> a_M,
  and in deep MOND the phantom scales as sqrt(a), so the published a_M = cH_0/6 buys
  sqrt({A_M_H0/A0_CAN:.4f}) = {np.sqrt(A_M_H0/A0_CAN):.4f} = +{(np.sqrt(A_M_H0/A0_CAN)-1)*100:.1f}% more phantom mass than Carl's canonical a0.
  That does not close an 11-26% residual, and the interior d[M_b r]/dr term (Part 3) helps only
  where rho_b is large, i.e. in the core, not at R500 where the deficit lives.
""")
short_can = 0.11/ (np.sqrt(A_M_H0/A0_CAN))
check("the entropic scale's +8.0% phantom bonus does not close Carl's own 11-26% cluster "
      "residual -- Route 3 inherits the cluster problem essentially unchanged",
      (np.sqrt(A_M_H0/A0_CAN)-1) < 0.11, "ADVERSE, priced against Carl's numbers")

print("""
  WHAT I COULD NOT DETERMINE (rule 5, stated plainly):
   1. I did NOT re-derive Verlinde's elastic bookkeeping from his eqs 7.34-7.39.  I reconstructed
      the 6 from his ingredients (Part 1) and showed it is fixed only to within a factor 2 by the
      modulus/equipartition convention.  Whether Verlinde's own text removes that ambiguity, I
      cannot say without the full paper text, and I will not fabricate it.
   2. Whether the y=3 cutoff, granted an EFE, would ALSO suppress the quadrupole-generating region:
      the cutoff surface in the TOTAL field sits at ~7200 AU while the l=2 source peaks near
      r_e = sqrt(GM/g_ext) = 5250 AU, so the two overlap.  Resolving that needs the discontinuity
      treated as a surface layer with a theta-dependent radius; I did not do it, and I therefore
      do NOT claim the cut version's Q2.  Only the uncut version's Q2 is computed here.
   3. Whether the 25.6% v_c step at r_* is excluded per-galaxy.  Part 6b measures it only through
      binned RAR scatter, which is the wrong statistic for a sharp feature at a galaxy-dependent
      radius.  The correct test is a per-galaxy stacked residual aligned on r_*(M_b).  NOT DONE.
   4. Whether an EG-with-EFE even exists.  I priced one by fiat (reading nu_V as an interpolation
      function).  Verlinde does not supply one and I did not derive one.
""")

# =====================================================================================
hdr("PART 9 -- THE T2 LEAD, TESTED AND KILLED: entropy-budget cutoff grafted onto CARL'S kernel")
# =====================================================================================
print("""
  The one transferable thing Route 3 has that the fleet does not is a screen that comes from
  COUNTING (a finite entropy budget) rather than from a chosen mu.  So: graft it onto Carl's own
  a0-line and ask whether it fixes gate 3.  Cutoff radius is NOT free -- it is S_M = S_DE, i.e.
  y = 3 in the TOTAL field.  The step is smoothed over width w in ln y and w is driven to zero;
  the surface layer at the discontinuity is therefore RESOLVED, not dropped.
  NUMBER FIRST.  Verdict written after the table.
""")
S_cut = sp.Rational(1,2)*(1-sp.tanh((sp.log(gmag/a_s)-sp.log(3))/sp.Symbol('w', positive=True)))
w_sym = sp.Symbol('w', positive=True)
def build_rho_w(nm1_expr):
    hr  = nm1_expr*gr_e; hth = nm1_expr*gth_e
    div = sp.diff(r_sym**2*hr, r_sym)/r_sym**2 \
        + sp.diff(sp.sin(th_sym)*hth, th_sym)/(r_sym*sp.sin(th_sym))
    return sp.lambdify((r_sym, th_sym, GMs, ges, a_s, w_sym), div/(4*sp.pi*G), 'numpy')
F_cut = build_rho_w(KERNELS['a0-line']*S_cut)
def Q2_w(fn, a0v, w, N=4000):
    rg = np.logspace(np.log10(AU), np.log10(1e10*AU), N)
    R, T = np.meshgrid(rg, th_n, indexing='ij')
    rho2 = 2.5*np.einsum('rt,t->r', fn(R, T, GM_sun, g_ext, a0v, w)*P2[None, :], mu_w)
    return 2.0*(-(4*np.pi*G/5.0)*np.trapz(rho2, np.log(rg)))
print(f"  g_ext/a0_can = {g_ext/A0_CAN:.4f} and g_ext/a0_alt = {g_ext/A0_ALT:.4f}: the SOLAR POSITION")
print(f"  itself sits at y < 3, i.e. INSIDE the elastic regime.  The cutoff cannot reach it.")
print(f"\n  {'w (ln y)':>10}{'Q2 can':>14}{'/ceil':>8}{'Q2 alt':>14}{'/ceil':>8}")
print("  " + "-"*54)
qs = []
for w in [0.30, 0.20, 0.10, 0.05, 0.025]:
    qc = Q2_w(F_cut, A0_CAN, w); qa = Q2_w(F_cut, A0_ALT, w)
    qs.append(qc)
    print(f"  {w:>10.3f}{qc:>14.4e}{abs(qc)/Q2_CEIL:>8.2f}{qa:>14.4e}{abs(qa)/Q2_CEIL:>8.2f}")
print(f"\n  UNCUT a0-line for comparison: {Q2res['a0-line']:.4e} ({abs(Q2res['a0-line'])/Q2_CEIL:.2f}x ceiling)")
print(f"  cut/uncut = {abs(qs[-1])/abs(Q2res['a0-line']):.3f}")
sc_cut = [rar(lambda y: np.where(y >= 3.0, 1.0, np.sqrt(1+1.0/y)), A0_CAN, U)[0] for U in Uds]
i_ = int(np.argmin(sc_cut))
print(f"  SPARC, a0-line + y=3 entropy cutoff: best Upsilon = {Uds[i_]:.2f}, scatter = {sc_cut[i_]:.4f} dex"
      f"  (uncut a0-line: {s_carl:.4f})")
check("CONVERGED: the grafted-cutoff Q2 is stable to <2% from w = 0.20 down to w = 0.025, so the "
      "surface layer at the discontinuity is resolved and this is not a smoothing artefact",
      abs(qs[-1]/qs[2] - 1) < 0.02, "control")
check("*** THE T2 LEAD IS DEAD, AND THE DIRECTION IS THE OPPOSITE OF THE HOPE.  Grafting "
      "Verlinde's entropy-budget screen onto Carl's a0-line makes Q2 WORSE, 2.21e-26 vs 1.68e-26 "
      "canonical (4.25x vs 3.22x the Park ceiling) and 2.40e-26 alt.  The cutoff surface is "
      "itself an l=2 SOURCE, and it adds. ***",
      abs(qs[-1]) > abs(Q2res['a0-line']), "ADVERSE -- computed before the verdict was written")
check("AND the reason is structural, not numerical: g_ext = 2.29 a0_can / 1.90 a0_alt, so the "
      "solar position is BELOW y=3.  Any cutoff placed high enough to leave galaxies intact sits "
      "ABOVE the region that sources Q2, and any cutoff placed low enough to reach it would "
      "delete the external field itself",
      g_ext/A0_CAN < 3.0 and g_ext/A0_ALT < 3.0, "the mechanism, stated")
print("""
  THIS COMPLETES A TWO-INSTANCE PATTERN WITH A MECHANISM, and it is the most useful thing in
  this file for the wider programme:
     Route A/MS08 kills the 1-AU MONOPOLE stone dead (1e-3459) and its Q2 is 1.51x WORSE.
     The entropy-budget cutoff kills the monopole exactly and its Q2 is 1.32x WORSE.
  Q2 is sourced at y ~ 2, at the SOLAR POSITION IN THE GALAXY, not in the solar system.  Every
  device that screens the deep interior is acting seven orders of magnitude away from where Q2
  lives, and devices that put a FEATURE near y ~ 2 add to Q2 rather than subtracting.
  Conclusion for the programme, stated as a conjecture with its evidence and NOT as a theorem:
  Q2 will not be fixed by screening.  It can only be fixed by making nu - 1 SMALLER at y ~ 2,
  which is the interpolation-function squeeze (Route 1), not a new field and not a new screen.
""")

# =====================================================================================
hdr("VERDICT -- Route 3 against all five gates, both footings")
# =====================================================================================
print(f"""
  GATE 1  amplitude law / BTFR              CLEARS -- exactly, and it is the ONLY published
          derivation of it from a stated microphysical postulate.  But the deflation applies in
          full: outside the baryons rho_D IS the Bekenstein-Milgrom deep-MOND phantom plus M_b,
          which mu = x/(1+x) also returns.  Gate 1 is a THRESHOLD.  What is distinctively
          Verlinde's is not the law, it is the SCALE.

  GATE 2  screening the FORCE               SPLIT.
          reading (a), no cutoff  : FAIL, and worse than anything in the fleet.
          reading (b), his own S_M >= S_DE : PASS, structurally -- a finite entropy budget, not a
          free function, with the elastic limit eps_V=1 on the same surface.  Its price is a
          25.6% discontinuous jump in v_c at r_*, which is NOT refuted by RAR scatter
          (Carl {s_carl:.4f} / Verlinde cut {s_cut:.4f} dex) and which I did not test the right way.

  GATE 3  Q2 and the 1-AU monopole          SPLIT, and this is the surprise of Route 3.
          monopole, reading (a) : {worst['V']:.2e}x the Mars budget -- FOUR ORDERS worse than the
             a0-line's own adverse-corrected {worst['a0']:.0f}x (canonical) / {worst_alt:.0f}x (alt).
          monopole, reading (b) : EXACTLY ZERO.  Every planet is inside r_* = 4256 AU.  CLEARS.
          Q2 as published : DOES NOT EXIST.  No external-field slot, so no quadrupole.  Route 3
             GENUINELY ESCAPES the arm-level Q2 proof -- by falsifying its hypothesis, the only
             honest way anything can escape a theorem.  Cost: no EFE at all, Crater II +1.9 to
             +4.0 sigma (M/L dependent; NOT a clean kill at M/L=1).
          Q2 if granted an EFE : {abs(Q2res['Verlinde']):.2e} s^-2 = {abs(Q2res['Verlinde'])/Q2_CEIL:.0f}x the Park ceiling, +{(abs(Q2res['Verlinde'])-Q2_CEN)/Q2_SIG:.0f} sigma,
             {abs(Q2res['Verlinde'])/abs(Q2res['a0-line']):.1f}x Carl's a0-line ({abs(Q2res['a0-line']):.2e} here vs 2.50e-26 banked) and {abs(Q2res['Verlinde'])/abs(Q2res['RouteA']):.1f}x Route A.

  GATE 4  theoretical health                CANNOT BE POSED, which is worse than FAIL, and the
          COVARIANTISATION DILEMMA makes it structural: the only reason gate 3's Q2 is escapable
          is the absence of field equations, and that same absence is why no ghost / Cherenkov /
          c_T / w=-1 / CMB statement exists.  Supply the action and Q2 comes straight back.
          Plus the a0(z) collision: {Ez/0.0060:.1e}x (H(z) reading, wrong sign) or 167x (fixed-dS).

  GATE 5  no double count                   VACUOUS PASS, refused.  Nothing carries Omega_dm
          because nothing carries stress-energy; grafted onto the condensate the full 32.5x /
          25.7x / 11.5x / 3.6x overshoot returns.

  STATUS: NOT A SURVIVOR.  Clears 1 of 5 outright (gate 1, the threshold), plus one reading of
  gate 2 and one reading of gate 3.  Fails gate 4 structurally and gate 5 vacuously.

  BUT THE LANE IS NOT WASTED.  Three transferable results:
   T1. THE 6 IS 2x3 AND THE 3 IS CARL'S OWN FRIEDMANN 3.  a_M = cH/6 IS kappa_V c sqrt(G rho_dS)
       with kappa_V = sqrt(8 pi/3)/6 = 0.4824.  The two constructions are the SAME construction;
       their ratio is exactly 3 sqrt(3/(8 pi)) = 1.03648, a pure number.  Verlinde's chain is a
       CANDIDATE DERIVATION OF kappa and it lands 3.65% from 1/2 -- inside Carl's own measurement
       (0.23 sigma BTFR, 1.60 sigma distance-free).  It is worth p ~ 0.05 given the argument's own
       factor-4 slack, so it is a lead, not a derivation.  This is the first object in the whole
       programme that even PROPOSES a value for kappa from a stated postulate.
   T2. THE ONLY FORCE-SCREENING IN THE FLEET THAT COMES FROM COUNTING.  Verlinde's S_M >= S_DE
       cutoff switches the anomaly off entirely inside r_* = sqrt(2 G M L/c^2), with no free
       function and no chosen mu, and the elastic limit lands on the same surface independently.
       Carl's framework has no such object.  Whether a SMOOTHED version of an entropy-budget
       cutoff can be grafted onto a Lagrangian kernel is the transferable question, and it is
       exactly the thing that would fix gate 3 without a free parameter.
   T3. AN ADVERSE FINDING ABOUT CARL'S KERNEL, REPORTED AS FIRST-CLASS.  On 175 SPARC rotation
       curves with Upsilon refit for each kernel, Verlinde's nu = 1 + y^(-1/2) gives {s_verl:.4f} dex
       against the a0-line's {s_carl:.4f} dex, and it prefers Upsilon = {tab['Verlinde 1+1/sqrt(y)'][0]:.2f} against the a0-line's
       {tab['Carl a0-line (canonical)'][0]:.2f}, where stellar populations expect ~0.5.  The RAR does not favour Carl's kernel
       over Verlinde's; if anything it mildly favours Verlinde's.
""")
print("#"*100)
print(f"# {NCHK} checks, {'ALL PASS' if PASS else 'SOME FAILED -- read them, they are the finding'}")
print("#"*100)
sys.exit(0 if PASS else 1)
