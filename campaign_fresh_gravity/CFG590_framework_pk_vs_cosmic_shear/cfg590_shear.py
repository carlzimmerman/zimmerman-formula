#!/usr/bin/env python3
"""CFG590 (FROZEN_CRITERIA.md): the framework's matter power against cosmic shear (KiDS-1000, DES Y3 A_mod), with the SAME
HMcode-2020 (BAHAMAS-calibrated) baryonic-feedback suppression applied to LCDM and to the framework; LCDM-DMO judged by the same rule.

  OMP_NUM_THREADS=2 nice -n 10 python3 cfg590_shear.py                  -> cfg590_shear.out, cfg590_results.json
  CFG590_MUTATE=1 OMP_NUM_THREADS=2 nice -n 10 python3 cfg590_shear.py  -> *_MUTATE.out / *_MUTATE.json (exit 1 = all teeth bite)

kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed. Nothing downloaded; other lanes read only."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import numpy as np
import camb

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.abspath(os.path.join(HERE, ".."))
MUT = os.environ.get("CFG590_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ inputs: R(k) at z = 0 (read only)
J556 = json.load(open(os.path.join(CFG, "CFG556_halo_model_matter_power", "cfg556_results.json")))
J557 = json.load(open(os.path.join(CFG, "CFG557_settling_catchment_derived", "cfg557_tests_results.json")))
J559 = json.load(open(os.path.join(CFG, "CFG559_kinetic_settled_profile", "cfg559_tests_results.json")))
KR = np.array(J556["k"])
def Rsrc(foot):
    d = {"PRIMARY CFG559 kin": J559["halo_model"][foot]["PRIMARY_kin"]["R"],
         "CFG559 full_kin": J559["halo_model"][foot]["VARIANT_full_kin"]["R"],
         "CFG557 TESTED": J557["halo_model"][foot]["TESTED"]["R"],
         "CFG556 census|cen (sharp)": J556["cases"][f"{foot}|census|cen"]["R"],
         "CFG556 census|emg": J556["cases"][f"{foot}|census|emg"]["R"],
         "CFG556 s25 (reported)": J556["cases"][f"{foot}|census|s25"]["R"],
         "CFG556 s55 (reported)": J556["cases"][f"{foot}|census|s55"]["R"],
         "CFG556 fret1 (reported)": J556["cases"][f"{foot}|fret1|cen"]["R"],
         "CFG556 r200scope (reported)": J556["cases"][f"{foot}|census|cen|r200scope"]["R"]}
    return {n: np.array(v, float) for n, v in d.items()}
ONES = np.ones_like(KR)
MAINLINE = ["CFG559 full_kin", "CFG557 TESTED", "CFG556 census|cen (sharp)", "CFG556 census|emg"]
def R_of(Rarr, k):
    """R(k<1e-3) = 1, R(k>10) = R(10), log-k interpolation in between."""
    lk = np.log(np.clip(k, KR[0], KR[-1]))
    r = np.interp(lk, np.log(KR), Rarr)
    return np.where(k < KR[0], 1.0, r)

# ------------------------------------------------------------------ data (recalled, PROVISIONAL)
DATA = {"KiDS": (0.858, 0.052), "DES": (0.82, 0.04)}
S8DATA = {"KiDS": (0.759, 0.024, 0.021), "DES": (0.759, 0.025, 0.023)}
SURV = {"KiDS": dict(zmean=0.67, area=1006.0, neff=6.17, se=0.265), "DES": dict(zmean=0.63, area=4143.0, neff=5.59, se=0.261)}

# ------------------------------------------------------------------ CAMB
H0, OMBH2, OMCH2, NS, S8T = 67.36, 0.02237, 0.1200, 0.965, 0.811
h = H0 / 100; OM = (OMBH2 + OMCH2) / h ** 2
TFULL = [round(7.3 + 0.1 * i, 1) for i in range(11)]
TFID = [t for t in TFULL if 7.6 - 1e-9 <= t <= 8.0 + 1e-9]
TSEARCH = [round(7.0 + 0.1 * i, 1) for i in range(21)]
def camb_pk(T=None, s8=S8T):
    p = camb.CAMBparams(); p.set_cosmology(H0=H0, ombh2=OMBH2, omch2=OMCH2, mnu=0.0, omk=0, num_massive_neutrinos=0)
    p.InitPower.set_params(ns=NS, As=2.1e-9); p.set_matter_power(redshifts=[0.0], kmax=60)
    r = camb.get_results(p); As = 2.1e-9 * (s8 / r.get_sigma8_0()) ** 2
    p.InitPower.set_params(ns=NS, As=As)
    if T is None: p.NonLinearModel.set_params(halofit_version="mead2020")
    else: p.NonLinearModel.set_params(halofit_version="mead2020_feedback", HMCode_logT_AGN=T)
    pnl = camb.get_matter_power_interpolator(p, nonlinear=True, hubble_units=True, k_hunit=True, kmax=60, zmax=3.5)
    pl = camb.get_matter_power_interpolator(p, nonlinear=False, hubble_units=True, k_hunit=True, kmax=60, zmax=3.5)
    r = camb.get_results(p)
    return pnl, pl, r
P("CFG590: framework matter power vs cosmic shear, identical HMcode-2020 feedback on both models" + (" [MUTATE]" if MUT else ""))
P("kappa = 1/2 FITTED; footings never pooled; flat a0; nu_mono; candidate B; cold energy MASS still required; not theory closed.")
P(f"CAMB {camb.__version__}; HMcode-2020 DMO base; cosmology h {h}, wb {OMBH2}, wc {OMCH2}, ns {NS}, sigma8 {S8T}")
PNL, PL, RES = camb_pk()
s8chk = float(RES.get_sigma8_0())
FB = {}
for T in TSEARCH:
    try: FB[T] = camb_pk(T)[0]
    except Exception as e: P(f"  feedback T = {T}: CAMB failed ({e})")
P(f"  C1 sigma8(z=0) = {s8chk:.5f} -> {'PASS' if abs(s8chk - S8T) < 1e-3 else 'FAIL'}")
CHI = lambda z: RES.comoving_radial_distance(z) * h       # Mpc/h

# ------------------------------------------------------------------ Limber machinery
ZG = np.linspace(0.005, 3.0, 300); CHIG = np.array([CHI(z) for z in ZG]); AG = 1 / (1 + ZG)
def nz(zmean):
    z0 = zmean / (math.gamma(4 / 1.5) / math.gamma(3 / 1.5))
    n = ZG ** 2 * np.exp(-(ZG / z0) ** 1.5); return n / np.trapz(n, ZG)
def kernel(zmean):
    n = nz(zmean); dchidz = np.gradient(CHIG, ZG); nchi = n / dchidz          # per unit chi
    q = np.array([np.trapz(np.where(CHIG >= c, nchi * (CHIG - c) / CHIG, 0), CHIG) for c in CHIG])
    q *= 1.5 * OM * (1 / 2997.92458) ** 2 * CHIG / AG
    return q ** 2 / CHIG ** 2                                                   # integrand weight per d chi
SETUP_CACHE = {}
def setup(surv, lmax=2000, dz=0.0):
    key = (surv, lmax, dz)
    if key in SETUP_CACHE: return SETUP_CACHE[key]
    s = SURV[surv]; ell = np.geomspace(100, lmax, 24); W = kernel(s["zmean"] + dz)
    kk = (ell[:, None] + 0.5) / CHIG[None, :]                                   # [ell, z]
    def Cl(Pz):  # Pz(z, k-array) -> C_ell
        Pm = np.array([Pz(ZG[j], kk[:, j]) for j in range(len(ZG))]).T
        return np.trapz(W[None, :] * Pm, CHIG, axis=1)
    pnl = np.array([PNL.P(ZG[j], kk[:, j]) for j in range(len(ZG))]).T
    pl = np.array([PL.P(ZG[j], kk[:, j]) for j in range(len(ZG))]).T
    sfb = {T: np.array([FB[T].P(ZG[j], kk[:, j]) for j in range(len(ZG))]).T / pnl for T in FB}
    CNL = np.trapz(W[None, :] * pnl, CHIG, axis=1); CL = np.trapz(W[None, :] * pl, CHIG, axis=1)
    fsky = s["area"] / 41252.96; nsr = s["neff"] * (180 * 60 / math.pi) ** 2; N = s["se"] ** 2 / nsr
    dl = ell * np.log(ell[1] / ell[0])
    var = 2.0 / ((2 * ell + 1) * dl * fsky) * (CNL + N) ** 2
    out = dict(ell=ell, kk=kk, W=W, pnl=pnl, pl=pl, sfb=sfb, CNL=CNL, CL=CL, w=1 / var)
    SETUP_CACHE[key] = out; return out
def A_fit(S, Cm):
    d = S["CNL"] - S["CL"]
    return float(np.sum(S["w"] * (Cm - S["CL"]) * d) / np.sum(S["w"] * d * d))
def C_model(S, Rarr, T):
    Rm = R_of(Rarr if Rarr is not None else ONES, S["kk"])      # LCDM uses the same code path with R = 1
    Sf = S["sfb"][T] if T is not None else 1.0
    return np.trapz(S["W"][None, :] * Rm * Sf * S["pnl"], CHIG, axis=1)
def A_M1(surv, Rarr, T, lmax=2000, dz=0.0):
    S = setup(surv, lmax, dz); return A_fit(S, C_model(S, Rarr, T))
# M2: k = 1, 2, 4 at z = 0.5
K2 = np.array([1.0, 2.0, 4.0])
def A_M2(Rarr, T):
    pnl = PNL.P(0.5, K2); pl = PL.P(0.5, K2)
    sf = FB[T].P(0.5, K2) / pnl if T is not None else 1.0
    Rm = R_of(Rarr if Rarr is not None else ONES, K2)
    return float(np.mean((Rm * sf * pnl - pl) / (pnl - pl)))

def Zs(Afun, Rarr, T):
    return {d: (Afun(d, Rarr, T) - m) / s for d, (m, s) in DATA.items()}
def classify(zmax_by_T):
    v = list(zmax_by_T.values())
    if all(x >= 3 for x in v): return "EXCLUDED"
    if all(x >= 2 for x in v): return "TENSION"
    return "CONSISTENT"
def judge(Rarr, mapping="M1", lmax=2000, dz=0.0, Ts=TFULL):
    if mapping == "M1": Af = lambda d, R, T: A_M1(d, R, T, lmax, dz)
    else: Af = lambda d, R, T: A_M2(R, T)
    tab = {T: Zs(Af, Rarr, T) for T in Ts}
    zmax = {T: max(abs(x) for x in z.values()) for T, z in tab.items()}
    return classify(zmax), tab, zmax

# ------------------------------------------------------------------ controls
S0 = setup("KiDS")
c2 = max(abs(A_fit(S0, S0["CNL"]) - 1), abs(A_fit(S0, S0["CL"])))
P(f"  C2 fit identity |A(C_NL) - 1|, |A(C_L)|: {c2:.1e} -> {'PASS' if c2 < 1e-9 else 'FAIL'}")
alc = [A_M1("KiDS", None, T) for T in TFULL]
c3 = all(alc[i + 1] < alc[i] for i in range(len(alc) - 1))
P(f"  C3 LCDM A_eff decreasing in T over [7.3, 8.3]: {c3}")
RS = {f: Rsrc(f) for f in ("canonical", "alt")}
c4 = max(abs(float(R_of(v, np.array([1e-3]))[0]) - 1) for f in RS for v in RS[f].values())
P(f"  C4 max |R(1e-3) - 1| over inputs: {c4:.2e} -> {'PASS' if c4 < 1e-3 else 'FAIL'}")
CONTROLS = dict(C1=s8chk, C1_pass=abs(s8chk - S8T) < 1e-3, C2=c2, C2_pass=c2 < 1e-9, C3_pass=c3, C4=c4, C4_pass=c4 < 1e-3)

# ------------------------------------------------------------------ feedback-needed search
def crossings(Afun_d, Rarr, d):
    m, s = DATA[d]; Ts = [T for T in TSEARCH if T in FB]
    z = np.array([(Afun_d(d, Rarr, T) - m) / s for T in Ts])
    def root(level):
        for i in range(len(Ts) - 1):
            if (z[i] - level) * (z[i + 1] - level) <= 0 and z[i] != z[i + 1]:
                return float(Ts[i] + (level - z[i]) * (Ts[i + 1] - Ts[i]) / (z[i + 1] - z[i]))
        return None
    return dict(T_at_Z0=root(0.0), T_at_Zp2=root(2.0), T_at_Zm2=root(-2.0), T_at_Zp3=root(3.0), Z_at_T={str(T): float(x) for T, x in zip(Ts, z)})
def sfb_k1(T):
    if T is None: return None
    Tl = max([t for t in FB if t <= T], default=None); Tu = min([t for t in FB if t >= T], default=None)
    if Tl is None or Tu is None: return None
    a = FB[Tl].P(0.5, 1.0) / PNL.P(0.5, 1.0); b = FB[Tu].P(0.5, 1.0) / PNL.P(0.5, 1.0)
    return float(a if Tu == Tl else a + (b - a) * (T - Tl) / (Tu - Tl))

# ------------------------------------------------------------------ S8-equivalent
S8_GRID = np.linspace(0.70, 0.95, 11)
S8_PKS = {}
def amp(S, Cm):
    return float(np.sum(S["w"] * Cm * S["CNL"]) / np.sum(S["w"] * S["CNL"] ** 2))
def s8eq(surv, Rarr, T):
    S = setup(surv)
    if not S8_PKS:
        for s8 in S8_GRID: S8_PKS[float(s8)] = camb_pk(None, float(s8))[0]
    a_m = amp(S, C_model(S, Rarr, T))
    a_g = []
    for s8 in S8_GRID:
        pk = S8_PKS[float(s8)]
        pm = np.array([pk.P(ZG[j], S["kk"][:, j]) for j in range(len(ZG))]).T
        a_g.append(amp(S, np.trapz(S["W"][None, :] * pm, CHIG, axis=1)))
    sig = float(np.interp(a_m, a_g, S8_GRID))
    return sig * math.sqrt(OM / 0.3)

# ------------------------------------------------------------------ main evaluation
RESULT = dict(lane="CFG590", date="2026-10-10", mutate=MUT, camb=camb.__version__, data=DATA, data_S8=S8DATA, surveys=SURV,
              T_full=TFULL, T_fid=TFID, controls=CONTROLS, models={})
def full_report(name, Rarr, do_s8=False, do_sys=True):
    r = {}
    P(f"\n--- {name} ---")
    # A_eff tables
    rows = {}
    for T in [None] + TFULL:
        rows["off" if T is None else str(T)] = {"A_M1_KiDS": A_M1("KiDS", Rarr, T), "A_M1_DES": A_M1("DES", Rarr, T), "A_M2": A_M2(Rarr, T)}
    for key in ("off", "7.3", "7.6", "7.8", "8.0", "8.3"):
        x = rows[key]; zk = (x["A_M1_KiDS"] - DATA["KiDS"][0]) / DATA["KiDS"][1]; zd = (x["A_M1_DES"] - DATA["DES"][0]) / DATA["DES"][1]
        P(f"  feedback {key:>4s}: A_eff M1 KiDS {x['A_M1_KiDS']:.3f} (Z {zk:+.2f})  DES {x['A_M1_DES']:.3f} (Z {zd:+.2f})   M2 {x['A_M2']:.3f}")
    r["A_table"] = rows
    cls, tab, zmax = judge(Rarr)
    clsoff, taboff, _ = judge(Rarr, Ts=[None])
    r["class_M1"] = cls; r["class_feedback_off"] = clsoff; r["Zmax_by_T"] = {str(k): v for k, v in zmax.items()}
    r["Z_by_T"] = {str(k): v for k, v in tab.items()}
    fidok = any(zmax[T] < 2 for T in TFID); r["consistent_T_in_fiducial"] = fidok
    r["consistent_T"] = [T for T in TFULL if zmax[T] < 2]
    P(f"  M1 class over [7.3, 8.3]: {cls}  (min Zmax {min(zmax.values()):.2f} at T {min(zmax, key=zmax.get)}; |Z|<2 at T = {r['consistent_T']}; inside fiducial: {fidok}); feedback off: {clsoff}")
    if do_sys:
        sysc = {"M2": judge(Rarr, "M2")[0], "lmax1000": judge(Rarr, lmax=1000)[0], "lmax3000": judge(Rarr, lmax=3000)[0],
                "nz-0.1": judge(Rarr, dz=-0.1)[0], "nz+0.1": judge(Rarr, dz=+0.1)[0]}
        r["systematics_classes"] = sysc
        nd = any(v != cls for v in sysc.values())
        r["final_class"] = "NOT DIAGNOSTIC" if nd else cls
        P(f"  mapping systematics: {sysc} -> final class {r['final_class']}")
    cr = {d: crossings(lambda dd, R, T: A_M1(dd, R, T), Rarr, d) for d in DATA}
    for d in DATA:
        c = cr[d]; c["S_fb_k1_z05_at_T0"] = sfb_k1(c["T_at_Z0"]) if c["T_at_Z0"] is not None else None
        out = (c["T_at_Z0"] is not None and not (7.3 <= c["T_at_Z0"] <= 8.3))
        P(f"  feedback needed ({d}): Z = 0 at log T_AGN = {c['T_at_Z0'] if c['T_at_Z0'] is None else round(c['T_at_Z0'], 3)}"
          f"{' (OUTSIDE calibration)' if out else ''}; Z = +2 at {c['T_at_Zp2'] if c['T_at_Zp2'] is None else round(c['T_at_Zp2'], 3)}"
          f"; Z = -2 at {c['T_at_Zm2'] if c['T_at_Zm2'] is None else round(c['T_at_Zm2'], 3)}; S_fb(k=1, z=0.5) at Z=0: "
          f"{c['S_fb_k1_z05_at_T0'] if c['S_fb_k1_z05_at_T0'] is None else round(c['S_fb_k1_z05_at_T0'], 3)}")
    r["feedback_needed"] = cr
    if do_s8:
        r["S8_eq"] = {d: {"off": s8eq(d, Rarr, None), "7.8": s8eq(d, Rarr, 7.8)} for d in DATA}
        P("  S8-equivalent: " + "; ".join(f"{d} off {v['off']:.3f}, T7.8 {v['7.8']:.3f}" for d, v in r["S8_eq"].items()) + "  (data 0.759; base Planck-like " + f"{S8T * math.sqrt(OM / 0.3):.3f})")
    return r

if not MUT:
    RESULT["models"]["LCDM-DMO"] = full_report("LCDM (R = 1), same feedback", None, do_s8=True)
    lc = RESULT["models"]["LCDM-DMO"]
    for foot in ("canonical", "alt"):
        P(f"\n===================== footing {foot} =====================")
        for n, Rarr in RS[foot].items():
            prim = n.startswith("PRIMARY")
            rr = full_report(f"{foot} | {n}", Rarr, do_s8=prim, do_sys=prim or n in MAINLINE)
            # excess over LCDM at the same T
            rr["dA_vs_LCDM_M1"] = {T: {d: rr["A_table"][T][f"A_M1_{d}"] - lc["A_table"][T][f"A_M1_{d}"] for d in DATA} for T in ("off", "7.8")}
            P(f"  excess dA (M1) vs LCDM: off KiDS {rr['dA_vs_LCDM_M1']['off']['KiDS']:+.3f} DES {rr['dA_vs_LCDM_M1']['off']['DES']:+.3f}; T7.8 KiDS {rr['dA_vs_LCDM_M1']['7.8']['KiDS']:+.3f}")
            if prim:
                # z-scaling family R_s = 1 + s(R - 1), reported only: A linear in s at fixed T
                sgrid = np.round(np.arange(0.0, 1.201, 0.01), 2); cls_s = []
                for s in sgrid:
                    zmax = {}
                    for T in TFULL:
                        zz = []
                        for d, (m, sd) in DATA.items():
                            A = lc["A_table"][str(T)][f"A_M1_{d}"] + s * (rr["A_table"][str(T)][f"A_M1_{d}"] - lc["A_table"][str(T)][f"A_M1_{d}"])
                            zz.append(abs((A - m) / sd))
                        zmax[T] = max(zz)
                    cls_s.append(classify(zmax))
                ch = [(float(sgrid[i]), cls_s[i - 1], cls_s[i]) for i in range(1, len(sgrid)) if cls_s[i] != cls_s[i - 1]]
                rr["s_class_changes"] = ch
                P(f"  z-scaling family R_s (reported only): class changes at s = {ch}")
            RESULT["models"][f"{foot}|{n}"] = rr
        prim = RESULT["models"][f"{foot}|PRIMARY CFG559 kin"]
        vs = {n: RESULT["models"][f"{foot}|{n}"]["class_M1"] for n in MAINLINE}
        prim["variant_classes"] = vs; prim["variant_sensitive"] = any(v != prim["class_M1"] for v in vs.values())
        P(f"\n  VERDICT [{foot}] framework PRIMARY: {prim['final_class']} (M1 {prim['class_M1']}); mainline variants {vs}"
          f"{' -> VARIANT-SENSITIVE' if prim['variant_sensitive'] else ''}")
    P(f"\n  VERDICT LCDM-DMO (same rule, same feedback): {lc['final_class']} (M1 {lc['class_M1']})")
    RESULT["verdict"] = {"LCDM-DMO": lc["final_class"], **{f: RESULT["models"][f"{f}|PRIMARY CFG559 kin"]["final_class"] for f in ("canonical", "alt")}}
else:
    teeth = {}
    lc_cls, lc_tab, _ = judge(None)
    # MU1: R = 1 reproduces LCDM exactly
    one = np.ones_like(KR); m1_cls, m1_tab, _ = judge(one)
    d1 = max(abs(A_M1(d, one, T) - A_M1(d, None, T)) for d in DATA for T in [None] + TFULL)
    d1 = max(d1, max(abs(A_M2(one, T) - A_M2(None, T)) for T in [None] + TFULL))
    teeth["MU1"] = bool(d1 == 0.0 and m1_cls == lc_cls)
    P(f"  MU1 R = 1: max |dA| = {d1:.3e}; class {m1_cls} vs LCDM {lc_cls} -> {'BITES' if teeth['MU1'] else 'FAILS'}")
    # MU2: feedback off -> LCDM A = 1; framework = main-run feedback-off row
    a_off = max(abs(A_M1(d, None, None) - 1) for d in DATA)
    main = json.load(open(os.path.join(HERE, "cfg590_results.json")))
    dd = 0.0
    for f in ("canonical", "alt"):
        Rp = RS[f]["PRIMARY CFG559 kin"]
        for d in DATA:
            dd = max(dd, abs(A_M1(d, Rp, None) - main["models"][f"{f}|PRIMARY CFG559 kin"]["A_table"]["off"][f"A_M1_{d}"]))
    teeth["MU2"] = bool(a_off < 1e-9 and dd < 1e-12)
    P(f"  MU2 feedback off: |A_LCDM - 1| = {a_off:.1e}; framework vs main-run off row max |d| = {dd:.1e} -> {'BITES' if teeth['MU2'] else 'FAILS'}")
    # MU3: tooth R = 0.5 at k >= 1
    tooth = np.where(KR >= 1.0, 0.5, 1.0)
    z3 = Zs(lambda d, R, T: A_M1(d, R, T), tooth, 7.3)
    teeth["MU3"] = all(v <= -3 for v in z3.values())
    P(f"  MU3 R = 0.5 (k >= 1), T = 7.3: Z = {{{', '.join(f'{d}: {v:+.2f}' for d, v in z3.items())}}} -> {'BITES' if teeth['MU3'] else 'FAILS'}")
    RESULT["mutate"] = dict(teeth=teeth, MU1_dA=d1, MU1_class=m1_cls, LCDM_class=lc_cls, MU2_A_off=a_off, MU2_dmain=dd, MU3_Z=z3)
    P(f"\nMUTATE: all teeth bite: {all(teeth.values())}")

open(os.path.join(HERE, f"cfg590_shear{SUF}.out"), "w").write("\n".join(OUT) + "\n")
def _clean(o):
    if isinstance(o, dict): return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
json.dump(_clean(RESULT), open(os.path.join(HERE, f"cfg590_results{SUF}.json"), "w"), indent=1)
if MUT: sys.exit(1 if all(RESULT["mutate"]["teeth"].values()) else 0)
