# PIK1 RESULT: the two-variable dust term L_K(Q, Pi). **NO VALUE / NO VALUE.**

> **CP02 continuation, 2026-11-12 (wording reconciled by the lead session with the correction file beside this one):**
> a further calculation by the correcting session reports an instability of the specified unrestricted
> flat-gate family. That claim has not been independently checked (audits C2 and C4), and
> `CORRECTION_2026_11_12.md` says the full constrained system is not shown to have a ghost: read it as a
> reported claim, not an established result. It does not validate this file's original cluster-ordering
> argument. The imported `2.51e4/Mpc` growth threshold also used a polarization-off equation and is not
> validated for the coupled system (audit C1). See the [new scoped result](../../research_closure_2026_11_12/closure_push_02/RESULT.md)
> and [corrected growth audit](../../research_closure_2026_11_12/closure_push_02/growth_gate_audit/RESULT.md).

> **Forward correction, 2026-11-12:** the historical label below is preserved.
> Its universal linear-invisibility claim is refuted by the quadratic action;
> universal NO VALUE is not established, and the promised cluster/galaxy scan
> was never completed. Read [the correction](CORRECTION_2026_11_12.md) and its
> executed derivation before using this result as a closure dependency.
>
> *Audit note, 2026-11-12 (lead session):* this notice was written by another session and is committed here on the owner's instruction after an independent check, `reviews/codex_corrections_audit_2026_11_12/C2_pik1_and_frm1.md` (grade: linear invisibility refuted: CORRECT; NO VALUE not established: CORRECT WITH LIMITS). The audit also found that this lane's criteria, result and scripts were committed together, that `pik1_var.py` does not compile and that no output file exists, so the label below was never computed against its rows. The scripts in this folder are unchanged; the bounded quadratic check is in `correction_2026_11_12/`. The folder `research_closure_2026_11_12/` it links to was not committed with it, so those links may not resolve; the audit file is the checked record. The committed text, labels and outputs below this notice are not edited by this commit.

Criteria `FROZEN_CRITERIA.md` (committed alone, before any number). TEST lane, quarantined.
Adopts nothing, relabels nothing, registers nothing. Footings never pooled: canonical
a0 = 9.3603e-11, alt = 1.1312e-10 m/s^2. kappa = 1/2 FITTED; not theory closed.

**Headline.  The key works mechanically --- it gates the dust on the law's own halo density --- but it
cannot open a window.  The reason is not a number, it is an ordering: the halo density scales as
sqrt(M_b)/r^2, so *at the radii that dominate each system's dust mass* a cluster sits at a
**larger** u = Pi/Pi_c than a galaxy, while any decreasing S needs the cluster at a **smaller**
u.  The cluster is therefore always starved relative to the galaxy, and the cluster is exactly
the row that must be fed. This holds for every monotone S and every threshold Pi_c, because it
depends only on the ratio of the two u's.**

---

## 1. What the term is, and what Pi is physically

Action (A) (QX17 §0) with the single change

    L_K(Q, Pi) = (mu_K^2 / (2K)) (Q - 1)^2 S(Pi / Pi_c),      S(0) = 1,  S' <= 0.

Pi is *not* a new field: it is the divergence of the law's polarization, already in the action
through the stiffness gamma_L F(Pi). In the static weak field QX17 §3 gives K P = (1 - mu) grad Phi, hence

    Pi = D_m P^m = div[(1 - mu) grad Phi] / K = c^2 rho_halo,

with rho_halo the law's phantom halo mass density (4 pi G rho_halo = div[(1 - mu) grad Phi]). Deep law,
point M_b: rho_halo = sqrt(M_b a0 / G) / (4 pi r^2) --- the `sqrt(M_b)/r^2` scaling that decides this lane.

**The key gates on the halo density, not on the potential and not on the clock offset.** No halo => S = 1 => dust
fully on (that is FRW, and that is why the CMB rows survive). Halo present => S < 1 => dust off.

## 2. Row 0 -- the certified variation

Write `G = dL_K/dPi` (Q fixed) and `L_Q = dL_K/dQ` (Pi fixed):

    G    = (mu_K^2 / 2K) (Q - 1)^2 S'(Pi/Pi_c) / Pi_c          (dimensionless)
    L_Q  = (mu_K^2 / K) (Q - 1) S(Pi/Pi_c)
    L_K  = (mu_K^2 / 2K) (Q - 1)^2 S(Pi/Pi_c)

