#!/usr/bin/env python3
"""NH2 (criteria 7d6ec1b5e7): NGC 1052's measured mass against the host mass form B needs for tides on DF2 / DF4.

    OMP_NUM_THREADS=1 python3 -I nh2.py            -> nh2.out / nh2.json
    OMP_NUM_THREADS=1 python3 -I nh2.py --mutate   -> nh2_MUTATE.out / nh2_MUTATE.json

TEST lane: adopts nothing, relabels nothing (RB2's labels stand), registers nothing.  kappa = 1/2 FITTED; not theory
closed.  Cold dark energy is a gravitating field component, never a particle.  Footings never pooled.
Data are read from their paths as untrusted text and parsed by this script; nothing in them is executed.
RB2's DF2/DF4 machinery (gl, gNp, solve_rJ, rJ_iso, gB, df_geom, df_E and the need bisection) is COPIED verbatim from
closure_2026_11_09/RB2_form_b_hosted_rows/rb2.py (commit 814021b340 / origin e62ab03ebb), with DFG made distance-dependent.
"""
import os, sys, json, math, re, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
GC_TEX = os.path.join(os.path.dirname(REPO), "_external_data", "forbes2019_ngc1052_gcs_2026_11_10", "src", "N1052.tex")
KT3 = os.path.join(REPO, "campaign_fresh_gravity", "CFG393_group_catalogue_rar", "data", "kt2017_table3.tsv")
KT2 = os.path.join(REPO, "campaign_fresh_gravity", "CFG393_group_catalogue_rar", "data", "kt2017_table2.tsv")
MUT = "--mutate" in sys.argv
TAG = "nh2_MUTATE" if MUT else "nh2"
T0 = time.time(); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
CHK = {}
def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); P(f"{name} {'PASS' if ok else 'FAIL'}  {msg}")

G, MSUN, KPC = 6.67430e-11, 1.989e30, 3.0856775814913673e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
DISTS = (13.5, 19.4, 20.0)
NGC1052 = (40.2700, -8.2558)
VSYS = 1510.0
Q2 = 0.02275                       # one-sided 2 sigma
NBOOT = 4000
SEED = 20261110

# =============================================================================== RB2 copy (verbatim; DFG made per-distance)
G_U, MSUN_U, KPC_U = 6.674e-11, 1.989e30, 3.0857e19
R12 = 4.0 / 3.0
def gl(gN):
    """isolated law, a0 units: g = nu(gN) gN with nu(y) = 1/2 + sqrt(1/4 + 1/y)."""
    gN = np.asarray(gN, float); return 0.5 * gN + np.sqrt(0.25 * gN * gN + gN)
def gNp(r, y):
    return y * r / (1.0 + r * r) ** 1.5
def solve_rJ(hfun, K, lo=-12.0, hi=12.0, it=90):
    """largest r with hfun(r) = K for a decreasing hfun (vectorised bisection in log10 r); K <= 0 -> inf."""
    K = np.asarray(K, float); lo = np.full(K.shape, lo); hi = np.full(K.shape, hi)
    for _ in range(it):
        mid = 0.5 * (lo + hi); above = hfun(10 ** mid) > K
        lo = np.where(above, mid, lo); hi = np.where(above, hi, mid)
    return np.where(K > 0, 10 ** (0.5 * (lo + hi)), np.inf)
def rJ_iso(y, K):
    y = np.asarray(y, float); K = np.broadcast_to(np.asarray(K, float), y.shape)
    return solve_rJ(lambda r: gl(gNp(r, y)) / r, K)
def gB(r, y, rJ):
    y = np.asarray(y, float); rJ = np.broadcast_to(np.asarray(rJ, float), y.shape)
    gi = gl(gNp(r, y))
    fin = np.isfinite(rJ); rJs = np.where(fin, rJ, 1.0)
    gt = gNp(r, y) + (gl(gNp(rJs, y)) - gNp(rJs, y)) * rJs ** 2 / r ** 2
    return np.where(fin & (rJs < r), gt, gi)
DFG20 = {"DF2": dict(Ms=2.0e8, Re=2.0, D=20.0, obs=(8.5, 2.3, 3.1), pos=(40.4451, -8.4028)),
         "DF4": dict(Ms=1.5e8, Re=1.6, D=20.0, obs=(6.3, 2.5, 1.6), pos=(39.8128, -8.1160))}
HOSTS = {"NGC1052": (40.2700, -8.2558), "NGC1035": (39.8713, -8.1328)}
MH_1052 = 1e11
DFG = dict(DFG20)
def set_distance(D):
    """NH2 addition: the dwarfs at distance D (Ms ~ D^2 from luminosity, R_e ~ D, sigma_obs fixed)."""
    global DFG
    DFG = {k: dict(v, Ms=v["Ms"] * (D / 20.0) ** 2, Re=v["Re"] * D / 20.0, D=D) for k, v in DFG20.items()}
