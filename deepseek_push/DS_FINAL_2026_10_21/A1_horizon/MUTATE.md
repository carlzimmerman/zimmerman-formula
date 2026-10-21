# MUTATE.md — proof that the A1 checks have teeth

`a1_checks.py` accepts `--mutate[=m1|m2|m3|m4]`. Each mutation injects one *specific* wrong
claim — the kind a careless or motivated derivation would actually make — and corrupts
**only** the checks whose stated content that claim contradicts. Untouched checks stay
green, so the output pinpoints which check guards which claim.

Exit code: 0 when at least one targeted check breaks (mutation confirmed), 1 if a mutation
fails to bite.

Run: `python3 a1_checks.py --mutate=mN`

---

## m1 — "the twelfth": assert 2Z = 12 exactly

Replaces the irrational 2Z = 11.577620073 with the folklore integer 12 and asserts
κ("1/12") = 1/2.

```
# *** MUTATION m1 ACTIVE: corrupting K1,K3 ***
K1 FAIL 12.000000000 2Z=11.577620073+-1e-9   # 2sqrt(32pi/3)-2Z is identically 0 (sympy); 32pi/3 = 4*(8pi/3)
K3 FAIL kappa(twelfth)=0.500000000 Z/12=0.482400836, 3.52pct below 1/2   # 1/12 <=> kappa=Z/12; kappa=1/2 <=> 2cH/a0=2Z=11.577620; 12/2Z=1.036482

A1 COMPLETE: 11/13 checks PASS.
# mutated checks broken: K1,K3
# MUTATION CONFIRMED
```

## m2 — the folklore "a0 = cH/6", i.e. a0/(cH) = 1/6

The most common informal statement of the coincidence. It is not 1/Z = 0.1727471.

```
# *** MUTATION m2 ACTIVE: corrupting K2 ***
K2 FAIL 0.166666666667 1/Z=0.172747074736+-1e-12   # the two Einstein substitutions Lambda->rho and rho->H are both exact

A1 COMPLETE: 12/13 checks PASS.
# mutated checks broken: K2
# MUTATION CONFIRMED
```

## m3 — claim κ = 1/2 *is* a member of the horizon-counting class

This is the failure mode the BRIEF §2 names (premise insertion): assert that the menu
contains 1/2, and that a class member reproduces it.

```
# *** MUTATION m3 ACTIVE: corrupting K5,K9 ***
K5 FAIL min|kappa-1/2|=0.039341 >0.03 and gap>0.4   # nearest menu entry g=2pi -> 0.460659; kappa=1/2 needs g=Z=5.78881, 0.494 from the nearest menu g
K9 FAIL min|kappa-1/2|=0.1382 >1e-6, closed forms to 1e-8   # numeric ['4.0933', '2.8944', '5.7888', '0.3618'] vs exact ['4.0933', '2.8944', '5.7888', '0.3618'] ; P1c (cell-length strain) kappa=1.76e+41, kappa^2/pi in Q for all four

A1 COMPLETE: 11/13 checks PASS.
# mutated checks broken: K5,K9
# MUTATION CONFIRMED
```

## m4 — claim the strain-saturation principle P1 returns 1/2

The tempting reading of §6: "per-cell saturation must give the canonical κ."

```
# *** MUTATION m4 ACTIVE: corrupting K8 ***
K8 FAIL kappa=0.500000000 4sqrt(pi/3)=4.093306832+-1e-9   # a0 = sqrt2 cH = 7.6579e-10 m/s2; mismatch to 1/2 = 8sqrt(pi/3) = 8.186614

A1 COMPLETE: 12/13 checks PASS.
# mutated checks broken: K8
# MUTATION CONFIRMED
```

---

## Coverage

| mutation | breaks | what it proves the check guards |
|---|---|---|
| m1 | K1, K3 | the exactness of 2√(32π/3) = 2Z and the 3.52 % gap to 12 |
| m2 | K2 | that a0/(cH_Λ) is 1/Z, not 1/6 |
| m3 | K5, K9 | that 1/2 is not on the ladder and not in the class image |
| m4 | K8 | that P1 gives 4.093307, not 0.5 |

Checks **not** covered by any mutation (K4, K6, K7, K10, K11, K12, K13) are structural —
they assert symbolic identities, dimension counts, or root-find agreement rather than a
single quotable number, so there is no one-token corruption that leaves the rest of the
check intact. They are guarded by construction: K6/K10 compare sympy nullspace dimensions
and solve results against closed forms, K4/K13 by the 3-dp / sub-percent thresholds quoted
in the check line.
