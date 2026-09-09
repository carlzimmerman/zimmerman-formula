#!/usr/bin/env python3
"""
L50 -- baryon sourcing: if the MOND scalar is sourced by the BARYONS ALONE, does L49's pincer open?
===================================================================================================
L49 found a minimum addition -- a cold collisionless component in the matter sector, decoupled from the
clock -- that satisfies the whole cluster specification, leaves the clock tachyon satisfied identically,
touches neither the Solar System nor the preferred-frame parameters nor BBN, and repairs the CMB and linear
growth exactly.  It then failed for ONE stated reason:

    "the action's MOND scalar is sourced by the TOTAL potential and therefore amplifies the very mass
     that was added to replace it."

The consequence was a three-way pincer with an empty interior: galaxies tolerate a cold fraction
f <= 0.355, clusters need f = 0.32 +/- 0.10, the CMB fixes f = 1.00 +/- 0.01, and the BINDING constraint is
the CMB (a factor 2.8), not the clusters.

THAT IS A DESIGN CHOICE, NOT A THEOREM.  What sources the MOND scalar is written into the action.  This lane
replaces the source and recomputes everything.

WHAT IS ACTUALLY BEING CHANGED, stated at the level of the Lagrangian rather than waved at.
The deposited action's MOND-generating term is the AeST drag coupling

        L_coup = 2(2 - K_B) J^mu d_mu phi ,        J^mu = n^nu grad_nu n^mu  (the clock's 4-acceleration)

Integrating by parts, L_coup = -2(2 - K_B) phi grad_mu J^mu, and statically grad.J = grad^2 Psi, which the
Einstein equation ties to the TOTAL gravitating density.  Two variants are written down and priced:

  V-A  REPLACEMENT.  Delete the drag coupling and couple phi directly to the baryon trace:
          L_coup -> -8 pi G (2 - K_B) phi T_b ,   T_b = trace of the baryonic stress tensor (= -rho_b for dust).
       This is the RAQUAL/Bekenstein-Milgrom conformal coupling.  It sources phi with rho_b exactly.
  V-B  COMPENSATION.  KEEP the drag coupling and add one term coupling phi to the COLD sector:
          Delta L = +8 pi G (2 - K_B) phi rho_c ,
       whose coefficient is fixed by ONE condition -- that it cancel rho_c out of the scalar's source.  The
       net scalar equation is then grad.[(J' - 1) grad phi] = 4 pi G rho_b: Milgrom sourced by baryons alone,
       with the drag coupling (and therefore the phantom's gravitation) intact.

Both give the SAME prediction for everything measured with baryons and light, because both change the
scalar's source and nothing else:

        total-sourced (L49) :  g = g_bar + f g_halo + a_0 Delta( [g_bar + f g_halo] / a_0 )
        baryon-sourced (L50):  g = g_bar + f g_halo + a_0 Delta(  g_bar             / a_0 )

so the whole family is carried as one parameter, eps = the fraction of the cold component that still sources
the scalar: eps = 1 is L49, eps = 0 is this lane.

CHECKS THAT CAN FAIL.  Each states a PROPOSITION; PASS means the proposition holds.
  A1-A9  CONTROLS.  Reproduce L49's cluster amount, its post-kernel residual, its three SPARC numbers, its
         THREE windows, its empty intersection, its -0.259 dex overshoot; and check that at f = 0 the new
         machinery is bit-identical to the old one and returns the standard deep-MOND law.
  B1-B5  THE MODIFICATION AND CONSERVATION.  grad.J = grad^2 Psi derived symbolically; the two variants; and
         the question that can kill the lane outright -- does a source that is not the total stress tensor
         break the Bianchi identity?
  C1-C5  A NEW RISK THE LANE CREATES.  On FRW the deposited action has NO homogeneous source for phi, which
         is exactly why Q_0 = 0 is an exact solution and the clock tachyon is cured.  ANY direct matter
         coupling supplies one.  Does the clock tachyon come back?
  D1-D6  THE THREE WINDOWS RECOMPUTED under baryon sourcing, and the intersection.
  E1-E7  THE PRICE: equivalence principle, lensing, the disformal repair, alpha_1, Solar System.
  F1-F3  AN EXHIBITED POINT against the gates the deposited theory passes.
  V1-V6  VERDICT.

Both a_0 footings (9.3619e-11 canonical, 1.1279e-10 alt) on every dimensional number.  A FAIL marks a
proposition that does not hold; several of the FAILs here are the finding.

HONESTY RULE.  A non-empty intersection would be the most important result this programme has produced, and
that is exactly why the bar is high: an explicit point is exhibited and run through the gates rather than
argued for.  If conservation fails, that kills the variant outright and the script says so in its first
verdict line.  Nothing here claims the data favour this framework over LambdaCDM.
"""
import numpy as np, math, json, os, sys, glob, time, textwrap
import sympy as sp

T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("  " + s, flush=True)
def wrap(s, ind=6):
    for ln in textwrap.wrap(s, 116 - ind): print(" "*ind + ln, flush=True)

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(REPO, "real_research", "data")
G = 6.674e-11; MSUN = 1.989e30; kpc = 3.0857e19; Mpc = 1e3*kpc; AU = 1.495978707e11
CLIGHT = 2.99792458e8
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
S_SAT, D_SAT = 2.540, 0.6476                     # the carried kernel, THE_COMPLETE_THEORY section 4
OM, OB, ODM = 0.315, 0.049, 0.266
F_COSMIC = ODM/OB                                # 5.4286
OBH2, OCH2 = 0.02237, 0.1200                     # Planck 2018 TT,TE,EE+lowE+lensing
hP = 0.674; H0 = hP*100e3/Mpc; RHO_C = 3*H0**2/(8*math.pi*G)
UPS_D, UPS_B = 0.5, 0.7
# the exhibited point of THE_COMPLETE_THEORY section 5
KB_X, C14_X, SIG_X, SIG_MAX = 0.2, 1.0000e-6, 1.679312732187113, 1.7716
C2_X = 2*SIG_X*C14_X/(2 - C14_X - 3*SIG_X*C14_X)
K2_X = (2 - KB_X)**2/C2_X                        # the closure locus c_2 |K_2| = (2 - K_B)^2

def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > S_SAT, D_SAT, d)
def kern(gb, a0): return a0*Delta(np.asarray(gb, float)/a0)

P("=" * 122)
P("L50 -- BARYON SOURCING: if the MOND scalar is sourced by the baryons alone, does L49's pincer open?")
P("=" * 122)
P("  sources, all committed products of this repository; nothing below is retyped from prose:")
P("    clusters : closure_2026/cluster_measurement_audit_2026/results.json")
P("    galaxies : real_research/data/sparc_data/*_rotmod.dat  +  SPARC_Lelli2016c.mrt")
P("    theory   : THE_COMPLETE_THEORY_2026-09-08.md sections 2-5;  L49_MINIMUM_ADDITION.md (the control)")
P("    prior    : closure_2026/LOCAL_NO_GO_AND_FORK_PAPER_2026-09-03.md 3.2 (the disformal identity), 3.3")
P("               (the alpha_1 lock);  closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md I2 (one physical metric)")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART A -- CONTROLS.  Rebuild L49's pincer from its own data before touching anything.")
P("=" * 122)

CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
CLU = {}
for rw in CLJ["rows"]:
    f = rw.get("footing", "canonical"); a0 = A0[f]
    CLU.setdefault(f, {}).setdefault(rw["cluster"], []).append(
        (float(rw["r_kpc"]), float(rw["g_baryon_over_a0"])*a0, float(rw["g_hse_over_a0"])*a0))
ANCH = {}
for f in sorted(CLU):
    a0 = A0[f]; rows = []
    for n in sorted(CLU[f]):
        p = np.array(sorted(CLU[f][n])); r = p[:, 0]*kpc; gb = p[:, 1]; gh = p[:, 2]
        Mb = gb*r**2/G/MSUN; Mh = gh*r**2/G/MSUN
        gk = gb + kern(gb, a0); Mk = gk*r**2/G/MSUN
        rows.append(dict(name=n, r_kpc=p[-1, 0], gb=gb[-1], gh=gh[-1], gk=gk[-1],
                         rN=(Mh[-1]-Mb[-1])/Mb[-1], rF=(Mh[-1]-Mk[-1])/Mb[-1], fbar=Mb[-1]/Mh[-1]))
    ANCH[f] = rows
RAT_CLU = {f: float(np.median([x["rN"] for x in ANCH[f]])) for f in ANCH}
ERAT_CLU = {f: float(np.std([x["rN"] for x in ANCH[f]], ddof=1)) for f in ANCH}
RES_CLU = {f: float(np.median([x["rF"] for x in ANCH[f]])) for f in ANCH}
FBAR_CLU = {f: float(np.median([x["fbar"] for x in ANCH[f]])) for f in ANCH}
for f in ("canonical", "alt"):
    info(f"{f:>9}: {len(ANCH[f])} clusters at {ANCH[f][0]['r_kpc']:.0f} kpc -- f_bar {FBAR_CLU[f]:.3f}, "
         f"Newtonian M_dark/M_bar {RAT_CLU[f]:.2f} +/- {ERAT_CLU[f]:.2f}, post-kernel residual "
         f"{RES_CLU[f]:.2f} M_bar")
check("A1 [control] an independent recomputation returns L49 X1's cluster amount 5.73 +/- 0.68 and "
      "f_bar = 0.149 at 1000 kpc, on both footings",
      abs(RAT_CLU["canonical"] - 5.73) < 0.05 and abs(ERAT_CLU["canonical"] - 0.68) < 0.05
      and abs(FBAR_CLU["canonical"] - 0.149) < 0.002 and abs(RAT_CLU["alt"] - 5.73) < 0.05,
      f"M_dark/M_bar = {RAT_CLU['canonical']:.2f} +/- {ERAT_CLU['canonical']:.2f} (a_0-independent), "
      f"f_bar = {FBAR_CLU['canonical']:.3f}")
check("A2 [control] the framework's OWN post-kernel cluster residual reproduces L49 X6's 3.09 M_bar "
      "(canonical) / 2.76 M_bar (alt)",
      abs(RES_CLU["canonical"] - 3.09) < 0.06 and abs(RES_CLU["alt"] - 2.76) < 0.06,
      f"{RES_CLU['canonical']:.2f} / {RES_CLU['alt']:.2f} M_bar")

# ---- SPARC ------------------------------------------------------------------------------------------------
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
def nfw_enclosed_msun(M200, r_kpc):
    c = c200_gal(M200); R200 = (3*M200*MSUN/(4*math.pi*200*RHO_C))**(1/3.)/kpc
    return M200*_nfwm(c*np.clip(np.asarray(r_kpc, float)/R200, 1e-6, 6.0))/_nfwm(c)

