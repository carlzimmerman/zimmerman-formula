# L84 affine-dust BBN gate

This is a deliberately narrow closure gate for the affine `F(Q)Theta` dust
reading examined in the latest Fable commits.  The same conserved charge that
creates the pressureless (a^{-3}) term creates a negative (a^{-6}) term.
With (Omega_{dust,0}=33/125) and the fiducial BBN limit
(Omega_{stiff,0}le 42/10^{26}), exact arithmetic gives

\[
  \frac{\Omega_{stiff,0}}{\Omega_{dust,0}}=\frac{r}{2},
  \qquad r=\frac{|C|}{|A|},
  \qquad r\le \frac{350}{11\,10^{25}}≈3.18\times10^{-24}.
\]

Thus an integer number `q` of (10^{-24}) charge-ratio units obeys
`q <= 3`; the natural `r=1` branch is excluded by more than twenty orders of
magnitude.  This is a route-specific fine-tuning result, not a no-go theorem
for the nonlocal clock construction or for all relativistic MOND actions.

Run the executable gate:

```sh
python3 -B L84_stiff_bbn_gate.py
```

Run the dependency-light Lean companion:

```sh
python3 -B run_lean_core.py
```

The Lean file follows the Navier--Stokes project’s useful discipline—small
definitions, explicit declarations, zero `sorry`, and a machine-checkable
compiler result—but intentionally uses only Lean’s core omega arithmetic so
the proof is not hidden behind a large dependency cache.

