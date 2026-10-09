# CFG531: is the KiDS inner-bin deficit the same shortfall as the SLUGGS centrals' residual? FOOTING-DEPENDENT: canonical SHARED SHORTFALL (weak, kpc-only overlap), alt EXPLAINED BY (a) a +0.10 dex stellar-mass shift. Mechanism NONE

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (750fa1f55).
- **Scripts:**
  - `cfg531_kids.py`: the KiDS arm. It execs CFG529's scorer read-only up to its controls. It rebuilds LAW_RTA own tables (cached in `_external_data/cfg531_work/`, not committed); the first run took about 27 min. Checks: 3/3 main, 6/7 MUTATE (MU3 FAILS and is kept).
  - `cfg531_sluggs.py`: the SLUGGS arm. It execs CFG528b read-only. Checks: 2/2 main, 3/3 MUTATE.
  - `cfg531_verdict.py`: applies the frozen ladder to the two JSONs.
- **Settings:**
  - κ = ½ is FITTED. The footings 9.3603e-11 and 1.1312e-10 are never pooled. The kernel is ν_mono.
  - The cold energy's mass is still required.
  - Nothing was downloaded. This is not "theory closed".
- **Numbers** come from `cfg531_*_results*.json`. Pairs are canonical / alt.

## The common quantity
ε = ΔM(<r)/M_pred(<r), the extra enclosed mass over the law plus baryons (own profile only).
- **KiDS:** ε is the GLS amplitude of the stacked own law profile, measured in the validated f30 environment (CFG529, constructions A and B).
- **SLUGGS:** ε = 10^(2·offset) − 1. This is exact, because Jeans is linear in g.

| | radius | r/r_M | log M* | environment | ε canonical | ε alt |
|---|---|---|---|---|---|---|
| KiDS K-in (bins 12–14) | 52–98 kpc (16–84%), mean 74 | 4.3–10.1 / 4.8–11.2 | 10.72 (weighted) | isolated (f30) | **+0.342 ± 0.157 (2.2σ)** | +0.231 ± 0.144 (1.6σ) |
| KiDS K-mid (9–11) | 119–228 kpc | 10–24 | 10.71 | isolated | +0.521 ± 0.148 (3.5σ) | +0.389 ± 0.135 (2.9σ) |
| KiDS K-out (6–8) | 279–534 kpc | 24–56 | 10.71 | isolated | +0.144 ± 0.179 | +0.042 ± 0.163 |
| KiDS K9 (A; B the same to 0.002) | 193–527 kpc | 4.3–56 | 10.71 | isolated | **+0.385 ± 0.094 (4.1σ)** | **+0.265 ± 0.086 (3.1σ)** |
| SLUGGS J class (4 centrals) | 8–109 kpc (outer GC bins) | 0.3–4.2 / 0.35–4.7 | 11.46–11.62 | group/cluster centrals | **+0.398 ± 0.132 (3.0σ)** | +0.298 ± 0.123 (2.4σ) |

The SLUGGS J class has these variants:
- With a 0.05 dex systematic per galaxy: +0.40 ± 0.21 (1.9σ) / +0.30 ± 0.19 (1.5σ).
- Three galaxies, without NGC 4374: +0.79 ± 0.10 / +0.66 ± 0.09.
- Row M own (not the joint best case): +1.00 / +0.90.

**Overlap.**
- **kpc: yes.** KiDS K-in sits inside the SLUGGS outer-bin range.
- **r/r_M: no.** KiDS starts at 4.3 / 4.8 r_M; SLUGGS ends at 4.2 / 4.7.
- **M\*: no.** The f30 95th percentile is 10.95; the lightest SLUGGS central is 11.46.
- **Environment:** different (isolated lenses against group/cluster centrals).

**Amplitude agreement** (frozen: K-in against the J class): Z = −0.27 / −0.36 in both constructions. It passes, but the errors are large: 2σ_comb ≈ 0.41 / 0.38.

