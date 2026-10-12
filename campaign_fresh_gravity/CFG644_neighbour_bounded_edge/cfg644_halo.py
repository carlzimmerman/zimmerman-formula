#!/usr/bin/env python3
"""CFG644 T6 (CONTEXT ONLY, LCDM halo model labelled): CFG556's halo model with the settled cold energy of each halo truncated at its
neighbour-bounded radius r_nb, drawn from the halo model's own neighbour statistics.  Criteria: FROZEN_CRITERIA.md (6a03c0870).
CFG556 cfg556_halo_model.py is exec'd read-only up to its run block.  Closing neighbours: halos with M_ta' >= M_ta (Tinker08 number
density, clustering 1 + b b' xi_lin(s), Tinker10 bias, xi from the same P_lin), s >= r_ta + r_ta'; pairwise watershed with the
framework's census profiles; P(r_nb < x) = 1 - exp(-N(<s_x)).  Remainder goes into CFG556's drained shell (its native convention).
MUTATE (CFG644_MUTATE=1): M1 r_nb = inf for every halo -> CFG556 primary R(k) exactly.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg644_halo.py ; CFG644_MUTATE=1 ... (same)
"""
import os, sys, io, json, math, contextlib, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG644_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(10)
except OSError:
    pass
LOG, CHK = [], {}


def Pr(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = dict(ok=bool(ok), msg=msg); Pr(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


Pr(__doc__.split("Run:")[0].strip())
p556 = os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_halo_model.py")
src = open(p556).read()
cut = "# ------------------------------------------------------------------ run"
assert src.count(cut) == 1
os.environ.pop("CFG556_MUTATE", None)
H = {"__file__": p556, "__name__": "cfg556_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(cut)], "cfg556_ro", "exec"), H)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
HB, MTA, MM, KK, W_M, BIAS = H["HB"], H["MTA"], H["MM"], H["KK"], H["W_M"], H["BIAS"]
frame_profile, U_of, U_set, M_L, baryon_cum, nu_k = (H[k] for k in ("frame_profile", "U_of", "U_set", "M_L", "baryon_cum", "nu_k"))
Gh, hh, FB, A0MPC = H["G"], H["h"], H["FB"], H["A0MPC"]
# the CFG556 run block's references, rebuilt verbatim
H["Ustd"] = H["U_std"](); H["Pstd"], H["P1std"], H["Istd"] = H["spectra_std"](H["Ustd"])
H["Ulta"], _ = U_set(lambda hb: frame_profile(hb, "canonical", mode="lta"))
H["Plta"], H["P1lta"], H["Ilta"] = H["spectra_ta"](H["Ulta"])
H["res"] = dict(cases={})
_s2 = src[src.index("KSEL = ["):src.index('FOOTS = ("canonical", "alt")')]                 # CFG556's summarize(), verbatim
exec(compile(_s2, "cfg556_ro_summarize", "exec"), H)
summarize = H["summarize"]
J556 = json.load(open(os.path.join(LANES, "CFG556_halo_model_matter_power", "cfg556_results.json")))


def frame_profile_nb(hb, ft, rnb):
    """CFG556 'cen' census profile with the settled phantom stopped at r_out = min(r_e, r_nb); baryons stay truncated at r_e;
    everything else inside r_ta (unsettled cold energy included) in CFG556's drained shell ~ M_L."""
    r0, MF0, inf0 = frame_profile(hb, ft, edge="cen")
    re = inf0["re"]
    if not np.isfinite(rnb) or rnb >= re:
        return r0, MF0, inf0
    Mta = hb["Mta"]; f = inf0["fret"]; Mb = f * FB * Mta; a0 = A0MPC[ft]
    r = np.unique(np.concatenate([H["rgrid"](hb, hb["rta"]), [re, rnb]]))
    ML = M_L(hb, r)
    mb = baryon_cum(hb, Mb, r, re)
    y = Gh * mb * hh / (np.maximum(r, 1e-30) ** 2 * a0)
    Sph = np.where(r > 0, mb * nu_k(y), 0.0) - mb
    i = np.searchsorted(r, rnb); Sout = Sph[i]; MLo = ML[i]
    Rem = Mta - mb[-1] - Sout
    MF = mb + np.where(r <= rnb, Sph, Sout + Rem * (ML - MLo) / (Mta - MLo))
    return r, MF, dict(inf0, rout=rnb)


# ------------------------------------------------------------------ framework census pull profiles on a common log-r grid
LR = np.linspace(math.log(1e-4), math.log(200.0), 900); RR = np.exp(LR); DLR = LR[1] - LR[0]
SEL = np.nonzero((np.log10(MTA) >= 10.0) & (np.log10(MTA) <= 16.0))[0]
xi_k = np.geomspace(1e-4, 60.0, 30000); pk = H["P_lin"](xi_k) * np.exp(-(xi_k * 0.05) ** 2)
SG = np.geomspace(0.05, 200.0, 2000)
XI = np.array([np.trapz(xi_k ** 2 * pk * np.sinc(xi_k * s / math.pi), xi_k) / (2 * math.pi ** 2) for s in SG])
K0 = 4 * math.pi * SG ** 3 / 3
K1 = np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * SG[1:] ** 2 * XI[1:] + 4 * math.pi * SG[:-1] ** 2 * XI[:-1]) * np.diff(SG))])
K1 += 4 * math.pi * SG[0] ** 3 / 3 * XI[0]
XB = np.linspace(0.0, 1.0, 11); XM = 0.5 * (XB[1:] + XB[:-1])
RES = {"lane": "CFG644", "script": "cfg644_halo", "mutate": MUTATE, "exclusion": os.environ.get("CFG644_EXCL", "sum"), "label": "CONTEXT ONLY (LCDM halo model: Tinker08/10, NFW shell, EH P_lin)",
       "criteria_commit": "6a03c0870", "cases": {}}


