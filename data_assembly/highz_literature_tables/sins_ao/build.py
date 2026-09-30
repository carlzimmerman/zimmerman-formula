#!/usr/bin/env python3
"""Parse Tables 1, 2, 4, 5, 6 and 7 of Forster Schreiber et al. 2018 (SINS/zC-SINF AO survey, arXiv:1802.07276, ApJS 238, 21) from its arXiv HTML page
(fetched 2026-09-29; copy and sha256 in ../raw_small and manifest.json).  Table 1 = sample (positions, K, z, M*, SFR); 2 = observations; 4 = integrated Halpha line properties;
5 = Halpha sizes and structure (single- and double-Gaussian PSF); 6 = kinematic properties and dynamical masses (R_e, sin i, PA_kin, dv_obs/2, V_rot, sigma_0, V_c, M_dyn, disk criteria);
7 = [N II]/Halpha gradients.  Values keep their asymmetric errors, limits ('<'), and '...' as missing.  No acceleration or a0 is computed.  The SINFONI AO cubes on disk are NOT parsed here."""
import csv, hashlib, html, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "..", "raw_small", "arxiv_1802.07276_html_fetched_2026-09-29.html")
s = open(SRC, errors="ignore").read(); LOG = []
def log(m): LOG.append(m); print(m)
def flat(x):
    x = re.sub(r'<math[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: " [" + html.unescape(m.group(1)) + "] ", x, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
def rows(tid):
    i = s.index('<table id="%s"' % tid); j = s.index("</table>", i)
    return [[flat(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)] for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], flags=re.S)]
def val(x):
    """(value, err_lo, err_hi, flag): flag '' | '<' | '>' | 'missing'"""
    t = x.replace("[", "").replace("]", "").replace("\\rm", "").strip()
    if t in ("", "…", "..."): return (None, None, None, "missing")
    lim = "<" if t.startswith("<") else (">" if t.startswith(">") else ""); t = t.lstrip("<>").strip()
    m = re.match(r"([+-]?\d+\.?\d*)\s*\^\{\s*\+\s*(\d+\.?\d*)\}\s*_\{\s*-\s*(\d+\.?\d*)\}", t)
    if m: return (float(m.group(1)), float(m.group(3)), float(m.group(2)), lim)
    m = re.match(r"([+-]?\d+\.?\d*)\s*\\pm\s*(\d+\.?\d*)", t)
    if m: return (float(m.group(1)), float(m.group(2)), float(m.group(2)), lim)
    m = re.match(r"([+-]?\d+\.?\d*)", t.replace("\\farcs", ".").replace(" ", ""))
    return (float(m.group(1)), None, None, lim) if m else (None, None, None, "unparsed:" + x[:20])
def is_id(c): return bool(c) and c not in ("Source", "…") and re.match(r"^[A-Za-z][A-Za-z0-9\-_]*$", c.replace("[\\rm", "").replace("]", "").strip()) is not None
def table(tid, ncols, names, textcols=(), idcol=0):
    out = []
    for r in rows(tid):
        if len(r) != ncols or not is_id(r[idcol]): continue
        d = {"source": r[0]}
        for k, nm in enumerate(names, start=1):
            if k in textcols: d[nm] = r[k]; continue
            v, lo, hi, fl = val(r[k]); d[nm] = v; d[nm + "_errlo"] = lo; d[nm + "_errhi"] = hi
            if fl: d[nm + "_flag"] = fl
        out.append(d)
    return out
