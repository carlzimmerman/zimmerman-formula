# HG2 FROZEN CRITERIA: MWG1 redone with published hot-gas density laws from full texts

Written 2026-11-12, before any HG2 script and before any gate was evaluated with these profiles.
TEST lane. Adopts nothing. Relabels no other lane. kappa = 1/2 FITTED; not theory closed.

## Question

MWG1 (criteria 9884ea05fd, result 827ed33db9) added hot halo gas to the Milky Way census and found
(1) inside 27 kpc the gas gives only 3 to 16 per cent of what the rotation curve asks for, and (2)
beyond 100 kpc it lifts the line enough to pass the outer data at the record's field 0.01273
(FRAGILE: Salem 2015 fails). MWG1 used abstracts, assumed three of four radial shapes, took Faerman
2017's radius and slope from memory, and left out disc-like hot gas. HG2 replaces every shape and
normalisation with the density law printed in each paper's full text and re-runs both parts, now with
the disc-like components included.

## Sources read (full texts, arXiv PDFs, read 2026-11-12; PROVISIONAL web look-ups)

Every number below was read from the arXiv PDF text (https://arxiv.org/pdf/<id>), at the place given.

| id | paper | density law used (as printed) | parameters | Z assumed | conversion |
|---|---|---|---|---|---|
| MB15 | Miller and Bregman 2015, 1412.3116 | eq. 2: n(r) = n0 rc^3b / r^3b | Table 2, O VIII optically thin: n0 rc^3b = 1.35e-2 cm^-3 kpc^3b, b = 0.50; outer radius 250 kpc (Sec. 5.1) | fit at solar emissivity; masses quoted for 0.3 Zsun (Table 2 note c) | see KA2 |
| MB13 | Miller and Bregman 2013, 1305.2430 | eq. 5: n = n0 (1 + (r/rc)^2)^(-3b/2), plus an ambient n = 1e-5 cm^-3 out to 200 kpc (Sec. 4.1) | Table 2 spherical saturated: n0 = 0.46 cm^-3, rc = 0.35 kpc, b = 0.71 | n is the electron density from an O VII column, eq. 4: Ne proportional to (Z/Zsun)^-1; masses quoted for solar (Sec. 4.2: 2.2e8 inside 18 kpc, 1.2e10 inside 200 kpc) and 0.3 Zsun (abstract: 7.5e8, 3.8e10) | m per electron 1.17 m_p; Z = 0.3 by n / 0.3 |
| S15 | Salem et al. 2015, 1507.07935 | eq. 7: n = n0 rc^3b / r^3b | n(48.2 kpc) = 1.1e-4 cm^-3 (abstract, Table 6); M(<300 kpc) = 2.6e10 (abstract; 2.68e10 Sec. 6.1); n0 rc^3b sampled in [0.005, 0.03] (Fig. 14 caption) | not needed (ram pressure measures total density) | rho = mu m_p n, mu = 0.6 (assumed: mu m_p appears in eq. 11 but no value was found in the text); slope solved from the two printed numbers |
| F17 | Faerman, Sternberg and McKee 2017, 1602.00689 | numerical hydrostatic profile (data file not retrieved); reconstructed as n_H proportional to r^-s through Table 3's n_H(50 to 100 kpc) = 1.3e-4 to 0.83e-4 cm^-3 | r_vir = r_CGM = 250 kpc; Mgas(r_vir) = 1.2e11 (hot 9.4e10 + warm 2.7e10), Table 3 | 0.5 Zsun | mass per H 1.4 m_p (assumed, X = 0.71) |
| F20 | Faerman, Sternberg and McKee 2020, 1909.09169 | Table 1 approximation n_H = 1.3e-5 (r / r_CGM)^-0.93 cm^-3, R0 = 8.5 kpc to r_CGM = 283 kpc, "accurate to within 20%" (Sec. 3.1) | Mgas(258) = 4.6e10, Mgas(283) = 5.5e10 (Table 1) | Z' = 1.0 at R0 to 0.3 at r_CGM | mass per H 1.4 m_p (assumed) |
| B18 | Bregman et al. 2018, 1803.08963 | "beta = 0.5" power law, n proportional to r^-1.5 (Sec. 2.5 summary) | M(<250 kpc) = 2.8e10 after optical-depth corrections; exponential hot disc 1.8e8 (Sec. 2.5) | 0.3 to 1 Zsun (abstract) | normalised to the printed mass |
| K20b | Kaaret et al. 2020, 2011.00126 | modified beta: n = nc (r/rc)^-3b | nc = 0.0044 cm^-3, rc = 2.4 kpc, b = 0.39 (main text and Table, patchiness column); lines of sight to 260 kpc | 0.3 Zsun | m per electron 1.17 m_p |
| L24 | Locatelli et al. 2024, 2310.10715 | combined (b = 0.5) model: eq. 5 halo n = C r^-3b plus eq. 6 disc n = n0 exp(-R/Rh) exp(-abs(z)/zh) | Table 1: C = 4.6e-2 cm^-3 kpc^1.5, n0 = 3.2e-2 cm^-3, Rh = 6.2 kpc, zh = 1.1 kpc; Rout = 350 kpc (Sec. 3.3) | halo Z = 0.1 Zsun (Sec. 3.2), kT 0.15 keV | m per electron 1.17 m_p |
| L24z | same, row "combined+high eps" | same laws | C = 1.36e-2, n0 = 9.4e-3, Rh = 6.2, zh = 1.1 | 0.3 Zsun, kT 0.225 keV | same |

Disc-like components (Part 1, and added to their own paper's halo in Part 2):

| id | source | law and parameters | printed mass |
|---|---|---|---|
| D-L24 | Locatelli combined b = 0.5 | as above | none printed (Fig. 7 only) |
| D-L24d | Locatelli disc-only model, Table 1 | n0 = 1.7e-2, Rh = 8.0, zh = 3.3 (Z = 0.1) | none |
| D-K20e | Kaaret empirical disc in the disc+adiabatic-halo fit | n = n0 S(R) exp(-z/z0), S = 1 for R < 5.5 kpc, exp(-(R - 5.5)/2) beyond; n0 = 0.0081, z0 = 1.60 | 2e7 Msun (text) |
| D-K20x | Kaaret exponential disc model | n0 = 0.012, R0 = 5.4, z0 = 2.8 | none |
| D-N18 | Nakashima et al. 2018, 1806.04832 (extra source) | exponential disc, log n0 = -2.42, R0 = 7.03, z0 = 2.73, solar Z, mu = 0.61 (eq. 11) | 5e7 Msun (eq. 11, abstract) |
| D-B18 | Bregman 2018 | exponential hot disc (Li and Bregman 2017) | 1.8e8 Msun (Sec. 2.5) |

Kaaret's preferred halo (adiabatic NFW gas, 5.5 to 8.6e10 inside 260 kpc) has no printed closed-form
law, so only its beta-model fit (K20b) enters as a halo. F17 has no closed-form law either; F17 is a
reconstruction from printed numbers and is labelled as such.

## Disclosed before freezing (hand numbers, not gates)

- MB15 KA2 by hand: the printed 1.35e-2 at solar, treated as an electron density with 1.17 m_p per
  electron, gives 1.16e9 inside 50 kpc. Scaling the density by (Z/Zsun)^-1 = 1/0.3 gives 3.85e9 and
  4.3e10 inside 250 kpc: the quoted masses. The emission-physics scaling (Z/Zsun)^-1/2 (emission goes
  as n^2 Z) gives 2.1e9, a factor 0.55 lower. MB15 Sec. 5.1 itself states DM proportional to Z^-1,
  the absorption-line convention of MB13 eq. 4. So the paper's masses close only with the Z^-1
  convention. I expect KA2 to pass with that convention and will print the Z^-1/2 masses beside it.
- MB13 by hand: beta part 2.1e9 + ambient 9.7e9 = 1.18e10 inside 200 kpc at solar (quoted 1.2e10).
- F20 by hand: the approximation with 1.4 m_p per H gives 6.2e10 inside 283 kpc (quoted 5.5e10).
- F17 reconstruction by hand: slope s = 0.65; 1.32e11 inside 250 kpc with 1.4 m_p (quoted 1.2e11).
- Kaaret disc law by hand: 1.4e8 Msun (both sides of the plane) against the printed 2e7.
  Nakashima's disc: 9.7e7 (both sides) against the printed 5e7; one side gives 4.9e7.
- Part 1 by hand: every halo gives about 0.1 to 0.2e10 inside 27 kpc; the largest disc (Locatelli's
  disc-only fit at Z = 0.1) about 0.13e10 in total. I expect ROTATION CURVE NOT SUPPLIED again.
- Part 2: B18 (2.8e10 inside 250) and L24z are lighter than MB15 and may fail at 0.01273 as S15 did.
  I expect the FRAGILE suffix to survive.

## Enclosed masses

M(<r) is computed in SI from each law: for a power law n = C r^-a, M = m_n 4 pi C r^(3-a) / (3 - a);
for the full beta model and the discs, numerical integration (discs: spherical enclosed mass over
R^2 + z^2 < r^2, both sides of the plane). Printed per model at 27, 80, 100, 150, 200, 273 kpc (and 30).
**Outer edge (frozen): each profile stops at its paper's stated outer radius** (MB15 250, MB13 200,
S15 300, F17 250, F20 283, B18 250, K20b 260, L24 350 kpc); M is constant beyond it. A variant that
extrapolates every law to 273 kpc is printed, not labelled.

## Part 1, the rotation curve

Need inside 27 kpc, from the record: 1.71 to 2.07e10 Msun canonical, 1.02 to 1.39e10 alt (MWG1's
numbers; 6.681e10 census times 0.256 to 0.310 or 0.152 to 0.208). Supplied by a model = its halo
M(<27) plus its own paper's disc-like M(<27) where one is published (L24, L24z, B18; K20b with
D-K20e). Discs D-L24d, D-K20x, D-N18 are also listed alone. **SUPPLIED** if a model reaches the lower
end of the need; per footing, label **ROTATION CURVE NOT SUPPLIED** if none does, else **SUPPLIED IN
k OF N**. The share of the need is printed for every model and for every disc alone. The question
"does disc-like hot gas change the inner answer" is answered by the largest disc's share.

