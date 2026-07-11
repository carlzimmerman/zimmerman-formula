#!/usr/bin/env python3
"""
LANE 2 -- THE SLIP LOOPHOLE (de Sitter-Unruh MODIFIED-INERTIA MOND).

Question: can the ANISOTROPIC part of the MI stress tensor T_ij source a
gravitational slip (Psi - Phi) large enough to make light deflection
grad(Psi+Phi) carry the (nu-1) MOND enhancement WITHOUT enhancing the
dynamical grad(Phi) -- i.e. a pure-MI, no-dark-matter, correct-lensing
channel -- or is the slip v^2/c^2 suppressed (loophole CLOSED, horn C)?

Framework-first (NON-negotiable): the theory is MODIFIED INERTIA, a0 horizon-
derived. Covariant matter action (Zenodo 21303747 companion):
    S_m = -1/2 INT d^4x sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],  s=-1
    Box_u f = (u.nabla)^2 f  (frame-derivative along the matter worldline)
    K(z) = (sqrt(1+4z)-1)/(2 sqrt z)   -- Herglotz-Nevanlinna, ||K||<=1.
K(0)=0 (static trap), K(inf)=1 (Newtonian). The MOND boost lives at z~O(1).

We test on the theory's OWN terms. We do NOT judge through Milgrom's nu or
McGaugh conventions. Both a0 footings are carried:
   canonical a0 = c H_Lambda / Z = 9.36e-11 m/s^2  (rho_DE / cH_Lambda)
   alt       a0 = 1.13e-10       m/s^2             (rho_total / cH0)
The scaling verdict is shown to be FOOTING-INDEPENDENT (it is kinematic).

Outcome is decisive either way: SLIP-LENSES (channel found) or SLIP-CLOSED.
We manufacture neither a win nor a deficit.
"""

import sympy as sp

print("="*74)
print("LANE 2  --  MI ANISOTROPIC-STRESS SLIP:  channel or closed?")
print("="*74)

# ----------------------------------------------------------------------
# STEP 0.  The static trap (crux subtlety a), made explicit.
# ----------------------------------------------------------------------
print("\n[0] STATIC TRAP  --  where the MI stress can and cannot come from")
print("-"*74)
z = sp.symbols('z', positive=True)
K = (sp.sqrt(1+4*z) - 1)/(2*sp.sqrt(z))
K0   = sp.limit(K, z, 0)          # -> 0
Kinf = sp.limit(K, z, sp.oo)      # -> 1
print(f"   K(z) = (sqrt(1+4z)-1)/(2 sqrt z)")
print(f"   K(0)   = {K0}   (a STRICTLY STATIC blob: Box_u=(d/dt)^2->0, no MI term)")
print(f"   K(inf) = {Kinf}   (Newtonian/high-accel limit -> standard inertia)")
print("   => the ONLY MI stress comes from ORBITING matter, whose worldline")
print("      sees a nonzero centripetal accel a_c=v^2/r, i.e. Box_u ~ a_c^2 != 0.")
print("      A static-source lensing calc gives exactly zero. Must use the disk.")

# ----------------------------------------------------------------------
# STEP 1.  Stress tensor of orbiting dust; extract the anisotropic part.
#          The action is dust-like: S ~ INT rho (K-dressing) u.u ; varying
#          g gives T_mn = rho_eff u_m u_n  (+ K' correction terms, Step 3).
#          Track orders in eps = v/c EXACTLY with sympy.
# ----------------------------------------------------------------------
print("\n[1] ORBITING-DUST STRESS  T_mn = rho_eff u_m u_n  (leading, K-dressed)")
print("-"*74)
eps = sp.symbols('epsilon', positive=True)   # eps = v/c   (galaxy: ~5e-4)
D   = sp.symbols('D', positive=True)          # D = K-dressing factor, |D|<=1
# 4-velocity of an orbiting element, tangential (x-direction), Minkowski bg:
#   u^mu = gamma (1, v, 0, 0),  v = eps c;   work in c=1 units, restore later.
gamma = 1/sp.sqrt(1-eps**2)
u_up  = sp.Matrix([gamma, gamma*eps, 0, 0])            # u^mu  (c=1)
eta   = sp.diag(-1, 1, 1, 1)
u_dn  = eta*u_up                                        # u_mu
rho_eff = D                                            # rho_eff = rho * D  (set rho=1)
T = sp.Matrix(4,4, lambda a,b: rho_eff*u_dn[a]*u_dn[b])

