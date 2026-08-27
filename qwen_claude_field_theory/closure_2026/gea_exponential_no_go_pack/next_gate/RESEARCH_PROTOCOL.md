# Research Protocol for the Two-Function Search

## Principle

The new architecture only earns consideration if it actually separates the constitutive MOND response from the vector stability data at the level of the quadratic action.

## Required symbolic workflow

1. Define conventions and signature.
2. Write the full covariant action.
3. Derive the background equations.
4. Choose the Minkowski + weak-static background and impose the unit-timelike constraint consistently.
5. Derive the nonrelativistic field equation.
6. Recover the exponential \(\mu(y)\) exactly.
7. Expand the same action to second order around Minkowski.
8. Decompose perturbations into spin-2, spin-1, and spin-0 sectors.
9. Compute the kinetic and gradient matrices.
10. Diagonalize or otherwise obtain the physical eigenvalues.
11. Check whether the MOND function and its derivatives enter each physical eigenvalue.
12. Search the allowed parameter region analytically before using numerics.
13. Test the singular/strong-coupling boundaries.
14. Test PPN, GW, and Cherenkov constraints.
15. Only then test black-hole backgrounds.

## Required anti-self-deception checks

- Derive the same vector speed in two independent ways.
- Verify that field redefinitions do not hide a ghost.
- Check dimensions in every term.
- Repeat the quadratic expansion after eliminating nondynamical variables.
- Test both sign conventions for the action and explicitly map them.
- Distinguish phase speed from kinetic positivity.
- Treat \(c_{13}=0\) as a limiting case only after deriving the exact expression at finite \(c_{13}\).
- Keep track of the measured Newton constant rather than silently identifying bare and measured couplings.

## Required negative result format

If the candidate fails, record:

```text
FAILURE GATE:
ACTION:
ASSUMPTIONS:
EXACT EQUATION:
SIGN/INEQUALITY:
WHY PATCHES CANNOT REPAIR IT WITHOUT CHANGING THE ARCHITECTURE:
```

The purpose is to accumulate rigorous closures rather than continuously rename failed constructions.
