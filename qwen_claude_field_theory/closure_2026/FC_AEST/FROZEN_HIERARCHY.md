# FC-AeST — FROZEN HIERARCHY (2026-08-28)

The relativistic-MOND / Fried-Chicken program, consolidated. This is a **freeze**, not a new result:
every line below is backed by a committed, runnable script cited inline. The scientific endpoint is
now **empirical**, not architectural — see §4.

---

## 1. CLOSED (structurally dead, each on its own terms)

| # | Object | How it dies | Committed proof |
|---|--------|-------------|-----------------|
| C1 | **2-DOF C_M constraint chassis** (MMG: `C_M=D_i[μ D^i ln N]−4πGρ`) | γ_PPN=0, α₁=+4, α₃=−1, Newtonian matter non-conservation — all kernel-blind. Deleting H_⊥ simultaneously buys 2-DOF and kills lensing + matter conservation. | `closure_2026/REFEREE_REPORT_FINAL.md`, `RUN_ALL_GATES.py` 13/13; RETRACTIONS.md 2026-08-27 |
| C2 | **6-DOF shift-symmetric K(Q) as an *evolving*-DE mechanism** | Shift charge `a³K'(Q)=I₀` forces the K-sector = **constant DE (w=−1) + dust (a⁻³)** for *any* K. So a₀²=−κ²c²G·K(Q) → constant; no evolving a₀(z). | `scripts/fc_inverse_KQ_nogo_2026.py` (exit 0); RETRACTIONS.md 2026-08-28 |
| C3 | **Exact-exponential FC kernel μ_obs=1−e⁻ʸ (and tanh field fn) under Cassini** | Observable EFE phantom quadrupole q=0.166 = **3.76× the Park+ ceiling**, K_B-blind in the full 6-DOF vector solve. | `scripts/fc_cassini_CORRECTED_2026.py`; `refute_transverse_KB_lock_2026.py` 12/12; `typeII_direct_variation_2026.py` 44/44 |

The narrow escape from C2 — **break the AeST shift symmetry with a potential V(φ)** — is also committed-dead:
`nbody_2026/routeB_dust_to_dark_energy_2026.py` shows the shift-breaking route reaches only the **phantom
side (cannot cross w=−1)** and is short 4–12× vs DESI + the 0.30-dex floor. **So there is currently no
demonstrated local 6-DOF route from the AeST Q-sector to evolving dark energy.**

## 2. STILL ALIVE (a coherent relativistic-MOND chassis, with declared liabilities)

**6-DOF AeST + sharp μ_n (n≳4–5).** The two-field bridge `μ̃=μ_n/(2−μ_n)` (f_G=½) is kernel-agnostic; a
sharp observable μ_n is Cassini-safe (μ₅ 0.31×, μ₁₀ 0.06× of the ceiling — `fc_cassini_CORRECTED_2026.py`),
inheriting AeST's c_T=1, γ_PPN=1 (Φ=Ψ lensing), 6-DOF count. **Costs (all real):** RAR 0.108→0.127 dex;
6 DOF (not 2); κ, Z fitted; and the inherited-open AeST liabilities untouched by any kernel choice —
**low-k unbounded-H mode** (2109.13287), **oscillatory 3rd spherical regime** (2304.05134), **c_s²
superluminal at SS scales** (set by K₂, not the kernel).

## 3. PHENOMENOLOGICAL HYPOTHESIS (not a theorem of the field theory)

**a₀² = κ²c²G ρ_DE.** Realizable in 6 DOF only as a **constant-a₀ point-identification** at the dS minimum
(ρ_DE=−K(Q₀)=const, w=−1) — see C2. Making a₀(z) *evolve* requires a **separate quintessence field χ
(7 DOF)**, in which `w_χ(z) = −1 + (2/3) d ln a₀/d ln(1+z)` holds but **w_χ(z) is imported through the
choice of P(X_χ,χ), not predicted by AeST symmetry** (`fc_flrw_quadratic_gate.py`: χ canonical, c_χ²=1,
sequestered O(δ³)). So a₀²∝ρ_DE is a **fit target the chassis can carry, not a law it forces.**

