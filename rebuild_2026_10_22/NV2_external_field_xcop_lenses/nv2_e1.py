#!/usr/bin/env python3
"""NV2 E1: the record's Chae-2021 Sec. 3.1 external-field sum (gext_vectors_2026/src/gext_estimator.py, imported read-only for its loaders and
LF; the sum is reimplemented here so one function serves every catalogue), truncated at R_s = 30 Mpc for every system (FROZEN_CRITERIA).
Modes (outputs nv2_e1_<mode>.{json,out}):
  ka        estimator known answers (control 3): point mass, uniform field, antipodal shell, truncation edge, record reproduction on SPARC
  sparc     NV2 E1 for the 175 SPARC galaxies from 2M++ (R_s = 30 Mpc), vs the record's full-sky E1; 2M++ depth sensitivity (ks115 vs full)
  fidelity  photo-z fidelity (control 4): SPARC test points, 2M++ sources with redrawn distances, models A (KiDS) and B (2MPZ, p_spec(Ks) from the cones)
  xcop      E1 for the 12 X-COP clusters from the 2MPZ cones (+ MCXC), photo-z Monte Carlo, coverage
  lenses    Step 0 (B21 isolated-lens rebuild, known answer 259,383 +- 5 %) and lens E1 per bin (5000 lenses per bin)
Run: PYTHONHASHSEED=0 nice -n 10 python3 -I nv2_e1.py MODE. Downloaded data are read, never written. kappa = 1/2 FITTED; not theory closed."""
import csv, json, math, os, resource, subprocess, sys, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.spatial import cKDTree
from scipy.special import gammaincc, gamma as GF
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
GX = os.path.join(REPO, "gext_vectors_2026"); RAW = os.path.join(GX, "data", "raw")
sys.path.insert(0, os.path.join(GX, "src")); import gext_estimator as GE        # read-only: loaders, LF, constants
EXT = os.path.join(REPO, "_external_data"); CONES = os.path.join(EXT, "nv2_2mpz_cones_2026-11-04"); KIDS = os.path.join(EXT, "lam1_kids_bright_2026_11_03")
CACHE = os.path.join(HERE, "cache"); os.makedirs(CACHE, exist_ok=True)
G, MSUN, MPC, A0, CK = GE.G_SI, GE.MSUN_KG, GE.MPC_M, GE.A0, GE.C_KMS
RS = 30.0; EXCL = 0.010; H0 = 73.0
OUT = []; T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def fpk():
    try: return [l.split(":")[1].strip() for l in subprocess.run(["footprint", str(os.getpid())], capture_output=True, text=True).stdout.splitlines() if "phys_footprint_peak" in l][0]
    except Exception: return "?"
def tm(): return f"[{time.time() - T0:.0f}s, max RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB, phys footprint peak {fpk()}]"

# ---------------------------------------------------------------- cosmology (comoving distance, flat Om 0.3)
_zg = np.linspace(0, 1.5, 30001); _E = np.sqrt(0.3 * (1 + _zg) ** 3 + 0.7); _CH = np.concatenate([[0], np.cumsum(0.5 * (1 / _E[1:] + 1 / _E[:-1]) * np.diff(_zg))])
def DC(z, h0=H0): return np.interp(z, _zg, _CH) * CK / h0
def unit(ra, dec): return GE.radec_to_cart(ra, dec)

# ---------------------------------------------------------------- the sum (one function for every catalogue)
def field(tp, zt, spos, mno, mmax, clu=None, Rs=RS, keep=None):
    """tp: test point, comoving Mpc (3,); zt: test redshift; spos (N,3) comoving; mno/mmax: masses for noclu / maxclu (maxclu already /f, x8 applied below);
    clu: dict(pos, Mmond, R500 (proper Mpc)); keep: optional bool mask (self exclusion). Returns (|g_no|, |g_max|) in m/s^2. Separations proper = comoving/(1+zt)."""
    a = 1.0 / (1.0 + zt); gno = np.zeros(3); gmx = np.zeros(3)
    if len(spos):
        d = spos - tp; rc = np.sqrt((d * d).sum(1)); m = (rc < Rs) & (rc * a > EXCL)
        if keep is not None: m &= keep
        r = rc[m] * a * MPC; u = d[m] / rc[m, None]; w = G * MSUN / r ** 2
        gno = (u * (w * mno[m])[:, None]).sum(0); gmx = (u * (w * mmax[m])[:, None]).sum(0)
    if clu is not None and len(clu["pos"]):
        d = clu["pos"] - tp; rc = np.sqrt((d * d).sum(1)); m = (rc < Rs) & (rc * a > EXCL) & clu.get("keep", np.ones(len(rc), bool))
        rp = rc[m] * a; M = clu["Mmond"][m]; R5 = clu["R500"][m]; Me = np.where(rp < R5, M * (rp / np.maximum(R5, 1e-6)) ** 3, M)
        g = (d[m] / rc[m, None]) * (G * Me * MSUN / (rp * MPC) ** 2)[:, None]; gno = gno + g.sum(0); gmx = gmx + g.sum(0)
    return float(np.linalg.norm(gno)), float(np.linalg.norm(gmx)) * 8.0
