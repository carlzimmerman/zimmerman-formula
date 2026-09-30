#!/usr/bin/env python3
"""Parse the tables of NOEMA3D papers 1 and 2 (Jolly+2026 arXiv:2604.18503 'Resolving radial gas flows ...' and arXiv:2604.18504 'Spatially resolved dust, CO and [CI] ...')
from their arXiv HTML pages (fetched 2026-09-29; copies and sha256 in raw_small/ and manifest.json).  10 galaxies, z = 1.1151-1.6335.
Paper 1: Table 1 (z, R_e,star, M*, M_gas, f_gas, SFR, inc, PA, B/T, n_disk, morphology), Table 2 (observations, two weightings per galaxy), Table 3 (DysmalPy: log M_bary, sigma_0,
V_c(R_e,disk), V_c/sigma_0, f_DM(R_e,disk), R_e,disk, R_e,bulge, Q_gas), Table 4 (radial-flow velocities).  Paper 2: Table 1 (positions, log M_mol, L_IR, M*, SFR), Table 2 (R_e for star, CO, CI, dust, 500 nm; S_CO, S_CI, S_dust), Table 3 (inc, PA, bulge/disk fits).
No acceleration, a0 or verdict is computed.  Field is assigned from the Table 2 coordinates by this script (EGS ~14h19m +52d48m; GOODS-N ~12h37m +62d14m).  The rotation curves are figure-only (Fig. 6) and are NOT in these tables.
Checks compare the two papers on quantities they share; disagreements are REPORTED, not corrected.
"""
import csv, hashlib, html, json, math, os, re, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw_small")
P1 = os.path.join(RAW, "arxiv_2604.18503_html_fetched_2026-09-29.html"); P2 = os.path.join(RAW, "arxiv_2604.18504_html_fetched_2026-09-29.html")
LOG = []
def log(m): LOG.append(m); print(m)
def check(c, m):
    log(("PASS  " if c else "FAIL  ") + m)
    if not c:
        open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n"); raise SystemExit(m)
S = {p: open(p, errors="ignore").read() for p in (P1, P2)}
def flat(x):
    x = re.sub(r'<math[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: " [" + html.unescape(m.group(1)) + "] ", x, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
def table(p, tid):
    s = S[p]; i = s.index('<table id="%s"' % tid); j = s.index("</table>", i)
    return [[flat(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)] for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], flags=re.S)]
NAME = re.compile(r"^G[N]?4_\d+$")
def rows(p, tid): return [r for r in table(p, tid) if r and NAME.match(r[0])]
def num(x):
    if x is None: return None
    m = re.search(r"-?\d+\.?\d*", x.replace("−", "-")); return float(m.group(0)) if m and x.strip() not in ("-", "") else None
def pm(x):  # value and symmetric error from '[8.3\pm 1.3]' or '85 [\pm] 4'
    x = x.replace("[", "").replace("]", "")
    m = re.match(r"\s*(-?\d+\.?\d*)\s*\\pm\s*(\d+\.?\d*)", x)
    return (float(m.group(1)), float(m.group(2))) if m else (num(x), None)
def asym(x):
    m = re.search(r"(-?\d+\.?\d*)\^\{\s*\+\s*(\d+\.?\d*)\}_\{\s*-\s*(\d+\.?\d*)\}", x)
    if m: return float(m.group(1)), float(m.group(3)), float(m.group(2))
    return (num(x), None, None)
def sex(ra, dec):
    h, m, s = [float(v) for v in ra.split(":")]; d, dm, ds = dec.replace("+", "").split(":"); sg = -1 if d.startswith("-") else 1
    return 15 * (h + m / 60 + s / 3600), sg * (abs(float(d)) + float(dm) / 60 + float(ds) / 3600)
