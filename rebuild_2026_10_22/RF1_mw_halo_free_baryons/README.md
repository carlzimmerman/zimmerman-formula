# RF1_mw_halo_free_baryons: UNDETERMINED, no halo-free bulge mass on disk. Bracket reading: the decider is the disc scale length, not the bulge

> **A1 result (2026-10-31, after the text below was committed; `AMENDMENTS.md`, script 60c9eae3d1). A halo-free bulge mass is now on
> disk: Valenti+16 (A&A 587 L6), 2.0 ± 0.3 × 10¹⁰ M☉ in stars and remnants from VVV red-clump counts and the Zoccali+00 empirical
> IMF, no dynamics, no halo, parsed from the paper's text in `_external_data/rf1_valenti2016/` (untracked). The frozen verdict
> item 2, graded at that mass on the McKee ±2σ × BH&G16 ±2σ box with McKee's gas, background A, PRIMARY V_last:**
>
> | rule | verdict | passing cells / 35 | passing R_d | in LN16's R_d tag |
> |---|---|---|---|---|
> | OS1 canonical | **FAIL on halo-free baryons** | 0 | none (best D 1.18 at R_d 1.93: K_z 67.6, χ²_Ou 71) | 0 |
> | OS1 alt | **PASS on halo-free baryons (WIDE PRIORS ONLY)** | 1 | 1.93 kpc | 0 |
> | Native N (footings coincide) | **PASS on halo-free baryons (WIDE PRIORS ONLY)** | 1 | 1.93 kpc | 0 |
>
> Reported, not graded: at +1σ (2.3 × 10¹⁰) OS1 canonical PRIMARY gains one cell at R_d 1.93; at −1σ (1.7) nothing changes;
> VARIANT V_last 229 passes 2–4 cells at R_d 1.93–2.27 on every footing; background B agrees except native N at +1σ (0 cells).
> No cell at R_d ≥ 2.6 passes anywhere. So the diagnostic reading below stands: the bulge moves the count, the disc scale
> length decides. The headline "UNDETERMINED" below is superseded for the bulge input only; the open inputs 2–5 (gas tables,
> vertical structure, R_d read directly, McKee read directly) remain. Checks 9/9 with K8 (value and sha from disk); MUTATE fails
> K1–K3 and exits 1. Runtime 107 s, peak RSS 0.43 GB, one thread, nice 15. This is not "the framework passes the Milky Way":
> it passes only on a disc shorter than the published star-count scale length, on the alt footing and the native rule, and
> fails on the canonical OS1 rule. κ = ½ FITTED. Not theory closed.

Criteria and ledger 9468ee04b2 (committed alone, before any script or number); script 856ffb2959; no amendment. I expected this
headline before running, as the criteria disclose. Runtime minutes, peak RSS 0.35 GB, one thread, nice 15. No download.

## Verdict (frozen)

| rule | canonical | alt |
|---|---|---|
| OS1 (Burkert, q_f on SPARC) | **UNDETERMINED: no halo-free bulge mass on disk** | **same** |
| Native N (working rule; no a₀, footings coincide, K6) | **same** | **same** |

The summary's wording is "exists". I can only say that none has been read. Kent 1992, Dwek+95 and pre-M2M counts are not on
disk, so no row was usable and none came from memory. Neither "FAIL on halo-free baryons" nor "PASS on halo-free baryons" can
be quoted. The Milky Way miss on McMillan 2017 is now labelled **FAIL against ΛCDM-processed baryons** (`LEDGER.md`).

## What is known without a verdict

**BRACKET rows, never graded.** M_bb is Portail+17's, which is ΛCDM-PROCESSED and PROVISIONAL. Gas 13.7 at R₀ (McKee).
Background A; 175 cells.

| rule | BRACKET class | all four lines (fraction of box) | inside both LN tags | best in tags: v_c (z vs Eilers), χ²_Ou |
|---|---|---|---|---|
| OS1 canonical, V_last 173 | V+K ONLY (bg B: WIDE PRIORS, 1 cell) | 0 / 175 = 0.000 | 0 / 25 | 207.6 (−4.6), 281 |
| OS1 alt, V_last 173 | FEASIBLE (WIDE PRIORS ONLY) | 5 / 175 = 0.029 | 0 / 25 | 210.7 (−4.0), 188 |
| OS1 canonical, V_last 229 | FEASIBLE (WIDE PRIORS ONLY) | 15 / 175 = 0.086 | 0 / 25 | 215.1 (−3.0), 106 |
| OS1 alt, V_last 229 | FEASIBLE (WIDE PRIORS ONLY) | 12 / 175 = 0.069 | 0 / 25 | 217.4 (−2.5), 81 |
| **Native N, both footings** | FEASIBLE (WIDE PRIORS ONLY) | 5 / 175 = 0.029 (bg B 4) | 0 / 25 | 210.5 (−4.0), 165 |

