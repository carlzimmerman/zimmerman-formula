#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG245 common helpers (phase 2 of the frozen criteria `CFG245_FROZEN_CRITERIA.md`).

Repository discovery (ZF_REPO or walk up from __file__), a Report class that never prints an absolute home path, constants,
the three declared relaxation rates, the committed passive-infall products of CFG244 (READ-ONLY JSON, no CFG118/CFG244 code is
imported or run), the committed per-cluster arrays of CFG4_clusters (read-only JSON), the relaxation model of Gate T, kernels.
The repository is READ, never written; every output goes to the lane directory (HERE).
kappa = 1/2 is FITTED; there is no dark-matter particle; the cold MASS is required; nothing here is closure.
"""
import os, sys, json, math, time, io, contextlib

sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def find_repo():
    z = os.environ.get("ZF_REPO")
    if z and os.path.isdir(os.path.join(z, "campaign_fresh_gravity")):
        return os.path.abspath(z)
    p = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(p, "campaign_fresh_gravity")) and os.path.isdir(os.path.join(p, "hunt_2026")):
            return p
        p = os.path.dirname(p)
    raise SystemExit("cannot find the repository: set ZF_REPO to the repository root")


REPO = find_repo()
LANES = os.path.join(REPO, "campaign_fresh_gravity")
HOME = os.path.expanduser("~")


def scrub(s):
    s = str(s)
    for a, b in ((REPO, "<repo>"), (HERE, "<lane>"), (HOME, "~")):
        if a and a != "/":
            s = s.replace(a, b)
    return s


def jclean(o):
    if isinstance(o, dict):
        return {str(k): jclean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jclean(v) for v in o]
    if isinstance(o, np.ndarray):
        return jclean(o.tolist())
    if isinstance(o, (np.floating,)):
        o = float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, float):
        if math.isnan(o):
            return None
        if math.isinf(o):
            return "inf" if o > 0 else "-inf"
    return o


# ------------------------------------------------------------------------------------------------ constants (declared)
C_SI = 2.99792458e8
KPC_M = 3.0856775814913673e19
MPC_M = KPC_M * 1e3
GYR_S = 3.15576e16
MSUN = 1.98847e30
G_SI = 6.67430e-11
G_KPC = 4.30091727e-6                       # kpc (km/s)^2 / Msun
KAPPA = 0.5                                 # FITTED
FOOTS = ("canonical", "alt")
A0_SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0K = {f: A0_SI[f] * KPC_M / 1e6 for f in FOOTS}      # (km/s)^2 / kpc
H0, OM = 67.4, 0.315
OL = 1.0 - OM
H0S = H0 * 1e3 / MPC_M                      # 1/s
HL_S = H0S * math.sqrt(OL)
HL = HL_S * GYR_S                           # 1/Gyr
MASSES = (1e9, 1e10, 1e11, 1e12)
QS = (0.05, 0.1, 0.2)
OMEGA_C_OVER_B = 5.36                       # the record's cosmic share (CFG4_README.md:227)


def t_of_z(z):
    return 2.0 / (3.0 * H0S * math.sqrt(OL)) * math.asinh(math.sqrt(OL / OM) * (1.0 + z) ** -1.5) / GYR_S


T0 = t_of_z(0.0)
RHO_L = 3.0 * HL_S ** 2 / (8.0 * math.pi * G_SI) * KPC_M ** 3 / MSUN      # Msun / kpc^3


def r_M(M, foot="canonical"):
    return math.sqrt(G_KPC * M / A0K[foot])


def rates(foot):
    """the three DECLARED relaxation rates, per Gyr (frozen section 1)."""
    a0c = A0_SI[foot] / C_SI * GYR_S
    return {"G-H": HL, "G-a": a0c, "G-b": a0c / KAPPA}


CAND = ("G-H", "G-a", "G-b")

# ------------------------------------------------------------------------------------------------ kernels
def nu_p2(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return np.sqrt(1.0 + 1.0 / y)


_NUMONO = None


def nu_mono(y):
    """FP1's committed nu_mono table, the slice exec'd READ-ONLY from real_research/derivation_chain_2026/FP1_static_sector.py
    (the same slice CFG4_common exec's); a SHARED, declared piece of record code."""
    global _NUMONO
    if _NUMONO is None:
        from scipy.optimize import brentq
        path = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP1_static_sector.py")
        src = open(path).read()
        ia = src.index("def _h_rar(y):")
        ib = src.index("KER, KNAME = ")
        ns = {"np": np, "math": math, "brentq": brentq}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[ia:ib], path, "exec"), ns)
        _NUMONO = ns["nu_mono"]
    return _NUMONO(y)


KERNELS = {"P2": nu_p2, "nu_mono": nu_mono}


def Mph_point(x, kernel="P2"):
    """M_ph(<r)/M_b for a point mass: r^2 (g_law - g_N)/G / M_b = nu(y) - 1, y = g_N/a0 = 1/x^2."""
    x = np.asarray(x, float)
    return KERNELS[kernel](1.0 / x ** 2) - 1.0


# ------------------------------------------------------------------------------------------------ the committed passive products (read-only)
XB = 10.0 ** np.round(np.arange(-1.0, 1.5001, 0.1), 10)
XC = np.sqrt(XB[1:] * XB[:-1])
SIMS_PATH = os.path.join(LANES, "CFG244_bound_fluid", "CFG244_A_infall_bound_sims.json")
CLUST_PATH = os.path.join(LANES, "CFG4_clusters_results.json")
_SIMS = None


def sims():
    global _SIMS
    if _SIMS is None:
        _SIMS = json.load(open(SIMS_PATH))
    return _SIMS


