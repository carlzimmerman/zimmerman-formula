# SV2 iter_2: can the standard khronometric kinetic terms remove the instantaneous mode? FROZEN CRITERIA

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Frozen before any script or number of this lane exists.
Run whatever iter_1 says.

## The class

The standard khronometric terms (Blas-Pujolas-Sibiryakov), added to v3s / AC2q with the action's own normalization
c^4/(16 pi G): alpha (u.grad u)^2 = alpha a^2, beta K_ij K^ij, lambda K^2 (K_ij the extrinsic curvature of the
leaves; for a hypersurface-orthogonal u these are all independent quadratic terms). Weak field, khronon frame, on
AC18's frozen background (v_bg = 0, charge Pi, Hessian K Mt, Mt = (1+x)[I + x e e], K = 4 pi G), a = grad Xi and
K = -lap sigma / c to leading order, K_ij K^ij = (d_i d_j sigma)^2 / c^2, which equals (lap sigma)^2 / c^2 after
integration by parts. So at this order beta and lambda enter only as beta + lambda:

    L2 = P.grad Xi - (gamma/2)(div P)^2 - (K/2) P.Mt.P - (Pi/2)|grad sigma|^2
         + (alpha/(4K)) |grad Xi|^2 - ((beta+lambda) c^2/(4K)) (lap sigma)^2,     Xi = phi - sigma_t.

The alpha normalization is fixed by the known Newtonian limit G_N = G/(1 - alpha/2) (static coefficient of
|grad phi|^2 goes 1 -> 1 - alpha/2); positive alpha adds to the khronon kinetic term. (-Pi/2)|grad sigma|^2 is the
quadratic part of P.grad(|grad sigma|^2/2) on the charged background.

## Derivation (sympy, exact, script sv2_iter2.py)

Euler-Lagrange equations of L2 in Fourier (exp i(k.x - omega t)), phi frozen (homogeneous modes), general symmetric
Mt with e = z. The P equation carries no omega (leaf constraint); eliminate P exactly; obtain the leaf-mode
dispersion omega^2(k). Expected form, to be confirmed or refuted by the script, not assumed:
omega^2 = (Pi + lambda'' k^2) / (1/Z + alpha/(2K)), Z = K f(k_hat) + gamma k^2, f = 1/(k_hat.Mt^-1.k_hat),
lambda'' = (beta+lambda) c^2/(2K). The source-driven chain of AC18 is redone in the same way: the off-source leaf
symbol is S(k) = Z (Pi + lambda'' k^2)/(1 + alpha Z/(2K)) acting on Int (t - t') delta phi_hat.

## Lines

- R1 (instantaneous mode removed?), the decisive line. Necessary condition for a solution kernel supported in a
  finite cone: G_hat(t, k) entire in k (Paley-Wiener-Schwartz). A direction-dependent limit
  omega0^2(k_hat) = lim_{k->0} omega^2(k k_hat) makes G_hat(t, .) discontinuous at k = 0, so the kernel reaches
  outside every ball. Graded: omega0^2(e)/omega0^2(perp) - 1, exact in sympy, and Lean (SV2_repair.lean) that it is
  nonzero for every alpha with no ghost, every beta, lambda, whenever x > 0 and Pi K > 0.
  KEPT if nonzero on the whole healthy region; REMOVED-CANDIDATE at any healthy point where it vanishes (then R2-R5
  are checked there).
- R1b (size of the change, numeric, both footings): the lambda channel of the source-driven chain, the off-source
  part lambda'' K k^2 f(k_hat) of S(k), evaluated with AC18's machinery (k^2 -> -lap on H) at AC18's graded rows,
  reported per unit (beta + lambda) as |dv_lambda| / |dv_AC18|. The alpha channel changes the kernel f -> f/(1 + alpha
  f/2): its relative size at the symbol level is <= alpha f_max / 2, reported at the window edge.
- R2 (finite khronon speed): lim_{k->inf} omega^2/k^2 = c_k^2. Expected (beta+lambda) c^2/alpha (the standard
  result, used as a known answer: the script must reproduce it). Finite iff alpha > 0.
- R3 (no ghost, no gradient instability): kinetic coefficient 1/Z + alpha/(2K) > 0 for all k, and
  Pi + lambda'' k^2 > 0 for all k. Lean: alpha >= 0 and beta + lambda >= 0 suffice; alpha < 0 gives a ghost at large k,
  beta + lambda < 0 a gradient instability at large k (gamma > 0).
- R4 (bounds; LITERATURE formulas, not re-derived here, provisional): c_T^2 = 1/(1 - beta) with GW170817
  -3e-15 < c_T - 1 < 7e-16, so beta in (-6e-15, 1.4e-15); alpha1_PPN = 4(alpha - 2 beta)/(beta - 1) with LLR
  |alpha1| <= 1e-4, so |alpha - 2 beta| <= 2.5e-5; alpha2_PPN is proportional to (alpha - 2 beta) and vanishes on
  that line (its exact bound is not used). Window W = {alpha >= 0, beta in that band, |alpha - 2 beta| <= 2.5e-5,
  beta + lambda >= 0}; c_k <= c in addition needs beta + lambda <= alpha.
- R5 (static galaxy limit): beta and lambda terms vanish on static leaves (v = 0, K_ij = 0): sympy. alpha shifts the
  law mu -> mu - alpha/2 exactly (the term is quadratic in a). With G_N absorbed, the change of g on the balance
  (mu(g/a0) - alpha/2) g = g_N, over g_N/a0 in [1e-3, 1e3], must be <= 0.01 dex at the window edge alpha = 2.5e-5,
  both footings (a0 enters only as a scale; both reported). mu - alpha/2 > 0 is required over that range.

## Label (frozen)

- REPAIRED if one point of W satisfies R1 REMOVED, R2 finite, R3, R5. The coefficients are those the bounds force,
  never chosen to pass R1.
- NO REPAIR IN CLASS if R1 is KEPT on the whole healthy region (alpha >= 0, beta + lambda >= 0), independent of W.
  The window W is stated either way, with c_k and the R1b sizes.

## MUTATE (iter_3) and controls

- Control that lets R1 pass: an isotropic Hessian (x = 0, the KA1 background) must give omega0^2 direction
  independent, i.e. REMOVED-CANDIDATE. If the script cannot return REMOVED there, R1 cannot see a repair.
- Sign-flipped terms: iter_3.

Kappa = 1/2 FITTED; not theory closed.
