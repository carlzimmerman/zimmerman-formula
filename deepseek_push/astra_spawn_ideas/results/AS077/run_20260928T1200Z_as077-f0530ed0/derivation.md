# AS077 — Finite-shell normalization of the isothermal profile: derivation

**Run:** `run_20260928T1200Z_as077-f0530ed0` · **Worker:** Hermes subagent seed
(deepseek/deepseek-v4-flash-0731 via openrouter) · **Task hash:**
`fa263a939f2e45507a206b5588dc9e983b21128486e4e9bb7e8db910845a463d` (verified at start, matches)
· **Group A04, branch:** conditional deep-equilibrium sector; no automatic particle ontology.

---

## 0. Step 1 of the seed — precise claim, symbols, boundary conditions, assumptions

**Claim under test (named result "Finite-shell normalization of the isothermal profile"):**
for the profile

$$\rho(r) = \frac{A}{r^{2}},\qquad r_{\rm in}\le r\le R,\qquad r_{\rm in}>0,\qquad R\le r_M\ \text{(default domain)}$$

with total shell mass $M$, the amplitude $A$ derived from the fixed mass must be compared with the
framework equipartition amplitude $A_* = C/(4\pi G)$; the task is to state **exactly which
$(M,R,r_{\rm in})$ make the two normalizations coincide**, and to quantify the failure modes
(naive $1/R$ normalization, imposed-log-well ansatz, deep-exterior transfer).

### Symbol dictionary

| symbol | meaning | units (SI) |
|---|---|---|
| $\rho$ | phantom mass density | kg m⁻³ |
| $A$ | profile amplitude ($\rho r^2$) | kg m⁻¹ |
| $r_{\rm in}, R$ | shell inner edge, outer edge, $r_{\rm in}>0$ | m |
| $M$ | total phantom (shell) mass, $M=4\pi A(R-r_{\rm in})$ | kg |
| $M_b$ | baryon source mass | kg |
| $G$ | Newton coupling $G_N=6.67430\times10^{-11}$ (separate from $G_{\rm bare}, G_{\rm cosmo}$; unused here) | m³ kg⁻¹ s⁻² |
| $a_0$ | framework scale, $a_0=\kappa c\sqrt{G\rho_\Lambda}$, $\kappa=1/2$ **adopted** | m s⁻² |
| $C$ | $=(GM_b a_0)^{1/2}=v_{\rm flat}^2$ | m² s⁻² |
| $r_M$ | $=(GM_b/a_0)^{1/2}$ (equipartition radius) | m |
| $A_*$ | $=C/(4\pi G)$ — the G084/G03E equipartition amplitude | kg m⁻¹ |

### Framework inputs (declared, not derived in this run)
$a_0=\kappa c\sqrt{G\rho_\Lambda}$ with $\kappa=1/2$ adopted; $\rho_\Lambda=4a_0^2/(Gc^2)$;
$\Lambda=32\pi a_0^2/c^4$ (when Einstein and scale $G$ coincide — not used here);
$r_M=(GM_b/a_0)^{1/2}$; $C=(GM_b a_0)^{1/2}$; $v_{\rm flat}^4=GM_b a_0$;
$\sigma^2=C/2$, $\rho=A/r^2$, $P=\sigma^2\rho$ are **conditional deep-equilibrium targets** of the
framework (FRAMEWORK_CONTRACT), i.e. we take the isothermal profile as the equilibrium's
declared outcome (G084/G091) and derive only its *finite-shell normalization consequences*.

### Branch discipline
Q, RAR, MU2, EXP-AQUAL and filtered MONO (criterion B) are declared distinct kernels. This run
uses **no kernel**; it lives in the conditional deep-equilibrium sector (the log well
$\Phi=C\ln r$ and its finite-shell version). **No branch transfer is claimed** — in particular the
interior normalization is not transferred to the operative MONO field equation (seed's explicit
warning; the deep-exterior check below is the required separate-shell fixture).

