#!/usr/bin/env python3
"""TS1 (FROZEN_CRITERIA.md 4b352f2a37) local gates: T1 SPARC in the disc mid-plane (+ T1-z above it), 1 KiDS single lens, T3 KiDS
with an equal neighbour at D, 2 groups, 3 X-COP (spherical I(x)), for M-W, M-split, M-law; KA-T6 (s = 1 replay), MT1 (s = 0),
MT2 (h_z x 3), MT3 (D = 7 Mpc). Loaders as SS1 run_local (QX8 SPARC + exact-field tables, GB1 battery prefix), read-only.
    SS1_PJ1_DIR=<pj1 extract> python3 ts1_local.py   -> parts/local.json, ts1_local.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); SS1D = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1D); sys.path.insert(0, HERE)
CRIT = "4b352f2a37"; T0 = time.time()
_a = sys.argv; sys.argv = [_a[0]]
import ss1_core as C
import ss1v as SV
import ts1_core as TC
sys.argv = _a
L = []
def P(s): print(s, flush=True); L.append(s)
G_SI, MS, KPC, MPC = 6.6743e-11, 1.98892e30, 3.0857e19, 3.0857e22; G_KPC = 4.3009172706e-6; PC = 3.0857e16
A0H = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; FOOTS = ("canonical", "alt")
def nu(y): y = np.maximum(np.asarray(y, float), 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)
def geff(g, a0, s): g = np.asarray(g, float); return g * (1 + (nu(np.abs(g) / a0) - 1) * s)
def glaw(g, a0): return geff(g, a0, 1.0)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}; a = sys.argv; sys.argv = [path]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns
# ---------------- data (as SS1 run_local)
sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field")); a_ = sys.argv; sys.argv = [a_[0]]
with contextlib.redirect_stdout(io.StringIO()):
    import qx8 as Q8
sys.argv = a_
GALS = Q8.load_sparc()
GB = load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
XC, GR = GB["XC"], GB["GR"]; LE = GB["NS"]["lensing"]()
from astropy.io import fits
R500X = {}
for name in sorted({z["name"] for z in XC}):
    with fits.open(os.path.join(GB["DATA"], "xcop", name, f"{name}_fgas_profile.fits")) as h: R500X[name] = float(h[1].header["R500"])
lU, lN = np.log(Q8.UPS), np.log(Q8.NODES)
PRE = {f: [np.array([np.interp(lU, lN, T[:, j]) for j in range(T.shape[1])]) for T in
           (np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False)["T"] for i in range(len(GALS)))] for f in FOOTS}
TR1 = [0.71, 0.66, 0.58, 0.46, 0.32]
# ---------------- components
def viel_Mhm(mk, F):
    h = F["h"]; OD = F["R"] * F["ob"]; rho = F["Om"] * 2.77536627e11 * h * h
    al = 0.049 * mk ** -1.11 * ((OD / h ** 2) / 0.25) ** 0.11 * (h / 0.7) ** 1.22 / h; lam = 2 * math.pi * al * (2 ** (1.12 / 5) - 1) ** (-1 / (2 * 1.12)); return 4 * math.pi / 3 * rho * (lam / 2) ** 3
MHM0 = (0.050 ** (-1 / 1.16) - 1) * 4.060e11
def comp(variant, f):
    """returns Mchi(r_kpc, Mb_sys) and dMchi/dr (Msun/kpc) for the system with baryon mass Mb_sys (SS1 primary halo, S(M200))."""
    F = SV.footing(f)
    if variant == "M-law": return (lambda r, Mb: 0.0 * np.asarray(r, float)), (lambda r, Mb: 0.0 * np.asarray(r, float)), {}
    m_W = 1000 * brentq(lambda x: math.log(viel_Mhm(x, F) / MHM0), 1e-3, 100.0); mhms = [(1.0, MHM0)] if variant == "M-W" else [(0.5, MHM0), (0.5, viel_Mhm(m_W / 10 / 1000, F))]
    def H(Mb): Hh = C.halo(Mb, F["R"], F["h"], F["Om"], z=0.55); return Hh
    def M(r, Mb):
        Hh = H(Mb); Sx = sum(w * (1 + Mh / Hh["M200"]) ** -1.16 for w, Mh in mhms); return Sx * Hh["Menc"](np.asarray(r, float))
    def dM(r, Mb):
        Hh = H(Mb); Sx = sum(w * (1 + Mh / Hh["M200"]) ** -1.16 for w, Mh in mhms); r = np.asarray(r, float); return np.where(r < Hh["R200"], Sx * Hh["Mchi0"] / Hh["R200"], 0.0)
    return M, dM, dict(m_W_eV=m_W, M_hm=[Mh for _, Mh in mhms])
# ---------------- T1 SPARC
def sparc(f, variant, smode="disc", hz_fac=1.0, zabove=False):
    a0 = A0H[f]; Mc, _, _ = comp(variant, f); rows = []; srep = []
    for i, (q, Tf) in enumerate(zip(GALS, PRE[f])):
        R = q["R"]; Rm = q["Rm"]; g = q["GB"].copy()
        VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2; Mb = np.maximum(np.maximum.accumulate(np.clip(VB2 * R / G_KPC, 0, None)), 1e3)
        fk = np.asarray(Mc(R, float(Mb[-1]))) / Mb; g = g * (1 + fk)[:, None]
        if smode == "one": s = np.ones_like(g)
        elif smode == "zero": s = np.zeros_like(g)
        else:
            Rd = max(q["meta"]["Rdisk"], 0.1); hz = 0.196 * Rd ** 0.633 * hz_fac * 1000 * PC          # m
            rho0 = Q8.UPS[None, :] * np.clip(q["SBd"], 0, None)[:, None] * MS / PC ** 2 / (2 * hz)       # kg/m^3, stars only (generous)
            if zabove: rho0 = rho0 / math.cosh(2.0) ** 2
            PRR = np.gradient(g, Rm, axis=0); PRo = g / Rm[:, None]; Pzz = 4 * math.pi * G_SI * rho0 - PRR - PRo
            I = TC.I_of_eig(np.stack([PRR, PRo, Pzz], axis=-1)); s = TC.s_of_I(I)
            j50 = int(np.where(Q8.UPS == 0.50)[0][0]); srep.extend(list(s[q["OK"][:, j50], j50]))
        lgp = np.log10(np.maximum(geff(g, a0, s), 1e-300)) + Tf
        OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); k = int(np.argmin(wr2 / np.maximum(ws, 1e-300))); rows.append((wr2[k], wr[k], ws[k], k))
    def pooled(idx):
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx)
        return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws), U_median=float(np.median([Q8.UPS[rows[i][3]] for i in idx])))
    massive = [i for i, q in enumerate(GALS) if q["meta"]["Vflat"] >= 250.0]
    out = dict(all=pooled(range(len(rows))), massive=pooled(massive))
    if srep: out["s_at_U0.5"] = dict(median=float(np.median(srep)), p10=float(np.percentile(srep, 10)), p90=float(np.percentile(srep, 90)), frac_below_0p5=float(np.mean(np.array(srep) < 0.5)))
    return out
# ---------------- spherical systems
def s_from_profile(r, Mtot):
    lr = np.log(np.asarray(r, float)); lm = np.log(np.maximum(np.asarray(Mtot, float), 1e-30)); o = np.argsort(lr)
    sl = np.empty_like(lr); sl[o] = np.gradient(lm[o], lr[o]) if len(lr) > 1 else 0.0; return TC.s_sph(np.clip(sl, 0, None) / 3.0), sl / 3.0
def kids(f, variant, smode="sph", D=3.5):
    a0 = A0H[f]; Mc, dMc, _ = comp(variant, f); sh = []; svals = []
    for p in LE:
        Mb = p["Mb"] / MS; r = math.sqrt(G_SI * p["Mb"] / p["gbar"]); rk = r / KPC; mk = float(Mc(rk, Mb)); gN = p["gbar"] + G_SI * mk * MS / r ** 2
        x = rk * float(dMc(rk, Mb)) / (3 * (Mb + mk))
        if smode == "one": s = 1.0
        elif smode == "zero": s = 0.0
        elif smode == "sph": s = float(TC.s_sph(x))
        else: s = TC.sbar_two_mass(rk / 1000.0 / D, 1.0, x_lens=x)                 # T3: equal neighbour at D (Mpc)
        svals.append(s); sh.append(math.log10(float(geff(gN, a0, s)) / float(glaw(p["gbar"], a0))))
    sh = np.array(sh); return dict(status="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs=float(np.max(np.abs(sh))), n_over=int(np.sum(np.abs(sh) > 0.05)), s_min=float(min(svals)), mean_shift=float(sh.mean()))
def xcop(f, variant, smode="sph"):
    a0 = A0H[f]; Mc, _, _ = comp(variant, f); d = []; xr = []; fr = []; sv = []
    for name in R500X:
        pts = [z for z in XC if z["name"] == name]; Mbt = pts[0]["Mb_last"][0]; r = np.array([z["r_kpc"] for z in pts]); mk = np.array([float(Mc(z["r_kpc"], Mbt)) for z in pts])
        Mt = np.array([z["M_b"] for z in pts]) + mk; s, x = s_from_profile(r, Mt)
        if smode == "one": s = np.ones_like(s)
        if smode == "zero": s = np.zeros_like(s)
        for z, mk_, s_, Mt_ in zip(pts, mk, s, Mt):
            rm = z["r_kpc"] * KPC; Mp = float(geff(G_SI * Mt_ * MS / rm ** 2, a0, s_)) * rm ** 2 / G_SI / MS; d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / R500X[name]); fr.append(mk_ / z["M_obs"]); sv.append(s_)
    d, xr, fr, sv = map(np.array, (d, xr, fr, sv)); EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; bins = []
    for b_, (lo, hi) in enumerate(zip(EDG[:-1], EDG[1:])):
        m = (xr >= lo) & (xr < hi)
        bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None, graded=bool(m.sum() >= 3), within=bool(abs(d[m].mean()) <= 0.10) if m.sum() >= 3 else None,
                         retained_over_Mdyn=float(np.median(fr[m])) if m.sum() else None, TR1=TR1[b_], s_median=float(np.median(sv[m])) if m.sum() else None))
    amp = abs(d.mean()) <= 0.05 and math.sqrt((d ** 2).mean()) <= 0.10; shp = all(b["within"] for b in bins if b["graded"])
    return dict(status="PASS" if (amp and shp) else "FAIL", mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())), bins=bins)
def groups(f, variant, smode="sph"):
    a0 = A0H[f]; Mc, _, _ = comp(variant, f); o = {}
    for fst in (0, 1):
        npass = 0; med = []; sv = []
        for gp in GR:
            Mbt = gp["g5"] * (1 + fst); r = np.array([p["r_kpc"] for p in gp["pts"]]); mk = np.array([float(Mc(p["r_kpc"], Mbt)) for p in gp["pts"]])
            Mt = np.array([p["M_gas"] * (1 + fst) for p in gp["pts"]]) + mk; s, x = s_from_profile(r, Mt)
            if smode == "one": s = np.ones_like(s)
            if smode == "zero": s = np.zeros_like(s)
            ok = True
            for p, Mt_, s_ in zip(gp["pts"], Mt, s):
                rm = p["r_kpc"] * KPC; Mp = float(geff(G_SI * Mt_ * MS / rm ** 2, a0, s_)) * rm ** 2 / G_SI / MS; dl = math.log10(p["M_obs"] / Mp); med.append(dl); sv.append(s_)
                ok &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
            npass += ok
        o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)), s_median=float(np.median(sv)))
    return dict(status="PASS" if all(v["n_pass"] >= 16 for v in o.values()) else "FAIL", **o)
# ---------------- run
RES = dict(criteria=CRIT, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
for f in FOOTS:
    base = sparc(f, "M-law", "one"); RES[f] = dict(L0_sparc=base)
    P(f"[{f}] L0 (law only, s = 1): SPARC rms {base['all']['rms']:.4f} mean {base['all']['mean']:+.4f}; massive rms {base['massive']['rms']:.4f}")
    def sparc_status(o): return "PASS" if (o["all"]["rms"] <= base["all"]["rms"] + 0.010 and abs(o["all"]["mean"]) <= 0.05 and o["massive"]["rms"] <= base["massive"]["rms"] + 0.010 and abs(o["massive"]["mean"]) <= 0.05) else "FAIL"
    # KA-T6 (s = 1, law only) vs the record's law-only numbers: KiDS 0 shift, X-COP +0.4675 / +0.4345, groups 0/0
    k6 = dict(kids=kids(f, "M-law", "one"), xcop=xcop(f, "M-law", "one"), groups=groups(f, "M-law", "one"))
    ref = {"canonical": 0.467500, "alt": 0.434524}[f]; ka6 = abs(k6["kids"]["max_abs"]) < 1e-9 and abs(k6["xcop"]["mean"] - ref) < 1e-5 and k6["groups"]["fst0"]["n_pass"] == 0 and k6["groups"]["fst1"]["n_pass"] == 0
    RES[f]["KA_T6"] = dict(k6, pass_=bool(ka6), xcop_ref=ref)
    P(f"[{f}] KA-T6 (s = 1 replay): KiDS max {k6['kids']['max_abs']:.1e}, X-COP mean {k6['xcop']['mean']:+.6f} (record {ref:+.6f}), groups {k6['groups']['fst0']['n_pass']}/{k6['groups']['fst1']['n_pass']} -> {'PASS' if ka6 else 'FAIL'}")
    for V in ("M-W", "M-split", "M-law"):
        _, _, info = comp(V, f)
        sp = sparc(f, V); sp["status"] = sparc_status(sp); spz = sparc(f, V, zabove=True); spz["status_reported"] = sparc_status(spz)
        k1 = kids(f, V, "sph"); k3 = kids(f, V, "two", 3.5); g2 = groups(f, V); x3 = xcop(f, V)
        RES[f][V] = dict(info=info, T1=sp, T1_z_above=spz, G1=k1, T3=k3, G2=g2, G3=x3)
        P(f"[{f}] {V}: T1 SPARC {sp['status']} rms {sp['all']['rms']:.4f} (line {base['all']['rms']+0.010:.4f}) mean {sp['all']['mean']:+.3f}, massive rms {sp['massive']['rms']:.4f} mean {sp['massive']['mean']:+.3f}; s at Ups 0.5 median {sp['s_at_U0.5']['median']:.3f} (p10 {sp['s_at_U0.5']['p10']:.3f}, p90 {sp['s_at_U0.5']['p90']:.3f}, <0.5: {100*sp['s_at_U0.5']['frac_below_0p5']:.0f} %)"
          f"; above disc (2 h_z) rms {spz['all']['rms']:.4f} {spz['status_reported']}")
        P(f"    KiDS single {k1['status']} max {k1['max_abs']:.3f} (s_min {k1['s_min']:.3f}); T3 neighbour 3.5 Mpc {k3['status']} max {k3['max_abs']:.3f} (s_min {k3['s_min']:.3f}); groups {g2['status']} {g2['fst0']['n_pass']}/{g2['fst1']['n_pass']} med {g2['fst0']['median_res']:+.2f}/{g2['fst1']['median_res']:+.2f} (s med {g2['fst0']['s_median']:.2f})"
          f"; X-COP {x3['status']} {x3['mean']:+.3f}/{x3['rms']:.3f} bins " + " ".join(f"{b['mean']:+.2f}(s {b['s_median']:.2f}, ret {b['retained_over_Mdyn']:.2f})" for b in x3['bins'] if b['graded']))
    # MUTATE
    mt1 = sparc(f, "M-W", "zero"); mt1["status"] = sparc_status(mt1); mt2 = sparc(f, "M-W", hz_fac=3.0); mt2["status"] = sparc_status(mt2); mt3 = kids(f, "M-W", "two", 7.0)
    RES[f]["MUTATE"] = dict(MT1_s0=mt1, MT2_hz_x3=mt2, MT3_D7=mt3)
    P(f"[{f}] MUTATE: MT1 s = 0 SPARC {mt1['status']} rms {mt1['all']['rms']:.4f}; MT2 h_z x3 SPARC {mt2['status']} rms {mt2['all']['rms']:.4f} (s median {mt2['s_at_U0.5']['median']:.3f}); MT3 D 7 Mpc KiDS max {mt3['max_abs']:.3f} {mt3['status']}")
RES["seconds"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "parts", "local.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ts1_local.out"), "w").write("\n".join(L) + "\n")
P(f"done {RES['seconds']:.0f} s")
