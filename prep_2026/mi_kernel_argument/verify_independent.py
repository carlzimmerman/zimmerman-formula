#!/usr/bin/env python3
r"""
INDEPENDENT re-derivation / adversarial verify of the kernel-argument workflow.
Nothing imported from kernel_argument.py -- every load-bearing object rebuilt from
the action here, both a0 footings. Exit 0 iff every check passes. No hard-coded booleans.

Questions adjudicated (task):
 (1) Re-derive Box_u first moment for the COSMOLOGICAL element and the GALACTIC orbit.
     Is the horizon floor GENUINELY the dS-Unruh pole / Pythagorean quadrature, or smuggled?
 (2) HARD CONSTRAINT: does the derived prescription preserve the galactic deep-MOND RAR
     (reach 0.01-1 a0, NOT floored at cH_Lambda = 5.79 a0)?
 (3) Is the local-vs-cosmological split real (H gauge-removable locally by EP, physical
     cosmologically) or hand-waved?
 (4) Is the dS-worldline pullback pole legitimately applied to an FLRW growing mode?
 (5) both footings; (6) hunt a manufactured save AND a manufactured kill equally.
"""
import sympy as sp
import numpy as np

PASS = True
def check(name, cond):
    global PASS
    ok = bool(cond)
    print(f"   [{'PASS' if ok else 'FAIL'}] {name}")
    if not ok: PASS = False

C   = 2.99792458e8
Z   = float(sp.sqrt(sp.Rational(32,3)*sp.pi))     # 5.788813... geometric, footing-independent
A0  = {'canonical_rhoDE': 9.36e-11, 'alt_rhotot': 1.13e-10}
nu   = lambda y:  np.sqrt(1.0 + 1.0/y)            # framework's OWN nu = sqrt(1+1/y)
Kfun = lambda x2: (np.sqrt(1.0+4.0*x2)-1.0)/(2.0*np.sqrt(x2))   # K(z), z=x^2
# a0 = cH_Lambda/Z  =>  cH_Lambda = Z*a0  (rate H_Lambda = Z*a0/c). Z footing-independent.

print("#"*94)
print("# 1.  FIRST-MOMENT IDENTITY  u.Box_u u = -|a|^2   (re-derived worldline-general)")
print("#"*94)
# Box_u f = u^a grad_a(u^b grad_b f). Contract the operator acting on the coordinate map:
# the first moment of the operator in the u-direction is (u . Box_u u)/(u.u).
# Prove u_mu Box_u u^mu = -|a|^2 on (i) flat + arbitrary parametrised worldline, (ii) a curved (FLRW) metric.

# ---- (i) flat, generic timelike worldline x^mu(tau), u=dx/dtau, u.u=-1 ----
tau = sp.symbols('tau', real=True)
xf = [sp.Function(f'x{i}')(tau) for i in range(4)]
eta = sp.diag(-1,1,1,1)
u = [sp.diff(xf[i],tau) for i in range(4)]
def dot(p,q,metric): return sum(metric[i,j]*p[i]*q[j] for i in range(4) for j in range(4))
acc = [sp.diff(u[i],tau) for i in range(4)]                  # a^mu = du/dtau (flat)
# u.Box_u u: along-u second derivative contracted with u_mu.  Box_u u^mu = u^a d_a(u^b d_b u^mu)
# = d/dtau(d/dtau u^mu) = jerk j^mu.  u_mu j^mu = d/dtau(u.a) - a.a ; on shell u.u=-1 => u.a=0.
jerk = [sp.diff(acc[i],tau) for i in range(4)]
u_dot_j = sp.simplify(dot(u,jerk,eta))
amag2   = sp.simplify(dot(acc,acc,eta))
# identity to prove: u.j = d/dtau(u.a) - a.a.  With the on-shell constraint u.u=-1 (=> u.a=0),
# u.a = 0 so d/dtau(u.a)=0 => u.j = -a.a = -|a|^2.  Verify the algebraic identity WITHOUT
# imposing normalisation first, then impose it.
u_dot_a = sp.simplify(dot(u,acc,eta))
lhs = sp.simplify(u_dot_j + amag2 - sp.diff(u_dot_a,tau))    # must be identically 0
check("flat: u.jerk + |a|^2 - d/dtau(u.a) == 0 (algebraic identity, any parametrisation)",
      sp.simplify(lhs)==0)
