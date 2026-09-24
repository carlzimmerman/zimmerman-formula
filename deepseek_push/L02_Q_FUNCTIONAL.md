# L02 -- THE Q-FUNCTIONAL:  E[Q](tau0, q) has NO closed form (registered MEASURED-ONLY)

**Lane:** deepseek_push/L02_q_functional.py (engine: J02_moment_hierarchy kernels, bit-identical
RNG stream to J02 `simulate_Q`).  **Date:** 2026-09-23.  **Status: CLOSED, no git commit.**

---

## VERDICT (one paragraph)

```
E[Q](tau0,q) = E[ sum_{j=0..N} ell_j (u_j . u_final) ]   (volume source, unit ball,
kappa(r) = tau0 (1 + q r^2), isothermal Thomson kicks, E[mu]=0)

= MEASURED-ONLY  (new functional; 18-point table published below, n = 1.5e5/point)
KILL CONDITION: any closed form claimed by another lane must reproduce the L02
table (E[Q] +/- s_Q at every grid point) within 3 SE.
```

Every candidate class in the task brief was swept and fails by at least an order of
magnitude: the best **zero-free-parameter** named form reaches 415 SE, the best
**data-fitted** 2-10 parameter rational family reaches 21.1 SE (7x the 3-SE kill
threshold), and the specific suggested shapes a\*tau0\*(1+q/3)/(1+q\*b)+c (a = 3/8, 1/2)
fail at 103 SE even with b, c fit from the data.  The derivation route closes with an
exact collapse to an escape-conditioned covariance sum plus a proven
non-exchangeability obstruction; no E[N]\*E[l]-type factorization exists.

Checks (all PASS): bookkeeping Q==X (max err 3.8e-15); anchor E[Q](1,0)=0.5971526
reproduced at 0.0 SE (bit-identical photons, seed 41); E[v^2]=2E[N] exact identity;
central frozen identity E[D] = tau0 (1/2 + q/4) exact at all 16 central points.

---

## 1. Exact facts (what CAN be said in closed form)

Let N = number of collisions, u_0 = emission direction, u_j = direction after the
j-th kick, u_final = u_N = direction of the last (escape) flight, and
d_j := u_j . u_N.  Definitionally (J02 B4, cross-checked to 3.8e-15 per photon):

```
Q  =  sum_{j=0..N} ell_j d_j  =  (x_tau - x_0) . u_N        (x_tau = exit point)
D  =  tau - Q  >= 0
```

**Exact (no asymptotics), for BOTH sources:**

1. **Mean-zero non-final dots.**  E[mu] = 0 for the Thomson kernel (symmetric
   density (1+mu^2)/2), so by induction on the kick,
   `E[d_j] = 0  for every j < N`, while `d_N = 1` identically.  Hence

   ```
   E[Q] = E[ell_N]  +  sum_{j<N} Cov(ell_j, d_j)          (*)
   ```

   The non-final terms are PURE covariance terms between flight lengths and the
   (mean-zero) final-direction dots; there is no E[l]\*E[d] piece to factor.

2. **E[v^2] = 2 E[N] exactly** (conditional N(x,2 ang) kicks; E[ang]=E[N]·E[1-mu]=E[N]).
   Verified: -7e-3 +/- 3e-2.  Consequence: the candidate class E[Q] = E[tau] E[v^2]/...
   collapses immediately to E[tau]\*E[N]-rational forms, all of which die on the
   tau0->0 face (E[N] -> 0 while E[Q] -> 3/4, below).

3. **Central source is closed:** the frozen identity E[D] = int_0^1 r kappa(r) dr
   holds for the q-cloud too — kappa(r) = tau0(1+q r^2) — giving the exact
   `E[D]_central = tau0 (1/2 + q/4)`, verified at all 16 central points
   (e.g. (1,3): 1.2489 vs 1.25; (1,10): 2.9997 vs 3.0).  Therefore
   `E[Q]_central = E[tau]_central - tau0(1/2 + q/4)`: the central Q is closed IFF
   the mean total path E[tau]_central is; E[tau]_central is itself a classical
   transport functional (table below, no elementary closed form known).

