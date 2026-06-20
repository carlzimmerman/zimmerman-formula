# ROUTE D — Fresh 2024-2026 relativistic-MOND cluster mechanisms: has anyone solved it? — verdict 2026-06-20

**Workflow:** `cluster_hunt2` ROUTE D — WebSearch/WebFetch of the 2024-2026 literature for a genuinely-NEW
cluster-core mechanism not in the banked killed-list, scored against the four gates G1-G4 on the framework's
own footing (a0=9.36e-11), both ways. Scripts in `opus_48_extended_research/reviews/cluster_hunt2/`.

## HEADLINE (both ways)
**NO 2024-2026 paper closes the framework's cluster-CORE soft-spot. The literature offers ONE genuinely-new,
no-new-particle mechanism the banked work missed — the Kroupa-group IGIMF stellar-remnant route (Zhang-Zonoozi-
Kroupa 2026, arXiv:2602.06082) — and it is a REAL partial closure of the INTEGRATED deficit (passes G2 + G3
cleanly) but FAILS G1 on the CORE: it fills only ~17% of the ~1.9e14 M_sun core shortfall and has the WRONG
SHAPE (star-tracking central spike, not the flat gas-tracking ~10 shell FPS observe). The two other new lines
are dead or relocating: the 11-eV MOND-neutrino (νHDM) revival is now KILLED at >5σ by 2026 N-body structure
overproduction AND by MicroBooNE+cosmology lab exclusion; Deffayet-Woodard nonlocal MOND (2026) does not
address clusters at all (inherits standard MOND's cluster failure). Net standing UNCHANGED: the cored residual
stays an honest shared-MOND open soft-spot — but the IGIMF route is a genuine new both-ways CREDIT on the
integrated/equilibrium mass.**

---

## THE FOUR CANDIDATES SCREENED (2024-2026)

### 1. IGIMF stellar remnants — Zhang, Zonoozi & Kroupa 2026 (arXiv:2602.06082, PRD) — THE NEW LEAD
**The genuinely-new no-particle mechanism the banked killed-list does not contain.**
- **Claim:** a top-heavy IGIMF in massive cluster ellipticals (high SFR > 10 M_sun/yr) raises their M/L ~6x
  canonical; the boost is dominated by stellar remnants (neutron stars + stellar black holes). Baryons
  (stars+remnants+ICM) then account for **88%** of the MOND dynamical mass at R200 (vs ~52% canonical).
  46 clusters z<0.1, WINGS+2MASS, a0=1.2e-10.
- **G3 NO-NEW-PARTICLE — PASS (clean).** Neutron stars + stellar BHs are REAL collapsed baryons, not a new
  species. This is exactly the kind of "known physics / real baryons" the gate allows. It is NOT the banked
  cold-baryon route (which failed on BBN by needing 2e14 *extra* baryons → f_b 2.3x cosmic): IGIMF adds NO new
  baryons, it re-weights existing stellar light into a higher M/L, so BBN/Omega_b are untouched.
- **G2 GALAXY-VETO — PASS (clean, by construction).** The IGIMF is top-heavy ONLY in high-SFR massive
  ellipticals; SPARC disks keep ~canonical IMF, so their M/L and the RAR are UNCHANGED. This is the opposite of
  the density-a0 killer (which boosted a0 222-406x on SPARC and blew RAR scatter 0.145→0.379 dex). The remnant
  mass is galaxy-internal stellar mass, phase-space-irrelevant on disks.
- **G1 SUFFICIENCY — FAILS on the CORE (the make-or-break), PARTIAL on the integrated mass.**
  - *Mass budget:* granting the FULL extra IGIMF mass (~6.5e13 M_sun for a rich cluster), the fraction that
    lands inside the 420 kpc core (stars track BCG+ICL+satellites) is ~50%, i.e. ~3.3e13 M_sun — only **~17%
    of the ~1.9e14 M_sun core shortfall** (target 2.3e14 minus the framework MI phantom 4.0e13).
  - *SHAPE mismatch (decisive):* FPS 2025 find the residual is GAS-TRACKING with a FLAT missing-to-gas ratio
    ~10 out to a ~400 kpc cutoff. Remnants are STAR-tracking → a residual/gas ratio that RISES toward the
    center (13.4 at 100 kpc → 3.0 at 420 kpc), a central spike, NOT the observed flat cored shell. Even with
    enough mass the geometry is wrong.
  - *a0 surcharge:* the framework's a0=9.36e-11 makes the deep-MOND residual ~1.28x harder than Kroupa's
    a0=1.2e-10, so the 88% is OPTIMISTIC for the framework (covers ~69% on equal accounting).
- **G4 DATA — PARTIAL.** Kroupa's 88% is the INTEGRATED R200 (HSE-equivalent) mass; the framework's soft-spot
  is the lensing CORE (FPS, ~420 kpc, ratio ~10) — a different, Kroupa-untested regime. On REAL eRASS1 the
  IGIMF 6x boost raises the integrated baryon fraction by a robust relative ~1.4-1.7x on any footing (my raw
  eRASS1 +40%, Kroupa +69%), so it GENUINELY helps the integrated/equilibrium mass — exactly the post-XRISM
  bracket [~1.0 HSE-reliable, ~2.33 WL] where the framework's η also deflates. At the HSE-reliable end
  (η~1.0-1.6) the IGIMF baryons can largely close the EQUILIBRIUM problem.
- **NET (both ways):** a REAL new partial closure — it passes the two gates that kill most candidates (G2, G3)
  and substantially closes the INTEGRATED/equilibrium deficit, which is a genuine both-ways credit the banked
  work did not have. But it does NOT close the framework's specific CORE soft-spot (wrong shape + only ~17% of
  the mass budget there), so it is **PARTIAL, not a closure of the open soft-spot.** Both arms quantified in
  `igimf_remnant_core_test.py` and `igimf_integrated_erass1.py`.

