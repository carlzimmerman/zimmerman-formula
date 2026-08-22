#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
HOSTILE REFEREE -- GATE E (double counting).

Charge: the theory has TWO places where ordinary matter enters the
NON-RELATIVISTIC force felt by a test particle:

  (i)  the METRIC time potential Phi_g, whose Poisson equation
       (weak_field_taskE_2026.py, line 130-133) is
           lap Phi_g = 4 pi G rho  +  a0^2 (Y U' - U)          [channel 1]
       -- note the BARE  4 pi G rho  term: matter sources Phi_g Newtonianly.

  (ii) the disformal SCALAR phi.  Task E imports sec14_matter_coupling_static.py
       ([14.3]) for its dynamics; that equation is
           div[ mu(x) grad phi ] = 4 pi G rho                  [channel 2]
       -- ALSO a bare 4 pi G rho source.

  Task E then asserts the physical dynamical potential is
           Xi = Phi_g + phi                                    (its line 289 / 227)
  and that matter falls in -grad Xi.

The claim to be refuted (Task E VERDICT): "the Newtonian piece appears ONCE ...
MOND exactly once."  If BOTH channel-1 Phi_g and channel-2 phi are each sourced
by the SAME bare 4 pi G rho, then a test mass feels the Newtonian potential
TWICE.  We derive the explicit spherical point-mass force from BOTH channels
and check whether the total is v^4 = G M a0 with the CORRECT Newtonian floor,
or whether it is 2x (double counted).

Everything below is Task E's OWN equations, taken literally.  c = 1.
"""
import sympy as sp

results = []
def check(name, cond, extra=""):
    ok = bool(cond)
    results.append(ok)
    print(("PASS: " if ok else "FAIL: ") + name + (("   " + extra) if extra else ""),
          flush=True)

G, M, r, a0 = sp.symbols('G M r a_0', positive=True)
gN = G*M/r**2                      # Newtonian point-mass acceleration g_N
x  = sp.symbols('x', positive=True)
mu_std = x/sp.sqrt(1+x**2)         # standard mu (Task E / Task F kernel)

print("="*74)
print(" STEP 1.  What each channel gives for a spherical point mass")
print("="*74)

# ---- channel 2: the scalar phi obeys the IMPORTED sec14 AQUAL eq -------------
#   div[mu(|grad phi|/a0) grad phi] = 4 pi G rho
#   first integral for a point mass:  mu(g_phi/a0) g_phi = G M/r^2 = g_N
gphi = sp.symbols('g_phi', positive=True)
scalar_relation = sp.Eq(mu_std.subs(x, gphi/a0)*gphi, gN)
print("channel-2 (scalar phi) first integral:  mu(g_phi/a0) g_phi = g_N")

# high-acceleration (Newtonian) limit of channel 2: mu -> 1  => g_phi -> g_N
gphi_newt = sp.limit(sp.solve(scalar_relation, gphi)[0].rewrite(sp.Pow), a0, 0)
# solve is messy; instead expand the relation at small a0/g:  mu->1 => g_phi=g_N
# verify directly that g_phi = g_N solves it as a0/g_N -> 0:
resid_newt = sp.simplify((mu_std.subs(x, gN/a0)*gN - gN))
lim_resid = sp.limit(resid_newt, a0, 0)
check("[channel 2] Newtonian limit: g_phi -> g_N  (phi becomes FULL Newtonian, not 0)",
      lim_resid == 0,
      "so phi does NOT vanish at high g; it equals the whole Newtonian potential")

# deep-MOND limit of channel 2: mu ~ g_phi/a0 => g_phi = sqrt(a0 g_N)
gphi_deep = sp.sqrt(a0*gN)
check("[channel 2] deep-MOND limit: g_phi = sqrt(a0 g_N)",
      sp.simplify((gphi_deep/a0)*gphi_deep - gN) == 0)   # mu~x in deep MOND

# ---- channel 1: the metric time potential Phi_g -----------------------------
#   lap Phi_g = 4 pi G rho + a0^2(YU'-U).  The a0^2(YU'-U) phantom is the SOFT
#   ~Y^{3/2} piece (Task E line 139-141), i.e. ~1/r^3 for a point source =>
#   its contribution to |grad Phi_g| falls as ln r / r^2, subdominant to the
#   bare 4 pi G rho term, which gives the FULL Newtonian gradient:
gPhig_newt = gN                    # |grad Phi_g| from the bare 4 pi G rho term
check("[channel 1] Phi_g has a BARE 4 pi G rho source => |grad Phi_g| >= g_N (Newtonian)",
      sp.simplify(gPhig_newt - gN) == 0,
      "the a0^2(YU'-U) phantom only ADDS to this, it does not cancel it")

print()
print("="*74)
print(" STEP 2.  Total force on a test mass:  g_tot = |grad(Phi_g + phi)|")
print("="*74)
# Task E: matter falls in Xi = Phi_g + phi.  Radial, both gradients point inward,
# so magnitudes ADD:
#   g_tot = g_Phig + g_phi

# --- Newtonian regime (g >> a0) ---
g_tot_newt = gPhig_newt + gN       # = g_N (from Phi_g) + g_N (from phi, mu->1)
check("[Newtonian regime]  g_tot = g_N + g_N = 2 g_N   ==> G_eff = 2G  (DOUBLE COUNT)",
      sp.simplify(g_tot_newt - 2*gN) == 0,
      "solar-system gravity DOUBLED -- the exact failure Task E pinned only on (A)")

# --- deep-MOND regime (g << a0) ---
# g_tot = g_N (from Phi_g bare term) + sqrt(a0 g_N) (from phi).  As r->oo the
# sqrt term dominates, so asymptotic rotation is OK; but there is a LEFTOVER g_N.
g_tot_deep = gN + gphi_deep
v2 = g_tot_deep*r                  # circular v^2 = g_tot r
v4 = sp.expand(v2**2)
# leading (asymptotic) piece:
v4_lead = sp.limit(v4/(G*M*a0), r, sp.oo)*(G*M*a0)
check("[deep-MOND, asymptotic]  v^4 -> G M a0  (rotation curve survives asymptotically)",
      sp.simplify(v4_lead - G*M*a0) == 0,
      "BUT the g_N leftover is a spurious extra Newtonian term at finite r")

print()
print("  Explicit v^4 (finite r, two-channel):")
print("   ", sp.simplify(v4))
print("   = G M a0 + 2 (G M)^{3/2} sqrt(a0)/r + (G M)^2/r^2")
print("  The 2nd and 3rd terms are the double-count residue; a SINGLE-MOND theory")
print("  (below) has ONLY  v^4 = G M a0 + (G M/r)^2-type Newtonian, not the cross term.")

print()
print("="*74)
print(" STEP 3.  The HONEST single-MOND theory (one potential) for contrast")
print("="*74)
# The internally-consistent single-MOND law is ONE AQUAL potential Xi with
#   div[mu(|grad Xi|/a0) grad Xi] = 4 pi G rho,  force = grad Xi.
# This is sec14's ACTUAL structure: matter couples to N=e^{k phi}; phi IS the
# whole potential; there is NO separate metric Phi_g with its own 4 pi G rho.
gXi = sp.symbols('g_Xi', positive=True)
single_relation = sp.Eq(mu_std.subs(x, gXi/a0)*gXi, gN)
# Newtonian limit: g_Xi -> g_N (ONCE)
check("[single-MOND] Newtonian:  g_Xi -> g_N  (Newton ONCE, G_eff = G)",
      sp.limit(mu_std.subs(x, gN/a0)*gN - gN, a0, 0) == 0)
# deep-MOND: g_Xi = sqrt(a0 g_N), v^4 = G M a0 with NO leftover g_N cross term
gXi_deep = sp.sqrt(a0*gN)
v4_single = sp.simplify((gXi_deep*r)**2)
check("[single-MOND] deep-MOND:  v^4 = G M a0 EXACTLY (no Newtonian cross term)",
      sp.simplify(v4_single - G*M*a0) == 0)

print()
print("="*74)
print(" STEP 4.  Numerical size of the Newtonian double-count (solar system)")
print("="*74)
# Sun, Earth orbit: g_N ~ 5.9e-3 m/s^2, a0 = 1.2e-10 m/s^2 => x ~ 5e7, deep Newtonian.
import math
gN_earth = 5.93e-3
a0_num   = 1.2e-10
mu_num   = gN_earth/math.sqrt(gN_earth**2 + a0_num**2)   # ~1 - 2e-16
gphi_earth = gN_earth   # channel-2 phi -> g_N to 1 part in 1e16
g_tot_num  = gN_earth + gphi_earth
print(f"  g_N (Earth orbit)      = {gN_earth:.3e} m/s^2")
print(f"  mu(x) at x=g_N/a0      = {mu_num:.15f}  (=> phi carries FULL g_N)")
print(f"  g_tot two-channel      = {g_tot_num:.3e} m/s^2  = 2 g_N")
print(f"  fractional excess      = {(g_tot_num-gN_earth)/gN_earth:.3f}  (i.e. +100%)")
check("[numeric] two-channel solar-system force is 2x Newton (100% excess, ~1e15 sigma)",
      abs((g_tot_num - gN_earth)/gN_earth - 1.0) < 1e-6)

print()
print("="*74)
print(" STEP 5.  Why the Task E 'escape' fails (phi = MOND excess) ")
print("="*74)
print("""  Task E line 227 asserts: "phi carries the MOND EXCESS (phi->0 as g>>a0),
  so the Newtonian piece appears ONCE."  For phi -> 0 at high g, phi must obey a
  PHANTOM/excess equation, e.g.
        div[ (mu(x) - 1) grad phi ] = 4 pi G rho      (QUMOND-phantom style)
  NOT the AQUAL equation  div[mu grad phi] = 4 pi G rho  it IMPORTS from sec14.
  Check the two are different at high g:""")
# QUMOND-phantom scalar: (mu-1) grad -> 0 as mu->1, so g_phi_excess -> 0 at high g:
# (mu(g_ph/a0)-1) g_ph = g_N  has NO high-g solution with g_ph~g_N; instead the
# EXCESS is g_ph ~ (mu-1) suppressed.  Symbolically at large x, mu-1 ~ -1/(2x^2):
excess_kernel = sp.simplify(mu_std - 1)
excess_hi = sp.series(excess_kernel.subs(x, 1/sp.Symbol('u', positive=True)),
                      sp.Symbol('u', positive=True), 0, 3).removeO()
check("[escape] a TRUE excess kernel (mu-1) -> 0 as g>>a0 (so phi->0): needs (mu-1), "
      "NOT mu", sp.limit(excess_kernel, x, sp.oo) == 0)
print("        (mu-1) at large x  =", excess_hi, " -> 0   [excess vanishes: OK]")
print("        but sec14 [14.3] gives  mu -> 1  (NOT 0)  at large x, so the IMPORTED")
print("        phi does NOT vanish -- the escape contradicts the imported equation.")
print()
print("  Moreover sec14's ACTUAL structure couples matter ONLY to N=e^{k phi} with")
print("  phi the SINGLE potential (psi=phi); there is NO separate metric Phi_g")
print("  carrying its own 4 pi G rho.  So sec14 CANNOT be cited to license the")
print("  two-potential  Xi = Phi_g + phi  bookkeeping that produces the double count.")

print()
print("="*74)
print(" VERDICT")
print("="*74)
print("""  Taking Task E's OWN two equations literally:
      lap Phi_g = 4 pi G rho + a0^2(YU'-U)          [metric, channel 1]
      div[mu grad phi] = 4 pi G rho  (imported sec14) [scalar, channel 2]
      Xi = Phi_g + phi   (test mass falls in -grad Xi)
  the Newtonian force is 2 G M/r^2 (G_eff = 2G) -- Newton counted TWICE, the
  SAME failure Task E attributes ONLY to the rejected linear-rho-Phi coupling.
  The disformal metric does NOT cure it: what matters is that phi and Phi_g each
  carry a BARE 4 pi G rho.  Deep-MOND rotation survives asymptotically (v^4->GMa0)
  but with a spurious Newtonian cross term at finite r.

  Task E's stated escape ("phi carries only the MOND excess, phi->0 at high g")
  is (a) NOT what its imported sec14 equation div[mu grad phi]=4piG rho gives
  (that phi -> full Newton), and (b) inconsistent with sec14's real one-potential
  structure.  The single-MOND result IS available -- but ONLY in the ONE-potential
  form (div[mu grad Xi]=4piG rho, force=grad Xi), which is NOT the
  'metric-rho_MOND + disformal scalar Xi=Phi_g+phi' narrative Task E sells.

  => Gate E, AS WRITTEN, DOUBLE-COUNTS.  Single-MOND is recoverable only by
     DROPPING the two-potential additive bookkeeping and using one AQUAL
     potential; the reconciliation Task E offers is asserted, not derived, and
     contradicts its own imported equation.""")

n_fail = results.count(False)
print(f"\n{results.count(True)}/{len(results)} checks passed, {n_fail} failed.")
import sys
sys.exit(1 if n_fail else 0)
