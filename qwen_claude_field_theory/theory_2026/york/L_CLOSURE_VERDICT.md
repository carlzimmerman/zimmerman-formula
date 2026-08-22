# L-CLOSURE FINAL VERDICT

**Question.** The Helmholtz outer-field filter `(1 - L² D²)Ψ = Φ`, `e = |DΨ|`, with
`L = r_M = √(GM/a0)`, solves the internal/external separation by scale and passes
Cassini / galaxy / dwarf **given L per system**. Is `L = r_M` **derivable from the
action** as a functional of ρ, with no per-system input, keeping the York/CMC 2+0 DOF count?

**Verdict: PRECISE NO-GO.** The EFE separation scale `r_M` **cannot** be a single-valued,
action-determined **local** functional of ρ. It is irreducibly **relational** (it presupposes a
segmentation of ρ into subsystems). The one action-clean alternative — a global mass functional —
is derivable but **fails Cassini by ~3.5×**. This branch is **CLOSED as a scale-derivation**; the
e-screen phenomenology it was meant to underwrite is **untouched and still requires L=r_M as an
external input**.

Footing-independent: verified at both a0 = 9.36e-11 (canonical, ρ_DE/cH_Λ) and 1.20e-10
(ρ_total/cH0). The load-bearing quantities (geometric response S, threshold Σ_M=a0/G) are a0-free.

---

## (1) GLOBAL M[ρ] = ∫ρ d³x — derivable & action-clean, but FAILS Cassini

- Action-clean: a single Lagrange constraint `λ_L(L²a0 − G∫ρ)` promotes L with no per-system label.
- **But** ∫ρ over any box reaching galactic mass is dominated by the Milky Way. `L(R)=√(G M(<R)/a0)`
  is monotone non-decreasing with **no stopping scale** (large-R log-log slope **1.496**, homogeneous
  background predicts 3/2), reaching **L ≈ r_M(MW) ≈ 27–30 kpc**, and already **12.2 kpc by R0=8.2 kpc**.
- Since that L **exceeds** the MW field's own structure scale R0=8.2 kpc, the filter treats the MW's
  external field at the Sun as **internal** and suppresses it by the a0-independent geometric response
  `S(R0/L) = 1 − (1 + R0/L)e^(−R0/L) = 0.037`. So e_SS drops ~1000×, screen amplitude A → 1 (OFF).
- **Q2_global = 1.79e-26 vs Cassini 5.1e-27 → 3.5× VIOLATION at both a0 footings.**
- The only box returning M=M_sun (→ L=r_M(Sun)=7961 AU, S=1.000, Q2 PASS) is the one integrating the
  **Sun alone** — which **is** the internal/external cut the closure was meant to derive (circular).

Script: `york_Lclosure_global_2026.py` (13/13 green, commit a33803dc). **→ NOT_DERIVABLE.**

## (2) LOCAL self-consistent L — resolution-ambiguous & un-selectable; dies on the 3-level counterexample

`L(x)² a0 = G M(<L(x); x)` (mass within radius L of x):

- **Resolution-ambiguous, not merely multi-valued.** At the Sun, roots and their existence swing by
  **×200 in L** (mass ambiguity ×4.15e4) purely from ρ's coarse-graining scale — which the action does
  **not** fix. Resolve the Sun as a point → small root r_M(Sun)=7961 AU (screens); smear it into the
  disk → large root ~kpc (no screen).
- **3-level hierarchy (Sun at the edge of a 2e7 M_sun dwarf orbiting the MW)** restores true
  multi-valuedness: `f(L)=L²a0 − G M(<L of Sun)=0` has **THREE roots** at the same point
  (**7961 AU, 83 pc, 162 pc**). "Smallest root" returns r_M(Sun) at the Sun only by the accident that
  the Sun is the most compact peak — and gives **no** local rule that also delivers MOND-ON at the dwarf.
- The selection that makes the Sun screen (resolve it as a point) **IS** the per-system label the
  closure was meant to remove. `M_sub` is a **segmentation of ρ into objects**, not a pointwise/ball
  field functional.
- Alternatives fail too: tidal `|DΦ|/|D²Φ|` ~ distance-to-source (kpc at the Sun); density `√(a0/Gρ)`
  swings sub-AU ↔ kpc with the averaging scale. Neither returns r_M(subsystem).

Scripts: `york_Lclosure_local_2026.py`, `york_Lclosure_hierarchy_2026.py` (both green, commits
cbae50b3 / 009ba839). **→ NOT_DERIVABLE (single-valued, locally selectable: NO).**

## (3) Dirac / DOF — 2+0 only for the P1-dead global L; LOCAL L breaks it two ways

All 6 filter/scale fields (Φ, e, Ψ, λ_Ψ, λ_L, L) are non-dynamical, so the 12×12 Dirac matrix is
`[[0, −Hᵀ],[H, 0]]`, `det = (det H)²`; the whole DOF question is invertibility of the 6×6 field
Hessian. sympy gives the exact factorization

