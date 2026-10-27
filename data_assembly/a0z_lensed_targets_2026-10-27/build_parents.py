"""a0(z) lensed-disc target search, step 1: parent list from the published lensed kinematic surveys (TeX tables in raw/, fetched with
fetch_logged.py) and the selection declared in README.md before any archive query. Writes parents.csv and selected.csv. No law is fitted.
Run: python3 -I build_parents.py"""
import re, csv, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw")
def tables(path):
    t = open(os.path.join(RAW, path), errors="ignore").read()
    return re.findall(r"\\begin\{(?:deluxe)?table\*?\}(.*?)\\end\{(?:deluxe)?table\*?\}", t, re.S)
def cells(row):
    row = re.sub(r"%.*", "", row)
    return [c.strip() for c in row.split("&")]
def num(s):
    m = re.search(r"[-+]?\d+(?:\.\d+)?", s.replace("−", "-")); return float(m.group()) if m else None
def first_num(s):                                   # value before ± / _ / ^ ; '<x' -> upper limit flagged
    s = s.replace("$", "").replace("\\pm", "±")
    lim = "<" in s
    return num(re.split(r"±|_|\^", s)[0]), lim
def hms(s):
    h, m, x = map(float, s.replace(":", " ").replace("$", "").split()[:3]); return 15 * (h + m / 60 + x / 3600)
def dms(s):
    s = s.replace(":", " ").replace("$", "").strip(); sg = -1 if s.startswith("-") else 1
    d, m, x = map(float, s.lstrip("+-").split()[:3]); return sg * (d + m / 60 + x / 3600)

P = []
# --- KLASS I (Mason+2017, arXiv:1610.03075): Cluster, ID, RA, Dec, z, line, t, mu, logM*, sigma0, Vmax, class
for r in tables("1610.03075/ms.tex")[0].split("\\\\"):
    c = cells(r)
    if len(c) < 12 or not re.match(r"^(MACS|RXJ)", c[0]): continue
    s0, sl = first_num(c[9]); vm, vl = first_num(c[10]); m, _ = first_num(c[8]); mu, _ = first_num(c[7])
    P.append(dict(name=f"{c[0]}-{c[1]}", survey="KLASS-I (Mason+17)", ra=num(c[2]), dec=num(c[3]), z=num(c[4]), logMstar=m, mu=mu,
                  V=vm if c[10].strip("$ ") != "-" else None, sigma=s0, sigma_upper=sl, vsig_def="Vmax/sigma0 (intrinsic, GalPaK/2D)",
                  kin_class=re.sub(r"[^0-9]", "", c[11])[:1], note=("probable merger" if "f" in c[11] else ("2D model" if "e" in c[11] else ""))))
# --- KLASS 2020 (Girard+2020, arXiv:2006.14633): T0 properties (Objects, RA Dec, z, lines, mu, logM*, SFR); T1 kinematics (v_rot, sigma0, class)
T0, T1 = tables("2006.14633/mgirard_KLASS2020.tex")[:2]
kin = {}
for r in T1.split("\\\\"):
    c = cells(r)
    if len(c) >= 4 and re.match(r"^(A2744|MACS|RXJ)", c[0]):
        v, _ = first_num(c[1]) if "Non" not in c[1] and c[1].strip("$ ") != "-" else (None, False)
        s, _ = first_num(c[2]) if "Non" not in c[2] and c[2].strip("$ ") != "-" else (None, False)
        kin[c[0].strip()] = (v, s, re.sub(r"[^0-9]", "", c[3])[:1], c[4].strip() if len(c) > 4 else "")
for r in T0.split("\\\\"):
    c = cells(r)
    if len(c) < 7 or not re.match(r"^(A2744|MACS|RXJ)", c[0]): continue
    ra, dec = [float(x) for x in re.findall(r"[-+]?\d+\.\d+", c[1].replace("+ ", "+"))[:2]]
    nm = c[0].strip(); v, s, k, cl = kin.get(nm, (None, None, "", ""))
    m, _ = first_num(c[5]); mu, _ = first_num(c[4])
    P.append(dict(name=nm, survey="KLASS-2020 (Girard+20)", ra=ra, dec=dec, z=num(c[2]), logMstar=m, mu=mu, V=v, sigma=s, sigma_upper=False,
                  vsig_def="v_rot/sigma0 (intrinsic)", kin_class=k, note=("potential merger" if "merger" in cl.lower() else "")))
# --- OLAS I (Hirtenstein+2019, arXiv:1811.11768): T0 (Cluster, ID, z, RA, Dec, ..., mu), T1 (Cluster, ID, logM*, ..., local sigma, integ sigma, dV, V/sigma, class)
O0, O1 = tables("1811.11768/OLAS_I.tex")[:2]
pos = {}
for r in O0.split("\\\\"):
    c = cells(r)
    if len(c) >= 12 and re.match(r"^(A370|M\d{4})", c[0]):
        pos[(c[0], re.sub(r"\\footnote.*", "", c[1]).strip())] = (num(c[2]), hms(c[3]), dms(c[4]), first_num(c[11])[0])