def e1_of(gno, gmx):
    ln, lm = math.log10(max(gno, 1e-30) / A0), math.log10(max(gmx, 1e-30) / A0); return 0.5 * (ln + lm), 0.5 * abs(lm - ln), ln, lm

# ---------------------------------------------------------------- masses (record convention, Chae / Lavaux-Hudson; masses from Ks and a luminosity distance)
def ks_masses(ks, z, D):
    dm = 5 * np.log10(np.maximum(D, 1e-3) * (1 + z)) + 25.0; Mabs = ks + 2.1 * z - 0.8 * z - dm; Ms = GE.ML_KS * 10.0 ** (-0.4 * (Mabs - GE.MSUN_KS))
    return Ms + gas_of(Ms)
def gas_of(Ms):
    lgM = np.log10(np.maximum(Ms, 1.0)); fe = np.clip(0.28 * lgM - 2.12, 0.0, 1.0); Mc = 11500.0 * np.maximum(Ms, 1.0) ** 0.54 + 0.07 * Ms; Mh = 10.0 ** (1.47 * lgM - 5.414)
    return (1 - fe) * Mc + fe * Mh

# ---------------------------------------------------------------- MCXC (all rows, Chae Eqs. 3-4 via the record's loader with the 200 Mpc cut lifted)
def mcxc_all():
    s = GE.D_MAX; GE.D_MAX = 1e9
    try: c = GE.load_mcxc(os.path.join(RAW, "mcxc.tsv"))
    finally: GE.D_MAX = s
    return dict(name=c["name"], ra=c["ra"], dec=c["dec"], z=c["z"], Mmond=c["Mmond"], R500=c["R500"], pos=unit(c["ra"], c["dec"]) * DC(c["z"])[:, None])

# ---------------------------------------------------------------- SPARC test points and 2M++ (record files)
def GE_load_sparc():
    rows = []
    for ln in open(os.path.join(RAW, "sparc_table1_vizier.tsv")):
        if ln.startswith("#") or not ln.strip(): continue
        p = ln.rstrip("\n").split("\t")
        if len(p) < 9: continue
        try: D = float(p[1]); ra = float(p[7]); dec = float(p[8])
        except ValueError: continue
        rows.append(dict(name=p[0].strip(), D=D, ra=ra, dec=dec))
    return rows
REC_MODE = "ks115"   # AMENDMENT_A1: the record csv was built in mode ks115 (reproduced to 5e-6 dex), not full
def twompp(mode=REC_MODE, nv2=True):
    g = GE.load_2mpp(os.path.join(RAW, "2mpp_vizier.tsv"), catalog_mode=mode)
    # Ks again (the record loader keeps no Ks): re-read with the same cuts
    K = []; V = []
    for ln in open(os.path.join(RAW, "2mpp_vizier.tsv")):
        if ln.startswith("#") or not ln.strip(): continue
        p = ln.rstrip("\n").split("\t")
        if len(p) < 10: continue
        try: k = float(p[1]); v = float(p[2]); float(p[8]); float(p[9])
        except ValueError: continue
        K.append(k); V.append(v)
    K = np.array(K); V = np.array(V); Dr = V / H0; sel = ((K <= GE.KS_LIM) if mode == "ks115" else np.ones(len(K), bool)) & (Dr > 0) & (Dr <= GE.D_MAX); K = K[sel]
    assert len(K) == len(g["D"]) and np.allclose(V[sel] / H0, g["D"])
    z = g["z"]
    if nv2:
        D = DC(z); M = ks_masses(K, z, D); f = GE.lf_visible_fraction(D, z, g["kslim"])
    else:
        D = g["D"]; M = g["Mstar"] + g["Mgas"]; f = GE.lf_visible_fraction(g["D"], g["z"], g["kslim"])
    return dict(name=g["name"], ra=g["ra"], dec=g["dec"], z=z, D=D, Ks=K, M=M, f=f, kslim=g["kslim"], u=unit(g["ra"], g["dec"]))
