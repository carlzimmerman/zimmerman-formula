#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
c1_frame_curvature.py -- LANE C1: NONMINIMAL FRAME-CURVATURE completion candidate
=================================================================================
CANDIDATE (the lane spec):
  Delta-S = (c^4/16piG) INT sqrt(-g) F( K(Box_u/a0^2) ) * Q,   Q in { R , u^mu u^nu R_munu }
  i.e. the frame's OWN kernel K modulates the gravitational coupling, in the hope that the
  vacuum-derived a0 (entering only via X = |a|^2/a0^2 inside K) SOURCES the phantom mass
  M_phantom = (nu-1) M_bar so that single-metric lensing closes: g_lens = nu g_bar (F_lens -> 1),
  with the deep-MOND slope g_lens ~ sqrt(a0 g_bar).

We test this on ITS OWN terms (modified-INERTIA, a0 = cH_Lambda/Z, framework nu = sqrt(1+1/y)).
BOTH footings: a0 = 9.36e-11 (canonical rho_DE/cH_Lambda) and 1.13e-10 (alt rho_tot/cH0).

The five completion checks are SCORED at the end:
  (1) LENSING   -> does the metric variation add (nu-1) rho u u with the sqrt(a0 g_bar) slope?
  (2) c_gamma=c_GW (single metric, no disformal photon; watch the uuR_munu variant for c_T shift)
  (3) GHOST-FREE (Ostrogradsky from K(Box_u) INSIDE a curvature coupling?)
  (4) CASSINI   -> Delta-S -> 0 at a>>a0 (nu->1), verify at y~1e6
  (5) COSMOLOGY -> phantom stays small where the growing mode sees the horizon-floored argument
CRUCIAL: is a0 STILL cH_Lambda/Z (derived), or does F re-introduce a free scale / free function?

HONEST RAILS: no manufactured save, no manufactured kill.  Every load-bearing number is printed
by a machine check below; exit 0 iff all checks pass (a check FAILS loudly if the claim is false).

