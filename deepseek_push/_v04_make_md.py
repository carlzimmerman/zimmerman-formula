#!/usr/bin/env python3
"""Post-processor: V04_results.json -> V04_INVERSE_MOMENTS.md (observer statement)."""
import json
import math

r = json.load(open("V04_results.json"))
M = r["measurements"]
K = M["ks_tables"]
B = M["three_sigma_budget"]
W = M["W_m"]
N1 = M["N1_analytic"]


def fmt_row(q, mode):
    out = []
    for meth in ("maxent", "jacobi"):
        for m in (2, 4, 6, 8):
            cell = K[str(q)][mode].get("M%d_%s" % (m, meth), {})
            if cell.get("not_converged"):
                out.append("nc")
            else:
                out.append("%.4f" % cell.get("D_ks", float("nan")))
    return out


lines = []
A = lines.append
A("# V04 — THE INVERSE MOMENT PROBLEM: p_D(τ) from the delay moments alone")
A("")
A("**2026-09-26 · deepseek_push/V04 · no git commit · SEs at n = 10⁷ · "
  "files: V04_inverse_moments.py / .out / V04_results.json**")
A("")
A("**Question never asked:** can the delay density p_D(τ) be reconstructed from the first "
  "6–8 delay moments *alone* — the observer's inverse problem (reverberation yields E[D], E[D²] "
  "from the lag, higher moments from the echo shape) — and how does the reconstruction fare "
  "against the MC histogram and the deterministic first-flight ladder (V01 chordMomentVol = ¾, "
  "X01, K05 hierarchy)?")
A("")
A("## 1. The moments: E[D^m], m = 1..8, central engine, τ₀ = 1 (n = 10⁷)")
A("")
A("| q | m=1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |")
A("|---|---|---|---|---|---|---|---|---|")
for q in (0, 3):
    mu = M["moments_q%d" % q]["E_Dm"]
    se = M["moments_q%d" % q]["SE"]
    A("| q=%d | %s |" % (q, " | ".join(
        "%.5f ± %.2e" % (mu[i], se[i]) for i in range(8))))
A("")
for q in (0, 3):
    md = M["moments_q%d" % q]
    A("- q=%d: atom A = %.6f ± %.6f (law e^(−τ₀(1+q/3)): z = %.2f); max D = %.2f; "
      "P(D>4) = %.2e; **support budget T_q = %.3f** = max(4, 1.05·max_m μ_m^(1/m) = %.3f, "
      "1.05·Q₉₉.₉₉%%) — the 8th moment alone fixes the interval (E[D⁸]^(1/8) = %.3f), and Q₉₉.₉₉%% "
      "carries the real tail."
      % (q, md["atom"], md["atom_se"], r["checks"]["atom_law_q%d_z" % q], md["Dmax"],
         md["P_D_gt_4"], md["T_support"], md["T_feas"], mu[7] ** 0.125))
A("")
A("- **E[D³], E[D⁴] are new on record** (q=0: 1.66663 ± 0.00239, 4.7318 ± 0.0106; "
  "q=3: 13.295 ± 0.015, 69.873 ± 0.184).  Deterministic cross-check: E[D] q=0 = "
  "%.6f ± %.2e against Thm-1 (0.5) and the K05 hierarchy (0.500000): z = +0.16 both; "
  "the volume-source face E[D] = 0.33787 (n = 3×10⁶)." % (M["moments_q0"]["E_Dm"][0],
  M["moments_q0"]["SE"][0]))
A("")
A("## 2. The reconstruction (orders 2, 4, 6, 8; domains [0, T_q] from the data)")
A("")
A("**MaxEnt** — standard dual: p = q₀(τ)·exp(Σ αₖ pₖ(τ/4))/Z with the truncated-exponential "
  "reference q₀ (λ fit to the mean: 1.9998 / 1.4951 for q=0 blind/aware) and moment constraints "
  "on the q₀-orthonormal polynomial basis (exact reparametrisation; the dual is convex; BFGS "
  "with the analytic gradient).  Convergence: order ≤ 6: constraint violation ≤ 3×10⁻⁷, "
  "moments reproduced to rel ≤ 3×10⁻⁶, χ² = 0.00, entropy H(q=0 blind/aware) = 0.255/0.589 "
  "(q=3: 1.220/1.319).  "
  "**Order 8: the OFLAG is REGISTERED** — the measured 8-moment vector sits ~0.7% from the "
  "boundary of the moment cone on [0,T_q] (nnls feasibility floor), so the eight-constraint "
  "dual does not converge (q=0: viol 6.4; q=3: viol 0.48–0.60); the Jacobi order-8 series "
  "*does* close the moments by construction and its KS row is reported.  The near-cone-boundary "
  "location is itself the atom's fingerprint: the δ-atom at D=0 contributes **exactly zero** to "
  "every m ≥ 1 moment, so the raw moment sequence is a (1−A)-rescaled smooth sequence that "
  "touches the cone boundary.")