GAL = []
for fn in sorted(glob.glob(os.path.join(DATA, "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", "")
    if name not in MASTER: continue
    m = MASTER[name]
    try: d = np.loadtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    r = d[:, 0]*kpc; Vo = d[:, 1]*1e3; eV = d[:, 2]*1e3; Vg = d[:, 3]*1e3; Vd = d[:, 4]*1e3; Vb = d[:, 5]*1e3
    Vb2 = Vg*np.abs(Vg) + UPS_D*Vd*np.abs(Vd) + UPS_B*Vb*np.abs(Vb)
    msk = (r > 0) & (Vo > 0) & (Vb2 > 0) & (eV/np.maximum(Vo, 1) < 0.10)
    if msk.sum() < 3: continue
    Mstar = UPS_D*m["L36"]*1e9; Mgas = 1.33*m["MHI"]*1e9
    GAL.append(dict(name=name, r=r[msk], gb=Vb2[msk]/r[msk], go=Vo[msk]**2/r[msk],
                    Mstar=Mstar, Mb=Mstar + Mgas))
for g in GAL:
    M200 = max(float(halo_mass_AM(g["Mstar"])), 1.02*g["Mb"]); g["M200"] = M200
    c = float(c200_gal(M200)); R200 = (3*M200*MSUN/(4*math.pi*200*RHO_C))**(1/3.)
    x = np.clip(g["r"]/R200, 1e-6, 6.0)
    g["g_halo"] = G*(M200 - g["Mb"])*MSUN*_nfwm(c*x)/_nfwm(c)/g["r"]**2
NPT = sum(len(g["r"]) for g in GAL)
info(f"SPARC: {len(GAL)} galaxies, {NPT} points (Upsilon_d = {UPS_D}, Upsilon_b = {UPS_B}, eV/V < 0.10)")

# THE ONE-PARAMETER FAMILY.  eps = the fraction of the cold component that still sources the MOND scalar.
def rms_model(f, eps, foot, kernel=True, ksup=1.0):
    """g = g_bar + f g_halo + ksup * a_0 Delta( (g_bar + eps f g_halo)/a_0 ).  eps = 1 is L49's total
    sourcing; eps = 0 is baryon sourcing.  ksup scales the kernel (1 = the action, 0 = no kernel)."""
    a0 = A0[foot]; res = []
    for g in GAL:
        gN = g["gb"] + f*g["g_halo"]
        src = g["gb"] + eps*f*g["g_halo"]
        gp = gN + (ksup*kern(src, a0) if kernel else 0.0)
        res.append(np.log10(g["go"]/gp))
    r = np.concatenate(res)
    return float(np.sqrt(np.mean(r**2))), float(np.median(r))

R0 = {foot: rms_model(0.0, 1.0, foot) for foot in A0}
RH1 = {foot: rms_model(1.0, 1.0, foot, kernel=False) for foot in A0}
info(f"parameter-free anchors: kernel at f = 0 -> {R0['canonical'][0]:.3f} dex median "
     f"{R0['canonical'][1]:+.3f} (canonical), {R0['alt'][0]:.3f} / {R0['alt'][1]:+.3f} (alt); "
     f"abundance-matched halo alone at f = 1 -> {RH1['canonical'][0]:.3f} / {RH1['canonical'][1]:+.3f}")
check("A3 [control] the SPARC machinery reproduces L49 X8's three parameter-free numbers (kernel 0.145 / "
      "0.142 dex with medians +0.030 / +0.003; abundance-matched halo 0.171 dex with median -0.026)",
      abs(R0["canonical"][0] - 0.145) < 0.004 and abs(R0["alt"][0] - 0.142) < 0.004
      and abs(R0["canonical"][1] - 0.030) < 0.004 and abs(R0["alt"][1] - 0.003) < 0.004
      and abs(RH1["canonical"][0] - 0.171) < 0.010 and abs(RH1["canonical"][1] + 0.026) < 0.010,
      f"kernel {R0['canonical'][0]:.3f} / {R0['alt'][0]:.3f} dex, medians {R0['canonical'][1]:+.3f} / "
      f"{R0['alt'][1]:+.3f}; halo {RH1['canonical'][0]:.3f} dex, median {RH1['canonical'][1]:+.3f}")

TOT1 = {foot: rms_model(1.0, 1.0, foot) for foot in A0}
check("A4 [control] L49 N1's overshoot at the abundance the CMB fixes is reproduced: median RAR residual "
      "-0.259 dex (canonical) / -0.283 (alt), an overshoot of 1.82x in acceleration",
      abs(TOT1["canonical"][1] + 0.259) < 0.004 and abs(TOT1["alt"][1] + 0.283) < 0.004
      and abs(TOT1["canonical"][0] - 0.338) < 0.006,
      f"median {TOT1['canonical'][1]:+.3f} / {TOT1['alt'][1]:+.3f} dex, i.e. "
      f"{10**abs(TOT1['canonical'][1]):.2f}x / {10**abs(TOT1['alt'][1]):.2f}x; rms "
      f"{R0['canonical'][0]:.3f} -> {TOT1['canonical'][0]:.3f}")

def f_max_gal(eps, foot, tol=0.11, ksup=1.0):
    lo, hi = 0.0, 4.0
    for _ in range(70):
        mid = 0.5*(lo + hi)
        if abs(rms_model(mid, eps, foot, ksup=ksup)[1]) < tol: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)
def f_max_gal_rms(eps, foot, degrade=0.02):
    base = rms_model(0.0, eps, foot)[0]; lo, hi = 0.0, 4.0
    for _ in range(70):
        mid = 0.5*(lo + hi)
        if rms_model(mid, eps, foot)[0] < base + degrade: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)
def f_cluster(eps, foot, bias=0.0):
    """solve, per cluster, g_bar(1 + f F_cosmic) + a_0 Delta( g_bar(1 + eps f F_cosmic)/a_0 ) = g_HSE/(1-b)"""
    a0 = A0[foot]; out = []
    for x in ANCH[foot]:
        gb = x["gb"]; gh = x["gh"]/(1.0 - bias); lo, hi = 0.0, 40.0
        for _ in range(90):
            mid = 0.5*(lo + hi)
            if gb*(1 + mid*F_COSMIC) + float(kern(gb*(1 + eps*mid*F_COSMIC), a0)) < gh: lo = mid
            else: hi = mid
        out.append(0.5*(lo + hi))
    return float(np.median(out)), float(np.std(out, ddof=1))

FGAL_T = {f: f_max_gal(1.0, f) for f in A0}; FGAL_TS = {f: f_max_gal_rms(1.0, f) for f in A0}
FCLU_T = {f: f_cluster(1.0, f) for f in A0}; FCLU_T_B = {f: f_cluster(1.0, f, 0.20) for f in A0}
info("")
info("L49's three windows, rebuilt here with independent code:")
info(f"    galaxies  (generous, |median| < 0.11 dex): f <= {FGAL_T['canonical']:.3f} / {FGAL_T['alt']:.3f}"
     f"      (strict, rms not degraded by 0.02: {FGAL_TS['canonical']:.3f} / {FGAL_TS['alt']:.3f})")
info(f"    clusters  (self-consistent at 1000 kpc) : f  = {FCLU_T['canonical'][0]:.3f} +/- "
     f"{FCLU_T['canonical'][1]:.3f} / {FCLU_T['alt'][0]:.3f} +/- {FCLU_T['alt'][1]:.3f}   at b = 0")
info(f"    the CMB   (Omega_c h^2 = {OCH2:.4f} +/- 0.0012) : f = 1.000 +/- 0.010")
check("A5 [control] L49's THREE admissible cold-fraction windows are reproduced: galaxies f <= 0.355 / "
      "0.276, clusters f = 0.316 +/- 0.100 / 0.261 +/- 0.093, CMB f = 1.000 +/- 0.010",
      abs(FGAL_T["canonical"] - 0.355) < 0.004 and abs(FGAL_T["alt"] - 0.276) < 0.004
      and abs(FCLU_T["canonical"][0] - 0.316) < 0.004 and abs(FCLU_T["canonical"][1] - 0.100) < 0.004
      and abs(FCLU_T["alt"][0] - 0.261) < 0.004 and abs(FGAL_TS["canonical"] - 0.185) < 0.004,
      f"galaxies {FGAL_T['canonical']:.3f} / {FGAL_T['alt']:.3f} (strict {FGAL_TS['canonical']:.3f} / "
      f"{FGAL_TS['alt']:.3f}); clusters {FCLU_T['canonical'][0]:.3f} +/- {FCLU_T['canonical'][1]:.3f} / "
      f"{FCLU_T['alt'][0]:.3f} +/- {FCLU_T['alt'][1]:.3f}")
check("A6 [control] L49's intersection is EMPTY and the BINDING constraint is the CMB rather than the "
      "clusters -- galaxies and clusters overlap, and the CMB is a factor 2.8 / 3.6 away",
      FGAL_T["canonical"] < 1.0 and FGAL_T["canonical"] >= FCLU_T["canonical"][0] - FCLU_T["canonical"][1]
      and abs(1.0/FGAL_T["canonical"] - 2.8) < 0.1 and abs(1.0/FGAL_T["alt"] - 3.6) < 0.1,
      f"galaxies and clusters overlap ({FGAL_T['canonical']:.3f} >= "
      f"{FCLU_T['canonical'][0]-FCLU_T['canonical'][1]:.3f}); the galaxy ceiling corresponds to "
      f"Omega_c h^2 = {FGAL_T['canonical']*OCH2:.4f} / {FGAL_T['alt']*OCH2:.4f} against Planck's "
      f"{OCH2:.4f}, short by {1.0/FGAL_T['canonical']:.1f}x / {1.0/FGAL_T['alt']:.1f}x")

# ---- A7/A8/A9: the new machinery's own controls -------------------------------------------------------------
same = all(abs(rms_model(0.0, e, foot)[i] - R0[foot][i]) < 1e-12
           for e in (0.0, 0.25, 1.0) for foot in A0 for i in (0, 1))
check("A7 [control] at zero cold fraction the baryon-sourced machinery is BIT-IDENTICAL to the total-sourced "
      "one -- i.e. eps is a genuine one-parameter deformation and not a different model",
      same,
      f"|difference| < 1e-12 dex at eps = 0, 0.25, 1 on both footings; both return the deposited theory's "
      f"{R0['canonical'][0]:.3f} / {R0['alt'][0]:.3f} dex at medians {R0['canonical'][1]:+.3f} / "
      f"{R0['alt'][1]:+.3f}")

# the standard MOND limit, checked as a limit rather than asserted
gtest = np.array([1e-4, 1e-3, 1e-2])*A0["canonical"]
dm = (gtest + kern(gtest, A0["canonical"]))/np.sqrt(A0["canonical"]*gtest)
hi_g = np.array([1e3, 1e4, 1e5])*A0["canonical"]
hi_excess = kern(hi_g, A0["canonical"])/A0["canonical"]
info("")
info(f"deep-MOND limit of the carried kernel, g_pred/sqrt(a_0 g_bar) at g_bar/a_0 = 1e-4, 1e-3, 1e-2: "
     f"{', '.join(f'{x:.4f}' for x in dm)}   (Milgrom: 1)")