Credits: nonlocal-MG phantom-source mechanism -- Deffayet-Woodard 2011 (1106.4984);
AeST -- Skordis-Zlosnik 2021; MOND / QUMOND phantom mass -- Milgrom.
"""
import sympy as sp
import numpy as np
import sys, random

PASS = 0; FAIL = 0
def check(name, ok, tag=""):
    global PASS, FAIL
    print(("  [PASS] " if ok else "  [FAIL] ") + name + tag)
    if ok: PASS += 1
    else: FAIL += 1

def eq0(expr):
    e = sp.simplify(expr)
    if e == 0: return True, " (symbolic)"
    free = sorted(e.free_symbols, key=lambda s: s.name)
    import mpmath
    for _ in range(30):
        subs = {s: mpmath.mpf(random.uniform(0.05, 4.0)) for s in free}
        v = sp.lambdify(free, e, 'mpmath')(*[subs[s] for s in free])
        if abs(v) > 1e-10: return False, ""
    return True, " (numeric, 30 random pts < 1e-10)"

# ---------------------------------------------------------------------------
print("="*92)
print("SEC 1 -- the kernel on the RAR shell: what F is a free function OF")
print("="*92)
z, y = sp.symbols('z y', positive=True)
K  = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
nu = sp.sqrt(1 + 1/y)
z_on = y**2 + y
rad  = sp.sqrt(4*y**2+4*y+1)
K_on = sp.simplify(K.subs(z, z_on).subs(rad, 2*y+1))
ok, tg = eq0(K_on - 1/nu)
check("on-shell (|a|=g_obs=nu g_bar): K = 1/nu(y)  -> F(K) is a free function of 1/nu, i.e. of y", ok, tg)
check("deep-MOND K -> sqrt(z) = |a|/a0 (so K=1/nu ~ sqrt(y) as y->0)",
      sp.limit(K/sp.sqrt(z), z, 0, '+') == 1)
check("Newtonian K -> 1 as z->oo (=> F(K) -> F(1) const at a>>a0; needed for Cassini)",
      sp.limit(K, z, sp.oo) == 1)
print("  => the candidate's ONLY new freedom is the SHAPE of the function F. a0 enters just via X.")
print("     No new DIMENSIONFUL coupling is written (prefactor is c^4/16piG, same as EH).")

# ---------------------------------------------------------------------------
print("\n"+"="*92)
print("SEC 2 -- metric variation of the nonminimal term -> the extra gravitating source")
print("="*92)
print("  Standard scalar-tensor identity for  INT sqrt(-g) (1+F) R  (F = F(K), scalar):")
print("     (1+F) G_munu + (g_munu Box - grad_mu grad_nu) F  =  8piG/c^4 T_munu .")
print("  The NEW source (relative to GR), moved to the RHS, is  -(g_munu Box - grad grad) F(K).")
print("  Verify its weak-field, static 00-projection is a Laplacian of F (a total divergence):")
r = sp.symbols('r', positive=True)
Phi = sp.Function('Phi')(r); Psi = sp.Function('Psi')(r); Fs = sp.Function('Fcal')(r)
# spherical Laplacian of a scalar
def lap(f): return sp.diff(f, r, 2) + (2/r)*sp.diff(f, r)
# The 00 field eq to linear order: G_00 = 2 lap(Psi); extra term -(g00 Box - d0d0)F = +lap(F) (static).
# So  2 lap(Psi) = 8piG/c^4 (rho c^2) + lap(F)   ->  effective phantom density rho_ph:
#     rho_ph c^2 = (c^4/8piG) lap(F).  Verify the enclosed phantom mass is a pure surface flux:
M_ph_integrand = lap(Fs)*4*sp.pi*r**2                    # 4pi r^2 * lap(F)
M_ph = sp.integrate(sp.diff(4*sp.pi*r**2*sp.diff(Fs, r), r), (r, r, r))  # placeholder; use FTC below
ok, tg = eq0( M_ph_integrand - sp.diff(4*sp.pi*r**2*sp.diff(Fs, r), r) )
check("GAUSS: 4pi r^2 lap(F) = d/dr[4pi r^2 F'(r)]  => M_phantom(r) proportional to r^2 F'(r) (surface flux)",
      ok, tg)
print("  KEY STRUCTURAL FACT: the nonminimal-term phantom is a TOTAL DIVERGENCE (lap of a LOCAL F).")
print("  Enclosed phantom mass  M_ph(r) = (c^2/G) * kappa * r^2 F'(r)   (kappa = O(1) from the variation).")
print("  This is the QUMOND/nonlocal-MG mechanism -- BUT here F is a LOCAL function of |a| (see SEC 3).")

# ---------------------------------------------------------------------------
print("\n"+"="*92)
print("SEC 3 -- THE DECIDER: can a UNIVERSAL local F(K) source (nu-1)M_bar with the right slope?")
print("="*92)
print("  Require, for lensing to close:  M_ph(r) = (nu(y)-1) M_bar(r)  at every r, for EVERY source.")
print("  Test on the cleanest case, a point mass M (M_bar(r)=M): g_bar=GM/r^2, y=GM/(a0 r^2).")
print("  Impose M_ph(r) = (c^2/G) kappa r^2 F'(r) = (nu-1) M, with F = F(y) UNIVERSAL (function of y only).")
# symbolic reduction: r^2 F'(r) = r^2 F'(y) y'(r), y'(r) = -2y/r, r^2 = GM/(a0 y)
G, c, M, a0, kap = sp.symbols('G c M a0 kappa', positive=True)
yv = sp.Symbol('y', positive=True)
Fy = sp.Function('F')(yv)
r_of_y = sp.sqrt(G*M/(a0*yv))
# r^2 F'(r) expressed in y:
rsq_Fprime_r = (G*M/(a0*yv)) * sp.diff(Fy, yv) * (-2*yv/r_of_y)   # = -2 sqrt(GM/a0) sqrt(y) F'(y)
target = -2*sp.sqrt(G*M/a0)*sp.sqrt(yv)*sp.diff(Fy, yv)
ok, tg = eq0(rsq_Fprime_r - target)
check("reduce: r^2 F'(r) = -2 sqrt(GM/a0) sqrt(y) F'(y)  (universal-F ansatz, point mass)", ok, tg)
# solve for the REQUIRED F'(y):
nu_y = sp.sqrt(1+1/yv)
Fprime_required = sp.simplify( (nu_y-1)*M / ( (c**2/G)*kap * (-2*sp.sqrt(G*M/a0)*sp.sqrt(yv)) ) )
Fprime_required = sp.simplify(Fprime_required)
print("  Required  F'(y) =", Fprime_required)
# extract the M and a0 scaling: F'(y) = -(nu-1)/(2 kappa sqrt(y)) * sqrt(G M a0)/c^2
claim = -(nu_y-1)/(2*kap*sp.sqrt(yv)) * sp.sqrt(G*M*a0)/c**2
ok, tg = eq0(Fprime_required - claim)
check("=> Required F'(y) = -(nu-1)/(2 kappa sqrt(y)) * sqrt(G M a0)/c^2   [CARRIES sqrt(M)!]", ok, tg)
# the killer: ratio of required F' at two DIFFERENT masses is sqrt(M2/M1), INDEPENDENT of y
M1, M2 = sp.symbols('M1 M2', positive=True)
ratio = sp.simplify( claim.subs(M, M2)/claim.subs(M, M1) )
ok, tg = eq0(ratio - sp.sqrt(M2/M1))
check("NON-UNIVERSALITY: F'_required(y;M2)/F'_required(y;M1) = sqrt(M2/M1), INDEPENDENT of y", ok, tg)
print("  => NO single universal local F(K) can source (nu-1)M_bar for all masses: the required")
print("     amplitude scales as sqrt(M). A local nonminimal F(K) is BLIND to M (it sees only |a|).")
print("     This is exactly why LOCAL curvature couplings do not give the MOND phantom mass:")
print("     the phantom needs the NONLOCAL inverse-Laplacian (QUMOND Poisson), not a local F(|a|).")

# ---------------------------------------------------------------------------
print("\n"+"="*92)
print("SEC 4 -- QUANTIFY the miss: fix F on a galaxy, apply to a cluster (both footings)")
print("="*92)
def nu_num(yy): return np.sqrt(1.0+1.0/yy)
# If F is FIXED to satisfy the requirement at mass M1, the phantom it PRODUCES at mass M2 is
#   M_ph^produced(y;M2) = (nu-1) sqrt(M1 M2)   (derived analytically; verify vs required (nu-1)M2)
Mgal = 6.0e10*1.989e30    # ~Milky-Way baryonic, kg
Mclu = 1.0e14*1.989e30    # cluster baryonic, kg
for label, a0v in [("canonical a0=9.36e-11", 9.36e-11), ("alt a0=1.13e-10", 1.13e-10)]:
    print(f"  [{label}]")
    for (nm, Msrc, Mfix) in [("cluster w/ F tuned to galaxy", Mclu, Mgal),
                              ("galaxy w/ F tuned to cluster", Mgal, Mclu)]:
        for yy in (0.1, 0.01):
            # produced phantom / required phantom = sqrt(Mfix/Msrc)  (from SEC 3 algebra)
            frac = np.sqrt(Mfix/Msrc)
            # lensing completion metric F_lens = g_lens/(nu g_bar) = [1 + (nu-1)*frac]/nu
            nuw = nu_num(yy)
            Flens = (1.0 + (nuw-1.0)*frac)/nuw
            print(f"    {nm:30s} y={yy:<5} phantom fraction={frac:.3f}  ->  F_lens={Flens:.3f}  (target 1.000)")
# the miss is footing-independent (a0 cancels in the ratio); assert the algebra M_prod=(nu-1)sqrt(M1 M2)
Msym1, Msym2 = sp.symbols('Ma Mb', positive=True)
Fprime_fixed = claim.subs(M, Msym1)                 # F fixed by mass Ma
# produced M_ph at mass Msym2 uses r^2 F'(r) = -2 sqrt(G Msym2/a0) sqrt(y) F'_fixed(y):
Mprod = sp.simplify( (c**2/G)*kap * (-2*sp.sqrt(G*Msym2/a0)*sp.sqrt(yv)*Fprime_fixed) )
ok, tg = eq0( Mprod - (nu_y-1)*sp.sqrt(Msym1*Msym2) )
check("produced phantom with F fixed at Ma, applied to Mb:  M_ph = (nu-1) sqrt(Ma Mb)  != (nu-1)Mb", ok, tg)
print("  => tuned to a 6e10 galaxy, a 1e14 cluster gets ~2.4% of its phantom (F_lens collapses);")
print("     tuned to the cluster, the galaxy is over-lensed ~40x. A universal a0-derived F CANNOT fit both.")

# ---------------------------------------------------------------------------
print("\n"+"="*92)
print("SEC 5 -- GHOST / OSTROGRADSKY: K(Box_u) inside a curvature coupling")
print("="*92)
print("  Under HONEST metric variation, X = |a|^2/a0^2 is METRIC-DEPENDENT: a^mu = u^b grad_b u^mu")
print("  contains the connection Gamma (= d g). Show it explicitly for the static frame u.")
# weak-field static metric diag(-(1+2Phi),1,1,1); static observer u^mu = (1/sqrt(1+2Phi),0,0,0)
# Represent the potential value P=Phi and its gradient dP=Phi' as independent symbols (amplitude eps).
P, dP = sp.symbols('P dP', real=True)
gtt = -(1+2*P)
# Christoffel Gamma^r_tt = -(1/2) g^rr d_r g_tt = -(1/2)(1)(-2 dP) = dP   (g^rr=1)
Gam_r_tt = dP
u_t = 1/sp.sqrt(1+2*P)
# a^r = u^b grad_b u^r = (u^t)^2 Gamma^r_tt   (static u, u^r=0)
a_r = sp.simplify((u_t**2)*Gam_r_tt)                     # = dP/(1+2P)
# leading order in the field amplitude: a^r -> dP = Phi'  (the connection/dg term)
ok = sp.simplify(a_r.subs(P, 0) - dP) == 0 and sp.simplify(a_r - dP).subs(P, 0) == 0
check("static-frame acceleration a^r = dP/(1+2P) -> Phi' = d(g)/dr as P->0: |a|^2=(Phi')^2 depends on d g",
      ok)
print("  Hence F(K(X)) = F( (Phi')^2/a0^2 ) is a function of FIRST derivatives of the metric.")
print("  The metric field equation from delta[ sqrt(-g) F(K(X)) R ]/delta g contains  Box F(K):")
print("    Box F ~ d^2[ F((dg)^2) ] ~ (dg)(d^3 g) + (d^2 g)^2  =>  THIRD derivatives of g in the EOM.")
print("  A 4th-order (in derivatives) metric field equation with NO f(R)-type degeneracy")
print("  (F depends on g through Gamma/|a|, NOT through R) => an OSTROGRADSKY ghost mode.")
# demonstrate the >2-derivative appearance concretely: Box of a function of Phi' has Phi'''
Phi_r = sp.Function('Phi')(r)
Ffun = sp.Function('Fc')
FK = Ffun(sp.diff(Phi_r, r)**2)                          # F(K(X)) ~ F((Phi')^2), X depends on dg
BoxFK = sp.diff(FK, r, 2)                                 # spatial part of Box (static)  -> appears in EOM
has_third = BoxFK.has(sp.diff(Phi_r, r, 3))
check("Box F(K((Phi')^2)) contains Phi''' (third metric derivative) -> higher-order EOM (Ostrogradsky)",
      has_third)
print("  ESCAPE (the only ghost-free reading): FREEZE X -- treat |a| as an external, g-independent")
print("  prescribed profile.  Then F(K(X)) = phi(x) is a PRESCRIBED scalar and phi R is Brans-Dicke")
print("  with an imposed phi.  Ghost-free & single-metric -- but phi is put in BY HAND to solve the")
print("  phantom-Poisson => this IS QUMOND/nonlocal-MG: a FREE function, and (SEC 3) it must carry")
print("  sqrt(M) per object => a0 is NO LONGER the controlling scale of the phantom.  a0 FORFEITED.")

# ---------------------------------------------------------------------------
print("\n"+"="*92)
print("SEC 6 -- Cassini (check 4) and c_gamma (check 2): the parts that DO pass, honestly")
print("="*92)
# Cassini: if F(1)=0 and F'(K) -> 0 fast at a>>a0, the term vanishes. The REQUIRED F' ~ (nu-1)/sqrt(y)
# -> 0 as y->oo (nu-1 ~ 1/(2y)), so F' ~ y^-3/2. Evaluate the phantom fraction at Saturn y~1e6.
ybig = 1.0e6
nu_minus1 = np.sqrt(1+1/ybig) - 1.0
Fprime_scaling = nu_minus1/np.sqrt(ybig)      # ~ y^-3/2
check(f"Cassini: at y~1e6, (nu-1)/sqrt(y) = {Fprime_scaling:.2e} << 1  => phantom self-vanishes (IF F so chosen)",
      Fprime_scaling < 1e-8)
print(f"  nu-1 at y=1e6 = {nu_minus1:.2e} (deep-Newton); the nonminimal term -> 0 at a>>a0. Check 4 OK*.")
print("  (*contingent on choosing F with F(1)=0; not a distinctive win -- any MG interp does this.)")
print("  c_gamma (check 2): the F(K)R (scalar-Ricci) variant is CONFORMAL-type -> tensor modes stay")
print("  luminal (c_T=1), photons on the SAME g => c_gamma=c_GW OK.  BUT the u^mu u^nu R_munu variant")
print("  is an aether-curvature (Einstein-aether-like) coupling that GENERICALLY shifts c_T => GW170817")
print("  RISK for the uuR_munu choice.  So check 2 is variant-dependent: FR safe, uuR risky.")

# ---------------------------------------------------------------------------
print("\n"+"="*92)
print("SEC 7 -- SCORECARD (both footings; the miss is footing-independent -- a0 cancels in SEC 3/4)")
print("="*92)
print("""
  Candidate: Delta-S = (c^4/16piG) INT sqrt(-g) F(K(Box_u/a0^2)) [ R  or  u^mu u^nu R_munu ]

  (1) LENSING      : FAILS as a LOCAL, ghost-free, a0-derived term. The phantom is a total
                     divergence of a LOCAL F(|a|); a universal F cannot source (nu-1)M_bar --
                     the required F carries sqrt(M) (SEC 3), so it fits one object's mass and
                     misses all others (SEC 4). To actually close lensing you must PRESCRIBE
                     phi nonlocally (QUMOND) => next line.
  (2) c_gamma=c_GW : OK for the F(K)R (scalar) variant (c_T=1, single metric); the u u R_munu
                     variant risks c_T != 1 (GW170817) -- aether-curvature coupling.
  (3) GHOST-FREE   : FAILS under honest variation (X = |a|^2 depends on dg via the connection;
                     Box F(K) => 3rd metric derivatives => Ostrogradsky).  Ghost-free ONLY if X
                     is FROZEN (prescribed phi) -- which removes the a0-derivation (next line).
  (4) CASSINI      : OK* (contingent -- F(1)=0, term ~ (nu-1)/sqrt(y) -> 0 at a>>a0). Not distinctive.
  (5) COSMOLOGY    : plausibly OK (phantom small where growing mode sees horizon-floored arg), but
                     CONTINGENT on the free F; not a constraint that bites here.

  CRUCIAL (a0 status): the term writes NO new dimensionful coupling (prefactor c^4/16piG), so a0
  never appears as an explicit new scale -- superficially "a0 kept". BUT to source the phantom, F
  must be (i) a FREE FUNCTION whose shape is not forced by the frame/vacuum, and (ii) per SEC 3 it
  must carry sqrt(M) per object => the phantom's amplitude is set by F, NOT by a0=cH_Lambda/Z.
  The a0-DERIVATION is FORFEITED in substance even though no new constant is written.

  VERDICT: as posed (local, ghost-free, a0-derived) the candidate FAILS-LENSING (SEC 3 non-
  universality + SEC 5 ghost). The ONLY way to make it close lensing is to freeze X and prescribe
  phi nonlocally -- i.e. slide to QUMOND/nonlocal-MG: single-metric & (then) ghost-free, but
  a0 becomes a FREE coupling/function (= modified GRAVITY, not modified inertia).  No combination
  gives {a0-derived + single-metric + ghost-free + MOND-lensing} -- the C1 horn of the trilemma.
""")
print("="*92)
print(f"TOTAL: {PASS} checks passed, {FAIL} failed")
print("="*92)
sys.exit(0 if FAIL == 0 else 1)
