#!/usr/bin/env python3
"""BG1 (FROZEN_CRITERIA.md d5b23bf2d4): cold-gas conversion key for the K(Q) dust component. TEST lane; adopts nothing.
Dust -> smooth phase at Gamma = alpha rho_cold (T < 1e4 K baryons); retained fraction f = exp(-alpha E), E = int rho_cold dt
along the orbit. alpha scanned over 61 log points in [1e-3, 1e3] (M_sun pc^-3 Gyr)^-1; gates G1-G10 per footing.

    python3 bg1.py expo     -> parts/expo.json       exposures + G1, G1b, G2, G3, G4, G5, G6, G7 on the alpha grid; KA1-KA3; M2
      BG1_ESCALE=10 python3 bg1.py expo  -> parts/expo_x10.json   (KA replay: wrong exposure scale must flip a gate)
      BG1_CATALYST=hot python3 bg1.py expo -> parts/expo_hot.json (M1: catalyst swapped to T > 1e6 K gas)
    python3 bg1.py cosmic   -> parts/cosmic.json     dark ages, neutral IGM, galaxy-hosted cold gas: f_conv(z); G8, G9, G10
      BG1_ESCALE=10 python3 bg1.py cosmic -> parts/cosmic_x10.json
    python3 bg1.py grade    -> bg1.json / bg1.out, bg1_MUTATE.json / bg1_MUTATE.out

Exposure model, as frozen (section "Exposure model"), with the geometric identities used here stated once:
  a parcel at radius r on an isotropic orbit crosses the gas layer twice per orbit, each crossing adds Sigma_cold(r)/v_z;
  N_cross = t_exposed / T_orbit(r), T_orbit = 2 pi r / v_orb, v_z = v_orb / sqrt(3) (isotropic rms vertical component), so
  E(r) = N_cross 2 Sigma / v_z = sqrt(3) t_exposed <Sigma_cold(r)>_t / (pi r), independent of the orbital speed. The same
  identity holds for dispersion-supported hosts (v_orb = sqrt(3) sigma, v_z = sigma).
  Gas history (frozen rule): Sigma_cold(t) = Sigma_cold(0) G(t), G = 1 + (M_*(0) - M_*(t)) / M_gas(0); late types form stars
  at a constant rate over the disc age, so <G>_t = 1 + M_*(0) / (2 M_gas(0)). Quenched classes (gas-rich phase of frozen
  length L, stars formed linearly over it): <M_gas>_t = M_*(0)/2 in an exponential gas disc of scale R_e/1.678.
  Hot ICM / IGrM / ionized IGM / z >= 1100 plasma convert nothing. Clusters keep 1 - s_mem (1 - f_gal), s_mem the member
  (stellar) share of the cluster baryons read from the X-COP stellar-mass profiles (the input MB1 sums), f_gal the SPARC
  disc-weighted retained fraction. Cosmic: dark ages z 20-1100 at the mean baryon density (neutral), neutral mean-density
  IGM z 6-20, galaxy-hosted cold gas from the raw Omega_HI(z) table + the record's CO-based rho_H2(z) fit, summed over the
  GAMA baryonic mass function (AM1), with SPARC's own gas-mass and size relations.
Amount: R = omega_X / omega_b = F1A's R_B2 (5.4096 / 5.4123); f_cap R (KD1's captured share) is a reported reading.
Profiles: galaxy classes use the record's uniform-b convention (dust with the baryons, b = 1 + R f_ret; DX1 / KD1 diagnostic);
X-COP and groups use a cold-collapse (Hernquist) profile M_d(<r) = M_d r^2/(r + a)^2, a = R500/c, c a reported nuisance in [2, 10].
Both footings graded separately, never pooled. Cold dark energy, never dark matter; no particle. Raw data or framework-native
inputs only. One thread, RSS < 1 GB, SIGTERM checkpoint. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, time, signal, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")

T0 = time.time()
CRIT = "d5b23bf2d4"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07"); CL8 = os.path.join(REPO, "closure_2026_11_08")
RB = os.path.join(REPO, "rebuild_2026_10_22"); DATA = os.path.join(REPO, "real_research", "data")
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOTS = ("canonical", "alt")
WHICH = sys.argv[1] if len(sys.argv) > 1 else ""
ESCALE = float(os.environ.get("BG1_ESCALE", "1"))            # KA replay: wrong exposure scale
CATALYST = os.environ.get("BG1_CATALYST", "cold")             # M1: "hot" swaps the catalyst to T > 1e6 K gas
SUFFIX = ("_x10" if ESCALE != 1 else "") + ("_hot" if CATALYST == "hot" else "") + ("_test" if os.environ.get("BG1_TEST") else "") + ("_m3" if os.environ.get("BG1_ALPHAS") else "")
ALPHAS = [float(x) for x in np.logspace(-3, 3, 61)]            # (M_sun pc^-3 Gyr)^-1
if os.environ.get("BG1_TEST"): ALPHAS = [1e-3, 1.0, 100.0, 1e3]   # smoke test only (outputs tagged _test)
if os.environ.get("BG1_ALPHAS"): ALPHAS = [float(x) for x in os.environ["BG1_ALPHAS"].split(",")]   # M3: 10 x best alpha (outputs tagged _m3)
CGRID = [float(x) for x in np.linspace(2.0, 10.0, 17)]         # Hernquist concentration nuisance, X-COP and groups
RES = {}
def P(s=""): print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return o
def dump(name, obj): json.dump(clean(obj), open(os.path.join(PARTS, name), "w"), indent=1)
def on_term(sig, frm):
    dump(f"{WHICH}{SUFFIX}_partial.json", RES); P("SIGTERM: partial checkpoint written"); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}; a = sys.argv; sys.argv = [path]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns

# ------------------------------------------------------------------ record inputs (read-only)
F1A = json.load(open(os.path.join(CL7, "F1A_primary_cmb_audit", "f1a.json")))
RF = {f: float(F1A[f]["R_B2"]) for f in FOOTS}                               # omega_X / omega_b, the CMB's amount
KD1J = json.load(open(os.path.join(CL6, "KD1_unpinned_kq_dust", "kd1.json")))
FCAPR = {f: float(KD1J["footings"][f]["uniform_f_diag"]["capture_f"]) for f in FOOTS}   # f_cap R (reported reading)
Q15 = json.load(open(os.path.join(CL6, "QX15_cmb_primary_likelihood", "qx15.json")))
THETA = {f: dict(Q15["footings"][f]["main"]["theta"], h=Q15["footings"][f]["main"]["h"]) for f in FOOTS}
ST1 = json.load(open(os.path.join(CL6, "ST1_multi_cause_step", "st1.json")))
M31_TARGET = {f: ST1["footings"][f]["remaining"]["dSph bright M31"] for f in FOOTS}    # residual +0.214 / +0.201, ci
M31_DROP = ("Andromeda I", "Andromeda XVII", "Andromeda XIX", "Andromeda XXV", "And I", "And XVII", "And XIX", "And XXV")
A0H = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}   # QX5 / GB1 A0 (kappa 1/2)

# physical constants / units
G_KPC = 4.30091e-6          # kpc (km/s)^2 / Msun
MPC_GYR_C = 306.601         # c in Mpc / Gyr
RHO_CRIT_H2 = 2.77536627e11 # Msun / Mpc^3 per h^2
SQ3PI = math.sqrt(3.0) / math.pi
# the record's H2 rule (U1 N6 / UX5 Milky Way gas model, McMillan 2017 forms): Sigma_H2(8.33 kpc) = 2.0 Msun/pc^2 against the
# stellar discs Sigma_*(8.33) = 896 e^{-8.33/2.5} + 183 e^{-8.33/3.02}; here H2 rides on the bulge + disc stellar surface density
# at that ratio (rebuild_2026_10_22/U1_v3_dust_content/u1_v3_dust_content.py, block N6; UX5_mw_stellar_mass/README.md).
F_MOL = 2.0 / (896.0 * math.exp(-8.33 / 2.5) + 183.0 * math.exp(-8.33 / 3.02))
# frozen class lengths (Gyr) of the gas-rich phase
PHASE = {"ellipticals": 2.0, "LG field": 3.0, "bright M31": 4.0, "MW classical": 4.0, "coma_udg": 4.0}
Z_DISC = 2.0                # disc age = lookback time to z 2 on the footing background (declared)
Z_HOT = 2.0                 # clusters hot since z 2 (M1 only)
Z_REION = 6.0               # neutral mean-density IGM between z 6 and 20
Z_DARK = (20.0, 1100.0)
# raw Omega_HI(z) (DLA / 21 cm measurements, transcribed; PROVISIONAL per the record's look-up rule): z 0 ALFALFA (Jones+2018),
# z 0.6 / 1.2 MgII-DLA (Rao+2017), z 2.3 SDSS DLA (Noterdaeme+2012), z 3.1 / 4.0 (Crighton+2015), z 5 (Prochaska & Wolfe 2009 trend)
OMEGA_HI_TAB = [(0.0, 3.9e-4), (0.6, 4.7e-4), (1.2, 6.0e-4), (2.3, 1.0e-3), (3.1, 1.1e-3), (4.0, 1.2e-3), (5.0, 1.2e-3)]
def rho_H2_comoving(z):     # CO-based fit as the record transcribed it (campaign_fresh_gravity/CFG632_frb_dm_variance/cfg632_predict.py)
    return 5.3e6 * ((1 + z) ** 3.6) / (1 + ((1 + z) / 2.1) ** 5.9)   # Msun / Mpc^3
def omega_HI(z):
    zz, oo = zip(*OMEGA_HI_TAB); return float(np.interp(z, zz, oo))
def hern(r, a): return r * r / (r + a) ** 2
def glaw_np(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN * gN + a0 * gN)

class Background:
    """Footing background from QX15's fit through CLASS: t(z) in Gyr, H(z) in 1/Gyr, rho_b0 in Msun/pc^3 (physical, z = 0)."""
    def __init__(self, f):
        from classy import Class
        th = THETA[f]; self.h = th["h"]; self.ob = th["omega_b"]; self.od = th["omega_d"]
        M = Class(); M.set({'output': '', 'h': self.h, 'omega_b': self.ob, 'omega_cdm': self.od, 'N_ur': 3.046, 'T_cmb': 2.7255}); M.compute()
        self.lz = np.linspace(0, math.log10(1e9 + 1), 4001); zz = 10 ** self.lz - 1
        self.Hz = np.array([M.Hubble(z) for z in zz]) * MPC_GYR_C          # 1/Gyr
        self.rho_b0 = self.ob * RHO_CRIT_H2 / 1e18                           # Msun/pc^3
        self.rho_crit0 = RHO_CRIT_H2 * self.h ** 2                           # Msun/Mpc^3
        M.struct_cleanup(); M.empty()
    def H(self, z): return float(np.interp(math.log10(1 + z), self.lz, self.Hz))
    def lookback(self, z, n=4000):
        zz = np.linspace(0, z, n + 1); return float(np.trapz(1.0 / ((1 + zz) * np.array([self.H(x) for x in zz])), zz))
    def expo_mean_density(self, z1, z2, n=6000):
        """int_{z1}^{z2} rho_b0 (1+z)^3 dt  (Msun pc^-3 Gyr), log-spaced in 1+z."""
        u = np.linspace(math.log(1 + z1), math.log(1 + z2), n + 1); z = np.exp(u) - 1
        f = self.rho_b0 * (1 + z) ** 3 / np.array([self.H(x) for x in z])       # d t / d ln(1+z) = 1/H
        return float(np.trapz(f, u))