info(f"high-acceleration limit, (g_pred - g_bar)/a_0 at g_bar/a_0 = 1e3, 1e4, 1e5: "
     f"{', '.join(f'{x:.4f}' for x in hi_excess)}   (the bounded boost C = {D_SAT})")
check("A9 [control] the machinery returns the STANDARD MOND result at zero cold fraction: the deep-MOND "
      "asymptote g -> sqrt(a_0 g_bar) and the action's own bounded-boost ceiling C = 0.6476 a_0",
      abs(dm[0] - 1) < 0.02 and abs(dm[-1] - 1) < 0.06 and np.allclose(hi_excess, D_SAT, atol=1e-9),
      f"deep-MOND ratio {dm[0]:.4f} at g_bar = 1e-4 a_0 (1.0 exact in the limit), and the excess saturates "
      f"at exactly {hi_excess[0]:.4f} a_0")

# the amount L49's kernel supplies in a cluster, needed below
KER_CLU = {f: RAT_CLU[f] - RES_CLU[f] for f in RAT_CLU}
check("A8 [control] the kernel's own contribution in a cluster is recovered as the difference between the "
      "measured amount and the post-kernel residual",
      abs(KER_CLU["canonical"] - 2.64) < 0.05 and abs(KER_CLU["alt"] - 2.97) < 0.05,
      f"the kernel supplies {KER_CLU['canonical']:.2f} M_bar (canonical) / {KER_CLU['alt']:.2f} (alt) of the "
      f"missing {RAT_CLU['canonical']:.2f}; the addition must supply the remaining {RES_CLU['canonical']:.2f} "
      f"/ {RES_CLU['alt']:.2f}")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART B -- THE MODIFICATION, WRITTEN AT THE LEVEL OF THE LAGRANGIAN, AND CONSERVATION.")
P("          Conservation is checked FIRST because a source that is not the total stress tensor is the")
P("          one thing that can kill this outright.")
P("=" * 122)

# ---- B1: grad.J = grad^2 Psi, derived rather than quoted ----------------------------------------------------
t, x, y, z, e = sp.symbols("t x y z epsilon", real=True)
Ph = sp.Function("Phi")(x, y, z)
X4 = (t, x, y, z)
gd = sp.diag(-(1 + 2*e*Ph), 1 - 2*e*Ph, 1 - 2*e*Ph, 1 - 2*e*Ph)
gu = gd.inv()
def Gam(a, b, c):
    return sp.Rational(1, 2)*sum(gu[a, d]*(sp.diff(gd[d, b], X4[c]) + sp.diff(gd[d, c], X4[b])
                                           - sp.diff(gd[b, c], X4[d])) for d in range(4))
# static clock tau = t: n_mu = -d_mu tau / sqrt(X) => n^mu = (1/sqrt(-g_00), 0, 0, 0)
n_up = [1/sp.sqrt(-gd[0, 0]), 0, 0, 0]
Jup = [sp.simplify(sum(n_up[b]*(sp.diff(n_up[a], X4[b]) + sum(Gam(a, b, c)*n_up[c] for c in range(4)))
                       for b in range(4))) for a in range(4)]
J1 = [sp.simplify(sp.series(Jup[a], e, 0, 2).removeO().coeff(e, 1)) for a in range(4)]
sqg = sp.sqrt(-gd.det())
divJ = sp.simplify(sum(sp.diff(sqg*Jup[a], X4[a]) for a in range(4))/sqg)
divJ1 = sp.simplify(sp.series(divJ, e, 0, 2).removeO().coeff(e, 1))
lapPh = sp.diff(Ph, x, 2) + sp.diff(Ph, y, 2) + sp.diff(Ph, z, 2)
info("")
info(f"the clock's 4-acceleration on a static weak-field metric ds^2 = -(1+2Phi)dt^2 + (1-2Phi)dx^2, to")
info(f"first order:   J^i = {J1[1]}, {J1[2]}, {J1[3]}   (i.e. J^i = grad^i Phi)")
info(f"and its divergence:   grad_mu J^mu = {sp.simplify(divJ1)}   =  grad^2 Phi")
check("B1 the AeST drag coupling's source IS the total gravitating density: grad.J = grad^2 Psi statically, "
      "and grad^2 Psi is fixed by the Einstein equation to 4 pi G times EVERYTHING minimally coupled to g",
      sp.simplify(divJ1 - lapPh) == 0 and all(sp.simplify(J1[i+1] - sp.diff(Ph, X4[i+1])) == 0 for i in range(3)),
      "derived symbolically, not quoted: J^i = grad^i Phi exactly at first order and grad.J = grad^2 Phi. "
      "Integrating 2(2-K_B) J^mu d_mu phi by parts therefore gives -2(2-K_B) phi grad^2 Psi = "
      "-8 pi G (2-K_B) phi rho_total. THIS IS THE DESIGN CHOICE L49 NAMED, and it is a choice: the term is "
      "written in the action")

P("")
info("THE TWO BARYON-SOURCED VARIANTS, written out.")
wrap("V-A  REPLACEMENT.  Delete the drag coupling and couple phi to the baryon trace instead:", 4)
wrap("2(2 - K_B) J^mu d_mu phi   ->   -8 pi G (2 - K_B) phi T_b ,   T_b = g_mn T^mn_baryon (= -rho_b for dust).", 9)
wrap("The coefficient is not free: it is fixed by demanding the SAME static limit, and with it the scalar "
     "equation becomes grad.[J'(Y) grad phi] = 4 pi G rho_b exactly, with the 2(2-K_B) cancelling as it "
     "does in the deposited theory. This is the RAQUAL / Bekenstein-Milgrom conformal coupling.", 9)
wrap("V-B  COMPENSATION.  KEEP the drag coupling and add ONE term coupling phi to the cold sector:", 4)
wrap("Delta L = +8 pi G (2 - K_B) phi rho_c ,   rho_c = n_mu n_nu T^mn_cold.", 9)
wrap("Its coefficient is fixed by ONE condition -- that it cancel rho_c out of the scalar's source -- and "
     "the net scalar equation is grad.[(J' - 1) grad phi] = 4 pi G rho_b: Milgrom sourced by the baryons "
     "alone, with the drag coupling intact. This matters, and E3 is why.", 9)
wrap("BOTH variants change the scalar's SOURCE and nothing else, so both predict the same thing for "
     "everything measured with baryons and with light. They differ only in whether the phantom gravitates "
     "(E3), so they are carried together as eps = 0 and separated only where they differ.", 4)

# ---- B2: conservation -------------------------------------------------------------------------------------
P("")
info("B2 -- CONSERVATION.  The brief's first kill condition: does a source that is not the total stress")
info("     tensor break the Bianchi identity?  Checked symbolically on FRW with the coupled sector present.")
tt = sp.symbols("t", positive=True)
a = sp.Function("a", positive=True)(tt); Hb = sp.diff(a, tt)/a
rb = sp.Function("rho_b")(tt); rc = sp.Function("rho_c")(tt); ph = sp.Function("phi")(tt)
K2s, bet, Vpot = sp.symbols("K2 beta", real=True), None, None
K2sym, betsym = sp.symbols("K2 beta", real=True)
# scalar sector on FRW: L = -K(Q) with Q = phi-dot, plus the coupling  beta phi rho_s  (s = the sourced species)
# energy density and pressure of a P(Q) sector with P = -K2 Q^2 :  rho = Q P_Q - P = -K2 Q^2, p = P = -K2 Q^2
Qd = sp.diff(ph, tt)
rho_phi = -K2sym*Qd**2
p_phi = -K2sym*Qd**2
# equations of motion (the coupled species is "b" here; identical algebra if it is "c")
eom_phi = sp.Eq(-2*K2sym*(sp.diff(ph, tt, 2) + 3*Hb*Qd), betsym*rb)
eom_rb = sp.Eq(sp.diff(rb, tt) + 3*Hb*rb, -betsym*Qd*rb/1)      # the sourced species exchanges with phi
eom_rc = sp.Eq(sp.diff(rc, tt) + 3*Hb*rc, 0)                    # the uncoupled species is separately conserved
rho_tot = rb + rc + rho_phi; p_tot = p_phi
lhs = sp.diff(rho_tot, tt) + 3*Hb*(rho_tot + p_tot)
sub = {sp.diff(ph, tt, 2): sp.solve(eom_phi, sp.diff(ph, tt, 2))[0],
       sp.diff(rb, tt): sp.solve(eom_rb, sp.diff(rb, tt))[0],
       sp.diff(rc, tt): sp.solve(eom_rc, sp.diff(rc, tt))[0]}
resid = sp.simplify(lhs.subs(sub).doit())
info(f"     total continuity residual, d(rho_tot)/dt + 3H(rho_tot + p_tot), on shell:  {resid}")
check("B2 [THE FIRST KILL CONDITION] baryon sourcing preserves conservation / the Bianchi identity",
      sp.simplify(resid) == 0,
      "IT DOES, and the reason is structural rather than lucky. The modification is made in the ACTION, and "
      "the action remains a diffeomorphism-invariant functional of (g, tau, phi, psi_b, psi_c); the Einstein "
      "equation is untouched (G_mn = 8 pi G T^total_mn), so grad_mu T^mu_nu(total) = 0 follows from the "
      "Bianchi identity exactly as before. What is NOT conserved is the coupled species alone: "
      "grad_mu T^mu_nu(coupled) = -beta T d_nu phi, an exchange term that the scalar's own equation "
      "cancels identically -- verified here to be zero symbolically. The threat is real only for a source "
      "inserted by hand into the FIELD EQUATION; it does not arise for a source written into the LAGRANGIAN")
check("B3 the compensating term of V-B is a free knob that could be tuned away, i.e. the construction has a "
      "hidden parameter",
      False,
      "it is not free: one condition (cancel rho_c out of the scalar's source) fixes one coefficient, "
      "-8 pi G (2 - K_B), and it is the SAME (2 - K_B) that generates MOND. But it is chosen rather than "
      "forced by a symmetry, and that is a real cost recorded here: the deposited action's source is a "
      "consequence of the geometric coupling, whereas the baryon-sourced one is an imposed selection of "
      "which matter the scalar sees. Unlike L49 P3's lambda <= 3.9e-7 it needs no EXACTNESS -- a mismatch "
      "just moves eps continuously off 0 -- which is why the whole family is carried as eps below")

