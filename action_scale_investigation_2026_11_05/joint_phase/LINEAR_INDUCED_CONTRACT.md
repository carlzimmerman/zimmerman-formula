# Linear induced-coupling discriminator

Base: b3268c9114af471b41e313961f92d85e3150b93f. Owner: this chat; writes
only in action_scale_investigation_2026_11_05. Freeze before executable
checks. No coefficient scan or campaign candidate registration.

Changed construction, in c=hbar=1 units:

    r=sqrt(sigma^2+p^2), F=D r,
    U=U0+C_A r^3/3+C_B p^3/3,
    L=F R/2-Z(grad sigma)^2/2-U.

D,C_A,C_B,Z,U0>0, sigma>0, p>=0. D,C_A,C_B have mass dimension one,
Z dimension zero. Matter is minimally coupled in the Jordan frame.
The quadratic detuning is set to zero as an explicit critical-surface
assumption, NOT selected by the preceding source RG. No bare Einstein
term or sequestering constraint is imported. The p-sector covariant
kinetic/clock action and its microscopic spectrum remain unconstructed.

Question: does a linear, rather than quadratic, condensate-dependent
Planck coefficient cancel the condensate scale in the joint ratio, and
can scalar exchange then be neglected? Calculate homogeneous stationarity,
positive vacuum, Einstein-frame kinetic/mass and matter scalar charge;
fixed-curvature elimination of sigma; the held-background tensor ratio;
and the scalar Compton-to-Hubble hierarchy. Keep all coefficients symbolic.

Success of this discriminator means a mathematically consistent scaling
cancellation plus an explicit account of the local calibration obstacle.
It is not achievement of the user goal. Goal achievement still requires
microscopic coefficient selection, protected criticality, the operational
force law, positive physical vacuum and the full constraint/health audit.

Exact SymPy identities, single-thread, 60-second cap, no numerical scans.
Negative control: omit the conformal scalar-metric kinetic contribution;
the kinetic, canonical mass and scalar-charge checks must detect it.
Store separate runner manifests and results; distinguish symbolic
identities from full-model predictions. Next decision depends on whether
a sub-Hubble region can suppress this scalar by its mass alone.
