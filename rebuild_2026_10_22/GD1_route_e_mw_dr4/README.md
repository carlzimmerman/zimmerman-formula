# GD1_route_e_mw_dr4: the flagship's Milky Way for Gaia DR4. Under OS1 the Sun's orbital speed is 200–210 km/s, 4–6σ below the measurement

> **AMENDMENT A1 (2026-10-26, post-result; correction).** The first run below graded the **X38 core (q = 0, Σ = Σ_a₀)**.
> The flagship's cold sector is **OS1**: Σ = Σ_a₀ (σ/σ_ref)^q_f, with σ = V_last/√2, σ_ref = 70.50 km/s and
> q_f = 0.892 / 0.748. The first headline (V_c(R₀) 190 km/s, z −8.5) is therefore **not the flagship's number**. It is
> kept below, labelled as the q = 0 reading. The flagship's numbers are in A1's tables. Script: `--os1 VLAST`.

## A1. The flagship (OS1) Milky Way

The Milky Way's V_last is bracketed between Ou+24's last point, 172.98 km/s at 27.3 kpc (SC1's literal definition), and
V_c(R₀) = 229.05 km/s. Then Σ/Σ_a₀ = 1.635 / 1.510 (V_last 173) and 2.100 / 1.863 (V_last 229), for canonical / alt.

| quantity (s = 1, bg A; band = stellar band) | canonical V_last 173 | canonical V_last 229 | alt V_last 173 | alt V_last 229 |
|---|---|---|---|---|
| V_c(R₀) [km/s] | **200.3** (192.8–207.6) | **208.0** (200.8–215.0) | **203.5** (196.1–210.7) | **210.5** (203.3–217.4) |
| z vs Eilers 229.05 ± 4.65 | **−6.2** | **−4.5** | **−5.5** | **−4.0** |
| K_z(R₀, 1.1)/2πG [M☉ pc⁻²] | 67.4 (62.1–72.6) | 69.3 (64.0–74.6) | 68.2 (62.9–73.4) | 69.9 (64.7–75.2) |
| z vs Bovy & Rix 66.4 ± 2.2 | +0.4 | +1.3 | +0.8 | +1.6 |
| V_c(20 kpc) | 194.3 | 205.4 | 199.2 | 208.5 |
| dlnV/dlnR 15–27.5 | −0.013 | −0.026 | −0.018 | −0.031 |
| local dark density [GeV cm⁻³] | 0.224 | 0.290 | 0.252 | 0.311 |
| χ² vs Ou+24 (37 points) | 441 | 194 | 317 | 148 |
| halo pull cap at R₀ (0.2545 × 2πGΣ) [km/s] | 98.8 | 112.0 | 104.4 | 115.9 |
| baryons needed at R₀ to reach Eilers | ×1.36 | ×1.27 | ×1.32 | ×1.24 |

The structural cap still holds: a Burkert core pulls at most 0.2545 × 2πGΣ. OS1 raises Σ for the Milky Way, but only to
1.5–2.1 Σ_a₀. Reaching Eilers with McMillan's baryons needs about 3.5 Σ_a₀, which under OS1 means σ ≈ 290 km/s
(V_last ≈ 410 km/s). K_z still matches. The miss is the orbital speed alone.

### A1b. The native lift, T7's thermalised core, cannot reach R₀ (`gd1b_thermal_radius.py`)

The core law is LN1's T7: Γt = 1 at the core, with s·v = Kσ^(1−n) and Kt = 9σ_ref^(1+n)/(4πG Σ_a₀²) (no free number;
t cancels). The native way to deepen a core in a baryon-dominated galaxy is for the thermalised region (Γt ≥ 1) to relax
isothermally in the **total** potential. Mass inside r₁ is conserved and the halo outside r₁ is untouched, so the halo's
pull at R₀ can move only if r₁ > R₀.

| case | ρ₀ (OS1 Burkert) | ρ at Γt = 1 [M☉ pc⁻³] | r₁ | Γt at R₀ | V_c(R₀) upper bound | Γt multiplier needed |
|---|---|---|---|---|---|---|
| canonical, V_last 173 | 0.0123 | 0.0123 | 0.10 kpc | 0.48 | 200.3 (unchanged) | ×3.1 |
| alt, V_last 173 | 0.0148 | 0.0153 | 0 (Γt < 1 everywhere) | 0.43 | 203.5 | ×3.3 |
| canonical, V_last 229 | 0.0187 | 0.0115 | 4.78 kpc | 0.66 | 208.0 | ×2.1 |
| alt, V_last 229 | 0.0209 | 0.0133 | 4.37 kpc | 0.62 | 210.5 | ×2.1 |

**Reading.** The thermal region is at most 4.8 kpc, inside R₀ = 8.1 kpc, so the self-coupled response cannot change
V_c(R₀). The "upper bound" assumes all of M(<r₁) is moved inside R₀, which no relaxation does. Even that bound needs
Γt larger by ×2.1–3.3 than T7 gives, which is one new number (in K or t). It is not native. The other native levers
in the record are also closed:
- X43's collapse branch is inactive at lgM200 11.93.
- The halo's own σ (DW1 M3) lowers Σ.
- X39 contraction breaks SPARC.
- An isothermal core shape (IC1) breaks 7 cluster cells.

**No native core rule in the record lifts the Milky Way's halo pull at R₀.** The only open lever is the baryons. X5's
short-disc corner (R_d 1.9–2.3 kpc, light local column) puts more mass inside R₀ at fixed K_z. That is the corner the law
(v3) also needs, and route E has not been run there. Checks: K5 (T7 ρ₁ identity) ×4 PASS; `--mutate` FAILS K5.

---

## Original run (X38 core, q = 0): superseded for the flagship, kept for the record

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

OS1 runs: `python3 gd1_route_e_mw.py --os1 172.98` and `--os1 229.05`; then `python3 gd1b_thermal_radius.py` (+ `--mutate`).
