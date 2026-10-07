# Session 3 calcs: results (2026-10-06)

Criteria: `FROZEN_CRITERIA.md`. T, B and B2 were each frozen before their scripts ran. κ = ½ fitted; both footings. No dark-matter particle; the cold mass is still required. Promoted into committed lane CFG440 (scripts and outputs byte-identical to the exploratory run).

| test | script | verdict | key numbers |
|---|---|---|---|
| T: are the UFD offsets tidal? (pericentres in the law's own MW, 300 MC draws each) | `tidal_ufd.py` | **NOT TIDAL** (both footings; pericentre and current D) | ρ(offset, log τ) = −0.16 (p 0.40); the tidally SAFEST half sits at +0.36 dex. Eridanus II (peri 348 kpc) +0.36, Pegasus III (206 kpc) +0.25 |
| T controls | | K1, K3 pass; **K2 FAIL as frozen** | K2 assumed the MW is deep-MOND at 50 kpc; it is at y = 0.032, so the law's transition term adds 9%. K2b (added after the run, disclosed) confirms the formula by hand to 1e-9. MUTATE uninformative (main \|ρ\| < 0.3), as the criteria anticipated |
| B: can (Ω_c/Ω_b) × ORIGINAL baryons pay for the missing mass? (lower bound: all cold mass inside r_½) | `supply_ufd.py` | **VIABLE** at the nominal yield | median f_min = 0.10 (16–84%: 0.05–0.48), both footings; yield −0.5: 0.21 (STRAINED); +0.1: 0.05. Carina III has no CFG317 R_ind (data gap). MUTATE detected |
| B2: zero-parameter σ from law + 0.13 × cosmic share of original baryons | `predict_ufd.py` | **NOT SUPPORTED** in the primary case (nominal yield, q = 1) | median −0.048 (the level is fixed: the bare law is +0.35), but scatter 0.204 against the same-sample bare law's 0.193. Shuffling R_ind raises the scatter by 0.024 (MUTATE detected) |

## Disclosure on B2
The frozen threshold compared the scatter to 0.201, the bare law's scatter on all 31 objects. B2 had to exclude Carina III (no R_ind). On the same 30 objects the bare law's scatter is **0.193**, and *every* B2 variant (0.194–0.208) is at or above it. So the rows the script labels "SUPPORTED" (q = 0.5, or yield −0.5) pass only through that sample mismatch. **Read all B2 rows as: level fixed, no added structure.**

## What this settles
- **The ultra-faints' +0.35 dex is not tidal** under the law's own Milky Way at the measured pericentres. Together with CFG259 (binaries) and AUDIT_UFD (Υ, kernel, distance cuts), that leaves extra mass.
- **The working model's supply rule can pay for that mass.** About 10% of the cosmic cold share of each ultra-faint's original baryons (CFG317's leaky box, R_ind ~ 100) is enough, close to the ~0.13 galaxy retention measured independently in ETGs, the MW and spirals. This is a budget consistency that could have failed (f > 1). It did not, except for one data-gap object.
- **It is not evidence.** The per-object R_ind does not predict the scatter any better than the bare law. ΛCDM also has ample mass for UFDs. The result rests on CFG317's yield (median 0.05–0.21 across the bracket) and on the most concentrated cold mass (q = 1).
- **Net:** the ultra-faints move from "a 3.8σ failure of the law" to "the law alone fails; law + galaxy-level retained cold mass is budget-consistent, with no discriminating power". The law-only failure stands as frozen.
