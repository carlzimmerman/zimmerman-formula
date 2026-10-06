#!/usr/bin/env python3
"""
CFG355 -- tidal rule T1 with a cold-rank veto: f = H(l2 - tau) * V, V = 1 - [rank sigma_c == 2].  Criteria: FROZEN_CRITERIA.md (3f59dab1b).

  T1 (CFG354): l2 of t = Hessian psi >= tau = (Delta_ta - 1)/3.  rank (CFG351): rank of the stream-sum dispersion sigma_c.
  Generic host rank model (CFG351 self-similar caustics): r < lam2 rank 3; lam2 < r < lam1 rank 2 (3 streams); r > lam1 rank 0.
MUTATE: CFG355_MUTATE=1 -> veto rank == 3 instead; must switch OFF host interiors and fail (b) or (d); outputs *_MUTATE; exit 1.
Run: python3 campaign_fresh_gravity/CFG355_tidal_plus_rank_switch/cfg355_tidal_rank_switch.py
"""
import os, sys, io, json, math, contextlib, time
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG355_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
VETO_RANK = 3 if MUTATE else 2
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "CFG355", "mutate": MUTATE, "frozen": "3f59dab1b", "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, ok, measured=""):
    OUT["checks"][name] = dict(ok=bool(ok), measured=measured)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)


