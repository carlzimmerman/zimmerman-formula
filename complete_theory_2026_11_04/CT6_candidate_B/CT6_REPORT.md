# CT6: candidate B (Lambda-projector khronon), graded to its first failed gate

Lane under CT_GATES_COMMON.md and owner decision D1 ("Yes, grade it"): a go to grade, not an adoption. The cold sector retired 2026-11-01 stays retired; no particle. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour the framework. Criteria frozen first in FROZEN_CRITERIA.md. Numbers: ct6_g0_health.py -> ct6_g0_health.out (sympy, single thread, seconds).

**Verdict: G0 FAILS. Candidate B stops at G0; G1-G3 are not graded.**

## The action

Host v3s (V3_FULL_PICTURE.md:23-37), units c = 1, 8 pi G = 1:

    S = ∫ √−g { (1/2)[R − 2 J(Y; a_geo²)] + K_BS(Q) } − (γ_L/2)∫ √−g [max(D·P, 0)]² + S_m,
    J = Λ − G(Y, A),  G = 2A[u − ln(1+u)],  u = √Y/√A,
    A ≡ a_geo² = ξ Qp,   Qp = K²/3 + (2/3) L_n K,   K = ∇_μ u^μ (khronon leaves).

On FRW Qp = 3H² + 2Ḣ (out:1) = Λ − p (out:2): dust cancels, as CT1 said. Auxiliary form: A(Qp) → μ Qp − Ṽ(μ), Ṽ'' = 1/A_QQ, and μ L_n K integrates by parts exactly (out:3) to μQp = −(μ/3)K² − (2/3)K L_n μ, which removes the Ṅ and K̇ that Qp carries.

## G0, item by item (frozen lines (a)-(e))

- **Degeneracy is not available.** G depends on A first at Y^(3/2), as −(2/3)Y^(3/2)/√A (out:7), which is the deep-MOND scale invariance: a_geo must enter as (ξQp)^(−1/2). So the action is nonlinear in L_n K wherever Y > 0 (Hessian A''·(2/(N²a))², out:12-15; A·G_AA = −u³/(2(1+u)²) ≠ 0, out:6). The P-form of v3s has the same onset, w³/(3√A K_c) (out:11). One extra scalar (4 DOF against v3s's 3).
- **(a) FAIL: the count changes between backgrounds.** On FRW, Y = 0, so A, A_Q and A_QQ all vanish (out:7, 14): B's quadratic action there is v3s's (3 DOF). Around any Y > 0 background it has a fourth scalar. The fourth mode is strongly coupled around FRW.
- **(b) passes where it is defined.** Unlocked kinetic matrix (ζ, μ) has det = 1/μ̄ (out:16-17); μ̄ = ξ f(u)/2 > 0 (out:4-5, 18). No ghost where Y > 0 and Qp > 0.
- **(c) passes.** Fast mode c_s² = u/3 ≥ 0 (out:19). The extra mode is dispersionless and tachyonic, with ω² = 3μ̄/(2A_QQ) (out:20) = −1.00 to −2.97 Qp for u = 1e-3 to 1e3 (out:24-28). That is a Hubble-rate, k-independent growth. Frozen coefficients cannot decide it: UNDECIDED (out:29).
- **(d) FAIL: static backgrounds are singular.** Static leaves have K = L_n K = 0, so Qp = 0. Then dG/dA diverges like s/√A (out:10): the quadratic action has infinite coefficients, and a0 = 0 there. Wherever Qp < 0 (FRW above z ≈ 11.3, CT1_REPORT.md:67; any contracting leaf), √A is imaginary and the action is complex.
- **(e) FAIL: the constraint escape is on record.** A CMC multiplier (cuscuton/VCDM type) removes δQp at k ≠ 0, but that is the VCDM + f(a²) structure with f → G, and dG/dY at Y = 0 is 1 (out:7, 31). That is exactly the premise f_s(0) = 1 of FLRW_OBSTRUCTION.md: negative matter kinetic coefficient, c_UV² = −1/(6 + 9c_m²) < 0 (out:32). The K_BS lapse mass drops out of that k → ∞ limit. The cuscuton record (sol61_push/.../cuscuton/REPORT.md) adds that a0 tied to a constrained field moves with H. Matching the premises was checked here; the theorem itself was not re-derived.
- W4b is inherited UNDECIDED (CT2_REPORT.md:7).

Limits of the check: flat frozen background, k ⟂ ā (the ā·k cross terms only shift the slow mass at O(H)), P stiffness sector and expansion terms left out. None of these touches (a), (d) or (e).

## Hand-set constants

- ξ (κ² = 8πξ, a TRADE; κ = 1/2 is not derived);
- L★ ≥ 21.7 / 22.9 pc (v3s);
- μ_K (free);
- the J_x form (POSTULATED);
- Λ;
- the dust abundance (an initial condition).

The 2/3 coefficient is fixed by the requirement that dust cancels, so it is not a free knob.

## Not graded

G1-G3 and beyond. A side note, not a grade: the Qp = 0 on static leaves found at G0(d) is the same fact behind CT1's G2 kill test.