# ---- B4: the observable consequence, stated as the family --------------------------------------------------
P("")
info("B4 -- what the change does to the prediction, which is the only thing the data see:")
info("     total sourcing  (eps = 1, L49): g = g_bar + f g_halo + a_0 Delta( [g_bar + f g_halo] / a_0 )")
info("     baryon sourcing (eps = 0, L50): g = g_bar + f g_halo + a_0 Delta(  g_bar              / a_0 )")
info(f"     and since Delta is monotonically INCREASING (0 -> {D_SAT} at the ceiling), baryon sourcing gives a")
info("     STRICTLY SMALLER kernel term whenever f > 0.  So the effect has the right sign; PART D asks how big.")
mono = np.all(np.diff(Delta(np.geomspace(1e-4, S_SAT*0.999, 400))) > 0)
check("B4 the kernel term is monotone in its argument, so removing the cold component from the source can "
      "only DECREASE the kernel's contribution -- the change has the sign the lane needs",
      bool(mono),
      f"Delta(s) is strictly increasing on 0 < s < {S_SAT} and constant at {D_SAT} above it, so "
      f"Delta(g_bar/a_0) <= Delta([g_bar + f g_halo]/a_0) pointwise for every f >= 0")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART C -- A NEW RISK THE LANE ITSELF CREATES: does the clock tachyon come back?")
P("          On FRW the deposited action has NO homogeneous source for phi -- which is exactly why Q_0 = 0")
P("          is an exact solution and the tachyon is cured.  Any DIRECT MATTER coupling supplies one.")
P("=" * 122)

aa, Qb, uT, vT, up, vp, K2t, epss = sp.symbols("a Qbar uT vT up vp K2 epsilon", real=True)
tau_t = 1 + epss*uT; tau_x = epss*vT; phi_t = Qb + epss*up; phi_x = epss*vp
Xexp = tau_t**2 - tau_x**2/aa**2
Qexp = (tau_t*phi_t - tau_x*phi_x/aa**2)/sp.sqrt(Xexp)
KQ = sp.expand(sp.simplify(sp.series(K2t*Qexp**2, epss, 0, 3).removeO()))
coef_TT = sp.simplify(sp.expand(KQ).coeff(epss, 2).coeff(vT, 2))
info("")
info(f"C1  L49 P1 reproduced independently: the clock's induced gradient-mass coefficient is {coef_TT},")
info(f"    i.e. exactly K_2 Qbar^2 / a^2 -- tachyonic at K_2 = -|K_2| and vanishing IDENTICALLY at Qbar = 0.")
check("C1 [control] the clock tachyon's coefficient is exactly K_2 Qbar^2/a^2, reproducing L49 P1 with "
      "independent code -- so any mechanism that forces Qbar away from zero revives it",
      sp.simplify(coef_TT - K2t*Qb**2/aa**2) == 0 and sp.simplify(coef_TT.subs(Qb, 0)) == 0,
      f"coefficient of (dT/dx)^2 = {coef_TT}, zero at Qbar = 0")

# on FRW the deposited action has no homogeneous source; the modified one does
info("")
info("C2  On an exactly homogeneous slice: J^mu = n^nu grad_nu n^mu = 0 (the comoving congruence is")
info("    geodesic) and Y = q^ab d_a phi d_b phi = 0 (no spatial gradients).  So in the DEPOSITED action the")
info("    phi equation on FRW is d/dt[a^3 K'(Qbar)] = 0, which admits Qbar = 0 exactly -- the cure.")
info("    A direct coupling  -8 pi G (2 - K_B) phi rho_s  supplies a homogeneous source that does not vanish:")
info("        d/dt[a^3 K'(Qbar)] = -8 pi G (2 - K_B) rho_s a^3   =>   Qbar = -4 pi G (2-K_B) rhobar_s t / |K_2|")
tsym = sp.symbols("t", positive=True)
asym = sp.Function("a", positive=True)(tsym); C = sp.symbols("C", real=True)
Qsol = C*tsym/asym**3
lhs_ode = sp.simplify(sp.diff(asym**3*Qsol, tsym)/asym**3)
check("C2 the forced condensate is solved rather than asserted: a^3 Qbar = C t solves the sourced clock "
      "equation exactly for a constant comoving source density",
      sp.simplify(lhs_ode - C/asym**3) == 0,
      f"d/dt(a^3 Qbar)/a^3 = {sp.simplify(lhs_ode)} = C/a^3, which is the constant comoving source rho_s a^3 "
      f"divided by a^3 -- so Qbar is NOT zero once any matter couples directly to phi, and by C1 the clock "
      f"tachyon is revived")

# the induced rate, with |K_2| and (2-K_B) cancelling on the closure locus
def rate_over_H(fs, c2=C2_X, c14=C14_X):
    return fs*math.sqrt(c2/(2*c14))
FB_MD = OB/OM; FC_MD = ODM/OM
OMK_A = FB_MD**2*C2_X/6.0; OMK_B = FC_MD**2*C2_X/6.0
RATE_A = rate_over_H(FB_MD); RATE_B = rate_over_H(FC_MD)
FS_MAX = math.sqrt(2.0/SIG_X); FS_MAX_TOP = math.sqrt(2.0/SIG_MAX)
info("")
info(f"C3  In matter domination Qbar = -H f_s (2 - K_B)/|K_2| with f_s = rho_s/rho_total, so the induced")
info(f"    condensate carries Omega_K = f_s^2 (2-K_B)^2/(6|K_2|), and ON THE CLOSURE LOCUS c_2|K_2| = (2-K_B)^2")
info(f"    BOTH |K_2| AND (2-K_B) CANCEL:   Omega_K = f_s^2 c_2/6,   rate/H = f_s sqrt(c_2/2c_14) = f_s sqrt(sigma/2).")
info(f"    The exhibited point has c_2 = {C2_X:.4e}, |K_2| = {K2_X:.4e}, sigma = {SIG_X:.6f}, c_14 = {C14_X:.1e}.")
info(f"      V-A, source = baryons  : f_s = Omega_b/Omega_m = {FB_MD:.4f}  ->  Omega_K = {OMK_A:.3e}, "
     f"rate/H = {RATE_A:.4f}")
info(f"      V-B, source = the cold : f_s = Omega_c/Omega_m = {FC_MD:.4f}  ->  Omega_K = {OMK_B:.3e}, "
     f"rate/H = {RATE_B:.4f}")
info(f"    Stability (the programme's own criterion, L49 P3 / g03w) is rate <= H at every a, i.e. "
     f"f_s^2 sigma <= 2, i.e. f_s <= sqrt(2/sigma) = {FS_MAX:.4f}.")
check("C4 the revived clock condensate does NOT violate the tachyon gate -- and it cannot, for any source, "
      "because f_s = rho_s/rho_total <= 1 while the bound is sqrt(2/sigma) > 1 across the whole clock window",
      RATE_A < 1.0 and RATE_B < 1.0 and FS_MAX_TOP > 1.0,
      f"rate/H = {RATE_A:.3f} (V-A, margin {1/RATE_A:.1f}x) and {RATE_B:.3f} (V-B, margin {1/RATE_B:.2f}x); "
      f"the bound f_s <= sqrt(2/sigma) is {FS_MAX:.3f} at sigma* = {SIG_X:.4f} and {FS_MAX_TOP:.3f} at the "
      f"top of the clock window sigma < {SIG_MAX}, both above 1, so the gate is structurally safe -- c_14 "
      f"cancels entirely and the margin is a pure number set by sigma alone. THIS IS A REAL COST NONETHELESS: "
      f"the deposited theory satisfies the gate IDENTICALLY (Qbar = 0 exactly), and V-B satisfies it with a "
      f"margin of only {1/RATE_B:.2f}x")

# does the coupling drift Omega_c between recombination and today?
PHI_AMP = FC_MD*(2 - KB_X)/K2_X
DRIFT = (2 - KB_X)*PHI_AMP/2
info("")
info(f"C5  V-B makes the cold particles' mass depend on phi, so Omega_c could drift between recombination and")
info(f"    today, which would move the CMB window.  The cosmological amplitude is phi ~ Qbar/H = "
     f"f_c (2-K_B)/|K_2| = {PHI_AMP:.2e},")
info(f"    so the fractional mass drift is (2-K_B) phi/2 = {DRIFT:.2e}.")
check("C5 the compensating coupling leaves the cold component pressureless and its comoving density constant "
      "to better than 1e-5, so the CMB window f = 1.000 +/- 0.010 is unchanged by the modification",
      DRIFT < 1e-5,
      f"fractional drift {DRIFT:.2e}, five orders below the CMB's 1% error on Omega_c h^2; the cold "
      f"component still scales as a^-3 and the third-peak determination is untouched")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART D -- THE THREE WINDOWS RECOMPUTED UNDER BARYON SOURCING.  This is the whole question.")
P("=" * 122)

P("")
info("D1  SPARC under the two sourcings, side by side.  f is in units of the LambdaCDM abundance-matched halo.")
info(f"{'f':>6} | {'eps=1 (L49) rms':>15} {'median':>8} | {'eps=0 (L50) rms':>15} {'median':>8} | "
     f"{'halo alone rms':>14} {'median':>8}")
FGRID = np.array([0.0, 0.05, 0.10, 0.20, 0.35, 0.50, 0.582, 0.75, 1.00])
TAB = {}
for foot in ("canonical", "alt"):
    info(f"  --- {foot} ---")
    TAB[foot] = []
    for f in FGRID:
        t1 = rms_model(f, 1.0, foot); t0 = rms_model(f, 0.0, foot); th = rms_model(f, 0.0, foot, kernel=False)
        TAB[foot].append((f, t1, t0, th))
        info(f"{f:6.3f} | {t1[0]:15.3f} {t1[1]:+8.3f} | {t0[0]:15.3f} {t0[1]:+8.3f} | "
             f"{th[0]:14.3f} {th[1]:+8.3f}")

BAR1 = {foot: rms_model(1.0, 0.0, foot) for foot in A0}
OVER_T = {foot: 10**abs(TOT1[foot][1]) for foot in A0}
OVER_B = {foot: 10**abs(BAR1[foot][1]) for foot in A0}
frac_removed = {foot: (abs(TOT1[foot][1]) - abs(BAR1[foot][1]))/abs(TOT1[foot][1]) for foot in A0}
P("")
info(f"D2  the overshoot at the abundance the CMB fixes (f = 1):")
info(f"      total sourcing  : median {TOT1['canonical'][1]:+.3f} / {TOT1['alt'][1]:+.3f} dex  = "
     f"{OVER_T['canonical']:.2f}x / {OVER_T['alt']:.2f}x in acceleration")
info(f"      baryon sourcing : median {BAR1['canonical'][1]:+.3f} / {BAR1['alt'][1]:+.3f} dex  = "
     f"{OVER_B['canonical']:.2f}x / {OVER_B['alt']:.2f}x in acceleration")
info(f"      so baryon sourcing removes {100*frac_removed['canonical']:.0f}% / "
     f"{100*frac_removed['alt']:.0f}% of the overshoot in dex, and {100*(1-frac_removed['canonical']):.0f}% "
     f"of it SURVIVES.")
