# AZ13 — FAIL jointly; canonical FAIL, alt PASS of limited gates

κ = ½ FITTED; not theory closed

The stored sample contains 155 galaxies and 2788 accepted points. The fixed squared resolvent gives galaxy-equal rms 0.179032800 / 0.172614581 dex, compared with plain-law 0.169114605 / 0.170093010. Frozen rms margins are -0.004918195 / +0.002478428 dex; pooled-median margins are -0.015378224 / +0.012695541 dex. Canonical therefore fails both lines; alternate survives both. These fixed-U, spherical-surrogate comparison lines are not whole A1/A2 acceptance rows.

All nine controls pass. Point-source enclosed-mass error is 1.1433e-5; maximum mass-conservation relative error 3.8647e-13; density remains positive. Doubling shells changes statistics at most 2.1791e-5 dex. The nu=1 MUTATE has rms .573024732 dex and is rejected on both footings. Per-galaxy statistics and complete input hashes are in results.json and manifest.json.

The initial execution completed the calculation but failed JSON serialization of a numpy boolean before results were written. The repair converts check booleans to Python bool, with no criteria, mathematics or data change. The successful run records the repaired script. No outcome-dependent parameter selection occurred.

Finite-volume derivation: integrate (1-xi² Laplacian)u=rho over each shell. The diagonal is shell volume plus adjacent face conductances; off-diagonal is minus face conductance. Face conductance is 4 pi xi² r_face² / delta r_center. Applying this same conservative solve twice realizes the squared inverse. Face fluxes telescope, preserving total mass; the positive diagonal and nonpositive off-diagonals give a positive inverse. Outer zero flux and the declared distant boundary remain approximation choices. This is not an axisymmetric disc solution or a local-length action.
