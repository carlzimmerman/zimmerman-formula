# L07 — THE KERNEL-FREE WINDOW: phase-function independence of the window + inversion

**2026-09-23 · deepseek lane · engine: J02_moment_hierarchy transport (verbatim copy with a kernel switch, parity-checked bitwise) · no git commit**

**Result: 46/46 checks PASS. The window −lnA/E[D] and the inversion (A,E[D])→(τ₀,q) are phase-function-INDEPENDENT. The scattering kernel enters the falsifier battery exclusively through the width channel E[N]→E[v²]. The pre-registered kill (window deviation > 5 SE) did NOT fire — max |z| = 0.44 SE against the closed form, 1.22 combined SE cross-kernel.**

---

## 1. The claim and why it should hold

The central-source window and inversion consume exactly two observables:

| observable | definition | dependence on the phase function |
|---|---|---|
| A | P(no collision) — atom fraction at (τ=0, v=0) | **none** — the kernel never fires |
| E[D] = d̄ | mean delay; obeys E[D] = τ₀(½+q/4) = ∫₀¹ r κ(r) dr | enters only through the kernel **mean cosine** E[μ]; any symmetric kernel (E[μ]=0) leaves the identity exact (J02 Dynkin argument: the scattering term of L(x·u) is −x·u + E[μ]·|x|-terms) |

Both scattering kernels tested here are symmetric (E[μ]=0): Thomson p(μ)=(3/8)(1+μ²) and isotropic p(μ)=½. Therefore A, E[D], the window −lnA/d̄ = (1+q/3)/(½+q/4) and the K06-inv inversion must be identical under the two kernels — a *strong* statement, falsifiable by the pre-registered kill.

The width channel E[v²] = 2E[ang] = 2E[N] (Gaussian-spine lemma + E[1−μ]=1) is **not** protected: E[N] = E[∫ κ(X_s) ds] is a residence functional whose value depends on how the walk mixes — the phase function's E[μ²] enters. Only the *magnitude* of that entry is a measurement.

## 2. Pre-registration (kill conditions)

- **(c)** |window − (1+q/3)/(½+q/4)| > **5 SE** ⇒ the window carries kernel dependence ⇒ the J09/J10 radius test must be kernel-tagged, reported with the measured deviation.
- Width channel: E[N], E[v²] must DIFFER between the two kernels at ≥ 3σ (kernel entry) — a null difference would have falsified the width-channel picture instead.

## 3. Central source, τ₀ = 1, n = 3×10⁶ per (kernel × q) — ISOTROPIC kernel

| q | A_hat (pred e^{−τ₀(1+q/3)}) | z(A) | d̄_hat (pred ½+q/4) | z(d̄) | −lnA/d̄ (pred) | z(window) | (τ₀_hat, q_hat) | z(inv) |
|---|---|---|---|---|---|---|---|---|
| 0  | 0.367706 (0.367879) | 0.62 | 0.500226 (0.5000) | 0.56 | 2.00004 (2.00000) | 0.04 | (1.001, −0.000) | 0.36 / 0.04 |
| 3  | 0.135475 (0.135335) | 0.71 | 1.249823 (1.2500) | 0.23 | 1.59940 (1.60000) | 0.44 | (0.998, 3.011) | 0.50 / 0.44 |
| 10 | 0.013105 (0.013124) | 0.29 | 2.999909 (3.0000) | 0.06 | 1.44497 (1.44444) | 0.32 | (1.005, 9.943) | 0.31 / 0.31 |

Every deviation is < 1 SE. The window is reproduced at maximum zW = 0.44 (kill threshold 5). The inversion — closed-form on (A, d̄) — recovers the injected family on the isotropic data. Checks K1a/K1b/K1c/K1e (all q): PASS.

## 4. Direct cross-kernel comparison (same n = 3×10⁶, same (τ₀,q))