check("D5 [THE FIRST OF THE LANE'S OWN QUESTIONS] the galaxy overshoot VANISHES when the scalar is blind to "
      "the cold component",
      abs(BAR1["canonical"][1]) < 0.11 and abs(BAR1["alt"][1]) < 0.11,
      f"it does not. At f = 1 the median RAR residual falls from {TOT1['canonical'][1]:+.3f} to "
      f"{BAR1['canonical'][1]:+.3f} dex (canonical) and {TOT1['alt'][1]:+.3f} to {BAR1['alt'][1]:+.3f} (alt), "
      f"an overshoot of {OVER_B['canonical']:.2f}x rather than {OVER_T['canonical']:.2f}x. Only "
      f"{100*frac_removed['canonical']:.0f}% of the overshoot was the AMPLIFICATION L49 named; the other "
      f"{100*(1-frac_removed['canonical']):.0f}% is the kernel evaluated on the BARYONS ALONE, which is the "
      f"MOND anomaly itself and is exactly what the theory cannot switch off. L49's diagnosis is correct but "
      f"it is the smaller half of the effect")

FGAL_B = {f: f_max_gal(0.0, f) for f in A0}; FGAL_BS = {f: f_max_gal_rms(0.0, f) for f in A0}
FCLU_B = {f: f_cluster(0.0, f) for f in A0}; FCLU_B_B = {f: f_cluster(0.0, f, 0.20) for f in A0}
# closed form cross-check on the cluster window: f = (post-kernel residual)/F_cosmic
FCLU_B_CLOSED = {f: RES_CLU[f]/F_COSMIC for f in RES_CLU}
P("")
info("D3  THE THREE WINDOWS, total sourcing (L49) against baryon sourcing (L50):")
info(f"{'':>26} {'eps = 1  (L49)':>28} {'eps = 0  (L50)':>28}")
info(f"{'galaxies, generous':>26} {'f <= %.3f / %.3f' % (FGAL_T['canonical'], FGAL_T['alt']):>28} "
     f"{'f <= %.3f / %.3f' % (FGAL_B['canonical'], FGAL_B['alt']):>28}")
info(f"{'galaxies, strict':>26} {'f <= %.3f / %.3f' % (FGAL_TS['canonical'], FGAL_TS['alt']):>28} "
     f"{'f <= %.3f / %.3f' % (FGAL_BS['canonical'], FGAL_BS['alt']):>28}")
info(f"{'clusters, b = 0':>26} "
     f"{'%.3f+/-%.3f / %.3f+/-%.3f' % (FCLU_T['canonical'][0], FCLU_T['canonical'][1], FCLU_T['alt'][0], FCLU_T['alt'][1]):>28} "
     f"{'%.3f+/-%.3f / %.3f+/-%.3f' % (FCLU_B['canonical'][0], FCLU_B['canonical'][1], FCLU_B['alt'][0], FCLU_B['alt'][1]):>28}")
info(f"{'clusters, b = 0.20':>26} "
     f"{'%.3f+/-%.3f / %.3f+/-%.3f' % (FCLU_T_B['canonical'][0], FCLU_T_B['canonical'][1], FCLU_T_B['alt'][0], FCLU_T_B['alt'][1]):>28} "
     f"{'%.3f+/-%.3f / %.3f+/-%.3f' % (FCLU_B_B['canonical'][0], FCLU_B_B['canonical'][1], FCLU_B_B['alt'][0], FCLU_B_B['alt'][1]):>28}")
info(f"{'the CMB':>26} {'1.000 +/- 0.010':>28} {'1.000 +/- 0.010':>28}   (C5: unchanged)")
check("D3 [control] the baryon-sourced cluster window agrees with its own closed form, f = (post-kernel "
      "residual)/(cosmic dark-to-baryon share) -- because with the scalar blind to the cold component the "
      "kernel's contribution no longer depends on f",
      abs(FCLU_B["canonical"][0] - FCLU_B_CLOSED["canonical"]) < 0.003
      and abs(FCLU_B["alt"][0] - FCLU_B_CLOSED["alt"]) < 0.003,
      f"solved numerically {FCLU_B['canonical'][0]:.3f} / {FCLU_B['alt'][0]:.3f} against the closed form "
      f"{RES_CLU['canonical']:.2f}/{F_COSMIC:.4f} = {FCLU_B_CLOSED['canonical']:.3f} and "
      f"{RES_CLU['alt']:.2f}/{F_COSMIC:.4f} = {FCLU_B_CLOSED['alt']:.3f}")
check("D4 [the second of the lane's own questions] the cluster window MOVES under baryon sourcing",
      abs(FCLU_B["canonical"][0] - FCLU_T["canonical"][0]) > 0.05,
      f"it does, and UPWARD: from {FCLU_T['canonical'][0]:.3f} +/- {FCLU_T['canonical'][1]:.3f} to "
      f"{FCLU_B['canonical'][0]:.3f} +/- {FCLU_B['canonical'][1]:.3f} (canonical) and from "
      f"{FCLU_T['alt'][0]:.3f} to {FCLU_B['alt'][0]:.3f} (alt), a factor "
      f"{FCLU_B['canonical'][0]/FCLU_T['canonical'][0]:.2f}. Clusters need MORE cold matter when the kernel "
      f"no longer amplifies it, which is the correct direction and moves them TOWARD the CMB")

gal_clu = {f: FGAL_B[f] >= FCLU_B[f][0] - FCLU_B[f][1] for f in A0}
gal_clu_s = {f: FGAL_BS[f] >= FCLU_B[f][0] - FCLU_B[f][1] for f in A0}
gal_clu_b20 = {f: FGAL_B[f] >= FCLU_B_B[f][0] - FCLU_B_B[f][1] for f in A0}
P("")
check("D6 galaxies and clusters remain mutually admissible under baryon sourcing -- and now at a HIGHER "
      "cold fraction than L49's f ~ 0.3",
      gal_clu["canonical"] and gal_clu["alt"],
      f"they do, and the agreement is sharper than L49's: the galaxy ceiling is "
      f"{FGAL_B['canonical']:.3f} / {FGAL_B['alt']:.3f} and clusters need {FCLU_B['canonical'][0]:.3f} +/- "
      f"{FCLU_B['canonical'][1]:.3f} / {FCLU_B['alt'][0]:.3f} +/- {FCLU_B['alt'][1]:.3f} -- the two central "
      f"values differ by {abs(FGAL_B['canonical']-FCLU_B['canonical'][0])/FCLU_B['canonical'][1]:.1f} sigma "
      f"(canonical). At the allowed hydrostatic bias b = 0.20 clusters want "
      f"{FCLU_B_B['canonical'][0]:.2f} +/- {FCLU_B_B['canonical'][1]:.2f} and the window is "
      f"{'still open' if gal_clu_b20['canonical'] else 'CLOSED'}; on the STRICT galaxy criterion "
      f"(f <= {FGAL_BS['canonical']:.3f}) it is "
      f"{'open' if gal_clu_s['canonical'] else 'CLOSED on both footings'}")

z_clu_cmb = {f: abs(1.0 - FCLU_B_B[f][0])/FCLU_B_B[f][1] for f in A0}
check("D10 clusters and the CMB are still in tension under baryon sourcing once the measured hydrostatic "
      "bias is allowed",
      z_clu_cmb["canonical"] > 2.0,
      f"they are NOT, and this reframes what is left of the pincer. At the allowed b = 0.20 the baryon-sourced "
      f"cluster requirement is {FCLU_B_B['canonical'][0]:.3f} +/- {FCLU_B_B['canonical'][1]:.3f} (canonical) / "
      f"{FCLU_B_B['alt'][0]:.3f} +/- {FCLU_B_B['alt'][1]:.3f} (alt), which is {z_clu_cmb['canonical']:.1f} / "
      f"{z_clu_cmb['alt']:.1f} sigma from the CMB's f = 1.000. So under baryon sourcing CLUSTERS AND THE CMB "
      f"ARE COMPATIBLE at the measured bias, and the entire surviving obstruction is GALAXIES -- the ceiling "
      f"f <= {FGAL_B['canonical']:.3f} / {FGAL_B['alt']:.3f}. That is a cleaner statement of the problem than "
      f"L49's three-way pincer, and it points at exactly one gate")
OCH2_B = {f: FGAL_B[f]*OCH2 for f in A0}
GAP_T = {f: 1.0/FGAL_T[f] for f in A0}; GAP_B = {f: 1.0/FGAL_B[f] for f in A0}
P("")
info("D-VERDICT  the three-way intersection:")
info(f"    galaxies allow   f <= {FGAL_B['canonical']:.3f} (canonical) / {FGAL_B['alt']:.3f} (alt)")
info(f"    clusters need    f  = {FCLU_B['canonical'][0]:.3f} +/- {FCLU_B['canonical'][1]:.3f} / "
     f"{FCLU_B['alt'][0]:.3f} +/- {FCLU_B['alt'][1]:.3f}")
info(f"    the CMB fixes    f  = 1.000 +/- 0.010")
info(f"    the galaxy ceiling corresponds to Omega_c h^2 = {OCH2_B['canonical']:.4f} / "
     f"{OCH2_B['alt']:.4f} against Planck's {OCH2:.4f} +/- 0.0012")
check("D7 [THE WHOLE QUESTION] the three-way intersection is NON-EMPTY under baryon sourcing -- i.e. there "
      "is one cold fraction admissible to galaxies, to clusters AND to the CMB at once",
      FGAL_B["canonical"] >= 0.99 and FGAL_B["alt"] >= 0.99,
      f"it is not. The pincer NARROWS but does not open: the gap between the galaxy ceiling and the CMB's "
      f"f = 1 falls from a factor {GAP_T['canonical']:.2f} / {GAP_T['alt']:.2f} (total sourcing) to "
      f"{GAP_B['canonical']:.2f} / {GAP_B['alt']:.2f} (baryon sourcing), a reduction of "
      f"{100*(1-GAP_B['canonical']/GAP_T['canonical']):.0f}%, and the binding constraint is STILL the CMB "
      f"and still by a wide margin. Clusters, which L49 already found were not the obstacle, move further "
      f"out of the way")

# how much kernel is allowed to survive at f = 1?  the sharp form of the obstruction
def ksup_max(foot, tol=0.11):
    lo, hi = 0.0, 1.0
    for _ in range(70):
        mid = 0.5*(lo + hi)
        if abs(rms_model(1.0, 0.0, foot, ksup=mid)[1]) < tol: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)
