#!/usr/bin/env python3
"""CFG553: sealed (hash-committed) Milky Way predictions for Gaia DR4 (release 2026-12-02).

Frozen criteria: FROZEN_CRITERIA.md (committed alone first, 43fb64612).
Predictions P1 K_z(R, |z|) + midplane nu_z^2; P2 V_c(R) + dlnV/dlnR (15-22, 15-27.5 kpc); P3 local cold-energy density,
K_z(R0, 1.1), Sigma(|z| < 1.1), Oort limit; P4 sigma_z for declared isothermal tracers (h 0.30 / 0.90 kpc); P5 V_c 30-60 kpc.
Framework: round cold-energy rule RM-v and RM-phi (CFG516). Rivals: PD (full QUMOND phantom disc) and NFW fitted to Ou+24.
Baryons: McMillan17 census, band = stars x [0.895, 1.105] (5.43 +- 0.57e10); variants B2 / B2b / B3 reported.
Machinery executed read-only from CFG532 (which executes CFG516 and CFG514); nothing there is edited.
MUTATE (CFG553_MUTATE=1): round <-> disc swap for P1; exit 1 = DETECTED.
kappa = 1/2 is FITTED; both footings never pooled; no EFE; cold energy mass still required; not theory closed.
The Gaia DR4 wide-binary prereg (prep_2026/gaia_dr4_prep/) is NOT touched.
Run: nice -n 10 python3 cfg553_predict.py   (2 threads)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "2"
import sys, json, math, time, io, contextlib
import numpy as np
from scipy.stats import chi2 as chi2dist

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG553_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""

# ------------------------------------------------------------------ re-used machinery (read-only exec of CFG532's head)
SRC532 = os.path.join(HERE, "..", "CFG532_mw_gaia_rotation_curves", "cfg532_mw_curves.py")
src = open(SRC532).read()
head = src.split("\n# ------------------------------------------------------------------ controls\n")[0]
comp = src.split("# ------------------------------------------------------------------ comparators")[1].split(
    "# ------------------------------------------------------------------ verdict machinery")[0]
N5 = {"__file__": os.path.abspath(SRC532)}
os.environ.pop("CFG532_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, "cfg532_head", "exec"), N5)
    exec(compile(comp, "cfg532_comparators", "exec"), N5)
G, A0, GR, nu_mono = N5["G"], N5["A0"], N5["GR"], N5["nu_mono"]
Base, build_PD, flux_mass, Mtab, RS = N5["Base"], N5["build_PD"], N5["flux_mass"], N5["Mtab"], N5["RS"]
Mix, v_model, b1mix, slope, fit_nfw, CURVES = N5["Mix"], N5["v_model"], N5["b1mix"], N5["slope"], N5["fit_nfw"], N5["CURVES"]
b_st, b_gas, b_b2, b_b2b = N5["b_st"], N5["b_gas"], N5["b_b2"], N5["b_b2b"]
rho_b2, rho_mcm = N5["rho_b2"], N5["rho_mcm"]
nfw_params, nfw_g = N5["nfw_params"], N5["nfw_g"]
N6 = N5["ns"]                       # CFG516 namespace
N4 = N6["ns"]                       # CFG514 namespace
rho_b3, FieldModel, Mcold_phi, Mcold_v, chi2_kz = N6["rho_b3"], N6["FieldModel"], N6["Mcold_phi"], N6["Mcold_v"], N6["chi2_kz"]
BR_R, KZ_UNIT, R0 = N6["BR_R"], N6["KZ_UNIT"], N6["R0"]
rho_stars, nfw_rho = N4["rho_stars_only"], N4["nfw_rho"]
ZC0 = GR.zc[0]
FOOTS = ("canonical", "alt")
FORMS = ("RMv", "RMphi")
MSTAR, MSTAR_ERR = 5.43e10, 0.57e10
DS = MSTAR_ERR / MSTAR
S_LIST = [1 - DS, 1 - DS / 2, 1.0, 1 + DS / 2, 1 + DS]
S_LAB = ["s-", "s-/2", "s1", "s+/2", "s+"]

# unit conversion from constants: 1 Msun/pc^3 in GeV/cm^3
MSUN_KG, C_MS, PC_CM, GEV_J = 1.98847e30, 299792458.0, 3.0856775814913673e18, 1.602176634e-10
MSUNPC3_GEVCM3 = MSUN_KG * C_MS ** 2 / GEV_J / PC_CM ** 3

# declared grids
P1_R = np.arange(5.0, 16.0 + 1e-9, 1.0)
P1_Z = np.array([0.5, 1.1, 2.0])
Z_NU = 0.075
P2_R = np.arange(5.0, 27.0 + 1e-9, 1.0)
P4_H = {"thin_h0.30": 0.30, "thick_h0.90": 0.90}
P5_R = np.array([30.0, 40.0, 50.0, 60.0])
FLOOR = {"P1": 0.05, "P2": 0.02, "P4": 0.05}

OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(cond, msg):
    CHECKS.append((bool(cond), msg)); P(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    return bool(cond)


T0 = time.time()
P("=" * 112)
P(f"CFG553  sealed Milky Way predictions for Gaia DR4 (2026-12-02)   {'*** MUTATE: round <-> disc swap ***' if MUTATE else 'PRIMARY'}")
P("kappa = 1/2 FITTED; footings 9.36e-11 / 1.13e-10 never pooled; nu_mono; no EFE; cold energy mass still required")
P("=" * 112)

# ------------------------------------------------------------------ baryon variants (density functions alongside the grid mixes)
b_b3 = Base("B3_short_disc", rho_b3)


def rho_b1(s):
    return lambda R, z: s * rho_stars(R, z) + (rho_mcm(R, z) - rho_stars(R, z))


VARIANTS = {}
for s, lab in zip(S_LIST, S_LAB):
    mx, key = b1mix(s)
    VARIANTS[f"B1_{lab}"] = dict(mix=mx, key=key, rho=rho_b1(s), s=s, census=True)
VARIANTS["B2_6.0e10"] = dict(mix=Mix([(b_b2, 1.0)]), key="B2", rho=lambda R, z: rho_b2(R, z, 6.0e10), s=None, census=False)
VARIANTS["B2b_7.3e10"] = dict(mix=Mix([(b_b2b, 1.0)]), key="B2b", rho=lambda R, z: rho_b2(R, z, 7.3e10), s=None, census=False)
VARIANTS["B3_short_disc_2.15"] = dict(mix=Mix([(b_b3, 1.0)]), key="B3", rho=rho_b3, s=None, census=False)
CENSUS = [f"B1_{l}" for l in S_LAB]
for k, v in VARIANTS.items():
    P(f"  baryon variant {k:<20} M_b(grid) = {v['mix'].Mb:.4e} Msun")


# ------------------------------------------------------------------ a predicting model
class Pred:
    """total field of one model on one baryon variant. kind: RMv, RMphi, PD, NFW."""

    def __init__(self, kind, var, foot):
        self.kind, self.var, self.foot = kind, var, foot
        V = VARIANTS[var]; self.mix = V["mix"]; self.rho_b = V["rho"]
        mix = self.mix
        self.Mc = None; self.pd = None; self.nfw = None
        if kind in ("RMphi", "PD"):
            pd, rho_ph = build_PD(mix, 1.0, foot)
            self.pd = pd.gm
            if kind == "RMphi":
                self.Mc = flux_mass(pd.gm.gRz, RS) - mix.Menc
        if kind == "RMv":
            a0 = A0[foot]; g = np.abs(mix.gNplane)
            self.Mc = RS * (RS * nu_mono(g / a0) * g) / G - mix.Menc
        if kind == "NFW":
            f = fit_nfw(CURVES["C1_Ou24"], mix)
            self.nfw = nfw_params(f["M200"], f["c"]); self.nfw_fit = dict(M200=f["M200"], c=f["c"], chi2_Ou24=f["chi2"], p=f["p"])
        if self.Mc is not None:
            self.dMdr = np.gradient(self.Mc, RS)

    def gRz(self, R, z):
        R = np.asarray(R, float); z = np.abs(np.asarray(z, float))
        if self.kind == "PD":
            return self.pd.gRz(R, z)
        dR = sum(c * b.m.gRz(R, z)[0] for b, c in self.mix.parts)
        dz = sum(c * b.m.gRz(R, z)[1] for b, c in self.mix.parts)
        r = np.sqrt(R ** 2 + z ** 2)
        if self.Mc is not None:
            gr = G * Mtab(self.Mc, r) / r ** 2
        else:
            gr = nfw_g(self.nfw, r)
        return dR + gr * R / r, dz + gr * z / r

    def Kz(self, R, z):
        return self.gRz(R, z)[1]

    def vc(self, R):
        R = np.asarray(R, float)
        return np.sqrt(np.maximum(R * self.gRz(R, np.full_like(R, ZC0))[0], 0))

    def rho_dark(self, R, z):
        R = np.asarray(R, float); z = np.abs(np.asarray(z, float)); r = np.sqrt(R ** 2 + z ** 2)
        if self.kind == "PD":
            return self.pd.rho_d(R, z)
        if self.kind == "NFW":
            return nfw_rho(self.nfw, r)
        return np.interp(np.log(r), np.log(RS), self.dMdr) / (4 * math.pi * r ** 2)


def sigz2(pm, R, h):
    zz = np.linspace(0.0, 12 * h, 1201)
    return float(np.trapz(np.exp(-zz / h) * pm.Kz(np.full_like(zz, R), zz), zz))


def predict(pm):
    o = {}
    K = np.array([[pm.Kz(np.full(1, R), np.full(1, z))[0] / KZ_UNIT for z in P1_Z] for R in P1_R])
    nuz2 = pm.Kz(P1_R, np.full_like(P1_R, Z_NU)) / Z_NU            # (km/s)^2/kpc^2
    o["P1"] = dict(Kz_o2piG=K.tolist(), nuz2_kms_kpc2=nuz2.tolist(),
                   Kz11_R0=float(pm.Kz(np.array([R0]), np.array([1.1]))[0] / KZ_UNIT),
                   nuz2_R0=float(pm.Kz(np.array([R0]), np.array([Z_NU]))[0] / Z_NU))
    V = pm.vc(P2_R)
    Rg1 = np.arange(15.0, 22.0 + 1e-9, 0.5); Rg2 = np.arange(15.0, 27.5 + 1e-9, 0.5)
    v1 = pm.vc(Rg1); v2 = pm.vc(Rg2)
    o["P2"] = dict(Vc=V.tolist(), Vc_R0=float(pm.vc(np.array([R0]))[0]), V20=float(pm.vc(np.array([20.0]))[0]),
                   slope_15_22=slope(Rg1, v1, v1 / 100, 15.0, 22.0)[0], slope_15_275=slope(Rg2, v2, v2 / 100, 15.0, 27.5)[0])
    rd = float(pm.rho_dark(np.array([R0]), np.array([0.0]))[0]) / 1e9                 # Msun/pc^3
    zc = np.linspace(0.0, 1.1, 2201)
    Rc = np.full_like(zc, R0)
    sig_b = 2 * np.trapz(pm.rho_b(Rc, zc), zc) / 1e6
    sig_d = 2 * np.trapz(pm.rho_dark(Rc, zc), zc) / 1e6
    rb0 = float(pm.rho_b(np.array([R0]), np.array([0.0]))[0]) / 1e9
    o["P3"] = dict(rho_dark_Msun_pc3=rd, rho_dark_GeV_cm3=rd * MSUNPC3_GEVCM3, Kz11_o2piG=o["P1"]["Kz11_R0"],
                   Sigma11_true_Msun_pc2=float(sig_b + sig_d), Sigma11_dark_Msun_pc2=float(sig_d),
                   Sigma11_baryon_Msun_pc2=float(sig_b), rho_tot_mid_Msun_pc3=rb0 + rd, rho_b_mid_Msun_pc3=rb0)
    o["P4"] = {k: [math.sqrt(max(sigz2(pm, R, h), 0)) for R in P1_R] for k, h in P4_H.items()}
    o["P4"]["thin_R0"] = math.sqrt(sigz2(pm, R0, 0.30))
    V5 = pm.vc(P5_R)
    Rm = np.linspace(30.0, 60.0, 31)
    # added after the first run (K6 failed as frozen): spherical-equivalent V_c = sqrt(G M(<r)/r) from the Gauss flux
    Vs = np.sqrt(G * flux_mass(pm.gRz, Rm) / Rm)
    o["P5"] = dict(Vc=V5.tolist(), mean_30_60=float(np.mean(pm.vc(Rm))),
                   Vc_sph=[float(Vs[int(np.argmin(np.abs(Rm - r)))]) for r in P5_R], mean_30_60_sph=float(np.mean(Vs)))
    if pm.kind == "NFW":
        o["NFW_fit"] = pm.nfw_fit
    return o


# ------------------------------------------------------------------ controls
P("\n--- controls")
j516 = json.load(open(os.path.join(HERE, "..", "CFG516_round_cold_energy", "cfg516_mw_results.json")))
j532 = json.load(open(os.path.join(HERE, "..", "CFG532_mw_gaia_rotation_curves", "cfg532_results.json")))
b1 = Base("B1_McMillan17", rho_mcm)
ZB = np.full_like(BR_R, 1.1)
k1 = 0.0
for foot in FOOTS:
    ref = j516["models"]["B1_McMillan17"][f"{foot}_F0"]
    pdm, _ = build_PD(b1, 1.0, foot)
    mods = {"PD": pdm, "RMphi": FieldModel(b1, 1.0, Mcold=Mcold_phi(b1, 1.0, foot)[0]),
            "RMv": FieldModel(b1, 1.0, Mcold=Mcold_v(b1, 1.0, foot))}
    for k, fm in mods.items():
        c2 = chi2_kz(fm.Kz(BR_R, ZB) / KZ_UNIT)
        k1 = max(k1, abs(c2 / ref[k]["chi2_kz"] - 1))
        P(f"    K1 {foot:<9} {k:<5} K_z chi2 {c2:9.4f}  CFG516 {ref[k]['chi2_kz']:9.4f}")
check(k1 < 1e-4, f"K1 CFG516 K_z chi2 (B1 F0; PD, RM-phi, RM-v; both footings) reproduced: max rel dev {k1:.2e} (< 1e-4)")
k2 = 0.0; k2s = 0.0
Rg6 = np.array([15.0, 17.5, 20.0, 22.5, 25.0, 27.5])
for foot in FOOTS:
    for kind in FORMS:
        mx, key = b1mix(1.0)
        v20 = float(v_model(kind, mx, key, foot, np.array([20.0]))[0])
        ref = j532["dr4"][f"{foot}|{kind}"]["B1_census"]
        v6 = v_model(kind, mx, key, foot, Rg6); b6 = slope(Rg6, v6, v6 / 100)[0]
        k2 = max(k2, abs(v20 / ref["V20"] - 1)); k2s = max(k2s, abs(b6 - ref["slope"]))
        P(f"    K2 {foot:<9} {kind:<5} V(20) {v20:.3f} (CFG532 {ref['V20']:.3f}); 6-pt slope {b6:+.5f} (CFG532 {ref['slope']:+.5f})")
check(k2 < 1e-4 and k2s < 1e-4, f"K2 CFG532 census V(20 kpc) and DR4 slope reproduced: rel dev {k2:.2e}, slope dev {k2s:.2e}")
mxc = VARIANTS["B1_s1"]["mix"]
kmix = sum(c * b.m.gRz(np.array([R0]), np.array([1.1]))[1][0] for b, c in mxc.parts)
kb1 = b1.m.gRz(np.array([R0]), np.array([1.1]))[1][0]
check(abs(kmix / kb1 - 1) < 0.005, f"K3 Mix (stars + gas) Newtonian K_z(R0, 1.1) vs single B1 Base: {kmix / kb1 - 1:+.2e} (< 0.5%)")
fN = fit_nfw(CURVES["C1_Ou24"], mxc)
refN = j532["comparators"]["C1_Ou24"]["NFW"]["chi2"]
check(abs(fN["chi2"] / refN - 1) < 1e-3, f"K4 fitted NFW chi2 on Ou+24 {fN['chi2']:.4f} vs CFG532 {refN:.4f}")


class _Uni:
    def Kz(self, R, z):
        return np.full_like(np.asarray(z, float), 3000.0)


s2u = sigz2(_Uni(), R0, 0.3)
check(abs(s2u / (3000.0 * 0.3) - 1) < 1e-3, f"K5 Jeans integrator, uniform K_z: sigma^2 / (K h) = {s2u / 900.0:.6f}")
check(abs(MSUNPC3_GEVCM3 / 37.97 - 1) < 2e-3, f"K5b unit: 1 Msun/pc^3 = {MSUNPC3_GEVCM3:.3f} GeV/cm^3")

# ------------------------------------------------------------------ predictions
KINDS_F = FORMS
SWAP = {"RMv": "PD", "RMphi": "PD"}                # MUTATE: the framework's P1 is the disc's
PRED = {}
MODELS = {}
for foot in FOOTS:
    PRED[foot] = {}
    for kind in ("RMv", "RMphi", "PD"):
        PRED[foot][kind] = {}
        for var in VARIANTS:
            pm = Pred(kind, var, foot)
            MODELS[(foot, kind, var)] = pm
            PRED[foot][kind][var] = predict(pm)
PRED["footing_independent"] = {"NFW": {}}
for var in VARIANTS:
    pm = Pred("NFW", var, "canonical")
    MODELS[("any", "NFW", var)] = pm
    PRED["footing_independent"]["NFW"][var] = predict(pm)

if MUTATE:
    # round <-> disc swap for P1: the framework forms carry the disc's P1; the PD rival carries RM-v's
    for foot in FOOTS:
        rm_p1 = {var: PRED[foot]["RMv"][var]["P1"] for var in VARIANTS}
        rmphi_p1 = {var: PRED[foot]["RMphi"][var]["P1"] for var in VARIANTS}
        pd_p1 = {var: PRED[foot]["PD"][var]["P1"] for var in VARIANTS}
        PRED[foot]["_true_RM_P1"] = dict(RMv=rm_p1, RMphi=rmphi_p1)
        for var in VARIANTS:
            PRED[foot]["RMv"][var]["P1"] = pd_p1[var]
            PRED[foot]["RMphi"][var]["P1"] = pd_p1[var]
            PRED[foot]["PD"][var]["P1"] = rm_p1[var]


def get(foot, kind):
    return PRED["footing_independent"]["NFW"] if kind == "NFW" else PRED[foot][kind]


# ------------------------------------------------------------------ scalars, bands, vectors
SCALARS = {
    "P1_Kz11_R0": ("P1", "Kz11_R0"), "P1_nuz2_R0": ("P1", "nuz2_R0"),
    "P2_Vc_R0": ("P2", "Vc_R0"), "P2_V20": ("P2", "V20"),
    "P2_slope_15_22": ("P2", "slope_15_22"), "P2_slope_15_27.5": ("P2", "slope_15_275"),
    "P3_rho_dark_GeV_cm3": ("P3", "rho_dark_GeV_cm3"), "P3_rho_dark_Msun_pc3": ("P3", "rho_dark_Msun_pc3"),
    "P3_Sigma11_true": ("P3", "Sigma11_true_Msun_pc2"), "P3_Sigma11_dark": ("P3", "Sigma11_dark_Msun_pc2"),
    "P3_rho_tot_mid": ("P3", "rho_tot_mid_Msun_pc3"),
    "P4_sigz_thin_R0": ("P4", "thin_R0"),
    "P5_V30": ("P5", "Vc", 0), "P5_V40": ("P5", "Vc", 1), "P5_V50": ("P5", "Vc", 2), "P5_V60": ("P5", "Vc", 3),
    "P5_mean_30_60": ("P5", "mean_30_60"),
    "P5_V60_sph(added)": ("P5", "Vc_sph", 3), "P5_mean_30_60_sph(added)": ("P5", "mean_30_60_sph"),
}


def sval(o, spec):
    v = o[spec[0]][spec[1]]
    return v[spec[2]] if len(spec) > 2 else v


def vec(o, name):
    if name == "P1":
        return np.array(o["P1"]["Kz_o2piG"]).ravel()
    if name == "P2":
        return np.array(o["P2"]["Vc"])
    if name == "P4":
        return np.array(o["P4"]["thin_h0.30"])
    if name == "P4thick":
        return np.array(o["P4"]["thick_h0.90"])
    raise ValueError(name)


def band(d, spec):
    vals = [sval(d[v], spec) for v in CENSUS]
    varv = [sval(d[v], spec) for v in VARIANTS]
    return dict(central=sval(d["B1_s1"], spec), lo=min(vals), hi=max(vals), env_lo=min(varv), env_hi=max(varv),
                at_s=vals)


BANDS = {}
for foot in FOOTS:
    BANDS[foot] = {k: {n: band(get(foot, k), sp) for n, sp in SCALARS.items()} for k in ("RMv", "RMphi", "PD", "NFW")}


def sep_scalar(F, Rb):
    """required sigma (3 sigma) both ways; NOT SEPARABLE if a central lies inside the other band."""
    fin = Rb["lo"] <= F["central"] <= Rb["hi"]
    rin = F["lo"] <= Rb["central"] <= F["hi"]
    dF = min(abs(F["central"] - Rb["lo"]), abs(F["central"] - Rb["hi"]))
    dR = min(abs(Rb["central"] - F["lo"]), abs(Rb["central"] - F["hi"]))
    return dict(delta_central=F["central"] - Rb["central"], bands_overlap=bool(F["lo"] <= Rb["hi"] and Rb["lo"] <= F["hi"]),
                sigma_req_F_truth=None if fin else dF / 3, sigma_req_R_truth=None if rin else dR / 3,
                separable=bool(not fin and not rin))


S_FINE = np.linspace(S_LIST[0], S_LIST[-1], 41)


def interp_s(arrs, s):
    """linear interpolation in s between the five census tabulations (arrs: list of 5 arrays)."""
    return np.array([np.interp(s, S_LIST, [a[i] for a in arrs]) for i in range(len(arrs[0]))])


def chi2min_rival(truth, rival_arrs, f, floor):
    sig2 = (f * truth) ** 2 + (floor * truth) ** 2
    return min(float(np.sum((truth - interp_s(rival_arrs, s)) ** 2 / sig2)) for s in S_FINE)


def req_frac(truth, rival_arrs, floor):
    c0 = chi2min_rival(truth, rival_arrs, 0.0, floor)
    if c0 < 9:
        return dict(f_req=None, chi2_at_zero_error=c0, floor_limited=True)
    lo, hi = 0.0, 1.0
    if chi2min_rival(truth, rival_arrs, hi, floor) >= 9:
        return dict(f_req=hi, chi2_at_zero_error=c0, floor_limited=False)
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if chi2min_rival(truth, rival_arrs, mid, floor) >= 9:
            lo = mid
        else:
            hi = mid
    return dict(f_req=lo, chi2_at_zero_error=c0, floor_limited=False)


SEP = {}
for foot in FOOTS:
    SEP[foot] = {}
    for form in FORMS:
        SEP[foot][form] = {}
        for rival in ("PD", "NFW"):
            d = {}
            for n in SCALARS:
                d[n] = sep_scalar(BANDS[foot][form][n], BANDS[foot][rival][n])
            for vname in ("P1", "P2", "P4", "P4thick"):
                truthF = vec(get(foot, form)["B1_s1"], vname)
                truthR = vec(get(foot, rival)["B1_s1"], vname)
                arrF = [vec(get(foot, form)[v], vname) for v in CENSUS]
                arrR = [vec(get(foot, rival)[v], vname) for v in CENSUS]
                fl = FLOOR["P4" if vname.startswith("P4") else vname]
                d[f"{vname}_vector"] = dict(F_truth=req_frac(truthF, arrR, fl), R_truth=req_frac(truthR, arrF, fl), floor=fl,
                                            N=len(truthF))
            SEP[foot][form][rival] = d

# ------------------------------------------------------------------ MUTATE detection / unswapped ratio diagnostics
RATIO = {}
for foot in FOOTS:
    RATIO[foot] = {}
    for form in FORMS:
        if MUTATE:
            rm = PRED[foot]["_true_RM_P1"][form]
            fw = {v: PRED[foot][form][v]["P1"] for v in VARIANTS}          # = disc after swap
        else:
            rm = {v: PRED[foot][form][v]["P1"] for v in VARIANTS}
            fw = {v: PRED[foot]["PD"][v]["P1"] for v in VARIANTS}
        nu_rm = np.array(rm["B1_s1"]["nuz2_kms_kpc2"]); nu_pd = np.array(fw["B1_s1"]["nuz2_kms_kpc2"])
        r16 = float(nu_pd[-1] / nu_rm[-1]); rR0 = float(fw["B1_s1"]["nuz2_R0"] / rm["B1_s1"]["nuz2_R0"])
        K11 = lambda p: np.array(p["Kz_o2piG"])[:, 1]
        lo = np.min([K11(rm[v]) for v in CENSUS], axis=0); hi = np.max([K11(rm[v]) for v in CENSUS], axis=0)
        kd = K11(fw["B1_s1"]); m8 = P1_R >= 8
        outside = bool(np.all((kd[m8] > hi[m8]) | (kd[m8] < lo[m8])))
        RATIO[foot][form] = dict(nuz2_ratio_PD_over_RM_R16=r16, nuz2_ratio_R0=rR0,
                                 nuz2_ratio_by_R=(nu_pd / nu_rm).tolist(),
                                 Kz11_ratio_PD_over_RM_by_R=(kd / K11(rm["B1_s1"])).tolist(),
                                 in_1p6_3p6=bool(1.6 <= r16 <= 3.6), ge_1p28=bool(r16 >= 1.28), Kz11_outside_RM_band_R_ge_8=outside)

# ------------------------------------------------------------------ the post-DR4 scorer (frozen code path; self-test only now)


def score_scalar(m, sig, F, Rb):
    def d(B):
        return 0.0 if B["lo"] <= m <= B["hi"] else min(abs(m - B["lo"]), abs(m - B["hi"])) / sig
    dF, dR = d(F), d(Rb)
    if dF <= 2 and dR >= 3:
        v = "FRAMEWORK-SUPPORTED"
    elif dF >= 3 and dR <= 2:
        v = "FRAMEWORK-EXCLUDED"
    elif dF >= 3 and dR >= 3:
        v = "BOTH EXCLUDED"
    else:
        v = "NOT DIAGNOSTIC"
    return dict(d_F=dF, d_R=dR, verdict=v)


def score_vector(m, cov, arrF, arrR, floor):
    def c2(arrs):
        best = None
        for s in S_FINE:
            mod = interp_s(arrs, s)
            C = cov + np.diag((floor * mod) ** 2)
            r = m - mod
            x = float(r @ np.linalg.solve(C, r))
            best = x if best is None or x < best else best
        return best
    cF, cR = c2(arrF), c2(arrR)
    pF, pR = float(chi2dist.sf(cF, len(m))), float(chi2dist.sf(cR, len(m)))
    okF, okR = pF >= 0.0455, pR >= 0.0455
    exF, exR = pF < 0.0027, pR < 0.0027
    if okF and exR:
        v = "FRAMEWORK-SUPPORTED"
    elif exF and okR:
        v = "FRAMEWORK-EXCLUDED"
    elif exF and exR:
        v = "BOTH EXCLUDED"
    else:
        v = "NOT DIAGNOSTIC"
    return dict(chi2_F=cF, chi2_R=cR, p_F=pF, p_R=pR, dchi2_R_minus_F=cR - cF, verdict=v)


if not MUTATE:
    P("\n--- K7 (added; scorer self-test on synthetic measurements, no data)")
    F = BANDS["canonical"]["RMv"]["P1_Kz11_R0"]; Rb = BANDS["canonical"]["PD"]["P1_Kz11_R0"]
    t1 = score_scalar(F["central"], 1.0, F, Rb)["verdict"]; t2 = score_scalar(Rb["central"], 1.0, F, Rb)["verdict"]
    arrF = [vec(PRED["canonical"]["RMv"][v], "P1") for v in CENSUS]; arrR = [vec(PRED["canonical"]["PD"][v], "P1") for v in CENSUS]
    tru = arrF[2]; cov = np.diag((0.02 * tru) ** 2)
    t3 = score_vector(tru, cov, arrF, arrR, FLOOR["P1"])["verdict"]
    check(t1 == "FRAMEWORK-SUPPORTED" and t2 == "FRAMEWORK-EXCLUDED" and t3 == "FRAMEWORK-SUPPORTED",
          f"K7 scorer: framework-central truth -> {t1}; PD-central truth -> {t2}; P1 vector at 2% (framework truth) -> {t3}")

# K6 in-plane vs spherical-equivalent V_c at 30-60 kpc
k6 = 0.0
for foot in FOOTS:
    for kind in ("RMv", "RMphi", "PD"):
        pm = MODELS[(foot, kind, "B1_s1")]
        vin = pm.vc(P5_R)
        vsp = np.sqrt(G * flux_mass(pm.gRz, P5_R) / P5_R)
        k6 = max(k6, float(np.max(np.abs(vin / vsp - 1))))
check(k6 < 0.01, f"K6 P5 in-plane vs spherical-equivalent V_c at 30-60 kpc: max dev {k6:.2%} (< 1%)"
      f" [frozen expectation; the disc quadrupole and, for PD, the flattened phantom make it larger; spherical-equivalent P5 added]")

# ------------------------------------------------------------------ print
P("\n--- headline scalars (census central [census band]; variant envelope)")
for foot in FOOTS:
    P(f"\n  [{foot}]")
    for n in SCALARS:
        row = []
        for k in ("RMv", "RMphi", "PD", "NFW"):
            b = BANDS[foot][k][n]
            row.append(f"{k} {b['central']:.4g} [{b['lo']:.4g},{b['hi']:.4g}]")
        P(f"    {n:<22} " + " | ".join(row))
P("\n--- separations: required DR4 sigma (3 sigma) for framework-central truth vs rival band / rival-central truth vs framework band")
for foot in FOOTS:
    for form in FORMS:
        for rival in ("PD", "NFW"):
            d = SEP[foot][form][rival]
            P(f"\n  [{foot} {form} vs {rival}]")
            for n in SCALARS:
                x = d[n]
                fmt = lambda v: "NOT SEP" if v is None else f"{v:.4g}"
                P(f"    {n:<22} delta {x['delta_central']:+.4g}  sigma_req F-truth {fmt(x['sigma_req_F_truth'])}  R-truth {fmt(x['sigma_req_R_truth'])}")
            for vname in ("P1", "P2", "P4", "P4thick"):
                x = d[f"{vname}_vector"]
                g = lambda q: "FLOOR-LIMITED" if q["floor_limited"] else f"{100 * q['f_req']:.2f}%"
                P(f"    {vname + '_vector':<22} N {x['N']}  floor {x['floor']:.0%}  f_req F-truth {g(x['F_truth'])} (chi2@0 {x['F_truth']['chi2_at_zero_error']:.1f})"
                  f"  R-truth {g(x['R_truth'])} (chi2@0 {x['R_truth']['chi2_at_zero_error']:.1f})")
P("\n--- disc / round ratios (census central)" + (" [MUTATE: swapped]" if MUTATE else ""))
for foot in FOOTS:
    for form in FORMS:
        r = RATIO[foot][form]
        P(f"  {foot:<9} {form:<5} nu_z^2 PD/RM at R0 {r['nuz2_ratio_R0']:.3f}, at 16 kpc {r['nuz2_ratio_PD_over_RM_R16']:.3f} "
          f"(in 1.6-3.6: {r['in_1p6_3p6']}); K_z,1.1 PD/RM by R: " + " ".join(f"{x:.2f}" for x in r["Kz11_ratio_PD_over_RM_by_R"])
          + f"; outside RM band at R>=8: {r['Kz11_outside_RM_band_R_ge_8']}")
if MUTATE:
    det_a = all(RATIO[f][m]["in_1p6_3p6"] for f in FOOTS for m in FORMS)
    det_lo = all(RATIO[f][m]["ge_1p28"] for f in FOOTS for m in FORMS)
    det_b = all(RATIO[f][m]["Kz11_outside_RM_band_R_ge_8"] for f in FOOTS for m in FORMS)
    detected = bool(det_b and det_lo)
    label = "DETECTED" if (det_a and det_b) else ("DETECTED BELOW THE HEADLINE RANGE" if detected else "NOT DETECTED")
    P(f"\n  MUTATE: (a) nu_z^2 ratio at 16 kpc in 1.6-3.6 all cells: {det_a}; >= 1.28: {det_lo}; (b) K_z,1.1 outside RM band at R>=8 all cells: {det_b} -> {label}")
    check(detected, f"MUTATE {label}")

RES = dict(lane="CFG553", mutate=MUTATE, criteria_commit="43fb64612", release="Gaia DR4 2026-12-02",
           settings=dict(kappa="1/2 FITTED", a0_SI=dict(canonical=9.36e-11, alt=1.13e-10), kernel="nu_mono 1/(1-exp(-sqrt y))",
                         efe=False, R0_kpc=R0, census_stars=MSTAR, census_err=MSTAR_ERR, s_list=S_LIST, s_labels=S_LAB,
                         floors=FLOOR, nfw_fit_to="Ou+24 Table 1 (CFG532 error model)", z_nu_kpc=Z_NU,
                         Msun_pc3_to_GeV_cm3=MSUNPC3_GEVCM3),
           grids=dict(P1_R=P1_R.tolist(), P1_z=P1_Z.tolist(), P2_R=P2_R.tolist(), P4_R=P1_R.tolist(), P4_h=P4_H, P5_R=P5_R.tolist()),
           baryon_variants={k: dict(Mb_grid=float(v["mix"].Mb), s=v["s"], census=v["census"]) for k, v in VARIANTS.items()},
           predictions=PRED, bands=BANDS, separations=SEP, disc_round_ratios=RATIO,
           checks=[dict(ok=a, msg=b) for a, b in CHECKS])
if MUTATE:
    RES["mutate_detected"] = bool(CHECKS[-1][0])


def jc(o):
    if isinstance(o, dict):
        return {str(k): jc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    return o


jpath = os.path.join(HERE, f"cfg553_predictions{TAG}.json")
json.dump(jc(RES), open(jpath, "w"), indent=1, sort_keys=True)
P(f"\nchecks: {sum(a for a, _ in CHECKS)}/{len(CHECKS)} pass; runtime {time.time() - T0:.0f} s")
open(os.path.join(HERE, f"cfg553_predict{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if RES["mutate_detected"] else 0)
sys.exit(0 if all(a for a, _ in CHECKS) else 2)
