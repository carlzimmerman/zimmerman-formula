#!/usr/bin/env python3
"""SS1 local gates (FROZEN_CRITERIA.md b5adc7a90b + AMENDMENT_A1 9aeeb48503): the self-shielded late conversion graded on
gate 1 KiDS, 2 groups, 3 X-COP (+TR1 fraction), 4 Coma UDGs (reported, UA1), 5 SPARC (+F2 allowance, AGC 114905 / Malin 1),
10 Cassini; known answers KA1, KA2 (ss1_core), KA3 (component -> 0 replays the record's law-only numbers).
    python3 ss1.py local                      -> parts/local.json
    SS1_MUTATE=M1|M2|M3|M4 python3 ss1.py local -> parts/local_M1.json ...
Gate construction is WD1's (closure_2026_11_08/WD1_cvwd_condensate/wd1.py run_local, own transcription) with the component
replaced by SS1's retained profile; loaders read-only through PJ1 (imported from a read-only copy of origin/main's lane dir,
SS1_PJ1_DIR), QX8, GB1 / QX5, S1, UD1 / UD2. One thread, < 1 GB, SIGTERM checkpoint.
TEST lane, quarantined; adopts nothing. kappa = 1/2 FITTED; not theory closed; footings never pooled."""
import os, sys, json, math, io, contextlib, time, signal, resource, csv
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import ss1_core as C
PJ1DIR = os.environ.get("SS1_PJ1_DIR", os.path.join(REPO, "closure_2026_11_08", "PJ1_potential_gated_jeans"))
sys.path.insert(0, PJ1DIR); _argv = sys.argv; sys.argv = [os.path.join(PJ1DIR, "pj1.py")]
with contextlib.redirect_stdout(io.StringIO()):
    import pj1 as J                     # read-only: constants, law, loaders; nothing of PJ1's is run or written
sys.argv = _argv
CL6, CL7, RB = J.CL6, J.CL7, J.RB
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOTS = J.FOOTS; A0H = J.A0H; RF = J.RF; glaw = J.glaw
G_SI, MS, KPC, MPC, PC = J.G_SI, J.MS, J.KPC, J.MPC, J.PC
G_KPC = 4.3009172706e-6
MUT = C.MUT; SUFFIX = ("_" + MUT if MUT else ""); NOTE = C.NOTE
WHICH = sys.argv[1] if len(sys.argv) > 1 else ""
Q15 = json.load(open(os.path.join(CL6, "QX15_cmb_primary_likelihood", "qx15.json")))
KD1 = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
COSMO = {f: dict(h=float(Q15["footings"][f]["main"]["h"]), ob=Q15["footings"][f]["main"]["theta"]["omega_b"], R=RF[f]) for f in FOOTS}
for f in FOOTS: COSMO[f]["Om"] = COSMO[f]["ob"] * (1 + COSMO[f]["R"]) / COSMO[f]["h"] ** 2
F2_ALLOW = {f: KD1["footings"][f]["uniform_f_diag"]["SPARC_f_max"] for f in FOOTS}
KX1_LINE = {"canonical": [0.047, 0.221, 0.197, 0.236], "alt": [0.007, 0.181, 0.158, 0.196]}   # KX1 RESULT.md per-bin line (E_b + 2 sigma_tot), 100-300 kpc
TR1_D_CAN = [0.71, 0.66, 0.58, 0.46, 0.32]                                                     # TR1 RESULT: M_X / M_dyn by r/R500 bin, reading D canonical
RES = {}
def P(s=""): print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return str(o)
    return o
def dump(name, obj): json.dump(clean(obj), open(os.path.join(PARTS, name), "w"), indent=1)
def on_term(sig, frm):
    dump(f"{WHICH}{SUFFIX}_partial.json", RES); P("SIGTERM: partial checkpoint written"); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)

