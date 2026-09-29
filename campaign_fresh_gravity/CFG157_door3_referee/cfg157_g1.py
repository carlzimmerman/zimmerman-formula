#!/usr/bin/env python3
"""cfg157_g1 -- CFG157: independent re-derivation of CFG121 T1.1 / T1.2 / T1.5 (G1: single polarisation law vs the CFG44 target).
Frozen: CFG157_FROZEN_CRITERIA.md.  MUTATE=sign|kernel|target for the controls.  Exit: main 0 (all integrity checks pass), 2 (integrity fail);
MUTATE: 1 when the named control bites as declared, 0 when it does not (kept and disclosed).
README numbers below are TARGETS READ before deriving, not blind predictions."""
import os, sys, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg157_common import *

MUTATE = os.environ.get("MUTATE", "")
assert MUTATE in ("", "sign", "kernel", "target")
TAG = "" if not MUTATE else "_MUTATE_" + MUTATE
OUT = os.path.join(HERE, "cfg157_g1%s.out" % TAG)
JS = os.path.join(HERE, "cfg157_g1%s_results.json" % TAG)
T = Tee(OUT)
P = T.P
README_T12 = {1e9: 1.31, 1e10: 1.02, 1e11: 0.43, 1e12: 0.063}     # CFG121 README, canonical a0
README_T15 = {1e9: 1.46, 1e10: 1.40, 1e11: 1.19, 1e12: 0.62}
README_DIGIT = {1e9: 0.005, 1e10: 0.005, 1e11: 0.005, 1e12: 0.0005}   # half unit of the last printed digit
LINE = 0.10
def tol(M, tgt):
    return max(0.02 * tgt, README_DIGIT[M])

kern = "simple" if MUTATE == "kernel" else "P2"
sgn = -1.0 if MUTATE == "sign" else 1.0
mtar = "total" if MUTATE == "target" else None
P("CFG157 G1  (repo files printed as <repo>-relative; MUTATE=%s: kernel=%s sign=%+d target=%s)" % (MUTATE or "none", kern, sgn, "total-mass (constant charge)" if mtar else "enclosed mass (CFG44)"))
P("nu_mono is RECONSTRUCTED: RAR kernel up to y_m = %.6f, then y(nu-1) held at %.6f (see cfg157_common.py)." % (Y_M, C_M))
P("README numbers are targets read before deriving; my hand estimates in the frozen file were made after reading them.\n")

def dev_arrays(sph, kernel, a0, G, x, sg=1.0, mt=None, route="chain"):
    r = x * rM(sph.mtot(), a0, G)
    f = {"chain": route_chain, "fd": route_fd, "sympy": route_sympy}[route]
    return f(sph, kernel, sg, a0, G, r, mt) - 1.0

results = {"mutate": MUTATE, "footings": {}}
x121, x2001 = grid_x(121), grid_x(2001)

# ------------------------------------------------------------------ integrity checks
P("=== integrity checks (abort exit 2 on failure in the main run) ===")
a0c = A0["canonical"]
# (b) enclosed mass vs numerical integral, and total
from scipy.integrate import quad
okb = True
for M in MASSES:
    sph = ExpSphere(M * MSUN, h_of_M(M))
    for s in (0.05, 0.5, 2.0, 10.0, 40.0):
        r = s * sph.h
        num = quad(lambda t: 4 * math.pi * t * t * sph.rho(t), 0, r, epsabs=0, epsrel=1e-12, limit=200)[0]
        okb &= abs(num / sph.m(r) - 1) < 1e-8
    okb &= abs(sph.m(200 * sph.h) / sph.M - 1) < 1e-12
T.check("(b) M_b(<r) closed form = quad of rho_b (1e-8), M_b(<inf)=M_b", okb)
# (a) point mass identity, analytic and fd
pm = PointMass(1e11 * MSUN)
xs = grid_x(121, 0.1, 30)
rp = xs * rM(pm.M, a0c, G_CFG121)
pa = route_chain(pm, "P2", 1.0, a0c, G_CFG121, rp) - 1
pf = route_fd(pm, "P2", 1.0, a0c, G_CFG121, rp) - 1
ps = route_sympy(pm, "P2", 1.0, a0c, G_CFG121, rp) - 1
P("  (a) point-mass, P2, +, enclosed-mass target: max|ratio-1| analytic %.3e, fd %.3e, sympy %.3e" % (abs(pa).max(), abs(pf).max(), abs(ps).max()))
pm_dev = {}
for k, ker in (("P2", "P2"), ("used", kern)):
    d = route_chain(pm, ker, sgn if k == "used" else 1.0, a0c, G_CFG121, rp, mtar if k == "used" else None) - 1
    pm_dev[k] = float(abs(d).max())
