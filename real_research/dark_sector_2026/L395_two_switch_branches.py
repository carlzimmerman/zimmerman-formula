#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L395 -- THE FULL CONSTRUCTION AT THE LINEAR GATE ON THE LEAK-FREE SWITCH READING, WITH THE REGION CAP, SCORED RESOLUTION-FREE:
the MOND-sector switch (baryons + their phantom) with MS3's 1.75 Mpc region cap as the primary cell, the curvature and
matter-only readings as labelled comparisons; the particle-tracked clearing estimator (XR2 section 5); the z = 0.4 fields;
the alternative footing in one box.  Cells are never pooled across.

WHY.  L388 found a pooled window (575-650 km/s) at the linear vacuum gate p = 1, x_c0 = 2.5 with the MATTER-ONLY switch.  Since:
  * MS1 (mond_sector_gate_2026, committed 2a5def6d9): once the gate is an action term, a switch that reads the carrier --
    directly (matter) or through the curvature it sources -- gives the carrier an edge force (0.06-60x its own gravity
    around an L* lens); the MOND-sector reading, the baryons with their phantom (del^2(Phi - v)), is leak-free.
  * MS2: on that reading the flat-a0 flagship holds at z = 2.5 with no circumgalactic gas; the web needs 1/f_b = 6.4x the
    matter reading's overdensity to switch on.
  * MS3: the mock behind L388's cosmic-shear pass cannot score the construction; on L363's resolution-free halo model every
    uncapped carrier fails, and with L388's retention shear passes only with MOND regions capped near 1.75 Mpc (z = 0.5),
    v_cap ~ 325 km/s, whose local form is a threshold scaled by max(1, v_loc^2/v_cap^2), v_loc^2 = |grad Phi|^2/lap Phi.
  * the user (relayed by the coordinating review): both architectures as separate branches; on the switch, "all doors".
