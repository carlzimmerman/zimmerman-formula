#!/usr/bin/env python3
"""CFG496: hunt for a clue linking COLD ENERGY (Omega_c/Omega_b = R, input) and DARK ENERGY (rho_Lambda; a0 = kappa c sqrt(G rho_L),
kappa = 1/2 FITTED). Criteria: FROZEN_CRITERIA.md (committed alone first). On-disk data only.
Run:  python3 cfg496_hunt.py            -> cfg496.out, cfg496_results.json
      CFG496_MUTATE=1 python3 cfg496_hunt.py -> cfg496_MUTATE.out, cfg496_results_MUTATE.json (scrambled cosmology, 200 draws)"""
import os, sys, json, glob, math
import numpy as np
import sympy as sp
from astropy.io import fits
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
import CFG2_common as C2  # noqa: E402  (read-only: loader, nu_mono, footings)

MUT = os.environ.get("CFG496_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s); OUT.append(str(s))

G, c, MSUN, KPC = C2.G_SI, C2.C_SI, C2.MSUN, C2.KPC
KAPPA = C2.KAPPA
A0 = dict(C2.A0)
RHO_L = C2.RHO_LAMBDA
FOOTS = ("canonical", "alt")
h, OBH2, OCH2 = 0.6736, 0.02237, 0.1200
OB = OBH2 / h ** 2
R_TRUE = OCH2 / OBH2
nu_mono = C2.nu_mono

def cosmo(R):
    Oc = R * OB; Om = OB + Oc; OL = 1.0 - Om
    fb = 1.0 / (1.0 + R); s = math.log1p(1.0 / R)
    return dict(R=R, Ob=OB, Oc=Oc, Om=Om, OL=OL, fb=fb, s=s, ye=s * s, ge=(1 + R) * s * s)

def nu_exp(y):
    return 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))

# ------------------------------------------------------------------ number families (rule 3)
PSET = [1, 2, 3, 4, 8, 1/2, 1/3, 1/4, 1/8, 2/3, 3/2, 3/4, 4/3]
PNAME = ["1", "2", "3", "4", "8", "1/2", "1/3", "1/4", "1/8", "2/3", "3/2", "3/4", "4/3"]
def family_F1(cs):
    vals, names = [], []
    for p, pn in zip(PSET, PNAME):
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for cc in (-1, 0, 1):
                    for d in (-1, 0, 1):
                        vals.append(p * math.pi ** a * KAPPA ** b * cs["OL"] ** cc * cs["Om"] ** d)
                        names.append((pn, a, b, cc, d))
    return np.array(vals), names
def family_F2(cs):
    vals, names = [], []
    for p, pn in zip(PSET, PNAME):
        for a in range(-2, 3):
            for b in range(-2, 3):
                vals.append(p * math.pi ** a * KAPPA ** b); names.append((pn, a, b, 0, 0))
    return np.array(vals), names
def fname(n):
    pn, a, b, cc, d = n
    t = [pn]
    for sym, e in (("pi", a), ("kappa", b), ("OmL", cc), ("Om", d)):
        if e: t.append(f"{sym}^{e}")
    return " ".join(t)

def best_match(v, fam):
    vals, names = fam
    lv = np.log(vals); dd = np.abs(np.log(v) - lv); i = int(np.argmin(dd))
    return float(dd[i]), names[i], float(vals[i])

def lee_p(v, delta, fam, n=20000, seed=496):
    lv = np.sort(np.log(fam[0]))
    rng = np.random.default_rng(seed)
    x = np.log(v) + np.log(10.0) * rng.uniform(-1, 1, n)
    j = np.clip(np.searchsorted(lv, x), 1, len(lv) - 1)
    dmin = np.minimum(np.abs(x - lv[j - 1]), np.abs(x - lv[j]))
    return float(np.mean(dmin <= delta + 1e-15))

def omega_at(cs, z):
    E2 = cs["Om"] * (1 + z) ** 3 + cs["OL"]
    return dict(OL=cs["OL"] / E2, Om=cs["Om"] * (1 + z) ** 3 / E2)

def family_test(tag, v, fam, cs, v_at_z1, fam_kind="F1", nlee=20000):
    d, nm, X = best_match(v, fam)
    match = d <= 0.01
    p = lee_p(v, d, fam, n=nlee)
    has_om = bool(nm[3] or nm[4])
    if not match:
        sec, sec_txt = False, "n/a (no match)"
    elif not has_om:
        sec, sec_txt = False, "NOT AVAILABLE (pure-number form: no second epoch/scale) -> FAIL"
    else:
        oz = omega_at(cs, 1.0)
        pn, a, b, cc, dd_ = nm
        Xz = PSET[PNAME.index(pn)] * math.pi ** a * KAPPA ** b * oz["OL"] ** cc * oz["Om"] ** dd_
        dz = abs(math.log(v_at_z1 / Xz)); sec = dz <= 0.03
        sec_txt = f"z=1: value {v_at_z1:.4g} vs form {Xz:.4g} (|dln| {dz:.3f}, need <= 0.03) -> {'PASS' if sec else 'FAIL'}"
    if match and p < 0.01 and sec: lab = "CLUE"
    elif match: lab = "COINCIDENCE"
    else: lab = "NO MATCH"
    return dict(tag=tag, value=v, best_form=fname(nm), form_value=X, delta=d, match=match, p_lee=p, second=sec,
                second_txt=sec_txt, label=lab, family=fam_kind, n_forms=len(fam[0]))

