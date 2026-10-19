# FSP-011 navigation note (live files deliberately not edited)

FSP-011 was produced under an instruction to add new files only. The live navigation files (README.md, STATUS.md, HANDOFF.md, HISTORY.md, CHECKPOINT.json, ARTIFACTS.sha256) therefore still describe FSP-010. When the coordinator next updates them, the programme's convention applies: snapshot the six files under checkpoints/FSP-010_navigation/ first, then apply the changes below.

## Proposed STATUS.md line

**FSP-011 assessed partial**, 2026-10-19. The proton side of the stuck step reduces to one isoscalar observable, N0(mu0): M_u^p = Born^(0) + (1/2) M_u^(p-n) + N0. Born^(0) is computed from published form factors, M_u^(p-n) is published, and N0 is absent. Original goal: **open**. Full M_u^p, A_rho, R(alpha), finite-alpha dependence and alpha: **not calculated**.

## Proposed HANDOFF.md replacement for "Full proton response"

The proton requirement is now the single functional N0(mu0) of [qcd_full_proton/DERIVATION.md](../qcd_full_proton/DERIVATION.md) eq. (5): the isoscalar, Born-subtracted Cottingham integral of the u,d,s two-current tensor, with contraction classes X, Y, W, Z and V and local matching. Acquisition requirements are in [REMAINING_OBSERVABLE.md](../qcd_full_proton/REMAINING_OBSERVABLE.md).

* Isovector data cannot replace N0 (an exact isospin argument).
* Charm classes reduce to local matching plus power corrections.
* The higher gluon Wilson order reaches R_u only through light and strange mass derivatives.

Do not add Born^(0) + (1/2) M_u^(p-n) (5.0-5.9 MeV per e^2) or the 0.814 local anchor as if N0 were known. Items 2 (smooth-sphere vacuum) and 3 (joint ratio and selection) are unchanged.

## Proposed HISTORY.md entry

- **FSP-011 — full proton response, data inventory and remaining isoscalar observable, 2026-10-19 America/New_York.** [Checkpoint](checkpoints/FSP-011.md), package qcd_full_proton/. Exact isospin split; all-Q^2 Born from published form factors; published isovector totals; charm reduction; independent re-derivation by a separate method. The missing isoscalar non-Born functional N0 and its acquisition requirements are specified. Original goal open.

## Inventory

The package has its own [ARTIFACTS.sha256](../qcd_full_proton/ARTIFACTS.sha256). The programme-level ARTIFACTS.sha256 and CHECKPOINT.json were not regenerated. The FSP-010 inventory (1737 entries, file SHA-256 d68ad674351192fec80af6cf62b96c8ee5d7d16c9e3e079aff23b8589c0c8745) was verified unchanged before FSP-011 began.

## Git location

The FSP-010 programme files are committed on branch codex/fine-structure-claude-handoff (6ce8eec12) and are untracked on main. The FSP-011 commit on main contains only the new FSP-011 files. Relative links resolve in the shared working tree, and on main once the handoff branch content is merged.
