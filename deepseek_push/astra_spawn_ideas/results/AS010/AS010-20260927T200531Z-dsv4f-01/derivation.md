# AS010 — Pressure normalization at the MOND radius: derivation and checks

**Run:** `AS010-20260927T200531Z-dsv4f-01`
**Worker:** deepseek/deepseek-v4-flash-0731 (provider: openrouter), Hermes subagent `sa-9-19146eff`
**Branch:** CORE scale identities (Group A01); no Q/RAR/MU2/EXP/MONO branch is used or transferred.
**Task source hash:** `38cd8235f4db3bd4c45b4285d7d936ea5b72ff707560bf064b9255d42e0d439e`
**Sources inspected (hashes verified against SOURCE_MANIFEST.json, all match):**
`91a5fac4…` README.md · `98d9149f…` FRIED_CHICKEN_SPEC.md · `8da8176e…` campaign_fresh_gravity_astra/DERIVATIONS.md · `660462eb…` STANDING.md

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

### 1.1 Symbols and units (SI)

| symbol | meaning | units |
|---|---|---|
| $a_0$ | vacuum acceleration scale, two separate footings | $\mathrm{m\,s^{-2}}$ |
| $\kappa$ | one-half normalization of $a_0=\kappa c\sqrt{G\rho_\Lambda}$ | — (adopted input $=1/2$) |
| $G$ | gravitational constant $6.67430\times10^{-11}$ | $\mathrm{m^3\,kg^{-1}\,s^{-2}}$ |
| $c$ | speed of light $299792458$ | $\mathrm{m\,s^{-1}}$ |
| $M_b$ | baryonic mass (test system) | kg |
| $M_\odot$ | $1.98847\times10^{30}$ | kg |
| $\rho_\Lambda$ | vacuum mass density $=4a_0^2/(Gc^2)$ (bookkeeping at given $a_0$, $\kappa=1/2$ fixed) | $\mathrm{kg\,m^{-3}}$ |
| $\varepsilon_L$ | vacuum energy density $=\rho_\Lambda c^2 = 4a_0^2/G$ | $\mathrm{J\,m^{-3}}=\mathrm{kg\,m^{-1}\,s^{-2}}$ |
| $\Lambda$ | same-$G$ vacuum curvature scale $=32\pi a_0^2/c^4$ | $\mathrm{m^{-2}}$ |
| $r_M$ | MOND radius $=\sqrt{GM_b/a_0}$ | m |
| $C$ | deep-law coefficient $=\sqrt{GM_b a_0}=v_{\rm flat}^2$ | $\mathrm{m^2\,s^{-2}}$ |
| $v_{\rm flat}$ | deep flat speed, $v_{\rm flat}^4=GM_b a_0$ | $\mathrm{m\,s^{-1}}$ |
| $\sigma$ | velocity dispersion (deep equilibrium), $\sigma^2=C/2$ | $\mathrm{m\,s^{-1}}$ |
| $\rho_{\rm ph}$ | phantom/equilibrium mass density $=C/(4\pi G r^2)$ (conditional input) | $\mathrm{kg\,m^{-3}}$ |
| $P$ | equilibrium pressure $=\sigma^2\rho_{\rm ph}$ (conditional input) | $\mathrm{Pa}=\mathrm{J\,m^{-3}}$ |
| $y$ | Newtonian argument $B/a_0$ with $B=GM_b/r^2$ | — |

### 1.2 Precise claim

**Claim (conditional identity).** Let $a_0,G,M_b,r$ be positive reals with the units above, and define
$r_M=\sqrt{GM_b/a_0}$, $C=\sqrt{GM_b a_0}$. Subject to the task-declared conditional deep-equilibrium
inputs

$$\rho_{\rm ph}(r)=\frac{C}{4\pi G r^2},\qquad \sigma^2=\frac{C}{2},\qquad P=\sigma^2\rho_{\rm ph},$$

with $a_0=\kappa c\sqrt{G\rho_\Lambda}$, $\kappa=1/2$ **adopted** as input, the pressure at the MOND radius is

$$\boxed{P(r_M)=\frac{a_0^2}{8\pi G}}$$

*exactly — independent of $M_b$ and of $\kappa$* — and, for all $r>0$,

$$P(r)=\frac{a_0^2}{8\pi G}\left(\frac{r_M}{r}\right)^2,\qquad
   \frac{P(r_M)}{\varepsilon_L}=\frac{1}{32\pi},\qquad
   \sigma=\frac{v_{\rm flat}}{\sqrt2}.$$

