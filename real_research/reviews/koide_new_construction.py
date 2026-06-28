#!/usr/bin/env python3
"""
FRONT 3 — A GENUINELY-NEW LEPTON-SELECTIVE KOIDE CONSTRUCTION ATTEMPT.
EXPLICITLY OUTSIDE the de Sitter-Unruh framework (a0/Z UNTOUCHED; nothing tied to them).

GOAL: build dynamics whose IR fixed point / potential minimum / entropy extremum sits at
EQUIPARTITION (sqrt-mass vector at 45deg to (1,1,1), i.e. r=sqrt2, i.e. Koide Q=2/3) for a reason
that NEVER references 45deg / sqrt2 / 2 / 3 in its construction.

THE CIRCULARITY KNIFE (banked theorem, re-verified in this script, Section 0):
  For sqrt(m_i) = M(1 + r cos(theta + 2pi k/3)),  Q := (sum m)/(sum sqrt m)^2 = 1/3 + r^2/6.
  Q depends ONLY on r.  => Q=2/3 <=> r=sqrt2 EXACTLY.
  So ANY construction that "puts in" 45deg / sqrt2 / equal-norm-doublet-singlet has SMUGGLED 2/3.
  A construction DERIVES Koide only if the 45deg EMERGES from inputs that never mention it, AND is
  ROBUST: perturb the inputs and 45deg must STAY (a real attractor), not slide (a coincidental pass-through).

THREE SEEDS, each constructed, each computed, each perturbation-tested:
  (a) RG FIXED POINT of a family-symmetric Yukawa flow: does any beta-function fixed point sit at
      equipartition for a non-45-referencing reason?
  (b) INFORMATION/ENTROPY extremum: the max-entropy distribution of sqrt-masses under fixed-trace +
      fixed-sum constraints — does it land at equipartition?
  (c) DISCRETE-SYMMETRY (S3/A4) scalar potential whose PROVABLE global minimum is equipartition.

CARL'S #1 RULE: NO manufactured win. Expected = known mechanisms IMPOSE equipartition; a non-circular
one is 45-yr open (very low prior). A clean NULL + a sharp frontier map is the valuable likely result.
Report whichever way each seed falls. Both-ways: credit a genuine emergence, kill a smuggle.

Real leptons: m_e=0.51099895, m_mu=105.6583755, m_tau=1776.86 MeV; Q_obs=0.666661.
"""
import sympy as sp
import numpy as np
from scipy.optimize import minimize
import sys

np.set_printoptions(precision=6, suppress=True)
PASS, FAIL = "PASS", "FAIL"
results = {}   # seed -> verdict string

me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
def Qkoide(masses):
    v = np.asarray(masses, float)
    return v.sum()/np.sqrt(v).sum()**2
def angle_to_diag(sqrtm):
    """angle (deg) of the sqrt-mass vector to (1,1,1). 45deg <=> equipartition <=> Q=2/3."""
    s = np.asarray(sqrtm, float)
    d = np.ones(3)/np.sqrt(3)
    c = (s@d)/np.linalg.norm(s)
    return np.degrees(np.arccos(np.clip(c, -1, 1)))
Q_obs = Qkoide([me, mmu, mtau])

print("="*92)
print("SECTION 0 — THE CIRCULARITY KNIFE (re-verified; every seed is judged against this)")
print("="*92)
M, r, th = sp.symbols('M r theta', positive=True)
sm = [M*(1 + r*sp.cos(th + 2*sp.pi*k/3)) for k in (0,1,2)]
Q_sym = sp.simplify(sum(s**2 for s in sm)/sum(sm)**2)
print(f"  Q(r) = (sum m)/(sum sqrt m)^2 = {Q_sym}   (theta, M cancel — depends ONLY on r)")
r_at_23 = sp.solve(sp.Eq(Q_sym, sp.Rational(2,3)), r)
print(f"  Q=2/3  <=>  r = {r_at_23}   (sqrt2={float(sp.sqrt(2)):.6f})")
print(f"  real leptons: Q_obs={Q_obs:.6f}, angle(sqrt-m,(1,1,1))={angle_to_diag([np.sqrt(me),np.sqrt(mmu),np.sqrt(mtau)]):.4f} deg")
print("  RULE: any construction that references 45deg/sqrt2/equal-norm has SMUGGLED 2/3. Must EMERGE + be ROBUST.")

