# L152 — the running-sound-speed field dust vs the CMB (deciding computation 1 of 4)

Scripts: `L152_running_cs2_cmb_boltzmann.py` (21/21), `L152_running_cs2_pk_lyman_alpha.py` (14/14), patched
CLASS in `L152_class_running_cs2/` (`running_cs2.patch`, `apply_running_cs2_patch.py`, `build_patched_classy.sh`).
Results as JSON: `L152_cmb_results.json`, `L152_pk_results.json`. Outputs: the two `.out` files.

## VERDICT

**The running-c_s² sector (c_s² = c0·a³, the cosh/exp-K leaf-normal k-essence of L139) PASSES the CMB across
the entire L138 window c0 = 1e-6 … 3.21e-6, and it suppresses galaxy-scale power. The CMB is not the
binding test of this sector. The Lyman-α forest is — and there the verdict is UNDETERMINED, forked between a
decisive FAIL and a borderline pass depending on which density field the forest traces.**

| c0 = c_s²(today) | unlensed TT/EE/TE max dev (ℓ=30–2000) | lensed TT / EE | ⟨ΔC_L^φφ/C⟩ L=8–400 | Δχ² (Planck-like, fixed params) | c_s²(a_rec) |
|---|---|---|---|---|---|
| 1e-6 | 1.8e-5 / 1.1e-5 / 1.2e-5 | 1.8e-4 / 2.0e-4 | −0.19% | 0.012 | 7.7e-16 |
| 1.8e-6 | 3.3e-5 / 1.3e-5 / 9.6e-6 | 3.0e-4 / 3.1e-4 | −0.33% | 0.035 | 1.4e-15 |
| 3.21e-6 | 5.9e-5 / 1.2e-5 / 9.4e-6 | 4.5e-4 / 5.1e-4 | −0.55% | 0.095 | 2.5e-15 |

Peak heights 1/2/3 and the ratios 3/1, 3/2 equal the CDM control to < 1e-4 (peak3/peak2 = 0.99144 in both).
The 1% precision band is met by a factor ~100 (primary) and ~20 (lensed). The CMB's own ceiling on the running
sector is c0 ≈ 4e-4 (lensed TT reaches 1%), **127× above the window** — and that ceiling is a lensing bound,
not a recombination bound. **Yes: c_s²(a_rec) = c0·a_rec³ ~ 1e-15 makes the CMB at recombination
indistinguishable from CDM.**

| c0 | σ₈ (total matter) | P/P_CDM at z=0: k=0.1 / 1 / 10 h/Mpc | k₅₀ (50% suppression, z=0) |
|---|---|---|---|
| control | 0.8226 | 1 / 1 / 1 | — |
| 1e-6 | 0.8025 (−2.4%) | 0.990 / 0.320 / 0.013 | 0.79 h/Mpc |
| 1.8e-6 | 0.7880 (−4.2%) | 0.981 / 0.114 / 0.008 | 0.59 h/Mpc |
| 3.21e-6 | 0.7645 (−7.1%) | 0.967 / 0.013 / 0.009 | 0.44 h/Mpc |

Galaxy-scale power is halved at k ≈ 0.4–0.8 h/Mpc today while k = 0.1 h/Mpc survives to 1–3%; at z = 0.5 the
BOSS/DESI range is touched at 0.3% (k=0.1) to 2.6% (k=0.3). σ₈ moves down by 2–7% — not a kill, not a win.

**Lyman-α (the named falsifier), c0 = 1e-6, suppression 1 − P/P_CDM at k = 1 / 2 / 3 / 5 / 8 / 10 h/Mpc:**

| z | total matter | linear baryons | allowed (5.3-keV WDM proxy) |
|---|---|---|---|
| 2 | .022 .086 .186 .439 .791 .923 | .001 .005 .011 .029 .070 .104 | .000 .001 .002 .006 .016 .027 |
| 3 | .007 .029 .064 .167 .378 .529 | .000 .002 .004 .010 .025 .038 | same |
| 4 | .003 .012 .027 .072 .175 .262 | .000 .001 .001 .004 .010 .016 | same |

