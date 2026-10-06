# Independent review of root geodesic stationary exterior lemma

**Primary verdict: proved as written.** The result is a necessary-equation obstruction on the explicitly normalized N=B=1 stationary geodesic vacuum interval, not a no-go for an accelerated clock or a statement that all geodesic clocks admit this normalization. Current input hashes are recorded in geodesic_review_inputs.json. I read the actual lemma and script and independently reconstructed its necessary equations from the radial action.

For spatial dimension n≥2, write p=(n−1)M/2 and Veff=n(n−1)MH²/2. At N=B=1 after varying, the B Euler equation is
p r^(n−3)[2rVV'+(n−2)V²]−Veff r^(n−1)=0.
This is exactly (r^(n−2)V²)'=nH²r^(n−1). The difference between the N and B Euler equations is
r^(n−1){2c+[2c/(nH)](V'+(n−1)V/r)}=0,
so V'+(n−1)V/r=−nH. The acceleration response has Q(0)=Q_a(0)=0, so neither its background value nor first variation changes these necessary equations. Its positive quadratic lapse-gradient coefficient should not be confused with a nonzero first variation at N'=0.

The integrated solutions are V²=H²r²+μ r^−(n−2) and V=−Hr+C r^−(n−1). Substituting the latter into the first yields the exact residual −nC²r^−(n+1), forcing C=0 for real C on any open positive-r interval and hence μ=0. The sign of C is irrelevant. The conclusion comes from this general-n algebra, not the finite checks. n=2 has a constant μ contribution and no asserted ordinary4D Newton interpretation.

The lemma first uses the momentum equation to make B constant where V≠0, then explicitly assumes the flat cosmological B=1 and lapse N=1 normalization. This scope is essential: one cannot silently turn an arbitrary constant areal B into1 by changing the areal radius while preserving the same spherical metric form. Similarly c>0,H>0 and the chosen rolling vacuum branch are actual hypotheses. They are already stated, so no correction is needed.

The contrast with the expanding-dust first-order control is sound. At O(C), r^(n−2)V² differs by the constant −2HC, whose radial derivative vanishes. The obstruction first appears at O(C²). The control is also nonstationary matter in physical coordinates; its linear Newton force cannot be promoted to an exact finite-mass stationary vacuum solution from those data alone.

I ran the current supplied check script with --output restricted to this owned directory (geodesic_review_run.json): its symbolic checks for n=2..7 passed, including its false-exact-linear-mode rejection. The script implements the displayed action, varies N/B before substitution, and correctly compares the lapse difference and quadratic residual. It uses positive C for its test fixtures, whereas the prose proof correctly covers all real C. There is no mathematical issue in that narrower computational fixture.

Strongest safe statement: this flat-normalized stationary geodesic branch has only the massless rolling de Sitter exterior. The exact nonzero-flow accelerated P2 candidate in REPORT.md here remains outside the obstruction. Its matching, regular conserved interior, and finite-gradient health are unproved. No remaining implication is needed for the stated necessary-equation lemma; existence of the excluded broader source problem was never its claim.