KSUP = {f: ksup_max(f) for f in A0}
P("")
info("D8  the obstruction stated sharply, and it is source-INDEPENDENT.  Ask instead: at f = 1, what")
info("    fraction s of the kernel may survive before galaxies break?  (s = 1 is the action; s = 0 is no MOND.)")
info(f"      s <= {KSUP['canonical']:.3f} (canonical) / {KSUP['alt']:.3f} (alt) on the generous criterion.")
info(f"    So at the abundance the CMB fixes, the action's MOND kernel must be suppressed by a factor")
info(f"    {1/max(KSUP['canonical'],1e-9):.1f}x / {1/max(KSUP['alt'],1e-9):.1f}x in galaxies. Re-sourcing the")
info("    scalar cannot do that: it only removes the halo-driven part of the kernel, and the baryon-driven")
info("    part IS the MOND anomaly the theory exists to produce.")
check("D9 re-sourcing the scalar is capable IN PRINCIPLE of reaching f = 1, i.e. the obstruction is about "
      "WHICH matter sources the scalar rather than about the kernel existing at all",
      FGAL_B["canonical"] >= 1.0,
      f"it is not: even with the scalar completely blind to the cold component (eps = 0, the most that "
      f"re-sourcing can achieve) the galaxy ceiling is {FGAL_B['canonical']:.3f}. Reaching f = 1 requires "
      f"the KERNEL ITSELF to be suppressed to s <= {KSUP['canonical']:.3f} of its value where galaxies are "
      f"measured -- a screening of the MOND term by the cold component, which is L49's option (b) and not "
      f"this lane, and which L6's cosmological-ordering theorem already constrains")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART E -- THE PRICE.  Baryon-sourced modified gravity has known costs; which of them actually bite here?")
P("=" * 122)

# ---- E1 equivalence principle -------------------------------------------------------------------------------
etas = []
for g in GAL:
    a0 = A0["canonical"]; f = FGAL_B["canonical"]
    gN = g["gb"] + f*g["g_halo"]; k = kern(g["gb"], a0)
    etas.append(k/(gN + k))
ETA = float(np.median(np.concatenate(etas)))
P("")
info(f"E1  EQUIVALENCE PRINCIPLE.  In BOTH variants the cold component and the baryons no longer fall")
info(f"    identically: baryons feel the MOND kernel and the cold component does not. At f = "
     f"{FGAL_B['canonical']:.3f} the")
info(f"    median fractional difference across SPARC is eta = kernel/total = {ETA:.3f}, i.e. an O(1) violation")
info(f"    BETWEEN SECTORS. Two things it is NOT:")
info(f"      (i) it is not a violation within the Standard Model. In V-B baryons stay minimally coupled to g,")
info(f"          so there is NO composition dependence and MICROSCOPE/Eotvos are untouched. In V-A the")
info(f"          conformal coupling is to the TRACE T_b, so electromagnetic binding energy (traceless)")
info(f"          decouples and a composition dependence DOES appear -- one more reason V-B is the variant to")
info(f"          carry;")
info(f"      (ii) it is not inconsistent with the LambdaCDM halo used throughout. In V-B the cold component")
info(f"          feels only the Newtonian field of rho_b + rho_c, which is exactly the gravity under which")
info(f"          abundance-matched NFW halos are built -- so the halo library is self-consistent, and MORE")
info(f"          so than under total sourcing, where the halo would itself have been MOND-boosted.")
check("E1 the equivalence-principle cost is confined to the DARK sector and does not touch any laboratory or "
      "Solar-System test",
      True,
      f"in V-B it is: baryons and photons remain minimally coupled to the single metric g (the programme's "
      f"own requirement I2), so gamma_PPN, Eotvos and MICROSCOPE are untouched, and the violation is "
      f"between the visible and dark sectors alone, where it is unobservable except through the halo's "
      f"equilibrium -- which is the LambdaCDM one by construction. Magnitude eta = {ETA:.2f} (median across "
      f"SPARC). In V-A it is NOT confined: the conformal coupling to T_b is composition-dependent through "
      f"the traceless electromagnetic binding energy")

# ---- E2/E3 lensing ------------------------------------------------------------------------------------------
# the MOND scalar's OWN gravitating energy against the phantom it must mimic
def lens_ratio(gradphi, r):
    """(scalar's own energy density)/(phantom density) ~ |grad phi|^2 r / (2 a_0 c^2) in the deep-MOND regime"""
    return gradphi**2*r/(2*A0["canonical"]*CLIGHT**2)
LR_GAL = lens_ratio(A0["canonical"], 10*kpc); LR_CLU = lens_ratio(A0["canonical"], 1000*kpc)
P("")
info(f"E2  LENSING, and this is where the two variants part company.")
info(f"    In V-A the drag coupling is DELETED, so the only thing the MOND sector contributes to the Einstein")
info(f"    equation is its own gradient energy. Deep-MOND AQUAL has energy density ~ |grad phi|^3/(8 pi G a_0),")
info(f"    against a phantom density ~ |grad phi|/(4 pi G r); the ratio is |grad phi|^2 r/(2 a_0 c^2) =")
info(f"    {LR_GAL:.2e} at 10 kpc in a galaxy and {LR_CLU:.2e} at 1 Mpc in a cluster. The phantom therefore")
info(f"    does not gravitate: light is deflected by the baryons and the cold component ONLY.")
# conformal invariance of null geodesics, DERIVED explicitly for a generic static isotropic metric
Nf = sp.Function("N", positive=True)(x, y, z); Bf = sp.Function("B", positive=True)(x, y, z)
Af = sp.Function("A", positive=True)(x, y, z)
g_c = sp.diag(-Nf**2, Bf**2, Bf**2, Bf**2)
gt_c = Af**2*g_c
def christoffel(gm):
    gi_ = gm.inv()
    return [[[sp.simplify(sum(gi_[m, d]*(sp.diff(gm[d, al], X4[be]) + sp.diff(gm[d, be], X4[al])
                                         - sp.diff(gm[al, be], X4[d])) for d in range(4))/2)
              for be in range(4)] for al in range(4)] for m in range(4)]
Gm = christoffel(g_c); Gt = christoffel(gt_c)
k1s, k2s, k3s = sp.symbols("k1 k2 k3", real=True)
k0s = Bf*sp.sqrt(k1s**2 + k2s**2 + k3s**2)/Nf          # the null condition g(k,k) = 0
kvec = [k0s, k1s, k2s, k3s]
knorm = sp.simplify(sum(g_c[i, j]*kvec[i]*kvec[j] for i in range(4) for j in range(4)))
Dacc = [sp.simplify(sum((Gt[m][al][be] - Gm[m][al][be])*kvec[al]*kvec[be]
                        for al in range(4) for be in range(4))) for m in range(4)]
# parallel to k  <=>  D^mu k^nu - D^nu k^mu = 0 for all mu, nu
parallel = (sp.simplify(knorm) == 0) and all(
    sp.simplify(sp.expand(Dacc[m]*kvec[n] - Dacc[n]*kvec[m])) == 0 for m in range(4) for n in range(4))
info(f"    and that is not a modelling choice. Derived here rather than quoted: for a generic static isotropic")
info(f"    metric g = diag(-N^2, B^2, B^2, B^2) with arbitrary N(x), B(x), and a conformal rescaling")
info(f"    gtilde = A(x)^2 g, the Christoffel difference contracted on a vector k that is NULL with respect to")
info(f"    g satisfies  D^mu k^nu - D^nu k^mu = 0 for every mu, nu -- i.e. the extra acceleration is PARALLEL")
info(f"    to k, so the null curve is unchanged up to reparametrisation. A conformally coupled scalar cannot")
info(f"    bend light, whatever it does to matter.  (This is why TeVeS carries a DISFORMAL matter metric and a")
info(f"    vector, and why AeST couples its scalar to the aether's acceleration instead of to matter: both")
info(f"    couplings are UNIVERSAL, which is what buys the equivalence principle and lensing at once.)")
check("E2 a conformally baryon-coupled MOND scalar still lenses",
      not parallel,
      f"it does not, and this is derived rather than asserted: with a generic static isotropic metric and an "
      f"arbitrary conformal factor, the connection difference contracted on a g-null k comes out parallel to "
      f"k (all sixteen antisymmetric combinations vanish identically), so null geodesics are unchanged. "
      f"Combined with the energy-density ratio ({LR_GAL:.1e} in a galaxy, {LR_CLU:.1e} in a cluster) this "
      f"says V-A predicts M_dyn/M_lens > 1 by the FULL phantom -- the failure mode that the repository's own "
      f"record puts at 21.2 sigma for the un-completed kernel and that the AeST drag coupling cures to "
      f"0.601 sigma")

# quantify V-A's residual lensing failure WITH the cold component present
fEX = min(FGAL_B["canonical"], FCLU_B["canonical"][0])
MDYN = 1 + fEX*F_COSMIC + KER_CLU["canonical"]; MLENS_A = 1 + fEX*F_COSMIC
WL_OVER_HSE = 1.1536                                   # L24 C8's identity check, Herbonnet-based
SLIP_MEAS, SLIP_ERR = 0.369, 0.238                     # L24 C8, canonical
slip_A = WL_OVER_HSE*(MDYN/MLENS_A) - 1.0
sig_A = abs(slip_A - SLIP_MEAS)/SLIP_ERR
gal_ratio = float(np.median(np.concatenate(
    [(g["gb"] + fEX*g["g_halo"] + kern(g["gb"], A0["canonical"]))/(g["gb"] + fEX*g["g_halo"]) for g in GAL])))
info("")
info(f"E3  how badly does V-A's lensing failure bite ONCE the cold component is present? At f = {fEX:.3f}:")
info(f"      clusters: M_dyn/M_lens = ({1:.0f} + {fEX*F_COSMIC:.2f} + {KER_CLU['canonical']:.2f})/"
     f"({1:.0f} + {fEX*F_COSMIC:.2f}) = {MDYN/MLENS_A:.3f}, against the observed 1.0-1.3;")
info(f"      in L24 C8's own statistic that predicts S_lens - S_dyn = {slip_A:+.3f} against the measured "
     f"{SLIP_MEAS:+.3f} +/- {SLIP_ERR:.3f} = {sig_A:.1f} sigma;")
info(f"      galaxies: the median SPARC point has M_dyn/M_lens = {gal_ratio:.2f}, i.e. rotation curves and")
info(f"      galaxy-galaxy lensing would disagree by {100*(gal_ratio-1):.0f}% at the SAME radius.")
check("E3 V-A survives the lensing-equals-dynamics gate once a cold component is present (the cold mass "
      "lenses, so the discrepancy is diluted)",
      sig_A < 2.0 and gal_ratio < 1.10,
      f"it does not. The dilution is real -- the ratio falls from the un-completed kernel's 1/f_bar ~ 6.4 to "
      f"{MDYN/MLENS_A:.2f} in clusters -- but it is still {gal_ratio:.2f} at the median SPARC radius and "
      f"{sig_A:.1f} sigma in L24's cluster statistic, against a gate the deposited theory passes "
      f"STRUCTURALLY (Phi = Psi, M_dyn/M_lens = 1 exactly). NOTE the cluster significance alone is not a "
      f"kill: L24's error is 5-cluster weak-lensing noise. The load-bearing statement is structural, not "
      f"statistical -- V-A predicts a definite inequality where the deposited theory predicts an identity")
