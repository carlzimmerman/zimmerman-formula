# FINAL-16 (KAPPA_REAL) PREREGISTER -- 2026-11-11

Committed **alone**, before any FINAL16 script exists and before any FINAL16 number is computed.
Nothing below has been run. The predicted outcome is written down first, on purpose: this lane is
expected to return a NEGATIVE, and the negative is stated here so that it cannot be softened later.

**Lane.** FINAL MILE, lane **FINAL-16 (KAPPA_REAL)**. TEST lane, quarantined: adopts nothing,
relabels nothing, registers nothing, edits nothing outside this folder. Footings never pooled
(canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2). Cold dark energy is a gravitating field
component; no particle is added. **kappa = 1/2 FITTED; not theory closed.**

**Id checked free:** no `closure_2026_11_11/FINAL16*` path exists, and no commit subject on any
branch names FINAL16, FINAL-16 or kappa_real.

## 0. The question, in one line

> Under the formation reading -- the amount is set at the assembly event and conserved -- does
> `a_0 = kappa * c * sqrt(G * rho_Lambda)` follow, with a specific kappa?

Split, as FINAL6 did, because the halves have different answers:
- **Q1 (form).** Does the reading output the *form* `a_0 ∝ c sqrt(G rho_*)`, and pick `rho_* = rho_Lambda`?
- **Q2 (coefficient).** Does it output the number 1/2?

## 1. What the siblings already fixed (adopted, not redone)

- **FINAL6 (KAPPA, cbba716d05)** -- label **KAPPA NOT DERIVED (FITTED)**. K1: universality (no M in a_0)
  forces the form uniquely. K3: a frozen 20-item scan over closed forms in the formation data lands on
  1/2 only for the item `1/2` itself. K4: freeze-out at matter--Lambda equality gives `z_f = 0.295478`
  vs `z_L = 0.294967` -- flagged as a *consistency test, not a derivation*. K5: per-galaxy freeze-out
  refuted by RAR universality.
- **GF1/GF2 (deepseek_push, 2026-11-08)** -- a *different* channel, certified:
  `kappa := a_0/s = 1/n` with `s := n a_0`; at `n = 2` this is 1/2, and **n = 2 is measured
  independently** (germ ratio 4.000406 vs 4, `Z^2 = 32 pi/3 = 33.510322`, `Omega_L = 0.685`,
  `S = 3/2 - ln 2`). Also `kappa = sigma^2/v_flat^2 = 1/2` exactly from the log-branch closure.
- **NPJ1** -- nine sectors; a1 clears cosmology, fails unitarity (dim -4 `|psi|^6`); a2 fails on
  odd `g_k = 1/k`; b2/c3 pass unitarity but miss locality by `10^5.42 / 10^5.37`.

So a `kappa = 1/2` route **already exists in the record** (GF2/GF1). What has *not* been established,
and what this lane tests, is whether **the formation reading specifically** outputs the normalisation.
The GAP is real: GF1/GF2's `kappa = 1/n` constrains the ratio `a_0/s`; it says nothing about which
cosmic density stands under the square root, and it does not come from formation physics.

## 2. Conventions

SI unless a line says eV. G = 6.67430e-11, c = 2.99792458e8.
Planck 2018 TT,TE,EE+lowE+lensing: H0 = 67.36 km/s/Mpc, Om = 0.3153, OL = 0.6847, Ob = 0.0493,
Oc = 0.26445. rho_crit,0 = 3 H0^2/(8 pi G); rho_L = OL rho_crit,0; rho_m,0 = Om rho_crit,0.
E(z) = sqrt(Om (1+z)^3 + OL); rho_m(z) = rho_m,0 (1+z)^3.
f_cdm = Oc/Ob = 5.3640; f_b = Ob/Om = 0.156359; OL/Om = 2.17158; delta_c = 1.686; Delta_v = 178.
X (formation-share, FINAL4/PD1) = 59.4861 can / 59.5029 alt.
Record's tie: rho_ref = 4 a0^2/(c^2 G); Z = c H_L/a_0 = sqrt(32 pi/3) = 5.78881; a = 2 pi^2, n = 2.

**The formation reading F (same operational definition as FINAL6, verbatim in substance).**
- **F1 (amount).** X is fixed at the assembly event and conserved: X = X_L(g_b,f),
  X_L(y) = (sqrt(1 + 4 a_0/y) - 1)/2.
