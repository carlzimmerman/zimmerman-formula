# Explicit cuscuton-F(Q)Theta candidate: no-slip gate

The current proposed repair replaces the quadratic `K(Q)` by a cuscuton
square root.  The candidate tested here is

\[
 S=\int\sqrt{-g}\left[\frac{M^2}{2}R-\Lambda M^2
 +\sigma\sqrt{Q^2-Y}+fQ\Theta
 +M^2a_0^2G(\sqrt{Y}/a_0)\right]+S_m[g,\psi],
\]

with `G'(y)/(2y)=1-exp(-y)` and `Q=n·dφ`, `Y=q^{μν}d_μφ d_νφ`.

On a weak-field constant-gradient patch, direct variation with respect to the
spatial inverse metric gives the traceless coefficient

\[
 C_{TF}(y)=M^2(1-e^{-y})-
 \frac{\sigma}{2\sqrt{Q_0^2-a_0^2y^2}} .
\]

The requirement `Phi=Psi` for every finite acceleration requires this vanish
throughout the branch.  At `y=0`, it forces `sigma=0`; after that,

\[
 C_{TF}(y)=M^2(1-e^{-y})>0\qquad(y>0),
\]

so the candidate cannot retain both the exact exponential MOND term and exact
no slip.  The Lean theorem proves the contradiction under the displayed
positive-branch hypotheses; the Python script derives the coefficient and
checks the exact kernel, constitutive stiffness, cuscuton Hessian, and
homogeneous tensor-speed ratio.

This is a candidate-level obstruction, not a universal no-go. An escape must
add a genuinely new covariant stress compensator (or a nonlocal metric
operator) and then redo the complete Dirac, Ward, PPN, FLRW, tensor-speed,
causality, and stability analysis from that enlarged action.

## Reproduction

```sh
python3 -B qwen_claude_field_theory/closure_2026/cuscuton_fqtheta_candidate_2026/cuscuton_fqtheta_gate.py
python3 -B qwen_claude_field_theory/closure_2026/cuscuton_fqtheta_candidate_2026/run_lean_cuscuton_slip.py
```
