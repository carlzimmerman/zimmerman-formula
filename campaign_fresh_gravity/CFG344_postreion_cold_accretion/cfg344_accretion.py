#!/usr/bin/env python3
"""CFG344 -- post-reionisation cold accretion onto reionisation-fossil satellites (M_V > -7.7), scored per object with CFG317's
committed harness (rule S, V1/V2, both footings). Frozen: FROZEN_CRITERIA.md (8cb772fc5).
Growth: Correa+15 median MAH M(z) = M0 (1+z)^alpha exp(beta z), inverted so that M(z_f) = M_cool(z_f) (CFG343), then M_c = M(z_inf).
Run from the repository root:  python3 campaign_fresh_gravity/CFG344_postreion_cold_accretion/cfg344_accretion.py
CFG344_MUTATE=1: z_inf = z_f (no post-reionisation growth), separate _MUTATE outputs."""
import os, sys, io, math, json, contextlib, time
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG344_MUTATE", "0") == "1"; SLUG = "cfg344_accretion" + ("_MUTATE" if MUTATE else "")
LOG, CH, OUT = [], [], {"lane": "CFG344", "frozen": "8cb772fc5", "mutate": MUTATE, "checks": {}}
T0 = time.time()


def P(s=""):
    print(s, flush=True); LOG.append(s)


def check(n, v, ok):
    CH.append(bool(ok)); OUT["checks"][n] = {"ok": bool(ok), "measured": str(v)}; P(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")


# ---------------------------------------------------------------- M_cool from CFG343 (read-only import of its function)
src343 = open(os.path.join(LANES, "CFG343_atomic_cooling_floor", "cfg343_cooling.py")).read()
ns343 = {"__file__": os.path.join(LANES, "CFG343_atomic_cooling_floor", "cfg343_cooling.py")}
exec(compile(src343[:src343.index("def fnum")], "cfg343_prefix", "exec"), ns343)
m_cool = ns343["m_cool"]                     # Msun, T_vir 1e4 K, mu 1.22

# ---------------------------------------------------------------- Correa+15 median accretion history (colossus planck18, EH98)
from colossus.cosmology import cosmology
from colossus.lss import peaks
COS = cosmology.setCosmology("planck18"); h = COS.H0 / 100.0
dDdz0 = float(COS.growthFactor(0.0, derivative=1))   # analytic derivative; a 1e-4 finite difference hits colossus's table noise (-0.84, bug in run 1)


def S(M):                                    # sigma^2(M), M in Msun
    return COS.sigma(peaks.lagrangianR(M * h), 0.0) ** 2


def f_of(M0):
    lm = math.log10(M0); zt = -0.0064 * lm ** 2 + 0.0237 * lm + 1.8837; q = 4.137 * zt ** -0.9476
    return (S(M0 / q) - S(M0)) ** -0.5


def ab(M0):
    f = f_of(M0); return (1.686 * math.sqrt(2 / math.pi) * dDdz0 + 1.0) * f, -f


def M_of(z, M0):
    a, b = ab(M0); return M0 * (1 + z) ** a * math.exp(b * z)


def M0_from(Mz, z):
    return 10 ** brentq(lambda l: math.log10(M_of(z, 10 ** l)) - math.log10(Mz), math.log10(Mz) - 0.5, math.log10(Mz) + 6, xtol=1e-12)


check("C0 dD/dz|0 matches -Omega_m^0.55 within 2%", f"{dDdz0:.4f} vs {-COS.Om(0.0) ** 0.55:.4f}", abs(dDdz0 / -COS.Om(0.0) ** 0.55 - 1) < 0.02)
# C2: mean accretion rate of a 1e12 Msun halo at z = 0 vs Fakhouri+10 mean 46.1 Msun/yr (PROVISIONAL)
a12, b12 = ab(1e12); H0yr = COS.H0 / 977.792 / 1e9
rate = -(a12 + b12) * 1e12 * H0yr
zhalf = brentq(lambda z: M_of(z, 1e12) - 5e11, 0.01, 5)
check("C2 Correa+15 dM/dt(1e12 Msun, z=0) within x1.5 of Fakhouri+10 mean 46.1 Msun/yr (PROVISIONAL)", f"{rate:.1f} Msun/yr (z_1/2 = {zhalf:.2f})",
      46.1 / 1.5 <= rate <= 46.1 * 1.5)
OUT["C2"] = {"rate": rate, "zhalf_1e12": zhalf, "dDdz0": dDdz0}

ZF0, ZINF0, ZRE0 = 8.0, 2.0, 7.0
MF = 1e9                                     # filtering mass (Gnedin 2000, PROVISIONAL)
CASES = [(8.0, 8.0)] if MUTATE else [(8.0, 2.0), (6.0, 2.0), (10.0, 2.0), (8.0, 1.0), (8.0, 3.0)]
HIST = {}
P(f"\nCFG344{' MUTATE (z_inf = z_f)' if MUTATE else ''}: Correa+15 MAH, colossus planck18, dD/dz|0 = {dDdz0:.4f}")
inv_err, mono = 0.0, True
for zf in sorted({c[0] for c in CASES}):
    Mc = m_cool(zf); M0 = M0_from(Mc, zf); a, b = ab(M0)
    inv_err = max(inv_err, abs(M_of(zf, M0) / Mc - 1))
    zz = np.linspace(0, zf, 200); mm = np.array([M_of(z, M0) for z in zz]); mono &= bool(np.all(np.diff(mm) < 0))
    HIST[zf] = {"M_cool": Mc, "M0": M0, "alpha": a, "beta": b, "M": {str(z): M_of(z, M0) for z in (1.0, 2.0, 3.0, 6.0, 7.0, 8.0, zf)}}
    P(f"  z_f {zf:4.1f}: M_cool {Mc:.3e} -> M0 {M0:.3e} (alpha {a:.3f}, beta {b:.3f}); M(z=3,2,1) = {M_of(3, M0):.3e}, {M_of(2, M0):.3e}, {M_of(1, M0):.3e}; "
      f"M(z_re 6/7/8) = {M_of(6, M0):.2e}/{M_of(7, M0):.2e}/{M_of(8, M0):.2e}")
check("C3 inversion M(z_f) = M_cool to 1e-8 and M(z) monotone over 0..z_f", f"max rel err {inv_err:.1e}; monotone {mono}", inv_err < 1e-8 and mono)
OUT["HIST"] = HIST

# ---------------------------------------------------------------- CFG317's harness (read-only exec up to its scans)
p317 = os.path.join(LANES, "CFG317_baryon_loss_cold_mass", "cfg317_baryon_loss.py")
src317 = open(p317).read(); src317 = src317[:src317.index('R.banner("(A)')]
N17 = {"__file__": p317, "__name__": "cfg317_prefix"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src317, "cfg317_prefix", "exec"), N17)
if _e is not None:
    os.environ["MUTATE"] = _e
