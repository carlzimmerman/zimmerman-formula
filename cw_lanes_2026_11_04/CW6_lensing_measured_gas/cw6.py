#!/usr/bin/env python3
"""CW6_lensing_measured_gas (FROZEN_CRITERIA.md, 7ac475d533): the law's KiDS galaxy-lensing gap with the gas the record measured.
Each harness's fixed hot-gas term is swapped for Zhang's beta profile at the published DESI DR2 x ACT kSZ amplitude. Nothing else changes.
  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 10 python3 -I cw6.py ksz                 K2 and the F1/F2 fits on the DR2 points
  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 10 python3 -I cw6.py gas                 K3 and the profile table
  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 10 python3 -I cw6.py le1 [--mutate]      H1: A30 (G1), A30 no two-halo, A1, G3 on B21 Fig-3 (LE1's harness)
  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 10 python3 -I cw6.py b21c [--mutate]     H2: B21 Fig-8 colour bins through S2's forward model (L4 row)
  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 10 python3 -I cw6.py si2 <p2_work_dir> [--mutate]   H3: SI2's spectroscopically isolated lenses by colour
  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 nice -n 10 python3 -I cw6.py verdict [--mutate]  labels from the JSONs, frozen precedence
Outputs cw6_<mode>[_MUTATE].{json,out}. --mutate zeroes the gas term everywhere (stars and cold gas kept).
Graders are exec'd or copied read-only; nothing outside this folder is written (CRG1's cache dirs point to ./cache_crg, gitignored).
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import json, math, os, sys, time, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True; os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import numpy as np
from scipy.special import erfc
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); RB = os.path.join(REPO, "rebuild_2026_10_22")
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]; MODE = ARGS[0] if ARGS else "gas"; MUT = "--mutate" in sys.argv[1:]; SFX = "_MUTATE" if MUT else ""
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10); FEET = ("canonical", "alt"); T0 = time.time()
OUT = []; RES = {"lane": "CW6_lensing_measured_gas", "criteria": "7ac475d533", "mode": MODE, "mutate": MUT}
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9          # bytes on macOS -> GB
def tick(): return f"[{time.time() - T0:.0f} s, RSS {rss():.2f} GB]"
def save():
    RES["runtime_s"] = time.time() - T0; RES["peak_rss_gb"] = rss()
    json.dump(RES, open(os.path.join(HERE, f"cw6_{MODE}{SFX}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cw6_{MODE}{SFX}.out"), "w").write("\n".join(OUT) + "\n")

# ============================================================== gas profiles (FROZEN_CRITERIA.md, "Gas profiles")
BETA, RCK, NORM = 0.43, 6.0, 1.84                                       # Zhang et al. 2024: beta, r_c [kpc], M(<R_vir)/M*
ZTF = np.array([[9, 82.], [9.5, 102.], [10, 131.], [10.5, 178.], [10.75, 210.], [11, 295.], [11.25, 480.], [11.5, 950.]])   # GH10's copy of Zhang's Table 1
def Rvir(l): return float(np.interp(l, ZTF[:, 0], ZTF[:, 1]))          # kpc, clamped at the table ends
def base(r): return (1 + (np.asarray(r, float) / RCK) ** 2) ** (-1.5 * BETA)
def taper(r, kR, form, w=0.3):
    if form == "F1": return np.exp(-.5 * (r / kR) ** 2)
    return .5 * erfc(np.log(np.maximum(r, 1e-6) / kR) / (math.sqrt(2) * w))
_QC = {}
def qprof(shape, k, lmg, w=0.3, cache=True):
    """(ln r [kpc], q(r) = I_f(r) / I_f(R_vir)) for the template shape at gas-rule mass lmg; I_f = int 4 pi r^2 f dr."""
    key = (shape, float(k), round(float(lmg), 9), float(w))
    if key in _QC: return _QC[key]
    R0 = Rvir(lmg); kR = k * R0; rmax = kR if shape == "sharp" else 6 * kR
    r = np.geomspace(1e-3, rmax, 8001); lr = np.log(r)
    f = base(r) if shape == "sharp" else base(r) * taper(r, kR, shape, w)
    g = 4 * np.pi * r ** 3 * f
    I = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(lr))]) + 4 * np.pi * r[0] ** 3 * f[0] / 3
    out = (lr, I / np.interp(math.log(R0), lr, I))
    if cache: _QC[key] = out
    return out
def gas_M(pr, lm, r_pc):
    """M_hot(< r) [Msun] for catalogue log M* lm (native h) at radii r_pc [pc]. FIXED is each harness's own term, written as the record writes it."""
    if pr["shape"] == "fixed": return 0.5 * 10 ** lm * np.minimum(1.0, (r_pc / 1e5) ** 3)
    if pr["shape"] == "zero": return np.zeros_like(np.asarray(r_pc, float))
    lmg = lm + pr["delta"]; lr, q = qprof(pr["shape"], pr["k"], lmg, pr.get("w", 0.3))
    return pr["A"] * NORM * 10 ** lmg * np.interp(np.log(np.asarray(r_pc, float) / 1e3), lr, q)
def gas_tot_ratio(pr, lm):
    """M_gas(< infinity) / 10^lm."""
    if pr["shape"] == "fixed": return 0.5
    if pr["shape"] == "zero": return 0.0
    lmg = lm + pr["delta"]; return pr["A"] * NORM * 10 ** pr["delta"] * float(qprof(pr["shape"], pr["k"], lmg, pr.get("w", 0.3), cache=False)[1][-1])   # no cache: keeps RSS under 1 GB
def gas_tot_vec(pr, lms):
    g = np.round(np.arange(4.0, 13.0001, 0.005), 3); v = np.array([gas_tot_ratio(pr, float(x)) for x in g])
    return np.interp(lms, g, v) * 10 ** lms