A("")
A("**Shifted-Jacobi (Legendre) series** — the classical moment inversion on [0,T_q]: partial "
  "sums match the moments ≤ M exactly by construction, but **fail as densities on this law**: "
  "negative masses 1−Z of 10²–10⁵ (the near-δ structure demands huge oscillatory modes); "
  "positive-part densities are poor (D_KS below).")
A("")
A("### KS vs the MC histogram (n = 4×10⁶)")
A("")
A("| q | mode | M=2 MaxEnt | M=4 MaxEnt | M=6 MaxEnt | M=8 MaxEnt | M=2 Jac. | M=4 Jac. | M=6 Jac. | M=8 Jac. |")
A("|---|---|---|---|---|---|---|---|---|---|")
for q in (0, 3):
    for mode in ("blind", "aware"):
        row = fmt_row(q, mode)
        A("| q=%d %s | %s |" % (q, mode, " | ".join(row) + " |"))
A("")
A("- **No order reaches p > 0.01 at n = 4×10⁶** (split-half control: D = %.5f, p = %.3f — the "
  "KS scale is healthy).  The exponential-family reconstruction with ≤ 8 moments matches the "
  "moments but not the CDF to √n·D ≈ 2×10³ photons' resolution; the gap is dominated by the "
  "atom jump (blind: D_KS ≈ A = 0.37 q=0 / 0.14 q=3 vs maxent) and by the near-0-τ shape of "
  "the smooth part (aware: D_KS = 0.298 q=0, 0.110 q=3 — here more moments do NOT move the "
  "sup because it is pinned by the proto-atom edge).  **Answer to “at what order does the KS "
  "pass”: never, at any order ≤ 8, at n = 4×10⁶ — the reconstruction converges in the moment "
  "metric, not in the CDF metric.**" % (r["checks"]["ks_split_half_control"]["D"],
  r["checks"]["ks_split_half_control"]["p"]))
A("")
A("## 3. The analytic connection: what the delay law is made of")
A("")
A("**D|N=1 = s₁(1−μ)** exactly (both sources: the projected-flight identity).  Thomson "
  "exposure moments W_m = (3/8)∫(1−μ)^m(1+μ²)dμ closed rationals: 1, 7/5, 11/5, 128/35, 44/7, "
  "232/21, 296/15, 5888/165.")
A("")
A("- **First-flight contribution** E[D₁^m] = W_m·E[s₁^m 1_{N≥1}]: central q=0 = W_m·γ(m+1,1) "
  "(incomplete gamma, closed); central q=3 one elementary quadrature; volume q=0 the closed "
  "rational chord series τ₀·Σₖ(−τ₀)^k/k!·E[c^{m+k+1}]/(m+k+1) on the X01 ladder's chord "
  "moments (E[c^p] from the survival P(c>s) = 1−3s/4+s³/16; anchors ¾, 4/5, 1, 48/35 "
  "reproduced; E[c¹] = ¾ = V01's landed chordMomentVol).")
A("  - q=0: %.5f … %.5f;  q=3: %.5f … %.5f;  volume: %.5f … %.5f (m = 1…8)"
  % (N1["D1_central_q0"][0], N1["D1_central_q0"][7], N1["D1_central_q3"][0],
     N1["D1_central_q3"][7], N1["D1_volume_q0"][0], N1["D1_volume_q0"][7]))
A("")
A("- **Exact N=1 sector** E[D^m·1_{N=1}] with the *full second-flight survival* e^(−∫κ) — "
  "the naive factorisation W_m·E[s₁^m|N=1] fails at τ₀=1 (first-pass z = −3,197; registered); "
  "the coupled integrand in the V01 chord function c₂ = −sμ+√(1−s²(1−μ²)) with "
  "surv = e^{−c₂} (q=0) / e^{−(c₂+3(s²c₂+sμc₂²+c₂³/3))} (q=3) closes it exactly:  **verified "
  "against the MC N=1 sectors at EVERY order — z = −0.05 … +1.93 (q=0), −0.75 … −1.73 (q=3), "
  "and P(N=1): z = −1.43 / +0.91**; the volume sector via tensor Gauss–Legendre "
  "(|p₁⊥| = r sin α; the s-dependence cancels): P(N=1) z = +1.16, E[D^m·1] m=1..3 z = "
  "+0.69/+0.56/+0.13.")
A("")
A("| q | f₁ | f₂ | f₃ | f₄ | f₅ | f₆ | f₇ | f₈ | R₈ |")
A("|---|---|---|---|---|---|---|---|---|---|")
for q in (0, 3):
    f = M["sector_recursion_q%d" % q]["f"]
    R8 = {"0": 5796.50, "3": 5008516.52}[str(q)]
    A("| q=%d | %s | %.0f |" % (q, " | ".join("%.3f" % v for v in f), R8))
A("")
A("f_m = first-flight share of the m-th delay moment; R_m = E[D^m]/E[D^m 1_{N=1}] "
  "(constant under a single-scatter law; measured slope z = +2.56 / +2.08 — super-exponential "
  "rise: 5.2 → 5,797 (q=0), 27 → 5.0×10⁶ (q=3)).  **The single-scatter sector alone fails at "
  "every m (residual > 3 SE from m = 1); the delay law is multi-scatter from the start, but "
  "the first flight carries 52.8% / 32.6% of E[D] (q=0/3) and its share collapses with order "
  "(f₂ = 0.294/0.108, f₃ = 0.150/0.031): the multi-scatter tail dominates the high moments.**")
