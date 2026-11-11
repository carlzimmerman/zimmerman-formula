#!/usr/bin/env python3
"""DD1 step 0: build the one table of measured points (criteria 2a3f76f295). TEST lane, quarantined; adopts nothing.
kappa = 1/2 FITTED; not theory closed. One thread. Usage: python3 dd1_table.py  -> dd1_table.csv, dd1_table.out

Every loader is restated from the lane that first used it (named per class); other lanes' folders are read only.
Columns: cls, sys, bracket, r_kpc, lgb, lgo, e_lgb, e_lgo, eY, z, lSig, last
  lgb / lgo = log10 g_bar / g_obs (m/s^2); eY = error of Y = lgo - lgb (dex); lSig = log10 of the system's baryonic
  surface density inside its half-light radius (Msun/pc^2; nan = not covered); last = 1 on the system's outermost point;
  bracket = '' main table, 'kids_hot' B21 hot-gas Nobins, 'atlas_salp' ATLAS3D at Salpeter (bracket runs only).
"""
import os, sys, csv, math, json, re, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data"); EXT = os.path.join(REPO, "_external_data")
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
T0 = time.time()

# constants: SWT1's (as SHP1 imports them)
G, MS, PC, CL = 6.6743e-11, 1.98847e30, 3.0856775814913673e16, 2.99792458e8
KPC, MPC = 1e3 * PC, 1e6 * PC
LN10 = math.log(10.0)
G_PC = 4.52e-30                                     # B21's G in pc^3 / (Msun s^2) (SHP1)
H0_SPARC, H0_70 = 73.0, 70.0
def z_of_D(D_Mpc, H0=H0_70): return H0 * D_Mpc / (CL / 1e3)
ROWS = []
def add(cls, sys_, r_kpc, gb, go, e_lgb, e_lgo, z, lSig=float("nan"), eY=None, bracket=""):
    lgb = math.log10(gb); lgo = math.log10(go) if go > 0 else float("-inf")
    eY = math.sqrt(e_lgb ** 2 + e_lgo ** 2) if eY is None else eY
    ROWS.append(dict(cls=cls, sys=sys_, bracket=bracket, r_kpc=float(r_kpc), lgb=lgb, lgo=lgo, e_lgb=float(e_lgb),
                     e_lgo=float(e_lgo), eY=float(eY), z=float(z), lSig=float(lSig), last=0))
def norm(n): return re.sub(r"[^A-Z0-9]", "", n.upper())
COUNTS = {}

# ============================================================== SPARC (SHP1's loader and cuts, errors added)
def sparc(ud=0.5, ub=0.7):
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19: continue
        try: tab[tok[0]] = dict(zip(keys, [float(t) for t in tok[1:18]]))
        except ValueError: continue
    nfile, pts = 0, []
    for fn in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
        if not fn.endswith("_rotmod.dat"): continue
        nm = fn.replace("_rotmod.dat", "")
        a = np.genfromtxt(os.path.join(DATA, "sparc_data", fn), comments="#")
        if a.ndim != 2 or a.shape[1] < 6 or nm not in tab: continue
        nfile += 1; m = tab[nm]
        if m["Q"] >= 3 or m["Inc"] < 30: continue
        gal = []
        for R, Vo, eV, Vg, Vd, Vb in a[:, :6]:
            if Vo <= 0 or R <= 0 or eV / Vo > 0.1: continue
            r = R * KPC
            gs = (ud * Vd * abs(Vd) + ub * Vb * abs(Vb)) * 1e6 / r; gg = Vg * abs(Vg) * 1e6 / r; gb = gs + gg
            if gb <= 0: continue
            gal.append((R, gb, Vo * Vo * 1e6 / r, eV / Vo, min(max(gs / gb, 0.0), 1.0)))
        if gal: pts.append((nm, m, gal, a))
    return pts, nfile