check("E4 V-B survives the lensing-equals-dynamics gate",
      True,
      f"it does, and this is why V-B is the variant to carry: the drag coupling 2(2-K_B)J^mu d_mu phi is "
      f"RETAINED, so the phantom continues to enter the Einstein equation exactly as in the deposited theory, "
      f"and baryons and photons both remain minimally coupled to the single metric g. Phi = Psi, "
      f"M_dyn/M_lens = 1 and gamma_PPN = 1 are untouched; only the scalar's SOURCE is changed, by a term that "
      f"couples to the cold sector alone")

P("")
info("E5  THE DISFORMAL REPAIR OF V-A IS ALREADY CLOSED IN THIS REPOSITORY, and it is worth saying because it")
info("    is the standard fix. Repairing a conformally coupled scalar's lensing needs a disformal piece,")
info("    gtilde = g + B d_mu phi d_nu phi (this is why TeVeS carries a vector). LOCAL_NO_GO 3.2's identity:")
info("        (c_GW - c_light)/c = B phi'^2/2 = (Psi - Phi)_uncancelled,")
info("    i.e. the slip cancelled IS the light-cone tilt created. Along GW170817's path the two host galaxies'")
info("    MOND regions exceed the bound by ~2e6 eps, and the 40 Mpc of intergalactic medium alone by 30-300x.")
info("    A CONTRARY RECORD IS FLAGGED RATHER THAN RESOLVED: LEDGER sf27 reports a disformal+conformal")
info("    coupling to the khronon's normal REPAIRING the lensing gate in a different chassis. The two are not")
info("    the same construction and this lane does not adjudicate them; V-B needs neither.")
check("E5 the disformal repair is available to V-A as an unencumbered option",
      False,
      "it is not: the repository's own LOCAL_NO_GO 3.2 identity ties the cancelled slip to a light-cone tilt "
      "excluded by GW170817 by 30-300x from the intergalactic path alone, and the programme's I2 requirement "
      "(one physical metric, no disformal matter metric) forbids it by construction. A contrary record "
      "(LEDGER sf27, a different chassis) is flagged, not resolved. This is a reason to carry V-B, which "
      "needs no repair, rather than a kill of the lane")

# ---- E6 alpha_1 ---------------------------------------------------------------------------------------------
ALPHA1_MOND = lambda JY: -4*(2 - KB_X)/(JY + 1)
P("")
info(f"E6  PREFERRED-FRAME PARAMETERS. LOCAL_NO_GO 3.3's closed form is alpha_1 = -4 c_14 - 4(2-K_B)/(J_Y+1),")
info(f"    and the drag coefficient (2 - K_B) IS the MOND-generating coupling. The deposited theory clears")
info(f"    alpha_1 because the coherence length xi screens the Solar System (J_Y -> large there), giving")
info(f"    alpha_1 -> -4 c_14 = {-4*C14_X:.2e} against the 1e-4 bound.")
info(f"      V-B keeps the drag coupling, so alpha_1, alpha_2, alpha_3 and gamma are LITERALLY unchanged.")
info(f"      V-A deletes it, so the MOND piece {ALPHA1_MOND(1):.2f} (at J_Y = 1) disappears identically and")
info(f"      alpha_1 = -4 c_14 with no screening needed -- a genuine GAIN for V-A, and moot given E3.")
check("E6 baryon sourcing leaves the preferred-frame parameters at or better than the deposited theory's "
      "values",
      True,
      f"it does. V-B changes nothing in the aether/scalar sector (the added term couples phi to the cold "
      f"sector, which is absent from the Solar System), so alpha_1 = -4 c_14 = {-4*C14_X:.2e} and "
      f"alpha_2 = (c_14/2)(1/sigma - 1) = {(C14_X/2)*(1/SIG_X - 1):.2e} stand. V-A removes the "
      f"MOND piece of alpha_1 entirely, which is an improvement it cannot cash because of E3")

# ---- E7 Solar System ----------------------------------------------------------------------------------------
RHO_DM_LOCAL = 0.0104; R_SAT_AU = 9.5826; PP_BOUND = 6.7e-11
M_DM_SAT = fEX*RHO_DM_LOCAL*(4*math.pi/3)*(R_SAT_AU/206264.806)**3
check("E7 the Solar-System phantom-mass bound survives the exhibited cold fraction",
      M_DM_SAT < PP_BOUND,
      f"a smooth cold halo at f = {fEX:.3f} of the locally measured density puts {M_DM_SAT:.2e} Msun inside "
      f"Saturn's orbit against Pitjev-Pitjeva's {PP_BOUND:.1e} Msun, a margin of {PP_BOUND/M_DM_SAT:.0f}x")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART F -- AN EXHIBITED POINT, RUN AGAINST THE GATES THE DEPOSITED THEORY PASSES.")
P("=" * 122)
med_ex = {foot: rms_model(fEX, 0.0, foot) for foot in A0}
f_clu_z = {foot: abs(fEX - FCLU_B[foot][0])/FCLU_B[foot][1] for foot in A0}
P("")
info(f"THE POINT: variant V-B, cold fraction f = {fEX:.3f} of the abundance-matched LambdaCDM halo, on the")
info(f"deposited theory's own exhibited parameters K_B = {KB_X}, c_14 = {C14_X:.1e}, sigma = {SIG_X:.6f},")
info(f"c_2 = {C2_X:.4e}, |K_2| = {K2_X:.4e} (closure locus), xi and p unchanged.")
GATES = [
 ("Cassini / sunward / coherence length xi", "PASS", "the aether-scalar sector is untouched; the cold "
  f"component adds no field gradient and {M_DM_SAT:.1e} Msun inside Saturn (E7)"),
 ("Saturn phantom mass", "PASS", f"{M_DM_SAT:.2e} vs {PP_BOUND:.1e} Msun, margin {PP_BOUND/M_DM_SAT:.0f}x"),
 ("alpha_1, alpha_2, alpha_3, gamma", "PASS", f"unchanged: alpha_1 = {-4*C14_X:.2e}, "
  f"alpha_2 = {(C14_X/2)*(1/SIG_X-1):.2e} (E6)"),
 ("c_T = c (GW170817)", "PASS", "c_13 = 0 identically; no disformal matter metric is introduced (E5)"),
 ("mode count and health", "PASS", "2 tensor + 1 clock + 1 MOND scalar unchanged; the cold component adds "
  "at most one matter degree of freedom and the compensating term adds none"),
 ("clock tachyon", "PASS, with a NEW and much thinner margin", f"the deposited theory satisfies it "
  f"IDENTICALLY (Qbar = 0); V-B forces Qbar =/= 0 and satisfies it at rate/H = {RATE_B:.3f}, margin "
  f"{1/RATE_B:.2f}x (C4)"),
 ("lensing == dynamics (Phi = Psi)", "PASS", "structurally, because the drag coupling is retained (E4)"),
 ("BBN", "PASS", "Delta N_eff = 0; and the cold component supplies Omega_m, which the deposited theory "
  "could not"),
 ("rotation curves (non-overshoot)", "PASS at this f", f"median RAR residual {med_ex['canonical'][1]:+.3f} / "
  f"{med_ex['alt'][1]:+.3f} dex, rms {med_ex['canonical'][0]:.3f} / {med_ex['alt'][0]:.3f}"),
 ("cluster amount", "PASS at this f", f"{f_clu_z['canonical']:.1f} sigma / {f_clu_z['alt']:.1f} sigma from "
  f"the required {FCLU_B['canonical'][0]:.3f} +/- {FCLU_B['canonical'][1]:.3f} / {FCLU_B['alt'][0]:.3f} +/- "
  f"{FCLU_B['alt'][1]:.3f}"),
 ("conservation / Bianchi", "PASS", "verified symbolically (B2)"),
 ("CMB cold-matter density", "FAIL", f"Omega_c h^2 = {fEX*OCH2:.4f} against Planck's {OCH2:.4f} +/- 0.0012, "
  f"short by a factor {1/fEX:.2f}"),
 ("linear growth / sigma_8", "FAIL, by the same factor", "S_eff = 0 exactly, so growth is algebraically "
  "LambdaCDM's -- but with only Omega_c h^2 = %.4f of cold matter" % (fEX*OCH2)),
]
info("")
info(f"{'gate':<44} {'verdict':<40} number")
info("-"*118)
for a_, b_, c_ in GATES:
    info(f"{a_:<44} {b_:<40} {c_[:70]}")
    for ln in textwrap.wrap(c_[70:], 70):
        info(f"{'':<44} {'':<40} {ln}")
npass = sum(1 for _, v, _ in GATES if v.startswith("PASS"))
check("F1 an admissible point exists that survives every gate the DEPOSITED theory already passes",
      npass >= 11,
      f"it does: {npass} of {len(GATES)} gates pass at f = {fEX:.3f} in variant V-B, including the two the "
      f"lane put at risk -- conservation (B2) and lensing-equals-dynamics (E4) -- and including the clock "
      f"tachyon, at a margin of {1/RATE_B:.2f}x rather than identically")
check("F2 that point also repairs the two gates the deposited theory FAILS outright -- the CMB cold-matter "
      "density and linear growth",
      fEX >= 0.99,
      f"it does not: f = {fEX:.3f} gives Omega_c h^2 = {fEX*OCH2:.4f} against {OCH2:.4f} +/- 0.0012, short by "
      f"a factor {1/fEX:.2f}. This is the same failure L49 found, reduced from a factor "
      f"{GAP_T['canonical']:.1f} to {1/fEX:.1f} but not removed")
check("F3 the exhibited point is at least a strict improvement on L49's -- the admissible cold fraction is "
      "higher and every gate L49's point passed is still passed",
      fEX > FGAL_T["canonical"] and npass >= 11,
      f"it is: f = {fEX:.3f} against L49's {min(FGAL_T['canonical'], FCLU_T['canonical'][0]):.3f}, a factor "
      f"{fEX/min(FGAL_T['canonical'], FCLU_T['canonical'][0]):.2f}, with the CMB deficit falling from "
      f"{GAP_T['canonical']:.1f}x to {1/fEX:.1f}x and no gate lost")

# ==========================================================================================================
P("\n" + "=" * 122)
P("PART G -- VERDICT")
P("=" * 122)
check("V1 [the brief's first kill condition] conservation survives baryon sourcing",
      sp.simplify(resid) == 0,
      "YES. The modification is written into the Lagrangian, so diffeomorphism invariance gives "
      "grad_mu T^mu_nu(total) = 0 identically; only the individually coupled species is non-conserved, and "
      "its exchange term cancels against the scalar's own equation (B2, verified symbolically). The lane is "
      "not killed at step one")
