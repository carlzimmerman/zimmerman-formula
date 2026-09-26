#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
GP4 -- THE GENERATED PHANTOM WITH A FREE-STREAMING CARRIER: does GP1's kernel (bound baryons only, screened at lambda)
plus L319's kicked, Lambda-triggered carrier pass KiDS, cosmic shear, X-COP, the galaxies, S_8 and the forest together?

WHY.  GP3: the phantom KiDS needs, ADDED to an LCDM-like matter field, over-produces the lensing power at k ~ 0.5-1 h/Mpc
(2-3x).  But the phantom's OWN power is only 0.2-0.75 of LCDM's there (measured on GP3's mock against P_NL), so it can
REPLACE the dark component's small-scale power if the carrier stops clustering on those scales by the lens epoch.  L364
(committed, the parallel session's region kernel) scored exactly that replacement with L319's carrier -- kicked daughters
that free-stream -- and found a near miss (one gate, KiDS on the alt footing).  GP1's kernel differs: its phantom is
screened at lambda instead of cut at a region's edge, so its lensing power, its KiDS profile and its cluster phantom are
different numbers.  This lane scores GP1's kernel with L319's carrier on L364's gates, from committed machinery only.

MACHINERY (loaded unedited; nothing re-derived):
  * GP3's nonlinear mock (z = 0.5): s^2(k) = P_ph/P_NL and the matter-phantom correlation r_x(k) for GP1's kernel at
    lambda = 0.7, 1, 1.5, 2 Mpc, both footings;
  * L364's committed carrier scan (L319's solver): the lens-epoch transfer T(k, z = 0.5) of the total matter (it carries
    the daughters' free streaming), the forest T^2(k = 5) at z = 3 and 2, S_8, and S(z_l = 0.25), the fraction of the
    carrier that has not decayed at the KiDS lens epoch;
  * GP2's KiDS machinery (BK1's, Lagrangian form, the construction's own external field, observed reading) with the
    carrier's surviving halo fixed at S(z_l) x (1 - f_b) NFW(M200) of each bin's Moster+13 host (L355/L360's template;
    kernel-invisible, so it adds linearly);
  * L354's X-COP and galaxy machinery (L321's 12 clusters and three hosts, the carrier's retained fraction under
    Newtonian orbits -- independent of the kernel), with the OBSERVABLE replaced by GP1's: at radius R
        g_obs = g_b + L_R s(R) [nu(sqrt((s g_b)^2 + e^2)/a0) - 1] g_b + g_c,   s = (1 + R/lam) e^(-R/lam),
    e = 1e-4 a0 (GP2's bound-baryon field; L321/L354's 0.01-0.02 a0 is the whole web's), and L_R the Lagrangian
    re-screening factor at R (GP1 N2/N3) computed for a central point mass.
COSMIC SHEAR (GP3's gate, L364's formula):  R(k) = T^2 + 2 r_x T s + s^2 <= 1.2 on k = 0.1-1 h/Mpc, both footings.
PRE-DECLARED GATES (L364's, unchanged): forest strict T^2(k=5) >= 0.9952 at z = 3 and 2 (loose 0.9); S_8 >= 0.767
(strict) / 0.748 (alt); X-COP |M_dyn/M_HSE - 1| <= 0.2 (strict) / after the 6% non-thermal support (alt), both footings;
galaxies <= 0.06 dex (both footings); KiDS Delta chi^2 <= +4 against the unswitched isolated-MOND + 2-halo base (L352's
acceptance, as L360/L364), both footings; cosmic shear as above.  Strict set = strict forest, S_8 and X-COP; alt set =
loose forest, alt S_8 and alt X-COP; KiDS, cosmic shear and galaxies are the same in both.

CHECKS
  C1 CONTROL: with T = 1 (no decay) the cosmic-shear ratio equals GP3's R_cons for the same kernel (to 1e-9).
  C2 CONTROL: with L354's own observable (unscreened, e = 0.01 a0) the machinery reproduces L364's committed X-COP ratios
     for the shared carrier cells (to 0.005).
  C3 CONTROL: with no carrier halo (f_s = 0) the KiDS score reproduces GP2's committed W5 numbers (to 0.1).
  W1 THE WINDOW: some (lambda, carrier cell) passes every gate on the strict or the alt set.
  W2 (documentary) the scan; the nearest miss by normalised margin; which gates block.
MUTATE=1 turns the free streaming off (T = 1: the decayed carrier keeps its small-scale power, so the phantom adds
instead of replacing).  If W1 finds a window, MUTATE must close it (rc = 1).
(Record: the first launch computed R from s^2 and r_x interpolated separately at the gate's k, so C1 differed from
 GP3's per-bin R_cons by 1e-2; it was stopped and R is now built per bin, in GP3's order.)
SCOPE.  One lens epoch for cosmic shear (z = 0.5, P(k) not a projected xi+-); r_x held at its full-matter value (L364's
approximation); the carrier's halo around KiDS lenses is the uniformly surviving fraction (daughters at >= 800 km/s
leave galaxy halos); the cluster L_R from a point mass; lambda remains a free length (BK2).

Run from the repository root:  python3 real_research/generated_phantom_2026/GP4_generated_phantom_plus_kicked_carrier.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore")
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "GP4_generated_phantom_plus_kicked_carrier"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "GP4", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


def load(path, split, name):
    """exec a committed lane's machinery (everything before `split`), unedited, with its MUTATE forced off."""
    src = open(path).read().split(split)[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    ns = {"__name__": name, "__file__": path}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, ns)
    return ns


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: no free streaming (T = 1): the phantom adds instead of replacing ***")
LAMS = [0.7, 1.0, 1.5, 2.0]
FOOTS = ("canonical", "alt")
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)

# ---------------------------------------------------------------------------------- L364's carrier scan (committed)
L364 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))
CELLS = L364["numbers"]["scan"]
P(f"  L364 carrier scan loaded: {len(CELLS)} cells (f_d(0) x v_k)   [{time.time() - T0:.0f}s]")