SP, NFILE = sparc()
SPARC_NAMES = {norm(nm) for nm, _, _, _ in SP}
SPARC_FILES = {norm(fn.replace("_rotmod.dat", "")) for fn in os.listdir(os.path.join(DATA, "sparc_data")) if fn.endswith("_rotmod.dat")}
for nm, m, gal, a in SP:
    z = z_of_D(m["D"], H0_SPARC); einc = m["eInc"] / math.tan(math.radians(m["Inc"])) * math.radians(1.0) * 1.0
    # SHP1's g_bar at R_eff on the galaxy's own baryonic curve (log-log interpolation; nearest end outside)
    Rg = np.array([g[0] for g in gal]); gbg = np.array([g[1] for g in gal])
    lgR = np.interp(math.log10(m["Reff"]), np.log10(Rg), np.log10(gbg)) if m["Reff"] > 0 else float("nan")
    lSig = lgR - math.log10(math.pi * G) + math.log10(PC ** 2 / MS) if np.isfinite(lgR) else float("nan")
    for R, gb, go, fe, fs in gal:
        e_lgo = math.sqrt((2 * fe) ** 2 + (2 * einc) ** 2 + (m["eD"] / m["D"]) ** 2) / LN10
        e_lgb = math.sqrt((0.11 * fs) ** 2 + (0.04 * (1 - fs)) ** 2)
        add("SPARC", nm, R, gb, go, e_lgb, e_lgo, z, lSig)
COUNTS["SPARC"] = dict(files=NFILE, galaxies=len(SP), points=sum(len(g) for _, _, g, _ in SP))
P(f"SPARC: {NFILE} files, {len(SP)} galaxies, {COUNTS['SPARC']['points']} points (SHP1: 175 / 149 / 2700)")

# ============================================================== faint rotators (McQuinn+2022 t1, t2)
FR = os.path.join(DATA, "faint_rotators_mcquinn2022")
def mrt_rows(fn):
    L = open(os.path.join(FR, fn)).read().splitlines(); i = max(k for k, l in enumerate(L) if l.startswith("----"))
    return [l for l in L[i + 1:] if l.strip()]
T1 = {}
for l in mrt_rows("apjac9285t1_mrt.txt"):
    t = l.split(); T1[t[0]] = dict(D=float(t[1]), eD=float(t[2]), lMb=float(t[-2]), elMb=float(t[-1]))
ALIAS = {"HOII": "UGC04305"}
nfr, drop = 0, []
for l in mrt_rows("apjac9285t2_mrt.txt"):
    t = l.split(); nm = t[0]
    Rmax, eR, Vc, eVc = float(t[8]), float(t[9]), float(t[14]), float(t[15])
    key = ALIAS.get(norm(nm), norm(nm))
    if key in SPARC_FILES: drop.append(nm); continue
    d = T1[nm]; r = Rmax * KPC
    go = (Vc * 1e3) ** 2 / r; gb = G * 10 ** d["lMb"] * MS / r ** 2
    e_lgo = math.sqrt((2 * eVc / Vc) ** 2 + (eR / Rmax) ** 2) / LN10
    e_lgb = math.sqrt(d["elMb"] ** 2 + (2 * eR / Rmax / LN10) ** 2)
    eY = math.sqrt(((2 * eVc / Vc) ** 2 + (eR / Rmax) ** 2 + (d["eD"] / d["D"]) ** 2) / LN10 ** 2 + d["elMb"] ** 2)
    add("faint rotators", nm, Rmax, gb, go, e_lgb, e_lgo, z_of_D(d["D"]), eY=eY); nfr += 1
COUNTS["faint rotators"] = dict(rows=nfr, dropped_as_SPARC=drop)
P(f"faint rotators: {nfr} (dropped as SPARC files: {', '.join(drop)})")

