#!/usr/bin/env python3
"""CFG934 -- cooling-floor primordial halos (H-CF): a parameter-free supply for faint dwarfs.
Criteria: FROZEN_CRITERIA.md (9782c3df7, committed alone before this script existed).

H-CF: every star-forming dwarf sits in a primordial cold-matter halo of at least M_cool(z_f), the halo whose virial temperature
T_vir = mu m_p V_c^2 / (2 k_B) reaches 1e4 K at its formation epoch z_f (Weisz+14 tau50 / tau90).  Native background and
Delta_vir from CFG654 (A1 CMB set, N0 turnaround table); NFW with rho_s = C rho_m(z_f), C in {1500, 3000, 6000}; CFG42/CFG45
readings (S) sum [primary] and (M) max [alternative]; classes U, C, M, I, S, L (criteria section 3).

Run (one core, one process):  OMP_NUM_THREADS=1 nice -n 10 python3 cfg934.py   with CFG934_MODE = K | MUTATE_T100 | MUTATE_T001 | main
(default main).  K must pass before MUTATE / main run (they read cfg934_results_K.json).  Each mode writes its own outputs.
Other lanes' code is exec'd read-only (writes refused); their JSON files are only read.
kappa = 1/2 FITTED; the footings are never pooled; cold energy, not a particle; not theory closed."""
import os, sys, io, math, json, time, csv, contextlib, builtins, resource
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import spearmanr

for _v in ("MUTATE", "CFG827_MUTATE", "CFG874_MUTATE", "CFG880_MUTATE"):
    os.environ.pop(_v, None)
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MODE = os.environ.get("CFG934_MODE", "main"); assert MODE in ("K", "MUTATE_T100", "MUTATE_T001", "main"), MODE
TFAC = {"MUTATE_T100": 100.0, "MUTATE_T001": 0.01}.get(MODE, 1.0)
SUF = {"K": "_K", "MUTATE_T100": "_MUTATE_T100", "MUTATE_T001": "_MUTATE_T001", "main": ""}[MODE]
OUT = []; T0W = time.time(); CHECKS = []
FOOTS = ("canonical", "alt")


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e6 if sys.platform == "darwin" else r / 1e3


def check(name, ok, detail):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}"); return bool(ok)


_real_open = builtins.open


def ro_open(file, mode="r", *a, **k):
    if any(ch in mode for ch in "wax+"):
        raise PermissionError(f"CFG934: write refused inside exec'd code ({os.path.basename(str(file))})")
    return _real_open(file, mode, *a, **k)


def exec_prefix(path, marker, name, env0=None):
    src = _real_open(path).read()
    g = {"__file__": path, "__name__": name, "open": ro_open}
    saved = {k: os.environ.get(k) for k in (env0 or {})}
    for k, v in (env0 or {}).items():
        os.environ[k] = v
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:src.index(marker)], name, "exec"), g)
    finally:
        for k, v in saved.items():
            os.environ.pop(k) if v is None else os.environ.__setitem__(k, v)
    return g


def J(*p):
    return json.load(_real_open(os.path.join(LANES, *p)))


P(__doc__.split("Run (one core")[0].strip())
P(f"\n  MODE {MODE}" + (f"   *** T_vir x {TFAC:g} ***" if TFAC != 1.0 else ""))

# =====================================================================================================================  inputs (read-only)
BAR = "# ================================================================================================ "
g42 = exec_prefix(os.path.join(LANES, "CFG42_satellites_rule.py"), BAR + "C1 / C2", "cfg42", env0={"MUTATE": "0"})
SAMPLES, UL, A0H, UPS_V, a_int = g42["SAMPLES"], g42["UL"], g42["A0H"], g42["UPS_V"], g42["a_int"]
GSAT, MSAT, infall_gas, halo_mass, nfw_DM = g42["G"], g42["Msun"], g42["infall_gas"], g42["halo_mass"], g42["nfw_enclosed"]
EDGE, FB42, g10, C7 = g42["edge_phantom"], g42["FB"], g42["g10"], g42["C"]
A0X = dict(C7.A0_SI)                                                  # exact footings 9.3603e-11 / 1.1312e-10
assert abs(A0X["canonical"] - 9.3603e-11) < 1e-20 and abs(A0X["alt"] - 1.1312e-10) < 1e-20
R42 = J("CFG42_satellites_rule_results.json")["numbers"]; R45 = J("CFG45_rule_readings_results.json")["numbers"]
ns874 = exec_prefix(os.path.join(LANES, "CFG874_isolated_dwarfs_pooled", "cfg874.py"), 'P("CFG874  all isolated', "cfg874")
J874 = J("CFG874_isolated_dwarfs_pooled", "cfg874_results.json")
ns880 = exec_prefix(os.path.join(LANES, "CFG880_clump_sigma_universality", "cfg880.py"), "# ---------------- hierarchical likelihood", "cfg880")
ns827 = exec_prefix(os.path.join(LANES, "CFG827_dwarf_age_sfh_ml", "cfg827.py"), 'P("CFG827 (= CFG824b)', "cfg827")
R27J = J("CFG827_dwarf_age_sfh_ml", "cfg827_results.json"); R27 = R27J["rows"]
R24 = J("CFG824_dwarf_age_fossil", "cfg824_results.json")["rows"]
R933 = J("CFG933_udg_sealed_test", "cfg933_results.json")
NAT = J("CFG654_independent_inputs", "cfg654_delta_ta_results_cmb.json")["native"]
TAB = J("CFG654_independent_inputs", "cfg654_delta_ta_cmb.json")
P(f"  inputs loaded ({time.time() - T0W:.1f} s, {rss_mb():.0f} MB)")

# =====================================================================================================================  native background (criteria 2.1, 2.2)
h, OM, OR, FBN = NAT["h"], NAT["Om"], NAT["Or"], NAT["fb"]; OL = 1.0 - OM - OR
GS, KB, MP, MSUN_C = 6.67430e-11, 1.380649e-23, 1.67262192e-27, 1.98892e30
MPC = 3.0856775814913673e22; KPC_M = MPC / 1e3; GYR = 3.15576e16
H0 = 100.0 * h * 1e3 / MPC; RHOC0 = 3 * H0 ** 2 / (8 * math.pi * GS)
LNA = np.linspace(math.log(1e-9), 0.0, 400001); _A = np.exp(LNA)
_IH = 1.0 / (H0 * np.sqrt(OM / _A ** 3 + OR / _A ** 4 + OL))
TT = (np.concatenate([[0.0], np.cumsum(0.5 * (_IH[1:] + _IH[:-1]) * np.diff(LNA))]) + _A[0] ** 2 / (2 * H0 * math.sqrt(OR))) / GYR
T0 = float(TT[-1]); del _A, _IH


def t_of_z(z):
    return float(np.interp(-math.log1p(z), LNA, TT))


def z_of_t(t):
    return math.exp(-float(np.interp(t, TT, LNA))) - 1.0


ZT, DT = np.array(TAB["z"], float), np.array(TAB["D"], float); LZT = np.log1p(ZT)


def delta_ta(z):
    return float(np.interp(math.log1p(z), LZT, DT))


def delta_vir(zc, eds=False):
    if eds:
        return 18 * math.pi ** 2
    zta = z_of_t(t_of_z(zc) / 2.0)
    return 8.0 * delta_ta(zta) * ((1 + zta) / (1 + zc)) ** 3


def rhom(z):
    return OM * RHOC0 * (1 + z) ** 3


def m_nfw(t):
    return (t * t / 2 - 2 * t ** 3 / 3 + 3 * t ** 4 / 4 - 4 * t ** 5 / 5) if t < 1e-3 else (math.log1p(t) - t / (1 + t))


def mcool(z, mu, T, eds=False):
    D = delta_vir(z, eds); V2 = 2 * KB * T / (mu * MP)
    M = (V2 / GS) ** 1.5 * (4 * math.pi / 3 * D * rhom(z)) ** -0.5
    r = (3 * M / (4 * math.pi * D * rhom(z))) ** (1 / 3)
    return M / MSUN_C, r / KPC_M, D


def conc(D, C, zf, zcoll):
    target = C * ((1 + zcoll) / (1 + zf)) ** 3
    return brentq(lambda c: D / 3 * c ** 3 / m_nfw(c) - target, 1e-3, 1e4, xtol=1e-14, rtol=1e-15)


