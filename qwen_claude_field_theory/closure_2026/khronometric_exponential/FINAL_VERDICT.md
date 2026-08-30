# KM-X1 — FINAL VERDICT (asymptotic endpoint gate)

## Question
Can μ(y)=1−e^{−y} live inside a **finite-coupling** generalized-khronometric theory (α_∞>0, β=0,
λ finite) without trading Solar-System PPN success for strong coupling?

## Result: the finite-α_∞ endpoint is CONDITIONALLY CLOSED by GW170817 (outcome C, severe narrowing)
Deterministic, symbolic (`gw170817_collapse.py`, sympy — all checks residual-exact):

1. **The Bonetti–Barausse escape is the surface α=2β.** Both α₁ and α₂ carry the factor (α−2β), so
   on α=2β they vanish *identically* — with α_∞=2β_∞ **finite** ⇒ finite khronon kinetic term ⇒ no
   strong coupling. This reproduces their 2015 viable finite-coupling endpoint. ✔ verified symbolically.

2. **c_T=1 ⇒ β=0** (exact solve of 1/(1−β)=1). GW170817 forces this to |β|≲10⁻¹⁵.

3. **β=0 collapses the escape surface α=2β to α=0.** On the c_T=1 slice α₁=4α — a function of α
   **alone**; ∂α₁/∂λ=0, so there is **no third-parameter freedom to keep α₁ small at finite α.**

4. **Solar-System preferred-frame bounds then force α_∞ → tiny:** |α₁|<10⁻⁴ ⇒ α<2.5e-5;
   |α₂|<10⁻⁷ ⇒ **α_∞ < 2e-7** (binding). α_2 leading term = α/2, λ-independent.

5. **That is the Bonetti–Barausse strong-coupling wall.** K_s ∝ α → 0 and c_s² ∝ 1/α → ∞ as α→0;
   on the escape surface itself c_s²=(β+λ)/(β(β+3λ+2)) diverges as β→0. GW170817 pushes the endpoint
   from a finite healthy surface into the exact α→0 pathology the paper identified.

**Net:** GW170817 shrinks the finite-α_∞ khronometric-MOND window from a finite viable *surface* to a
fine-tuned *sliver* α_∞ ≲ 2×10⁻⁷ pressed against the strong-coupling wall. The clean structural reason:
**post-GW, the ONE coupling that must stay finite to avoid strong coupling (α) is the SAME coupling the
preferred-frame bound drives to zero — and λ cannot separate them.** This is our P7 collision
re-expressed through the c_T=1 door.

## Honest scope — what is and isn't settled
- SETTLED (symbolic, decisive): the *asymptotic* (high-a = Solar-System) endpoint. The finite-coupling
  freedom BB2015 relied on is a β≠0 effect; c_T=1 removes it. This is STEP 6/7's make-or-break and it
  is adverse.
- NOT YET DONE (needs the reconstructed acceleration-dependent f(a) action, Carl's STEP 7 in full):
  whether acceleration-dependent corrections to α₁ at Solar-System accelerations could *cancel* the
  4α_∞ term (the one door that could reopen this). Standard "local-background" reduction says no, but
  proving it needs the full 1PN of the acceleration-dependent action.
- NOT YET DONE (quantitative): whether the sliver α_∞≲2e-7 is *truly* dead or merely fine-tuned —
  the actual M_sc(α_∞, a_0) vs Solar-System energies. Setup in `gw170817_collapse.py` §5; needs M_ae.

## Do-not-overclaim
This is NOT "khronometric MOND is dead." It is: **the finite-α_∞ escape that motivated this branch is
closed to a fine-tuned sliver by a constraint postdating Bonetti–Barausse; the remaining sliver + the
acceleration-dependent α₁-cancellation door are the only two ways it lives.** μ(y)=1−e^{−y} was never
the problem — the chassis's preferred-frame/tensor structure is, exactly as the pincer predicted.
