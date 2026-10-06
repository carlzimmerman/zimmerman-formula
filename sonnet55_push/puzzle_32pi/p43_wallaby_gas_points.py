"""p43: the Upsilon-free gas-point a0 (p41b/p42 method) on WALLABY DR2 kinematic models + AllWISE W1 stars.
Data (outside the repo, ../_external_data/wallaby_dr2/, fetch log data_assembly/wallaby_dr2/FETCH_LOG.md): kinematic catalogue (Rad, Vrot_model, e_Vrot_model, Rad_SD,
SD_FO_model in Msun/pc^2 face-on HI), source catalogue (dist_h, Hubble-flow, H0 = 70), AllWISE nearest match (w1gmag if present else w1mpro).
Model per galaxy: best-quality (QFlag 0) model with the most radii. Gas = 1.33 x HI, thin disc by exact ring summation (control: analytic Freeman disc).
Stars: exponential thin disc, L_W1 from M_sun,W1 = 3.24, Upsilon_W1 = 0.6 nominal; R_d = r_2mass/3.5 if a 2MASS size exists, else the size-mass relation
log R_d[kpc] = 0.33 (log M* - 10) + 0.45 (crude; its effect is tested by x0.5 / x2). Distances rescaled to H0 = 73 (SPARC's Hubble-flow scale); H0 = 70 also reported.
Gas points: gas > 80% of g_bar at nominal Upsilon. Fit: framework kernel, log g chi2 with sigma_obs + 0.11 dex, a0 profiled; Upsilon sensitivity (0.3/0.6/0.9);
galaxy bootstrap. Compared with SPARC's gas-point a0 = 9.00e-11 (p41b) and the footings.
Run: python3 p43_wallaby_gas_points.py [NBOOT]  |  MUTATE=1: gas surface densities x2 (check C, the Freeman control, still passes; check W must move > 15%)
"""
import csv, math, os, sys
import numpy as np
from scipy.special import ellipk, i0, i1, k0, k1
MUTATE = os.environ.get("MUTATE") == "1"
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 200
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DD = os.path.join(os.path.dirname(REPO), "_external_data", "wallaby_dr2")
G = 4.30091e-6          # kpc (km/s)^2 / Msun
KMS2KPC_TO_MS2 = 1e6 / 3.0857e19
# ---------------------------------------------------------------- thin-disc rotation from a surface-density profile (ring summation)
def v2_disc(R_eval, r_prof, sig_prof, rmax_fac=1.5, nring=600):
    """Sigma in Msun/kpc^2 on radii r_prof (kpc); linear interpolation, exponential extrapolation beyond the last point to rmax_fac x last radius."""
    rlast = r_prof[-1]; rr = np.linspace(0, rmax_fac * rlast, nring + 1); a = 0.5 * (rr[1:] + rr[:-1]); da = np.diff(rr)
    sig = np.interp(a, r_prof, sig_prof)
    if len(r_prof) >= 3 and sig_prof[-1] > 0 and sig_prof[-2] > sig_prof[-1]:
        h = (r_prof[-1] - r_prof[-2]) / math.log(sig_prof[-2] / sig_prof[-1])
        out = a > rlast; sig[out] = sig_prof[-1] * np.exp(-(a[out] - rlast) / h)
    else:
        sig[a > rlast] = 0.0
    m = 2 * math.pi * a * da * sig
    v2 = np.zeros_like(R_eval, dtype=float)
    for j, R in enumerate(R_eval):
        def phi(Rx):
            k2 = 4 * a * Rx / (a + Rx)**2
            return np.sum(-2 * G * m / math.pi * ellipk(np.minimum(k2, 1 - 1e-12)) / (a + Rx))
        dR = 1e-3 * R
        v2[j] = R * (phi(R + dR) - phi(R - dR)) / (2 * dR)
    return v2
# control: Freeman exponential disc
Rd, M = 2.0, 1e10; rp = np.linspace(0.01, 12 * Rd, 400); sp = M / (2 * math.pi * Rd**2) * np.exp(-rp / Rd)
Rt = np.array([1.0, 2.0, 4.4, 8.0]); y = Rt / (2 * Rd)
vf = 4 * math.pi * G * (M / (2 * math.pi * Rd**2)) * Rd * y**2 * (i0(y) * k0(y) - i1(y) * k1(y))
vn = v2_disc(Rt, rp, sp, rmax_fac=1.0)
check(f"C thin-disc ring summation reproduces the Freeman disc within 2% (max {100*np.max(np.abs(vn/vf-1)):.2f}%)", np.max(np.abs(vn / vf - 1)) < 0.02)
# ---------------------------------------------------------------- data
kin = list(csv.DictReader(open(os.path.join(DD, "wallaby_dr2_kinematic_catalogue.csv"))))
src = {r["name"]: r for r in csv.DictReader(open(os.path.join(DD, "wallaby_dr2_source_catalogue.csv")))}
wise = {r["wallaby_name"]: r for r in csv.DictReader(open(os.path.join(DD, "allwise_wallaby_dr2.csv")))}
GX = {("WALLABY " + r["name"]): r for r in csv.DictReader(l for l in open(os.path.join(REPO, "prep_2026", "wallaby_firing", "gext_wallaby_237.csv")) if not l.startswith("#"))}
arr = lambda s: np.array([float(x) for x in s.split(",")]) if s else np.array([])
best = {}
for r in kin:
    if r["QFlag_model"] not in ("0.0", "0"): continue
    n = len(arr(r["Rad"]))
    if r["name"] not in best or n > len(arr(best[r["name"]]["Rad"])): best[r["name"]] = r
