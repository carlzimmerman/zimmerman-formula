#!/usr/bin/env python3
"""
L55 -- THE COMPOSITION KERNEL: can the MOND kernel be suppressed where cold matter dominates?
=============================================================================================
THE STATE.  L49 found the minimum addition to the deposited action is a cold collisionless component in the
matter sector: it satisfies the whole cluster specification, leaves the clock tachyon satisfied identically,
and repairs the CMB and linear growth exactly.  It failed on one gate -- the action's MOND scalar is sourced
by the TOTAL matter potential, so the kernel amplifies the very mass added to replace it, and the three
admissible cold fractions (galaxies, clusters, CMB) have an empty intersection.  L50 re-sourced the scalar on
the baryons alone, which is legitimate at the Lagrangian level; it moved both windows it was meant to move
(galaxies 0.355 -> 0.582, clusters 0.316 -> 0.569, so the two now agree to 0.1 sigma) but the intersection
stayed empty because the CMB window cannot move at all.  The gap narrowed from 2.82x to 1.72x (canonical).

BOTH LANES NAME THE SAME REMAINING MOVE.  L49 option (b); L50 D8/D9 computed what it needs: at f = 1 the
kernel must be suppressed to s <= 0.495 (canonical) / 0.439 (alt) where galaxies are measured.  This lane
tests the only stated way to get that suppression from a field-theory variable rather than by hand:

  ***  LET THE KERNEL'S ARGUMENT DEPEND ON THE BARYON FRACTION f_b = rho_b / (rho_b + rho_c),  ***
  ***  i.e. on the RATIO OF TWO SPECIES rather than on any single environmental scalar.        ***

THE CRUX, SETTLED FIRST.  L6 closed a screened force whose strength depends on ONE local variable -- the
potential, the density, the acceleration or the enclosed mass -- on two horns: overlap (clusters and galaxies
occupy the same X and need different enhancement) and the cosmological ordering (the background lies BEYOND
cluster outskirts in every such variable, so any monotone S unscreens it at least as much, forcing
G_cosmo/G_local >= 1.82 against BBN's 1.2).  L6's own closing note says a function of TWO variables at once
was NOT closed.  Part B decides whether f_b is genuinely new or collapses into L6's class.

THE MOST LIKELY WAY THIS DIES, checked directly (Part C).  Galaxy discs are baryon-dominated in the inner
regions but -- on this very hypothesis, at the cold abundance the CMB fixes -- COLD-DOMINATED in the outer
rotation curve, which is exactly where MOND is needed.  The suppression may therefore switch on precisely
where the kernel is supposed to work.

WHAT IS TESTED (checks that can fail; the check() helper is copied from L6_screened_force.py):
  X1-X6   CONTROLS.  Rebuild L50's two windows and the 1.72x gap, L50's s <= 0.495, and reproduce L6's
          closure on its own terms (both horns) before using either.
  B1-B4   Is a baryon-fraction kernel outside L6's closed class, or does it collapse into it?
  C1-C6   Can ONE function of f_b be full strength in discs and suppressed at high cold fraction?  Two
          readings of f_b are carried, because they are the two horns of the mechanism: the ENCLOSED-MASS
          fraction (spherical, what sets the rotation curve) and the LOCAL MIDPLANE fraction (what a local
          field-theory scalar would actually see in a thin disc).
  D1-D8   The three windows and the deposited theory's gates, re-run on each horn.
  E1-E4   The price: equivalence-principle violation, free functions, observability.
  V1-V3   The verdict, and -- if it fails -- the general theorem.

Both a_0 footings (9.3619e-11 canonical, 1.1279e-10 alt) on every dimensional number.
NOTHING HERE FAVOURS THIS FRAMEWORK OVER LambdaCDM AND NOTHING HERE CONSTRAINS LambdaCDM: the cold component
and its abundance-matched profile are LambdaCDM's, imported wholesale.
"""
import numpy as np, math, json, os, sys, glob, textwrap

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("  " + s, flush=True)
def wrap(s, ind=6):
    for ln in textwrap.wrap(s, 118 - ind): print(" " * ind + ln, flush=True)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "real_research/data")
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 3.0857e22; pc = 3.0857e16
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
S_SAT, D_SAT = 2.540, 0.6476
OM, OB, ODM = 0.315, 0.049, 0.266
F_COSMIC = ODM/OB                                   # 5.4286
FB_COSMIC = OB/OM                                   # 0.1556
OCH2 = 0.1200                                       # Planck 2018
hP = 0.674; H0 = hP*100e3/Mpc; RHO_C = 3*H0**2/(8*math.pi*G)
UPS_D, UPS_B = 0.5, 0.7
KB_X, C14_X, SIG_X = 0.2, 1.0000e-6, 1.679312732187113
C2_X = 2*SIG_X*C14_X/(2 - C14_X - 3*SIG_X*C14_X)
K2_X = (2 - KB_X)**2/C2_X

def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def kern(gb, a0): return a0*Delta(np.asarray(gb, float)/a0)

P("=" * 122)
P("L55 -- THE COMPOSITION KERNEL: can the MOND kernel be suppressed where cold matter dominates,")
P("       without reintroducing what L6 already closed?")
P("=" * 122)
P("  sources, all committed products of this repository; nothing below is retyped from prose:")
P("    clusters : closure_2026/cluster_measurement_audit_2026/results.json")
P("    galaxies : real_research/data/sparc_data/*_rotmod.dat  +  real_research/data/SPARC_Lelli2016c.mrt")
P("    controls : L50_BARYON_SOURCED.md (windows, gap, s<=0.495);  L6_screened_force.py (the closed class)")
P("    theory   : THE_COMPLETE_THEORY_2026-09-08.md sections 2-5;  L49_MINIMUM_ADDITION.md")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART A -- CONTROLS.  Rebuild L50's windows and gap, and reproduce L6's closure, before using either.")
P("=" * 122)

CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
CLU = {}
for rw in CLJ["rows"]:
    f = rw.get("footing", "canonical"); a0 = A0[f]
    CLU.setdefault(f, {}).setdefault(rw["cluster"], []).append(
        (float(rw["r_kpc"]), float(rw["g_baryon_over_a0"])*a0, float(rw["g_hse_over_a0"])*a0))

ANCH = {}           # outermost row per cluster -- the amount anchors
CROWS = {}          # every usable row per cluster -- for the overlap machinery
for f in sorted(CLU):
    a0 = A0[f]; rows = []; allrows = []
    for n in sorted(CLU[f]):
        p = np.array(sorted(CLU[f][n])); r = p[:, 0]*kpc; gb = p[:, 1]; gh = p[:, 2]
        Mb = gb*r**2/G; Mh = gh*r**2/G
        rho_b = np.gradient(Mb, r)/(4*math.pi*r**2)
        rho_t = np.gradient(Mh, r)/(4*math.pi*r**2)
        for i in range(len(r)):
            if rho_b[i] <= 0 or rho_t[i] <= 0: continue
            allrows.append(dict(name=n, r=r[i], gb=gb[i], gh=gh[i], M=Mb[i], phi=gb[i]*r[i],
                                rho=rho_b[i], rho_t=rho_t[i],
                                fb_enc=Mb[i]/max(Mh[i], 1e-300),
                                fb_loc=rho_b[i]/max(rho_t[i], 1e-300),
                                E=gh[i]/(gb[i] + float(kern(gb[i], a0)))))
        rows.append(dict(name=n, r_kpc=p[-1, 0], gb=gb[-1], gh=gh[-1],
                         rN=(Mh[-1]-Mb[-1])/Mb[-1],
                         rF=(Mh[-1]-(gb[-1]+float(kern(gb[-1], a0)))*r[-1]**2/G)/Mb[-1],
                         fbar=Mb[-1]/Mh[-1]))
    ANCH[f] = rows; CROWS[f] = allrows
RAT_CLU = {f: float(np.median([x["rN"] for x in ANCH[f]])) for f in ANCH}
ERAT_CLU = {f: float(np.std([x["rN"] for x in ANCH[f]], ddof=1)) for f in ANCH}
RES_CLU = {f: float(np.median([x["rF"] for x in ANCH[f]])) for f in ANCH}
FBAR_CLU = {f: float(np.median([x["fbar"] for x in ANCH[f]])) for f in ANCH}
for f in ("canonical", "alt"):
    info(f"{f:>9}: {len(ANCH[f])} clusters at {ANCH[f][0]['r_kpc']:.0f} kpc, {len(CROWS[f])} usable rows -- "
         f"f_bar {FBAR_CLU[f]:.3f}, Newtonian M_dark/M_bar {RAT_CLU[f]:.2f} +/- {ERAT_CLU[f]:.2f}, "
         f"post-kernel residual {RES_CLU[f]:.2f} M_bar")
check("X1 [control] an independent recomputation returns L49 X1 / L50 A1's cluster amount 5.73 +/- 0.68 and "
      "f_bar = 0.149 at 1000 kpc, and the post-kernel residual 3.09 / 2.76 M_bar",
      abs(RAT_CLU["canonical"] - 5.73) < 0.05 and abs(ERAT_CLU["canonical"] - 0.68) < 0.05
      and abs(FBAR_CLU["canonical"] - 0.149) < 0.002 and abs(RES_CLU["canonical"] - 3.09) < 0.06
      and abs(RES_CLU["alt"] - 2.76) < 0.06,
      f"M_dark/M_bar = {RAT_CLU['canonical']:.2f} +/- {ERAT_CLU['canonical']:.2f}, f_bar = "
      f"{FBAR_CLU['canonical']:.3f}, residual {RES_CLU['canonical']:.2f} / {RES_CLU['alt']:.2f} M_bar")

# ---- SPARC ---------------------------------------------------------------------------------------------
def read_master():
    lines = open(os.path.join(DATA, "SPARC_Lelli2016c.mrt"), encoding="latin-1").read().splitlines()
    last = max(i for i, l in enumerate(lines) if l.startswith("-----")); rows = {}
    for line in lines[last + 1:]:
        f = line.split()
        if len(f) < 18: continue
        try: rows[f[0]] = dict(L36=float(f[7]), MHI=float(f[13]))
        except ValueError: continue
    return rows
MASTER = read_master()
def moster_mstar(logMh):
    N, logM1, be, ga = 0.0351, 11.590, 1.376, 0.608
    x = 10**(np.asarray(logMh, float) - logM1)
    return 10**np.asarray(logMh, float)*2*N/(x**(-be) + x**ga)
_LMH = np.linspace(8.5, 15.5, 2801); _LMS = np.log10(moster_mstar(_LMH))
def halo_mass_AM(Ms): return 10**np.interp(np.log10(np.asarray(Ms, float)), _LMS, _LMH)
_nfwm = lambda x: np.log1p(x) - x/(1.0 + x)
def c200_gal(M): return 10**(0.905 - 0.101*np.log10(np.asarray(M, float)*hP/1e12))

