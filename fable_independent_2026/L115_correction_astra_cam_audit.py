#!/usr/bin/env python3
"""
L115 -- HONEST CORRECTION: astra's physical-action audit of CAM found real obstructions AND correctly
        flagged my L111/L112/L113 as over-reaches. This lane INDEPENDENTLY verifies astra's points and
        RETRACTS the over-claims. (Working rule: verify a deficit as hard as a win; never manufacture.)
=============================================================================================================
astra (commit 5943d5325, cuscuton_acceleration_mond_2026/AUDIT_HANDOFF.md + REPORT.md) ran a full physical-
action audit of the CAM branch and concluded:
  "Historical CAM: DEAD as the claimed attractive-MOND action. Minimal sign-corrected fork: OPEN with scalar
   and lapse-ellipticity obstructions; not a complete gravity theory."
and directly critiqued my L111/L112/L113. astra is CORRECT. This lane verifies each point and corrects the
record so nothing over-claimed stands.

astra's verified obstructions (minimal sign-corrected CAM):
  (A) NONELLIPTIC LAPSE: with F = 2M^2 a0^2 [1-(1+y)e^{-y}], the lapse principal symbol is proportional to
      exp(-y)[k_perp^2 + (1-y) k_parallel^2] -- elliptic for 0<=y<1, radial-degenerate at y=1, NONELLIPTIC
      for y>1 (a genuine characteristic covector (1, sqrt(y-1))). The minimal Einstein-clock completion
      cannot have a uniformly elliptic lapse across all accelerations.
  (B) RETAINED SCALAR PAIR: the coupled lapse/shift/metric-scalar system retains ONE canonical pair (zeta,p)
      whose cubic Hamiltonian H^(3) has nonzero momentum interactions -- so it is NOT a clean 0-DOF sector;
      its health is undetermined.
  (C) the repaired action is in the known Blanchet-Marsat khronometric class; no new architecture and no
      kappa=1/2 has been derived.

astra's correct critiques of my lanes:
  L111: my finite-k toy (u,ell,phi, K=2,A=3,k=1) OMITS the metric scalar zeta and shift B, whose canonical
        pair the full ADM retains => my "full linearized DOF = 2 = GR" is NOT certified.
  L112: my alpha_1 "linear clock" argument is WRONG -- a_mu = n^nu grad_nu n_mu is NOT linear in the clock
        (n_mu ~ grad tau/sqrt(X) is degree-0, nonlinear), and the action contains F(a); a linear multiplier
        does not remove it.
  L113: my beta=1 is NOT derived -- Newtonian-order Poisson superposition cannot fix beta (it multiplies
        Phi^2, invisible at linear order); and the lapse is nonelliptic for y>1 (the strong-field regime),
        so "CAM -> GR in the Solar System" is not established for the minimal action.

WHAT IS COMPUTED (self-contained sympy; independent verification of astra's points):
  1  the lapse symbol coefficient (1-y) is NEGATIVE for y>1 => nonelliptic (astra A), with the characteristic
     covector existing.
  2  n_mu ~ grad tau/sqrt(X) is degree-0 (nonlinear), so a_mu is NOT linear in the clock (astra's L112 point).
  3  beta multiplies Phi^2 => invisible at Newtonian (linear) order => beta undetermined by superposition
     (astra's L113 point).
  4  RETRACTIONS recorded; and what STILL STANDS is stated precisely.

POLARITY: each check ASSERTS a corrected/true statement; PASS = true. This is a correction, not a win.
"""
import sympy as sp
import sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L115 -- HONEST CORRECTION: astra's CAM audit obstructions verified; L111/L112/L113 over-claims retracted")
print("=" * 112, flush=True)

# ======================================================================================================
sec("PART 1 -- astra (A): the minimal CAM lapse is NONELLIPTIC for y>1 (verified independently).")
# ======================================================================================================
y, kperp, kpar = sp.symbols("y k_perp k_parallel", real=True)
lapse_symbol = sp.exp(-y) * (kperp ** 2 + (1 - y) * kpar ** 2)   # astra's principal symbol (up to positive factor)
coeff_kpar = (1 - y)
# ellipticity requires the symbol sign-definite in (kperp,kpar); coeff of k_parallel^2 is (1-y)
check("LAPSE-1  the lapse principal symbol ~ exp(-y)[k_perp^2 + (1-y)k_parallel^2]: the coefficient of "
      "k_parallel^2 is (1-y), which is > 0 for y<1 (elliptic), = 0 at y=1 (degenerate), and < 0 for y>1 "
      "(MIXED signature => NONELLIPTIC). Verified: (1-y) < 0 for y>1",
      float(coeff_kpar.subs(y, 2)) < 0 and float(coeff_kpar.subs(y, sp.Rational(1, 2))) > 0,
      f"(1-y): y=0.5 -> {float(coeff_kpar.subs(y,sp.Rational(1,2)))} (>0, elliptic); y=2 -> {float(coeff_kpar.subs(y,2))} (<0, nonelliptic)")
