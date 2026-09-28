# AS023 — Footing sensitivity of physical radii and pressures: derivation and checks

**Run:** `AS023-20260928T0008Z-dsv4f-01`
**Worker:** deepseek/deepseek-v4-flash-0731 (provider: openrouter; Hermes Agent subagent platform,
slot `sa-2-8c1bd8df` per `claims/AS023.json` dispatch record)
**Branch:** CORE scale identities (Group A01); Q appears ONLY as a labelled comparison kernel
(regime limits); no RAR/MU2/EXP/MONO branch is used or transferred (criterion-B/operative
target untouched).
**Task source hash:** `5ddf03f918e0bd961087b8005e28480fd64612d734bf8f049cb2481fcf72a712`
(matches `claims/AS023.json` reservation).
**Sources inspected — hashes verified against SOURCE_MANIFEST.json, all match:**
`91a5fac4…` README.md · `98d9149f…` FRIED_CHICKEN_SPEC.md · `8da8176e…` campaign_fresh_gravity_astra/DERIVATIONS.md
· `ca696c7f…` FRAMEWORK_CONTRACT.md · `621fdad0…` RESULT_CONTRACT.json.

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

### 1.1 Symbols and units (SI)

| symbol | meaning | units |
|---|---|---|
| $a_0$ | vacuum acceleration scale; two separately labelled footings $a_{0,\mathrm{can}}=9.3619\times10^{-11}$, $a_{0,\mathrm{alt}}=1.1279\times10^{-10}$ | $\mathrm{m\,s^{-2}}$ |
| $\kappa$ | normalization of $a_0=\kappa c\sqrt{G\rho_\Lambda}$ — **adopted input** $=1/2$ | — |
| $q$ | footing ratio $a_{0,\mathrm{alt}}/a_{0,\mathrm{can}}=1.204776808126555\ldots$ | — |
| $G,c,M_b,M_\odot$ | Newton constant $6.67430\times10^{-11}$, light speed $299792458$, baryonic/test mass, solar mass $1.98847\times10^{30}$ | SI |
| $\rho_\Lambda,\varepsilon_L,\Lambda$ | vacuum mass density $4a_0^2/(Gc^2)$, energy density $4a_0^2/G$, same-$G$ curvature $32\pi a_0^2/c^4$ (bookkeeping at given $a_0$, $\kappa=1/2$ fixed) | $\mathrm{kg\,m^{-3}}$, $\mathrm{J\,m^{-3}}$, $\mathrm{m^{-2}}$ |
| $r_M$ | MOND radius $\sqrt{GM_b/a_0}$ | m |
| $C$ | deep-law coefficient $\sqrt{GM_b a_0}=v_{\mathrm{flat}}^2$ | $\mathrm{m^2\,s^{-2}}$ |
| $v_{\mathrm{flat}}$ | deep flat speed, $v_{\mathrm{flat}}^4=GM_b a_0$ | $\mathrm{m\,s^{-1}}$ |
| $\sigma$ | velocity dispersion (deep equilibrium), $\sigma^2=C/2$ (conditional input) | $\mathrm{m\,s^{-1}}$ |
| $\rho_{\mathrm{ph}}$ | phantom/equilibrium mass density $C/(4\pi G r^2)$ (conditional input) | $\mathrm{kg\,m^{-3}}$ |
| $P$ | equilibrium pressure $\sigma^2\rho_{\mathrm{ph}}$ (conditional input) | Pa |
| $x$ | dimensionless radius $r/r_M$ | — |
| $y$ | Newtonian argument $B/a_0$, $B=GM_b/r^2$ | — |
| $M_{\mathrm{ph}}(<r)$ | enclosed phantom mass $\int_0^r\rho_{\mathrm{ph}}4\pi s^2\,ds=Cr/G$ | kg |

### 1.2 Precise claim (conditional theorem)

Let $a_0,G,M_b,r$ be positive reals with the units above, and define $r_M=\sqrt{GM_b/a_0}$,
$C=\sqrt{GM_b a_0}$, $q=a_{0,\mathrm{alt}}/a_{0,\mathrm{can}}$. Subject to the task-declared
conditional deep-equilibrium inputs $\rho_{\mathrm{ph}}=C/(4\pi G r^2)$, $\sigma^2=C/2$,
$P=\sigma^2\rho_{\mathrm{ph}}$ and the framework definitions, **every physical output $O$ of the
CORE cell is an exact power law $O \propto a_0^{\,p}$ at fixed physical $r$ or at fixed
$x=r/r_M$, with footing conversion $O_{\mathrm{alt}}/O_{\mathrm{can}}=q^{\,p}$**, per the table
in §2. The alternative footing at fixed $\kappa=1/2$ carries a different vacuum density
(ratio $q^2=1.45148716$); the fixed-density cell (same $\rho_\Lambda$) requires
$\kappa_{\mathrm{eff}}=q/2=0.60238840$ and leaves $\rho_\Lambda,\varepsilon_L,\Lambda$
invariant. Exactly six output channels are footing-invariant ($p=0$, exact): the
$x$-anchored enclosed phantom mass $M_{\mathrm{ph}}(<x r_M)=xM_b$, the dimensionless
$x$-profile $y(x)=1/x^2$, the fixed-$r$ baryonic acceleration $B$, $\sigma/v_{\mathrm{flat}}=1/\sqrt2$,
$P(r_M)/\varepsilon_L=1/(32\pi)$, and $v_{\mathrm{flat}}^4/(GM_b a_0)=1$.

