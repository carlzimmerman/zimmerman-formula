# Stellar self-gravity selects massive spirals; the field response is still missing

This is a finite independent-selector and angular-momentum screen, not a bar mechanism that passes the data. The externally specified ELN stellar-disc proxy leaves most dwarfs unselected and selects most 150–250 km/s spirals. It also selects many 250–400 km/s galaxies, so it does not isolate precisely the required response window. Whole-disc angular momentum can pay much of the conditional energy demand, while the initially enclosed bar region cannot pay in the tested geometries. Neither statement supplies the actual field torque, bar history or surviving final rotation curve.

The comparator is **historical ng64-era ER1**, with canonical-A energies reconstructed from A's own EM1 mass line and h. No ng80 or full-grader result is claimed. Cold dark energy is a gravitating field component, never a particle. No a0 is used.

## Independent structural criterion and its validity limit

[Efstathiou, Lake & Negroponte (1982), original paper](https://adsabs.harvard.edu/pdf/1982MNRAS.199.1069E), study cold exponential stellar discs and propose `epsilon_m=Vmax/sqrt(G Md/Rd)<1.1` as the bar-unstable side. The threshold is taken from that paper, without fitting any SPARC bin or response residual. Its self-gravitating exponential-disc coefficient is approximately0.63, so the force-based form here is `epsilon_m=0.63 Vobs,max/[sqrt(.50) Vdisk,max]`. Upsilon stays .50.

This is an externally specified **structural proxy**, not a reliable general instability criterion. [Athanassoula (2008)](https://arxiv.org/abs/0808.0016) explicitly shows that the ELN criterion cannot generally distinguish bar stability; random stellar motion and the live halo matter. We have no measured SPARC stellar dispersions, bar amplitudes, lengths or pattern speeds. A criterion-selected galaxy is not an observed or predicted barred galaxy.

Three mass alternatives were declared before calculation:

1. `Md_phot=2 pi(.50 SBdisk)Rd^2`, extrapolating the catalogue central brightness as one exponential to infinity.
2. `Md_force=.50 Vdisk,max^2 Rd/(0.63^2 G)`, interpreting the tabulated stellar-disc force peak as an exponential-disc normalization.
3. `Md_total_light=.50 L36`, a generous upper allowance assigning all stellar light to the disc, including any bulge.

**The first must not be treated as measured total disc mass:** it exceeds catalogue total stellar luminosity in101/123 galaxies. This is a failure of that extrapolation, not additional observed baryonic mass. Its raw selection and AM outputs are retained in run002 but are not the physical headline. The force proxy also assumes an exponential relation and can differ from total light; those discrepancies and bulges/truncated coverage are retained. The two other proxies give the same broad dwarf/spiral ordering.

The [independent coordinator-appointed review](../../../reviews/er2_ng80_selective_response_2026_11_01/BAR_REVIEW.md) also finds that the force-derived exponential-equivalent mass exceeds the all-light stellar allowance in46/123 galaxies, including9/25 and7/18 target spirals. It therefore cannot be treated as a measured stellar mass or guaranteed physical angular-momentum reservoir. The reported force ratio is still a reproducible structural proxy; its exponential-mass and AM interpretation is conditional. The review also distinguishes the inherited ER1 Delta W/2 comparator from exact mechanical energy in extended fixed baryons. A separate energy-functional audit retains the original results and investigates that issue.

| Vflat, km/s | n | Force proxy selected | Total-light upper-disc proxy selected | Force-clean selected / n |
|---|---:|---:|---:|---:|
| 20–60 | 12 | 0 | 1 | 0/8 |
| 60–100 | 35 | 1 | 1 | 0/25 |
| 100–150 | 23 | 5 | 6 | 3/16 |
| 150–200 | 25 | 20 | 22 | 12/12 |
| 200–250 | 18 | 12 | 15 | 6/7 |
| 250–400 | 10 | 6 | 7 | 2/2 |

The force-clean sensitivity omits bulge force, curves shorter than4Rd and disc-force peaks at a curve edge. It was defined **after** finding the photometric extrapolation problem, explicitly as a sensitivity specific to the force proxy. The predeclared clean subset additionally rejected photometric luminosity excess and is tiny; its counts remain in run002. No galaxies were silently removed from the all-row result. Of the target bins,10/25 and10/18 have bulge force,3/25 and5/18 have their observed Vmax inside Rd, and3/25 and1/18 have curves shorter than4Rd. No morphology-to-response or V-bin threshold was tuned.

## Jacobi work and the angular-momentum allowance

For a fixed-amplitude pattern `Phi(R,phi-Omega_p t)`:

`dE/dt=partial_t Phi=-Omega_p partial_phi Phi=Omega_p dLz/dt`.

Thus `Delta E=Omega_p Delta Lz` for a steady pattern. [Sellwood & Binney (2002), section2](https://academic.oup.com/mnras/article/336/3/785/973352) give the corresponding Jacobi integral and energy/angular-momentum relation. It is a total orbital-work relation; it does not say how much becomes irreversible cold-field heating. A varying-amplitude/speed bar requires the actual time-dependent work accounting.

We integrate an exponential stellar disc's current angular momentum using observed rotation curves, with disclosed inner/outer extensions. The force and total-light alternatives analytically rescale this integral by their mass normalizations. `E_req/(Omega_p L_disc)` reports the fraction of the **entire stellar disc's current** angular momentum that would have to be transferred at perfect work delivery. This is a deliberately generous reservoir allowance: losing a large fraction changes the disc and does not preserve the fixed baryons assumed by the historical energy target.

A stellar bar is a density pattern supported by stellar orbits. It is **not a rigid material body**, so no `I Omega_p^2/2` is used as its actual stellar-bar energy. `L(<a_bar)` below is only the present stellar angular momentum inside an assumed radius. It is not a universal upper bound on an evolving bar's access to the outer disc, replenished gas, growing extent, or prior histories.

Geometry alternatives come from primary observations: [Erwin (2005)](https://arxiv.org/abs/astro-ph/0508590) reports mean bar semimajor axis/disc scale length around0.6 in late types and1.4 in early types, with much broader distributions; [Aguerri, Debattista & Corsini (2003)](https://arxiv.org/abs/astro-ph/0209377) find five early-type bars consistent with `R_CR/a_bar=1–1.4`. We apply all four combinations to **every** galaxy, without assigning geometry by desired V bin. `Omega_p=Vobs(R_CR)/R_CR`; cases lacking observed coverage there are omitted and counted. These alternatives are neither a universal bracket nor measurements of these SPARC bars.

Force-based disc results, medians:

| a_bar/Rd | R_CR/a_bar | 150–200: n | Required Delta L/L_disc | Required Delta L/L(<a_bar) | 200–250: n | Required Delta L/L_disc | Required Delta L/L(<a_bar) |
|---|---|---:|---:|---:|---:|---:|---:|
|0.6|1.0|17|0.259|16.11|15|0.118|5.61|
|0.6|1.4|21|0.400|29.07|16|0.164|8.03|
|1.4|1.0|24|0.568|4.03|17|0.257|1.66|
|1.4|1.4|25|0.721|4.94|18|0.348|2.30|

The **whole force-normalized disc** can pay the target in16/17,19/21,20/24,21/25 galaxies in the150–200 bin; it can pay15/15,16/16,17/17,17/18 in200–250. Every force-selected targeted galaxy can pay except1/19 and1/20 in the two longer-bar geometries at150–200. Total-light upper-disc allowances are generally more generous; all detailed counts are in run003.

The **initial angular momentum inside the assumed bar** pays **zero** targeted galaxies in all four geometries for either force or total-light normalization. This rejects the narrow isolated-current-bar-region reservoir model. It does not exclude bars exchanging substantial angular momentum through the outer disc, changing size or coupling over their history. A physical calculation must determine those exchanges and the field's response; no delivery efficiency was fitted here.

## Conditional radius discriminator

For a flat circular curve, `Omega=V/R`, `kappa=sqrt(2) Omega`. The m=2 outer Lindblad condition `Omega_p=Omega+kappa/2`, together with `Omega_p=V/R_CR`, gives

`R_OLR=(1+1/sqrt(2))R_CR`.

The four declared geometry alternatives yield:

| a_bar/Rd | R_CR/a_bar | R_OLR/Rd |
|---|---|---:|
|0.6|1.0|1.0243|
|0.6|1.4|1.4340|
|1.4|1.0|2.3899|
|1.4|1.4|3.3459|

Longer-bar alternatives place this circular-orbit resonance in the2–4Rd region where the rotation-curve response is evaluated, while the shorter alternatives put it further inward. This is a **conditional stellar/circular resonance analogy**. A halo field's actual resonances depend on its orbital/phase-space dynamics and need not be circular epicycles or this radius. No field torque or radial heating profile follows from this arithmetic. Four direct substitutions check the frequency condition to2.22e-16 in run004.

## Evidence, failures and remaining input

`CONTRACT.md` and `contract.json` preceded the first calculation. run001 failed the20-versus30Rd angular-momentum convergence check at1.97e-5, caused by trapezoidal sampling across the discontinuous switch from the last observed velocity to catalogue Vflat. No scientific result was accepted. `CONTRACT_v2.md` records that diagnosis before the accepted run; v2 splits the measured interval and integrates the exponential outer tail analytically. The original code/contract are retained. No physical input or tolerance changed.

`run002/manifest.json` and `run003/manifest.json` are **completed**, validator-checked v2 records. run002 covers the original123 rows and184 inputs, computes the selector/geometry and reconstructs canonical-A energy. run003 records the transparent mass rescaling and post-result force-clean sensitivity. run004 records only the four radius arithmetic cases. Raw literature tool evidence is preserved in the two `primary_sources*raw.json` files.

The independent B-energy reconstruction matches historical ER1 to7.21e-15. Canonical-A energies use A's own EM1 coefficients a=11.18,b=.90 and its h; their full-undo values are0.9446–0.9670 of the overwritten B records. This correction includes the mass line, unlike a h-only comparison. Epsilon algebra agrees to3.33e-16; the Jacobi quadrupole identity is exact at floating precision; exponential flat-curve AM agrees to4.51e-11;20-versus30Rd AM differs at most1.05e-6. These verify the stated finite arithmetic and bookkeeping, not the external ELN approximation or a native field response.

Key SHA256: `bar_screen_v2.py` `b68ebfc8bde2be96c73f9c2789c346c485a09c72266aa3cdf8bd2589e1324bb8`; run002 results `ba0d80d038022068486fb9be71e7449c50b18030d24722ec29e548aae82783d8`; run003 results `16cf3a41b7e7f7071dd999bf2c6cac34c1789119472a03685cde7f84406ac378`. Every raw curve/table/profile/background input hash is in run002's manifest.

The bounded outcome is **a useful independent structural preference with conditional AM feasibility, not a supplied mechanism**. The next required evidence is independently measured bar incidence/amplitude/length/pattern speed and stellar dispersions, and a native gravitating-field wake/phase-space or caustic completion. Only then can this selector be translated into a response and graded against the spiral/dwarf rotation curves. An arbitrary epsilon-to-response function would remain a fit and was not introduced.
