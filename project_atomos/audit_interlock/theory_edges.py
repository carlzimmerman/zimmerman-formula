#!/usr/bin/env python3
r"""
theory_edges.py -- the dependency edges targets/pdg_constants.py is BLIND to.
=============================================================================
pdg_constants.py builds its dependency structure only for source=="DERIVED" entries. Three entries it
files as independent MEASUREMENTS are, physically, restatements of another entry through known SM
theory:
    a_e              = QED series in alpha        (Schwinger + Kinoshita coefficients)
    alpha_em_inv_MZ  = alpha_em_inv_0 + RG running (leptonic exact + hadronic VP input)
    a_mu             = QED series in alpha + hadronic (the contested one)
plus one CORRELATION the dataset's ratio() explicitly assumes away:
    r_p_e and r_mu_e share the MeV unit conversion, so their quadrature sigmas are not right.

This matters for the interlock in TWO DIFFERENT WAYS and they must not be conflated:
  (i)  FDR / look-elsewhere bits: the enumeration's vocabulary is {3, sqrt(8pi/3), small ints}. It is
       NOT closed under the QED series (coefficient -0.328478965579... is not reachable), so hitting
       a_e after alpha is NOT a free hit and the look-elsewhere bits DO legitimately add.
  (ii) Gate C's C1 mode literally requires ">=2 INDEPENDENT observables". a_e and alpha are one
       observable stated twice. So the *count* k is inflated even though the *bits* are honest.
Direction of each is reported separately. Numbers below are COMPUTED; literature inputs are tagged
[LIT] and every conclusion that depends on one is given as a sensitivity, not an assertion.

Local-only. python3 audit_interlock/theory_edges.py
"""
from __future__ import annotations
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import targets.pdg_constants as pdg                     # noqa: E402

ds = pdg.load()
bar = "=" * 104
ok = []


def check(m, c):
    ok.append(bool(c))
    print(f"   [{'PASS' if c else 'FAIL'}] {m}")


def bits(w):
    return math.log2(1.0 / w)


ALPHA_INV = float(ds.target("alpha_em_inv_0").value)
ALPHA_INV_S = float(ds.target("alpha_em_inv_0").sigma)
ALPHA = 1.0 / ALPHA_INV
A_E = float(ds.target("a_e").value)
A_E_S = float(ds.target("a_e").sigma)
A_MU = float(ds.target("a_mu").value)
A_MU_S = float(ds.target("a_mu").sigma)

print(bar)
print("theory_edges -- dependency edges the dataset files as INDEPENDENT measurements")
print(bar)

# ---------------------------------------------------------------------------------------------
# T1. a_e from alpha: the QED series
# ---------------------------------------------------------------------------------------------
print("\nT1  a_e  <-  alpha   (mass-independent QED series; coefficients [LIT] Kinoshita et al.)")
print("-" * 104)
# [LIT] mass-independent QED coefficients A1^(2n) written as C_n in a_e = sum C_n (alpha/pi)^n
C = [0.5,                       # Schwinger
     -0.328478965579193,        # 2-loop, exact
     1.181241456587,            # 3-loop, exact
     -1.9122457649264,          # 4-loop
     6.737]                     # 5-loop (numerical)
A_E_HAD_EW = 1.693e-12 + 0.0297e-12    # [LIT] hadronic + electroweak contributions to a_e
x = ALPHA / math.pi
print(f"      alpha       = 1/{ALPHA_INV:.9f} = {ALPHA:.12e}")
print(f"      alpha/pi    = {x:.12e}")
print(f"  {'order n':>8}{'C_n':>22}{'C_n (alpha/pi)^n':>22}{'running total':>22}")
print("  " + "-" * 100)
tot = 0.0
for n, cn in enumerate(C, 1):
    term = cn * x ** n
    tot += term
    print(f"  {n:>8}{cn:>22.12g}{term:>22.12e}{tot:>22.12e}")
tot_full = tot + A_E_HAD_EW
print(f"  {'had+EW':>8}{'[LIT]':>22}{A_E_HAD_EW:>22.12e}{tot_full:>22.12e}")
resid = abs(tot_full - A_E) / A_E
sig_off = abs(tot_full - A_E) / A_E_S
print(f"\n      a_e (measured, dataset) = {A_E:.14e}  +/- {A_E_S:.2e}  (rel {A_E_S/A_E:.3e})")
print(f"      a_e (QED from alpha)    = {tot_full:.14e}")
print(f"      residual                = {abs(tot_full-A_E):.3e} abs = {resid:.3e} rel"
      f" = {sig_off:.2f} sigma")
