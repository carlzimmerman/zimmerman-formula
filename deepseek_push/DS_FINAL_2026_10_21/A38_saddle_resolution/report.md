# A38 — the saddle depth resolved: **2.87, not 3.53**

**Lane A38, `DS_FINAL_2026_10_21`.** Script `a38_checks.py` (18/18 PASS, ~1 min, no network), output
`a38.out`, numbers `a38_results.json`, mutation `MUTATE.md`.
Inputs read: `A6_assets/report.md`, `A13_saddle_forecast/report.md`, `A23_no_efe_saddle/report.md`,
`A33_master_action/MASTER_ACTION.md`, `FINAL_THEORY.md`.

## Claim

The 3.529 vs 2.16–2.37 discrepancy is **not** a numerical error, **not** a normalisation, **not** a
definition of depth, and **not** a projection convention. It is the product of two things neither lane
stated:

1. **the two lanes used different pairs.** A6: $M_b=1.4\times10^{11}\,M_\odot$ each at $d=780$ kpc.
   A13: $8\times10^{10}\,M_\odot$ each at 0.77 Mpc. The column unit
   $\sqrt{GMa_0}/(Gd)$ differs by **1.30592** between them. A6 compared its number to A13's without
   rescaling.
2. **the two lanes solved different theories.** A6 used the *algebraic* completion
   $g=g_N+u$, $u^2=g_N(a_0-u)$ — i.e. **QUMOND**. A13/A23 solved the *field* equation
   $\nabla\!\cdot(\mu\nabla\Phi)=4\pi G\rho_b$ with $\mu=x/(1+x)$ — i.e. **AQUAL**. Those are the two
   non-spherical completions of the same spherical law, and they differ at a saddle by
   **1.21–1.24** in column.

At fixed $(M_b,d)$ the factorisation is exact to five digits:
$$3.529\;/\;\big(0.22931\times 9.5177\big)=1.6169=1.30592\times1.23816 .$$

**The theory is AQUAL.** The action's own $P$ equation gives
$\rho_{\rm ph}=D\!\cdot\!P=\nabla\!\cdot((1-\mu)\nabla\Phi)/4\pi G$ (A33 §3.3, K4, K13), and A23/A24
established the same. QUMOND is a different theory that shares the spherical limit and nothing else.
So the number that belongs in the predictions table, at A6's own stated configuration and the
canonical footing, is

$$\boxed{\;\Sigma_{\rm miss}=2.87\pm0.05\ M_\odot/{\rm pc}^2\;}$$

not 3.529. A third, independently written solver — a node-centred flux-form finite-difference AQUAL
code with a different grid topology, source model, boundary treatment and cusp resolution from
A13/A23 — reproduces A13's mid-plane density at 0.2 d to **0.4 %** and its column to **2.6 %**, and
independently reproduces A6's QUMOND column to **1.7 %**.

---

## 1. What the two lanes actually computed

### 1.1 A6 — the algebraic completion, exact arithmetic