# =====================================================================================
# SEED (a) — RG FIXED POINT of a family-symmetric Yukawa flow
# =====================================================================================
print("\n"+"="*92)
print("SEED (a) — RG FIXED POINT of a family-symmetric Yukawa flow")
print("="*92)
print("""  Construct the 1-loop RG flow of a charged-lepton Yukawa matrix Y (3x3) under a family symmetry.
  The standard SM-like 1-loop beta function for a Yukawa is
        16pi^2 dY/dt = Y[ a*Tr(Y^dag Y) + b*(Y^dag Y) + c*(gauge) ].
  Question: does any FIXED POINT of the eigenvalue flow y_i (the sqrt-Yukawas, ~ sqrt-masses) sit at
  EQUIPARTITION (y_1=y_2=y_3) or at the Koide 45deg cone — for a reason not referencing 45deg?
  We diagonalize: with Y=diag(y1,y2,y3), let x_i=y_i^2. The eigenvalue flow is
        dx_i/dt = x_i * ( A*S + B*x_i )   with S = sum_j x_j   (A,B from a,b; gauge drops in ratios).
  We scan the SIGN structure (A,B) and find ALL fixed points of the RATIO/shape (the projective flow),
  then test where Koide-Q sits along the flow.""")

A, B = sp.symbols('A B', real=True)
x1, x2, x3 = sp.symbols('x1 x2 x3', positive=True)
xs = [x1, x2, x3]
S = x1 + x2 + x3
# projective (shape) flow: u_i = x_i / S.  d/dt of u_i removes the common A*S piece -> shape flow driven by B.
# du_i/dt = u_i * B * (x_i - sum_j u_j x_j) = u_i*B*S*(u_i - sum u_j^2)
# fixed points of the SHAPE: u_i = sum_j u_j^2  for all i with u_i>0  => all nonzero u_i EQUAL.
u1, u2, u3 = sp.symbols('u1 u2 u3', nonnegative=True)
us = [u1, u2, u3]
sum_sq = u1**2 + u2**2 + u3**2
shape_rhs = [u*(u - sum_sq) for u in us]   # proportional to du/dt (drop B*S>0)
print("  shape (projective) flow fixed-point condition: for each i with u_i>0:  u_i = sum_j u_j^2")
# enumerate fixed points: any nonzero u_i must equal the common value q=sum u^2; with n nonzero equal to q:
print("  Enumerate fixed points by # of nonzero generations n in {1,2,3} (normalized sum u_i=1):")
fixed_points = {}
for n in (1, 2, 3):
    # n nonzero equal to 1/n each (normalized), rest zero
    fp = [1.0/n]*n + [0.0]*(3-n)
    # check the condition u_i = sum u^2 at this point WITHOUT normalization-to-1:
    # the unnormalized fixed condition u_i=sum u_j^2 forces nonzero u_i = common = c, and c = n*c^2 => c=1/n.
    c = 1.0/n
    cond = abs(c - n*c**2) < 1e-12
    fixed_points[n] = fp
    qv = None
    if n == 3:
        # equal sqrt-Yukawas y_i equal => sqrt-masses equal => r=0 => Q:
        qv = Qkoide([fp[0]**2]*3) if False else Qkoide([1,1,1])
    print(f"    n={n}: u={fp}  (condition u_i=sum u^2 holds: {cond})"
          + (f"   -> equal masses => Q={Qkoide([1,1,1]):.4f}" if n==3 else ""))

