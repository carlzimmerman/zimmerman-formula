# A62 — mutation controls

`a62_checks.py --mutate=<m>` activates one corrupted premise, runs all 25 checks, and exits 0
**iff some check broke**. Each mutation is stated as the claim it injects, so a passing run under
mutation would mean the corresponding check has no teeth. All five bite.

Captured outputs: `a62_MUTATE_m1.out` … `a62_MUTATE_m5.out`.

| flag | injected claim | checks broken | verdict |
|---|---|---|---|
| `m1` | `2Z = 12` exactly (the folklore substitution, taken as an identity) | K1, K5 | CONFIRMED |
| `m2` | `a0/(cH0) = 1/(2Z)` (H0 used where the vacuum statement needs H_Λ) | K4, K18 | CONFIRMED |
| `m3` | route (a) capacity saturation returns κ = ½ | K8, K22 | CONFIRMED |
| `m4` | exactly one closed form lies within 1 % of 11.5776 (no look-elsewhere) | K16, K17, K18 | CONFIRMED |
| `m5` | a Langevin medium reproduces the deep-MOND slope and the target scale | K14, K15 | CONFIRMED |

Notes on collateral damage, which is expected and stated:

- `m2` also takes K18, because K18 evaluates the pool at 1/(2Z) and the mutation corrupts the
  ratio table it prints. The targeted check K4 is the one that matters.
- `m4` restricts the pool to the target's own family (107 values instead of 156 210), so K16
  collapses to 2 hits, K17's random-target calibration collapses with it, and K18 loses the pool
  it shares. That is the point of the mutation: the "unique match" claim is only true if the pool
  is artificially narrowed.

Each mutation leaves every other check green, so the output shows exactly which check carries the
claim. Nothing else in the file reads the mutated constant.

## Sample lines (verbatim, truncated to 140 columns)

    m1  K1   FAIL  residuals ['0', '0', '0', '0']; 2Z=11.5776201; |2Z-12|=0.42238
        K5   FAIL  2Z=12 <=> pi=[27/8] (3.375000); |pi-27/8|=0.2334
    m2  K4   FAIL  a0/cH0=0.142937; 1/7 rel=5.62e-04; Omega_L=0.68380 vs 32pi/147=0.68388
    m3  K8   FAIL  kappa_route=2.894405 (=Z/2); a_crit/cH=1.000000000
    m4  K16  FAIL  pool=107; within 1%: 2 (same-shape k*sqrt(n pi/m): 9); 0.1%: 2
    m5  K15  FAIL  dlnA/dlnx: Langevin=1.000000, tanh=0.999999, MOND=0.500000

## What is *not* mutated

The exact-algebra checks (K2, K3, K6, K7, K11, K19, K21, K23, K24, K25) are identities, not fits: there is no
constant to corrupt, only a residual that is either 0 or not. Their teeth are shown instead by the
errata they catch — K23 fails against the FINAL_THEORY §1 chain as printed, which is why that
erratum is in the report. K2 encodes the correction to A1 eq. (2.1); running K2 against A1's
printed `κ = (Z/2)/g` would fail by exactly a factor 2 (verified by hand: (Z/2)/g at g = 12 gives
Z/24 = 0.2412, whereas A1's own (2.2) gives Z/12 = 0.4824).
