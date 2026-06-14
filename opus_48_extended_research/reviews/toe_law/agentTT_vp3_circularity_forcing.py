"""
HOSTILE VERIFIER VP3 — THE LINCHPIN: is the edge-exclusion an INDEPENDENT rep-theoretic FORCING,
or the SAME pole data as agentS's t^{-3/2} relabeled (CONSISTENCY/sharpening)?
Mission step (3): respect agentR's 'terminal at the algebra' — has anything been DERIVED, or restated?

I test the route's ATTACK-1 claim from BOTH hostile directions:

  (D1) PRO-FORCING: is there an INDEPENDENT input the rep argument uses that agentS did NOT —
       e.g. a Tomita-Takesaki/Bisognano-Wichmann UNIQUENESS theorem that, ON THE GRAVITY SIDE ALONE,
       fixes the matter modular operator to the GH boost only at theta_v=pi/2? If yes, the rep
       argument could be a genuine 2nd forcing and the grade should rise toward FORCED.

  (D2) ANTI-FORCING (the route's own claim): is the rep-class label of BOTH placements computed
       PURELY from the matter-2pt pole positions {omega_pole(theta_v,k)} — the SAME object agentS
       fed to get t^{-3/2}? If yes, the rep argument adds NO independent exclusion; it is the
       reproduce-dS-relaxation conditional restated. => CONSISTENCY/sharpening, not forcing.

DECISIVE LOGICAL TEST for (D2): take the rep-class verdict as a FUNCTION of its inputs. If
rep_class(placement) = f(pole positions only), and pole positions = the agentS discriminator input,
then rep_class is INFORMATIONALLY DOWNSTREAM of agentS — a strictly weaker-or-equal statement, never
an independent forcing.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*80)
print("VP3 — FORCING (independent exclusion) vs CONSISTENCY (same pole data, relabeled)?")
print("="*80)

# ---------------------------------------------------------------------------------
# (D2 first) What ARE the inputs to the rep-class label, explicitly?
# ---------------------------------------------------------------------------------
print("""
[D2] INPUT-TRACE of the rep-class verdict (what does the discrete/principal/continuum label
     actually depend on?):

  Side A (GH): the discrete series D^+_Delta with ladder {Delta+n} is the TARGET. It is a fact
    about the dS HORIZON's own relaxation (QNM spectrum). It is fixed independently of theta_v.
    It does NOT, by itself, say anything about WHICH chord placement realizes it.

  Side B (matter): the rep CLASS of the boost-about-|theta_v> is read off:
       omega_pole(theta_v, k) = cos(theta_v)cosh(u_k) - i sin(theta_v)sinh(u_k).
     - 'discrete series' <=> Re omega_pole = 0 for all k  <=> cos(theta_v)=0  (pure-imaginary ladder)
     - 'not discrete / continuum-edge' <=> Re omega_pole != 0 AND poles exit band.
     The ENTIRE discriminator is a property of {omega_pole(theta_v,k)} — the pole POSITIONS.

  agentS's t^{-3/2} discriminator input: the SAME pole positions omega_pole(theta_v,k)
     (sub-threshold the contour sweeps no poles -> Watson-lemma sqrt-edge -> t^{-3/2}).

  => Both the rep-class label AND agentS's t^{-3/2} are FUNCTIONS OF THE SAME OBJECT:
     the matter-2pt pole set. The rep label is informationally DOWNSTREAM of (not independent of)
     the agentS pole data.