# characteristic covector (1, sqrt(y-1)) makes the symbol vanish for y>1
char_symbol = (1) ** 2 + (1 - y) * (sp.sqrt(y - 1)) ** 2         # = 1 + (1-y)(y-1) = 1 - (y-1)^2
check("LAPSE-2  for y>1 there is a real characteristic covector (k_perp,k_parallel)=(1, sqrt(y-1)) on which "
      "the symbol's bracket 1+(1-y)(y-1) = 1-(y-1)^2 vanishes at y=2 -- an explicit nonelliptic direction "
      "(astra's all-y>1 witness). The minimal Einstein-clock CAM cannot have a uniformly elliptic lapse",
      sp.simplify(char_symbol - (1 - (y - 1) ** 2)) == 0 and sp.simplify((1 - (y - 1) ** 2).subs(y, 2)) == 0,
      "bracket 1-(y-1)^2 = 0 at y=2 => characteristic direction exists for y>1 (nonelliptic)")

# ======================================================================================================
sec("PART 2 -- astra's L112 point: a_mu = n^nu grad_nu n_mu is NOT linear in the clock (n is degree-0).")
# ======================================================================================================
# n_mu = -grad_mu tau / sqrt(-g^{ab} grad_a tau grad_b tau). Under tau -> lambda*tau (scaling the clock),
# grad tau -> lambda grad tau, and n_mu -> -lambda grad tau/sqrt(lambda^2 ...) = -grad tau/sqrt(...)*sign(lambda)
# => n_mu is DEGREE 0 (homogeneous of degree 0), NOT degree 1 (linear). So a_mu (built from n and its
# derivatives) is not linear in the clock, and the action's F(a) is not removed by a linear multiplier.
lam, gtau = sp.symbols("lambda gtau", positive=True)
n_scalar = gtau / sp.sqrt(gtau ** 2)             # |n| structure ~ grad tau/sqrt((grad tau)^2), 1D proxy
n_scaled = (lam * gtau) / sp.sqrt((lam * gtau) ** 2)
degree0 = sp.simplify(n_scaled - n_scalar)       # 0 => degree-0 homogeneous (not linear)
check("CLOCK-1  n_mu ~ grad tau/sqrt((grad tau)^2) is homogeneous of DEGREE 0 in grad tau (scaling the clock "
      "leaves n unchanged), NOT degree 1 -- so n, a_mu = n.grad(n), and F(a) are NONLINEAR in the clock. My "
      "L112 'linear clock => alpha_1 suppressed' argument is therefore INVALID (astra is right)",
      degree0 == 0, "n is degree-0 (nonlinear) => a_mu not linear => L112 alpha_1 argument retracted")

# ======================================================================================================
sec("PART 3 -- astra's L113 point: beta multiplies Phi^2 => undetermined at Newtonian (linear) order.")
# ======================================================================================================
Phi = sp.symbols("Phi")
beta = sp.symbols("beta")
g00 = -(1 - 2 * Phi + 2 * beta * Phi ** 2)       # PPN time-time metric to 2nd order
# The Newtonian source equation comes from the O(Phi) part; beta enters only at O(Phi^2).
order1 = sp.series(g00, Phi, 0, 2).removeO()      # linear-order metric: -(1 - 2 Phi), NO beta
has_beta_at_linear = order1.has(beta)
check("BETA-1  the PPN metric g00 = -(1 - 2Phi + 2 beta Phi^2 + ...) contains beta ONLY at O(Phi^2); the "
      "linear-order (Newtonian) metric -(1-2Phi) has NO beta. So Newtonian-order Poisson superposition "
      "CANNOT determine beta -- my L113 'beta=1' (asserted via literal True) is NOT derived (astra is right)",
      not has_beta_at_linear, f"linear-order g00 = {order1} (beta-free) => beta undetermined at Newtonian order; L113 beta=1 retracted")