# ---------------------------------------------------------------------------------- GP3: s^2 and r_x for GP1's kernel
G3 = load(os.path.join(HERE, "GP3_lensing_power_and_growth.py"),
          "# ============================================================================================ M1 control", "gp3")
SH = {}
for foot in FOOTS:
    for lam in LAMS:
        ms = G3["measure"](G3["MK"], lam, A0[foot])
        kh = ms["kh"]; Pnl = G3["PNL_of"](kh)
        s2 = ms["Ppp"] / Pnl; rx = ms["Pxx"] / np.sqrt(np.maximum(ms["Pmm"] * ms["Ppp"], 1e-300))
        _, _, Rc, _ = G3["ratios"](ms)
        SH[(foot, lam)] = {"kh": kh, "s2_bin": s2, "rx_bin": rx, "Rc_bin": Rc,
                           "s2": {q: float(np.interp(q, kh, s2)) for q in KG}, "rx": {q: float(np.interp(q, kh, rx)) for q in KG},
                           "Rcons": {q: float(np.interp(q, kh, Rc)) for q in KG}}
del G3
P(f"  GP3 mock measured for lambda {LAMS}   [{time.time() - T0:.0f}s]")


def shear_R(sh, T05, T_on=True):
    """R(k) = T^2 + 2 r_x T s + s^2 on the mock's k bins (T interpolated in log k from L364's six values), then read at
    the gate's k -- the same order as GP3's R_cons, so T = 1 reproduces it exactly."""
    kh = sh["kh"]
    if T_on:
        lk = np.log([float(q) for q in KG]); Tv = np.array([T05[str(q)] for q in KG])
        T = np.interp(np.log(kh), lk, Tv)
    else:
        T = np.ones_like(kh)
    sb = np.sqrt(np.maximum(sh["s2_bin"], 0.0))
    Rb = T * T + 2 * sh["rx_bin"] * T * sb + sb * sb
    return {q: float(np.interp(q, kh, Rb)) for q in KG}