GAL = []
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    if name not in MASTER: continue
    m = MASTER[name]
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0]*kpc; Vo = d[:, 1]*1e3; eV = d[:, 2]*1e3; Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
    SBd = d[:, 6] if d.shape[1] > 6 else np.zeros_like(r)
    SBb = d[:, 7] if d.shape[1] > 7 else np.zeros_like(r)
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    msk = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV/np.maximum(Vo, 1) < 0.10)
    if msk.sum() < 3: continue
    Mstar = UPS_D*m["L36"]*1e9; Mgas = 1.33*m["MHI"]*1e9
    rr = r[msk]
    Mb_enc = Vb2[msk]*rr/G/MSUN                                   # spherical-equivalent enclosed baryons
    # local baryon SURFACE density: stars from the photometry (exact), gas from the enclosed-mass gradient
    Sig_star = (UPS_D*SBd[msk] + UPS_B*SBb[msk])                  # M_sun / pc^2
    Mg_enc = Vg[msk]*np.abs(Vg[msk])*rr/G/MSUN
    Sig_gas = np.gradient(Mg_enc, rr/pc)/(2*math.pi*np.maximum(rr/pc, 1e-9))
    Sig_gas = np.clip(Sig_gas, 0.0, None)
    GAL.append(dict(name=name, r=rr, gb=Vb2[msk]/rr, go=Vo[msk]**2/rr, Mstar=Mstar, Mb=Mstar + Mgas,
                    Mb_enc=Mb_enc, Sig=Sig_star + Sig_gas))
for g in GAL:
    M200 = max(float(halo_mass_AM(g["Mstar"])), 1.02*g["Mb"]); g["M200"] = M200
    c = float(c200_gal(M200)); R200 = (3*M200*MSUN/(4*math.pi*200*RHO_C))**(1/3.)
    x = np.clip(g["r"]/R200, 1e-6, 6.0)
    Mh_enc = (M200 - g["Mb"])*_nfwm(c*x)/_nfwm(c)                 # M_sun, enclosed halo
    g["g_halo"] = G*Mh_enc*MSUN/g["r"]**2
    g["Mh_enc"] = Mh_enc
    rs = R200/c; dc = (200/3.)*c**3/_nfwm(c); rho_s = dc*RHO_C
    g["rho_halo"] = rho_s/((g["r"]/rs)*(1 + g["r"]/rs)**2)        # kg/m^3, NFW local density
NPT = sum(len(g["r"]) for g in GAL)
info(f"SPARC: {len(GAL)} galaxies, {NPT} points (Upsilon_d = {UPS_D}, Upsilon_b = {UPS_B}, eV/V < 0.10)")

def rms_model(f, eps, foot, kernel=True, ksup=1.0):
    a0 = A0[foot]; res = []
    for g in GAL:
        gN = g["gb"] + f*g["g_halo"]; src = g["gb"] + eps*f*g["g_halo"]
        gp = gN + (ksup*kern(src, a0) if kernel else 0.0)
        res.append(np.log10(g["go"]/gp))
    r = np.concatenate(res)
    return float(np.sqrt(np.mean(r**2))), float(np.median(r))
R0 = {foot: rms_model(0.0, 1.0, foot) for foot in A0}
RH1 = {foot: rms_model(1.0, 1.0, foot, kernel=False) for foot in A0}
check("X2 [control] the SPARC machinery reproduces L49 X8 / L50 A3's three parameter-free numbers: kernel "
      "0.145 / 0.142 dex at medians +0.030 / +0.003, abundance-matched halo alone 0.171 dex at -0.026",
      abs(R0["canonical"][0] - 0.145) < 0.004 and abs(R0["alt"][0] - 0.142) < 0.004
      and abs(R0["canonical"][1] - 0.030) < 0.004 and abs(RH1["canonical"][0] - 0.171) < 0.010
      and abs(RH1["canonical"][1] + 0.026) < 0.010,
      f"kernel {R0['canonical'][0]:.3f} / {R0['alt'][0]:.3f} dex, medians {R0['canonical'][1]:+.3f} / "
      f"{R0['alt'][1]:+.3f}; halo {RH1['canonical'][0]:.3f} dex at {RH1['canonical'][1]:+.3f}")

def f_max_gal(eps, foot, tol=0.11, ksup=1.0, sfun=None):
    lo, hi = 0.0, 4.0
    for _ in range(60):
        mid = 0.5*(lo + hi)
        if abs(rms_supp(mid, eps, foot, ksup=ksup, sfun=sfun)[1]) < tol: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)
def f_cluster(eps, foot, bias=0.0, ksup=1.0):
    a0 = A0[foot]; out = []
    for x in ANCH[foot]:
        gb = x["gb"]; gh = x["gh"]/(1.0 - bias); lo, hi = 0.0, 40.0
        for _ in range(80):
            mid = 0.5*(lo + hi)
            if gb*(1 + mid*F_COSMIC) + ksup*float(kern(gb*(1 + eps*mid*F_COSMIC), a0)) < gh: lo = mid
            else: hi = mid
        out.append(0.5*(lo + hi))
    return float(np.median(out)), float(np.std(out, ddof=1))

# the suppressed model.  sfun = None reproduces L50 exactly (s == ksup, constant).
def rms_supp(f, eps, foot, ksup=1.0, sfun=None, mode="enc"):
    a0 = A0[foot]; res = []
    for g in GAL:
        gN = g["gb"] + f*g["g_halo"]; src = g["gb"] + eps*f*g["g_halo"]
        s = ksup if sfun is None else ksup*sfun(fb_gal(g, f, mode))
        res.append(np.log10(g["go"]/(gN + s*kern(src, a0))))
    r = np.concatenate(res)
    return float(np.sqrt(np.mean(r**2))), float(np.median(r))
def fb_gal(g, f, mode="enc"):
    if mode == "enc":
        return g["Mb_enc"]/np.maximum(g["Mb_enc"] + f*g["Mh_enc"], 1e-300)
    rho_b = g["Sig"]*MSUN/pc**2/(2*HZ)                            # midplane, scale height HZ
    return rho_b/np.maximum(rho_b + f*g["rho_halo"], 1e-300)
HZ = 0.30*kpc                                                     # stellar+gas scale height, varied in C4

FGAL_B = {f: f_max_gal(0.0, f) for f in A0}
FCLU_B = {f: f_cluster(0.0, f) for f in A0}
FCLU_B_B = {f: f_cluster(0.0, f, 0.20) for f in A0}
GAP_B = {f: 1.0/FGAL_B[f] for f in A0}
info("")
info("L50's baryon-sourced (eps = 0) windows, rebuilt here with independent code:")
info(f"    galaxies  (generous, |median| < 0.11 dex) : f <= {FGAL_B['canonical']:.3f} / {FGAL_B['alt']:.3f}")
info(f"    clusters  (self-consistent at 1000 kpc)   : f  = {FCLU_B['canonical'][0]:.3f} +/- "
     f"{FCLU_B['canonical'][1]:.3f} / {FCLU_B['alt'][0]:.3f} +/- {FCLU_B['alt'][1]:.3f}  at b = 0")
info(f"    the CMB   (Omega_c h^2 = {OCH2:.4f})       : f  = 1.000 +/- 0.010")
info(f"    gap to the CMB                            : {GAP_B['canonical']:.2f}x / {GAP_B['alt']:.2f}x")
check("X3 [control] L50's two windows and its 1.72x / 2.06x gap are reproduced: galaxies f <= 0.582 / 0.486, "
      "clusters 0.569 +/- 0.130 / 0.508 +/- 0.133, and the intersection is EMPTY",
      abs(FGAL_B["canonical"] - 0.582) < 0.005 and abs(FGAL_B["alt"] - 0.486) < 0.005
      and abs(FCLU_B["canonical"][0] - 0.569) < 0.005 and abs(FCLU_B["canonical"][1] - 0.130) < 0.005
      and abs(FCLU_B["alt"][0] - 0.508) < 0.005 and abs(GAP_B["canonical"] - 1.72) < 0.02
      and abs(GAP_B["alt"] - 2.06) < 0.02 and FGAL_B["canonical"] < 0.99,
      f"galaxies {FGAL_B['canonical']:.3f} / {FGAL_B['alt']:.3f}; clusters {FCLU_B['canonical'][0]:.3f} +/- "
      f"{FCLU_B['canonical'][1]:.3f} / {FCLU_B['alt'][0]:.3f} +/- {FCLU_B['alt'][1]:.3f}; gap "
      f"{GAP_B['canonical']:.2f}x / {GAP_B['alt']:.2f}x; at b = 0.20 clusters want "
      f"{FCLU_B_B['canonical'][0]:.3f} +/- {FCLU_B_B['canonical'][1]:.3f}, i.e. "
      f"{abs(1-FCLU_B_B['canonical'][0])/FCLU_B_B['canonical'][1]:.1f} sigma from the CMB")

def ksup_max(foot, tol=0.11):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5*(lo + hi)
        if abs(rms_supp(1.0, 0.0, foot, ksup=mid)[1]) < tol: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)
KSUP = {f: ksup_max(f) for f in A0}
check("X4 [control] L50 D8's sharp form is reproduced: at f = 1 a UNIFORM suppression of the kernel to "
      "s <= 0.495 (canonical) / 0.439 (alt) is what the galaxy window requires",
      abs(KSUP["canonical"] - 0.495) < 0.006 and abs(KSUP["alt"] - 0.439) < 0.006,
      f"s <= {KSUP['canonical']:.3f} / {KSUP['alt']:.3f}, i.e. the kernel must be suppressed by "
      f"{1/KSUP['canonical']:.1f}x / {1/KSUP['alt']:.1f}x where galaxies are measured")

# ---- X5/X6: L6 reproduced on its own terms -------------------------------------------------------------
GROW = []
for g in GAL:
    a0c = A0["canonical"]
    Mb = g["Mb_enc"]*MSUN
    rho = np.gradient(Mb, g["r"])/(4*math.pi*g["r"]**2)
    fbe = fb_gal(g, 1.0, "enc"); fbl = fb_gal(g, 1.0, "loc")
    for i in range(len(g["r"])):
        if rho[i] <= 0: continue
        GROW.append(dict(name=g["name"], r=g["r"][i], gb=g["gb"][i], go=g["go"][i], M=Mb[i],
                         phi=g["gb"][i]*g["r"][i], rho=rho[i], idx=i, gal=g,
                         fb_enc=fbe[i], fb_loc=fbl[i]))