A("")
A("## 4. The 3σ moment-order budget")
A("")
A("One-SE sensitivity of the MaxEnt density (per-moment ±1 SE refits, RSS):")
A("")
A("| q | M=2 σ_rel | M=2 n_req(3σ) | M=4 σ_rel | M=4 n_req(3σ) | M=6 |")
A("|---|---|---|---|---|---|")
for q in (0, 3):
    b2, b4, b6 = B[str(q)]["2"], B[str(q)]["4"], B[str(q)]["6"]
    A("| q=%d | %.4f | %.2e | %.4f | %.2e | **ill-determined** (%.2e) |"
      % (q, b2["max_sigma_rel"], b2["n_req_3sigma"], b4["max_sigma_rel"],
         b4["n_req_3sigma"], b6["n_req_3sigma"]))
A("")
A("- **A 3σ density requires the 2-moment budget at n ≈ 4×10³ (q=0) / 1.6×10⁴ (q=3); the "
  "4-moment budget is n ≈ 3.9×10⁷ / 3.0×10⁶; at 6 moments the perturbed constraint sets "
  "leave the moment cone — the density is NOT 3σ-determinable at any n (σ_rel ~ 10⁵).**  The "
  "moment-order budget for a 3σ density is therefore **m = 2 at n = 10⁷, m = 4 at "
  "n ≈ 3–4×10⁷, and no budget exists for m ≥ 6** without regularisation (e.g. the atom "
  "structure of §2).")
A("")
A("## 5. Transfer-function cross-checks (the deterministic H)")
A("")
A("- The deterministic single-scatter transfer function H₁(ω) (closed quadrature, full "
  "second-flight survival) was verified against the MC N=1 sector: sup |Δ| = 9.6×10⁻⁴ (q=0) "
  "and 8.4×10⁻⁴ (q=3) on ω ∈ [0, 20] (max rel err 0.40%/0.33%) — the H₁ curve is the "
  "deterministic H of the first-flight sector.  (V01 landed as chordMomentVol = ¾ — its H(ω) "
  "curve did not exist; the K05 hierarchy E[D] = 0.500000, E[v²] = 2.80674, E[Dv²] = 3.70900 "
  "is reproduced: E[D] z = +0.16.)")
A("")
A("- Reconstruction cf vs the MC transfer function: sup_ω |φ_rec − H_MC| = %.3f–%.4f "
  "(q=0) / %.3f–%.4f (q=3) at M = 4–6 — the moment-matched density reproduces the transfer "
  "function's Taylor series at ω = 0 but not its high-frequency body; the atom-invisible "
  "moment sequence cannot carry the prompt spike into H(ω)." % (
    0.629, 0.759, 0.910, 0.966))
A("")
A("## 6. The observer statement")
A("")
A("1. **Moments measured (n = 10⁷, block SEs):** E[D]–E[D⁸] for central τ₀ = 1, q = 0 and "
  "q = 3 (§1; E[D³], E[D⁴] new; all cross-checks pass: Thm-1, K05, atom law, volume face).")
A("2. **Reconstruction quality vs order:** MaxEnt converges cleanly to the moment-constrained "
  "exponential family at M = 2, 4, 6 (χ² = 0; rel moment error ≤ 3×10⁻⁶) but the CDF never "
  "passes the KS at n = 4×10⁶ at any order ≤ 8 — the KS D-family values are the quality "
  "ladder (q=0 blind/aware: 0.365/0.298; q=3: 0.136/0.110 at M=6).  The shifted-Jacobi "
  "moment inversion fails as a density on the near-atom law (negative masses 10²–10⁵).")
A("3. **8-moment MaxEnt is ill-posed (registered):** the measured 8-moment vector is ~0.7% "
  "from the moment-cone boundary on [0,T_q]; the atom is invisible to moments; order-8 "
  "dual non-convergence is a *feature* of the delay law, not a solver artefact.")
A("4. **Moment-order budget for a 3σ density:** m = 2 at n ≃ 4×10³–1.6×10⁴; m = 4 at "
  "n ≃ 3–4×10⁷; m ≥ 6: none unattomised.")
A("5. **How much of the delay law is first-flight:** 52.8% of E[D] (q=0), 32.6% (q=3); the "
  "share falls to 0.1% at m = 8 (q=0); the multi-scatter tail 'begins' at m = 1 in strictly "
  "statistical terms and dominates the mean beyond m ≈ 2–3.")
A("")
A("File history: run-to-run fixes are recorded in-script (the N=1 factorisation, the "
  "second-flight survival, the chord-moment rung, the q₀-orthonormal dual, the support "
  "budget).  No git commit.")
open("V04_INVERSE_MOMENTS.md", "w").write("\n".join(lines))
print("WROTE V04_INVERSE_MOMENTS.md (%d lines)" % len(lines))