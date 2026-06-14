"""
agentXX Route 2 — PART 3: the b-family edge & dilatation-caustic test (sub-test b).

agentSS found the sonic edge b -> c_chi is where the dilatation caustic sits;
agentEE [2c] gives the b-family pullback with the POLE structure
   W_b(tau) = -H^2 / [16 pi^2 c_chi (c_chi^2 - b^2) sinh^2(kappa tau / 2)],
   b = a/kappa,   kappa^2 = a^2 + H^2   (Deser-Levin),   b^2 = a^2/(a^2+H^2).

The edge is b -> c_chi : the amplitude prefactor 1/(c_chi^2 - b^2) BLOWS UP.
QUESTION (b): does requiring the sonic edge (b=c_chi) to coincide with a
dS-INVARIANT surface FORCE a relation c_chi = f(H)?

The candidate dS-invariant surfaces / fixed loci:
  - the dS horizon  b -> 1  (the light cone, modular fixed point of the boost),
  - the static-patch modular fixed point (the boost L_0 fixed points),
  - b -> 0 (the comoving/static worldline, the dilatation fixed point).

Sub-tests:
  (c1) Compute the caustic locus b=c_chi in terms of (a,H): solve b=a/kappa,
       kappa^2=a^2+H^2 for the acceleration a_edge at which b=c_chi, and read
       whether c_chi gets tied to H. Show that a_edge is a FREE function of
       both c_chi AND H => the edge is a one-parameter family, NOT a lock.
  (c2) Test the dS-invariance of the edge condition under the dilatation
       (the surviving generator). Under s -> e^a s the chord/acceleration
       co-dilate; does c_chi co-dilate? c_chi is a (H=0)-present PPN datum =>
       dilatation weight 0 => it does NOT co-dilate. So the edge equation
       b(a,H)=c_chi is NOT scale-covariant: the dilatation maps the edge locus
       to a DIFFERENT c_chi value, confirming c_chi is a modulus the symmetry
       does not constrain (the agentSS weight argument, now for the edge).
  (c3) The luminal-coincidence trap: the ONLY way the edge b=c_chi lands ON a
       dS-invariant surface for ALL (a,H) is c_chi=1 (edge=horizon). For
       c_chi != 1 the sonic edge is a NON-invariant surface (it sits at
       metrically spacelike separation for c_chi>1). So requiring edge=dS-
       invariant FORCES c_chi=1 — the luminal value — which DECOUPLES the
       sonic edge. Report this honestly: the symmetry 'forces' only the value
       that destroys the mechanism.
"""
import sympy as sp

a, H, cchi, b, kappa, tau = sp.symbols('a H c_chi b kappa tau', positive=True)

print("="*70)
print("PART 3 (c1): the caustic locus b=c_chi in (a,H)")
print("="*70)
# Deser-Levin: kappa = H/sqrt(1-b^2)  <=> kappa^2 = a^2+H^2, b=a/kappa.
# Express b in terms of a,H:
b_of_aH = a/sp.sqrt(a**2 + H**2)
print("b(a,H) = a/sqrt(a^2+H^2) =")
sp.pprint(b_of_aH)
print()
# Edge condition b = c_chi : solve for the acceleration a_edge.
a_edge = sp.solve(sp.Eq(b_of_aH, cchi), a)
print("Solve b(a,H)=c_chi for a_edge:")
sp.pprint(a_edge)
print()
# Take the positive root.
a_edge_pos = [s for s in a_edge if sp.ask(sp.Q.positive(s)) is not False]
print("a_edge (positive branch):")
sp.pprint(a_edge_pos)
print()
print("Read-off: a_edge = H * c_chi / sqrt(1 - c_chi^2)  for c_chi<1.")
print("  * For c_chi>1 (the banked super-luminal corner c_chi^2 in")
print("    [1.000,1.033]) there is NO real a_edge: b=a/kappa<1 ALWAYS, so")
print("    b=c_chi>1 is UNREACHABLE on physical worldlines.  The sonic edge")
print("    b=c_chi is NOT on any timelike-worldline caustic for c_chi>1.")
print("  * The edge ties a (acceleration, a worldline label) to (c_chi,H) but")
print("    leaves BOTH c_chi and H free: it is a 1-parameter family, NOT a")
print("    relation c_chi=f(H).  H and c_chi can be varied independently and")
print("    a_edge simply tracks them.  No lock.")

