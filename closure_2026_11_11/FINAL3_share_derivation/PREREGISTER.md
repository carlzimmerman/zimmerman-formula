# FINAL-3 (SHARE_DERIVATION) — pre-registration, before any FINAL-3 number exists

Lane **LANE FINAL-3 (SHARE_DERIVATION)**. TEST lane: adopts nothing, relabels nothing, registers nothing.
Footings canonical a0 = 9.360324825027975e-11 m/s^2 and alt a0 = 1.1312035414413022e-10 m/s^2, graded
separately, never pooled. Cold dark energy is a gravitating field component; no particle is added anywhere.
kappa = 1/2 FITTED; not theory closed.

## 0. Why this lane exists, and what is already on the record (read before any number here)

**The input rule.** THREE lanes carry `X_s = 59.5 M_b` as a fixed, imposed number:

- **PD1** (`closure_2026_11_09/PD1_phantom_is_dust`, criteria 0dc7929421): "the dust in the Lagrangian
  sphere of the turnaround shell is a fixed **59.5 M_b** for every mass (seed M_b (1 + R))", with
  `share = RHO_D0 * (4 pi/3) x_L^3 + R * M_b` and `r_ta` taken from WL1's transcribed shell solver with
  `dM = M_b (1 + R)`, `a0 = 0`. PD1 labels FAIL/FAIL (first failing gate P2 KiDS).
- **ONE1** (`fable52_push/ONE1_counted_once`, criteria a967a38851): `X_S = 59.5`, `XS_X = 59.9983` (the
  dimensionless end radius). KiDS host-free **PASSES / PASSES** at the 1.6 R_h veto.
- **SRH1** (`closure_2026_11_10/SRH1_settled_radius_history`, criteria 5ed8a37ec6): `X = ONE1's X
  (PD1's share, 59.4861 / 59.5029)`, used to normalise the reference layout `C_R(r_ta) = X M_b`.

None of them DERIVES it. PD1's own RESULT says "neither share reproduces the source's numbers", and its
brackets show KiDS rejects both 10.82 and 5.41. So the number the KiDS pass rests on is an un-fitted,
un-derived convention.

**This lane's job.** Derive the share instead of imposing it: state what is conserved, integrate it over the
formation history of a halo, obtain X_s(z, M_b) as an **output**, then grade the derived value against the
three lanes that used the frozen number.

**Seen before this freeze (no FINAL-3 number of any kind has been computed):** PD1's RESULT, `pd1.py`,
`pd1.out`, `pd1_a1*.out`, `pd1_a2.out`; ONE1's RESULT, `one1_kids.py`, `one1_kids.out`,
`one1_kids_brackets.out`, `one1_kids.json`; SRH1's FROZEN_CRITERIA, RESULT, `srh1_grade.out`,
`srh1_forest_<footing>.out`, `srh1_lens.out`, `srh1_hm.py`; GRW2's FROZEN_CRITERIA (the inverse question,
criteria 1863e717a8); DW1's RESULT (the MW's lever arms).

## 1. What is conserved (stated once, used by every derivation in this lane)

**The cold component's charge.** Concretely, the record's own closure, restated:

1. **Comoving conservation.** Unprocessed cold dust is neither created nor destroyed anywhere in the
   record; its mean density is `rho_c(z) = rho_c0 (1 + z)^3` and the cold-to-baryon ratio carried by any
   comoving fluid element is the cosmic one, `R = omega_d / omega_b`.
2. **Settling rearranges, it does not create.** The "joint" (the still-missing equation that takes the cold
   component from falling dust to the settled halo) may move cold charge into the law's phantom layout, but it
   cannot change the total.
3. **Therefore the settled cold mass of a halo = the cold charge of every shell that has crossed the settling
   front.** With monotone spherical infall, shells cross the front once and in order, so this is exactly the cold
   charge inside the Lagrangian radius `x_L(z)` of the shell that sits at the front at redshift z:

       M_s(z, M_b) = (4 pi / 3) rho_c0 x_L(z)^3 = [R / (1 + R)] * (4 pi / 3) rho_M0 x_L(z)^3 .
                                                                 (H)  the history integral

   **The closed form (used for the numbers):**
       X_s(z, M_b)  =  M_s / M_b  =  [R / (1 + R)] * [ (4 pi / 3) rho_M0 x_L(z)^3 / M_b ] .

   **The integral form (computed as a check, not used for the numbers):**
       M_s(z) = M_s(z_form) + Integral_{t_form}^{t(z)} 4 pi R_set(t)^2 rho_c(a(t))
                                        * | v_r(R_set, t) - dR_set/dt |  dt ,
   with `v_r` and `R_set` from the same shell library; M_s(z_form) is the charge of the
   shells that had already crossed at the formation node.