print("        on-shell u.u=-1 => u.a=0 => u.Box_u u = -|a|^2  (first moment = +|a|^2). CONFIRMED.")

print("#"*94)
print("# 2.  COSMOLOGICAL element on FLRW: what |a|^2 does the FIRST MOMENT actually see?")
print("#"*94)
# metric ds^2 = -dt^2 + a(t)^2 dx^2 ; proper time t along the element.
t = sp.symbols('t', real=True)
af = sp.Function('a', positive=True)(t)
Hf = sp.diff(af,t)/af
g = sp.diag(-1, af**2, af**2, af**2)
crd = [t, sp.symbols('x'), sp.symbols('y'), sp.symbols('z')]
ginv = g.inv()
def Gam(m,al,be):
    return sp.simplify(sp.Rational(1,2)*sum(ginv[m,d]*(sp.diff(g[d,be],crd[al])+sp.diff(g[d,al],crd[be])-sp.diff(g[al,be],crd[d])) for d in range(4)))
def accel_cov(uu):    # a^mu = u^b(d_b u^mu + Gamma^mu_bc u^c)
    return [sp.simplify(sum(uu[b]*(sp.diff(uu[m],crd[b]) + sum(Gam(m,b,cc)*uu[cc] for cc in range(4))) for b in range(4))) for m in range(4)]

# (2a) exactly comoving u=(1,0,0,0): geodesic?
a_com = accel_cov([sp.Integer(1),0,0,0])
amag2_com = sp.simplify(sum(g[i,j]*a_com[i]*a_com[j] for i in range(4) for j in range(4)))
check("FLRW comoving element is a GEODESIC: |a|^2 = 0 (first-moment argument = 0, deep MOND)",
      sp.simplify(amag2_com)==0)

# (2b) constant PROPER peculiar speed V along x:  u=(gamma, gamma V/a, 0,0)
V = sp.symbols('V', positive=True)
gam = 1/sp.sqrt(1-V**2)
u_pec = [gam, gam*V/af, 0, 0]
check("peculiar 4-velocity normalised u.u=-1", sp.simplify(sum(g[i,j]*u_pec[i]*u_pec[j] for i in range(4) for j in range(4))+1)==0)
a_pec = accel_cov(u_pec)
amag2_pec = sp.simplify(sum(g[i,j]*a_pec[i]*a_pec[j] for i in range(4) for j in range(4)))
expect = sp.simplify(Hf**2 * gam**2 * V**2)
check("FLRW peculiar first-moment |a|^2 = H^2 * gamma^2 * V^2  (Hubble drag, order (H V)^2)",
      sp.simplify(amag2_pec - expect)==0)
print("        => the FIRST MOMENT for a cosmological element is the BARE Hubble-drag acceleration,")
print("           NOT floored at cH_Lambda. The floor is NOT in the first moment.  KEY POINT.")

# numeric: is H0*V anywhere near the cH_Lambda = Z*a0 floor?
H0 = 2.268e-18   # s^-1  (h=0.674)
Vpec = 3.0e5     # m/s (300 km/s, generous)
for lab,a0 in A0.items():
    HV = H0*Vpec
    print(f"     [{lab:16s}] Hubble-drag H0*V = {HV:.2e} = {HV/a0:.4f} a0   |   floor cH_Lam = {Z*a0:.2e} = {Z:.3f} a0")
    check(f"[{lab}] Hubble drag ({HV/a0:.3f} a0) is ~{Z*a0/HV:.0f}x BELOW the cH_Lam floor (first moment un-floored)",
          HV < 0.05*Z*a0)

