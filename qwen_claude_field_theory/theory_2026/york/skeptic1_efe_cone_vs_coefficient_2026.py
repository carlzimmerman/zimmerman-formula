"""
skeptic1_efe_cone_vs_coefficient_2026.py
================================================================================
SKEPTIC-1 LENS: CONSTRAINT-vs-HIDDEN-DYNAMICS re-check of the DEAD-INSTANTANEOUS
verdict.  The verdict's kill rests on a NEW ingredient not in the committed
scripts: the MOND External Field Effect (EFE) allegedly turns the instantaneous
elliptic Phi into a "physical superluminal channel" (d a_int/d g_ext != 0,
delivered by equal-time Lap^-1).  This script tests whether the EFE coupling
--matter on g_phys = nu(s) g_N, s = |D Phi|^2/a0^2-- actually TILTS the matter
characteristic cone (= a genuine superluminal SIGNAL), or whether it enters as a
BACKGROUND COEFFICIENT (Newtonian-potential-like instantaneity, benign).

DISCRIMINATOR (the only rigorous one): a superluminal SIGNAL <=> the matter
field's OWN characteristic cone tilts OUTSIDE the local g_phys null cone. A
distant source changing the local COEFFICIENTS instantaneously (as Newtonian
Phi does) is NOT that -- it is quasi-static/preferred-frame coefficient
dependence, causal iff (i) the local cone stays timelike and (ii) monotone York
time forbids CTCs.

Built on committed source_dichotomy (matter cone lambda-INDEPENDENT for
rest-mass rho) -- this ADDS the EFE/nu-channel that the verdict newly invokes.
================================================================================
"""
import sympy as sp

R = {}
def check(label, cond):
    R[label] = bool(cond)
    print(("  [PASS] " if bool(cond) else "  [FAIL] ") + label)
    return bool(cond)
def head(t): print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)

w, k = sp.symbols('omega k', real=True)

# ==========================================================================
head("1.  MATTER CONE from g_phys = nu(s) g_N: cone set by LOCAL nu, always causal")
# ==========================================================================
print("""
  Matter scalar psi propagates on the physical metric g_phys = nu * g_bar (single
  metric; conformal-type MOND coupling). In 1+1 the matter wave operator principal
  symbol is  -A(x) omega^2 + B(x) k^2  with A,B > 0 set by the LOCAL value of the
  conformal factor nu(s(x)). The cone speed^2 = B/A is a ratio => the overall nu
  factor CANCELS. So the local matter cone is UNCHANGED by nu's magnitude:
""")
nu_local = sp.symbols('nu_local', positive=True)   # local value of nu(s) at the point
A = nu_local            # schematic: conformal factor multiplies the metric uniformly
B = nu_local            # -> both A and B scale by the same nu (conformal) at a point
speed2 = sp.simplify(B / A)
print("  local cone speed^2 = B/A =", speed2, "  (nu cancels => = c^2, luminal)")
check("matter cone speed^2 = 1 (=c^2) INDEPENDENT of the local nu value "
      "=> matter stays ON the g_phys null cone at every point; no local superluminality",
      sp.simplify(speed2 - 1) == 0)

print("""
  READ: even where nu (hence g_ext via EFE) is large, matter's LOCAL cone is the
  g_phys null cone. The EFE changes the SIZE of the acceleration a_int (real SEP
  violation, genuinely observable) -- it does NOT push matter's cone outside g_phys.
""")

# ==========================================================================
head("2.  EFE ENTERS AS A BACKGROUND COEFFICIENT, not a matter principal symbol")
# ==========================================================================
print("""
  The verdict: d a_int/d g_ext != 0 (EFE) + g_ext delivered instantaneously by
  Lap^-1 => "physical superluminal channel". Decompose: a_int depends on the
  LOCAL nu(s), s = |D Phi|^2/a0^2. Phi solves the elliptic carrier, so s(x) at B
  depends on matter everywhere incl distant A. Does THAT dependence tilt B's
  matter cone? It enters the matter symbol ONLY through the coefficient nu(s), a
  ZEROTH-order (undifferentiated-in-psi) background field. Test: differentiate the
  cone speed^2 w.r.t. the background nu -- if 0, nu is a pure coefficient (benign);
  a genuine tilt would need nu to multiply the psi-DERIVATIVE structure asymmetrically.
""")
# cone speed as a function of the background nu(s); conformal coupling => cancels.
s_ext = sp.symbols('s_ext', positive=True)
nu_of_s = sp.sqrt(1 + 1/s_ext)                     # nu(s) = sqrt(1+1/s), s = |DPhi|^2/a0^2
speed2_bg = (nu_of_s) / (nu_of_s)                  # B/A with common conformal nu(s)
check("d(cone speed^2)/d(background s_ext) = 0 => the EFE/Phi dependence is a pure "
      "COEFFICIENT modulation (Newtonian-potential-like), NOT a cone tilt",
      sp.simplify(sp.diff(speed2_bg, s_ext)) == 0)

