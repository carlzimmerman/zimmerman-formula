#!/usr/bin/env python3
"""GS4 step 1 (criteria 1bf15a0aff): parse published gas masses from _external_data/gs4 into gs4_inputs.csv. No eRASS1 read, no matching. Reads data only; nothing downloaded is executed.
    python3 -I gs4_parse.py   # NED look-ups cached in _external_data/gs4/ned/positions.tsv
kappa = 1/2 FITTED; not theory closed."""
import os, re, math, csv, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); X = os.path.join(REPO, "_external_data", "gs4"); DATA = os.path.join(REPO, "real_research", "data")
def tsv(p):
    L = [l.rstrip("\n") for l in open(p, errors="replace") if not l.startswith("#") and l.strip()]; H = [h.strip() for h in L[0].split("\t")]
    return [dict(zip(H, [t.strip() for t in l.split("\t")])) for l in L[3:]]
def sex(a, b):
    f = lambda s: [abs(float(t)) for t in re.split(r"[:\s]+", s.strip())]; A = f(a); B = f(b); ra = 15 * (A[0] + A[1] / 60 + A[2] / 3600); de = B[0] + B[1] / 60 + B[2] / 3600
    return ra, (-de if b.strip().startswith("-") else de)
def rho_c(z, h, Om): H = h * 100 * 1.0227e-3 * math.sqrt(Om * (1 + z) ** 3 + 1 - Om); return 3 * H ** 2 / (8 * math.pi * 4.30091e-6)   # Msun/kpc^3, H in km/s/kpc
def r500(M, z, h, Om): return (3 * M / (4 * math.pi * 500 * rho_c(z, h, Om))) ** (1 / 3)
os.makedirs(os.path.join(X, "ned"), exist_ok=True); NC = os.path.join(X, "ned", "positions.tsv"); NED = {}
if os.path.exists(NC):
    for l in open(NC):
        a = l.rstrip("\n").split("\t"); NED[a[0]] = (float(a[1]), float(a[2]), a[3]) if a[1] != "nan" else None
def ned(name):
    if name in NED: return NED[name]
    u = "https://ned.ipac.caltech.edu/cgi-bin/objsearch?" + urllib.parse.urlencode(dict(objname=name, extend="no", of="ascii_bar", list_limit=1)); r = None
    for att in range(8):
        try:
            t = urllib.request.urlopen(u, timeout=40).read().decode(errors="replace"); L = [l for l in t.splitlines() if l.startswith("1|")]
            if L: c = L[0].split("|"); r = (float(c[2]), float(c[3]), c[4].strip())
            break
        except Exception as e: time.sleep(5 + 5 * att)
    else: print("NED error, not cached", name); return None
    NED[name] = r; open(NC, "a").write(f"{name}\t{r[0] if r else 'nan'}\t{r[1] if r else 'nan'}\t{r[2] if r else ''}\n"); time.sleep(1.5); return r
def nedname(n):
    n = n.replace("~", " ").replace("\\,", " ").strip()
    ALIAS = {"M1455": "MS 1455.0+2232", "R0437": "RX J0437.1+0043", "R0439": "RX J0439.0+0715", "Z2089": "ZwCl 0857.9+2107", "Z3146": "ZwCl 1021.0+0426", "Z5247": "ZwCl 1231.4+1706", "Z5768": "ZwCl 1309.1+2216", "Z7215": "ZwCl 1454.8+2233", "R1720": "RX J1720.1+2638", "R2129": "RX J2129.6+0005", "Hydra-A": "Hydra A", "2A 0335": "2A 0335+096", "EXO 0422": "EXO 0422-086", "S 1101": "ABELL S1101", "Zw Cl1215": "ZwCl 1215.1+0400", "RX J1504": "RX J1504.1-0248", "RXJ 1022+3830": "RX J1022.1+3830", "RXJ 1159": "RX J1159.8+5531", "CID28": "CID 28"}
    if n in ALIAS: return ALIAS[n]
    m = re.match(r"^(?:A|Abell)\s*(\d+)$", n, re.I)
    if m: return f"ABELL {int(m.group(1)):04d}"
    m = re.match(r"^S0?(\d+)$", n)
    if m: return f"ABELL S{int(m.group(1)):04d}"
    m = re.match(r"^Z(\d+)$", n)
    if m: return f"ZwCl {m.group(1)}"
    m = re.match(r"^(MKW|AWM|NGC|IC|UGC|ESO|HCG|WBL)\s*([\d-]+\w*)$", n, re.I)
    if m: return f"{m.group(1).upper()} {m.group(2)}"
    m = re.match(r"^RXC\s*J?(.*)$", n)
    if m: return "RXC J" + m.group(1)
    return n
