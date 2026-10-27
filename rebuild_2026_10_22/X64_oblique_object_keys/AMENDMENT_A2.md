# Post-result amendment A2: a consistent same-radius C6R proxy

Authorized 2026-10-27 after the independent closure audit. Original frozen
criteria, ledger, script and results remain historical. This amendment changes
the C6 physical definition and regrades it explicitly; it is not a pre-result
choice and supplies no additional exclusion significance.

The old C6 divided a Newtonian potential evaluated at a catalogue measurement
radius by a circular-speed reference at a different radius. It fails its stated
point-mass invariant. For extended sources, `sqrt(G M_catalog/a0)` also need not
be the radius where the actual enclosed baryonic acceleration equals a0.

The corrected candidate C6R is a **Newtonian baryonic binding-speed to law
circular-speed proxy at one common reference radius**:

    r* = sqrt(G M_catalog/a0)
    g_b* = G M_b(<r*) / r*^2
    C6R = sqrt(2 |Phi_N,b(r*)| / [nu(g_b*/a0) g_b* r*]).

Both potential and force use the same adopted baryonic mass profile. This is
not escape speed in the full isolated-law potential, and r* is not called an
actual transition radius for extended sources. For a point mass it is exactly
`sqrt(2/nu(1))`, independent of any catalogue measurement radius.

The source-profile conventions remain explicit:

- Pressure-supported systems: the existing Plummer model, total catalogue mass
  and scale `3*r_catalogue/4`, with enclosed mass and potential evaluated at r*.
- SPARC, UMa, MW disc, TDGs, groups: the existing point-mass approximation.
- Clusters: X19's beta=2/3 baryon profile, core radius 0.15 R500, normalized to
  1.2 Mgas500 inside R500 and truncated at 3 Mpc. Its mass inside r* and the
  exterior-shell potential integral are both retained. `M_catalog=1.2 Mgas500`
  defines r*; it is not relabelled as the mass inside the 3 Mpc boundary.
- KiDS: compact stars+cold gas plus the existing uniform hot-gas sphere of
  radius 100 kpc. Its actual enclosed hot mass enters the circular force.

No halo or host potential is added. The host-potential variant is not regraded,
because an environment-free potential cannot silently be converted into a
specified host geometry. The C6R P/G/W labels, strict intervals, and single lens
radius variant are regraded. Seven other candidate intervals are inherited
unchanged from the original JSON. The eight-candidate primary null-relabelling
enumeration is recomputed. Its frequency is not statistical power.

The read-only member reconstruction must reproduce historical C6 class
intervals and counts before any new result is accepted. The corrected
definition also has point-mass, Plummer, uniform-sphere and truncated-beta
potential/force checks. Separate artifacts and their commands are under
`closure_program_2026_10_27/gate_fixes/`. This remains a finite family of eight
scalar keys tested with one threshold; arbitrary object-property keys and
retarded/nonlocal history are not excluded. Kappa remains fitted.
