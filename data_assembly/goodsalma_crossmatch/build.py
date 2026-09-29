#!/usr/bin/env python3
"""Cross-match the 22 KURVS-CDFS galaxies with the GOODS-ALMA 2.0 catalogue (Gomez-Guijarro+2022, arXiv:2106.13246).

Source: Tables 2 (blind, 44 sources) and 3 (prior-based, 44 sources) of the paper's arXiv HTML page, fetched 2026-09-29 (sha256 in manifest.json,
copy in raw_small/).  Parsed from the HTML table cells, not read by a summariser.  No download other than that one HTML page.
KURVS positions: ../arxiv_tables/kurvs_positions/kurvs_positions.csv (Table 1 of arXiv:2305.04382).
Outputs: goodsalma2_catalogue.csv (88 rows), kurvs_goodsalma_nearest.csv (per KURVS galaxy: nearest sources), checks.txt.
No gas mass, no conversion, no verdict.
"""
import csv, hashlib, html, json, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "raw_small", "arxiv_2106.13246_html_v_fetched_2026-09-29.html")
LOG = []


def check(c, m):
    LOG.append(("PASS  " if c else "FAIL  ") + m); print(LOG[-1])
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)


s = open(SRC, errors="ignore").read()
def txt(x): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
def num(x):
    m = re.match(r"\s*(-?\d+\.?\d*)", x); return float(m.group(1)) if m else None
def pm(x):
    m = re.match(r"\s*(-?\d+\.?\d*)\s*±.*?(\d+\.?\d*)\s*$", x)
    return (float(m.group(1)), float(m.group(2))) if m else (num(x), None)

cat = []
for tid, kind in (("S3.T2.4", "blind"), ("S3.T3.4", "prior")):
    i = s.index('<table id="%s"' % tid); j = s.index("</table>", i)
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], flags=re.S)
    for r in rows:
        c = [txt(x) for x in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)]
        if not c or not re.fullmatch(r"A2GS\d+", c[0]):
            continue
        flux, eflux = pm(c[7])
        cat.append(dict(table=kind, id=c[0], ra_deg=float(c[1]), dec_deg=float(c[2]), id_zf=c[3], z=num(c[4]), logMstar=num(c[5]),
                        snr_peak=num(c[6]), S1p1mm_mJy=flux, S1p1mm_err_mJy=eflux,
                        high_res=(c[9] if kind == "blind" else c[8]), low_res=(c[10] if kind == "blind" else c[9])))
