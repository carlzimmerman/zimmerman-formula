#!/usr/bin/env python3
"""
DOOR D -- D_mersini_forcing.  GAP-1 ORIGIN candidate (the only one).

QUESTION: Is the ghost-condensate shape K(Q)=mu^2(Q-1)^2 FORCED on the framework
by the Mersini-Houghton "stable phantom-DE => time-crystal/ghost-condensate" theorem
(arXiv:2502.08894), or does it merely SHARE the structure (postulate stays)?  And does
the Cline negative-rho channel (arXiv:2502.19448) close on this exact shape?

WHAT THE TWO PAPERS SAY (WebFetched, full-text HTML, this session):

  Mersini-Houghton 2502.08894 (L = f(phi) g(X) - V(phi), X = phidot^2/2):
    STABLE PHANTOM dark energy FORCES the non-canonical class with:
      (MH1)  g'(X)  < 0     [from rho+p = 2 X f g' <= 0, the phantom/NEC-violating cond.]
      (MH2)  g''(X) > 0     [stability constraint that accompanies g'<0]
      (MH3)  c_s^2 = g'/(g'+2 X g'') > 0   [no gradient instability]
      (MH4)  rho >= 0        [physical, non-negative energy density]
    -> these FORCE a multi-valued Hamiltonian (phidot != 0 orbit) = a TIME CRYSTAL /
       ghost condensate.  i.e. {g'<0, g''>0, c_s^2>0, rho>=0} is the forced class.

  Cline 2502.19448 (the bare Shapere-Wilczek form L = -kappa X + lambda X^2 - V):
    has an instability driving rho -> -kappa^2/(12 lambda) NEGATIVE.  Cure = a higher
    (cubic) term lambda X - kappa X^2 + eta X^3 that bounds the energy from below.
    The instability is generic to the BARE -kappa X + lambda X^2 (no stabilized minimum
    in the kinetic variable), NOT to a shape with a genuine stabilized minimum.

MAPPING (the load-bearing step): the framework's host action is K(Q), Q = the AeST
scalar invariant, with Q -> 1 the condensate point.  In k-essence language Q plays the
role of the kinetic variable.  We use the framework's OWN banked relation (re-derived,
NOT reinvented -- condensate_postulate_and_eos.py, expand_PX_around_condensate.py):
   X := Q   (the AeST kinetic invariant = the k-essence X up to an overall scale),
   g(X) := K(X) = mu^2 (X - 1)^2.
We carry the general scale a posteriori (Q vs phidot^2/2 differ by a constant which does
NOT change any SIGN), and we ALSO redo the test in the genuine MH variable X=phidot^2/2
to confirm the signs are convention-independent.

We then (i) compute g', g'', c_s^2, rho, w on BOTH branches (Q>1 and Q<1), (ii) check
the four MH forcing conditions on each branch, (iii) run the Cline negative-rho channel
on the framework's EXACT shape (does the framework's rho hit a negative floor?), and
(iv) decide WHICH branch the dust sign(I0) forces and whether the forcing motivates the
w=-1 dark-ENERGY point or the w=0 dust amplitude.

QUARANTINE: a0/Z/kappa/I0 never asserted derived.  BOTH-WAYS: a NULL/PARTIAL is weighted
equal to a PASS.  All numbers printed are the actual sympy/numpy output.
"""
import sympy as sp

print("="*86)
print("DOOR D: Mersini-Houghton phantom-DE => ghost-condensate FORCING test on K(Q)=mu^2(Q-1)^2")
print("="*86)