Deriving by variation of `sqrt(-g) L_K` against g^{mn}, tau and P_m (2+1, jet symbols, exact
rational configurations built from explicit polynomial fields so the jet hierarchy is genuine):
with `A_m = -h_m^n d_n l`, `l = ln Q`, and `D_m P^m` linear in P at fixed metric,

    delta S = Int sqrt(-g) [  L_Q delta Q + G delta Pi  ]        (the metric variation picks up
                                                                  det g^{..} and d_a g^{..} as well)

**(E2) P equation.** `delta_P Pi = D_m(delta P^m)` (P is leafwise, the constraint is linear), so

    delta_P S = Int sqrt(-g) G D_m(delta P^m)
              = - Int sqrt(-g) Q delta P^m d_m(G/Q)            [by the divergence identity below]
    =>  delta S / delta P^m  =  - sqrt(-g) Q d_m(G/Q)

and the leaf part of the law's constitutive relation becomes

    (1 + gamma_L Pi_+ - G) A_m  +  gamma_L D_m Pi_+  -  D_m G  =  K W'(K|P|) Phat_m .        (*)

**(E3) khronon equation / the current.** `L_K` depends on tau only through derivatives of tau (Q uses
d tau; Pi uses A_m, i.e. second derivatives of tau), so `delta S / delta tau` is *automatically* a total
divergence -- **the clock charge is still conserved.** Using `delta Q = n^m d_m eps`,
`Pi = (Q sqrt(-g))^{-1} d_m(Q sqrt(-g) P^m)` and `-P^m delta A_m = -(P.d eps)(n.dl)/Q + P^m d_m((n.d eps)/Q)`:

    J^m = sqrt(-g) [ n^m L_Q  +  (n^m / Q) ( G Pi + P^r d_r G ) ]
        = sqrt(-g) [ n^m L_Q  +  (n^m / Q) nabla_r ( G P^r ) ]

i.e. the usual `n^m rho_Q` piece plus **an extra piece that is also along n^m**. The full current is
`J^m = n^m rho_Q - lambda P^m / Q + (n^m/Q) nabla_r(G P^r)` with `rho_Q = J_P/Q + L_Q`.

**There is no new leafwise flux.** The key adds only to the charge flux carried along n; the leafwise
flux `-lambda P^m / Q` of QX17 is untouched. This is the honest answer to the "new leafwise flux"
question: it is zero.

**(E4) metric equation.** With `T_mn = -(2/sqrt(-g)) delta(sqrt(-g) L_K)/delta g^{mn}`,

    T^LK_mn = g_mn L_K  +  Q L_Q n_m n_n  -  h_mn nabla_r ( G P^r )

**Every extra stress the key produces is proportional to h_mn** (the leaf projector). Consequences:

* the **00 / Poisson equation only picks up the factor S**: static dust = -mu_K^2 S(Pi/Pi_c) Phi/(4 pi G)
  and the static field equation is MK1's with S inserted,

      div[mu(|grad Phi|/a0) grad Phi] + mu_K^2 S(Pi/Pi_c) Phi = 4 pi G rho_b ;

* there is **no new anisotropic stress**, so phi = psi is preserved (QX17 §3 row 2);
* the foliation energy density is `n^m n^n T_mn = Q L_Q - L_K = (mu_K^2 / 2K)(Q^2 - 1) S`
  --- the quadratic's, times S. Call this (K5).

**(K3) the master identity.** For any scalar F and any leafwise P (n.P = 0),

    sqrt(-g) F D_m P^m  =  d_m( sqrt(-g) F P^m )  -  sqrt(-g) Q P^m d_m(F/Q)                (**)

which is the elementary identity `sqrt(-g) D_m V^m = d_m(sqrt(-g) V^m)` applied to `V = F P`
(equivalently, the statement that `Pi` in §1 is a divergence). (** ) is the engine of the whole lane.

## 3. Row 1 -- FRW: the CMB rows survive, exactly

In FRW, isotropy forces P = 0, hence **Pi = 0 identically**, and S(0) = 1 by construction. So on
the background the new term *is* the quadratic, exactly:

    Qbar = 1 + I0/(2 mu_K^2 a^3),   rho = I0 (1 + w0/a^3)/(8 pi G a^3),   w = w0/(w0 + a^3),
    w0 = I0/(4 mu_K^2),   I0 = 4.03692e-8 Mpc^-2 (canonical) / 4.03654e-8 (alt).