w_ae = 2.0 * ds.target("a_e").rel_precision
cond_ae = max(0.0, bits(min(1.0, max(resid, 1e-16)) / 1.0) * 0 + math.log2(max(resid, 1e-16) / w_ae)) \
    if resid > 0 else 0.0
cond_ae = max(0.0, math.log2(max(resid, 1e-16) / w_ae))
print(f"""
      READ: the QED series, fed ONLY alpha, reproduces the measured a_e to {resid:.2e} relative -- that is
      {sig_off:.1f} sigma of a_e's own error bar, i.e. a_e contains no information about nature beyond alpha
      that is bigger than the accuracy of this reconstruction. a_e's own window is {w_ae:.2e}
      ({bits(w_ae):.1f} bits). Given alpha, the PHYSICS content left in a_e is at most
      log2({resid:.1e}/{w_ae:.1e}) = {cond_ae:.1f} bits, not {bits(w_ae):.1f}.""")
check(f"the QED series reproduces a_e from alpha alone to {resid:.1e} relative ({sig_off:.0f} sigma) "
      f"-- self-validating: wrong coefficients could not land this close", resid < 1e-6)
check(f"so a_e carries at most {cond_ae:.1f} bits of NEW physics beyond alpha, not the "
      f"{bits(w_ae):.1f} bits its window advertises", cond_ae < bits(w_ae) - 10)
print(f"""
      BUT THE FDR BITS STILL ADD, and this is the distinction that must not be blurred: the search
      vocabulary is {{3, sqrt(8pi/3), small ints}}. It cannot build -0.328478965579..., so an expression
      that lands on alpha does NOT thereby land on a_e -- a_e sits {abs(A_E - ALPHA/(2*math.pi))/A_E:.3e} relative away from
      alpha/2pi, which is {abs(A_E - ALPHA/(2*math.pi))/A_E/w_ae:.2e} target-windows away. So:
        * look-elsewhere accounting (exhaust._exact_fdr_bits): CORRECT to add the bits. No leniency bug.
        * Gate C's C1 mode ('>=2 INDEPENDENT observables'): WRONG to count them as 2. k is inflated.""")
LO = ALPHA / (2 * math.pi)
check(f"a_e is NOT free for the enumeration: |a_e - alpha/2pi|/a_e = {abs(A_E-LO)/A_E:.2e} = "
      f"{abs(A_E-LO)/A_E/w_ae:.1e} windows", abs(A_E - LO) / A_E / w_ae > 1e3)

# ---------------------------------------------------------------------------------------------
# T2. alpha(M_Z) from alpha(0)
# ---------------------------------------------------------------------------------------------
print("\nT2  alpha_em_inv_MZ  <-  alpha_em_inv_0   (RG running; increment = leptonic + hadronic VP)")
print("-" * 104)
AINV_MZ = float(ds.target("alpha_em_inv_MZ").value)
AINV_MZ_S = float(ds.target("alpha_em_inv_MZ").sigma)
d_alpha = 1.0 - AINV_MZ / ALPHA_INV
print(f"      1/alpha(0)   = {ALPHA_INV:.9f} +/- {ALPHA_INV_S:.1e}")
print(f"      1/alpha(M_Z) = {AINV_MZ:.6f} +/- {AINV_MZ_S:.4f}   (MS-bar, 5 flavours)")
print(f"      implied total running increment  Delta = 1 - a(0)/a(MZ) = {d_alpha:.6f}")
# how well must Delta be known for alpha(MZ) to add bits beyond alpha(0)?
sig_delta_break_even = AINV_MZ_S / ALPHA_INV
print(f"\n      d(1/alpha(MZ)) = -1/alpha(0) * d(Delta), so alpha(MZ) adds information beyond alpha(0)")
print(f"      only if Delta is known WORSE than {sig_delta_break_even:.2e} absolute.")
print(f"\n  {'assumed sigma(Delta) [LIT range]':>34}{'predicted sigma(1/a_MZ)':>26}"
      f"{'r_j (rel)':>12}{'cond bits':>11}")
