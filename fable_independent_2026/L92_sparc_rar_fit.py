#!/usr/bin/env python3
"""
L92 -- DOES THE F(Q)Theta EXPONENTIAL KERNEL ACTUALLY FIT SPARC GALAXIES?
=========================================================================
The F(Q)Theta completion's galaxy dynamics come from its OWN static-branch field equation

        4 M^2  div[ (1 - e^{-|grad Phi|/a0}) grad Phi ] = rho_b ,

i.e. an AQUAL/QUMOND law with the EXPONENTIAL interpolating function  mu(x) = 1 - e^{-x}.
That kernel is the one that literally descends from the completion (FINDINGS L80/L89 "exponential
carrier").  The repository's registered wide-binary pipeline and THE_ACTION section 3 instead carry
the empirical RAR kernel  nu_RAR(y) = 1/(1 - e^{-sqrt(y)})  (McGaugh/Lelli).  That mismatch is the
standing "D1 kernel conflict".  L89 showed the exponential kernel Newtonises FASTER than nu_RAR at the
external-field scale.  THIS lane asks the foundational question the completion must pass regardless of
D1: does the exponential kernel FIT ACTUAL GALAXY ROTATION CURVES -- the radial acceleration relation --
and how does it rank head-to-head against nu_RAR?

CONVENTION (stated explicitly, because it is the whole point).
  The field equation carries mu as a function of the PHYSICAL field gradient |grad Phi| = g_obs.
  Spherically, div[ mu(g_obs/a0) grad Phi ] = div(grad Phi_N) gives the ALGEBRAIC relation
        mu(x) * x = y ,   x = g_obs/a0 ,   y = g_bar/a0 ,   mu(x) = 1 - e^{-x}.
  This is the "mu in the AQUAL variable" reading and it is the CORRECT one: it has the right
  deep-MOND limit  x -> sqrt(y)  (since mu(x) -> x),  i.e. g_obs -> sqrt(a0 g_bar).  In spherical
  symmetry AQUAL and QUMOND coincide, so the "boost nu(y) = x/y with g_obs = g_bar nu(y)" reading is
  NUMERICALLY IDENTICAL -- we verify that.  The ONLY reading that differs is the naive literal one
  that evaluates mu at the BARYONIC argument, g_obs = g_bar/(1 - e^{-y}); that has the WRONG
  deep-MOND limit (g_obs -> a0, a constant) and is shown here to be catastrophic -- it is a
  documentation trap, not a physical kernel.  Both readings are reported because the brief asks for it.

WHAT IS RUN  (controls first; PASS = the printed statement is TRUE; both a0 footings throughout)
  A  CONTROLS.  (A1) reproduce the carried bounded-boost kernel's RAR scatter 0.145/0.142 dex -- this
     validates the SPARC loading + RAR machinery against L61's committed gate number.  (A2) reproduce
     the exponential-carrier canonical scatter 0.1613 dex quoted in FINDINGS L1087.  (A3) the AQUAL
     implicit solve equals the QUMOND-boost reading to machine precision.  (A4) both kernels share the
     deep-MOND asymptote sqrt(a0 g_bar).
  B  THE EXPONENTIAL KERNEL ON THE FULL MASKED SPARC SAMPLE (155 of 175 curves).  RAR rms + median, both footings.
  C  HEAD-TO-HEAD vs nu_RAR.  Same statistics; the difference; is it comparable (<=0.02 dex) or worse?
  D  THE NAIVE g_bar-VARIABLE READING.  Quantify how badly it breaks (the D1 trap).
  E  THE BTFR.  Deep-MOND V^4 = G M a0 zero-point and scatter under the exponential kernel; note that
     nu_RAR shares the identical zero-point (same deep-MOND limit), so BTFR does NOT discriminate them.
  F  VERDICT.

Self-contained numpy.  Reads only the committed SPARC data.  Imports NOTHING from qwen_claude_field_theory/.
Reads no PREREGISTRATION or *_HASH file.  All printed paths are repo-relative (os.path.relpath).
"""
import numpy as np, math, os, glob

FAILS = []; NCHK = 0
def check(name, ok, detail=""):
    global NCHK; NCHK += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("      " + s, flush=True)
def sec(t): P(); P("=" * 100); P(t); P("=" * 100)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data")
def rel(p): return os.path.relpath(p, REPO)          # never print an absolute machine path