def df_geom(nm):
    gg_ = DFG[nm]; p, q = gg_["pos"], HOSTS["NGC1052"]
    ra1, d1, ra2, d2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    cc = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)
    return gg_["D"] * 1000 * math.acos(min(1.0, cc)) * KPC_U       # projected distance to NGC 1052 (m)
def df_E(nm, a0, mode, Mh_fac=1.0):
    gg_ = DFG[nm]
    r12 = R12 * gg_["Re"] * KPC_U; aP = r12 / 1.30477; rev = 1.30477
    yv = G_U * gg_["Ms"] * MSUN_U / (aP ** 2 * a0)
    rJ = np.inf
    if mode == "N":
        g = float(gNp(rev, yv))
    else:
        if mode == "B":
            d = df_geom(nm); gh = float(gl(G_U * MH_1052 * Mh_fac * MSUN_U / d ** 2 / a0))   # host law field, a0 units
            K = 3.0 * gh / d * aP
            rJ = float(rJ_iso(np.array([yv]), np.array([K]))[0])
        g = float(gB(rev, np.array([yv]), rJ)[0])
    sp = math.sqrt(r12 * g * a0 / 3) / 1e3
    so, up, lo = gg_["obs"]; e = lo if so > sp else up
    return 2 * math.log(so / sp), 2 * e / so, sp, rJ / rev
def df_need(nm, a0):
    """RB2's need block, verbatim logic: host mass (k = 3, projected distance) for E_B + 2 e = 0."""
    Eiso, eiso, spi, _ = df_E(nm, a0, "iso"); EB, eB, spB, rjr = df_E(nm, a0, "B"); EN, eN, spN, _ = df_E(nm, a0, "N")
    low = Eiso + 2 * eiso < 0
    reach = ("TIDES CAN REACH" if EB + 2 * eB >= 0 else "TIDES CANNOT REACH") if low else None
    need = None
    if low and reach == "TIDES CANNOT REACH":
        if EN + 2 * eN < 0:
            need = "none"
        else:
            lo_, hi_ = 0.0, 8.0
            for _ in range(80):
                mid = 0.5 * (lo_ + hi_); Em, em, _, _ = df_E(nm, a0, "B", 10 ** mid)
                if Em + 2 * em >= 0: hi_ = mid
                else: lo_ = mid
            d = df_geom(nm); fac = 10 ** hi_
            Em8, em8, _, _ = df_E(nm, a0, "B", fac)
            if Em8 + 2 * em8 < 0: fac = float("nan")
            Mneed = d ** 2 * float(gl(G_U * MH_1052 * fac * MSUN_U / d ** 2 / a0)) * a0 / G_U / MSUN_U
            Mhave = d ** 2 * float(gl(G_U * MH_1052 * MSUN_U / d ** 2 / a0)) * a0 / G_U / MSUN_U
            need = dict(baryon_factor=fac, M_host_lt_d_needed=Mneed, M_host_lt_d_B=Mhave, ratio=Mneed / Mhave)
    return dict(E_iso_dex=Eiso / math.log(10), E_B_dex=EB / math.log(10), LOW=bool(low), reach=reach, need=need,
                d_proj_kpc=df_geom(nm) / KPC_U, rJ_over_r12=rjr)

# =============================================================================== form B's own NGC 1052
def M_B(r_kpc, a0, Mb=MH_1052):
    r = r_kpc * KPC; gN = G * Mb * MSUN / r ** 2
    M = r ** 2 * a0 * float(gl(gN / a0)) / G / MSUN
    return min(M, 60.5 * Mb), M >= 60.5 * Mb
def cap_radius(a0, Mb=MH_1052):
    lo, hi = 1.0, 1e5
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        r = mid * KPC; M = r ** 2 * a0 * float(gl(G * Mb * MSUN / r ** 2 / a0)) / G / MSUN
        lo, hi = (mid, hi) if M < 60.5 * Mb else (lo, mid)
    return math.sqrt(lo * hi)