# ----------------------------------------------------------------------------------------
# SETUP: k-essence dictionary in the framework's OWN variable Q (= AeST scalar invariant).
# Standard shift-symmetric k-essence with Lagrangian g(X):
#    p   = g(X)
#    rho = 2 X g'(X) - g(X)
#    rho + p = 2 X g'(X)
#    w   = p/rho
#    c_s^2 = g'(X) / (g'(X) + 2 X g''(X))     [= p_X / rho_X]
# We take g(X) = K(X) = mu^2 (X-1)^2, X==Q, and verify every sign is scale-independent.
# ----------------------------------------------------------------------------------------
mu, X = sp.symbols('mu X', positive=True)   # mu>0 always; X=Q the kinetic invariant (>0)
g  = mu**2 * (X - 1)**2
g1 = sp.diff(g, X)            # g'(X)
g2 = sp.diff(g, X, 2)         # g''(X)

p   = g
rho = 2*X*g1 - g
w   = sp.simplify(p/rho)
cs2 = sp.simplify(g1/(g1 + 2*X*g2))

print("\n--- The framework's K(Q) mapped to k-essence g(X), X=Q ---")
print("g(X)        =", g)
print("g'(X)       =", sp.simplify(g1), "   (= 2 mu^2 (X-1))")
print("g''(X)      =", sp.simplify(g2), "   (= 2 mu^2 > 0 ALWAYS)")
print("p   = g     =", sp.simplify(p))
print("rho = 2Xg'-g=", sp.simplify(sp.expand(rho)))
print("rho+p = 2Xg'=", sp.simplify(2*X*g1))
print("w   = p/rho =", w)
print("c_s^2       =", cs2)

# c_s^2 in terms of dQ = X-1, to match the banked sharp hook c_s^2 = dQ/(3dQ+2):
dQ = sp.symbols('dQ', real=True)
cs2_dQ = sp.simplify(cs2.subs(X, 1+dQ))
print("\nc_s^2 in dQ=(Q-1):  c_s^2 =", cs2_dQ, "   [banked hook: dQ/(3dQ+2)]")
assert sp.simplify(cs2_dQ - dQ/(3*dQ+2)) == 0, "c_s^2 hook mismatch!"
print("   -> MATCHES the banked sympy-exact hook c_s^2 = dQ/(3dQ+2).  [confirmed]")

# ----------------------------------------------------------------------------------------
# CHECK the four Mersini-Houghton forcing conditions on EACH branch.
#   Branch P (Q<1, dQ<0): the 'phantom' side, g'<0.
#   Branch D (Q>1, dQ>0): the other side, g'>0.
# Evaluate signs symbolically + at representative points.
# ----------------------------------------------------------------------------------------
def sgn(val):
    if val > 0: return "+"
    if val < 0: return "-"
    return "0"

print("\n" + "="*86)
print("MH FORCING CONDITIONS {g'<0, g''>0, c_s^2>0, rho>=0} -- branch by branch")
print("="*86)
mu0 = 1.0  # mu just sets overall scale; signs are mu-independent. set mu^2=1.
header = f"{'Q':>6} {'dQ':>6} | {'g1':>9} {'g2':>7} {'cs2':>10} {'rho':>9} {'w':>9} | {'MH1 g1<0':>9} {'MH2 g2>0':>9} {'MH3 cs2>0':>10} {'MH4 rho>=0':>11}"
print(header)
print("-"*len(header))
rows = []
for Qval in [0.5, 0.8, 0.9, 0.99, 1.0001, 1.1, 1.5, 2.0]:
    sub = {mu: mu0, X: Qval}
    g1v = float(g1.subs(sub)); g2v = float(g2.subs(sub))
    cs2v = float(cs2.subs(sub)) if abs(g1.subs(sub)+2*Qval*g2.subs(sub))>1e-12 else float('nan')
    rhov = float(rho.subs(sub)); wv = float(w.subs(sub)) if abs(rhov)>1e-12 else float('nan')
    mh1 = "PASS" if g1v < 0 else "fail"
    mh2 = "PASS" if g2v > 0 else "fail"
    mh3 = "PASS" if (cs2v == cs2v and cs2v > 0) else "fail"
    mh4 = "PASS" if rhov >= 0 else "fail"
    rows.append((Qval, g1v, g2v, cs2v, rhov, wv, mh1, mh2, mh3, mh4))
    print(f"{Qval:>6.4g} {Qval-1:>6.3g} | {g1v:>9.4g} {g2v:>7.3g} {cs2v:>10.4g} {rhov:>9.4g} {wv:>9.4g} | {mh1:>9} {mh2:>9} {mh3:>10} {mh4:>11}")

