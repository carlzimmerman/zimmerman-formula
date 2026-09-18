#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L272 -- THE CUSCUTON-POINT alpha_1 for the magnitude-only EFE: attempted, with an explicit confidence ceiling.

The single most-likely killer (L270/L271): does the 2-DOF cuscuton (non-dynamical khronon) point admit
alpha_1 = 0?  This lane attempts it.  CONFIDENCE LABELS are load-bearing here: [RIGOROUS], [LIT/validated],
[CEILING].  This is NOT at the confidence level of L268-L271; the definitive khronometric reduction is
flagged as not reproduced.

  P1 [RIGOROUS] the hypersurface-orthogonal aether has NO spin-1 (transverse-vector) mode: delta u_i =
     d_i chi is pure longitudinal, so alpha_1 cannot arise from an aether vector mode (the Einstein-aether
     mechanism); it is a spin-0 (khronon) effect only.
  P2 [LIT=Foster-Jacobson 2006, GR-validated] in the EA formulas the cuscuton limit (c1+c4 -> 0) and
     alpha_1 = 0 (numerator c3^2 + c1 c4 = 0) are COMPATIBLE: c4 = -c1, c3 = +-c1 gives a CLEAN alpha_1=0
     (denominator 2c1 != 0), a 1-parameter family.
  P3 [CEILING] khronometric (h.o.) is NOT EA-with-restricted-couplings for the PPN parameters; the
     definitive reduced khronometric alpha_1(alpha_K,beta_K,lambda_K) (Blas-Sibiryakov 2011) is NOT
     reproduced here, and alpha_2 is not attempted.  So P2 is SUGGESTIVE, not a validated khronometric pass.

VERDICT: cuscuton-point alpha_1 = 0 is PLAUSIBLE/ACHIEVABLE on EA-level evidence (GR-validated,
compatible, clean); formally still OPEN pending the khronometric Blas-Sibiryakov reduction and alpha_2.
Neither a validated pass nor a kill -- the most-likely killer does NOT fire at the level I can compute.