# =============================================================================== data
def sep_rad(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(math.radians, (ra1, de1, ra2, de2))
    c = math.sin(de1) * math.sin(de2) + math.cos(de1) * math.cos(de2) * math.cos(ra1 - ra2)
    return math.acos(max(-1.0, min(1.0, c)))
def load_gcs():
    rows = []; pat = re.compile(r"NGC1052\$\\_\$GC(\d+)\s*&\s*([-\d.]+)\s*&\s*([-\d.]+)\s*&\s*(\d+)\s*&\s*(\d+)")
    for line in open(GC_TEX, encoding="utf-8", errors="replace"):
        m = pat.search(line)
        if m:
            rows.append(dict(id=int(m.group(1)), ra=float(m.group(2)), de=float(m.group(3)), v=float(m.group(4)),
                             ev=float(m.group(5))))
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate GC ids"
    for r in rows:
        r["theta"] = sep_rad(r["ra"], r["de"], *NGC1052)
    return rows
def load_kt(group=9843):
    mem = []
    for line in open(KT3, encoding="utf-8", errors="replace"):
        if line.startswith("#") or not line.strip(): continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 18: continue
        try:
            pg1 = int(f[17])
        except ValueError:
            continue
        if pg1 != group: continue
        mem.append(dict(pgc=int(f[1]), name=f[2].strip(), ra=float(f[3]), de=float(f[4]), hrv=float(f[13]),
                        logK=float(f[12]) if f[12].strip() else None))
    grp = None
    for line in open(KT2, encoding="utf-8", errors="replace"):
        if line.startswith("#") or not line.strip(): continue
        f = line.rstrip("\n").split("\t")
        if len(f) > 21 and f[1].strip() == str(group):
            grp = dict(N=int(f[3]), D=float(f[13]), sigmaV=float(f[16]), Rg=float(f[18]), logMK=float(f[19]), logMd=float(f[20]))
    return mem, grp

# =============================================================================== estimators
from math import gamma as Gam
def C_watkins(al, ga, be):
    I = math.sqrt(math.pi) * Gam(al / 2 + 1) / (4 * Gam(al / 2 + 2.5)) * (al + 3 - be * (al + 2))
    return (al + ga - 2 * be) / I
def tme(R_kpc, dv, al, ga, be, rout_kpc):
    """Watkins+10 projected TME, Msun.  R in kpc, dv in km/s."""
    R = np.asarray(R_kpc) * KPC; v = np.asarray(dv) * 1e3
    return C_watkins(al, ga, be) / G * np.mean(v ** 2 * R ** al, axis=-1) * (rout_kpc * KPC) ** (1 - al) / MSUN
CORN1 = [(a, g, b) for a in (0.0, 0.22, 0.55) for g in (2.5, 2.9, 3.5) for b in (-0.5, 0.0, 0.5)]
def tme_boot(R, dv, rout, rng):
    n = len(R); idx = rng.integers(0, n, size=(NBOOT, n)); R = np.asarray(R); dv = np.asarray(dv)
    out = {}
    for (a, g, b) in CORN1:
        cen = float(tme(R, dv, a, g, b, rout)); bs = tme(R[idx], dv[idx], a, g, b, rout)
        out[(a, g, b)] = dict(M=cen, lo=float(np.quantile(bs, Q2)), hi=float(np.quantile(bs, 1 - Q2)),
                              sd=float(np.std(bs)))
    return out
def pair_inv(xy):
    s = 0.0; n = len(xy)
    for i in range(n):
        for j in range(i + 1, n):
            s += 1.0 / math.hypot(xy[i][0] - xy[j][0], xy[i][1] - xy[j][1])
    return s
def tangent_xy(ra, de, ra0, de0, D):
    """projected position (kpc) of (ra, de) about (ra0, de0) at distance D Mpc (gnomonic, small angles)."""
    ra, de, ra0, de0 = map(math.radians, (ra, de, ra0, de0))
    c = math.sin(de0) * math.sin(de) + math.cos(de0) * math.cos(de) * math.cos(ra - ra0)
    x = math.cos(de) * math.sin(ra - ra0) / c; y = (math.cos(de0) * math.sin(de) - math.sin(de0) * math.cos(de) * math.cos(ra - ra0)) / c
    return x * D * 1000, y * D * 1000
def group_masses(xy, v):
    """KT virial form, PME iso and radial (HTB85, centre = centroid, mean velocity).  xy kpc, v km/s.  Msun."""
    xy = np.asarray(xy, float); v = np.asarray(v, float); N = len(v)
    sig2 = np.var(v, ddof=1) * 1e6
    Rg = N * N / pair_inv(xy) * KPC
    Mvir = 2.5 * math.pi / (2 * G) * sig2 * Rg / MSUN
    c = xy.mean(axis=0); R = np.hypot(*(xy - c).T) * KPC; dv = (v - v.mean()) * 1e3
    S = np.sum(dv ** 2 * R)
    Mpi = 32 / math.pi / (G * (N - 1.5)) * S / MSUN; Mpr = 64 / math.pi / (G * (N - 1.5)) * S / MSUN
    return dict(vir=Mvir, pme_iso=Mpi, pme_rad=Mpr, sigma=math.sqrt(sig2) / 1e3, Rg_kpc=Rg / KPC)

# =============================================================================== C2 Monte Carlo
def los_depth_sampler(R, ga, rmax, rng, n):
    """draw |z| (same units as R) along a line of sight at projected R, density ~ (R^2+z^2)^(-ga/2), r <= rmax."""
    zmax = math.sqrt(rmax ** 2 - R ** 2) if math.isfinite(rmax) else 1e4 * R
    if zmax <= 0: return np.zeros(n)
    zg = np.concatenate([[0.0], np.geomspace(1e-4 * R, zmax, 4000)])
    f = (R * R + zg * zg) ** (-ga / 2)
    cdf = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(zg))]); cdf /= cdf[-1]
    return np.interp(rng.random(n), cdf, zg)