def sparc_self_keep(S, ra, dec, D):
    """record self rule: exclude 2M++ sources within 0.1 deg and |dD| < max(3 Mpc, 0.2 D)."""
    tp = unit(ra, dec); ang = np.degrees(np.arccos(np.clip(S["u"] @ tp, -1, 1))); return ~((ang < 0.1) & (np.abs(S["D"] - D) < max(3.0, 0.2 * D)))

def sparc_E1(S, CL, pts, Rs=RS, Dsrc=None):
    o = {}
    pos = S["u"] * (S["D"] if Dsrc is None else Dsrc)[:, None]
    for g in pts:
        tp = unit(g["ra"], g["dec"]) * g["D"]; keep = sparc_self_keep(S, g["ra"], g["dec"], g["D"])
        o[g["name"]] = e1_of(*field(tp, 0.0, pos, S["M"], S["M"] / S["f"], CL, Rs, keep))
    return o

# ================================================================ mode ka
def mode_ka():
    R = {}
    GE._unit_test(); R["record_unit_test"] = True
    # (a) point mass
    M = 1e12; src = np.array([[0.0, 10.0, 0.0]]); tp = np.array([5.0, 0.0, 0.0]); gno, _ = field(tp, 0.0, src, np.array([M]), np.array([M]), Rs=1e9)
    ge = G * M * MSUN / (np.linalg.norm(src[0] - tp) * MPC) ** 2; R["a_point"] = dict(ratio=gno / ge, ok=abs(gno / ge - 1) < 1e-10)
    # (b) uniform field: 1e15 Msun at 1e4 Mpc, 50 test points within 10 Mpc
    rng = np.random.default_rng(1); src = np.array([[1e4, 0, 0]]); rat = []; dirs = []
    for _ in range(50):
        v = rng.normal(size=3); v *= 10 * rng.uniform() ** (1 / 3) / np.linalg.norm(v); d = src[0] - v
        gno, _ = field(v, 0.0, src, np.array([1e15]), np.array([1e15]), Rs=1e9); rat.append(gno / (G * 1e15 * MSUN / (1e4 * MPC) ** 2)); dirs.append(d / np.linalg.norm(d))
    dirs = np.array(dirs); ang = np.arccos(np.clip(dirs @ dirs[0], -1, 1)).max()
    R["b_uniform"] = dict(max_dev=float(np.max(np.abs(np.array(rat) - 1))), max_angle=float(ang), ok=bool(np.max(np.abs(np.array(rat) - 1)) < 5e-3 and ang < 0.01))
    # (c) antipodal shell
    v = rng.normal(size=(500, 3)); v /= np.linalg.norm(v, axis=1)[:, None]; tp = np.array([3.0, -2.0, 1.0]); src = np.vstack([tp + 2.0 * v, tp - 2.0 * v]); Mp = np.full(1000, 1e11)
    gno, _ = field(tp, 0.0, src, Mp, Mp, Rs=1e9); sc = G * 1e11 * MSUN / (2.0 * MPC) ** 2; R["c_shell"] = dict(rel=gno / sc, ok=gno / sc < 1e-10)
    # (d) truncation edge
    src = np.array([[RS - 1e-6, 0, 0], [RS + 1e-6, 0, 0]]); g1, _ = field(np.zeros(3), 0.0, src[:1], np.ones(1), np.ones(1)); g2, _ = field(np.zeros(3), 0.0, src[1:], np.ones(1), np.ones(1))
    R["d_truncation"] = dict(inside=g1 > 0, outside=g2 == 0, ok=bool(g1 > 0 and g2 == 0))
    # (e) record reproduction: record distances, record loaders (MCXC <= 200 Mpc), no truncation, record self rule
    S = twompp(REC_MODE, nv2=False); c = GE.load_mcxc(os.path.join(RAW, "mcxc.tsv")); CL = dict(pos=unit(c["ra"], c["dec"]) * c["D"][:, None], Mmond=c["Mmond"], R500=c["R500"])
    E = sparc_E1(S, CL, GE_load_sparc(), Rs=1e9); rec = {r["name"]: r for r in csv.DictReader(open(os.path.join(GX, "data", "gext_vectors.csv")))}
    dn = np.array([E[n][2] - float(rec[n]["log_eN_noclu"]) for n in E if n in rec]); dx = np.array([E[n][3] - float(rec[n]["log_eN_maxclu"]) for n in E if n in rec])
    R["e_record"] = dict(n=len(dn), n_record=len(rec), max_abs_noclu=float(np.max(np.abs(dn))), max_abs_maxclu=float(np.max(np.abs(dx))), ok=bool(len(dn) == 175 and np.max(np.abs(dn)) <= 2e-3 and np.max(np.abs(dx)) <= 2e-3))
    R["ok"] = bool(all(v["ok"] for k, v in R.items() if isinstance(v, dict)))
    for k, v in R.items(): P(k, json.dumps(clean(v)) if isinstance(v, dict) else v)
    P("estimator known answers:", "ALL OK" if R["ok"] else "FAILED", tm()); return R