def interp_tab(T, m, r):
    t = (np.log(np.maximum(r, RR[0])) - LR[0]) / DLR
    i0 = np.clip(np.floor(t).astype(int), 0, len(LR) - 2); f = np.clip(t - i0, 0, 1)
    return (1 - f) * T[m, i0] + f * T[m, i0 + 1]


EXCL = os.environ.get("CFG644_EXCL", "sum")                                  # "sum": s >= r_ta + r_ta' (frozen); "max": reported variant
if EXCL != "sum":
    SUF = SUF + "_EXCLmax"
    Pr("*** REPORTED VARIANT: separations s >= max(r_ta, r_ta') (catchments may overlap; the smaller centre outside the larger r_ta) ***")
for ft in ("canonical", "alt"):
    Pr(f"\n[{ft}]")
    U_B, infB = U_set(lambda hb: frame_profile(hb, ft, edge="cen"))
    oB = summarize(f"{ft}|census|cen|recomputed", U_B, infB)
    dB = max(abs(oB["E"] - J556["cases"][f"{ft}|census|cen"]["E"]), abs(oB["s8_ratio"] - J556["cases"][f"{ft}|census|cen"]["s8_ratio"]))
    check(f"K1 [{ft}] CFG556 primary (census, cen) reproduced from the exec'd code (E, sigma8 ratio)", dB < 1e-10, f"|d| {dB:.1e}")
    nM = len(MM)
    TAB = np.zeros((nM, len(LR))); RE = np.full(nM, np.nan)
    for i in SEL:
        r, MF, inf = frame_profile(HB[i], ft, edge="cen")
        TAB[i] = np.interp(LR, np.log(np.maximum(r, 1e-30)), MF, right=MTA[i])
        RE[i] = inf["re"]
    RTA = np.array([hb["rta"] for hb in HB])
    PROB = np.zeros((nM, len(XB)))                                             # P(r_nb < x r_e)
    if not MUTATE:
        S_REL = np.geomspace(1.0, 60.0, 56)
        for i in SEL:
            js = SEL[SEL >= i]
            smin = RTA[i] + RTA[js] if EXCL == "sum" else np.maximum(RTA[i], RTA[js])
            s = smin[:, None] * S_REL[None, :]                                 # (nj, ns)
            jj = np.repeat(js, len(S_REL)); ii = np.full(jj.shape, i); sv = s.ravel()
            lo = np.zeros(sv.shape); hi = np.ones(sv.shape)
            for _ in range(50):
                t = 0.5 * (lo + hi); rr_ = t * sv; dd = (1 - t) * sv
                go = interp_tab(TAB, ii, rr_) / rr_ ** 2; gj = interp_tab(TAB, jj, dd) / dd ** 2
                pos = go > gj; lo = np.where(pos, t, lo); hi = np.where(pos, hi, t)
            req = (0.5 * (lo + hi) * sv).reshape(s.shape)                     # increasing in s
            Ncum = np.zeros(len(XB))
            for b_, x in enumerate(XB[1:], start=1):
                target = x * RE[i]
                sx = np.array([np.interp(target, req[k], s[k], left=np.nan, right=s[k, -1]) for k in range(len(js))])
                ok = np.isfinite(sx) & (sx > smin)
                if ok.any():
                    I_hi = np.interp(sx[ok], SG, K0) + BIAS[i] * BIAS[js[ok]] * np.interp(sx[ok], SG, K1)
                    I_lo = np.interp(smin[ok], SG, K0) + BIAS[i] * BIAS[js[ok]] * np.interp(smin[ok], SG, K1)
                    Ncum[b_] = float(np.sum(W_M[js[ok]] * np.maximum(I_hi - I_lo, 0.0)))
            PROB[i] = 1 - np.exp(-Ncum)
    U_H = U_B.copy()
    for i in SEL:
        if PROB[i, -1] <= 0:
            continue
        dP = np.diff(PROB[i])
        acc = (1 - PROB[i, -1]) * U_B[i]
        for b_ in range(len(XM)):
            if dP[b_] > 0:
                r, MF, _ = frame_profile_nb(HB[i], ft, XM[b_] * RE[i])
                acc = acc + dP[b_] * U_of(r, MF, KK)
        U_H[i] = acc
    oH = summarize(f"{ft}|HNB", U_H, None)
    frac = (oB["E"] - oH["E"]) / oB["E"] if oB["E"] != 0 else float("nan")
    cls = "MATERIAL" if frac >= 0.5 else "PARTIAL" if frac >= 0.1 else "NEGLIGIBLE"
    bite = {f"{l}-{l + 1}": float(np.average(PROB[(np.log10(MTA) >= l) & (np.log10(MTA) < l + 1), -1],
                                             weights=W_M[(np.log10(MTA) >= l) & (np.log10(MTA) < l + 1)])) for l in range(10, 16)}
    RES["cases"][ft] = dict(E_B=oB["E"], E_HNB=oH["E"], kE_HNB=oH["kE"], s8_ratio_B=oB["s8_ratio"], s8_ratio_HNB=oH["s8_ratio"],
                            R_at_B=oB["R_at"], R_at_HNB=oH["R_at"], frac_excess_removed=frac, class_=cls, P_bite_by_logMta=bite,
                            drivers_HNB=oH["drivers"])
    Pr(f"  [{ft}] E census {oB['E']:+.4f} -> H-NB {oH['E']:+.4f} (k {oH['kE']:.2f}); R(0.35) {oB['R_at']['0.35']:.4f} -> {oH['R_at']['0.35']:.4f}; "
       f"R(1) {oB['R_at']['1.0']:.4f} -> {oH['R_at']['1.0']:.4f}; sigma8 ratio {oB['s8_ratio']:.4f} -> {oH['s8_ratio']:.4f}; "
       f"excess removed {100 * frac:.2f}% -> {cls}")
    Pr("      P(r_nb < r_e) by log M_ta: " + "  ".join(f"{k}: {v:.3f}" for k, v in bite.items()))
    if MUTATE:
        dm = float(np.max(np.abs(np.array(oH["R"]) - np.array(oB["R"]))))
        check(f"M1 [{ft}] r_nb = inf for every halo -> CFG556 primary R(k) exactly", dm <= 1e-12, f"max |dR| {dm:.1e}")
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nf = sum(1 for c in CHK.values() if not c["ok"])
Pr(f"\n{sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg644_halo_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg644_halo{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nf else 0)
