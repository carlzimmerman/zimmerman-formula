# FC-KH TERMINAL FALSIFICATION MISSION (overnight autonomous run)

**Goal:** determine whether FC-KH v1.0 admits a globally stable, hyperbolic spherical
MOND→Newtonian transition on the observational khronometric branch. **DO NOT ASSUME A PASS.
DO NOT ASSUME A KILL. Derive the actual result. Prefer a rigorous PARTIAL over a fabricated
completion. Terminal verdict is three-way: PASS / KILL / UNRESOLVED.**

## HARD RULES (non-negotiable)
- **NEVER run git add / commit / push / reset / checkout / stash.** This repo is the user's
  human-curated work log; touching git history is forbidden. Write ALL artifacts as plain files
  under `qwen_claude_field_theory/closure_2026/fc_kh_terminal/` only. Untracked files are fine.
- Do not silently change the action or conventions. Do not delete prior results.
- Never turn a numerical artifact into a physics conclusion. Never report PASS from f'' alone,
  from the homogeneous scalar-speed formula alone, or because no instability was found at a
  finite number of points.
- Start commit hash is recorded in `START_COMMIT.txt`.

## TARGET THEORY
S_FC = (M_Pl^2/2) ∫ d^4x √-g [ R − ((β+3λ)/3) θ² − β σ_{μν}σ^{μν} + f_FC(a) ] + S_m[g,ψ]
with
  f_FC(a) = −2Λ + α a² + 2(2−α) a0² [ 1 − (1+a/a0) e^{−a/a0} ].
Geometry: X=−∇_μT∇^μT>0; n_μ=−∇_μT/√X; h_{μν}=g_{μν}+n_μn_ν; a_μ=n^ν∇_ν n_μ; a=√(a_μa^μ);
K_{μν}=h_μ^ρh_ν^σ∇_ρn_σ; θ=∇_μn^μ; σ_{μν}=K_{μν}−(1/3)θh_{μν}.
Branch: α=2β, β>0, λ>0, β≪1. Benchmark P1: (α,β,λ)=(2e-15, 1e-15, 1e-3).
Scan: α=2β; β∈{1e-18,1e-16,1e-15,1e-14}; λ∈{1e-6,1e-5,1e-4,1e-3,1e-2,1e-1}.

## ★ THE CORRECT KILL CRITERION (read before Phase 5) ★
The old sufficient condition f_B''≤0 (f_B=−f_FC/2) FAILS near a~a0 — this is EXPECTED and is
**NOT** a kill (Flanagan proves the BM sufficient conditions cannot hold across the whole
interpolation; he does NOT prove instability). Do NOT test f'' as the kill criterion.
Derive the FULL β,λ≠0 reduced quadratic scalar action and its dispersion polynomial
  P(ω²,k;r) = A(r) ω² − B2(r) k² − B4(r) k⁴/M_*² − …
- IR long-wavelength stability: **A(r)>0 and B2(r)>0** (c_IR²=B2/A>0) through the transition.
- UV: B4(r)>0. A positive k⁴ term can regulate a high-k band but CANNOT cure a genuine
  B2<0 long-wavelength (k→0) instability — do not use k⁴ to hide a B2<0.
- KILL only if A<0 or B2<0 is UNAVOIDABLE over the α=2β branch in 1≲a/a0≲38 (the f''>0 window),
  radial AND tangential modes. The β,λ terms are spatial (∂∂π)² at leading order and reach A only
  through shift/metric constraint back-reaction — that reduction is the crux; do it explicitly.

## SEED — BB ADM / unitary-gauge decomposition (start here for Phases 4–5)
In preferred-foliation ADM variables the generalized theory is
  S = ((1−β)/16πG) ∫ N√γ [ K_ij K^ij − ((1+λ)/(1−β)) K² + ³R/(1−β) + f(a)/(1−β) ].
(Bonetti-Barausse arXiv:1502.05554; L4/M*², L6/M*⁴ are SPATIAL-derivative-only UV terms → no
Ostrogradsky time ghost, Hořava anisotropic scaling.) In unitary gauge T=t the khronon lives in
lapse/shift/γ. **The quadratic TIME-derivative (kinetic) terms come from K_ijK^ij − ((1+λ)/(1−β))K²,
NOT from f(a).** Eliminating the scalar shift gives a bare scalar kinetic coefficient
  K_scalar ∝ (2+β+3λ)/(β+λ) > 0  on β>0, λ>0  ⇒ f''(a) sign change is NOT a ghost.