# ================================================================ mode sparc
def mode_sparc():
    R = {}; CL = mcxc_all(); pts = GE_load_sparc(); S = twompp(REC_MODE)
    E = sparc_E1(S, CL, pts); R["E1"] = {n: dict(E1=v[0], sig=v[1], lno=v[2], lmax=v[3]) for n, v in E.items()}
    rec = {r["name"]: r for r in csv.DictReader(open(os.path.join(GX, "data", "gext_vectors.csv")))}; nm = sorted(E)
    a = np.array([E[n][0] for n in nm]); b = np.array([0.5 * (float(rec[n]["log_eN_noclu"]) + float(rec[n]["log_eN_maxclu"])) for n in nm])
    R["vs_record"] = dict(n=len(nm), spearman=float(spearmanr(a, b)[0]), median_offset=float(np.median(a - b)), p16_84=np.percentile(a - b, [16, 84]).tolist())
    S115 = twompp("full"); E115 = sparc_E1(S115, CL, pts); d = np.array([E115[n][0] - E[n][0] for n in nm])
    R["depth_full_minus_ks115"] = dict(median=float(np.median(d)), p16_84=np.percentile(d, [16, 84]).tolist(), spearman=float(spearmanr(a, [E115[n][0] for n in nm])[0]))
    R["summary"] = dict(median=float(np.median(a)), p16_84=np.percentile(a, [16, 84]).tolist(), sigma_median=float(np.median([E[n][1] for n in nm])))
    P("SPARC NV2 E1 (R_s 30 Mpc, 2M++ ks115, the record mode):", json.dumps(R["summary"])); P("vs record full-sky E1:", json.dumps(R["vs_record"])); P("depth (full - ks115):", json.dumps(R["depth_full_minus_ks115"]), tm())
    return R

# ================================================================ 2MPZ cones
def cones():
    import nv2_download as DL
    rows = {}; per = {}
    for c in DL.clusters():
        fn = os.path.join(CONES, f"twompz_cone_{c['name']}.csv"); n = 0
        for r in csv.DictReader(open(fn)):
            try: i = int(r["twomassID"]); q = (float(r["ra"]), float(r["dec"]), float(r["kCorr"]), float(r["zPhoto"]), float(r["zSpec"]))
            except (ValueError, KeyError): continue
            rows[i] = q; n += 1
        per[c["name"]] = n
    ids = np.array(sorted(rows)); A = np.array([rows[i] for i in ids])
    T = dict(id=ids, ra=A[:, 0], dec=A[:, 1], ks=A[:, 2], zp=A[:, 3], zs=A[:, 4]); T["spec"] = (T["zs"] > -1) & (T["zs"] > -0.5) & (T["zs"] < 5)
    T["okz"] = T["spec"] | ((T["zp"] > -0.5) & (T["zp"] < 5)); T["u"] = unit(T["ra"], T["dec"]); return T, per, DL.clusters()