# ------------------------------------------------------------------ sympy (C01, C02, C10, C07, K1)
def sympy_checks():
    R, k, Gs, cs_, rho, M, z, X = sp.symbols("R kappa G c rho M z X", positive=True)
    s = sp.log(1 + 1 / R)
    ye = s ** 2
    nu_e = 1 / (1 - sp.exp(-sp.sqrt(ye)))
    c01 = sp.simplify(nu_e - (1 + R)) == 0
    k1_wrong = sp.simplify(nu_e - R) == 0                  # must be False
    # C02 deep form: edge y_e = f_b^2, r_e = r_M/f_b, M_tot = M/f_b, SIS sigma^2 = G M_tot/(2 r_e)
    a0 = k * cs_ * sp.sqrt(Gs * rho)
    fb = 1 / (1 + R); rM = sp.sqrt(Gs * M / a0)
    sig2 = Gs * (M / fb) / (2 * rM / fb)
    c02 = sp.simplify(sig2 ** 2 - Gs * M * a0 / 4) == 0
    exact_fac = sp.simplify(((1 + R) * s) ** 2)            # exact-kernel factor on sigma^4
    # C10: a0/(c H) with H^2 = 8 pi G rho_L/(3 OmL(z)) -> kappa sqrt(3 OmL/(8 pi))
    OLz = sp.symbols("OmL_z", positive=True)
    H = sp.sqrt(8 * sp.pi * Gs * rho / (3 * OLz))
    ratio = sp.simplify(a0 / (cs_ * H))
    c10 = sp.simplify(ratio - k * sp.sqrt(3 * OLz / (8 * sp.pi))) == 0
    thr = sp.solve(sp.Eq(ratio, X), OLz)[0]               # marker a0 = X c H(z) <=> OmL(z) = thr
    # C07 Buckingham: dims (M, L, T) of G, c, rho, Mb
    D = sp.Matrix([[-1, 0, 1, 1], [3, 1, -3, 0], [-2, -1, 0, 0]])
    ns = D.nullspace()
    # edge quantities with exact kernel, expressed in G, c, rho, M, R, kappa
    re = rM / s; Mt = (1 + R) * M
    sig2e = Gs * Mt / (2 * re)
    Q = dict(r_edge=re, M_tot=Mt, rho_edge_local=sig2e / (2 * sp.pi * Gs * re ** 2), rho_mean=3 * Mt / (4 * sp.pi * re ** 3),
             t_dyn=sp.sqrt(re ** 3 / (Gs * Mt)), V_edge=sp.sqrt(Gs * Mt / re), g_edge=Gs * Mt / re ** 2,
             Sigma_edge=Mt / (sp.pi * re ** 2), P_edge=(sig2e / (2 * sp.pi * Gs * re ** 2)) * sig2e)
    a0s = sp.symbols("a0", positive=True)
    rows = {}
    for nmq, q in Q.items():
        mexp = sp.simplify(M * sp.diff(sp.log(q), M))
        mfree = (mexp == 0)
        # does q depend on (c, rho) only through a0? substitute rho = a0^2/(k^2 c^2 G) and test c-independence
        qa = sp.simplify(q.subs(rho, a0s ** 2 / (k ** 2 * cs_ ** 2 * Gs)))
        via_a0 = sp.simplify(sp.diff(qa, cs_)) == 0
        rows[nmq] = dict(M_exponent=str(mexp), mass_free=bool(mfree), c_rho_only_via_a0=bool(via_a0), in_a0=str(sp.simplify(qa)))
    return dict(c01=bool(c01), k1_wrong_fails=not bool(k1_wrong), c02_deep=bool(c02), c02_exact_factor=str(exact_fac),
                c10=bool(c10), c10_threshold=str(sp.simplify(thr)), pi_groups=[str(list(v)) for v in ns], edge_quantities=rows)