class Halo:
    """the floor halo: total mass M_cool(z_f) [Msun] inside r_vir [kpc], NFW with rho_s = C rho_m(z_coll), truncated at r_vir."""
    def __init__(s, zf, mu, C, T, eds=False, zcoll=None):
        s.zf, s.mu, s.C = zf, mu, C; s.M, s.rv, s.D = mcool(zf, mu, T, eds); s.zcoll = zf if zcoll is None else zcoll
        s.c = conc(s.D, C, zf, s.zcoll); s.mc = m_nfw(s.c)

    def enc(s, r_kpc):
        return s.M * m_nfw(s.c * min(r_kpc / s.rv, 1.0)) / s.mc


_HC = {}


def get_halo(zf, mu, C, T, eds=False, zcoll=None):
    k = (zf, mu, C, T, eds, zcoll)
    if k not in _HC:
        _HC[k] = Halo(zf, mu, C, T, eds, zcoll)
    return _HC[k]


Z_ONSET = z_of_t(T0 - 13.3)
P(f"  native background: h {h:.5f}, Omega_m {OM:.5f}, Omega_r {OR:.3e}, f_b {FBN:.5f}; age t0 {T0:.4f} Gyr; onset 13.3 Gyr -> z {Z_ONSET:.3f}")

# =====================================================================================================================  formation epochs (criteria 2.4)
WZ = os.path.join(REPO, "real_research", "data", "dsph", "weisz2014_dl")


def read_tsv(fn):
    L = [l.rstrip("\n") for l in _real_open(fn) if not l.startswith("#") and l.strip()]
    hdr = L[0].split("\t"); rows = []
    for l in L[3:]:
        v = l.split("\t")
        if len(v) == len(hdr):
            rows.append(dict(zip(hdr, [x.strip() for x in v])))
    return rows


def fnum(x):
    try:
        v = float(x); return None if math.isnan(v) else v
    except (TypeError, ValueError):
        return None


def taus(r):                                                         # CFG824's rule, re-implemented (checked in K3)
    fk = {float(k[1:]): fnum(v) for k, v in r.items() if k.startswith("f") and k[1:].replace(".", "").isdigit() and fnum(v) is not None}
    grid = sorted(fk, reverse=True); f = np.array([fk[g] for g in grid]); out = {}
    for X in (0.5, 0.9):
        if f[0] >= X:
            out[X] = 10 ** grid[0] / 1e9; continue
        i = int(np.argmax(f >= X)); lt = grid[i - 1] + (X - f[i - 1]) * (grid[i] - grid[i - 1]) / (f[i] - f[i - 1])
        out[X] = 10 ** lt / 1e9
    return out[0.5], out[0.9]


NAMEMAP = {"Canes Venetici I": "Canes Venatici I", "Canes Venetici II": "Canes Venatici II", "DDO 210": "Aquarius",
           "Pegasus": "Pegasus dIrr", "Sag DIG": "Sagittarius dIrr", "M32": "M 32", "Sex A": "Sextans A", "Sex B": "Sextans B"}
T6 = {r["ID"]: r for r in read_tsv(os.path.join(WZ, "table6.tsv"))}
WZT = {}
for r in read_tsv(os.path.join(WZ, "table5.tsv")):
    nm = r["ID"]; key = NAMEMAP.get(nm, nm)
    if key in WZT:
        continue
    WZT[key] = taus(T6.get(nm, r))
LVD = ns880["LVD"]
SATH = ("mw", "lmc", "m_031")
GRP_MEM = {}
for nm, (t50, t90) in WZT.items():
    L = LVD.get(nm)
    if L is None or fnum(L.get("M_V")) is None:
        continue
    g = ("sat" if (L.get("host") or "field") in SATH else "field", "faint" if fnum(L["M_V"]) > -7.7 else "bright")
    GRP_MEM.setdefault(g, []).append((nm, t50, t90))
LUM_MEM = {lc: [m for g, ms in GRP_MEM.items() if g[1] == lc for m in ms] for lc in ("faint", "bright")}
LDEF = {lc: (float(np.median([m[1] for m in ms])), float(np.median([m[2] for m in ms])), f"lum-{lc} median N{len(ms)}") for lc, ms in LUM_MEM.items()}
GDEF = {}
for g in [(a, b) for a in ("sat", "field") for b in ("faint", "bright")]:
    ms = GRP_MEM.get(g, [])
    GDEF[g] = ((float(np.median([m[1] for m in ms])), float(np.median([m[2] for m in ms])), f"{g[0]}-{g[1]} median N{len(ms)}")
               if len(ms) >= 3 else LDEF[g[1]][:2] + (f"{g[0]}-{g[1]} N{len(ms)} < 3 -> {LDEF[g[1]][2]}",))


def norm(nm):
    return "Andromeda " + nm[4:] if nm.startswith("And ") else nm


def tau_of(nm, MV, grp, deflt="group"):
    nm = norm(nm)
    if nm in WZT:
        return WZT[nm][0], WZT[nm][1], "Weisz+14"
    lc = "faint" if MV > -7.7 else "bright"
    d = GDEF[(grp, lc)] if deflt == "group" else LDEF[lc]
    return d[0], d[1], d[2]


def zf_of_tau(tau):
    return 0.0 if tau <= 0 else z_of_t(T0 - tau)


def grp_of_host(host):
    return "sat" if (host or "field") in SATH else "field"


# =====================================================================================================================  estimators (criteria 3)
_EP = {}


def ephan(Mb, foot):
    k = (float(Mb), foot)
    if k not in _EP:
        _EP[k] = float(EDGE(Mb, foot, 0.40))
    return _EP[k]


def sat_sig(d, foot, a0, reading, halo, fb, ups=None, gas=False):
    """CFG42 / CFG45 satellite estimator with a reading switch; halo(d) -> (M_c [Msun], enclosed(r_kpc) [Msun])."""
    ups = UPS_V if ups is None else ups
    Ms = ups * d["LV"]
    Mb = Ms + (max(1.33 * d["MHI"], infall_gas(d)) if gas else 1.33 * d["MHI"])
    rh_pc = (4.0 / 3.0) * d["rh"]; rh = rh_pc * 3.0857e16
    gN = GSAT * 0.5 * Mb * MSAT / rh ** 2
    g = a_int(gN, 0.0, a0); fex = 0.0
    if reading != "L":
        Mc, enc = halo(d)
        Me = float(enc(rh_pc / 1000.0))
        if reading == "S":
            fex = max(0.0, 1.0 - ephan(Mb, foot) / ((1 - fb) * Mc))
            g += GSAT * fex * (1 - fb) * Me * MSAT / rh ** 2
        else:
            g += max(0.0, (1 - fb) * GSAT * Me * MSAT / rh ** 2 - (g - gN))
    return math.sqrt(g * rh / 3.0) / 1e3, fex


def km_median(x, xu):                                                 # CFG42's, verbatim
    y = np.concatenate([-x, -xu]); ev = np.concatenate([np.ones(len(x), bool), np.zeros(len(xu), bool)])
    o = np.lexsort((~ev, y)); y, ev = y[o], ev[o]
    S, n, i = 1.0, len(y), 0
    while i < len(y):
        t = y[i]; j = i; d_ = 0; c_ = 0
        while j < len(y) and y[j] == t:
            d_ += int(ev[j]); c_ += int(not ev[j]); j += 1
        if d_:
            S *= 1.0 - d_ / n
            if S <= 0.5:
                return -t
        n -= d_ + c_; i = j
    return -y[-1]


def boot(x, xu, nb=1000, seed=42):                                    # CFG42's, verbatim
    rng = np.random.default_rng(seed); v = []
    for _ in range(nb):
        v.append(km_median(x[rng.integers(0, len(x), len(x))], xu[rng.integers(0, len(xu), len(xu))]))
    return float(np.std(v))


def halo_K(floor_mh=None):                                            # CFG42's own inputs (K1 only)
    def f(d):
        Mh = float(halo_mass(UPS_V * d["LV"]))
        if floor_mh is not None and UPS_V * d["LV"] < 1e5:
            Mh = floor_mh
        return Mh, (lambda r, Mh=Mh: float(nfw_DM(Mh, r)))
    return f


FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)