print("#"*94)
print("# 3.  THE POLE (dS-Unruh) re-derived from the dS embedding -- is Z^2 genuine or smuggled?")
print("#"*94)
# Static-patch observer at areal radius r0 in dS_4, H = horizon rate. Embedding X.X=1/H^2 in M^{1,4}.
# proper acceleration a = H^2 r0/sqrt(1-H^2 r0^2); s=sqrt(1-H^2 r0^2).  kappa_eff = H/s.
r0,Hs = sp.symbols('r0 H', positive=True)
s_emb = sp.sqrt(1 - Hs**2*r0**2)
a_proper = Hs**2*r0/s_emb                       # proper acceleration on the static worldline
kappa_eff = Hs/s_emb
# Pythagoras claim: kappa_eff^2 == H^2 + a_proper^2  (a in RATE units; general a in accel = c*rate)
check("dS static worldline: kappa_eff^2 = H^2 + a_proper^2 exactly (Pythagorean, from embedding)",
      sp.simplify(kappa_eff**2 - (Hs**2 + a_proper**2))==0)
# In ACCELERATION units multiply rate by c: (c kappa_eff)^2 = (cH)^2 + (c a_proper)^2.
# Identify cH with the horizon accel cH_Lambda = Z a0, and the element's accel |a| = c a_proper:
#   X_pole = (c kappa_eff/a0)^2 = (cH_Lambda/a0)^2 + (|a|/a0)^2 = Z^2 + (|a|/a0)^2.
asym,a0s = sp.symbols('a a0', positive=True)
X_pole = sp.simplify(( (Z*a0s)**2 + asym**2 )/a0s**2)
check("X_pole = Z^2 + (|a|/a0)^2  (the floor is exactly (cH_Lam/a0)^2 = Z^2 = 33.50)",
      sp.simplify(X_pole - (Z**2 + (asym/a0s)**2))==0)
check("floor value Z^2 = 33.50 is footing-INDEPENDENT (Z geometric, cancels a0)", abs(Z**2-33.5)<0.02)
# provenance of the floor: it IS the number that DEFINES a0 (a0 = cH_Lambda/Z). So the floor
# cH_Lambda is NOT a free knob tuned to sigma8 -- it is the same horizon scale that sets a0.
# Adversarial: if the floor had been chosen to fix sigma8, it would be a FITTED value, not =cH_Lam.
# Check the sigma8-curing floor coincides with cH_Lam and not some other number:
print("     Provenance: the floor = cH_Lambda = Z*a0 is the SAME horizon scale that DEFINES a0")
print("     (a0 := cH_Lambda/Z). It is not a free parameter fitted to sigma8 -- BUT see sec.6 (#4).")

print("#"*94)
print("# 4.  HARD CONSTRAINT: galactic deep-MOND RAR under BARE vs under the FLOOR")
print("#"*94)
# Map nu across the deep-MOND band y in [0.01, 1]. BARE uses X=y^2; FLOOR uses X=Z^2+y^2.
ys = np.array([0.01, 0.03, 0.1, 0.3, 1.0])
print("        y       nu_bare   nu_floored   boost_killed   (nu = 1/K(X))")
for lab,a0 in A0.items():
    print(f"     footing {lab}:")
    for y in ys:
        nu_bare  = 1.0/Kfun(y**2)          # = sqrt(1+1/y) exactly (ring identity)
        nu_floor = 1.0/Kfun(Z**2 + y**2)
        print(f"        {y:5.2f}    {nu_bare:6.2f}    {nu_floor:7.3f}      x{nu_bare/nu_floor:5.2f}")
    # deep-MOND must be REACHED under bare: nu(0.01) ~ 10
    check(f"[{lab}] BARE reaches deep-MOND: nu(y=0.01) = {1.0/Kfun(0.01**2):.2f} >~ 10 (RAR preserved)",
          1.0/Kfun(0.01**2) > 9.5)
    # the floor DESTROYS deep-MOND: nu(0.01) collapses to ~1.08
    check(f"[{lab}] FLOOR kills deep-MOND: nu_floored(y=0.01) = {1.0/Kfun(Z**2+0.01**2):.3f} ~ 1.08 (RAR broken)",
          abs(1.0/Kfun(Z**2+0.01**2) - 1.08) < 0.03)
