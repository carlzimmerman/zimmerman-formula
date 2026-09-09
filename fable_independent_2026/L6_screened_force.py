#!/usr/bin/env python3
"""
L6 -- the screened-force door: can a density- or potential-dependent force supply the cluster residual?
=======================================================================================================
L5 closed a SINGLE FINITE-RANGE force of fixed strength: it fits the cluster shape at 0.064 dex but wants
lambda = 14 kpc (which puts ~1 dex into the radial acceleration relation) and its strength IS the
cosmological Newton constant (G_cosmo/G_local = 9.2, 41x the BBN bound).  L5 explicitly did NOT close the
adjacent door: a SCREENED force -- chameleon, symmetron, Vainshtein, any mechanism whose strength depends
on a local variable -- where the cluster and cosmological values are decoupled by construction.  This is
that test, and it is the last structural candidate for the cluster residual.

WHAT A SCREENING MECHANISM IS, operationally.  A monotone function S(X) of ONE local screening variable X:
fully screened (no enhancement, S = 1) at one end, fully unscreened (S = S_max) at the other.  The
candidates in the literature are X = the Newtonian potential depth (chameleon, symmetron), the local
density (density-dependent couplings), the acceleration, or the enclosed mass / Vainshtein radius.

THE TWO WAYS IT CAN DIE, both tested here.
(1) OVERLAP.  If clusters and galaxies occupy the SAME range of X but require DIFFERENT enhancement, no
    single-valued S(X) exists.  Where the two populations do not overlap in X, this test is VACUOUS and
    is reported as such -- a non-overlapping variable is NOT excluded by this argument.
(2) THE COSMOLOGICAL ORDERING.  The homogeneous background sits BEYOND cluster outskirts in every
    candidate variable: lower density, shallower potential, smaller acceleration, no enclosed mass.  A
    monotone S that unscreens clusters relative to galaxies therefore unscreens the BACKGROUND at least
    as much, so G_cosmo >= G_cluster ~ 7 G_local, and BBN excludes it -- the same kill as L5, reached
    without assuming a range.  This is the general argument; it does not care which X is chosen.

The enhancement tested is the one a screened force would have to supply ON TOP of the framework's own
kernel, E = g_obs / [g_bar + a0 Delta(g_bar/a0)] with nu_RAR saturated (THE_ACTION section 3): E = 1 means
the kernel already suffices (galaxies), E > 1 means it does not (clusters).

  S0 [control]     in bins of the ACCELERATION g_bar the test reproduces L2's kill (clusters require more
                   than galaxies at the same g_bar).  A screening function of acceleration IS a kernel, so
                   this must fail for the machinery to be trusted;
  S1 [potential]   overlap in Phi_loc = g_bar * r, and whether E agrees there;
  S2 [density]     overlap in the enclosed-mass gradient density rho_b = (dM/dr)/(4 pi r^2), and whether E agrees;
  S3 [mass]        overlap in enclosed baryonic mass M_b(<r), and whether E agrees;
  S4 [cosmology]   the ordering test: is the homogeneous background beyond cluster outskirts in EVERY
                   candidate variable?  If yes, monotone screening cannot decouple G_cosmo from G_cluster;
  S5 [verdict]     the screened-force route survives overlap AND the cosmological ordering.
Both a0 footings.  FAIL marks a requirement the route does not meet.  A PASS on S5 would be the first live
mechanism for the cluster residual in this programme and is the outcome most worth finding.

CAVEAT, direction stated: rho_b for SPARC uses the spherical-equivalent (dM/dr)/(4 pi r^2), which
UNDERSTATES a disc's true local density.  That makes the density overlap in S2 an UPPER bound on the real
overlap -- correcting it separates the populations further, it cannot merge them.
"""
import numpy as np, math, json, os, sys, glob
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22
H0 = 0.674*100e3/Mpc; Om, Ob = 0.315, 0.049; rho_c = 3*H0**2/(8*math.pi*G)
print("=" * 118); print("L6 -- the screened-force door: can a density- or potential-dependent force supply the cluster residual?"); print("=" * 118, flush=True)

def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
def g_kernel(g_bar, a0): return g_bar + a0*Delta(g_bar/a0)

# ---------------- clusters ----------------
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
A0 = CLJ["a0_m_s2"]
CL = {}
for rw in CLJ["rows"]:
    foot = rw.get("footing", "canonical"); a0 = A0[foot]
    r = float(rw["r_kpc"])*kpc; gb = float(rw["g_baryon_over_a0"])*a0; gh = float(rw["g_hse_over_a0"])*a0
    CL.setdefault(foot, {}).setdefault(rw["cluster"], []).append((r, gb, gh))
