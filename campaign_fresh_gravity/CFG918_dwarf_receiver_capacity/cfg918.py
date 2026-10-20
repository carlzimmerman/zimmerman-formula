"""CFG918 -- sol61 roadmap gate 1: outer-envelope energy / angular-momentum receiver capacity
for Draco, Sextans, Fornax and Leo I (one common model, finite stock).

Criteria: FROZEN_CRITERIA.md (commit d74df7476, committed alone before this script); Amendment A1 (commit 8c450e4d1,
POST HOC, three reported-only diagnostics PH1-PH3, no class weight).
Run from anywhere (one core, < 1 GB, numpy + stdlib only):
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg918.py K                 -> cfg918_K.out (controls only)
  CFG918_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg918.py   -> cfg918_MUTATE1.out, cfg918_results_MUTATE1.json
  CFG918_MUTATE=2 OMP_NUM_THREADS=1 nice -n 10 python3 cfg918.py   -> cfg918_MUTATE2.out, cfg918_results_MUTATE2.json
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg918.py                   -> cfg918.out, cfg918_results.json (controls + main)
  OMP_NUM_THREADS=1 nice -n 10 python3 cfg918.py R                 -> cfg918_REFINE.out, cfg918_results_REFINE.json
                                                                      (grid refinement, separate process, after main)
The K, MUTATE and main modes all rerun the controls; the MUTATE modes also recompute the frozen classes they compare to.
Units: pc, Msun, km/s; G in pc (km/s)^2 / Msun; energies in Msun (km/s)^2; J in Msun pc km/s.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, csv, json, math, hashlib, time
from decimal import Decimal
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = sys.argv[1] if (len(sys.argv) > 1 and sys.argv[1] in ("K", "R")) else "main"
MUT = os.environ.get("CFG918_MUTATE", "")
if MUT not in ("", "1", "2"):
    raise SystemExit("CFG918_MUTATE must be 1 or 2")
TAG = {"K": "_K", "R": "_REFINE"}.get(MODE, f"_MUTATE{MUT}" if MUT else "")
if MODE == "R" and MUT:
    raise SystemExit("refinement mode takes no MUTATE")
OUT = []
def P_(s=""):
    print(s, flush=True); OUT.append(str(s))

G_SI, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
G = G_SI * MSUN / (PC * 1e6)                     # pc (km/s)^2 / Msun  (same constants as CFG853)
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
PF = 64 / 125; SUP = 5.364; FRET = 0.1; STOCK = SUP / FRET
RC_CORE = 104.0                                   # CFG870 core radius (shape only)
LN10 = math.log(10.0)
NAMES = ["Draco", "Sextans", "Fornax", "Leo I"]
LAMS = np.round(np.linspace(0.0, 1.0, 101), 10)
PHIK = (0.0, 0.5, 1.0)
CORES = ("S", "U", "C")
NR, NX = 80, 60
NR_REF, NX_REF = 160, 120
CRITERIA_COMMIT = "d74df7476"; A1_COMMIT = "8c450e4d1"

# ---------------------------------------------------------------- inputs (record; CFG853 convention)
P_LVD = os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv")
P_827 = os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827_results.json")
P_824 = os.path.join(LANES, "CFG824_dwarf_age_fossil", "cfg824_results.json")
P_822 = os.path.join(LANES, "CFG822_hex_dsph", "cfg822_results.json")
P_861 = os.path.join(LANES, "CFG861_classical_dsph_binaries", "cfg861_results.json")
P_853 = os.path.join(LANES, "CFG853_cold_core_transport", "cfg853_results.json")
P_916 = os.path.join(LANES, "CFG916_lock_and_release", "cfg916_results.json")
P_RCT = os.path.join(REPO, "sol61_push", "formation_one_shot_2026_10_19", "receipt.json")
P_RMP = os.path.join(REPO, "sol61_push", "ROADMAP_COLD_ENERGY_MECHANISMS_2026-10-19.md")
INPUT_FILES = [P_LVD, P_827, P_824, P_822, P_861, P_853, P_916, P_RCT, P_RMP]
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
INPUT_HASHES = {os.path.relpath(p, REPO): sha(p) for p in INPUT_FILES}

lvd = {r["name"]: r for r in csv.DictReader(open(P_LVD))}
c827 = json.load(open(P_827))["rows"]
c824 = json.load(open(P_824))["rows"]
c822 = json.load(open(P_822))["rows"]
c861 = {s["name"]: s for s in json.load(open(P_861))["systems"]}
INP = {}
for n in NAMES:
    r = lvd[n]
    ups = c827[n]["ups"] if n in c827 else 2.0
    so, eso = (c824[n]["so"], c824[n]["eso"]) if n in c824 else (float(r["vlos_sigma"]), float(r["vlos_sigma_em"]))
    INP[n] = dict(MV=float(r["M_V"]), a=float(r["rhalf_sph_physical"]), ups=ups,
                  ups_src="CFG827 SFH" if n in c827 else "assumed 2", sig=so, esig=eso,
                  rta={f: 1000.0 * c822[f"{f}|{n}"]["rta_kpc"] for f in A0}, delta861=c861[n]["delta"])

def baseline(n, a0, branch="B0"):
    """CFG853 baseline (handoff convention); B1 applies the CFG861 shift sigma -> sigma 10^(delta/2)."""
    d = INP[n]
    sig = d["sig"] * (10 ** (d["delta861"] / 2.0) if branch == "B1" else 1.0)
    Ms = d["ups"] * 10 ** (0.4 * (4.83 - d["MV"])); a = d["a"]; R = 4.0 / 3.0 * a
    y = G_SI * PF * Ms * MSUN / (R * PC) ** 2 / a0
    s = min(PF * (math.sqrt(0.25 + 1.0 / y) - 0.5), SUP)
    Mrem = (STOCK - s) * Ms
    Mneed = 3 * R * sig ** 2 / G
    Mx = Ms * (3 * R * sig ** 2 / (G * Ms) - PF - s)
    return dict(name=n, branch=branch, Ms=Ms, a=a, R=R, s=s, sMs=s * Ms, y=y, sig=sig, Mrem=Mrem, Mneed=Mneed, Mx=Mx,
                F=Mx / Mrem, Mout=Mrem - Mx)

# ---------------------------------------------------------------- potentials and integrals
def M_pl(r, b): return b["Ms"] * r ** 3 / (r * r + b["a"] ** 2) ** 1.5
def phi_pl(r, b): return -G * b["Ms"] / np.sqrt(r * r + b["a"] ** 2)
def M_set(r, b): return b["sMs"] * np.minimum(r / b["R"], 1.0)
def phi_set(r, b):
    r = np.asarray(r, dtype=float); R = b["R"]
    inside = -G * b["sMs"] / R * (1.0 + np.log(R / np.minimum(r, R)))
    return np.where(r >= R, -G * b["sMs"] / np.maximum(r, 1e-300), inside)
def phi_ext(r, b): return phi_pl(r, b) + phi_set(r, b)

def simpson_log(f, r1, r2, n=20001):
    """int_{r1}^{r2} f(r) dr by composite Simpson in u = ln r (n odd)."""
    u = np.linspace(math.log(r1), math.log(r2), n); r = np.exp(u); y = f(r) * r
    h = (u[-1] - u[0]) / (n - 1)
    w = np.ones(n); w[1:-1:2] = 4.0; w[2:-1:2] = 2.0
    return float(h / 3.0 * np.dot(w, y))

def simpson_lin(f, r1, r2, n=20001):
    r = np.linspace(r1, r2, n); y = f(r); h = (r2 - r1) / (n - 1)
    w = np.ones(n); w[1:-1:2] = 4.0; w[2:-1:2] = 2.0
    return float(h / 3.0 * np.dot(w, y))

# ---------------------------------------------------------------- initial patch (M2)
def patch(b, rout):
    R, Ms, a, sMs, Mrem = b["R"], b["Ms"], b["a"], b["sMs"], b["Mrem"]
    mu = Mrem / (rout - R)
    Wcc = -G * mu ** 2 * ((rout - R) - R * math.log(rout / R))
    Wext = -G * Ms * mu * (math.asinh(rout / a) - math.asinh(R / a)) - G * sMs * mu * math.log(rout / R)
    Mtot = lambda r: M_pl(r, b) + sMs + mu * (r - R)
    Kvir = 0.5 * simpson_log(lambda r: G * Mtot(r) / r * mu, R, rout)
    J1 = (2.0 / 3.0) * simpson_log(lambda r: np.sqrt(G * Mtot(r) * r) * mu, R, rout)
    Wext_num = simpson_log(lambda r: phi_ext(r, b) * mu, R, rout)
    return dict(rout=rout, mu=mu, Wcc=Wcc, Wext=Wext, Wext_num=Wext_num, W=Wcc + Wext, Kvir=Kvir, J1=J1,
                rF=R + b["Mx"] / mu)

def E_init(pt, lam, phik):
    Krot = (2.0 / 3.0) * lam * lam * pt["Kvir"]
    return pt["W"] + Krot + phik * (pt["Kvir"] - Krot)

# ---------------------------------------------------------------- final core (M3)
def core_profile(state, Mx, Rc):
    if state == "U":
        g = lambda r: r ** 3; dg = lambda r: 3 * r * r
    else:
        g = lambda r: r ** 3 / (r * r + RC_CORE ** 2); dg = lambda r: r * r * (r * r + 3 * RC_CORE ** 2) / (r * r + RC_CORE ** 2) ** 2
    gR = g(Rc)
    return (lambda r: Mx * g(r) / gR), (lambda r: Mx * dg(r) / gR)

def core(b, state, Rc):
    Mx = b["Mx"]
    if state == "S":
        vc2 = G * (M_pl(Rc, b) + M_set(Rc, b) + Mx / 2.0) / Rc
        K = 0.5 * Mx * vc2; Wself = -G * Mx * Mx / (2 * Rc); Wext = Mx * float(phi_ext(Rc, b)); Jmax = Mx * Rc * math.sqrt(vc2)
    else:
        m, dm = core_profile(state, Mx, Rc); lo = Rc * 1e-7
        Wself = -G * simpson_log(lambda r: m(r) * dm(r) / r, lo, Rc)
        Wext = simpson_log(lambda r: phi_ext(r, b) * dm(r), lo, Rc)
        K = 0.5 * simpson_log(lambda r: G * (M_pl(r, b) + M_set(r, b) + m(r)) / r * dm(r), lo, Rc)
        Jmax = 0.0
    return dict(state=state, Rc=Rc, K=K, Wself=Wself, Wext=Wext, E=K + Wself + Wext, Jmax=Jmax)

# ---------------------------------------------------------------- receiver family (M3)
def family(b, cr, Rmax, Mout, nr=NR, nx=NX, rin=None):
    Mx = b["Mx"]
    Rc = cr["Rc"] if rin is None else rin          # receiver inner boundary (A1 PH1: 2R); core lies inside cr["Rc"]
    r = np.geomspace(Rc, Rmax, nr); xg = (np.arange(nx) + 1.0) / nx
    i1, i2 = np.triu_indices(nr)
    r1 = np.repeat(r[i1], nx); r2 = np.repeat(r[i2], nx); same12 = np.repeat(i1 == i2, nx)
    x = np.tile(xg, len(i1))
    mA = (1.0 - x) * Mout; mB = x * Mout
    Minner = lambda rr: M_pl(rr, b) + M_set(rr, b) + Mx
    vA2 = G * (Minner(r1) + mA / 2.0) / r1
    KA = 0.5 * mA * vA2
    WA = mA * phi_ext(r1, b) - G * Mx * mA / r1 - G * mA * mA / (2 * r1)
    WB = mB * phi_ext(r2, b) - G * Mx * mB / r2 - G * mA * mB / r2 - G * mB * mB / (2 * r2)
    Epart = cr["E"] + KA + WA + WB
    JA = mA * r1 * np.sqrt(vA2)
    def phiB(rr):
        return phi_ext(rr, b) - G * Mx / rr - G * mA / np.maximum(rr, r1) - G * (mB / 2.0) / np.maximum(rr, r2)
    PB2 = phiB(r2)
    dPc = phiB(np.full_like(r2, Rc)) - PB2
    dPm = phiB(np.full_like(r2, Rmax)) - PB2
    at_lo = r2 <= Rc * (1 + 1e-12); at_hi = r2 >= Rmax * (1 - 1e-12)
    with np.errstate(divide="ignore", invalid="ignore"):
        Klo = np.where(at_lo, 0.5 * mB * G * (Minner(r2) + np.where(same12, mA / 2.0, mA) + mB / 2.0) / r2,
                       mB * (-dPc) / ((r2 / Rc) ** 2 - 1.0))
        Khi = np.where(at_hi, 0.5 * mB * G * (Minner(r2) + np.where(same12, mA / 2.0, mA) + mB / 2.0) / r2,
                       mB * dPm / (1.0 - (r2 / Rmax) ** 2))
    Klo = np.maximum(Klo, 0.0)
    Elo = Epart + Klo; Ehi = np.where(Khi >= Klo, Epart + Khi, -np.inf)
    return dict(r1=r1, r2=r2, x=x, mA=mA, mB=mB, KA=KA, Epart=Epart, JA=JA, Klo=Klo, Khi=Khi, Elo=Elo, Ehi=Ehi,
                C=r2 * np.sqrt(2.0 * mB), Rc=Rc, Rmax=Rmax, Mout=Mout, Emax_RB=float(np.max(Ehi)), Emin=float(np.min(Elo)))

def jcap(fam, Etot, branch):
    ok = fam["Elo"] <= Etot
    if branch == "RB":
        ok &= Etot <= fam["Ehi"]
    if not ok.any():
        return -math.inf, -1
    J = np.where(ok, fam["JA"] + fam["C"] * np.sqrt(np.where(ok, Etot - fam["Epart"], 0.0)), -np.inf)
    k = int(np.argmax(J))
    return float(J[k]), k

# ---------------------------------------------------------------- independent energy recomputation (K7)
_CORE_IND = {}
def core_independent(b, cr):
    """Core energy by discrete thin shells (midpoint radii, exact shell masses, half self), Richardson N/2N."""
    key = (b["name"], b["branch"], round(b["s"], 12), cr["state"], round(cr["Rc"], 9))
    if key in _CORE_IND:
        return _CORE_IND[key]
    Rc, Mx = cr["Rc"], b["Mx"]
    def disc(N):
        if cr["state"] == "S":
            rk = np.array([Rc]); dmk = np.array([Mx])
        else:
            m, _ = core_profile(cr["state"], Mx, Rc)
            edges = Rc * np.linspace(0.0, 1.0, N + 1); dmk = np.diff(m(edges)); rk = 0.5 * (edges[1:] + edges[:-1])
        Menc = np.cumsum(dmk) - 0.5 * dmk
        Wself = float(-G * np.sum(Menc * dmk / rk))
        Wext = float(np.sum(phi_ext(rk, b) * dmk))
        Kc = float(0.5 * np.sum(G * (M_pl(rk, b) + M_set(rk, b) + Menc) / rk * dmk))
        return Kc + Wself + Wext
    if cr["state"] == "S":
        val = disc(1)
    else:
        e1, e2 = disc(20000), disc(40000); val = (4 * e2 - e1) / 3.0
    _CORE_IND[key] = val
    return val

def energy_independent(b, cr, fam, k, Etot):
    """Recompute E_fin of configuration k: discrete-shell core (Richardson) + explicit pair sums (receiver)."""
    Mx = b["Mx"]
    Ecore = core_independent(b, cr)
    r1, r2, mA, mB = fam["r1"][k], fam["r2"][k], fam["mA"][k], fam["mB"][k]
    KB = Etot - fam["Epart"][k]
    shells = [(r1, mA), (r2, mB)]
    W = 0.0
    for (rs, ms) in shells:
        W += ms * float(phi_ext(rs, b)) - G * Mx * ms / rs - G * ms * ms / (2 * rs)
    W += -G * mA * mB / max(r1, r2)
    KA = 0.5 * mA * G * (M_pl(r1, b) + M_set(r1, b) + Mx + mA / 2.0) / r1
    return Ecore + KA + KB + W

# ---------------------------------------------------------------- controls
def half_ulp(s):
    return 0.5 * float(Decimal(1).scaleb(Decimal(s).as_tuple().exponent))

ROADMAP_TABLE = {"Draco": ("2.77236e7", ".469303", ".427664"), "Sextans": ("2.53958e7", ".988540", ".645287"),
                 "Fornax": ("9.90289e8", ".0130695", ".0117393"), "Leo I": ("1.88437e8", ".0345131", ".0344714")}

def controls():
    rep = {}; ok_all = True
    def rec(name, ok, detail):
        nonlocal ok_all
        rep[name] = dict(ok=bool(ok), detail=detail); ok_all &= bool(ok)
        P_(f"  {name}: {'PASS' if ok else 'FAIL'}  {detail}")
    P_("CONTROLS")
    # K1 roadmap table + CFG853 JSON
    c853 = json.load(open(P_853))["footings"]["canonical"]["primary"]["base"]
    k1 = []; ok = True
    for n in NAMES:
        b0 = baseline(n, A0["canonical"], "B0"); b1 = baseline(n, A0["canonical"], "B1")
        sM, sF0, sF1 = ROADMAP_TABLE[n]
        for lab, val, ref in (("Mrem", b0["Mrem"], sM), ("F_B0", b0["F"], sF0), ("F_B1", b1["F"], sF1)):
            d = abs(val - float(ref)); good = d <= half_ulp(ref); ok &= good
            k1.append(f"{n} {lab} {val:.7g} vs {ref} ({'ok' if good else 'X'})")
        for lab in ("Mrem", "F"):
            good = abs(b0[lab] / c853[n][lab] - 1) <= 1e-9; ok &= good
            if not good: k1.append(f"{n} {lab} vs CFG853 JSON X")
    rec("K1 roadmap table (12 numbers, half-digit) + CFG853 JSON (1e-9)", ok, "; ".join(k1))
    # K2 receiver examples
    rct = json.load(open(P_RCT))["receiver_examples"]; ok = True; got = []
    for e in rct:
        j, al, ratio = e["j"], e["alpha"], e["Rout_over_Ri"]
        M = 1.0; Ri = 1.0; v = 1.0; Rout = ratio * Ri
        J = j * M * Ri * v; K = 0.5 * al * M * v * v
        mmin = J * J / (2.0 * Rout ** 2 * K) / M
        good = abs(mmin - e["minimum_receiver_fraction"]) <= 1e-12; ok &= good
        got.append(f"({j},{al})->{mmin:.6g}")
    rec("K2 roadmap j^2/alpha receiver fractions (9, 1e-12)", ok, " ".join(got))
    # K3a ring saturates CS; K3b random isotropic strict
    rng = np.random.default_rng(918)
    th = rng.uniform(0, 2 * np.pi, 1000); rr = 37.0; vv = 5.0; m = np.full(1000, 2.0)
    xx, yy = rr * np.cos(th), rr * np.sin(th); vx, vy = -vv * np.sin(th), vv * np.cos(th)
    J = np.sum(m * (xx * vy - yy * vx)); I = np.sum(m * (xx ** 2 + yy ** 2)); K = np.sum(0.5 * m * (vx ** 2 + vy ** 2))
    rec("K3a ring J^2 = 2IK", abs(J * J / (2 * I * K) - 1) <= 1e-12, f"ratio {J * J / (2 * I * K):.15f}")
    pos = rng.normal(size=(10000, 3)); pos *= (rng.uniform(1, 50, 10000) / np.linalg.norm(pos, axis=1))[:, None]
    vel = rng.normal(size=(10000, 3)) * 3.0
    Jz = np.sum(pos[:, 0] * vel[:, 1] - pos[:, 1] * vel[:, 0]); Iz = np.sum(pos[:, 0] ** 2 + pos[:, 1] ** 2)
    Kk = np.sum(0.5 * np.sum(vel ** 2, axis=1))
    rec("K3b random isotropic J^2 < 2IK", Jz * Jz < 2 * Iz * Kk, f"J^2/(2IK) = {Jz * Jz / (2 * Iz * Kk):.3e}")
    # K4 analytic energetics
    Mt, Rt = 3.7e6, 412.0
    Wu = -G * simpson_log(lambda r: (Mt * (r / Rt) ** 3) * (3 * Mt * r * r / Rt ** 3) / r, Rt * 1e-7, Rt)
    r_a, d_ = 300.0, 300.0 * 1e-8
    msh = lambda r: Mt * (r ** 3 - r_a ** 3) / ((r_a + d_) ** 3 - r_a ** 3)
    dmsh = lambda r: Mt * 3 * r * r / ((r_a + d_) ** 3 - r_a ** 3)
    Wsh = -G * simpson_lin(lambda r: msh(r) * dmsh(r) / r, r_a, r_a + d_, 2001)
    mu_, ra_, rb_ = 1234.0, 200.0, 9000.0
    Wr2 = -G * simpson_log(lambda r: mu_ * (r - ra_) * mu_ / r, ra_, rb_)
    Wr2a = -G * mu_ ** 2 * ((rb_ - ra_) - ra_ * math.log(rb_ / ra_))
    ap = 250.0
    Mp = lambda r: Mt * r ** 3 / (r * r + ap * ap) ** 1.5; dMp = lambda r: 3 * Mt * ap * ap * r * r / (r * r + ap * ap) ** 2.5
    Wp = -G * simpson_log(lambda r: Mp(r) * dMp(r) / r, ap * 1e-6, ap * 1e6, 200001)
    tests = [("uniform", Wu, -0.6 * G * Mt * Mt / Rt), ("thin shell", Wsh, -G * Mt * Mt / (2 * r_a)),
             ("r^-2 shell", Wr2, Wr2a), ("Plummer", Wp, -3 * math.pi / 32 * G * Mt * Mt / ap)]
    ok = all(abs(w / ref - 1) <= 1e-6 for _, w, ref in tests)
    # patch external integral analytic vs numeric (same tolerance), all dwarfs/footings/geometries
    worst = 0.0
    for f in A0:
        for n in NAMES:
            b = baseline(n, A0[f])
            for rout in (INP[n]["rta"][f], 5 * b["R"]):
                pt = patch(b, rout); worst = max(worst, abs(pt["Wext_num"] / pt["Wext"] - 1))
    ok &= worst <= 1e-6
    rec("K4 analytic energetics (1e-6)", ok, "; ".join(f"{t} {w / ref - 1:+.2e}" for t, w, ref in tests) + f"; patch W_ext worst {worst:.2e}")
    # K5 CE-FM-089 Sextans example
    Mi, Ri_, fc, Rf = 2.540e7, 3239.0, 0.988540, 25.21
    Ei = -0.3 * G * Mi * Mi / Ri_; Ef = -0.3 * G * (fc * Mi) ** 2 / Rf
    rel_J = (Ei - Ef) * MSUN * 1e6; vinf = math.sqrt(2 * (Ei - Ef) / ((1 - fc) * Mi))
    ok = abs(rel_J - 6.37e46) <= half_ulp("6.37e46") and abs(vinf - 469) <= 0.5
    rec("K5 CE-FM-089 release 6.37e46 J / 469 km/s", ok, f"{rel_J:.4e} J, {vinf:.2f} km/s")
    # K6 roadmap Sextans 1-F
    bs0 = baseline("Sextans", A0["canonical"], "B0"); bs1 = baseline("Sextans", A0["canonical"], "B1")
    ok = abs((1 - bs0["F"]) - 0.01146) <= half_ulp(".01146") and abs((1 - bs1["F"]) - 0.35471) <= half_ulp(".35471")
    rec("K6 Sextans 1-F .01146 / .35471", ok, f"{1 - bs0['F']:.6f} / {1 - bs1['F']:.6f}")
    # K3c / K7 on optimum configurations
    worst3, worst7, nopt = 0.0, 0.0, 0
    for n in NAMES:
        b = baseline(n, A0["canonical"])
        for rout in (INP[n]["rta"]["canonical"], 5 * b["R"]):
            pt = patch(b, rout)
            for st in CORES:
                cr = core(b, st, b["R"]); fam = family(b, cr, INP[n]["rta"]["canonical"], b["Mout"])
                for br in ("RB", "RE"):
                    for lam, phik in ((0.0, 0.0), (1.0, 1.0)):
                        Et = E_init(pt, lam, phik); Jc, k = jcap(fam, Et, br)
                        if k >= 0:
                            w3, w7 = optimum_checks(b, cr, fam, k, Et, Jc)
                            worst3 = max(worst3, w3); worst7 = max(worst7, w7); nopt += 1
                del fam
    rec("K3c optimum J^2 <= 2 Mout Rmax^2 (KA+KB) [subset]", worst3 <= 1 + 1e-12, f"max ratio {worst3:.6f} over {nopt} optima")
    rec("K7 ledger closure, independent recomputation (1e-9 rel) [subset]", worst7 <= 1e-9,
        f"max |dE/E| {worst7:.2e} (discrete-shell core, Richardson 2e4/4e4)")
    return ok_all, rep

def optimum_checks(b, cr, fam, k, Et, Jc):
    KB = Et - fam["Epart"][k]
    bound = 2 * fam["Mout"] * fam["Rmax"] ** 2 * (fam["KA"][k] + KB)
    w3 = Jc * Jc / bound if bound > 0 else (0.0 if Jc == 0 else math.inf)
    w7 = abs(energy_independent(b, cr, fam, k, Et) - Et) / abs(Et)
    return w3, w7

TRACK = dict(K3c=0.0, K7=0.0, n=0)

# ---------------------------------------------------------------- main evaluation
def evaluate_cell_set(f, branch, mut="", nr=NR, nx=NX, keep_opt=False, track=False, rin_fac=1.0, cores=CORES):
    """All cells for one footing and mass branch.  Returns per-dwarf/geometry/receiver-branch results."""
    a0 = A0[f]; res = {}
    for n in NAMES:
        b = baseline(n, a0, branch)
        Mout = b["Mout"] * (0.01 if mut == "2" else 1.0)
        res[n] = dict(base={k: b[k] for k in ("Ms", "a", "R", "s", "sig", "Mrem", "Mneed", "Mx", "F", "Mout")}, geoms={})
        res[n]["base"]["Mout_used"] = Mout
        for g in ("G1", "G2"):
            rout = INP[n]["rta"][f] if g == "G1" else 5 * b["R"]
            pt = patch(b, rout)
            Rc = pt["rF"] if mut == "1" else b["R"]
            rmax_set = [INP[n]["rta"][f]] if g == "G1" else [5 * b["R"], INP[n]["rta"][f]]
            crs = {st: core(b, st, Rc) for st in cores}
            gres = dict(patch={k: pt[k] for k in ("rout", "mu", "Wcc", "Wext", "W", "Kvir", "J1", "rF")},
                        cores={st: {k: crs[st][k] for k in ("Rc", "K", "Wself", "Wext", "E", "Jmax")} for st in cores},
                        Emax_RB={}, Emin={}, rmax_set=rmax_set, rb={})
            passmat = {"RB": {}, "RE": {}}; jinfo = {"RB": {}, "RE": {}}
            for st in cores:
                for rm in rmax_set:
                    fam = family(b, crs[st], rm, Mout, nr, nx, rin=(None if rin_fac == 1.0 else rin_fac * Rc))
                    gres["Emax_RB"][f"{st}|{rm:.6g}"] = fam["Emax_RB"]; gres["Emin"][f"{st}|{rm:.6g}"] = fam["Emin"]
                    for rb in ("RB", "RE"):
                        for phik in PHIK:
                            arr = np.zeros(len(LAMS), dtype=bool); jc_list = []; cache = {}
                            for il, lam in enumerate(LAMS):
                                Et = E_init(pt, lam, phik)
                                if Et not in cache: cache[Et] = jcap(fam, Et, rb)
                                Jc, k = cache[Et]
                                Ji = lam * pt["J1"]; Jreq = Ji - min(Ji, crs[st]["Jmax"])
                                arr[il] = (k >= 0) and (Jc >= Jreq)
                                if track and k >= 0:
                                    w3, w7 = optimum_checks(b, crs[st], fam, k, Et, Jc)
                                    TRACK["K3c"] = max(TRACK["K3c"], w3); TRACK["K7"] = max(TRACK["K7"], w7); TRACK["n"] += 1
                                if il in (0, len(LAMS) - 1):
                                    KB = Et - fam["Epart"][k] if k >= 0 else None
                                    jc_list.append(dict(lam=float(lam), Etot=Et, Jcap=Jc if k >= 0 else None, Jreq=Jreq,
                                                        cfg=(dict(r1=float(fam["r1"][k]), r2=float(fam["r2"][k]), x=float(fam["x"][k]),
                                                                  mA=float(fam["mA"][k]), mB=float(fam["mB"][k]), KA=float(fam["KA"][k]),
                                                                  KB=float(KB), B_leaves=bool(KB > fam["Khi"][k]),
                                                                  CS_bound=float(math.sqrt(2 * Mout * rm ** 2 * (fam["KA"][k] + KB))),
                                                                  Mout_min_CS=(float(Jreq ** 2 / (2 * rm ** 2 * (fam["KA"][k] + KB)))
                                                                               if (fam["KA"][k] + KB) > 0 else None))
                                                             if k >= 0 else None)))
                            passmat[rb][(phik, st, rm)] = arr; jinfo[rb][(phik, st, rm)] = jc_list
                    del fam
            for rb in ("RB", "RE"):
                pm = passmat[rb]; keys = sorted(pm.keys(), key=lambda t: (t[0], t[1], t[2]))
                M = np.array([pm[k] for k in keys])          # combos x lams
                any_l = M.any(axis=0); all_l = M.all(axis=0)
                if not any_l.any(): cls = "CAPACITY EXCLUDED"
                elif all_l.all(): cls = "CAPACITY ALLOWED"
                else: cls = "INDETERMINATE"
                lam_mf = float(LAMS[np.where(any_l)[0].max()]) if any_l.any() else None
                contiguous_mf = bool(any_l[: (np.where(any_l)[0].max() + 1)].all()) if any_l.any() else None
                if all_l[0]:
                    stop = np.where(~all_l)[0]; lam_all = float(LAMS[stop[0] - 1]) if len(stop) else 1.0
                else:
                    lam_all = None
                dec0 = [f"phiK={k[0]},{k[1]},Rmax={k[2]:.0f}" for k in keys if not pm[k][0]]
                dec1 = [f"phiK={k[0]},{k[1]},Rmax={k[2]:.0f}" for k in keys if pm[k][-1]]
                lc = {}
                for kk in keys:
                    arr = pm[kk]
                    if not arr[0]: lc[f"{kk[0]}|{kk[1]}|{kk[2]:.6g}"] = None
                    else:
                        stop = np.where(~arr)[0]; lc[f"{kk[0]}|{kk[1]}|{kk[2]:.6g}"] = float(LAMS[stop[0] - 1]) if len(stop) else 1.0
                lamP = lambda lam, p: lam * pt["J1"] * math.sqrt(abs(E_init(pt, lam, p))) / (G * b["Mrem"] ** 2.5)
                entry = dict(cls=cls, lam_crit_MF=lam_mf, MF_set_contiguous=contiguous_mf, lam_crit_all=lam_all,
                             fail_at_lam0=dec0, pass_at_lam1=dec1, lam_crit_by_combo=lc,
                             PH2_lambdaP={lab: ({f"phiK{p}": lamP(v, p) for p in (0.0, 1.0)} if v is not None else None)
                                          for lab, v in (("at_lam_crit_MF", lam_mf), ("at_lam_crit_all", lam_all))})
                if keep_opt:
                    entry["opt"] = {f"{k[0]}|{k[1]}|{k[2]:.6g}": jinfo[rb][k] for k in keys}
                gres["rb"][rb] = entry
            E0 = E_init(pt, 0.0, 0.0)
            gres["RB_shortfall_MF"] = E0 - max(gres["Emax_RB"].values())
            gres["stars_tolerance"] = PF * b["Ms"] * 3 * b["sig"] ** 2 * LN10
            gres["E_init_corners"] = {f"lam{l}|phiK{p}": E_init(pt, l, p) for l in (0.0, 1.0) for p in PHIK}
            gres["lambda_P_at_lam1"] = {f"phiK{p}": pt["J1"] * math.sqrt(abs(E_init(pt, 1.0, p))) / (G * b["Mrem"] ** 2.5) for p in PHIK}
            res[n]["geoms"][g] = gres
    return res

def classes_flat(allres):
    out = {}
    for f in allres:
        for br in allres[f]:
            for n in allres[f][br]:
                for g in allres[f][br][n]["geoms"]:
                    for rb in ("RB", "RE"):
                        out[f"{f}|{br}|{n}|{g}|{rb}"] = allres[f][br][n]["geoms"][g]["rb"][rb]["cls"]
    return out

SHORT = {"CAPACITY EXCLUDED": "EXCL", "CAPACITY ALLOWED": "ALLOW", "INDETERMINATE": "INDET"}

def print_tables(allres, label):
    P_(f"\n=== CLASSES ({label}) ===")
    for f in A0:
        for br in ("B0", "B1"):
            P_(f"\n-- footing {f}, mass branch {br} --")
            P_(f"{'dwarf':8s} {'F':>9s} {'Mx[Msun]':>10s} {'Mout':>10s} | {'G1 RB':>22s} {'G1 RE':>22s} | {'G2 RB':>22s} {'G2 RE':>22s}")
            for n in NAMES:
                r = allres[f][br][n]; b = r["base"]
                cells = []
                for g in ("G1", "G2"):
                    for rb in ("RB", "RE"):
                        e = r["geoms"][g]["rb"][rb]
                        lm = "-" if e["lam_crit_MF"] is None else f"{e['lam_crit_MF']:.2f}"
                        la = "-" if e["lam_crit_all"] is None else f"{e['lam_crit_all']:.2f}"
                        cells.append(f"{SHORT[e['cls']]:5s} MF{lm:>4s} all{la:>4s}")
                P_(f"{n:8s} {b['F']:9.6f} {b['Mx']:10.4g} {b['Mout_used']:10.4g} | {cells[0]:>22s} {cells[1]:>22s} | {cells[2]:>22s} {cells[3]:>22s}")

def summaries(allres):
    summ = {}; four = {}
    for f in allres:
        for br in allres[f]:
            for rb in ("RB", "RE"):
                for n in NAMES:
                    c1 = allres[f][br][n]["geoms"]["G1"]["rb"][rb]["cls"]; c2 = allres[f][br][n]["geoms"]["G2"]["rb"][rb]["cls"]
                    if c1 == c2 == "CAPACITY EXCLUDED": s = "CAPACITY EXCLUDED"
                    elif c1 == c2 == "CAPACITY ALLOWED": s = "CAPACITY ALLOWED"
                    else: s = "INDETERMINATE"
                    summ[f"{f}|{br}|{n}|{rb}"] = s
                for g in ("G1", "G2"):
                    cl = [allres[f][br][n]["geoms"][g]["rb"][rb]["cls"] for n in NAMES]
                    four[f"{f}|{br}|{g}|{rb}"] = "BROKEN" if "CAPACITY EXCLUDED" in cl else "no capacity obstruction (not formation)"
    return summ, four

# ---------------------------------------------------------------- run
P_("CFG918 -- sol61 roadmap gate 1: outer-envelope E/J receiver capacity (Draco, Sextans, Fornax, Leo I)")
P_(f"criteria {CRITERIA_COMMIT} (+ A1 {A1_COMMIT}, post hoc, reported only); mode {MODE}; MUTATE {MUT or 'off'}; G = {G:.6e} pc (km/s)^2/Msun")
P_("kappa = 1/2 FITTED; footings never pooled; B0/B1 never pooled; necessary capacity only (not formation)")
P_("inputs:")
for kk, vv in INPUT_HASHES.items():
    P_(f"  {kk}  sha256 {vv[:16]}")
for n in NAMES:
    d = INP[n]
    P_(f"  {n:8s} M_V {d['MV']:.2f} a {d['a']:.2f} pc Ups {d['ups']:.4f} ({d['ups_src']}) sigma {d['sig']} delta861 {d['delta861']:+.5f} "
       f"r_ta {d['rta']['canonical']:.0f}/{d['rta']['alt']:.0f} pc")

ok_K, rep_K = controls()
P_(f"controls {'ALL PASS' if ok_K else 'FAILED'}  ({time.time() - T0:.1f} s)")

result = dict(lane="CFG918", criteria_commit=CRITERIA_COMMIT, amendment_A1=A1_COMMIT, mode=MODE, mutate=MUT or None,
              script_sha256=sha(os.path.abspath(__file__)), input_hashes=INPUT_HASHES, controls=rep_K, controls_pass=ok_K,
              constants=dict(G=G, A0=A0, PF=PF, SUP=SUP, FRET=FRET, STOCK=STOCK, RC_CORE=RC_CORE, NR=NR, NX=NX))

if MODE == "K":
    open(os.path.join(HERE, f"cfg918{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if ok_K else 1)

if MODE == "R":
    # grid refinement as its own process (keeps each process well under 1 GB); frozen-grid classes stand
    frozen = json.load(open(os.path.join(HERE, "cfg918_results.json")))
    cls0 = frozen["classes"]; fres = frozen["results"]
    P_("\n=== GRID REFINEMENT (r 160, x 120; reported, frozen-grid class stands) ===")
    refres = {f: {br: evaluate_cell_set(f, br, "", NR_REF, NX_REF) for br in ("B0", "B1")} for f in A0}
    clsR = classes_flat(refres)
    chg = {k: (cls0[k], clsR[k]) for k in cls0 if cls0[k] != clsR[k]}
    P_(f"  {len(chg)} of {len(cls0)} classes change under refinement")
    for k, v in chg.items():
        P_(f"  FLAG {k}: {v[0]} -> {v[1]}")
    lamshift = []
    for f in A0:
        for br in ("B0", "B1"):
            for n in NAMES:
                for g in ("G1", "G2"):
                    for rb in ("RB", "RE"):
                        a_ = fres[f][br][n]["geoms"][g]["rb"][rb]; b_ = refres[f][br][n]["geoms"][g]["rb"][rb]
                        for kk in ("lam_crit_MF", "lam_crit_all"):
                            if a_[kk] != b_[kk]: lamshift.append(f"{f}|{br}|{n}|{g}|{rb} {kk} {a_[kk]} -> {b_[kk]}")
    P_(f"  lambda_crit entries that move: {len(lamshift)}")
    for s_ in lamshift:
        P_("    " + s_)
    result["refinement_changed"] = chg; result["refinement_lam_shifts"] = lamshift
    result["refined_classes"] = clsR; result["frozen_results_sha256"] = sha(os.path.join(HERE, "cfg918_results.json"))
    result["refined_results"] = refres
    P_(f"\nruntime {time.time() - T0:.1f} s")
    open(os.path.join(HERE, f"cfg918{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(result, open(os.path.join(HERE, f"cfg918_results{TAG}.json"), "w"), indent=1, default=float)
    sys.exit(0 if ok_K else 1)

# frozen classes (needed by main and MUTATE modes)
P_("\nMOST FAVOURABLE RECEIVER AUDIT FIRST: lam_c = 0 column of each cell decides EXCLUDED (see 'MF' entries)")
allres = {f: {br: evaluate_cell_set(f, br, "", keep_opt=(not MUT), track=True) for br in ("B0", "B1")} for f in A0}
ok3 = TRACK["K3c"] <= 1 + 1e-12; ok7 = TRACK["K7"] <= 1e-9
P_(f"\n  K3c [all {TRACK['n']} optima of the frozen run]: {'PASS' if ok3 else 'FAIL'}  max J^2/(2 Mout Rmax^2 K) = {TRACK['K3c']:.6f}")
P_(f"  K7  [all {TRACK['n']} optima of the frozen run]: {'PASS' if ok7 else 'FAIL'}  max |dE/E| = {TRACK['K7']:.2e}")
rep_K["K3c all optima"] = dict(ok=bool(ok3), detail=f"max {TRACK['K3c']:.6f} over {TRACK['n']}")
rep_K["K7 all optima"] = dict(ok=bool(ok7), detail=f"max {TRACK['K7']:.2e} over {TRACK['n']}")
ok_K = ok_K and ok3 and ok7
result["controls"] = rep_K; result["controls_pass"] = ok_K
print_tables(allres, "frozen")
cls0 = classes_flat(allres)
summ, four = summaries(allres)
result["classes"] = cls0; result["summary_across_geometries"] = summ; result["four_dwarf"] = four

if MUT:
    mres = {f: {br: evaluate_cell_set(f, br, MUT) for br in ("B0", "B1")} for f in A0}
    print_tables(mres, f"MUTATE-{MUT}")
    cls1 = classes_flat(mres)
    changed = {k: (cls0[k], cls1[k]) for k in cls0 if cls0[k] != cls1[k]}
    bites = len(changed) >= 1
    P_(f"\nMUTATE-{MUT}: {len(changed)} of {len(cls0)} graded classes change -> {'BITES' if bites else 'DOES NOT BITE'}")
    for k, v in changed.items():
        P_(f"  {k}: {v[0]} -> {v[1]}")
    result["mutate_classes"] = cls1; result["mutate_changed"] = changed; result["mutate_bites"] = bites
    result["mutate_results"] = mres
    result["frozen_results"] = allres
    open(os.path.join(HERE, f"cfg918{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(result, open(os.path.join(HERE, f"cfg918_results{TAG}.json"), "w"), indent=1, default=float)
    sys.exit(0 if (ok_K and bites) else 1)

# main: detail, summaries, refinement
P_("\n=== SUMMARY ACROSS GEOMETRIES (per dwarf x branch x footing x receiver branch) ===")
for k, v in summ.items():
    P_(f"  {k}: {v}")
P_("\n=== FOUR-DWARF LINE (per footing x branch x geometry x receiver branch) ===")
for k, v in four.items():
    P_(f"  {k}: {v}")

P_("\n=== AMENDMENT A1 (POST HOC, reported only, no class weight) ===")
ph = {}
for lab, kw in (("PH1 receiver r >= 2R", dict(rin_fac=2.0)), ("PH3 record cored core only", dict(cores=("C",)))):
    pres = {f: {br: evaluate_cell_set(f, br, "", **kw) for br in ("B0", "B1")} for f in A0}
    print_tables(pres, lab)
    clsP = classes_flat(pres)
    chgP = {k: (cls0[k], clsP[k]) for k in cls0 if cls0[k] != clsP[k]}
    P_(f"  {lab}: {len(chgP)} of {len(cls0)} classes differ from the frozen classes")
    for k, v in chgP.items():
        P_(f"    {k}: {v[0]} -> {v[1]}")
    ph[lab] = dict(classes=clsP, changed=chgP,
                   lam={k: (pres[k.split('|')[0]][k.split('|')[1]][k.split('|')[2]]['geoms'][k.split('|')[3]]['rb'][k.split('|')[4]]['lam_crit_MF'],
                            pres[k.split('|')[0]][k.split('|')[1]][k.split('|')[2]]['geoms'][k.split('|')[3]]['rb'][k.split('|')[4]]['lam_crit_all'])
                        for k in clsP})
result["A1_posthoc"] = ph
P_("  PH2 Peebles spin at the critical lambda_c (phiK 0 / 1), frozen classes:")
for f in A0:
    for br in ("B0", "B1"):
        for n in NAMES:
            for g in ("G1", "G2"):
                for rb in ("RB", "RE"):
                    e = allres[f][br][n]["geoms"][g]["rb"][rb]
                    if e["cls"] == "INDETERMINATE":
                        lp = e["PH2_lambdaP"]
                        fm = lambda d: "-" if d is None else f"{d['phiK0.0']:.3f}/{d['phiK1.0']:.3f}"
                        P_(f"    {f}|{br}|{n}|{g}|{rb}: lam_c,MF {e['lam_crit_MF']} -> lambda_P {fm(lp['at_lam_crit_MF'])}; "
                           f"lam_c,all {e['lam_crit_all']} -> lambda_P {fm(lp['at_lam_crit_all'])}")

P_("\n=== LEDGERS (canonical and alt; B0 and B1) ===")
for f in A0:
    for br in ("B0", "B1"):
        for n in NAMES:
            r = allres[f][br][n]; b = r["base"]
            P_(f"\n[{f} {br} {n}] M*={b['Ms']:.4g} R={b['R']:.1f} pc s={b['s']:.4f} sigma={b['sig']:.4f} M_need={b['Mneed']:.4g} "
               f"M_rem={b['Mrem']:.6g} M_x={b['Mx']:.6g} (F={b['F']:.6f}) M_out={b['Mout_used']:.6g}")
            for g in ("G1", "G2"):
                gr = r["geoms"][g]; pt = gr["patch"]
                P_(f"  {g}: r_out={pt['rout']:.0f} pc  W_cc,i={pt['Wcc']:.4g}  W_ext,i={pt['Wext']:.4g}  K_vir={pt['Kvir']:.4g}  "
                   f"J_1={pt['J1']:.4g}  E_init(lam0,phiK0)={gr['E_init_corners']['lam0.0|phiK0.0']:.4g}  "
                   f"E_init(lam1,phiK1)={gr['E_init_corners']['lam1.0|phiK1.0']:.4g}  lambda_P(lam1,phiK0/1)="
                   f"{gr['lambda_P_at_lam1']['phiK0.0']:.3f}/{gr['lambda_P_at_lam1']['phiK1.0']:.3f}")
                P_("      cores: " + "  ".join(f"{st}: E_f={gr['cores'][st]['E']:.4g} J_keep={gr['cores'][st]['Jmax']:.3g}" for st in CORES))
                P_("      RB max bound-envelope final energy (core|Rmax): " +
                   "  ".join(f"{k}={v:.4g}" for k, v in gr["Emax_RB"].items()))
                P_(f"      RB energy shortfall at MF corner (lam0, phiK0, best core/Rmax) = {gr['RB_shortfall_MF']:.4g}  "
                   f"(stars' permissive tolerance p M* 3 sigma^2 ln10 = {gr['stars_tolerance']:.3g})")
                for rb in ("RB", "RE"):
                    e = gr["rb"][rb]
                    P_(f"      {rb}: {e['cls']}  lam_crit,MF={e['lam_crit_MF']}  lam_crit,all={e['lam_crit_all']}  "
                       f"fail@lam0: {len(e['fail_at_lam0'])}/{len(e['lam_crit_by_combo'])}  pass@lam1: {len(e['pass_at_lam1'])}/{len(e['lam_crit_by_combo'])}")
                    # one representative optimum: most favourable core S at the largest Rmax, phiK 1, lam 1
                    key = f"1.0|S|{gr['rmax_set'][-1]:.6g}"
                    o = e["opt"][key][-1]
                    if o["cfg"] is not None:
                        c = o["cfg"]
                        P_(f"         optimum (phiK1, core S, Rmax {gr['rmax_set'][-1]:.0f}, lam 1): J_req={o['Jreq']:.4g} J_cap={o['Jcap']:.4g} "
                           f"[A: {c['mA']:.3g} at {c['r1']:.0f} pc; B: {c['mB']:.3g} at {c['r2']:.0f} pc, K_B={c['KB']:.3g}, "
                           f"{'leaves R_max' if c['B_leaves'] else 'bound'}; CS form sqrt(2 Mout Rmax^2 K)={c['CS_bound']:.4g}]")
                    else:
                        P_(f"         optimum (phiK1, core S, Rmax {gr['rmax_set'][-1]:.0f}, lam 1): no energy-feasible configuration")

# present Jacobi radii context (CFG916, canonical/alt, present)
try:
    d916 = json.load(open(P_916))["readings"]["LR-x"]["D"]
    rj = {}
    for f, fk in (("canonical", "can"), ("alt", "alt")):
        for ep in ("present", "peri"):
            for n, v in d916[fk]["sat"][ep]["rJ_over_r12"].items():
                if n in NAMES: rj[f"{f}|{ep}|{n}"] = v
    result["context_rJ_over_R_CFG916"] = rj
    P_("\ncontext: CFG916 Jacobi radius / R (R = 4a/3), present and pericentre: " + "  ".join(f"{k}={v:.2f}" for k, v in rj.items()))
except Exception as ex:
    P_(f"\ncontext: CFG916 Jacobi radii unavailable ({ex})")

P_("\ngrid refinement (r 160, x 120): separate process, `python3 cfg918.py R` -> cfg918_REFINE.out")
result["results"] = allres
P_(f"\nruntime {time.time() - T0:.1f} s")
open(os.path.join(HERE, f"cfg918{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(result, open(os.path.join(HERE, f"cfg918_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if ok_K else 1)
