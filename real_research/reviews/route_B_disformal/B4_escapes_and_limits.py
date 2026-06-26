"""
ROUTE B -- B4. Close the escapes honestly (both-ways), then verify the remaining 4 limits.

Literature anchor (verified firsthand):
 - Sanders' STRATIFIED theory = disformal coupling to a CONSTANT TIMELIKE 4-vector, "gives the
   correct lensing while retaining MOND" (Bekenstein-Sanders). This is the EXACT structure of Route B.
 - "Does GW170817 falsify MOND?" (1805.06804): Sanders-stratified + TeVeS + disformal-timelike are
   EXCLUDED (c_GW != c). The SURVIVOR (Skordis-Zlosnik/AeST) uses CONFORMAL-ONLY scalar coupling.
 - Horndeski speed tests (2407.20339): photon & graviton cones CAN be made equal -- but only by
   modifying BOTH cones the SAME way (a shared gravitoelectric coupling), i.e. moving GRAVITY too.

So Route B (gravity standard + disformal matter coupling) is the historically-killed branch. We now
(A) close the two steelman escapes with sympy, then (B) check Newtonian / deep-MOND / cosmo limits.
"""
import sympy as sp

print("="*78)
print("B4-A1. ESCAPE 1: disformal vector = matter's OWN 4-velocity u (genuine MI), not cosmic A.")
print("="*78)
print("""
Claim to test: if g~ = C g + D u_mu u_nu with u = the MASSIVE particle's 4-velocity, then PHOTONS
(null, no rest frame, not 'the particle') do not see D -> c_photon = c_graviton, GW safe; only
massive matter feels the MI. Does this work AND still lens?
""")
# If only massive matter couples to g~=C g + D u u, photons couple to g (or to C g). Then:
#  - GW/photon cone: photon sees g (or conformal C g) -> c_photon = c_graviton EXACT.  GW SAFE.
#  - BUT lensing: photons then see ONLY the baryon metric g -> ZERO phantom deflection.
print(" - GW cone: photons see g (or C g, conformal) -> c_photon=c_graviton. GW170817 PASSES.")
print(" - Lensing: photons see baryon metric only -> NO phantom lensing. This is EXACTLY the")
print("   metric-passive MI lensing gap (agentC lensing-RAR wall): under-predicts g-g lensing.")
print(" - Worse: u_mu u_nu requires a rest frame; for the COLLECTIVE field sourcing lensing you")
print("   need a frame for the bulk matter = back to a cosmic A^mu (the dS-comoving congruence),")
print("   i.e. ESCAPE 1 collapses into the killed timelike-A case the moment matter clumps lens.")
print("""
 VERDICT ESCAPE 1: it RESOLVES the GW problem but RE-OPENS the lensing gap -- the two cannot be
 satisfied together. A velocity-disformal that photons ignore cannot lens; one that photons feel
 (so it lenses) needs a frame and breaks GW. This is the SAME trade B3 found, restated. NO ESCAPE.
""")

print("="*78)
print("B4-A2. ESCAPE 2: move BOTH cones equally (graviton sees a disformal metric too).")
print("="*78)
print("""
Horndeski-speed-test escape (2407.20339): c_photon=c_graviton if the SAME disformal structure dresses
the graviton kinetic term. But that means S_gravity is NOT pure (c^4/16piG)R on g -- gravity is
MODIFIED (the graviton cone is moved by the A A term). That is precisely AeST / modified GRAVITY,
NOT Route B's premise (gravity standard, modification on the matter side). So Escape 2 EXITS Route B
and LANDS on AeST -- the sibling modified-gravity EFT the JOIN_VERDICT already adjudicated. It is not
a disformal-matter-coupling theory anymore.
""")
# Make the 'both cones equal' condition explicit: c_photon^2=(C-D)/C must equal c_grav^2.
# c_grav^2=1 (pure R) forces D=0. To get c_grav^2=(C-D)/C too, the graviton must couple to g~ -> R(g~)
# -> modified gravity. sympy: the equality holds for D!=0 ONLY if c_grav^2 is ALSO (C-D)/C:
C, D = sp.symbols('C D', positive=True)
c_ph2 = (C-D)/C
print("  c_photon^2 = (C-D)/C ; pure-R c_grav^2 = 1.")
print("  equal & D!=0  =>  c_grav^2 must also be (C-D)/C  =>  graviton couples to g~  => MODIFIED GRAVITY.")
print("  -> EXITS Route B. (This is the AeST branch, separately adjudicated PARTIAL/sibling.)")

print("\n" + "="*78)
print("B4-B. THE FOUR LIMITS for the (now-cornered) Route-B disformal action.")
print("  We grant the NONLOCAL gate (B2b) so the test law holds, and check each limit's status.")
print("="*78)