def p_spec_table(T):
    b = np.arange(5.0, 14.5, 0.5); o = []
    for lo in b[:-1]:
        m = (T["ks"] >= lo) & (T["ks"] < lo + 0.5) & T["okz"]; o.append([float(lo), int(m.sum()), float(T["spec"][m].mean()) if m.sum() else None])
    return o

# ================================================================ mode fidelity
def mode_fidelity():
    R = {}; CL = mcxc_all(); pts = GE_load_sparc(); S = twompp(REC_MODE); E0 = sparc_E1(S, CL, pts); nm = sorted(E0); e0 = np.array([E0[n][0] for n in nm])
    T, _, _ = cones(); ps = p_spec_table(T); R["p_spec_Ks"] = ps; P("2MPZ p_spec by Ks (0.5 mag bins: lo, n, fraction with zSpec):", ps)
    def p_of(ks):
        lo = np.array([x[0] for x in ps]); fr = np.array([x[2] if x[2] is not None else 0.0 for x in ps]); i = np.clip(((ks - lo[0]) / 0.5).astype(int), 0, len(lo) - 1); return fr[i]
    models = (("A_KiDS", 0.02, lambda ks: np.zeros(len(ks))), ("B_2MPZ", 0.015, p_of))
    if "--extra" in sys.argv:   # AMENDMENT_A2, post-result, reported not gated: every source perturbed at 2MPZ's sigma_z (model B leaves 2M++'s Ks <= 11.5 sources ~99 % unperturbed)
        models = (("Bworst_2MPZ_all_perturbed", 0.015, lambda ks: np.zeros(len(ks))),)
    for model, sz, pfun in models:
        rng = np.random.default_rng(20261114); runs = []
        for k in range(50):
            pert = rng.uniform(size=len(S["D"])) >= pfun(S["Ks"]); Dn = S["D"] + np.where(pert, rng.normal(0, CK * sz / H0, len(S["D"])), 0.0); Dn = np.abs(Dn)
            Ek = sparc_E1(S, CL, pts, Dsrc=Dn); runs.append([Ek[n][0] for n in nm])
        med = np.median(np.array(runs), 0); rho = float(spearmanr(med, e0)[0]); R[model] = dict(spearman=rho, median_bias=float(np.median(med - e0)), p16_84_bias=np.percentile(med - e0, [16, 84]).tolist(), ok=bool(rho >= 0.5))
        P(f"fidelity {model} (sigma_z {sz}): Spearman {rho:.3f}, median bias {R[model]['median_bias']:+.3f} -> {'USABLE' if rho >= 0.5 else 'NOISE-DOMINATED'}", tm())
    return R

