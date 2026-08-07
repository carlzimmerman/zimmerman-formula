# M08 — The b-projector, at the cost of third derivatives
COST: M | KILLS FAST: no | script: `mi_b_projector_2026.py`

## The task
The last named escape from the 2026-08-01 no-goes: a projector built from the **binormal** b of the
worldline's Frenet frame, which evades the (v/c)² suppression at the price of third derivatives.

## Do
1. Build the Frenet frame (t, n, b) for the exact circular dS worldline. The corpus has closed forms:
   κ₁ = R(w²+H²)/√(1−H²R²), κ₂ = hw/H, κ₃ = 0 — verify them.
2. Construct the projector onto b, write the MI law with it, and compute the in-phase gain at galactic
   frequencies. Does it evade the (v/c)²?
3. Then count the cost: **Ostrogradsky**. Third derivatives generically give a ghost. Is this one degenerate
   (constrained) or genuinely unbounded? Compute the kinetic matrix eigenvalues.

## Settles if / refuted if
CONFIRMS: unsuppressed gain with a degenerate (ghost-free) structure ⇒ a live covariant route.
CLOSES: an unremovable Ostrogradsky ghost ⇒ the 2026-08-01 no-goes become complete for the form class.

## Known walls
κ₃ = 0 exactly for this worldline, so the frame is effectively 3-dimensional — check what that does to the
projector before assuming it is nontrivial.
