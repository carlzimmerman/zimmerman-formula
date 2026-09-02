# The CRISPY gap, closed as a prediction: what ΛCDM must do to its dark-matter fabric to track a₀(z), and what it costs (2026-09-02)

**The gap (2026-07-30).** CRISPY DARK MATTER showed *that* ΛCDM would absorb an evolving-dark-energy result by tweaking parameters, but
did not predict *what property of the dark component* modellers would have to change to track the redshift dependence of a₀, nor its cost.
**Script:** `crispy_fabric_prediction_2026.py` (7 checks, rc=0; output `.out`). Both a₀ footings cancel in every ratio used.

## 1. ΛCDM's native prediction is a rising RAR scale
ΛCDM has no fundamental a₀; its radial-acceleration relation is emergent from halo structure, and halo structure is locked to the
critical density at formation. For an NFW halo the characteristic acceleration at the scale radius is
a_s = G M(<r_s)/r_s² = g₂₀₀ c² f(1)/f(c), g₂₀₀ ∝ M^{1/3} ρ_crit(z)^{2/3} ∝ M^{1/3} H(z)^{4/3}, f(x) = ln(1+x) − x/(1+x).
With the mass–concentration–redshift relation of Dutton & Macciò 2014 (Duffy 2008 as a sensitivity row), at fixed M₂₀₀ = 10¹² M☉:

| z | 0.5 | 1 | 2 | 2.3 | 3 | 5 |
|---|---|---|---|---|---|---|
| a_s(z)/a_s(0), DM14 | 1.08 | 1.23 | 1.76 | 1.97 | 2.57 | 5.10 |
| a_s(z)/a_s(0), D08 | 1.13 | 1.43 | 2.28 | 2.59 | 3.37 | 6.04 |

This reproduces the hydrodynamical result (Magneticum, Mayer et al. 2023: apparent a₀ rising ~×3 by z = 2.3, robust without feedback) to
within a factor 1.6, and it is the order of the MUSE-DARK III rise (×2.4 at z ~ 1). **The MUSE rise is ΛCDM-native, not a framework signal.**

## 2. The framework's laws against it
| z | stage-17 derived law | CPL (DESI-DR2 dressing) | rival a₀ ∝ H(z) | ΛCDM-native (DM14) |
|---|---|---|---|---|
| 1 | 1.000 | 0.96 | 1.79 | 1.23 |
| 2 | 1.000 | 0.81 | 3.03 | 1.76 |
| 3 | 1.000 | 0.70 | 4.57 | 2.57 |
| 5 | 0.9999 | 0.54 | 8.29 | 5.10 |

## 3. The prediction: the fabric change, quantified
To mimic a **constant** a₀ out to z ~ 3–5, ΛCDM must break the ρ_crit-lock: the inner-halo characteristic acceleration ρ_s r_s must be made
redshift-independent. The required concentration relative to gravity-only N-body (M₂₀₀ = 10¹², DM14):

| z | c_N-body | c_req (constant a₀) | c_req/c_N-body | ρ_s ratio | (H/H₀)^{−2/3} | c_req (CPL law) |
|---|---|---|---|---|---|---|
| 0.5 | 6.76 | 6.38 | 0.94 | 0.87 | 0.83 | 0.96 × c_N-body |
| 1 | 5.50 | 4.67 | 0.85 | 0.69 | 0.68 | 0.82 |
| 2 | 4.18 | 2.55 | 0.61 | 0.35 | 0.48 | 0.50 |
| 3 | 3.64 | 1.44 | 0.40 | 0.15 | 0.36 | 0.24 |
| 5 | 3.31 | 0.38 | 0.12 | 0.02 | 0.24 | no NFW solution |

In words: **dark-matter interiors that dilute with redshift as (H/H₀)^{−2/3} in concentration, (H/H₀)^{−4/3} in ρ_s r_s** — a property no
gravity-only halo has (their interiors get denser with z), which feedback does not supply (Magneticum's rise survives without feedback),
and which by z = 3 requires halos at 15% of the N-body inner density and by z = 5 at 2%. For the CPL-declining law no NFW concentration is
diffuse enough at z = 5 (c²/f(c) ≥ 2 as c → 0). That is not a parameter shift; it is a new, expansion-rate-locked property of the component.

## 4. The observable lever, and which arm
BTFR: v⁴ = G M a₀, so the M(v) zero-point shifts by log(a₀_eff(z)/a₀(0)): ΛCDM-native +0.09 (z=1), +0.24 (z=2), +0.41 dex (z=3);
framework 0.00 (stage 17) or −0.09/−0.16 (CPL). A > 0.3 dex discriminator at z = 3. The RAR-fit arm on z ~ 1 star-forming disks is where
ΛCDM's native rise lives and where pressure support contaminates; the clean arm is the BTFR / massive-disk zero-point at z ≥ 2 (the z = 3.25
Big Wheel is flat; KMOS3D/KROSS flat-to-declining). **Both ways:** a rising zero-point at z ≥ 2 favours ΛCDM-native structure and kills the
framework's flat law; a flat one forces the fabric change above.

## Scope
Fixed-M₂₀₀ scaling (the fixed-M★ version needs the SHMR's evolution; the direction is the same); NFW; two published c(M,z) fits; the
hydrodynamical cross-check is Magneticum's number as quoted in the repo's MUSE confrontation record. The framework's flat law is not
distinctive against constant-a₀ MOND; it is distinctive against ΛCDM. a₀ and κ are inputs and cancel here.
