# GD1_route_e_mw_dr4: the flagship's Milky Way, for Gaia DR4. The a₀-cored halo cannot hold the Sun's orbit up

κ = ½ FITTED. Footings never pooled. Route E: gravity Newtonian, the galaxy law emergent from cold dark energy halos
Burkert-cored at ρ₀r₀ = a₀/(2πG) (X38; X43's collapse branch is inactive below 10^12.1 / 10^12.4 M☉, and the MW halo is
10^11.93). M200 comes from EM1's committed SPARC relation, borrowed and not refit. The baryons are S3's McMillan 2017 B1
field, recovered from the sealed NFW rival by subtracting its analytic halo. `SEALED_V3_MW_DR4.json` was only read. No
dark-matter particle. Predictions, not results. Not theory closed. Nothing here says the data favour the framework.

**Status: a lane with no frozen criteria.** It computes predictions and reports them against the record's existing MW
targets (X5's Eilers v_c(R₀) and Bovy & Rix K_z; S3's Ou+24 error model). It is not sealed, and no verdict class is
claimed. Sealing a route-E DR4 file is the owner's call.

## Predictions (s = 1; band = the five-value stellar band; background A, B in brackets where it moves)

| quantity | route E canonical | route E alt | v3 sealed (can / alt) | NFW rival (sealed) |
|---|---|---|---|---|
| wide-binary γ_v (any separation) | **1.000** (Newtonian by construction) | 1.000 | screened ≈ 1.000 | 1.000 |
| V_c(R₀) [km/s] | **189.5** (181.5–197.3) | **193.1** (185.2–200.6) | 215.5 / 220.6 | 234.4 |
| V_c(20 kpc) | 173.2 (169.1–177.0) | 181.1 (177.0–185.0) | 196.0 / 203.2 | 207.2 |
| dlnV/dlnR 15–27.5 kpc | −0.020 (−0.033 to −0.007) [B −0.013] | −0.011 (−0.021 to −0.002) [B −0.003] | −0.120 / −0.110 | −0.174 |
| K_z(R₀, 1.1)/2πG [M☉ pc⁻²] | **64.8** (59.5–70.1) | **65.6** (60.4–70.9) | 92.3 / 96.8 | 76.3 |
| ρ_tot(R₀, 0) [M☉ pc⁻³] | 0.111 | 0.111 | 0.166 / 0.174 | 0.116 |
| local dark density [GeV cm⁻³] | 0.125 | 0.158 | phantom 2.22 / 2.55 midplane | 0.338 |
| V_c(60 kpc) | 171.3 | 175.7 | 170.9 / 178.4 | 166.6 |
| azimuthal V_c asymmetry P6 | **0** (no EFE) | 0 | 0.030 at 20 kpc | 0 |
| halo lgM200, r₀ | 11.93, 19.7 kpc | 11.93, 17.3 kpc | n/a | 11.76, c 18.3 |

## Today's data already decide the amplitude (reported; DR3-era targets the record uses)

| | canonical | alt |
|---|---|---|
| v_c(R₀) vs Eilers+19 229.05 ± 4.65 | **z −8.5** | **z −7.8** |
| K_z(R₀) vs Bovy & Rix 66.4 ± 2.2 | z −0.7 | z −0.4 |
| χ² vs Ou+24 (37 points, S3 error model) | **1188** | **872** |
| same χ² for v3 / NFW (context) | 170 / 9.8 | 69 / 9.8 |

**The reason is structural, not a fit.** A Burkert halo with ρ₀r₀ fixed pulls at most **0.2545 × 2πGΣ = 0.2545 a₀**
anywhere, at R ≈ 0.96 r₀, whatever its mass. At R₀ that caps the halo's speed at **77.3 / 84.9 km/s**. McMillan's
baryons give 177.2 km/s there, so reaching Eilers' 229 needs 145 km/s from the halo, about 1.8 × the cap. No M200
rescues it. The collapse branch would need Σ ≈ 3.5 Σ_a₀, which needs halo masses near 10^14 M☉.

**What would have to give.** The baryons would need ×1.44 to ×1.48 at R₀, outside S3's stellar band (×1.105) and X5's
published-prior box. That would drag K_z(R₀) far above Bovy & Rix's 66.4, which route E matches today. Read plainly:
**route E with an a₀-pinned core gets the Sun's vertical pull right and its orbital speed 40 km/s too low.**

**Why SPARC did not show this.** X38 passes SPARC at median Υ 0.77 / 0.60, against the law's 0.52 / 0.44. Free per-galaxy
Υ lets the stars carry the inner pull the capped halo cannot. In the Milky Way, K_z and v_c(R₀) are measured separately,
so that freedom is gone. This lane's reading is that the Milky Way is the hard test of the flagship's core law. It
belongs to today's data, not to DR4.

## What DR4 adds for route E

- **Wide binaries:** γ_v = 1.000, the same as Newton, Cookson/Banik and Saad–Ting, and the screened v3s (X36). DR4
  separates route E from the MOND-class claims (Hernandez ~1.22, Chae √1.60 ≈ 1.26, AQUAL 1.15–1.20). It cannot separate
  route E from ΛCDM.
- **Milky Way:** the route-E curve is flat to slightly rising (slope −0.02 to −0.003), where NFW gives −0.174 and v3 −0.12,
  and its amplitude sits below both. P6 = 0 matches the symmetric NFW rival and differs from v3's EFE asymmetry.
- These are numbers under one baryon model, against DR3 data that already fail the amplitude. They are not a sealed file.

## Limits

- One baryon field (McMillan 2017, stars × s, gas held). X5's short-disc corner was not rerun for route E.
- Spherical Burkert. Flattening redistributes the pull but cannot lift the 0.2545 a₀ cap on the mean radial pull.
- No baryonic contraction (X39 rejected it: it breaks SPARC). No c(M) scatter.
- The Ou+24 χ² uses S3's error model (random ⊕ 3 % to 22 kpc, ⊕ 15 % beyond).

## Checks (`gd1_route_e_mw.out`)

K1 (×5) rebuild S3's sealed NFW slope from the recovered baryons (|Δ| < 2e-3); K2 no halo saturated; K3 the halo raises
K_z; K4 Σ equals X38's 106.88 / 129.16; K5 the solved halo obeys the analytic cap. `--mutate` (Σ × 2) FAILS K5.

## Reproduce

```
OMP_NUM_THREADS=1 nice -n 15 python3 gd1_route_e_mw.py            # gd1_route_e_mw.out, gd1_route_e_mw_results.json
OMP_NUM_THREADS=1 nice -n 15 python3 gd1_route_e_mw.py --mutate   # *_MUTATE; K5 FAILS by design
```
