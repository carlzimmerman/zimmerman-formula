"""CX1 rows: RS1's row table (rs1_rows.table, read-only) rebuilt per system with its error ingredients, then Monte Carlo of the leaves
(SY1's sy1_leaves, imported) and the required boost B = g_obs / g_law(g_b). See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, sys
import numpy as np
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RB, "RS1_required_source")); sys.path.insert(0, os.path.join(RB, "SY1_free_constant_law_search"))
import rs1_rows as R
from sy1_leaves import A0C, CL, slope_1d, D_leaf
from astropy.io import fits
np.seterr(all="ignore")
G, MS, PC = R.G, R.MS, R.PC
A0 = {"canonical": A0C, "alt": 1.1312e-10}
NMC = 400; SEED = 20261103; E_SD = 0.15
INP = R.INP
BS1 = json.load(open(os.path.join(RB, "BS1_basin_switch", "bs1_basin_switch_results.json")))
LG_LGM = BS1["LG"]["basin"]["lgM"]; R0D = BS1["LG"]["R0_data_kpc"]; FIELD_R = BS1["LG"]["field_R_kpc"]
BASIN_SP = BS1["primary_basins"]["lgM_basin_sparc"]["A_c2b_refit"]; NODIST = set(BS1["primary_basins"]["no_dist"])
EM1 = (11.18, 0.90)
def lgM200(lMb): return EM1[0] + EM1[1] * (lMb - 10.0)
def mb_of_mstar(Ms):
    l = math.log10(Ms); return Ms * (1.0 + 10 ** (-0.69 * l + 6.63)) if 8.5 <= l <= 11.0 else 1.2 * Ms      # BS1's A1
def norm(n): import re; n = n.upper().replace(" ", ""); return re.sub(r"(?<=[A-Z])0+(?=\d)", "", n)
ALIAS = {norm(a): norm(b) for a, b in [("DDO 50", "UGC04305"), ("DDO 87", "UGC05918"), ("DDO 126", "UGC07559"), ("Haro 29", "UGCA281"),
                                        ("WLM", "UGCA444"), ("DDO 210", "Aquarius"), ("DDO 216", "Pegasus dIrr")]}
def sysid(n): k = norm(n); return ALIAS.get(k, k)
LG_IDENT = {sysid(x) for x in ("IC 1613", "Aquarius", "Pegasus dIrr", "UGCA444")}

def mrt():
    T = {}
    for l in open(os.path.join(INP, "sparc", "SPARC_Lelli2016c.mrt")):
        t = l.split()
        if len(t) != 19: continue
        try: T[t[0]] = dict(D=float(t[2]), eD=float(t[3]), Inc=float(t[5]), eInc=float(t[6]), L36=float(t[7]), MHI=float(t[13]))
        except ValueError: continue
    return T

class Sys:
    """One system: rows (centre values), a draw function returning (n, nrows) arrays gb, gg, gobs, r, and E draws."""
    def __init__(s, line, name, sub, rows, draw, lE, tags):
        s.line, s.name, s.sub, s.rows, s.draw, s.lE, s.tags = line, name, sub, rows, draw, lE, tags; s.sid = sysid(name)

def systems(foot, ups="U50", amult=1.0):
    """Every system with its MC. amult multiplies every ASSUMED sd (ASSUMED x 2 run)."""
    Yd0, Yb0 = R.UPS[ups]; out = []; T = mrt(); KMS2 = 1e6
    gal = {g["name"]: g for g in R.SP.load_gal()}
    for i, n in enumerate(sorted(gal)):
        g = gal[n]
        if g["Q"] >= 3 or g["Inc"] < 30: continue
        rk, v, e, vg, vd, vb = (np.asarray(g[k], float) for k in ("Rk", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"))
        m = np.abs(vg) * vg + Yd0 * np.abs(vd) * vd + Yb0 * np.abs(vb) * vb; ok = (rk > 0) & (v > 0) & (m > 0)
        if not ok.any(): continue
        rk, v, e, vg, vd, vb, m = rk[ok], v[ok], e[ok], vg[ok], vd[ok], vb[ok], m[ok]; r0 = rk * 1e3 * PC; t = T[n]
        def dr(rng, N, rk=rk, v=v, e=e, vg=vg, vd=vd, vb=vb, r0=r0, t=t):
            D = np.maximum(t["D"] + t["eD"] * rng.standard_normal((N, 1)), 0.1 * t["D"])
            inc = np.clip(t["Inc"] + t["eInc"] * rng.standard_normal((N, 1)), 1.0, 179.0)
            Yd = Yd0 * 10 ** (0.10 * amult * rng.standard_normal((N, 1))); Yb = Yd * (Yb0 / Yd0); gf = 1 + 0.10 * amult * rng.standard_normal((N, 1))
            V = v + e * rng.standard_normal((N, len(v)))
            gg = gf * np.abs(vg) * vg * KMS2 / r0; gb = gg + (Yd * np.abs(vd) * vd + Yb * np.abs(vb) * vb) * KMS2 / r0
            gobs = V * V * KMS2 / r0 * (t["D"] / D) * (math.sin(math.radians(t["Inc"])) ** 2 / np.sin(np.radians(inc)) ** 2)
            return gb, gg, gobs, r0 * D / t["D"]
        lE = (BASIN_SP[n] if n in BASIN_SP else (np.nan if n in NODIST else lgM200(math.log10((0.5 * t["L36"] + 1.33 * t["MHI"]) * 1e9))))
        out.append(Sys("S", n, "odd" if i % 2 == 1 else "even", dict(r=r0, gobs=v * v * KMS2 / r0, gg=np.abs(vg) * vg * KMS2 / r0,
                       gb=m * KMS2 / r0), dr, lE, "D, Inc, eV MEASURED; Upsilon 0.10 dex, gas 10 % ASSUMED"))
    # LITTLE THINGS (RS1's rows)
    lt = [q for q in csv.DictReader(open(os.path.join(INP, "little_things", "oh2015_table2.csv"))) if all(q[k].strip() != "" for k in ("Rmax_kpc", "V_kms", "Mgas_1e7Msun", "MSED_1e7Msun"))]
    lt.sort(key=lambda q: q["name"])
    for q in lt:
        r0 = float(q["Rmax_kpc"]) * 1e3 * PC; v0 = float(q["V_kms"]) * 1e3; mg0 = float(q["Mgas_1e7Msun"]) * 1e7 * MS; ms0 = float(q["MSED_1e7Msun"]) * 1e7 * MS
        ev = float(q["eV_kms"]) * 1e3 if q["eV_kms"].strip() else None
        def dr(rng, N, r0=r0, v0=v0, mg0=mg0, ms0=ms0, ev=ev):
            d = np.maximum(1 + 0.10 * amult * rng.standard_normal((N, 1)), 0.2); sv = ev if ev is not None else 0.10 * amult * v0
            V = v0 + sv * rng.standard_normal((N, 1)); mg = mg0 * (1 + 0.10 * amult * rng.standard_normal((N, 1))); ms = ms0 * 10 ** (0.2 * amult * rng.standard_normal((N, 1)))
            r = r0 * d; return G * (mg + ms) / r0 ** 2 * np.ones_like(d), G * mg / r0 ** 2 * np.ones_like(d), V * V / r, r      # masses scale as d^2, radius as d: g_b distance-free
        sid = sysid(q["name"]); sp = [n for n in gal if sysid(n) == sid]
        if sid in LG_IDENT: lE = LG_LGM
        elif sp: n_ = sp[0]; lE = BASIN_SP.get(n_, np.nan if n_ in NODIST else lgM200(math.log10((0.5 * T[n_]["L36"] + 1.33 * T[n_]["MHI"]) * 1e9)))
        else: lE = np.nan
        line = "IC1613" if sid == sysid("IC 1613") else "LT"
        out.append(Sys(line, q["name"], "LT", dict(r=np.array([r0]), gobs=np.array([v0 * v0 / r0]), gg=np.array([G * mg0 / r0 ** 2]), gb=np.array([G * (mg0 + ms0) / r0 ** 2])),
                       dr, lE, ("eV MEASURED" if ev is not None else "eV 10 % ASSUMED") + "; D 10 %, Mgas 10 %, M_SED 0.2 dex ASSUMED"))
    # groups, one row each, with the table's errors
    names = {}
    for l in open(os.path.join(INP, "groups", "J_A_A_710_L39.tsv")):
        f = l.rstrip("\n").split("\t")
        if len(f) >= 13 and f[0].strip().isdigit() and f[1].strip() == "Galaxy group":
            names[(float(f[5]), float(f[7]), float(f[10]))] = (f[2].strip(), float(f[6]), float(f[8]))
    for (ls, lM, Re) in sorted(R.GR.load(), key=lambda t: (t[1], t[0])):
        nm, els, elM = names[(ls, lM, Re)]; r0 = 4 / 3 * Re * 1e3 * PC
        def dr(rng, N, ls=ls, lM=lM, els=els, elM=elM, r0=r0):
            s = 10 ** (ls + els * rng.standard_normal((N, 1))) * 1e3; Mb = 10 ** (lM + elM * rng.standard_normal((N, 1))) * MS
            f = np.clip(0.45 + 0.15 * amult * rng.standard_normal((N, 1)), 0, 1); gb = G * Mb / 2 / r0 ** 2
            return gb, f * gb, 3 * s * s / r0, r0 * np.ones_like(s)
        out.append(Sys("G", nm, "", dict(r=np.array([r0]), gobs=np.array([3 * (10 ** ls * 1e3) ** 2 / r0]), gg=np.array([0.45 * G * 10 ** lM * MS / 2 / r0 ** 2]),
                       gb=np.array([G * 10 ** lM * MS / 2 / r0 ** 2])), dr, lgM200(lM), "sigma, Mbar MEASURED; f 0.45 +- 0.15 ASSUMED"))
    # X-COP, RS1's interpolation, coherent error draws per cluster
    for c in R.C.xcop_load():
        p = os.path.join(INP, "xcop", c["name"], c["name"])
        with fits.open(p + "_hydro_mass.fits") as H: hr = np.array(H[1].data["RADIUS"], float); ehm = np.array(H[1].data["EM_FORW"], float)
        with fits.open(p + "_fgas_profile.fits") as H: Rg = float(H[1].header["R500"]); gr = np.array(H[1].data["RADIUS"], float) * Rg; egm = 0.5 * (np.array(H[1].data["MGAS_LO"], float) + np.array(H[1].data["MGAS_HI"], float))
        with fits.open(p + "_mstar.fits") as H: sr = np.array(H[2].data["RADIUS"], float); esm = 0.5 * (np.array(H[2].data["MSTAR_HI"], float) - np.array(H[2].data["MSTAR_LO"], float))
        rr = []
        for x in R.C.XS:
            t = (x, R.C.li(c["hr"], c["hm"], x * c["R500"]), R.C.li(c["gr"], c["gm"], x * c["R500"]), R.C.li(c["sr"], c["sm"], x * c["R500"]))
            if all(map(np.isfinite, t)):
                rt = x * c["R500"]; fh = R.C.li(hr, ehm, rt) / t[1]; fg = R.C.li(gr, egm, rt) / t[2]; fs = R.C.li(sr, esm, rt) / t[3]
                rr.append(t + (fh, fg, fs))
        A = np.array(rr); r0 = A[:, 0] * c["R500"] * 1e3 * PC
        Mg5 = R.C.li(c["gr"], c["gm"], c["R500"]); Ms5 = R.C.li(c["sr"], c["sm"], c["R500"])
        Mbt = (Mg5 if np.isfinite(Mg5) else A[-1, 2]) + (Ms5 if np.isfinite(Ms5) else A[-1, 3])
        def dr(rng, N, A=A, r0=r0):
            nh, ng, ns = (rng.standard_normal((N, 1)) for _ in range(3))
            mh = A[:, 1] * np.maximum(1 + A[:, 4] * nh, 0.01); mg = A[:, 2] * np.maximum(1 + A[:, 5] * ng, 0.01); ms = A[:, 3] * np.maximum(1 + A[:, 6] * ns, 0.01)
            k = G * MS / r0 ** 2; return k * (mg + ms), k * mg, k * mh, r0 * np.ones_like(nh)
        k = G * MS / r0 ** 2
        out.append(Sys("X", c["name"], "", dict(r=r0, gobs=k * A[:, 1], gg=k * A[:, 2], gb=k * (A[:, 2] + A[:, 3]), x=A[:, 0], fe=A[:, 4:7]), dr, lgM200(math.log10(Mbt)),
                       "M_HSE, gas, stars MEASURED (coherent per cluster)"))
    # lensing, RS1's rows
    d = np.load(os.path.join(INP, "lensing", "lens_inventory.npz")); bins = np.digitize(d["logM"], [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
    for b in range(4):
        a = np.loadtxt(os.path.join(INP, "lensing", f"Fig-3_Lensing-rotation-curves_Massbin-{b + 1}.txt"), comments="#"); s = bins == b
        Ms_ = float(np.average(10 ** d["logM"][s], weights=d["WLENS"][s])) * MS
        rows = [(rm * 1e6 * PC, e / k, er / k) for rm, e, er, k in zip(a[:, 0], a[:, 1], a[:, 3], a[:, 4]) if rm <= 0.3 and e / k > 0]
        A = np.array(rows); r0 = A[:, 0]
        def dr(rng, N, A=A, r0=r0, Ms_=Ms_):
            ms = Ms_ * 10 ** (0.15 * amult * rng.standard_normal((N, 1))); f = np.clip(0.2 + 0.1 * amult * rng.standard_normal((N, 1)), 0.0, 0.9); mg = ms * f / (1 - f)
            ds = A[:, 1] + A[:, 2] * rng.standard_normal((N, len(A))); return G * (mg + ms) / r0 ** 2, G * mg / r0 ** 2, 4 * G * ds * MS / PC ** 2, r0 * np.ones_like(ms)
        Mg_ = Ms_ * 0.25
        out.append(Sys("L", f"bin{b + 1}", "", dict(r=r0, gobs=4 * G * A[:, 1] * MS / PC ** 2, gg=G * Mg_ / r0 ** 2, gb=G * (Mg_ + Ms_) / r0 ** 2), dr,
                       lgM200(math.log10((Ms_ + Mg_) / MS)), "Delta Sigma MEASURED; M* 0.15 dex, gas share 0.2 +- 0.1 ASSUMED; PROVISIONAL"))
    # dwarfs, this footing's table
    for cl in R.DW.CLASSES:
        for q in sorted([q for q in R.DW.load(foot) if q["cls"] == cl], key=lambda q: q["name"]):
            def dr(rng, N, q=q):
                rf = np.maximum(1 + 0.10 * amult * rng.standard_normal((N, 1)), 0.2); mf = 10 ** (0.10 * amult * rng.standard_normal((N, 1)))
                gobs = q["gobs"] * 10 ** (q["s"] * rng.standard_normal((N, 1))) / rf; gb = q["gN"] * mf / rf ** 2
                return gb, 0 * gb, gobs, q["r12"] * rf
            sid = sysid(q["name"]); line = "IC1613" if sid == sysid("IC 1613") else ("Dw-UFD" if cl == "MW ultra-faint" else "Dw")
            if q["host"] in ("MW", "M31"): lE = LG_LGM
            else:
                Rk = FIELD_R.get(q["name"]); lE = LG_LGM if (Rk is not None and Rk < R0D) else lgM200(math.log10(mb_of_mstar(10 ** q["lgMs"])))
            out.append(Sys(line, q["name"], cl, dict(r=np.array([q["r12"]]), gobs=np.array([q["gobs"]]), gg=np.array([0.0]), gb=np.array([q["gN"]])), dr, lE,
                           "log g_obs sdMC MEASURED; M* 0.10 dex, r_1/2 10 % ASSUMED"))
    for s_ in out: s_.amult = amult
    return out

def law(g, a): return 0.5 * g + np.sqrt(0.25 * g * g + a * g)

def centre_check(S, foot, ups="U50"):
    """Centre values against RS1's table, matched by class and radius: max relative deviation in g_obs and g_b per class."""
    T = R.table(foot, ups); mine = {}
    for s in S:
        c = "LT" if s.sub == "LT" else ("Dw" if s.line in ("Dw", "Dw-UFD", "IC1613") else s.line)
        for k in range(len(s.rows["r"])): mine.setdefault(c, []).append((s.rows["r"][k], s.rows["gobs"][k], s.rows["gb"][k]))
    mine = {c: np.array(v) for c, v in mine.items()}; dev = {}
    for q in T:
        c = {"G3": "G", "G6": "G"}.get(q["c"], q["c"]); M = mine[c]; j = np.abs(M[:, 0] / q["r"] - 1) < 1e-9
        d = np.min(np.maximum(np.abs(M[j, 1] / q["gobs"] - 1), np.abs(M[j, 2] / q["gb"] - 1))) if j.any() else np.inf
        dev[c] = max(dev.get(c, 0.0), float(d))
    return dev, {c: len(v) for c, v in mine.items()}, len(T)