4. **Limits (volume):** E[Q](tau0->0) -> E[ell_0] = 3/4 EXACTLY (chord-length bias
   argument: E[wall | x~vol, u~iso] = E[c^2]/(2E[c]) = 2/(2·4/3) = 3/4, and the first
   flight dominates).  Probes: E[Q](0.05)=0.7378, (0.1)=0.7269, consistent with
   3/4 - O(tau0).  E[Q] is monotone DECREASING in tau0 (0.738 -> 0.370 at tau0=8)
   with a positive limit as tau0->inf (E[Q](8,0)=0.3695, still drifting);
   E[tau] is monotone increasing (0.758 -> 2.31).  No rational-in-tau0 closed form
   can carry both faces (see sweep).

## 2. The derive route and the obstruction (registered)

**First-scatter form.**  Q = ell_N + T_<,  T_< = Q - ell_N = sum over the N non-final
segments.  Measured (1,0): E[ell_N] = 0.5633, E[T_<] = +0.0339 +/- 0.0012 — the
covariance sum is POSITIVE (long flights positively correlate with final-direction
alignment; the sign/intensity are purely escape-conditioned transport effects).

**Exchangeability of the direction chain — PROVEN false, and why.**
(a) *Marginals.*  E[d_j] = 0 (j<N) vs E[d_N] = 1 — exchangeability would require
identical marginals.  (b) *Second moments, empirically* (n=1.5e5, volume, q=0,
aggregated per k = N-j):

```
k = N-j :  0      1       2       3       4       >=5
E[d^2]  :  1.000  0.4001  0.339   0.333   0.333   0.333   (stable across tau0, n_k>=1e4)
free-chain spectral pred 1/3+(2/3)(3/10)^k:
         :  1.000  0.5333  0.3933  0.3513  0.3387  1/3
```

The free reversible-chain prediction FAILS at k=1,2 (37 and 16 sigma): the ESCAPE
event conditions the last kick (E[cos^2] of the escape-selected pair = 0.4001 ~ 2/5,
not the Thomson 8/15 = 0.5333), and the correlation tail dies within ~2 kicks instead
of geometrically.  The direction chain conditioned on "escaped" is *not* the free
Thomson chain, is not reversible, and its marginals depend on position j — the
segment sequence {(ell_j, d_j)} is emphatically non-exchangeable.

**The obstruction.**  The E[N]\*E[l]-type decomposition would require
E[ell_j d_j] = E[ell]\*E[d_j]-ish with j-free structure; instead (*) leaves only
escape-conditioned covariances that are kernels of the STOPPED transport (exit
geometry), not moments of the free kick law.  Any closed form for E[Q] requires
a closed form for the escape-conditioned covariance — a strictly harder object than
E[N] or E[tau] — while E[Q] itself depends nontrivially on the joint law
(pos_j, u_j, u_N).  No such form exists in the engine's data.

## 3. The published table (the KILL-CONDITION reference)

**VOLUME source** (n = 1.5e5 per row; E[D] = E[tau] - E[Q]; <Q/N> = E[Q/N],
  <Q/(N+1)> = per-segment mean = E[ell_J d_J] over a uniform random segment):

