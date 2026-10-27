# PS1_phase_space_core_cap: RESULT

Frozen criteria: `FROZEN_CRITERIA.md` (748770f505). Script: `ps1_phase_space_cap.py`.

Standing rules:
- κ = ½ FITTED.
- Footings canonical / alt are graded separately and never pooled.
- Cold dark energy, not a particle.
- Not "theory closed". Nothing here says the data favour the framework.

## Verdict: TRADES on both footings (checks 4/5: K2 FAILED, see below)

The posit (central Q ≤ the formation object's **mean** Q) binds in **every** cluster, and in every case it drives the core
all the way to the a₀ floor:
- clusters: 326/326 at both h, all to the floor;
- groups: 189/189 group calls, all to the floor;
- SPARC: 94/175 canonical (86 to the floor) and 68/175 alt (65 to the floor).

Clusters and groups therefore land on X38's all-floor rule. That rule's known pattern returns (the groups' Z +2.48 is X38's
own value).

**Cluster cells:**

| | canonical | alt |
|---|---|---|
| G-IN-Mall, Z (h 0.672 / 0.686) | −2.41 → +1.18 / +0.96 (PASS) | −2.41 → +0.99 / +0.80 (PASS) |
| newly failing, all UNDER | G-MID-T2 (h 0.686), G-MID-T3 +4.3, G-MID-b +3.1, G-OUT-Mall +2.4, G-OUT-M3 +5.4 | G-MID-T3 +3.8, G-MID-b +3.0, G-OUT-Mall +2.1, G-OUT-M3 +4.9 |

**Side lines:**

| | canonical | alt |
|---|---|---|
| groups | Z +2.48, ABOVE LAW (FAIL) | Z +2.29 (FAIL) |
| SPARC line (rms) | PASS (0.0650 → 0.0757) | PASS (0.0657 → 0.0719) |

Σ/Σ_HG (106 KT clusters):
- baseline: median 2.56;
- PS1: 0.44 (canonical) / 0.54 (alt).

The cap overshoots the gas's own core by about 2×, in the opposite direction from the baseline's 2.5×.

## Why: the mean-Q posit is far too strong (F0 map, reported)

Q_core / Q_form at the baseline Σ is 107–252 at every mass from 10¹¹ to 10¹⁵ M☉, on both backgrounds and both footings. That
range includes the a₀-floor halos that fit SPARC. A cold core is about 100–200× denser in phase space than the mean of the
object that formed it. So "never above the formation mean" cannot hold for any halo in the record. The posit is
contradicted by the halos that pass, not only by clusters.

## Reported, not graded: the theorem-strength cap

This is the weaker cap that Liouville actually licenses: Q_core ≤ the progenitor's own **central** Q.
- It binds only in clusters (652/652 cluster-cells, all at an interior root, none at the floor).
- It binds in none of SPARC or the groups. Their lines are unchanged: SPARC 0.0650 / 0.0657, groups Z +1.53.
- G-IN-Mall: Z −1.65 / −1.43 (PASS, both footings).
- The only failing cell is **G-OUT-M3 (UNDER)**, which passed in the baseline (+1.80).

By §3's rule this would be TRADES, but it is not graded and is not credited here. It does select clusters with no regime
switch, which no earlier rule did (cf. X19). It is worth its own frozen lane, with M3 as the stated risk.

Other reported lines:
- **Anisotropy bracket:** σ_r(β = 0.5)/σ_r(iso) at 0.1 r₀ is about 3.1, so Q would be about 30× lower. The cap's binding is
  sensitive to the orbit structure, which the graded isotropic σ₀ fixes by choice.
- **KT-only line:** PQ does not use kT, so the KT cells (G-IN-all, G-OUT-all, KT terciles) above already are the KT-only
  line.
- **Per-bin pred/meas (PS1, h 0.672):** 0.45 → 0.88 canonical, 0.56 → 0.93 alt. These are UNDER in every bin.

## Checks

| check | result |
|---|---|
| **K0** | PASS: with the cap off, the script reproduces X48 ng 48 (G-IN-Mall pred at both h and the SPARC rms, to 1e-9). |
| **K1** | PASS: Plummer −3e-12. |
| **K3** | PASS: the formation side reuses X41 exactly. |
| **K4** | PASS: 0.68 GB. |
| **MUTATE** | K1 fails (−0.50) and the script exits 1, as required. |

**K2 FAILED (implementation, disclosed).** The script tested monotonicity on 0.5 Σ_min … 1.5 η Σ_coll for bare
M200 / R200 halos. That is wider than §4's "solver's bracket" [Σ_a0, η Σ_coll].
- **Where it breaks:** Q_core(Σ) is non-monotonic only where the Burkert is SATURATED (r₀ pinned at r₀_pk, so the mass is
  not matched).
  - At 10¹⁴: Σ < 0.14 kg m⁻², below the floor (0.223).
  - At 10¹⁵: Σ < 0.28, which reaches into the bracket for a bare R200 halo.
- **Why the verdict stands anyway:**
  - The graded runs had **0 saturations**: clusters use R_out = r_ta.
  - The root residuals were ≤ 4.3e-14 over 1325 solves.
  - Every cluster sits ~100× above Q_form even at the floor. No bracket choice changes where the clusters land.
- **No amendment is made.** The run stands with K2 FAIL and exit 1.

## Implementation choices (made before any graded number, not in the criteria text)

- **SPARC baryons in the Jeans potential:** the Υ = 0.50 column of the record's g_bar (the same Υ that sets M200 from
  lg M_b). Below the first point M_b ∝ r³; beyond the last point M_b is held flat.
- **Cluster baryons:** `prep`'s M_b on RM, with M_b ∝ r³ inside RM[0]. **Groups:** Hernquist.
- **INERT's "fraction of 326"** is counted per h cell.
- **Anisotropy:** σ_r for constant β = 0.5 diverges as r → 0, so the bracket is evaluated at r = 0.1 r₀.