Over the constraining range k = 8–12 h/Mpc: total-matter reading **23× (z=3), 11× (z=4) over the allowance → FAIL**;
linear-baryon reading **0.63× (z=4, inside), 1.5× (z=3, borderline), 4.3× (z=2, outside but weaker data)**. At the
window's top (3.21e-6) even the baryon reading is 4.5× over at z=3. The fork is physical: once the fluid's
Jeans term switches on its own δ freezes, but baryons keep falling into the frozen (not erased) fluid
potential, so linear δ_b is 14× less suppressed than δ_total at z=3, k=10 h/Mpc. On scales that are mildly
non-linear at z=3 the gas needs the fluid's wells to reach forest overdensities, and a fluid pressure-supported
below ~3 h/Mpc at z=3 does not supply them — so the generous reading is likely optimistic, and it already sits
at the tolerance for the smallest allowed c0. **Deciding computation: a hydrodynamical simulation with a
separate pressure-supported dark fluid, which exists neither for this sector nor for AeST.**

**Constant c_s² (quadratic K) at the same c_s²(today), for contrast:** invisible at recombination (< 3e-4) but
the lensing potential drops 4–10% (L=8–400) and the lensed spectra move 0.4–0.8%; Planck-like Δχ² = 33 at
3.21e-6, of which only 4.6 is TT+TE+EE — **the published 3.21e-6 ceiling is a CMB-lensing bound** (a first
version of that check without the lensing term failed at 4.6; the failure identified the bound's origin). And it
is dead on structure alone: σ₈ −18%, P/P_CDM = 0.004 at k = 1 h/Mpc, k₅₀ = 0.25 h/Mpc.

## What was run, exactly

* CLASS 3.3.4.0 (`classy`) **patched** so the fluid's rest-frame sound speed can run:
  `cs2_fld(a) = min(cs2_fld_max, cs2_fld·(a/cs2_fld_astar)^cs2_fld_p)`, new inputs `cs2_fld_p`, `cs2_fld_astar`,
  `cs2_fld_max` (defaults 0, 1, 1 = stock). Four call sites replaced (fluid ICs ×2, rest-frame→gauge pressure
  transformation, fluid equations of motion) plus the PPF branch for consistency; each replacement asserted to
  occur exactly once. Built into a repo-local, gitignored `site/` by `build_patched_classy.sh`; the system
  classy is untouched. **Regression: with p = 0 the patched code reproduces stock classy to 0.0e+00 on every
  spectrum.** This is a real Boltzmann integration of a GDM fluid with w ≈ 0, c_s²(a), c_vis² = 0 — no
  piecewise stand-in, no growth-ODE substitute.
* Fluid: `w0_fld = −1e-5` (CLASS refuses w ≥ 0; L129 used −1e-4 and that configuration is run as a cross-check —
  hyrec/recfast ratios of the running deviations 1.10 / 0.96 / 1.00), Ω_fld h² = 0.1190 + residual
  ω_cdm = 0.001, `use_ppf = no`, Planck-2018-like otherwise, linear P(k).
* **`recombination = recfast`, for a reason found here:** CLASS's HyRec wrapper computes its own recombination-era
  H(z) from `Omega0_nfsm` (baryons + CDM only, the fluid excluded), so any fluid-as-dust run recombines in the
  wrong Hubble rate (z_rec off by 0.52, TT off by 0.7% against true ΛCDM). With recfast the c_s² = 0 control
  matches a **real ΛCDM run** (real CDM, no fluid) to 2.1e-4 in TT, 5.0e-4 in EE, θ_s to 2.8e-5, and its
  total-matter σ₈ to 0.04%. Differential comparisons (all verdict numbers) are immune either way.
* Every test run is compared with the c_s² = 0 control of the same fluid: identical background by construction
  (100θ_s agrees to 0.0e+00), so peak heights are compared at fixed acoustic scale.
* Total-matter P(k) = CLASS's P(k) × (δ_tot/δ_m)² from the transfer functions (CLASS's own `mPk`/`sigma8` count
  only b+cdm, 16% of the matter here); validated against a true ΛCDM run (σ₈ 0.8226 vs 0.8229; P(k) to 0.1%).