def c2_sim_T(Rs, M, ga, be, rmax, rng, n):
    """T = sum v_los^2 R (km/s^2 kpc) under a point mass M (Msun), Jeans with constant beta, truncated at rmax."""
    T = np.zeros(n)
    for R in Rs:
        z = los_depth_sampler(R, ga, rmax, rng, n); r = np.sqrt(R * R + z * z)
        k = ga + 1 - 2 * be
        s2r = G * M * MSUN / (k * r * KPC) / 1e6
        if math.isfinite(rmax): s2r = s2r * (1 - (r / rmax) ** k)
        s2r = np.maximum(s2r, 0.0)
        s2 = s2r * (z / r) ** 2 + (1 - be) * s2r * (R / r) ** 2
        v = rng.standard_normal(n) * np.sqrt(s2)
        T += v * v * R
    return T
CORN2 = [(g, b, rm) for g in (2.0, 3.0, 4.0) for b in (-0.5, 0.0, 0.5, 0.9) for rm in ("1.5Rmax", "inf")]
NC2 = 20000
def c2_test(Rs, vs, M, Rmax_all, vsys_list, rng):
    if len(Rs) < 3: return dict(status="NO POWER", n=len(Rs))
    best = None; rows = []
    for (g, b, rm) in CORN2:
        rmax = 1.5 * Rmax_all if rm == "1.5Rmax" else float("inf")
        Ts = c2_sim_T(Rs, M, g, b, rmax, rng, NC2)
        for vsys in vsys_list:
            Tobs = float(np.sum((np.asarray(vs) - vsys) ** 2 * np.asarray(Rs)))
            p = float(np.mean(Ts <= Tobs)); rows.append(dict(gamma=g, beta=b, rmax=rm, vsys=vsys, p=p, Tobs=Tobs))
            if best is None or p > best["p"]: best = rows[-1]
    return dict(status="BELOW" if best["p"] < Q2 else "NOT BELOW", n=len(Rs), p_max=best["p"], lenient=best,
                p_min=min(r_["p"] for r_ in rows))

