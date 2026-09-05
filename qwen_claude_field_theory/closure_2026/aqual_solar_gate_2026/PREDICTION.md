# A concrete orbital prediction from the audited coefficient

This is an additional quantitative prediction, **not a new fundamental law**.
It is a standard quadrupole-mechanics consequence of the exponential AQUAL
coefficient computed in this study. Its empirical comparison is adverse.

Let P be a nearly circular orbital period, n=2*pi/P, I the angle between the
orbit normal and the Galactic external-field axis, and Omega the node longitude
around that axis. At leading order in Q2/n^2 and zero eccentricity,

\[
 \boxed{\dot\Omega=\frac{Q_2 P}{4\pi}\cos I.}
\]

Thus two nearly circular test orbits about the same central source have
dot(Omega_i)/[P_i*cos(I_i)] = dot(Omega_j)/[P_j*cos(I_j)] = Q2/(4*pi),
where denominators are nonzero. This concerns the **anomalous** contribution,
not total observed precession. The node coordinate is undefined at sin(I)=0.

Derivation: vary the signed potential
delta(Phi)=-Q2[(e dot r)^2-r^2/3]/2 to obtain
delta(a)=Q2[(e dot r)e-r/3]. For a circular orbit with unit normal l,
average r_i*r_j=a^2(delta_ij-l_i*l_j)/2 over orbital phase. The resulting
specific torque divided by n*a^2 gives
dot(l)=[Q2/(2*n)](e dot l)(e cross l), and hence the boxed result.
`orbital_prediction.py` independently differentiates the potential and
integrates the torque symbolically; it does not insert the answer.

The fine-grid coefficient Q2=2.097827704e-26 s^-2 predicts

\[
 \dot\Omega\simeq0.034292\,(P/\mathrm{yr})\cos I
 \quad\mathrm{milliarcseconds/century}.
\]

For a circular **Saturn-like** 29.4-year orbit this is 1.0082*cos(I)
milliarcseconds/century. The 29.4-year illustrative period comes from
[NASA's Saturn facts](https://science.nasa.gov/saturn/facts/). This is not a
calculation of Saturn's exact eccentric orbit or an inferred actual inclination.

The published Cassini Q2 mean+2sigma endpoint implies only 0.24990*cos(I)
in that same illustration. This is the **same Cassini constraint expressed
as a precession coefficient**, not independent empirical evidence. The
prediction exceeds that endpoint by a factor 4.03. See
[Park et al.](https://arxiv.org/html/2602.17884v1), equation (6) and Table 1.
No fitted orbital anomaly or new raw-data analysis is being claimed.

Inherits all limitations in REPORT.md, especially the failed strict-tolerance
PDE check. The nonlinear/exact relativistic theory is not closed. The
precession structure itself is not novel; what this run adds is a reproducible
coefficient for the fixed framework and an adverse test. An empirically
successful Kepler-grade discovery has **not** been obtained.

## Reproduce the extension

After generating results.json with audit.py:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/aqual_solar_gate_2026/test_orbital_prediction.py -q
PYTHONDONTWRITEBYTECODE=1 python3 qwen_claude_field_theory/closure_2026/aqual_solar_gate_2026/orbital_prediction.py
```

Both exit 0; three tests check the tidal sign/trace, integrated torque and
zero-response control. They first failed before implementation. The extension
adds these two scripts, orbital_prediction.json, orbital_manifest.json and
this document. All eleven new tests and 32 existing regression tests pass;
the separate 14-case PDE audit still exits 1 on its failed tolerance gate.

Novelty scope: a formal corollary of known quadrupole mechanics. No global
priority claim or assertion of a new fundamental interaction.