# ---- constants (identical to L61) --------------------------------------------------------------------
G     = 6.674e-11
MSUN  = 1.989e30
kpc   = 3.0857e19
A0    = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FOOT  = ("canonical", "alt")
S_SAT, D_SAT = 2.540, 0.6476                    # the carried bounded-boost kernel (THE_COMPLETE_THEORY sec 4)
UPS_D, UPS_B = 0.5, 0.7

P("=" * 100)
P("L92 -- does the F(Q)Theta EXPONENTIAL kernel mu(x)=1-e^{-x} fit the SPARC radial acceleration relation?")
P("=" * 100)
P(f"a0 footings: canonical {A0['canonical']:.4e} m/s^2,  alt {A0['alt']:.4e} m/s^2   (both carried throughout)")

# ======================================================================================================
# THE KERNELS
# ======================================================================================================
def Delta_boundedboost(s):
    """Carried kernel: saturated nu_RAR.  Delta(s) = s/(e^sqrt(s)-1), capped at D_SAT above S_SAT."""
    s = np.asarray(s, float)
    sc = np.clip(s, 1e-300, S_SAT)
    d = np.where(s > 0, sc / np.expm1(np.sqrt(sc)), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def g_boundedboost(gb, a0):
    return gb + a0 * Delta_boundedboost(gb / a0)

def g_nuRAR(gb, a0):
    """Unsaturated McGaugh/Lelli RAR kernel: g_obs = g_bar / (1 - e^{-sqrt(y)}), y = g_bar/a0."""
    y = gb / a0
    return gb / (-np.expm1(-np.sqrt(y)))          # 1 - e^{-sqrt(y)} = -expm1(-sqrt(y))

def x_exp_AQUAL(y):
    """Solve  x*(1 - e^{-x}) = y  for x = g_obs/a0  (the exponential-carrier AQUAL reading).
    Pure-numpy vectorised Newton.  x >= y always (mu<=1); x -> sqrt(y) deep, x -> y Newtonian."""
    y = np.asarray(y, float)
    x = np.maximum(np.sqrt(y), y)                 # exact-limit initial guess in both regimes
    for _ in range(80):
        e = np.exp(-x)
        f  = x * (1.0 - e) - y                    # = x - x e^{-x} - y
        fp = 1.0 - e * (1.0 - x)                  # d/dx [x - x e^{-x}] = 1 - e^{-x}(1-x)
        step = f / fp
        x = np.clip(x - step, 1e-300, None)
    return x
def g_exp_AQUAL(gb, a0):
    return a0 * x_exp_AQUAL(gb / a0)

def g_exp_literal_gbar(gb, a0):
    """The NAIVE / documentation-trap reading: evaluate mu at the BARYONIC argument.
    g_obs = g_bar/(1 - e^{-y}), y = g_bar/a0.  WRONG deep-MOND limit (g_obs -> a0)."""
    y = gb / a0
    return gb / (-np.expm1(-y))

# ======================================================================================================
sec("PART A -- CONTROLS.  Load SPARC by the L61 recipe; validate the RAR machinery on a committed number.")
# ======================================================================================================

def read_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----")); rows = {}
    for line in lines[last + 1:]:
        f = line.split()
        if len(f) < 18: continue
        try: rows[f[0]] = dict(D=float(f[2]), inc=float(f[5]), L36=float(f[7]), MHI=float(f[13]), Q=int(f[17]))
        except ValueError: continue
    return rows
MASTER = read_master()

GAL = []
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    if name not in MASTER: continue
    m = MASTER[name]
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0] * kpc; Vo = d[:, 1] * 1e3; eV = d[:, 2] * 1e3
    Vg = d[:, 3] * 1e3; Vd = d[:, 4] * 1e3; Vb = d[:, 5] * 1e3
    Vb2 = Vg * np.abs(Vg) + UPS_D * Vd * np.abs(Vd) + UPS_B * Vb * np.abs(Vb)
    msk = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV / np.maximum(Vo, 1) < 0.10)
    if msk.sum() < 3: continue
    Mstar = UPS_D * m["L36"] * 1e9; Mgas = 1.33 * m["MHI"] * 1e9
    GAL.append(dict(name=name, r=r[msk], Vo=Vo[msk],
                    gb=Vb2[msk] / r[msk], go=Vo[msk]**2 / r[msk],
                    Mb=Mstar + Mgas, inc=m["inc"], Q=m["Q"]))