- **F2 (normalisation).** a_0 = kappa c sqrt(G rho_*) with rho_* the cosmic density the event imprints.
- **F3 (universality -- empirical).** One a_0 fits the RAR; the two footings differ by 0.0411 dex.

## 3. The graded items (criteria fixed now)

**J0 -- REAL-kappa: what is the number, measured?** *(graded)*
kappa is not a free constant of nature until the two sides are measured in the same units. Compute
kappa = a_0/(c sqrt(G rho_L)) for three a_0 inputs: (i) record canonical footing a0 = 9.3603e-11;
(ii) record alt footing a0 = 1.1312e-10 against rho_crit,0; (iii) the external RAR/SPARC value
a_0 = 1.20e-10 m/s^2 with +-0.02 (random) +-0.24 (systematic) x 1e-10 (Lelli/McGaugh/Schombert 2017,
PROVISIONAL).
**Verdict rule, fixed now:** J0 = "kappa = 1/2 is a CONVENTION, not a measurement" **iff**
|kappa_ext - 1/2| > 0.05; otherwise "COMPATIBLE". *Predicted:* kappa_ext ~ 0.64 -> CONVENTION.

**J1 -- the scale-covariance no-go (exact; sympy).** *(graded)*
Exhibit the one-parameter group G_lam:
  a_0 -> lam a_0,  g_b -> lam g_b (every formation field),  X, M_b, rho_*, c, G fixed.
Check every relation of F for invariance, symbolically: (i) X_L(lam y; lam a_0) == X_L(y; a_0);
(ii) the exact quadratic form of F1, g_b,f X (1+X) = a_0, is covariant (weight 1 on each side, so the
relation is preserved); (iii) F3 is covariant; (iv) the budget relation rho_ph = X rho_b carries no a_0.
F2 is the *only* relation that is not invariant -- it is the definition of kappa, so kappa -> lam kappa.
**Verdict rule, fixed now:** J1 = **NO-GO CONFIRMED iff G_lam is an exact symmetry of F1, F3 and every
formation relation and no G_lam-invariant is available to fix kappa.** *Predicted:* CONFIRMED.
Meaning if confirmed: **kappa is a flat direction of the formation physics.** The reading can at most
say "kappa is the same number for every galaxy and every epoch"; no equation of the reading can say
which number.