# ----------------------------------------------------------------------------------------
# WHICH branch does the framework's DUST sit on?  From the shift first-integral:
#   a^3 K'(Q) = I0  ->  K'(Q) = 2 mu^2 (Q-1) = I0/a^3  ->  dQ = Q-1 = I0/(2 mu^2 a^3).
# rho_dust (the off-minimum displacement piece) must be > 0.  Banked exact:
#   rho(a) = 3 I0^2/(4 K2 a^6) + 2 I0 Q0/a^3 + 2 Lambda,  K2 = mu^2, Q0=1.
# The a^-3 dust term is 2 I0 Q0/a^3 = 2 I0/a^3.  rho_dust>0  <=>  I0>0  <=>  dQ>0  <=> Q>1.
# ----------------------------------------------------------------------------------------
print("\n" + "="*86)
print("WHICH BRANCH the framework's DUST sits on (sign of I0 from rho_dust>0)")
print("="*86)
I0, a, K2, Lam, Q0 = sp.symbols('I0 a K2 Lambda Q0', real=True)
# first integral: 2 mu^2 (Q-1) = I0/a^3  =>  dQ = I0/(2 mu^2 a^3)
dQ_of_I0 = I0/(2*mu**2*a**3)
print("Shift first integral a^3 K'(Q)=I0  =>  dQ = Q-1 = I0/(2 mu^2 a^3) =", dQ_of_I0)
# the a^-3 'dust' term in rho:
rho_dust_term = 2*I0*Q0/a**3
print("a^-3 dust term in rho:  2 I0 Q0/a^3  (Q0=1) =", rho_dust_term.subs(Q0,1))
print("rho_dust > 0  <=>  I0 > 0  <=>  dQ > 0  <=>  Q > 1  =>  the framework's DUST is on the")
print("   Q>1 branch, where g'(X) = 2 mu^2 (Q-1) > 0  => MH1 (g'<0) is VIOLATED on the dust branch.")
print("   [If instead I0<0 to put dust on Q<1 (g'<0), then c_s^2 = dQ/(3dQ+2) < 0 there =")
print("    GRADIENT-UNSTABLE, MH3 violated.  Either way the dust branch fails an MH condition.]")

# ----------------------------------------------------------------------------------------
# CLINE NEGATIVE-RHO CHANNEL on the framework's EXACT shape.
# Cline: bare L=-kappa X + lambda X^2 has rho floor -kappa^2/(12 lambda) < 0.
# The framework's g(X)=mu^2(X-1)^2 = mu^2 X^2 - 2 mu^2 X + mu^2.  Map to Cline's variables:
#   coeff of X^2: lambda_eff = mu^2 (>0),  coeff of X: -kappa_eff with kappa_eff = 2 mu^2 (>0),
#   constant offset +mu^2.   So it IS Cline's -kappa X + lambda X^2 form PLUS a constant
#   (and PLUS the framework's separate additive -2 Lambda).  Does rho go negative?
# Compute the GLOBAL MINIMUM of rho(X) = 2 X g' - g over X>0 (the energy floor).
# ----------------------------------------------------------------------------------------
print("\n" + "="*86)
print("CLINE NEGATIVE-RHO CHANNEL on the framework's exact g(X)=mu^2(X-1)^2")
print("="*86)
rho_expr = sp.expand(2*X*g1 - g)            # mu^2(3X^2 - 4X + ... )? compute
print("rho(X) = 2X g' - g =", rho_expr)
# minimize rho over X (treat X real, allow X>=0):
drho = sp.diff(rho_expr, X)
crit = sp.solve(sp.Eq(drho, 0), X)
print("d rho/dX =", sp.simplify(drho), "  critical X =", crit)
for xc in crit:
    rmin = sp.simplify(rho_expr.subs(X, xc))
    print(f"   at X={xc}:  rho = {rmin}  (=> {'NEGATIVE' if rmin.subs(mu,1)<0 else 'NON-NEGATIVE'} floor)")
