# Cluster-residual closure calculation — what closes it on the framework's footing (2026-06-19)

*9-agent both-ways workflow (target -> matter route -> MI-dynamic route -> galaxy veto -> confront ->
synthesis); all four legs reproduced + adversarially verified. Code in cluster_closure/. Quarantine held.*

**HEADLINE: on the cluster CLOSURE the framework adds NOTHING distinctive over generic MOND, and its
own modified-inertia supplies NEGLIGIBLE residual.** The only galaxy-veto-surviving closure is a
Tremaine-Gunn-protected eV-keV collisionless fermion (sterile-nu-like) on cluster galaxies -- a PARTIAL,
RELOCATING patch (a separate undetected ~0.25-Omega dark species, so "no dark matter" is forfeited at
clusters; still needs a BCG stellar residual; simplest 11-eV/active versions squeezed by DESI/KATRIN/N_eff).
Verified kills (both ways, no manufactured cure, no reflexive dismissal):
 - MI non-adiabatic MEAN-mass boost: the 17.5x local-mu Jensen gain is a PHYSICALLY-VOID apocenter
   a->0 singularity; the honest Milgrom-2022 A(omega) functional gives cycle-averaged boost <= quasi-static
   (0.05-0.67 <1); deep-MOND scale invariance pins M*G*a0=eta*sigma^4 with eta~1 SHARED by MI and MG.
 - dS-Unruh environmental term: wrong-signed (hot core a>>a0 -> MORE Newtonian -> LESS MOND).
 - density-a0 flattening: the ONLY zero-param mechanism that flattens cluster eta(r) (1.55-7.66 -> 0.75-1.30)
   but VERIFIED to BREAK galaxies -- 222-406x a0-boost on SPARC disks, RAR scatter 0.145 -> 0.379 dex (2.6x
   floor); no smoothing length threads cluster-ON/galaxy-OFF. The 40-year MOND-cluster graveyard, reproduced.
Framework-distinctive cluster product: ONLY the non-adiabatic relational sigma-SPREAD (~6-13%, MG-impossible)
-- a TEST, not a closure (supplies zero mean mass). Target: eRASS1 (Bulbul+2024, N=9830) median eta=2.333,
central/cored, missing/gas ~6-10, post-XRISM bracket [~1.0 relaxed, ~2.33 WL]; cure needs a0~4-5e-10 (~5x,
out of cosmic-z reach); +12.6% surcharge for a0=9.36e-11. NEXT: inject a keV sterile (clears dSph TG ~390 eV
+ X-ray non-detection) as real mass into galaxy_veto_test.py for a per-galaxy RAR number.

---

# Cluster-residual-closure synthesis (Zimmerman framework, 2026-06-19)

All four legs re-run and reproduced independently this session (target_profile.py, tremaine_gunn_matter_route.py, mi_dynamic_route.py, galaxy_veto_test.py — all in `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/cluster_closure/`). Framework footing held throughout: a0=9.36e-11, dS-Unruh nu g_obs=sqrt(gbar²+gbar·a0), Ups~0.70 (the eta-WORST footing per the MEMORY rule). Quarantine held (a0/Z never asserted derived). Both-ways applied to every "closes" and every "fails" claim.

## (1) THE TARGET — what any closure must pay
Source: `TARGET_PROFILE_RESULT_2026-06-19.md`, anchored to real eRASS1 (`real_research/data/erass1cl_primary_v3.2.fits`, Bulbul+2024, N=9830).

