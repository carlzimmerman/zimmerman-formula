# PG06 protected-gravity continuation contract

Owner: `/root/protected_completion`; base checkpoint
`a5617b4742892d38b77382fd67540fba365b2993`. Write scope is this directory
only. TP01–TP05, queues and Git state are not mutated. Current files, rather
than an assumed unchanged HEAD, are pinned by each numerical manifest.

Target: test the actual proposal

    K=-n M^2 log Y, n=3-epsilon, epsilon=1e-4,
    Y=H-K_micro/(n M^2),
    H=tau+taubar+b(tau+taubar-1)^4+c(tau-taubar)^4,
    b=c=1e8, W=W_SU5+W0, constant tree gauge kinetic function.

First discriminator: independently invert the complex metric. Then solve
the finite-CW/leading-gravity vacuum and inspect the uneaten neutral
fermion and its actual matter-current projection. A heavier gravitino does
not establish photino stability. Conversely, an open decay is not itself
an age-bound failure; its coupling and width must be computed.

The two conclusions sought are distinct: a local Einstein-frame particle
embedding with a tuned tiny net residual, and a dynamically selected raw
F-energy/DE link. W0 tuning can at most establish the former. Nothing here
derives the V3 khronon action, rho_DE, kappa or the stiffness ratio.

Accuracy is declared per run. The starting cheap solve uses the exact
tree SUGRA potential plus the complete rigid one-loop CW potential on the
collective valley. This is not a finite one-loop SUGRA matching or a
transverse quantum effective action. A loop-stationary scalar background
cannot be paired with an off-shell tree Goldstino matrix and called a pole.
The rigid Ward self-energy required by the CW force must be retained.

Canonical orthonormal neutral coordinates, for h=lambda=e, are

    T=(X+sqrt(30) B_D)/sqrt(31),
    N=(sqrt(30) X-B_D)/sqrt(31), Q=A_D,
    W=mu^2 T/sqrt(31)+sqrt(30/31) mu^2 N
      +(e/2)sqrt(31/30) N Q^2+W0,
    Q=i mu sqrt[60/(31 e)], N=0 on the rigid valley.

Here A_D and B_D multiply D/sqrt(30). This gives canonical matter metric
before the logarithm and avoids importing the unrelated Shih model.

Success requires stationarity, K-positive domain, neutral physical scalar
and fermion masses, current projection and explicit remaining matching
errors. Failure closes only the stated construction. The minimal next
route must address its measured obstruction, without unconstrained added
sectors. Exact n=3 with tiny raw F and a new modulus gauge-mass source is
a different model and is not silently substituted.

Computations: installed mathbox 4.0.0 v2 runner, fresh output directory,
one numerical thread, <=240 s wall each, CPU cap, measured RSS. On macOS
do not request unsupported affinity or RLIMIT_AS. No packages installed.
Controls include n=3/Q_H=0, complex direct inversion, precision repeat,
Goldstino Ward/null checks, canonical normalization, phase directions,
and dimensional scaling. Approximation errors remain explicit.
