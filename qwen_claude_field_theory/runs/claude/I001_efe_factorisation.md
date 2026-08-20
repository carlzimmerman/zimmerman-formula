# I001 — Does the EFE factorise against a density-dependent a0?

**Verdict:** KILL (adverse; stronger than the idea's own KILL condition)
**Decisive number:** combined reduction = **1.097x** (raw, most generous) / **1.000x** (differential) against **181x** required (corrected) / 233x (brief). The EFE relief the idea wanted to compound does not survive as a real vector effect: derived = **1.000x**, not the committed 119–189x.
**Script:** `runs/i001_efe_factorisation.py`  (checks: 41/41, exit 0, ~20 s)

## Hypothesis

From IDEAS.md: "the committed EFE reduction (119–189x) was computed at constant a0; against a0(ρ) it may compound differently. Take the EFE suppression as a function of g_ext/a0, then let a0 vary per the promotion and recompute. PASS: the combined reduction exceeds 233x. KILL: it stays near the multiplicative estimate."

## What I actually did

The script `runs/i001_efe_factorisation.py` (pre-existing, correctly named for I001 and cross-referencing the same corpus) was **run and verified, not re-authored**, to respect the anti-manufacture discipline: a second independent re-derivation of the same 800-line nonlinear solve would only risk introducing error. It runs to 41/41 checks, exit 0, in ~20 s — well inside the 20-minute box.

Instead of importing the 119–189x, the EFE is **derived** for the legal family `J_Y = v/(1 - v/s)` two independent ways, and the promotion `a0 -> a0(ρ)` is applied on both the ephemeris and galaxy sides. (i) A linearised AQUAL operator about the saturated spherical background gives the longitudinal/transverse stiffnesses `L, T`, and the `l=1` penetration ODE is integrated with the exact background coefficients — the external field is **screened** at 1 AU (residual `2e-8`–`3e-7` of `U_ext`), not the anomaly. (ii) A perturbation-free flux bound shows the saturated anomaly is `>= s a0 (1 - 3.9e-9)` for ANY external field. The committed 119–189x is then **reproduced** and **diagnosed** as a scalar-addition artefact: the construction adds a fixed-direction external vector to a co-rotating sunward one as if collinear, and orbit-averaging gives `<cos(phase)> = -2e-16`. The galaxy-side anti-manufacture check confirms the same promotion suppresses `a0` in the SPARC galaxies too and moves their required product the *wrong* way.

## The math

Legal-family local law (spherical symmetry + Gauss):

```
J_Y(u^2) u = g_bar ,   J_Y = v/(1 - v/s),  v = |grad chi|/a0,  U = u/a0
  =>  U^2/(1 - U/s) = y   <=>   U_s(y) = [ sqrt(y^2/s^2 + 4y) - y/s ]/2
  exact saturation identity (cancellation-free):  s - U = s U^2 / y
```

EFE via the linearised AQUAL operator about the spherical background `grad chi = u(r) rhat`:

```
L = J_Y + 2 Y J_YY = (2s - v) y^2 / (s v^3) ,   T = J_Y = y/v
l=1 mode:  d/dr [ r^2 L f' ] = 2 T f
regular branch f ~ r^3   =>   delta ~ U_ext (r/r_M)^2   (external field expelled)
```

Perturbation-free flux bound (no kernel choice beyond legality):

```
< J_Y(v^2) v cos(alpha) >_sphere = y      (uniform field is divergence-free, zero net flux)
G(v) = s v^2/(s-v) = U_s^{-1},  cos(alpha) <= 1  =>  max_sphere v >= U_s(y)
```

The promotion (PROTOCOL line 6):

```
a0(nu)/a0(0) = [ (1+nu0^2)/(1+nu^2) ]^(1/4),   nu = nu0 * rho/rho0
```

## Numbers

All dimensional numbers reported on BOTH footings: `a0 = 9.3619e-11` (canonical) / `1.1279e-10` (alt) m/s².

| quantity | value (canonical / alt) | note |
|---|---|---|
| g_ext (derived, v_c=233 km/s, R_0=8.2 kpc) | 2.1456e-10 m/s² | footing-independent input; matches corpus |
| external scalar field u_ext at Sun | 0.446 a0 = 4.176e-11 / 4.911e-11 m/s² | 89% of the saturation value s a0 |
| y_MW = g_bar/a0 at the Sun | 1.846 | Sun sits INSIDE the RAR transition |
| MOND radius r_M = sqrt(GM/a0) | 7958.8 / 7251.0 AU | |
| longitudinal stiffness L/T at 1 AU | 2.53e8 (s=1/2) | the mechanism the idea hoped for, and it is real |
| EFE residual at 1 AU | 2.16e-08 – 2.81e-07 of U_ext | the *field* is screened, not the anomaly |
| flux bound on the 1-AU anomaly | >= s a0 (1 - 3.95e-09) | rigorous, any external field |
| 1-AU anomaly floor, param-free (G5) | 0.4 a0 = 3.745e-11 / 4.512e-11 m/s² | = 31539x (canonical) the Saturn limit |
| **EFE relief, DERIVED (gate E1)** | **1.000x** | NOT the committed 119–189x |
| EFE relief, committed scalar artefact | 115–186x over Earth bound | reproduced at E2, diagnosed at E3 |
| promotion relief, raw (nu0 <= 2.36e-6) | 1.097x | a0 nearly environment-independent locally |
| promotion relief, differential vs galaxies | 1.000x | same 0.4 GeV/cm³ env; Sun at y=1.85 |
| galaxy floor s (anchored / brief) | 0.4348 / 0.558 | anchored narrows the gap 1.28x (favours framework) |
| gap required | 181x (corrected) / 233x (brief) | |
| **TOTAL combined reduction** | **1.097x (raw) / 1.000x (diff)** | |

## Why this verdict

Pre-registered PASS = "the combined reduction exceeds 233x." The combined reduction is **1.097x** on the most generous raw reading and **1.000x** differentially — against **181x** required after the (framework-favouring) anchored-floor correction, **233x** on the brief's closed form. PASS does not fire by three orders of magnitude. The KILL condition ("stays near the multiplicative estimate") fires, but the result is *stronger* than that: the two effects do not merely fail to compound synergistically — the EFE term the idea wanted to compound with does not survive as a real vector effect at all. Deriving it returns **1.000x**, so the multiplicative estimate itself rested on a relief that is a scalar-addition artefact (the committed 119–189x adds a fixed galactic vector to a co-rotating sunward one as if collinear; orbit-averaging kills it). The idea removes relief the ledger was already banking rather than adding any.

## Against my own result

1. **The single surviving door (F4, not computed):** every step assumes the dark-sector density at 1 AU equals the ambient galactic value. A solar-system enhancement of ~`9.75e4`x would supply the whole factor, and it is *not excluded by planetary dynamics* (only `4.9e-13 M_sun` inside 1 AU). This is the honest weakness; if the local density is enhanced over the ambient, the differential gain could in principle close the gap. It is flagged, not closed.
2. **The anti-manufacture check (F5/F7) assumes** the Sun and the SPARC galaxies sample the same density. If the Sun samples a higher dark density than the galaxies' environments, the "moves both sides" argument breaks — which is exactly the F4 door restated.
3. **The EFE=1.0x (E3) rests on orbit-averaging** a *fixed-direction* galactic field against a co-rotating one. For a bound orbit that is robust, but a non-fixed, orbit-locked external field was not considered.
4. **The flux bound D7** is rigorous but assumes the saturated spherical background and the legal family's monotonicity. It rules out suppressing the saturated *tail* — which is precisely the ephemeris liability — so it is on point, but it is one assumption (the background) the reader should weigh.
5. **The 181x vs 233x gap:** the anchored floor 0.4348 is *smaller* than the brief's 0.558, so the corrected gap is *smaller* (more favourable to the framework); the KILL holds a fortiori on the larger 233x.

## Owed / not computed

- **Dark-sector density at 1 AU vs ambient** (F4): a `~1e5`x enhancement would close the gap; needs a dark-sector density model / the promotion evaluated at the actual local density field. Not computed.
- **The extra force from `grad a0`** if such a density gradient existed — not computed.
- **The EFE-present exact two-body solve** (referenced as owed in `aqual_efe_a0line_kernel_2026.py`) — out of scope here.

## Files touched

- `runs/i001_efe_factorisation.py` — pre-existing; **run and verified** (41/41, ~20 s, exit 0), not modified.
- `results/I001_efe_factorisation.md` — this file (new).
- `LEDGER.md` — one row appended.