- **eta(R) is CENTRAL, dies outward.** Rich cluster (M500=1e15): eta ~9.4 at 0.10 R500 (140 kpc) -> 2.33 at R500 -> 1.9 at 1.3 R500. Group (1e14): 13.9 -> 2.33 -> 1.83. Monotone-decreasing, validated vs the banked SHAPE_RECONCILED table within ~10-15%.
- **eta vs M500 is FLAT-to-slightly-rising on real data** (2.29 group -> 2.42 rich; Spearman p=2.6e-10), median over 9830 = **2.333** (5-95%: 2.00-4.43; intrinsic ~0.04 dex), gbar/a0=0.037 (deep-MOND). eta does NOT shrink where baryons are most complete -> genuinely NOT a missing-baryon-at-R500 artifact.
- **Post-XRISM true eta(R500) bracket = [~1.0 relaxed/HSE-reliable, ~2.33 WL]**; best equilibrium ~1.0-1.6. XRISM A2029 (non-thermal P <=2%, HSE bias ~2%) does NOT deflate via turbulence — it removes the "HSE-biased-low" escape and pulls equilibrium eta DOWN; the outer 2x is WL/disequilibrium-inflated.
- **Implied missing-mass M_res(<R):** CORE target ~**2.3e14 Msun** (rich, <420 kpc) / ~**2.3e13 Msun** (group, <214 kpc); M_res(<R500)=4.8e14 / 3.2e13; dies to ~0 by 1.3 R500; cored, gas-tracking, ~400-450 kpc cutoff scaling as sqrt(M500); missing/gas ~6-10 (matches Famaey 2025 CLASH ~10). This is a MOND-SOURCE phantom (re-run through the same interpolation), correctly the right target for a MOND-internal matter closure.
- Robust to cosmic-density a0(z): z=0.296 moves it <1%; curing needs a0~4-5e-10 (~5x, out of z-reach). The +12.6% eta-worst surcharge for a0=9.36e-11 vs canonical 1.2e-10 is real and correctly labeled as the HARDER target (not manufactured).

## (2) THE MATTER ROUTE — sterile-nu / cold baryons (Tremaine-Gunn)
Reproduced: AFD-2010 Eq.14 norm (compact 2.16e2·(m/eV)⁴·(sigma/c)³ form matches their 11-eV form to 0.4%).

- **The sigma³ lever IS the whole game.** TG min mass to dominate: rich cluster **4.3 eV**, group 6.6 eV, L* spiral **69 eV**, dSph **390 eV**. A 2-11 eV fermion is cluster-ALLOWED and galaxy-FORBIDDEN by 1-2 dex in mass = 4-16 dex in packable density — in EVERY (sigma, r_core) cell of the both-ways sweep. The separation is NOT an r_core artifact.
- **PASSES the galaxy veto automatically** (this is exactly why 40 years of eV-neutrino cluster fixes did NOT spoil rotation curves — phase-space exclusion, not a fudge). On a galaxy it is <1% of disk mass, <10 km/s on the outer RC.
- **PARTIAL closure, with real costs:** (i) AFD-2010 — the 11-eV sterile SATURATES TG at the centre in all 30 systems, so a BCG stellar residual is ALWAYS still required (not a clean fill); (ii) it is a SEPARATE, undetected, ~0.25-Omega dark species — the framework is no longer "no dark matter"; (iii) modern cosmology squeezes it: DESI+CMB Sum m_nu<0.072 eV kills the active-nu version ~80x, KATRIN <0.45 eV rules out Sanders' 2-eV active route, N_eff=3.10±0.17 squeezes a thermalized ~eV sterile.
- **Cold-baryon variant FAILS on BBN:** closing eta~2.33 needs (eta-1)·M_bar ~ 2e14 extra baryons -> cluster f_b 0.157 -> 0.366 (2.3x cosmic) -> violates Omega_b. Closes ~1/3 of the gap at most; consistent with the repo baryon-budget forensic (all-cosmic-baryons ceiling only floors eta at ~1.69).

## (3) THE MI-DYNAMIC ROUTE — does the framework's modified inertia supply ANY residual?
The make-or-break the prior MI work hadn't closed: does the cycle-AVERAGED mean dynamical mass rise (a residual), beyond the known sigma-SPREAD (a test)?

- **(a) Non-adiabatic MEAN mass: NO.** The naive local-mu Jensen "gain" blows up to **17.5x** at ecc=0.99 — but this is PHYSICALLY VOID: it is an apocenter a->0 singularity of the LOCAL interpolation. The honest Milgrom-2022 A(omega) functional (Eq.20) sums |a_hat| over the orbit -> argument >= rms a -> cycle-averaged boost <= quasi-static (the "vs QS" column is 0.05-0.67, i.e. <1 everywhere). DECISIVE: deep-MOND space-time scale invariance (Milgrom Sec IID) pins V⁴/(M·G·a0)=const and M·G·a0=eta·sigma⁴ with eta~1 SHARED by MI and MG; orbit shape is a second-tier O(1) wiggle, not the ~4x clusters need.
- **(b) dS-Unruh T_eff environmental term: NO, and wrong-signed.** (b1) The only way to raise core a0 is the density reading a0_local=(c/2)sqrt(G·rho) — but that IS the already-vetoed density-a0 law; AND in the hot core (b2) the kinematic a² term makes a member MORE Newtonian (a>>a0 -> mu->1 -> boost->1) = LESS MOND, the wrong direction. a0 is set by the (cH_Lambda)² cosmological FLOOR, blind to the cluster.
- **NET: the MI-dynamic route supplies NEGLIGIBLE mean residual.** Its one genuinely distinctive product is the member-internal relational sigma-SPREAD (~6-13%, MG-impossible) — a TEST, not a closure.