**The halo identity used below:** the halo's total collapsed mass is its baryons plus its settled cold,
`M_h = M_b (1 + X_s)`. This is ONE1's and SRH1's own normalisation (their total is `(1 + X) M_b`).

**Consistency cap (derived in the criteria, not assumed).** If the settling front coincides with, or lies
inside, the shell that has collapsed — i.e. if the settled region is the collapsed region — then the swept
Lagrangian mass IS `M_h`, whose cosmic-composition cold fraction is `R/(1+R)`. Then

       X_s M_b = [R/(1+R)] M_h = [R/(1+R)] M_b (1 + X_s)   ==>   X_s = R   exactly.

**X_s is therefore not a free number: consistency pins it to the cosmic cold-to-baryon ratio.** Any value
above R requires the settled region to have drawn cold charge from a Lagrangian volume larger than the
collapsed one (a deviation from spherical-collapse bookkeeping that no lane in the record derives); any
value below R means the halo has not yet swept its own patch (a formation-history statement).

## 2. The three pre-registered derivations

All three use §1 verbatim. They differ in ONE physical input: **which shells have delivered their charge**,
i.e. where the settling front is. Let `x_ta(M_h) = (3 M_h / (4 pi rho_M0))^(1/3)` be the comoving radius of
the collapsed patch, and `u = x_L / x_ta` the dimensionless Lagrangian parameter of a shell.

- **D1 — COLLAPSED CORE (primary).** The front is the shell that collapses at the epoch of observation: the
  settled region is the region whose shells have collapsed (and virialised), `R_set = R_vir(z) = r_ta(a_obs)/2`.
  By §1 this gives **`X_s = R` exactly**, at every z and M_b, with no free parameter.
- **D2 — THE FOLD.** The front is FLD1's law-dominated fold radius, `R_set = R_fold(z, M_b)` — the same function
  SRH1 used at f = 1, with no free parameter. Then `X_s = R u^3` with `u` fixed by the inversion
  `r(a_obs; u) = R_fold`, i.e. the charge of the shells that have crossed the fold.