NPT = sum(len(g["r"]) for g in GAL)
info(f"SPARC loaded from {rel(os.path.join(DATA,'sparc_data'))}: {len(GAL)} galaxies, {NPT} points "
     f"(Upsilon_d={UPS_D}, Upsilon_b={UPS_B}, eV/V<0.10, >=3 points)")

GB = np.concatenate([g["gb"] for g in GAL])
GO = np.concatenate([g["go"] for g in GAL])

def rar_stats(gpred_fn, a0):
    res = np.log10(GO / gpred_fn(GB, a0))
    return float(np.sqrt(np.mean(res**2))), float(np.median(res))

# --- A1: reproduce L61's committed bounded-boost gate number ---
P(""); row = {f: rar_stats(g_boundedboost, A0[f]) for f in FOOT}
info(f"carried bounded-boost kernel:  rms {row['canonical'][0]:.4f} / {row['alt'][0]:.4f} dex   "
     f"medians {row['canonical'][1]:+.3f} / {row['alt'][1]:+.3f}   (L61 committed: 0.145/0.142, +0.030/+0.003)")
check("A1  CONTROL: SPARC loading + RAR machinery reproduce L61's bounded-boost gate 0.145/0.142 dex",
      abs(row["canonical"][0] - 0.145) < 0.004 and abs(row["alt"][0] - 0.142) < 0.004
      and abs(row["canonical"][1] - 0.030) < 0.006 and abs(row["alt"][1] - 0.003) < 0.006,
      f"{row['canonical'][0]:.4f}/{row['alt'][0]:.4f} at {row['canonical'][1]:+.3f}/{row['alt'][1]:+.3f}")

# --- A2: reproduce FINDINGS L1087 exponential-carrier canonical number ---
exp_row = {f: rar_stats(g_exp_AQUAL, A0[f]) for f in FOOT}
info(f"exponential carrier (AQUAL):   rms {exp_row['canonical'][0]:.4f} / {exp_row['alt'][0]:.4f} dex   "
     f"medians {exp_row['canonical'][1]:+.3f} / {exp_row['alt'][1]:+.3f}   (FINDINGS L1087: 0.1613 canonical)")
check("A2  CONTROL: the exponential-carrier canonical RAR scatter reproduces FINDINGS L1087's 0.1613 dex",
      abs(exp_row["canonical"][0] - 0.1613) < 0.005,
      f"{exp_row['canonical'][0]:.4f} vs 0.1613")

# --- A3: AQUAL mu-variable reading == QUMOND boost reading (spherical identity) ---
a0 = A0["canonical"]
x = x_exp_AQUAL(GB / a0)
g_from_x   = a0 * x                     # g_obs = a0 * x
nu_boost   = x / (GB / a0)             # nu(y) = x/y
g_from_nu  = GB * nu_boost            # g_obs = g_bar * nu(y)
check("A3  CONTROL: 'mu in AQUAL variable' and 'nu=x/y boost in g_bar variable' are the same relation",
      np.max(np.abs(np.log10(g_from_x / g_from_nu))) < 1e-12,
      f"max |dlog10| = {np.max(np.abs(np.log10(g_from_x/g_from_nu))):.1e} dex")

# --- A4: both physical kernels share the deep-MOND asymptote sqrt(a0 g_bar) ---
# The asymptote is a y->0 statement (both kernels approach it with O(sqrt(y)) corrections), so it must
# be probed at genuinely deep y, not at the y~1 transition where they legitimately differ by ~0.07 dex.
gb_deep = np.array([1e-6, 1e-5, 1e-4]) * a0
dm = np.sqrt(a0 * gb_deep)
err_exp = np.max(np.abs(g_exp_AQUAL(gb_deep, a0) / dm - 1))
err_rar = np.max(np.abs(g_nuRAR(gb_deep, a0)   / dm - 1))
check("A4  CONTROL: exponential AQUAL and nu_RAR both -> sqrt(a0 g_bar) in deep MOND (same BTFR zero-point)",
      err_exp < 0.01 and err_rar < 0.01,
      f"at y<=1e-4: exp within {100*err_exp:.3f}%, nu_RAR within {100*err_rar:.3f}% of sqrt(a0 g_bar)")

