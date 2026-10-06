# Verification checkpoint

Authoritative main_a passes 13 checks. The upper-shell parity control fails its three complex-Mellin comparisons, as intended. Both manifests are retained and validate. Symbolic checks verify the beta-coefficient reduction, four reflection/parity identities, removable moment value, endpoint leading orders and trigonometric factorization. Numerical comparisons use three frequencies on Re(s)=1/2, 65 digits and explicit q cutoffs [1e-6,1e6]; they are bounded corroboration, not a universal analytic certificate.

The first development quadrature formed q=1-v² before dividing by sqrt(1-q). Extremely small v rounded q to one and caused a zero division. The final implementation cancels that square root algebraically in the transformed integrand, retaining the exact finite shell limit. No approximate shell replacement or tail shortcut is used. The unused direct-weight helper was removed before execution inputs were frozen.

The independent review reconstructs the finite-part continuation and weighted-L1 injectivity proof. No kernel or astronomical source was fitted, and no claim of C=32pi follows from the checks.
