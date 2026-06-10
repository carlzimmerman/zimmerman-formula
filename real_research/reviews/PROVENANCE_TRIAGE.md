# Provenance triage — untracked reviews/ scripts (Prompt 0, 2026-06-10)

*Before new work (WB-F → DW → LR), every untracked file in `reviews/` is identified, verification-status-tagged, and
committed here — never silent-committed, never deleted. All trace to two documented sessions; none is an unidentifiable
or an unverified gamma_th-blind output (those live in `reviews/gamma_th_blind/`, already committed 08d17031). The
conclusions these scripts support were ALREADY banked in CONVENTION_LOCK.md / the doors ledgers BEFORE this commit —
committing the scripts adds provenance, it does not newly "read results into a ledger."*

## Verification-status legend
- **BANKED** — supports a verdict already locked in a ledger; conclusion is conceptual/robust, numerics are the backing.
- **EXPLORATORY** — a steelman/probe run; reasoning preserved, not a load-bearing number.

## June 9 2026 session — DSSYK sign + AeST/BIMOND labels-close (the "close last two labels" run)
Supports the banked **DSSYK = CONTESTED-TERMINAL** and **AeST = LEANING-PINNED** verdicts.
| File | Topic | Status |
|---|---|---|
| `door2_dssyk_deepmond_sign_synthesis.py` | Door-2 DSSYK deep-MOND sign synthesis verdict | BANKED (CONTESTED-TERMINAL) |
| `door2_dssyk_matter_chord_stageAB_verify.py` | matter-chord stage-A/B verification | BANKED |
| `door2_dssyk_perprobe_both_maps.py` | per-probe both-maps (center↔MOND, edge↔anti) | BANKED |
| `door2_dssyk_wE_center_vs_edge_DIRECT.py` | w(E) center-vs-edge, direct | BANKED |
| `dssyk_wE_center_vs_edge_INDEPENDENT.py` | w(E) center-vs-edge, independent re-derivation | BANKED |
| `chord_vacuum_placement_test.py` | θ_vac assumed (dictionary) not derived by chord algebra | BANKED (the load-bearing result) |
| `edge_exponent_check.py` | edge-spectral-exponent check | BANKED |
| `REDERIVE_dssyk_center_edge.py` | independent re-derivation, center/edge | BANKED |
| `steelman_both_ways.py` | both-ways steelman (center/MOND vs edge/anti under N-V vs Okuyama) | BANKED (both-ways) |
| `rahman_susskind_confinement_approachB.py` | R-S confinement as an independent obstruction to the sign | BANKED |
| `dssyk_problem1_STRUCTURED_OUTPUT.json` | structured-output artifact: headline CONTESTED-TERMINAL + honest_caveat + bothways_check | BANKED |
| `door3_bimond_canitdecline.py` | can the AeST/BIMOND 𝒦(𝒬) decline? (both-ways) | BANKED (LEANING-PINNED) |
| `door3_bimond_frw_integrate.py` | BIMOND FRW numerical integration | BANKED |
| `door3_bimond_frw_symbolic.py` | BIMOND FRW symbolic | BANKED |
| `door3_bimond_legendre_pin.py` | Legendre-transform pin of δQ/Q₀ | BANKED |
| `aest_radial_aether_eom.py` | AeST radial aether EOM (Mistele curl-sector grounding) | BANKED |
| `aest_locality_theta_profile.py` | AeST locality / θ-profile | BANKED |

## June 5 2026 session — doors/routes + free-fall-clock + footing
Supports the banked **Z-is-a-data-selected-convention** (coefficient not forced) and the a₀-footing work.
| File | Topic | Status |
|---|---|---|
| `freefall_clock_rigor_audit.py` | free-fall-clock premise: "Z is a data-selected convention, not derived" | BANKED |
| `freefall_clock_orbit_steelman.py` | orbit steelman of the free-fall-clock premise | EXPLORATORY |
| `freefall_clock_unruh_escape_test.py` | Unruh escape test of the premise | EXPLORATORY |
| `aest_cassini_quadrupole_full.py` | AeST Cassini quadrupole (full) | BANKED |
| `aest_quasistatic_cassini.py` | AeST quasi-static Cassini bound | BANKED |
| `cmb_modinertia_oscillator.py` | CMB modified-inertia oscillator | BANKED (superseded by the bath result) |
| `desi_a0z_loop_CLOSED.py` | DESI a₀(z) loop (CLOSED) | BANKED |

## Modified tracked file
| File | Change | Status |
|---|---|---|
| `project14_wide_binaries.py` | swapped hardcoded MOND a₀=1.2e-10 → framework a₀=9.36e-11 (computed from ρ_Λ); external-field printout uses the computed value | SOUND (framework-footing fix; commit) |

**Disposition:** all committed with this catalog as the provenance record. No quarantine, no deletion. The DSSYK/AeST/coefficient
conclusions remain as banked; nothing here is promoted to a new ledger claim.