## Alternatives
**(a) Stellar-mass scale / IMF** (environment held at CFG529's validated term)

ε(K9) for each shift, construction A (B within 0.002):

| shift | canonical | alt |
|---|---|---|
| 0 | +0.385 (4.1σ) | +0.265 (3.1σ) |
| +0.05 | +0.315 | +0.202 |
| +0.10 | +0.248 | **+0.141 (1.8σ, law χ² p 0.59)** |
| +0.15 | +0.183 (2.3σ) | +0.082 (1.1σ) |
| +0.20 | +0.120 (1.6σ) | +0.025 |
| IMF (rising with M\*, PROVISIONAL) | +0.230 (2.8σ) | +0.125 (1.6σ) |
| IMF on early types only | +0.273 (3.2σ) | +0.163 (2.1σ) |

- **δ_close** (where ε(K9) reaches 0): **0.30 / 0.22** dex. For K-in alone it is 0.26 / 0.19.
- **Frozen rule** (an allowed shift ≤ 0.15 that brings |Z| < 2 and p > 0.01 in both constructions):
  - canonical: none, so not explained;
  - alt: +0.10, +0.15 and IMF all qualify, so **EXPLAINED BY (a)**.
- The reported variant with E and the stripping re-evaluated at the shifted M\* differs little (+0.15: ε 0.205 / 0.102).
- **The same shift does not help SLUGGS.** On the JAM-law ceiling, +0.05 dex moves the offsets by only −0.010 to −0.015 dex. Already at +0.10 the shift is INADMISSIBLE in all four centrals: the inner JAM excess is 0.075–0.088 dex, above the 0.06 limit. The IMF row is inadmissible too.

**(b) Stripping / satellite term.** ε(K9) under each variant:

| variant | canonical | alt | LCDM χ² on f30 |
|---|---|---|---|
| S-off | +0.310 (3.5σ) | +0.196 (2.4σ) | 26.6, p 0.03 |
| S-half | +0.347 (3.8σ) | +0.230 (2.8σ) | — |
| S-502, CFG502 environment (A) | +0.360 (4.1σ) | +0.242 (3.0σ) | 18.3 |
| zero leakage (reported) | +0.537 (6.1σ) | +0.405 (5.0σ) | — |

- Stripping lowers the law model by only 0.04–0.08 in ε, so the deficit does not depend on it.
- The frozen reading is **not DEPENDS ON (b)**.

**(c) Early vs late types.** ε(K9) per class:

| class | canonical | alt |
|---|---|---|
| early | **+0.832 ± 0.127 (6.5σ)** | +0.676 (5.8σ) |
| late | **−0.313 ± 0.124 (−2.5σ)** | −0.373 (−3.3σ) |

- Late types sit at an *excess* (negative ε), not at zero.
- The difference is +1.15 / +1.05, at 6.4σ.
- The frozen reading is MIXED/UNRESOLVED, because late is not consistent with 0.
- **Mass tertiles:** ε(K-in) is −0.65 (log M* 10.33), +0.48 (10.70), +0.60 (10.90), canonical. **The deficit grows with stellar mass** and changes sign in the lowest tertile.
- **MU3 (below)** shows that most of the early/late difference follows the M_gal distribution, not the type label.

**(d) Kernel (report only).** a0 is set by CFG468's SPARC fit.
- **ν_simple:** ε(K9) is +0.389 / +0.269. SLUGGS J moves by about +0.02 in ε (+0.42 / +0.32).
- **ν_standard:** ε(K9) is +0.291 / +0.175 with T-free and +0.225 / +0.115 with T-fix. SLUGGS J is +0.31 / +0.19 with T-fix.
- **Both kernels fail SPARC** (CFG468: Δχ² +12.8 / −7.0 and +242 / +408). No kernel removes both shortfalls while passing SPARC.

## Mechanism (derived, no knobs): NONE
- **The bound.** M_law(<r) = ν(G M_b(<r)/r²a0) M_b(<r) increases with M_b(<r). So a fixed baryon mass, however it is redistributed, can never exceed the point-mass law.
- **KiDS is already at that bound.** The KiDS own profile is the point mass, so contraction (M-a) adds 0.
- **M-b, extended baryons** (Hernquist with a = 3 kpc) moves the wrong way: ε(K-in) rises by +0.092 / +0.084.
- **M-c, census edge:** it removes 0.0001 / 0.0002 in K-in and never binds for SLUGGS (r_edge 475–581 kpc against R_out ≤ 109 kpc).
- **SLUGGS, maximal-contraction upper bound** (stars collapsed to a point): ε supplied is +0.10 to +0.18 per galaxy, 37% / 47% of the J class need. That is unphysical as a limit and below the 50% rule, and it gives 0 for KiDS.
- **Template (not derived): missing hot CGM baryons.**
  - KiDS K-in needs (10^0.26 − 1) ≈ 0.8 / 0.55 × M* of extra baryons inside about 100 kpc. Recalled hot-CGM masses for L* galaxies are about ≤0.1 M* there (PROVISIONAL).
  - SLUGGS needs ×17–268 the measured gas (CFG528).
  - Neither closes.

## Verdict (frozen ladder)
- **canonical: SHARED SHORTFALL.** KS, SS, RG and AG are all true, and (a), (b) and (d) do not explain it.
- **alt: EXPLAINED BY (a).** A +0.10 dex M* shift closes KiDS. The same shift is inadmissible for SLUGGS.
- **Headline: FOOTING-DEPENDENT.** Mechanism NONE.

**How solid the canonical label is** (written after the results; no verdict weight). The label is weak:
1. The two data sets meet only in kpc. There is no overlap in r/r_M, M\* (0.5 dex gap) or environment.
2. KiDS K-in is only 2.2σ. The K9 significance comes mostly from 107–189 kpc, beyond the SLUGGS radii.
3. Amplitude agreement is easy to pass with errors of ±0.13–0.16.
4. SLUGGS falls to 1.9σ with the 0.05 dex per-galaxy systematic.
5. The KiDS deficit depends on mass and type. It is negative for late types and for the lowest-mass tertile, which is what a stellar-mass-scale or mass-to-halo trend does, not a universal extra mass at fixed radius. δ_close is 0.30 dex (canonical), just above the frozen "allowed" 0.15–0.20.

What the two data sets share is the sign and a similar ε ≈ 0.3–0.4 at 50–100 kpc around massive early-type-dominated systems. They do not share a scaled radius, a mass range or an environment, and the KiDS part tracks stellar mass.

## Controls and MUTATE
**Controls:**
- K1: CFG529's f30 LAW_RTA / LCDM χ² and inner-9 χ² are reproduced exactly (A and B, both footings).
- K2: the rebuilt LAW_RTA tables equal CFG503's (0.0 rel); K2b: the mixing path is exact.
- K3: CFG528b's row M own is reproduced to 1e-6.
- K4: the kernel swap with ν_mono is an exact identity.

**MUTATE:**
- **MU1 PASS:** a uniform ε = 0.4 is recovered to 3e-16.
- **MU2 PASS:** the isothermal injection is recovered, e.g. K9 +0.059 against a true +0.058.
  - The injected amplitude came out at about 0.05, smaller than the about 0.4 intended. So the test checks the shape at small amplitude, where the 0.02 floor is generous.
  - The relative agreement is 0–4% in K-in, K-mid and K9 (K-out +10%).
- **MU3 FAIL** (kept). Type labels shuffled within (M_gal, z) groups still give an early − late K9 difference of Z +3.96 in all four cells.
  - The shuffled "early" ε is +0.705 / +0.558 and the shuffled "late" ε is −0.020 / −0.105.
  - So about two-thirds of the real split (+1.15) comes from the different M_gal distribution of the two classes, i.e. the mass dependence, and about a third from the type itself at fixed M_gal.
  - The tooth was meant to vanish. Its failure is itself informative, and (c) must be read with it.
- **MU4 PASS:** a null mock gives KS false.
- **MU5 PASS:** g × 1.5 shifts every offset by exactly 0.5 log10 1.5 and returns ε = 0.5 (1e-15).

## Dated disclosures (2026-10-09)
1. **MU3 print.** After the first MUTATE run, a diagnostic print of the shuffled per-class ε was added to MU3 and MUTATE was re-run. The criterion and the Z values are unchanged.
2. **MU2 amplitude.** The injected profile's amplitude relative to the law, about 0.05, was not checked before the freeze.
3. **SLUGGS kernel row.** The kernel shift is computed on row M own and added to J, as declared. IMF and shift rows for SLUGGS are on row M own.
4. **IMF2 approximation.** IMF2 uses the group-mean log M* (the groups are binned in M_gal) for the early lenses.
5. **(c) reading.** The frozen ladder does not use (c)'s MIXED reading. The interpretive paragraph above was written after the results and carries no verdict weight.

## Run
```
nice -n 10 python3 cfg531_kids.py ; CFG531_MUTATE=1 nice -n 10 python3 cfg531_kids.py
nice -n 10 python3 cfg531_sluggs.py ; CFG531_MUTATE=1 nice -n 10 python3 cfg531_sluggs.py
python3 cfg531_verdict.py
```

κ = ½ is fitted. The cold energy's mass is still required. This is not "theory closed".