# ================================================================ mode xcop
def mode_xcop():
    R = {}; CL = mcxc_all(); T, per, CS = cones(); R["cone_rows"] = per; R["unique_rows"] = int(len(T["id"])); R["usable_z_rows"] = int(T["okz"].sum()); R["spec_rows"] = int(T["spec"].sum())
    P("2MPZ cones: rows per cone", per, "unique", len(T["id"]), "with usable z", int(T["okz"].sum()), "spec", int(T["spec"].sum()))
    tree = cKDTree(T["u"]); sel = T["okz"]; idx = np.nonzero(sel)[0]; ks = T["ks"][idx]; zp = T["zp"][idx]; zs = T["zs"][idx]; sp = T["spec"][idx]; u = T["u"][idx]
    zobs = np.where(sp, zs, zp)
    for c in CS:
        zc = c["z"]; Dc = float(DC(zc)); tpu = unit(c["ra"], c["dec"]); tp = tpu * Dc; th = math.asin(RS / Dc)
        # coverage: 2000 uniform points in the cap
        rng = np.random.default_rng(20261112); cz = rng.uniform(math.cos(th), 1.0, 2000); ph = rng.uniform(0, 2 * math.pi, 2000); sz = np.sqrt(1 - cz ** 2)
        e3 = np.array([0, 0, 1.0]) if abs(tpu[2]) < 0.9 else np.array([1.0, 0, 0]); e1 = np.cross(tpu, e3); e1 /= np.linalg.norm(e1); e2 = np.cross(tpu, e1)
        Pts = cz[:, None] * tpu + sz[:, None] * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2); dd, _ = tree.query(Pts, k=1, distance_upper_bound=2 * math.sin(math.radians(0.25)))
        cov = float(np.mean(np.isfinite(dd)))
        # self exclusion: projected < 2 R500 (proper -> comoving x (1+z)) and z-consistent; MCXC self within 0.2 deg and |dz| < 0.01
        ang = np.arccos(np.clip(u @ tpu, -1, 1)); Rproj = ang * Dc / (1 + zc); dzlim = np.where(sp, 0.01, 3 * 0.015)
        keep = ~((Rproj < 2 * c["r500_kpc"] / 1e3) & (np.abs(zobs - zc) < dzlim))
        ca = np.degrees(np.arccos(np.clip(unit(CL["ra"], CL["dec"]) @ tpu, -1, 1))); CLk = dict(CL, keep=~((ca < 0.2) & (np.abs(CL["z"] - zc) < 0.01)))
        mclu = np.nonzero(~CLk["keep"])[0]
        rng = np.random.default_rng(20261110); vals = []
        for k in range(200):
            z = np.where(sp, zs, np.abs(zp + rng.normal(0, 0.015, len(zp)))); D = DC(z); M = ks_masses(ks, z, D); f = GE.lf_visible_fraction(D, z, np.full(len(z), 13.9))
            vals.append(e1_of(*field(tp, zc, u * D[:, None], M, M / f, CLk, RS, keep)))
        V = np.array(vals); E1 = float(np.median(V[:, 0])); hb = float(np.median(V[:, 1])); hmc = 0.5 * float(np.percentile(V[:, 0], 84) - np.percentile(V[:, 0], 16)); sig = math.sqrt(hb ** 2 + hmc ** 2)
        R[c["name"]] = dict(z=zc, Dc=Dc, coverage=cov, computable=bool(cov >= 0.8), E1=E1 if cov >= 0.8 else None, E1_raw=E1, sigma=sig, h_bracket=hb, h_MC=hmc, lno_med=float(np.median(V[:, 2])), lmax_med=float(np.median(V[:, 3])),
                            excluded_members=int((~keep).sum()), mcxc_self=[str(CL["name"][i]) for i in mclu], n_sources_in_cone=int(len(idx)))
        P(f"{c['name']:8s} z {zc:.4f} coverage {cov:.3f} -> {'E1 %+.3f +- %.3f (bracket %.3f, MC %.3f)' % (E1, sig, hb, hmc) if cov >= 0.8 else 'NOT COMPUTABLE (coverage)'}; members excluded {int((~keep).sum())}, MCXC self {R[c['name']]['mcxc_self']}")
    P(tm()); return R

