# Correction to frozen derivation, before new-author exposure

The immutable FROZEN_DERIVATION.md has an algebraic misstatement in Section 3
for the off-constraint scalar difference. Subtracting the displayed u,w rows
actually gives

  2b(g_t-p_x)+2H_chi h=2H_chi h,
  hence g_t-p_x=0,

without using chi_x=k. The frozen line g_t-p_x=H_chi(chi_x-k) is incorrect
away from compatibility. The sum is correctly given there:

  p_t-b^2 g_x=F+b H_chi(chi_x-k).

The construction proves chi_x=k first, so both the mistaken frozen expression
and the correct expression reduce to the same required zero for the constructed
solution. The proved scoped conclusion is unchanged, but the off-constraint
identity must not be reused. This failed algebraic intermediate is preserved
explicitly and is not silently edited out of the frozen source. The diagonal
source terms themselves and the iteration estimates are unchanged.

Detected by direct addition/subtraction during pre-author self-review; no new
author or stage34 proof had been read when this correction was written.
