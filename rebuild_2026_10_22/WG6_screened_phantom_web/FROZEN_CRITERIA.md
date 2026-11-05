# WG6_screened_phantom_web: FROZEN CRITERIA, committed alone before any script or number

**Not blind.** These results are known:
- **WG2 / WG4:** with the law on as QUMOND, a baryons-only start and a0 tracking DESI's ρ_DE, CMB lensing overshoots: r 6.7-8.5 on B2D.
- **WG3 T1τ0:** a uniform halving of the phantom lands, at 1.3-1.9.
- **WG5:** pure modified inertia is closed.

Expected before any run: screening at 10 Mpc (μ = 0.1 Mpc⁻¹) removes most of the phantom on CMB-lensing scales and reads low; 100 Mpc (0.01 Mpc⁻¹) reads close to unscreened.

κ = ½ FITTED. The cold sector stays retired. No particle and no cold component is added. Not theory closed. Nothing here says the data favour the framework. No downloads.

**Owner 2026-11-04:** "OK lets do that then", on a mass term that weakens the law beyond tens of Mpc, put in by hand. In the same turn I corrected my description of the record's term:
- v3/AeST's μ_K (BS24 static limit, `V3_FULL_PICTURE.md` §2) enters as +μ_K²ψ. That is the oscillating sign: it does not screen.
- It also carries v3's khronon dust, which belongs to the retired sector.

So this lane tests a **new, by-hand screening term**, labelled as such. Any value that lands is FITTED, not derived.

## Rule
- **R1Y(μ):** QUMOND on the peculiar field, as WG2/WG4, with only the phantom part of the potential Yukawa-screened:
  - φ_k = φ_N,k + φ_ph,k × k²/(k² + μ²);
  - in real space the phantom's Green's function becomes e^(−μr)/r;
  - Newton is untouched;
  - lensing sees φ.
- **a0:** tracks ρ_DE (DESI DR2 CPL, the owner's standing rule; WG4's DE rule).
- **Background:** B2D (WG4).
- **Everything else is WG2's:** engine (imported read only, through WG4's patch), ICs, box, steps, projection, PR4 grading and r.
- **μ values:** {0.01, 0.03, 0.1} Mpc⁻¹, i.e. screening lengths of 100, 33 and 10 Mpc.
  - The top value is the record's galaxy-lensing bound on a mass term (S4, μ_K < 0.1 Mpc⁻¹). That bound was derived for the oscillating sign. G-gal below checks this term's own galaxy effect.
  - Three values spanning the range is a bracket, not a scan. No value between them is run after the results.

## Run matrix (canonical, 128³, 200 steps, z_on 50)
- R1Y(μ) × μ {0.01, 0.03, 0.1} × A_s {1e-9, 4e-9}: 6 runs.
- K5: R1Y(0.03), A_s 2.1e-9, at 128³ and 192³: 2 runs.

## Labels
- **Per μ, over its two A_s members, with WG2's thresholds:** FAILS LOW if r < 0.5; FAILS HIGH if r > 2; WITHIN ×2 if 0.5 ≤ r ≤ 2; STRADDLES otherwise.
- **Lane reading:**
  - If no μ reads WITHIN ×2 and the bracket goes from FAILS HIGH at 0.01 to FAILS LOW at 0.1: "the allowed range crosses the measured amplitude between bracket members". No interpolated value is quoted as a result. Any value inside would be FITTED.
  - If a μ reads WITHIN ×2 and passes G-gal: "a screening length of 1/μ lands within ×2, FITTED, not derived, allowed by the galaxy-lensing gate".
  - If every μ FAILS HIGH: "screening within the galaxy-allowed range can't supply the factor".
  - If every μ FAILS LOW: "every allowed screening overshoots low".

## G-gal: the galaxy-lensing gate for this term
This is computed, not fitted.
- **Lens:** an isolated deep-MOND point lens. The phantom density is ρ_ph = √(G M a0)/(4πG r²) out to 10 Mpc; its total density is scale-free, so the result depends only on μr.
- **Screening:** applied to the phantom's potential with Yukawa shells. Outside a shell: −G dm e^(−μr) sinh(μs)/(μs r). Inside: −G dm e^(−μs) sinh(μr)/(μr s).
- **Pass:** the screened over unscreened radial force of the phantom must be ≥ 0.89 (0.05 dex) at r = 0.1, 0.3 and 1 Mpc. That is KiDS's isolated-lens range, where the law is already 0.09 dex short (LE1). r = 3 Mpc is reported.
- A μ that fails G-gal can't be the rule, whatever its CMB-lensing label.

## Checks (all must PASS before any label is read)
- **K1-K3:** WG2's K1 and K2 on the imported engine; K3 Limber; K4b ICs on R1Y(0.03) A_s 2.1e-9.
- **K10, screening code test** on a random 32³ field, off the Nyquist planes, to 1e-6:
  - (a) μ = 1e-12 reproduces R1;
  - (b) μ = 1e6 reproduces R0.
- **K11, Yukawa shell code test:** for μ → 0 the shell force equals the unscreened force to 1e-6 at r = 1 Mpc.
- **K5:** the 192³ run must give the same label as 128³. Otherwise R1Y(0.03) carries NOT CONVERGED.
- **MUTATE:** WG2's Poisson-halved K1 must FAIL. Outputs carry `_MUTATE`.

## What this lane can't say
- The term is not from any action on record. A landing value is a FITTED new length, like κ, not a derivation.
- Everything WG2 can't say also holds here.
- G-gal is an isolated point lens. Real lenses sit in an external field.
- Nothing here reinstates the cold sector.

## Output
- `wg6_pm.py`: wraps WG4's patched engine and adds R1Y, K10 and K11.
- `wg6_ggal.py`: G-gal.
- `wg6_run_all.py`: the 8 runs.
- `wg6_grade.py`: copies WG2's projection; writes `wg6_results.json` and `wg6.out`. MUTATE writes `_MUTATE`.
- `README.md`.