def write(fn, data):
    keys = []
    for d in data:
        for k in d:
            if k not in keys: keys.append(k)
    with open(os.path.join(HERE, fn), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(data)
T1 = table("S2.T1.2", 13, ["ra", "dec", "K_AB", "z_Halpha", "Mstar_1e10Msun", "A_V", "SFR_SED", "sSFR_SED", "SFR_UVIR", "sSFR_UVIR", "UV_rest", "notes"], textcols=(1, 2, 9, 10, 12))
T2 = table("S3.T2.2", 9, ["z_Halpha", "band", "AO_mode", "PA_deg", "strategy", "t_int_s", "res_arcsec", "runs"], textcols=(2, 3, 5, 8))
T4 = table("S4.T4.2", 11, ["z_Halpha", "r_ap_arcsec", "F_Halpha_circ_1e-17", "sigma_tot_kms", "NII_Halpha_circ", "r_maj_ap_arcsec", "q_ap", "PA_ap_deg", "F_Halpha_ell_1e-17", "NII_Halpha_ell"])
T5 = table("S5.T5.2", 11, ["r_half_circ_kpc_1G", "Re_kpc_1G", "n_1G", "q_1G", "PA_1G", "r_half_circ_kpc_2G", "Re_kpc_2G", "n_2G", "q_2G", "PA_2G"])
T6 = table("S6.T6.2", 12, ["Re_kpc", "sin_i", "PA_kin_deg", "dPA_deg", "half_dv_obs_kms", "Vrot_kms", "sigma0_kms", "Vrot_over_sigma0", "Vc_kms", "Mdyn_1e10Msun", "disk_criteria"], textcols=(11,))
T7 = table("S8.T7.2", 4, ["dN2dr_observed", "dN2dr_restricted", "dN2dr_intrinsic"])
for nm, t in (("table1_sample", T1), ("table2_observations", T2), ("table4_integrated_Halpha", T4), ("table5_sizes", T5), ("table6_kinematics", T6), ("table7_N2Ha_gradients", T7)): write(f"sins_ao_{nm}.csv", t); log(f"{nm}: {len(t)} rows")
ids = [set(d["source"] for d in t) for t in (T1, T2, T4, T5, T6)]
log(f"IDs common to Tables 1, 2, 4, 5, 6: {len(set.intersection(*ids))}; union {len(set.union(*ids))}")
for n_, i_ in zip(("T1", "T2", "T4", "T5", "T6"), ids): log(f"  {n_} only: {sorted(i_ - set.intersection(*ids))}")
z1 = {d["source"]: d["z_Halpha"] for d in T1}; bad = [d["source"] for d in T4 if d["source"] in z1 and abs(d["z_Halpha"] - z1[d["source"]]) > 1e-3]
log(f"z agrees between Tables 1 and 4 (tolerance 1e-3): {'yes' if not bad else bad}")
k = [d for d in T6 if d.get("Vc_kms") is not None]
log(f"Table 6: V_c present for {len(k)} of {len(T6)}; sin_i in (0, 1] for all: {all(0 < d['sin_i'] <= 1 for d in T6 if d.get('sin_i') is not None)}; disk-criteria 'Irr': {sum(d['disk_criteria']=='Irr' for d in T6)}")
log(f"z range {min(d['z_Halpha'] for d in T1):.3f}-{max(d['z_Halpha'] for d in T1):.3f}; log M* range {min(__import__('math').log10(d['Mstar_1e10Msun']*1e10) for d in T1 if d['Mstar_1e10Msun']):.2f}-{max(__import__('math').log10(d['Mstar_1e10Msun']*1e10) for d in T1 if d['Mstar_1e10Msun']):.2f}")
# cube inventory on disk (names and sizes only; nothing opened) and name overlap with the local PHIBSS 2013 join
D = os.path.expanduser("~/new_physics/_external_data/sins_ao/cubes/SINS-ZCSINF_AO_release"); norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
files = sorted(f for f in os.listdir(D) if f.endswith(".fits")); inv = []
for f in files: inv.append(dict(file=f, bytes=os.path.getsize(os.path.join(D, f)), kind=re.sub(r"^.*_(data_cut|noise_cut|data|noise|psf)\.fits$", r"\1", f), galaxy=f.split("_K")[0].split("_H")[0].split("_J")[0]))
write("sins_ao_cube_inventory.csv", inv)
log(f"cube files on disk: {len(files)} FITS ({sum(i['bytes'] for i in inv)/1e9:.2f} GB) for {len({i['galaxy'] for i in inv})} galaxies; kinds {sorted({i['kind'] for i in inv})}; not opened")
miss = [d["source"] for d in T6 if not any(norm(d["source"]) in norm(i["galaxy"]) for i in inv)]; log(f"Table-6 sources with no cube by name: {miss} (component rows of ZC400569 and ZC407376)")
ph = [r["name"] for r in csv.DictReader(open(os.path.join(HERE, "..", "..", "kmos3d_phibss", "phibss13_joined.csv")))]
ov = sorted({d["source"] for d in T6 if any(norm(d["source"]) == norm(p) or norm(d["source"]) in norm(p) or norm(p) in norm(d["source"]) for p in ph)}); log(f"name overlap with the local PHIBSS 2013 table: {ov}")
open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
json.dump(dict(source_html_sha256=hashlib.sha256(open(SRC, "rb").read()).hexdigest(), url="https://arxiv.org/html/1802.07276", fetched="2026-09-29", bytes=os.path.getsize(SRC)), open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