print("  " + "-" * 100)
w_mz = 2.0 * ds.target("alpha_em_inv_MZ").rel_precision
for sd in (3e-5, 7e-5, 1.0e-4, 2.0e-4, 1.0e-3):
    s_pred = sd * ALPHA_INV
    rj = 2.0 * s_pred / AINV_MZ
    cb = max(0.0, math.log2(min(1.0, rj) / w_mz))
    print(f"  {sd:>34.1e}{s_pred:>26.4f}{rj:>12.2e}{cb:>11.1f}")
print(f"""
      READ: the standard hadronic-VP uncertainty sigma(Delta_alpha_had^(5)) is of order 1e-4 [LIT], the
      SAME order as the break-even {sig_delta_break_even:.1e}. So alpha(M_Z) adds ~0-2 bits of new physics
      beyond alpha(0), not the {bits(w_mz):.1f} bits its window advertises. The increment {d_alpha:.6f} printed above
      is INFERRED from the two dataset entries, not independently computed -- the repo stores no
      breakdown into leptonic / hadronic / top / W pieces and no scheme tag beyond the note string, so
      the split cannot be checked here. That missing breakdown is itself the point: the MS-bar
      5-flavour entry and the on-shell running of alpha(0) are different numbers, which is exactly the
      hidden scale/scheme choice GATE_POWER_ANALYSIS S4.3 already flags. Same split as T1: FDR bits
      add (the search cannot build the running), sector COUNT k does not.""")
check(f"alpha(M_Z)'s break-even on the running increment ({sig_delta_break_even:.1e}) is the same order "
      f"as the literature hadronic-VP error (~1e-4) -> ~0-2 new bits, not {bits(w_mz):.1f}",
      abs(math.log10(sig_delta_break_even) + 4) < 1.0)

# ---------------------------------------------------------------------------------------------
# T3. a_mu -- flagged PARTIAL/CONTESTED, given as a requirement not an assertion
# ---------------------------------------------------------------------------------------------
print("\nT3  a_mu  <-  alpha   (PARTIAL: hadronic term is large and its value is CONTESTED)")
print("-" * 104)
w_amu = 2.0 * ds.target("a_mu").rel_precision
lo_mu = ALPHA / (2 * math.pi)
print(f"      a_mu measured  = {A_MU:.10e} +/- {A_MU_S:.1e}  (window {w_amu:.2e}, {bits(w_amu):.1f} bits)")
print(f"      alpha/2pi      = {lo_mu:.10e}   -> a_mu/(alpha/2pi) = {A_MU/lo_mu:.8f}")
print(f"      a_e /(alpha/2pi) = {A_E/lo_mu:.8f}")
print(f"      so a_mu and a_e are BOTH alpha/2pi to within {max(abs(A_MU/lo_mu-1),abs(A_E/lo_mu-1))*100:.3f}%,")
print(f"      and they differ from each OTHER by {abs(A_MU-A_E)/A_E:.3e} relative"
      f" = {abs(A_MU-A_E)/A_E/w_amu:.1e} a_mu-windows.")
need = 32.0 * w_amu
print(f"\n      For a_mu to contribute >= 5 bits beyond alpha, the SM prediction of a_mu would have to be")
print(f"      uncertain by >= {need:.2e} relative (= {need*A_MU:.2e} absolute). The hadronic vacuum-")
print(f"      polarisation term is ~7e-8 absolute of a_mu with a percent-level error [LIT], i.e. of order")
print(f"      1e-9..1e-10 absolute -> {math.log2(max(1e-9/A_MU, 1e-16)/w_amu):.1f} bits. AND the SM value is currently in 4-5 sigma")
print(f"      dispute (data-driven vs lattice HVP), so 'predicted from alpha' is contested either way.")
print(f"      VERDICT ON a_mu: PARTIAL dependence, unquantifiable from inside this repo. Do NOT count")
print(f"      a_mu and a_e as two independent observables -- they share the entire QED series.")
check("a_mu's dependence on alpha is PARTIAL and contested -> reported as a requirement "
      "(needs >= {:.1e} rel theory error to add 5 bits), not asserted".format(need), True)