**McMillan 2017, labelled ΛCDM-PROCESSED.** Native N: v_c 202.8 (z −5.6), K_z 67.9, χ²_Ou 290. OS1, V_last 173: 200.3 / 203.5
(z −6.2 / −5.5), as GD1. So native N does not lift McMillan's disc, and the K_z key still passes there.

**GD2's short disc against the priors.** R_d 1.933 kpc is inside BH&G16's range (−1.3σ) and outside LN16's (−5.4σ, with
LN16's error PROVISIONAL). Σ_b is inside McKee. So the answer depends on which star-count scale length is used, and the two
sources disagree here. GD2's own canonical cell sat at the top of Portail's box. With McKee's gas in place of McMillan's
(13.7 vs 12.39), OS1 canonical loses its only passing cell on background A, with best D 1.01 at Σ_b 50.5, M_bb 1.64e10 (K_z 70.8 against a limit of
70.8). That edge is too thin to carry weight in either direction. Alt and native N keep cells, all at R_d 1.933.

**The bulge does not decide it. R_d does (LOOKUP, DIAGNOSTIC, not a prior).** With M_bb free from 0.5 to 3.0 × 10¹⁰ and Σ_b at
any of its 5 values:
- Native N, and OS1 with V_last 173, pass **no cell at R_d ≥ 2.6 kpc for any M_bb in that range**.
- Native N at R_d 2.6 reaches v_c 188–221 across that range. L1 needs about 220 at M_bb ≈ 3e10, where the χ²_Ou line still fails.
- OS1 with V_last 229 passes R_d 2.6 only at M_bb 2.5–3.0e10 (canonical at 3.0 only), above Portail's bracket.
- At R_d 1.93 passes occur at nearly every M_bb from 1.0e10 up, on OS1 alt and native N.

So a bulge value read later would most likely move the count, not the class. A disc at LN16's R_d stays out across that
M_bb range on the working rule. A disc at 1.93 passes across it. This is conditional on the labelled shapes below, and it is
not the verdict.

**Sensitivity (bracket box, primary rows).** Gas ±2σ: native N all-4 cells 11 / 2, best in-tag v_c 213.3 / 207.6. z_d × 0.8, × 1.2:
5 / 6. OS1 canonical moves between V+K ONLY and WIDE PRIORS (0–5 cells). No sensitivity gives a passing cell inside both
tags. The class of OS1 canonical is fragile; the in-tag zero is not.

**External field.** Graded at e_N = 0, since route E has no EFE. Largest tide on V_c(R₀): LMC 0.51 km/s with M200 as the upper
bound (0.03 on baryons only); M31 0.004. It does not matter for any key.

## How clean this baryon field is

Not fully, even apart from the bulge. Per the ledger:
- **Normalisations** (Σ_b, gas column, R_d) carry no halo in their derivation, but I have them as transcriptions in the
  record, not from the papers.
- **Gas radial forms, z_d, thin/thick share, bulge shape** are McMillan's, held and labelled. The summary allows z_d only
  where the ledger shows a star-count origin; it does not, so that condition is not met.

## What would close it (owner's OK needed for each)

1. **Bulge:** Kent 1992 and Dwek+95 (or the pre-M2M clump-giant count papers), with mass and the M/L behind it. Check first
   whether each M/L is photometric or was set dynamically; a dynamical M/L with a halo in the fit would not be clean.
2. **Gas:** Σ_HI(R) and Σ_H₂(R) tables from the surveys themselves. Kalberla & Dedes 2008 was fetched for flaring only (CFG574).
3. **Vertical structure:** a star-count source for z_d and the thin/thick share.
4. **R_d, read directly:** BH&G16 and LN16, to settle the −1.3σ against −5.4σ. **This is the input the lookup says matters most.**
5. McKee+15, read directly.

With 1 in hand: add a row to `HALO_FREE_BULGE`, then wire the frozen grade. The script stops rather than guess if a usable row
appears without that step.

## Checks (`rf1_mw.out`)

8/8. K0 McMillan V_b 177.09, K_z,b 61.89. K1 reproduces GD2: canonical 1 cell, D 0.950357; alt 7 cells, D 0.700212. K2 OS1
factors. K3 native table 51.8, 78.5, 149.0, 236.4, 380.4; 29.4 at lg M200 9. K4 halo raises. K5 masses. K6 native footings
identical. K7 RSS. Rerun byte-identical. No 5.364 or Planck value in the scripts. MUTATE (`RF1_MUTATE=1`): K1, K2, K3 FAIL, exit 1.
With McMillan's gas the native box gives 7 cells at R_d 1.93 and 2.27, the same as RG1's P2 log (quoted, not imported).

## Limits

Spherical halo, no contraction, EM1's M200 relation (built on NFW dust on SPARC). One R_d for both discs. Background A is the
record's plik-lite refit; background B's row is printed beside it. Eilers, Ou+24 and Bovy & Rix are Jeans or dynamical
reductions, as in X5's ledger.

Rerun: `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf1_rule.py`, then `... rf1_mw.py`; `RF1_MUTATE=1` for the twin.

κ = ½ FITTED; c_f not used; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.