# =============================================================================== main
def main():
    rng = np.random.default_rng(SEED)
    P(f"NH2 {'MUTATE ' if MUT else ''}run  (criteria 7d6ec1b5e7; adopts nothing; kappa = 1/2 FITTED; not theory closed)")
    gcs = load_gcs(); mem, grp = load_kt()
    P(f"GC rows parsed: {len(gcs)} (ids {min(r['id'] for r in gcs)}-{max(r['id'] for r in gcs)}); KT2017 group 9843 members: {len(mem)}; "
      f"table2: {grp}")
    vgc = np.array([r["v"] for r in gcs]); thgc = np.array([r["theta"] for r in gcs])
    n1052 = [m for m in mem if m["name"].startswith("NGC1052")][0]
    others = [m for m in mem if m is not n1052]
    th_m = np.array([sep_rad(m["ra"], m["de"], *NGC1052) for m in others]); v_m = np.array([m["hrv"] for m in others])
    J = dict(gc_n=len(gcs), members=[dict(m) for m in mem], kt_group=grp)
    # ---------------------------------------------------------------- MUTATE edits of the data
    mut_note = ""
    MODE = os.environ.get("NH2_MUT", "") if MUT else ""
    if MODE == "M1":
        vgc = VSYS + 4 * (vgc - VSYS); v_m = VSYS + 4 * (v_m - VSYS); mut_note = "M1: every velocity offset x4"
    # ---------------------------------------------------------------- known answers
    if not MUT:
        R194 = thgc * 19.4e3
        mv, sd = float(vgc.mean()), float(vgc.std(ddof=1))
        rout = float(R194.max())
        M40 = float(tme(R194, vgc - VSYS, 0.22, 2.9, 0.0, rout))
        in23 = R194 <= 23.0; M23 = float(tme(R194[in23], vgc[in23] - VSYS, 0.22, 2.9, 0.0, 23.0))
        bsd = np.std([tme(R194[i], vgc[i] - VSYS, 0.22, 2.9, 0.0, rout) for i in rng.integers(0, len(vgc), (NBOOT, len(vgc)))])
        M40m = float(tme(R194, vgc - mv, 0.22, 2.9, 0.0, rout))
        check("KA1", len(gcs) >= 70 and abs(mv - 1503) <= 15 and abs(sd - 132) <= 15 and abs(rout / 40 - 1) <= 0.10
              and abs(M40 / 4.14e11 - 1) <= 0.10 and abs(M23 / 2.44e11 - 1) <= 0.15,
              f"{len(gcs)} GCs; mean {mv:.1f} km/s (1503 +- 15), sd {sd:.1f} (132 +- 15); r_out {rout:.2f} kpc (40); "
              f"TME(<r_out) {M40:.3e} (4.14e11 +- 0.71; bootstrap sd {bsd:.2e}; about the GC mean {M40m:.3e}); "
              f"TME(<23 kpc, {int(in23.sum())} GCs) {M23:.3e} (2.44e11)")
        J["KA1"] = dict(n=len(gcs), mean=mv, sd=sd, rout=rout, M40=M40, M40_sd=float(bsd), M23=M23, M40_about_mean=M40m)
        # KA2
        xy = [tangent_xy(m["ra"], m["de"], *NGC1052, grp["D"]) for m in mem]
        vv = np.array([m["hrv"] for m in mem]); gm = group_masses(xy, vv)
        Rg_kpc = gm["Rg_kpc"]; logM_form = math.log10(2.5 * math.pi / (2 * G) * (grp["sigmaV"] * 1e3) ** 2 * grp["Rg"] * 1e3 * KPC / MSUN)
        alt_Rg = dict(i_lt_j_halfN2=Rg_kpc / 2, harmonic_pairs=(len(mem) * (len(mem) - 1) / 2) / pair_inv(xy))
        check("KA2", len(mem) == 16 and abs(gm["sigma"] / 143 - 1) <= 0.05 and abs(Rg_kpc / 373 - 1) <= 0.10 and abs(logM_form - 12.844) <= 0.01,
              f"{len(mem)} members; sigma_v {gm['sigma']:.1f} km/s (143); R_g {Rg_kpc:.1f} kpc at {grp['D']} Mpc (373; other forms "
              f"{alt_Rg['i_lt_j_halfN2']:.1f}, harmonic {alt_Rg['harmonic_pairs']:.1f}); log M from KT's sigma and R_g {logM_form:.4f} (12.844); "
              f"my vir {math.log10(gm['vir']):.3f}, PME iso {math.log10(gm['pme_iso']):.3f}, rad {math.log10(gm['pme_rad']):.3f}")
        J["KA2"] = dict(gm, logM_form=logM_form, alt_Rg=alt_Rg)
        # KA3
        ref = {"canonical": (11632213297492.045, 139589586192713.66), "alt": (13466287429650.672, 161808913905117.44)}
        set_distance(20.0); dmax = 0.0
        for f in FOOTS:
            for j, nm in enumerate(("DF2", "DF4")):
                dmax = max(dmax, abs(df_need(nm, A0[f])["need"]["M_host_lt_d_needed"] / ref[f][j] - 1))
        check("KA3", dmax <= 1e-6, f"RB2's needs at D = 20 reproduced: max relative |d| {dmax:.1e}")
        # KA4 (a) mock GC systems in a logarithmic potential
        vc = 250.0; Ms_ = []
        for _ in range(200):
            ga = 2.9; u = rng.random(77); rin, rmx = 1.0, 40.0
            r = (rin ** (3 - ga) + u * (rmx ** (3 - ga) - rin ** (3 - ga))) ** (1 / (3 - ga))
            ct = rng.uniform(-1, 1, 77); R = r * np.sqrt(1 - ct ** 2)
            v = rng.standard_normal(77) * vc / math.sqrt(ga)
            ro = R.max(); Mt = (vc * 1e3) ** 2 * ro * KPC / G / MSUN
            Ms_.append(float(tme(R, v, 0.0, ga, 0.0, ro)) / Mt)
        ka4a = float(np.median(Ms_))
        # KA4 (b) C2 size and power, mocks drawn at the boundary corner (gamma 4, beta 0.9, r_max 1.5 R_max) at DF2's selection
        sel = th_m * 20e3 >= 79.3; Rs = th_m[sel] * 20e3; Rmax_all = float((th_m * 20e3).max())
        Mh = 1.0e13; rej = 0; rejL = 0; NM = 400
        global NC2
        keep = NC2; NC2 = 2000
        Tm = c2_sim_T(Rs, Mh, 4.0, 0.9, 1.5 * Rmax_all, rng, NM); TmL = c2_sim_T(Rs, Mh / 10, 4.0, 0.9, 1.5 * Rmax_all, rng, NM)
        # mock velocities: sign-random v with v^2 R contributions reproduced through T only; the test uses T alone
        sims = {}
        for (g, b, rm) in CORN2:
            rmax = 1.5 * Rmax_all if rm == "1.5Rmax" else float("inf")
            sims[(g, b, rm)] = np.sort(c2_sim_T(Rs, Mh, g, b, rmax, rng, NC2))
        for k in range(NM):
            pm = max(np.searchsorted(s, Tm[k], side="right") / NC2 for s in sims.values())
            pmL = max(np.searchsorted(s, TmL[k], side="right") / NC2 for s in sims.values())
            rej += pm < Q2; rejL += pmL < Q2
        NC2 = keep
        size, power = rej / NM, rejL / NM
        # KA4 (c) mock groups: singular isothermal sphere, tracers follow mass, 16 members, r in [20, 500] kpc
        rat = {"vir": [], "pme_iso": [], "pme_rad": []}
        for _ in range(200):
            r = rng.uniform(20, 500, 16); ct = rng.uniform(-1, 1, 16); ph = rng.uniform(0, 2 * math.pi, 16)
            st = np.sqrt(1 - ct ** 2); xy_ = np.c_[r * st * np.cos(ph), r * st * np.sin(ph)]
            v = rng.standard_normal(16) * vc / math.sqrt(2)
            Mt = (vc * 1e3) ** 2 * 500 * KPC / G / MSUN
            gmm = group_masses(xy_, v)
            for k in rat: rat[k].append(gmm[k] / Mt)
        ka4c = {k: float(np.median(v)) for k, v in rat.items()}
        # A1 (post hoc, named in RESULT.md): the same mock with Jeans velocities of the TRUNCATED tracer set,
        # sigma^2 = (v_c^2 / 2)(1 - (r / r_max)^2), so the frozen mock's velocities match its own boundary
        ratA = {"vir": [], "pme_iso": [], "pme_rad": []}
        for _ in range(200):
            r = rng.uniform(20, 500, 16); ct = rng.uniform(-1, 1, 16); ph = rng.uniform(0, 2 * math.pi, 16)
            st = np.sqrt(1 - ct ** 2); xy_ = np.c_[r * st * np.cos(ph), r * st * np.sin(ph)]
            v = rng.standard_normal(16) * vc / math.sqrt(2) * np.sqrt(1 - (r / 500) ** 2)
            Mt = (vc * 1e3) ** 2 * 500 * KPC / G / MSUN
            gmm = group_masses(xy_, v)
            for k in ratA: ratA[k].append(gmm[k] / Mt)
        ka4cA = {k: float(np.median(v)) for k, v in ratA.items()}
        P(f"A1 (post hoc) KA4c with a self-consistent truncated mock: medians vir {ka4cA['vir']:.3f}, PME iso {ka4cA['pme_iso']:.3f}, "
          f"PME rad {ka4cA['pme_rad']:.3f} (each > 1 makes C3 a looser ceiling, never a tighter one)")
        P(f"A1 (post hoc) KA2 with Tully's pi/2 projected-to-3D factor: R_g {Rg_kpc * math.pi / 2:.1f} kpc at {grp['D']} Mpc (373)")
        J["A1"] = dict(ka4c_truncated=ka4cA, Rg_pi_over_2_kpc=Rg_kpc * math.pi / 2)
        check("KA4", abs(ka4a - 1) <= 0.10 and 0.005 <= size <= 0.06 and power >= 0.5 and all(abs(x - 1) <= 0.25 for x in ka4c.values()),
              f"(a) mock GC TME median M/M_true {ka4a:.3f}; (b) C2 size {size:.4f} (0.005-0.06), power vs a 10x lighter host {power:.3f} (>= 0.5); "
              f"(c) mock group medians vir {ka4c['vir']:.3f}, PME iso {ka4c['pme_iso']:.3f}, PME rad {ka4c['pme_rad']:.3f} (within 25 %)")
        J["KA4"] = dict(tme_median=ka4a, c2_size=size, c2_power=power, group=ka4c)
        # KA5 density theorem
        rr = np.geomspace(1, 1000, 400); ok = True
        profs = {"isothermal": rr, "NFW": np.log(1 + rr / 20) - (rr / 20) / (1 + rr / 20), "Hernquist": rr ** 2 / (rr + 10) ** 2}
        a0c = A0["canonical"]
        profs["law"] = np.array([(x * KPC) ** 2 * a0c * float(gl(G * 1e11 * MSUN / (x * KPC) ** 2 / a0c)) for x in rr])
        for nm, Mp in profs.items():
            mb = Mp / rr ** 3; ok &= bool(np.all(np.diff(mb) <= 1e-12 * mb[:-1]))
        check("KA5", ok, "mean enclosed density non-increasing for isothermal, NFW, Hernquist and the law around 1e11 Msun")
    elif MODE == "M3":
        # planted heavy host: point mass 3 x DF4's canonical need; GC and member velocities redrawn (isotropic, gamma 2.9)
        Mpl = 3 * 139589586192713.66
        def redraw(theta, D=20.0, ga=2.9):
            out = []
            for th in theta:
                R = th * D * 1e3; z = los_depth_sampler(R, ga, float("inf"), rng, 1)[0]; r = math.hypot(R, z)
                s2 = G * Mpl * MSUN / ((ga + 1) * r * KPC) / 1e6
                out.append(VSYS + rng.standard_normal() * math.sqrt(s2))
            return np.array(out)
        vgc = redraw(thgc); v_m = redraw(th_m); mut_note = f"M3: velocities redrawn from a point-mass host of {Mpl:.3e} Msun"
    if mut_note: P(mut_note)
    # ---------------------------------------------------------------- grading
    vsys_list = (VSYS, n1052["hrv"])
    G_ = {}
    for D in DISTS:
        set_distance(D)
        Rgc = thgc * D * 1e3; rout = float(Rgc.max())
        tb = tme_boot(Rgc, vgc - VSYS, rout, rng)
        c1hi = max(x["hi"] for x in tb.values()); floor = min(x["lo"] for x in tb.values())
        cen = tb[(0.22, 2.9, 0.0)]
        # C3 whole group (all 16 members, NGC 1052 included)
        xy = [tangent_xy(m["ra"], m["de"], *NGC1052, D) for m in mem]
        vv = np.array([m["hrv"] for m in mem])
        if MODE in ("M1", "M3"):
            vv = np.array(list(v_m[:]) + [VSYS])   # others then NGC 1052 at v_sys
            xy = [tangent_xy(m["ra"], m["de"], *NGC1052, D) for m in others] + [(0.0, 0.0)]
        gm = group_masses(xy, vv); idx = rng.integers(0, len(vv), (NBOOT, len(vv)))
        bs = {k: [] for k in ("vir", "pme_iso", "pme_rad")}
        xya = np.asarray(xy)
        for row in idx:
            if len(set(row.tolist())) < 3: continue
            # duplicate members give zero separations; drop duplicates within a resample for the pair sum
            u = np.unique(row); g_ = group_masses(xya[u], vv[u]) if len(u) >= 3 else None
            # weight by multiplicity through the velocity variance and PME sums
            sig2 = np.var(vv[row], ddof=1) * 1e6
            Rg = len(u) ** 2 / pair_inv(xya[u]) * KPC
            bs["vir"].append(2.5 * math.pi / (2 * G) * sig2 * Rg / MSUN)
            c = xya[row].mean(axis=0); R = np.hypot(*(xya[row] - c).T) * KPC; dv = (vv[row] - vv[row].mean()) * 1e3
            S = np.sum(dv ** 2 * R); N = len(row)
            bs["pme_iso"].append(32 / math.pi / (G * (N - 1.5)) * S / MSUN); bs["pme_rad"].append(64 / math.pi / (G * (N - 1.5)) * S / MSUN)
        c3 = {k: dict(M=gm[k], hi=float(np.quantile(bs[k], 1 - Q2)), lo=float(np.quantile(bs[k], Q2))) for k in bs}
        c3hi = max(x["hi"] for x in c3.values())
        G_[D] = dict(rout=rout, c1_hi_at_rout=c1hi, floor_at_rout=floor, tme_central=cen, tme_corners={str(k): v for k, v in tb.items()},
                     c3=c3, c3_hi=c3hi, group_sigma=gm["sigma"], group_Rg_kpc=gm["Rg_kpc"], cells={})
        P(f"\nD = {D} Mpc: GC r_out {rout:.2f} kpc; TME(<r_out) central (0.22, 2.9, 0) {cen['M']:.3e} [{cen['lo']:.3e}, {cen['hi']:.3e}]; "
          f"corners span lo {floor:.3e} .. hi {c1hi:.3e}")
        P(f"  C3 group: sigma {gm['sigma']:.1f} km/s, R_g {gm['Rg_kpc']:.1f} kpc; vir {c3['vir']['M']:.3e} (hi {c3['vir']['hi']:.3e}), "
          f"PME iso {c3['pme_iso']['M']:.3e} (hi {c3['pme_iso']['hi']:.3e}), PME rad {c3['pme_rad']['M']:.3e} (hi {c3['pme_rad']['hi']:.3e}); ceiling {c3hi:.3e}")
        Rm_all = th_m * D * 1e3; Rmax_all = float(Rm_all.max())
        for f in FOOTS:
            a0 = A0[f]
            for nm, dfv in (("DF2", 1803.0), ("DF4", 1444.0)):
                nd = df_need(nm, a0); d = nd["d_proj_kpc"]
                MBd, capd = M_B(d, a0)
                cell = dict(d_kpc=d, need=nd, M_B=MBd, cap_binds=capd)
                if not nd["LOW"] or not isinstance(nd["need"], dict):
                    cell["label"] = "NO RESCUE NEEDED" if not nd["LOW"] else f"need {nd['need']}"
                    G_[D]["cells"][f"{f}/{nm}"] = cell; P(f"  {f} {nm}: {cell['label']}"); continue
                Mn = nd["need"]["M_host_lt_d_needed"]
                if MODE == "M2": Mn /= 100
                c1 = c1hi * (d / rout) ** 3
                sel = Rm_all >= d - 1e-9
                Rs = list(Rm_all[sel]); vs = list(v_m[sel])
                c2a = c2_test(Rs, vs, Mn, Rmax_all, vsys_list, rng)
                # C2b adds DF2 and DF4 (cited velocities) if beyond d
                Rs_b, vs_b = list(Rs), list(vs)
                if MODE != "M3":
                    for nm2, v2 in (("DF2", 1803.0), ("DF4", 1444.0)):
                        d2 = df_geom(nm2) / KPC_U
                        if d2 >= d - 1e-9: Rs_b.append(d2); vs_b.append(v2 if MODE != "M1" else VSYS + 4 * (v2 - VSYS))
                c2b = c2_test(Rs_b, vs_b, Mn, Rmax_all, vsys_list, rng)
                b1 = c1 < Mn; b2 = c2a["status"] == "BELOW" and c2b["status"] == "BELOW"; b3 = c3hi < Mn
                fl_d = floor   # M(<d) >= M(<r_out) for d >= r_out
                if fl_d >= Mn: lab = "TIDES CAN REACH"
                elif b1 and (b2 or b3): lab = "TIDES CANNOT REACH"
                else:
                    which = [k for k, b in (("C1", b1), ("C2", b2), ("C3", b3)) if b]
                    lab = "NOT DECIDED" + (f" ({' + '.join(which)} ONLY)" if which else " (no ceiling below)")
                cell.update(M_need=Mn, C1_ceiling=c1, C1_below=b1, C2a=c2a, C2b=c2b, C2_below=b2, C3_ceiling=c3hi, C3_below=b3,
                            floor=fl_d, label=lab, ratio_C1=c1 / Mn, ratio_C3=c3hi / Mn)
                G_[D]["cells"][f"{f}/{nm}"] = cell
                P(f"  {f:9s} {nm} d {d:6.1f} kpc: need {Mn:.3e} (B has {MBd:.3e}{' CAPPED' if capd else ''}); C1 {c1:.3e} ({c1 / Mn:.3f} of need) "
                  f"{'BELOW' if b1 else 'not below'}; C2a {c2a['status']} (n {c2a['n']}, p_max {c2a.get('p_max', float('nan')):.2e}), "
                  f"C2b {c2b['status']} (n {c2b['n']}, p_max {c2b.get('p_max', float('nan')):.2e}); C3 {c3hi:.3e} ({c3hi / Mn:.3f}) "
                  f"{'BELOW' if b3 else 'not below'}; floor {fl_d:.3e} -> {lab}")
    # ---------------------------------------------------------------- labels
    P("\nLABELS (per footing; distances 13.5 / 19.4 / 20.0 must agree)")
    LAB = {}
    for f in FOOTS:
        LAB[f] = {}
        for nm in ("DF2", "DF4"):
            ls = [G_[D]["cells"][f"{f}/{nm}"]["label"] for D in DISTS]
            graded = [l.split(" (")[0] for l in ls if l != "NO RESCUE NEEDED"]
            LAB[f][nm] = graded[0] if graded and len(set(graded)) == 1 else ("NOT DECIDED (DISTANCE)" if graded else "NO RESCUE NEEDED")
            P(f"  {f:9s} {nm}: {LAB[f][nm]}   cells {ls}")
        a, b = LAB[f]["DF2"], LAB[f]["DF4"]
        LAB[f]["lane"] = ("HOST CANNOT RESCUE DF2 / DF4" if a == b == "TIDES CANNOT REACH" else
                          "HOST CAN RESCUE" if a == b == "TIDES CAN REACH" else f"DF2 {a}; DF4 {b}")
        P(f"  {f:9s} LANE: {LAB[f]['lane']}")
    # ---------------------------------------------------------------- row S
    P("\nROW S (B's own host vs the GC mass at r_out; HI reported)")
    RS = {}
    for D in DISTS:
        g = G_[D]; lo_ = min(x["lo"] for x in g["tme_corners"].values()); hi_ = max(x["hi"] for x in g["tme_corners"].values())
        for f in FOOTS:
            mb, _ = M_B(g["rout"], A0[f]); mb23, _ = M_B(23.0 * D / 19.4, A0[f])
            lab = "B HOST CONSISTENT" if lo_ <= mb <= hi_ else ("B HOST TOO LIGHT" if mb < lo_ else "B HOST TOO HEAVY")
            RS[f"{D}/{f}"] = dict(M_B=mb, central=g["tme_central"]["M"], lo=lo_, hi=hi_, label=lab, M_B_23=mb23, HI_23=3.1e11 * D / 19.4)
            P(f"  D {D} {f:9s}: M_B(<{g['rout']:.1f} kpc) {mb:.3e} vs GC {g['tme_central']['M']:.3e} [{lo_:.3e}, {hi_:.3e}] -> {lab}; "
              f"HI {3.1e11 * D / 19.4:.2e} inside {23.0 * D / 19.4:.1f} kpc vs B {mb23:.2e}")
    for f in FOOTS:
        P(f"  cap radius ({f}): {cap_radius(A0[f]):.0f} kpc (B's charge 59.5 M_b used up there; the cap does not bind inside it)")
    J.update(grading={str(D): v for D, v in G_.items()}, labels=LAB, rowS=RS, checks=CHK, mutate=MODE, note=mut_note,
             runtime_s=time.time() - T0, peak_rss_gb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 3)
    P(f"\nruntime {time.time() - T0:.1f} s; peak RSS {J['peak_rss_gb']:.2f} GB")
    return J

if __name__ == "__main__":
    if MUT:
        allJ = {}; allOUT = []
        base = None
        for mode in ("M1", "M2", "M3"):
            os.environ["NH2_MUT"] = mode; OUT.clear(); CHK.clear()
            allJ[mode] = main(); allOUT += [f"==================== {mode}"] + OUT[:]
        OUT[:] = allOUT
        J = allJ
    else:
        J = main()
    def clean(o):
        if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [clean(v) for v in o]
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.bool_,)): return bool(o)
        if isinstance(o, float) and not math.isfinite(o): return str(o)
        return o
    json.dump(clean(J), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