# ============================================================================================ C1
banner("C1  CONTROL: T = 1 reproduces GP3's R_cons for the same kernel")
c1 = max(abs(shear_R(SH[(f, l)], None, T_on=False)[q] - SH[(f, l)]["Rcons"][q]) for f in FOOTS for l in LAMS for q in KG)
P(f"    max |R(T = 1) - R_cons| = {c1:.1e}")
OUT["numbers"]["C1"] = c1
check("C1 CONTROL: with T = 1 the cosmic-shear ratio is GP3's R_cons (1e-9)", f"{c1:.1e}", c1 < 1e-9)

# ---------------------------------------------------------------------------------- L354: X-COP + galaxies machinery
L54 = load(os.path.join(REPO, "real_research", "dark_sector_2026", "L354_carrier_lagrangian_additive_window.py"),
           "# ============================================================================================ C1 control", "l354")
Lm = L54["Lm"]; retained, cl_ratio, CL, GAL = L54["retained"], L54["cl_ratio"], L54["CL"], L54["GAL"]
cl_ref, cl_mass_fn, GE_CL, GE_GAL = L54["cl_ref"], L54["cl_mass_fn"], L54["GE_CL"], L54["GE_GAL"]
hernquist, c200_dm14, NT = L54["hernquist"], L54["c200_dm14"], L54["NT"]
Gk, KPC_M = Lm["Gk"], Lm["KPC_M"]
P(f"  L354 machinery loaded ({len(CL)} X-COP clusters, {len(GAL)} galaxy hosts)   [{time.time() - T0:.0f}s]")
E_GP = 1e-4                                                            # the construction's own external field (units of a0)

# Lagrangian re-screening factor at R for a central point mass (GP1 N2 / GP2's shell kernel)
def shell_frac(r, rp, lam):
    em = np.exp(-rp / lam)
    IB = lam * em * (lam - np.exp(-r / lam) * (r + lam))
    IA_in = lam * (np.exp(np.minimum(r - rp, 0.0) / lam) * (r - lam) + lam * em)
    IA_rp = lam * ((rp - lam) + lam * em)
    IA_out = IA_rp + lam * ((rp + lam) - np.exp(-np.maximum(r - rp, 0.0) / lam) * (r + lam))
    return (np.where(r <= rp, IA_in, IA_out) - IB) / (2 * lam * rp)


RGK = np.geomspace(1.0, 60000.0, 1500)                                   # kpc
LR_CACHE = {}


def L_R(Mb, R, lam_mpc, a0k):
    key = (round(math.log10(Mb), 3), round(R, 1), lam_mpc, round(a0k, 6))
    if key in LR_CACHE: return LR_CACHE[key]
    lam = lam_mpc * 1e3
    s = (1 + RGK / lam) * np.exp(-RGK / lam); gb = Gk * Mb / RGK ** 2
    Mph = Mb * s * (Lm["nu"](np.maximum(s * gb / a0k, 1e-14)) - 1)
    dM = np.diff(Mph, prepend=0.0)
    PL = shell_frac(RGK[:, None], RGK[None, :], lam)
    MphL = Mph - PL @ dM
    val = float(np.interp(R, RGK, MphL) / np.interp(R, RGK, Mph))
    LR_CACHE[key] = val
    return val


def g_gp(gb, gc, R, Mb, lam_mpc, a0k):
    """GP1's observable at radius R (kpc): screened phantom with the Lagrangian factor, small external field."""
    lam = lam_mpc * 1e3; s = (1 + R / lam) * math.exp(-R / lam)
    nu_ = float(Lm["nu"](math.sqrt((s * gb) ** 2 + (E_GP * a0k) ** 2) / a0k))
    return gb + L_R(Mb, R, lam_mpc, a0k) * (nu_ - 1) * s * gb + gc


def xcop_gp(eps, lam_mpc, foot):
    a0k = A0[foot] * KPC_M / 1e6
    rat = []
    for cl in CL:
        R = cl["R500"]; gb = Gk * cl["Mb"] / R ** 2; gc = Gk * eps * cl["Mcarr"] / R ** 2
        rat.append(g_gp(gb, gc, R, cl["Mb"], lam_mpc, a0k) * R ** 2 / Gk / cl["Mhse"])
    med = float(np.median(rat)); return med, med * (1 - NT)