**FC-7 (the concrete 7-DOF candidate action):** AeST + sharp μ₁₀ + canonical χ + a local Lagrange lock
`ζ[α²−κ²c²G·E_χ]` promoting the MOND scale to an auxiliary scalar α. Its **ground-state / quadratic
closure is now VERIFIED** (`scripts/fc7_groundstate_closure_2026.py`, exit 0, 15/15): (a) the auxiliary
(α,ζ) pair is algebraically eliminable (2 second-class pairs, ζ₀=0 at the ground state) — no propagating
pair, so N_phys=6+1=7 *locally*; (b) sharp-kernel sequestration `J₁₀(x)=x³/3+…` ⇒ `F_MOND=O(Y^{3/2})=O(δ³)`
⇒ **L_MOND^(2)=0**, no quadratic MOND ghost on the vacuum; (c) constant-a₀ dS vacuum `α₀²=κ²c²GV₀`
(χ=χ₀, χ̇=0), so a₀ need not evolve; (d) BTFR `v⁴=Gα M_b` exact in the spherical reduction. (One harmless
transcription typo caught: `x=(y/2)(1+μ₁₀)` should be `(2−μ₁₀)`; did not propagate.) **The last gate — perturbative half now VERIFIED** (`scripts/fc7_reduced_action_rank_2026.py`, exit 0):
integrating out (α,ζ) gives the reduced action `S_AeST + S_χ + ∫α(∇χ)²J₁₀(√Y/α)`; the derivative coupling
does **not** spoil the rank perturbatively because (S1) the aether-orthogonal projector `(g^μν+A^μA^ν)`
*exactly* removes φ̇ from Y (verified symbolically: Y = spatial gradients only), so the MOND term carries
no φ̇ ⇒ **zero contribution to K_φφ and K_φχ ⇒ it cannot induce a φ–χ kinetic degeneracy**; and (S2) the
one entry it does touch, K_χχ, is corrected only at `df/du = J₁₀−(x/2)J₁₀' = −x³/6 = O(Y^{3/2})`. So near
the vacuum `det K = K_AeST·(1+O(Y^{3/2})) > 0` — 7 DOF preserved in the whole vacuum neighborhood.

**Still genuinely OPEN (NOT PASS, no shortcut):** the **fully-nonlinear (large-Y) Poisson rank** of the
enlarged 3+1 Hamiltonian (the one remaining fundamental field-theory gate); PPN γ/β/α₁/α₂/α₃; Φ=Ψ for the
*full nonlinear* galaxy solution (only *inherited on the ground-state branch*, not FC-7-derived);
general-background c_T; FLRW growth; the AeST outer oscillatory regime. **And crucially: FC-7 being
consistent does NOT change a₀²∝ρ_DE from imported to derived** — V(χ) is *chosen*, the lock is *imposed*;
a clean phenomenological realization, not a symmetry consequence.

**FC-8 (the frozen shape — supersedes FC-7's lock).** Change the lock `α²=κ²Gρ_χ → α²=κ²GV(χ)` (potential
only). Verified (`scripts/fc8_clean_lock_2026.py`, exit 0): (i) `C_ζ=α²−κ²GV(χ)` carries **no χ-momentum**
(`∂C_ζ/∂χ̇=0`), so the lock no longer grafts onto the χ kinetic constraint algebra; (ii) the reduced MOND
term `κ²GV(χ)·J₁₀(√Y/√(κ²GV))` depends on χ **only through V(χ)** — no χ̇, no ∇χ — so it contributes
**identically zero to every kinetic entry AND to the χ gradient entry, at all orders** (vs FC-7's nonzero
O(Y^{3/2}) K_χχ correction). χ is a fully healthy canonical scalar; FC-8 adds **no** new ghost/gradient
risk in the χ sector. Vacuum still exact: `a₀,₀²=κ²GV₀`, ζ₀=0, δ²S_MOND=0, BTFR `v⁴=Ga₀M_b` untouched.
**Price (honest):** `a₀²=κ²GV` equals κ²Gρ_χ **only when potential-dominated** (χ̇²≪V) — so a₀²∝ρ_DE is
exact only in the slow-roll/frozen regime, and remains **imported** (V chosen). a₀ still evolves iff χ rolls.
**Genuinely OPEN, unchanged (no shortcut):** full *nonlinear* Dirac rank of the enlarged 3+1 system; PPN
γ/β/α_i; nonlinear Φ=Ψ; the *inherited* AeST φ-sector stability (low-k mode) + outer oscillatory regime;
FLRW growth. Rating: **9/10 — right mathematical shape, not proven viable.**

## 4. THE ENDPOINT IS NOW EMPIRICAL

The surviving branch (§2) makes one clean, near-parameter-free prediction that the same sharpness which
buys Cassini forces: **a near-null wide-binary EFE, γ_v ≈ 1.000–1.004** (the lock between Q₂ and γ_v is
structural in the full 6-DOF vector solve — `refute_transverse_KB_lock_2026.py`, contingent on measured
α₂/w-c smallness and kpc-scale 1/m_a, per RETRACTIONS.md). Against the **registered Gaia-DR4 Amendment-10
band γ_v ≈ 1.16–1.23**:

> **If DR4 confirms the registered band, FC-AeST+μ_n is falsified. If DR4 is consistent with a null EFE,
> the branch survives this test and earns another round of theory (full AeST cosmology / lensing /
> structure formation / whether a₀²∝ρ_DE can be realized without a new conflict).**

Cassini-safety and a wide-binary signal are the same lever; they cannot both be had. **This is the
experiment that decides whether the surviving relativistic-MOND branch deserves more theory — no further
architecture search changes that.**

---

**One line:** The elegant routes are closed by symmetry (shift-charge ⇒ no evolving-DE in 6 DOF) and by
Cassini (exponential kernel dead); what survives is 6-DOF AeST + sharp μ_n as a real but liability-laden
MOND chassis, with a₀²∝ρ_DE demoted to a phenomenological hypothesis — and the next move is Gaia DR4, not
another Lagrangian.
