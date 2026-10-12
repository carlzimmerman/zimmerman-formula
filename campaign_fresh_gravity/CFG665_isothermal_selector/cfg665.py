#!/usr/bin/env python3
"""CFG665 (FROZEN_CRITERIA.md, 79599c03e): is thermal equilibrium the selector?

S*: settled cold energy isothermal in the total potential; supply M_c(<r_e) = 5.364 M_b; edge acceleration g_e = f_b a0; edge
pressure rho_c(r_e) sigma^2 = g_e^2/(8 pi G); sigma from central regularity (inward shooting).  The law's kernel is not used in
the prediction.  Raw SPARC rotmod via the record's CFG4 harness (Upsilon = 0.61).
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not "theory closed".
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg665.py     (CFG665_MUTATE=1 -> _MUTATE outputs, exit 1 iff both teeth bite)"""
import os, sys, io, json, math, contextlib, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4
    import CFG7_common as C7
MUT = os.environ.get("CFG665_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
FOOTS = ("canonical", "alt")
G = 6.67430e-11; KMS = 1e3; KPC = 3.0857e19; MSUN = 1.98847e30
FB = 0.02237 / 0.14237; COLD = (1 - FB) / FB                     # 5.364
OUT, RES = [], {"lane": "CFG665", "criteria": "79599c03e", "mutate": MUT, "f_b": FB, "cold_ratio": COLD}
T0 = time.time()


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def solve(Mb_of, Mb_tot, a0, ge_fac=FB, supply_fac=COLD, r_scale=None):
    """returns dict(sigma, r_e, Mc_of) or None.  Mb_of(r) [kg], r in m."""
    ge = ge_fac * a0; Pe = ge ** 2 / (8 * math.pi * G); Ms = supply_fac * Mb_tot
    f = lambda r: G * (Mb_of(r) + Ms) / r ** 2 - ge
    lo, hi = r_scale * 1e-3, r_scale * 1e4
    if f(lo) * f(hi) > 0:
        return None
    re = brentq(f, lo, hi, rtol=1e-10)
    rmin = r_scale * 1e-3

    def shoot(sig, dense=False):
        lr0 = math.log(Pe / sig ** 2)

        def rhs(r, y):
            Mc, lr = y
            return [4 * math.pi * r * r * math.exp(min(lr, 700.0)), -G * (Mb_of(r) + Mc) / (r * r * sig * sig)]
        ev = lambda r, y: y[0]; ev.terminal = True; ev.direction = -1
        s = solve_ivp(rhs, (re, rmin), [Ms, lr0], events=ev, method="LSODA", rtol=1e-8, atol=[1e-6 * Ms, 1e-8],
                      dense_output=dense)
        if s.t_events[0].size:
            return math.log(s.t_events[0][0] / rmin), s          # mass ran out before the centre: sigma too small
        return -s.y[0, -1] / Ms, s                                # mass left at the centre: sigma too large
    sgrid = np.geomspace(5 * KMS, 2000 * KMS, 40)
    vals = [shoot(sg)[0] for sg in sgrid]
    idx = [i for i in range(len(sgrid) - 1) if vals[i] > 0 >= vals[i + 1]]
    if not idx:
        return None
    i = idx[0]
    sig = brentq(lambda sg: shoot(sg)[0], sgrid[i], sgrid[i + 1], xtol=1e-6 * sgrid[i])
    _, s = shoot(sig, dense=True)

    def Mc_of(r):
        r = np.asarray(r, float)
        out = np.where(r >= re, Ms, 0.0)
        m = (r < re) & (r > s.t[-1])
        out[m] = s.sol(r[m])[0]
        return np.maximum(out, 0.0)
    return dict(sigma=sig, r_e=re, Mc_of=Mc_of)


# ------------------------------------------------------------------------------------------------ K1 deep control
def hern_Mb(M, a):
    return lambda r: M * np.asarray(r, float) ** 2 / (np.asarray(r, float) + a) ** 2


K1 = {}
for foot in FOOTS:
    a0 = C7.A0_SI[foot]; M = 1e10 * MSUN; rM = math.sqrt(G * M / a0)
    sv = solve(hern_Mb(M, 0.01 * rM), M, a0, r_scale=rM)
    dex = math.log10(sv["sigma"] ** 4 / (G * M * a0 / 4)) if sv else float("nan")
    sv2 = solve(hern_Mb(M, 0.01 * rM), M, a0, supply_fac=2 * COLD, r_scale=rM) if MUT else None
    K1[foot] = dict(dex=dex, r_e_over_rM=(sv["r_e"] / rM if sv else None),
                    M2_dex=(math.log10(sv2["sigma"] ** 4 / (G * M * a0 / 4)) if sv2 else None))
    P(f"K1 [{foot}] Hernquist a = 0.01 r_M: sigma^4/(G M a0/4) = {dex:+.4f} dex; r_e/r_M = {K1[foot]['r_e_over_rM']:.3f}"
      + (f"; M2 supply x2: {K1[foot]['M2_dex']:+.4f} dex" if MUT else ""))
K1_ok = all(abs(v["dex"]) <= 0.05 for v in K1.values())
RES["K1"] = dict(rows=K1, pass_=K1_ok)

# ------------------------------------------------------------------------------------------------ D1 SPARC
with contextlib.redirect_stdout(io.StringIO()):
    g4, _ = C4.exec_slices(os.path.join(LANES, "CFG4_galaxy_law.py"), [(None, 'banner("K  CONTROLS')], name="cfg4_galaxy_ro")
iu = int(np.argmin(np.abs(g4["UPS"] - 0.61)))
gb4, go4, ok4, ww4, Rm, GI = g4["GB"][:, iu], g4["GO"][:, iu], g4["OK"][:, iu], g4["WW"][:, iu], g4["Rm"], g4["GI"]
nu = lambda y: np.asarray(C7.nu_mono(np.asarray(y, float)), float)

D1 = {}
for foot in FOOTS:
    a0 = C7.A0_SI[foot]
    ge_fac = 1.0 if MUT else FB
    pred = np.full(gb4.shape, np.nan); law = np.where(ok4, nu(np.where(ok4, gb4, 1.0) / a0) * np.where(ok4, gb4, 1.0), 1.0)
    nsolv = nuns = 0; sig_rows = []
    for gi in np.unique(GI):
        idx = np.where((GI == gi) & ok4 & (gb4 > 0))[0]
        if idx.size < 3:
            continue
        idx = idx[np.argsort(Rm[idx])]
        R = Rm[idx]; Mbp = gb4[idx] * R ** 2 / G; Mtot = Mbp[-1]

        def Mb_of(r, R=R, Mbp=Mbp):
            r = np.asarray(r, float)
            inner = Mbp[0] * (r / R[0]) ** 2
            mid = np.interp(r, R, Mbp)
            return np.where(r < R[0], inner, np.where(r > R[-1], Mbp[-1], mid))
        try:
            sv = solve(Mb_of, Mtot, a0, ge_fac=ge_fac, r_scale=R[0])
        except Exception:
            sv = None
        if sv is None:
            nuns += 1; continue
        nsolv += 1
        pred[idx] = G * (Mb_of(R) + sv["Mc_of"](R)) / R ** 2
        sig_rows.append((float(Mtot / MSUN), float(sv["sigma"] / KMS), float(sv["r_e"] / KPC)))
    m = np.isfinite(pred) & ok4 & (pred > 0)
    w = ww4[m]; lo = np.log10(go4[m])
    rS = float(np.sqrt(np.sum(w * (lo - np.log10(pred[m])) ** 2) / w.sum()))
    rL = float(np.sqrt(np.sum(w * (lo - np.log10(law[m])) ** 2) / w.sum()))
    bS = float(np.sum(w * (lo - np.log10(pred[m]))) / w.sum())
    # diagnostics: g_bar bins; surface-brightness halves (g_bar at the first point)
    bins = {}
    for lab, (a, b) in {"g_bar > 1e-10": (1e-10, 1), "1e-11..1e-10": (1e-11, 1e-10), "< 1e-11": (0, 1e-11)}.items():
        mm = m & (gb4 > a) & (gb4 <= b)
        if mm.sum():
            ww = ww4[mm]; ll = np.log10(go4[mm])
            bins[lab] = dict(n=int(mm.sum()), rms_S=float(np.sqrt(np.sum(ww * (ll - np.log10(pred[mm])) ** 2) / ww.sum())),
                             rms_L=float(np.sqrt(np.sum(ww * (ll - np.log10(law[mm])) ** 2) / ww.sum())),
                             bias_S=float(np.sum(ww * (ll - np.log10(pred[mm]))) / ww.sum()))
    first = {gi: gb4[np.where((GI == gi) & m)[0]].max() for gi in np.unique(GI[m])}
    med = np.median(list(first.values()))
    halves = {}
    for lab, cond in (("low central g_bar half", lambda v: v <= med), ("high central g_bar half", lambda v: v > med)):
        gs = [gi for gi, v in first.items() if cond(v)]
        mm = m & np.isin(GI, gs); ww = ww4[mm]; ll = np.log10(go4[mm])
        halves[lab] = dict(n_gal=len(gs), rms_S=float(np.sqrt(np.sum(ww * (ll - np.log10(pred[mm])) ** 2) / ww.sum())),
                           rms_L=float(np.sqrt(np.sum(ww * (ll - np.log10(law[mm])) ** 2) / ww.sum())))
    sr = np.array(sig_rows)
    btfr = float(np.polyfit(np.log10(sr[:, 0]), np.log10(sr[:, 1]), 1)[0]) if len(sr) > 3 else float("nan")
    uns_frac = nuns / max(nsolv + nuns, 1)
    D1[foot] = dict(rms_S=rS, rms_law=rL, d=rS - rL, bias_S=bS, n_pts=int(m.sum()), n_solved=nsolv, n_unsolvable=nuns,
                    unsolvable_frac=uns_frac, gbar_bins=bins, halves=halves, dlog_sigma_dlog_Mb=btfr)
    P(f"\nD1 [{foot}] solved {nsolv}, unsolvable {nuns} ({uns_frac:.1%}); {int(m.sum())} points")
    P(f"   rms S* {rS:.4f}  law {rL:.4f}  d {rS - rL:+.4f}  mean residual S* {bS:+.4f};  d log sigma / d log M_b = {btfr:.3f} (target 0.25)")
    for k, v in bins.items():
        P(f"   g_bar {k:13s}: n {v['n']:4d}  rms S* {v['rms_S']:.3f}  law {v['rms_L']:.3f}  bias S* {v['bias_S']:+.3f}")
    for k, v in halves.items():
        P(f"   {k:24s}: {v['n_gal']:3d} gal  rms S* {v['rms_S']:.3f}  law {v['rms_L']:.3f}")

if all(D1[f]["d"] <= 0.02 and abs(D1[f]["bias_S"]) <= 0.05 and D1[f]["unsolvable_frac"] <= 0.10 for f in FOOTS):
    lab = "S* VIABLE"
elif all(D1[f]["d"] <= 0.05 for f in FOOTS):
    lab = "S* TENSION"
else:
    lab = "S* FAIL"
RES["D1"] = D1
if MUT:
    J = json.load(open(os.path.join(HERE, "cfg665_results.json")))
    m1 = D1["canonical"]["rms_S"] - J["D1"]["canonical"]["rms_S"] >= 0.05
    m2 = all(abs(v["M2_dex"] - v["dex"]) >= 0.1 for v in K1.values() if v["M2_dex"] is not None)
    RES["MUTATE"] = dict(M1=bool(m1), M2=bool(m2))
    P(f"\nMUTATE: M1 (g_e = a0) rms rise >= 0.05: {m1}; M2 (supply x2) sigma^4 moves >= 0.1 dex: {m2}")
    rc = 1 if (m1 and m2) else 0
else:
    lab = lab if K1_ok else "VOID (K1 fails)"
    RES["label"] = lab
    P(f"\nLANE LABEL: {lab}")
    rc = 0
RES["wall_s"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, f"cfg665_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg665{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(rc)