n_blind = sum(r["table"] == "blind" for r in cat); n_prior = sum(r["table"] == "prior" for r in cat)
check(n_blind == 44 and n_prior == 44, f"88 sources parsed: {n_blind} blind + {n_prior} prior-based (the abstract says 44 + 44)")
ids = [int(r["id"][4:]) for r in cat]
check(sorted(ids) == list(range(1, 89)), "IDs A2GS1..A2GS88 all present once")
check(all(r["S1p1mm_mJy"] is not None and r["S1p1mm_err_mJy"] is not None for r in cat), "every row has flux and error")
check(all(52.9 < r["ra_deg"] < 53.4 and -28.0 < r["dec_deg"] < -27.6 for r in cat), "all positions inside the GOODS-S box")
blind = [r for r in cat if r["table"] == "blind"]
check(all(r["snr_peak"] >= 5 for r in blind) and sum(r["snr_peak"] >= 5 for r in blind) == 44, "blind table: all 44 sources have S/N_peak >= 5 as parsed")
pri = [r for r in cat if r["table"] == "prior"]
check(all(3.4 <= r["snr_peak"] <= 5.5 for r in pri), f"prior table S/N_peak range {min(r['snr_peak'] for r in pri)}-{max(r['snr_peak'] for r in pri)} (paper: 3.5-5 with priors)")
fields = list(cat[0].keys())
with open(os.path.join(HERE, "goodsalma2_catalogue.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(cat)

def sep(ra1, d1, ra2, d2):
    return math.hypot((ra1 - ra2) * math.cos(math.radians((d1 + d2) / 2)) * 3600, (d1 - d2) * 3600)

kurvs = list(csv.DictReader(open(os.path.join(HERE, "..", "arxiv_tables", "kurvs_positions", "kurvs_positions.csv"))))
out = []
for k in kurvs:
    ra, dec = float(k["ra_deg"]), float(k["dec_deg"])
    d = sorted(((sep(ra, dec, r["ra_deg"], r["dec_deg"]), r) for r in cat), key=lambda t: t[0])
    within = [(x, r) for x, r in d if x <= 1.5]
    out.append(dict(kurvs_id=k["kurvs_id"], candels_id=k["candels_id"], z_halpha=k["z_halpha"],
                    n_within_1p5_arcsec=len(within),
                    nearest_id=d[0][1]["id"], nearest_sep_arcsec=round(d[0][0], 2), nearest_table=d[0][1]["table"],
                    nearest_S1p1mm_mJy=d[0][1]["S1p1mm_mJy"], nearest_S1p1mm_err_mJy=d[0][1]["S1p1mm_err_mJy"], nearest_snr_peak=d[0][1]["snr_peak"],
                    nearest_z=d[0][1]["z"], nearest_logMstar=d[0][1]["logMstar"],
                    second_id=d[1][1]["id"], second_sep_arcsec=round(d[1][0], 2),
                    within_10_arcsec=";".join(f"{r['id']}@{x:.1f}" for x, r in d if x <= 10)))
with open(os.path.join(HERE, "kurvs_goodsalma_nearest.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
nm = [o for o in out if o["n_within_1p5_arcsec"]]
LOG.append(f"KURVS galaxies with a GOODS-ALMA 2.0 source within 1.5 arcsec: {len(nm)}: " + ", ".join(f"KURVS-{o['kurvs_id']}->{o['nearest_id']}@{o['nearest_sep_arcsec']}" for o in nm)); print(LOG[-1])
# ---------------------------------------------------------------- footprint from the paper's stated geometry
# centre 03:32:30, -27:48:00; ~10' x 7'; six parallel ~6.8' x 1.5' slices at position angle 70 deg (arXiv:2106.13246 Sect. 2.1).  PA convention (N through E) and that the
# 6.8' side is the slice's long axis along PA 70 deg are MY reading of the sentence (interpretation A); interpretation B swaps the two sides.
C_RA, C_DEC = 15 * (3 + 32 / 60 + 30 / 3600), -(27 + 48 / 60)
def uv(ra, dec, pa):
    e = (ra - C_RA) * math.cos(math.radians(C_DEC)) * 60; n = (dec - C_DEC) * 60          # arcmin east, north
    a = math.radians(pa)
    return e * math.sin(a) + n * math.cos(a), e * math.sin(a + math.pi / 2) + n * math.cos(a + math.pi / 2)   # along PA, along PA+90
def status(ra, dec, half_along, half_across):
    u, v = uv(ra, dec, 70.0)
    m = min(half_along - abs(u), half_across - abs(v))
    return u, v, m
A = (3.4, 5.0)      # interpretation A: 6.8' along PA 70, ~10' across
B = (5.0, 3.5)      # interpretation B: ~10' along PA 70, 7' across
def frac_inside(dims):
    return sum(status(r["ra_deg"], r["dec_deg"], *dims)[2] >= 0 for r in cat) / len(cat)
LOG.append(f"88 catalogue sources inside the nominal rectangle: interpretation A (6.8' along PA70) {frac_inside(A):.0%}, interpretation B (10' along PA70) {frac_inside(B):.0%}"); print(LOG[-1])
best = "A" if frac_inside(A) >= frac_inside(B) else "B"
check(max(frac_inside(A), frac_inside(B)) >= 0.90 and frac_inside(B) > frac_inside(A), f"the paper's own 88 sources fit the 10'x7' rectangle with the 10' side along PA 70 deg (interpretation B) at >= 90% and better than A")
ENV = (max(abs(status(r["ra_deg"], r["dec_deg"], 99, 99)[0]) for r in cat), max(abs(status(r["ra_deg"], r["dec_deg"], 99, 99)[1]) for r in cat))
LOG.append(f"empirical envelope of the 88 sources along/across PA70: {ENV[0]:.2f}' / {ENV[1]:.2f}' (half-extent)"); print(LOG[-1])
with open(os.path.join(HERE, "kurvs_goodsalma_footprint.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["kurvs_id", "candels_id", "u_arcmin_alongPA70", "v_arcmin_acrossPA70", "margin_B_nominal_arcmin", "status_B_nominal", "margin_envelope_arcmin", "status_envelope", "margin_A_arcmin", "status_A_alternative_reading"])
    w.writeheader()
    for k in kurvs:
        ra, dec = float(k["ra_deg"]), float(k["dec_deg"])
        u, v, mA = status(ra, dec, *A); _, _, mB = status(ra, dec, *B)
        f = lambda m: "inside" if m >= 0.5 else ("inside, within 0.5' of the edge" if m >= 0 else ("outside, within 0.5' of the edge" if m > -0.5 else "outside"))
        _, _, mE = status(ra, dec, ENV[0], ENV[1])
        w.writerow(dict(kurvs_id=k["kurvs_id"], candels_id=k["candels_id"], u_arcmin_alongPA70=round(u, 2), v_arcmin_acrossPA70=round(v, 2),
                        margin_B_nominal_arcmin=round(mB, 2), status_B_nominal=f(mB), margin_envelope_arcmin=round(mE, 2), status_envelope=f(mE),
                        margin_A_arcmin=round(mA, 2), status_A_alternative_reading=f(mA)))
json.dump(dict(source_html_sha256=hashlib.sha256(open(SRC, "rb").read()).hexdigest(), url="https://arxiv.org/html/2106.13246", fetched="2026-09-29"),
          open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")

# ---------------------------------------------------------------- per-galaxy summary + controls
import statistics
foot = {r["kurvs_id"]: r for r in csv.DictReader(open(os.path.join(HERE, "kurvs_goodsalma_footprint.csv")))}
near = {r["kurvs_id"]: r for r in out}
kz = {k["kurvs_id"]: float(k["z_halpha"]) for k in kurvs}
rows = []
for kid in [str(i) for i in range(1, 23)]:
    n = near[kid]; f = foot[kid]
    zsrc = float(n["nearest_z"]) if n["nearest_z"] not in ("", "None") else None
    rows.append(dict(kurvs_id=kid, in_calc_thread_ten=int(int(kid) in (3, 7, 8, 9, 11, 13, 15, 16, 17, 21)),
                     footprint_nominal=f["status_B_nominal"], footprint_envelope=f["status_envelope"],
                     source_within_1p5_arcsec=n["nearest_id"] if int(n["n_within_1p5_arcsec"]) else "",
                     separation_arcsec=n["nearest_sep_arcsec"] if int(n["n_within_1p5_arcsec"]) else "",
                     S1p1mm_mJy=n["nearest_S1p1mm_mJy"] if int(n["n_within_1p5_arcsec"]) else "",
                     S1p1mm_err_mJy=n["nearest_S1p1mm_err_mJy"] if int(n["n_within_1p5_arcsec"]) else "",
                     snr_peak=n["nearest_snr_peak"] if int(n["n_within_1p5_arcsec"]) else "",
                     catalogue_table=n["nearest_table"] if int(n["n_within_1p5_arcsec"]) else "",
                     source_z=zsrc if int(n["n_within_1p5_arcsec"]) else "", kurvs_z_halpha=kz[kid],
                     nearest_source_any_arcsec=n["nearest_sep_arcsec"]))
with open(os.path.join(HERE, "kurvs_goodsalma_summary.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# controls
matched = [r for r in rows if r["source_within_1p5_arcsec"]]
check(all(abs(float(r["source_z"]) - float(r["kurvs_z_halpha"])) < 0.01 for r in matched), "both 1.5-arcsec matches have a catalogue redshift equal to the KURVS H-alpha redshift within 0.01: " + ", ".join(f"KURVS-{r['kurvs_id']} z {r['kurvs_z_halpha']} vs {r['source_z']}" for r in matched))
dens = len(cat) / (72.42 * 3600)
LOG.append(f"expected chance matches within 1.5 arcsec for 22 galaxies (uniform density {dens:.2e}/arcsec^2, area-weighted): {22 * math.pi * 1.5**2 * dens:.3f}; found {len(matched)}"); print(LOG[-1])
bl = [r for r in cat if r["table"] == "blind"]; pr = [r for r in cat if r["table"] == "prior"]
LOG.append(f"faintest blind-table flux {min(r['S1p1mm_mJy'] for r in bl)} mJy (median {statistics.median(r['S1p1mm_mJy'] for r in bl):.2f}); prior-table faintest {min(r['S1p1mm_mJy'] for r in pr)} mJy"); print(LOG[-1])
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