- **D3 — THE BASIN (PD1's rule, recomputed).** The front is the turnaround radius, `R_set = r_ta(z, M_ta)`; this is
  PD1's `share = rho_d0 (4 pi/3) x_L^3 + R M_b`. Reported twice, and graded on the iterated version:
  (a) **one-shot**, PD1's convention (`M_ta = M_b(1+R)`, evaluated once) — this is the input rule, and it is
  the lane's anchor, not a derivation; (b) **iterated**, the fixed point of §1 with the front at r_ta.

**The fixed point.** Given (z, M_b), start from X_s = R (the collapsed-patch value), form
`M_h = M_b (1 + X_s)`, find the Lagrangian parameter `u` of the shell sitting at the front today
(invert `r(a_obs; u) = R_set`), then `X_s <- [R/(1+R)] u^3 M_h / M_b`. Iterate to 1e-10 or declare
divergence after 200 steps. The dimensionless shell problem is **independent of M_h** (G M_h / x_ta^3 is the
same number for every halo), so only u, z and the closure depend on the halo, and the whole map is one
universal function per footing.

## 3. Kill conditions (pre-registered)

A derivation **survives** only if it passes all four.

- **K1 — internal consistency.** The iterated map of §2 must converge to a finite positive X_s. Divergence
  (runaway) kills it: the closure is then not a derivation but a one-shot convention.
- **K2 — ONE1's KiDS host-free row.** ONE1's frozen gate at the 1.6 R_h veto: |z| <= 2 for all / late /
  early; profile chi^2 <= 9.49 (all); type difference |z| <= 2. Reference numbers: model R_s 1.003
  canonical / 0.847 alt for X = 59.5, gate PASS / PASS; measured 1.4002 +- 0.2211 canonical /
  1.2740 +- 0.2012 alt. ONE1's own brackets: X = 5.41 -> z +4.85 / -0.08 / +4.93 canonical and
  +4.93 / -0.07 / +5.00 alt, chi^2 23.7 / 24.4 -> FAIL; X = 10.82 -> +4.34 / -0.19 / +4.47 and
  +4.53 / -0.15 / +4.64, chi^2 19.2 / 20.8 -> FAIL.
- **K3 — SRH1's four gates.** G1 forest Delta chi^2 <= 4 (upper); G2 = 2.2 R_e <= R_set for all 100
  RC100 galaxies (lower); G3 = SPARC coverage or PD1's rms <= 0.0660 / |mean| <= 0.05 (lower); G4 = K2.
  SRH1's numbers: G1 edge 0.722 / 0.725; G4 edge 1.004 / 1.050; gap 1.39 / 1.45; G2 lower 0.391 /
  0.391; G3(a) coverage 0.467 / 0.467.
- **K4 — the four independent rows (CO1's, recomputed with the derived R_cold(k, z)).** C2 PR4 lensing
  amplitude: |A - 1| <= 2 sigma_A, shape chi^2 <= 18.48 (CO1: A = 0.9617 +- 0.0231 canonical /
  0.9564 +- 0.0230 alt, shape chi^2 8.56 / 8.56). C3 DESI DR1 f sigma8, 4 bins: every |pull| <= 2
  (CO1: chi^2 2.23 / 2.20 canonical, 2.29 / 2.23 alt; largest pull 1.22 / 1.23). C4 PR4 lensing
  with the redistribution: |r_eff - 1| <= 0.0481 (CO1: +0.00003 / +0.00005). C5 raw KiDS d_cold < 9
  (CO1: +1.15 / +2.21).

## 4. Labels (per footing)

- **SHARE DERIVED** — D1 (the primary, parameter-free closure) passes K1-K4, every known answer passes and
  every MUTATE arm bites.
- **SHARE NOT DERIVED** — no closure passes K1-K4. The RESULT names the failing gate and the factor by which
  the derived share misses the frozen 59.5.
- **NO VERDICT** — a known answer fails, a MUTATE arm does not bite, or a row cannot be evaluated.

Two qualifiers are printed beside the label either way:
- **KiDS is share-driven, not radius-driven**: printed if the KiDS fail is set by the amount X_s and not by
  the settled radius (checked by re-running G4 at the frozen share with the derived radius, and at the
  derived share with the frozen radius).
- **The 59.5 is a baryon depletion of 1/11**: printed if the derived share divided by the frozen share
  is within 10 % of 1/11.

## 5. Known answers (each must pass on both footings)

- **KA-PD1.** D3 one-shot at z = 0 reproduces PD1's frozen share to 1e-3 relative: 59.4861 (canonical) /
  59.5029 (alt).
- **KA-CHARGE.** The integral form (H) and the closed form of §1 agree to 1e-6 at three (z, M_b) nodes.
- **KA-COSMIC.** With the front at the collapsed shell, the map returns X_s = R to machine precision, i.e.
  5.4092 / 5.4107 (the cosmic share; identical to ONE1's X = 5.41 bracket row).
- **KA-RFOLD.** FLD1's `rfold_kpc` reproduces FZS1's KA-F: 62.2 / 21.3 / 7.6, 139.3 / 47.8 / 17.2,
  168.8 / 57.9 / 21.0, 196.9 / 67.6 / 24.5 kpc at log M_b 9.4 / 10.45 / 10.7 / 10.9 for z = 0 / 2 / 4.
- **KA-G4.** ONE1's machinery run at the derived share X_s = R reproduces ONE1's stored bracket row at
  X = 5.41 to 0.02 in z.

## 6. MUTATE (each must bite on both footings)

- **MU1 — conservation off.** Multiply the swept cold charge by 2 (as if R -> 2 R). X_s must double, and the KiDS
  |z| on "all lenses" must move by more than 1.
- **MU2 — the front reversed in z.** Mirror FLD1's `R_fold` redshift dependence (z <-> 6.6 - z over the twelve
  DESI bins). The derived X_s at z = 3 must change by more than 20 %.
- **MU3 — the iteration is not vacuous.** The one-shot and iterated readings of D3 must differ by more than a
  factor 1.2, or the iteration is reported as vacuous.

## 7. Reported, never graded

- X_s(z, M_b) as a table on both footings at the lens nodes (0, 0.16, 0.31, 0.43), the RC100 nodes
  (0.6, 1.0, 1.5, 2.0, 2.5), the twelve DESI bins, and over log M_b = 8 to 14.
- The decomposition of the derivation into (conserved charge) x (swept volume).
- The internal-consistency diagnostic of the record's shell solver (PD1/WL1's): the Lagrangian mass enclosed
  by the shell it assigns to a given turnaround epoch, divided by the interior mass it was given.

## 8. What counts against (stated now)

- The derivation is a **bookkeeping** result, not a mechanism: the joint (the equation that takes the cold
  component from falling dust to the settled halo) stays missing, as in SRH1 and GRW2.
- Spherical symmetry and monotone first infall, as in every lane that reuses WL1's / FLD1's shells.
- a0 is frozen per footing; if a0(z) is later admitted, X_s(z) inherits it through r_M and the front.
- The two footings are graded separately and never pooled.

## 9. Files

- `PREREGISTER.md` (this file, committed alone, before any script or number).
- `final3.py` -> `final3.json` / `final3.out` (the derived share, the gates, the known answers, MUTATE).
- `RESULT.md` (the label on both footings).
