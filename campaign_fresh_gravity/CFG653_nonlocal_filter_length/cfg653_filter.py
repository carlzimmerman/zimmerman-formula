#!/usr/bin/env python3
"""CFG653: can the filter length L of astra's variational nonlocal response be DERIVED from framework quantities?
Criteria: FROZEN_CRITERIA.md (commit d44fee295, committed alone before this script).  kappa = 1/2 FITTED; both footings,
never pooled; cold energy; not theory closed.
Run: nice -n 10 python3 cfg653_filter.py [--mutate] [--part K|A|B|C|all]
"""
import os
for _n in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_n] = "1"
import sys
import io
import json
import math
import time
import hashlib
import contextlib
import warnings
import numpy as np
from scipy.optimize import brentq
from scipy.linalg import expm
from scipy.stats import chi2 as CHI2

warnings.filterwarnings("ignore")
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg653_core as K

C = K.C
MUT = "--mutate" in sys.argv
PART = sys.argv[sys.argv.index("--part") + 1] if "--part" in sys.argv else "all"
TAG = "_MUTATE" if MUT else ""
OUTF = os.path.join(HERE, f"cfg653_filter{TAG}_{PART}.out")
JSF = os.path.join(HERE, f"cfg653_filter{TAG}_{PART}_results.json")
OUT, RES = [], {}


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


def save():
    open(OUTF, "w").write("\n".join(OUT) + "\n")
    json.dump(RES, open(JSF, "w"), indent=1, default=float)


# ------------------------------------------------------------------ constants
G, CL, MSUN, KPC, MPC = C.G_SI, C.C_SI, C.MSUN, C.KPC, C.MPC
A0 = C.A0
FOOTS = ("canonical", "alt")
RHO_L = C.RHO_LAMBDA
H_L = math.sqrt(8 * math.pi * G * RHO_L / 3)
L_DS = CL / H_L / KPC                                         # kpc
L_C2A = {f: CL ** 2 / A0[f] / KPC for f in FOOTS}               # kpc
OM0, H_FID, DTA = 0.3153, 0.6733167, 11.81                      # CFG4_target.py's r_ta inputs (flagged)
RHO_M = OM0 * 3 * (100 * H_FID * 1e3 / MPC) ** 2 / (8 * math.pi * G)
SCAN = [1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1e3, 3e3, 1e4, 1e5, 1e6, 1e7]
P(f"CFG653 nonlocal filter length{' [MUTATE]' if MUT else ''}; part {PART}")
P(f"  a0 canonical {A0['canonical']:.4e} / alt {A0['alt']:.4e}; l_dS = c/H_Lambda = {L_DS:.4e} kpc; c^2/a0 = "
  f"{L_C2A['canonical']:.4e} / {L_C2A['alt']:.4e} kpc; rho_m (CFG4 r_ta input) = {RHO_M:.3e} kg/m^3")


def mb_kpc2(Mb_msun, a0):
    """G M_b / a0 in kpc^2 (= r_M^2)."""
    return G * Mb_msun * MSUN / a0 / KPC ** 2


def r_ta_kpc(mb, a0):
    """CFG4's turnaround radius of an isolated point baryon mass under the local law: F(mb/r^2) r^2 a0 / G = DTA rho_m 4pi/3 r^3."""
    fn = lambda lr: math.log(K.F_law(mb / math.exp(lr) ** 2) * a0) - math.log(DTA * RHO_M * 4 * math.pi / 3 * G * math.exp(lr) * KPC)
    return math.exp(brentq(fn, math.log(1e-6), math.log(1e7)))


def r_zg_kpc(mb, a0):
    """dark-energy balance radius: law acceleration = (8 pi G rho_L / 3) r."""
    fn = lambda lr: math.log(K.F_law(mb / math.exp(lr) ** 2) * a0) - math.log(H_L ** 2 * math.exp(lr) * KPC)
    return math.exp(brentq(fn, math.log(1e-6), math.log(1e7)))


def length_of(cand, mb, a0, foot):
    if cand == "C1_rM":
        return math.sqrt(mb)
    if cand == "C2a_c2_a0":
        return L_C2A[foot]
    if cand == "C2b_l_dS":
        return L_DS
    if cand == "C3a_r_ta":
        return r_ta_kpc(mb, a0)
    if cand == "C3b_r_zg":
        return r_zg_kpc(mb, a0)
    raise ValueError(cand)