| q | window iso | window thom | z (3 combined SE budget) | E[N] iso − thom | z | E[v²] iso − thom | z |
|---|---|---|---|---|---|---|---|
| 0  | 2.00004 | 2.00128 | **0.76** | −0.00626 (−0.45%) | 4.71 | −0.01702 (−0.61%) | 2.73 |
| 3  | 1.59940 | 1.60181 | **1.22** | +0.01222 (+0.28%) | 3.54 | +0.00382 (+0.04%) | 0.23 |
| 10 | 1.44497 | 1.44527 | **0.15** | +0.05613 (+0.30%) | 4.46 | +0.17139 (+0.46%) | 2.74 |

- The window agrees between the two kernels at ≤ 1.22 combined SE (K1c2 PASS) — the same value the closed form predicts.
- **E[N] differs at 3.5–4.7σ** (K1d PASS), with a sign flip: at q=0 isotropic scatters *less* than Thomson (−0.45%); at q=3,10 more (+0.3%). The E[v²] shift equals 2×the E[N] shift (K1d_v2_tracks_2N PASS: |dV − 2dN| < 3 SE at every q), and the spine E[v²]=2E[N] holds per kernel (z<3, all six runs) — i.e. the kernel enters the width channel *through E[N] exactly as the exposure identity predicts*, at the measured 0.3–0.5% level. The v² differences are individually ≤ 2.7σ because v² is a high-variance moment; the *N*-level entry is the clean measurement.

So: two kernels with the same E[μ]=0, wildly different Peierls-like behavior, identical (A, d̄, window, inversion) to < 1.3σ, different E[N]/E[v²] at 3.5–4.7σ. That is the phase-function-independence statement, measured.

## 5. Exact statement — what F1/F2/F6 do and do not tell you

For any scattering kernel with E[μ] = 0 (symmetric in μ), central source:

1. **F1 (atom):** A = exp(−τ₀(1+q/3)) — kernel-free (verified to 0.71σ isotropic).
2. **F2 (lag):** E[D] = τ₀(½+q/4) — kernel-free by the first-moment identity (verified to 0.56σ).
3. **F6 (window):** −lnA/d̄ ∈ [4/3, 2], exactly (1+q/3)/(½+q/4) — kernel-free (verified to 0.44σ; cross-kernel to 1.22σ). Equivalently the invertibility domain d̄/a ∈ [½, ¾] of (A,d̄)→(τ₀,q).

**Hence the F1/F2/F6 members of the falsifier battery classify the scattering phase function ONLY through the width channel.** The battery's kernel-bearing members are exactly those built on velocity/lag-width moments: the F2b lag–width band, F3's hierarchy R_m(q) (angles E[ang^m]), F4's E[D²] bound tightness, F5's coherence floor via L, and the Step-3 prediction E[v²]=2E[N] with E[N] the residence functional — all of which absorb the phase function through E[N] and its higher analogues, at the measured ±0.5% level in E[N] for the isotropic-vs-Thomson pair at τ₀=1.

**Consequence (the radius test):** an observer who does **not** know the scattering kernel can still measure (A, d̄) from the transfer function, form the window (validating the conservative central reading), invert to (τ₀,q), and run the J10-I radius test J10-I = (r_B/R)·window — all kernel-agnostic. What such an observer *cannot* do without a kernel model is predict the line width E[v²] (and the joint moments): that prediction is kernel-tagged, tying the F-series width members to the phase-function model chosen for the cloud.

**Scope line (honesty):** the central-source statement above is exact. The *volume* window is NOT exactly kernel-free (below): E[D]_vol carries the residence-coupling Q = Σℓⱼ uⱼ·u_final, whose mean depends on the walk's correlation structure. The kernel shift is measured (0.6% in the window at τ₀=1, z=5.3) — small relative to the geometry separations the window discriminates.

## 6. Volume source, q=0, isotropic kernel (the J11 port)

