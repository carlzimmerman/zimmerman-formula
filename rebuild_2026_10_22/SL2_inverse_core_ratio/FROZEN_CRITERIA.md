# SL2_inverse_core_ratio: FROZEN CRITERIA (committed alone, before any script or number)

**Question (owner's relay, 2026-11-01).** On NR1 PRIMARY's baseline, what r₀_eff / r₀_native = A does each mass scale ask for, and does A = 1 / (1 + q_contract − ε q_diss) with one ε give it?

**Disclosed before the freeze.** Not blind. I have read SL1's GA and sweep logs: NATIVE seed 3's tree clears G1–G3 with A 0.67–0.94 on SPARC, keys at baseline; a constant A = 2 probe gives worst |Z| 2.35 and A = ½ gives 9.08. q_diss medians are about 5,600 (SPARC) and 17 (clusters). The relay's curve (A_req 0.70, 0.80, 0.95–1.00, 1.35, 2.30 at 10¹⁰ to 10¹⁴) is a **prediction, not a measurement**, and is scored here. Its c_f 10.1 to 4 is not this baseline, where c_f is 7.08 at 10¹⁴; it is not used. SL1's regrade is unfinished and unread.

**Expectation on record, mine.** One ε fails: ε set by clusters is far too large for galaxies, since q_diss falls about 300-fold from SPARC to clusters. Clusters may also have no single A clearing every key, since A = 2 still has |Z| 2.35.

## Part 1, inversion (constant A per scale, no tree)
- **SPARC, by ET1's six bins, 123 galaxies, background A, then B.** (a) A_Υ: per galaxy, the A minimising ET1's mse at Υ fixed at 0.55 and at 0.60; bin median and bootstrap 95 %. (b) A_S: per galaxy, A whose S_eff equals the ET1 interval's ends and median, at that bin's median halo. Grid 0.05–20, log, 241 points.
- **LITTLE THINGS:** A such that median E = 0, and the range |E| ≤ 0.05, constant A over all 20.
- **63 groups:** range of A with |Z| ≤ 1.5, verdict as `grade_groups`.
- **Clusters, exact `dvecN`, both h:** for constant A on 0.5–5, 19 points: range clearing all 15 keys, and range clearing each of G-IN-Mall, G-IN-all, G-MID-T3, G-OUT-M3. Also the three mass terciles' own stacks reported, using surrogate.
- **X-COP:** range with rms ≤ 0.10 and |mean| ≤ 0.05. Bracket, hydrostatic.

Reads: **MONOTONIC** if medians rise with mass within errors from 10¹⁰ to 10¹⁴; **CROSSES AT 10¹²** if A = 1 lies inside the interval of a bin with lg M₂₀₀ in 11.75–12.25 and not in bins further than 0.75 dex from it. **NO CLUSTER A** if no constant A clears 15 keys. Relay's curve scored per scale: HIT if its value lies inside my interval.

## Part 2, the virial law
A = 1 / (1 + q_contract − ε q_diss). Denominator ≤ 0 is unbound, so rejected.
- q_contract = E_contract / |W_core0|. E_contract is CN1's: virial energy between the halo before and after X39's Blumenthal contraction, Υ 0.50, recomputed on NR1 PRIMARY's halos for all SPARC galaxies, not read from `cn1_energy.json`, which used another η. **W is over the whole halo in E_contract and over the core in W_core0; the relay's equation uses one W. Both normalisations are reported: W_core0 primary, the halo's own W as alternate.**
- Clusters and groups: q_contract 0, as the relay states. **BY HAND.** LITTLE THINGS has no profile: q_contract interpolated from SPARC on lg M_b, **BY HAND**.
- **ε is FITTED**: one number, scanned log 10⁻⁶–1, 121 points, per normalisation. Never reported as derived. A pass here is a one-parameter fit and is labelled so.
- q_diss as SL1: E_SN + E_BH at coupling 1.

**ε_req**: (1 + q_contract − 1/A_req) / q_diss by scale. Overlap of all intervals is the direct test.
**Forward grade:** SL1's train gates G1–G4, surrogate, at each ε; lowest gate regraded exact, then holdout, groups, X-COP as SL1.

Labels: **LAW HOLDS AT ONE FITTED ε** if L_gate 0 on train and the gauntlet passes; **FAILS, SCALES DISAGREE** if ε_req intervals have no overlap; otherwise **FAILS, name the gates**. Post-result variants, separate fractions for SN and BH, are a second knob and are reported only, not graded as this law.

## Checks
K1 A = 1 returns SL1's K1–K7 values. K2 q_contract: contraction identity from CN1 (no baryons, no change) to 10⁻⁶; R-free Υ at full contraction on the frozen table within 0.02 of CN1's direction (Υ falls). K3 planted: synthetic SPARC at constant A = 0.8 returns 0.8 within a grid step. MUTATE: M_b × 2 moves q_contract; q_diss × 0.1 moves ε_req by × 10.

Inherits NR1's ANCHOR-DEPENDENT low masses, since NR2 hasn't landed. One thread, nice 15. κ = ½ FITTED; footings never pooled; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework.