def overlap(var, foot, cl_key="E", nbin=6):
    a0 = A0[foot]; cl = CROWS[foot]
    xc = np.array([x[var] for x in cl]); Ec = np.array([x[cl_key] for x in cl])
    xg = np.array([x[var] for x in GROW])
    Eg = np.array([x["go"]/(x["gb"] + float(kern(x["gb"], a0))) for x in GROW])
    lo = max(xc.min(), xg.min()); hi = min(xc.max(), xg.max())
    if not (hi > lo): return 0.0, 0.0
    frac = float(((xc >= lo) & (xc <= hi)).mean())
    edges = np.geomspace(lo, hi, nbin + 1); worst = 0.0
    for i in range(nbin):
        mc = (xc >= edges[i]) & (xc < edges[i+1]); mg = (xg >= edges[i]) & (xg < edges[i+1])
        if mc.sum() < 3 or mg.sum() < 5: continue
        cm = float(np.median(Ec[mc])); gm = float(np.median(Eg[mg]))
        cs = float(np.std(Ec[mc], ddof=1)/math.sqrt(mc.sum())); gs = float(np.std(Eg[mg], ddof=1)/math.sqrt(mg.sum()))
        worst = max(worst, abs((cm - gm)/math.hypot(max(cs, 1e-9), max(gs, 1e-9))))
    return frac, worst
L6TAB = {}
for var, lab in (("gb", "acceleration g_bar (control: this IS a kernel)"), ("phi", "potential Phi_loc"),
                 ("rho", "baryon density rho_b"), ("M", "enclosed baryon mass M_b(<r)")):
    fr, wz = overlap(var, "canonical")
    L6TAB[var] = (fr, wz)
    info(f"    L6 {lab:<44s} overlap {100*fr:3.0f}% of cluster rows, worst |z| = {wz:5.1f}")
check("X5 [control] L6's overlap horn is reproduced on its own terms: the control in acceleration kills at "
      "|z| ~ 25, and density screening dies with 100% overlap at |z| ~ 12.8",
      L6TAB["gb"][1] > 20 and L6TAB["rho"][0] > 0.99 and L6TAB["rho"][1] > 10 and L6TAB["phi"][1] > 10,
      f"acceleration |z| = {L6TAB['gb'][1]:.1f} at {100*L6TAB['gb'][0]:.0f}% overlap; density "
      f"|z| = {L6TAB['rho'][1]:.1f} at {100*L6TAB['rho'][0]:.0f}%; potential |z| = {L6TAB['phi'][1]:.1f} at "
      f"{100*L6TAB['phi'][0]:.0f}%; mass |z| = {L6TAB['M'][1]:.1f} at {100*L6TAB['M'][0]:.0f}%")

