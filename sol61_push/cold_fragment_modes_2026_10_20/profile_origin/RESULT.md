# Regular origin profiles

Both fixed-charge stationary profiles converged at the unchanged final BVP tolerance `1e-8`. The v2 manifest validates, and all 23 declared checks passed. This supplies finite stationary profile data for subsequent operator calculations; it establishes no stability or formation result.

| Charge | omega | E | Adaptive nodes | Maximum RMS residual |
|---|---:|---:|---:|---:|
| 80000 | 0.9217883882803886 | 76151.17723273078 | 2580 | 9.96130874478141e-9 |
| 160000 | 0.9095170227013512 | 149323.629584538 | 2949 | 9.988801431790158e-9 |

Independent Simpson charge errors are `8.43e-13` and `5.08e-13` relative; the virial residuals are below `1.25e-12`. Energies differ from the prior `r_min=1e-4` finite stationary profiles by less than `1.22e-11` relative. The branch energy difference is `2E(80000)-E(160000)=2978.7248809235753`. Peak measured process RSS was 130285568 bytes; elapsed runner time was below one second. The memory figure is measured RSS, not an enforced address-space limit.

## Origin equation and boundary conditions

State is `y=(f,fp,b,bp,h,hp,q)`, with unknown `omega`. The regular radial equations for each field `z` are `z''+2z'/r=F_z`. SciPy solves `y'=fun+Sy/r` with exactly `S=diag(0,-2,0,-2,0,-2,0)`, at `r=0`. The regular `fun` has no explicit division by `r`. The integrated charge is normalized, so `q'=8 pi omega r^2(f^2+4b^2)/Q_target`.

The eight boundary residuals are `fp(0),bp(0),hp(0),q(0),f(60),b(60),h(60),q(60)-1`. Singular-interface regularity enforces the same three vanishing first derivatives; it does not contradict them. With one unknown frequency, seven states require eight BVP residuals. At the origin the regular equation gives `z''(0)=F_z(0)/3`; the SciPy derivative correction `(I-S)^+` implements precisely this identity. The identity is checked to absolute error below `7e-18`. An independent analytic benchmark `z=1-r^2`, satisfying `z''+2z'/r=-6`, verifies this interface at error `1.12e-16`.

Using regularity at exactly zero removes the artificial Neumann boundary at positive `r_min`. The two previous failed high-accuracy finite-`r_min` records remain unchanged; this experiment does not retroactively mark them successful, and their exact residual failure mechanism is not diagnosed here.

## Data and reconstruction

`run_001/Q80000.npz` and `run_001/Q160000.npz` contain 24001 uniformly spaced points from zero through 60, named `r,f,fp,b,bp,h,hp,q`, along with the stacked `y`, scalar `omega,Q,E`, JSON metadata, adaptive mesh `mesh_x,mesh_y`, and cubic-polynomial coefficients `ppoly_c`. `q` is the cumulative charge divided by the target charge.

The continuous SciPy interpolant can be reconstructed without rerunning:

```python
z = np.load(path)
s = scipy.interpolate.PPoly(z['ppoly_c'], z['mesh_x'])
y = s(r)  # seven state rows; s(r, 1) gives their derivatives
```

Input/output bytes are pinned in `sources_origin.json` and the v2 run manifest. The declared final tolerance, physical coefficients, charge targets, and scope were fixed before execution. No PDE, eigenvalue calculation, merger kernel, dwarf fit, ground-state proof, or nonlinear-stability conclusion is supplied by this profile experiment.
