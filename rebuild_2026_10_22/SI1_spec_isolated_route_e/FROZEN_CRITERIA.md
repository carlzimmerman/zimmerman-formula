# SI1_spec_isolated_route_e: FROZEN CRITERIA (committed alone, before any script or model number)

**Question.** X53, X55, GH2 and X79 find that KiDS isolated lenses prefer the a₀ law to route E by Δχ² of hundreds. X53's own main caveat is isolation leakage: the isolation there is photometric, and leakage adds a ~1/R excess that the law's tail absorbs. P2 built the only spectroscopically isolated sample on disk (GAMA G3C × KiDS-1000). Route E has never been graded on it. On the clean sample, which of the two is closer?

**What is already known to me.** P2's committed data vector and its law model are on record, including A_in 1.83 ± 0.30 and the outer stack falling below the zero-field law. So the data are not blind. Route E's prediction on them has not been computed. The model below is fixed without reference to them, and it has no fitted parameter.

**Data.** P2's own stack, unchanged:
- **S3 (primary):** 2,251 lenses, R_iso 3 Mpc. **S1 (reported):** 10,620 lenses, R_iso 1 Mpc.
- Data vector Δ = L − I (iso-random hole subtraction), 15 bins over 0.03–3 Mpc, 36-patch jackknife, Hartlap factor (36 − p − 2)/35 for p bins.
- The scratch measurement is rebuilt with P2's own script. K1 below requires it to reproduce P2's committed Δ.

**Models, both on P2's lens inventory (M★ LePhare + 0.15, cold gas, hot CGM 0.5 M★ to 100 kpc).** Each is T_own + T_nbr(L) − T_nbr(I), with neighbours treated by the same model as the lens.
- **L(a):** P2's isolated AQUAL, y_e = 0 (committed). **L(b):** P2's catalogue external field, reported.
- **H:** route E, Newtonian. M_h from EM1's M200 relation at log(M★ + M_cold), FC1's core rule (S_cold = max(Σ_a0, f_c η Σ_coll(M/f_c)), commit 061b2e2a1a), smooth core, normalised to M200 at R200 and continued to r_ta as in BL1 (commit c64f9be055), with each centre's own z replaced by the sample's lens-weighted median z. Neighbours: the same halo around each catalogued neighbour, from its baryonic mass through the same relation.
- **H_T (reported):** the same with the halo cut at R200.

## Statistic and frozen grade
Δχ² = χ²(H) − χ²(L(a)), 15 bins, full covariance with Hartlap, each footing separately. D² = (m_H − m_L)ᵀ C⁻¹ (m_H − m_L) is the separation the data can resolve: Δχ² has mean +D² if L is true, −D² if H is true, and σ = 2D in both cases.

- **NOT POWERED:** D < 3.
- **LAW PREFERRED:** D ≥ 3 and Δχ² ≥ 0 and Δχ² lies within 2σ of +D².
- **ROUTE E PREFERRED:** D ≥ 3 and Δχ² ≤ 0 and Δχ² lies within 2σ of −D².
- **NEITHER:** D ≥ 3 and Δχ² lies more than 2σ from both.

Goodness of fit, χ²/15 and its p-value, is reported for every model. A preferred model with a poor fit is labelled so.

The ranges inner (R ≤ 0.31 Mpc) and outer (0.4 < R ≤ 3 Mpc) are reported with the same statistic. S1 gets the same statistic and a separately stated class; it is not the primary.

## Reported, not graded
- Common log M200 shift Δ that minimises χ²(H), with its Δχ² = 1 range, on S3 and S1.
- A_in, A_O1, A_O2 for H with P2's estimator.
- Environment-free check: no neighbour term in either model.
- M★ −0.2 / +0.2 dex.

## Checks (any failure makes the verdict NOT DECIDED)
- **K1:** the rebuilt stack reproduces P2's committed Δ, and P2's law model reproduces its committed m_a (S3, both footings), within 1e-6 in units of σ per bin.
- **K2:** the neighbour-term machinery for a halo: at offset → 0, the offset table equals the centred bin average of the same halo within 1e-3; a uniform sheet of identical halos gives |∫|/∫|·| ≤ 1e-2, as P2's K2.
- **K3:** M_h(R200) = M200 within 1e-8.
- **MUTATE:** halo × 0.5 lowers m_H in every bin and changes χ²(H).

## What this cannot show
- It does not measure leakage in the KiDS photometric sample. A reversal here would show only that the law's preference does not survive spectroscopic isolation at this N.
- The lens sample is small. S3 has 1.2 % of KiDS's lenses, so the absolute Δχ² cannot be compared with X53's; D is the comparison.
- It says nothing about a cause for the halos' mass relation, about the floor, or about the alt footing's SPARC failure (X78).
- If route E is preferred here, that does not show the data favour the framework over ΛCDM. It is a comparison of two members of this record only.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.
