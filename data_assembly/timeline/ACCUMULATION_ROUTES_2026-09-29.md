# Ways to select and accumulate the data we need (data front, 2026-09-29)

"Cherry-picking" is legitimate here only in one sense: choose objects because of what they can TELL US (their input-side information), never
because of what they would show. A subset picked after seeing the offset from the z = 0 relation can manufacture either verdict for either law. So
every selection axis below uses quantities that exist before any Δ is computed, and each is written down before the numbers are opened
(the frozen-criteria practice the calc thread already uses, CFG141).

## A. Selection axes (input-side only)
| axis | what to require | why it is informative | where to read it |
|---|---|---|---|
| low baryonic acceleration | g_bar at the outermost measured radius below a0, from measured gas + stars | only g_bar ≲ a0 separates flat a0 from a0 ∝ H(z) | needs gas: `INVENTORY_2026-09-29.md` |
| stated radius | velocity at a tabulated radius, not a plateau "V_flat" | g = V²/R needs R | KURVS tables; CRISTAL R_out; ALPAKA digitised |
| measured gas | CO / [CI] / HI / dust with the conversion written down | the baryon budget is the dominant systematic | see B |
| pressure support known | σ(R) measured, not assumed constant | the correction grows with radius (Burkert+10) | `arxiv_tables/kurvs_sigma_profiles/` |
| independence | one entry per galaxy; group members and lensing duplicates flagged | correlated points inflate significance | ledger |
| same-pipeline anchor | z ≈ 0 objects reduced the same way (KROSS↔SAMI) | removes pipeline offsets | `high_z_tf_tables/` |
| blind sign | fix the sign convention of Δ before computing | prevents post-hoc reading | design note §3 |

## B. Routes that add measured gas to objects we already have (biggest single gain)
1. **Positions for the ten rotation-supported KURVS-CDFS discs** and a footprint table against GOODS-ALMA (arXiv:1803.00157, 69 arcmin²), ASAGAO, ASPECS, archival ALMA. Blocked: needs a small public-table query and the owner's go (dismissed once; not run).
2. **Scoville-method dust gas** from public 1.1–1.3 mm source tables at those positions; upper limits count as data.
3. **KURVS COSMOS half:** the paper says it is a forthcoming paper; check arXiv for its release each session.
4. **KGES / KROSS / KMOS3D** galaxies that also sit in PHIBSS, ASPECS or ALPAKA fields (the KMOS3D×PHIBSS overlap was empty and verified; KGES×ALPAKA unchecked).
5. **HI stacks (GMRT-CATz1, CATz1-COSMOS)** as an independent bracket only, never per galaxy.

## C. New objects found in this pass (abstract pages only; **UNVERIFIED** beyond the abstract)
| object / sample | z | tracer | what the abstract states | use |
|---|---|---|---|---|
| Drew+ arXiv:1811.01958, DSFG850.95 | 1.555 | Hα + [NII], MOSFIRE | flat outer curve at 6–14 kpc (1.2–2.8 scale lengths); no gas mass in the abstract | one disc; a submm-selected galaxy, so a dust/CO gas mass may exist elsewhere — not searched |
| Noble+ arXiv:1809.03514 | ~1.6 | CO(2-1), ALMA, 3.5 kpc | 8 cluster galaxies, rotating gas discs in most; elevated gas fractions | cluster environment, but measured CO gas at resolved scale |
| Girard+ arXiv:1909.07400 | ~1 | CO (Cosmic Snake, A521) + [OII] | two lensed galaxies, sub-kpc to few-kpc, major-axis curves and σ profiles | lensed discs with measured CO |
| Motta+ arXiv:1808.02828, Cosmic Seagull | 2.78 | CO(3-2) | f_gas ≤ 80%, curve to 2.6 kpc, no decline | gas by dynamical minus stellar mass, i.e. model-dependent; inner radius |
| MIGHTEE-HI RAR, arXiv:2504.20857 | 0.08 | HI | 19 galaxies, intrinsic scatter 0.045 ± 0.022 dex with resolved M/L | low-z anchor (already in ledger) |
| MIGHTEE-HI/LADUMA, arXiv:2608.03576 | ≤0.09 | HI | 130 galaxies, a0 = (1.50 ± 0.05)e-10, no evolution to z≈0.09 | low-z anchor, other pipeline |
| MIGHTEE-HI bTFR, arXiv:2109.04992 | ≤0.081 | HI | 67 galaxies, no bTFR evolution over the last Gyr | low-z anchor |
| CHILES XI, arXiv:2601.11011 | 0.22–0.47 | HI + CO | 4 galaxies, M_HI 1.6–6.7e10, M_H2 0.4–5.2e10, H2/HI up 10.3 ± 3.4× vs local | the only measured HI + H2 at z ~ 0.3–0.5 found here; 4 objects, resolved HI kinematics not stated in the abstract |
| MIGHTEE-HI z 0.26–0.38 | 0.26–0.38 | HI | "eleven galaxies" (search snippet only) | **UNVERIFIED**; paper not opened |
- **Systematic warning, not data:** de Araujo-Carvalho+ arXiv:2507.10544 (abstract) reports that surface-brightness dimming and lost resolution make cosmic-noon curves look smoother and more symmetric than the truth, so the outer-curve quality of every high-z Hα sample is optimistic. This is a reason to prefer measured gas and low-asymmetry flags, and it applies to KURVS too.

## D. Timeline accumulation without new data
- **Fill the z gap 0.1–0.5 first.** Measured HI+H2 exists only in CHILES XI (4 galaxies) and BUDHIES (166 HI, no stellar masses, z ≈ 0.2). Getting stellar masses for BUDHIES from public photometry is a data task with no new observation.
- **Stack by information, not by outcome:** bin any sample by g_bar/a0 measured at the outermost radius, and report the count per bin, so a bin with too few decisive objects is declared empty before Δ is computed.
- **Cross-survey duplicates:** a galaxy that appears in two surveys gives two independent velocity measurements, useful as a systematic test (KROSS × KGES-style overlaps, unchecked).
- **Record upper limits as data** (CO non-detections, HI non-detections); dropping them is the classic hidden cherry-pick.

## E. What I will not do
- Pick objects by the sign or size of their Δ, or drop the ones that disagree.
- Use a gas mass to "rescue" a curve after seeing it; the gas source and conversion are declared per object first.
- Calculate anything here: g values, verdicts and P-model fits stay in the calculation thread.

## F. Needs the owner's go before I act
1. The position query for the ten KURVS discs (public catalogue, a few kB).
2. Any table or FITS download beyond HTML pages (filename, source, size will be stated first).