# ================================================================== the component per system
GALAXY_SCALE = {"kids", "sparc", "udg", "mw", "lsb"}
class Comp:
    """builds pre-conversion halos for a batch of systems (one footing, one bracket setting), peels them together, and serves
    enclosed retained masses. zero=True: the component is absent (KA3)."""
    def __init__(self, f, kind="SIS", am=False, zero=False):
        self.f, self.kind, self.am, self.zero = f, kind, am, zero; c = COSMO[f]; self.c = c; self.cache = {}
    def halo_for(self, Mb, cls):
        c = self.c
        if self.am and cls in GALAXY_SCALE:
            M200 = C.moster_halo(Mb, C.Z_DEC); Mchi = M200 * c["R"] / (1 + c["R"])
            return C.halo(Mb, c["R"], c["h"], c["Om"], kind=self.kind, M200=M200, Mchi=Mchi)
        return C.halo(Mb, c["R"], c["h"], c["Om"], kind=self.kind)
    def build(self, keys):
        """keys: list of (Mb, cls) or (Mb, cls, host_key, d_kpc) for members. Peels hosts first, then members."""
        new = [k for k in dict.fromkeys(keys) if k not in self.cache]
        if self.zero or not new: return
        plain = [k for k in new if len(k) == 2]; mem = [k for k in new if len(k) == 4]
        if plain:
            Hs = [self.halo_for(k[0], k[1]) for k in plain]
            rec = None
            if any(k[1] == "host" for k in plain): rec = [i * C.DTAU for i in range(int(round(C.TAU_TOT / C.DTAU)) + 1)]
            Pk = C.peel(Hs, record_taus=rec)
            for i, k in enumerate(plain):
                self.cache[k] = dict(H=Hs[i], P=Pk, i=i, fn=C.enclosed_fn(Pk, i, "M"), fn0=C.enclosed_fn(Pk, i, "M0"))
        if mem:
            Hs = []; hs = []
            for k in mem:
                Hs.append(self.halo_for(k[0], k[1])); host = self.cache[k[2]]; d = k[3]; Ph, ih = host["P"], host["i"]
                taus = np.array(sorted(Ph["snaps"])); sig = np.array([C.sigma_profile_fn(Ph, ih, Ph["snaps"][t][ih])(d) for t in taus])
                hs.append(lambda tau, taus=taus, sig=sig: float(np.interp(tau, taus, sig)))
            Pm = C.peel(Hs, host_sigma=hs)
            for i, k in enumerate(mem):
                self.cache[k] = dict(H=Hs[i], P=Pm, i=i, fn=C.enclosed_fn(Pm, i, "M"), fn0=C.enclosed_fn(Pm, i, "M0"))
    def M(self, r_kpc, key):
        if self.zero: return np.zeros_like(np.asarray(r_kpc, float))
        if key not in self.cache: self.build([key])
        return self.cache[key]["fn"](r_kpc)
    def info(self, key):
        if self.zero: return {}
        e = self.cache[key]; H, Pk, i = e["H"], e["P"], e["i"]
        return dict(M_b=H["M_b"], M200=H["M200"], Mchi0=H["Mchi0"], R200=H["R200"], R500=H["R500"], c200=H["c200"], x0_system=C.x0_system(H),
                    ret_total=C.retention(Pk, i), ret_R500=C.retention(Pk, i, H["R500"]), ret_025R500=C.retention(Pk, i, 0.25 * H["R500"]),
                    reduced_reading=C.reduced(C.x0_system(H)) if not C.GATE_OFF else math.exp(-C.TAU_TOT), frozen_da_bracket=C.frozen_da(C.x0_system(H)),
                    retained_over_Mb=float(Pk["M"][i].sum()) / H["M_b"])
    def rho(self, r_kpc, key):
        if self.zero: return 0.0
        e = self.cache[key]; E = e["P"]["E"][e["i"]]; M = e["P"]["M"][e["i"]]; V = 4 / 3 * math.pi * (E[1:] ** 3 - E[:-1] ** 3)
        j = int(np.searchsorted(E, r_kpc) - 1); return float(M[j] / V[j])

