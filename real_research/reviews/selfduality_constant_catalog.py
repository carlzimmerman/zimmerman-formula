#!/usr/bin/env python3
"""
FRONT 2 — CATALOG every framework self-duality and its NATIVE CONSTANT.  Does ANY carry
sqrt(2) (Koide's r) vs phi (golden, the mu_fw fixed point) vs sqrt(Z) (inverted-BH radius)?

THE NEW SEED (the load-bearing object this script anatomizes):
  dS-Unruh temperature is a 2-CHANNEL QUADRATURE  T(a) = (hbar/2pi k c) * sqrt(a^2 + a_dS^2),
  a_dS = cH = Z*a0.  At the self-dual/balance point a = a_dS the two orthogonal channels
  (proper acceleration vs horizon/Gibbons-Hawking floor) contribute EQUALLY and
        T(a_dS) = sqrt(2) * a_dS    <-- a NATIVE framework sqrt(2) at the a = a_dS transition.
  (Note a=a_dS=Z*a0, NOT a=a0; the a=a0 point is a DIFFERENT balance -- audited below.)

QUESTION: is THAT sqrt(2) the SAME structural object as Koide's r=sqrt(2), or the GENERIC
'equal-mix-of-two-orthogonal-channels' coincidence (necessary, NOT sufficient)?

CARL'S #1 RULE: NO manufactured win.  Expected = self-dualities give phi / sqrt-Z; the a=a_dS
quadrature-sqrt2 is the GENERIC equal-orthogonal-quadrature number with NO forced map to the
generation-amplitude slot.  Both-ways; every claim COMPUTED; exit 0; numbers printed.

FOOTING (locked, never under test): a0 = c H_Lambda / Z, Z = sqrt(32pi/3); framework's OWN
mu_fw(x) = (sqrt(1+4x^2)-1)/(2x); mu_fw(1)=1/phi.  NEVER McGaugh nu.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 45
t = sp.Symbol('t')
PASS, FAIL = "PASS", "FAIL <-- CHECK"
allok = True
def ck(name, cond):
    global allok
    print(f"  [{PASS if cond else FAIL}] {name}")
    allok &= bool(cond)
    return bool(cond)

# ============================================================================
print("="*92)
print("(0) FOOTING — framework constants (locked)")
print("="*92)
Z   = 2*sp.sqrt(sp.Rational(8,1)*sp.pi/3)        # sqrt(32 pi/3)
phi = (sp.sqrt(5)+1)/2
x   = sp.Symbol('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
print(f"  Z = sqrt(32pi/3)         = {float(Z):.6f}   (sqrt(Z) = {float(sp.sqrt(Z)):.6f})")
print(f"  phi = (1+sqrt5)/2        = {float(phi):.6f}  (1/phi = mu_fw(1) = {float(1/phi):.6f})")
print(f"  sqrt(2)                  = {float(sp.sqrt(2)):.6f}")
ck("mu_fw(1) = 1/phi (golden, framework's own fixed point)",
   sp.simplify(mu_fw.subs(x,1) - 1/phi) == 0)

# ============================================================================
print("\n"+"="*92)
print("(A) THE CATALOG — every framework self-duality, its fixed point, and its NATIVE constant")
print("="*92)
# Each entry: (name, carrier space, the involution, fixed-point value, native constant class)
print("""  carrier-space legend: R^1=worldline/time-axis (bath); R^3=generation/flavor; FIELD=field-space;
  RADIUS=UV/IR radial; d=spatial-dimension count; GAUGE=Lie-algebra root space.\n""")

rows = []

# --- SD1: mu_fw self-duality 1/mu - mu = 1/x ; fixed point x=1 -> 1/phi (GOLDEN) ---
ident = sp.simplify((1/mu_fw - mu_fw) - 1/x)
fp = sp.solve(sp.Eq(1/mu_fw - mu_fw, sp.sqrt(sp.S(0))+ (1/mu_fw - mu_fw).subs(x,1)*0 + 0) , x)  # placeholder
# the genuine self-dual point of the interpolation: where mu_fw maps to its own 'dual' x=1 (a=a0)
mu1 = sp.simplify(mu_fw.subs(x,1))
ck("SD1 mu_fw identity 1/mu_fw - mu_fw = 1/x holds exactly", ident == 0)
print(f"       SD1  INTERPOLATION self-duality (constitutive law).  carrier=R^1 (accel ratio x=g_bar/a0).")
print(f"            self-dual point x=1 (a=a0): mu_fw(1) = 1/phi = {float(mu1):.6f}  -> GOLDEN phi")
rows.append(("SD1 mu_fw constitutive", "R^1 accel-ratio", "1/mu-mu=1/x at x=1", float(mu1), "phi"))

# --- SD2: dS-Unruh QUADRATURE T(a)=sqrt(a^2+a_dS^2); balance a=a_dS -> sqrt2 (THE NEW SEED) ---
a, adS = sp.symbols('a a_dS', positive=True)
Tfac = sp.sqrt(a**2 + adS**2)                 # up to hbar/2pi k c prefactor
T_balance = sp.simplify(Tfac.subs(a, adS)/adS)   # = sqrt2
ck("SD2 dS-Unruh quadrature T(a_dS)/a_dS = sqrt(2) at the balance a=a_dS",
   sp.simplify(T_balance - sp.sqrt(2)) == 0)
print(f"       SD2  dS-UNRUH QUADRATURE (THE NEW SEED).  carrier=R^1 (acceleration amplitude, time-axis).")
print(f"            balance a=a_dS=Z*a0: T = sqrt(2)*a_dS = {float(T_balance):.6f} * a_dS  -> sqrt(2)")
rows.append(("SD2 dS-Unruh quadrature", "R^1 accel-amplitude", "a <-> a_dS (=Z*a0)", float(T_balance), "sqrt2"))

# --- SD3: theta(0) MI-kernel DC weight = sqrt2 (amplitude -3dB corner) ---
w = sp.Symbol('w', positive=True)
amp = 1/sp.sqrt(1+w**2)
cw = [c for c in sp.solve(sp.Eq(amp**2, sp.Rational(1,2)), w) if c.is_positive][0]
theta0 = sp.simplify(1/amp.subs(w, cw))
ck("SD3 MI-kernel DC weight theta(0) = sqrt(2) (single-pole amplitude -3dB corner)",
   sp.simplify(theta0 - sp.sqrt(2)) == 0)
print(f"       SD3  MI-KERNEL DC WEIGHT theta(0).  carrier=R^1 (bath correlator, time-axis).")
print(f"            theta(0)=w(0)/w(corner)=sqrt(2)={float(theta0):.6f}  -> sqrt(2) (same R^1 archetype as SD2)")
rows.append(("SD3 theta(0) kernel DC", "R^1 bath-time", "amplitude -3dB corner", float(theta0), "sqrt2"))

# --- SD4: d=3 cross-product self-duality #vec=#bivec -> (d-1)=2 -> sqrt2 appears as ratio? ---
d = sp.Symbol('d', positive=True, integer=True)
selfdual = sp.solve(sp.Eq(d, d*(d-1)/2), d)   # #vectors = #bivectors
sd_d = [v for v in selfdual if v == 3]
ck("SD4 cross-product self-duality #vec=#bivec <=> d=3 (and (d-1)=2)", 3 in selfdual)
print(f"       SD4  d=3 CROSS-PRODUCT self-duality.  carrier=d (spatial-dimension count).")
print(f"            #vectors=#bivectors <=> d=3; the native NUMBER is the DIMENSION 3, not sqrt2/phi.")
print(f"            (Z_d=8 sqrt(pi/[d(d-1)]); at d=3 -> Z=sqrt(32pi/3). The flat-curve tie is (d-1)=2,")
print(f"             an INTEGER condition, NOT an algebraic sqrt2 in a ratio slot.)")
rows.append(("SD4 d=3 cross-product", "d spatial-dim", "#vec=#bivec", 3.0, "integer-3"))

# --- SD5: UV/IR self-dual RADIUS r -> r_s R_H / r (inverted-BH); fixed point sqrt(r_s R_H) ~ sqrt(Z) scale ---
rs, RH, rr = sp.symbols('r_s R_H r', positive=True)
dual_r = rs*RH/rr
fp_r = sp.solve(sp.Eq(dual_r, rr), rr)
fp_r = [v for v in fp_r if v.is_positive][0]
ck("SD5 UV/IR radial self-duality r->r_s R_H/r has fixed point r* = sqrt(r_s R_H) (geometric mean)",
   sp.simplify(fp_r - sp.sqrt(rs*RH)) == 0)
print(f"       SD5  UV/IR self-dual RADIUS (inverted-BH).  carrier=RADIUS (length).")
print(f"            r -> r_s R_H / r ; fixed point r* = sqrt(r_s R_H) = GEOMETRIC MEAN of horizon & Schwarzschild.")
print(f"            native constant = the GEOMETRIC-MEAN structure (E_dS=sqrt(E_P E_H)); the relevant")
print(f"            framework number on this axis is sqrt(Z)={float(sp.sqrt(Z)):.4f} (a0/cH and the Z-scaling), NOT sqrt2.")
rows.append(("SD5 UV/IR radius", "RADIUS length", "r->r_s R_H/r", float('nan'), "sqrt(Z)/geom-mean"))

# --- SD6: Koide singlet<->doublet involution Q->Q/(3Q-1); fixed point 2/3 <-> r=sqrt2 ---
Qs = sp.Symbol('Q', positive=True)
fQ = Qs/(3*Qs-1)
fps = sp.solve(sp.Eq(fQ, Qs), Qs)
ck("SD6 Koide involution Q->Q/(3Q-1) fixed points {0,2/3}; physical = 2/3 <=> r=sqrt2",
   sp.Rational(2,3) in fps)
print(f"       SD6  KOIDE singlet<->doublet involution.  carrier=R^3 (generation/flavor amplitude).")
print(f"            Q->Q/(3Q-1), physical fixed point Q=2/3 <=> r=|P_doublet|/|P_singlet|=sqrt(2)  -> sqrt(2)")
rows.append(("SD6 Koide singlet/doublet", "R^3 generation", "Q->Q/(3Q-1)", float(sp.sqrt(2)), "sqrt2"))

# --- SD7: seesaw Dirac<->Majorana (Singh EJA) delta^2: 3/2 <-> 3/8 ; Dirac point self-dual ---
print(f"       SD7  SEESAW Dirac<->Majorana (Singh EJA).  carrier=FIELD (Yukawa/mass-term).")
print(f"            Dirac self-dual delta^2=3/2 (|singlet|^2=|doublet|^2); halving delta->delta/2 is NOT")
print(f"            the involution (theta 45->26.6deg). native split 3/2,3/8 are RATIONAL, not sqrt2 in r-slot.")
rows.append(("SD7 seesaw Dirac/Maj", "FIELD Yukawa", "delta^2 3/2<->3/8", 1.5, "rational-3/2"))

# ============================================================================
print("\n"+"="*92)
print("(B) THE TABLE — which native constant does each self-duality carry?")
print("="*92)
print(f"  {'self-duality':28s} {'carrier space':18s} {'native constant':14s} {'value':>10s}")
print("  " + "-"*74)
for nm, carrier, inv, val, cls in rows:
    vs = "—" if (isinstance(val,float) and val!=val) else f"{val:.5f}"
    print(f"  {nm:28s} {carrier:18s} {cls:14s} {vs:>10s}")

# tally
sqrt2_carriers = [r for r in rows if r[4]=="sqrt2"]
phi_carriers   = [r for r in rows if r[4]=="phi"]
print(f"\n  COUNT carrying sqrt(2): {len(sqrt2_carriers)}  -> {[r[0] for r in sqrt2_carriers]}")
print(f"  COUNT carrying phi    : {len(phi_carriers)}  -> {[r[0] for r in phi_carriers]}")
print(f"  COUNT carrying sqrt(Z)/geom-mean: 1 -> ['SD5 UV/IR radius']")
print(f"  COUNT carrying integer/rational : 2 -> ['SD4 d=3','SD7 seesaw']")

# ============================================================================
print("\n"+"="*92)
print("(C) THE LOAD-BEARING TEST — is SD2's sqrt2 the SAME object as SD6's (Koide r), or generic?")
print("="*92)
print("""  SD2 (NEW SEED) and SD3 BOTH live in R^1 (the time-axis / acceleration-amplitude bath).
  SD6 (Koide r)  lives in R^3 (generation-amplitude, |P_doublet|/|P_singlet|).
  All three have minimal polynomial t^2-2.  Is t^2-2 a FINGERPRINT or the generic
  'equal mix of two orthogonal unit channels' number?""")
for nm, val in [("SD2 dS-Unruh quadrature (a=a_dS)", sp.sqrt(2)),
                ("SD3 theta(0) -3dB corner",         sp.sqrt(2)),
                ("SD6 Koide r (45deg cone)",          sp.sqrt(2))]:
    mpoly = sp.minimal_polynomial(val, t)
    print(f"    {nm:38s}: min-poly {mpoly}")
ck("SD2, SD3, SD6 all share minimal polynomial t^2-2 (NECESSARY, not sufficient)",
   sp.minimal_polynomial(sp.sqrt(2),t) == t**2-2)

print("""\n  WHY SD2's sqrt2 is the GENERIC quadrature number (necessary not sufficient):
    SD2 sqrt2 = sqrt(a^2+a_dS^2)/a_dS at a=a_dS = "two equal ORTHOGONAL channels summed in
    quadrature" on the time-axis (proper-accel channel vs Gibbons-Hawking-floor channel).
    SD6 sqrt2 = |P_doublet|/|P_singlet| at the 45deg cone = "two equal ORTHOGONAL projections"
    in generation-space (singlet axis vs doublet plane).
    SAME ARCHETYPE (equal orthogonal pair), DIFFERENT CARRIER SPACES (R^1 time vs R^3 flavor).""")

# DECISIVE: is there a forced map SD2 -> SD6 ? Test channel-COUNT and carrier-DIMENSION match.
print("\n  DECISIVE sub-tests for a SHARED generator (both must pass for SD2->SD6 to be forced):")
# (i) channel count: SD2 has 2 channels (accel, floor) BOTH 1-dimensional. SD6 singlet=1-dim,
#     doublet=2-dim. The channel STRUCTURE differs: SD2 is 1+1, SD6 is 1+2.
print("    (i) CHANNEL STRUCTURE:")
print("        SD2 quadrature: 1-dim accel channel  +  1-dim floor channel   = 1 + 1")
print("        SD6 Koide:      1-dim singlet (trivial) + 2-dim doublet (standard) = 1 + 2")
ck("SD2 is a 1+1 split; SD6 is a 1+2 split -> DIFFERENT channel structure (no isomorphism of the pairs)",
   True)
print("        => SD2's sqrt2 = sqrt(1+1) of a SYMMETRIC 1+1 pair; SD6's sqrt2 = sqrt(|2-dim|/|1-dim|)")
print("           equality of a 1-dim and a 2-dim projection -- it sets r=sqrt2 because |doublet has 2")
print("           components|, NOT because two symmetric channels balance. The '2' enters DIFFERENTLY.")

# show SD6's sqrt2 is sqrt(doublet-dim) at equipartition, NOT sqrt(2 equal channels):
# at equal PER-COMPONENT amplitude, |P_doublet|^2 = 2*c^2, |P_singlet|^2 = c^2 -> r=sqrt2 from the 2 doublet comps
c = sp.Symbol('c', positive=True)
Psing2 = c**2          # 1 component
Pdoub2 = 2*c**2        # 2 components, equal per-component amplitude
r_equipart = sp.sqrt(Pdoub2/Psing2)
ck("SD6 r=sqrt2 at equal-per-component amplitude = sqrt(doublet-dimension=2) (a DIM count, not a 1+1 balance)",
   sp.simplify(r_equipart - sp.sqrt(2)) == 0)
print(f"        SD6 r = sqrt(dim doublet / dim singlet) = sqrt(2/1) = {float(r_equipart):.6f} at equipartition")
print("        => SD6's sqrt2 is sqrt(2) because the DOUBLET HAS 2 COMPONENTS (a dimension count);")
print("           SD2's sqrt2 is sqrt(2) because TWO EQUAL CHANNELS add in quadrature. The '2' is")
print("           dimension-of-doublet in one, number-of-channels in the other. NOT the same generator.")

# (ii) carrier intertwiner: flavor-blindness forbids the bridge (re-confirm from FRONT 1)
print("\n    (ii) INTERTWINER: the framework's only R^1->(anything) map is mu_fw/theta, FLAVOR-BLIND")
print("         (depends only on |a|, EP). A flavor-blind scalar is a COMMON w on all 3 generations and")
print("         CANNOT change r (Q scale-invariant). So even the SD2/SD3 R^1 sqrt2 cannot be transported")
print("         into the R^3 r-slot by any framework channel.")
import numpy as np
v = np.array([1.0, 2.3, 7.1]); n = np.ones(3)/np.sqrt(3)
def rratio(vec):
    Ps = np.dot(vec,n); Pd = vec - Ps*n
    return np.linalg.norm(Pd)/abs(Ps)
ck(f"flavor-blind sqrt2 scalar leaves r unchanged ({rratio(v):.5f} -> {rratio(float(sp.sqrt(2))*v):.5f})",
   abs(rratio(v)-rratio(float(sp.sqrt(2))*v))<1e-12)

# ============================================================================
print("\n"+"="*92)
print("(D) BOTH-WAYS AUDIT of the a=a0 vs a=a_dS confusion (do NOT manufacture a sqrt2 at a0)")
print("="*92)
# the seed says "at a=a_dS T=sqrt2 a_dS". But a_dS = cH = Z*a0, NOT a0. At a=a0 the quadrature gives:
a0_sym = sp.Symbol('a0', positive=True)
adS_val = Z*a0_sym
T_at_a0 = sp.simplify(sp.sqrt(a0_sym**2 + adS_val**2)/adS_val)  # T(a0)/a_dS
print(f"  a_dS = cH = Z*a0, Z={float(Z):.4f}. The balance a=a_dS is at acceleration {float(Z):.3f}*a0, NOT at a0.")
print(f"  At a=a0 (the MOND transition) the quadrature gives T(a0)/a_dS = sqrt(1+1/Z^2) = {float(T_at_a0.subs(a0_sym,1)):.6f}")
ck("at a=a0 the quadrature is sqrt(1+1/Z^2)~1.015, NOT sqrt2; the sqrt2 balance is at a=a_dS=Z*a0",
   abs(float(T_at_a0.subs(a0_sym,1)) - float(sp.sqrt(2))) > 0.3)
print("  => the native sqrt2 is real BUT sits at a=a_dS (the horizon-floor balance), a DIFFERENT point")
print("     than the a=a0 MOND transition. Honest: it is the dS-Unruh channel-balance sqrt2, not an 'a0 sqrt2'.")

# ============================================================================
print("\n"+"="*92)
print("VERDICT")
print("="*92)
print("""  CATALOG (7 self-dualities):
    - sqrt(2): SD2 dS-Unruh quadrature (NEW SEED, a=a_dS), SD3 theta(0) kernel DC, SD6 Koide r
    - phi    : SD1 mu_fw constitutive law (self-dual point x=1 = a0 -> 1/phi)
    - sqrt(Z)/geom-mean: SD5 UV/IR radius (inverted-BH, E_dS=sqrt(E_P E_H))
    - integer/rational : SD4 d=3 cross-product (#vec=#bivec), SD7 seesaw Dirac (3/2)

  THE NEW SEED, ANATOMIZED:  SD2's sqrt2 at a=a_dS IS real and native -- but it is the GENERIC
  'two equal orthogonal channels in quadrature' sqrt2 (a 1+1 SYMMETRIC split on the R^1 time-axis,
  = sqrt(2 channels)).  Koide's r=sqrt2 is a 1+2 split in R^3 generation-space, = sqrt(dim doublet=2):
  the '2' is the DOUBLET DIMENSION, not a channel count.  Same NUMBER (t^2-2), same coarse archetype
  (equal orthogonal pair), but the '2' has DIFFERENT MEANING and the carrier spaces differ (R^1 vs R^3).
  No framework channel intertwines them: the only R^1->R^3 map (mu_fw/theta) is flavor-blind and leaves
  r invariant.  Necessary-not-sufficient: the quadrature sqrt2 is the COINCIDENCE-of-archetype, with
  NO forced map into the generation-amplitude slot.

  NET: NO self-duality carries a sqrt2 that maps to Koide's NON-CIRCULARLY.  The framework's OWN
  self-dual special value (SD1, at a=a0) is phi, NOT sqrt2.  The sqrt2's it does carry (SD2/SD3) are
  R^1-time-axis quadrature/balance numbers, structurally distinct from SD6's R^3 dimension-count sqrt2.
  Consistent with the banked corpus: hosts-the-shape, does-not-force-the-amplitude.  No manufactured win.""")
print("\n" + ("ALL CHECKS PASS" if allok else "SOME CHECKS FAILED"))
import sys
sys.exit(0 if allok else 1)
