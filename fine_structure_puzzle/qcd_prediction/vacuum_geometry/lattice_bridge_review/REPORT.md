# Yamamoto lattice bridge: bounded primary-source audit

Owner QCD-V; FSP-003 / parent FSP-002. Checked 2026-10-18 America/New_York.

**Verdict: the checked numerical result is inapplicable as a determination of the physical vacuum-stress coefficient (A_\rho).** It is a verified adjacent current-response calculation. This citation supplies no (R=A_\rho/m_p^3\), electromagnetic derivative, or independent value of (c_H).

## Authentication and citation path

[Yamamoto, *Lattice QCD in curved spacetimes*, arXiv:1405.6665v2](https://arxiv.org/abs/1405.6665v2), latest revision 30 September 2014, is the exact five-page source audited. Its banner, official submission history, and journal identity PRD **90**, 054510 agree. The PDF's displayed manuscript date is 1 October 2014. [SOURCES.json](SOURCES.json) pins the temporary PDF/text hashes and all locators; no full paper is copied into this packet.

The requested citation is indirect: [2506.14182v4](https://arxiv.org/abs/2506.14182v4), p.14 ref.[10], cites [1505.05151v2](https://arxiv.org/abs/1505.05151v2); that paper's p.13, Section III.D item 7, invokes Yamamoto, listed on p.16 as ref.[46]. The latter bibliography is unversioned. It does not establish which arXiv revision was read. The audited latest v2 has the cited journal identity. The full v4 bibliography, pp.14–15, contains no direct Yamamoto/1405.6665 entry.

## What the lattice number measures

The background, parameters, observable, and fit are in Yamamoto pp.3–4, Section V, equations (21), (25)–(27) and Figures 1–3:

\[
 ds_E^2=d\tau^2+s(\tau)^2d\mathbf x^2,
 \qquad s(\tau)=e^{H_I\tau},\qquad H_I=iH,
\]
\[
 N_I(\tau)=\int d^3x\sqrt{\det g}\,n_I(x),
 \qquad n_I=-i\langle\bar\psi\gamma^4\psi\rangle.
\]

Here (s\) denotes the paper's scale factor (\alpha(\tau)\); it is unrelated to electromagnetic (\alpha_{\rm em}\). The calculation is quenched, (10^3\times20\), with Wilson parameters (\beta=5.9,\ \kappa=0.154\), periodic space and Dirichlet temporal ends, initial (s=1\), and small (aH_I\). It does not specify a Lorentzian vacuum-state construction.

The source's numerical fit, transcribed in its lattice normalization, is

\[
 \frac{N_I}{L_xL_yL_z}=C_1H_I\left(\frac\tau a+C_2\right),
 \quad n_I=C_1H_I\left(\frac\tau a+C_2\right)s^{-3},
 \quad C_1=0.012\pm0.001,\quad C_2=57\pm8.
\]

The plots use (aN_I/(L_xL_yL_z)\) and (a^4n_I\). No physical-unit conversion is supplied here. These are the paper's fitted current coefficients; this audit performs no fit. Its p.4 paragraph after equation (25) explicitly requires analytic continuation before relating the result to Lorentzian particle production. Sections III–IV and VI leave continuation, scale renormalization, and full-QCD phenomenology open.

## Why this does not close the required arrow

The required numerator is a metric observable, with a fixed physical comparison prescription:

\[
 A_\rho=\lim_{H\to0^+}\frac{\rho_{\rm QCD}(H)-\rho_{\rm QCD}(0)}{H}.
\]

An expectation of a fermion current is a different functional derivative from a metric stress tensor. A calculation of the former supplies no identity determining the latter. Equations (26)–(27) are not a measurement of (T_{\mu\nu}\), vacuum persistence, a production rate, or a subtracted vacuum free energy. Even an eventual justified continuation of this same current would leave the observable mismatch intact. Finite temporal boundaries also require a state-matching argument before interpreting any result as a de Sitter vacuum response.

The 2015 paper's item 7 instead associates particle production with an imaginary stress tensor and uses analyticity to suggest a common linear (H\) correction in the real part. This implication is not established by the cited simulation. Even granting one analytic complex function, analyticity alone cannot equate its real and imaginary leading powers: for real (H\), the entire function (F(H)=ibH+cH^2\), with real nonzero (b,c\), has a linear imaginary part and quadratic real part. This is elementary hand algebra, not a model for QCD. Additional reality, state, and observable identities would have to supply the missing implication. None is provided in the checked citation paragraph.

The full Yamamoto paper contains no renormalized stress insertion, matched (H=0\) vacuum subtraction, continuum/infinite-volume extraction of (A_\rho\), QED variation, or proton correlator/mass matching. Its strong lattice coupling (\beta\), hopping parameter (\kappa\), and scale factor (\alpha(\tau)\) supply no electromagnetic derivative. Thus neither (C_1\) nor (C_2\) can be inserted into (c_H\), (R\), or (dR/d\alpha_{\rm em}\).

## Scope and executable continuation

Authentication, extraction, and the proposed application were checked separately. The current response is **verified as a reported source result**; its use as (A_\rho\) is **inapplicable**. The 2015 suggestion remains **conditional**, requiring a presently absent metric-observable bridge. This bounded check covers the three exact versions and their citation path; it makes no claim about all later curved-background lattice work.

An executable next preparatory step is to derive the renormalized metric insertion and its flat-background subtraction for a specified full-QCD lattice action, boundary state, and fixed-physical-parameter path. A proposed imaginary-(H\) route must establish continuation of that same observable, including the one-sided limit and possible nonanalyticity. The published (C_1\) is useful only as a check of the original current observable under its own setup; it cannot validate the target insertion. Physical (R\) would additionally require matched proton and QED observables. No new simulation is warranted merely by identifying the existing current fit.

[INPUTS.json](INPUTS.json) records the source check and preserved parent-file inventory. No mathematical experiment was executed; only acquisition, extraction, source reading, text searches, and metadata hashing were used. All new files lie in `lattice_bridge_review/`.