### 2. 11-eV MOND-neutrino (νHDM) revival — KILLED HARDER than banked (2025-2026)
- The Angus-2009 11-eV sterile neutrino MOND cluster patch was revived 2025-2026 (arXiv:2506.19196 νHDM
  initial conditions; arXiv:2602.21975 νHDM N-body on Gpc scales).
- **G3 — FAILS (new particle).** An 11-eV sterile is a new BSM species → relocates the dark sector, forfeits
  "no dark matter," exactly the banked keV/eV verdict.
- **NEW KILL (2026):** arXiv:2602.21975 N-body finds νHDM **massively overproduces** large-scale structure
  (most massive cluster ≈5e17 M_sun/h) and high peculiar velocities **rule out νHDM at >5σ** — "replacing CDM
  with HDM is unlikely to be viable regardless of the gravity law." Independently, MicroBooNE 2025 excludes the
  eV sterile (2-3σ over MiniBooNE region) and a thermalized sterile is cosmologically constrained to
  m_s ≲ 0.5 eV. So the 11-eV route is now dead from BOTH ends (structure overproduction AND lab/cosmology),
  not merely "relocating." The banked keV-squeeze conclusion is strengthened, not weakened.

### 3. Deffayet-Woodard nonlocal metric MOND — arXiv:2512.10513 (JCAP 04(2026)081) — does not address clusters
- A genuinely-new (Dec 2025) covariant nonlocal MOND that interpolates cosmology↔bound systems via a nonlocal
  vector field built from a scalar gradient; reproduces the cosmological DM successes (CMB/BAO/structure)
  WITHOUT a particle (emergent/nonlocal, the model's own field). Flagged in the banked Bridge Scout as "a
  structural rival fork to watch."
- **Verdict:** the paper does NOT mention galaxy clusters or the cluster missing-mass problem at all; in bound
  systems it reduces to standard MOND, so it INHERITS the same cluster-core failure. Not a cluster closure —
  a cosmology-side rival theory, not a core mechanism.

### 4. Superfluid DM (Berezhiani-Khoury) + dipolar DM (Blanchet) — particles, G3 fails
- 2025 superfluid-DM review (arXiv:2505.23900): clusters explained by DM in the NORMAL/thermal (non-superfluid)
  phase — i.e. a real axion-like ~eV particle providing cluster mass galaxies lack. **G3 FAILS** (new particle).
- Blanchet dipolar DM (gravitational polarization): a new dark FLUID, indistinguishable from ΛCDM at cosmo
  scales. **G3 FAILS** (new dark species). Neither is the framework's own field; both relocate the sector.

### What FPS themselves propose (the route's literal question) — they leave it OPEN
FPS 2410.02612 (PRD 111, 123042, 2025) do NOT propose a closure. Their Discussion lists candidates and rejects/
defers each: (a) eV sterile neutrinos "considerable overproduction of massive clusters" (now the >5σ 2026 kill);
(b) "additional baryonic mass in collisionless form, e.g. cold gas clouds in a multiphase IGM" (a no-particle
baryon route, but unquantified — adjacent to but distinct from IGIMF); (c) "relativistic MOND formulations most
often imply additional fields... whether such fields could also explain away the residual... is an open
question," noting preliminary studies give "mass-dependent enhancement followed by an oscillation at large
radii, quite different from the MOND non-relativistic limit" (= the banked AeST μ²Φ outskirts term, Durakovic-
Skordis 2312.00889, which makes the core WORSE — no escape). FPS deliver a precise fit-TARGET, not a closure.