# ============================================================== tidal dwarfs (Lelli+2015)
ntdg = 0
for r in csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"), encoding="utf-8-sig")):
    R, eR = float(r["R_out_kpc"]), float(r["e_R_out_kpc"]); V, eV = float(r["V_circ_kms"]), float(r["e_V_circ_kms"])
    Mb, eMb = float(r["M_bar_1e8"]) * 1e8, float(r["e_M_bar_1e8"]) * 1e8; rr = R * KPC
    go = (V * 1e3) ** 2 / rr; gb = G * Mb * MS / rr ** 2
    e_lgo = math.sqrt((2 * eV / V) ** 2 + (eR / R) ** 2) / LN10; e_lgb = math.sqrt((eMb / Mb) ** 2 + (2 * eR / R) ** 2) / LN10
    eY = math.sqrt((2 * eV / V) ** 2 + (eR / R) ** 2 + (eMb / Mb) ** 2) / LN10
    add("tidal dwarfs", r.get("object") or r.get("Object"), R, gb, go, e_lgb, e_lgo, z_of_D(float(r["dist_Mpc"])), eY=eY); ntdg += 1
COUNTS["tidal dwarfs"] = ntdg; P(f"tidal dwarfs: {ntdg}")

# ============================================================== massive spirals (Di Teodoro+2023), last tabulated point
def tsv(fn):
    L = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, fn)) if l.strip() and not l.startswith("#")]
    return [dict(zip(L[0], x)) for x in L[1:]]
DTS = {r["name"]: r for r in tsv("diteodoro2023_massive_spirals.tsv")}
DTC = {}
for r in tsv("diteodoro2023_hi_rotation_curves.tsv"): DTC.setdefault(r["name"], []).append((float(r["R_kpc"]), float(r["V_kms"]), float(r["dV_kms"])))
nms, mdrop = 0, []
for nm, s in DTS.items():
    if s["flag_uncertain"] == "1" or norm(nm) in SPARC_FILES or nm not in DTC: mdrop.append(nm); continue
    R, V, dV = max(DTC[nm]); rr = R * KPC
    Ms, Mg = 10 ** float(s["logMs_W1"]), 10 ** float(s["logMgas"]); Mb = Ms + Mg
    eMb = math.sqrt((Ms * 0.2 * LN10) ** 2 + (Mg * 0.1 * LN10) ** 2) / Mb / LN10
    go = (V * 1e3) ** 2 / rr; gb = G * Mb * MS / rr ** 2
    e_lgo = math.sqrt((2 * dV / V) ** 2 + (float(s["dD"]) / float(s["D_Mpc"])) ** 2) / LN10
    add("massive spirals", nm, R, gb, go, eMb, e_lgo, z_of_D(float(s["D_Mpc"]))); nms += 1
COUNTS["massive spirals"] = dict(rows=nms, dropped=mdrop); P(f"massive spirals: {nms} (dropped: {', '.join(mdrop)})")

# ============================================================== ATLAS3D (Cappellari+2013 XV, XX), r12, qual >= 1
na3 = 0
CHAB = 0.61
for r in tsv("atlas3d_fj_table.tsv"):
    try: q = int(r["qual"]); D = float(r["Dist_Mpc"]); lr12 = float(r["logr12"]); lRe = float(r["logRe"]); lL = float(r["logL"])
    except (ValueError, KeyError): continue
    try: mlj = float(r["logML_JAM"]); mls = float(r["logML_Salp"])
    except ValueError: continue
    if q < 1: continue
    r12 = 10 ** lr12 * math.pi / 180 / 3600 * D * 1e3; Re = 10 ** lRe * math.pi / 180 / 3600 * D * 1e3; L = 10 ** lL
    Md = L * 10 ** mlj / 2; Mbc = CHAB * L * 10 ** mls / 2; Mbs = L * 10 ** mls / 2
    rr = r12 * KPC
    for Mb, br in ((Mbc, ""), (Mbs, "atlas_salp")):
        lSig = math.log10(Mb / (math.pi * (Re * 1e3) ** 2))
        add("ATLAS3D", r["name"], r12, G * Mb * MS / rr ** 2, G * Md * MS / rr ** 2, 0.10, 0.05, z_of_D(D), lSig, bracket=br)
    na3 += 1