CELLS (all at p = 1, x_c0 = 2.5; L377's construction otherwise unchanged: phantom felt by the baryons and read by the
trigger, carrier Newtonian; the gate a prescribed mask each step):
  (c) "msc", THE PRIMARY CELL: the MOND-sector reading x = 1.5 Omega_m(a)(rho_b + max(delta_ph,all, 0)) -- the baryons plus
      the positive part of their untruncated phantom, MS3's absolute "door" convention -- with the local cap: the threshold
      x_c0 [Omega_L0/Omega_L(a)] is multiplied by max(1, v_loc^2/v_cap^2), v_loc^2 = |g_ms|^2/(-div g_ms) of the MOND-sector
      field g_ms = g_N,b + g_ph,all, v_cap = 325 km/s (MS3's K1);
  (b) "curv", comparison: the curvature reading x = 1.5 Omega_m(a)(rho - 1 + max(delta_ph,all, 0)) (L352/DE1/DE2's edge,
      MS3's "upper" convention), uncapped;
  (a) "matter", comparison on the (7, 11) box only: L377's matter-only switch (identical to L388 -- the reproduction control).
HISTORY.  Designs before any real run: (1) cell (b) as a freely iterated masked phantom -- a 128^3 code test showed it does
not converge (the compensation layer flips edge cells); (2) the curvature cell as the priority -- superseded by MS1-MS3 the
same day; the absolute-gate and grow-only-iteration extras were dropped to fund cell (c).  XR2's K2/K3 were recast for real
particles (0.42 baryon particles per cell; L particle-weighted) after the same code test.
RUNS: LCDM x 3 realisations (L369's seeds); cells (c) and (b) x 3 realisations x {600, 650} km/s; cell (a) on (7, 11) at
600 and 650; cell (c) on (7, 11) at the alternative footing, 600 and 650.  19 runs.
HOOKS (XR2 section 5; XR1): the z = 2 total and unit-weight carrier fields and the NGP cell of every baryon particle, and the
z = 0.4 fields, are written to real_research/dark_sector_2026/_L395_fields/ (gitignored) and kept; every estimator's per-box
numerators and denominators go into the results JSON.
GATES: strict S_8 (>= 0.922), forest (<= 10%), the clearing rule, two-sided X-COP (z = 0 median over >= 1e14 halos), and
COSMIC SHEAR ON MS3's HALO MODEL (L363's resolution-free halo model, MS3's R_of loaded unedited): worst R <= 1.2 on both
footings with the cell's OWN pooled retention by halo mass (MS3's construction of the retention function), at the cell's
convention and cap -- (c) "door", 1.75 Mpc; (b) "upper", uncapped; (a) "upper", uncapped (a proxy: MS3 has no matter-only
convention).  The mock score against DE3's T_max is reported beside it, not gated (MS3: not established).
PRE-DECLARED (before the run):
  CLEARING RULE (XR2 section 5): pooled L <= 0.30 AND B <= 0.30; D, E, E_rank reported; "estimator-dependent" if L and E fall
    on opposite sides of 0.30; "galaxy-bin failure" if the galaxy bin's L > 0.30 with a passing pool; C < 0.5 flagged.
  H_c: cell (c) has a pooled window (every gate above) at 600 or 650 km/s.
  (reported, not gated) cell (b), uncapped, is expected to FAIL cosmic shear on the halo model (MS3's X1).
CHECKS
  C1 the (7, 11) LCDM run reproduces L366's sigma_8 exactly.
  C2 cell (a) at (7, 11), 600 and 650 km/s reproduces L388's committed per-box S_8, fixed-cell clearing and X-COP median exactly.
  C3 MS3's halo model, loaded here, reproduces MS3's committed K1 at the 1.75 Mpc cap with L388's retention (1e-9, both footings).
  K0 species identity (rho = rhoc2 exactly in every LCDM run).  K1 null (model := LCDM gives every estimator 1).
  K2 index order (8^3 block sums: Pearson > 0.95, the transposed order >= 0.3 lower).
  K3 synthetic injection on the real (7, 11) LCDM z = 2 fields: in place B = D = E = the cell truth (1e-10); a rigid one-cell
     shift of baryons with their retained carrier leaves E and L unchanged (1e-10) while B drops.
  R_c = H_c.  W (informational): every table, flags, the cap's reach, cell (b), cell (a), the alternative footing, the mock
     shear score, the z = 0.4 retention by mass.
MUTATE=1: every kick is 0 (one run per realisation per cell, used for every kick): R_c must FAIL (rc = 1).
L395_POOL sets the pool size (default 8).

Run from the repository root:  python3 real_research/dark_sector_2026/L395_two_switch_branches.py
"""
import os, sys, json, math, time, inspect, io, contextlib
import numpy as np
from multiprocessing import Pool
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import L377_full_construction_pm as L77                        # noqa: E402  (L377's construction)
L77.X_C0, L77.P_GATE = 2.5, 1                                   # THE CELL: the linear vacuum gate (as L388)
L77.VCAP_CODE2 = (325.0 / 100.0) ** 2                           # MS3's v_cap, in the code's (100 km/s)^2

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L395_two_switch_branches"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L395", "cell": "p=1, x_c0=2.5", "mutate": MUTATE, "checks": {}, "numbers": {},
               "cells": {"msc": "MOND-sector reading (baryons + positive untruncated phantom, MS3's door) with the local v_cap = 325 km/s "
                                "cap -- the primary cell (MS1: leak-free as an action term)",
                         "curv": "curvature reading (matter + positive untruncated phantom, L352/DE1's edge), uncapped -- comparison",
                         "matter": "matter-only contrast (L377/L388), (7, 11) box only -- comparison and reproduction control"},
               "trigger": "phantom-inclusive (L377)", "footing": "canonical; cell (c) also at the alternative footing on (7, 11)",
               "shear": "MS3's resolution-free halo model gates; DE3's mock reported only"}
EXPECT_C = True                                                  # H_c, set before the run
L6, L7, L2 = L77.L6, L77.L7, L77.L2
LBOX, NG, NP, RHO_M, KG, WB, WC = L77.LBOX, L77.NG, L77.NP, L77.RHO_M, L77.KG, L77.WB, L77.WC
SEEDS = ((7, 11), (17, 21), (29, 33))
VK = (600.0, 650.0)
TAGS = tuple(f"v{int(v)}" for v in VK)
CELLS = ("msc", "curv")                                          # pooled cells, priority order
HM = {"msc": ("door", 1.75), "curv": ("upper", math.inf), "matter": ("upper", math.inf), "msc_alt": ("door", 1.75)}
THR = 50.0
BINS = (("galaxy", 0.0, 3e12), ("group", 3e12, 1e13), ("protocluster", 1e13, 1e18))
MBINS = (("6.0e+13-1.0e+14", 6e13, 1e14, 7.75e13), ("1.0e+14-1.5e+14", 1e14, 1.5e14, 1.22e14),
         ("1.5e+14-2.5e+14", 1.5e14, 2.5e14, 1.94e14), ("2.5e+14-1.0e+17", 2.5e14, 1e17, 5.0e14))   # L371's bins, MS3's centres
FIELDS = os.path.join(HERE, "_L395_fields" + ("_MUTATE" if MUTATE else ""))

# ---------------------------------------------------------------------------------- the switch readings, in L377's namespace
_SW = '''
SWDIAG = {"steps": 0, "capped_max": 0.0, "switched_max": 0.0}


def phantom_sw(s, rb, rho, a, a0c, swmode):
    """L377's phantom() with the switch reading as a choice: 'matter' (L377's own); 'curv' (matter + the positive untruncated
    phantom, uncapped); 'msc' (baryons + the positive untruncated phantom, absolute, with the local v_cap cap)."""
    if swmode == "matter":
        return phantom(s, rb, rho, a, a0c)
    gate = (OL / (Om * a ** -3 + OL) / OL) ** P_GATE
    gb = [-(1.0 / a) * g for g in s.grad(s.poisson(1.5 * Om * (rb - WB) / a))]
    nu1 = nu_vec(np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / a0c) - 1.0

    def solve(f):
        w = [np.where(f, nu1 * g, 0.0) for g in gb]
        divw = s.div(w)
        return s.poisson(-a * divw), -(2 * a * a / (3 * Om)) * divw

    Phi_all, dph_all = solve(np.ones(rho.shape, bool))           # the phantom as if switched on everywhere (untruncated)
    dpos = np.maximum(dph_all, 0.0)
    if swmode == "curv":
        f = 1.5 * Om_a(a) * (rho - 1.0 + dpos) * gate > X_C0
    else:                                                         # 'msc': the MOND sector, absolute, with the local cap
        xms = 1.5 * Om_a(a) * (rb + dpos) * gate
        gms = [gb[i] - (1.0 / a) * g for i, g in enumerate(s.grad(Phi_all))]
        mdiv = -s.div(gms) / a                                    # -div_r g_ms (physical), > 0 where the MOND sector is dense
        vloc2 = np.where(mdiv > 0, (gms[0] ** 2 + gms[1] ** 2 + gms[2] ** 2) / np.maximum(mdiv, 1e-30), 0.0)
        thr = X_C0 * np.maximum(1.0, vloc2 / VCAP_CODE2)
        f = xms > thr
        f0 = xms > X_C0
        SWDIAG["steps"] += 1
        if f0.any():
            SWDIAG["capped_max"] = max(SWDIAG["capped_max"], float((f0 & ~f).sum() / f0.sum()))
    SWDIAG["switched_max"] = max(SWDIAG["switched_max"], float(f.mean()))
    if not f.any():
        return None, None, 0.0
    Phi, dph = solve(f)
    return Phi, dph, float(f.mean())
'''
exec(compile(_SW, "L395.phantom_sw", "exec"), L77.__dict__)

_SRC = inspect.getsource(L77.run)
_REPS = [
    ("    name, sp, sk, xc, vk, gamma, tmp, mode, a0 = cfg",
     "    name, sp, sk, xc, vk, gamma, tmp, mode, a0, swmode = cfg\n    SWDIAG.update(steps=0, capped_max=0.0, switched_max=0.0)"),
    ("        ph = phantom(s, rb, rho, a, a0c) if mode != \"none\" else (None, None, 0.0)",
     "        ph = phantom_sw(s, rb, rho, a, a0c, swmode) if mode != \"none\" else (None, None, 0.0)"),
    ("    a = ai; dlna = 0.02; zs = [3.0, 2.0, 0.5, 0.3, 0.0]; out = {}",
     "    a = ai; dlna = 0.02; zs = [3.0, 2.0, 0.5, 0.4, 0.3, 0.0]; out = {}"),
    ("""                    rec["carrier_in_dense"] = float(rhoc2[dense].sum() / max(rho[dense].sum(), 1e-30))
""", """                    rec["carrier_in_dense"] = float(rhoc2[dense].sum() / max(rho[dense].sum(), 1e-30))
                    if z == 2.0:                                        # L395 hooks (XR2 section 5)
                        np.save(os.path.join(tmp, f"{name}_z2_rho.npy"), rho.astype(np.float32))
                        np.save(os.path.join(tmp, f"{name}_z2_rhoc.npy"), rhoc2.astype(np.float32))
                        ijk = np.floor(xb / s.d).astype(np.int64) % NG
                        np.save(os.path.join(tmp, f"{name}_z2_bcell.npy"), ((ijk[:, 0] * NG + ijk[:, 1]) * NG + ijk[:, 2]).astype(np.int32))
"""),
    ("    return name, out", "    out['sw_diag'] = dict(SWDIAG)\n    return name, out"),
]
_T = _SRC
for _a, _b in _REPS:
    assert _T.count(_a) == 1, _a[:60]
    _T = _T.replace(_a, _b)
exec(compile(_T.replace("def run(cfg):", "def run_sw(cfg):", 1), "L377.run+L395", "exec"), L77.__dict__)
run_sw = L77.run_sw


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


# ---------------------------------------------------------------------------------- XR2's estimators (ported), + L per section 5
def estimators(rho_l, c_l, rho_m, c_m, bcell_l=None, bcell_m=None, sel=None):
    """one box's numerators/denominators (XR2's estimators(); L particle-weighted per XR2 section 5).  sel restricts F (bins)."""
    b_l, b_m = rho_l - c_l, rho_m - c_m
    F = rho_l > THR
    Fs = F if sel is None else (F & sel)
    D_m = rho_m > THR
    S_m = b_m / WB > THR
    S_ms = S_m if sel is None else (S_m & sel)
    nF = int(F.sum())
    top = np.argsort(b_m.ravel())[::-1][:nF]
    out = dict(A=(float(c_m[D_m].sum() / WC / max(rho_m[D_m].sum(), 1e-30)), float(c_l[F].sum() / WC / max(rho_l[F].sum(), 1e-30))),
               B=(float(c_m[Fs].sum()), float(c_l[Fs].sum())), C=(float(b_m[Fs].sum()), float(b_l[Fs].sum())),
               E=(float(c_m[S_ms].sum()), float(b_m[S_ms].sum())),
               Er=(float(c_m.ravel()[top].sum()), float(b_m.ravel()[top].sum())),
               Fref=(float(c_l[Fs].sum()), float(b_l[Fs].sum())),
               n=dict(F=int(Fs.sum()), D_m=int(D_m.sum()), S_m=int(S_ms.sum()), S_m_in_F=int((S_ms & F).sum()),
                      bmass_S_m_in_F=float(b_m[S_ms & F].sum() / max(b_m[S_ms].sum(), 1e-30))))
    if bcell_l is not None:
        Fsr = Fs.ravel(); Pm = Fsr[bcell_l]                         # P: baryon particles in (the bin's part of) F in LCDM
        cm_, bm_, cl_, bl_ = c_m.ravel(), b_m.ravel(), c_l.ravel(), b_l.ravel()
        out["L"] = (float(cm_[bcell_m[Pm]].sum()), float(bm_[bcell_m[Pm]].sum()))
        out["Lref"] = (float(cl_[bcell_l[Pm]].sum()), float(bl_[bcell_l[Pm]].sum()))
    return out


def combine(rows):
    """pool over boxes by summing numerators and denominators (XR2's combine(); L380's convention); NaN where a set is empty."""
    s = lambda k, j: sum(r[k][j] for r in rows)
    q = lambda n, d: n / d if d > 0 else float("nan")
    ref = q(s("Fref", 0), s("Fref", 1))
    res = dict(A=q(s("A", 0), s("A", 1)), B=q(s("B", 0), s("B", 1)), C=q(s("C", 0), s("C", 1)),
               E=q(q(s("E", 0), s("E", 1)), ref) if ref == ref and ref > 0 else float("nan"),
               Er=q(q(s("Er", 0), s("Er", 1)), ref) if ref == ref and ref > 0 else float("nan"))
    res["D"] = q(res["B"], res["C"]) if res["C"] == res["C"] else float("nan")
    if all("L" in r for r in rows):
        lr = q(s("Lref", 0), s("Lref", 1))
        res["L"] = q(q(s("L", 0), s("L", 1)), lr) if lr == lr else float("nan")
    return res


def de3_tmax():
    """DE3's committed mock T_max(k) at this cell's lens-epoch threshold (reported only: MS3 shows the mock cannot score it)."""
    d3 = json.load(open(os.path.join(REPO, "real_research", "dark_energy_2026", "DE3_tmax_at_linear_gate_results.json")))["numbers"]
    assert (d3["cell"]["p"], d3["cell"]["x_c0"]) == (float(L77.P_GATE), float(L77.X_C0)), d3["cell"]
    key = f"{d3['cell']['x_lens']:.7f}"
    return {f_: {q: float(d3["table"][f"{key}/{f_}"]["T_max"][str(q)]) for q in KG} for f_ in ("canonical", "alt")}


def load_ms3():
    """MS3's halo-model machinery (L363's resolution-free halo model with the region cap), loaded unedited up to its scenarios;
    only MS3's own MUTATE flag (its first occurrence) is held False."""
    p3 = os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector.py")
    src = open(p3).read()
    flag = 'MUTATE = os.environ.get("MUTATE", "0") == "1"'
    assert src.index(flag) < src.index(".replace(" + repr(flag)[0] + flag), "MS3's own flag must come first"
    src = src.replace(flag, "MUTATE = False", 1).split("cut = lambda Mc")[0]
    ns = {"__name__": "ms3_in_l395", "__file__": p3}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, "MS3(L395)", "exec"), ns)
    return ns


