# Q3 quantum continuation: exact primary-source gate

Checkpoint FSP-000, Git `3c01aa2861bf576f4c2d942251eb9d2f89cae108`. Checked 2026-10-19 UTC by the delegated archive auditor using `mathbox:literature-check`. No new loop calculation, manuscript edit or status update was made. This file supplements the archive report's explicitly hypothetical logarithmic-potential check.

**Result:** the first quantum step is partly answered by an actual calculation: a supersymmetric matter-sector cancellation, and a brane extension whose stabilization depends on brane data. It does not supply a derived A/B or physical alpha(0).

Primary version authenticated from its first page: C. P. Burgess, L. van Nierop, S. Parameswaran, A. Salvio and M. Williams, [*Accidental SUSY: Enhanced Bulk Supersymmetry from Brane Back-reaction*, arXiv:1210.5405v2](https://arxiv.org/pdf/1210.5405), 28 January 2013. Title, authors and version were checked. The project-local source inventory was searched first; no matching cached primary file was found. No full copyrighted text was retained, so no local PDF hash is claimed.

The following compact extraction stays within the source's scope. **Here beta denotes the paper's conical parameter alpha, not the electromagnetic coupling.**

- **Verified, added-brane model:** two codimension-two sources on a rugby ball, with phenomenological coefficients `T_b,A_b` (Eq. 2.16). Equations (2.21),(2.25) give `2 pi Phi_b=A_b exp(phi)` and `sum Phi_b=N ∓ beta g_B/g_R`.
- **Verified, supersymmetric specialization:** equal localized fluxes obey `Phi_+=Phi_-=±(1-beta)/2` (Eq. 2.44). Sections 4 and 6 find cancellation of the computed hyper/gauge-multiplet one-loop contribution on that background. Higher-spin supergravity loops are not computed; higher-derivative brane terms can break the protection.
- **Verified limitation:** Section 5 tracks the large RG logarithm and explicitly leaves the general finite backreaction insufficiently understood. It supplies no complete finite nonsupersymmetric modulus potential fixing A/B.

Independent algebraic application: choose the plus branch, `N=1`, `g_B=g_R`, and equal constant brane coefficients. Writing `A_sum=A_++A_-`, the two extracted equations imply

`exp(phi*)=2 pi (1-beta)/A_sum`,

provided both sides are positive. Holding beta fixed, replacing `A_sum` by `s A_sum` with s>0 changes `phi*` to `phi*-log s` while preserving the required localized flux. This is a counterfamily across differently chosen brane actions. The BPS relation does not select s. Thus classical stabilization can coexist with a vanishing loop vacuum contribution and still leave a microscopic matching datum free. No arbitrary logarithmic ansatz is needed to expose it.

**Original Q3 versus extension:** the smooth brane-free limit is `beta=1`, `Phi_b=A_b=0`; the flux equation then places no condition on phi. Applying the checked supersymmetric cancellation to that limit excludes a nonzero one-loop lifting coefficient **from the computed matter-multiplet determinants** along the smooth supersymmetric family. It is conditional as a claim about the complete original quantum theory, because the entire supergravity multiplet, UV counterterms and higher orders were not evaluated here. Nor does cancellation of an on-background action establish that every individual kinetic coupling has zero renormalization.

Do not transfer the archive's `alpha_SU2=chat^2/pi^2` unchanged to the rugby-ball brane extension: the geometry/isometries, matter identification and kinetic matching must be recalculated. The next useful task is to supply a microscopic brane action or a different explicit supersymmetry-breaking source that fixes its finite coefficients independently, then check uniqueness, vacuum energy and the physical photon. Another trial value of A/B would add no evidence.

Local audit inputs, SHA-256:

| Input | Hash |
|---|---|
| `real_research/alpha_principle_2026/Q3_salam_sezgin/q1_ss_vacuum_and_flat_direction.py` | `efb891b9ce91311354cd9df2d067ce9baa95fee0f125ee67328fbf992369b0dd` |
| `real_research/alpha_principle_2026/Q3_salam_sezgin/q3_dictionary_and_scoring.py` | `ff65cb80940af75b44bf35b1a0828099ef451e06d85519f2b38a70e257397342` |
| `fine_structure_puzzle/archive_audit/scope_checks.py` | `9f4c5fb1a63d0b661929a2025b33ba182411f041639a25b647c4fcda5756ea2d` |
| `fine_structure_puzzle/archive_audit/REPORT.md` | `0f3c67b7f1e6bbcc8c53da079997677fbeea0334282d053f360e99eece3f752d` |

Acquisition/read commands: `rg --files` over local source/research paths; web searches restricted to arXiv for Salam-Sezgin one-loop stabilization and the paper title; primary `open` at the linked PDF; `find/open` for Eqs. (2.21),(2.25),(2.44), Sections 4-6; `shasum -a 256` for the local inputs. Primary text beyond the relevant setup, cancellation, backreaction limits and conclusions was not audited line by line. No novelty claim or complete literature search is made.