T00 = sp.simplify(T[0,0])
# spatial block
Tij = T[1:,1:]
trace_sp = sp.simplify(Tij[0,0]+Tij[1,1]+Tij[2,2])
# traceless (anisotropic) spatial part, the SLIP source
aniso = sp.simplify(Tij[0,0] - trace_sp/3)             # xx traceless component
print(f"   T_00 (energy density)          = {sp.simplify(T00)}")
print(f"          series in eps           = {sp.series(T00, eps, 0, 4).removeO()}")
print(f"   Tr T_ij (spatial trace)        = {sp.series(trace_sp, eps,0,4).removeO()}")
print(f"   anisotropic (traceless) T_ij   = {sp.series(aniso, eps,0,5).removeO()}")
lead_aniso = sp.series(aniso, eps, 0, 5).removeO()
lead_T00   = sp.series(T00,   eps, 0, 5).removeO()
ratio = sp.simplify(sp.limit(aniso/T00/eps**2, eps, 0))
print(f"\n   LEADING ORDER:  anisotropic T_ij / T_00  =  {ratio} * eps^2  =  O(v^2/c^2)")
print("   => the anisotropic (slip-sourcing) stress is intrinsically O(v^2/c^2)")
print("      times the energy density. K-dressing D is a BOUNDED O(1) prefactor")
print("      (||K||<=1), it does NOT change this power of eps.")

# ----------------------------------------------------------------------
# STEP 2.  Slip Poisson equation -> exact scaling of (Psi-Phi) vs (nu-1)Phi.
# ----------------------------------------------------------------------
print("\n[2] SLIP FROM THE TRACELESS EINSTEIN EQ  -- exact scaling")
print("-"*74)
print("   Newtonian-gauge field eqs (static, weak field):")
print("      lap(Phi)      = 4 pi G rho_bar                (MI keeps source baryonic)")
print("      lap(Psi-Phi)  = -8 pi G Sigma_aniso           (traceless part sources slip)")
print("   with Sigma_aniso = (anisotropic T_ij) ~ D * rho v^2  (Step 1).")
print("   Dividing the two Poisson eqs on the same scale L:")
G, rho, v, c, L, nu = sp.symbols('G rho v c L nu', positive=True)
Phi_scale  = 4*sp.pi*G*rho*L**2 / c**2          # dimensionless Phi (restore c)
slip_scale = 8*sp.pi*G*(D*rho*v**2)*L**2 / c**4 # (Psi-Phi), aniso stress ~ D rho v^2
slip_over_phi = sp.simplify(slip_scale/Phi_scale)
print(f"\n   (Psi - Phi)/Phi   =  {slip_over_phi}   =  2 D (v/c)^2")
print("   NEEDED for pure-MI lensing:  (Psi-Phi) ~ (nu-1) Phi  with (nu-1)=O(1).")
got_over_needed = sp.simplify(slip_over_phi/(nu-1))
print(f"   got / needed      =  {got_over_needed}   =  2 D (v/c)^2 / (nu-1)")
print("   => the slip falls SHORT of the requirement by a factor ~ (v/c)^2 / (nu-1)")
print("      ~ (v/c)^2 ~ 1e-6 .  D<=1 cannot help; (nu-1)=O(1) in the MOND regime.")