# ======================================================================================================
sec("PART B -- THE EXPONENTIAL F(Q)Theta KERNEL ON THE FULL MASKED SPARC SAMPLE (155 of 175 curves) (RAR residuals, both footings).")
# ======================================================================================================
P("")
for f in FOOT:
    r_rms, r_med = exp_row[f]
    info(f"[{f:9s}] exponential kernel g_obs=a0*x with x(1-e^{{-x}})=g_bar/a0:  "
         f"rms {r_rms:.4f} dex, median {r_med:+.4f} dex,  N={len(GB)} points")
check("B1  the exponential kernel produces a finite, MOND-like RAR fit on the full masked sample (rms < 0.20 dex)",
      exp_row["canonical"][0] < 0.20 and exp_row["alt"][0] < 0.20,
      f"{exp_row['canonical'][0]:.4f} / {exp_row['alt'][0]:.4f} dex")

# per-galaxy rms distribution (honest look at the tail)
def pergal_rms(gpred_fn, a0):
    out = []
    for g in GAL:
        res = np.log10(g["go"] / gpred_fn(g["gb"], a0))
        out.append(float(np.sqrt(np.mean(res**2))))
    return np.array(out)
pg_exp = pergal_rms(g_exp_AQUAL, A0["canonical"])
pg_rar = pergal_rms(g_nuRAR,    A0["canonical"])
info(f"per-galaxy rms (canonical): exponential median {np.median(pg_exp):.4f}, 90th pct {np.percentile(pg_exp,90):.4f}; "
     f"nu_RAR median {np.median(pg_rar):.4f}, 90th pct {np.percentile(pg_rar,90):.4f}")

# ======================================================================================================
sec("PART C -- HEAD-TO-HEAD vs nu_RAR (McGaugh/Lelli).  Is the exponential fit comparable or worse?")
# ======================================================================================================
P("")
rar_row = {f: rar_stats(g_nuRAR, A0[f]) for f in FOOT}
P(f"      {'footing':10s} {'nu_RAR rms':>11s} {'exp rms':>9s} {'d(rms)':>8s}   "
  f"{'nu_RAR med':>11s} {'exp med':>9s}")
d_rms = {}
for f in FOOT:
    d_rms[f] = exp_row[f][0] - rar_row[f][0]
    P(f"      {f:10s} {rar_row[f][0]:11.4f} {exp_row[f][0]:9.4f} {d_rms[f]:+8.4f}   "
      f"{rar_row[f][1]:+11.4f} {exp_row[f][1]:+9.4f}")
# point-level maximum divergence between the two kernels (cross-check the D1 0.073 dex number)
maxdiv = np.max(np.abs(np.log10(g_exp_AQUAL(GB, A0['canonical']) / g_nuRAR(GB, A0['canonical']))))
info(f"maximum point-level divergence exp-carrier vs nu_RAR = {maxdiv:.4f} dex "
     f"(FINDINGS D1: 'up to 0.073 dex'); the two kernels are NOT interchangeable")
check("C1  the exponential kernel fits the RAR MEASURABLY WORSE than nu_RAR on BOTH footings",
      d_rms["canonical"] > 0.005 and d_rms["alt"] > 0.005,
      f"exp is worse by {d_rms['canonical']:+.4f}/{d_rms['alt']:+.4f} dex")
comparable = (abs(d_rms["canonical"]) <= 0.02 and abs(d_rms["alt"]) <= 0.02)
check("C2  the gap is within the ~0.01-0.02 dex 'comparable' band (worse, but not a different regime)",
      comparable,
      f"|d(rms)| = {abs(d_rms['canonical']):.4f}/{abs(d_rms['alt']):.4f} dex")
check("C3  CROSS-CHECK: the two kernels diverge by ~0.07 dex at a point (reproduces the D1 number)",
      abs(maxdiv - 0.073) < 0.02, f"{maxdiv:.4f} dex")

# ======================================================================================================
sec("PART D -- THE NAIVE g_bar-VARIABLE READING (the D1 documentation trap).  How badly does it break?")
# ======================================================================================================
P("")
lit_row = {f: rar_stats(g_exp_literal_gbar, A0[f]) for f in FOOT}
for f in FOOT:
    info(f"[{f:9s}] literal g_obs=g_bar/(1-e^{{-g_bar/a0}}):  rms {lit_row[f][0]:.4f} dex, median {lit_row[f][1]:+.4f} dex")