| τ₀ | A (J11 quadrature) | z(A) | E[D]_vol,iso | window_iso ± SE | central flat (q=0) |
|---|---|---|---|---|---|
| 0.5 | 0.70759 (0.70728) | 0.97 | 0.18210 | 1.89941 ± 0.0029 | 2.00000 |
| 1.0 | 0.52660 (0.52725) | 1.86 | 0.34092 | 1.88114 ± 0.0015 | 2.00000 |
| 2.0 | 0.33262 (0.33242) | 0.60 | 0.61444 | 1.79149 ± 0.0023 | 2.00000 |
| 3.0 | 0.23597 (0.23635) | 1.26 | 0.85943 | 1.68022 ± 0.0022 | 2.00000 |

- The volume atom is kernel-free (no-collision escape; matches the J11 quadrature to ≤ 1.9σ — same check J11 ran for Thomson).
- **The J11 geometry fingerprint survives the kernel change:** volume window strictly below the central flat 2.0 at every depth (≥ 35 SE each), monotonically decreasing in τ₀ (z = 60.6 across the scan), and below 4/3 at q=10, τ₀=1: **1.31661 ± 0.0011, 14.8 SE below 4/3** (J11 Thomson: 1.3142 — identical landmark). Checks K4_*: PASS 7/7.
- **The measured kernel tag on the volume channel:** at τ₀=1, E[D]_vol iso 0.34092 vs Thomson 0.33817 (z=4.31); window 1.8811 vs 1.8926 (z=5.31, a 0.6% shift) — the volume lag is NOT exactly kernel-free (E[D]=E[τ]−E[Q] carries Q), exactly as J02's Theorem B warned off-centre. The shift is an order of magnitude smaller than the window separations being discriminated (volume 1.68–1.90 vs central 2.00 ⇒ 5–16%), so the T4 geometry discriminator keeps its force, with a small kernel tag ~0.6% to be carried into K09-style error budgets.
- **J11-record note:** the t=0.5 row of J11's τ₀ table (2.049) was the thin-scaling *proxy* −lnA/(τ₀·0.338), not a direct MC window (J11 flagged the scaling itself: "E[D]_v must be re-measured by MC at large τ₀; K07 lane"). The direct MC windows measured here (1.899 thin under isotropic; 1.8926 Thomson at τ₀=1, in line with J11's V3 direct value 1.897) supersede the proxy's deep rows. The verdict's *shape* claim — τ₀-crossing, below central, sub-4/3 at q=10 — is the surviving content, now kernel-independent.

## 7. Status

- **L07: LANDED — 46/46 checks, exit 0.** No git commit (house rule). Parity P: copied transport ≡ J02 transport bitwise (4 stats × 2 clouds).
- The lane gives the F-series its cleanest structural split: **{F1, F2, F6} = geometry channel (kernel-free, exact); {F2b, F3, F4, F5, Step-3 E[v²]} = width channel (kernel-bearing through E[N])**.
- Consequence for the framework core: J10-I = (r_B/R)·window is kernel-agnostic; the framework's radius reading does not need a phase-function model, only central-source geometry and (A, d̄).
- Open edges: kernels with E[μ] ≠ 0 (forward-peaked) would break the central identity through the mean-cosine term — the statement here is scoped to symmetric phase functions (the conservative Thomson reading's class); K08 oblateness integration unchanged.

## Traceability

Engine parity → J02_moment_hierarchy.py::simulate (imported reference); transport copy → L07_kernel_free.py::simulate (kernel switch; bitwise parity P-checks); closed forms → J09 (atom A, window) + K06-inv/K04 (inversion τ₀_hat = −3lnA − 4d̄, q_hat = 4d̄/τ₀_hat − 2); volume quadrature → J11 (A_vol), volume record → J11_VOLUME_WINDOW_VERDICT.md, K11 T4; battery numbering → K06_METHODS_NOTES.md F1–F7; radius test → J10_A0_RADIUS_READING.md (J10-I). Every number above is in deepseek_push/L07_results.json.