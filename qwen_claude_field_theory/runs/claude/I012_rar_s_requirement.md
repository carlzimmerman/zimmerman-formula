# I012 — Is the RAR requirement on s really 0.558?

**Verdict:** PARTIAL
**Decisive number:** refitting Upsilon drops the galaxy-side floor on s from 0.558 to
**s ≥ 0.219 (canonical a0 = 9.3619e-11)** / **s ≥ 0.172 (alt a0 = 1.1279e-10)** — a
~2.5–3.2× relief, but s < 0.1 is excluded (s=0.1 → 0.176–0.187 dex, U=1.0, 12.1 σ vs s=0.5).
The 233× ephemeris/galaxy gap shrinks to **72–91×** but is not closed.
**Script:** `runs/i012_rar_s_requirement.py`  (checks: 22/22, exit 0, 5 s)

## Hypothesis
`U(y~2) >= 0.4` (the `s >= 0.558` galaxy floor) was read off the a0-line with Upsilon FROZEN;
a proper per-kernel refit of Upsilon on the real SPARC component decompositions may allow a
much smaller s.

## What I actually did
For `s in [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1, 2]` I refit the stellar mass-to-light
ratio `Upsilon` (committed 1-parameter convention `Upsilon_bulge = 1.4·Upsilon_disk`, and a
generous 2-parameter `(Ud,Ub)` variant) on the 3389 real SPARC RAR points, reporting the best
rms in dex at each s, at BOTH a0 footings. `g_bar` is rebuilt exactly from
`sign(Vgas)Vgas^2 + Ud·Vdisk^2 + Ub·Vbul^2` for every Upsilon (never rescaled — see C2 below).
The kernel scanned is the closed-form legal family `U_s(y) = s·sqrt(y)/(s+sqrt(y))`, `y = g_bar/a0`,
`g_obs = g_bar + a0·U_s(y)`, alongside Carl's a0-line `g_obs = sqrt(g_bar^2 + g_bar·a0)`.
The data are the committed `rar_real_sparc.json` (verified bit-identical to the raw 0.7/0.7 build).
Two premises in the brief are FALSE and are corrected as numbered checks (C1, C2); both corrections
make the small-s verdict *harder*, not easier, so they do not flatter the framework.

## The math
- Legal family, ghost-free: `U_s(y) = s·sqrt(y)/(s+sqrt(y))`, strictly increasing, `U_s → sqrt(y)`
  as `y→0` and `U_s → s` as `y→∞` (verified monotone for every s scanned).
- The a0-line is `U(y) = sqrt(y^2+y) - y` ≡ `sqrt(1+1/y)·g_bar/a0`; it also has both shared limits
  but is a **different function** (C1): at y=2 it gives 0.4495 vs the family's 0.3694 (ratio 0.82).
  The committed 0.1083 dex belongs to the a0-line, NOT to the family at s=1/2 (family s=1/2 fits at
  0.1195 dex) — splicing the two kernels would have manufactured a small-s win.
- Fit metric: eV/Vobs-weighted rms of `log10 g_obs − log10 g_obs_pred`, `Ub = 1.4·Ud`.
- Why small s fails structurally: the family is MOND-like (`U_s ~ sqrt(y)`) only where `sqrt(y) << s`,
  i.e. `y << s^2`. As s shrinks this deep-MOND window retreats below the SPARC data
  (`y` spans 1e-3..1e3; `frac(y<s^2)`: s=0.1 → 0.00%, s=0.5 → 12%), so every point sees the
  saturated `U_s ~ s` and the kernel goes Newtonian. The degradation is **smooth and monotonic**,
  crossing 0.15 dex at s ≈ 0.219 — NOT the "sharp cliff at 0.4" the brief predicted.