**Domain.** $r\in(0,\infty)$, $M_b\in(0,\infty)$; the identity is evaluated at the boundary $r=r_M>0$.
No limiting regime or expansion is used: the claim is an exact algebraic identity in real arithmetic
(no neglected term exists). All quantities are real and positive; $r\neq0$, $r_M\neq0$ are required
for the divisions and are satisfied on the stated domain.

**Framework inputs vs. conclusions.** *Inputs (adopted, not derived in this task):* $\kappa=1/2$,
both $a_0$ footings, $G$, $c$, $M_\odot$; the definitions of $r_M$, $C$, $v_{\rm flat}$; and the
conditional deep-equilibrium relations $\sigma^2=C/2$, $\rho_{\rm ph}=C/(4\pi G r^2)$,
$P=\sigma^2\rho_{\rm ph}$ — the framework contract explicitly marks these as conditional
inputs/targets whose derivation from the time-dependent relativistic equations (finite boundaries,
source coupling, normalization, equilibrium formation, possible double counting of the logarithmic
well) is a separate obligation. *Conclusions established here:* the boxed identity and its three
corollaries, exactly.

## 2. Derivation (all scale factors, signs and units)

**(i) Pressure from the conditional inputs.** With $\sigma^2=C/2$ and $\rho_{\rm ph}=C/(4\pi G r^2)$,

$$P(r)=\sigma^2\rho_{\rm ph}(r)=\frac{C}{2}\cdot\frac{C}{4\pi G r^2}
      =\frac{C^2}{8\pi G r^2}.$$

Units: $[C]=L^2T^{-2}$ (since $C=v_{\rm flat}^2$ and $[v_{\rm flat}]=LT^{-1}$; equivalently
$[\sqrt{GM_b a_0}]=\sqrt{L^3M^{-1}T^{-2}\cdot M\cdot LT^{-2}}=\sqrt{L^4T^{-4}}=L^2T^{-2}$),
$[G]=L^3M^{-1}T^{-2}$, so $[C^2/(8\pi G r^2)]=(L^2T^{-2})^2/(L^3M^{-1}T^{-2}\cdot L^2)
=M L^{-1}T^{-2}=\mathrm{Pa}$. ✓

**(ii) Key algebraic fact.** $C^2=GM_b a_0$ and $r_M^2=GM_b/a_0$ give
$C^2=a_0^2\,r_M^2$ exactly:

$$C^2=GM_ba_0=(a_0 r_M^2)a_0=a_0^2 r_M^2.$$

**(iii) Evaluation at $r=r_M$.** Substituting into (i),

$$P(r_M)=\frac{C^2}{8\pi G r_M^2}
      =\frac{a_0^2 r_M^2}{8\pi G r_M^2}
      =\frac{a_0^2}{8\pi G}
      \qquad\text{(exact; }M_b\text{ and }r_M^2\text{ cancel).}$$

Units of the claim: $[a_0^2/G]=(LT^{-2})^2/(L^3M^{-1}T^{-2})=M L^{-1}T^{-2}=\mathrm{Pa}$. ✓
Signs: all quantities positive; the pressure is positive, no sign freedom enters.

**(iv) Scaling law and corollaries.**

$$P(r)=\frac{C^2}{8\pi G r^2}=\frac{a_0^2 r_M^2}{8\pi G r^2}
      =P(r_M)\left(\frac{r_M}{r}\right)^2.$$

With $\varepsilon_L=4a_0^2/G$ (energy density),

$$\frac{P(r_M)}{\varepsilon_L}=\frac{a_0^2/(8\pi G)}{4a_0^2/G}=\frac{1}{32\pi}.$$

With $C=v_{\rm flat}^2$ and $\sigma^2=C/2$: $\sigma=v_{\rm flat}/\sqrt2$.

Note that $y(r_M)\equiv B(r_M)/a_0=GM_b/(GM_b/a_0)/a_0=1$ identically for every $M_b$: the identity
is evaluated at the crossing point of the deep and Newtonian scales, and the $r$-scaling law (iv)
propagates it to all $y=(r_M/r)^2\in(0,\infty)$.

### 2.1 Physical pressure versus mass-equivalent density (task step 2)

$P(r_M)$ and $\varepsilon_L$ share the dimensions of pressure/energy density, $M L^{-1}T^{-2}$
($\mathrm{Pa}=\mathrm{J\,m^{-3}}$). The *mass* density $\rho_\Lambda=M L^{-3}$ differs from the
pressure by exactly $c^2$: $\varepsilon_L=\rho_\Lambda c^2$. Hence

