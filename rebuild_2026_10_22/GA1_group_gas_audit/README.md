# GA1_group_gas_audit: auditing the bright groups' hot gas does NOT help; the negative sign survives and grows

**Criteria and history:**
- Criteria: `FROZEN_CRITERIA.md` (5afacf2b5c, committed alone, before any script or regraded number).
- Amendment A1 (398263fbc7): post-result, code order only. It changes Step 0's random-number order to HG2's and was
  committed alone before the rerun. The first run, `run1.log`, is kept.
- Graded run: `run2.log` / `ga1_group_gas_audit.out`.
- Machinery: HO1's committed script (91cc5c3bd4), executed read-only.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating w ≈ 0 field component, not matter and not a
particle. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen, PRIMARY): **GAS AUDIT DOES NOT HELP** (canonical and alt)

| run | BRIGHT (in shared σ bins) | measured D [95 %] | D_pred, base picture (canonical / alt) | D_pred, all on the law | class |
|---|---|---|---|---|---|
| Step 0 (no audit) | 14 (11) | −0.294 [−0.511, −0.076] | +0.229 / +0.201 | +0.137 | gap 0.523 |
| V-a: duplicates resolved, eRASS1 gas | 12 (9) | −0.268 [−0.536, −0.037] | +0.235 / +0.210 | +0.158 | DOES NOT HELP |
| **PRIMARY: (a) + Lovisari gas** | 12 (8) | **−0.362 [−0.605, −0.139]** | **+0.306 / +0.282** | +0.173 | **DOES NOT HELP** (gap 0.668) |
| V-b: PRIMARY minus kT–σ mismatches | 8 (6) | −0.287 [−0.594, −0.059] | +0.291 / +0.270 | +0.160 | DOES NOT HELP |
| V-σ+ / V-σ− (±1σ Lovisari scatter) | 12 | −0.401 / −0.312 | +0.322 / +0.313 (canonical) | +0.17 / +0.19 | DOES NOT HELP |

The power on the audited samples is 0.28–0.37, below HG2's 0.50 bar. That bar was not part of GA1's frozen class rule,
which tests only the minimum of 6 BRIGHT groups in shared bins. It is reported here.

## The audit itself (PRIMARY)

**Lovisari+2015 fits (20 XMM groups, h70):**
- log Mgas500 = 12.244 + 1.693 log kT, rms 0.10 dex;
- log R500 = −0.353 + 0.548 log kT, rms 0.02 dex.

**Profile check:** the β-model puts 0.334 of the R500 gas inside 0.45 R500. Lovisari's median Mgas2500/Mgas500 is 0.281.
The profile is close.

**Comparing eRASS1 with the Lovisari relation (ratio eRASS1 / audited):**
- Spread: 0.05 to 1.90.
- **The eRASS1 gas is not mostly too high.** It is too *low* for 7 of 12 groups, by up to 20×:
  - J1000−1938: 0.05;
  - J2009−4822: 0.09.
- Too high by 1.5–1.9× for 4 groups, including the two the record flagged: gas-to-star ratios of 14 and 10 come down
  to 9 and 5.
- About right for one.

**Bad matches.** 4 of 12 groups are kT–σ MISMATCHED (β_spec 0.09–3.06), which suggests mis-associations:
- Virgo's σ-794 KT2017 group;
- J1242+0241;
- J1030−3519 (σ 163, kT 1.8);
- J0416−5546 (σ 242, kT 4.1).

**Duplicates.** Two eRASS1 sources were matched to two KT2017 groups each. Rule (a) removed the second match in each case.

## Reading

**HG2's negative sign is not an artefact of over-counted group gas.** With duplicates resolved and the gas taken from a
measured XMM group scaling:
- the measured D moves further negative, to −0.36;
- every halo-free and halo picture moves further positive.

Combined with DS1, no rule g_pred = F(g_bar) on these baryons gives the sign. That includes the law, a halo, and a
displaced halo.

**What remains open:**
- The **dynamical** side of HG2: g_obs = 3σ²/r from member galaxies at (4/3) R_h.
- The sample's **power**: at most 11 X-ray-bright groups in shared bins.

Four of the 12 bright groups have galaxy σ inconsistent with their gas temperature. That points at group membership or
σ, not at the gas. This is stated, not graded.

## Checks: 4/4 (graded run)

- **K0:** Step 0 reproduces HG2 exactly (D −0.2940 [−0.5110, −0.0758], power 0.448) and HO1(b)'s D_pred
  (+0.2293 / +0.2011).
- **K1:** audited gas equals Mgas500,aud × the β fraction to 1e-12.
- **K2:** one eRASS1 source per BRIGHT group.
- **K3:** peak RSS 0.72 GB, one thread.
- **Rerun:** the results JSON is byte-identical (`e4c5f70d…dfaa`).
- **MUTATE twin** (`GA1_MUTATE=1`, rule (a) off): K2 fails, checks 3/4, exit 1.
