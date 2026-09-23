# The cluster exclusion does not follow from L293

**Verdict: refuted for its stated hydrostatic solution; incomplete for the carrier's physical viability.** L293's slope and density formulas fail the equation it intends to solve. Correcting those formulas does not validate the carrier: the resulting tracer atmosphere becomes enormously self-gravitating, and the declared fluid equation of state was not derived from the L290 action.

Base: `3aaed026d55f65b38733316cb63c432290a339e1`, shared dirty workspace. All changes are new review artifacts. This calculation uses the source parameters only as an internal consistency test, without importing an external cosmological model or new observational data.

## Exact equation and solution

First audit the explicitly stated surrogate. Let `P=rho*C(r)`, `g=v²/r` and `P'=-rho*g`. Here `C` has dimensions of speed squared; it is being assumed to equal `P/rho`, independently of any perturbative sound-speed calculation. The product rule gives

```text
d log(rho)/d log(r) = -v²/C - r C'/C.
```

L293 line 32 instead uses `-v²/C + r C'/C`. For its decreasing `C(r)`, that error makes the reported slope more negative.

Write `h=AD/r_M`, `eta=v²/c²`, and `C=c²/(1+h*r)`. With the *single* boundary condition `rho(R)=rho_R`, the correct solution is

```text
rho(r)/rho_R = (1+h*r)/(1+h*R) * (R/r)^eta * exp[eta*h*(R-r)].
```

The symbolic check substitutes this expression into the differential equation and obtains exactly zero; a separately stepped DOP853 integration agrees in log density to below `10^-12` on the tested interval. The four Lean theorems certify the algebraic slope implication, sign difference, amplitude freedom, and distinction between an affine and isothermal equation of state. They do not formalize the action variation or the numerical integration.

L293 lines 46 and 58 reverse the inward integral's sign. Its implemented density consequently does not solve hydrostatic balance. In addition, its mass integral resets `rho(1.4 Mpc)` to the cosmic mean instead of transporting the stated boundary at `5 Mpc`. Finally, its `delta_needed` formula uses `0.32*Mb` although the prose says the target is `2.2*Mb`. These are independent issues, not numerical tolerance effects.

For the exact same surrogate parameters:

| Diagnostic | Result |
| --- | --- |
| Original-formula mean slope, 75–420 kpc | −4.30047 |
| Correct mean slope over that band | −2.30049 |
| Correct local slopes at 75, 200, 420 kpc | −0.2360, −2.2960, −5.9215 |
| `rho(1.4 Mpc)/rho(5 Mpc)` | `1.63150e25` |
| Mass in 30–1400 kpc, divided by baryon mass | `2.20127e28` |

The huge last two values diagnose a failure of the prescribed tracer potential and boundary assumptions. They are **not** a physical halo prediction: such a mass cannot consistently be evolved in the fixed baryon-only potential used to compute it. The lower radius is 30 kpc; the computation makes no claim about the omitted central mass.

There is a further domain issue. The point-source parameters give `r_M=481.988 kpc`, so the assumed `g_N/a0` runs from about `41.30` at 75 kpc to `1.317` at 420 kpc. This inner band is not in the deep-MOND limit of the source's own point-mass field. An actual enclosed baryon profile and interpolation law must replace that approximation before a cluster comparison.

## An overlooked result already in the repository

`fable_independent_2026/L41_cluster_specification.py:815` had already examined the interpretation of the fitted slope. A genuinely cored profile

```text
rho(r) = rho0 / [1+(r/200 kpc)^2]^(3.5/2)
```

has a fitted log slope `-1.57342` over 40–750 kpc under that source's sampling and fitting rule. The independent reproduction here recovers that number. Thus a measured or inferred finite-band slope near −1.5 is not by itself a requirement for a singular central cusp. L293 also changes the fitted radial range. The old data reductions were not re-audited here; this is a mathematical counterexample to equating a finite-band fit with an asymptotic core classification.

## The constructive reframing: solve the inverse pressure problem

For a specified positive target density, force, and outer pressure, the hydrostatic pressure is determined by

```text
P(r) = P(R) + integral_r^R rho(s) g(s) ds.
```

If `rho=K*r^(-gamma)` and `g=v²/r`, this gives exactly

```text
C(r) = P(r)/rho(r)
     = v²/gamma + [C_R-v²/gamma]*(r/R)^gamma.
```

Consequently a density slope does not generally imply a constant sound speed. The isothermal relation `C=v²/gamma` is the special boundary choice `C_R=v²/gamma`. Mass normalization is another input: at fixed shape and force, hydrostatic balance is homogeneous in the density amplitude. A mass cap inferred with one cosmic boundary prescription cannot be promoted to an amplitude-independent shape theorem. `Hydrostatic.lean` records that precise algebraic freedom; it does not assume that formation dynamics can realize any chosen boundary.

The useful next step for the actual carrier is stronger still: obtain its energy density, radial and tangential pressures, conserved current, and exchange force from the same `p(X,Y)` action, then solve those equations with gravitational backreaction. The companion carrier-action review supplies that dictionary. For the L290 Taylor jet, `p=0` at `X=C²` while `rho>0` and the characteristic speed squared is positive. Therefore `p=rho*c_s²` cannot describe that state. Away from it, the `Y` interaction also contributes anisotropic stress and exchange. Replacing L293's sign alone is insufficient.

This reopens the question that L293 purported to close, but does not settle it in the carrier's favor. The surviving exact result is the corrected hydrostatic theorem and the action-to-pressure obligation.

## Reproduction

`check_cluster.py` checks eight exact identities, a separate log-density IVP, quadrature, the regime ratios, and the previously recorded core-fit example. `Hydrostatic.lean` contains four algebraic theorems. `verify.py` executes both in the existing Lean host. `contract.json` specifies the limited claim; `run/manifest.json` pins source, code and result hashes. No original research source is modified.
