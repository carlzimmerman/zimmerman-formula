# MAGNETIZED-TORUS + DISCRETE WILSON LINES — FROZEN CRITERIA (committed before any script)

Same setup as TORUS_YUKAWA (M_L = M_R = 3, M_H = 6, numerical theta overlaps). Wilson lines shift each field's
zero modes: ψ_ζ(z) = ψ(z + ζ) (prefactor included). Gauge invariance: ζ_H = (ζ_L + ζ_R)/2 (flux-weighted);
gate: the integrand ψ_L ψ_R conj(ψ_H) must be single-valued on the torus to 1e-10, else the convention is wrong.

PRE-DECLARED set: ζ_L, ζ_R ∈ {(p + q τ)/3 : p, q ∈ {0,1,2}} (Z3-compatible, 9 each), τ ∈ {i, e^{2πi/3}},
Higgs single mode k ∈ {0..5} or uniform → 9·9·2·7 = 1134 configurations.
 PASS only if a configuration has |Q - 0.666661| < 3e-5 AND m_μ/m_e and m_τ/m_μ both within a factor 2 of
 206.77 and 16.82, AND the number of such hits exceeds the chance expectation (estimated by replacing the
 1134 Q values with Q drawn from the configurations' own empirical distribution, i.e. the expected number of
 |Q - 2/3| < 3e-5 hits = 1134 × empirical density near 2/3).
 KILL otherwise. Report: Q range, number of non-degenerate spectra, best hierarchy match, and every Koide-band hit.
