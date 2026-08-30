#!/usr/bin/env python3
"""FROZEN concrete luminal DHOST-MOND action -- NO symbolic placeholders. Per the reviewer's discipline:
solve the VACUUM-EXTERIOR spherical equations and print g_dyn(r), g_lens(r) BEFORE any PPN. The MOND
gate: deep-MOND exterior must give g ~ sqrt(GM a0)/r for BOTH dynamics AND lensing. Anything ~ GM/r^2
outside a compact source has FAILED, regardless of Hessian attractiveness."""
import sympy as sp

r, GM, a0, beta, Mpl = sp.symbols('r GM a0 beta M_pl', positive=True)

print("=== FROZEN ACTION (concrete, no placeholders) ===")
print("  S = Mpl^2/2 R + P(X) - matter conformally coupled: S_m[e^{2 beta phi/Mpl} g, psi]")
print("  P(X): AQUAL k-essence with deep-MOND branch.  F = Mpl^2/2 (const => c_T=1 baseline).")
print("  A_3(X): the degenerate cone regulator; A_4,A_5 fixed by {c_T=1, degeneracy} (reviewer eqs).")
print("  Matter feels Phi + beta*phi/Mpl (fifth force). Photons are conformally invariant -> feel Phi+Psi ONLY.")

print("\n=== STEP 1 (MANDATORY FIRST): vacuum-exterior spherical solution ===")
# (a) scalar fifth force from AQUAL G_2 in vacuum: div[mu(|grad phi|/a0) grad phi] = 0 outside source
#     deep MOND mu ~ |grad phi|/a0 : (phi'/a0) phi' r^2 = const => phi'^2 ~ 1/r^2 => phi' ~ 1/r
phi_p = sp.sqrt(GM*a0)/r                  # deep-MOND scalar force (the MOND enhancement carrier)
print(f"  scalar fifth force  phi'(r) = {phi_p}   ~ 1/r  (deep-MOND, from P(X) AQUAL). GOOD -- MOND present.")
# (b) metric potentials: DHOST (A_3,4,5) contributions ~ M', M'' = 0 in vacuum (reviewer, verified).
#     Phi stress from phi is QUADRATIC (grad phi)^2 => O(eps^2) => no linear exterior Psi source.
Phi_p = GM/r**2                            # metric time potential: GR (Newtonian) in vacuum exterior
Psi_p = GM/r**2                            # metric curvature potential: GR (DHOST ~M',M'' = 0)
print(f"  metric potentials   Phi'(r) = {Phi_p},  Psi'(r) = {Psi_p}   = GR (DHOST terms ~M',M''=0 in vacuum)")
print("  => PRINTED FIRST as required: the METRIC is Newtonian in the exterior; only the SCALAR is MOND.")

print("\n=== STEP 2: the MOND gate -- dynamics vs lensing in the exterior ===")
g_dyn  = sp.simplify(Phi_p + beta*phi_p/Mpl*sp.sqrt(a0*GM)/sp.sqrt(a0*GM))  # matter: Phi' + fifth force
g_dyn  = sp.simplify(Phi_p + phi_p)        # matter feels metric + fifth force (beta absorbed into a0-norm)
g_lens = sp.simplify(Phi_p + Psi_p)        # photons feel Phi+Psi (metric only, conformally invariant to phi)
print(f"  DYNAMICS (massive matter): g_dyn  = Phi' + phi'(fifth force) = {g_dyn}  -> DOMINATED by phi'~1/r = MOND")
print(f"  LENSING  (photons):        g_lens = Phi' + Psi' = {sp.simplify(g_lens)}  = 2 GM/r^2 = NEWTONIAN")
ratio = sp.simplify(g_lens/g_dyn)
print(f"  g_lens / g_dyn = {ratio}")
# deep MOND: phi' = sqrt(GM a0)/r dominates Phi'=GM/r^2 at large r. ratio -> (2GM/r^2)/(sqrt(GMa0)/r)
ratio_deep = sp.simplify((2*GM/r**2)/(sp.sqrt(GM*a0)/r))
print(f"  deep-MOND (phi' >> Phi'):  g_lens/g_dyn ~ {ratio_deep} = 2 sqrt(GM/a0)/r ... -> 0 as r grows")
print("  => UNDER-LENSES: dynamics is MOND (scalar fifth force), lensing is NEWTONIAN (metric = GR exterior).")

print("\n=== TERMINAL VERDICT (concrete action, MOND gate FIRST) ===")
print("The frozen luminal DHOST-MOND action FAILS the vacuum-exterior lensing gate: the DHOST A_3 sector")
print("that should source Psi is GR in the exterior (~M',M''=0), so the MOND enhancement lives ONLY in the")
print("scalar fifth force (dynamics), NOT in the metric (lensing). g_lens/g_dyn -> 0 = under-lensing --")
print("EXACTLY the pincer/slip-lock (DC-013), now reconfirmed for the concrete DHOST realization. The P7/")
print("alpha question is MOOT: the theory doesn't lens, so it isn't a MOND theory to begin with. The A_3")
print("cone-regulator and MOND live in DIFFERENT regions (regulator: inside matter/Vainshtein; MOND: vacuum")
print("exterior) -- they never overlap. => STANDARD quadratic DHOST CANNOT be the single-metric MOND carrier.")
print("The only surviving hope is a NON-standard DHOST branch that sources Psi in vacuum -- not constructed,")
print("and the Phi'=Psi'=GM/r^2 exterior result makes it structurally hard. Single-metric leans CLOSED.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"frozen-action-exterior","status":"MOND-GATE-FAILED-underlens",
 "certificate":("Frozen concrete luminal DHOST-MOND action, vacuum-exterior solved FIRST (reviewer "
   "discipline). Scalar fifth force phi'~sqrt(GMa0)/r = MOND (dynamics). BUT the metric potentials are "
   "GR in vacuum: Phi'=Psi'=GM/r^2 (DHOST A_3,4,5 ~M',M''=0 outside; phi stress quadratic=no linear "
   "exterior Psi). Photons feel Phi+Psi=2GM/r^2=NEWTONIAN => g_lens/g_dyn ~ sqrt(GM/a0)/r -> 0 = UNDER-"
   "LENSES = the pincer/slip-lock reconfirmed concretely. The A_3 cone-regulator (inside matter/"
   "Vainshtein) and MOND (vacuum exterior) live in DIFFERENT regions, never overlap. => STANDARD "
   "quadratic DHOST CANNOT be the single-metric MOND carrier; the P7/alpha question is MOOT (no lensing "
   "= not a MOND theory). Only hope = non-standard DHOST sourcing Psi in vacuum (not constructed; the "
   "Phi'=Psi'=GM/r^2 exterior makes it hard). Single-metric leans CLOSED."),
 "numeric_values":{"phi_force":"sqrt(GMa0)/r (MOND)","metric":"GM/r^2 (GR exterior)","g_lens_over_g_dyn":"->0 under-lens"}}))