# ================================================================ mode lenses (Step 0 + lens E1)
def kids():
    from astropy.io import fits
    b = fits.open(os.path.join(KIDS, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data; L = fits.open(os.path.join(KIDS, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
    o = dict(id=np.array(b["ID"]), ra=np.array(b["RAJ2000"], "f8"), dec=np.array(b["DECJ2000"], "f8"), r=np.array(b["MAG_AUTO_CALIB"], "f8"), z=np.array(b["zphot_ANNz2"], "f8"), masked=np.array(b["masked"]))
    assert np.array_equal(np.array(L["ID"]), o["id"]); o["lm"] = np.array(L["MASS_BEST"], "f8") + 0.15 + 0.056; return o
def mode_lenses():
    R = {}; K = kids(); n0 = len(K["z"])
    pool = (K["masked"] == 0) & (K["r"] < 20) & np.isfinite(K["lm"]) & np.isfinite(K["z"]) & (K["z"] > 0) & (K["lm"] > 0)
    ip = np.nonzero(pool)[0]; z = K["z"][ip]; lm = K["lm"][ip]; u = unit(K["ra"][ip], K["dec"][ip]); chi70 = DC(z, 70.0)
    lens = (z > 0.1) & (z < 0.5) & (lm < 11.0); il = np.nonzero(lens)[0]
    R["catalogue_rows"] = n0; R["pool"] = int(len(ip)); R["lens_candidates"] = int(len(il)); P(f"KiDS-bright rows {n0}, pool (masked 0, r<20, finite M*) {len(ip)}, lens candidates (0.1<z<0.5, M*<1e11) {len(il)}")
    tree = cKDTree(u); iso = np.ones(len(il), bool); CH = 4000
    for i0 in range(0, len(il), CH):
        sl = il[i0:i0 + CH]; lists = tree.query_ball_point(u[sl], r=2 * np.sin(0.5 * 3.0 / chi70[sl]))
        k = np.repeat(np.arange(len(sl)), [len(x) for x in lists]); j = np.fromiter((q for x in lists for q in x), np.int64, int(sum(len(x) for x in lists))); i = sl[k]
        m = (j != i) & (lm[j] > lm[i] - 1.0); k, i, j = k[m], i[m], j[m]
        ang = np.arccos(np.clip((u[i] * u[j]).sum(1), -1, 1)); Rp = chi70[i] * ang; r3 = np.sqrt(Rp ** 2 + (chi70[i] - chi70[j]) ** 2)
        iso[i0 + np.unique(k[r3 < 3.0])] = False   # AMENDMENT_A2: the first run indexed by chunk position (bug), giving 99.5 % isolated
    bins = np.digitize(lm[il], [8.5, 10.3, 10.6, 10.8, 11.0]) - 1; nb = [int(((bins == b) & iso).sum()) for b in range(4)]
    N = int(iso.sum()); Nin = int((iso & (bins >= 0) & (bins <= 3)).sum())
    R["step0"] = dict(isolated_total=N, isolated_in_bins_8p5_11=Nin, per_bin=nb, fraction=N / len(il), target=259383, window=[246414, 272352], passed=bool(246414 <= N <= 272352))
    P(f"Step 0: isolated {N} ({100 * N / len(il):.1f} % of lens candidates); in B21 bins {Nin}; per bin {nb}; B21 259,383 +- 5 % -> {'PASSED' if R['step0']['passed'] else 'FAILED'}", tm())
    # ---- lens E1 (graded only if Step 0 passed)
    zall = z; ok = iso & (bins >= 0) & (bins <= 3); rng = np.random.default_rng(20261113)
    zb = np.arange(0.0, 1.21, 0.02); pc = [np.percentile(lm[(zall >= a) & (zall < a + 0.02)], 5) if ((zall >= a) & (zall < a + 0.02)).sum() > 20 else np.nan for a in zb[:-1]]
    pc = np.array(pc); good = np.isfinite(pc); zc_ = zb[:-1][good] + 0.01; pc = pc[good]; R["M_lim_z"] = [[float(a), float(b)] for a, b in zip(zc_, pc)]
    LMS, PH1, A1, PH2, A2 = 10.66, 3.96e-3, -0.35, 0.79e-3, -1.47
    def fvis(zz):
        x = 10 ** (np.interp(zz, zc_, pc) - LMS); num = PH1 * gammaincc(A1 + 2, x) * GF(A1 + 2) + PH2 * gammaincc(A2 + 2, x) * GF(A2 + 2); den = PH1 * GF(A1 + 2) + PH2 * GF(A2 + 2); return np.clip(num / den, 1e-3, 1.0)
    W = np.load(os.path.join(RB, "CRG1_clean_room_regrade", "inputs", "lensing", "lens_inventory.npz")); wz = np.arange(0.1, 0.5001, 0.02); wv = np.array([W["WLENS"][(W["z"] >= a) & (W["z"] < a + 0.02)].mean() for a in wz[:-1]]); wzc = wz[:-1] + 0.01
    CL = mcxc_all(); Ms = 10 ** lm; Mtot = Ms + gas_of(Ms)
    # coverage per lens (2000 points in the cap of radius asin(R_s / D_c(z_l, H0 73)); covered if a pool source within 0.06 deg)
    def coverage(i):
        Dl = float(DC(z[i])); th = math.asin(min(1.0, RS / Dl)); tpu = u[i]; g = np.random.default_rng(20261112); cz = g.uniform(math.cos(th), 1.0, 2000); ph = g.uniform(0, 2 * math.pi, 2000); sz = np.sqrt(1 - cz ** 2)
        e3 = np.array([0, 0, 1.0]) if abs(tpu[2]) < 0.9 else np.array([1.0, 0, 0]); e1 = np.cross(tpu, e3); e1 /= np.linalg.norm(e1); e2 = np.cross(tpu, e1)
        Pts = cz[:, None] * tpu + sz[:, None] * (np.cos(ph)[:, None] * e1 + np.sin(ph)[:, None] * e2); dd, _ = tree.query(Pts, k=1, distance_upper_bound=2 * math.sin(math.radians(0.03))); return float(np.mean(np.isfinite(dd)))
    chosen = {}; dropped = {}
    for b in range(4):
        cand = il[ok & (bins == b)]; cand = cand[rng.permutation(len(cand))]; ch = []; dr = 0
        for i in cand:
            if len(ch) >= 5000: break
            if coverage(i) >= 0.8: ch.append(i)
            else: dr += 1
        chosen[b] = np.array(ch); dropped[b] = dr; P(f"  bin {b + 1}: {len(ch)} lenses chosen, {dr} dropped on coverage < 0.8 {tm()}")
    allL = np.concatenate([chosen[b] for b in range(4)]); res = np.full((20, len(allL), 4), np.nan); g = np.random.default_rng(20261111)
    zobs = z; dzl = 3 * 0.02 * (1 + zobs)
    for k in range(20):
        zk = np.abs(z + g.normal(0, 0.02 * (1 + z))); Dk = DC(zk); pos = u * Dk[:, None]; f = fvis(zk); t3 = cKDTree(pos)
        for n, i in enumerate(allL):
            tp = pos[i]; js = np.array(t3.query_ball_point(tp, RS), np.int64)
            ang = np.arccos(np.clip(u[js] @ u[i], -1, 1)); Rp = chi70[i] * ang; kp = ~((Rp < 3.0) & (np.abs(zobs[js] - zobs[i]) < dzl[i])) & (js != i)
            js = js[kp]; res[k, n] = e1_of(*field(tp, zk[i], pos[js], Mtot[js], Mtot[js] / f[js], CL, RS))
        if k % 5 == 4: P(f"  MC {k + 1}/20 {tm()}")
    E1 = np.median(res[:, :, 0], 0); hb = np.median(res[:, :, 1], 0); hmc = 0.5 * (np.percentile(res[:, :, 0], 84, 0) - np.percentile(res[:, :, 0], 16, 0)); sig = np.sqrt(hb ** 2 + hmc ** 2)
    wl = np.interp(z[allL], wzc, wv); bl = np.concatenate([np.full(len(chosen[b]), b) for b in range(4)]); R["bins"] = []; bs = np.random.default_rng(20261115)
    for b in range(4):
        m = bl == b; e = E1[m]; w = wl[m]; mu = float(np.sum(w * e) / np.sum(w)); sd = float(np.sqrt(np.sum(w * (e - mu) ** 2) / np.sum(w)))
        boot = [float(np.sum(w[q] * e[q]) / np.sum(w[q])) for q in (bs.integers(0, m.sum(), m.sum()) for _ in range(1000))]
        R["bins"].append(dict(bin=b + 1, n=int(m.sum()), dropped_coverage=dropped[b], E1_weighted=mu, sd=sd, err_mean=float(np.std(boot)), E1_unweighted_median=float(np.median(e)), sigma_median=float(np.median(sig[m])), mean_logMstar=float(np.mean(lm[allL][m]))))
        P(f"  bin {b + 1}: lens-weighted E1 {mu:+.3f} (sd {sd:.3f}, err {np.std(boot):.3f}), median per-lens sigma {np.median(sig[m]):.3f}, n {int(m.sum())}")
    R["lens_E1_status"] = "GRADED" if R["step0"]["passed"] else "UNGRADED (Step 0 FAILED)"
    np.savez(os.path.join(CACHE, "nv2_lens_E1.npz"), idx=ip[allL], E1=E1, sig=sig, bin=bl, w=wl)
    P("lens E1:", R["lens_E1_status"], tm()); return R

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, float) and not math.isfinite(o): return None
    return o
if __name__ == "__main__":
    MODE = sys.argv[1]; sys.path.insert(0, HERE); TAG = MODE + ("_extra" if "--extra" in sys.argv else "")
    R = dict(ka=mode_ka, sparc=mode_sparc, fidelity=mode_fidelity, xcop=mode_xcop, lenses=mode_lenses)[MODE]()
    P(f"\n{tm()}. kappa = 1/2 FITTED; not theory closed.")
    json.dump(clean(R), open(os.path.join(HERE, f"nv2_e1_{TAG}.json"), "w"), indent=0); open(os.path.join(HERE, f"nv2_e1_{TAG}.out"), "w").write("\n".join(OUT) + "\n")