def mc(S, foot, seed=SEED, nmc=NMC):
    """Per row: mean (6,) and covariance (6,6) of (log y, log ell, f, s, log B, E); leaves at a0 canonical, B at the footing's a0."""
    rng = np.random.default_rng(seed); a0 = A0[foot]; MU, COV, META = [], [], []; dropped = []
    for si, s in enumerate(S):
        gb, gg, gobs, r = s.draw(rng, nmc); nr = gb.shape[1]
        gb = np.broadcast_to(gb, (nmc, nr)); gg = np.broadcast_to(gg, (nmc, nr)); gobs = np.broadcast_to(gobs, (nmc, nr)); r = np.broadcast_to(r, (nmc, nr))
        sl = np.array([slope_1d(gb[k], r[k]) for k in range(nmc)])
        E = s.lE + E_SD * s.amult * rng.standard_normal((nmc, 1)) * np.ones((1, nr))
        valid = (gb > 0) & (gobs > 0)
        with np.errstate(all="ignore"):
            ly = np.log10(np.where(gb > 0, gb, 1) / A0C); lell = np.log10(r * A0C / CL ** 2); f = np.clip(np.maximum(gg, 0) / np.where(gb > 0, gb, 1), 0, 1)
            lB = np.log10(np.where(valid, gobs, 1) / law(np.where(gb > 0, gb, 1), a0))
        for k in range(nr):
            v = valid[:, k]
            if v.mean() < 0.9: dropped.append((s.line, s.name, k)); continue
            Z = np.column_stack([ly[v, k], lell[v, k], f[v, k], sl[v, k], lB[v, k], E[v, k]])
            MU.append(Z.mean(0)); COV.append(np.cov(Z.T)); META.append((si, k))
    return np.array(MU), np.array(COV), META, dropped