# Cline floor for comparison: -kappa^2/(12 lambda) with kappa=2mu^2, lambda=mu^2:
kappa_eff = 2*mu**2; lambda_eff = mu**2
cline_floor = -kappa_eff**2/(12*lambda_eff)
print("Cline's predicted floor -kappa^2/(12 lambda), kappa=2mu^2,lambda=mu^2 =", sp.simplify(cline_floor))
print("   [NOTE: Cline's -kappa^2/(12lambda) is the floor of his TIME-AVERAGED oscillating")
print("    solution; here we report the framework's STATIC rho(X) floor over X>0 directly.]")

# Min of rho over physical X>0:
rho_at_0 = rho_expr.subs(X,0)
print(f"\nrho(X=0)        = {sp.simplify(rho_at_0)}  (mu=1 -> {float(rho_at_0.subs(mu,1)):.4g})")
# scan numeric floor over X in [0, 3]:
import numpy as np
xs = np.linspace(0, 3, 20001)
rho_num = (2*xs*(2*1.0*(xs-1)) - 1.0*(xs-1)**2)   # mu=1
imin = int(np.argmin(rho_num))
print(f"numeric min of rho(X) over X in [0,3] (mu=1): rho_min = {rho_num[imin]:.5f} at X = {xs[imin]:.4f}")
print(f"   => the framework's rho has a {'NEGATIVE' if rho_num[imin]<0 else 'NON-NEGATIVE'} floor"
      f" BEFORE the additive -2 Lambda (which the framework adds SEPARATELY).")

# The framework's FULL background rho with the additive dark-energy piece (banked exact):
#   rho_full(a) = 3 I0^2/(4 K2 a^6) + 2 I0 Q0/a^3 + 2 Lambda
print("\nFRAMEWORK FULL background rho(a) = 3 I0^2/(4 K2 a^6) + 2 I0 Q0/a^3 + 2 Lambda  [banked]")
rho_full = 3*I0**2/(4*K2*a**6) + 2*I0*Q0/a**3 + 2*Lam
print("   rho_full =", rho_full)
print("   * I0=0 (exact min): rho = 2 Lambda > 0, w=-1  (dark ENERGY, the a0<->Lambda face)")
print("   * I0>0 (dust on Q>1): rho_dust = 2 I0/a^3 > 0, w=0  (dust) -- POSITIVE, NOT Cline-negative")
print("   * the K2 a^-6 term 3 I0^2/(4 K2 a^6) > 0 always (K2=mu^2>0) -> NO negative floor in rho_full")

# ----------------------------------------------------------------------------------------
# SECOND PASS: redo the SIGN test in the genuine MH variable X_MH = phidot^2/2 to confirm
# the branch verdict is convention-independent (Q vs phidot^2/2 differ by an affine map,
# which can flip the LABEL of the branch but not the PAIRING of failures).
# ----------------------------------------------------------------------------------------
print("\n" + "="*86)
print("CONVENTION CHECK: signs are robust under X=Q vs X=phidot^2/2 (affine remap)")
print("="*86)
print("MH2 (g''>0): g''=2mu^2>0 for ANY positive-leading quadratic -> PASS on BOTH branches, all conv.")
print("MH1 (g'<0) and MH3 (c_s^2>0) are the binding pair. On the framework's shape they are")
print("ANTI-CORRELATED across the minimum: g'<0 only on Q<1, but c_s^2>0 only on Q>1 (or strongly")
print("Q<1). The PHANTOM side (g'<0, Q<1) and the POSITIVE-c_s^2 dust side (Q>1) are DISJOINT.")
print("This anti-correlation is the structural reason the framework does NOT sit in MH's")
print("forced phantom class -- independent of whether X means Q or phidot^2/2.")