CANDS = ["C1_rM", "C2a_c2_a0", "C2b_l_dS", "C3a_r_ta", "C3b_r_zg"]


def point_boost(mb, r_eval, L):
    """isolated nonlocal boost M_dyn(<r)/M_b of a point baryon mass (a0 = 1 units, kpc) at radii r_eval."""
    r_eval = np.atleast_1d(np.asarray(r_eval, float))
    Lg = L if (L is not None and np.isfinite(L) and L > 0) else 1e3
    rg = K.make_grid(Lg, r_data=r_eval, rmin=1e-4 * min(math.sqrt(mb), r_eval.min()), per_dec=40,
                     rmax_min=max(1e3, 30 * r_eval.max()))
    mN = np.full(len(rg), mb)
    m, z, nr, it = K.Filter(rg, L).solve(mN, m0=rg ** 2 * K.F_law(mN / rg ** 2))
    idx = np.searchsorted(rg, r_eval)
    return m[idx] / mb, nr


def fres_of(L, mq_fun, R):
    """residual fraction of a host's total field after the filter: (P_L q)(R) / q(R)."""
    if L is None or not np.isfinite(L):
        return 1.0
    if L <= 0:
        return 0.0
    rg = K.make_grid(L, r_data=np.array([R]), rmin=1e-4 * min(R, L), per_dec=60, rmax_min=max(1e3, 40 * R))
    mq = mq_fun(rg)
    A = np.eye(len(rg)) - K.smoothing_matrix(rg, L)
    i = np.searchsorted(rg, R)
    return float((A[i] @ mq) / mq[i])


# ================================================================== PART K: controls K1, K2, M3, (c2)
def part_K():
    P("\n=== K1: local-law reproduction on SPARC (CFG4 statistic) ===")
    # done inside part A (same code path); here: K2 and M3 against astra's own 3D solver
    P("\n=== K2 / M3: astra's 3D periodic solver (calculate.py re-executed read-only, nothing written) vs this spherical solver ===")
    src = open(os.path.join(K.REPO, "sol61_push/nonlocal_response_2026_10_12/calculate.py")).read()
    src = src.replace("HERE=Path(__file__).resolve().parent",
                      "HERE=Path(%r)" % os.path.join(K.REPO, "sol61_push/nonlocal_response_2026_10_12"))
    src = src[:src.index("reference=profiles")]
    from scipy.special import erf
    k2 = {}
    for N, box, Ls in ((64, 128.0, (4, 8)), (32, 64.0, (4,)), (64, 64.0, (4,)), (128, 64.0, (4,))):
        s3 = src.replace("N=32;box=64.", f"N={N};box={box!r}").replace("for L in (4,8,16,'local'):", f"for L in {tuple(Ls) + ('local',)!r}:")
        ns = {"__file__": "cfg653_k2"}
        t0 = time.time()
        with contextlib.redirect_stdout(io.StringIO()):
            exec(s3, ns)
        r3 = ns["r"]
        sel = (r3 >= 4) & (r3 <= 12)
        rr = r3[sel]
        rhobar = 4 * np.pi / box ** 3
        for L in tuple(Ls) + ("local",):
            Lv = np.inf if L == "local" else float(L)
            rg = K.make_grid(1.0 if L == "local" else Lv, r_data=np.unique(np.round(rr, 10)), per_dec=40, rmax_min=200)
            x = rg / (2.0 * math.sqrt(2))
            mN = (erf(x) - math.sqrt(2 / math.pi) * (rg / 2.0) * np.exp(-rg ** 2 / 8.0)) - rhobar * rg ** 3 / 3
            m, z, nr, it = K.Filter(rg, Lv).solve(mN, m0=mN.copy())
            gs = np.interp(rr, rg, m / rg ** 2)
            prof = ns["profiles"][str(L)]
            d = float(np.linalg.norm(gs - prof) / np.linalg.norm(prof))
            k2[f"N{N}_box{int(box)}_L{L}"] = d
            P(f"  N {N} box {box:.0f} (dx {box / N:.1f}) L {L}: spherical vs 3D radial-force rel L2 (4<=r<=12) = {d:.4f}")
        inv = [c for c in ns["checks"] if c["name"].startswith("uniform external invariance")]
        for c in inv:
            P(f"  M3 {c['name']}: max change {c['value']:.2e} (tol {c['tolerance']:.0e}) -> {'PASS' if c['passed'] else 'FAIL'}")
        k2[f"M3_N{N}_box{int(box)}"] = [dict(name=c["name"], value=c["value"], passed=c["passed"]) for c in inv]
        P(f"  ({time.time() - t0:.0f} s)")
    RES["K2"] = k2
    # (c2) the variable-width filter operator: self-adjoint, doubly stochastic, contraction
    P("\n=== (c2): variable-width filter P = 1 - exp(div (L(x)^2/2) grad), 1D periodic check ===")
    n, box = 256, 100.0
    dx = box / n
    x = np.arange(n) * dx
    Lx = 1.0 + 4.0 * (1 + np.sin(2 * np.pi * x / box)) / 2           # L varies 1..5
    Dh = 0.5 * (0.5 * (Lx ** 2 + np.roll(Lx, -1) ** 2))              # half-point diffusivity
    Dm = np.zeros((n, n))
    for i in range(n):
        ip, im = (i + 1) % n, (i - 1) % n
        Dm[i, ip] += Dh[i] / dx ** 2
        Dm[i, im] += Dh[im] / dx ** 2
        Dm[i, i] -= (Dh[i] + Dh[im]) / dx ** 2
    S = expm(Dm)
    Pm = np.eye(n) - S
    ev = np.linalg.eigvalsh(0.5 * (Pm + Pm.T))
    c2 = dict(symmetric=float(np.abs(Pm - Pm.T).max()), annihilates_constants=float(np.abs(Pm @ np.ones(n)).max()),
              eig_min=float(ev.min()), eig_max=float(ev.max()))
    c2["pass"] = bool(c2["symmetric"] < 1e-10 and c2["annihilates_constants"] < 1e-10 and c2["eig_min"] > -1e-10 and c2["eig_max"] < 1 + 1e-12)
    P(f"  |P - P^T| {c2['symmetric']:.1e}; |P 1| {c2['annihilates_constants']:.1e}; eig(P) in [{c2['eig_min']:.2e}, {c2['eig_max']:.6f}] -> "
      f"{'PASS' if c2['pass'] else 'FAIL'} (self-adjoint, annihilates constants, 0 <= P <= 1: astra's convexity bound carries over)")
    RES["c2"] = c2