# ================================================================== SPARC exposures (QX8 galaxies, exact-field T carried)
def sparc_setup():
    sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field"))
    a = sys.argv; sys.argv = [a[0]]
    with contextlib.redirect_stdout(io.StringIO()):
        import qx8 as Q8
    sys.argv = a
    return Q8

def sparc_exposure(Q8, GALS, t_disc):
    """Per galaxy: Sigma_cold(r) today (HI x 1.33 from Vgas + H2 rule), <G>, E(r) at the rotation-curve radii (M_sun pc^-3 Gyr),
    baryon weights for the enclosed mean, Sigma_cold(2.2 h). Frozen model; ESCALE multiplies E (KA replay only)."""
    out = []
    for q in GALS:
        R = q["R"]; m = q["meta"]
        Mg = np.sign(q["Vgas"]) * q["Vgas"] ** 2 * R / G_KPC                       # spherical-equivalent enclosed gas (Msun)
        dM = np.gradient(Mg, R) if len(R) > 1 else np.array([Mg[0] / R[0]])
        sig_hi = np.maximum(dM / (2 * math.pi * R), 0.0) / 1e6                      # Msun / pc^2 (helium included: SPARC's 1.33)
        sig_h2 = F_MOL * (0.5 * q["SBd"] + 0.7 * q["SBb"])                          # H2 rule on the bulge + disc stellar discs
        sig = sig_hi + sig_h2
        Ms = 0.5 * m["L36"] * 1e9                                                   # stars (Upsilon 0.5 disc)
        MH2 = float(np.trapz(2 * math.pi * R * 1e3 * sig_h2, R * 1e3)) if len(R) > 1 else 0.0
        Mgas0 = max(1.33 * m["MHI"] * 1e9 + MH2, 0.02 * Ms)                        # floor: the rule needs M_gas(0) > 0
        Gbar = 1.0 + Ms / (2 * Mgas0)                                               # <G>_t, constant SFR over the disc age
        E = ESCALE * SQ3PI * t_disc * Gbar * sig / (R * 1e3)                        # Msun pc^-3 Gyr
        # baryon weights for the enclosed mean (Upsilon 0.5 / 0.7 mass profile)
        VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mb = np.maximum.accumulate(np.clip(VB2 * R / G_KPC, 0, None)); dMb = np.diff(np.concatenate([[0.0], Mb]))
        dMb = np.maximum(dMb, 0.0); cum = np.cumsum(dMb)
        s22 = float(np.interp(2.2 * m["Rdisk"], R, sig)) if m["Rdisk"] > 0 else float("nan")
        out.append(dict(name=q["name"], R=R, sig_hi=sig_hi, sig_h2=sig_h2, sig=sig, E=E, dMb=dMb, cumMb=cum, Gbar=Gbar, Ms=Ms, Mgas0=Mgas0,
                        MHI=1.33 * m["MHI"] * 1e9, MH2=MH2, sig22=s22, lowdens=bool(np.isfinite(s22) and s22 < 10.0), Rdisk=m["Rdisk"]))
    return out

def fbar_enclosed(ex, alpha, maxexp=False):
    """M_b-weighted mean retained fraction inside each radius (uniform-b: the dust rides with the enclosed baryons).
    maxexp: generous reading, every parcel at r credited with the largest exposure inside r (eccentric orbits)."""
    E = np.maximum.accumulate(ex["E"]) if maxexp else ex["E"]
    f = np.exp(-alpha * E); num = np.cumsum(f * ex["dMb"]); den = np.maximum(ex["cumMb"], 1e-30)
    return np.where(ex["cumMb"] > 0, num / den, f)