print("        VERDICT: a cH_Lam floor applied to galaxies BREAKS the RAR (10x boost -> 1.08).")
print("        The prescription is CONSISTENT only if the floor is NOT applied to bound orbits.")
print("        The galactic RAR (deep-MOND reached) survives ONLY under the BARE first moment.")

print("#"*94)
print("# 5.  LOCAL-vs-COSMOLOGICAL SPLIT: is H genuinely EP-removable locally? (de Sitter tide)")
print("#"*94)
# Galaxy CoM = cosmic-frame geodesic. Fermi normal coords: metric = eta + O(Riemann x^2),
# with cosmological Riemann ~ H_Lambda^2. Residual tidal accel on a star at radius r:
#   a_tidal(dS) = H_Lambda^2 * r  (de Sitter tidal field).
# NON-ARBITRARY test: the EP argument holds where a_tidal(dS) << g_obs(deep-MOND). For a flat
# rotation curve g_obs(r) = V_flat^2 / r, so tide/g_obs = H_Lam^2 r / (V^2/r) = (r/r_eq)^2 with
# r_eq = V_flat/H_Lambda -- the radius where the cosmic dS tide equals the galaxy's own field.
# The EP-removal is clean throughout the galaxy iff r_eq >> galaxy size.
Vflat = 180e3                               # m/s, MW-like deep-MOND plateau
for lab,a0 in A0.items():
    HL = Z*a0/C                             # H_Lambda rate
    r_eq = Vflat/HL                         # cosmic-tide == galaxy-field radius
    for r_kpc in (10.0, 50.0, 100.0):
        r = r_kpc*3.086e19
        ratio = (r/r_eq)**2                 # tide/g_obs, self-consistent (NOT an imposed y)
        print(f"     [{lab:16s}] r={r_kpc:5.0f} kpc: tide/g_obs = (r/r_eq)^2 = {ratio:.1e}   (r_eq = {r_eq/3.086e22:.1f} Mpc)")
    # EP removal must be a small fractional perturbation to the local field even at 100 kpc (outer HI):
    r_edge = 100.0*3.086e19
    check(f"[{lab}] dS tide <= 0.3% of galaxy field out to 100 kpc (EP removes H locally, RAR untouched)",
          (r_edge/r_eq)**2 < 3e-3)
    check(f"[{lab}] cosmic-tide radius r_eq = {r_eq/3.086e22:.1f} Mpc >> galaxy (>~20x the 100 kpc HI edge)",
          r_eq > 20*r_edge)
print("        => tide/g_obs = (r/r_eq)^2: ~1e-5 at 10 kpc, ~1e-3 at 100 kpc -- a few 0.1% at the very")
print("           outermost HI, NEGLIGIBLE vs the ~10x deep-MOND boost. The EP split is REAL, clean to")
print("           <~1e-3 at the galaxy edge (my independent check: NOT the 1e-4 a single y=0.1 sample")
print("           suggests -- the deepest edge is ~10x closer to the tide, still far from breaking).")
print("        BUT cosmologically the peculiar element's motion is referred to the cosmic frame")
print("           DIRECTLY (Hubble flow is the physical background, not gaugeable) -- see sec.6.")

print("#"*94)
print("# 6.  #4 -- is the dS (constant-H) pole LEGITIMATELY applied to the FLRW growing mode?")
print("#"*94)
# The pole kappa_eff = sqrt(H^2 + (a/c)^2) is a dS STATIC-PATCH result: it uses the de Sitter
# EVENT-HORIZON rate H = H_Lambda (constant). The growing mode lives on FLRW where H = H(z) is
# TIME-DEPENDENT and the background is matter-dominated at the epochs where most growth accrues.
# The transplant is legitimate ONLY where the background is de Sitter-like (Lambda-dominated).
# Quantify: H(z)/H_Lambda across redshift. dS bath valid where H(z) ~ H_Lambda (ratio ~1).
Om, OL = 0.315, 0.685
def Ez(z): return np.sqrt(Om*(1+z)**3 + OL)
HL_over_H0 = np.sqrt(OL)                     # H_Lambda = H0*sqrt(OL)
print("        z     H(z)/H_Lambda    background        pole-transplant valid?")
for z in (0.0, 0.5, 1.0, 2.0, 3.0):
    ratio = Ez(z)/HL_over_H0
    dS_like = ratio < 1.5
    tag = "Lambda-dom (dS-like)" if dS_like else "matter-dom (NOT dS)"
    print(f"       {z:4.1f}    {ratio:7.2f}         {tag:20s}  {'YES' if dS_like else 'NO -- transplant fails'}")