$$P(r_M)=\frac{\varepsilon_L}{32\pi}=\frac{\rho_\Lambda c^2}{32\pi}
      =\frac{1}{32\pi}\cdot4a_0^2/G
      \qquad\text{(dimensionless ratio }1/(32\pi)\approx 9.947\times10^{-3}\text{ against the energy density)}.$$

Dropping $c^2$ in the comparison produces the **dimensionful** ratio

$$\frac{P(r_M)}{\rho_\Lambda}=\frac{c^2}{32\pi}\approx 8.940\times10^{14}\ \mathrm{m^2\,s^{-2}},$$

which is not a number one may compare to unity — this is the task's negative control (NC1) and it
fails exactly as designed (Section 4). The correctly normalized statement is
$P(r_M)=\varepsilon_L/(32\pi)$; the $32\pi$ coefficient is the same one that appears in
$\Lambda=32\pi a_0^2/c^4$ and in requirement 13's $a_0=c^2\sqrt{\Lambda/32\pi}$.

### 2.2 Sensitivity to the adopted normalization (framework contract discipline)

The task's one-half enters through $\sigma^2=\eta C$ with $\eta=1/2$. The general identity is

$$\sigma^2=\eta C\ \Longrightarrow\ P_\eta(r_M)=\eta\,\frac{a_0^2}{4\pi G},$$

i.e. the boundary pressure is **linear** in the adopted normalization $\eta$. The value $1/2$ is an
input of this task (consistent with $\kappa=1/2$), not a derived result; the present identity does not
remove its freedom. (Certified as theorem `as010_eta_generalization`.)

### 2.3 Footing bookkeeping (both footings, never jointly fixed)

Both footings are carried separately; they do not share a fixed $\rho_\Lambda$ *and* a fixed $\kappa$:

| | canonical $a_0=9.3619\times10^{-11}$ | alternative $a_0=1.1279\times10^{-10}$ |
|---|---|---|
| $\rho_\Lambda=4a_0^2/(Gc^2)$ | $5.84441\times10^{-27}\ \mathrm{kg\,m^{-3}}$ | $8.48309\times10^{-27}\ \mathrm{kg\,m^{-3}}$ |
| $\varepsilon_L=4a_0^2/G$ | $5.25270\times10^{-10}\ \mathrm{J\,m^{-3}}$ | $7.62422\times10^{-10}\ \mathrm{J\,m^{-3}}$ |
| $\Lambda=32\pi a_0^2/c^4$ | $1.09080\times10^{-52}\ \mathrm{m^{-2}}$ | $1.58328\times10^{-52}\ \mathrm{m^{-2}}$ |
| $r_M(M_\odot)$ | $1.19064\times10^{15}\ \mathrm{m}=0.038586\ \mathrm{pc}$ | $1.08474\times10^{15}\ \mathrm{m}=0.035154\ \mathrm{pc}$ |
| $v_{\rm flat}(M_\odot)$ | $333.87\ \mathrm{m\,s^{-1}}$ | $349.78\ \mathrm{m\,s^{-1}}$ |
| $\sigma(M_\odot)=v_{\rm flat}/\sqrt2$ | $236.08\ \mathrm{m\,s^{-1}}$ | $247.33\ \mathrm{m\,s^{-1}}$ |
| $\rho_{\rm ph}(r_M,M_\odot)$ | $9.37493\times10^{-17}\ \mathrm{kg\,m^{-3}}$ | $1.23973\times10^{-16}\ \mathrm{kg\,m^{-3}}$ |
| $P(r_M,M_\odot)$ | **$5.22495\times10^{-12}\ \mathrm{Pa}$** | **$7.58395\times10^{-12}\ \mathrm{Pa}$** |
| $P(r_M)/\varepsilon_L$ | $1/(32\pi)=9.94718\times10^{-3}$ (exact) | same (exact) |
| $P(r_M)/\rho_\Lambda$ (c² dropped) | $8.94008\times10^{14}\ \mathrm{m^2s^{-2}}$ (dimensionful) | same (dimensionful) |

If $\rho_\Lambda$ were held fixed at the canonical value, the alternative footing would imply an
effective $\kappa_{\rm alt}=0.60239\neq1/2$; if $\kappa=1/2$ is held fixed, the alternative footing
implies $\rho_\Lambda$ larger by $(a_{0,\rm alt}/a_{0,\rm can})^2=1.45149$. The boxed identity is
footing-invariant in form; only its numerical value changes (with $a_0^2$), as shown.

