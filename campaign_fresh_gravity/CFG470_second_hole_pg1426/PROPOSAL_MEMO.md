# CFG470 feasibility memo: PG 1426+015 and the best second hole (HS 0749+1943)

A file in the lane only. Nothing has been submitted and nobody has been contacted. Every fraction comes from `cfg470_second_hole.py` (`.out` / `_results.json`). "frac" means the share of the light end (2.01-4.35e-20 eV) excluded by CFG367's `mass_range`/`excluded` at the stated 1-sigma fractional mass error e and spin lower edge a.

## Bottom line

The conditions behind CFG444's 34% / 56% for PG 1426+015 are a mass to ±10% and a robust spin edge of at least 0.9 / 0.98. **No GRAVITY BLR mass has yet reached that precision, and W25's own systematic floor puts both spin edges out of reach.** A realistic program gives PG 1426+015 about 0-9% of the light end, and adding HS 0749+1943 does not change that. The light end stays open.

## 1. Mass: what GRAVITY(+) has achieved

Source: CFG444 `data/gravity_masses.csv`, read from the papers.

| target | method | log M error (dex) | about ±% |
|---|---|---|---|
| NGC 3783 | SARM II (GRAVITY 2021 + RM) | +0.07 / -0.05 | +17 / -11 |
| Mrk 509 | GRAVITY BLR model | +0.06 / -0.23 | +15 / -41 |
| 3C 273 | GRAVITY 2018 | 2.6 ± 1.1e8 | ±42 |
| J0529-4351 (z = 4) | GRAVITY+ BLR | +0.11 / -0.13, statistical only | +29 / -26 |
| J0920+0657 (z = 2.3) | GRAVITY+ BLR | +0.27 / -0.28, including 0.16 systematic | +86 / -48 |

- ±10% is 0.04 dex. No GRAVITY BLR mass has reached it on either side.
- The best case is SARM on a low-z Seyfert, about 0.06 dex (e ≈ 0.15). PG 1426+015 already has an RM lag (Kaspi+00 / Peterson+04), so SARM is the natural route. A new RM campaign would help, since the old lag carries +0.11/-0.16 dex.
- A typical outcome is 0.1-0.2 dex (e ≈ 0.25-0.5). Both levels are ESTIMATES based on the precedents above.
- K = 11.1 for PG 1426+015 (2MASS, including the host). This lane did not check that against current GRAVITY/GRAVITY+ fringe-tracking limits. Whoever writes the proposal must.

## 2. Spin: what broadband XMM+NuSTAR can give

What W25 used: good exposures of NuSTAR 105 ks and pn 71 ks (MOS 99/101 ks).
- The archive also holds an earlier 32 ks NuSTAR pointing and two short 2001 XMM pointings, which W25 did not use.

W25's published spin constraints depend on how the soft excess is modelled:

| soft-excess treatment | spin |
|---|---|
| Relativistic reflection, xillver-based | a* = 0.95 ± 0.01 |
| Relativistic reflection, reflionx-based | a* = 0.77 +0.06 / -0.08 |
| Hard band only, no soft-excess assumption | a* ≳ -0.15 (the authors: essentially all prograde spins) |
| Warm corona (Mallick+25) | 0.3-0.93 |

W25 also quote a systematic of Δa* ~ 0.1 for moderate-to-high spins.

**ESTIMATE of the exposure needed** (labelled; computed in the script):
- Assume the hard-band Δχ² scales with exposure and with (Δr_isco)².
- Moving the 90% lower edge from -0.15 to 0.9 (true a = 0.998) then needs about 23× W25's exposure: **NuSTAR ~2.5 Ms and pn ~1.7 Ms of good time.**
- This is an order-of-magnitude scaling, not a simulation. A fakeit study with W25's best-fit models would replace it.

**The systematic floor matters more than the exposure:**
- With Δa* ~ 0.1, a robust edge is at most a_true - 0.1. That gives 0.85 for a_true = 0.95 and 0.898 for a_true = 0.998.
- **An edge of 0.98 is not reachable, and 0.9 is reachable only if the systematic shrinks below 0.1.** More exposure does not remove the soft-excess model dependence.

