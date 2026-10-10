#!/usr/bin/env python3
"""CFG557 tasks 2 (i), (ii), (iv), (v) and 3 (FROZEN_CRITERIA.md, criteria commit 5149a12f1), with the tested catchment s_c* from
cfg557_derive_results.json (the derivation verdict names it).  One change per source lane: the settled supply x s_c*.
  (i)  CFG556 halo model (cfg556_halo_model.py exec'd read-only up to its run block; frame profile copied with the supply factor)
  (ii) CFG543 P2 groups (cfg543_group_supply imported read-only; per-group supply factor)
  (iv) MW edge through CFG513's Prof (via CFG522's read-only exec of CFG515)
  (v)  CFG522 M1 timing (exec'd read-only up to its main block) + unsettled cold energy kept as a drained-shell mass; CFG548 ZVS from its JSON
  OMP_NUM_THREADS=4 nice -n 10 python3 cfg557_tests.py               -> cfg557_tests.out, cfg557_tests_results.json
  CFG557_MUTATE=1 OMP_NUM_THREADS=4 nice -n 10 python3 cfg557_tests.py -> *_MUTATE.* (MU1, MU2; exit 1 = all teeth bite)
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, io, json, math, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "4")
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import cfg557_lib as L

MUTATE = os.environ.get("CFG557_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
FOOTS = ("canonical", "alt")
JD = json.load(open(os.path.join(HERE, "cfg557_derive_results.json")))
TESTED = JD["verdict"]["tested"]                                   # "ff" (free-fall ceiling) or "a1"
res = dict(lane="CFG557", script="cfg557_tests", date="2026-10-10", mutate=MUTATE, criteria_commit="5149a12f1", tested=TESTED,
           derivation_label=JD["verdict"]["label"],
           settings="kappa = 1/2 FITTED; footings never pooled; nu_mono; candidate B; G9; no EFE; cold energy mass required; not theory closed")
P(f"CFG557 tests {'(MUTATE)' if MUTATE else ''} -- FROZEN_CRITERIA.md (5149a12f1). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
P(f"Derivation verdict: {JD['verdict']['label']}; tested catchment = '{TESTED}'")
E0 = L.Epoch(0.0)

# ====================================================================== (i) CFG556 halo model
P556 = os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
_src = open(P556).read()
_cut = _src.index("# ------------------------------------------------------------------ run")
H = {"__file__": P556, "__name__": "cfg556_ro"}
_e = os.environ.pop("CFG556_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_cut], "cfg556_ro", "exec"), H)
if _e is not None:
    os.environ["CFG556_MUTATE"] = _e
HB, MTA, KK, U_set, U_std, spectra_ta, spectra_std, s8_of = (H[k] for k in ("HB", "MTA", "KK", "U_set", "U_std", "spectra_ta", "spectra_std", "s8_of"))
M_L, baryon_cum, rgrid, nu_k, fret_of = H["M_L"], H["baryon_cum"], H["rgrid"], H["nu_k"], H["fret_of"]
G, h, FB, A0MPC = H["G"], H["h"], H["FB"], H["A0MPC"]
assert np.allclose(np.log10(MTA), JD["grid"]["canonical"]["log10_Mta"], atol=1e-10, rtol=0), "mass grid mismatch with the derivation grid"

def frame_profile_sc(hb, foot, sc):
    """cfg556 frame_profile (edge = cen, census f_ret, mode = normal) copied verbatim, with ONE change: supply = sc (1 - f_b) M_ta, so
    r_e = r_M / ln(1 + f f_b / ((1 - f_b) sc)).  sc = 0: nothing settles; the declared limit is the L-ta profile (FROZEN MU2)."""
    r = rgrid(hb, hb["rta"]); Mta = hb["Mta"]; ML = M_L(hb, r)
    f = fret_of(math.log10(Mta))
    if sc <= 0.0:
        return r, ML.copy(), dict(re=0.0, q=0.0, capped=False, fret=f)
    Mb = f * FB * Mta; supply = sc * (1 - FB) * Mta; a0 = A0MPC[foot]
    rM = math.sqrt(G * Mb * h / a0)
    re = rM / math.log1p(f * FB / ((1 - FB) * sc))
    capped = re >= hb["rta"]
    re = min(re, hb["rta"])
    r = np.unique(np.concatenate([r, [re]])); ML = M_L(hb, r)
    mb = baryon_cum(hb, Mb, r, re)
    y = G * mb * h / (np.maximum(r, 1e-30) ** 2 * a0)
    Min = np.where(r > 0, mb * nu_k(y), 0.0)
    iout = np.searchsorted(r, re)
    Mout = Min[iout]; MLout = ML[iout]
    if capped or MLout >= Mta * (1 - 1e-12):
        rem = max(Mta - Min[-1], 0.0)
        MF = Min + rem * ML / Mta; q = 0.0
    else:
        MF = np.where(r <= re, Min, Mout + (Mta - Mout) * (ML - MLout) / (Mta - MLout))
        q = 1.0 - (Mta - Mout) / (Mta - MLout)
    return r, MF, dict(re=re, q=q, capped=capped, fret=f, supply=supply)

Ustd = U_std(); Pstd, _, _ = spectra_std(Ustd)
Ulta, _ = U_set(lambda hb: (lambda r: (r, M_L(hb, r), {}))(rgrid(hb, hb["rta"])))
Plta, _, _ = spectra_ta(Ulta)
W8K = H["_W8"](KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
KSEL = [0.05, 0.1, 0.2, 0.3, 0.35, 0.5, 0.7, 1.0, 2.0, 3.0]
J556 = json.load(open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_results.json")))

def hm_case(foot, scs, label):
    U, infos = U_set(lambda hb, _it=iter(scs): frame_profile_sc(hb, foot, next(_it)))
    PF, _, IF = spectra_ta(U)
    R = 1 + (PF - Plta) / Pstd; Rr = PF / Plta
    s8F = math.sqrt(s8_of(Pstd) ** 2 + np.trapz((PF - Plta) * W8K, KK)); s8r = s8F / s8_of(Pstd)
    m = (KK >= 0.05) & (KK <= 1.0)
    E, D = float(np.max(R[m] - 1)), float(np.min(R[m] - 1)); mx = max(abs(E), abs(D))
    o = dict(label=label, R=R.tolist(), E=E, D=D, maxdev=mx, kE=float(KK[m][np.argmax(R[m])]), kD=float(KK[m][np.argmin(R[m])]),
             E_ratio=float(np.max(Rr[m] - 1)), D_ratio=float(np.min(Rr[m] - 1)), s8_ratio=s8r,
             R_at={str(k): float(np.interp(k, KK, R)) for k in KSEL}, I_k1e3=float(IF[np.argmin(abs(KK - 1e-3))]),
             q_at={str(l): float(np.interp(l, np.log10(MTA), [i["q"] for i in infos])) for l in (12, 13, 14, 15)},
             re_over_rta_at={str(l): float(np.interp(l, np.log10(MTA), [i["re"] / hb["rta"] for i, hb in zip(infos, HB)])) for l in (12, 13, 14, 15)},
             passed=bool(mx <= 0.10 and abs(s8r - 1) <= 0.05))
    # drivers by log M_ta decade at k = 1 (one-halo + two-halo, exact decomposition as CFG556)
    j = int(np.argmin(abs(KK - 1.0))); W_M, BIAS, RHO_M, NORM_TA, PL = H["W_M"], H["BIAS"], H["RHO_M"], H["NORM_TA"], H["PL"]
    _, _, Il = spectra_ta(Ulta)
    d1 = W_M * ((U[:, j] / RHO_M) ** 2 - (Ulta[:, j] / RHO_M) ** 2)
    d2 = PL[j] * (IF[j] + Il[j]) * W_M * BIAS * (U[:, j] - Ulta[:, j]) / RHO_M / NORM_TA
    o["drivers_k1"] = {f"{lo}-{lo + 1}": float((d1 + d2)[(np.log10(MTA) >= lo) & (np.log10(MTA) < lo + 1)].sum() / Pstd[j]) for lo in range(10, 16)}
    return o, U, infos

def prof_ratios(foot, scs):
    out = {}
    for lt in (12, 13, 14, 15):
        i = int(np.argmin(abs(np.log10(MTA) - lt))); hb = HB[i]
        r, Mc, inf = frame_profile_sc(hb, foot, scs[i])
        out[str(lt)] = {str(x): float(np.interp(x * hb["rta"], r, Mc) / M_L(hb, x * hb["rta"])) for x in (0.05, 0.1, 0.2, 0.3, 0.5, 1.0)}
        out[str(lt)].update(sc=float(scs[i]), re_over_rta=float(inf["re"] / hb["rta"]))
    return out

res["halo_model"] = {}
if not MUTATE:
    P("\n(i) CFG556 halo model with the settled supply x s_c*(M_ta).  R = 1 + (P_F,ta - P_L,ta)/P_L,std; PASS iff max|R-1| <= 0.10 (0.05-1 h/Mpc) AND |s8 ratio - 1| <= 0.05")
    for ft in FOOTS:
        g = JD["grid"][ft]; res["halo_model"][ft] = {}
        cases = [("TESTED", g[TESTED]), ("context_alpha1", g["a1"]), ("context_alpha05", g["a05"]),
                 ("context_b_M200m", [hb["M"] / hb["Mta"] for hb in HB]), ("context_turnaround_sc1", [1.0] * len(HB))]
        for nm, scs in cases:
            o, _, _ = hm_case(ft, scs, nm)
            res["halo_model"][ft][nm] = o
            tag = ("PASS" if o["passed"] else "FAIL") if nm == "TESTED" else "(context)"
            P(f"  [{ft:9s}] {nm:24s} E {o['E']:+.3f} (k {o['kE']:.2f})  D {o['D']:+.3f} (k {o['kD']:.2f})  ratio-form {o['E_ratio']:+.3f}/{o['D_ratio']:+.3f}  "
              f"s8 ratio {o['s8_ratio']:.4f}  -> {tag}")
            P("        R(k): " + "  ".join(f"{k}:{v:.3f}" for k, v in o["R_at"].items()) + "  | k=1 drivers by log M_ta: "
              + " ".join(f"{d}:{v:+.3f}" for d, v in o["drivers_k1"].items() if abs(v) > 5e-4))
            if nm == "TESTED":
                P("        r_e/r_ta at log M_ta 12/13/14/15: " + "/".join(f"{o['re_over_rta_at'][str(l)]:.3f}" for l in (12, 13, 14, 15))
                  + "; shell depletion q: " + "/".join(f"{o['q_at'][str(l)]:.2f}" for l in (12, 13, 14, 15)))
        pr = prof_ratios(ft, g[TESTED]); res["halo_model"][ft]["profile_ratios_TESTED"] = pr
        for lt, v in pr.items():
            P(f"        M_F/M_L logM_ta {lt} (s_c {v['sc']:.3f}, r_e/r_ta {v['re_over_rta']:.3f}): " + " ".join(f"{x}:{v[x]:.2f}" for x in ("0.05", "0.1", "0.2", "0.3", "0.5", "1.0")))
else:
    P("\nMU1 / MU2 halo model")
    teeth = {}
    for ft in FOOTS:
        o1, _, _ = hm_case(ft, [1.0] * len(HB), "MU1_sc1")
        R556 = np.array(J556["cases"][f"{ft}|census|cen"]["R"]); dR = float(np.max(np.abs(np.array(o1["R"]) - R556)))
        ds8 = abs(o1["s8_ratio"] - J556["cases"][f"{ft}|census|cen"]["s8_ratio"])
        o0, _, _ = hm_case(ft, [0.0] * len(HB), "MU2_sc0")
        d0 = float(np.max(np.abs(np.array(o0["R"]) - 1)))
        # information only: s_c -> 1e-6 through the general E-cen path (baryons compressed inside a vanishing edge)
        oe, _, _ = hm_case(ft, [1e-6] * len(HB), "info_sc1e-6")
        teeth[ft] = dict(MU1_maxdR=dR, MU1_ds8=ds8, MU1_bites=dR <= 1e-10 and ds8 <= 1e-10, MU2_maxdev=d0, MU2_bites=d0 <= 1e-10,
                         info_sc1e6_E=oe["E"], info_sc1e6_D=oe["D"])
        P(f"  [{ft}] MU1 s_c=1 vs CFG556 primary: max|dR| {dR:.1e}, |ds8| {ds8:.1e} -> {'BITES' if teeth[ft]['MU1_bites'] else 'FAILS'};  "
          f"MU2 s_c=0: max|R-1| {d0:.1e} -> {'BITES' if teeth[ft]['MU2_bites'] else 'FAILS'};  (info: s_c=1e-6 via the E-cen path E {oe['E']:+.3f} D {oe['D']:+.3f})")
    res["teeth_halo_model"] = teeth

# ====================================================================== (ii) CFG543 P2 groups
sys.path.insert(0, os.path.join(LANES, "CFG543_group_supply"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg543_group_supply as M43                                                     # noqa: E402  (read-only; main guarded)
M43.GEO = M43.gas_geometry(M43.lovisari())
ROWS = M43.read_groups()
C40 = M43.C
J543 = json.load(open(os.path.join(LANES, "CFG543_group_supply", "cfg543_results.json")))
J543M = json.load(open(os.path.join(LANES, "CFG543_group_supply", "cfg543_results_MUTATE.json")))
FMAP = {"can": "canonical", "alt": "alt"}

def group_sc(o, foot, mode="TESTED"):
    Mb = 10 ** o["lM"]                                           # Msun
    Mta_h = Mb / (0.10 * L.FB) * L.h; Mb_h = Mb * L.h
    a = math.inf if TESTED == "ff" else 1.0
    if mode == "progenitor":
        lt = 12.0; Mta_p = 10 ** lt; Mb_p = 0.10 * L.FB * Mta_p
        return L.s_catch(E0, Mta_p, Mb_p, foot, a)
    return L.s_catch(E0, Mta_h, Mb_h, foot, a)

def run_groups(a0, scs, cfg):
    lp = np.array([M43.sigma_log(o, a0, cfg, 0.0, s) for o, s in zip(ROWS, scs)])
    lp2 = np.array([M43.sigma_log(o, a0, cfg, 0.01, s) for o, s in zip(ROWS, scs)])
    sl = (lp2 - lp) / 0.01
    D = np.array([o["ls"] for o in ROWS]) - lp
    return M43.stats(D, sl)

def p2_aperture_sc(o, a0, k, sc):
    """cfg543_addendum.p2_aperture copied, with ONE change: Msup x sc."""
    Mc = 10 ** o["lM"]; Msup = M43.COLD_PER_B * Mc / 0.10 * sc
    Re = o["Re"] / k; a = Re * C40.KPC / C40.HERN_RE; GM = C40.G * Mc * C40.MSUN; a0d = a0 * a * a / GM
    rho, m = C40.prof("hern", C40.X); gN = m / C40.X ** 2; mph = (C40.nu(gN / a0d) - 1) * gN * C40.X ** 2
    kk = np.where(mph >= Msup / Mc)[0]; xe = None if not len(kk) else float(C40.X[kk[0]])
    return 0.5 * math.log10(C40.sigma2("hern", a0d, 0.0, o["Re"] * C40.KPC / a, xe) * GM / a) - 3.0

res["groups"] = {}
if not MUTATE:
    P("\n(ii) CFG543 P2 groups (Tian+26 M_bar = stars + observed X-ray gas, complete; containment supply) with supply x s_c*(M_ta,group); PASS iff |Z| < 2")
    for fk, a0 in M43.FOOT.items():
        ft = FMAP[fk]
        scs = np.array([group_sc(o, ft) for o in ROWS])
        st = run_groups(a0, scs, dict(kind="P2"))
        st1 = run_groups(a0, np.ones(len(ROWS)), dict(kind="P2"))
        scp = np.array([group_sc(o, ft, "progenitor") for o in ROWS])
        stp = run_groups(a0, scp, dict(kind="P2"))
        kc20 = 1.5627                                               # addendum k(c = 20), recomputed below
        try:
            from scipy.integrate import quad
            mm = 20 ** 2 / 21 ** 2; kc20 = (math.pi / 4) * quad(lambda r: r * 2 * r / (1 + r) ** 3, 0, 20, limit=200)[0] / mm / M43.HERN_RE
        except Exception:
            pass
        ls = np.array([o["ls"] for o in ROWS]); ap = {}
        for kn, k in (("k1", 1.0), ("k_c20", kc20)):
            lp = np.array([p2_aperture_sc(o, a0, k, s) for o, s in zip(ROWS, scs)]); D = ls - lp
            ap[kn] = dict(k=k, mean=float(D.mean()), se=float(D.std(ddof=1) / math.sqrt(len(D))))
        st_k = run_groups(a0, scs, dict(kind="P2", k=kc20))
        res["groups"][ft] = dict(TESTED=st, sc_median=float(np.median(scs)), sc_min=float(scs.min()), sc_max=float(scs.max()),
                                 sc1_check=st1, cfg543_P2=J543["footings"][fk]["configs"]["P2"]["mean"], progenitor_sc=stp,
                                 aperture=ap, Re_over_k_c20=st_k, passed=bool(abs(st["Z"]) < 2))
        P(f"  [{ft:9s}] s_c* median {np.median(scs):.3f} ({scs.min():.3f}-{scs.max():.3f}); P2 x s_c*: mean {st['mean']:+.3f} Z {st['Z']:+.2f} -> {st['label']} "
          f"-> {'PASS' if abs(st['Z']) < 2 else 'FAIL'}   (s_c = 1: {st1['mean']:+.4f}, CFG543 {J543['footings'][fk]['configs']['P2']['mean']:+.4f})")
        P(f"        reported: s_c at a log M_ta 12 progenitor ({np.median(scp):.3f}): mean {stp['mean']:+.3f} Z {stp['Z']:+.2f}; R_e = Re/{kc20:.3f}: {st_k['mean']:+.3f} Z {st_k['Z']:+.2f}; "
              f"aperture R<Re k=1: {ap['k1']['mean']:+.3f} +- {ap['k1']['se']:.3f} (SE), k(c20): {ap['k_c20']['mean']:+.3f} +- {ap['k_c20']['se']:.3f}")
else:
    P("\nMU1 / MU2 groups (P2)")
    tg = {}
    for fk, a0 in M43.FOOT.items():
        ft = FMAP[fk]
        st1 = run_groups(a0, np.ones(len(ROWS)), dict(kind="P2")); ref = J543["footings"][fk]["configs"]["P2"]["mean"]
        st0 = run_groups(a0, np.zeros(len(ROWS)), dict(kind="P2")); refN = J543M["footings"][fk]["mutate"]["M3_P2"]["mean"]
        tg[ft] = dict(MU1_mean=st1["mean"], ref=ref, MU1_bites=abs(st1["mean"] - ref) <= 1e-4, MU2_mean=st0["mean"], refN=refN, MU2_bites=abs(st0["mean"] - refN) <= 0.005)
        P(f"  [{ft}] MU1 s_c=1: {st1['mean']:+.5f} vs CFG543 P2 {ref:+.5f} -> {'BITES' if tg[ft]['MU1_bites'] else 'FAILS'};  MU2 s_c=0: {st0['mean']:+.4f} vs CFG543 Newtonian P2 {refN:+.4f} -> {'BITES' if tg[ft]['MU2_bites'] else 'FAILS'}")
    res["teeth_groups"] = tg

# ====================================================================== (v)+(iv) CFG522 machinery (LG timing; MW edge via Prof)
P522 = os.path.join(LANES, "CFG522_local_group_timing", "cfg522_lg_timing.py")
_src = open(P522).read()
_mk = "fM, f31 = L.fret_census(MB_PRIM)[0], L.fret_census(MB_M31)[0]"
assert _src.count(_mk) == 1
K = {"__file__": P522, "__name__": "cfg522_ro"}
_e = os.environ.pop("CFG522_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_src.index(_mk)], "cfg522_ro", "exec"), K)
if _e is not None:
    os.environ["CFG522_MUTATE"] = _e
Pair, full_stats, Prof, L15 = K["Pair"], K["full_stats"], K["Prof"], K["L"]
MB_PRIM, MB_M31, D_LG, COLD = K["MB_PRIM"], K["MB_M31"], K["D_LG"], K["COLD"]
H16 = L15.H16
fLG = L15.fret_census(MB_PRIM + MB_M31)[0]
J522 = json.load(open(os.path.join(LANES, "CFG522_local_group_timing", "cfg522_results.json")))
J548 = json.load(open(os.path.join(LANES, "CFG548_local_group_zero_velocity_surface", "cfg548_results.json")))
LM200 = np.array(JD["grid"]["canonical"]["log10_M200m"]); LMTA = np.array(JD["grid"]["canonical"]["log10_Mta"])
halo_basics = H["halo_basics"]

def sc_obj(Mta_h, Mb_h, foot):
    return L.s_catch(E0, Mta_h, Mb_h, foot, math.inf if TESTED == "ff" else 1.0)

class ShellPair:
    """CFG522 Pair (M1 shared catchment) with settled supply x s_i and the unsettled cold energy (1 - s_i) kept as mass in the
    drained-shell shape (M_L of the extended NFW of M_ta,i between r_e,i and r_ta,i)."""
    def __init__(self, foot, s_mw, s_m31, shell=True):
        self.p = Pair(foot, MB_PRIM, fLG / s_mw if s_mw > 0 else 1e30, MB_M31, fLG / s_m31 if s_m31 > 0 else 1e30)
        d = 10 ** self.p.ld
        self.extra = np.zeros_like(d); self.info = {}
        for nm, prof, Mb, s in (("mw", self.p.mw, MB_PRIM, s_mw), ("m31", self.p.m31, MB_M31, s_m31)):
            Mbt = prof.Mb_tot(); Mta_h = Mbt * H16 / (fLG * L.FB)
            hb = halo_basics(10 ** float(np.interp(math.log10(Mta_h), LMTA, LM200)))
            U = (1 - s) * COLD * Mbt / fLG                                    # Msun
            re_h = prof.redge / 1000.0 * L.h; rta_kpc = hb["rta"] / L.h * 1000.0
            dh = d / 1000.0 * L.h
            MLd = M_L(hb, np.minimum(dh, hb["rta"])); MLe = float(M_L(hb, min(re_h, hb["rta"])))
            frac = np.clip((MLd - MLe) / (hb["Mta"] - MLe), 0.0, 1.0) if re_h < hb["rta"] else np.zeros_like(d)
            sh = U * frac if shell else 0 * frac
            self.extra += sh
            self.info[nm] = dict(s=s, U=U, edge_kpc=prof.redge, rta_kpc=rta_kpc, Mta_Msun=hb["Mta"] / L.h, hb=hb, re_h=re_h)
        self.p.Mc_sc = self.p.Mc_sc + self.extra
        # barycentre / LMC fraction uses each galaxy's total (baryons + settled + unsettled = the s = 1 total)
        self.p.M1 = self.p.mw.Mb_tot() + COLD * self.p.mw.Mb_tot() / fLG
        self.p.M2 = self.p.m31.Mb_tot() + COLD * self.p.m31.Mb_tot() / fLG

def zvs(sp, R0_guess=1440.0):
    """mass inside R0 of the LG barycentre: point-like settled parts + the part of each unsettled shell inside R0 (offset sphere)."""
    pairs = [(v["M"], v["R0_pred"]) for v in J548["pred"]["canonical"].values()]
    lm = np.log([m for m, _ in pairs]); lr = np.log([r for _, r in pairs]); A = np.polyfit(lm, lr, 1)
    R0pred = lambda M: float(np.exp(np.polyval(A, math.log(M))))
    M1, M2 = sp.p.M1, sp.p.M2
    b = {"mw": D_LG * M2 / (M1 + M2), "m31": D_LG * M1 / (M1 + M2)}
    R0 = R0_guess
    for _ in range(100):
        Min = 0.0
        for nm, prof in (("mw", sp.p.mw), ("m31", sp.p.m31)):
            inf = sp.info[nm]; Mset = prof.Mb_tot() + prof.Mcold
            Min += Mset
            if inf["U"] > 0 and inf["re_h"] < inf["hb"]["rta"]:
                rr = np.linspace(inf["re_h"], inf["hb"]["rta"], 800); dM = np.diff(M_L(inf["hb"], rr)); rm = 0.5 * (rr[1:] + rr[:-1]) / L.h * 1000.0
                w = dM / dM.sum(); bb = b[nm]
                cst = (R0 ** 2 - rm ** 2 - bb ** 2) / (2 * rm * bb)
                fin = np.clip((1 + cst) / 2, 0, 1)                     # fraction of the shell at radius rm inside R0 (uniform in cos theta)
                Min += inf["U"] * float(np.sum(w * fin))
        new = R0pred(Min)
        if abs(new - R0) < 1e-3:
            R0 = new; break
        R0 = new
    Wg = J548["weighing"]
    return dict(M_in_R0=Min, R0_pred=R0, Z=(R0 - Wg["R0_meas"]) / Wg["sig_tot"], fit=A.tolist(), M_flow=Wg["M_flow"],
                Z_FM1=J548["pred"]["canonical"]["F-M1 shared catchment"]["Z"])

res["mw"] = {}; res["lg"] = {}
if not MUTATE:
    P("\n(iv) Milky Way edge with the settled supply x s_c* (CFG513 Prof, census f_ret); PASS (unchanged) iff r_e > 30 kpc")
    fM, lMta_mw = L15.fret_census(MB_PRIM)
    for ft in FOOTS:
        s = sc_obj(10 ** lMta_mw, MB_PRIM * H16, ft)
        pr0 = Prof("mw", Mb=MB_PRIM, foot=ft, fret=fM); pr1 = Prof("mw", Mb=MB_PRIM, foot=ft, fret=fM / s)
        res["mw"][ft] = dict(sc=s, edge_census_kpc=pr0.redge, edge_new_kpc=pr1.redge, fret=fM, log10_Mta=lMta_mw, passed=bool(pr1.redge > 30.0))
        P(f"  [{ft:9s}] M_ta,MW 10^{lMta_mw:.3f} Msun/h, f_ret {fM:.3f}, s_c* {s:.3f}: edge {pr0.redge:.0f} -> {pr1.redge:.0f} kpc "
          f"-> {'PASS: CFG532 curves and CFG553 K_z inside 30 kpc unchanged by construction' if pr1.redge > 30 else 'CHANGED'}")

    P("\n(v) Local Group: CFG522 M1 shared catchment, settled supply x s_c* per galaxy share + unsettled cold energy as a drained-shell mass")
    for ft in FOOTS:
        out = {}
        Mbt_mw = Prof("mw", Mb=MB_PRIM, foot=ft, fret=fLG).Mb_tot()
        s_mw = sc_obj(Mbt_mw * H16 / (fLG * L.FB), Mbt_mw * H16, ft)
        s_31 = sc_obj(MB_M31 * H16 / (fLG * L.FB), MB_M31 * H16, ft)
        for nm, shell in (("TESTED", True), ("shell_omitted", False)):
            sp = ShellPair(ft, s_mw, s_31, shell=shell)
            with contextlib.redirect_stdout(io.StringIO()):
                fs = full_stats(sp.p, f"CFG557 {nm}")
            meff = sp.p.Meff(D_LG)
            z = zvs(sp) if shell else None
            out[nm] = dict(z_meas=fs["z_meas"], v_radial=fs["v_radial"], z_full=fs["z_full"], z_full_LMC=fs["z_full_LMC"], sigma_full=fs["sigma_full"],
                           v_vtSal=fs["v_vtSal"], Meff_780=meff, edges=[sp.p.mw.redge, sp.p.m31.redge],
                           s=[s_mw, s_31], U=[sp.info["mw"]["U"], sp.info["m31"]["U"]], rta_kpc=[sp.info["mw"]["rta_kpc"], sp.info["m31"]["rta_kpc"]], zvs=z)
        sp1 = ShellPair(ft, 1.0, 1.0, shell=False)
        with contextlib.redirect_stdout(io.StringIO()):
            fs1 = full_stats(sp1.p, "s=1")
        out["sc1"] = dict(z_meas=fs1["z_meas"], z_full=fs1["z_full"], Meff_780=sp1.p.Meff(D_LG), cfg522_z_full=J522["M1"][ft]["full"]["z_full"])
        out["passed_timing"] = bool(abs(out["TESTED"]["z_full"]) < 2)
        res["lg"][ft] = out
        t, o1 = out["TESTED"], out["shell_omitted"]
        P(f"  [{ft:9s}] s_c* MW {s_mw:.3f}, M31 {s_31:.3f}; edges {t['edges'][0]:.0f}/{t['edges'][1]:.0f} kpc (s=1: {sp1.p.mw.redge:.0f}/{sp1.p.m31.redge:.0f}); "
          f"r_ta {t['rta_kpc'][0]:.0f}/{t['rta_kpc'][1]:.0f} kpc; unsettled {t['U'][0]:.2e}/{t['U'][1]:.2e} Msun")
        P(f"        M_eff(<780 kpc) {t['Meff_780']:.3e} (s=1 {out['sc1']['Meff_780']:.3e}; shell omitted {o1['Meff_780']:.3e})")
        P(f"        timing: v_rad {t['v_radial']:.1f} z_meas {t['z_meas']:+.2f}; z_full {t['z_full']:+.2f} (sigma {t['sigma_full']:.1f}), z_full,LMC {t['z_full_LMC']:+.2f} "
          f"-> {'PASS' if out['passed_timing'] else 'FAIL'}   [s=1: z_meas {out['sc1']['z_meas']:+.2f}, z_full {out['sc1']['z_full']:+.2f} (CFG522 {out['sc1']['cfg522_z_full']:+.2f}); "
          f"shell omitted: z_meas {o1['z_meas']:+.2f}, z_full {o1['z_full']:+.2f}]")
        zz = t["zvs"]
        P(f"        ZVS: M inside R0 {zz['M_in_R0']:.3e} -> R0_pred {zz['R0_pred']:.0f} kpc, Z {zz['Z']:+.2f} (F-M1 {zz['Z_FM1']:+.2f}); flow mass {zz['M_flow']:.2e} "
          f"-> NOT DIAGNOSTIC (CFG548 line); moves toward the flow mass by dZ {zz['Z'] - zz['Z_FM1']:+.2f}")
else:
    P("\nMU1 LG pair, s_c = 1, no shell vs CFG522 M1 z_full")
    tl = {}
    for ft in FOOTS:
        sp1 = ShellPair(ft, 1.0, 1.0, shell=False)
        with contextlib.redirect_stdout(io.StringIO()):
            fs1 = full_stats(sp1.p, "s=1")
        ref = J522["M1"][ft]["full"]["z_full"]
        tl[ft] = dict(z_full=fs1["z_full"], ref=ref, MU1_bites=abs(fs1["z_full"] - ref) <= 0.01)
        P(f"  [{ft}] z_full {fs1['z_full']:+.4f} vs CFG522 {ref:+.4f} -> {'BITES' if tl[ft]['MU1_bites'] else 'FAILS'}")
    res["teeth_lg"] = tl

if MUTATE:
    allb = all(v["MU1_bites"] and v["MU2_bites"] for v in res["teeth_halo_model"].values()) and \
           all(v["MU1_bites"] and v["MU2_bites"] for v in res["teeth_groups"].values()) and all(v["MU1_bites"] for v in res["teeth_lg"].values())
    res["all_teeth_bite"] = bool(allb)
    P(f"\nMUTATE: all teeth bite -> {allb}")
json.dump(res, open(os.path.join(HERE, f"cfg557_tests_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg557_tests{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if res["all_teeth_bite"] else 0)