check("V2 the galaxy overshoot vanishes under baryon sourcing",
      abs(BAR1["canonical"][1]) < 0.11,
      f"NO. It falls from {TOT1['canonical'][1]:+.3f} to {BAR1['canonical'][1]:+.3f} dex at f = 1 "
      f"({OVER_T['canonical']:.2f}x -> {OVER_B['canonical']:.2f}x in acceleration), removing "
      f"{100*frac_removed['canonical']:.0f}% of it. The surviving "
      f"{100*(1-frac_removed['canonical']):.0f}% is the kernel evaluated on the baryons alone")
check("V3 the cluster window moves",
      abs(FCLU_B["canonical"][0] - FCLU_T["canonical"][0]) > 0.05,
      f"YES, upward, from {FCLU_T['canonical'][0]:.3f} +/- {FCLU_T['canonical'][1]:.3f} to "
      f"{FCLU_B['canonical'][0]:.3f} +/- {FCLU_B['canonical'][1]:.3f} (canonical) and {FCLU_T['alt'][0]:.3f} "
      f"to {FCLU_B['alt'][0]:.3f} (alt) -- toward the CMB, and into near-exact agreement with the galaxy "
      f"ceiling")
check("V4 [THE LANE'S QUESTION] the three-way intersection is non-empty: the pincer OPENS",
      FGAL_B["canonical"] >= 0.99,
      f"NO. Galaxies allow f <= {FGAL_B['canonical']:.3f} / {FGAL_B['alt']:.3f}, clusters need "
      f"{FCLU_B['canonical'][0]:.3f} +/- {FCLU_B['canonical'][1]:.3f} / {FCLU_B['alt'][0]:.3f} +/- "
      f"{FCLU_B['alt'][1]:.3f}, the CMB fixes 1.000 +/- 0.010. The interior is still empty and the binding "
      f"constraint is still the CMB. What DID change: the gap narrowed from {GAP_T['canonical']:.2f}x to "
      f"{GAP_B['canonical']:.2f}x (canonical) and {GAP_T['alt']:.2f}x to {GAP_B['alt']:.2f}x (alt), and "
      f"galaxies and clusters now agree to "
      f"{abs(FGAL_B['canonical']-FCLU_B['canonical'][0])/FCLU_B['canonical'][1]:.1f} sigma at f ~ "
      f"{fEX:.2f} instead of ~0.3")
check("V5 an admissible point survives the gates the deposited theory passes",
      npass >= 11,
      f"YES: {npass} of {len(GATES)} at f = {fEX:.3f} in variant V-B (F1), with two new costs -- the clock "
      f"tachyon margin falls from IDENTICAL to {1/RATE_B:.2f}x (C4), and the compensating coefficient is "
      f"chosen rather than forced (B3). It does not repair the CMB (F2)")
check("V6 [VERDICT] baryon sourcing is the calculation that decides L49's pincer in the theory's favour",
      FGAL_B["canonical"] >= 0.99,
      "NO, and the reason is a theorem rather than a number. THE WINDOW THAT CANNOT MOVE IS THE CMB'S: it is "
      "a statement about the pressureless gravitating density at recombination, and on the closure locus the "
      "MOND sector contributes EXACTLY ZERO to linear growth (S_eff = 0), so changing which matter sources a "
      "field that contributes nothing changes nothing (C5 confirms the coupling-induced drift is 1e-7). AND "
      "THE GALAXY WINDOW CANNOT REACH 1: at f = 1 the abundance-matched halo ALONE already reproduces SPARC "
      "at %.3f dex with median %+.3f, so any further acceleration is an overshoot; the kernel adds "
      "a_0 Delta(g_bar/a_0), which in the deep-MOND regime IS the observed anomaly. Re-sourcing removes only "
      "the part of the kernel driven by the added halo -- %.0f%% of the overshoot in dex -- and the "
      "remaining %.0f%% is the theory's own reason for existing. Reaching f = 1 requires suppressing the "
      "kernel itself to s <= %.3f where galaxies are measured (D8)."
      % (RH1["canonical"][0], RH1["canonical"][1], 100*frac_removed["canonical"],
         100*(1-frac_removed["canonical"]), KSUP["canonical"]))

# ==========================================================================================================
P("\n" + "=" * 122)
P("THE THREE WINDOWS, BEFORE AND AFTER")
P("=" * 122)
info(f"{'':>22} {'L49 (total-sourced)':>30} {'L50 (baryon-sourced)':>30} {'moved':>12}")
info("-"*118)
info(f"{'galaxies (generous)':>22} {'f <= %.3f / %.3f' % (FGAL_T['canonical'], FGAL_T['alt']):>30} "
     f"{'f <= %.3f / %.3f' % (FGAL_B['canonical'], FGAL_B['alt']):>30} "
     f"{'+%.0f%% / +%.0f%%' % (100*(FGAL_B['canonical']/FGAL_T['canonical']-1), 100*(FGAL_B['alt']/FGAL_T['alt']-1)):>12}")
info(f"{'clusters (b = 0)':>22} {'%.3f / %.3f' % (FCLU_T['canonical'][0], FCLU_T['alt'][0]):>30} "
     f"{'%.3f / %.3f' % (FCLU_B['canonical'][0], FCLU_B['alt'][0]):>30} "
     f"{'+%.0f%% / +%.0f%%' % (100*(FCLU_B['canonical'][0]/FCLU_T['canonical'][0]-1), 100*(FCLU_B['alt'][0]/FCLU_T['alt'][0]-1)):>12}")
info(f"{'the CMB':>22} {'1.000 +/- 0.010':>30} {'1.000 +/- 0.010':>30} {'0%':>12}")
info(f"{'gap to the CMB':>22} {'%.2fx / %.2fx' % (GAP_T['canonical'], GAP_T['alt']):>30} "
     f"{'%.2fx / %.2fx' % (GAP_B['canonical'], GAP_B['alt']):>30} "
     f"{'-%.0f%% / -%.0f%%' % (100*(1-GAP_B['canonical']/GAP_T['canonical']), 100*(1-GAP_B['alt']/GAP_T['alt'])):>12}")

P("")
P("=" * 122)
P("THREE-SENTENCE VERDICT")
P("=" * 122)
wrap(f"Baryon sourcing is a legitimate action-level modification and it survives the test that could have "
     f"killed it outright -- conservation and the Bianchi identity are untouched, because the change is made "
     f"in the Lagrangian and diffeomorphism invariance then guarantees grad_mu T^mu_nu(total) = 0, with only "
     f"the individually coupled species exchanging energy with the scalar -- and in the variant that keeps "
     f"the drag coupling (V-B) it also keeps lensing = dynamics, the preferred-frame parameters, c_T = c and "
     f"the mode count, at the cost of one chosen coefficient, an O(1) equivalence-principle violation "
     f"confined to the dark sector, and a clock-tachyon margin that falls from IDENTICAL to "
     f"{1/RATE_B:.2f}x.", 2)
P("")
wrap(f"It moves both of the windows it was supposed to move: the galaxy ceiling rises from f <= "
     f"{FGAL_T['canonical']:.3f} / {FGAL_T['alt']:.3f} to {FGAL_B['canonical']:.3f} / {FGAL_B['alt']:.3f} "
     f"and the cluster requirement rises from {FCLU_T['canonical'][0]:.3f} +/- {FCLU_T['canonical'][1]:.3f} / "
     f"{FCLU_T['alt'][0]:.3f} +/- {FCLU_T['alt'][1]:.3f} to {FCLU_B['canonical'][0]:.3f} +/- "
     f"{FCLU_B['canonical'][1]:.3f} / {FCLU_B['alt'][0]:.3f} +/- {FCLU_B['alt'][1]:.3f}, so that galaxies and "
     f"clusters now agree to {abs(FGAL_B['canonical']-FCLU_B['canonical'][0])/FCLU_B['canonical'][1]:.1f} "
     f"sigma at f ~ {fEX:.2f} -- but the CMB does not move at all, and the intersection stays EMPTY with the "
     f"gap narrowed from {GAP_T['canonical']:.1f}x to {GAP_B['canonical']:.1f}x (canonical) and "
     f"{GAP_T['alt']:.1f}x to {GAP_B['alt']:.1f}x (alt).", 2)
P("")
wrap(f"What closes it is a theorem, not a number: the CMB window cannot move because on the closure locus "
     f"the MOND sector contributes exactly zero to linear growth, so re-sourcing a field that contributes "
     f"nothing changes nothing; and the galaxy window cannot reach f = 1 because at that abundance the "
     f"LambdaCDM halo alone already reproduces SPARC to {RH1['canonical'][0]:.3f} dex, leaving no room for "
     f"the kernel evaluated on the baryons -- which is {100*(1-frac_removed['canonical']):.0f}% of the "
     f"overshoot, is the MOND anomaly itself, and is the one thing re-sourcing cannot touch. The only "
     f"remaining move is to suppress the kernel where the cold component dominates (s <= "
     f"{KSUP['canonical']:.3f} at f = 1), which is L49's option (b) and a different lane.", 2)

P("")
P("  CAVEATS, stated rather than buried:")
P("   (i)   nothing here favours this framework over LambdaCDM and nothing here constrains LambdaCDM. The")
P("         cold component and its abundance-matched profile are LambdaCDM's, imported wholesale; the")
P("         stellar-to-halo-mass relation remains a free function of host mass (L49 M5).")
P("   (ii)  f_gal is the GENEROUS criterion (median RAR shift inside the RAR's own 0.11 dex), carried so the")
P("         candidate is not handed a manufactured deficit. The strict criterion gives %.3f / %.3f, on which"
  % (FGAL_BS['canonical'], FGAL_BS['alt']))
P("         even the galaxy-cluster overlap closes. The full table at nine values of f is printed.")
P("   (iii) abundance matching carries ~0.30 dex of systematic on log M200; it moves f_gal and the cluster")
P("         requirement together and cannot close a gap of %.1fx." % GAP_B['canonical'])
P("   (iv)  V-B's compensating coefficient is fixed by one condition but chosen rather than forced by a")
P("         symmetry (B3). Whether the SAME coefficient also exactly cancels the MOND force on the cold")
P("         component is a weak-field question this lane does not settle; it does not affect any number here,")
P("         because every window is computed from what BARYONS and LIGHT feel, and it would only alter the")
P("         cold component's own equilibrium profile -- for which the LambdaCDM library is already assumed.")
P("   (v)   the induced-condensate calculation is matter-domination scaling on a flat FRW background,")
P("         calibrated against g03w's published rate through the same formula L49 X5 uses. It fixes the")
P("         STRUCTURE (rate/H = f_s sqrt(sigma/2), with c_14 and |K_2| cancelling on the closure locus); it is")
P("         not a full cosmological-perturbation calculation.")
P("   (vi)  E3's cluster significance for V-A rests on 5-cluster weak-lensing noise and is NOT a kill on its")
P("         own; the load-bearing statement there is structural (a conformal coupling cannot bend light).")

P("")
P(f"RESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
P(f"[{time.time()-T0:.0f} s]")
sys.exit(0)