## Numbers
| quantity | value | note |
|---|---|---|
| GATE: a0-line, Udisk=0.70, Ub=1.4Ud | 0.1083 dex | reproduces committed value exactly |
| a0-line refit, canonical / alt a0 | U=0.696 → 0.1083 / U=0.650 → 0.1036 dex | best a0-line fit |
| s=0.1, canonical / alt | 0.1866 / 0.1763 dex at U=1.009 / 0.979 | > 0.15, U outside 0.3–0.9 |
| s=0.2, canonical / alt | 0.1541 / 0.1433 dex at U=0.905 / 0.868 | canonical just over, alt just under |
| s=0.5, canonical / alt | 0.1195 / 0.1120 dex at U=0.757 / 0.714 | inside the band |
| 2-param rescue, s=0.1 | 0.1748 dex at Ud=1.208 | freeing bulge M/L does not save it |
| **galaxy floor (rms=0.15 dex)** | **0.219 / 0.173** | down from 0.558 |
| **galaxy floor (Upsilon=0.90)** | **0.207 / 0.165** | the two bind together |
| binding floor s ≥ | **0.219 (canon) / 0.172 (alt)** | ~2.5–3.2× below 0.558 |
| s=0.1 vs s=0.5, 400× galaxy bootstrap | +0.067 dex, 12.1 σ, P=0.000 | small s excluded |
| s_eph_max (ephemeris ceiling) | 2.397e-3 (opt EFE) / 1.509e-3 (cons) | reproduces s ≤ 2.4e-3 |
| old gap (frozen Upsilon) | 232.8× | reproduces briefed 233× |
| **new gap (refit, opt / cons EFE)** | **72.0–145.1× (canon), 72.0–114.3× (alt)** | not closed |
| relief factor | 3.24× | genuine but partial |

## Why this verdict
The brief's **PASS** ("some s < 0.1 reaches < 0.15 dex") is **NOT met**: s=0.1 needs U=1.0
(outside the Spitzer 0.3–0.9 band) and still costs 0.187 dex; it is 12.1 σ worse than s=0.5.
The brief's **KILL** ("rms blows up below s ~ 0.4") is **also not accurate as worded** — there is
no cliff; the rms crosses 0.15 dex smoothly at s ≈ 0.219. So neither pre-registered condition fires
cleanly: the hypothesis is *partly* right (refitting genuinely lowers the floor from 0.558 to
~0.17–0.22, a 2.5–3.2× relief) but the deeper claim (small s is viable, the tension is an artefact)
is *refuted* — the 233× ephemeris/galaxy gap survives as 72–91×. PARTIAL: decisive numbers,
refutes the specific 0.558 figure, but does not resolve the framework's core tension.

## Against my own result
- **Upsilon band is the real arbiter, and it is somewhat conventional.** The floor is set by
  two independent constraints biting at nearly the same s (rms=0.15 at 0.219; Upsilon=0.90 at
  0.207). If the Spitzer 3.6 µm M/L band were legitimately wider on the low end (young/gas-rich
  dwarfs can have M/L well below 0.3), the Upsilon constraint loosens and the rms alone bites at
  ~0.20–0.22 — a small shift, but it shows the "0.17–0.22" floor is band-sensitive, not an absolute.
- **The 2-param variant (free bulge M/L) is generous and still fails**, which strengthens the
  "small s is excluded" reading but weakens the "0.558 was a frozen-Upsilon artefact" reading:
  even with two free M/L ratios s=0.1 reaches only 0.175 dex.
- **EFE treatment is a big unmodelled swing.** The gap numbers depend on the committed 119–189×
  EFE reduction. I001 found the *derived* EFE relief is ~1.0×, not 119–189×; if that holds, the
  ephemeris ceiling is far tighter than 2.4e-3 and the "72× gap" is an underestimate — the tension
  is *worse* than reported here.
- **Only one kernel family tested.** The result is specific to `U_s = s·sqrt(y)/(s+sqrt(y))` and the
  a0-line. A legal kernel whose approach to saturation is slower in radius, or an EFE-dressed kernel
  with a radius-dependent effective s, is not ruled out.

## Owed / not computed
- A legal kernel *outside* the one-parameter family (slower saturation, or effective s differing
  between solar system and galaxy outskirts) — the only route that could separate the two regimes.
- A self-consistent EFE-dressed s that differs by environment, on a per-galaxy basis.
- What the ephemeris ceiling is under the I001 "EFE relief ≈ 1.0×" finding rather than the 119–189×.

## Files touched
- `runs/i012_rar_s_requirement.py` (script, 22/22 checks, exit 0)
- `results/I012_rar_s_requirement.md` (this file)
- `LEDGER.md` (one row appended)
- read-only: `real_research/rar_framework_a0_mlfit.py`, `ai_slop/website/public/data/rar_real_sparc.json`,
  `real_research/data/sparc_data/*_rotmod.dat`
