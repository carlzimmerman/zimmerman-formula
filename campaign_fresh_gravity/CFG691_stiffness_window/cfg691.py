"""CFG691: can astra's stiffness hide the sector from the Sun and keep it in galaxies?

Criteria: FROZEN_CRITERIA.md (committed alone, 9560a93c5). Universal point-mass profile q(s) (solve_bvp), the record's CFG3
Solar-System gates -> L*_min; raw SPARC on the CFG4 statistic (as copied in CFG690) with the screened form -> L*_max.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg691.py      (CFG691_MUTATE=1: M1 no stiffness, M2 scalar Laplacian; exit 1 iff both bite)
"""
import os, sys, json, math

import numpy as np
from scipy.integrate import solve_bvp

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402  (read only)

MUT = os.environ.get("CFG691_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg691{TAG}.out"), "w")
RES = {"lane": "CFG691", "criteria": "9560a93c5", "mutate": MUT, "checks": {}, "numbers": {}}
G, MSUN, AU, PC, KPC_S = 6.6743e-11, 1.98847e30, 1.495978707e11, 3.0856775814913673e16, 3.0857e19
GM_SUN = 1.32712440018e20
SUN_BOUND, M_SAT_BOUND, R_SAT = 3.66e-14, 6.7e-11, 9.54 * AU         # the record's CFG3 gates


def P(s=""):
    print(s)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P(__doc__.strip())


# ============================================================================ the universal profile q(s)
def solve_profile(vector=True, smin=1e-4, smax=1e4):
    """-[q'' + 2q'/s - 2q/s^2] + q|q| = 1/s^2 in t = ln s: y1 = q, y2 = dq/dt."""
    k = 2.0 if vector else 0.0

    def f(t, y):
        s = np.exp(t)
        return np.vstack([y[1], -y[1] + k * y[0] + s ** 2 * y[0] * np.abs(y[0]) - 1.0])

    def bc(ya, yb):
        return np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1 / smax - 1 / smax ** 2)])   # inner regular q = 1/2 + A s; outer asymptote

    t = np.linspace(math.log(smin), math.log(smax), 4001)
    s = np.exp(t)
    y0 = np.vstack([1 / (s + 2), -s / (s + 2) ** 2])
    sol = solve_bvp(f, bc, t, y0, tol=1e-8, max_nodes=200000)
    return sol, f


sol, ffun = solve_profile(vector=not MUT)
tt = np.linspace(sol.x[0], sol.x[-1], 20001)
yy = sol.sol(tt)
dy = sol.sol(tt, 1)
res_rel = np.max(np.abs(dy[1] - ffun(tt, yy)[1]) / (1 + np.abs(ffun(tt, yy)[1])))
sg = np.exp(tt)
q_in = float(sol.sol(math.log(1e-3))[0])
S_out = float(1e3 * sol.sol(math.log(1e3))[0])
P(f"\nPROFILE: solve_bvp status {sol.status} ({sol.message}); nodes {sol.x.size}; max rel ODE residual {res_rel:.2e}")
P(f"    q(1e-3) = {q_in:.6f} (inner limit 1/2);  S(1e3) = s q = {S_out:.6f}")
for sv in (1e-2, 0.1, 0.3, 1, 3, 10, 100):
    P(f"    s = {sv:7.2f}: q = {float(sol.sol(math.log(sv))[0]):.5f}, S = s q = {sv * float(sol.sol(math.log(sv))[0]):.5f}")


def S_of(s):
    s = np.asarray(s, float)
    out = np.empty_like(s)
    lo, hi = s < 1e-4, s > 1e4
    mid = ~(lo | hi)
    out[lo] = s[lo] * 0.5
    out[hi] = 1 - 1 / s[hi]
    out[mid] = s[mid] * sol.sol(np.log(s[mid]))[0]
    return out


def g_an(r, M, Lstar, a0):
    """anomalous acceleration of an isolated point mass M (kg) at r (m); Lstar (m); Lstar = 0 means no stiffness."""
    if Lstar == 0 or MUT:
        return math.sqrt(G * M * a0) / r
    rM = math.sqrt(G * M / a0)
    ell = Lstar ** 2 / (2 * rM)
    return math.sqrt(G * M * a0) / r * float(S_of(np.array([r / ell]))[0])


# K1: physical inner limit equals GM/L*^2
a0c = C4.A0["canonical"]
Lt = 1.0 * PC
inner = g_an(1e-4 * Lt ** 2 / (2 * math.sqrt(GM_SUN / a0c)), MSUN, Lt, a0c)
k1_phys = abs(inner / (GM_SUN / Lt ** 2) - 1)
k1 = check("K1 profile: ODE residual <= 1e-6, S(1e3) >= 0.999, q(1e-3) -> 1/2 within 1e-3, inner g_an = GM/L*^2 within 1e-3",
           sol.status == 0 and res_rel <= 1e-6 and S_out >= 0.999 and abs(q_in - 0.5) <= 1e-3 and k1_phys <= 1e-3,
           f"status {sol.status}, residual {res_rel:.1e}, S(1e3) {S_out:.5f}, q(1e-3) {q_in:.5f}, inner/(GM/L*^2) - 1 = {k1_phys:.1e}")