COUNTS["ATLAS3D"] = na3; P(f"ATLAS3D: {na3} (qual >= 1, both M/L columns present)")

# ============================================================== RC100 (FLD1's input file)
nrc = 0
for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv"))):
    Re, Vc, lM = float(r["Re_kpc"]), float(r["Vc_Re_kms"]), float(r["logMbar_Msun"]); rr = Re * KPC
    go = (Vc * 1e3) ** 2 / rr; gb = G * 10 ** lM / 2 * MS / rr ** 2
    lSig = math.log10(10 ** lM / 2 / (math.pi * (Re * 1e3) ** 2))
    add("RC100", r["name"], Re, gb, go, 0.20, 0.087, float(r["z"]), lSig); nrc += 1
COUNTS["RC100"] = nrc; P(f"RC100: {nrc}")

# ============================================================== KiDS B21 (SHP1's conversion), four mass bins; hot-gas Nobins bracket
B21 = os.path.join(DATA, "lensing_rar", "brouwer2021_rar")
CONV = 4 * G_PC * PC
def esd(fn):
    a = np.loadtxt(os.path.join(B21, fn), comments="#")
    return dict(gbar=a[:, 0], gobs=4 * G_PC * a[:, 1] / a[:, 4] * PC, esd=a[:, 1] / a[:, 4], bias=a[:, 4])
def cov_diag(fn, blocks):
    c = np.loadtxt(os.path.join(B21, fn), comments="#"); out = {}
    keys = [k for k, _ in blocks]; gmap = dict(blocks)
    for row in c:
        m, n, Ri, Rj, cv, _, bias = row[:7]
        km = min(keys, key=lambda k: abs(k - m)); kn = min(keys, key=lambda k: abs(k - n))
        if km != kn or abs(math.log(Ri / Rj)) > 1e-6: continue
        i = int(np.argmin(np.abs(np.log(gmap[km] / Ri)))); assert abs(math.log(gmap[km][i] / Ri)) < 1e-3
        out[(km, i)] = CONV ** 2 * cv / bias
    return out
LN = np.load(os.path.join(DATA, "lensing_rar", "lr_lenses.npz")); LZ, LM = LN["z"], LN["logM"]
MB_KEYS = (8.5, 10.3, 10.6, 10.8); MB_EDGES = (8.5, 10.3, 10.6, 10.8, 11.0); MREP = (9.4, 10.45, 10.7, 10.9)
MB = [esd(f"Fig-9_RAR-KiDS-isolated_Massbin-{i}.txt") for i in (1, 2, 3, 4)]
CD = cov_diag("Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt", [(k, d["gbar"]) for k, d in zip(MB_KEYS, MB)])
KZ = []
for j, (d, lm) in enumerate(zip(MB, MREP)):
    sel = (LM >= MB_EDGES[j]) & (LM < MB_EDGES[j + 1]); zb = float(np.median(LZ[sel])); KZ.append((int(sel.sum()), zb))
    for i, (gb, go) in enumerate(zip(d["gbar"], d["gobs"])):
        s = math.sqrt(CD[(MB_KEYS[j], i)]); r = math.sqrt(G * 10 ** lm * MS / gb) / KPC
        e_lgo = s / max(go, s) / LN10
        add("KiDS", f"KiDS bin {j + 1}", r, gb, go, 0.20, e_lgo, zb)
