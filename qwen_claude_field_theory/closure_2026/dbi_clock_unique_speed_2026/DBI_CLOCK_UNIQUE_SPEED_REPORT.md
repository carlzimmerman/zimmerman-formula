# DBI clock unique-speed theorem

## Result

`DBIClockUniqueSpeed.lean` is a kernel-checked Lean proof of the following
homogeneous-branch statement.  For every `A,L,C,a > 0`, there is exactly one
`z` with `0 < z < 1` satisfying

\[
  \frac{z^3}{1-z^2}
  = L\left(\frac{C}{A a^3}\right)^2 .
\]

This is the algebraic form of the conserved shift current used by the
evolving DBI clock minisuperspace gate.  It establishes an admissible clock
speed for every positive scale factor, rather than only at sampled values of
`a`.

## Proof structure

1. `charge_shape_strictMono_on` proves strict monotonicity on `(0,1)` by
   cross multiplication.  The exact numerator factorization is

   \[
   y^3(1-x^2)-x^3(1-y^2)
   =(y-x)(x^2+xy+y^2-x^2y^2),
   \]

   whose factors are positive for `0 < x < y < 1`.
2. `charge_shape_exists` applies the intermediate-value theorem to
   `P_q(z)=z^3+qz^2-q`, using `P_q(0)<0<P_q(1)`, then excludes the two
   endpoints and converts `P_q(z)=0` to `chargeShape z=q`.
3. `charge_shape_unique_positive_root` combines existence and strict
   monotonicity.
4. `dbi_clock_unique_speed` proves the physical right-hand side is positive
   from `A,L,C,a > 0` and applies the previous theorem.

## Reproduction

From this directory:

```text
python3 -B run_lean.py
python3 -B -m unittest -v test_dbi_clock_unique_speed.py
```

The runner records the source hash and Lean exit status in
`run_001/lean_result.json`.

## Scope and nonclaims

This result is a theorem about the homogeneous DBI clock current.  It does
not establish the full covariant metric variation, the nonlinear Dirac/HDA
constraint algebra, two tensor-only gravitational degrees of freedom, PPN
parameters, or inhomogeneous perturbative stability.  In particular, it does
not close the relativistic MOND theory by itself.
