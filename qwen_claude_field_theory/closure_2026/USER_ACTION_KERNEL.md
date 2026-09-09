# Conditional exponential physical-force calibration

In the xi=0 leading static planar/aligned reduction, with zero scalar flux,
write g=Phi'>0, s=phi'>0, a=1/(4 pi G)-2(c1+c4), b=2-K_B. The integrated
metric and scalar equations are a*g-2b*s=source flux and J'(s^2)*s=g.
Let A denote the desired high-acceleration inverse coupling 1/(4 pi G_N).
Impose source flux=A*mu(g/a0)*g. Direct solution gives the parametric input

s(y)=a0*y*[a-A+A exp(-y)]/(2b),
J(s(y)^2)=a0^2/b*[(a-A)y^2/2+A((y^2+y+1)exp(-y)-1)],
y=g/a0.

The script derives J by integrating 2g ds and verifies both equations
symbolically. Its asymptotic J' is 2b/(a-A), so the effective inverse
coupling a-2b/J'_infinity is A. This identifies how the desired measured
normalization differs from the bare G; it does not derive its observed value.

For b>0 the map is globally strictly monotone under
a/A > max_y [mu+y mu']=1+exp(-2).
The maximum and its location y=2 are computed. This is the same type of
regular scalar-map condition already encountered in earlier bridge work,
not a claimed new physical law or literature novelty.

Numerical inversion at 61 logarithmically spaced y in [1e-5,50], using
(a,A,b,a0)=(1.2,1,1,1), gives maximum relative force error 1.57e-15.
The negative control a=1.1 yields ds/dy=-0.0176676 at y=2, detecting a fold.

Scope: xi=0, regular positive aligned fields, leading weak-field reduction
and no-slip boundary data. No arbitrary-source three-dimensional AQUAL,
nonzero-xi equivalence, full metric-slip cancellation, or dynamical mode
removal is proved. The earlier illustrative branch used a different J input
and cannot be relabeled as calibrated. A new branch calculation is required.

Next: insert this parametric J into the curved equations with declared xi,
and quantify the physical departure from the unscreened force law while
deriving both metric potentials. The full-theory requirements remain intact.

Command: `python3 qwen_claude_field_theory/closure_2026/user_action_kernel_calibration.py`
Exit 0. Output is printed reproducibly; symbolic identities and a folding
negative control are executable. Mathbox computation-audit scope applies.