f''(a) enters the SPATIAL lapse-gradient constraint. So the decisive terminal objects are the
radial/tangential IR gradient speeds AFTER the lapse constraint is eliminated on the MOND background:
  c²_{2,∥}(a/a0;β,λ) > 0  AND  c²_{2,⊥}(a/a0;β,λ) > 0  through 0.5≲a/a0≲2.
Minkowski cross-check: c_s²=(α−2)(β+λ)/[α(β−1)(2+β+3λ)], c_T²=1/(1−β). L4,L6 handle high-k;
they cannot rescue a k→0 (c²₂<0) IR instability. Compute c²₂∥, c²₂⊥ — that is the whole game.

## SHARPENED TARGET (use this — collapses the problem)
Static spherical background ⇒ K_ij=0 ⇒ β,λ do NOT alter the MOND background (χ controls it), they
act ONLY on perturbations. Local frozen-background method: freeze ā at r*, y=ā(r*)/a0, decompose
into radial (k∥) and transverse (k⊥); principal symbol A ω² − B∥ k∥² − B⊥ k⊥² + … = 0, A from the
K_ij sector, B's carry the acceleration Hessian. KEY SIMPLIFICATION:
  transverse Hessian ∝ f'/a = 2[α+(2−α)e^{−y}] > 0 ALWAYS ⇒ B⊥ never flips from the accel sector;
  radial Hessian ∝ f'' = 2α+2(2−α)(1−y)e^{−y} ⇒ the ONLY dangerous direction.
So the whole transition collapses to: **B∥(a;β,λ) = B_f[f''] + B_KH[β,λ,ā] > 0 near a~a0**, i.e. does
B_KH > |B_f| in 0.5≲y≲2. Rescue is structurally possible because K_ij=0 means β,λ don't touch the
background, only stabilize perturbations. Terminal quantity: min_{y,k-angle} eigenvalue(K⁻¹G) > 0.
CONSISTENCY CHECKS the symbol MUST pass: high-a limit → c_T²=1/(1−β) and
c_s²=(α−2)(β+λ)/[α(β−1)(2+β+3λ)]; deep-MOND limit checked independently.
EMPIRICAL ANCHOR (BB): β+λ=0 is the strong-coupling corner (1PN gravitomagnetic term ∝1/(β+λ));
BB require β+λ ≳ 2.5e-7 (20% 1PN tolerance). So λ~1e-3 is MOTIVATED, not an arbitrary rescue knob.
Scan β∈{1e-18…1e-12}, λ∈{1e-7…1e-1}, α=2β; maximize min(B∥,B⊥)/A. Do NOT stop when f'' flips.

## PHASES
0. **Repo audit** — inventory existing FC-KH/khronometric action, symbolic, spherical-background,
   PPN, MOND-limit, stability code under `qwen_claude_field_theory/`. Reuse verified code. Record
   start hash.
1. **Convention lock** — from Bonetti-Barausse arXiv:1502.05554 and Flanagan arXiv:2302.14846,
   verify sign of f(a); defs of α,β,λ; α1,α2; G_N; G_C; c_T; c_s; slow-motion scaling. Do NOT mix
   BB and Blanchet-Marsat/Flanagan conventions. Write `CONVENTION_MAP.md`.
2. **Symbolic action verification (sympy)** — verify f'=2a[α+(2−α)e^{−y}]; f''=2α+2(2−α)(1−y)e^{−y};
   χ=f'/2a; μ_phys=(1−χ/2)/(1−α/2) → prove μ−(1−e^{−y})≡0; small-a f→−2Λ+2a²−(2(2−α)/3)a³/a0;
   large-a f→−2Λ+αa². G_N=2G/(2−α).
3. **Full spherical background** — DO NOT insert the MOND equation by hand. Derive static
   spherically-symmetric background from the FULL action; document gauge; solve numerically for
   a(r) through u=a/a0 ∈ {≪1,0.1,0.5,1,2,10,≫1} with adaptive resolution + convergence check.
   Use ≥1 point-mass exterior and ≥1 smooth finite-density source. Dimensionless x=r/r0, u=a/a0.