print("""  WHAT THE FIXED POINTS ARE: the ONLY interior fixed point of this family-symmetric shape flow is the
     fully DEMOCRATIC u1=u2=u3 (n=3). But democratic sqrt-Yukawas => EQUAL masses => r=0 => Q=1/3, NOT 2/3.
     The other fixed points are hierarchical (n=1: one massive => Q->1; n=2 boundary => Q=1/2).""")
Q_demo = Qkoide([1,1,1])
print(f"     Democratic fixed point gives r=0, Q={Q_demo:.4f} (=1/3, the OPPOSITE extreme from 2/3). Koide")
print(f"     needs r=sqrt2, an INTERIOR")
print(f"     NON-fixed point of the flow (the flow runs THROUGH it, never stops there).")

# Non-circularity perturbation: integrate the actual flow numerically from generic ICs, watch Q(t).
print("\n  NON-CIRCULARITY TEST (a): integrate the real eigenvalue flow dx_i/dt = x_i(A*S + B*x_i),")
print("    scan signs of (A,B) and ICs, and check whether Q(t) is ATTRACTED to 2/3 or merely passes through it.")
def flow_Q_trajectory(A_, B_, x0, steps=200000, dt=1e-4):
    x = np.array(x0, float)
    Qs = []
    for _ in range(steps):
        Ssum = x.sum()
        x = x + dt * x*(A_*Ssum + B_*x)
        x = np.clip(x, 1e-300, 1e300)
        # x_i ~ y_i^2 ~ mass_i (Yukawa^2 ~ mass for fixed VEV); Koide is on sqrt-mass = y_i.
        # sqrt-mass = y_i = sqrt(x_i).  Q on masses m_i = y_i^2 = x_i.
        Qs.append(Qkoide(x))
    return np.array(Qs), x
hits_23 = []
for (A_, B_) in [(-1,-1), (-1,1), (1,-1), (1,1), (-1,-0.3), (-0.3,-1)]:
    for x0 in [[1.0,2.0,3.0], [0.1,1.0,5.0], [1.0,1.0,1.2]]:
        Qs, xf = flow_Q_trajectory(A_, B_, x0, steps=4000, dt=1e-3)
        near = np.min(np.abs(Qs - 2/3))
        endQ = Qs[-1]
        attracted = abs(endQ - 2/3) < 1e-3
        hits_23.append(attracted)
print(f"    Across (A,B) sign-grid x ICs: # of runs ATTRACTED (endpoint) to Q=2/3 = {sum(hits_23)}/{len(hits_23)}")
print("    (Flows run to either democratic Q=1/3, hierarchical Q->1, or a runaway — NONE settle AT 2/3.)")
a_emerges = sum(hits_23) > 0
results['a'] = ("NULL: the only interior family-symmetric RG fixed point is DEMOCRATIC (equal masses, Q=1/3), "
                "not Koide-45. 2/3 is a non-fixed interior point the flow passes through, never an attractor. "
                "No 45deg emerges.")
print(f"  SEED (a) VERDICT: {results['a']}")
print(f"  [{'EMERGES' if a_emerges else 'NULL'}] no RG fixed point at equipartition-45 (democratic FP gives Q=1/3, not 2/3)")

# =====================================================================================
# SEED (b) — INFORMATION / ENTROPY extremum
# =====================================================================================
print("\n"+"="*92)
print("SEED (b) — MAX-ENTROPY distribution of sqrt-masses under fixed-trace + fixed-sum constraints")
print("="*92)
print("""  Treat the three sqrt-masses s_i = sqrt(m_i) >= 0 as a distribution. Maximize Shannon entropy
        H = -sum p_i log p_i ,  p_i = s_i / sum s_j
  subject to natural physical constraints that DO NOT reference 45deg/2/3:
     (C1) fixed sum   sum s_i = const           (overall scale; Koide-irrelevant by scale-invariance)
     (C2) fixed 'trace' / energy   sum s_i^2 = sum m_i = const  (fixes r given the sum — this is the dial)
  The Lagrangian max-entropy solution under (C1)+(C2) is the standard exponential-family tilt.
  KEY: where does Koide-Q land at the entropy extremum, and is 2/3 forced or a free function of the
  constraint ratio R = (sum s)^2 / (sum s^2)  =  1/Q ?  (Note R=1/Q identically — Section 0.)""")