**Domain.** $r\in(0,\infty)$, $M_b\in(0,\infty)$, $x\in(0,\infty)$; all identities exact in real
arithmetic (no expansion, no neglected leading term in the CORE table). Regime statements
(Q-comparison only, §3.3) carry their own stated domains $x<1$ (Newtonian) and $x>1$ (deep).

**Framework inputs vs conclusions.** *Inputs (adopted, not derived here):* $\kappa=1/2$, both
$a_0$ footings, $G,c,M_\odot$, the definitions of $r_M,C,v_{\mathrm{flat}}$, and the
conditional deep-equilibrium relations (contract: finite boundaries, source coupling,
normalization, equilibrium formation and the possible double counting of the logarithmic well
are separate obligations). *Conclusions established:* the complete footing-sensitivity
exponent table (CORE), the fixed-r vs fixed-x structural difference, the fixed-density cell
bookkeeping, the uncertainty classification, and the negative control.

### 1.3 Prior-art reuse (not re-derived)

- **AS010** (`results/AS010/AS010-20260927T200531Z-dsv4f-01`, Lean-certified):
  $P(r_M)=a_0^2/(8\pi G)=\varepsilon_L/(32\pi)$, $P(r)=P(r_M)(r_M/r)^2$, linearity in the
  $\sigma^2=\eta C$ normalization. Reused as the $x=1$ row of this table.
