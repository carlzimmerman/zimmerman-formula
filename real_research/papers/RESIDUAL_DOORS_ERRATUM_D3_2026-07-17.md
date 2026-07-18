# Erratum (v3, 2026-07-17): Correction to the Door D3 Sign-Flip Signature

**Paper:** *No Pump-Free Corner: The Residual Doors of Covariant Modified Inertia, Computed* (Zenodo concept DOI 10.5281/zenodo.21179352).
**Author:** Carl P. Zimmerman, Briar Creek Tech (carl@briarcreektech.com).

---

## Scope

This erratum corrects **only Door D3** -- the pre-registered infall-phase velocity-dispersion sign-flip signature (Section 5, its Abstract sentence, and the pre-registered table). **The core result of the paper -- that no pump-free MOND-sign channel exists (Doors D1, D2, D4 and the Section 6 all-orders extension of the sign wall) -- is UNAFFECTED and stands as published.** D3 is the paper's own "one door that opens," a forward prediction; it does not enter the sign-wall closure, and correcting it does not touch any other door.

A subsequent, more careful reconciliation of the dispersion-spread sign (workflow-verified, both coefficient footings, five committed exit-0 scripts under `prep_2026/cluster_efe_sign/`) found the D3 sign-flip as published to be **backwards in polarity and hostage to a non-framework memory timescale**, for two identifiable reasons.

## 1. Polarity inversion (a bookkeeping error)

The "cold isolated past" of a first-infall member was encoded as a *low* value of the loading ratio $y = \omega_{\rm ex}/\omega_{\rm in}$. But the external-field-effect loading factor $\theta(y)$ is *maximal* as $y \to 0$; true isolation is $a_{\rm ext} \to 0$ (**zero** external loading), not low $y$. Correctly, a first-infall member on a rising-field approach has a memory-felt external field **below** its current field, so it is **under-loaded relative to a matched settled member -- hence hotter, not colder.** The claimed raw-loading-versus-memory "competition" was an artifact of this encoding: in field space the two contributions reinforce (under-loaded $=$ hotter), and the net sign is fixed by $\mathrm{sign}(a_{\rm ext,felt} - a_{\rm ext,now})$. A parallel text-label slip in the companion script printed "plungers less boosted" while its own loop output them hotter -- the same conflation of low $\theta$ with low boost, when low $\theta$ means *less* suppression and therefore *more* boost. Corrected on the record.

## 2. Timescale hostage (a physics error)

The dated pericentre flip was computed with a Lorentzian memory kernel of $\tau = 0.45$ Gyr. The framework's committed covariant kernel gives $\tau_{\rm mem} = 2c/a_0 = 2Z/H_\Lambda =$ **203 Gyr (canonical) / 168 Gyr (alt)**, footing-free ($\tau_{\rm mem} H_\Lambda = 2Z = 11.58$). Against a cluster crossing time of $\sim 1$--$2$ Gyr this is the **deep-adiabatic regime**, in which a sharp sub-orbit pericentre flip **freezes out** -- the same correction already made for the star-orbit dispersion-spread channel. Only the un-anchored $0.45$ Gyr value made the flip a resolvable transient.

## 3. The corrected statement (two-tier)

**(i) Existence -- theorem-grade, modified-gravity-impossible, sign-independent.** At fixed cluster-centric field, cluster members exhibit a non-zero internal-dispersion spread correlated with infall history. In any instantaneous-EFE gravity (QUMOND/AeST; Milgrom's MG-virial universality) this fixed-field history spread is **exactly zero**, so its existence is modified-gravity-impossible. This claim is unchanged in force.

**(ii) Leading sign -- first-infall pre-pericentre zone only, conditional on $s = -1$.** Among members matched at the same cluster-centric field, **first-infall pre-pericentre members are HOTTER** (larger internal dispersion) than matched long-resident / post-pericentre members; equivalently the dispersion excess decreases monotonically with accumulated loading ($\approx$ time-since-infall). This sign is **structural and timescale-free** -- on a monotonically rising approach the causal memory-felt field is always below the current field, so the member is under-loaded for *any* causal kernel -- and was found robust across the memory-time / kernel-shape / member-depth grid and an independent orbit-distribution scan (0/125 sign flips).

**The dated pericentre sign-flip (pre-pericentre deficit then post-pericentre excess) is retracted.** Post-pericentre and backsplash zones are timescale-hostage and not pre-registrable; the ancient/virialized zone is $\approx 0$.

## 4. Corrected magnitude, falsifier, and decisiveness

At the framework-committed memory the modified-gravity-impossible history spread is **$\sim 0.3$--$1.5\%$ absolute / $\sim 4$--$9.5\%$ relational** (residence-time-limited), reaching the printed $11$--$26\%$ only in the short-memory ($0.45$ Gyr) corner. The instantaneous $\theta(y_{\rm cur})$ boost of $6$--$13\%$ is a **current-configuration** quantity that modified gravity partly shares, not the discriminant.

The published kill-condition is inverted: a significantly **negative** fixed-field sign -- first-infall members **cooler** at $\ge 3\sigma$ -- or a null spread, is the falsifier. With the amplitude reduced to the residence-limited few-percent level and the sharp flip removed, the "$3\sigma \approx 2029$--$2031$" forecast is **not supported**; the corrected observable is **future-instrument-gated** -- a dedicated wide dwarf-IFU cluster survey or ELT/HARMONI ($\sim 2032$), the observable being a fixed-radius, phase-tagged relational statistic $D(\mathrm{zone})$ that differences the shared external-field gradient out as a common mode. A public-data feasibility scout (MultimodalUniverse MaNGA $+$ DESI DR1 membership) returns a NO-GO on the diffuse-carrier count. The existence (modified-gravity $=0$) claim is unaffected by any of this.

## Scope reminder

The signature is modified-inertia-*class*-generic -- it distinguishes any history-dependent inertia from modified gravity, not this framework from Milgrom's linear model (arXiv:2503.07106, which also spreads) -- and does not test $a_0$'s value or the sign $s = -1$ (both postulates; the leading sign rides on $s = -1$). The interpolation kernel remains Milgrom's (Phys. Lett. A 253:273, 1999; ApJ 270:365, 1983; the EFE subsystem boost, Phys. Rev. D 106:064060, 2022). No claim of proof is made for the framework; modified-gravity $=0$ at fixed true field is the sole theorem-grade claim, and it is unchanged. This correction is reported with the same weight as the original claim, per this program's standing practice.