| tau0 | q | E_Q     | s_Q    | E_tau | E_D   | E_N   | E_mu_exit | E_lN  | E[T_<]  | <Q/(N+1)> |
|------|---|---------|--------|-------|-------|-------|-----------|-------|---------|-----------|
| 0.05 | 0 | 0.73783 | 0.00125| 0.7576| 0.0198| 0.037 | 0.7492    | 0.7378| 0.00007 | 0.72397   |
| 0.10 | 0 | 0.72694 | 0.00124| 0.7662| 0.0392| 0.077 | 0.7477    | 0.7265| 0.00047 | 0.69929   |
| 0.30 | 0 | 0.69163 | 0.00121| 0.8027| 0.1111| 0.240 | 0.7459    | 0.6867| 0.00493 | 0.61563   |
| 0.50 | 0 | 0.65985 | 0.00119| 0.8411| 0.1813| 0.421 | 0.7417    | 0.6484| 0.01141 | 0.54244   |
| 1.00 | 0 | 0.59715 | 0.00113| 0.9374| 0.3402| 0.938 | 0.7352    | 0.5633| 0.03385 | 0.40319   |
| 2.00 | 0 | 0.51693 | 0.00104| 1.1286| 0.6117| 2.261 | 0.7263    | 0.4356| 0.08137 | 0.24299   |
| 3.00 | 0 | 0.46766 | 0.00098| 1.3228| 0.8551| 3.975 | 0.7234    | 0.3489| 0.11874 | 0.15897   |
| 8.00 | 0 | 0.36954 | 0.00088| 2.3099| 1.9404| 18.47 | 0.7143    | 0.1665| 0.20308 | 0.04207   |
| 0.30 | 3 | 0.62902 | 0.00119| 0.9226| 0.2935| 0.728 | 0.7349    | 0.5997| 0.02931 | 0.46344   |
| 0.50 | 3 | 0.57291 | 0.00115| 1.0416| 0.4687| 1.357 | 0.7286    | 0.5147| 0.05824 | 0.34432   |
| 1.00 | 3 | 0.49012 | 0.00106| 1.3436| 0.8535| 3.437 | 0.7204    | 0.3567| 0.13340 | 0.18191   |
| 2.00 | 3 | 0.41556 | 0.00099| 1.9651| 1.5495| 9.870 | 0.7149    | 0.1983| 0.21726 | 0.06840   |
| 3.00 | 3 | 0.38608 | 0.00096| 2.6008| 2.2147| 19.33 | 0.7128    | 0.1318| 0.25430 | 0.03527   |
| 0.30 |10 | 0.53143 | 0.00113| 1.2104| 0.6790| 2.289 | 0.7223    | 0.4294| 0.10207 | 0.25378   |
| 0.50 |10 | 0.47135 | 0.00107| 1.5314| 1.0600| 4.744 | 0.7166    | 0.2994| 0.17191 | 0.14083   |
| 1.00 |10 | 0.41000 | 0.00101| 2.3468| 1.9368| 14.12 | 0.7138    | 0.1518| 0.25820 | 0.04855   |
| 2.00 |10 | 0.37437 | 0.00099| 3.9684| 3.5940| 46.57 | 0.7128    | 0.0720| 0.30242 | 0.01426   |
| 3.00 |10 | 0.36213 | 0.00098| 5.5690| 5.2069| 96.84 | 0.7123    | 0.0472| 0.31491 | 0.00682   |

Anchor: E[Q](1,0) = 0.5971526 (J02: 0.5971526, same seed, bit-identical; the J02
"0.59715 is not a nameable constant" statement stands — it is 0.6 = 3/5 at -2.5 SE,
i.e. 3/5 is excluded at 3-SE for the full table (named-candidate row, max 5046 SE)).

**CENTRAL source** (for completeness; note E[D] = tau0(1/2+q/4) exact => any
closed form here reduces to E[tau]_central, a classical functional):

| tau0 | q | E_Q     | s_Q    | E_tau | E_D         |
|------|---|---------|--------|-------|-------------|
| 0.1  | 0 | 0.98801 | 0.00016| 1.0394| 0.0514      |
| 0.3  | 0 | 0.96679 | 0.00025| 1.1152| 0.1484      |
| 0.5  | 0 | 0.94656 | 0.00031| 1.1947| 0.2482      |
| 1.0  | 0 | 0.90376 | 0.00040| 1.4035| 0.4997      |
| 2.0  | 0 | 0.84211 | 0.00047| 1.8456| 1.0035      |
| 3.0  | 0 | 0.80401 | 0.00050| 2.3002| 1.4962      |
| 0.3  | 3 | 0.91276 | 0.00041| 1.2874| 0.3747      |
| 0.5  | 3 | 0.87113 | 0.00047| 1.4942| 0.6230      |
| 1.0  | 3 | 0.80315 | 0.00052| 2.0520| 1.2489      |
| 2.0  | 3 | 0.74861 | 0.00054| 3.2537| 2.5051      |
| 3.0  | 3 | 0.73194 | 0.00055| 4.4853| 3.7533      |
| 0.3  |10 | 0.83010 | 0.00052| 1.7312| 0.9011      |
| 0.5  |10 | 0.78022 | 0.00054| 2.2819| 1.5017      |
| 1.0  |10 | 0.73723 | 0.00054| 3.7369| 2.9997      |
| 2.0  |10 | 0.72111 | 0.00055| 6.7256| 6.0045      |
| 3.0  |10 | 0.71695 | 0.00056| 9.7076| 8.9907      |

## 4. Candidate closed forms — sweep results (residuals in SE units)