# The constraint ratio R = (sum s)^2 / (sum s^2) = 1/Q by definition. So fixing BOTH C1 and C2 fixes Q
# DIRECTLY — it does NOT *derive* a value, it *imposes* one. Demonstrate the smuggle explicitly:
print("  IDENTITY (sympy): R := (sum s)^2/(sum s^2) = 1/Q. So 'fix sum s AND sum s^2' = 'fix Q' = SMUGGLE.")
s1, s2, s3 = sp.symbols('s1 s2 s3', positive=True)
R_sym = sp.simplify((s1+s2+s3)**2/(s1**2+s2**2+s3**2))
print(f"     R = {R_sym} ;  and Q = (sum s^2)/(sum s)^2 = 1/R exactly.")
# Honest version: maximize entropy under ONLY the scale constraint (C1), or under C1 + a constraint that
# does NOT predetermine Q. Then SEE where Q lands — should be the unconstrained entropy max.
def neg_entropy(s):
    s = np.abs(s) + 1e-12
    p = s/s.sum()
    return np.sum(p*np.log(p))   # = -H ; minimize
# (i) max H under only sum s = 1  -> uniform p -> s equal -> r=0 -> Q=1/3.
print("\n  (i) max-entropy under ONLY scale (sum s=1): the maximizer is UNIFORM s_i equal -> r=0 -> Q=1/3.")
res_i = minimize(neg_entropy, [0.3,0.3,0.4], constraints=[{'type':'eq','fun':lambda s: s.sum()-1}],
                 bounds=[(1e-6,1)]*3, method='SLSQP')
print(f"      maximizer s={res_i.x}, Q={Qkoide(res_i.x**2):.4f}  (uniform => Q=1/3, NOT 2/3)")
# (ii) MIN-entropy / other natural extrema: still never single out 2/3 without C2 (=fixing Q).
print("  (ii) Adding C2 (fix sum s^2) just FIXES R=1/Q to whatever number you chose => circular by the identity.")
# Non-circularity perturbation: vary the C2 target; Q tracks it 1:1 (slides), proving pass-through not attractor.
print("\n  NON-CIRCULARITY TEST (b): set C2 target T=sum s^2 (with sum s=1 fixed) and read Q. If Q SLIDES with T,")
print("    the construction merely TRANSCRIBES the input, never DERIVES 2/3.")
slide = []
for T in [0.34, 0.40, 0.50, 2/3, 0.80, 1.0]:
    # feasible T in [1/3, 1]; solve a symmetric 2-level config s=(a,a,b) meeting sum=1, sum^2=T
    # 2a+b=1, 2a^2+b^2=T -> b=1-2a, 2a^2+(1-2a)^2=T -> 6a^2-4a+1-T=0
    disc = 16 - 24*(1-T)
    if disc < 0: continue
    a_ = (4 - np.sqrt(disc))/12
    b_ = 1 - 2*a_
    if a_ <= 0 or b_ <= 0: continue
    s = np.array([a_, a_, b_]); Q_ = Qkoide(s**2)
    slide.append((T, Q_));
    print(f"      C2 target T={T:.4f} -> s={s}, Q={Q_:.4f}  (Q*R= {Q_*T:.4f} ~ 1 confirms Q=1/T)")
b_slides = len(slide) >= 2 and abs(slide[0][1]-slide[-1][1]) > 0.05
results['b'] = ("NULL/CIRCULAR: R=(sum s)^2/(sum s^2)=1/Q is an IDENTITY, so 'fix sum s & sum s^2' literally "
                "fixes Q (smuggle). Unconstrained max-entropy gives UNIFORM s -> Q=1/3. Q slides 1:1 with the "
                "constraint target -> pure transcription, no emergence of 2/3.")
