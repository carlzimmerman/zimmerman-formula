"""RS1: all classes as one row table, per footing and Upsilon reading. CRG1's inputs read-only. FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, os.path.join(RB, "HF1_hybrid_fermion")); sys.dont_write_bytecode = True
import hf1_crgload as HL; HL.crg()
import crg1_core as CO, crg1_clusters as C, crg1_sparc as SP, crg1_groups as GR, crg1_dwarfs as DW
from astropy.io import fits
np.seterr(all="ignore")
G = 6.674e-11; MS = 1.989e30; PC = 3.0857e16; CL = 299792458.0; A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312e-10}
UPS = {"U50": (0.5, 0.7), "low": (0.41, 0.574)}; CLS = ["S", "LT", "G3", "G6", "X", "L", "Dw"]; INP = os.path.join(RB, "CRG1_clean_room_regrade", "inputs")
def table(foot, ups):
    R = []
    def add(c, name, sub, tr, r, gobs, gg, gs, Mbt, err=np.nan, sig=np.nan, weight=1.0):
        gb = gg + gs; R.append(dict(c=c, name=name, sub=sub, tr=tr, r=r, gobs=gobs, gg=gg, gs=gs, gb=gb, Mbt=Mbt, err=err, sig=sig))
    Yd, Yb = UPS[ups]; KMS2 = 1e6
    gal = {g["name"]: g for g in SP.load_gal()}; names = sorted(gal)
    for i, n in enumerate(names):
        g = gal[n]
        if g["Q"] >= 3 or g["Inc"] < 30: continue
        mbt = (Yd * g["L36"] + 1.33 * g["MHI"]) * 1e9 * MS; sig = float(np.max(g["Vobs"])) * 1e3 / math.sqrt(2)
        for rk, v, e, vg, vd, vb in zip(g["Rk"], g["Vobs"], g["eV"], g["Vgas"], g["Vdisk"], g["Vbul"]):
            m = abs(vg) * vg + Yd * abs(vd) * vd + Yb * abs(vb) * vb; r = rk * 1e3 * PC
            if rk <= 0 or v <= 0 or m <= 0: continue
            add("S", n, "", i % 2 == 1, r, v * v * KMS2 / r, abs(vg) * vg * KMS2 / r, (Yd * abs(vd) * vd + Yb * abs(vb) * vb) * KMS2 / r, mbt, 2 * e / v / math.log(10), sig)
    lt = []
    for q in csv.DictReader(open(os.path.join(INP, "little_things", "oh2015_table2.csv"))):
        if all(q[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun")): lt.append(q)
    lt.sort(key=lambda q: q["name"])
    for i, q in enumerate(lt):
        r = float(q["Rmax_kpc"]) * 1e3 * PC; v = float(q["V_kms"]) * 1e3; mg = float(q["Mgas_1e7Msun"]) * 1e7 * MS; ms = float(q["MSED_1e7Msun"]) * 1e7 * MS
        add("LT", q["name"], "", i % 2 == 0, r, v * v / r, G * mg / r ** 2, G * ms / r ** 2, mg + ms, np.nan, v / math.sqrt(2))
    gr = sorted(GR.load(), key=lambda t: (t[1], t[0]))
    for i, (ls, lM, Re) in enumerate(gr):
        r = 4 / 3 * Re * 1e3 * PC; s = 10 ** ls * 1e3; Mb = 10 ** lM * MS
        for c, f in (("G3", 0.3), ("G6", 0.6)):
            add(c, f"g{i}", "", i % 2 == 0, r, 3 * s * s / r, G * f * Mb / 2 / r ** 2, G * (1 - f) * Mb / 2 / r ** 2, Mb, np.nan, s)
    for j, c in enumerate(C.xcop_load()):
        Mg5 = C.li(c["gr"], c["gm"], c["R500"]); Ms5 = C.li(c["sr"], c["sm"], c["R500"]); xs = [x for x in C.XS]
        rr = [(x, C.li(c["hr"], c["hm"], x * c["R500"]), C.li(c["gr"], c["gm"], x * c["R500"]), C.li(c["sr"], c["sm"], x * c["R500"])) for x in xs]
        rr = [t for t in rr if all(map(np.isfinite, t))]; vm = max(math.sqrt(G * t[1] * MS / (t[0] * c["R500"] * 1e3 * PC)) for t in rr)
        mbt = ((Mg5 if np.isfinite(Mg5) else rr[-1][2]) + (Ms5 if np.isfinite(Ms5) else rr[-1][3])) * MS
        for x, mh, mg, ms in rr:
            r = x * c["R500"] * 1e3 * PC; add("X", c["name"], f"{x}", j % 2 == 0, r, G * mh * MS / r ** 2, G * mg * MS / r ** 2, G * ms * MS / r ** 2, mbt, np.nan, vm / math.sqrt(2))
    d = np.load(os.path.join(INP, "lensing", "lens_inventory.npz")); bins = np.digitize(d["logM"], [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
    for b in range(4):
        a = np.loadtxt(os.path.join(INP, "lensing", f"Fig-3_Lensing-rotation-curves_Massbin-{b + 1}.txt"), comments="#"); s = bins == b
        Ms_ = float(np.average(10 ** d["logM"][s], weights=d["WLENS"][s])) * MS; Mg_ = Ms_ * 0.2 / 0.8
        for rm, e, er, k in zip(a[:, 0], a[:, 1], a[:, 3], a[:, 4]):
            ds = e / k; ee = er / k
            if rm > 0.3 or ds <= 0: continue
            r = rm * 1e6 * PC; add("L", f"bin{b + 1}", "", b % 2 == 0, r, 4 * G * ds * MS / PC ** 2, G * Mg_ / r ** 2, G * Ms_ / r ** 2, Mg_ + Ms_, ee / ds / math.log(10), np.nan)
    dw = [q for q in DW.load(foot) if q["cls"] in DW.CLASSES]; 
    for cl in DW.CLASSES:
        for i, q in enumerate(sorted([q for q in dw if q["cls"] == cl], key=lambda q: q["name"])):
            add("Dw", q["name"], cl, i % 2 == 0, q["r12"], q["gobs"], 0.0, q["gN"], 2 * q["gN"] * q["r12"] ** 2 / DW.D.G * MS / DW.D.Msun, q["s"], math.sqrt(q["gobs"] * q["r12"] / 3))
    return R
def arrays(R):
    A = {k: np.array([q[k] for q in R], float) for k in ("r", "gobs", "gg", "gs", "gb", "Mbt", "err", "sig")}
    A["c"] = np.array([CLS.index(q["c"]) for q in R]); A["tr"] = np.array([bool(q["tr"]) for q in R]); A["name"] = np.array([q["name"] for q in R]); A["sub"] = np.array([q["sub"] for q in R]); return A
def leaves(A, a0):
    gg = np.maximum(A["gg"], 0.0); gb = A["gb"]; r = A["r"]
    return dict(y_g=gg / a0, y_s=np.maximum(A["gs"], 1e-30) / a0, f=np.clip(gg / gb, 0, 1), ell=r * a0 / CL ** 2, mu=G * A["Mbt"] * a0 / CL ** 4, x=r / np.sqrt(G * A["Mbt"] / a0))
def law(g, a0): return 0.5 * g + np.sqrt(0.25 * g * g + a0 * g)
def greq(gobs, a0): return gobs ** 2 / (gobs + a0)