4. **Quadratic perturbation theory** — perturb the COMPLETE theory g=ḡ+δg, T=T̄+π to 2nd order.
   Do NOT infer S² from the homogeneous scalar speed. Separate non-dynamical / constraint /
   propagating variables; integrate out non-dynamical (lapse δN, shift δN_i — δN_i sourced by π̇);
   produce the reduced principal quadratic form. Don't assume a single scalar before the count.
5. **Principal symbol** — q~exp[i(kr−ωt)]; build P(ω,k,r); det P=0; extract physical scalar
   branches ω²=c_i²(r,k)k²+…; for each: kinetic eigenvalue A, gradient B2, sound speed, hyperbolicity.
   Apply the KILL CRITERION above (A>0, B2>0 IR; B4>0 UV; no zero-A strong coupling).
6. **Transition scan** — for each (β,λ) on α=2β, evaluate P continuously through a/a0∈[0.01,100],
   dense near 0.5–2. Record min_A, min_B2, min/max c_s², min discriminant, every sign change.
7. **Stable-window search** — optimize (β,λ) on α=2β to maximize min_{r,k,mode}{A,B2,hyperbolicity};
   log search. Any candidate PASS must survive 2×/4×/8× resolution, ≥6 decades in k, a changed
   background profile, a parameter perturbation, and an independent second numerical route.
8. **WKB / high-k** — scan kr∈{1e-3…1e6}; classify instability as low-k / high-k / finite-k /
   transition-radius. Report finite-k separately from UV.
9. **Background robustness** — repeat around point-mass, smooth compact, Hernquist, exponential.
   Determine if any stability is structural or background-specific.
10. **Constraint overlay** — c_T²=1/(1−β); scalar speed; G_N=2G/(2−α); G_C=2G/(2+β+3λ); G_N/G_C.
    Check GW, Solar-System, pulsar, cosmology, PPN with current primary literature (state dates).
11. **Kill switch** — KILL if unavoidable over the branch: A<0, or B2<0 (IR), or c_s²<0, or complex
    speeds, or forced zero-A strong coupling, or background fails before Newtonian regime, or MOND
    not recovered. Classify any failure A(structural)/B(benchmark)/C(parameter)/D(numerical)/E(coord).
12. **PASS criteria** — PASS requires ALL of: full action derived; background solves full eqs;
    MOND limit recovered; S² explicitly derived; A>0; B2>0; real speeds; no uncontrolled strong
    coupling; survives resolution + k-range + background refinement; ≥1 point also passes obs
    constraints. Else FAIL/UNRESOLVED.
13. **Literature comparison** — compare to Flanagan's statement that the BM sufficient conditions
    cannot hold across the full interpolation. If β,λ let FC-KH escape, SHOW THE ALGEBRA; if not,
    derive the no-go. Do not assume the outcome.
14. **Reproducibility artifacts** — write RESULTS.md, PASS_KILL.md, CONVERGENCE.md,
    CONVENTION_MAP.md, STABILITY_OPERATOR.md, PARAMETER_SCAN.csv, PARAMETER_SCAN.json + source +
    param files + solver settings + raw output + symbolic expressions (+ plots if feasible).
15. **Final report** — exactly one of GLOBAL STABILITY PASS / KILL / UNRESOLVED, then: surviving/
    failed region; min stability margin; worst transition point; its a/a0, r, k; kinetic & gradient
    eigenvalues; scalar & tensor speeds; G_N/G_C; convergence evidence. PASS ⇒ reproduce the
    strongest point independently. KILL ⇒ give the obstruction and show why β,λ tuning can't evade.
    UNRESOLVED ⇒ name the exact derivation that blocks certification.

## AUTONOMY
Work continuously through the phases without asking for confirmation. Symbolic first, then
numerics once equations are well-defined. If one approach fails, debug and try an independent
formulation. Do not stop at the first plausible stable point (PASS needs the global scan +
refinement). Do not stop at the first instability (first prove it's unavoidable across the branch).
The goal is not to make FC-KH pass — it is to determine whether FC-KH passes.