# ================================================================== PART A: SPARC RAR
def sparc_setup():
    GAL = C.load_sparc()
    out = []
    for g in GAL:
        R = g["R"]
        ok = (g["Vobs"] > 0)
        out.append(dict(name=g["name"], R=R, Vo=g["Vobs"], eV=g["eV"], Vg=g["Vgas"], Vd=g["Vdisk"], Vb=g["Vbul"]))
    return out


UC = np.round(np.arange(0.30, 1.2001, 0.05), 2)


def gal_resid(g, U, a0, Lrule, foot, cache):
    """weighted residual sums for one galaxy at one Upsilon; Lrule(mb) -> L (kpc) or None for local."""
    KPC_S = 3.0857e19
    Rm = g["R"] * KPC_S
    VB2 = np.sign(g["Vg"]) * g["Vg"] ** 2 + U * g["Vd"] ** 2 + 1.4 * U * g["Vb"] ** 2
    GB = VB2 * 1e6 / Rm
    GO = (g["Vo"] * 1e3) ** 2 / Rm
    OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & (g["Vo"] > 0)
    w = 1.0 / (np.clip(g["eV"], 1, None) / np.clip(g["Vo"], 1, None)) ** 2
    gb = GB / a0
    mb = g["R"][-1] ** 2 * gb[-1]
    L = Lrule(max(mb, 1e-30))
    if L is None:
        gp = K.F_law(np.maximum(gb, 0)) * a0
        nneg = 0
    else:
        rg = K.make_grid(L if (np.isfinite(L) and L > 0) else 1e3, r_data=g["R"], per_dec=40,
                         rmax_min=max(1e3, 30 * g["R"][-1]))
        key = (round(math.log(L), 9) if (np.isfinite(L) and L > 0) else L, len(rg))
        if key not in cache:
            cache.clear()
            cache[key] = K.Filter(rg, L)
        f = cache[key]
        mN = K.mN_profile(rg, g["R"], gb)
        m, z, nr, it = f.solve(mN, m0=rg ** 2 * K.F_law(np.abs(mN) / rg ** 2) * np.sign(mN))
        idx = np.searchsorted(rg, g["R"])
        gp = m[idx] / g["R"] ** 2 * a0
        nneg = int(((gp <= 0) & OK).sum())
    gpf = np.where(gp > 0, gp, 1e-3 * GO)                      # repulsive/zero prediction: floored (3 dex residual), counted
    r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, gpf, 1.0))
    return float(np.sum(np.where(OK, w * r_ ** 2, 0))), float(np.sum(np.where(OK, w, 0))), nneg, L


