# W4-02: independent fixed-vacuum portal and response audit

Date: 2026-10-20. Base checkpoint: `177591c05a384bc07c819e3fe0d5517aa8798cb4`.
This file is frozen before this lane creates or runs a script. Other working-tree
changes belong to other work. Owner: the coordinating independent attempt;
delegates are read-only and do not append the shared register.

## Target and interpretation

Explain the coefficient in `a0 = kappa c sqrt(G rho_DE)`, with
`epsilon = rho_DE c^2`. A solution must independently select `kappa = 1/2`
and supply an independent consequence of that selection. Otherwise report the
strongest exact obstruction with its scope. Do not claim a no-go for unknown
physics. `kappa = 1/2` remains FITTED. The inherited measurement is CFG493:
`kappa_Lambda = 0.417 +/- 0.095`, `kappa_crit = 0.345 +/- 0.078`; these footings
are never pooled and neither measurement enters a derivation.

Read authorities: `../README.md`,
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md`,
`KAPPA_DOORS.md`, `KAPPA_ATTEMPTS_LEDGER.md`,
`campaign_fresh_gravity/CFG911_kappa_constructive_coupling/README.md`, and
`FRAMEWORK_EQUATIONS_2026-10-15.md` (paths relative to repository root except
the first). Do not duplicate the reserved p63 or KAPPA_LOGIC work.

## Routes and discriminators

R1: symmetry and protected normalization. Test whether ordinary internal
symmetries, field redefinitions, duality, or a criticality condition fix the
relative normalization of a physical acceleration and a vacuum stress. A
surviving candidate must specify its operators, all couplings, vacuum
prescription, dimensional extension, and second prediction. An invariant
vacuum counterterm or a freely variable observable coupling is a closure of
that particular selection mechanism, not all possible symmetries.

R2: constitutive response. Derive the principal symbol of a single Lorentz
invariant scalar with a cubic static gradient energy. Check whether its
characteristic cone selects a normalization, gives only an inequality, or
fails the specified condition that its cone lie inside the matter light cone.
A wider cone alone will not be called a proof of acausality. If relevant,
verify a primary DBI screening proposal and explicitly retain its matter
coupling and any free identification of its screening radius with the MOND
radius. No inferred equality from a screening inequality.

R3: fix the background vacuum first, then test the remaining freedom. For
spatial dimension n >= 2 let `K_n = Omega_(n-1) G_n`, where G_n is defined by
the Newtonian force law. For every `xi > 0`, consider the explicit portal

    a_xi(epsilon)^2 = xi G_n epsilon,
    W_xi(u; epsilon) = a_xi^2/K_n F(u/a_xi),
    F(t) = -t - log(1-t) - t^2/2,     0 <= t < 1.

This is a family testing nonselection, not a proposed derivation of xi. In
three spatial dimensions its local field action is the framework's square
term plus W and the same nonnegative stiffness coefficient. The decisive
checks are: W(0) = d_epsilon W(0) = 0, convexity, and elimination of the
polarization in the algebraic spherical limit. These distinguish an
independent multiplicative portal freedom from merely adding a cosmological
constant. Retain the existing law-form split: this construction tests the
simple-mu member, not the exact quadratic law. Give a separate scaling
argument if discussing the quadratic member.

## Option spaces, dimensions, and bookkeeping

R1 is `free` until a named principle fixes every normalization. R2 is `free`
or `closure`; its continuous couplings are not sampled. R3 has the exact
continuous space `xi in (0,infinity)`, with no probability weights or numeric
scan: `kappa^2 = xi` is a TRADE, not a hit. All density-portal expressions
are pi-even (pi weight zero after cancellation of K_n) and hbar-free.
H-only comparisons, if any, must declare the permitted coefficient field;
do not invoke an unrestricted pi-parity theorem for arbitrary functions.
`[G_n epsilon] = L^2 T^-4` in every n, so the portal's units do not pick n=3.

## Checks and failure conditions

Check the exact W derivatives, zero-background stress/source, two Hessian
eigenvalues on 0 < u < a, force-law elimination, G/rho/c scaling, and
invariance of `a_xi^2/(G_n epsilon)` under the Gauss normalization. Inspect
the script for forbidden upstream measured inputs. Record script and input
hashes and software versions. No fitted constants, scans, or target-derived
units are allowed. A scalar-cone statement must specify its background and
metric convention. Static convexity is not full dynamical stability or a
complete cosmological model.

## Mutation controls, declared before execution

M1: multiply F by `b != 1`, keeping the physical acceleration scale a fixed.
Expected: the constitutive relation becomes
`g = u + b u^2/(a-u)`. It must fail the original simple-mu force-law identity,
while W(0)=0 and convexity for b>0 remain true. This checks a load-bearing
normalization rather than mutating the answer.

M2: in the single Lorentz scalar, replace static power p=3 by p=2.
Expected: the squared longitudinal characteristic speed changes from
`p-1 = 2` to `1` in units of the matter light speed. The check for the cubic
cone must fail. The prefactor remains absent from the speed ratio.

M3: n=3 -> n=4. Expected: K_n changes from `4 pi G_n` to `2 pi^2 G_n`;
`a_xi^2/(G_n epsilon)` remains xi. A fake dimension selector must not appear.
Controls have separate `_MUTATE` outputs and a nonzero exit when they bite.

## Second consequence and endpoint

The density portal gives `a0(z)/a0(0)=sqrt(epsilon(z)/epsilon(0))` for constant
xi and G. This is independently testable but common to every xi: it cannot
promote a free xi to a selection. No significance is assigned to these
nonselection routes. Any exact candidate needs a fresh proof audit before
reporting. With no candidate, preserve the proofs, exact missing implication,
and the actual untried continuation rather than claiming theory closure.

Outputs: a bounded exact symbolic checker and separate control outputs, a
source/route report, independent review, and one append-only register row per
scoped route after reconciliation. No downloads or heavy computation.