def ufd_pass(foot, a0, reading, halo, fb, ups=None):
    x = np.array([math.log10(d["sig"] / sat_sig(d, foot, a0, reading, halo, fb, ups=ups)[0]) for d in SAMPLES["ufd"]])
    xu = np.array([math.log10(d["sig_ul"] / sat_sig(d, foot, a0, reading, halo, fb, ups=ups)[0]) for d in UL])
    return km_median(x, xu), x, xu


def U_stat(foot, a0, reading, halo, fb, floors=False):
    m, x, xu = ufd_pass(foot, a0, reading, halo, fb)
    err = boot(x, xu)
    uv = [ufd_pass(foot, a0, reading, halo, fb, ups=u)[0] for u in (1.0, 4.0)]; f_ups = 0.5 * abs(uv[1] - uv[0])
    flo = [ufd_pass(foot, a0, reading, halo_K(fm), fb)[0] for fm in FLOORS] if floors else [m]
    f_mh = 0.5 * (max(flo) - min(flo)); tot = math.sqrt(err ** 2 + f_ups ** 2 + f_mh ** 2)
    fx = [sat_sig(d, foot, a0, reading, halo, fb)[1] for d in SAMPLES["ufd"]] if reading == "S" else []
    return dict(km=m, resolved_median=float(np.median(x)), err=err, f_ups=f_ups, f_mh=f_mh, tot=tot, z=m / tot, floors=flo, stat=m,
                fex_median=(float(np.median(fx)) if fx else None), fex_gt0=(int(np.sum(np.array(fx) > 0)) if fx else None))


def CL_stat(key, foot, a0, reading, halo, fb, floors=False):
    def offs(ups=None, hl=halo):
        return np.array([math.log10(d["sig"] / sat_sig(d, foot, a0, reading, hl, fb, ups=ups, gas=True)[0]) for d in SAMPLES[key]])
    x = offs(); u = [offs(ups=v) for v in (1.0, 4.0)]
    f_ups = 0.5 * abs(float(np.median(u[1])) - float(np.median(u[0])))
    flo = [float(np.median(offs(hl=halo_K(fm)))) for fm in FLOORS] if floors else [float(np.median(x))]
    err = 1.2533 * float(np.std(x)) / math.sqrt(len(x)); tot = math.sqrt(err ** 2 + f_ups ** 2 + (0.5 * (max(flo) - min(flo))) ** 2)
    med = float(np.median(x))
    fx = [sat_sig(d, foot, a0, reading, halo, fb, gas=True)[1] for d in SAMPLES[key]] if reading == "S" else []
    return dict(med=med, tot=tot, z=med / tot, stat=med, err=err, f_ups=f_ups,
                fex_median=(float(np.median(fx)) if fx else None), fex_gt0=(int(np.sum(np.array(fx) > 0)) if fx else None))


SPM = g10["read_master"]()


def sparc_rows(foot, a0, reading, halo_fn, fb, nu_fn=None):
    """CFG42 H4 (S) / CFG45 P3 (M) form: d log v at R_HI for SPARC log M* < 10; halo_fn(Ms) -> (M_c, enclosed)."""
    nu_fn = nu_fn or (lambda y: float(C7.nu_mono(np.array([y]))[0]))
    rows = []
    for name, m in SPM.items():
        Ms = 0.61 * m["L36"] * 1e9; Mb = Ms + 1.33 * m["MHI"] * 1e9
        if Ms <= 0 or m["RHI"] <= 0 or not (math.log10(Ms) < 10.0):
            continue
        Mc, enc = halo_fn(Ms)
        r = m["RHI"]; gb = g10["G"] * Mb * g10["Msun"] / (r * g10["kpc"]) ** 2
        nu = nu_fn(gb / a0)
        fex = max(0.0, 1.0 - ephan(Mb, foot) / ((1 - fb) * Mc))
        if reading == "S":
            dv = 0.5 * math.log10(1 + fex * (1 - fb) * float(enc(r)) / (nu * Mb))
        else:
            gl = nu * gb; conv = g10["G"] * g10["Msun"] / (r * g10["kpc"]) ** 2
            ex = max(0.0, (1 - fb) * float(enc(r)) * conv - (gl - gb)); dv = 0.5 * math.log10(1 + ex / gl)
        rows.append((name, fex, dv, math.log10(Ms)))
    return rows


def S_stat(rows):
    dv = np.array([r[2] for r in rows]); fz = np.array([r[1] for r in rows])
    w = sorted(rows, key=lambda t: -t[2])[:3]
    return dict(n=len(rows), nfex=int((fz > 0).sum()), max=float(dv.max()), frac=float(np.mean(dv < 0.03)), stat=float(np.mean(dv < 0.03)),
                worst=[(a, round(b, 3), round(c, 4)) for a, b, c, _ in w])


# ---- class I: CFG874's isolated dwarfs (its own estimator; bootstrap replay)
G874, MS874, PC874, nu_e874 = ns874["G"], ns874["Msun"], ns874["PC"], ns874["nu_e"]
ROWS874 = ns874["build"]("canonical", gas="disc")
I874 = [r for r in ROWS874 if r["grp"] == "I" and r["dmin"] >= 300.0]
S874 = [r for r in ROWS874 if r["grp"] == "S"]
_lo, _hi = min(r["lg"] for r in I874) - 0.5, max(r["lg"] for r in I874) + 0.5
S874 = [r for r in S874 if _lo <= r["lg"] <= _hi]
_rng = np.random.default_rng(874); IDX874 = np.empty((4000, len(I874)), int)
for _b in range(4000):
    IDX874[_b] = _rng.integers(0, len(I874), len(I874)); _rng.integers(0, len(S874), len(S874))
MG874 = {r["name"]: ns874["gas_in"](r["lHI"], (4 / 3) * r["rh"], "disc") for r in I874}


def ups_for(nm, ups):
    if ups == "SFH":
        return R27[nm]["ups"] if nm in R27 else 2.0
    return ups


def I_D(foot, a0, reading, halo, fb, ups=2.0):
    D, fx = [], []
    for r in I874:
        U = ups_for(r["name"], ups)
        r12_pc = (4 / 3) * r["rh"]; r12 = r12_pc * PC874
        Ms = U * 10 ** (0.4 * (4.83 - r["MV"])); Mg = MG874[r["name"]]
        gb = G874 * (Ms / 2 + Mg) * MS874 / r12 ** 2; gl = gb * nu_e874(gb / a0); g = gl; fex = 0.0
        if reading != "L":
            Mc, enc = halo(r)
            Me = float(enc(r12_pc / 1000.0))
            if reading == "S":
                Mb_e = Ms + (1.33 * 10 ** r["lHI"] if r["lHI"] is not None else 0.0)
                fex = max(0.0, 1.0 - ephan(Mb_e, foot) / ((1 - fb) * Mc)); g = gl + G874 * fex * (1 - fb) * Me * MS874 / r12 ** 2
            else:
                g = gl + max(0.0, (1 - fb) * G874 * Me * MS874 / r12 ** 2 - (gl - gb))
        D.append(math.log10(3 * (r["s"] * 1e3) ** 2 / r12 / g)); fx.append(fex)
    return np.array(D), np.array(fx)


def I_stat(foot, a0, reading, halo, fb, ups=2.0):
    D, fx = I_D(foot, a0, reading, halo, fb, ups)
    E = float(np.mean(D)); se = float(np.std(D[IDX874].mean(axis=1)))
    return dict(stat=E, err=se, z=E / se, N=len(D), fex_gt0=int((fx > 0).sum()), per={r["name"]: float(x) for r, x in zip(I874, D)})


# ---- class L: CFG880's 83 LVD dwarfs (its own estimator)
SAMP880 = ns880["SAMP"]; G880, MS880, PC880, nu880 = ns880["G"], ns880["Msun"], ns880["PC"], ns880["nu"]
PRE880 = {}
for _d in SAMP880:
    _L = LVD[_d["name"]]; _rh = fnum(_L.get("rhalf_sph_physical")) or fnum(_L.get("rhalf_physical")); _r12 = (4 / 3) * _rh
    _lHI = fnum(_L.get("mass_HI"))
    PRE880[_d["name"]] = dict(r12=_r12, MV=fnum(_L["M_V"]), lHI=_lHI, Mg=ns880["gas_in"](_lHI, _r12))