NS313, SC, CFG, FB0 = N17["ns"], N17["SC"], N17["CFG"], N17["FB0"]
NEED317 = json.load(open(os.path.join(LANES, "CFG317_baryon_loss_cold_mass", "cfg317_baryon_loss_results.json")))["numbers"]["NEED"]
TARGET = {}


def make_mc344(committed_fn):                # per-object M_c = max(M_b/f_b, M(z_inf)) for fossils; R = 1 otherwise
    def hook(Ms, colour, Mb):
        m0 = Mb / (FB0 * CFG["fbx"]); t = TARGET.get(float(Ms))
        mc = m0 if t is None else max(m0, t); SC["cur"] = mc / m0
        return mc
    return hook


NS313["make_mc"] = N17["make_mc317"] = make_mc344
SC.update(mode="perobj", lookup={}, R=1.0, cur=1.0)    # mc_native -> R = 1 (SLUGGS/SPARC); floor uses SC["cur"]
FOOTS, PROFS = ("canonical", "alt"), ("nfw", "sis")
ROWS = ["P1", "P2a", "P2b", "P2c", "P2d"]
SAT = {"ufd": "P1", "cls": "P2a", "col": "P2b", "m31": "P2c", "fld": "P2d"}


def score():
    out = {}
    for prof in PROFS:
        b, n45 = N17["run"](prof); out[prof] = N17["extract"](b)
    return out, n45


# R = 1 baseline (TARGET empty)
BASE, N45 = score()
P(f"\n  R = 1 baseline done ({time.time() - T0:.0f} s)")
c1 = max(max(abs(BASE[p][r][f][0] - NEED317[f"{p}|{f}|{r}"]["s"][0]), abs(BASE[p][r][f][1] - NEED317[f"{p}|{f}|{r}"]["z"][0]))
         for p in PROFS for f in FOOTS for r in ROWS)
check("C1 R = 1 reproduces CFG317's baseline (P1, P2a-d; V1/V2; both footings) to 1e-6", f"max |diff| {c1:.1e}", c1 < 1e-6)
ELAW = {p: {f: BASE[p]["P1"][f][0] / BASE[p]["P1"][f][1] for f in FOOTS} for p in PROFS}
P("  e_law(R=1) [UFD, from s/z]: " + "; ".join(f"{p} {f} {ELAW[p][f]:.4f} (2e {2 * ELAW[p][f]:.4f})" for p in PROFS for f in FOOTS))
OUT["ELAW"] = ELAW; OUT["BASE"] = {p: {r: BASE[p][r] for r in ROWS} for p in PROFS}

