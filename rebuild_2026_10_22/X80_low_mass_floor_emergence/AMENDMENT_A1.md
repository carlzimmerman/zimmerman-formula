# X80 AMENDMENT A1: run before A5 (committed alone, 2026-10-30, before any low-mass zoom exists)

**Owner's decision, 2026-10-30:** "Yes, X80 first." It answers ARGON_BRIEF_2026-10-30_EVENING §9, step 1.

## What changes: the order
`FROZEN_CRITERIA.md` said the runs start only after A5 logs "A5 done". They now start when X74's post-A4 watcher logs "post-A4 regrades done". A5 starts after this lane logs "X80 done". There is still no overlap with A4 or A5, and A5's own amendment (a0cbcc6928) still holds: it runs after A4 and the post-A4 regrades, just later.

**Unchanged:** the 24 runs, X77's fit, the primary R(M), the verdict classes, K1, MUTATE, Argon's smooth-max scoring and the outside prediction in `README.md`.

**Why.**
- X81: A5 keeps ε = 0.01 r_f, so it measures the same cut, and it cannot settle η(10¹²). A5's cost is 5–6 days.
- NF1 (f95621e30a): the collapse branch alone passes SPARC's line. X80's masses are what decide between the floor rule and no floor.

## Added: reported, not graded, frozen here
X80's frozen R(M) uses X77's fit at the ε cut, without the cold share. FC1 and NF1 use the converged-cusp η with f_c. So the frozen R can't be read against NF1 directly. These lines are added beside it. They don't change the frozen verdict.

1. **Converged η.** For each low-mass halo with a fit: η_conv = η(smooth-core fit to an exact NFW at that run's c_nfw, x_c 0.001), X81's and CE1's method unchanged. Median and bootstrap 68 % (10 000 draws, seed 20261030) per mass and grid. **Check:** the same script on the committed 10¹² ng 64 runs reproduces 25.94 within 0.01.
2. **Ratios at ng 64.** ρ₁₀ = η_conv(10¹⁰)/η_conv(10¹²), ρ₁₁ = η_conv(10¹¹)/η_conv(10¹²), with the bootstrap range from independent resampling. The zoom mass is total mass, so these are at M_t, as NF1's rule is.
3. **Reading against NF1's window**, numbers taken from NF1's README before any low-mass number:
   - **N OVER:** ρ₁₀ > 1.9. NF1's line holds only to s ≈ 0.14.
   - **N IN WINDOW:** 1.1 ≤ ρ₁₀ ≤ 1.9.
   - **N SHORT:** ρ₁₀ < 1.1. ET1 and ET2's lower bounds at the two lowest bins want about 1.1–1.2.
   - **[NOISE-LIMITED]** if the bootstrap 68 % of ρ₁₀ spans two of these.
   For the record, NF1's N1 gives ρ₁₀ 1.53, ρ₁₁ 1.24.
4. **Native read of version N.** NF1's grader with f_c η(M_t) Σ_coll(M_t) at every mass, no floor, η below 10¹² from the measured ρ₁₀ and ρ₁₁: interpolated in lg M between 10¹⁰, 10¹¹ and 10¹², flat below 10¹⁰ as X74's `cf_of` is flat outside its table. CE1's A4 table when it exists, otherwise CE1's. Labels: **NATIVE N PASSES THE SPARC LINE** or **NATIVE N FAILS THE SPARC LINE**, from EM1's `line` on both backgrounds. Plus LS1's table by V_flat against ET1. **Check:** ρ₁₀ = ρ₁₁ = 1 reproduces NF1's N0, |d| ≤ 1e-9.

## What this cannot show
Same limits as X80 and NF1: Newtonian dust, no baryons, the core shape imposed, and a pass here is a SPARC statement. Taking a₀ out of the cold sector stays the owner's call whatever these numbers say.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework.