# ================================================================== expo: galaxy-class gates on the alpha grid
def run_expo():
    from astropy.io import fits
    Q8 = sparc_setup(); GALS = Q8.load_sparc(); Q8J = json.load(open(os.path.join(CL6, "QX8_sparc_exact_field", "qx8.json")))
    GB = load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
    GBJ = json.load(open(os.path.join(CL6, "GB1_all_gates_battery", "gb1.json")))
    DX1J = json.load(open(os.path.join(CL6, "DX1_disc_only_exclusion", "dx1.json")))
    G, MS, KPC, PC = GB["G"], GB["MS"], GB["KPC"], GB["PC"]; XC, SP, EL, GR = GB["XC"], GB["SP"], GB["EL"], GB["GR"]
    glaw = GB["glaw"]; LE = GB["NS"]["lensing"]()
    R500 = {}; GASP = {}
    for name in sorted({z["name"] for z in XC}):
        with fits.open(os.path.join(GB["DATA"], "xcop", name, f"{name}_fgas_profile.fits")) as h:
            R500[name] = float(h[1].header["R500"]); gas = h[1].data.copy()
            GASP[name] = (np.array(gas["RADIUS"], float) * R500[name], np.array(gas["MGAS"], float))
    lU, lN = np.log(Q8.UPS), np.log(Q8.NODES); ACC = 1e6 / Q8.KPC_S
    # QX8 per-galaxy exact-field T at every Upsilon, and the per-unit-ratio dust acceleration (uniform-b: ratio multiplies g_b)
    PRE = {f: [np.array([np.interp(lU, lN, T[:, j]) for j in range(T.shape[1])]) for T in
               (np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False)["T"] for i in range(len(GALS)))] for f in FOOTS}
    def fit_stats(q, lgp):
        """QX8's fit_one plus the weighted mean residual at the chosen Upsilon."""
        OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); i = int(np.argmin(wr2 / np.maximum(ws, 1e-300)))
        return wr2[i], wr[i], ws[i], i
    def sparc_eval(f, bfac_list, tmode="T"):
        a0 = Q8.FOOT[f]; rows = []
        for q, Tf, bf in zip(GALS, PRE[f], bfac_list):
            lg = np.log10(np.maximum(glaw_np(q["GB"] * bf[:, None], a0), 1e-300)) + (Tf if tmode == "T" else 0.0)
            rows.append(fit_stats(q, lg))
        return rows
    def pooled(rows, sel=None):
        idx = range(len(rows)) if sel is None else sel
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx)
        return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws), U_median=float(np.median([Q8.UPS[rows[i][3]] for i in idx])), n=len(list(idx)))
    # GB1 point sets, per-point candidate b through GB1's own delta formula
    def delta_b(b, ft, a0h):
        gN = GB["need"](ft, "x") * a0h; gNb = b * gN; return math.log10(glaw(gNb, a0h) / glaw(gN, a0h))
    def xcop_eval(a0h, amount, c, fcl, uniform=False):
        d = []
        for z in XC:
            rm = z["r_kpc"] * KPC; Ml = z["Mb_last"][0]
            md = amount * fcl[z["name"]] * (z["M_b"] if uniform else Ml * hern(z["r_kpc"], R500[z["name"]] / c))
            Mp = glaw(G * (z["M_b"] + md) * MS / rm ** 2, a0h) * rm ** 2 / G / MS; d.append(math.log10(z["M_obs"] / Mp))
        d = np.array(d); return dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())))
    def groups_eval(a0h, amount, c, fret_of_fst):
        o = {}
        for fst in (0, 1):
            npass = 0; med = []
            for gp in GR:
                Mbt = gp["g5"] * (1 + fst); ok = True
                for p in gp["pts"]:
                    rm = p["r_kpc"] * KPC; Mb = p["M_gas"] * (1 + fst); md = amount * fret_of_fst[fst] * Mbt * hern(p["r_kpc"], gp["R5"] / c)
                    Mp = glaw(G * (Mb + md) * MS / rm ** 2, a0h) * rm ** 2 / G / MS; dl = math.log10(p["M_obs"] / Mp); med.append(dl)
                    ok &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
                npass += ok
            o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)))
        return o
    def lens_mean(a0h, md_of_lm):
        d = []
        for p in LE:
            Mb = p["Mb"] / MS; r = math.sqrt(G * p["Mb"] / p["gbar"]); md = md_of_lm(math.log10(Mb), r / KPC)
            gp = glaw(p["gbar"] + G * md * MS / r ** 2, a0h); d.append(math.log10(p["gobs"] / gp))
        return float(np.mean(d))
    # quenched-class exposure: E(r) = sqrt(3) L <Sigma>(r) / (pi r), <M_gas> = M_*/2, exponential gas disc R_g = r_half / 1.678
    def quenched_fret(alpha, Ms, rhalf_pc, L, catalyst=CATALYST):
        if catalyst == "hot": return 1.0          # no hot gas catalogued in these hosts
        Rg = rhalf_pc / 1.678; rr = np.linspace(0.02, 12.0, 600) * Rg
        sig = (0.5 * Ms) / (2 * math.pi * Rg ** 2) * np.exp(-rr / Rg); E = ESCALE * SQ3PI * L * sig / rr
        w = rr * np.exp(-rr / Rg); return float(np.trapz(w * np.exp(-alpha * E), rr) / np.trapz(w, rr))
    for f in FOOTS:
        a0h = A0H[f]; Rf = RF[f]; bg = Background(f); t_disc = bg.lookback(Z_DISC); t_hot = bg.lookback(Z_HOT)
        EX = sparc_exposure(Q8, GALS, t_disc)
        if CATALYST == "hot":
            for ex in EX: ex["E"] = np.zeros_like(ex["E"])      # discs carry no T > 1e6 K gas in SPARC
        exn = {ex["name"]: ex for ex in EX}
        R_ = {}; RES[f] = R_
        R_["inputs"] = dict(R=Rf, fcapR=FCAPR[f], a0=a0h, t_disc_Gyr=t_disc, t_hot_Gyr=t_hot, F_MOL=F_MOL, ESCALE=ESCALE, catalyst=CATALYST,
                            sparc_n=len(EX), sparc_lowdens_n=int(sum(ex["lowdens"] for ex in EX)),
                            E_sparc_median_at_2p2h=float(np.nanmedian([np.interp(2.2 * ex["Rdisk"], ex["R"], ex["E"]) for ex in EX if ex["Rdisk"] > 0])),
                            E_sparc_massweighted_median=float(np.median([float(np.sum(ex["E"] * ex["dMb"]) / max(ex["cumMb"][-1], 1e-30)) for ex in EX])),
                            Gbar_median=float(np.median([ex["Gbar"] for ex in EX])), MH2_over_MHI_median=float(np.median([ex["MH2"] / max(ex["MHI"], 1) for ex in EX])))
        # ---- GB1 battery pieces
        S, E_, X = GB["build"](f, a0h); U = GB["udgs"](f, a0h); D = GB["dsphs"](f, a0h)
        st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
        # SPARC (GB1 set) point -> (name, r_kpc) in build order
        skeys = [(g["name"], g["R"][i] / KPC) for g in SP for i in range(len(g["R"]))]; assert len(skeys) == len(S)
        # member share of the cluster baryons (stellar fraction at the outermost graded radius; MB1's input profiles)
        smem = {}
        for z in XC:
            smem.setdefault(z["name"], []).append((z["r_kpc"], 1.0 - z["M_gas"] / z["M_b"]))
        smem = {n: max(v)[1] for n, v in smem.items()}
        R_["member_share_xcop"] = smem
        # hot-catalyst exposures (M1): ICM at the graded radii, and the T > 1e6 K primordial plasma (z 3.67e5 .. 3.7e8)
        E_icm = {}
        if CATALYST == "hot":
            zT6 = 1e6 / 2.7255 - 1; zBBN = 1e9 / 2.7255 - 1
            E_plasma = ESCALE * bg.expo_mean_density(zT6, zBBN)
            for z in XC:
                gr, gM = GASP[z["name"]]; rho = np.gradient(gM, gr) / (4 * math.pi * gr ** 2) / 1e9     # Msun/pc^3
                E_icm[(z["name"], z["r_kpc"])] = ESCALE * t_hot * max(float(np.interp(z["r_kpc"], gr, rho)), 0.0)
            R_["inputs"]["E_plasma_T_gt_1e6K"] = E_plasma; R_["inputs"]["E_icm_median"] = float(np.median(list(E_icm.values())))
        # ---- known answers
        ka = {}
        rows0 = sparc_eval(f, [np.ones(len(q["R"])) for q in GALS]); p0 = pooled(rows0); rx = Q8J["footings"][f].get("exact", Q8J["footings"][f].get("st_ex", {}))
        ka["KA2_qx8_law"] = dict(rms=p0["rms"], U=p0["U_median"], qx8_rms=rx["rms"], qx8_U=rx["U_median"], pass_=bool(abs(p0["rms"] - rx["rms"]) <= 1e-6 and abs(p0["U_median"] - rx["U_median"]) <= 1e-6))
        L0 = GBJ["cands"]["L0"][f]
        res_S0 = np.array([p["D"] for p in S]); Z0 = float(res_S0.mean()); rms0 = float(np.sqrt((res_S0 ** 2).mean()))
        x0 = xcop_eval(a0h, 0.0, 5.0, {n: 1.0 for n in R500}); e0 = float(np.mean([p["D"] for p in E_])); u0 = float(np.mean([p["D"] for p in U]))
        g0 = groups_eval(a0h, 0.0, 5.0, {0: 1.0, 1: 1.0})
        ka["KA1_gb1_L0"] = dict(d_sparc=max(abs(Z0 - L0["G1 SPARC"]["num"]["Z"]), abs(rms0 - L0["G1 SPARC"]["num"]["rms"])), d_xcop=max(abs(x0["mean"] - L0["G2 X-COP"]["num"]["mean"]), abs(x0["rms"] - L0["G2 X-COP"]["num"]["rms"])),
                                d_ell=abs(e0 - L0["G4 ellipticals"]["num"]["mean"]), d_udg=abs(u0 - L0["G5 Coma UDGs"]["num"]["mean"]),
                                d_groups=max(abs(g0["fst0"]["n_pass"] - L0["G3 groups"]["num"]["fst0"]["n_pass"]), abs(g0["fst0"]["median_res"] - L0["G3 groups"]["num"]["fst0"]["median_res"])))
        ka["KA1_gb1_L0"]["pass_"] = bool(all(v <= 1e-6 for k, v in ka["KA1_gb1_L0"].items() if k != "pass_"))
        # KA3: uniform-b at KD1's f_cap R reproduces DX1 O1's X-COP, ellipticals, UDG cells (the hot set at full retention)
        o1 = DX1J["footings"][f]["rows"]["O1"]
        xu = xcop_eval(a0h, FCAPR[f], 5.0, {n: 1.0 for n in R500}, uniform=True)
        eu = float(np.mean([p["D"] - delta_b(1 + FCAPR[f], p["feat"], a0h) for p in E_])); uu = float(np.mean([p["D"] - delta_b(1 + FCAPR[f], p["feat"], a0h) for p in U]))
        def o1num(g):
            try: return o1[g]["num"]
            except Exception: return None
        ref = dict(x=o1num("G2 X-COP"), e=o1num("G4 ellipticals"), u=o1num("G5 Coma UDGs")) if o1 else None
        if ref and ref["x"] and ref["e"] and ref["u"]:
            d3 = max(abs(xu["mean"] - ref["x"]["mean"]), abs(xu["rms"] - ref["x"]["rms"]), abs(eu - ref["e"]["mean"]), abs(uu - ref["u"]["mean"]))
            ka["KA3_dx1_O1"] = dict(xcop=[xu["mean"], xu["rms"]], ell=eu, udg=uu, dx1=[ref["x"]["mean"], ref["x"]["rms"], ref["e"]["mean"], ref["u"]["mean"]], maxd=d3, pass_=bool(d3 <= 1e-6))
        else:
            ka["KA3_dx1_O1"] = dict(xcop=[xu["mean"], xu["rms"]], ell=eu, udg=uu, dx1="not found in dx1.json (reported only)", pass_=True)
        R_["KA"] = ka
        for k, v in ka.items(): P(f"[{f}] {k}: {'PASS' if v['pass_'] else 'FAIL'}  " + json.dumps(clean({a: b for a, b in v.items() if a != 'pass_'}))[:300])
        if not all(v["pass_"] for v in ka.values()):
            P(f"[{f}] KA FAIL: stop"); continue
        # ---- law-only baselines for the shift lines
        base = dict(sparc=pooled(rows0), sparc_lowdens=pooled(rows0, [i for i, ex in enumerate(EX) if ex["lowdens"]]), lens=lens_mean(a0h, lambda lm, r: 0.0))
        R_["baselines"] = base
        # per-class quenched exposures (alpha-independent inputs)
        ellq = {e["name"]: (e["Mbar"](1e9), e["Re"] * 1e3) for e in EL}
        udgq = {(p["feat"]["Mb"], p["feat"]["r"]): (p["feat"]["Mb"], p["feat"]["r"] / PC) for p in U}       # r = 4/3 Re (GB1), in pc
        dq = {}
        for cls in D:
            for p in D[cls]:
                xr = GB["X1R"].get((f, p["name"]))
                dq[p["name"]] = (10 ** float(xr["logMstar"]), float(xr["rh_pc"])) if xr is not None else None
        # KiDS lens-bin disc exposure: SPARC galaxies within 0.3 dex of the bin's stellar mass (0.5 dex if fewer than 3)
        lmbins = sorted({round(math.log10(p["Mb"] / MS), 3) for p in LE}); lensgal = {}
        for lm in lmbins:
            for wid in (0.3, 0.5, 1.0):
                sel = [ex for ex in EX if abs(math.log10(ex["Ms"]) - lm) <= wid]
                if len(sel) >= 3: break
            lensgal[lm] = sel
        R_["lens_bins"] = {str(lm): [ex["name"] for ex in sel] for lm, sel in lensgal.items()}
        # M31 equilibrium subset (ST1: the four most tidally exposed dropped)
        m31 = D["bright M31"]; m31_sub = [p for p in m31 if p["name"] not in M31_DROP]
        R_["m31_subset_n"] = len(m31_sub); tgt = M31_TARGET[f]; sig_m31 = (tgt["ci"][1] - tgt["ci"][0]) / (2 * 1.959964)
        R_["m31_target"] = dict(step=tgt["residual"], ci=tgt["ci"], sigma=sig_m31)
        grid = []
        for ia, alpha in enumerate(ALPHAS):
            row = dict(alpha=alpha)
            # SPARC: enclosed retained fraction per galaxy
            FB = [fbar_enclosed(ex, alpha) for ex in EX]; FBmax = [fbar_enclosed(ex, alpha, True) for ex in EX]
            fgal = {ex["name"]: fb for ex, fb in zip(EX, FB)}
            fdisc = {ex["name"]: float(fb[-1]) for ex, fb in zip(EX, FB)}          # whole-disc retained fraction
            rows = sparc_eval(f, [1.0 + Rf * fb for fb in FB]); pa = pooled(rows); pb = pooled(rows, [i for i, ex in enumerate(EX) if ex["lowdens"]])
            g1 = bool(pa["rms"] <= base["sparc"]["rms"] + 0.010 and abs(pa["mean"]) <= 0.05)
            g1b = bool(pb["rms"] <= base["sparc_lowdens"]["rms"] + 0.010 and abs(pb["mean"]) <= 0.05)
            rowsm = sparc_eval(f, [1.0 + Rf * fb for fb in FBmax]); pm = pooled(rowsm)
            row["G1"] = dict(status="PASS" if g1 else "FAIL", **pa, rms_line=base["sparc"]["rms"] + 0.010, fdisc_median=float(np.median(list(fdisc.values()))),
                             maxexp=dict(rms=pm["rms"], mean=pm["mean"], pass_=bool(pm["rms"] <= base["sparc"]["rms"] + 0.010 and abs(pm["mean"]) <= 0.05)))
            row["G1b"] = dict(status="PASS" if g1b else "FAIL", **pb, rms_line=base["sparc_lowdens"]["rms"] + 0.010,
                              fdisc_median=float(np.median([fdisc[ex["name"]] for ex in EX if ex["lowdens"]])))
            # KiDS lenses (G2): the lens galaxy's dust rides with its baryons at the disc-weighted retention of its mass bin
            fl = {lm: float(np.median([fdisc[ex["name"]] for ex in sel])) for lm, sel in lensgal.items()}
            def md_of(lm, r, fl=fl): return Rf * 10 ** lm * fl[min(fl, key=lambda k: abs(k - lm))]
            Lm = lens_mean(a0h, md_of); shift = Lm - base["lens"]
            row["G2"] = dict(status="PASS" if abs(shift) <= 0.05 else "FAIL", shift=shift, f_lens={str(k): v for k, v in fl.items()})
            # cluster / group retention: hot ICM converts nothing; members' own halos convert as discs
            fgal_mean = float(np.mean(list(fdisc.values())))
            if CATALYST == "hot":
                fcl = {n: math.exp(-alpha * (R_["inputs"]["E_plasma_T_gt_1e6K"] + float(np.mean([E_icm[k] for k in E_icm if k[0] == n])))) for n in R500}
                fgrp = {0: math.exp(-alpha * R_["inputs"]["E_plasma_T_gt_1e6K"]), 1: math.exp(-alpha * R_["inputs"]["E_plasma_T_gt_1e6K"])}
            else:
                fcl = {n: 1.0 - smem[n] * (1.0 - fgal_mean) for n in R500}
                fgrp = {0: 1.0, 1: 1.0 - 0.5 * (1.0 - fgal_mean)}             # f* = 1: half the baryons are member stars
            xc = {c: xcop_eval(a0h, Rf, c, fcl) for c in CGRID}; xpass = [c for c in CGRID if abs(xc[c]["mean"]) <= 0.05 and xc[c]["rms"] <= 0.10]
            cbest = min(CGRID, key=lambda c: (0 if c in xpass else 1, xc[c]["rms"])); xcap = xcop_eval(a0h, FCAPR[f], cbest, fcl)
            row["G3"] = dict(status="PASS" if xpass else "FAIL", c_best=cbest, **xc[cbest], c_pass=xpass, f_cluster_mean=float(np.mean(list(fcl.values()))),
                             at_fcapR=xcap, uniform_b=xcop_eval(a0h, Rf, cbest, fcl, uniform=True))
            gg = {c: groups_eval(a0h, Rf, c, fgrp) for c in CGRID}; gpass = [c for c in CGRID if all(gg[c][k]["n_pass"] >= 16 for k in gg[c])]
            cg = cbest if cbest in gpass or not gpass else gpass[0]
            row["G4"] = dict(status="PASS" if gpass else "FAIL", c=cg, **gg[cg], c_pass=gpass, f_group={str(k): v for k, v in fgrp.items()}, at_c_best_xcop=gg[cbest])
            # UDGs (G5): per galaxy f_ret from its own gas-rich phase (4 Gyr ending at infall z 1)
            fu = {k: quenched_fret(alpha, v[0], v[1], PHASE["coma_udg"]) for k, v in udgq.items()}
            ru = np.array([p["D"] - delta_b(1 + Rf * fu[(p["feat"]["Mb"], p["feat"]["r"])], p["feat"], a0h) for p in U]); mu = float(ru.mean())
            row["G5"] = dict(status="PASS" if abs(mu) <= 2 * sigU else "FAIL", mean=mu, sigma_U=sigU, z=mu / sigU, f_udg_mean=float(np.mean(list(fu.values()))),
                             need_f_ret_for_zero=None)
            # SPARC anchor on GB1's set with the same candidate (b = 1 + R fbar(<r) by galaxy and radius)
            bS = []
            for (nm, rk) in skeys:
                ex = exn.get(nm)
                bS.append(1.0 + Rf * (float(np.interp(rk, ex["R"], fgal[nm])) if ex is not None else 1.0))
            resS = np.array([p["D"] - delta_b(b, p["feat"], a0h) for p, b in zip(S, bS)]); anchor = float(resS.mean())
            # dSph classes (G6)
            def cls_res(pts, L):
                out = []
                for p in pts:
                    q = dq.get(p["name"]); fr = quenched_fret(alpha, q[0], q[1], L) if q else 1.0
                    out.append(p["D"] - delta_b(1 + Rf * fr, p["feat"], a0h))
                return np.array(out)
            rng = np.random.default_rng(21)
            def boot_ci(v):
                bs = np.median(v[rng.integers(0, len(v), (10000, len(v)))], axis=1); lo, hi = np.percentile(bs, [2.5, 97.5]); return [float(lo - anchor), float(hi - anchor)]
            rlg = cls_res(D["LG field"], PHASE["LG field"]); rm31 = cls_res(m31, PHASE["bright M31"]); rm31s = cls_res(m31_sub, PHASE["bright M31"]); rmw = cls_res(D["MW classical"], PHASE["MW classical"])
            lg_mean = float(rlg.mean() - anchor); m31_stat = float(np.median(rm31s) - anchor)
            g6_lg = bool(abs(lg_mean) <= 0.10); g6_m31 = bool(abs(m31_stat) <= 2 * sig_m31)
            flg = float(np.mean([quenched_fret(alpha, dq[p["name"]][0], dq[p["name"]][1], PHASE["LG field"]) for p in D["LG field"] if dq.get(p["name"])]))
            fm31 = float(np.mean([quenched_fret(alpha, dq[p["name"]][0], dq[p["name"]][1], PHASE["bright M31"]) for p in m31 if dq.get(p["name"])]))
            row["G6"] = dict(status="PASS" if (g6_lg and g6_m31) else "FAIL", anchor=anchor,
                             LG_field=dict(pass_=g6_lg, mean_minus_anchor=lg_mean, median_minus_anchor=float(np.median(rlg) - anchor), ci=boot_ci(rlg), f_ret_mean=flg, N=len(rlg)),
                             bright_M31=dict(pass_=g6_m31, stat_subset=m31_stat, line=2 * sig_m31, full_median_minus_anchor=float(np.median(rm31) - anchor), ci_full=boot_ci(rm31), f_ret_mean=fm31, N_subset=len(rm31s)),
                             MW_classical_reported=dict(median_minus_anchor=float(np.median(rmw) - anchor), ci=boot_ci(rmw)))
            # ellipticals (G7): both readings
            fe = {n: quenched_fret(alpha, v[0], v[1], PHASE["ellipticals"]) for n, v in ellq.items()}; fem = float(np.mean(list(fe.values())))
            re1 = float(np.mean([p["D"] - delta_b(1 + Rf * fe[p["name"]], p["feat"], a0h) for p in E_]))
            re2 = float(np.mean([p["D"] - delta_b(GB["b_imf"](p["feat"]) * (1 + Rf * fe[p["name"]]), p["feat"], a0h) for p in E_]))
            row["G7"] = dict(status="PASS" if (fem <= 0.1 or fem >= 0.9) else "FAIL", f_ret_mean=fem, reading=("IMF (f_ret <= 0.1)" if fem <= 0.1 else ("HX1 B 4.2 (f_ret >= 0.9)" if fem >= 0.9 else "neither")),
                             gb1_G4_mean_plain=re1, gb1_G4_mean_imf=re2)
            grid.append(row); R_["grid"] = grid
            if ia % 5 == 0 or ia == len(ALPHAS) - 1:
                P(f"[{f}] alpha {alpha:8.3g}: G1 {row['G1']['status'][0]} rms {pa['rms']:.4f} mean {pa['mean']:+.3f} fdisc {row['G1']['fdisc_median']:.3f} | G1b {row['G1b']['status'][0]} {pb['rms']:.4f}/{pb['mean']:+.3f} "
                  f"| G2 {row['G2']['status'][0]} {shift:+.3f} | G3 {row['G3']['status'][0]} c {cbest:g} {xc[cbest]['mean']:+.3f}/{xc[cbest]['rms']:.3f} fcl {row['G3']['f_cluster_mean']:.3f} | G4 {row['G4']['status'][0]} {gg[cg]['fst0']['n_pass']}/{gg[cg]['fst1']['n_pass']} "
                  f"| G5 {row['G5']['status'][0]} {mu:+.3f} ({mu/sigU:+.2f}s) f {row['G5']['f_udg_mean']:.3f} | G6 {row['G6']['status'][0]} LG {lg_mean:+.3f} (f {flg:.3f}) M31 {m31_stat:+.3f} (f {fm31:.3f}) | G7 {row['G7']['status'][0]} f {fem:.3f}  [{time.time()-T0:.0f}s {rss():.2f}GB]")
                dump(f"expo{SUFFIX}_partial.json", RES)
        # M2 (alpha -> 0): the full component in galaxies
        FB0 = [np.ones(len(ex["E"])) for ex in EX]; rows = sparc_eval(f, [1.0 + Rf * fb for fb in FB0]); p2 = pooled(rows)
        L2 = lens_mean(a0h, lambda lm, r: Rf * 10 ** lm)
        R_["M2_alpha0"] = dict(G1=dict(rms=p2["rms"], mean=p2["mean"], line=base["sparc"]["rms"] + 0.010, fail=bool(not (p2["rms"] <= base["sparc"]["rms"] + 0.010 and abs(p2["mean"]) <= 0.05))),
                               G2=dict(shift=L2 - base["lens"], fail=bool(abs(L2 - base["lens"]) > 0.05)))
        R_["M2_alpha0"]["bites"] = bool(R_["M2_alpha0"]["G1"]["fail"] and R_["M2_alpha0"]["G2"]["fail"])
        P(f"[{f}] M2 alpha 0: G1 rms {p2['rms']:.4f} mean {p2['mean']:+.3f} (line {base['sparc']['rms']+0.01:.4f}); G2 shift {L2-base['lens']:+.3f} -> {'BITES' if R_['M2_alpha0']['bites'] else 'NO BITE'}")
        # per-galaxy exposure table (reported)
        R_["sparc_table"] = [dict(name=ex["name"], Ms=ex["Ms"], Mgas0=ex["Mgas0"], Gbar=ex["Gbar"], sig22=ex["sig22"], lowdens=ex["lowdens"],
                                  E_massweighted=float(np.sum(ex["E"] * ex["dMb"]) / max(ex["cumMb"][-1], 1e-30)), E_at_2p2h=float(np.interp(2.2 * ex["Rdisk"], ex["R"], ex["E"])) if ex["Rdisk"] > 0 else None) for ex in EX]
        R_["quenched_inputs"] = dict(ellipticals={n: dict(Ms=v[0], rhalf_pc=v[1]) for n, v in ellq.items()},
                                     udg_n=len(udgq), dsph={cls: [dict(name=p["name"], Ms=dq[p["name"]][0], rh_pc=dq[p["name"]][1]) for p in D[cls] if dq.get(p["name"])] for cls in ("LG field", "bright M31", "MW classical")})
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; RES["criteria"] = CRIT; RES["alphas"] = ALPHAS; RES["cgrid"] = CGRID
    dump(f"expo{SUFFIX}.json", RES)
    pp = os.path.join(PARTS, f"expo{SUFFIX}_partial.json")
    if os.path.exists(pp): os.remove(pp)
    P(f"expo{SUFFIX} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")