RES["numbers"]["profile"] = dict(status=sol.status, residual=res_rel, q_1em3=q_in, S_1e3=S_out,
                                 S_table={str(sv): sv * float(sol.sol(math.log(sv))[0]) for sv in (1e-2, 0.1, 0.3, 1, 3, 10, 100)})

# ============================================================================ G-SS: L*_min
P("\nG-SS  the record's CFG3 gates for the isolated Sun: sunward anomaly at 1 AU < 3.66e-14 m/s^2; anomalous mass inside 9.54 AU < 6.7e-11 Msun")
LGRID = 10 ** np.round(np.arange(-4, 4.0001, 0.01), 2) * PC
GSS = {}
for f in C4.FOOTS:
    a0 = C4.A0[f]
    a1 = np.array([g_an(AU, MSUN, L, a0) for L in LGRID]) / SUN_BOUND
    ms = np.array([g_an(R_SAT, MSUN, L, a0) * R_SAT ** 2 / G / MSUN for L in LGRID]) / M_SAT_BOUND
    ok = (a1 < 1) & (ms < 1)
    mono = bool(np.all(np.diff(ok.astype(int)) >= 0))
    i = int(np.argmax(ok)) if ok.any() else None
    nos = (math.sqrt(GM_SUN * a0) / AU / SUN_BOUND, math.sqrt(GM_SUN * a0) / R_SAT * R_SAT ** 2 / G / MSUN / M_SAT_BOUND)
    GSS[f] = dict(Lmin_pc=(LGRID[i] / PC if i is not None else None), monotone=mono, unscreened_ratio_1AU=nos[0], unscreened_ratio_Sat=nos[1],
                  ratio_1AU_at_Lmin=(float(a1[i]) if i is not None else None), ratio_Sat_at_Lmin=(float(ms[i]) if i is not None else None))
    P(f"    {f:9s}: unscreened ratios 1 AU {nos[0]:.2e}, Saturn {nos[1]:.2e};  L*_min = "
      + (f"{LGRID[i] / PC:.4g} pc (ratios {a1[i]:.3f}, {ms[i]:.3f}); pass set monotone in L*: {mono}" if i is not None else "NONE on 1e-4..1e4 pc"))
RES["numbers"]["G_SS"] = GSS
gss_pass = all(GSS[f]["Lmin_pc"] is not None for f in C4.FOOTS)

# ============================================================================ G-GAL: L*_max on raw SPARC
P("\nG-GAL  raw SPARC, CFG4 statistic (CFG690 copy), screened nu = 1 + y^-1/2 S(R / l(M_b)); M_b = V_bar^2 R / G at the last point")
GAL = C4.load_sparc()
NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
Rm = np.concatenate([g["R"] for g in GAL]) * KPC_S
Vo = np.concatenate([g["Vobs"] for g in GAL]); eV = np.concatenate([g["eV"] for g in GAL])
Vg = np.concatenate([g["Vgas"] for g in GAL]); Vd = np.concatenate([g["Vdisk"] for g in GAL]); Vb = np.concatenate([g["Vbul"] for g in GAL])
GI = np.concatenate([np.full(len(g["R"]), i) for i, g in enumerate(GAL)])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WPT = 1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2
WW = np.where(OK, WPT[:, None], 0.0)
last = np.array([np.where(GI == i)[0][-1] for i in range(NG)])
MB = np.clip(VB2[last] * 1e6 * Rm[last, None] / G, 1e30, None)          # [NG, U] kg; clipped (a non-positive V_bar^2 at the edge)
RM_G = np.sqrt(G * MB / 1.0)                                             # sqrt(G M_b); r_M = RM_G / sqrt(a0)


def fit(a0, Lstar):
    with np.errstate(all="ignore"):
        gb = np.where(OK, GB, 1.0)
        boost = np.sqrt(a0 / gb)
        if Lstar > 0 and not MUT:
            ell = Lstar ** 2 / (2 * RM_G[GI] / math.sqrt(a0))
            boost = boost * S_of((Rm[:, None] / ell).ravel()).reshape(ell.shape)
        r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, (1 + boost) * gb, 1.0))
    mse = (WW * r_ ** 2).sum(0) / WW.sum(0)
    i = int(np.argmin(mse))
    return math.sqrt(mse[i]), float(UPS[i])


c690 = json.load(open(os.path.join(LANES, "CFG690_cubic_origin", "cfg690_results.json")))["numbers"]["T3"]
k2 = True
for f in C4.FOOTS:
    r0, u0 = fit(C4.A0[f], 0.0)
    k2 &= abs(r0 - c690[f]["rms_SI"]) <= 1e-6 and u0 == c690[f]["U_SI"]
    P(f"    {f:9s} L* = 0: rms {r0:.6f} @ U {u0:.2f} (CFG690 {c690[f]['rms_SI']:.6f} @ {c690[f]['U_SI']:.2f})")
