#!/usr/bin/env python3
"""CLR1 transcription (FROZEN_CRITERIA.md 7756d82189, section 1). Parses Tables 1-5 of Chen et al. 2007
(arXiv:astro-ph/0702482, chenyAAfinal.tex) into one tracked CSV row per cluster, every value with its TeX table and line.
    python3 -I -B clr1_transcribe.py <path to chenyAAfinal.tex> <out csv>
Parse checks (lane stops on failure): 106 clusters in Tables 1+2, 106 in Tables 4+5 with matching names, 49 in Table 3,
every Table 3 name in Tables 1/2. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import sys, re, csv, hashlib

TEX, OUT = sys.argv[1], sys.argv[2]
raw = open(TEX, "rb").read()
SHA = hashlib.sha256(raw).hexdigest()
lines = raw.decode("latin-1").split("\n")

# table spans located by caption text (1-based line numbers)
def span(caption):
    i0 = next(i for i, l in enumerate(lines) if "\\caption" in l and caption in l)
    i1 = next(i for i in range(i0, len(lines)) if "\\end{table" in lines[i])
    return i0, i1
CAP = {1: "Cluster properties.}", 2: "Cluster properties of the extended cluster sample.}",
       3: "Fit parameters with a double", 4: "Cluster properties for the scaling relations.}",
       5: "Cluster properties for the scaling relations of the extended cluster sample.}"}
NUM = r"[-+]?\d+(?:\.\d+)?"

def cell(c):
    """value, err_plus, err_minus, flag ('' | letter | 'est' for values in parentheses)."""
    c = c.strip()
    flag = ""
    m = re.match(r"\$\^\{?([a-d])\}?\$", c)
    if m: flag = m.group(1); c = c[m.end():]
    if c.startswith("("): flag = "est"
    c2 = c.replace("(", "").replace(")", "")
    v = re.match(r"\s*(" + NUM + ")", c2)
    if not v: return None, None, None, flag
    val = float(v.group(1))
    m = re.search(r"\^\{\s*\+?\s*(" + NUM + r")\s*\}_\{\s*-?\s*(" + NUM + r")\s*\}", c2)
    if m: return val, float(m.group(1)), float(m.group(2)), flag
    m = re.search(r"\\pm\{\s*(" + NUM + r")\s*\}", c2)
    if m: return val, float(m.group(1)), float(m.group(1)), flag
    return val, None, None, flag

def rows(t):
    i0, i1 = span(CAP[t]); out = []
    for i in range(i0, i1):
        l = lines[i]
        if l.strip().startswith("%") or "&" not in l or "\\\\" not in l: continue
        parts = l.split("\\\\")[0].split("&")
        name = parts[0].strip()
        if not name or "$" in name or name.lower() in ("name",) or "Name" in name: continue
        out.append((name, i + 1, [cell(p) for p in parts[1:]]))
    return out

T = {t: rows(t) for t in CAP}
key = lambda n: n.upper().replace(" ", "")
cl = {}
order = []
for t in (1, 2):
    for name, ln, c in T[t]:
        k = key(name); order.append(k)
        cl[k] = dict(name=name, src_t12=f"T{t}:L{ln}", z=c[0][0], Tm=c[1][0], Tm_ep=c[1][1], Tm_em=c[1][2], Tm_flag=c[1][3],
                     beta=c[2][0], beta_ep=c[2][1], beta_em=c[2][2], rc_kpc=c[3][0], rc_ep=c[3][1], rc_em=c[3][2],
                     ncenter_1e2cm3=c[4][0], tcool_1e10yr=c[5][0], Mdot=c[6][0], Mdot_ep=c[6][1], Mdot_em=c[6][2], sample=t)
for t in (4, 5):
    for name, ln, c in T[t]:
        k = key(name)
        assert k in cl, ("T4/5 name not in T1/2", name)
        cl[k].update(src_t45=f"T{t}:L{ln}", Th=c[0][0], Th_ep=c[0][1], Th_em=c[0][2], Th_flag=c[0][3], LX_1e44=c[1][0],
                     M500_1e14=c[2][0], M500_ep=c[2][1], M500_em=c[2][2], r500_Mpc=c[3][0], r500_ep=c[3][1], r500_em=c[3][2],
                     fgas=c[4][0], Mgas500_1e13=c[5][0], Mgas500_ep=c[5][1], Mgas500_em=c[5][2], Lnir_1e12=c[6][0] if len(c) > 6 else None)
n3 = 0
for name, ln, c in T[3]:
    k = key(name); assert k in cl, ("T3 name not in T1/2", name); n3 += 1
    cl[k].update(src_t3=f"T3:L{ln}", S01=c[0][0], S02=c[1][0], beta1=c[2][0], beta2=c[3][0], rc1_kpc=c[4][0], rc2_kpc=c[5][0],
                 chi2_single=c[6][0], chi2_double=c[7][0], double=1)
n12 = len(T[1]) + len(T[2]); n45 = len(T[4]) + len(T[5])
checks = dict(n_T12=n12, n_T45=n45, n_T3=n3, all_have_T45=all("Th" in v for v in cl.values()), unique=len(cl) == n12)
print("tex sha256", SHA); print("checks", checks)
ok = n12 == 106 and n45 == 106 and n3 == 49 and checks["all_have_T45"] and checks["unique"]
cols = ["name", "sample", "src_t12", "src_t45", "src_t3", "z", "Tm", "Tm_ep", "Tm_em", "Tm_flag", "beta", "beta_ep", "beta_em", "rc_kpc",
        "rc_ep", "rc_em", "ncenter_1e2cm3", "tcool_1e10yr", "Mdot", "Mdot_ep", "Mdot_em", "Th", "Th_ep", "Th_em", "Th_flag", "LX_1e44",
        "M500_1e14", "M500_ep", "M500_em", "r500_Mpc", "r500_ep", "r500_em", "fgas", "Mgas500_1e13", "Mgas500_ep", "Mgas500_em",
        "Lnir_1e12", "double", "S01", "S02", "beta1", "beta2", "rc1_kpc", "rc2_kpc", "chi2_single", "chi2_double"]
with open(OUT, "w", newline="") as f:
    f.write(f"# Chen et al. 2007 A&A 466 805 (arXiv:astro-ph/0702482) Tables 1-5 transcribed by clr1_transcribe.py from chenyAAfinal.tex sha256 {SHA}\n")
    f.write("# Units as published: H0 = 50, Omega_m = 1, Omega_L = 0. src_* = table and TeX line. T in keV (Th 90% errors), M500 1e14 Msun, r500 Mpc, Mgas500 1e13 Msun, rc kpc, Mdot Msun/yr, S0 1e-6 cts/s/pixel^2. Tm_flag/Th_flag: a-d = Chen's source notes, est = in parentheses (from L_X-T)\n")
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
    for k in order:
        r = {c: "" for c in cols}; r.update({c: ("" if v is None else v) for c, v in cl[k].items()}); r.setdefault("double", 0)
        if r["double"] == "": r["double"] = 0
        w.writerow(r)
print("PARSE", "OK" if ok else "FAILED"); sys.exit(0 if ok else 1)