if not MUTATE:
    T.check("(a) point-mass identity 1e-9 analytic / 1e-6 fd", abs(pa).max() <= 1e-9 and abs(pf).max() <= 1e-6 and abs(ps).max() <= 1e-9)
else:
    P("  (a) [control] point-mass max|ratio-1| with the mutated model: %.4f (identity %s)" % (pm_dev["used"], "HOLDS" if pm_dev["used"] <= 1e-6 else "BROKEN"))
# (c) three routes agree, on all masses, both footings; (d) closed form; (f) grid; (g) constants
okc = okd = okf = okg = True
worst_c = worst_d = 0.0
for fname, a0 in A0.items():
    for M in MASSES:
        sph = ExpSphere(M * MSUN, h_of_M(M))
        d1 = dev_arrays(sph, kern, a0, G_CFG121, x121, sgn, mtar, "chain")
        d2 = dev_arrays(sph, kern, a0, G_CFG121, x121, sgn, mtar, "fd")
        d3 = dev_arrays(sph, kern, a0, G_CFG121, x121, sgn, mtar, "sympy")
        e = max(np.max(np.abs(d1 - d2) / (np.abs(d1) * 1e-5 + 1e-9)), np.max(np.abs(d1 - d3) / (np.abs(d1) * 1e-5 + 1e-9)))
        worst_c = max(worst_c, e)
        okc &= e <= 1.0
        if not MUTATE or MUTATE == "target":
            cf = closed_form_P2(sph, a0, G_CFG121, x121 * rM(sph.M, a0, G_CFG121)) - 1
            if MUTATE == "target":
                cf = (cf + 1) * sph.m(x121 * rM(sph.M, a0, G_CFG121)) / sph.M - 1
            worst_d = max(worst_d, np.max(np.abs(cf - d1)))
        d2001 = dev_arrays(sph, kern, a0, G_CFG121, x2001, sgn, mtar, "chain")
        okf &= abs(abs(d2001).max() / abs(d1).max() - 1) < 0.005
        if fname == "canonical":
            d4 = dev_arrays(sph, kern, a0, G_ALT, x121, sgn, mtar, "chain")
            g_eff = abs(d4).max() / abs(d1).max() - 1
            okg &= abs(g_eff) < 1e-3
T.check("(c) three derivative routes (chain rule / 5-pt FD / sympy) agree to 1e-5 relative (+1e-9 abs); worst scaled err %.2e" % worst_c, okc)
if not MUTATE or MUTATE == "target":
    T.check("(d) closed form 1+(dln m/dln r)B(y) = numerical ratio to 1e-6 (abs); worst %.2e" % worst_d, worst_d < 1e-6)
T.check("(f) 121 -> 2001 points changes max dev < 0.5%", okf)
T.check("(g) G of CFG121 vs 4.30091727e-6 kpc(km/s)^2/Msun changes max dev < 1e-3 relative", okg)

