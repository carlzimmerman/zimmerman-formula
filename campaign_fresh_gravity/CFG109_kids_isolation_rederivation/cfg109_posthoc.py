"""CFG109 post hoc (labelled): (1) C8 re-done with the correct simulation convention (true covariance, no Hartlap factor in the simulated statistic);
(2) power table with sigma_delta and sigma_A treated without the Hartlap inflation of the GLS error (delta), keeping the observed jackknife sigma_A;
(3) C4 tolerance diagnosis.  Run after cfg109_run.py wrote cfg109_results.json."""
import json, os, numpy as np
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg109_results.json")))
rng = np.random.default_rng(1109)
h = 41 / 49
for W in ("20", "30"):
    a = R["A2"][W]; wi = a["wiso"]["early"]; wn = 1 - wi
    sd_h = a["sigma_delta"]; sd_t = sd_h * np.sqrt(h)          # sigma with the true covariance (no Hartlap in P)
    Cb = np.array(a["Cb"]); s = np.array(R["main"]["D"]["10"])
    sPs_t = float(s @ np.linalg.solve(Cb, s)); assert abs(sPs_t ** -0.5 - sd_t) < 1e-9
    print("W%s: sigma_delta with Hartlap %.3f, with true C %.3f (ratio %.3f = sqrt(h))" % (W, sd_h, sd_t, sd_t / sd_h))
    if W == "20":
        dtrue = 0.5 / wn; lam = dtrue ** 2 * sPs_t; crit = stats.chi2.isf(0.05, 7)
        pan = stats.ncx2.sf(crit, 7, lam)
        r = dtrue * s[None, :] + rng.standard_normal((200000, 7)) @ np.linalg.cholesky(Cb).T
        Pt = np.linalg.inv(Cb); x = np.einsum("ni,ij,nj->n", r, Pt, r)
        dh = (r @ Pt @ s) / sPs_t; z = (dh - dtrue) / sd_t
        print("  C8 redone (no Hartlap in simulation): omnibus power analytic %.4f MC %.4f (lambda %.2f); GLS z mean %+.4f std %.4f" % (pan, np.mean(x > crit), lam, z.mean(), z.std()))
    for eta in (0.75, 0.9, 1.0):
        k = eta / wn - (1 - eta) / wi
        print("  eta %.2f: eps_min(80%%, 1-dof) Hartlap %.2f  true-C %.2f ; 95%% UL on eps Hartlap %.2f  true-C %.2f" % (eta, 2.487 * sd_h / abs(k), 2.487 * sd_t / abs(k), (a["delta"] + 1.645 * sd_h) / k, (a["delta"] + 1.645 * sd_t) / k))
print("C4: the measured max relative deviation of the shell partition is 6.27e-12 (summation-order roundoff at double precision; the same size as C2's 3e-11); the frozen 1e-12 tolerance was unrealistically tight.")