def gal_gp(eps_by_host, lam_mpc, foot):
    a0k = A0[foot] * KPC_M / 1e6; out = {}
    for kh, h_ in GAL.items():
        Mb_fn = hernquist(h_["Mb"], h_["a"]); Mn, r200, rs = Lm["nfw"](h_["M200"], c200_dm14(h_["M200"]))
        r = h_["rg"]; gb = Gk * float(Mb_fn(r)) / r ** 2
        gc = Gk * eps_by_host[kh] * (1 - Lm["FB"]) * float(Mn(r)) / r ** 2
        out[kh] = math.log10(g_gp(gb, gc, r, h_["Mb"], lam_mpc, a0k) / g_gp(gb, 0.0, r, h_["Mb"], lam_mpc, a0k))
    return out


EPS, EPSG = {}, {}
for c in CELLS:
    fd, vk = c["fd"], c["vk"]
    Lm["A0"] = A0["canonical"] * KPC_M / 1e6
    EPS[(fd, vk)] = float(retained(cl_mass_fn, cl_ref["M200"], cl_ref["c"], cl_ref["R500"], GE_CL, "newtonian", vk, fd, rhoc=cl_ref["rhoc"])[0])
    EPSG[(fd, vk)] = {kh: float(retained(hernquist(h_["Mb"], h_["a"]), h_["M200"], c200_dm14(h_["M200"]), h_["rg"], GE_GAL,
                                         "newtonian", vk, fd)[0]) for kh, h_ in GAL.items()}
P(f"  retained carrier fractions (Newtonian orbits, kernel-independent) computed for {len(EPS)} cells   [{time.time() - T0:.0f}s]")

# ============================================================================================ C2
banner("C2  CONTROL: L354's own observable (unscreened, e = 0.01 a0) reproduces L364's committed X-COP ratios")
dev2 = 0.0
for c in CELLS:
    for foot in FOOTS:
        Lm["A0"] = A0[foot] * KPC_M / 1e6
        med = float(np.median([cl_ratio(cl, EPS[(c["fd"], c["vk"])], "additive") for cl in CL]))
        dev2 = max(dev2, abs(med - c["xcop"][foot][0]))
P(f"    max |ratio - L364| = {dev2:.1e}")
OUT["numbers"]["C2"] = dev2
check("C2 CONTROL: the X-COP machinery reproduces L364's committed ratios (0.005)", f"{dev2:.1e}", dev2 < 5e-3)

# ---------------------------------------------------------------------------------- GP2: KiDS machinery (observed reading)
G2 = load(os.path.join(HERE, "GP2_kids_bound_source_kernel.py"),
          "# ============================================================================================ W1-W3", "gp2")
fit_gen, DATA, REF, rr, MPCm, MS = G2["fit_gen"], G2["DATA"], G2["REF"], G2["rr"], G2["MPCm"], G2["MS"]
esd_from_M, Rd, npb, SEL = G2["esd_from_M"], G2["Rd"], G2["npb"], G2["SEL"]
GP0 = G2["GP0"]; ZL = G2["ZL"]
LOGMS = [10.0, 10.45, 10.70, 10.90]                                     # typical log M* of the four bins (L355)
M200s = [10 ** brentq(lambda lm: math.log10(GP0.moster_Mstar(10 ** lm, ZL)) - ls, 10.5, 15.5) for ls in LOGMS]
h = 0.6736
rho_c_z = GP0.RHO_CRIT0 * (GP0.Om * (1 + ZL) ** 3 + GP0.OL)
c200 = lambda M: 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h)))   # Dutton & Maccio 2014 (as L355, GP2)


def nfw_M(M200, r_mpc):
    cc = c200(M200); r200 = (3 * M200 / (4 * math.pi * 200 * rho_c_z)) ** (1 / 3); rs = r200 / cc
    mm = lambda s_: np.log(1 + s_) - s_ / (1 + s_)
    return M200 * mm(np.minimum(r_mpc, r200) / rs) / mm(cc)


TCAR = []
for b in range(4):
    Mc = (1 - GP0.FB) * nfw_M(M200s[b], rr / MPCm) * MS
    Rq, dS = esd_from_M(Mc + 1.0, 1.0, 0.0); TCAR.append(np.interp(Rd[b], Rq, dS))