## 3. Independent checks (task step 4) — actual residuals, not Booleans

All checks with tolerances set before evaluation; full raw output in `raw_output.txt`
(60-digit mpmath + sympy; single thread; observed wall time 0.121 s; peak RSS ≈ 54.6 MB).

| check | nature | observed residual | tolerance | pass |
|---|---|---|---|---|
| CK-SYM exact identity | sympy symbolic simplify of $P(r_M)-a_0^2/(8\pi G)$ with $r_M=\sqrt{GM_b/a_0}$, $C=\sqrt{GM_b a_0}$ | exactly 0 | exactly 0 | ✓ |
| CK-HP canonical/alternative | premise-by-premise evaluation of $(C/2)\cdot C/(4\pi G r_M^2)$ vs $a_0^2/(8\pi G)$, 60 dps | $1.08\times10^{-61}$ / $1.49\times10^{-61}$ | $<10^{-50}$ | ✓ |
| CK-MBSWEEP | $M_b\in[10^{-3},10^6]M_\odot$ (200 log points; $y(r_M)\equiv1$ identically — mass-independence at the crossing) | max rel. dev $3.25\times10^{-61}$ / $2.99\times10^{-61}$ | $<10^{-50}$ | ✓ |
| CK-NORM | boundary $r=r_M$ plus $r/r_M\in\{0.1,0.5,2,10\}$: $P(r)=P(r_M)(r_M/r)^2$; covers $y=(r_M/r)^2\in[0.01,100]$ (deep-to-Newtonian window) | max rel. dev $2.77\times10^{-59}$ / $9.55\times10^{-60}$ | $<10^{-50}$ | ✓ |
| CK-EPS | $P(r_M)/\varepsilon_L=1/(32\pi)$ | rel. dev 0.0 / 0.0 | $<10^{-50}$ | ✓ |
| CK-SIGMA | $\sigma=v_{\rm flat}/\sqrt2$ | rel. dev 0.0 / 0.0 | $<10^{-50}$ | ✓ |
| CK-RHOL | $\rho_\Lambda=\Lambda c^2/(8\pi G)$ (requirement-13 same-$G$ identity) | rel. dev 0.0 / 0.0 | $<10^{-50}$ | ✓ |
| CK-DIM | $[P]=[\varepsilon_L]=[a_0^2/G]=ML^{-1}T^{-2}$; $[P]$ vs $[\rho_\Lambda]$ differ by exactly $c^2$ | hand-table units | equal / mismatch exactly $c^2$ | ✓ |

The symbolic residual (CK-SYM) is the proof; the mpmath residuals are finite consistency checks
evaluated in a *different representation* (direct substitution into the original defining equations),
and are reported at their actual magnitude (all $\le 2.8\times10^{-59}$, consistent with the
60-digit working precision). This is explicitly **not** the same thing as the exact identity.

## 4. Negative controls (task step 5) — both capable of failing, both executed

**NC1 — drop $c^2$ in the pressure/vacuum comparison.** Compare $P(r_M)$ with the mass density
$\rho_\Lambda$ without the $c^2$ conversion. Observed: $P(r_M)/\rho_\Lambda=c^2/(32\pi)=
8.94008\times10^{14}\ \mathrm{m^2\,s^{-2}}$ — a number *with units* (it equals $c^2/(32\pi)$ to
relative deviation $\le 10^{-61}$). The c²-dropped claim "$P(r_M)=\rho_\Lambda/(32\pi)$" is rejected:
pressure and mass density are not commensurable without multiplying by $c^2$ (NC1_verdict FAILs the
invalid claim). The control is thus genuinely capable of failing and it fails as required.

**NC2 — regime/boundary/normalization control.** The claim contains no limiting regime: it is an
exact algebraic identity in $a_0,G,M_b,r$ with no small/large parameter and no expansion, so there is
no neglected leading term to derive; the "deep and Newtonian" window is instead scanned through the
exact scaling law $P(r)=P(r_M)(r_M/r)^2$, i.e. $y\in[0.01,100]$, and the boundary case is
$r=r_M$ itself (both verified above). The exact-vs-numerical distinction is stated explicitly:
CK-SYM (residual exactly 0) is the identity; CK-HP/MBSWEEP/NORM are finite consistency checks.
Also verified: at $r=r_M$ the Newtonian argument is identically $y=1$, so the mass sweep tests
mass-independence at fixed $y$, not a regime scan — the regime content lives in CK-NORM.