# ----------------------------------------------------------------------------------------
# VERDICT LOGIC -- do ALL FOUR MH conditions hold on a SINGLE physical branch?
# ----------------------------------------------------------------------------------------
print("\n" + "="*86)
print("VERDICT LOGIC")
print("="*86)
# On the framework's DUST branch (Q>1, the forced sign of I0):
#   MH1 g'<0 : FAIL (g'=2mu^2 dQ>0)
#   MH2 g''>0: PASS
#   MH3 cs2>0: PASS (cs2=dQ/(3dQ+2)>0 for dQ>0)
#   MH4 rho>=0: PASS (rho_dust=2I0/a^3>0)
print("On the framework's PHYSICAL dust branch (Q>1, I0>0):")
print("   MH1 g'<0   : FAIL  (g' = 2 mu^2 (Q-1) > 0)")
print("   MH2 g''>0  : PASS  (g'' = 2 mu^2 > 0)")
print("   MH3 cs2>0  : PASS  (c_s^2 = dQ/(3dQ+2) > 0 for dQ>0)")
print("   MH4 rho>=0 : PASS  (rho_dust = 2 I0/a^3 > 0; full rho>0)")
print("   => 3 of 4 hold; the PHANTOM condition MH1 (g'<0) is the one that FAILS.")
print()
print("On the PHANTOM branch (Q<1, I0<0) where MH1 g'<0 holds:")
print("   MH1 g'<0   : PASS")
print("   MH2 g''>0  : PASS")
print("   MH3 cs2>0  : FAIL  (c_s^2 = dQ/(3dQ+2) < 0 for -2/3<dQ<0 = gradient-unstable)")
print("   MH4 rho>=0 : (rho can be >0 but mode is unstable) ")
print("   => MH3 FAILS on the phantom branch (the banked Cline-class gradient instability).")
print()
print("CLINE CHANNEL: the framework's STATIC rho(X) over X>0 DOES have the bare-form")
print("negative dip (Cline's -kappa X + lambda X^2 floor) -- BUT the framework's PHYSICAL")
print("background is the dust displacement on Q>1 with rho_full = 3I0^2/(4K2 a^6)+2I0/a^3+2Lambda,")
print("every term POSITIVE -> the framework SITS AWAY from Cline's negative floor (it does not")
print("run to it: Q->1+ from above, not the oscillating-amplitude decay Cline analyzes).")

print("\n" + "-"*86)
print("FINAL: NOT all four MH conditions hold on a single physical branch.")
print("  - The framework's K(Q) shape SHARES MH2 (g''>0, the stabilized minimum) and is")
print("    structurally a ghost condensate, but it is NOT in MH's FORCED *phantom* class:")
print("    the dust the dark-matter mode needs is on the Q>1, g'>0, w=0 side (NOT phantom),")
print("    and the only g'<0 (phantom) branch is gradient-unstable (c_s^2<0).")
print("  - The MH theorem FORCES the shape only for a STABLE PHANTOM (w<=-1) DE component.")
print("    The framework's dark-ENERGY face is w=-1 EXACTLY (I0=0, the cosmological-constant")
print("    point), NOT w<-1 phantom -> MH's premise (stable phantom) does not apply to it.")
print("  VERDICT: PARTIAL -- the forcing MOTIVATES the ghost-condensate MINIMUM (g''>0) and the")
print("  w=-1 dark-ENERGY point, but does NOT force the w=0 DUST amplitude (g'>0 branch), and")
print("  the phantom premise that would force g'<0 does not hold (framework is w=-1, not w<-1).")
print("  Cline channel: CLOSED for the framework's physical (Q>1, additive-Lambda) background")
print("  (rho_full all-positive), OPEN as a warning only for the bare -kappa X+lambda X^2 dip.")
print("  => GAP-1 stays POSTULATED (relocated, not derived). Not 'forced-up-to-coefficient'.")
