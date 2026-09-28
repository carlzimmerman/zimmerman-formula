# AS669 — Topological flux integral and metric-volume dependence of the vacuum

**Run:** `AS669-r1-20260928T143344Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent, single-run worker seed; host macOS 26.5.2
**Task hash:** `4006975c1141d3aac813eb5804a6b47b3012774c686152549e9ad6cff7243b0e` (verified at start, matches dispatch value)
**Branch:** Explicit coefficient-mechanism diagnostic — k04 four-form promotion; no transfer to filtered MONO claimed.
**Gate:** Requirement 13 (a0–vacuum relation, "preserved as input or genuinely derived"), ORCHESTRATOR cell A03. Gate stays OPEN (kappa adopted).

---

## 0. Source pinning and prerequisite status

| Source | SHA-256 | Status |
|---|---|---|
| `deepseek_push/astra_spawn_ideas/AS669_topological_flux_integral_and_metric_volume_dependence.md` | `4006975c1141d3aac813eb5804a6b47b3012774c686152549e9ad6cff7243b0e` | matches dispatch + on-disk read in full |
| `kappa_closure/k04_four_form_promotion_consistency.py` | `15c0a7e13eb9b7a5fdb403c8826bd01912d68dc81614609fddb6cd6ed9d32399` | matches SOURCE_MANIFEST.json pin exactly |
| `deepseek_push/astra_spawn_ideas/FRAMEWORK_CONTRACT.md` | `ca696c7fe7cccbe21d754eff833a4c59df6dee962ea61f50f04b5d20d80dddf9` | read in full |
| `deepseek_push/astra_spawn_ideas/RESULT_CONTRACT.json` | `621fdad0067c731654a0fa95eb7a4dd112f8829b96503d8d57c2ee8ca2cc1517` | read in full |

Prerequisite **AS657** (`AS657_flux_boundary_term_changes_the_variational_ensemble.md`): the seed's explicit prerequisite has **no run on record** (`results/AS657/` absent; no claims found). This run therefore treats AS657 as *blocked-on-dependency-not-yet-executed*: the flux-integral identity here is derived from first principles and from the pinned k04 source only; nothing is inherited from AS657. The upstream chain actually read for this run: `results/AS067/AS067-r1-20260928T103724Z-dsv4f-hermes/result.json` (exact additive zero-mode gauge degeneracy), `results/AS068/run_20260928T1030/result.json` (boundary-fixed vacuum negative), `results/AS069/AS069-r1-20260928T114316Z-dsv4f-hermes/result.json` (vacuum datum lambda-blind), `results/AS075/AS075-r1-20260928T121520Z-dsv4f-hermes/result.json` (T2O: premise B = shift-free vacuum equation E*; k04 listed there as the extension-cell candidate). All four are `unreviewed` evidence, used as context only — nothing accepted as theorem.

Record on k04's own record: `kappa_closure/k04_F6_CORRECTION_2026-09-27.md` (lane XR31) supersedes k04's F6 stability reading (F6 tests the flux's secant stiffness only; the slaved scalar is unstable for 2.39 < g_N/a0 < 155). **F1–F2 are explicitly unaffected** — those are exactly the pieces this seed's identity exercises; the correction is recorded, not imported.

---

## 1. Step 1 — fixed source equation, independent variables, boundary conditions, measure

**Model cell (k04, unmodified):** compact connected oriented Riemannian 4-manifold $(M^4, g)$ with Riemannian volume form $\varepsilon_g$ (measure $=\sqrt{-g}\,\mathrm d^4x$; boundary $\partial M=\varnothing$). A closed four-form field strength $F_4$ (dual amplitude $q$) with the **homogeneous ansatz**

$$\boxed{\,F_4 = q\,\varepsilon_g\;,\quad q = \text{const on } M\,}\qquad\Phi(g)\equiv\int_M F_4 = q \int_M \varepsilon_g = q\,\mathrm{Vol}_4(g)\;.$$

Vacuum action density (k04): $\displaystyle P(q)=\frac{Z}{2}q^2 + b\,\beta^2 q^2$, $Z,\beta,b>0$; promoted scale $a_0=\beta\sqrt{G_N}\,|q|$; the $b$-term is the k01 primitive promoted to the flux ($b=(2-K_B)I_{\mathrm{rar}}/(16\pi)$, $I_{\mathrm{rar}}=0.4525248967$, $K_B\in\{0,1/4\}$, imported — see §6). The gravitational part of the action and the matter coupling are untouched (same-theory discipline; only the flux sector of k04 is varied).

**First-principles obligation (before fixing any normalization):** vary the candidate flux action with $F_4$ **held fixed form-wise** (its de Rham class is the topological datum). Constraint: $q\sqrt{-g}=F_{0123}=\text{const}$ in coordinates, so under metric variation $\delta(q\sqrt{-g})=0$, i.e.

$$\delta q = \tfrac{q}{2}\,g_{\mu\nu}\,\delta g^{\mu\nu}, \qquad q(\lambda)=\lambda^{-4}q\ \text{under } g\mapsto\lambda^2 g .$$

Then $\delta S=\int\!\sqrt{-g}\,\big[-\tfrac12 P\,g_{\mu\nu}+\tfrac12 qP_q\,g_{\mu\nu}\big]\delta g^{\mu\nu}$, giving (verified symbolically in the run)

$$T_{\mu\nu}=(P-qP_q)\,g_{\mu\nu},\qquad \varepsilon_{\mathrm{vac}}\equiv qP_q-P\;.$$

**Boundary conditions / ensemble:** closed manifold (no boundary term); the flux enters the variational problem only through its total period $\Phi=\langle[F],[M]\rangle$ (de Rham pairing). The homogeneous amplitude is *not* an independent boundary datum — it is forced by the flux, see §5.

---

## 2. Step 2 — fixed integrated flux vs fixed local $q$ under volume variation

From the identity $\Phi=q\,\mathrm{Vol}_4$ (exact, symbolic; S2) the two single-fix responses under a metric variation with $\delta\mathrm{Vol}_4\neq 0$ are:

| regime | response | vacuum consequences |
|---|---|---|
| **fixed local $q$** ($\delta q=0$, field-amplitude fixed) | $\delta\Phi = q\,\delta\mathrm{Vol}_4$ (S3) | $\varepsilon_{\mathrm{vac}},a_0,\kappa$ **unchanged**; total flux linear in volume (N2b: $\Phi_2/\Phi_1=(R_2/R_1)^4=16$ at $R_2=2R_1$) |
| **fixed integrated flux** ($\delta\Phi=0$, topological period fixed) | $\delta q=-q\,\delta\mathrm{Vol}_4/\mathrm{Vol}_4$ — dilution law $q=\Phi/\mathrm{Vol}_4$ (S2, N2a: $q_2/q_1=(R_1/R_2)^4=1/16$) | $q\propto\mathrm{Vol}_4^{-1}$, $\varepsilon_{\mathrm{vac}}\propto\mathrm{Vol}_4^{-2}$, $a_0\propto\mathrm{Vol}_4^{-1}$ (N3); **$\kappa^2$ unchanged** (N3, F2) |

The vacuum energy of a fixed flux therefore *dilutes* as $1/\mathrm{Vol}_4^2$ (in the conformal picture $\varepsilon_{\mathrm{vac}}(\lambda)=\lambda^{-8}\varepsilon_{\mathrm{vac}}(1)$, verified symbolically), while the local-amplitude regime keeps it constant. **Both regimes leave the same coincidence untouched**:

$$\kappa^2 \equiv \frac{a_0^2}{G_N\,\varepsilon_{\mathrm{vac}}} = \frac{2\beta^2}{Z+2b\beta^2}\qquad\text{(S4: } q,\ \mathrm{Vol}_4 \text{ cancel identically; Lean T7/T8)} .$$

---

## 3. Step 3 — every integration constant independent until its equation fixes it

Independent symbols carried separately: $Z$, $\beta$, $b$ (imported k01 datum), $q$, $\mathrm{Vol}_4$, $\Phi$, and (F3's $d\mathcal L/dq=\mathrm{const}$ integration constant) $q_0$. Nothing is set by the flux identity beyond the relation $q=\Phi/\mathrm{Vol}_4$. Separation of roles:

- **Constructed candidate (this branch):** the flux sector $P(q)$ with the identity $\Phi=q\,\mathrm{Vol}_4$, the Legendre energy $\varepsilon_{\mathrm{vac}}=qP_q-P$, and its coefficient consequence (S5, Lean T9): $\kappa=1/2 \iff Z/\beta^2 = 8-2b$.
- **Inherited (imported, not derived here):** $b=(2-K_B)I_{\mathrm{rar}}/(16\pi)$ from k01's primitive on the *RAR* kernel ($\Delta(s)=s/(e^{\sqrt s}-1)=h_{\mathrm{RAR}}(s)$, $I_{\mathrm{rar}}=j(s_{\mathrm{sat}})=0.4525248967$, $s_{\mathrm{sat}}=2.53963828219$ — reproduced, S7; the operative filtered-MONO analogue is **not** used and not transferred).
- **Adopted:** $\kappa=1/2$ itself (framework input; this run derives only what the volume channel can and cannot do — it cannot select it, §6).

No fit: the S⁴/T⁴ fixtures are declared (radius/period as free declared parameters; one refinement at dps=100). $Z/\beta^2$ is **not fitted**; its k04 value $7.96399$ ($K_B=0$) / $7.96849$ ($K_B=0.25$) is reproduced from the imported datum and quoted as the value at which $\kappa=1/2$ *would* hold.

---

## 4. Step 4 — negative control: $q$ and total flux simultaneously fixed (capable of failing)

**Premise under test:** $\delta q = 0$ and $\delta\Phi = 0$ simultaneously under a metric change. The identity's first variation is exact:

$$\delta\Phi = q\,\delta\mathrm{Vol}_4 + \mathrm{Vol}_4\,\delta q \quad\Longrightarrow\quad 0 = q\,\delta\mathrm{Vol}_4 \ \text{if both are fixed}.$$

For $q\neq 0$ (nonzero flux) this forces $\delta\mathrm{Vol}_4=0$: **the simultaneous-fixing premise is consistent only for volume-preserving variations**. The violated identity is $\delta\Phi = q\,\delta\mathrm{Vol}_4$ with residual $q\,\delta\mathrm{Vol}_4\neq 0$ at every volume-changing variation — equivalently, the constraint system $\{\Phi=q\,\mathrm{Vol}_4,\ q=\text{const},\ \Phi=\text{const}\}$ has one identity and two fixed responses: rank 1 versus 2, overdetermined.

- **Algebraic (exact, Lean T1/T2/T10):** $q\neq 0 \Rightarrow qV=qW \Rightarrow V=W$; hence $V\neq W \Rightarrow \neg(qV=qW)$.
- **Witness (S⁴ round, $R_1=1$, $R_2=2$):** fixed-$q$ flux ratio = 16, fixed-$\Phi$ amplitude ratio = 1/16 (both 60-digit exact); the simultaneous-fixing residual $q\,\mathrm{Vol}_4(1)\cdot 15 = 0.00452\ldots\ \mathrm{kg}^{1/2}\mathrm m^{7/2}\mathrm s^{-1}\neq 0$ (NEG1). Central finite differences confirm each single-fix law to 1e-10 (N4, N5).
- **Capability of failing:** the check is constructed so that it passes only if $\mathrm{Vol}_2=\mathrm{Vol}_1$; any volume-changing pair fires. It discriminates: with the identity in hand the premise fails at every pair of distinct volumes and at every nonzero flux (R1 refinement keeps the identity at 1e-95).

---

## 5. Step 5 — verification by substitution and independent representation

1. **Substitution (symbolic):** $\varepsilon_{\mathrm{vac}}=qP_q-P=P$ for quadratic $P$ (exact, S1/Lean T5); $T_{\mu\nu}=(P-qP_q)g_{\mu\nu}$ re-derived from $\delta S$ (conformal law $\delta(q\sqrt{-g})=0$, T-derivative checked); $Z/\beta^2=8-2b$ from $\kappa^2=1/4$ (S5, Lean T9); positivity $\varepsilon_{\mathrm{vac}}>0$ for $Z,b>0$, $q,\beta\neq 0$ (Lean T6).
2. **Direct integration (S⁴, T⁴, mpmath dps=60, one dps=100 refinement):** $\int_{S^4}\varepsilon=8\pi^2R^4/3$ (N1a, R1), $\int_{T^4}\varepsilon=(2\pi)^4$; the flux identity $\Phi=q\,\mathrm{Vol}_4$ holds at 60-digit level at $R\in\{1,\tfrac32,2\}$ in both regimes (N2a/N2b/N3).
3. **Independent representation (cohomology + Stokes):** on a closed manifold $\int_M\mathrm dC=0$ (N6: adding the exact term $\mathrm dC$, $C=\sin x^0\,\mathrm dx^1\wedge\mathrm dx^2\wedge\mathrm dx^3$ on $T^4$, changes the period only at the quadrature floor $|{\int}\mathrm dC|<10^{-54}\,\Phi$). $H^4_{\mathrm{dR}}(M)\cong\mathbb R$ for connected compact oriented $M$, so every closed $F_4$ is cohomologous to a **unique** homogeneous representative: $F_4=q\,\varepsilon_g+\mathrm d\eta$ with $q=\Phi/\mathrm{Vol}_4$ — the total flux selects the homogeneous amplitude with no freedom (N7). The exact part $\mathrm d\eta$ is pointwise non-homogeneous but period-invisible.
4. **Limiting/boundary cases in the same measure:** $q\to 0$: $\varepsilon_{\mathrm{vac}}\to 0$, $a_0\to 0$ — the promotion loses its source (N8); $\mathrm{Vol}_4\to\infty$ at fixed $\Phi$: $q\to 0$ (dilution); the $\kappa^2$ expression is regular in both since it contains no $q$ or $\mathrm{Vol}_4$.

---

## 6. Result — derived equations, scope, and the missing input

**Derived equations (all exact in the declared class; Lean-certified core T1–T10):**

- (E1) fixed-flux amplitude law: $q=\Phi/\mathrm{Vol}_4$, $\delta q/q=-\delta\mathrm{Vol}_4/\mathrm{Vol}_4$;
- (E2) fixed-local-q law: $\delta\Phi/\Phi=\delta\mathrm{Vol}_4/\mathrm{Vol}_4$;
- (E3) representation: flux fixes only the homogeneous amplitude; exact parts are period-invisible;
- (E4) negative-control theorem: $(\delta q=0\wedge\delta\Phi=0)\Rightarrow\delta\mathrm{Vol}_4=0\ \text{or}\ q=0$;
- (E5) coefficient consequence: $\kappa^2=2\beta^2/(Z+2b\beta^2)$ — **the metric-volume channel is $\kappa$-blind**: it relates $q$ to $\mathrm{Vol}_4$ (or vice versa) but cancels from the coefficient, and $\kappa=1/2\iff Z/\beta^2=8-2b$ remains a one-number/two-couplings ratio (k04 F2 deficit, unaffected by the volume channel, unaffected by XR31's F6 correction).

**Footings (both carried separately, never simultaneously fixed):** canonical $a_0=9.3619\times10^{-11}$: $q=1.1460\times10^{-5}$, $\varepsilon_{\mathrm{vac}}=5.25270\times10^{-10}\,\mathrm{J\,m^{-3}}=4a_0^2/G_N=\rho_\Lambda c^2$, $\kappa=1/2$; alternative $a_0=1.1279\times10^{-10}$: $q=1.3807\times10^{-5}$, $\varepsilon_{\mathrm{vac}}=7.62422\times10^{-10}\,\mathrm{J\,m^{-3}}$, $\kappa=1/2$ — identical couplings $Z/\beta^2$, identical $\kappa$ (F1). Fixed-density relabel $\kappa_{\mathrm{eff}}=a_{0,\mathrm{alt}}/(2a_{0,\mathrm{can}})=0.6023884041$ recorded as diagnostic only (F1).

**Precisely named missing inputs** (the seed's completion criterion): (i) an equation fixing $Z/\beta^2$ (the "why $8{-}2b$" question) — nothing in the flux sector, the volume identity, or the bulk action supplies it; (ii) in the fixed-flux regime, the flux datum itself: $\Phi$ (lattice unit $\varphi_0$ and winding $n$, if quantized) is an adopted input — the volume identity only *relocates* the freedom (amplitude $\leftrightarrow$ flux), in the same pattern AS068/AS069/AS075 established for the boundary reference and the kernel label. The k04 feedback equation $d\mathcal L/dq=\mathrm{const}$ (F3, i.e. the environmental $q_0$) is the one place $q$ is locally constrained, and its integration constant $q_0$ is likewise an adopted datum.

**Domain:** compact connected oriented $M^4$ (witnesses: $S^4$ round, $T^4$ flat; $R\in\{1,\tfrac32,2\}$, one dps=100 refinement), homogeneous $q$, quadratic flux action, $Z,b,\beta>0$, $K_B\in\{0,1/4\}$, RAR-kernel $I_{\mathrm{rar}}$ datum imported (no MONO transfer). Algebraic statements: all $q\neq 0$, $\mathrm{Vol}_4\neq 0$; numerics at 60–100 digits are finite evidence; exactness rests on the symbolic identities and the Lean certificates.

**What this does not establish:** no selection of $\kappa=1/2$ (stays adopted); no statement on the operative filtered-MONO branch (the RAR-based $I_{\mathrm{rar}}$ is a comparison datum); no dynamics, no criterion-B statement, no empirical test, no transfer of stability statements (XR31's F6 correction respected); AS657 (the seed's explicit prerequisite) has no executed run on record — flagged for the orchestrator.

---

## 7. Bounds, controls, artifacts

- Prototype: `ulimit -t 120` CPU cap enforced; wall 0.37 s; max RSS 62,636,032 bytes ≈ 59.7 MiB ≪ 512 MB (`/usr/bin/time -l`, err_time.txt; RLIMIT_AS not enforceable on macOS — measured, same convention as AS067/AS068/AS075); 1 thread (single-threaded CPython; OMP/OPENBLAS/MKL/NUMEXPR/VECLIB_NUM_THREADS=1; no multiprocessing). 24/24 checks PASS, exit 0.
- Negative control NEG1 (simultaneous fixing) is the discriminator; exact algebra S2–S6; representation N6/N7; footings F1/F2; limits N8; refinement R1/R2.
- Lean 4 (Mathlib v4.34-rc2, `lake env lean`, compile host only): 10 theorems, compile exit 0, zero `sorry`, unfiltered `#print axioms` for all 10 = `[propext, Classical.choice, Quot.sound]` (lean_check.out, lean_axioms.out).
- Failed attempts (harness, fixed; physics untouched): (1) dict-key FD indexing crash at `q_fix_Phi[1+h]` (KeyError) — replaced by direct evaluation; (2) N6 exact-equality check too strict for the dps=60 quadrature floor — replaced by relative 1e-54 threshold; (3) R1 reference computed at dps=60 after the reset — reference re-computed at dps=100; (4) Lean T3 `rw [←h1, h2]` order and missing $V_2\neq 0$ (derived from the hypotheses), Lean T7 trailing `ring` after `field_simp` closed the goal (removed).