def profiles():
    """The frozen set. A values are read unrounded from GH11's JSON; P4/P5 from this lane's ksz fit; B3's offset is GH9's median."""
    G = json.load(open(os.path.join(RB, "GH11_ksz_two_halo_miscentring", "gh11.json"))); F = G["fits"]
    A = lambda key: float(F[key]["b0"]["A"]); e = float(G["Q1"]["primary"]["e"])
    d9 = -float(json.load(open(os.path.join(RB, "GH9_cigale_chen_mass_offset", "gh9_match.json")))["D_all"])
    kz = os.path.join(HERE, "cw6_ksz.json"); K = json.load(open(kz)) if os.path.exists(kz) else None
    sh = lambda pid, k, a, d=0.0, note="": dict(id=pid, shape="sharp", k=k, A=a, delta=d, note=note)
    L = [dict(id="FIXED", shape="fixed", note="the record's 0.5 M* min(1, (r/100 kpc)^3)"),
         sh("P1", 1.8, A("primary_1.8"), note="PRIMARY: sharp 1.8 R_vir, GH11 primary miscentring"),
         sh("P2", 1.0, A("primary_1.0"), note="sharp 1 R_vir, GH11 primary"), sh("P3", 3.0, A("primary_3.0"), note="sharp 3 R_vir, GH11 primary")]
    for pid, form in (("P4", "F1"), ("P5", "F2")):
        ok = bool(K and K.get("K2", {}).get("ok"))
        L.append(dict(id=pid, shape=form, k=1.8, A=float(K["fits"][pid]["A"]) if ok else None, delta=0.0, w=0.3, note=f"{form} taper at 1.8 R_vir, A fitted here on DR2"))
    L += [sh("P6", 1.0, 1.0, note="Zhang's X-ray value inside R_vir, no kSZ"),
          sh("B1", 1.8, A("nomis_1.8"), note="no miscentring (GH10 primary)"), sh("B2", 1.8, A("bracket_1.8"), note="extreme miscentring (0.5, 500 kpc)"),
          sh("B3", 1.8, A("primary_1.8"), d9, note=f"lens masses on CIGALE's scale, +{d9:.4f} dex"),
          sh("B4", 1.8, A("primary_1.8") + e, note="A + e"), sh("B5", 1.8, A("primary_1.8") - e, note="A - e")]
    return L
ZERO = dict(id="ZERO", shape="zero", note="MUTATE: gas term zeroed")
def run_list():
    if MUT: return [ZERO]
    return [p for p in profiles() if p["shape"] == "fixed" or p.get("A") is not None]

