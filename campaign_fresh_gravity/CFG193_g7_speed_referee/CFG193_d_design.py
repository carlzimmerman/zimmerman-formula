#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""CFG193_d_design -- attack (d): what sample WOULD be diagnostic for G7 (repo tables only, no new data).
D1 design formula sigma_beta = ln10 s / (sqrt(N) rms z), checked against my measured Fisher; D2 the lever arm in the repo tables
(UNGC redshift-independent distances; others excluded as circular); D3 the physical ceiling; D4 the statement.
Needs CFG193_c_fit_power_results.json (main run).  Rerun: ZF_REPO=<repo> python3 CFG193_d_design.py (< 1 min).  Exit 0."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG193_common import *

T = Tee(os.path.join(HERE, "CFG193_d_design.out"))
P = T.p
P("CFG193_d_design  (repo = <repo>)")
M = json.load(builtins.open(os.path.join(HERE, "CFG193_c_fit_power_results.json")))
tau, sigi, rmsz, SF = M["tau"], M["median_sigma_i"], M["rms_z"], M["fisher"]
s_meas = math.sqrt(sigi ** 2 + tau ** 2)
N = M["n_primary"]
form = LN10 * s_meas / (math.sqrt(N) * rmsz)
P("D1 check: s = sqrt(median sigma_i^2 + tau^2) = %.3f dex, N = %d, rms z = %.3f -> formula sigma_beta = %.3f;  my measured Fisher = %.3f (ratio %.2f; the formula uses the median sigma_i and the population rms, the Fisher the per-galaxy weights)" % (
    s_meas, N, rmsz, form, SF, SF / form))
P("D1 target sigma_beta = 0.05 (2 sigma = G7's 0.10):  N required = (ln10 * s / 0.05)^2 / rms(z)^2")
S_ = (0.43, s_meas, 0.30, 0.20, 0.10)
R_ = (0.27, rmsz, 0.5, 1.0, 1.39, 2.0)
P("   s (dex) \\ rms z  " + "  ".join("%7.3f" % r for r in R_))
tab = {}
for s in S_:
    row = []
    for r in R_:
        n = (LN10 * s / 0.05) ** 2 / r ** 2
        row.append(n)
    tab[str(round(s, 3))] = row
    P("   %14.3f  " % s + "  ".join("%7.0f" % n for n in row))
P("   (SPARC-like s = 0.43, rms z = 0.27 -> N = %.0f galaxies; s = 0.43 and rms z ~ 1 -> N = %.0f; s = 0.20 and rms z = 1 -> N = %.0f)" % (
    (LN10 * 0.43 / 0.05) ** 2 / 0.27 ** 2, (LN10 * 0.43 / 0.05) ** 2 / 1.0, (LN10 * 0.20 / 0.05) ** 2 / 1.0))
P("   at SPARC's actual N = %d and rms z: sigma_beta(s) = ln10 s/(sqrt(N) rms z): s = 0.43 -> %.2f; s = 0.20 -> %.2f; s = 0.10 -> %.2f  (never reaches 0.05)" % (
    N, LN10 * 0.43 / (math.sqrt(N) * rmsz), LN10 * 0.20 / (math.sqrt(N) * rmsz), LN10 * 0.10 / (math.sqrt(N) * rmsz)))
# D2: UNGC
ns = os.path.join(DATA, "ungc_karachentsev2013.tsv")
hdr, rows = read_tsv_vizier(ns)
INDEP = {"TRGB", "SBF", "Cep", "SN", "RR", "HB", "CMD", "geom", "PNLF", "BS"}
out = []
for r in rows:
    try:
        ra, dec, hrv, d = float(r["_RAJ2000"]), float(r["_DEJ2000"]), float(r["HRV"]), float(r["Dist"])
    except (ValueError, KeyError):
        continue
    m = r["f_Dist"].strip()
    out.append((r["Name"], ra, dec, hrv, d, m))