## Part 2, the outer data

MWJ1's line as in MWG1 (copied functions): census at A = 1 plus the model's M_hot(<r) (halo plus its
own disc), same kernel, G239's angle average at e_N, both footings. Gates as MWG1: G1 (NMB1's
Q <= 6.180 at 30 and 80 kpc), G2 (PLT1's class medians, rows at r >= 100 kpc), G2p (rows at r >= 150
kpc), all medians within 2. For every model and footing: the range of e_N in [0, 0.03] (step 0.0005)
passing all three, whether 0.01273 passes, and whether a field at or below 0.008 passes.

Halo models in Part 2: MB15 (primary, Z^-1 convention, i.e. the paper's own masses), MB15h (same law,
Z^-1/2), MB13, S15, F17, F20, B18, K20b, L24, L24z.

## Labels, per footing

- Part 1 as above.
- Part 2, on MB15: **RECORD'S FIELD PASSES WITH HOT GAS** if 0.01273 passes G1, G2 and G2p; **RECORD'S
  FIELD STILL FAILS** otherwise. **FRAGILE** is appended if any other Part 2 model gives the other
  answer; the models that do are named.

## Known-answer checks (must all pass before any label)

| id | check | pass condition |
|---|---|---|
| KA1 | no gas reproduces MWJ1 | Q 4.89 / 2.91 (within 0.03), satellite plateau median -2.72 (within 0.02), window [0, 0.0075] both footings |
| KA2 | MB15's printed law reproduces its own quoted masses | 3.8e9 inside 50 kpc and 4.3e10 inside 250 kpc, each within 5 per cent, with the convention stated (n_e, 1.17 m_p per electron, density times (Z/Zsun)^-1 at 0.3). The Z^-1/2 masses are printed. If the Z^-1 convention does not close it, STOP and report |
| KA3 | the line at 80 kpc with no gas | 5.691 / 6.219 and 4.977 / 5.109 within 0.5 per cent |
| KA4 | F20's approximation against its Table 1 masses | 4.6e10 inside 258 kpc and 5.5e10 inside 283 kpc, each within 20 per cent (the paper's stated accuracy) |
| KA5 | SI check of the power-law mass formula | numerical shell integral of MB15's law equals the closed form within 0.1 per cent |

Reported, not blocking (consistency of the reconstructions with each paper's own numbers): MB13 at 18
and 200 kpc; F17 inside 250 kpc; S15's solved n0 rc^3b inside [0.005, 0.03]; Kaaret's and
Nakashima's disc masses against the printed 2e7 and 5e7; L24 halo mass at 250 kpc against "some 1e9
to some 1e10".

## Mutations (must bite)

- M1: ten times the MB15 gas, at (e_N = 0, census): must fail at least one gate on both footings.
- M2: ten times the largest Part 1 supply: Part 1 must flip to SUPPLIED on both footings.
Mutation runs write `hg2_mut.out`.

## What a label will and will not mean

Each law is the paper's fit under its own metallicity, temperature and outer-radius assumptions; the
spread between papers is the systematic. F17 and S15 are reconstructions from printed numbers, not
printed laws. The Faerman profiles are hydrostatic in a dark-matter potential. Part 1 is an upper
bound argument (mass inside the outermost fitted radius), not a refit of the rotation curve. Outer
gates have little power; a pass is the absence of a contradiction.