* **Independent validation of the running's time dependence:** a sub-horizon two-fluid growth solver written
  from the equations reproduces the patched CLASS's fluid suppression to 0.003 and the baryon suppression to
  0.001 (absolute, in P/P_CDM) across z = 0–3, k = 0.3–10 h/Mpc, wherever the ratio exceeds 0.3; the same
  solver run with a² or a⁴ instead of a³ disagrees by 0.59 / 0.47, so the test is discriminating.
* Planck-like Δχ²: TT+TE+EE (lensed, ℓ = 30–2000, f_sky 0.7, 7′ beam, 30/60 μK-arcmin) at **fixed** cosmological
  parameters plus a lensing-amplitude term (⟨ΔC_L^φφ/C⟩ over L = 40–400 against 2.5%). No marginalisation ⇒ an
  upper bound on detectability; no σ is quoted from it.
* Lyman-α allowance proxy: 1 − T²_WDM(k) with the Viel et al. 2005 transfer function at m_WDM = 5.3 keV (Iršič
  et al. 2017, 95%), evaluated over k = 8–12 h/Mpc (0.07–0.1 s/km at z = 3–4) where the bound's information
  lives; at k ≤ 3 h/Mpc the proxy "allows" 1e-4–2e-3, below any real forest sensitivity, so a max over all k
  would be an artefact of the proxy.

## Honest scope

1. GDM mapping: w = −1e-5 rather than 0; rest-frame c_s² identified with the dispersion sound speed 2c_Y/K_QQ;
   no shear. Exact sub-horizon, an O((aH/k)²) effective description at horizon crossing — irrelevant here
   because c_s²(a_rec) ~ 1e-15.
2. c_s² ∝ a³ holds while the shift charge is undiluted (Z ≫ 1). If the cosh/exp transition a_t < 1 the late-time
   c_s² saturates at a constant; that case lies between the running and constant scans, neither of which was
   tuned for it.
3. Linear theory throughout part 2; the forest at k ~ 5–10 h/Mpc, z = 3 is mildly non-linear (Δ² ~ 10–30). The
   WDM allowance is a z-independent proxy for a bound from a joint z = 3–5.4 fit, compared redshift by redshift.
4. The window itself (floor c_s² ~ 1e-6 from galaxy smoothness, ceiling 3.21e-6 from the constant-c_s² bound)
   is L138's; it is not re-derived, and the ceiling does not apply to the running case (whose own CMB ceiling
   is 4e-4).
5. Not computed here: the O(w) PPN solve with χ (L139 item iii), the non-linear galaxy-smoothness calculation
   (L139 item ii), and the two-species hydro simulation the Lyman-α verdict needs.

## What decides it next

The Lyman-α forest at z = 2–4, k = 1–12 h/Mpc. The numbers above are the target: a two-species (gas +
pressure-supported dark fluid) hydrodynamical simulation of the flux power spectrum. If the forest follows the
total matter, the sector fails by 10–50×. If it follows the linear gas, c0 = 1e-6 sits at 1.5× the allowance
at z = 3 and inside it at z = 4 — a knife-edge, with the whole window above 1e-6 already outside at z = 3.
Secondary tests that this lane quantified but did not adjudicate: the z = 0.5 full-shape P(k) (0.3–2.6%
suppression at k = 0.1–0.3 h/Mpc) and σ₈ (−2.4% to −7.1%).