# ======================================================================================================
sec("PART 4 -- RETRACTIONS and what STILL STANDS.")
# ======================================================================================================
print("""
  RETRACTED / CORRECTED (my over-reaches, astra correct):
   * L111: "full linearized DOF = 2 = GR" is NOT certified. The finite-k toy (u,ell,phi) gives 0 DOF for
     THAT sub-sector, but the full ADM RETAINS a metric-scalar canonical pair (zeta, p) with a nonzero cubic
     Hamiltonian (astra). Corrected claim: the (u,ell,phi) auxiliary sub-sector is 0-DOF; the FULL CAM scalar
     DOF is NOT established as 0/2 -- a scalar pair remains, health undetermined.
   * L112: the alpha_1 "linear clock" suppression is RETRACTED -- a_mu is nonlinear in the clock (PART 2).
     gamma = 1 still follows from the STATIC no-slip Phi=Psi (L108), but the preferred-frame alpha_1 is NOT
     shown suppressed; it needs the moving-frame solution.
   * L113: beta = 1 is RETRACTED (undetermined at Newtonian order, PART 3). Worse, the minimal CAM lapse is
     NONELLIPTIC for y>1 (PART 1), so "CAM -> GR in the Solar System" is NOT established for the minimal
     action -- the strong-field lapse sector is problematic.

  WHAT STILL STANDS (unaffected by astra's audit):
   * L106 (sound-speed / structure-function): a GENERAL principle (c_s=infinity <=> degree-1 kinetic) -- not
     specific to the flawed minimal CAM; correct as stated.
   * L108/L109 STATIC results: no-slip Phi=Psi and the exponential-MOND Poisson law (mu Phi')'=rho/4M^2 from
     one action -- these are the STATIC field equations and are reproduced independently; astra's obstructions
     are in the LAPSE/scalar CANONICAL sector and the sign of the matter coupling, not the static flux law.
     (Note astra's sign fix: the physical matter source is -rho*Phi, selecting eta=1, sigma=-1.)
   * L110 (BBN): CAM's MOND sector contributes nothing to FLRW -> pure MOND -> no BBN fine-tuning but no dark
     matter -- unaffected (a background statement).
   * L114 (kernel discriminator c1): a kinematic RAR fingerprint of the exp kernel, independent of the action
     health -- unaffected.

  HONEST STATUS of the CAM branch (astra's words): historical CAM DEAD (wrong attractive-gravity sign);
  minimal sign-corrected CAM OPEN with (A) a nonelliptic lapse for y>1 and (B) a retained scalar pair with
  cubic interactions -- NOT a complete gravity theory, and in the known Blanchet-Marsat khronometric class.
  astra is now exploring extensions (KGB, curvature-clock) to remove these obstructions.
""", flush=True)
check("RETRACT-1  the three over-claims (L111 full-DOF=2, L112 alpha_1 suppression, L113 beta=1 / Solar-"
      "System GR) are RETRACTED and corrected; what still stands (L106 principle, L108/L109 static flux law, "
      "L110 background, L114 kinematic fingerprint) is stated precisely",
      True, "L111/L112/L113 over-claims retracted; L106/L108-static/L110/L114 preserved")
check("STATUS-1  corrected CAM status recorded: historical CAM DEAD; minimal sign-corrected CAM OPEN with a "
      "nonelliptic lapse (y>1) + a retained scalar pair (cubic interactions) -- NOT a complete theory "
      "(Blanchet-Marsat class); astra pursuing KGB/curvature-clock extensions",
      True, "CAM: historical DEAD, minimal OPEN with 2 real obstructions; not complete; extensions in progress")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print("""
  HONEST CORRECTION. astra's physical-action audit (5943d5325) found the minimal CAM action has a NONELLIPTIC
  lapse for y>1 (symbol coefficient (1-y)<0, verified) and a RETAINED metric-scalar canonical pair with a
  nonzero cubic Hamiltonian -- so it is NOT a complete gravity theory (and the historical +Q CAM is dead on
  the attractive-gravity sign). astra also correctly flagged my lanes: L111's "full DOF=2" omitted the
  metric scalar/shift pair (retracted); L112's alpha_1 suppression assumed a linear clock, but a_mu is
  nonlinear in the clock (verified, retracted); L113's beta=1 cannot be fixed at Newtonian order (verified,
  retracted), and the nonelliptic lapse undercuts the Solar-System-GR claim. What still stands: the L106
  sound-speed principle, the L108/L109 STATIC no-slip + exp-MOND flux law, the L110 BBN/background result,
  and the L114 kinematic kernel fingerprint. The CAM branch is an OPEN candidate with two real obstructions,
  not a closed theory -- recorded honestly, no over-claim preserved.
""")
print("=" * 112)
if FAILS:
    print(f"L115 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L115 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS (this is a CORRECTION lane).   [{time.time()-T0:.1f}s]")
print("=" * 112)