def L_parts(foot, a0, reading, halo, fb, ups=2.0, extra2=None):
    E, eps, fx, boost, sl = [], [], [], [], []
    for d in SAMP880:
        q = PRE880[d["name"]]; U = ups_for(d["name"], ups)
        r12_pc = q["r12"]; r12 = r12_pc * PC880; Ms = U * 10 ** (0.4 * (4.83 - q["MV"]))
        gN = G880 * (Ms / 2 + q["Mg"]) * MS880 / r12 ** 2
        sN2 = gN * r12 / 3 / 1e6; sl2 = float(gN * nu880(gN / a0)) * r12 / 3 / 1e6
        s2 = sl2; fex = 0.0
        if extra2 is not None:
            s2 = sl2 + extra2(d, r12_pc)
        elif reading != "L":
            Mc, enc = halo(d)
            add = G880 * (1 - fb) * float(enc(r12_pc / 1000.0)) * MS880 / (3 * r12) / 1e6
            if reading == "S":
                Mb_e = Ms + (1.33 * 10 ** q["lHI"] if q["lHI"] is not None else 0.0)
                fex = max(0.0, 1.0 - ephan(Mb_e, foot) / ((1 - fb) * Mc)); s2 = sl2 + fex * add
            else:
                s2 = sN2 + max(sl2 - sN2, add)
        E.append(math.log(d["s"] / math.sqrt(s2))); eps.append(0.5 * (d["em"] + d["ep"]) / d["s"]); fx.append(fex)
        boost.append(0.5 * math.log(s2 / sl2)); sl.append(math.sqrt(sl2))
    return np.array(E), np.array(eps), np.array(fx), np.array(boost), np.array(sl)


def L_stat(foot, a0, reading, halo, fb, ups=2.0):
    E, eps, fx, boost, _ = L_parts(foot, a0, reading, halo, fb, ups)
    se = max(float(np.std(E, ddof=1)) / math.sqrt(len(E)), float(math.sqrt(np.sum(eps ** 2))) / len(E))
    m = float(np.mean(E))
    return dict(stat=m, err=se, z=m / se, N=len(E), fex_gt0=int((fx > 0).sum()), median=float(np.median(E)))


# =====================================================================================================================  H-CF halo factories
CK = [(mu, tk, C) for mu in (0.59, 1.22) for tk in ("t50", "t90") for C in (1500, 3000, 6000)]
ckey = lambda c: f"mu{c[0]}|{c[1]}|C{c[2]}"
TV = 1.0e4 * TFAC


def hcf(mu, tk, C, eds=False, onset=False, deflt="group", T=None):
    T = TV if T is None else T

    def for_obj(nm, MV, grp):
        t50, t90, _ = tau_of(nm, MV, grp, deflt)
        zf = zf_of_tau(t50 if tk == "t50" else t90)
        H = get_halo(zf, mu, C, T, eds, Z_ONSET if onset else None)
        return H.M, H.enc

    def zero(_Ms):
        H = get_halo(0.0, mu, C, T, eds, Z_ONSET if onset else None)
        return H.M, H.enc
    return dict(sat=lambda d: for_obj(d["name"], d["MV"], "sat"),
                iso=lambda r: for_obj(r["name"], r["MV"], grp_of_host(r.get("host"))),
                lvd=lambda d: for_obj(d["name"], d["MV"], grp_of_host(d.get("host"))),
                sparc=zero)


SEV = {"CONSISTENT": 0, "TENSION": 1, "CONTRADICTED": 2}


def lab(z):
    return "CONSISTENT" if abs(z) < 2 else ("TENSION" if abs(z) < 3 else "CONTRADICTED")


def lab_S(frac):
    return "CONSISTENT" if frac >= 0.90 else ("TENSION" if frac >= 0.75 else "CONTRADICTED")


CLASSES = ("U", "C", "M", "I", "S", "L")


def all_classes(foot, reading, H, ups_IL=2.0, skip_sat=None):
    a0 = A0X[foot]; fb = FBN; out = {}
    if skip_sat is None:
        out["U"] = U_stat(foot, a0, reading, H["sat"], fb)
        out["C"] = CL_stat("cls", foot, a0, reading, H["sat"], fb)
        mc = CL_stat("col", foot, a0, reading, H["sat"], fb); ml = CL_stat("m31", foot, a0, reading, H["sat"], fb)
        worse = mc if (SEV[lab(mc["z"])], abs(mc["z"])) >= (SEV[lab(ml["z"])], abs(ml["z"])) else ml
        out["M"] = dict(worse, which=("Collins+13" if worse is mc else "M31 LVD"), collins=mc, lvd=ml)
        out["S"] = S_stat(sparc_rows(foot, a0, reading, H["sparc"], fb))
    else:
        out.update({k: skip_sat[k] for k in ("U", "C", "M", "S")})
    out["I"] = I_stat(foot, a0, reading, H["iso"], fb, ups_IL)
    out["L"] = L_stat(foot, a0, reading, H["lvd"], fb, ups_IL)
    for k in CLASSES:
        out[k]["label"] = lab_S(out[k]["frac"]) if k == "S" else lab(out[k]["z"])
    return out


def verdict(grid):
    """grid[foot][corner] = {class: result}; criteria section 4."""
    labs = {f: {ck: {c: grid[f][ck][c]["label"] for c in CLASSES} for ck in grid[f]} for f in grid}
    if all(l == "CONSISTENT" for f in labs for ck in labs[f] for l in labs[f][ck].values()):
        return "SURVIVES", labs
    if any(all(labs[f][ck][c] == "CONTRADICTED" for ck in labs[f]) for f in labs for c in CLASSES):
        return "FAILS", labs
    cks = list(next(iter(labs.values())).keys())
    sel = any(all(labs[f][ck][c] == "CONSISTENT" for f in labs for c in CLASSES) for ck in cks)
    return ("PARTIAL (corner-selectable)" if sel else "PARTIAL"), labs


def fmt_cls(res):
    s = []
    for c in CLASSES:
        r = res[c]
        if c == "S":
            s.append(f"S {r['frac']:.2f} ({r['nfex']} f_ex>0, max {r['max']:+.3f}) {r['label'][:4]}")
        else:
            s.append(f"{c} {r['stat']:+.3f} ({r['z']:+.2f}) {r['label'][:4]}")
    return " | ".join(s)


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return str(o)
    return o


RES = dict(lane="CFG934", criteria="9782c3df7", mode=MODE, T_vir=TV,
           native=dict(h=h, Om=OM, Or=OR, OL=OL, fb=FBN, t0_Gyr=T0, z_onset=Z_ONSET),
           tau_groups={f"{a}-{b}": dict(members=GRP_MEM.get((a, b), []), default=GDEF[(a, b)]) for (a, b) in GDEF},
           tau_lum=LDEF)


