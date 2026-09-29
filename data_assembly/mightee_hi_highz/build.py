#!/usr/bin/env python3
"""Parse Tables 2 and 3 of MIGHTEE-HI z>0.25 (Jarvis+2025, arXiv:2506.11935) from its arXiv HTML page (fetched 2026-09-29; copy + sha256 in raw_small/, manifest.json).
Table 2: positions, redshift, HI line flux, log M_HI (SNR-a error and systematic in parentheses), three SNRs, W50 and inclination-corrected W50^c, inclination.
Table 3: BAGPIPES stellar masses and SFRs with and without far-IR data, radio 1.28 GHz flux.  No baryonic mass, velocity or a0 quantity is computed here: the paper defines
M_bar = M* + 1.4 M_HI and does not say in the text I read which stellar mass column enters its bTFR figure, so that choice is left to the calc thread.
Checks: 11 sources (ID11 has two counterparts a/b), W50c = W50/sin(i) within 8% for every row, log M_HI recomputed from the line flux within 0.15 dex (assumed Planck18 cosmology; the paper's own cosmology was not read).
"""
import csv, hashlib, html, json, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "raw_small", "arxiv_2506.11935_html_fetched_2026-09-29.html")
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
    m = re.search(r"-?\d+\.?\d*", x.replace("−", "-")); return float(m.group(0)) if m else None
def pm(x):
    m = re.search(r"(-?\d+\.?\d*)\s*(?:\[\\pm\]|\\pm|±)\s*\[?\s*(\d+\.?\d*)", x)
    return (float(m.group(1)), float(m.group(2))) if m else (num(x), None)
t2 = table("S4.T2.11"); t3 = table("S4.T3.9")
rows2 = [r for r in t2 if r and re.match(r"^\d+[ab]?", r[0]) and len(r) >= 12]
check(len(rows2) == 12, f"Table 2: 12 rows (ID1-10, 11a, 11b): {[r[0] for r in rows2]}")
rows3 = {r[0]: r for r in t3 if r and re.match(r"^\d+[ab]?", r[0]) and len(r) >= 7}
def hi_mass(row):
    return None
out = []
for r in rows2:
    rid = r[0].replace("†", "").strip(); ident = rid.replace("∗", "").strip()
    if r[4] == '"':   # ID11b shares 11a's line flux, mass and SNRs
        base = [x for x in out if x["id"] == "11a"][0]
        out.append(dict(base, id="11b", ra=r[1], dec=r[2], z=num(r[3]), W50_kms=None, W50_err=None, W50c_kms=pm(r[10])[0], W50c_err=pm(r[10])[1], incl_deg=pm(r[11])[0], incl_err=pm(r[11])[1], shared_with_11a=1))
        continue
    flux = pm(r[4]); mhi = re.search(r"(\d+\.\d+)\s*\[?\\?pm\]?\s*(\d+\.\d+)\s*\(\s*\[?\\?pm\s*(\d+\.\d+)", r[5])
    w50 = pm(r[9]); w50c = pm(r[10]); inc = pm(r[11])
    out.append(dict(id=ident, ra=r[1], dec=r[2], z=num(r[3]), line_flux_JyHz=flux[0], line_flux_err_JyHz=flux[1],
                    logMHI=float(mhi.group(1)), logMHI_err_SNRa=float(mhi.group(2)), logMHI_err_syst=float(mhi.group(3)),
                    snr_a=num(r[6]), snr_b=num(r[7]), snr_c=num(r[8]), W50_kms=w50[0], W50_err=w50[1], W50c_kms=w50c[0], W50c_err=w50c[1],
                    incl_deg=inc[0], incl_err=inc[1], shared_with_11a=0))
check(len(out) == 12, "12 parsed rows")
for o in out:
    r3 = rows3.get(o["id"] if o["id"] in rows3 else "", None)
    key = [k for k in rows3 if k.replace("∗", "").replace("†", "").strip() == o["id"]]
    r3 = rows3[key[0]] if key else None
    o["star_or_dagger_flag_table3"] = ("*" if key and "∗" in key[0] else "") + ("dagger" if key and "†" in key[0] else "")
    if r3:
        o["logMstar_withFarIR"], o["logMstar_withFarIR_err"] = pm(r3[1]) if r3[1] else (None, None)
        o["SFR_withFarIR"] = pm(r3[2])[0] if r3[2] else None
        o["logMstar_noFarIR"], o["logMstar_noFarIR_err"] = pm(r3[3]) if r3[3] else (None, None)
        o["SFR_noFarIR"] = pm(r3[4])[0] if r3[4] else None
        o["S1p28_uJy"], o["S1p28_err_uJy"] = pm(r3[5])
        o["SFR_radio"] = pm(r3[6])[0] if r3[6] else None
# checks
bad = [(o["id"], o["W50c_kms"], o["W50_kms"] / math.sin(math.radians(o["incl_deg"]))) for o in out if o["W50_kms"] and abs(o["W50c_kms"] / (o["W50_kms"] / math.sin(math.radians(o["incl_deg"]))) - 1) > 0.08]
check(not bad, f"W50c = W50/sin(i) within 8% for every row with both (exceptions: {bad})")
from astropy.cosmology import Planck18 as C
worst = 0
for o in out:
    if o["shared_with_11a"]: continue
    dl = C.luminosity_distance(o["z"]).to("Mpc").value
    nu_obs = 1.42040575e9 / (1 + o["z"])                          # Hz
    s_jykms = o["line_flux_JyHz"] * 2.99792458e5 / nu_obs        # Jy km/s
    m = 2.356e5 * dl**2 * s_jykms / (1 + o["z"])
    d = abs(math.log10(m) - o["logMHI"]); worst = max(worst, d); o["logMHI_recomputed_Planck18"] = round(math.log10(m), 3)
check(worst < 0.15, f"log M_HI recomputed from the line flux agrees with Table 2 within {worst:.3f} dex for all rows (assumed Planck18)")
fields = list(dict.fromkeys(k for o in out for k in o))
with open(os.path.join(HERE, "mightee_hi_highz.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(out)
json.dump(dict(source_html_sha256=hashlib.sha256(open(SRC, "rb").read()).hexdigest(), url="https://arxiv.org/html/2506.11935", fetched="2026-09-29"), open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