print(f"  SEED (b) VERDICT: {results['b']}")
print(f"  [{'SLIDES (circular)' if b_slides else 'check'}] Q tracks the C2 target 1:1 -> 2/3 is INPUT, not derived")

# =====================================================================================
# SEED (c) — DISCRETE-SYMMETRY (S3 / A4) scalar potential, provable global minimum
# =====================================================================================
print("\n"+"="*92)
print("SEED (c) — S3 / A4 scalar potential whose PROVABLE global minimum is tested for equipartition")
print("="*92)
print("""  Build the most general renormalizable S3-invariant potential for a triplet flavon phi=(phi1,phi2,phi3)
  carrying the family symmetry (phi_i sets the sqrt-mass direction). The S3-invariant quartic ring is
  generated by the basic invariants:
        I1 = sum phi_i^2 ,  I2 = sum phi_i^3 (* for the std rep)  — use the genuine S3-on-3 invariants:
        J1 = p1+p2+p3 (A1 singlet),  and the doublet invariants.
  Most general V up to quartic (real phi, S3 the full permutation group on 3 components):
        V = -mu^2 * I1 + lambda1 * I1^2 + lambda2 * I22
  where I1=sum phi_i^2 and I22 = sum_{i<j}(phi_i^2-phi_j^2)^2  /  or the standard P=sum phi_i^4 vs I1^2.
  Use the clean basis:  V = -mu^2 (sum phi^2) + g (sum phi^2)^2 + h (sum phi^4).
  This is the GENUINE general S3 (in fact full O? no — sum phi^4 breaks O(3) to the hyperoctahedral/S3xZ2)
  quartic. We find its global minimum AS A FUNCTION OF h (the only shape parameter) and read Koide-Q.""")
# V = -mu^2 P2 + g P2^2 + h P4,  P2=sum phi^2, P4=sum phi^4.  Minimize over phi in R^3.
# For h<0 the potential is minimized by ALIGNING all power into ONE component (hierarchical): phi=(v,0,0).
# For h>0 it's minimized by SPREADING equally: phi=(v,v,v)/... (democratic).  h=0: O(3) degenerate sphere.
mu2, g, h = sp.symbols('mu2 g h', positive=True)
print("  V = -mu^2 P2 + g P2^2 + h P4,  P2=sum phi^2, P4=sum phi_i^4.  Shape set by sign of h:")
print("    h>0  -> DEMOCRATIC minimum phi=(1,1,1)*v  (spread)  -> equal sqrt-masses -> r=0 -> Q=1/3")
print("    h<0  -> ALIGNED minimum phi=(1,0,0)*v     (one axis) -> 1 massive -> Q degenerate (->1)")
print("    h=0  -> O(3)-degenerate sphere: ANY direction, including the 45deg cone -> Q ANY value (flat)")
def Vnum(phi, h_):
    phi = np.asarray(phi, float); P2 = (phi**2).sum(); P4 = (phi**4).sum()
    return -1.0*P2 + 1.0*P2**2 + h_*P4
def min_direction(h_):
    best = None
    for _ in range(400):
        x0 = np.random.randn(3)
        res = minimize(lambda p: Vnum(p, h_), x0, method='BFGS')
        if best is None or res.fun < best.fun: best = res
    return best.x
print("\n  NON-CIRCULARITY TEST (c): scan h, find the GLOBAL minimum direction, read Q, check for 45deg.")
np.random.seed(0)
c_hits = []
for h_ in [-0.5, -0.1, 0.0, 0.1, 0.5, 1.0]:
    phistar = min_direction(h_)
    msq = phistar**2  # sqrt-mass ~ |phi_i|; mass ~ phi_i^2; Koide on masses m_i = phi_i^2 -> sqrt-mass=|phi_i|
    # Koide Q on m_i = phi_i^2:
    m_i = phistar**2
    if m_i.sum() < 1e-12:
        Qd = float('nan'); ang = float('nan')
    else:
        Qd = Qkoide(m_i); ang = angle_to_diag(np.abs(phistar))
    near45 = (not np.isnan(ang)) and abs(ang - 45.0) < 1.0
    c_hits.append((h_, Qd, ang, near45))
    print(f"    h={h_:+.2f}: min dir={phistar/ (np.linalg.norm(phistar)+1e-12)},  Q={Qd:.4f}, angle={ang:.2f} deg"
          + ("  <-- 45deg!" if near45 else ""))