R = []; MISS = []
def add(cat, inst, name, ra, de, z, Mg, Rk, M, h, Om, note=""): R.append(dict(cat=cat, inst=inst, name=name, ra=ra, dec=de, z=z, Mgas=Mg, R500=Rk, M500=M, h=h, Om=Om, note=note))
# L20
AS = {r["PLCKESZ"]: sex(r["RAJ2000"], r["DEJ2000"]) for r in reversed(tsv(os.path.join(X, "andradesantos17", "table4.tsv"))) if r["Sub"] != "S"}
for r in tsv(os.path.join(X, "lovisari20", "table3.tsv")):
    z = float(r["z"]); M = float(r["M500"]) * 1e14; n = r["PLCKESZ"]; pos = AS.get(n) or (float(r["_RA"]), float(r["_DE"])); add("L20", "XMM", n, pos[0], pos[1], z, float(r["Mg500"]) * 1e13, r500(M, z, .7, .3), M, .7, .3, "AS17 centre" if n in AS else "ESZ position")
# L15
for l in open(os.path.join(DATA, "lovisari2015_groups.tsv")):
    if l.startswith(("#", "name")) or not l.strip(): continue
    c = l.rstrip("\n").split("\t"); p = ned(nedname(c[0]))
    if not p: MISS.append(("L15", c[0])); continue
    add("L15", "XMM", c[0], p[0], p[1], float(c[1]), float(c[8]) * 1e12, float(c[4]), float(c[6]) * 1e13, .7, .3, "NED")
# C08
T = open(os.path.join(X, "croston08", "x", "9154_ms.tex")).read()
for m in re.finditer(r"^RXCJ(\d\d)(\d\d\.\d)(\$?[-+]\$?)(\d\d)(\d\d)\s*&\s*([\d.]+)\s*&.*?&\s*([\d.]+)\s*&\s*([\d.]+)\$\\pm\$", T, re.M):
    ra = 15 * (int(m[1]) + float(m[2]) / 60); de = int(m[4]) + int(m[5]) / 60; de = -de if "-" in m[3] else de; z = float(m[6]); Rk = float(m[7]); Mg = 10 ** float(m[8]); add("C08", "XMM", f"RXCJ{m[1]}{m[2]}{'-' if '-' in m[3] else '+'}{m[4]}{m[5]}", ra, de, z, Mg, Rk, float("nan"), .7, .3, "RXC name")
# E16
XXL = {int(r["XLSSC"]): (float(r["RAJ2000"]), float(r["DEJ2000"])) for r in tsv(os.path.join(X, "xxl100", "xxl100gc.tsv"))}
for l in open(os.path.join(X, "eckert16", "x", "table3.tex")):
    m = re.match(r"XLSSC (\d+).*?&\s*([\d.]+)\s*&.*?&\s*\$\s*(\d+)\s*\\pm\s*\d+\s*\$\s*&\s*\$\(([\d.]+)_.*?\\times10\^\{(\d+)\}\$\s*&\s*\$\(([\d.]+)_.*?\\times10\^\{(\d+)\}\$", l)
    if not m: continue
    i = int(m[1])
    if i not in XXL: MISS.append(("E16", i)); continue
    add("E16", "XMM", f"XLSSC{i:03d}", *XXL[i], float(m[2]), float(m[4]) * 10 ** int(m[5]), float(m[3]), float(m[6]) * 10 ** int(m[7]), .7, .28, "IX/49")
# M08
Z = {}
for r in tsv(os.path.join(X, "maughan08", "table1.tsv")): Z.setdefault(r["Name"], float(r["z"]))
for r in tsv(os.path.join(X, "maughan08", "clusters.tsv")):
    if r["Name"] not in Z or not r["Mgas"]: MISS.append(("M08", r["Name"])); continue
    add("M08", "Chandra", r["Name"], float(r["_RA"]), float(r["_DE"]), Z[r["Name"]], float(r["Mgas"]) * 1e13, float(r["R500"]) * 1e3, float("nan"), .7, .3, "VizieR")
# L13
ZL = {}; 
for l in open(os.path.join(X, "landry13", "x", "bcsSample_short_no_ref_DA.tex")):
    m = re.match(r"(\S+)\s*&\s*([\d.]+)\s*&\s*([\d.]+)", l)
    if m: ZL[m[1]] = (float(m[2]), float(m[3]))
for k_, v_ in dict(M1455="MS~1455+2232", R0437="RX~J0437.1+0043", R0439="RX~J0439.0+0715", R1720="RX~J1720.1+2638", R2129="RX~J2129.6+0005").items():
    for l in open(os.path.join(X, "landry13", "x", "bcsSample_short_no_ref_DA.tex")):
        if l.startswith(v_): c_ = l.split("&"); ZL[k_] = (float(c_[1]), float(c_[2]))