for r in O1.split("\\\\"):
    c = cells(r)
    if len(c) < 10 or not re.match(r"^(A370|M\d{4})", c[0]): continue
    key = (c[0], c[1].strip())
    if key not in pos: continue
    z, ra, dec, mu = pos[key]; dV = num(c[7]); s = first_num(c[5])[0]
    P.append(dict(name=f"{c[0]}-{c[1].strip()}", survey="OLAS-I (Hirtenstein+19)", ra=ra, dec=dec, z=z, logMstar=first_num(c[2])[0], mu=mu,
                  V=(dV / 2 if dV is not None else None), sigma=s, sigma_upper=False, vsig_def="(dV/2)/sigma_local, NOT inclination-corrected",
                  kin_class=re.sub(r"[^0-9]", "", c[9])[:1], note=""))
# --- Leethochawalit+2016 (arXiv:1509.01279) and Jones+2010 (arXiv:0910.4488): no stellar masses in the tables; all massive (V_c 129-570) or V/sigma < 2;
#     recorded with V as the mass proxy only (see README), positions from their observation logs.
LEE = {"cswa15": (2.16, "10:09:01", "+19:37:23", 29, 48), "cswa19": (2.03, "09:00:03", "+22:34:08", 126, 78), "cswa20": (1.43, "14:41:49", "+14:41:22", 133, 62),
       "cswa28": (2.09, "13:43:33", "+41:55:13", 91, 56), "cswa31": (1.49, "09:21:25", "+18:10:11", 122, 56), "cswa128": (2.22, "19:58:35", "+59:50:53", 570, 66),
       "cswa139": (2.54, "08:07:32", "+44:10:51", 265, 62), "cswa159": (2.30, "22:22:09", "+27:45:25", 141, 61), "cswa165": (2.13, "01:05:20", "+01:44:58", 359, 44)}
for n, (z, ra, de, v, s) in LEE.items():
    P.append(dict(name=n, survey="Leethochawalit+16", ra=hms(ra.replace(":", " ")), dec=dms(de.replace(":", " ")), z=z, logMstar=None, mu=None, V=v, sigma=s,
                  sigma_upper=False, vsig_def="V_c/sigma (model, inclination-corrected)", kin_class="", note="no M* in tables"))
JON = {"Cl0024+1709": (1.680, "00 26 34.43", "+17 09 55.4", 76, 69), "MACSJ0451+0006": (2.014, "04 51 57.27", "+00 06 20.7", 38, 80),
       "MACSJ0712+5932": (2.648, "07 12 17.51", "+59 32 16.3", 15, 81), "MACSJ0744+3927": (2.209, "07 44 47.82", "+39 27 25.7", 129, 99),
       "MACSJ2135-0102": (3.074, "21 35 12.73", "-01 01 43.0", 47, 54)}
for n, (z, ra, de, v, s) in JON.items():
    P.append(dict(name=n, survey="Jones+10", ra=hms(ra), dec=dms(de), z=z, logMstar=None, mu=None, V=v, sigma=s, sigma_upper=False,
                  vsig_def="V_max/sigma", kin_class="", note="no M* in tables"))

# --- declared selection (README section 2): z, mass window via M_b = M*/(1 - f_gas) with f_gas 0.5 (bracket 0.3-0.7), V/sigma
for p in P:
    p["vsig"] = (p["V"] / p["sigma"]) if (p["V"] and p["sigma"]) else None
    m = p["logMstar"]
    p["logMb_f05"] = (m + math.log10(2.0)) if m is not None else None
    z = p["z"] or 0
    p["z_ok"] = "yes" if 1.5 <= z <= 2.6 else ("near" if 1.45 <= z < 1.5 else "no")
    lo, hi = math.log10(5e9), math.log10(2e10)
    p["mass_ok"] = ("yes" if (m is not None and lo <= m + math.log10(2.0) <= hi) else
                    ("bracket" if (m is not None and lo <= m + math.log10(1 / 0.3) and m + math.log10(1 / 0.7) <= hi) else ("unknown" if m is None else "no")))
    p["vsig_ok"] = "yes" if (p["vsig"] or 0) >= 2.5 else ("near" if (p["vsig"] or 0) >= 2.0 else "no")
    p["selected"] = p["z_ok"] in ("yes", "near") and p["mass_ok"] in ("yes", "bracket") and p["vsig_ok"] in ("yes", "near") and "merger" not in p["note"]
cols = ["name", "survey", "ra", "dec", "z", "logMstar", "logMb_f05", "mu", "V", "sigma", "sigma_upper", "vsig", "vsig_def", "kin_class", "note", "z_ok", "mass_ok", "vsig_ok", "selected"]
for fn, rows in (("parents.csv", P), ("selected.csv", [p for p in P if p["selected"]])):
    with open(os.path.join(HERE, fn), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for p in rows: w.writerow({k: (round(p[k], 5) if isinstance(p[k], float) else p[k]) for k in cols})
print(f"parents {len(P)} (" + ", ".join(f"{s} {sum(p['survey'] == s for p in P)}" for s in sorted(set(p['survey'] for p in P))) + ")")
print(f"selected {sum(p['selected'] for p in P)}:")
for p in P:
    if p["selected"]:
        print(f"  {p['name']:16s} {p['survey'][:10]:10s} z {p['z']:.2f} logM* {p['logMstar']:.2f} mu {p['mu']} V {p['V']} sig {p['sigma']} V/s {p['vsig']:.2f} [{p['vsig_def'][:22]}] class {p['kin_class']} z_ok {p['z_ok']} mass {p['mass_ok']} vsig {p['vsig_ok']}")
