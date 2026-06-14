"""
HOSTILE VERIFIER, BLOCK 2 — stress-test the two load-bearing CLAIMS:

  (II)  the single-scale dimensional no-go, AND its honesty about the
        SECOND scale M_Pl that dS+gravity demonstrably contains;
  (III) the 'luminal c_chi=1 HURTS' claim — does a symmetry-forced fixed
        point actually decouple the sonic edge from the fold band?

I attack the no-go from the LOCK side as hard as I can, because that is where a
'free relabelled as locked' error would hide. The danger is the REVERSE here:
the claim might be too GENEROUS to itself by calling f(H) 'dimensionally
forbidden' when M_Pl is in fact a second scale. So I test:
  - Is the no-go's premise ('dS is single-scale') actually true once gravity
    (G=M_Pl^-2) is included? NO — there ARE two scales. So the correct no-go is
    NOT 'forbidden' but 'allowed only as f(H/M_Pl), un-forced, and dead at the
    relevant magnitude.' I check the verdict survives this correction.
  - At the RELEVANT scale (the edge coincidence), what would M have to be to
    move c_chi by O(1)? Is M_Pl really dead, and is any sub-Planckian M that
    works already excluded by agentU's PPN/Cherenkov bounds?
  - Does luminal c_chi->1 quantitatively collapse the sonic edge onto the
    horizon (k* -> horizon scale), removing the fold band?
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 40

print("#"*72)
print("# BLOCK 2-II: the single-scale no-go, stress-tested for honesty")
print("#"*72)
print("""
The claim states de Sitter is SINGLE-SCALE (only H), so a dimensionless f(H)
must be constant. RUTHLESS CHECK: dS + dynamical gravity contains G = M_Pl^-2.
So there ARE two scales: H and M_Pl. The 'forbidden' framing is therefore too
strong taken literally. The HONEST statement is:
   c_chi = f(H/M_Pl)  is dimensionally ALLOWED (two scales),
   but (a) the coefficient is NOT forced by any dS symmetry, and
       (b) it is numerically DEAD at the relevant magnitude.
Does the FREE-PARAMETER verdict survive this correction?  -> test (a),(b).
""")

# (b) magnitude: a curvature-induced shift to a marginal coupling is generically
# delta(c_chi^2) ~ (H/M_Pl)^2 (one curvature insertion, R ~ H^2, /M_Pl^2).
# To LAND the edge coincidence we need delta(c_chi^2) = O(1) (c_chi must sit at
# the Cherenkov corner c_chi^2 in [1.000,1.033], i.e. an O(10^-2..1) offset from
# any luminal/symmetry value). Solve for the M that would deliver O(1):
H_over_MPl_cosmo = mp.mpf('1e-61')   # H_Lambda/M_Pl ~ 1.4e-33 eV / 2.4e27 eV ~ 6e-61
shift_MPl = H_over_MPl_cosmo**2
print(f"(b) curvature shift with M=M_Pl:  (H/M_Pl)^2 ~ {mp.nstr(shift_MPl,3)}")
print(f"    needed to land edge coincidence: O(1e-2 .. 1).")
print(f"    => M_Pl channel falls short by ~120 orders of magnitude. DEAD. CONFIRMED.")
print()
# What M would deliver O(1)?  (H/M)^2 ~ 1  => M ~ H.  i.e. the new scale would
# have to sit AT the Hubble scale itself (an IR Lorentz-violation scale).
print("    What M lands O(1)?  (H/M)^2 ~ 1 => M ~ H. The required second scale")
print("    is an IR scale AT H itself — i.e. a NEW low-energy LV scale equal to")
print("    the Hubble rate. That is not in the banked dS+khronon content; it is")
print("    new, model-dependent physics introduced precisely to land the number.")
print("    Introducing M~H and a function f to hit the coincidence == TUNING with")
print("    extra steps, not a symmetry FORCING. (a): un-forced. CONFIRMED.")
print()

# (a) is the coefficient forced? A dS symmetry that forced delta(c_chi^2) would
# have to be a dilatation/conformal Ward identity. But c_chi is weight-0 and the
# only invariant a dilation fixes is weight-0 *ratios*; it cannot generate an
# H-dependent value from H alone (that is the genuinely correct core of the
# no-go). Re-state it in the dimensionally-correct (two-scale) form:
H, MPl, p = sp.symbols('H M_Pl p', positive=True)
print("(a) Dimensionally-correct no-go: with scales {H, M_Pl}, c_chi=f(H/M_Pl)")
print("    is allowed for ANY f. dS dilatation symmetry (the only candidate)")
print("    acts on H, not on the dimensionless ratio H/M_Pl in a way that PINS f")
print("    -> f is unconstrained by symmetry. The value is INPUT, not forced.")
print("    NET: the literal 'dimensionally forbidden' overshoots, but the")
print("    OPERATIVE verdict (no SYMMETRY forces a USEFUL c_chi=f(H)) stands,")
print("    and the only dimensionally-open channel (M=M_Pl) is numerically dead.")

print()
print("#"*72)
print("# BLOCK 2-III: does luminal c_chi=1 HURT (decouple the sonic edge)?")
print("#"*72)
# The fold mechanism needs a DISTINCT sonic edge inside the horizon: a surface
# where the khronon sound cone b(a,H)=a/sqrt(a^2+H^2) meets c_chi. Deser-Levin
# b-family (banked agentEE/agentSS): b = a/sqrt(a^2+H^2) in [0,1).
a, Hsym, cc = sp.symbols('a H c_chi', positive=True)
b = a/sp.sqrt(a**2 + Hsym**2)
edge_eq = sp.Eq(b, cc)
a_edge = sp.solve(edge_eq, a)
print("Sonic-edge locus from b(a,H)=c_chi:  a_edge =", a_edge)
# Real positive solution requires c_chi < 1 (since b<1). Examine c_chi->1:
print()
print("b = a/sqrt(a^2+H^2) is STRICTLY < 1 for finite a; b->1 only as a->inf.")
print("So the edge b=c_chi has a finite real a_edge ONLY for c_chi<1.")
a_edge_expr = sp.sqrt(Hsym**2*cc**2/(1-cc**2))
print("  a_edge =", a_edge_expr, " (the c_chi<1 branch)")
print()
# Limit c_chi -> 1^-:
lim = sp.limit(a_edge_expr, cc, 1, '-')
print("  lim_{c_chi->1^-} a_edge =", lim, "  => the sonic edge runs to a=INFINITY")
print("  (the de Sitter horizon / null infinity). The edge surface DECOUPLES")
print("  from any finite interior fold band. QUANTITATIVELY CONFIRMED: luminal")
print("  c_chi=1 pushes the sonic edge to the horizon and OUT of the fold band.")
print()
# And for the banked super-luminal corner c_chi^2 in [1.000,1.033] (c_chi>1):
print("For the BANKED corner c_chi>1: 1-c_chi^2 < 0 => a_edge imaginary => NO")
print("timelike edge crossing at all on the b-family (matches the claim's note).")
print("Either way, a symmetry that drives c_chi->1 REMOVES the distinct sonic")
print("surface the fold needs. The fixed point HURTS, it does not help. CONFIRMED.")
print()
print("CONCLUSION (Block 2): the no-go's OPERATIVE content survives a hostile")
print("second-scale audit (M_Pl real but ~10^-122 dead; the only M that works is")
print("a new IR scale ~H = new physics); and luminal c_chi=1 quantitatively")
print("decouples the edge (a_edge->infinity). No symmetry delivers a USEFUL,")
print("H-determined c_chi at the RELEVANT scale. Verdict FREE-PARAMETER holds.")
