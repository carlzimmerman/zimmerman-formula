# AG4i FROZEN CRITERIA (2026-10-20): the five clean positive-pull galaxies against independent kinematics and radial M/L gradients

Committed alone, before any AG4i script or number. Owner's go (2026-10-20, in chat): "freeze criteria and run the follow-up as a
small job: refit the pulls with the independent rotation curves (NGC 5985 GHASP, UGC 731 and NGC 5023 de Blok & Bosma) and
with radial M/L gradients from the colour profiles, against law-true mocks."

## Galaxies and data (owner-approved fetch; `_external_data/five_galaxies_2026_10_20/`, FETCH_LOG cbba8e465)
- The galaxies are AG4h's five: NGC0024, NGC5985, UGC00128, UGC00731, UGC08286 (= NGC 5023). Their AG4g pulls are
  +3.40, +3.55, +3.50, +4.90 and +3.70.
- **Baryons always come from SPARC** (rotmod Vgas, Vdisk, Vbul, SBdisk, SBbul). The law is n=1 at the canonical a₀. AG4g's
  estimator is unchanged: Υ prior N(log 0.5, 0.10), bulge 1.4Υ, s₀ = 0.05 dex, coherent c_g from SPARC's eD and eInc,
  MAP over the grid.
- **K. Independent rotation curves:**
  - NGC 5985: GHASP (Epinat+2008, tablef). Vrot is deprojected with GHASP's own kinematic inclination. Radii are taken in
    arcsec and converted at SPARC's distance.
  - UGC 731 and NGC 5023: de Blok & Bosma 2002 rawcurve (Hα long slit, not corrected for inclination).
    V = |Vrot|/sin i_SPARC; radius = |r| at SPARC's distance; both sides folded.
  - Every curve is binned in 6″ radial bins over both sides:
    - V is the mean of the points in the bin. Its error is √(σ_mean² + (asym/2)²), with σ_mean = sd/√n (the median e_Vrot
      when n = 1) and asym = |mean(side 1) − mean(side 2)| when both sides are present. The floor is 3 km/s.
    - For GHASP the side comes from its Side column. For the raw curves it is the sign of r.
  - Only bins inside SPARC's radial range are used. Baryons are interpolated linearly in R (on V² for each component).
  - Reported, not graded: NGC 5023's procurve, which is only partly independent beyond 180″.
- **M. Radial M/L gradient from the [3.6]−[4.5] colour:**
  - **Relation:** Meidt et al. 2014, ApJ 788, 144, Eq. 4, log Υ₃.₆ = 3.98(±0.98)([3.6]−[4.5]) + 0.13, with Vega colours.
    Verified from the paper's text in this session (arXiv 1402.5210).
  - **Primary slope:** β = 3.98. Variants: β = 2.99 and 4.97 (±1σ), and β = −0.74 (the paper's LMC-based Eq. 5).
  - **Colour:** [3.6]−[4.5]_Vega = −2.5 log₁₀(I₁/I₂) + 2.5 log₁₀(280.9/179.7). Only the gradient matters, through
    c(R) − c̄.
  - **NGC 24, NGC 5985, NGC 5023:** colour from the S4G P3 `fx2a` profiles (column 1 is the semi-major axis in 0.75″ pixels;
    column 2 is the intensity; column 3 its error).
  - **UGC 128 and UGC 731:** colour from this lane's own elliptical-annulus photometry on the IRAC ch1/ch2 images.
    - Centre from `sesame_sparc.csv`. PA from intensity-weighted second moments within 60″; axis ratio from SPARC's
      inclination (b/a = cos i).
    - Annuli 6″ wide; the background is the median of an annulus at 1.5–2× the outermost used radius; pixels more than 5σ
      above an annulus' median are clipped.
  - A radius is used only where both bands have I/σ ≥ 10. The colour is smoothed by a running median of 5 points; beyond the
    last valid radius it is held at the last valid value.
  - c̄ is the SBdisk-weighted mean of c(R) over SPARC's radii.
  - **Υ(R)/Υ₀ = 10^(β(c(R) − c̄)), applied to the disc only.** NGC 5985's bulge keeps 1.4Υ₀ (declared approximation).
  - **The new disc rotation curve:** a thin-disc Hankel transform of Σ(R) ∝ SBdisk(R)·Υ(R)/Υ₀, exponentially extrapolated
    beyond the last SPARC point. The multiplier m(R) = V²_grad/V²_const comes from the same code with constant Υ, so the
    disc-thickness treatment cancels. Vdisk² → m(R)·Vdisk².
- **K+M:** the independent curve combined with the gradient-modified baryons, for NGC 5985, UGC 731 and NGC 5023.

## Law-true mocks, per galaxy and per variant
200 mocks built with that variant's own radii, errors and baryon model (seeds 1–200): Υ_true from the prior,
c_true ~ N(0, c_g), and per-point noise N(0, √(σ_i² + s₀²)) in log g. Each mock is refitted identically.
p_emp = the fraction of mocks with |pull| ≥ |pull_obs|.

## Readings
- **Per galaxy and variant:**
  - **RESOLVED** if |pull| < 3.
  - **PERSISTS** if |pull| ≥ 3 and p_emp < 0.01.
  - **WEAK** if |pull| ≥ 3 and p_emp ≥ 0.01 (that variant's mocks are too broad to tell).
- **Per galaxy, using the primary β:**
  - **KINEMATIC:** K resolves it.
  - **M/L GRADIENT:** M resolves it with SPARC's curve.
  - **BOTH NEEDED:** only K+M resolves it.
  - **UNEXPLAINED:** it persists under every variant available for it. NGC 24 and UGC 128 have only M.
- **Summary:** the five classes are reported. A galaxy is a candidate for a real profile difference only if it is UNEXPLAINED.
  It is a pointer for its own pre-registered test, not a detection.
- Also reported for every variant: AG4h's shape statistic Δχ² (Υ at SPS with a free offset, vs Υ free).

## Controls
- **K1:** with SPARC's own curve and β = 0, AG4g's five pulls are reproduced exactly.
- **K2 (thin-disc code):** with constant Υ, the normalised V_disk(R) from SPARC's SBdisk matches SPARC's Vdisk shape within ±15%
  at every SPARC radius beyond the first point, for each of the five. The NGC 5985 disc component is checked alone.
- **K3 (own photometry, UGC 128 and UGC 731):** the 3.6 μm surface-brightness profile from this lane's photometry matches the
  shape of SPARC's SBdisk within 0.3 mag rms over the valid radii (normalisation free). If K3 fails, that galaxy's M variant
  is reported as NOT AVAILABLE.
- **K4 (independent curves):** the median ratio V_ind/V_SPARC over the common radii is reported, for information.

## MUTATE
`AG4I_MUTATE=1` runs K on SPARC's own curve (at SPARC radii, with SPARC errors) and M with β = 0. Every one of the five must then
return PERSISTS or WEAK with |pull| ≥ 3, as in AG4g. The script then exits 1 (the control bites).

## Settings
κ = ½ fitted; not theory closed. A small job beside NC2x under the owner's 10-20 rule (< 1 GB, single thread, minutes).
Outputs: `ag4i.py` → `ag4i.out`, `ag4i_results.json`; MUTATE → `_MUTATE`. Downloaded files are read only (astropy; nothing in
them is executed).