def flt(x):
    try: return float(x)
    except Exception: return float("nan")
def build(H0=73.0, ups=0.6, rdfac=1.0, sigfac=1.0, fluxcorr=True, sig_ad=0.0, dist="hubble"):
    gals = []
    for nm, r in best.items():
        s, w = src.get(nm), wise.get(nm)
        if s is None or w is None: continue
        D = flt(s["dist_h"]) * 70.0 / H0
        gx = GX.get(nm)
        if dist == "cmb" and gx is not None: D = flt(gx["D_mpc"]) * 73.0 / H0
        if flt(r["Inc_model"]) < 30: continue
        fc = 10**(flt(s["log_m_hi_corr"]) - flt(s["log_m_hi"])) if fluxcorr and np.isfinite(flt(s.get("log_m_hi_corr", "nan"))) else 1.0
        m1 = flt(w["w1gmag"]) if np.isfinite(flt(w["w1gmag"])) else flt(w["w1mpro"])
        if not (np.isfinite(D) and D > 0 and np.isfinite(m1)): continue
        kpc_as = D * 1e3 / 206264.806
        R = arr(r["Rad"]) * kpc_as; V = arr(r["Vrot_model"]); eV = np.maximum(arr(r["e_Vrot_model"]), 2.0)
        rS = arr(r["Rad_SD"]) * kpc_as; S = arr(r["SD_FO_model"]) * 1e6 * 1.33 * sigfac * fc * (2.0 if MUTATE else 1.0)
        if len(R) < 3 or len(rS) < 3: continue
        Mstar = ups * 10**(-0.4 * (m1 - 5 * math.log10(D * 1e6) + 5 - 3.24))
        r2 = flt(w["r_2mass"])
        Rd = (r2 * kpc_as / 3.5) if (np.isfinite(r2) and r2 > 0) else 10**(0.33 * (math.log10(Mstar) - 10) + 0.45)
        Rd *= rdfac
        ok = (R > 0) & (V > 0)
        R, V, eV = R[ok], V[ok], eV[ok]
        if sig_ad > 0:                                   # asymmetric drift: V_c^2 = V^2 + sigma^2 R/h_HI, h_HI = last SD radius / 3.5
            V = np.sqrt(V**2 + sig_ad**2 * R / (rS[-1] / 3.5))
        vg2 = v2_disc(R, rS, S)
        yy = R / (2 * Rd)
        vs2 = 4 * math.pi * G * (Mstar / (2 * math.pi * Rd**2)) * Rd * yy**2 * (i0(yy) * k0(yy) - i1(yy) * k1(yy))
        gext = {b: (flt(gx[f"g_{b}_ms2"]) if gx is not None else float("nan")) for b in ("noclu", "maxclu")}
        near = (gx is not None and np.isfinite(flt(gx["sep_attr_mpc"])) and flt(gx["sep_attr_mpc"]) < 15)
        gals.append(dict(name=nm, R=R, V=V, eV=eV, vg2=vg2, vs2=vs2, Mstar=Mstar, gext=gext, near=near, field=(gx["field"] if gx is not None else "?")))
    return gals
def gas_points(gals, ups_scale=1.0, fcut=0.8):
    P = []
    for g in gals:
        vb2 = g["vg2"] + g["vs2"]
        fg = np.where(vb2 > 0, g["vg2"] / np.where(vb2 > 0, vb2, 1), 0)
        m = (fg > fcut) & (g["vg2"] > 0)
        if m.sum() >= 2:
            gb = (g["vg2"][m] + ups_scale * g["vs2"][m]) / g["R"][m] * KMS2KPC_TO_MS2
            go = g["V"][m]**2 / g["R"][m] * KMS2KPC_TO_MS2
            sg = (2 * g["eV"][m] / g["V"][m]) / math.log(10)
            P.append((g["name"], gb, go, sg, g["gext"], g["near"]))
    return P