`det H = σ_Φ · σ_e · (1 + L²k²)² · (2 L a0 − G M_L)²`

— every other L-block entry (Ψ-L, λΨ-L, L-L) **cancels**; only `c = 2La0 − G M_L = f'(L)` matters, and
it enters **squared**, so a zero of c drops rank 12→10, sending (L, P_L) first-class = **+1 scalar DOF**.

- **GLOBAL L:** at a transversal root (Sun-as-point, M_L=0 → c = 2 r_M a0 > 0) full rank → **2+0** at both
  footings — but P1 forces L~30 kpc and Q2=1.79e-26 (physically dead).
- **LOCAL L breaks 2+0 two independent ways:** (a) c=f'(L) is **not sign-definite** — `f'|_root=(2−p)La0`,
  so a tangent double root occurs exactly in the ρ~1/r inner-galaxy regime (surface density > Σ_M=a0/G):
  det H=0 on a codim-1 tangency locus → count jumps to **2+1**; (b) M(<L;x) is a ball integral of
  field-dependent radius with Fourier form factor `F(kL)=4π(sin kL − kL cos kL)/k³`, an entire function
  with infinitely many real zeros (tan kL=kL: 4.4934, 7.7253, 10.9041, …) → **not ghost-free**
  (Tomboulis/Kuz'min); any finite truncation misrepresents the enclosed mass and adds spurious poles.

Script: `york_Lclosure_dirac_2026.py` (15/15 green, commit 37972bde). **→ the DOF count the hierarchy
needs (LOCAL L) is NOT preserved.**

---

## (4) THE VERDICT

**Branch CLOSED as a scale-derivation — a precise NO-GO.**

> The EFE separation scale `r_M = √(GM/a0)` cannot be realized as a single-valued, action-determined
> **local** functional of ρ while keeping the York/CMC 2+0 count and passing Cassini. "External" is
> irreducibly **relational**: it requires segmenting ρ into subsystems (which mass M is "mine"),
> information a pointwise/ball functional of the density does not carry.

What it forbids, exactly:
1. **No local ρ-functional** (∫ρ, ball M(<L;x), tidal ratio, or a0/Gρ) returns r_M(subsystem) at the Sun
   without either (i) failing Cassini for embedded subsystems (global: 3.5×) or (ii) requiring a
   coarse-graining/segmentation choice the action does not fix (local: ×200 L-swing, 3 roots).
2. **No action realization keeps 2+0** except the P1-dead global L; the local L the hierarchy needs
   incurs a tangency rank-drop (2+1) and a nonlocal zero-bearing form factor (not ghost-free).

What could still work (not achieved here, flagged for honesty):
- A **non-local / relational** construction that inputs the subsystem identity from the matter sector's
  own bound-state structure (segmentation as physics, not as a density functional). This is exactly the
  ingredient a local action cannot supply, so it is a genuinely different object, not a repair of this one.
- A **matter-sector** definition of "the object" (e.g. via the baryonic field's own binding) could in
  principle set L per bound system — but that reintroduces per-system content by construction, i.e. it
  concedes the no-go's substance while relocating it.

## (5) What SURVIVES regardless of this NO-GO

- **a0(z) = a0,0 · H(z)/H0** — Z-independent, derived in the York/CMC reduction (unaffected: this run
  is about the spatial scale L, not the temporal a0(z) law).
- **The 2+0 York/CMC skeleton** (tensor sector 2 DOF, H_perp closure) — inherited, not disturbed.
- **G_eff = G** in the relevant (single-potential) branch — untouched.
- **The Helmholtz scale-separation MECHANISM itself** — the low-pass filter provably retains a uniform
  external field 100% (harmonic ⇒ Ψ=Φ exact) and suppresses the system's own field to 26.4% at its MOND
  radius (`1−2/e`). Both machine-verified. The mechanism WORKS; only the **derivation of its scale L**
  from ρ is closed off.
- **The e-screen phenomenology** (SS Q2 < Cassini, isolated galaxy/dwarf unscreened, wide-binary
  Newtonian cost γ_v~1.036) — all intact **given L=r_M per system as an external input**. This run
  did not touch eps_s, which remains FITTED with no independent calibrator.

---

### Ledger
| Route | Derivable? | 2+0? | Cassini? | Verdict |
|---|---|---|---|---|
| GLOBAL ∫ρ | yes, action-clean | yes (transversal root) | **NO (3.5×)** | EXCLUDED (P1) |
| LOCAL M(<L;x) | no (×200 swing, 3 roots) | **no (2+1 tangency + nonlocal)** | n/a | EXCLUDED (P2) |
| tidal / density alt | no (kpc / sub-AU↔kpc) | — | — | EXCLUDED |

Scripts (all green, committed): `york_Lclosure_global_2026.py` (a33803dc),
`york_Lclosure_local_2026.py` (cbae50b3), `york_Lclosure_dirac_2026.py` (37972bde),
`york_Lclosure_hierarchy_2026.py` (009ba839). No new free parameter introduced.