# demonstrate the wrong deep-MOND limit explicitly
gb_t = 1e-3 * A0["canonical"]
info(f"deep-MOND probe (y=1e-3): correct sqrt(a0 g_bar)={math.sqrt(A0['canonical']*gb_t):.3e}, "
     f"AQUAL exp={float(g_exp_AQUAL(np.array([gb_t]),A0['canonical'])[0]):.3e}, "
     f"literal={float(g_exp_literal_gbar(np.array([gb_t]),A0['canonical'])[0]):.3e} (-> a0={A0['canonical']:.3e}, WRONG)")
check("D1  the naive g_bar-variable reading is CATASTROPHIC (rms worse than the correct AQUAL reading)",
      lit_row["canonical"][0] > exp_row["canonical"][0] + 0.05,
      f"literal {lit_row['canonical'][0]:.4f} vs AQUAL {exp_row['canonical'][0]:.4f} dex")

# ======================================================================================================
sec("PART E -- THE BTFR.  Deep-MOND V^4 = G M a0 zero-point and scatter under the exponential kernel.")
# ======================================================================================================
P("")
# V_flat measured PROPERLY: the largest outermost run of >=3 points flat to within 10% of their mean
# (Lelli-style flatness), on the standard BTFR quality cuts Q<3 and inclination >= 30 deg.  Galaxies
# with no flat part are excluded rather than forced.  M/L is FIXED at 0.5 (no per-galaxy nuisance) --
# this, plus the coarse V_flat, is why the scatter below is looser than Lelli 2016's 0.10 dex; it is a
# pipeline systematic, reported as such, and it is IDENTICAL for both kernels.
def vflat_of(Vo, tol=0.10):
    n = len(Vo)
    for k in range(n, 2, -1):
        seg = Vo[-k:]; mu = float(np.mean(seg))
        if np.all(np.abs(seg - mu) / mu < tol): return mu, k
    return None, 0
Vflat = []; Mb = []; gbo = []
for g in GAL:
    if g["Q"] >= 3 or g["inc"] < 30: continue
    vf, k = vflat_of(g["Vo"])
    if vf is None: continue
    Vflat.append(vf); Mb.append(g["Mb"]); gbo.append(float(np.mean(g["gb"][-k:])))
Vflat = np.array(Vflat); Mb = np.array(Mb); gbo = np.array(gbo)
info(f"BTFR sample: {len(Vflat)} galaxies with a flat V_flat (Q<3, inc>=30 deg); M/L fixed at {UPS_D}")

# free-slope BTFR fit  log10(Mb) = alpha*log10(Vflat[km/s]) + beta
lx = np.log10(Vflat / 1e3); ly = np.log10(Mb)
alpha, beta = np.polyfit(lx, ly, 1)
scat_free = float(np.std(ly - (alpha * lx + beta)))
info(f"free-slope BTFR: slope alpha = {alpha:.3f} (deep-MOND predicts 4.00; sub-4 here is a fixed-M/L +"
     f" coarse-V_flat regression effect, not a kernel property), scatter {scat_free:.3f} dex")

# fixed-slope-4 zero-point test V^4 = G Mb a0, both footings
P(f"      {'footing':10s} {'implied a0 [m/s^2]':>18s} {'log d vs footing':>17s} {'zero-pt offset(dex)':>20s} {'rms(dex)':>10s}")
btfr = {}
for f in FOOT:
    a0 = A0[f]
    Mb_pred = (Vflat**4) / (G * a0) / MSUN                       # Msun, from V^4 = G M a0
    resid = np.log10(Mb / Mb_pred)                               # >0 => data heavier than deep-MOND predicts
    a0_impl = 10**float(np.median(np.log10((Vflat**4) / (G * Mb * MSUN))))   # implied a0 from the data
    btfr[f] = (float(np.median(resid)), float(np.sqrt(np.mean(resid**2))), a0_impl)
    P(f"      {f:10s} {a0_impl:18.3e} {math.log10(a0_impl)-math.log10(a0):+17.3f} "
      f"{btfr[f][0]:+20.3f} {btfr[f][1]:10.3f}")
a0_impl = btfr["canonical"][2]
info(f"the data's own deep-MOND normalisation a0 = {a0_impl:.3e} m/s^2 sits {math.log10(a0_impl/A0['canonical']):+.3f} dex"
     f" from canonical and {math.log10(a0_impl/A0['alt']):+.3f} dex from alt")