for fn in ("vikh_poly_masses_1.tex", "vikh_poly_masses_2.tex"):
    cur = None
    for l in open(os.path.join(X, "landry13", "x", fn)):
        m = re.match(r"\\underline\{(.+?)\}", l)
        if m: cur = m[1]; continue
        if l.startswith("& Vikh") and cur:
            v = re.findall(r"([\d.]+) \$\\pm", l)
            if len(v) < 8 or cur not in ZL: MISS.append(("L13", cur)); continue
            z, DA = ZL[cur]; p = ned(nedname(cur))
            if not p: MISS.append(("L13", cur)); continue
            add("L13", "Chandra", cur, p[0], p[1], z, float(v[5]) * 1e13, float(v[4]) * DA * 1e3 * math.pi / 180 / 3600, float(v[6]) * 1e14, .702, .27, "NED, Vikhlinin model")
# S09
T = open(os.path.join(X, "sun09", "x", "ms.tex")).read().split("\n"); ZS = {}
i0 = next(i for i, l in enumerate(T) if "The group sample and the" in l); i1 = next(i for i, l in enumerate(T) if "Absorption, radial range" in l)
for l in T[i0:i1]:
    c = [t.strip() for t in l.split("&")]
    if len(c) > 3 and c[0] and re.match(r"^[\d.]+$", c[1]): ZS[re.sub(r"\s*\(.*\)", "", c[0])] = float(c[1])
i0 = next(i for i, l in enumerate(T) if "Derived properties of groups (I:" in l); i1 = next(i for i, l in enumerate(T) if "Derived properties of groups (II:" in l)
num = lambda s: float(re.match(r"\$?([\d.]+)", s.replace("\\", "")).group(1))
for l in T[i0:i1]:
    c = [t.strip() for t in l.split("&")]
    if len(c) < 9 or c[3].startswith("(") or not c[5] or not c[6] or not re.match(r"^\$?[\d.]", c[3]): continue
    n = re.sub(r"\s*\(.*\)", "", c[0])
    try: Rk, M, f = num(c[3]), num(c[5]) * 1e13, num(c[6])
    except Exception: MISS.append(("S09 parse", n)); continue
    if n not in ZS: n2 = next((k for k in ZS if k.startswith(n) or k.replace("~", "").startswith(n.replace("~", ""))), None); ZS[n] = ZS[n2] if n2 else None
    if ZS[n] is None: MISS.append(("S09 z", n)); continue
    p = ned(nedname(n))
    if not p: MISS.append(("S09", n)); continue
    add("S09", "Chandra", n, p[0], p[1], ZS[n], f * M, Rk, M, .73, .24, "NED, f_gas x M500")
# M13
T1 = open(os.path.join(X, "mahdavi13", "x", "table1.tex")).read(); T2 = open(os.path.join(X, "mahdavi13", "x", "table2.tex")).read(); P1 = {}
for m in re.finditer(r"^\s*([A-Za-z0-9+-]+)\s*&\s*(\d\d:\d\d:[\d.]+)\s*&\s*([-+]\d\d:\d\d:[\d.]+)\s*&\s*([\d.]+)\s*&", T1, re.M): P1[m[1]] = (*sex(m[2], m[3]), float(m[4]))
for m in re.finditer(r"^\s*([A-Za-z0-9+-]+)\s*&\s*\$([\d.]+)\\pm[\d.]+\$\s*&\s*\$([\d.]+)\\pm[\d.]+\$\s*&\s*\$([\d.]+)\\pm[\d.]+\$", T2, re.M):
    if m[1] not in P1: MISS.append(("M13", m[1])); continue
    add("M13", "MIXED", m[1], P1[m[1]][0], P1[m[1]][1], P1[m[1]][2], float(m[4]) * 1e14, float(m[2]) * 1e3, float(m[3]) * 1e14, .7, .3, "table, WL r500")
# V09 (low-z table; the high-z names carry no usable position), not primary
fg0 = 0.0764 * 0.72 ** -1.5
for l in open(os.path.join(X, "vikhlinin09", "x", "local_sample_dat.tex")):
    m = re.match(r"(.+?)\\dotfill\s*&\s*[\d.]+\s*&\s*([\d.]+)\s*&.*?&\s*\$\s*[\d.]+\\pm[\d. ]+\$\s*&\s*\$\s*[\d.]+\\pm[\d. ]+\$\s*&\s*\$\s*([\d.]+)\\pm", l)
    if not m: continue
    n = m[1].strip(); p = ned(nedname(n))
    if not p: MISS.append(("V09", n)); continue
    z = float(m[2]); M = float(m[3]) * 1e14; add("V09", "Chandra", n, p[0], p[1], z, M * (fg0 + 0.037 * math.log10(M / 1e15)), r500(M, z, .72, .3), M, .72, .3, "NED, Mgas from M_G and f_g(M)")
K = list(R[0].keys()); w = csv.DictWriter(open(os.path.join(HERE, "gs4_inputs.csv"), "w"), K); w.writeheader(); w.writerows(R)
from collections import Counter
print(Counter(r["cat"] for r in R)); print("unresolved or unparsed:", MISS); print("NED type counts:", Counter(v[2] if v else "None" for v in NED.values()))