Run:  python3 fable_independent_2026/L272_cuscuton_alpha1.py
"""
import os, sys, json
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "L272_cuscuton_alpha1"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L272", "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
# =================================================================================================
banner("P1 [RIGOROUS] the h.o. aether has no spin-1 mode -> alpha_1 is spin-0, not the EA vector mechanism")
x, y, z = sp.symbols('x y z', real=True)
chi = sp.Function('chi')(x, y, z)
du = [sp.diff(chi, v) for v in (x, y, z)]                       # delta u_i = d_i chi (longitudinal)
div_du = sum(sp.diff(du[i], [x, y, z][i]) for i in range(3))    # = laplacian(chi)
# a transverse mode needs div = 0 for arbitrary chi; here div = lap(chi) is generically nonzero, and a
# gradient has zero curl -- so delta u is pure longitudinal, no transverse (spin-1) content.
curl_z = sp.simplify(sp.diff(du[1], x) - sp.diff(du[0], y))    # (curl du)_z = 0 for a gradient
check("P1 delta u_i = d_i chi is a pure gradient: curl(delta u) = 0 identically, so the h.o. aether has "
      "NO transverse-vector (spin-1) perturbation -- alpha_1 cannot come from an aether vector mode "
      "(unlike Einstein-aether); it is a spin-0 khronon effect",
      f"curl(delta u)_z = {curl_z} (=0, pure gradient); div(delta u) = lap(chi) (generically !=0)",
      curl_z == 0,
      "this is rigorous and it is WHY the khronometric alpha_1 differs from the general-aether one")

# =================================================================================================
banner("P2 [LIT=FJ2006, GR-validated] cuscuton limit and alpha_1=0 are compatible in the EA formulas")
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
alpha1 = -8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2)      # Foster-Jacobson EA alpha_1 (literature)
gr = sp.limit(alpha1.subs({c2: 0, c3: 0, c4: 0}), c1, 0)
# cuscuton limit: scalar speed s0^2 -> inf requires c1+c4 -> 0 (a factor c14 in the s0^2 denominator)
a1_cusc = sp.simplify(alpha1.subs(c4, -c1))                     # at the cuscuton point
a1_zero = sp.simplify(a1_cusc.subs(c3, c1))                     # + alpha_1=0 condition c3 = +-c1
denom = sp.simplify((2 * c1 - c1**2 + c3**2).subs(c3, c1))      # must be nonzero => clean, not 0/0
check("P2 [LIT/GR-validated] alpha_1(GR limit)=0, and at the cuscuton point (c4=-c1) the condition "
      "alpha_1=0 is met by c3=+-c1 with a CLEAN (nonzero-denominator) zero -- cuscuton and alpha_1=0 are "
      "COMPATIBLE (1-parameter family: c1 free, c3=+-c1, c4=-c1, c2 free)",
      f"alpha_1(GR)={gr}; alpha_1(cuscuton,c3=c1)={a1_zero}; denominator there={denom} (!=0)",
      gr == 0 and a1_zero == 0 and denom != 0,
      "the FJ alpha_1 is the Einstein-aether formula, validated at the GR limit; the compatibility is a "
      "genuine computation on it")

# =================================================================================================
banner("P3 [CEILING] the honest confidence limit -- this is SUGGESTIVE, not a validated khronometric pass")
# document the ceiling as a real statement, not a pass/fail: EA != khronometric for PPN.
ceiling = ("khronometric (hypersurface-orthogonal) is NOT EA-with-restricted-couplings for the PPN "
           "parameters; the definitive reduced alpha_1(alpha_K,beta_K,lambda_K) (Blas-Sibiryakov 2011) is "
           "not reproduced here, and alpha_2 (messier FJ form) is not attempted")
P(f"    [ceiling] {ceiling}")
check("P3 the result is SUGGESTIVE (EA-level, GR-validated) not DEFINITIVE (khronometric-reduced): the "
      "confidence is explicitly below L268-L271; the exact khronometric alpha_1/alpha_2 remain the last "
      "genuine computation",
      "EA-level compatibility established; khronometric Blas-Sibiryakov reduction + alpha_2 NOT done",
      True and (a1_zero == 0),      # passes iff P2 held; documents that the CEILING is attached to a real result
      "recorded so the chain is not over-read: the most-likely killer does not fire at the level I can "
      "compute, but 'suggestive' is not 'proven'", load_bearing=False)

# =================================================================================================
banner("VERDICT")
P("""  (1) ATTEMPTED: the cuscuton-point alpha_1 -- the single most-likely killer of the magnitude-only EFE.
  (2) RESULT: [RIGOROUS] the h.o. aether has no spin-1 mode, so alpha_1 is a spin-0 effect (not the EA
      vector mechanism).  [LIT/GR-validated] in the Foster-Jacobson EA formulas the cuscuton limit
      (c1+c4->0) and alpha_1=0 (c3^2+c1 c4=0) are compatible and give a clean alpha_1=0 on a 1-parameter
      family.  [CEILING] khronometric != EA for PPN; the definitive reduced alpha_1 (Blas-Sibiryakov) and
      alpha_2 are NOT reproduced.
  (3) HONEST SENTENCE: the most-likely killer does NOT fire at the level I can compute -- cuscuton-point
      alpha_1=0 is plausible and achievable on EA-level, GR-validated evidence.  But this is SUGGESTIVE,
      explicitly a notch below the rigor of L268-L271: the exact khronometric alpha_1/alpha_2 from the
      Blas-Sibiryakov reduction is the last genuine computation, and I did not reproduce it reliably, so I
      will not call it a validated pass.  Status: cuscuton alpha_1 formally OPEN, evidence pointing to
      ACHIEVABLE.  Even a definitive alpha_1=0 would still leave alpha_2, the full ghost Hamiltonian, and
      the slip-lock -- so this does not complete the theory; it clears (suggestively) the item most
      likely to have killed it.
      NOT CLAIMED: a validated khronometric alpha_1, alpha_2, ghost-freedom, or viability.""")
OUT["verdict"] = {"word": "CUSCUTON-ALPHA1-SUGGESTIVE-ACHIEVABLE-FORMALLY-OPEN",
                  "spin1_absent_rigorous": True, "EA_cuscuton_alpha1_zero_compatible": True,
                  "khronometric_definitive": False, "alpha2_attempted": False,
                  "confidence": "suggestive (EA-level, GR-validated); below L268-L271",
                  "residual": ["definitive khronometric alpha_1/alpha_2 (Blas-Sibiryakov)", "full ghost Hamiltonian", "slip-lock"]}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb = [nm for nm, ok, l in CH if l and not ok]
P(f"L272 COMPLETE: {npass}/{n} checks PASS  (confidence: SUGGESTIVE, not validated -- see P3 ceiling)")
for nm in lb:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb else 0)
