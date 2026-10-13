#!/usr/bin/env python3
"""CFG711 (criteria 60d8c7737): does the law predict each SLACS lens's total density slope from its light?
Auger+2010 Table 1 (paper TeX). Per lens: Hernquist stars + the law (record nu_mono via its h table), M* normalised to the lensing
M(<re/2) (projected); isotropic Jeans sigma in aperture re/2; gamma'_pred via Auger's power-law mapping. Both footings.
kappa = 1/2 FITTED; cold energy mass required; not theory closed."""
import os, sys, io, re, json, math, contextlib
import numpy as np
from scipy.optimize import brentq
from scipy.special import gamma as Gf
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
MUT = os.environ.get("CFG711_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
G, MSUN, KPC = C4.G_SI, C4.MSUN, C4.KPC
TEX = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data", "slacs_auger2010", "T_lens_data.tex")
OUT, RES = [], {"lane": "CFG711", "criteria": "60d8c7737", "mutate": MUT}
P = lambda s: (print(s, flush=True), OUT.append(str(s)))

# ------------------------------------------------------------------ parse Auger+2010 Table 1
rows = []
for line in open(TEX):
    if not line.strip().startswith("SDSSJ"): continue
    cells = [c.strip() for c in line.split("&")]
    num = lambda s: [float(x) for x in re.findall(r"-?\d+\.\d+|-?\d+", s.replace("\\phantom{0}", "").replace("\\phantom{-}", ""))]
    name = re.sub(r"\$|\\dagger|-|\+", lambda m: {"-": "-", "+": "+"}.get(m.group(0), ""), cells[0])
    re_kpc = num(cells[1])[0]; sig, esig = num(cells[2])[:2]
    lMc = num(cells[3])[0]; lMs = num(cells[4])[0]; lMe2, elMe2 = num(cells[5])[:2]
    g, eg = num(cells[8].rstrip("\\").strip())[:2]
    rows.append(dict(name=name, re=re_kpc, sig=sig, esig=esig, lMc=lMc, lMs=lMs, lMe2=lMe2, elMe2=elMe2, g=g, eg=eg,
                     dagger="dagger" in cells[0]))
P(f"Auger+2010 Table 1 rows parsed: {len(rows)}")

def hcol(y):
    return np.interp(np.log10(np.maximum(y, 1e-14)), C4._KNS["LYG"], C4._KNS["_HM"])

X = np.logspace(-3, np.log10(300), 1500)          # radii in units of r_e

def law_model(re_m, Mstar, a0):
    a = re_m / 1.8153; r = X * re_m
    Ms = Mstar * r ** 2 / (r + a) ** 2
    gN = G * Ms / r ** 2
    g = gN + (a0 * hcol(gN / a0) if a0 > 0 else 0.0)
    return r, g * r ** 2 / G, a                   # 3-D total enclosed mass (kg)

def proj_mass(r, M, R):
    """projected mass inside R from a spherical M(r): M(<R) + shells outside weighted by 1 - sqrt(1 - R^2/r^2)"""
    rho4pi_r2 = np.gradient(M, r)
    w = np.where(r > R, 1 - np.sqrt(np.clip(1 - (R / r) ** 2, 0, 1)), 1.0)
    return float(np.trapz(rho4pi_r2 * w, r))

def sigma_ap(r, M, a, Rap):
    """isotropic Jeans, Hernquist tracer, luminosity-weighted LOS dispersion inside aperture Rap"""
    nu = a / (r * (r + a) ** 3)
    integrand = nu * G * M / r ** 2
    cum = np.concatenate([np.cumsum((0.5 * (integrand[1:] + integrand[:-1]) * np.diff(r))[::-1])[::-1], [0.0]])
    p = cum                                         # nu sigma_r^2 (r) = int_r^inf nu G M / r^2
    # aperture-weighted: sigma_ap^2 = [int over sphere and cylinder] -> use the identity for luminosity-weighted dispersion in a
    # cylinder: int_0^Rap 2 pi R Sigma sigma_los^2 dR = int_0^inf 4 pi r^2 p(r) f(r) dr, f = fraction of the shell inside the cylinder,
    # with isotropy (3 equal components) f-weighted -- computed numerically by projecting p and nu on the same shells.
    w = np.where(r > Rap, 1 - np.sqrt(np.clip(1 - (Rap / r) ** 2, 0, 1)), 1.0)
    num_ = np.trapz(4 * math.pi * r ** 2 * p * w, r)
    den_ = np.trapz(4 * math.pi * r ** 2 * nu * w, r)
    return math.sqrt(num_ / den_)

def pl_sigma(re_m, Mproj_e2, gam, a, Rap):
    """power-law total density with projected mass Mproj_e2 inside re/2; same tracer/aperture"""
    k = 2 * Gf(gam / 2) / (math.sqrt(math.pi) * Gf((gam - 1) / 2))          # M3D(r)/Mproj(R=r) for a power law
    r = X * re_m; R2 = re_m / 2
    M = k * Mproj_e2 * (r / R2) ** (3 - gam)
    return sigma_ap(r, M, a, Rap)

def predict(L, a0):
    re_m = L["re"] * KPC; Me2 = 10 ** L["lMe2"] * MSUN
    f = lambda lm: proj_mass(*law_model(re_m, 10 ** lm * MSUN, a0)[:2], re_m / 2) / Me2 - 1
    lo, hi = 8.0, 13.5
    if f(lo) > 0 or f(hi) < 0: return None
    lMs = brentq(f, lo, hi, xtol=1e-4)
    r, M, a = law_model(re_m, 10 ** lMs * MSUN, a0)
    sp = sigma_ap(r, M, a, re_m / 2)
    gfun = lambda gm: pl_sigma(re_m, Me2, gm, a, re_m / 2) - sp
    try:
        gp = brentq(gfun, 1.2, 2.95, xtol=1e-4)
    except ValueError:
        gp = float("nan")
    yE = float(np.interp(re_m / 2, r, G * (10 ** lMs * MSUN) * r ** 2 / (r + a) ** 2 / r ** 2) / a0) if a0 > 0 else float("inf")
    return dict(lMstar=lMs, sig_pred=sp / 1e3, gam_pred=gp, gN_over_a0_at_re2=yE)

for foot, a0v in C4.A0.items():
    a0 = 1e-30 if MUT else a0v
    out = []
    for L in rows:
        p = predict(L, a0)
        if p is None: continue
        out.append({**L, **p})
    ok = [o for o in out if math.isfinite(o["gam_pred"])]
    gp = np.array([o["gam_pred"] for o in ok]); go = np.array([o["g"] for o in ok]); eg = np.array([o["eg"] for o in ok])
    sp = np.array([o["sig_pred"] for o in ok]); so = np.array([o["sig"] for o in ok])
    d = gp - go
    rng = np.random.default_rng(711); bs = [np.median(rng.choice(d, d.size)) for _ in range(4000)]
    med, smed = float(np.median(d)), float(np.std(bs))
    rho, pval = spearmanr(gp, go)
    rms_law = float(np.sqrt(np.mean((go - gp) ** 2))); rms_mean = float(np.sqrt(np.mean((go - go.mean()) ** 2)))
    T1 = "CONSISTENT" if abs(med) <= 0.10 else ("INCONSISTENT" if (abs(med) > 0.20 and abs(med) > 3 * smed) else "TENSION")
    T2 = "PREDICTIVE" if (rho > 0 and pval < 0.01) else ("NOT PREDICTIVE" if pval >= 0.05 or rho <= 0 else "WEAK")
    imf = np.array([o["lMstar"] for o in ok]); lc = np.array([o["lMc"] for o in ok]); ls = np.array([o["lMs"] for o in ok])
    RES[foot] = dict(n=len(ok), n_parsed=len(rows), median_dgamma=med, boot_sigma=smed, T1=T1, spearman_rho=float(rho), spearman_p=float(pval),
                     T2=T2, rms_obs_minus_law=rms_law, rms_obs_minus_mean=rms_mean, median_dlogsigma=float(np.median(np.log10(sp / so))),
                     median_gam_pred=float(np.median(gp)), median_gam_obs=float(np.median(go)),
                     median_logM_law_minus_chab=float(np.median(imf - lc)), median_logM_law_minus_salp=float(np.median(imf - ls)),
                     per_lens=[dict(name=o["name"], gam_obs=o["g"], gam_err=o["eg"], gam_pred=o["gam_pred"], sig_obs=o["sig"], sig_pred=o["sig_pred"],
                                    lMstar_law=o["lMstar"], gN_a0=o["gN_over_a0_at_re2"]) for o in ok])
    P(f"== {foot}: n = {len(ok)} of {len(rows)}")
    P(f"  T1: median gamma'_pred - gamma'_obs = {med:+.3f} +- {smed:.3f} -> {T1}  (median pred {np.median(gp):.3f}, obs {np.median(go):.3f})")
    P(f"  T2: Spearman rho = {rho:+.3f}, p = {pval:.2e} -> {T2}; rms(obs - law) {rms_law:.3f} vs rms(obs - mean) {rms_mean:.3f}")
    P(f"  median dlog sigma (pred - obs) {np.median(np.log10(sp/so)):+.3f}; implied log M* - SPS: Chabrier {np.median(imf-lc):+.2f}, Salpeter {np.median(imf-ls):+.2f}")

code = 0
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg711_results.json")))
    m1 = RES["canonical"]["median_gam_pred"] - base["canonical"]["median_gam_pred"]
    bite1 = m1 > 0.3
    # M2: shuffle r_e across lenses (canonical a0), Spearman must drop by > 0.2
    rng = np.random.default_rng(7110); perm = rng.permutation(len(rows))
    shuffled = [dict(L, re=rows[j]["re"]) for L, j in zip(rows, perm)]
    sh = [dict(o, **(predict(o, C4.A0["canonical"]) or {})) for o in shuffled]
    sh = [o for o in sh if "gam_pred" in o and math.isfinite(o["gam_pred"])]
    rho_sh = spearmanr([o["gam_pred"] for o in sh], [o["g"] for o in sh])[0]
    bite2 = (base["canonical"]["spearman_rho"] - rho_sh) > 0.2
    P(f"MUTATE M1 pure stars: median gamma'_pred {base['canonical']['median_gam_pred']:.3f} -> {RES['canonical']['median_gam_pred']:.3f} (+{m1:.3f}): {'BITES' if bite1 else 'DOES NOT BITE'}")
    P(f"MUTATE M2 shuffled r_e: rho {base['canonical']['spearman_rho']:+.3f} -> {rho_sh:+.3f}: {'BITES' if bite2 else 'DOES NOT BITE'}")
    code = 1 if (bite1 and bite2) else 0
json.dump(RES, open(os.path.join(HERE, f"cfg711_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg711{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(code)
