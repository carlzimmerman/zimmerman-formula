#!/usr/bin/env python3
"""Parse the per-galaxy multi-tracer gas tables of published compilations from their arXiv HTML pages (fetched 2026-09-30; sha256 in manifest.json):
  kirkpatrick2019 (arXiv:1905.11417, 12 z~2 galaxies: CO(1-0) and dust RJ gas masses), bourne2019 (arXiv:1810.01640, 10 z~1 galaxies: [CI], CO, dust), 
  dunne_follow_up z=0.35 set (arXiv:2111.09067, 12 H-ATLAS galaxies: L'CI, L'CO, L850 and per-galaxy alpha_CI, alpha_CO, alpha_850), 
  shivaei-style [CI] SMG set (arXiv:2404.05596, 20 SMGs z 2-5: [CI] gas mass, L'CO(1-0), 3 mm dust flux), stripe82 (arXiv:1803.08926: CO and dust gas masses), 
  spt_dsfg (arXiv:2306.03153: fluxes only) and three single galaxies.  Nothing is recomputed; every value is the paper's.  Notes on independence are in MULTI_TRACER_GAS_2026-09-30.md."""
import sys, os, re, csv, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "highz_literature_tables"))
from tabutil import *
RAW = os.path.join(HERE, "raw_small"); LOG = []
def log(m): LOG.append(m); print(m)
def page(i): return open(os.path.join(RAW, f"arxiv_{i}_html_fetched_2026-09-30.html"), errors="ignore").read()
def idclean(x): return re.sub(r"[\s†∗*∗]+$", "", re.sub(r"\[\{\}\^\{?[^\]]*\]", "", x)).strip()
def cells(R, start, names, textcols=(), minlen=None, idre=r"^[A-Za-z0-9][A-Za-z0-9._\- ]*$"):
    out = []
    for r in R[start:]:
        if len(r) < (minlen or len(names) + 1) or not r[0] or not re.match(idre, idclean(r[0])): continue
        d = {"id": idclean(r[0]), "id_raw": r[0]}
        for k, nm in enumerate(names, start=1):
            if k >= len(r): break
            if nm in textcols: d[nm] = r[k]; continue
            v, lo, hi, fl = val(r[k]); d[nm] = v; d[nm + "_errlo"] = lo; d[nm + "_errhi"] = hi
            if fl: d[nm + "_flag"] = fl
        out.append(d)
    return out
# ---------- Kirkpatrick+2019 ----------
s = page("1905.11417"); T3 = cells(rows(s, "S3.T3.2"), 2, ["LCO10_1e10", "L850_1e31", "Mmol_CO_1e11", "Mmol_RJ_1e11", "Mstar_1e11", "SFR", "Tcold_K", "Mdust_1e9"])
T1 = rows(s, "S1.T1.2"); z = {}
for r in T1:
    m = re.match(r"^(\d+)", r[0].strip() if r else "")
    if m and len(r) >= 6:
        zc = val(r[5])[0] if len(r) > 5 else None; zp = val(r[3])[0]
        z.setdefault(m.group(1), zc if zc else zp)
for d in T3: d["z"] = z.get(re.match(r"\d+", d["id"]).group(0)); d["alpha_CO_adopted"] = 6.5; d["note"] = "M_mol,RJ is calibrated to CO with alpha_CO = 6.5, so CO and RJ are NOT independent; Tcold/Mdust from MAGPHYS"
write(os.path.join(HERE, "kirkpatrick2019_z2_CO_dust.csv"), T3); log(f"Kirkpatrick+19: {len(T3)} galaxies (paper: 12); z {min(d['z'] for d in T3 if d['z']):.3f}-{max(d['z'] for d in T3 if d['z']):.3f}")
# ---------- Bourne+2019 ----------
s = page("1810.01640"); B1 = cells(rows(s, "S2.T1.12"), 2, ["cid", "ra", "dec", "z", "Mstar_1e10", "LUV_1e10", "LIR_1e10", "SFR", "Md_1e7", "Td_K", "lambda0_um", "alpha"], textcols=("cid", "ra", "dec"))
B4 = cells(rows(s, "S5.T4.4"), 2, ["Md_SED_1e7", "Md_Lcont_1e7", "Mmol_CI_1e9", "Mmol_cont_1e9", "ratio_cont_over_CI"])
B2 = rows(s, "S3.T2.2"); b4 = {d["id"]: d for d in B4}
for d in B1: d.update({k: v for k, v in b4.get(d["id"], {}).items() if k not in ("id", "id_raw")}); d["conversions"] = "[CI]: Q10 = 0.35, X_CI = 3e-5; continuum: Scoville-type from L_cont; kappa_850 = 0.077 m2/kg for SED dust"
write(os.path.join(HERE, "bourne2019_z1_CI_CO_dust.csv"), B1); log(f"Bourne+19: {len(B1)} galaxies in Table 1, {len(B4)} in Table 4 (masses from [CI] and continuum); z {min(d['z'] for d in B1):.3f}-{max(d['z'] for d in B1):.3f}")
Bf = []
for r in B2[2:]:
    if len(r) >= 10 and r[0]: Bf.append(dict(id_component=r[0], Scont_mJy=val(r[1])[0], SCI_Jykms=val(r[2])[0], SCO_Jykms=val(r[6])[0], z_CI=val(r[5])[0], z_CO=val(r[9])[0], raw_SCI=r[2], raw_SCO=r[6]))