# ---- (1) NEWTONIAN limit: mu_fw->1, D->0 -------------------------------------
print("\n(1) NEWTONIAN (high a, a/a0->inf):")
x = sp.symbols('x', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
print("    mu_fw(x->inf) =", sp.limit(mu_fw,x,sp.oo), "-> inertia standard.")
print("    gate D ~ (1-mu_fw) ->", sp.simplify(sp.limit(1-mu_fw, x, sp.oo)), "-> g~ -> C g (conformal/Newtonian).")
print("    With C->1: g~->g, S_matter -> GR+SM.  PASS (test-particle), inherited from the gate.")

# ---- (2) DEEP-MOND limit: mu_fw->x, v^4=GM a0 (BTFR) ------------------------
print("\n(2) DEEP-MOND (low a):  mu_fw->x => m a (a/a0) = F = GMm/r^2 => a^2/a0 = GM/r^2")
G,M,r,a0s,v = sp.symbols('G M r a0 v', positive=True)
a_dm = sp.sqrt(G*M*a0s)/r            # from a^2/a0 = GM/r^2 => a = sqrt(GM a0)/r
# circular: a = v^2/r => v^2 = a r = sqrt(GM a0) => v^4 = GM a0
v4 = sp.simplify((a_dm*r))**2
print("    a_deepMOND = sqrt(GM a0)/r ; circular v^2=a r =>")
print("    v^4 =", sp.simplify((a_dm*r)**2), " = G M a0  -> BTFR. PASS (test-particle).")
print("    LENSING in deep-MOND: requires D~O(1) -> the GW-fatal regime (B3). So dynamics PASS,")
print("    but the LENSING that deep-MOND needs is exactly what GW170817 forbids. CONDITIONAL/FAIL.")

# ---- (3) COSMOLOGICAL limit ------------------------------------------------
print("\n(3) COSMOLOGICAL (CMB-safe):")
print("    A^mu = the dS-comoving frame = u^mu_cosmic. In FRW, A_mu=(-1,0,0,0) (a(t) factored),")
print("    so g~_munu = C g_munu + D A_mu A_nu shifts only g~_00 -> renormalizes the lapse/time.")
print("    This is a homogeneous redefinition of cosmic time for matter vs gravity. It DOES alter")
print("    the matter sound speed c_s^2=(C-D)/C and the photon-baryon cone at recombination ->")
print("    shifts acoustic-peak positions unless D->0 at high-z high-a. The gate: at recombination")
print("    a_ambient >> a0 (dense plasma) so D->0 -> g~->Cg -> CMB-safe ONLY in the gated/high-a")
print("    epochs. In voids/late-time low-a, D~O(1) -> ISW/lensing-of-CMB and the GW issue recur.")
print("    STATUS: CMB-safe at recombination via the gate; NOT safe for late-time low-a CMB lensing.")

# ---- (4) GW limit ----------------------------------------------------------
print("\n(4) GRAVITATIONAL WAVES (c_T=c):")
print("    c_graviton=c EXACT (pure R). c_photon^2=(C-D)/C != c whenever D!=0 on the path.")
print("    Deep-space GW path is LOW-a -> gate OPEN -> D~O(1) -> |c_ph/c-1|~O(1) >> 5e-16. FAIL.")
print("    (This is the Sanders-stratified exclusion, reproduced from first principles.)")

print("\n" + "="*78)
print("LIMITS LEDGER (Route B, disformal matter coupling to a preferred timelike frame):")
print("="*78)
print("""
  (1) Newtonian     : PASS   (gate -> g~->Cg->g; GR+SM recovered)
  (2) deep-MOND     : PASS for DYNAMICS (BTFR v^4=GMa0); but the LENSING it needs is GW-fatal
  (3) cosmological  : CONDITIONAL (CMB-safe at recombination via gate; late-time low-a unsafe)
  (4) GW c_T=c      : FAIL on the matter/photon cone (c_photon!=c_graviton when D!=0; gate OPEN
                      on the low-a GW path) -> the GW170817 exclusion of disformal-timelike MOND.
  GHOST             : the gate must be NONLOCAL (B2); LOCAL acceleration-disformal = Ostrogradski.
                      Granting nonlocal: ghost-free by Milgrom-94's 'blessing'. The disformal A A
                      term itself adds no NEW propagating dof if A is non-dynamical (frame), but a
                      non-dynamical timelike A breaks Lorentz softly (acceptable) -- IF A is made
                      DYNAMICAL to be covariant, it is the AeST aether (exits Route B again).
""")