**J2 -- the routes that break the covariance (frozen list; graded).** *(graded)*
Since G_lam is a symmetry of F, the *only* thing that can output kappa is an added relation that is
NOT G_lam-covariant -- i.e. one that nails a dimensionful formation field to cosmology independently
of a_0. Frozen list of six such conditions; no item added or dropped after the run:
| id | added condition | kappa it forces |
|----|-----------------|-----------------|
| C1 | freeze-out at matter--Lambda equality: rho_m(z_f) = rho_L | 1/(2 sqrt 1) = 0.5 |
| C2 | freeze-out today: rho_* = rho_m,0 | 1/(2 sqrt(Om/OL)) |
| C3 | freeze-out at acceleration onset: rho_m = 2 rho_L | 1/(2 sqrt 2) |
| C4 | freeze-out at the record's binding epoch z_bind = 10.83 | 1/(2 sqrt(beta(z_bind))) |
| C5 | freeze-out at spherical-collapse threshold, g_b,f = delta_c * c sqrt(G rho_L) | a_0/(c sqrt(G rho_L)) with a_0 = delta_c c sqrt(G rho_L) X(1+X) |
| C6 | turnaround R_ta^3 = 3 M_tot/(8 pi rho_L) with R_set = (1+X) r_M, r_M = sqrt(G M_b/a_0) | solve for kappa |
*(Note C1 is FINAL6's K4 hit -- it is included deliberately, to grade what it is worth.)*
**Verdict rule, fixed now:** a route PASSES **iff** |kappa_route - 1/2| <= 0.025 **AND** the route's added
condition is *derived from F*, not chosen from a menu of named epochs.
**Spread test (graded, decisive):** report the dex span of kappa across the frozen menu that is
consistent with the data, and compare with the observational allowance 0.0411 dex. **If the menu freedom
exceeds 0.0411 dex, the route class cannot fix kappa at the required precision and J2 = NO ROUTE PASSES.**
*Predicted:* the epoch menu alone spans ~0.32 dex (and ~1.6 dex including z_bind) -> FAIL by ~8x.

**J3 -- the GF1/GF2 n = 2 hook (graded).** *(graded)*
The record's certified identity is `kappa = 1/n`, `n = 2` measured to ~1%. Grade whether this
*derives* the normalisation relation `a_0 = kappa c sqrt(G rho_Lambda)`.
**Verdict rule:** PASS only if all three hold: (i) kappa = 1/n is a theorem of the family (re-verify);
(ii) n = 2 is measured **independently of a_0's normalisation**; (iii) the step that puts `rho_Lambda`
under the root is not itself equivalent to assuming the relation.
*Predicted:* (i) YES, (ii) YES, (iii) NO -> **J3 = RESTATEMENT, not a formation output** -- the n = 2
channel fixes the *ratio* `a_0/s`; it does not select the cosmic density, and it is not formation physics.

**J4 -- where the formation event actually sits (graded).** *(graded)*
From F1's exact quadratic, g_b,f = a_0/[X(1+X)]. Compute it per footing and compare with the cosmic
accelerations c H_0, c H_L, c sqrt(G rho_L). **Verdict rule:** if g_b,f lies more than 2 dex below
every cosmic acceleration, the formation event is *not* set by cosmology in acceleration units and no
formation equation can supply a_0's magnitude from cosmology. *Predicted:* ~3.9 dex below.

**J5 -- the epoch-prediction the reading does supply (reported, not graded).**
rho_* = rho_Lambda is epoch-independent, so the reading predicts `a_0(z) = a_0(0)` exactly; the
alternative rho_* = rho_crit(z) predicts `a_0(z)/a_0(0) = E(z)`. Print E(z) and both at
z = 0.3, 0.5, 1.0, 2.0, 6.0. FINAL2's own bound on a_0(z) stands; this lane does not grade it.

## 4. Known answers (each must pass, both footings)

- **KA-1.** Z = c H_L/a_0 = sqrt(32 pi/3) = 5.78881 to 1e-4.
- **KA-2.** rho_ref(can)/rho_L = 1 within 2e-3; rho_ref(alt)/rho_crit,0 = 1 within 2e-3.
- **KA-3.** X_L satisfies g_b,f X(1+X) = a_0 exactly (sympy, positive root).
- **KA-4 (GF1/GF2 battery at n = 2).** germ ratio = n^2 = 4; Z^2 = 32 pi/3 = 33.510322;
  A*Lambda = 8 pi^2 n^2/c^4 -- each to |rel| <= 1e-3.

## 5. MUTATE -- three false twins, each of which MUST be rejected by the same machinery

- **M1.** "kappa = 1/(2 pi) is derived by the formation reading." (Milgrom's q; the T001 closest
  near-miss.) Machinery must reject: |0.159 - 0.5| = 0.341 >> 0.025.
- **M2.** "the z_f = z_L hit (C1) derives kappa = 1/2." Machinery must reject via the spread test:
  the named-epoch menu moves kappa by more than 0.0411 dex, so the hit is an epoch choice.
- **M3.** "kappa = 1/2 is a measurement." Machinery must reject via J0: kappa = 1/2 is realized on
  the canonical footing by construction (rho_ref := 4 a0^2/(c^2 G)), and the external RAR a_0 gives
  kappa ~ 0.64.

## 6. Labels

- **KAPPA DERIVED (FORMATION).** Some route in F, with no free dimensionless input, outputs kappa with
  |kappa_out - 1/2| <= 0.025 on both footings.
- **KAPPA NOT DERIVED (FITTED) -- FORM OUTPUT.** Q1 = YES (the reading outputs
  `a_0 = kappa c sqrt(G rho_Lambda)`, with rho_Lambda fixed by universality + epoch-independence);
  Q2 = NO. *This is the pre-registered expectation.*
- **KAPPA NOT DERIVED (FITTED) -- FORM NOT OUTPUT.** Neither half.
- **OPEN** if any known answer fails or a numerical step fails.

## 7. Scope

Dimensional analysis, the formation reading's own algebra, the kernel-family identity already certified
in GF1/GF2, a flat-LambdaCDM background, and sympy for every exact step. No new data, no download, no
CLASS run, no refit of a_0, no new sector, no verdict on NPJ1's sectors. Literature attributions
PROVISIONAL.