Neither negative control damaged the result: the claim survives both, in the conditional form of
Section 1.2.

## 5. Strongest surviving statement and first missing implication

**Strongest surviving statement (conditional theorem).** Under the declared CORE premises —
definitions $r_M=\sqrt{GM_b/a_0}$, $C=\sqrt{GM_b a_0}=v_{\rm flat}^2$, adopted $\kappa=1/2$ in
$a_0=\kappa c\sqrt{G\rho_\Lambda}$, and the task-declared conditional deep-equilibrium inputs
$\sigma^2=C/2$, $\rho_{\rm ph}=C/(4\pi G r^2)$, $P=\sigma^2\rho_{\rm ph}$ — the boundary pressure at
the MOND radius is exactly the $M_b$-independent universal constant $a_0^2/(8\pi G)$
($5.22495\times10^{-12}$ Pa canonical / $7.58395\times10^{-12}$ Pa alternative), equal to
$\varepsilon_L/(32\pi)$ with $\varepsilon_L=4a_0^2/G=\rho_\Lambda c^2$; equivalently
$\sigma(r_M)=v_{\rm flat}/\sqrt2$ and $P(r)=P(r_M)(r_M/r)^2$ for all $r>0$. Certified in Lean 4
(six theorems, zero `sorry`, axioms $\subseteq\{\text{propext},\text{Classical.choice},\text{Quot.sound}\}$).

**Why it is not a full-theory prediction.** The framework contract marks $\sigma^2=C/2$,
$\rho_{\rm ph}=C/(4\pi G r^2)$ and $P=\sigma^2\rho_{\rm ph}$ as *conditional* deep-equilibrium
inputs/targets: equilibrium formation, finite boundaries, source coupling, normalization and the
possible double counting of the logarithmic well each need their own derivation from the time-
dependent operative dynamics. Similarly $\kappa=1/2$ (and hence the $\eta=1$ coefficient within
$P_\eta$) remains an adopted input. No branch (Q, RAR, MU2, EXP-AQUAL, MONO) was used or invoked,
so no branch translation is needed and none is claimed; the result lives entirely in the CORE scale
identities of group A01.

**First missing implication (transfer to full theory).** Derive, from the operative dynamics, the
deep-equilibrium normalization $\sigma^2=C/2$ (and the profile $\rho_{\rm ph}=C/(4\pi G r^2)$) that
the identity takes as input — including the formation/attainment question — and then establish the
bridge from the deep-equilibrium boundary pressure to the static global solution at the MOND radius.
Until that derivation exists, $P(r_M)=a_0^2/(8\pi G)$ is a certified *conditional* identity, not an
independent prediction.

## 6. Limitations

- Conditional on the task-declared equilibrium inputs; does not solve the time-dependent or
  relativistic equations; nothing here establishes equilibrium formation, normalization, or which
  physical system (if any) realizes $\rho_{\rm ph}=C/(4\pi G r^2)$ at $r_M$.
- $\kappa=1/2$ (and the $\sigma^2=C/2$ half) are adopted inputs; the identity is exactly linear in
  the normalization $\eta$ (theorem `as010_eta_generalization`), so the $1/2$ freedom survives.
- No observational data used or claimed; numerical agreement is a consistency check of an exact
  identity, and the finite np-residuals are reported as such.
- The $r\to0$ singular behavior of the equilibrium ansatz (divergence of $\rho_{\rm ph}$) is
  outside the claim's domain $r>0$; the boundary/formation content is open.
- $G$ enters as the single Newton coupling; ratio effects of $G_N$ vs $G_{\rm bare}$ vs $G_{\rm cosmo}$
  do not arise in this identity and were not asserted.
- A completed task is not closure of gravity; this is one conditional CORE-scale identity of the
  A01 group.

## 7. Evidence files (this run directory)

- `compute_as010.py` — runnable bounded prototype (1 thread, 120 s wall cap, 512 MB cap attempted;
  RSS measured ≈54.6 MB; elapsed 0.121 s). Memory cap note: `RLIMIT_AS` could not be raised on this
  macOS host ("current limit exceeds maximum limit"); the observed RSS is reported instead.
- `raw_output.txt` — full raw output: all values, 21/21 checks PASS, exit 0.
- `AS010_pressure_normalization.lean` — self-contained Lean 4 certificate (6 theorems, no `sorry`).
- `lean_axioms_out.txt` — `lake env lean` output; axiom list per theorem.
- `derivation.md` (this file), `result.json` (structured contract result).