CLU = {}
for foot, cls in CL.items():
    rows = []
    for name, pts in cls.items():
        p = np.array(sorted(pts)); r, gb, gh = p[:, 0], p[:, 1], p[:, 2]
        M = gb*r**2/G
        rho = np.gradient(M, r)/(4*math.pi*r**2)
        for i in range(len(r)):
            if rho[i] <= 0: continue
            rows.append(dict(r=r[i], gb=gb[i], gh=gh[i], M=M[i], phi=gb[i]*r[i], rho=rho[i],
                             E=gh[i]/g_kernel(gb[i], A0[foot])))
    CLU[foot] = rows
    print(f"    clusters, {foot}: {len(rows)} usable rows; E = g_HSE/g_kernel median {np.median([x['E'] for x in rows]):.2f}", flush=True)

# ---------------- SPARC ----------------
UPS_D, UPS_B = 0.5, 0.7
gal = []
for fn in sorted(glob.glob(os.path.join(REPO, "real_research/data/sparc_data", "*_rotmod.dat"))):
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0]*kpc; Vo = d[:, 1]*1e3; eV = d[:, 2]*1e3; Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    m = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV/np.maximum(Vo, 1) < 0.10)
    if m.sum() < 3: continue
    r, Vo, Vb2 = r[m], Vo[m], Vb2[m]
    gb = Vb2/r; go = Vo**2/r; M = gb*r**2/G
    rho = np.gradient(M, r)/(4*math.pi*r**2)
    for i in range(len(r)):
        if rho[i] <= 0: continue
        gal.append(dict(r=r[i], gb=gb[i], go=go[i], M=M[i], phi=gb[i]*r[i], rho=rho[i]))
print(f"    SPARC: {len(gal)} points (Upsilon_d = {UPS_D}, Upsilon_b = {UPS_B}, eV/V < 0.10)", flush=True)

# ---------------- the overlap machinery ----------------
def overlap_test(var, foot, nbin=6):
    a0 = A0[foot]; cl = CLU[foot]
    xc = np.array([x[var] for x in cl]); Ec = np.array([x["E"] for x in cl])
    xg = np.array([x[var] for x in gal]); Eg = np.array([x["go"]/g_kernel(x["gb"], a0) for x in gal])
    lo = max(xc.min(), xg.min()); hi = min(xc.max(), xg.max())
    if not (hi > lo): return None, 0.0, []
    frac = float(((xc >= lo) & (xc <= hi)).mean())
    edges = np.geomspace(lo, hi, nbin + 1); out = []
    for i in range(nbin):
        mc = (xc >= edges[i]) & (xc < edges[i + 1]); mg = (xg >= edges[i]) & (xg < edges[i + 1])
        if mc.sum() < 3 or mg.sum() < 5: continue
        c_m = float(np.median(Ec[mc])); g_m = float(np.median(Eg[mg]))
        c_se = float(np.std(Ec[mc], ddof=1)/math.sqrt(mc.sum())); g_se = float(np.std(Eg[mg], ddof=1)/math.sqrt(mg.sum()))
        z = (c_m - g_m)/math.hypot(max(c_se, 1e-9), max(g_se, 1e-9))
        out.append(dict(lo=edges[i], hi=edges[i + 1], nc=int(mc.sum()), ng=int(mg.sum()), Ec=c_m, Eg=g_m, z=z, ratio=c_m/max(g_m, 1e-9)))
    return (lo, hi), frac, out
def report(var, label, unit=""):
    worst = 0.0; anybin = False
    for foot in sorted(CLU):
        rng, frac, out = overlap_test(var, foot)
        if rng is None or not out:
            print(f"    {label} {foot}: NO usable overlap between clusters and SPARC -> this variable is NOT tested by the overlap argument")
            continue
        anybin = True
        print(f"    {label} {foot}: overlap {rng[0]:.3g}-{rng[1]:.3g}{unit}, {100*frac:.0f}% of cluster rows inside")
        for b in out:
            print(f"        {b['lo']:9.3g}-{b['hi']:9.3g}  n_cl {b['nc']:3d} n_gal {b['ng']:4d}   E_cluster {b['Ec']:5.2f}   E_galaxy {b['Eg']:5.2f}   ratio {b['ratio']:4.2f}   z {b['z']:+6.1f}")
            worst = max(worst, abs(b["z"]))
    return anybin, worst