# ------------------------------------------------------------------ T1.2 / T1.5
P("\n=== T1.2 (exponential spheres, chi = P2 kernel, NO refit) and T1.5 (reconstructed nu_mono) ===")
verdict12, verdict15 = {}, {}
for fname, a0 in A0.items():
    P("\n-- footing %s: a0 = %.4e m/s^2" % (fname, a0))
    rec = {"T12": {}, "T15": {}, "beta": {}}
    for M in MASSES:
        sph = ExpSphere(M * MSUN, h_of_M(M))
        rm = rM(sph.M, a0, G_CFG121)
        beta = sph.h / rm
        d = dev_arrays(sph, kern, a0, G_CFG121, x121, sgn, mtar, "chain")
        i = int(np.argmax(np.abs(d)))
        dm = dev_arrays(sph, "mono", a0, G_CFG121, x121, 1.0, None, "chain") if not MUTATE else None
        rec["T12"][str(M)] = {"maxdev": float(abs(d)[i]), "x_at_max": float(x121[i]), "mindev": float(d.min()), "beta_h_over_rM": beta,
                              "dev_at_x": {("%g" % xx): float(np.interp(math.log(xx), np.log(x121), d)) for xx in (0.1, 0.3, 1, 3, 10, 30)}}
        line = "  M=%.0e h=%g kpc r_M=%.3f kpc (h/r_M=%.3f): T1.2 max|dev|=%.4f at x=%.3f; min dev=%+.4f; dev(x=0.1,0.3,1,3,10,30)=%s" % (
            M, h_of_M(M) / KPC, rm / KPC, beta, abs(d)[i], x121[i], d.min(), " ".join("%+.4f" % rec["T12"][str(M)]["dev_at_x"][k] for k in ("0.1", "0.3", "1", "3", "10", "30")))
        P(line)
        if dm is not None:
            j = int(np.argmax(np.abs(dm)))
            rec["T15"][str(M)] = {"maxdev": float(abs(dm)[j]), "x_at_max": float(x121[j]), "mindev": float(dm.min()), "ratio_max": float(1 + dm.max())}
            P("     T1.5 (reconstructed nu_mono): max|dev|=%.4f at x=%.3f (max ratio %.4f, min ratio %.4f)" % (abs(dm)[j], x121[j], 1 + dm.max(), 1 + dm.min()))
        rec["beta"][str(M)] = beta
    results["footings"][fname] = rec
# verdicts vs README (canonical)
P("\n=== comparison with CFG121 README (canonical footing), pass lines of the frozen file ===")
can = results["footings"]["canonical"]
allok = True
for M in MASSES:
    mine = can["T12"][str(M)]["maxdev"]
    ok = abs(mine - README_T12[M]) <= tol(M, README_T12[M])
    vm = "PASS" if mine <= LINE else "FAIL"
    vr = "PASS" if README_T12[M] <= LINE else "FAIL"
    P("  T1.2 M=%.0e: mine %.4f vs README %.3g (tol +-%.4f) -> %s; door verdict mine %s vs README %s" % (M, mine, README_T12[M], tol(M, README_T12[M]), "REPRODUCES" if ok else "DISAGREES", vm, vr))
    allok &= ok and vm == vr
if not MUTATE:
    P("  T1.2 headline: %s" % ("REPRODUCES" if allok else "DISAGREES"))
    ok15 = True
    for M in MASSES:
        mine = can["T15"][str(M)]["maxdev"]
        ok = abs(mine - README_T15[M]) <= tol(M, README_T15[M]) if M in README_T15 else False
        ok15 &= ok
        P("  T1.5 M=%.0e: mine %.4f vs README %.3g -> %s" % (M, mine, README_T15[M], "REPRODUCES" if ok else "DISAGREES (nu_mono reconstructed; see README)"))
    P("  T1.5 headline (conditional on the reconstruction): %s" % ("REPRODUCES" if ok15 else "DISAGREES/NOT-CONFIRMED"))
    # point mass R(1) for the reconstructed nu_mono (CFG44 quotes R(x=1)=1.46)
    y1 = 1.0
    R1 = float(-2 * y1 * y1 * nu_mono(y1) * dnu_mono(y1))
    P("  point-mass charge function R(x=1) with the reconstructed nu_mono: %.4f (CFG44 README: 1.46)" % R1)
    results["R_pm_x1_mono"] = R1
    # section-3 identities
    P("\n=== section-3 identities (frozen file) ===")
    okI = True
    okI &= T.check("(i) point mass ratio identically 1 (see integrity check (a))", abs(pa).max() <= 1e-9)
    minall, argx = 1e9, {}
    for fname, a0 in A0.items():
        for M in MASSES:
            sph = ExpSphere(M * MSUN, h_of_M(M))
            d = dev_arrays(sph, "P2", a0, G_CFG121, x121, 1.0, None, "chain")
            minall = min(minall, d.min())
            argx[(fname, M)] = float(x121[np.argmax(d)])
    T.check("(ii-a) deviation >= 0 everywhere on the grid (min over masses and footings %.3e)" % minall, minall >= -1e-12)
    T.check("(ii-b) maximum at the grid edge x=0.1 for every mass and footing", all(abs(v - 0.1) < 1e-9 for v in argx.values()), str({("%s,%.0e" % k): round(v, 4) for k, v in argx.items()}))
    # NOTE: the first run sampled x=1e-6, 1e-5 with a 0.02 tolerance; for 1e12 the deep limit is reached later (y ~ x, dev(1e-6)=1.474): a poor sample point of MY
    # check, not a physics disagreement (cfg157_g1_firstrun.out kept). The limit is now checked as a sequence x = 1e-6, 1e-9, 1e-12.
    lim = []
    seq_ok = True
    for M in MASSES:
        sph = ExpSphere(M * MSUN, h_of_M(M))
        xs = np.array([1e-6, 1e-9, 1e-12])
        dd = dev_arrays(sph, "P2", a0c, G_CFG121, xs, 1.0, None, "chain")
        seq_ok &= bool(dd[0] < dd[1] < dd[2] < 1.5)
        lim.append(dd[2])
    T.check("(ii-c) deviation -> 1.5 (ratio 2.5) as r -> 0, increasing along x = 1e-6, 1e-9, 1e-12; at x=1e-12: %s" % ", ".join("%.5f" % v for v in lim), seq_ok and all(abs(v - 1.5) < 0.005 for v in lim))
    results["deviation_limit_r0"] = [float(v) for v in lim]
    # monotone decrease of the deviation with x
    mono = True
    for M in MASSES:
        sph = ExpSphere(M * MSUN, h_of_M(M))
        d = dev_arrays(sph, "P2", a0c, G_CFG121, x2001, 1.0, None, "chain")
        mono &= bool(np.all(np.diff(d) <= 1e-12))
    T.check("(ii-d) deviation decreases monotonically with x on [0.1,30] (2001 points)", mono)
    results["T12_verdict"] = "REPRODUCES" if allok else "DISAGREES"
    results["T15_verdict"] = "REPRODUCES" if ok15 else "NOT-CONFIRMED"

