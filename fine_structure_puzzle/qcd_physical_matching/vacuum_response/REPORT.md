# Physical vacuum route: a topology-conditioned stress test

FSP-006, parent FSP-005; checked 2026-10-19. **The full physical QCD/QED coefficient A_rho remains unevaluated.** This route obtains a new exact mixed observable and an explicit fixed-topology diagnostic that test its theta-dependent part. It does not repeat the conditional flat-gap argument or infer stress from a contact susceptibility.

Let t=log a, H=a^-1, V=Omega4 a^4, D=H partial_H. Define Tcal=partial_t S to include the regulated metric/measure/matching response and I=partial_(e^2)S to include the complete canonical current insertion. At theta=0, for an integrated metric-independent integer Q,

    rho_theta_theta=-Cov(Q^2,Tcal)/(4V)
                   =(1-D/4)chi,
    partial_(e^2)rho_theta_theta
      =[kappa(Q^2,I,Tcal)-Cov(Q^2,I_t)]/(4V).

These finite-regulator identities specify the missing mixed correlator and its metric contact term. Flat chi and its Q^2JJ derivative do not evaluate them. The actual EM vacuum stress instead uses [<I_t>-Cov(I,Tcal)]/(4V), without Q^2 probes. Full renormalized limits and the matched parameter path remain necessary.

The new practical quantity uses sector-conditioned integrated trace measurements. Under a large-chi V Fourier saddle with bounded higher theta cumulants and a uniformly differentiable remainder along S4,

    X_top(H)={8V[rho_Q=0-rho_theta=0]-4}/H
            =-Dlog chi/H+O(H^3).

If chi(H)=chi0+a_chi H+O(H^2 log H), chi0>0, then

    lim X_top=-a_chi/chi0,
    partial_theta^2 A_rho|0=-(3chi0/4) lim X_top.

At fixed nonzero chi the constraint alone gives rho_Q-rho=H^4/(2Omega4)+O(H^8). A theta-dependent linear-H susceptibility appears as an H^5 correction to that known baseline. This is a calculable, falsifiable stress difference with its normalization and leading artifact fixed; it has not been measured here. It tests a proposed mechanism predicting theta dependence, and cannot exclude a theta-independent A_rho. No uniform-sphere remainder follows merely from a flat hadronic gap.

There is an exact information obstruction. Multiplying every topological sector by the same metric functional leaves normalized sector probabilities, every theta cumulant, and Z(theta)/Z(0) unchanged. Thus these data cannot recover a theta-independent geometric vacuum term. This is an underdetermination of topology data, not freedom to add a nonlocal counterterm to a fixed microscopic theory. The latter theory still has to calculate or exclude the common factor. The earlier compact three-form model already exposed this issue in a model; the present derivation identifies its exact QCD mixed-observable consequence and a topology-conditioned lattice test.

The primary-source checks establish the scope of actual evidence:

- [AFHO, 0707.0396v2](https://arxiv.org/abs/0707.0396v2) derives the fixed-Q saddle after choosing Z(0)=1. Its source result supplies the constraint correction, and discards the common vacuum normalization. Its application along S4 needs the stated saddle/derivative control.
- [Gorghetto–Villadoro, 1812.01008v2](https://arxiv.org/abs/1812.01008v2) supplies the flat chiral Q^2JJ coefficient already used by the prior EM lane. It supplies neither the radius derivative nor the mixed trace contact. No new chiral numerical prediction is claimed.
- [Kotov–Lombardo–Trunin, 2502.15407v2](https://arxiv.org/abs/2502.15407v2) reports recent actual thermal QCD topology and normalized sector reconstruction. Its physical pion/mass tuning and f_pi scale calibration are inputs. It does not measure the S4 response or its theta-independent factor.
- [Makino–Suzuki, 1403.4772v5](https://arxiv.org/abs/1403.4772v5), equations (2.11),(4.73), explicitly uses a vacuum-subtracted EMT and separated insertions. Integrated Tqq or TqqJJ needs its own contact completion; its flat formula cannot silently be used as the full curved metric response.
- The recent-looking CERN holonomy/magnetic-field source is [Zhitnitsky, 1902.07737v2](https://arxiv.org/abs/1902.07737v2), published in 2019. It still leaves the strong-QCD coefficient for lattice computation. Its crawl date is not a new calculation.

The exact derivation, anomalous/axial Ward interpretation, finite-H qualifications and next measurement are in DERIVATION.md. SOURCES.json pins primary versions, hashes, locators, extraction/application verdicts and calibration limits. INPUTS.json pins the frozen project inputs. Full sources remain temporary; no prior artifact, shared navigation or Git state was modified.

The bounded run run_001 completed **37 exact rational checks** and its v2 manifest validates. It verifies finite-ensemble differentiation against direct normalized Taylor coefficients, the metric contact sign, trace-identity cancellation, Gaussian fixed-sector derivatives at four stated H fixtures, and the source's change between quark-mass and pion-mass variables. The ensemble and rational coefficients are algebra fixtures, not QCD data. No measured alpha, cosmological value, physical mass, LEC number or susceptibility was inserted.

The cheapest useful continuation is a common-regulator QCD sphere measurement of joint Q and the action-derived integrated trace, checked against radius differences of chi before extrapolating. Then measure X_top with higher-cumulant/derivative errors. The corresponding order-e^2 test additionally measures I_t and the connected three-variable cumulant above. The unconditioned stress remains necessary for A_rho(theta=0), and therefore R=A_rho/m_p^3 and a predictive alpha remain open. This package has a self-audit and mathematical proofreading pass; the parent coordinator independently checked the mixed identities and saddle signs, while no independent review of the completed files is claimed here.
