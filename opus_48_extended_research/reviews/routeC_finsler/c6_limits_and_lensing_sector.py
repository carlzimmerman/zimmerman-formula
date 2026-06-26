"""
Route C / step 6.  Close the four limits for the TWO honest Finsler readings, and state the
lensing/metric-sector status from the primaries.

Reading (I)  -- the framework's TARGET: acceleration-keyed MI (mu_fw(|a|/a0)).
   Established c1-c4: NOT an ordinary Finsler structure; the local acceleration-Finsler
   (Lagrange/Kawaguchi) Lagrangian that reproduces it is either wrong-order or Ostrogradski-
   ghost.  So Reading (I) has NO healthy local Finsler action -- the limits below are the
   limits of the MI LAW itself (which the framework already has at the worldline level), not
   of a new Finsler field theory.

Reading (II) -- the LITERATURE's Finsler MOND (Chang-Li / Finslerian-lensing): velocity-keyed
   MODIFIED GRAVITY, g_obs = g_bar nu(g_bar/a0) = sqrt(g_bar^2+g_bar a0).  This DOES have a
   covariant Finsler action (Pfeifer-Wohlfarth on the tangent bundle) and a lensing sector
   (GR angle x Finslerian rescaling) -- but it is the AeST/AQUAL sibling (modified gravity),
   NOT the framework's MI, and its lensing factor is an UNDERIVED hypothesis (3 free params).

We sympy the four limits for the LAW g_obs=sqrt(g_bar^2+g_bar a0) (shared by both readings on
static circular orbits -- the degeneracy), and report the GW/ghost/lensing status per reading.
"""
import sympy as sp

gbar, a0, c = sp.symbols('g_bar a_0 c', positive=True)
g_obs = sp.sqrt(gbar**2 + gbar*a0)

print("="*78)
print("FOUR LIMITS of the shared static law g_obs = sqrt(g_bar^2 + g_bar a0)")
print("="*78)

# 1. Newtonian: g_bar >> a0
newt = sp.series(g_obs, a0, 0, 2).removeO()
print("1. NEWTONIAN (a0->0):  g_obs ->", sp.simplify(newt.subs(a0,0)),
      " ; leading correction:", sp.simplify(newt - gbar))
print("   PASS: g_obs -> g_bar  (mu_fw->1, GR+SM recovered).")

# 2. deep-MOND: g_bar << a0
deep = sp.sqrt(gbar*a0)
deep_check = sp.limit(g_obs/deep, gbar, 0)
print("2. DEEP-MOND (g_bar->0):  g_obs/sqrt(g_bar a0) ->", deep_check,
      " => g_obs -> sqrt(g_bar a0).")
# BTFR v^4 = G M a0
G, M, r, v = sp.symbols('G M r v', positive=True)
# circular: v^2/r = g_obs = sqrt(g_bar a0) = sqrt(GM/r^2 * a0)
v2 = r*sp.sqrt(G*M/r**2*a0)
v4 = sp.simplify(v2**2)
print("   v^2 = r*g_obs =", v2, " ; v^4 =", v4, " = G M a0  (BTFR).  PASS.")

# 3. cosmological / CMB-safe: the law is a quasistatic acceleration relation; both readings
#    reduce to GR at high z (early universe is high-acceleration, a>>a0 => mu_fw->1 => GR).
print("3. COSMOLOGICAL: early universe a>>a0 => mu_fw->1 / nu->1 => GR limit => CMB-safe at")
print("   the background level (same as MOND/AeST class).  For Reading II the FULL AeST host")
print("   is CMB-fitted (Skordis-Zlosnik); for Reading I the MI sector has no cosmo field eq")
print("   (no covariant action) -- cosmology is INHERITED from the host, not from Finsler.")

# 4. GW speed c_T = c.
print("4. GW SPEED: Reading II (Pfeifer-Wohlfarth/Berwald-Finsler) propagates the metric")
print("   perturbation; for the Berwald (Riemann-reducible) class c_T=c by construction in")
print("   the GR-limit boundary term.  Finsler birefringence/anisotropy is the GENERIC risk")
print("   (Lorentz-violation, 2304.12767) -- c_T=c only in the Berwald/near-Riemann corner.")
print("   PASS-CONDITIONAL (Berwald corner); Reading I has no propagating Finsler GW sector.")

print()
print("="*78)
print("GHOST STATUS per reading")
print("="*78)
print("""
Reading (I) acceleration-keyed MI Finsler: GHOST (Ostrogradski) for any local nondegenerate
   acceleration-Lagrangian (c3: T''!=0 everywhere -> H linear in P1, unbounded).  Healthy
   only as a NONLOCAL-in-time functional (the established Galley worldline route), which is
   NOT a finite-order Finsler structure.  => no healthy local Finsler action for the MI.
Reading (II) velocity-keyed MG Finsler: GHOST-FREE in the Berwald/near-Riemann corner
   (it is essentially a disformal/AeST-class metric theory); the Finsler anisotropy is a
   Lorentz-violation/birefringence risk outside that corner.  Same ghost status as AeST.
""")

print("="*78)
print("LENSING / METRIC SECTOR (the Bullet-Cluster question), from the primaries")
print("="*78)
print("""
Reading (II) DOES supply a metric/lensing sector: Chang-Li modify h00 (a real metric
potential), and Finslerian-MOND-lensing (1309.1343) gives light-deflection = GR-angle x a
'Finslerian rescaling factor', fitting early-type-galaxy strong lenses and (with added
dipole+quadrupole) the Bullet Cluster WITHOUT dark matter.  BUT verbatim caveats:
  * 'we do not know how to write the energy-momentum tensor on the bundle ... we cannot
     solve the field equations to derive the Finslerian rescaling factor f_v(r). The factor
     ... is just a HYPOTHESIS.'  -> the lensing factor is FITTED, not derived from an action.
  * THREE free parameters (a0, r_c, v_c); 'one can choose the parameters such that the
     gravitational mass exactly matches' -> the metric sector is UNDERDETERMINED.
  * a0 inserted by hand (=1.2e-10 in the rotation-curve fit); Lambda only NOTED
     (2 pi a0 ~ c sqrt(Lambda/3)), never derived; NOT the framework's 9.36e-11 nor kappa.
Reading (I): the framework's MI leaves the metric UNDETERMINED at the particle level (pure
   MI doesn't say how light bends) -- exactly the session's known gap; Finsler does NOT close
   it for the MI reading (Reading I has no Finsler metric at all).
""")
print("STEP 6 done.  Assembling verdict.")