def sparc_rms(GALS, a0, Lrule, foot, label):
    t0 = time.time()

    def total(U):
        S = W = 0.0
        nn = 0
        Ls = []
        for g in GALS:
            s, w, n_, L = gal_resid(g, U, a0, Lrule, foot, g.setdefault("_cache", {}))
            S += s; W += w; nn += n_; Ls.append(L if L is not None else np.inf)
        return math.sqrt(S / W), nn, Ls

    best = None
    tried = {}
    for U in UC:
        tried[round(U, 2)] = total(U)
    Ub = min(tried, key=lambda u: tried[u][0])
    for U in np.round(np.arange(Ub - 0.04, Ub + 0.0401, 0.01), 2):
        if 0.30 <= U <= 1.20 and round(U, 2) not in tried:
            tried[round(U, 2)] = total(U)
    Ub = min(tried, key=lambda u: tried[u][0])
    rms, nn, Ls = tried[Ub]
    Ls = np.array(Ls)
    fin = Ls[np.isfinite(Ls)]
    P(f"  {label:22s} {foot:9s}: rms {rms:.4f} dex @ Upsilon {Ub:.2f}; repulsive points {nn}; "
      + (f"L median {np.median(fin):.3g} kpc (range {fin.min():.3g}-{fin.max():.3g})" if len(fin) else "L local")
      + f"  [{time.time() - t0:.0f} s]")
    return dict(rms=rms, U=Ub, n_repulsive=nn, L_median=float(np.median(fin)) if len(fin) else None,
                L_min=float(fin.min()) if len(fin) else None, L_max=float(fin.max()) if len(fin) else None)


def gate_a(r, base):
    d = r["rms"] - base
    if d <= 0.005 and 0.50 <= r["U"] <= 0.80:
        return "PASS"
    if d <= 0.010:
        return "TENSION"
    return "FAIL"


def part_A():
    GALS = sparc_setup()
    P(f"\n=== PART A: SPARC RAR ({len(GALS)} galaxies), CFG4 statistic, nu_mono ===")
    A = {}
    base = {}
    for foot in FOOTS:
        a0 = A0[foot]
        r_alg = sparc_rms(GALS, a0, lambda mb: None, foot, "local law (algebraic)")
        r_inf = sparc_rms(GALS, a0, lambda mb: np.inf, foot, "solver, L = infinity")
        base[foot] = r_alg["rms"]
        ref = {"canonical": (0.1003, 0.61), "alt": (0.0991, 0.57)}[foot]
        k1 = abs(r_alg["rms"] - ref[0]) <= 1e-4 + 5e-5 and abs(r_alg["U"] - ref[1]) < 1e-9 and abs(r_inf["rms"] - r_alg["rms"]) < 1e-4
        P(f"  K1 {foot}: CFG4 {ref[0]} @ {ref[1]} vs algebraic {r_alg['rms']:.5f} @ {r_alg['U']:.2f}, solver(L=inf) {r_inf['rms']:.5f} -> {'PASS' if k1 else 'FAIL'}")
        A[f"K1|{foot}"] = dict(algebraic=r_alg, solver_inf=r_inf, pass_=bool(k1))
    if MUT:
        for foot in FOOTS:
            a0 = A0[foot]
            m1 = sparc_rms(GALS, a0, lambda mb: 1e12, foot, "M1 L = 1e12 kpc")
            m2 = sparc_rms(GALS, a0, lambda mb: 1e-6, foot, "M2 L = 1e-6 kpc")
            newton = sparc_rms(GALS, a0, lambda mb: 0.0, foot, "Newton (A = 0)")
            A[f"M1|{foot}"] = dict(r=m1, detect=bool(abs(m1["rms"] - base[foot]) <= 1e-4))
            A[f"M2|{foot}"] = dict(r=m2, newton=newton, detect=bool(abs(m2["rms"] - newton["rms"]) <= 1e-3))
            P(f"  M1 {foot}: |rms - local| = {abs(m1['rms'] - base[foot]):.2e} -> {'DETECTED' if A[f'M1|{foot}']['detect'] else 'NOT'}; "
              f"M2 {foot}: |rms - Newton| = {abs(m2['rms'] - newton['rms']):.2e} -> {'DETECTED' if A[f'M2|{foot}']['detect'] else 'NOT'}")
        RES["A"] = A
        return
    for foot in FOOTS:
        a0 = A0[foot]
        for L in SCAN:
            r = sparc_rms(GALS, a0, lambda mb, L=L: L, foot, f"scan L = {L:g} kpc")
            r["gate_a"] = gate_a(r, base[foot])
            A[f"scan{L:g}|{foot}"] = r
            save()
        for cand in CANDS:
            r = sparc_rms(GALS, a0, lambda mb, cand=cand: length_of(cand, mb, a0, foot), foot, cand)
            r["gate_a"] = gate_a(r, base[foot])
            A[f"{cand}|{foot}"] = r
            RES["A"] = A
            save()
    RES["A"] = A
    RES["A_base"] = base


