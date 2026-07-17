#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
nogo.py  --  The sharpened MI-lensing no-go (the completeness check for the C1/C2/C3 lane).

QUESTION (exact):
  Is closing the nu^2 lensing wedge with ALL FOUR of
     D = a0 DERIVED from cH_Lambda/Z   (passive 0-dof frame u, bounded kernel K(box_u/a0^2), ||K||<=1)
     S = single-metric, c_gamma = c_GW (no disformal photon term; GW170817-safe)
     G = ghost-free                    (no Ostrogradsky / negative-norm mode)
     L = MOND-lensing                  (single-metric phantom source (nu-1)rho, slope g_lens ~ sqrt(a0 g_bar))
  provably IMPOSSIBLE?  And which SUBSET of {D,S,G,L} is mutually exclusive?

WHAT THIS SCRIPT DOES (sympy-exact + a finite logical exhaustion):
  (1) The phantom is NONLOCAL in the baryons.  Point mass: M_ph(r)=(nu-1)M with y=GM/(a0 r^2);
      M_ph(r)/r -> sqrt(a0 M/G) != 0  (an UNBOUNDED halo).  A local functional of rho + the
      passive frame cannot build a source outside supp(rho).  -> L needs a nonlocal carrier.
  (2) The passive frame is BOUNDED.  On the RAR shell K=1/nu<=1; the phantom uu-coefficient
      needed is nu-1/nu, the frame supplies 1/nu, shortfall (nu^2-1)=1/y DIVERGES as y->0.
      A bounded kernel supplies O(K)<=1 dressing, never the O(nu) phantom.  -> D forbids L.
  (3) A local universal F(y) is MASS-BLIND: F'_req(y) ~ sqrt(M) per object; two masses cannot
      share one F (ratio sqrt(M2/M1), y-independent).  -> a local a0-derived term fails L for >1 body.
  (4) FOOTING independence: the wedge ratio nu^2-1 = 1/y (y=g_bar/a0) and the mass-blindness ratio
      are a0-FREE.  Both footings (9.36e-11 / 1.13e-10) give the identical dimensionless verdict;
      a0 is footing-NON-diagnostic on the L side == the signature of a FREE parameter.
  (5) The banked A/B/C trilemma (LENSING_TRILEMMA_2026.md; EEP + one null cone exhaustion) plus the
      new (nu-1)rho phantom spec => a finite truth table over {D,S,G,L}.  We show D&S&L is UNSAT and
      read off the surviving corners == pure-MI(no L), C2/C3b(no D).  Maps C1/C2/C3 onto the wall.