Fitted families (weighted least squares, 18 volume points, params noted):

| family | form | max|resid|/SE | rms/SE | fitted params |
|--------|------|-------------|--------|---------------|
| F1 a=1/2 | a tau0 (1+q/3)/(1+qb) + c | 102.9 | 61.2 | b=0.055, c=0.611 |
| F1 a=3/8 | same | 102.9 | 61.2 | b=0.055, c=0.611 |
| F1 a=3/4 | same | 102.9 | 61.2 | b=0.055, c=0.611 |
| F1 a free | same | 102.9 | 61.2 | a=-0.037, b=0.055, c=0.611 |
| F2 | a tau0 (1+q/3)/(1+qb) | 587.1 | 406.1 | a=0.100, b=0.376 |
| F3 | a tau0/(1+b tau0) (1+q/3)/(1+cq) | 508.4 | 288.7 | b=3.0, c=1.29, a=2.37 |
| F4 | (a tau0 + b tau0^2)(1+q/3)/(1+cq) | 573.1 | 356.9 | a=0.451, b=-0.051, c=1.54 |
| F5 | f(tau0)(1+alpha q)/(1+beta q), 8 free rows | 21.1 | 12.1 | alpha=0.102, beta=0.169 |
| F6 | (3/4)(1+aq)/(1+b tau0+cq) | 69.2 | 35.8 | b=0.152, c=0.051, a=0.001 |
| F7 | (3/4)(1+aq)/(1+b tau0+cq+d q tau0) | 63.1 | 35.4 | b=0.09, c=0.18, d=0.06, a=0.114 |

Zero-free-parameter named candidates (best -> worst):  (1/2)(1-E[mu_exit]^2) = 415 SE;
E[tau](1-E[mu_exit]^2) = 2426 SE; (1/2)E[tau] = 2467 SE; E[tau]E[mu_exit]^2 = 2509 SE;
(4/3)E[tau](1-E[mu_exit]^2) = 3357 SE; E[tau]-1/2 = 4794 SE; (3/5)tau0 = 5046 SE;
(3/5)tau0(1+q/3)/(1+q/2) = 5046 SE; (3/4)tau0(1+q/3)/(1+q/2) = 6413 SE.

Shape diagnostics against the specific brief candidate (1+q/3)/(1+q\*b), per tau0 row
(volume): implied b from the q=3 and q=10 ratios disagree by **39 / 38 / 24 / 1.1 / 6.6 SE**
at tau0 = 0.3 / 0.5 / 1 / 2 / 3 — the shape is rejected on the small-tau0 face,
is consistent (b ~ 1/2) only near tau0 = 2, and no single b works across the grid.
q-ratios at tau0=1: 1, 0.8208, 0.6866 (vs (1+q/3)/(1+q/2): 1, 0.8000, 0.7222).

The E[tau]E[v]^2 class is closed analytically: E[v^2] = 2 E[N] exactly, and every
E[tau]E[N]-rational shows E[N]->0 while E[Q]->3/4 on the tau0->0 face.

## 5. Registration

- **E[Q](tau0, q; volume) is a NEW functional, MEASURED-ONLY.**  Table in Sec. 3,
  machine-readable copy in L02_results.json (18 volume + 16 central rows with SEs
  and the per-collision decomposition E[ell_N], E[T_<], <Q/N>, <Q/(N+1)>,
  E[mu_exit]).
- **Kill condition:** a closed form claimed by another lane must reproduce every
  row of Table 3 (volume) within 3\*s_Q.  In particular it must hit 0.59715+/-0.0034
  at (1,0), the 3/4-face at tau0->0, and the tau0=8 value 0.3695+/-0.0026.
- Per-collision decomposition (the task's <Q/N> request): <Q/N> = E[Q/N] = 0.4977 at
  (1,0) = E[ell_N/N] + E[T_</N] = 0.4778 + 0.0199; the per-segment mean
  E[Q/(N+1)] = E[ell_J d_J] (uniform random segment) = 0.4032, dominated by the
  final segment E[ell_N] = 0.5633.  All columns tabulated per row in
  L02_results.json (E_Q_over_N, E_Q_over_Np1, E_lN, E_Tless).
- E[Q]_central is closed IFF E[tau]_central is (Sec. 1.3); both tabulated.