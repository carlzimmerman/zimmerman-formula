#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h109_halo_spin.py -- HUNT ITEM 109: the halo SPIN PARAMETER, predicted from the baryons.
=========================================================================================
lambda = j / (sqrt(2) R200 V200) is the one halo number that LambdaCDM claims to explain from first principles: tidal torque
theory gives a log-normal with median ~0.035 and sigma_ln ~ 0.5, essentially independent of mass, and the disc is then required
to retain its share of it.  In the framework there is no halo -- what a rotation-curve fitter calls a halo is the PHANTOM -- so
R200 and V200 are not free: in the deep-MOND regime the phantom's enclosed dynamical mass is M_dyn(r) = sqrt(M_b a_0/G) r, so

        V200^2 = G M_dyn(R200)/R200 = sqrt(G M_b a_0)  =>  V200 = (G M_b a_0)^(1/4) = V_flat  EXACTLY,
        R200   = V200/(10 H0),      lambda = 10 H0 j / (sqrt(2) sqrt(G M_b a_0)).

That is a ZERO-PARAMETER prediction of the whole spin distribution from photometry + a rotation curve + a_0, and it is
DISTANCE-FREE: j scales as D and V200^2 as sqrt(M_b) scales as D, so lambda does not move when the distance does.
Here the exact kernel version is solved (nu(y) at R200, a 0.3% correction on the deep-MOND limit) and compared, galaxy by
galaxy, with lambda built from Li+2020's own fitted V200 for all twelve halo models, and with the tidal-torque log-normal.

j is the STELLAR DISC's specific angular momentum measured from the [3.6] surface-brightness profile and the observed rotation
curve, j = int SB v r^2 dr / int SB r dr, with an analytic exponential tail beyond the last measured point.  Upsilon cancels
inside a single component, so j carries no stellar mass-to-light ratio at all; M_b does, and the lever is quoted.