# ------------------------------------------------------------------ structural scale-free (C04-C06)
def scale_free(cs, foot):
    a0 = A0[foot]; rhoL = RHO_L                              # the record's rho_Lambda (FP0) on both footings
    lM = np.linspace(7, 15, 81); Mb = 10 ** lM * MSUN
    rM = np.sqrt(G * Mb / a0); re = rM / cs["s"]; Mt = (1 + cs["R"]) * Mb
    sig2 = G * Mt / (2 * re)
    rho_loc = sig2 / (2 * math.pi * G * re ** 2); rho_mean = 3 * Mt / (4 * math.pi * re ** 3)
    t_e = np.sqrt(re ** 3 / (G * Mt)); tL = 1 / math.sqrt(G * rhoL)
    RL = (3 * Mt / (8 * math.pi * rhoL)) ** (1 / 3)
    out = {}
    for nm, ratio, target, tname in (("C04 rho_edge_local/rho_L", rho_loc / rhoL, None, None),
                                     ("C04 rho_mean(<r_edge)/rho_L", rho_mean / rhoL, 200 / C2_OL_TRUE, "200 rho_crit"),
                                     ("C05 t_edge/t_L", t_e / tL, 1.0, "t_L"),
                                     ("C06 r_edge/R_Lambda", re / RL, 1.0, "R_Lambda")):
        sl = np.polyfit(lM * math.log(10), np.log(ratio), 1)[0]
        cross = None
        if target is not None:
            if True:
                coef = np.polyfit(lM, np.log10(ratio), 1)
                cross = float((math.log10(target) - coef[1]) / coef[0])
        out[nm] = dict(slope=float(sl), scale_free=bool(abs(sl) <= 0.02), ratio_1e7=float(ratio[0]), ratio_1e11=float(ratio[40]),
                       ratio_1e15=float(ratio[-1]), crossing_target=tname, log10_Mb_crossing=cross,
                       label="NO MATCH" if abs(sl) > 0.02 else "SCALE-FREE")
    return out

C2_OL_TRUE = cosmo(R_TRUE)["OL"]

# ------------------------------------------------------------------ X-COP (C13)
XD = os.path.join(REPO, "real_research", "data", "xcop")
def loginterp(x, xp, fp):
    return np.exp(np.interp(np.log(x), np.log(xp), np.log(fp), left=np.nan, right=np.nan))
XJ = json.load(open(os.path.join(XD, "xcop_r500_ettori2019.json")))
XC = []
for d in sorted(glob.glob(os.path.join(XD, "*", ""))):
    n = os.path.basename(os.path.dirname(d))
    with fits.open(os.path.join(d, n + "_hydro_mass.fits")) as f:
        rh = np.array(f[1].data["RADIUS"], float); mh = np.array(f[1].data["M_FORW"], float)
    with fits.open(os.path.join(d, n + "_fgas_profile.fits")) as f:
        r500 = float(f[1].header["R500"]); rg = np.array(f[1].data["RADIUS"], float) * r500; mg = np.array(f[1].data["MGAS"], float)
    st = os.path.join(d, n + "_mstar.fits"); rs = ms = None
    if os.path.exists(st):
        with fits.open(st) as f:
            rs = np.array(f[2].data["RADIUS"], float); ms = np.array(f[2].data["MSTAR"], float)
    XC.append(dict(name=n, r500=r500, rh=rh, mh=mh, rg=rg, mg=mg, rs=rs, ms=ms, M500=XJ[n]["M500"]))
# K3: CFG432 data identity on 0.1-1 R500
_k3 = True
for cl in XC:
    rr = np.logspace(np.log10(0.1 * cl["r500"]), np.log10(cl["r500"]), 16)
    for v in (loginterp(rr, cl["rh"], cl["mh"]), loginterp(rr, cl["rg"], cl["mg"])):
        _k3 &= bool(np.all(np.isfinite(v) & (v > 0)))
# stellar ratio M*/Mgas vs x = r/R500 (median over clusters with files), held constant outside each file's range
XG = np.logspace(np.log10(0.05), np.log10(2.7), 200)
_rat = []
for cl in XC:
    if cl["rs"] is None: continue
    rr = XG * cl["r500"]
    q = loginterp(rr, cl["rs"], cl["ms"]) / loginterp(rr, cl["rg"], cl["mg"])
    _rat.append(q)
_rat = np.array(_rat)
MED_RAT = np.nanmedian(_rat, axis=0)
ok = np.isfinite(MED_RAT); MED_RAT = np.interp(np.arange(len(XG)), np.where(ok)[0], MED_RAT[ok])
for cl in XC:
    rr = XG * cl["r500"]; meas = rr <= cl["rg"].max()
    mgas = loginterp(rr, cl["rg"], cl["mg"]); mhse = loginterp(rr, cl["rh"], cl["mh"])
    if cl["rs"] is not None:
        q = loginterp(rr, cl["rs"], cl["ms"]) / mgas
        okq = np.isfinite(q)
        q = np.interp(np.arange(len(rr)), np.where(okq)[0], q[okq])   # held at end values outside the file's range
    else:
        q = MED_RAT
    cl.update(grid=rr[meas], mb=(mgas * (1 + q))[meas], mhse=mhse[meas])

