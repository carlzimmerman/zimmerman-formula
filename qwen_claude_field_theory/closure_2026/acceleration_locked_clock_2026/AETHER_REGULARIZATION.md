# ALC aether-regularization gate

The acceleration-locked action has a useful static branch, but its covariant
preferred-frame corner is formally (c_1=c_2=c_3=0,;c_4\ne0).  That is
exactly where the usual Einstein--aether PPN expressions lose denominators.
This gate asks whether adding a small, explicit constant-aether completion can
repair the PPN/GW sector without adding a gravitational scalar.

For nonzero (c_1), solve the standard PPN equations directly:

\[
c_4=-c_3^2/c_1,
\qquad
c_2=\frac{-2c_1^2-c_1c_3+c_3^2}{3c_1}.
\]

Writing (c_3=r c_1) and (c_1=\epsilon) gives the exact identities

\[
c_{13}=\epsilon(r+1),\quad
c_{14}=\epsilon(1-r^2),\quad
c_{123}=\epsilon(r+1)^2/3.
\]

The regular principal-symbol speeds used by the executable gate are

\[
s_0^2=\frac{c_{123}(2-c_{14})}
 {c_{14}(1-c_{13})(2+c_{13}+3c_2)},\quad
s_1^2=\frac{2c_1-c_1^2+c_3^2}{2c_{14}(1-c_{13})},\quad
s_2^2=\frac1{1-c_{13}}.
\]

These formulas make the architectural split explicit:

* On the exact PPN-tuned branch with nonzero (epsilon), the equation
  (c_{13}=0) has the unique solution (r=-1).  Substitution then gives
  (c_{14}=c_{123}=0), and (s_0^2	o0) when approached from the regular
  (r>-1) side.  Thus exact tensor luminality is the scalar-degenerate
  surface, not an ordinary regular point.
* There are regular points with exact algebraic (alpha_1=alpha_2=0),
  (|c_{13}|\ll1), and positive/superluminal principal speeds.
* At every such regular point (c_{14}c_{123}\ne0), so the scalar aether
  principal symbol is nonzero.  It is an additional gravitational scalar in a
  covariant aether completion, not the explicitly counted clock matter mode.
* Killing that scalar by taking (c_{14}=0) or (c_{123}=0) moves to a
  degenerate branch.  The PPN and speed expressions are then singular and do
  not certify (alpha_i=0); a full lapse/shift/clock Dirac chain is required.

The script `alc_aether_regularization.py` derives the branch, scans a
deterministic ((\epsilon,r)) grid, separates regular from degenerate points,
and writes `run_001/aether_regularization.json`.  It therefore turns the
preferred-frame problem into a falsifiable gate rather than assigning PPN
values by hand.  The result is **OPEN**: the regular branch repairs the PPN
corner only by reintroducing an extra gravitational mode, while the degenerate
branch remains an explicit unresolved calculation.