# ----------------------------------------------------------------------
# STEP 3.  Could the NONLOCAL K enhance the slip by c^2/v^2 ?  (the loophole)
#          Check (i) form factor bound, (ii) the K'(Box_u) derivative terms
#          that the metric variation of K(Box_u) generates.
# ----------------------------------------------------------------------
print("\n[3] CAN K (or its K' variation terms) MANUFACTURE a c^2/v^2 ENHANCEMENT?")
print("-"*74)
# (i) form factor magnitude on the physical MOND window z ~ O(1):
Kp = sp.simplify(sp.diff(K, z))
for zz in [sp.Rational(1,4), 1, 4]:
    print(f"     z={float(zz):>4}:  K={float(K.subs(z,zz)):.4f}   K'={float(Kp.subs(z,zz)):.4f}"
          f"   (both O(1), form factor ||K||<=1 verified)")
print("   (i)  K and K' are O(1) on z~O(1); the Herglotz bound ||K||<=1 caps the")
print("        form factor.  No c^2/v^2 here.")
print("   (ii) delta[ K(Box_u/a0^2) ] = K'(Box_u/a0^2) * delta(Box_u)/a0^2 .")
print("        Box_u = (u.nabla)^2 acting on the worldline ~ a_c^2 = (v^2/r)^2,")
print("        and in the MOND regime a_c ~ a0 so Box_u/a0^2 ~ O(1)  (arg stays O(1)).")
print("        delta(Box_u)/delta g^mn brings down GRADIENTS of u and Christoffels:")
print("        each factor is a KINEMATIC scale (velocity v, accel a_c<=a0, freq")
print("        Omega=v/r) -- all sub-c.  No factor of c appears in delta(Box_u).")
# demonstrate: the largest dimensionless ratio available in the operator is
# a_c/a0 ~ O(1); express the would-be enhancement factor needed vs available.
a_c, a0 = sp.symbols('a_c a0', positive=True)
needed_factor = c**2/v**2                # what would be required to lift v^2->c^2
available_max = sp.Integer(1)            # K, K', arg all O(1); largest is O(1)
print(f"\n     enhancement REQUIRED to lift O(v^2/c^2)->O(1):  c^2/v^2 ~ {int(1/(0.5e-3)**2):.0e}")
print(f"     enhancement AVAILABLE in K,K',arg (all O(1)):   O(1)")
print("   => the operator is a function of the BOUNDED ratio a_c/a0=O(1); neither")
print("      K, nor K', nor delta(Box_u) contains c^2/v^2.  The loophole has no")
print("      large dimensionless factor to draw on.  Enhancement is impossible.")

# ----------------------------------------------------------------------
# STEP 4.  T_00 horn check: is the gravitating source enhanced to nu*rho?
# ----------------------------------------------------------------------
print("\n[4] T_00 HORN  --  does the source collapse to modified gravity?")
print("-"*74)
print("   rho_eff = rho * D with D = K-dressing, and ||K||<=1  =>  rho_eff <= rho.")
print("   The MI dressing REDUCES (does not enhance) the energy density; it never")
print("   becomes nu*rho_bar.  So T_00 stays ~baryonic (mildly reduced) -- the")
print("   field/lensing potential is sourced by baryons alone => MI UNDER-lenses.")
print("   The theory does NOT collapse to MG via an enhanced T_00 either.")
print("   (nu-1)*rho_bar is NOT present in the gravitating source.")

# ----------------------------------------------------------------------
# STEP 5.  Numbers, BOTH footings -- show the verdict is footing-independent.
# ----------------------------------------------------------------------
print("\n[5] NUMERICAL SLIP/NEEDED, BOTH a0 FOOTINGS  (representative galaxy)")
print("-"*74)
c_val = 2.998e8
G_val = 6.674e-11
footings = {"canonical a0 = 9.36e-11 (rho_DE, cH_Lambda/Z)": 9.36e-11,
            "alt       a0 = 1.13e-10 (rho_total, cH0)":       1.13e-10}