# ================================================================== cosmic: dark ages, IGM, galaxy-hosted gas; G8, G9, G10
def run_cosmic():
    Q3 = load_prefix(os.path.join(CL6, "QX3_cmb_growth", "iter2_kq_dust", "iter2.py"), 'if __name__ == "__main__":', "qx3_iter2_lib")
    Class, LMAX, ZPK = Q3["Class"], Q3["LMAX"], Q3["ZPK"]
    KG = np.logspace(-4, 1, 70); ZG = np.linspace(0.02, ZPK, 120)
    AM1 = json.load(open(os.path.join(RB, "AM1_native_abundance_match", "am1_bmf.json")))
    # SPARC's own relations (raw table): log M_cold = 4.301 + 0.533 log M_*; log R_d[kpc] = -2.066 + 0.254 log M_*; log R_HI[kpc] = -3.748 + 0.524 log M_HI
    def Mcold_of_Ms(Ms): return 10 ** (4.30129617 + 0.53319394 * math.log10(Ms))
    def Rd_of_Ms(Ms): return 10 ** (-2.06596709 + 0.25403748 * math.log10(Ms))
    def RHI_of_MHI(MHI): return 10 ** (-3.74783435 + 0.52390359 * math.log10(MHI))
    DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19), ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
            ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092), ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]   # DESI DR1 Table 9 as CE2 / L181 transcribed it
    def limber4(M, kgrid, zgrid, Rm):
        chis = M.angular_distance(1089.0) * (1 + 1089.0); chi = np.array([M.angular_distance(z) * (1 + z) for z in zgrid]); lnk = np.log(kgrid)
        Pm = np.array([[M.pk_lin(k, z) for z in zgrid] for k in kgrid])
        w = ((chis - chi) / (chi * chis)) ** 2 * (1 + np.asarray(zgrid)) ** 2 / np.array([M.Hubble(z) for z in zgrid])
        Ls = np.arange(2, LMAX + 1); num = np.zeros(len(Ls)); den = np.zeros(len(Ls))
        for j in range(len(zgrid)):
            kk = (Ls + 0.5) / chi[j]; m = (kk >= kgrid[0]) & (kk <= kgrid[-1])
            Pj = np.interp(np.log(kk[m]), lnk, Pm[:, j]); Rj = np.interp(np.log(kk[m]), lnk, Rm[:, j]); ex = (chi[j] / (Ls[m] + 0.5)) ** 4
            num[m] += w[j] * Pj * Rj ** 2 / chi[j] ** 2 * ex; den[m] += w[j] * Pj / chi[j] ** 2 * ex
        S = np.ones(LMAX + 1); ok = den > 0; S[Ls[ok]] = num[ok] / den[ok]; return S, Pm
    def growth_conv(M, ob, od, H0, fconv_of_lna, kgrid, zgrid):
        """QX3 iter2's growth solve with the converted dust fraction f(a) removed from the clustering source and from the
        clustering density; the background (total omega_d) is unchanged (density conserved). Returns delta_m(k, z) / reference."""
        h = H0 / 100; Om_b0 = ob / h ** 2; Om_d0 = od / h ** 2
        lna_t = np.linspace(math.log(1 / 3500.0), 0.0, 4000)
        lnH_t = np.array([math.log(M.Hubble(1 / math.exp(x) - 1)) for x in lna_t]); dlnH_t = np.gradient(lnH_t, lna_t); H0c = M.Hubble(0.0)
        ai = 1 / 3401.0; adec = 1 / 1091.0
        lnz = np.log(1 / (1 + np.asarray(zgrid))); kv = np.asarray(kgrid); nk = len(kv)
        def solve(fc):
            grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnz]))
            y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai; rec = {}; tset = {float(x): i for i, x in enumerate(lnz)}; I4 = np.eye(4)[None, :, :]
            def Amat(lna):
                a = math.exp(lna); E2 = math.exp(2 * np.interp(lna, lna_t, lnH_t)) / H0c ** 2; dl = float(np.interp(lna, lna_t, dlnH_t))
                Od = Om_d0 * a ** -3 / E2 * (1.0 - (fc(lna) if fc else 0.0)); Ob = Om_b0 * a ** -3 / E2; on = a > adec
                A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od; A[:, 1, 1] = -(2 + dl)
                if on: A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
                return A
            for n in range(len(grid) - 1):
                h_ = grid[n + 1] - grid[n]; A = Amat(0.5 * (grid[n] + grid[n + 1]))
                y = np.linalg.solve(I4 - 0.5 * h_ * A, ((I4 + 0.5 * h_ * A) @ y[:, :, None]))[:, :, 0]
                t = float(grid[n + 1])
                if t in tset: rec[tset[t]] = y.copy()
            out = np.empty((nk, len(zgrid)))
            for jz in range(len(zgrid)):
                yy = rec[jz]; a = 1 / (1 + zgrid[jz]); E2 = math.exp(2 * np.interp(math.log(a), lna_t, lnH_t)) / H0c ** 2
                Od = Om_d0 * a ** -3 / E2; Ob = Om_b0 * a ** -3 / E2; fz = fc(math.log(a)) if fc else 0.0
                out[:, jz] = (Od * (1 - fz) * yy[:, 0] + Ob * yy[:, 2]) / (Od + Ob)
            return out
        ref = solve(None); return (lambda fc: solve(fc) / ref), ref
    for f in FOOTS:
        th = THETA[f]; bg = Background(f); R_ = {}; RES[f] = R_
        # ---- exposures: dark ages, neutral IGM, galaxy-hosted cold gas
        E_dark = ESCALE * bg.expo_mean_density(*Z_DARK); E_igm = ESCALE * bg.expo_mean_density(Z_REION, Z_DARK[0])
        E_dark_z800 = ESCALE * bg.expo_mean_density(Z_DARK[0], 800.0)
        # matter-era closed form for KA4: rho_b0 (2/3) [(1+z2)^1.5 - (1+z1)^1.5] / (H0 sqrt(Om))
        Om = (bg.ob + bg.od) / bg.h ** 2; H0 = 100 * bg.h * 1.022712e-3   # km/s/Mpc -> 1/Gyr
        E_closed = bg.rho_b0 * (2.0 / 3.0) * ((1 + Z_DARK[1]) ** 1.5 - (1 + Z_DARK[0]) ** 1.5) / (H0 * math.sqrt(Om))
        # galaxy-hosted: GAMA baryonic mass function (AM1 "all"), SPARC relations; conversion coefficient Gamma'(z) (Msun pc^-3 per unit alpha)
        grid = np.array(AM1["grid"]); ncum = np.array(AM1["all"]); ndiff = np.maximum(-np.gradient(ncum, grid), 0.0) * (grid[1] - grid[0])   # per bin, Mpc^-3
        bins = []
        for lMb, n in zip(grid, ndiff):
            if n <= 0: continue
            Mb = 10 ** lMb; lo, hi = 1e5, Mb
            for _ in range(80):
                mid = math.sqrt(lo * hi)
                if mid + Mcold_of_Ms(mid) > Mb: hi = mid
                else: lo = mid
            Ms = math.sqrt(lo * hi); Mc = Mb - Ms; Rd = Rd_of_Ms(Ms) * 1e3
            MHI = Mc / 1.33; RHI = RHI_of_MHI(max(MHI, 1e4)) * 1e3
            lo2, hi2 = RHI / 2, RHI  # exponential gas disc with Sigma_cold(R_HI) = 1.33 Msun/pc^2: the outer root (s(Rg) peaks at R_HI/2)
            for _ in range(80):
                Rg = math.sqrt(lo2 * hi2); s = Mc / (2 * math.pi * Rg ** 2) * math.exp(-RHI / Rg)
                if s > 1.33: lo2 = Rg
                else: hi2 = Rg
            Rg = math.sqrt(lo2 * hi2)
            I_star = Ms * Mc / (4 * math.pi ** 2 * Rd ** 2 * Rg ** 2) * (Rd * Rg / (Rd + Rg))
            I_gas = Mc ** 2 / (4 * math.pi ** 2 * Rg ** 4) * (Rg / 2)
            bins.append(dict(lMb=float(lMb), n=float(n), Ms=Ms, Mc=Mc, Rd_pc=Rd, Rg_pc=Rg, I=I_star + I_gas, I_star=I_star, I_gas=I_gas))
        rho_b_com = bg.ob * RHO_CRIT_H2 / 1e18                       # Msun/pc^3 comoving
        rho_cold_model0 = sum(b["n"] * b["Mc"] for b in bins) / 1e18   # Msun/pc^3 comoving at z 0 from the mass function
        rho_cold_raw0 = (1.33 * omega_HI(0.0) * bg.rho_crit0 + rho_H2_comoving(0.0)) / 1e18
        def gamma_prime(z):
            """conversion coefficient (Msun pc^-3): rate per unit alpha of the cosmic dust, with each galaxy's cold gas scaled by the raw
            cold-gas density history and the I integrals linear/quadratic in M_c."""
            s = (1.33 * omega_HI(z) * bg.rho_crit0 + rho_H2_comoving(z)) / 1e18 / rho_cold_model0
            tot = sum(b["n"] / 1e18 * (b["I_star"] * s + b["I_gas"] * s * s) for b in bins)
            return 2 * math.sqrt(3) * tot / rho_b_com
        zz = np.concatenate([np.linspace(0, 6, 121), np.linspace(6.1, 20, 60)]); gp = np.array([gamma_prime(z) for z in zz])
        dtdz = np.array([1.0 / ((1 + z) * bg.H(z)) for z in zz])
        Egal_cum = np.concatenate([[0.0], np.cumsum(0.5 * (gp[1:] * dtdz[1:] + gp[:-1] * dtdz[:-1]) * np.diff(zz))])   # from z 0 up to z
        Egal_total = ESCALE * float(Egal_cum[-1])
        def E_total(z):
            """cumulative exposure of the mean dust parcel from z 1100 down to z."""
            if z >= Z_DARK[1]: return 0.0
            if z >= Z_DARK[0]: return ESCALE * bg.expo_mean_density(z, Z_DARK[1], 2000)
            e = E_dark
            e += ESCALE * bg.expo_mean_density(max(z, Z_REION), Z_DARK[0], 1000) if z < Z_DARK[0] else 0.0
            e += ESCALE * float(np.interp(Z_DARK[0], zz, Egal_cum) - np.interp(z, zz, Egal_cum))
            return e
        R_["exposures"] = dict(E_dark_20_1100=E_dark, E_dark_20_800_reported=E_dark_z800, E_dark_matter_era_closed_form=E_closed, E_igm_6_20=E_igm,
                               E_gal_0_20=Egal_total, E_gal_2_20=E_total(2.0) - E_dark - E_igm, E_total_z2=E_total(2.0), E_total_z0=E_total(0.0),
                               rho_b0_Msun_pc3=bg.rho_b0, rho_cold_model0=rho_cold_model0, rho_cold_raw0=rho_cold_raw0, n_bins=len(bins),
                               bins_example=[b for b in bins if abs(b["lMb"] - 10.5) < 0.03 or abs(b["lMb"] - 9.0) < 0.03])
        R_["KA4_dark_ages"] = dict(numeric=E_dark, closed_form_matter_era=E_closed, ratio=E_dark / E_closed, pass_=bool(0.7 <= E_dark / E_closed <= 1.0))
        P(f"[{f}] exposures: E_dark(20-1100) {E_dark:.4e} (closed-form matter era {E_closed:.4e}, ratio {E_dark/E_closed:.3f}); E_IGM(6-20) {E_igm:.3e}; E_gal(0-20) {Egal_total:.3e}; E_gal(2-20) {R_['exposures']['E_gal_2_20']:.3e}; rho_cold0 model {rho_cold_model0:.3e} vs raw {rho_cold_raw0:.3e} Msun/pc^3  [{time.time()-T0:.0f}s {rss():.2f}GB]")
        # ---- G10 machinery: CLASS on the footing fit; GL1's corrected kernel; CE2's fsigma8 ratio
        M = Class(); M.set({'output': 'tCl,lCl,mPk', 'l_max_scalars': LMAX + 100, 'h': th["h"], 'omega_b': th["omega_b"], 'omega_cdm': th["omega_d"], 'A_s': Q3["AS0"],
                            'n_s': th["n_s"], 'tau_reio': th["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 12.0, 'z_max_pk': ZPK}); M.compute()
        X0 = Q3["X_of"](M); c0, _ = Q3["best_amp_chi2"](X0); H0c = 100 * th["h"]
        ratio_of, ref = growth_conv(M, th["omega_b"], th["omega_d"], H0c, None, KG, ZG)
        S1, Pref = limber4(M, KG, ZG, np.ones_like(ref)); c1, _ = Q3["best_amp_chi2"](X0 * S1)
        hh = th["h"]; R8 = 8.0 / hh; lk = np.log(KG)
        def W(x): return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
        w2k3 = W(KG * R8) ** 2 * KG ** 3 / (2 * np.pi ** 2)
        def sig8(Rr): return np.sqrt(np.trapz(Pref * Rr ** 2 * w2k3[:, None], lk, axis=0))
        lna_z = np.log(1 / (1 + ZG))
        def fs8_ratio(Rr):
            from scipy.interpolate import CubicSpline
            o = np.argsort(lna_z); s_sw = sig8(Rr); s_rf = sig8(np.ones_like(Rr))
            d_sw = CubicSpline(lna_z[o], s_sw[o]).derivative()(lna_z); d_rf = CubicSpline(lna_z[o], s_rf[o]).derivative()(lna_z)
            rr = d_sw / d_rf; return {b[0]: float(np.interp(b[1], ZG, rr)) for b in DESI}
        def fs8_gate(rf):
            rows = []
            for (t, z, r1, p1, m1, r2, p2, m2) in DESI:
                e1, e2 = 0.5 * (p1 + m1), 0.5 * (p2 + m2); x = rf[t]
                rows.append(dict(bin=t, z=z, Rf=x, in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2), s8dir=bool(x <= 1.001)))
            return dict(rows=rows, pass_=bool(all(r["in_sf"] and r["in_sfb"] and r["s8dir"] for r in rows)))
        ka5 = fs8_ratio(np.ones_like(ref)); R_["KA5_growth_identity"] = dict(fs8_at_R1=ka5, dchi2_at_R1=float(c1 - c0), pass_=bool(max(abs(v - 1) for v in ka5.values()) <= 1e-6 and abs(c1 - c0) <= 1e-9))
        P(f"[{f}] KA5: R = 1 gives Rf 1 (max |d| {max(abs(v-1) for v in ka5.values()):.1e}) and dchi2 {c1-c0:.2e}; baseline chi2 {c0:.3f} -> {'PASS' if R_['KA5_growth_identity']['pass_'] else 'FAIL'}")
        # exposure history on a fine ln a table (for the ODE)
        ztab = np.concatenate([np.linspace(0, 20, 201), np.geomspace(20.5, 1100, 200), [1200.0, 3500.0]])
        Etab = np.array([E_total(z) for z in ztab]); lnatab = np.log(1 / (1 + ztab))
        R_["E_history"] = dict(z=[0, 0.5, 1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 800, 1000, 1100], E=[float(np.interp(math.log(1 / (1 + z)), lnatab[::-1], Etab[::-1])) for z in [0, 0.5, 1, 2, 3, 6, 10, 20, 50, 100, 200, 500, 800, 1000, 1100]])
        rows = []
        for ia, alpha in enumerate(ALPHAS):
            f20 = 1 - math.exp(-alpha * E_dark); f2 = 1 - math.exp(-alpha * E_total(2.0)); f0 = 1 - math.exp(-alpha * E_total(0.0))
            fc = lambda lna, alpha=alpha: 1 - math.exp(-alpha * float(np.interp(lna, lnatab[::-1], Etab[::-1])))
            Rr = ratio_of(fc); S, _ = limber4(M, KG, ZG, Rr); c, A = Q3["best_amp_chi2"](X0 * S); dchi = float(c - c0)
            rf = fs8_ratio(Rr); fg = fs8_gate(rf)
            g10 = bool(dchi <= 4.0 and fg["pass_"])
            rows.append(dict(alpha=alpha, f_conv_z20=f20, f_conv_z2=f2, f_conv_z0=f0, G8=dict(status="PASS" if f2 <= 0.03 else "FAIL", f_conv_z2=f2),
                             G9=dict(status="PASS" if f20 <= 0.01 else "FAIL", f_conv_z20=f20),
                             G10=dict(status="PASS" if g10 else "FAIL", lensing_dchi2=dchi, lensing_chi2=float(c), lensing_pass=bool(dchi <= 4.0), S_L100=float(S[100]), S_L400=float(S[400]),
                                      fsigma8=fg, R_z0_k0p1=float(np.interp(0.1, KG, Rr[:, 0])))))
            R_["grid"] = rows
            if ia % 5 == 0 or ia == len(ALPHAS) - 1:
                P(f"[{f}] alpha {alpha:8.3g}: f_conv z20 {f20:.4f} z2 {f2:.4f} z0 {f0:.4f} | G8 {rows[-1]['G8']['status'][0]} G9 {rows[-1]['G9']['status'][0]} | G10 {rows[-1]['G10']['status'][0]} dchi2 {dchi:8.2f} Rf " + " ".join(f"{k} {v:.3f}" for k, v in rf.items()) + f"  [{time.time()-T0:.0f}s {rss():.2f}GB]")
                dump(f"cosmic{SUFFIX}_partial.json", RES)
        M.struct_cleanup(); M.empty()
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; RES["criteria"] = CRIT; RES["alphas"] = ALPHAS; RES["omega_HI_table"] = OMEGA_HI_TAB
    dump(f"cosmic{SUFFIX}.json", RES)
    pp = os.path.join(PARTS, f"cosmic{SUFFIX}_partial.json")
    if os.path.exists(pp): os.remove(pp)
    P(f"cosmic{SUFFIX} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")

if __name__ == "__main__":
    P(f"BG1 {WHICH}{SUFFIX}. Criteria {CRIT}. R = {RF['canonical']:.6f} / {RF['alt']:.6f} (f_cap R {FCAPR['canonical']:.4f} / {FCAPR['alt']:.4f} reported). "
      f"alpha grid {len(ALPHAS)} points [{ALPHAS[0]:g}, {ALPHAS[-1]:g}]. kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing.")
    if WHICH == "grade":
        import bg1_grade  # noqa
    else:
        {"expo": run_expo, "cosmic": run_cosmic}[WHICH]()
    P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