UPS = N45["UPS_V"]; SMP = N17["samples"](N45); UL = list(N45["UL"])
LVCUT = 10 ** (0.4 * (4.83 + 7.7))
POPS = {k: list(v) for k, v in SMP.items()}; POPS["ufd"] = POPS["ufd"] + UL
fossil = {k: [d for d in v if d["LV"] < LVCUT] for k, v in POPS.items()}
P("  fossils (M_V > -7.7) per population: " + "; ".join(f"{k} {len(fossil[k])}/{len(POPS[k])}" for k in POPS) + "  (fld: reported, NOT grown -- non-fossil by class)")
OUT["n_fossil"] = {k: [len(fossil[k]), len(POPS[k])] for k in POPS}
fld_keys = {float(UPS * d["LV"]) for d in POPS["fld"]}


def ufd_R(Mt):
    return [max(1.0, FB0 * Mt / (UPS * d["LV"] + 1.33 * d.get("MHI", 0.0))) for d in POPS["ufd"]]


RUNS = {}
for zf, zinf in CASES:
    Mt = M_of(zinf, HIST[zf]["M0"])
    TARGET.clear()
    for k in ("ufd", "cls", "col", "m31"):
        for d in fossil[k]:
            TARGET[float(UPS * d["LV"])] = Mt
    coll = sorted(TARGET.keys() & fld_keys)
    res, _ = score()
    R = np.array(ufd_R(Mt)); lr = np.log10(R)
    cap = {str(zre): int(M_of(zre, HIST[zf]["M0"]) > MF) * len(fossil["ufd"]) for zre in (6.0, 7.0, 8.0)}
    key = f"zf{zf:g}_zinf{zinf:g}"
    RUNS[key] = {"M_target": Mt, "median_logR_ufd": float(np.median(lr)), "logR_ufd_p16_p84": [float(np.percentile(lr, 16)), float(np.percentile(lr, 84))],
                 "logR_ufd_min_max": [float(lr.min()), float(lr.max())], "cap_violations_ufd": cap, "fld_key_collisions": len(coll),
                 "rows": {p: {r: res[p][r] for r in ROWS} for p in PROFS},
                 "reported_rows": {p: {r: v for r, v in res[p].items() if r not in ROWS} for p in PROFS}}
    P(f"\n  z_f {zf:g}, z_inf {zinf:g}: M_c(fossil) = {Mt:.3e} Msun; UFD median log R_acc {np.median(lr):.3f} (R = {10 ** np.median(lr):.0f}; "
      f"16-84% {np.percentile(lr, 16):.2f}-{np.percentile(lr, 84):.2f}); cap violations (M(z_re) > 1e9) z_re 6/7/8: {cap['6.0']}/{cap['7.0']}/{cap['8.0']} of {len(fossil['ufd'])}; "
      f"fld collisions {len(coll)}  ({time.time() - T0:.0f} s)")
    for p in PROFS:
        for f in FOOTS:
            s, z = res[p]["P1"][f]; s0 = BASE[p]["P1"][f][0]
            oth = " ".join(f"{r} {res[p][r][f][0]:+.3f}(z{res[p][r][f][1]:+.2f})" for r in ROWS[1:])
            P(f"    {p:3s} {f:9s}: UFD {s:+.3f} (z {z:+.2f}; base {s0:+.3f}; 2e {2 * ELAW[p][f]:.3f})  | {oth}")


def verdict(rows):
    ok_o = all(abs(rows[p][r][f][1]) < 2 for p in PROFS for f in FOOTS for r in ROWS[1:])
    res_ = all(abs(rows[p]["P1"][f][0]) <= 2 * ELAW[p][f] for p in PROFS for f in FOOTS)
    par = all(-2 * ELAW[p][f] <= rows[p]["P1"][f][0] <= 0.5 * BASE[p]["P1"][f][0] for p in PROFS for f in FOOTS)
    return ("RESOLVES" if (res_ and ok_o) else "PARTIAL" if (par and ok_o) else "NOT"), ok_o


prim = f"zf{CASES[0][0]:g}_zinf{CASES[0][1]:g}"
V, okO = verdict(RUNS[prim]["rows"])
for k in RUNS:
    RUNS[k]["verdict"] = verdict(RUNS[k]["rows"])[0]
P("\n  bracket verdicts (reported): " + "; ".join(f"{k} {RUNS[k]['verdict']}" for k in RUNS))
OUT["RUNS"] = RUNS; OUT["verdict"] = V; OUT["others_ok"] = okO
OUT["logR_need"] = {f"{p}|{f}": NEED317[f"{p}|{f}|P1"]["lr0"] for p in PROFS for f in FOOTS}
if MUTATE:
    s = RUNS[prim]["rows"]["nfw"]["P1"]["canonical"][0]
    check("MUTATE: z_inf = z_f gives NOT and V1 canonical UFD offset within 0.05 dex of CFG343's +0.322", f"{V}; {s:+.3f}", V == "NOT" and abs(s - 0.322) < 0.05)
P(f"\n{'MUTATE (z_inf = z_f) ' if MUTATE else ''}VERDICT (primary {prim}): {V}")
P(f"\n{sum(CH)}/{len(CH)} checks pass ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1, default=float)
raise SystemExit(0 if all(CH) else 1)