TAB = {}
for foot in FOOTS:
    for lam in LAMS:
        TAB[(foot, lam)] = G2["table_from_samples"](G2["FIELD"][("observed", lam)] / A0[foot], A0[foot], lam)
P(f"  GP2 KiDS tables built (observed reading, Lagrangian form)   [{time.time() - T0:.0f}s]")


def kids(foot, lam, fs):
    dat = [d - fs * t for d, t in zip(DATA, TCAR)]
    return fit_gen(TAB[(foot, lam)], dat, 2.0)[0] - REF[foot]["iso_all"], fit_gen(TAB[(foot, lam)], dat, 2.0, SEL)[0] - REF[foot]["iso_in"]


# ============================================================================================ C3
banner("C3  CONTROL: no carrier halo reproduces GP2's committed W5 (L352-acceptance) numbers")
gp2r = json.load(open(os.path.join(HERE, "GP2_kids_bound_source_kernel_results.json")))
w5 = gp2r["numbers"]["W5"]["observed"]
dev3 = max(abs(kids(f, l, 0.0)[0] - w5[str(l)][i]) for i, f in enumerate(FOOTS) for l in LAMS)
P(f"    max |Delta chi^2 - GP2 W5| = {dev3:.2e}")
OUT["numbers"]["C3"] = dev3
check("C3 CONTROL: with no carrier halo the KiDS score is GP2's committed W5 (0.1)", f"{dev3:.2e}", dev3 < 0.1)

# ============================================================================================ the scan
banner("THE SCAN: every lambda x carrier cell, every gate, both footings")
FOREST_STRICT = 0.9952; FOREST_LOOSE = 0.9; S8_STRICT, S8_ALT = 0.767, 0.748
ROWS = []
KCACHE = {}
for lam in LAMS:
    for c in CELLS:
        fd, vk = c["fd"], c["vk"]; key = (fd, vk)
        sh = {f: shear_R(SH[(f, lam)], c["T05"], T_on=not MUTATE) for f in FOOTS}
        sh_worst = {f: max(sh[f].values()) for f in FOOTS}
        fs = c["S_zl"]
        if (lam, fs) not in KCACHE: KCACHE[(lam, fs)] = {f: kids(f, lam, fs) for f in FOOTS}
        kd = KCACHE[(lam, fs)]
        xc = {f: xcop_gp(EPS[key], lam, f) for f in FOOTS}
        gl = {f: max(gal_gp(EPSG[key], lam, f).values()) for f in FOOTS}
        forest = min(c["t3"], c["t2"])
        row = {"lam": lam, "fd": fd, "vk": vk, "S_zl": fs, "shear": sh_worst, "kids": {f: kd[f][0] for f in FOOTS},
               "kids_in03": {f: kd[f][1] for f in FOOTS}, "xcop": xc, "gal": gl, "S8": c["S8"], "forest": forest}
        ok = {}
        for st in ("strict", "alt"):
            ok[st] = {
                "shear": all(sh_worst[f] <= 1.2 for f in FOOTS),
                "kids": all(kd[f][0] <= 4.0 for f in FOOTS),
                "xcop": all(abs(xc[f][0 if st == "strict" else 1] - 1) <= 0.2 for f in FOOTS),
                "gal": all(gl[f] <= 0.06 for f in FOOTS),
                "S8": c["S8"] >= (S8_STRICT if st == "strict" else S8_ALT),
                "forest": forest >= (FOREST_STRICT if st == "strict" else FOREST_LOOSE)}
        row["ok"] = ok
        # normalised exceedance (alt set) for the nearest-miss ranking
        ex = {"shear": max(0.0, max(sh_worst.values()) - 1.2) / 0.2, "kids": max(0.0, max(kd[f][0] for f in FOOTS) - 4.0) / 4.0,
              "xcop": max(0.0, max(abs(xc[f][1] - 1) for f in FOOTS) - 0.2) / 0.2, "gal": max(0.0, max(gl.values()) - 0.06) / 0.06,
              "S8": max(0.0, S8_ALT - c["S8"]) / 0.02, "forest": max(0.0, FOREST_LOOSE - forest) / 0.1}
        row["exceed_alt"] = ex; row["margin_alt"] = sum(ex.values())
        ROWS.append(row)
    P(f"    lambda {lam}: " + "; ".join(
        f"f_d {r['fd']} v_k {r['vk']:.0f}: shear {r['shear']['canonical']:.2f}/{r['shear']['alt']:.2f}, KiDS {r['kids']['canonical']:+.1f}/{r['kids']['alt']:+.1f}, "
        f"X-COP(NT) {r['xcop']['canonical'][1]:.2f}/{r['xcop']['alt'][1]:.2f}"
        for r in ROWS if r["lam"] == lam and r["vk"] in (1000.0, 1200.0) and r["fd"] in (0.9, 0.95)) + f"   [{time.time() - T0:.0f}s]")