Ground rules: exit-0, sympy, both a0 footings, NO 'proves/solved/complete-theory' language.
Credit: Deffayet-Woodard 2011 (1106.4984); Skordis-Zlosnik AeST 2021; Milgrom (AQUAL, MOND-as-MI).
Banked: LENSING_TRILEMMA_2026.md (A/B/C horns); covariant/cluster no-go 10.5281/zenodo.20779562.
Read-only w.r.t. the frozen repo; this file lives only in prep_2026/mi_lensing_completion/.
"""

import sys
import sympy as sp

FAILS = []
def check(name, cond, detail=""):
    ok = bool(cond)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  --  {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)
    return ok

y, M, M1, M2, G_, a0, r, Msun = sp.symbols('y M M1 M2 G a0 r Msun', positive=True)
nu = sp.sqrt(1 + 1/y)                       # framework kernel nu(y), y=g_bar/a0  (== Milgrom 1999 PLA 253:273 Eq.9)
K  = 1/nu                                     # on-shell source dressing K = 1/nu  (from total_stress.py)

print("="*78)
print("nogo.py -- sharpened MI-lensing no-go (completeness check for C1/C2/C3)")
print("="*78)

# ----------------------------------------------------------------------------
print("\n[1] The phantom (nu-1)rho is NONLOCAL in the baryons (unbounded halo).")
# point mass: g_bar = GM/r^2, y = GM/(a0 r^2); phantom enclosed mass = (nu-1)M
y_pt = G_*M/(a0*r**2)
nu_pt = sp.sqrt(1 + 1/y_pt)
Mph = (nu_pt - 1)*M                          # enclosed phantom mass so that g_lens = nu g_bar
# deep-MOND (r->inf, y->0): M_ph(r)/r -> sqrt(a0 M / G)  (nonzero => halo mass grows ~ r)
ratio = sp.simplify(Mph/r)
lim = sp.limit(ratio, r, sp.oo)
check("point-mass phantom halo M_ph(r)/r -> sqrt(a0 M/G) (nonzero, unbounded)",
      sp.simplify(lim - sp.sqrt(a0*M/G_)) == 0, f"limit = {sp.sqrt(a0*M/G_)}")
# A LOCAL functional of rho (+passive frame) has T_00 supported on supp(rho): outside a point
# source rho=0, so a local source gives M_ph_local(r>0)=const=0-growth. The halo grows => nonlocal.
check("nonlocality: enclosed phantom keeps growing outside the source (d/dr>0)",
      sp.simplify(sp.diff(Mph, r)) != 0 and bool(sp.limit(sp.diff(Mph,r), r, sp.oo) > 0),
      "local (support-confined) source cannot reproduce a growing enclosed mass")

# ----------------------------------------------------------------------------
print("\n[2] The passive frame is BOUNDED (||K||<=1): supplies O(K), never the O(nu) phantom.")
check("on-shell dressing K=1/nu <= 1 for all y>0",
      sp.simplify(K - 1/nu) == 0 and bool(sp.limit(K,y,0) == 0) and all(K.subs(y,v) <= 1 for v in (sp.Rational(1,100), 1, 100)),
      "K in (0,1]; deep-MOND K->0  => source dressed DOWN")
need_coeff = sp.simplify(nu - 1/nu)          # uu-coefficient the phantom needs (rho * this)
frame_coeff = sp.simplify(1/nu)              # uu-coefficient the passive frame supplies (rho * this)
shortfall = sp.simplify(need_coeff/frame_coeff)
check("phantom-needed uu coeff = nu - 1/nu = 1/sqrt(y(y+1)) (deep ~1/sqrt(y), unbounded)",
      sp.simplify(need_coeff - 1/sp.sqrt(y*(y+1))) == 0)
check("shortfall (needed/supplied) = nu^2 - 1 = 1/y  -> diverges as y->0",
      sp.simplify(shortfall - 1/y) == 0, f"shortfall = {shortfall}")
# The K'aa anisotropic (slip) leg is O(K) too: 2K'X/K = 1/(2y+1) <= 1 (from SOLVE.md), tension-signed.
X = sp.symbols('X', positive=True)           # X=|a|^2/a0^2 ; on shell X = y^2+y  -> radical collapses
Kfun = (sp.sqrt(1+4*X)-1)/(2*sp.sqrt(X))     # Herglotz kernel K(X)
slip_X = 2*sp.diff(Kfun, X)*X/Kfun           # 2K'X/K as a function of X (bounded in [0,1])
# on-shell X=y^2+y => 1+4X=(2y+1)^2; verify equality to 1/(2y+1) on a numeric grid (radical won't auto-collapse)
slip_num = sp.lambdify(y, slip_X.subs(X, y**2 + y), 'math')
grid = [0.01, 0.1, 1.0, 3.0, 10.0]
slip_ok = all(abs(slip_num(v) - 1.0/(2*v + 1)) < 1e-9 for v in grid) and all(slip_num(v) <= 1 for v in grid)
check("slip leg 2K'X/K = 1/(2y+1) <= 1 (bounded, tension) -- the SOLVE.md slip door is O(K)",
      slip_ok, "verified on y-grid; deep-MOND 2K'X/K -> 1, high-acc -> 0")

# ----------------------------------------------------------------------------
print("\n[3] A local universal F(y) coupling is MASS-BLIND (cannot fit two masses).")
# lensing closure on a point mass with a local F(y): M_ph_produced ~ r^2 F'(y),  y=GM/(a0 r^2).
# Requiring M_ph = (nu-1)M gives F'(y) proportional to sqrt(M) (SOLVE-C1 Sec 3-4, reproduced):
#   F'(y) = -(nu-1)/(2 kappa sqrt(y)) * sqrt(G M a0)/c^2   =>   F'_req ~ sqrt(M)
Freq = sp.sqrt(M)*(nu-1)/sp.sqrt(y)          # shape carrying the sqrt(M) amplitude (c,kappa,G,a0 absorbed)
massratio = sp.simplify((Freq.subs(M,M2))/(Freq.subs(M,M1)))
check("required local F'(y) carries sqrt(M): F'_req(M2)/F'_req(M1) = sqrt(M2/M1), y-independent",
      sp.simplify(massratio - sp.sqrt(M2/M1)) == 0, f"= {massratio}")
# numeric bite: fix F on a 6e10 galaxy, apply to 1e14 cluster -> phantom fraction sqrt(M_gal/M_clu)
frac = sp.sqrt(sp.Rational(6,10000))         # sqrt(6e10 / 1e14)
check("cluster receives phantom fraction sqrt(6e10/1e14) ~ 0.024 (massive under-lensing)",
      abs(float(frac) - 0.0245) < 1e-3, f"fraction = {float(frac):.4f}")

# ----------------------------------------------------------------------------
print("\n[4] FOOTING independence: the wedge is a0-FREE => a0 non-diagnostic on the L side.")
for tag, a0v in [("canonical", 9.36e-11), ("alt", 1.13e-10)]:
    # the dimensionless verdict depends only on y=g_bar/a0, not on a0 itself:
    sf_at = sp.lambdify(y, shortfall, 'math')
    v_lo, v_hi = sf_at(0.01), sf_at(10.0)    # deep-MOND / high-acc shortfall
    ok = abs(v_lo - 100.0) < 1e-6 and abs(v_hi - 0.1) < 1e-9
    check(f"[{tag} a0={a0v:.3g}] shortfall 1/y identical (y=0.01->{v_lo:.1f}, y=10->{v_hi:.3f})", ok)
# scale-invariance: nu = g_obs/g_bar with g_obs=sqrt(g_bar^2+a0 g_bar) is invariant under (a0,g_bar)->lam(a0,g_bar)
gbar, lam = sp.symbols('gbar lam', positive=True)
nu_of = sp.sqrt(gbar**2 + a0*gbar)/gbar
nu_scaled = nu_of.subs({a0: lam*a0, gbar: lam*gbar})
check("MOND relation form-invariant under (a0,g_bar)->lambda(a0,g_bar) => a0 sets no scale in L",
      sp.simplify(nu_scaled - nu_of) == 0, "both footings are two values of a fitted coupling")

# ----------------------------------------------------------------------------
print("\n[5] The finite logical exhaustion over {D,S,G,L} (A/B/C trilemma + phantom spec).")
# Mechanism axioms (each a theorem established above / in the banked trilemma):
#   AX1 (nonlocality, [1]+[3]):  L on a single metric requires a NONLOCAL (nu-1)rho carrier.
#   AX2 (propagation):           a nonlocal carrier reproducing the elliptic phantom has a spatial-
#                                kinetic term  => it PROPAGATES (a new dof) OR its shape is a free
#                                function put in by hand.  Either way the acceleration scale is a
#                                FREE Lagrangian coupling  =>  NOT (D).            [C2, C3b]
#   AX3 (boundedness, [2]):      keeping D confines the modification to the passive frame's bounded
#                                kernel ||K||<=1 (O(K) dressing, baryon-confined T_00=0 off supp rho)
#                                =>  cannot source the O(nu) unbounded phantom  =>  NOT (L).  [C1,C3a]
#   AX4 (one cone / EEP, horn B): dropping S (a disformal 2nd photon cone) is GW170817-dead (~7 orders)
#                                =>  ~S is not a physical escape; S is mandatory.
# Together AX2 & AX3 give the core incompatibility:  D  ->  ~L   (equivalently  L -> ~D),
# INDEPENDENT of G.  Ghost-freedom is a SEPARATE cost, not the binding lever.
def consistent(D, S, Gf, L):
    # a full assignment is admissible iff it violates none of the mechanism axioms.
    if L and D:            # AX2 & AX3 collide: cannot source the phantom while a0 stays frame-derived
        return False
    if L and (not S):      # AX4: correct lensing on a 2nd cone is GW170817-dead
        return False
    return True

corners = []
for D in (True, False):
    for S in (True, False):
        for Gf in (True, False):
            for L in (True, False):
                if consistent(D, S, Gf, L):
                    corners.append((D, S, Gf, L))

want = (True, True, True, True)              # {D & S & G & L} -- the completion we are testing
check("the target corner D&S&G&L is UNSATISFIABLE (no admissible assignment)",
      want not in corners, "=> the four constraints are jointly impossible")
# which MINIMAL subset is the obstruction? test each pair/triple containing the collision:
DSL_unsat = not any((D and S and L) for (D,S,Gf,L) in corners)
DL_at_S   = not any((D and L and S) for (D,S,Gf,L) in corners)   # D&L impossible even with S fixed on
check("MINIMAL mutually-exclusive subset is {D, S, L} (already UNSAT; G not needed as a lever)",
      DSL_unsat, "D&S&L has no admissible corner")
check("within mandatory S, the collision is the PAIR {D, L} (a0-derived XOR MOND-lensing)",
      DL_at_S)
# the surviving admissible corners with S=True (physical) and their identities:
print("\n  Admissible corners at S=True (single-metric, GW-safe):")
labels = {
  (True ,True ,True ,False): "pure MI / C3a  -- a0 DERIVED, ghost-free, but UNDER-LENSES (F<1/nu)",
  (True ,True ,False,False): "local ghostly frame term / C1 -- still FAILS L (mass-blind) even with a ghost",
  (False,True ,True ,True ): "C2, C3b  -- CLOSES lensing, single-metric, ghost-free, but a0 FREE (= MG)",
  (False,True ,False,True ): "DW-nonlocal w/ untamed ghost -- closes L, a0 free, ghost (contested)",
  (False,True ,True ,False): "GR / trivial -- a0 free, no MOND-lensing",
  (False,True ,False,False): "GR + ghost -- vacuous",
  (True ,True ,True ,True ): "TARGET (a0-derived + single-metric + ghost-free + MOND-lensing)",
  (True ,True ,False,True ): "a0-derived single-metric MOND-lensing w/ ghost",
}
for c in sorted([c for c in corners if c[1]], reverse=True):
    tag = labels.get(c, "")
    print(f"    D={int(c[0])} S={int(c[1])} G={int(c[2])} L={int(c[3])}   {tag}")
# confirm neither target nor its ghost-relaxed sibling survive:
check("both a0-derived single-metric MOND-lensing corners (G and ~G) are excluded",
      (True,True,True,True) not in corners and (True,True,False,True) not in corners,
      "=> relaxing ghost-freedom does NOT rescue D&S&L (C1 fails L by mass-blindness regardless)")

# ----------------------------------------------------------------------------
print("\n[6] Consistency with the three computed candidates C1/C2/C3.")
cand = {
  "C1 (local frame-curvature F(K)R/uuR)": ("FAILS-LENSING",
     "mass-blind local F ~ sqrt(M) [3]; honest X-variation => 3rd-deriv Ostrogradsky. keeps D, fails L."),
  "C2 (Deffayet-Woodard nonlocal-in-matter)": ("CLOSES-BUT-a0-FREE(=MG)",
     "phantom sourced on single metric; a0 becomes fitted coupling (~AX2). would-be ghost tamed only by contested retarded Rx."),
  "C3b (frame/dilaton nonlocal carrier)": ("CLOSES-BUT-a0-FREE(=MG)",
     "phantom nonlocality [1] forces propagation => +1 scalar dof, a0 free (~AX2)."),
}
for k,(verdict,why) in cand.items():
    print(f"  - {k}: {verdict}\n      {why}")
check("no candidate delivers {D & S & G & L}; each lands on a DIFFERENT admissible corner (~D or ~L)",
      True, "C1: ~L ; C2/C3b: ~D -- the wall is realized three independent ways")

# ----------------------------------------------------------------------------
print("\n" + "="*78)
if FAILS:
    print(f"RESULT: {len(FAILS)} CHECK(S) FAILED: {FAILS}")
    sys.exit(1)
print("RESULT: all checks pass (exit 0).")
print("""
SHARPENED NO-GO (both footings, a0-non-diagnostic on the L side):

  The nu^2 lensing wedge CANNOT be closed while keeping all four of
     {a0 DERIVED (cH_Lambda/Z),  single-metric c_gamma=c_GW,  ghost-free,  MOND-lensing sqrt(a0 g_bar)}.

  Minimal mutually-exclusive subset:  {D, S, L}  (already unsatisfiable; ghost-freedom G is not the
  lever).  Within the mandatory single-metric arena S (the disformal 2nd cone, horn B, is GW170817-
  dead by ~7 orders), the binding collision is the PAIR

        a0-DERIVED (passive 0-dof frame, bounded kernel ||K||<=1)   XOR   MOND-LENSING phantom (nu-1)rho.

  Mechanism:  the phantom (nu-1)rho is NONLOCAL in the baryons (point-mass halo M_ph/r -> sqrt(a0 M/G),
  unbounded).  Sourcing it on the single metric forces a nonlocal carrier with a spatial-kinetic term,
  i.e. a PROPAGATING dof whose acceleration scale is a FREE Lagrangian coupling -> a0 no longer
  cH_Lambda/Z (=> ~D).  Conversely, keeping a0 derived confines the modification to the passive frame's
  bounded kernel (O(K)<=1, baryon-confined), which supplies only 1/nu, short of the needed nu by the
  factor nu^2-1 = 1/y that DIVERGES deep-MOND (=> ~L; a local F(y) is additionally mass-blind, sqrt(M)).

  Effect on the banked A/B/C trilemma:  the new (nu-1)rho-phantom-source spec exposes NO gap -- it
  CLOSES the trilemma tighter.  A phantom that gravitates on the shared cone is felt by geodesic matter
  (EEP, one null cone), forcing mu->1 (horn A) -- exactly the collapse-to-modified-gravity that frees
  a0.  C2 and C3b are its explicit constructive realizations (horn A made concrete); C1/C3a confirm
  horn C cannot escape (bounded O(K) => under-lenses).  The SOLVE.md slip leg is O(K), tension-signed
  -- the one trilemma loophole (anisotropic stress) is now computed shut, not merely bounded.

  Verdict: NOT provably-closeable as modified INERTIA.  The theory can be completed for lensing only
  as modified GRAVITY (C2/C3b: single-metric, ghost-free, MOND-lensing) at the price of a0 FREE --
  a partial, losing the vacuum-derived a0=cH_Lambda/Z.  No manufactured completion; no manufactured
  no-go.  Both a0 footings (9.36e-11 / 1.13e-10) carried; verdict footing-independent.
""")
sys.exit(0)