NOB = esd("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"); HOT = esd("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
CDH = cov_diag("Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt", [(-999.0, HOT["gbar"])])
same_esd = bool(np.allclose(NOB["esd"], HOT["esd"], rtol=1e-6))
selall = (LM >= 8.5) & (LM < 11.0); zall = float(np.median(LZ[selall]))
for i, (gb, go) in enumerate(zip(HOT["gbar"], HOT["gobs"])):
    s = math.sqrt(CDH[(-999.0, i)]); r = math.sqrt(G * 10 ** 10.45 * MS / gb) / KPC   # B21 stacks in g_bar bins; hot gas not in M_rep, so r is a lower bound
    add("KiDS", "KiDS Nobins hot gas", r, gb, go, 0.20, s / max(go, s) / LN10, zall, bracket="kids_hot")
COUNTS["KiDS"] = dict(bins=4, points_per_bin=[len(d["gbar"]) for d in MB], lens_count_and_median_z=KZ, hot_rows=len(HOT["gbar"]),
                      hot_esd_equals_published_esd=same_esd, zall=zall)
P(f"KiDS: 4 bins x {len(MB[0]['gbar'])} points; lenses / median z per bin {[(n, round(z, 3)) for n, z in KZ]}; "
  f"hot-gas Nobins {len(HOT['gbar'])} rows, its ESD equals the published Nobins ESD row by row: {same_esd}")

# ============================================================== Lovisari+2015 groups at R500 (RB1 / QX5 loader, KVM18 stars)
def kvm18(M500): return 1.7e12 * (M500 / 1e14) ** 0.60
ngr = 0
for r in tsv("lovisari2015_groups.tsv"):
    R5 = float(r["R500_kpc"]); M5, eM5 = float(r["M500_1e13"]) * 1e13, float(r["eM500"]) * 1e13
    Mg, eMg = float(r["Mgas500_1e12"]) * 1e12, float(r["eMgas500"]) * 1e12; Ms = kvm18(M5); rr = R5 * KPC
    Mb = Mg + Ms; eMb = math.sqrt(eMg ** 2 + (Ms * 0.2 * LN10) ** 2)
    add("groups", r["name"], R5, G * Mb * MS / rr ** 2, G * M5 * MS / rr ** 2, eMb / Mb / LN10, eM5 / M5 / LN10, float(r["z"])); ngr += 1
COUNTS["groups"] = ngr; P(f"groups (Lovisari+2015): {ngr}")

# ============================================================== X-COP (RB1 / HL3 loader), 7 with measured stars, 0.1 dex grid
def li(r, m, t):
    r = np.asarray(r, float); m = np.asarray(m, float)
    if t < r[0] or t > r[-1]: return float("nan")
    return float(10 ** np.interp(math.log10(t), np.log10(r), np.log10(m)))
XD = os.path.join(DATA, "xcop"); R5J = json.load(open(os.path.join(XD, "xcop_r500_ettori2019.json")))
XN = sorted(d for d in os.listdir(XD) if os.path.isdir(os.path.join(XD, d))); nxc, xw = 0, []
for name in XN:
    p_ = os.path.join(XD, name)
    if not os.path.exists(os.path.join(p_, f"{name}_mstar.fits")): xw.append(name); continue
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500h = float(h[1].header["R500"])
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy()
    with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    hr = np.array(hm["RADIUS"], float); hM = np.array(hm["M_FORW"], float); heM = np.array(hm["EM_FORW"], float)
    ok = np.isfinite(hM) & (hM > 0) & np.isfinite(heM); hr, hM, heM = hr[ok], hM[ok], heM[ok]
    gr = np.array(gas["RADIUS"], float) * r500h; gM = np.array(gas["MGAS"], float); gL = np.array(gas["MGAS_LO"], float); gH = np.array(gas["MGAS_HI"], float)
    ok = np.isfinite(gM) & (gM > 0) & (gr > 0) & np.isfinite(gL) & np.isfinite(gH) & (gL > 0); gr, gM, gL, gH = gr[ok], gM[ok], gL[ok], gH[ok]
    sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float); sL = np.array(st["MSTAR_LO"], float); sH = np.array(st["MSTAR_HI"], float)
    ok = np.isfinite(sM) & (sM > 0) & (sr > 0) & np.isfinite(sL) & np.isfinite(sH) & (sL > 0); sr, sM, sL, sH = sr[ok], sM[ok], sL[ok], sH[ok]
    r0 = max(30.0, gr[0]); k = 0; npt = 0
    while r0 * 10 ** (0.1 * k) <= gr[-1] * (1 + 1e-12):
        r = r0 * 10 ** (0.1 * k); k += 1
        md, emd = li(hr, hM, r), li(hr, heM, r); mg, mgl, mgh = li(gr, gM, r), li(gr, gL, r), li(gr, gH, r); ms, msl, msh = li(sr, sM, r), li(sr, sL, r), li(sr, sH, r)
        if not np.all(np.isfinite([md, emd, mg, mgl, mgh, ms, msl, msh])): continue
        rr = r * KPC; Mb = mg + ms; eMb = math.sqrt(((mgh - mgl) / 2) ** 2 + ((msh - msl) / 2) ** 2)
        add("X-COP", name, r, G * Mb * MS / rr ** 2, G * md * MS / rr ** 2, eMb / Mb / LN10, emd / md / LN10, float(R5J[name]["z"])); npt += 1
    nxc += 1