write(os.path.join(HERE, "bourne2019_line_fluxes.csv"), Bf); log(f"Bourne+19 Table 2 line/continuum fluxes: {len(Bf)} rows")
# ---------- z = 0.35 H-ATLAS (arXiv:2111.09067) ----------
s = page("2111.09067"); H6 = cells(rows(s, "S3.T6.4"), 2, ["LCI_log", "LCO_log", "L850_log", "Mstar_log", "LIR_log", "Md_log", "sSFR_log", "Tc_K"]); H7 = cells(rows(s, "S4.T7.14"), 2, ["logMH2", "XCI_1e-5", "alpha_CI", "alpha_CO", "deltaGDR", "alpha_850", "fgas", "tdep_Gyr"])
h7 = {}
for d in H7: h7.setdefault(d["id"].split()[0], []).append(d)
H = []
for d in H6:
    k = d["id"].split()[0]; e = dict(d)
    for x in h7.get(k, [])[:1]: e.update({kk: vv for kk, vv in x.items() if kk not in ("id", "id_raw")})
    H.append(e)
T1 = rows(s, "S2.T1.2"); zz = {}
for r in T1:
    for c in r[:3]:
        c = c.strip()
        if re.match(r"^\d+$", c) and len(r) > 5:
            v = val(r[5])[0]
            if v and 0.3 < v < 0.4: zz[c] = v
for d in H: d["z"] = zz.get(d["id"].split()[0])
write(os.path.join(HERE, "hatlas_z035_CI_CO_dust.csv"), H); log(f"H-ATLAS z=0.35 set: {len(H6)} rows in Table 6, {len(H7)} in Table 7; z found for {sum(1 for d in H if d['z'])}")
# ---------- arXiv:2404.05596 SMGs ----------
s = page("2404.05596"); S1 = rows(s, "S1.T1.2"); zs = {}
for r in S1:
    if len(r) > 3 and re.match(r"^AS2|^[A-Z]", r[0]) and val(r[3])[0]: zs[r[0].strip()] = val(r[3])[0]
S2 = cells(rows(s, "S2.T2.9"), 2, ["z", "ICI_Jykms", "FWHM_CI_kms", "LpCI_1e10", "Mgas_CI_1e10", "LpCO10_1e10", "Jup", "LpCO_Jup_1e10", "LIR_1e12", "S3mm_mJy"])
for d in S2: d["note"] = "M_gas,[CI] uses X_[CI] = 5.1e-5; L'CO(1-0) may be estimated from mid-J CO (see footnotes); no CO-based mass column"
write(os.path.join(HERE, "smg_CI_CO_3mm_arxiv2404.05596.csv"), S2); log(f"arXiv:2404.05596: {len(S2)} sources (paper: 20); z {min(d['z'] for d in S2):.3f}-{max(d['z'] for d in S2):.3f}")
# ---------- Stripe82 (arXiv:1803.08926) ----------
s = page("1803.08926"); R3 = rows(s, "A2.T3.8") + rows(s, "A2.T4.2")
S3 = []
for r in R3:
    if len(r) >= 12 and re.match(r"^\d+", r[0].strip()):
        d = {"id": idclean(r[0]), "id_raw": r[0]}
        for k, nm in enumerate(["z", "logMstar", "logSFR", "Z_12logOH", "Re_kpc", "Tdust_K", "logMdust", "logMgas_dust", "logMgas_CO", "logMdyn", "logMHI"], start=1):
            v, lo, hi, fl = val(r[k]); d[nm] = v; d[nm + "_errlo"] = lo; d[nm + "_errhi"] = hi
            if fl: d[nm + "_flag"] = fl
        S3.append(d)
seen = set(); S3u = []
for d in S3:
    if d["id"] not in seen: seen.add(d["id"]); S3u.append(d)
for d in S3u: d["conversions"] = "CO: alpha_CO,MW = 3.2 x metallicity factor (G12/B13 geometric mean); dust: Leroy+2011 metallicity-dependent dust-to-gas"
write(os.path.join(HERE, "stripe82_z_lt0.3_CO_dust.csv"), S3u); log(f"Stripe82 (arXiv:1803.08926): {len(S3u)} galaxies with M_gas,dust and M_gas,CO; z {min(d['z'] for d in S3u):.3f}-{max(d['z'] for d in S3u):.3f}")
# ---------- arXiv:2306.03153 SPT DSFG fluxes ----------
s = page("2306.03153"); P = []
for r in rows(s, "S2.T2.2")[2:]:
    if len(r) >= 8 and r[0].startswith("SPT"): P.append(dict(id=r[0].strip(), z=val(r[1])[0], CI10_Jykms=val(r[4])[0], CI21_Jykms=val(r[5])[0], CO76_Jykms=val(r[6])[0], CII_Jykms=val(r[7])[0], raw=" ; ".join(r[4:8])))
write(os.path.join(HERE, "spt_dsfg_CI_CO_CII_fluxes_arxiv2306.03153.csv"), P); log(f"arXiv:2306.03153: {len(P)} lensed SPT DSFGs with line fluxes (no masses tabulated); z {min(d['z'] for d in P):.3f}-{max(d['z'] for d in P):.3f}")
open(os.path.join(HERE, "checks_multitracer.txt"), "w").write("\n".join(LOG) + "\n")
json.dump({f: hashlib.sha256(open(os.path.join(RAW, f), "rb").read()).hexdigest() for f in sorted(os.listdir(RAW))}, open(os.path.join(HERE, "manifest_multitracer.json"), "w"), indent=1)