check("K2 L* -> 0 reproduces CFG690 T3 (rms 1e-6, Upsilon exact), both footings", k2, "")

LG2 = 10 ** np.round(np.arange(-2, 3.0001, 0.01), 2) * PC
GGAL = {}
for f in C4.FOOTS:
    rows = [fit(C4.A0[f], L) for L in LG2]
    rms = np.array([x[0] for x in rows]); ups = np.array([x[1] for x in rows])
    okg = rms <= 0.110
    j = int(np.where(okg)[0][-1]) if okg.any() else None
    contiguous = bool(j is not None and okg[: j + 1].all())
    Lmin = GSS[f]["Lmin_pc"]
    at_min = fit(C4.A0[f], Lmin * PC) if Lmin is not None else (None, None)
    GGAL[f] = dict(Lmax_pc=(LG2[j] / PC if j is not None else None), pass_set_contiguous_from_low=contiguous,
                   rms_at_Lmin=at_min[0], U_at_Lmin=at_min[1],
                   ladder={f"{LG2[k] / PC:.3g}": dict(rms=float(rms[k]), U=float(ups[k])) for k in range(0, len(LG2), 50)})
    P(f"    {f:9s}: L*_max = " + (f"{LG2[j] / PC:.4g} pc (rms {rms[j]:.4f} @ U {ups[j]:.2f}); pass set contiguous from 0.01 pc: {contiguous}"
                                    if j is not None else "NONE") +
      (f";  at L*_min {Lmin:.4g} pc: rms {at_min[0]:.4f} @ U {at_min[1]:.2f}" if Lmin is not None else ""))
    for k in range(0, len(LG2), 50):
        P(f"        L* {LG2[k] / PC:8.3g} pc: rms {rms[k]:.4f} @ U {ups[k]:.2f}")
RES["numbers"]["G_GAL"] = GGAL

# ============================================================================ verdict
win = {f: (GSS[f]["Lmin_pc"] is not None and GGAL[f]["Lmax_pc"] is not None and GSS[f]["Lmin_pc"] < GGAL[f]["Lmax_pc"]) for f in C4.FOOTS}
verdict = "WINDOW OPEN" if all(win.values()) else "WINDOW CLOSED"
P(f"\nVERDICT: {verdict}  " + "; ".join(f"{f}: [{GSS[f]['Lmin_pc']}, {GGAL[f]['Lmax_pc']}] pc" for f in C4.FOOTS)
  + "  (Upsilon band failure inherited from CFG690; never a C2 pass)")
RES["verdict"] = dict(window=verdict, per_footing=win)

# ============================================================================ reported only
P("\nREPORTED (no verdict weight), at L* = L*_min per footing")
rep = {}
for f in C4.FOOTS:
    a0 = C4.A0[f]; Lm = GSS[f]["Lmin_pc"]
    if Lm is None:
        continue
    L = Lm * PC
    rep[f] = {"sun_constant_pull": GM_SUN / L ** 2}
    P(f"    {f}: Sun's constant inner pull GM/L*^2 = {GM_SUN / L ** 2:.3e} m/s^2; l_gamma(Sun) = {L ** 2 / (2 * math.sqrt(GM_SUN / a0)) / PC:.3g} pc")
    for d in (1e3, 3e3, 1e4):
        M = 2 * MSUN; r = d * AU
        ratio = g_an(r, M, L, a0) / (G * M / r ** 2); unscr = math.sqrt(G * M * a0) / r / (G * M / r ** 2)
        rep[f][f"WB_{int(d)}AU"] = dict(screened=ratio, unscreened=unscr)
        P(f"      wide binary 2 Msun at {d:6.0f} AU: anomaly/Newton {ratio:.3e} (unscreened {unscr:.3e})")
    P("      UFD rows from CFG259: NOT REPORTED (its committed tables carry no stellar masses or half-light radii). Generic ladder, disclosed:")
    for lm in (3, 4, 5, 7, 9):
        M = 10 ** lm * MSUN
        ell = L ** 2 / (2 * math.sqrt(G * M / a0))
        rep[f][f"ell_M1e{lm}"] = ell / PC
        P(f"      M_b = 1e{lm} Msun: l_gamma = {ell / PC:.3g} pc")
RES["numbers"]["reported"] = rep

# ============================================================================ MUTATE / exit
if MUT:
    m1 = not gss_pass
    m2 = not k1
    RES["mutate_bites"] = dict(M1=m1, M2=m2)
    P(f"\nMUTATE: M1 (no stiffness) G-SS fails: {m1}; M2 (scalar Laplacian) K1 fails: {m2}")
    rc = 1 if (m1 and m2) else 0
else:
    rc = 0 if (k1 and k2) else 1


def js(o):
    if isinstance(o, dict):
        return {str(k): js(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [js(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    return o


json.dump(js(RES), open(os.path.join(HERE, f"cfg691_results{TAG}.json"), "w"), indent=1)
OUT.close()
sys.exit(rc)
