# L317 — the registered tSZ test, scored under its original rules

`L317_tsz_original_window_score.py` (4/4; `MUTATE=1` replaces the measured pressure with the framework's own phantom-zone prediction, and the "window missed" findings fail, rc=1).

**Registration.** The test was registered in G129 and `TSZ_PROPOSAL.md` §5 (commit fe4ea03a3, 2026-09-16 00:30). The statistic is the log-slope of the Compton-y profile over [θ500, 2θ500]:

- **PASS:** sample median in (−1.7, −0.9). This is the phantom zone isothermal at 2 T_floor, which gives y ~ b^−(q−1).
- **F1:** a slope steeper than −2.0 at ≥ 3σ.

G177 rewrote the window to (−2.94, −2.14) nine hours later, before any map was read.

**Data.** Ghirardini et al. 2019, A&A 621, A41: the XMM + Planck-SZ pressure of the same 12 X-COP clusters, out to about 2.5 R500. The numbers are taken from the paper's Tables 2–3.

| Channel | Measured | Against the registration |
|---|---|---|
| Compton slope from the X-COP GNFW, Monte-Carlo over the published errors | −2.48 ± 0.33 (best fit −2.50; Arnaud+10 −2.78; Planck+13 −2.43) | **2.4σ outside the pass window**; beyond F1 at 1.5σ |
| Piecewise 3D pressure slope over 1.29–2.65 R500 | −3.21 ± 0.40, which projects to a y-slope of −2.21 ± 0.40 | 1.3σ outside the window |
| Temperature slope over 0.88–1.90 R500 | −0.31 ± 0.11 | 2.8σ against the predicted isotherm |

**Score under the original rules:** not passed, and not formally killed, because F1 needed 3σ. The rewritten window contains the data because it is the ordinary universal-pressure-profile band.

**Caveat:** the data predate the registration. A blind map-level score, using the Z06 pipeline on ACT DR6 and Planck y-maps, would upgrade this from a confrontation to a registered outcome.
