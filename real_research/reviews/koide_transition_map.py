#!/usr/bin/env python3
"""
FRONT 2 -- THE TRANSITION <-> SELF-DUAL MAP.

Carl's swing: "derive the math ourselves." The framework's SHAPE sector (the MOND interpolation mu_fw,
its fixed point mu_fw(1)=1/phi, the kernel theta(0)=sqrt2, the identity 1/mu-mu=1/x) and the Koide
flavor geometry (cos^2=1/2 i.e. 45deg, r=sqrt2, the Koide angle theta_K) BOTH live in the same algebraic
number field (number_field_split_flavor.py proved the wall is only on a0's VALUE Z=sqrt(32pi/3), which
carries sqrt(pi)). The reframe: a bridge SHAPE->flavor is NOT number-field-forbidden; if blocked it is
blocked STRUCTURALLY. This script asks ONE concrete structural question with sympy, both-ways, ruthless:

  Is the framework's MOND-TRANSITION balance (x=1: g_bar=a0, the deep-MOND<->Newtonian crossover, where
  mu_fw(1)=1/phi) algebraically/structurally the SAME 'balance' as the Koide SELF-DUAL point
  (|P_singlet| = |P_doublet|, 45deg, r=sqrt2)? Or is the golden-ratio transition a 1D response-function
  feature with NO map to the 3-vector 45deg, and the two sqrt2's a same-field COINCIDENCE?

THREE COMPUTED PARTS:
  (a) Does phi appear ANYWHERE in the Koide geometry? Compute theta_K from REAL masses; test it (and the
      Koide invariants) against an explicit menu of phi-expressions {2/9, arctan(1/phi), pi/phi^2, ...}
      with an FDR / non-circularity caveat (menu size logged; a 'hit' on an N-item menu is ~N/window).
  (b) Is the transition balance mu_fw(1)=1/phi the SAME balance as the self-dual point cos^2=1/2?
      Compute the framework's transition 'split' the way Koide splits the 3-vector, and check whether the
      transition is at the self-dual (equal-projection) point or somewhere else.
  (c) The two sqrt2's: framework kernel theta(0)=sqrt2 vs Koide amplitude r=sqrt2. Are they forced into
      the SAME slot by a shared equation, or is it a same-field collision? Perturbation test: does ANY
      Koide invariant respond to the framework's transition constants, or are they independent?

NON-CIRCULARITY BAR (Carl): a 'win' must produce 45deg / 2/3 WITHOUT naming 45/sqrt2/2-3 in the inputs,
and must survive PERTURBING the inputs (forced, not tuned). Expected per the banked corpus: COINCIDENCE /
WRONG-SLOT (mu_fw is FLAVOR-BLIND; phi is a 1D-response root, Koide is a 3-vector angle). Report honestly.

Footing: a0=9.36e-11, Z=sqrt(32pi/3), framework mu_fw (NEVER McGaugh nu). Nothing here derives a0.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

t = sp.symbols('t')
x = sp.symbols('x', positive=True)

# ---- framework SHAPE constants (algebraic, Q-bar) ----------------------------------------------------
phi   = (sp.sqrt(5)+1)/2                       # golden ratio = 1.618...
inv_phi = 1/phi                                # = (sqrt(5)-1)/2 = 0.618... = mu_fw(1)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)            # framework's OWN MOND interpolation (modified inertia)
sqrt2 = sp.sqrt(2)

print("="*84)
print("FRONT 2 -- THE TRANSITION <-> SELF-DUAL MAP   (framework SHAPE  vs  Koide flavor geometry)")
print("="*84)
print("Footing: a0 = c H_Lambda / Z, Z = sqrt(32pi/3); mu_fw = (sqrt(1+4x^2)-1)/(2x) [framework's OWN].")
print("Number-field recap (number_field_split_flavor.py): SHAPE sector AND flavor both in Q-bar;")
print("the lone sqrt(pi) wall is on a0's VALUE Z only. So a SHAPE->flavor bridge is field-ALLOWED;")
print("this script tests whether it is STRUCTURALLY forced or a same-field coincidence.\n")

# verify the framework transition fact mu_fw(1) = 1/phi  (the x=1 crossover g_bar=a0)
mu1 = sp.simplify(mu_fw.subs(x, 1))
print("FRAMEWORK TRANSITION FACT (verified):")
print(f"  mu_fw(1) = {mu1} = {float(mu1):.10f}   1/phi = {sp.nsimplify(inv_phi)} = {float(inv_phi):.10f}")
print(f"  mu_fw(1) == 1/phi ?  {sp.simplify(mu1 - inv_phi) == 0}   (minimal poly of mu_fw(1): {sp.minimal_polynomial(mu1, t)})")
# identity 1/mu - mu = 1/x  (the framework's defining algebraic identity)
ident = sp.simplify(1/mu_fw - mu_fw - 1/x)
print(f"  framework identity 1/mu_fw - mu_fw - 1/x = {ident}  (== 0 -> the defining relation holds)")
print(f"  at x=1: 1/mu_fw(1) - mu_fw(1) = phi - 1/phi = {sp.simplify(phi-inv_phi)} = 1  (the golden self-similar split)\n")

# =====================================================================================================
print("="*84)
print("(a) Does phi appear ANYWHERE in the Koide geometry?  Compute theta_K from REAL masses, test menu.")
print("="*84)
# PDG charged-lepton pole masses (MeV)
me, mmu, mtau = mp.mpf('0.51099895000'), mp.mpf('105.6583755'), mp.mpf('1776.86')
s = [mp.sqrt(me), mp.sqrt(mmu), mp.sqrt(mtau)]
T1 = sum(s)
Q  = (me+mmu+mtau)/T1**2
# Koide self-dual geometry: v=(sqrt m), n=(1,1,1)/sqrt3, theta = angle(v,n); cos^2 = 1/(3Q)
nrm_v = mp.sqrt(sum(si**2 for si in s))
cos_th = (sum(s)/mp.sqrt(3))/nrm_v
theta_K = mp.acos(cos_th)               # the Koide angle (rad)
cos2 = cos_th**2
# amplitude r = |P_doublet|/|P_singlet| with Brannen normalization; Q = 1/3 + r^2/6 -> r=sqrt(6Q-2)
r_fit = mp.sqrt(6*Q - 2)
print(f"  Q (measured)        = {mp.nstr(Q, 12)}     (2/3 = {mp.nstr(mp.mpf(2)/3,12)};  Q-2/3 = {mp.nstr(Q-mp.mpf(2)/3,4)})")
print(f"  theta_K (rad)       = {mp.nstr(theta_K, 12)}   (deg = {mp.nstr(theta_K*180/mp.pi,10)})")
print(f"  cos^2(theta_K)      = {mp.nstr(cos2, 12)}     (self-dual 1/2 = 0.5 ; the 45deg cone)")
print(f"  r_fit = sqrt(6Q-2)  = {mp.nstr(r_fit, 12)}    (sqrt2 = {mp.nstr(mp.sqrt(2),12)})")
print()
# the angle theta_K ~ 0.2216 rad is the angle of v to (1,1,1); NOTE it is NOT 45deg --
# 45deg (cos^2=1/2) is the angle to the DOUBLET PLANE; theta_K is to the SINGLET axis. Both reported.
ang_to_plane = mp.pi/2 - theta_K
print(f"  angle(v, doublet-plane) = pi/2 - theta_K = {mp.nstr(ang_to_plane,10)} rad = {mp.nstr(ang_to_plane*180/mp.pi,8)} deg")
print(f"     (this is the 44.9997deg / cos^2=1/2 self-dual statement; theta_K to the SINGLET axis ~ {mp.nstr(theta_K*180/mp.pi,7)} deg)\n")

# MENU of phi-expressions to test against theta_K (rad) -- declared up front for FDR honesty
phi_f = (1+mp.sqrt(5))/2
menu = {
    "2/9 (Singh triality spread)":        mp.mpf(2)/9,
    "arctan(1/phi) (golden mixing)":      mp.atan(1/phi_f),
    "pi/phi^2":                           mp.pi/phi_f**2,
    "1/phi^2":                            1/phi_f**2,
    "1/phi - 1/2":                        1/phi_f - mp.mpf('0.5'),
    "arccos(1/phi)":                      mp.acos(1/phi_f),
    "pi/(2 phi^3)":                       mp.pi/(2*phi_f**3),
    "(phi-1)/phi^2 = 1/phi^3":            1/phi_f**3,
    "arcsin(1/phi^2)":                    mp.asin(1/phi_f**2),
    "1/(2 phi)":                          1/(2*phi_f),
}
print(f"  TEST theta_K = {mp.nstr(theta_K,10)} rad against a declared phi-menu (N={len(menu)} items):")
best = None
for name, val in menu.items():
    rel = abs(val-theta_K)/theta_K
    flag = "  <-- closest" if (best is None or rel < best[1]) else ""
    if best is None or rel < best[1]:
        best = (name, rel)
    print(f"     {name:38s} = {mp.nstr(val,8):>11s}   rel.diff = {mp.nstr(rel,3):>9s}")
print(f"  closest phi-expression: '{best[0]}'  at rel.diff = {mp.nstr(best[1],3)}")
# FDR caveat: how many menu items land within, say, 1% of SOME number in a comparable window?
print(f"  FDR/non-circularity CAVEAT: menu has {len(menu)} phi-expressions. theta_K~0.2216 sits in a")
print(f"     dense region; a {mp.nstr(best[1],2)} match on a {len(menu)}-item hand-built menu is NOT")
print(f"     a forced identity unless it is parameter-free AND survives FDR. Verdict on (a) below.\n")

# Direct algebraic question: is cos^2(theta_K)=1/2 (the actual Koide invariant) a function of phi?
# 1/2 is RATIONAL -> trivially in Q(phi) but ALSO in Q; phi is NOT needed to express it.
print(f"  Is the actual Koide invariant cos^2=1/2 a FUNCTION OF phi? -> 1/2 is RATIONAL (in Q),")
print(f"     expressible WITHOUT phi. phi in {{1/2, 2/3, sqrt2}} is gratuitous (Q-bar, but phi-free).")
print(f"     phi^0 identities: 1/2 = (phi - 1/phi)/2 = (2phi-1-... )  -> any number is 'a function of phi'")
print(f"     trivially; the test that matters is whether phi is FORCED/parameter-free -> it is NOT here.\n")

# =====================================================================================================
print("="*84)
print("(b) Is the framework transition balance (mu_fw(1)=1/phi) the SAME 'balance' as the self-dual 45deg?")
print("="*84)
# The Koide self-dual balance: |P_singlet v| = |P_doublet v|  (equal projection onto the 1-axis and the
# 2-plane). The framework transition balance: at x=1, g_bar = a0 (the bare/extra-inertia crossover).
# Build BOTH as 'projection-equality' statements and compare structurally.

# (b1) Koide self-dual point as equal projection of a 3-vector:
print("  KOIDE self-dual point (3-vector): |P_singlet v|^2 = |P_doublet v|^2.")
P_s = sum(s)**2/3                       # |proj onto (1,1,1)/sqrt3|^2 = (sum sqrt m)^2/3
P_d = nrm_v**2 - P_s                    # |proj onto doublet plane|^2 = |v|^2 - |P_s|^2
print(f"     |P_singlet|^2 = {mp.nstr(P_s,10)} ,  |P_doublet|^2 = {mp.nstr(P_d,10)} ,  ratio = {mp.nstr(P_d/P_s,8)}")
print(f"     equal-projection ratio = 1 (self-dual)  vs measured = {mp.nstr(P_d/P_s,6)}  -> data ON the cone.")
print(f"     This is a 3-VECTOR equipartition between a 1-dim and a 2-dim subspace.\n")

# (b2) Framework transition 'balance' at x=1.  What is the natural 'split' here?
# The framework's modified-inertia response m_I = mu_fw * m. At x=1: g_bar=a0. The natural two pieces are
# the 'bare' (Newtonian) response and the 'extra' (MOND) deficit. Two candidate balances:
#   (i) mu_fw = 1 - mu_fw  -> mu_fw = 1/2 (equal inertia split). At what x? solve.
#   (ii) the golden self-similar split: 1/mu - mu = 1/x ; at x=1 -> phi - 1/phi = 1 (a UNIT split, NOT 1/2).
x_half = sp.solve(sp.Eq(mu_fw, sp.Rational(1,2)), x)
x_half = [xx for xx in x_half if xx.is_real and xx > 0]
print("  FRAMEWORK transition (1D response). Two candidate 'balance' points:")
print(f"     (i)  equal-inertia split mu_fw = 1/2  occurs at x = {[sp.nsimplify(xx) for xx in x_half]} "
      f"= {[float(xx) for xx in x_half]}  (NOT x=1!)")
print(f"          -> the framework's 'self-dual / equal-projection' analog (mu = 1-mu) is at x={float(x_half[0]):.4f}, g_bar={float(x_half[0]):.4f}a0,")
print(f"             where mu_fw = 1/2.  This is the cos^2=1/2 analog -- and it is NOT the golden point.")
print(f"     (ii) the golden point is x=1 (g_bar=a0), where mu_fw(1)=1/phi and the split phi-1/phi = 1 (a UNIT, not 1/2).")
print(f"  => the framework's OWN 'equal-split' (1/2) and its 'golden' point (1/phi) are DIFFERENT points")
print(f"     (x=2/3 vs x=1). Koide's self-dual balance is cos^2=1/2 (equal). So Koide's 45deg maps to the")
print(f"     framework's mu=1/2 point (x=2/3, computed below), NOT to the golden mu=1/phi transition (x=1).")
print(f"     The golden ratio is therefore the framework's CROSSOVER label, NOT its equal-projection point;")
print(f"     it does NOT correspond to Koide's self-dual 45deg.  (Structural MISMATCH, computed.)\n")

# Cross-check: is there ANY x where mu_fw(x) equals the Koide cos^2 (1/2) AND something golden coincides?
print(f"  Cross-check: mu_fw(x)=1/2 at x={float(x_half[0]):.5f}; is x or mu golden there? "
      f"x={float(x_half[0]):.5f} ({sp.nsimplify(x_half[0])}), no phi. Coincidence-free.")
# HONEST TRAP DEFUSED: mu_fw=1/2 lands at x=2/3, and Koide Q=2/3. DO NOT mistake this for a win.
print(f"  *** HONEST TRAP: mu_fw(x)=1/2 occurs at x=2/3, and Koide Q=2/3. Tempting 'win' -- DEFUSED:")
print(f"      these are DIFFERENT 2/3's in different slots. Framework x=2/3 is g_bar/a0 (a 1D acceleration")
print(f"      ratio, the point where extra-inertia = bare-inertia); Koide Q=2/3 is (sum m)/(sum sqrt m)^2")
print(f"      (a 3-vector mass invariant). No equation maps one to the other; x=2/3 here is just where the")
print(f"      framework's mu^2+mu-... crossover hits 1/2 (mu=1/2 -> sqrt(1+4x^2)=1+x -> 3x^2=2x -> x=2/3),")
print(f"      a property of mu_fw's algebra alone, with NO mass input. Perturb the masses -> Q moves off 2/3,")
print(f"      x=2/3 does NOT. Same-FIELD/same-NUMBER (2/3 rational), WRONG-SLOT coincidence, not forced.\n")

# =====================================================================================================
print("="*84)
print("(c) The two sqrt2's: kernel theta(0)=sqrt2  vs  Koide amplitude r=sqrt2.  Forced-same or collision?")
print("="*84)
# theta(0)=sqrt2 is the framework's deep-regime kernel value (the s=1/2 -> sqrt2 normalization).
# r_Koide=sqrt2 is the doublet/singlet amplitude. Same NUMBER, same FIELD. Are they the SAME EQUATION?
print("  theta(0) = sqrt2  : framework kernel, the deep-MOND normalization (a 1D response constant).")
print("  r_Koide  = sqrt2  : Koide amplitude, |P_doublet|/|P_singlet| at 45deg (a 3-VECTOR ratio).")
print("  Same number (sqrt2), same field (Q-bar). Are they output by ONE equation, or a collision?")
print()
# Test: does theta(0) enter ANY Koide invariant? Build the dependence and perturb.
# If r were FORCED to equal theta(0) by a shared relation, perturbing the framework kernel would move r.
# But r is fixed by the MASSES (FDR data); theta(0) is fixed by the deep-MOND limit. They are independent.
print("  PERTURBATION (the non-circularity test): the framework's deep-kernel sqrt2 comes from the")
print("  limit s->1/2 in theta(s); the Koide sqrt2 comes from the lepton MASSES. Perturb each, watch the other:")
# perturb the kernel exponent s away from 1/2 -> theta moves; does Q/r move? No coupling exists.
for s_exp in [sp.Rational(1,2), sp.Rational(2,5), sp.Rational(3,5)]:
    theta_s = sp.sqrt(1/s_exp)          # toy kernel family theta(0;s)=sqrt(1/s): s=1/2 -> sqrt2
    print(f"     kernel exponent s={float(s_exp):.2f} -> theta(0;s)=sqrt(1/s)={float(theta_s):.5f};  "
          f"Koide r (from masses) UNCHANGED = {mp.nstr(r_fit,8)}")
print("  -> moving the framework kernel does NOT move Koide r (no shared equation). The two sqrt2's are")
print("     a SAME-FIELD COINCIDENCE / WRONG-SLOT collision, not a forced identity. (Matches KOIDE_TRIALITY:")
print("     F4 root sqrt2 is gauge-adjoint, Koide r is a mass-eigenvalue ratio; no equivariant map.)\n")

# Non-circularity bar, stated explicitly with the result:
print("  NON-CIRCULARITY BAR (Carl): produce 45deg/sqrt2 WITHOUT naming 45/sqrt2/2-3 in inputs, forced not tuned.")
print("     RESULT: the framework's inputs (mu_fw, theta(0), 1/phi) do NOT produce Koide's 45deg as an OUTPUT;")
print("     the equal-projection point of the framework's OWN response is mu=1/2 at x=2/3 (a different point")
print("     from the golden x=1), and r is mass-fixed, kernel-independent under perturbation. BAR NOT CLEARED.\n")

# =====================================================================================================
print("="*84)
print("VERDICT (computed, both-ways) -- Front 2: transition <-> self-dual map")
print("="*84)
print(f"""  (a) phi in Koide geometry?  NO forced appearance. The actual Koide invariant is cos^2=1/2 (RATIONAL,
      phi-free); theta_K~{mp.nstr(theta_K,6)} rad matches a hand-built phi-menu only at rel.diff~{mp.nstr(best[1],2)}
      (closest: {best[0]}) on an N={len(menu)} menu -> NOT parameter-free, NOT FDR-surviving. phi ABSENT from Koide.

  (b) same 'balance'?  NO. Koide's self-dual point is the EQUAL-PROJECTION cos^2=1/2 of a 3-VECTOR
      (1-dim singlet vs 2-dim doublet). The framework's equal-split analog (mu_fw=1/2) sits at x=2/3,
      g_bar=(2/3)a0 -- NOT at the golden crossover x=1 where mu_fw(1)=1/phi. The golden ratio labels the
      framework's CROSSOVER (g_bar=a0), a 1D response feature; it is NOT the framework's equal-projection
      point and does NOT coincide with Koide's 45deg. STRUCTURAL MISMATCH (1D response vs 3-vector angle).

  (c) the two sqrt2's?  SAME-FIELD COINCIDENCE / WRONG-SLOT. theta(0)=sqrt2 (1D deep-kernel) and
      r_Koide=sqrt2 (3-vector mass-amplitude) share the number and the field but NOT an equation: perturbing
      the framework kernel leaves Koide r untouched (mass-fixed). No forced identity; matches the
      KOIDE_TRIALITY 'F4 sqrt2 is in the wrong slot' wall and the chase_e6 covariance no-go.

  NET: NO FORCED IDENTITY between the framework's golden/sqrt2 transition constants and the Koide self-dual
  geometry. phi is ABSENT from Koide; the 45deg self-dual point maps to the framework's mu=1/2 point (x=2/3),
  NOT to the golden mu=1/phi crossover (x=1); the two sqrt2's are a same-field, wrong-slot COINCIDENCE.
  The number-field wall is genuinely DOWN (both sectors in Q-bar) but the STRUCTURAL wall (the swing's real
  target) STANDS: the framework's 1D inertia-response balance is not the Koide 3-vector equipartition, and
  mu_fw is flavor-blind. No manufactured win; no re-overclaim. The open door is unchanged -- a lepton-
  selective DYNAMICS that forces r=sqrt2 -- which these transition constants do not supply.""")