COUNTS["X-COP"] = dict(clusters=nxc, left_out_no_stars=xw); P(f"X-COP: {nxc} clusters with measured stars (left out: {', '.join(xw)})")

# ============================================================== CLASH (HL3's parse of Tian+2020; z from Umetsu+2016 table 1)
def ckey(name):
    n = name.replace("~", "").replace(" ", "").replace("*", "")
    m = re.match(r"^A(?:bell)?(\d+)$", n, re.I)
    if m: return "A" + m.group(1)
    m = re.search(r"(\d{4})", n); return m.group(1) if m else n
ZU = {}
for ln in open(os.path.join(EXT, "hl3", "umetsu16", "src", "table1.tex"), errors="replace"):
    if ln.lstrip().startswith("~~"):
        c = ln.split("&"); ZU[ckey(c[0])] = float(c[1].replace("$", ""))
ncl = 0; cln = set()
for line in open(os.path.join(DATA, "clash_rar_tian2020_fig2.tsv")):
    if line.startswith("#") or not line.strip(): continue
    f = line.rstrip("\n").split("\t")
    if len(f) < 7: continue
    try: r, a, b, ea, eb = (float(x) for x in f[2:7])
    except ValueError: continue
    nm = f[1].strip(); add("CLASH", nm, r, 10 ** a, 10 ** b, ea, eb, ZU[ckey(nm)]); ncl += 1; cln.add(nm)
COUNTS["CLASH"] = dict(points=ncl, clusters=len(cln), z_found=len(ZU)); P(f"CLASH: {ncl} points, {len(cln)} clusters, Umetsu z for {len(ZU)}")