## (4) GALAXY VETO — per closure (reproduced)
Baseline framework RAR scatter = **0.1446 dex** (consistent with McGaugh 0.13; scalar-a0 optimum 1.33e-10, the 9.36e-11 penalty is only +0.0015 dex).

| Closure | Galaxy signature | Veto |
|---|---|---|
| eV collisionless residual (sterile-nu) | TG-forbidden from galaxies (m_min 100s eV-keV >> eV); <1% disk mass | **PASSES** |
| density-a0 MI flattening | median a0-boost 222-406x on disks; RAR 0.145 -> **0.379 dex** (2.6x floor, +0.235 dex); robust across Ups, interp, a0, h; no fixed L threads cluster-ON/galaxy-OFF | **BREAKS** |
| MI non-adiabatic theta(y) sigma-spread | omega_ex/omega_in ~0.02-0.10 on disks (deeply adiabatic) -> exactly MOND | **PASSES (null)** |

The density-a0 flattening is the ONLY zero-parameter mechanism that genuinely flattens cluster eta(r) (banked 1.55-7.66 -> 0.75-1.30) — and it dies on the galaxy veto, exactly the 40-year MOND graveyard.

## (5) HONEST VERDICT
- **Cheapest closure on the framework's footing:** a Tremaine-Gunn-protected eV-keV collisionless residual (sterile neutrino or sterile/dark baryon) on cluster galaxies. It is the ONLY candidate that survives the galaxy veto. But it is a PARTIAL, RELOCATING closure: a separate undetected ~0.25-Omega dark species (so "no dark matter" is forfeited at clusters), still needs a BCG stellar residual at the very centre, and the simplest active/11-eV versions are squeezed by DESI/KATRIN/N_eff. It does not derive a0; it bolts consensus dark matter onto MOND.
- **Does the framework add anything DISTINCTIVE over generic MOND? On the cluster CLOSURE, no.** The matter route, the BBN cold-baryon ceiling, the density-a0 break, and the MI scale-invariance pin are all MOND-SHARED. The framework INHERITS MOND's cluster failure and pays a +12.6% surcharge for its lower a0. The one genuinely framework-distinctive cluster product — the non-adiabatic relational sigma-spread — is a TEST (MG-impossible, ~6-13%), not a residual; it supplies zero mean mass.
- **No manufactured cure, no reflexive dismissal.** The density-a0 "cure" is right-signed and zero-parameter but verifiably breaks galaxies (0.38 dex); the MI Jensen 17x is real arithmetic but physically void (apocenter singularity). Both are correctly killed. The matter route is correctly credited as galaxy-safe-but-relocating.
- **Minor caveat (does not flip anything):** mi_dynamic_route.py (b1) prints a0_local ~100-150x using the full enclosed mass inside 0.3-0.5 Mpc, while the verdict text says "few-x" (the local density at the 300-450 kpc residual radius). Loose labeling; the route is vetoed regardless.

## NEXT CONCRETE CALCULATION
Compute the **keV sterile-neutrino residual that survives BOTH the cluster TG floor AND modern cosmology**, as the framework's honest cluster patch: solve for the (m_s, mixing/abundance) that (i) gives Omega ~ the cluster-CDM share clusters need (not the full 0.25), (ii) clears the dSph TG floor (m_min ~390 eV — so a ~keV sterile, not eV) so it is ALSO consistent as galaxy DM yet phase-space-thin enough to leave the SPARC RAR <0.15 dex, and (iii) satisfies X-ray non-detection (no 3.5 keV-type line) + DESI N_eff. Then re-run galaxy_veto_test.py with that keV residual injected as an actual mass component on the SPARC disks to confirm the RAR stays at the 0.145-dex floor — converting the "TG forbids it" argument from an order-of-magnitude bound into a direct per-galaxy scatter number. This pins whether the cheapest surviving closure is eV-cluster-only (needs separate galaxy treatment) or a single keV species doing both.