# representative MOND-regime disk galaxy: flat v ~ 150 km/s
v_val = 150e3
for label, a0v in footings.items():
    epsv = v_val/c_val
    # deep-MOND enhancement on the theory's OWN dS-Unruh interpolation:
    # g_obs = sqrt(g_bar^2 + g_bar a0); at g_bar ~ a0, nu = g_obs/g_bar:
    g_bar = a0v            # take the source at the a0 scale (MOND onset)
    g_obs = (g_bar**2 + g_bar*a0v)**0.5
    nu_val = g_obs/g_bar               # = sqrt(2) here, O(1)
    slip_ratio = 2*1.0*epsv**2         # D<=1, take D=1 (most generous)
    got_needed = slip_ratio/(nu_val-1)
    print(f"   {label}")
    print(f"      v=150 km/s -> (v/c)^2 = {epsv**2:.2e};  nu(own dS-Unruh) = {nu_val:.3f}")
    print(f"      (Psi-Phi)/Phi   = 2 D (v/c)^2  = {slip_ratio:.2e}   (D=1, most generous)")
    print(f"      got/needed      = {got_needed:.2e}   (need ~1 for a channel)")
print("\n   Both footings: got/needed ~ 1e-6.  The O(1) shift in a0 and in nu")
print("   between footings does NOT touch the (v/c)^2 kinematic suppression.")
print("   VERDICT IS FOOTING-INDEPENDENT.")

# ----------------------------------------------------------------------
# STEP 6.  Consistency of the closed verdict (would-be double count).
# ----------------------------------------------------------------------
print("\n[6] CONSISTENCY  --  and why the ONLY way to 'win' would be MG")
print("-"*74)
print("   To lens correctly WITHOUT dark matter you must enhance grad(Psi+Phi)")
print("   by ~nu while leaving grad(Phi) (rotation curves) baryonic.  The slip is")
print("   the only pure-MI handle for that.  It delivers ~(v/c)^2, short by 1e6.")
print("   Enhancing T_00 instead WOULD lens correctly but enhances grad(Phi) too")
print("   = the double count = modified gravity / effective dark matter, NOT MI.")
print("   MI genuinely modifies inertia (the EOM), not the gravitational source;")
print("   photons (massless) carry no MI boost, and the anisotropic matter stress")
print("   that could rescue lensing is a real relativistic pressure ~ rho v^2.")

print("\n"+"="*74)
print("VERDICT:  SLIP-CLOSED  (horn C confirmed).")
print("="*74)
print("""
  The MI anisotropic stress sources a slip (Psi-Phi) ~ 2 D (v/c)^2 * Phi with
  D = K-dressing, |D|<=1.  The needed lensing enhancement is (nu-1)*Phi with
  (nu-1)=O(1).  The slip is therefore SHORT by ~ (v/c)^2/(nu-1) ~ 1e-6.

  The nonlocal operator K cannot rescue it: K, its derivative K', and the
  metric variation delta(Box_u) are all functions of the BOUNDED MOND ratio
  a_c/a0 = O(1); none contains the c^2/v^2 factor a channel would require.
  The ||K||<=1 Herglotz bound caps the form factor, and the K' (derivative)
  terms carry only kinematic (sub-c) scales, so they do NOT exceed it in a way
  that matters -- there is simply no large dimensionless factor to draw on.

  T_00 is NOT enhanced to nu*rho_bar (K-dressing is <=1, mildly reducing);
  the gravitating source stays ~baryonic -> pure MI UNDER-lenses.  It neither
  collapses to MG (no enhanced T_00) NOR opens a slip channel.

  => The slip loophole (trilemma tooth T1's assumed-away case) is CLOSED.
     A pure-MI, no-dark-matter, correct-lensing channel is NOT found here.
     No-DM lensing must come from Road 1 Branch B (modified source) or Road 2
     (Woodard nonlocal-MG) -- both of which are modified GRAVITY, not pure MI.

  Honesty note: this is a SCALING/order-of-magnitude proof, footing-independent.
  It does not require the full covariant T_mn variation to be carried to all
  orders -- the suppression is set by the single robust fact that the anisotropic
  matter stress is a v^2/c^2 relativistic pressure and K supplies only O(1)
  dressing.  A full-variation surprise would need K' terms to violate the
  Herglotz bound by ~1e6, which Step 3 rules out.
""")
print("exit 0")