# ================================================================== PART B: R7 (satellites, binaries)
def nfw_setup():
    CM = os.path.join(K.REPO, "sonnet55_push", "cold_mass", "cm14b_sifon_table.py")
    src = open(CM).read()
    ns = {"__file__": CM, "__name__": "cm14b"}
    os.environ.pop("MUTATE", None)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src[:src.index('rows = {"A"')], ns)
    return ns


TH = np.linspace(0, math.pi, 4001)
_trap = getattr(np, "trapezoid", None) or np.trapz


def boost_efe(y, ye):
    """CFG478's exact QUMOND enclosed boost (point mass y = g_N/a0 at the sphere, uniform Newtonian host field ye), a0 = 1."""
    y = np.atleast_1d(np.asarray(y, float))
    gr = -y[:, None] + ye * np.cos(TH)[None, :]
    gm = np.sqrt(y[:, None] ** 2 + ye ** 2 - 2 * y[:, None] * ye * np.cos(TH)[None, :])
    nu = C.nu_mono(np.maximum(gm, 1e-30))
    integ = (nu - 1) * gr * np.sin(TH)[None, :]
    return 1.0 - _trap(integ, TH, axis=1) / (2.0 * y)


def satellites(Lassign, foot, ns, label, verbose=True):
    """Lassign(kind, mb_sat_kpc2, R_mpc) -> L (kpc) for the satellite at R; returns chi2, p, boosts."""
    a0 = A0[foot]
    mstar, mbg, rsat, Mh, rho_h = ns["mstar"], ns["mbg"], ns["rsat"], ns["Mh"], ns["rho_h"]
    Gc, Msun_c, Mpc_c = ns["G"], ns["Msun"], ns["Mpc"]
    pulls, boosts, fr, bs, be, Lused = [], [], [], [], [], []
    for lm, (lmb, elo, ehi), R in zip(mstar, mbg, rsat):
        Ms = 10 ** lm; Mb = 1.2 * Ms; ret = 0.13 * (0.1200 / 0.02237) * Mb; mb = 10 ** lmb
        rbg = (mb / (4 * math.pi * rho_h(R))) ** (1 / 3)              # Mpc
        ge = Gc * Mh(R) * Msun_c / (R * Mpc_c) ** 2                   # host total field, m/s^2
        msat = mb_kpc2(Mb, a0)
        L = Lassign(msat, R)
        mq = lambda rk: Gc * np.array([Mh(x / 1e3) for x in rk]) * Msun_c / a0 / KPC ** 2   # host m(r) in kpc^2 (a0 = 1)
        f = fres_of(L, mq, R * 1e3)
        ye_eff = abs(f) * ge / a0                                    # CFG478's convention: host field enters as g_e
        yN_rbg = msat / (rbg * 1e3) ** 2
        bE = float(boost_efe(np.array([yN_rbg]), ye_eff)[0])
        bS = float(point_boost(msat, np.array([rbg * 1e3]), L)[0][0])
        bt = min(bS, bE)
        Mtot = Mb * bt + ret
        sig = 0.5 * (elo + ehi)
        pulls.append((lmb - math.log10(max(Mtot, 1e-3 * Mb))) / sig)   # repulsive/zero: floored, counted as a huge pull
        boosts.append(bt); fr.append(f); bs.append(bS); be.append(bE); Lused.append(L if L is not None else np.inf)
    X2 = float(np.sum(np.array(pulls) ** 2)); p = float(CHI2.sf(X2, 5))
    if verbose:
        P(f"  sat {label:26s} {foot:9s}: chi2 {X2:7.1f}/5 p {p:.2g} | f_res {np.round(fr, 3).tolist()} | B_self "
          f"{np.round(bs, 2).tolist()} B_EFE {np.round(be, 2).tolist()} | L {np.round(Lused, 1).tolist()} kpc")
    return dict(chi2=X2, p=p, f_res=fr, B_self=bs, B_EFE=be, L=Lused, gate=("PASS" if p >= 0.01 else "FAIL"))


