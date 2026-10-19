# Independent mixed-shape audit

An independent read-only subagent audited the proposed relation and returned:

\[
\lim_{M\to0^+}
{D_p\over g_0^2D_\chi}={3\pi\over2}
\]
is correct as a restricted leading two-flavour EFT statement, with the charge derivative at zero taken before the mass shape and chiral limit. It is not an exact finite-mass or proven nonperturbative QCD identity.

The auditor independently checked the exact source text at Gorghetto–Villadoro equations (34)–(36), Müller–Meißner equations (2.28)–(2.30), (3.4), (3.9)–(3.10), and the frozen electromagnetic report. It did not read the coordinator's raw mixed-chiral derivation. No files were changed by that reviewer.

## Conditions retained in REPORT.md

- Positive light masses at fixed ratio, strange mass and strong reference theory; ordinary broken-phase SU(2), zero temperature, infinite volume before the chiral limit.
- A canonically normalized e=0 pion mass coordinate and reference susceptibility; Z0 and g0 nonzero; additional hadrons retain nonzero chiral-limit gaps.
- Leading e2 p2 meson local operators give a constant after dividing by chi0. Third-order baryon derivative operators do not generate an on-shell zero-pion mass. No independent chirally analytic local e2 log M or e2 M operator can alter the leading shapes.
- Fixed-scale chiral RG is consistent. Choosing the chiral subtraction scale equal to M requires differentiating the running matching constant. The source's barred fourth-order baryon constants explicitly contain log M and cannot be held fixed in a mass scan.
- Fixed-UV, mass-independent mass conversions alter a constant in the vacuum response and analytic M2 terms in the proton response. Arbitrary IR-dependent mass conversions can change the leading ratio; the report supplies the explicit logarithmic counterexample.
- Replacing the LO denominator by full pure-QCD susceptibility or the mass coordinate by the actual e=0 pion pole mass preserves the limiting value. An arbitrary independent rescaling or charge-dependent pion normalization does not.
- The unexpanded one-loop shapes give a normalized finite-charge ratio sqrt(1+Delta_pi/M2), proving why the prescribed infrared order is essential.

## Improved curvature filters

The reviewer separately checked
\[
L(1-L)(M^2)^n=n(1-n)(M^2)^n,\qquad
(\partial_M-M\partial_M^2)M^p=p(2-p)M^{p-1}.
\]
Both kill constants and analytic M2 terms while preserving the leading loop shapes.
Their actions on M2 log M2 are minus M2 in the vacuum filter and minus 4M in the proton filter. The vacuum double log becomes minus 2M2(log M2+1).

For the standard next-order expansion the generic baryon contamination therefore changes from M log M to M. Unknown constants inside loop-log coefficients remain. Termwise differentiability and regular chiral matching are assumptions; an arbitrary IR-dependent convention can spoil the claimed contamination powers.

## Execution and self-review

The root lane's mixed_response.py independently derives both response shapes from the actual unexpanded pion kernels and checks the relation, its counterterm projections, scale/mass-convention changes and listed limits. Run_001 completed 38 exact checks and manifest validation passed. The reviewer did not rerun it or inspect its implementation; implementation checking belongs to this lane's recorded audit.

Mathematical proofreading self-review covered the new report and derivation. The second-derivative notation in the proton curvature filter is explicit. The distinction between the LO mass parameter, measured e=0 pion pole mass and charge-dependent pion mass is preserved. No objective unresolved notation issue was found. No frozen parent artifact was edited.

Residual limitation: this is a same-program independent derivation and bounded source audit, not an external referee report or a full-QCD all-order proof.