def point_run(M, q, N=20000):
    for r in sims()["runs"]:
        sp = r["spec"]
        if sp["kind"] in ("main", "C3") and sp["geom"] == "point" and sp["M"] == M and sp["q"] == q and sp["N"] == N:
            return r
    raise KeyError((M, q, N))


def passive(M, q, foot):
    """dict: x grid, M_c,bound(<r) time-averaged (Msun), bootstrap sd of the cumulative ratio, the 5k-shell cumulative ratio, S (bound cold mass)."""
    r20 = point_run(M, q, 20000)
    r5 = point_run(M, q, 5000)
    f20, f5 = r20["foot"][foot], r5["foot"][foot]
    Mc = np.array(f20["inst"]["Mc"])
    Mph = M * Mph_point(XC)                          # canonical-footing x grid is the sims' own; see rescale below
    # the sims' x grid is x = r/r_M(foot): the bins are in units of THAT footing's r_M, so XC is right for both footings
    McT = np.array(f20["target"]["Mc"])
    S = r20["diag"]["frac_bound_all"] * r20["setup"]["M_out"]
    return dict(M=M, q=q, foot=foot, x=XC, Minf=Mc, McT=McT, Mph=Mph,
                R=Mc / Mph, R5=np.array(f5["inst"]["Mc"]) / Mph, boot=np.array(f20["inst"]["boot_sd_cum"]),
                dM=np.array(f20["inst"]["dM"]), S=S, M_out=r20["setup"]["M_out"], r_ta0=r20["setup"]["r_ta0"],
                M_ta=r20["setup"]["M_ta"], Rs_z0=r20["Rs_z0"]["inst"], x_Rs_z0=r20["x_Rs_z0"]["inst"])


# ------------------------------------------------------------------------------------------------ the frozen relaxation model (section 3, Gate T)
def relaxed_Mc(Minf, Mph, S, e, mode="two", cap=True, create=False):
    """cumulative cold mass after relaxation; e = exp(-Gamma tau).  All masses in Msun (or M_b units, consistently).
    two     : M_target + e (M_inf - M_target),   M_target = min(M_ph, S)   (R-FLUX-2, primary)
    one     : M_inf + (1-e) max(M_target - M_inf, 0)                       (R-FLUX-1, fill-only)
    create  : the creation form (variant V-CREATE): no supply cap
    sign flip is applied by the caller through e -> 2 - e  (relaxation away from the target)."""
    Mt = np.minimum(Mph, S) if (cap and not create) else Mph
    if mode == "two":
        return Mt + e * (Minf - Mt)
    if mode == "one":
        return Minf + (1.0 - e) * np.maximum(Mt - Minf, 0.0)
    raise ValueError(mode)


def delta_dex(Mc, Mph, Mb):
    """Delta = log10[g_tot,class / g_law] = log10[(M_b + M_c) / (M_b + M_ph)] (point mass: M_law = M_b sqrt(1+x^2))."""
    return np.log10((Mb + Mc) / (Mb + Mph))


# ------------------------------------------------------------------------------------------------ clusters (committed arrays, read-only)
def clusters(foot, kernel="P2", b="b0.0"):
    d = json.load(open(CLUST_PATH))
    return d["numbers"]["C"][f"{foot}|{kernel}|{b}"], d


# ------------------------------------------------------------------------------------------------ report / output
class Report:
    def __init__(self, slug, mutate=None):
        self.mutate = mutate
        self.slug = slug + (f"_MUTATE_{mutate}" if mutate else "")
        self.lines, self.cells, self.numbers, self.t0 = [], {}, {}, time.time()

    def P(self, s=""):
        s = scrub(s)
        print(s, flush=True)
        self.lines.append(s)

    def banner(self, s):
        self.P("\n" + "=" * 118 + "\n" + s + "\n" + "=" * 118)

    def cell(self, name, outcome, detail=""):
        self.cells[name] = dict(outcome=outcome, detail=str(detail))
        self.P(f"  [{outcome}] {name}" + (f"\n         {detail}" if detail else ""))

    def finish(self, extra=None):
        self.numbers["seconds"] = time.time() - self.t0
        out = dict(slug=self.slug, mutate=self.mutate, cells=self.cells, numbers=self.numbers)
        if extra:
            out.update(extra)
        open(os.path.join(HERE, self.slug + ".out"), "w").write("\n".join(self.lines) + "\n")
        json.dump(jclean(out), open(os.path.join(HERE, self.slug + "_results.json"), "w"), indent=1)


def upstream_binding():
    """Which gate (if any) has already produced a binding FAIL, read from the committed lane outputs, so that later gates are labelled POST-HOC."""
    order = [("T", "CFG245_T_timescale"), ("C", "CFG245_C_clusters"), ("A", "CFG245_A_supply"), ("E", "CFG245_E_ledger")]
    for g, slug in order:
        for suffix in ("", "_POSTHOC"):
            p = os.path.join(HERE, slug + suffix + "_results.json")
            if os.path.exists(p):
                try:
                    d = json.load(open(p))
                except Exception:
                    continue
                if d.get("binding_fail"):
                    return g
    return None


def exit_mutate(bites, expected_bites):
    """MUTATE exit convention: 1 when the control bites, 0 when it does not; prints the frozen expectation."""
    print(f"MUTATE {'bites' if bites else 'does NOT bite'} (frozen expectation: {'bites' if expected_bites else 'does not bite'}; "
          f"{'as frozen' if bool(bites) == bool(expected_bites) else 'UNEXPECTED'})", flush=True)
    sys.exit(1 if bites else 0)
