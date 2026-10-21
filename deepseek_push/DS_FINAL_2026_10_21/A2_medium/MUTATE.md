# MUTATE — A2_medium

## Mutation

`--mutate` changes exactly one thing: the capacity assignment. The gate capacity is
halved, `C = a0/2`, while the affinity stays `s = a0` — i.e. it applies the n=2 capacity
assignment to a Langmuir lattice. Everything else (constants, grid, seeds) is unchanged.

```python
CAP = A0 / 2.0 if MUTATE else A0     # capacity=A0/2 under --mutate
AFF = A0                             # affinity unchanged
```

This is the mutation with teeth, because the whole claim is that `n` *is* the capacity
assignment: if the checks survive a halved capacity they are not testing the law at all.

## Why it must break

The single-scale lattice law is `g_N = g − C g/(g+s)`, whose expansion has linear
coefficient `1 − C/s` (K5). With `C = s = a0` that coefficient vanishes and the law is
canonical; with `C = a0/2` it is `0.5`, so `g_N ≈ g/2` at low acceleration — no MOND deep
limit. K16 then measures the same fact end-to-end: inverting the lattice relation with
`(C,s) = (a0/2, a0)` and comparing to the canonical law over `g_N/a0 ∈ [1e-3, 1e3]` gives a
93.8% maximum deviation instead of a round-off.

## Mutated output

```
K1 PASS 0.0 0.0  # exact sympy: A=a0*th, gN=g*th, 1/A=1/g+1/a0, g=(a0+g)th, homogeneity deg 1
K2 PASS 0.0 0.0  # k_a g (1-th) = k_d th  =>  th = g/(g+a0)  =>  g_N = g^2/(g+a0)
K3 PASS 0.0 0.0  # GC: th=x/(1+x), mu=kT ln(g/a0)-eps => th=g/(g+a0); K W_full'=g; W_rem=Eq.(2,n=1)
K4 PASS 0.2689414213700161 1.0  # Fermi(theta) finite at g=-a0 where Langmuir has its only pole; g(1-th)->0 vs ->a0
K5 FAIL 0.5 1e-15  # series linear coeff = 1-C/s; MOND forces C=s => capacity=affinity=a0 (n=1)
K6 PASS 1.0 0.99  # n=2 gN(g) is EVEN; any Langmuir is not. Shared g^2/a0, cubic 1/a0^2 vs 0
K7 PASS 2.0 2.0  # A2/g has branch points +-i a0/2 (off (-inf,0]); A2''' changes sign at g=a0/4
K8 PASS 0.0 0.0  # 2 identical gates = 1 Langmuir with capacity 2c; A'(0)=1 => 2c=s => n=1
K9 PASS 0.15470053837641218 0.15470053837925152  # max at gN/a0=0.499994; v-ratio max 0.074569932 vs 0.074569932
K10 PASS 5.457356756685289 5.4574  # M=1e10 Msun: r*=5.45736 kpc v1=125.546 v2=116.834 km/s
K11 PASS 0.0016872173263471346 0.03  # Var(th)/th^2=(1-th)/(th Ns); MC rel.std 0.011199 vs 0.011180
K12 PASS -1.4997853494132798 -1.5  # ratio(0.3a0/3a0) n1=22.34 n2=34.49; ratio(a0/10a0) n1=23.00 n2=30.38
K13 PASS 0.013801311186847085 0.0  # skew(delta g) ~ (1-2 theta): positive below g=a0, negative above
K14 PASS 0.0 0.0  # both laws homogeneous deg 1 in (g,a0): a0 is the only dimensionful input
K15 PASS 0.999999999999 1.0  # ladders N=0..Nmax: capacity/a0 >= 1 always (a0/2 unreachable); only Nmax=1 is exact
K16 FAIL 0.9378703069057032 1e-12  # lattice inversion with CAP=4.680e-11, AFF=9.360e-11 vs canonical law on gN/a0 in [1e-3,1e3]
A2 COMPLETE: 14/16 checks PASS.
FAILED: K5,K16
```

Exit code 1. The two failures are precisely the two checks that assert `capacity =
affinity`; the 14 others are law-level or n=2-level statements that do not depend on the
assignment and therefore *should* survive, which is the expected pattern (a mutation that
broke everything would indicate the checks were not independent).

## Second mutation considered and rejected as a declared flag

Swapping the isotherm for the linear-coupling Fermi function `θ = 1/(1+e^{−βλg})` would
break K2/K3/K16 but would also break K4 by construction (K4 is the statement that the Fermi
form is *not* the Langmuir form), so it would be circular as a mutation. It is reported as
the K4 result instead.