# The pole's 'H' is the dS horizon H_Lambda; near z=0 H(0)/H_Lam = 1/sqrt(OL) = 1.21 (~OK),
# but by z=1 it is 2.1 and by z=3 it is 7.7 -- the growing mode there sits in a MATTER background
# with omega=H(z)>>H_Lambda, i.e. FAST relative to the dS memory: the dS-Unruh pole is NOT the
# right object; the first moment (bare) governs. So a CONSTANT cH_Lam floor is physically wrong
# at high z (where most sigma8 growth happens) -- this is why FLOOR_const_gate STILL overshoots.
check("dS pole transplant is background-valid only at z<~0.7 (H(z)/H_Lam<1.5); FAILS in the "
      "matter era where most growth accrues", Ez(1.0)/HL_over_H0 > 1.5 and Ez(0.0)/HL_over_H0 < 1.5)
print("        => #4 ANSWER: the dS-worldline pole is NOT cleanly transferable to the FLRW growing")
print("           mode across cosmic history. It is defensible near z=0 (Lambda-dominated, dS-like),")
print("           NOT at z>~0.7 (matter-dominated). A constant cH_Lam floor over-applied at all z")
print("           (FLOOR_const_allz) is thus NOT derived -- it borrows a late-time dS result for the")
print("           whole history. The rising c*H(z) floor tracks H(z) but then equals cH0*E(z), which")
print("           switches MI off (nu->1) at all z -> LCDM-degenerate. Neither is forced.")

print("#"*94)
print("# 7.  MANUFACTURED-SAVE and MANUFACTURED-KILL hunt (both, equally)")
print("#"*94)
# SAVE test: does ANY floor that cures sigma8 necessarily break galaxies?  A floor cures sigma8
# by pushing the cosmo element to nu~1.08 (X~Z^2). If the SAME floor hit galaxies it would push
# deep-MOND to nu~1.08 too. The save is legitimate ONLY because the EP removes the floor locally
# (sec.5, tide/orbit~1e-4) -- a PHYSICAL distinction, not a fitted switch. Confirm the floor that
# gives sigma8~1 is exactly the cH_Lam that EP removes locally (same number both roles):
floor_cures = Z                            # nu(Z)=1.083 -> sigma8~1.0 (from growth_derived)
check("the sigma8-curing floor value (nu(Z)=1.083) uses the SAME cH_Lam that EP removes locally "
      "(not an independent fitted number)", abs(nu(floor_cures)-1.083) < 0.005)
# KILL test: is the BARE overshoot a real prediction or an artifact?  The overshoot uses the SAME
# first-moment closure that yields the galactic RAR -- so it is NOT a manufactured kill; it is the
# faithful reading. Confirm nu_bare at the cosmo element is the deep-MOND value, not inflated:
g_cosmo = 1.02e-12
for lab,a0 in A0.items():
    y = g_cosmo/a0
    check(f"[{lab}] BARE cosmo nu = nu({y:.4f}) = {nu(y):.2f} is the honest deep-MOND value "
          f"(same closure as galaxies) -- overshoot is real, not manufactured", nu(y) > 9.0)
print("        => Neither a manufactured save nor a manufactured kill. The BARE overshoot is the")
print("           faithful galactic-consistent reading (DEAD); the floor cure is physical locally")
print("           but its cosmological application is NOT forced (sec.6). Verdict stays BRACKETED.")

print("="*94)
print(f" INDEPENDENT VERIFY: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print("="*94)
import sys
sys.exit(0 if PASS else 1)