if __name__ == "__main__":
    P(__doc__)
    os.makedirs(FIELDS, exist_ok=True)
    A0C, A0A = L77.A0["canonical"], L77.A0["alt"]
    cfgs, SRC = [], {}
    cfgs += [(f"s{sp}_lcdm", sp, sk, float("inf"), 0.0, 0.0, FIELDS, "none", A0C, "matter") for sp, sk in SEEDS]
    for cell in CELLS:                                          # cell order = priority (the MOND-sector cell first)
        for sp, sk in SEEDS:
            if MUTATE:
                cfgs.append((f"s{sp}_{cell}_v0", sp, sk, L77.XC_TRIG, 0.0, 10.0, FIELDS, "full", A0C, cell))
                SRC.update({(sp, cell, t): f"s{sp}_{cell}_v0" for t in TAGS})
            else:
                cfgs += [(f"s{sp}_{cell}_{t}", sp, sk, L77.XC_TRIG, v, 10.0, FIELDS, "full", A0C, cell) for t, v in zip(TAGS, VK)]
                SRC.update({(sp, cell, t): f"s{sp}_{cell}_{t}" for t in TAGS})
    if not MUTATE:
        cfgs += [(f"s7_msc_{t}_alt", 7, 11, L77.XC_TRIG, v, 10.0, FIELDS, "full", A0A, "msc") for t, v in zip(TAGS, VK)]
        cfgs += [(f"s7_matter_{t}", 7, 11, L77.XC_TRIG, v, 10.0, FIELDS, "full", A0C, "matter") for t, v in zip(TAGS, VK)]
        SRC.update({(7, "msc_alt", t): f"s7_msc_{t}_alt" for t in TAGS}); SRC.update({(7, "matter", t): f"s7_matter_{t}" for t in TAGS})
    else:
        P("  MUTATE: v_k = 0 in every decaying run (one run per realisation per cell, used for every kick)")
    P(f"  {len(cfgs)} runs, pool {int(os.environ.get('L395_POOL', '8'))}, cell p = {L77.P_GATE}, x_c0 = {L77.X_C0}; fields kept in {os.path.basename(FIELDS)}/")
    with Pool(int(os.environ.get("L395_POOL", "8"))) as pool:
        res = dict(pool.map(run_sw, cfgs, chunksize=1))
    P(f"  {len(cfgs)} runs done in {time.time() - T0:.0f}s")
    ld = lambda nm, z, f: np.load(os.path.join(FIELDS, f"{nm}_z{z}_{f}.npy"))

    # ------------------------------------------------------------------------------ controls C1, C3, K0, K2
    banner("C1, C3, K0, K2  CONTROLS")
    R66 = json.load(open(os.path.join(HERE, "L366_triggered_carrier_cluster_retention_results.json")))["numbers"]
    d1 = abs(res["s7_lcdm"]["0.0"]["sigma8"] / R66["runs"]["lcdm"]["0.0"]["sigma8"] - 1)
    check("C1 the (7, 11) LCDM run reproduces L366's sigma_8", f"relative deviation {d1:.1e}", d1 < 1e-9)
    M3 = load_ms3()
    R_of, XLIN, A0M = M3["R_of"], M3["XLIN"], M3["A0"]
    K1c = json.load(open(os.path.join(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector_results.json")))["numbers"]["K1"]["1.75"]
    c3 = {f_: max(R_of(XLIN, A0M[f_], 1.75, "door", M3["ret_L388"])[0].values()) for f_ in ("canonical", "alt")}
    dc3 = max(abs(c3[f_] - K1c[f_]["worst"]) for f_ in c3)
    check("C3 MS3's halo model, loaded here, reproduces MS3's committed K1 at the 1.75 Mpc cap with L388's retention (both footings)",
          f"worst R {c3} vs committed { {f_: K1c[f_]['worst'] for f_ in c3} } (max |diff| {dc3:.1e})", dc3 < 1e-9)
    k0 = max(float(np.max(np.abs(ld(f"s{sp}_lcdm", 2, "rho") - ld(f"s{sp}_lcdm", 2, "rhoc")))) for sp, _ in SEEDS)
    check("K0 species identity: in every LCDM run the z = 2 total and unit-weight carrier fields are equal (float32)",
          f"max |rho - rhoc2| = {k0:.1e}", k0 == 0.0)
    blk = lambda x_: x_.reshape(NG // 8, 8, NG // 8, 8, NG // 8, 8).sum(axis=(1, 3, 5)).ravel()
    k2c, k2t = [], []
    for sp, _ in SEEDS:
        cnt = np.bincount(ld(f"s{sp}_lcdm", 2, "bcell"), minlength=NG ** 3).reshape(NG, NG, NG).astype(float)
        rl_ = ld(f"s{sp}_lcdm", 2, "rho").astype(float)
        k2c.append(float(np.corrcoef(blk(cnt), blk(rl_))[0, 1])); k2t.append(float(np.corrcoef(blk(cnt.transpose(2, 1, 0)), blk(rl_))[0, 1]))
    check("K2 index order: on 8^3 block sums the LCDM baryon NGP counts correlate with rho at Pearson > 0.95 in every box, and the "
          "axis-transposed order (negative control) at least 0.3 lower", f"correct order {min(k2c):.4f} (min); transposed {max(k2t):.4f} (max)",
          min(k2c) > 0.95 and min(k2c) - max(k2t) > 0.3)

    # ------------------------------------------------------------------------------ per-box measurements
    TM = de3_tmax()
    est = L6.eps_bounds(); lo = max(v[0] for v in est.values()); hi = min(v[1] for v in est.values())
    s = L2.Sim(LBOX, NG, NP)
    PER, EST = {}, {}
    for sp, _ in SEEDS:
        L = f"s{sp}_lcdm"
        rho_l2 = ld(L, 2, "rho").astype(float); c_l2 = WC * ld(L, 2, "rhoc").astype(float); bc_l = ld(L, 2, "bcell")
        pk2 = L7.peaks_fast(s, rho_l2, npk=4000, sep=1.0)
        Mp = np.array([L6.sphere_sum(s, rho_l2, p_, 0.5) * RHO_M for p_ in pk2]); tree = cKDTree(pk2, boxsize=LBOX)
        _, jj = tree.query((np.array(np.unravel_index(np.arange(NG ** 3), rho_l2.shape)).T + 0.5) * s.d)
        envmass = Mp[jj].reshape(rho_l2.shape); del jj
        rho_l0, rc_l0 = ld(L, 0.0, "rho").astype(float), ld(L, 0.0, "rhoc").astype(float)
        pk = L6.peaks(s, rho_l0)
        Mh = np.array([L6.sphere_sum(s, rho_l0, p_, 1.0) * RHO_M for p_ in pk]); sel = Mh >= 1e14
        Mc_l = np.array([L6.sphere_sum(s, rc_l0, p_, 1.0) for p_ in pk])
        rho_l4, rc_l4 = ld(L, 0.4, "rho").astype(float), ld(L, 0.4, "rhoc").astype(float)
        pk4 = L6.peaks(s, rho_l4)
        Mh4 = np.array([L6.sphere_sum(s, rho_l4, p_, 1.0) * RHO_M for p_ in pk4])
        Mc_l4 = np.array([L6.sphere_sum(s, rc_l4, p_, 1.0) for p_ in pk4])
        if sp == 7:                                               # K1 and K3 on the real (7, 11) LCDM z = 2 fields
            K1 = combine([estimators(rho_l2, c_l2, rho_l2, c_l2, bc_l, bc_l)])
            b_l2 = rho_l2 - c_l2; F7 = rho_l2 > THR
            ret = np.random.default_rng(11).uniform(0.0, 0.2, rho_l2.shape)
            c1 = ret * c_l2; c1 = c1 + (c_l2 - c1).sum() / c1.size
            e1 = combine([estimators(rho_l2, c_l2, b_l2 + c1, c1, bc_l, bc_l)])
            t1 = float((c1[F7].sum() / b_l2[F7].sum()) / (c_l2[F7].sum() / b_l2[F7].sum()))
            shf = lambda x_: np.roll(x_, 1, axis=0)
            c2 = shf(ret * c_l2); c2 = c2 + (c_l2 - ret * c_l2).sum() / c2.size; b2 = shf(b_l2)
            i0, i1, i2 = np.unravel_index(bc_l, rho_l2.shape); bc2 = (((i0 + 1) % NG * NG + i1) * NG + i2).astype(np.int64)
            e2 = combine([estimators(rho_l2, c_l2, b2 + c2, c2, bc_l, bc2)])
            OUT["numbers"]["K"] = dict(K1=K1, K3_inplace=dict(truth=t1, **e1), K3_shift=e2)
        keys_here = [(sp, c_, t) for c_ in CELLS for t in TAGS] + ([(7, "msc_alt", t) for t in TAGS] + [(7, "matter", t) for t in TAGS]
                                                                    if sp == 7 and not MUTATE else [])
        for key_ in keys_here:
            nm = SRC[key_]; r_ = res[nm]
            rho_m2 = ld(nm, 2, "rho").astype(float); c_m2 = WC * ld(nm, 2, "rhoc").astype(float); bc_m = ld(nm, 2, "bcell")
            ests = {"all": estimators(rho_l2, c_l2, rho_m2, c_m2, bc_l, bc_m)}
            for bn, b0, b1 in BINS:
                ests[bn] = estimators(rho_l2, c_l2, rho_m2, c_m2, bc_l, bc_m, sel=(envmass >= b0) & (envmass < b1))
            eps = np.array([L6.sphere_sum(s, ld(nm, 0.0, "rhoc").astype(float), p_, 1.0) for p_ in pk]) / Mc_l
            eps4 = np.array([L6.sphere_sum(s, ld(nm, 0.4, "rhoc").astype(float), p_, 1.0) for p_ in pk4]) / Mc_l4
            PER[key_] = dict(s8=r_["0.0"]["sigma8"] / res[L]["0.0"]["sigma8"],
                             p1d={z: (np.array(r_[z]["p1d"]), np.array(res[L][z]["p1d"]), np.array(res[L][z]["kpar"])) for z in ("3.0", "2.0")},
                             pk=({q: r_["0.5"]["pk"][q] for q in KG}, {q: res[L]["0.5"]["pk"][q] for q in KG}),
                             eps_sel=eps[sel], eps=eps, Mh=Mh, eps4=eps4, Mh4=Mh4, sw_diag=r_.get("sw_diag"),
                             switched_z0=r_["0.0"].get("switched"))
            EST[key_] = ests
        for z_ in (0.3, 0.0):                                     # only the z = 2 and z = 0.4 fields are kept (the hooks)
            for f_ in (os.path.join(FIELDS, x) for x in os.listdir(FIELDS) if x.startswith(f"s{sp}_") and f"_z{z_}_" in x):
                os.remove(f_)

    def retention_fn(keys):
        """MS3's construction of the carrier's retention by halo mass: galaxies (1e13) at the fixed-cell clearing B, then the
        pooled z = 0 medians in L371's bins at MS3's centres."""
        mh = np.concatenate([PER[k_]["Mh"] for k_ in keys]); ee = np.concatenate([PER[k_]["eps"] for k_ in keys])
        B = combine([EST[k_]["all"] for k_ in keys])["B"]
        lx, ly = [math.log10(1e13)], [B]
        for _, b0, b1, cen in MBINS:
            m_ = (mh >= b0) & (mh < b1)
            if m_.any():
                lx.append(math.log10(cen)); ly.append(float(np.median(ee[m_])))
        return (lambda M: float(np.interp(math.log10(M), lx, ly, left=ly[0], right=ly[-1]))), dict(zip([f"{10 ** x:.2e}" for x in lx], ly))

    def gates(keys, cell):
        rows = [PER[k_] for k_ in keys]
        s8 = float(np.mean([r["s8"] for r in rows])); fdev = 0.0
        for z in ("3.0", "2.0"):
            px = sum(r["p1d"][z][0] for r in rows); pl = sum(r["p1d"][z][1] for r in rows); kp = rows[0]["p1d"][z][2]
            m = (kp >= 0.2) & (kp <= 2.0); fdev = max(fdev, float(np.max(np.abs(px[m] / pl[m] - 1))))
        eps = np.concatenate([r["eps_sel"] for r in rows]); med = float(np.median(eps)) if len(eps) else float("nan")
        T = {q: math.sqrt(sum(r["pk"][0][q] for r in rows) / sum(r["pk"][1][q] for r in rows)) for q in KG}
        sh_mock = all(T[q] <= TM[f_][q] for q in KG for f_ in ("canonical", "alt"))
        conv, rcap = HM[cell]; ret, rtab = retention_fn(keys)
        worst = {f_: max(R_of(XLIN, A0M[f_], rcap, conv, ret)[0].values()) for f_ in ("canonical", "alt")}
        sh = all(v <= 1.2 for v in worst.values())
        cl = combine([EST[k_]["all"] for k_ in keys]); byb = {bn: combine([EST[k_][bn] for k_ in keys]) for bn, _, _ in BINS}
        clear = cl["L"] <= 0.30 and cl["B"] <= 0.30
        flags = dict(estimator_dependent=bool((cl["L"] <= 0.30) != (cl["E"] <= 0.30)),
                     galaxy_bin_failure=bool(clear and byb["galaxy"].get("L", 0.0) > 0.30), C_below_half=bool(cl["C"] < 0.5))
        return dict(S8=s8, forest=fdev, eps_cl=med, shear_hm=bool(sh), shear_hm_worstR=worst, shear_mock=bool(sh_mock), T_mock=T,
                    retention_used=rtab, clearing=cl, clearing_by_bin=byb, clear=bool(clear), flags=flags,
                    full=bool(s8 >= 0.922 and fdev <= 0.10 and clear and lo <= med <= hi and sh))

    def line(tag, g):
        c_ = g["clearing"]
        return (f"    {tag}: S8 {g['S8']:.3f} | forest {g['forest']:.3f} | clearing L {c_['L']:.3f} B {c_['B']:.3f} (D {c_['D']:.3f} "
                f"E {c_['E']:.3f} A {c_['A']:.2f} C {c_['C']:.2f}) | X-COP {g['eps_cl']:.3f}"
                f"{'' if lo <= g['eps_cl'] <= hi else (' UNDER' if g['eps_cl'] < lo else ' OVER')} | shear halo-model worst R "
                f"{g['shear_hm_worstR']['canonical']:.2f}/{g['shear_hm_worstR']['alt']:.2f} {'ok' if g['shear_hm'] else 'X'} (mock "
                f"{'ok' if g['shear_mock'] else 'X'})  =>  {'ALL PASS' if g['full'] else 'no'}"
                + (f"  [{', '.join(k_ for k_, v_ in g['flags'].items() if v_)}]" if any(g["flags"].values()) else ""))

    banner("C2  CONTROL: cell (a) at (7, 11) reproduces L388")
    if not MUTATE:
        R88 = json.load(open(os.path.join(HERE, "L388_linear_gate_pooled_results.json")))["numbers"]["table"]["7"]
        dv = []
        for t in TAGS:
            g_ = gates([(7, "matter", t)], "matter")
            dv += [abs(g_["S8"] / R88[t]["S8"] - 1), abs(g_["clearing"]["B"] / R88[t]["clear_fixed"] - 1), abs(g_["eps_cl"] / R88[t]["eps_cl"] - 1)]
        check("C2 cell (a) at (7, 11), 600 and 650 km/s reproduces L388's committed per-box S_8, fixed-cell clearing (B) and X-COP median",
              f"max relative deviation {max(dv):.1e} over {len(dv)} numbers", max(dv) < 1e-9)

    banner("K1, K3  ESTIMATOR CONTROLS on the real (7, 11) LCDM z = 2 fields")
    K = OUT["numbers"]["K"]
    k1 = max(abs(K["K1"][k_] - 1) for k_ in ("A", "B", "C", "D", "E", "Er", "L"))
    check("K1 null: model := LCDM gives every estimator 1 (1e-6)", f"max |estimator - 1| = {k1:.1e}", k1 < 1e-6)
    a_, b_ = K["K3_inplace"], K["K3_shift"]
    ok3 = (max(abs(a_[k_] - a_["truth"]) for k_ in ("B", "D", "E")) < 1e-10
           and abs(b_["E"] - a_["E"]) < 1e-10 and abs(b_["L"] - a_["L"]) < 1e-10 and b_["B"] < a_["B"])
    check("K3 synthetic injection: in place B = D = E = the cell truth (1e-10, A reported); a rigid one-cell shift of the baryons with "
          "their retained carrier leaves E and L unchanged (1e-10) while B drops",
          f"in place truth {a_['truth']:.5f}: A {a_['A']:.5f} B {a_['B']:.5f} D {a_['D']:.5f} E {a_['E']:.5f} L {a_['L']:.5f}; "
          f"shifted: B {b_['B']:.5f} E {b_['E']:.5f} L {b_['L']:.5f}", ok3,
          "L is particle-weighted: it need not equal the cell-weighted truth, and the difference is reported")

    banner("THE GATES PER CELL (cosmic shear on MS3's halo model; clearing rule pooled L <= 0.30 and B <= 0.30)")
    P(f"    X-COP two-sided {lo:.3f}-{hi:.3f}; forest <= 0.10; S8 >= 0.922; shear: worst R <= 1.2 both footings "
      f"(msc: door, cap 1.75 Mpc; curv: upper, uncapped)")
    TAB, WIN = {}, {}
    for cell in CELLS:
        TAB[cell] = {}
        for key, keys_of in [(str(sp), lambda t, sp=sp: [(sp, cell, t)]) for sp, _ in SEEDS] + [("pooled", lambda t: [(sp, cell, t) for sp, _ in SEEDS])]:
            TAB[cell][key] = {}
            for t in TAGS:
                g = gates(keys_of(t), cell); TAB[cell][key][t] = g
                P(line(f"{cell:5s} {key:>6s} {t}", g))
        WIN[cell] = [t for t in TAGS if TAB[cell]["pooled"][t]["full"]]
    for cell in CELLS:
        for t in TAGS:
            P(f"    {cell:5s} pooled {t} clearing by environment: " + "; ".join(
                f"{bn} L {d.get('L', float('nan')):.3f} B {d['B']:.3f} E {d['E']:.3f}" for bn, d in TAB[cell]["pooled"][t]["clearing_by_bin"].items())
              + f"  | retention used: {TAB[cell]['pooled'][t]['retention_used']}")
    EXTRA = {}
    if not MUTATE:
        for cell in ("msc_alt", "matter"):
            for t in TAGS:
                g = gates([(7, cell, t)], cell); EXTRA[f"{cell}/{t}"] = g
                P(line(f"(7, 11) {cell} {t}", g))
    DIAG = {f"{k_[0]}/{k_[1]}/{k_[2]}": dict(v_["sw_diag"] or {}, switched_z0=v_["switched_z0"]) for k_, v_ in PER.items()}
    P("    switch diagnostics (max fraction of would-be-switched cells removed by the cap; max switched fraction): " + "; ".join(
        f"{k_}: capped {d.get('capped_max', 0):.3f}, switched {d.get('switched_max', 0):.4f}" for k_, d in list(DIAG.items())[:6]))
    RB4 = {}
    for cell in CELLS:
        for t in TAGS:
            mh = np.concatenate([PER[(sp, cell, t)]["Mh4"] for sp, _ in SEEDS]); ee = np.concatenate([PER[(sp, cell, t)]["eps4"] for sp, _ in SEEDS])
            RB4[f"{cell}/{t}"] = {nm_: (float(np.median(ee[(mh >= b0) & (mh < b1)])) if ((mh >= b0) & (mh < b1)).any() else None,
                                        int(((mh >= b0) & (mh < b1)).sum())) for nm_, b0, b1, _ in MBINS}
    OUT["numbers"].update(table={c_: {k_: {t: {kk: vv for kk, vv in g.items()} for t, g in d.items()} for k_, d in v.items()} for c_, v in TAB.items()},
                          windows=WIN, extra=EXTRA, switch_diagnostics=DIAG, retention_by_mass_z04=RB4, eps_bounds=dict(lo=lo, hi=hi),
                          C3=dict(computed=c3, committed={f_: K1c[f_]["worst"] for f_ in c3}),
                          per_box_sums={f"{k_[0]}/{k_[1]}/{k_[2]}": v_ for k_, v_ in EST.items()},
                          halos={f"{k_[0]}/{k_[1]}/{k_[2]}": dict(Mh=v_["Mh"], eps=v_["eps"], Mh_z04=v_["Mh4"], eps_z04=v_["eps4"])
                                 for k_, v_ in PER.items()}, fields_dir=os.path.relpath(FIELDS, REPO))
    check("W (informational) per-cell tables, clearing by environment, flags, cell (b), cell (a), the alternative footing, the mock "
          "shear score, the cap's reach, the z = 0.4 retention by mass", "see tables", True, "reported either way", load_bearing=False)

    banner("R_c  THE HYPOTHESIS (set before the run)")
    check("R_c = H_c: cell (c), the MOND-sector switch with the 1.75 Mpc cap, has a pooled window at 600 or 650 km/s (S_8, forest, the "
          "clearing rule, X-COP, cosmic shear on MS3's halo model)", f"pooled window: {WIN['msc'] or 'none'}", bool(WIN["msc"]) == EXPECT_C)
    P(f"    (reported) cell (b), curvature uncapped: pooled window {WIN['curv'] or 'none'} (MS3's X1 predicts none: uncapped fails shear)")

    banner("VERDICT")
    P(f"""  Linear gate (p = 1, x_c0 = 2.5), cells never pooled: MOND-sector + cap (primary) window {WIN['msc'] or 'none'};
  curvature uncapped window {WIN['curv'] or 'none'}.  Fields kept in {os.path.relpath(FIELDS, REPO)}/.  LIMITS: three 100 Mpc/h boxes
  on a 0.39 Mpc/h mesh; the gate a prescribed mask each step (the action-term leak of MS1 is not modelled -- it is why the
  MOND-sector cell is primary); the cap's local form is a construction (MS3); cosmic shear on the halo model is MS3's
  sufficient bound (isolated halos), not a same-volume ray-trace; the trigger posited.""")

    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
    json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
    sys.exit(0 if n_fail == 0 else 1)
