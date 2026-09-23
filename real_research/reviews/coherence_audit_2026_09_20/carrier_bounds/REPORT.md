# What the constructed carrier can and cannot inherit

This is an independent algebraic check of the proposed smooth carrier, made at base `3aaed026d55f65b38733316cb63c432290a339e1` in the shared workspace. It supplies a positive kinetic certificate and a concrete finite-gradient obligation. It is not a full perturbation-action derivation or a stability theorem.

## Positive velocity core

The carrier-action audit reconstructs the cold MOND scalar equation from the six-field source with `xi=0`. In unitary clock gauge and at homogeneous constant MOND scalar, it is algebraic. If healing is included in this candidate, it is explicitly the **intrinsic spatial** operator `(Delta_h phi)^2` used in the corrected September 19 ADM action. Eliminating its perturbation `P` from the spatial block

```text
alpha psi² + 2d psi P - d[beta+xi²(k/a)²]P²
```

gives the effective lapse coefficient

```text
alpha_eff = alpha+d/[beta+xi²(k/a)²].
```

For `d>0`, `0<alpha<2`, `beta=d/(2-alpha)` and `xi²>=0`, this is positive and at most two. It equals two in the zero-healing case. The coefficient two is not the forbidden bare `alpha=2` limit; the original beta remains finite.

This mapping does not apply to the different projected spacetime-Hessian operator squared in the L291 builder. On FRW that operator linearizes to `a^-2 Delta P-3H Pdot` even when the background MOND scalar is constant. At nonzero `H xi`, its square supplies a temporal derivative and the scalar cannot be eliminated by the displayed algebraic rule. The two choices agree for this purpose when `xi=0`. The independent review identified this distinction before final interpretation.

Use the ADM kinetic geometry already derived in the September 19 review, `c13=0`, and `b=c2>0`. Before solving the shift, its velocity terms are

```text
-3r(v+H psi)² - 2r(v+H psi)sigma - b sigma²
+ Kchi(u-C psi)² + alpha_eff(k/a)² psi²,
r=3b+2, Kchi=p_X+2X p_XX, C=sqrt(X).
```

Here `v=Phi_dot`, `u=delta_chi_dot`, and `sigma` is the shift divergence. Terms linear in velocities and involving field positions do not change this Hessian. The shift gives the positive-square core

```text
L_velocity = A(v+H psi)²+B(u-C psi)²+E psi²,
A=2(3b+2)/b>0, B=Kchi>0, E=alpha_eff(k/a)²>0.
```

Eliminate `psi` and set `D=A H²+B C²+E`. The resulting velocity Hessian is

```text
K11=2A(B C²+E)/D,
K12=2ABHC/D,
K22=2B(A H²+E)/D,
det K=4ABE/D>0.
```

`check_bounds.py` independently obtains this Hessian by differentiation. `KineticSchur.lean` certifies the determinant, positive principal minors, and strict positivity for every nonzero real velocity pair. The action-to-core mapping remains a separately stated variational obligation: it combines the prior ADM geometry, the reconstructed cold scalar constraint, and the carrier kinetic coefficient. This review does not rederive all lower-order field equations or their physical transfer functions. In particular `k=0`, `b=0` and vanishing kinetic coefficient are excluded, and positivity need not be uniform near those limits.

## Finite gradients impose another condition

The candidate is

```text
y=Y/Yd, z=log(X/X0),
m=1+(Ac-1)/[2(1+y²)^(1/4)],
p=rho0 [exp(mz)-1]/(2m), Ac>1.
```

It has `p_Y(X,0)=0` for every `X>0`. That homogeneous cancellation does not imply positivity of the scalar spatial block at nonzero `Y`.

For a fixed clock, the scalar sector `-J(Y)+p(X,Y)` needs the longitudinal spatial-energy coefficient

```text
J_Y+2Y J_YY - [p_Y+2Y p_YY]
```

to be positive. This is only one necessary principal-block test; it is not sufficient for the full coupled system. Direct differentiation gives

```text
p_y+2y p_yy = p_m(m_y+2y m_yy)+2y p_mm(m_y)²,
m_y+2y m_yy = (Ac-1)y(2y²-3)/[4(1+y²)^(9/4)].
```

For `z>0`, both `p_m` and `p_mm` are positive: equivalently they are the first and second `m` derivatives of `(rho0/2) integral_0^z exp(m t) dt`. Thus the carrier opposes the old longitudinal scalar stiffness when `y>sqrt(3/2)`.

An exact local example uses `Ac=9`, `Yd=rho0=1`, `y=sqrt(15)`, and `X/X0=exp(1/3)`, so `m=3`. It gives

```text
p_Y = -sqrt(15)/288,
p_Y+2Y p_YY = sqrt(15)(7+10e)/4608 = 0.02873035719... > 0.
```

The transverse sign is helpful, while the longitudinal term must be bounded against the actual `J` sector. This is not a global halo, and the example does not show that the full candidate is unstable. It prevents an unjustified inference from homogeneous decoupling and positive carrier kinetic energy to universal nonlinear health.

There is a stronger analytic restriction. Fix any finite `Y>0`. Then `m_Y` is nonzero, and as `z=log(X/X0)` grows, the leading term is `p_Y+2Yp_YY ~ rho0 Y m_Y² exp(mz) z²/m`, which diverges positively. Hence an X-independent `J(Y)` with finite longitudinal stiffness cannot keep this fixed-clock spatial block positive over the entire unbounded domain `X>0`. A viable use requires a justified physical X range, additional X-dependent structure, or another constitutive choice. This is a restricted principal-block result, not a claim about a realized halo or a full coupled dynamical mode.

The next test is therefore specific: retain the exchange and anisotropic stresses, determine the accessible `X,Y` range from a self-consistent solution, and verify the complete principal matrix there. The construction is useful because its conserved cosmological background and its first decoupling requirement are explicit; the finite-gradient problem remains live.

## Reproducibility

`check_bounds.py` runs thirteen exact symbolic checks. `KineticSchur.lean` contains four real-algebra certificates. `verify.py` runs both; the bounded run's contract and manifest record sources, toolchain, outputs and limits. The source action and all existing research files remain unchanged.