- **AS011** (`results/AS011/run_20260927T224056Z`): the two mutually exclusive one-cell
  footing models ($R_a=1.2047768081\ldots$; fixed-density $\kappa_{\mathrm{alt}}=R_a/2=0.6023884040\ldots$;
  fixed-$\kappa$ density ratio $R_a^2$). Reused as the cell bookkeeping (this task's §4).
- **AS007** (`results/AS007/AS007-r1-20260927T2011-fc399d`): $v_{\mathrm{flat}}^4=G_N M_b a_0$
  and the log-sensitivity $d\ln v=(d\ln G_N+d\ln M_b+d\ln a_0)/4$.
- **AS016** (`results/AS016/run_20260927T2233Z`): $P(r)=M_b a_0/(8\pi r^2)$,
  $P(r_M)=a_0^2/(8\pi G)$ density-mapping identification.

---

## 2. Exact scaling tables (task step 2) — fixed physical radius vs fixed $x=r/r_M$

### 2.1 Derived closed forms

From $C^2=GM_b a_0$ and $r_M^2=GM_b/a_0$ (hence $C^2=a_0^2 r_M^2$, theorem `as023_C_sq_a0rM`):

$$r_M=k a_0^{-1/2},\ k=\sqrt{GM_b};\qquad
v_{\mathrm{flat}}=(GM_b)^{1/4}a_0^{1/4};\qquad C=\sqrt{GM_b}\,a_0^{1/2};\qquad \sigma=(GM_b/2)^{1/4}a_0^{1/4}.$$

$$ \rho_{\mathrm{ph}}(r)=\frac{\sqrt{GM_b}\,a_0^{1/2}}{4\pi\sqrt G\,r^2}
   \qquad(\text{fixed }r,\ p=\tfrac12),\qquad
   \rho_{\mathrm{ph}}(x r_M)=\frac{a_0^{3/2}}{4\pi\,G^{3/2}\sqrt{M_b}\,x^2}
   \qquad(\text{fixed }x,\ p=\tfrac32),$$

$$P(r)=\frac{M_b a_0}{8\pi r^2}\quad(\text{fixed }r,\ p=1),\qquad
P(x r_M)=\frac{a_0^2}{8\pi G\,x^2}\quad(\text{fixed }x,\ p=2,\ \text{independent of }M_b),$$

$$M_{\mathrm{ph}}(<r)=\frac{Cr}{G}=\frac{\sqrt{M_b a_0/G}}{1}\,r\qquad(p=\tfrac12\text{ at fixed }r),\qquad
M_{\mathrm{ph}}(<x r_M)=xM_b\qquad(p=0:\ \text{footing-invariant}),$$

$$y(x)\equiv\frac{B(x r_M)}{a_0}=\frac{1}{x^2}\quad(p=0),\qquad
y(r)=\frac{GM_b}{a_0 r^2}\quad(p=-1),\qquad B(r)=\frac{GM_b}{r^2}\quad(p=0).$$

### 2.2 The exponent table (fixed $\kappa=1/2$; $q=1.2047768081\ldots$; measured ratios mpmath-60)

| # | output | form | $p$ | $O_{\mathrm{alt}}/O_{\mathrm{can}}=q^p$ | $\Delta\%$ |
|---|---|---|---|---|---|
| 1 | $r_M$ | $\sqrt{GM_b}\,a_0^{-1/2}$ | $-\tfrac12$ | 0.9110594151 | −8.8941 |
| 2 | $v_{\mathrm{flat}}$ | $(GM_b)^{1/4}a_0^{1/4}$ | $\tfrac14$ | 1.0476751663 | +4.7675 |
| 3 | $C=v_{\mathrm{flat}}^2$ | $\sqrt{GM_b}\,a_0^{1/2}$ | $\tfrac12$ | 1.0976232542 | +9.7623 |
| 4 | $\sigma$ | $\sqrt{C/2}$ | $\tfrac14$ | 1.0476751663 | +4.7675 |
| 5 | $\rho_\Lambda=4a_0^2/(Gc^2)$ | $\propto a_0^2$ | $2$ | 1.4514871574 | +45.1487 |
| 6 | $\varepsilon_L=4a_0^2/G$ | $\propto a_0^2$ | $2$ | 1.4514871574 | +45.1487 |
| 7 | $\Lambda=32\pi a_0^2/c^4$ | $\propto a_0^2$ | $2$ | 1.4514871574 | +45.1487 |
| 8 | $\rho_{\mathrm{ph}}$ fixed $r$ | $\propto a_0^{1/2}$ | $\tfrac12$ | 1.0976232542 | +9.7623 |
| 9 | $\rho_{\mathrm{ph}}$ fixed $x$ | $\propto a_0^{3/2}$ | $\tfrac32$ | 1.3223910407 | +32.2391 |
| 10 | $P$ fixed $r$ | $\propto a_0$ | $1$ | 1.2047768081 | +20.4777 |
| 11 | $P$ fixed $x$ (incl. $P(r_M)$) | $\propto a_0^2$ | $2$ | 1.4514871574 | +45.1487 |
| 12 | $M_{\mathrm{ph}}(<r)$ fixed $r$ | $\propto a_0^{1/2}$ | $\tfrac12$ | 1.0976232542 | +9.7623 |
| 13 | $M_{\mathrm{ph}}(<x r_M)$ | $=xM_b$ | $0$ | **1.0000000000** | **0 (invariant)** |
| 14 | $y(x)$ | $=1/x^2$ | $0$ | **1.0000000000** | **0 (invariant)** |
| 15 | $y(r)$ fixed $r$ | $\propto a_0^{-1}$ | $-1$ | 0.8300292579 | −16.9971 |
| 16 | $B(r)$ fixed $r$ | $=GM_b/r^2$ | $0$ | **1.0000000000** | **0 (invariant)** |
| 17 | $g_{\mathrm{deep}}(x r_M)=\sqrt{a_0 B}=a_0/x$ | $\propto a_0$ | $1$ | 1.2047768081 | +20.4777 |
| 18 | $g_{\mathrm{deep}}(r)$ fixed $r$ | $\propto a_0^{1/2}$ | $\tfrac12$ | 1.0976232542 | +9.7623 |
| 19 | $g_Q(x r_M)=a_0\sqrt{x^{-4}+x^{-2}}$ (Q-comparison) | $\propto a_0$ | $1$ | 1.2047768081 | +20.4777 |
| 20 | $\sigma/v_{\mathrm{flat}}$ | $=1/\sqrt2$ | $0$ | **1.0000000000** | **0 (invariant)** |
| 21 | $P(r_M)/\varepsilon_L$ | $=1/(32\pi)$ | $0$ | **1.0000000000** | **0 (invariant)** |
| 22 | $v_{\mathrm{flat}}^4/(GM_b a_0)$ | $=1$ | $0$ | **1.0000000000** | **0 (invariant)** |

Headline numbers of the task statement, verified: $(a_{0,\mathrm{alt}}/a_{0,\mathrm{can}})^2=1.45148716$;
$(a_{0,\mathrm{alt}}/a_{0,\mathrm{can}})^{1/4}=1.0476752$; $(a_{0,\mathrm{alt}}/a_{0,\mathrm{can}})^{-1/2}=0.911059$;
$\kappa_{\mathrm{eff}}=0.60238840$ (all to the quoted digits; exact values in `raw_output.txt`).

### 2.3 The terms that differ between the two comparisons (task step 2, second half)

Comparing the fixed-r columns (8, 10, 12) with the fixed-x columns (9, 11, 13):

1. **The $a_0$ exponent rises by exactly 1** in the fixed-$x$ comparison: $p(\rho):\tfrac12\!\to\!\tfrac32$,
   $p(P):1\!\to\!2$. The extra power is the radius rescaling itself:
   $r=x r_M$ with $r_M\propto a_0^{-1/2}$ contributes $a_0^{+1}$ through $1/r^2\propto a_0$.
2. **The $M_b$ exponent flips sign**: $\rho_{\mathrm{ph}}(r)\propto\sqrt{M_b}$ at fixed $r$ vs
   $\rho_{\mathrm{ph}}(x r_M)\propto 1/\sqrt{M_b}$ at fixed $x$.
3. **The pressure loses its mass dependence entirely** at fixed $x$:
   $P(x r_M)=a_0^2/(8\pi G x^2)$ is $M_b$-independent for every $x$ (the $M_b$ dependence of
   $C^2$ and $r_M^2$ cancel to the last symbol; theorems `as023_P_fixed_x`, `as023_rho_fixed_x_sq`).
4. **Mass accumulates footing-invariantly in $x$**: $M_{\mathrm{ph}}(<x r_M)=xM_b$ with the
   handoff $M_{\mathrm{ph}}(<r_M)=M_b$ at $x=1$ — the enclosed phantom mass is a pure
   dimensionless statement, while $M_{\mathrm{ph}}(<r)\propto a_0^{1/2}\,r$ at fixed $r$ grows
   without bound (the known logarithmic-well/no-outer-cutoff feature of the conditional ansatz).

Everything in §2 is an **exact identity** — for a fixed positive $a_0$ pair there is no
limiting regime and no neglected term; the "$y\in[10^{-2},10^{2}]$ window" of the pressure law
is an exact inverse-square law in disguise (check C5c).

---

## 3. Intermediate algebra, scale factors, signs, units (task step 3)

**(i) $C^2=a_0^2r_M^2$.** $C^2=GM_b a_0=a_0^2(GM_b/a_0)=a_0^2 r_M^2$ (exact; `as023_C_sq_a0rM`).
Units: $[C]=L^2T^{-2}$, $[r_M]=L$, $[a_0^2r_M^2]=L^4T^{-4}=[C^2]$. ✓ All quantities positive;
no sign freedom enters anywhere in the CORE table.

**(ii) Fixed-$x$ density.** With $r=x r_M$,
$$\rho_{\mathrm{ph}}=\frac{C}{4\pi G x^2 r_M^2}=\frac{\sqrt{GM_b a_0}}{4\pi G x^2}\cdot\frac{a_0}{GM_b}
=\frac{a_0^{3/2}}{4\pi G^{3/2}\sqrt{M_b}\,x^2}.$$
Units: $[a_0^{3/2}/G^{3/2}\sqrt{M_b}]=L^{3/2}T^{-3}\cdot L^{-9/2}M^{3/2}T^3\cdot M^{-1/2}
=L^{-3}M=\mathrm{kg\,m^{-3}}$ per $x^{-2}$. ✓

**(iii) Fixed-$x$ pressure.**
$$P(x r_M)=\frac{C}{2}\cdot\frac{C}{4\pi G x^2r_M^2}=\frac{C^2}{8\pi G x^2 r_M^2}
=\frac{a_0^2 r_M^2}{8\pi G x^2 r_M^2}=\frac{a_0^2}{8\pi G\,x^2}.$$
At $x=1$: $P(r_M)=a_0^2/(8\pi G)=5.22495\times10^{-12}\,\mathrm{Pa}$ (canonical) /
$7.58395\times10^{-12}\,\mathrm{Pa}$ (alternative) — AS010's certified identity, recovered as
the $x=1$ row. Units: $[a_0^2/G]=M L^{-1}T^{-2}=\mathrm{Pa}$. ✓ The $M_b$ independence is
exact: $C^2$ and $r_M^2$ each carry one factor of $GM_b$, which cancels.

**(iv) Enclosed mass.** $\int_0^r \rho_{\mathrm{ph}}4\pi s^2 ds=\int_0^r (C/G)\,ds=Cr/G$; at
$r=x r_M$: $C x r_M/G$; since $(C r_M)^2=C^2r_M^2=(GM_b a_0)(GM_b/a_0)=G^2M_b^2$ and all
factors are positive, $C r_M=GM_b$ and $M_{\mathrm{ph}}(<x r_M)=xM_b$ (`as023_Mph_handoff`).
The quadrature itself is check C9 (residual $1.0-1.0$ at $10^{-40}$).

**(v) $y(r_M)=1$.** $B(r_M)=GM_b/(GM_b/a_0)=a_0$ so $y(r_M)\equiv1$ for every $M_b$
(`as023_y_at_rM`); the $x$-profile $y(x)=1/x^2$ is the exact dimensionless statement of the
whole scaling content.

**(vi) Fixed-density cell.** Holding $\rho_\Lambda=\rho_{\Lambda,\mathrm{can}}$ while changing
$a_0$ forces $\kappa$: from $a_0=\kappa c\sqrt{G\rho_\Lambda}$,
$\kappa_{\mathrm{eff}}=a_{0,\mathrm{alt}}/a_{0,\mathrm{can}}\cdot\tfrac12=0.6023884040\ldots$
(verified: $\kappa_{\mathrm{eff}}c\sqrt{G\rho_{\Lambda,\mathrm{can}}}=1.1279\times10^{-10}$
to $10^{-45}$ relative). In that cell $\rho_\Lambda,\varepsilon_L=\rho_\Lambda c^2$ and the
Einstein curvature $\Lambda_{\mathrm{vac}}=8\pi G\rho_\Lambda/c^2$ are invariant by
construction, while the kinetic block ($r_M,v_{\mathrm{flat}},\rho_{\mathrm{ph}},P,\ldots$) shifts
with the same $q^p$ factors — the kinetic block depends on $(a_0,M_b)$ only. Bookkeeping
control: $32\pi a_{0,\mathrm{alt}}^2/c^4$ is *not* the physical vacuum curvature in the
fixed-density cell (it is $q^2$ too large; the $\Lambda=32\pi a_0^2/c^4$ formula presumes
$\kappa=1/2$) — check C4d.

### 3.1 Regime limits (labelled Q-comparison only) with leading neglected terms

On the algebraic Q-line $g^2=B^2+a_0B$ (AS023 uses it strictly as a labelled comparison kernel
in the dimensionless variable; no branch transfer), with $y=1/x^2$:

- **Deep** ($x\to\infty$, $y\to0$): $g/a_0=\sqrt{y^2+y}=\sqrt{y}\,\sqrt{1+y}=\sqrt y+\tfrac12 y^{3/2}-\tfrac18y^{5/2}+\cdots
  =1/x+\tfrac12 x^{-3}+O(x^{-5})$. Leading neglected term after $g=a_0/x=\sqrt{a_0B}$:
  $\tfrac12 a_0 x^{-3}$; relative error $O(x^{-2})$. Domain $x>1$.
- **Newtonian** ($x\to0$, $y\to\infty$): $g/a_0=y\sqrt{1+1/y}=y+\tfrac12-\tfrac18 y^{-1}+\cdots$.
  Leading neglected term after $g=B$: $a_0/2$ (the Q-line's characteristic half); relative
  error $O(y^{-1})$. Domain $x<1$.

Measured (check C5): at $x=10^{-4}$, $g/a_0-y=0.49999999875\to\tfrac12$; at $x=10^4$,
$(g/a_0-x^{-1})/(\tfrac12x^{-3})=0.9999999975\to1$. These are finite consistency witnesses of
the exact series, not exact identities (stated as such).

---

## 4. Fixed-density cell table (task: $\kappa_{\mathrm{eff}}=0.60238840$)

| quantity | fixed-$\kappa$ cell (κ=½) | fixed-density cell (κ_eff=0.60238840) |
|---|---|---|
| $\rho_\Lambda,\varepsilon_L,\Lambda_{\mathrm{vac}}$ | ratio $q^2=1.45148716$ | **ratio 1 (invariant)** |
| $a_0$ | ratio $q=1.20477681$ | ratio $q=1.20477681$ |
| $r_M (\propto a_0^{-1/2})$ | $0.9110594151$ | $0.9110594151$ |
| $v_{\mathrm{flat}},\sigma (\propto a_0^{1/4})$ | $1.0476751663$ | $1.0476751663$ |
| $\rho_{\mathrm{ph}}(r)$ fixed r | $1.0976232542$ | $1.0976232542$ |
| $\rho_{\mathrm{ph}}(x r_M)$ fixed x | $1.3223910407$ | $1.3223910407$ |
| $P(r)$ fixed r | $1.2047768081$ | $1.2047768081$ |
| $P(x r_M)$ incl. $P(r_M)$ | $1.4514871574$ | $1.4514871574$ |
| $\kappa$ | $1/2$ (adopted, invariant) | $0.6023884040$ (changes) |

The two cells differ ONLY in the vacuum bookkeeping rows and in $\kappa$; the kinetic block is
a function of $(a_0,M_b)$ alone and shifts identically. This is the resolution of the
contract's "they cannot share both fixed vacuum density and fixed kappa": each cell fixes one
of the two, and exactly the other one moves.

---

## 5. Independent checks (task step 4) — actual residuals, not Booleans

All tolerances set before evaluation; full raw output in `raw_output.txt` (60-digit mpmath +
sympy + float64; single thread; wall 0.147 s; peak RSS 57.0 MB).

| check | nature | observed | tolerance | pass |
|---|---|---|---|---|
| C0a–C0e | task-stated ratios vs quoted digits ($q^2$, $q^{1/4}$, $q^{-1/2}$, $\kappa_{\mathrm{eff}}$; $\rho_{\Lambda,\mathrm{alt}}/\rho_{\Lambda,\mathrm{can}}=q^2$) | all within quoted precision (e.g. 1.45148715739961 vs 1.45148716) | 1e-6/1e-8 rel | ✓ |
| C1a–C1g | sympy exact identities: fixed-x and fixed-r forms of $\rho_{\mathrm{ph}}$, $P$; $M_{\mathrm{ph}}(<x r_M)=xM_b$; $y(x)=1/x^2$; $C^2=a_0^2r_M^2$ | residual **exactly 0** (7/7) | 0 | ✓ |
| C2 | mpmath-60, 2 footings × 3 masses × 5 x-values × 5 forms (150 evaluations): all five closed forms substituted back | max relative residual **$4.16\times10^{-61}$** | <1e-50 | ✓ |
| C3 | exponent table: all 22 outputs, ratio $O_{\mathrm{alt}}/O_{\mathrm{can}}$ vs $q^p$ | max rel resid **$2.58\times10^{-61}$**, no fails | <1e-45 | ✓ |
| C4a–C4d | fixed-density cell: $a_0$ reproduction via $\kappa_{\mathrm{eff}}$; vacuum invariance; kinetic shifts identical; $\Lambda$-formula separation | residuals ≤1e-45; $\Lambda_{\mathrm{formula}}/\Lambda_{\mathrm{vac}}=q^2$ | 1e-45 | ✓ |
| C5a–C5c | regime limits (Q-comparison): Newtonian $g/a_0-y\to1/2$ at $x=10^{-4}$; deep leading term $\tfrac12x^{-3}$ at $x=10^4$; CORE inverse-square law across $y\in[10^{-2},10^{2}]$ | 0.49999999875; 0.9999999975; ≤1e-50 | 1e-6; 1e-6; 1e-50 | ✓ |
| C6a–C6d | negative control (fixed-r vs fixed-x), §6 | see §6 | | ✓ |
| C7a–C7d | uncertainty classification, §7 | 16/16 resolved at 1σ-scale; 0/16 at 2σ; only p≥3/2 beyond g-scatter | pre-declared rules | ✓ |
| C8a–C8c | boundary behavior: $r_M\propto a_0^{-1/2}$ under $a_0$-rescaling ×10⁺¹²/10⁻¹²; phantom content $\to0$ at $a_0\to0^+$ ($a_0=10^{-40}$: all ratios <1e-4, exact power-law values 3.2e-15/3.2e-8); $r_M\to\infty$ | 8.16e-56; [1.03e-15,1.03e-15,1.07e-30,3.21e-8]; 1.15e+25 m | 1e-40; 1e-4; >1e20 m | ✓ |
| C9 | enclosed phantom mass by quadrature $\int_0^{r_M}\rho_{\mathrm{ph}}4\pi s^2ds=M_b$ | **1.0** (rel dev ≤1e-40) | 1e-40 | ✓ |
| C10 | float64 cross-representation of the four headline ratios | 0.911059415 / 1.047675166 / 1.451487157 / 0.602388404 | 1e-5/1e-6 | ✓ |

The symbolic residuals (C1) are the identities; the mpmath residuals (C2/C3, ~$10^{-61}$) are
finite consistency checks evaluated in a different representation (direct substitution into
the original defining equations) and are reported at their actual magnitude — explicitly not
the same thing as the exact identity. Float64 (C10) is a third representation.

---

## 6. Negative controls (task step 5) — both capable of failing, both executed

**NC1 (task-specified): fixed-r and fixed-x densities treated as the same experiment.**
The phantom density at the canonical MOND radius, re-evaluated on the alternative footing at
the *same physical radius* vs at the *same $x=1$*, gives
$\rho_{\mathrm{alt}}(r_M^{\mathrm{can}})/\rho_{\mathrm{can}}(r_M^{\mathrm{can}})=
q^{1/2}=1.0976232542$ but
$\rho_{\mathrm{alt}}(r_M^{\mathrm{alt}})/\rho_{\mathrm{can}}(r_M^{\mathrm{can}})=
q^{3/2}=1.3223910407$. The two ratios differ by exactly $q=1.2047768081$ — the conflation
"the density shifts by one number" is **rejected** (C6c: ratio-of-ratios $=q\neq1$ to
$10^{-45}$). The control is live: at $q=1$ both ratios coincide exactly (C6d liveness probe).
The fixed-$x$ comparison is the one that respects the physics (dimensionless equivalence), and
it is the one that picks up the extra factor $q$: any per-footing density quote must state
whether it is a fixed-$r$ or fixed-$x$ statement.

**NC2 (regime/boundary/normalization).** The CORE table contains no limiting regime — every
row is an exact power law on $a_0>0$, so there is no neglected term inside the table; the
"deep and Newtonian" content lives (a) in the CORE inverse-square pressure law scanned over
$y\in[10^{-2},10^{2}]$ (exact; C5c), (b) in the Q-comparison series with derived leading
neglected terms and stated domains (C5a/C5b, finite witnesses of the exact series), and (c) in
the boundaries $a_0\to0^+$ (phantom content vanishes to zero with the exact exponents; $r_M$
diverges) and $a_0\to\infty$ ($r_M\to0$). Normalization: the enclosed-mass handoff
$M_{\mathrm{ph}}(<r_M)=M_b$ is exact by quadrature (C9). Exact-vs-numerical distinction is
stated per check.

Neither control damaged the result; the claim survives in the conditional form of §1.2.

---

## 7. Measurement-uncertainty classification (declared, no observational fit)

**Declared yardsticks (comparison values, chosen before evaluation; provenance stated, not a
fit):**
- **Y1 (scale-calibration, 1σ):** $\delta\kappa/\kappa=0.076/0.465=16.34\%$ from the registered
  BTFR measurement $\kappa=0.465\pm0.076$ (STANDING rev. 9 / README; secondary distance-free
  channel $0.551\pm0.043\to7.80\%$). Propagation: an $a_0^p$ output carries fractional
  uncertainty $|p|\cdot Y1$ at 1σ.
- **Y2 (phenomenological scatter):** the framework's registered RAR intrinsic scatter
  $0.1116$ dex in $\log_{10}g$ → $29.30\%$ in $g$, $13.71\%$ in $v$ (half-dex since
  $v\propto g^{1/2}$).

**Classification rule (pre-declared):** footing shift $\Delta_p=q^p-1$ is *resolved* at the 1σ
scale yardstick iff $|\Delta_p|>|p|\cdot Y1$; *resolved* against the scatter yardstick iff
$|\Delta_p|>29.30\%$ ($g$-domain) or $>13.71\%$ ($v$-domain); $p=0$ is *exactly
footing-invariant*.

**Result (C7):**
- **16/16 $a_0$-dependent dimensional outputs exceed the 1σ scale-calibration yardstick** —
  ordered by size: $+45.15\%$ ($p=2$: $\rho_\Lambda,\varepsilon_L,\Lambda$ at fixed κ,
  $P(x r_M)$ incl. $P(r_M)$), $+32.24\%$ ($p=\tfrac32$: $\rho_{\mathrm{ph}}$ fixed $x$),
  $+20.48\%$ ($p=1$: $P$ fixed $r$, $g_{\mathrm{deep}}/g_Q$ fixed $x$), $+9.76\%$
  ($p=\tfrac12$: $\rho_{\mathrm{ph}}$ fixed $r$, $C$, $M_{\mathrm{ph}}$ fixed $r$),
  $-8.89\%$ ($p=-\tfrac12$: $r_M$), $+4.77\%$ ($p=\tfrac14$: $v_{\mathrm{flat}},\sigma$),
  $+17.00\%$ ($p=-1$: $y$ fixed $r$).
- **No output is resolved at 2σ of the scale yardstick** (max ratio
  $|\Delta_p|/(2|p|Y1)=0.6906$ at $p=2$): the footing fork is *consistent* with the declared
  calibration uncertainty at 2σ — the quantitative form of "the framework carries both footings
  always" on an independently declared yardstick.
- **Against the RAR-scatter yardstick**: only the $p\ge\tfrac32$ outputs — fixed-$x$ phantom
  density ($+32.2\%$) and fixed-$x$ pressure incl. $P(r_M)$ ($+45.1\%$) — exceed the $29.3\%$
  $g$-scatter; the fixed-$r$ pressure ($+20.5\%$) sits between the $v$- and $g$-scatter;
  $v_{\mathrm{flat}},\sigma$ ($+4.8\%$) sit *below* the $13.7\%$ $v$-scatter — a v_flat-based
  footing discrimination is scatter-limited at the declared yardsticks.
- **Exactly footing-invariant ($p=0$):** $M_{\mathrm{ph}}(<x r_M)=xM_b$; $y(x)=1/x^2$;
  $B(r)$; $\sigma/v_{\mathrm{flat}}=1/\sqrt2$; $P(r_M)/\varepsilon_L=1/(32\pi)$;
  $v_{\mathrm{flat}}^4/(GM_b a_0)=1$; the dimensionless Q-curve $(g/a_0)^2=x^{-4}+x^{-2}$;
  the exponent structure itself; and the framework's $a_0(z)/a_0(0)=\sqrt{\rho_{\mathrm{DE}}(z)/\rho_{\mathrm{DE}}(0)}$
  evolution form (footing-independent by construction of $\kappa c\sqrt{G\rho}$; cited, not re-derived).

---

## 8. Strongest surviving statement, next implication, transfer conditions

**Strongest surviving statement (conditional theorem).** Under the declared CORE premises —
$r_M=\sqrt{GM_b/a_0}$, $C=\sqrt{GM_b a_0}=v_{\mathrm{flat}}^2$, adopted $\kappa=1/2$ in
$a_0=\kappa c\sqrt{G\rho_\Lambda}$, and the conditional deep-equilibrium inputs
$\sigma^2=C/2$, $\rho_{\mathrm{ph}}=C/(4\pi G r^2)$, $P=\sigma^2\rho_{\mathrm{ph}}$ — the footing
transformation is the exact power map $O\mapsto q^p O$ with the $p$-table of §2.2: at fixed
$x=r/r_M$ the phantom density and pressure scale as $a_0^{3/2}$ and $a_0^2$ (pressure
$M_b$-independent for every $x$), at fixed $r$ as $a_0^{1/2}$ and $a_0$; $r_M\propto a_0^{-1/2}$,
$v_{\mathrm{flat}}\propto a_0^{1/4}$, $P(r_M)=a_0^2/(8\pi G)$; the fixed-density cell fixes
$\kappa_{\mathrm{eff}}=0.60238840$ and leaves the vacuum bookkeeping invariant; the enclosed
phantom mass at fixed $x$ ($=xM_b$), the dimensionless profile $y=1/x^2$, and the six $p=0$
channels are exactly footing-invariant; no $a_0$-dependent dimensional output is resolved at
2σ of the declared $\kappa$-scale yardstick while all are resolved at 1σ; v_flat-level
discrimination is below the declared RAR scatter. Certified in Lean 4 (11 theorems, zero
`sorry`, axioms $\subseteq\{\text{propext},\text{Classical.choice},\text{Quot.sound}\}$) and
by sympy exact residuals 0, mpmath-60 residuals ≤4.2e-61.

**First missing implication (transfer to the full theory).** Same as the CORE gate AS010
named, plus the operative-branch step that this task cannot take with CORE identities alone:
(1) derive from the operative dynamics the conditional equilibrium inputs
($\sigma^2=C/2$, $\rho_{\mathrm{ph}}=C/(4\pi G r^2)$; equilibrium formation, finite boundaries,
source coupling, normalization, possible double counting of the logarithmic well), so the
footing-sensitivity table becomes a prediction rather than a conditional identity; and
(2) carry the same footing-pair through the operative **filtered-MONO weak-field system**
($\nu_{\mathrm{mono}}$ with $y^\star=2.3374$, $\delta=0.05$, heat filter
$S=\exp(\tfrac12\xi^2\Delta)$) to state the branch-level version of "fixed-r vs fixed-x" —
the CORE tables do not fix how $S$ and $\nu_{\mathrm{mono}}$ readings shift between footings at
finite radius. Until then every statement here is a certified *conditional* CORE-scale
identity; numerical agreement is a finite witness of exact algebra, and a completed task is
not closure of gravity.

**Transfer conditions (nothing hidden):** all real-positive domain; $\kappa=1/2$ adopted;
$G$ single Newton coupling ($G_N=G_{\mathrm{bare}}=G_{\mathrm{cosmo}}$ play no role in the
CORE identities and were not asserted equal); conditional equilibrium inputs; Q appears only
as a labelled comparison kernel; no observational fit performed.

---

## 9. Limitations

- Conditional on the task-declared equilibrium inputs; does not solve the time-dependent or
  relativistic equations; equilibrium formation/normalization/which system realizes the
  $r^{-2}$ profile at $r_M$ is open (owned jointly with AS010's open implication).
- $\kappa=1/2$ adopted (fitted, not derived; k01/k03 no-go record untouched; AS010's
  $\eta$-linearity of $\sigma^2=\eta C$ shows the $\tfrac12$ freedom survives inside $P$).
- Uncertainty yardsticks are declared comparison values (BTFR κ, RAR scatter), not fits; their
  systematics are not propagated into an empirical claim; no data were used.
- The $M_{\mathrm{ph}}(<r)\propto r$ growth at fixed $r$ (no outer cutoff of the conditional
  ansatz) is recorded as the known logarithmic-well feature; its resolution is part of the
  equilibrium obligation.
- The operative MONO branch (filter, kernel, criterion B) is untouched; the Q-regime series
  are labelled-comparison statements with stated domains, certified only as finite numerical
  witnesses (their exact series terms are stated analytically in §3.1).
- One self-confirming harness bug was caught by the lane itself (v_flat exponent $1/8$ in
  draft C3 due to $C^{1/4}$ instead of $(GM_ba_0)^{1/4}$) and corrected with the failure
  recorded; the final run is 34/34 PASS.

## 10. Evidence files (this run directory)

- `compute_AS023_footing_sensitivity.py` — bounded prototype (1 thread; SIGALRM 120 s
  hard-enforced; RLIMIT_AS 512 MB attempted and refused by macOS — recorded in result.json
  failed_attempts; measured wall 0.147 s, peak RSS 57.0 MB).
- `raw_output.txt` — full raw output: all values, 34/34 checks PASS, exit 0.
- `AS023_outputs.json` — machine-readable checks/verdicts/table.
- `time_bounds.txt` — `/usr/bin/time -p` output.
- `AS023_footing_sensitivity.lean` — self-contained Lean 4 certificate (11 theorems, no `sorry`).
- `lean_compile.out` — `lake env lean` output (exit 0, zero errors/warnings of substance; 4
  benign linter notes).
- `lean_axioms_out.txt` — unfiltered `#print axioms` of all 11 theorems; each exactly
  `[propext, Classical.choice, Quot.sound]`; `sorryAx` count 0.
- `derivation.md` (this file), `result.json` (structured contract result).
