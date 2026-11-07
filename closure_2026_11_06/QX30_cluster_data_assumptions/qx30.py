#!/usr/bin/env python3
"""QX30 (criteria f861a41f04): LCDM-based assumptions inside the hot-system data, re-derived where the published
products on disk allow it.
    python3 qx30.py            # graded: qx30.json / qx30.out
    python3 qx30.py --mutate   # M1 opposite sign, M2 swap back, M3 h 0.35 plant: qx30_MUTATE.json / .out
Graders are reused read-only: QX2's X-COP builder + gate (qx2.py executed up to its output block) and QX5's
(QX16-fixed) group / elliptical loaders (qx5.py executed up to its sample line), exactly as QX20 does.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, csv
import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "qx30_MUTATE" if MUT else "qx30"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)

def load_prefix(path, marker, name):
    src = open(path).read(); cut = src.index(marker)
    NS = {"__file__": path, "__name__": name}
    argv = sys.argv; sys.argv = [sys.argv[0]]
    exec(compile(src[:cut], name, "exec"), NS); sys.argv = argv
    return NS
Q2 = load_prefix(os.path.join(REPO, "closure_2026_11_06", "QX2_clusters", "qx2.py"), "OUTJ = dict(", "qx2_lib")
Q5 = load_prefix(os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py"), "XC, SP, EL, LE, GR = ", "qx5_lib")
G, MS, KPC, C = Q2["G"], Q2["MS"], Q2["KPC"], Q2["C"]
A0 = Q2["A0"]; law_M, gate, li = Q2["law_M"], Q2["gate"], Q2["li"]; glaw = Q5["glaw"]
DATA = os.path.join(REPO, "real_research", "data")
QX2J = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX2_clusters", "qx2.json")))
QX20J = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX20_failure_ladder", "qx20.json")))

# ---------------- backgrounds ----------------
def chi(z, h, om, n=4000):  # comoving distance [Mpc], flat, radiation neglected
    zz = np.linspace(0.0, z, n + 1); E = np.sqrt(om * (1 + zz) ** 3 + (1 - om))
    return (C / 1e3) / (100 * h) * float(np.trapz(1 / E, zz))
def DA(z, h, om): return chi(z, h, om) / (1 + z)
NAT = dict(h=0.674, om=0.3085)
RHO_DE_CAN = A0["canonical"] ** 2 / (0.25 * C ** 2 * G)
RHO_C100 = 3 * (100e3 / 3.0857e22) ** 2 / (8 * math.pi * G)  # rho_crit for h = 1 [kg/m^3]
H_CAN = math.sqrt(RHO_DE_CAN / RHO_C100 / (1 - NAT["om"]))
H_ALT = math.sqrt((A0["alt"] ** 2 / (0.25 * C ** 2 * G)) / RHO_C100)
FID = dict(xcop=dict(h=0.70, om=0.30), groups=dict(h=0.70, om=0.27), ell=dict(h=0.70, om=0.30), coma=dict(h=0.70, om=0.30))
def fratio(z, bg, sample):
    fd = FID[sample]; return DA(z, bg["h"], bg["om"]) / DA(z, fd["h"], fd["om"])

# KA3: distance code
eds = chi(0.5, 0.7, 1.0); eds_an = (C / 1e3) / 70 * 2 * (1 - 1 / math.sqrt(1.5))
ka3 = abs(eds / eds_an - 1)
try:
    from astropy.cosmology import FlatLambdaCDM
    ap = FlatLambdaCDM(H0=70, Om0=0.3, Tcmb0=0).angular_diameter_distance(0.06).value
    ka3b = abs(DA(0.06, 0.7, 0.3) / ap - 1)
except Exception:
    ka3b = None
P(f"QX30 {TAG}: kappa = 1/2 FITTED; footings never pooled; + = model short")
P(f"KA3 distance: EdS rel err {ka3:.2e}; astropy rel err {ka3b if ka3b is None else f'{ka3b:.2e}'} -> {'PASS' if ka3 <= 1e-6 and (ka3b is None or ka3b <= 1e-6) else 'FAIL'}")
P(f"native h: primary {NAT['h']} (QX15; alt a0 gives h = {H_ALT:.4f}); canonical-consistent h (Omega_m 0.3085) = {H_CAN:.4f} [reported]")

# ---------------- X-COP rows with gas / stars split (QX2's builder, same files and radii) ----------------
COLS = ["M_FORW", "M_NFW", "M_EIN", "M_ISO", "M_BUR"]
XR = []
for c in Q2["XC"]:
    name = c["name"]; p_ = os.path.join(DATA, "xcop", name)
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500 = h[1].header["R500"]; z = h[1].header["REDSHIFT"]
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); rg500 = h[1].header["R500"]
    with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    for row in c["rows"]:
        r = row["r_kpc"]; mg = li(gas["RADIUS"] * rg500, gas["MGAS"], r); ms = li(st["RADIUS"], st["MSTAR"], r)
        cols = {k: li(hm["RADIUS"], hm[k], r) for k in COLS}
        XR.append(dict(name=name, z=z, x=row["x"], r=r, Mg=mg, Ms=ms, eM=row["eM"], cols=cols, Mb_q2=row["M_b"], MH_q2=row["M_HSE"]))
P(f"X-COP: {len(set(r['name'] for r in XR))} clusters, {len(XR)} points (QX2 builder); z range {min(r['z'] for r in XR):.4f}-{max(r['z'] for r in XR):.4f}")

def xcop_grade(bg=None, beta=1.0, col="M_FORW", gasx=1.0, starx=1.0):
    """Rebuild QX2's rows under a background / convention and run QX2's own gate on them."""
    rows_by = {}
    for r in XR:
        f = fratio(r["z"], bg, "xcop") if bg else 1.0
        MH = r["cols"][col]
        if not np.isfinite(MH): continue
        rows_by.setdefault(r["name"], []).append(dict(x=r["x"], r_kpc=f * r["r"], M_HSE=f ** beta * MH,
                                                      M_b=gasx * f ** 2.5 * r["Mg"] + starx * f ** 2 * r["Ms"], eM=f ** beta * r["eM"]))
    Q2["XC"] = [dict(name=k, rows=v) for k, v in rows_by.items()]
    res = gate(lambda c, z, a0: law_M(z["M_b"], z["r_kpc"], a0)[0])
    return {fo: dict(mean=v["mean"], rms=v["rms"], n=v["n"], PASS=v["PASS"]) for fo, v in res.items()}

# ---------------- groups / ellipticals (QX5 loaders, QX20 class-mean definitions) ----------------
GR = Q5["groups"](); EL = Q5["ellipticals"]()
GZ = {l.split("\t")[0]: float(l.split("\t")[1]) for l in open(os.path.join(DATA, "lovisari2015_groups.tsv")) if not l.startswith(("#", "name"))}
def groups_mean(a0, bg=None, beta=1.0, fst=0.5, gasx=1.0):
    d = []
    for gp in GR:
        f = fratio(GZ[gp["name"]], bg, "groups") if bg else 1.0
        for p in gp["pts"]:
            rm = f * p["r_kpc"] * KPC; Mb = gasx * f ** 2.5 * p["M_gas"] + fst * f ** 2 * p["M_gas"]
            gN = G * Mb * MS / rm ** 2; Ml = glaw(gN, a0) * rm ** 2 / G / MS
            d.append(math.log10(f ** beta * p["M_obs"] / Ml))
    return float(np.mean(d))
_ER = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "humphrey2006_ellipticals.tsv")) if not l.startswith("#")]
SALP = {r[0]: float(r[10]) / float(r[9]) for r in _ER[1:]}  # Humphrey+2006 SPS Upsilon_K Salpeter / Kroupa, per galaxy (QX18's systematic)
Z6482 = 4116.0 / 299792.458  # LEDA kinematic distance 58.8 Mpc at h70 (Humphrey+2006 Table 1 note); f is insensitive to z here
def ell_mean(a0, bg=None, beta=1.0, salp=False):
    d = []
    for e in EL:
        f = fratio(Z6482, bg, "ell") if (bg and e["name"] == "NGC6482") else 1.0
        for m in (2, 4, 8):
            r = m * e["Re"]; Mo = f ** beta * e["Mtot"](r); Mb = (SALP[e["name"]] if salp else 1.0) * f ** 2 * e["Mbar"](r); rm = f * r * KPC
            gN = G * Mb * MS / rm ** 2; Ml = glaw(gN, a0) * rm ** 2 / G / MS
            d.append(math.log10(Mo / Ml))
    return float(np.mean(d))
UDG = {fo: QX20J[fo]["udg_mean"] for fo in A0}
Z_COMA = 0.0231

RES = dict(tag=TAG, criteria="f861a41f04", note="kappa = 1/2 FITTED; not theory closed", native=NAT, h_can_consistent=H_CAN, h_alt=H_ALT,
           KA3=dict(eds=ka3, astropy=ka3b))

# ---------------- KA1 / KA2 ----------------
base_x = xcop_grade()
ka1 = max(max(abs(base_x[fo]["mean"] - QX2J["iter1"][fo]["mean"]), abs(base_x[fo]["rms"] - QX2J["iter1"][fo]["rms"])) for fo in A0)
P(f"KA1 X-COP f = 1 vs QX2 iter 1: max |d| {ka1:.2e} -> {'PASS' if ka1 <= 1e-9 else 'FAIL'}")
base = {fo: dict(X=base_x[fo]["mean"], Xrms=base_x[fo]["rms"], G=groups_mean(a0), G0=groups_mean(a0, fst=0.0), G1=groups_mean(a0, fst=1.0),
                 E=ell_mean(a0), U=UDG[fo]) for fo, a0 in A0.items()}
ka2 = max(max(abs(base[fo]["G"] - QX20J[fo]["class_means"]["G"]), abs(base[fo]["E"] - QX20J[fo]["class_means"]["E"]),
              abs(base[fo]["G0"] - QX20J[fo]["groups_fst0"]), abs(base[fo]["G1"] - QX20J[fo]["groups_fst1"])) for fo in A0)
P(f"KA2 groups / ellipticals f = 1 vs QX20 class means: max |d| {ka2:.2e} -> {'PASS' if ka2 <= 1e-6 else 'FAIL'}")
RES.update(KA1=ka1, KA2=ka2, baseline=base)
for fo in A0:
    b = base[fo]; P(f"  [{fo}] baseline: X-COP {b['X']:+.4f} (rms {b['Xrms']:.4f}); groups f*0.5 {b['G']:+.4f} [f*0 {b['G0']:+.4f}, f*1 {b['G1']:+.4f}]; ellipticals {b['E']:+.4f}; UDGs {b['U']:+.3f}")

fx = [fratio(r["z"], NAT, "xcop") for r in XR]; fg = [fratio(z, NAT, "groups") for z in GZ.values()]
P(f"native/fiducial D_A ratio f: X-COP {min(fx):.4f}-{max(fx):.4f}; groups {min(fg):.4f}-{max(fg):.4f}; NGC6482 {fratio(Z6482, NAT, 'ell'):.4f}; Coma {fratio(Z_COMA, NAT, 'coma'):.4f}")

def label(shift, after):
    if abs(after["mean"]) <= 0.05 and after["rms"] <= 0.10: return "ARTEFACT"
    return "PARTIAL" if abs(shift) >= 0.1 else "ROBUST"

if not MUT:
    # ---------------- C1: framework-native D_A (graded) ----------------
    c1 = xcop_grade(bg=NAT, beta=1.0)
    RES["C1"] = {}
    P("C1 framework-native D_A (h 0.674, Omega_m 0.3085, beta = 1) -- GRADED")
    for fo, a0 in A0.items():
        sx = c1[fo]["mean"] - base[fo]["X"]; g = groups_mean(a0, NAT); g0 = groups_mean(a0, NAT, fst=0.0); g1 = groups_mean(a0, NAT, fst=1.0); e = ell_mean(a0, NAT)
        fc = fratio(Z_COMA, NAT, "coma"); us = [(1 - p) * math.log10(fc) for p in (2, 3)]
        lab = label(sx, c1[fo])
        gl = "inside" if (min(g0, g1) <= 0.05 and max(g0, g1) >= -0.05) else "outside"
        RES["C1"][fo] = dict(X=c1[fo], X_shift=sx, label=lab, G=g, G_shift=g - base[fo]["G"], G0=g0, G1=g1, G_line=gl, E=e, E_shift=e - base[fo]["E"],
                             E_line="inside" if abs(e) <= 0.15 else "outside", U_shift_bracket=us, U=[UDG[fo] + s for s in us])
        P(f"  [{fo}] X-COP {c1[fo]['mean']:+.4f} (shift {sx:+.4f}), rms {c1[fo]['rms']:.4f} -> LABEL {lab}")
        P(f"  [{fo}] groups f*0.5 {g:+.4f} (shift {g - base[fo]['G']:+.4f}); bracket [{g1:+.4f}, {g0:+.4f}] -> {gl} the line")
        P(f"  [{fo}] ellipticals {e:+.4f} (shift {e - base[fo]['E']:+.5f}; only NGC 6482 moves) -> {'inside' if abs(e) <= 0.15 else 'outside'} G7")
        P(f"  [{fo}] Coma UDGs: shift bracket {us[1]:+.4f} to {us[0]:+.4f} (p 3..2, not re-solved) -> {UDG[fo] + us[1]:+.3f} to {UDG[fo] + us[0]:+.3f}")

    # ---------------- reported sensitivities (not graded) ----------------
    RES["sens"] = {}
    P("REPORTED (not graded): one assumption at a time on X-COP, mean shift canonical / alt")
    def rep(tag, **kw):
        r = xcop_grade(**kw); s = {fo: r[fo]["mean"] - base[fo]["X"] for fo in A0}
        RES["sens"][tag] = dict(shift=s, mean={fo: r[fo]["mean"] for fo in A0}, rms={fo: r[fo]["rms"] for fo in A0}, n=r["canonical"]["n"])
        P(f"  {tag:<46s} {s['canonical']:+.4f} / {s['alt']:+.4f}   -> mean {r['canonical']['mean']:+.4f} / {r['alt']['mean']:+.4f} (n {r['canonical']['n']})")
    rep("native D_A, beta = 1/2 (SZ pressure end)", bg=NAT, beta=0.5)
    rep(f"native D_A, h {H_CAN:.4f} (canonical-consistent)", bg=dict(h=H_CAN, om=NAT["om"]), beta=1.0)
    rep("native D_A, h 0.70", bg=dict(h=0.70, om=NAT["om"]), beta=1.0)
    rep("native D_A, h 0.73", bg=dict(h=0.73, om=NAT["om"]), beta=1.0)
    rep("Omega_m 0.3085 only (h 0.70)", bg=dict(h=0.70, om=0.3085), beta=1.0)
    for col in COLS[1:]: rep(f"mass-model column {col}", col=col)
    rep("clumping: gas x 1.1 (mean, not median)", gasx=1.1)
    rep("stars x 1/0.75 (no deprojection)", starx=1 / 0.75)
    rep("stars x 1/0.6 (ICL 40 % of stellar light)", starx=1 / 0.6)
    rep("stars x 1.8 (Salpeter vs Chabrier)", starx=1.8)
    nt = {fo: math.log10(1 / 0.94) for fo in A0}
    RES["sens"]["non-thermal 6 % at R500 (INADMISSIBLE)"] = dict(shift=nt, note="M_true = M_HSE/0.94 at R500 (Eckert+2019); upper end, applies fully only at R500")
    P(f"  {'non-thermal 6 % at R500 (INADMISSIBLE)':<46s} {nt['canonical']:+.4f} / {nt['alt']:+.4f}   (M_HSE / 0.94; makes the miss larger)")
    # best (most favourable) column per footing
    colmeans = {col: xcop_grade(col=col) for col in COLS}
    best = {fo: min(COLS, key=lambda k: colmeans[k][fo]["mean"]) for fo in A0}
    P(f"  most favourable mass-model column: {best}")

    # ---------------- all-favourable bound ----------------
    RES["bound"] = {}
    P("ALL-FAVOURABLE BOUND (every BOUND at its favourable end + C1 with h 0.671, beta 1/2; reported, sets no label)")
    hb = dict(h=H_CAN, om=NAT["om"])
    for fo, a0 in A0.items():
        r = xcop_grade(bg=hb, beta=0.5, col=best[fo], gasx=1.1, starx=1.8 / 0.75 / 0.6)[fo]
        g = groups_mean(a0, hb, beta=0.5, fst=1.0, gasx=1.1); e = ell_mean(a0, hb, beta=0.5, salp=True); es = ell_mean(a0, salp=True)
        RES["bound"][fo] = dict(X=r, G=g, E=e, E_salpeter_only=es)
        P(f"  [{fo}] X-COP {r['mean']:+.4f} rms {r['rms']:.4f} (shift {r['mean'] - base[fo]['X']:+.4f}) -> {'inside' if r['PASS'] else 'outside'} the HO1 line;"
          f" groups (f* 1, gas x1.1) {g:+.4f}; ellipticals (Salpeter, per-galaxy SPS ratio) {e:+.4f} [Salpeter alone {es:+.4f}, QX18 +0.071/+0.053]")
    lab = {fo: RES["C1"][fo]["label"] for fo in A0}
    RES["label"] = lab; P(f"LANE LABEL (X-COP, C1): canonical {lab['canonical']}, alt {lab['alt']}")
else:
    RES["M"] = {}
    inv = {k: v for k, v in NAT.items()}
    # M1 opposite sign: f -> 1/f, implemented as a background whose D_A ratio is the inverse
    c1 = xcop_grade(bg=NAT, beta=1.0)
    rows_saved = list(XR)
    for r in XR: r["_f"] = fratio(r["z"], NAT, "xcop")
    def xcop_inv():
        rows_by = {}
        for r in XR:
            f = 1 / r["_f"]; rows_by.setdefault(r["name"], []).append(dict(x=r["x"], r_kpc=f * r["r"], M_HSE=f * r["cols"]["M_FORW"], M_b=f ** 2.5 * r["Mg"] + f ** 2 * r["Ms"], eM=f * r["eM"]))
        Q2["XC"] = [dict(name=k, rows=v) for k, v in rows_by.items()]
        return gate(lambda c, z, a0: law_M(z["M_b"], z["r_kpc"], a0)[0])
    m1 = xcop_inv()
    for fo in A0:
        s, si = c1[fo]["mean"] - base[fo]["X"], m1[fo]["mean"] - base[fo]["X"]
        ok = abs(si + s) <= 0.15 * abs(s)
        RES["M"].setdefault("M1", {})[fo] = dict(shift_C1=s, shift_inv=si, BITES=bool(ok))
        P(f"M1 [{fo}] opposite sign: C1 shift {s:+.5f}, inverse shift {si:+.5f} -> {'BITES' if ok else 'NO BITE'}")
    # M2 swap back to each source's fiducial
    m2 = xcop_grade(bg=FID["xcop"], beta=1.0)
    for fo, a0 in A0.items():
        dx = abs(m2[fo]["mean"] - base[fo]["X"]); dg = abs(groups_mean(a0, FID["groups"]) - base[fo]["G"]); de = abs(ell_mean(a0, FID["ell"]) - base[fo]["E"])
        ok = dx <= 1e-9 and dg <= 1e-6 and de <= 1e-6
        RES["M"].setdefault("M2", {})[fo] = dict(dX=dx, dG=dg, dE=de, BITES=bool(ok))
        P(f"M2 [{fo}] swap back to fiducial: |dX| {dx:.1e}, |dG| {dg:.1e}, |dE| {de:.1e} -> {'REPRODUCES (BITES)' if ok else 'FAIL'}")
    # M3 power plant
    m3 = xcop_grade(bg=dict(h=0.35, om=NAT["om"]), beta=1.0)
    for fo in A0:
        s = m3[fo]["mean"] - base[fo]["X"]; ok = abs(s) >= 0.1
        RES["M"].setdefault("M3", {})[fo] = dict(shift=s, BITES=bool(ok))
        P(f"M3 [{fo}] planted h 0.35: X-COP mean {m3[fo]['mean']:+.4f} (shift {s:+.4f}) -> {'BITES' if ok else 'NO BITE'}")

json.dump(RES, open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