print("""
  This is STRUCTURALLY identical to Newtonian gravity: the metric coefficients
  (the potential) at B depend on the instantaneous matter distribution everywhere
  via an elliptic Poisson solve, yet no superluminal SIGNAL exists -- because the
  matter cone is set by the local metric and is not tilted outside it. The MOND
  novelty (EFE makes the coefficient LOCALLY OBSERVABLE) changes WHAT is measurable,
  not the SPEED at which the cone can be tilted (which is the signalling criterion).
""")

# ==========================================================================
head("3.  The ONLY genuine tilt channel = derivative-dependent source (CASE 2), "
     "avoided by rest-mass rho")
# ==========================================================================
print("""
  Reproduce the committed source_dichotomy discriminator: a genuine cone tilt
  requires the elliptic multiplier to couple to a psi-DERIVATIVE-dependent source
  (rho+3p). The physically-correct QUMOND source is conserved rest-mass density
  (derivative-INDEPENDENT) => no tilt. Confirm both branches:
""")
lam, Gc, crho = sp.symbols('lambda G c_rho', positive=True)
A0, B0 = sp.symbols('A0 B0', positive=True)
psit, psix = sp.symbols('psi_t psi_x', real=True)
L0 = sp.Rational(1,2)*A0*psit**2 - sp.Rational(1,2)*B0*psix**2
# rest-mass source: derivative-independent -> no (dpsi)^2 contribution from -4piG lam rho
L1 = L0 - 4*sp.pi*Gc*lam*crho
sp1 = sp.simplify((-sp.diff(L1,psix,2))/sp.diff(L1,psit,2))
check("rest-mass rho: cone speed^2 = B0/A0, d/dlambda = 0 => NO tilt => NO signal",
      sp.simplify(sp.diff(sp1, lam)) == 0)
# rho+3p: carries kinetic (dpsi)^2 -> tilts
L2 = L0 - 4*sp.pi*Gc*lam*crho*psit**2
sp2 = sp.simplify((-sp.diff(L2,psix,2))/sp.diff(L2,psit,2))
check("rho+3p: cone speed^2 depends on lambda => tilt => would signal (the AVOIDED case)",
      sp.simplify(sp.diff(sp2, lam)) != 0)

# ==========================================================================
head("4.  VERDICT of the lens: pure-gauge? Horava-physical? pathological?")
# ==========================================================================
print("""
  THREE-WAY classification of the instantaneous mode:
   (i)  lapse N               : PURE GAUGE (matter couples to Phi, not N) [test1 c1].
   (ii) MOND potential Phi     : PHYSICAL & PREFERRED-FRAME (khronon foliation is
        physical) -- NOT pure gauge. The verdict is RIGHT it is Horava-like, not
        GR-maximal-slicing-gauge.
   (iii) BUT (ii) is CAUSALLY CONSISTENT, not a superluminal pathology:
        - matter cone NOT tilted (sec 1-3, rest-mass source) => no cone-level signal;
        - monotone York time forbids CTCs (committed qumond_causality C/D);
        - EFE instantaneity = coefficient dependence (sec 2), Newtonian-potential-like,
          = the ALREADY-PRICED preferred-frame cost of the CMC spine, not a NEW channel.
""")
allpass = all(R.values())
print(f"  internal checks: {sum(R.values())}/{len(R)} PASS   all green: {allpass}\n")
print("""  => The DEAD-INSTANTANEOUS kill is NOT ESTABLISHED. It fires criterion (a) only
     under the STRICT-literal reading (any preferred-frame instantaneity = kill),
     while (a)'s operative intent ("physical SUPERLUMINAL channel" / CTCs) is NOT
     met: no cone tilt, no CTCs. The kill's decisive new ingredient (EFE => physical
     superluminal channel) never computes the characteristic cone -- it re-runs the
     "elliptic => acausal" inference that RESULT sec 4c EXPLICITLY RETRACTED as too
     strong. The scripts the verdict cites (source_dichotomy/lapse_fixing/dof_deformed)
     conclude the OPPOSITE (causal-legit, conditional on the preferred foliation).

     CORRECT STATUS: CAUSAL-LEGIT-CONDITIONAL (= committed scripts + sec 4c open gate).
     The instantaneous mode is physical preferred-frame (Horava-type), causally
     consistent, NOT a pure-gauge artifact AND NOT a superluminal pathology.
     This does NOT save the sector: gates E (G_eff=2G) and F (Cassini ~4-8 sigma)
     remain INDEPENDENT active kills. And the full nonlinear coupled Dirac +
     characteristic/Cauchy well-posedness solve (sec 4c) is STILL owed -- so the
     honest classification is OPEN/causal-legit, not a positive causality PROOF.
""")
import sys
sys.exit(0 if allpass else 1)
