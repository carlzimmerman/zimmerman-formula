# The confrontation: galaxy-side a0(z) vs cosmic ρ_DE(z)

**Confrontation lane of the cross-scale a0(z) test** (de Sitter–Unruh modified-inertia
framework, C. P. Zimmerman). Backing script: `confront.py` (exit 0, numpy/scipy, both
footings). Companion galaxy-side lane: `galaxy_a0z.py` / `GALAXY_A0Z.md`.

## What is being confronted (the non-circular content)
The framework FORCES the galaxy acceleration scale to track the cosmic dark-energy density,
a0(z) = c²√(ρ_DE(z)/32π) ⇒ **a0(z)/a0(0) = √(ρ_DE(z)/ρ_DE0)**. This is a **bridge between two
independent measurements** — (i) a0 from *galaxy dynamics* (the Λ-blind BTFR zero-point at each
z) and (ii) cosmic ρ_DE(z) from *SNe/DESI*. ΛCDM gives no reason for a galaxy's acceleration
scale to track cosmic expansion; the framework does. We confront the galaxy a0(z) against two
cosmic reference tracks:

| track | (w0, wa) | a0(z=3)/a0(0) | a0(3.25)/a0(0) |
|---|---|---|---|
| **flat-Λ** (w=−1) | (−1.00, 0.00) | **1.00** (flat) | 1.00 |
| **DESI-DR2 evolving** | (−0.75, −0.90) | **0.712** (declining) | 0.685 |
| _(alt cH0 footing, for contrast)_ | a0∝cH(z)·E(z) | 4.57 (rising) | 4.99 |

Framework distinctive prediction: **a0(3)/a0(0) ≈ 0.60–0.75** (declining). The flat−DESI track
**separation is only 0.147 dex at z=3, 0.164 dex at z=3.25** — that small gap is what the galaxy
data must resolve.

## Q1 — Does the galaxy a0(z) prefer flat or declining?
Joint χ² of the four galaxy points against each track (galaxy points from the companion lane;
z=0 SPARC anchor, z~1/2.3 sign-contested KMOS³D, z=3.25 Big Wheel):

| set | χ²(flat) | χ²(DESI-decl) | Δχ² | lean |
|---|---|---|---|---|
| all 4 points | 1.08 | 3.05 | **−1.97** | flat, weak |
| clean deep-MOND only (z=0 + Big Wheel) | 0.27 | 1.55 | **−1.28** | flat, weak |

The data **mildly prefer flat**, |Δχ²|≈1.3–2.0 — **not significant** (the intermediate-z lean is
toward *rising*, the wrong sign for the decline, but those points are not valid a0 readouts).

## Q2 — Constraining or underpowered? (the decisive number)
Separability = the maximum sigma at which the *current errors* could ever tell flat from DESI:
S = √Σ[(log a0_flat − log a0_DESI)/σ_i]².

- Big Wheel alone (z=3.25): separation 0.164 dex vs error **0.226 dex → only 0.73σ**.
- Joint, clean probes (z=0 + z=3.25): **S = 0.73σ**.
- Joint, all 4 points: **S = 0.80σ**.

**⇒ UNDERPOWERED — consistent with BOTH tracks (S < 2σ).** The M_bar systematic (~0.23 dex on
the clean z=3.25 datum; ~0.30–0.35 dex on the sign-contested intermediate points) **exceeds the
0.157-dex decline signal**. Every galaxy point sits ≤~1.2σ from *both* the flat and the declining
track. The test is **not passed and not failed.**

## Q3 — The z=0 tie
Galaxy-measured a0(0) (SPARC, Λ-blind) = 1.181e-10 ±16% vs cosmic a0(0)=(c/2)√(G ρ_DE0):

| footing | cosmic a0(0) | a0_SPARC/a0_cosmic | tension |
|---|---|---|---|
| Planck (Ω_DE=0.685, H0=67.4) | 9.36e-11 | 1.26 | **1.44σ** |
| SH0ES-H0 (H0=73.0) | 1.01e-10 | 1.17 | 0.95σ |

The **z=0 tie holds at ~1σ** on the canonical (Planck-H0) footing — the anchor the bridge extends
from. (This is by construction; a0↔Λ at z=0 is the definition, not itself a test.)

## Q4 — Both footings (the Big Wheel absolute)
Ratios cancel the footing; it re-enters only in the Big-Wheel absolute value
a0_eff(3.25)=1.54(+1.10/−0.61)e-10:

| footing | a0(3.25)/a0(0) |
|---|---|
| SPARC 1.181e-10 | 1.31 (+0.93/−0.52) |
| canonical 0.936e-10 (ρ_DE/cH_Λ) | 1.65 (+1.17/−0.65) |
| alt 1.131e-10 (ρ_tot/cH0) | 1.37 (+0.97/−0.54) |

On **every** footing the Big Wheel ratio is **consistent with flat (1.0) and with the DESI decline
(0.68)**, and **disfavors the alt-cH0 ~5× rise (~2σ, banked P~1–3%)**. Flat-vs-declining stays
undetermined.

## Q5 — Forecast (the decisive future test)
Target signal (flat − decline) at z~3 = 0.155 dex ⇒ need σ_mean = 0.052 dex for 3σ:

- SPARC-like clean deep-MOND (M_bar to 0.10 dex): **N ≈ 4** rotators per z~2–3 bin.
- Realistic high-z per-object (~0.25 dex): **N ≈ 24** per bin.
- Fixed samples: N=10 needs ≤0.16 dex/object; N=20 needs ≤0.23 dex; N=40 needs ≤0.33 dex.

Feasible: JWST/ALMA already deliver ~tens of z~2–3 gas-traced rotators; **ELT/HARMONI** resolves
individual outer (deep-MOND) rotation curves. A sample of **~20–40 clean deep-MOND z~2–3 disks
(Big-Wheel-like), M_bar to ~0.1 dex, reaches 3σ** on the declining track — the decisive test.

## Bottom line
**S(all) = 0.80σ → UNDERPOWERED, consistent with both flat and the 0.60–0.75 decline.** The z=0
tie holds (~1σ, canonical footing); the predicted decline is **neither detected nor excluded**.
The only thing the data currently exclude is the alt-cH0 *rising* footing (~2σ, via the Big
Wheel). No 'proves'; a0 magnitude inherits the posited Z — only the ratio/tracking is tested.

## Credits
Milgrom 1999 (ν-kernel + BTFR, a0∝√ρ_vac); McGaugh & Lelli (SPARC BTFR); Übler+2017, Tiley+2019,
Di Teodoro+2016, Sharma+2024 (high-z TFR); Big Wheel arXiv:2409.17956; Limbach–Psaltis–Özel 2008
(a0∝√ρ_DE); Brout+2022 / DESI DR2 (ρ_DE(z)).