rho_cos_b = OB*RHO_C
OUT6 = {}
for foot in sorted(CROWS):
    out_rows = sorted(CROWS[foot], key=lambda x: -x["r"])[:max(3, len(CROWS[foot])//10)]
    OUT6[foot] = dict(rho=float(np.median([x["rho"] for x in out_rows])),
                      E=float(np.median([x["E"] for x in out_rows])),
                      fb_enc=float(np.median([x["fb_enc"] for x in out_rows])),
                      fb_loc=float(np.median([x["fb_loc"] for x in out_rows])))
info("")
info(f"    L6 ordering: cluster outskirts rho_b = {OUT6['canonical']['rho']:.2e} kg/m^3 against the cosmic "
     f"{rho_cos_b:.2e} ({OUT6['canonical']['rho']/rho_cos_b:.0f}x LOWER); Phi_loc, g_bar -> 0 by homogeneity")
info(f"                 => any monotone S unscreening clusters unscreens the background at least as much, "
     f"forcing G_cosmo/G_local >= E_out = {OUT6['canonical']['E']:.2f} against BBN's 1.2")
check("X6 [control] L6's cosmological-ordering horn is reproduced: the homogeneous background lies BEYOND "
      "cluster outskirts in every one of L6's variables, forcing G_cosmo/G_local >= 1.82 = 4x the BBN bound",
      OUT6["canonical"]["rho"]/rho_cos_b > 1000 and abs(OUT6["canonical"]["E"] - 1.82) < 0.03
      and abs(OUT6["alt"]["E"] - 1.68) < 0.03,
      f"density {OUT6['canonical']['rho']/rho_cos_b:.0f}x lower, potential and acceleration -> 0; "
      f"E(cluster outskirts) = {OUT6['canonical']['E']:.2f} / {OUT6['alt']['E']:.2f}, i.e. "
      f"{abs(OUT6['canonical']['E']-1)/0.2:.0f}x the BBN bound. L6's closure reproduces")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART B -- THE CRUX: is a BARYON-FRACTION kernel outside L6's closed class, or does it collapse into it?")
P("=" * 122)
wrap("The mechanism, stated precisely.  The deposited action's MOND term is J(Y) with Y = |grad phi|^2 and a "
     "coupling 2(2 - K_B) J^mu d_mu phi.  The proposal is to make the coupling -- equivalently the kernel's "
     "overall strength -- a function of the LOCAL BARYON FRACTION f_b = rho_b/(rho_b + rho_c), so that the "
     "MOND term is at full strength where baryons dominate and switched off where the cold component does:", 2)
P("        g = g_bar + f g_halo + s(f_b) a_0 Delta( g_src / a_0 ) ,      s(1) = 1,   s(f_b -> 0) -> 0.")
wrap("L6 closed S(X) for X a SINGLE environmental scalar: the potential, the baryon density, the "
     "acceleration, or the enclosed mass.  f_b is a RATIO OF TWO SPECIES.  L6's own closing note records that "
     "'a non-monotone S, or S of two variables at once, is a fitted function rather than a screening "
     "mechanism.  Neither is claimed closed here.'  So the class is formally untested; B1-B3 decide whether "
     "it is genuinely new or collapses in practice.", 2)

# f_b for every population, at the CMB's own abundance f = 1
FB_G = {}
for mode in ("enc", "loc"):
    vals = []
    for g in GAL: vals.append(fb_gal(g, 1.0, mode))
    FB_G[mode] = np.concatenate(vals)
FB_C = {"enc": np.array([x["fb_enc"] for x in CROWS["canonical"]]),
        "loc": np.array([x["fb_loc"] for x in CROWS["canonical"]])}
P("")
info(f"    f_b at the CMB's own cold abundance f = 1:")
info(f"      SPARC, enclosed-mass reading  : median {np.median(FB_G['enc']):.3f}, "
     f"10-90% [{np.percentile(FB_G['enc'],10):.3f}, {np.percentile(FB_G['enc'],90):.3f}]")
info(f"      SPARC, local-midplane reading : median {np.median(FB_G['loc']):.3f}, "
     f"10-90% [{np.percentile(FB_G['loc'],10):.3f}, {np.percentile(FB_G['loc'],90):.3f}]   (h_z = 300 pc)")
info(f"      clusters, enclosed            : median {np.median(FB_C['enc']):.3f}; local: "
     f"{np.median(FB_C['loc']):.3f}")
info(f"      the homogeneous background    : f_b = Omega_b/Omega_m = {FB_COSMIC:.4f}")

# B1 -- does f_b collapse into a function of one of L6's variables?
def collapse_z(mode, nbin=6):
    """At the SAME value of an L6 variable, do the two populations sit at the same f_b?  If not, f_b is not
       a function of that variable and the mechanism is not L6's."""
    worst = 0.0; tab = []
    for var in ("gb", "phi", "rho", "M"):
        xc = np.array([x[var] for x in CROWS["canonical"]]); yc = np.array([x["fb_" + mode] for x in CROWS["canonical"]])
        xg = np.array([x[var] for x in GROW])
        yg = np.array([fb_gal(x["gal"], 1.0, mode)[x["idx"]] for x in GROW])
        lo = max(xc.min(), xg.min()); hi = min(xc.max(), xg.max())
        if not (hi > lo): tab.append((var, 0.0, 0.0)); continue
        edges = np.geomspace(lo, hi, nbin + 1); wz = 0.0
        for i in range(nbin):
            mc = (xc >= edges[i]) & (xc < edges[i+1]); mg = (xg >= edges[i]) & (xg < edges[i+1])
            if mc.sum() < 3 or mg.sum() < 5: continue
            cm, gm = float(np.median(yc[mc])), float(np.median(yg[mg]))
            cs = float(np.std(yc[mc], ddof=1)/math.sqrt(mc.sum())); gs = float(np.std(yg[mg], ddof=1)/math.sqrt(mg.sum()))
            wz = max(wz, abs((cm - gm)/math.hypot(max(cs, 1e-9), max(gs, 1e-9))))
        frac = float(((xc >= lo) & (xc <= hi)).mean())
        tab.append((var, frac, wz)); worst = max(worst, wz)
    return tab, worst
TAB_B1, ZB1 = collapse_z("enc")
P("")
info("  B1  does f_b collapse into a function of one of L6's variables?  At the SAME value of X, do clusters")
info("      and galaxies sit at the same f_b?  (If they do, s(f_b) IS an S(X) in disguise.)")
for var, fr, wz in TAB_B1:
    info(f"        X = {var:<4s}  overlap {100*fr:3.0f}%   cluster-vs-galaxy separation in f_b: |z| = {wz:6.1f}")
check("B1 f_b COLLAPSES into a single-valued function of one of L6's environmental variables, i.e. the "
      "mechanism is L6's screening under a new name",
      ZB1 < 3.0,
      f"it does not. At the same acceleration, potential, baryon density or enclosed baryon mass the two "
      f"populations sit at DIFFERENT baryon fractions, separated by |z| up to {ZB1:.0f}. f_b is not a "
      f"function of any single L6 variable, because it carries information about a SECOND species that none "
      f"of L6's variables contains. This is a genuinely new function, as L6's own closing note anticipated")

# B2 -- the cosmological ordering, the horn that killed L6 independently of overlap
fb_out = OUT6["canonical"]["fb_enc"]; fb_out_loc = OUT6["canonical"]["fb_loc"]
ratio_bg = FB_COSMIC/max(fb_out, 1e-12)
P("")
info("  B2  the cosmological ordering -- the horn that closed L6 without needing overlap.")
info(f"        L6's variables : the background is BEYOND cluster outskirts in ALL of them "
     f"(rho_b {OUT6['canonical']['rho']/rho_cos_b:.0f}x lower; Phi, g_bar -> 0).")
info(f"        f_b            : cluster outskirts f_b = {fb_out:.4f} (enclosed) / {fb_out_loc:.4f} (local); "
     f"the background is f_b = {FB_COSMIC:.4f}.")
info(f"                         ratio background/outskirts = {ratio_bg:.2f} -- the background is NOT beyond "
     f"cluster outskirts, it sits essentially AT them.")
wrap("This is L7's measured fact read as a statement about the screening variable: clusters retain "
     "essentially the cosmic baryon fraction (f_bar = 0.149 against 0.156), so the sequence "
     "galaxy-disc -> cluster-outskirts -> background is NOT monotone in f_b; it TERMINATES at the cluster "
     "value. A monotone s(f_b) therefore assigns the background the same suppression as cluster outskirts, "
     "and generates no runaway.", 8)
check("B2 the cosmological-ordering horn that closed L6 also fires on f_b, i.e. the background lies beyond "
      "cluster outskirts in the baryon fraction too",
      not (0.5 < ratio_bg < 2.0),
      f"it does not fire. In every L6 variable the background is orders of magnitude beyond cluster "
      f"outskirts; in f_b it is a factor {ratio_bg:.2f} away -- indistinguishable. The ordering argument "
      f"needs the background to be MORE unscreened than clusters; in f_b it is EQUALLY screened, so the "
      f"chain from cluster to cosmos is broken. This is L7's f_bar = 0.149 vs 0.156 read as a statement "
      f"about the screening variable")

# B3 -- the sign, and whether BBN can bite at all
P("")
g_bbn = 1e-6      # any acceleration scale at nucleosynthesis vastly exceeds a_0; the kernel is additive
info("  B3  the SIGN, and whether the BBN horn can bite at all.")
info(f"        L6's candidates were ENHANCEMENTS (E > 1) of a force whose unscreened value IS G_cosmo; the")
info(f"        kill was G_cosmo/G_local >= {OUT6['canonical']['E']:.2f} against BBN's 1.2. Here s <= 1 by")
info(f"        construction: it is a SUPPRESSION, so the ratio moves the OTHER WAY.")
info(f"        And the kernel is an ADDITIVE a_0-scale term, not a rescaling of G: at any BBN-era")
info(f"        acceleration the fractional kernel contribution is a_0 Delta(g/a_0)/g <= "
     f"{float(kern(g_bbn, A0['canonical']))/g_bbn:.1e}, so suppressing it changes G_eff by that much.")
check("B3 the BBN horn that closed L6 can bite on this mechanism, i.e. suppressing the kernel moves "
      "G_cosmo/G_local outside |G/G_0 - 1| < 0.2",
      abs(float(kern(g_bbn, A0["canonical"]))/g_bbn) > 0.2,
      f"it cannot. s <= 1 is a suppression, the opposite sign to L6's enhancement; and the kernel is an "
      f"additive a_0-scale term whose fractional size at BBN-era accelerations is "
      f"{float(kern(g_bbn, A0['canonical']))/g_bbn:.1e}, so switching it off entirely changes G_eff by "
      f"1 part in {1/max(float(kern(g_bbn, A0['canonical']))/g_bbn,1e-30):.0e}. BBN is blind to it")

KFRAC_BBN = float(kern(g_bbn, A0["canonical"]))/g_bbn
INSIDE_L6 = (ZB1 < 3.0) or (ratio_bg < 0.5) or (KFRAC_BBN > 0.2)
check("B4 [THE CRUX] a baryon-fraction-dependent kernel is INSIDE L6's closed class, so the lane is over "
      "before it starts",
      INSIDE_L6,
      f"it is NOT inside it, on three independent grounds: (i) f_b is not a single-valued function of any "
      f"of L6's four variables (B1, |z| up to {ZB1:.0f}); (ii) the ordering horn does not fire because the "
      f"background sits AT cluster outskirts in f_b rather than beyond them (B2, factor {ratio_bg:.2f}); "
      f"(iii) the sign is a suppression, not an enhancement, and the additive a_0-scale kernel is invisible "
      f"to BBN (B3). L6's own closing note already recorded that a function of two variables was untested. "
      f"The mechanism therefore has to be tested on its own, which is Parts C-E -- and being outside a "
      f"closed class is NOT evidence that it works")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART C -- THE FUNCTION.  Can ONE s(f_b) be full strength in discs and suppressed at high cold fraction?")
P("=" * 122)
wrap("This is where the brief says the mechanism is most likely to die, so it is checked directly and "
     "before any window is recomputed.  At the cold abundance the CMB fixes, galaxy discs are "
     "baryon-dominated in the inner regions and cold-dominated in the outer rotation curve -- which is "
     "exactly where MOND is needed.  Two readings of f_b are carried, because they are the two horns of the "
     "mechanism and they answer this question oppositely.", 2)

def deep_mask(g, foot):
    return g["gb"] < A0[foot]           # the deep/transition-MOND regime: where the kernel does the work
DEEP = {foot: [ (g, deep_mask(g, foot)) for g in GAL ] for foot in A0}
def dist_at_deep(mode, f=1.0, foot="canonical"):
    v = []
    for g, m in DEEP[foot]:
        if m.sum() == 0: continue
        v.append(fb_gal(g, f, mode)[m])
    return np.concatenate(v)
D_ENC = dist_at_deep("enc"); D_LOC = dist_at_deep("loc")
ndeep = sum(int(m.sum()) for g, m in DEEP["canonical"])
P("")
info(f"  C1  WHERE MOND IS NEEDED.  {ndeep} of {NPT} SPARC points ({100*ndeep/NPT:.0f}%) have g_bar < a_0 -- "
     f"the regime the kernel exists to explain.")
info(f"      At f = 1 those points sit at f_b = {np.median(D_ENC):.3f} (enclosed reading; 10-90% "
     f"[{np.percentile(D_ENC,10):.3f}, {np.percentile(D_ENC,90):.3f}])")
info(f"                                    f_b = {np.median(D_LOC):.3f} (local midplane; 10-90% "
     f"[{np.percentile(D_LOC,10):.3f}, {np.percentile(D_LOC,90):.3f}])")
check("C1 [THE MOST LIKELY WAY THIS DIES] at the cold abundance the CMB fixes, the points where MOND is "
      "needed are still BARYON-DOMINATED, so a suppression keyed to f_b leaves them alone",
      np.median(D_ENC) > 0.5,
      f"on the reading that actually sets the rotation curve -- the ENCLOSED-mass fraction -- they are not: "
      f"the median deep-MOND SPARC point sits at f_b = {np.median(D_ENC):.3f}, i.e. COLD-DOMINATED, and "
      f"{100*float((D_ENC < 0.5).mean()):.0f}% of them are below one half. The suppression switches on "
      f"exactly where the kernel is supposed to work. (On the LOCAL midplane reading the answer is the "
      f"opposite, f_b = {np.median(D_LOC):.3f}; that is the second horn, C3-C4)")

# C2 -- the overlap test in the new variable, run exactly as L6 runs it
fr_fb, z_fb = overlap("fb_enc", "canonical")
fr_fl, z_fl = overlap("fb_loc", "canonical")
P("")
info("  C2  L6's own overlap machinery, run in the NEW variable (this is the fair test of the new class):")
info(f"        f_b enclosed : overlap {100*fr_fb:3.0f}% of cluster rows, cluster-vs-galaxy required "
     f"enhancement differs at |z| = {z_fb:.1f}")
info(f"        f_b local    : overlap {100*fr_fl:3.0f}% of cluster rows, |z| = {z_fl:.1f}")
check("C2 in the new variable the two populations at the same f_b require the SAME kernel strength, so a "
      "single-valued s(f_b) exists on the data",
      z_fb < 3.0,
      f"at the same enclosed baryon fraction clusters and galaxies require kernel strengths differing at "
      f"|z| = {z_fb:.1f} over {100*fr_fb:.0f}% overlap -- L6's overlap horn fires in the new variable too, "
      f"for the SAME reason it fired in the old ones: the required enhancement is not a function of the "
      f"environment. (Local reading: |z| = {z_fl:.1f} at {100*fr_fl:.0f}% overlap)")

# C3 -- the two horns, exhibited as functions
def s_pow(p):    return lambda fb: np.clip(np.asarray(fb, float), 0.0, 1.0)**p
def s_sig(fs, n): return lambda fb: 1.0/(1.0 + (fs/np.maximum(np.asarray(fb, float), 1e-12))**n)
P("")
info("      the exhibited functions.  Two one- and two-parameter families, both monotone, both s(1) = 1:")
info("        s_pow(p)    = f_b^p                       (gentle; one parameter)")
info("        s_sig(f*,n) = 1/(1 + (f*/f_b)^n)          (sharp; two parameters, n = sharpness)")
for lab, sf in (("s = f_b^1     ", s_pow(1.0)), ("s = f_b^3     ", s_pow(3.0)),
                ("s: f*=0.5,n=4 ", s_sig(0.5, 4)), ("s: f*=0.2,n=8 ", s_sig(0.2, 8))):
    sd = sf(D_ENC); sl = sf(D_LOC); sc = sf(np.array([np.median(FB_C["enc"])]))[0]
    info(f"        {lab}  median s at deep-MOND SPARC points: {np.median(sd):.3f} (enclosed) / "
         f"{np.median(sl):.3f} (local);  at cluster outskirts: {sc:.3f}")
# is there ANY threshold separating "MOND needed in galaxies" from "cluster outskirts"?
sep_enc = float(np.percentile(D_ENC, 90)) > float(np.percentile(FB_C["enc"], 10))
ov_enc = float(((D_ENC >= FB_C["enc"].min()) & (D_ENC <= FB_C["enc"].max())).mean())
P("")
info(f"  C3  is there a THRESHOLD in f_b separating the deep-MOND galaxy points from cluster rows?")
info(f"        deep-MOND SPARC (enclosed): [{D_ENC.min():.3f}, {D_ENC.max():.3f}], median "
     f"{np.median(D_ENC):.3f}")
info(f"        cluster rows    (enclosed): [{FB_C['enc'].min():.3f}, {FB_C['enc'].max():.3f}], median "
     f"{np.median(FB_C['enc']):.3f}")
info(f"        {100*ov_enc:.0f}% of the deep-MOND galaxy points lie INSIDE the cluster range")
check("C3 ONE monotone function of f_b can be full strength where MOND is needed in galaxies AND suppressed "
      "at cluster outskirts -- i.e. the two requirements are separated by a threshold in f_b",
      not sep_enc and ov_enc < 0.05,
      f"they are not separated on the enclosed reading: {100*ov_enc:.0f}% of the deep-MOND galaxy points "
      f"fall inside the cluster f_b range, so any monotone s that switches OFF at cluster outskirts "
      f"switches off at those galaxy points too. The transition cannot be made sharp enough because there "
      f"is no gap to be sharp about")

# C4 -- the local horn: does the disc escape?  and how sensitive is it to h_z?
P("")
info("  C4  the LOCAL horn, and its sensitivity.  A thin disc is locally baryon-dominated even where the")
info("      ENCLOSED mass is not, so a kernel keyed to the local density ratio would survive in discs.")
info("      Scale height h_z varied over the observed range for stellar+gas discs:")
HZS = [0.15, 0.30, 0.60, 1.00]
LOCTAB = {}
for hz in HZS:
    globals()["HZ"] = hz*kpc
    d = dist_at_deep("loc")
    LOCTAB[hz] = float(np.median(d))
    info(f"        h_z = {hz:4.2f} kpc : median f_b at deep-MOND SPARC points = {np.median(d):.3f}, "
         f"fraction below 0.5 = {100*float((d < 0.5).mean()):3.0f}%")
globals()["HZ"] = 0.30*kpc
check("C4 the LOCAL-density reading rescues the disc, i.e. deep-MOND galaxy points stay baryon-dominated "
      "locally across the observed range of disc scale heights",
      all(v > 0.5 for v in LOCTAB.values()),
      f"it does across most of the range -- median local f_b at deep-MOND points is "
      + ", ".join(f"{LOCTAB[h]:.2f} at h_z = {h:.2f} kpc" for h in HZS) +
      f". That is the SECOND HORN and it is a genuine escape from C1/C3: on this reading the kernel is NOT "
      f"switched off where MOND is needed, and Part D shows it is the horn that both opens the pincer and "
      f"keeps part of the phenomenology. Its cost is that the one number it must hit is set by h_z (E2)")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART D -- THE THREE WINDOWS, RE-RUN ON EACH HORN, AND THE GATES.")
P("=" * 122)

def cluster_window_supp(foot, sfun, bias=0.0):
    """same solve as L50's f_cluster, but the kernel carries s(f_b) evaluated self-consistently at the row"""
    a0 = A0[foot]; out = []
    for x in ANCH[foot]:
        gb = x["gb"]; gh = x["gh"]/(1.0 - bias); lo, hi = 0.0, 40.0
        for _ in range(80):
            mid = 0.5*(lo + hi)
            fb = 1.0/(1.0 + mid*F_COSMIC)                # enclosed baryon fraction at that cold fraction
            s = float(sfun(np.array([fb]))[0]) if sfun is not None else 1.0
            if gb*(1 + mid*F_COSMIC) + s*float(kern(gb, a0)) < gh: lo = mid
            else: hi = mid
        out.append(0.5*(lo + hi))
    return float(np.median(out)), float(np.std(out, ddof=1))

HORNS = [("H1  enclosed f_b,  s = f_b^3", "enc", s_pow(3.0)),
         ("H1' enclosed f_b,  f*=0.5 n=8", "enc", s_sig(0.5, 8)),
         ("H2  local f_b,     s = f_b^3", "loc", s_pow(3.0)),
         ("H2' local f_b,     s = f_b^4", "loc", s_pow(4.0))]
P("")
info("  D1  the three windows on each horn (generous galaxy criterion, |median RAR shift| < 0.11 dex):")
info(f"    {'variant':<32s} {'gal can':>8s} {'gal alt':>8s} {'clusters b=0':>18s} {'clusters b=0.20':>18s} {'CMB':>6s}")
WIN = {}
for lab, mode, sf in HORNS:
    fg = {}
    for foot in A0:
        lo, hi = 0.0, 4.0
        for _ in range(50):
            mid = 0.5*(lo + hi)
            if abs(rms_supp(mid, 0.0, foot, sfun=sf, mode=mode)[1]) < 0.11: lo = mid
            else: hi = mid
        fg[foot] = 0.5*(lo + hi)
    fc = cluster_window_supp("canonical", sf); fcb = cluster_window_supp("canonical", sf, 0.20)
    WIN[lab] = (fg, fc, fcb, sf, mode)
    info(f"    {lab:<32s} {fg['canonical']:8.3f} {fg['alt']:8.3f}   {fc[0]:7.3f} +/- {fc[1]:.3f}   "
         f"{fcb[0]:7.3f} +/- {fcb[1]:.3f}  1.000")
info(f"    {'L50 control (no suppression)':<32s} {FGAL_B['canonical']:8.3f} {FGAL_B['alt']:8.3f}   "
     f"{FCLU_B['canonical'][0]:7.3f} +/- {FCLU_B['canonical'][1]:.3f}   "
     f"{FCLU_B_B['canonical'][0]:7.3f} +/- {FCLU_B_B['canonical'][1]:.3f}  1.000")

H1 = WIN["H1  enclosed f_b,  s = f_b^3"]; H2 = WIN["H2  local f_b,     s = f_b^3"]
H2b = WIN["H2' local f_b,     s = f_b^4"]
check("D1 the galaxy window MOVES under a composition-dependent kernel, i.e. the mechanism does something "
      "L50's re-sourcing could not",
      H1[0]["canonical"] > FGAL_B["canonical"] + 0.05 and H2b[0]["canonical"] > FGAL_B["canonical"] + 0.05,
      f"it does, on BOTH readings of f_b and by a large margin: the ceiling rises from L50's "
      f"{FGAL_B['canonical']:.3f} / {FGAL_B['alt']:.3f} to {H1[0]['canonical']:.3f} / {H1[0]['alt']:.3f} "
      f"(enclosed reading) and {H2b[0]['canonical']:.3f} / {H2b[0]['alt']:.3f} (local reading, s = f_b^4). "
      f"This is the first move in the L49-L50-L55 sequence that lifts the galaxy ceiling past f = 1, and it "
      f"is reported as a positive result before it is priced")

inter = {}
for lab, (fg, fc, fcb, sf, mode) in WIN.items():
    inter[lab] = (fg["canonical"] >= 0.99 and fg["alt"] >= 0.99 and abs(fc[0] - 1.0) < 2*fc[1])
open_any = any(inter.values())
check("D2 [THE PINCER] the three-way intersection is non-empty on at least one exhibited function -- one "
      "cold fraction admissible to galaxies, to clusters AND to the CMB at once",
      open_any,
      "it is, and this is a genuine positive that the lane was set up to be able to find: on the "
      + ", ".join(lab.strip() for lab, v in inter.items() if v) +
      f" variants the galaxy ceiling clears f = 1 on both footings, clusters need "
      f"{H1[1][0]:.3f} +/- {H1[1][1]:.3f} at b = 0 ({abs(H1[1][0]-1)/H1[1][1]:.1f} sigma from the CMB's "
      f"1.000) and {H1[2][0]:.3f} +/- {H1[2][1]:.3f} at b = 0.20, and the CMB fixes 1.000 +/- 0.010. The "
      f"pincer that closed L49 and L50 OPENS. D3-D7 price what opening it costs, and that price is the "
      f"actual finding")

# ---- D3: what the kernel is still doing -----------------------------------------------------------------
def mond_work(f, foot, sfun, mode):
    """median over deep-MOND SPARC points of the share of the OBSERVED anomaly g_obs - g_bar that the
       kernel supplies.  1 = the kernel IS the anomaly; 0 = the kernel does nothing."""
    a0 = A0[foot]; num = []
    for g in GAL:
        m = g["gb"] < a0
        if m.sum() == 0: continue
        s = sfun(fb_gal(g, f, mode))[m] if sfun is not None else 1.0
        num.append(s*kern(g["gb"], a0)[m]/np.maximum(g["go"][m] - g["gb"][m], 1e-30))
    return float(np.median(np.concatenate(num)))
def halo_work(f, foot):
    a0 = A0[foot]; num = []
    for g in GAL:
        m = g["gb"] < a0
        if m.sum() == 0: continue
        num.append(f*g["g_halo"][m]/np.maximum(g["go"][m] - g["gb"][m], 1e-30))
    return float(np.median(np.concatenate(num)))
W0 = mond_work(0.0, "canonical", None, "enc")
WH1 = halo_work(1.0, "canonical")
W_H1 = mond_work(1.0, "canonical", H1[3], "enc"); W_H1a = mond_work(1.0, "alt", H1[3], "enc")
W_H2 = mond_work(1.0, "canonical", H2[3], "loc"); W_H2b = mond_work(1.0, "canonical", H2b[3], "loc")
P("")
info("  D3  WHAT THE KERNEL IS STILL DOING.  Median over the deep-MOND SPARC points of the share of the")
info("      OBSERVED anomaly (g_obs - g_bar) that each term supplies:")
info(f"        the kernel, deposited theory at f = 0    W = {W0:.3f}   (the kernel IS the anomaly)")
info(f"        the LambdaCDM halo alone at f = 1        W = {WH1:.3f}   (it already supplies "
     f"{100*WH1:.0f}% of it)")
info(f"        the kernel, H1 enclosed horn at f = 1    W = {W_H1:.3f} / {W_H1a:.3f}")
info(f"        the kernel, H2 local horn at f = 1       W = {W_H2:.3f} (p = 3), {W_H2b:.3f} (p = 4)")
check("D3 [THE WHOLE QUESTION] opening the pincer leaves the galaxy-scale MOND phenomenology INTACT, i.e. "
      "the kernel still supplies most of the observed deep-MOND anomaly at f = 1",
      max(W_H1, W_H2b) > 0.7,
      f"it does not. The halo at the CMB's own abundance already supplies {100*WH1:.0f}% of the observed "
      f"deep-MOND anomaly on its own, so the kernel's remaining room is whatever the tolerance allows. On "
      f"the variants that clear f = 1 the kernel's share falls from {W0:.3f} to "
      f"{max(W_H1, W_H2b):.3f} at best -- the suppression switches on exactly where MOND is needed, which "
      f"is what C1 predicted. The window opens by removing between {100*(1-max(W_H1,W_H2b)/W0):.0f}% and "
      f"{100*(1-min(W_H1,W_H2b)/W0):.0f}% of the kernel's work")

# ---- D4: the trade-off, and that it does not depend on the variable ------------------------------------
def unif(s): return (lambda fb, s=s: np.full(np.shape(fb), s))
P("")
info("  D4  THE TRADE-OFF, computed with a UNIFORM suppression so it cannot depend on which variable is")
info("      screened.  s is the kernel's strength at the deep-MOND points; f_max is the galaxy ceiling:")
info(f"    {'s':>7} {'f_max can':>10} {'f_max alt':>10} {'W (kernel share)':>18} {'rms at f=1':>12}")
SCAN = []
for s in (1.0, 0.8, 0.6, 0.5, 0.439, 0.4, 0.3, 0.2, 0.1, 0.0):
    sf = unif(s)
    fc = f_max_gal(0.0, "canonical", sfun=sf); fa = f_max_gal(0.0, "alt", sfun=sf)
    w = mond_work(1.0, "canonical", sf, "enc"); rr = rms_supp(1.0, 0.0, "canonical", sfun=sf)
    SCAN.append((s, fc, fa, w, rr[0]))
    info(f"    {s:7.3f} {fc:10.3f} {fa:10.3f} {w:18.3f} {rr[0]:12.3f}")
# the ceiling: the largest kernel share compatible with f = 1 on BOTH footings
ss = np.array([x[0] for x in SCAN]); fa_ = np.array([x[2] for x in SCAN]); ww = np.array([x[3] for x in SCAN])
o = np.argsort(ss); S_CRIT = float(np.interp(1.0, fa_[o][::-1], ss[o][::-1]))
W_CEIL = float(np.interp(S_CRIT, ss[o], ww[o]))
info(f"    => f = 1 admissible on BOTH footings requires s <= {S_CRIT:.3f} (the alt footing binds),")
info(f"       at which the kernel's share of the observed anomaly is W <= {W_CEIL:.3f}.")
# does the whole two-horn family collapse onto this one curve?
FAM = [("s=f_b^0.5 enc", s_pow(0.5), "enc"), ("s=f_b^1 enc", s_pow(1.0), "enc"),
       ("s=f_b^2 enc", s_pow(2.0), "enc"), ("s=f_b^3 enc", s_pow(3.0), "enc"),
       ("f*=0.3,n=2 enc", s_sig(0.3, 2), "enc"), ("f*=0.5,n=8 enc", s_sig(0.5, 8), "enc"),
       ("s=f_b^1 loc", s_pow(1.0), "loc"), ("s=f_b^2 loc", s_pow(2.0), "loc"),
       ("s=f_b^3 loc", s_pow(3.0), "loc"), ("s=f_b^4 loc", s_pow(4.0), "loc"),
       ("s=f_b^6 loc", s_pow(6.0), "loc")]
def s_eff(sf, mode, foot="canonical"):
    v = []
    for g in GAL:
        m = g["gb"] < A0[foot]
        if m.sum() == 0: continue
        v.append(sf(fb_gal(g, 1.0, mode))[m])
    return float(np.median(np.concatenate(v)))
P("")
info("      and the same table for ELEVEN genuine functions of f_b, on BOTH readings, against the uniform")
info("      curve evaluated at each one's own median deep-MOND strength s_eff:")
info(f"    {'function':<18s} {'s_eff':>7} {'f_max can':>10} {'uniform':>9} {'W':>7} {'uniform':>9}")
dev_f = []; dev_w = []
for lab, sf, mode in FAM:
    se = s_eff(sf, mode)
    lo, hi = 0.0, 4.0
    for _ in range(45):
        mid = 0.5*(lo + hi)
        if abs(rms_supp(mid, 0.0, "canonical", sfun=sf, mode=mode)[1]) < 0.11: lo = mid
        else: hi = mid
    fm = 0.5*(lo + hi); w = mond_work(1.0, "canonical", sf, mode)
    fu = float(np.interp(se, ss[o], np.array([x[1] for x in SCAN])[o]))
    wu = float(np.interp(se, ss[o], ww[o]))
    dev_f.append(abs(fm - fu)); dev_w.append(abs(w - wu))
    info(f"    {lab:<18s} {se:7.3f} {fm:10.3f} {fu:9.3f} {w:7.3f} {wu:9.3f}")
MAXDEV_F = float(max(dev_f)); MAXDEV_W = float(max(dev_w))
check("D4 [the general form] the galaxy ceiling and the kernel's share depend on WHICH variable the "
      "suppression is a function of, so a better choice of variable could still be found",
      MAXDEV_F > 0.15 or MAXDEV_W > 0.10,
      f"they do not. Every one of the eleven functions, on both readings of f_b, lands on the uniform curve "
      f"at its own median deep-MOND strength to within {MAXDEV_F:.3f} in f_max and {MAXDEV_W:.3f} in W. The "
      f"galaxy data see exactly ONE number -- the kernel's effective strength where the anomaly is -- and "
      f"every choice of variable is only a different way of setting it. So the bound is universal: f = 1 on "
      f"both footings requires s_eff <= {S_CRIT:.3f}, hence W <= {W_CEIL:.3f}. This generalises L50 D8 from "
      f"a uniform suppression to ANY function of ANY variable, environmental or compositional")

# ---- D5: the surviving kernel is degenerate with a smaller a_0 -----------------------------------------
dev = []; devS = []
for s in (0.2, 0.3, 0.439):
    a0 = A0["canonical"]
    gdeep = np.geomspace(1e-6, 1e-3, 200)*s*s*a0          # STRICTLY deep for BOTH kernels
    dev.append(float(np.max(np.abs(s*kern(gdeep, a0)/kern(gdeep, s*s*a0) - 1))))
    gsp = np.concatenate([g["gb"][g["gb"] < a0] for g in GAL])   # the actual SPARC deep-MOND points
    devS.append(float(np.median(np.abs(s*kern(gsp, a0)/kern(gsp, s*s*a0) - 1))))
A0_EFF = S_CRIT**2
KAPPA_FIT = 0.4998
P("")
info("  D5  WHAT THE SURVIVING KERNEL IS.  In the deep-MOND limit Delta(x) -> sqrt(x), so")
info("      s * a_0 Delta(g/a_0) = sqrt(s^2 a_0 g) = a_0' Delta(g/a_0') with a_0' = s^2 a_0 EXACTLY:")
info(f"        verified numerically in the strict deep limit (g << s^2 a_0): max |s*kern(a_0)/kern(s^2 a_0)")
info(f"        - 1| = {max(dev):.1e} at s = 0.2, 0.3, {S_CRIT:.3f}. At the ACTUAL SPARC deep-MOND points the")
info(f"        degeneracy is only APPROXIMATE, median |ratio - 1| = {min(devS):.2f}-{max(devS):.2f}, because")
info(f"        the interpolation is not yet asymptotic there. So this is an exact statement about the DEEP")
info(f"        LIMIT and a rough one on the data, and both are reported rather than the flattering one.")
info(f"      So the surviving kernel term, taken on its own, produces its MOND transition at "
     f"a_0' = s^2 a_0 <= {A0_EFF:.3f} a_0")
info(f"      = {A0_EFF*A0['canonical']:.2e} m/s^2 -- a factor {1/A0_EFF:.1f} BELOW the acceleration at "
     f"which the observed RAR turns over.")
info(f"      For that term to still account for the observed turnover the action's a_0 would have to be "
     f"{1/A0_EFF:.1f}x larger,")
info(f"      i.e. kappa = {KAPPA_FIT/A0_EFF:.2f} instead of the fitted {KAPPA_FIT:.4f} -- outside every "
     f"principle-shaped candidate the")
info(f"      coefficient programme carries. What actually happens instead is D7: at f = 1 the BTFR zero "
     f"point is the")
info(f"      HALO's, so the framework's a_0 is no longer MEASURED by galaxy dynamics at all, and kappa "
     f"loses the")
info(f"      empirical anchor (0.465 +/- 0.076 from the BTFR) from which it is quoted.")
check("D5 the kernel that survives at f = 1 is still the deposited theory's kernel, i.e. it carries the "
      "same a_0 and the a_0-Lambda tie still refers to something that acts",
      S_CRIT > 0.9,
      f"it is not. A partial suppression is EXACTLY degenerate with a smaller a_0 in the strict deep-MOND "
      f"limit (verified to {max(dev):.0e}) and roughly so on the data ({min(devS):.0%}-{max(devS):.0%} at "
      f"the actual SPARC deep-MOND points, which are not yet asymptotic), so the surviving kernel has "
      f"a MOND transition at a_0' = s^2 a_0 <= {A0_EFF:.3f} a_0, a factor {1/A0_EFF:.1f} below where the "
      f"observed RAR turns over -- so the surviving term no longer sets the scale it was built to set. "
      f"Making it do so would need kappa = {KAPPA_FIT/A0_EFF:.2f} rather than the fitted {KAPPA_FIT:.4f}. "
      f"The operative consequence is D7's: at f = 1 the BTFR zero point is the HALO's, so the framework's "
      f"a_0 is not measured by galaxy dynamics any more and kappa loses the 0.465 +/- 0.076 BTFR anchor it "
      f"is quoted from. Since kappa is FITTED rather than derived this is not a falsification -- it is the "
      f"loss of the coincidence that motivated the tie")

# ---- D6: the strict criterion, and what it says about f = 1 --------------------------------------------
base_rms = R0["canonical"][0]
rms_f1_nokernel = RH1["canonical"][0]
P("")
info("  D6  THE STRICT CRITERION, stated because the generous one is doing real work above.  L49/L50's")
info("      strict galaxy criterion is 'rms not degraded by more than 0.02 dex against the kernel's own")
info(f"      {base_rms:.3f} dex at f = 0'. At f = 1 with the kernel switched off ENTIRELY the rms is")
info(f"      {rms_f1_nokernel:.3f} dex, already {rms_f1_nokernel - base_rms:.3f} dex worse.")
check("D6 f = 1 is admissible on the STRICT galaxy criterion too, so the opening does not depend on which "
      "of L49's two criteria is used",
      rms_f1_nokernel < base_rms + 0.02,
      f"it is not, and the reason has nothing to do with this mechanism: at f = 1 the abundance-matched "
      f"halo ALONE gives {rms_f1_nokernel:.3f} dex against the kernel's {base_rms:.3f}, so no kernel "
      f"treatment whatever can meet the strict criterion at f = 1. That is a statement about the "
      f"LambdaCDM halo library's scatter, not about the composition kernel, and it means the strict "
      f"criterion cannot be used to test this mechanism. The generous criterion is therefore carried "
      f"throughout, exactly as L49 and L50 carry it")

# ---- the exhibited point's distinctive predictions ------------------------------------------------------
a0c = A0["canonical"]
def btfr_zero(sf, mode, f):
    out = []
    for g in GAL:
        i = int(np.argmax(g["r"]))
        s = 1.0 if sf is None else float(sf(fb_gal(g, f, mode))[i])
        gt = g["gb"][i] + f*g["g_halo"][i] + s*float(kern(g["gb"][i], a0c))
        out.append(np.log10((gt*g["r"][i])**2/(G*g["Mb"]*MSUN*a0c)))
    return float(np.median(out))
BT0 = btfr_zero(None, "enc", 0.0); BT1 = btfr_zero(H1[3], "enc", 1.0); BT2 = btfr_zero(H2b[3], "loc", 1.0)
CAP = {f: D_SAT*A0[f] for f in A0}          # L49 N3: C a_0 = 6.06e-11 / 7.30e-11 m/s^2
over = []
for g in GAL:
    over.append(g["g_halo"] > CAP["canonical"])
FRAC_CAP = float(np.concatenate(over).mean())
n_half = 0; n_dp = 0
for g in GAL:
    m = g["gb"] < a0c; n_dp += int(m.sum())
    n_half += int((H2b[3](fb_gal(g, 1.0, "loc"))[m] > 0.5).sum())
FRAC_HALF = n_half/max(n_dp, 1)
P("")
info("  D7  the framework's THREE distinctive galaxy-scale statements, at the best variant that clears")
info("      f = 1 on both footings (H2', local f_b, s = f_b^4):")
info(f"        deep-MOND BTFR zero point log10[V^4/(G M_b a_0)] : {BT0:+.3f} dex at f = 0 (the theory's own "
     f"prediction) -> {BT2:+.3f} at f = 1")
info(f"        bounded-boost ceiling g_obs - g_N <= C a_0 = {CAP['canonical']:.2e} m/s^2 : "
     f"{100*FRAC_CAP:.0f}% of SPARC points have the HALO term alone above it, so the ceiling is no longer "
     f"a statement about an observable")
info(f"        kernel above half strength in the deep-MOND regime : {100*FRAC_HALF:.0f}% of points")
check("D7 the framework's distinctive galaxy-scale predictions survive at the variant that opens the "
      "pincer: the deep-MOND BTFR zero point, the bounded-boost ceiling, and a kernel that acts",
      abs(BT2 - BT0) < 0.05 and FRAC_CAP < 0.10,
      f"they do not survive as tests. The BTFR zero point moves from {BT0:+.3f} to {BT2:+.3f} dex and is "
      f"now set by the halo, not by V^4 = G M_b a_0; {100*FRAC_CAP:.0f}% of SPARC points have the halo term "
      f"alone above the bounded-boost ceiling, so the falsifier the programme calls the one LambdaCDM "
      f"structurally cannot make becomes a statement about an unobservable (L49 N3, unchanged); and the "
      f"kernel is above half strength at {100*FRAC_HALF:.0f}% of deep-MOND points. What survives is a "
      f"kernel supplying at most {W_CEIL:.2f} of the anomaly with an effective a_0 of {A0_EFF:.2f} a_0")

# D8 -- the gates the deposited theory passes
P("")
info("  D8  the deposited theory's gates, re-run at the exhibited point (H2', local f_b, s = f_b^4, f = 1):")
rho_loc = 0.0093*MSUN/pc**3     # local cold density 0.0093 M_sun/pc^3 (Read 2014 central value)
Msat = rho_loc*4*math.pi/3*(9.5*1.496e11)**3/MSUN
PPN_a1 = -4*C14_X; PPN_a2 = (C14_X/2)*(1/SIG_X - 1)
RMS_X = rms_supp(1.0, 0.0, "canonical", sfun=H2b[3], mode="loc")
gate = {
  "Cassini / sunward / xi": ("PASS", "aether-scalar sector untouched; f_b -> 1 in the Solar System so "
                             "s -> 1 and the local kernel is the deposited theory's"),
  "Saturn phantom mass": ("PASS", f"a smooth cold halo puts {Msat:.2e} M_sun inside Saturn's orbit against "
                          f"Pitjev-Pitjeva's 6.7e-11, margin {6.7e-11/Msat:.0f}x"),
  "alpha_1, alpha_2, alpha_3, gamma": ("PASS", f"unchanged: alpha_1 = -4 c_14 = {PPN_a1:.2e}, "
                                       f"alpha_2 = (c_14/2)(1/sigma - 1) = {PPN_a2:.2e}"),
  "c_T = c (GW170817)": ("PASS", "c_13 = 0; no disformal matter metric; s multiplies a scalar term only"),
  "mode count and health": ("PASS", "2 tensor + 1 clock + 1 scalar + 1 matter DOF; s(f_b) adds no field"),
  "clock tachyon": ("PASS", "Qbar = 0 remains an exact solution: s multiplies the MOND term, which still "
                    "has no homogeneous source (Y = 0 on a homogeneous slice)"),
  "lensing == dynamics": ("PASS", "V-B retains the drag coupling, so Phi = Psi and M_dyn/M_lens = 1"),
  "BBN": ("PASS", f"Delta N_eff = 0; and B3, the kernel's fractional size at BBN-era accelerations is "
          f"{KFRAC_BBN:.1e}"),
  "rotation curves": ("PASS", f"at f = 1, rms {RMS_X[0]:.3f} dex, median {RMS_X[1]:+.3f} -- but D3 shows "
                      f"{100*WH1:.0f}% of the anomaly is the halo's"),
  "cluster amount": ("PASS", f"f = {H2b[1][0]:.3f} +/- {H2b[1][1]:.3f} at b = 0, "
                     f"{abs(H2b[1][0]-1)/H2b[1][1]:.1f} sigma from the CMB's 1.000"),
  "CMB cold-matter density": ("PASS", "Omega_c h^2 = 0.1200 at f = 1 -- the gate L49 and L50 both FAIL"),
  "linear growth / sigma_8": ("PASS", "S_eff = 0 on the closure locus, so growth is algebraically LambdaCDM's"),
  "conservation / Bianchi": ("PASS", "diffeomorphism invariance of the Lagrangian is untouched by making J "
                             "depend on two matter scalars, so grad.T(total) = 0 exactly as in L50 B2"),
  "cold component is dust": ("FAIL", "NEW HERE -- see D9: ds/drho_c gives the cold component its own fifth "
                             "force, so it is no longer the pressureless dust the halo library assumes"),
}
npass = sum(1 for v in gate.values() if v[0] == "PASS")
for k, (v, d) in gate.items():
    info(f"      {k:<34s} {v:<5s}  {d}")
check("D8 every gate the deposited theory is run against still passes at the exhibited point",
      npass == len(gate),
      f"{npass} of {len(gate)} do, including the two that L49 and L50 FAIL outright (the CMB cold-matter "
      f"density and linear growth) and including conservation, which survives because diffeomorphism "
      f"invariance does not care how many matter scalars J reads. The one that fails is NEW to this "
      f"mechanism and is the subject of D9")

# D9 -- the new gate this mechanism creates
P("")
info("  D9  THE GATE THIS MECHANISM CREATES.  If the kernel's strength depends on rho_c, then varying the")
info("      action with respect to the cold sector gives it a force it did not have:")
P("        delta S / delta rho_c  includes  (ds/drho_c) J(Y)   =>   the cold component feels a MOND-scale")
P("        fifth force of order (dln s / dln rho_c) x (the phantom acceleration the kernel supplies).")
dlnsdlnrc = {}
for p_ in (3.0, 4.0):
    fbv = np.array([0.15, 0.3, 0.5, 0.8])
    dlnsdlnrc[p_] = p_*(1 - fbv)     # for s = f_b^p and f_b = rho_b/(rho_b+rho_c)
info(f"        for s = f_b^p, dln s/dln rho_c = -p(1 - f_b): at p = 4 that is "
     + ", ".join(f"{-v:.2f} at f_b = {b:.2f}" for v, b in zip(dlnsdlnrc[4.0], np.array([0.15,0.3,0.5,0.8]))))
info(f"        and the kernel supplies W = {W_H2b:.2f} of the anomaly there, so the extra acceleration on")
info(f"        the cold component is of order {4.0*(1-0.5)*W_H2b:.2f} of the anomaly itself -- an O(1)")
info(f"        effect, not a correction.")
check("D9 the cold component remains pressureless dust under this action, so the abundance-matched "
      "LambdaCDM halo library used for every number in this lane is self-consistent",
      False,
      f"it does not. A kernel whose strength reads rho_c gives the cold component a fifth force of order "
      f"|dln s/dln rho_c| x W ~ {4.0*(1-0.5)*W_H2b:.1f} of the anomaly at p = 4 -- O(1). Every halo profile "
      f"used here (Moster abundance matching, Dutton-Maccio concentration, NFW) is built for dust in "
      f"Newtonian gravity, so under this action the halo library is NOT self-consistent and the cluster "
      f"and galaxy windows would have to be recomputed with a re-equilibrated halo. This is an ESTIMATE of "
      f"the size, not a solved profile: it is flagged as the mechanism's own unpaid bill, and it is the "
      f"reason the D2 opening should not be read as a working theory")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART E -- THE PRICE.")
P("=" * 122)
etas = []
for g in GAL:
    s = H2b[3](fb_gal(g, 1.0, "loc")); k = s*kern(g["gb"], a0c)
    etas.append(k/(g["gb"] + g["g_halo"] + k))
ETA = float(np.median(np.concatenate(etas)))
etas_L50 = [kern(g["gb"], a0c)/(g["gb"] + g["g_halo"] + kern(g["gb"], a0c)) for g in GAL]
ETA_L50 = float(np.median(np.concatenate(etas_L50)))
P("")
info("  E1  EQUIVALENCE PRINCIPLE.  A kernel whose STRENGTH depends on species composition violates the WEP")
info("      in the gravitational sector twice over, where L50's baryon sourcing violated it once:")
info("        (a) baryons feel the kernel and the cold component does not -- L50's violation, inherited;")
info("        (b) NEW HERE: the force on a BARYON depends on how much OTHER-species matter is nearby. Two")
info("            identical baryonic configurations with the same g_bar accelerate differently according")
info("            to the local cold density, so the field a test particle feels is not a functional of the")
info("            metric and the scalar alone -- the force law reads the matter census.")
info(f"        magnitude at f = 1: median kernel share of the total acceleration eta = {ETA:.3f} "
     f"(L50 at f = 1 without suppression: {ETA_L50:.3f}).")
info(f"        Neither is a laboratory or Solar-System effect: it takes a cold overdensity comparable to")
info(f"        the local baryon density, and there is {Msat:.1e} M_sun of cold matter inside Saturn's orbit")
info(f"        against Pitjev-Pitjeva's 6.7e-11 ({6.7e-11/Msat:.0f}x margin). Baryons and photons stay")
info(f"        minimally coupled to the single metric g, so gamma_PPN, Eotvos and MICROSCOPE are untouched.")
check("E1 the equivalence-principle cost is confined to the dark sector and is no worse in kind than "
      "L50's single between-sector violation",
      False,
      f"it is confined to the dark sector EMPIRICALLY -- no laboratory or Solar-System test fires, margin "
      f"{6.7e-11/Msat:.0f}x on the Saturn bound -- but it is worse IN KIND. L50's violation is that two "
      f"species fall differently. This lane adds a second, sharper one: the acceleration of a baryon "
      f"depends on the abundance of a species it is not made of, so the gravitational field is not "
      f"determined by the total stress-energy even in principle. Magnitude eta = {ETA:.2f}. Priced as a "
      f"structural cost, not an empirical one")

P("")
info("  E2  FREE FUNCTIONS AND PARAMETERS, counted against the deposited theory:")
info("        deposited theory       : kernel J(Y) fixed; a_0 = kappa c sqrt(G rho_Lambda), kappa FITTED")
info("        + L49's cold component : + M200(M_star), a free function of host mass (abundance matching),")
info("                                 i.e. LambdaCDM's galaxy-formation sector inherited wholesale")
info("        + L50's re-sourcing    : + one chosen coefficient (V-B's compensator); no exactness needed")
info("        + L55's s(f_b)         : + ONE NEW FREE FUNCTION of a composition variable, carrying a scale")
info("                                 (f*) and a sharpness (n or p), neither predicted by the action")
info(f"        and the value it must hit is not free either: D4 fixes s_eff <= {S_CRIT:.3f}, delivered on")
info(f"        the local reading only near p = 4 at h_z ~ 0.3 kpc. Across C4's observed range of disc")
info(f"        scale heights the same p = 4 gives s_eff from {LOCTAB[0.15]**4:.2f} (h_z = 0.15 kpc) to "
     f"{LOCTAB[1.00]**4:.2f} (h_z = 1.0 kpc),")
info(f"        so the one number the mechanism must hit is set by an ASTROPHYSICAL nuisance parameter.")
check("E2 the new function is fixed by the theory rather than fitted -- s(f_b) has a derivation and not "
      "merely a shape, and the value it must take is set by the action",
      False,
      f"it is not. s(f_b) is a new free function introduced for the single purpose of suppressing the term "
      f"the theory exists to produce; no symmetry of the deposited action selects it, and in L6's own "
      f"words a function of two variables at once 'is a fitted function rather than a screening "
      f"mechanism'. Worse, the number it has to hit (s_eff <= {S_CRIT:.3f}) is delivered on the local "
      f"reading only for a particular disc thickness: at fixed p = 4, s_eff runs from "
      f"{LOCTAB[0.15]**4:.2f} to {LOCTAB[1.00]**4:.2f} across h_z = 0.15-1.0 kpc, a factor "
      f"{LOCTAB[0.15]**4/max(LOCTAB[1.00]**4,1e-9):.1f}, so the mechanism's success is controlled by disc "
      f"scale height, about which the action says nothing")

P("")
info("  E3  OBSERVABILITY.  Fraction of SPARC points at which the kernel contributes more than 10% of the")
info("      total acceleration:")
for lab, sf, mode, ff in (("deposited theory (f = 0)", None, "enc", 0.0),
                          ("L50 (f = 1, no suppression)", None, "enc", 1.0),
                          ("H1  (f = 1, enclosed, p = 3)", H1[3], "enc", 1.0),
                          ("H2' (f = 1, local, p = 4)", H2b[3], "loc", 1.0)):
    fv = []
    for g in GAL:
        s = 1.0 if sf is None else sf(fb_gal(g, ff, mode))
        k = s*kern(g["gb"], a0c); fv.append(k/(g["gb"] + ff*g["g_halo"] + k) > 0.10)
    info(f"        {lab:<32s} {100*float(np.concatenate([np.atleast_1d(x) for x in fv]).mean()):5.1f}% of points")
check("E3 the kernel remains observationally distinguishable at the variant that opens the pincer",
      FRAC_HALF > 0.5,
      f"partially, and this is the fairest statement of what survives. On the LOCAL horn the kernel is "
      f"still above half strength at {100*FRAC_HALF:.0f}% of deep-MOND points and supplies W = "
      f"{W_H2b:.2f} of the anomaly, so it is not switched off -- but D5 shows what survives is "
      f"observationally a kernel with a_0' = {A0_EFF:.2f} a_0, and D7 shows the three statements the "
      f"framework calls distinctive (BTFR zero point, bounded-boost ceiling, RAR at zero parameters) are "
      f"set by the halo at that abundance. On the ENCLOSED horn the kernel is above half strength at 0% "
      f"of deep-MOND points and W = {W_H1:.3f}: switched off entirely")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART V -- VERDICT, AND THE THEOREM.")
P("=" * 122)
check("V1 [THE LANE'S QUESTION] the kernel can be suppressed where cold matter dominates in a way that "
      "lets the galaxy window reach f = 1 WHILE LEAVING THE GALAXY-SCALE MOND PHENOMENOLOGY INTACT",
      max(W_H1, W_H2b) > 0.7,
      f"NO, and the two halves separate cleanly. The mechanism IS outside L6's closed class (B1-B4), and "
      f"it DOES open the three-way intersection (D2): on the local reading with s = f_b^4 the galaxy "
      f"ceiling is {H2b[0]['canonical']:.3f} / {H2b[0]['alt']:.3f}, clusters need {H2b[1][0]:.3f} +/- "
      f"{H2b[1][1]:.3f}, the CMB fixes 1.000, and every gate the deposited theory passes still passes. But "
      f"'intact' fails: the kernel's share of the observed deep-MOND anomaly is capped at W <= "
      f"{W_CEIL:.3f} on both footings (D4), against {W0:.3f} in the deposited theory, because the halo at "
      f"the CMB's own abundance already supplies {100*WH1:.0f}% of that anomaly. What survives is "
      f"a kernel whose own MOND transition sits at a_0' <= {A0_EFF:.2f} a_0 (D5), while the observed "
      f"turnover, the BTFR zero point and the bounded-boost ceiling are all the halo's (D7) -- so the "
      f"a_0-Lambda tie loses the galaxy measurement kappa is quoted from")

check("V2 the pincer can be opened while the MOND sector still does MOST of the galaxy-scale dynamical "
      "work, on ANY function of ANY variable, environmental or compositional",
      W_CEIL > 0.5,
      f"it cannot, and D4 shows this is a bound rather than a failed search: eleven functions on two "
      f"readings of f_b all land on the single uniform-suppression curve at their own median deep-MOND "
      f"strength, to within {MAXDEV_F:.3f} in the ceiling and {MAXDEV_W:.3f} in W. The galaxy data "
      f"constrain exactly ONE number, and f = 1 on both footings forces it below {S_CRIT:.3f}, hence "
      f"W <= {W_CEIL:.3f}")

P("")
info("  V3  THE THEOREM, stated generally because the programme deserves the statement rather than one")
info("      more dead mechanism:")
wrap("The observed galaxy-scale anomaly is ONE number per point, g_obs - g_bar.  At the cold abundance the "
     f"CMB fixes, the abundance-matched LambdaCDM halo alone already supplies {100*WH1:.0f}% of it and "
     f"reproduces SPARC at {RH1['canonical'][0]:.3f} dex with median {RH1['canonical'][1]:+.3f}.  Whatever "
     "the MOND kernel adds at that abundance is therefore an overshoot, and the galaxy window can be "
     f"reached only by suppressing the kernel to an effective strength s_eff <= {S_CRIT:.3f} where the "
     "anomaly is measured.  That bound is a statement about the DATA and the halo, not about the kernel's "
     "functional form: D4 verifies that eleven suppression functions, keyed to two different composition "
     "variables, all reduce to the same one number as far as the galaxy data are concerned.  It is "
     "therefore invariant under every remaining move -- re-sourcing the scalar (L50), screening on an "
     "environmental scalar (L6), or keying the kernel to the species composition (this lane).  Each is "
     "only a different way of choosing s_eff.", 6)
P("")
wrap(f"HENCE, quantitatively: at Omega_c h^2 = 0.1200 the kernel may supply at most W = {W_CEIL:.2f} of the "
     f"observed deep-MOND galaxy anomaly, against {W0:.2f} in the theory without a cold component; and "
     f"because a partial suppression is exactly degenerate with a smaller a_0 in the deep-MOND limit, the "
     f"surviving term's own MOND transition sits at a_0' <= {A0_EFF:.2f} a_0, a factor {1/A0_EFF:.1f} "
     f"below where the observed relation turns over, and the turnover, the BTFR zero point and the "
     f"bounded-boost ceiling are all set by the halo instead.  A FULL COLD ABUNDANCE AND A MOND KERNEL "
     f"DOING THE GALAXY WORK ARE ALTERNATIVES, NOT COMPLEMENTS -- not because the pincer stays shut, but "
     f"because they are two explanations of the SAME measured excess and the excess can only be spent "
     f"once.  The theory can have the CMB, the clusters and the growth of structure, at which point its "
     f"kernel is at most a third-strength correction whose own MOND scale is five times too small, and "
     f"none of its "
     f"distinctive predictions survives as a test; or it can have the galaxy phenomenology at f = 0, at "
     f"which point S_eff = 0 exactly and it fails the CMB and linear growth outright.", 6)
P("")
wrap("What is NOT claimed.  Nothing here favours this framework over LambdaCDM and nothing here constrains "
     "LambdaCDM: the cold component, its abundance-matched profile and its stellar-to-halo-mass relation "
     "are LambdaCDM's, imported wholesale, and a per-galaxy NFW with two free parameters reaches 0.061 dex "
     "where the kernel reaches 0.145 (L28 / L49 W1).  Nor is this a closure of MOND-like theories in "
     "general: it closes the combination of THIS action's kernel with a full cold abundance whose galaxy "
     "profile is LambdaCDM's.  A theory whose cold component is distributed differently -- less in "
     "galaxies, more elsewhere -- is not covered, though L49's specification and the 2026-09-06/07 "
     "dark-sector no-go between them close every mechanism so far proposed for making one.  And the "
     "opening exhibited in D2 is a real result that should not be talked away: the pincer that closed L49 "
     "and L50 does open, on a mechanism genuinely outside L6's class.  It is the price, not the "
     "arithmetic, that makes it not worth taking.", 6)

P("")
info("  CAVEATS, stated rather than buried:")
info("    1. The GENEROUS of L49's two galaxy criteria (|median| < 0.11 dex) is carried throughout, so the")
info("       candidate is not handed a manufactured deficit. D6 shows the strict criterion cannot be used")
info("       here at all: at f = 1 the halo ALONE already misses it, independently of any kernel.")
info("    2. The local-midplane f_b uses SBdisk/SBbul photometry for stars and a thin-disc inversion of")
info("       V_gas for gas, at a fixed scale height. C4 varies h_z over 0.15-1.00 kpc and E2 shows the")
info("       mechanism's key number s_eff swings by a large factor across that range -- so the local")
info("       horn's success is h_z-controlled and is reported as such, not as a robust result.")
info("    3. Abundance matching carries ~0.30 dex of systematic on log M200 (Moster vs Behroozi vs")
info("       Kravtsov). It moves the galaxy ceiling and the cluster requirement together. It does not")
info("       touch the theorem, which is about the halo ALREADY supplying the anomaly at f = 1.")
info("    4. D9's fifth force on the cold component is an ORDER-OF-MAGNITUDE estimate from dln s/dln rho_c,")
info("       not a solved profile. It is the mechanism's largest unpaid bill and it is flagged, not")
info("       resolved: every halo number in this lane assumes dust, which under this action it is not.")
info("    5. Cluster windows use the enclosed baryon fraction inside the same 1000 kpc aperture as L50, at")
info("       b = 0 and b = 0.20. The hydrostatic bias is not resolved here.")
info("    6. The kernel, its saturation constant and the closure locus are the deposited theory's,")
info("       unchanged; nothing here re-fits them, and kappa remains FITTED (0.4998 / 0.6023).")

P("")
P("=" * 122)
P(f"RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
P("=" * 122)
sys.exit(0)