---

## THE FOUR GATES — final scoring of the best new candidate (IGIMF remnants)
| Gate | IGIMF stellar-remnant route (Kroupa 2026) |
|---|---|
| G1 SUFFICIENCY (close ~4.4-5.8x core undershoot / ~2.3e14 core target) | **FAILS on the core** (~17% of mass budget there, wrong gas-tracking shape); PARTIAL on integrated/equilibrium mass |
| G2 GALAXY-VETO (RAR < 0.13 dex) | **PASS** — IGIMF top-heavy only in high-SFR ellipticals; SPARC disks canonical, RAR untouched |
| G3 NO-NEW-PARTICLE | **PASS** — neutron stars + stellar BHs are real baryons, no new species, BBN-safe (re-weighting not new baryons) |
| G4 DATA (eRASS1/CLASH/XRISM/Lyα/X-ray) | **PARTIAL** — closes integrated R200 (Kroupa) + real-eRASS1 +40% on framework footing; the lensing CORE is a different untested regime |

## HONEST VERDICT (both ways)
- **CREDIT at full weight:** the IGIMF stellar-remnant route is a GENUINELY-NEW (Feb 2026), no-new-particle,
  galaxy-safe mechanism the banked killed-list did not contain. It passes the two gates (G2, G3) that kill most
  cluster fixes, and it substantially closes the INTEGRATED/equilibrium deficit — the post-XRISM bracket where
  the framework's own η deflates toward ~1. For the framework's "no dark matter" thesis this is the best
  available cluster help: it shrinks the integrated problem using only real stellar remnants. That is a real
  both-ways gain over the banked "shared open gap with no no-particle help."
- **CONCEDE at full weight:** it does NOT close the framework's specific open soft-spot, the CORED lensing
  residual (FPS gas-tracking, ratio ~10, ~420 kpc). Stellar remnants track the BCG/galaxies, not the gas, so
  even granting the full IGIMF mass they fill only ~17% of the core shortfall with the wrong (centrally-spiked)
  shape. The core residual remains an honest shared-MOND open soft-spot — not a referee-proof kill (post-XRISM
  η bracket keeps the equilibrium magnitude ambiguous), not a framework-specific failure (AeST/MI/FPS-simple
  all undershoot the core identically), and not closed by any 2024-2026 mechanism.
- **No manufactured cure, no reflexive dismissal:** the IGIMF route is credited as a real integrated-mass
  partial closure (it is — Kroupa's 88% is real arithmetic and it passes G2/G3), but the core/shape failure is
  reported at full weight (the geometry mismatch is quantified, not asserted). The νHDM revival is reported as
  KILLED HARDER (2026 >5σ structure + MicroBooNE), not hand-waved. Deffayet-Woodard is reported as a real new
  theory that simply does not bear on clusters.
- **Quarantine held:** a0/Z/κ never asserted derived.

## FILES (absolute)
- `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/cluster_hunt2/igimf_remnant_core_test.py` — the core mass-budget + shape test (the G1 make-or-break)
- `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/cluster_hunt2/igimf_integrated_erass1.py` — the integrated eRASS1 both-ways test on framework footing
- `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/cluster_hunt2/ROUTE_D_FRESH_MECHANISMS_VERDICT_2026-06-20.md` — this verdict

## arXiv IDs cited
- Famaey-Pizzuti-Saltas 2410.02612 (PRD 111, 123042, 2025) — the CLASH-lensing core target; leaves closure open
- Zhang-Zonoozi-Kroupa 2602.06082 (PRD, Feb 2026) — IGIMF stellar-remnant route (THE new lead)
- νHDM: 2506.19196 (initial conditions), 2602.21975 (N-body, the >5σ kill); MicroBooNE 2025 (eV sterile exclusion)
- Deffayet-Woodard 2512.10513 (JCAP 04(2026)081) — nonlocal MOND, does not address clusters
- Durakovic-Skordis 2312.00889 (JCAP 04(2024)040) — AeST cluster isothermal spheres (banked: outskirts term, core worse)
- Superfluid DM review 2505.23900; Blanchet dipolar DM (gravitational polarization) — both new particles (G3 fails)
