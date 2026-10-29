# GX1_infall_shape_measured_budget: the derived infall shape fixes X-COP *or* the lensing outskirts, not both

Criteria: `FROZEN_CRITERIA.md` (254f01d34a, committed alone, before any script or number); no amendment.

**Machinery:**
- Stage A: HO1's X-COP harness. Stage B: GS1's lensing harness (R4, native, measured slope 2.777).
- Both are executed read-only, with only the halo's cumulative profile swapped (Burkert → GC3's infall profile).

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen, PRIMARY = infall with its edge at r_ta): **FAILS BOTH** (canonical and alt)

| halo (GS1 measured-gas budget) | X-COP (Stage A): mean / rms; Δ at 0.1 → 0.7 R500 | lensing (Stage B, 15 keys) |
|---|---|---|
| Burkert, edge r_ta (Step 0 = HO1 / GS1 R4) | −0.002 / 0.126: +0.19 → −0.12, **FAIL** (cores light) | **all pass** |
| **infall, edge r_ta (PRIMARY)** | +0.114 / 0.142: +0.02 → +0.16, **FAIL** (outskirts light) | **FAIL**: MID-T2, MID-T3, OUT-Mall, OUT-M3 (UNDER) |
| infall, edge 0.364 r_ta (splashback; reported variant) | −0.035 / 0.079: +0.02 → −0.08, **PASS** | **FAIL**: OUT-all, OUT-T2, OUT-Mall, OUT-M2, OUT-M3 (OVER) |

The alt footing gives the same classes.

## Reading

- **The infall shape fixes the X-COP cores** in both variants: the 0.1 R500 miss goes from +0.19 to +0.02.
- **The splashback-truncated infall halo passes X-COP outright**, at every radius within 0.08 dex. But it puts too much
  mass inside 0.5–3 Mpc for the eRASS1 × KiDS lensing outskirts.
- Spreading the same budget to r_ta fixes the lensing direction but leaves both X-COP's outer points and lensing's MID
  band short.

**So the two cluster data sets pull this halo family in opposite directions:**
- X-COP's hydrostatic profiles, individual massive clusters inside 0.7 R500, want the mass concentrated;
- the eRASS1 × KiDS stacked lensing, lower-mass clusters out to 3 Mpc, wants it extended.

A single profile from this family cannot do both. **The cluster halo shape stays an open failure**, now localised to
this X-COP-versus-lensing tension. Next diagnostic: are the two samples comparable in mass and in definition (R500 from
hydrostatic masses versus lensing apertures)?

## Checks

**Stage A: 4/4.**
- K0 reproduces HO1(a).
- K1: the budget root holds to 1e-8, with 0 saturated.
- K2: peak RSS 0.67 GB.
- K3: q = 2.25.
- Rerun byte-identical.
- MUTATE (q = 3): K3 fails, exit 1.

**Stage B: 2/2.**
- K0 reproduces GS1 R4: all 15 keys pass on both footings.
- K3.
- Rerun byte-identical.
- **Disclosed:** the first Stage B run crashed only when writing its `.out` file, after the results JSON was saved. The
  write was removed (the graded lines are in the run log and `gx1_stage_b.out`), and no number changed.
- No separate Stage B MUTATE twin was run. Stage A's twin covers the shared halo code (the same q path).