# ============================================================== Local Group dwarfs (RB2's load_lvd and build default, central values)
CFG = os.path.join(REPO, "campaign_fresh_gravity"); R12 = 4.0 / 3.0
def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None
LVD = []
for fn, host in (("lvd_dwarf_mw.csv", "MW"), ("lvd_dwarf_m31.csv", "M31"), ("lvd_dwarf_local_field.csv", "field")):
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fn))):
        s = fl(r.get("vlos_sigma")); rh = fl(r.get("rhalf_sph_physical")) or fl(r.get("rhalf_physical"))
        ms = fl(r.get("mass_stellar")); mv = fl(r.get("M_V"))
        if not s or s <= 0 or not rh or rh <= 0: continue
        if ms is None and mv is not None: ms = 0.4 * (4.83 - mv) + 0.301
        if ms is None: continue
        rhe = fl(r.get("rhalf_sph_physical_em")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_em"))
        rhp = fl(r.get("rhalf_sph_physical_ep")) if fl(r.get("rhalf_sph_physical")) else fl(r.get("rhalf_physical_ep"))
        LVD.append(dict(name=r["name"], host=host, sigma=s, sem=fl(r.get("vlos_sigma_em")) or 0.1 * s, sep=fl(r.get("vlos_sigma_ep")) or 0.1 * s,
                        ul=bool(r.get("vlos_sigma_ul")), rh=rh, rhem=rhe or 0.1 * rh, rhep=rhp or 0.1 * rh, logms=ms,
                        dmem=fl(r.get("distance_modulus_em")) or 0.1, dmep=fl(r.get("distance_modulus_ep")) or 0.1, mv=mv, dist=fl(r.get("distance"))))
ARR = list(csv.DictReader(open(os.path.join(CFG, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"]) / float(r["sig_f0"]) for r in ARR}
med_free = float(np.median(list(arr_free.values())))
DROP = {"LMC", "SMC", "M 32", "Sagittarius"}
ndw = {}; nul = 0
for r in LVD:
    if r["name"] in DROP: continue
    if r["ul"]: nul += 1; continue
    if r["host"] == "MW": cls = "MW ultra-faints" if (r["mv"] is not None and r["mv"] > -7.7) else "MW bright dwarfs"
    elif r["host"] == "M31": cls = "M31 dwarfs"
    else: cls = "LG field dwarfs"
    b = arr_free.get(r["name"], med_free)
    s = r["sigma"] * b; es = (r["sem"] + r["sep"]) / 2 * b; rh = r["rh"]; erh = (r["rhem"] + r["rhep"]) / 2
    eDD = LN10 / 5 * (r["dmem"] + r["dmep"]) / 2
    r12 = R12 * rh * PC; Ms = 10 ** r["logms"]
    go = 3 * (s * 1e3) ** 2 / r12; gb = G * Ms / 2 * MS / r12 ** 2
    e_lgo = math.sqrt((2 * es / s) ** 2 + (erh / rh) ** 2) / LN10; e_lgb = math.sqrt(0.1 ** 2 + (2 * erh / rh / LN10) ** 2)
    eY = math.sqrt(((2 * es / s) ** 2 + (erh / rh) ** 2 + eDD ** 2) / LN10 ** 2 + 0.1 ** 2)
    lSig = math.log10(Ms / 2 / (math.pi * rh ** 2))
    D_Mpc = (r["dist"] or 0.0) / 1e3
    add(cls, r["name"], R12 * rh / 1e3, gb, go, e_lgb, e_lgo, z_of_D(D_Mpc), lSig, eY=eY); ndw[cls] = ndw.get(cls, 0) + 1
COUNTS["LG dwarfs"] = dict(per_class=ndw, upper_limits_dropped=nul, binary_factor_median=med_free, binary_listed=len(arr_free))
P(f"LG dwarfs: {ndw}; sigma upper limits dropped {nul}; RB2 binary factor: {len(arr_free)} listed, median {med_free:.3f} for the rest")

# ============================================================== Coma UDGs (Freundlich+2022, RB2's loader) and NGC 1052 UDGs (RB2's values)
FRE = tsv("freundlich2022_coma_udgs.tsv"); ka3_coma = []
for r in FRE:
    try: sig, esig = float(r["sig"]), float(r["esig"])
    except ValueError: continue
    Ms = float(r["L_1e8"]) * 1e8 * float(r["ML"]); Re = float(r["Re_kpc"]); r12 = R12 * Re * KPC
    go = 3 * (sig * 1e3) ** 2 / r12; gb = G * Ms / 2 * MS / r12 ** 2
    e_lgo = math.sqrt((2 * esig / sig) ** 2 + 0.1 ** 2) / LN10; e_lgb = math.sqrt(0.2 ** 2 + (0.2 / LN10) ** 2)
    eY = math.sqrt(((2 * esig / sig) ** 2 + 0.1 ** 2) / LN10 ** 2 + 0.2 ** 2)
    add("Coma UDGs", r["name"], R12 * Re, gb, go, e_lgb, e_lgo, 0.0231, math.log10(Ms / 2 / (math.pi * (Re * 1e3) ** 2)), eY=eY)
    ka3_coma.append(dict(name=r["name"], d_lgb=math.log10(gb) - float(r["lgbar"]), d_lgo=math.log10(go) - float(r["lgobs"])))
DFG = {"DF2": dict(Ms=2.0e8, Re=2.0, D=20.0, obs=(8.5, 2.3, 3.1)), "DF4": dict(Ms=1.5e8, Re=1.6, D=20.0, obs=(6.3, 2.5, 1.6))}  # RB2's values
for nm, d in DFG.items():
    s, ep, em = d["obs"]; es = (ep + em) / 2; r12 = R12 * d["Re"] * KPC
    go = 3 * (s * 1e3) ** 2 / r12; gb = G * d["Ms"] / 2 * MS / r12 ** 2
    eY = math.sqrt(((2 * es / s) ** 2 + 0.1 ** 2) / LN10 ** 2 + 0.2 ** 2)
    add("NGC 1052 UDGs", nm, R12 * d["Re"], gb, go, 0.2, math.sqrt((2 * es / s) ** 2 + 0.1 ** 2) / LN10, z_of_D(d["D"]),
        math.log10(d["Ms"] / 2 / (math.pi * (d["Re"] * 1e3) ** 2)), eY=eY)
COUNTS["Coma UDGs"] = len(ka3_coma); COUNTS["KA3_coma"] = ka3_coma
P(f"Coma UDGs: {len(ka3_coma)}; NGC 1052 UDGs: 2")

# ============================================================== last-point flags, write
bykey = {}
for i, r in enumerate(ROWS): bykey.setdefault((r["cls"], r["sys"], r["bracket"]), []).append(i)
for k, idx in bykey.items():
    j = max(idx, key=lambda i: ROWS[i]["r_kpc"]); ROWS[j]["last"] = 1
COLS = ["cls", "sys", "bracket", "r_kpc", "lgb", "lgo", "e_lgb", "e_lgo", "eY", "z", "lSig", "last"]
with open(os.path.join(HERE, "dd1_table.csv"), "w", newline="") as fh:
    fh.write("# DD1 frozen table (dd1_table.py, criteria 2a3f76f295). lgb/lgo = log10 g_bar/g_obs [m/s^2]; eY dex; lSig log10 Msun/pc^2 "
             "(nan = not covered); bracket '' = main table. kappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
    w = csv.writer(fh); w.writerow(COLS)
    for r in ROWS: w.writerow([r[c] if isinstance(r[c], str) else (repr(r[c]) if c != "last" else r[c]) for c in COLS])
main = [r for r in ROWS if r["bracket"] == ""]
P(); P(f"table: {len(ROWS)} rows ({len(main)} main), classes {len({r['cls'] for r in main})}, systems {len({(r['cls'], r['sys']) for r in main})}")
P("per class (main): points / systems / lg g_bar range / g_obs <= 0 points")
for c in sorted({r["cls"] for r in main}, key=lambda c: min(i for i, r in enumerate(ROWS) if r["cls"] == c)):
    rr = [r for r in main if r["cls"] == c]
    P(f"  {c:18s} {len(rr):5d} {len({r['sys'] for r in rr}):4d}  {min(r['lgb'] for r in rr):7.2f} {max(r['lgb'] for r in rr):7.2f}  {sum(1 for r in rr if not math.isfinite(r['lgo']))}")
json.dump(COUNTS, open(os.path.join(HERE, "dd1_table_counts.json"), "w"), indent=1)
P(f"runtime {time.time() - T0:.1f} s"); P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, "dd1_table.out"), "w").write("\n".join(OUT) + "\n")
