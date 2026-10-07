# Session 3 calcs, FROZEN before any script exists

κ = ½ fitted; both footings. No DM particle; the cold mass is still required. Inputs are on disk only.

## T. Are the ultra-faints' +0.35 dex offsets tidal (non-equilibrium) under the law's own Milky Way?
Motivation: Session 2 found the UFDs follow the law's *shape* with a +0.35 dex level offset. Tidal heating under the framework is unmodelled (AUDIT_UFD row 4). The audit's D_gc cuts used current distance, not pericentre.

**Host potential (the law's own):** MW baryons as a Hernquist sphere, M = 6e10 M☉ (the record's MW baryons), a = 3 kpc (declared); g(r) = ν_exp(g_N/a₀) g_N (= ν_mono in this regime to the precision needed; declared). Φ(r) = −∫_r^{R_max} g dr' with R_max = 3 Mpc (only differences matter).
**Orbits:** astropy Galactocentric defaults (v7.2). Phase space from LVD ra, dec, distance, vlos_systemic, pmra, pmdec. Spherical potential, so r_peri comes from E and L (root of E = Φ(r) + L²/2r²). 300 Monte-Carlo draws of (distance, pm, vlos) within the quoted errors (seed 9); median r_peri. Objects missing pm or vlos are excluded from T and reported.
**Tidal susceptibility, independent of σ_obs:** τ = t_host / g_int with t_host = (g_host(r_p)/r_p)(1 − dln g_host/dln r) · r_½ the radial tidal stretch at pericentre, and g_int = the law's isolated internal acceleration at r_½ = (4/3) R_e from the baryons (AUDIT_UFD estimator, Υ_V = 2). τ uses no velocity dispersion.
**Residual:** the audit's isolated-law offset log(σ_obs/σ_pred) (resolved objects).
**Verdicts (canonical and alt; pericentre is primary, current D reported):**
- TIDES-DRIVEN if Spearman ρ(offset, log τ) > 0 with p < 0.01 **and** the median offset of the low-τ half is within 2 × 0.086 dex of zero.
- NOT TIDAL if the low-τ half's median offset exceeds 3 × 0.086 dex (tidally safe objects still sit high), whatever ρ is.
- INCONCLUSIVE otherwise.
**Controls:** K1 astropy round trip: the Sun's Galactocentric radius reproduces the default R₀ to 1e-6. K2 the host g at 50 kpc equals the Hernquist deep-MOND √(G M a₀)/(r + a) to 3% (canonical). [Amended before any script was written: the first text used /r, which a Hernquist sphere misses by 6% at 50 kpc for geometric reasons alone.] K3 for a circular test orbit, r_peri = r_apo = r to 1e-4.
**MUTATE (`--mutate`):** the offsets are shuffled among objects (seed 13). The script exits 1 when the mutated |ρ| < 0.3, i.e. when the shuffle is detected as destroying any real correlation. If the main ρ is itself < 0.3, the MUTATE check is uninformative, and that is reported.

### Result of T (main run): NOT TIDAL on both footings, pericentre and current distance. K2 failed as frozen (mis-specified: the MW at 50 kpc has y = 0.032, not deep); K2b, added after the run and disclosed, confirms the host formula by hand to 1e-9. MUTATE is uninformative (main |ρ| = 0.16 < 0.3), as the criteria anticipated.

---
## ADDENDUM B (frozen before any B number exists): can the cosmic cold share of the ORIGINAL baryons pay for the UFDs' missing mass?
The working model's supply rule: the cold fluid available to a system is set by its catchment, i.e. (Ω_c/Ω_b) × its original baryons. The law's phantom comes from today's baryons. Reading: M_dyn(<r_½) = M_law(<r_½) + M_cold(<r_½).
- M_dyn(<r_½) = 3 σ² r_½ / G (the audit estimator's own inversion, r_½ = (4/3) R_e). M_law(<r_½) = g_law r_½² / G (audit estimator, half the baryons inside, Υ_V = 2).
- M_init = R_ind × M_now, CFG317 leaky box (nominal yield −0.2; −0.5 / +0.1 bracket), as AUDIT_UFD §7.
- f_min = (M_dyn − M_law) / ((Ω_c/Ω_b) M_init), Ω_c/Ω_b = 0.1200/0.02237. This assumes ALL the retained cold mass sits inside r_½, so it is a LOWER bound on the retention each UFD needs.
- Measured retention levels elsewhere: galaxy ≈ 0.13, group/cluster ≈ 0.6 (cm08).
- Verdicts (resolved UFDs, canonical and alt, nominal yield): VIABLE if the median f_min ≤ 0.13; STRAINED if 0.13 < median ≤ 0.6; EXCLUDED if median > 1 (needs more than the full cosmic share, even with all of it inside r_½); otherwise OVER-CLUSTER (0.6–1).
- Also reported: the fraction of objects with f_min > 1, and the same at the yield bracket.
- MUTATE (`--mutate`): M_law = 0 (drop the law's phantom). The median f_min must rise; the script exits 1 when it does.

### Result of B (main run): VIABLE at the nominal yield (median f_min 0.10, both footings); STRAINED at yield −0.5 (0.21); VIABLE at +0.1 (0.05). Carina III has no CFG317 R_ind (defaulted to 1, f_min 65.7: a data gap, not physics). MUTATE detected (exit 1).

---
## ADDENDUM B2 (frozen before any B2 number exists): zero-parameter prediction with the galaxy retention level
σ_pred² = G [M_law(<r_½) + q · f_gal · (Ω_c/Ω_b) · R_ind · M_now] / (3 r_½), with f_gal = 0.13 (cm08's galaxy level, measured on other populations; NOT fitted here) and q = 1 (all retained cold mass inside r_½; declared, the most concentrated case).
- Objects with no CFG317 R_ind (Carina III) are excluded and named.
- Statistic: resolved offsets log(σ_obs/σ_pred); median and scatter.
- SUPPORTED if |median| < 2 × 0.086 dex **and** the scatter is below the bare law's 0.201 dex, on both footings at the nominal yield.
- NOT SUPPORTED if the scatter is ≥ 0.201 (no structure beyond a level shift) or |median| > 3 × 0.086. Otherwise PARTIAL.
- Control: a level-only comparator. The bare law shifted by its own median offset gives the scatter a pure level fix would give (0.201 by construction); B2 must beat it to claim structure.
- Reported: yields −0.5 / +0.1, and q = 0.5.
- MUTATE (`--mutate`): R_ind shuffled among objects (seed 17). If the per-object R_ind carries real information, the scatter must rise; the script exits 1 when it rises by > 0.01 dex.
