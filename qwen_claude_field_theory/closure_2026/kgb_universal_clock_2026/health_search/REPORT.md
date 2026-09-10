# Independent matched-seed health and next-preservation audit

Three initial two-halo matches are independently reproduced at 80 decimal
digits. Each admits one shared curvature \(j=F_{XX}=10^{10}\) with both local
vacuum EF principal diagnostics healthy and the coupled EF Einstein/current
equations satisfied. **None of these three matched points passes the next
common-action preservation gate.** This is a pointwise obstruction, not a
universal exclusion or a CMB result.

Only new `health_search/` files are written. Frozen `health/`, old source
files, index and Git history remain untouched. Computation-audit determines
the provenance and failure criteria; proof-audit distinguishes the exact
conditional implication from floating root evidence; proofread-math covers
the new equations and scope. No external theorem or empirical novelty is
asserted.

## What was actually changed and run

The initial assignment was to widen the signed common-\(F_X\) search. Its
exploratory `signed_search.py` evaluator was implemented and tested against
the original varied inverse for both signs of \(F_X\), including large
negative \(w=F_X X'\). Its parametrization
\(w=-2F\eta/r\), \(0<\eta<1\), ensures
\(D_{\rm coord}=1-\eta>0\). **No broad multistart search was executed.**
The parent task found actual matches and redirected this task before that run.

`matched_seed_audit.py` uses the parent's double-precision matches only as
initial guesses. It solves all five equations for
\((f,w_1,y_2,U_2/\epsilon_2,w_2)\), using real `mp.diff` differentiation,
not the parent's pressure/preservation-eliminated determinant or complex-step
derivatives. The five equations equate \(P,P_X,G_X,P_{XX},G_{XX}\).
The root is not interval-enclosed, so arbitrary-precision agreement is strong
numerical evidence, not an exact existence theorem.

All trials use one shared \(F=.525\), \(X=.5\),
\(\epsilon_1=10^{-6}\), \(\epsilon_2=2\times10^{-6}\), \(y_1=.1\), and
one global constant \(a_0\) used as units. Within each pair, \(f=F_X\) and
\(j=F_{XX}\) are shared. The three different \(u_1=U_1/\epsilon_1\) values
are different candidate seeds, not three additional halos claimed to share
the same action. There are no dark-matter particles; the clock is explicit.

## Exact next-gate interpretation

Let \(\kappa=P_X/f\), \(\gamma=G_X/f\), and let \(\mathcal D=d/dX\)
be the actual static flow, with \(w=fX'\). On the regular chart,

\[
 \mathcal D(y,X,U,w,F,f)=
 \left(\frac{f}{r_yw},1,-2-\frac{2fg(2X+U)}w,
 \frac{fW}w,f,j\right),\qquad W=dw/dr.
\]

The normalized inverse supplies \(\kappa,\gamma,W\) independently of
\(f,j\). Write \(E_\kappa=\mathcal D\kappa\) and
\(E_\gamma=\mathcal D\gamma\). Then

\[
 P_{XX}=j\kappa+fE_\kappa,\qquad
 G_{XX}=j\gamma+fE_\gamma.
\]

At a matched point, \(\Delta\kappa=\Delta\gamma=
\Delta E_\kappa=\Delta E_\gamma=0\), where \(\Delta\) is halo 1 minus
halo 2. Differentiating once more gives

\[
 \begin{pmatrix}\Delta P_{XXX}\\\Delta G_{XXX}\end{pmatrix}
 =f\begin{pmatrix}\Delta\mathcal DE_\kappa\\
 \Delta\mathcal DE_\gamma\end{pmatrix}
 =f(N+jB).
\]

Any common \(F_{XXX}\) contribution multiplies an already matched lower
jet and cancels here; it cannot repair this pointwise discrepancy.
`matched_seed_audit.py` differentiates the full flow directly at \(j=0\)
and \(j=1\) to obtain \(N\) and \(B\), rather than importing the parent's
values. A necessary next tangency is \(N+jB=0\). With \(B_\kappa\ne0\),
the first component fixes \(j_\kappa=-N_\kappa/B_\kappa\); the second is
then an actual remaining residual, not another freely fitted control.

## Three independently refined measurements

The table rounds only for readability; full values and jets are in the result.

| \(u_1\) | Shared \(f\) | Open common local-health interval for \(j\) | Necessary \(j_\kappa\) | Remaining \(\gamma\) drift |
|---|---:|---:|---:|---:|
| .03 | 259.685368559567 | \((1.5511398850\times10^9,3.0405125844\times10^{14})\) | \(-1.4583318107\times10^9\) | \(-9.8091132777\times10^{13}\) |
| .128 | 235.452268636833 | \((3.6482627757\times10^8,5.3138308124\times10^{13})\) | \(-1.0685166911\times10^9\) | \(-3.8490232976\times10^{13}\) |
| .5 | 175.637512132227 | \((6.6432395831\times10^7,5.6530709001\times10^{12})\) | \(-4.1732986152\times10^8\) | \(-1.0312064398\times10^{13}\) |

The normalized determinants \(\det(N,B)/(\|N\|\|B\|)\) are respectively
\(-.000538829413840944\), \(-.000262477518649397\), and
\(-.000135746899087186\). Their nonzero values persist at higher precision.
Both actual halo principal checks fail at each negative \(j_\kappa\).
Thus the next preservation requirement is not merely outside the selected
healthy witness: its first necessary component is outside the entire common
healthy interval, and its second component is inconsistent even without the
health requirement.

For comparison, at the one shared value \(j=10^{10}\), all six actual halo
checks have \(K>0,R<0,T<0\) and positive strict null-cone margin. Across the
three pairs:

- initial five-jet relative mismatch is below \(6.3\times10^{-71}\);
- five-jet mismatch after changing the **shared** curvature is below
  \(1.6\times10^{-71}\), using the total-derived curvatures above;
- coupled EF Einstein-stress residual is below \(5.9\times10^{-79}\);
- total mapped EF current residual is below \(7.0\times10^{-81}\).

These are same-action, on-shell **point** checks. Choosing a healthy curvature
does not grant permission to ignore the subsequent preservation equation.

## Independent finite perturbation of the original raw curvatures

As a separate check of the next derivative, the script evaluates the original
`universal_seed.raw_jet`, which calls the varied 3-by-3 inverse and its total
action curvatures. It perturbs each halo along its actual \(X\)-flow, keeping
one common \(j=j_\kappa\) constant and using
\(F(X\pm h)=F\pm fh+jh^2/2\), \(f(X\pm h)=f\pm jh\).
No projection back onto the matched surface is applied. The central
derivative of the two raw curvature differences, divided by the common \(f\),
approaches \(N+j_\kappa B\).

Six steps from \(10^{-9}\) to \(3\times10^{-12}\) are recorded. The best
relative errors in the nonzero \(\gamma\) residual are approximately
\(3.2\times10^{-8}\), \(5.1\times10^{-9}\), and \(2.6\times10^{-9}\).
The \(\kappa\) component is cancellation-limited in the original floating
code; its scaled error is also recorded and is not presented as an exact zero.
The finite differences independently confirm the large remaining mismatch.

## Map and physical limitations

At all three seeds \(F>0\), \(X>0\), \(U_i>0\), \(B_i>0\), and
\(D_{{\rm coord},i}>.9996\). The derivative-conformal field Jacobian
\(\Delta=2(F-Xf)=1.05-f\) is negative but nonzero. Either sign is locally
invertible; rejecting these seeds only because \(\Delta<0\) would be an error.
This does not prove a global extension avoids \(\Delta=0\), or that mapped
matter/fluid perturbations remain healthy.

The coupled EF vacuum principal is evaluated through the previously tested
general dictionary, at its original scalar-tensor principal and stress. There
is no assigned rank, PPN coefficient, separate acceleration scale, cosmological
likelihood, or complete physical-frame Hamiltonian certificate. Ordinary
matter is minimally coupled in the physical action; none is inserted as
minimally coupled EF dust. Source calibration, boundary data, other matching
roots, continuously varying seed parameters, and CMB evolution remain outside
this three-seed checkpoint.

## Reproduction and evidence

From the repository root:

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health_search/test_signed_search.py
python3 -B qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health_search/matched_seed_audit.py
```

Five focused tests cover six fast-versus-original jet controls, both signs of
\(f\), five coordinate-chart samples, an equal-mass zero-residual control,
the high-precision actual seed, all three next-preservation obstructions and
the finite-raw-derivative checks. Tests use 70 digits; the recorded three-seed
audit uses 80 digits. `run_matched_audit.py` runs both and writes the bounded
record in `run_001/`. Its manifest records actual argv, source hashes,
environment, exit status, resource limits and results. The exploratory broad
search remains unexecuted and is not counted as evidence.
