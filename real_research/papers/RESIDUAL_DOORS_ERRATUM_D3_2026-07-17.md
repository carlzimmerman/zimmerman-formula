# Erratum (v3, 2026-07-17) — Correction to the D3 Sign-Flip Signature

**Paper:** *No Pump-Free Corner: The Residual Doors of Covariant Modified Inertia, Computed — and a Pre-Registered Sign-Flip Signature for Dynamically Unsettled Galaxies* (Zenodo concept DOI [10.5281/zenodo.21179352](https://doi.org/10.5281/zenodo.21179352)).

**Author:** Carl Zimmerman, Briar Creek Tech (carl@briarcreektech.com).

---

## Scope of this erratum

This erratum corrects **only door D3** — the pre-registered infall-phase σ-spread sign-flip signature (§5, the corresponding abstract sentence, and Table in §5). **The core result of the paper — that no pump-free MOND-sign channel exists (doors D1, D2, D4, and the §6 all-orders extension of the sign wall) — is UNAFFECTED and stands as published.** D3 is the paper's own "one door that opens," a forward prediction fused from the Theorem-VI transient and the memory-kernel σ-spread; it does not enter the sign-wall closure, and correcting it does not touch D1/D2/D4/§6.

A subsequent, more careful reconciliation of the σ-spread sign (workflow-verified, both coefficient footings, five committed exit-0 scripts under `prep_2026/cluster_efe_sign/`, repo commit `dd12427b`) found that the D3 sign-flip as published is **backwards in polarity and hostage to a non-framework memory timescale**, for two identifiable reasons. What survives, corrected, is *cleaner* than what was printed: an existence claim that is theorem-grade, and a leading-sign claim of the opposite polarity.

## What is wrong, and why

The published D3 states (§5, abstract, Table): *"first-infall systems run 11–21% cold, flipping to hot after pericentre"* — a coherent pre-pericentre **deficit** flipping to a post-pericentre **excess**, with amplitudes Crater II +13.6–26.5%, first-infall −11 to −21%, decisive at 3σ ≈ 2029–2031. Two errors:

1. **Polarity inversion (a bookkeeping error).** The "cold isolated past" of a first-infall member was encoded as a **low** value of the loading ratio y = ω_ex/ω_in. But in the external-field effect the loading factor θ(y) is **maximal** as y → 0; true isolation is a_ext → 0 (**zero** external loading), not low-y. Correctly, a first-infall member on a rising-field approach has a *memory-felt* external field **below** its current field, so it is **under-loaded relative to a matched settled member — hence hotter, not colder.** A parallel text-label slip in the companion script (`rederive_spread_and_power.py`, echoed in `GAP_STATEMENT.md` E4/E7) printed "plungers less boosted" while its own loop output them hotter — the same conflation of "low θ" with "low boost," when low θ means *less suppression* and therefore *more* boost. The claimed raw-loading-versus-memory "competition" was an artifact of this encoding: in field space the two contributions **reinforce** (under-loaded = hotter), and the net sign is fixed unambiguously by sign(a_ext,felt − a_ext,now).

2. **Timescale hostage (a physics error).** The dated pericentre *flip* was computed with a Lorentzian memory kernel of τ = 0.45 Gyr (a dwarf-sector value), which is **not** the framework's committed covariant memory time. The equation-book kernel gives τ_mem = 2c/a₀ = 2Z/H_Λ = **203 Gyr (canonical) / 168 Gyr (alt)**, footing-free (τ_mem·H_Λ = 2Z = 11.58) and algebraic from the kernel. Against a cluster crossing time of ~1–2 Gyr, this is **τ_mem ≫ τ_cross ⇒ the deep-adiabatic regime**, in which a sharp sub-orbit pericentre flip **freezes out** — the same correction already made for the star-orbit σ-spread channel (which fell from a nominal 6–13% to sub-percent for the same reason). Only the un-anchored 0.45 Gyr value made the flip a resolvable transient.

## The corrected statement

D3 is replaced by a **two-tier** claim:

- **(i) Existence — theorem-grade, MG-impossible, sign-independent.** At fixed cluster-centric gravitational field, cluster members exhibit a non-zero internal-σ spread correlated with infall history. In any instantaneous-EFE gravity (QUMOND/AeST; Milgrom's MG-virial universality) this fixed-field history spread is **exactly zero**; its existence is therefore modified-gravity-impossible. This claim is unchanged in force and is the sole theorem-grade content of D3.

- **(ii) Leading sign — first-infall pre-pericentre zone only, conditional on the s = −1 postulate.** Among members matched at the same cluster-centric field, **first-infall pre-pericentre members are HOTTER** (larger internal σ) than matched long-resident / post-pericentre members; equivalently σ-excess decreases monotonically with accumulated loading (≈ time-since-infall). This sign is **structural and timescale-free** — on a monotonically rising approach the causal memory-felt field is always below the current field, so the member is under-loaded for *any* causal kernel — and was found robust across the full memory-time / kernel-shape / member-depth grid and an independent orbit-distribution scan (0/125 sign flips).

**The dated pericentre sign-flip (pre-pericentre deficit → post-pericentre excess) is retracted.** Post-pericentre and backsplash zones are timescale-hostage (their sign depends on the memory time within its uncertainty) and are not pre-registrable; the ancient/virialized zone is ~zero.

**Corrected magnitude.** At the framework-committed E10 memory the MG-impossible history spread is **~0.3–1.5% absolute / ~4–9.5% relational** (residence-time-limited), reaching the printed ~7–24% only in the short-memory (0.45 Gyr) corner. The instantaneous θ(y_cur) boost of 6–13% quoted elsewhere is a **current-configuration** quantity that modified gravity partly shares, not the MG-impossible discriminant.

**Corrected falsifier.** The published kill-condition is inverted. A significantly **negative** fixed-field sign — first-infall members measured **cooler** at ≥ 3σ — or a null spread, is what would falsify the corrected prediction. (As printed, a "coherent pre-pericentre deficit" was named as the *signature*; it is in fact the *falsifier*.)

**Corrected decisiveness.** With the amplitude reduced to the residence-limited few-percent level and the sharp flip removed, the "3σ ≈ 2029–2031" forecast is **not supported**. The corrected observable is currently **underpowered**: the nearest bite is an exploratory (~2–3σ, firewalled) MaNGA/SAMI IFU diffuse-dwarf reanalysis at fixed phase-space tags; a clean detection needs 30 m-class (ELT/HARMONI, ~2032) resolved dispersions or a dedicated wide-cluster IFU dwarf survey, plus explicit modeling of projection scatter and the same-signed tidal-heating confound (both unmodeled in the original D3 lanes). These do not affect the existence (MG = 0) claim.

## Root cause and verification

Both errors trace to door D3's forward-prediction lane and to one companion script; no other door, and no result in the sign-wall closure, uses the affected code path. The reconciliation was carried out with the framework's own kernel and orbit integrator, on both coefficient footings (materially identical, < 2% on every sign fraction), with an adversarial verify pass that confirmed the pinned memory timescale follows algebraically from the kernel (independent of the sign it produces) and that the surviving first-infall-hotter sign holds at all three committed memory corners. Scripts: `prep_2026/cluster_efe_sign/{setup_diagnose,net_sign,robustness}.py` (all exit 0), `SETUP.md`, `NET_SIGN.md`, `ROBUSTNESS.md`, `VERIFY.md`, `SYNTHESIS.md`.

Consistent with this program's standing practice, this correction is reported with the same weight as the original claim. The interpolation kernel remains Milgrom's (Phys. Lett. A 253:273, 1999; ApJ 270:365, 1983; the EFE subsystem boost, Phys. Rev. D 106:064060, 2022); the acceleration scale a₀ and the sign s = −1 remain postulates, and the corrected leading sign depends on the s = −1 postulate (s = +1 reverses it). The signature is modified-inertia-class-generic (it distinguishes any history-dependent inertia from modified gravity, not this framework from Milgrom's linear model). No claim of proof is made for the framework; MG = 0 at fixed true field is the sole theorem-grade claim, and it is unchanged.