# ------------------------------------------------------------------ controls
bite = None
if MUTATE:
    P("\n=== MUTATE=%s control ===" % MUTATE)
    base = {}
    for M in MASSES:
        sph = ExpSphere(M * MSUN, h_of_M(M))
        d0 = dev_arrays(sph, "P2", a0c, G_CFG121, x121, 1.0, None, "chain")
        base[M] = float(abs(d0).max())
    cur = {M: can["T12"][str(M)]["maxdev"] for M in MASSES}
    for M in MASSES:
        P("  M=%.0e: main max dev %.4f -> mutated %.4f (x%.2f); verdict %s -> %s" % (M, base[M], cur[M], cur[M] / base[M], "PASS" if base[M] <= LINE else "FAIL", "PASS" if cur[M] <= LINE else "FAIL"))
    P("  point-mass identity: main %.2e -> mutated %.4f" % (pm_dev["P2"], pm_dev["used"]))
    if MUTATE == "sign":
        bite = pm_dev["used"] > LINE and cur[1e12] > LINE
        P("  declared: point-mass dev >= 1.5 (analytic 2/nu at x=0.1 ~ 2): observed %.4f -> %s" % (pm_dev["used"], "as declared" if pm_dev["used"] >= 1.5 else "NOT as declared"))
    elif MUTATE == "kernel":
        moved = max(abs(cur[M] / base[M] - 1) for M in MASSES)
        bite = pm_dev["used"] > LINE and moved > 0.10
        P("  declared: point-mass dev >= 0.5 at x=0.1: observed %.4f; max relative move of a T1.2 number %.3f" % (pm_dev["used"], moved))
    else:
        bite = cur[1e12] > LINE and pm_dev["used"] <= 1e-6
        P("  declared: |dev| ~ 0.9-1.0 at all masses; 1e12 PASS -> FAIL; point-mass identity intact (%.2e)" % pm_dev["used"])
    P("  CONTROL %s" % ("BITES (exit 1)" if bite else "DOES NOT BITE (exit 0, kept and disclosed)"))
    results["bite"] = bool(bite)
    results["mutated_maxdev"] = {str(M): cur[M] for M in MASSES}
    results["point_mass_maxdev"] = pm_dev

results["integrity_fails"] = T.fails
results["verdict_note"] = "Nothing here says the theory is closed or that data favour the framework; a pass of the point-mass identity is a positive control."
json.dump(results, open(JS, "w"), indent=1)
P("\nwrote %s and %s" % (os.path.basename(OUT), os.path.basename(JS)))
T.close()
if MUTATE:
    # integrity failures of the checks that the mutation is supposed to break are not aborts
    sys.exit(1 if bite else 0)
sys.exit(2 if T.fails else 0)