p1t1, p1t2, p1t3, p1t4 = (rows(P1, t) for t in ("S2.T1.5", "S2.T2.5", "S3.T3.6", "S3.T4.5"))
p2t1, p2t2, p2t3 = (rows(P2, t) for t in ("S2.T1.2", "S3.T2.2", "S3.T3.2"))
for n, t in (("P1 T1", p1t1), ("P1 T3", p1t3), ("P1 T4", p1t4), ("P2 T1", p2t1), ("P2 T2", p2t2), ("P2 T3", p2t3)): check(len(t) == 10, f"{n}: 10 galaxies (got {len(t)})")
# Table 2 of paper 1: first row per galaxy has 14 cells, the continuation row (weighting Ro5) starts with 'Ro5'
obs = []; cur = None
S2 = table(P1, "S2.T2.5")
for r in S2:
    if r and NAME.match(r[0]): cur = r; obs.append(dict(id=r[0], ra=r[1], dec=r[2], z=num(r[3]), line=r[4], freq_GHz=num(r[5]), config=r[6], t_int_hr=num(r[7]), weighting="natural/first", beam=r[9], beam_pa=num(r[10]), chan_MHz=num(r[11]), noise_mJy=num(r[12]), S_CO_Jykms=num(r[13])))
    elif r and r[0] == "Ro5" and cur: obs.append(dict(id=cur[0], ra=cur[1], dec=cur[2], z=num(cur[3]), line=cur[4], freq_GHz=num(cur[5]), config=cur[6], t_int_hr=num(cur[7]), weighting="Ro5", beam=r[1], beam_pa=num(r[2]), chan_MHz=num(r[3]), noise_mJy=num(r[4]), S_CO_Jykms=num(r[5])))
check(len(obs) == 20, f"Table 2 gives two weightings for each of 10 galaxies (got {len(obs)} rows)")
ids = [r[0] for r in p1t1]
for n, t in (("P1 T3", p1t3), ("P1 T4", p1t4), ("P2 T1", p2t1), ("P2 T2", p2t2), ("P2 T3", p2t3)): check(sorted(r[0] for r in t) == sorted(ids), f"{n} lists the same 10 IDs as P1 T1")
by = lambda t: {r[0]: r for r in t}
b3, b4, q1, q2, q3 = by(p1t3), by(p1t4), by(p2t1), by(p2t2), by(p2t3)
out = []
for r in p1t1:
    i = r[0]; a = b3[i]; f = b4[i]; o2 = [x for x in obs if x["id"] == i][0]
    ra, dec = sex(o2["ra"], o2["dec"]); field = "EGS" if 213 < ra < 216 else ("GOODS-N" if 188 < ra < 190.5 else "?")
    Re, Ree = pm(r[2]); ms, mse = pm(r[3]); mg, mge = pm(r[4]); sfr, sfre = pm(r[6])
    mb, mbl, mbu = asym(a[1]); sg, sgl, sgu = asym(a[2]); vc = num(a[3]); vs, vsl, vsu = asym(a[4]); fd, fdl, fdu = asym(a[5]); Red, Redr = pm(a[6]); Reb, Rebr = pm(a[7]); Q = num(a[8])
    P2R = q2[i]; P2M = q1[i]; P2G = q3[i]
    rc, rce = pm(P2R[2]); rci, rcie = pm(P2R[3]); rd, rde = pm(P2R[4])
    out.append(dict(id=i, field_from_coords=field, ra_deg=round(ra, 5), dec_deg=round(dec, 5), z=num(r[1]), line=o2["line"], t_int_hr=o2["t_int_hr"], beam_first=obs[[k for k, x in enumerate(obs) if x["id"] == i][0]]["beam"],
        Re_star_kpc=Re, Re_star_err=Ree, logMstar_SED=ms, logMstar_err=mse, logMgas_CO_P1=mg, logMgas_err=mge, fgas=num(r[5]), SFR=sfr, SFR_err=sfre, incl_deg_P1=num(r[7]), PA_deg_P1=num(r[8]), BT_P1=num(r[9]), n_disk_P1=num(r[10]), morphology=r[11],
        logMbary_dyn=mb, logMbary_lo=mbl, logMbary_hi=mbu, sigma0_kms=sg, sigma0_lo=sgl, sigma0_hi=sgu, Vc_at_Re_disk_kms=vc, Vc_over_sigma0=vs, fDM_Re_disk=fd, fDM_lo=fdl, fDM_hi=fdu, Re_disk_fixed_kpc=Red, Re_bulge_fixed_kpc=Reb, Q_gas=Q,
        v_r_in_kms=pm(f[1])[0], v_r_out_kms=pm(f[2])[0], Mdot_Msun_yr=pm(f[3])[0],
        logMmol_CO_P2=pm(P2M[4])[0], logLIR_P2=pm(P2M[5])[0], Re_CO_kpc=rc, Re_CO_err=rce, Re_CI_kpc=rci, Re_dust_kpc=rd, Re_500nm_kpc=pm(P2R[5])[0], R80_500nm_kpc=pm(P2R[6])[0],
        S_CO_P2_Jykms=pm(P2R[7])[0], S_CI_Jykms=pm(P2R[8])[0], S_dust_mJy=pm(P2R[9])[0], incl_deg_P2=num(P2G[1]), PA_deg_P2=num(P2G[2]), BT_P2=num(P2G[8]), n_disk_P2=pm(P2G[5])[0], Re_disk_P2_kpc=pm(P2G[6])[0], logSigma1kpc=num(P2G[7])))
