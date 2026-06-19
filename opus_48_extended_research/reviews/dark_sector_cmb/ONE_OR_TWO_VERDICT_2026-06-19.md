# One component, two, or a tension? — the framework's dark-sector accounting (2026-06-19)

*Resolves whether the cluster-required collisionless component (Tremaine-Gunn floor) and the
CMB/structure-required cold component (free-streaming floor) can be the SAME species. Code +
full both-ways print: `dark_sector_cmb/one_or_two.py`. Quarantine held (a0/Z/kappa not derived).
An Omega~0.25 coincidence is NOT a unification unless ONE m satisfies BOTH floors.*

## HEADLINE
**TWO-NEEDED in the strict reading — OR a single keV+ species that makes the dark sector
'nuLCDM-LIKE' (relocated, not eliminated, DM). It is NOT a one-number unification either way.**
The eV cluster-only fix (HOT, galaxy phase-space-excluded) and the cold CMB/structure fix
(keV, third peak + small-scale power) are in genuine TENSION as a single particle: their mass
windows are **disjoint by ~8x** (galaxy-exclusion needs m < ~390 eV; Lyman-alpha small-scale
power needs m > ~3100 eV). The only single particle that threads both is a >~3-6 keV species —
but a keV species is TG-ALLOWED in galaxies, so it clusters in disks as warm CDM and is NOT
phase-space-excluded: galaxy-safety then rests on the MOND-vs-CDM degeneracy, not on TG. The
Omega~0.25 closeness is a FREE amplitude (I0 / sterile abundance) that LCDM also fits, not a
prediction from a0=Lambda.

## THE OVERLAY (this repo's TG norm, verified vs AFD-2010 Eq.14 to 0.3%; literature floors)
| floor | mass | meaning |
|---|---|---|
| cluster TG (pack a cluster core) | **4.3 eV** | m above -> CAN fill clusters |
| L* spiral TG | 69 eV | |
| dSph TG (this repo iso / lit) | **390 eV** (100-390 eV) | m below -> galaxy phase-space EXCLUDED ("hot escape") |
| **CMB free-streaming (Lyman-alpha WDM, 95%)** | **3.1 keV** (loose) – **5.7 keV** (strict) | m above -> cold enough for small-scale structure |

To be ONE species doing the cluster-only HOT fix AND the cold CMB you need simultaneously
`m < 390 eV` (galaxy exclusion) AND `m > 3100 eV` (CMB free-streaming) -> **EMPTY (gap ~8x)**.

## THE TWO READINGS OF "GALAXY-SAFETY" (the crux)
- **Reading (I) — HOT ESCAPE (Sanders/Angus, m ~ a few eV):** m below the dSph floor so it is
  phase-space-excluded from galaxies (this is why 40 yr of eV-neutrino cluster fixes never
  spoiled rotation curves). Window **~4.3-100 eV EXISTS** — but it is ~100-190x too HOT for the
  CMB small-scale floor. **=> needs a SEPARATE cold CMB component => TWO components.**
- **Reading (II) — nuLCDM (m ~ keV):** m above the ~3-6 keV CMB floor is automatically above
  every galaxy TG floor by 1-3 dex. So it is TG-ALLOWED in galaxies: a 3-6 keV species has
  half-mode halo mass ~3e7-3e8 Msun, BELOW typical SPARC disks (1e9-1e11) -> it DOES cluster in
  galaxies as warm CDM. Galaxy-safety is then NOT phase-space exclusion; it is the standard
  MOND-with-CDM degeneracy. **=> ONE component, but it is CDM-by-another-name, not a MOND
  elimination of galaxy DM.**

## BOTH-WAYS: the 11 eV Angus counterexample (do not overstate the CMB floor)
Angus 2009 (MNRAS 394, 527) showed a SINGLE 11 eV sterile reproduces the CMB power spectrum
INCLUDING the third peak (Omega_nu_s h^2 ~ 0.117 ~ Omega_CDM at recombination; 3x(1-2 eV) active
nu instead suppress P3 ~25%). So **"CMB strictly needs keV" is an OVERSTATEMENT at the bare
third-peak level.** BUT the 11 eV hot fix is killed by the FULL modern package: fully-thermalized
-> DeltaN_eff ~ 1 vs Planck+DESI N_eff=3.0+-0.2; DESI+Planck sterile m_eff ~ 0.5 eV (arXiv:2501.10785,
~20x below 11 eV); and it free-streams ~10s Mpc -> wipes Lyman-alpha small-scale power. **The
eV-hot vs keV-cold tension therefore STANDS on 2024 data — it is the N_eff/DESI/Lyman-alpha axis
(not the bare peak height) that bites the eV species.**