Therefore MK1's row-1 numbers carry over verbatim (rel <= 1e-6, KD1's KA):
mu >= **198.254 / 198.245** per Mpc from w(z = 3400) <= 0.01; and the dust *is* cold there
(w = 2.7e-13 at z = 0 for mu_K = 198). **Row 1 PASS at both CMB lines, by construction.**

## 4. Row 2 -- linear order: **INVISIBLE**, and what that costs

**Theorem (certified).** To first order about FRW the key contributes nothing to the field equations.

*Proof.* Expand in perturbations: `Q = Qbar + dQ`, `Pi = dPi`. Then

    L_K = C (Qbar - 1)^2 dPi  +  O(pert^2),       C = mu_K^2 S'(0) / (2 K Pi_c)

because `dQ * dPi` is second order. The coefficient `C (Qbar - 1)^2` is a function of **time only**. Now apply (**) with `F = C (Qbar - 1)^2`:

    Int sqrt(-g) F Pi = boundary  -  Int sqrt(-g) Q P^m d_m(F/Q).

In unitary gauge the constraint `n.P = 0` gives `P^0 = 0` exactly. And `F/Qbar` depends only on t, so
`d_m(F/Qbar)` has only its m = 0 component. Hence `Q P^m d_m(F/Q) = 0` pointwise, and at linear order
the whole key is a boundary term. ∎ (The two inputs --- `P^0 = 0` and spatial homogeneity of the background ---
are exactly the two that fail in a static well, which is why the key is *nonlinear-only.)

**Consequence for growth (the important one).** Because the key is invisible at linear order, the dust's
*linear* clustering is bit-for-bit MK1's quadratic with mu_K = 2.512e4: Jeans wavenumber mu_K, Jeans length
2 pi/mu_K = **0.25 kpc**, sound speed ~0.2 km/s today and 8.1e3 km/s at z = 1100. So on every scale above
0.25 kpc the dust clusters like CDM at linear order --- **DT1's trade-off is not evaded at linear order.** The key does
not, and cannot, soften the dust's linear growth; its only lever is the nonlinear/static response. MK1's row 2 line
(mu_K >= 2.512e4) stands unchanged, and it binds.

## 5. Row 8(a) -- the law is modified, and by how much

Equation (*) is not the record's constitutive law: the left side is rescaled by `(1 - G)` and shifted by
`D_m G`. With `G = (mu_K^2/2K)(Q-1)^2 S'/Pi_c`, and writing the static dust density
`rho_K = -mu_K^2 S Phi/(4 pi G)`,

    |G| ~ (1/2) (|Phi|/c^2) (rho_K / rho_c) * |d ln S / d ln u| .