# ============================================================== mode ksz: K2 and the P4/P5 fits (GH10's head exec'd, GH11's model copied)
def mode_ksz():
    from scipy.stats import chi2 as CH
    P("CW6 ksz: GH11's model and b = 0 fit on GH10's DR2 differential bin; sharp K2 checks, F1/F2 at 1.8 R_vir. kappa = 1/2 FITTED; not theory closed.")
    g10 = os.path.join(RB, "GH10_dr2_ksz_published_points", "gh10.py"); N = {"__file__": g10, "__name__": "g"}; exec(open(g10).read().split("def load(lbl)")[0], N)
    Z, tau_tab, DA, FT, BF, FG, TCMB, ST, Rv = N["Z"], N["tau_tab"], N["DA"], N["FT"], N["BF"], N["FG"], N["TCMB"], N["ST"], N["Rv"]
    MSUN, KPC, MP, SIGT, MUE = N["MSUN"], N["KPC"], N["MP"], N["SIGT"], N["MUE"]; hterm = 2 * np.log10(.704 / N["H"]); DAREA = FG * FG
    assert abs(N["BETA"] - BETA) < 1e-12 and abs(N["RCK"] - RCK) < 1e-12 and abs(N["NORM"] - NORM) < 1e-12 and np.array_equal(N["ZTF"], ZTF)
    Af, Bf = [np.load(os.path.join(Z, f"Fig6_BGS_BRIGHT-20.2_logm{l}.npz")) for l in ("10.50", "11.00")]
    G10 = json.load(open(os.path.join(RB, "GH10_dr2_ksz_published_points", "gh10.json"))); w = G10["w"]; th = Af["th"]
    T = (Af["prof"] - (1 - w) * Bf["prof"]) / w; C = (Af["cov"] - (1 - w) ** 2 * Bf["cov"]) / w ** 2
    Dj = json.load(open(os.path.join(RB, "GH9_cigale_chen_mass_offset", "gh9_match.json")))["Dj"]; DG = lambda x: Dj[int(np.clip((x - 10.6) // .1, 0, 3))]
    h = np.load(os.path.join(Z, "Fig2_BGS_BRIGHT-20.2.npz")); bc, hh = h["binc"], h["hist"]; wd = float(np.median(np.diff(bc)))
    def Nn(a, b): return float(np.sum(hh * np.clip((np.minimum(bc + wd / 2, b) - np.maximum(bc - wd / 2, a)) / wd, 0, 1)))
    D = np.load(os.path.join(EXT, "gh6_work", "gh6_bgs.npz")); z, lm = D["z"], D["lm"]
    K1_, K2_ = np.fft.fftfreq(FT.shape[0], FG), np.fft.rfftfreq(FT.shape[0], FG); KK2 = K1_[:, None] ** 2 + K2_[None, :] ** 2
    o = np.argsort(FT.ravel()); fs_sort = FT.ravel()[o]
    def cap_from_field(cv, thv):
        cs = np.cumsum(cv.ravel()[o]) * DAREA; a = np.interp(thv, fs_sort, cs); b = np.interp(thv * math.sqrt(2), fs_sort, cs); return a - (b - a)
    def smear(sig_arcmin): return np.exp(-2 * math.pi ** 2 * sig_arcmin ** 2 * KK2)
    def massint(f, rmax, n=60001):
        rr = np.r_[0, np.geomspace(1e-2, rmax, n)]; return np.trapz(4 * np.pi * rr ** 2 * f(rr), rr)
    def tau_taper(l, k, form, wid):
        """GH10_smooth_gas_taper's tab(), 'Zhang's mass in R_vir' normalisation (M_T(<R_vir) = 1.84 M*), with GH10's constants and R_vir table."""
        R0 = float(Rv(l)); kR = k * R0; bf = lambda r: (1 + (r / RCK) ** 2) ** (-1.5 * BETA); f = lambda r: bf(r) * taper(r, kR, form, wid); Rm = 6 * kR
        s0 = massint(bf, R0); ne0 = NORM * 10 ** l * MSUN / (s0 * KPC ** 3) / (MUE * MP); fac = s0 / massint(f, R0)
        Rk = np.r_[0, np.geomspace(.1, Rm, 500)]; t = np.zeros_like(Rk)
        for i, R in enumerate(Rk[:-1]):
            ll = np.linspace(0, math.sqrt(Rm ** 2 - R * R), 4001); t[i] = 2 * np.trapz(f(np.sqrt(R * R + ll * ll)), ll) * KPC
        return Rk, SIGT * ne0 * fac * t
    TAB = {}
    def gas_field(zc, l, k, form, wid):
        key = (round(l, 4), k, form, wid)
        if key not in TAB: TAB[key] = tau_tab(l, k) if form == "sharp" else tau_taper(l, k, form, wid)
        Rk, t = TAB[key]; return np.interp(FT * DA(zc) * 1e3 * math.pi / 180 / 60, Rk, t, right=0)
    ed = np.linspace(10.5, 11, 6); CELLS = []
    for j in range(5):
        q = (lm >= ed[j]) & (lm < ed[j + 1]) & (z > .05) & (z < .5); c = (ed[j] + ed[j + 1]) / 2; CELLS.append((Nn(ed[j], ed[j + 1]), c + hterm - DG(c), np.quantile(z[q], [.125, .375, .625, .875])))
    del D, z, lm
    WT = sum(c[0] for c in CELLS)
    def model(k, fs, sig_kpc, form="sharp", wid=0.3):
        o1 = np.zeros(len(th))
        for wj, l, zq in CELLS:
            for zc in zq:
                F = np.fft.rfft2(gas_field(float(zc), float(l), k, form, wid)) * BF; S = 1.0
                if fs > 0: S = (1 - fs) + fs * smear(sig_kpc / (DA(float(zc)) * 1e3 * math.pi / 180 / 60))
                o1 += wj / 4 * cap_from_field(np.fft.irfft2(F * S, s=FT.shape), th)
        return TCMB * ST * o1 / WT
    def fit(m):
        CI = np.linalg.inv(C); s = 1 / math.sqrt(m @ CI @ m); a = float(m @ CI @ T) * s * s; c2 = float((T - a * m) @ CI @ (T - a * m))
        return dict(A=a, s=s, e=math.hypot(s, 0.1 * a), chi2=c2, p=float(CH.sf(c2, len(T) - 1)), n=len(T))
    G11 = json.load(open(os.path.join(RB, "GH11_ksz_two_halo_miscentring", "gh11.json")))["fits"]
    ms = model(1.8, .24, 300.); fs = fit(ms); mn = fit(model(1.8, 0., 300.)); mf2n = fit(model(1.8, .24, 300., "F2", 0.005))
    k2a = abs(fs["A"] - G11["primary_1.8"]["b0"]["A"]); k2b = abs(mn["A"] - G11["nomis_1.8"]["b0"]["A"]); k2c = abs(mf2n["A"] / fs["A"] - 1)
    ok = k2a <= 1e-3 and k2b <= 1e-3 and k2c <= 0.02
    P(f"K2a sharp(1.8), primary miscentring: A {fs['A']:.5f} vs GH11 {G11['primary_1.8']['b0']['A']:.5f} (|d| {k2a:.1e}, line 1e-3)")
    P(f"K2b sharp(1.8), no miscentring: A {mn['A']:.5f} vs GH11/GH10 {G11['nomis_1.8']['b0']['A']:.5f} (|d| {k2b:.1e}, line 1e-3)")
    P(f"K2c F2 width 0.005 vs sharp(1.8): A {mf2n['A']:.5f} vs {fs['A']:.5f} (rel {k2c:.2e}, line 0.02)")
    P(f"K2: {'PASS' if ok else 'FAIL'}  {tick()}")
    RES["K2"] = dict(ok=ok, sharp_primary=fs, sharp_nomis=mn, F2_narrow=mf2n, d=[k2a, k2b, k2c])
    RES["fits"] = {}
    for pid, form in (("P4", "F1"), ("P5", "F2")):
        f_ = fit(model(1.8, .24, 300., form, 0.3)); f_["form"] = form; f_["k"] = 1.8; RES["fits"][pid] = f_
        P(f"{pid} {form}(1.8), primary miscentring, b = 0: A {f_['A']:.4f} +- {f_['s']:.4f} (e with 10 % r {f_['e']:.4f}), chi2 {f_['chi2']:.2f}/{f_['n'] - 1}, p {f_['p']:.3f}  {tick()}")
    for k in (1.0, 3.0):
        f_ = fit(model(k, .24, 300.)); P(f"reported: sharp({k}) primary A {f_['A']:.4f} (GH11 {G11[f'primary_{k}']['b0']['A']:.4f})"); RES[f"sharp_{k}"] = f_
    save()

# ============================================================== mode gas: K3 and the profile table
def mode_gas():
    from scipy.integrate import quad
    P("CW6 gas: K3 checks and the measured profiles. kappa = 1/2 FITTED; not theory closed.")
    d1 = 0.0
    for shp, k in (("sharp", 1.0), ("sharp", 1.8), ("sharp", 3.0), ("F1", 1.8), ("F2", 1.8)):
        for l in (10.0, 10.75, 11.3):
            pr = dict(shape=shp, k=k, A=1.0, delta=0.0); v = float(gas_M(pr, l, np.array([Rvir(l) * 1e3]))[0]) / (NORM * 10 ** l); d1 = max(d1, abs(v - 1))
    d2 = 0.0
    for k in (1.0, 1.8, 3.0):
        for l in (10.0, 10.75, 11.3):
            R0 = Rvir(l); fq = lambda r: 4 * np.pi * r * r * float(base(r)); ref = quad(fq, 0, k * R0, limit=400, epsabs=0, epsrel=1e-12)[0] / quad(fq, 0, R0, limit=400, epsabs=0, epsrel=1e-12)[0]
            d2 = max(d2, abs(gas_tot_ratio(dict(shape="sharp", k=k, A=1.0, delta=0.0), l) / NORM / ref - 1))
    d3 = max(abs(gas_tot_ratio(dict(shape="F2", k=1.8, A=1.0, delta=0.0, w=0.005), l) / gas_tot_ratio(dict(shape="sharp", k=1.8, A=1.0, delta=0.0), l) - 1) for l in (10.0, 10.75, 11.3))
    ok = d1 <= 1e-4 and d2 <= 1e-4 and d3 <= 0.01
    P(f"K3a M_T(<R_vir) / 1.84 M* - 1, max {d1:.1e} (line 1e-4); K3b sharp total vs quadrature, max {d2:.1e} (line 1e-4); K3c F2 width 0.005 vs sharp(1.8) total {d3:.1e} (line 0.01) -> {'PASS' if ok else 'FAIL'}")
    RES["K3"] = dict(ok=ok, d=[d1, d2, d3])
    RS = np.array([50, 100, 200, 300, 500, 1000, 2000.]); tab = {}
    P("\nM_hot(<r)/M* at r [kpc] " + " ".join(f"{x:>6.0f}" for x in RS) + "   total  (R_vir kpc)")
    for pr in profiles():
        if pr["shape"] != "fixed" and pr.get("A") is None: P(f"{pr['id']}: NOT EVALUABLE (no A)"); continue
        tab[pr["id"]] = {}
        for l in (10.0, 10.5, 10.75, 11.0):
            v = gas_M(pr, l, RS * 1e3) / 10 ** l; tt = gas_tot_ratio(pr, l); tab[pr["id"]][str(l)] = dict(r_kpc=RS.tolist(), ratio=v.tolist(), total=tt, Rvir_kpc=Rvir(l + pr.get("delta", 0.0)))
            P(f"  {pr['id']:5s} lm {l:5.2f} " + " ".join(f"{x:6.2f}" for x in v) + f"  {tt:6.2f}  ({Rvir(l + pr.get('delta', 0.0)):.0f})" + (f"   A {pr['A']:.4f} {pr['note']}" if l == 10.0 and "A" in pr else ""))
    RES["table"] = tab; RES["profiles"] = profiles(); save()

# ============================================================== mode le1: H1, LE1's harness (copied, gas hook only)
def mode_le1():
    import importlib.util, types
    P(f"CW6 le1 (H1): A30 (G1), A30 no two-halo, A1, G3 on B21 Fig-3 through LE1's harness, gas swapped{' [MUTATE: gas zeroed]' if MUT else ''}. kappa = 1/2 FITTED; not theory closed.")
    CRG = os.path.join(RB, "CRG1_clean_room_regrade"); RQ3 = os.path.join(RB, "RQ3_acceptance_v2"); NP1 = os.path.join(RB, "NP1_nonparametric_rule"); cc = os.path.join(HERE, "cache_crg")
    p = os.path.join(CRG, "v1", "crg1_core.py"); s = open(p).read()
    for a, b in (('INP = os.path.join(HERE, "inputs")', f'INP = {os.path.join(CRG, "inputs")!r}'),
                 ('PART = os.path.join(HERE, os.environ.get("CRG1_PARTIALS", "partials"))', f'PART = {os.path.join(cc, "p")!r}'),
                 ('CACHE = os.path.join(HERE, os.environ.get("CRG1_CACHE", "cache"))', f'CACHE = {os.path.join(cc, "c")!r}')):
        assert s.count(a) == 1, a; s = s.replace(a, b)
    m = types.ModuleType("crg1_core"); m.__file__ = p; sys.modules["crg1_core"] = m; exec(compile(s, p, "exec"), m.__dict__); sys.path.insert(0, os.path.join(CRG, "v1"))
    sp = importlib.util.spec_from_file_location("rq3acc", os.path.join(RQ3, "acceptance.py")); ACC = importlib.util.module_from_spec(sp); sp.loader.exec_module(ACC)
    import crg1_lens as Le
    sp = importlib.util.spec_from_file_location("cand_law", os.path.join(RQ3, "candidates", "law.py")); law = importlib.util.module_from_spec(sp); sp.loader.exec_module(law)
    RGRID = Le.RGRID; SIk = 1e6 / 3.0857e16; REX = [.343, .442, .433, .429]
    L = Le.load(); st = Le.Stencil(L["Rn"] * 1e6); TH = Le.TwoHalo(Le.load()); T0_ = np.array([TH.esd2h(L["R"][b], REX[b]) * Le.FF for b in range(4)])
    IP = [j for j in range(15) if L["R"][0][j] <= 0.31]; P(f"  harness loaded {tick()}")
    def bary(lm, pr):
        lm70 = lm - 2 * math.log10(0.70 / Le.HN); lmc = lm + (-0.69 * lm70 + 6.63); Ms, Mcg = 10 ** lm, 10 ** lmc
        return Ms + Mcg + gas_M(pr, lm, RGRID), Ms + Mcg                 # Le.baryon with its hot term as the hook
    def table(foot, pr):
        Tb = np.zeros((len(Le.LMG), 60)); a0 = A0[foot]
        for i, lm in enumerate(Le.LMG):
            MB, _ = bary(float(lm), pr); gg = Le.Gpc * (MB - 10 ** float(lm)) / RGRID ** 2; gb = Le.Gpc * MB / RGRID ** 2
            v = ACC.call(law, gb=gb * SIk, gg=gg * SIk, gs=(gb - gg) * SIk, r=RGRID * 3.0857e16, a0=a0, sample="lens"); Tb[i] = st.dsig(MB * v / (gb * SIk), "linear")
        return Tb
    def grade(mo, twoh=True):
        T = T0_ if twoh else np.zeros_like(T0_); ch, b = Le.fit(L, mo, list(range(15)), T); dof = 60 - (4 if twoh else 0)
        return dict(chi2=float(ch), dof=dof, Z=float((ch - dof) / math.sqrt(2 * dof)), b=[float(x) for x in b])
    def amp(mo, bins=(0, 1, 2, 3)):
        idx = np.concatenate([15 * b + np.array(IP) for b in bins]); y = L["Yn"].ravel()[idx]; mm = mo[idx]; sg = np.sqrt(np.diag(L["Cn"]))[idx]; ok = (y > 0) & (mm > 0)
        d = np.log10(y[ok] / mm[ok]); w = (y[ok] * math.log(10) / sg[ok]) ** 2; mu = float((w * d).sum() / w.sum()); se = float(1 / math.sqrt(w.sum()))
        return dict(mean=mu, se=se, z=mu / se, n=int(ok.sum()), amp=10 ** mu)
    # G3: CX1's lensing line through NP1's cx_rows (as LE1's g3_rows / g3_z), with a baryon hook
    sys.path.insert(0, NP1); import np1_core as NC
    d = np.load(os.path.join(CRG, "inputs", "lensing", "lens_inventory.npz")); bins = np.digitize(d["logM"], [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
    MSB = [float(np.average(10 ** d["logM"][bins == b], weights=d["WLENS"][bins == b])) for b in range(4)]          # LE1's cx1_masses (Msun, h70)
    ROWS = {f: [q for q in NC.cx_rows(f) if q["line"] == "L"] for f in FEET}; C3 = sys.modules["cx1_rows"]; P(f"  G3 rows loaded ({len(ROWS['canonical'])} / {len(ROWS['alt'])}) {tick()}")
    def g3(foot, pr):
        R = ROWS[foot]; y = np.array([q["y"] for q in R]); ell = np.array([q["ell"] for q in R]); f = np.array([q["f"] for q in R]); lb = np.array([q["logB"] for q in R]); sd = np.array([q["sd"] for q in R])
        gb0 = y * NC.A0C; r = ell * NC.CL ** 2 / NC.A0C; gobs = 10 ** lb * NC.law(gb0, NC.FOOT[foot])
        if pr is None:                                                    # LE1's g3_z exactly (CX1's own baryons)
            gm = ACC.call(law, gb=gb0, gg=f * gb0, gs=(1 - f) * gb0, r=r, a0=NC.FOOT[foot], sample="lens")
        else:
            bi = np.array([int(q["name"][3:]) - 1 for q in R]); MB = np.zeros(len(R)); Mg = np.zeros(len(R)); rpc = r / C3.PC
            for b in range(4):
                s_ = bi == b
                if not s_.any(): continue
                Ms = MSB[b]
                if pr == "CX1hook": MB[s_] = Ms + 0.25 * Ms; Mg[s_] = 0.25 * Ms
                else:
                    l = math.log10(Ms); lm70 = l - 2 * math.log10(0.70 / Le.HN); Mcg = 10 ** (l + (-0.69 * lm70 + 6.63)); gas = gas_M(pr, l, rpc[s_])
                    MB[s_] = Ms + Mcg + gas; Mg[s_] = Mcg + gas
            gb = C3.G * MB * C3.MS / r ** 2; gg = C3.G * Mg * C3.MS / r ** 2
            gm = ACC.call(law, gb=gb, gg=gg, gs=gb - gg, r=r, a0=NC.FOOT[foot], sample="lens")
        dd = np.log10(gobs / gm); w = 1 / sd ** 2; mu = float((w * dd).sum() / w.sum()); se = float(1 / math.sqrt(w.sum())); return dict(mean=mu, se=se, z=mu / se, n=len(dd))
    LJ = json.load(open(os.path.join(RB, "LE1_lensing_estimator_audit", "le1_real.json")))
    RES["prof"] = {}; RES["K1"] = {}; RES["K4"] = {}
    for pr in run_list():
        RES["prof"][pr["id"]] = {}
        for foot in FEET:
            mo = Le.stack(L, table(foot, pr)); o = dict(A30=grade(mo), A30_no2h=grade(mo, False), A1=amp(mo), A1_bins=[amp(mo, (b,)) for b in range(4)], G3=g3(foot, pr))
            RES["prof"][pr["id"]][foot] = o
            P(f"[{pr['id']:5s} {foot:9s}] A30 chi2 {o['A30']['chi2']:7.2f} Z {o['A30']['Z']:+6.2f} | no 2h Z {o['A30_no2h']['Z']:+6.2f} | A1 {o['A1']['mean']:+.4f} +- {o['A1']['se']:.4f} (amp {o['A1']['amp']:.3f}, z {o['A1']['z']:+.2f}) "
              f"bins " + " ".join(f"{x['mean']:+.3f}" for x in o["A1_bins"]) + f" | G3 (G1 inventory) z {o['G3']['z']:+.2f} (mean {o['G3']['mean']:+.4f})  {tick()}")
            if pr["id"] == "FIXED":
                ref = LJ["G1"]["law"][foot]; g3ref = LJ["G3"][foot]["law"]["base"]; k1 = g3(foot, None); k4 = g3(foot, "CX1hook")
                dv = dict(A30_Z=abs(o["A30"]["Z"] - ref["S0 base"]["Z"]), A30_chi2=abs(o["A30"]["chi2"] - ref["S0 base"]["chi2"]), no2h_Z=abs(o["A30_no2h"]["Z"] - ref["S2 no two-halo"]["Z"]),
                          A1_mean=abs(o["A1"]["mean"] - ref["A1 G1 model, G3 statistic"]["mean"]), A1_z=abs(o["A1"]["z"] - ref["A1 G1 model, G3 statistic"]["z"]), G3_z=abs(k1["z"] - g3ref["z"]))
                RES["K1"][foot] = dict(ok=max(dv.values()) <= 1e-9, d=dv, G3_CX1=k1); RES["K4"][foot] = dict(ok=abs(k4["z"] - k1["z"]) <= 1e-9, z_hook=k4["z"], z=k1["z"], d=abs(k4["z"] - k1["z"]))
                P(f"   K1 [{foot}] vs le1_real.json: max |d| {max(dv.values()):.1e} -> {'PASS' if RES['K1'][foot]['ok'] else 'FAIL'}  (G3 CX1 baryons z {k1['z']:+.4f}, record {g3ref['z']:+.4f})")
                P(f"   K4 [{foot}] G3 hook fed CX1's baryons: z {k4['z']:+.6f} vs {k1['z']:+.6f} (|d| {RES['K4'][foot]['d']:.1e}) -> {'PASS' if RES['K4'][foot]['ok'] else 'FAIL'}")
    save()

# ============================================================== mode b21c: H2, S2's forward model on B21 Fig-8 colour bins (S2's text exec'd up to its K2 block, as BL1)
def mode_b21c():
    P(f"CW6 b21c (H2): B21 Fig-8 colour bins, S2's L4 row (v3 at y_e = 0), window A, gas swapped{' [MUTATE: gas zeroed]' if MUT else ''}. kappa = 1/2 FITTED; not theory closed.")
    S2 = os.path.join(RB, "S2_v3_lowg_lensing", "s2_v3_lowg_lensing.py"); argv0 = sys.argv; sys.argv = [S2]
    Tx = open(S2).read(); CUT = "# ---- K2: forward model of an isolated point mass"; assert Tx.count(CUT) == 1; H = Tx[:Tx.index(CUT)]
    a = "    finish()\n"; assert H.count(a) == 1; H = H.replace(a, '    raise SystemExit("S2 K0a failed: the record is not reproduced")\n')   # S2 would write its own outputs; it must not here
    N = {"__file__": S2, "__name__": "s2_ro"}; exec(compile(H, S2, "exec"), N); sys.argv = argv0
    AQ, RG, LMG, LRT, a0u, Gpc = (N[k] for k in ("AQ", "RGRID_PC", "LMG", "LRT", "a0u", "Gpc")); P(f"  S2 head done {tick()}")
    STATE = {}; TAB = {}
    def table(foot, h, yk, fhot, dcold, dMs):
        """S2's table with meff's hot term as the hook (y_e = 0 only, as the L4 row)."""
        pr = STATE["pr"]; assert yk == "zero" and fhot == 0.5; key = (foot, h, dcold, round(dMs, 8), pr["id"])
        if key in TAB: return TAB[key]
        tab = np.empty((len(LMG), len(LRT))); a0 = a0u(foot)
        for gi, lm in enumerate(LMG):
            lm70 = lm - 2 * math.log10(0.70 / h); Mcold = 10 ** (lm + (-0.69 * lm70 + 6.63) + dcold); Mpt = 10 ** (lm + dMs) + Mcold
            Mb = Mpt + gas_M(pr, lm, RG)                                   # hot gas tied to the catalogue M* (S2's convention)
            Miso = Mb * AQ.nu_simple(Gpc * Mb / RG ** 2 / a0); tab[gi] = np.log(AQ.delta_sigma(np.exp(LRT) * 1e6, RG, Miso, "linear"))
        TAB[key] = tab; return tab
    N["table"] = table; CFG = dict(N["CENTRAL"], ye="zero")
    S2J = json.load(open(os.path.join(RB, "S2_v3_lowg_lensing", "s2_v3_lowg_lensing_results.json")))["ladder"]; L4 = "L4 + hot CGM 0.5 M* (v3 at y_e = 0)"
    RES["prof"] = {}; RES["K1"] = {}
    for pr in run_list():
        STATE["pr"] = pr; RES["prof"][pr["id"]] = {}
        for foot in FEET:
            o = {k: N["cell"](foot, k, CFG) for k in ("blue", "red", "all")}; RES["prof"][pr["id"]][foot] = o
            P(f"[{pr['id']:5s} {foot:9s}] " + "  ".join(f"{k} A {o[k]['A']:.4f} +- {o[k]['sA']:.4f} ({o[k]['cls']}, z {(o[k]['A'] - 1) / o[k]['sA']:+.2f}; chi2_15 {o[k]['chi2_15_A1']:.1f})" for k in ("blue", "red", "all")) + f"  {tick()}")
            if pr["id"] == "FIXED":
                dv = max(max(abs(o[k]["A"] - S2J[foot][L4][k]["A"]), abs(o[k]["sA"] - S2J[foot][L4][k]["sA"])) for k in ("blue", "red", "all"))
                RES["K1"][foot] = dict(ok=dv <= 1e-9, d=dv); P(f"   K1 [{foot}] vs S2's L4 row: max |d| {dv:.1e} -> {'PASS' if dv <= 1e-9 else 'FAIL'}")
    save()

# ============================================================== mode si2: H3, SI2's clean lenses (SI1's head exec'd as SI2 does: P2 phase B)
def mode_si2():
    P(f"CW6 si2 (H3): SI2's spectroscopically isolated lenses S1, S3 by colour, law at R0, gas swapped{' [MUTATE: gas zeroed]' if MUT else ''}. kappa = 1/2 FITTED; not theory closed.")
    WORK = os.path.abspath(ARGS[1]); assert os.path.exists(os.path.join(WORK, "p2_meas_d8787042a095deef.npz")), "P2's measurement cache is not in the work dir"
    SI1F = os.path.join(RB, "SI1_spec_isolated_route_e", "si1_grade.py"); argv0 = sys.argv; sys.argv = [SI1F, os.path.join(WORK, "phase_B_reads_no_source_cache"), WORK]
    src = open(SI1F).read(); cut = 'RES = dict(criteria="ed3c0f8bb1"'; assert src.count(cut) == 1
    G = {"__file__": SI1F, "__name__": "si1_head"}; exec(compile(src[:src.index(cut)], "si1_head", "exec"), G); sys.argv = argv0; N = G["N"]
    P(f"  SI1 head (P2 phase B) done {tick()}")
    _lh = N["read_fits_cols"](os.path.join(N["DKB"], "KiDS_DR4_brightsample_LePhare.fits"), ["MAG_ABS_u", "MAG_ABS_r"], rowmask=N["inb"]); _ur = _lh["MAG_ABS_u"].astype("f8") - _lh["MAG_ABS_r"].astype("f8"); del _lh
    valid, kk, NG = N["valid"], N["kk"], N["NG"]; UR_g = np.full(NG, np.nan); UR_g[valid] = _ur[kk[valid]]; red_g = valid & (UR_g > 2.0); blue_g = valid & ~(UR_g > 2.0)   # SI2's split
    idxS1 = G["idxS1"]; RL = red_g[idxS1]; BL = blue_g[idxS1]; NLn = len(idxS1); inS3 = N["inS3"]; SETS = G["SETS"]; SETL = SETS["L"]
    AQ, RG, LMG, EDGES, H0N, bin_avg, TOWN, OATS, town_per_lens, tnbr, stack, amps, compare = (G[k] if k in G else N[k] for k in ("AQ", "RG", "LMG", "EDGES", "H0N", "bin_avg", "TOWN", "OATS", "town_per_lens", "tnbr", "stack", "amps", "compare"))
    lMa, z_g, LMB_T, lMs_nat, lM70 = N["lMa"], G["z_g"], G["LMB_T"], G["lMs_nat"], G["lM70"]; TIX0, MBN0 = N["tix"].copy(), N["MBN_g"].copy()
    lMs_g = lMs_nat(lMa, z_g); cold_g = 10 ** (-0.69 * lMa + 6.63)
    def nbr(pr):
        ms = 10 ** lMs_g
        lmb = np.log10(ms * (1 + cold_g + 0.5)) if pr["shape"] == "fixed" else np.log10(ms * (1 + cold_g) + gas_tot_vec(pr, lMs_g))   # P2's lMb_nat for FIXED
        return np.clip(np.round((lmb - LMB_T[0]) / 0.05).astype(int), 0, len(LMB_T) - 1), 10 ** lmb
    def law_table(foot, pr):
        """P2's town_table at y_e = 0 with meff_lens's hot term as the hook; two identical nodes, as SI1/SI2."""
        tab = np.empty((len(LMG), 15)); Rpe = EDGES * 1e6; a0 = A0[foot] * 3.0857e16 / 1e6; Gpc = 4.30091e-3
        for gi, lm in enumerate(LMG):
            lm70 = lm - 2 * np.log10(0.70 / H0N); lmc = lm + (-0.69 * lm70 + 6.63); Mpt = 10 ** lm + 10 ** lmc
            Mb = Mpt + gas_M(pr, lm, RG); M = Mb * AQ.nu_simple(Gpc * Mb / RG ** 2 / a0); tab[gi] = bin_avg(Rpe, lambda R: AQ.delta_sigma(R, RG, M, "linear"))
        return np.stack([tab, tab], 1)
    def st(mod, sample, sub):                                              # SI2's st()
        Lc = SETL[inS3] if sample == "S3" else SETL; sel = {"all": np.ones(NLn, bool), "red": RL, "blue": BL}[sub][Lc]; Lc = Lc[sel]; Ic = SETS["I3"] if sample == "S3" else SETS["I1"]
        return stack([(Lc, +1, mod), (Ic, -1, mod)])
    def rows(mod):
        o = {}
        for sm in ("S3", "S1"):
            o[sm] = {}
            for sub in ("all", "red", "blue"):
                sL = st(mod, sm, sub); c = compare(sL, sL); a = amps(sL); o[sm][sub] = dict(a, chi2_L=c["chi2_L"], pL=c["pL"], p=c["p"])
        return o
    SJ = json.load(open(os.path.join(RB, "SI2_spec_isolated_colour", "si2_results.json")))["foot"]
    RES["prof"] = {}; RES["prof_own_only"] = {}; RES["K1"] = {}
    for pr in run_list():
        RES["prof"][pr["id"]] = {}; RES["prof_own_only"][pr["id"]] = {}
        for foot in FEET:
            key = "cw6|" + pr["id"]; OATS[key] = {}; TOWN[(foot, key)] = law_table(foot, pr)
            ow = town_per_lens(foot, key, lM70[idxS1], z_g[idxS1], np.zeros(NLn))
            tix, mbn = nbr(pr); N["tix"], N["MBN_g"] = tix, mbn; TNp = tnbr(foot, node=0); N["tix"], N["MBN_g"] = TIX0, MBN0
            mod = TNp.copy(); mod[:NLn] += ow; mod_o = N["TN"][(foot, "a")].copy(); mod_o[:NLn] += ow
            o = rows(mod); RES["prof"][pr["id"]][foot] = o; RES["prof_own_only"][pr["id"]][foot] = rows(mod_o)
            for sm in ("S3", "S1"):
                P(f"[{pr['id']:5s} {foot:9s} {sm}] " + "  ".join(f"{sub} A_in {o[sm][sub]['A_in']:.3f} +- {o[sm][sub]['sA_in']:.3f} (z {(o[sm][sub]['A_in'] - 1) / o[sm][sub]['sA_in']:+.2f}), A_O1 {o[sm][sub]['A_O1']:.2f}, chi2 {o[sm][sub]['chi2_L']:.1f}" for sub in ("all", "red", "blue")) + f"  {tick()}")
            if pr["id"] == "FIXED":
                own0 = TOWN[(foot, "central")][:, 0, :]; d_own = float(np.max(np.abs(TOWN[(foot, key)][:, 0, :] / own0 - 1))); d_tix = int(np.sum(tix != TIX0)); d_tn = float(np.max(np.abs(TNp - N["TN"][(foot, "a")])))
                dv = 0.0
                for sm in ("S3", "S1"):
                    for sub, g in (("all", "all_R0"), ("red", "red_R0"), ("blue", "blue_R0")):
                        r_ = SJ[foot][sm][g]
                        for kq in ("A_in", "sA_in", "A_O1", "sA_O1", "A_O2", "sA_O2"): dv = max(dv, abs(o[sm][sub][kq] - r_["amps_L"][kq]))
                        dv = max(dv, abs(o[sm][sub]["chi2_L"] - r_["all"]["chi2_L"]), abs(o[sm][sub]["pL"] - r_["all"]["pL"]))
                RES["K1"][foot] = dict(ok=dv <= 1e-9, d=dv, own_table_rel=d_own, nbr_tix_changed=d_tix, TN_absdiff=d_tn)
                P(f"   K1 [{foot}] vs si2_results.json (R0, all/red/blue, S1/S3): max |d| {dv:.1e}; own table vs P2's {d_own:.1e}; neighbour bins changed {d_tix}; T_nbr |d| {d_tn:.1e} -> {'PASS' if dv <= 1e-9 else 'FAIL'}")
    save()

# ============================================================== mode verdict: frozen labels
SAMPLES = ("B21c", "S1", "S3")
def colour_amps(h2, h3, pid, foot):
    o = {"B21c": {c: (h2[pid][foot][c]["A"], h2[pid][foot][c]["sA"]) for c in ("red", "blue")}}
    for sm in ("S1", "S3"): o[sm] = {c: (h3[pid][foot][sm][c]["A_in"], h3[pid][foot][sm][c]["sA_in"]) for c in ("red", "blue")}
    return o
def label(cur, fix):
    over = []
    for s in SAMPLES:
        for c in ("red", "blue"):
            A, sg = cur[s][c]; Af, sf = fix[s][c]
            if (A - 1) / sg < -2 and (A - Af) / sf <= -1: over.append((s, c))
    if over:
        cs = [c for c in ("red", "blue") if any(c == x[1] for x in over)]; return "OVERSHOOTS (" + " and ".join(cs) + ")", over
    if all(abs((cur[s][c][0] - 1) / cur[s][c][1]) <= 2 for s in SAMPLES for c in ("red", "blue")): return "GAP CLOSED", []
    m = (cur["B21c"]["red"][0] - fix["B21c"]["red"][0]) / fix["B21c"]["red"][1]
    return ("GAP NARROWED" if m <= -1 else "GAP WIDENED" if m >= 1 else "GAP UNCHANGED"), []
def a30flag(Zp, Zf):
    if abs(Zp) <= 2: return "PASSES"
    return "IMPROVES" if Zp - Zf <= -1 else "WORSENS" if Zp - Zf >= 1 else "SAME"
def mode_verdict():
    J = lambda n, s="": json.load(open(os.path.join(HERE, f"cw6_{n}{s}.json")))
    H1, H2, H3 = J("le1"), J("b21c"), J("si2"); KZ, GS = J("ksz"), J("gas"); M1, M2, M3 = J("le1", "_MUTATE"), J("b21c", "_MUTATE"), J("si2", "_MUTATE")
    P(f"CW6 verdict{' [MUTATE outputs, printed, not graded]' if MUT else ''}: frozen precedence. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
    k1 = {f: bool(H1["K1"][f]["ok"] and H2["K1"][f]["ok"] and H3["K1"][f]["ok"]) for f in FEET}; k3 = bool(GS["K3"]["ok"]); k2 = bool(KZ["K2"]["ok"]); k4 = all(H1["K4"][f]["ok"] for f in FEET)
    bite = {}
    for f in FEET:
        z1 = M1["prof"]["ZERO"][f]; z2 = M2["prof"]["ZERO"][f]["all"]["A"]; z3 = {sm: M3["prof"]["ZERO"][f][sm]["all"]["A_in"] for sm in ("S1", "S3")}
        cond = [z1["A1"]["amp"] >= max(H1["prof"][q][f]["A1"]["amp"] for q in ("FIXED", "P1")) + 0.01, abs(z1["A30"]["chi2"] - H1["prof"]["P1"][f]["A30"]["chi2"]) >= 5,
                z2 >= max(H2["prof"][q][f]["all"]["A"] for q in ("FIXED", "P1")) + 0.01] + [z3[sm] >= max(H3["prof"][q][f][sm]["all"]["A_in"] for q in ("FIXED", "P1")) + 0.01 for sm in ("S1", "S3")]
        bite[f] = dict(ok=all(cond), cond=cond, A1_amp=z1["A1"]["amp"], A30_chi2=z1["A30"]["chi2"], b21c_all=z2, si2_all=z3)
    bs = ", ".join(f"{f}: {bite[f]['ok']} {bite[f]['cond']}" for f in FEET)
    P(f"K1 (H1, H2, H3) {k1}; K2 {k2}; K3 {k3}; K4 {k4}; MUTATE bites {bs}")
    RES.update(K1=k1, K2=k2, K3=k3, K4=k4, MUTATE_bites=bite)
    pids = ["ZERO"] if MUT else [p for p in H2["prof"] if p != "FIXED"]
    src2 = M2["prof"] if MUT else H2["prof"]; src3 = M3["prof"] if MUT else H3["prof"]; src1 = M1["prof"] if MUT else H1["prof"]
    lab = {}
    for f in FEET:
        fix = colour_amps(H2["prof"], H3["prof"], "FIXED", f); lab[f] = {}
        for pid in pids:
            cur = colour_amps(src2, src3, pid, f); l, over = label(cur, fix)
            ne = (not k1[f]) or (not k3) or (not all(bite[x]["ok"] for x in FEET)) or (pid in ("P4", "P5") and not k2)
            zt = {s: {c: dict(A=cur[s][c][0], s=cur[s][c][1], z=(cur[s][c][0] - 1) / cur[s][c][1], m=(cur[s][c][0] - fix[s][c][0]) / fix[s][c][1], A_fixed=fix[s][c][0], s_fixed=fix[s][c][1]) for c in ("red", "blue")} for s in SAMPLES}
            a1 = src1[pid][f]; a1f = H1["prof"]["FIXED"][f]
            lab[f][pid] = dict(label="NOT EVALUABLE" if ne else l, raw=l, overshoots=over, amps=zt, A30_Z=a1["A30"]["Z"], A30_Z_fixed=a1f["A30"]["Z"], A30_flag=a30flag(a1["A30"]["Z"], a1f["A30"]["Z"]),
                               A1=a1["A1"], A1_fixed=a1f["A1"], G3=a1["G3"], G3_fixed=a1f["G3"], G3_CX1=H1["K1"][f]["G3_CX1"])
    RES["labels"] = lab
    for f in FEET:
        P(f"\n===== [{f}] amplitudes, data/model (z = (A - 1)/sigma; m = move in fixed-term sigma)")
        P(f"  {'sample':5s} {'colour':6s} {'FIXED':>16s} " + " ".join(f"{pid:>22s}" for pid in pids))
        for s in SAMPLES:
            for c in ("red", "blue"):
                zf = lab[f][pids[0]]["amps"][s][c]
                P(f"  {s:5s} {c:6s} {zf['A_fixed']:6.3f}+-{zf['s_fixed']:.3f} ({(zf['A_fixed'] - 1) / zf['s_fixed']:+.1f}) " + " ".join(f"{lab[f][p]['amps'][s][c]['A']:6.3f} z{lab[f][p]['amps'][s][c]['z']:+5.1f} m{lab[f][p]['amps'][s][c]['m']:+5.1f}" for p in pids))
        for p in pids:
            q = lab[f][p]
            P(f"  {p:5s} {q['label']:28s} A30 Z {q['A30_Z_fixed']:+.2f} -> {q['A30_Z']:+.2f} ({q['A30_flag']}); A1 {q['A1_fixed']['mean']:+.4f} -> {q['A1']['mean']:+.4f} dex (z {q['A1']['z']:+.2f}); "
              f"G3 z {q['G3_fixed']['z']:+.2f} -> {q['G3']['z']:+.2f} (CX1 baryons {q['G3_CX1']['z']:+.2f})" + (f"; over {q['overshoots']}" if q["overshoots"] else ""))
    if not MUT:
        fin = {}
        for f in FEET:
            p1 = lab[f]["P1"]["label"]; dep = {p: lab[f][p]["label"] for p in ("P2", "P3", "P4", "P5", "P6") if p in lab[f] and lab[f][p]["label"] != p1}
            fin[f] = dict(label=p1, profile_dependent=dep, A30_flag=lab[f]["P1"]["A30_flag"], brackets={p: lab[f][p]["label"] for p in ("B1", "B2", "B3", "B4", "B5") if p in lab[f]})
            P(f"\nLANE LABEL [{f}]: {p1}" + (f" (PROFILE-DEPENDENT: {dep})" if dep else "") + f"; A30 flag {fin[f]['A30_flag']}; brackets {fin[f]['brackets']}")
        RES["lane"] = fin
    save()

if __name__ == "__main__":
    {"ksz": mode_ksz, "gas": mode_gas, "le1": mode_le1, "b21c": mode_b21c, "si2": mode_si2, "verdict": mode_verdict}[MODE]()