### Assumptions (explicit)
1. $\rho=A r^{-2}$ on $[r_{\rm in},R]$ (equilibrium profile, G084 result — taken as input here).
2. $r_{\rm in}>0$; default $R\le r_M$; diagnostics at $r_{\rm in}/R\in\{0.01,0.1,0.5\}$,
   $R/r_M\in\{0.62,1\}$ are **controls, not a fit**.
3. $\kappa=1/2$ adopted (not derived; its freedom is an explicit open input).
4. Static, non-relativistic, spherical; no particle ontology.
5. Constants: $G=6.67430\times10^{-11}$, $c=299792458$, $M_\odot=1.98847\times10^{30}$,
   $\mathrm{pc}=3.085677581491367\times10^{16}$ (campaign defaults; historical sources used
   $G=6.674e{-}11$, $M_\odot=1.98892e30$ — the <0.05% differences are noted in limitations).

---

## 1. Step 2 — derivation of $A$ from fixed $M$; comparison with $C/(4\pi G)$

**Mass integral (exact, closed form):**

$$M=\int_{r_{\rm in}}^{R}\frac{A}{r^{2}}\,4\pi r^{2}\,dr
 =4\pi A\int_{r_{\rm in}}^{R}dr = 4\pi A\,(R-r_{\rm in}).$$

Units: $[A]=\mathrm{kg\,m^{-1}}$, $[4\pi A(R-r_{\rm in})]=\mathrm{m^{-1}\cdot kg\,m^{-1}\cdot m}=\mathrm{kg}$ ✓.
The integrand $\rho\cdot4\pi r^2=4\pi A$ is constant, so the quadrature is exact to machine
precision (measured rel. residual $3.58\times10^{-16}$; direct differentiation check
$dM/dR=4\pi R^2\rho(R)=4\pi A$: exact, rel. residual $0$). The antiderivative identity
$\int_{r_{\rm in}}^R(1/r-r_{\rm in}/r^2)dr=\ln(R/r_{\rm in})-1+r_{\rm in}/R$ is verified at 50
digits (residual $0$).

**Fixed-mass normalization:**

$$A_M=\frac{M}{4\pi(R-r_{\rm in})}.$$

**Framework amplitude:**

$$A_*=\frac{C}{4\pi G}=\frac{\sqrt{GM_b a_0}}{4\pi G},\qquad
\frac{C}{G}=\sqrt{\frac{M_b a_0}{G}}=\frac{M_b}{r_M}\quad
\left(\text{since } \frac{M_b}{r_M}=M_b\sqrt{\frac{a_0}{GM_b}}=\sqrt{\frac{M_b a_0}{G}}\right).$$

**Equality condition:**

$$A_M=A_*\iff \frac{M}{R-r_{\rm in}}=\frac{C}{G}\iff
\boxed{\left(\frac{M}{M_b}\right)\left(\frac{r_M}{R-r_{\rm in}}\right)=1}.$$

**Which $(M,R,r_{\rm in})$ allow both normalizations simultaneously** (all algebra Lean-certified,
theorems T0–T3, T8):

1. **$M=M_b$, shifted family (outside the default bound):** $R-r_{\rm in}=r_M$, i.e.
   $R=r_M+r_{\rm in}$ for *any* $r_{\rm in}>0$. This family satisfies the equality for all finite
   $r_{\rm in}$ but violates the default $R\le r_M$ constraint ("unless specified" — we record it).
2. **$M=M_b$, classical G084/G03E reading (boundary limit of the default domain):**
   $R=r_M$ and $r_{\rm in}\to 0^{+}$. This is the only equality point inside/on the default
   domain, and it is a **limit, not an interior point**: every admissible fixture with $r_{\rm in}>0$
   and $R\le r_M$ has
   $$A_M/A_*=(R-r_{\rm in})/r_M<1.$$
3. **Interior-domain equivalent:** for fixed $(r_{\rm in},R)$ with $R\le r_M$, equality requires a
   *reduced* source mass $M^*=M_b\,(R-r_{\rm in})/r_M<M_b$. The shell holding $M^*<M_b$ is the only
   interior configuration whose amplitude equals the equipartition value.

**Measured ratios on the six diagnostic fixtures** ($A_M/A_*=(R-r_{\rm in})/r_M$):