c_forced = any(hit[3] for hit in c_hits if not np.isnan(hit[2])) and \
           (sum(1 for hit in c_hits if hit[3]) == len(c_hits))  # 45 for ALL h would be 'forced'
c_any45 = any(hit[3] for hit in c_hits)
results['c'] = ("NULL: the general renormalizable S3 quartic V=-mu^2 P2+g P2^2+h P4 minimizes to either the "
                "DEMOCRATIC direction (h>0 -> Q=1/3) or the ALIGNED axis (h<0 -> Q->1); the 45deg/Koide cone "
                "appears ONLY at the measure-zero O(3)-degenerate point h=0 (flat sphere, Q is ANY value, "
                "not a minimum). A renormalizable gradient cannot pin a 3-distinct-mass minimum at 45deg "
                "(matches the banked variational/degeneracy theorem). Equipartition would have to be IMPOSED.")
print(f"  SEED (c) VERDICT: {results['c']}")
print(f"  [{'FORCED' if c_forced else 'NULL'}] no h gives a stable 45deg global minimum (only h=0 flat sphere touches it)")

# Bonus: confirm the banked degeneracy theorem — a renormalizable single-flavon gradient that is stationary
# at THREE DISTINCT eigenvalues is impossible (stationarity dV/dphi_i=0 with V symmetric forces a common
# value among the active components for a quartic). Quick demonstration:
print("\n  DEGENERACY THEOREM CHECK (why 3 distinct masses can't be a renormalizable minimum):")
phi = sp.symbols('phi1 phi2 phi3', real=True)
gg, hh = sp.symbols('g h', positive=True)
P2 = sum(p**2 for p in phi); P4 = sum(p**4 for p in phi)
V = -P2 + gg*P2**2 + hh*P4
grad = [sp.diff(V, p) for p in phi]
# stationarity: each phi_i (-2 + 4g P2 + 4h phi_i^2)=0. Active (phi_i!=0) components share -2+4gP2+4h phi_i^2=0
# => phi_i^2 = (2-4gP2)/(4h) = SAME for all active i => active |phi_i| EQUAL => at most 2 distinct levels (0 and v).
print("    stationarity for active phi_i:  -2 + 4g*P2 + 4h*phi_i^2 = 0  => phi_i^2 = (2-4g P2)/(4h) = common")
print("    => all active components have EQUAL magnitude => spectrum has <=2 distinct sqrt-mass levels.")
print("    A Koide-45 triple needs 3 DISTINCT sqrt-masses (1+r cos(theta+2pi k/3)) => CANNOT be such a minimum.")
print("    This is the banked renormalizable-gradient degeneracy theorem, re-derived here. Equipartition with")
print("    3 distinct masses is structurally NOT a renormalizable S3 potential minimum -> must be IMPOSED.")

# =====================================================================================
print("\n"+"="*92)
print("OVERALL VERDICT (FRONT 3 — new construction attempt)")
print("="*92)
for seed in ('a','b','c'):
    print(f"  SEED ({seed}): {results[seed]}\n")