def xcop_test(cs, nboot=2000, seed=496):
    res = {}
    allmatch, allsec = True, True
    for foot in FOOTS:
        a0 = A0[foot]
        for b in (0.0, 0.3):
            ly, lm, cens = [], [], 0
            for cl in XC:
                ratio = cl["mhse"] / (1 - b) / cl["mb"]
                below = np.where(ratio <= 1 + cs["R"])[0]
                if len(below) == 0 or below[0] == 0:
                    if len(below) == 0: cens += 1
                    i = len(ratio) - 1 if len(below) == 0 else 0
                    rx = cl["grid"][i]; mbx = cl["mb"][i]
                else:
                    i = below[0]; f = (math.log(1 + cs["R"]) - math.log(ratio[i - 1])) / (math.log(ratio[i]) - math.log(ratio[i - 1]))
                    rx = math.exp(math.log(cl["grid"][i - 1]) + f * (math.log(cl["grid"][i]) - math.log(cl["grid"][i - 1])))
                    mbx = math.exp(math.log(cl["mb"][i - 1]) + f * (math.log(cl["mb"][i]) - math.log(cl["mb"][i - 1])))
                y = G * mbx * MSUN / (rx * KPC) ** 2 / a0
                ly.append(math.log10(y)); lm.append(math.log10(cl["M500"]))
            ly, lm = np.array(ly), np.array(lm)
            rng = np.random.default_rng(seed)
            idx = rng.integers(0, len(ly), (nboot, len(ly)))
            med = np.median(ly); bmed = np.median(ly[idx], axis=1); sd = float(np.std(bmed))
            dlt = med - math.log10(cs["ye"])
            sl = np.polyfit(lm, ly, 1)[0]
            bsl = np.array([np.polyfit(lm[j], ly[j], 1)[0] if np.ptp(lm[j]) > 0 else np.nan for j in idx[:500]])
            ssd = float(np.nanstd(bsl))
            match = abs(dlt) <= 0.15 and abs(dlt) <= 2 * max(sd, 1e-9)
            sec = abs(sl) <= 2 * ssd
            allmatch &= match; allsec &= sec
            res[f"{foot}|b{b}"] = dict(median_log_ymix=float(med), sd=sd, log_ye=math.log10(cs["ye"]), Delta=float(dlt),
                                       censored=cens, slope_vs_M500=float(sl), slope_sd=ssd, match=bool(match), no_trend=bool(sec),
                                       ymix_per_cluster=dict(zip([cl["name"] for cl in XC], [float(v) for v in ly])))
    worst = max(abs(v["Delta"]) for v in res.values())
    p = min(1.0, 2 * worst / 3.0)
    lab = "CLUE" if (allmatch and p < 0.01 and allsec) else ("COINCIDENCE" if allmatch else "NO MATCH")
    return dict(cells=res, all_match=bool(allmatch), all_no_trend=bool(allsec), p_lee=p, label=lab)

# ------------------------------------------------------------------ SPARC (C14, C15, K4)
GAL = C2.load_sparc()
UNIT = 1e6 / 3.0857e19
SP = []
for g in GAL:
    m = g["meta"]
    if m is None or m["Q"] >= 3 or m["Inc"] < 30: continue
    vb2 = np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2
    okp = (vb2 > 0) & (g["Vobs"] > 0) & (g["R"] > 0)
    if okp.sum() < 3: continue
    R_ = g["R"][okp]
    gobs = g["Vobs"][okp] ** 2 / R_ * UNIT; gN = vb2[okp] / R_ * UNIT
    Mb = (0.5 * m["L36"] + 1.33 * m["MHI"]) * 1e9
    SP.append(dict(name=g["name"], R=R_, gobs=gobs, gN=gN, Mb=Mb, Rlast=float(R_.max()), SBeff=m["SBeff"], Q=m["Q"]))

def sparc_arrays(foot):
    a0 = A0[foot]
    out = []
    for gg in SP:
        y = gg["gN"] / a0
        r = np.log10(gg["gobs"]) - np.log10(nu_mono(y) * gg["gN"])
        out.append((y, r))
    return out

SPA = {f: sparc_arrays(f) for f in FOOTS}

def edge_stat(foot, ye, R, nboot=2000, seed=496):
    arr = SPA[foot]
    S1 = np.array([r[y < ye].sum() for y, r in arr]); n1 = np.array([(y < ye).sum() for y, r in arr])
    m2 = [(y >= ye) & (y < 3 * ye) for y, r in arr]
    S2 = np.array([r[mm].sum() for (y, r), mm in zip(arr, m2)]); n2 = np.array([mm.sum() for mm in m2])
    SPd = np.array([np.log10((1 + R) / nu_mono(y[y < ye])).sum() if (y < ye).any() else 0.0 for y, r in arr])
    if n1.sum() < 5 or n2.sum() < 5:
        return None
    D = S1.sum() / n1.sum() - S2.sum() / n2.sum(); Dp = SPd.sum() / n1.sum()
    rng = np.random.default_rng(seed); idx = rng.integers(0, len(arr), (nboot, len(arr)))
    bn1 = n1[idx].sum(1); bn2 = n2[idx].sum(1); okb = (bn1 > 0) & (bn2 > 0)
    bD = S1[idx].sum(1)[okb] / bn1[okb] - S2[idx].sum(1)[okb] / bn2[okb]
    sd = float(np.std(bD))
    match = abs(D) >= 3 * sd and abs(D - Dp) <= 2 * sd
    return dict(Delta=float(D), sd=sd, Delta_pred=float(Dp), n_below=int(n1.sum()), n_inside=int(n2.sum()),
                n_gal_below=int((n1 > 0).sum()), match=bool(match))

