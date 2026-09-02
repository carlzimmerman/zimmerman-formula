# Generalized-aether PPN gate — VERDICT: KILL, and it GENERALIZES (2026-09-01)

**Question (gate 4 of the fried-chicken spec): AeST fixes its aether sector to Maxwell-only
(c1=-c3=K_B, c2=c4=0). Restoring the two omitted Einstein-aether couplings — c2 (∇·A)^2 and
c4 a_μa^μ, both tensor-blind so c_T=1 survives — can they open a healthy preferred-frame PPN-null
locus (α1=α2=0) once the AeST scalar drag 2(2-K_B) a·∇φ is included?**

**Answer: NO. The full Einstein-aether + shift-scalar completion fails preferred-frame PPN on the
ENTIRE ghost-free locus — not just at AeST's Maxwell point. Restoring c2, c4 does not save it.**
Scripts (all re-run by hand 2026-09-01, exit 0, checks that can fail + mutation controls):
`generalized_aest_2026/gen_aest_alpha1_c2c4.py` (anchor A: reproduces the banked c2=c4=0 kill on 5
grid points, γ=1, α3=0), `gen_aest_locus_numeric.py` (the α1=0 locus), `gen_aest_dispersion_health.py`
(spin-2/spin-1 spectrum), `verify_closedform.py`, `verify_noghost_signflip.py`.

## The closed form (SOLID — verified symbolically against a 4×3 (K_B,J_Y) grid; c2=c4=0 anchor exact)

    α1 = -4 c14 - 4 (2 - K_B)/(J_Y + 1),      c14 ≡ K_B + c4  (the spin-1 kinetic coefficient)

- First term −4c14: the pure Einstein-aether contribution. In the frozen-scalar limit J_Y→∞ it is the
  whole thing, reproducing Foster–Jacobson α1 = −4c14 on the c13=0 (c_T=1) plane.
- Second term −4(2−K_B)/(J_Y+1): the AeST SCALAR-DRAG contribution. It is **c14-independent and
  strictly negative** for K_B<2. It is present at the physical deep field J_Y = μ(u0) = 1.
- **c2 does not enter α1 at all** (the (∇·A)^2 operator is longitudinal; α1 is transverse) — confirmed.

## Why it kills, and cannot be tuned out (the mechanism — this is the publishable part)

α1 = 0 requires  **c14 = −(2−K_B)/(J_Y+1) < 0**  for every 0<K_B<2 and every J_Y≥1
(at J_Y=1: c14* = (K_B−2)/2 ≈ −0.9). But the spin-1 (vector) kinetic coefficient is
**2·c14·B** with B = 2Q0²(J_Y+1)(K_B−2) − k² < 0, so it is ∝ c14 and flips sign as c14 crosses 0.
AeST (c4=0, c14=K_B>0) is the ghost-free reference (published v9 no-ghost theorem, stage 22);
the α1=0 locus (c14<0) carries the OPPOSITE-sign spin-1 kinetic term — a **ghost** (sign flip
verified numerically: healthy point −0.429, α1=0 locus +1.930, opposite).

**So: zeroing the preferred-frame PPN parameter α1 costs a spin-1 ghost. The two aether kinetic
couplings can move c14 but cannot remove the drag's −4(2−K_B)/(J_Y+1); c2 is transverse-blind.**

**The drag coefficient (2−K_B) is EXACTLY the AeST scalar–aether coupling 2(2−K_B) J^μ∇_μφ that
GENERATES the MOND behaviour.** The very term that makes the theory MOND is the term that forces
α1 ≠ 0 on the ghost-free locus. This is a genuine no-go with a one-line reason:

> In an Einstein-aether relativistic MOND theory with c_T = c (GW170817 ⇒ c13 = 0), the scalar–aether
> coupling required to produce MOND contributes an irreducible, aether-kinetic-independent negative
> term to the preferred-frame PPN parameter α1; α1 can be driven to zero only by sending the vector
> kinetic coefficient c14 = K_B + c4 negative, i.e. by introducing a spin-1 ghost. There is no
> ghost-free, c_T=c, α1=0 point in the class.

## Scope and honesty
- SOLID within the standing cosmological-background + inert-J_Y=1 linearization (the same
  solar-profile-background residual named in V9_PPN_KILL_VERDICT.md remains the one un-run upgrade to
  "final"; it would have to flip a certified O(1) coefficient by O(1), not a small correction).
- Gate 2 (α2): moot once α1 kills, but α2's novel channel (v9) is unchanged by c2, c4 (also transverse
  bookkeeping), so it independently fails too.
- c_T = 1 EXACT with c2, c4 on (spin-2 check passed) — GW170817 is not the obstruction; the drag is.
- This does not touch Layer A (a0 = ½c√(Gρ_Λ), a0∝H(z)). It closes the aether-embedding PPN gate for
  the whole Einstein-aether class, generalizing the AeST-specific v9 kill.

## What it means for the fried-chicken program
Combined with the local no-go theorem (FRIED_CHICKEN_VERDICT_2026-09-01.md), the aether/preferred-frame
carrier — the one carrier class that survives the single-metric-scalar no-gos — is now closed by a
mechanism, not case-by-case. The surviving relativistic option is MOND-with-a-dark-field (the universal
shift-charge), or the nonlocal door. The a0 reframing survives; a Lorentz-invariant, ghost-free,
2-tensor-DOF field-theory embedding of exact-MOND-plus-lensing does not exist in the local aether class.
