# SCALE-SPLIT DOOR — two-auxiliary localization of the nonlocal F₊ kernel
**Status: SPECTRAL LEVEL SOLVED (PASS-CONDITIONAL). The door is OPEN at the quadratic level, with an
explicit healthy structure — and one unavoidable cost, and one decisive confrontation still ahead.**
Script: `two_auxiliary_spectral_theorem.py` (all sympy-exact).

## Theorem A (dichotomy — why DC-011 was inevitable)
For ANY 2-field localization L = ½χ̇ᵀAχ̇ − ½χᵀMχ + χᵀcS with kernel readout dᵀχ, demanding the static
response R(k²)=dᵀ(Ak²+M)⁻¹c equal 1/k² EXACTLY forces **det(M)=0**: the k⁰ matching condition IS
−det(M). One massless mode always. Corollary: gap it and R(0) goes finite ⇒ Yukawa/contact ⇒ kernel
dead. **The massless pole IS the Coulomb kernel — they are the same object.** A fully-gapped auxiliary
sector is impossible; the only question was ever whether the SECOND mode can be gapped independently.

## Theorem B (the scale-split point exists, ghost-free)
Explicit solution: **A = 𝟙 (no ghost), M = m² diag(0,1) (no tachyon), c=(1,0), d=(1,d_B)** ⇒
R(k²)=1/k² exactly at every k, verified against the full general conditions. The second auxiliary is
gapped at m with 1/m < 1 kpc — frozen on every observable band — with ZERO effect on the kernel,
because the source couples only to the massless direction. **DC-011 evaded: the gap operator and the
kernel operator are different field-space directions.** P7 does not bite: the kinetic matrix is fixed
(𝟙), independent of the screening — the e^{−y} lives in the VERTEX c(y), not in A.

## The unavoidable cost (Thm A): one massless radiative scalar
χ_A propagates (ω=ck). Its static exchange is MOND; its radiation is new physics. Mitigations that
make this plausibly survivable: the vertex runs with 2F₊′=e^{−y} (binary-pulsar and solar-system
source regions are high-y ⇒ radiative coupling exponentially screened), and it is NOT a
preferred-frame carrier ⇒ no α₁/α₂ bill at all. Quantitative pulsar-flux gate still to be computed.

## THE DECISIVE OPEN GATE: the pincer confrontation
The localized theory is **local, ≤2-derivative, single-metric, frameless**. DC-001 (108k exhaustive)
says such a theory CANNOT produce correct MOND lensing without an unremovable preferred frame. So
exactly one of three things is true, and computing which is the next knife:
1. The lensing-carrying embedding of (χ_A, χ_B) into the gravity sector lies INSIDE the pincer's
   scanned basis ⇒ lensing will fail in a specific, computable way (Φ≠Ψ or under-lensing) — door closes.
2. The 2-auxiliary structure lies OUTSIDE the 108k basis (the scan's carrier/coupling grammar must be
   re-checked against this specific readout structure) ⇒ compute lensing directly from the embedding.
3. The embedding only works by smuggling a frame ⇒ back to the closed khronometric family.
Also still open for the full theory: c_T on FRW (DW-type nonlocal terms famously dress the tensor
kinetic term away from Minkowski), Cassini time-domain response, and the Dirac count of the full
coupled system. NONE of these are computed yet — the PASS above is strictly spectral.