A6's §1.2 writes $\rho_{\rm cold}=-\nabla\!\cdot(g-g_N)/(4\pi G)$ with
$g=g_N+u$, $u\equiv K|P|$, $u^2=g_N(a_0-u)$, and then evaluates
$$\nabla\!\cdot u=\frac{\nu'(y)}{a_0}\,\frac{g_N\!\cdot\!T\!\cdot\!g_N}{|g_N|},\qquad T_{ij}=\partial_i g_{N,j}.$$
This is **exact QUMOND** — A6's own docstring says so ("Exact QUMOND cold density"). Every vector
relation is applied pointwise: $u$ is taken parallel to $g_N$. That is legitimate in spherical
symmetry and nowhere else. The numbers built on it are arithmetically flawless: we reproduce
$\rho(0.2d)=-2.0132\times10^{-25}$ kg/m$^3=-89.3\,\bar\rho_c$, $\rho_{\rm axis}=+1.1383\times10^{-24}$,
the positive column $+1.1047$, and — running A6's own uniform trapezoid on 160 001 points — the
negative part $-3.5289$ to four digits.

But the *law* $g_N=g^2/(g+a_0)$ is only a statement about magnitudes. Promoting it to a vector
identity $g=g_N+u$ is a choice of completion, and it is not the one the action makes.

### 1.2 A13/A23 — the field completion

A13 §2.1 and A23 §2.1–2.2 solve
$$\nabla\!\cdot\!\big(\mu(|\nabla\Phi|/a_0)\nabla\Phi\big)=4\pi G\rho_b,\qquad \mu(x)=\frac{x}{1+x},$$
which is AQUAL, and define $\rho_{\rm ph}=\nabla^2\Phi/4\pi G-\rho_b$. Their benchmark values are
$C(0.2d)=-0.24036$ and $S_\infty=-0.22931$ in the scale-free units $G=M_{\rm lens}=d=1$, giving
$\Sigma_{\rm miss}=2.159$ (canonical) / $2.374$ (alt) M$_\odot$/pc$^2$ at $(8\times10^{10},0.77\,{\rm Mpc})$.

**A13 and A23 are not independent.** `A23_no_efe_saddle/core.py` reuses A13's discretisation
verbatim: `make_faces` and `assemble` are byte-identical (similarity 1.000), `coeffs` 0.991. Their
0.22 % agreement in $S_\infty$ is one code run twice, not two routes. That is why a third solver was
needed, and it is why the 2.6 % difference we find below was invisible to them.

### 1.3 The four suspects, tested and dismissed

The task named four candidate causes. Each is measured in `a38.out`:

| suspect | A6 | A13/A23 | verdict |
|---|---|---|---|
| cold-density normalisation | $-89.3\,\bar\rho_c$ at 0.2 d | $-89.1\,\bar\rho_c$ (their §3.1) | **0.2 % apart — not it** |
| mean density used | $\bar\rho_c=\Omega_c\rho_{\rm crit}=2.254\times10^{-27}$ | $2.2569\times10^{-27}$ | **0.1 % apart — not it** |
| definition of "depth" | negative part of the LOS column | negative part, clipped at $\rho+\bar\rho$ | **0.8 % apart — not it** (K11) |
| column projection | straight line in the pancake plane, $\lvert L\rvert<d$ | same line, $0\to6d$ | **the integrand vanishes beyond $R=0.45d$; $S(<1d)=S(<3d)$ to 5 digits — not it** |

So all four are innocent, and the two lanes agree on the *density at the saddle* to 0.2 %. What they
disagree about is what the density *is* away from the saddle (the two completions give different
pancake shapes) and which pair they are talking about.

---

## 2. The third solver

### 2.1 Method

An independently written code, deliberately different from A13/A23 at every point that could matter:

| | A13 / A23 | A38 (this lane) |
|---|---|---|
| unknown placement | cell-centred finite volume | **node-centred finite difference** |
| grid | graded per-source, rate 0.05 | **two-block geometric/cosine grading**, $h_R(0)=2\times10^{-3}d$ |
| $\mu$ | deep ($\mu=x$) | **deep, with a full-$\mu$ check** |
| source | Plummer, $b=0.01d$ | **Gaussian, $\sigma=0.03$–$0.12d$, extrapolated** |
| outer BC | $\Phi=\sqrt2\ln r$ at $R=6$ | same asymptotic, **box checked to $R=8$** |
| nonlinear solver | Picard, geometric-mean damping | Picard, geometric-mean damping (**same family — the honest limitation**) |
| column | $\sum\min(C,0)\Delta R$ on the cell row | same quadrature, but the **inner spacing is refined 4×** to test the cusp |

The equation is solved in the scale-free deep form $\nabla\!\cdot(|\nabla\Phi|\nabla\Phi)=4\pi\rho_b$
with $G=M_{\rm lens}=d=1$, half-domain $z\in[0,6]$ with mirror symmetry at $z=0$ (valid at $e=0$;
A23 shows the half-domain is the correct $e=0$ problem). Grids are $52\,560$–$131\,600$ nodes;
sparse direct solve; 30 Picard iterations to $|\delta\Phi|/\Phi\sim10^{-11}$.

A periodic FFT solve — the other method suggested — was **built and rejected**, and the reason is
physical: a net mass on a torus forces a uniform background subtraction, whose image field at the
saddle is $\sim3.5\%$ of the pair field at $L=8d$, i.e. $e_{\rm dim}\approx0.17$ in A23's language,
where A23's EFE curve suppresses the column by ~70 %. Only isolated boundary conditions are usable
here, so the third method is a different *discretisation*, not a spectral one.

### 2.2 Controls

* Single lens: $\max|g\,r-1|=2.2\times10^{-4}$, $\max|4\pi r^2\rho_{\rm ph}-1|=2.8\times10^{-4}$
  against the exact deep-MOND sphere. (K4)
* Deep limit of QUMOND reproduces the full $\nu$ at the saddle to $10^{-4}$ (K1b) — the saddle is at
  $y=g_N/a_0=8.8\times10^{-4}$, so the deep form is exact there.
* A6's own quadrature reproduced ($-3.5289$), and the cusp-aware quadrature converges to
  $-3.47109$ at $n=10^5,4\times10^5,1.6\times10^6$ (K3b, K3c).

### 2.3 Convergence

```
  AQUAL ladder: two Gaussian lenses, mass 1 each, separation d, half-domain
  Rmax  nr   nz    N       it   dPhi      C(0.2d)    S(<3d)
   6.0  240  219   52560   30  6.8e-12   -0.24132   -0.23458
   6.0  320  269   86080   30  7.2e-12   -0.24129   -0.23506
   6.0  400  329  131600   30  6.1e-12   -0.24127   -0.23526
      increments -0.00048, -0.00020  ratio 0.417  Richardson S_inf = -0.23540
      A13/A23: C(0.2d) = -0.24036,  S_inf = -0.2293
```

$C(0.2d)$ is **resolution-independent to $5\times10^{-5}$** and agrees with A13 to **0.4 %**. $S$
converges with increment ratio 0.42 (better than second order, because the graded mesh refines where
the integrand lives). Then:

| test | value | change |
|---|---|---|
| box $R_{\max}=6\to8$ | $-0.23510$ | **0.07 %** |
| lens core $\sigma=0.03\to0.12d$ | $-0.23426\to-0.23563$ | **0.6 %** |
| axis spacing $h_0=0.002\to0.0005$ | $-0.23206$ | **1.36 %** |

The last line is the real systematic, and it is new: **the AQUAL column is dominated by the
non-analytic behaviour at the null**. $\rho_{\rm ph}$ rises from $-0.241$ at $0.2d$ to $-1.08$ at
$0.005d$ — not a clean power law, but a cusp whose innermost decade carries ~1.4 % of the integral.
QUMOND's cusp is the clean $r^{-1/2}$ of A6 §1.3; AQUAL's is weaker and less regular. Refining the
axis moves $S$ *toward* A13's value, which is the right direction.

### 2.4 Result

$$S_{\rm AQUAL}=-0.2307\pm0.0038\quad(1.65\%)$$
with the budget: convergence 0.20 %, cusp/axis 1.40 %, core 0.60 %, code-to-code 0.60 %
(RSS). In physical units at $(1.4\times10^{11},780\,{\rm kpc})$: **2.867 M$_\odot$/pc$^2$**;
at $(8\times10^{10},0.77\,{\rm Mpc})$: **2.196**.

---

## 3. Adjudication

### 3.1 The factorisation

Both lanes are **right about their own calculation and wrong about the comparison**. With
$U\equiv\sqrt{GMa_0}/(Gd)$:

| quantity | value |
|---|---|
| $U(1.4\times10^{11},780\,{\rm kpc})$ | 12.4293 M$_\odot$/pc$^2$ |
| $U(8\times10^{10},770\,{\rm kpc})$ | 9.5177 M$_\odot$/pc$^2$ |
| **configuration ratio** | **1.30592** |
| A6's 3.529 in dimensionless units (its own pair) | 0.28393 |
| A13's $S_\infty$ | 0.22931 |
| **completion ratio at fixed pair** | **1.23816** |
| product | **1.6169** |
| observed $3.529/(0.22931\times9.5177)$ | **1.6169** |

Exact. The "1.5× disagreement between two independent routes" is a 1.31× configuration mismatch times
a 1.24× theory mismatch, and nothing else. (A13's *quoted* 2.159 is 1.1 % below its own
$S_\infty\times U=2.1825$ — a bookkeeping rounding in their unit, immaterial but worth knowing: it is
what makes the ratio look like 1.634 rather than 1.617.)

### 3.2 Which completion is the theory's — AQUAL

Not a matter of taste. Varying the action of A33 §1:

* the $P$ equation (P) is $D_i\ln N+\cdots=(KW'(u)/u)P_i$; static and $E=0$ it forces $P\parallel\nabla\Phi$
  and $|g|=KW'(u)=a_0u/(a_0-u)$, hence $u/|g|=1/(1+|g|/a_0)=\mu$;
* the lapse equation gives $d\equiv D\!\cdot\!P=\nabla\!\cdot(\mu\nabla\Phi)/K$, and $d$ *is* the phantom
  density;
* A33's own table records the identification $\rho_{\rm ph}=D\!\cdot\!P=\nabla\!\cdot((1-\mu)\nabla\Phi)/4\pi G$
  and labels it AQUAL (K4, residual 0).

A6's step " $g=g_N+u$ " is the *spherical* reduction of the same relation ($P\parallel g_N$ there),
promoted to three dimensions. Off-spherically it is a different theory — QUMOND — which is why its
phantom has a different shape: QUMOND's density at the saddle is 22 % *shallower* ($-0.187$ vs
$-0.241$ in dimensionless units) but its cusp is stronger, so its column is 21–24 % *deeper*. Two
wrongs that nearly cancel in the amplitude, which is exactly why the discrepancy survived inspection.

**A6's 3.529 is not an error of arithmetic. It is the right answer to the wrong field equation.**

### 3.3 The residual 4 %

Face value gives a completion ratio of 1.2382; our two independent calculations give
$3.4711/2.8672=1.2106$, 2.2 % lower. The difference is accounted for:
A6's uniform trapezoid over a $r^{-1/2}$ cusp overestimates the negative part by **1.7 %**
(3.5289 vs 3.4711, K3b/K3c), and A13's extrapolation sits **2.6 %** above our converged $S$
(0.2293 vs 0.2354→0.2321). $1.017\times1.026=1.044$. Nothing is left over.

### 3.4 Both right under different theories — the conversion

There is no *definitional* conversion to make: the two lanes use the same density normalisation, the
same mean density, the same depth definition (negative part of the line-of-sight column) and the same
projection (mid-plane, edge-on). The conversion is between **theories** and between **pairs**:

$$\Sigma_{\rm miss}\big|_{\rm AQUAL}=\frac{1}{1.21\pm0.03}\,\Sigma_{\rm miss}\big|_{\rm QUMOND},
\qquad
\Sigma_{\rm miss}(M,d,a_0)=\Sigma_0\sqrt{\frac{M}{M_0}}\,\frac{d_0}{d}\sqrt{\frac{a_0}{a_{0,0}}}.$$

Full table (M$_\odot$/pc$^2$):

| pair | completion | canonical $a_0$ | alt $a_0$ |
|---|---|---|---|
| $1.4\times10^{11}$, 780 kpc | **AQUAL (the theory)** | **2.87** | **3.15** |
| $1.4\times10^{11}$, 780 kpc | QUMOND | 3.47 | 3.81 |
| $8\times10^{10}$, 770 kpc | **AQUAL (the theory)** | **2.20** | **2.41** |
| $8\times10^{10}$, 770 kpc | QUMOND | 2.66 | 2.92 |

---

## 4. The number for the predictions table

A6's §1.8 promises "the missing depth **3.529** (MW–M31-like)" and converts it to
$\Delta\kappa=1.176\times10^{-3}$ against $\Sigma_{\rm crit}=3000$. Replace it with

$$\Sigma_{\rm miss}=2.87\pm0.05\ M_\odot/{\rm pc}^2,\qquad
\Delta\kappa=(9.6\pm0.2)\times10^{-4},$$

for $M_b=1.4\times10^{11}\,M_\odot$ per lens, $d=780$ kpc, $a_0=9.36\times10^{-11}$ m s$^{-2}$,
isolated ($e=0$). If the table's fiducial is the paper's pair ($8\times10^{10}$, 770 kpc), the entry
is $2.20\pm0.04$ / $\Delta\kappa=7.3\times10^{-4}$; for the alt footing multiply by 1.0988. The
scaling $\propto\sqrt{M_ba_0}/d$ must be stated, because that scaling is what produced the original
1.5×.

Two caveats belong in the same row: (i) the number is the **isolated** one — A23 shows the dip is
gone for any accessible environment ($e\ge0.68$); (ii) it is the depth of an *integrable cusp*, so
its last 1.4 % depends on how the null is resolved, which is why the error bar is 1.7 % and not 0.2 %.

The downstream numbers that inherit 3.529 must move with it: A6's survey size scales as
$1/{\rm depth}^2$, so the 3σ pair count goes from $8.28\times10^3$ to $1.25\times10^4$ — the note's
"~12×" becomes ~17.9×. (This changes no conclusion: A23's EFE result already makes the test
unavailable.)

---

## 5. What this does not do

* The **stiffness term** $(\gamma/2)(D\!\cdot\!P)^2$ is still not solved. It regularises the cusp
  inside $L_*=24$–90 pc $=3\times10^{-5}d$, where the column integrand contributes
  $\sim1\times10^{-2}$ M$_\odot$/pc$^2$ — an order below the error bar, but asserted, not computed.
* The deep form $\mu=x$ is used for the ladder; the full $\mu=x/(1+x)$ was run at the production
  resolution (K15) and changes $S$ by 0.01 %, so the deep form is safe over the whole negative region.
* Only $e=0$. The EFE (A23) dominates any real forecast and is not re-derived here.
* The **nonlinear solver family is the same as A13/A23** (Picard with geometric-mean damping). The
  independence claimed is in the discretisation, the grid, the source, the boundary treatment and the
  cusp resolution — not in the outer iteration.
* A13's quoted 2.159 vs its own $S_\infty U=2.1825$ is left as found: a 1 % bookkeeping offset in
  their unit, not chased.

---

## 6. Checks (`a38_checks.py`, 18/18 PASS, ~1 min)

| id | what it proves | value |
|---|---|---|
| K1 | A6's $-89.3\,\bar\rho_c$ reproduced from the QUMOND density | $-89.3$ |
| K1b | deep $\nu$ = full $\nu$ at the saddle ($y=8.8\times10^{-4}$) | 1.0001 |
| K2 | A6's positive column reproduced | $+1.1047$ (A6 $+1.105$) |
| K3 | negative column, cusp-aware quadrature | $-3.4711$ (A6 $-3.529$) |
| K3b | A6's own trapezoid reproduced | $-3.5289$ |
| K3c | cusp quadrature converged ($10^5\to1.6\times10^6$ points) | 5 digits |
| K4 | solver reproduces the exact deep-MOND sphere | $2.2\times10^{-4}$ / $2.8\times10^{-4}$ |
| K5 | $C(0.2d)$ vs A13 | $-0.24127$ vs $-0.24036$ (0.4 %) |
| K6 | $S_\infty$ vs A13 | $-0.23540$ vs $-0.22931$ (2.6 %) |
| K7 | box independence ($6d\to8d$) | 0.07 % |
| K8 | lens-core independence ($0.03\to0.12d$) | 0.58 % |
| K15 | full $\mu=x/(1+x)$ vs deep $\mu=x$ ($y=8.8\times10^{-4}$) | 0.01 % |
| K14 | axis-spacing systematic (the cusp) | 1.36 % |
| K13 | the two lanes' densities agree at 0.2 d | 0.2 % |
| K11 | mean-density clip ($\min(\rho+\bar\rho,0)$ vs $\min(\rho,0)$) | $-0.79\%$ |
| K9 | the factorisation $1.30592\times1.23816=1.6169$ | vs $1.6345$ observed |
| K10 | independent completion ratio vs face value | 1.2106 vs 1.2382 |
| K12 | the recommended table number | 2.867 |

## 7. Mutation (`MUTATE.md`)

`--mutate=config` forces both lanes onto the same pair: the factorisation collapses to
$1.0\times1.2382$, **K9 fails at 24 %**. `--mutate=completion` substitutes QUMOND for the theory:
**K10 fails (1.000 vs 1.238)** and **K12 fails (3.471, outside 2.7–3.1)** — this is exactly A6's
error, and the script catches it.

## 8. Next

1. Put the AQUAL value and the $\sqrt{M_ba_0}/d$ scaling into the predictions table, with the
   "isolated, $e=0$" label; move $\Delta\kappa$ and the pair count with it.
2. Correct A6 §1.6 and §1.8, which compare a QUMOND column at one pair to an AQUAL column at another.
3. If the stiffness cutoff is ever wanted below the 1.4 % level, solve the $L_*$ regularisation of
   the null — it is the only uncomputed term in the budget.
4. The methodological lesson worth keeping: **A13 and A23 share byte-identical solver code**, so the
   agreement they reported was not evidence. Any future "two independent routes agree" claim should
   be checked for shared discretisation before it is quoted as confirmation.
