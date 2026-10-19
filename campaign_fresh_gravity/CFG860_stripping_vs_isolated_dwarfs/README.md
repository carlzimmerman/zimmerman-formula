# CFG860: is the dwarf excess tied to gas lost by stripping? Plus the Earth bound

**Label: NOT GAS (canonical, graded). Isolated dwarfs carry the excess too, with or without gas. Earth bound: NO LAB CHANNEL.**

- **Criteria:** `FROZEN_CRITERIA.md` (219d4d5dc), committed alone before any script. Block CFG860–869.
- **Scripts:** `cfg860.py` (Parts A and R, K1) → `cfg860.out`, `cfg860_results.json`; `CFG860_MUTATE=1` → `cfg860_MUTATE.out`,
  `cfg860_results_MUTATE.json`. `cfg860_earth_bound.py` (Part E, K2) → `cfg860_earth_bound.out`, `cfg860_earth_bound.json`.
  One process each, a few seconds, numpy only, nothing downloaded. JSON is deterministic.
- **Settings:** κ = ½ FITTED; footings never pooled; Δ is CFG852's `delta_ups2` (Υ_V = 2, Wolf estimator, kernel ν_e).

## The question

CFG846 found the low-g excess only in gas-poor systems. Winds leave a metallicity mark, and CFG852 saw no link to that mark.
Stripping by a host removes gas without one. So: at matched g_bar, do stripped satellites (S) sit above isolated dwarfs that
lost their gas without a host (I0) and isolated dwarfs that kept it (IG)?

## Result (canonical a0 = 9.3603e-11, graded)

Fit Δ = a + b (log g_bar + 12.5) + c0 [I0] + cG [IG]; 2000 stratified bootstrap draws, seed 860.

| quantity | value |
|---|---|
| N (S / I0 / IG) | 69 / 6 / 5 |
| slope b | −0.233 per dex |
| **c0** (isolated gas-free − satellites) | **−0.150 ± 0.122** (1.2σ) |
| **cG** (isolated gas-bearing − satellites) | **−0.064 ± 0.093** (0.7σ) |
| a + c0 (isolated gas-free over the law at g_bar 10⁻¹²·⁵) | +0.285 ± 0.108 (2.6σ) |
| a + cG (isolated gas-bearing over the law) | +0.370 ± 0.073 (5.1σ) |
| group means (raw) | S +0.507 at log g_bar −12.81; I0 +0.256 at −12.38; IG +0.235 at −11.92 |

- **I0:** Eridanus II, Perseus I, Andromeda XXVIII, Andromeda XVIII, Cetus, Tucana.
- **IG:** Leo T, Antlia B, Aquarius, Phoenix, UGC 4879.
- **SG** (satellites with HI, not graded): LGS 3, NGC 185, NGC 205. Offset from the graded line −0.08 / +0.03 / +0.19, mean +0.05.
- No isolated dwarf lacked an HI entry, so none was left out on that rule.

**CLASS: NOT GAS.** Neither isolated group differs from the satellites by 2σ, and both sit above the law by more than 2σ. Every faint
dwarf carries the excess, whether it has a host or gas.

What this means for the record: H-EX (the cold share of expelled baryons becomes free; CFG809) predicts the excess only where gas
was lost. Gas-bearing isolated dwarfs carry it too, so gas loss does not set it. CFG843 found MW = M31 satellites (SAME), so the host
does not set it either. The excess looks like a property of faint pressure-supported dwarfs wherever they sit. It could also be a
systematic they all share (binaries, small stellar samples, Υ), which this lane does not correct.

Limits: the isolated groups are small (6 and 5). Both point offsets are negative. The base 2σ range of c0 reaches −0.39 dex, and the restricted fit gives
c0 −0.24 ± 0.15, so an environmental part of a few tenths of a dex is not excluded. Distance-only isolation cannot rule out backsplash dwarfs. Eridanus II,
Perseus I and Andromeda XXVIII lie only 340–372 kpc from a host. HI non-detections are limits of uneven depth.

## Controls

- **K1 PASS.** Draco's Δ equals CFG852's `delta_ups2` exactly (both +0.632219040953, difference 0). CFG852's constants and function are taken from its
  source with `ast`, without running its I/O. The pooled fit (c0 = cG = 0) slope matches numpy.polyfit (−0.248420984).