""")

# Demonstrate concretely: the SAME quantity (Re omega_pole) drives BOTH the rep class AND
# the pole-in/out-of-band fact that agentS uses for t^{-3/2}.
Delta, k, lam = sp.symbols('Delta k lambda', positive=True)
theta_v = sp.symbols('theta_v', real=True)
u = (Delta + k)*lam
re_w = sp.cos(theta_v)*sp.cosh(u)
im_w = -sp.sin(theta_v)*sp.sinh(u)
floor = sp.cos(sp.pi - theta_v)  # not used; band floor is cos(eps)-1, eps=pi-theta_v
print("  SHARED quantity Re omega_pole = cos(theta_v)cosh(u):")
print("    - rep-class test: =0 <=> discrete series (center).")
print("    - agentS band-exit test: < cos(eps)-1 <=> pole leaves support => t^{-3/2}.")
print("  Both tests are evaluations of the SAME Re omega_pole. No second, independent input enters.")

# ---------------------------------------------------------------------------------
# (D1) PRO-FORCING: is there an INDEPENDENT gravity-side theorem the route could have used
#      to FORCE the matter modular operator to coincide with the GH boost ONLY at center?
# ---------------------------------------------------------------------------------
print("""
[D1] PRO-FORCING search: does any INDEPENDENT theorem fix matter-modular = GH-boost at center?

  Candidate: Tomita-Takesaki UNIQUENESS — for a von Neumann algebra M with cyclic-separating
  vector |Omega>, the modular operator Delta_Omega and modular flow sigma_t are UNIQUE. If one
  could show the matter algebra's modular flow about |theta_v> EQUALS the GH static-patch boost
  ONLY for theta_v=pi/2, that would be an algebra-INTERNAL forcing (independent of 'reproduce
  dS relaxation').

  THE OBSTRUCTION (why this does NOT upgrade to forcing — checked, not assumed):
   (i) Tomita-Takesaki gives a UNIQUE modular flow PER STATE. Each placement |theta_v> is a
       DIFFERENT cyclic vector => a DIFFERENT (its own) modular flow. T-T does NOT say which
       placement's modular flow equals the GH boost; it guarantees each HAS one.
   (ii) To single out theta_v=pi/2 one must DEMAND 'the matter modular flow = the GH static-patch
        boost'. But that demand IS 'the matter sector reproduces the dS (GH) relaxation' — the
        agentS conditional, now stated operator-wise. T-T uniqueness does not SUPPLY that demand;
        it only says IF two flows agree THEN the generators agree.
   (iii) The chord algebra (VP2 S-B) is a SINGLE continuum rep admitting BOTH placements, so there
        is no algebra-internal superselection forcing the GH boost onto one vacuum.
  => No independent gravity-side theorem upgrades the exclusion. The 'only at center' is the
     TARGET-matching demand, not an a-priori algebra constraint. (This matches Route-2's own
     honest residual: the boost is INNER/diagonal on theta_v, cannot rotate edge->center; and
     'dS vacuum = GH boost-KMS state' is the framework's presupposed identification.)
""")

# Numerically witness the inner/diagonal fact: the boost (energy) is conserved => theta_v fixed.
print("  WITNESS that the boost is diagonal on the placement (cannot move theta_v):")
print("    Boost charge = energy E_v = cos(theta_v) (q-rescaled). Boost flow: |E_v> -> e^{iE_v t}|E_v>.")
for tv in [mp.pi/2, mp.pi - mp.mpf('1e-3')]:
    Ev = mp.cos(tv)
    print(f"    theta_v={float(tv):.5f}: E_v={float(Ev):+.5f} CONSERVED under boost -> theta_v UNMOVED.")
print("    => the boost cannot dynamically carry edge into center: selection is fixed-point/target,")
print("       NOT a symmetry that forbids the edge. Confirms FAVORED, not FORCED.")

print("\n" + "="*80)
print("VP3 RESULT — the linchpin")
print("="*80)
print("(D2) The rep-class label of BOTH placements is a function of the matter-2pt POLE POSITIONS")
print("     ONLY — the SAME object agentS used for t^{-3/2}. The rep argument is informationally")
print("     DOWNSTREAM of agentS: it RESTATES the same discriminator as a clean rep-class label,")
print("     it does not add an independent exclusion. => CONSISTENCY/SHARPENING, NOT a new FORCING.")
print("(D1) No independent gravity-side theorem (Tomita-Takesaki uniqueness incl.) forces the matter")
print("     modular flow = GH boost only at center; T-T gives one flow PER state, and singling out")
print("     center requires DEMANDING matter-modular=GH-boost = agentS's reproduce-dS-relaxation.")
print("     The boost is diagonal on theta_v (inner) -> cannot rotate edge->center.")
print("VERDICT: the modular argument is a CONSISTENCY (center fits exactly + uniquely; edge off-")
print("         target) SHARPENED to a rep-class statement — NOT a FORCING (edge not excluded by")
print("         representation theory acting alone; it survives as an admissible chord-algebra sector).")
