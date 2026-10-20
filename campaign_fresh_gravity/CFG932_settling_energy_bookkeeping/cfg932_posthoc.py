#!/usr/bin/env python3
"""CFG932 POST-HOC diagnostics (amendment A1, 2026-10-20, written AFTER cfg932.py's main results were seen; no verdict weight;
the frozen Q1/Q3 classes are unchanged).  Reads cfg932_results.json and imports cfg932.py's functions read-only.

PH0  what sets each non-empty frozen window: eps_hi and the system that sets it; the largest eps_hi over all non-empty corners.
PH1  OVER-SUPPLIED system-corners (r_* > r_ta: the law cannot hold M_cat inside the catchment; 16 flagged by the main run, all
     Draco/Fornax at L = 100).  The frozen rule (R_x = last +/- crossing below r_*) is not defined for them.  Completion used here:
     settled = law inside r_ta plus the overfill M_cat - M_ph(<r_ta) as a shell at r_ta (the least-cost mass-conserving completion:
     the surplus must at least reach the catchment edge); region R = r_ta.  (b): same formula; (a): shell self/interaction term added;
     (c): monotone map with r_s = r_ta beyond M_ph(<r_ta).  Windows recomputed.
PH2  flagged system-corners treated as never payable (eps_req = inf; most favourable to a window).
PH3  flagged corners dropped.
PH4  one-sided (E5) drift test on a mixed initial state (a0 = 1 instead of the frozen 0.05, so deficit cells exist): the drift only
     moves cold energy inward and only releases energy; the frozen one-sided run had no deficit cell and did not move.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg932_posthoc.py  -> cfg932_posthoc.out, cfg932_posthoc.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import importlib.util
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cfg932", os.path.join(HERE, "cfg932.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
OUT = []
def log(s=""):
    print(s, flush=True); OUT.append(s)

R = json.load(open(os.path.join(HERE, "cfg932_results.json")))
S = C.systems(); by = {s["name"]: s for s in S}; roles = {s["name"]: s["role"] for s in S}
SA = ["UFD-c", "UFD-e", "Draco-like", "cluster-core"]; SB = SA + ["Fornax-like"]
CUSP = {k: (rule, F) for k, rule, F in C.CUSPS}
J = {"lane": "CFG932", "part": "posthoc A1", "criteria": "dce2a2e3d"}

# ---------------- PH0
log("PH0 frozen windows (measure b, S_A): non-empty corners, eps_hi and the system that sets it")
ne = []
for c in R["corners"]:
    w = c["windows"]["b"]["S_A"]
    if w["nonempty"]:
        e = c["eps_req"]["b"]; setter = min(SA, key=lambda n: e[n])
        ne.append(dict(footing=c["footing"], cusp=c["cusp"], L=c["L"], MBH=c["MBH"], eps_lo=w["eps_lo"], eps_hi=w["eps_hi"], set_by=setter))
mx = max(x["eps_hi"] for x in ne)
from collections import Counter
log(f"  {len(ne)}/72 non-empty; largest eps_hi = {mx:.3e}; eps_hi set by: {dict(Counter(x['set_by'] for x in ne))}")
J["PH0"] = dict(n_nonempty=len(ne), max_eps_hi=mx, setters=dict(Counter(x["set_by"] for x in ne)), corners=ne)

# ---------------- PH1 edge-shell completion for over-supplied system-corners
def edge_shell(sysd, a0_si, rule, F, L):
    a0 = C.a0k(a0_si); Mb, dMb = sysd["Mb"], sysd["dMb"]
    Mta, fr = C.supply(sysd["Mb_tot"], L); Mcat = (1 - C.FB) * Mta
    rta = (3 * Mta / (4 * math.pi * C.DTA0 * C.RHOM)) ** (1 / 3)
    c, _ = C.conc(Mta, rule, F); rs = rta / c; mc = float(C.mfun(c))
    Mp = lambda r: (1 - C.FB) * Mta * C.mfun(np.minimum(r, rta) / rs) / mc
    dMp = lambda r: np.where(r < rta, (1 - C.FB) * Mta * (r / rs) / (1 + r / rs) ** 2 / (rs * mc), 0.0)
    Mph, dMph = C.phantom(sysd, a0)
    Mphr = float(Mph(np.array(rta))); Mover = Mcat - Mphr
    assert Mover > 0
    b = C.dE_b(Mb, dMb, Mph, dMph, Mp, rta)
    dWs = C.dW_diff(Mb, dMb, Mph, dMph, Mp, dMp, rta)                      # smooth parts (law inside r_ta vs primordial)
    shell = -C.GK * Mover * (float(Mb(np.array(rta))) + Mphr + 0.5 * Mover) / rta
    a = 0.5 * (dWs + shell)
    cg, cn = C.dE_c(Mb, Mph, Mp, rta)
    return dict(M_over=Mover, M_over_frac=Mover / Mcat, dE_b_erg=b * C.ERG, dE_a_erg=a * C.ERG, dE_c_erg=cg * C.ERG,
                dE_c_net_erg=cn * C.ERG, R_kpc=rta)

flag = {k: v for k, v in R["flags"].items() if v}
ph1 = {}
log("\nPH1 over-supplied system-corners (r_* > r_ta), edge-shell completion, region r_ta:")
for key, names in flag.items():
    fk, ck, Lk = key.split("|"); rule, F = CUSP[ck]
    for nm in names:
        r = edge_shell(by[nm], C.FOOT[fk], rule, F, int(Lk[1:]))
        Esn = R["grid"][key][nm]["E_SN_erg"]
        r.update(E_SN_erg=Esn, eps_req_b=max(r["dE_b_erg"], 0) / Esn, eps_req_a=max(r["dE_a_erg"], 0) / Esn, eps_req_c=max(r["dE_c_erg"], 0) / Esn)
        ph1[f"{key}|{nm}"] = r
        log(f"  {key:18s} {nm:12s} overfill {r['M_over']:.3e} ({r['M_over_frac']:.3f} of M_cat)  dE_b {r['dE_b_erg']:.3e}  dE_a {r['dE_a_erg']:.3e}  "
            f"dE_c {r['dE_c_erg']:.3e} erg; E_SN {Esn:.3e}; eps_req b/a/c {r['eps_req_b']:.3e} / {r['eps_req_a']:.3e} / {r['eps_req_c']:.3e}")
J["PH1_rows"] = ph1

def windows_with(mode):
    """recompute every corner's windows with flagged system-corners replaced (mode: PH1 / PH2 / PH3)."""
    res = {}
    for meas in ("b", "a", "c"):
        for sset_name, sset in (("S_A", SA), ("S_B", SB)):
            nn = 0; tot = 0; his = []; details = []
            for c in R["corners"]:
                key = f"{c['footing']}|{c['cusp']}|L{c['L']}"
                fl = flag.get(key, [])
                if mode == "PH3" and fl: continue
                er = dict(c["eps_req"][meas])
                for nm in fl:
                    er[nm] = ph1[f"{key}|{nm}"][f"eps_req_{meas}"] if mode == "PH1" else float("inf")
                    if mode == "PH1" and er[nm] == 0.0: er[nm] = 0.0
                w = C.window(er, roles, sset); tot += 1
                if w["nonempty"]:
                    nn += 1; his.append(w["eps_hi"])
                    details.append(dict(footing=c["footing"], cusp=c["cusp"], L=c["L"], MBH=c["MBH"], eps_lo=w["eps_lo"], eps_hi=w["eps_hi"]))
            cls = "WINDOW EXISTS" if nn == tot else ("NO WINDOW" if nn == 0 else "BRACKET-DEPENDENT")
            res[f"{meas}_{sset_name}"] = dict(cls=cls, n_nonempty=nn, n=tot, max_eps_hi=(max(his) if his else None), nonempty=details)
    return res