- **MUTATE bites 2/2.** (a) −0.4 dex on every I0 and IG Δ gives c0 −0.550 ± 0.122 and cG −0.464 ± 0.093, so it classes **STRIPPING**.
  (b) −0.4 dex on IG only gives c0 −0.150 and cG −0.464, so it classes **GAS LOSS, ANY ROUTE**. Both are as required.
- **K2 PASS** (Part E). At y = 1e4 the simple-kernel f is 9.9990e-5 against 1/y = 1e-4, a relative difference of 1.0e-4 (tolerance 1e-3).

## Reported variants (not graded)

| variant | canonical | alt (a0 1.1312e-10) |
|---|---|---|
| base | NOT GAS | NOT GAS (c0 −0.150 ± 0.122, cG −0.064 ± 0.093; a+c0 +0.245 ± 0.108, a+cG +0.331 ± 0.073) |
| isolation cut 350 kpc (Perseus I left out) | NOT GAS (c0 −0.077 ± 0.125) | NOT GAS |
| isolation cut 400 kpc (Eri II, And XXVIII, Per I left out; N(I0) 3) | NOT DIAGNOSTIC | NOT DIAGNOSTIC |
| Υ_SFH from CFG828 rows (26 dwarfs) | NOT GAS (c0 −0.164 ± 0.121, cG −0.054 ± 0.097) | NOT GAS |
| IG gas bracket, g_bar from (M★ + 1.33 M_HI)/2 | NOT GAS (cG −0.129 ± 0.113) | NOT GAS |
| Antlia B dropped (N(IG) 4) | NOT GAS (cG −0.073 ± 0.105) | NOT GAS |
| log g_bar < −11.9 (N 62/6/4) | NOT GAS (c0 −0.238 ± 0.145, cG −0.151 ± 0.128) | INCONCLUSIVE (a+c0 +0.230 ± 0.116, just under 2σ) |

- **Cetus / Tucana vs CFG838.** With the Υ_SFH rows, Cetus is +0.127 and Tucana +0.168. Both equal CFG838's field values exactly.
  With Υ_V = 2 they are +0.047 and +0.118. The difference (−0.08 and −0.05 dex) comes from Υ and from CFG828's σ source.

## Disclosed decisions (fixed in code before the first run)

1. **Wider isolation cuts.** S stays at < 300 kpc, as the frozen satellite definition says. Dwarfs between 300 kpc and the wider
   cut are left out and listed. They are not moved into S.
2. **Υ_SFH variant.** CFG828's footing-matched rows (`canonical|nu_e`, `alt|nu_e`) replace Δ and g_bar for the 26 dwarfs that have
   them. Those rows also carry CFG824's σ, not LVD's. Every other dwarf keeps Υ_V = 2.
3. **SG offset.** This is the mean residual of the SG dwarfs from the graded line a + b(log g_bar + 12.5).
4. **Bootstrap.** Each fit, every variant included, starts a fresh generator at seed 860. σ is the standard deviation of the draws
   (ddof 0).
5. Andromeda XXII (LVD host M33) lies 215 kpc from M31, so it falls in S by the distance rule. LGS 3, at 292 kpc with HI, falls in SG.
6. **Part E.** L* = 24 pc is used as frozen. CFG820's exact canonical edge is 23.96 pc. That changes (s/L*)² by a factor of 1.004.

No crash and no deviation from the frozen text was needed.

## Part R: isolated red lenses (reported, CFG850 JSON, +0.123 dex red M★ correction)

| footing | A_red | A_blue | split |
|---|---|---|---|
| canonical | 1.451 (+0.162 dex) | 1.016 (+0.007 dex) | 4.0σ |
| alt | 1.324 (+0.122 dex) | 0.928 (−0.033 dex) | 4.0σ |

Isolated red lenses lost their gas without being satellites, and they still sit above the law. This agrees with "not stripping".
**Scale caveat:** lensing probes 30–300 kpc, while the dwarf dispersions probe r_1/2 ≈ 0.1–1 kpc. CFG851 found no single law across
the two: dwarfs carry about 3× more.

## How dwarfs and galaxies lose gas, and what the record says about each route becoming cold energy

The committed action conserves cold mass (CFG793). No route can *make* cold energy. A route can only set free a share
(H-EX, CFG809) or bind one by a rule not yet on the record.

