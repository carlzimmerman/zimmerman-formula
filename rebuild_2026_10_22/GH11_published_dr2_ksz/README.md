# GH11_published_dr2_ksz: CLOSED UNRUN, superseded

**No grade was run here.** While this lane's criteria were being frozen (606f89cf0f), a parallel session had already graded the same published points in `GH10_dr2_ksz_published_points` (BELOW NEED, A(1.8) 0.448 ± 0.105), using the machine-readable data release, which is better than the table extraction planned here. It has continued in `GH11_ksz_two_halo_miscentring`. Read those. This folder's ID collides with that lane, and GH10_smooth_gas_taper collides with GH10_dr2; both were found by the check that should have come first.

Not covered by that lane and not done here: the F1 and F2 tapers on the DR2 points.

## Source check of arXiv:2604.19745 (LaTeX source, not a fetch summariser)

`GH10_dr2_ksz_published_points` quotes these through a summariser. Read directly from `main.tex`:

| Value | Source | Status |
|---|---|---|
| SNR 8.23, log M★ > 10.5 | CAP table | confirmed |
| f_sat 0.279 (> 10.5), 0.364 (> 11) | HOD table | confirmed; errors +0.212/−0.157 and +0.213/−0.177 |
| log M̄_h 13.336 (> 10.5) | HOD table | confirmed |
| r_fid 0.64 for BGS, about 10 % uncertainty | text | confirmed; adopted from Guachalla et al. 2023 and Hadzhiyska et al. 2023 mocks |
| σ_true 300 km/s | text | confirmed, "for ease" |

**Its open K2 question has most of an answer.** That lane computes S/N(> 10.5) 9.46 from the published covariance against the paper's 8.23 and says the convention isn't identified. The paper defines SNR ≡ √(χ²_null − χ²_bf), not √χ²_null. Its CAP table gives χ²_null 80.77 and χ²_bf 13.07, so √67.70 = 8.23 exactly. The comparable number to 9.46 is therefore √80.77 = 8.99. A residual of 5 % in S/N (χ² 89.5 vs 80.77) remains unexplained; I did not trace it. The result of that lane isn't changed by this.

κ = ½ FITTED; c_f EXTERNAL. Not theory closed. Nothing here says the data favour the framework.