def sparc_edge_test(cs, nlee=200, seed=496, nboot=2000):
    cells = {f: edge_stat(f, cs["ye"], cs["R"], nboot=nboot) for f in FOOTS}
    allm = all(v is not None and v["match"] for v in cells.values())
    rng = np.random.default_rng(seed)
    Rp = np.exp(rng.uniform(math.log(1.5), math.log(20), nlee))
    hits = 0
    for Rq in Rp:
        yt = math.log1p(1 / Rq) ** 2
        ok_all = True
        for f in FOOTS:
            e = edge_stat(f, yt, Rq, nboot=300, seed=seed + 1)
            ok_all &= (e is not None and e["match"])
        hits += ok_all
    p = hits / nlee
    return dict(cells=cells, all_match=bool(allm), p_lee=float(p))

def sparc_corr(nsh=2000, seed=496):
    out = {}
    for foot in FOOTS:
        a0 = A0[foot]; cs = cosmo(R_TRUE)
        res = np.array([r.mean() for y, r in SPA[foot]])
        X1 = np.array([math.log10(gg["Rlast"] * KPC / (math.sqrt(G * gg["Mb"] * MSUN / a0) / cs["s"])) for gg in SP])
        X2 = np.array([math.log10(max(0.5 * gg["SBeff"], 1e-3) / C2.SIGMA_M[foot]) for gg in SP])
        r1 = spearmanr(res, X1)[0]; r2 = spearmanr(res, X2)[0]
        obs = max(abs(r1), abs(r2))
        rng = np.random.default_rng(seed); cnt = 0
        for _ in range(nsh):
            rs_ = rng.permutation(res)
            cnt += max(abs(spearmanr(rs_, X1)[0]), abs(spearmanr(rs_, X2)[0])) >= obs
        p = cnt / nsh
        # invariance under R: X1 shifts by a constant
        X1b = X1 - math.log10(cs["s"]) + math.log10(math.log1p(1 / 3.0))
        inv = abs(spearmanr(res, X1b)[0] - r1) < 1e-12
        out[foot] = dict(rho_Rlast_over_redge=float(r1), rho_Sigma_over_SigmaM=float(r2), p_lee=float(p), R_invariant=bool(inv),
                         median_residual=float(np.median(np.concatenate([r for y, r in SPA[foot]]))), n_gal=len(SP))
    anyp = any(v["p_lee"] < 0.01 for v in out.values())
    out["label"] = "BUILT-IN (law residual, R-invariant)" if anyp else "NO MATCH"
    return out

# ------------------------------------------------------------------ C08 / C09 inputs from committed results
J424 = json.load(open(os.path.join(CFG, "CFG424_turnaround_catchment", "cfg424_results.json")))
J460 = json.load(open(os.path.join(CFG, "CFG460_zero_knob_512_second_seed", "cfg460_results.json")))
Q256 = {"canonical": J424["TA-can"]["q_max"], "alt": J424["TA-alt"]["q_max"]}
Q512 = float(J460["q_max"])
PMSRC = open(os.path.join(CFG, "CFG424_turnaround_catchment", "cfg424_pm.py")).read()
C09_lines = ["rM = math.sqrt(6.674e-11 * Mbn * 1.989e30 / a0p)", "math.log(1.0 + fr * FB / (1.0 - FB))", "Mbn = fr * FB * Mta"]
C09_builtin = all(t in PMSRC for t in C09_lines)

def c08_test(cs):
    v = Q256["canonical"] * cs["R"] / R_TRUE
    fam = family_F1(cs)
    d, nm, X = best_match(v, fam)
    match = d <= 0.01
    p = lee_p(v, d, fam)
    v512 = Q512 * cs["R"] / R_TRUE
    sec = abs(math.log(v512 / v)) <= 0.10
    lab = "CLUE" if (match and p < 0.01 and sec) else ("COINCIDENCE" if match else "NO MATCH")
    dOm = abs(math.log(v / cs["Om"]))
    return dict(value=v, best_form=fname(nm), delta=d, match=match, p_lee=p, q512=v512, second=bool(sec),
                delta_vs_Omega_m=dOm, label=lab)

# ------------------------------------------------------------------ the hunt for one cosmology
def hunt(cs, full=True):
    L = {}
    L["C01"] = dict(label="BUILT-IN")
    L["C02"] = dict(label="BUILT-IN")
    L["C03"] = family_test("C03 g_e/a0", cs["ge"], family_F1(cs), cs, cs["ge"])
    L["C08"] = c08_test(cs)
    rc_rl = cs["Oc"] / cs["OL"]
    L["C11"] = family_test("C11 Om_c/Om_L", rc_rl, family_F2(cs), cs, rc_rl * 8.0, fam_kind="F2")
    L["C12"] = family_test("C12 R", cs["R"], family_F1(cs), cs, cs["R"])
    L["C13"] = xcop_test(cs, nboot=2000 if full else 400)
    if full:
        L["C14"] = sparc_edge_test(cs)
    else:
        cells = {f: edge_stat(f, cs["ye"], cs["R"], nboot=300) for f in FOOTS}
        L["C14"] = dict(cells=cells, all_match=all(v is not None and v["match"] for v in cells.values()), p_lee=None)
    # C14 classification: match + LEE + second check (C13 match)
    c14 = L["C14"]
    if not c14["all_match"]: lab14 = "NO MATCH"
    elif full and c14["p_lee"] < 0.01 and L["C13"]["all_match"]: lab14 = "CLUE"
    elif not full and L["C13"]["all_match"]: lab14 = "CLUE (LEE not re-run in MUTATE)"
    else: lab14 = "COINCIDENCE"
    c14["label"] = lab14
    return L

