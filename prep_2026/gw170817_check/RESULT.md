# GW170817 vs the disformal photon metric — line-integral check

**Question.** Does the disformal lensing metric `g~ = g + B u u` (photons on `g~`, gravitons on
`g`) survive GW170817 when `B` is accumulated along the REAL ~40 Mpc NGC 4993 sightline, rather
than through a single deep-MOND galaxy crossing?

**Verdict: EXCLUDED. Erratum needed: YES.**

Reproduce: `python3 gw170817_lineintegral.py` (exit 0, both footings).

## The number

| | canonical `a0=9.36e-11` | alt `a0=1.13e-10` |
|---|---|---|
| `B_max` (host / MW shell) | 4.5e-6 / 3.4e-6 | 5.1e-6 / 3.8e-6 |
| **Delta_t** (host+MW crossings, IGM=0) | **3.5e7 s** (~1.1 yr) | **3.9e7 s** |
| `|c_gamma-c_gw|/c = Dt/t_travel` | **8.6e-9** | **9.5e-9** |
| vs the 1.7 s bound | EXCLUDED 2.1e7x (7.3 orders) | 2.3e7x (7.4 orders) |
| vs `|dc|/c < 1e-15` | EXCLUDED 8.6e6x (6.9 orders) | 9.5e6x (7.0 orders) |

Adding a nominal IGM (`g_bar=1e-14 m/s^2` over 40 Mpc) only makes it worse (`Dt ~ 1e11 s`); the
IGM never subtracts. The robust, IGM-independent minimum — the two **mandatory** galaxy crossings
(kilonova exits NGC 4993's MOND shell; light enters the Milky Way's, where the Sun sits at
`g_bar ~ 2 a0`) — already blows the bound by **~6–7 orders**, both footings.

## The three derivation points

1. **Local differential (exact).** Rest frame, `g~_00 = -(1-B)` (the `u_i u_j` block is zero, so
   the spatial metric is untouched — the same fact that makes `c_T=1` for gravitons). Photon null:
   `c_gamma = sqrt(1-B)`, graviton `c_T = 1`. So `|c_gamma - c_gw|/c = 1 - sqrt(1-B) = B/2`
   (photon subluminal). The factor is **B/2**, confirmed, not B.

2. **Line integral.** `grad|B| = 4(nu-1)g_bar/c^2` (UNIFICATION.md §2), framework
   `nu = sqrt(1+a0/g_bar)`, boundary condition `B->0` in the void (the choice most favorable to the
   framework). `Delta_t = (1/c) INT (1/sqrt(1-B) - 1) dl` over host-exit + IGM + MW-entry segments.

3. **Both footings** carried throughout; verdict identical.

## Why the hoped-for void rescue fails (and the banked ~6-order note was NOT a wrong path)

The subtlety that was hoped to rescue it: in a void `g_bar -> 0`, so `nu-1 -> inf` but
`(nu-1)g_bar = (c^2/4) grad B ~ sqrt(a0 g_bar) -> 0`. **True — but it only kills the GROWTH of B,
not B itself.** The delay `INT (B/2) dl` depends on the *accumulated* `B` (~1e-6, sustained across
each galaxy's ~100+ kpc width), not on `grad B`. B stops rising in the void; it does not vanish,
and the two galaxy crossings are unavoidable.

The banked `mi_disformal_gw170817_TENSION.py` (`Dt~3.6e6 s`, `|dc|/c~8.8e-10`) was **not** a single
deep-MOND galaxy crossing: it already used host (1e11) + Milky Way (6e10) and set the IGM to zero.
This independent segmented re-derivation (framework `grad B`, framework `nu`, void BC) **reproduces
it to the same order** (`3.5e7 s`, `8.6e-9`; slightly worse only because it integrates to 300 kpc
vs 100 kpc). The exclusion is real and robust — the banked "arguably the deepest challenge" and the
"lensing resolved" walk-back both stand.

**The `c_T=1` "exact" pass is irrelevant here.** GW170817 constrains the graviton–photon *arrival
difference*, which in this construction is exactly `B/2 != 0`. Riding the graviton on the clean
metric `g` does not help when the photon rides the tilted cone `g~`. This is the generic
dark-matter-emulator wall (Boran, Desai, Kahya & Woodard 2018; Kahya & Desai 2016): messengers on
different effective metrics.

## Consequence for the published paper (DOI 10.5281/zenodo.21403470)

The paper does **not** claim "lensing resolved" or "passes GW170817" — good. But its Honest-hinge
paragraph (`MI_FIELD_THEORY_RESULTS_2026.tex:489-490`) lists the LOS timing integral as open and
characterizes it as **"order-of-magnitude satisfied only."** That characterization is **false** —
it is order-of-magnitude *excluded* by ~6–7 orders. **Erratum required:** change "order-of-magnitude
satisfied only" to an explicit statement that the photon-vs-graviton LOS timing integral is
GW170817-**excluded** by ~6–7 orders (the two mandatory galaxy-shell crossings give
`Dt ~ 3.5e7 s >> 1.7 s`, `|dc|/c ~ 1e-8 >> 1e-15`, both footings), so the disformal photon-only
lensing sector does **not** clear GW170817 — a genuine open problem for the lensing sector, not a
near-miss. The abstract/§2.3 line `c_gamma^2 = 1-B > 0` should not be read as a GW170817 pass; the
same `B` that keeps the cone Lorentzian is what violates the timing bound.

**No claim that lensing is "resolved."** The dynamics sector (RAR, BTFR, `c_T=1` graviton) is
untouched by this. What is excluded is the specific **disformal photon-metric route to
dark-matter-free lensing** — as the banked note already held.
