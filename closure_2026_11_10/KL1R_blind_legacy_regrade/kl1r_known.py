#!/usr/bin/env python3
"""KL1R known answers KB1 (Legacy loader counts, n(z) sums, PD covariance) and KB2 (CO2's P4 through my loader and fit on KiDS-1000),
plus KA4 (CO2's response check).   python3 -I kl1r_known.py -> parts/known.json, kl1r_known.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl1r_lib as K
import numpy as np
T0 = time.time(); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
S = K.load_legacy(); F = K.fits.open(os.path.join(K.LEGACY, "data", "KiDS_Legacy_xipm.fits")); nzt = F["NZ_SOURCE"].data
npl = sum(r[0] == "+" for r in S["rows"]); nmi = len(S["rows"]) - npl
sums = [float(np.sum(nzt[f"BIN{i+1}"])) for i in range(6)]
zm = np.array(nzt["Z_MID"]); beyond = [float(np.sum(np.array(nzt[f"BIN{i+1}"])[zm > 3.5]) / np.sum(nzt[f"BIN{i+1}"])) for i in range(6)]
ev = np.linalg.eigvalsh(S["cov"]); angs = sorted({r[3] for r in S["rows"]}); prs = sorted({(r[1], r[2]) for r in S["rows"]})
order_ok = all(S["rows"][i][0] == "+" for i in range(189)) and all(S["rows"][189 + i][0] == "-" for i in range(189))
kb1 = dict(n_plus=npl, n_minus=nmi, n_bins=S["nbin"], n_pairs=len(prs), n_ang=len(angs), cov_min_eig=float(ev.min()), nz_sums=sums, nz_frac_beyond_3p5=beyond,
           mu_u=S["mu_u"].tolist(), ang_centres=sorted({round(r[4], 4) for r in S["rows"]}), n_pubkeep=int(S["pubkeep"].sum()), sig_e=S["sig_e"].tolist(), ngal=S["ngal"].tolist(), order_ok=order_ok)
kb1["pass_"] = bool(npl == 189 and nmi == 189 and S["nbin"] == 6 and len(prs) == 21 and len(angs) == 9 and ev.min() > 0 and all(abs(s - 1) <= 0.01 for s in sums) and order_ok)
P(f"KB1 Legacy: {npl} xi+ and {nmi} xi- points, {S['nbin']} bins, {len(prs)} pairs, {len(angs)} angular bins; COVMAT min eigenvalue {ev.min():.2e}; "
  f"n(z) weight sums {np.round(sums, 4).tolist()}; fraction beyond z 3.5 {np.round(beyond, 4).tolist()}; published cuts keep {kb1['n_pubkeep']} -> {'PASS' if kb1['pass_'] else 'FAIL'}")
P(f"    prior-mean shifts mu {S['mu_u'].tolist()}; angular centres {kb1['ang_centres']} arcmin; geometric centres of geomspace(2,300,10): {np.round(np.sqrt(np.geomspace(2,300,10)[:-1]*np.geomspace(2,300,10)[1:]),4).tolist()}")
# KB2
K0 = K.load_k1000(); R1 = K.run_of(K.ONE, K.S8E); PS0 = K.Pmat(R1, "S0")
fm = K.support_k(K0, R1, PS0); D0 = K.subset(K0, K0["pubkeep"] & (fm >= 0.9))
ROWS = json.load(open(os.path.join(K.CO2D, "co2_rows.json"))); CO2S = json.load(open(os.path.join(K.CO2D, "co2_shear.json")))
kb2 = {}
for ft in ("canonical", "alt"):
    s8 = ROWS["P2"][ft]["sigma8"]; r = K.fit_k(K0, D0, K.Pm_of(K.HM["primary"][ft]["R_tot"], s8)); ref = CO2S["P4"][ft]["chi2"]
    kb2[ft] = dict(chi2=r["chi2"], ref=ref, N=D0["N"], pass_=bool(abs(r["chi2"] - ref) <= 0.01 and D0["N"] == 104))
    P(f"KB2 [{ft}] CO2's P4 through my loader and fit on KiDS-1000: chi2 {r['chi2']:.3f} (CO2 {ref:.3f}), N {D0['N']} -> {'PASS' if kb2[ft]['pass_'] else 'FAIL'}")
k4 = K.ka4(); P("KA4 response median below k 0.12: " + ", ".join(f"node {z}: {v['median_alpha']:.3f}" for z, v in k4.items()) + f" -> {'PASS' if all(v['pass_'] for v in k4.values()) else 'FAIL'}")
json.dump(dict(KB1=kb1, KB2=kb2, KA4=k4, criteria="1792bd07ea", note="kappa = 1/2 FITTED; not theory closed"), open(os.path.join(K.HERE, "parts", "known.json"), "w"), indent=1, default=float)
open(os.path.join(K.HERE, "kl1r_known.out"), "w").write("\n".join(OUT) + "\n"); P(f"({time.time() - T0:.0f} s)")