# DEGENERACY check, stated honestly.  The BTFR ZERO-POINT is the deep-MOND asymptote V^4=G M a0, which
# both kernels share EXACTLY (A4).  But the flat-velocity acceleration is NOT uniformly deep-MOND: the
# highest-mass galaxies' outer points still sit near g_bar ~ a0, where the two kernels legitimately
# differ by up to 0.073 dex.  So the split is: over the genuinely deep-MOND galaxies (which fix the
# zero-point) the kernels are indistinguishable; the transition-regime galaxies carry the only handle.
a0 = A0["canonical"]
div_all  = float(np.max(np.abs(np.log10(g_exp_AQUAL(gbo, a0) / g_nuRAR(gbo, a0)))))
deep = gbo < 0.3 * a0
div_deep = float(np.max(np.abs(np.log10(g_exp_AQUAL(gbo[deep], a0) / g_nuRAR(gbo[deep], a0))))) if deep.any() else 0.0
info(f"exp-vs-nu_RAR difference over the BTFR flat points: worst-case {div_all:.4f} dex; even over the "
     f"{int(deep.sum())} deep-MOND (g_bar<0.3a0) galaxies it is {div_deep:.4f} dex (they converge only as y->0)")
info(f"but the BTFR scatter is {scat_free:.3f} dex, so this {div_all:.3f} dex kernel difference is buried below the noise")

check("E1  a MOND-like power-law BTFR exists under the kernel (slope 3.0 <= alpha <= 4.5)",
      3.0 <= alpha <= 4.5, f"alpha = {alpha:.3f}")
check("E2  the deep-MOND BTFR zero-point recovers a0 to within 0.25 dex of BOTH footings",
      abs(math.log10(a0_impl / A0["canonical"])) < 0.25 and abs(math.log10(a0_impl / A0["alt"])) < 0.25,
      f"implied a0 = {a0_impl:.3e}; {math.log10(a0_impl/A0['canonical']):+.3f}/{math.log10(a0_impl/A0['alt']):+.3f} dex")
check("E3  the BTFR cannot discriminate the kernels: their max BTFR difference is well below the scatter",
      div_all < 0.5 * scat_free,
      f"kernel difference {div_all:.3f} dex vs BTFR scatter {scat_free:.3f} dex (asymptote is identical, A4)")

# ======================================================================================================
sec("PART F -- VERDICT.")
# ======================================================================================================
P("")
info("FOUNDATIONAL QUESTION: does the F(Q)Theta exponential kernel FIT galaxies?  YES -- with the")
info("CORRECT (AQUAL) reading it delivers a MOND-like RAR at ZERO per-galaxy parameters:")
info(f"    exponential kernel:  rms {exp_row['canonical'][0]:.4f} / {exp_row['alt'][0]:.4f} dex   "
     f"(medians {exp_row['canonical'][1]:+.3f} / {exp_row['alt'][1]:+.3f})")
info(f"    nu_RAR (McGaugh):    rms {rar_row['canonical'][0]:.4f} / {rar_row['alt'][0]:.4f} dex")
info(f"    carried boundedboost:rms {row['canonical'][0]:.4f} / {row['alt'][0]:.4f} dex   (= saturated nu_RAR)")
info(f"RANKING: exponential is WORSE than nu_RAR by {d_rms['canonical']:+.4f}/{d_rms['alt']:+.4f} dex -- inside the")
info("~0.01-0.02 'comparable' band, so it FITS, but it is the poorest of the three MOND kernels tested.")
info(f"BTFR: MOND-like power law (slope {alpha:.2f}; sub-4 from fixed M/L + coarse V_flat, not the kernel), "
     f"scatter {scat_free:.2f} dex,")
info(f"deep-MOND zero-point a0 = {a0_impl:.2e} m/s^2 (within {abs(math.log10(a0_impl/A0['alt'])):.2f} dex of alt, "
     f"{abs(math.log10(a0_impl/A0['canonical'])):.2f} of canonical).")
info("The exponential and nu_RAR kernels give the SAME BTFR (identical deep-MOND limit), so galaxies do NOT")
info("decide the D1 kernel conflict -- the external-field / wide-binary scale (L89) does.")
info("The naive g_bar-variable reading (g_obs=g_bar/(1-e^{-y})) is deep-MOND-broken and must never be used.")

P("")
P("=" * 100)
P(f"RESULT: {NCHK - len(FAILS)}/{NCHK} PASS." + ("" if not FAILS else "  FAILURES: " + "; ".join(FAILS)))
P("=" * 100)
raise SystemExit(0 if not FAILS else 1)
