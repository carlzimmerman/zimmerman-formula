#!/usr/bin/env python3
"""NC4 (= Framework Candidate 2's NC1; criteria 54784e16e5): the born-clumped cold dark energy clump spectrum.
R3/K3 abundance + cosmic share (eRASS1 1/Vmax host baryon mass function), R7 (CK3's tests on UA1's posterior, child
process nc4_r7.py), K5 (Lagrangian top-hat collapse in the law's field vs NA2's gas-to-stars band and per-bin rule, NC3's
core rule), cored-profile question and CLASH slope (reported). Both footings, never pooled.
    python3 nc4.py            -> nc4.json / nc4.out
    python3 nc4.py --mutate   -> nc4_MUTATE.json / nc4_MUTATE.out   (M1 flat spectrum, M2 uniform component, M3 planted)
Read-only: NA2's na2.py prefix (QX7 iter_5 prelude, X-COP shapes, x_eval) exec'd from source; KD1 kd1.json; eRASS1 FITS;
X-COP ettori2019 JSON. Env NC4_UA1_DIR overrides UA1's folder for the R7 child. One thread.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, signal, resource, subprocess
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from astropy.io import fits
from scipy.integrate import solve_ivp, quad
np.seterr(all="ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07")
MUT = "--mutate" in sys.argv; TAG = "nc4_MUTATE" if MUT else "nc4"; OUT = []
RES = dict(lane="NC4", alias="NC4 = Framework Candidate 2's NC1", criteria="54784e16e5", tag=TAG,
           note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
def P(s=""): print(s, flush=True); OUT.append(s)
def dump(tag=TAG):
    RES["peak_rss_MB_main"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
    json.dump(RES, open(os.path.join(HERE, tag + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n")

# ------------------------------------------------------------------ NA2 prefix (X-COP machinery), exec'd read-only
NA2P = os.path.join(CL7, "NA2_compact_baryon_remnant", "na2.py")
src = open(NA2P).read(); src = src[:src.index("# ------------------------------------------------------------------ GB1 battery")]
NS = {"__file__": NA2P, "__name__": "na2_prefix"}; _a = sys.argv; sys.argv = [NA2P]; _so = sys.stdout; sys.stdout = io.StringIO()
try: exec(compile(src, "na2_prefix", "exec"), NS)
finally: sys.argv = _a; sys.stdout = _so
def _term(sig, frm):
    RES["interrupted"] = "SIGTERM"; dump(TAG + "_partial"); sys.exit(3)
signal.signal(signal.SIGTERM, _term)
A0, XC, KPC, MS, G, glaw, DATA = (NS[k] for k in ("A0", "XC", "KPC", "MS", "G", "glaw", "DATA"))
SH, XINFO, x_eval, fit_x, BIN_EDGES = NS["SH"], NS["XINFO"], NS["x_eval"], NS["fit_x"], NS["BIN_EDGES"]
XNAMES = sorted(XINFO)
P(f"NC4 {'MUTATE' if MUT else 'MAIN'} (NC4 = Framework Candidate 2's NC1). X-COP set {XNAMES}. kappa = 1/2 FITTED; not theory closed.")

R_NAT = 5.562; RHO_B = 0.02166 * 2.775e11; RHO_B_NAT = 0.1209 / R_NAT * 2.775e11   # Msun / Mpc^3, h-free
KDJ = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
ETT = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json")))
KA = {}; RES["KA"] = KA

# ------------------------------------------------------------------ KA1 KD1 f-table
FT = {}
ref1 = {"canonical": dict(X=4.1786, cap=0.3257, g1=1.2320, g0=3.4640, cap_f=4.1110), "alt": dict(X=3.7833, cap=0.1937, g1=0.9323, g0=2.8646, cap_f=4.1121)}
ok = True
for f in A0:
    u = KDJ["footings"][f]["uniform_f_diag"]
    FT[f] = dict(X=u["Xcop_f_need"], cap=u["SPARC_f_max"], g1=u["groups_fst1_f_need"], g0=u["groups_fst0_f_need"], cap_f=u["capture_f"])
    ok &= all(abs(FT[f][k] - ref1[f][k]) <= 1e-4 for k in ref1[f])
KA["KA1_KD1_ftable"] = dict(table=FT, ok=bool(ok))
P(f"KA1 KD1 f-table: {FT} -> {'PASS' if ok else 'FAIL'}")

# ------------------------------------------------------------------ KA2 NA2 band and shapes
def conc(fun, r500):
    return float(fun(np.array([0.25 * r500]))[0] / fun(np.array([0.7 * r500]))[0])
BAND = {}
for n in XNAMES:
    I = XINFO[n]; BAND[n] = dict(gas=conc(I["fg"], I["r500"]), hse=conc(I["fh"], I["r500"]), stars=conc(I["fs"], I["r500"]), r500_kpc=I["r500"])
rng_ = {k: (min(BAND[n][k] for n in XNAMES), max(BAND[n][k] for n in XNAMES)) for k in ("gas", "hse", "stars")}
okb = (abs(rng_["gas"][0] - 0.16) <= 0.01 and abs(rng_["gas"][1] - 0.24) <= 0.01 and abs(rng_["hse"][0] - 0.21) <= 0.01 and abs(rng_["hse"][1] - 0.30) <= 0.01
       and abs(rng_["stars"][0] - 0.32) <= 0.01 and abs(rng_["stars"][1] - 0.51) <= 0.01)
st = {}; oks = True
for f, (Fr, rr) in {"canonical": (1.723, 0.1208), "alt": (1.560, 0.1138)}.items():
    Fx = fit_x(f, "stars"); e = x_eval(f, "stars", Fx); eb = x_eval(f, "baryon", FT[f]["X"])
    st[f] = dict(stars_F=Fx, stars_rms=e["rms"], baryon_at_need_mean=eb["mean"], baryon_at_need_rms=eb["rms"])
    oks &= abs(Fx - Fr) <= 1e-3 and abs(e["rms"] - rr) <= 1e-3 and abs(eb["mean"]) <= 1e-3 and abs(eb["rms"] - {"canonical": 0.0818, "alt": 0.0835}[f]) <= 1e-3
KA["KA2_NA2_band_shapes"] = dict(band=BAND, ranges=rng_, shapes=st, ok=bool(okb and oks))
P(f"KA2 NA2 band ranges gas {rng_['gas'][0]:.3f}-{rng_['gas'][1]:.3f}, HSE {rng_['hse'][0]:.3f}-{rng_['hse'][1]:.3f}, stars {rng_['stars'][0]:.3f}-{rng_['stars'][1]:.3f}; "
  f"shapes {json.dumps({f: {k: round(v, 4) for k, v in s.items()} for f, s in st.items()})} -> {'PASS' if okb and oks else 'FAIL'}")

# ------------------------------------------------------------------ eRASS1 (NA2's census columns and cuts) + KA3
d = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
Z_ = np.array(d["BEST_Z"], float); PC = np.array(d["PCONT"], float); MG = np.array(d["MGAS500"], float) * 1e11
M5 = np.array(d["M500"], float) * 1e13; F5 = np.array(d["F500"], float)
del d
sX = float(np.mean([XINFO[n]["s500"] for n in XNAMES]))
def census_na2(zmax=0.10, pcmax=0.5, area=20626.0, h=0.70):
    sel = (Z_ >= 0.02) & (Z_ <= zmax) & (PC <= pcmax) & np.isfinite(MG) & (MG > 0) & np.isfinite(M5)
    Dh = 2.998e5 / (100 * h); V = area / 41252.96 * 4 / 3 * math.pi * ((Dh * zmax) ** 3 - (Dh * 0.02) ** 3)
    hs = (h / 0.70) ** 2.5; cl = sel & (M5 >= 1e14); gr = sel & (M5 >= 1e13) & (M5 < 1e14)
    return dict(N_cl=int(cl.sum()), N_gr=int(gr.sum()), V=V, hb=(MG[cl].sum() / hs * (1 + sX) + MG[gr].sum() / hs * 2.0) / (RHO_B * V))
c0 = census_na2()
KA["KA3_NA2_census"] = dict(**c0, ok=bool(c0["N_cl"] == 467 and c0["N_gr"] == 590 and abs(c0["V"] / 1.63e8 - 1) < 0.005 and abs(c0["hb"] - 0.0108) < 0.00005))
P(f"KA3 NA2 census: {c0['N_cl']} clusters, {c0['N_gr']} groups, V {c0['V']:.4g} Mpc^3, host baryons {c0['hb']:.5f} of rho_b -> {'PASS' if KA['KA3_NA2_census']['ok'] else 'FAIL'}")

# ------------------------------------------------------------------ spectrum basics
LMX = float(np.median([math.log10(ETT[n]["M500"] * 1e14) for n in XNAMES]))
SGRID = [round(0.1 * i, 2) for i in range(41)]
def f_spec(fX, sf, lm500): return np.maximum(fX + sf * (np.asarray(lm500, float) - LMX), 0.0)

# ------------------------------------------------------------------ R7 child (also KA4)
UA1D = os.environ.get("NC4_UA1_DIR", "")
r7p = os.path.join(HERE, TAG + "_r7child.json")
cp = subprocess.run([sys.executable, os.path.join(HERE, "nc4_r7.py"), r7p, json.dumps({f: dict(fX=FT[f]["X"], lMX=LMX) for f in A0}), json.dumps(SGRID)],
                    capture_output=True, text=True, env=dict(os.environ, **({"NC4_UA1_DIR": UA1D} if UA1D else {})))
if cp.returncode != 0: P("R7 child failed: " + cp.stderr[-800:]); RES["label"] = "NO VERDICT (R7 child failed)"; dump(); sys.exit(2)
R7 = json.load(open(r7p)); os.remove(r7p); RES["r7_child_peak_rss_GB"] = R7["peak_rss_GB"]
ok4 = True
for f, ref in {"canonical": (0.259, 0.21, 0.04, 0.49), "alt": (0.221, 0.20, 0.05, 0.45)}.items():
    k = R7["KA"][f]; ok4 &= (k["array_equal"] and k["summary_equals_ua1_json"] and round(k["step0"]["median"], 3) == ref[0]
                            and round(k["data_slope"]["median"], 2) == ref[1] and round(k["data_slope"]["lo95"], 2) == ref[2] and round(k["data_slope"]["hi95"], 2) == ref[3])
KA["KA4_UA1_CK3"] = dict(child=R7["KA"], ok=bool(ok4))
P(f"KA4 UA1/CK3: step0 {R7['KA']['canonical']['step0']['median']:+.3f} / {R7['KA']['alt']['step0']['median']:+.3f}; data slope "
  + " / ".join(f"{R7['KA'][f]['data_slope']['median']:+.2f} [{R7['KA'][f]['data_slope']['lo95']:+.2f}, {R7['KA'][f]['data_slope']['hi95']:+.2f}]" for f in A0)
  + f" -> {'PASS' if ok4 else 'FAIL'} (child peak RSS {R7['peak_rss_GB']:.2f} GB)")
RES["KA_all"] = bool(all(v["ok"] for v in KA.values()))
if not RES["KA_all"]: P("KNOWN ANSWER FAILED: stop, nothing graded."); RES["label"] = "NO VERDICT (known answer failed)"; dump(); sys.exit(2)

# =================================================================== 1/Vmax host baryon mass function
SEL0 = (Z_ >= 0.02) & (Z_ <= 0.10) & (PC <= 0.5) & np.isfinite(MG) & (MG > 0) & np.isfinite(M5) & (M5 >= 1e13) & np.isfinite(F5) & (F5 > 0)
def vmax_sample(Flim, area=20626.0, h=0.70, sG=1.0, zlo=0.02, zhi=0.10):
    s = SEL0 & (F5 >= Flim)
    Dh = 2.998e5 / (100 * h); D = Dh * Z_[s]; Dlo, Dhi = Dh * zlo, Dh * zhi
    Om = area / 41252.96 * 4 * math.pi
    Dmax = np.minimum(D * np.sqrt(F5[s] / Flim), Dhi)
    Vmax = Om / 3 * (Dmax ** 3 - Dlo ** 3); V = Om / 3 * (D ** 3 - Dlo ** 3)
    hs = (h / 0.70) ** 2.5; m5 = M5[s]
    Mb = MG[s] / hs * np.where(m5 >= 1e14, 1 + sX, 1 + sG)
    vv = V / Vmax; N = int(s.sum())
    return dict(N=N, Vmax=Vmax, Mb=Mb, lm5=np.log10(m5), vv_mean=float(vv.mean()), vv_sig=float(1 / math.sqrt(12 * N)), Flim=Flim, area=area, h=h, sG=sG)
FGRID = [2.0, 5.0, 10.0, 20.0, 50.0]
schmidt = {}
for Fl in FGRID:
    S_ = vmax_sample(Fl); schmidt[Fl] = dict(N=S_["N"], vv=S_["vv_mean"], sig=S_["vv_sig"], ok=bool(abs(S_["vv_mean"] - 0.5) <= 2 * S_["vv_sig"]))
okF = [Fl for Fl in FGRID if schmidt[Fl]["ok"]]
FLIM = okF[0] if okF else FGRID[-1]
RES["schmidt"] = {str(k): v for k, v in schmidt.items()}; RES["F_lim"] = FLIM; RES["F_lim_found_by_test"] = bool(okF)
P("Schmidt V/Vmax: " + "; ".join(f"F>={Fl:g}e-14: N {v['N']} <V/Vmax> {v['vv']:.3f} +- {v['sig']:.3f} {'ok' if v['ok'] else 'no'}" for Fl, v in schmidt.items())
  + f" -> F_lim {FLIM:g}e-14 erg/cm^2/s{'' if okF else ' (no grid value passed: the largest used, disclosed)'}")
FBR = sorted({FGRID[max(0, FGRID.index(FLIM) - 1)], FLIM, FGRID[min(len(FGRID) - 1, FGRID.index(FLIM) + 1)]})
BINS = np.arange(10.75, 14.76, 0.25)   # log10 M_b edges
def massfn(S_):
    h_, _ = np.histogram(np.log10(S_["Mb"]), BINS, weights=1 / S_["Vmax"]); n_, _ = np.histogram(np.log10(S_["Mb"]), BINS)
    return h_ / 0.25, n_        # per dex, Mpc^-3

def capacity(S_, fX, sf, X=1.0, rho_d=None, extend=False):
    rho_d = R_NAT * RHO_B if rho_d is None else rho_d
    fi = f_spec(fX, sf, S_["lm5"]); cap = float((X * fi * S_["Mb"] / S_["Vmax"]).sum() / rho_d)
    hb = float((S_["Mb"] / S_["Vmax"]).sum() / (rho_d / R_NAT))
    ext = 0.0
    if extend:      # power law below the two lowest populated bins, to f's floor (M500 via the median Mb/M500 of the lowest hosts)
        phi, n_ = massfn(S_); mids = 0.5 * (BINS[1:] + BINS[:-1]); pop = np.where(n_ >= 3)[0]
        if len(pop) >= 2:
            i0, i1 = pop[0], pop[1]; sl = (math.log10(phi[i1]) - math.log10(phi[i0])) / (mids[i1] - mids[i0])
            lo_ = S_["lm5"] < 13.3; rat = float(np.median(np.log10(S_["Mb"][lo_]) - S_["lm5"][lo_])) if lo_.any() else -1.0
            lm5_floor = LMX - fX / sf if sf > 0 else 10.0
            xs = np.linspace(max(lm5_floor + rat, 9.0), BINS[0], 200)
            if xs[-1] > xs[0]:
                ph = phi[i0] * 10 ** (sl * (xs - mids[i0])); fx = f_spec(fX, sf, xs - rat)
                ext = float(np.trapz(X * fx * 10 ** xs * ph, xs) / rho_d)
    return dict(C=cap + ext, C_hosts=cap, C_ext=ext, host_baryons_over_rhob=hb, A=(1 / (cap + ext)) if cap + ext > 0 else float("inf"))

# X_HSE: room for cold dark energy between R500 and R200 from the X-COP HSE masses (generous)
def mb_r500(n): I = XINFO[n]; r = np.array([I["r500"]]); return float(I["fg"](r)[0] + I["fs"](r)[0])
def x_hse(f):
    v = [1 + (ETT[n]["M200"] - ETT[n]["M500"]) * 1e14 / (FT[f]["X"] * mb_r500(n)) for n in XNAMES]
    return float(np.median(v)), v

# =================================================================== collapse model (section 2)
GG = 4.498e-15                       # Mpc^3 Msun^-1 Gyr^-2
SI2 = 3.0857e22 / (3.15576e16) ** 2  # (Mpc/Gyr^2) per (m/s^2) inverse: m/s^2 = 1/SI2 ... see conv below
ACC = (3.15576e16) ** 2 / 3.0857e22  # 1 m/s^2 in Mpc/Gyr^2
def bg(f):
    s = KDJ["footings"][f]["setting"]; h = s["h"]; Or = KDJ["footings"][f]["B1"]["Omega_r"]
    Om = (s["omega_b"] + s["omega_d"]) / h ** 2; OL = 1 - Om - Or; H0 = 0.102271 * h
    rc0 = 3 * H0 ** 2 / (8 * math.pi * GG)
    return dict(h=h, Om=Om, Or=Or, OL=OL, H0=H0, rc0=rc0, zeq=Om / Or - 1)
def Hof(B, a): return B["H0"] * math.sqrt(B["Om"] / a ** 3 + B["Or"] / a ** 4 + B["OL"])
def tof(B, a): return quad(lambda x: 1 / (x * Hof(B, x)), 1e-12, a, limit=200)[0]
def collapse(f, M_matter, phi, zb):
    """outer shell of a Lagrangian top-hat: returns r_ta, z_ta, r_f (Mpc physical) and law boost at turnaround."""
    B = bg(f); a0 = A0[f]; ab = 1 / (1 + zb); Db = (R_NAT / phi + 1) / (R_NAT + 1) - 1
    rhob = B["rc0"] * B["Om"] / ab ** 3; ri = (3 * M_matter / (4 * math.pi * (1 + Db) * rhob)) ** (1 / 3)
    vi = Hof(B, ab) * ri; tb = tof(B, ab); t0 = tof(B, 1.0)
    def rhs(t, y):
        a, r, v = y; gN = GG * M_matter / r ** 2
        g = glaw(gN / ACC, a0) * ACC
        acc = -g - (8 * math.pi * GG / 3) * B["rc0"] * B["Or"] / a ** 4 * r + (8 * math.pi * GG / 3) * B["rc0"] * B["OL"] * r
        return [a * Hof(B, a), v, acc]
    ev = lambda t, y: y[2]; ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, (tb, t0), [ab, ri, vi], method="DOP853", rtol=1e-9, atol=1e-14 * ri, events=ev)
    if sol.t_events[0].size:
        a_ta, r_ta = sol.y_events[0][0][0], sol.y_events[0][0][1]; gN = GG * M_matter / r_ta ** 2
        return dict(turned=True, Delta_b=Db, r_ta=r_ta, z_ta=1 / a_ta - 1, r_f=0.5 * r_ta, t_ta=float(sol.t_events[0][0]),
                    collapsed_by_z0=bool(2 * sol.t_events[0][0] <= t0), nu_ta=float(glaw(gN / ACC, a0) / (gN / ACC)))
    return dict(turned=False, Delta_b=Db, r_ta=None, z_ta=None, r_f=float(sol.y[1][-1]), collapsed_by_z0=False, nu_ta=None)
PHIS = [0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99, 0.995, 0.999, 0.9995, 0.9999]

def sphere_shape(rf_kpc):
    return lambda rk: np.minimum(np.asarray(rk, float), rf_kpc) ** 3
def cored_shape(rc, gam):
    def m(rk):
        x = np.asarray(rk, float) / rc
        return (x - np.arctan(x)) if gam == 2 else (np.arcsinh(x) - x / np.sqrt(1 + x * x))
    return m
def install(name_key, n, mfun):       # NA2-style normalisation at Mb_last's radius, constant beyond
    tl = XINFO[n]["tl"]; t = float(mfun(np.array([tl]))[0])
    SH[n][name_key] = lambda r_m, mfun=mfun, t=t, tl=tl: np.where(np.asarray(r_m, float) / KPC > tl, 1.0, mfun(np.asarray(r_m, float) / KPC) / t)
def clash_slope(f, key, F):
    sl = []
    for n in XNAMES:
        pts = [z for z in XC if z["name"] == n and z["r_kpc"] > 100]
        if len(pts) < 2: continue
        r = np.array([z["r_kpc"] for z in pts]); mb = np.array([z["M_b"] for z in pts])
        mc = F * XINFO[n]["Mlast"] * SH[n][key](r * KPC)
        y = np.log10(mc / mb); x = np.log10(r); sl.append(float(np.polyfit(x, y, 1)[0]))
    return float(np.median(sl)) if sl else None
def k5_grade(f, key, mfun_by_cluster, fit=True):
    for n in XNAMES: install(key, n, mfun_by_cluster[n])
    cc = {n: conc(lambda r, m=mfun_by_cluster[n]: m(r), XINFO[n]["r500"]) for n in XNAMES}
    inband = {n: bool(BAND[n]["gas"] <= cc[n] <= BAND[n]["stars"]) for n in XNAMES}
    Ff = fit_x(f, key); e = x_eval(f, key, Ff); en = x_eval(f, key, FT[f]["X"])
    return dict(conc=cc, conc_range=[min(cc.values()), max(cc.values())], in_band_all=bool(all(inband.values())), n_in_band=int(sum(inband.values())),
                dist_to_hse_median=float(np.median([cc[n] - BAND[n]["hse"] for n in XNAMES])),
                fitted=dict(F=Ff, mean=e["mean"], rms=e["rms"], bins=e["bins"], gate=e["gate"]),
                at_need=dict(F=FT[f]["X"], mean=en["mean"], rms=en["rms"], bins=en["bins"], gate=en["gate"]),
                clash_s=clash_slope(f, key, Ff))

# =================================================================== MUTATE
if MUT:
    MU = {}
    S_ = vmax_sample(FLIM); phi_obs, n_obs = massfn(S_); mids = 0.5 * (BINS[1:] + BINS[:-1])
    for f in A0:
        # M1 flat spectrum: equal cold dark energy per dex of M500 over [13, 15.5], f by the s_f = 1 spectrum (R7-passing) ; host Mb via the bin's median Mb/M500
        sf = 1.0; rho_d = R_NAT * RHO_B; rows = []; bad = 0
        for i in range(len(mids)):
            sel = (np.log10(S_["Mb"]) >= BINS[i]) & (np.log10(S_["Mb"]) < BINS[i + 1])
            if n_obs[i] < 5: continue
            lm5 = float(np.median(S_["lm5"][sel])); fi = float(f_spec(FT[f]["X"], sf, lm5))
            # cold dark energy per dex of M500 -> per dex of Mb (Mb ~ M500 locally, slope 1 assumed)
            n_imp = (rho_d / 2.5) / max(fi * 10 ** mids[i], 1e-30) if 13 <= lm5 <= 15.5 else 0.0
            ratio = n_imp / phi_obs[i]; bad += not (0.5 <= ratio <= 2.0)
            rows.append(dict(lMb=float(mids[i]), n_obs=float(phi_obs[i]), N=int(n_obs[i]), n_implied=n_imp, ratio=ratio))
        MU[f"M1_flat_{f}"] = dict(rows=rows, n_bins_off=bad, bites=bool(bad > 0))
        P(f"[{f}] M1 flat spectrum: per-bin implied/observed " + ", ".join(f"{r['lMb']:.2f}:{r['ratio']:.3g}" for r in rows) + f" -> {bad} bins off x2 -> {'BITES' if bad else 'NO BITE'}")
        # M2 uniform component
        s = KDJ["footings"][f]["setting"]; fu = 0.76 * s["omega_d"] / s["omega_b"]
        MU[f"M2_uniform_{f}"] = dict(f=fu, kd1=FT[f]["cap_f"], diff=fu - FT[f]["cap_f"], fails_field=bool(fu > FT[f]["cap"]), ok=bool(abs(fu - FT[f]["cap_f"]) <= 1e-3 and fu > FT[f]["cap"]))
        P(f"[{f}] M2 uniform component: f = 0.76 omega_d/omega_b = {fu:.4f} vs KD1 {FT[f]['cap_f']:.4f} (|d| {abs(fu - FT[f]['cap_f']):.1e}); > SPARC cap {FT[f]['cap']:.4f}: {fu > FT[f]['cap']} -> {'HOLDS / BITES' if MU[f'M2_uniform_{f}']['ok'] else 'FAIL'}")
        # M3 planted abundance and planted r_f = 0.4 R500
        c = capacity(S_, FT[f]["X"], 1.0); Sp = dict(S_, Vmax=S_["Vmax"] * c["C"]); cp_ = capacity(Sp, FT[f]["X"], 1.0)
        mf = {n: sphere_shape(0.4 * XINFO[n]["r500"]) for n in XNAMES}; g3 = k5_grade(f, "planted", mf)
        MU[f"M3_planted_{f}"] = dict(A_planted=cp_["A"], K3_pass=bool(cp_["A"] <= 2.0), n_in_band=g3["n_in_band"], conc_range=g3["conc_range"], ok=bool(cp_["A"] <= 2.0 and g3["n_in_band"] >= 1))
        P(f"[{f}] M3 planted: abundance x 1/C reads A {cp_['A']:.3f} -> K3 {'PASS' if cp_['A'] <= 2 else 'FAIL'}; planted r_f 0.4 R500 conc {g3['conc_range'][0]:.3f}-{g3['conc_range'][1]:.3f}, in band {g3['n_in_band']}/{len(XNAMES)} -> {'HOLDS' if MU[f'M3_planted_{f}']['ok'] else 'FAIL'}")
    RES["MUTATE"] = MU
    RES["MUTATE_ok"] = bool(all(MU[k]["bites"] for k in MU if k.startswith("M1")) and all(MU[k]["ok"] for k in MU if not k.startswith("M1")))
    P(f"MUTATE all bite / hold: {RES['MUTATE_ok']}"); P("Adopts nothing. kappa = 1/2 FITTED; not theory closed."); dump(); sys.exit(0)

# =================================================================== MAIN: R3/K3
SUM = {}
S0 = vmax_sample(FLIM); phi0, n0 = massfn(S0)
RES["massfn"] = dict(edges_lMb=BINS.tolist(), phi_per_dex=phi0.tolist(), N=n0.tolist(), N_total=S0["N"])
P(f"eRASS1 1/Vmax host baryon mass function (F >= {FLIM:g}e-14, N {S0['N']}): " + ", ".join(f"{0.5*(BINS[i]+BINS[i+1]):.2f}:{phi0[i]:.3g}({n0[i]})" for i in range(len(phi0)) if n0[i]))
# X-COP lower bound (whole sky, 0.04-0.10, h 0.70) vs eRASS1 n(>M500 min X-COP)
Dh = 2.998e5 / 70.0; Vx = 4 / 3 * math.pi * ((Dh * 0.10) ** 3 - (Dh * 0.04) ** 3); nx = 12 / Vx
mmin = min(ETT[n]["M500"] for n in ETT if n != "HydraA") * 1e14
ne = float((1 / S0["Vmax"][S0["lm5"] >= math.log10(mmin)]).sum())
RES["xcop_lower_bound"] = dict(n_ge=nx, M500_min=mmin, eRASS1_n_ge=ne, consistent=bool(ne >= nx))
P(f"X-COP lower bound n(>= {mmin:.2e}) >= {nx:.3g} Mpc^-3 (12 / whole-sky 0.04-0.10); eRASS1 1/Vmax {ne:.3g} -> {'consistent' if ne >= nx else 'eRASS1 BELOW the X-COP bound'}")
for f in A0:
    fX = FT[f]["X"]; xh, xhv = x_hse(f); o = dict(X_HSE=xh, X_HSE_per_cluster=xhv, cells={})
    r7 = R7["footings"][f]["cells"]
    for sf in SGRID:
        c = capacity(S0, fX, sf); fmed = float(f_spec(fX, sf, R7["footings"][f]["median_group_lM500"]))
        ft_ok = bool(FT[f]["g1"] <= fmed <= FT[f]["g0"])
        o["cells"][f"{sf:.2f}"] = dict(**c, f_group_median=fmed, ftable_ok=ft_ok, R7_pass=r7[f"{sf:.2f}"]["R7_pass"], R7=r7[f"{sf:.2f}"])
    ok_s = [sf for sf in SGRID if o["cells"][f"{sf:.2f}"]["R7_pass"] and o["cells"][f"{sf:.2f}"]["ftable_ok"]]
    o["sf_pass_R7_and_ftable"] = ok_s
    best = max(ok_s, key=lambda s_: o["cells"][f"{s_:.2f}"]["C"]) if ok_s else max(SGRID, key=lambda s_: o["cells"][f"{s_:.2f}"]["C"])
    o["best_sf"] = best
    # generous brackets at the best s_f: area, h, F_lim neighbours, X_HSE, extension
    br = {}
    for area in (20626.0, 13116.0):
        for h in (0.674, 0.70, 0.74):
            for Fl in FBR:
                for X in (1.0, xh):
                    for ext in (False, True):
                        Sb = vmax_sample(Fl, area, h); cb = capacity(Sb, fX, best, X, extend=ext)
                        br[f"area{area:g}_h{h}_F{Fl:g}_X{X:.3f}_ext{int(ext)}"] = cb
    gen_k = max(br, key=lambda k: br[k]["C"]); o["brackets"] = br; o["most_generous"] = dict(key=gen_k, **br[gen_k])
    o["theorem_bound_C_max"] = fX / R_NAT
    o["K3_pass"] = bool(br[gen_k]["A"] <= 2.0 and o["cells"][f"{best:.2f}"]["ftable_ok"])
    SUM[f] = o
    cb = o["cells"][f"{best:.2f}"]
    P(f"[{f}] R3/K3: s_f passing R7 + f-table: {ok_s[0] if ok_s else None}-{ok_s[-1] if ok_s else None} per dex; best s_f {best}: f(group median) {cb['f_group_median']:.3f}, "
      f"host baryons in R500 {cb['host_baryons_over_rhob']:.4f} of rho_b, capacity C {cb['C']:.4f} -> needed abundance A = {cb['A']:.1f} x observed; "
      f"most generous ({gen_k}) C {br[gen_k]['C']:.4f}, A {br[gen_k]['A']:.1f}; X_HSE {xh:.3f}; theorem C <= f_X/R = {fX/R_NAT:.3f} -> K3 {'PASS' if o['K3_pass'] else 'FAIL'}")
    P(f"[{f}] R7 at best s_f {best}: pred eps slope {cb['R7']['pred_slope_eps']:+.3f}, A delta 95 % [{cb['R7']['A_delta']['lo95']:+.3f}, {cb['R7']['A_delta']['hi95']:+.3f}], "
      f"B step {cb['R7']['B_step']['median']:+.3f} [{cb['R7']['B_step']['lo95']:+.3f}, {cb['R7']['B_step']['hi95']:+.3f}] -> R7 {'PASS' if cb['R7_pass'] else 'FAIL'}")
RES["R3K3"] = SUM

# =================================================================== MAIN: K5 collapse model + core rule
K5 = {}
for f in A0:
    o = {}
    B = bg(f); o["background"] = B
    for zb in (B["zeq"], 1100.0):
        rows = {}
        for phi in PHIS:
            per = {}; mf = {}
            for n in XNAMES:
                Mc = FT[f]["X"] * mb_r500(n); Mm = Mc * (1 + phi / R_NAT)
                cl = collapse(f, Mm, phi, zb); per[n] = cl; mf[n] = sphere_shape(cl["r_f"] * 1e3)
            g5 = k5_grade(f, f"clump_{phi}_{int(zb)}", mf)
            rf = [per[n]["r_f"] * 1e3 for n in XNAMES]
            core_ok = bool(min(rf) >= 100.0)
            pas = bool(core_ok and g5["in_band_all"] and g5["fitted"]["gate"])
            rows[str(phi)] = dict(Delta_b=per[XNAMES[0]]["Delta_b"], z_ta=[per[n]["z_ta"] for n in XNAMES], r_f_kpc=rf, nu_ta=[per[n]["nu_ta"] for n in XNAMES],
                                  core_rule_ok=core_ok, K5_pass=pas, field_volume_share=1 - phi, **g5)
            zt = [z_ for z_ in rows[str(phi)]["z_ta"] if z_ is not None]
            P(f"[{f}] z_b {zb:.0f} phi {phi}: Delta_b {per[XNAMES[0]]['Delta_b']:.4g}; z_ta {('%.1f-%.1f' % (min(zt), max(zt))) if zt else 'none'}; r_f {min(rf):.3g}-{max(rf):.3g} kpc; "
              f"conc {g5['conc_range'][0]:.3f}-{g5['conc_range'][1]:.3f} (in band {g5['n_in_band']}/{len(XNAMES)}); NA2 gate fitted F {g5['fitted']['F']:.2f} mean {g5['fitted']['mean']:+.3f} rms {g5['fitted']['rms']:.3f} "
              f"bins {','.join('%+.2f' % b['mean'] for b in g5['fitted']['bins'] if b['mean'] is not None)} {'pass' if g5['fitted']['gate'] else 'FAIL'}; core {'ok' if core_ok else 'FAIL'} -> {'PASS' if pas else 'fail'}")
        o[f"zb_{zb:.0f}"] = rows
    zk = f"zb_{B['zeq']:.0f}"
    o["K5_pass"] = bool(any(v["K5_pass"] for v in o[zk].values())); o["K5_pass_phis"] = [p for p, v in o[zk].items() if v["K5_pass"]]
    o["K5_bracket_zb1100_pass_phis"] = [p for p, v in o["zb_1100"].items() if v["K5_pass"]]
    # cored-profile question (reported)
    cq = {}
    for gam in (2, 3):
        for rc in (20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000):
            mf = {n: cored_shape(float(rc), gam) for n in XNAMES}; g5 = k5_grade(f, f"cored_{gam}_{rc}", mf)
            cq[f"g{gam}_rc{rc}"] = dict(gamma=gam, r_c=rc, both=bool(g5["in_band_all"] and g5["fitted"]["gate"]), **g5)
            P(f"[{f}] cored gamma {gam} r_c {rc} kpc: conc {g5['conc_range'][0]:.3f}-{g5['conc_range'][1]:.3f} in band {g5['n_in_band']}/{len(XNAMES)}, d(HSE) {g5['dist_to_hse_median']:+.3f}; "
              f"fitted F {g5['fitted']['F']:.2f} mean {g5['fitted']['mean']:+.3f} rms {g5['fitted']['rms']:.3f} {'pass' if g5['fitted']['gate'] else 'fail'}; at need rms {g5['at_need']['rms']:.3f} {'pass' if g5['at_need']['gate'] else 'fail'}; CLASH-type s {g5['clash_s']:+.3f}")
    o["cored"] = cq; o["cored_pass"] = [k for k, v in cq.items() if v["both"]]
    K5[f] = o
    P(f"[{f}] K5 (z_b = z_eq): {'PASS at phi ' + str(o['K5_pass_phis']) if o['K5_pass'] else 'FAIL at every phi'}; bracket z_b 1100 passing phi: {o['K5_bracket_zb1100_pass_phis']}; cored profiles meeting core rule + band + per-bin: {o['cored_pass']}")
RES["K5"] = K5
both_cored = sorted(set(K5["canonical"]["cored_pass"]) & set(K5["alt"]["cored_pass"]))
RES["cored_both_footings"] = both_cored
P(f"cored profiles meeting core rule + band + NA2 per-bin rule on BOTH footings: {both_cored}")

# =================================================================== labels
LAB = {}
for f in A0:
    rows = dict(K3=SUM[f]["K3_pass"], R7=SUM[f]["cells"][f"{SUM[f]['best_sf']:.2f}"]["R7_pass"], K5=K5[f]["K5_pass"])
    LAB[f] = rows
one = all(all(LAB[f].values()) for f in A0) and SUM["canonical"]["best_sf"] == SUM["alt"]["best_sf"] and set(K5["canonical"]["K5_pass_phis"]) & set(K5["alt"]["K5_pass_phis"])
if one: label = "CANDIDATE ON NC1 ROWS (scoped)"
else:
    misses = {"K3": max(SUM[f]["most_generous"]["A"] for f in A0) if not all(LAB[f]["K3"] for f in A0) else 0}
    failing = [k for k in ("K3", "K5", "R7") if not all(LAB[f][k] for f in A0)]
    label = "FAILS (rows): " + ", ".join(failing) + (f"; binding K3 (needed abundance A >= {min(SUM[f]['most_generous']['A'] for f in A0):.1f} x observed in the most generous bracket)" if "K3" in failing else "")
RES["rows"] = LAB; RES["label"] = label
P(f"\nROWS {json.dumps(LAB)}\nLABEL: {label}")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
dump()