## 3. What the decider grid then gives (PG 1426+015 alone)

| e | a ≥ 0.85* | a ≥ 0.89* | a ≥ 0.9 | a ≥ 0.95 | a ≥ 0.98 |
|---|---|---|---|---|---|
| 0.05 | 0.400 | 0.540 | 0.580 | 0.670 | 0.695 |
| 0.10 | 0.160 | 0.300 | 0.335 | 0.535 | 0.565 |
| 0.15 | 0.000 | 0.050 | 0.090 | 0.305 | 0.415 |
| 0.20 | 0.000 | 0.000 | 0.000 | 0.035 | 0.220 |
| 0.30 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

\*Columns marked * are departure D3: edges set by W25's systematic. At a ≥ 0.7 the fraction is 0 for every e.

- Best case at demonstrated precision (e = 0.15, edge 0.89-0.9): **5-9%**.
- Typical case (e ≥ 0.2): **0%**.
- CFG444's 34% / 56% needs e = 0.10 *and* edges of 0.9 / 0.98, both beyond demonstrated capability.

## 4. Second hole: HS 0749+1943 (best-ranked in part A)

| property | value |
|---|---|
| catalogue (BAT 394) | z = 0.117; dec +19.6; Sy1 |
| mass, broad Hα (MR22) | log M 9.16 (1.45e9) |
| mass, Hβ / Koss22 adopted | log M 9.29 |
| Eddington ratio | λ ≈ 0.019 (Koss22 log λ = -1.94) |
| GRAVITY lines | Brγ and Paα both in K |
| K magnitude (2MASS) | 12.9, 1.8 mag fainter than PG 1426+015 |
| X-ray | BAT 1.7e-11 cgs (comparable to PG 1426+015); a 20 ks NuSTAR exposure is accepted but not yet archived; no XMM |

**Mass.**
- There is no RM lag, so SARM is not available without a multi-year RM campaign.
- A GRAVITY-only BLR model follows the J0529/J0920 precedent: 0.11-0.28 dex, so e ≳ 0.3, which gives **0%** at any spin edge.
- Its virial mass is uncertain by about 0.3 dex (Hα and Hβ differ by 0.13 dex). The chance that its true mass lands where the pair closes is P(close) ≈ 0.10 even at ±10% and a ≥ 0.98.

**Spin.** It starts from no X-ray spectrum, at a flux similar to PG 1426+015's, so the same exposure scale and systematic floor apply.

**Pair exclusion with PG 1426+015 (both at e):**

| e | a ≥ 0.89* | a ≥ 0.9 | a ≥ 0.95 | a ≥ 0.98 |
|---|---|---|---|---|
| 0.05 | 0.855 | 0.930 | 1.000 | 1.000 |
| 0.10 | 0.505 | 0.570 | 0.960 | 1.000 |
| 0.15 | 0.050 | 0.090 | 0.525 | 0.820 |
| 0.20 | 0.000 | 0.000 | 0.035 | 0.360 |
| 0.30 | 0.000 | 0.000 | 0.000 | 0.000 |

- The pair would close the light end only at e ≤ 0.10 with edges ≥ 0.98, or at e = 0.05 with edges ≥ 0.95.
- With demonstrated precision and the systematic floor, it adds nothing beyond PG 1426+015's 5-9%.

**Alternative.** 1RXS J084521.7-353048 also closes at its catalogue mass. It has z = 0.137, dec -35.5 (better placed for VLTI), K = 12.5 and 11 ks of archived NuSTAR. Its Hα and Hβ masses differ by 0.24 dex (9.17 vs 8.93), and the same walls apply.

## 5. What would change this

- A GRAVITY(+) BLR mass at ≤ 0.04 dex. No precedent exists.
- A spin method whose systematic is well below 0.1 near maximal spin, independent of the soft excess. The hard band alone needs Ms-class NuSTAR exposures (ESTIMATE). Whether XRISM or future missions change this was not assessed here.

Scope: a gravity-only bound on where the field's mass can be. It detects nothing. κ = ½ is fitted. The cold-fluid amount stays free. No dark-matter particle species is claimed, and the theory is not closed.