for mode, label in (("PH1", "edge-shell completion"), ("PH2", "flagged = never payable (inf)"), ("PH3", "flagged corners dropped")):
    W = windows_with(mode); J[mode] = W
    log(f"\n{mode} ({label}):")
    for k, v in W.items():
        log(f"  {k}: {v['cls']} ({v['n_nonempty']}/{v['n']}); largest eps_hi {v['max_eps_hi'] if v['max_eps_hi'] is None else format(v['max_eps_hi'], '.3e')}")
    big = [d for d in W["b_S_A"]["nonempty"] if d["eps_hi"] > 1e-4]
    log(f"  b/S_A windows reaching above eps = 1e-4: {len(big)}" + ("" if not big else ": " + "; ".join(
        f"{d['footing']} {d['cusp']} L{d['L']} MBH {d['MBH']:.0e} [{d['eps_lo']:.2e}, {min(d['eps_hi'], 1):.2e})" for d in big)))

# ---------------- PH4 one-sided drift test on a mixed state (a0 = 1)
def drift_mixed(a0, two_sided, t_end=200.0, maxsteps=3_000_000):
    G = 1.0; N = 400; alpha = 1.0
    rf = np.geomspace(1e-3, 30.0, N + 1); V = 4 * math.pi / 3 * np.diff(rf ** 3); A = 4 * math.pi * rf ** 2; rc = np.sqrt(rf[1:] * rf[:-1])
    Mbf = rf ** 3 / (rf ** 2 + 1.0) ** 1.5; Mb_in = Mbf[0]; mb = np.diff(Mbf); rhob = mb / V
    Mphf = Mbf / np.expm1(np.sqrt(Mbf / (rf ** 2 * a0))); rhoph = np.diff(Mphf) / V
    Mcf = 30.0 * C.mfun(rf / 3.0) / float(C.mfun(10.0)); mc = np.diff(Mcf).copy(); mc[0] += Mcf[0]
    def W_Phi(mc):
        mt = mb + mc; Sinc = Mb_in + np.cumsum(mt)
        W = -G * float(np.sum((Sinc - 0.5 * mt) * mt / rc)); tail = np.cumsum((mt / rc)[::-1])[::-1] - mt / rc
        return W, -G * (Sinc / rc + tail)
    sur0 = mc / V > rhoph                                       # cells in local surplus at t = 0
    Msur0 = float(mc[sur0].sum()); ndef0 = int((~sur0).sum())
    W0, Phi = W_Phi(mc); t = 0.0; n = 0; Pacc = Pout = Pin = 0.0
    while t < t_end and n < maxsteps:
        rho = mc / V; rhom = rho + rhob; cin = np.cumsum(mc)[:-1]
        if two_sided: dpsi = G * (Mphf[1:N] - cin) / rf[1:N] ** 2
        else: dpsi = G * np.cumsum(np.maximum(rhoph - rho, 0.0) * V)[:-1] / rf[1:N] ** 2
        out_dir = dpsi < 0; donor = np.where(out_dir, np.arange(0, N - 1), np.arange(1, N))
        tau = 1.0 / np.sqrt(4 * math.pi * G * np.maximum(rhom[donor], 1e-300)); v = -alpha * tau * dpsi
        flux = v * rho[donor] * A[1:N]; act = np.abs(flux) > 0
        if not act.any(): break
        dt = min(0.2 * float((V[donor][act] / (np.abs(v[act]) * A[1:N][act])).min()), t_end - t)
        dm = flux * dt; P = dm * (Phi[1:] - Phi[:-1])
        Pacc += float(P.sum()); Pout += float(P[dm > 0].sum()); Pin += float(P[dm < 0].sum())
        mc[:-1] -= dm; mc[1:] += dm; mc = np.maximum(mc, 0.0); _, Phi = W_Phi(mc); t += dt; n += 1
    W1, _ = W_Phi(mc)
    return dict(a0=a0, two_sided=two_sided, t=t, steps=n, deficit_cells_t0=ndef0, dW=W1 - W0, dW_over_absW0=(W1 - W0) / abs(W0),
                int_P=Pacc, identity_rel=abs(W1 - W0 - Pacc) / max(abs(W1 - W0), 1e-300), int_P_out=Pout, int_P_in=Pin,
                surplus_cells_mass_t0=Msur0, surplus_cells_mass_end=float(mc[sur0].sum()))
log("\nPH4 drift test on a mixed initial state (a0 = 1; same baryons and NFW as the frozen test):")
ph4 = {}
for ts in (False, True):
    d = drift_mixed(1.0, ts); ph4["two_sided" if ts else "one_sided"] = d
    log(f"  {'two-sided' if ts else 'one-sided'}: deficit cells at t0 {d['deficit_cells_t0']}, t {d['t']:.1f}, steps {d['steps']}, dW/|W0| {d['dW_over_absW0']:+.4e}, "
        f"int P {d['int_P']:+.4e} (identity rel {d['identity_rel']:.2e}); outward {d['int_P_out']:+.3e}, inward {d['int_P_in']:+.3e}; "
        f"mass in t0-surplus cells {d['surplus_cells_mass_t0']:.4f} -> {d['surplus_cells_mass_end']:.4f}")
J["PH4"] = ph4
log("\nPOST-HOC, no verdict weight; frozen classes unchanged. kappa = 1/2 FITTED; footings never pooled; not theory closed.")
json.dump(C.jsonable(J), open(os.path.join(HERE, "cfg932_posthoc.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg932_posthoc.out"), "w").write("\n".join(OUT) + "\n")