# ================================================================== local gates
def run_local():
    from astropy.io import fits
    sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field")); a_ = sys.argv; sys.argv = [a_[0]]
    with contextlib.redirect_stdout(io.StringIO()):
        import qx8 as Q8
    sys.argv = a_
    GALS = Q8.load_sparc(); Q8J = json.load(open(os.path.join(CL6, "QX8_sparc_exact_field", "qx8.json")))
    GB = J.load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
    GBJ = json.load(open(os.path.join(CL6, "GB1_all_gates_battery", "gb1.json")))
    XC, GR = GB["XC"], GB["GR"]; LE = GB["NS"]["lensing"]()
    R500X = {}
    for name in sorted({z["name"] for z in XC}):
        with fits.open(os.path.join(GB["DATA"], "xcop", name, f"{name}_fgas_profile.fits")) as h: R500X[name] = float(h[1].header["R500"])
    lU, lN = np.log(Q8.UPS), np.log(Q8.NODES)
    PRE = {f: [np.array([np.interp(lU, lN, T[:, j]) for j in range(T.shape[1])]) for T in
               (np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False)["T"] for i in range(len(GALS)))] for f in FOOTS}
    def fit_stats(q, lgp):
        OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); i = int(np.argmin(wr2 / np.maximum(ws, 1e-300)))
        return wr2[i], wr[i], ws[i], i
    def pooled(rows, sel=None):
        idx = list(range(len(rows))) if sel is None else list(sel)
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx)
        return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws), U_median=float(np.median([Q8.UPS[rows[i][3]] for i in idx])), n=len(idx))
    def sparc_eval(f, bf_list):
        a0 = A0H[f]; rows = []
        for i, (q, Tf) in enumerate(zip(GALS, PRE[f])):
            g = q["GB"] * bf_list[i][:, None]; rows.append(fit_stats(q, np.log10(np.maximum(glaw(g, a0), 1e-300)) + Tf))
        return rows
    SPROF = []
    for q in GALS:
        R = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mb = np.maximum.accumulate(np.clip(VB2 * R / G_KPC, 0, None)); Mb = np.maximum(Mb, 1e3)
        SPROF.append(dict(R=R, Mb=Mb, Mtot=float(Mb[-1]), Vflat=q["meta"]["Vflat"], Mstar_proxy=float(Mb[-1])))
    massive = [i for i, s in enumerate(SPROF) if s["Vflat"] >= 250.0]
    UD1 = json.load(open(os.path.join(RB, "UD1_agc114905_udg_rotation", "ud1.json"))); UD2 = json.load(open(os.path.join(RB, "UD2_malin1_giant_lsb", "ud2.json")))
    CONV = 1e6 / 3.0857e19
    agc = dict(R=np.array(UD1["data2024"]["R"]), V=np.array(UD1["data2024"]["V"]), E=np.array(UD1["data2024"]["E"]), vb2=np.array(UD1["baryons"]["Vgas"]) ** 2 + np.array(UD1["baryons"]["Vstar"]) ** 2)
    mal = dict(R=np.array([12.5, 37.5, 62.5, 87.5]), V=np.array([236.9, 216.2, 197.4, 214.1]), E=np.array([9.4, 2.6, 4.7, 11.8]),
               vb2=np.array(UD2["decoHL"]["gas"]) ** 2 + np.array(UD2["decoHL"]["lsb"]) ** 2 + np.array(UD2["decoHL"]["hsb"]) ** 2)
    for d in (agc, mal): d["Mb"] = np.maximum.accumulate(d["vb2"] * d["R"] / G_KPC)
    def rc_chi2(d, a0, fK=None):
        gN = d["vb2"] / d["R"] * CONV * (1.0 if fK is None else 1 + fK); V = np.sqrt(np.maximum(glaw(gN, a0) / CONV * d["R"], 0.0)); return float(np.sum(((d["V"] - V) / d["E"]) ** 2))
    S1D = os.path.join(RB, "S1_v3_hosted_small"); UROWS = list(csv.DictReader(open(os.path.join(S1D, "s1_coma_per_galaxy.csv"))))
    UD = {f: [r for r in UROWS if r["footing"] == f] for f in FOOTS}
    KEV, MP = 1.602176634e-16, 1.67262e-27; BETA = dict(kT=8.6, rc=276.0, beta=0.71, mu=0.6); CB = 3 * BETA["beta"] * BETA["kT"] * KEV / (BETA["mu"] * MP); KPC_C = 3.0857e19
    def g_beta(d_kpc): r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C; return CB * r / (r * r + rc * rc)
    def law_inverse(g, a0): return g * g / (g + a0)
    def coma_host(f):
        a0 = A0H[f]; h = float(json.load(open(os.path.join(CL7, "F1A_primary_cmb_audit", "parts", f"fit_B2_{f}_cold.json")))["pars"]["h"])
        rho_c = 3 * (h * 1e5 / MPC) ** 2 / (8 * math.pi * G_SI)
        Mb_of = lambda d: law_inverse(g_beta(d), a0) * (d * KPC_C) ** 2 / G_SI / MS
        r5 = 300.0
        for _ in range(200): r5 = (3 * Mb_of(r5) * MS / (4 * math.pi * 500 * rho_c)) ** (1 / 3) / KPC * 0.5 + 0.5 * r5
        return dict(R500_kpc=r5, Mb_tot=law_inverse(g_beta(r5), a0) * (r5 * KPC_C) ** 2 / G_SI / MS)
    def delta_b(b, ft, a0):
        gN = GB["need"](ft, "x") * a0; return math.log10(glaw(b * gN, a0) / glaw(gN, a0))

    def eval_set(f, CP, B, base, verbose=False):
        a0 = A0H[f]; out = dict(kind=CP.kind, abundance_matching=CP.am, zero=CP.zero)
        # ---- gate 5: SPARC (galaxy-scale), F2 allowance, G1b massive tail, AGC 114905 / Malin 1
        keys = [(s["Mtot"], "sparc") for s in SPROF] + [(float(agc["Mb"][-1]), "lsb"), (float(mal["Mb"][-1]), "lsb")]; CP.build(keys)
        FK = [np.asarray(CP.M(s["R"], (s["Mtot"], "sparc"))) / s["Mb"] for s in SPROF]
        rows = sparc_eval(f, [1 + fk for fk in FK]); pa = pooled(rows); pb = pooled(rows, massive)
        fk_last = np.array([fk[-1] for fk in FK]); f2 = float(np.median(fk_last))
        st5 = pa["rms"] <= base["rms"] + 0.010 and abs(pa["mean"]) <= 0.05 and pb["rms"] <= base["rms_massive"] + 0.010 and abs(pb["mean"]) <= 0.05 and f2 <= F2_ALLOW[f]
        out["G5"] = dict(status="PASS" if st5 else "FAIL", all=dict(pa, rms_line=base["rms"] + 0.010), massive_tail=dict(pb, rms_line=base["rms_massive"] + 0.010),
                         F2=dict(median_retained_inside_last_over_Mb=f2, max=float(fk_last.max()), allowance=F2_ALLOW[f]),
                         retention_examples={str(round(math.log10(s["Mtot"]), 2)): CP.info((s["Mtot"], "sparc")) for s in sorted(SPROF, key=lambda s: s["Mtot"])[::35]} if not CP.zero else None)
        g1c = {}
        for nm, d in (("AGC114905", agc), ("Malin1", mal)):
            fk = np.asarray(CP.M(d["R"], (float(d["Mb"][-1]), "lsb"))) / d["Mb"]
            g1c[nm] = dict(law_only=rc_chi2(d, a0, None), with_component=rc_chi2(d, a0, fk), fK_last=float(fk[-1]))
        out["G5"]["gas_rich_LSB_reported"] = g1c
        # ---- gate 1: KiDS 59 points (each lens bin's M_b as the loader gives it; r = sqrt(G M_b / g_bar))
        CP.build([(p["Mb"] / MS, "kids") for p in LE]); per = []
        for p in LE:
            Mb = p["Mb"] / MS; r = math.sqrt(G_SI * p["Mb"] / p["gbar"]); mk = float(CP.M(r / KPC, (Mb, "kids")))
            sh = math.log10(glaw(p["gbar"] + G_SI * mk * MS / r ** 2, a0) / glaw(p["gbar"], a0))
            per.append(dict(lm=round(math.log10(Mb), 3), r_Mpc=r / MPC, shift=sh, comp_over_Mb=mk / Mb))
        sh = np.array([x["shift"] for x in per]); bins = sorted({x["lm"] for x in per}); near = {}
        for jb, lm in enumerate(bins):
            pts = [x for x in per if x["lm"] == lm]; Mb = 10 ** lm; e = {}
            for R_ in (0.3, 1.0, 1.5):
                q = min(pts, key=lambda x: abs(math.log(x["r_Mpc"] / R_))); e[f"{R_} Mpc"] = dict(r_Mpc=q["r_Mpc"], shift=q["shift"])
            near[str(lm)] = dict(nearest=e, comp_inside_200kpc_over_Mb=float(CP.M(200.0, (Mb, "kids"))) / Mb, max_shift_100_300kpc=float(max([abs(x["shift"]) for x in pts if 0.1 <= x["r_Mpc"] <= 0.3] or [0.0])),
                                 KX1_line=KX1_LINE[f][jb] if jb < 4 else None, halo=CP.info((Mb, "kids")) if not CP.zero else None)
        out["G1"] = dict(status="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs_shift=float(np.max(np.abs(sh))), n_fail=int(np.sum(np.abs(sh) > 0.05)), n_points=len(sh),
                         mean_shift=float(sh.mean()), per_bin=near, points=per if verbose else None, F2_isolated_lens_reference_Mb_inside_200kpc=0.9)
        # ---- gate 3: X-COP (amount + NA2 per-bin shape) and TR1's fraction
        CP.build([([z for z in XC if z["name"] == n][0]["Mb_last"][0], "xcop") for n in R500X])
        d = []; xr = []; fr = []; rs_ = []; per_cl = {}
        for name in R500X:
            Mbt = [z for z in XC if z["name"] == name][0]["Mb_last"][0]; key = (Mbt, "xcop"); rows_ = []
            for z in XC:
                if z["name"] != name: continue
                mk = float(CP.M(z["r_kpc"], key)); rm = z["r_kpc"] * KPC
                Mp = glaw(G_SI * (z["M_b"] + mk) * MS / rm ** 2, a0) * rm ** 2 / G_SI / MS; d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / R500X[name])
                fr.append(mk / z["M_obs"])
                gd = G_SI * z["M_obs"] * MS / rm ** 2; Msrc = law_inverse(gd, a0) * rm ** 2 / G_SI / MS - z["M_b"]
                rows_.append((z["r_kpc"] / R500X[name], math.log10(max(Msrc, 1e-30) / max(mk, 1e-30)) if Msrc > 0 and mk > 0 else None))
            per_cl[name] = dict(info=CP.info(key) if not CP.zero else None, R500_obs=R500X[name], rows=rows_)
        d = np.array(d); xr = np.array(xr); fr = np.array(fr); EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; bins3 = []
        for b_, (lo, hi) in enumerate(zip(EDG[:-1], EDG[1:])):
            m = (xr >= lo) & (xr < hi)
            bins3.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None, graded=bool(m.sum() >= 3), within=bool(abs(d[m].mean()) <= 0.10) if m.sum() >= 3 else None,
                              retained_over_Mdyn_median=float(np.median(fr[m])) if m.sum() else None, TR1_D_canonical=TR1_D_CAN[b_]))
        # TR1 SHAPE with the retained component as tracer (S reading: M_src / M_chi, one amplitude per cluster)
        shp = {b_: [] for b_ in range(5)}
        for name, pc in per_cl.items():
            vals = [(x, v) for x, v in pc["rows"] if v is not None]
            if not vals: continue
            A = float(np.mean([v for _, v in vals]))
            for b_, (lo, hi) in enumerate(zip(EDG[:-1], EDG[1:])):
                vv = [v - A for x, v in vals if lo <= x < hi]
                if vv: shp[b_].append(float(np.median(vv)))
        SH = [float(np.median(v)) if v else None for v in shp.values()]; SHv = [s for s in SH if s is not None]
        amp_ok = abs(d.mean()) <= 0.05 and math.sqrt((d ** 2).mean()) <= 0.10; shape_ok = all(b["within"] for b in bins3 if b["graded"])
        out["G3"] = dict(status="PASS" if (amp_ok and shape_ok) else "FAIL", amount_status="PASS" if amp_ok else "FAIL", shape_status="PASS" if shape_ok else "FAIL",
                         mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())), n=len(d), bins=bins3,
                         TR1_shape_reported=dict(SHAPE=SH, RMS=float(math.sqrt(np.mean(np.square(SHv)))) if SHv else None, max_abs=float(max(abs(s) for s in SHv)) if SHv else None,
                                                 follows=bool(SHv and math.sqrt(np.mean(np.square(SHv))) <= 0.10 and max(abs(s) for s in SHv) <= 0.15)),
                         per_cluster={k: v["info"] for k, v in per_cl.items()})
        # ---- gate 2: groups (Lovisari 20; M_b,sys = gas inside R500 x (1 + f*))
        o = {}
        for fst in (0, 1):
            CP.build([(gp["g5"] * (1 + fst), "group") for gp in GR]); npass = 0; med = []; per_g = []
            for gp in GR:
                Mbt = gp["g5"] * (1 + fst); key = (Mbt, "group"); ok = True; dl_g = []
                for p in gp["pts"]:
                    rm = p["r_kpc"] * KPC; Mb = p["M_gas"] * (1 + fst); mk = float(CP.M(p["r_kpc"], key))
                    Mp = glaw(G_SI * (Mb + mk) * MS / rm ** 2, a0) * rm ** 2 / G_SI / MS; dl = math.log10(p["M_obs"] / Mp); med.append(dl); dl_g.append(dl)
                    ok &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
                npass += ok; inf = CP.info(key) if not CP.zero else {}
                per_g.append(dict(name=gp["name"], R500_obs=gp["R5"], pass_=bool(ok), dlog=dl_g, R500_pre=inf.get("R500"), x0=inf.get("x0_system"), ret_R500=inf.get("ret_R500"), retained_over_Mb=inf.get("retained_over_Mb")))
            o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)), per=per_g)
        out["G2"] = dict(status="PASS" if all(v["n_pass"] >= 16 for v in o.values()) else "FAIL", **o, record_step_dex=[0.19, 0.45])
        # ---- gate 4 (reported, UA1): Coma UDGs in the mediator bath; Coma's retained component in the external field
        CH = coma_host(f); hk = (CH["Mb_tot"], "host"); CP.build([hk]); res = []; res0 = []; bs = []; rets = []
        mem = []
        for p, row in zip(B["U"], UD[f]):
            Ms = float(row["Mstar"]); dk = float(row["d_mean_kpc"]); mem.append((Ms, "udg", hk, dk))
        CP.build(mem)
        for (p, row), mk_ in zip(zip(B["U"], UD[f]), mem):
            Ms = float(row["Mstar"]); Re = float(row["Re_kpc"]); dk = float(row["d_mean_kpc"]); rh = 4 / 3 * Re
            mk = float(CP.M(rh, mk_)); b = 1.0 + mk / (0.5 * Ms); bs.append(b)
            if not CP.zero: rets.append(CP.info(mk_)["ret_total"])
            gNi = GB["need"](p["feat"], "x") * a0; gext = g_beta(dk); gNe = law_inverse(gext, a0)
            mc = float(CP.M(dk, hk)); gNe2 = gNe + G_SI * mc * MS / (dk * KPC_C) ** 2
            nu = lambda g: glaw(g, a0) / g
            d_efe = math.log10(nu(math.hypot(gNi, gNe2)) / nu(math.hypot(gNi, gNe)))
            res.append(p["D"] - delta_b(b, p["feat"], a0) - d_efe); res0.append(p["D"] - delta_b(b, p["feat"], a0))
        mu_ = float(np.mean(res)); mu0 = float(np.mean(res0))
        out["G4"] = dict(status_reported="PASS" if abs(mu_) <= 2 * B["sigU"] else "FAIL", graded=False, note="UA1: NOT A TEST; reading reported", mean=mu_, z=mu_ / B["sigU"], sigma_U=B["sigU"],
                         mean_without_host_component=mu0, b_median=float(np.median(bs)), retention_median=float(np.median(rets)) if rets else None,
                         coma_host=dict(CH, info=CP.info(hk) if not CP.zero else None), law_only_mean=float(np.mean([p["D"] for p in B["U"]])))
        # ---- gate 10: Cassini with the MW's retained component density at 8.2 kpc (uniform background)
        mwk = (6e10, "mw"); CP.build([mwk]); rhoK = CP.rho(8.2, mwk) * MS / KPC ** 3
        def cand(ft, rhoK=rhoK):
            gN = ft["x"] * a0; gK = 4 * math.pi / 3 * G_SI * rhoK * ft["r"]; return dict(delta=math.log10(glaw(gN + gK, a0) / glaw(gN, a0)))
        ok, num = GB["g_ss"](cand, B, a0)
        out["G10"] = dict(status="PASS" if ok else "FAIL", rho_Msun_pc3=rhoK / MS * PC ** 3, cassini_use=num["cassini_use"], worst_planet_use=num["worst_planet_use"], mw=CP.info(mwk) if not CP.zero else None)
        return out
    def summary(o):
        return (f"G1 KiDS {o['G1']['status'][0]} max {o['G1']['max_abs_shift']:.3f} ({o['G1']['n_fail']} over) | G2 groups {o['G2']['status'][0]} {o['G2']['fst0']['n_pass']}/{o['G2']['fst1']['n_pass']} med {o['G2']['fst0']['median_res']:+.2f}/{o['G2']['fst1']['median_res']:+.2f} "
                f"| G3 X-COP {o['G3']['status'][0]} {o['G3']['mean']:+.3f}/{o['G3']['rms']:.3f} bins " + " ".join(f"{b['mean']:+.2f}" for b in o['G3']['bins'] if b['graded'])
                + f" | G4 UDG(rep) {o['G4']['mean']:+.3f} | G5 SPARC {o['G5']['status'][0]} rms {o['G5']['all']['rms']:.4f}/{o['G5']['all']['rms_line']:.4f} F2 {o['G5']['F2']['median_retained_inside_last_over_Mb']:.3g} | G10 {o['G10']['status'][0]}")
    for f in FOOTS:
        a0 = A0H[f]; R_ = {}; RES[f] = R_
        S, E_, X = GB["build"](f, a0); U = GB["udgs"](f, a0)
        st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
        B = dict(f=f, S=S, E=E_, X=X, U=U, sigU=sigU)
        rows0 = sparc_eval(f, [np.ones(len(q["R"])) for q in GALS]); p0 = pooled(rows0); pm0 = pooled(rows0, massive)
        rx = Q8J["footings"][f].get("exact", Q8J["footings"][f].get("st_ex", {})); L0 = GBJ["cands"]["L0"][f]
        base = dict(rms=p0["rms"], mean=p0["mean"], rms_massive=pm0["rms"])
        # KA3: component -> 0 replays the record's law-only numbers
        z = eval_set(f, Comp(f, zero=True), B, base)
        ka3 = dict(G5_rms=z["G5"]["all"]["rms"], qx8_rms=rx["rms"], G5_ok=bool(abs(z["G5"]["all"]["rms"] - rx["rms"]) <= 1e-6 and abs(z["G5"]["all"]["U_median"] - rx["U_median"]) <= 1e-6),
                   G1_ok=bool(z["G1"]["max_abs_shift"] <= 1e-6),
                   G3=[z["G3"]["mean"], z["G3"]["rms"]], gb1=[L0["G2 X-COP"]["num"]["mean"], L0["G2 X-COP"]["num"]["rms"]],
                   G3_ok=bool(abs(z["G3"]["mean"] - L0["G2 X-COP"]["num"]["mean"]) <= 1e-6 and abs(z["G3"]["rms"] - L0["G2 X-COP"]["num"]["rms"]) <= 1e-6),
                   G2=[z["G2"]["fst0"]["n_pass"], z["G2"]["fst1"]["n_pass"]], G2_ok=bool(z["G2"]["fst0"]["n_pass"] == L0["G3 groups"]["num"]["fst0"]["n_pass"] and z["G2"]["fst1"]["n_pass"] == L0["G3 groups"]["num"]["fst1"]["n_pass"]
                                                                             and abs(z["G2"]["fst0"]["median_res"] - L0["G3 groups"]["num"]["fst0"]["median_res"]) <= 1e-6),
                   G4=z["G4"]["mean_without_host_component"], gb1_G4=L0["G5 Coma UDGs"]["num"]["mean"], G4_ok=bool(abs(z["G4"]["mean_without_host_component"] - L0["G5 Coma UDGs"]["num"]["mean"]) <= 1e-6),
                   G10=z["G10"]["status"])
        ka3["pass_"] = bool(ka3["G5_ok"] and ka3["G1_ok"] and ka3["G3_ok"] and ka3["G2_ok"] and ka3["G4_ok"])
        R_["KA3"] = ka3; R_["baselines"] = dict(sparc=base, sparc_qx8=dict(rms=rx["rms"], U=rx["U_median"]), sigma_U=sigU)
        P(f"[{f}] KA3 (component -> 0): {'PASS' if ka3['pass_'] else 'FAIL'} SPARC {ka3['G5_ok']} KiDS {ka3['G1_ok']} X-COP {ka3['G3_ok']} {ka3['G3'][0]:+.6f}/{ka3['G3'][1]:.6f} groups {ka3['G2_ok']} {ka3['G2']} UDG {ka3['G4_ok']} {ka3['G4']:+.6f}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
        if not ka3["pass_"]: P(f"[{f}] KA3 FAIL: stop"); continue
        R_["sets"] = {}
        sets = (("primary_SIS", dict(kind="SIS", am=False)),) if MUT else \
               (("primary_SIS", dict(kind="SIS", am=False)), ("B1_NFW_Duffy08", dict(kind="NFW", am=False)), ("B2_AM_Moster13", dict(kind="SIS", am=True)), ("B1B2_NFW_AM", dict(kind="NFW", am=True)))
        for tag, kw in sets:
            o = eval_set(f, Comp(f, **kw), B, base, verbose=(tag == "primary_SIS")); R_["sets"][tag] = o
            P(f"[{f}] {tag:15s}: " + summary(o) + f"  [{time.time()-T0:.0f}s {rss():.2f}GB]")
            dump(f"local{SUFFIX}_partial.json", RES)
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; RES["criteria"] = C.CRIT; RES["amendment"] = C.AMEND; RES["mutate"] = MUT; RES["note"] = NOTE
    RES["declared"] = dict(z_dec=C.Z_DEC, tau_tot=C.TAU_TOT, Sigma_gate_Msun_kpc2=C.SIGMA_GATE, gate_off=C.GATE_OFF, f_cap=C.F_CAP, cosmo=COSMO, F2=F2_ALLOW)
    dump(f"local{SUFFIX}.json", RES)
    pp = os.path.join(PARTS, f"local{SUFFIX}_partial.json")
    if os.path.exists(pp): os.remove(pp)
    P(f"local{SUFFIX} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")

def run_core():
    out = C.known_answers(); out["sigma_gate"] = C.sigma_gate_search()
    # reduced readings at representative systems on each footing (reported)
    out["criteria"] = C.CRIT; out["amendment"] = C.AMEND; out["mutate"] = MUT
    for k in ("KA1", "KA2", "convergence"): P(f"{k}: {'PASS' if out[k]['pass_'] else 'FAIL'}")
    P(f"Sigma_gate 0.042 g/cm^2 from the stated constants: {'REPRODUCED' if out['sigma_gate']['reproduced'] else 'NOT REPRODUCED'}; nearest " +
      "; ".join(f"{h_['expr']} = {h_['value_gcm2']:.4f} ({h_['rel']:+.1%})" for h_ in out["sigma_gate"]["within_10pct"][:3]))
    dump(f"core{SUFFIX}.json", out)

if __name__ == "__main__":
    P(f"SS1 {WHICH}{SUFFIX}. Criteria {C.CRIT} (+A1 {C.AMEND}). z_dec {C.Z_DEC}, tau {C.TAU_TOT}, Sigma_gate {C.SIGMA_GATE:.4g} Msun/kpc^2, gate off {C.GATE_OFF}; {NOTE}; footings never pooled; adopts nothing.")
    if WHICH == "core": run_core()
    elif WHICH == "local": run_local()