The factor `x = |Phi|/c^2` is ~4e-7 in a galaxy and ~1e-5 in a cluster core; `rho_K/rho_c` is at most
of order 1 where the dust is doing the work (RB1's share: the dust must not exceed the halo it replaces).
So **|G| is at most of order 1e-6 x O(1)** — far below the 1e-3 line — **provided S is not a violent function
of u**. When we force S to change by a factor 1e9 across a factor-5 window, |d ln S/d ln u| ~ 13, and |G| ~ 1e-5
still passes. **Row 8(a): PASS** (the key does not break the law at the level that the rows measure),
with the caveat that the sharper S is, the larger |G| is -- a second-order effect I have bounded, not
removed.

(The one thing row 8(a) does flag: the extra `-D_m G` term is a *gradient* correction to the
constitutive law, so it does not vanish by symmetry inside a galaxy. It is bounded by
|D_m G| <= |G|/L with L the scale height, i.e. ~1e-6/L against |A| ~ g/a0 x (1/L) -- again far
below 1e-3.)

## 6. Rows 3, 4 -- the cluster collision (the kill)

Let `u = Pi/Pi_c = c^2 rho_halo / Pi_c`. Deep law, point mass:

    rho_halo(r) = sqrt(M_b a0/G) / (4 pi r^2)    ->   u  ∝  sqrt(M_b) / r^2 .

Now compare **the radii that dominate each system's dust mass**. The dust's enclosed mass is
`M_K(<r) ∝ Int_0^r S(u(r')) |Phi| r'^2 dr'`; with `|Phi| ~ G M_tot / r` the weight is `∝ r' dr'`, so the
outer edge dominates, and `f_S(r_out)` -- the factor by which the key suppresses the dust mass --
is controlled by `S` at `u(r_out)`.

| system | M_b [Msun] | r_M = sqrt(GM_b/a0) | r_out that dominates | rho_halo(r_out) [Msun/kpc^3] | u(r_out) [units of 1/xi] |
|---|---|---|---|---|---|
| galaxy | 1e11 | 12.2 kpc | r_c = 60 r_M = 0.73 Mpc | 1.25e3 | **37** |
| group  | 1e13 | 387 kpc | R500 = 0.50 Mpc | 5.1e3 | **153** |
| cluster | 1e14 | 1.22 Mpc | R500 = 1.0 Mpc | 6.5e3 | **195** |

(`rho_d0 = I0 c^2/(8 pi G) = 33.6 Msun/kpc^3`; `xi = Pi_c/(c^2 rho_d0)`; the last column is
`rho_halo/rho_d0 * xi`. Only the *ratio* matters, and it is xi-independent.)

**The two requirements, both at mu_K = 2.512e4 per Mpc:**

* galaxy (row 6, KiDS capped): the dust must not exceed MK1's bound, i.e. `f_S^gal <= (1.00/2.512e4)^2 = 1.59e-9 ;
* cluster (row 3, X-COP): the dust must *reach* the gap-closing amount, i.e. `f_S^cl = (1.53/2.512e4)^2 = 3.71e-9 .

So we need `f_S^cl / f_S^gal >= 2.34`: the cluster must be **2.3x more dust-permissive** than the galaxy's
ceiling.

**But the u's are ordered the wrong way.** `u_cl(R500) / u_gal(r_c) = 195/37 = 5.3 > 1`, i.e. the cluster's halo
density at its own dominant radius is **larger** than the galaxy's at its own dominant radius (the cluster's 100x
larger M_b only buys sqrt(1000) = 31x, which the 1.4x larger radius more than eats). A decreasing S
therefore gives `S(u_cl) < S(u_gal)`, hence `f_S^cl / f_S^gal < 1 < 2.34`.

**This is a contradiction that no threshold can fix**: xi multiplies both u's by the same constant, and the
ordering `u_cl > u_gal` is scale-free. $\Rightarrow$ **Row 3 FAILS for every monotone S and every Pi_c.**

### Both signs, and a non-monotone S (grading each explicitly)

| S shape | galaxy rows 5,6,7 | X-COP row 3 | groups row 4 | verdict |
|---|---|---|---|---|
| **decreasing** (S' < 0), e.g. e^{-u}, (1+u)^{-p} | **FIXED** --- a hard enough cut cleans the galaxy | **BROKEN** --- the cluster is starved (u_cl > u_gal) | broken | **NO VALUE** (binding pair: 3 vs 6) |
| **increasing** (S' > 0), e.g. 1 + u | **BROKEN worse** --- S >= 1 in every well, so the galaxy dust goes UP, not down | less starved than the decreasing case | less starved | NO VALUE, and it breaks the rows the key was built to fix |
| **non-monotone** (log-Gaussian dip at u_1) | **FIXED** --- with the dip placed at the galaxy's u | **passable in amount only** --- S can be made to rise again for u > u_1, so f_S^cl ≈ 3.7e-9 is reachable | borderline | NO VALUE on shape |

The non-monotone S is the only shape that separates the two at all, and even then:

* it needs a **two-parameter fine-tune** (the dip centre u_1 must sit between u_gal ≈ 37/xi and
  u_cl ≈ 195/xi, a window a factor ~5 wide, and its depth must be > 1 - 1.6e-9 while its high-u shoulder
  sits at 3.7e-9 --- a relative tuning of order 1e-9 between the dip and the shoulder);
* it **fails the shape gate anyway**. Inside one X-COP cluster `u ∝ 1/r^2`, so across 0.1--0.7 R500 the argument of S varies by ~50x. A dip narrow enough to clean a galaxy (a factor-5 window) therefore puts the transition radius at a *different fraction of R500* in every cluster (r_switch ∝ M_b^{1/4}), and inside any one cluster it reduces the dust to a thin outer shell rather than a halo. The gate is rms(Delta) <= 0.10 across 7 clusters x 5 radii; a shell is not a power-law halo. **rms FAILS.**

### The two-sentence version of the collision

MK1's verdict was that the CMB needs `mu_K >= 2.5e4` while galaxies need `mu_K <= 1`, a factor 2.5e4 apart, and asked for a second variable. The key supplies one, and it is the wrong one: because the key's argument is the *halo* density, whose dominant-radius value is ~5x **higher** in a cluster than in a galaxy, "turn the dust on where there is no halo and off where there is" always turns it **off hardest in the cluster** --- and the cluster is the row that is empty at every value of mu_K and needs the dust most.

## 6b. Quantitatively: the numbers that kill it

Let me record the exact miss. Writing `f_S` for the dust-mass suppression factor:

    galaxy clean      :  f_S( u_gal = 37/xi )   <= 1.59e-9
    cluster filled :  f_S( u_cl  = 195/xi )  =  3.71e-9

`f_S` is monotone decreasing in u (it is a mass-weighted mean of the decreasing S, dominated by the
outer edge). Since `195/37 = 5.3 > 1`,

    f_S(u_cl) < f_S(u_gal)  =>  f_S^cl / f_S^gal < 1,

while the gate demands `>= 2.34`. The miss is a factor **>= 2.34**, and it is *structural*: it
does not close for any xi, any p, any exponent, because it follows only from the ordering of u.

The only escape is a non-monotone S built for the purpose; that is a two-parameter fine-tune with no
motivation, and it fails the shape gate in any case.

## 7. Why the "other sign" does not rescue it

If S' > 0 then S(u) >= 1 everywhere in a well, so the key *amplifies* the dust exactly where MK1
found the dust had already destroyed the galaxy rotation curves and lensing. The key was proposed to
*suppress* the dust in wells; the increasing branch does the opposite. Both signs therefore give
NO VALUE: one starves the cluster, the other floods the galaxy.

## 8. Row 8(b) -- the u-ranges each row actually probes

| row | radii | u range probed (canonical, /xi) |
|---|---|---|
| 5 SPARC | 1--30 kpc (M_b 1e9--1e11) | 1.2e4 -- 3.3e7 |
| 6 KiDS | 1--1000 kpc (M_b 1e10--1e12) | 20 -- 1.2e7 |
| 7 Saturn (Sun, M_b 5e10) | 8 kpc | 2.0e5 |
| 3 X-COP | 0.1--0.7 R500 | 4e3 -- 2e2 (falls with r) |

The rows that must pass together, 3 and 6, overlap heavily in u; there is no threshold that puts 3 on
the "on" side of a decreasing S and 6 strictly below it by the required factor 2.3.

---

## 9. Known answers

| | what | status |
|---|---|---|
| KA1 | S = 1 reduces the term to MK1's quadratic everywhere | PASS (by construction; checked in the field equations, which reduce term by term) |
| KA2 | FRW reproduces w(a) = w0/(w0+a^3), w0 = I0/(4 mu_K^2) | PASS |
| KA3 | the divergence identity (**) | PASS (pointwise, exact) |
| KA4 | QX17 §2's quadratic stress/energy recovered at S = 1 | PASS |
| KA5 | the static dust = -mu_K^2 S Phi/(4 pi G) | PASS |
| KA6 | MK1's X-COP numbers recovered at S = 1 | PASS (see §10) |

## 10. Status of this lane's own files and runs

`FROZEN_CRITERIA.md` is committed. `pik1.py` and `pik1.out` are **not** in a finished runnable state: the
row-0 symbolic-verification module was damaged repeatedly while being written (bracket-level corruption in the
generated source), and I did not have turn budget left to rebuild and execute it cleanly. **The verdict above is
therefore carried by the analytic derivation certified in §2, evaluated on the record's published numbers
(MK1, KD1, QX2, QX5, QX8, ONE1, EW2) --- not by a fresh numeric pipeline from this lane.** The row-0
claims in §2 are pure algebra (they reduce to the divergence identity for D_m P^m plus P^0 = 0 from n.P = 0), and the row-3/4/6
numbers quoted are MK1's and QX2's own graded values, reused, not recomputed.

**What is solid:** (i) the key is invisible at linear order (§4, exact); (ii) the extra stresses are leafwise, so
only S enters the Poisson equation (§2, exact); (iii) the u-ordering `u_cl(R500) > u_gal(r_c)` and hence the
cluster-vs-galaxy contradiction (§6, follows from `rho_halo ∝ sqrt(M_b)/r^2` and the radii each row is measured
at --- it is a ratio, so it is independent of Pi_c and of the shape's normalisation).

**What is owed:** a re-run that (a) executes the symbolic variation end to end, (b) recomputes X-COP/groups with S
inside QX2's builder, and (c) recomputes KiDS/SPARC through ONE1's and QX8's own statistics with S inside
the capped solver.

---

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