def part_B():
    ns = nfw_setup()
    PIPE = os.path.join(K.REPO, "prep_2026", "gaia_dr4_prep", "wide_binary_pipeline.py")
    sha0 = hashlib.sha256(open(PIPE, "rb").read()).hexdigest()
    sys.path.insert(0, os.path.dirname(PIPE))
    argv0 = sys.argv; sys.argv = [sys.argv[0]]
    with contextlib.redirect_stdout(io.StringIO()):
        import wide_binary_pipeline as W
    sys.argv = argv0
    B = {}
    P("\n=== PART B1: cluster satellites (CFG478 data), residual host field + filtered self-field ===")
    # K3: f_res = 1, local self-field -> CFG478 Q1 nu_mono
    for foot in FOOTS:
        r = satellites(lambda m, R: np.inf, foot, ns, "K3 local (L = inf)")
        ref = {"canonical": 98.7, "alt": 94.6}[foot]
        B[f"K3|{foot}"] = dict(r=r, pass_=bool(abs(r["chi2"] - ref) <= 0.1))
        P(f"  K3 {foot}: chi2 {r['chi2']:.2f} vs CFG478 {ref} -> {'PASS' if B[f'K3|{foot}']['pass_'] else 'FAIL'}")
    if MUT:
        for foot in FOOTS:
            r1 = satellites(lambda m, R: 1e12, foot, ns, "M1 L = 1e12")
            r2 = satellites(lambda m, R: 1e-6, foot, ns, "M2 L = 1e-6")
            B[f"M1sat|{foot}"] = dict(r=r1, detect=bool(min(r1["f_res"]) >= 0.999))
            B[f"M2sat|{foot}"] = dict(r=r2, detect=bool(max(abs(b - 1) for b in r2["B_self"]) < 0.02))
    else:
        for foot in FOOTS:
            a0 = A0[foot]
            for L in SCAN + [L_C2A[foot], L_DS]:
                B[f"sat_scan{L:g}|{foot}"] = satellites(lambda m, R, L=L: L, foot, ns, f"scan L = {L:g} kpc")
            for cand in ("C1_rM", "C3a_r_ta", "C3b_r_zg"):
                for fb in (0.10, 0.20):
                    mcl = lambda R, fb=fb: mb_kpc2(fb * 6e14, a0)
                    B[f"sat_{cand}_cluster_fb{fb}|{foot}"] = satellites(
                        lambda m, R, cand=cand, fb=fb: length_of(cand, mb_kpc2(fb * 6e14, a0), a0, foot), foot, ns,
                        f"{cand} cluster f_b {fb}")
                B[f"sat_{cand}_own|{foot}"] = satellites(lambda m, R, cand=cand: length_of(cand, m, a0, foot), foot, ns,
                                                         f"{cand} own")
            for cand in ("C2a_c2_a0", "C2b_l_dS"):
                B[f"sat_{cand}|{foot}"] = satellites(lambda m, R, cand=cand: length_of(cand, 1.0, a0, foot), foot, ns, cand)
            P("  [POST-HOC diagnostic, not frozen: finer constant-L satellite scan between the frozen 100 and 300 kpc nodes]")
            for L in (120.0, 150.0, 180.0, 210.0, 250.0):
                B[f"sat_posthoc{L:g}|{foot}"] = satellites(lambda m, R, L=L: L, foot, ns, f"post-hoc L = {L:g} kpc")
            RES["B"] = B
            save()

    P("\n=== PART B2: wide binaries (CFG447 machinery; frozen DR4 pipeline imported read-only) ===")
    DR3 = {"canonical": (W.A0_CAN, 1.0750, 0.0550, 1.1175, 0.0625), "alt": (W.A0_ALT, 1.0775, 0.0512, 1.0875, 0.0537)}
    rng = np.random.default_rng(4470)
    with contextlib.redirect_stdout(io.StringIO()):
        pop_m = W.make_population(1_000_000, rng, dr4=True)
        mods = {f: W.model_medians(pop_m, DR3[f][0], W.GRID, rng) for f in DR3}
    seeds = list(range(47001, 47011))
    LY = np.linspace(-4.0, 4.0, 161)
    tabs = {}

    def boost_table(foot, f_res, Lratio):
        """B(y) = min(B_self(y), B_EFE(y, f_res)) on the LY grid; Lratio = L / r_M of the binary (None: self unfiltered)."""
        key = (foot, round(f_res, 6), None if Lratio is None else round(Lratio, 6))
        if key in tabs:
            return tabs[key]
        a0 = DR3[foot][0]
        ye = float(K.B_inv(np.array([abs(f_res) * W.GEXT_PHYS / a0]))[0])
        y = 10 ** LY
        bE = boost_efe(y, ye) if ye > 0 else C.nu_mono(y)
        if Lratio is None:
            bS = C.nu_mono(y)
        else:
            # point mass m_b = 1 (r_M = 1): y = 1/r^2 -> r = y^-1/2 ; L = Lratio
            bS, _ = point_boost(1.0, 1.0 / np.sqrt(y[::-1]), Lratio)
            bS = bS[::-1]
        tabs[key] = np.minimum(bS, bE)
        return tabs[key]

    def recover(foot, f_res, Lratio):
        a0 = DR3[foot][0]
        tab = boost_table(foot, f_res, Lratio)
        gs = []
        for s in seeds:
            r = np.random.default_rng(s)
            with contextlib.redirect_stdout(io.StringIO()):
                pd = W.make_population(int(6210 * 2.7), r, dr4=False)
                keep = r.permutation(len(pd["s_obs"]))[:6210]
                pd = {k: v[keep] for k, v in pd.items()}
                gam = np.sqrt(np.interp(np.log10(pd["g_true"] / a0), LY, tab))
                vX = (gam * pd["pmx"] + pd["npmx"]) * 4.74e3 * (pd["d_obs"] / 1000.)
                vY = (gam * pd["pmy"] + pd["npmy"]) * 4.74e3 * (pd["d_obs"] / 1000.)
                vt = np.hypot(vX, vY) / pd["vc_obs"]
                g, sg, *_ = W.run_fit(np.log10(pd["g_proj"] / a0), vt, mods[foot], r, "x")
            gs.append(g)
        gs = np.array(gs)
        med, spr = float(np.median(gs)), float(np.std(gs))
        _, gb, sb, gl, sl = DR3[foot]
        zb = (med - gb) / math.hypot(sb, spr)
        zl = (med - gl) / math.hypot(sl, spr)
        gate = "PASS" if zb <= 2 else ("TENSION" if zb <= 5 else "FAIL")
        return dict(median=med, spread=spr, pinned=int((gs >= W.GRID[-1] - 1e-9).sum()), z_builder=float(zb),
                    z_literal=float(zl), gate=gate, f_res=f_res, Lratio=Lratio)

    R0 = 8.2
    rcache = {}

    def run(label, foot, f_res, Lratio):
        key = (foot, round(f_res, 4), None if Lratio is None else round(Lratio, 4))
        if key not in rcache:
            rcache[key] = recover(foot, f_res, Lratio)
        r = dict(rcache[key])
        P(f"  wb {label:30s} {foot:9s}: f_res {f_res:.4f} L/r_M(binary) {('-' if Lratio is None else f'{Lratio:.3g}')}: "
          f"gamma_hat {r['median']:.4f} (spread {r['spread']:.4f}, {r['pinned']}/10 pinned) z_builder {r['z_builder']:+.1f} "
          f"literal {r['z_literal']:+.1f} -> {r['gate']}")
        return r

    for foot in FOOTS:
        a0 = DR3[foot][0]
        mmw = mb_kpc2(6e10, a0)
        mq_mw = lambda rk, mmw=mmw: rk ** 2 * K.F_law(mmw / rk ** 2)
        P(f"  MW law field at R0 = {R0} kpc: {K.F_law(mmw / R0 ** 2):.3f} a0 (pipeline banked {W.GEXT_PHYS / a0:.3f} a0)")
        B[f"K4|{foot}"] = run("K4 EFE-blind (f_res = 0)", foot, 0.0, None)
        B[f"wb_local|{foot}"] = run("local (f_res = 1)", foot, 1.0, None)
        if MUT:
            f1 = fres_of(1e12, mq_mw, R0)
            B[f"M1wb|{foot}"] = dict(f_res=f1, detect=bool(f1 >= 0.999))
            P(f"  M1 binary host: f_res(L = 1e12) = {f1:.6f}")
            continue
        for L in SCAN + [L_C2A[foot], L_DS]:
            B[f"wb_scan{L:g}|{foot}"] = run(f"scan L = {L:g} kpc", foot, fres_of(L, mq_mw, R0), None)
        for cand in ("C1_rM", "C3a_r_ta", "C3b_r_zg"):
            for host, Mh_ in (("MW", 6e10), ("LG", 2e11)):
                L = length_of(cand, mb_kpc2(Mh_, a0), a0, foot)
                B[f"wb_{cand}_{host}|{foot}"] = run(f"{cand} {host} (L {L:.3g} kpc)", foot, fres_of(L, mq_mw, R0), None)
                B[f"wb_{cand}_{host}|{foot}"]["L"] = L
            # own: binary of 1.5 Msun (pipeline-typical); L / r_M fixed at that mass
            mbin = mb_kpc2(1.5, a0)
            Lb = length_of(cand, mbin, a0, foot)
            B[f"wb_{cand}_own|{foot}"] = run(f"{cand} own (L {Lb * 206264.8e3:.3g} AU)", foot, fres_of(Lb, mq_mw, R0),
                                             Lb / math.sqrt(mbin))
            B[f"wb_{cand}_own|{foot}"]["L_kpc"] = Lb
        for cand in ("C2a_c2_a0", "C2b_l_dS"):
            L = length_of(cand, 1.0, a0, foot)
            B[f"wb_{cand}|{foot}"] = run(cand, foot, fres_of(L, mq_mw, R0), None)
        RES["B"] = B
        save()
    sha1 = hashlib.sha256(open(PIPE, "rb").read()).hexdigest()
    P(f"  pipeline sha256 unchanged: {sha0 == sha1} ({sha0[:16]}...)")
    B["pipeline_sha_unchanged"] = bool(sha0 == sha1)
    RES["B"] = B