## THE FLUID ESCAPE (AeST K(Q) — the framework's ACTUAL banked CMB-fix)
The banked CMB-fix is NOT a thermal particle: it is the AeST K(Q) scalar's a^-3 "dust" mode
(Skordis-Zlosnik 2021) — a FLUID, exactly a^-3, ZERO free-streaming (cold by construction, no TG,
no Lyman-alpha cutoff), amplitude = free integration constant I0 ~ Omega_dm ~ 0.26, orthogonal to
a0=Lambda. The fluid REMOVES the eV/keV tension (a fluid is cold and not TG-bound) but NOT the
cost: (i) fluid-for-CMB + particle-for-clusters = TWO dark sectors; (ii) one-fluid-for-both is the
literature-OPEN AeST question (ROUTE2/SKORDIS: "remains to be seen") and carries no galaxy
phase-space exclusion (same nuLCDM tension); (iii) either way I0~0.26 is a SEPARATE free number,
not from a0=Lambda.

## HONEST VERDICT (no manufactured unification, no reflexive dismissal)
1. As a SINGLE PARTICLE the cluster (hot, galaxy-excluded, eV) and CMB (cold, keV) fixes are in
   genuine **TENSION** (windows disjoint ~8x). The clean Sanders/Angus eV cluster-fix is too hot
   for the CMB -> needs a second species.
2. A single **>~3-6 keV** (sterile-nu joint X-ray+Lyman-alpha window m_s >~ 20 keV) species CAN
   thread cluster+galaxy+CMB numerically — but ONLY as **warm CDM that clusters in galaxies too**.
   That is **nuLCDM-like: DM RELOCATED, not eliminated.** The framework then replaces galaxy-scale
   DM with MOND yet **still needs ~LCDM-amount of cold DM for clusters+CMB.** Say so honestly.
3. The **Omega~0.25 closeness is NOT a unification** — it is a free amplitude (I0 / sterile
   abundance) that LCDM also free-fits; nothing ties it to a0=Lambda (the Bridge-1 theorem says
   a0 is absent from linear perturbations, so a0 demonstrably does not set it).

## ANSWER TO 'one_or_two'
**TWO-NEEDED** under the strict (phase-space-honest) reading; collapses to **ONE keV+ species
only by becoming nuLCDM** (cold CDM in galaxies, MOND-degenerate galaxy-safety). Not a one-number
unification in any reading. The cluster-fix and CMB-fix CAN share one cold species, but that
species is consensus (warm) dark matter relocated onto a MOND background — "no dark matter" is
forfeited at clusters AND the CMB.

## SOURCES (real, 2026-06-19)
- WDM Lyman-alpha floor: Villasenor+2023 (arXiv:2209.14220) m_WDM>3.1 keV; Irsic+2024 (PhysRevD.109.043511, arXiv:2309.04533) m_WDM>5.7 keV.
- TG dSph fermion floor: Alvey+2018 (arXiv:1704.06644) ~100 eV (Segue1)/127 eV (TriII); closure-file conservative 390 eV.
- 11 eV sterile CMB fit: Angus 2009 (MNRAS 394, 527; arXiv:0805.4014).
- DESI+Planck sterile mass / N_eff: arXiv:2501.10785 (m_eff~0.5 eV).
- DW sterile X-ray exclusion + resonant Shi-Fuller: Boyarsky/XRISM lit; Abazajian 2014 (arXiv:1403.0954); m_s>~20 keV joint window.
- AeST K(Q) a^-3 dust / I0 free: Skordis-Zlosnik 2021 (arXiv:2007.00082); repo ROUTE2_CMB_THROUGH_AEST, SKORDIS_CMB_CLUSTER_DEEPDIVE_LEDGER (2026-06-15).
- Repo TG cluster floors + closure: tremaine_gunn_matter_route.py, CLUSTER_RESIDUAL_CLOSURE_2026-06-19.md.