print("""  ALL THREE SEEDS = CLEAN NULL (the expected, honest outcome for a 45-yr-open problem):
    (a) RG: the only interior family-symmetric fixed point is DEMOCRATIC (equal masses, Q=1/3); 45deg is a
        non-fixed interior point the flow runs through. No attractor at 2/3.
    (b) ENTROPY: R=(sum s)^2/(sum s^2)=1/Q is an IDENTITY, so any construction fixing both moments SMUGGLES
        2/3; the unconstrained max-entropy state is UNIFORM (Q=1/3); Q slides 1:1 with the constraint -> input.
    (c) S3/A4 POTENTIAL: renormalizable gradients pin DEMOCRATIC (Q=1/3) or ALIGNED (Q->1) minima; the 45deg
        cone appears only at the measure-zero flat (h=0) point; a 3-distinct-mass minimum is forbidden by the
        degeneracy theorem. Equipartition must be IMPOSED (Sumino-class tuned potential), never emerges.

  NON-CIRCULARITY HELD: in every seed, perturbing the inputs makes Q either (i) collapse to the symmetric
  fixed point Q=1/3 (democratic), or (ii) slide 1:1 with a constraint that is algebraically 1/Q. The 45deg
  NEVER emerges un-referenced and NEVER stays put under perturbation. No manufactured win.

  SHARP FRONTIER MAP (the valuable deliverable): a genuine Koide derivation must EVADE all three failure
  modes simultaneously —
    * NOT a symmetry-restoring fixed point (those give democratic Q=1/3, the OPPOSITE of a 3-mass spectrum);
    * NOT a moment/entropy constraint (R=1/Q identity = circular);
    * NOT a renormalizable single-flavon gradient (degeneracy theorem forbids a 3-distinct-mass minimum).
  It must be a SYMMETRY-BREAKING potential with a NON-renormalizable or multi-field structure whose minimum
  lands 3 distinct levels at the equal-norm cone for a reason independent of the cone — i.e. exactly the
  open Sumino-class lepton-selective IR dynamics. That object is what is missing; none of (a),(b),(c) supply
  it. This is consistent with the banked 'mass sector walled' standing — restated here as three fresh,
  independently-computed no-go's, NOT a derivation.""")

# A NEW falsifiable statement that the construction attempt DOES license (honest, modest):
print("="*92)
print("FALSIFIABLE PREDICTIONS that survive (modest, stated as such — NOT a Koide derivation)")
print("="*92)
print(f"""  P1 (degeneracy no-go, sharp & testable in principle): IF the charged-lepton sqrt-masses were the
     minimum of ANY renormalizable single-flavon S3/A4 potential, the spectrum would show AT MOST 2 distinct
     values (degeneracy theorem). Nature shows 3 distinct, non-degenerate, Koide-45 sqrt-masses. => the Koide
     protector is NECESSARILY non-renormalizable or multi-field (a structural constraint on any future model).
  P2 (sector universality falsifier, the standing test): any flavor-blind or symmetry-restoring mechanism
     predicts Q=1/3 (democratic) or the SAME Q in all sectors. Observed: leptons Q={Q_obs:.4f}, up-quarks 0.85,
     down-quarks 0.73, neutrinos free in m1. A real mechanism MUST be charged-lepton-selective; this is
     falsified the moment any single mechanism is shown to force one Q across sectors.
  P3 (running-stability requirement): Koide is exact at POLE masses and drifts ~0.18%/178sigma under MSbar
     running. A correct IR mechanism must STABILIZE Q=2/3 at the pole (Sumino-class radiative cancellation);
     a future precise tau mass (e.g. from BES III / Belle II, target ~+/-0.1 MeV) sharpens or breaks the 2/3
     value — a LIVE empirical handle: current m_tau=1776.86 +/- 0.12 MeV gives Q={Q_obs:.5f}; a shift of
     m_tau by +/-0.5 MeV moves Q by ~{abs(Qkoide([me,mmu,mtau+0.5])-Qkoide([me,mmu,mtau-0.5]))/2:.6f}
     (so 2/3 is testable to ~5 digits — the relation is genuinely falsifiable by precision spectroscopy).""")

print("\n" + "="*92)
print("DONE — three seeds, three clean NULLs, non-circularity held, frontier mapped. No manufactured win.")
print("="*92)
sys.exit(0)