print("\n  S0 control -- screening in the ACCELERATION (this IS a kernel; must fail):")
ok0, z0 = report("gb", "S0 g_bar", " m/s^2")
check("S0 [control] in bins of acceleration the machinery reproduces L2's kill: clusters require more than galaxies at the SAME g_bar",
      ok0 and z0 > 3, f"worst |z| = {z0:.1f}" if ok0 else "no overlap -- machinery could not be validated")
print("\n  S1 -- screening in the POTENTIAL (chameleon, symmetron):")
ok1, z1 = report("phi", "S1 Phi_loc", " m^2/s^2")
check("S1 [potential] clusters and galaxies at the same potential depth require the SAME enhancement, so a potential-screened force is admissible",
      ok1 and z1 < 3, f"worst |z| = {z1:.1f}" if ok1 else "no overlap -- NOT excluded by this argument")
print("\n  S2 -- screening in the DENSITY:")
ok2, z2 = report("rho", "S2 rho_b", " kg/m^3")
check("S2 [density] clusters and galaxies at the same baryon density require the SAME enhancement, so a density-screened force is admissible",
      ok2 and z2 < 3, f"worst |z| = {z2:.1f}" if ok2 else "no overlap -- NOT excluded by this argument (see S4, which does not need overlap)")
print("\n  S3 -- screening in the ENCLOSED MASS (Vainshtein-like):")
ok3, z3 = report("M", "S3 M_b(<r)", " kg")
check("S3 [mass] clusters and galaxies at the same enclosed baryonic mass require the SAME enhancement, so a mass-screened force is admissible",
      ok3 and z3 < 3, f"worst |z| = {z3:.1f}" if ok3 else "no overlap -- NOT excluded by this argument")

# ---------------- S4: the cosmological ordering ----------------
print("\n  S4 -- the cosmological ordering (does not need overlap):")
rho_cos_b = Ob*rho_c; rho_cos_m = Om*rho_c
beyond = {}
for foot in sorted(CLU):
    cl = CLU[foot]
    out_rows = sorted(cl, key=lambda x: -x["r"])[:max(3, len(cl)//10)]
    rho_out = float(np.median([x["rho"] for x in out_rows])); phi_out = float(np.median([x["phi"] for x in out_rows]))
    gb_out = float(np.median([x["gb"] for x in out_rows])); E_out = float(np.median([x["E"] for x in out_rows]))
    beyond[foot] = dict(rho=rho_cos_b < rho_out, phi=True, gb=True, rho_out=rho_out, phi_out=phi_out, gb_out=gb_out, E_out=E_out)
    print(f"    {foot}: cluster outskirts  rho_b = {rho_out:.2e} kg/m^3, Phi_loc = {phi_out:.2e} m^2/s^2, g_bar = {gb_out:.2e} m/s^2, E = {E_out:.2f}")
    print(f"           cosmic background  rho_b = {rho_cos_b:.2e} kg/m^3 ({rho_out/rho_cos_b:.0f}x LOWER), Phi_loc -> 0, g_bar -> 0 (homogeneous)")
allbeyond = all(b["rho"] and b["phi"] and b["gb"] for b in beyond.values())
Emax = max(b["E_out"] for b in beyond.values())
print(f"    => a monotone S(X) that unscreens clusters relative to galaxies unscreens the BACKGROUND at least as much,")
print(f"       so G_cosmo/G_local >= E(cluster outskirts) = {Emax:.2f}; BBN allows |G/G_0 - 1| < 0.2, i.e. {abs(Emax-1)/0.2:.0f}x the bound.")
check("S4 [cosmology] the homogeneous background is NOT beyond cluster outskirts in every candidate variable, so monotone screening can decouple G_cosmo from G_cluster",
      not allbeyond, f"it is beyond in all of them (density {min(b['rho_out'] for b in beyond.values())/rho_cos_b:.0f}x lower, potential and acceleration -> 0), forcing G_cosmo/G_local >= {Emax:.2f}")
surv = (ok1 and z1 < 3) or (ok2 and z2 < 3) or (ok3 and z3 < 3)
check("S5 [verdict] the screened-force route survives the overlap tests AND the cosmological ordering",
      surv and not allbeyond,
      "the ordering argument is independent of which variable is screened and of whether the populations overlap")
print("\n  what remains open, stated rather than closed: (i) a TIME-dependent transition (a field that rolls late) evades the"
      "\n  ordering argument because the background value at BBN and today differ -- that is not screening, it is a cosmological"
      "\n  history, and it must then face the CMB and growth of structure; (ii) a non-monotone S, or S of two variables at once,"
      "\n  is a fitted function rather than a screening mechanism.  Neither is claimed closed here.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