| $r_{\rm in}/R$ | $R/r_M=0.62$ | $R/r_M=1.0$ |
|---|---|---|
| 0.01 | 0.6138 | 0.9900 |
| 0.1  | 0.5580 | 0.9000 |
| 0.5  | 0.3100 | 0.5000 |

(identical on both footings — dimensionless; checked to $1.11\times10^{-16}$). Mass deficit vs
$M_b$: $(r_M-R+r_{\rm in})/r_M = 1-(R-r_{\rm in})/r_M$ ∈ {0.386, 0.442, 0.69, 0.010, 0.10, 0.50}.
The limit reading: $r_{\rm in}/R=10^{-9}$ at $R=r_M$ gives $A_M/A_*=0.999999999000$ (C3).

**Mass normalization residual (independent check of the closed form):**
$|4\pi A_M(R-r_{\rm in})-M|/M\le 1.39\times10^{-16}$ on all six fixtures, both footings (C2).

**G084/G091 connection:** the sources' amplitude $A\to C/(4\pi G)$ is the *point-inner-edge
equipartition limit* $r_{\rm in}\to0^+$, $R\to r_M$; the sources' own formula
$A=M_b/(4\pi(r_M-r_{\rm in}))$ is exactly the fixed-mass form $A_M$ and equals
$A_*$ only along $R-r_{\rm in}=r_M$ (T3). At $A=A_*$ the phantom mass inside $r_M$ is exactly
$M_b$ (T8: $4\pi A_* r_M=M_b$; certified using $C/G=M_b/r_M$).

---

## 2. Step 3 — intermediate algebra, signs, units, limiting regime and leading neglected term

### Self-potential of the finite shell (signs and boundary conditions explicit)
Poisson: $\nabla^2\Phi=4\pi G\rho$ with the shell's own source. Enclosed mass
$M({<}r)=4\pi A(r-r_{\rm in})$; the inward field magnitude is

$$g(r)=-\Phi'(r)=\frac{G M({<}r)}{r^2}=4\pi G A\,\frac{r-r_{\rm in}}{r^2}
=C_{\rm eff}\left(\frac{1}{r}-\frac{r_{\rm in}}{r^2}\right),\qquad
\Phi(r)=C_{\rm eff}\left(\ln r+\frac{r_{\rm in}}{r}\right)+\Phi_0,\qquad C_{\rm eff}\equiv 4\pi G A.$$