def nclues(L):
    return sum(1 for k, v in L.items() if isinstance(v, dict) and str(v.get("label", "")).startswith("CLUE"))

# ================================================================== main
if not MUT:
    P("CFG496: hunt for a clue linking COLD ENERGY (Omega_c/Omega_b) and DARK ENERGY (rho_Lambda). kappa = 1/2 FITTED.")
    P("On-disk data only. Both footings, never pooled. Criteria: FROZEN_CRITERIA.md.")
    cs = cosmo(R_TRUE)
    P(f"R = {cs['R']:.4f}  f_b = {cs['fb']:.5f}  s = {cs['s']:.5f}  y_e = {cs['ye']:.5f}  g_e/a0 = {cs['ge']:.5f}  "
      f"Om = {cs['Om']:.4f}  OmL = {cs['OL']:.4f}")
    S = sympy_checks()
    k1 = S["c01"] and S["c02_deep"] and S["c10"] and S["k1_wrong_fails"]
    P("")
    P("== Structural (sympy, symbolic R and kappa)")
    P(f"C01 nu(y_e = ln^2(1+1/R)) == 1 + R identically: {S['c01']}  -> BUILT-IN (the edge is DEFINED by the phantom using R M_b)")
    P(f"C02 deep form sigma^4 == G M_b a0/4 for any R: {S['c02_deep']}; exact-kernel factor on sigma^4 = {S['c02_exact_factor']} "
      f"= {((1+cs['R'])*cs['s'])**2:.4f} (+{math.log10(((1+cs['R'])*cs['s'])**2):.3f} dex, = CFG461 R0)  -> BUILT-IN")
    fam = family_F1(cs)
    k2v = 3 * math.pi * KAPPA * cs["Om"]; k2d, _, _ = best_match(k2v, fam); k2p = lee_p(k2v, k2d, fam)
    k2 = k2d < 1e-12 and k2p < 0.01
    hres = hunt(cs, full=True)
    c3 = hres["C03"]
    P(f"C03 g_e/a0 = {c3['value']:.5f}; best F1 form {c3['best_form']} = {c3['form_value']:.5f} (|dln| {c3['delta']:.4f}); "
      f"match(<=0.01) {c3['match']}; look-elsewhere p = {c3['p_lee']:.3f}; second: {c3['second_txt']}  -> {c3['label']}")
    P(f"     (deep limit: g_e -> f_b a0 = {cs['fb']:.4f} a0; the 0.186 is f_b dressed by the kernel, i.e. set by the law)")
    sf = {f: scale_free(cs, f) for f in FOOTS}
    for nm in sf["canonical"]:
        a, b = sf["canonical"][nm], sf["alt"][nm]
        cr = "" if a["crossing_target"] is None else (f"; equals {a['crossing_target']} at log M_b = {a['log10_Mb_crossing']:.2f} "
                                                      f"(can) / {b['log10_Mb_crossing']:.2f} (alt)")
        P(f"{nm}: d ln/d ln M_b = {a['slope']:+.3f} (can) / {b['slope']:+.3f} (alt); value 1e7/1e11/1e15 = "
          f"{a['ratio_1e7']:.3g}/{a['ratio_1e11']:.3g}/{a['ratio_1e15']:.3g}{cr}  -> {a['label']} (not scale-free)")
    P(f"C07 Buckingham: dims (M,L,T) of (G, c, rho_L, M_b) -> Pi groups {S['pi_groups']} (one group, Pi = G^3 M_b^2 rho_L / c^6)")
    for nmq, row in S["edge_quantities"].items():
        P(f"     {nmq:15s} M-exponent {row['M_exponent']:>5s}  mass-free {str(row['mass_free']):5s}  c, rho_L only via a0 "
          f"{row['c_rho_only_via_a0']}")
    mf = [k for k, v in S["edge_quantities"].items() if v["mass_free"]]
    c07_builtin = all(S["edge_quantities"][k]["c_rho_only_via_a0"] for k in mf)
    P(f"     mass-free edge quantities: {mf}; all enter dark energy only through a0 -> "
      f"{'BUILT-IN' if c07_builtin else 'NOT BUILT-IN'} (no scale-free cold-dark relation beyond the law exists in the record's model)")
    P("")
    P("== Simulation (committed zero-knob runs)")
    c8 = hres["C08"]
    P(f"C08 q_max 256^3 seed 359 = {Q256['canonical']:.3f} (can) / {Q256['alt']:.3f} (alt); Omega_m = {cs['Om']:.4f} "
      f"(|dln| {c8['delta_vs_Omega_m']:.3f} > 0.01); best F1 form {c8['best_form']} |dln| {c8['delta']:.4f}, p = {c8['p_lee']:.3f}; "
      f"512^3 seed 360 (CFG460) = {Q512:.3f} (second check {'PASS' if c8['second'] else 'FAIL'}: an extreme statistic that moves "
      f"with resolution/seed)  -> {c8['label']}")
    P(f"C09 cfg424_pm.py computes the settled supply as f_ret f_b M_ta and the edge as r_M/ln(1+f_ret f_b/(1-f_b)) with "
      f"r_M = sqrt(G M_b/a0(a)): {C09_builtin} -> every a0 regularity of the settled cold energy is put in by the code: BUILT-IN")
    P("")
    P("== Epoch")
    P(f"C10 a0/(c H(z)) == kappa sqrt(3 OmL(z)/(8 pi)) identically: {S['c10']}. Any framework epoch marker a0 = X c H(z) is the "
      f"threshold OmL(z) = {S['c10_threshold']}.")
    thr = 2 / (3 * math.pi * KAPPA ** 2)
    P(f"     e.g. X = 1/(2 pi): OmL(z*) = {thr:.3f} > today's {cs['OL']:.3f} (a future epoch). rho_c = rho_L at z = "
      f"{(cs['OL']/cs['Oc'])**(1/3)-1:.3f}; rho_m = rho_L at z = {(cs['OL']/cs['Om'])**(1/3)-1:.3f}.")
    P("     The framework has no dynamics that sets Omega_c/Omega_Lambda: R is an input, rho_L is an input, and the 'MOND coincidence'")
    P("     a0 ~ cH0/6 IS the cosmic coincidence written through kappa (L258).  -> BUILT-IN (input; no 'why now')")
    c11 = hres["C11"]
    P(f"C11 Omega_c/Omega_L = {c11['value']:.4f}; best F2 form {c11['best_form']} = {c11['form_value']:.4f} (|dln| {c11['delta']:.4f}); "
      f"match {c11['match']}; p = {c11['p_lee']:.3f}; second: {c11['second_txt']}  -> {c11['label']}")
    c12 = hres["C12"]
    P(f"C12 R = {c12['value']:.4f}; best F1 form {c12['best_form']} = {c12['form_value']:.4f} (|dln| {c12['delta']:.4f}); "
      f"match {c12['match']}; p = {c12['p_lee']:.3f}; second: {c12['second_txt']}  -> {c12['label']}")
    P("")
    P("== Data")
    c13 = hres["C13"]
    P(f"C13 X-COP ({len(XC)} clusters; K3 CFG432 data identity {'PASS' if _k3 else 'FAIL'}): y_mix where M_HSE/(1-b)/M_b = 1+R, "
      f"vs galaxy edge log y_e = {math.log10(cs['ye']):.3f}")
    for k, v in c13["cells"].items():
        P(f"     {k:14s} median log y_mix {v['median_log_ymix']:+.3f} +- {v['sd']:.3f}  Delta {v['Delta']:+.3f} dex  censored {v['censored']}  "
          f"slope vs log M500 {v['slope_vs_M500']:+.2f} +- {v['slope_sd']:.2f}  match {v['match']}  no-trend {v['no_trend']}")
    P(f"     look-elsewhere p (worst cell, 3-dex prior) = {c13['p_lee']:.3f}  -> {c13['label']}")
    c14 = hres["C14"]
    P(f"C14 SPARC ({len(SP)} galaxies, Q<3, Inc>=30, Ups 0.5/0.7): Delta = mean res(y<y_e) - mean res(y_e<=y<3y_e); edge cap predicts Delta_pred")
    for f, v in c14["cells"].items():
        P(f"     {f:9s} Delta {v['Delta']:+.4f} +- {v['sd']:.4f}  Delta_pred {v['Delta_pred']:+.4f}  points below/inside "
          f"{v['n_below']}/{v['n_inside']} ({v['n_gal_below']} galaxies below)  match {v['match']}")
    P(f"     look-elsewhere: fraction of 200 random thresholds y_t = ln^2(1+1/R'), R' in [1.5, 20], that also match = {c14['p_lee']:.3f}"
      f"; second check = C13 match {c13['all_match']}  -> {c14['label']}")
    c15 = sparc_corr()
    for f in FOOTS:
        v = c15[f]
        P(f"C15 {f:9s} rho(res, log R_last/r_edge) {v['rho_Rlast_over_redge']:+.3f}  rho(res, log Sigma_eff/Sigma_M) "
          f"{v['rho_Sigma_over_SigmaM']:+.3f}  p_LEE(max|rho|, 2000 shuffles) {v['p_lee']:.4f}  R-invariant {v['R_invariant']}")
    P(f"     -> {c15['label']}  (R enters only as a constant offset, so no correlation can carry the cold-energy amount)")
    K4 = all(abs(c15[f]["median_residual"]) < 0.1 for f in FOOTS)
    P(f"K4 SPARC nu_mono median residual: can {c15['canonical']['median_residual']:+.3f} / alt {c15['alt']['median_residual']:+.3f} dex -> "
      f"{'PASS' if K4 else 'FAIL'}")
    P(f"K1 sympy identities + wrong-identity control: {'PASS' if k1 else 'FAIL'};  K2 planted 3 pi kappa Om: delta {k2d:.1e}, p {k2p:.4f} "
      f"-> {'PASS' if k2 else 'FAIL'};  K3 {'PASS' if _k3 else 'FAIL'}")
    table = [("C01", "edge mix = cosmic mix", "BUILT-IN"), ("C02", "sigma^4 = G M_b a0/4 from the share", "BUILT-IN"),
             ("C03", "g_e/a0 = 0.186 = simple DE number", c3["label"]),
             ("C04", "edge density / rho_L scale-free", sf["canonical"]["C04 rho_mean(<r_edge)/rho_L"]["label"]),
             ("C05", "edge time / vacuum time scale-free", sf["canonical"]["C05 t_edge/t_L"]["label"]),
             ("C06", "r_edge / R_Lambda scale-free", sf["canonical"]["C06 r_edge/R_Lambda"]["label"]),
             ("C07", "mass-free relation not set by a0", "BUILT-IN" if c07_builtin else "OPEN"),
             ("C08", "q_max = Omega_m", c8["label"]), ("C09", "sim settled-a0 regularity", "BUILT-IN" if C09_builtin else "OPEN"),
             ("C10", "why now", "BUILT-IN" if S["c10"] else "OPEN"), ("C11", "Omega_c/Omega_L = simple number", c11["label"]),
             ("C12", "R = simple DE number", c12["label"]), ("C13", "X-COP cosmic mix at y_e", c13["label"]),
             ("C14", "SPARC edge feature at y_e", c14["label"]), ("C15", "SPARC residual vs DE-scaled quantities", c15["label"])]
    P("")
    P("== Candidate table")
    for t in table: P(f"  {t[0]}  {t[1]:42s} {t[2]}")
    ncl = sum(1 for t in table if t[2].startswith("CLUE"))
    P(f"CLUES: {ncl}")
    ctrl = k1 and k2 and _k3 and K4
    P(f"Controls K1-K4: {'PASS' if ctrl else 'FAIL'}.  kappa = 1/2 FITTED; cold energy's mass still required; no particle; not 'theory closed'.")
    json.dump(dict(cosmology=cs, sympy=S, scale_free=sf, hunt=hres, C15=c15, C09_builtin=C09_builtin, C07_builtin=c07_builtin,
                   table=table, n_clues=ncl, controls=dict(K1=k1, K2=k2, K3=_k3, K4=K4)),
              open(os.path.join(HERE, "cfg496_results.json"), "w"), indent=1, default=lambda o: o if not isinstance(o, np.generic) else o.item())
    open(os.path.join(HERE, "cfg496.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if ctrl else 1)
else:
    P("CFG496 MUTATE: scrambled cosmology. 200 draws R' ~ U[3, 8] (seed 4960), Omega_b fixed, flat; a0 footings held.")
    P("R-invariant candidates (C04-C07, C09, C10, C15) keep their labels (BUILT-IN / NO MATCH); C01/C02 stay BUILT-IN for any R'.")
    rng = np.random.default_rng(4960)
    Rs = rng.uniform(3, 8, 200)
    rows = []
    for i, Rq in enumerate(Rs):
        cs = cosmo(float(Rq))
        L = hunt(cs, full=False)
        n = nclues(L)
        rows.append(dict(R=float(Rq), n_clues=n, labels={k: v["label"] for k, v in L.items()},
                         C13_match=L["C13"]["all_match"], C14_match=L["C14"]["all_match"],
                         C13_Delta_can_b0=L["C13"]["cells"]["canonical|b0.0"]["Delta"]))
        if i < 10 or n:
            P(f"  draw {i:3d} R'={Rq:5.3f}: " + "  ".join(f"{k}:{v['label']}" for k, v in L.items()) + f"  -> clues {n}")
    nc = np.array([r["n_clues"] for r in rows])
    fam_lab = {k: sum(1 for r in rows if r["labels"][k] == "COINCIDENCE") for k in ("C03", "C08", "C11", "C12")}
    P("")
    P(f"mean CLUE labels per draw = {nc.mean():.3f}; fraction of draws with >= 1 CLUE = {np.mean(nc > 0):.3f}  (false-positive rate)")
    P(f"COINCIDENCE counts over 200 draws (a 1% family match that fails the controls): {fam_lab}")
    P(f"C13 X-COP match fraction = {np.mean([r['C13_match'] for r in rows]):.3f};  C14 SPARC edge match fraction = "
      f"{np.mean([r['C14_match'] for r in rows]):.3f}")
    d13 = np.array([r["C13_Delta_can_b0"] for r in rows])
    P(f"C13 Delta (canonical, b=0) across R': min {d13.min():+.3f}, median {np.median(d13):+.3f}, max {d13.max():+.3f} dex")
    json.dump(dict(draws=rows, mean_clues=float(nc.mean()), frac_with_clue=float(np.mean(nc > 0)), coincidence_counts=fam_lab),
              open(os.path.join(HERE, "cfg496_results_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg496_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0)