print()
print("="*70)
print("PART 3 (c1'): is there ANY a_edge eliminating c_chi between two")
print("              edge conditions? (test for an over-determination lock)")
print("="*70)
# A lock would arise if TWO independent dS-invariant conditions both had to
# hold at the edge, over-determining and eliminating to give c_chi=f(H).
# Condition A: edge b=c_chi.  Condition B: edge sits at the horizon b=1
# (modular fixed point).  Both => c_chi=1.  Solve:
sol = sp.solve([sp.Eq(b, cchi), sp.Eq(b, 1)], [b, cchi], dict=True)
print("Require edge (b=c_chi) AND horizon (b=1) simultaneously:")
sp.pprint(sol)
print("=> c_chi=1.  The over-determination forces the LUMINAL value, with NO H.")
print("   Again: H drops out; the only forced value is c_chi=1 (no scale-lock,")
print("   and it decouples the edge).")

print()
print("="*70)
print("PART 3 (c2): dilatation weight of the edge equation b=c_chi")
print("="*70)
# Under the surviving dilatation D: s -> e^l s, proper time tau and the
# chord co-scale; kappa has weight -1 (inverse length), a (acceleration) has
# weight -1, H has weight -1 (all inverse-length). b=a/kappa is a RATIO of two
# weight-(-1) objects => WEIGHT 0 (dimensionless), dilatation-INVARIANT.  Good:
# b is invariant.  But c_chi is ALSO weight 0 (a pure speed ratio).  So the
# edge equation b=c_chi is an equation between two weight-0 objects — it is
# dilatation-COVARIANT (both sides invariant).  Does that HELP?  No: a relation
# between two invariants is preserved by the dilatation but the dilatation
# supplies NO new constraint tying them.  The dilatation fixes weight-0
# invariants only up to their initial values — it cannot generate c_chi=f(H).
l = sp.symbols('l', real=True)  # dilatation parameter
w_kappa, w_a, w_H, w_b, w_cchi = -1, -1, -1, 0, 0
print(f"dilatation weights: [kappa]={w_kappa} [a]={w_a} [H]={w_H} "
      f"[b]={w_b} [c_chi]={w_cchi}")
print("b=a/kappa: weight =", w_a - w_kappa, "(invariant). c_chi: weight 0 (invariant).")
print()
print("Both sides of b=c_chi are dilatation-INVARIANTS (weight 0).")
print("A dilatation maps invariants to themselves => it preserves the edge")
print("equation but generates NO relation between c_chi and H.")
print("Mirror of agentSS: there the gain ratio had weight -1 vs a weight-0")
print("target (a dilation slides it, pins nothing). HERE the edge is weight-0")
print("on both sides (a dilation cannot move it AT ALL) — so the dilatation")
print("has even LESS purchase to force c_chi=f(H). It is structurally inert.")
print()
print("KEY: H itself is weight -1 (a scale), c_chi is weight 0 (a modulus).")
print("A relation c_chi=f(H) would need f(H) to be DIMENSIONLESS, i.e. f(H)")
print("could only be a PURE NUMBER (H^0) or a ratio H/H_ref with an external")
print("reference scale H_ref. dS has NO second scale (single-scale background).")
print("So the only dilatation-consistent 'lock' is c_chi=const (no H) — i.e.")
print("NOT a scale-lock. The symmetry forbids a genuine c_chi=f(H) by weight.")
