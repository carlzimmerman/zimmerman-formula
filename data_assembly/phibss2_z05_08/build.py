#!/usr/bin/env python3
"""Parse Tables 1-4 of PHIBSS2 z=0.5-0.8 (Freundlich+2019, A&A 622, A105; arXiv:1812.08180) from its arXiv HTML page (fetched 2026-09-29; copy + sha256 in raw_small/, manifest.json).
Table 1 sample (optical position, z, morphology, M*, SFR); Table 2 CO observation (beam, z offset, CO peak, rms, FWHM of a single-Gaussian fit to the spatially integrated spectrum and its error);
Table 3 CO(2-1) flux, S/N, L'_CO, M_gas (alpha_CO = 4.36 Msun/(K km/s pc^2) Galactic, x1.36 helium, r21 = 0.77, +-50% systematic), mu_gas, f_gas, t_depl; Table 4 HST I-band sizes (single Sersic and two-component disc and bulge half-light radii, B/T).
Flags: a star marks a marginal detection and a dagger a non-detection.  No velocity, baryonic mass or acceleration is computed here.
Checks: 61 rows; mu = M_gas/M*, f_gas = mu/(1+mu), t_depl = M_gas/SFR recomputed from the table columns; L'_CO recomputed from F(CO) with the paper's Eq. 2 (assumed Planck18).
"""
import csv, hashlib, html, json, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "raw_small", "arxiv_1812.08180_html_fetched_2026-09-29.html")
LOG = []
def check(c, m):
    LOG.append(("PASS  " if c else "FAIL  ") + m); print(LOG[-1])
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)
s = open(SRC, errors="ignore").read()
def flat(x):
    x = re.sub(r'<math[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: " [" + html.unescape(m.group(1)) + "] ", x, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
def table(tid):
    i = s.index('<table id="%s"' % tid); j = s.index("</table>", i)
    return [[flat(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)] for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], flags=re.S)]
def num(x):
    x = x.replace("−", "-"); m = re.search(r"-?\d+\.?\d*(?:[Ee][+-]?\d+)?", x); return float(m.group(0)) if m else None
def flag(x): return ("marginal" if "⋆" in x else "") + ("nondetection" if "†" in x else "")
T = {k: [r for r in table(t) if r and re.fullmatch(r"\d+", r[0])] for k, t in (("t1", "S3.T1.1"), ("t2", "S3.T2.1"), ("t3", "S3.T3.1"), ("t4", "S3.T4.1"))}
for k in T: check(len(T[k]) == 61, f"{k}: 61 rows")
rows = []
for a, b, c, d in zip(T["t1"], T["t2"], T["t3"], T["t4"]):
    check(a[1] == b[1] == c[1] == d[1] and a[0] == b[0] == c[0] == d[0], f"row {a[0]} ({a[1]}): IDs agree across the four tables")
    beam = re.findall(r"(\d+\.?\d*)", b[6])
    rows.append(dict(num=int(a[0]), id=a[1], field=a[2], source=re.sub(r"[⋆†]", "", a[3]).strip(), ra=a[4], dec=a[5], z_optical=num(a[6]), morphology=a[7],
        Mstar_Msun=num(a[8]), SFR_Msun_yr=num(a[9]), sSFR_Gyr=num(a[10]),
        config=b[4], t_int_hr=num(b[5]), beam_major_arcsec=float(beam[0]) if len(beam) > 1 else None, beam_minor_arcsec=float(beam[1]) if len(beam) > 1 else None,
        dz_CO_minus_optical=num(b[7]), dRA_arcsec=num(b[8]), dDEC_arcsec=num(b[9]), CO_peak_mJy=num(b[10]), rms_30kms_mJy=num(b[11]), CO_FWHM_kms=num(b[12]), CO_FWHM_err_kms=num(b[13]),
        F_CO_Jykms=num(c[4]), dF_CO_Jykms=num(c[5]), SN_CO=num(c[6]), Lprime_CO21=num(c[7]), Mgas_Msun=num(c[8]), mu_gas=num(c[9]), f_gas=num(c[10]), t_depl_Gyr=num(c[11]),
        R_Sersic_kpc=num(d[4]), n_Sersic=num(d[5]), q_Sersic=num(d[6]), sersic_single_better=int("+" in d[5]), R_d_halflight_kpc=num(d[7]), R_b_halflight_kpc=num(d[8]), BT=num(d[9]),
        flag=flag(a[3] + b[3] + c[3] + d[3]) or "detection"))