# ================================================================== PART C: well-posedness (c3, c4)
def part_C():
    P("\n=== PART C: (c3) discontinuity across system boundaries; (c4) static-limit causality ===")
    Cc = {}
    for foot in FOOTS:
        a0 = A0[foot]
        m1, m2 = mb_kpc2(6e10, a0), mb_kpc2(1.2e11, a0)
        for cand in ("C1_rM", "C3a_r_ta", "C3b_r_zg"):
            L1, L2 = length_of(cand, m1, a0, foot), length_of(cand, m2, a0, foot)
            r_e = np.array([3.0 * math.sqrt(m1)])                          # outer RAR radius 3 r_M of the galaxy
            b1, _ = point_boost(m1, r_e, L1)
            b2, _ = point_boost(m1, r_e, L2)
            jump = float(abs(math.log10(max(b2[0], 1e-30) / max(b1[0], 1e-30))))
            Cc[f"c3|{cand}|{foot}"] = dict(L_own=L1, L_merged=L2, r_eval=float(r_e[0]), boost_own=float(b1[0]),
                                           boost_merged=float(b2[0]), jump_dex=jump,
                                           verdict="OK" if jump <= 0.005 else "CONDITIONAL")
            P(f"  c3 {cand:9s} {foot:9s}: MW-mass galaxy, L own {L1:.4g} -> merged {L2:.4g} kpc; boost at 3 r_M "
              f"{b1[0]:.4f} -> {b2[0]:.4f}: jump {jump:.4f} dex -> {Cc[f'c3|{cand}|{foot}']['verdict']}")
        for cand, L in (("C2a_c2_a0", L_C2A[foot]), ("C2b_l_dS", L_DS)):
            ok = 3.37 * L <= L_DS
            Cc[f"c4|{cand}|{foot}"] = dict(L=L, ratio=3.37 * L / L_DS, pass_=bool(ok))
            P(f"  c4 {cand:9s} {foot:9s}: 3.37 L / l_dS = {3.37 * L / L_DS:.2f} -> {'PASS' if ok else 'FAIL'}")
    RES["C"] = Cc


if PART in ("K", "all"):
    part_K(); save()
if PART in ("A", "all"):
    part_A(); save()
if PART in ("B", "all"):
    part_B(); save()
if PART in ("C", "all") and not MUT:
    part_C(); save()
P("\ndone."); save()