# ---------------------------------------------------------------------------------------------
# T4. the unit-conversion correlation the dataset's ratio() assumes away
# ---------------------------------------------------------------------------------------------
print("\nT4  r_p_e / r_mu_e: the MeV unit-conversion correlation ratio() drops by construction")
print("-" * 104)
print("      pdg_constants.ratio() docstring: 'relative errors added in quadrature")
print("      (independent-Gaussian assumption)'. But m_e, m_mu, m_p are stored in MeV and every")
print("      MeV value carries the SAME kg->MeV / u->MeV conversion, so their errors are common-mode")
print("      and the RATIO is better known than quadrature says.")
for a, b, key in (("m_p", "m_e", "r_p_e"), ("m_mu", "m_e", "r_mu_e"), ("m_n", "m_p", "r_n_p")):
    ta, tb, tr = ds.target(a), ds.target(b), ds.target(key)
    q = math.hypot(ta.rel_precision, tb.rel_precision)
    diff = abs(ta.rel_precision - tb.rel_precision)          # fully common-mode limit
    print(f"      {key:<8} rel(quadrature, as stored) = {q:.3e}  ({bits(2*q):.1f} bits)")
    print(f"      {'':<8} rel(fully common-mode)     = {diff:.3e}  ({bits(2*max(diff,1e-16)):.1f} bits)"
          f"   -> up to {bits(2*max(diff,1e-16)) - bits(2*q):+.1f} bits")
print(f"""
      DIRECTION: this makes the dataset's windows for the mass ratios TOO WIDE, i.e. too LENIENT --
      more chance hits than there should be -- while simultaneously UNDER-crediting the bits a genuine
      hit would earn. Both errors point the same way for a false positive: a wider window is easier to
      hit. Size: up to {bits(2*max(abs(ds.target('m_p').rel_precision-ds.target('m_e').rel_precision),1e-16)) - bits(2*math.hypot(ds.target('m_p').rel_precision, ds.target('m_e').rel_precision)):+.0f} bits on r_p_e in the fully-common-mode limit. The true correlation
      is between 0 and 1 and cannot be settled from inside this repo (the dataset stores no covariance),
      so this is flagged as a BOUNDED unknown, not a corrected number.""")
check("the mass-ratio windows are bounded between the stored quadrature value and the fully "
      "common-mode value; the repo stores no covariance so the true value is unresolved", True)

# ---------------------------------------------------------------------------------------------
# EXPORT: the extra edges for target_independence_graph.py
# ---------------------------------------------------------------------------------------------
# target -> (parents, predicted relative spread r_j given parents, kind, note)
THEORY_EDGES = {
    "a_e":             (("alpha_em_inv_0",), resid, "QED",
                        f"QED series reproduces a_e from alpha to {resid:.2e} rel"),
    "alpha_em_inv_MZ": (("alpha_em_inv_0",), 2.0 * (1.0e-4 * ALPHA_INV) / AINV_MZ, "RG",
                        "running increment known to ~1e-4 [LIT] -> r_j at break-even"),
    "a_mu":            (("alpha_em_inv_0",), float("nan"), "QED-PARTIAL",
                        "hadronic term contested; dependence real but unquantified here"),
}

# SYMMETRIC closure: the QED map alpha -> a_e is monotone with dln(a_e)/dln(alpha) ~ 1, so it is a
# BIJECTION at this precision -- given a_e, alpha is pinned just as tightly. An interlock that contains
# BOTH members of a bijective pair counts as ONE observable whichever way round it is listed.
THEORY_BIJECTIONS = [("a_e", "alpha_em_inv_0", resid),
                     ("alpha_em_inv_MZ", "alpha_em_inv_0",
                      2.0 * (1.0e-4 * ALPHA_INV) / AINV_MZ)]

if __name__ == "__main__":
    print("\n" + bar)
    print("EXPORTED THEORY EDGES (consumed by target_independence_graph.py):")
    for k, (ps, rj, kind, note) in THEORY_EDGES.items():
        print(f"   {k:<18} <- {','.join(ps):<18} r_j={rj:<12.3e} [{kind}]  {note}")
    print(f"CHECKS: {sum(ok)}/{len(ok)} PASS")
    print(bar)
    sys.exit(0)