Boundary consistency: $g(r_{\rm in})=0$ (field vanishes at the inner edge — the interior
$r<r_{\rm in}$ is empty); $g\to C_{\rm eff}/r$ for $r\gg r_{\rm in}$ (log-well asymptote).
Independent-representation checks (C5): Poisson residual in the shell
$(1/r^2)(r^2\Phi')'-4\pi G\rho$ relative $\le 4.4\times10^{-12}$ (all three diagnostic $r_{\rm in}/R$
at $R=r_M$, $N=40001$ grid); finite-difference $\Phi'$ vs closed form: interior stencils
$\le 2.0\times10^{-6}$ (edge stencil $5.75\times10^{-2}$ reported separately — the known
one-sided-stencil artifact), 50-digit antiderivative identity residual $0$ (C1b).

### Limiting regime and leading neglected term
The **imposed-log-well ansatz** $\Phi_{\log}=C\ln r+\text{const}$ is the $r_{\rm in}\to0$ limit of
the exact shell potential. At finite $r_{\rm in}$ with $C_{\rm eff}=C$, the **leading neglected
term** (dominant $r$-dependent correction) is

$$\Delta\Phi_{\rm leading}(r)=C\,\frac{r_{\rm in}}{r}\qquad(r\gg r_{\rm in}),$$

with domain of validity $r_{\rm in}/R\ll 1$: relative to the log variation over the shell,
$\Delta\Phi/\left[C\ln(R/r_{\rm in})\right]$ at the outer edge is
$(r_{\rm in}/R)/\ln(R/r_{\rm in})=\{0.00217,\ 0.0434,\ 0.721\}$ for
$r_{\rm in}/R=\{0.01,0.1,0.5\}$ (0.22 %, 4.3 %, 72 %). At $r_{\rm in}/R=0.5$ the correction
*dominates* the log span: the historical imposed-log-well ansatz is a poor representation of a
half-shell. The field correction is a pure factor: $g(R)=C_{\rm eff}(1-r_{\rm in}/R)/R$; the
log-well boundary identity $g(r_M)=a_0$ (T6, certified) becomes, at finite $r_{\rm in}$ with
$R=r_M$: $g(r_M)=a_0(1-r_{\rm in}/r_M)<a_0$ — correction factors $\{0.99,0.90,0.50\}$ (C6; T7
certifies the strict inequality $C(1-r_{\rm in}/R)/R<C/R$).

---

## 3. Step 4 — negative control (capable of failing) and deep-exterior fixture

### Control N1 — the naive $1/R$ normalization (fails by design on every admissible shell)
Use $A=M/(4\pi R)$ at finite $r_{\rm in}$ (i.e. assume the mass fills $[0,R]$ as if
$r_{\rm in}=0)$:

$$M_{\rm enc}=4\pi\,\frac{M}{4\pi R}\,(R-r_{\rm in})=M\left(1-\frac{r_{\rm in}}{R}\right)
\;\Rightarrow\; \boxed{\text{mass deficit}=M\,r_{\rm in}/R}.$$

Measured (C4): deficits $= r_{\rm in}/R$ exactly — $\{1\,\%,10\,\%,50\,\%\}$ at
$r_{\rm in}/R=\{0.01,0.1,0.5\}$, i.e. $\{0.01,0.10,0.50\}$ on all fixtures, both footings.
The control **is** capable of failing (deficit would be $0$ at $r_{\rm in}=0$, a point outside
the admitted domain $r_{\rm in}>0$) and **does fail** at every admissible fixture: the naive
$1/R$ normalization never reproduces the shell mass; the exact normalization is $1/(R-r_{\rm in})$
(T4, T5 — deficit positivity certified in Lean).

### Control N2 — default-domain equality (fails on every fixture, as it must)
The claim "the finite-shell normalization equals $C/(4\pi G)$ on the default domain" is FALSE:
$A_M/A_*<1$ strictly on all six fixtures (C2); equality holds only on the boundary limit
$r_{\rm in}\to0^+$, $R=r_M$, or on the shifted family $R=r_M+r_{\rm in}$ outside the default
bound (T3). The negative control therefore converts the G084 reading into its exact
domain-of-validity statement.

### Deep exterior (the seed's required separate-shell fixture, no interior transfer)
At the interior-equipartition amplitude $A_*$, a deep shell $[q\,r_M,\ s\,q\,r_M]$ carries

$$M_{\rm shell}=4\pi A_*(s-1)\,q\,r_M = M_b\,q\,(s-1)$$

phantom mass (C7): $\{10,90,100,900\}\,M_b$ for $(q,s)=\{(10,2),(10,10),(100,2),(100,10)\}$.
Consequences:
- The phantom mass in a deep shell **exceeds the galaxy's baryon mass** by 1–3 orders of
  magnitude; normalizing the deep shell to $M_b$ would set $A$ low by the same factors
  ($A_{\rm loc}/A_*=1/[q(s-1)]\in\{0.1,\ 0.0111,\ 0.01,\ 0.00111\}$).
- $A$ is fixed by **interior equipartition** $M_{\rm ph}({<}r_M)=M_b$ (T8), not by any deep local
  shell; the interior normalization ansatz does **not** transfer to the deep exterior. Any
  transfer of an interior/log-well ansatz to the operative filtered-MONO kernel remains
  unperformed and is an explicit open dependency (the seed demands that check; it is outside
  this equilibrium-sector run).

---

## 4. Step 5 — strongest surviving statement

**Theorem (finite-shell normalization of the isothermal profile).** Let
$\rho=A r^{-2}$ on $[r_{\rm in},R]$, $r_{\rm in}>0$, $R\le r_M$ (default domain), and let
$C=(GM_b a_0)^{1/2}$, $r_M=(GM_b/a_0)^{1/2}$, $A_*=C/(4\pi G)$.

1. $M=4\pi A(R-r_{\rm in})$ exactly; the unique mass-normalized amplitude is
   $A_M=M/(4\pi(R-r_{\rm in}))$.
2. $A_M=A_*$ **iff** $(M/M_b)(r_M/(R-r_{\rm in}))=1$; with $M=M_b$ this is
   $R-r_{\rm in}=r_M$: the shifted family $R=r_M+r_{\rm in}$ (outside the default bound) and the
   boundary limit $r_{\rm in}\to0^+$, $R=r_M$ (the historical G084/G03E reading). On the entire
   open default domain, $A_M<A_*$ strictly with ratio $(R-r_{\rm in})/r_M$ (0.31–0.99 over the
   control grid).
3. The naive amplitude $A=M/(4\pi R)$ under-counts the shell mass by exactly $M r_{\rm in}/R>0$
   at every admissible fixture (1 %, 10 %, 50 % on the control grid): the $1/R$ normalization is
   invalid on every finite shell.
4. The exact finite-shell potential is $\Phi=C_{\rm eff}(\ln r+r_{\rm in}/r)+\Phi_0$
   ($C_{\rm eff}=4\pi GA$); the imposed-log-well ansatz neglects the leading term
   $C_{\rm eff}r_{\rm in}/r$, of relative size $(r_{\rm in}/R)/\ln(R/r_{\rm in})\in
   \{0.22\,\%,4.3\,\%,72\,\%\}$ at the cap, and the cap field is suppressed by
   $1-r_{\rm in}/R$ (so $g(r_M)=a_0(1-r_{\rm in}/r_M)<a_0$).
5. In the deep exterior the amplitude is fixed by interior equipartition; a shell
   $[q r_M, sq r_M]$ carries $q(s-1)M_b$ (10–900 $M_b$ on the control grid) and is not
   re-normalizable to the baryon mass.

**Footnote applicability (both footings):** the whole theorem is dimensionless
(condition (2) and all ratios) and identical for $a_0=9.3619\times10^{-11}$ and
$a_0=1.1279\times10^{-10}\ \mathrm{m\,s^{-2}}$ (C8: cross-footing ratio difference
$\le1.11\times10^{-16}$). The physical radii/amplitudes differ per footing: with
$M_b=7\times10^{10}M_\odot$, canonical gives $r_M=10.209\ \mathrm{kpc}$, $C=2.94913\times10^{10}$
m² s⁻², $A_*=3.51623\times10^{19}$ kg m⁻¹, $v_{\rm flat}=171.7$ km s⁻¹; alternative gives
$r_M=9.301\ \mathrm{kpc}$ (ratio $0.91106=\sqrt{a_{0,\rm can}/a_{0,\rm alt}}$),
$C=3.23703\times10^{10}$ m² s⁻², $A_*=3.85950\times10^{19}$ kg m⁻¹, $v_{\rm flat}=179.9$ km s⁻¹.
$\rho_\Lambda=4a_0^2/(Gc^2)$ = $5.844412\times10^{-27}$ kg m⁻³ (canonical) and
$8.483090\times10^{-27}$ kg m⁻³ (alternative) — the two footings cannot share both fixed
$\rho_\Lambda$ and fixed $\kappa=1/2$: at fixed $\rho_\Lambda$(canonical), the alternative
footing has effective $\kappa=0.6024$ (= $a_{0,\rm alt}/(2a_{0,\rm can})$); at fixed
$\kappa=1/2$ the density ratio is $1.4515$.

**Outcome:** *supports_scoped_claim* — a self-contained conditional lemma with exact
equality/deficit statements, certified algebra (Lean, 9 theorems, zero sorry, axioms ⊆
{propext, Classical.choice, Quot.sound}), reproducible residuals, and an explicit
non-transfer statement to the deep exterior and to filtered MONO.

---

## 5. Open dependencies and next implication

- **D1 (immediate, same group):** the virial closed forms of G091 (W_self from 0, W_bar from
  $r_b$) must be re-derived with the finite inner edge $r_{\rm in}>0$: the self-energy sliver
  $16\pi^2GA^2r_{\rm in}$ and the shifted baryon-coupling log. This determines whether
  $\sigma^2=C/2$ survives at finite $r_{\rm in}$ with the well-consistent boundary, and supplies
  the exact finite-shell energy budget for closure gate A04.
- **D2 (kernel gate):** the operative filtered-MONO field equation
  $\Delta u=4\pi G\rho_b$, $\Delta\Phi=4\pi G\rho_b+S^*\mathrm{div}[(\nu_{\rm MONO}-1)\nabla Su]$
  has not been checked against the finite-shell equilibrium; the interior log-well ansatz must
  not be transferred there without that check (seed's explicit warning).
- **D3 (attainment):** dynamical attainment of the profile (G035's kill) is untouched by this
  normalization result.
- **D4 (footing):** $\kappa=1/2$ remains an adopted input; the two footings are separate scales
  (they cannot share both fixed $\rho_\Lambda$ and fixed $\kappa$).

**Next unresolved implication (strongest single statement):** *the exact finite-shell virial
budget at $r_{\rm in}>0$* — with $W_{\rm self}=-16\pi^2GA^2(R-r_{\rm in})$ replaced by the
full-shell form including the sliver, and the matching condition
$(M/M_b)(r_M/(R-r_{\rm in}))=1$ as input, determine the finite-shell
$\sigma^2(r_{\rm in},R)$ and whether the triad value $C/2$ is recovered in the
$r_{\rm in}\to0$, $R=r_M$ limit only.

**Suggested follow-up (child AS077.C01, ready spec):** *finite-shell virial closure with the
inner edge* — target: closed form of T, W_self, W_bar, boundary term at $r_{\rm in}>0$ and the
resulting $\sigma^2$; controls: (i) recover G091's closed forms at $r_{\rm in}\to0$,
(ii) negative control: $W_{\rm self}^{\rm shell}$ sliver term must change the reading by
exactly $16\pi^2GA^2r_{\rm in}$ vs G091's $R$-integral, (iii) both footings; dependencies: this
run's matching condition; dispatch state: **proposed, not dispatched** (no claims file created).
Duplicate check: G091 integrates W_self from 0 and W_bar from $r_b$; no existing AS/MY seed or
result derives the finite-$r_{\rm in}$ shell virial (verified against
`deepseek_push/astra_spawn_ideas/manifest.json` titles AS001–AS2000 — G091's finite-boundary
bookkeeping is the closest, and it does not carry $r_{\rm in}>0$ in W_self).

---

## 6. Bounds, commands, artifacts

- **Bounds (declared and enforced):** wall $\le120$ s (actual $0.054$ s), RSS $\le512$ MB
  (actual $49.5$ MB peak, macOS ru_maxrss bytes), 1 thread (OMP_NUM_THREADS=1, single process,
  no threading/parallel libs; enforced by design and recorded by the script).
- **Commands:**
  - `python3 as077_derive.py > out/stdout_capture.log` (cwd = run dir) → exit 0; writes
    `out/residuals.json`, `out/run.log`.
  - `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS077_cert.lean` → exit 0
    (9 theorems).
  - `LEAN_PATH=<run_dir>:<lake env LEAN_PATH> lean --root=<run_dir> -o AS077_cert.olean AS077_cert.lean` → 0;
    `lean --root=<run_dir> AS077_axioms.lean > axioms_check.out` → 0 (axioms transcript: all 9
    theorems ⊆ {propext, Classical.choice, Quot.sound); zero sorry.
  - `sha256sum` on task, sources, and all artifacts.
- **Sources inspected (hashes pinned in SOURCE_MANIFEST.json, all match):** G084
  `752999fd…`, G091 `8164360f…`, G233 `ad89298d…`; STANDING.md `660462eb…`; the September 26
  amendment block in FRIED_CHICKEN_SPEC.md `98d9149f…`; FRAMEWORK_CONTRACT.md, RESULT_CONTRACT.json,
  SOURCE_MANIFEST.json, FIRST_PRINCIPLES_AND_BRANCHING.md.