A = np.exp(np.linspace(math.log(0.3e-10), math.log(3.0e-10), 121))
def gpred(gb, a, ge):
    """framework EFE cubic (equation book E7): g^2 - gb^2 = a gb g/(g + sqrt2 ge); ge = 0 gives g = gb sqrt(1 + a/gb). Solved by fixed-point/Newton per point."""
    g = gb * np.sqrt(1 + a / gb)
    if not np.isfinite(ge) or ge <= 0: return g
    e = math.sqrt(2) * ge
    for _ in range(60):
        f = g**2 - gb**2 - a * gb * g / (g + e); fp = 2 * g - a * gb * e / (g + e)**2
        g = np.maximum(g - f / fp, gb)
    return g
def fit(P, sint=0.11, efe=None):
    ch = np.zeros_like(A)
    for _, gb, go, sg, gx, near in P:
        ge = gx[efe] if efe else float("nan")
        for i, a in enumerate(A):
            pred = gpred(gb, a, ge)
            ch[i] += np.sum((np.log10(go) - np.log10(pred))**2 / (sg**2 + sint**2))
    i = int(np.argmin(ch)); lo, hi = max(0, i - 6), min(len(A), i + 7)
    p = np.polyfit(np.log(A[lo:hi]) - math.log(A[i]), ch[lo:hi], 2)
    return math.exp(math.log(A[i]) - p[1] / (2 * p[0]))
gals = build()
P = gas_points(gals)
npts = sum(len(p[1]) for p in P)
ys = np.concatenate([p[1] for p in P]) / 9.36e-11 if P else np.array([np.nan])
print(f"   WALLABY: {len(best)} galaxies with QFlag 0; {len(gals)} with distance + WISE; gas-dominated points: {npts} in {len(P)} galaxies; y median {np.median(ys):.3f}")
a_nom = fit(P)
sens = [fit(gas_points(gals, s)) for s in (0.5, 1.0, 1.5)]          # Upsilon 0.3 / 0.6 / 0.9
rd = [fit(gas_points(build(rdfac=f))) for f in (0.5, 2.0)]
h70 = fit(gas_points(build(H0=70.0)))
rng = np.random.default_rng(43); B = []
for _ in range(NB):
    Pb = [P[i] for i in rng.integers(0, len(P), len(P))]
    B.append(fit(Pb))
lo, hi = np.percentile(B, [16, 84]); err = (hi - lo) / 2 / a_nom
print(f"   a0 (gas points, H0 73) = {a_nom:.3e}  (68% {lo:.3e}-{hi:.3e}, +-{100*err:.1f}% stat, {len(P)} galaxies)")
print(f"   Upsilon 0.3/0.6/0.9: {sens[0]:.3e} / {sens[1]:.3e} / {sens[2]:.3e} (spread {100*(max(sens)/min(sens)-1):.1f}%);  R_d x0.5 / x2: {rd[0]:.3e} / {rd[1]:.3e};  H0 70: {h70:.3e}")
print(f"   vs SPARC gas points 9.00e-11: {100*(a_nom/9.00e-11-1):+.1f}%;  vs 9.3603e-11 {100*(a_nom/9.3603e-11-1):+.1f}%;  vs 1.1312e-10 {100*(a_nom/1.1312e-10-1):+.1f}%;  vs 1.061e-10 {100*(a_nom/1.061e-10-1):+.1f}%")
efe_n, efe_m = fit(P, efe="noclu"), fit(P, efe="maxclu")
nofc = fit(gas_points(build(fluxcorr=False))); ad8 = fit(gas_points(build(sig_ad=8.0))); cmb = fit(gas_points(build(dist="cmb")))
Pnear = [p for p in P if p[5]]; Pfar = [p for p in P if not p[5]]
a_near = fit(Pnear) if len(Pnear) >= 3 else float("nan"); a_far = fit(Pfar) if len(Pfar) >= 3 else float("nan")
print(f"   EFE (framework cubic, per-galaxy g_ext): noclu {efe_n:.3e}, maxclu {efe_m:.3e}  (vs isolated {a_nom:.3e}: {100*(efe_m/a_nom-1):+.1f}% at maxclu)")
print(f"   flux scale uncorrected: {nofc:.3e};  asymmetric drift 8 km/s: {ad8:.3e};  CMB-frame distances (table, /73): {cmb:.3e}")
print(f"   near a cluster/group (<15 Mpc 3D): {len(Pnear)} galaxies, a0 {a_near:.3e};  field: {len(Pfar)} galaxies, a0 {a_far:.3e}")
check(f"U the WALLABY gas-point a0 is Upsilon-insensitive (spread {100*(max(sens)/min(sens)-1):.1f}% < 12%)", max(sens) / min(sens) < 1.12)
check(f"W WALLABY and SPARC gas-point a0 agree within the combined statistical error ({100*abs(a_nom/9.0e-11-1):.1f}% vs {100*math.hypot(err, 0.11):.1f}%)",
      abs(math.log(a_nom / 9.0e-11)) < math.hypot(err, 0.11))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