P("D2 UNGC: %d rows with position, HRV and Dist; methods: %s" % (len(out), dict(sorted({m: sum(1 for o in out if o[5] == m) for m in set(o[5] for o in out)}.items(), key=lambda kv: -kv[1]))))
ra = np.array([o[1] for o in out]); de = np.array([o[2] for o in out]); hrv = np.array([o[3] for o in out]); dist = np.array([o[4] for o in out]); meth = np.array([o[5] for o in out])
l, b = to_gal(ra, de)
nh = np.array([unit(a, c) for a, c in zip(l, b)])
zc = np.array([cmb_convert(v, li, bi) for v, li, bi in zip(hrv, l, b)])
uu = np.array([float(u_los(z_, D_)) for z_, D_ in zip(zc, dist)])
zz = (uu / W_REF) ** 2
D2 = {}
for lab, sel in (("independent, D <= 40 Mpc", np.isin(meth, list(INDEP)) & (dist <= 40)), ("independent, D <= 40 Mpc, D >= 3 Mpc", np.isin(meth, list(INDEP)) & (dist <= 40) & (dist >= 3)),
                 ("independent, 8 < D <= 40 Mpc", np.isin(meth, list(INDEP)) & (dist <= 40) & (dist > 8)), ("SPARC-like: TRGB/Cep/SN only, D <= 25", np.isin(meth, ["TRGB", "Cep", "SN"]) & (dist <= 25)),
                 ("TF (mass-dependent, circular for a0; excluded)", meth == "TF"), ("all rows", np.ones(len(out), bool))):
    if sel.sum() < 3:
        continue
    D2[lab] = dict(n=int(sel.sum()), rms_z=float(np.std(zz[sel])), median_abs_u=float(np.median(np.abs(uu[sel]))), max_abs_u=float(np.max(np.abs(uu[sel]))),
                   median_sigma_u_5pct=float(np.median(H0_PRIMARY * 0.05 * dist[sel])))
    P("   %-52s N=%4d  rms z = %.3f  median |u| = %5.0f  max |u| = %5.0f km/s;  sigma_u at 5%% distance error (median) = %.0f km/s" % (
        lab, sel.sum(), D2[lab]["rms_z"], D2[lab]["median_abs_u"], D2[lab]["max_abs_u"], D2[lab]["median_sigma_u_5pct"]))
sel = np.isin(meth, list(INDEP)) & (dist <= 40)
Ndiag = (LN10 * 0.43 / 0.05) ** 2 / max(D2["independent, D <= 40 Mpc"]["rms_z"], 1e-9) ** 2
P("   UNGC independent-distance set: rms z %.3f vs SPARC's %.3f (ratio %.2f); at s = 0.43 dex that set would need N = %.0f (it has %d) for sigma_beta = 0.05; it has no rotation curves (W50 only), so it is a lever-arm census, not an a0 sample" % (
    D2["independent, D <= 40 Mpc"]["rms_z"], rmsz, D2["independent, D <= 40 Mpc"]["rms_z"] / rmsz, Ndiag, int(sel.sum())))
P("D2 other repo tables: KT2017 galaxies (HRV only, no distances); KT2017 groups_full (group distances from flow/TF: circular); 2MRS (cz only); ALFALFA tables (flow-model distances: circular); SLACS/SLUGGS/ATLAS3D (ellipticals, not the SPARC a0 estimator).  None gives a redshift-independent-distance sample beyond ~40 Mpc with rotation curves.")
# D3
P("D3 lever-arm ceiling: half the sample at w = 0 and half at 1000 km/s gives z in {0, 2.78}: rms z = %.2f; sigma_u = H0 e_D <= 100 km/s needs D <= %.0f Mpc at e_D/D = 5%% and D <= %.0f Mpc at 3%%" % (
    float(np.std([0.0] * 50 + [(1000 / 600.0) ** 2] * 50)), 100.0 / (H0_PRIMARY * 0.05), 100.0 / (H0_PRIMARY * 0.03)))
P("D3 but nearby galaxies co-move with the Local Volume (r(u, V_LG.n) = %.2f in SPARC): u ~ V_LG.n, so w = 0 relative to the CMB frame is rare inside 40 Mpc; the single component u alone cannot give the 3D w (only 3D flow reconstructions can)" % M["A3"]["r_u_proj"])
P("D4 STATEMENT: SPARC-like N = 68 gives sigma_beta ~ %.2f (Fisher); a diagnostic sample (sigma_beta <= 0.05) needs N * rms(z)^2 >= (ln10 s / 0.05)^2 = %.0f for s = 0.43 dex, i.e. ~%.0f galaxies with independent distances to ~5%% and w spanning 0-1000 km/s (rms z ~ 1), or ~%.0f if per-galaxy a0 scatter s could be cut to 0.2 dex; no repo table supplies it." % (
    SF, (LN10 * 0.43 / 0.05) ** 2, (LN10 * 0.43 / 0.05) ** 2 / 1.0, (LN10 * 0.20 / 0.05) ** 2 / 1.0))
jdump(dict(D1_table=tab, D1_formula=form, D1_measured=SF, D2=D2, s_meas=s_meas), os.path.join(HERE, "CFG193_d_design_results.json"))
P("verdict: done (no pass/fail lines; design arithmetic)")
sys.exit(0)