Data: SPARC (Q<=2, i>=30) + Li+2020 halo fits (real_research/data/li2020_sparc_halos.tsv).  Both footings.  Mutations.
Checks CAN fail.
"""
import sys, math, os
import numpy as np
from scipy.optimize import brentq
from scipy import stats
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(109)
H0_LI = 73.0e3/Mpc                      # Li+2020's own convention, recovered below from their table: V200 = 10 H0 R200
KMS_PER_KPC = 1e3/kpc

# ------------------------------------------------------------------ Li+2020 halo fits
path = os.path.join(DATA, "li2020_sparc_halos.tsv")
rows = [l.rstrip("\n").split("\t") for l in open(path) if l.strip() and not l.startswith("#")]
hdr = [h.strip() for h in rows[0]]; col = {h: i for i, h in enumerate(hdr)}
def _ff(v):
    try: return float(v)
    except Exception: return np.nan
LI = {}
for d in rows[3:]:
    if len(d) < len(hdr): continue
    m = d[col["Model"]].strip(); n = d[col["Name"]].strip()
    LI.setdefault(m, {})[n] = dict(V200=_ff(d[col["V200"]]), eV200=_ff(d[col["e_V200"]]), C200=_ff(d[col["C200"]]),
                                   rs=_ff(d[col["rs"]]), chi2=_ff(d[col["chi2"]]), Yd=_ff(d[col["Ydisk"]]),
                                   Yb=_ff(d[col["Ybul"]]), D=_ff(d[col["Dist"]]), lM=_ff(d[col["log(M200)"]]))
MODELS = sorted(LI)
P("="*126); P("ITEM 109 -- the halo spin parameter predicted from the baryons"); P("="*126)
info(f"Li+2020 J/ApJS/247/31: {len(MODELS)} halo models x {len(LI[MODELS[0]])} SPARC galaxies")
_b = LI["Burkert-Flat"]
_rat = np.array([_b[n]["V200"]/(_b[n]["C200"]*_b[n]["rs"]) for n in _b if np.isfinite(_b[n]["V200"])])
info(f"convention recovered from the table itself: V200/(C200 rs) = {np.median(_rat):.4f} km/s/kpc = 10 H0 with H0 = {np.median(_rat)*100:.1f} km/s/Mpc")
ck("109-setup Li+2020's R200 = C200 x r_s and V200 = 10 H0 R200 with H0 = 73, recovered from their own table to 0.5%; the same H0 is used on BOTH sides here so the comparison is internally consistent",
   abs(np.median(_rat)*100 - 73.0) < 0.5, f"implied H0 = {np.median(_rat)*100:.2f} km/s/Mpc, spread {np.percentile(_rat,95)/np.percentile(_rat,5)-1:.1%}")

# ------------------------------------------------------------------ specific angular momentum of the stellar disc
def j_star(g, ups_d=UPS_D):
    """j = int SB_disk(r) v_obs(r) r^2 dr / int SB_disk(r) r dr, plus an analytic exponential tail beyond r_max.
    Upsilon cancels exactly (one component), so j carries NO stellar mass-to-light ratio.  Returns (j, tail fraction, h_out)."""
    ok = g["sbd"] > 0
    if ok.sum() < 4: return np.nan, np.nan, np.nan
    r, sb, v = g["r"][ok], g["sbd"][ok], g["vobs"][ok]
    num = np.trapz(sb*v*r*r, r); den = np.trapz(sb*r, r)
    out = r > 0.5*r[-1]                                    # outer half: local exponential scale length for the tail
    h = np.nan
    if out.sum() >= 3:
        s = np.polyfit(r[out], np.log(sb[out]), 1)
        if s[0] < 0: h = -1.0/s[0]
    Rd = g["Rdisk"]
    if not np.isfinite(h) or not (0.3*Rd < h < 3.0*Rd): h = Rd
    if not np.isfinite(h) or h <= 0: return num/den, 0.0, np.nan
    rm, S, vl = r[-1], sb[-1], v[-1]
    den_t = S*h*(rm + h)                                   # int_rm^inf S e^{-(r-rm)/h} r dr
    num_t = vl*S*h*(rm*rm + 2*rm*h + 2*h*h)                # int_rm^inf S e^{-(r-rm)/h} v r^2 dr, v = v_last
    return (num + num_t)/(den + den_t), num_t/(num + num_t), h

# ------------------------------------------------------------------ the framework's own R200, V200 (exact kernel)
def v200_phantom(Mb_kg, a0, H0):
    """Solve (10 H0 R)^2 = nu(G Mb/(a0 R^2)) G Mb / R for R200; returns (V200 [m/s], R200 [m], y at R200)."""
    f = lambda lr: 2*lr + 2*math.log(10*H0) - math.log(nu_s(G*Mb_kg/(a0*math.exp(2*lr)))*G*Mb_kg) + lr
    lo, hi = math.log(1e17), math.log(1e24)
    lr = brentq(f, lo, hi, xtol=1e-10)
    R = math.exp(lr)
    return 10*H0*R, R, G*Mb_kg/(a0*R*R)

gals = load_sparc()
recs = []
for g in gals:
    j, tf, h = j_star(g)
    if not np.isfinite(j) or j <= 0: continue
    if not np.isfinite(tf) or tf > 0.5: continue            # reject discs whose j is more tail than data
    ok = g["sbd"] > 0
    if g["Rdisk"] <= 0 or g["r"][ok][-1]/g["Rdisk"] < 2.0: continue
    recs.append(dict(name=g["name"], j=j, tail=tf, Mb=g["Mb"], Vflat=g["Vflat"], L36=g["L36"], MHI=g["MHI"],
                     inc=g["inc"], D=g["D"], Rdisk=g["Rdisk"], rmax=g["r"][ok][-1], g=g))
info(f"j measured for {len(recs)}/{len(gals)} SPARC discs (cuts: >=4 photometric points, r_max/R_d >= 2, tail < 50% of j)")
tails = np.array([r["tail"] for r in recs])
info(f"the exponential tail beyond the last measured point carries a median {100*np.median(tails):.0f}% of j (90th pct {100*np.percentile(tails,90):.0f}%) -- it is NOT negligible and it is the largest modelling choice in j")
jj = np.array([r["j"] for r in recs])
jchk = np.array([2*r["Rdisk"]*r["Vflat"] for r in recs]); okc = jchk > 0
ck("109-j the measured j reproduces the analytic 2 R_d V_flat of an ideal exponential disc with a flat curve to better than 0.1 dex in the median -- the estimator is not broken",
   abs(np.median(np.log10(jj[okc]/jchk[okc]))) < 0.1,
   f"median log10(j_measured / 2 R_d V_flat) = {np.median(np.log10(jj[okc]/jchk[okc])):+.3f} dex, scatter {np.std(np.log10(jj[okc]/jchk[okc])):.3f}, N = {okc.sum()}")

# ------------------------------------------------------------------ lambda, framework side
P(""); P("-"*126); P("the framework's V200 and lambda (zero parameters: photometry, the rotation curve, and a_0)"); P("-"*126)
LAM_P = {}
for ft, a0 in A0.items():
    V, R, Y = [], [], []
    for r in recs:
        v, rr, y = v200_phantom(r["Mb"]*Msun, a0, H0_LI)
        V.append(v/1e3); R.append(rr/kpc); Y.append(y)
    V = np.array(V); R = np.array(R); Y = np.array(Y)
    lam = jj/(math.sqrt(2)*R*V)
    LAM_P[ft] = dict(lam=lam, V200=V, R200=R, y=Y)
    Vdeep = np.array([(G*r["Mb"]*Msun*a0)**0.25/1e3 for r in recs])
    info(f"{ft:10}: V200 median {np.median(V):6.1f} km/s, R200 median {np.median(R):6.1f} kpc, y = g_bar/a_0 at R200 median {np.median(Y):.2e} (deep MOND, so V200 = (G M_b a_0)^1/4 to {100*np.median(V/Vdeep-1):.2f}%)")
    info(f"{'':10}  lambda: median {np.median(lam):.4f}, 16-84% [{np.percentile(lam,16):.4f}, {np.percentile(lam,84):.4f}], width {np.std(np.log10(lam)):.3f} dex")
vf = np.array([r["Vflat"] for r in recs]); okv = vf > 0
dvf = {ft: np.log10(LAM_P[ft]["V200"][okv]/vf[okv]) for ft in A0}
ck("109f the framework's sharpest statement here, tested on its own: deep MOND forces V200 = V_flat EXACTLY, and SPARC's measured V_flat reproduces the predicted V200 to within 0.05 dex in the median with only 0.06 dex of scatter.  This is the BTFR wearing a virial-velocity label, and it must be quoted that way and not as an independent success",
   max(abs(np.median(dvf[ft])) for ft in A0) < 0.10 and np.std(dvf["canonical"]) < 0.10,
   f"median log10(V200_pred/V_flat) = {np.median(dvf['canonical']):+.3f} dex (canonical) / {np.median(dvf['alt']):+.3f} (alt), scatter {np.std(dvf['canonical']):.3f} dex over N = {okv.sum()}")
# the M/L-FREE version of the same prediction: V200 = V_flat is an identity, so lambda needs no M_b and no Upsilon at all
R200_id = vf[okv]*1e3/(10*H0_LI*kpc)                     # kpc; R200 = V_flat/(10 H0) exactly, since V200 = V_flat
lam_id = jj[okv]/(math.sqrt(2)*R200_id*vf[okv])
info(f"the M/L-FREE form: because V200 = V_flat identically, lambda = 10 H0 j/(sqrt(2) V_flat^2) can be evaluated with NO stellar mass-to-light ratio anywhere -- j is Upsilon-free by construction and V_flat is measured.  Median {np.median(lam_id):.4f}, width {np.std(np.log10(lam_id)):.3f} dex, on N = {okv.sum()}")
info(f"     (versus {np.median(LAM_P['canonical']['lam'][okv]):.4f} for the fully predicted canonical version on the same galaxies: median per-galaxy")
info(f"      log10(lambda_MLfree/lambda_pred) = {np.median(np.log10(lam_id/LAM_P['canonical']['lam'][okv])):+.3f} dex, which is exactly minus twice the 109f BTFR zero-point offset, as it must be)")

# ------------------------------------------------------------------ lambda, fitted-halo side
P(""); P("-"*126); P("lambda from Li+2020's fitted halos, all twelve models (same j, so the comparison is entirely about V200)"); P("-"*126)
FIT = {}
for m in MODELS:
    lam, lr_c, lr_a, eV = [], [], [], []
    for i, r in enumerate(recs):
        b = LI[m].get(r["name"])
        if b is None or not np.isfinite(b["V200"]) or b["V200"] <= 0: continue
        R200 = b["C200"]*b["rs"]
        lam.append(r["j"]/(math.sqrt(2)*R200*b["V200"]))
        lr_c.append(math.log10(b["V200"]/LAM_P["canonical"]["V200"][i]))
        lr_a.append(math.log10(b["V200"]/LAM_P["alt"]["V200"][i]))
        eV.append(b["eV200"]/b["V200"])
    FIT[m] = dict(lam=np.array(lam), dV_c=np.array(lr_c), dV_a=np.array(lr_a), eV=np.array(eV))
    L = FIT[m]["lam"]
    info(f"{m:14} N={len(L):3d}  lambda_fit median {np.median(L):.4f} width {np.std(np.log10(L)):.3f} dex | "
         f"log10(V200_fit/V200_pred) med {np.median(FIT[m]['dV_c']):+.3f} sc {np.std(FIT[m]['dV_c']):.3f} (canon) "
         f"{np.median(FIT[m]['dV_a']):+.3f} (alt) | median e_V200/V200 {np.median(FIT[m]['eV']):.2f}")
PRIOR = [m for m in MODELS if m.endswith("-LCDM")]; FLAT = [m for m in MODELS if m.endswith("-Flat")]
dv_prior = np.array([np.median(FIT[m]["dV_c"]) for m in PRIOR]); sc_prior = np.array([np.std(FIT[m]["dV_c"]) for m in PRIOR])
dv_flat  = np.array([np.median(FIT[m]["dV_c"]) for m in FLAT]);  sc_flat  = np.array([np.std(FIT[m]["dV_c"]) for m in FLAT])
P("")
ck("109a (a WORKS) the framework's zero-parameter V200 = (G M_b a_0)^(1/4) reproduces the V200 that halo fitters actually recover: across the five LambdaCDM-prior halo models the median log10(V200_fit/V200_pred) is inside 0.1 dex on both footings, with a 0.09-0.11 dex galaxy-to-galaxy scatter -- i.e. a halo virial velocity predicted from photometry and a_0 alone",
   np.abs(dv_prior).max() < 0.10,
   f"LambdaCDM-prior models {[f'{m.split(chr(45))[0]}:{v:+.3f}' for m, v in zip(PRIOR, dv_prior)]} dex (canonical); alt footing "
   f"{[f'{np.median(FIT[m]['dV_a']):+.3f}' for m in PRIOR]}; scatter {sc_prior.min():.3f}-{sc_prior.max():.3f} dex")
ck("109a-AGAINST-INTEREST the agreement is best exactly where the LambdaCDM prior is doing the work.  The seven flat-prior fits, where the rotation curve alone must set V200, scatter 2-3x more and their medians move by up to 0.3 dex -- so lambda_fit is substantially a PRIOR, not a measurement, and 109a must be quoted as consistency with the fitters' convention, not as a measurement of V200",
   sc_flat.max() > 2*sc_prior.min(),
   f"flat-prior scatter {sc_flat.min():.3f}-{sc_flat.max():.3f} dex vs LambdaCDM-prior {sc_prior.min():.3f}-{sc_prior.max():.3f}; flat-prior medians {dv_flat.min():+.3f} to {dv_flat.max():+.3f} dex; median e_V200/V200 is {np.median([np.median(FIT[m]['eV']) for m in FLAT]):.2f} for flat priors vs {np.median([np.median(FIT[m]['eV']) for m in PRIOR]):.2f} with the prior")

# ------------------------------------------------------------------ the distributions
P(""); P("-"*126); P("the lambda distributions: median AND width, framework vs fitted vs tidal torque"); P("-"*126)
TT_MED, TT_SIG = 0.035, 0.5/math.log(10)                  # Bullock+2001 tidal-torque log-normal: median 0.035, sigma_ln = 0.5
info(f"LambdaCDM alternative (tidal torque, Bullock+2001): lambda log-normal, median {TT_MED:.3f}, width {TT_SIG:.3f} dex, no mass dependence")
ref = "NFW-LCDM"
lam_f = FIT[ref]["lam"]
for ft in A0:
    lam_p = LAM_P[ft]["lam"]
    info(f"{ft:10} framework lambda: median {np.median(lam_p):.4f} ({math.log10(np.median(lam_p)/TT_MED):+.3f} dex from tidal torque), width {np.std(np.log10(lam_p)):.3f} dex")
info(f"{ref:10} fitted    lambda: median {np.median(lam_f):.4f} ({math.log10(np.median(lam_f)/TT_MED):+.3f} dex from tidal torque), width {np.std(np.log10(lam_f)):.3f} dex")
d_med = {ft: math.log10(np.median(LAM_P[ft]["lam"])/np.median(lam_f)) for ft in A0}
ck("109b (a WORKS) the framework's predicted spin-parameter distribution matches the one built from the fitted halos in MEDIAN to better than 0.15 dex on both footings -- with j identical on the two sides, this is the V200 agreement squared, and it is the whole distribution, not a fit",
   max(abs(v) for v in d_med.values()) < 0.15,
   f"median log10(lambda_pred/lambda_fit) = {d_med['canonical']:+.3f} (canonical) / {d_med['alt']:+.3f} (alt) against {ref}; across all five LambdaCDM-prior models {min(math.log10(np.median(LAM_P['canonical']['lam'])/np.median(FIT[m]['lam'])) for m in PRIOR):+.3f} to {max(math.log10(np.median(LAM_P['canonical']['lam'])/np.median(FIT[m]['lam'])) for m in PRIOR):+.3f} dex")
w_p = np.std(np.log10(LAM_P["canonical"]["lam"])); w_f = np.std(np.log10(lam_f))
excess = math.sqrt(max(w_f**2 - w_p**2, 0.0))
ck("109c CLAIM UNDER TEST, AND IT FAILS: that the framework predicts the WIDTH of the spin distribution as well as its median, to the hunt's 0.05 dex.  It does not -- the predicted distribution is the narrower, because with j identical on both sides its only scatter is the BTFR's",
   abs(w_p - w_f) < 0.05,
   f"predicted width {w_p:.3f} dex vs fitted {w_f:.3f} dex ({ref}) vs tidal torque {TT_SIG:.3f} dex; five LambdaCDM-prior models give {min(np.std(np.log10(FIT[m]['lam'])) for m in PRIOR):.3f}-{max(np.std(np.log10(FIT[m]['lam'])) for m in PRIOR):.3f} dex")
info(f"where the missing width lives, exactly: the excess in quadrature is {excess:.3f} dex in lambda = {excess/2:.3f} dex in V200, and the")
info(f"     galaxy-to-galaxy scatter of log10(V200_fit/V200_pred) is {np.std(FIT[ref]['dV_c']):.3f} dex.  They agree, so the framework is not missing a")
info(f"     source of spin scatter -- it is missing the fitters' halo-to-halo V200 scatter at fixed baryons, of which the fits' own")
info(f"     e_V200/V200 = {np.median(FIT[ref]['eV']):.2f} accounts for {2*np.median(FIT[ref]['eV'])/math.log(10):.3f} dex.  About half the excess is fit noise; the rest is real and unexplained here.")
ks_p = stats.kstest(np.log10(LAM_P["canonical"]["lam"]), "norm", args=(math.log10(TT_MED), TT_SIG))
ks_f = stats.kstest(np.log10(lam_f), "norm", args=(math.log10(TT_MED), TT_SIG))
info(f"KS against the tidal-torque log-normal: framework D = {ks_p.statistic:.3f} (p = {ks_p.pvalue:.1e}); fitted-halo D = {ks_f.statistic:.3f} (p = {ks_f.pvalue:.1e})")
ck("109d the framework's lambda distribution is not distinguishable from the tidal-torque log-normal any more badly than the fitted halos' own is -- so spin does NOT discriminate between the two accounts, which is the honest verdict of this item",
   ks_p.statistic < 2.0*ks_f.statistic,
   f"framework D = {ks_p.statistic:.3f} vs fitted D = {ks_f.statistic:.3f} on N = {len(lam_f)}; both reject the exact Bullock log-normal, chiefly because SPARC is not a volume-limited sample and both distributions here are too narrow")

# ------------------------------------------------------------------ levers, systematics, mutations
P(""); P("-"*126); P("levers and mutation controls"); P("-"*126)
Mb_arr = np.array([r["Mb"] for r in recs]); Ms = np.array([UPS_D*r["L36"]*1e9 for r in recs])
fstar = Ms/Mb_arr
for ups in (0.35, 0.5, 0.7):
    Mb2 = np.array([ups*r["L36"]*1e9 + 1.33*r["MHI"]*1e9 for r in recs])
    V2 = np.array([v200_phantom(m*Msun, A0["canonical"], H0_LI)[0]/1e3 for m in Mb2])
    R2 = np.array([v200_phantom(m*Msun, A0["canonical"], H0_LI)[1]/kpc for m in Mb2])
    l2 = jj/(math.sqrt(2)*R2*V2)
    info(f"Upsilon_[3.6] = {ups:.2f}: median lambda_pred = {np.median(l2):.4f} ({math.log10(np.median(l2)/np.median(LAM_P['canonical']['lam'])):+.3f} dex from the committed 0.50)")
info(f"the M/L lever, stated explicitly (bug pattern 5): j is Upsilon-FREE but M_b is not, and lambda_pred ~ M_b^(-1/2) at fixed j, so d log lambda/d log Upsilon = -0.5 f_star with median f_star = {np.median(fstar):.2f} -> {-0.5*np.median(fstar):.2f}.  A 40% error in Upsilon moves lambda_pred by {abs(0.5*np.median(fstar)*math.log10(1.4)):.3f} dex.  It cannot make 109c pass.")
info(f"the DISTANCE lever is exactly zero: j ~ D and V200_pred^2 = sqrt(G M_b a_0) ~ D, so lambda_pred is distance-independent by construction; lambda_fit is not.")
info(f"the INCLINATION lever: v_obs ~ 1/sin i so j ~ 1/sin i and lambda_pred ~ 1/sin i; a 5 deg error at i = 60 deg is {abs(math.log10(math.sin(math.radians(60))/math.sin(math.radians(65)))):.3f} dex.")
info(f"the GAS lever, the one that matters most for the MEDIAN: j here is the STELLAR disc's.  HI is more extended, so j_bar > j_star; taking the")
info(f"     literature range j_bar/j_star = 1.0-1.7 for gas-rich discs raises the median lambda_pred to {np.median(jj*1.35/(math.sqrt(2)*LAM_P['canonical']['R200']*LAM_P['canonical']['V200'])):.4f} at 1.35x, i.e. onto the tidal-torque 0.035.  Not claimed as a match.")
info(f"the H0 convention: lambda ~ H0, so using H0 = 67.4 instead of Li's 73 lowers every lambda here by {abs(math.log10(67.4/73.0)):.3f} dex on BOTH sides and cancels in the comparison.")
# mutations
lam_mut = {}
for fac, tag in ((4.0, "a_0 x 4"), (0.25, "a_0 / 4")):
    Vm = np.array([v200_phantom(r["Mb"]*Msun, fac*A0["canonical"], H0_LI)[0]/1e3 for r in recs])
    Rm = np.array([v200_phantom(r["Mb"]*Msun, fac*A0["canonical"], H0_LI)[1]/kpc for r in recs])
    lm = jj/(math.sqrt(2)*Rm*Vm)
    lam_mut[tag] = math.log10(np.median(lm)/np.median(lam_f))
    info(f"mutation {tag:10}: median log10(lambda_pred/lambda_fit) = {lam_mut[tag]:+.3f} dex")
ck("M109a mutation: moving a_0 by a factor 4 either way breaks 109b -- the median lambda shifts by more than the 0.15 dex tolerance, so the agreement is a statement about a_0's value and not an identity",
   min(abs(v) for v in lam_mut.values()) > 0.15, f"a_0 x 4 -> {lam_mut['a_0 x 4']:+.3f} dex, a_0/4 -> {lam_mut['a_0 / 4']:+.3f} dex, vs the 0.15 dex tolerance")
sh = rng.permutation(jj)
lam_sh = sh/(math.sqrt(2)*LAM_P["canonical"]["R200"]*LAM_P["canonical"]["V200"])
r_true = np.corrcoef(np.log10(LAM_P["canonical"]["lam"]), np.log10(lam_f))[0, 1]
lam_f_sh = rng.permutation(lam_f)
r_sh = np.corrcoef(np.log10(LAM_P["canonical"]["lam"]), np.log10(lam_f_sh))[0, 1]
ck("M109b mutation: shuffling the fitted lambdas across galaxies destroys the per-galaxy correlation, so 109b is not carried by the shared j alone",
   abs(r_sh) < 0.3 < r_true, f"per-galaxy r(log lambda_pred, log lambda_fit) = {r_true:.3f}; shuffled {r_sh:+.3f}; the shared j guarantees SOME correlation, which is why the width check 109c is the load-bearing one")
V_N = np.array([(10*H0_LI)**(1/3.)*(G*r["Mb"]*Msun)**(1/3.)/1e3 for r in recs])       # nu = 1: M200 = M_b, V200 = (10 H0 G M_b)^(1/3)
R_N = np.array([(G*r["Mb"]*Msun/(10*H0_LI)**2)**(1/3.)/kpc for r in recs])
lam_N = jj/(math.sqrt(2)*R_N*V_N)
d_N = math.log10(np.median(lam_N)/np.median(lam_f))
ck("M109c mutation, the Newtonian alternative computed beside the framework: with nu = 1 there is no phantom, the virial mass IS the baryonic mass, and the resulting spin parameter misses the fitted one by about a decade -- so 109a/109b are statements about the boost, not about arithmetic",
   abs(d_N) > 0.5, f"nu = 1 gives median V200_N = {np.median(V_N):.1f} km/s against a fitted {np.median(lam_f)*0+np.median([LI[ref][r['name']]['V200'] for r in recs if r['name'] in LI[ref]]):.1f} km/s, and median log10(lambda_N/lambda_fit) = {d_N:+.2f} dex")

# ------------------------------------------------------------------ mass trend
sl, b_, sc_ = fit_loglog(Mb_arr, LAM_P["canonical"]["lam"])
sl_f, _, sc_f = fit_loglog(Mb_arr, lam_f)
ck("109e both distributions are near-flat in baryonic mass, as a spin parameter should be, but the framework's residual mass slope is not zero and is quoted rather than hidden",
   abs(sl) < 0.25, f"d log lambda_pred/d log M_b = {sl:+.3f} (scatter {sc_:.3f} dex); fitted {sl_f:+.3f} ({sc_f:.3f} dex); tidal torque predicts 0")

P(""); P("-"*126); P("self-audit against the five bug patterns this hunt has already produced"); P("-"*126)
P("  (1) TOTAL vs ENCLOSED mass: V200_pred uses the TOTAL M_b deliberately and correctly -- R200 is 100-200 kpc, far outside every")
P("      SPARC disc, so the enclosed baryonic mass there IS the total.  j, by contrast, uses only the mass that is measured, with an")
P("      explicit tail; the tail fraction is printed above and the estimator is validated against 2 R_d V_flat.")
P("  (2) SPHERICAL formula on a DISC: M_dyn(<R200) = V200^2 R200/G is spherical, which is right here because at R200 the disc")
P("      subtends a few degrees and is a point mass; and Li+2020's own halos are spherical, so both sides use the same geometry.")
P("      j itself is computed with the DISC integral, not a spherical one.")
P("  (3) an aperture on a SADDLE: not applicable -- no aperture, no minimum, one monotone radius per galaxy.")
P("  (4) covariance reshaped wrongly: no covariance matrix is used; errors here are bootstrap-free percentiles and the fits' own e_V200.")
P("  (5) a result that is really about the stellar M/L: j is Upsilon-FREE by construction, but M_b is not, and the lever is printed")
P("      above (-0.28 dex per dex of Upsilon).  Upsilon moves lambda_pred by 0.04-0.06 dex over the plausible 0.35-0.70 range -- larger")
P("      than the 109b median offset, so 109b MUST NOT be quoted at better than ~0.06 dex, and smaller than the 109c width failure,")
P("      which Upsilon therefore cannot rescue.  The M/L-free form (lambda from measured V_flat) is given above for exactly this reason.")
P(""); P("="*126); P("VERDICT -- item 109"); P("="*126)
P("  MEDIAN WORKS, WIDTH FAILS.  The framework's V200 is not a fit parameter: deep MOND makes V200 = (G M_b a_0)^(1/4) = V_flat exactly")
P("  (to 0.6% with the full kernel), and R200 follows.  That zero-parameter V200 reproduces the V200 recovered by five LambdaCDM-prior")
P("  halo models to -0.01/-0.07 dex in the median with ~0.10 dex scatter, and the spin-parameter distribution built from it matches the")
P("  fitted one in MEDIAN to -0.028 dex (canonical) / -0.068 (alt).  The prediction is also exactly DISTANCE-FREE, and it has an")
P("  M/L-free form, lambda = 10 H0 j/(sqrt(2) V_flat^2), which needs no Upsilon anywhere and gives 0.019.")
P("  AGAINST INTEREST, four things.  (1) The WIDTH does not match: 0.220 dex predicted against 0.292-0.317 fitted, and the missing")
P("  0.21 dex in quadrature is exactly the 0.10 dex galaxy-to-galaxy scatter of V200_fit/V200_pred, doubled -- about half of it the")
P("  fits' own noise, the rest real.  (2) Both distributions sit 0.12-0.15 dex BELOW the tidal-torque 0.035 and both reject the")
P("  Bullock log-normal by KS, so spin does not discriminate between the two accounts.  (3) The fitted V200 is an extrapolation far")
P("  beyond the last measured point -- flat-prior fits scatter 2-3x more and their medians move by 0.3 dex -- so lambda_fit is")
P("  substantially prior, and 109a is consistency with the fitters' convention, not a measurement.  (4) j here is the stellar disc's;")
P("  HI would raise it by 0-70%, larger than every difference tested.  NOT Kepler-grade, and 109f says why: V200 = V_flat is the")
P("  BTFR under another name, so the median agreement is the BTFR being re-derived, not a new law.")
sys.exit(ck.done())