| route | lane(s) | record |
|---|---|---|
| winds / outflows | CFG852 | **NO SIGNAL**. The excess does not track the metallicity deficit (partial ρ −0.11 / −0.02; power shown by injection). |
| stripping by a host (ram pressure, tides on gas) | **CFG860** | **NOT GAS**. Isolated dwarfs, gas-free or gas-bearing, match the satellites within 2σ. |
| reionization photo-evaporation | CFG782 | **DEAD** (it flags about half of M31's satellites too). Removed in THEORY_CANONICAL_2026-10-16. |
| hot-gas escape (hidden gas around early types) | CFG580–582 | Closed. Hot gas cools too fast (580+581); cool CGM is ×6 short (582). The early-type shortfall stands as a limit of the law. |
| freed cold share from expelled gas, placed by the rule | CFG822 | Improves dSphs negligibly (χ² 57.8 vs 58.4). The free share sits too far out, so dwarfs need bound cold mass inside r_1/2. |
| capture of host cold energy by satellites | CFG842 | Fails. The Liouville ceiling is 1.5e-8 to 1.8e-5 of the need. |
| tides, present and past | CFG838 / CFG839 | **NO TIDAL SIGNAL** (ρ −0.00) and **NO SIGNAL** at pericentre (ρ +0.08). |
| internal consumption / quenching (red isolated lenses) | CFG846 / CFG850 | Red lenses sit above the law at low g (split 4.0σ after the M★ correction). This is a different scale from the dwarfs (CFG851). |

No gas-loss route examined so far ties to the dwarf excess. The common factor left is being a faint pressure-supported dwarf, or a
systematic that all such dwarfs share.

## Earth: can removing gas here set cold energy free, or make it?

- **E1, conversion: none.** The action conserves cold mass, η = 0 exactly (CFG793). Removing gas cannot make cold energy.
- **E2, release bound without stiffness** (cold share tied to gas in Earth's field, g = 9.81 m/s², f = ν(g/a0) − 1 per kg of gas):
  - simple kernel (most generous): **9.54e-12** canonical, **1.15e-11** alt (= a0/g)
  - ν_e: **10^−140596** canonical, **10^−127894** alt
- **E3, with stiffness** (E2 × (s/L*)², L* = 24 pc, simple kernel; the ν_e values are about 10^−140620 canonical and
  10^−127920 alt):

  | s | canonical | alt |
  |---|---|---|
  | 1 m (lab vessel) | 1.7e-47 | 2.1e-47 |
  | 1 km (plant) | 1.7e-41 | 2.1e-41 |
  | 6.371e6 m (Earth radius: the atmosphere) | 7.1e-34 | 8.5e-34 |

- **E4, natural loss.** Hydrogen escapes at about 3 kg/s, roughly 9.5e7 kg/yr (an order-of-magnitude literature value, provisional).
  The freed cold mass per year is at most **9.0e-4 kg** (canonical) or 1.1e-3 kg (alt) from E2 simple. With stiffness at Earth's
  radius it is **6.7e-26 kg** (canonical) or 8.1e-26 kg (alt). Under ν_e the amount is effectively zero.
- **E5 reference.** 1e-9 kg per kg is about the best mass-comparator resolution. The most generous E2 is 1% of that.
- **E6.** The 541.664 / 595.463 GHz line remains the only lab-scale test of the cold sector (CFG797–799):
  - 541.664 GHz: the Herschel/HIFI archive gives a NULL (ε95 1.9e-11; converter window closed ×200; kill line 1e-12 not reached).
  - 595.463 GHz: the frozen run is INCONCLUSIVE (C2 null offsets fail; converter tier excluded 31/31; kill line not tested).
- **E7 (reported).** CFG745's hot-gas term C = k·M_hot (k 2.9–3.6, fitted at galaxy scale, no mechanism) is a tethered amount, not a
  conversion. At s = 1 m it gives 5–7e-36 kg per kg of hot gas.

**CLASS: NO LAB CHANNEL.** E2 with the simple kernel is below 1e-9 kg/kg on both footings. The order of magnitude was estimated in
chat before the freeze, as disclosed. Part E is a bound, not a test against data.

κ = ½ fitted; cold energy mass required; not theory closed.