def finish(code):
    RES["checks"] = CHECKS; RES["runtime_s"] = time.time() - T0W; RES["peak_rss_mb"] = rss_mb(); RES["exit_code"] = code
    P(f"\n  runtime {RES['runtime_s']:.0f} s, peak RSS {RES['peak_rss_mb']:.0f} MB, exit {code}")
    json.dump(jclean(RES), _real_open(os.path.join(HERE, f"cfg934_results{SUF}.json"), "w"), indent=1)
    _real_open(os.path.join(HERE, f"cfg934{SUF}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(code)


# =====================================================================================================================  K
if MODE == "K":
    P("\n" + "=" * 118 + "\nK TESTS (criteria section 5)\n" + "=" * 118)
    KOK = []
    # ---- K1: CFG42 through this lane's generic estimator with CFG42's own inputs and constants
    dmax = 0.0; nk = 0; t1 = time.time()
    for foot in FOOTS:
        a0 = A0H[foot]
        for rule in (False, True):
            u = U_stat(foot, a0, "S" if rule else "L", halo_K(), FB42, floors=rule)
            ref = R42["UF"][f"{foot}|{'rule' if rule else 'law'}"]
            for k in ("km", "err", "f_ups", "f_mh", "tot", "z"):
                dmax = max(dmax, abs(u[k] - ref[k])); nk += 1
            for key in ("cls", "col", "m31"):
                c = CL_stat(key, foot, a0, "S" if rule else "L", halo_K(), FB42, floors=rule)
                ref = R42["CL"][f"{key}|{foot}|{'rule' if rule else 'law'}"]
                for k in ("med", "tot", "z"):
                    dmax = max(dmax, abs(c[k] - ref[k])); nk += 1
    h4 = S_stat(sparc_rows("canonical", A0H["canonical"], "S", lambda Ms: (float(halo_mass(Ms)), lambda r, M=float(halo_mass(Ms)): float(nfw_DM(M, r))), FB42))
    h4d = max(abs(h4["n"] - R42["H4"]["n"]), abs(h4["nfex"] - R42["H4"]["nfex"]), abs(h4["frac"] - R42["H4"]["frac"]), abs(h4["max"] - R42["H4"]["max"]))
    KOK.append(check("K1 CFG42 H1/H2/H4 reproduced through this lane's generic estimator with CFG42's inputs (Moster, Dutton-Maccio, FB, floors, hunt_lib a0)",
                     dmax <= 1e-9 and h4d <= 1e-9, f"{nk} UF/CL numbers, max |d| {dmax:.1e}; H4 n {h4['n']} nfex {h4['nfex']} frac {h4['frac']:.3f} max {h4['max']:.3f} (|d| {h4d:.1e}) [{time.time() - t1:.0f} s]"))
    # ---- K1b: CFG45's (M) reading
    dmax = 0.0; nk = 0
    for foot in FOOTS:
        a0 = A0H[foot]
        u = U_stat(foot, a0, "M", halo_K(), FB42, floors=True); ref = R45["UF"][f"{foot}|M"]
        for k in ("km", "z"):
            dmax = max(dmax, abs(u[k] - ref[k])); nk += 1
        for key in ("cls", "col", "m31"):
            c = CL_stat(key, foot, a0, "M", halo_K(), FB42, floors=True); ref = R45["CL"][f"{key}|{foot}|M"]
            for k in ("med", "z"):
                dmax = max(dmax, abs(c[k] - ref[k])); nk += 1
    sm = S_stat(sparc_rows("canonical", A0X["canonical"], "M", lambda Ms: (float(halo_mass(Ms)), lambda r, M=float(halo_mass(Ms)): float(nfw_DM(M, r))), FB42))
    refm = R45["SPARC"]["dwarf|M"]; smd = max(abs(sm["frac"] - refm["frac_lt003"]), abs(sm["max"] - refm["max"]))
    KOK.append(check("K1b CFG45 (M) reading reproduced (UF km/z, CL med/z, SPARC dwarf|M frac/max)", dmax <= 1e-6 and smd <= 1e-6,
                     f"{nk} UF/CL numbers max |d| {dmax:.1e}; SPARC M frac {sm['frac']:.4f} max {sm['max']:.4f} (|d| {smd:.1e})"))
    # ---- K2: M_cool analytic, V_c identity, NFW quadrature, c solve
    Mme, rme, Dme = mcool(9.0, 0.6, 1.98e4, eds=True)
    Omz = OM * 10 ** 3 / (OM * 10 ** 3 + OR * 10 ** 4 + OL); Dc = 18 * math.pi ** 2 * Omz
    Mbl = 1e8 / h * ((OM / Omz) * Dc / (18 * math.pi ** 2)) ** -0.5
    k2a = abs(Mme / Mbl - 1)
    vids = []
    for (z, mu) in ((0.0, 0.59), (5.0, 1.22), (9.0, 0.59)):
        M_, r_, _ = mcool(z, mu, 1e4)
        vids.append(abs(math.sqrt(GS * M_ * MSUN_C / (r_ * KPC_M)) / math.sqrt(2 * KB * 1e4 / (mu * MP)) - 1))
    Hh = Halo(5.3, 1.22, 3000, 1e4); rs = Hh.rv / Hh.c; rho_s = Hh.M / (4 * math.pi * rs ** 3 * Hh.mc)
    qd = max(abs(quad(lambda r: 4 * math.pi * r * r * rho_s / ((r / rs) * (1 + r / rs) ** 2), 0, R, epsabs=0, epsrel=1e-12, limit=200)[0] / Hh.enc(R) - 1)
             for R in (0.01, 0.05, 0.2, 0.5 * Hh.rv, Hh.rv))
    cres = max(abs(H_.D / 3 * H_.c ** 3 / m_nfw(H_.c) / (H_.C * ((1 + H_.zcoll) / (1 + H_.zf)) ** 3) - 1)
               for H_ in (Hh, Halo(0.0, 0.59, 1500, 1e4), Halo(3.0, 0.59, 6000, 1e4, zcoll=Z_ONSET)))
    KOK.append(check("K2 M_cool vs BL01 eq. 26 (z 9, Delta 18 pi^2, mu 0.6, T 1.98e4 K) within 2%; V_c identity 1e-10; NFW vs quadrature 1e-6; c solve 1e-10",
                     k2a <= 0.02 and max(vids) <= 1e-10 and qd <= 1e-6 and cres <= 1e-10,
                     f"M_cool {Mme:.4e} vs BL01 {Mbl:.4e} (rel {k2a:.2e}); V_c max rel {max(vids):.1e}; NFW quad max rel {qd:.1e}; c residual {cres:.1e}"))
    # ---- K3: CFG827 dwarf excess and CFG824 taus
    law827, A827, wt827 = ns827["law"], ns827["A0"], ns827["wt"]
    rows827 = ns827["rows"]; dE = 0.0
    for r in rows827:
        E = math.log(r["so"] / law827(r["MV"], r["rhl"], A827["canonical"], R27[r["name"]]["ups"]))
        dE = max(dE, abs(E - R27[r["name"]]["E_SFH"]))
    OOS = [r for r in rows827 if not r["train"]]; w = wt827(OOS); E0 = np.array([R27[r["name"]]["E_SFH"] for r in OOS])
    flat = float(np.sum(w * E0) / np.sum(w)); dflat = abs(flat - R27J["ufd"]["flat"])
    dtau = 0.0; ntau = 0
    for nm, r in R24.items():
        if nm in WZT:
            dtau = max(dtau, abs(WZT[nm][0] - r["tau50"]), abs(WZT[nm][1] - r["tau90"])); ntau += 1
    KOK.append(check("K3 CFG827 E_SFH rows + OOS weighted flat mean reproduced (1e-9); this lane's tau50/tau90 = CFG824's (1e-12)",
                     dE <= 1e-9 and dflat <= 1e-9 and dtau <= 1e-12 and ntau == len(R24),
                     f"{len(rows827)} rows max |dE| {dE:.1e}; flat {flat:+.6f} (|d| {dflat:.1e}); OOS N {len(OOS)} unweighted mean E {E0.mean():+.4f} "
                     f"({int((E0 > 0).sum())}/{len(E0)} above the law); taus {ntau}/{len(R24)} max |d| {dtau:.1e}"))
    # ---- K4: CFG874
    dd = 0.0; txt = []
    for foot in FOOTS:
        st = I_stat(foot, A0X[foot], "L", None, FBN); ref = J874[foot]["primary"]
        dd = max(dd, abs(st["stat"] - ref["E"]), abs(st["err"] - ref["se_E"])); txt.append(f"{foot}: E {st['stat']:+.4f} +- {st['err']:.4f}")
    KOK.append(check("K4 CFG874 primary isolated E and se_E reproduced by this lane's replay (1e-12), both footings", dd <= 1e-12 and len(I874) == 11,
                     f"N_I {len(I874)}, N_S {len(S874)}; " + "; ".join(txt) + f"; max |d| {dd:.1e}"))
    # ---- K5: CFG880 sample
    from collections import Counter
    hc = dict(Counter(d["host"] for d in SAMP880)); want = {"mw": 37, "m_031": 31, "field": 7, "lmc": 6, "m_033": 1, "ngc_3109": 1}
    dl = 0.0
    for foot in FOOTS:
        for d in SAMP880:
            sl2, r12 = ns880["law2"](d["name"], A0X[foot], 2.0, True)
            q = PRE880[d["name"]]; Ms = 2.0 * 10 ** (0.4 * (4.83 - q["MV"])); gN = G880 * (Ms / 2 + q["Mg"]) * MS880 / (q["r12"] * PC880) ** 2
            dl = max(dl, abs(float(gN * nu880(gN / A0X[foot])) * q["r12"] * PC880 / 3 / 1e6 / sl2 - 1), abs(r12 / q["r12"] - 1))
    KOK.append(check("K5 CFG880 sample N 83 with the declared host counts (and this lane's sigma_law equals CFG880's law2, extra)",
                     len(SAMP880) == 83 and hc == want and dl <= 1e-12, f"N {len(SAMP880)}; hosts {hc}; sigma_law^2 max rel {dl:.1e}"))
    # ---- K6: native background
    dnode = max(abs(delta_ta(z) - d) for z, d in zip(ZT, DT)); dv30 = delta_vir(30.0) / (18 * math.pi ** 2) - 1
    t0q = quad(lambda a: 1.0 / (a * H0 * math.sqrt(OM / a ** 3 + OR / a ** 4 + OL)), 0, 1, epsabs=0, epsrel=1e-12, limit=400)[0] / GYR
    KOK.append(check("K6 Delta_ta table nodes exact; Delta_vir(z = 30) within 3% of 18 pi^2 (extra: t0 vs quadrature)",
                     dnode == 0.0 and abs(dv30) <= 0.03, f"node max |d| {dnode:.1e}; Delta_vir(30)/18pi^2 - 1 = {dv30:+.4f}; t0 table {T0:.6f} vs quad {t0q:.6f} Gyr"))
    RES["K_all"] = all(KOK)
    P(f"\n  K-stage {'ALL PASS' if RES['K_all'] else 'FAILED'}")
    finish(0 if RES["K_all"] else 2)

# =====================================================================================================================  MUTATE / main need K
KJ = os.path.join(HERE, "cfg934_results_K.json")
if not (os.path.exists(KJ) and json.load(_real_open(KJ)).get("K_all") is True):
    P("  K has not passed (cfg934_results_K.json): per criteria section 5 the lane stops; no class is reported."); RES["class"] = None; finish(2)

# ---- the floor masses used (table)
P("\n" + "=" * 118 + "\nM_cool(z): floor halo mass at T_vir " + f"{TV:g} K (native Delta_vir), r_vir, concentration for C 1500/3000/6000\n" + "=" * 118)
MTAB = []
for z in (0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 9.0):
    for mu in (0.59, 1.22):
        Hs = [get_halo(z, mu, C, TV) for C in (1500, 3000, 6000)]
        MTAB.append(dict(z=z, mu=mu, M=Hs[0].M, rvir_kpc=Hs[0].rv, Dvir=Hs[0].D, c=[H_.c for H_ in Hs]))
        P(f"  z {z:4.1f} mu {mu:4.2f}: M_cool {Hs[0].M:9.3e} Msun  r_vir {Hs[0].rv:7.3f} kpc  Delta_vir {Hs[0].D:6.1f}  c {Hs[0].c:.2f}/{Hs[1].c:.2f}/{Hs[2].c:.2f}")
RES["mcool_table"] = MTAB
VV = {mu: math.sqrt(2 * KB * TV / (mu * MP)) / 1e3 for mu in (0.59, 1.22)}
P(f"  V_vir (fixed by T and mu): mu 0.59 {VV[0.59]:.2f} km/s, mu 1.22 {VV[1.22]:.2f} km/s")
P("\n  formation-epoch defaults (criteria 2.4): " + "; ".join(f"{a}-{b}: tau50 {v[0]:.2f} tau90 {v[1]:.2f} Gyr ({v[2]})" for (a, b), v in GDEF.items()))
for (a, b), ms in sorted(GRP_MEM.items()):
    P(f"     {a}-{b} Weisz members: " + ", ".join(f"{m[0]} ({m[1]:.2f}/{m[2]:.2f})" for m in ms))
ZF = {}
for key, src, grp in (("ufd", SAMPLES["ufd"], "sat"), ("UL", UL, "sat"), ("cls", SAMPLES["cls"], "sat"), ("col", SAMPLES["col"], "sat"),
                      ("m31", SAMPLES["m31"], "sat")):
    for d in src:
        t50, t90, s_ = tau_of(d["name"], d["MV"], grp); ZF[f"{key}:{d['name']}"] = dict(t50=t50, t90=t90, z50=zf_of_tau(t50), z90=zf_of_tau(t90), src=s_)
for r in I874:
    g = grp_of_host(r.get("host")); t50, t90, s_ = tau_of(r["name"], r["MV"], g)
    ZF[f"I:{r['name']}"] = dict(t50=t50, t90=t90, z50=zf_of_tau(t50), z90=zf_of_tau(t90), src=s_, grp=g)
for d in SAMP880:
    g = grp_of_host(d.get("host")); t50, t90, s_ = tau_of(d["name"], d["MV"], g)
    ZF[f"L:{d['name']}"] = dict(t50=t50, t90=t90, z50=zf_of_tau(t50), z90=zf_of_tau(t90), src=s_, grp=g)
RES["z_f"] = ZF
for cls_, pre in (("U", "ufd:"), ("C", "cls:"), ("M LVD", "m31:"), ("I", "I:"), ("L", "L:")):
    v = [x for k, x in ZF.items() if k.startswith(pre)]
    P(f"  z_f {cls_:6s}: tau50 -> z {np.median([x['z50'] for x in v]):.2f} (range {min(x['z50'] for x in v):.2f}-{max(x['z50'] for x in v):.2f}), "
      f"tau90 -> z {np.median([x['z90'] for x in v]):.2f} (range {min(x['z90'] for x in v):.2f}-{max(x['z90'] for x in v):.2f}); "
      f"own SFH {sum(1 for x in v if x['src'] == 'Weisz+14')}/{len(v)}")

# ---- bare law (reference) and the corner grid
P("\n" + "=" * 118 + "\nBARE LAW (reference; no debris)\n" + "=" * 118)
BARE = {}
NOH = dict(sat=None, iso=None, lvd=None, sparc=lambda Ms: (1.0, lambda r: 0.0))
for foot in FOOTS:
    BARE[foot] = all_classes(foot, "L", NOH)
    BARE[foot]["S"] = S_stat(sparc_rows(foot, A0X[foot], "S", lambda Ms: (1e-30, lambda r: 0.0), FBN))
    BARE[foot]["S"]["label"] = lab_S(BARE[foot]["S"]["frac"])
    P(f"  {foot:9s}: " + fmt_cls(BARE[foot]))
RES["bare_law"] = BARE

GRID = {}
for reading in ("S", "M"):
    P("\n" + "=" * 118 + f"\nH-CF, reading ({reading}) {'[PRIMARY]' if reading == 'S' else '[ALTERNATIVE]'}: 12 corners x 2 footings\n" + "=" * 118)
    GRID[reading] = {}
    for foot in FOOTS:
        GRID[reading][foot] = {}
        for c in CK:
            t1 = time.time()
            GRID[reading][foot][ckey(c)] = all_classes(foot, reading, hcf(*c))
            P(f"  {foot:9s} {ckey(c):18s}: " + fmt_cls(GRID[reading][foot][ckey(c)]) + f"  [{time.time() - t1:.1f} s, {rss_mb():.0f} MB]")
RES["corners"] = GRID

# =====================================================================================================================  MUTATE checks
if MODE.startswith("MUTATE"):
    P("\n" + "=" * 118 + f"\nMUTATE {MODE} (criteria section 5)\n" + "=" * 118)
    g = GRID["S"]; bad = []
    if MODE == "MUTATE_T100":
        for f in FOOTS:
            for ck, res in g[f].items():
                for c in ("U", "C", "I", "L"):
                    if not (res[c]["stat"] < 0 and res[c]["z"] <= -2):
                        bad.append(f"{f} {ck} {c} {res[c]['stat']:+.3f} ({res[c]['z']:+.2f})")
                for sub in ("collins", "lvd"):
                    if not (res["M"][sub]["stat"] < 0 and res["M"][sub]["z"] <= -2):
                        bad.append(f"{f} {ck} M-{sub} {res['M'][sub]['stat']:+.3f} ({res['M'][sub]['z']:+.2f})")
                if res["S"]["label"] == "CONSISTENT":
                    bad.append(f"{f} {ck} S frac {res['S']['frac']:.2f}")
        ok = check("MUTATE T100: T_vir x 100 over-predicts every class at every corner on both footings (U, C, M both, I, L: stat < 0 and z <= -2; S not CONSISTENT)",
                   not bad, f"{len(bad)} failing cells" + (": " + "; ".join(bad[:12]) if bad else ""))
    else:
        dmx = 0.0
        for f in FOOTS:
            for ck, res in g[f].items():
                for c in ("U", "C", "I", "L", "S"):
                    dmx = max(dmx, abs(res[c]["stat"] - BARE[f][c]["stat"]))
                for sub in ("collins", "lvd"):
                    dmx = max(dmx, abs(res["M"][sub]["stat"] - BARE[f]["M"][sub]["stat"]))
                if res["U"]["label"] != BARE[f]["U"]["label"]:
                    bad.append(f"{f} {ck} U {res['U']['label']}")
        ok = check("MUTATE T001: T_vir x 0.01 returns the bare law in every class (|d| <= 1e-3; U class unchanged), reading S",
                   dmx <= 1e-3 and not bad, f"max |stat - bare| {dmx:.2e}; U label mismatches {len(bad)}")
        dmm = max(abs(GRID['M'][f][ck][c]["stat"] - BARE[f][c]["stat"]) for f in FOOTS for ck in GRID["M"][f] for c in ("U", "C", "I", "L"))
        P(f"  (reported) reading M at T x 0.01: max |stat - bare| {dmm:.2e}")
    RES["mutate_ok"] = ok
    vS, _ = verdict(GRID["S"]); vM, _ = verdict(GRID["M"]); RES["verdict_S"] = vS; RES["verdict_M"] = vM
    P(f"\n  (MUTATE run, no verdict weight) H-CF verdict as computed: S {vS}; M {vM}")
    finish(0 if ok else 1)

# =====================================================================================================================  main: verdicts
P("\n" + "=" * 118 + "\nVERDICT (criteria section 4)\n" + "=" * 118)
vS, labS = verdict(GRID["S"]); vM, labM = verdict(GRID["M"])
for reading, labs_ in (("S", labS), ("M", labM)):
    for f in FOOTS:
        for c in CLASSES:
            cnt = {k: sum(1 for ck in labs_[f] if labs_[f][ck][c] == k) for k in SEV}
            P(f"  ({reading}) {f:9s} {c}: CONSISTENT {cnt['CONSISTENT']:2d} / TENSION {cnt['TENSION']:2d} / CONTRADICTED {cnt['CONTRADICTED']:2d} of 12")
P(f"\n  H-CF (S) [headline]: {vS}\n  H-CF (M) [alternative]: {vM}")
RES["verdict_S"], RES["verdict_M"] = vS, vM
RES["labels"] = dict(S=labS, M=labM)

# ---- variants (reading S)
P("\n" + "=" * 118 + "\nVARIANTS (reading S; a variant that changes the verdict marks it FRAGILE)\n" + "=" * 118)
VAR = {}


def run_var(name, Hfun, ups_IL=2.0, reuse_sat=False, err_floor=False):
    grid = {}
    for f in FOOTS:
        grid[f] = {}
        for c in CK:
            base = GRID["S"][f][ckey(c)]
            res = all_classes(f, "S", Hfun(c), ups_IL=ups_IL, skip_sat=(base if reuse_sat else None))
            grid[f][ckey(c)] = res
    v, _ = verdict(grid); VAR[name] = dict(verdict=v, grid=grid)
    P(f"  {name:34s}: {v}" + ("   <-- changes the verdict" if v != vS else ""))
    return grid


run_var("V1 Delta_vir = 18 pi^2", lambda c: hcf(*c, eds=True))
run_var("V2 onset z_coll (13.3 Gyr)", lambda c: hcf(*c, onset=True))
for U_ in (1.0, 4.0):
    run_var(f"V3 Upsilon_V {U_:g} for I and L", lambda c: hcf(*c), ups_IL=U_, reuse_sat=True)
# V4: uniform recipe (Upsilon x1/2..x2 floor added to I and L errors)
g4 = {}
for f in FOOTS:
    g4[f] = {}
    for c in CK:
        base = GRID["S"][f][ckey(c)]; lo_ = VAR["V3 Upsilon_V 1 for I and L"]["grid"][f][ckey(c)]; hi_ = VAR["V3 Upsilon_V 4 for I and L"]["grid"][f][ckey(c)]
        res = dict(base)
        for k in ("I", "L"):
            fl = 0.5 * abs(hi_[k]["stat"] - lo_[k]["stat"]); e = math.sqrt(base[k]["err"] ** 2 + fl ** 2)
            res[k] = dict(base[k], err=e, z=base[k]["stat"] / e, ups_floor=fl); res[k]["label"] = lab(res[k]["z"])
        g4[f][ckey(c)] = res
v4, _ = verdict(g4); VAR["V4 uniform recipe (Ups floor on I, L)"] = dict(verdict=v4, grid=g4)
P(f"  {'V4 uniform recipe (Ups floor on I, L)':34s}: {v4}" + ("   <-- changes the verdict" if v4 != vS else ""))
run_var("V5 Upsilon_SFH (CFG827) for I and L", lambda c: hcf(*c), ups_IL="SFH", reuse_sat=True)
run_var("V6 luminosity-class tau default", lambda c: hcf(*c, deflt="lum"))
FRAG = [k for k, v in VAR.items() if v["verdict"] != vS]
P(f"\n  FRAGILE: {'YES (' + ', '.join(FRAG) + ')' if FRAG else 'no (no variant changes the (S) verdict)'}")
RES["variants"] = {k: dict(verdict=v["verdict"], labels={f: {ck: {c: v["grid"][f][ck][c]["label"] for c in CLASSES} for ck in v["grid"][f]} for f in FOOTS},
                           stats={f: {ck: {c: (v["grid"][f][ck][c].get("stat"), v["grid"][f][ck][c].get("z")) for c in CLASSES if c != "S"} for ck in v["grid"][f]} for f in FOOTS})
                   for k, v in VAR.items()}
RES["fragile"] = FRAG

# =====================================================================================================================  ungraded reports
P("\n" + "=" * 118 + "\nUNGRADED REPORTS (criteria section 6)\n" + "=" * 118)
UNG = {}


def sint_ml(E, eps):
    S = np.concatenate([[0.0], np.geomspace(1e-3, 3.0, 600)]); ll = []
    for s in S:
        w = 1.0 / (eps ** 2 + s ** 2); m = np.sum(w * E) / np.sum(w); ll.append(-0.5 * np.sum(w * (E - m) ** 2) + 0.5 * np.sum(np.log(w)))
    ll = np.array(ll); k = int(np.argmax(ll)); d = 2 * (ll[k] - ll); ok = S[d <= 3.84]
    return dict(s_int=float(S[k]), lo95=float(ok.min()), hi95=float(ok.max()))


# D3: CFG880 scatter and where the floor puts the excess
D3 = {}
for f in FOOTS:
    a0 = A0X[f]
    Eb, epsb, _, _, slb = L_parts(f, a0, "L", None, FBN)
    SX = ns880["SREF"][f]
    Ec, _, _, _, _ = L_parts(f, a0, "L", None, FBN, extra2=lambda d, r12: float(ns880["clump2"](r12, SX, a0)))
    D3[f] = dict(bare=sint_ml(Eb, epsb), clump877=dict(sint_ml(Ec, epsb), sigma_x=SX, mean=float(np.mean(Ec))), hcf={})
    obs_ex = Eb                                                        # ln(sigma_obs / sigma_law)
    for reading in ("S", "M"):
        for c in CK:
            E, eps, fx, boost, _ = L_parts(f, a0, reading, hcf(*c)["lvd"], FBN)
            rho = spearmanr(boost, obs_ex).correlation if np.ptp(boost) > 0 else float("nan")
            D3[f]["hcf"][f"{reading}|{ckey(c)}"] = dict(sint_ml(E, eps), mean=float(np.mean(E)), rho_boost_vs_obs=float(rho),
                                                        n_boosted=int(np.sum(boost > 1e-6)), boost_median=float(np.median(boost)))
    hs = [v["s_int"] for k, v in D3[f]["hcf"].items() if k.startswith("S|")]; hm = [v["s_int"] for k, v in D3[f]["hcf"].items() if k.startswith("M|")]
    rs = [v["rho_boost_vs_obs"] for k, v in D3[f]["hcf"].items() if k.startswith("S|")]; rm = [v["rho_boost_vs_obs"] for k, v in D3[f]["hcf"].items() if k.startswith("M|")]
    P(f"  D3 [{f}] LVD-83 intrinsic scatter of ln(sigma_obs/sigma_pred) (ML, eps + s_int): bare law {D3[f]['bare']['s_int']:.3f} "
      f"(95% {D3[f]['bare']['lo95']:.3f}-{D3[f]['bare']['hi95']:.3f}); CFG877 universal clump sigma_x {SX:.2f}: {D3[f]['clump877']['s_int']:.3f} "
      f"(mean E {D3[f]['clump877']['mean']:+.3f}); H-CF (S) {min(hs):.3f}-{max(hs):.3f}, (M) {min(hm):.3f}-{max(hm):.3f} over 12 corners")
    P(f"       Spearman rho(H-CF predicted boost, observed excess): (S) {np.nanmin(rs):+.2f} to {np.nanmax(rs):+.2f}; (M) {np.nanmin(rm):+.2f} to {np.nanmax(rm):+.2f}; "
      f"dwarfs boosted (S) {min(v['n_boosted'] for k, v in D3[f]['hcf'].items() if k.startswith('S|'))}-{max(v['n_boosted'] for k, v in D3[f]['hcf'].items() if k.startswith('S|'))} of 83")
UNG["D3_scatter"] = D3

# D4: common scale (floor halo mass inside 300 pc over the 83; V_max)
D4 = {}
for c in CK:
    H = hcf(*c)["lvd"]; m3 = np.array([H(d)[1](0.3) for d in SAMP880]) * (1 - FBN)
    D4[ckey(c)] = dict(cold_M300_median=float(np.median(m3)), dex16=float(np.percentile(np.log10(m3), 16)), dex84=float(np.percentile(np.log10(m3), 84)))
vmax = {}
for mu in (0.59, 1.22):
    for C in (1500, 3000, 6000):
        Hh = get_halo(5.0, mu, C, TV); vmax[f"mu{mu}|C{C}"] = VV[mu] * math.sqrt(0.21626 * Hh.c / Hh.mc)
P("  D4 cold floor-halo mass inside 300 pc over the 83 (1-f_b) M_NFW(<0.3 kpc): " +
  "; ".join(f"{k} median {v['cold_M300_median']:.2e} (16-84% {10 ** v['dex16']:.1e}-{10 ** v['dex84']:.1e})" for k, v in list(D4.items())[::3]))
P("       floor-halo V_max (z_f 5): " + ", ".join(f"{k} {v:.1f} km/s" for k, v in vmax.items()) + f"; V_vir {VV[0.59]:.1f} / {VV[1.22]:.1f} km/s for every epoch")
UNG["D4_common_scale"] = dict(M300=D4, Vmax=vmax, Vvir=VV)

# D5: clusters
D5 = {}
for f in FOOTS:
    for Mb in (1e13, 1e14):
        ph = ephan(Mb, f)
        for mu in (0.59, 1.22):
            H = get_halo(0.0, mu, 3000, TV)
            mlaw = float(C7.M_law(Mb, 0.5, C7.A0[f], C7.nu_mono)) - Mb
            D5[f"{f}|Mb{Mb:.0e}|mu{mu}"] = dict(edge_phantom=ph, cold_floor=(1 - FBN) * H.M, fex=max(0.0, 1 - ph / ((1 - FBN) * H.M)),
                                                 phantom_500kpc=mlaw, floor_500kpc=(1 - FBN) * H.enc(500.0))
P("  D5 clusters: " + "; ".join(f"{k}: f_ex {v['fex']:.0f} (edge phantom {v['edge_phantom']:.1e} vs cold floor {v['cold_floor']:.1e}); (M) floor(<0.5 Mpc) "
                                  f"{v['floor_500kpc']:.1e} vs phantom {v['phantom_500kpc']:.1e}" for k, v in D5.items() if k.startswith("canonical")))
UNG["D5_clusters"] = D5

# D6 / D7: CFG933 galaxies (Coma UDGs; DF2/DF4) with the record's sigma_law
D67 = {}
for f in FOOTS:
    a0 = A0X[f]; pg = R933["byfoot"][f]["per_galaxy"]
    for zf in (0.0, 0.5, 1.0, 2.0, 3.0, 5.0):
        for mu in (0.59, 1.22):
            H = get_halo(zf, mu, 3000, TV); rec = {}
            for g in pg:
                r12_kpc = 4.0 / 3.0 * g["Re"]; r12 = r12_kpc * 3.0857e19; sl2 = g["sigma_law"] ** 2
                gN = 6.674e-11 * (g["Ms"] / 2) * 1.989e30 / r12 ** 2; sN2 = gN * r12 / 3 / 1e6
                add = 6.674e-11 * (1 - FBN) * H.enc(r12_kpc) * 1.989e30 / (3 * r12) / 1e6
                fex = max(0.0, 1 - ephan(g["Ms"], f) / ((1 - FBN) * H.M))
                eS = 0.5 * math.log((sl2 + fex * add) / sl2); eM = 0.5 * math.log((sN2 + max(sl2 - sN2, add)) / sl2)
                rec[g["name"]] = dict(pop=g["pop"], E_obs=g["E_obs"], E_pred_S=eS, E_pred_M=eM, fex=fex)
            coma = [v for v in rec.values() if v["pop"] == "Coma"]
            D67[f"{f}|zf{zf}|mu{mu}"] = dict(per=rec, coma_E_obs=float(np.mean([v["E_obs"] for v in coma])),
                                            coma_E_pred_S=float(np.mean([v["E_pred_S"] for v in coma])), coma_E_pred_M=float(np.mean([v["E_pred_M"] for v in coma])),
                                            coma_fex_gt0=int(sum(v["fex"] > 0 for v in coma)))
for f in FOOTS:
    rows_ = [(k, v) for k, v in D67.items() if k.startswith(f)]
    P(f"  D7 Coma UDGs [{f}] <E_obs> {rows_[0][1]['coma_E_obs']:+.3f} ln; H-CF <E_pred> (S) {min(v['coma_E_pred_S'] for _, v in rows_):+.3f} to "
      f"{max(v['coma_E_pred_S'] for _, v in rows_):+.3f} (f_ex > 0 in {max(v['coma_fex_gt0'] for _, v in rows_)}/9 at most), (M) {min(v['coma_E_pred_M'] for _, v in rows_):+.3f} to "
      f"{max(v['coma_E_pred_M'] for _, v in rows_):+.3f} over z_f 0-5, both mu, C 3000")
    dfs = rows_[0][1]["per"]
    P(f"  D6 DF2/DF4 [{f}] E_obs " + ", ".join(f"{n} {v['E_obs']:+.2f}" for n, v in dfs.items() if v["pop"] != "Coma") +
      "; H-CF (no primordial halo): E_pred = 0 exactly; with a floor halo (any z_f 0-5): (S) up to " +
      f"{max(v['per'][n]['E_pred_S'] for _, v in rows_ for n in v['per'] if v['per'][n]['pop'] != 'Coma'):+.3f}, (M) up to "
      f"{max(v['per'][n]['E_pred_M'] for _, v in rows_ for n in v['per'] if v['per'][n]['pop'] != 'Coma'):+.3f}")
UNG["D67_cfg933"] = D67
UNG["TDG_cfg931_info"] = "CFG931 INFO: Lelli+15 tidal dwarfs sit 0.69 dex BELOW the bare law; H-CF assigns no primordial halo, so it predicts exactly the bare law (no excess), not a deficit"
RES["ungraded"] = UNG

# ---- headline numbers for the README
P("\n" + "=" * 118 + "\nHEADLINE (reading S, both footings): class statistic range over the 12 corners\n" + "=" * 118)
HL = {}
for reading in ("S", "M"):
    for f in FOOTS:
        for c in CLASSES:
            vals = [GRID[reading][f][ck][c]["stat"] for ck in GRID[reading][f]]
            zs = [GRID[reading][f][ck][c].get("z", float("nan")) for ck in GRID[reading][f]]
            HL[f"{reading}|{f}|{c}"] = dict(min=float(min(vals)), max=float(max(vals)), zmin=float(np.nanmin(zs)) if c != "S" else None,
                                             zmax=float(np.nanmax(zs)) if c != "S" else None, bare=BARE[f][c]["stat"], bare_z=BARE[f][c].get("z"))
            if reading == "S":
                P(f"  {f:9s} {c}: bare {BARE[f][c]['stat']:+.3f}" + (f" ({BARE[f][c]['z']:+.2f})" if c != "S" else "") +
                  f"  ->  H-CF {min(vals):+.3f} to {max(vals):+.3f}" + (f" (z {np.nanmin(zs):+.2f} to {np.nanmax(zs):+.2f})" if c != "S" else ""))
RES["headline"] = HL
P(f"\n  H-CF (S) {vS}; H-CF (M) {vM}; FRAGILE {'YES' if FRAG else 'no'}.  kappa = 1/2 FITTED; footings never pooled; not theory closed.")
finish(0)
