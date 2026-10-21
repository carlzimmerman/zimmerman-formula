# CFG960 AMENDMENT A5 (2026-10-21): "own baryons" = CFG953's census convention (f_ret); the M2-condensed variant becomes secondary

Committed ALONE, at the orchestrator's instruction, before any number of the primary variant defined here exists at any resolution
and before any 1024³ job. It replaces U5 of FROZEN_CRITERIA.md (6fc440225) for the primary jobs. Every other rule, gate line,
statistic and reading is unchanged.

## Why: fidelity to the theory under test

The 1024³ test must test CFG953's SCT-M as written. CFG953 fixes the size of a body's own-baryon source through the engine census:
- its criteria §2 take "CFG947's census for supply, N = M_c/M_b = (1 − f_b)/(f_r f_b), with the engine's f_ret table";
- its README cost 9 reads "The supply N is inherited from the engine census";
- its DERIVATION a3 quotes N = 53.6 → 44.1 → 14.9 → 8.3 at M_b 3e10 → 1e11 → 1e12 → 1e13 M☉.

The criteria (U5) used M2's condensed fraction instead, following the brief's wording "the M2 condensed source, i.e. retained
baryons". At z = 0 that fraction sits at the census floor 0.10 for every resolved mass, so N = 53.7 everywhere (A2's check with
`fcond_of`). That does not match CFG953's convention: it gives clusters about 6× too little own-baryon mass and bodies about 3× too
large.

**Disclosure.** The 128³ preview of the M2-condensed variant had been seen before this choice. It is listed in
FROZEN_CRITERIA_1024.md §0 and in A2:
- canonical 0.959 / 0.881 / 0.628, alt 0.965 / 0.902 / 0.679 (P_grav/P_S0 at k 0.3 / 0.5 / 1, z = 0);
- A2's diagnosis that extended cluster bodies drive it.

The reason for the change is fidelity to CFG953, not that preview. The direction of the change in P(k) at 1024³ was not computed
before this commit.

## What changes

- **Primary (jobs SC1x, SC2x; validation VC, VSC, VSA, VMU).** Each labelled particle carries own retained baryons f_b f_own,i m_p:
  - f_own,i is raised at each census refresh (irreversible max) to the census retained fraction f_ret(M_ta(r_ON,h, Δ_ta)) of the
    partition peak owning the particle's NGP cell;
  - f_ret is the engine's `fret_of`, the same census table and M_ta conversion that M3 uses for its catchments (`_CBX["fret"]`);
  - so the own baryons are exactly the baryons M3 leaves in place, and a fully converted domain has N = (1 − f_b)/(f_b f_ret), as in
    CFG953;
  - floor 0.10 below M_ta 10^12.5 h⁻¹ M☉, rising to 0.90 for clusters; no RMIN.
- **Secondary (registered, reported only, NOT queued; the owner may run it later).** The M2-condensed variant of FROZEN_CRITERIA.md
  U5 (`fcond_of`, floor 0.10), as jobs SC1m (canonical) and SC2m (alt). Its 128³ validation is the earlier record (commit 32ccc6ffe,
  kept in `validation_m2cond/`). It carries no verdict weight.
- **Engine switch.** `CFG960_OWNB = fret` (default, primary) | `cond` (secondary). The run JSON records it; the secondary's output tag
  carries `_ownc`. The scorer wrapper accepts SC1m / SC2m. The runner defines them; `chain960.sh` does not run them.

## Validation of the primary variant (≤ 128³, same jobs, settings and lines as FROZEN_CRITERIA.md §2)

The six 128³ jobs, LAW and SCOREK are rerun with the switched engine under A1's environment. Graded: V-K, V-IC, V-MASS, V-MOM, V-N1
(as frozen; A2's diagnosis stands), V-LAW, V-SCORE, V-MEM and V-MUT. The PREVIEW is reported and labelled NOT A VERDICT.

## Gate (chain960.sh)

`chain960.sh` runs SC1x then SC2x (primary variant). Its gate now also waits while any other python process has RSS > 1 GB, besides
the heavy-job patterns. The free + inactive ≥ 46 GB and free disk ≥ 45 GB rules are unchanged.

The pre-registration update is a separate, dated `FROZEN_CRITERIA_1024_ADDENDUM_A1.md`. FROZEN_CRITERIA_1024.md is not edited.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