OUT["numbers"]["scan"] = [{k: (v if not isinstance(v, dict) else {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()})
                           for k, v in r.items()} for r in ROWS]

# ============================================================================================ W1 / W2
banner("W1  THE WINDOW: every gate, strict or alternative threshold set")
WIN = {st: [(r["lam"], r["fd"], r["vk"]) for r in ROWS if all(r["ok"][st].values())] for st in ("strict", "alt")}
block = {}
for r in ROWS:
    for g, v in r["ok"]["alt"].items():
        if not v: block[g] = block.get(g, 0) + 1
near = sorted(ROWS, key=lambda r: r["margin_alt"])[:5]
P(f"    strict window: {WIN['strict']}")
P(f"    alt window:    {WIN['alt']}")
P(f"    gates failed across the scan (alt set): {block}")
for r in near:
    P(f"    near: lambda {r['lam']} f_d {r['fd']} v_k {r['vk']:.0f} (margin {r['margin_alt']:.2f}): shear {r['shear']['canonical']:.2f}/{r['shear']['alt']:.2f}, "
      f"KiDS {r['kids']['canonical']:+.1f}/{r['kids']['alt']:+.1f}, X-COP {r['xcop']['canonical'][0]:.2f}({r['xcop']['canonical'][1]:.2f})/"
      f"{r['xcop']['alt'][0]:.2f}({r['xcop']['alt'][1]:.2f}), galaxies {max(r['gal'].values()):+.3f}, S_8 {r['S8']:.3f}, forest {r['forest']:.4f}; "
      f"fails (alt): {[g for g, v in r['ok']['alt'].items() if not v]}")
OUT["numbers"]["W1"] = {"strict": WIN["strict"], "alt": WIN["alt"], "blocking_alt": block,
                        "nearest": [{k: r[k] for k in ("lam", "fd", "vk", "margin_alt", "shear", "kids", "S8", "forest")} | {"xcop": {f: list(v) for f, v in r["xcop"].items()}, "fails_alt": [g for g, v in r["ok"]["alt"].items() if not v]} for r in near]}
check("W1 THE WINDOW: some (lambda, carrier cell) passes forest, S_8, X-COP, galaxies, KiDS and cosmic shear together "
      "(strict or alternative set), both footings", f"strict {WIN['strict']}; alt {WIN['alt']}",
      len(WIN["strict"]) + len(WIN["alt"]) > 0, "")
check("W2 (documentary) the nearest misses and the blocking gates",
      {f"lam {r['lam']} fd {r['fd']} vk {r['vk']:.0f}": [g for g, v in r["ok"]["alt"].items() if not v] for r in near},
      True, "", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
if WIN["strict"] or WIN["alt"]:
    P(f"""  A WINDOW (alt set: {WIN['alt']}; strict: {WIN['strict']}).  GP1's generated phantom, screened at lambda, with L319's kicked,
  free-streaming carrier passes KiDS isolated lensing, cosmic shear, X-COP, the galaxies' RAR gate, S_8 and the forest together
  on the named threshold set.  The phantom replaces the carrier's small-scale lensing power instead of adding to it.""")
else:
    P(f"""  NO WINDOW.  Blocking gates (alt set): {block}.  Nearest miss: lambda {near[0]['lam']} Mpc, f_d(0) {near[0]['fd']}, v_k {near[0]['vk']:.0f}.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} ({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
