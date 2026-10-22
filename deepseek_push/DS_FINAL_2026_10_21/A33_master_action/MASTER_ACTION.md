# A33 — THE MASTER ACTION

**Lane:** A33_master_action · **Date:** 2026-10-21 · **Base:** `DS_FINAL_2026_10_21/BRIEF.md`,
`FINAL_THEORY.md`, `core_open_problems_round2_2026_10_20/03_relativity/report.md` (§2 action), A3, A12, A16, A20, A22.
**Script:** `a33_checks.py` (28/28 PASS, exit 0, 1.2 s) · **Output:** `a33.out` · **Data:** `a33_results.json`
(includes the coefficient table as `coefficient_table` and the free-parameter ledger as `free_parameters`).

**Claim.** The theory has one action. Every equation the DSF-21 push derived is a variation, a limit, or an
algebraic consequence of the single Lagrangian density of §1, with the coefficients of §2. The action has
**four free numbers** (`κ`, `β`, `η`, `γ`), of which `κ` and `γ` are measured and `β`, `η` are only bounded;
**three free functionals** (`R = 4`'s principle, `ς(r)`, the turn-off form) which the action does not fix;
and `y_t` is **not** free — it is derived (66.2999) from the closure once the turn-off form is posited.
Two derivations in the record are corrected (§7): the `r_switch` arithmetic is now attributed to the
P-sector's own gradient force, and A3's reduced P equation is missing its `γP″` term.

---

## 1. The action

Units `c = 1` unless stated; signature `(−+++)`; `K = 4πG` (the action's own normalisation — see §1.1).
`h_ij` is the spatial metric, `N` the lapse, `N^i` the shift, `√h = √det h`, `D_i` the covariant derivative
of `h_ij`, `θ ≡ K^i_i`, `K_ij = (1/2N)(ḣ_ij − D_iN_j − D_jN_i)`, `R3` the 3-Ricci scalar of `h_ij`.

$$
\boxed{
\begin{aligned}
\frac{L}{N\sqrt h}=\;&\frac{{}^{(3)}R+K_{ij}K^{ij}-(1+\beta)\theta^{2}-2\Lambda}{4K}
&&\text{[Einstein–Hilbert}+\Lambda+\text{ADM deformation]}\\[2pt]
&+P^{i}D_i\ln N &&\text{[clock]}\\
&-\;W(u),\qquad u\equiv K|P|\equiv K\sqrt{h^{ij}P_iP_j},\qquad
W(u)=\frac{a_0^{2}}{K}\Big[-\frac{u}{a_0}-\ln\!\Big(1-\frac{u}{a_0}\Big)\Big]
&&\text{[saturating log]}\\[2pt]
&+\frac{\eta}{2}E_iE^{i},\qquad E_i\equiv\frac{\dot P_i-\mathcal L_NP_i}{N} &&\text{[P kinetic]}\\
&-\frac{\gamma}{2}\big(D_iP^{i}\big)^{2}-\frac{\gamma}{4}F_{ij}F^{ij},\qquad F_{ij}\equiv D_iP_j-D_jP_i
&&\text{[P gradient]}\\[2pt]
&+\;\frac{L_{\rm cold}}{N\sqrt h}+\frac{L_m}{N\sqrt h} &&\text{[cold sector, ordinary matter]}
\end{aligned}}
$$

with `P_0 = N^iP_i` (so `P_μ` is a spatial covector, `n^μP_μ = 0`), `u < a₀` (the cap is a hard boundary of the
configuration space), and the two matter sectors defined as follows.

**Cold sector.** A collisionless medium, not a fluid with an equation of state:

$$
T^{c}_{\mu\nu}=\int\frac{d^{3}p}{E}\,p_\mu p_\nu f_c(x,p),\qquad
p^{\mu}\nabla_\mu f_c=0\ (\text{Vlasov}),\qquad
\nabla_\mu T_c^{\mu\nu}=0 .
$$

Its fluid reduction (second moment) is `T^c_{μν} = ρ_c u_μu_ν + p_c h_{μν}` with

$$
p_c=\rho_c\sigma_c^{2},\qquad \sigma_c=\sqrt{a_0L_*}\quad(\text{the surviving map, A20}),
$$

`σ_c` a **fixed dispersion**, not a thermodynamic pressure: only `ρ_c` is varied. This matters — it is why the
`Γ = 2` "polytrope" of A16 is a *closure of the P sector's gradient energy* (§7.1), not an equation of state of
the medium. The two are different objects by 8.4 orders of magnitude: `p_kin/p_el = 2σ_c²/(γρ_c) = 2.7e8` at the
cosmic mean, and the medium's Jeans length is `σ_c/\sqrt{4πGρ_c} = 198 kpc`, so at the 24 pc scale of the core it
neither supports nor collapses. Only the elastic term enters the field equation.

**Sourcing split.** The total cold density splits as `ρ_c = ςρ_c + (1−ς)ρ_c`: the first part is what the P
sector's charge reproduces, the second gravitates natively. The matching condition that defines the split is

$$
D_iP^{i}=\varsigma\,\big(\rho_c-\bar\rho_c\big),\qquad 0\le\varsigma\le 1 ,
$$

and is *not* an extra Lagrangian term — it is the identification of the two descriptions on a solution
(§3.4, §7.3). On the static branch it is equivalent to `ς = M_ph(<r)/M_c(<r)`.

**Ordinary matter** is minimally coupled (`L_m`), with no direct `P·J` coupling; that absence is what makes
`α₁ = α₂ = 0` structural (A22).

### 1.1 One convention that must be stated

The BRIEF writes `K = 8πG`. The action above has `(R3 − 2Λ)/(4K) = (R − 2Λ)/(16πG)`, i.e. **`K = 4πG`**. Every
lane that used the action (A3, A12, A22, this one) uses `K = 4πG`; the BRIEF's `K` is the Einstein-tensor
normalisation (`G_{μν} = 2KT_{μν}` with `K = 4πG`) and is a different symbol. `c² = 1` in the action; SI is
restored only in the numbers.

---

## 2. The coefficient table

`D` = derived inside the theory, `M` = measured (a free coefficient whose value comes from data), `F` = free
(bounded only), `C` = chosen (an assumption of minimality), `P` = posit (a functional form with no derivation).
The machine-readable copy is `a33_results.json → coefficient_table`.

| # | term | coefficient | what fixes it | constraint | status |
|---|---|---|---|---|---|
| 1 | `(R3+K_ijK^ij)/(4K)` | `1/(4K)`, `K = 4πG` | definition of `G` (Newtonian limit) | exact | **D** |
| 2 | `−2Λ/(4K)` | `Λ = 1.0890e−52 m⁻²` | measured; tied to `a₀` by the closure | `Λ = 32πa₀²/c⁴` ⇔ `ΛL² = 32π`, `L = c²/a₀` | **M** |
| 3 | `−(1+β)θ²/(4K)` | `β` | nothing (free) | `β > 2ηa₀²/K` (principal positivity, round-2); background: `2+3β = 2Λ_bare c²/(3H²)` ⇒ `Λ_bare ≥ 1.462 Λ_obs` (K16); `β` invisible to `α₁, α₂, β_PPN` | **F** |
| 4 | `+P^iD_i\ln N` | `1` exactly | **derived**: the only `O(ε)` lapse source; any `ξ ≠ 1` deforms the law (K5: at `ξ=2`, `g_N − g²/(g+a₀) = −0.55 a₀` at `g = a₀/3`) | `ξ = 1` | **D** |
| 5 | `−W(u)` | `W = (a₀²/K)[−u/a₀ − \ln(1−u/a₀)]` | **derived**: `n = 1` Langmuir isotherm (one gate per site, A2) fixes the function; `W(0)=W′(0)=0` and `KW′ → u` fix the normalisation | cap `u < a₀`; `W″(0)=1/K`; the quadratic `W` gives a different law (K3b) | **D** |
| 6 | `+(η/2)E_iE^i` | `η` [L²] | nothing | `η > 0`, `η ≥ γ` (scalar luminality); `m² = K/η` is the FRW P mass | **F** |
| 7 | `−(γ/2)(D_iP^i)²` | `γ = KL_*²/2` [L²] | **measured** through `L_*`: `L_*² := 2γ/K` is a definition, so the content is `L_* ∈ [24,90] pc` (A20) | `γ ≤ η`; `L_*` window | **M** |
| 8 | `−(γ/4)F_ijF^ij` | the same `γ` | **chosen**: one stiffness | `γ_F = γ_L` is an assumption; it makes all three polarisation speeds equal (`γ/η`, K9) | **C** |
| 9 | `L_cold` | `ρ_c = (\Omega_c/\Omega_b)ρ_b = 5.3643ρ_b`, `σ_c = \sqrt{a₀L_*}` | cosmic share (A9/A11/A18) + measured dispersion | `M_c = 5.3643M_b` is *not* a cold-sector parameter | **D/M** |
| 10 | sourcing `ς` | `ς(r) ∈ [0,1]` | measured at two bands: `0.4716 ± 0.0362` (MID), `0.9865 ± 0.0984` (OUT) (A21) | **not a coefficient of the action**; `ς = f_ret(u/g_c)`, degenerate with the catchment (K15) | **M** (function unfixed) |
| 11 | `L_m` | `1` | equivalence principle | exact | **D** |
| 12 | turn-off `ν_fix = 1 + (ν−1)/(1+(y/y_t)²)` | `y_t = 66.2999` | **posit** (Zenodo 23171085); the *number* is derived from `F(y_t) = Λc⁴/a₀² = 100.4058` | not a term of the action; changes the interpolation only; origin unfixed | **P** / number **D** |
| 13 | `a₀ = κc\sqrt{Gρ_Λ}` | `κ = 1/2` | **measured/selected** (0.87σ in the saturation cap, A19); **not derived** (A15: `DIFFERENT-QUANTITY`) | `R ≡ Λc⁴/(8πa₀²) = 4 ⇔ κ = ½` | **M** |

**Count.** Four finite-dimensional free parameters — `κ`, `β`, `η`, `γ` — of which `κ` (0.5) and `γ`
(`L_* ∈ [24,90] pc`) have measured values and `β`, `η` have only bounds. Three free **functionals**:
(i) the scale-setting functional that would return exactly `R = 4`; (ii) `ς(r)`; (iii) the turn-off form.

**Degeneracies (five).**
1. `γ ↔ η`: every existing observable sees only `γ/η` (the scalar speed; the two constants enter the P mass
   separately and no measurement constrains it). The pair is one measurable combination today.
2. `γ ↔ L_*`: the same parameter (`L_*² := 2γ/K`). Not a degeneracy in principle, but it means `γ` has no
   independent handle.
3. `κ ↔ a₀`: with `Λ` measured, `a₀ = κc\sqrt{Gρ_Λ}` is one parameter, not two.
4. `β ↔ Λ_bare`: the background gives **one** equation, `2+3β = 2Λ_bare c²/(3H²)`, for two unknowns.
5. `ς ↔ f_ret`: a single-band amplitude cannot separate the sourcing fraction from the retained fraction
   (A21); only the band ratio does, at 4.9σ.

---

## 3. The field equations

Vary the action of §1. `ρ ≡ ρ_m + ρ_c` is the total matter density, `d ≡ D_iP^i`.

### 3.1 Lapse equation (Hamiltonian constraint)

$$
{}^{(3)}R-K_{ij}K^{ij}+(1+\beta)\theta^{2}-2\Lambda
=4K\Big[\rho_m+\rho_c+d+W(u)+\frac{\gamma}{2}d^{2}\Big]
\tag{L}
$$

*Verified:* K1 (residual 0 against the direct variation of the reduced action), K1b (`R3` formula returns 0 on
the isotropic-Schwarzschild slice `f = (1+m/r)^4` in exact rational arithmetic).
On the static branch (`K_ij = θ = 0`) this is `R3 = 2Λ + 4K(ρ + d + W + (γ/2)d²)` — A3's (H), same sign, same
`K = 4πG`. The P sector's contribution to the source is `+d + W + (γ/2)d²`: the **charge** `d` first, the
potential and the gradient energy as `O(ε²)`.

### 3.2 Shift equation (momentum constraint)

$$
D_j\big(K^{ij}-\theta h^{ij}\big)=2K\Big[j^{i}_{m}+j^{i}_{c}+j^{i}_{P}\Big],\qquad
j^{i}_{P}=-\eta E^{j}D^{i}P_j+\frac{1}{\sqrt h}D_j\!\big(\sqrt h\,\eta E^{j}P^{i}\big)
\tag{S}
$$

The clock term carries **no** `N^i` (it is `P^i∂_i\ln N`), and every other P operator is quadratic in `P`, so
`j_P = 0` identically for `E = 0`. This is (F2) of A22 and the reason there is no momentum density, hence no
`g_{0i}`, hence `α₁ = α₂ = 0`.

### 3.3 P equation

$$
D_i\ln N+\gamma\Big[D_i\big(D_jP^{j}\big)+\big(D_jP^{j}\big)D_i\ln(N\sqrt h)\Big]
+\gamma D_jF^{j}{}_{i}+\frac{\eta}{N}\big(\partial_t-\mathcal L_N\big)E_i
=\frac{KW'(u)}{u}\,P_i
\tag{P}
$$

with `KW'(u) = a₀u/(a₀−u)`. The `D_i\ln(N√h)` term is the lapse weight of the gradient energy — it is present
because the term is `N√h(γ/2)d²`, not minimally coupled. **Static spherical, `f = 1`** (`n₁ ≡ (\ln N)′`,
`d = P′ + 2P/r`):

$$
n_1\big(1+\gamma d\big)+\gamma\,d'=KW'(u),\qquad d'=P''+\frac{2P'}{r}-\frac{2P}{r^{2}} .
\tag{P-sph}
$$

*Verified:* K2 — the EL of the reduced action equals `(P-sph)` times a constant (`NV`). Two corrections fall
out of doing this from scratch:
- **A3's reduced P equation is missing its `γP″` term.** Its `Dt` chain runs over `(N,N′,N″)`, `(f,f′,f″)`,
  `(P,P′,P″)` but pairs `P′→P″` only through the `PV→PP` slot, so the `∂²L/∂P′²·P″` piece is dropped. Its
  conclusions are unaffected (K2 there is evaluated at `P = 0`, where the term vanishes), but the printed
  equation is not the exact one.
- The `(1+γd)` factor is a genuine non-linear correction; dropping it (the A22 regime, `γd ≪ 1`) gives
  `n₁ = KW′ − γd′`, whose constant-`P` limit is A22's `p(K + 2γ/r²) = |∇\ln N|` exactly.

### 3.4 Cold-sector equations

$$
p^{\mu}\nabla_\mu f_c=0,\qquad
\nabla_\mu T_c^{\mu\nu}=0,\qquad
\sigma_c^{2}\,\frac{d\ln\rho_c}{dr}=-\,g\quad(\text{static, spherical, isotropic}),
\tag{C1}
$$

with `g = |∇\ln N|` the total field (the Jeans equation, which is A15's eq. (4) — the same equation that
produced `σ²/v_c² = ½`). The sourcing identity and its inversion:

$$
D_iP^{i}=\varsigma\,(\rho_c-\bar\rho_c),\qquad
\varsigma(r)=\frac{M_{\rm ph}(<r)}{M_c(<r)}=\frac{u(r)}{g_c(r)},\qquad
g_c\equiv\frac{GM_c(<r)}{r^{2}} .
\tag{C2}
$$

`M_c` is the *catchment* cold mass; `M_c = 5.3643M_b` only if the system retains its full cosmic share.

### 3.5 The two cosmological equations

`P = 0` on FRW (§3.6), so the P sector contributes nothing to the background. With `ρ = ρ_m + ρ_c` and
`p = p_m + p_c`:

$$
3(2+3\beta)H^{2}=2\Lambda+4K\rho ,
\tag{F1}
$$

$$
(2+3\beta)\big(2\dot H+3H^{2}\big)=2\Lambda-4Kp .
\tag{F2}
$$

*Verified:* K10 (`H² = 2Λ/(3(2+3β))` exactly from the lapse variation of `L_bg`), K10b (the `a`-variation,
with `(F2)` reducing to `2Λ` for dust as the round-2 result states). For pure bare `Λ`, `H² = 2Λ/(3(2+3β))`,
`Ḣ = 0`.

**A constraint the record has not stated.** Combining `(F1)` with the definition of `Λ_obs`:
`2+3β = 2Λ_bare c²/(3H²)`. Setting `Λ_bare = Λ_obs = 1.0890e−52 m⁻²` and `H = H₀` gives **`β = −0.211`**, which
violates `β > 2ηa₀²/K > 0`. Hence the action's `Λ` cannot be the observed one: **`Λ_bare ≥ 3H₀²/c² = 1.462 Λ_obs`**
(K16). The de Sitter endpoint of this action is a *pure* de Sitter universe (`Ω_Λ,eff = 1`); matching the
observed `ΛCDM` budget requires the clock's negative background stress `ρ_β = −9βH²/(4K)` to cancel the excess,
which is one more reason `β` is not observable anywhere else.

### 3.6 No cosmic aether

On FRW (`N = 1`, `N^i = 0`, homogeneous `P`): every derivative in `(P)` vanishes, so it reduces to
`dW/du = 0`, whose **only** root is `u = 0` (`dW/du = u/[K(1−u/a₀)]`, K12a). Linearising about it,
`η(Ṗ̈_i + 3HṖ_i) + KP_i = 0`: a massive vector with `m² = K/η` (K12b), `m/H₀ = 2.6e8` for `η = γ`. So `P = 0`
is the unique homogeneous solution and there is no preferred-frame VEV.

---

## 4. What the action reproduces

Every entry is a check in `a33_checks.py`; the residual is printed in `a33.out`.

| result (lane) | how it comes out of §1 | check | residual |
|---|---|---|---|
| `g_N = g²/(g+a₀)` (the law) | `(P-sph)` gives `g = KW'(u)`; `(L)` integrated gives `g_N = g − u`; eliminate `u` | K3 | `0` |
| `μ(x) = x/(1+x)`, i.e. AQUAL (A13/A23/A24) | `gμ(g/a₀) = g_N` identically | K4 | `0` |
| the clock coefficient is 1 | any `ξ ≠ 1` gives `g_N = g(a₀+ξg−ξ²a₀)/(a₀+ξg)`, not the law | K5 | 0 at `ξ=1`; −0.55 a₀ at `ξ=2` |
| `c_T² = 1` exactly (A3) | no operator carries two derivatives of `h^TT`; the quadratic TT action is `a³(ḣ²−p²h²)/(16K)` | K6 | `0` |
| slip `Φ−Ψ = O(Ψ²)` (A12) | `Π = KW′(u)u = u²/(1−u/a₀) = O(ε²)` | K7 | `Π/ε² = q²`, `Π/ε → 0` |
| `α₁ = α₂ = 0` (A22) | `θ ≡ 0` static; no momentum density; the `w²` rescaling multiplies a **linear** potential `(GM/L_*²)r`, whose `α₁(r) = 2r²/L_*²` has no constant term | K8a–c | `0, 0, 0` |
| scalar speed `c_s = \sqrt{γ/η}` (A3) | transverse principal sector `ηṙ²/2 − γk²r²/2` | K9 | `γ/η` |
| `H² = 2Λ/(3(2+3β))` (round-2) | lapse variation of `L_bg` | K10 | `0` |
| `r_switch` scaling (A16/A20) | the P-sector's own gradient force `γ∂_r(D·P)` vs gravity, `n(3−n)/2·(L_*/r)²f_c = 1` | K11 | `r_sw = L_*\sqrt{n(3−n)f_c/2}` |
| `γ = KL_*²/2` | definition `L_*² := 2γ/K` — no content beyond that | K11a | `0` |
| no cosmic aether (A22) | `dW/du = 0` ⇒ `u = 0` unique; `m² = K/η` | K12 | `[0]`; `K/η` |
| saddle needs negative cold density (A13/A23) | `ρ_ph = D·P = ∇·((1−μ)∇Φ)/4πG`; a positive-mass medium needs `|D·P| ≤ ςρ̄_c`; A13's saddle amplitude is `114.8 ρ̄_c` | K13 | see §7.2 |
| `Λ = 32πa₀²/c⁴`, `a₀ = κc\sqrt{Gρ_Λ}` | closure | K14 | rel `< 4e-3` |
| `ς` is a catchment, not a coefficient | `ς = f_ret(u/g_c)`; a constant partition `ς = 0.4716` deforms the law by 0.243 at `g = a₀/2` (excluded) | K15 | `0`; 0.243 |
| `Λ_bare ≥ 1.462 Λ_obs` | §3.5 | K16 | `β(Λ_bare=Λ_obs) = −0.211 < 0` |

**The eight results the task names are all here**: the law (K3), `c_T² = 1` (K6), slip `O(Ψ²)` (K7),
`α₁ = α₂ = 0` (K8), the scalar speed (K9), `H²` (K10), `r_switch` (K11), the saddle (K13) — plus eleven more.

---

## 5. The static spherical system, closed

For reference, the three ODEs that every galactic result solves, with coefficients substituted
(`f` is the spatial conformal factor, `d = f^{-3/2}(r²\sqrt f P)′/r²`):

$$
{}^{(3)}R=2\Lambda+4K\big[\rho+d+W(u)+\tfrac{\gamma}{2}d^{2}\big],\qquad
n_1(1+\gamma d)+\gamma d'=KW'(u),\qquad
\sigma_c^{2}\frac{d\ln\rho_c}{dr}=-g .
$$

The third equation is the only place the cold medium enters the *field* equations at `O(ε)`; it is the Jeans
equation, and its solution `σ_c² = const` with `ρ_c ∝ r^{-2}` is the singular isothermal sphere — the
configuration whose ratio `σ²/v_c² = ½` (A15) is *not* `κ`.

*Consistency of the three:* `(L)` differentiated and `(P-sph)` substituted give
`(r²g)′ = Kρ_src r² + (r²u)′`, i.e. `g = g_N + u` with `g_N = GM_src/r²`, which is `(P-sph)`'s first integral.
That is why the law is *exact* and not an expansion, and why the P sector is a **charge** sector.

---

## 6. What is not fixed — the honest list

Three items, and they are the whole of what the action leaves open. Each is marked `F/P` in §2.

**6.1 The scale-setting functional (`κ`).** Nothing in §1 fixes `κ = ½`, i.e. `R ≡ Λc⁴/(8πa₀²) = 4`, i.e.
`ΛL² = 32π` with `L = c²/a₀`. A15 proved the closure route returns a different quantity (`μ = σ²/v_c²`, invariant
under a rescaling that moves `κ`), A1/A19 killed counting, dimensional analysis, strain saturation and the Euler
charge, and A19 showed the saturation cap admits only `R ∈ {1,2,4}` with the data excluding `R = 1, 2` at
6.14σ and 3.05σ. So `R = 4` is **selected, not derived**. The missing object is a local functional, with no
dimensionful parameter and no free dimensionless constant, whose stationarity on de Sitter returns exactly 4.
This is the single hole in Q1.

**6.2 `ς(r)`, the sourcing-fraction profile.** Measured at two bands (0.4716, 0.9865 — a 4.9σ difference), with
the scaling `ς ≈ (f_ret/R_cosmic)[y_v^{-1/2} − ½]` and `d\ln ς/d\ln M_v → +1/6`. The action does **not** contain
a mechanism for it: §3.4's identity defines `ς` on a solution, it does not predict it. What would fix it is a
statement about how much cold energy a system retains (equivalently `f_ret(M, environment)`), which is an
assembly/formation question, not a term in the Lagrangian. `ς = ½` is structurally excluded as an identity
(A21: it needs `w = −1/6`, a negative sound speed).

**6.3 The turn-off's origin.** `y_t = 66.2999` is *derived* from `F(y_t) = Λc⁴/a₀² = 100.4058` given the posited
form `ν_fix = 1 + (ν−1)/(1+(y/y_t)²)`. Nothing in §1 produces that form: it is a posit inherited from Zenodo
23171085, and it is not a term of the action (it modifies the interpolation, i.e. the `W` that the *static*
law uses, not the covariant `W(u)`). What is missing is a derivation of the turn-off scale from the action —
most plausibly from a term that couples `P` to the field's own curvature, which the action does not have.

Two further items that are *not* holes in the action but are open in the theory: `L_*`'s microscopic value
(bounded, 24–90 pc, not derived) and a UV completion of the cold sector (no established covariant parent).

---

## 7. What this document corrects, and what it could not do

**7.1 `r_switch` belongs to the P sector, not to a fluid pressure.** A16/A20 compute the switch-off from a
`Γ = 2` pressure `p = (γ/2)ρ_c²` and `c_s² = γρ_c`, which at the cosmic mean is `c_s = 0.72 m/s` — four
orders below the medium's `σ_c = 8.33 km/s`. Read as a fluid, the cold sector would have two wildly different
"temperatures". The action says what is going on: `(γ/2)(D·P)²` **is** the `Γ = 2` internal energy with
`D·P ↔ ρ_c − ρ̄_c`, so the stiff pressure is the P sector's elastic energy, not the medium's kinetic pressure.
`c_s = 0.72 m/s` is the *elastic* speed and `σ_c = 8.33 km/s` the *kinetic* dispersion; they are different
objects (ratio 1.2e4) and only the first enters the field equation that sets `r_switch`. The scaling `r_switch ∝ L_*\sqrt{f_c}` is unchanged; its meaning is
sharper.

**7.2 The saddle amplitude is not reproduced, only its sign.** K13 confirms (i) the exact identity
`ρ_c = ρ̄_c + D·P/ς`, (ii) `D·P = ∇·((1−μ)∇Φ)/4πG` — so a negative `D·P` *is* a negative cold density, and
(iii) that A13's published amplitude, converted with this document's unit
`\sqrt{GMa₀}/(Gd²) = 1.079e−24 kg/m³`, gives `114.8 ρ̄_c` (A13's own figure is 89.32, a 1.29× difference in the
definition of the mean cold density). What this lane could **not** do is reproduce the amplitude from a
from-scratch PDE solve: an axisymmetric finite-volume solve of `∇·(μ∇Φ) = 4πGρ_b` validates to 35 % on the
single-mass case (`g(0.3d) = 4.51` vs `3.33`) and is worse in `ρ_ph` near the null, so it is not fit to
adjudicate A13/A23's `−0.2362`. The *sign-definite* content — a midplane pancake with `ρ_ph < 0` in the deep
limit — is what the no-go needs, and that is confirmed independently. The amplitude is flagged, not certified.

**7.3 `ς` cannot be a coefficient of the action.** K15 shows that a *constant* partition coefficient
`ς = 0.4716` deforms the law by 0.243 at `g = a₀/2` — a 24 % effect, excluded by the RAR by orders of magnitude.
So the partition reading (`(1−ς)ρ_c` falls natively) is only consistent with `ς = 1`; the measured `ς < 1` must
be the *catchment* (`f_ret < 1`), i.e. `ς = f_ret(u/g_c)`, which is A21's own formula. This removes an ambiguity
in `FINAL_THEORY.md` §0, whose prose ("only a fraction `u` is sourced into the phantom; the rest falls
natively") is the partition reading and is not the one the data support.

**7.4 A3's P-equation transcription** (§3.3) — a real defect, no conclusion affected.

**What this does not do.** It does not derive `κ`, `ς(r)` or the turn-off; it does not UV-complete the cold
sector; it does not solve the exact static system with all `β, η, γ` and `f ≠ 1` (the `f`-equation is used only
to check the exact Schwarzschild solution); it does not re-derive the second-order PPN metric; and it does not
check the cosmological slip (`E²` active, `P̄` evolving), which A12 explicitly leaves open.

---

## 8. Checks

`a33_checks.py`: 28 checks, deterministic, stdlib + sympy, 1.2 s, no network, exit 0 iff all pass.
`--mutate {clock2,wquad,gamma0,beta0,ricciP,nocharge}` breaks at least one check each (see `MUTATE.md`).

```
K1   lapse eq = Hamiltonian constraint (exact)                 resid 0
K1b  R3 formula on isotropic Schwarzschild f=(1+m/r)^4        [0,0,0]
K2   P equation, static spherical, f=1                        ratio NV (constant)
K3   g_N = g^2/(g+a0)                                         0
K3b  quadratic W gives a different law                        nonzero
K4   AQUAL mu(x)=x/(1+x)                                      0
K5   clock coefficient = 1                                    0 ; 0.55 at xi=2
K6   c_T^2 = 1                                                1
K7   slip Pi = O(eps^2)                                       q^2 ; 0
K8a  theta = 0 static                                         0
K8b  no O(rho) momentum density                               0
K8c  alpha_1 from a linear potential                          0 ; 0
K9   c_s = sqrt(gamma/eta)                                    gamma/eta
K10  H^2 = 2 Lambda/(3(2+3beta))                              exact
K10b second cosmological equation                             exact
K11a L*^2 = 2 gamma/K                                         0
K11b r_switch = L* sqrt(f_c n(3-n)/2)                         exact
K12a dW/du = 0 has the unique root u=0                        [0]
K12b m^2 = K/eta                                              K/eta
K13a rho_c = rho_bar + D.P/varsigma                           0
K13b D.P = div((1-mu) grad Phi)                               0
K13c saddle requires |D.P| > rho_bar_c                        114.8 x
K14a Lambda = 32 pi a0^2/c^4                                  rel 1.2e-3
K14b a0 from Lambda                                           9.3542e-11
K14c kappa = 1/2 identity                                     9.3542e-11
K15a varsigma = f_ret (u/g_c)                                  exact
K15b a constant partition deforms the law                     0.243
K16  Lambda_bare >= 3H0^2/c^2 = 1.462 Lambda_obs              beta=-0.211
```

## 9. Reproduce

```bash
cd deepseek_push/DS_FINAL_2026_10_21/A33_master_action
python3 a33_checks.py --json-out a33_results.json | tee a33.out
python3 a33_checks.py --mutate clock2      # must exit 1
```