check(all(r["Mstar_Msun"] and r["Mgas_Msun"] is not None for r in rows), "every row has M* and M_gas")
nd = [r for r in rows if r["flag"] == "nondetection"]; mg = [r for r in rows if r["flag"] == "marginal"]
LOG.append(f"flags: {len(mg)} marginal, {len(nd)} non-detection, {61 - len(mg) - len(nd)} detections"); print(LOG[-1])
bad = [(r["id"], round(r["Mgas_Msun"] / r["Mstar_Msun"], 3), r["mu_gas"]) for r in rows if r["mu_gas"] is not None and abs(r["Mgas_Msun"] / r["Mstar_Msun"] - r["mu_gas"]) > 0.006 + 0.05 * r["mu_gas"]]
check(not bad, f"mu_gas = M_gas/M* within the table rounding (0.006 + 5%; exceptions {bad[:5]})")
bad = [(r["id"], r["f_gas"]) for r in rows if r["mu_gas"] is not None and r["f_gas"] is not None and abs(r["mu_gas"] / (1 + r["mu_gas"]) - r["f_gas"]) > 0.015]
check(not bad, f"f_gas = mu/(1+mu) within 0.015 (exceptions {bad[:5]})")
bad = [(r["id"], round(r["Mgas_Msun"] / r["SFR_Msun_yr"] / 1e9, 2), r["t_depl_Gyr"]) for r in rows if r["t_depl_Gyr"] is not None and abs(r["Mgas_Msun"] / r["SFR_Msun_yr"] / 1e9 - r["t_depl_Gyr"]) > 0.06 + 0.1 * r["t_depl_Gyr"]]
check(not bad, f"t_depl = M_gas/SFR within the table rounding (0.06 Gyr + 10%; exceptions {bad[:5]})")
from astropy.cosmology import Planck18 as C
worst = 0; badL = []
for r in rows:
    if r["F_CO_Jykms"] and r["Lprime_CO21"]:
        z = r["z_optical"] + (r["dz_CO_minus_optical"] or 0); dl = C.luminosity_distance(z).to("Mpc").value
        L = 3.25e7 / (1 + z) * r["F_CO_Jykms"] * 230.538 ** -2 * dl ** 2; d = abs(L / r["Lprime_CO21"] - 1); worst = max(worst, d)
        if d > 0.12: badL.append((r["id"], round(L / r["Lprime_CO21"], 3)))
check(not badL, f"L'_CO recomputed from F(CO) (Eq. 2, Planck18) within 12% (the table rounds to 2 significant digits) for every row (worst {worst:.3f}; exceptions {badL[:5]})")
def alpha_eq45(z, mstar):
    lz1 = math.log10(1 + z); b = 10.4 + 4.46 * lz1 - 1.78 * lz1 ** 2
    logZ = 8.74 - 0.087 * (math.log10(mstar) - b) ** 2
    return 4.36 * math.sqrt(0.67 * math.exp(0.36 * 10 ** (8.67 - logZ)) * 10 ** (-1.27 * (logZ - 8.67)))
al = []; badA = []
for r in rows:
    if r["Lprime_CO21"] and r["Mgas_Msun"]:
        eff = r["Mgas_Msun"] * 0.77 / r["Lprime_CO21"]; pred = alpha_eq45(r["z_optical"], r["Mstar_Msun"])
        r["alpha_CO_effective_from_table"] = round(eff, 3); r["alpha_CO_eq4_5_predicted"] = round(pred, 3); al.append(eff)
        if abs(eff / pred - 1) > 0.15: badA.append((r["id"], round(eff / pred, 3)))
check(not badA, f"alpha_CO,eff = M_gas x r21 / L' (r21 = 0.77) equals the paper's Eq. 4-5 metallicity-dependent alpha_CO within 15% for every row (exceptions {badA[:5]}); mean alpha_eff = {sum(al) / len(al):.2f} (paper: mean 4.0 +- 0.3)")
LOG.append("NOTE: Table 3's footnote d says alpha_CO = 4.36 with a 1.36 helium factor, but the table values follow M_gas = alpha_CO(Z) L'/0.77 with alpha_CO from Eq. 4-5 (which already includes helium, per the text); the footnote is not the recipe the numbers follow"); print(LOG[-1])
with open(os.path.join(HERE, "phibss2_z05_08.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(dict(source_html_sha256=hashlib.sha256(open(SRC, "rb").read()).hexdigest(), url="https://arxiv.org/html/1812.08180", fetched="2026-09-29"), open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