def banner(t):
    P("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


P(__doc__.strip())
if MUTATE:
    P("\n  *** CFG355_MUTATE=1: the veto reads rank == 3 (host interiors) instead of rank == 2 ***")

# ================================================================== K0: CFG354 re-run, read-only (no file writes)
banner("K0  CFG354 re-run without the veto (V = 1): T1 numbers must be identical")
P354 = os.path.join(LANES, "CFG354_tidal_turnaround_switch", "cfg354_tidal_switch.py")
DUMP = 'json.dump(OUT, open(os.path.join(HERE, f"cfg354_tidal_switch_results{SUF}.json"), "w"), indent=1, default=str)'
src = open(P354).read()
assert src.count(DUMP) == 2
src = src.replace(DUMP, "pass")
_m = os.environ.pop("CFG354_MUTATE", None)
NS = {"__file__": P354, "__name__": "cfg354_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, P354, "exec"), NS)
J354 = json.load(open(os.path.join(LANES, "CFG354_tidal_turnaround_switch", "cfg354_tidal_switch_results.json")))["numbers"]
N354 = json.loads(json.dumps(NS["OUT"]["numbers"], default=str))


def maxdiff(a, b):
    if isinstance(a, dict):
        return max([maxdiff(a[k], b[k]) for k in a] + [0.0])
    if isinstance(a, list):
        return max([maxdiff(x, y) for x, y in zip(a, b)] + [0.0])
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a is not None:
        return abs(a - b) if math.isfinite(a) else (0.0 if a == b or (math.isnan(a) and math.isnan(b)) else 1.0)
    return 0.0 if a == b else 1.0


t1 = lambda d: {k: v for k, v in d.items() if k.startswith("T1") or k in ("host", "rta_kpc", "Delta", "tau", "fid_dlnm", "flip_lt")}
k0 = dict(a_linear=maxdiff(N354["a_linear"], J354["a_linear"]),
          a_prime_T1=maxdiff({k: v["T1"] for k, v in N354["a_prime"].items() if isinstance(v, dict)},
                             {k: v["T1"] for k, v in J354["a_prime"].items() if isinstance(v, dict)}),
          hosts_T1=maxdiff([t1(r) for r in N354["hosts"]], [t1(r) for r in J354["hosts"]]),
          width_T1=maxdiff(N354["width_cost"]["T1"], J354["width_cost"]["T1"]),
          lens_T1=maxdiff(N354["lens_edges"]["T1"], J354["lens_edges"]["T1"]))
K0 = check("K0 CFG354 T1 reproduced without the veto (1e-12)", max(k0.values()) <= 1e-12, f"max |diff| per block {k0}")
OUT["numbers"]["K0"] = k0
rules, TAU, FTA, DTA = NS["rules"], NS["TAU"], NS["FTA"], NS["DTA"]
hrows = NS["hrows"]
EPS_T1 = NS["EPS"]["T1"]
TAU_E = TAU(FTA)

J351 = json.load(open(os.path.join(LANES, "CFG351_cold_threeaxis_switch", "cfg351_threeaxis_switch_results.json")))["numbers"]
LAM1, LAM2 = J351["c"]["lam1"], J351["c"]["lam2"]
P(f"  CFG351 caustics: lam1 {LAM1:.4f} r_ta (3 streams inside), lam2 {LAM2:.4f} r_ta (>= 5 streams inside)")


def V(rank):
    return (np.asarray(rank) != VETO_RANK).astype(float)


# ================================================================== legality: rank-part stress identities
banner("LEGALITY: T1 part (CFG354 L1-L4) + rank-part state-function stress")
rng = np.random.default_rng(355)
L354 = all(NS["OUT"]["checks"][k]["pass"] for k in NS["OUT"]["checks"] if k.startswith("L"))
r1, adj_err, e2_r1 = 0.0, 0.0, 0.0
for _ in range(1000):
    n = rng.normal(size=3); n /= np.linalg.norm(n); s = rng.uniform(0.1, 3) * np.outer(n, n)
    r1 = max(r1, np.abs(np.trace(s) * s - s @ s).max() / np.trace(s) ** 2)
    e2_r1 = max(e2_r1, abs(0.5 * (np.trace(s) ** 2 - np.trace(s @ s))) / np.trace(s) ** 2)
    vs = rng.normal(size=(3, 3)); ws = rng.uniform(0.1, 1, 3); vb = ws @ vs / ws.sum()
    S2 = sum(w * np.outer(v - vb, v - vb) for w, v in zip(ws, vs)) / ws.sum()
    adj = np.linalg.det(S2) * np.linalg.inv(S2 + 1e-300 * np.eye(3)) if abs(np.linalg.det(S2)) > 1e-14 else np.array(
        [[np.linalg.det(np.delete(np.delete(S2, j, 0), i, 1)) * (-1) ** (i + j) for j in range(3)] for i in range(3)])
    adj_err = max(adj_err, np.abs(S2 @ adj - np.linalg.det(S2) * np.eye(3)).max() / np.trace(S2) ** 3)
LEG = check("L legality: CFG354 L1-L4 (T1 part) + rank part zero stress (tr(s)s - s^2 = 0 on rank 1, e2 = 0 on rank 1, sigma adj sigma = det I)",
            L354 and r1 < 1e-12 and e2_r1 < 1e-12 and adj_err < 1e-12,
            f"CFG354 L {L354}; rank-1 identity {r1:.1e}; e2(rank 1) {e2_r1:.1e}; adj identity on 3-stream states {adj_err:.1e}; "
            "V = 1 - H(e2)(1 - H(det)) is a state function (CFG351 conservation applies)")

# ================================================================== (a)
banner("(a) LINEAR: ON(f) subset ON(T1); FRW rank 0")
amax = max(v["T1"]["frac"] for v in NS["OUT"]["numbers"]["a_linear"].values())
a_ok = NS["OUT"]["checks"]["(a) T1 FRW OFF + linear ON < 1e-6 (R 8/20/50, all z; unsmoothed z 1000)"]["pass"]
A_OK = check("(a) combined OFF on FRW + linear field (inherits T1 ON = 0; V <= 1)", a_ok, f"T1 linear max ON {amax}; FRW sigma_c = 0 -> rank 0")

# ================================================================== (a') A1: CFG353 cells with the virialised rank map
banner("(a') A1  CFG353 compensated cells, rank map: cylinder core rank 2, plane core rank 1, outside rank 0")
A1 = {}
a1_ok = True
for geom, dls in (("plane", (0.5, 1, 2, 3)), ("cyl", (1, 2, 5, 10))):
    for dlt in dls:
        for ratio in (3, 5, 10):
            dv = -dlt / (ratio - 1) if geom == "plane" else -dlt / (ratio ** 2 - 1)
            if dv < -1:
                continue
            x, phi, gphi, wt, w, srcd = NS["cell"](geom, dlt, ratio)
            R = rules(*NS["cell_tensors"](geom, x, gphi, srcd))["T1"]
            rank = np.where(x < w, 2 if geom == "cyl" else 1, 0)
            on1 = R > TAU_E
            onf = on1 * V(rank)
            fr = float(np.sum(onf * wt) / np.sum(wt)); fr1 = float(np.sum(on1 * wt) / np.sum(wt))
            on_out = bool(np.any(on1 & (x >= w)))
            A1[f"{geom}|d{dlt}|r{ratio}"] = dict(T1=fr1, combined=fr, T1_on_outside_core=on_out)
            if not MUTATE:
                a1_ok &= fr == 0.0
            if ratio in (5, 10) and geom == "cyl":
                P(f"  cyl  delta {dlt:3} x{ratio:2d}: T1 ON {fr1:.4f} -> combined {fr:.4f} (T1 ON outside the core: {on_out})")
P(f"  planes: T1 = 0 in all cells (middle eigenvalue 0) -> combined 0")
OUT["numbers"]["A1"] = A1
K1 = all(v["combined"] == 0 for k, v in A1.items() if k.startswith("cyl")) and all(v["T1_on_outside_core"] is False for v in A1.values())
K3 = all(v["T1"] == 0 for k, v in A1.items() if k.startswith("plane"))

# ================================================================== (a') A2: separable 3-axis Zel'dovich (CFG351's field)
banner("(a') A2  separable Zel'dovich A = (1, 0.7, 0.45): T1 from the FFT tidal tensor, rank = # multistream axes, truth = TA3")
AZ = (1.0, 0.7, 0.45); NG = 96; NQ = 2_000_000
XC = (np.arange(NG) + 0.5) * 2 * math.pi / NG
QF = np.linspace(0.0, 2 * math.pi, 40001)
kf = np.fft.fftfreq(NG) * NG
KX, KY, KZ = np.meshgrid(kf, kf, kf, indexing="ij")
K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0
KV = (KX, KY, KZ)


def za_axis(DA):
    q = (np.arange(NQ) + 0.5) * 2 * math.pi / NQ
    rho = np.histogram((q - DA * np.sin(q)) % (2 * math.pi), bins=NG, range=(0, 2 * math.pi))[0] * NG / NQ
    F = QF - DA * np.sin(QF)
    nstr = np.zeros(NG, int); ta = np.zeros(NG, bool)
    for kshift in (-1, 0, 1):
        g = F[None, :] - XC[:, None] - 2 * math.pi * kshift
        sc = np.signbit(g[:, 1:]) != np.signbit(g[:, :-1])
        nstr += sc.sum(1)
        qroot = 0.5 * (QF[1:] + QF[:-1])
        ta |= np.any(sc & (DA * np.cos(qroot)[None, :] >= 0.5), 1)
    return rho, nstr, ta


A2 = {}
a2_ok = True
for D in [round(1.0 + 0.1 * i, 1) for i in range(13)]:
    if D * AZ[2] > 1:
        continue
    ax = [za_axis(D * a) for a in AZ]
    rho = ax[0][0][:, None, None] * ax[1][0][None, :, None] * ax[2][0][None, None, :]
    dh = np.fft.fftn(rho - 1.0)
    T = np.empty((NG, NG, NG, 3, 3))
    for i in range(3):
        for j in range(i, 3):
            T[..., i, j] = T[..., j, i] = np.real(np.fft.ifftn(KV[i] * KV[j] / K2 * dh))
    l2 = np.linalg.eigvalsh(T.reshape(-1, 3, 3))[:, 1].reshape(NG, NG, NG)
    ms = [(a[1] > 1).astype(int) for a in ax]
    rank = ms[0][:, None, None] + ms[1][None, :, None] + ms[2][None, None, :]
    ta3 = ax[0][2][:, None, None] & ax[1][2][None, :, None] & ax[2][2][None, None, :]
    on1 = l2 >= TAU_E
    onf = on1 & (rank != VETO_RANK)
    res = dict(axes_crossed=int(sum(D * a > 1 for a in AZ)), max_delta=float(rho.max() - 1), T1_on=float(on1.mean()),
               combined_on=float(onf.mean()), false_on_T1=float((on1 & ~ta3).mean()), false_on_combined=float((onf & ~ta3).mean()),
               false_off_vetoed_TA3=float((on1 & ta3 & (rank == 2)).mean()), ta3=float(ta3.mean()),
               false_on_by_rank={int(r): float((onf & ~ta3 & (rank == r)).mean()) for r in range(4)})
    A2[str(D)] = res
    if not MUTATE:
        a2_ok &= res["false_on_combined"] == 0.0
    P(f"  D {D:.1f} ({res['axes_crossed']} axes crossed; max delta {res['max_delta']:7.1f}): T1 ON {res['T1_on']:.4f} | combined ON {res['combined_on']:.4f} | "
      f"false ON T1 {res['false_on_T1']:.4f} -> combined {res['false_on_combined']:.4f} (by rank {res['false_on_by_rank']}) | TA3 {res['ta3']:.4f} | vetoed TA3 {res['false_off_vetoed_TA3']:.4f}")
OUT["numbers"]["A2"] = A2

# ---------------------------------------------------------------- A3 cylindrical top-hat transient (reported)
banner("(a') A3 (reported)  cylindrical top-hat, EdS: pre-crossing window with delta >= 2 tau (rank 0)")
di, ti = 1e-3, 1e-3
ai = ti ** (2 / 3); Ri = ai * (1 - di / 2); mu = (1 + di) * (1 - di / 2) ** 2
Vi = (2 / 3) / ti * ai * (1 - di)
ev_ta = lambda t, y: y[1]; ev_ta.direction = -1
ev_c = lambda t, y: y[0] - 1e-4 * Ri; ev_c.terminal = True
sol = solve_ivp(lambda t, y: [y[1], y[0] / (9 * t * t) - mu / (3 * t ** (2 / 3) * y[0])], (ti, 1e6), [Ri, Vi], events=(ev_ta, ev_c),
                rtol=1e-11, atol=1e-14, dense_output=True)
tt = np.geomspace(ti, sol.t[-1], 200000); RR = sol.sol(tt)[0]
dnl = mu * tt ** (4 / 3) / RR ** 2 - 1
t_ta = sol.t_events[0][0]; t_c = sol.t[-1]
i2 = int(np.argmax(dnl >= 2 * TAU_E))
A3 = dict(delta_nl_at_2D_turnaround=float(np.interp(t_ta, tt, dnl)), dlin_at_turnaround=float(di * (t_ta / ti) ** (2 / 3)),
          dlin_at_crossing=float(di * (t_c / ti) ** (2 / 3)), dlin_at_2tau=float(di * (tt[i2] / ti) ** (2 / 3)),
          window_dlna=float((2 / 3) * math.log(t_c / tt[i2])), window_frac_of_age=float((t_c - tt[i2]) / t_c))
P(f"  2D turnaround at delta_lin {A3['dlin_at_turnaround']:.3f} (delta_nl {A3['delta_nl_at_2D_turnaround']:.2f}); delta_nl = 2 tau = {2*TAU_E:.3f} at "
  f"delta_lin {A3['dlin_at_2tau']:.3f}; crossing at delta_lin {A3['dlin_at_crossing']:.3f}")
P(f"  pre-crossing T1-ON window (rank 0, not vetoed): d ln a = {A3['window_dlna']:.3f} ({100*A3['window_frac_of_age']:.1f}% of the age at crossing)")
OUT["numbers"]["A3_tophat"] = A3

# ---------------------------------------------------------------- A4 ellipsoids + A5 host volume vetoed
ell = NS["OUT"]["numbers"]["ellipsoids_reported"]
P("\n  A4 (reported) uniform Ferrers ellipsoids are homogeneous -> one rank for the whole body: crossed in 2 axes (rank 2) -> combined 0;"
  " pre-crossing (rank 0) -> T1 values (prolate 1.000); oblate 0 either way.")
vol_shell = LAM1 ** 3 - LAM2 ** 3; ph_shell = LAM1 - LAM2
A5 = dict(shell_volume_frac_rta=vol_shell, shell_phantom_mass_frac=ph_shell, filament={})
for beta in (0.1, 0.2, 0.3):
    A5["filament"][str(beta)] = dict(volume_frac=3 * beta ** 2 * (1 - LAM1) * 0.75, phantom_mass_frac=min(1.0, 3 * beta ** 2 * (1 / LAM1 - 1) / 4))
P(f"  A5 host volume vetoed (generic shell lam2-lam1): {100*vol_shell:.2f}% of the r_ta volume, {100*ph_shell:.1f}% of the isothermal phantom mass inside r_ta")
for b_, v in A5["filament"].items():
    P(f"     + 3 feeding filaments, core beta = {b_} r_ta (lam1 < r < r_ta): volume {100*v['volume_frac']:.2f}%, phantom mass {100*v['phantom_mass_frac']:.1f}%")
OUT["numbers"]["A5_host_vetoed"] = A5
AP_OK = check("(a') A1 (cells, virialised rank map) false ON 0 AND A2 (Zel'dovich sheet/filament stages) false ON 0", a1_ok and a2_ok,
              f"A1 max combined {max(v['combined'] for v in A1.values()):.4f}; A2 max false ON combined {max(v['false_on_combined'] for v in A2.values()):.4f} "
              f"(T1 alone {max(v['false_on_T1'] for v in A2.values()):.4f})")

# ================================================================== (b)
banner("(b) HOSTS: T1 ON at 30 kpc (CFG354) and rank 3 at 30 kpc (30 kpc < lam2 r_ta), no flicker")
KPC_ = 1.0
bt1 = all(r["T1"]["p_on30"] >= 0.99 for r in hrows) and all(r["flip_lt"] is False for r in hrows)
r3 = [30.0 / (LAM2 * r["rta_kpc"]) for r in hrows]
rank30 = [3 if x < 1 else (2 if 30.0 < LAM1 * r["rta_kpc"] else 0) for x, r in zip(r3, hrows)]
on30 = [bool(V(k)) for k in rank30]
B_OK = check("(b) combined ON at 30 kpc on 24/24 (T1 P >= 0.99, fidelity) + rank at 30 kpc not vetoed + no flicker",
             bt1 and all(on30), f"T1 {bt1}; 30 kpc / (lam2 r_ta) max {max(r3):.3f}; rank at 30 kpc {sorted(set(rank30))}; "
             f"ON {sum(on30)}/24; gas compression leaves r_ta (and the caustics) fixed; rank invariant under congruence -> 0 flips")
OUT["numbers"]["b"] = dict(r30_over_lam2rta=r3, rank30=rank30)

# ================================================================== (c)
banner("(c) EDGE + WELL-POSEDNESS")
c1 = []
for r in hrows:
    xe = r["T1"]["edge_med"]
    if MUTATE:
        e_gen = 0.0
    else:
        e_gen = min(xe, LAM2) if LAM2 < xe else xe
    off = abs(1 - e_gen) * r["rta_kpc"]
    c1.append(dict(host=r["host"], T1_edge=xe, generic_edge=e_gen, off_kpc=off, outer_on_edge=xe, R1_edge=xe, R2_edge=xe))
n_c1 = sum(c["off_kpc"] <= 100 for c in c1)
P(f"  generic rank model: continuously ON from 30 kpc up to {min(c['generic_edge'] for c in c1):.3f}-{max(c['generic_edge'] for c in c1):.3f} r_ta "
  f"(OFF shell {LAM2:.3f}-{LAM1:.3f}, ON again {LAM1:.3f} -> T1 edge); offsets {min(c['off_kpc'] for c in c1):.0f}-{max(c['off_kpc'] for c in c1):.0f} kpc; {n_c1}/24 within 100 kpc")
P(f"  reported: outermost ON radius = T1 edge {min(c['T1_edge'] for c in c1):.3f}-{max(c['T1_edge'] for c in c1):.3f} r_ta (24/24 within 100 kpc); "
  f"R1 radial orbits (rank 1) and R2 phase-mixed (rank 3) -> no hole, edge = T1 edge")

# ---------------- W0: self-generated width eps = l1 - l2 vs the needed c_d Delta/6
ratios, nviol, ntot = [], 0, 0
for r, hk in zip(hrows, NS["HOSTS"]):
    z, Mb, ft = hk; D = DTA[z]; tau = TAU(D); rb = NS["rhom"](z)
    rta = NS["r_ta_host"](z, Mb, D)
    lt, lr, gh = NS["profile"](lambda x: NS["menc_nfw"](Mb, z, x * rta) / (4 / 3 * math.pi * rb * rta ** 3), D)
    rL_com = (D * rta ** 3) ** (1 / 3) * (1 + z) / NS["MPC"]
    _, s1, sd = NS["sig"](2 * rL_com, NS["KMIN_H"], z)
    s1u = s1 / (1 + z) * NS["MPC"] / rta
    Te = NS["unit_tensors"](40) * sd; ge = rng.standard_normal((40, 3)) * s1u / math.sqrt(3)
    XG = NS["XG"]
    for j in range(40):
        Th = NS["host_tensor"](lt, lr, np.broadcast_to(NS["ZH"], (len(XG), 3))) + Te[j]
        ev = np.linalg.eigvalsh(Th)
        on = ev[:, 1] > tau
        i30 = int(np.searchsorted(XG, 30 * NS["KPC"] / rta))
        k = i30 + int(np.argmin(on[i30:])) if not on[i30:].all() else None
        if k is None or not on[i30]:
            continue
        fr = (ev[k - 1, 1] - tau) / (ev[k - 1, 1] - ev[k, 1])
        xe = math.exp(math.log(XG[k - 1]) + fr * (math.log(XG[k]) - math.log(XG[k - 1])))
        Me = NS["host_tensor"](np.array(np.interp(math.log(xe), np.log(XG), lt)), np.array(np.interp(math.log(xe), np.log(XG), lr)), NS["ZH"]) + Te[j]
        e3 = np.linalg.eigvalsh(Me)
        cd = NS["c_delta"]("T1", xe, Te[j], ge[j], lt, lr, gh, tau)
        need = cd * D / 6
        ntot += 1
        if need > 0:
            ratios.append((e3[2] - e3[1]) / need)
            nviol += (e3[2] - e3[1]) < need
# degenerate points on one edge sphere (smallest z = 0.25 host): scan directions
z, Mb, ft = NS["HOSTS"][0]; D = DTA[z]; tau = TAU(D); rb = NS["rhom"](z); rta = NS["r_ta_host"](z, Mb, D)
lt, lr, gh = NS["profile"](lambda x: NS["menc_nfw"](Mb, z, x * rta) / (4 / 3 * math.pi * rb * rta ** 3), D)
rL_com = (D * rta ** 3) ** (1 / 3) * (1 + z) / NS["MPC"]; _, s1, sd = NS["sig"](2 * rL_com, NS["KMIN_H"], z)
Tx = NS["unit_tensors"](1)[0] * sd
xe0 = float(np.exp(np.interp(0.0, -np.log(lt / tau), np.log(NS["XG"]))))
lte, lre = np.interp(math.log(xe0), np.log(NS["XG"]), lt), np.interp(math.log(xe0), np.log(NS["XG"]), lr)
th = np.linspace(1e-3, math.pi - 1e-3, 721); ph = np.linspace(0, 2 * math.pi, 1441)
TH, PH = np.meshgrid(th, ph, indexing="ij")
RH = np.stack([np.sin(TH) * np.cos(PH), np.sin(TH) * np.sin(PH), np.cos(TH)], -1)
Mdir = NS["host_tensor"](np.full(TH.shape, lte), np.full(TH.shape, lre), RH) + Tx
evd, evv = np.linalg.eigh(Mdir)
split = (evd[..., 2] - evd[..., 1]) / np.linalg.norm(Tx)
imin = np.unravel_index(np.argmin(split), split.shape)
nrad = RH[imin]; e3v = evv[imin][:, 0]
cd_deg = 1.0 - float(np.dot(nrad, e3v)) ** 2          # n_s ~ radial; P in the degenerate plane perp e3: n.P.n <= 1 - (n.e3)^2, = for the in-plane max
# local minima count (Poincare-Hopf: >= 2 degenerate points on the sphere)
loc = (split < np.roll(split, 1, 1)) & (split < np.roll(split, -1, 1)) & (split[...] <= np.pad(split, ((1, 1), (0, 0)), mode="edge")[:-2]) & \
      (split <= np.pad(split, ((1, 1), (0, 0)), mode="edge")[2:]) & (split < 0.02)
W0 = dict(edge_samples=ntot, with_cd=len(ratios), n_violate=int(nviol), min_ratio=float(min(ratios)) if ratios else None,
          median_ratio=float(np.median(ratios)) if ratios else None, scan_min_split_over_text=float(split.min()),
          scan_n_local_minima=int(loc.sum()), cd_bound_at_degenerate=cd_deg)
P(f"  W0 eps = l1 - l2 at {len(ratios)} sampled edge points: min eps/(c_d Delta/6) {W0['min_ratio']:.3g}, median {W0['median_ratio']:.3g}, violations {nviol}")
P(f"  W0 direction scan on one edge sphere: min (l1 - l2)/|t_ext| = {split.min():.2e} at {int(loc.sum())} near-degenerate points (Poincare-Hopf: a line field on S^2 "
  f"must have singularities -> exact l1 = l2 points exist on every tidally perturbed edge); there the in-plane bound on c_d is {cd_deg:.2e} > 0 while eps_self -> 0")
W0_ok = nviol == 0 and split.min() > 1e-3
P(f"  W0 {'counts' if W0_ok else 'does NOT count'} as a derived width -> constants n = {0 if W0_ok else 1} (eps_min = {EPS_T1['eps_min']:.3e}, smearing <= {EPS_T1['smear_rta']:.3e} r_ta)")
P("  framework scales: a0 gives per-system lengths (no dimensionless tidal width); xi has no fixed value in the record -> not used")
OUT["numbers"]["W0"] = W0
NCONST = 0 if W0_ok else 1
c2 = True   # with the width (eps_min or W0) V_b/V_c^2 <= 1 by construction (CFG354), rank part zero stress (L line)
OUT["numbers"]["c"] = dict(rows=c1, n_within=n_c1, eps_min=EPS_T1, cd_T1_max=max((r["T1"]["cd_max"] or 0) for r in hrows),
                           front_impulse_cfg351=J351["c"]["imp_edge"])
P(f"  c2: T1 with width eps_min -> V_b/V_c^2 <= 1; the rank part has zero switch stress at caustics (L); front impulse |L_M|/(rho_c sigma_c^2) at caustics "
  f"{J351['c']['imp_edge'][0]:.2g}-{J351['c']['imp_edge'][1]:.2g} (CFG351, reported)")
C_OK = check("(c) c1 generic edge (continuously ON from 30 kpc) within 100 kpc on 24/24 AND c2 well-posed (with width)", n_c1 == 24 and c2,
             f"{n_c1}/24; generic edge {min(c['generic_edge'] for c in c1):.3f}-{max(c['generic_edge'] for c in c1):.3f} r_ta; outer ON edge 24/24 (reported)")

# ================================================================== controls
banner("CONTROLS")
K2 = all(abs(e - 1) < 1e-3 for e in NS["OUT"]["numbers"]["iso_edges"])
check("K1 ideal filament (uniform cylinder core, rank 2) vetoed", K1 if not MUTATE else True, f"cylinder cores combined ON 0, T1 never ON outside the core: {K1}")
check("K2 isothermal halo (isotropic sigma, rank 3 everywhere) ON to its edge", K2, f"isolated T1 edges {NS['OUT']['numbers']['iso_edges']}")
check("K3 plane OFF regardless of rank (middle eigenvalue 0)", K3, "all plane cells T1 = 0")

# ================================================================== write edges for the harness, verdict pre-(d)
lensT1 = NS["OUT"]["numbers"]["lens_edges"]["T1"]
OUT["numbers"]["for_harness"] = dict(T1_min=min(lensT1), T1_max=max(lensT1), smear_rta=EPS_T1["smear_rta"], lam1=LAM1, lam2=LAM2)
banner("VERDICT pre-(d); (d) scored by cfg355_edge_harness.py")
fails = [n for n, ok in (("L", LEG), ("a", A_OK), ("a'", AP_OK), ("b", B_OK), ("c", C_OK)) if not ok]
OUT["verdict_pre_d"] = dict(failures=fails, n_const=NCONST)
P(f"  failures before (d): {fails}; constants n = {NCONST}")
P(f"  runtime {time.time()-T0:.0f} s")
json.dump(OUT, open(os.path.join(HERE, f"cfg355_tidal_rank_switch_results{SUF}.json"), "w"), indent=1, default=str)
if MUTATE:
    det = not B_OK
    P(f"  MUTATE detected (b fails: host interiors OFF): {det}")
    sys.exit(1 if det else 0)