check(all(o["field_from_coords"] != "?" for o in out), "every galaxy assigned to a field from its Table 2 coordinates")
check(all(0 <= o["fDM_Re_disk"] <= 1 for o in out), "f_DM in [0, 1] for all 10")
check(1.11 < min(o["z"] for o in out) and max(o["z"] for o in out) < 1.64, f"z range {min(o['z'] for o in out)}-{max(o['z'] for o in out)} (paper: ~1.12-1.63)")
check(all(abs(o["z"] - num(q1[o["id"]][3])) < 1e-6 for o in out), "z agrees between P1 Table 1 and P2 Table 1")
# cross-paper agreement on shared quantities: REPORTED, not corrected
DIS = []
def cmp(name, a, b, tol):
    for o in out:
        x, y = o[a], o[b]
        if x is None or y is None or abs(x - y) > tol: DIS.append(f"{o['id']}: {name} P1={x} vs P2={y}")
cmp("log M_mol (CO)", "logMgas_CO_P1", "logMmol_CO_P2", 0.005); cmp("inclination (deg)", "incl_deg_P1", "incl_deg_P2", 0.5); cmp("PA (deg)", "PA_deg_P1", "PA_deg_P2", 0.5); cmp("B/T", "BT_P1", "BT_P2", 0.005); cmp("n_disk", "n_disk_P1", "n_disk_P2", 0.05)
cmp("R_e,disk (kpc)", "Re_disk_fixed_kpc", "Re_disk_P2_kpc", 0.05)
for o in out:
    if abs(o["Re_star_kpc"] - o["Re_disk_fixed_kpc"]) > 0.3: DIS.append(f"{o['id']}: R_e,star (Table 1) = {o['Re_star_kpc']} kpc but R_e,disk (Table 3, where V_c is evaluated) = {o['Re_disk_fixed_kpc']} kpc")
log(f"Cross-paper / definition differences found: {len(DIS)}"); [log("  DIFF " + d) for d in DIS]
# descriptive only
log(f"log(M*_SED + M_gas) minus log M_bary(dyn), dex: " + ", ".join(f"{math.log10(10**o['logMstar_SED']+10**o['logMgas_CO_P1'])-o['logMbary_dyn']:+.2f}" for o in out))
log(f"sigma_0: median {st.median(o['sigma0_kms'] for o in out):.1f} km/s; V_c(R_e,disk): {min(o['Vc_at_Re_disk_kms'] for o in out):.0f}-{max(o['Vc_at_Re_disk_kms'] for o in out):.0f} km/s; f_DM median {st.median(o['fDM_Re_disk'] for o in out):.2f}")
log("fields: " + ", ".join(f"{k}={sum(o['field_from_coords']==k for o in out)}" for k in ("EGS", "GOODS-N")))
# positional overlap with tables already in this repo (input-side, no velocities used)
def load(path, ra, dec, idc):
    p = os.path.join(HERE, "..", path); res = []
    for r in csv.DictReader(open(p)):
        a, d = r.get(ra), r.get(dec)
        if a in (None, "", "nan") or d in (None, "", "nan"): continue
        if ":" in a: a, d = sex(a, d)      # sexagesimal RA (hours) and Dec
        res.append((float(a), float(d), r[idc]))
    return res
def sep(a, b): return 3600 * math.hypot((a[0] - b[0]) * math.cos(math.radians(a[1])), a[1] - b[1])
cats = {"PHIBSS 2013 (Tacconi+13) local table": load("kmos3d_phibss/phibss13_joined.csv", "ra_deg", "dec_deg", "name"), "PHIBSS2 z0.5-0.8 local table": load("phibss2_z05_08/phibss2_z05_08.csv", "ra", "dec", "id"), "KMOS3D catalogue (local)": load("kmos3d_phibss/kmos3d_catalog.csv", "RA", "DEC", "ID"),
        "KURVS-CDFS positions (local)": load("arxiv_tables/kurvs_positions/kurvs_positions.csv", "ra_deg", "dec_deg", "kurvs_id"), "ALPAKA I sample (local)": load("arxiv_tables/alpaka1_sample.csv", "ra_deg", "dec_deg", "name"), "CRISTAL sample (local)": load("arxiv_tables/cristal2025_sample.csv", "ra_deg", "dec_deg", "name")}
ov = []
for cn, cat in cats.items():
    best = min(((sep((o["ra_deg"], o["dec_deg"]), (c[0], c[1])), o["id"], c[2]) for o in out for c in cat), default=None)
    n3 = [(round(s, 2), i, c) for o in out for c in cat for s in [sep((o["ra_deg"], o["dec_deg"]), (c[0], c[1]))] for i in [o["id"]] if s < 3.0]
    log(f"overlap {cn}: {len(cat)} positioned rows; nearest pair {best[0]:.1f} arcsec ({best[1]} - {best[2]}); pairs within 3 arcsec: {len(n3)} {n3}" if best else f"overlap {cn}: no positioned rows"); ov.append((cn, len(cat), n3))
# ID-number overlap against the tables with no coordinates (Price+2021 RC41 ids, PHIBSS 2013 names, KMOS3D ID_SKELTON): same numeric id in a family of the same field is REPORTED, not treated as a match
def numid(x):
    m = re.search(r"(\d+)$", x); return m.group(1) if m else None
for cn, path, col in (("Price+2021 RC41 ids", "price2021_rc41/price2021_rc41.csv", "id"), ("PHIBSS 2013 names", "kmos3d_phibss/phibss13_joined.csv", "name"), ("KMOS3D ID_SKELTON", "kmos3d_phibss/kmos3d_catalog.csv", "ID_SKELTON")):
    ids_ = [r[col] for r in csv.DictReader(open(os.path.join(HERE, "..", path)))]
    hit = [(o["id"], x) for o in out for x in ids_ if numid(o["id"]) == numid(x) and (x.startswith(("EGS", "GN", "G4", "GNS")) )]
    log(f"ID-number overlap with {cn}: {len(ids_)} ids; same trailing number AND an EGS/GN-type prefix: {hit if hit else 'none'}"); ov.append((cn, len(ids_), hit))
with open(os.path.join(HERE, "noema3d_per_galaxy.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
with open(os.path.join(HERE, "noema3d_observations.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(obs[0].keys())); w.writeheader(); w.writerows(obs)
json.dump(dict(sources={os.path.basename(p): hashlib.sha256(open(p, "rb").read()).hexdigest() for p in (P1, P2)}, urls=["https://arxiv.org/html/2604.18503v2", "https://arxiv.org/html/2604.18504v2"], fetched="2026-09-29"), open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
